"""Recompute P2's descriptive results from archived arrays and gradient traces.

Run python3 -m analysis.p2_audit. No benchmark training; no new incidence estimate.
"""
from pathlib import Path
import hashlib,json,math
import numpy as np
import torch
from analysis.s0_2_1r_classify import parse_driver_log
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'results/s0_2/gate_i'
SEEDS=[2345,3456,4567,5678,6789]


def gradient_probe(gap):
    z=torch.tensor([-float(gap),0.],dtype=torch.float32,requires_grad=True)
    p=torch.softmax(z,dim=0)
    unstable=-torch.log(p[0]+1e-8)
    stable=-torch.log_softmax(z,dim=0)[0]
    a=torch.autograd.grad(unstable,z,retain_graph=True)[0]
    b=torch.autograd.grad(stable,z)[0]
    return {'gap':gap,'p_true':float(p[0].detach()),'epsilon_loss':float(unstable.detach()),
            'epsilon_gradient_max':float(a.abs().max()),'logsoftmax_gradient_max':float(b.abs().max())}


def main():
    files=set()
    def load(path):
        files.add(path);return np.load(path,allow_pickle=False)
    def records(path):
        files.add(path);return [json.loads(x) for x in path.read_text().splitlines()]
    official=[]
    for seed in SEEDS:
        paths=list((BASE/'xcheck_official/outputs/LinOSS_IM/EigenWorms').glob('*seed_'+str(seed)))
        assert len(paths)==1
        path=paths[0];test=float(load(path/'test_metric.npy'))
        val=load(path/'all_val_metric.npy');train=load(path/'all_train_metric.npy')
        schedule=load(path/'steps.npy')
        assert len(val)==len(train) and len(val)>1
        official.append({'seed':seed,'test_accuracy':test,'test_correct_out_of_36':round(test*36),
                         'scheduled_step_count':len(schedule),'evaluation_count':len(val)-1,'last_evaluation_step':(len(val)-1)*1000,
                         'best_val':float(max(val))})
    arr=np.array([r['test_accuracy'] for r in official])*100
    port={}
    for dataset in ['EigenWorms','Heartbeat']:
        summaries=[]
        for seed in SEEDS:
            rr=records(BASE/f'{dataset}_seed{seed}.jsonl')
            summary=[r for r in rr if r.get('record')=='summary'];assert len(summary)==1
            summaries.append(summary[0])
        port[dataset]={'mean_percent':np.mean([r['test_acc'] for r in summaries])*100,'seeds':summaries}
    local=BASE/'xcheck_official_local';screen=[]
    for seed in [7890,8901,9012,11111,22222,33333,44444,55555]:
        paths=list((local/'outputs/LinOSS_IM/EigenWorms').glob('*nsteps_4000_*seed_'+str(seed)));assert len(paths)==1
        val=load(paths[0]/'all_val_metric.npy');train=load(paths[0]/'all_train_metric.npy');assert len(val)>=5 and len(train)>=5
        log=local/f'logs/driver_seed{seed}.log';files.add(log)
        losses=parse_driver_log(str(log))[seed];assert len(losses)>=4
        flags=[bool(val[2]==val[3]==val[4]),bool(train[2]==train[3]==train[4]),len({f'{x:.6g}' for x in losses[1:4]})==1]
        screen.append({'seed':seed,'constancy_flags_val_train_loss':flags,'strict_trap':all(flags),
                       'loss_cycles':losses[:4],'val_evals':val[1:5].tolist(),'train_evals':train[1:5].tolist()})
    annex=[]
    for seed in [7890,8901,9012]:
        rr=records(local/f'ours_annex_screens/EigenWorms_annexscreen_seed{seed}.jsonl')
        steps=[r for r in rr if 'grad_sq_total' in r];assert len(steps)==600
        # Recompute zero-gradient suffix, independently of the stored verdict.
        start=None
        for r in reversed(steps):
            if r['grad_sq_total']!=0:break
            start=r['step']
        stored=[r for r in rr if r.get('record')=='summary'][0]
        assert (start is not None)==(stored['verdict']=='TRAP')
        annex.append({'seed':seed,'zero_gradient_suffix_start':start,'last_observed_step':steps[-1]['step']})
    for name in ['logs/parity_gpu.log','logs/gpu_remote_driver.log','xcheck_official_local/PREDECLARATION.md','xcheck_official_local/config/LinOSS/EigenWorms.json']:
        files.add(BASE/name)
    upstream=ROOT/'docs/p2/upstream'
    files.update(upstream.glob('*'))
    result={'date':'2026-09-20','official_commit':'05a835355439ee5500b2c8f891132c53adf020c0',
        'official_five':official,'mean_percent':float(arr.mean()),'population_sd_pp_ddof0':float(arr.std(ddof=0)),
        'sample_sd_pp_ddof1':float(arr.std(ddof=1)),
        'published_sd_convention':'Upstream postprocess_results.py uses numpy.std default ddof=0.',
        'port':port,'official_local_screen':screen,'official_local_strict_traps':sum(r['strict_trap'] for r in screen),
        'port_local_annex':annex,'gradient_probe_cpu_float32':[gradient_probe(g) for g in [0,20,80,104,120,160]],
        'probe_torch_version':torch.__version__,'cloud_spend_eur':0,
        'limitations':['Official reruns have no per-step gradient instrumentation; descriptive accuracy gaps do not identify their cause.',
        'Local official screen is 4000 steps, port annex is 600; do not pool their incidence or infer equality from a nonsignificant test.',
        'GPU driver and JAX CUDA runtime version were not recovered; Torch CUDA version is not JAX runtime evidence.',
        'No paired full benchmark rerun with stable log-softmax loss exists in this audit; the numerical probe is not that experiment.'],
        'evidence_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}}
    out=ROOT/'results/p2_audit';out.mkdir(exist_ok=True)
    (out/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['mean_percent','population_sd_pp_ddof0','sample_sd_pp_ddof1','official_local_strict_traps','port_local_annex','gradient_probe_cpu_float32']},indent=2))

if __name__=='__main__':main()
