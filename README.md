# Project_SSM — Training a photonic state-space model in simulation

A research codebase for a dissipative silicon-nitride coupled-ring recurrence,
with PAT, SPSA, recurrent-adjoint, and Hamiltonian-echo estimators evaluated on
one shared substrate. **No chip has been fabricated or trained in this project.**

## Current status — 2026-09-13

Stage 0 produced the P1 simulation manuscript and follow-up experiments through
S0.12. Stage 0b ended at its first arithmetic gate: the best registered inline
cell has **E_digital/E_photonic = 0.64**, below parity and the 3× advantage bar.
The photonic estimate is 1.56× the digital energy. Hardware development and the
higher-rate residue are paused; S0b.1–S0b.3 were not run.

The repository audit found a PAT mismatch-scaling defect. It is fixed, but the
historical m>1 comparisons are **withdrawn**, with no corrected runs claimed.
The base 5%-class comparison and separate drift result are unaffected by this
bug. Total training-energy claims based on optical duration alone are also
withdrawn; the conversion and digital-twin component budgets remain.
See [supplementary N8](paper/supplementary.md) for the audit trail.

- [P1 manuscript](paper/p1_manuscript.md) and [PDF](paper/p1_manuscript.pdf)
- [P5 negative-envelope draft](paper/p5_negative_envelope.md)
- [Stage 0b result](results/s0b_0/reading.md) (restore the bundle if absent)
- [Pre-registration and post-run errata](shared/preregistration.md)
- [Current handoff](shared/PROJECT_HANDOFF.md)

Submission/public release remains pending. No email or publication is part of
the repair workflow.

## Setup and verification

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest -q
python3 scripts/reproduce_paper.py verify
python3 scripts/reproduce_paper.py restore
python3 analysis/make_figures.py
python3 analysis/make_sfigures.py
python3 analysis/build_manuscript.py
```

The revised suite has **169 tests**. The package runtime is PyTorch-only;
analysis, rendering, and independent numerical reference tests have additional
dependencies. Versions used for this audit are recorded in
[the reproduction environment](paper/repro/environment.txt).

[Reproduction instructions](paper/repro/README.md) distinguish regenerating
figures from stored results from rerunning the original training experiments.
The archive includes historical invalid records for audit; their inclusion does
not reinstate withdrawn claims. The generic sweep runner uses atomic replacement
for saved results; it does not support simultaneous writers to the same path.

## Layout

| Directory | Purpose |
|---|---|
| `photonic_ssm/dynamics/` | Coupled-mode dynamics and pole mapping |
| `photonic_ssm/substrate/` | Shared gain, noise, splitting, and ring model |
| `photonic_ssm/estimators/` | PAT, SPSA, adjoint, RHEL, training and drift harness |
| `photonic_ssm/linoss/` | Digital benchmark implementation |
| `analysis/` | Experiment drivers, summaries, figures, manuscript build |
| `tests/` | Physics references, gradients, protocol and persistence checks |
| `paper/` | Manuscript sources, figures, supplementary, reproduction archive |
| `docs/` | Source ledgers and technical memos |
| `shared/` | Registration, decisions, and historical coordination records |

The original proposal is `photonic-ssm-proposal-v0_5.md`; the TFLN v0.2 draft is
historical. Current empirical conclusions and dated corrections take precedence
over proposal aspirations. Salvaged components retain provenance headers from
`pnn-multilayer @ e2eec80`.
