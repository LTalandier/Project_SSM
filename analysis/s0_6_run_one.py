# NEW (task S0.6, 2026-07-08) — one (arm, r-value, seed) unit of the damping
# characterization (PR-12 R-ii), spec pre-registered in task_queue.md before
# any run. Writes results/s0_6/runs/<tag>.json.
"""usage: s0_6_run_one.py ARM RVAL SEED   (ARM ∈ {pinned, boxed})"""

from __future__ import annotations

import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from photonic_ssm.estimators.harness import train         # noqa: E402
from photonic_ssm.substrate import cells as cellmod        # noqa: E402

U_MAX = 12000


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def main():
    arm, rval, seed = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
    t0 = time.time()
    if arm == "pinned":
        led = train("bptt", "C-2", run_seed=seed, n_updates=U_MAX,
                    eval_every=100, r0=rval, pin_kext=True)
    elif arm == "boxed":
        r0 = math.sqrt(cellmod.R_MIN_SATURATING * rval)   # registered formula
        led = train("bptt", "C-2", run_seed=seed, n_updates=U_MAX,
                    eval_every=100, r0=r0, r_hi=rval)
    else:
        raise SystemExit(f"unknown arm {arm}")
    evs = [s for _, _, s in led["eval_trace"]]
    row = {"arm": arm, "r": rval, "seed": seed,
           "final_ser": median(evs[-3:]),
           "min_ser": min(evs),
           # plateau flag: last-10-eval improvement < 5% relative
           "plateaued": bool((median(evs[-13:-10]) - median(evs[-3:]))
                             <= 0.05 * max(median(evs[-13:-10]), 1e-9)),
           "eval_trace": led["eval_trace"],
           "final_r": led["in_situ_r"],
           "wall_s": round(time.time() - t0, 1)}
    os.makedirs("results/s0_6/runs", exist_ok=True)
    tag = f"{arm}_{rval}_{seed}"
    with open(f"results/s0_6/runs/{tag}.json", "w") as fh:
        json.dump(row, fh)
    print(f"done {tag}: SER {row['final_ser']:.4f} "
          f"{'plateau' if row['plateaued'] else 'NO-PLATEAU'} "
          f"[{row['wall_s']}s]")


if __name__ == "__main__":
    main()
