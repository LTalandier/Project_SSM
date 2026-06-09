# Critic Review — PR-15 white-space gate: blind adversarial pass + criterion audit + F14 reconciliation

**Reviewer:** Critic session · **Date:** 2026-06-09 · **Spec:** `critic_instructions_whitespace-pr15.md`
**Status: PART 1 of 2.** The Executor memo (`docs/s0_L/debt1_whitespace_search.md`) **was not yet filed**
when this pass ran, so spec items 2 (memo audit) and 5 (final gate verdict) are **PENDING**; this part
delivers item 1 (blind adversarial search — run first, blind, as required), item 3 (criterion audit),
and item 4 (F14 reconciliation). Part 2 will be appended when the memo lands.

> **Executor: do not read this file until your S0.L-1 memo is committed** — two-modality independence.
> The blind pass below was completed 2026-06-09 with the full query trail in the Appendix, before any
> Executor output existed to read.

---

## Provisional verdict (what Lucas needs to know now)

1. **No prior found that kills the claim as intended** — i.e. machine-learning training of the physical
   recurrent parameters of a photonic recurrence. ~100 logged queries across five lanes (adaptive
   photonic filters 1985–2015; intracavity/laser adaptive control; delay-RC + Bueno/Brunner hostile
   read; 1980s–90s optical neural networks; modern 2015–2026 + Ising/quantum). The two strongest
   *supports* found: Hermans et al. PRL 2016 ran **physical backprop through a photonic delay loop and
   explicitly declined to train the loop parameter** ("optimising the parameters (input scaling, bias
   scaling and feedback gain) on the hardware would be too costly in terms of time" — supplementary);
   and the field's own survey (Buckley et al., *Photonic online learning: a perspective*, Nanophotonics
   2023) lists every in-situ demo as feedforward, citing recurrent application of SPSA as theoretical
   potential only.
2. **But the frozen kill-rule is defective: q1∧q2∧q3 with no task-objective condition is satisfied, by
   the letter, by hardware demos nobody would accept as "training a photonic RNN"** — dither-locked
   cavity servos (1988→2015) and gradient/policy-gradient optimization of intracavity laser parameters
   for mode-locking (2021–2024, incl. one explicit two-point finite-difference gradient on intracavity
   waveplates). The rule operationalized "training" purely as the update-rule class (q3) and left the
   *objective* undefined. **Amendment proposed below (WS-F1); PR-15 is frozen, so it requires Lucas's
   sign-off.** This is urgent because the Executor is classifying against the defective rule right now.
3. **Four AMBIGUOUS candidates escalated with primaries** (per the frozen disposition: never adjudicated
   in-pipeline): **Böhm 2022** (hardware-in-the-loop Boltzmann-machine *gradient* training of an
   optoelectronic Ising machine's couplings — survives even the amended rule on everything except
   parameter physicality; the single most dangerous prior found), **NTT Photonic Compute-in-Wire 2025**
   (intra-loop trained modulations, "in-situ on-the-fly training" claimed, full text unreached),
   **Mak/Bois/Poon 2016** filter-synthesis line (pole+coupling updated on hardware toward a target
   transfer shape; algorithm class unverified), **Fisher 1987** (Widrow-Hoff on LCLV associative
   hardware; loop topology unresolved).
4. **Gate call:** cannot be returned under the frozen letter (the letter is satisfiable by servo-class
   priors → meaningless); **under the amended rule the blind pass is consistent with PASS (one-sided)**,
   pending the Part-2 memo audit, the A1–A4 dispositions, and Lucas's amendment sign-off. Formal output
   today: **AMEND (criterion) + AMBIGUOUS-escalate (4 candidates) + no-FATAL-found (blind pass)**.

---

## 1. Findings

### WS-F1 (CRITICAL) — The kill-rule is missing the task-objective condition; as frozen it is satisfied by the cavity-servo and laser-regime-optimization literatures

**The hole.** q3 admits "zeroth-order perturbative (… estimates a descent direction from perturbation
measurements)". Dither/lock-in locking, perturb-and-observe tuning, extremum-seeking, and SPGD are
exactly that. q1 admits any pole-defining parameter; a cavity length or ring heater *is* one. q2 admits
any closed loop on hardware. Nothing in the rule asks **what objective** the update serves. Verified
instances that therefore satisfy q1∧q2∧q3 as written:

