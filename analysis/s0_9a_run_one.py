# NEW (S0.9a, 2026-07-22) — one (method, seed, mismatch_scale) unit of the
# PR-5 §E mismatch-sensitivity sweep. In-situ PAT-both vs offline-deploy at
# C-2, scaling the M-par calibration/actuation gap by m. Writes
# results/s0_9/runs_a/<tag>.json; merge/stats in analysis/s0_9_analyze.py.
"""usage: s0_9a_run_one.py METHOD SEED M_SCALE N_UPDATES [fine]
   METHOD ∈ {pat-both, offline-deploy}; trailing "fine" = PR-17 eval-F final
   evaluation, output to results/s0_10/runs_a (frozen unit otherwise verbatim)."""

from __future__ import annotations

import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from photonic_ssm.estimators.harness import final_fine_ser, train  # noqa: E402


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def main():
    method, seed, m, n_up = (sys.argv[1], int(sys.argv[2]),
                             float(sys.argv[3]), int(sys.argv[4]))
    fine = len(sys.argv) > 5 and sys.argv[5] == "fine"
    t0 = time.time()
    out = train(method, "C-2", run_seed=seed, n_updates=n_up, eval_every=100,
                mismatch_scale=m, return_state=fine)
    led, sub, head = out if fine else (out, None, None)
    row = {"method": method, "cell": "C-2", "seed": seed, "mismatch_scale": m,
           "n_updates": n_up,
           "final_ser": median([s for _, _, s in led["eval_trace"][-3:]]),
           "eval_trace": led["eval_trace"],
           "device_passes": led["device_passes"],
           "digital_passes": led["digital_passes"],
           "wall_s": round(time.time() - t0, 1)}
    outdir = "results/s0_10/runs_a" if fine else "results/s0_9/runs_a"
    if fine:
        row["final_ser_fine"] = final_fine_ser(sub, head, led["y_scale"])
        row["wall_s"] = round(time.time() - t0, 1)
    os.makedirs(outdir, exist_ok=True)
    tag = f"{method}_m{m:g}_{seed}"
    with open(f"{outdir}/{tag}.json", "w") as fh:
        json.dump(row, fh)
    print(f"done {tag}: SER {row['final_ser']:.4f} [{row['wall_s']}s]")


if __name__ == "__main__":
    main()
