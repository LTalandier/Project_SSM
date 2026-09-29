# Can a photonic state-space model be trained on-chip? A pre-registered in-situ-training bake-off on a realistic silicon-nitride ring substrate

*Lucas Talandier — independent researcher, Paris*

Copyright © 2026 Lucas Talandier. Paper: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Accompanying code: MIT.

**Abstract.** To our knowledge, no physical photonic system has yet had the parameters that define a continuous-time dissipative-resonator recurrence — pole positions and inter-resonator couplings, the physics that *is* the memory — trained on the device by gradient-based or gradient-estimating methods.¹ We ask whether such training is feasible for a photonic state-space model on ultra-low-loss silicon nitride, and answer it in simulation: **on a pre-registered dissipative substrate model, both hardware-committed methods, physics-aware training (PAT) and model-free SPSA, train the recurrence to within margin of the exact-gradient reference on 8/8 seeds at realistic noise.** Every threshold was frozen before the run that consumed it.

We derive the SSM↔ring mapping and its realizable pole region, build one shared substrate (finite Q, saturating gain, amplifier noise), and run a four-method bake-off. PAT needs 4.6× fewer device passes than SPSA. Hamiltonian-echo learning is censored: the substrate's own dissipation defeats the echo. One input drive trains ≈3 of 32 rings and four taps recover all 32; the winning routes converge on the same damp-the-driven-rings profile.

