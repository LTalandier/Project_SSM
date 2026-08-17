# NEW (PR-19 §19.4-P2 refit row, 2026-08-17) — reconstruct one PAT solution
# from its serialized state, ablate readouts at k = N_drop*+1 (target from
# §19.6b: 5.00e-3), retrain the head only (2,000 updates, §18.6b budget),
# report recovery. Also measures the STEP-4 at-solution gradient gate
# (S0.4-0 probe verbatim) on the reconstructed device.
"""usage: s0_12_refit_one.py SEED"""

from __future__ import annotations

import json
import os
import sys
import time

import torch

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from photonic_ssm.estimators.harness import (   # noqa: E402
    make_substrate, TapHead, eval_ser_td, fresh_batch_td, encode_drive,
    ase_gen)
import s0_4_0_calibration as cal                # noqa: E402

SER_TARGET = 0.005      # §19.6b ceiling addendum (a4e6a70)
ROBUST_SEEDS = (7, 19, 41, 101, 271)


def reconstruct(seed):
    st = json.load(open(f"results/s0_12/states/pat_{seed}.json"))
    sub = make_substrate("C-2", seed)
    with torch.no_grad():
        sub.delta.copy_(torch.tensor(st["delta"], dtype=torch.float64))
        sub.kappa_ext.copy_(torch.tensor(st["kappa_ext"], dtype=torch.float64))
        sub.mu_chain.copy_(torch.tensor(st["mu_chain"], dtype=torch.float64))
        c = torch.complex(torch.tensor(st["c_readout_re"], dtype=torch.float64),
                          torch.tensor(st["c_readout_im"], dtype=torch.float64))
        sub.c_readout.copy_(c)
    head = TapHead()
    head.load_state_dict({k: torch.tensor(v, dtype=torch.float64)
                          for k, v in st["head"].items()})
    return sub, head, st["y_scale"]


def main():
    seed = int(sys.argv[1])
    t0 = time.time()
    run = json.load(open(f"results/s0_12/runs/pat_{seed}.json"))
    curve = run["ablation"]["curve"]
    order = [j - 1 for j in run["ablation"]["order_1based"]]
    passing = [k for k, s in curve if s <= SER_TARGET]
    n_drop = max(passing)
    sub, head, y_scale = reconstruct(seed)

    # sanity: reconstructed device reproduces the stored k=0 eval
    ser0 = eval_ser_td(sub, head, y_scale)
    k_fail = n_drop + 1
    row = {"seed": seed, "n_drop_star": n_drop, "n_eff": 32 - n_drop,
           "recon_ser0": float(ser0),
           "recon_matches": bool(abs(ser0 - curve[0][1]) < 1e-12)}

    if k_fail < 32:
        c_orig = sub.c_readout.detach().clone()
        with torch.no_grad():
            c = c_orig.clone()
            c[order[:k_fail]] = 0
            sub.c_readout.copy_(c)
            u0, _, _ = fresh_batch_td(seed, 0)
            y0 = sub.forward_intensity(encode_drive(u0).unsqueeze(-1),
                                       generator=ase_gen(seed, 0, 22))
            ys_abl = float(y0.mean()) + 1e-30
        head_r = TapHead()
        head_r.load_state_dict(head.state_dict())
        opt = torch.optim.Adam(head_r.parameters(), lr=3e-2)
        for it in range(1, 2001):
            u_raw, target, mask = fresh_batch_td(seed, it)
            with torch.no_grad():
                y = sub.forward_intensity(encode_drive(u_raw).unsqueeze(-1),
                                          generator=ase_gen(seed, it, 21))
            pred = head_r(y / ys_abl)
            loss = torch.nn.functional.mse_loss(pred[:, mask], target[:, mask])
            opt.zero_grad()
            loss.backward()
            opt.step()
        ser_refit = eval_ser_td(sub, head_r, ys_abl)
        with torch.no_grad():
            sub.c_readout.copy_(c_orig)
        row["refit_at_k"] = k_fail
        row["refit_ser"] = float(ser_refit)
        row["refit_recovers"] = bool(ser_refit <= SER_TARGET)

    # STEP-4 at-solution gradient gate (S0.4-0 probe verbatim, noiseless)
    sub.ase_variance_scale = 0.0
    pm = None
    for s in ROBUST_SEEDS:
        g = cal.per_ring_gradient(sub, loss_kind="mse_zero", seed=s)
        r = g / g.max().clamp_min(1e-300)
        pm = r if pm is None else torch.minimum(pm, r)
    row["gate_count_ge_1e-3"] = int((pm >= 1e-3).sum())
    row["gate_worst_ratio"] = float(pm.min())
    row["wall_s"] = round(time.time() - t0, 1)
    os.makedirs("results/s0_12/refit", exist_ok=True)
    with open(f"results/s0_12/refit/pat_{seed}.json", "w") as fh:
        json.dump(row, fh)
    print(f"refit {seed}: n_eff {row['n_eff']} recon_match "
          f"{row['recon_matches']} refit_rec {row.get('refit_recovers')} "
          f"gate {row['gate_count_ge_1e-3']}/32 [{row['wall_s']:.0f}s]")


if __name__ == "__main__":
    main()
