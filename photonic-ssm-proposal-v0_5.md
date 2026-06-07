# An In-Situ-Trained Photonic State-Space Model on Silicon Nitride
### An Oscillatory (LinOSS) Coupled-Microring Recurrence, Trained on Hardware

*Research proposal — draft v0.5 (supersedes v0.4; for circulation and iteration)*

> **Changes since v0.4 (v0.5 — a framing & precision pass, not the substantive revision).** Five surgical edits for external circulation, no structural change. **(1) RHEL re-promotion reframed honestly.** The SiN flip improves RHEL's *noise* odds but does **not** reopen feasibility: the echo's physical primitive — optical phase conjugation, which needs χ²/χ³ — is precisely what low-loss/weak-nonlinearity SiN is worst at, and any gain injects irreducibly-irreversible ASE. RHEL is now evaluated *in simulation* on those honest terms, with its echo sub-model required to commit to a concrete conjugation mechanism (§5.2, §6). **(2) Bake-off primary metric** changed to sample-efficiency-to-target-accuracy under realistic noise; gradient-cosine-error demoted to a secondary diagnostic (used alone it structurally flatters the exact methods) (§6). **(3) Systems-advantage envelope** promoted from "a section to keep sharp" to an explicit Stage-0 deliverable, and distinguished from the training-baseline comparison (§6, §10). **(4) Gap-2 white-space claim sharpened** to its precise form — recurrent parameters updated *on the device* by gradient-based/-estimating training — with named pre-emption of the closest priors (§2). **(5) Unselective scope owned** as a deliberate continuous-signal/time-series choice rather than an incidental deferral (§4). The substantive revision — concrete echo-mechanism analysis, advantage numbers, bake-off results — awaits Stage 0.
>
> **Changes (v0.4, since v0.3).** Repositioned the training program from *primary + contingent* to a **parallel four-method bake-off in Stage-0 simulation** (PAT, SPSA, recurrent in-situ adjoint, RHEL on the same dissipative ring model). **Guardrail: parallel in simulation, singular in hardware** — the Stage-1 chip stays committed to the PAT/SPSA workhorse, and the bake-off decides whether the adjoint or RHEL earns a later hardware slot.
>
> *Earlier (v0.3): platform flipped TFLN → ultra-low-loss SiN, and training moved off RHEL onto PAT + SPSA, after two neutral comparative studies overturned both salience-anchored choices; the conservatism–damping tension dissolved (damping is now a free design knob). The headline contribution — first in-situ-trained recurrent photonic system — is platform- and method-independent and unchanged.*

---

## Abstract

State-space models (SSMs) are the leading linear-recurrence alternative to attention, and their unselective core is a linear time-invariant system — a rational transfer function — which integrated photonics builds natively. This proposal develops a **photonic SSM as an oscillatory (LinOSS-style) coupled-microring recurrence on silicon nitride**, in which rings are complex poles/oscillators, optical loss sets the damping, and erbium (or III-V) gain extends effective memory. The central scientific target is not the device alone but **training the physical recurrence in situ** — no recurrent photonic system has been so trained by any method. We adopt **Physics-Aware Training (a hybrid digital-twin, hardware-in-the-loop method) and SPSA (model-free, zeroth-order)** as the primary, hardware-committed route: both are dissipative-agnostic, absorb hardware non-idealities, and are demonstrated on photonic chips. Two exact/physics-native methods — a **recurrent/time-domain extension of in-situ photonic adjoint backpropagation** and **Hamiltonian-echo learning (RHEL)** — are evaluated *in parallel* with PAT/SPSA in a Stage-0 simulation bake-off on the same dissipative ring model, with the hardware roadmap held on the proven PAT/SPSA route until the simulation promotes one. Silicon nitride is chosen for its class-leading ring $Q$ / low loss — the figure of merit that bounds memory length — and its drift-stable thermo-optic tuning, which suits gradient-free weight loading. The plan is staged with explicit decision gates and graceful fallbacks (offline-train-deploy; reservoir-readout baselines). We are candid that this is a *feasibility-first* program: a first-mover scientific demonstration and a route to a low-latency analog niche, **not** a near-term general-purpose accelerator.

---

## 1. Background and motivation

