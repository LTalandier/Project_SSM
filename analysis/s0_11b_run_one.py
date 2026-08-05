# NEW (PR-18 §18.6, 2026-08-05, registered pre-run at ec2d4e3) — one
# (set, seed) unit of the round-5 follow-ups: (a) taps-only training control,
# (b) N_eff readout ablation on the winning routes' solutions, (c) state
# serialization. Writes results/s0_11/runs_b/<set>_<seed>.json and
# results/s0_11/states/<set>_<seed>.json.
"""usage: s0_11b_run_one.py SET SEED   (SET ∈ {patC2, spsaC2, tapsonly})"""

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
    train, eval_ser, final_fine_ser, fresh_batch, encode_drive, ase_gen,
    TapHead)
import s0_4_0_calibration as cal                # noqa: E402

SER_TARGET = 0.005651        # PR-3 rule of record (coarse)
COARSE_BATCHES = 2           # protocol of record (3,840 scored symbols)
REFIT_UPDATES = 2000         # §18.6b registered head-refit budget
REFIT_LR = 3e-2              # harness lr_head


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


SPECS = {
    "patC2": dict(stored="results/s0_5/runs/pat-both_C-2_{seed}.json",
                  kw=dict(method="pat-both", cell_label="C-2",
                          n_updates=31600, eval_every=100)),
    "spsaC2": dict(stored="results/s0_5/runs/spsa_C-2_{seed}.json",
                   kw=dict(method="spsa", cell_label="C-2",
                           n_updates=15800, eval_every=100)),
    "tapsonly": dict(stored=None,
                     kw=dict(method="pat-both", cell_label="C-2",
                             n_updates=31600, eval_every=100,
                             taps_only=True)),
}


def fingerprint(led, stored):
    got_trace = [list(t) for t in led["eval_trace"]]
    got_final = median([s for _, _, s in led["eval_trace"][-3:]])
    ok = (got_trace == stored["eval_trace"]
          and got_final == stored["final_ser"])
    return ("bit" if ok else "protocol"), got_final


def serialize_state(sub, head, y_scale, path):
    st = {
        "delta": sub.delta.detach().tolist(),
        "kappa_ext": sub.kappa_ext.detach().tolist(),
        "mu_chain": sub.mu_chain.detach().tolist(),
        "c_readout_re": sub.c_readout.detach().real.tolist(),
        "c_readout_im": sub.c_readout.detach().imag.tolist(),
        "head": {k: v.tolist() for k, v in head.state_dict().items()},
        "y_scale": y_scale,
        "kappa_i": float(sub.kappa_i),
    }
    with open(path, "w") as fh:
        json.dump(st, fh)


