# S0.3-1 compute estimate (F21)

Aggregate order-of-magnitude compute for the S0.3-1 substrate build + the
coarse damping sweep, with a forward-looking note for S0.4/S0.5. Per the
roadmap F21 rule: **if anything implies cluster spend, stop and escalate to
Lucas via `escalate_to_human.md` before running it.**

## Hardware
Local CPU only (AMD Ryzen AI 9 365, 20 threads, 30 GB RAM); torch 2.x CPU.
**No cloud / cluster spend.** complex128 substrate (S0.1 fidelity).

## Per-primitive cost (measured)
| Operation | C-1 (N=8, 2N=16) | C-2 (N=32, 2N=64) | C-3 (N=128, 2N=256) |
|---|---|---|---|
| forward+backward, T=384, batch 8 | ~22 ms/step | ~55 ms/step | ~0.6 s/step (est.) |
| van-Loan ASE cov + Cholesky (per fwd) | <1 ms | ~3 ms | ~60 ms (est.) |
| 500-step train (one damping point) | ~11 s | ~28 s | ~5 min (est.) |

The ASE injector rebuilds its (2N×2N) van-Loan covariance + Cholesky once per
forward (M1: gain/M fixed within the rollout); the rollout itself is the
dominant cost. C-3/N=128 is ~25× C-1 per step — kept OUT of the gating path
(aspirational axis only; never in the damping sweep or Gate ii).

## This task (S0.3-1) — actuals / estimates
| Item | Cost | Spend |
|---|---|---|
| Substrate + leaf modules (build) | — | $0 |
| 8 registered unit tests (a–h) + checkpoint | ~2 s | $0 |
| E₀ + reachability calibration (5 cells) | ~3 s | $0 |
| M2 validation (2 cells, τ=3.4 ms rate eq.) | ~5 s | $0 |
| **Coarse damping sweep** (2 cells × 5 damping × 4 seeds = 40 configs, 500 steps, batch 8) | **~13 min** | **$0** |
| Smoke test (3 cells × 3 clocks) | ~10 s | $0 |

**Total S0.3-1: ~15 min wall, entirely local CPU, $0. No escalation
required.** The damping sweep is comfortably local-feasible (the deployment
gate). C-3/N=128 is excluded from every gating/sweep path (aspirational).

## Forward-looking note (S0.4 / S0.5 — for the Supervisor; not authorized here)
The bake-off (S0.5) runs **4 estimators + 2 baselines** on the shared
substrate, ≥8 seeds (PR-8), across the loss/gain/ASE sweep, at the registered
cells + the PR-12 damping cell. Order-of-magnitude, using the substrate cost
above and a comparable training budget:

- **SPSA / PAT / adjoint / RHEL** each need O(10²–10³) physical forward passes
  per training run; at C-2 (~55 ms/fwd) a single method×seed×sweep-point is
  minutes, so a full bake-off grid (6 methods × 8 seeds × ~5 sweep points ×
  2 gating cells) is O(10³) runs → **plausibly O(10–100) CPU-hours**. This is
  **near the local/cluster boundary** and depends on the PR-6/PR-7/PR-8 grid
  sizes (not yet frozen).
- **C-3/N=128** at ~25× C-1 cost would dominate if it ever entered the gating
  path — it must stay the labelled aspirational axis (PR-4 v2 §S), as
  registered.
- RHEL's echo sub-model (χ³ FWM) adds a second physical pass per step
  (S0.4c) — roughly doubles RHEL's cost.

**Recommendation (Supervisor):** size the S0.5 bake-off grid at PR-6/7/8 with
this envelope in mind; if the frozen grid × ≥8 seeds × C-2 pushes past
~local-overnight, file a cluster-spend request (escalate_to_human.md) **before**
S0.5 — not at S0.3-1, which is fully local. The S0.4 estimator builds
themselves (no large sweeps) are local.

*Generated as deliverable 10 of S0.3-1; numbers measured on the build host.*
