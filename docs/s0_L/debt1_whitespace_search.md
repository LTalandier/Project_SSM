# Debt #1 — White-space existence search (PR-15)

**Task:** S0.L-1 · **Author:** Executor · **Search dates:** 2026-06-09 · **Snapshot:** 2026-06
("as of mid-2026") · **Governing pre-registration:** **PR-15, 🔒 FROZEN 2026-06-09**
(`shared/preregistration.md`) — the kill-rule and lanes are applied **as written**, not re-derived.
**Modality:** this memo is modality (1) of the PR-15 two-modality protocol (Executor systematic
sweep). The Critic's independent adversarial pass (modality 2) is separate
(`shared/critic_instructions_whitespace-pr15.md`) and was not read before or during this sweep.

**Claim under test (PR-15, existence form):** *recurrent parameters — parameters that define the
recurrence of a physical photonic system (pole positions / feedback / inter-node couplings) —
updated on the physical device by gradient-based/-estimating training*: believed never demonstrated.

**Kill-rule (PR-15, frozen):** a prior is **FATAL iff q1 ∧ q2 ∧ q3** —
**q1** internal to the recurrence (readout-only / input-mask-only / encoder-only does **not** satisfy);
**q2** on the physical device, in the training loop (simulate-train-then-deploy does **not** satisfy);
**q3** gradient-based or gradient-estimating rule (backprop / in-situ adjoint / PAT-hybrid;
zeroth-order perturbative SPSA/FD/SPGD; REINFORCE/policy-gradient). Population-selection
(genetic / evolutionary / CMA-ES / Boolean / exhaustive) does **not** satisfy q3 → **non-fatal but
must be cited**. AMBIGUOUS (partially-internal params; hybrid digital recurrence; unclear update
locus; unreachable primary) → **escalate to Lucas, never adjudicated in-pipeline**.

---

## 0. Verdict summary

| Verdict | Count | Content |
|---|---|---|
| **FATAL (confirmed)** | **0** | No prior was confirmed to satisfy q1 ∧ q2 ∧ q3. |
| **AMBIGUOUS → escalated** | **15** (4 groups) | **A1 Wu et al. eLight 2025 — potentially FATAL** (update locus); A2 Böhm 2022 (hybrid digital recurrence); A3 calibration/self-optimization boundary class, 5 members (**A3a Milanizadeh 2020 potentially fatal under wording**); A4 unreachable primaries, 8 members. |
| **non-fatal-cite** | 33 | Near-misses the paper must cite; each PR-15 qualifier is individually load-bearing many times over (§4.2). |
| **clear (examined)** | 12 | Checked and out of scope / failing multiple q's with no cite obligation (§4.3). |

**Disposition:** the AMBIGUOUS set is escalated to Lucas with primaries
(`shared/escalate_to_human.md` E-2026-06-09-3; `shared/decisions_needed.md` D-2026-06-09-2), per
PR-15. **This memo does not and cannot issue the PR-15 PASS**: PASS is one-sided *and* now
conditional on Lucas's adjudication of A1 (and A3a). Everything else in the sweep is consistent
with the white-space claim *as of 2026-06*.

**The single load-bearing sentence of this memo:** in ~60 examined candidates across all five
frozen lanes, every system with genuine physical recurrence is trained at the readout/encoder only,
or by a non-gradient rule, or offline-then-deployed — **except** one 2025 monolithic optical RNN
trained in-situ by SPGD whose *trained-parameter set is not stated* (A1), and a class of in-loop
gradient-style *device-calibration* loops on pole-defining ring parameters whose status turns on
the word "training" (A3).

---

## 1. Method

1. **Lane sweeps.** Six parallel systematic sweeps, one per PR-15 lane (lane v split into the
   named-group minimum set and the free/forward search), executed 2026-06-09 by research subagents
   under the frozen rule. Lanes **locate**; all verdicts below were (re-)derived by the Executor by
   applying the frozen rule to the quoted primary evidence.
2. **Primary-source rule (the B2/F5 lesson).** Every non-clear verdict is grounded in primary-source
   text with the load-bearing sentence quoted. No verdict rests on a search snippet or a secondary
   summary. Where no primary text could be reached, the verdict is **AMBIGUOUS by rule**, never
   "clear".
3. **Executor first-hand re-verification.** For every escalated or single-sourced load-bearing
   item, the Executor re-fetched the primary directly (curl; WebFetch was session-limited) and
   re-extracted the quotes: **Wu et al. eLight 2025** (full publisher PDF **and** complete
   supplementary DOCX, S1–S11 swept), **Zhou et al. DPU 2021** (arXiv PDF), **Pérez-López et al.
   2020** (PMC full text), **Bueno et al. 2018** (arXiv PDF), **Böhm et al. 2022** (PMC full text),
   **Jayatilleka et al. 2015** (arXiv PDF), **Yorke 2026** (arXiv abstract). Marked **EV** below.
   Items verified by one sweep agent from fetched primary text are marked **AV** (two agents
   independently: **AV²**); items where only the primary's abstract was reachable are marked
   **abstract**.
4. **Scope.** Physical photonic / optical / optoelectronic systems. "Recurrent" = feedback/temporal
   memory in the computational use (delay loops, rings as dynamical memory, coupled lasers,
   output-feedback closed loops, recirculating meshes). Non-photonic physical learning (electronic,
   acoustic, mechanical) noted only where a photonic line depends on it.

---

## 2. The top kill-risk — A1: Wu et al., eLight 5:7 (2025) ⚠ potentially FATAL

**Citation:** B. Wu, H. Zhou, J. Cheng, W. Zhang, S. Zhang, C. Huang, D. Huang, H. Zhou, J. Dong,
X. Zhang, "Monolithically integrated asynchronous optical recurrent accelerator," *eLight* **5**:7
(2025), DOI 10.1186/s43593-025-00084-y (HUST + CUHK; received 2024-10-27, accepted 2025-03-04).
Open access. **EV** — Executor read the full publisher PDF and the complete supplementary
(S1–S11). Primary archived at `docs/s0_L/primaries/`.

**System.** The first monolithically integrated optical RNN ("ORNN") chip: three on-chip
incoherent MZI meshes realize W_in, W (feedback), W_out; hidden-state dimension 2; sequence
length 4 (cycle-4 output multiplexed back to cycle 1 for longer sequences); time steps
wavelength-encoded. The recurrence Eq. (6) is **physically closed on chip** through "wavelength
relay units": photodetector photocurrent *directly drives* the next microring modulator — analog
O/E/O, **no ADC/DAC or digital buffer in the recurrent path**. Task: Japanese-vowel classification
(binary 97 %/95 % train/test; 8-class 87.7 % via one-versus-rest).

**Verified quotes (EV, exact):**
- Recurrent map: "x⃗(t) = f_nl(W_in u⃗(t) + W x⃗(t − τ))" (Eq. 6) with "W is the feedback weight
  matrix for the hidden vector" (§2.3).
- Physical recurrence: "the hidden vector x(t) is fed into the on-chip incoherent MZI mesh (W) in
  reverse and the wavelengths from the previous cycle will be dropped to the photodetector
  representing the current cycle. […] The drop ports of the respective MRRs are connected to a
  photodetector, which sums the optical signal intensities and drives the next hidden signal step
  […]. This process completes the calculation of Eq. (6)." (§2.3)
- In-situ training: "entropy loss was selected as the loss function, which was minimized **in-situ**
  using a stochastic parallel gradient descent algorithm (see 'Methods' section)." (§2.3, Results)
- Rule (gradient-estimating, two-sided SPGD + Adam): "In the in-situ training of the ORNN, we
  employ the stochastic parallel gradient descent algorithm to estimate the gradient of the loss
  function [49]. In each iteration, a random perturbation vector δ is generated and applied to the
  current voltages as U + δ and U − δ." then "G = 2δ[L(U + δ) − L(U − δ)]" and Adam updates of U
  (Methods 5.1). Ref. [49] is Wan et al., *Opto-Electron. Adv.* 7, 230182 (2024) — SPGD on a
  feedforward 6×6 on-chip processor (the algorithmic antecedent).

**Rule application:**
- **q2 = YES** (verbatim: minimized in-situ; L(U±δ) measured on the chip per iteration).
- **q3 = YES** (SPGD = zeroth-order perturbative, explicitly "estimate the gradient"; + Adam).
- **q1 = UNRESOLVED.** W is a physical on-chip feedback mesh (thermally tuned MZIs) — its phase
  voltages are recurrence-defining. But **nowhere in the main text or the complete supplementary is
  the trained voltage vector U enumerated.** Executor sweep of every "training/trained/trainable"
  occurrence and the full supplementary (S1–S11) confirms: S9 ("Results of eight-class training")
  contains **only iteration curves**; the only locus-adjacent statements are (a) "we applied a
  **pre-trained** linear dimensionality reduction step followed by a ReLU function" (the digital
  12→2 input encoder — pre-trained, i.e. *not* in-situ), and (b) supplementary S10: the
  wavelength-routing "MRRs … this process is performed only once. Once the computing begins, the
  bias voltages for these devices remain static" (routing rings = calibrate-once, excluded). Neither
  statement says whether U spans the W-mesh heaters or only W_in/W_out.

**Verdict: AMBIGUOUS (unclear update locus) — potentially FATAL.** The *natural* reading of
"applied to the current voltages" with no stated restriction is that U includes all trainable mesh
voltages, W included — on that reading the prior satisfies q1 ∧ q2 ∧ q3 and **falsifies the
existence claim as frozen**. The restricted reading (W fixed at calibration; only W_in/W_out
trained — i.e. a reservoir-style protocol) is also consistent with the text and with the paper's
SPGD antecedent [49] being feedforward. **Resolution requires an author/code query or Lucas's
reading — not adjudicated here.** Note for wording (Supervisor/PR-2, *not* a rescue of the
existence claim): the recurrent path traverses analog O/E/O (PD→MRM) — optoelectronic, but *not*
"hybrid digital recurrence" (no ADC/DAC/memory in the loop); and the architecture is a
discrete-time mesh RNN, not a continuous-time dissipative resonator recurrence (pole positions).