def main():
    set_name, seed = sys.argv[1], int(sys.argv[2])
    smoke = len(sys.argv) > 3 and sys.argv[3] == "smoke"
    spec = SPECS[set_name]
    kw = dict(spec["kw"])
    if smoke:
        kw["n_updates"] = 200
    t0 = time.time()
    led, sub, head = train(run_seed=seed, return_state=True, **kw)
    y_scale = led["y_scale"]

    row = {"set": set_name, "seed": seed, "registered": "PR-18 §18.6 (ec2d4e3)",
           "smoke": smoke}

    if spec["stored"] and not smoke:
        stored = json.load(open(spec["stored"].format(seed=seed)))
        fp, got_final = fingerprint(led, stored)
        row["fingerprint"] = fp
        row["final_ser_stored"] = stored["final_ser"]
        row["final_ser_reproduced"] = got_final
    else:
        row["fingerprint"] = "new-arm"
        row["final_ser_coarse"] = median(
            [s for _, _, s in led["eval_trace"][-3:]])

    os.makedirs("results/s0_11/states", exist_ok=True)
    os.makedirs("results/s0_11/runs_b", exist_ok=True)
    if not smoke:
        serialize_state(sub, head, y_scale,
                        f"results/s0_11/states/{set_name}_{seed}.json")

    ki = float(sub.kappa_i)
    if set_name == "tapsonly":
        # §18.6a: eval-F is the verdict protocol; converged tap params
        # co-reported.
        row["final_ser_fine"] = final_fine_ser(sub, head, y_scale)
        taps = list(sub.input_taps)
        row["tap_r"] = [round(float(sub.kappa_ext[j] / ki), 4) for j in taps]
        row["tap_delta_over_ki"] = [round(float(sub.delta[j] / ki), 4)
                                    for j in taps]
        row["interior_moved_max"] = float(
            (sub.kappa_ext.detach() / ki - 0.3).abs()[
                [j for j in range(sub.N) if j not in taps]].max())
    else:
        # §18.6b: N_eff readout ablation. Ranking = ascending |c_j|·ā_j with
        # ā_j the settled CW amplitude (S0.4-0 participation convention,
        # noiseless); evaluation = coarse protocol of record (ASE on),
        # decoder frozen (trained head + trained y_scale, §17.7 rule).
        ase_saved = sub.ase_variance_scale
        sub.ase_variance_scale = 0.0
        prof = cal.participation_profile(sub)["profile_rel"]
        sub.ase_variance_scale = ase_saved
        cmag = sub.c_readout.detach().abs()
        contrib = [float(cmag[j]) * prof[j] for j in range(sub.N)]
        order = sorted(range(sub.N), key=lambda j: contrib[j])
        c_orig = sub.c_readout.detach().clone()
        curve = []
        with torch.no_grad():
            for k in range(0, sub.N):
                c = c_orig.clone()
                c[order[:k]] = 0
                sub.c_readout.copy_(c)
                ser = eval_ser(sub, head, y_scale, n_batches=COARSE_BATCHES)
                curve.append([k, float(ser)])
                if ser > 0.5:        # chance-level; curve is dead beyond here
                    break
            sub.c_readout.copy_(c_orig)
        passing = [k for k, s in curve if s <= SER_TARGET]
        n_drop = max(passing) if passing else None
        if n_drop is None:               # solution itself above target —
            row["ablation_invalid"] = True   # cannot happen for converged
            n_drop = 0                       # winners (k=0 passes); flagged.
        row["ablation"] = {
            "order_1based": [j + 1 for j in order],
            "contrib_sorted": [f"{contrib[j]:.3e}" for j in order],
            "curve": curve,
            "n_drop_star": n_drop,
            "n_eff": sub.N - n_drop,
        }
        # Registered robustness row: head refit at k = n_drop*+1.
        k_fail = n_drop + 1
        if k_fail < sub.N:
            with torch.no_grad():
                c = c_orig.clone()
                c[order[:k_fail]] = 0
                sub.c_readout.copy_(c)
                u0, _ = fresh_batch(seed, 0)
                y0 = sub.forward_intensity(encode_drive(u0).unsqueeze(-1),
                                           generator=ase_gen(seed, 0, 22))
                ys_abl = float(y0.mean()) + 1e-30
            head_r = TapHead()
            head_r.load_state_dict(head.state_dict())
            opt = torch.optim.Adam(head_r.parameters(), lr=REFIT_LR)
            for it in range(1, REFIT_UPDATES + 1):
                u_raw, target = fresh_batch(seed, it)
                y = sub.forward_intensity(encode_drive(u_raw).unsqueeze(-1),
                                          generator=ase_gen(seed, it, 21))
                loss = torch.nn.functional.mse_loss(
                    head_r(y / ys_abl), target)
                opt.zero_grad()
                loss.backward()
                opt.step()
            with torch.no_grad():
                ser_refit = eval_ser(sub, head_r, ys_abl,
                                     n_batches=COARSE_BATCHES)
                sub.c_readout.copy_(c_orig)
            row["ablation"]["refit_at_k"] = k_fail
            row["ablation"]["refit_ser"] = float(ser_refit)
            row["ablation"]["refit_recovers"] = bool(ser_refit <= SER_TARGET)

    row["wall_s"] = round(time.time() - t0, 1)
    out = f"results/s0_11/runs_b/{set_name}_{seed}.json"
    with open(out, "w") as fh:
        json.dump(row, fh)
    msg = f"done {set_name}_{seed}: fp={row['fingerprint']}"
    if "ablation" in row:
        msg += (f" n_eff {row['ablation']['n_eff']}"
                f" refit_rec {row['ablation'].get('refit_recovers')}")
    if set_name == "tapsonly":
        msg += (f" coarse {row['final_ser_coarse']:.2e}"
                f" fine {row['final_ser_fine']:.2e} tap_r {row['tap_r']}")
    print(msg + f" [{row['wall_s']}s]")


if __name__ == "__main__":
    main()
