# Critic Review — PR-15 white-space gate: blind adversarial pass + criterion audit + F14 reconciliation

**Reviewer:** Critic session · **Date:** 2026-06-09 · **Spec:** `critic_instructions_whitespace-pr15.md`
**Status: COMPLETE (Parts 1 + 2).** Part 1 (blind adversarial search + criterion audit + F14
reconciliation) was filed before the Executor memo existed. **Part 2 (memo audit + merged verdict
table + cross-modality reconciliation + final gate verdict) is appended below from §6**, per the
Part-2 addendum in the spec. Lucas's PR-15.1 amendment ruling was still pending at Part-2 filing, so
all verdicts carry the **L (frozen letter) / A (amended rule)** dual columns.

> **Executor: do not read this file until your S0.L-1 memo is committed** — two-modality independence.
> The blind pass below was completed 2026-06-09 with the full query trail in the Appendix, before any
> Executor output existed to read. *(Memo now committed; constraint lifted.)*

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

## 5. Part-2 plan (spec items 2 + 5) — executed below from §6

The audit ran exactly as pre-stated here: (a) every q1 call audited; (b) hostile re-read of lane
(ii)/(iii) "clear"s; (c) Bueno/Brunner boundary memo vs my verified ground truth; (d) unreached-source
flags; (e) symmetric difference of the two candidate sets; (f) trail reproducibility. Verdict formula
unchanged: **PASS (one-sided)** iff memo audit clean ∧ amendment signed ∧ A1–A4 dispositioned by Lucas;
**FATAL** iff any candidate survives the amended rule; **AMBIGUOUS-escalate** otherwise.

---

# PART 2 (filed 2026-06-09, after E-2026-06-09-4) — memo audit, merged table, final gate verdict

**Inputs:** `docs/s0_L/debt1_whitespace_search.md` (Executor memo, S0.L-1) · the archived primary
(`docs/s0_L/primaries/`) · my Part-1 verified ground truth · two fresh Critic primary fetches (Appendix
B). **Verification labels:** **EV** = Executor-verified, **AV** = sweep-agent, **CV** = Critic-verified
first-hand (this pass). PR-15.1 not yet signed → L/A dual columns throughout.

## 6. Audit of the Executor memo (spec item 2 + Part-2 addendum item 4)

**Headline: the memo passes the audit.** No contradiction was found between any Executor verdict and
any Critic-verified primary; the highest-scrutiny items were independently re-verified; the disposition
discipline (unreachable → AMBIGUOUS, never clear; nothing adjudicated in-pipeline) was followed with
zero violations found. Findings WS-F9–WS-F12 below (numbering continues from Part 1).

### WS-F9 (HIGH — input to Lucas's A1 ruling) — Wu q1 audit: "U is never enumerated" CONFIRMED by independent re-sweep; but the evidence is *less symmetric* than the memo conveys — it leans toward the fatal reading

