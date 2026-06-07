# A Self-Learning Photonic State-Space Model on Thin-Film Lithium Niobate
### From Oscillator Pole-Placement to In-Situ Hamiltonian-Echo Training

*Research proposal — draft v0.2 (supersedes v0.1; for circulation and iteration)*

> **Changes since v0.1.** The target architecture moves from a generic diagonal S4D to an **oscillatory / Hamiltonian unit (LinOSS-style)**, which maps more naturally onto coupled rings *and* is state-of-the-art on long-range tasks. A new training program is added around **Recurrent Hamiltonian Echo Learning (RHEL)** and the Hamiltonian-echo family, framed as two *decoupled* research questions — (Q1) in-situ training of a photonic recurrence, achievable via a physical-forward / digital-echo hybrid, and (Q2) the all-optical echo. The staged plan, risks, and headline are revised accordingly. The S4D→ring pole-placement mapping and the candid feasibility-vs-advantage framing are retained.

---

## Abstract

State-space models (SSMs) are the leading linear-recurrence alternative to attention for long sequences, and their unselective core is a linear time-invariant (LTI) system — a rational transfer function — which integrated photonics builds natively. This proposal develops a **photonic SSM on thin-film lithium niobate (TFLN)** in which ring resonators are complex poles, delay lines supply memory, electro-optic (EO) elements set the projections, and erbium gain biases the poles toward the imaginary axis. We target an **oscillatory (LinOSS-style) unit** rather than a generic diagonal SSM: it maps directly onto coupled ring-resonators and is the current state of the art on long-range benchmarks. Beyond the device, we propose to attack the open problem of *training a physical recurrence in situ* using **Hamiltonian-echo learning (RHEL)**, which computes exact, variance-free gradients from time-reversed physical trajectories — no backward pass, no Jacobian — for near-conservative systems. We separate the program into two decoupled bets: **(Q1)** demonstrate in-situ training of a photonic recurrence via a *physical-forward / digital-echo* hybrid — which would be the **first in-situ-trained recurrent photonic system** — and **(Q2)** realize the echo *all-optically* via on-chip phase conjugation, the physics-native endpoint. To our knowledge no photonic SSM and no in-situ-trained recurrent photonic system exists as of mid-2026; both targets are open white space. The plan is staged with explicit decision gates and graceful fallbacks (physics-aware training; digital optical phase conjugation). We are candid that RHEL and Hamiltonian-echo learning are, today, **theory and simulation only** — no Hamiltonian-echo hardware exists — and that this is a frontier program, not a near-term GPU competitor.

---

## 1. Background and motivation

### 1.1 SSMs as transfer functions
A structured SSM layer is the continuous-time linear system

$$\dot{x}(t) = A\,x(t) + B\,u(t), \qquad y(t) = C\,x(t) + D\,u(t),$$

discretized to $x_k = \bar A\,x_{k-1} + \bar B\,u_k,\; y_k = C\,x_k + D\,u_k$. Its three equivalent views — recurrent (a feedback loop), convolutional ($y=u*K$, $K=(C\bar B, C\bar A\bar B,\dots)$, an IIR/FIR kernel), and parallel-scan (GPU training) — all describe one rational transfer function

$$H(s) = C\,(sI-A)^{-1}B + D = \sum_{i}\frac{c_i b_i}{s-a_i} + D,$$

a sum of one-pole (Lorentzian) terms. **Photonics realizes $H(s)$ directly:** each pole is a damped optical resonance, residues are coupling weights, delays supply the kernel's temporal support.

### 1.2 Why an oscillatory / Hamiltonian unit (the v0.2 architecture choice)
Rather than a generic diagonal S4D, we target the **LinOSS oscillator** — a forced harmonic-oscillator SSM. Three reasons:
- **It is the natural ring abstraction.** A forced harmonic oscillator *is* a resonance; a coupled-oscillator bank is a coupled-ring bank. The mapping in §3 is tighter for oscillators than for an abstract diagonal.
- **It is competitive-to-superior on long-range tasks.** LinOSS reportedly leads on the longest sequence benchmarks (e.g. EigenWorms at ~18k length, and ~2× a Mamba baseline on a ~50k-length regression) — so committing to oscillatory units is a performance *upgrade*, not a sacrifice. *(Verify benchmark specifics against the LinOSS papers before load-bearing use.)*
- **It is exactly the unit our training method assumes.** RHEL (§5) trains "Hamiltonian Recurrent Units," whose linear block is the LinOSS oscillator. Choosing this unit aligns device and training algorithm.