Against calibrating offline and deploying, in-situ training shows no resolved advantage at five calibration-error levels spanning 5–30%, after a corrected command-binding rerun, or under common-mode drift. Under uncorrelated per-ring drift it holds a pre-registered 2.42× advantage (a threshold crossing under a frozen rule; the ratio's own CI spans [1.7, 4.6]). Capacity remains a limitation: the deployed equalizer's output rides on 6–8 of 32 rings, and no workload in our data exercises more. A registered inline follow-up finds no energy-advantage window at 0.1–2 GS/s against a per-tap digital equalizer (best digital/photonic ratio 0.64), and total training energy remains unmeasured. A registered prediction that the damping optimum tracks task memory span failed. The pre-registration ledger, substrate model and code are released with the paper.

¹ *The nearest neighbor, an in-situ-trained optical recurrent network, trains interferometer weights around an optoelectronic relay; its resonators stay fixed.*

## 1. Introduction

### 1.1 The gap

Photonic neural networks now train themselves on-chip in feedforward form: model-free
perturbative methods [1, 2], hybrid physical-forward/digital-backward
methods [3], and in-situ adjoint methods that read gradients from interference
[4]. Recurrent photonic processors, whose memory lives in the physics, have barely
received such training. Reservoir computing avoids the problem by fixing the recurrence and
training only a readout [5]. Where internal parameters of a photonic
recurrence have been adjusted, it has been by calibration or regime-tuning rather than
task-driven training [6], by reinforcement-style search over a readout while
the loop stays fixed [7], or with the recurrent state carried digitally between
optical passes [8]. A two-modality literature search with a pre-registered kill
criterion (supplementary N3) found no demonstration, by any method, of the following:

> **a continuous-time dissipative-resonator recurrence — pole positions and inter-resonator
> couplings — trained in situ on the physical device by gradient-based or gradient-estimating
> methods on a computational task.**

Each qualifier is load-bearing. *On a computational task* excludes the servo and calibration
lineage; *physical parameters of the recurrence* excludes hybrid-digital state carriage;
*weight-tied recurrence* excludes feedforward meshes folded in time. The nearest neighbor is the
optical recurrent accelerator of Wu et al. [9]. Its ORNN chip is trained in
situ by a model-free perturbative method (SPGD) on classification, with a weight-tied mesh applied
across wavelength-encoded time steps, which makes it, to our knowledge, the first in-situ-trained
optical recurrent network of any kind. Its trained weights are interferometer-mesh voltages,
however; its recurrent state is regenerated electronically at every step through a
photodetector–modulator relay, and its resonators are calibrated once and held static. The
resonator recurrence itself stays untrained. The other near-misses each fall along one
qualifier: all-photonic on-chip backpropagation for a *feedforward* network [10];
microring weight banks trained in situ as *feedforward* layers [11]; a time-synthetic
fiber-loop network whose per-step parameters are distinct, i.e. unrolled feedforward
[12]; microring weights inside an analog recurrent loop trained by particle-swarm
search, *without gradients* [13]; an optoelectronic delay reservoir whose
recurrence parameters were optimized by Bayesian search *through a digital loop*
[14]; and a silicon photonic reservoir equalizer trained in hardware *in its readout
only* [15]. No coupled-resonator lattice has had its couplings learned on-device by
any method. The claim is time-indexed: the last bounded search ran on 2026-09-13, and the
dated record is in supplementary N3.

### 1.2 Why a state-space model, and why silicon nitride

Deep state-space models showed that *linear* recurrences with well-placed poles carry most of
long-sequence performance [16, 17], and the oscillatory LinOSS line extended this to
second-order units that are exactly coupled damped oscillators [18, 19]. A
lattice of coupled microrings *is* such a system: poles are ring detunings and losses, couplings
are physical couplers, and the LinOSS stability analysis tolerates nonnegative damping, so a
lossy-but-high-Q lattice is in-regime rather than an approximation to a conservative ideal (§2).
Damping becomes a design knob.

The figure of merit for a dissipative ring recurrence is memory per pass, i.e. intrinsic Q.
Ultra-low-loss silicon nitride is class-leading and foundry-accessible ($Q_i$ near $10^7$ on
multi-project-wafer runs [20]), thermally stable enough for the slow thermo-optic
actuation that gradient-estimating training wants, and needs little gain, which keeps injected
amplifier noise low (§3). The cost is SiN's weak $\chi^{(3)}$, which makes the one route that
needs an optical nonlinearity — Hamiltonian-echo learning, whose echo is a phase conjugation —
harder; §4–§5 model it concretely rather than idealize it.

### 1.3 What this paper does

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

## 2. From oscillatory state-space models to coupled SiN microrings

### 2.1 The model class

A structured state-space model (SSM) processes a sequence $u_1, u_2, \dots$ through a linear
recurrence $x_{t+1} = \bar A x_t + \bar B u_t$, $y_t = \mathrm{Re}(\bar C x_t) + D u_t$, whose
expressive power is set by where the eigenvalues (poles) of $\bar A$ can be placed. The diagonal
variants S4D and DSS [17, 21] reduce $\bar A$ to independent complex poles,
$H(s) = \sum_j c_j b_j/(s - \lambda_j) + D$; the oscillatory LinOSS family [18]
parameterizes forced, damped harmonic oscillators, and D-LinOSS [19] makes each mode's
damping trainable. The LinOSS construction holds for any nonnegative-diagonal (dissipative) state
matrix: stability requires only that every mode decay. A substrate that is lossy but slowly so is
therefore in-regime, and its loss is the model's damping parameter. Where the trained optimum
lands in that range is measured in §6.

### 2.2 One ring is one trainable complex pole

The mode amplitude $a_j$ of a silicon-nitride microring obeys temporal coupled-mode theory (Haus
energy-amplitude convention) [22]:

$$\dot a_j = (i\delta_j - \kappa_{\mathrm{tot},j})\,a_j
+ i\sum_{k\neq j}\mu_{jk}\,a_k + \sqrt{2\kappa_{\mathrm{ext},j}}\,u(t),$$

with $\kappa_{\mathrm{tot},j} = \kappa_{i,j} + 2\kappa_{\mathrm{ext},j}$ the amplitude decay rate of
the add–drop ring (intrinsic loss plus two bus ports; the drive enters through one), $\delta_j$ the
detuning and $\mu_{jk}$ the inter-ring coupling. An uncoupled ring is exactly one **complex**
Laplace pole, $s_j = -\kappa_{\mathrm{tot},j} + i\,\delta_j$, complex because the optical envelope
carries a carrier. A bank of $N$ rings therefore realizes a diagonal complex-pole SSM of the
S4D/DSS class, with injection and readout couplings as the residues $c_j b_j$. LinOSS is recovered
as the uncoupled, real-input special case, a conjugate pole pair: against its eigenvalue
$a_i = -e^{\alpha_i} + i\beta_i$,

$$e^{\alpha_i} = \kappa_\mathrm{tot}, \qquad \beta_i = \delta,$$

and storing $\alpha_i = \log\kappa_\mathrm{tot}$ enforces dissipation by construction. We claim
the broader class. Published LinOSS/D-LinOSS benchmarks validate only the $\mu = 0$ diagonal
reduction, so performance of the coupled realization is measured in-house against a
BPTT-on-substrate reference (§5.1), not assumed.

Discretization is exact: for piecewise-constant input the zero-order-hold (van Loan) step gives
$z = e^{s\,dt}$ with $dt$ the round-trip time, and per-step retention
$|z| = e^{-\kappa_\mathrm{tot} dt}$. The mapping passes three pre-specified internal checks: pole
identity, the continuous-wave limit (static transfer error $O(1/\mathcal{F})$, $4.5\times10^{-4}$
at finesse $\mathcal{F} = 1048$), and an independent RK45 time-domain integration (N9.1). These
certify that the simulator computes its model, not that the model captures a fabricated device
(§8.1).

### 2.3 Coupling rings

Energy-conserving inter-ring coupling adds $i\Omega$ with $\Omega$ real-symmetric. It hybridizes
the poles while conserving total damping,
$\sum_j \mathrm{Re}\,\lambda_j = -\sum_j \kappa_{\mathrm{tot},j}$ (verified: the two-ring beat
matches the $2\mu$ eigenvalue splitting to $<2\%$). The trainable $\mu_{jk}$ reshape frequencies
but cannot buy stability or memory; they matter for the claim because inter-ring couplings are
recurrence-defining (§2.5).

### 2.4 The realizable pole region

Four boundaries define the envelope (Fig. F1). **Memory is loss-limited.** Passive rings satisfy
$\kappa_\mathrm{tot} \geq \kappa_i = \omega_0/(2Q_i)$, so the maximum amplitude memory
$1/\kappa_i = 2Q_i/\omega_0$ runs from **3.29 ns (329 round trips)** at $Q_i = 2\times10^6$ to
**49.4 ns (4937 round trips)** at $Q_i = 3\times10^7$. Net gain pushes $|z|$ toward 1 at the cost
of saturation and amplified spontaneous emission (§3). **Frequency is FSR-bounded:**
$|\beta_j\,dt| \leq \pi$ with $dt = 1/\mathrm{FSR}$. **Readout trades against memory.** The external
coupling sets memory and on-resonance drop efficiency $(2\kappa_\mathrm{ext}/\kappa_\mathrm{tot})^2$
in opposite directions: at the foundry corner, from 274 round trips at efficiency 0.028
($\kappa_\mathrm{ext} = 0.1\kappa_i$) to 16 round trips at 0.91 ($10\kappa_i$). Because
$\kappa_\mathrm{ext}$ is itself a pole-real-part actuator, training it folds this trade into the
recurrence training. **Backscatter bounds the one-ring-one-pole picture.** Sidewall roughness
couples the counter-propagating modes at a fabrication-set rate $\gamma$, and the resonance splits
into a doublet when $2\gamma \gtrsim \kappa_\mathrm{tot}$ [23]. Since $\kappa_i$
falls as $Q_i$ rises while $\gamma$ does not, splitting grows with $Q$: a clean damascene-class
process ($\gamma/2\pi \approx 12$ MHz [24]) keeps single poles at the foundry corner
and splits near $Q \approx 4\times10^6$, while a rough subtractive process splits 21–75% of
resonances already at $Q_i \lesssim 2.7\times10^6$ [25]. The substrate therefore
carries the doublet explicitly (§3.4). Crossover conventions and their sources are in N9.1.

### 2.5 What training the recurrence in situ means physically

The recurrence is defined by $M = \mathrm{diag}(-\kappa_{\mathrm{tot},j} + i\delta_j) + i\Omega$,
and every entry has an addressable actuator:

| Pole quantity | Physical knob | Actuator | Cost |
|---|---|---|---|
| $\mathrm{Im}$ (frequency) $\delta_j$ | ring resonance offset | thermo-optic heater (trench-isolated), one per ring | low: 1 heater + DAC channel/ring |
| $\mathrm{Re}$ (damping) $\kappa_{\mathrm{tot},j}$ | bus–ring coupling $\kappa_{\mathrm{ext},j}$ | tunable coupler (MZI-assisted gap) | medium: 1–2 heaters/ring |
| same, past the passive floor | per-ring net gain $g_j$ | Er:SiN / III–V pump current | high (gain stage + ASE cost); not required for the claim |
| off-diagonal $\mu_{jk}$ | ring–ring coupling | tunable photonic-molecule coupler (or bus-mediated mesh) | medium–high; topology fixed at fab, strengths trainable |
| residues $B, C$ | injection/readout mesh | thermo-optic MZI mesh | **not recurrence-defining** |

The last row is the load-bearing exclusion. Training only the residues while the poles stay fixed
is reservoir computing with a trained head, including reinforcement-learning-tuned readouts
[7]. A method earns the in-situ-training claim only if it updates
$\{\delta_j,\ \kappa_{\mathrm{tot},j},\ \mu_{jk}\}$ on the device (PR-2, PR-6), and every method in
the bake-off trains that same set. The set is gain-free and all-thermo-optic, heaters and tunable
couplers only, which suits perturbative training on SiN.

## 3. A pre-registered dissipative substrate

### 3.1 Why one shared substrate

The bake-off's conclusions are comparisons, so all four training routes run on a *single*
simulated substrate — one dynamical model, noise model, parameter partition, initialization and
data convention (PR-6) — frozen before any estimator existed. The model is the 2N-mode
coupled-mode lattice of §2: N rings, each a clockwise/counter-clockwise doublet, read by direct
detection $y(n) = |\sum_j c_j a_j(n)|^2$, the only nonlinearity besides gain saturation. The
trainable partition (PR-2) is the per-ring detunings $\delta_j$, per-ring bus couplings
$\kappa_{\text{ext},j}$ and nearest-neighbor couplings $\mu_{j,j+1}$. A digital head (an 8-lag
linear FIR on $y$) and a fixed affine intensity encoder bracket the photonic core; both are
identical across methods.

### 3.2 Loss, gain, and noise

The per-ring net decay is $\kappa_{\text{net},j} = \kappa_i - g_j + 2\kappa_{\text{ext},j}$. Gain
follows a static-saturated class (M1): a per-episode operating point $g(\bar P) =
g_0/(1+\bar P/P_\text{sat})$, differentiable in the drive statistics and in $\kappa_\text{ext}$,
fixed within a rollout. Its validity conditions are registered (stationary within-episode drive,
pinned train/test power statistics, quasi-static margin $E_\text{sym}/E_\text{sat} \sim
10^{-6}$–$10^{-5}$); bursty inputs would void it. Every gain-bearing cell runs at
$g_\text{rt} = 0.9\times$ the intrinsic round-trip loss, so gain never compensates port loading and
$\kappa_\text{net} = 0.1\kappa_i + 2\kappa_\text{ext}$ at the operating point; the passive floor is
a sensitivity row. Amplified spontaneous emission enters as a Langevin term
$\langle FF^*\rangle = 2\kappa_g n_\text{sp}\,\delta(t{-}t')$, discretized exactly with the
propagator, with **fresh draws on every physical pass**, never shared between passes, methods or
directions. The noise figure is **NF = 7.0 dB** ($n_\text{sp}=2.5$), frozen to match the measured
value for the flagship Er:Si₃N₄ amplifier, "ca. 7 dB … limited by coupling losses" [26].
That is a system NF, not an isolated intrinsic one, so NF ∈ {3, 5} remain sensitivity values.

### 3.3 The three cells

| cell | platform class | $Q_i$ | N | role |
|---|---|---|---|---|
| C-1 | foundry floor (P-FND) | $2\times10^6$ | 8 | Gate-ii gating cell |
| **C-2** | demonstrated MPW class (P-AN800) | $6.8\times10^6$ | **32** | **bake-off headline** |
| C-3 | aspirational (P-UHQ) | $3\times10^7$ | 128 | labelled sweep axis; never gates |

C-2 is a conservative bound on a demonstrated multi-project-wafer result (3.3 dB/m, mean
$Q_i \approx 10.8$M [20], independently assessed in [27]): our
5.1 dB/m and $Q_i = 6.8\times10^6$ are worse than the broadest-linewidth device in that paper's
249-resonance distribution. The residual risk is geometry transfer, since the demonstrated loss
comes from a wide multimode racetrack and our ring is single-mode; a registered ×2-loss derate row
prices it. At the operating point C-2 holds ~32 samples of memory at 2 GS/s, and C-1 holds ~9.4,
covering the task's 7-tap span at the operating point and marginal only at its passive floor.

### 3.4 Backscatter and the doublet

Roughness couples the clockwise and counter-clockwise modes at $\gamma$ = 11.8 MHz at C-2
(damascene-clean class) and 90 MHz at C-1. At the C-2 initialization $2\gamma/\kappa_\text{net}
\approx 2.4$, so the doublet is resolved, and the substrate is always the full $2N$-mode lattice
rather than an $N$-mode idealization. This mattered: calibration measured the drive build-up at
the lasing floor at ×0.42 of the hold value, the doublet and chain hybridization quenching the
single-pole build-up that two earlier estimates (×37 and ×91) had assumed.

### 3.5 The feasible box and the drive budget

The trainable couplings live in a registered box $r_j = \kappa_{\text{ext},j}/\kappa_i \in
[0.1, 3]$. With saturating gain, a ring below $r^* \approx 0.134$ crosses threshold and the linear
rollout diverges, so the training clamp is the measured $\mathbf{r_\text{min} = 0.1606}$ (crossing
plus registered margins); the initialization is $r_0 = 0.3$. Damping in the D-LinOSS sense is not
a frozen cell: it is the trainable per-ring net loss explored through $\kappa_\text{ext}$ at fixed
$g_\text{rt}$ (§6). Drive is normalized by an intracavity-energy budget: the registered
$\bar P_0 = 1$ mW bus drive corresponds to $E_0 = 1.069\times10^8$ intracavity photons at the
initialization θ₀, held fixed across methods and across the in-situ/offline comparison so that the
encoder cannot buy SNR.

### 3.6 The measured input map

A single bus port cannot train a 32-ring chain: with drive on ring 1, the per-ring gradient
collapses with hop distance, leaving an effective participating dimension of ≈3 of 32 rings. A
pre-registered every-ring gate — each ring's gradient $\ge 10^{-3}$ of the maximum, minimum over
five drive seeds — resolved the minimal map **B = taps {3, 12, 21, 30}** at $K=4$ (32/32 rings
pass, worst $1.42\times10^{-3}$; no three-tap set passes). The four drive channels are charged to
the systems envelope (§7). One anchor risk (vii) stays open: the clamp is calibrated on-resonance,
and under a worst-case de-saturation hypothetical a detuned ring at $r_\text{min}$ reaches
$\kappa_\text{net} = -0.48\kappa_i$; a δ-aware clamp would sit at $r \approx 0.2547$. An endpoint
diagnostic (PR-18) found three of eight SPSA solutions with at least one ring in that hypothetical
super-threshold corner and none of PAT's. The as-built substrate never lases, and every exposed
ring sits below the δ-aware clamp, which Stage 1 therefore inherits (N9.2).

### 3.7 The ledger as method

Every choice above — the gain class and its validity conditions, the NF axis, the cells, the box,
the clamp, the input map, the drive budget — was written into a pre-registration ledger before the
run that consumed it, in most cases signed by the PI, with measured quantities ($E_0$,
$r_\text{min}$, the input map, the budget, the reference) returned as dated addenda. Superseded
text is retained. The ledger and the registration-to-run commit table accompany the paper
(supplementary N1, N4). A bake-off whose thresholds were set after seeing results would not
support the claims of §5.

## 4. Four routes to on-chip gradients

### 4.1 What counts as a physical gradient

The fairness contract (PR-6) fixes one invariant: **a training method may obtain gradient
information only from simulated device passes on the shared substrate, with fresh noise on every
pass.** Automatic differentiation through the substrate is reserved for the BPTT reference, never
a contestant. Per seed, all methods share the initialization (detunings spread over
$[-\kappa_i, \kappa_i]$, $r_0 = 0.3$, connected chain $\mu_c = 0.3\kappa_i$), the data stream, the
head cadence, the clamp and the pre-registered hyperparameters. Cost is counted in **physical
device passes, any direction** (PR-7), one pass being one sequence through the substrate. Digital
compute sits on a side-ledger that is always co-reported and never folded into the rank: saving
device passes by spending digital FLOPs is a real but different advantage from needing no model.

### 4.2 SPSA — model-free, two passes

Simultaneous-perturbation stochastic approximation [1] perturbs the whole partition by
$\pm c\Delta$ (a random sign vector) and measures the loss twice: **2 device passes per update**,
no model, no twin, no hardware beyond the plant's own actuators and readout (supplementary N2).
Perturbations at the clamp boundary are one-sided. SPSA is chip-demonstrated
[2] and was crosstalk-robust in our prior thermo-optic work
[28]; its gradient variance, growing with parameter count, is what the
sample-efficiency metric prices.

### 4.3 PAT — physical forward, twin backward

Physics-aware training [3] evaluates the loss on the *measured* output and takes
the gradient through a differentiable digital twin at the commanded parameters: **1 device pass
per update**, plus a twin forward and backward on the digital ledger. Its honesty depends on the
twin being imperfect in a registered way (PR-5). **M-par** applies 5%-class parametric errors
($\kappa_i{+}5\%$, $\gamma{+}5\%$, actuation ×1.05/×0.95, detuning offset $0.05\kappa_i$, gain
pair ×1.10/×0.75). **M-struct** drops the gain's dependence on the trained coupling, the one
channel a fixed-gain model cannot see. **M-noise**, always on, makes the twin noiseless. The
headline PAT carries the composed mismatch; §5.6 decomposes it. With mismatch off, PAT's gradient
equals BPTT's to machine precision.

### 4.4 Recurrent in-situ adjoint — a physical reverse pass, by hypothesis

The adjoint route extends feedforward in-situ backpropagation [4] to the cavity:
the error field propagates backward through the same dissipative substrate, and the gradient is
read from forward/adjoint interference. No recurrent photonic demonstration of this pass exists
(verification debt #4). The simulation charges it **as if realizable** — 1 forward + 1 adjoint =
**2 device passes per update**, zero digital — and leaves realizability to the hardware ledger
(circulators, phase-coherent injection, separating the counter-propagating field from the
backscatter doublet). The simulated reverse pass carries fresh noise, and the saturating gain is
frozen at its operating-point value. On the fixed-gain plane the adjoint gradient equals BPTT to
machine precision; in saturating mode the frozen-gain approximation costs 0.6% of gradient
direction at C-1 but **7.5% at C-2**. It omits a noise term on the adjoint field itself, which awaits an unresolved error-launch
power convention. These simplifications flatter the adjoint, so its arm is an **optimistic bound**
wherever it appears.

### 4.5 RHEL — Hamiltonian echoes on a substrate that forgets

Recurrent Hamiltonian echo learning [29, 30] trains by time
reversal: evolve forward, apply one conjugation to the state snapshot (for optical fields, phase
conjugation), evolve again through the same physics with the input replayed time-reversed and a
small error nudge, and take the symmetric finite difference of $\nabla_\theta H$ between a
$+\varepsilon$ and a $-\varepsilon$ echo. Taking the published algorithm seriously on a
dissipative substrate has three registered consequences: **4 device passes per update**
operationally (3 in the Hamiltonian limit, but the echo does not return a reusable state and
state cloning is unphysical; PR-7.1); the conjugation fires **twice per update**; and the update
reads only the coherent generator, so the dissipative channel of $\kappa_\text{ext}$ is invisible
to it.

The echo is modelled concretely (PR-11): a $\chi^{(3)}$ four-wave-mixing conjugation stage whose
extraction, spiral-conversion and timing penalties total **−22.4 dB per conjugation** (Fig. S3; N9.3),
plus the parametric quantum floor, at $\gamma_\text{nl} \approx 0.97\,\text{W}^{-1}\text{m}^{-1}$
[31]. Published ultra-low-loss demonstrations reach 0.29–0.51 W⁻¹m⁻¹, so the chain is
optimistic for RHEL by ~6 dB. Conjugating N spectrally overlapping rings needs N pumped arms,
**≈9.6 W of on-chip pump at the headline cell**, charged to the envelope. Implementation
invariants — independent forward and echo noise, no loss-sign flip, fresh amplifier noise in the
echo — are test-enforced, and as dissipation is removed the implemented gradient converges to the
exact reference (cosine $\to 1.0000$; Fig. S5).

### 4.6 The guardrail

The four routes are *parallel in simulation, singular in hardware*: a Stage-1 chip is committed to
the two chip-demonstrated workhorses, PAT and SPSA, whatever the ranking, and an exact-gradient
route can earn a later hardware slot only by clearly beating both on a pre-registered outcome
(PR-9).

## 5. The bake-off: which routes train the recurrence, and at what cost

### 5.1 Pre-registration and the reference

Every threshold in this section was fixed in the ledger before the run it judges: the fairness
contract, cost metric and mismatch families (PR-6/7/5), then the target rule, statistical plan and
gate semantics (PR-3/8/9), then the measured budget and reference as dated addenda committed before
any contestant ran (supplementary N4). The central claim is a threshold-crossing claim, and a
threshold chosen after seeing the curve would be worthless.

The reference is backpropagation through time on the substrate itself (BPTT). It is not a physical
method, since it reads gradients the device cannot expose; it is the strongest gradient access the
model admits, and a budget-scoped reference rather than a capacity ceiling. On the headline cell
(C-2: 32 rings, $Q_i = 6.8\times10^6$; 4-PAM channel equalization at 28 dB), BPTT reaches a median
symbol-error rate (SER) of $5.2\times10^{-4}$ over eight seeds; seven sit at $5\times10^{-4}$, two
errors in 3,840 evaluated symbols, which is the quantization floor. That floor can manufacture or
erase differences between near-ceiling arms, so every such comparison (§5.5, §5.6) is re-scored
under a pre-registered fine protocol (**eval-F**, PR-17: 99,840 symbols, per-seed resolution
$1.0\times10^{-5}$). The coarse protocol stays the protocol of record for every gate, target and
ranking, and both are reported where they differ. At eval-F the reference reads
$9.8\times10^{-4}$. It is protocol-local: the §5.5 follow-ups train for 31,600 updates rather than
12,000, and their matched-budget BPTT reference, $8.1\times10^{-4}$, is the line drawn in Fig. F8
(N9.4; the one eval-F implementation erratum is audited in N7).

A method *reaches target* if its held-out SER falls to $\text{SER}_\text{target} =
1.25\times\text{reference} + 0.005 = 5.65\times10^{-3}$ within the budget $B = 252{,}800$ device
passes, twice BPTT's convergence point in a sizing pilot excluded from the scored seeds. Using the
eval-F reference would give $6.23\times10^{-3}$ and change no verdict. The reference is identical
under fixed and saturating gain ($\Delta_{M3}=0$), so the gain-model class, the substrate's largest
modelling uncertainty, cannot flip any ranking below, and the registered M3 sensitivity trigger
cannot fire at this cell. **The frozen substrate has headroom for the
task; the open question is which physical training routes reach it, and at what cost.**

### 5.2 Gate ii: the recurrence trains on the device

Two parts were pre-registered (PR-9). **Capacity (ii-a):** the reference must clear half the
readout-only error. The reservoir baseline, which freezes the recurrence and trains only the
digital head, stalls at $2.2\times10^{-2}$, putting the floor at $1.1\times10^{-2}$; the reference
clears it by $21\times$ at the coarse protocol and $11\times$ at eval-F. **Trainability (ii-b):**
PAT or SPSA must reach target on at least five of eight seeds.

**Both reach target on all eight.** The parameters that define the recurrence —
$\{\delta_j, \kappa_{\text{ext},j}, \mu_{jk}\}$ — are trained on the simulated physical substrate,
through physical-operation-only gradient methods with fresh noise on every pass, to within the
pre-registered margin of exact gradients. To our knowledge this is the first demonstration — **in
simulation, on a pre-registered realistic substrate model** — of a continuous-time
dissipative-resonator recurrence whose poles and couplings are updated by device-protocol
gradient-based or gradient-estimating training [32]. The on-chip counterpart
does not exist yet, and every use of "demonstration" in this paper carries this qualifier.

### 5.3 The ranking: sample efficiency at matched device-pass cost

Routes are ranked by success fraction, then median device passes to target (PR-8), with the
digital side-ledger co-reported but never folded in. Priced in joules, the two component ledgers
reverse the PAT–SPSA order (§7.3), although no total training energy is established; this is why
neither metric is presented as the truth.

| route | success | median device passes → target | final SER (median) | digital ledger (at budget $B$) |
|---|---|---|---|---|
| **PAT** (twin-backward) | 8/8 | **38,400** | $8\times10^{-4}$ | 505,600 |
| **adjoint**† (physical reverse pass) | 8/8 | 73,600 | $5\times10^{-4}$ | 0 |
| **SPSA** (model-free) | 8/8 | 176,000 | $1.3\times10^{-3}$ | 0 |
| **RHEL**‡ (Hamiltonian echo) | 0/8 | censored at $B$ | $1.4\times10^{-1}$ | 0 |

† *Charged as if realizable; no recurrent physical reverse pass has been demonstrated (debt #4,
§8.2), so this row is an optimistic bound.* ‡ *A measured feasibility bound, not a competitive
entry (§5.4).*

All three ordered pairs among the passing routes separate with paired-by-seed bootstrap 95%
confidence intervals excluding zero: PAT−SPSA $=-137{,}600$ passes, CI $[-155{,}200,-123{,}200]$;
adjoint−PAT $=+35{,}200$, CI $[+35{,}200,+36{,}800]$; adjoint−SPSA $=-102{,}400$, CI
$[-120{,}000,-88{,}000]$. The adjoint−PAT interval is degenerate because passes-to-target lives on
a 1,600-pass evaluation grid and all eight paired differences fall within two grid steps, positive
on every seed; it is a sign-consistent separation, not a distributional interval (N9.4). **PAT** is
cheapest on the device but pays digitally, 505,600 twin passes over the full budget, and carries
the burden of characterizing a differentiable twin. **The adjoint** reaches ceiling-grade accuracy
at zero digital cost and $1.9\times$ PAT's device passes, as if realizable. **SPSA** costs
$4.6\times$ PAT's device passes but needs no model, twin or added hardware. No route earns
promotion (PR-9): the adjoint beats SPSA but loses to PAT, and promotion requires beating both. The
hardware roadmap stays on PAT and SPSA.

### 5.4 RHEL: a feasibility bound on echo learning in dissipative substrates

RHEL is best read as a measured feasibility bound, and its outcome was foreseeable in direction:
the theorem behind the echo assumes a non-dissipative system, and the headline operating point sits
at $\kappa_\text{net} T\, dt \approx 8$ (≈27 at C-1), one to two orders beyond the $\lesssim 0.1$
regime where our recovery curve shows the update aligning with the true gradient (Fig. S5). What
the bake-off adds is the quantified boundary, measured under the same fairness contract as the
routes that pass.

RHEL reaches target on no seed. Its final SER, $0.14$, is *worse than the readout-only baseline*
(a $+0.118$ readout differential). Two controls locate the cause. As the substrate is made less
dissipative, the RHEL gradient converges to the exact reference (cosine $\to 1.0000$), so the
estimator is correct. An idealized-conjugator control at C-1, a *perfect* echo, formally reaches
the C-1 target ($5.7\times10^{-3} \le 7.3\times10^{-3}$ coarse; $7.2\times10^{-3}$ at eval-F) but
converges to the head-only level: the recorded diagnosis is that even a perfect echo's
recurrence contribution is ≈0 here, and
the digital head does the passing. The conjugation chain is therefore second-order. The failure
is dissipative-echo bias: an echo that assumes time reversal, on a substrate whose 256-sample
sequence spans ≈8 memory lifetimes (memory ≈32 samples at C-2). Silicon nitride's low loss helps
RHEL's noise budget, but the dissipation the recurrence itself requires defeats the echo at this
operating point.

### 5.5 The comparison the fair design was built to expose

The decisive baseline is offline-train-then-deploy: train the full parameter set digitally on a
designer's model, deploy through actuation maps, and recalibrate only the digital head on-device.
It receives the *same* 5%-class calibration errors as PAT's twin, drawn from one frozen family
(PR-5), so it cannot be a secretly weaker competitor. It reaches $1.0\times10^{-3}$ against PAT's
$8\times10^{-4}$ at the coarse protocol, a one-to-two-symbol gap that the coarse floor scores as formally
real; at eval-F the two show no resolved difference. **At 5% calibration accuracy on this task, we resolve no performance benefit
for in-situ training over calibrate-then-deploy.** This neither establishes equivalence nor rules
out smaller benefits. Two pre-registered follow-ups (PR-5 §E, PR-16) then asked where an advantage
appears.

**Calibration sweep: no resolved difference through the 30%-class point (Fig. F8a).** The original
sweep's command binding failed to scale three of PAT's five mismatch terms. Its higher-mismatch
comparisons were withdrawn, the code corrected, and a bounded correction rerun registered before
execution (S0.13; supplementary N8). The rerun is post-result bug repair, not a newly blinded
experiment; the thresholds and bootstrap rule were not changed. At eval-F all five paired
intervals include zero:

| mismatch class | PAT median SER ×10⁻³ | offline median SER ×10⁻³ | offline/PAT | paired 95% CI of (offline−PAT) ×10⁻³ |
|---|---:|---:|---:|---|
| 5% | 0.851 | 0.896 | 1.053 | [-0.050, 0.100] |
| 10% | 0.861 | 0.891 | 1.035 | [-0.060, 0.120] |
| 15% | 0.861 | 0.866 | 1.006 | [-0.045, 0.080] |
| 20% | 0.861 | 0.881 | 1.023 | [-0.045, 0.100] |
| 30% | 0.881 | 0.876 | 0.994 | [-0.090, 0.070] |

No level clears the frozen advantage rule (ratio ≥2 and difference-CI lower bound >0). These data resolve no difference at the tested
levels; they do not establish statistical equivalence. The coarse protocol, reported because it
differs, gives ratios of 1.33–1.50 with positive difference intervals at 5–20% and one touching
zero at 30%; none reaches 2×. The m=1 bake-off and the drift experiment
are unaffected by the binding defect.

**Drift is the axis — specifically the part a re-lock cannot catch** (Fig. F8b,c). After
convergence, the ring detunings random-walk at a rate calibrated to a measured free-running SiN
resonance drift ($\approx 341$ MHz over 24 h $\approx 24\,\kappa_i$ at C-2 [33]). The
offline arm recalibrates the head and re-locks the laser, a single global detuning re-centering and
the strongest response available without per-ring observability; the in-situ arm retrains the
recurrence. Under **common-mode** drift the re-lock keeps offline in pace ($0.98$ vs
$0.73\times10^{-3}$ time-integrated; ratio $1.34$, CI including zero). Under **independent**
per-ring drift the re-lock cannot correct the scattered poles, and in-situ retraining pulls ahead:
$0.82\times10^{-3}$ versus $1.98\times10^{-3}$. The frozen rule (PR-16, ratified before any drift
run and re-applied verbatim at eval-F) declares an advantage iff the offline median is
$\ge 2\times$ the in-situ median **and** the paired-by-seed 95% CI of the difference excludes zero.
**Both hold (ratio $2.42$; difference CI $[+0.71, +2.84]\times10^{-3}$): this is the one comparison
in which in-situ training formally beats the strong offline baseline.** The rule does not
guarantee the ratio itself: its bootstrap CI is $[1.7, 4.6]$, below 2 in 17% of resamples, so the
advantage is a threshold crossing under a rule frozen in advance, not a 95%-confidence claim that
the true ratio exceeds 2. At the coarse floor the same comparison read $1.84\times$, below the bar.
Coarse and fine protocols score the same bit-identical trajectories, the coarse set is a strict
subsample of the fine one, and the fine protocol was registered while the coarse estimate was on
record (N9.5). The gap grows with accumulated drift, to ~3–4× at the largest step. Its relevance to
hardware depends on how uncorrelated real on-chip drift is, which has not been measured for this
architecture.

### 5.6 What the diagnostics add

At C-1 (three seeds, eval-F; Fig. S2), PAT with a perfect twin and PAT with the structural-omission
twin are indistinguishable (medians $1.11\times10^{-3}$, per-seed within $2\times10^{-5}$), while
the fine floor resolves a small M-par excess ($1.31\times10^{-3}$, +18%, positive on all three
seeds, a consistent sign rather than an interval at $n=3$). PAT absorbs the structural omission
completely and the parametric family almost completely at this cell. This does **not** extrapolate
to C-2, where the dropped gain channel carries ~8% of the gradient direction (the adjoint's cosine
falls from 0.994 at C-1 to 0.925 at C-2); the C-2 mismatch decomposition has not been measured. The idealized-RHEL row is §5.4's control. The registered
bias/variance decomposition of each gradient (PR-14) was not run; it is secondary by design,
because gradient-direction agreement flatters exact methods and penalizes SPSA, whose averaged
trajectory converges although single steps align poorly.

### 5.7 Controllability: what "N = 32" actually means

Under a single input tap the per-ring gradient collapses geometrically with distance from the drive
— ring 32 sits some twenty-five orders of magnitude below the maximum — and the settled
participation profile counts only $\{1, 3, 5\}$ of 32 rings above $\{10^{-1}, 10^{-2}, 10^{-3}\}$
(Fig. F3). A 32-ring lattice driven at one port is effectively a three-ring computer, a property of
chain physics rather than of any training method. The resolved four-tap map (§3.6) raises the
counts to $\{4, 26, 32\}$, and every "$N = 32$" in this paper carries that measured profile. The
readout-only baseline of §5.2 runs under the same four-tap map; its stall reflects untrained poles,
not drive coverage.

The map's guarantee holds at initialization only, so a pre-registered diagnostic (PR-18)
reproduced the converged solutions bit-identically and re-ran the gate there. PAT clears 32/32 on
every seed (worst $1.7\times10^{-3}$) and SPSA a median 30.5/32 (range 29–32). Both winning routes
converge, on every seed, to the same actuator structure: the four driven rings damped to
$r \approx 1.3$ and the undriven rings left at their initialization (median $r \approx 0.30$),
damping where the input lands without severing gradient transport. A uniform pin at the §6 optimum
($r^* = 2.0$) instead leaves only 20 of 32 rings above the gate (N9.6).

Two registered follow-ups bound what this means (PR-18). *Output* participation is narrower
than gradient reach: zeroing readouts in order of contribution with the decoder frozen, the
solutions stay within 2× of their own floor until ~24–26 of 32 readouts are gone, so the delivered
function rides on $N_\text{eff} \approx$ **6–8 rings** (median 6 for PAT, 7 for SPSA), a number
§7.2 must carry. And the interior's contribution is real but thin: a taps-only control, with only
the four driven rings trainable, reaches within 12% of the full partition at eval-F, and the full
partition wins by a paired CI of $[+0.25, +1.55]\times10^{-4}$ excluding zero, the pre-registered
"discovers" reading by a modest margin. The coarse floor inverts this ordering, a second
illustration of the hazard in §5.1.

## 6. Choosing the damping operating point

The D-LinOSS observation that damping in an oscillatory SSM is a *performance knob* has a direct
physical meaning here: per-ring damping is the net loss $\kappa_\text{net}(\kappa_\text{ext})$,
set by a coupler already in the trained partition. The registered disposition (R-ii) therefore
asks whether training *finds* the right damping inside the feasible box. Two arms, six damping
points and eight seeds each were run at the headline cell under convergence control.

**The damping value matters enormously.** With $\kappa_\text{ext}$ *pinned*, so that only
detunings and inter-ring couplings train, the converged error spans a factor of ~300 across the
box: SER 0.39 at light damping ($r = 0.2$; chance on 4-PAM is 0.75) down to $1.3\times10^{-3}$ at
**deep overcoupling**, $r^* = 2.0$ (measured $\kappa_\text{net} = 3.7\kappa_i$ at the converged
solutions, about 6 samples of memory at 2 GS/s). The task needs only a 7-tap span, and the 30–45
samples of memory supplied at light damping are harmful because stale symbols interfere. Damping
tunes memory to the task class, with the optimum on the heavily damped side.

**Training absorbs the knob.** When the full partition trains inside progressively wider boxes
$[r_\text{min}, r_\text{hi}]$, every box containing the pinned optimum reaches $5\times10^{-4}$, the
§5 reference, *better* than the best uniform pin; boxes that exclude the good regime fail. R-ii is
confirmed: the designer must make the box contain the good regime, and the trained substrate sets
the operating point. The mechanism is controllability at the solutions (PR-18; §5.7). The uniform
pin leaves the three inter-tap interior segments gradient-dark, with only 20 of 32 rings above the
gate. The boxed winner damps the four driven rings hard ($r \approx 1.3$) and holds the 28 undriven
rings light ($r \approx 0.7$), keeping 30 of 32 rings trainable. Heterogeneous damping buys
task-optimal damping and trainability at once, which no uniform design value can express.

Two qualifications. The slow mid-grid configurations ($r = 0.3$–$0.5$) had not fully plateaued,
so the ×300 spread is budget-bounded, although both endpoints and every winning configuration
converged and the verdict uses converged points only. And much of what in-situ training does in §5
is finding this operating point: the θ₀ hold value, pinned, yields 0.038, seventy-seven times
worse than the trained substrate. The offline baseline finds $r^*$ on its calibrated model just as
well, so this strengthens the trainability result without moving the advantage question. The
optimum also sits far from the weakly damped corner where the LinOSS parameterization is most
distinctive, so on this task class the results are evidence about the broader dissipative
diagonal-SSM class claimed in §2.2, not about LinOSS-specific expressivity.

**Does the optimum track task memory? A registered prediction, failed.** Because "excess memory is
harmful" on one 7-tap task is close to tautological, we froze a transfer test (PR-17): task T-A-L
adds a −6 dB replica of the channel's past-tap profile delayed by 7 symbols, doubling the memory
span to 14, with the prediction that the optimum moves to lighter damping ($r^*_L < 2.0$) under a
30%-separation rule. **The prediction failed.** The error keeps falling to the heavy edge of the
grid ($2.2\times10^{-3}$ at $r = 3$ vs $2.5\times10^{-3}$ at $r = 2$, eval-F, within 13%; Fig. F6,
dashed); the harder task raised the floor everywhere and left the optimum in place. On this
substrate the heavy-damping optimum is robust to a ×2 change in memory span, set by the
bandwidth/interference trade of the equalization family rather than by span matching. A second
probe (PR-19), a spread-spectrum task whose decisions integrate 31 chips, predicted
$r^*_D \leq 1.0$ and **failed by degeneracy**: at the frozen SNR every grid point reached zero
error, so the separation rule could not fire, and every arm ended near its initialization. The
damping-tracks-memory hypothesis therefore has one informative null and one degenerate attempt
against it; we leave it as a hypothesis that one probe declined to confirm and a second could not
reach (N9.6).

## 7. Does it pay? The systems envelope

### 7.1 The question, and its exclusions

A photonic SSM matters only if, after paying the conversion toll — DAC and modulator in,
photodiode and ADC out, heaters held throughout — it still beats a competent digital
implementation on the axis the niche cares about. We priced this at two frozen corners (OPT = best
published device class; CONS = named vendor parts at ENOB-at-speed, never nominal bits) against
named baselines (Microsoft Brainwave's author-stated batch-1 streaming efficiency, a coherent-DSP
ASIC class, Jetson AGX Orin), with every number traced to a frozen source row. Five known costs
are excluded: laser wall-plug, the substrate's Er:Si₃N₄ gain pump, locking, control compute and
packaging. They only shrink positive cells, so negative findings are robust to them. A
primary-source retrieval puts the integrated-class stack at 0.5–1 W, the same order as the budgeted
N = 128 photonic power (~0.9 W at 2 GS/s), and the erbium pump adds 26–550 mW at N = 32 (derived;
N9.7). A benchtop realization, with 40–100 W of laser and instrument lock, would erase any niche,
so every positive statement below carries an integrated-realization condition.

### 7.2 Inference: the original block-level envelope

The original envelope suggested a conditional low-latency niche: up to ~15× lower energy per
sample than the strongest streaming baseline (Brainwave) at N = 128 and 2 GS/s, with an optical
latency lower bound of tens of nanoseconds per sample against the baseline's reported
milliseconds. That was an estimate, not a measured end-to-end advantage, and it required three
conditions at once: line rates ≳0.5 GS/s (every scenario loses at 0.1 GS/s), N ≳ 32, and suspended
low-power heaters (~1 mW/π, class B). Under the registered worst-case holding convention,
foundry-standard heaters lose to every baseline everywhere in the window at the deployable corner.
Measurement has since undercut the N condition: the deployed equalizer's output rides on
$N_\text{eff} \approx 6$–$8$ of 32 rings (§5.7), so a baseline built to the *function* would carry
~6–8 states. The ~15× was computed against a baseline priced at nominal N, and a baseline built
to the function would shrink by a comparable factor. **The advantage is therefore unmeasured
in magnitude, not merely conditional.** Restoring it needs a workload that exercises N ≳ 32 states
on this substrate, and no such workload exists in our data; the registered long-memory follow-up
(PR-19) could not measure concentration at its degenerate operating point (N9.7). Jetson's peak
rating is never beaten anywhere; the comparison rests on sustained batch-1 behavior, which for
recurrent workloads on edge GPUs is documented at more than 100× below claimed peak
[34]. The function-matched follow-up of §7.4 supersedes this block-level reading.

### 7.3 Training: partial energy budgets, unresolved wall-clock cost

The device-pass and digital ledgers yield component estimates at the optimistic corner. These are
not total training energies.

| route | conversion energy | digital-twin compute estimate |
|---|---|---|
| PAT | 0.57 mJ | ≈13–44 J |
| adjoint | 1.1 mJ | 0 in the idealized physical-adjoint ledger |
| SPSA | 2.6 mJ | no digital twin |

PAT's digital estimate uses the registered FLOP model and named accelerator-efficiency classes, not
a measured implementation; the adjoint row is conditional on realizing the reverse pass; SPSA's
vendor-part conversion estimate is 99 mJ. SPSA's 176,000 passes, each of 256 samples at 2 GS/s,
occupy **22.528 ms of optical sequence time**, a lower bound on training duration and not elapsed
wall time. A total estimate must add parameter writes, actuator settling, measurement and
controller latency, reset gaps, and the laser, gain-pump, locking, packaging and thermal-hold power
over the full duration,
$E_{\rm train}=E_{\rm conversion}+E_{\rm digital}+E_{\rm writes}
+\int_0^{t_{\rm wall}}P_{\rm hold}(t)\,dt$. Those quantities have not been established for any
device, so no total-training-energy ranking is claimed; an earlier total-energy claim is withdrawn
(supplementary N8).

### 7.4 Registered inline follow-up: no energy-advantage window

A follow-up envelope (PR-20, frozen before calculation) replaces the block-level comparison with
the per-tap digital equalizer an inline device would replace, and charges actuator, common-mode
thermal-management, gain-pump and maintenance rows. It is a calculated model envelope, not measured
hardware performance. Across the registered 0.1–2 GS/s grid, the best optimistic cell gives
$E_{\rm digital}/E_{\rm photonic}=0.64$: 3.2 pJ/sample digital against ≈5.0 pJ/sample photonic at
2 GS/s, 64 taps, passive C-3 and 10 mW of global thermal hold. The photonic estimate is therefore
**1.56 times the digital energy**, missing both parity and the registered 3× threshold. Removing
the unsourced optimistic rows lowers the best ratio to 0.23, and the conservative maximum is 0.38.
The kill gate fired, and no product simulation or fabrication spend followed.

Thermal management dominates even the most favorable cell with zero actuator hold. Dropping the
gain stage costs memory, though less than a naive tenfold: the frozen minimum-damping model gives a
pumped-to-passive memory ratio of 3.14 at $r_\text{min}$ (N9.7). Longer control and settling times
can only raise modelled photonic energy at a fixed retraining cadence, so they cannot reverse the
gate. The calculation also does not establish that practical retraining is cheap, or that the
chosen cadence maintains accuracy. At fixed power and fixed
tap count the ratio grows only linearly with sample rate; higher rates lie outside PR-20 and have
no trainability result. This function-matched result supersedes the positive reading of §7.2: the
simulated trainability result stands, and energy-competitive hardware has not been demonstrated.

## 8. Limits of this model

### 8.1 Robustness here means robustness to what we modelled

Every robustness statement in §5 is conditioned on the substrate of §3: the methods absorb the
imperfections *we simulated* — saturating gain at a registered operating point, Langevin amplifier
noise at NF 7 dB, resolved backscatter doublets, 5%-class calibration mismatch, fresh noise per
pass. Hardware contains channels we did not model: thermal transients and self-heating, polarization
rotation, fabrication disorder beyond the derate row, drift at cadences between our episode and
training scales, and mode-splitting behavior not captured by one always-on γ per process class. Any
of these could reorder the §5 ranking on a real chip. We regard the ranking as a hypothesis for
hardware to test, with PAT and SPSA committed because their chip-level robustness is already
established [3, 2].

### 8.2 Anchor risks and verification debts, by name

The C-2 loss class transfers a wide-multimode racetrack result to a single-mode ring, priced by the
×2-loss derate row (§3.3). The Er:Si₃N₄ noise budget rests on a single coupling-loss-limited system
NF of ~7 dB, with the intrinsic amplifier NF not isolated (§3.2). The recurrent adjoint pass is
charged as if realizable with no demonstration in the literature (debt #4, an inference from
absence as of mid-2026). The white-space claim is one-sided evidence from a pre-registered search, last refreshed by a
bounded search on 2026-09-13 (debt #1; N3). The on-resonance clamp calibration under worst-case de-saturation remains a labelled
risk, with the δ-aware clamp ($r \approx 0.2547$) as its computed mitigation (§3.6).

### 8.3 The benchmark anchor we do not use

An early gate required reproducing a published LinOSS benchmark as an external anchor. Our port of
the model reproduced the Heartbeat result within its published band. On EigenWorms, five runs of
the authors' official code on their published seeds averaged 90.56%, against the published
95.0 ± 4.4%, with a population standard deviation of 8.35 percentage points (Fig. S1). Five runs
are descriptive; they do not show that the published mean or dispersion is wrong. We also found that
the implementation's classification loss, $-\log(p_\text{true} + 10^{-8})$ on softmax
probabilities, loses its gradient when the correct-class probability underflows. Our port shows
finite windows of exactly zero gradient, but an archived screen of the official code found no strict traps in eight runs under its registered classifier, so this mechanism is not established as the cause of the lower scores;
a separate note is in preparation. The gate was adjudicated purpose-served with the external anchor void (PR-1.1), and every
accuracy reference in this program is therefore an in-house
BPTT-on-substrate measurement under our own protocol (§5.1), never a transferred published number.
Our substrate runs in float64.

### 8.4 Review independence

Through 2026-07-06 every freeze in the ledger passed adversarial review by an independent reviewer
session reporting to the PI, and several results exist because that review forced them (the
multi-tap input map, the mismatch decomposition, the readout-differential rule). From 2026-07-07 the
program ran in a single-session mode in which one agent performed both execution and review under
standing PI delegation. Everything from that date, including the S0.4b/c and S0.5 findings and the
two honest nulls (the offline tie; RHEL's failure), should be read with that reduced independence
in mind. Pre-registration is the structural mitigation, with a stated caveat: once registrar and
registrant are the same agent, the commit trail is self-graded until it is externally anchored.
Two anchors exist. An OpenTimestamps proof of the ledger head certifies existence by date,
independently of repository access, though not the actual execution times of experiments. The
repository, with the full ledger and commit history, is released publicly with this preprint at
`github.com/LTalandier/Project_SSM`, which makes the recorded commit ordering inspectable. Seven
post-assembly review rounds and a later repository audit found errata concentrated in unregistered
connective prose, one pre-written consumption text applied to a degenerate outcome, one
implementation defect and one optical-time versus wall-time error. The affected claims were
corrected or withdrawn, and the defect was repaired by a registered rerun; the record is in
supplementary N8 and N9.8.

### 8.5 Scope limits we chose

The task family is deliberately narrow — continuous-signal channel equalization plus a synthetic
memory family, with the registered secondary task deferred — and the 128-ring C-3 cell never gates
anything. Calibration mismatch and drift, held fixed in the bake-off, were measured afterward in
pre-registered follow-ups (§5.5). Drift remains unmodelled *during* training at the bake-off cadence, and the tested drift
is gentle ($\approx 1.4\,\kappa_i$ accumulated) rather than worst-case. A follow-up task's operating
point must be registered against its own processing gain, the lesson of the degenerate memory probe
in §6. The strongest current evidence on the advantage question is §5.5's triple: no resolved
difference at five calibration levels spanning 5–30%, none under common-mode drift, and a declared
2.42× advantage specific to uncorrelated per-ring drift, whose hardware relevance rests on the
unmeasured correlation of real on-chip drift. The 2026-09-13 repository audit and its correction
were implemented and checked in one session without independent review (N8).

## 9. Outlook: Stage 1

### 9.1 Hardware development paused

The inline kill gate (§7.4) closes the registered product route, and no wafer or
product-development spend is planned. A later exploratory study of a low-Q ring regime, registered
in the same ledger (PR-22, PR-23), found no validated energy window either; it is not part of this
paper's results. What follows describes a possible collaborator-led research demonstrator, not a
fabrication plan.

The bake-off fixes that demonstrator's training stack by evidence: **PAT and SPSA, nothing else in
the loop.** Neither exotic route earned promotion (§5.3), and the hardware ledger (supplementary
N2) shows why hardware grounds are unlikely to reverse that: the adjoint adds circulators,
phase-coherent reverse injection and an unsolved separation of the counter-propagating field from
the backscatter doublet, and RHEL adds a pumped conjugator bank whose ≈9.6 W budget at 32 rings
exceeds the rest of the system. The minimal demonstrator is the §3 plant with 8–32 rings
(foundry-floor Q suffices, per C-1's gate), thermo-optic $\{\delta, \kappa_\text{ext}, \mu\}$
actuation, one drop-port readout chain, the four-tap drive map of §3.6, SPSA as the first-light
route and PAT once the twin is characterized to the 5%-class accuracy the mismatch protocol
assumed. SPSA runs under the δ-aware clamp $r \geq 0.2547$ from the start, because its solutions
are the ones that approached the hypothetical super-threshold corner (§3.6). The registered cells
are foundry-realizable, with C-2 bounded by a demonstrated multi-project-wafer result
[20], and the actuation uses standard thermo-optic tuners.

### 9.2 What would change our mind

Three pre-registered forks. (i) **Adjoint promotion**: if a physical recurrent reverse pass is
demonstrated (debt #4), the PR-9 criterion reopens with these data as prior; the simulation
predicts ceiling-grade accuracy at 2× PAT's device passes and zero digital cost. (ii) **The in-situ
advantage**: with no resolved calibration difference across 5–30%, in-situ training earns a place
on hardware only through a measured differential. Independent drift is the modelled candidate, and
the experiment should be designed to measure it on one chip, offline-deploy against PAT/SPSA arms,
rather than assume it; mismatch beyond the tested grid and total training energy remain
unresolved. (iii) **RHEL**: nothing on SiN. The idealized-conjugator control shows a perfect echo
contributing ≈0 through the recurrence (§5.4), so reopening it needs a conservative platform
regime, not a better conjugator.

### 9.3 Beyond the linear unselective core

The frozen architecture is the unselective linear time-invariant core — poles and couplings, the
part photonics builds natively. Input-dependent dynamics in the Mamba direction [35] would
map onto the same lattice as input-dependent $C$ and then $B$ actuation, behind its own gate;
nothing in this paper depends on it.

### 9.4 Closing

The program asked a narrow question with unusual bookkeeping: can the physics of a dissipative
photonic recurrence be trained through itself, and at what honest cost? In simulation, under
pre-registered thresholds, yes — by the two methods a chip can already run, at quantified
device-pass cost, with the exotic routes priced out by data and the independent-drift advantage
bounded by its simulation assumptions. The function-matched inline envelope is negative within the registered window. A chip
would test physical trainability, but these results do not justify product development or
fabrication spend.

## Figures

![F1](figures/F1_architecture_pole_region.png)

**Figure F1 — Architecture and realizable pole region.** (a) The N = 32 coupled-ring chain (C-2):
trained set {δ_j, κ_ext,j, μ_j,j+1} with the resolved four-tap input map B = {3, 12, 21, 30}
(§3.6). (b) Realizable memory (samples at 2 GS/s) versus intrinsic Q at gain fractions
g_f ∈ {0, 0.5, 0.9}, the three registered cells and the 7-tap task span: at g_f = 0 the
foundry-floor cell sits at the task span; at the registered g_f = 0.9 all three cells clear it.

![F2](figures/F2_substrate_clamp.png)

**Figure F2 — The substrate's operating map.** (a) Settled saturating net loss κ_net(r) against the
fixed-gain plane, the lasing crossing r\*, the clamp band (r_min = 0.1606; margins m_κ = 0.05,
Δr = 0.02) and the initialization θ₀. (b) Off-resonance de-saturation at r_min: a detuned ring
reaches κ_net = −0.48 κ_i, the open anchor risk of §3.6.

![F3](figures/F3_participation_profile.png)

**Figure F3 — Controllability is a first-class constraint.** Per-ring gradient magnitude relative to
the maximum ring, under one input tap and under the resolved four-tap map. The single-drive profile
collapses with distance (ring 32 ~25 orders below the maximum); B = {3, 12, 21, 30} puts all 32
rings above the 10⁻³ gate (worst 1.42 × 10⁻³, minimum over five drive seeds).

![F4](figures/F4_sample_efficiency.png)

**Figure F4 — Sample efficiency to target.** Median held-out SER versus device passes at C-2 (8
seeds; shaded IQR) for PAT, adjoint, SPSA, RHEL (censored), the readout-only baseline and the
offline-deploy arm, which starts low because it is pre-trained. Dotted lines: the BPTT reference,
drawn as a level because it uses no device passes, and the target SER = 5.65 × 10⁻³. Vertical
line: the budget B = 252,800.

![F5](figures/F5_ranking.png)

**Figure F5 — Ranking at matched device-pass cost.** Median device passes to target, per-seed dots,
with the digital side-ledger hatched (PAT's twin = 505,600 digital passes): PAT 38,400 < adjoint
73,600 < SPSA 176,000; RHEL censored 0/8. Neither exact method beats both workhorses.

![F6](figures/F6_damping.png)

**Figure F6 — Damping is a first-order design knob.** Final SER versus uniform pinned overcoupling r
(plateaued endpoints spanning ×302), with the optimum r\* = 2.0 (measured κ_net = 3.7 κ_i). Boxes
containing r\* train to the 5 × 10⁻⁴ reference, beating every uniform pin. Dashed red: the T-A-L
transfer task (14-tap span, eval-F), whose predicted shift to lighter damping failed; r = 2–3 lie
within 13% (§6).

![F7](figures/F7_envelope.png)

**Figure F7 — Historical systems-envelope components.** (a) Conversion-energy estimates (SPSA
2.6 mJ OPT / 99 mJ CONS; PAT 0.57 mJ OPT) and PAT's 13–44 J digital-twin estimate. Writes, settling
and full-duration holding costs are excluded, so the panel does not rank total training energy
(§7.3, N8). (b) The original nominal-N inference comparison at 2 GS/s, superseded by the
function-matched result of §7.4.

![F8](figures/F8_mismatch_drift.png)

**Figure F8 — Pre-registered follow-ups to the offline comparison (§5.5; eval-F).** (a) Corrected
5–30%-class calibration sweep (S0.13), eight seeds per arm and level; lines are medians, dots
seeds. All five paired intervals include zero; offline/PAT ratios span 0.994–1.053. (b)
Common-mode drift (σ_step = 0.40 κ_i on all detunings coherently): the offline re-lock keeps pace
(ratio 1.34, CI including zero). (c) Independent per-ring drift: in-situ retraining holds near the
reference while the re-locking offline arm degrades — time-integrated ratio 2.42×, difference CI
[+0.71, +2.84] × 10⁻³, both conditions of the frozen rule (PR-16). The coarse-floor estimate of the same bit-identical trajectories, 1.84×, sat below the bar and is
co-reported; the ratio's own CI, [1.7, 4.6], is given in §5.5. The in-situ SPSA curve is context
only. Dashed and dotted
lines: the target and the matched-budget BPTT reference (31,600 updates).

![S1](figures/S1_g3_anchor_dossier.png)

**Figure S1 — The benchmark anchor we do not use (§8.3).** (a) Validation-accuracy trajectories of
the official LinOSS-IM code on the five published EigenWorms seeds (our rerun). Two trails drop
sharply late in training. Test accuracy is taken at the validation-selected checkpoint, and the
trails carry no per-step gradient measurements, so they do not explain the two low test scores.
(b) Final test
accuracy per seed (97.22 / 83.33 / 97.22 / 97.22 / 77.78%) against the published 95.0 ± 4.4%: rerun
mean 90.56%, population SD 8.35 percentage points.

![S2](figures/S2_twin_mismatch_c1.png)

**Figure S2 — Twin-mismatch decomposition at C-1 (§5.6; eval-F).** Final SER (3 seeds) for PAT
with a perfect, a parametric-error (M-par) and a structural-omission (M-struct) twin: perfect and
M-struct coincide (1.11 × 10⁻³) and M-par shows a small excess (1.31 × 10⁻³, +18%). Mismatch
channels are ≈ 0 at this cell only (§5.6). The idealized-conjugator RHEL control clears the C-1
target narrowly (7.2 vs 7.3 × 10⁻³), locating RHEL's C-2 failure in echo physics.

![S3](figures/S3_echo_chain.png)

**Figure S3 — The concrete echo sub-model (§4.5).** (a) Conjugation-chain waterfall at the frozen
operating point: ring-port extraction η_ex², single-pass χ³-FWM spiral conversion (0.3 W pump,
0.5 m) and routing, η_c = −22.4 dB per conjugation. (b) Per-cell ceilings for the alternatives: a
resonant-ring loaded-Q ceiling (mechanism B) and 10-ns off-chip transit amplitude survival
(mechanism C).

![S5](figures/S5_rhel_r1_recovery.png)

**Figure S5 — RHEL recovers its own theorem's limit (§5.4).** Cosine between the RHEL update and
the exact gradient as the substrate is made less dissipative: −0.75 at κ_net T dt ≈ 1.0, rising
monotonically to +1.0000 at 0.03. The C-2 operating point sits at κ_net T dt ≈ 8 (C-1 at ≈ 27).

## References

1. Spall, "Multivariate stochastic approximation using a simultaneous perturbation gradient approximation," IEEE Trans. Autom. Control 37(3), 332–341 (1992)
2. Bandyopadhyay, Sludds, Krastanov, Hamerly, Harris, Bunandar, Streshinsky, Hochberg, Englund, "Single-chip photonic deep neural network with forward-only training," Nat. Photonics 18, 1335–1343 (2024). arXiv:2208.01623
3. Wright, Onodera, Stein, Wang, Schachter, Hu, McMahon, "Deep physical neural networks trained with backpropagation," Nature 601, 549–555 (2022)
4. Hughes, Minkov, Shi, Fan, "Training of photonic neural networks through in situ backpropagation and gradient measurement," Optica 5(7), 864–871 (2018)
5. Tanaka et al., "Recent advances in physical reservoir computing: A review," Neural Networks 115, 100–123 (2019); Van der Sande, Brunner, Soriano, "Advances in photonic reservoir computing," Nanophotonics 6(3), 561–576 (2017)
6. Jayatilleka et al., "Wavelength tuning and stabilization of microring-based filters using silicon in-resonator photoconductive heaters," Opt. Express 23(19), 25084–25097 (2015); Mak, Sacher, Xue, Mikkelsen, Yong, Poon, "Automatic Resonance Alignment of High-Order Microring Filters," IEEE JQE 51(11) (2015); Milanizadeh, Aguiar, Melloni, Morichetti, "Canceling Thermal Cross-Talk Effects in Photonic Integrated Circuits," JLT 37(4), 1325–1332 (2019)
7. Bueno, Maktoobi, Froehly, Fischer, Jacquot, Larger, Brunner, "Reinforcement learning in a large-scale photonic recurrent neural network," Optica 5(6), 756–760 (2018)
8. Böhm, Verschaffelt, Van der Sande, "A poor man's coherent Ising machine based on opto-electronic feedback systems…," Nat. Commun. 10, 3538 (2019); companion: Böhm et al., Nat. Commun. 13, 5847 (2022)
9. Wu et al., "Monolithically integrated asynchronous optical recurrent accelerator," eLight 5, 7 (2025)
10. Ashtiani, Idjadi, Kim, "Integrated photonic neural network with on-chip backpropagation training," Nature 651, 927–932 (2026). arXiv:2506.14575
11. Zhao et al., "In-Situ Trained Microring-Based Neural Networks," Laser Photon. Rev. (2025), 10.1002/lpor.202501576
12. Wu, Ren et al., "Time-synthetic optical neural networks with stable programmable gain," arXiv:2507.02297 (retitled from "A scalable and programmable optical neural network in a time-synthetic dimension")
13. Zhang, Wang, Lederman, Shastri, Prucnal et al., "Compact, reconfigurable, and scalable photonic neurons by modulation-and-weighting microring resonators," eLight 6, 6 (2026). arXiv:2505.11369
14. "In-situ optimization of an optoelectronic reservoir computer with digital delayed feedback," ACS Photonics (2025). arXiv:2502.11126
15. Van Assche, Masaad, Gooskens, Sackesyn, Van Kerrebrouck, Yin, Bienstman, "Real-time optical signal equalization with a silicon photonic spatially distributed reservoir computer," Nat. Photonics 20, 1062–1069 (2026), 10.1038/s41566-026-01968-2. arXiv:2503.19911
16. Gu, Goel, Ré, "Efficiently Modeling Long Sequences with Structured State Spaces," ICLR 2022. arXiv:2111.00396
17. Gu, Gupta, Goel, Ré, "On the Parameterization and Initialization of Diagonal State Space Models," NeurIPS 2022. arXiv:2206.11893
18. Rusch, Rus, "Oscillatory State-Space Models," ICLR 2025 (Oral). arXiv:2410.03943
19. Boyer, Rusch, Rus, "Learning to Dissipate Energy in Oscillatory State-Space Models," arXiv:2505.12171
20. Cui, Cao, Pan, Gao, Yu, Zhang, "Compact microring resonator based on ultralow-loss multimode silicon nitride waveguide," Adv. Photonics Nexus 2(4), 046007 (2023)
21. Gupta, Gu, Berant, "Diagonal State Spaces are as Effective as Structured State Spaces," NeurIPS 2022. arXiv:2203.14343
22. Haus, *Waves and Fields in Optoelectronics*, Prentice-Hall (1984)
23. Gorodetsky, Pryamikov, Ilchenko, "Rayleigh scattering in high-Q microspheres," JOSA B 17(6), 1051–1057 (2000); Kippenberg, Spillane, Vahala, "Modal coupling in traveling-wave resonators," Opt. Lett. 27(19), 1669–1671 (2002)
24. Liu, Huang, Wang, He, Raja, Liu, Engelsen, Kippenberg, "High-yield, wafer-scale fabrication of ultralow-loss, dispersion-engineered silicon nitride photonic circuits," Nat. Commun. 12, 2236 (2021)
25. Rukh, Colación, Buck, Drake, "Process-structure-property relationships in subtractive fabrication of silicon nitride microresonators for nonlinear photonics," arXiv:2511.02198 (2025)
26. Liu, Qiu, Ji, Lukashchuk, He, Riemensberger, Hafermann, Wang, Liu, Ronning, Kippenberg, "A photonic integrated circuit-based erbium-doped amplifier," Science 376, 1309–1313 (2022)
27. Ye, Marpaung, "Compact multi-mode silicon-nitride micro-ring resonator with low loss," Adv. Photonics 5(5), 050503 (2023)
28. Talandier, multi-layer photonic-equalization manuscript (in preparation) + chip β-track thermal-crosstalk/perturbation-tolerance results
29. Pourcel, Ernoult, "Learning long range dependencies through time reversal symmetry breaking," arXiv:2506.05259 (2025)
30. López-Pastor, Marquardt, "Self-Learning Machines Based on Hamiltonian Echo Backpropagation," Phys. Rev. X 13, 031020 (2023). arXiv:2103.04992
31. Riemensberger, Kuznetsov, Liu, He, Wang, Kippenberg, "A photonic integrated continuous-travelling-wave parametric amplifier," Nature 612, 56–61 (2022); Krückel et al., "Continuous wave-pumped wavelength conversion in low-loss silicon nitride waveguides," Opt. Lett. 40(6), 875–878 (2015)
32. this work: PR-15 two-modality search + refresh memos, supplementary N3; public repository `github.com/LTalandier/Project_SSM`
33. Dacha, Zhao, McNulty, Bhatt, Lipson, Gaeta, "Frequency-stable nanophotonic microcavities via integrated thermometry," Nature Photonics (2025). arXiv:2506.21692
34. Gao, Rios-Navarro, Chen, Liu, Delbruck, "EdgeDRNN: Recurrent Neural Network Accelerator for Edge Inference," IEEE JETCAS 10(4), 419–432 (2020). arXiv:2012.13600
35. Gu, Dao, "Mamba: Linear-Time Sequence Modeling with Selective State Spaces," COLM 2024 (Outstanding Paper). arXiv:2312.00752
