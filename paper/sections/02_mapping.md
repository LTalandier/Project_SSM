# §2 — From oscillatory state-space models to coupled SiN microrings

**Status:** DRAFT v1 (2026-07-07, Supervisor) — first prose pass, not frozen, Critic-unreviewed.
**Sources of record:** `docs/s0_1/{mapping_result,mapping_notes,B1_actuation_map,B2_backscatter_bound,B3_kappa_ext_tradeoff}.md`
· `shared/results_log.md` (S0.1, S0.1.1) · `shared/critic_review_s0-1-results.md`. Every number
below is the Executor's, validated by the cited tests; none originate in this draft.
**Open flags carried:** [CITE-*] keys resolved via `paper/references.md` (2026-07-12; backscatter sources page-verified, convention stated in-text); the B2 quantitative crossovers are ⚠ provisional
pending F5 primary-source verification (S0.L, before submission).

---

## 2.1 The model class

A structured state-space model (SSM) processes a sequence $u_1, u_2, \dots$ through a linear
recurrence $x_{t+1} = \bar A x_t + \bar B u_t$, $y_t = \mathrm{Re}(\bar C x_t) + D u_t$, whose
expressive power is set by where the eigenvalues (poles) of $\bar A$ can be placed and how
precisely. The diagonal variants that dominate current practice — S4D and DSS [CITE-S4D, CITE-DSS]
— reduce $\bar A$ to a set of independent complex poles, $H(s) = \sum_j c_j b_j/(s - \lambda_j) + D$;
the oscillatory LinOSS family [CITE-LINOSS] instead parameterizes forced, damped harmonic
oscillators, and its damped extension D-LinOSS [CITE-DLINOSS] makes the damping of each mode a
trainable parameter. Crucially for what follows, the LinOSS construction is valid for any
nonnegative-diagonal (dissipative) state matrix: stability does not require conservative dynamics,
only that every mode decay. A physical substrate that is *lossy but slowly so* is therefore
in-regime by construction — the loss is not an error term to be fought but the damping parameter
of the model class itself. (Where in the damping range the trained optimum actually lands — and
what that does to the LinOSS-specific part of this motivation — is measured, not assumed; see
§6.)

## 2.2 One ring is one trainable complex pole

The mode amplitude $a_j$ of a silicon-nitride microring obeys temporal coupled-mode theory
(Haus energy-amplitude convention, $|a|^2$ = stored energy) [CITE-HAUS]:

$$\dot a_j = (i\delta_j - \kappa_{\mathrm{tot},j})\,a_j
+ i\sum_{k\neq j}\mu_{jk}\,a_k + \sqrt{2\kappa_{\mathrm{ext},j}}\,u(t),$$

with $\kappa_{\mathrm{tot},j} = \kappa_{i,j} + 2\kappa_{\mathrm{ext},j}$ the amplitude decay rate
(intrinsic + both bus ports of the add–drop registry ring, each loading the mode at
$\kappa_\mathrm{ext}$; the drive enters through one port, hence the single
$\sqrt{2\kappa_{\mathrm{ext}}}$ injection term), $\delta_j$ the detuning of the drive from the ring resonance, and
$\mu_{jk}$ the inter-ring coupling. A single uncoupled ring is therefore exactly one **complex**
Laplace pole,

$$s_j = -\kappa_{\mathrm{tot},j} + i\,\delta_j,$$

— complex, not real, because the optical envelope carries a carrier. A bank of $N$ rings natively
realizes a **diagonal complex-pole SSM of the S4D/DSS class**: one ring per pole, with the
injection and readout couplings playing the role of the residues $c_j b_j$. The oscillatory
LinOSS unit is recovered *exactly* as the uncoupled, real-input/output special case: a real damped
second-order oscillator is a conjugate pole pair, and the identification against the LinOSS
eigenvalue $a_i = -e^{\alpha_i} + i\beta_i$ is

$$e^{\alpha_i} = \kappa_\mathrm{tot}, \qquad \beta_i = \delta.$$

Storing $\alpha_i = \log\kappa_\mathrm{tot}$ enforces the dissipative sign and
$\kappa_\mathrm{tot} > 0$ by construction — the physical substrate implements the model's own
stability parameterization. We deliberately claim the broader class and treat LinOSS as its
special case, with one consequence made explicit now: published LinOSS/D-LinOSS benchmark results
validate only the $\mu = 0$ diagonal reduction, and transfer to the coupled realization is
verified in-house against a BPTT-on-substrate ceiling (§5.1) rather than assumed.

