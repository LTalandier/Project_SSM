# Critic Review — Stage-0 Roadmap (plan review, pre-code)

**Reviewer:** Critic (independent session; reports to **Lucas**, not the Supervisor)
**Date:** 2026-06-08
**Spec:** `shared/critic_instructions_stage0-roadmap.md`
**Reviewed:** `shared/stage0_roadmap.md` (draft v2, 2026-06-06) · `photonic-ssm-proposal-v0_5.md` ·
`shared/tooling_recon.md` (2026-06-07) · `shared/task_queue.md` (S0.0 ACTIVE) ·
`shared/decisions_needed.md` (D-1/D-2 resolved; D-2026-06-08-1 parked).

---

## Overall verdict: **APPROVE-WITH-EDITS**

The headline question — *if this plan runs to completion, does it produce a defensible answer to "can a
photonic recurrence be trained in situ, and is it worth building?"* — gets a **conditional yes**. The
decomposition is essentially right, the two gates are the right gates, the primary metric is correctly
chosen and correctly defended, the RHEL-honesty requirements are present, and the §10 premise is treated
as falsifiable before MPW spend. None of my findings require restructuring the phase graph.

But the plan as drafted would, executed naively, permit several **silent validity failures**: the PAT
twin-mismatch protocol is unspecified (it is a free parameter that effectively *sets* PAT's bake-off
score — F7, the one CRITICAL); Gate ii's wording lets the demoted cosine diagnostic re-enter through the
promotion menu as "exactness," and its "PAT/SPSA regardless" clause has a corner case that would commit
hardware to methods that failed in simulation (F10); the bake-off target accuracy as written conflates
architecture capacity with training-method quality (F2); and the roadmap's S0.0 text contradicts the
recon it is supposed to have absorbed (F17). All are fixable by pre-registration entries and roadmap
text edits. The Supervisor's proposal to pull a cheap S0.7 envelope earlier is **endorsed**, with a
sharper rationale than kill-testing (F1).

**Severity count:** 1 CRITICAL · 9 HIGH · 11 MEDIUM · 1 LOW.

### Fix-by schedule (consolidated)

| Deadline | Findings |
|---|---|
| **Now / S0.0 close (before S0.1 science starts)** | F17 (stale roadmap text), F12 (create the pre-registration ledger) |
| **Before S0.2 runs** | F1 (S0.7-lite), F2 (task + architecture pinning), F13 (Q pair), F20 (secondary task) |
| **Before S0.3 build** | F18 (substrate gates), F21 (compute sizing), F19 (backscatter bound, from S0.1) |
| **Before S0.4 implementations** | F7 (fairness contract — CRITICAL), F8 (hardware ledger), F9 (RHEL invariants), F5 (pass accounting hooks) |
| **Before S0.5 runs** | F10 (gate semantics + promotion criteria), F11 (stats plan), F3 (damping-sweep timing), F22 (conclusion templates) |
| **Before the Stage-0 paper (S0.8)** | F14/F15 (debt timing + white-space search), F16 (S0.7 content), F19 (limits-of-simulation caveat), F4, F6 |

---

## 1. Decomposition & dependency order

**Answer: order is right in structure; two real ordering defects (F1, F2), one optimization (F3).**

### F1 (HIGH) — The early S0.7 envelope: AGREE, but reframe it from "kill-test" to "task-selection input"
The Supervisor proposes pulling a cheap S0.7 systems-advantage envelope earlier as a kill-test of the
§10 premise. **I endorse pulling it earlier — but the kill-test framing both overstates and undersells it.**

- *Overstates:* a negative early envelope does **not** kill Stage 0. Proposal §10 is explicit that "the
  scientific first stands without a systems advantage; the commercial thesis does not." The bake-off
  paper and the mapping paper are publishable regardless. What a negative envelope changes is the
  *framing of the Stage-1 spend decision* (science-only chip vs commercially-motivated chip) — which is
  Lucas's call, made better early.
- *Undersells:* the sharper reason to run it early is **dependency inversion in the current order**. S0.7
  is the phase that identifies the target low-latency *niche*; S0.2 pre-registers the bake-off *task*.
  As ordered, the task is chosen blind to the niche. If the only plausible advantage window is (say)
  GHz-rate RF/streaming preprocessing with µs latency budgets, then a bake-off pre-registered on a
  generic long-range benchmark invites the hostile question: *"why did you benchmark on a task irrelevant
  to your claimed niche?"* The early envelope is an **input to the S0.2 task choice**, not just a kill
  switch.