---

## 3. The Bueno/Brunner boundary memo (lane ii required deliverable)

The Bueno/Brunner photonic-RNN "reinforcement learning" line is the claim's most likely confuser
because its titles say *reinforcement learning* and its systems are *genuinely recurrent photonic
hardware*. The primaries show it never satisfies q1 — and (2018–2021) not q3 either:

1. **What the 2018 system is.** "a network of up to 2025 diffractively coupled photonic nodes,
   forming a large-scale recurrent neural network" (published abstract, Optica 5(6):756; the arXiv
   v1 says 2500; N=900 demonstrated in the learning experiments). Internal coupling is fixed by
   construction: "Recurrent and complex network connections are implemented using a Diffractive
   Optical Element (DOE), an intrinsically parallel and passive device" (**EV**, arXiv:1711.05133).
2. **What is physically updated during learning: the Boolean DMD readout, nothing else.**
   "learning is limited to Boolean readout weights" (**EV**); "Inspired by the RC concept, we
   constrain learning induced weight adjustment to the readout layer" (AV²). → **q1 fails.**
3. **What the "reinforcement learning" rule actually is: a greedy single-weight flip search, not a
   reward-gradient estimator.** "If the error is reduced, we keep DMD configuration W_k^DMD, if
   not, we revert back to W_{k−1}^DMD" [and invert a different weight] (**EV**). → **q3 fails**
   (Boolean/greedy ∈ population-selection class). Andreoli et al. 2020 (same hardware,
   arXiv:2003.12319, AV) recasts this in RL vocabulary but remains Boolean accept/reject: "a reward
   r(k)=1 only if a modification … was beneficial", with "As in RC, we restrict learning to the
   optimization of the readout weights".
4. **The recurrence is hybrid electro-optic in time**: the camera-detected state is digitally
   rescaled and re-displayed ("After multiplication with scalar β, we add a constant phase offset
   θ_i and send the resulting matrix back to the SLM", AV) — spatial coupling optical (DOE),
   temporal loop through camera+electronics at ~Hz rates.
5. **Porte et al. 2021** (J. Phys. Photonics 3, 024017, AV) moves to a LA-VCSEL whose inter-node
   coupling *is* internal-physical ("optical diffusion of the LA-VCSEL's intra-cavity field as well
   as carrier diffusion induce interactions") — and keeps the boundary: "Evolutionary learning will
   be used to optimize only W^out"; "W^in and W^int do not partake in task-specific optimization,
   and we therefore implement a reservoir computer". → q1 fails; rule Boolean.
6. **The line's 2025 frontier finally adopts genuinely gradient-estimating rules** — Skalli et al.
   arXiv:2503.16943 (AV): SPSA, finite-difference, and PEPG ("policy gradient theorem"; "We find
   that PEPG is the most efficient algorithm") run hardware-in-the-loop on the LA-VCSEL ONN, **but
   the trained parameters are input weights + readout weights on SLMs/DMD only**; the baseline is
   described as "fixed random input and non-optimized recurrent internal weights", and the
   laser's internal/recurrent coupling is never an optimized parameter. → **q2+q3 now satisfied in
   this line; q1 still fails.**

**Boundary conclusion:** across 2018→2026 the Bueno/Brunner line never satisfies q1. The 2018
"reinforcement learning" is reward-triggered Boolean readout search (fails q3 too). The white-space
sentence must cite this line and hang its exclusion on **"recurrent/internal parameters"** (and,
for 2018–2021, additionally on **"gradient-based/-estimating"**). Watch item: Skalli et al. now
have hardware-in-the-loop SPSA/PEPG infrastructure one parameter-set away from q1.

---

## 4. Per-candidate verdict table

Format per PR-15: citation · system · what was *physically* updated · q1 · q2 · q3 class ·
verdict, with the load-bearing quote. Sources: **EV** = Executor-verified first-hand; **AV/AV²** =
sweep-agent primary fetch (×2 independent); *abstract* = only the primary's abstract reachable.

### 4.1 AMBIGUOUS — escalated to Lucas (15 items, 4 groups)

**A1. Wu et al., eLight 5:7 (2025)** — §2 above. **EV.** On-chip ORNN; SPGD+Adam on "the current
voltages U" in-situ; q1 unresolved (U unenumerated), q2 yes, q3 yes (SPSA-class).
**AMBIGUOUS — potentially FATAL.** → escalated.

**A2. Böhm, Alonso-Urquijo, Verschaffelt, Van der Sande, "Noise-injected analog Ising machines
enable ultrafast statistical sampling and machine learning," Nat. Commun. 13:5847 (2022).** **EV**
(PMC9532389). System: time-multiplexed optoelectronic Ising machine (fiber loop, MZM, PD) used as
the sampler inside RBM training; physical machine in the training loop each iteration.
Physically updated: RBM weights w_mn and biases — **held in the FPGA feedback path**: "The FPGA
demultiplexes the signal to obtain the spin amplitudes x_m, performs a matrix-vector
multiplication, and adds biases b_m to generate the feedback signal" (**EV**). Rule: "The biases
for the visible neurons b_m,vis, hidden neurons b_m,hid and the connection weights w_mn are
optimized in a gradient descent with the learning rate ϵ during each training iteration" (**EV**).
q1: **unclear** — the trained weights define the recurrent map of the hybrid loop but are digital
numbers, not photonic actuators; q2 yes; q3 yes (gradient). **AMBIGUOUS — textbook PR-15 "hybrid
digital recurrence"** → escalated (pre-listed ambiguity type; the claim wording must say whether
"parameters of a physical photonic system" excludes digitally-stored loop weights).

**A3. The calibration / self-optimization boundary class** — in-the-loop, perturbative/gradient
-style updates of *pole-defining ring parameters* or *intracavity laser parameters* on physical
devices, with a **device-quality objective** (filter alignment, mode-locking) rather than a
computational task loss. Whether such loops are "training" is a wording question the rule's word
"training" does not settle mechanically → escalated as a class; members:

- **A3a (potentially fatal under wording). Milanizadeh, Morichetti, Melloni et al., "FSR free
  coupled microring resonator filter on extended C-band," ECIO 2020** (method: Milanizadeh et al.,
  J. Lightwave Technol. 37, 2019 — thermal eigenmode decomposition). AV (conference PDF text
  extracted; Executor re-fetch 403). 4th-order series-coupled microring filter tuned closed-loop on
  chip: "Automatic tuning of this filter is done using **gradient descent** technique while
  cancelling the effect of thermal cross talk by thermal eigenmode decomposition (TED)". q1 yes
  (ring detunings = poles of a coupled-cavity response); q2 yes (physical chip, monitor feedback);
  q3 yes (gradient descent). **Mechanically q1∧q2∧q3 hold; the only exclusion is reading
  "training" as task-loss training rather than filter synthesis.** Not adjudicated here.
- **A3b. Jayatilleka, Shekhar, Chrostowski et al., "Wavelength tuning and stabilization of
  microring-based filters using silicon in-resonator photoconductive heaters," Opt. Express
  23:25084 (2015), arXiv:1507.00686.** **EV.** First/second-order ring filters auto-tuned and
  continuously stabilized via in-resonator photoconductive monitors: "I_PD is measured before and
  after changing P. If I_PD increases, then the sign of ∆P is unchanged and the algorithm proceeds
  to the next iteration. Otherwise, the sign of ∆P is reversed before proceeding" (**EV**) —
  perturb-and-observe sign rule (a perturbation-measured descent direction) on ring detunings,
  sequential per ring. Same boundary as A3a.
- **A3c. Mak, Poon et al., "Automatic resonance alignment of high-order microring filters," IEEE
  JQE 51:11 (2015), arXiv:1507.02129.** AV (ar5iv full). 5th-order coupled-ring filter; coordinate
  line-search + Nelder-Mead on ring phases (pole-defining, in-loop). Rule class = derivative-free
  direct search (not in the q3 list) → likely fails q3 on its own; carried in the class for the
  wording call.
- **A3d. Pu, Yi et al., "Intelligent programmable mode-locked fiber laser with a human-like
  algorithm," Optica 6:362 (2019), arXiv:1812.00796.** AV (full PDF). Intracavity EPC voltages
  (the only tunable intracavity element — recurrence-defining for the cavity map) updated in real
  time by Advanced Rosenbrock Search: "It is based on the traditional Rosenbrock algorithm, which
  is an unconstrained direct search method" + success/failure "pace punishment". Rule class
  straddles direct-search vs perturbation-estimated-descent → AMBIGUOUS on q3; objective =
  mode-locking (self-optimization).
- **A3e. Yan, Jiang et al., "Low-latency deep-reinforcement learning algorithm for ultrafast fiber
  lasers," Photonics Research 9:1493 (2021).** AV (full PDF). DDPG agent sets intracavity EPC
  voltages of a physical NPE fiber laser in closed loop: "The above actor network interacts with
  the laser environment directly and determines the voltage values given to the EPC in the next
  step". The *gradient-trained* parameters are the **digital** actor/critic weights; the EPC
  receives *actions*, not parameter-gradient updates → q1 arguably fails as written, but the case
  sits exactly on the "what counts as the updated parameter" boundary; objective =
  self-optimization. Carried in the class.

**A4. Unreachable primaries (AMBIGUOUS by rule — retrieval asks):**
- **A4a. Zhao et al., "In-situ trained microring-based neural networks for scalable and robust
  photonic computing," Laser Photonics Rev. (2025), DOI 10.1002/lpor.202501576.** Paywalled (Wiley
  402; no arXiv mirror found). Secondary descriptions: on-chip forward+backward optical propagation
  physically updating MRR weight-bank parameters (+13.3 % over conventional weight banks). Rings as
  *static weights* in a feedforward network would fail q1, but the updated parameters are literally
  ring detunings (partially-internal boundary) and the rule is gradient-class in-situ → **must be
  read before the claim freezes.** Highest-priority retrieval after A1.