Discretization is exact, not approximate: for piecewise-constant input the zero-order-hold
(van-Loan matrix-exponential) step gives discrete poles $z = e^{s\,dt}$ to machine precision, with
$dt$ the round-trip time. The per-step memory retention is $|z| = e^{-\kappa_\mathrm{tot} dt}$;
long memory is literally $|z| \to 1$.

**Validation.** The mapping is validated at three levels (test-anchored; all
thresholds pre-specified): (i) *by construction* — uncoupled system poles match the CMT reference
to $<10^{-3}$ and discrete $|z|$ to $<10^{-9}$; (ii) *in the CW limit* — the dynamical model's
steady state recovers independently derived static transfer functions with error scaling as
$O(1/\mathcal{F})$ (finesse), measured $4.5\times10^{-4}$ at $\mathcal{F} = 1048$ falling to
$4.4\times10^{-5}$ at $\mathcal{F} = 10473$; the registry rings sit at $\mathcal{F} \approx 10^3$–
$1.5\times10^4$, where the CMT pole is an excellent model; (iii) *in the time domain* — against an
independent RK45 integration, ringdown matches the closed form to $<10^{-9}$ and both pole
coordinates ($\kappa$ and $\delta$) re-fitted from the trajectory recover the set values to
$<10^{-5}$. All three are *internal* checks — independent implementations and limits of the
same coupled-mode model class — so they certify that the simulator faithfully computes the
model it claims, not that the model captures a fabricated device; the latter is a hardware
question, scoped honestly in §8.1.

## 2.3 Coupling rings: the structured off-diagonal generalization

Energy-conserving inter-ring coupling enters as $i\Omega$ with $\Omega$ real-symmetric — an
anti-Hermitian addition to the state matrix. It hybridizes the poles (photonic-molecule
supermodes) while conserving total damping: the eigenvalues move along the imaginary axis while
$\sum_j \mathrm{Re}\,\lambda_j = -\sum_j \kappa_{\mathrm{tot},j}$ is invariant (verified: two-ring
beat frequency equals the eigenvalue splitting $2\mu$ to $<2\%$, with a no-beat control at
$\mu = 0$). The trainable $\mu_{jk}$ are thus a *mild, structured* generalization beyond
diagonal-$A$ SSMs — off-diagonal terms that reshape frequencies but cannot buy stability or
memory. They are also load-bearing for the claim this paper builds toward: inter-ring couplings
are recurrence-defining parameters (§2.5).

## 2.4 The realizable pole region

Where can the poles actually go? Four physical boundaries define the envelope (Fig. F1).

**Memory is loss-limited; stability is free.** Passive rings satisfy
$\kappa_\mathrm{tot} \geq \kappa_i = \omega_0/(2Q_i)$, so the maximum amplitude (state) memory
time is $1/\kappa_i = 2Q_i/\omega_0$ — twice the photon-energy lifetime, a convention this paper
uses consistently. Across the registered platform range this gives **3.29 ns (329 round trips)**
at the foundry-conservative corner ($Q_i = 2\times10^6$) to **49.4 ns (4937 round trips)** at the
class-leading corner ($Q_i = 3\times10^7$): a 15× memory span that is the platform's dominant
figure of merit and the reason this program is on SiN (§1). Net optical gain moves
$\kappa_\mathrm{tot} \to 0$ and hence $|z| \to 1$, extending memory past the passive floor at the
cost of saturation and amplified-spontaneous-emission noise — deferred to the substrate model
(§3).

**Frequency is FSR-bounded.** The detuning axis aliases at one free spectral range:
$|\beta_j\,dt| \leq \pi$ with $dt = 1/\mathrm{FSR}$. The reachable imaginary axis is one FSR wide.

**Readout trades against memory.** The external coupling sets both memory
($1/\kappa_\mathrm{tot}$, maximized by deep undercoupling) and readability (residue
$\propto 2\kappa_\mathrm{ext}$; on-resonance drop efficiency
$(2\kappa_\mathrm{ext}/\kappa_\mathrm{tot})^2$, i.e. detector SNR) in opposite directions; their
product is bounded by the passive memory length (tested). At the foundry corner the trade runs
from 274 round trips at drop efficiency 0.028 (deep undercoupling,
$\kappa_\mathrm{ext} = 0.1\kappa_i$) to 16 round trips at 0.91 (deep overcoupling, $10\kappa_i$);
the same Pareto shape holds at the class-leading corner with the memory axis scaled ~15×. The
operating point is not chosen here: it is pre-registered (§3, PR-4), and
$\kappa_\mathrm{ext}$ is itself a pole-real-part actuator, so a trainable-$\kappa_\mathrm{ext}$
policy folds the readout trade into the recurrence training.