- **Jayatilleka et al., Opt. Express 23:25084 (2015)** — perturb-and-observe (finite-difference-sign)
  updates of in-resonator photoconductive heaters of 1st- and 2nd-order **coupled-ring** filters during
  live data transmission ("IPD is measured before and after changing P. If IPD increases, then the sign
  of ΔP is unchanged… Otherwise, the sign of ΔP is reversed" — full text verified). Intracavity phase =
  pole position; closed loop; FD-class rule.
- **Padmaraju et al., JLT 32:505 (2014)** — dither/lock-in error signal driving a microring heater
  (wavelength locking). Abstract-level verified.
- **Kaminow et al. (~1988–1990)** — fiber-Fabry-Perot channel filters dither-locked to the selected
  channel during transmission (patent-corroborated). The archetype is PDH locking (1983).
- **Pu et al., arXiv:2306.06565 (2023)** — explicit **two-point finite-difference gradient** on
  intracavity waveplate angles of an NPR fiber laser, on hardware, ~19 iterations to mode-lock ("The
  gradient algorithm... updates the parameters in the direction corresponding to the negative gradient"
  — full text verified; preprint-only).
- **Yan et al., Photonics Res. 9:1493 (2021)** and **Kokhanovskiy et al., Nanophotonics 13:2891
  (2024)** — deep-RL (TD3 / Soft Actor-Critic = policy-gradient family, on the q3-pass list) trained
  **on the physical laser** (45 h on hardware in the 2024 paper), setting intracavity polarization /
  gated-saturable-absorber modulation depth (= intracavity nonlinear loss) and pump.

None of these trains an input→output computation; all regulate or optimize the device's own operating
regime (lock to a resonance; attain/maintain mode-locking). A hostile reviewer can nevertheless quote
Pu 2023 against the claim sentence *as currently worded*. The fix belongs in the rule **and** in the
eventual claim wording.

**Proposed amendment (requires Lucas sign-off; log as a dated amendment under PR-15, keeping the v1
text per the ledger's supersession discipline):**

> **q4 — task-objective condition.** The update minimizes a loss defined over the system's
> **input→output behavior on a computational task** (a corpus of input–output examples, with the
> trained system evaluated on inputs beyond the tuning set). Regulation of the device's own operating
> point — setpoint/resonance locking, stabilization, alignment, regime attainment or maintenance (e.g.
> mode-locking, comb states) — does **not** satisfy q4, regardless of update rule. A prior is FATAL iff
> q1∧q2∧q3∧**q4**.
>
> Secondary clarification (RL class): in controller-RL demos the policy-gradient lands on the
> *controller network's* digital weights; the physical parameters are set as *actions*. Such priors fail
> q4 here anyway, but record the distinction — a future prior should only count if the physical
> recurrent parameters are themselves the trained weights of the learning system.

Consequences to record with the amendment: (i) the servo class becomes citable lineage, not a threat;
(ii) the laser-RL class likewise (cite Yan/Kokhanovskiy — they are the closest "gradient-estimating
updates of intracavity parameters on hardware" relatives); (iii) the **transfer-function-synthesis
class lands on the q4 boundary** (a target filter response *is* an input→output objective) — see WS-F4;
the "evaluated beyond the tuning set" clause is what cleanly separates learning from filter synthesis,
and the paper's claim sentence should carry the same qualifier ("…by gradient-based/-estimating
training **on a computational task**").

### WS-F2 (HIGH) — Böhm 2022 makes the hybrid-digital-recurrence class live, and q4 does NOT defuse it; the claim needs the parameter-physicality qualifier

**Böhm, Verschaffelt, Van der Sande et al., Nat. Commun. 13:5847 (2022)** ("Noise-injected analog Ising
machines enable ultrafast statistical sampling and machine learning"): a time-multiplexed
**opto-electronic** Ising machine used as the Gibbs sampler inside **unsupervised Boltzmann-machine
training** — couplings J_ij updated every iteration from hardware samples via the BM **log-likelihood
gradient**, "with equal accuracy as software-based training" (full text verified). Score it: q2 YES
(hardware sampling inside the training loop); q3 YES (estimated likelihood gradient); **q4 YES — this
is a genuine ML task** (unsupervised learning on data), unlike everything in WS-F1. The *only* line of
defense is q1: the J_ij live as **digital numbers in the in-loop FPGA**; the analog opto-electronic part
of the recurrence carries no trained parameter, and the recurrence itself is hybrid (optical
nonlinearity, electronic coupling/memory).

The frozen disposition anticipated the *class* ("hybrid digital recurrence" → AMBIGUOUS, escalate,
never adjudicated in-pipeline) — credit where due — so **Böhm goes to Lucas with the primary attached**
(https://pmc.ncbi.nlm.nih.gov/articles/PMC9532389/ · arXiv:2112.11534). My recommendation, for Lucas to
accept or reject: the claim wording must make explicit what q1 only implies — *the updated parameters
are physical (analog) degrees of freedom of a photonic recurrence, and the recurrent state is carried
in the photonic system* — and the paper should cite Böhm by name as the hybrid boundary case rather
than hoping nobody notices. Watch item: any follow-up (VUB group; NTT measurement-feedback CIM line)
that moves the couplings into the analog/optical domain while keeping hardware-in-the-loop gradient
updates **flips this to FATAL** (WS-F8).

### WS-F3 (HIGH) — "Recurrence" is undefined with respect to weight-tying; the NTT Compute-in-Wire line exploits exactly that gap and its q2 status is unresolved

**M. Nakajima et al., "Photonic Compute-in-Wire: Remotely Driven Photonic DNN with a Single Nonlinear
Loop," Adv. Devices & Instrumentation (2025), doi 10.34133/adi.0121**: a folded-in-time DNN whose
trained weights ARE temporal modulations applied **inside a physical fiber loop** ("The parameters of
the constructed photonic FiT-DNN were trained by using a digital twin…"), with separate claims of
"in-situ, on-the-fly training" and GBaud online tracking. Full text unreached (publisher + mirrors
403; no arXiv found) — q2 (twin = simulate-then-deploy vs PAT-style physical-forward) **unverified**.

The conceptual problem is prior to the verification: the loop is *physically* recurrent, but the
computation is an **unrolled feedforward network** — each circulation applies a *different* layer's
weights, and no state is carried across input samples. The same issue covers per-time-bin-programmed
loop processors (time-bin interferometers). The frozen rule's q1 ("parameters that define the recurrent
map") does not say which notion of recurrence governs, so the Executor could defensibly call this
either way. **Amendment rider (same sign-off):**

> For q1, "recurrence" means a **weight-tied iterated map carrying state across the input sequence**
> (the parameters define poles/memory over the task's time axis). Time-multiplexed implementations of
> feedforward architectures (folded-in-time DNNs; loop processors with per-pass reprogrammed elements)
> do not satisfy q1, however physically recirculating the hardware is.

Action: obtain the ADI 2025 full text (institutional access) before the claim sentence freezes; if its
online tracking updates intra-loop modulations from physical measurements, the paper must state this
boundary explicitly rather than rely on the unstated definition.

### WS-F4 (MEDIUM) — The filter-synthesis boundary: Mak/Bois/Poon shape their rings' poles *and couplings* on hardware toward a target response; survival currently rests on an unverified algorithm class

**Mak, Bois, Poon (2016), "Programmable multiring Butterworth filters with automated resonance and
coupling tuning"** (IEEE, + OFC 2016 Tu2F.4): ring resonances **and inter-ring coupling** — precisely
the B1 parameter classes — updated on a physical Si chip until the response matches a target Butterworth
shape ("automatically… set to an optimal Butterworth shape… automatically compensates for fabrication
variations and thermal crosstalk"). q1 YES, q2 YES; reported (secondary-source) algorithm: coordinate
descent + Nelder-Mead, ~346 function evaluations — **direct search, fails q3 — but NOT VERIFIED from
the primary**. Kin: Mak et al. 2015 (5th-order alignment, arXiv:1507.02129, "using a feedback system",
algorithm unstated) and Shawon & Saxena, arXiv:2205.12048 (2022) (in-situ reconfiguration of RF-photonic
ring filters from physical measurements; likely Nelder-Mead-class, unverified).

Under the amended rule these sit exactly on the q4 line (target response = an input→output objective;
no generalization beyond the tuning objective = not a learning task). Required actions: (1) verify the
algorithm class from the primaries before the paper — if any stage is dither/gradient-estimating, bring
it back to Lucas, because then only the "computational task / evaluated beyond the tuning set" clause
separates it from the claim; (2) cite this line in the paper as the **nearest classical kin** regardless
of outcome (pole-and-coupling tuning on hardware exists; *learning* is what doesn't).

### WS-F5 (MEDIUM) — q3 taxonomy gaps: Bayesian optimization, direct search, annealing, value-based RL, gradient-surrogates are unclassified

The frozen q3 excludes only "population-selection methods (genetic/evolutionary/CMA-ES/Boolean/
exhaustive search)". Unclassified, all encountered in the blind pass: **Bayesian optimization**
(Morozko et al., ACS Photonics 2025 — *in-situ* optimization of an OEO reservoir's loop gain, phase
bias, and delay, i.e. pole-defining knobs, "For the optimization, a Bayesian algorithm was employed…
along with random search"; one algorithm swap from a kill — must-cite); **comparison-based direct
search** (Nelder-Mead, coordinate/pattern search, Rosenbrock — the auto-mode-locking and
filter-synthesis workhorses); **simulated annealing**; **value-based RL** (DQN/DDQN — Kuprikov et al.
2022, sim-trained anyway); **greedy accept/reject Boolean flips** (Bueno/Andreoli describe them in
gradient *language* — "the error gradient is probed…" — but the update forms no gradient estimate;
classify explicitly as selection); **aDFA-style gradient surrogates** (Nakajima et al., Nat. Commun.
2022 — fixed random projection of the error; trained masks/readout only, so q1 fails there regardless).
Amendment rider: enumerate all of the above as non-q3 (non-fatal-but-cite), and define q3 positively as
*forming an explicit local gradient/descent-direction estimate* (FD, SPSA, SPGD, dither/lock-in,
extremum-seeking, MGD) *or an analytic/algorithmic gradient* (BP, adjoint, EP, parameter-shift,
policy-gradient, likelihood gradient).

### WS-F6 (LOW) — q2 handles on-device fine-tuning correctly; instruct the Executor accordingly

Answer to the spec's direct question: a prior that pretrains offline and **fine-tunes the recurrent
parameters on the device** satisfies q2 for the fine-tuning phase (updates applied on hardware,
physical forwards) — and *should*: it would be a genuine, if weaker, demonstration. No amendment
needed; the Executor must not clear such priors on q2. One live instance found: arXiv:2604.02429
(2026), photonic-CNN pretrain + in-situ SPSA fine-tune — **feedforward**, dies on q1, non-fatal.

### WS-F7 (MEDIUM) — Fisher 1987 is the one 1980s candidate that could still flip; full-text it before the paper

**Fisher, Lippincott, Lee, Appl. Opt. 26:5039 (1987)** (+ Proc. SPIE 625:196, 1986; NRL): "actual
laboratory optical implementations of associative modules based on Hebbian **and Widrow-Hoff** learning
rules… including successful experimental demonstrations" — Widrow-Hoff = LMS = q3 YES, in-hardware =
q2 YES. Unresolved: q1 — whether any demonstrated configuration ran the adaptive weight matrix inside a
**closed optical loop** during learning (his architecture papers compose modules with feedback), or
open-loop single-pass association. Everything else in the 1980s–90s lane bifurcates cleanly (gradient
demos feedforward: Hsu/Brady/Psaltis 1987 perceptron, Yoshinaga 1989, Qiao/Psaltis 1992–93, Mitsubishi
neurochips; in-loop adaptation Hebbian/competitive: D.Z. Anderson photorefractive ring-resonator
circuits; corroborated by Guo et al. arXiv:1912.12256: "Developing an all-optically trained ONN…
remains an unsolved problem"). Cheap interlibrary scan resolves it; do so by S0.8 at latest.

### WS-F8 (MEDIUM) — Named watchlist for the dated S0.8 final sweep (the claim's live threats are forward, not backward)

PR-15 already mandates a dated final sweep at S0.8; register these names in it now: (1) **MGD →
recurrent** — Guo, Aadhi, …, Tait, Shastri (arXiv:2506.18041): fully analog multiplexed-gradient-descent
training demonstrated on an MRR weight-bank chip (feedforward demo), i.e. q2∧q3 already on the
**canonical recurrent substrate** (Tait 2017 broadcast-and-weight CTRNN); a loop-back version is one
wiring change from FATAL. (2) **Böhm/VUB + NTT CIM "learning-to-sample"** follow-ups with analog
couplings (flips WS-F2). (3) **Winters et al., Opt. Express 25:33216 (2017)** — identify the "local"
optimizer on intracavity LC retarders (full text blocked this pass); if gradient-type, it joins the
WS-F1 exhibit list (q4 still defuses). (4) **NTT FiT-DNN online tracking** (WS-F3). (5) **Brunner-group
online/gradient variants** beyond greedy Boolean. None of these is fatal *today*; any could be by the
paper's submission date — which is exactly why the one-sided-PASS semantics (a clean search never
certifies) was the right freeze.

---

## 2. Critic candidate table (blind pass)

Verdicts under both readings: **L** = frozen letter (q1∧q2∧q3), **A** = amended rule (… ∧q4 + WS-F2/F3
qualifiers). Verification status per row; primaries for escalated rows linked in §1.

| # | Prior | What's updated, where | q1/q2/q3/q4 | L | A | Verified? |
|---|-------|----------------------|-------------|---|---|-----------|
| S1 | Jayatilleka 2015, Opt. Express 23:25084 | Intracavity heaters, coupled-ring filter, live link | Y/Y/Y(FD-sign)/N (alignment servo) | FATAL-by-letter | non-fatal-cite | full text |
| S2 | Padmaraju 2014, JLT 32:505 | Ring heater, dither lock | Y/Y/Y(dither)/N | FATAL-by-letter | non-fatal-cite | abstract |
| S3 | Kaminow ~1988–90, FFP channel filter | Cavity length, dither lock in transmission | Y/Y/Y(dither)/N | FATAL-by-letter | patent-corrob. |
| R1 | Pu 2023, arXiv:2306.06565 | Intracavity waveplates, NPR laser | Y/Y/Y(2-pt FD)/N (mode-lock merit) | FATAL-by-letter | non-fatal-cite | full text |
| R2 | Yan 2021, Photon. Res. 9:1493 | Intracavity polarization via EPC (TD3 actor) | Y/Y/Y(policy-grad fam.)/N | FATAL-by-letter | non-fatal-cite | abstract+ |
| R3 | Kokhanovskiy 2024, Nanophotonics 13:2891 | Gated-SA modulation depth + pump (SAC, 45 h on hardware) | Y/Y/Y(policy-grad fam.)/N | FATAL-by-letter | non-fatal-cite | full text |
| A1 | **Böhm 2022, Nat. Commun. 13:5847** | BM couplings J_ij (digital, in-loop FPGA) of optoelectronic Ising sampler; likelihood-gradient from hardware samples | q1 *hybrid/digital*/Y/Y/**Y (ML task)** | **AMBIGUOUS** | **AMBIGUOUS → Lucas** | full text |
| A2 | NTT Compute-in-Wire 2025, ADI 10.34133/adi.0121 | Intra-loop temporal weight modulations; folded-in-time feedforward | q1 *defn-dependent*/q2 **unverified**/Y/Y | AMBIGUOUS | AMBIGUOUS → Lucas | abstract only |
| A3 | Mak/Bois/Poon 2016 (+2015; Shawon 2022) | Ring resonances + inter-ring coupling → target Butterworth shape, on chip | Y/Y/q3 *unverified (NM-class?)*/boundary | AMBIGUOUS | AMBIGUOUS → verify | abstract |
| A4 | Fisher 1987, Appl. Opt. 26:5039 | LCLV adaptive weights, Widrow-Hoff, in hardware | q1 *unresolved*/Y/Y/Y? | AMBIGUOUS | AMBIGUOUS → full-text | abstract |
| N1 | Hermans 2015 NC 6:6729 + 2016 PRL 117:128301 | Input/bias/output masks via *physical* BPTT; loop gain μ fixed, declared too costly to train on hardware | N/Y/Y/Y | clear | **anchor-cite (supports)** | full texts |
| N2 | Antonik 2017 PRApplied 7:054014 (+NPL 2018) | Readout (FPGA), offline ridge, teacher-forced; weights constant during closed-loop autonomy | N(readout)/partial/N(ridge)/Y | clear | cite + boundary argument | full text |
| N3 | Bueno 2018 Optica 5:756; Porte 2021; Andreoli 2020 | Boolean DMD readout, greedy accept/reject; β,γ scanned | N/Y/N(selection)/Y | clear | cite (named pre-emption) | full text |
| N4 | Lugnan 2025, Adv. Sci. 12:2404920 | GST patches ON recurrent photonic elements self-modify in situ (emergent plasticity) | **Y/Y**/N(no gradient)/Y | non-fatal-cite | **must-cite** (nearest internal-params-changed prior) | full text |
| N5 | Morozko 2025, ACS Photonics 12:5097 | OEO reservoir loop gain/phase/delay, in situ, Bayesian+random | partial(digital loop)/Y/N(BO)/Y | non-fatal-cite | must-cite ("one swap from fatal") | full text |
| N6 | Laydevant 2024, Nat. Commun. 15 | D-Wave couplings via equilibrium propagation, hardware-in-loop | Y/Y/Y/Y — **not photonic** | non-fatal-cite | cite ("photonic" load-bearing) | title-level |
| N7 | Feedforward in-situ canon: Pai Science 2023; Xue FFM Nature 2024; Bandyopadhyay Nat. Photon. 2024; Ashtiani Nature 2026 (full on-chip BP); Guo MGD 2025; Zhan 2024 (REINFORCE-on-SLM) | All feedforward | N/Y/Y/Y | clear | cite as canon-stops-at-recurrence | full texts |
| N8 | 1980s–90s: Hsu/Brady/Psaltis 1987; Yoshinaga 1989; Qiao/Psaltis 1992; D.Z. Anderson resonator circuits; Tait 2017 (programmed CTRNN); Spagnolo 2022 (QRC simulated) | Gradient⇒feedforward; in-loop⇒Hebbian/fixed/programmed | various, all one-q-short | clear | cite (lineage ¶) | mixed |

**Cross-check seed for Part 2:** the Executor memo will be audited against this table — in particular
whether it found A1 (Böhm), N4 (Lugnan), N5 (Morozko), A2 (FiT-DNN), the laser-RL class, and the servo
class at all, and whether any of its "clear" verdicts contradict a verified row above.

---

## 3. Criterion audit (spec item 3) — summary

The q1∧q2∧q3 skeleton is **sound** (each condition is individually load-bearing and the blind pass
confirms every lane's priors die on exactly one of them) but **incomplete in four places**, three with
live exploits found: missing q4 task-objective condition (WS-F1 — exploited by servo + laser-regime
classes); missing parameter-physicality / photonic-state-carrier qualifier (WS-F2 — exploited by Böhm);
missing weight-tied recurrence definition (WS-F3 — exploited by FiT-DNN); under-enumerated q3 taxonomy
(WS-F5 — BO/direct-search/value-RL/surrogates unclassified). q2 is correct as frozen, including the
fine-tuning case (WS-F6). The disposition machinery (AMBIGUOUS → Lucas, never in-pipeline; one-sided
PASS) is right and anticipated the hybrid class. **Amendment text: WS-F1 block + WS-F3 rider + WS-F5
enumeration; log as dated PR-15 amendment, frozen v1 retained.** Until signed, the Executor's verdict
table should be read with the L/A dual-column lens above.

## 4. F14 reconciliation (spec item 4)

**Confirmed — no conflict, and the ledger placement is correct.** My roadmap-F14 was a *dependency*
statement: debts #2/#3 sit on the critical path (consumed at S0.2/S0.3) and must front-load; for #1 and
#4 it said S0.8-pacing **suffices** — a permission, not a prescription. D-09-1 front-loads #1 on a
different, orthogonal axis: *value-at-risk scheduling* (a cheap kill-shot must run before the spend it
could invalidate). Both lenses now coexist in roadmap v3.1's per-debt pacing (line 271: #1 → pre-S0.2 ·
#2 → S0.2 · #3 → S0.3 · #4 → S0.8), and F14's load-bearing content (#2/#3 front-loading) is intact — I
verified the v3.1 graph note directly. D-09-1 strictly improves on F14's placement of #1.

**Does the go/no-go belong in the PR ledger? Yes.** Freezing the kill-rule *before* the search is the
literature-search analog of pre-registering the analysis before the data: it removes the post-hoc
temptation to lawyer any found prior out of fatality. This review is the existence proof that the
discipline works — the rule turned out defective, and the defect is being fixed by a **visible, dated,
human-signed amendment** rather than by silent reinterpretation during classification. That is the
ledger doing its job. (Refinement: amendments to frozen entries should follow the ledger's own
supersession discipline — keep v1, date the change, record the trigger — as proposed above.)

## 5. PENDING — Part 2 (spec items 2 + 5)

When `docs/s0_L/debt1_whitespace_search.md` lands: (a) audit **every q1 call** against primaries
(motivated-reasoning hotspot); (b) hostile re-read of every "clear" on lanes (ii)/(iii); (c) the
Bueno/Brunner boundary memo vs my verified ground truth (greedy = selection, not gradient; recurrence
params fixed/scanned; Hermans masks-only with loop gain pinned; Antonik teacher-forced offline ridge,
weights constant when the loop closes); (d) flag any verdict resting on a source the Executor did not
reach (the B2/F5 lesson); (e) symmetric-difference of the two candidate sets (above); (f) reproducibility
of the Executor's trail. Final gate verdict then issues as: **PASS (one-sided)** iff memo audit clean ∧
amendment signed ∧ A1–A4 dispositioned by Lucas; **FATAL** iff any candidate survives the amended rule;
**AMBIGUOUS-escalate** otherwise.

---

## Appendix — reproducible blind-search trail (item 1 requirement)

Five independent search agents, 2026-06-09, ~100 web queries total + primary-source fetches. Full query
logs verbatim, per lane:

**Lane A — adaptive photonic/RF-photonic filters 1985–2015 (20 queries):** adaptive dispersion
compensation ring resonator dither feedback control · Madsen adaptive all-pass filter dispersion
compensation ring resonator feedback · tunable dispersion compensator automatic feedback BER monitor
closed-loop all-pass filter experiment · Madsen integrated all-pass filter PMD compensator feedback
control degree of polarization algorithm · recirculating delay line adaptive optical filter loop gain
LMS fiber-optic signal processing · adaptive microwave photonic filter LMS algorithm experiment IIR
recursive · Gires-Tournois etalon tunable dispersion compensator feedback control dithering experiment ·
Sandel Noe "fully automatic" chromatic dispersion compensation 40 Gbit/s Electronics Letters tunable
compensator type · all-pass filter ring resonator dispersion compensator adaptive closed-loop eye
monitor 40 Gb/s Lucent OFC experiment · automatic dispersion equalization 40 Gbit/s VIPA clock power
feedback control Fujitsu Ishikawa Ooi · Takiguchi dispersion equalizer ring resonator planar lightwave
circuit automatic compensation experiment NTT · microring resonator wavelength locking dithering signals
thermal stabilization feedback Padmaraju · "automatic resonance alignment" high-order microring filters
Mak Poon algorithm tuning · adaptive fiber-optic filter 1980s Stanford Shaw Moslehi Goodman LMS adaptive
delay line processor recirculating · Jayatilleka photoconductive heaters microring tuning algorithm
maximize photocurrent sequentially thesis · Madsen all-pass filter compensator "feedback" automatic
adjustment demonstration JLT 2004 polarimeter PMD closed loop · adaptive microwave photonic notch filter
recirculating loop gain amplifier feedback adjustment experiment interference mitigation · fiber
Fabry-Perot filter dither lock feedback channel selection FDM optical network Kaminow 1989 1990 · Mak
Bois Poon programmable multiring Butterworth filters automated resonance coupling tuning JSTQE arXiv
Nelder-Mead · "tunable dispersion compensator" etalon feedback "hill climbing" OR dithering OR
"gradient" automatic 43 Gb/s experiment. *Fetched:* US6842547 (Google Patents, verified); EP0165773A2
(verified); ar5iv 1507.00686 (full text); OFC-2002-FD9, OFC-2016-Tu2F.4, arXiv 1507.02129 / 2205.12048
abstracts; several blocked (IEEE 418, Optica JS-gate).

**Lane B — intracavity/laser adaptive control (21 queries):** "intracavity" "deformable mirror" SPGD
"stochastic parallel gradient" laser · Lubeigt intracavity adaptive optics laser mode control
hill-climbing algorithm Opt Express 2002 · self-tuning fiber laser extremum-seeking control experiment
Kutz Brunton Fu polarization controllers · Ping Yang intracavity deformable mirror solid-state laser
hill-climbing algorithm beam quality improvement · automatic mode-locking fiber laser "stochastic
parallel gradient descent" experiment polarization controller · "optoelectronic oscillator" intelligent
self-optimizing adaptive loop algorithm phase noise optimization experiment · reinforcement learning
mode-locked fiber laser experimental demonstration polarization controller intracavity · random laser
adaptive pump shaping optimization algorithm Nature Physics Bachelard Gigan Sebbah experiment · laser
resonator automatic alignment SPGD algorithm cavity mirror experiment optimization output power · Yan
"low-latency deep-reinforcement learning" ultrafast fiber lasers Photonics Research 2021 TD3 experiment
mode-locking · "optoelectronic oscillator" "machine learning" OR "neural network" OR "reinforcement
learning" automatic tuning mode selection experiment loop · coherent beam combining "common cavity" OR
"shared resonator" intracavity phase control SPGD dither experiment fiber lasers · "extremum seeking"
experimental laser cavity hardware demonstration mode-locked OR "frequency comb" OR resonator control ·
soliton microcomb generation optimization "Bayesian" OR "reinforcement learning" OR "gradient descent"
OR dither feedback experiment intracavity detuning pump · Cherezova Kudryashov intracavity bimorph
mirror super-Gaussian output formation algorithm 1998 Vdovin Kiyko 200-W Nd:YAG micromachined deformable
mirror control · "DELAY" algorithm Yan Jiang 2021 deep reinforcement learning fiber laser "polarization
controller" trained online real laser experiment recovery vibration · "intelligent" OR "smart"
optoelectronic oscillator automatic optimization FPGA algorithm gradient mode hopping suppression
experiment · Michelson cavity coherent combining two fiber lasers intracavity phase modulator active
feedback dither hill climbing experiment · "intracavity" "spatial light modulator" laser closed-loop
optimization feedback algorithm mode shaping experiment · automatic mode-locking fiber laser experiment
"gradient descent" OR "Nelder-Mead" OR "simplex" OR "Rosenbrock" algorithm polarization search
Radnatarov Kobtsev · Winters Kirchner Backus "Electronic initiation and optimization of nonlinear
polarization evolution mode-locking" algorithm genetic simplex gradient liquid crystal. *Fetched:*
Lubeigt OE 2002 (full); Pu arXiv:2306.06565 (full); Kokhanovskiy PMC11501165 (full); Kuprikov SciRep
2022 (full); Yan PRJ abstract (verbatim); Morozko arXiv 2502.11126 (HTML); Brunton/Fu/Kutz JQE 2013 PDF.

**Lane C — delay-RC + Bueno/Brunner hostile read (20 queries):** Hermans "Trainable hardware for
dynamical computing using error backpropagation through physical media" Nature Communications 2015
trained parameters input mask feedback · Hermans "Embodiment of learning in electro-optical signal
processors" Physical Review Letters 2016 arXiv · Antonik Haelterman Massar "Brain-inspired photonic
signal processor" "Physical Review Applied" 2017 output feedback pattern generation chaotic emulation
arXiv · Antonik Duport Hermans Smerieri "online training" opto-electronic reservoir FPGA gradient
descent channel equalization which weights updated · Antonik "output feedback" reservoir computer online
training gradient descent pattern generation ICONIP "Neural Processing Letters" FPGA · Bueno Maktoobi
Froehly Fischer Larger Brunner "Reinforcement learning in a large-scale photonic recurrent neural
network" Optica 2018 arXiv greedy algorithm Boolean DMD readout weights · Antonik Haelterman Massar
"Cognitive Computation" 2017 photonic reservoir output feedback online training pattern generation
Mackey-Glass · Porte Skalli Haghighi Reitzenstein Fischer Brunner 2021 "autonomous" photonic neural
network VCSEL "Journal of Physics Photonics" learning Boolean weights evolutionary · Antonik "Random
pattern and frequency generation using a photonic reservoir computer with output feedback" arXiv online
learning simulation experiment · Andreoli Skalli Brunner "Boolean learning" photonic neural network
noise 2020 OR 2021 gradient descent DMD; Brunner group online gradient learning photonic recurrent
network 2022 2023 2024 · FORCE learning hardware implementation photonic optoelectronic experiment RLS
recursive least squares output feedback closed loop · "FORCE" training photonic reservoir computer
experiment "output feedback" online RLS closed-loop weights updated while loop closed Antonik conceptor ·
Antonik Gulina Pauwels Massar "Using a reservoir computer to learn chaotic attractors" Physical Review E
2018 experiment FPGA training ridge regression teacher · Nakajima 2022 "Physical deep learning with
biologically inspired training method" Nature Communications augmented direct feedback alignment
optoelectronic delay reservoir which parameters updated input mask · folded-in-time deep neural network
Fit-DNN experimental hardware optoelectronic delay loop modulated feedback backpropagation Stelzer
Yanchuk demonstration · "Photonic Compute-in-Wire" "single nonlinear loop" photonic deep neural network
2025 training in situ arXiv · NTT Nakajima "compute-in-wire" OR "folded-in-time" photonic deep neural
network fiber loop training digital twin arXiv preprint 2025 online tracking GBaud · photonic reservoir
computing hardware-in-the-loop optimization feedback gain Bayesian optimization SPSA evolutionary
hyperparameter experiment delay loop attenuator · Hermans Soriano Dambre Bienstman Fischer "photonic
delay systems as machine learning implementations" JMLR 2015 backpropagation through time trained input
mask parameters model offline experiment · Lupo Picco Massar "deep photonic reservoir" Optica 2023
frequency multiplexing "hidden layer" connections trained backpropagation analog hardware in the loop.
*Fetched (full texts):* arXiv 1610.06269 incl. supplementary; PMC4382991; arXiv 1802.02026; ULB
antonik2015online; arXiv 1711.05133; PMC9792515; arXiv 2506.18041; arXiv 2305.08892; abstracts of
2012.10615, 2312.06558; SPJ adi.0121 blocked (403).

**Lane D — 1980s–90s optical NNs / photorefractive (20 queries + 12 fetches):** Farhat Psaltis 1985
"optical implementation of the Hopfield model" weights mask feedback learning · Psaltis Brady Wagner
"adaptive optical networks using photorefractive crystals" 1988 perceptron learning experiment · D.Z.
Anderson photorefractive ring resonator neural network self-organizing learning circuits novelty filter ·
A.D. Fisher "optical implementations of associative networks" adaptive learning Widrow-Hoff LCLV 1987
Applied Optics · Farhat "self-programming" optoelectronic neural net stochastic learning simulated
annealing experimental 1987 1989 · "Experimental studies on learning capabilities of optical associative
memory" Applied Optics 1990 · Wagner Psaltis "multilayer optical learning networks" backpropagation
experimental demonstration photorefractive recurrent · Hsu Brady Psaltis "experimental demonstrations of
optical neural computers" 1988 perceptron Hopfield loop photorefractive · Benkert Anderson
"winner-take-all" photorefractive ring oscillator competitive learning rule 1991 · Qiao Psaltis
photorefractive two-layer optical network learning experimental 1992 "local learning" · "recurrent"
optical neural network photorefractive feedback weights trained in hardware experiment 1990 1995
backpropagation · Anderson "photorefractive" ring resonator "learning" Hebbian competitive rule
"self-organizing" Optics 1992 review circuits adaptive interconnections · Kyuma Ohta optical neurochip
learning GaAs Mitsubishi recurrent Hopfield feedback weight update experiment · Vorontsov nonlinear
optical feedback LCLV "learning" OR "adaptive" parameter training synergetics 1990s wavefront stochastic
parallel gradient descent intracavity · "recurrent backpropagation" OR "backpropagation through time"
optical implementation experimental demonstration holographic 1990s · optical "bidirectional associative
memory" adaptive learning experimental implementation photorefractive OR LCTV delta rule weights
updated · Farhat 1991 1992 optoelectronic "learning machine" experimental demonstration stochastic
Boltzmann annealing weights hardware Penn · "D. Z. Anderson" photorefractive circuit supervised OR
perceptron OR error-driven training task demonstration 1993 1994 1995 · PhD thesis SPIE "adaptive
optical neural network" recurrent feedback photorefractive gradient descent learning experimental 1990s
Caltech Colorado · Ishikawa "optical associatron" learning rule outer product orthogonal learning MSLM
Hamamatsu error correction. *Fetched:* NIPS-1987 Hsu/Brady/Psaltis (full); arXiv 1912.12256 (Guo et al.,
partial); Optica/AO abstracts (ao-26-23-5039, ao-27-9-1752, ao-29-2-289, ol-16-10-744, ao-32-8-1354,
ao-32-8-1399, ol-19-9-655, OPTCOMP-1985-WB4); PubMed 19752945.

**Lane E — modern 2015–2026 + Ising/quantum (30 queries):** "in situ training" recurrent photonic
neural network experiment hardware · on-chip training photonic recurrent neural network 2025
demonstration · Hermans "backpropagation through physical media" trainable hardware dynamical delay
system which parameters trained · Antonik online training photonic reservoir computer output feedback
FPGA gradient descent · Tait Shastri Prucnal microring weight bank recurrent silicon photonic neural
network trained calibration · coherent Ising machine learning couplings hardware Boltzmann machine
training gradient experiment · Xue "fully forward mode" training optical computing Nature 2024 recurrent
cavity follow-up · eLight 2025 "monolithically integrated" asynchronous optical recurrent accelerator
training · Pai "in situ backpropagation" Science 2023 photonic recurrent loop follow-up 2024 2025 ·
photonic quantum memristor Spagnolo Nature Photonics 2022 feedback loop trained reservoir hardware ·
Ashtiani "on-chip backpropagation" photonic neural network Nature 2026 architecture feedforward layers
arXiv · equilibrium propagation photonic optical network experimental demonstration training · arXiv
"photonic state-space model" OR "optical state space model" training hardware 2025 · Bueno Brunner 2018
Optica reinforcement learning photonic recurrent network DMD readout weights trained internal fixed ·
"noise-injected" analog Ising machine Boltzmann machine training couplings FPGA opto-electronic Bohm
Nature Communications 2022 · Hermans "embodiment of learning" electro-optical signal processors PRL 2016
physical backpropagation input mask trained · time-multiplexed optical loop neural network training
experiment recurrent fiber loop weights updated per time step · Antonik photonic reservoir "output
feedback" pattern generation experiment online training FPGA readout weights closed loop · "fully
forward mode" learning 2025 2026 recurrent extension self-learning photonic follow-up citing Xue ·
microring weight bank "in situ training" OR "online learning" silicon photonic experiment
demonstration · "Ising machine" photonic training couplings "Boltzmann" sampling learning 2024 2025
experiment measurement-feedback · photonic quantum processor variational training on-chip gradient
"parameter shift" experiment time-bin loop feedback · Tsinghua SJTU optical recurrent neural network
chip "in situ" OR "on-chip" training 2025 2026 demonstration LSTM · SPSA OR "simultaneous perturbation"
photonic hardware training experiment recurrent feedback chip · "hardware-in-the-loop" training photonic
OR optical recurrent feedback network experiment 2024 2025 2026 · "1610.06269" OR "Embodiment of
Learning in Electro-Optical" trained "input mask" readout weights delay loop parameters · "Emergent
Self-Adaptation" integrated photonic neural network backpropagation-free authors journal phase change
GST microring · photonic crossbar OR weight bank running recurrent neural network RNN weights updated
hardware in the loop fine-tuning phase-change · "trained in situ" OR "in-situ trained" recurrent OR
feedback photonic system arXiv 2026 · "In-Situ Optimization" optoelectronic reservoir computer "digital
delayed feedback" ACS Photonics 2025 parameters algorithm Bayesian gradient. *Fetched (full or
substantial):* arXiv 2506.14575; Nature s41586-026-10262-8 (via PubMed); PMC4382991; PMC9995662
(Buckley perspective); PMC11306102 (FFM); PMC11906216 (Lugnan); PMC12338871; PMC9532389 (Böhm); arXiv
2506.18041, 2508.20472, 2502.11126, 2307.11957, 1711.05133, 1802.02026, 2012.10615, 2311.16896 + 2026
preprints 2602.09162, 2602.19246, 2604.02429, 2605.19911, 2506.20833.
