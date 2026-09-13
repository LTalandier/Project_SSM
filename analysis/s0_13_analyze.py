#!/usr/bin/env python3
"""Consume all corrected PAT units with hashed, unchanged historical controls.

Fails closed on incomplete grids, duplicate seeds, source mismatch, nonfinite
metrics, or a failed base-scale reproducibility anchor. Does not overwrite S0.10.
"""
from pathlib import Path
import copy
import hashlib
import json
import math
import statistics
import sys
import torch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from analysis.s0_10_analyze import paired_ci

SEEDS=(11,23,47,61,83,101,127,151)
LEVELS=(1,2,3,4,6)
TARGET=0.005651
OUT=ROOT/'results/s0_13'


def read_row(path,method,seed,m,corrected=False,source_commit=None):
    d=json.loads(path.read_text())
    for key,value in [('method',method),('seed',seed),('mismatch_scale',m),('n_updates',31600),('cell','C-2')]:
        if d.get(key)!=value:raise ValueError(f'{path}: wrong {key}')
    if corrected:
        if d.get('binding_revision')!=2 or d.get('source_commit')!=source_commit:
            raise ValueError(f'{path}: wrong source/binding revision')
        if d.get('device_passes')!=252800 or d.get('digital_passes')!=505600:
            raise ValueError(f'{path}: wrong pass ledger')
    for key in ('final_ser','final_ser_fine'):
        if not isinstance(d[key],(float,int)) or not math.isfinite(d[key]) or not 0<=d[key]<=1:
            raise ValueError(f'{path}: invalid SER')
    if len(d['eval_trace'])!=316:raise ValueError(f'{path}: incomplete trace')
    for i, point in enumerate(d['eval_trace'], 1):
        if (len(point)!=3 or point[:2]!=[i*100,i*800]
                or not isinstance(point[2],(float,int)) or not math.isfinite(point[2])
                or not 0<=point[2]<=1):
            raise ValueError(f'{path}: invalid trace point {i}')
    if d['final_ser']!=statistics.median(p[2] for p in d['eval_trace'][-3:]):
        raise ValueError(f'{path}: final SER differs from final trace median')
    return d


def summarize(rows,key):
    g=torch.Generator().manual_seed(20260727)
    out={'levels':{},'crossover_m_star':None,'offline_fails_target_at':None,
         'offline_fails_while_insitu_passes_at':None}
    for m in LEVELS:
        ins=[rows[('pat-both',m,s)][key] for s in SEEDS]
        off=[rows[('offline-deploy',m,s)][key] for s in SEEDS]
        im,om=statistics.median(ins),statistics.median(off)
        ci,_=paired_ci(ins,off,g)
        ratio=om/max(im,1e-12)
        adv=ratio>=2 and ci[0]>0
        out['levels'][str(m)]={'insitu_median':im,'offline_median':om,
            'ratio_off_over_in':ratio,'ci95_off_minus_in':ci,'advantage':adv,
            'offline_below_target':om<=TARGET,'insitu_below_target':im<=TARGET,
            'insitu_per_seed':ins,'offline_per_seed':off,'seeds':list(SEEDS)}
        if adv and out['crossover_m_star'] is None:out['crossover_m_star']=m
        if om>TARGET:
            if out['offline_fails_target_at'] is None:out['offline_fails_target_at']=m
            if im<=TARGET and out['offline_fails_while_insitu_passes_at'] is None:
                out['offline_fails_while_insitu_passes_at']=m
    return out


def main():
    manifest=json.loads((OUT/'source_manifest.json').read_text())
    head=manifest['source_commit']
    rows={};provenance=[]
    expected={f'pat-both_m{m}_{s}.json' for m in (2,3,4,6) for s in SEEDS}|{'pat-both_m1_11.json'}
    actual={p.name for p in (OUT/'runs').glob('*.json')}
    if actual!=expected:
        raise SystemExit(f'Incomplete/unexpected corrected grid: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}')
    for name in sorted(expected):
        row=json.loads((OUT/'runs'/name).read_text())
        state=OUT/'states'/Path(name).with_suffix('.pt')
        if hashlib.sha256(state.read_bytes()).hexdigest()!=row['state_sha256']:
            raise SystemExit(f'Saved-state checksum mismatch: {state}')
    for method in ('pat-both','offline-deploy'):
        for m in LEVELS:
            for seed in SEEDS:
                fresh=method=='pat-both' and m>1
                folder=OUT/'runs' if fresh else ROOT/'results/s0_10/runs_a'
                path=folder/f'{method}_m{m}_{seed}.json'
                rows[(method,m,seed)]=read_row(path,method,seed,m,fresh,head)
                provenance.append({'path':str(path.relative_to(ROOT)),
                    'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                    'role':'corrected' if fresh else 'unchanged historical control'})
    anchor=read_row(OUT/'runs/pat-both_m1_11.json','pat-both',11,1,True,head)
    old=rows[('pat-both',1,11)]
    anchor_checks={key:anchor[key]==old[key] for key in
                   ('eval_trace','final_ser','final_ser_fine','device_passes','digital_passes')}
    if not all(anchor_checks.values()):
        (OUT/'anchor_discrepancy.json').write_text(json.dumps(anchor_checks,indent=2)+'\n')
        raise SystemExit(f'Anchor discrepancy requires adjudication before combined result: {anchor_checks}')
    fine=summarize(rows,'final_ser_fine');coarse=summarize(rows,'final_ser')
    historical=ROOT/'results/s0_10/analysis.json'
    result=copy.deepcopy(json.loads(historical.read_text()))
    result['s0_10a_mismatch_fine']=fine
    result['s0_13_mismatch_coarse']=coarse
    result['correction']={'status':'complete','source_commit':head,'fresh_units':32,
        'anchor_units':1,'reused_units':48,'anchor_checks':anchor_checks,
        'anchor_path':'results/s0_13/runs/pat-both_m1_11.json',
        'anchor_sha256':hashlib.sha256((OUT/'runs/pat-both_m1_11.json').read_bytes()).hexdigest(),
        'bootstrap_seed':20260727,'historical_summary_sha256':hashlib.sha256(historical.read_bytes()).hexdigest(),
        'unchanged_summary_blocks':'drift, diagnostics, ceilings and damping imported from S0.10',
        'inputs':provenance}
    (OUT/'analysis.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    lines=['# Corrected PAT mismatch sweep — S0.13','',
        'Complete grid: 32 corrected PAT units + one reproducibility anchor; 48 unchanged controls reused.',
        'Base m=1 seed-11 full coarse trace, coarse/fine SER, and pass ledgers match exactly.','',
        '| mismatch class | PAT fine median | offline fine median | ratio off/PAT | paired 95% CI (off−PAT) | registered advantage |',
        '|---|---:|---:|---:|---|---|']
    for m,d in fine['levels'].items():
        lines.append(f'| {5*int(m)}% | {d["insitu_median"]:.8f} | {d["offline_median"]:.8f} | {d["ratio_off_over_in"]:.4f} | {d["ci95_off_minus_in"]} | {d["advantage"]} |')
    lines+=['',f'Fine crossover m*: {fine["crossover_m_star"]}; coarse crossover m*: {coarse["crossover_m_star"]}.',
        f'Offline first target failure: {fine["offline_fails_target_at"]}.',
        'Intervals including zero indicate no resolved difference, not statistical equivalence.',
        'The N8 defect and original withdrawal remain in the audit trail; this record replaces the affected comparisons only.']
    (OUT/'reading.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))


if __name__=='__main__':main()
