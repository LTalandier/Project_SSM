# Pre-Registration Ledger — Stage 0

**Created:** 2026-06-08 (per Critic finding **F12**, `critic_review_stage0-roadmap.md`).
**Owner:** Supervisor maintains; **Lucas freezes each entry**; Critic audits at phase boundaries.

## Discipline

Every margin, gate threshold, task choice, noise cell, budget, and analysis convention that could be
tuned after seeing results is registered **here, dated, and frozen *before* the run it governs.** This is
the single ledger; if a value is decided inside Executor code at implementation time instead of here, the
pre-registration has failed (Critic F12). Each entry is reviewed by the Critic at the relevant phase
boundary before the run proceeds.

**Status legend:** ⬜ UNSET (not yet registered) · 🔒 FROZEN (registered + dated + Lucas-approved) ·
🔁 SUPERSEDED (frozen value changed by logged decision — keep the history).

> **Adoption status (2026-06-08):** **Lucas signed off** ("accept all") — the Critic review
> (APPROVE-WITH-EDITS) is adopted and folded into `stage0_roadmap.md` **v3**. This ledger's *structure* is
> locked; **entries remain UNSET** and each freezes (date + value + Lucas approval) at its governing phase
> boundary.

## Ledger

| ID | Governs | Freeze before | Status | What must be registered | Source |
|----|---------|---------------|--------|-------------------------|--------|
| **PR-1** | Gate (i) | S0.2 run | ⬜ | Gate-i accuracy margin + the named published benchmark it reproduces. | roadmap S0.2 |
| **PR-2** | Bake-off setup | S0.2 | ⬜ | The bake-off **task**; the **hybrid architecture** (what is simulated — layer/stack, encoder, head, nonlinearity); the **trainable-parameter partition** (every method trains the *same* partition); the **in-situ-trainable physical-parameter set + actuation map** (which params, by what actuator — heater detuning vs tunable coupling vs gain). Task sized against S0.1's pole/memory bound + the S0.7-lite niche (PR-10). | F2, white-space |
| **PR-3** | S0.5 target | rule before S0.4 close; **ceiling frozen at S0.4 close** | ⬜ | The bake-off **target rule relative to the BPTT-on-substrate ceiling** ("within X% of exact-gradient accuracy at the same cell"); the **absolute task-utility floor** (ii-a). Register the *rule* (X%) first; measure + freeze the ceiling once at S0.4 close; then run. | F2.3, F10.2 |
| **PR-4** | Substrate + Gate ii | S0.3 build / S0.5 gate | ⬜ | Self-consistent operating **(α, Q_i) pair** (derive one from the other; add a loss↔Q registry check); the **κ_ext policy** (fixed regime or trainable bounds); the named **"realistic SiN noise" cell** (Q/α, NF, ASE level). **Foundry-grade gates Gate ii; class-leading is a labelled aspirational sweep axis.** Resolves D-2026-06-08-1. | F13, F10.5 |
| **PR-5** | PAT (S0.4a) | S0.4a | ⬜ | PAT **twin-mismatch families + levels** (parametric calibration error at realistic characterization accuracy + structural omission); **calibration-error unification** — offline-deploy baseline's weight-mapping error drawn from the *same* family. Headline cell = the registered mismatch level; report PAT as a function of it. | F7.2–3 (CRITICAL) |
| **PR-6** | All estimators (S0.4) | S0.4a | ⬜ | The **fairness contract**: physical-operations invariant (gradients only from simulated device passes on the shared substrate w/ fresh noise; autodiff-through-substrate reserved for the BPTT reference); common θ₀ + data ordering per seed; **equal pre-registered HP budgets** per method; **equal max-device-pass budget B** per cell. | F7 (CRITICAL) |
| **PR-7** | Cost metric (S0.4/S0.5) | S0.4 | ⬜ | Cost **unit = physical device passes, any direction** (per-method table: SPSA 2 fwd; PAT 1 fwd + digital twin-backward on a side-ledger; adjoint 1 fwd + 1 adjoint device pass; RHEL 1 fwd + 1 echo device pass); batch convention; **digital-compute side-ledger** reported alongside. | F5 |
| **PR-8** | S0.5 analysis | S0.5 | ⬜ | Statistical plan: **right-censoring** treatment (fraction-reaching-target within B + median/IQR among reachers / survival treatment); lexicographic ranking (success-fraction, then median passes); paired-by-seed bootstrap CIs; **≥8 seeds for all methods in headline cells** (4 only for exploratory grid). | F11 |
| **PR-9** | Gate ii + promotion | S0.5 | ⬜ | **Gate-ii semantics** decomposed: (ii-a) capacity — BPTT ceiling clears the utility floor; (ii-b) trainability — **PAT or SPSA** within margin of ceiling (only-adjoint/RHEL-pass → escalate-and-redesign, *not* a pass). **Promotion criteria**: "clearly beats" quantified (e.g. ≥X% better pass-to-target w/ non-overlapping 95% CIs, or strictly-better scaling, or strictly-simpler hardware ledger at non-inferior efficiency); **"exactness" struck** from the menu (outcome metrics + F8 hardware ledger only). | F10 |
| **PR-10** | S0.7-lite | before S0.2 task reg | ⬜ | S0.7-lite **assumptions**: conversion energies, DAC/ADC rates, named **digital-baseline class + sources**, operating scale (N rings, rates). Labelled assumption-driven; not load-bearing in outreach before full S0.7. | F1, F16 |
| **PR-11** | RHEL echo (S0.4c) | S0.4c | ⬜ | RHEL echo **invariants**: independent forward/echo ASE streams (no common-RNG reversal); no loss-sign flip (echo through the *same* dissipative substrate); gain injects fresh ASE in the echo too. **Conjugation-fidelity bound** + the **unit test** (echo of a noisy forward must *not* recover the noiseless state; bounded by fidelity × ASE floor). | F9 |
| **PR-12** | Damping cell | after S0.3 coarse sweep, before S0.5 grid | ⬜ | The **central damping operating cell** for the bake-off, from the F3 coarse BPTT-on-substrate sweep; the sweep is over the physical damping **floor** + init/range, not a fixed value. | F3 |
| **PR-13** | S0.5 secondary task | S0.5 | ⬜ | A **synthetic memory-task family** with tunable memory length (delayed recall / sticky detection at parametric lag) as a pre-registered secondary; stress-tests ranking robustness + the memory-vs-Q story. | F20 |
| **PR-14** | Secondary diagnostic | S0.5 | ⬜ | The secondary diagnostic = **bias/variance decomposition of the gradient estimate vs the BPTT reference** (mean error-vector norm + variance), **not raw cosine**; confined to mechanism discussion, never the headline. | F6 |

## Notes

- **Dependency reality:** several entries *consume* upstream numbers that don't exist yet — PR-2's task
  sizing needs S0.1's pole/memory bound; PR-3's ceiling is measured at S0.4 close; PR-4's pair needs the
  S0.1 κ_ext trade. The freeze-before column is the **run it governs**, not "today."
- **Convergence note (PR-4):** the `SiN_LIGENTEC_AN800` registry Q/loss inconsistency (Q=2×10⁶ vs
  0.03 dB/cm ⇒ Q≈1.1×10⁷) was found **independently** by the Executor (S0.0 results) and the Critic
  (F13.1). Fix at S0.1: register one as primary, derive the other, add a loss↔Q self-consistency test.
- This ledger is referenced by `stage0_roadmap.md` and `escalate_to_human.md`. When an entry freezes, log
  the date + the approved value here and cite it from the phase's `task_queue.md` spec.
