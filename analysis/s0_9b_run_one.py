# NEW (S0.9b, PR-16, 2026-07-24) — one (arm, regime, seed) unit of the
# deploy-then-drift sweep. Writes results/s0_9/runs_b/<tag>.json.
"""usage: s0_9b_run_one.py ARM REGIME SEED [fine]
   ARM ∈ {insitu-pat, insitu-spsa, offline-head, offline-relock}
   REGIME ∈ {common, independent}; trailing "fine" = PR-17 eval-F for ser0 and
   every per-step evaluation, output to results/s0_10/runs_b."""

from __future__ import annotations

import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from photonic_ssm.estimators.drift import deploy_then_drift  # noqa: E402
from photonic_ssm.estimators.harness import EVAL_FINE_BATCHES  # noqa: E402

# PR-16 §16.7 frozen build parameters.
SIGMA_STEP = 0.40
K = 12
B_UPDATES = 4000
N_CONVERGE = {"insitu-pat": 20000, "offline-head": 20000,
              "offline-relock": 20000, "insitu-spsa": 15800}


def main():
    arm, regime, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
    fine = len(sys.argv) > 4 and sys.argv[4] == "fine"
    t0 = time.time()
    res = deploy_then_drift(arm, run_seed=seed, regime=regime, K=K,
                            b_updates=B_UPDATES, sigma_step=SIGMA_STEP,
                            n_converge=N_CONVERGE[arm],
                            n_eval_batches=EVAL_FINE_BATCHES if fine else 2)
    res["eval_protocol"] = "eval-F" if fine else "coarse"
    res["wall_s"] = round(time.time() - t0, 1)
    outdir = "results/s0_10/runs_b" if fine else "results/s0_9/runs_b"
    os.makedirs(outdir, exist_ok=True)
    tag = f"{arm}_{regime}_{seed}"
    with open(f"{outdir}/{tag}.json", "w") as fh:
        json.dump(res, fh)
    ser_end = res["ser_traj"][-1][1]
    print(f"done {tag}: ser0={res['ser0']:.4f} ser_end={ser_end:.4f} "
          f"[{res['wall_s']}s]")


if __name__ == "__main__":
    main()