**Backscatter bounds the one-ring-one-pole abstraction — by roughness, not cleanly by $Q$.**
Sidewall roughness couples the counter-propagating modes at a coherent rate $\gamma$ that is a
fabrication constant, essentially independent of $\kappa_\mathrm{tot}$; the resonance resolves
into a standing-wave doublet when $2\gamma \gtrsim \kappa_\mathrm{tot}$ (conservative HWHM
criterion; the FWHM criterion shifts every crossover ×2, conclusion unchanged)
[CITE-modal-coupling]. Because
$\kappa_i$ falls as $Q_i$ rises while $\gamma$ does not, splitting *grows* with $Q$: from
measured SiN rates, a clean damascene-class process ($\gamma/2\pi \approx 12$ MHz
[CITE-damascene]) keeps the single-pole picture at the foundry corner ($2\gamma/\kappa_i
\approx 0.5$) and breaks it at $Q \approx 4\times10^6$ (HWHM; $8\times10^6$ FWHM), while a rough
subtractive process splits 21–75 % of resonances *already at* $Q_i \lesssim 2.7\times10^6$, with
average doublet separations of 180–320 MHz depending on etch mask [CITE-SUBTRACTIVE] — i.e.
modal-coupling rates $\gamma/2\pi \approx 90$–$160$ MHz under the standard
$2\gamma$-separation convention [CITE-modal-coupling], a mapping we state here because the
source tabulates separations, not rates (page-verified 2026-07-12). *The assembled crossover curve brackets published SiN data
points — no single published SiN crossover exists, and no $\gamma$ is published for the
specific target processes; primary-source verification is registered before submission.*
Two consequences propagate forward: the substrate model carries a roughness-gated CW/CCW doublet
knob, default ON except at the clean-damascene corner (§3); and a platform tension
is on record — the best-memory (highest-$Q$) platforms are the most splitting-prone, while the
splitting-safe low-$Q$ foundry corner is memory-poor. Overcoupling suppresses the visible
doublet, so the $\kappa_\mathrm{ext}$ policy and the splitting risk are coupled: the max-memory
(deep-undercoupled) regime is the most exposed.

## 2.5 What "training the recurrence in situ" means physically

The recurrence is defined by the state matrix
$M = \mathrm{diag}(-\kappa_{\mathrm{tot},j} + i\delta_j) + i\Omega$. Every entry has a concrete,
independently addressable actuator:

| Pole quantity | Physical knob | Actuator | Cost |
|---|---|---|---|
| $\mathrm{Im}$ (frequency) $\delta_j$ | ring resonance offset | thermo-optic heater (trench-isolated), one per ring | low: 1 heater + DAC channel/ring |
| $\mathrm{Re}$ (damping) $\kappa_{\mathrm{tot},j}$ | bus–ring coupling $\kappa_{\mathrm{ext},j}$ | tunable coupler (MZI-assisted gap) | medium: 1–2 heaters/ring |
| same, past the passive floor | per-ring net gain $g_j$ | Er:SiN / III–V pump current | high (gain stage + ASE cost); not required for the claim |
| off-diagonal $\mu_{jk}$ | ring–ring coupling | tunable photonic-molecule coupler (or bus-mediated mesh) | medium–high; topology fixed at fab, strengths trainable |
| residues $B, C$ | injection/readout mesh | thermo-optic MZI mesh | **not recurrence-defining** |

The last row is the load-bearing exclusion. Training only the injection/readout mesh — the
residues — while the poles stay fixed is precisely reservoir computing with a trained linear
head, and prior photonic work in that regime (including reinforcement-learning-tuned readouts
[CITE-BUENO-BRUNNER]) does not train the recurrence. The partition this program registers
(§4, PR-2/PR-6) is that a method earns the in-situ-training claim only if it updates
the pole-defining set $\{\delta_j,\ \kappa_{\mathrm{tot},j},\ \mu_{jk}\}$ on the device, and
every method in the bake-off trains the same partition. Notably, the minimal set is *gain-free*
and all-thermo-optic — heaters and tunable couplers only — which is what makes it drift-stable
and realistic for perturbative (SPSA-class) training on SiN; no active gain stage is required
for the headline claim.

The mapping, then, is not an analogy but an identification: a coupled SiN ring bank *is* a
diagonal-complex-pole SSM with structured coupling, its loss *is* the model's damping parameter,
its realizable pole region is bounded and known, and every recurrence-defining parameter has a
physical actuator. Whether those parameters can be *trained through the physics* — with realistic
gain saturation, ASE noise, and measurement cost — is the question the rest of this paper is
built to answer.
