# NEW (task S0.4b, 2026-07-07) — the pre-registered S0.4b smoke
# (task_queue.md S0.4b spec, committed c85fe62 BEFORE this run):
# B2 (saturating-noiseless adjoint-vs-BPTT cosine at θ₀, C-1 + C-2;
# registered expectation ≥ 0.9, report-only), B3 (trainability, mirrors S2:
# ≥20 % MSE cut within ≤300 updates, C-1/N=8, ≥2/3 seeds {11,23,47}),
# + the ungated C-2/N=32 spot (extends the S0.4a sizing-flag row).
"""S0.4b smoke. Writes results/s0_4b/smoke.{json,md}.

Operationalization (identical to S0.4a): initial = mean(loss[0:5]);
achieved = mean(loss[-20:]); B3 PASS iff achieved <= 0.8 * initial on
>= 2 of 3 seeds.
"""

from __future__ import annotations

import json
import os
import sys
import time

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from photonic_ssm.estimators.adjoint import AdjointEstimator  # noqa: E402
from photonic_ssm.estimators.harness import (                 # noqa: E402
    TapHead, encode_drive, fresh_batch, make_substrate, mse_loss, train,
)

OUT = "results/s0_4b"
SEEDS = (11, 23, 47)
N_UPDATES = 300
REDUCTION = 0.20


def b2_cosine(cell: str, N: int, seed: int = 3) -> float:
    """Saturating-noiseless adjoint-vs-full-BPTT gradient cosine at θ₀ on a
    fresh T-A batch through an init head (B2, report-only)."""
    sub = make_substrate(cell, seed=seed, N=N)
    sub.ase_variance_scale = 0.0
    torch.manual_seed(seed)
    head = TapHead()
    u_raw, target = fresh_batch(seed, 1)
    u = encode_drive(u_raw).unsqueeze(-1)
    with torch.no_grad():
        y_scale = float(sub.forward_intensity(u).mean()) + 1e-30

    def flat():
        return torch.cat([p.grad.reshape(-1).clone()
                          for p in (sub.delta, sub.kappa_ext, sub.mu_chain)])

    est = AdjointEstimator(sub)
    est.step(u, lambda y: mse_loss(head(y / y_scale), target))
    g_adj = flat()
    for p in (sub.delta, sub.kappa_ext, sub.mu_chain):
        p.grad = None
    for p in head.parameters():
        p.grad = None
    y = sub.forward_intensity(u)
    mse_loss(head(y / y_scale), target).backward()
    g_bptt = flat()
    return float(torch.dot(g_adj, g_bptt) /
                 (g_adj.norm() * g_bptt.norm() + 1e-300))


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
    out = {"spec": "task_queue.md S0.4b (pre-registered at c85fe62)",
           "cell": "C-1/N=8, 28 dB, T=256, batch 8",
           "gate_B3": f"reduction >= {REDUCTION:.0%} within {N_UPDATES} "
                      f"updates on >=2/3 seeds"}

    print("[B2 — saturating-noiseless adjoint-vs-BPTT cosine (report-only, "
          "expectation >= 0.9)]")
    out["B2_cosines"] = {}
    for cell, N in (("C-1", 8), ("C-2", 32)):
        c = b2_cosine(cell, N)
        out["B2_cosines"][f"{cell}/N={N}"] = c
        print(f"  {cell}/N={N}: cosine(adjoint, BPTT) = {c:.6f} "
              f"[{'meets' if c >= 0.9 else 'MISSES'} expectation]")

    print(f"[B3 — adjoint trainability, {N_UPDATES} updates, "
          f"seeds {SEEDS}]")
    rows = []
    for s in SEEDS:
        t0 = time.time()
        led = train("adjoint", "C-1", run_seed=s, n_updates=N_UPDATES, N=8)
        row = summarize(led)
        row["seed"] = s
        row["wall_s"] = round(time.time() - t0, 1)
        rows.append(row)
        print(f"  adjoint seed {s}: init {row['loss_init_mean5']:.4f} -> "
              f"final {row['loss_final_mean20']:.4f} "
              f"({row['reduction_frac']:+.1%}); SER {row['ser_final']:.3f}; "
              f"passes dev {row['device_passes']}/dig "
              f"{row['digital_passes']} [{row['wall_s']}s]")
    out["runs"] = rows
    n_pass = sum(r["reduction_frac"] >= REDUCTION for r in rows)
    out["gate_results"] = {"seeds_passing": n_pass,
                           "B3_pass": bool(n_pass >= 2)}
    print(f"  => B3: {n_pass}/3 seeds {'PASS' if n_pass >= 2 else 'FAIL'}")

    print("[C-2/N=32 spot, 1 seed x 100 updates — ungated]")
    t0 = time.time()
    led = train("adjoint", "C-2", run_seed=11, n_updates=100)
    row = summarize(led)
    row["wall_s"] = round(time.time() - t0, 1)
    out["c2_spot"] = row
    print(f"  adjoint: init {row['loss_init_mean5']:.4f} -> final "
          f"{row['loss_final_mean20']:.4f} ({row['reduction_frac']:+.1%}) "
          f"[{row['wall_s']}s]")

    with open(os.path.join(OUT, "smoke.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("B3 overall:", "PASS" if out["gate_results"]["B3_pass"] else "FAIL")
    print("wrote", os.path.join(OUT, "smoke.json"))


if __name__ == "__main__":
    main()