- **A4b. Shi et al., "Intelligent configuration of integrated microwave photonic filter featuring
  self-stabilization and programmable response," Laser Photonics Rev. (2025), arXiv:2505.10001.**
  Abstract only (Wiley 402; arXiv PDF >10 MB fetch-failed). "Universal hybrid collaboration
  strategy" on a likely ring-bearing MPF; optimizer class unknown → A3-class suspect, unverified.
- **A4c. Nakajima et al., "Photonic compute-in-wire: remotely driven photonic deep neural network
  with single nonlinear loop," Adv. Devices Instrum. 6:0121 (2025).** SPJ 403; abstract (via
  records): folded-in-time DNN over a 20-km optoelectronic nonlinear delay loop, weights =
  feedback-modulation signals; "The parameters … were trained by using a **digital twin** of
  nonlinear optoelectronic dynamics" → indicates offline/simulate-train (q2 fails), and the loop
  time-multiplexes a *feedforward* DNN; full text unverified.
- **A4d. NUDT group (Zejin Liu), "Stable coherent beam combination by active phasing a mutual
  injection-locked fiber laser array," Opt. Lett. 35:950 (2010).** Abstract only. The one CBC
  variant where the lasers are *mutually coupled* (recurrent dynamics); phase-actuator locus
  relative to the coupling paths and exact rule (SPGD-class?) unresolvable from the abstract;
  objective = phase locking (self-optimization class).
- **A4e–A4h. Historical optical-NN primaries not reachable in full:** Farhat, Psaltis, Prata,
  Paek, "Optical implementation of the Hopfield model," Appl. Opt. 24:1469 (1985) (every reachable
  description: fixed photographic-mask weights, electronic feedback — no learning; companion
  Psaltis/Farhat OL 10:98 abstract reached); Benkert/Anderson, "Controlled competitive dynamics in
  a photorefractive ring oscillator," PRA 44:4633 (1991) (designed competitive couplings per
  secondary; APS 403); Psaltis, Brady, Wagner, "Adaptive optical networks using photorefractive
  crystals," Appl. Opt. 27:1752 (1988) (abstract reached; the *experimental* architecture's
  recurrence status unconfirmed — companion NIPS-1987 primary, reached in full, shows the
  era's in-loop-trained system was a feedforward perceptron, §4.2 N28); Psaltis, Brady, Gu, Lin,
  "Holography in artificial neural networks," Nature 343:325 (1990) (abstract; review character).
  All lean strongly non-fatal; listed for completeness per the unreachable-primary rule.

### 4.2 Non-fatal-cite (33) — the priors the claim's qualifiers must carry

*Readout-/encoder-only training of physically recurrent photonic systems (q1 fails — "reservoir
computing" per the rule):*

- **N1. Bueno et al., Optica 5:756 (2018)**, arXiv:1711.05133. **EV.** SLM/DOE photonic RNN
  (up to 2025 nodes); Boolean DMD **readout** flips, greedy accept/revert. q1 ✗, q2 ✓, q3 ✗.
  Quotes in §3. *The headline confuser — cite and pre-empt.*
- **N2. Andreoli et al., Nanophotonics 9:4139 (2020)**, arXiv:2003.12319. AV. Same hardware;
  Boolean readout under noise; "we restrict learning to the optimization of the readout weights".
  q1 ✗, q3 ✗.
- **N3. Porte et al., J. Phys. Photonics 3:024017 (2021)**, arXiv:2012.11153. AV. LA-VCSEL network
  (internal coupling physical); "W^in and W^int do not partake in task-specific optimization".
  q1 ✗, q3 ✗ (Boolean), q2 ✓.
- **N4. Skalli et al., arXiv:2503.16943 (2025).** AV. LA-VCSEL ONN trained hardware-in-the-loop by
  **SPSA / FD / PEPG (policy gradient)** — but "trainable input weights as well as … positive and
  negative [readout] weights"; internal laser coupling never optimized. q1 ✗, **q2 ✓, q3 ✓** —
  *the lane's nearest two-of-three miss; watch item.*
- **N5. Skalli et al., arXiv:2409.01042 (2024).** AV. Ternary readout, annealing-inspired
  multi-flip Boolean. q1 ✗, q3 ✗.
- **N6. Antonik, Duport, …, Massar, "Online training of an opto-electronic reservoir computer
  applied to real-time channel equalization," IEEE TNNLS 28:2686 (2017)**, arXiv:1610.06268. AV
  (full PDF). Online **gradient/LMS readout** on FPGA during physical operation: "w_i(n+1) = w_i(n)
  + λ(d(n) − y(n)) x_i(n)"; "These parameters remain fixed and only readout weights are optimised";
  feedback attenuation "scanned finely between 4.5 dB and 6 dB" (recurrence knob = manual scan).
  q1 ✗, q2 ✓, q3 ✓ (on the readout).
- **N7. Kanno, Uchida et al., Sci. Rep. 12:3720 (2022)**, PMC. AV. Photonic RL (Q-function) on a
  delay-RC: "only the output weights (readout weights) are trained using a simple learning rule."
  q1 ✗.
- **N8. Antonik, Haelterman, Massar, Phys. Rev. Applied 7:054014 (2017)**, arXiv:1802.02026 (+
  Neural Proc. Lett. 47:1041 (2018), arXiv:2012.10615). AV (both deep-read). **Output-feedback**
  delay reservoir — the trained readout *feeds back into the physical loop*: "Here we use the FPGA
  to feed the output of the reservoir back into itself". Decisive for the rule: training is
  teacher-forced with the loop open, then frozen — "During the training phase, the reservoir
  computer is driven by a time-multiplexed teacher signal … Then, the reservoir input is switched
  from the teacher sequence to the reservoir output signal … and the system is left running
  autonomously"; "The readout weights w_i are kept constant" (Fig. 1 caption); rule = offline ridge
  ("trained either offline (using standard linear regression methods, such as the ridge regression
  algorithm …)"). q1 ✗ (readout-trained), q2 ✗ (never updated while recurrence-defining), q3 ✗
  (ridge) → non-fatal on three independent grounds, **but the case type (trained weights that
  *become* recurrence-defining on loop closure, through a digital feedback path) is documented here
  for the wording work.**
- **N9. Hermans, Antonik, Haelterman, Massar, PRL 117:128301 (2016)**, arXiv:1610.06269. AV²
  (full PDF + supplement, two agents). **Physical backpropagation through a photonic recurrence**
  — forward *and* time-inverted backward passes run on the fiber-loop hardware; trained by true
  gradient descent. But: "The goal of applying error backpropagation to the above scheme is to
  optimise both the input and output masks m(r), m_b(r), u(r) and u_b" — masks only; the loop gain
  µ is preset ("we first choose a value of µ close to the threshold for instability") and, for the
  RC baseline, tuned **in simulation**: "optimising the parameters (input scaling, bias scaling and
  feedback gain) on the hardware would be too costly in terms of time. Therefore we optimised them
  on a PC using a simulation of the physical setup" (Suppl. §5.2). q1 ✗, **q2 ✓, q3 ✓** — *the
  closest gradient-class near-miss in the literature; cite and pre-empt explicitly.*
- **N10. Hermans, Burm, Van Vaerenbergh, Dambre, Bienstman, Nat. Commun. 6:6729 (2015)**,
  arXiv:1407.6637, PMC4382991. AV². Physical-BP framework; the hardware experiment is **acoustic**
  (the electro-optical version is simulated: "we simulate 20 electro-optical nodes"); "We have used
  the physical backpropagation set-up to train input and output masks." And the era-defining
  admission: "Note that in principle it could also be used to optimize properties of the acoustic
  set-up itself, but **we have omitted this for reasons of experimental simplicity**." q1 ✗ (and
  photonic q2 ✗). *Direct primary evidence the gap was recognized and left open in 2015.*
- **N11. Nakajima et al., "Physical deep learning with biologically inspired training method,"
  Nat. Commun. 13:7847 (2022)**, PMC. AV. Optoelectronic deep delay-RC; augmented-DFA recomputes
  inter-layer masks + readout; "Ω … is the fixed random internal connection"; feedback gain = set
  attenuator. q1 ✗.
- **N12. Morozko et al., ACS Photonics (2025)**, arXiv:2502.11126. AV² . In-situ optimization of an
  optoelectronic RC's recurrence-shaping knobs ("gain G, phase bias Φ0, input scaling ρ, delay
  time τ, and regularization λ") — but "For the optimization, a Bayesian algorithm was employed …
  along with random search" (q3 ✗), and the delay/feedback is digital ("an FPGA-based instrument
  that implements delay lines") → hybrid. *In-loop adaptation of genuine feedback parameters
  exists — under a non-gradient rule.*
- **N13. Antonik, Marsal, Brunner, Rontani, Cognitive Computation 13:1224 (2021)**,
  arXiv:2004.02535. AV. Bayesian optimization of feedback/input/interconnection gains of a
  large-scale SLM reservoir — recurrence matrix applied **in Matlab** (hybrid); "the simple grid
  search has been the standard hyper-parameter optimisation method in experimental reservoir
  computers so far" (load-bearing for the field's rule classes). q3 ✗, q1 hybrid.