### 1.1 SSMs as transfer functions
A structured SSM layer is the continuous-time system $\dot{x}=Ax+Bu,\;y=Cx+Du$, whose recurrent, convolutional ($y=u*K$, an IIR/FIR kernel), and parallel-scan views all describe one rational transfer function $H(s)=C(sI-A)^{-1}B+D=\sum_i c_ib_i/(s-a_i)+D$ — a sum of one-pole (Lorentzian) terms. Photonics realizes $H(s)$ directly: poles are damped optical resonances, residues are couplings, delays supply memory.

### 1.2 The oscillatory (LinOSS) unit
We target the **LinOSS oscillator** — a forced harmonic-oscillator SSM. It is the natural coupled-ring abstraction, it is state-of-the-art on the longest-range benchmarks, and — decisively for v0.3 — **it is proven stable for any nonnegative-diagonal (i.e. dissipative) state matrix**, so a lossy-but-high-$Q$ ring lattice is squarely in its valid regime. With the conservative-physics training method no longer the primary (§5), we are not bound to near-conservative dynamics, so **damping becomes a free design knob**: D-LinOSS-style *learnable* damping can be used for performance. *(Verify LinOSS/D-LinOSS benchmark specifics before load-bearing use.)*

### 1.3 Why silicon nitride
For a dissipative oscillatory ring recurrence the dominant figure of merit is **round-trip loss / intrinsic $Q$**, because every dB lost per round trip erodes effective memory length. Ultra-low-loss SiN is the class leader — foundry films at single-digit dB/m and intrinsic $Q>10^7$, roughly an order of magnitude better than the *accessible* TFLN foundry. SiN's other properties fit this project's needs: its small thermo-optic coefficient makes resonances intrinsically drift-stable, which matters for gradient-free in-situ training; mature, gdsfactory-native open MPWs (CORNERSTONE, LIGENTEC) make it accessible to a solo operator; and erbium or III-V gain can be added *within the SiN family* to extend memory. Its honest weaknesses — no native gain or detection (heterogeneous integration needed), weak χ³ / no χ², larger bend radii (lower ring density) — are weighed in §7–§9. TFLN's headline strengths (fast EO, χ²) are unused under this framing; it is retained only as a fallback (§8) should the framing reverse.

---

## 2. Prior art and the white space (two gaps)

**Gap 1 — no photonic SSM (the device).** Microwave-photonic IIR/FIR filters and programmable meshes are *hand-set* transfer functions; photonic reservoir computing leaves the recurrence *untrained*; ROSS-NN is a filter-bank neuromorphic net; IMSSA (arXiv:2412.20215) is the first S4D kernel on analog hardware but is *electronic*. A trained, structured photonic SSM is open.

**Gap 2 — no in-situ-trained recurrent photonic system (the training).** In-situ backpropagation is established for *feedforward* photonics (Hughes/Minkov/Shi/Fan, *Optica* 2018; Pai et al., *Science* 2023), and the recurrent case has been shown only in *simulation* (Hughes et al., "wave physics as an analog RNN," *Sci. Adv.* 2019). Physics-Aware Training (*Nature* 2022) trains real hardware with a digital backward pass. Photonic *recurrent* systems have been trained only at the readout or externally. **Stated precisely, the open claim is this: the recurrent parameters themselves — the pole positions and inter-ring couplings that *define* the recurrence — have never been updated *on the physical device* by gradient-based or gradient-estimating training.** We pre-empt the closest priors explicitly: photonic reservoir computing fixes the recurrence and trains only a linear readout; the photonic-RNN reinforcement-learning line (Bueno, Brunner et al., *Optica* 2018) trains output/readout weights by reward rather than updating the recurrent weights in situ; and reservoir variants that adapt *internal* parameters do so without gradient-based training of the recurrence. *(This is the single load-bearing sentence of the proposal; it carries a verification debt — a systematic prior-art search is owed before submission. Mid-2026 snapshot.)*

**Claim.** A *trained, structured photonic SSM* (Gap 1) that is, moreover, *trained in situ* (Gap 2) is open white space on both axes (to our knowledge, mid-2026), and is independent of the platform/training-method specifics below.

---

## 3. Core mapping: oscillator → ring-bank

