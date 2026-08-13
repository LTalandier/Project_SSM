# NEW (PR-19 §19.6, 🔒 2026-08-13) — the seed-7 sizing pilot (EXCLUDED from
# scoring): T-D solvability probe (BPTT, free partition) + convergence
# flatness for U_MAX + per-unit wall-clock for the fleet projection.
# Writes results/s0_12/pilot_seed7.json. Fleet stays gated on the PI seeing
# the projection.
from __future__ import annotations

import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from photonic_ssm.estimators.harness import train, final_fine_ser_td  # noqa: E402

U_PILOT = 12000


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def main():
    t0 = time.time()
    led, sub, head = train("bptt", "C-2", run_seed=7, n_updates=U_PILOT,
                           eval_every=100, task="td", return_state=True)
    wall = time.time() - t0
    evs = [s for _, _, s in led["eval_trace"]]
    fine = final_fine_ser_td(sub, head, led["y_scale"])
    row = {
        "spec": "PR-19 §19.6 pilot, seed 7 (excluded)",
        "task": "td", "method": "bptt", "n_updates": U_PILOT,
        "eval_trace": led["eval_trace"],
        "final_ser_coarse": median(evs[-3:]),
        "min_ser": min(evs),
        "final_ser_fine": fine,
        "in_situ_r": led["in_situ_r"],
        "wall_s": round(wall, 1),
        "s_per_update": round(wall / U_PILOT, 3),
    }
    os.makedirs("results/s0_12", exist_ok=True)
    with open("results/s0_12/pilot_seed7.json", "w") as fh:
        json.dump(row, fh)
    print(f"pilot done: coarse {row['final_ser_coarse']:.3e} "
          f"fine {fine:.3e} min {row['min_ser']:.3e} "
          f"[{wall:.0f}s, {row['s_per_update']}s/upd]")


if __name__ == "__main__":
    main()
