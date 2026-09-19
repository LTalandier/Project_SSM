#!/usr/bin/env python3
"""PR-23-P local exploratory preflight; run with python -m analysis.s0c_1_pilot."""
import hashlib
import json
import math
from pathlib import Path
import subprocess
import time
import numpy as np
import torch
from photonic_ssm.delay_ring import ring_cascade, decode_controls, fit_response, chromatic_dispersion

ROOT = Path(__file__).resolve().parents[1]


def fir_match(channel, threshold):
    # Unit-modulus CD gives an orthonormal Fourier design. Truncating its
    # inverse-channel impulse is the exact LS projection for each tap window.
    impulse = np.fft.ifft(1/channel)
    energy = abs(impulse)**2
    errors = []
    for taps in range(1,129):
        retained = max(sum(energy[(start+np.arange(taps)) % len(energy)]) for start in range(len(energy)))
        errors.append(max(0., 1-float(retained)))
    matches = [i+1 for i,e in enumerate(errors) if e <= threshold+1e-12]
    return {'first_matching_taps': min(matches) if matches else None, 'nmse_by_taps': errors}


def objective_check(p,f,h,target,x):
    p = p.detach().requires_grad_()
    residual = fit_response(p,f,h,target)
    response_loss = residual.abs().square().mean()
    task_loss = torch.fft.ifft(residual*x,norm='ortho').abs().square().mean()
    a = torch.autograd.grad(response_loss,p,retain_graph=True)[0]
    b = torch.autograd.grad(task_loss,p)[0]
    return {'loss_abs_difference': abs(float(response_loss.detach()-task_loss.detach())),
            'gradient_max_abs_difference': float((a-b).abs().max())}


def main():
    started = time.monotonic()
    torch.set_num_threads(1)
    torch.set_default_dtype(torch.float64)
    f = torch.fft.fftfreq(512,d=1/64e9)
    h = chromatic_dispersion(f)
    outcomes = []
    for seed in [11,22,33]:
        gen = torch.Generator().manual_seed(seed)
        phases = torch.linspace(-math.pi*.64,math.pi*.64,8)+.05*torch.randn(8,generator=gen)
        initial = torch.cat([phases,torch.zeros(8)])
        targets = [torch.exp(-2j*math.pi*f*d/64e9) for d in range(33)]
        delay = min(range(33), key=lambda d: float(fit_response(initial,f,h,targets[d]).abs().square().mean()))
        target = targets[delay]
        x = torch.exp(2j*math.pi*torch.rand(512,generator=gen))
        init_loss = float(fit_response(initial,f,h,target).abs().square().mean())
        init_check = objective_check(initial,f,h,target,x)
        for method in ['BPTT_oracle','SPSA']:
            p = initial.clone().requires_grad_(method=='BPTT_oracle')
            opt = torch.optim.Adam([p],lr=.03) if method=='BPTT_oracle' else None
            trace = []
            for i in range(300):
                if opt is not None:
                    opt.zero_grad()
                    loss = fit_response(p,f,h,target).abs().square().mean()
                    loss.backward(); opt.step()
                else:
                    delta = torch.randint(0,2,(16,),generator=gen)*2.-1
                    c = .02/(1+i/50)**.101
                    a = .1/(1+i/50)**.602
                    plus = fit_response(p+c*delta,f,h,target).abs().square().mean()
                    minus = fit_response(p-c*delta,f,h,target).abs().square().mean()
                    p = p-a*(plus-minus)/(2*c)*delta
                if i % 10 == 0 or i == 299:
                    trace.append({'update':i+1,'nmse':float(fit_response(p,f,h,target).abs().square().mean().detach())})
            final = trace[-1]['nmse']
            final_check = objective_check(p,f,h,target,x)
            fir = fir_match(h.numpy(),final)
            outcomes.append({'seed':seed,'method':method,'receiver_delay_samples':delay,
                'initial_nmse':init_loss,'final_nmse':final,'controls':p.detach().tolist(),
                'initial_equivalence_check':init_check,'final_equivalence_check':final_check,
                'optimization_objective_probes':600 if method=='SPSA' else 0,
                'optimization_parameter_writes':600 if method=='SPSA' else 0,
                'accounting_note':'Simulated queries only; initialization, diagnostics, and held-out evaluation are not a hardware budget.',
                'trace':trace,'fir':fir})
    checks = [r[k][v] for r in outcomes for k in ['initial_equivalence_check','final_equivalence_check'] for v in ['loss_abs_difference','gradient_max_abs_difference']]
    result = {'protocol':'PR-23-P','commit_before_execution':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'source_hashes':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['analysis/s0c_1_pilot.py','photonic_ssm/delay_ring.py','shared/preregistration.md']},
        'runtime_seconds':time.monotonic()-started,'cloud_spend_eur':0,'torch_version':torch.__version__,
        'scalar_delay_only_best_nmse':fir_match(h.numpy(),0)['nmse_by_taps'][0],
        'equivalence_tolerance':1e-10,'equivalence_pass':max(checks)<=1e-10,
        'decision':'STOP paid expansion of equivalent-objective comparison; drift protocol not run.', 'outcomes':outcomes}
    out = ROOT/'results/s0c_1_pilot';out.mkdir(exist_ok=True)
    (out/'pilot.json').write_text(json.dumps(result,indent=2)+'\n')
    lines = ['# PR-23-P exploratory local pilot','',f"Cost: €0 cloud; runtime {result['runtime_seconds']:.2f} s.",
        f"Pre-run commit: `{result['commit_before_execution']}`.",'',
        '| Seed | Method | Initial NMSE | Final NMSE | Matching FIR taps |','|---|---|---:|---:|---:|']
    for r in outcomes:
        lines.append(f"| {r['seed']} | {r['method']} | {r['initial_nmse']:.6f} | {r['final_nmse']:.6f} | {r['fir']['first_matching_taps']} |")
    lines += ['',f"Scalar/delay-only best NMSE: {result['scalar_delay_only_best_nmse']:.6f}.",
        f"Largest task/response loss or gradient discrepancy: {max(checks):.3g}.",
        '',result['decision'],'',
        'No physical training, PAT, drift test, SER comparison, or energy advantage is established.',
        'FIR lengths are noiseless, cyclic, and channel-specific; they do not validate the PR-22 eta assumption.',
        'A fitted receiver scalar removes attenuation for this noiseless check; it cannot restore SNR in hardware.',
        'BPTT has exact plant gradients and is an oracle, not a feasible calibration algorithm.',
        'The equivalence is between objectives with identical information and estimators, not every possible learning/control method.']
    (out/'reading.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))


if __name__=='__main__':
    main()
