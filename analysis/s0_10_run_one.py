# NEW (S0.10, PR-17, 2026-07-27) — one unit of the eval-F re-evaluation /
# T-A-L damping-transfer sweep. Three unit kinds:
#   diagc1   METHOD SEED N_UP     (S0.5 C-1 diag verbatim + eval-F final)
#   ceiling  SEED                 (BPTT C-2 12,000 verbatim + eval-F final)
#   talong   RVAL SEED            (PR-17 §17.5: pinned BPTT on T-A-L + eval-F)
# Writes results/s0_10/runs_<kind>/<tag>.json.

from __future__ import annotations

import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import photonic_ssm.estimators.harness as harness          # noqa: E402
from photonic_ssm.estimators.harness import (               # noqa: E402
    final_fine_ser, train)
from photonic_ssm.tasks.equalization import TA_LONG_TAPS    # noqa: E402


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def main():
    kind = sys.argv[1]
    t0 = time.time()
    if kind == "diagc1":
        method, seed, n_up = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
        led, sub, head = train(method, "C-1", run_seed=seed, n_updates=n_up,
                               eval_every=100, N=8, return_state=True)
        tag = f"{method}_{seed}"
    elif kind == "ceiling":
        seed = int(sys.argv[2])
        led, sub, head = train("bptt", "C-2", run_seed=seed, n_updates=12000,
                               eval_every=100, return_state=True)
        tag = f"bptt_{seed}"
    elif kind == "talong":
        rval, seed = float(sys.argv[2]), int(sys.argv[3])
        harness.TASK_TAPS = TA_LONG_TAPS          # PR-17 §17.4 task override
        led, sub, head = train("bptt", "C-2", run_seed=seed, n_updates=12000,
                               eval_every=100, r0=rval, pin_kext=True,
                               return_state=True)
        tag = f"pinned_{rval:g}_{seed}"
    else:
        raise SystemExit(f"unknown kind {kind}")

    evs = [s for _, _, s in led["eval_trace"]]
    row = {"kind": kind, "tag": tag,
           "final_ser_coarse": median(evs[-3:]),
           "final_ser_fine": final_fine_ser(
               sub, head, led["y_scale"]),
           # S0.6 plateau flag verbatim (talong claim rule needs it);
           # None for traces too short to evaluate it (smoke only)
           "plateaued": (bool((median(evs[-13:-10]) - median(evs[-3:]))
                              <= 0.05 * max(median(evs[-13:-10]), 1e-9))
                         if len(evs) >= 13 else None),
           "eval_trace": led["eval_trace"],
           "device_passes": led["device_passes"],
           "digital_passes": led["digital_passes"],
           "wall_s": round(time.time() - t0, 1)}
    if kind == "talong":
        row["r"] = rval
    outdir = f"results/s0_10/runs_{kind}"
    os.makedirs(outdir, exist_ok=True)
    with open(f"{outdir}/{tag}.json", "w") as fh:
        json.dump(row, fh)
    print(f"done {kind}/{tag}: coarse {row['final_ser_coarse']:.5f} "
          f"fine {row['final_ser_fine']:.5f} [{row['wall_s']}s]")


if __name__ == "__main__":
    main()
