# Results Log

The **Executor** appends experiment results here (newest at top). The **Supervisor** reads and
evaluates them, then assigns the next task. The **Critic** reads this file to check claims against data.

Per result, report:
- **Phase / task** and **date**
- **Goal** — what this run tested
- **Config** — grid size, key parameters, seed count
- **Key findings** — numbered, with specific numbers
- **Gates** — passed / failed (vs the pre-registered criterion)
- **Anomalies / concerns** — anything surprising or fragile
- **Data path** — where the raw results live
- **Compute used** — where it ran, wall-clock, cost (if cloud)

---

**S0.0a — Tooling recon (2026-06-07, Executor):** report at [`shared/tooling_recon.md`](tooling_recon.md) — `equalization_ringbank.py` is **not** a head start for the S0.1 mapping (all `pnn-multilayer` ring code is static/CW transfer functions; the dynamical CMT core is new code either way), but SPSA + pass-accounting, rate-equation gain (autograd-checkpointed), SiN platform registry, drift machinery, ridge readout and sweep scaffolding are liftable → recommendation: **(a) selective salvage** (≈1 day port vs ≈3–5 days extra for clean start). Read-only; no code written. Awaiting Lucas's D-1/D-2 rulings.
