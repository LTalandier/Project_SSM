# §2 — From oscillatory state-space models to coupled SiN microrings

**Status:** v2, condensed 2026-09-29 for the first public deposit (v1 at commit `a508a28`).
Validation detail and backscatter conventions moved to supplementary N9.1.

---

## 2.1 The model class

A structured state-space model (SSM) processes a sequence $u_1, u_2, \dots$ through a linear
recurrence $x_{t+1} = \bar A x_t + \bar B u_t$, $y_t = \mathrm{Re}(\bar C x_t) + D u_t$, whose
expressive power is set by where the eigenvalues (poles) of $\bar A$ can be placed. The diagonal
variants S4D and DSS [CITE-S4D, CITE-DSS] reduce $\bar A$ to independent complex poles,
$H(s) = \sum_j c_j b_j/(s - \lambda_j) + D$; the oscillatory LinOSS family [CITE-LINOSS]
parameterizes forced, damped harmonic oscillators, and D-LinOSS [CITE-DLINOSS] makes each mode's
damping trainable. The LinOSS construction holds for any nonnegative-diagonal (dissipative) state
matrix: stability requires only that every mode decay. A substrate that is lossy but slowly so is
therefore in-regime, and its loss is the model's damping parameter. Where the trained optimum
lands in that range is measured in §6.

## 2.2 One ring is one trainable complex pole

The mode amplitude $a_j$ of a silicon-nitride microring obeys temporal coupled-mode theory (Haus
energy-amplitude convention) [CITE-HAUS]:

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

## 2.3 Coupling rings

Energy-conserving inter-ring coupling adds $i\Omega$ with $\Omega$ real-symmetric. It hybridizes
the poles while conserving total damping,
$\sum_j \mathrm{Re}\,\lambda_j = -\sum_j \kappa_{\mathrm{tot},j}$ (verified: the two-ring beat
matches the $2\mu$ eigenvalue splitting to $<2\%$). The trainable $\mu_{jk}$ reshape frequencies
but cannot buy stability or memory; they matter for the claim because inter-ring couplings are
recurrence-defining (§2.5).

## 2.4 The realizable pole region

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
into a doublet when $2\gamma \gtrsim \kappa_\mathrm{tot}$ [CITE-modal-coupling]. Since $\kappa_i$
falls as $Q_i$ rises while $\gamma$ does not, splitting grows with $Q$: a clean damascene-class
process ($\gamma/2\pi \approx 12$ MHz [CITE-damascene]) keeps single poles at the foundry corner
and splits near $Q \approx 4\times10^6$, while a rough subtractive process splits 21–75% of
resonances already at $Q_i \lesssim 2.7\times10^6$ [CITE-SUBTRACTIVE]. The substrate therefore
carries the doublet explicitly (§3.4). Crossover conventions and their sources are in N9.1.

## 2.5 What training the recurrence in situ means physically

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
[CITE-BUENO-BRUNNER]. A method earns the in-situ-training claim only if it updates
$\{\delta_j,\ \kappa_{\mathrm{tot},j},\ \mu_{jk}\}$ on the device (PR-2, PR-6), and every method in
the bake-off trains that same set. The set is gain-free and all-thermo-optic, heaters and tunable
couplers only, which suits perturbative training on SiN.
