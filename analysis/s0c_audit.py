#!/usr/bin/env python3
"""Recompute PR-22 sensitivities without changing the frozen implementation."""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def loss_budget(loss_db, *, input_dbm=-10., target_dbm=0., nf_db=5.,
                efficiency=.1, idle_mw=None, receiver_snr_db=30., bandwidth_hz=64e9):
    """Illustrative post-filter amplifier; assumptions are NOT device specifications.

    Single spatial mode, two-polarization ASE in the stated optical bandwidth.
    F = 2*n_sp*(1-1/G)+1/G, hence P_ASE = (F*G-1)*h*nu*B.
    Gain >= 1. Pump/electrical lower bound excludes unknown idle and out-of-band ASE.
    """
    pin = 10**(input_dbm/10)*1e-3 * 10**(-loss_db/10)
    pout = 10**(target_dbm/10)*1e-3
    gain = max(1.,pout/pin)
    actual_out = pin*gain
    ase = (10**(nf_db/10)*gain-1)*6.62607015e-34*(299792458/1550e-9)*bandwidth_hz if gain>1 else 0.
    floor = ((actual_out-pin)+ase)/efficiency*1000
    total = None if idle_mw is None else floor+idle_mw
    return {'gain_db':10*math.log10(gain),'ase_mw':ase*1000,
        'output_snr_db':10*math.log10(actual_out/(ase+pout/10**(receiver_snr_db/10))),
        'electrical_lower_bound_mw':floor,'electrical_total_mw':total,
        'within_illustrative_30db_gain_16dbm_output_limits':10*math.log10(gain)<=30 and 10*math.log10((actual_out+ase)*1000)<=16,
        'product_verdict':'UNDETERMINED: idle/efficiency/gain/NF/saturation and link target unverified'}


def main():
    original=ROOT/'results/s0c_0/envelope.json'
    data=json.loads(original.read_text())
    cells=[r for r in data['cells']['CONS'] if r['cls']=='Cpcm' and r['drift']=='ATHERMAL' and r['N']==32]
    crossed=[dict(K=r['K'],rate_GS_s=r['fs'],old_ratio=r['ratio'],digital_pj_tap=e,
                  fixed_cost_ratio=64*e/r['E_ph']) for r in cells for e in [.03,.05,.15,.25]]
    mapping=[]
    for loss in [.051,.4]:
        a=10**(-loss*2*math.pi*242.2002619*1e-4/20)
        for k in [.05,.1,.2]:
            t=math.sqrt(1-k);p=t*a
            il=-20*math.log10(abs((t-a)/(1-t*a)))
            mapping.append({'loss_db_cm':loss,'K':k,'roundtrip_amplitude':a,
                'memory_efold_roundtrips':-1/math.log(p),
                'cavity_fwhm_GHz':2*100/math.pi*math.asin((1-p)/(2*math.sqrt(p))),
                'resonance_loss_db_per_ring':il,'32_aligned_rings_plus_package_db':32*il+3,
                'illustrative_amplifier':loss_budget(32*il+3)})
    result={'original_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),
        'crossed_comparator_costs':crossed,'mapping':mapping,
        'decision':'No validated product window; frozen PR-22 arithmetic retained as historical scenario.',
        'limitations':['0.4 dB/cm is a different athermal platform, transplanted here only as loss sensitivity.',
        'Adding N on-resonance losses assumes coincident resonances; actual trained spectrum must be evaluated.',
        'Amplifier inputs, targets, NF, efficiency, limits and receiver SNR are explicit sensitivity assumptions, not sourced product specifications.',
        'No idle/control/thermal/actuator number or taps-per-ring equivalence has been validated for a co-integrated device.']}
    out=ROOT/'results/s0c_audit';out.mkdir(exist_ok=True)
    (out/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    lines=['# PR-22 arithmetic and physical-budget audit','',result['decision'],'',
    'At 64 GS/s the stored favorable CONS cell is 2.0411×, not 1.25×.',
    'At 100 GS/s, holding photonic costs fixed and using 0.05 pJ/tap gives 1.0631×, not 3.1892×.','',
    '| Loss dB/cm | K | Cavity FWHM GHz | Memory round trips | Resonance loss dB/ring | Assumed gain dB | Assumed output SNR dB |',
    '|---:|---:|---:|---:|---:|---:|---:|']
    for r in mapping:
        b=r['illustrative_amplifier']
        lines.append(f"| {r['loss_db_cm']} | {r['K']} | {r['cavity_fwhm_GHz']:.3f} | {r['memory_efold_roundtrips']:.2f} | {r['resonance_loss_db_per_ring']:.3f} | {b['gain_db']:.2f} | {b['output_snr_db']:.2f} |")
    lines+=['','Amplifier scenario: input −10 dBm before lattice, target 0 dBm after amplifier; NF 5 dB, 64 GHz noise bandwidth, receiver SNR 30 dB, efficiency 10%, unknown idle power. Numbers outside assumed gain/output limits are infeasible in that scenario, not predictions of real devices.','']+result['limitations']
    (out/'reading.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))


if __name__=='__main__': main()