Near resonance, an add-drop microring has a single Laplace-domain pole $s_{\text{pole}}=-\kappa_{\text{tot}}+i\,\omega_{\text{res}}$, with $\omega_{\text{res}}$ the detuning and $\kappa_{\text{tot}}$ the total amplitude decay rate. Identifying with an oscillator/eigenvalue $a_i=-\exp(\alpha_i)+i\beta_i$:

| SSM / oscillator quantity | Physical realization (SiN) | Tuning handle |
|---|---|---|
| oscillation frequency $\beta_i$ | ring resonance detuning | thermo-optic phase shift (trench-isolated) |
| damping $-\exp(\alpha_i)$ | total decay rate $\kappa_{\text{tot}}$ | bus–ring coupling (+ net gain) |
| longer memory ($|\lambda|\to1$) | round-trip loss → 0 (net gain ≈ unity) | Er:SiN / III-V loop gain |
| residue $c_ib_i$, and $B,C$ | input/output couplings + MZI mesh | thermo-optic mesh phases |
| step $\Delta$ | loop round-trip time $\tau$ | path length / delay |
| $D$ (skip) | through path | bypass + weight |

An $N$-ring add-drop bank fed/read by a thermo-optic MZI mesh realizes an $N$-oscillator LinOSS layer. **Damping is set deliberately** for performance (D-LinOSS), unconstrained by the primary training method.

---

## 4. Pole-placement and expressivity

