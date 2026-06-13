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

## Ledger

| ID | Governs | Freeze before | Status | What must be registered | Source |
|----|---------|---------------|--------|-------------------------|--------|
| **PR-1** | Gate (i) | S0.2 run | 🔒 **FROZEN 2026-06-10** (Lucas "ok go", E-2026-06-10-4; Critic-reviewed v2 block below) · **amended by PR-1.1 🔒 SIGNED 2026-06-11** (G3 criterion void for anchor instability — F-G3; Gate i adjudicated purpose-served: G1 PASS ∧ parity dossier) | Gate-i accuracy margin + the named published benchmark it reproduces. | roadmap S0.2 |
| **PR-2** | Bake-off setup | S0.2 | 🔒 **FROZEN 2026-06-10** (Lucas "ok go", E-2026-06-10-4; Critic-reviewed v2 block below) | The bake-off **task**; the **hybrid architecture** (what is simulated — layer/stack, encoder, head, nonlinearity); the **trainable-parameter partition** (every method trains the *same* partition); the **in-situ-trainable physical-parameter set + actuation map** (which params, by what actuator — heater detuning vs tunable coupling vs gain). Task sized against S0.1's pole/memory bound + the S0.7-lite niche (PR-10). | F2, white-space |
| **PR-3** | S0.5 target | rule before S0.4 close; **ceiling frozen at S0.4 close** | ⬜ | The bake-off **target rule relative to the BPTT-on-substrate ceiling** ("within X% of exact-gradient accuracy at the same cell"); the **absolute task-utility floor** (ii-a). Register the *rule* (X%) first; measure + freeze the ceiling once at S0.4 close; then run. | F2.3, F10.2 |
| **PR-4** | Substrate + Gate ii | S0.3 build / S0.5 gate | 🔒 **SIGNED v2 2026-06-13** (Lucas, "sign PR-4"; block below; Critic review 2026-06-12 verdict **AMEND** — all P4-F1..F12 applied; Cui body confirmed [EV] via independent commentary 2026-06-13, risk (i) closed; E₀ numeric = registered S0.3-1 calibration addendum) | Self-consistent operating **(α, Q_i) pair** (derive one from the other; add a loss↔Q registry check); the **κ_ext policy** (fixed regime or trainable bounds); the named **"realistic SiN noise" cell** (Q/α, NF, ASE level). **Foundry-grade gates Gate ii; class-leading is a labelled aspirational sweep axis.** Resolves D-2026-06-08-1. | F13, F10.5 |
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
> **Saturated reachability (honest, confirms the §G/P4-F2 prediction):** required small-signal
> g₀ (bus) to hit 0.9×κᵢ at the registered drive = C-1 5.04, C-2 1.5, C-3 0.36 dB/cm vs the
> Er-anchor span 1.0–1.9 dB/cm ⇒ **C-1 material-aspirational** (headroom ×6.5–12.3 < required
> ×32.6 — anchor-risk (v)), **C-2 straddles** (reachable only for the **upper half** of the Er
> span, ≥1.5 dB/cm; ×21.8–41.4 vs ×32.6), C-3 ✓, C-2-derate material-aspirational. **The "✅"
> in the source table overstates C-2 — the registered honest status is "reachable iff Er ≥ 1.5
> dB/cm"; carried at anchor-risk (v).**

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
