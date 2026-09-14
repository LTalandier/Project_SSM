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
| **PR-16** | Drift model (S0.9b) | before the S0.9b run | ⬜ **PROPOSED 2026-07-22** (block below; source `docs/s0_L/drift_research_2026-07-22.md`) | The **drift model** (magnitude 341 MHz/24h RW = σ(24h)≈24κᵢ at C-2, on δ; κ_ext secondary; gain/heater = flagged gaps) + **deploy-then-drift protocol** + **both correlation regimes** (common-mode / independent) + offline variants (head-recal / +global re-lock) + the per-regime advantage margin (offline ≥2× in-situ, CI excludes 0). Tests whether in-situ retraining beats a stale offline calibration — the §5.5 advantage axis. | §5.5, §10 |

*(PR-5 gained §E — mismatch-sensitivity sweep addendum, ⬜ PROPOSED 2026-07-22, block below — turns the offline-tie null into a curve; a sensitivity extension of the signed §C unification.)*

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

---

## PR-5 §E — ⬜ **PROPOSED addendum** (2026-07-22) — mismatch-sensitivity sweep (S0.9a): *turn the offline-tie null into a curve*

> **Context.** At the frozen 5%-class M-par level the offline-deploy baseline **tied** in-situ PAT
> (§5.5: 0.0010 vs 0.0008, statistically indistinguishable) — the honest null. PR-5 §C already
> registered that in-situ and offline draw their calibration error from *one* family; §E sweeps the
> **level** of that family to locate where (if anywhere) in-situ pulls away. This is a *sensitivity
> extension of an already-signed contrast*, not a new comparison — so it inherits PR-5's fairness.
> **Freeze before the S0.9a run; margins below are the load-bearing part for Lucas.**

### E.1 — the swept knob
A scalar **mismatch_scale m** multiplies the *deviation* of the five **calibration/actuation** M-par
terms only — `kappa_i_rel` (+0.05), `gamma_rel` (+0.05), `kext_actuation` (1±0.05), `mu_actuation`
(1∓0.05), `delta_offset_ki` (+0.05) — i.e. each becomes m× its frozen 5%-class deviation. The two
**debt-#3 gain-characterization** terms (`gain_factor_rel`=+0.10, `p_sat_rel`=−0.25) are **held at
their frozen S0.4-0 values** (already independently "loose"; scaling `p_sat_rel` past m≈3 is
unphysical). Grid: **m ∈ {1, 2, 3, 4, 6}** → 5/10/15/20/30 %-class characterization accuracy.

### E.2 — arms, protocol, statistics
- Two arms per level: **in-situ PAT-both** and **offline-deploy**, both with the *same* m applied to
  the *same* family (PR-5 §C unification holds at every level). C-2, **8 seeds** (PR-8 seed set),
  same budget B=252,800, same target rule (PR-3). Final SER = median-last-3-evals (PR-3 §A).