*Recurrent photonic hardware with internal physical parameter changes — but no gradient rule
(q3 fails):*

- **N14. Lugnan et al., Advanced Science 12:2404920 (2025)**, arXiv:2312.03802, PMC. AV² (two
  agents, full text). "Photonic plastic recurrent resonator neural network": coupled silicon MRRs
  with GST phase-change patches **inside the recurrent network**, switched all-optically by the
  propagating signals (q1 ✓, q2 ✓): "the network's plastic behavior is fully emergent in the sense
  that it does not rely on an external controller updating the synaptic weights, or on a global
  reward signal" → **q3 ✗** (emergent local plasticity; task supervision = software logistic
  regression readout). *The strongest "internal-params-updated-on-device" prior; cite prominently —
  the "gradient-based/-estimating" qualifier carries it.*
- **N15. Feldmann et al., Nature 569:208 (2019).** abstract. PCM-on-waveguide spiking neurosynaptic
  network; on-device optical weight updates, but feedforward synapses + Hebbian/STDP-class rule.
  q1 ✗, q3 ✗.
- **N16. Montemezzani, Zhou, D.Z. Anderson, "Self-organized learning of purely temporal
  information in a photorefractive optical resonator," Opt. Lett. 19 (1994)** (+ Saffman/Benkert/
  Anderson, Opt. Lett. 16 (1991)). abstract (EuropePMC). Photorefractive ring resonator with
  intracavity delay; the adapting photorefractive gratings are intra-loop couplings (q1 ✓, q2 ✓):
  "A photorefractive resonator containing an optical delay line is shown to learn temporal
  information through a **self-organization** process." → q3 ✗ (no objective/error gradient).
  *The historical anchor for the same qualifier.*
- **N17. Tait, de Lima, …, Shastri, Prucnal, Sci. Rep. 7:7430 (2017)**, arXiv:1611.02272. AV²
  (Nature page + arXiv PDF). The first recurrent silicon-photonic CTRNN (MRR weight banks +
  fiber-MZM neurons in feedback). Weights **programmed, never trained**: "Each MRR weight bank is
  calibrated using … an offline measurement procedure"; "After calibration, the user can specify a
  desired weight matrix, and the control model calculates and applies the corresponding electrical
  currents"; "reservoir computers can only be made to elicit a desired behavior through
  instance-specific supervised training, whereas neuromorphic computers can be **programmed a
  priori** using a known set of weights." q2 ✗, q3 ✗ (q1-locus yes). *The canonical
  programmed-not-trained recurrent photonic system.*

*In-situ gradient(-estimating) training of FEEDFORWARD photonic hardware (q1 fails) — proves q2+q3
are individually demonstrated, never with q1:*

