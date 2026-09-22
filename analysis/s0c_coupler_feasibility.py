"""PR-23-D frozen-candidate coupler-loss and control sensitivity. No training."""
from pathlib import Path
import hashlib,json,math,subprocess
import numpy as np
ROOT=Path(__file__).resolve().parents[1]


def lossy_section(q,k,loss_db):
    s=10**(-loss_db/20);t=np.sqrt(1-k)
    return s*(t-s*q)/(1-s*t*q)


def evaluate(f,phase,k,loss_db,propagation,delay):
    a=10**(-propagation*2*np.pi*242.2002619*1e-4/20)
    q=a*np.exp(1j*(phase[:,None]-2*np.pi*f[None,:]/100e9))
    rings=lossy_section(q,k[:,None],loss_db).prod(axis=0)
    beta2=-17e-6*(1550e-9)**2/(2*np.pi*299792458)
    channel=np.exp(-.5j*beta2*20000*(2*np.pi*f)**2)
    target=np.exp(-2j*np.pi*f*delay/64e9)
    transfer=rings*10**(-3/20)
    pred=transfer*channel
    c=np.mean(pred.conj()*target)/np.mean(abs(pred)**2)
    return {'nmse':float(np.mean(abs(c*pred-target)**2)),
        'mean_insertion_loss_db_including_3db_package':float(-10*np.log10(np.mean(abs(transfer)**2))),
        'worst_insertion_loss_db_including_3db_package':float(-10*np.log10(np.min(abs(transfer)**2))),
        'receiver_noise_multiplier':float(abs(c)**2),
        'receiver_noise_enhancement_db':float(10*np.log10(abs(c)**2)),
        'passes_shape_only_screen':bool(np.mean(abs(c*pred-target)**2)<=.01)}


def main():
    source=ROOT/'results/s0c_capacity/capacity.json';saved=json.loads(source.read_text())['best_by_training_grid']['broad_diagnostic']
    p=np.array(saved['best_controls']);lo,hi=saved['coupling_bounds'];k=lo+(hi-lo)/(1+np.exp(-p[8:16]))
    phase=p[:8];delay=float(np.clip(p[16],0,32));f=(-.5+(np.arange(2048)+.5)/2048)*64e9
    theta=2*np.arcsin(np.sqrt(k));trim=np.mod(phase-theta/2,2*np.pi)
    phase_units=float(np.sum(theta+trim)/np.pi)
    rows=[{'coupler_loss_db':ell,'propagation_db_cm':prop,**evaluate(f,phase,k,ell,prop,delay)}
          for prop in [.051,.17,.4] for ell in [0,.02,.05,.1,.2,.4,.67,1.]]
    quant=[]
    for bits in [6,8,10,12]:
        step=2*np.pi/(2**bits)
        theta_q=np.round(theta/step)*step;trim_q=np.round(trim/step)*step
        quant.append({'bits_per_2pi_control':bits,**evaluate(f,trim_q+theta_q/2,np.sin(theta_q/2)**2,0,.051,delay)})
    powers=[{'Ppi_mw_scenario':ppi,'heater_mw':phase_units*ppi,'assumed_control_mw':32.,
             'subtotal_mw':phase_units*ppi+32.,'subtotal_pj_per_sample_64GSs':(phase_units*ppi+32.)/64}
            for ppi in [1,15,60,100]]
    digital=[{'assumed_taps':n,'pj_per_tap':e,'digital_pj_per_sample':n*e,
              'max_total_optical_mw_for_3x_at_64GSs':64*n*e/3}
             for n in [16,32,64] for e in [.03,.05,.15]]
    result={'protocol':'PR-23-D','date':'2026-09-22','cloud_spend_eur':0,
        'pre_run_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        'source_sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['analysis/s0c_coupler_feasibility.py','shared/preregistration.md','results/s0c_capacity/capacity.json']},
        'couplings':k.tolist(),'coupler_phase_over_pi':(theta/np.pi).tolist(),'ring_trim_over_pi':(trim/np.pi).tolist(),
        'total_heater_pi_units_zero_cold_phase':phase_units,
        'ideal_splitter_u_interval_for_max_K':[(1-np.sqrt(1-k.max()))/2,(1+np.sqrt(1-k.max()))/2],
        'max_arm_delay_ps_for_0_01_absolute_K_bound':.01/(np.pi*32e9)*1e12,
        'loss_scenarios':rows,'phase_quantization_scenarios':quant,'heater_subtotals':powers,
        'illustrative_digital_budgets_not_function_matched':digital,
        'limitations':['No reoptimization: failures are frozen-candidate sensitivity, not hardware impossibility.',
        'Symmetric frequency-flat coupler loss and matched arms are assumptions; measured complex S parameters are absent.',
        'Receiver scalar cannot undo noise. Multipliers refer to additive noise after optical filtering.',
        'Heater phase allocation assumes zero fabrication offsets and a specific MZI phase convention.',
        'Actuation, propagation, packaging and athermal data are not co-integrated evidence.',
        'No complete locking, amplification, DAC, refresh or task-matched digital energy budget.']}
    out=ROOT/'results/s0c_coupler';out.mkdir(exist_ok=True)
    (out/'sensitivity.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'phase_units':phase_units,'powers':powers,'base_loss_sweep':rows[:8],'quantization':quant},indent=2))

if __name__=='__main__':main()