- BPTT is **not** re-run (its ceiling is m-independent — the substrate is unchanged; only each
  arm's *knowledge* of it degrades). Reservoir/head-only likewise unchanged.

### E.3 — registered hypothesis + the crossover margin (the deliverable)
- **Hypothesis (directional, pre-registered).** In-situ PAT's final SER stays near the ceiling as m
  grows (it adapts to the *true* device through physical passes); offline-deploy's final SER rises
  monotonically (its model is m× wronger and the actuation-map errors compound with no on-device
  correction of the recurrence). The two are tied at m=1 (known) and diverge with m.
- **"In-situ advantage demonstrated at level m" iff:** offline median SER ≥ **2×** in-situ median SER
  **AND** the paired-by-seed bootstrap (10k, PR-8) 95% CI of (offline − in-situ) SER excludes 0.
  Report the **smallest such m = m\***, and separately the smallest m at which **offline fails the
  target** (median > SER_target) while in-situ still passes.
- **Honest either-way outcome:** if no m in the grid triggers the margin, the registered conclusion
  is *"the offline-tie persists to 30%-class mismatch"* — a stronger, more surprising null than the
  single 5% point, reported as such. The sweep cannot fail to produce a publishable statement.

---

## PR-16 — ⬜ **PROPOSED** (2026-07-22) — the drift model + deploy-then-drift protocol (S0.9b): *does in-situ retraining beat a stale offline calibration?*

> **The advantage axis §5.5 named but could not test.** In-situ training's canonical justification is
> that a device *drifts* and a once-calibrated offline model goes stale, while on-device retraining
> tracks it. Our substrate was static, so the tie at fixed 5% mismatch left the advantage open. PR-16
> introduces a **literature-sourced drift model** and a **deploy-then-drift** protocol to test it.
> Sources: `docs/s0_L/drift_research_2026-07-22.md` (deep-research, 21 claims 3-0/2-1 verified).
> **Freeze before the S0.9b run.** The correlation regime (§16.3) is the crux and is registered as
> *both* bracketing cases so the result cannot be an artifact of a convenient choice.

### 16.1 — the drift magnitude (SiN-specific, measured)
- **Anchor: free-running SiN microcavity resonance drift ≈ 341 MHz std / 24 h** (temperature-
  stabilized lab; Dacha et al., Nat. Photonics 2025, arXiv:2506.21692; device Q≈3×10⁶, our C-2 is the
  same tens-of-MHz-linewidth regime). At C-2 (κ_i/2π ≈ 14.2 MHz) this is **σ(24 h) ≈ 24 κ_i** — a
  random walk (Allan deviation grows with τ ⇒ RW): **σ²(t) = D·t, D = (24 κ_i)²/24 h = 24 κ_i²/h**,
  so σ(1 min) ≈ 0.63 κ_i, σ(10 min) ≈ 2 κ_i. **Sub-linewidth staleness lasts only minutes
  free-running** — an aggressive, well-sourced clock.
- The primary drifting quantity is **δ_j (per-ring detuning)** — thermo-optic resonance shift, the
  dominant and best-sourced term (dn/dT(SiN)=2.45×10⁻⁵/K; 1.2–1.9 GHz/K resonance sensitivity).
  κ_ext drift (thermo-optic coupler shift) is a **secondary, smaller** term — registered OFF in the
  primary run, ON in one sensitivity row. Gain drift (Er aging/photodarkening) and heater hysteresis
  are **literature gaps** (no SiN data; §16.5) — **unquantified, flagged**, not in the primary model.

### 16.2 — the deploy-then-drift protocol
- **t=0:** both arms start from a converged model (in-situ: a PAT/SPSA-trained recurrence; offline:
  the offline-deploy arm's phase-A model deployed through actuation maps — exactly as in S0.5, at the
  frozen 5% M-par level so drift is the *only* new stressor).
- **Deployment steps k=1…K** (candidate **K=12**, spacing ~5 min ⇒ window ~1 h): each step applies a
  drift increment to δ (regime per §16.3), then each arm spends a **fixed per-step on-device budget b**
  (candidate **b = 4,000 device passes**) on its allowed response, then SER is evaluated on the
  reserved held-out streams (EVAL_SEED_BASE).
- **Allowed responses (the honest asymmetry):** *in-situ* retrains the recurrence {δ, κ_ext, μ} +
  head (SPSA and PAT both, reported separately). *Offline* gets **head-recalibration only** in the
  baseline variant, and **head-recal + a single global δ re-centering ("laser re-lock")** in the
  strong variant — the latter removes the common-mode component, so the strong-offline is a genuine
  competitor, not a straw man.

### 16.3 — correlation regime (the crux; BOTH registered)
All measured drift is single-cavity; the cross-ring correlation is unmeasured (open question). Register
both bracketing cases and report both:
- **Regime I — common-mode:** one Wiener increment Δ(t) added to *all* δ_j (whole-chip thermal
  wander). Largely removable by the strong-offline's global re-lock ⇒ the tie may *survive* here.
- **Regime II — independent:** an i.i.d. per-ring increment Δ_j(t) (local drift) ⇒ scrambles the
  coupled eigenstructure; head-recal and global re-lock cannot fix per-ring pole errors ⇒ in-situ is
  expected to pull away. **This is where the advantage, if real, appears.**
- (Optional Regime III — mixed, fraction ρ common — only if I/II bracket cleanly.)

### 16.4 — registered margin (per regime)
- **"In-situ advantage under drift demonstrated (regime R)" iff**, over the deployment window, the
  **time-integrated (mean-over-k) median SER** of in-situ ≤ SER_target **AND** strong-offline's
  ≥ **2×** in-situ's **AND** the paired-by-seed bootstrap 95% CI of (offline − in-situ) excludes 0.
- Report the full SER(k) trajectories, both offline variants, both regimes, 8 seeds. **Pre-registered
  expectation:** Regime II triggers the margin; Regime I does not (strong-offline re-lock absorbs it)
  — and *that contrast is itself the result*: in-situ's advantage is specifically against
  **uncorrelated** drift, exactly the component a global lock cannot catch.

### 16.5 — registered gaps (do not overclaim)
- **Er:SiN gain drift** (aging/photodarkening/pump-drift): **no SiN data exists** (both flagship
  amplifier papers are static; verified). Left **unmodeled**; a §8 sentence states a slow gain drift
  would add to the δ stressor and *only worsen offline* (direction favorable, magnitude unquantified).
- **Heater/actuator hysteresis + thermal-crosstalk stability:** no SiN datum; `pnn-multilayer`
  crosstalk is the only analogue. Left unmodeled in the primary; flagged.
- **σ_step calibration** from D=24κ_i²/h and the chosen spacing is a **computation** addended at build
  (the E₀/ceiling pattern — no invented numbers in the headline).

### 16.6 — build + cost
New: a `drift_schedule` capability on the substrate (per-step δ increment, regime flag, RNG-seeded),
a harness `deploy-then-drift` protocol wrapping the existing arms, and gate tests (RW variance grows
∝t to the target σ(24h); common-mode ⟂ independent separated; zero-drift ≡ S0.5). Runs: C-2, 8 seeds,
2 regimes × 2 offline variants × {PAT, SPSA} in-situ + K=12 steps — an S0.6-scale cloud sweep (est.
few €). **Pre-register (commit this block) → build + smoke → Lucas ratifies margins → run.**

### 16.7 — BUILD ADDENDUM (2026-07-24): σ_step frozen; margins ratified by Lucas
- **σ_step = 0.40 κ_i/step FROZEN** (Lucas ratify 2026-07-24, "finer drift steps" — gradual
  resolvable curve over a cliff). With **K=12**: per-step increment 0.40 κ_i, **accumulated
  σ(window) = 0.40·√12 ≈ 1.39 κ_i** (RW). Nominal real-time mapping via D=24 κ_i²/h ⇒ ~24 s/step;
  **primary axis = accumulated drift (κ_i), elapsed-time secondary** — the short-time (s–min) drift
  PSD is an open question (research memo Q2), so we do not over-claim the wall-clock rate.
- **b_updates = 4,000/step** (fair per-step budget, both arms); **n_converge = 20,000** (insitu-pat,
  offline arms) / **15,800** (insitu-spsa) so t=0 sits at the S0.5 converged state (ser0 validates
  against S0.5 finals: pat 0.0008, offline 0.0010, spsa 0.0026).
- **Margins RATIFIED as written** (Lucas 2026-07-24): S0.9a and S0.9b both use the **2× advantage
  factor + CI-excludes-0**; grids as registered (m∈{1,2,3,4,6}; regimes common/independent; offline
  head/relock; {pat,spsa} in-situ). This addendum is committed BEFORE the runs it governs.

## PR-17 — ⬜ **PROPOSED** (2026-07-27) — S0.10: fine-grained evaluation (eval-F) + damping-transfer task (T-A-L). Committed BEFORE the runs it governs.

**Origin:** PI review of the assembled manuscript (Lucas, 2026-07-27): (1) the 3840-symbol eval
floor (per-seed resolution 2.6×10⁻⁴) is too coarse for the near-ceiling comparisons — the §5.5
tie, the 1.84× drift ratio, and the §5.6 decomposition all live inside a two-symbol-error band;
(2) §6's "excess memory is harmful" is near-tautological with a single 7-tap task — a
longer-span task showing the damping optimum *move* turns it into a claim.

### 17.1 eval-F protocol
`eval_ser(n_batches=52)`: the same reserved held-out construction (EVAL_SEED_BASE stream
families, never trained), extended from the frozen j∈{0,1} to j∈{0..51} → 52×8×240 = **99,840
scored symbols per evaluation; per-seed resolution 1.002×10⁻⁵** (26× finer). No change to any
training stream, budget, or seed.

### 17.2 Re-evaluated units (frozen specs replicated VERBATIM; only the reported evaluation is finer)
- **a-fine (80):** the S0.9a command lines of `results/s0_9/shard_*.txt` exactly (methods
  {pat-both, offline-deploy} × m∈{1,2,3,4,6} × the 8 frozen seeds × n_up=31,600), + one eval-F
  final evaluation on the trained state.
- **b-fine (64):** the S0.9b units exactly (PR-16 §16.7 frozen: σ_step=0.40κᵢ, K=12, b=4000,
  n_converge 20,000/15,800), with ser0 and all K per-step evaluations at eval-F
  (y_scale re-measured on the current drifted device before each evaluation, as ser0 does).
- **diag-fine (12):** the S0.5 C-1 diagnostic units exactly ({pat-perfect, pat-M-par,
  pat-M-struct} × 31,600 + rhel-ideal × 7,900; seeds {11,23,47}), + eval-F final.
- **ceiling-fine (8):** BPTT C-2 saturating, seeds {11,23,47,61,83,101,127,151} × 12,000
  updates (the frozen ceiling protocol), + eval-F final. **Diagnostic reference only** — the
  pre-registered target SER_target = 5.65×10⁻³ and every gate/rank verdict remain defined on
  the frozen coarse protocol and are NOT recomputed.

### 17.3 Rules of record
Coarse (3840-symbol) numbers remain the numbers of record for every pre-registered gate,
target, and ranking (PR-8/PR-9 untouched). **eval-F becomes the protocol of record for the
near-ceiling comparisons only**: §5.5 (S0.9a/b, Fig. F8), §5.6 (Fig. S2), and S0.10b. The
S0.9 verdict rules are re-applied VERBATIM at eval-F (advantage iff ≥2× and paired-bootstrap
CI excludes 0; time-integrated mean-over-K median metric). **If any coarse and fine verdict
differ, BOTH are reported in the paper.**

### 17.4 T-A-L task definition (frozen here)
T-A-L = the frozen T-A Jaeger–Haas channel (PR-2: same 4-PAM alphabet, same nonlinearity, same
SNR 28 dB, same target d(n−2)) **plus a −6 dB replica of its past-tap profile delayed by 7
symbols** (a second reflection): c_L[k] = c[k] for k ≤ 7, and c_L[7+m] = 0.5·c[m] for
m = 1..7, i.e. frozen added taps {8: +0.09, 9: −0.05, 10: +0.0455, 11: −0.025, 12: +0.02,
13: +0.015, 14: +0.005}. Memory span: 7 → 14 past symbols. WARMUP=16 still covers the
transient (14+2 = 16 ≤ 16). Implementation: `taps` override threaded through
`make_ta_dataset`; default `None` = bit-identical frozen T-A (gate test).

### 17.5 S0.10b sweep design + registered prediction
Pinned arm only, BPTT (exact gradient — locates the optimum without estimator noise), C-2,
r ∈ {0.2, 0.3, 0.5, 1.0, 2.0, 3.0} (the S0.6 grid), seeds {11,23,47,61,83,101,127,151},
U_MAX = 12,000, S0.6 plateau flag verbatim, final evaluation at eval-F. **Registered
prediction: the T-A-L damping optimum moves to lighter damping (r*_L < 2.0).** Claim-upgrade
rule (frozen): §6 gains the transfer claim iff, over plateaued points, the T-A-L minimizer
r*_L ≠ 2.0 AND median SER at r*_L < 0.7 × median SER at r = 2.0 on T-A-L (a 30% separation);
otherwise the §6 wording stays and the null is reported. (The T-A curve at these r is already
on record from S0.6 — no rerun.)

### 17.6 Budget
212 units, 3×cpx51-class, expected ≲7 h, ≲€2 (same envelope class as S0.9; servers deleted
after; single-threaded workers, OMP/MKL/OPENBLAS=1).

### 17.7 ERRATUM (2026-07-28, registered before the rerun it governs)
The first S0.10 execution (212/212 units, servers deleted) exposed an **implementation bug in
the eval-F helper**: it re-measured the intensity normalization y_scale on the *trained*
device, while the head was trained against the *training-time* y_scale — the head and its
scale are one decoder. Every arm that materially moves κ_ext (PAT, free BPTT, RHEL-ideal, and
underdamped T-A-L points) therefore returned chance-level fine SER while its coarse SER sat
at ceiling (the coarse numbers, S0.9-identical, prove training was intact). **Valid and kept
as registered:** all runs_b drift units (the per-step re-measure is the registered ser0
convention and tracks a near-unchanged device; fine tints match coarse within 10–20%) and the
runs_a offline-deploy arm (its head is recalibrated against the deploy-time re-measured scale
— the same quantity). **Invalid and rerun under the fixed decoder-consistent eval** (train()
now exposes `y_scale`; gate test: eval at the trained scale reproduces the trace eval to
<1e-12): a-fine pat-both (40), diag-fine (12), ceiling-fine (8), talong (48) = 108 units.
No frozen spec, seed, budget, or verdict rule changes — only the evaluation-scale convention
is corrected to the one every training-time eval already used.

### 17.8 Round-3 review addenda (2026-08-01, registered before the run below)

**(a) Resolution-vs-re-draw decomposition — analysis-only disclosure (stored data, no new
runs).** External review asked whether the coarse→fine movement of the drift verdict
(1.84×→2.42×) confounds the finer evaluation floor with a fresh noise draw. Checked against
stored outputs: the S0.10 reruns are **bit-identical reproductions** of the S0.9 trajectories,
not re-draws — the device-state fingerprint (`delta_rms_ki`, eval-independent) matches the
S0.9b files exactly on **64/64 drift units**, and the fresh coarse `final_ser` matches the
S0.9a values exactly on **80/80 mismatch units** (dynamics are deterministic given the
registered seed; eval draws from reserved streams that do not touch the training RNG; the
coarse symbol set is the j∈{0,1} subset of the fine j∈{0..51} set). The coarse→fine movement
therefore carries exactly one factor: the evaluation floor. This holds symmetrically for the
F8a dissolution (in-situ-favoring edge erased) and the F8c resolution (advantage declared).

**(b) Matched-budget reference (kind `ceiling_matched`) — spec.** The §5.1 BPTT reference is
protocol-local: it runs the bake-off budget (12,000 updates) while the §5.5 follow-up arms run
the PR-5 §E sweep budget (31,600 updates); at eval-F the arms' point medians sit below the
12k reference (paired (ref−arm) median +1.65×10⁻⁴, 95% CI [−0.10, +3.10]×10⁻⁴ — includes 0).
To give the follow-ups a same-protocol reference: **BPTT, C-2, n_updates=31,600, eval_every
=100, seeds {11,23,47,61,83,101,127,151}, coarse + eval-F both reported.** Consumed by no
gate or verdict; purpose = §5.1 scope disclosure + the F8 reference line. Review-added
diagnostic, disclosed as such. Falsifiable expectation: the matched reference lands at or
below the 12k reference, in or below the arms' 8.4–9.0×10⁻⁴ band; if it lands *above* the
arms, the budget explanation is wrong and §5.1 must say so.

---

## PR-18 — 🔒 REGISTERED (2026-08-04, single-session mode; pre-run) — converged-operating-point diagnostics (S0.11)

> Round-5 walkthrough (external-review conversation, 2026-08-04) crossed §5.7 with §6: the
> controllability gate and participation profile were resolved **at θ₀** (r₀=0.3, μ_c=0.3κᵢ,
> κ_net=0.7κᵢ), while the trained solutions live elsewhere (§6 pinned optimum r\*=2.0,
> κ_net≈4.1κᵢ; boxed winners heterogeneous). A per-hop gradient-attenuation model
> (μ/κ_net)^(2·hops) predicts the θ₀ gate profile within ~25% and predicts collapse
> (~8×10⁻¹⁰ ≪ 10⁻³ at 4 hops) at the pinned optimum **if μ stays at init** — whether training
> repairs its own controllability (via μ growth and/or profile heterogeneity) or converges
> with most rings gradient-dark is unmeasured. Also unmeasured: anchor-risk (vii) at the
> achieved solutions. This block freezes the diagnostics + interpretation rules **before any
> measurement is computed**.

### 18.1 Targets (all four reported regardless of outcome; no selective reporting)
Deterministic state-capture reproductions (`train(...)` identical registered args +
`return_state=True`) of stored converged runs, seeds {11,23,47,61,83,101,127,151}:
- **pinned2** — S0.6 arm B at r\*=2.0: `train("bptt","C-2",seed,12000,eval_every=100,r0=2.0,pin_kext=True)`
- **boxed3** — S0.6 arm A widest box: `train("bptt","C-2",seed,12000,eval_every=100,r0=√(0.1606·3.0),r_hi=3.0)`
- **patC2** — bake-off gate-ii route: `train("pat-both","C-2",seed,31600,eval_every=100)`
- **spsaC2** — bake-off gate-ii route: `train("spsa","C-2",seed,15800,eval_every=100)`
Stage order: {pinned2, boxed3} then {patC2, spsaC2}. Local CPU only (≈15 core-hours, €0).

### 18.2 Reproduction gate (before any measurement is read)
Primary: **bit-identity** vs the stored JSON — `eval_trace` exact, `final_ser` exact
(+ `final_r` exact where stored). Fallback (if cross-platform float drift breaks bit-identity):
protocol-identical reproduction; the deviation is reported per unit and every downstream
number is then labelled *reproduced-solution*, not *stored-solution*. Fingerprint verdict
recorded per unit.

### 18.3 Measurements (verbatim S0.4-0 protocol, on the converged device)
On the returned trained substrate with `ase_variance_scale=0` (the registered noiseless
calibration convention; device identity, disorder seed, taps, and trained {δ, κ_ext, μ}
untouched):
- **(i) Gradient gate at solution:** per-ring |∂L/∂δ_j| ratio-to-max, **min over the recorded
  drive seeds {7,19,41,101,271}**, loss `mse_zero` primary / `mse_target` co-reported,
  GATE_RATIO 10⁻³ — the S0.4-0 §B functions unmodified. Report count ≥ gate, worst ratio,
  full per-ring profile.
- **(ii) Participation at solution:** `participation_profile` counts ≥ {10⁻¹, 10⁻², 10⁻³}.
- **(iii) Converged parameters:** per-ring r_j, δ_j/κᵢ, per-link μ_j/κᵢ (init references:
  μ_c=0.3κᵢ; r₀ per arm), per-ring operating κ_net,j/κᵢ.
- **(iv) vii endpoint row:** hypothetical δ-aware de-saturation at the **achieved** (δ_j, r_j)
  — the S0.4-0 Item-3 Lorentzian convention (passive κ_tot in the build-up, the substrate's
  own gain model g₀/P_sat): κ_net^δ-aware_j = κᵢ − g₀/(1+P̄(δ_j,r_j)/P_sat) + 2κ_ext,j.
  Primary: min over rings at achieved δ_j. Secondary: min over the δ∈[−κᵢ,κᵢ] band at
  achieved r_j.

### 18.4 Interpretation rules (frozen now)
On the 8-seed **median count ≥ 10⁻³ (measurement i)** per target set:
- **maintained** ≥ 30/32 → §5.7 gains one sentence stating the at-solution check passed;
- **collapsed** ≤ 16/32 → the "N = 32 carries the measured profile" rule extends to
  solutions: §5.7 gains an at-solution paragraph, §7.2's N-scaling niche argument gains a
  caveat, and §5.2's *interpretation* sentence is softened (the gate itself is SER-based and
  unaffected);