- **N18. Bandyopadhyay et al., Nature Photonics 18:1335 (2024)** (FICONN), arXiv:2208.01623. AV².
  3-layer integrated coherent DNN trained in-situ by measured directional derivatives ("At every
  iteration, the directional derivative of the cost function L(Θ) is computed in hardware along a
  randomly chosen direction ∆"). "Our implementation of the FICONN makes use of **feedforward**
  unitary circuits". And the outlook concedes the gap: "temporal or frequency data may be
  classified using recirculating waveguide meshes, which can implement feedback and resonant
  filters. Such a system, where phase shifter settings are trained in situ, may be used …" —
  recurrent in-situ training framed as **future work**.
- **N19. Pai et al., Science 380:398 (2023)**, arXiv:2205.08501. AV. Experimental **in-situ
  backprop** (interfered forward/adjoint fields) on a 3-layer triangular MZI mesh: "proceeding in a
  'feedforward' manner through the layers"; "our protocol can be implemented on any feedforward
  photonic circuit with the requisite Analyzer and Generator circuitry"; nonlinearities digital.
  q1 ✗.
- **N20. Hughes, Minkov, Shi, Fan, Optica 5:864 (2018)**, arXiv:1805.09943. AV. The in-situ adjoint
  *method* paper — "we demonstrate the training of a **numerically simulated** photonic artificial
  neural network" (feedforward mesh). q1 ✗, q2 ✗. *Direct input to verification debt #4.*
- **N21. Hughes, Williamson, Minkov, Fan, Sci. Adv. 5:eaay6946 (2019)**, arXiv:1904.12831. AV.
  "Wave physics as an analog recurrent neural network" — recurrent ✓, internal wave-speed
  distribution trained by BPTT ✓ — entirely **in simulation/inverse design** (q2 ✗). *The nearest
  conceptual miss to our program; cite.*
- **N22. Wright, Onodera, …, McMahon, Nature 601:549 (2022)** (PAT), arXiv:2104.13386. AV. All
  demos layered cascades ("This cascading is repeated …, resulting in a multilayer PNN with five
  trainable physical layers"; SI: "we specialize to the feedforward PNN architecture"). q1 ✗.
- **N23. Onodera*, Stein*, …, McMahon, arXiv:2402.17750 (2024).** AV. PAT of a 2D-programmable
  slab (10⁴ internal index DOF — internal medium!) — single-pass edge-to-edge propagation. q1 ✗.
- **N24. Xue et al., Nature 632:280 (2024)** (fully forward mode), PMC. AV. In-situ optical
  gradient training (Lorentz reciprocity) of free-space + integrated ONNs; all demos layered
  ("Y=(Π T_iM_i)X"); zero occurrences of "recurrent". q1 ✗.
- **N25. Cheng et al., Nat. Commun. 15:6189 (2024).** AV. On-chip diffractive ONN with in-situ SGD
  ("only one forward propagation is required to obtain the inference results"). q1 ✗.
- **N26. Ashtiani, Idjadi, Kim, Nature 651:927 (2026)**, arXiv:2506.14575. abstract+AV (arXiv PDF
  grep: no "recurrent"). "the demonstration of an integrated photonic deep neural network, trained
  end-to-end with **on-chip gradient-descent backpropagation**" — feedforward DNN. q1 ✗. *The
  2026 state of the art for on-chip gradient training; cite.*
- **N27. Spall, Guo, Lvovsky, Optica 9:803 (2022) + Adv. Photonics 7:016004 (2025)**,
  arXiv:2203.11207 / 2308.05226. AV. Optical(-hybrid and end-to-end) backprop on free-space MLPs
  ("fully-connected feed-forward architecture"). q1 ✗.
- **N28. Hsu, Brady, Psaltis, NIPS 1987 ("Experimental demonstrations of optical neural
  computers").** AV (proceedings PDF, full). Two experiments: (a) recurrent optical associative
  loop with **pre-recorded, fixed** holograms ("This hologram is moved to plane P4 as our stored
  memory" — learning phase precedes the recurrent recall phase); (b) photorefractive
  **perceptron** with in-loop optical weight updates by the perceptron rule ("Δw_i = αx_i where
  alpha is positive (negative) if the output for x is too low (high) … exposing the crystal with
  each incorrectly classified pattern") — feedforward. *Decisive period evidence: q1∧q2∧q3 never
  co-occurred — the recurrent system wasn't trained in-loop; the in-loop-trained system wasn't
  recurrent.*
- **N29. Yoshinaga, Kitayama, Hori, Opt. Lett. 14:716 (1989).** abstract. "An optical
  perceptronlike neural network employing a **delta learning rule** and consisting of input units
  and a single output unit" with photorefractive holographic interconnections — gradient-class
  in-loop optical learning existed by 1989, **feedforward**. q1 ✗.
- **N30. Wagner, Psaltis, "Multilayer optical learning networks," Appl. Opt. 26:5061 (1987).**
  abstract. Optical backprop **proposal** ("The proposed network … performs an approximate
  implementation of the backpropagation learning procedure"). q2 ✗. No experimental recurrent
  optical backprop found anywhere, 1985–2005.
- **N31. Guo, Aadhi, McCaughan, Tait, …, Shastri, arXiv:2506.18041 (2025)** (+ McCaughan et al.,
  APL Mach. Learn. 1:026118 (2023) — MGD framework, **simulation-only**: "we first simulated its
  performance … The goal of the simulator was … to emulate hardware implementing MGD"). AV². Fully
  analog online MGD training of an MRR weight bank — "all of which are **broadcast** to all neurons
  in the same layer" (feedforward; FPGA nonlinearity; multi-layer = simulated). q1 ✗. *Watch: MGD
  applied to a Tait-style recurrent broadcast-and-weight network would be fatal.*
- **N32. Wan et al., Opto-Electron. Adv. 7:230182 (2024).** abstract. Online SPGD configuring a
  6×6 on-chip processor (switching/descrambling; feedforward) — the eLight ORNN's algorithmic
  antecedent (its ref. [49], **EV** on the reference identity). q1 ✗.
- **N33. Xiang et al., arXiv:2506.14272 (2025).** AV². GHz spiking photonic chip (DFB-SA neurons,
  MRR synapses) trained in-situ — "Following the **feed-forward** architecture …"; rule = "modified
  ReSuMe … a variant of … (STDP)". q1 ✗, q3 ✗.

*Population-selection training of internal/cavity parameters in the loop (q3 fails — these make
the "gradient-based/-estimating" qualifier load-bearing; PR-15 lane iv):*

- **N34. Woodward, Kelleher, Sci. Rep. 6:37616 (2016)**, PMC. AV. **Genetic algorithm**, hardware
  in the loop, on four intracavity NALM waveplates + pump current of a figure-8 laser ("we
  experimentally demonstrate the first photonic application of a GA … to achieve optimised,
  reliable self-starting operation"; "a generation size of 30 individuals … roulette-wheel
  selection, crossover, mutation"). q1 ✓, q2 ✓, **q3 ✗**.
- **N35. Andral, …, Grelu, Optica 2:275 (2015)** (+ Girardot et al., IEEE JSTQE 26 (2020), HAL).
  AV (via Andral thesis + Girardot full text; Optica PDF bot-walled). **Evolution strategy** on
  intracavity EPC voltages: "we implement an evolutionary algorithm for the self-optimization of an
  ultrashort laser pulse regime, based on the optimal 4-parameter tuning of the intracavity
  nonlinear transfer function" (Girardot). q3 ✗.
- **N36. Brunton, Fu, Kutz, IEEE JQE 49:852 (2013) + JSTQE 20 (2014)** (extremum-seeking control of
  mode-locking). AV (author PDFs). ESC **is** gradient-estimating dither ("sinusoidally varying a
  set of input parameters and measuring the consequent variation of the objective") on cavity
  parameters — but "demonstrated by **numerical simulations**" only (q2 ✗). *The q3-satisfying ESC
  line never left simulation; its experimental successors all switched to population rules
  (N34/N35) or direct search (A3d).*
- **N37. Zhang et al., ACS Photonics 8:1662 (2021)** (GA on-chip ONN training; abstract) **+ Cong
  et al., Nat. Commun. 13 (2022)** (bacterial foraging on-chip: "experimentally demonstrate on-chip
  bacterial foraging training … Iris classification with ~96.7–98.3 per cent accuracy"; abstract).
  Population/swarm rules on feedforward photonic circuits. q1 ✗, q3 ✗ (rule class decidable from
  title/abstract).
- **N38. Pérez-López, López, DasMahapatra, Capmany, Nat. Commun. 11:6359 (2020).** **EV** (PMC
  full text). Hardware-in-the-loop **self-configuration of a recirculating hexagonal mesh** —
  experimentally synthesized circuits **include ring/loop-bearing states**: "1–7: a 10-TBU optical
  ring resonator (ORR), … a 6-TBU ORR working in parallel with a 2-TBU imbalanced MZI, a 6-TBU ORR,
  a second-order coupled resonator optical waveguide …, and a 12-TBU ORR" (**EV**). But the
  in-hardware optimizer is **PSO**: "programmed several interferometric circuits experimentally in
  the 30-TBU waveguide mesh using PSO algorithm" (**EV**) → q3 ✗; gradient descent with momentum
  appears in the **simulation** performance-estimator only, and "offered less and sometimes
  nonexistent convergence success" (**EV**). Framing = circuit synthesis (A3 wording class too).
  *Near-adjacency watch: gradient-class + loop-bearing + in-hardware is one recombination away in
  this platform.*
- **N39. OEO stabilization with GA-tuned PID, Opt. Lett. 50:4954 (2025).** abstract. "PID
  parameters were optimized using a genetic algorithm **before hardware development**" → q2 ✗,
  q3 ✗; stabilization objective.

*Offline-trained / theory-only recurrent photonic systems (q2 fails) — the §10/offline-deploy
contrast class:*

- **N40. Xu et al., eLight (2025), DOI 10.1186/s43593-025-00098-6.** AV. Microcomb photonic chip
  running FC/CNN/**RNN** models with optical state hand-off — "The network parameters were trained
  using the Adam optimizer" (PyTorch/TensorFlow) then "deployed onto the MRR and MZI arrays".
  q2 ✗. *Exactly the offline-train-then-deploy baseline the proposal's §10 envelope must beat.*
- **N41. Li, Leefmans, …, Marandi, Light Sci. Appl. 13:283 (2024)** (photonic neural cellular
  automata), PMC. AV. Recurrent/iterated optical map ("The output is recurrently fed back to update
  the cell state"); "The training procedure was performed digitally using an idealized simulation
  model … that had no noise". q2 ✗.
- **N42. Gao, …, Bogaerts, Photonics Research (2023)**, arXiv:2208.14453. AV. Autodiff
  gradient-descent **synthesis** of recirculating-mesh configurations ("many rings have formed in
  the obtained configuration") — entirely offline ("all our numerical experiments are performed on
  the same RedHat Linux server"). q2 ✗. *Offline gradient synthesis of ring-bearing meshes exists;
  pairs with N38 for the watch item.*
- **N43. López-Pastor, Marquardt, PRX 13:031020 (2023)** (Hamiltonian echo backprop), arXiv. AV +
  dedicated searches: demonstrated "numerically for the case of coupled nonlinear wave fields";
  **no experimental demonstration found through 2026-06**. q2 ✗. *The RHEL basis — cite; its
  experimental absence is itself part of the white space.*
- **N44. Shen et al., Nature Photonics 11:441 (2017)**, arXiv:1610.02365. AV. Programmed
  pre-trained weights ("We train the matrix parameters … with the standard back propagation
  algorithm … Once all parameters have been trained and programmed on the nanophotonic processor,
  forward propagation computing is performed optically"); on-chip forward-difference training =
  **proposal** ("Here we propose an alternative approach to directly obtain the gradient of each
  distinct parameter without back propagation, using forward propagation on ONN and the finite
  difference method"). q2 ✗ (and feedforward).
- **N45. Becker, Englund, Stiller, Nat. Commun. 15 (2024)** (OREO optoacoustic recurrent
  operator), PMC. AV. Physically recurrent (acoustic-wave memory links optical pulses); control
  pulses predetermined; the paper itself defers the gap: "one could improve the accuracy of OREO in
  the future by **training (in-situ)** the amplitudes of the control pulses." q2 ✗, q3 ✗. *2024
  primary-source confirmation that in-situ training of a recurrent photonic system is outstanding.*
- **N46. Zhou et al., Nature Photonics 15:367 (2021)** (DPU), arXiv:2008.11659. **EV.** Recurrent
  D-RNN configuration demonstrated — and the feared coincidence dissolves on the paper's own
  sentence: "To implement the model experimentally, we performed adaptive training by fine-tuning
  the modulation coefficients of **only the read-out layer** due to the recurrent connection
  inherence of the D-RNN" (**EV**); state carried by electronic buffering ("By controlling and
  buffering the massively parallel optoelectronic dataflow…"); the authors explicitly contrast
  adaptive training with in-situ training ("In contrast to in situ training solutions that seek to
  update the gradient directly in the system, our adaptive training approach sequentially corrects
  the in silico-trained model layer by layer"). q1 ✗ (recurrent mode), q2 partial, q3 ✓ (in-silico
  backprop).
- **N47. Hermans, Soriano, Dambre, Bienstman, Fischer, JMLR 16:2081 (2015).** Characterized via
  the authors' own PRL-2016 description (AV): "BP was applied to a numerical model of the system,
  and the results … applied to the physical experimental setup" — masks, simulation-trained,
  transferred. q1 ✗, q2 ✗.

### 4.3 Clear — examined, no cite obligation under the rule (12)

- **C1. Li, Chen, Gong, Ozcan, Light Sci. Appl. (2025)** (PPO in-situ on an SLM diffractive
  processor; PMC, AV²): true policy-gradient on physical optics — feedforward phase masks (q1 ✗).
  (Borderline-cite for "in-situ policy-gradient photonics exists".)
- **C2. Naruse-line photonic RL / bandit decision-making + photonic actor-critic accelerators**
  (arXiv:2512.00427, 2602.01087): photonics *runs* RL agents; no photonic recurrent parameter is
  trained. q1 ✗.
- **C3. Yan-class DRL mode-locking siblings (Sci. Rep. 2022 etc.)**: digital agents actuating
  cavities — folded into A3 class discussion; individually clear.
- **C4. SPGD coherent-beam-combining mainstream (e.g., 60-laser SPGD, Chin. Opt. Lett. 18:101403
  (2020), abstract)**: feedforward MOPA phase pre-compensation; no computational recurrence. q1 ✗.
  (The mutually-coupled exception is A4d.)
- **C5. Intracavity-SPGD adaptive-optics beam cleanup family**: laser brightness optimization, no
  computational use. Out of scope.
- **C6. Rübeling et al., Nanophotonics 14:2779 (2025)** (PMC, AV): frequency-domain PNN, "The
  circuit realizes a feedforward learning algorithm", PSO. q1 ✗, q3 ✗.
- **C7. Photonic-chip SPSA fine-tuning, arXiv:2604.02429 (2026)** (AV): **simulation-only** SPSA
  fine-tuning of a feedforward photonic CNN ("The simulation of hardware testing with thermal
  crosstalk and fine-tuning was performed on an Intel i3 CPU"). q1 ✗, q2 ✗.
- **C8. ROSS-NN (Light Sci. Appl. 2024, PMC)**: recurrent optical-spectrum-slicing nodes — "we
  have numerically investigated its processing capabilities" → simulation; readout-trained. q2 ✗.
- **C9. ON-ODE (arXiv:2209.12898)**, time-bin loop processors (arXiv:2404.17657), PSR variational
  photonics (PRR 7:023227, 2025 — 6-mode feedforward): programmed or feedforward or
  training-locus-numerical. q1/q2 ✗.
- **C10. Freiberger et al. (CMA-ES reservoir readouts, arXiv:1810.03377)**: readout + evolutionary.
  q1 ✗, q3 ✗.
- **C11. Laporte, Dambre, Bienstman, Sci. Rep. 11 (2021)** (self-learning photorefractive
  reservoir): "We demonstrate this by **simulating** a typical reservoir computing setup". q2 ✗.
- **C12. Yorke, arXiv:2605.19911 (2026)** ("Reconfigurable Nonlinear Photonic Networks for In-Situ
  Learning and Memory Formation via Driven-Dissipative Dynamics"). **EV** (abstract): "Through
  **numerical simulations**, I demonstrate …; local physical learning rules …" → q2 ✗, q3 ✗
  (local plasticity, not gradient). **Strategic note, not a verdict:** this 2026 single-author
  concept paper works the same driven-dissipative in-situ-learning space as our program —
  simulation-only today; flagged to Lucas as scoop-risk context.

---

## 5. Lane coverage statements (PR-15 gate: every lane swept + logged)

- **(i) Zeroth-order/perturbative internal updates:** swept (16 queries + fetches). In-situ
  SPGD/SPSA/MGD/FD on physical photonics is now routine — **but only on feedforward architectures**
  (N18, N31, N32, C7), with two exceptions escalated: A1 (locus unknown) and the A3
  calibration class (rule-on-pole-parameters, objective = alignment).
- **(ii) REINFORCE/policy-gradient internal updates:** swept (26 queries). True policy-gradient on
  photonic hardware exists (C1 PPO; N4 PEPG) — feedforward or encoder/readout only. Bueno/Brunner
  boundary memo in §3: that line is readout-only throughout, Boolean until 2024, gradient-class by
  2025 (N4) — never internal.
- **(iii) HIL delay-reservoir feedback/internal adaptation:** swept (40+ queries). In-loop
  adaptation of genuine feedback parameters exists **only under non-gradient rules** (N12 Bayesian,
  N13 Bayesian, N6 scan); the gradient-class hardware work trains masks/readouts (N6, N9, N10);
  output-feedback closes through digital paths with weights frozen (N8). One unreachable (A4c).
- **(iv) Evolutionary/Boolean internal-weight training:** swept (30+ queries incl. historical).
  Exists and is cited (N34, N35, N37, N38; Boolean readout N1–N3, N5). **The claim's
  "gradient-based/-estimating" qualifier is load-bearing** against exactly this lane — said
  explicitly, per the roadmap. Historical photorefractive era: in-loop *gradient-class* optical
  learning existed by 1987–89 but only feedforward (N28, N29); recurrent optical systems adapted
  only by self-organization (N16) or ran fixed weights (N28a, A4e).
- **(v) Free/forward + named groups:** all ten named groups swept with one-line dispositions in
  §4 (Brunner/Fischer/Bueno → §3; Shastri/Prucnal/Tait → N17/N31; Wright/Onodera/McMahon →
  N22/N23; Hughes/Fan/Pai → N19–N21; Englund/Bandyopadhyay/Hamerly → N18 (+N45 Stiller co-auth);
  Psaltis/Moser historical → N28–N30, modern EPFL (fixed-MMF modules, digital-twin-trained
  preceding layers; Oguz 2025) → clear; Lvovsky → N27; Momeni/Fleury → "Backpropagation-free
  training of deep physical neural networks," Science 382:1297 (2023), arXiv:2304.11042, AV:
  feedforward cascades of fixed physical transformers + trained interleaved modulator layers
  ("here all augmented linear multiplications are trained, in contrast to the traditional deep-RC
  where only the final layer is trained …") → q1 ✗; Marquardt/López-Pastor → N43;
  coupled-laser/OEO adaptive control → A4d, N39, C4). Plus programmable photonics
  (N38/N42/A3/A4b — Capmany/Bogaerts extension of the named set), adaptive recursive filters
  (negative result: **no adaptive IIR/recursive photonic filter with in-loop adaptation of
  feedback-path taps surfaced** after four query formulations; 1980s Stanford fiber-lattice
  adaptive demos were transversal/FIR), photonic Ising machines (A2; instance-programmed CIMs
  clear), quantum-photonic loop processors (programmed; C9), spiking photonics (N33, N15, C-class
  Hurtado SCISSOR-reservoir arXiv:2602.05918 — readout-only, abstract), and the fresh 2024–2026
  sweep (N26, N40, A1, A4a–c, C12). **No 2024–2026 work claims an in-situ-trained recurrent
  photonic system in the claim's sense** — the closest is A1, which does not state the claim
  either (it claims an asynchronous recurrent *accelerator* with in-situ-trained voltages).

---

## 6. What this search does and does not establish

1. **It does not certify the claim** (PR-15 PASS is one-sided): a clean sweep bounds only what
   six search modalities + ~60 primaries could see as of 2026-06. The dated S0.8 final sweep
   stands.
2. **It does not issue even the one-sided PASS yet**: A1 (and the A3a wording call) must be
   adjudicated by Lucas first. If A1 resolves fatal, PR-15 disposition applies (residual =
   methods-comparison-only; Lucas decides whether that justifies the bake-off).
3. It **does** establish, with primary quotes: (a) every PR-15 qualifier is individually
   load-bearing (q1 excludes the entire reservoir/readout line incl. its 2025 gradient-rule
   frontier; q3 excludes the evolutionary/Boolean/self-organizing internal-update lines; q2
   excludes the offline-deploy recurrent chips and all theory); (b) the field itself repeatedly
   names the gap as open/future work (N10 2015, N18 2024, N45 2024); (c) the near-adjacent
   capabilities (in-situ zeroth-order training; physical recurrent chips; gradient mesh synthesis)
   all exist separately and are visibly converging (A1, N4, N31, N38) — the white space, if it
   survives adjudication, is **closing on the order of one publication cycle**.
4. **Known limitations:** (a) non-escalated verdicts rest on sweep-agent primary fetches (EV
   re-verification covered all escalated/decisive items); (b) WebFetch session limits forced the
   Executor's re-verification onto curl — all EV fetches logged in Appendix A.7; (c) paywalled
   primaries are listed in A4, never counted as clear; (d) non-English-venue literature was reached
   only where indexed in English.

---

## Appendix A — Reproducible search trail

All searches 2026-06-09, via WebSearch/WebFetch (sweep agents) and curl (Executor). "~hits" as
returned at search time; "followed" = primaries fetched.

### A.1 Lane (i) — zeroth-order/perturbative (16 queries + fetches)
1. "SPSA in situ training photonic chip simultaneous perturbation stochastic approximation" | WebSearch | ~9 | arXiv 2604.02429, LSA PPO
2. "stochastic parallel gradient descent SPGD coupled fiber laser array phase locking coherent combining" | WebSearch | ~9 | OL 35-7-950, COL 18-101403
3. "McCaughan multiplexed gradient descent hardware in situ training APL Machine Learning" | WebSearch | ~9 | arXiv 2303.03986 (PDF)
4. arXiv abs+html 2604.02429 | WebFetch | — | simulation-only confirmed
5. "Bandyopadhyay single chip photonic deep neural network in situ training Nature Photonics 2024" | WebSearch | ~8 | s41566-024-01567-z, arXiv 2208.01623
6. "photonic recurrent neural network on-chip in situ training experimental demonstration 2025" | WebSearch | ~6 | eLight ORNN; Pai Science 2023; arXiv 2506.14575
7. '"monolithically integrated" "optical recurrent" accelerator eLight 2025 in situ training' | WebSearch | ~9 | link.springer 10.1186/s43593-025-00084-y (PDF + 3 prompts)
8. "arXiv asynchronous optical recurrent accelerator wavelength relay unit ORNN SPGD Huazhong" | WebSearch | ~7 | arXiv 1902.07318; PMC11021513 (OREO); PMC10955832 noted
9. "Shen 2017 coherent nanophotonic circuits deep learning on-chip training forward propagation finite difference proposal" | WebSearch | ~10 | arXiv 1610.02365 (PDF); arXiv 2012.11148 noted (sim-only)
10. "optoelectronic oscillator adaptive loop parameter optimization gradient descent intelligent control" | WebSearch | ~5 | OL 50-16-4954, ACS Photonics 5c01056
11. '"in-situ optimization" optoelectronic reservoir computer delayed feedback arXiv 2025 hyperparameters' | WebSearch | ~6 | arXiv 2502.11126
12. "SPGD phase locking mutually injection-locked laser array coupled cavity stochastic parallel gradient descent intracavity" | WebSearch | ~8 | OL 35-7-950 (abstract only, paywalled)
13. "automated tuning coupled microring resonator filter on-chip monitors gradient dither algorithm coupling coefficients" | WebSearch | ~7 | arXiv 1507.00686 (PDF), ECIO Milanizadeh PDF
14. "Prucnal microring weight bank self-interference cancellation online adaptation dither gradient descent recurrent silicon photonic neural network" | WebSearch | ~9 | arXiv 2506.18041, Tait s41598-017-07754-z, PMC11906216
15. "2025 2026 experimental in situ training recurrent photonic neural network feedback weights on chip" | WebSearch | ~7 | arXiv 2506.14272 (PDF)
16. "zeroth-order SPSA hardware-in-the-loop training integrated photonic processor 2024 2025 experimental demonstration" | WebSearch | ~7 | arXiv 2512.00427 noted; Xue Nature 2024 cross-ref
17. "intracavity adaptive optics SPGD stochastic parallel gradient descent laser resonator deformable mirror inside cavity optimization" | WebSearch | ~8 | family classed out of scope
18. Fetches: Wan OEA 230182 abstract; eLight supplementary (static-content 403 at agent; **EV curl succeeded**); FICONN; Tait; PMC pages; LSA PPO; OL 50-16-4954; COL 18-101403; arXiv 1711.05133; arXiv 2502.11126 | WebFetch | — | as listed

### A.2 Lane (ii) — REINFORCE/policy-gradient + Bueno/Brunner (26 queries/fetches)
1. arXiv abs 1711.05133; abs 2012.11153 | WebFetch ×2 | — | abstracts
2. 'Andreoli Brunner "Boolean learning" noise-perturbations hardware neural networks Nanophotonics arXiv' | WebSearch | ~8 | arXiv 2003.12319
3. ar5iv 1711.05133; ar5iv 2012.11153; ar5iv 2003.12319 | WebFetch ×3 | — | full texts
4. "Brunner photonic recurrent neural network trainable internal coupling experiment 2024 2025" | WebSearch | ~25 | arXiv 2503.16943; LSA-PPO; Lugnan
5. "Skalli VCSEL photonic neural network learning training experiment" | WebSearch | ~9 | 2503.16943; 2409.01042
6. "policy gradient photonic hardware training optical neural network experiment" | WebSearch | ~7 | LSA-PPO
7. "REINFORCE reward-modulated learning photonic hardware recurrent" | WebSearch | ~8 | none new
8. arXiv abs 2503.16943; nature s41377-025-02148-7 | WebFetch ×2 | — | → html/PMC
9. 'Skalli Brunner "fully tuneable" VCSEL' | WebSearch | ~8 | EPJ abstract
10. arXiv html 2503.16943v1 | WebFetch ×2 | — | full text
11. '"proximal policy optimization" optical processor arXiv Ozcan' | WebSearch | ~9 | arXiv 2507.05583/PMC12756285
12. '"in situ training" photonic recurrent neural network feedback loop hardware 2025 2026 experiment' | WebSearch | ~9 | Lugnan PMC
13. arXiv pdf 2507.05583 (binary fail); PMC12756285; PMC11906216 | WebFetch ×3 | — | full texts
14. "actor-critic photonic hardware neural network training experiment optical" | WebSearch | ~10 | 2602.01087/2512.00427 noted
15. '"internal weights" OR "internal coupling" trained in situ photonic recurrent network experiment SLM phase' | WebSearch | ~9 | readout-only confirmed
16. opg.optica.org optica-5-6-756 (bot-blocked); arXiv html 2409.01042v1; iopscience addee7; strathprints 69578 | WebFetch ×4 | — | annealing + 40k-SNN + published abstract
17. "photonic recurrent NN hardware training internal parameters 2024..2026 gradient in situ demonstration first" | WebSearch | ~9 | arXiv 2506.14575
18. '"on-chip backpropagation" integrated photonic NN Nature 2026 recurrent or feedforward arXiv' | WebSearch | ~8 | feedforward confirmed
19–26. "Brunner photonic neural network coupling training"; "REINFORCE optical neural network experiment hardware photonic training"; "reinforcement learning laser feedback parameters experiment tuning coupled lasers training"; ar5iv 1410.1247 (wrong ID); PMC10955832; Antonik output-feedback searches; Hermans searches; PMC4382991 + ar5iv 1802.02026 + arXiv 1610.06269 fetches | mixed | — | as listed in §3/§4

### A.3 Lane (iii) — HIL delay-reservoir (40+ queries/fetches)
1. 'Hermans Antonik "Embodiment of Learning…" arXiv' | WebSearch | ~7 | arXiv 1610.06269
2. 'Antonik "Brain-Inspired Photonic Signal Processor" arXiv output feedback' | WebSearch | ~10 | arXiv 1802.02026
3. nature ncomms7729 | WebFetch | — | redirect-blocked
4. arXiv abs 1610.06269 / 1802.02026 | WebFetch ×2 | — | abstracts
5. 'Hermans Burm "error backpropagation through physical media" arXiv' | WebSearch | ~9 | PMC4382991
6. PMC4382991 | WebFetch ×2 | — | full quotes
7. arXiv pdf 1610.06269 (13 pp incl. supplement, page-read) | WebFetch+Read | — | deep read
8. arXiv pdf 1802.02026 (16 pp, page-read) | WebFetch+Read | — | deep read
9. 'Antonik "Online training of an opto-electronic reservoir" channel equalization arXiv' | WebSearch | ~10 | arXiv 1610.06268 (deep read)
10. 'Antonik "Towards adjustable signal generation" ICANN output feedback' | WebSearch | ~8 | arXiv 2012.10615 (deep read)
11. 'Bueno Brunner "Reinforcement learning…" Optica arXiv DMD' | WebSearch | ~10 | arXiv 1711.05133 (deep read)
12. "Bayesian optimization photonic reservoir experiment hyperparameters feedback" | WebSearch | ~9 | 2004.02535 (deep read); 2502.11126 (html full)
13. "SPGD photonic reservoir / optoelectronic oscillator training" | WebSearch | ~6 | on-chip MZI SPGD 2024 (out of lane)
14. "online adaptation optoelectronic oscillator reservoir adaptive fiber loop" | WebSearch | ~8 | ACS Photonics 2025; arXiv 2012.10613 (numerical-only confirmed)
15. "delay-based reservoir trainable feedback internal weights hardware 2024..2026" | WebSearch | ~7 | 2502.11126
16. "folded-in-time Fit-DNN experiment optoelectronic backpropagation" | WebSearch | ~8 | Stelzer NatComm 2021 (numerical); Compute-in-Wire
17. '"Photonic Compute-in-Wire" arXiv' | WebSearch | ~8 | spj.science.org 403; +/doi/pdf, DOAJ, Unpaywall, S2 API ×5 → primary NOT reached
18. "Stelzer Yanchuk experimental realization" | WebSearch | ~8 | none experimental
19. "photonic RNN in situ training internal weights gradient 2025 2026" | WebSearch | ~8 | Lugnan; Ashtiani
20. 'SPSA "simultaneous perturbation" optical delay reservoir hardware' | WebSearch | ~10 | arXiv 2503.16943
21. 'Lugnan "emergent self-adaptation" arXiv' | WebSearch | ~6 | PMC11906216 (full)
22. 'Nakajima "physical deep learning" DFA Nat Comm 2022' | WebSearch | ~8 | PMC9792515 (full); PNAS optical-DFA noted (digital nets)
23. '"FORCE learning" photonic reservoir closed loop online' | WebSearch | ~6 | PMC8904492 (full); **no photonic FORCE found**
24. arXiv pdf 2503.16943 (pp 1–3) | WebFetch+Read | — | partial
25–40. researchsquare rs-8145052 (title-only); remaining fetches as listed in §4.2 rows N6–N13 | mixed | — | as listed

### A.4 Lane (iv) — evolutionary/Boolean + historical (30+ queries/fetches)
1. "genetic algorithm optical neural network hardware experiment in-the-loop training weights" | WebSearch | ~8 | ACS GA 2021
2. "self-tuning mode-locked fiber laser genetic algorithm Kutz Brunton Fu intracavity polarization" | WebSearch | ~9 | Brunton line
3. 'Andral Grelu "fiber laser" mode locked "evolutionary algorithm" Optica 2015' | WebSearch | ~10 | Andral, Pu 2019
4. 'Brunton Fu Kutz "extremum-seeking control" mode-locked laser arXiv' | WebSearch | ~11 | BrFuKu2013/2014 PDFs (UW, full)
5. 'Farhat Psaltis Prata Paek "optical implementation of the Hopfield model" 1985 PDF' | WebSearch | ~10 | CaltechAUTHORS 403 ×3, EPFL WAF, CiteSeerX broken, PubMed 18223740 no-abstract, academia.edu login → NOT reached
6. opg.optica.org fulltext/viewmedia (Andral ×3 incl. curl) | WebFetch/curl | — | JS bot-wall
7. '"Adaptive optical networks using photorefractive crystals" Psaltis Brady Wagner 1988' | WebSearch | ~10 | PubMed 20531647 (abstract)
8. api.semanticscholar.org ×6 | curl | — | 429 mostly
9. "deep reinforcement learning mode-locked fiber laser DDPG DQN" | WebSearch | ~6 | Yan 2021 PRJ → researching.cn PDF (cert-bypass curl, full)
10. PMC5116642 (Woodward) | WebFetch | — | full
11. 'Hsu Brady Psaltis "optical neural computers" NIPS 1987' | WebSearch | ~10 | proceedings.neurips.cc PDF (full); Yoshinaga PMID
12. 'Benkert Anderson "photorefractive ring oscillator" PRA 1991' | WebSearch | ~9 | APS 403; ADS JS-empty; EuropePMC empty; Unpaywall none; CORE none; JILA none → NOT reached
13. pubmed 19752945 / 20531647 / Wagner-Psaltis | WebFetch | — | abstracts
14. nature 343325a0 (+idp redirect) | WebFetch | — | cookie loop
15. 'Bueno Brunner reinforcement learning photonic recurrent arXiv' + ar5iv | WebSearch+Fetch | ~9 | quotes
16. site:jila.colorado.edu Anderson photorefractive | WebSearch | ~8 | thesis only
17. "Saffman Benkert Anderson self-organizing pdf" | WebSearch | ~8 | Laporte sim paper surfaced
18. research.polyu.edu.hk GA record | WebFetch | — | authors/DOI
19. '"optical implementation hopfield" pdf -researchgate'; '"adaptive optical networks" pdf 1752' | WebSearch | ~9/10 | PubMed, EPFL handles
20. curl researching.cn yan2021.pdf; arXiv pu2019 1812.00796 | curl | — | full texts
21. '"Low-latency deep-reinforcement learning" ultrafast fiber lasers' | WebSearch | ~9 | researching.cn
22. 'Pu "human-like algorithm" Optica 2019 arXiv' | WebSearch | ~9 | arXiv 1812.00796
23. unpaywall ×6 DOIs; EPFL Infoscience ×4 (WAF/429); HAL API (Girardot PDF + Andral thesis, full) | curl | — | as listed
24. EuropePMC REST ×11 (Nature90, Li/Qiao93, Cong22, Benkert empty, Saffman91, Montemezzani94, OL-1985, Laporte21) | curl | — | abstracts
25. "CMA-ES / particle swarm photonic hardware-in-the-loop" | WebSearch | ~7 | Freiberger 1810.03377
26. '"evolution in materio" / "evolvable hardware" optical' | WebSearch | ~9 | AIST extra-cavity GA (q1-irrelevant); Harding/Miller LC (electrical I/O, out of scope)
27. pubs.acs.org meta | curl | — | bot-wall

### A.5 Lane (v-a) — named groups (25+ queries/fetches)
1. Tait Sci Rep 2017 search + nature page + arXiv 1611.02272 PDF | WebSearch+Fetch | ~9 | full
2. Zhou DPU searches + arXiv 2008.11659 PDF (grep-verified) | WebSearch+curl | ~9/~8 | full
3. Bandyopadhyay 2024 + arXiv 2208.01623 PDF | WebSearch+Fetch | ~9 | full
4. Wright PAT + arXiv 2104.13386 PDF | WebSearch+Fetch | ~10 | full
5. Pai 2023 + arXiv 2205.08501 PDF; flagged s41586-026-10262-8 / arXiv 2506.14575 (PDF grep: no "recurrent") | WebSearch+Fetch | ~10 | full
6. Spall/Guo/Lvovsky + arXiv 2203.11207, 2308.05226 PDFs | WebSearch+Fetch | ~10 | full
7. "McMahon Cornell physics-aware training recurrent dynamical 2024 2025 in situ" | WebSearch | ~7 | 2506.18041, 2506.22122 noted
8. arXiv 2506.18041 PDF | curl | — | full
9. Xue FFM Nature 2024 → PMC11306102 | WebSearch+Fetch | ~9 | full
10. '"dual adaptive training" photonic neural networks NMI 2023 Zheng recurrent' | WebSearch | ~10 | feedforward classifiers only
11. '"Hamiltonian echo backpropagation" experimental demonstration 2024 2025' | WebSearch | ~9 | **no experiment found**; arXiv 2103.04992
12. "Psaltis Moser EPFL multimode fiber training backpropagation nonlinear 2023 2024 2025" | WebSearch | ~9 | arXiv 2501.07991 (fixed-MMF modules)
13. 'Filipovich Shastri "direct feedback alignment" silicon photonic Optica 2022' | WebSearch | ~9 | GitHub "Simulation code" (q2 ✗); arXiv 2412.08184 (PDF, full)
14. "microring weight bank RF self-interference cancellation online training" | WebSearch | ~9 | feedforward cancellers
15. "experimental in situ training recurrent photonic neural network on-chip feedback weights 2025 2026" | WebSearch | ~7 | arXiv 2506.14272 (PDF); PMC12338871; eLight lead
16. '"monolithically integrated" asynchronous optical recurrent neural network accelerator 2025' | WebSearch | ~8 | eLight 5:7 — **full PDF + supplementary DOCX read**
17. "recurrent silicon photonic neural network 'weight bank' in situ training 2024 2025 CTRNN" | WebSearch | ~8 | Lugnan; compute-in-wire
18. Lugnan arXiv 2312.03802 PDF (Wiley 402) | WebSearch+curl | ~9 | full
19. '"compute-in-wire" photonic DNN "single nonlinear loop" training' | WebSearch | ~7 | digital-twin sentence (abstract-level)
20. Spall AP 7(1) venue check | WebSearch | ~10 | confirmed
21. Cheng NatComm 15:6189 (3-hop redirect) | WebFetch | — | full
22. arXiv abs 1805.09943, 2408.05464, 2406.03372, 1904.12831, 2103.04992, 2501.07991 | curl/Fetch | — | abstracts verbatim
23. science.org aay6946 | WebFetch | — | 403 → arXiv used

### A.6 Lane (v-b) — free/forward + programmable photonics (49 queries/fetches)
1. "photonic state-space model hardware in situ training" | WebSearch | ~9 | PMC12338871
2. nature s41467-020-19608-w (3 hops + 2 prompts) | WebFetch | — | full
3. "in situ training recurrent photonic neural network experiment" | WebSearch | ~8 | PMC12338871, optica-5-6-756
4. PMC12338871 (Rübeling) | WebFetch | — | full
5. "automated configuration recirculating photonic waveguide mesh gradient descent Bogaerts" | WebSearch | ~7 | arXiv 2208.14453 (ar5iv full), 2406.05502
6. '"self-configuring" photonic mesh feedback loop ring resonator automated tuning gradient' | WebSearch | ~8 | 1812.09317 (fetch failed)
7. "adaptive recursive fiber optic filter LMS feedback tap experiment" | WebSearch | ~7 | 2111.04969 (FIR — dropped)
8. "photonic SSM chip state-space model microring 2025" | WebSearch | ~8 | arXiv 2602.05918 (abstract)
9. "adaptive IIR optical filter experiment feedback coefficient adaptation" | WebSearch | ~9 | none photonic-recursive
10. '"self-adaptive" OR "automatic tuning" microwave photonic notch filter microring feedback gradient' | WebSearch | ~7 | 1507.02129 (ar5iv full), Shi LPR
11. "intelligent configuration integrated microwave photonic filter self-stabilization 2025" | WebSearch | ~8 | 2505.10001 (abstract; Wiley 402 ×2, pdf >10 MB, html 404, researchsquare title-only, figshare 403)
12. "Moslehi Goodman Shaw fiber-optic lattice filter adaptive recursive 1984" | WebSearch | ~10 | structures only — **negative result logged**
13. "hardware in the loop training coupled microring photonic network experiment" | WebSearch | ~10 | PMC11906216, 2605.19911, 2506.18041
14. arXiv html 2605.19911 (Yorke) | WebFetch | — | sim-only
15. "adaptive fiber optic filter LMS tap weight experiment 1985 recursive recirculating delay line" | WebSearch | ~8 | FIR only
16. pubmed 41851461 (Ashtiani) | WebFetch | — | abstract
17. "trained coupled microring network experiment gradient in situ" | WebSearch | ~8 | Zhao LPR
18. '"in situ" learning coupled resonator optical waveguide CROW training' | WebSearch | ~9 | CROW physics only
19. 'photonic Ising machine coherent feedback FPGA "trained" OR "learning" in the loop couplings' | WebSearch | ~9 | PMC9532389 (full)
20. "arXiv in-situ trained microring neural network bidirectional optical backpropagation Zhao" | WebSearch | ~9 | **no open mirror**
21. "training photonic recurrent neural network hardware 2026 feedback coupling updated" | WebSearch | ~7 | nothing new
22. "VCSEL spiking photonic neuron online learning on-device synaptic weight hardware" | WebSearch | ~8 | arXiv 2506.14272 (PDF pp 1–6)
23. semanticscholar "In-Situ Trained Microring-Based Neural Networks" | WebSearch | ~9 | snippets only (not used for verdict)
24. "quantum photonic time-bin loop interferometer trained in situ parameter-shift loop phases" | WebSearch | ~7 | 2404.17657, PRR 7,023227
25. "deep equilibrium photonic / optical neural ODE / photonic feedback neural network trained" | WebSearch | ~8 | 2209.12898, PMC11461964 (full)
26. "photonic parameter-shift rule experiment in situ training quantum photonic circuit gradient" | WebSearch | ~9 | PRR feedforward
27. "equilibrium propagation photonic OR optical hardware experiment training resonator network" | WebSearch | ~9 | EP = D-Wave (non-photonic); **no photonic EP experiment**
28. Hermans/delay-reservoir cross-checks + Feldmann 2102.09360 + PNCA PMC11461964 + eLight s43593-025-00098-6 + '"first" hardware-trained recurrent photonic' + "on-chip training photonic recurrent 2025 2026" + '"recurrent" photonic "in situ" OR "on-chip" trained 2026' | mixed | — | as listed in §4
29. researchsquare rs-6669261 + figshare 29093141 (Shi) | WebFetch | — | unreachable

### A.7 Executor first-hand verification trail (curl, 2026-06-09, after WebFetch session limit)
1. link.springer.com/content/pdf/10.1186/s43593-025-00084-y.pdf → 14-page PDF → pdftotext; greps: "in-situ|in situ", "relay|pre-trained|in reverse|hidden vector", "trainab|training|trained", refs 37/49 | **A1 quotes verified**
2. link.springer.com/article/10.1186/s43593-025-00084-y (HTML) → supplementary URL → static-content.springer.com …MOESM1_ESM.docx (16.6 MB) → python-zip text extraction → greps: "S9|in-situ|SPGD|trained|training", "voltage|phase shifter|thermal|tunable", section headers S1–S11 | **supplementary fully swept: S9 = iteration curves only; routing MRRs calibrate-once-static; no U enumeration**
3. arxiv.org/pdf/2008.11659 → pdftotext → grep "read-out layer" + context read | **N46 quote verified**
4. EuropePMC REST search → PMC7733469 → fullTextXML → greps "particle swarm|programmed several|gradient descent", "ORR" | **N38 quotes verified**
5. arxiv.org/pdf/1711.05133 → pdftotext → greps "readout layer|invert|revert|DOE", "learning induced|error is reduced|Boolean" | **N1/§3 quotes verified**
6. EuropePMC PMC9532389 fullTextXML → greps "gradient descent|demultiplexes|matrix-vector" | **A2 quotes verified**
7. ecio-conference.org Milanizadeh PDF | **403 at Executor** (reached by sweep agent earlier — quote stands as AV)
8. arxiv.org/pdf/1507.00686 → pdftotext → grep "sign of" + context | **A3b quote verified**
9. export.arxiv.org API '"thermal eigenmode decomposition"' | no open mirror of the JLT method paper
10. arxiv.org/abs/2605.19911 → title + abstract extracted | **C12 verified (simulation-only)**

*Primary archive:* `docs/s0_L/primaries/` — Wu et al. eLight 2025 publisher PDF (CC-BY) + extracted
supplementary text.