**Recommendation.** Add an explicit **S0.7-lite** (days, assumption-driven, no new code, parametric in
memory length where S0.1 numbers don't exist yet), running parallel with S0.1, **due before the S0.2
task registration**. Pre-register its assumptions (conversion energies, DAC/ADC rates, digital-baseline
class — named sources) so the "optimistic envelope" is not post-hoc tunable. Handle *both* outcomes with
discipline: a negative lite-envelope → escalate to Lucas as a Stage-1-reframing finding (per the existing
S0.7 language); a *positive* lite-envelope → it remains labelled assumption-driven and must **not**
become load-bearing in outreach before the full S0.7 (envelope honesty cuts both ways). Keep full S0.7
in place — the lite version does not discharge it. The roadmap's own footnote ("S0.7 … can also start
earlier") already half-licenses this; formalize it.

### F2 (HIGH) — S0.2 must pin the task, the *simulated architecture*, and the trainable-parameter set — and the bake-off target must isolate method quality from architecture capacity
Three under-specifications in S0.2/S0.5 that jointly confound Gate ii:

1. **Physical commensurability.** The published LinOSS results (Gate i's reference) come from full
   multi-block digital models with state dimensions and sequence lengths a physical ring bank cannot
   match (N rings is reticle-bounded — proposal §9 risk 5; memory is Q-bounded — see F13 numbers). If
   the S0.5 target is "the S0.2 accuracy" of a 6-block digital model, the physical-scale system may
   never reach it *under any training method*, and Gate ii fails for reasons unrelated to in-situ
   training. The pre-registered task must be sized against the S0.1 pole-region/memory bound (sequence
   scale vs achievable |λ|·steps; state dim vs plausible ring count) and, per F1, drawn from or linked
   to the S0.7-lite niche.
2. **Architecture pinning.** Nothing in the roadmap states what is actually simulated in the bake-off:
   one photonic SSM layer with digital readout? A stack? What surrounds the recurrence (encoder, head,
   nonlinearity), and which of those surrounding parameters are trained, by what (exact digital gradients
   alongside the estimator's physical-parameter updates?). Every method must train the **same parameter
   partition** or the comparison is void. Pin the hybrid architecture and the partition at S0.2.
3. **Two distinct pre-registered numbers, currently conflated.** Gate i's margin (digital reproduction
   of a published benchmark) and the S0.5 target accuracy are different quantities. **Recommended
   structure:** register the bake-off target *relative to the BPTT-trained-substrate ceiling* — i.e.
   "within X% of the accuracy that the *same physical architecture at the same noise cell* achieves
   under exact gradients (the BPTT reference, which S0.4's gate builds anyway)." Register the *rule*
   (X%) before S0.4 closes, measure the ceiling once at S0.4 close, freeze it, then run the bake-off.
   This isolates *method quality* (the bake-off's question) from *architecture capacity* (Gate i / the
   ceiling's own value). See F10 for the matching gate decomposition.

Also pin here the **trainable-parameter set + actuation map**: the white-space sentence claims *pole
positions + inter-ring couplings* trained on-device. Detunings β_i are clearly heater-trainable; pole
*real* parts require tunable bus–ring coupling (MZI-assisted couplers — added device complexity) and/or
per-ring gain; inter-ring coupling topology (direct photonic-molecule coupling vs bus-mediated) is
unstated. S0.1's deliverable should include exactly which physical parameters are in-situ-trainable,
since the headline claim's wording depends on it.

### F3 (MEDIUM) — S0.6 does not depend on S0.5; run a coarse damping sweep *before* the bake-off
The damping/accuracy curve is a property of the **architecture + task**, obtainable by training the
BPTT reference on the substrate at each damping point — no estimators needed. Placed after S0.5 it (a)
serializes needlessly and (b) means the bake-off grid was placed without knowing where the
accuracy-optimal damping region is. Recommend: coarse damping sweep at S0.3-close → pre-register the
bake-off's central operating cell from it → full S0.6 curve stays where it is (or merges into the S0.5
sweep analysis). Clarify too *what* S0.6 sweeps, since D-LinOSS damping is a trainable parameter: the
sweep is over the physical damping **floor** (loss–gain operating point) and any damping
initialization/range, not over a fixed damping value.

### F4 (LOW) — Remaining order is affirmed; minor parallelism available
S0.1 → S0.2 is **correct** (contra naive parallelization): task selection must consume the pole-region
bound (F2). S0.3 could start in parallel with S0.2 once S0.1 lands (the substrate doesn't need Gate i's
outcome, only S0.1's model) — worth taking if Executor bandwidth allows; the gate dependency
(Gate i before S0.4/S0.5 *spend*) is preserved either way.

---

## 2. Primary-metric integrity

**Answer: the metric choice is right and the stated rationale is sound — I re-derived it and it
strengthens (F6). But the metric's *unit* is under-specified in a way that favors different methods
depending on the choice (F5).**

### F5 (HIGH) — Define the cost unit: "physical forward passes" is ambiguous across exactly these four methods
The four estimators differ in *what kinds* of device passes they consume; an accounting convention that
counts only "forward" passes gives the exact methods a free ride:

| Method | Device passes / update | Digital compute / update | Extra device ops |
|---|---|---|---|
| SPSA | 2 forward | negligible | none |
| PAT | 1 forward | **1 full twin backward (a digital BPTT!)** | output-trajectory measurement |
| Adjoint | 1 forward **+ 1 adjoint (backward) device pass** | light | error-field injection; per-element monitor reads |
| RHEL | 1 forward **+ 1 echo device pass** | light | conjugation op (its own loss/noise); nudge injection |

The adjoint's backward pass and RHEL's echo are *device* passes — they consume device time and inject
ASE — and must be counted. PAT's twin backward is *digital* cost and must appear on a digital-compute
side-ledger (it is the reason PAT is not "free"; it also frames the obvious hostile question of what PAT
buys over offline training — answer: deployment-mismatch absorption, which F7's contract makes
measurable). **Recommendation:** pre-register (i) the unit = *physical device passes, any direction*,
with the per-method table above; (ii) a batch convention (a pass = one sequence through the device;
batching counts ×batch — hardware-realistic); (iii) a digital-compute side-ledger reported alongside;
(iv) note in S0.8 that pass ≠ equal wall-clock on hardware (an adjoint pass needs reconfiguration; an
echo needs storage/timing) — the hardware ledger (F8) carries that. The salvaged
`n_forward_equivalents` accounting is the right hook; extend it to non-forward passes.

### F6 (MEDIUM) — Cosine-demotion rationale: endorsed, and it sharpens in both directions; report the diagnostic as bias/variance
The stated rationale is correct: SPSA's per-step estimate has cosine ~O(1/√P) to the true gradient
(P = parameter count) by construction, yet its *expected* descent direction is unbiased to O(c²) and it
converges — a cosine headline would mark SPSA "broken" while it trains. The rationale strengthens in the
*other* direction too: per-step cosine can also **flatter the exact methods** — a systematically biased
but low-variance gradient (e.g. RHEL's echo under dissipation asymmetry, PAT under twin bias) can show
respectable average cosine while the bias stalls convergence at a plateau the primary metric *would*
catch. So cosine-as-headline misranks in both directions; sample-efficiency-to-target is the right
primary. **Recommendation:** report the secondary diagnostic as a **bias/variance decomposition of the
gradient estimate vs the BPTT reference** (mean error vector norm + variance), not raw cosine alone —
it is far more mechanistically attributive (why a method failed), which is the diagnostic's actual job.
**Creep audit result:** the roadmap's run/reporting language is clean (S0.4 "floor check, not the
headline"; S0.5 "never use it as the headline") — the creep is in Gate ii's promotion menu (F10) and a
soft incentive in the outreach framing (F22).

---

## 3. Shared-substrate fairness

**Answer: structurally yes — one S0.3 substrate, baselines included, stated as a quality standard. But
"one substrate" is necessary, not sufficient: the binding fairness question is what *information and
operations* each method is granted on top of it. That contract does not exist yet (F7), and one of its
consequences — Gate ii's "hardware simplicity" criterion having no data source — needs its own
deliverable (F8).**

### F7 (CRITICAL) — Pre-register the estimator information/operations contract; the PAT twin-mismatch protocol is currently a free parameter that sets the bake-off's outcome
In Stage-0 simulation, the "physical system" *is* the substrate model. PAT's digital twin is another
model of it. **If the twin equals the substrate, PAT is exact BPTT and structurally wins the bake-off;
the result is then an artifact of the experimental design, not a finding.** The roadmap says
"characterize twin-mismatch bias" (S0.4a) but never specifies how mismatch is generated, at what level,
or that it is pre-registered. This is the single largest validity threat in the plan. The same root
issue touches every estimator: an adjoint implemented as autodiff-through-the-substrate is just BPTT,
not a *physical* adjoint; an echo that reuses the forward pass's RNG reverses noise that physics cannot
reverse (F9).

**Recommendation — one pre-registered "fairness contract" (a section of F12's ledger), with at least
these clauses, fixed before S0.4a starts and audited per estimator at the S0.4 gate:**

1. **Physical-operations invariant.** Every estimator's gradient is produced exclusively by *simulated
   physical operations on the substrate* (device passes under the full noise model, in whichever
   direction the method physically uses) plus allowed digital post-processing. Autodiff through the
   substrate is reserved for the BPTT reference. The adjoint's backward pass and RHEL's echo propagate
   through the *same dissipative, noisy substrate* (fresh noise draws), with their injection/readout
   hardware modelled or explicitly idealized-and-declared.
2. **Twin-mismatch protocol (PAT).** Pre-register mismatch *families* and *levels*: (a) parametric
   calibration error — twin parameters (κ_i, κ_ext, detunings, gain saturation) drawn at realistic
   characterization accuracy (justify levels from what Stage-1-style transmission-spectrum fits achieve;
   cite); (b) structural omission — the twin is deterministic (no ASE realization) and may lack
   selected physics (e.g. dynamic gain), exactly as a real twin would. Report PAT's score as a *function*
   of mismatch level, with the pre-registered level as the headline cell. Optionally include a
   twin-recalibration cadence (it is part of PAT's real cost).
3. **Calibration-error unification.** The **offline-train-deploy baseline's weight-mapping error must be
   drawn from the same calibration-error family as PAT's twin mismatch** — they are physically the same
   knowledge gap. Otherwise the "what does in-situ training buy" comparison (the §10 *training*
   advantage) is incoherent: PAT's edge over offline-deploy is precisely mismatch absorption, so both
   must face the same mismatch.
4. **Common starting conditions.** Same initial parameter vector θ₀ per seed across all methods; same
   data ordering per seed; same noise *distribution* per cell with a documented seed protocol (exact
   realization-matching across methods is impossible given differing pass structures — match at
   distribution + seed-set level and let F11's stats handle the rest).
5. **Equal, pre-registered hyperparameter budgets.** Same search procedure, same trial count, per
   estimator (each has sensitive HPs: SPSA's c/a schedules, PAT's lr + recalibration, adjoint's
   injection amplitude, RHEL's nudge strength β and echo timing). Tuned where (one pre-registered cell
   or per-cell), then frozen. Unequal tuning effort is the classic way optimizer bake-offs get silently
   rigged, in either direction.
6. **Equal pass budgets.** One pre-registered max-device-pass budget B per cell, identical across
   methods (this is also what makes F11's censored statistics well-defined).

### F8 (HIGH) — Per-method hardware-requirements ledger (observability/actuation), as an S0.4 deliverable
The simulation grants observables and actuators that Stage-1 hardware may not have: full state
trajectories (constraint 3b) are an *API* convenience — on chip, every per-ring tap costs loss and every
injector costs components. The methods differ enormously here, and that difference is exactly Gate ii's
third promotion axis ("hardware simplicity") — **which currently has no phase producing its data**:
SPSA needs scalar loss only; PAT needs output trajectories (+ twin); the adjoint needs time-reversed
error-field injection and per-element field/intensity monitors to read the gradient; RHEL needs a
conjugator + storage/timing + nudge injection. **Recommendation:** S0.4 deliverables include, per
method, a table of (observables assumed, actuators assumed, added components incl. their loss impact,
calibration burden). It (a) gives Gate ii's "hardware simplicity" criterion its evidence, (b) feeds the
Stage-1 design, (c) honestly records where the simulation was generous.

---

## 4. RHEL echo honesty

**Answer: the plan-level requirements are right and match the proposal (§5.2): concrete mechanism
mandated, idealized operator banned, off-chip admission allowed, ASE floor named, odds-improved-not-
reopened framing intact. My findings are implementation traps that would silently un-do that honesty,
plus one physics tension the χ³-FWM sub-model must face (F9), and incentive hygiene (F22).**

### F9 (HIGH) — Bake the irreversibility into the implementation: three invariants + one unit test
1. **No common-RNG reversal.** Forward-pass ASE draws and echo-pass ASE draws are independent streams.
   If the echo replay reuses the forward RNG (an easy bug under a shared substrate object), the echo
   "retraces" noise — physically impossible, and it would silently flatter RHEL in exactly the way the
   plan exists to prevent.
2. **No loss-sign flip.** The echo pass propagates the conjugated field through the *same dissipative
   substrate* — conjugation reverses the dispersive/unitary part of evolution, not the dissipative part.
   Deterministic dissipation asymmetry (energy lost in *both* directions) then emerges automatically,
   which is the honest content of the GLEP/port-Hamiltonian non-extension. If the sub-model chooses
   gain-compensation in the echo, that gain injects *fresh* ASE — model it.
3. **Gain runs during the echo.** Any in-loop gain medium is active in the echo pass and injects its own
   ASE there too: two noise injections per update cycle, plus conjugation penalties, is the honest count.

**Unit test (pre-register at S0.4c):** *the echo of a noisy forward pass must not recover the noiseless
initial state* — quantitatively, echo fidelity is bounded by the pre-registered conjugation fidelity ×
the ASE floor; a perfect-recovery result fails the test and indicates invariant violation.

**χ³-FWM content note:** the listed penalties (pump power, bandwidth, conversion efficiency, added
noise) are the right set; add the specific tension that **resonant enhancement (needed for usable FWM
efficiency in low-n₂ SiN) narrows bandwidth, while conjugating the full N-ring lattice spectrum needs
bandwidth** — the sub-model should state which side it pays, since cw FWM conversion in SiN without
enhancement sits in the −20 to −40 dB range. Storage/timing of the field between forward and echo is a
further unsolved primitive; the off-chip admission can cover it but must then *say so*.

---

## 5. Gate (ii) + the hardware guardrail

**Answer: right gate in spirit; as worded it has one incoherent corner case, one re-entry door for the
demoted diagnostic, and no quantitative teeth — a marginal result could currently be smuggled through
all three (F10). The statistics that "clearly beats" must consume are also unspecified (F11).**

### F10 (HIGH) — Tighten Gate ii's semantics and the promotion criteria
1. **The "regardless" corner case.** "≥1 method trains to the pre-registered accuracy … PAT/SPSA the
   default hardware route *regardless*" — if the only method(s) reaching target are adjoint/RHEL while
   PAT *and* SPSA fail, the gate as written both *passes* and commits hardware to methods that failed in
   simulation. That outcome should be an **escalate-and-redesign**, not a pass. Rewrite: *"Gate ii
   passes iff **PAT or SPSA** reaches the pre-registered target at the pre-registered realistic cell. If
   only adjoint/RHEL reach it, Gate ii fails its hardware-commitment purpose → escalate to Lucas."*
2. **Decompose the gate** (pairs with F2.3): **(ii-a) capacity** — the BPTT-on-substrate ceiling at the
   realistic cell clears the absolute pre-registered task-utility floor (the noisy physical architecture
   can do the task at all); **(ii-b) trainability** — ≥1 hardware-committed method gets within the
   pre-registered margin of that ceiling. The current single gate conflates "device can't" with "method
   can't," which have opposite consequences (redesign architecture vs redesign training).
3. **Strike "exactness" from the promotion menu.** The menu "(exactness, scaling, or hardware
   simplicity)" — in both roadmap and proposal §6 — lets the demoted cosine diagnostic re-enter as a
   *decision criterion* under an alias. An adjoint with beautiful gradient alignment but no
   sample-efficiency or accuracy win must not be promotable on "exactness." Either strike it or redefine
   as "exactness *that delivers* an outcome win (efficiency, final accuracy, robustness)." Promotion
   axes should be outcome metrics + the F8 hardware ledger only. (Roadmap can sharpen this now; note for
   S0.8 to reconcile the proposal's wording.)
4. **Quantify "clearly beats."** Pre-register before S0.5: e.g. *promotion requires ≥X% better
   pass-to-target efficiency (or a strictly better scaling exponent over the swept range) with
   non-overlapping bootstrap 95% CIs across the common seed set at the pre-registered cell, or a
   strictly-simpler F8 ledger at non-inferior efficiency.* The current open menu ("a metric that
   matters") invites post-hoc metric shopping — with four methods and an open axis set, *something*
   always wins on *some* axis.
5. **Pre-register the "realistic SiN noise" cell** (which Q/α pair, which NF, which ASE level — ties to
   F13). Without naming the cell in advance, the gate is evaluable at whichever cell flatters.

### F11 (HIGH) — Statistical analysis plan, incl. censoring — currently absent
Passes-to-target is a **right-censored** quantity (some runs never reach target within budget B). Naive
means-among-finishers bias toward optimistic numbers; SPSA (high variance) is the likely victim or
beneficiary depending on convention. Pre-register: (i) per-cell report = fraction-reaching-target within
B **and** median (+IQR) passes among reachers (or a restricted-mean / survival-curve treatment);
(ii) method ranking lexicographic on (success fraction, then median passes); (iii) pairwise comparisons
paired by seed (common θ₀/data seeds per F7.4) with bootstrap CIs; (iv) seed counts: ≥8 for **all**
methods in headline cells (4 only for exploratory grid scoping) — the house 4-minimum is thin for a
method-comparison headline; (v) the F10.4 promotion test consumes exactly this plan.

---

## 6. Pre-registration discipline + the parked Q decision

**Answer: the margins the roadmap names are correctly pre-registration-gated (S0.2 before the run;
Lucas approves). But the pre-registration *surface* is much larger than the named margins, and nothing
yet forces the rest of it to be written down before the runs (F12). The parked Q decision is correctly
parked; my adjudication and a registry inconsistency found while re-deriving it are in F13.**

### F12 (HIGH) — Create `shared/preregistration.md` now; enumerate the required entries
One versioned file, each entry dated and frozen *before* the run it governs, Critic-reviewed at phase
boundaries. Required entries surfaced by this review: Gate-i margin + benchmark (S0.2); bake-off task +
hybrid architecture + parameter partition (F2); bake-off target rule relative to the BPTT ceiling (F2.3)
+ absolute utility floor (F10.2); operating (α, Q_i, κ_ext-policy) pair and the realistic-noise cell
(F13, F10.5); twin-mismatch families/levels + calibration-error unification (F7.2–3); HP budgets (F7.5);
pass budget B + pass-accounting conventions (F5, F7.6); statistical plan (F11); promotion criteria
(F10.3–4); S0.7-lite assumptions (F1); RHEL echo invariants + fidelity bound (F9); damping operating
cell once the F3 coarse sweep lands. Without the single ledger, each of these will be "decided" at
implementation time inside Executor code — which is how pre-registration quietly dies.

### F13 (MEDIUM) — Parked Q: register a self-consistent (α, Q_i) *pair* + a κ_ext policy; gate at foundry grade; sweep to class-leading as a labelled aspirational axis
Adjudication of D-2026-06-08-1, with numbers re-derived independently:

1. **A registry inconsistency to fix at S0.0/S0.1:** the salvaged `SiN_LIGENTEC_AN800` entry carries
   **0.03 dB/cm *and* Q_i = 2×10⁶ simultaneously — these disagree by ~5.7×.** At n_g = 1.95,
   λ = 1.55 µm: α = 0.03 dB/cm (0.691 m⁻¹ power) → Q_i = ω·n_g/(c·α) ≈ **1.1×10⁷**; conversely
   Q_i = 2×10⁶ → α ≈ 0.17 dB/cm. Likely provenance: best-case straight-waveguide loss vs conservative
   ring Q including bend/coupler contributions — defensible as *separate anchors*, wrong as one
   operating point. **Pre-register Q_i as primary and derive α from it** (or vice versa), and add a
   loss↔Q self-consistency test to the registry alongside the existing FSR check.
2. **What each choice means physically** (FSR 100 GHz → τ_rt = 10 ps; intrinsic-only): Q_i = 2×10⁶ →
   |λ| ≈ 0.997/round-trip, 1/e memory ≈ 330 round trips (3.3 ns); Q_i = 10⁷ → |λ| ≈ 0.9994,
   ≈ 1650 round trips (16 ns). Both are respectable SSM pole magnitudes — the memory story does not
   *need* the aspirational figure at demonstrator scale — but the gap is ~5× in usable horizon, which
   directly moves task feasibility (F2.1) and method ranking (longer horizons stress PAT/adjoint
   stability; SPSA is horizon-indifferent per update). So the choice **does** interact with the
   bake-off's conclusions — one more reason it must be pre-registered, not tuned.
3. **Loaded vs intrinsic.** These |λ| values are intrinsic-only; the pole damping is
   κ_tot = κ_i + κ_ext, and **unless deeply undercoupled, memory is coupling-dominated, not
   intrinsic-loss-dominated** — while deep undercoupling collapses I/O coupling (residues) and detector
   SNR. The "memory is loss-limited, SiN maximizes it" story is true as a *bound* but the realizable
   region is set by the κ_ext trade. The pre-registration must therefore include a **κ_ext policy**
   (trainable within stated bounds, or a fixed coupling regime), and S0.1's pole-region deliverable
   should show the memory-vs-readout-SNR trade explicitly.
4. **Which cell gates.** Gate ii authorizes a **foundry MPW** (CORNERSTONE/LIGENTEC); the proposal's own
   Stage-1 gate is Q_i ≥ 10⁶. Evaluating "realistic SiN noise" at damascene-class Q > 10⁷ — which no
   Stage-1 foundry chip will deliver — would bias the gate toward passing on memory the hardware won't
   have. **Register the foundry-grade pair as the Gate-ii cell; sweep to 10⁷ as a labelled
   aspirational/Stage-2 sensitivity axis; report both.** The D-file's instinct (register a range +
   sensitivity) is right — this sharpens *which point in the range carries the gate*.

---

## 7. Verification debts

**Answer: all four tracked (S0.L), correctly framed, and the white-space claim appears in its sharpened
form with the three named pre-emptions everywhere it occurs. Two fixes: debt timing (F14) and the
white-space search needing to target its *actual* nearest threats (F15).**

### F14 (MEDIUM) — S0.L is not purely parallel: debts #2 and #3 sit on the critical path
The dependency note ("S0.L runs in parallel and feeds S0.8") is wrong for two of the four: **debt #2**
(LinOSS/D-LinOSS/Mamba-3 specifics) is consumed *at S0.2* (the roadmap itself says "resolve … here") —
its memo is a *prerequisite* of the S0.2 benchmark/margin choice; **debt #3** (Er:Si₃N₄ NF) parameterizes
the *S0.3* conservative-NF assumption — its memo (or at minimum a sourced NF bracket) is a prerequisite
of the substrate's ASE knob. Front-load both; #1 and #4 can stay S0.8-paced. Update the graph note.

### F15 (MEDIUM) — White-space search: name the queries that could actually kill the claim
The sharpened claim ("recurrent parameters … updated on the physical device by gradient-based/-estimating
training") survives or dies on priors *between* the named pre-emptions. The S0.L memo must explicitly
search for: (i) **zeroth-order/perturbative (SPSA/FD) updates of internal parameters of any recurrent
photonic system** — a single such prior is fatal, since it is precisely our Stage-1 claim; (ii)
**REINFORCE/policy-gradient updates of internal recurrent params** — reward-*gradient* methods are
gradient-estimating, so the Bueno/Brunner pre-emption ("trains readout by reward") does not cover a
variant that nudged *internal* weights by policy gradient; pre-draft the boundary argument; (iii)
hardware-in-the-loop adaptation of delay-based reservoirs' *feedback/internal* parameters (the
delay-reservoir community's "online adaptation" line); (iv) evolutionary/Boolean-search internal-weight
training (claim survives via the "gradient-based/-estimating" qualifier — but say so explicitly rather
than leaving the lawyering implicit). Date the search; mid-2026 snapshot already flagged in the proposal.

---

## 8. The §10 advantage premise

**Answer: the training-vs-systems distinction is correctly preserved (S0.5 baselines = training
advantage; S0.7 = systems advantage incl. conversion overhead), and the plan honestly admits the premise
can fail pre-MPW (S0.7's escalation clause). The early-envelope adjudication is F1. What remains is
S0.7's content floor (F16).**

### F16 (MEDIUM) — S0.7 content requirements (write into the phase spec)
(i) **Strong digital baseline**: for a low-latency niche the honest comparator is a tuned FPGA/ASIC (or
embedded-GPU) implementation of the same SSM at matched accuracy — pre-register the baseline class and
the sources of its latency/energy numbers; "vs an unoptimized GPU" is the first hostile review comment.
(ii) **Full power ledger**: include thermo-optic *holding* power (mW-scale × N heaters just to hold the
operating point), control electronics, and any active locking — the costs photonic-advantage analyses
habitually omit — alongside E/O–O/E + DAC/ADC. (iii) **Precision–accuracy link**: tie analog state SNR
at the detector (which the S0.3 noise model produces) to achievable task accuracy — an envelope in
throughput/energy alone, silent on precision, is not credible for an *accuracy-targeted* system. (iv)
**Operating scale stated** (N rings, rates) consistent with §9 risk 5. (v) Both-direction honesty per F1.

---

## 9. Recon integration

**Answer: the *task spec* (S0.0 in `task_queue.md`) has fully absorbed the recon — manifest-scoped, both
architecture constraints baked in, parked-Q guard present. The *roadmap and CLAUDE.md* have not (F17),
and the constraints should be promoted from task text to roadmap gates (F18).**

### F17 (HIGH) — The roadmap's S0.0 text contradicts the recon and the active task spec; fix before S0.1
`stage0_roadmap.md` S0.0 still instructs: *"fork from pnn-multilayer the ring/MRR forward model, the
differentiable/batched training engine…"* — the recon's central finding is that **both are
not-liftable** (ring physics is static/CW; MZI application is structural in the engine), and Lucas's D-1
ruling adopted the recon's seven-asset manifest instead. The roadmap's S0.0 deliverable ("physics-level
smoke test: one SiN add-drop ring → its Laplace pole") also contradicts the active task spec, which
explicitly defers the dynamical-pole test to S0.1 and scopes S0.0's smoke test to salvage validation
(static CW Lorentzian + registry checks). The plan-of-record must not disagree with the ruling documents
it claims to incorporate: **issue roadmap v3** updating S0.0 (manifest-scoped salvage; CW-static smoke
test; dynamical pole moved to S0.1's gate) — and fix the same stale list in CLAUDE.md ("Codebase plan"
section, "ring / MRR forward models; differentiable + batched training engine"). Trivial edits;
authority of the roadmap is what's at stake.

### F18 (MEDIUM) — Promote the two architecture constraints into roadmap gates (S0.3, S0.4b/c)
Constraints 3a (gradients flow through optical state) and 3b (full state trajectories exposed) currently
live only in the S0.0 task text. They bind hardest at S0.3 (substrate) and S0.4b/c (adjoint/RHEL need
trajectories; BPTT reference needs gradient flow). Add to the S0.3 gate: *"full state trajectories
exposed in the API; the BPTT reference trains through the substrate (end-to-end gradient flow
verified)"* — the second clause is also the operational test that the recon's `no_grad`/detach
anti-pattern was avoided, and S0.4/S0.5 need that BPTT reference anyway.

---

## Beyond the checklist (hostile-reviewer sweep)

### F19 (MEDIUM) — Missing physics with mapping-level consequences: backscatter/CW–CCW mode splitting; plus the general simulation-of-simulation caveat
Surface-roughness backscattering couples the ring's clockwise/counter-clockwise modes and **splits each
resonance into a doublet** — a well-documented, *prominent* effect precisely in the ultra-high-Q SiN
regime the proposal's memory story leans on (splitting becomes visible once the splitting rate rivals
κ_tot, i.e. exactly as Q grows). It directly threatens the architecture's core abstraction
(one ring = one complex pole). At foundry Q ≈ 2×10⁶ it is plausibly negligible; at the aspirational 10⁷
end it is not. **Recommendation:** S0.1 includes a literature-sourced bound on where splitting matters
(splitting-rate distributions vs κ_tot across the registered Q range); S0.3 carries an optional
splitting knob if the bound says it bites in-range; S0.8 carries it in the limits-of-model section
either way. More generally, the bake-off measures robustness to *modelled* imperfections only — the
twin-mismatch protocol's structural-omission axis (F7.2b) partially probes this; the S0.8 paper must
state the caveat explicitly (unmodelled physics — thermal transients, polarization, fab variation of
coupling gaps — could reorder methods on hardware).

### F20 (MEDIUM) — One task is a thin basis for a method-ranking headline; add a cheap synthetic secondary
A bake-off ranked on a single task invites the "does the ranking generalize?" review. Add a
**synthetic memory-task family with tunable memory length** (e.g. delayed recall / sticky detection at
parametric lag) as a pre-registered secondary: it is nearly free on the same harness, it stress-tests
the ranking's robustness, and it *directly* exercises the memory-length-vs-Q story (F13.2) that the
primary benchmark only samples at one point.

### F21 (MEDIUM) — No compute sizing anywhere in the plan
The bake-off grid is (4 methods + 2 baselines) × loss/gain/ASE cells × ≥8 seeds × passes-to-target ×
time-domain substrate steps per pass — with SPSA's per-update double passes and PAT's twin BPTT on top.
The house standard demands per-experiment runtime estimates; the *roadmap* should carry the aggregate
order-of-magnitude before S0.3 fixes substrate fidelity (substrate step cost is the lever that
multiplies through everything; a too-expensive substrate quietly forces seed/grid cuts later, which is
how the F11 statistics get eroded). Deliver with the S0.3/S0.4 specs; escalate to Lucas if it implies
cluster spend (per the standing always-ask rule).

### F22 (MEDIUM) — Incentive hygiene on the RHEL finding: pre-draft both conclusion templates
The roadmap twice frames the RHEL-on-SiN finding as the anchor for collaboration outreach — a structural
incentive to make that finding *interesting*. Cheap immunization: at S0.4c close (before any S0.5
results), pre-draft **both** conclusion templates — "RHEL trains competitively under honest echo
penalties at cell X" *and* "RHEL fails to train / trains only under idealized-conjugation conditions
banned by the contract" — and commit to publishing whichever the pre-registered metric selects, with the
cosine/bias-variance diagnostic confined to the mechanism discussion. A negative RHEL result under an
honest echo model is itself a publishable, outreach-worthy finding (it is the first quantitative
RHEL-on-a-dissipative-photonic-substrate number either way); saying so now removes the spin temptation
later. Relatedly (presentation, S0.8): the bake-off's novelty for PAT/SPSA is the *recurrent dissipative
setting*, not re-validating chip-demonstrated methods — frame accordingly.

---

## Bottom line for Lucas

The plan is the right plan: right phases, right gates, right primary metric, honest RHEL terms, and the
§10 premise treated as falsifiable before money. I am approving it **with edits** rather than amending
it, because every defect found is repairable by pre-registration entries and text changes without moving
a phase. The non-negotiables before the relevant phases run: **F7** (the fairness contract — without it
the bake-off's headline is an artifact of an unstated twin-mismatch choice), **F10** (gate semantics —
as worded, a marginal or even *failing* PAT/SPSA result can still walk onto hardware, and "exactness"
re-admits the demoted diagnostic as a promotion criterion), **F2** (target-vs-ceiling separation — else
Gate ii confounds device capacity with method quality), **F12** (the ledger that makes all of this
enforceable), and **F17** (make the plan-of-record agree with the recon it already paid for). The
Supervisor's early-envelope instinct is endorsed (F1) — with the task-selection coupling, it is worth
more than the kill-test it was proposed as.

*Filed by the Critic, 2026-06-08. Independent review; not subject to Supervisor revision — disputes
escalate via `shared/escalate_to_human.md`.*