- intermediate → reported as measured, no verdict word.
Mechanism readings (not mutually exclusive; all stats reported regardless): *repair-by-μ* iff
median converged μ ≥ 2μ_c; *repair-by-profile* iff the gate holds without μ-repair and the
converged r profile is non-uniform (sd(r_j) > 0.15); *dark-but-converged* iff a set trains to
its stored SER while collapsed — reported as a finding (most parameters received no usable
gradient by convergence), not explained away.
**vii endpoint rule:** min over {sets, seeds, rings} of κ_net^δ-aware at achieved (δ_j, r_j)
> 0 → §3.6/§8.2 add the empirical note that trained endpoints never enter the exposed corner
(worst margin quoted; *endpoint* closure only — mid-training trajectories are not stored and
stay open); ≤ 0 → vii is a measured at-solution exposure and §3.6/§8.2 must say so.

### 18.5 Consumption
Consumed by: §5.7 (at-solution paragraph or sentence), §6 (mechanism sentence), §3.6/§8.2
(vii note), the round-5 walkthrough record. Gates/verdicts of §5.2–§5.5 are not re-scored by
this block.

### 18.6 Round-5 reviewer follow-ups (2026-08-05, registered pre-run)

External review raised two readings the 18.1–18.4 data cannot separate, and one metric
mismatch. Motivating stored-data context (zero compute, computed pre-registration): across
boxed_{0.5,1.0,2.0,3.0} the interior median sits within 0.002 of *its own arm's init*
(0.281/0.403/0.569/0.695 vs r₀ = 0.283/0.401/0.567/0.694) while tap rings saturate at
≈ 1.26–1.31 wherever the box allows (clipped at the box ceiling for r_hi ≤ 1.0); SER tracks
the tap damping. "Interior never moves off init anywhere" is what *both* readings predict.

