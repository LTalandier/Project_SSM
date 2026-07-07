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
>
> **Update (2026-06-10, Lucas rulings):** **PR-10 🔒 FROZEN** (S0.7-lite runs) · **PR-15 amended →
> PR-15.1, signed** (q4 task-objective + q1 riders + q3 positive definition; servo class → lineage,
> Böhm → boundary-cite, **Wu → W1 default claim, no outreach yet**). Gate state: **provisional one-sided
> PASS under PR-15.1, contingent on the Zhao / NTT / Fisher retrievals** (Lucas, in progress).
>
> **Update (2026-06-10, continuation gate):** Zhao resolved **non-fatal** (figure-level, Lucas);
> NTT/Fisher/Shi re-paced to the claim-wording freeze. S0.7-lite envelope ran on frozen PR-10 →
> conditional positive, Critic-audited (APPROVE-WITH-EDITS). **Lucas ruled GO (E-2026-06-10-3): S0.2–S0.5
> authorized.** Next freezes: **PR-1 + PR-2** (fed by S0.2-0; carry the ledger-Notes constraints incl.
> the envelope-audit carry-ins), then PR-4 at S0.3.
>
> **Update (2026-06-10, PR-1/PR-2 phase-boundary review):** Critic review filed
> (`critic_review_pr1-pr2-freeze.md`): **PR-1 APPROVE-WITH-EDITS · PR-2 AMEND** — one CRITICAL
> structural finding (PF-F1: the v1 R1-headline hybrid was end-to-end linear; re-derived floor
> SER ≈ 0.7 % at 24–32 dB, ~400× above the RC anchor it was built on; recommended fix = R2-intensity
> headline) + edits PF-F2–F9. Transcription integrity, anchor choices, partition/topology pins, and
> cross-references all verified clean. **Supervisor concurs in full; blocks revised to v2 below**
> (fix (i) + every edit applied; PR-3/PR-4/PR-6 carry-ins logged in Notes). ⬜ **awaiting Lucas
> signature** (E-2026-06-10-4).
>
> **Update (2026-06-10, freeze):** **PR-1 + PR-2 (+ PR-13, early) 🔒 FROZEN** — Lucas "ok go"
> (E-2026-06-10-4) on the Critic-reviewed v2 blocks. Gate i and the bake-off object are now fully
> governed; **S0.2-1** (in-house layer + the Gate-i runs — the project's first training runs) is
> posted to the Executor. Next freezes: **PR-4** at S0.3 (+ the PR-3 *rule* before S0.4 close).
>
> **Update (2026-06-11, Gate-i adjudication):** **PR-1.1 v2 🔒 SIGNED by Lucas** ("sign PR-1.1",
> E-2026-06-11-1) after Critic review (APPROVE-WITH-EDITS, `critic_review_g3-adjudication.md`)
> and the S0.2-1R archived record repair. **G1 PASS · G3 FAIL on record, criterion VOID for
> anchor instability (F-G3) · Gate i adjudicated purpose-served (G1 ∧ numerical-identity
> dossier) · no replacement published anchor — downstream reference = PR-3 in-house ceiling ·
> new binding freeze rule: reference-implementation transfer check before any externally-
> anchored accuracy/threshold freeze.** S0.2-1 closed. Next freeze: **PR-4** at S0.3 (behind
> the M1-vs-M3 gain-regime ruling).

> **Update (2026-06-13, S0.3 substrate freeze):** **PR-4 v2 🔒 SIGNED by Lucas** ("sign PR-4") after
> Critic AMEND (all P4-F1..F12 applied; g_rt=0.9× operating point registered). S0.3-1 substrate
> built + ACCEPTED + Critic APPROVE-WITH-EDITS; **S0.3-1b** freeze-conforming edits ACCEPTED (gain
> default → `saturating`, test_h de-hollowed, 128/128). E₀ + intracavity-reachability addenda folded
> into PR-4 §G/§N.
>
> **Update (2026-06-17, S0.4 freeze packet PROPOSED):** Lucas ruled the three open S0.4-gating
> questions — **(1) gain `saturating` for all four estimators** ("let's do the saturating");
> **(2) κ_ext clamp A** (δ-/M1-validity-aware r_min rule, co-registered with the PR-6 sweep recipe;
> D-2026-06-13-1); **(3) PR-12 = R-ii** (D-LinOSS damping a distinct trainable-net-loss knob at fixed
> g_f=0.9, with PR-12/K4/PR-6 init-consistency + r*-in-M1-validity checks). **PR-6 (fairness contract,
> CRITICAL) · PR-7 (cost metric) · PR-5 (PAT twin-mismatch; structure now, levels recon-deferred) ·
> PR-12 (R-ii disposition)** are now ⬜ **PROPOSED** (blocks at the end of this file). Next:
> **Critic phase-boundary review → Lucas signature → S0.4-0 calibration (δ-aware r_min + connected-init
> smoke + PR-5 recon) → S0.4a (PAT + SPSA on the substrate).** PR-8/PR-9/PR-11 (statistics, Gate-ii
> semantics + the M3-trigger margin, RHEL echo) freeze at S0.5; PR-3's *rule* freezes before S0.4 close.

## Ledger

| ID | Governs | Freeze before | Status | What must be registered | Source |
|----|---------|---------------|--------|-------------------------|--------|
| **PR-1** | Gate (i) | S0.2 run | 🔒 **FROZEN 2026-06-10** (Lucas "ok go", E-2026-06-10-4; Critic-reviewed v2 block below) · **amended by PR-1.1 🔒 SIGNED 2026-06-11** (G3 criterion void for anchor instability — F-G3; Gate i adjudicated purpose-served: G1 PASS ∧ parity dossier) | Gate-i accuracy margin + the named published benchmark it reproduces. | roadmap S0.2 |
| **PR-2** | Bake-off setup | S0.2 | 🔒 **FROZEN 2026-06-10** (Lucas "ok go", E-2026-06-10-4; Critic-reviewed v2 block below) | The bake-off **task**; the **hybrid architecture** (what is simulated — layer/stack, encoder, head, nonlinearity); the **trainable-parameter partition** (every method trains the *same* partition); the **in-situ-trainable physical-parameter set + actuation map** (which params, by what actuator — heater detuning vs tunable coupling vs gain). Task sized against S0.1's pole/memory bound + the S0.7-lite niche (PR-10). | F2, white-space |
| **PR-3** | S0.5 target | rule before S0.4 close; **ceiling frozen at S0.4 close** | 🔒 **rule FROZEN 2026-07-07** (by delegation; block below — SER_target = 1.25×ceiling+0.005; ii-a floor = 0.5×reservoir; ceiling number → S0.4-close addendum) | The bake-off **target rule relative to the BPTT-on-substrate ceiling** ("within X% of exact-gradient accuracy at the same cell"); the **absolute task-utility floor** (ii-a). Register the *rule* (X%) first; measure + freeze the ceiling once at S0.4 close; then run. | F2.3, F10.2 |
| **PR-4** | Substrate + Gate ii | S0.3 build / S0.5 gate | 🔒 **SIGNED v2 2026-06-13** (Lucas, "sign PR-4"; block below; Critic review 2026-06-12 verdict **AMEND** — all P4-F1..F12 applied; Cui body confirmed [EV] via independent commentary 2026-06-13, risk (i) closed; E₀ numeric = registered S0.3-1 calibration addendum) | Self-consistent operating **(α, Q_i) pair** (derive one from the other; add a loss↔Q registry check); the **κ_ext policy** (fixed regime or trainable bounds); the named **"realistic SiN noise" cell** (Q/α, NF, ASE level). **Foundry-grade gates Gate ii; class-leading is a labelled aspirational sweep axis.** Resolves D-2026-06-08-1. | F13, F10.5 |
| **PR-5** | PAT (S0.4a) | S0.4a | 🔒 **SIGNED v2 structure 2026-07-07** (by delegation, packet-v3 — block below; numeric levels frozen in the S0.4a spec at `0b8c817` from the S0.4-0 recon) | PAT **twin-mismatch families + levels** (parametric calibration error at realistic characterization accuracy + structural omission); **calibration-error unification** — offline-deploy baseline's weight-mapping error drawn from the *same* family. Headline cell = the registered mismatch level; report PAT as a function of it. | F7.2–3 (CRITICAL) |
| **PR-6** | All estimators (S0.4) | S0.4a | 🔒 **SIGNED v3 2026-07-07** (by delegation, E-2026-07-05-1; block below + S0.4-0 calibration addendum) | The **fairness contract**: physical-operations invariant (gradients only from simulated device passes on the shared substrate w/ fresh noise; autodiff-through-substrate reserved for the BPTT reference); common θ₀ + data ordering per seed; **equal pre-registered HP budgets** per method; **equal max-device-pass budget B** per cell. | F7 (CRITICAL) |
| **PR-7** | Cost metric (S0.4/S0.5) | S0.4 | 🔒 **SIGNED v2 2026-07-07** (by delegation, packet-v3; block below) · **PR-7.1 amendment 2026-07-07** (RHEL row) | Cost **unit = physical device passes, any direction** (per-method table: SPSA 2 fwd; PAT 1 fwd + digital twin-backward on a side-ledger; adjoint 1 fwd + 1 adjoint device pass; RHEL ~~1 fwd + 1 echo~~ **PR-7.1: 1 fwd + 2 echo = 3**); batch convention; **digital-compute side-ledger** reported alongside. | F5 |
| **PR-8** | S0.5 analysis | S0.5 | 🔒 **FROZEN 2026-07-07** (by delegation; block below — 8 seeds, censoring-at-B lexicographic rank, paired bootstrap, digital ledger co-reported-not-ranked, equal registered HPs) | Statistical plan: **right-censoring** treatment (fraction-reaching-target within B + median/IQR among reachers / survival treatment); lexicographic ranking (success-fraction, then median passes); paired-by-seed bootstrap CIs; **≥8 seeds for all methods in headline cells** (4 only for exploratory grid). | F11 |
| **PR-9** | Gate ii + promotion | S0.5 | 🔒 **FROZEN 2026-07-07** (by delegation; block below — ii-b ≥5/8; promotion = ≥25 % + CI-excludes-0 or simpler-F8-at-non-inferior; R3b readout-differential rule; M3 = Δ_M3) | **Gate-ii semantics** decomposed: (ii-a) capacity — BPTT ceiling clears the utility floor; (ii-b) trainability — **PAT or SPSA** within margin of ceiling (only-adjoint/RHEL-pass → escalate-and-redesign, *not* a pass). **Promotion criteria**: "clearly beats" quantified (e.g. ≥X% better pass-to-target w/ non-overlapping 95% CIs, or strictly-better scaling, or strictly-simpler hardware ledger at non-inferior efficiency); **"exactness" struck** from the menu (outcome metrics + F8 hardware ledger only). | F10 |
| **PR-10** | S0.7-lite | before S0.2 task reg | 🔒 **FROZEN 2026-06-10** (Lucas "ok"; values in the block below) | S0.7-lite **assumptions**: conversion energies, DAC/ADC rates, named **digital-baseline class + sources**, operating scale (N rings, rates). Labelled assumption-driven; not load-bearing in outreach before full S0.7. | F1, F16 |
| **PR-11** | RHEL echo (S0.4c) | S0.4c | ⬜ **PROPOSED 2026-07-07** (block below; recon `docs/s0_4/pr11_echo_submodel_recon.md`) | RHEL echo **invariants**: independent forward/echo ASE streams (no common-RNG reversal); no loss-sign flip (echo through the *same* dissipative substrate); gain injects fresh ASE in the echo too. **Conjugation-fidelity bound** + the **unit test** (echo of a noisy forward must *not* recover the noiseless state; bounded by fidelity × ASE floor). | F9 |
| **PR-12** | Damping cell | after S0.3 coarse sweep, before S0.5 grid | 🔒 **SIGNED disposition v2 (R-ii) 2026-07-07** (by delegation, packet-v3; block below) — D-LinOSS damping = trainable per-ring net loss (κ_ext over the §C clamped box) at fixed g_f=0.9, **not** a g_f sweep; PR-12 collapses into PR-6 §C/§D + a convergence-controlled BPTT diagnostic rerun. | The **central damping operating cell** for the bake-off, from the F3 coarse BPTT-on-substrate sweep; the sweep is over the physical damping **floor** + init/range, not a fixed value. | F3 |
| **PR-13** | S0.5 secondary task | S0.5 | 🔒 **FROZEN 2026-06-10** (early, jointly with PR-2 — Lucas E-2026-06-10-4; task-family detail in the PR-2 v2 block) | A **synthetic memory-task family** with tunable memory length (delayed recall / sticky detection at parametric lag) as a pre-registered secondary; stress-tests ranking robustness + the memory-vs-Q story. | F20 |
| **PR-14** | Secondary diagnostic | S0.5 | ⬜ | The secondary diagnostic = **bias/variance decomposition of the gradient estimate vs the BPTT reference** (mean error-vector norm + variance), **not raw cosine**; confined to mechanism discussion, never the headline. | F6 |
| **PR-15** | Pre-S0.2 continuation gate | the white-space search run (now) | 🔒 **FROZEN 2026-06-09** · 🔁 **AMENDED → PR-15.1, signed 2026-06-10** (v1 retained below) | White-space **existence** go/no-go (debt #1, front-loaded — D-2026-06-09-1): rule-form kill-criterion (**q1∧q2∧q3∧q4** per PR-15.1) + search lanes + two-modality protocol + disposition. **Full frozen detail + the signed amendment in the blocks below** — the table row is a pointer only. | D-09-1, F15, WS-F1/2/3/5 |

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
- **PR-2/PR-4 carry-ins from the Critic envelope audit (EV-F1/F3/F5, 2026-06-10,
  `critic_review_s07lite-envelope.md`):** *PR-2 (readout pin):* the envelope's digital-comparison
  consistency (C5 op count + C8 single conversion chain) holds **iff the readout is
  single-quadrature homodyne or intensity** — I/Q detection doubles the output chain (the boundary
  DSP cell dies; CONS×B N=32@1 GS/s vs Brainwave flips to LOSES; the deployable corner then starts
  at N=128). D-08-2's no-conjugate-pairing choice is load-bearing for the digital side too (pairing
  halves the op count to 7N and kills four deployable-corner CLEARs). *PR-4:* the envelope's
  **N=128 margins assume the class-leading-Q corner** (linewidth packing: O(10–20) informationally
  distinct poles/GHz at the foundry corner vs ~150 class-leading) — exactly the splitting-prone
  corner; adjudicate the {N=128 ⇄ class-leading-Q ⇄ splitting} coupling jointly with D-08-1.
  PR-4 should also eventually register a **holding/trim-statistics convention** (EV-F1: full-P_π
  worst case vs expected P_π/2 changes the hero-corner class-A in-window verdict).
- **Carry-ins from the Critic PR-1/PR-2 freeze review (`critic_review_pr1-pr2-freeze.md`,
  2026-06-10):** *PR-4 (PF-F8f):* register an **input-drive-power / intracavity-energy
  normalization** — the digital encoder must not be able to buy SNR against the registered
  noise cell (applies to both arms; the real F6 contamination channel, distinct from κ_ext).
  *PR-3 (PF-F3):* the absolute-floor (ii-a) cell-set must contain **≥1 foundry-feasible cell**;
  an ii-a miss at the foundry headline cell = the memory-vs-Q / Stage-1-reframing finding, not
  a bake-off failure. *PR-6 (PF-F8a/b):* honor the PR-2 v2 data-regime (streaming fresh draws)
  + init-ownership conventions. *S0.2-1 rider:* re-verify at retrieval level that the Vinckier
  anchor system is linear-cavity + photodiode-|·|² readout (the PF-F1 premise; the Critic's
  linear floor stands regardless of that sentence).
- **S0.4-packet carry-ins (2026-06-17, PR-6 PROPOSED — supersession index):** (a) PR-2 PF-F8b's
  *reference default* μ(0)=0 is **superseded by the PR-6 §B connected init** μ(0)=μ_c≈0.3κᵢ (S31-F2
  signal-starvation; PR-2 delegated the init to PR-6, so this is delegated authority exercised, not a
  PR-2 amendment; the μ(0)=0 cold-start is retained as a registered sensitivity row). (b) PR-4 §K's
  K4 [0.1,3] is the **passive/fixed-plane** bound; the **operative training band in `saturating`
  mode is PR-6 §C's [r_min,3]** (clamp A; r_min ≈ 0.15 candidate, δ-aware number measured at S0.4-0 +
  addended). (c) the M1-validity check on r* (PR-6 §C clause (b)) reads against PR-4 §G(iii).
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

