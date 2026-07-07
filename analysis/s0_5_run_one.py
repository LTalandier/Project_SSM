# NEW (S0.4-close/S0.5-core, 2026-07-07) — one (method, cell, seed) unit of
# the ceiling/bake-off, for the 20-core parallel launcher. Writes
# results/s0_5/runs/<tag>.json; the merge steps assemble ceiling.json /
# bakeoff_runs.json for analysis/s0_5_bakeoff.py stats.
"""usage: s0_5_run_one.py METHOD CELL SEED N_UPDATES [fixed]"""

from __future__ import annotations

import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from photonic_ssm.estimators.harness import train  # noqa: E402


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def main():
    method, cell, seed, n_up = (sys.argv[1], sys.argv[2], int(sys.argv[3]),
                                int(sys.argv[4]))
    gain_mode = "fixed" if (len(sys.argv) > 5 and sys.argv[5] == "fixed") \
        else None
    t0 = time.time()
    led = train(method, cell, run_seed=seed, n_updates=n_up, eval_every=100,
                gain_mode=gain_mode, N=8 if cell == "C-1" else None)
    row = {"method": method, "cell": cell, "seed": seed,
           "gain_mode": gain_mode or "saturating", "n_updates": n_up,
           "final_ser": median([s for _, _, s in led["eval_trace"][-3:]]),
           "eval_trace": led["eval_trace"],
           "device_passes": led["device_passes"],
           "digital_passes": led["digital_passes"],
           "wall_s": round(time.time() - t0, 1)}
    os.makedirs("results/s0_5/runs", exist_ok=True)
    tag = f"{method}_{cell}_{seed}" + ("_fixed" if gain_mode else "")
    with open(f"results/s0_5/runs/{tag}.json", "w") as fh:
        json.dump(row, fh)
    print(f"done {tag}: SER {row['final_ser']:.4f} [{row['wall_s']}s]")


if __name__ == "__main__":
    main()