**(a) Taps-only training control — "discovers" vs "starved".** Reading A: training discovers
damp-the-driven-rings with a transparent interior. Reading B: training moves only what it has
gradient on; the interior profile is inherited, not chosen. Control run: `pat-both`, C-2,
31,600 updates, eval_every=100, seeds {11,23,47,61,83,101,127,151}, trainable partition
restricted to the four driven rings' {δ_j, κ_ext,j} (gradient-masked to taps {3,12,21,30};
ALL μ and all interior δ/κ_ext pinned at init; head trains normally; clamp unchanged).
**Frozen rule:** reading A (and the word "discovers") is earned iff full-partition patC2
beats taps-only with paired-by-seed bootstrap 95% CI of (SER_tapsonly − SER_full) excluding
zero **at eval-F** (the near-ceiling comparison protocol; coarse co-reported). If the CI
includes zero → reading B adopted in prose: the abstract clause (pulled in this commit,
pending this rule) STAYS OUT, and §5.7/§6 state the split finding — tap damping is trained
(box-independent saturation ≈ 1.3), the interior profile is inherited from initialization.
If the CI excludes zero → the abstract clause returns with **"estimator-independent"**
replacing "universal" (the measured scope: three estimators, one task, one cell, one
topology). Taps-only converged tap-parameters are co-reported (do taps still ride to ≈1.3?).