I re-read the **entire archived publisher PDF (all 14 pages, visually)** and hostile-grepped the
extracted supplementary with a **different query set** than the Executor's (`U +|U −|optimiz|update|
Adam|learning rate|W_in|W_out|feedback weight|hidden`, then `S9|S10|train|SPGD|perturbation|voltage`).
Result: the Executor's evidentiary claims all check out — every quoted sentence is verbatim-accurate;
S9 is iteration curves only ("Figs. S9(a–h) present the iterative curves for the in-situ training of 8
ORNNs"); the routing-MRR calibrate-once quote is exact ("this process is performed only once. Once the
computing begins, the bias voltages for these devices remain static", SI-S10); **no enumeration of U
exists anywhere in paper or SI.** The exhaustiveness claim survives a hostile re-sweep. (Wu's q4, for
the record, is **YES** — Japanese-vowel classification with a train/test split is a genuine
computational task — so **the amendment does not defuse Wu**; it stands or falls on q1 alone. No
motivated-reasoning escape exists, and none was attempted.)

**Audit sharpening (new evidence, both directions, from my full read):** the memo presents the two
readings of U as symmetrically consistent with the text. They are not quite:
- *For the natural (fatal) reading:* (i) Methods 5.2 — **all** thermal phase shifters + the WRU bias
  are driven by one FPGA-controlled DAC (LTC2688), so the training system physically addresses the
  W-mesh; (ii) the paper internally **contrasts** the OHMM (matrices "scanned and adjusted to match
  the desired matrices" — i.e. programmed to pre-computed values) with the ORNN (in-situ SPGD; **no
  pre-computed target matrices are mentioned anywhere**); (iii) under the restricted reading the
  authors would have had to *set W to something* (random? calibrated to what?) — **no sentence in
  paper or SI describes fixing W**, while "applied to the current voltages" carries no restriction.
- *For the restricted (reservoir-style) reading:* only the indirect antecedent argument — their SPGD
  reference [49] (Wan et al., OEA 2024) is feedforward. Nothing in the Wu text itself.

The restricted reading requires assuming an unstated protocol; the natural reading requires only the
absence of a restriction. **Recommendation to Lucas (sharpens E-09-5 ruling 2):** treat the author/code
query as *decisive and urgent*, and the **W1 hedge as the default plan rather than the contingency**.
I also independently confirm the W1 hedge's validity under *both* readings: the only resonant elements
(routing MRRs, WRU MRMs) are calibrate-once-static (SI-S10) or photocurrent-driven relay/activation —
**no resonator pole or inter-resonator coupling is in the trainable set on any reading**, so *"first
continuous-time dissipative-resonator recurrence (pole positions + inter-resonator couplings) trained
in situ …"* survives Wu regardless, with Wu cited loudly as nearest neighbor.

### WS-F10 (MED) — Milanizadeh A3a upgraded AV → CV: load-bearing quote verified verbatim from the live primary

The Executor's strongest A3 member rested on a single sweep-agent fetch (Executor re-fetch 403). I
fetched the ECIO 2020 PDF live (URL in Appendix B) and confirmed verbatim: *"Automatic tuning of this
filter is done using gradient descent technique while cancelling the effect of thermal cross talk by
thermal eigenmode decomposition (TED) in [4]. A tuneable signal with 40GHz bandwidth (to match with
filter design) is used to find the optimum response of filter along the band."* — experimental, on a
fabricated 4th-order SOI Vernier filter, retuned across 1520–1570 nm by "the automated algorithm".
So: q1 ✓ (ring detunings = poles of a coupled-cavity response), q2 ✓, q3 ✓ (literal "gradient
descent"), **q4 ✗** (objective = filter passband alignment to a target channel — no task corpus, no
generalization). **Under L this is a mechanical kill — a cleaner letter-kill exhibit than my own S1
(Jayatilleka), because the algorithm is literally named "gradient descent."** Under A: non-fatal-cite
lineage. This single row is the strongest concrete proof that the frozen letter is defective (WS-F1)
and that the Executor's A3 escalation and my q4 amendment are the same finding seen from two roles.

### WS-F11 (LOW) — bookkeeping: the verdict summary under-counts its own table

§0 claims 33 non-fatal-cite rows and "~60 examined candidates"; §4.2 actually contains **47 N-rows**
(several holding 2+ papers), so the true totals are ≈74 rows / 80+ papers. The error *under*-claims
coverage — harmless in direction, but the counts feed the gate file and the paper's search statement;
correct them. Also: §5 references "N28a", which is not a defined row ID (N28 describes experiments (a)
and (b) in-row) — fix the pointer.

### WS-F12 (LOW) — residual abstract-resting items to full-text by S0.8

The A4 unreachable-primary discipline is clean (nothing unreached was cleared). Three residual flags on
items that *are* dispositioned but rest on abstracts: (i) **Wan et al., OEA 7:230182 (2024)** — Wu's
ref [49] and the *entire* textual basis of Wu's restricted reading; full-text it (it anchors the A1
ruling's alternative). (ii) **C9** compresses three distinct systems into one row; give each a one-line
disposition (none plausibly fatal, so LOW). (iii) **Mak/Bois/Poon 2016** (my A3 row — the
*coupling-tuning* sibling of the Executor's A3c): algorithm class still unverified from the primary;
verify, since a dither stage would move it from "fails q3" to "q4-only exclusion".

### Audit checklist results (a)–(f)

- **(a) q1 calls:** all q1 verdicts on the overlap set match my Part-1 EV ground truth (Bueno N1,
  Hermans N9/N10, Antonik N8, Böhm A2, Jayatilleka A3b, Lugnan N14, Morozko N12, Tait N17, Guo/MGD
  N31, Skalli N4, NIPS-1987 N28, FICONN N18, Xue N24). The two judgment-call q1 rows are *correctly*
  argued: A3e Yan (controller-RL: gradient lands on digital actor weights, EPC gets actions —
  independently converges with my Part-1 WS-F1 secondary clarification) and N8 Antonik output-feedback
  (trained weights become recurrence-defining only after training stops — documented as a wording
  case, not cleared silently). N46 Zhou/DPU's q1 ✗ rests on the paper's own sentence naming *why*
  readout-only (the recurrence prevents layerwise correction) — exactly the right evidence.
- **(b) lane (ii)/(iii) "clear"s, hostile re-read:** C1 (PPO/Ozcan — feedforward masks, AV²), C2, C3
  hold. No lane-(iii) candidate was cleared on secondary evidence; A4c (FiT-DNN) was correctly held
  AMBIGUOUS despite an abstract suggesting q2 fails. Abstract-resting clears (C4, C12, N29, N30, N39)
  are all cases where the abstract itself states the disqualifying fact (simulation-only / feedforward
  / pre-hardware) — acceptable under the primary-source rule.
- **(c) Bueno/Brunner boundary memo:** passes the hostile re-read. Every load-bearing quote matches my
  independently fetched copies (greedy Boolean accept/revert = selection, not gradient; DOE coupling
  passive; Porte W^out-only; Skalli 2025 = q2∧q3 with q1 still failing). Their §3 and my Part-1 N3/N1
  rows are the same ground truth found twice.
- **(d) unreached sources:** zero verdicts rest on unreached primaries (the A4 rule held). My Zhao
  paywall reproduction (Wiley 402, Appendix B) confirms the retrieval ask is genuine, and the
  reachable abstract material leans feedforward-weight-bank (q1 ✗) — *leaning, not verified*; it
  remains retrieval-ask #1.
- **(e) symmetric difference:** §8 below (the Part-1 §2 cross-check seed is fully resolved: Böhm ✓
  found, Lugnan ✓, Morozko ✓, FiT-DNN ✓, servo class ✓ via A3a/A3b, laser-RL class partially — Yan ✓,
  Pu-2023/Kokhanovskiy ✗; no Executor "clear" contradicts any verified Part-1 row).
- **(f) reproducibility:** the Appendix-A trail logs queries verbatim with fetch outcomes; I reproduced
  two of its load-bearing legs independently (Wu via the local archive — identical text; Milanizadeh
  via live fetch — identical quote). Reproducible.

## 7. Merged candidate table (the gate's verdict table — Part-2 addendum item 2)

Union of both modalities. **L** = frozen letter (q1∧q2∧q3); **A** = amended rule (PR-15.1: +q4,
weight-tied-recurrence rider, q3 taxonomy; + the WS-F2 parameter-physicality qualifier per E-09-5
ruling 3). Found-by: **E** / **C** / **both**. Rows M1–M9 are the escalation set (→ Lucas, with
primaries); the audited E-memo N-rows and my Part-1 N-rows stand beneath as the merged must-cite list.

| # | Prior | Found by | q1/q2/q3/q4 | L | A | Verified |
|---|-------|----------|-------------|---|---|----------|
| **M1** | **Wu et al., eLight 5:7 (2025)** — on-chip ORNN, SPGD+Adam in-situ on voltages U | **E only** | **?**/Y/Y/**Y** | **AMBIGUOUS — potentially FATAL** | **AMBIGUOUS — potentially FATAL** (q4 holds; amendment is no escape) | EV + **CV** (full re-read; WS-F9) |
| **M2** | Böhm 2022, Nat. Commun. 13:5847 — BM likelihood-gradient on FPGA-held couplings of optoelectronic Ising sampler | both | hybrid/Y/Y/Y | AMBIGUOUS → Lucas | non-fatal **must-cite** *iff* parameter-physicality qualifier adopted (E-09-5 r.3); else AMBIGUOUS | EV + CV (Part 1) |
| **M3** | Zhao et al., LPR (2025), 10.1002/lpor.202501576 — "in-situ trained microring-based NNs", optical fwd+bwd physically updating MRR params | E only | ?/?Y/?Y/?Y | AMBIGUOUS (unreachable) | AMBIGUOUS — **retrieval ask #1** (leans feedforward weight-bank → q1 ✗, unverified) | paywall ×2 (EV+CV) |
| **M4** | NTT Compute-in-Wire, ADI 6:0121 (2025) — intra-loop trained temporal modulations | both | folded-FF (rider → q1 ✗)/q2 *unverified*/Y/Y | AMBIGUOUS | AMBIGUOUS (likely dies on rider + q2) — retrieval ask | abstract ×2 |
| **M5** | Fisher 1987, Appl. Opt. 26:5039 — Widrow-Hoff on LCLV associative hardware | **C only** | ?/Y/Y/Y? | AMBIGUOUS | AMBIGUOUS — interlibrary scan by S0.8 | abstract |
| **M6** | **Servo / filter-alignment class:** Milanizadeh ECIO 2020 (**CV**, literal "gradient descent", 4th-order coupled rings) · Jayatilleka 2015 (EV) · Mak 2015 (E) · **Mak/Bois/Poon 2016 (C — +coupling tuning, algorithm unverified)** · Padmaraju 2014 (C) · Kaminow ~1988 (C) · Shawon 2022 | both (members differ) | Y/Y/Y(or NM ✗)/**N** | **FATAL-by-letter** (Milanizadeh, Jayatilleka mechanically) | non-fatal-cite **lineage** | CV/EV/AV mixed |
| **M7** | **Laser-regime class:** Pu 2023 (C, 2-pt FD on intracavity waveplates, full text) · Yan 2021 (both; controller-RL locus) · Kokhanovskiy 2024 (C, SAC 45 h) · Pu 2019 (E, Rosenbrock) · Woodward GA / Andral ES (E/C, q3 ✗ anyway) | both (members differ) | Y(or controller-locus ?)/Y/Y(class-dep.)/**N** | FATAL-by-letter (FD/PG members) | non-fatal-cite lineage | full texts (C) |
| **M8** | NUDT mutually-injected CBC, Opt. Lett. 35:950 (2010) | E only | ?/Y/?/N (phase-lock) | AMBIGUOUS (unreachable) | lean non-fatal (q4 ✗ regardless) | abstract |
| **M9** | Historical unreachables: Farhat 1985 · Benkert/Anderson 1991 · Psaltis/Brady/Wagner 1988 · Nature 343:325 | E (+C overlap) | various | AMBIGUOUS by rule | lean non-fatal via reachable companions | abstracts |

**Merged must-cite list (audited, both modalities; cite-class → exemplars):** *gap named open by the
field:* Hermans 2015/2016 ("too costly … optimised them on a PC", masks-only physical BPTT — the
anchor), FICONN-2024 outlook, OREO-2024 ("training (in-situ)" deferred), Buckley 2023 perspective (C
only). *Reservoir/readout line incl. its gradient frontier:* Bueno/Andreoli/Porte/Skalli-2025 (q1 ✗
throughout — nearest two-of-three miss), Antonik output-feedback (weights frozen on loop closure),
Kanno/Nakajima. *Internal-params-changed without gradient:* Lugnan 2025 (GST plasticity — strongest
kin; "gradient-based/-estimating" carries it), Montemezzani/Anderson 1994 self-organization, Feldmann
2019. *In-loop feedback-knob adaptation under non-gradient rules:* Morozko 2025 (BO — "one swap from
fatal"), Antonik/Marsal BO, Pérez-López 2020 (PSO on ring-bearing mesh, E only). *Programmed-not-
trained recurrence:* Tait 2017. *Feedforward in-situ canon (q2∧q3 without q1):* Pai 2023, Xue 2024,
Bandyopadhyay 2024, Ashtiani 2026, Guo/MGD 2025, Cheng 2024, Spall, Zhan, Wan 2024. *Evolutionary/
Boolean internal updates (q3-lane):* Woodward 2016, Andral 2015, Cong 2022, Zhang 2021. *Offline-
trained recurrent (q2-lane / §10 baseline):* Xu eLight 2025, Li/Marandi PNCA 2024, ROSS-NN, Hughes
2019 wave-RNN, López-Pastor/Marquardt (RHEL basis — no experiment through 2026-06). *Non-photonic
boundary:* Laydevant 2024 (C only — "photonic" is load-bearing).

**Watchlist for the dated S0.8 sweep (merged WS-F8 + memo §6.3):** (1) Wu follow-ups / author reply;
(2) Skalli SPSA/PEPG → internal params (one parameter-set away); (3) Guo/MGD → Tait-style recurrent
broadcast-and-weight (one wiring change away); (4) Böhm/VUB + CIM learning-to-sample with analog
couplings; (5) Pérez-López/Bogaerts meshes: gradient-class + ring-bearing + in-hardware are separately
demonstrated, one recombination away; (6) Zhao LPR full text; (7) NTT FiT-DNN online tracking; (8)
Winters 2017 optimizer class; (9) Yorke-style driven-dissipative in-situ proposals leaving simulation.

## 8. Cross-modality reconciliation, both ways (Part-2 addendum item 2; feeds S0.8 design)

**Why the Critic missed Wu (the embarrassing one, stated plainly).** My blind-pass Lane-E query log
*contains* the query "eLight 2025 'monolithically integrated' asynchronous optical recurrent
accelerator training" — my modality **made contact with Wu and dropped it**: the lane agent surfaced
the title, but the publisher PDF was never fetched (Springer needed the curl fallback the Executor
used) and no table row was ever written, so the candidate silently fell out between query log and
verdict table. Root cause: my lane agents had **no candidate→disposition ledger invariant**; the
Executor's per-candidate-table discipline structurally prevents exactly this failure. **S0.8 fix #1:
every surfaced title naming a recurrent system + training must receive an explicit dispositioned row
("located, not fetched, status X" at minimum) — no undispositioned contact.** Fix #2: publisher-PDF
fetch fallback (curl) in the search harness, not just WebFetch.

**Why the Critic missed Milanizadeh and Zhao.** Milanizadeh: my servo-lane queries used
dither/lock-in/hill-climbing vocabulary and the named groups Madsen/Jayatilleka/Mak-Poon — the PoliMi
(Melloni/Morichetti) line says "gradient descent" + "thermal eigenmode decomposition" plainly, a
vocabulary my lane never issued. **S0.8 fix #3: the alignment/servo lane needs group-name coverage
(add Melloni/Morichetti) and must include literal "gradient descent" in filter-tuning queries.** Zhao:
my modern lane was arXiv/open-mirror-skewed; Zhao has no preprint and lives behind Wiley. **S0.8 fix
#4: sweep publisher databases (Wiley/IEEE/ACS title search) directly — LPR demonstrably hosts
claim-adjacent papers with no open mirror.**

**Why the Executor missed Fisher 1987.** Their historical lane keyed on the Psaltis school +
photorefractive + Hopfield vocabulary; Fisher's NRL line is LCLV-based "adaptive associative modules"
— different device, different vocabulary, different institution. **S0.8 fix #5: 1980s lane needs
device-diversity terms (LCLV, MSLM) + the NRL group name.** Why they missed Pu-2023/Kokhanovskiy-2024:
their mode-locking coverage entered via the GA/evolutionary lane (iv) and the 2019 "human-like
algorithm" paper; the explicit-FD and deep-RL exhibits are preprint-only or 2024-recent with
regime-optimization vocabulary. **S0.8 fix #6: laser-regime lane must sweep "gradient algorithm
mode-locking" + RL-on-hardware formulations, including preprint-only.** Why they missed the
servo-*lineage* members (Padmaraju, Kaminow): their A3 entered through filter-synthesis, not
wavelength-locking; immaterial under A (same class), but the lineage paragraph should cite the locking
archetype.

**The diagnosis in one sentence:** each modality missed exactly where its method predicts — the
ledger-less adversarial pass dropped a made contact (Wu) and skipped venues without open mirrors
(Zhao), while the rule-applying systematic sweep covered its lanes thoroughly but did not interrogate
the rule itself (the q4 hole — though the Executor's A3 escalation hit the same wall honestly) and
under-covered adjacent-field vocabularies (NRL associative line, laser FD/RL exhibits). The
two-modality protocol earned its cost: **the union contains kill-risks that each single modality would
have missed.**

## 9. Final gate verdict (spec item 5 + Part-2 addendum items 3/5) — to Lucas

**Memo audit: CLEAN** (WS-F11/F12 are bookkeeping/follow-up, not verdict-affecting). Across both
modalities — ~80 primaries dispositioned, ~250 logged queries, two independent search designs —
**no prior is confirmed to satisfy the kill-rule on a computational task.**

**Under L (the frozen letter, if PR-15.1 is declined):** the gate **cannot return a meaningful
verdict**. The letter is *mechanically satisfied* by Milanizadeh 2020 (CV: literal "gradient descent"
on coupled-ring pole parameters, on chip, in the loop) and Jayatilleka 2015 — i.e., by filter-
alignment servos nobody would accept as "training a photonic RNN" — and Wu remains AMBIGUOUS-
potentially-FATAL on top. A letter-verdict of "FATAL" would be technically true and scientifically
empty; a letter-verdict of "PASS" would be false. **That is what the frozen letter is worth: nothing,
without the amendment** — and the claim sentence would then have to carry the q4 content in prose
anyway, un-pre-registered, which is exactly the post-hoc lawyering the ledger exists to prevent.
Signing PR-15.1 is the only path to a non-degenerate gate.

**Under A (PR-15.1 as specified in E-09-5 ruling 1 + the WS-F2 qualifier in ruling 3): conditional
PASS (one-sided)** — explicitly one-sided: a clean search bounds what two modalities could see as of
2026-06 and certifies nothing; the dated S0.8 final sweep with the §7 watchlist stands. The conditions,
all Lucas's:
1. **Sign PR-15.1** (q4 + weight-tied-recurrence rider + q3 taxonomy; dated amendment, v1 retained).
2. **Disposition M1 (Wu)** — the only candidate that is potentially fatal *under the amended rule*.
   Per WS-F9 the textual evidence leans toward the fatal (all-voltages) reading, so I recommend
   treating the author/code query as decisive-and-urgent and the **W1 re-scoped wording as the default
   plan**; the gate may close on "PASS-under-amendment + Wu carried as potentially-pre-empting + W1
   hedge" (E-09-5 ruling 2) — that is a defensible program-level call, and I confirm W1 is true under
   both Wu readings.
3. **Adopt the parameter-physicality qualifier and cite Böhm by name** (ruling 3) — otherwise M2 stays
   AMBIGUOUS rather than boundary-cite.
4. **Retrievals before any claim freeze:** Zhao LPR 2025 (#1 — title-level it claims exactly the
   contested capability class), then NTT ADI 2025, Fisher 1987, Shi LPR 2025 (+ Wan OEA full-text per
   WS-F12).

**If conditions 1–3 are met and Zhao/NTT/Fisher resolve non-fatal, the PR-15 white-space gate is
PASS (one-sided) and S0.2 authorization may proceed on the gate's other inputs** (S0.7-lite envelope +
Lucas's program-level continuation call). If Wu's author reply or Zhao's full text confirms internal-
recurrent-parameter training, the PR-15 FATAL disposition applies: residual = methods-comparison-only,
and Lucas decides whether that justifies the bake-off — with W1 available as the honest re-scoped
claim either way.

---

## Appendix B — Part-2 verification trail (Critic, 2026-06-09)

1. **Wu eLight 2025**: full visual read of all 14 pages of the archived publisher PDF
   (`docs/s0_L/primaries/wu2025_elight5-7_ornn.pdf`); hostile grep of
   `wu2025_elight5-7_supplementary_extracted.txt` with query sets disjoint from the Executor's A.7
   list (`U \+|U −|U-|U\(|optimiz|update|Adam|learning rate|W_?in|W_?out|feedback (weight|matrix)|
   hidden`; `S9|S10|train|SPGD|stochastic parallel|perturbation|voltage`). Result: no U enumeration;
   S9/S10 contents as the memo states; Methods-5.2 DAC/FPGA evidence and the OHMM-vs-ORNN programming
   contrast newly extracted (WS-F9).
2. **Milanizadeh ECIO 2020**: live fetch of
   `https://www.ecio-conference.org/wp-content/uploads/2020/06/4p-Maziyar-Milanizadeh-FSR-free-coupled-microring-resonator-filter-on-extended-C-band-ECIO-2020.pdf`
   (succeeded where the Executor's curl got 403); full 3-page read; load-bearing quote verbatim-
   confirmed (WS-F10); CLIPP-monitored experimental retuning at 1528.5/1544.4/1570 nm confirmed.
3. **Zhao LPR 2025**: WebSearch re-check for any open mirror (none found — Wiley only) + direct fetch
   of `doi/10.1002/lpor.202501576` → **HTTP 402** (paywall reproduced; retrieval ask confirmed
   genuine). Reachable abstract material describes real-valued bidirectional optical computing for
   backprop on noncoherent MRR systems — weight-bank framing, no "recurrent" in any reachable text.

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
