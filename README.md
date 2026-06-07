# Project_SSM — In-Situ-Trained Photonic State-Space Model on Silicon Nitride

Stage-0 codebase for the research program defined in
**`photonic-ssm-proposal-v0_5.md`** (the authoritative document): an
oscillatory (LinOSS-style) coupled-microring recurrence on SiN, with the
recurrent parameters trained **on the physical device** — evaluated in
Stage 0 by a four-method in-situ-training bake-off (PAT, SPSA, recurrent
adjoint, RHEL) on one shared dissipative ring substrate.

Multi-agent coordination state lives in `shared/` (see `CLAUDE.md`).

## Status

**S0.0 complete** — repo skeleton + selective salvage (decision
D-2026-06-05-1 → (a), Lucas 2026-06-08). The package contains the
salvaged *periphery* only; the SSM core does not exist yet (S0.1+).

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
| `tests/` | ported + extended from `tests/test_mrr_primitives.py` et al. | 60 tests, all passing |

**NOT here (new code, S0.1+):** the temporal-CMT dynamical ring model
(pole-as-recurrence), the LinOSS/D-LinOSS layer + oscillator↔ring
mapping, the S0.3 integrated substrate (incl. per-round-trip ASE
accumulation), PAT, the recurrent adjoint, RHEL + the concrete χ³-FWM
echo sub-model, and the bake-off evaluator/protocol.

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