**(b) N_eff readout ablation — §7.2's actual metric.** Gradient-aliveness (18.3-i) answers
trainability; §7.2's N-scaling argument needs *output participation* (a ring at 10⁻³ of max
amplitude contributes ~10⁻⁶ to y = |Σc_j a_j|²). On each stored winning-route solution
(patC2, spsaC2 × 8 seeds): rank rings by ascending |c_j|·ā_j (ā_j = settled CW amplitude,
the S0.4-0 participation convention), zero readout entries c_j cumulatively in that order
(device dynamics untouched; decoder frozen: trained head + trained y_scale, the §17.7
one-decoder rule), evaluate coarse SER (protocol of record) at each k. **N_drop\* = max k
with SER ≤ SER_target = 5.65×10⁻³; N_eff = 32 − N_drop\*.** One robustness row: at
k = N_drop\*+1, retrain the head only (2,000 Adam updates, lr_head = 3e-2, standard stream)
and report whether target is recovered. Consumption: §7.2 gains one sentence quoting median
N_eff and range, whatever they are (no verdict rule — the integer is the deliverable);
§5.7 one clause. The §7.2 "≥30/32 gradient-alive" defense is NOT added (wrong metric).

**(c) State serialization.** Every 18.6 unit writes the full converged device+decoder state
(δ, κ_ext, μ, c_readout, head state, y_scale) to `results/s0_11/states/` so future
diagnostics never re-train these solutions again. Reproduction gate unchanged (§18.2).

---

## PR-19 — 🔒 **SIGNED** (2026-08-13, Lucas: "sign PR-19") — long-coherent-memory task T-D (S0.12)

> **Status history:** PROPOSED-FOR-SIGNATURE 2026-08-13 (`d473437`, from the PI-approved
> STEP-1 candidates memo, T-D chosen "go T-D") → **SIGNED same day, no edits between
> proposal and signature.** Pilot (§19.6) authorized; fleet still gated on the pilot's
> wall-clock projection being reported to the PI.

> **Provenance:** proposed at external review (round-6 prompt, 2026-08-13); the discharge
> path for the N_eff finding (PR-18 §18.6b, consumed in §7.2). Builds on the PR-18
> taps-only and readout-ablation controls. Task chosen by PI from the STEP-1 candidates
> memo (`docs/s0_12/pr19_task_candidates.md`): **T-D**, unipolar despread-31. Nothing in
> this block runs before PI signature; the seed-7 pilot (§19.6) runs first and its
> wall-clock projection is reported before any fleet.

### 19.1 Task T-D (frozen)
Source = the frozen T-A 4-PAM alphabet and statistics. Each symbol $s_k$ is spread over
**L = 31 chips** at the sample rate (2 GS/s; chip = sample; symbol rate 64.5 MS/s) by the
fixed m-sequence from primitive polynomial $x^5+x^2+1$ over GF(2), initial state 11111
(chips $c_l \in \{0,1\}$, weight 16, fully determined). **Unipolar map, no new encoder
levels:** chip amplitude $x[n] = a(s_k)$ if $c_{l(n)}=1$ else $a(0)$, with $a(\cdot)$ the
frozen 4-PAM amplitude map, $l(n) = n \bmod 31$ aligned to symbol boundaries. Channel =
the frozen T-A 7-tap ISI at 28 dB, applied at chip rate, unchanged. Decision positions =
last chip of each symbol ($l = 30$); loss = MSE to the symbol level at decision positions
(masked elsewhere); SER scored per symbol. Episode = **64 symbols = 1,984 chips**
(WARMUP = 2 symbols); batch 8 → 496 scored symbols/pass. Protocols: **coarse = 3,968
scored symbols (8 eval passes), eval-F = 100,192 (202)** — the PR-3/PR-17 floor logic
transfers with these counts. Realizability row: span 31 chips = 15.5 ns ≤ max amplitude
memory ≈ 53 chips at the light edge of the registered box (κ_net ≈ 0.42κᵢ at r_min) —
the box contains the regime the task demands; θ₀ memory ≈ 32 chips sits at the span.

### 19.2 Cell, seeds, arms
C-2, seeds {11,23,47,61,83,101,127,151}; **pilot seed 7 excluded from scoring**. Arms:
(i) **pinned-damping sweep** (§6 protocol verbatim): BPTT, r ∈ {0.2, 0.3, 0.5, 1.0, 2.0,
3.0}, plateau flag as S0.6 — measures the T-D optimum $r^*_D$; (ii) **BPTT free-partition
reference** — the on-task ceiling, run at the same update budget as (iii) (the §5.1
matched-budget scope convention, no protocol-local mismatch by construction);
(iii) **PAT (pat-both, full partition)** — the demonstration route. No four-method
re-run (task-property question, not a method question). Substrate constructor, fairness
contract, noise conventions: PR-6 verbatim.

### 19.3 Target rule
PR-3 form, mechanical: $\text{SER}_\text{target} = 1.25 \times \text{ceiling}_{TD} +
0.005$, ceiling = arm-(ii) 8-seed median at the coarse protocol of record (eval-F
co-reported). The ceiling addendum commits before any to-target statistic is final
(the S0.4-close pattern). U_MAX and budget set by the pilot (§19.6) and addended
pre-fleet.

### 19.4 Registered joint prediction + decision rules (frozen now)
**One mechanism, two observables.** Memory ≥ 31 chips requires κ_net ≲ 1.0 κᵢ, and by the
per-hop gradient mechanism (μ/κ_net)^(2·hops) the same move raises gradient reach — so a
lighter optimum and a higher N_eff are the *same* prediction:
- **P1 (damping):** $r^*_D \leq 1.0$. Upgrade rule (§17.5 form): over plateaued points,
  the T-D minimizer satisfies $r^*_D \leq 1.0$ AND median SER at $r^*_D$ < 0.7 × median
  SER at r = 2.0. Fails → reported failed; with T-A-L that is the two-probes-no-movement
  pattern, stated as such (T-A-L's head-reach confound is removed here: span 31 ≫ the
  8-lag head).
