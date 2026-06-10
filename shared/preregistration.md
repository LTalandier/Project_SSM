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

## Ledger

| ID | Governs | Freeze before | Status | What must be registered | Source |
|----|---------|---------------|--------|-------------------------|--------|
| **PR-1** | Gate (i) | S0.2 run | 🔒 **FROZEN 2026-06-10** (Lucas "ok go", E-2026-06-10-4; Critic-reviewed v2 block below) | Gate-i accuracy margin + the named published benchmark it reproduces. | roadmap S0.2 |
| **PR-2** | Bake-off setup | S0.2 | 🔒 **FROZEN 2026-06-10** (Lucas "ok go", E-2026-06-10-4; Critic-reviewed v2 block below) | The bake-off **task**; the **hybrid architecture** (what is simulated — layer/stack, encoder, head, nonlinearity); the **trainable-parameter partition** (every method trains the *same* partition); the **in-situ-trainable physical-parameter set + actuation map** (which params, by what actuator — heater detuning vs tunable coupling vs gain). Task sized against S0.1's pole/memory bound + the S0.7-lite niche (PR-10). | F2, white-space |
| **PR-3** | S0.5 target | rule before S0.4 close; **ceiling frozen at S0.4 close** | ⬜ | The bake-off **target rule relative to the BPTT-on-substrate ceiling** ("within X% of exact-gradient accuracy at the same cell"); the **absolute task-utility floor** (ii-a). Register the *rule* (X%) first; measure + freeze the ceiling once at S0.4 close; then run. | F2.3, F10.2 |
| **PR-4** | Substrate + Gate ii | S0.3 build / S0.5 gate | ⬜ | Self-consistent operating **(α, Q_i) pair** (derive one from the other; add a loss↔Q registry check); the **κ_ext policy** (fixed regime or trainable bounds); the named **"realistic SiN noise" cell** (Q/α, NF, ASE level). **Foundry-grade gates Gate ii; class-leading is a labelled aspirational sweep axis.** Resolves D-2026-06-08-1. | F13, F10.5 |
| **PR-5** | PAT (S0.4a) | S0.4a | ⬜ | PAT **twin-mismatch families + levels** (parametric calibration error at realistic characterization accuracy + structural omission); **calibration-error unification** — offline-deploy baseline's weight-mapping error drawn from the *same* family. Headline cell = the registered mismatch level; report PAT as a function of it. | F7.2–3 (CRITICAL) |
| **PR-6** | All estimators (S0.4) | S0.4a | ⬜ | The **fairness contract**: physical-operations invariant (gradients only from simulated device passes on the shared substrate w/ fresh noise; autodiff-through-substrate reserved for the BPTT reference); common θ₀ + data ordering per seed; **equal pre-registered HP budgets** per method; **equal max-device-pass budget B** per cell. | F7 (CRITICAL) |
| **PR-7** | Cost metric (S0.4/S0.5) | S0.4 | ⬜ | Cost **unit = physical device passes, any direction** (per-method table: SPSA 2 fwd; PAT 1 fwd + digital twin-backward on a side-ledger; adjoint 1 fwd + 1 adjoint device pass; RHEL 1 fwd + 1 echo device pass); batch convention; **digital-compute side-ledger** reported alongside. | F5 |
| **PR-8** | S0.5 analysis | S0.5 | ⬜ | Statistical plan: **right-censoring** treatment (fraction-reaching-target within B + median/IQR among reachers / survival treatment); lexicographic ranking (success-fraction, then median passes); paired-by-seed bootstrap CIs; **≥8 seeds for all methods in headline cells** (4 only for exploratory grid). | F11 |
| **PR-9** | Gate ii + promotion | S0.5 | ⬜ | **Gate-ii semantics** decomposed: (ii-a) capacity — BPTT ceiling clears the utility floor; (ii-b) trainability — **PAT or SPSA** within margin of ceiling (only-adjoint/RHEL-pass → escalate-and-redesign, *not* a pass). **Promotion criteria**: "clearly beats" quantified (e.g. ≥X% better pass-to-target w/ non-overlapping 95% CIs, or strictly-better scaling, or strictly-simpler hardware ledger at non-inferior efficiency); **"exactness" struck** from the menu (outcome metrics + F8 hardware ledger only). | F10 |
| **PR-10** | S0.7-lite | before S0.2 task reg | 🔒 **FROZEN 2026-06-10** (Lucas "ok"; values in the block below) | S0.7-lite **assumptions**: conversion energies, DAC/ADC rates, named **digital-baseline class + sources**, operating scale (N rings, rates). Labelled assumption-driven; not load-bearing in outreach before full S0.7. | F1, F16 |
| **PR-11** | RHEL echo (S0.4c) | S0.4c | ⬜ | RHEL echo **invariants**: independent forward/echo ASE streams (no common-RNG reversal); no loss-sign flip (echo through the *same* dissipative substrate); gain injects fresh ASE in the echo too. **Conjugation-fidelity bound** + the **unit test** (echo of a noisy forward must *not* recover the noiseless state; bounded by fidelity × ASE floor). | F9 |
| **PR-12** | Damping cell | after S0.3 coarse sweep, before S0.5 grid | ⬜ | The **central damping operating cell** for the bake-off, from the F3 coarse BPTT-on-substrate sweep; the sweep is over the physical damping **floor** + init/range, not a fixed value. | F3 |
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