## PR-10 — 🔒 FROZEN values (proposed 2026-06-10, Supervisor; **frozen 2026-06-10, Lucas "ok"** — governs the S0.7-lite run)

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

## PR-15.1 — signed amendment (Lucas, 2026-06-10; PR-15 v1 above retained per supersession discipline)

**Rule change: a prior is FATAL iff q1 ∧ q2 ∧ q3 ∧ q4** (q2 unchanged; q1/q3 clarified; q4 new).
Amendment text per `critic_review_whitespace-pr15.md` WS-F1/F2/F3/F5; Supervisor + Executor + Critic
converged independently; Lucas signed ("ok", ruling 2 of E-2026-06-09-5).

> **q4 — task-objective condition.** The update minimizes a loss defined over the system's
> **input→output behavior on a computational task** (a corpus of input–output examples, with the
> trained system evaluated on inputs beyond the tuning set). Regulation of the device's own operating
> point — setpoint/resonance locking, stabilization, alignment, regime attainment or maintenance (e.g.
> mode-locking, comb states) — does **not** satisfy q4, regardless of update rule. Controller-RL
> distinction recorded: where the policy gradient lands on a *controller network's* digital weights and
> the physical parameters are set as *actions*, the physical parameters are not the trained weights of
> the learning system.

> **q1 rider — "recurrence" defined (WS-F3):** a **weight-tied iterated map carrying state across the
> input sequence** (the parameters define poles/memory over the task's time axis). Time-multiplexed
> implementations of feedforward architectures (folded-in-time DNNs; loop processors with per-pass
> reprogrammed elements) do **not** satisfy q1, however physically recirculating the hardware is.

> **q1 physicality qualifier (WS-F2; adopted with the Böhm ruling):** the updated parameters are
> **physical (analog) degrees of freedom of a photonic recurrence, and the recurrent state is carried
> in the photonic system**. Parameters held as digital numbers inside an in-loop processor (e.g. FPGA
> coupling memory) do **not** satisfy q1 — such priors are boundary-cites, not kills.

> **q3 defined positively (WS-F5):** q3 = *forming an explicit local gradient / descent-direction
> estimate* (FD, SPSA, SPGD, dither/lock-in, extremum-seeking, MGD) *or an analytic/algorithmic
> gradient* (BP, adjoint, EP, parameter-shift, policy gradient, likelihood gradient). Enumerated
> **non-q3** (non-fatal-but-cite), in addition to v1's population-selection exclusions: Bayesian
> optimization; comparison-based direct search (Nelder-Mead, coordinate/pattern, Rosenbrock); simulated
> annealing; value-based RL (DQN class); greedy accept/reject Boolean flips (even when described in
> gradient *language*); aDFA-style fixed-projection gradient surrogates.

**Dispositions recorded with the signature (2026-06-10):**
- **Servo / regime-optimization class** (Milanizadeh 2020 CV, Jayatilleka 2015, Padmaraju 2014,
  Kaminow/PDH lineage; Pu 2023, Yan 2021, Kokhanovskiy 2024): fail q4 → **citable lineage**, named in
  the paper's prior-art boundary paragraph.
- **Böhm 2022** (Nat. Commun. 13:5847): fails the q1 physicality qualifier → **non-fatal,
  boundary-cite by name** (Lucas ruling: "ok").
- **Wu et al., eLight 5:7 (2025) — M1:** remains **AMBIGUOUS-potentially-FATAL on q1 for the W0 claim
  only** (q2/q3/q4 verified; trained set U unenumerated; WS-F9 evidence leans fatal). **Lucas ruling:
  no author outreach for now ("maybe later")** → **W1 is the adopted default claim** (*first
  continuous-time dissipative-resonator recurrence — pole positions + inter-resonator couplings —
  trained in situ by gradient-based/-estimating methods on a computational task*; verified true under
  both Wu readings by Executor + Critic independently). Wu is carried as the **loudest must-cite**; W0
  is reclaimable only on later evidence (author reply / code release / Zhao reading).
- **Gate state: provisional one-sided PASS under PR-15.1, contingent on the retrievals reading
  non-fatal** — **Zhao LPR 2025** (DOI 10.1002/lpor.202501576 — the one item that could threaten even
  W1, if its trained MRRs form a weight-tied recurrence; secondary descriptions suggest a feedforward
  weight bank, unverified), NTT ADI 2025, Fisher 1987. Final PASS is recorded when those resolve; the
  dated S0.8 final sweep + the §7 watchlist stand regardless. A clean PASS certifies nothing
  (one-sided, per v1).
- **Retrieval #1 RESOLVED (2026-06-10, Lucas — figure-level primary evidence): Zhao LPR 2025 →
  NON-FATAL.** Lucas obtained figs. 1–2 (archived: `docs/s0_L/primaries/lpor70400-fig-000{1,2}-m.jpg`);
  adjudication (Lucas, Supervisor-confirmed): the architecture is a **feedforward MLP** — fig. 2 shows
  $Z^l = W^l X^{l-1}$, $X^l=f(Z^l)$ forward and $(W^l)^T dL/dZ^l \odot f'$ backward through the same
  MRR weight bank (bidirectional optical BP); each ring is a **static weight element $W_{ij}$**, no
  state carried across the input sequence → **fails q1** (weight-tied-recurrence rider). Does not
  graze W1 (rings are weight elements, not dynamical poles/couplings). **Becomes a prominent
  must-cite** (nearest neighbor on the in-situ-MRR-training *method* axis; sharpens debt #4:
  feedforward in-situ optical BP on MRRs now exists — the *recurrent* version remains the gap).
  Residual: full-text check rides the dated S0.8 sweep (guard against an unfigured recurrent demo).
  **Remaining full-texts (NTT ADI 2025, Fisher 1987, Shi LPR 2025): claim-freeze-paced (before
  PR-2/S0.8 wording), NOT continuation-gate-blocking** — both carry documented non-fatal leans
  (NTT: digital-twin-trained → q2; FiT-DNN class → q1 rider; Fisher: 1987 LCLV, topology unresolved).

---

## PR-1 — 🔒 FROZEN v2 (proposed 2026-06-10; Critic phase-boundary review `critic_review_pr1-pr2-freeze.md` APPROVE-WITH-EDITS, edits PF-F6/F7/F8g–i/F9d applied; **frozen 2026-06-10, Lucas "ok go" — E-2026-06-10-4**)

**Governs:** the S0.2-1 Gate-i run (idealized digital model reproduces published oscillatory-SSM
accuracy). Sources: `docs/s0_2/debt2_benchmark_recon.md` (§3–§5, [EV]-verified) — cited per row.

- **Anchors (two; Gate i passes iff BOTH pass):**
  - **G1 — Heartbeat, LinOSS-IM:** published 75.8 ± 3.7 % (recon §3 [EV]); config lr 1e-3 /
    hidden 16 / state 16 / blocks 6 / time T, 10,936 params (recon §4 [EV]). Criterion:
    **mean test accuracy ≥ 72.1 %** (published mean − 1σ).
  - **G3 — EigenWorms, LinOSS-IM:** published 95.0 ± 4.4 % (recon §3 [EV]); config lr 1e-3 /
    hidden 128 / state 64 / blocks 2 / time T, 134,279 params (recon §4 [EV]). Criterion:
    **mean test accuracy ≥ 90.6 %** (published mean − 1σ; implies clearing the best
    non-oscillatory competitor, LRU 87.8 %).
  - **Margin calibration (registered reading — PF-F9d):** −1σ on a 5-seed mean = a 2.24-SE
    one-sided allowance; false-kill ≈ 1.3 % per anchor, ≈ 2.5 % joint (Critic re-derivation).
    Calibrated to catch gross breaks, not ≤1σ systematic offsets — the bake-off's operative
    reference is the PR-3 in-house ceiling, not the published number.
- **Protocol:** exactly the published Walker protocol — the 5 fixed seeds {2345, 3456, 4567,
  5678, 6789} setting the 70/15/15 splits; mean over the 5 runs is the gated statistic,
  **compared against the thresholds unrounded** (PF-F8h). **Split reproduction pinned
  (PF-F6):** the five seeds must reproduce the published split assignment (port the split
  routine or extract split indices from the official repo); if exact split reproduction is
  infeasible in the chosen framework, declare via `decisions_needed.md` *before* the gated
  runs. **Non-gating annex:** +3 additional seeds **{7890, 8901, 9012}** (PF-F8g) reported for
  robustness (not part of the criterion).
- **Reference behavior = the official code, not the paper text** (recon §4.3 discrepancy):
  learnable per-dimension Δt (sigmoid), ReLU-parametrized diagonal A, IM discretization, the
  published multi-block stack (BatchNorm → SSM → GELU → dropout → GLU → skip; mean-pool head).
  **Closure rule (PF-F8i):** any protocol detail not stated here resolves to the official
  repo's behavior; **no hyperparameter tuning is permitted for the gated runs.**
- **Implementation under test = the in-house layer** (the one the bake-off uses downstream, run
  at μ=0), validated against the anchors; the official MIT JAX repo is a debugging cross-check
  only. Framework/runtime choice = S0.2-1 Executor within house hygiene (exceptions via
  `decisions_needed.md`).
- **Scope of Gate i (registered — PF-F7):** Gate i validates the stack under the published
  LinOSS-IM discretization (learnable Δt); the bake-off substrate runs exact-ZOH/CMT with
  dt ≡ 1/f_s — that delta is bridged by the PR-3 BPTT-on-substrate ceiling, not by Gate i.
- **Excluded anchors + reasons (registered):** G2 MotorImagery (tight-σ target anchors on
  D-LinOSS = preprint-only at snapshot; the LinOSS-IM alternative has σ = 7.5); G4 PPG-DaLiA
  (compute-flagged stretch; not needed for Gate-i purpose); Weather (no σ/seeds/code —
  irreproducible at pre-registration grade); EthanolConcentration (spectral, near-chance).

## PR-2 — 🔒 FROZEN v2 (proposed 2026-06-10; Critic phase-boundary review `critic_review_pr1-pr2-freeze.md` AMEND → fix (i) adopted: **R2-intensity headline readout** (PF-F1 CRITICAL) + PF-F2/F3/F4/F5/F8a–f/F9a–c applied; **frozen 2026-06-10, Lucas "ok go" — E-2026-06-10-4**) — jointly freezes PR-13

**Governs:** the bake-off setup (S0.2-1 → S0.5). Sources: `docs/s0_2/bakeoff_task_candidates.md`
(generator [EV]-quoted), `mapping_result.md`, `B1_actuation_map.md`, ledger Notes (D-08-2/D-08-3
constraints + EV-F1/F3/F5 carry-ins), PR-10 frozen grid, PR-15.1 W1.

- **Headline task — T-A, Jaeger–Haas nonlinear channel equalization:** 4-PAM i.i.d. d(n) ∈
  {−3,−1,1,3}; the verbatim 10-tap ISI polynomial + memoryless nonlinearity
  u(n) = q(n) + 0.036 q²(n) − 0.011 q³(n) + AWGN (candidates memo §2.T-A, [EV] from
  arXiv:1501.03024); **target = d(n−2)** (canonical 2-delay convention — the Vinckier prose
  ambiguity is resolved by freezing this). **Invariant pin (PF-F9c):** with the verbatim
  (centered) generator, the output at time n estimates d(n−2); implementations must not
  re-shift the polynomial to causal form while keeping the target index (that combination is a
  different, harder task — decision delay 0). Metric **SER** (NMSE secondary); held-out test
  **10⁵ symbols/seed at the 28/32 dB cells, 10⁴ at 16/24 dB** (PF-F5: anchor-class SER
  10⁻⁴–10⁻⁵ must be resolvable; cost trivial for a linear-time simulation). **Registered SNR
  grid {16, 24, 28, 32} dB, headline cell 28 dB** (the RC-anchored point: Vinckier SER→0 at
  28/32 dB with 50 nodes); **train and test at the same registered SNR per cell** (PF-F8d).
  **Clock: headline 2 GS/s** (dominant 7-tap span vs foundry memory 6.58 samples = ◑, honestly
  memory-limited — the ceiling-relative PR-3 *ranking* rule absorbs this for the method
  comparison; **Gate ii-a's *absolute* floor does not inherit that absorption** (PF-F3): PR-3
  must register the floor on a cell-set containing ≥1 foundry-feasible cell (e.g. T-C k≤3, or
  T-A at the class-leading corner), and an ii-a miss at the foundry headline cell is recorded
  as the memory-vs-Q / Stage-1-reframing finding (roadmap v3.1 semantics), not as a bake-off
  failure; class-leading fits fully); 1 GS/s = reported sweep cell (foundry-infeasible at
  3.29 samples — stated, kept for the memory story). **Honesty line (binding for S0.8 wording —
  PF-F2):** the photonic-hardware record on this exact channel is ~0.1–0.9 MS/s (Paquot 2012;
  Vinckier 2015); the GS/s clock sizes the *simulated* niche only and is not a
  hardware-demonstrated rate claim.
- **Secondary task family (= the PR-13 registration, frozen early in this act):** 4-ary i.i.d.
  input; **lag grid k ∈ {1, 3, 10, 30, 100}** at 1 GS/s (+ a 2 GS/s cell at k=100). Two arms:
  **(a) delayed recall** — target u(n−k), metric NMSE. **(b) sticky detection** — binary target
  1 iff a marker occurred within the last k samples, the marker drawn as a separate registered
  rare-event stream with per-cell **P(marker) = 1 − 2^(−1/k)** (class-balanced at every k by
  construction — PF-F4: the v1 4-ary-value variant is degenerate at k ≥ 10, P(1) → 94.4 %/
  99.98 %/≈100 % at k = 10/30/100); mechanical realization: the marker is a fifth registered
  input level (+5 on the {−3,−1,1,3} scale) substituted i.i.d. at the marker times; metric =
  **balanced accuracy**. **Memory-cliff cells = registered *hypothesis*, not a hard wall
  (PF-F9b):** k=100 already exceeds the 1 GS/s class-leading 1/e yardstick (100 > 49.4); the
  2 GS/s cell is the *marginal* cliff (100 > 98.8, amplitude retention e^(−100/98.8) ≈ 0.36);
  noiseless linear memory capacity scales with N, so the cliff outcome is interpreted jointly
  with the PR-4 noise cell. Tap-span generalization of T-A = optional tertiary, not frozen.
- **Hybrid architecture (the bake-off object, distinct from PR-1's digital stack):** digital
  affine encoder → **one** photonic ring-bank recurrence layer — complex-diagonal (S4D/DSS)
  poles + trainable nearest-neighbor couplings μ, **no conjugate pairing** (D-08-2 + audit
  carry-in) — → readout **R2 = direct-detection intensity** y(n) = |Σ_j c_j a_j(n)|² (single
  chain, EV-F5-consistent; the |·|² is the hybrid's only physical nonlinearity and the
  RC-anchor-native readout class — the ring states are time-mixtures of the input, so |·|²
  supplies the cross-lag quadratic features channel inversion needs) → digital linear head over
  the registered tap window **{y(n−m), m = 0…7}**. **R1 (single-quadrature homodyne,
  real-linear — the LinOSS-equivalent-head cell) = registered alternative sweep cell**; an
  end-to-end-linear hybrid floors at SER ≈ 0.7 % on this channel at 24–32 dB (Critic
  re-derivation, **PF-F1 CRITICAL** — the v1 R1-headline was ~400× above the RC anchor by
  construction), so R1 cells are reported against the linear-class ceiling, never against the
  RC anchor. **R3 (I/Q) excluded** — envelope-inconsistent (EV-F5; choosing it would re-open
  audited envelope cells). *(R2-headline consistency, Critic-checked: one O/E + one ADC — C8
  holds; no LO needed, removing one §7 unbudgeted exclusion; digital-equivalent op count rises
  ~14N → ~18N, a favorable-direction delta re-opening no audited envelope cell. Cost: departs
  the LinOSS-equivalent head, so benchmark transfer leans on the PR-3 in-house ceiling — the
  cost D-08-2 already accepted for μ≠0.)*
  **N grid {8, 32, 128}** (PR-10), **headline N=32** (niche + the 50-node RC anchor); every
  N=128 cell carries the EV-F3 class-leading-corner caveat.
- **Registered run conventions (F12 completeness — PF-F8):** *(a) data regime:* bake-off
  training data = **streaming fresh i.i.d. draws per iteration** (no fixed corpus); per-seed
  generator streams common across methods (→ PR-6) — streaming-vs-corpus changes what
  sample-efficiency *means* and cannot be an implementation choice. *(b) init ownership:* B1
  init distributions (δ, κ_ext, μ at θ₀) are registered at PR-6 with the common-θ₀ convention;
  reference default = D-LinOSS radial-band init mapped through B1 ranges, **μ(0) = 0**.
  *(c) hybrid timestep:* **no learnable Δt** — dt ≡ 1/f_s; pole-placement freedom is carried
  entirely by (δ_j, κ_ext,j) within B1/B3 ranges (a digitally-learnable per-ring dt would be
  unphysical).
- **Trainable-parameter partition (the SAME set for every estimator — PR-6): P2, gain-free
  minimal B1 = {δ_j (heaters), κ_ext,j (tunable couplers), μ_jk (ring–ring couplers)}** — all
  thermo-optic, ≈3 ch/ring (inside the frozen PR-10 2–4 bracket), actuation per the B1 map.
  **W1 cross-check ✓:** trains pole positions on both axes (Re via κ_ext, Im via δ) AND
  inter-resonator couplings. Digital-side params (encoder, B/C residues, head) trained
  digitally; **the claim attaches only to the in-situ-trained recurrent set.** P1 (gain-rich)
  = labelled Stage-2 extension, not frozen (4–5 ch/ring sits at/above the PR-10 bracket —
  PF-F9a; the load-bearing exclusion ground is Stage-2 gain); P3 excluded
  (surrenders trained damping — the D-LinOSS evidence axis — and strains the W1 "pole
  positions" wording); P4 excluded (fails W1).
- **F6 κ_ext dual-role policy = option (a):** κ_ext trainable within the registered B3 bounds;
  **the reservoir baseline holds κ_ext frozen at the common θ₀ ≡ the PR-4 policy value**
  (one value, reconciling the v1 "at init"/"at policy value" double reading — PF-F8e; the
  baseline must never gain recurrence-shaping through the readout knob — keeps the §5.3
  contrast clean). The real contamination channel is input power: → the PR-4 carry-in
  (PF-F8f, ledger Notes).
- **Coupling topology:** photonic-molecule **nearest-neighbor chain** (fixed sparsity mask,
  trainable strengths, N−1 couplers — deployable-corner-consistent with the PR-10 bracket);
  bus-mediated mesh = labelled sweep extension only.
- **Reservoir baseline (§5.3 contrast):** B1 frozen at the common θ₀; B/C residues + ridge head
  trained (readout-only) — the in-data falsifier of "training the recurrence matters." **Under
  R2 the baseline is Vinckier-class** — linear fixed dynamics + quadratic readout + trained
  linear weights — so the §5.3 contrast lands on the RC field's own configuration (PF-F1).
- **T-B (IM-DD PAM-4 at 1–2 GBd):** labelled non-frozen extension (niche-native demo for
  S0.7-full/Stage-1; generator port deferred — not in the salvage manifest).

## PR-1.1 — 🔒 **SIGNED amendment v2** (Lucas, 2026-06-11: "sign PR-1.1" — E-2026-06-11-1. Supervisor draft 2026-06-11, revised same day per Critic review `critic_review_g3-adjudication.md` — verdict **APPROVE-WITH-EDITS, "sign with these edits"**; GA-F1(b) demotion applied + GA-F1(a) regeneration **landed & archived** (S0.2-1R, Supervisor-verified from trails); GA-F2/F3/F5/F6/F7 applied; PR-1 v2 above retained per supersession discipline)

**Triggered by the measured Gate-i outcome** (results_log S0.2-1 addenda; adjudication item
D-2026-06-11-1) — filed *after* the runs, so it is held to the amendment standard: Critic
review + Lucas signature, with the measured record permanent and unamended.

**The measured record (stands forever, no reinterpretation):**
- **G1 Heartbeat: PASS** — unrounded gated mean 72.9032 % ≥ 72.1.
- **G3 EigenWorms: FAIL as measured** — unrounded gated mean 71.1111 % < 90.6 (per-seed
  19.44 / 88.89 / 94.44 / 97.22 / 55.56; two of five seeds in the absorbing state below).
- **Joint Gate i under the frozen letter: FAIL.** Zero tuning; zero gated reruns; the
  closure rule held throughout (Supervisor-verified).

**Finding F-G3 — the G3 anchor does not transfer (evidence: `results/s0_2/gate_i/` +
`xcheck_official/`; Supervisor re-derived the statistics independently):**
1. The **official implementation, faithfully rerun** (pinned commit 05a8353, reference-venv
   pins, official data pickles, the official runner, same GPU; per-seed trails archived and
   Critic-verified from raw) on the 5 published Walker seeds scores **90.56 % — at/below the
   frozen gate within one test-sample's granularity** (163 vs the required 164/180), on a
   2026 stack (jax 0.4.28, Ampere, default matmul precision), with **per-seed σ = 9.34 pp ≈
   2.1× the published 4.4** (seeds at 77.78 and 83.33, verified from archived trails).
   **The criterion's transfer premise fails on dispersion and environment-sensitivity, not on
   a 0.04-pp technicality** (GA-F2).
2. **Mechanism:** the official objective −Σ y·log(softmax + 1e-8) has a **zero-gradient
   absorbing state in fp32** (softmax saturation → p_true underflows to exactly 0 → total
   gradient exactly 0.0 permanently); step-instrumented, bit-deterministically reproduced —
   an **optimization collapse of the published objective**, entered at training steps 1–7
   (not an init pathology; GA-F3iii). Critic re-derived both saturation directions to
   exactly-zero gradient and bounded the escape paths (GA checklist 1: CONFIRMED).
3. **Incidence (all citable figures archived — S0.2-1R; reported per-environment, since
   incidence is stream- and environment-dependent):** ours, gated GPU run: **2/5** (2345@1,
   6789@4; the stop-at-exactly-12k trap signature is visible in the archived gated jsonls) ·
   ours, annex local-CPU regeneration: **2/3** (8901 absorbed from step 1; 9012 from step 555
   — the first observed *late* entry, one dropout-borne transient at 554; 7890 alive;
   per-step gradient ≡ 0.0 archived) · official code, fresh-8 local-CPU regeneration
   (pre-declared seed list, pinned venv, zero source edits): **0/8 strict-trap, 1/8
   behaviorally collapsed** (22222 chance-frozen on val AND train across all 4 evals —
   saturated basin with residual gradient). The rented-box console observations
   (official-fresh 2/8; ours-annex 7890@7/8901@1/9012-alive) are **superseded by these
   archived local estimates** (GA-F1) and remain indicative only. Relative to that console
   record, **the same seed's trap status flips with environment in both stacks** (ours 7890
   CUDA-trap→CPU-alive and 9012 CUDA-alive→CPU-trap; official 22222 console-strict→locally
   behavioral-only) — incidence is itself environment-contingent, which *is* the instability
   claim. **Equivalence across stacks is neither claimed nor needed: any material incidence
   voids the criterion** (small-n throughout — ~9 % power at these sizes; at incidence as
   low as 0.1, P(≥1 trap in a fresh 5-seed gate) = 41 %). The published 95.0 ± 4.4 **is
   consistent with** a favorable draw from a collapse mode with material incidence (GA-F3);
   the void ruling rests on the dispersion leg (bullet 1) and the mechanism (bullet 2), not
   on any particular k/n.
4. **The port is exonerated on independent evidence:** float32-exact cross-framework parity
   (2.4–2.7×10⁻⁷ full-model, both anchors, incl. full L=17,984; 1.2–1.5×10⁻⁷ on the GPU),
   line-by-line init-distribution audit vs the official source (BN scale/bias init-trivial;
   state arrays excluded from trainables, covered by the param-count reconciliation),
   healthy-seed mean 93.52 % inside the published band — **all on record before the G3 runs**
   (the cross-check harness was pre-specified in the task spec; nothing post-hoc).

**Amendment (re-registration; Lucas-only):**
- **The G3 criterion is declared VOID for anchor instability.** Its premise — "published
  mean − 1σ transfers to a faithful rerun" (PF-F9d) — is empirically false at this anchor:
  the faithful rerun lands at the threshold's edge with 2.1× the published dispersion on the
  published seeds themselves, in an environment-sensitive way, and the gated statistic is
  exposed to a material-incidence optimization collapse. As frozen, the criterion is a
  lottery on seed-stream draw in either direction; it no longer measures implementation
  fidelity, which is the only thing Gate i exists to measure.
- **No replacement published anchor is registered.** (i) The S0.2-0 alternates re-open
  registered exclusions (MotorImagery anchors on a preprint — the G2 exclusion ground);
  (ii) any replacement carries exactly the untested-transferability risk that just fired;
  (iii) the registered downstream reference was never the published numbers — it is the
  in-house BPTT-on-substrate ceiling (PR-3; stated at the freeze in PF-F9d and in the
  D-08-2 constraint).
- **Gate i is ADJUDICATED on the surviving pre-specified evidence** (GA-F5 wording): G1 PASS
  (gated, frozen, untouched) ∧ the numerical-identity dossier (cross-framework parity
  ≤ 3×10⁻⁷ on full-model outputs for both anchor configs, transplanted weights, train +
  inference modes — **on record before the G3 runs**, from the pre-specified cross-check
  harness). **No new accuracy criterion is registered — none is needed: the registered
  downstream reference is PR-3.** The gate's registered purpose — "idealized model reproduces
  published oscillatory-SSM behavior", i.e. validate the in-house implementation — is
  **SERVED**: the layer provably *computes the reference model* to float32 precision,
  categorically stronger evidence than any accuracy reproduction. The letter-FAIL of the
  frozen v2 criterion remains on record beside it. Downstream (S0.3+) proceeds on the PR-3
  anchoring path as registered. **This amendment changes no downstream behavior** — no task,
  threshold, or budget consumed by S0.3+ depends on G3; its only effects are the permanent
  record and S0.8 wording (Critic-verified, GA §1.6).
- **Binding for S0.8 / the paper:** the G3 outcome is reported as a *finding*, not buried —
  LinOSS-IM EigenWorms 95.0 ± 4.4 does not transfer under a faithful rerun of its own
  implementation (**90.56 %**, σ = 9.34 ≈ 2.1× published, environment-qualified; plus a
  material-incidence fp32 **optimization** collapse of the published objective); first-hand
  motivation for the PR-3 in-house-ceiling anchoring philosophy. Every citable F-G3 number
  must be archived (GA-F1) and environment-qualified (GA-F2). Optional upstream courtesy
  report to the LinOSS authors = outreach, Lucas-paced, not before the S0.8 wording freeze.
- **Annex-3 EigenWorms: cancelled** (non-gating by construction, PF-F8g; anchors nothing
  under this amendment; G1's annex is complete and stands).
- **Process carry-in (binding on future freezes):** any externally-anchored
  **accuracy/threshold** freeze must include a **reference-implementation transfer check** —
  rerun the official code at the smallest scale that exercises the gating statistic — *before*
  the threshold freezes (cost here would have been ~$1/hours and would have caught F-G3
  pre-freeze). Scope per GA-F6: PR-4-class physics freezes have no reference implementation —
  out of scope; if the check is infeasible at proportionate cost, that infeasibility is itself
  registered as anchor risk at the freeze.

---

## PR-4 — 🔒 **SIGNED v2** (Lucas, 2026-06-13: "sign PR-4")

> **🔒 FROZEN 2026-06-13 by Lucas.** The S0.3 substrate freeze is complete. Signed after the
> Critic phase-boundary review (verdict **AMEND**, `shared/critic_review_pr4-freeze.md`,
> 2026-06-12) with all twelve findings P4-F1..F12 applied in v2, and after the Cui anchor
> body-level numbers were confirmed [EV] (2026-06-13) via the independent peer-reviewed
> commentary (C-2 verification status; residual risk (i) closed). Amendments to this entry
> are Lucas-only henceforth (supersession discipline). The **E₀ numeric value** and the
> **saturated reachability solve** are the one registered deferral: mechanically evaluated at
> S0.3-1 calibration from the frozen in-block formula and reported here as a one-line addendum
> **before any run a PR-5–9 gate or bake-off statistic consumes** (O2 / G).
>
> Provenance of the v2 revision (Supervisor 2026-06-13 per the Critic review; v1 text
> preserved at commit 713efd4; fork ruling **E-2026-06-11-2** applied — M1 + M3 trigger +
> riders R1/R2/R3; evidence base `docs/s0_3/substrate_recon.md` (R§n) +
> `docs/s0_3/pr4_input_sheet.md`).

> **📌 CALIBRATION ADDENDUM (S0.3-1, 2026-06-13 — the registered §N/§G deferral, discharged).**
> Mechanical evaluation of the frozen E₀ formula and the saturated reachability solve at θ₀
> (r=0.3), P̄₀ = 1 mW, g_rt = 0.9×κᵢ — **sets no values; reproduces the closed form to ~1e-15**
> (unit test e). Source: `photonic_ssm.substrate.calibration` →
> `results/s0_3/e0_reachability_addendum.{md,json}` (Executor; Supervisor-verified, C-2
> hand-checked: 2·κ_ext,θ₀·(P̄₀/ħω₀)/κ_net² = 1.07e8 ✓).
> **Numeric E₀ (frozen for all S0.3-1+ runs):** C-1 = **3.14×10⁷**, C-2 = **1.07×10⁸**,
> C-3 = **4.72×10⁸** photons (C-2-derate 5.34×10⁷; P-CORN 7.06×10⁵). κ_net @ θ₀: C-1 2.13×10⁸,
> C-2 6.25×10⁷ rad/s. Build-up ×262 and bus saturation depth ×31.6 @ C-2/θ₀ reproduce §G.
> **Saturated reachability (honest; corrected per Critic S31-F3 to the operative plane).** Two
> planes: the gain model **saturates on the intracavity plane** (P4-F2's registered plane — "the
> field the gain medium sees"), where the build-up makes P_circ/P_sat ≈ ×8.3e3 (C-2). On the
> **bus** plane the required small-signal g₀ to hit 0.9×κᵢ is C-1 5.04 / C-2 1.50 / C-3 0.36
> dB/cm (vs Er 1.0–1.9) ⇒ C-1 material-aspirational, C-2 reachable iff Er ≥ 1.5, C-3 ✓. **But on
> the operative (intracavity) plane** the requirement is g₀ ≈ C-2 **380** / C-3 **403** dB/cm
> (= g_op·(1+P_circ/P_sat); in the JSON as `g0_required_intracavity`) — **so against demonstrated
> Er (≤1.9 dB/cm) every gain-bearing cell, C-2 and C-3 included, is material-aspirational.** The
> bus number is a floor, not the operative requirement; the source table's "✅" for C-2/C-3 is on
> the bus plane only. **Net honest status: the M1 gain operating point is a model aspiration not
> supplied by demonstrated Er on the plane the model saturates on — Stage-1 integration risk,
> strengthening anchor-risk (v) across all gain cells** (does not affect the substrate's runtime:
> g₀ is set to deliver 0.9×κᵢ as a model; reachability is a physical-Er label, not a parameter).

**v2 revision log (Critic findings → changes):** P4-F1 HIGH → per-cell operating gain
**registered** (G, new bullet) + every consequence number recomputed at it (C/S, passive floor
in parentheses) + C-1 marginality sentence reconciled. P4-F2 HIGH → P̄/P_sat reference plane
registered (intracavity), P_sat ring-scaling formula written, headroom rows demoted to
small-signal statements, reachability solve registered at S0.3-1 calibration. P4-F3 → C-1
splitting 1.9 corrected to **2.33** (kernel-reproduced). P4-F4 → Cui geometry corrected
(64-GHz-FSR racetrack, mode/width is the residual risk) + **C-2 ×2-loss derate row**
registered. P4-F5 → four-routes infeasibility superseded; **body-level numbers since
confirmed [EV] 2026-06-13** via an independent peer-reviewed commentary reproducing Cui's
figures (Ye & Marpaung, Adv. Photon. 5(5) 050503, archived `docs/s0_3/refs/`) — residual
risk (i) closed. P4-F6 → E₀ closed form written in-block, inputs
pinned, encoder-scale cadence registered. P4-F7 → anchor-risk items (v)/(vi) added; C-2 γ
lineage basis stated. P4-F8 → clock qualifiers + N-assignment semantics registered. P4-F9 →
M2 validation gains a C-1 episode. P4-F10 → F8-carry-in owners named. P4-F11 →
`loss_q_consistency_error()` cited as the registered α↔Q check. P4-F12 → encoder map
explicit, P_pk scoped per task family. **No registered choice changed** (Critic: every choice
survives attack; the repairs are completeness-of-numbers).

**Registers:** the shared dissipative-substrate cell that all four estimators train through
(S0.3-1 build; Gate ii gates on it; S0.5 bake-off runs on it). One substrate model; the cells
below are registered parameter points of it. All conventions inherited from S0.1 unless
restated (amplitude rates; κᵢ = ω₀/2Qᵢ; κ_tot = κᵢ + 2κ_ext symmetric add-drop; memory =
1/κ_tot; 100-GHz-FSR ring geometry registry convention; λ = 1550 nm). The ledger row's
loss↔Q self-consistency demand is discharged by the existing **test-enforced
`loss_q_consistency_error()` registry check**, hereby cited as the registered check (P4-F11).

### G — Gain-model class: **M1, static saturated operating point** (E-2026-06-11-2 ¶1)
- **Form:** per-episode operating point g(P̄) = g₀/(1 + P̄/P_sat), fixed within the rollout.
  **Reference plane (P4-F2): P̄ and P_sat live at the same plane — the field the gain medium
  sees (intracavity).** P_sat,ring is the flagship's measured input saturation (−15 dBm class
  [EV], R§4b) mapped through the registered geometry by the formula registered here:
  I_sat = P_sat,wg/A_eff (A_eff = 1.2 µm² [EV]), applied to the ring's circulating intensity
  P_circ = Σⱼ|aⱼ|²·ħω₀/τ_rt. The operating point enters the autograd graph as a
  **differentiable function of the episode drive statistics** (house constraint 3a/3b — no
  detach). Under this intracavity reading, SPSA's ± perturbations of {δ, κ_ext, μ} are
  handled automatically by the per-episode form: a κ_ext perturbation changes the intracavity
  power the gain sees, each SPSA pass is its own episode, and the ≥ ms inter-pass cadence is
  where gain follows adiabatically (Critic item 2).
- **Gain ceiling (no-lasing bound):** g_rt ∈ [0, **0.9 × intrinsic per-rt loss**] (the S0.1
  deep-compensation convention; gain never compensates κ_ext).
- **Operating point (registered, P4-F1):** every gain-bearing cell runs at **g_rt = 0.9 ×
  intrinsic per-rt loss** (the ceiling value — the same point the registered ASE level
  n_ss ≈ 23 is computed at), giving **κ_net = 0.1·κᵢ + 2κ_ext**. **g = 0 (passive floor) and
  g = 0.5× are labelled sensitivity rows**; P-CORN is passive-only (below). All in-block
  consequence numbers are quoted at the registered operating point with the passive floor in
  parentheses; **Gate ii and the bake-off headline run at the registered operating point.**
  g₀ per cell is set by the registered saturated solve such that g(P̄ at the registered
  drive) = 0.9 × intrinsic per-rt loss — a *model* operating point; whether the Er anchor
  materially supplies that g₀ is anchor-risk item (v), not a substrate parameter.
- **Reachability (P4-F2):** the saturated operating-point solve at the registered drive
  (O2, P̄₀ = 1 mW) is computed at S0.3-1 calibration alongside E₀ and reported to this ledger
  with the **achieved required-g₀ vs the Er-anchor span, per cell**. The headroom rows below
  are **small-signal material-plausibility statements, not operating-point claims**: at
  P̄₀ = 1 mW the bus-referenced saturation depth alone is ≈ ×32 (intracavity CW-resonant
  ≈ ×260 at C-2/θ₀ passive), so C-1's small-signal span (×6.5–12) already falls short of its
  bus-referenced requirement (≈ ×33) — C-1's gain-bearing rows carry the item-(v)
  material-aspirational label unless the calibration solve lands lower. Small-signal headroom
  vs demonstrated Er:Si₃N₄ gain (1.0–1.9 dB/cm [EV], R§4f): ×6.5–12 at C-1, ×22–41 at C-2.
  P-CORN does not close even small-signal (×0.7–1.3 vs *full* intrinsic) → P-CORN is
  **passive-only** wherever it appears (sensitivity axes).
- **ASE:** convention **A2** — continuous Langevin term in the CMT ODE, ⟨F F*⟩ = 2κ_g n_sp
  δ(t−t′) (photon units), discretized by the registered integrator (composes with the S0.1
  ZOH/van-Loan exact discretization). A1 (per-rt discrete kick) is registered as the
  first-order-equivalent alternative (difference O(10⁻³) relative at per-rt gains ≤ 0.2 dB,
  R§1.2) with a **statistical-equivalence unit test** in the S0.3-1 validation set. Fresh
  draws per pass; forward and echo streams independent (PR-11 carry-in). n_sp from the NF
  axis below.
- **Drift:** cross-episode gain memory + pump/thermal drift live at *training* cadence
  (batch-to-batch, SPSA perturbation tracking) via the salvaged `drift_inject` machinery + a
  slow operating-point update — never inside the rollout (R§4b table). **Deferred with named
  owners (P4-F10):** the drift *magnitudes*, thermal self-heating at operating power, and
  pole-placement precision (S0.1 §4 F8 carry-ins) freeze at **PR-6/PR-5–9** (the bake-off
  protocol freezes) — explicit deferrals, not silent.
- **Registered validity conditions (M1 is VOID outside these):**
  (i) **within-episode stationary drive statistics** — the frozen task families satisfy this
  by construction (PR-2 T-A i.i.d. 4-PAM; PR-13 synthetic family); **bursty/packeted inputs
  void M1** (Bononi–Rusch avalanche caveat, R§4b);
  (ii) **ensemble-power stationarity (rider R3, registered assumption of M1's validity):**
  the gain operating point follows the episode-average power, and the **train/test drive-power
  statistics are pinned** (with PR-2 F12's same-SNR convention) — any protocol that lets
  train and test (or the two arms of a comparison) present different power statistics to the
  same registered cell voids the M1 reduction;
  (iii) quasi-static margin holds at the registered drive (E_sym/E_sat ≈ 5×10⁻⁶–9×10⁻⁵ at
  P̄₀ = 1 mW across the clock grid, ≥4 orders [EV]-anchored, R§4b).
- **M2 (E-2026-06-11-2 ¶2):** retained strictly as M1's **one-off validation reference** —
  the salvaged rate-equation integrator at τ = 3.4 ms, run once at C-2/θ₀ **and once at
  C-1/θ₀ (P4-F9 — Gate ii's gating cell; trivial cost)** to confirm the quasi-static
  reduction (per-episode relaxation ≤ 3 % bound, R§4b); **not a substrate-matrix member**;
  the comparisons are archived with the S0.3-1 validation set.
- **M3 (E-2026-06-11-2 ¶3): deferred branch, pre-committed trigger, named and unbuilt at $0.**
  The M3 sensitivity row is built **iff** (a) a gated S0.5/S0.6 comparison lands within a
  margin where the gain-model class could plausibly flip the verdict — **the quantitative
  form of that margin is frozen with the bake-off pre-registrations (PR-5–9/PR-11), before
  any bake-off results exist** — or (b) the Stage-2 platform assessment tilts to III-V/SOA.

### C — Operating pairs / noise cells (closes D-2026-06-08-1; rider R1 throughout)
- **NF axis (R1):** **NF-A 7.0 dB (n_sp = 2.5, measured on-platform [EV]) is the headline
  noise value at every cell.** NF ∈ {3, 5} are sensitivity values only — never in a headline
  figure; NF-C 3.0 always carries the "quantum-floor, aspirational" label.
- **C-1 — Gate-ii gating cell ("foundry floor"):** **P-FND** (Qᵢ = 2×10⁶ ⇔ α = 0.172 dB/cm,
  registry-self-consistent), NF-A 7.0, γ = 90 MHz (subtractive-low, [EV] — process-class
  assumption, stated as such). **Gate ii gates here, at 2 GS/s** (ledger rule: foundry-grade
  gates Gate ii; clock per P4-F8), at **N = 8** — in-band at θ₀ in the 2-GHz band: **29.5 at
  the registered operating point (12.9 passive floor)**. Memory at θ₀ (r = 0.3) @ 2 GS/s:
  **≈ 9.4 samples at the registered operating point (4.1 passive floor)** — at the registered
  point C-1 **covers** the T-A 7-tap span; the honestly-marginal framing applies to the
  **passive-floor row only** (4.1 < 7; priced by PR-2's binding MS/s honesty line)
  (P4-F1 reconciliation). Gate ii's target is the **PR-3 BPTT ceiling measured on this same
  cell at the same operating point**, so capacity hits both arms identically.
- **C-2 — bake-off headline cell ("demonstrated MPW-class"):** **P-AN800** (Qᵢ = 6.8×10⁶ ⇔
  α = 0.051 dB/cm), NF-A 7.0, **γ = 11.8 MHz (damascene-clean class [AV]; basis stated per
  P4-F7: the AN800 platform is the LIGENTEC-AN damascene process lineage — a process-class
  assignment, no AN800-specific γ measurement exists; favorable assumption, knob ON
  regardless, see S).** **The PR-2 frozen headline N = 32 runs here** — in-band at θ₀ in the
  2-GHz band: **100 at the registered operating point (43.9 passive floor)**; memory at θ₀
  @ 2 GS/s: **32.0 samples at the registered point (14.0 passive)** — covers the T-A 7-tap
  span at both points; small-signal gain headroom ×22–41 (plausibility statement per G).
  **Verification status (transfer-check rule, GA-F6 scope) — body confirmed [EV]
  2026-06-13:** the pair is registered as a **conservative bound** on the platform numbers of
  Cui et al., Adv. Photon. Nexus 2(4) 046007 (2023). Abstract verbatim via Semantic Scholar
  API [EV]: *"propagation loss of only 3.3 dB/m and a mean intrinsic Q of around 10.8
  million"*, *"standard multi project wafer (MPW) foundry process"* (re-verified by the
  Critic 2026-06-12). **Body-level numbers now confirmed [EV] via an independent
  peer-reviewed commentary** (P4-F5 follow-through, Supervisor 2026-06-13): Ye & Marpaung
  (Univ. Twente), *"Compact multi-mode silicon-nitride micro-ring resonator with low loss,"*
  Adv. Photon. 5(5) 050503 (2023), CC-BY
  (`docs/s0_3/refs/Ye_Marpaung_2023_AdvPhoton_5-5-050503_commentary_on_Cui_046007_CCBY.pdf`)
  — reads Cui 046007 as its explicit subject (their Ref. 4) and **reproduces Cui's
  Figs. 1–2**: propagation loss reduced **20 → 3.3 dB/m**; intrinsic linewidth **18–20 MHz →
  Qᵢ ≈ 10.8M**; a **249-resonance intrinsic-linewidth histogram spanning ≈ 13–25 MHz** (Cui
  Fig. 2a, reproduced); 3-µm multimode waveguide, modified Euler bends, **FSR 65 GHz**. **The
  registered C-2 pair** (Qᵢ = 6.8×10⁶ ⇔ intrinsic linewidth ≈ 28 MHz, α = 5.1 dB/m) is
  therefore **strictly worse than the broadest-linewidth device in the full measured
  distribution** (≈ 25 MHz ⇔ Qᵢ ≈ 7.7×10⁶, α ≈ 4.3 dB/m) — the conservative bound holds
  against the *distribution*, not merely the mean. (The "0.051 dB/cm / 6.8M" pair is *our*
  conservative registry value, never a Cui sentence; the meaningful check — does the body
  support the platform class we bound against — is satisfied.) The Cui primary PDF remains
  programmatically walled (researching.cn article pages → Aliyun 405; SPIE renders
  title-only; six attempts/two sessions); the independent-commentary PDF was directly
  retrievable and is archived. Residual anchor risks: (i) body provenance — **RESOLVED**
  (reproduced primary figures in the peer-reviewed commentary); (ii) **geometry transfer
  (P4-F4, independently corroborated)** — Cui's device is a 3-µm-wide multimode racetrack
  (perimeter ≈ 2.23 mm, FSR 65 GHz, modified Euler bends); applying its loss class to the
  single-mode, narrower-waveguide 100-GHz-FSR registry ring (L ≈ 1.43–1.54 mm) assumes the
  loss class survives the geometry change — the demonstrated number is achieved *by* the
  wide-multimode Euler-bend design, so the residual risk is mode/width geometry, **not ring
  size** (registry equivalent bend radius ≈ 228 µm ≥ Cui's ≈ 195 µm). **The commentary
  independently flags this exact risk** ("suppression of higher-order modes... challenging...
  impacting yield and reproducibility"). Priced by the registered **C-2-derate sensitivity
  row: ×2 registered loss (Qᵢ ≈ 3.4×10⁶)** — cost ≈ 0 in simulation. Carried as a label on
  C-2.
- **C-3 — aspirational axis:** **P-UHQ** (Qᵢ = 3×10⁷), NF-A headline (NF ∈ {3, 5} labelled
  sensitivity). Hosts **N = 128** — per EV-F3 the *only* true N=128 option is escape (a):
  r ≲ 1 with the splitting knob ON (the doublet is the model). Labelled aspirational
  sweep axis; never gates anything.
- **Sensitivity axes (reported, never headline):** P-CORN (passive-only per G) ·
  P-MPW-MM · **C-2 derate ×2 loss (Qᵢ ≈ 3.4×10⁶, P4-F4)** · **gain rows g ∈ {0 (passive
  floor), 0.5×} (P4-F1; 0.9× is the registered point)** · γ ∈ {0, 11.8, 90, 160 MHz} ·
  NF ∈ {3, 5, 7}.

### K — κ_ext policy: **K4, trainable within registered bounds** (forced by the frozen PR-2
P2 partition — κ_ext,j is *in* the trainable set; a fixed-κ_ext policy would contradict it)
- **Bounds:** per-ring r_j = κ_ext,j/κᵢ ∈ **[0.1, 3]** (the B3 ladder's non-degenerate span:
  drop efficiency 0.028 → 0.735; r = 10 excluded — memory < 0.5 samples @ 2 GS/s at C-1,
  pole-region edge, SNR-degenerate). **B1-consistency requirement:** the bounds must map
  into the S0.1 realizable pole region at every cell — Executor verifies with a registered
  unit test in the S0.3-1 validation set.
- **θ₀ policy value (the F6 baseline hold, one value): r₀ = 0.3** (deep side of critical).
  Chosen jointly (input sheet §6): at C-2 it is the value where the frozen N = 32 packs
  in-band AND the T-A 7-tap span is covered AND drop efficiency (0.141) is non-degenerate
  under the O2 bookkeeping. **Direction of fit (Critic reading-1 adjudication, recorded):**
  N = 32 was frozen at PR-2/PR-10 — anchored to the 50-node Vinckier RC, before any substrate
  cell existed — and C-1 cannot host it; the alternatives were break a frozen grid or
  register a demonstrated-MPW cell that hosts it, keeping Gate ii on the foundry floor.
  θ₀ = 0.3 is not a knife edge: the C-2 co-satisfaction band is wide (N = 32 packs for
  r ≤ 0.6; the 7-tap span is covered for r ≤ 1.0; drop efficiency non-degenerate from
  r ≈ 0.3), and 0.3 is an existing B3 ladder rung — design-from-frozen-constraints, made
  before any results exist. The reservoir baseline holds κ_ext ≡ r₀ = 0.3 (PR-2 v2 F6,
  frozen).
- K4's registered prerequisites: (i) F6 hygiene — frozen in PR-2 v2 ✓; (ii) the **O2
  normalization below** (the only drive convention comparison-clean under trainable κ_ext,
  input sheet §5) ✓; (iii) splitting validity across the whole bound range — structurally
  satisfied: the knob is **always ON** (S below), so there is no OFF-validity to break.

### S — Splitting/backscatter sub-parameter: **K-pol-3 — knob always ON** (closes D-2026-06-08-3)
- The 2×2 doublet machinery runs at every cell; **γ = 0 recovers the single-pole model
  exactly** (and is the γ-sensitivity floor). γ registered per cell (C-block above);
  ~×2 ring-update cost accepted — same 2×2 machinery the coupled-μ hook needs anyway.
  Rationale: under K4 the κ_ext-conditional policies (K-pol-1/2) are incoherent — trained
  κ_ext moves through their validity boundary mid-run.
- **Registered claim condition (numbers corrected per P4-F3, kernel-reproduced):** any
  single-pole-abstraction claim anywhere downstream must name the cell (process class + Q +
  r) where 2γ/κ_tot < 1; at θ₀: **C-1 2γ/κ_tot ≈ 2.33 (split), C-2 ≈ 1.04 (doublet-class)
  at the passive floor — ≈ 5.3 / 2.4 at the registered operating gain** (C-3: 4.58 / 10.5) —
  **no registered cell supports a knob-OFF single-pole claim at θ₀, passive or compensated.**
- **Rider R2 — the N-grid consequence, stated here:** with the knob always ON, EV-F3's
  escape (a) stays open, so the **PR-2 frozen N-grid {8, 32, 128} survives intact** — pinned
  as a **per-cell assignment, not a per-cell sweep (P4-F8):** N = 8 ↔ C-1 (Gate ii) ·
  N = 32 ↔ C-2 (bake-off headline) · N = 128 **only** as the C-3 knob-ON aspirational cell.
  The de facto *deployable* grid is **{8 @ C-1, 32 @ C-2}**; any headline using N = 128 must
  carry the C-3 aspirational label. **Clock qualifier (P4-F8): all in-band counts in this
  block are 2-GS/s figures; Gate ii runs at 2 GS/s.** At 1 GS/s the registered operating
  point still holds N in-band at every cell (C-1 14.8, C-2 50, C-3 222) but the **passive
  floor does not** (6.5 < 8, 22 < 32, 97 < 128); at 0.1 GS/s no cell holds N in-band.
  Registered as a property, not a defect: training may overlap or park poles out-of-band;
  the packing row is the *initialization* feasibility statement (in-band counting
  convention: intrinsic-linewidth poles per the EV-F3/R§5 packing anchor, loaded ×(1+2r) at
  the quoted r, κ_net at the registered gain) — never an out-of-band-clock claim.
  **PR-13 cross-reference at 1 GS/s, registered operating point** (the k-grid placement the
  cliff hypothesis reads against; passive floor ÷2.3): C-1 memory 4.7 samples → k ∈ {1, 3}
  in-memory, k = 10 ×2.1 over; C-2 16.0 → k ≤ 10 in, k = 30 ×1.9 over; C-3 70.6 → k ≤ 30
  in, k = 100 ×1.4 over (the cliff).

### H — Holding/trim-statistics convention (EV-F1 carry-in): **H1, full-P_π worst case**
- The substrate's standing-power side-ledger charges every heater P_π/2-class holding at max
  trim (most conservative). **H2** (expected-value, uniform trim) is computed as a labelled
  sensitivity row; **H3** (measured distribution) is named as the Stage-1 upgrade path.
  The S0.7 envelope continues to report both corners; this fixes the *substrate's* own
  convention for any standalone number.

### N — Input-drive normalization (PF-F8f): **O2, registered intracavity-energy budget**
- **Anchor:** P̄₀ = **1 mW** per-sequence mean bus power (the [EV] quasi-static worked-example
  drive, G(iii)). **Encoder map, explicit (P4-F12):** the unipolar affine map
  {0, 1, 2, 3} → {0, ⅓, ⅔, 1}·P_pk; equiprobable mean = P_pk/2. **Peak-to-average is
  task-family-scoped:** P_pk = **2·P̄₀** for the equiprobable 4-PAM T-A family;
  **≈ 2.7·P̄₀** for the PR-13 marker family (fifth level on the same map). The G(iii)
  quasi-static margin is quoted at the worst registered family peak — it holds (≥ ~4 orders).
- **E₀ definition (the frozen formula, written here per P4-F6):** E₀ ≡ the steady-state
  intracavity photon number Σⱼ⟨|aⱼ|²⟩ established by a stationary P̄₀ drive at **C-2, θ₀,
  on-resonance (δ ≡ 0)**, under these pinned inputs: **CW-equivalent stationarity reading**
  (the formula uses the per-sequence mean power P̄₀, not the at-clock modulated PSD — the PSD
  reading differs by the build-up factor and is a labelled sensitivity only); **calibration
  injection on the bus port of ring 1 only** (chain head; input-output normalization
  |s_in|² = P̄₀/ħω₀ photon flux); **μ = μ(0) = 0** (rings 2..N dark at the calibration
  point); the cell's registered N. Closed form:
  **E₀ = 2κ_ext,θ₀ · (P̄₀/ħω₀) / κ_net²** , κ_net = 0.1·κᵢ + 2κ_ext at the registered
  operating gain (the passive-floor row uses κ_tot). No free parameter remains. The
  **numeric value** is a mechanical evaluation of this formula, computed at S0.3-1
  calibration (alongside the G reachability solve), reported to this ledger as a one-line
  addendum **before any run that a PR-5–9 gate or bake-off statistic consumes**, and frozen
  there. Every arm (SSM and reservoir baseline) and every κ_ext policy point derives its
  encoder scale to hit the same E₀ — **the encoder cannot buy SNR in either arm** (the F6
  contamination channel closed under K4; the natural partner of the corner-independent
  n_ss ≈ 23 ASE photons, R§1.3). **Encoder-scale cadence (P4-F6):** the encoder scale is
  derived **once per arm at the registered θ₀ and frozen for the run**; trained κ_ext
  excursions thereafter change intracavity energy **as physics, not as renormalization** —
  the only reading under which "the encoder cannot buy SNR" and "the task input is fixed"
  are simultaneously true.
- **Registered unit test:** E(E₀-normalized drive) = E₀ within tolerance, per cell × per
  κ_ext bound-edge (r = 0.1, 3) — S0.3-1 validation set.
- **R3 cross-reference:** the stationarity this normalization assumes is the same registered
  M1 validity condition G(ii) — one assumption, stated once, binding both.
- Interaction rows (registered): PR-7 charges the optical drive at P̄₀; PR-10's
  modulator-drive rows price the same P̄₀; PR-6 gives both arms the identical budget; the
  hardware analogue of the E₀ calibration is a Stage-1 convention (flagged, not silently
  assumed).

### Anchor-risk register (PR-1.1 transfer-check rule, GA-F6 physics scope)
No executable reference implementation exists for a physics cell — the transfer check is
**out of scope by the registered rule**; the analogous risk is carried instead by: (i) the
[EV]/[AV] provenance trail per number (R§Appendix A); (ii) the **conservative-bound
construction** of C-2 (registered values strictly worse than the verified demonstration —
now confirmed against the full measured distribution, see C-2); (iii) the M2 one-off
validation of the M1 reduction (now two cells, P4-F9); (iv) the named residual risks on C-2
(body-provenance — **RESOLVED 2026-06-13** via the independent peer-reviewed commentary
reproducing Cui's figures — + geometry transfer, priced by the ×2-loss derate row); **(v) the Er-gain budget
applies the flagship's straight-implanted-waveguide coefficient (1.0–1.9 dB/cm [EV]) to an
undoped foundry ring on a different process — a Stage-1 integration assumption (R§4f),
carried as a label on every gain-bearing cell (and the source of C-1's material-aspirational
label, G reachability); (vi) P_sat's ring scaling (formula in G) is an anchor-transfer
assumption validated only at Stage 1 (P4-F7).** The v1 sentence registering *infeasibility of
deeper verification* is **superseded (P4-F5):** the Cui body-level numbers were confirmed
[EV] (2026-06-13) via an independent peer-reviewed commentary that reproduces Cui's figures
(Ye & Marpaung, Adv. Photon. 5(5) 050503, CC-BY, archived in `docs/s0_3/refs/`); only
retrieval of the *primary* Cui PDF remains programmatically walled (bot-walled, six
attempts/two sessions) — and is no longer load-bearing.

**Freeze checklist for Lucas (after Critic review — verdict AMEND, this v2 is the revision):**
the registered choices are — M1 (+M2 validation ×2 cells, M3 trigger) · **operating point
g_rt = 0.9× intrinsic per cell (P4-F1)** · cells C-1/C-2/C-3 with roles as above, NF-A
headline · K4 r ∈ [0.1, 3], θ₀ = 0.3 · K-pol-3 always-ON · H1 · O2 @ P̄₀ = 1 mW with the
in-block E₀ formula. Everything else in the input sheet's menus is a labelled sensitivity
axis or an explicitly-owned deferral (P4-F10). **Pre-signature action (P4-F5): DISCHARGED
2026-06-13** — the Cui body-level numbers are confirmed [EV] via the independent
peer-reviewed commentary (C-2 verification status); residual risk (i) closed. No action
remains for Lucas but the signature itself.

---

## PR-6 — 🔒 **SIGNED v3** (2026-07-07) — the fairness contract (F7, **CRITICAL**) — the S0.4 bake-off apples-to-apples standard

> **Status: 🔒 SIGNED v3 (2026-07-07, by delegation).** Lucas 2026-07-07: *"don't use the critic for
> now on do everything"* — packet closure (re-confirm + signature) delegated to the Supervisor
> (E-2026-07-05-1 resolution). The focused v3 re-confirm was **Supervisor-performed** (Critic
> suspended; APPROVE-WITH-EDITS, 3 stale cross-refs fixed pre-signature — see
> `critic_review_s0_4_freeze.md` tail, independence disclosure there). **This signature also ratifies
> the §G frozen-PR-4-§N ride-on** (multi-point E₀ total-energy budget + the δ-conformance option).
> From here PR-6 §B/§C/§D/§E/§F/§G are frozen; the registered S0.4-0 numerics (r_min, resolved B,
> multi-tap E₀, participation profile) land as the single calibration addendum before any bake-off
> run. — *Drafted PROPOSED v3 2026-07-05 (Supervisor), folding the Critic max-effort pass + Lucas's
> delegated D3/D4 ("go", E-2026-07-05-1).* v3 changes:
> **§B** — registered effective-dimension (participation-profile) measurement + reporting requirement
> (the ≈3-of-32 capacity finding), the reservoir-baseline **falsifier consequence** (margin → PR-9),
> the **{1,9,17,25}** S0.4-0 search seed (Critic-verified 26/32), fallback wording "controllable
> subset"; **§C** — the v2 clause (b) M1-validity governor **DROPPED** (REFUTED: no §G(iii) void
> ceiling frozen; never binds before clause (a)) → r_min = clause (a) + Δr (candidate ≈ 0.16), with
> Lucas's M1-validity check registered **PERFORMED + PASSED** across the clamped box. v2
> (2026-06-17) folded the Critic AMEND + Lucas's delegated D1/D2 calls (E-2026-06-17-1,
> "OK I trust you"). v1 →
> AMEND (`critic_review_s0_4_freeze.md`: spine CONFIRMED — §A saturating-for-all, §C A-over-B/C, lasing
> arithmetic to the digit — two HIGH blockers + 7 mechanical). v2 changes: **§B** P6-F1 — the input map
> B becomes a **measured-minimal-controllable** topology (meaningful-ratio gate; E/O-cost-priced; (c)
> down-scope fallback), not the failed μ_c=0.3κᵢ single-drive init; **§C/§D** P6-F2 — clamp evaluated
> **on-resonance on the *saturating* κ_net**, m_κ/Δr **frozen**, δ-band numeric, "δ-aware" label dropped
> + off-resonance de-saturation logged as anchor-risk (with an S0.4-0 §G-conformance check that may
> restore it); **§E** P6-F6 SPSA c-grid in the feasible box; **PR-5** P6-F5 decomposed reporting;
> **PR-7** P6-F7 rank principle + P6-F8 PR-3-gate; **PR-12** P6-F9 wording. **Frozen-block ride-on:**
> §B's multi-point B and §C/§D's possible δ-fix re-derive the PR-4 §N E₀ injection convention → ratified
> by Lucas's packet signature (see §G-addendum below), not unilaterally.
> **Governs:** all four estimators (SPSA · PAT · recurrent in-situ adjoint · RHEL) on the shared
> `DissipativeRingSubstrate` (PR-4), S0.4a → S0.5. **Encodes Lucas's 2026-06-17 rulings:** gain
> mode `saturating` for all four (CONFIRM 1); κ_ext clamp **A** (D-2026-06-13-1 — the r_min rule is
> now v3 clause-(a)-only, §C: the "δ-aware" framing was dropped at v2 and the M1-validity governor
> refuted at v3, with the required M1 check recorded PASSED); the PR-12 **R-ii** disposition (block
> below). Sources: the frozen PR-2 v2
> (partition P2, data regime, init ownership, R2 readout, reservoir baseline), PR-4 v2 §G/§K/§N,
> the Critic S0.3-1 findings S31-F1/F2/F8, the PR-1/PR-2 freeze-review carry-ins (PF-F8a/b), the
> roadmap S0.5 sample-efficiency primary metric, the §6 CLAUDE quality standard (≥8 seeds).

### A — Physical-operations invariant (what a gradient may touch)
- **One shared substrate.** Every estimator's updates derive **only** from simulated device passes
  through the *single* `DissipativeRingSubstrate` instance (PR-4), with **fresh ASE per pass**
  (PR-11 stream independence). `autodiff-through-substrate` (BPTT) is **reserved for the PR-3
  reference ceiling only** — it is *not* one of the four estimators.
- **Gain mode = `saturating` for all four** (CONFIRM 1, Lucas 2026-06-17). SPSA's two forward
  passes and PAT/adjoint/RHEL's backward/adjoint/echo passes target the **same** g(P̄) function
  (PR-4 §G). No estimator runs `gain_mode="fixed"` — that is the demoted diagnostic floor (its
  ∂g/∂κ_ext≡0 drops 27 % of the κ_net channel at θ₀, 6× the retained term sign-flipped at the
  edge; S31-F1). **Load-bearing:** a method may not face a different substrate than its rivals;
  the whole bake-off premise is that the four train one model.
- **Stochasticity convention.** The **data stream** (PR-2 streaming fresh i.i.d. draws) and the
  **θ₀ init** are common-per-seed across methods (§B). **ASE realizations are fresh per pass,
  independent across methods** — exogenous hardware noise is not shared (sharing it would be an
  unphysical variance-reduction not available on a real device; PR-11). What is held common is the
  *task*, not the *noise*.

### B — Initialization: common θ₀ + the connected-init fix (S31-F2)
- **Common θ₀ per seed**: identical starting (δ_j, κ_ext,j, μ_jk) and identical data ordering
  across all four methods (PR-2 PF-F8a/b carry-in, verbatim). δ_j and κ_ext,j init = the PR-2
  reference D-LinOSS radial-band init mapped through the B1 ranges; **κ_ext init at θ₀ = r₀ = 0.3**
  (safely above r_min, §C).
- **The starvation problem (P6-F1, Critic HIGH — re-derived from code).** A connected init alone does
  **not** fix C-2. With the input driven into ring 1 only (input map B = e₁) and the nearest-neighbor
  chain, the per-ring task-gradient decays ~(μ/κ_net)^hop; at μ_c=0.3κᵢ ring-32 sits at **2.2e-28** of
  ring-1's gradient — the deep half of the 32-ring chain stays at init. This is **controllability**, not
  μ(0): a single input point + a length-32 chain starves the far end regardless of μ(0) in the
  weak-coupling regime (strong coupling μ_c≈2κᵢ "fixes" it only by delocalizing rings into supermodes —
  rejected: breaks the one-ring-one-pole framing / exits the K4 box). μ(0)=0 is strictly worse
  (S31-F2: exactly-zero task gradient noiseless; zero-mean noise gradient with ASE).
- **Input map B — registered as the minimal controllable topology (D1, Lucas-delegated 2026-06-17;
  the *rule* is frozen, the *topology* measured at S0.4-0).** B = the **fewest input taps** (spread
  along the chain) such that, at C-2 (N=32), the connected init, on-resonance, **every** ring's task
  gradient ≥ **10⁻³ · ring-1's** (the meaningful-ratio gate — replaces the hollow "nonzero" smoke).
  Drive amplitude split equally across taps. **Connected nearest-neighbor init μ(0) = μ_c = 0.3·κᵢ**
  retained (supersedes PR-2 PF-F8b's μ(0)=0 *reference default* — delegated authority, not a frozen
  override; PR-2 froze no μ(0) value). The same B + μ_c are common across all four methods (fairness)
  and given to the reservoir baseline (digital-side — the in-situ claim is about the recurrence
  μ/poles, not B; the contrast stays clean). **S0.4-0 search seed (registered, v3):** the
  Critic-verified candidate **{1, 9, 17, 25}** (lifts 26/32 rings ≥ 10⁻³·ring-1 at C-2, vs 3/32
  single-drive) — the minimal-tap search starts there, then tries fewer taps and completed coverage
  within K.
- **The capacity finding + the registered effective-dimension report (P6-F1 max-effort pass; D3,
  Lucas-delegated 2026-07-05 "go").** At the v1 §B remedy (single-drive B=e₁, μ_c=0.3κᵢ) the C-2
  settled-state amplitude profile has an **effective participating dimension ≈ 3 of 32 rings**
  (1 ring ≥ 0.1·|a₁|, 3 ≥ 10⁻³; ring-8 already 6×10⁻⁷) — i.e. the headline cell would run a ~3-mode
  recurrence wearing a 32-ring label. Accordingly, two registrations: **(1) S0.4-0 measures the
  participation profile** (per-ring settled |a_j|/maxⱼ + the count ≥ 10⁻³) under the *resolved*
  input map B, and **every use of the "N=32" label in results and paper carries the measured
  effective dimension**. **(2) Falsifier consequence:** the reservoir baseline (§F; PR-2 §5.3 —
  readout-only on the same substrate) is the **in-data falsifier of debt #1**: if the
  in-situ-trained recurrence fails to clear it at the headline cell, the "training the recurrence
  matters" claim **fails in-data at that cell** and is reported as such (the quantitative
  clear-margin freezes at PR-9 with the Gate-ii semantics, per the existing deferral).
- **Systems cost is priced, not assumed (the §10 carry).** Multi-point drive ⇒ more E/O channels
  (DAC/modulator per tap) — the conversion overhead the S0.7 envelope is most fragile on. S0.4-0
  **reports the resolved tap count to the envelope (PR-10)**; the trainability fix is charged against
  the §10 advantage, not hidden.
- **Honest fallback (c).** If **no bounded-tap B** (≤ a registered cap K_taps, candidate K=4) clears the
  10⁻³ gate at C-2, the headline **down-scopes**: the C-2 claim becomes "the **controllable subset**
  (the tap neighborhoods) is trained in situ," N=32 is reported as a **capacity-vs-controllability
  study**, and the measured effective trainable depth is stated. *(The registered seed previews this
  path: {1,9,17,25} reaches 26/32 at K=4 — if that is the ceiling, an honest ~26/32 report is a
  strong result; the gate is **not** softened to dodge the fallback.)* Either way the deep-ring limit
  is on the record, not hidden; the W1 claim attaches to the rings that are *actually* trained in situ.
- **Frozen-block ride-on:** a multi-point B re-derives the PR-4 §N E₀ injection convention (which froze
  single-port-ring-1 injection) — registered in the §G-addendum below, ratified by the v2 signature.

### C — κ_ext clamp: **policy A** (D-2026-06-13-1) — the saturating-mode feasible box
- **The hazard (measured, S0.3-1b).** Under `saturating` (§A), at κ_ext below θ₀ the on-resonance
  build-up falls, g **de-saturates above the 0.9κᵢ ceiling** (the §G ceiling is the *operating-point
  target*, not a hard cap on the saturating form), and κ_net = κᵢ − g(P̄) + 2κ_ext **crosses zero**.
  At the current init: r* ≈ 0.134 (cell-independent), κ_net/κᵢ = −0.318 at the K4 lower bound r=0.1
  → the ring lases. Because M1 holds the gain **fixed within the episode** (the in-loop dynamics are
  *linear*; saturation acts only between episodes, §G), there is **no in-rollout clamp** — the
  linear rollout diverges. So the registered K4 lower bound r=0.1 is **infeasible in saturating
  mode**; the K4 prerequisites §K(i–iii) silently assumed the fixed-mode relation
  κ_net=0.1κᵢ+2κ_ext, which CONFIRM 1 breaks at the lower edge.
- **Clamp A (Lucas 2026-06-17).** The operative trainable band that `clamp_to_bounds()` enforces
  **during training, in saturating mode** is **κ_ext ∈ [r_min, 3]**. K4's [0.1, 3] is **retained as
  the passive/fixed-plane bound** — the plane the frozen B1/E₀ numbers live on (`test_c`/`test_e`
  already pin `gain_mode="fixed"`); no PR-4 number changes.
- **r_min rule — v3, clause (a) alone, on-resonance on the *saturating* κ_net (P6-F2 max-effort
  pass; D4, Lucas-delegated 2026-07-05 "go". The formula + margins are frozen here, the *number* is
  measured at S0.4-0 + addended).** r_min ≡ (the smallest r such that, at the connected init (§B),
  **on-resonance (δ=0)**, the **saturating** κ_net(r) ≥ m_κ·κᵢ — a positive net-loss floor,
  **m_κ = 0.05 (frozen)**) **plus** a frozen safety margin **Δr = 0.02**. **Candidate r_min ≈ 0.16**
  (the κ_net = 0.05κᵢ crossing sits at r ≈ 0.14, above the bare lasing crossing r* ≈ 0.134 — this
  rule is *more* conservative than r* + Δr). The **numeric r_min** is a mechanical S0.4-0 sweep,
  reported as a one-line addendum **before any bake-off run** and frozen there (the E₀ deferral
  pattern). **Clamp identical for all four; reservoir baseline at κ_ext≡0.3 unaffected.**
- **The v2 clause (b) — the M1-validity governor — is DROPPED in v3 (Critic max-effort pass:
  REFUTED; Supervisor-verified textually).** Three independent reasons, each fatal: (i) frozen §G(iii)
  registers only the θ₀ *value* (E_sym/E_sat ≈ 5×10⁻⁶–9×10⁻⁵) — **no void ceiling was ever frozen**,
  so the clause had no registered threshold to test against; (ii) even evaluated on the saturating
  κ_net, it can **never bind before clause (a)**: at the clause-(a) floor the circulating energy is
  ×37–×91 vs θ₀ ⇒ E_sym/E_sat ≈ 3×10⁻³–10⁻² ≪ O(1); (iii) hence "r_min governed by r_M1 > r*"
  cannot occur in-band. **Lucas's required check — "r* verified inside M1's validity"
  (D-2026-06-13-1) — is registered here as PERFORMED and PASSED across the entire clamped box**
  (E_sym/E_sat ~10⁻² at r*, ≲10⁻² at the clause-(a) floor, ≥2 orders inside the O(1) void; the exact
  floor factor lands with the S0.4-0 r_min addendum). The requirement is honored as a **recorded
  verification result**, not a live governor that the ledger cannot evaluate.
- **Off-resonance is an unmodeled hazard, logged as anchor-risk (P6-F2 (i); the "δ-aware" label is
  dropped).** As-built the gain uses an **on-resonance** build-up, so κ_net is δ-independent — the
  substrate cannot evaluate a δ-aware r_min. Physically, a **detuned** ring has lower build-up ⇒ less
  saturation ⇒ g de-saturates toward g₀ ≈ 187κᵢ ⇒ it lases *more* easily — so the on-resonance r_min
  is a **lower bound** and the clamp may be slightly permissive when rings are simultaneously
  detuned-and-low-κ_ext. Registered as **anchor-risk (vii): off-resonance de-saturation is unmodeled;
  on-resonance r_min + Δr is the operative clamp.** **S0.4-0 §G-conformance check:** determine whether
  a δ-dependent build-up (PR-4 §G already registers P_circ = Σⱼ|aⱼ|², which *is* δ-dependent if it
  uses the actual field) is a **conformance fix** (no freeze change — the on-resonance build-up would
  then be an implementation simplification, cf. the S31-F1 gain-mode flip) rather than a model
  addition; **if conformance-cheap, fold it in** and r_min becomes genuinely δ-aware + conservative
  (re-addended); **else** the on-resonance clamp stands with anchor-risk (vii) logged.
- **Why A, not B or C (registered rationale).** **B** (hard-cap g ≤ 0.9κᵢ everywhere) *adds an
  unregistered mechanism*: it caps the saturating form below θ₀, putting a **kink in ∂g/∂κ_ext at
  θ₀** — the very gradient PAT/adjoint train on — a modeling choice the freeze did not make (the
  Executor correctly did **not** implement it). **C** (soft barrier in the objective) *cannot stand
  alone*: the divergence is in the forward **state recurrence**, not the loss landscape, so SPSA's
  sub-threshold perturbation diverges the rollout before any finite penalty can bite. **A is the
  only option that contains the SPSA hazard** while keeping §G's saturating form intact. (C may ride
  *on top of* A as an optional estimator-side soft guard — non-load-bearing.)
- **Identical for all four** (fairness): SPSA's ± perturbations, PAT/adjoint/RHEL updates all project
  onto [r_min, 3]. No method may reach a κ_ext its rivals cannot. The **reservoir baseline** holds
  κ_ext ≡ θ₀ = 0.3 (PR-2 §5.3) — above r_min, unaffected.

### D — Shared training protocol (the sweep recipe, S31-F8) — co-registered with §C
- **Data regime:** streaming fresh i.i.d. draws per iteration; per-seed generator stream **common
  across methods** (PR-2 PF-F8a, verbatim) — streaming-vs-corpus changes what sample-efficiency
  *means* and is not an implementation choice.
- **δ-band (numeric, P6-F4).** Detuning init band **δ_init ∈ [−κᵢ, +κᵢ]** per ring (the B1 radial-band
  image that keeps poles in the S0.1 realizable region at every cell — Critic-reviewable; ≤ half the
  100-GHz-FSR free range, well inside the in-band pole region). Role in v2: it is the **init** detuning
  range and the band the **S0.4-0 §G-conformance check** (§C) sweeps to characterize off-resonance
  de-saturation — **not** the r_min sweep (r_min is on-resonance per §C). No longer double-deferred.
- **Batch:** 8 fresh sequences per gradient step (one device pass = one sequence, PR-7 §C).
- **LR schedule / grad-clip (P6-F8):** cosine decay from a per-method base LR; **global-norm gradient
  clip at 1.0**; the per-method base-LR + SPSA c (§E) tuned within the equal HP budget on the
  **registered validation cell = C-2 at a held-out SNR (24 dB), distinct from the 28 dB test cell**,
  frozen before the gated seeds.
- **Budget B:** the equal max-device-pass horizon per cell (§E) = PR-8's right-censoring horizon.

### E — Equal budgets
- **Equal HP budget per method.** Each estimator gets the **same-size** hyperparameter search
  (e.g. equal number of {base-LR, perturbation-scale c, clip} trials), tuned on a **registered
  validation cell distinct from the test cell**, frozen before the gated seeds. SPSA's c, PAT's
  twin-LR, the adjoint step, RHEL's echo gain all get **equal** search — no method is hand-tuned
  more than another (the F7 core).
- **Equal device-pass budget B per cell.** The PRIMARY bake-off score is
  **sample-efficiency-to-target-accuracy** (device passes to target, roadmap S0.5). All methods get
  the same B at a given cell; PR-7 defines what one device pass *costs* per method (the exchange
  rate), PR-6 fixes B **equal in that common unit**. PR-6 = the budget; PR-7 = the conversion.
- **SPSA boundary handling (P6-F6 — a hazard with no gradient-method analogue).** Near κ_ext=r_min,
  a perturbation c that pushes the −c arm sub-r* would diverge the rollout; clamping that arm to r_min
  biases the two-sided difference. Registered: **the SPSA c-grid is bounded so r_min + c ≤ κ_ext ≤ 3 − c
  for all evaluated κ_ext** (the perturbation stays inside the feasible box); within the equal-HP search
  (above), c is selected from a grid respecting this box. Where a parameter sits within c of a boundary,
  SPSA uses the **one-sided** difference at that coordinate (registered, applied identically) rather than
  a clamped (biased) two-sided one. The residual boundary effect is reported, not hidden.

### F — Seeds, trained set, baseline
- **≥8 seeds** for every method in headline cells (esp. SPSA — high variance); 4 only for the
  exploratory grid (PR-8 / §6 quality standard).
- **Trained set = PR-2 P2 {δ_j, κ_ext,j, μ_jk}, gain-free** (frozen). Digital-side params (encoder,
  B/C residues, R2 head) trained digitally, **common across methods**; the claim attaches only to
  the in-situ recurrent set (PR-2 / W1).
- **Reservoir baseline** (§5.3 contrast): B1 frozen at θ₀ (κ_ext ≡ 0.3), readout-only trained
  (PR-2) — the in-data falsifier of "training the recurrence matters."

### G — Frozen-PR-4-§N ride-on (ratified by the packet signature, P6-F1/F2)
The §B multi-point input map and the §C δ-conformance option both touch the **frozen PR-4 §N E₀
convention** ("calibration injection on the bus port of ring 1 only"). Registered amendment, ratified
by Lucas's signature on this packet (supersession discipline — not a unilateral edit):
- **Multi-point E₀:** under input map B (§B), the encoder scale is derived **once per arm to hit the
  same total intracavity-energy budget E₀** summed over the driven taps (not per-ring) — the "encoder
  cannot buy SNR" invariant is preserved on **total** injected energy. The §N E₀ *formula* and θ₀
  calibration are otherwise unchanged; the numeric E₀ is re-evaluated for the resolved B at S0.4-0 and
  addended (the existing §N deferral, now over the multi-tap drive).
- **δ-conformance:** if S0.4-0 finds δ-dependent build-up is a §G P_circ=Σⱼ|aⱼ|² conformance fix (§C),
  that too is a §G/§N-faithful correction (no new mechanism), addended at S0.4-0.
Both numerics ride the **single S0.4-0 calibration addendum** consumed before any bake-off run.

### 🔒 S0.4-0 CALIBRATION ADDENDUM (2026-07-07; single-session mode) — the registered deferrals, discharged. Frozen; consumed by S0.4a+.
Evidence: `results/s0_4_0/s0_4_0_calibration.{md,json}` (deterministic; `analysis/s0_4_0_calibration.py`).
- **§B resolved input map: B = taps {3, 12, 21, 30} (1-based), K=4, equal amplitude split 1/√K
  (total injected power conserved).** The every-ring ≥10⁻³ gate **PASSES robustly** (32/32; worst
  ratio 1.42×10⁻³ under the recorded min-over-5-drive-seeds protocol); **fallback (c) NOT
  triggered**. The registered seed {1,9,17,25} is *not* the winner (28/32 robust — ring 32 sat 7
  hops from a tap); the registered search ("fewer taps, then completed coverage within K") found the
  tail-covered set. No K≤3 clears robustly (best 24/32); K=2 fails under the honest reading. **Two
  measurement-protocol rulings, recorded:** (i) gate reference = the **max ring** (the vs-ring-1
  letter is gameable when ring 1 is not a tap — K=2 passes it with rings at 10⁻⁵ of max, the
  hollow-gate pathology the gate replaces; both readings co-reported); (ii) per-ring ratio = min
  over drive seeds {7,19,41,101,271}, adopted *before* finalist evaluation (single-seed margins
  flicker ×20 with the realization). **Participation profile under the resolved B (the registered
  "N=32 carries eff-dim" rule): counts ≥{0.1, 10⁻², 10⁻³} = {4, 26, 32}/32**; single-drive
  verification of the capacity finding: {1, 3, 5}/32. **E/O cost to PR-10/S0.7: 4 input channels.**
- **§C r_min = 0.1606 (FROZEN; operative saturating-mode band r ∈ [0.1606, 3]).** Clause (a)
  crossing r_a = 0.1406, + Δr = 0.02; cell-independent (C-1/C-2/C-3 identical to 4 digits);
  r\* ≈ 0.1337. κ_net/κᵢ at r_min = 0.1749. Enforced in code (`cells.R_MIN_SATURATING`,
  mode-aware `clamp_to_bounds`); fixed/passive planes keep K4 r=0.1. PR-12 init-consistency ✓
  (r₀=0.3 and the damping axis inside the band). **E_sym/E_sat record (pins the ×37-vs-×91
  factor — both moot in-data):** measured as-built build-up at the floor is **×0.42 of θ₀** (not
  ×37 or ×91): the K-pol-3 doublet (γ/κ_net = 16.6 at the floor) + chain hybridization quench the
  single-pole on-resonance build-up both prior estimates presumed. E_sym/E_sat: floor (as-built)
  **[2.1×10⁻⁶, 3.8×10⁻⁵]** — *better than the θ₀ band*; r\* (field-consistent solve; as-built has
  no steady state there) **[4.7×10⁻⁶, 8.5×10⁻⁵]**; even the never-realized single-pole worst case
  (×91.9) stays ≤ 8.3×10⁻³ ≪ O(1). **Lucas's D-2026-06-13-1 check: PASSED with measured factors.**
- **§C/§G conformance determination: NOT conformance-cheap → the on-resonance clamp stands;
  anchor-risk (vii) is REAL and now quantified.** Actual-field P_circ needs a per-episode
  self-consistent solve — it would change the g(P̄) surface all four estimators train through
  (PR-6 §A) and add passes PR-7 would have to price: a model change, not a conformance fix.
  Magnitude (hypothetical Lorentzian δ-aware build-up over the §D band): at r_min a ring detuned by
  |δ|=κᵢ de-saturates to **κ_net = −0.48κᵢ (super-threshold)**; a δ-aware clause (a) would sit at
  r_min ≈ 0.2547 (+0.094). Goes verbatim to the paper's F19 limits section: *a real device detuned
  at low κ_ext could lase where this model does not.*
- **§G-addendum multi-tap E₀: INVARIANT — no numeric change.** CW-equivalent reading at θ₀:
  E₀(measured) = 1.069×10⁸ photons for single-port, seed, and resolved B alike (ratio 1.000000 to
  the frozen closed form; equal power split over identical rings reproduces the single-port E₀
  exactly). Encoder scale unchanged (=1 at θ₀); "encoder cannot buy SNR" preserved on total energy.
- PR-5 numeric mismatch levels: recon memo `docs/s0_4/pr5_twin_mismatch_recon.md` (menu; the levels
  freeze in the S0.4a task spec per the PR-5 v2 deferral).

---

## PR-7 — 🔒 **SIGNED v2** (2026-07-07) — the cost metric (F5)

> **Status: 🔒 SIGNED v2 (2026-07-07, by delegation — the packet-v3 signature, PR-6 block).**
> *(v2 = the P6-F7 fold: §B rank-ledger principle — device passes are the
> primary rank, the digital side-ledger is **always co-reported**, ledger-tiebreak semantics → PR-9).*
> Defines the unit the PRIMARY bake-off score is measured in, so PR-6 §E's
> "equal budget B" is unambiguous. Honors the PR-4 §N interaction rows (PR-7 charges the drive at
> P̄₀; PR-6 gives both arms the identical budget) verbatim.

### A — Cost unit = one physical device pass (any direction)
One **device pass** = a single forward / backward / adjoint / echo propagation through the shared
substrate over **one sequence/episode**. The PRIMARY metric = **device passes to reach target
accuracy** (PR-3 ceiling-relative target). **S0.4-close gate (P6-F8):** "target accuracy" is defined
by PR-3's ceiling-relative *rule*, which **must freeze before S0.4 closes** — S0.4a may *start* under
this packet, but no to-target statistic is final until PR-3's rule is signed. Per-method exchange rate:

| estimator | device passes / gradient step | digital side-ledger |
|---|---|---|
| **SPSA** | **2 forward** (two-sided ±c; model-free) | — |
| **PAT** | **1 forward** (physical) | **+1 twin-backward** (digital twin — *not* a device pass) |
| **recurrent in-situ adjoint** | **1 forward + 1 adjoint** = 2 (adjoint is a *physical* reverse pass by hypothesis) | — |
| **RHEL / Hamiltonian-echo** | ~~**1 forward + 1 echo** = 2~~ **→ PR-7.1 (§E-adjacent, below): 1 forward + 2 echo = 3** (+ the χ³ echo sub-model penalties, PR-11 — charged to accuracy-per-pass, not the count, now ×2/update) | — |
| **BPTT reference** (ceiling, not ranked) | 1 forward/step | **+1 autodiff-backward** (digital) |

- **The PAT crux (honest):** PAT's backward runs on the **digital twin**, so it lands on the digital
  side-ledger, **not** the device-pass count — PAT = 1 device pass/step. PAT spends *digital* compute
  to save *device* passes; both are reported (§B). This is exactly PAT's value proposition and must
  not be hidden by merging ledgers.
- **Adjoint realizability caveat:** the count charges 1 physical adjoint pass *as if* realizable; the
  recurrent-adjoint demonstration gap (debt #4) is the *separate* hardware-slot question (§5.2
  guardrail) — the simulation bake-off measures sample-efficiency assuming the pass exists.

### B — Digital-compute side-ledger (reported alongside, never merged — F5)
Captures PAT's twin-backward FLOPs, BPTT's backward FLOPs, the digital head/encoder training. The
**device pass is the physical-scarce resource** the photonic advantage is about; digital FLOPs are
conventional compute. A method that saves device passes by spending digital FLOPs (PAT) has a real
but *different* advantage than a model-free one (SPSA) — two ledgers keep that honest, and feed the
S0.7 systems-advantage envelope (PR-10) without double-counting.
- **Rank-ledger principle (P6-F7, outcome-determining — pinned now).** The PRIMARY rank runs on
  **device passes** (the photonic-scarce resource); the **digital side-ledger is always co-reported**
  and **no method may be called "most sample-efficient" without both shown**. The rank's median-passes
  tiebreaker (PR-8/PR-9) structurally favors the 1-pass method (PAT), so a PAT win on device-passes that
  rides a larger digital ledger must display both — the headline cannot hide the twin cost. Whether the
  digital ledger *enters* the rank (vs co-reported-only) is the one residual choice, **explicitly
  deferred to PR-9** with this principle binding it (it is registered as a known fork, not a silent hole).

### C — Batch convention
**One device pass = one sequence.** A batch-8 step costs (passes/step from §A) × 8 forward device
passes. Sample-efficiency is measured in **total device passes** (= steps × passes/step × batch),
never in steps (steps flatter the 2-pass methods). So at batch 8: SPSA = 16 fwd passes/step; PAT = 8
device passes/step (+ 8 twin-backwards, side-ledger). The metric captures the 2× device-pass gap and
the twin cost simultaneously.

### D — Interaction pins (PR-4 §N, verbatim)
PR-7 charges the optical drive at **P̄₀ = 1 mW**; PR-10's modulator-drive rows price the same P̄₀;
PR-6 gives both arms the identical budget. The device-pass **count** is the bake-off metric; the
**energy per pass** (conversion stack × passes) is the S0.7 envelope's concern — distinct but
consistent, no double-count.

### E — M3-trigger-margin hook (PR-4 §G carry-in)
The §G M3 trigger ("a gated S0.5/S0.6 comparison within a margin where the gain-model class could
flip the verdict") needs "the verdict" defined. **Form** (registered here; the numeric Δ lands in
PR-9 at the S0.5 freeze, before any bake-off results — honoring §G's "frozen with PR-5–9/PR-11"):
the verdict = the PR-9 lexicographic rank (success-fraction to target, then median device-passes);
the M3 trigger fires when the leader↔runner-up gap is **smaller than** the fixed↔saturating gain
sensitivity at that cell. Registered as a pointer now; quantified at PR-9.

### PR-7.1 — factual amendment to §A row 4 (RHEL pass count), 2026-07-07

> **Status: registered 2026-07-07 (single-session mode, by the standing delegation; v2 above
> retained per supersession discipline).** Source-driven correction, not a judgment call: the
> RHEL algorithm as published (Pourcel & Ernoult, arXiv:2506.05259, verified against the paper
> body 2026-07-07 — PR-11 ⚠verify-1) computes the gradient as a **symmetric finite difference
> between TWO nudged echo trajectories**: forward + echo(+ε) + echo(−ε).

- §A row 4 becomes: **RHEL = 1 forward + 2 echo = 3 device passes / gradient step** (+ the χ³
  echo sub-model penalties per PR-11, now charged **twice per update** — each echo pass starts
  from its own physical conjugation event). Digital side-ledger unchanged (—).
- §C batch arithmetic follows: at batch 8, RHEL = 24 device passes/step.
- Direction of the correction: **against** RHEL (3 > 2, and doubled conjugation penalties) — it
  cannot flatter the outsider method; fairness (PR-6) requires charging the true cost. The
  one-sided alternative (forward + single nudged echo vs the unperturbed reference) would be a
  *modified* algorithm, not the published one — if S0.4c wants it as a cheaper RHEL variant it
  must be registered as a separate arm, not silently substituted.
- **Extension (2026-07-07, same day — the S0.4c spec's operational analysis):** the paper's
  3-pass count relies on **Hamiltonian re-traversal chaining** (the echo returns the system
  near its pre-forward state, so the next pass can reuse it). On a **dissipative** substrate
  that chaining is unavailable (the echoed state is attenuated ~η_c·e^(−2κ_net·T)) and *state
  cloning is unphysical* — each nudged echo needs its own physical forward. **Operational
  bake-off count: RHEL = 2 forward + 2 echo = 4 device passes/update** (at batch 8: 32
  passes/step). The **split-state 3-pass variant** (beam-split a(T) into two conjugation arms;
  −3 dB + vacuum on each echo) is registered as a *variant*, not run in the headline. Direction:
  again against RHEL; again factual (dissipation is the substrate's defining property).

---

## PR-5 — 🔒 **SIGNED v2** (2026-07-07) — PAT twin-mismatch families (F7.2–3, **CRITICAL**) — *structure frozen; numeric levels recon-deferred to S0.4-0*

> **Status: 🔒 SIGNED v2 structure (2026-07-07, by delegation — the packet-v3 signature, PR-6
> block) · numeric mismatch levels [RECON-DEFERRED → S0.4-0], addended before S0.4a.**
> *(v2 = the P6-F5 fold: §B decomposed mismatch reporting — {M-par-only / M-struct-only / both /
> perfect-twin}, so PAT's headline isn't conflated with being handed the gain omission.)* PAT is
> Physics-Aware Training: physical forward, **digital-twin backward**. PAT's robustness *is* its
> ability to train when the twin ≠ the substrate; testing it against a *perfect* twin would flatter
> it (a perfect twin = BPTT-through-twin, unphysical for PAT's value). PR-5 registers the
> **twin-mismatch** so the test is honest. The *families* are a design decision (registered now,
> Critic-reviewable); the *magnitudes* want a metrology/PAT-precedent source (the project's
> menu-sourced-then-frozen discipline) → S0.4-0 recon + addendum, exactly as PR-4's E₀ *number* rode
> the S0.3-1 calibration.

### A — Mismatch families (the twin's gap vs the substrate); headline = one registered level each
- **(M-par) Parametric calibration error.** The twin's {κᵢ, κ_ext, δ, μ, g₀, P_sat, γ} differ from
  the substrate's by **characterization-accuracy-realistic** offsets. **Levels [RECON-DEFERRED]:**
  per-parameter brackets from realistic SiN ring + gain metrology (linewidth-fit κ accuracy,
  resonance-tracking δ, gain-characterization g₀/P_sat — the loosest) — sourced at S0.4-0.
- **(M-struct) Structural omission.** The twin omits a mechanism it plausibly would not model
  perfectly. **Headline candidate — the twin linearizes the gain (`gain_mode="fixed"`) while the
  substrate saturates** — this reuses the demoted `fixed` mode in its *honest* role and directly
  tests whether PAT absorbs the dropped ∂g/∂κ_ext (the exact S31-F1 quantity). Alternates registered
  as sensitivity: twin single-pole (γ=0) vs substrate splitting; twin A1-ASE vs substrate A2.
- **(M-noise) Noise-model mismatch.** Twin assumes a different NF/ASE than the substrate's NF-A 7.0
  — candidate twin at NF-C 3.0 (optimistic) — testing PAT under noise-underestimate.

### B — Headline + reporting (decomposed, P6-F5)
Headline = the registered realistic (M-par) level **+** the (M-struct) gain-linearization omission;
**PAT reported as accuracy/efficiency *as a function of* mismatch** (the table-descriptor mandate).
**Required decomposition (P6-F5 — never report the combined number alone):** the four cells
**{M-par-only, M-struct-only, both, perfect-twin}** are reported separately. Rationale: M-struct
(gain-linearization) hands PAT *exactly* the ∂g/∂κ_ext omission the white-space claim turns on, so a
single combined number conflates **PAT-the-method** with **PAT-handed-the-gain-omission**; the
decomposition keeps them distinct. The **perfect-twin cell is an upper-bound diagnostic only**, never
the headline.

### C — Calibration-error unification (PF-F7.3) — the in-situ-vs-offline fairness
The **offline-train-deploy baseline** (§5.3 fallback: train in simulation, deploy weights open-loop)
suffers a weight-mapping error = **the same (M-par) family at the same level** as PAT's twin error.
Registering them from one family makes "in-situ training (PAT) vs offline-deploy" fair: both face the
same characterization accuracy; PAT gets to **adapt** to it via in-loop physical forward passes,
offline-deploy does not. This is the registered apples-to-apples for the in-situ-vs-offline contrast
the white-space claim leans on.

### D — Recon scope (S0.4-0)
The numeric levels in (M-par)/(M-noise) + the (M-struct) magnitudes are sourced from: realistic SiN
characterization accuracies (ring + Er-gain metrology) and the **PAT-precedent twin-gap** (Wright
et al., *Nature* 2022, and the SPSA hardware demos). Drafted as a menu, frozen by Lucas after the
recon — no invented numbers enter the headline.

---

## PR-12 — 🔒 **SIGNED disposition v2** (2026-07-07) — **R-ii: D-LinOSS damping is a distinct knob** (Lucas 2026-06-17; resolves the PR-4 §G ↔ PR-12 reconciliation)

> **Status: 🔒 SIGNED v2 (R-ii) (2026-07-07, by delegation — the packet-v3 signature, PR-6 block).** *(v2 = the P6-F9 fold: init-consistency wording fixed — only
> κ_ext-valued quantities are constrained to [r_min, 3] — + the roadmap "damping cell" reword,
> applied 2026-07-05.)* RECONCILE 1 (E-2026-06-13-2): the coarse S0.3-1 damping sweep
> parametrized "damping" as the gain compensation g_f — **but g_f = 0.9 *is* PR-4 §G's registered
> operating point** (κ_net = 0.1κᵢ + 2κ_ext); PR-12 cannot freely "select" g_f without contradicting
> signed PR-4. **Lucas ruled R-ii.**

- **R-ii (registered).** D-LinOSS **damping** is **not** g_f. It is the **trainable per-ring net
  loss** — the pole-real-part range the partition explores via **κ_ext (the K4 box) at fixed
  g_f = 0.9** (PR-4 §G), i.e. the κ_net(κ_ext) range over the clamped band **[r_min, 3]** (§C). The
  D-LinOSS "damping operating point" is therefore **defined by the §C feasible box + the §B init**,
  not by a separate g_f freeze.
- **The coarse sweep used the wrong axis.** It varied g_f (an illegal degree of freedom under §G);
  it must be **re-run varying the trainable-damping range at fixed g_f = 0.9**. The rerun is also
  **convergence-controlled** (train-to-fixed-loss, not fixed-steps — the S0.3-1 anomaly-B confound:
  the fixed-budget curve conflated accuracy with training speed) and **≥8 seeds** at the candidate
  point. **Gated on Lucas's R-ii signature**; not yet posted.
- **Init-consistency check (Lucas's requirement; gated check at S0.4-0; wording fixed per P6-F9).**
  The box [r_min, 3] is a **κ_ext** band, so only κ_ext-valued quantities live in it: the **κ_ext init
  (θ₀=0.3)** and the **trainable-damping sweep range** (which *is* the κ_net(κ_ext) range over κ_ext)
  must sit inside [r_min, 3]. μ_c (a coupling) and the δ-init band (detunings) are **not** κ_ext ratios
  — they are *not* checked against this box; they have their own ranges (μ_c per §B, δ_init per §D
  within the realizable pole region). The S0.4-0 calibration confirms r_min at the connected init +
  the resolved input map, closing PR-12/K4/PR-6 consistency on the κ_ext axis.
- **Consequence for PR-9.** Because R-ii makes "damping" a *range the estimators train through*
  rather than a *cell we freeze*, the PR-12 "central operating cell" collapses into PR-6 §C/§D; PR-12
  survives as a **pointer to the §C box + the convergence-controlled rerun that characterizes the
  damping→accuracy curve** (a BPTT-reference diagnostic, not a frozen scalar). R-i (subsume into §G
  and drop PR-12) was the alternative; Lucas chose R-ii.

---

## PR-11 — ⬜ PROPOSED (2026-07-07) — the RHEL χ³-FWM echo / phase-conjugation sub-model (F9)

> **Status: ⬜ PROPOSED (Supervisor, 2026-07-07, single-session mode — review non-independent,
> disclosed).** Structure + invariants proposed now; the **numeric freeze happens in the S0.4c
> task spec** (committed before any RHEL run), after the recon's ⚠verify-1..6 items are checked
> — the PR-5 pattern (structure → recon → freeze-at-spec). Recon with the quantified mechanism
> menu: `docs/s0_4/pr11_echo_submodel_recon.md` (+ `analysis/pr11_echo_recon_calc.py` →
> `results/s0_4c/pr11_recon_calc.json`).

### A — The invariants (registered in the row above; bind the S0.4c implementation)
1. Independent forward/echo ASE streams — fresh generators, **no common-RNG reversal**.
2. **No loss-sign flip**: the echo pass propagates through the *same* dissipative substrate.
3. Gain injects **fresh ASE in the echo pass too** (no free re-amplification).
4. **Unit test**: the echo of a noisy forward must **not** recover the noiseless initial state —
   recovery error lower-bounded by (conjugation fidelity × ASE floor).

### B — The sub-model structure (freezes at the S0.4c spec)
One echo update = 1 forward pass + **C_op** + 1 echo pass (PR-7 row 4: 2 device passes; the χ³
penalties charge accuracy-per-pass, not the count). Per doublet mode j:
**C_op: a_j(T) → √η_c,j · e^{iφ_err,j} · a_j(T)\* + n_conj,j**, with η_c,j the *mechanism-derived*
efficiency chain (extraction × conversion × re-injection × timing decay — no idealized
conjugation operator, proposal §6(c) verbatim), φ_err the systematic phase error, n_conj ≥ the
phase-insensitive parametric quantum floor + pump-transfer excess.

### C — The mechanism menu (recon-quantified; freeze picks ONE headline)
- **(A) on-chip shared-spiral conjugator bank — proposed headline:** η_c ≈ −18 dB class at
  P_p = 0.3 W/arm (η_ex = 2κ_ext/κ_net = 0.86 at θ₀, computed live; η_spiral = (γ_nl P_p L)²);
  **N parallel arms** (ring fields spectrally overlap — not wavelength-separable) → **N·P_p ≈
  9.6 W on-chip pump at C-2**, charged to the S0.7 envelope like the S0.4-0 E/O channels.
- **(B) resonant conjugator ring:** the registered enhancement↔bandwidth tension, now
  quantified — under the state-snapshot reading the Q_L ceiling is 1.5e6/5.0e6/2.2e7 (C-1/2/3),
  so not trivially excluded; excluded ×70 under the drive-stream reading (recon ⚠verify-1
  decides). Recorded alternative, not the headline.
- **(C) off-chip conjugation — the explicit admission, priced:** transit amplitude survival at
  10 ns = 0.12/0.54/0.87 (C-1/2/3) + facet losses + N channels; **no storage/timing primitive
  exists to wait out the conjugator** — the decay is the price. Admission only; not run headline.

### D — S0.4c obligations (pre-registered here, before the RHEL build)
- The floor check (roadmap S0.4 gate): as η_c → 1, φ_err → 0, n_conj → 0, ASE → 0, the echo
  update must approach the exact gradient.
- **Both F22 conclusion templates** (RHEL-competitive / RHEL-fails-under-honest-echo)
  pre-drafted in the S0.4c spec before any run.
- RHEL semantics (⚠verify-1: state-snapshot vs drive-stream conjugation; update rule; error
  injection point) settled from Pourcel & Ernoult arXiv:2506.05259 + López-Pastor & Marquardt
  PRX 13, 031020 — and recorded in the spec — before the estimator is coded.

> **⚠verify-1 RESOLVED (2026-07-07, from arXiv:2506.05259 directly — recon memo §⚠verify has
> the full record):** conjugation = a **single state-snapshot momentum flip** (Σ_z; optically =
> phase conjugation of the snapshot — the state-band reading CONFIRMED, (B)'s ceilings stand);
> **RHEL takes THREE passes/update** (forward + echo(+ε) + echo(−ε), symmetric finite
> difference of ∇_θH between the nudged echo trajectories) → **PR-7.1 amendment** corrects
> row 4 to 3 device passes/update and **C_op fires twice per update** (two independent
> conjugation events, fresh penalties each); inputs replayed time-reversed; **error = a
> continuous nudge force during each echo** → error-injection E/O channels are an envelope
> cost (S0.4-0 multi-tap class); RHEL is stated for non-dissipative systems only (the
> dissipative extrapolation is exactly what the bake-off measures).

---

## PR-3 — 🔒 FROZEN rule (2026-07-07) — the to-target rule + utility floor (F2.3, F10.2); ceiling number = measured addendum at S0.4-close

> **Status: 🔒 rule FROZEN 2026-07-07 (single-session mode, by the standing delegation —
> Lucas 2026-07-07: "ok then do now: S0.4-close — freeze the PR-3 to-target rule, measure the
> BPTT ceiling…"; review non-independent, disclosed). Registered BEFORE the ceiling pilot and
> before any C-2 estimator run.** The ceiling *number* follows the S0.4-0 pattern: rule frozen
> here → measured → recorded in the S0.4-close addendum below this block.

### A — Ceiling protocol
- **Ceiling = BPTT-on-substrate** (the PR-3 reference, never a contestant) at the registered
  cell, PR-6 θ₀/data/clamp conventions, S0.4a registered smoke HPs (equal-HP simplification,
  PR-8 §D). **8 seeds = {11, 23, 47, 61, 83, 101, 127, 151}** (registered; the sizing pilot
  runs seed 7, excluded from the 8). Train U_max updates (U_max from the pilot plateau,
  recorded in the addendum); **eval every 100 updates** on the FIXED reserved eval streams
  (harness `EVAL_SEED_BASE`, 2 batches × 8 seqs × T=256, warmup-trimmed — identical for every
  method and seed). **Final statistic = median over the last 3 eval points, per seed;
  ceiling SER = median over the 8 seeds (+ IQR).** No best-checkpoint selection (the G3
  lesson: best-val + collapse = silent stop).
- **Fixed-gain sensitivity spot (PR-7 §E feed):** 3 seeds {11, 23, 47} at `gain_mode="fixed"`,
  same protocol → **Δ_M3 = |median SER_sat − median SER_fixed|** recorded in the addendum
  (the M3-trigger margin PR-9 §D consumes).
- Eval device passes are **excluded from the budget B** (uniform diagnostic overhead;
  registered PR-8 §C convention).
- **Cells:** headline = **C-2/N=32** (foundry P-AN800 — the PF-F3 ≥1-foundry-feasible-cell
  requirement holds); C-1/N=8 secondary (same protocol, exploratory); C-3 deferred to the
  S0.5 sweep tier (registered, not silent).

### B — The to-target rule (feeds Gate ii-b; the "X%")
A method **reaches target** at a cell iff its eval-SER ≤ **SER_target = 1.25 × SER_ceiling +
0.005** at any registered eval point within the budget B. **Passes-to-target = the device-pass
count at the first eval point at/below SER_target** (linear no-interpolation: the eval grid is
the resolution). Runs that never reach target within B are **right-censored at B** (PR-8 §B).
The multiplicative 25 % margin + the 0.005 additive guard (degenerate-ceiling protection) are
both frozen before any C-2 estimator run.

### C — The utility floor (Gate ii-a)
- **Primary (relative, in-data): SER_ceiling ≤ 0.5 × SER_reservoir** — the readout-only
  (head-only) arm at the same cell, budget, and eval protocol, 8 seeds median. In-situ
  capacity must at least halve the readout-only error (the debt-#1 falsifier direction made a
  gate). Per PF-F3 (carried in verbatim): an ii-a miss at the foundry headline cell = the
  memory-vs-Q / Stage-1-reframing **finding**, not a bake-off failure.
- **Absolute record (report-only, never gate-bearing):** absolute SER + 4-PAM chance (0.75)
  recorded for the paper. No external absolute anchor (the G3 anchor-void lesson).

---

## PR-8 — 🔒 FROZEN (2026-07-07) — the statistical plan (F11)

> **Status: 🔒 FROZEN 2026-07-07 (single-session mode, by the standing delegation — same
> instruction as PR-3; disclosed). Registered before any gated bake-off run.**

### A — Seeds & arms
**8 seeds** {11, 23, 47, 61, 83, 101, 127, 151} for ALL arms at the headline cell (C-2).
**Ranked contestants:** PAT-both (the PR-5 headline family) · SPSA · adjoint · RHEL (honest
frozen chain). **References/baselines (never ranked):** BPTT (ceiling) · head-only
(reservoir) · offline-train-deploy (phase A = all-digital training on the M-par-family-wrong
offline model, U_off = U_max updates; deploy through the same-family actuation maps; phase B =
on-device head recalibration within B — the §10/F7.3 baseline). PAT mismatch decomposition
{perfect, M-par, M-struct} + rhel-ideal run at **C-1** (3 seeds, diagnostic tier — registered
scope bound, cost control).

### B — Right-censoring + rank
Per-arm per-seed outcome = (reached_target ∈ {0,1}, passes_to_target; censored at B).
**Lexicographic rank:** (1) success fraction within B (higher wins); (2) median
passes-to-target with censored runs counted at B⁺ (i.e. above every uncensored value).
**Paired-by-seed bootstrap** (10,000 resamples over the 8 seed indices) for the CI on
median-passes differences between arm pairs. **The digital side-ledger is co-reported always
and does NOT enter the rank** (resolving the fork PR-7 §B left to PR-9, under its binding
principle: no "most sample-efficient" claim without both ledgers shown).

### C — Budget B
**B (device passes, per arm per seed) = 2 × the pilot-observed BPTT convergence-equivalent,
expressed as U_B updates of a 2-pass method: B = 16·batch·U_B... concretely B = 2 × U_conv ×
16 passes** where U_conv = the pilot plateau update count (recorded in the S0.4-close addendum
BEFORE any estimator run). Conversion per PR-7/PR-7.1 rates at batch 8: PAT B/8 updates ·
SPSA & adjoint B/16 · RHEL B/32 · head-only & offline-phase-B B/8. Eval passes excluded
(PR-3 §A). Loss traces + eval traces archived per run.

### D — HP policy (equal, pre-registered)
The S0.4a registered smoke HPs for every method (lr_phys = 1e-3·κᵢ Adam, lr_head = 3e-2,
grad-clip 1.0, SPSA c = 0.01·κᵢ, RHEL ε_frac = 0.05): **zero per-method tuning = equal
budgets** (PR-6 §E's equal-HP-search satisfied degenerately; a genuine equal-budget HP search
is registered as an S0.5-full sensitivity tier, not silently skipped). One-sided SPSA
perturbations at the clamp boundary per PR-6.

---

## PR-9 — 🔒 FROZEN (2026-07-07) — Gate-ii semantics + promotion + M3 trigger (F10)

> **Status: 🔒 FROZEN 2026-07-07 (single-session mode, by the standing delegation; disclosed).
> Registered before any gated bake-off run. Folds the S0.4c protocol note (the R3b
> template-rule gap).**

- **Gate ii-a (capacity):** PR-3 §C — SER_ceiling ≤ 0.5 × SER_reservoir at C-2 (8-seed
  medians). Miss ⇒ the PF-F3 reframing finding.
- **Gate ii-b (trainability):** **PAT-both or SPSA** reaches the PR-3 §B target on **≥ 5 of 8
  seeds** at C-2 within B. **Only-adjoint/RHEL-pass ⇒ escalate-and-redesign** (not a pass) —
  unchanged.
- **The R3b fix (registered rule, from the S0.4c finding):** any per-method "trains /
  competitive / improves" statement — in gates, ranks, or prose — must be stated as the
  **readout-only differential** (vs the head-only arm at matched budget and eval protocol),
  never as absolute loss reduction. The S0.4c smoke's F22 label is re-derived under this rule
  at S0.5 (expected: template B).
- **Promotion ("clearly beats", toward a later hardware slot):** a candidate (adjoint/RHEL)
  is promoted only if, vs BOTH PAT-both and SPSA: **(a)** ≥ 25 % lower median passes-to-target
  AND the paired-bootstrap 95 % CI on the difference excludes zero, at ≥ equal success
  fraction; **or (b)** a strictly simpler F8 hardware ledger at non-inferior efficiency
  (CI-overlapping median passes). "Exactness" remains struck.
- **M3 trigger (PR-7 §E quantified):** the gain-model-class flag fires if the
  leader↔runner-up gap in median passes-to-target < **Δ_M3** (the fixed-vs-saturating ceiling
  sensitivity measured per PR-3 §A, recorded in the S0.4-close addendum before the bake-off).

---

## 🔒 S0.4-CLOSE ADDENDUM — measured sizing + ceiling numbers (2026-07-07; consumed by PR-3/8/9)

> Recorded per the S0.4-close spec sequence; each part committed BEFORE the runs it governs.

### Part 1 — sizing (pilot seed 7, EXCLUDED from the 8; committed before any C-2 estimator run)
- Pilot: BPTT @ C-2, 8000 updates, eval/100. Curve: SER 0.70 (head warm-up to ~700) → steady
  descent → **0.0010–0.0013 floor from ~5700 updates** (= 4–5 symbol errors on the 3840-symbol
  eval set — the quantization floor). The registered 1 %-relative plateau rule fires at
  **U_conv = 7900** (it saturates at the eval-quantization floor — noted: conservative, longer).
- **U_max = 12000 · B = 252,800 device passes.** Per-arm updates at batch 8 (PR-8 §C):
  PAT-both 31,600 · SPSA 15,800 · adjoint 15,800 · RHEL 7,900 · head-only 31,600 ·
  offline-deploy 31,600 (phase B; phase A digital U_off = 12,000).
- Sizing observation (feeds the paper): the S0.4a "C-2 barely moves in 100 updates" flag is
  confirmed ×50 — the headline cell needs ~5,000+ updates; smoke scale was ~2 % of convergence.
- Raw: `results/s0_5/{pilot_seed7.json,sizing.json}`.

### Part 2 — ceiling + Δ_M3 (measured 2026-07-07; committed BEFORE any contestant run)
- **Ceiling (C-2, 8 seeds, U_max=12000): SER = 0.00052 median** (7/8 seeds at 0.0005 = 2
  errors/3840 eval symbols — the quantization floor; 1 seed at 0.0008). IQR ≈ 0. **The frozen
  substrate + BPTT solves the headline cell.** C-1 ceiling = 0.0018 (8 seeds).
- **SER_target(C-2) = 1.25×0.00052 + 0.005 = 0.00565** (the additive guard dominates at a
  floor-level ceiling — by design). SER_target(C-1) = 0.00728.
- **Δ_M3 = 0.0** — the fixed-gain ceiling is identical (0.0005) to the saturating one: the
  gain-model class does not move the achievable ceiling at all, so it cannot flip the bake-off
  verdict → **M3 declared un-triggerable at this cell.** Honest note: PR-9's M3 wording
  compares a passes-gap to an SER-difference (a unit inconsistency registered by mistake);
  with Δ_M3 = 0 the intent resolves unambiguously regardless (zero sensitivity ⇒ no flip
  possible), and the wording is marked for repair if a nonzero Δ_M3 ever needs it.
- Raw: `results/s0_5/ceiling.json` + `results/s0_5/runs/bptt_*.json`.
