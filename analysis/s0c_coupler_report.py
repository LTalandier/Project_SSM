"""Report saved PR-23-D arithmetic; no new sensitivity points or fitting."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]

def main():
    out=ROOT/'results/s0c_coupler';r=json.loads((out/'sensitivity.json').read_text())
    lines=['# Wide-coupler sensitivity — PR-23-D','',f"Pre-run commit `{r['pre_run_commit']}`; local arithmetic, €0 cloud; no retraining.",
    '', 'Sources, derivation and interpretation: `docs/s0c/coupler_feasibility_2026-09-22.md`.',
    '', '| Coupler excess dB | Propagation dB/cm | NMSE | Mean IL dB, incl. package | Receiver noise increase dB | Shape screen |',
    '|---:|---:|---:|---:|---:|---|']
    for x in r['loss_scenarios']:
        lines.append(f"| {x['coupler_loss_db']} | {x['propagation_db_cm']} | {x['nmse']:.6f} | {x['mean_insertion_loss_db_including_3db_package']:.3f} | {x['receiver_noise_enhancement_db']:.3f} | {'pass' if x['passes_shape_only_screen'] else 'fail'} |")
    lines+=['','Receiver-noise increase refers to fixed additive noise after filtering; this is not a BER prediction.',
    'Pass/fail is only the prior .01 noiseless shape-error screen. Scalar gain does not restore SNR.',
    '', '| Phase bits over 2π | NMSE at zero added coupler loss |','|---:|---:|']
    for x in r['phase_quantization_scenarios']:lines.append(f"| {x['bits_per_2pi_control']} | {x['nmse']:.6f} |")
    lines+=['','Loss and quantization are separate sensitivities, not combined pass conditions.','',
    '| Assumed Pπ, mW | Heater mW | Heater + assumed controls, mW | Subtotal pJ/sample at 64 GS/s |',
    '|---:|---:|---:|---:|']
    for x in r['heater_subtotals']:lines.append(f"| {x['Ppi_mw_scenario']} | {x['heater_mw']:.2f} | {x['subtotal_mw']:.2f} | {x['subtotal_pj_per_sample_64GSs']:.3f} |")
    lines+=['','Subtotals omit locking, amplification, monitoring and refresh. Pπ scenarios are not measurements of this design.',
    'No complete source-backed device budget, function-matched digital comparison, or product go.','',
    '![Coupler loss and phase precision sensitivity](sensitivity.png)']
    (out/'reading.md').write_text('\n'.join(lines)+'\n')
    fig,ax=plt.subplots(1,2,figsize=(10,3.7),layout='constrained')
    for prop in [.051,.17,.4]:
        rows=[x for x in r['loss_scenarios'] if x['propagation_db_cm']==prop]
        ax[0].plot([x['coupler_loss_db'] for x in rows],[x['nmse'] for x in rows],'o-',label=f'{prop} dB/cm')
    ax[0].set(xlabel='Symmetric excess loss per coupler (dB)',ylabel='Normalized field MSE',yscale='log',title='Saved controls; receiver scalar refitted')
    ax[0].legend(fontsize=8)
    q=r['phase_quantization_scenarios'];ax[1].plot([x['bits_per_2pi_control'] for x in q],[x['nmse'] for x in q],'o-')
    ax[1].set(xlabel='Bits per 2π phase control',ylabel='Normalized field MSE',yscale='log',title='Separate test: zero added coupler loss',xticks=[6,8,10,12])
    for a in ax:a.axhline(.01,linestyle='--',color='gray')
    fig.savefig(out/'sensitivity.png',dpi=170)
    print('Saved sensitivity report and plot.')

if __name__=='__main__':main()