The one tension to manage from the outset: **pure conservatism vs. damping.** Time-reversible (conservative) oscillators maximize the exactness of echo-based training, but recent work (D-LinOSS) shows that a *little learnable damping* improves long-range performance. We therefore treat the pole's distance from the imaginary axis as a **tunable knob** and let simulation (§6, Stage 0) locate the sweet spot between gradient fidelity (favor conservative) and task accuracy (favor slight damping).

### 1.3 Why TFLN
TFLN provides, on one platform: low-loss waveguides and high-$Q$ microrings (the oscillators/poles), true-time-delay (kernel memory), fast phase-transparent EO tuning (the projections and, eventually, selectivity), and — uniquely useful here — a strong **χ² nonlinearity**, which is both the route to an on-chip nonlinear unit *and* the natural primitive for **optical phase conjugation**, i.e. the time-reversal "echo" that physics-native training needs (§5). Erbium doping supplies the gain that biases poles toward the imaginary axis. The same χ² thus underwrites both the model's nonlinearity and its training mechanism — a rare platform coherence.

---

## 2. Prior art and the white space (two gaps)

**Gap 1 — no photonic SSM (the device).**

| Prior art | What it is | Why it is not a photonic SSM |
|---|---|---|
| Microwave-photonic IIR/FIR filters (Capmany, Marpaung; Bogaerts/Pérez-López meshes) | Hand-designed optical transfer functions | Untrained, hand-set; no learned $(A,B,C,\Delta)$ |
| Photonic reservoir computing (incl. TFLN/LNOI) | Fixed random recurrence + trained readout | Recurrence is untrained |
| ROSS-NN (Bogris, *Commun. Eng.* 2022) | Recurrent spectrum-slicing neuromorphic net | Filter-bank, not a structured SSM kernel |
| IMSSA (Siegel et al., arXiv:2412.20215) | First S4D kernel on analog in-memory (memristive) hardware | **Electronic**, not photonic |

**Gap 2 — no in-situ-trained recurrent photonic system (the training).** In-situ backpropagation is established for *feedforward* photonics (Hughes, Minkov, Shi & Fan, *Optica* 2018, adjoint/TRIM; Pai et al., *Science* 2023, experimental in a nanophotonic MZI mesh). Physics-aware training (Wright, Onodera, McMahon et al., *Nature* 2022) trains real hardware but with a *digital* backward pass. Photonic *recurrent* systems (reservoirs, recurrent Ising machines) are trained only at the readout or by external/digital optimization — **never the recurrence itself, in situ.** RHEL/HEB is the first algorithm designed to close exactly this gap for a dynamical recurrence.

**Claim.** A *trained, structured photonic SSM* (Gap 1) that is, moreover, *trained in situ via Hamiltonian echo* (Gap 2) sits in unoccupied white space on both axes (to our knowledge, mid-2026).

---

## 3. Core mapping: oscillator → ring-bank

### 3.1 One ring = one complex pole = one oscillator
Near resonance, an add-drop microring has a single Laplace-domain pole at

$$s_{\text{pole}} = -\kappa_{\text{tot}} + i\,\omega_{\text{res}},$$

with $\omega_{\text{res}}$ the resonance detuning and $\kappa_{\text{tot}}=\kappa_{\text{loss}}+\kappa_{\text{couple}}$ the total amplitude decay rate. Identifying with an SSM eigenvalue $a_i = -\exp(\alpha_i)+i\beta_i$ (equivalently, a damped oscillator of frequency $\beta_i$ and damping $\propto\exp(\alpha_i)$):