- **P2 (N_eff, measured on arm-(iii) solutions by the §18.6b path VERBATIM — ascending
  $|c_j|\bar a_j$ zeroing, frozen decoder, target-crossing integer, 2,000-update
  head-refit row):** **rise** iff median N_eff ≥ 16; **no-rise** iff ≤ 10; 11–15 =
  intermediate, reported as measured, no verdict word. T-A comparator: 6–8.
- **P0 (solvability):** if arm-(ii) BPTT fails target at every damping point, T-D is
  unsolvable on this architecture — consumed as the architectural negative below, and
  P1/P2 are moot (reported as such, not silently dropped).

### 19.5 Consumption texts (pre-written; the applicable one is inserted verbatim-modulo-numbers)
- **RISE →** §7.2: "On the registered long-coherent-memory task the deployed function
  rides on N_eff = ⟨X⟩ of 32 (vs 6–8 on equalization): the N-scaling premise is back on
  measured ground for workloads of this class, and the niche verdict's state-dimension
  condition is discharged where the niche needs it." §6: second data point per P1's own
  outcome. §8.5: scope narrowed accordingly.
- **NO-RISE (task passes, N_eff ≤ 10) →** §7.2: "A second task family engineered to need
  long coherent memory still concentrates its output on ≤10 of 32 rings. The ~15× at
  N = 128 was computed against a baseline priced at nominal N; a baseline built to the
  function would shrink by roughly the same factor — **the advantage is unmeasured in
  magnitude, not merely conditional.**" (Not softened.) §6/§8.5 per P1's outcome.
- **UNSOLVABLE (P0) →** §7.2 + §8.5: "A nearest-neighbor coupled-ring chain could not
  realize the flat-spectrum length-31 kernel at any damping in the registered box — a
  measured architectural limit of the chain topology for long-coherent-memory workloads;
  parallel-bank and non-chain topologies are the untested alternative." §6: P1 moot,
  stated.
- Intermediate N_eff (11–15) → numbers quoted in §7.2 with no verdict word; both
  neighboring texts' claims withheld.

### 19.6 Pilot + sizing (runs only after signature)
Seed 7 (excluded): solvability probe at light damping (BPTT), convergence flatness →
U_MAX (×1.5 margin, S0.4-close form), per-unit wall-clock at the ×7.75 chips-per-pass
cost. **Projection reported to the PI before any fleet commits** (compute-spend
escalation rules apply if cloud is proposed). Fleet: 6×8 pinned + 8 ceiling + 8 PAT = 56
units + pilot. All states serialized (§18.6c); N_eff code path reused verbatim.

### 🔒 19.6a PILOT ADDENDUM (2026-08-14; measured, committed pre-fleet)
Evidence: `results/s0_12/pilot_seed7.json` (BPTT free, seed 7, U = 12,000).
- **P0 (solvability): PASSES emphatically** — SER 0 at 1,000 updates' next eval
  (2.5×10⁻⁴ at 1,000 → 0 from 2,000 on), **zero errors in the full 100,192-symbol eval-F**.
- **U_MAX = 3,000** (flatness from ~2,000; ×1.5 margin, S0.4-close form). All arms
  (pinned sweep, ceiling, PAT) run U = 3,000, eval_every = 100.
- **Measured rate** (probe + pilot CPU-time consistent): ≈ 4.25 s/update single-threaded
  → ≈ 3.6 h/unit at U_MAX; 64 units ≈ 230 core-hours. (The naive ×7.75 chips estimate
  under-priced the autograd-depth cost; measured ×~70 vs T-A.)
- **Floor disclosure, pre-fleet:** despreading's ~16-chip integration gain makes the frozen
  28 dB trivially clean — the T-D ceiling will sit at or near SER 0, so §19.4-P1's
  minimizer will be a **degenerate all-zero plateau on the light side** (the rule can still
  fire via the heavy-side contrast, and is reported as floor-degenerate if it does);
  §19.4-P2 (N_eff vs the mechanical target) is unaffected — the ablation crossing is
  measured against SER_target = 1.25×ceiling + 0.005 ≥ 0.005 regardless. Any harder-SNR
  sensitivity row is a separate registration if proposed after the sweep; none is
  registered now.
- **Pilot profile note (context, 1 seed, ungated):** the converged free-BPTT solution
  stays at near-init damping — taps r ≈ 0.31–0.37, interior ≈ 0.30 — i.e. the T-A
  tap-heavy structure (taps → 1.3) does NOT appear on T-D; the actuator structure is
  task-dependent. The sweep and PAT arms decide P1/P2; this note pre-registers no verdict.

### 🔒 19.6b CEILING ADDENDUM (2026-08-17; committed before any to-target statistic)
Arm-(ii) BPTT free, 8 seeds: **ceiling_TD = 0.000** at the coarse protocol of record
(0.000 at eval-F as well — zero errors in 8 × 100,192 symbols). Mechanically:
$\text{SER}_\text{target} = 1.25 \times 0.000 + 0.005 = \mathbf{5.00\times10^{-3}}$ (the
additive guard alone, PR-3 §B by design). Floor context (extends the §19.6a disclosure):
at the frozen 28 dB the task is easy *everywhere on the grid* — even the heaviest pin
(r = 3.0, ~5-sample memory) reads 0 at eval-F, since partial-correlation gain at this SNR
still clears any measurable floor. Both P1's grid and P2's crossing are therefore
floor-dominated; verdicts are applied exactly as frozen, with this scope stated wherever
they are consumed.

