# Project_SSM — In-Situ-Trained Photonic State-Space Model on Silicon Nitride

Stage-0 codebase for the research program defined in
**`photonic-ssm-proposal-v0_5.md`** (the authoritative document): an
oscillatory (LinOSS-style) coupled-microring recurrence on SiN, with the
recurrent parameters trained **on the physical device** — evaluated in
Stage 0 by a four-method in-situ-training bake-off (PAT, SPSA, recurrent
adjoint, RHEL) on one shared dissipative ring substrate.

Multi-agent coordination state lives in `shared/` (see `CLAUDE.md`).

## Status

**S0.1 complete** — the first *new* dynamical core: the temporal-CMT
single-ring model + the coupled-ring → N-oscillator LinOSS forward model
(`photonic_ssm/dynamics/`), the realizable pole region, and the
scope-(B) deliverables (B1 actuation map, B2 backscatter bound, B3 κ_ext
trade) under `docs/s0_1/`. The CW limit recovers the S0.0 static
references (the gate). Both architecture constraints are honored in the
new dynamical model (not just inherited). *Still NOT here:* the LinOSS
digital baseline (S0.2), the dissipative substrate + ASE (S0.3), and the
four estimators (S0.4).

**S0.0** — repo skeleton + selective salvage (decision D-2026-06-05-1 →
(a), Lucas 2026-06-08): the salvaged *periphery*.

## Layout: salvaged vs new

Salvaged code carries a provenance header
`# salvaged from pnn-multilayer @ e2eec80 : <original path>` and was
copy-adapted (not git-forked); `~/Documents/pnn-multilayer` remains
read-only upstream.

| Path | Origin | Role |
|---|---|---|
| `photonic_ssm/platforms.py` | salvaged `channels/mrr_platforms.py` (+2 new SiN entries) | platform-constants registry; the SiN Q-range for D-2026-06-08-1 |
| `photonic_ssm/gain.py` | salvaged `physics.py` ~57–136 | instantaneous gain / ASE / NL knobs (S0.3 memoryless tier) |
| `photonic_ssm/dynamic_gain.py` | salvaged `channels/dynamic_soa.py` | rate-equation gain; `TrainingAwareDynamicSOAPerMode` = the constraint-(3a) reference pattern |
| `photonic_ssm/static_rings.py` | salvaged `mrr_primitives.py` statics + drift (+ NEW analytic add-drop refs) | CW-limit test references + S0.3 drift knob |
| `photonic_ssm/estimators/spsa.py` | salvaged `adaptation/perturbation_gradient.py` | S0.4a SPSA + FD/autograd diagnostic + forward-pass accounting (bake-off primary-metric bookkeeping) |
| `photonic_ssm/baselines/ridge_readout.py` | salvaged `equalization_mrr_rc.py` (readout only) | §5.3 reservoir-readout baseline |
| `photonic_ssm/runner/` | pattern-salvaged `sweep_phase4a_mrr1_ringbank.py` + `evaluate.py` JSONL | resume-safe pre-registered-grid sweep scaffold |
| `tests/` | ported + extended from `tests/test_mrr_primitives.py` et al. | 99 tests, all passing |

### New in S0.1 (the dynamical core — not salvage)

| Path | Role |
|---|---|
| `photonic_ssm/dynamics/single_ring.py` | temporal-CMT single ring; pole = recurrence; CW transfers (the gate's reference) |
| `photonic_ssm/dynamics/coupled_rings.py` | `CoupledRingLinOSS` N-oscillator forward model; `a_j=-e^{α_j}+iβ_j`; (3a)/(3b) honored; ZOH matrix-exp; checkpointed unroll |
| `photonic_ssm/dynamics/pole_region.py` | loss/gain→\|λ\| memory bound, κ_ext trade (B3), backscatter crossover (B2) |
| `analysis/s0_1_pole_region.py` | renders pole-region/B2/B3 figures + data → `results/s0_1/` (matplotlib; outside the package) |
| `docs/s0_1/*.md` | mapping notes + B1 actuation map + B2 backscatter bound + B3 κ_ext trade (feed the Supervisor's write-up, PR-2, PR-4) |

**NOT here (new code, S0.2+):** the LinOSS/D-LinOSS *digital* baseline
layer (S0.2), the S0.3 integrated dissipative substrate (incl.
per-round-trip ASE accumulation + the optional B2 splitting knob), PAT,
the recurrent adjoint, RHEL + the concrete χ³-FWM echo sub-model, and the
bake-off evaluator/protocol.

## The two architecture constraints (binding on all S0.1+ core code)

1. **(3a) Gradients flow through the optical state.** Never integrate
   substrate dynamics under `torch.no_grad()`/`.detach()` (the source
   repo's forward-only channel style). Reference pattern:
   `dynamic_gain.TrainingAwareDynamicSOAPerMode` (autograd through the
   rollout, gradient-checkpointed). Enforced by
   `tests/test_dynamic_gain.py::test_gradient_flows_through_state_and_params`.
2. **(3b) Expose full state trajectories.** The substrate/forward API
   must return the internal state trajectory x₁..x_T (adjoint + RHEL
   consume it; the reservoir baseline reads it). Already the contract of
   `baselines.ReservoirReadoutBaseline` ([T, F] trajectories in).

## Setup & tests

```bash
pip install -r requirements.txt   # package runtime is torch-only
python3 -m pytest tests/ -q       # 60 tests, ~2 s on CPU
```

## Quality conventions

Pre-registered grids; ≥4 seeds per configuration (8+ for SPSA);
resume-safe keyed-JSON sweeps (`runner.run_sweep`); JSONL run log
(`runner.log_experiment`); raw results under `results/` (git-ignored,
pointers go in `shared/results_log.md`).