| SSM / oscillator quantity | Physical realization | Tuning handle |
|---|---|---|
| oscillation frequency $\beta_i=\mathrm{Im}(a_i)$ | ring resonance detuning $\omega_{\text{res}}$ | EO / thermal phase shift |
| damping $-\exp(\alpha_i)=\mathrm{Re}(a_i)$ | total decay rate $\kappa_{\text{tot}}$ | bus–ring coupling (+ net gain) |
| undamped / long-memory ($|\lambda|\to1$) | round-trip loss $\to 0$ (net gain $\approx$ unity) | erbium gain in the loop |
| residue $c_i b_i$ | input/output coupling product | MZI-mesh weights |
| $B,C$ vectors | input fan-in / output fan-out | programmable MZI mesh |
| $\Delta$ (step) | loop round-trip time $\tau$ | path length / delay line |
| $D$ (skip) | through path | bypass + weight |

An $N$-ring add-drop bank fed and read by a programmable MZI mesh realizes an $N$-oscillator (LinOSS-style) layer with learnable parameters. **Damping is set deliberately** via coupling and net gain — near, but not necessarily on, the imaginary axis (§1.2 knob).

### 3.2 Continuous-time is a feature
An analog optical loop integrates the ODE in physical time, so $\Delta\to\tau$ (round-trip) and the discretization step is partly bypassed. LinOSS's IMEX discretization is chosen precisely because it preserves time-reversibility — which, as §5 shows, is the property echo-based training exploits.

---

## 4. Pole-placement and expressivity

