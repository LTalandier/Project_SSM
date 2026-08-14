# NEW (PR-19, 🔒 2026-08-13; U_MAX=3,000 per §19.6a addendum b55b135) — one
# T-D fleet unit. Writes results/s0_12/runs/<tag>.json + states/<tag>.json.
# The PAT arm records the FULL frozen-decoder ablation curve (§18.6b path);
# the target crossing + refit row are applied at analysis time, after the
# ceiling addendum (§19.3 ordering).
"""usage: s0_12_run_one.py pinned RVAL SEED | ceiling SEED | pat SEED"""

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
    train, eval_ser_td, final_fine_ser_td)
import s0_4_0_calibration as cal                # noqa: E402

U_MAX = 3000        # §19.6a


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def serialize(sub, head, y_scale, path):
    st = {"delta": sub.delta.detach().tolist(),
          "kappa_ext": sub.kappa_ext.detach().tolist(),
          "mu_chain": sub.mu_chain.detach().tolist(),
          "c_readout_re": sub.c_readout.detach().real.tolist(),
          "c_readout_im": sub.c_readout.detach().imag.tolist(),
          "head": {k: v.tolist() for k, v in head.state_dict().items()},
          "y_scale": y_scale, "kappa_i": float(sub.kappa_i)}
    with open(path, "w") as fh:
        json.dump(st, fh)


def main():
    arm = sys.argv[1]
    if arm == "pinned":
        rval, seed = float(sys.argv[2]), int(sys.argv[3])
        tag = f"pinned_{rval}_{seed}"
        kw = dict(method="bptt", r0=rval, pin_kext=True)
    elif arm == "ceiling":
        seed = int(sys.argv[2])
        tag = f"ceiling_{seed}"
        kw = dict(method="bptt")
    elif arm == "pat":
        seed = int(sys.argv[2])
        tag = f"pat_{seed}"
        kw = dict(method="pat-both")
    else:
        raise SystemExit(f"unknown arm {arm}")

    t0 = time.time()
    led, sub, head = train(cell_label="C-2", run_seed=seed, n_updates=U_MAX,
                           eval_every=100, task="td", return_state=True,
                           **kw)
    y_scale = led["y_scale"]
    evs = [s for _, _, s in led["eval_trace"]]
    ki = float(sub.kappa_i)
    row = {"arm": arm, "seed": seed, "tag": tag,
           "r": kw.get("r0"), "n_updates": U_MAX,
           "eval_trace": led["eval_trace"],
           "final_ser": median(evs[-3:]), "min_ser": min(evs),
           "final_ser_fine": final_fine_ser_td(sub, head, y_scale),
           "plateaued": bool((median(evs[-13:-10]) - median(evs[-3:]))
                             <= 0.05 * max(median(evs[-13:-10]), 1e-9)),
           "in_situ_r": led["in_situ_r"],
           "delta_over_ki": [round(float(x), 5)
                             for x in (sub.delta.detach() / ki)],
           "mu_over_ki": [round(float(x), 5)
                          for x in (sub.mu_chain.detach() / ki)],
           "device_passes": led["device_passes"]}

    os.makedirs("results/s0_12/states", exist_ok=True)
    os.makedirs("results/s0_12/runs", exist_ok=True)
    serialize(sub, head, y_scale, f"results/s0_12/states/{tag}.json")

    if arm == "pat":
        # §19.4-P2: the §18.6b ablation, frozen decoder, FULL curve recorded;
        # crossing + refit applied at analysis (target needs the ceiling).
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
                ser = eval_ser_td(sub, head, y_scale)
                curve.append([k, float(ser)])
                if ser > 0.5:
                    break
            sub.c_readout.copy_(c_orig)
        row["ablation"] = {"order_1based": [j + 1 for j in order],
                           "curve": curve}

    row["wall_s"] = round(time.time() - t0, 1)
    with open(f"results/s0_12/runs/{tag}.json", "w") as fh:
        json.dump(row, fh)
    print(f"done {tag}: coarse {row['final_ser']:.3e} "
          f"fine {row['final_ser_fine']:.3e} "
          f"{'plateau' if row['plateaued'] else 'NO-PLATEAU'} "
          f"[{row['wall_s']:.0f}s]")


if __name__ == "__main__":
    main()