- **Stability is free** (passive rings give $|\lambda|<1$); LinOSS is valid for any nonnegative-diagonal $A$, so the dissipative ring lattice is in-regime.
- **Memory length is loss-limited**: minimum damping is set by intrinsic loss, so the lowest-loss platform (SiN) maximizes passive memory; gain (§7) extends it. The conservatism–damping tension of v0.2 **no longer exists** — damping is a swept hyperparameter chosen for accuracy.
- **FSR and fabrication tolerance**: detunings $\beta_i$ are FSR-bounded; poles are *placed* by post-fab thermo-optic trimming (a calibration problem; SiN's drift-stability helps).
- **Selectivity (LTV) gap**: input-dependent dynamics (Mamba) require per-sample pole/coupling rewriting — deferred to Stage 3; we target time-invariant oscillatory dynamics first. This is a *deliberate scope choice, not an incidental deferral*: an unselective LTI core ties the program to continuous-signal and time-series tasks — where LinOSS is genuinely competitive — and away from language-like tasks, where selectivity is precisely what made Mamba win. The choice is consistent with this proposal's time-series target, and it is also part of *why* the eventual advantage is niche rather than general (§10).

---

## 5. Training: in-situ learning on a dissipative recurrence

The hardest scientific target is training the *physical* recurrence. The realized device is dissipative (loss + gain + ASE), which rules out methods that need conservative or fixed-point physics as the *primary* route: RHEL/Hamiltonian-echo requires non-dissipative time-reversible dynamics (its authors note the mapping "does not straightforwardly extend" to dissipative/port-Hamiltonian systems), and Equilibrium Propagation requires relaxation to an energy minimum.

### 5.1 Primary, hardware-committed method — PAT + SPSA
- **Physics-Aware Training (PAT)** (Wright et al., *Nature* 2022): the forward pass runs on the physical recurrence (unrolled in time); the backward pass runs on a differentiable digital twin. Physics-agnostic — gain, loss, and non-reciprocity are fine — and it trains the *physical* recurrence in the loop. Bounded by twin fidelity.
- **SPSA / zeroth-order fine-tuning**: estimates the gradient of *all* parameters from **two physical forward passes**, model-free, and *naturally absorbs* hardware noise and thermal crosstalk. A 2026 photonic demonstration trained 2,132 on-chip parameters this way with ~0.43% accuracy loss under severe crosstalk. Variance grows with parameter count — a real concern at scale, manageable at demonstrator scale.
- **Together** they deliver the contribution honestly: *first in-situ training of a photonic recurrence*, with the method labelled as hybrid PAT and/or model-free SPSA — **not** an exact-gradient or Hamiltonian claim the hardware cannot support.

### 5.2 Parallel exact/physics-native candidates — evaluated in Stage-0 simulation
Two aspirational methods would each give *exact, fully physical* gradients through the recurrence — the strongest version of the novelty — and both are evaluated **in parallel with PAT/SPSA in the Stage-0 bake-off (§6)** on the same realistic dissipative ring model, at low marginal cost since the substrate model is shared:
- **Recurrent in-situ photonic adjoint backprop** (Hughes/Fan/Pai lineage). Demonstrated only for feedforward meshes; the recurrent/cavity case is simulated but not built, and the adjoint field's interaction with gain and (under dynamic drive) non-reciprocity must be solved.
- **RHEL / Hamiltonian echo.** Re-examined under the SiN flip, with the conclusion stated honestly in both directions. The flip genuinely improves one term: low-loss SiN needs far less gain → less injected ASE → forward dynamics closer to the near-conservative regime RHEL assumes (the TFLN-era demotion was conditioned on a much lossier, gain-heavy device). But two countervailing facts keep this an *odds-improvement, not a feasibility reopening.* **(i)** RHEL's echo requires a *physical time-reversal* operation — for optical fields, phase conjugation — which is generated by χ²/χ³ nonlinear processes, precisely what SiN is worst at; the same low-loss / weak-nonlinearity property that maximizes memory makes the echo's core primitive *harder* to realize on-chip, possibly forcing it off-chip or onto a non-SiN element. **(ii)** Any loop gain injects ASE, and spontaneous emission is irreducibly irreversible — the echo cannot retrace noise added after the fact — so a noise floor remains regardless of how low the passive loss goes. Net: SiN improves RHEL's quantitative odds but does not change the *kind* of problem. Accordingly RHEL earns a parallel evaluation **in simulation**, on honest terms: Stage 0 tests its *noise/conservatism* regime while explicitly **bracketing the unsolved implementation primitive** (on-chip phase conjugation), which must be grounded in a concrete candidate mechanism — or an explicit off-chip admission — before any hardware promotion (§6, task c). RHEL's extra modelling cost is exactly this echo / phase-conjugation sub-model.

**Cross-link to the platform choice.** The two exact-gradient routes relate to SiN *differently*, and it is worth not lumping them. The **recurrent adjoint** benefits cleanly: it needs phase-coherent, low-loss propagation and (under dynamic drive) reciprocity, all of which SiN supplies well — arguably better than a lossier platform, since cleaner interference sharpens the gradient read. **RHEL** benefits only on the noise axis (§5.2 above) while being hampered on the phase-conjugation axis, so SiN is unambiguously friendly to the adjoint but mixed for RHEL. **Guardrail:** this is parallelism *in simulation*. The Stage-1 chip stays committed to the proven PAT/SPSA workhorse; the bake-off decides whether the adjoint or RHEL earns a *later* hardware slot, so the speculative options are evaluated cheaply without pulling the hardware roadmap prematurely.

### 5.3 Baselines (forfeit the novelty, but make it meaningful)
**Offline-train-then-deploy** (train a digital LinOSS, map weights to the chip) and **reservoir-readout** (recurrence left fixed) are the safe fallbacks and the comparison points that quantify what in-situ training of the recurrence actually buys. A LNOI/SiN microring reservoir is already demonstrated, giving a concrete baseline.

---

## 6. Staged plan with decision gates

### Stage 0 — Theory + simulation, incl. the four-method bake-off *(now; no fab; publishable)*
- **Objectives.** (a) Formalize the oscillator↔SiN-ring mapping and bound the realizable pole region. (b) **Run a four-method in-situ-training bake-off** on the *same* realistic dissipative ring model (finite $Q$, gain saturation, injected ASE) — **SPSA, PAT, recurrent in-situ adjoint, and RHEL/Hamiltonian-echo** — with the **primary score being sample-efficiency-to-target-accuracy under realistic noise** (does the method train to the pre-registered task accuracy, and at what cost in physical forward passes) as loss, gain, and ASE are swept. Gradient-direction agreement (cosine error vs a BPTT reference) is retained as a *secondary diagnostic only*: used as the headline it structurally flatters the exact methods (adjoint, RHEL) and penalizes SPSA — whose poor per-step alignment averages to good convergence — which would bias an evaluation built to be even-handed. (c) **Build the optical-echo sub-model, grounded in a concrete mechanism — not an abstract error term.** RHEL's echo requires physical time-reversal (phase conjugation), so the sub-model must commit to a *specific candidate conjugation route* — e.g. a defined χ³ four-wave-mixing scheme with its real pump-power, bandwidth, conversion-efficiency, and added-noise penalties, or an explicit admission that conjugation needs off-chip / non-SiN elements — with a conjugation-fidelity and systematic-error term layered on top. An idealized conjugation operator would let the bake-off promote RHEL on a primitive SiN may not deliver; modelling the mechanism honestly is the main reason RHEL costs more effort than the other three. (d) Choose the damping operating point for accuracy (D-LinOSS sweep). (e) **Sketch the systems-advantage envelope** (§10): end-to-end latency/energy for the target low-latency niche, *including* E/O–O/E and DAC/ADC conversion overhead, against a digital baseline on the same task.
- **Approach.** Reuse the author's differentiable-mesh/SSM tooling; train the digital model via the convolutional view; share one substrate model across all four estimators so the comparison is apples-to-apples.
- **Deliverables.** A mapping paper; **a comparison of in-situ training methods for a photonic oscillatory recurrence under realistic loss/gain/ASE** — a publishable result in its own right, and the concrete RHEL-on-SiN finding that would anchor any collaboration outreach; the damping/accuracy curve; **a first-pass systems-advantage envelope** (latency/energy vs a digital baseline including conversion overhead, §10).
- **Gates.** Proceed to hardware iff (i) the model reproduces oscillatory-SSM task accuracy within a pre-registered margin, and (ii) at realistic SiN noise levels **at least one method trains to the pre-registered accuracy** — with **PAT/SPSA as the default hardware choice** regardless. *Promote the adjoint or RHEL to a hardware slot only if the bake-off shows it clearly beats PAT/SPSA on a metric that matters (exactness, scaling, or hardware simplicity); if SPSA variance is prohibitive at the target parameter count, lean on PAT and reserve SPSA for fine-tuning.*

### Stage 1 — SiN oscillatory demonstrator + in-situ training *(chip; ~12–24 mo)*
- **Objectives.** (a) Fabricate coupled-ring LinOSS unit cells on an **open SiN MPW (CORNERSTONE or LIGENTEC)** with trench-isolated thermo-optic tuners; off-chip detection; opto-electronic nonlinearity between linear layers. (b) Train the physical recurrence in situ via **PAT + SPSA**, benchmarking against offline-deploy and a reservoir-readout baseline.
- **Deliverables.** A measured oscillatory photonic-SSM kernel; the *first in-situ-trained recurrent photonic system* result.
- **Gates.** (i) **Intrinsic $Q\geq10^6$ per ring** and round-trip loss low enough that the target sequence length fits the memory budget. (ii) **Resonance drift below the SPSA perturbation amplitude over one training epoch** (SiN's low $\mathrm{d}n/\mathrm{d}T$ favors this; if not met, add active resonance locking). (iii) **In-situ training beats offline-deploy by more than measured run-to-run hardware drift** — else the in-situ claim is not yet defensible.

### Stage 2 — Memory-rich / gain-rich version *(within the SiN family; ~24–36 mo)*
- **Objective.** Add loop gain to push effective memory toward the non-fading regime; add native detection.
- **Approach.** Monolithic **Er:Si₃N₄** (low-NF, distributed, in-loop friendly) or **heterogeneous III-V SOA-on-SiN** (lumped, electrically pumped) on the *same SiN waveguide layer* — Stage-1 ring/bend/gdsfactory libraries carry forward. Add Ge/III-V detection.
- **Gate.** Loop OSNR and gain flatness sustain usable state precision at the target memory length (Stage-0 model validated on-chip).

### Stage 3 — Exact gradients and/or selectivity
- **Objective.** Attempt whichever exact-gradient method the Stage-0 bake-off promoted (recurrent in-situ adjoint or RHEL/Hamiltonian-echo) on hardware, and/or incremental selectivity (input-dependent $C$, then $B$).
- **Gate.** Proceed to an all-physical exact-gradient loop or LTV "photonic-Mamba" only if the relevant sub-problem (reciprocal adjoint-field injection, or a low-loss echo regime *with a realizable phase-conjugation mechanism*; per-step tuning without per-state DACs) is solved; otherwise publish the PAT/SPSA-trained oscillatory result as the contribution.

---

## 7. Gain: memory extension on SiN

Gain extends effective memory by compensating round-trip loss. On SiN the options are **monolithic Er:Si₃N₄** — >30 dB small-signal / 26 dB on-chip net over a ~50 cm spiral at ~1.0–1.4 dB/cm (the flagship 2022 result) and related Er:Al₂O₃-on-SiN devices reporting >16 dB net with ~3 dB NF over 30 cm — or **heterogeneous III-V SOA-on-SiN** (9–15 dB on-chip, electrically pumped, compact). Erbium is preferred *inside* an oscillatory loop: low NF and no carrier-induced distortion, whereas SOA ASE and saturation add noise/nonlinearity (the latter possibly exploitable as activation, but it complicates the linear SSM). **Two honest flags:** the flagship Er:Si₃N₄ device published gain but **no measured noise figure** (only erbium's ~3 dB quantum limit) — so the in-loop *noise* budget is the less-proven number and must be verified, and unlike v0.2's Er:TFLN (measured NF ~4.4–6 dB) it cannot yet be taken as given. Because SiN's loss is so low, *less* gain is needed than on a higher-loss platform, which reduces total injected ASE — the main reason the platform and noise stories pull the same way (and the same reason SiN *improves, though does not by itself reopen,* RHEL's echo *noise* regime, §5.2).

---

## 8. Fabrication and toolchain route

The Stage-1 demonstrator needs only SiN rings + thermo-optic mesh, with off-chip detection and no gain — feasible on an open SiN MPW in the author's gdsfactory flow.
- **Primary — CORNERSTONE SiN MPW:** open GDSII/gdsfactory PDK, Europractice/JePPIX access, UK-academic subsidy, frequent low-cost runs. Submit coupled-ring LinOSS unit cells with trench-isolated TiN heaters.
- **Alternate — LIGENTEC AN800:** gdsfactory-compatible, ~15 runs/year, mature low-loss SiN.
- **Stage-2 gain/detection:** Er:Si₃N₄ (monolithic) or µTP/bonded III-V SOA-on-SiN; Ge/III-V detection — all *within the SiN family*, so Stage-1 layouts carry forward.
- **Practical blockers:** MPW pricing is quote-based (a SiN test reticle is typically *cheaper* and more accessible than the TFLN equivalent); solo purchasing benefits from a registered entity; heterogeneous-integration MPW access (for Stage-2 gain/detection) remains limited as of mid-2026 and is the harder procurement step.
- **Fallback platform:** reconsider TFLN *only if* the framing reverses (all-optical adjoint/echo training, or input-dependent χ²-based selectivity becomes central); reconsider InP only if native gain+detection outweighs its high passive loss (unlikely for a memory-centric loop).

---

## 9. Risks and mitigations (ranked)

1. **Er:SiN in-loop noise is under-characterized.** Flagship device has no published NF. *Mitigation:* Stage-0 noise model with conservative NF assumptions; measure NF early; III-V-on-SiN or Er:Al₂O₃ alternatives with reported NF as backup.
2. **SPSA variance at scale.** Zeroth-order variance grows with parameter count. *Mitigation:* PAT (digital backward) as the scalable workhorse, SPSA for fine-tuning; structured/blockwise perturbations.
3. **PAT twin fidelity.** Gradient bias from a poor model of ring dynamics/gain/ASE. *Mitigation:* careful twin calibration; SPSA correction; characterize twin mismatch in Stage 0.
4. **The exact-gradient candidates (recurrent adjoint, RHEL) are undemonstrated, and RHEL adds modelling cost.** Bidirectional propagation, coherent error injection, adjoint–gain interaction, and (for RHEL) a faithful echo/phase-conjugation sub-model are all unsolved or extra work. *Mitigation:* both are evaluated cheaply in the Stage-0 simulation bake-off, **not** committed to hardware; PAT/SPSA carries the near-term claim, and a speculative method earns a hardware slot only if the bake-off clearly justifies it (the §5.2 guardrail).
5. **SiN ring density at scale.** Larger bend radii limit rings/reticle. *Mitigation:* Euler/advanced bends; fine for a first demonstrator; if hundreds of rings are needed, weigh an SOI loss compromise.
6. **Memory length loss-limited even on SiN.** *Mitigation:* Stage-2 gain; shorter-memory multi-layer designs.
7. **Selectivity / LTV** (fixed optics is LTI). *Mitigation:* oscillatory LTI first; selectivity on $C$ then $B$ later.
8. **Long-term storage of learned parameters; thermo-optic power/locking.** *Mitigation:* trench-isolated low-crosstalk heaters; active locking if drift exceeds the SPSA perturbation; non-volatile phase-shifter options.

---

## 10. Honest scope: feasibility vs. advantage

**What this is.** A *device* first (a trained, structured photonic SSM), a *training* first (the **first in-situ-trained recurrent photonic system**, via PAT/SPSA, with the exact recurrent-adjoint or RHEL as the visionary upgrade), and a route to a low-latency analog niche. **What it is not (near-term):** a general-purpose GPU competitor — the DAC/ADC + E/O–O/E overhead and the LTV selectivity requirement are structural.

**The program shed its fragile exotic elements and kept the contribution.** Two neutral comparisons removed TFLN's χ²/EO rationale and RHEL's *primary* status, converging on a *buildable* core (SiN rings + PAT/SPSA), while the exact-gradient methods are now de-risked cheaply in simulation rather than bet on. The first-mover novelty survives because it is platform- and method-independent. **The remaining un-audited assumption is the premise itself** — that a photonic SSM is worth building, and where its genuine advantage over digital lies. After watching neutral analysis twice dissolve an anchor, this is the assumption to keep most honest before committing fabrication budget; it is *not* a reason to stall, but a reason to keep this section sharp and to treat the baselines (offline-deploy, reservoir) as the real test of whether in-situ training buys anything. **Two distinct advantage questions hide here, and the baselines answer only one.** The offline-deploy and reservoir baselines test the *training* advantage — whether training the recurrence in situ beats leaving it offline or fixed. They say nothing about the *systems* advantage — whether a photonic SSM beats a digital one once the E/O–O/E and DAC/ADC overhead is paid. The scientific first stands without a systems advantage; the commercial thesis does not. Accordingly a **first-pass quantitative advantage envelope is promoted from "a section to keep sharp" to an explicit Stage-0 deliverable** (§6, objective e): pick the target low-latency niche, write the end-to-end latency/energy budget *including* conversion overhead, and compare to a digital baseline on the same task. If even the optimistic envelope fails to clear digital, that is worth knowing *before* the MPW spend, not after.

**Dual academic–commercial frame.** Publish the Stage-0 mapping/bake-off and the Q1 in-situ-trained recurrence for scientific priority; keep company optionality open but un-committed until the advantage question is answered empirically against the baselines.

---

## 11. Indicative timeline

| Phase | Window (indicative) | Output |
|---|---|---|
| Stage 0 (mapping + four-method training bake-off) | months 0–6 | mapping paper; **comparison of in-situ training methods under realistic noise** (incl. the RHEL-on-SiN result); damping/accuracy curve; first-pass systems-advantage envelope |
| Entity + quoting | months 3–6 (parallel) | registered entity; SiN MPW quotes |
| Stage 1 (SiN demonstrator + in-situ training) | ~12–24 mo | **first in-situ-trained recurrent photonic system** |
| Stage 2 (Er:SiN / III-V-on-SiN gain + detection) | ~24–36 mo | memory-rich version; loop-noise characterization |
| Stage 3 (exact-gradient method and/or selectivity) | 36 mo+ | hardware exact-gradient or selective extension *or* a rigorous limits result |

---

## 12. Enabling capability

The author brings an audited differentiable photonic-mesh/SSM codebase and optimization tooling (directly reusable for Stage 0 and the bake-off); a mesh benchmark whose **thermal-crosstalk and perturbation-tolerance findings are now directly on-point**, since the SiN route relies on trench-isolated thermo-optic tuning and SPSA's crosstalk-robustness; hands-on RF/optical and PIC characterization experience (platform-agnostic, applicable to Stages 1–2); a gdsfactory flow matching the CORNERSTONE/LIGENTEC PDKs; and a reservoir-computing / POST-DIGITAL lineage adjacent to the photonic-recurrence and physics-based-learning communities (relevant to the adjoint and RHEL tracks).

---

## References (to verify against primary sources before submission)

1. Gu et al., S4 (2021/2022); S4D (2022); Smith et al., S5 (2023).
2. Gu & Dao, *Mamba* (2023); Mamba-2 (2024); *Mamba-3*, arXiv:2603.15569 (ICLR 2026) — verify specifics.
3. Rusch & Rus, *LinOSS: Oscillatory State-Space Models*, ICLR 2025, arXiv:2410.03943 (stability for nonnegative-diagonal $A$); *D-LinOSS* (learnable damping), arXiv:2505.12171.
4. Wright, Onodera, McMahon et al., *Deep physical neural networks trained with backpropagation* (Physics-Aware Training), *Nature* 601, 549 (2022).
5. Ranjan et al., hybrid digital-twin + SPSA in-situ training on a photonic chip (2,132 params, two forward passes, crosstalk-robust), arXiv:2604.02429 (2026) — recent; verify.
6. Hughes, Minkov, Shi & Fan, in-situ photonic adjoint/TRIM, *Optica* 5, 864 (2018); Pai et al., experimental feedforward in-situ backprop, *Science* 380, 398 (2023); Hughes et al., "wave physics as an analog RNN" (recurrent, simulation), *Sci. Adv.* 5, eaay6946 (2019).
7. Pourcel & Ernoult, RHEL, arXiv:2506.05259 (2025); Pourcel et al., GLEP / port-Hamiltonian non-extension, arXiv:2506.06248 (2025); López-Pastor & Marquardt, Hamiltonian Echo Backpropagation, *Phys. Rev. X* 13, 031020 (2023). *(Evaluated in the Stage-0 bake-off.)*
8. Ultra-low-loss SiN: damascene SiN ~3 dB/m, $Q\sim10^7$ (Kippenberg group); LIGENTEC / LioniX TriPleX foundry specs ($\leq0.1$–~2 dB/m); anneal-free SiN 8.66 dB/m, $Q$ 4.03M.
9. Er:Si₃N₄ amplifier (>30 dB small-signal / 26 dB on-chip net, ~1.0–1.4 dB/cm), *Science* (2022); Er:Al₂O₃-on-SiN (>16 dB net, ~3 dB NF over 30 cm; 24 dB fiber-to-fiber over 50 cm); III-V SOA-on-SiN (9–15 dB on-chip). **NF for the flagship Er:SiN device not measured — verify.**
10. TFLN drift liability: Liu et al., long-lived light/temperature-induced index change in Z-cut TFLN microresonators (recovery >10 h), *npj Nanophotonics* (2024), arXiv:2409.12354. TFLN low loss reference: Zhu, Hu & Lončar et al., 29M intrinsic $Q$ (1.3 dB/m), *Photonics Research* 12(8):A63 (2024).
11. IMSSA (S4D on analog in-memory hardware), arXiv:2412.20215; LNOI/SiN microring reservoir computing, arXiv:2408.13476.
12. CORNERSTONE and LIGENTEC SiN MPW / gdsfactory PDKs (foundry documentation).
13. Author's prior work — six-topology photonic-mesh equalizer benchmark; silicon-photonic NOFU-mesh chip budget (manuscripts in preparation).

---

*Status: draft v0.5 (a framing & precision pass over v0.4 — no substantive/Stage-0 content added; the substantive revision, with concrete echo-mechanism analysis, advantage numbers, and bake-off results, awaits Stage 0). Recommended first action: Stage 0 — the oscillator↔SiN-ring mapping plus the four-method (SPSA, PAT, recurrent-adjoint, RHEL) training bake-off on a shared realistic ring model, which is platform-parametric, reuses existing tooling, and gates fabrication. Verification debts before submission (unchanged): the "no photonic SSM / no in-situ-trained recurrent photonic system" white-space claim; LinOSS/D-LinOSS/Mamba-3 specifics; the Er:Si₃N₄ noise figure; and the recurrent-adjoint gap (inferred from absence of demonstrations, mid-2026 snapshot). Largest remaining conceptual risk: the advantage question of §10, now a Stage-0 deliverable, to be tested empirically against the offline-deploy and reservoir baselines.*