## PR-1.1 — PROPOSED amendment (Supervisor draft 2026-06-11; ⬜ until Critic review + Lucas signature; PR-1 v2 above retained per supersession discipline)

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
   pins, official data pickles, the official runner, same GPU) on the 5 published Walker seeds
   scores **90.5556 % — itself below the frozen 90.6 gate** (unrounded, per PF-F8h), with
   per-seed σ ≈ 9.3 pp against the published 4.4.
2. **Mechanism:** the official objective −Σ y·log(softmax + 1e-8) has a **zero-gradient
   absorbing state in fp32** (softmax saturation → p_true underflows to exactly 0 → total
   gradient exactly 0.0 permanently); step-instrumented, bit-deterministically reproduced.
3. **Incidence:** 4/8 protocol seeds (our declared framework-inherent stream) vs 2/8 fresh
   seeds (the official stream) — Fisher two-tailed **p ≈ 0.61**, statistically
   indistinguishable. At the observed incidence the published 5-seed set is trap-free with
   probability only ≈ 0.10–0.24: **the published 95.0 ± 4.4 sits on a favorable draw of a
   ~25 %-incidence collapse belonging to the published method.**
4. **The port is exonerated on independent evidence:** float32-exact cross-framework parity
   (2.4–2.7×10⁻⁷ full-model, both anchors, incl. full L=17,984; 1.2–1.5×10⁻⁷ on the GPU),
   line-by-line init-distribution audit vs the official source, healthy-seed mean 93.52 %
   inside the published band.

**Amendment (re-registration; Lucas-only):**
- **The G3 criterion is declared VOID for anchor instability.** Its premise — "published
  mean − 1σ transfers to a faithful rerun" (PF-F9d) — is empirically false at this anchor:
  the reference implementation fails the threshold on its own published seeds. As frozen,
  the criterion is a lottery on seed-stream trap incidence in either direction; it no longer
  measures implementation fidelity, which is the only thing Gate i exists to measure.
- **No replacement published anchor is registered.** (i) The S0.2-0 alternates re-open
  registered exclusions (MotorImagery anchors on a preprint — the G2 exclusion ground);
  (ii) any replacement carries exactly the untested-transferability risk that just fired;
  (iii) the registered downstream reference was never the published numbers — it is the
  in-house BPTT-on-substrate ceiling (PR-3; stated at the freeze in PF-F9d and in the
  D-08-2 constraint).
- **Gate i is re-registered as: G1 PASS (gated, frozen, untouched) ∧ the numerical-identity
  dossier** (cross-framework parity ≤ 3×10⁻⁷ on full-model outputs for both anchor configs,
  transplanted weights, train + inference modes — already on record from the pre-registered
  cross-check harness). **Adjudication under this criterion: the gate's registered purpose —
  "idealized model reproduces published oscillatory-SSM behavior", i.e. validate the in-house
  implementation — is SERVED**: the layer provably *computes the reference model* to float32
  precision, which is categorically stronger evidence than any accuracy reproduction. The
  letter-FAIL of the frozen v2 criterion remains on record beside it. Downstream (S0.3+)
  proceeds on the PR-3 anchoring path as registered.
- **Binding for S0.8 / the paper:** the G3 outcome is reported as a *finding*, not buried —
  LinOSS-IM EigenWorms 95.0 ± 4.4 does not reproduce under a faithful rerun of its own
  implementation (90.6 ± 9.3, with a ~25 %-incidence fp32 init collapse); first-hand
  motivation for the PR-3 in-house-ceiling anchoring philosophy. Optional upstream courtesy
  report to the LinOSS authors = outreach, Lucas-paced, not before the S0.8 wording freeze.
- **Annex-3 EigenWorms: cancelled** (non-gating by construction, PF-F8g; anchors nothing
  under this amendment; G1's annex is complete and stands).
- **Process carry-in (binding on future freezes):** any externally-anchored gate must include
  a **reference-implementation transfer check** — rerun the official code on the gating cell
  at small scale — *before* its threshold freezes (cost here would have been ~$1/hours and
  would have caught F-G3 pre-freeze).