### 🔒 19.6c ROUND-7 AMENDMENT (2026-08-17; post-consumption, review-driven — frozen blocks above untouched)
The round-7 external review found the §19.5 NO-RISE text's evidentiary frame ("still
concentrates its output on ≤10 of 32 rings") degenerate under the §19.6a/b floor: on a
task solved with ~16-chip integration margin at every grid point, the §18.6b ablation
crossing measures task slack, not substrate utilization — a small N_eff is guaranteed by
the margin regardless of concentration (internal demonstration: the T-D head-refit
recovers target from 3 rings where T-A's recovers nothing, 0/15 — same procedure,
opposite outcome). §19.6a's "P2 is unaffected" holds only mechanically (the crossing
integer is well-defined); its reading as concentration evidence does not survive the
floor, and §19.6b's "scope stated wherever consumed" was insufficient where the frozen
sentence itself asserted that reading. Amendments (applied text only): §7.2 drops the
"still concentrates" clause and states PR-19 is evidence-free on N_eff in either
direction (the informative measurement remains §18.6b's 6–8 on T-A); §6 inverts to
floor-explanation-first (the §19.6a pilot-note phrase "task-dependent" is bounded the
same way) and re-counts damping-tracks-memory as zero-for-two genuine tests (T-A-L
informative null, T-D degenerate; T-A is the generating observation — matching
§19.4-P1's own "two-probes" framing), not zero-for-three. Standing unchanged: the P2
branch rule and its mechanical firing (median N_eff = 4 ≤ 10 → no-rise), the P1
failed-by-degeneracy verdict, the unsoftened "unmeasured in magnitude, not merely
conditional" sentence, and the burden-flip. Same root, derived artifacts: round-5-
corrected values had persisted inside rendered figure annotations (F6 label ≈5.5
samples → ≈6 at measured 3.7 κᵢ; S5 in-image title ≈27 → C-2 ≈8; F7 caption "all-in" →
budgeted-stack scope); regenerated with this amendment.

---

## PR-20 — 🔒 **FROZEN** (2026-09-13, single-session mode; committed BEFORE `analysis/s0b_0_envelope.py` runs) — S0b.0 inline-scope re-envelope + Stage-0b verdict rule

**Governs:** S0b.0 (`shared/stage0b_roadmap.md`), the kill gate of Stage 0b, and the verdict rule reused
at S0b.4. **Source rows:** `docs/s0b/s0b_0_ledger.md` (retrieved and statused 2026-09-13) + the PR-10
frozen rows it re-uses. Arithmetic only — no simulation. Lucas's approval: E-2026-09-13-1 ("Ok go").

### 20.1 Scope: inline receiver stage
- The signal is already optical at the device input: **E/O in = 0**; the transmitter's laser and
  modulator are the link's (stated, not hidden).
- **Shared stages cancel on both sides:** photodiode + TIA + ADC are paid by the digital receiver
  whether or not the photonic stage exists; charged only if the photonic stage forces a different ADC
  (rate/ENOB) — not the case for a same-rate LTI filter; row carried at 0 with the condition stated.
- **Comparison object:** photonic-stage static + maintenance power ÷ line rate, vs the digital
  equalizer *block* it replaces, priced per tap. Everything else is shared (cancels) or the link's.
- Line-rate window: the S0.1 registered 0.1–2 GS/s (grid {0.1, 1, 2} GS/s, unchanged from S0.7).

### 20.2 What the photonic stage pays (all rows charged; ledger row in brackets)
1. **Actuator hold per control channel** × N × CH_PER_RING (PR-10: 2 OPT / 4 CONS):
   A = 60/175 + 2 mW; B = 1 + 2 mW; **C-pz** = 0.1 (OPT, UNSOURCED) / 2 (CONS, frozen DAC row) mW
   + 20–300 nW actuator [§1C-pz]; **C-pcm** = 0 (non-volatile; write electronics off at inference —
   retention not quantified, flagged) [§1C-pcm]; **hybrid** = 4 driven rings C-pz + the rest C-pcm
   (P1 §5.7: only the taps move).
2. **Drift management (the locking exclusion, charged):** common-mode option ∈ {TEC 180 mW [§3,
   VERIFIED]; global heater 10/50 mW [§3, UNSOURCED]; actuator-tracked lock 1.3/13 mW [§3, duty
   UNSOURCED; classes A, B, C-pz only — C-pcm and hybrid cannot track continuous drift]} **plus** the
   uncorrelated residual by **periodic retraining** at cadence T_r ∈ {1, 10, 100, 1000} s:
   P = E_ep/T_r + 0.13 W × 22.5 ms/T_r, E_ep = 2.6 / 99 mJ (§7.3 SPSA stack) [§3]. Default cell
   T_r = 100 s (the drift anchor gives ≈ 1 h per C-2 linewidth); the ladder is reported.
3. **Gain pump (the fifth unbudgeted item):** configuration **passive** (undoped rings, g = 0, the
   model's own passive variant; pump = 0) vs **pumped** (0.8/17 mW electrical per ring + 0/180 mW
   pump-module TEC) [§2, derived from two UNSOURCED inputs]. Passive is the product configuration;
   pumped is reported.
4. **Control compute at inference:** 0 unless a lock/retrain loop runs (then inside rows 2).
5. **Packaging:** insertion-loss co-condition 0.3 (OPT) / 3.0 (CONS) dB, two facets [§4]; a cell that
   clears on energy with > 3 dB is "clears-with-loss-penalty", never "clears".

### 20.3 Digital block, priced to the function
- E_digital = N_taps × e_tap, **e_tap = 0.05 (OPT) / 0.15 (CONS) pJ per tap per sample** [§5, the
  load-bearing row: Credo 802.3ck TX-FIR 0.075 and RX-FFE/DFE 0.10 pJ/tap/sample, Horowitz-scaled
  floor 0.02–0.06]; sensitivity band [0.03, 0.25].
- N_taps grid {4, 8, 16, 32, 64, 128}; the P1 point (7-tap task, N_eff 6–8) is marked at 8.
- Secondary rows for continuity only: Brainwave 287 GFLOPS/W and Jetson at 14·N ops/sample (C5);
  the P1 DSP-block row (25–170 pJ/bit × ENOB) — reported, not load-bearing.

### 20.4 Reachability
- Single-ring amplitude memory at the lightest registered damping r_min = 0.1606 (S0.4-0):
  κ_net,min = (1 + 2 r_min) κ_i passive, (0.1 + 2 r_min) κ_i pumped; κ_i from the registry
  (C-1 3.04×10⁸, C-2 8.94×10⁷, C-3 2.03×10⁷ rad/s; N = 8/32/128 ↔ C-1/C-2/C-3 per PR-4 R2).
  **N_reach = ⌊f_s / κ_net,min⌋**; cells with N_taps > N_reach are **UNREACHABLE** regardless of
  energy. Convention flagged conservative-to-the-lattice (hop delays could extend it; S0b.1 measures).

### 20.5 Verdict rules (frozen; reused verbatim at S0b.4)
- **Cell clears** iff E_digital / E_photonic ≥ 3 at that corner, the cell is reachable, and the
  packaging co-condition ≤ 3 dB.
- **Stage-0b product window exists** iff at **CONS**, at least one reachable cell with **N_taps ≥ 16**
  clears with all rows 20.2 charged, under a drift option S0b.3 can deliver (retrain-based cells are
  "conditional-on-S0b.3" until S0b.3 measures the cadence).
- **S0b.0 kill:** if the **maximum** E_digital/E_photonic over all **OPT** cells with class ∈ {C-pz,
  C-pcm, hybrid}, passive or pumped, any drift option (UNSOURCED rows included), T_r = 1000 s, at the
  best reachable N_taps, is **< 3**, the product door is closed by arithmetic and S0b.1–S0b.3 do not
  run. If ≥ 3, the surviving cells define the grid S0b.1–S0b.3 must hit.
- **Sensitivity re-statement (mandatory in the memo):** the same maxima with every UNSOURCED row
  removed (global heater and tracked-lock options dropped → TEC only; C-pz OPT hold → 2 mW; e_tap at
  the sensitivity band ends). The verdict of record is the frozen-row one; the sensitivity is
  reported next to it, S0.7 exclusions-ledger style.
- Every number carries its ledger row and status. No row is added or changed after this block
  without a dated addendum.

### 20.6 Output
`results/s0b_0/envelope.md` (tables + verdict + sensitivity), `envelope.json`, one PNG; memo
committed with `git add -f`; results_log entry; continuation-gate escalation to Lucas.

## Post-run erratum — 2026-09-13: PAT mismatch command binding and cost interpretation

This is a post-run correction, not a new pre-registration or a change to a frozen
threshold. User authorized repairs following the repository review ("Ok do it please").

- **PR-5 §E / PR-17 mismatch sweep:** `build_twin` scaled the intended level, but
  `bind_command` read global m=1 constants for detuning and both coupling maps.
  Offline deployment scaled all five errors. Comparisons at m>1 therefore did not
  implement the registered shared family. The claim of a tie through 30% is
  **withdrawn**, not reinterpreted as a new experiment. m=1 and the separate drift
  experiment are unaffected. The code is fixed with a regression covering command
  values and Jacobians at m=0/1/2/6. No corrected higher-level runs are claimed;
  original files and summaries remain historical evidence, with disposition in N8.
- **S0.7 training cost:** optical sequence duration is not wall-clock duration.
  Total-energy and four-orders total-energy ranking claims are withdrawn; component
  budgets remain. No timing or actuator costs are invented to fill the gap.
- **PR-20:** gate, frozen constants, and computed ratios are unchanged. Ratio 0.64
  means photonic energy is 1/0.64 times digital energy. The implemented minimum-
  damping memory ratio is 3.14, not ten. Rate scaling is linear at fixed tap count,
  approximately quadratic only while usable tap count also grows with rate.
  Maintenance is a lower-bound component estimate, not measured retraining cost.
  Additional nonnegative costs cannot improve the negative gate at fixed cadence.
- **Disposition:** Stage 0b remains closed; higher-rate work and fabrication are
  paused. P1 now includes the negative inline follow-up. Submission remains pending
  final release review; this correction does not authorize publication or email.

## Post-run correction rerun — S0.13 (2026-09-13, approved before new runs)

Lucas approved the bounded rerun after N8 ("okay let's do this"). The execution
protocol is `docs/s0_13_rerun_protocol.md`, committed before the fresh runs. It
retains PR-5 §E/PR-17's seeds, budget, evaluation, and statistical rule. Fresh
32 PAT m>1 units plus one m=1 anchor; unaffected offline/base records reused with
hash provenance. New source-versioned outputs only under `results/s0_13/`.
No corrected result is asserted by this entry. Both outcomes will be reported;
the old withdrawal remains in force until the corrected analysis is complete.


### S0.13 correction consumption — 2026-09-13 (post-run; frozen rules unchanged)

Bounded protocol committed at `bda989f`; corrected results at `174558c`. All 32
higher-mismatch PAT units and the single m=1 seed-11 anchor completed. The anchor
reproduces the full 316-point coarse trace, final coarse/fine SER, and both pass
ledgers exactly. Forty unchanged offline and eight PAT m=1 units are reused;
the anchor is not an additional replicate. Source and state hashes are retained
in `results/s0_13/` and the reproduction archive. This is implementation repair
after discovery of the bug, not a newly blinded experiment.

At PR-17 eval-F, offline/PAT ratios at m={1,2,3,4,6} are
{1.0529,1.0349,1.0058,1.0233,0.9943}; all paired difference intervals include zero.
No level meets the registered advantage rule; m* is absent. Neither arm's median
fails the target. Coarse ratios are {1.3333,1.3333,1.5000,1.5000,1.3333}; no coarse
level clears the advantage rule either. An unresolved difference is not evidence
of equivalence. Historical invalid m>1 PAT outputs remain withdrawn; S0.13 supplies
new corrected evidence for the complete tested grid. No thresholds, seeds, budgets,
or stopping rules were changed. The base bake-off and drift result are unchanged.

Fleet: 3.006 aggregate CPX62 server-hours; approximately EUR 1 gross with per-node
hour rounding, plus small IPv4 charges (estimate, not invoice). All four servers
and all primary addresses were removed after retrieval. No hardware or higher-rate
study was opened. P1 incorporates the correction and PR-20 negative envelope;
standalone P5 publication is deferred, and P2 contact remains separate.

### 🔒 20.7 PR-20b ADDENDUM (2026-09-14; post-run, interpretation only — frozen rows, grid, ratios and the kill verdict unchanged)

**Reachability over-credited the photonic side.** §20.4 bounded the emulable tap count by single-ring
amplitude memory × line rate, N_reach = ⌊f_s/κ_net,min⌋, flagged "conservative-to-the-lattice". It is
the opposite for a broadband input: an N-state linear time-invariant filter has an impulse response
that is a sum of N complex exponentials, so it can match at most ≈ N independent degrees of freedom of
a FIR equalizer, whatever the line rate. Memory and bandwidth trade inside each pole (a pole of
bandwidth Δf contributes memory ≈ 1/Δf; covering a band B with N poles gives Δf ≈ B/N and memory
≈ N samples). **Corrected bound: N_reach ≤ N (the system order), with the IIR-vs-FIR efficiency of
all-pass structures on smooth channel responses (chromatic dispersion) the only route to
"N states ≈ more than N taps", to be measured, not assumed.** Consequences:
- The S0b.0 kill is **more** robust: every clearing candidate used N_taps = 64 at N = 128 (fine) but
  the N = 32 cells credited 16–53 taps that the order bound caps at ≤ 32; no cell's ratio rises.
- The "f_s² lever" residue (reading.md; E-2026-09-13-2 item 2) is **withdrawn**: at fixed N the usable
  tap count does not grow with rate, so the ratio scales linearly in f_s at best. §7.4's "quadratic only
  while usable tap count grows" is now "quadratic never; linear at fixed N".
- The high-rate direction is re-framed (Stage 0c proposal, `docs/s0c/`): not the high-Q substrate at
  a faster clock, but the **FSR-matched low-Q ring lattice** (round trip ≈ symbol period, poles set by
  coupling, the classical all-pass/lattice equalizer regime of Lenz & Madsen 1999), where thermal
  sensitivity per linewidth relaxes ~100–1000× and the memory-vs-order question is the known
  IIR-compensator one. That is a new registration (PR-22 series), not a reading of PR-20.
