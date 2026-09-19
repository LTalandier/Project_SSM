"""PR-23-C: exact-model recovery and bounded multistart CD approximation."""
import hashlib
import json
import math
from pathlib import Path
import subprocess
import time
import torch
from photonic_ssm.delay_ring import ring_cascade, chromatic_dispersion
ROOT=Path(__file__).resolve().parents[1]


def response(p,f,bounds):
    return ring_cascade(f,p[:8],bounds[0]+(bounds[1]-bounds[0])*torch.sigmoid(p[8:16]))


def terms(p,f,kind,truth,bounds):
    if kind=='synthetic':
        return response(p,f,bounds),response(truth,f,bounds)
    return response(p,f,bounds)*chromatic_dispersion(f),torch.exp(-2j*math.pi*f*p[16].clamp(0,32)/64e9)


def objective(p,f,kind,truth,bounds):
    pred,target=terms(p,f,kind,truth,bounds)
    c=(pred.conj()*target).mean()/pred.abs().square().mean()
    return (c*pred-target).abs().square().mean()/target.abs().square().mean(),c


def fit(initial,f,fine,kind,truth,bounds,deadline):
    p=initial.clone().requires_grad_()
    initial_loss=float(objective(p,f,kind,truth,bounds)[0].detach())
    best_loss=initial_loss; best=p.detach().clone(); evaluations=0; iterations=0
    def assess():
        nonlocal best_loss,best,evaluations
        if time.monotonic()>deadline: raise TimeoutError
        loss,_=objective(p,f,kind,truth,bounds)
        evaluations+=1
        if not torch.isfinite(loss): raise FloatingPointError
        if float(loss.detach())<best_loss:
            best_loss=float(loss.detach());best=p.detach().clone()
        return loss
    complete=True
    try:
        optimizer=torch.optim.Adam([p],lr=.03)
        for i in range(1000):
            optimizer.zero_grad();loss=assess();loss.backward();optimizer.step()
            if kind=='cd':
                with torch.no_grad():p[16].clamp_(0,32)
            iterations+=1
        optimizer=torch.optim.LBFGS([p],lr=1,max_iter=100,max_eval=125,
                    line_search_fn='strong_wolfe',tolerance_grad=1e-10,tolerance_change=1e-12)
        def closure():
            optimizer.zero_grad();loss=assess();loss.backward();return loss
        optimizer.step(closure);assess()
    except (TimeoutError,FloatingPointError) as exc:
        complete=False
    final_loss=float(objective(p,f,kind,truth,bounds)[0].detach())
    train_loss,c=objective(best,f,kind,truth,bounds)
    pred,target=terms(best,fine,kind,truth,bounds)
    dense=float(((c*pred-target).abs().square().mean()/target.abs().square().mean()).detach())
    return {'complete':complete,'initial_nmse':initial_loss,'final_nmse':final_loss,
            'best_train_nmse':float(train_loss),'dense_nmse_fixed_scalar':dense,
            'adam_steps':iterations,'objective_evaluations':evaluations,
            'best_controls':best.tolist(),'receiver_scalar':[float(c.real),float(c.imag)]}


def main():
    start=time.monotonic();deadline=start+300
    torch.set_num_threads(1);torch.set_default_dtype(torch.float64)
    f=torch.fft.fftfreq(512,d=1/64e9)
    fine=(-.5+(torch.arange(2048)+.5)/2048)*64e9
    rows=[]
    for seed in [11,22,33]:
        g=torch.Generator().manual_seed(seed)
        phase=torch.linspace(-math.pi*.64,math.pi*.64,8)
        truth=torch.cat([phase+.2*torch.randn(8,generator=g),.6*torch.randn(8,generator=g)])
        initials={'near':truth+.05*torch.randn(16,generator=g),
                  'far':torch.cat([(torch.rand(8,generator=g)*2-1)*math.pi,torch.zeros(8)])}
        identity=float(objective(truth,f,'synthetic',truth,(.05,.2))[0])
        for label,initial in initials.items():
            row={'kind':'synthetic','seed':seed,'initialization':label,'truth_controls':truth.tolist(),'identity_nmse':identity,
                 **fit(initial,f,fine,'synthetic',truth,(.05,.2),deadline)}
            rows.append(row);print(json.dumps({k:row[k] for k in ['kind','seed','initialization','complete','dense_nmse_fixed_scalar']}),flush=True)
    for name,bounds in [('registered',(.05,.2)),('broad_diagnostic',(.01,.95))]:
        for seed in [11,22,33]:
            g=torch.Generator().manual_seed(seed)
            base=torch.cat([torch.linspace(-math.pi*.64,math.pi*.64,8)+.05*torch.randn(8,generator=g),torch.zeros(8)])
            for delay in [0.,8.,16.,24.,32.]:
                row={'kind':'cd','range':name,'coupling_bounds':bounds,'seed':seed,'initial_delay':delay,
                     **fit(torch.cat([base,torch.tensor([delay])]),f,fine,'cd',None,bounds,deadline)}
                rows.append(row);print(json.dumps({k:row[k] for k in ['kind','range','seed','initial_delay','complete','dense_nmse_fixed_scalar']}),flush=True)
    recovery=all(r['complete'] and r['dense_nmse_fixed_scalar']<=1e-6 for r in rows if r['kind']=='synthetic' and r['initialization']=='near')
    best={}
    for name in ['registered','broad_diagnostic']:
        candidates=[r for r in rows if r['kind']=='cd' and r['range']==name and r['complete']]
        best[name]=min(candidates,key=lambda r:r['best_train_nmse']) if candidates else None
    if not recovery:decision='STOP: synthetic near recovery failed; capacity interpretation blocked.'
    elif best['registered'] and best['registered']['dense_nmse_fixed_scalar']<=.01:decision='Original range meets screening target; design drift protocol separately, no fleet launched.'
    elif best['broad_diagnostic'] and best['broad_diagnostic']['dense_nmse_fixed_scalar']<=.01:decision='Only broad diagnostic passes; no go for original registered range.'
    else:decision='STOP expansion on this workload; neither search meets screening target. Not an impossibility proof.'
    result={'protocol':'PR-23-C','pre_run_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        'source_hashes':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['analysis/s0c_capacity.py','photonic_ssm/delay_ring.py','shared/preregistration.md']},
        'runtime_seconds':time.monotonic()-start,'cloud_spend_eur':0,'torch_version':torch.__version__,
        'synthetic_near_recovery_pass':recovery,'best_by_training_grid':best,'decision':decision,'outcomes':rows}
    out=ROOT/'results/s0c_capacity';out.mkdir(exist_ok=True)
    (out/'capacity.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(decision,flush=True)

if __name__=='__main__':main()
