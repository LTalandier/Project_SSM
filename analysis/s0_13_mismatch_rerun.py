#!/usr/bin/env python3
"""Correct PR-5 §E binding defect; frozen PR-17 evaluation, separate outputs.

Run one registered unit: python3 analysis/s0_13_mismatch_rerun.py SEED SCALE
Metadata is taken from the pre-run source_manifest.json shipped with the source.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import statistics
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import torch
from photonic_ssm.estimators.harness import train, final_fine_ser, make_substrate, TapHead

SEEDS = (11, 23, 47, 61, 83, 101, 127, 151)
SCALES = (2, 3, 4, 6)
UPDATES = 31600
OUT = ROOT / 'results/s0_13'


def atomic_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    with tmp.open('w') as fh:
        json.dump(obj, fh, indent=2, allow_nan=False)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def verified_manifest():
    manifest = json.loads((ROOT / 'source_manifest.json').read_text())
    for name, expected in manifest['sha256'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != expected:
            raise RuntimeError(f'Source differs from registered bundle: {name}')
    return manifest


def run(seed, scale):
    if seed not in SEEDS or not (scale in SCALES or (scale == 1 and seed == 11)):
        raise ValueError('Unit outside frozen correction grid')
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    manifest = verified_manifest()
    config = dict(method='pat-both', cell='C-2', seed=seed, mismatch_scale=scale,
                  n_updates=UPDATES, eval_every=100, source_commit=manifest['source_commit'],
                  binding_revision=2, evaluation='PR-17 eval-F at trained y_scale')
    tag = f'pat-both_m{scale}_{seed}'
    path = OUT/'runs'/f'{tag}.json'
    state_path = OUT/'states'/f'{tag}.pt'
    if path.exists():
        old = json.loads(path.read_text())
        if old['config'] != config:
            raise RuntimeError('Refusing incompatible completed result')
        print(f'already complete {tag}', flush=True)
        return
    started = datetime.now(timezone.utc).isoformat()
    t0 = time.monotonic()
    print(f'start {tag} {started}', flush=True)
    if state_path.exists():
        saved = torch.load(state_path, weights_only=False)
        if saved['config'] != config or saved['torch_version'] != torch.__version__:
            raise RuntimeError('Incompatible saved state')
        led = saved['ledger']
        sub = make_substrate('C-2', seed)
        head = TapHead()
        sub.load_state_dict(saved['sub'])
        head.load_state_dict(saved['head'])
        training_wall = saved['training_wall_s']
    else:
        led, sub, head = train('pat-both','C-2',run_seed=seed,n_updates=UPDATES,
                              eval_every=100,mismatch_scale=scale,return_state=True)
        training_wall = time.monotonic()-t0
        state_path.parent.mkdir(parents=True,exist_ok=True)
        tmp = state_path.with_suffix('.tmp')
        torch.save(dict(config=config, ledger=dict(led), sub=sub.state_dict(),
                        head=head.state_dict(), training_wall_s=training_wall,
                        torch_version=torch.__version__),tmp)
        os.replace(tmp,state_path)
    fine_t0 = time.monotonic()
    fine = final_fine_ser(sub,head,led['y_scale'])
    row = dict(config=config, **{k:v for k,v in config.items() if k != 'evaluation'},
               started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),
               torch_version=torch.__version__,python_version=platform.python_version(),
               machine=platform.machine(),threads=torch.get_num_threads(),
               final_ser=statistics.median([x[2] for x in led['eval_trace'][-3:]]),
               final_ser_fine=fine,eval_trace=led['eval_trace'],
               device_passes=led['device_passes'],digital_passes=led['digital_passes'],
               y_scale=led['y_scale'],training_wall_s=training_wall,
               fine_eval_wall_s=time.monotonic()-fine_t0,
               wall_s=training_wall+time.monotonic()-fine_t0,
               state_sha256=hashlib.sha256(state_path.read_bytes()).hexdigest())
    atomic_json(path,row)
    print(f'complete {tag}: fine={fine:.9g}, seconds={row["wall_s"]:.1f}',flush=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('seed',type=int)
    parser.add_argument('scale',type=int)
    args=parser.parse_args()
    run(args.seed,args.scale)
