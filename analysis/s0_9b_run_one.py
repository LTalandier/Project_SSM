# NEW (S0.9b, PR-16, 2026-07-24) — one (arm, regime, seed) unit of the
# deploy-then-drift sweep. Writes results/s0_9/runs_b/<tag>.json.
"""usage: s0_9b_run_one.py ARM REGIME SEED
   ARM ∈ {insitu-pat, insitu-spsa, offline-head, offline-relock}
   REGIME ∈ {common, independent}"""

from __future__ import annotations

import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from photonic_ssm.estimators.drift import deploy_then_drift  # noqa: E402

# PR-16 §16.7 frozen build parameters.
SIGMA_STEP = 0.40
K = 12
B_UPDATES = 4000
N_CONVERGE = {"insitu-pat": 20000, "offline-head": 20000,
              "offline-relock": 20000, "insitu-spsa": 15800}


def main():
    arm, regime, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
    t0 = time.time()
    res = deploy_then_drift(arm, run_seed=seed, regime=regime, K=K,
                            b_updates=B_UPDATES, sigma_step=SIGMA_STEP,
                            n_converge=N_CONVERGE[arm])
    res["wall_s"] = round(time.time() - t0, 1)
    os.makedirs("results/s0_9/runs_b", exist_ok=True)
    tag = f"{arm}_{regime}_{seed}"
    with open(f"results/s0_9/runs_b/{tag}.json", "w") as fh:
        json.dump(res, fh)
    ser_end = res["ser_traj"][-1][1]
    print(f"done {tag}: ser0={res['ser0']:.4f} ser_end={ser_end:.4f} "
          f"[{res['wall_s']}s]")


if __name__ == "__main__":
    main()
