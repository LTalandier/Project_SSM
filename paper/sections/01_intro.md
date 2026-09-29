# §1 — Introduction

**Status:** v2, condensed 2026-09-29 for the first public deposit. Claims, numbers and verdicts
carried over from v1 (commit `a508a28`); process detail moved to supplementary N9. Scope: W1 only.

---

## 1.1 The gap

Photonic neural networks now train themselves on-chip in feedforward form: model-free
perturbative methods [CITE-Spall; CITE-SPSA-photonic], hybrid physical-forward/digital-backward
methods [CITE-Wright-2022], and in-situ adjoint methods that read gradients from interference
[CITE-Hughes-2018]. Recurrent photonic processors, whose memory lives in the physics, have barely
received such training. Reservoir computing avoids the problem by fixing the recurrence and
training only a readout [CITE-reservoir-reviews]. Where internal parameters of a photonic
recurrence have been adjusted, it has been by calibration or regime-tuning rather than
task-driven training [CITE-servo-lineage], by reinforcement-style search over a readout while
the loop stays fixed [CITE-Bueno-Brunner], or with the recurrent state carried digitally between
optical passes [CITE-Boehm-class]. A two-modality literature search with a pre-registered kill
criterion (supplementary N3) found no demonstration, by any method, of the following:

> **a continuous-time dissipative-resonator recurrence — pole positions and inter-resonator
> couplings — trained in situ on the physical device by gradient-based or gradient-estimating
> methods on a computational task.**

Each qualifier is load-bearing. *On a computational task* excludes the servo and calibration
lineage; *physical parameters of the recurrence* excludes hybrid-digital state carriage;
*weight-tied recurrence* excludes feedforward meshes folded in time. The nearest neighbor is the
optical recurrent accelerator of Wu et al. [CITE-Wu-eLight-2025]. Its ORNN chip is trained in
situ by a model-free perturbative method (SPGD) on classification, with a weight-tied mesh applied
across wavelength-encoded time steps, which makes it, to our knowledge, the first in-situ-trained
optical recurrent network of any kind. Its trained weights are interferometer-mesh voltages,
however; its recurrent state is regenerated electronically at every step through a
photodetector–modulator relay, and its resonators are calibrated once and held static. The
resonator recurrence itself stays untrained. The other near-misses each fall along one
qualifier: all-photonic on-chip backpropagation for a *feedforward* network [CITE-Ashtiani-2026];
microring weight banks trained in situ as *feedforward* layers [CITE-Zhao-2025]; a time-synthetic
fiber-loop network whose per-step parameters are distinct, i.e. unrolled feedforward
[CITE-time-synthetic]; microring weights inside an analog recurrent loop trained by particle-swarm
search, *without gradients* [CITE-Zhang-eLight-2026]; an optoelectronic delay reservoir whose
recurrence parameters were optimized by Bayesian search *through a digital loop*
[CITE-OERC-insitu]; and a silicon photonic reservoir equalizer trained in hardware *in its readout
only* [CITE-spatial-RC]. No coupled-resonator lattice has had its couplings learned on-device by
any method. The claim is time-indexed: the last bounded search ran on 2026-09-13, and the
dated record is in supplementary N3.

## 1.2 Why a state-space model, and why silicon nitride

Deep state-space models showed that *linear* recurrences with well-placed poles carry most of
long-sequence performance [CITE-S4; CITE-S4D], and the oscillatory LinOSS line extended this to
second-order units that are exactly coupled damped oscillators [CITE-LinOSS; CITE-D-LinOSS]. A
lattice of coupled microrings *is* such a system: poles are ring detunings and losses, couplings
are physical couplers, and the LinOSS stability analysis tolerates nonnegative damping, so a
lossy-but-high-Q lattice is in-regime rather than an approximation to a conservative ideal (§2).
Damping becomes a design knob.

The figure of merit for a dissipative ring recurrence is memory per pass, i.e. intrinsic Q.
Ultra-low-loss silicon nitride is class-leading and foundry-accessible ($Q_i$ near $10^7$ on
multi-project-wafer runs [CITE-Cui-2023]), thermally stable enough for the slow thermo-optic
actuation that gradient-estimating training wants, and needs little gain, which keeps injected
amplifier noise low (§3). The cost is SiN's weak $\chi^{(3)}$, which makes the one route that
needs an optical nonlinearity — Hamiltonian-echo learning, whose echo is a phase conjugation —
harder; §4–§5 model it concretely rather than idealize it.

## 1.3 What this paper does

This is a theory-and-simulation (Stage-0) paper. Its thresholds — margins, budgets, fairness
conventions and statistical rules — were frozen in a pre-registration ledger before the runs that
consume them, and the ledger with its commit trail accompanies the paper (§3.7).

1. **A mapping with a realizable region** (§2): the oscillatory-SSM ↔ coupled-SiN-ring
   correspondence, its pole region bounded by measured platform numbers, an actuation map for
   $\{\delta, \kappa_\text{ext}, \mu\}$, and the backscatter doublet carried in the model.
2. **A shared dissipative substrate** (§3): saturating Er gain at a registered operating point,
   Langevin amplifier noise at NF 7 dB, three cells from foundry floor to aspirational, a feasible
   box bounded by the lasing crossing, and a measured four-tap input map after single-drive
   controllability was found to collapse to ≈3 of 32 rings.
3. **A four-method bake-off under one fairness contract** (§4–§5): SPSA, PAT with registered twin
   mismatch, a recurrent in-situ adjoint charged as if realizable, and RHEL over a concrete
   four-wave-mixing echo model, scored by device passes to a pre-registered target, eight seeds.
4. **The result** (§5): both hardware-committed methods, PAT and SPSA, train the recurrence to
   within margin of the exact-gradient reference on all eight seeds, in simulation. PAT needs the
   fewest device passes; RHEL is censored. Against calibrate-offline-then-deploy, in-situ training
   shows no resolved difference at five calibration-error levels spanning 5–30% and no advantage
   under common-mode drift, but holds a **declared, pre-registered 2.42× advantage under
   uncorrelated per-ring drift**, which a global laser re-lock cannot absorb.
5. **Costs and limits** (§6–§8): the damping optimum and a failed prediction about it, a
   function-matched energy envelope that is negative within the registered 0.1–2 GS/s window, and the modelling limits, verification debts and review
   conditions, stated with the same specificity as the results.

The contribution is a simulation test of training the pole positions and couplings that define a
dissipative SiN memory lattice, under registered thresholds and explicit cost accounting. PAT and
SPSA have prior chip demonstrations; the novelty is the specific recurrence of §1.1. A physical
demonstration remains future work.
