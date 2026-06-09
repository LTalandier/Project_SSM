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
>
> **Update (2026-06-09, Lucas "ok go" — E-2026-06-09-2):** **PR-15 registered and 🔒 FROZEN** (the first
> frozen entry; detail block at the end of this file). **PR-2 and PR-4 gained blessed *constraints*** from
> the resolved D-2026-06-08-2 / D-2026-06-08-3 (see Notes) — the entries themselves remain ⬜ until their
> own freeze.

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
| **PR-10** | S0.7-lite | before S0.2 task reg | ⬜ **PROPOSED 2026-06-10** (block below — awaiting Lucas freeze) | S0.7-lite **assumptions**: conversion energies, DAC/ADC rates, named **digital-baseline class + sources**, operating scale (N rings, rates). Labelled assumption-driven; not load-bearing in outreach before full S0.7. | F1, F16 |
| **PR-11** | RHEL echo (S0.4c) | S0.4c | ⬜ | RHEL echo **invariants**: independent forward/echo ASE streams (no common-RNG reversal); no loss-sign flip (echo through the *same* dissipative substrate); gain injects fresh ASE in the echo too. **Conjugation-fidelity bound** + the **unit test** (echo of a noisy forward must *not* recover the noiseless state; bounded by fidelity × ASE floor). | F9 |
| **PR-12** | Damping cell | after S0.3 coarse sweep, before S0.5 grid | ⬜ | The **central damping operating cell** for the bake-off, from the F3 coarse BPTT-on-substrate sweep; the sweep is over the physical damping **floor** + init/range, not a fixed value. | F3 |
| **PR-13** | S0.5 secondary task | S0.5 | ⬜ | A **synthetic memory-task family** with tunable memory length (delayed recall / sticky detection at parametric lag) as a pre-registered secondary; stress-tests ranking robustness + the memory-vs-Q story. | F20 |
| **PR-14** | Secondary diagnostic | S0.5 | ⬜ | The secondary diagnostic = **bias/variance decomposition of the gradient estimate vs the BPTT reference** (mean error-vector norm + variance), **not raw cosine**; confined to mechanism discussion, never the headline. | F6 |
| **PR-15** | Pre-S0.2 continuation gate | the white-space search run (now) | 🔒 **FROZEN 2026-06-09** | White-space **existence** go/no-go (debt #1, front-loaded — D-2026-06-09-1): rule-form kill-criterion (q1∧q2∧q3) + search lanes + two-modality protocol + disposition. **Full frozen detail in the block below** — the table row is a pointer only. | D-09-1, F15 |

## Notes

- **Dependency reality:** several entries *consume* upstream numbers that don't exist yet — PR-2's task
  sizing needs S0.1's pole/memory bound; PR-3's ceiling is measured at S0.4 close; PR-4's pair needs the
  S0.1 κ_ext trade. The freeze-before column is the **run it governs**, not "today."
- **Convergence note (PR-4):** the `SiN_LIGENTEC_AN800` registry Q/loss inconsistency (Q=2×10⁶ vs
  0.03 dB/cm ⇒ Q≈1.1×10⁷) was found **independently** by the Executor (S0.0 results) and the Critic
  (F13.1). Fix at S0.1: register one as primary, derive the other, add a loss↔Q self-consistency test.
- **PR-2 constraints from resolved D-2026-06-08-2 (Lucas 2026-06-09):** the simulated layer is the
  **diagonal complex-pole SSM (S4D/DSS class)** — one ring = one complex pole; LinOSS is the uncoupled +
  real-I/O conjugate-pair special case; trainable inter-ring μ is a **mild generalization beyond**
  standard diagonal-A LinOSS (benchmark transfer = **debt #2**, validated in-house via the PR-3
  BPTT-on-substrate ceiling). At the PR-2 freeze: **pin the readout** (coherent-quadrature = real-linear,
  LinOSS-equivalent head **vs** intensity = |·|², nonlinear head) and address the **F6 κ_ext dual-role**
  (damping actuator vs readout knob — keep the reservoir-baseline contrast clean).
- **PR-4 constraints from resolved D-2026-06-08-3 (Lucas 2026-06-09):** the realistic-SiN cell gains a
  **roughness/splitting sub-parameter**; splitting is evaluated at the **operating κ_ext** (not the
  undercoupled worst case — overcoupling suppresses the visible doublet); the S0.3 CW/CCW knob defaults
  **ON except the clean-damascene corner**, and if the single-pole substrate relies on the clean corner
  PR-4 must state that assumption explicitly; resolve **jointly with D-2026-06-08-1** (the (α, Q_i)
  operating pair). B2 crossover numbers remain provisional until the F5 primary-source pass (S0.L).
- This ledger is referenced by `stage0_roadmap.md` and `escalate_to_human.md`. When an entry freezes, log
  the date + the approved value here and cite it from the phase's `task_queue.md` spec.

## PR-15 — frozen detail (registered + 🔒 FROZEN 2026-06-09; Lucas "ok go", E-2026-06-09-2)

**Governs:** the white-space existence search (debt #1, front-loaded pre-S0.2 — D-2026-06-09-1) and the
**pre-S0.2 continuation gate** it feeds. Frozen *before* the search runs, per ledger discipline.

**Claim under test (existence form, sharpened):** *recurrent parameters — parameters that define the
recurrence of a physical photonic system (pole positions / feedback / inter-node couplings) — updated on
the physical device by gradient-based/-estimating training*: believed never demonstrated. The exact claim
**wording** (vs the B1 trained set) is refined at PR-2/S0.8 — this gate tests **existence only**.

**Kill-rule — a prior is FATAL iff q1 ∧ q2 ∧ q3:**
- **q1 — internal to the recurrence.** The updated parameters are feedback/coupling/pole-defining (they
  define the recurrent map). Readout-only, input-mask-only, or encoder-only training does **not** satisfy
  q1 (that is reservoir computing).
- **q2 — on the physical device, in the loop.** Updates are applied to the physical system inside the
  training loop (forward passes are physical). Simulate-train-then-deploy / offline transfer does **not**
  satisfy q2.
- **q3 — gradient-based or gradient-estimating rule.** Backprop / in-situ adjoint / PAT-style hybrid
  (digital backward, physical forward); zeroth-order perturbative (SPSA, finite-difference — estimates a
  descent direction from perturbation measurements); REINFORCE/policy-gradient (reward-gradient
  estimator). Population-selection methods (genetic/evolutionary/CMA-ES/Boolean/exhaustive search) do
  **not** satisfy q3 — such priors are **non-fatal but MUST be cited** (they make the
  "gradient-based/-estimating" qualifier load-bearing in the claim).

**Search lanes (F15 + named groups; lanes locate, the rule decides):** (i) zeroth-order/perturbative
updates of internal params of any recurrent photonic system; (ii) REINFORCE/policy-gradient updates of
internal recurrent params — incl. the **Bueno/Brunner boundary memo** (verify in primary sources what that
line physically updates); (iii) hardware-in-the-loop adaptation of delay-reservoir *feedback/internal*
params (fatal **iff q3 also holds**); (iv) evolutionary/Boolean internal-weight training (non-fatal lane —
cite); (v) free/forward search through the snapshot date + a **named-group minimum set** (extend, don't
truncate): Brunner/Fischer/Bueno (photonic RNN/reservoir), Shastri/Prucnal (neuromorphic photonics),
Wright/Onodera/McMahon (PAT), Hughes/Fan (in-situ adjoint), Englund/Bandyopadhyay/Hamerly (on-chip
training), Psaltis/Moser, Lvovsky, Momeni/Fleury (physical local learning), Marquardt (physical learning
theory), coupled-laser-array / optoelectronic-oscillator adaptive-control literature.

**Protocol (two-modality — the B2/F5 lesson):** (1) **Executor systematic sweep** → dated memo
`docs/s0_L/debt1_whitespace_search.md`: per-candidate verdict table (citation · system · what was
physically updated · q1? · q2? · q3 class · verdict FATAL / non-fatal-cite / AMBIGUOUS / clear), **every
verdict grounded in the primary source with the load-bearing sentence quoted** — no aggregator-snippet
citations; reproducible search trail (queries, databases, dates). (2) **Critic independent adversarial
pass** — blind search first, then audit of the Executor memo + this criterion + the F14 reconciliation
(`critic_instructions_whitespace-pr15.md`) → reports to Lucas.

**Snapshot date:** 2026-06 (the claim is dated "as of mid-2026").

**Disposition:** any **FATAL** → escalate to Lucas with primaries attached **before any S0.2–S0.5
authorization** (residual = methods-comparison-only; Lucas decides whether that justifies the bake-off).
Any **AMBIGUOUS** (partially-internal params; hybrid digital recurrence; unclear update locus) → escalate
with primaries; **never adjudicated in-pipeline**. **Clean → PASS is one-sided** (a found prior kills; a
clean search does *not* certify): the gate is satisfied for S0.2 authorization — jointly with the
S0.7-lite envelope + **Lucas's program-level continuation call** — and the claim stays provisional until
the dated S0.8 final sweep.

## PR-10 — PROPOSED freeze values (Supervisor draft 2026-06-10; ⬜ awaiting Lucas — governs the S0.7-lite run)

**Source record:** `docs/s0_7/pr10_assumption_sources.md` (S0.7L-0 — every value primary-quoted there;
row refs below). **Conventions proposed for the freeze:**
- **Two corners, no midpoints:** the envelope runs at **OPT** (best published, device/hero class) and
  **CONS** (system-level / named vendor part). The §10 escalation clause fires on the *optimistic*
  corner failing to clear digital, so OPT must be genuinely optimistic and CONS genuinely deployable.
- **ENOB-at-speed, never nominal bits** (memo §2 rule: 12-bit parts deliver 7.7–9.0 ENOB at GHz).
- **Heater-class consistency** (memo §4): each scenario uses ONE heater class for *both* its power row
  and its τ/training-cadence row — no mixing suspended-heater power with standard-heater speed.
- **Registered exclusions at lite** (deferred to the S0.7-full F16 ledger, listed as unbudgeted in the
  lite output): laser wall-plug, active locking, control-loop digital compute, packaging/thermal.

| Category | OPT corner | CONS corner | Memo |
|---|---|---|---|
| E/O incl. driver | 0.135 pJ/bit (hybrid TX, 10 Gb/s) | 10–20 pJ/bit (monolithic measured / Miller class) | §1 (1.4, 1.5, 1.6) |
| O/E (PD+TIA) | 0.17 pJ/bit (25 Gb/s best-case) | 1.4 pJ/bit (measured 64 Gb/s; "several" survey top noted) | §1 (1.8, 1.9) |
| ADC at GS/s | ≈32 pJ/sample @ 9.4 ENOB (research ◑, corroborated by the Murmann GS/s envelope) | ≈469 pJ/sample @ 8.4 ENOB (TI ADC12DJ3200, Executor-verified) | §2 (2.9, 2.4–2.6) |
| DAC at GS/s | 5–9 pJ/sample (8b research, ~4.6 ENOB at extreme rate ◑) | ≈308 pJ/sample (TI DAC38RF82, 14-bit core) | §2 (2.10, 2.7–2.8) |
| Heater class A (foundry std) | — | P_π ≤175 mW/π (foundry bound; 60–385 measured span) + 2 mW/ch trim electronics; fast τ | §4 |
| Heater class B (suspended) | ~1 mW/π at τ = 0.4–2.6 ms (non-CORNERSTONE; couples to SPSA cadence) | — | §4 |
| Digital baselines (F16, named) | **Brainwave** (batch-1 GRU streaming, 287 GFLOPS/W, author-stated) · **coherent-DSP ASIC class** 25–170 pJ/bit (GS/s streaming-FIR anchor) · **Jetson AGX Orin** (embedded-GPU rep.) · MARCA/LightMamba cited qualitatively (relative-only) | same set (the baseline is not corner-split) | §3 |
| Operating scale | N grid **{8, 32, 128}**; line-rate class **0.1–2 GS/s**; single-carrier-one-FSR λ-plan (WDM = labelled extension); 2–4 control ch/ring; memory 329→4937 rt by platform corner (S0.1) | same | §5 + `mapping_result.md` §4 |

**Adopted discrepancy corrections (memo §6 — these legacy anchors are NOT carried):** the pnn-multilayer
"Ozkaya 20–50 mW standing power" attribution (unverifiable; verifiable record is 1.4 pJ/bit @ 64 Gb/s);
the "~5 pJ/bit at 800G DSP" figure (model-computed, no primary; sourced bracket 25–170 pJ/bit); Harris
2014 24.77 mW/π **silicon** (not SiN — excluded from SiN heater rows).

**Output convention:** energy/sample + end-to-end latency per sample at the registered scale grid,
photonic side charged the full OPT/CONS conversion stack, vs each named baseline at author-stated
perf/W; **stated limitation:** no GHz-sample-stream SSM accelerator exists in the literature, so the
closest-workload mapping convention is stated in the output, not invented post hoc. Verdict semantics
per roadmap v3.1: negative lite → escalate as Stage-1-reframing finding (does not kill Stage 0);
positive → labelled assumption-driven, not outreach-load-bearing before full S0.7.

**Freeze action for Lucas:** "freeze PR-10" (or amend rows) → status flips 🔒, S0.7-lite (S0.7L-1) runs.
