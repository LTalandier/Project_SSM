"""Summarize the frozen PR-23-C outputs; never trains or selects by dense error."""
from pathlib import Path
import json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]

def main():
    out=ROOT/'results/s0c_capacity';r=json.loads((out/'capacity.json').read_text())
    lines=['# PR-23-C capacity diagnostic — 2026-09-20','',
        f"Pre-run commit: `{r['pre_run_commit']}`; runtime {r['runtime_seconds']:.2f} s; cloud spend €0.",
        f"Completed {sum(x['complete'] for x in r['outcomes'])}/{len(r['outcomes'])} fits.",'',
        'All three nearby synthetic starts recover the known response below the 1e-6 target.',
        'All three distant starts get stuck (dense NMSE 0.359–0.552) despite exact gradients.',
        'The model and local optimizer can fit a realizable target; global optimization remains unresolved.','',
        '| Coupling range | Best training NMSE | Dense NMSE, fixed receiver scalar | Seed | Initial / fitted delay, samples |',
        '|---|---:|---:|---:|---:|']
    for name,b in r['best_by_training_grid'].items():
        lines.append(f"| {name} {b['coupling_bounds']} | {b['best_train_nmse']:.8f} | {b['dense_nmse_fixed_scalar']:.8f} | {b['seed']} | {b['initial_delay']} / {min(32,max(0,b['best_controls'][16])):.4f} |")
    lines+=['',r['decision'],'',
        'The broad candidate has K = '+', '.join(f'{x:.4f}' for x in couplings(r['best_by_training_grid']['broad_diagnostic']))+'.',
        'Only one of the 15 broad-range starts passes the .01 screening target; optimization is fragile. All eight couplings of that candidate exceed the original .20 maximum. This is a constructive noiseless approximation in an expanded mathematical design space, not a realization within PR-22.',
        '', 'The original-range best has 46.13% residual power; the broad best has 0.2387% (26.22 dB residual suppression).',
        'These are normalized complex-field MSEs, not BER or a demonstrated communication link. No noise, finite actuator resolution, coupler excess loss, drift, nonlinearities or thermal budget is modeled here.',
        '', 'Selection was by training loss, with a separate 2048-point midpoint grid and no receiver refit. All candidates and controls are archived; no extra starts or tuning followed the registered grid.',
        'Near-start success is not global identifiability: phases wrap, rings permute, and distant starts failed. The poor restricted fit is not a lower bound on the best possible restricted design.',
        'The broad arm changes initialization as well as coupling bounds (zero logits imply K=.48 instead of .125); this is not a controlled causal estimate of the effect of widening bounds.',
        '', 'Next gate: before any adaptive-drift run, justify the broad coupling range with a feasible tunable-coupler model including excess loss/actuation, and freeze a matched-observation adaptive baseline. No paid fleet or hardware step follows from this result.',
        '', 'Reproduce: `python3 -m analysis.s0c_capacity` (optimization) and `python3 -m analysis.s0c_capacity_report` (report only).',
        '![All registered CD starts and best-fit couplings](capacity.png)']
    (out/'reading.md').write_text('\n'.join(lines)+'\n')
    fig,ax=plt.subplots(1,2,figsize=(10,3.7),layout='constrained')
    for offset,(name,color) in enumerate([('registered','#b45b31'),('broad_diagnostic','#236d9a')]):
        rows=[x for x in r['outcomes'] if x.get('range')==name]
        ax[0].scatter([x['initial_delay']+(.22 if offset else -.22)+(x['seed']-22)/55 for x in rows],
            [x['dense_nmse_fixed_scalar'] for x in rows],label=name,color=color,s=30,alpha=.8)
        ax[1].plot(np.arange(1,9),couplings(r['best_by_training_grid'][name]),'o-',label=name,color=color)
    ax[0].axhline(.01,color='gray',linestyle='--',label='screening target')
    ax[0].set(yscale='log',xlabel='Initial receiver delay (samples)',ylabel='Dense-grid normalized MSE',title='All 30 CD fits')
    ax[0].legend(fontsize=8)
    ax[1].axhspan(.05,.2,color='gray',alpha=.15,label='original allowed range')
    ax[1].set(xlabel='Ring index (ordering is arbitrary)',ylabel='Power coupling K',ylim=(0,1),title='Candidates selected by training loss')
    ax[1].legend(fontsize=8)
    fig.savefig(out/'capacity.png',dpi=170)
    print('\n'.join(lines[:15]))


def couplings(row):
    lo,hi=row['coupling_bounds'];logits=np.array(row['best_controls'][8:16])
    return lo+(hi-lo)/(1+np.exp(-logits))

if __name__=='__main__':main()