### 4.1 Realizable eigenvalue region
- **Stability is free.** Passive rings give $\mathrm{Re}(s_{\text{pole}})<0\Rightarrow|\lambda|<1$; the hardware cannot represent an unstable system.
- **Minimum damping (max $Q$)** is set by intrinsic loss; net gain extends toward $|\lambda|\to1$ (undamped). *Note:* full conservatism is exact only at zero net dissipation, and any residual loss/gain imbalance **accumulates linearly with loop length** — there is no free lunch in pushing to the axis (this couples directly to §5's training tolerance).
- **FSR bounds** the representable detunings $\beta_i$; **fabrication tolerance** means poles are *placed* by post-fab EO/thermal trimming, not trusted from layout (a calibration problem squarely in the author's wheelhouse).

### 4.2 Expressivity and the conservatism–damping tension
- **Oscillatory diagonal (LinOSS): reachable directly** — $N$ rings → $N$ oscillators.
- **The performance-vs-exactness conflict** is now explicit and central: pure-conservative oscillators maximize echo-training exactness (§5) but cost expressivity ("forgetting"); learnable damping (D-LinOSS) recovers performance but moves the system away from the non-dissipative regime RHEL requires. **Resolution:** treat damping as a swept hyperparameter and characterize the gradient-fidelity-vs-accuracy frontier in Stage 0; this frontier is itself a publishable result.
- **Selectivity (LTV) gap** (toward Mamba): input-dependent dynamics require rewriting poles/couplings per sample. EO modulation of $B,C$ at data rate is feasible; input-dependent $A/\Delta$ needs fast intracavity EO + a per-channel high-speed DAC — the conversion bottleneck. We target time-invariant oscillatory dynamics first.

---

## 5. Training: physics-native in-situ learning (new in v0.2)

The hardest unsolved problem is not the device but **how to train a physical recurrence**. Backprop-through-time on a noisy optical loop is intractable. We adopt the **Hamiltonian-echo** family.

### 5.1 RHEL in brief
Recurrent Hamiltonian Echo Learning (Pourcel & Ernoult, arXiv:2506.05259) computes loss gradients as **finite differences of time-reversed physical trajectories** of a non-dissipative Hamiltonian system: a forward pass; a momentum-flipped, reverse-time **nudged echo** (nudge strength $\pm\varepsilon$ breaks the time-reversal symmetry that would otherwise retrace the path); and a symmetric finite difference that **equals the BPTT gradient as $\varepsilon\to0$** — with *no backward pass, no Jacobian, and no gradient variance*. It is proven equivalent to the continuous adjoint-state method and, on Hamiltonian Recurrent Units (the LinOSS oscillator), to BPTT; it chains across stacked units. It is the recurrent, large-scale, trajectory-loss generalization of **Hamiltonian Echo Backpropagation** (López-Pastor & Marquardt, *PRX* 2023), which turns any time-reversible Hamiltonian system into a self-learning machine. (A companion result, GLEP, arXiv:2506.06248, unifies Equilibrium Propagation and HEB/RHEL as boundary-condition special cases of one Lagrangian framework.) **Crucially, both RHEL and HEB are validated in simulation only; no Hamiltonian-echo hardware exists.**

### 5.2 What the literature settles — and what it doesn't
- **The crux is echo fidelity, not perfect conservatism.** Gain must compensate loss so the *net* evaluation-window dynamics stay near-reversible, but the binding constraint is the fidelity of the time-reversal step. Critically: **random, zero-mean noise — including ASE — averages out at small learning rate**, whereas **systematic echo/conjugation error does not** and requires an independent in-loop calibration routine. *Biggest unverified assumption for our system:* ASE in a gain-loaded recurrent loop may carry correlated/systematic components that do **not** average out, and FWM-based conjugation adds spontaneous (idler) noise exactly at this sensitive step.
- **Non-dissipation is the stated central limitation.** The authors name only theoretical workarounds (artificial-dissipation integrators; embedding a dissipative system in a larger conservative one via ancillas) and flag credit assignment for *truly dissipative* systems as **an open problem**. RHEL also still uses explicit Hamiltonian-parameter gradients (not yet fully black-box).

### 5.3 The two decoupled bets (the key structuring idea)
- **Q1 — Can a photonic recurrence be trained in situ at all?** Answered by a **hybrid**: physical forward pass, **digital** echo (measure-and-reinject / digital optical phase conjugation). This isolates the recurrence-training question from the optical-echo question and would be the **first in-situ-trained recurrent photonic system** — publishable regardless of outcome.
- **Q2 — Can the echo be done all-optically?** The physics-native endpoint: on-chip phase conjugation via χ² cascade (SHG+DFG) or χ³ FWM. Optical phase conjugation is real and demonstrated for single beams/images, and digital OPC has reversed >200 spatial modes through a 1-km fiber at >80% fidelity — but **conjugating the entire instantaneous state of a recurrent multimode network on-chip is unsolved**, and FWM conjugation is intrinsically noisy. HEB's ancilla-based echo is theoretical.

**We win the major first (Q1) without betting the program on the hardest part (Q2).**

### 5.4 Fallbacks (graceful degradation)
- If realistic ASE destroys the echo gradient → fall back to **physics-aware training** (digital backward pass, *Nature* 2022 style): less elegant, non-physics-native, but functional.
- If an on-chip all-optical echo proves unattainable → commit permanently to **digital/hybrid conjugation** (Q1 route): forfeits the all-physical claim, keeps the in-situ-recurrence-training result.
- If task performance demands strong forgetting → adopt **D-LinOSS damping** and accept the (currently unsolved) dissipative-credit-assignment extension or a conservative-embedding ancilla.

---

## 6. Staged plan with decision gates (revised)

### Stage 0 — Theory + simulation *(now; no fab; publishable)*
- **Objectives.** (a) Formalize the oscillator↔ring mapping and bound the realizable pole region. (b) **Simulate RHEL on a realistic device model** — a coupled-ring/LinOSS HSSM with finite $Q$, erbium gain saturation, and injected ASE modelled as *zero-mean stochastic noise plus a systematic conjugation-error term* — and (c) map the gradient-fidelity-vs-accuracy frontier over the damping knob.
- **Approach.** Reuse the author's differentiable-mesh/SSM tooling; train via the convolutional view (stable, parallel).
- **Deliverables.** A pole-placement mapping paper; the gradient-survival result; the conservatism–damping frontier.
- **Gates.** Proceed iff (i) the idealized model reproduces oscillatory-SSM task accuracy within a pre-registered margin, **and** (ii) **RHEL's gradient stays within ~5–10% cosine error of BPTT** across the swept loss/gain/ASE-variance/echo-fidelity ranges. *If systematic conjugation error dominates → a calibration sub-routine is required before hardware. If ASE degrades gradients catastrophically even with averaging → pivot to physics-aware training.*

### Stage 1 — LTI oscillatory demonstrator + single optical echo *(TFLN chip; ~12–24 mo)*
- **Objectives.** (a) Demonstrate a trained oscillatory photonic SSM kernel in hardware (offline-trained weights, off-chip detection, modest memory so $|\lambda|<1$, **no gain, no selectivity**). (b) Build and characterize **one** TFLN phase-conjugating element (χ² cascade or χ³ FWM in a ring) and measure how faithfully it time-reverses a *multimode* state.
- **Deliverables.** Measured photonic-oscillator kernel with a pole-placement error budget; a single-element optical-echo fidelity figure.
- **Gates.** Kernel fidelity meets threshold → advance the device track. **Echo fidelity > ~90% over the memory window** → the all-optical echo (Q2) stays alive; below → commit to digital conjugation (Q1) and proceed.

### Stage 2 — Hybrid in-situ training of a small recurrence *(~24–36 mo)*
- **Objective.** Train a **2–6-ring HSSM with a physical forward pass and a digital echo** (DOPC-style) — the first in-situ-trained recurrent photonic system.
- **Deliverable.** A hardware-trained small photonic SSM; the headline first-mover result on Q1.
- **Gate.** In-situ-trained accuracy approaches the offline/simulated baseline within a target margin.

### Stage 3 — Full physics-native loop (+ selectivity)
- **Objective.** Replace the digital echo with the all-optical echo (Q2); only then, attempt incremental selectivity (input-dependent $C$, then $B$).
- **Gate.** Attempt the all-optical loop only after Stages 1–2 succeed; proceed to LTV "photonic-Mamba" only if per-step EO tuning needs no per-state high-speed DAC, else publish the in-situ-trained LTI/oscillatory result as the contribution.

---

## 7. Gain: dual role and status

Gain plays **two** roles here: it extends memory length (biases poles toward the imaginary axis) *and* it puts the system into the near-conservative regime echo training requires (§5). Per-device the requirement is met — erbium-doped TFLN waveguide amplifiers reach **16–38 dB internal net gain** with **~4.4–6 dB noise figures** across the C-band, are **phase-transparent** (ms upper-state lifetime, no amplitude-to-phase coupling — decisive for a coherent oscillator bank), and have been **monolithically co-integrated with a high-speed modulator** in a zero-change process. Alternatives are disqualified for inline use: III-V SOAs imprint Henry-factor phase chirp; SBS is ~20 MHz narrowband. **The unproven, modelling-critical quantities** are cascade OSNR through $N$ stages, the aggregate on-chip pump budget and its delivery (likely showstopper; mitigable via Er:Yb co-doping), and C-band gain-flatness/tilt. **New coupling in v0.2:** the gain that enables conservatism also injects ASE *into the training echo* — so the gain operating point trades off against gradient fidelity, which Stage 0 must quantify jointly.

---

## 8. Fabrication and toolchain route

The Stage-1 oscillatory demonstrator needs only mesh + rings (+ a χ² conjugation element), with off-chip detection and no gain — feasible on an open TFLN MPW.
- **Primary — Luxtelligence `lnoi400`:** the only TFLN platform with a genuinely open **gdsfactory-native PDK** (matching the author's workflow) + KLayout DRC, a public ~quarterly MPW calendar, a 1 cm × 0.5 cm die, ~3-month lead. C-band; >70 GHz modulators, MMIs, couplers. χ²/PPLN for the conjugation element is intrinsic to LN.
- **Backups:** QCi (gdsfactory PDK, US, on-platform PPLN); CCRAFT (open-to-startups MPW); LIGENTEC LABS (SiN host + TFLN modulator + on-chip InGaAs detection) if on-chip detection becomes attractive.
- **Practical blockers:** all TFLN MPW pricing is quote-based (plan a **mid-five-figure EUR** first-chip program incl. packaging); solo purchasing effectively requires a **registered entity**; US fabs add export-control screening. A cheap SiPh/SiN MPW (with Ge PDs) can prototype the mesh logic first if budget dominates.

---

## 9. Risks and mitigations (revised, ranked)

1. **Systematic echo / conjugation error.** Does *not* average out; corrupts the gradient. *Mitigation:* in-loop calibration that needs no knowledge of internal dynamics; characterize in Stage 0/1.
2. **Correlated ASE in the gain-loaded loop.** The biggest unverified assumption — may not average out like ideal zero-mean noise. *Mitigation:* low-NF erbium, moderate gain, Stage-0 noise model with a correlated component; fallback to physics-aware training.
3. **All-optical multimode-state echo.** Unsolved on-chip; FWM adds spontaneous noise. *Mitigation:* the Q1 hybrid (digital echo) carries the near-term claim; Q2 is a separate, longer bet.
4. **Conservatism vs. performance (damping).** RHEL exact at zero dissipation; D-LinOSS shows damping helps. *Mitigation:* damping as a swept knob; conservative-embedding ancilla or the (open) dissipative credit-assignment extension if strong forgetting is required.
5. **Selectivity / LTV updates.** Fixed optics is LTI. *Mitigation:* target oscillatory LTI first; add selectivity on $C$ then $B$.
6. **Gain cascade / loss budget & pump.** *Mitigation:* Stage-0 cascade OSNR + pump model; Er:Yb to cut pump.
7. **Long-term storage of learned parameters in an optical loop.** *Mitigation:* LN photorefractive/holographic or EO latching; non-volatile phase shifters.
8. **Thermal crosstalk, calibration, drift; clocking/synchronization of $\tau$.** *Mitigation:* the author's mesh-calibration methods; EO (not thermal) actuation.

---

## 10. Honest scope: feasibility vs. advantage

**What this is.** (1) A *device* first — a trained, structured photonic SSM (extending the IMSSA analog-electronic precedent into optics). (2) A *training* first — the **first in-situ-trained recurrent photonic system**, via the Q1 hybrid, with an all-optical self-learning loop (Q2) as the visionary endpoint. (3) A route to a niche where analog continuous-time wins — **ultra-low-latency RF/analog sequence processing** — connecting to microwave photonics and the author's optical-equalization background.

**What this is not (near-term).** A general-purpose GPU competitor. The DAC/ADC + E/O–O/E conversion overhead and the LTV selectivity requirement are structural; and RHEL/HEB are **theory + simulation only today**, so the all-physical self-learning loop is a frontier research bet, not an engineering deliverable. The program is designed to **degrade gracefully** (physics-aware training; digital conjugation) rather than fail binary.

**Dual academic–commercial frame.** Publish the Stage-0 mapping and gradient-survival results, then the Q1 in-situ-trained recurrence, for scientific priority. Keep company optionality open but **un-committed** until the noise budget (does the echo gradient survive ASE?) and the echo-fidelity question are answered. Protect architectural specifics of the gain-stabilized, self-learning realization for that optionality.

---

## 11. Indicative timeline

| Phase | Window (indicative) | Output |
|---|---|---|
| Stage 0 (theory + RHEL/device simulation) | months 0–6 | mapping paper; **gradient-survival-under-ASE result** (the gate, and the natural collaboration hook); damping frontier |
| Entity + quoting | months 3–6 (parallel) | registered entity; MPW quotes |
| Stage 1 (oscillatory chip + single optical echo) | ~12–24 mo | first oscillatory photonic-SSM kernel; echo-fidelity figure |
| Stage 2 (hybrid in-situ training) | ~24–36 mo | **first in-situ-trained recurrent photonic system** (Q1) |
| Stage 3 (all-optical echo + selectivity) | 36 mo+ | physics-native self-learning loop *or* a rigorous limits result |

---

## 12. Enabling capability and collaboration

The author brings an audited differentiable photonic-mesh codebase and optimization tooling (directly reusable for Stage 0), a mesh benchmark with parameter-economy and perturbation-tolerance findings and a chip loss/gain budget that motivated the gain track, hands-on RF/optical and PIC characterization experience (C2N, VLC) for Stages 1–2, a gdsfactory flow matching the Luxtelligence/QCi PDKs, and a reservoir-computing / POST-DIGITAL lineage adjacent to both the photonic-recurrence and physics-based-learning communities. The Hamiltonian-echo training direction sits naturally within that network; a collaboration on the *photonic realization* of RHEL is a stronger position than a solo reimplementation, and is best initiated once the Stage-0 gradient-survival result exists (i.e., a concrete finding to bring, not a question).

---

## References (to verify against primary sources before submission)

*Drawn from the underlying feasibility studies; recency- and detail-sensitive items flagged.*

1. Gu, Goel, Ré, *Efficiently Modeling Long Sequences with Structured State Spaces* (S4), 2021/2022.
2. Gu et al., *On the Parameterization and Initialization of Diagonal State Space Models* (S4D), 2022; Smith et al., *S5*, 2023.
3. Gu & Dao, *Mamba*, 2023; Mamba-2, 2024; *Mamba-3*, arXiv:2603.15569 (ICLR 2026) — **verify specifics against camera-ready.**
4. Rusch & Rus, *LinOSS: Oscillatory State-Space Models*, ICLR 2025, arXiv:2410.03943.
5. *D-LinOSS: Learning to Dissipate Energy in Oscillatory State-Space Models*, arXiv:2505.12171 (2025).
6. **Pourcel & Ernoult, *Learning long range dependencies through time reversal symmetry breaking* (RHEL), arXiv:2506.05259 (2025).**
7. Pourcel et al., *Generalized Lagrangian* unifying EqProp and HEB/RHEL (GLEP), arXiv:2506.06248 (2025).
8. López-Pastor & Marquardt, *Self-learning machines based on Hamiltonian echo backpropagation* (HEB), *Phys. Rev. X* 13, 031020 (2023).
9. Scellier & Bengio, *Equilibrium Propagation*, 2017; Laydevant, Marković, Grollier, *EqProp on a D-Wave Ising machine*, *Nat. Commun.* (2024).
10. Hughes, Minkov, Shi & Fan, *Training photonic neural networks through in-situ backpropagation* (TRIM), *Optica* (2018); Pai et al., experimental in-situ backprop, *Science* (2023).
11. Wright, Onodera, McMahon et al., *Deep physical neural networks trained with backpropagation* (physics-aware training), *Nature* 601, 549 (2022).
12. Zhou et al., *High-fidelity spatial mode transmission through a 1-km multimode fiber via vectorial time reversal* (DOPC), *Nat. Commun.* 12, 1866 (2021).
13. Siegel et al., *S4D on analog in-memory hardware* (IMSSA), arXiv:2412.20215.
14. Er:TFLN gain: Cai et al., arXiv:2108.08044 (16 dB); Xingjun Wang group (Peking U.), *Nat. Commun.* 16, 10462 (2025) (38 dB + modulator co-integration); Li/Yu/Cheng et al., *ACS Photonics* 12(11) (2025) (18 dB fiber-to-fiber).
15. Ye, Wang, Marpaung et al., *Brillouin photonics engine in TFLN*, *Sci. Adv.* (2025).
16. Wang et al., TFLN modulators >100 GHz, *Nature* 562, 101 (2018); Bogaerts et al., *Programmable photonic circuits*, *Nature* 585 (2020).
17. Luxtelligence `lnoi400` open gdsfactory PDK; QCi gdsfactory PDK (foundry docs).
18. Author's prior work — six-topology photonic-mesh equalizer benchmark; silicon-photonic NOFU-mesh chip budget (manuscripts in preparation).

---

*Status: draft v0.2. The recommended first action is Stage 0 — the oscillator↔ring mapping plus the RHEL-gradient-survival-under-ASE simulation — which is independent of fabrication, reuses existing tooling, and produces the result that gates everything downstream (and the finding to take to a potential collaborator). Three verification debts before any submission: the "no photonic SSM / no in-situ-trained recurrent photonic system" white-space claim, the LinOSS/Mamba-3 benchmark specifics, and the RHEL/HEB robustness claims (theory + simulation only).*
