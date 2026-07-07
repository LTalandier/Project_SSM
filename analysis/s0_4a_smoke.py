# NEW (task S0.4a phase 1, 2026-07-07) — the pre-registered S2 trainability
# smoke (task_queue.md S0.4a spec, committed BEFORE this run at 0b8c817):
# every estimator must cut T-A MSE by >=20 % of its initial value within
# <=300 updates at C-1/N=8, 28 dB, on >=2 of 3 seeds. Head-only = ungated
# context arm (isolates the digital head's share). C-2/N=32 spot = ungated.
"""S0.4a phase-1 smoke. Writes results/s0_4a/smoke.{json,md}.

Operationalization (recorded): initial = mean(loss[0:5]); achieved =
mean(loss[-20:]); PASS iff achieved <= 0.8 * initial.
"""

from __future__ import annotations

import json
import os
import sys
import time

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from photonic_ssm.estimators.harness import train  # noqa: E402

OUT = "results/s0_4a"
METHODS = ("bptt", "pat-perfect", "pat-M-par", "pat-M-struct", "pat-both",
           "spsa", "head-only")
GATED = {m for m in METHODS if m != "head-only"}
SEEDS = (11, 23, 47)
N_UPDATES = 300
REDUCTION = 0.20


def summarize(led):
    tr = led["loss_trace"]
    init = sum(tr[:5]) / 5.0
    final = sum(tr[-20:]) / 20.0
    return {"loss_init_mean5": init, "loss_final_mean20": final,
            "reduction_frac": 1.0 - final / init,
            "ser_final": led["ser_final"],
            "device_passes": led["device_passes"],
            "digital_passes": led["digital_passes"]}


def main():
    os.makedirs(OUT, exist_ok=True)
    out = {"spec": "task_queue.md S0.4a (pre-registered at 0b8c817)",
           "cell": "C-1/N=8, 28 dB, T=256, batch 8",
           "gate_S2": f"reduction >= {REDUCTION:.0%} within {N_UPDATES} "
                      f"updates on >=2/3 seeds (gated methods)",
           "runs": {}, "gate_results": {}}
    for m in METHODS:
        rows = []
        for s in SEEDS:
            t0 = time.time()
            led = train(m, "C-1", run_seed=s, n_updates=N_UPDATES, N=8)
            row = summarize(led)
            row["seed"] = s
            row["wall_s"] = round(time.time() - t0, 1)
            rows.append(row)
            print(f"  {m} seed {s}: init {row['loss_init_mean5']:.4f} -> "
                  f"final {row['loss_final_mean20']:.4f} "
                  f"({row['reduction_frac']:+.1%}); SER {row['ser_final']:.3f}; "
                  f"passes dev {row['device_passes']}/dig "
                  f"{row['digital_passes']} [{row['wall_s']}s]")
        out["runs"][m] = rows
        if m in GATED:
            n_pass = sum(r["reduction_frac"] >= REDUCTION for r in rows)
            out["gate_results"][m] = {"seeds_passing": n_pass,
                                      "S2_pass": bool(n_pass >= 2)}
            print(f"  => S2 {m}: {n_pass}/3 seeds "
                  f"{'PASS' if n_pass >= 2 else 'FAIL'}")

    print("[C-2/N=32 spot, 1 seed x 100 updates — ungated]")
    out["c2_spot"] = {}
    for m in ("bptt", "pat-both", "spsa"):
        t0 = time.time()
        led = train(m, "C-2", run_seed=11, n_updates=100)
        row = summarize(led)
        row["wall_s"] = round(time.time() - t0, 1)
        out["c2_spot"][m] = row
        print(f"  {m}: init {row['loss_init_mean5']:.4f} -> final "
              f"{row['loss_final_mean20']:.4f} ({row['reduction_frac']:+.1%}) "
              f"[{row['wall_s']}s]")

    out["S2_overall_pass"] = all(v["S2_pass"]
                                 for v in out["gate_results"].values())
    with open(os.path.join(OUT, "smoke.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("S2 overall:", "PASS" if out["S2_overall_pass"] else "FAIL")
    print("wrote", os.path.join(OUT, "smoke.json"))


if __name__ == "__main__":
    main()
