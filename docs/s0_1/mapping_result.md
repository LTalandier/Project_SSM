# Stage-0 result (a) — the oscillator ↔ SiN-ring mapping (Supervisor write-up)

**Author:** Supervisor · **Date:** 2026-06-09 · **Status:** S0.1 + S0.1.1 closed (gates passed; Critic
APPROVE-WITH-EDITS adopted in full); framing resolved **D-2026-06-08-2** (Lucas, 2026-06-09).
**Sources of record:** `shared/results_log.md` (S0.1, S0.1.1) ·
`docs/s0_1/{mapping_notes,B1_actuation_map,B2_backscatter_bound,B3_kappa_ext_tradeoff}.md` ·
`shared/critic_review_s0-1-results.md`. *This document states the result and its framing for the paper;
every number below is the Executor's, validated by the cited tests — none originate here.*

## 1. The result, in one paragraph

A bank of $N$ coupled silicon-nitride microrings, each described by temporal coupled-mode theory,

$$\dot a_j = (i\delta_j - \kappa_{\mathrm{tot},j})\,a_j + i\textstyle\sum_{k\neq j}\mu_{jk}\,a_k
+ \sqrt{2\kappa_{\mathrm{ext},j}}\;u(t),$$

natively realizes a **diagonal complex-pole state-space model of the S4D/DSS class**: one ring
contributes exactly one trainable **complex** pole $s_j = -\kappa_{\mathrm{tot},j} + i\delta_j$ (the
optical field carries a carrier, so the mode amplitude is complex), and energy-conserving inter-ring
coupling ($i\Omega$, anti-Hermitian) contributes a structured off-diagonal generalization. The
oscillatory **LinOSS/D-LinOSS** family is recovered **exactly** as the uncoupled ($\mu=0$), real-I/O
special case — a real damped second-order oscillator is precisely a conjugate pole pair, with the
identification $e^{\alpha_i}=\kappa_\mathrm{tot}$, $\beta_i=\delta$ against the LinOSS eigenvalue
$a_i=-e^{\alpha_i}+i\beta_i$. The realizable pole region is bounded by loss (memory) and FSR
(frequency); stability is free (passive rings are unconditionally dissipative); and the recurrence is
trainable in situ through a gain-free minimal actuation set. This is Stage-0 objective (a), validated by
construction (exact ZOH/van-Loan discretization), in the CW limit (recovers the salvaged static
references at $O(1/\mathcal{F})$), and in the time domain (independent RK45; S0.1.1).

## 2. Framing discipline — what we claim and what we do not (per Critic S0.1-F2, adopted)

- The ring bank **is** a diagonal complex-pole SSM (**S4D/DSS class**). We own that class; the
  "oscillatory LinOSS" branding is **softened** accordingly.
- **LinOSS is its special case**, not its synonym: uncoupled + real I/O $\Rightarrow$ conjugate-pair
  $\Rightarrow$ real second-order oscillator. The proposal's "loss = damping, a free knob" story is
  unchanged — damping is the pole's real part, $\kappa_\mathrm{tot}$.
- **Trainable inter-ring $\mu_{jk}$ is a mild generalization beyond** standard diagonal-$A$
  LinOSS. Published LinOSS/D-LinOSS benchmark results therefore validate **only the $\mu=0$ reduction**;
  transfer to the coupled realization is **open verification debt #2**, validated in-house against the
  BPTT-on-substrate ceiling (PR-3) rather than assumed.
- **The readout decides the remaining equivalence:** coherent-quadrature detection is a real-linear head
  (LinOSS-equivalent); intensity detection is $|\cdot|^2$ (a nonlinear head). **Pinned at PR-2**,
  together with the F6 $\kappa_\mathrm{ext}$ dual-role (damping actuator vs readout knob — the
  reservoir-baseline contrast must stay clean).
- The white-space claim is **unaffected by the framing choice**: what is trained in situ is the B1 set
  $\{\kappa_{\mathrm{tot},j},\,\delta_j,\,\mu_{jk}\}$ — parameters that define the recurrence —
  whichever class label is used. (Existence search running under PR-15; wording at PR-2/S0.8.)

## 3. The validated mapping table

| SSM object | Photonic realization | Validation (test-anchored) |
|---|---|---|
| Complex pole $s_j=-\kappa_{\mathrm{tot},j}+i\delta_j$ | ring $j$: $\kappa_\mathrm{tot}=\kappa_i(Q_i)+\kappa_\mathrm{ext}$, $\delta$ = carrier detuning (heater) | uncoupled poles < 1e-3 vs CMT reference; discrete $\lvert z\rvert$ < 1e-9; **time-domain**: ringdown < 1e-9 vs closed form, pole ($\kappa$ *and* $\delta$) re-fitted from the trajectory < 1e-5 (S0.1.1/F1) |
| LinOSS eigenvalue $a_i=-e^{\alpha_i}+i\beta_i$ | $e^{\alpha_i}=\kappa_\mathrm{tot}$, $\beta_i=\delta$ | pole-identity algebra, §2 of `mapping_notes.md` |
| Off-diagonal coupling | $i\Omega$ (ring–ring $\mu_{jk}$), energy-conserving | 2-ring beat frequency = $\mathrm{Im}\,\mathrm{eig}(M)$ splitting $2\mu$ < 2 %, with $\mu=0$ no-beat contrast; hybridization conserves $\sum\mathrm{Re}(\lambda)=-\sum\kappa_\mathrm{tot}$ |
| Input/readout | $\sqrt{2\kappa_\mathrm{ext}}$ injection; bus/drop ports (Haus convention; the proposal's $\sqrt{\kappa_\mathrm{ext}}$ is a factor-2 naming difference, `mapping_notes.md` §1) | CW limit recovers the S0.0 static references at $O(1/\mathcal{F})$: < 1 % for $\mathcal{F}\geq1000$ (4.5e-4 @ $\mathcal{F}$=1048 → 4.4e-5 @ 10473) |
| Discretization | ZOH van-Loan matrix exponential | **exact** for piecewise-constant input (discrete poles $=e^{\lambda\,dt}$ to machine precision) |
| Trainable recurrence (B1) | $\{\delta_j$ (heaters), $\kappa_{\mathrm{tot},j}$ (tunable coupler and/or per-ring gain), $\mu_{jk}$ (ring–ring coupling)$\}$ | **gain-free minimal set suffices** for the in-situ claim; residues/$B,C$ (MZI mesh) are train-only = the reservoir baseline, explicitly excluded from the claim |
| Gradient flow (3a/3b) | full state trajectory exposed; no `no_grad`/`detach` in the rollout | last-step loss receives gradient from the $t{=}0$ input (49 steps); checkpointed rollout bit-identical to plain — outputs, states, and all gradients (0.0) |

## 4. The realizable pole region (the quantitative envelope)

- **Stability is free; memory is loss-limited.** Amplitude/state memory $1/\kappa_i$:
  **3.29 ns / 329 round trips** at the foundry-conservative corner ($Q_i=2\times10^6$) →
  **49.4 ns / 4937 round trips** at class-leading ($Q_i=3\times10^7$) — a **15× span**. (Amplitude
  convention throughout; the photon-energy lifetime $Q_i/\omega_0$ is half — fixed at S0.1.1/F3. These
  are the numbers PR-2 sizes the bake-off task against.)
- **Frequency axis:** $\delta$ is FSR-bounded ($\lvert\beta\,dt\rvert\leq\pi$). **Gain** moves
  $\lvert\lambda\rvert\to1$ (plotted at net gain 0/50/90 % of loss); saturation + ASE enter at S0.3.
- **$\kappa_\mathrm{ext}$ trade (B3):** memory × residue ≤ passive memory (bounded, tested).
  Undercoupling buys memory at readout cost: at $Q_i=2\times10^6$, 274 rt @ 0.028 drop-efficiency
  ($\kappa_\mathrm{ext}=0.1\kappa_i$) → 16 rt @ 0.91 ($10\kappa_i$). Operating point → **PR-4** (the
  Executor characterized; the choice is pre-registered, not implicit).
- **Backscatter bound (B2/F19; resolved D-08-3):** CW/CCW splitting is **process-roughness-limited, not
  cleanly $Q$-gated**. Clean damascene-class: single-pole holds at foundry $Q_i$, crosses at
  $Q\approx4\times10^6$ (HWHM criterion $2\gamma\gtrsim\kappa_\mathrm{tot}$; the FWHM convention shifts
  every crossover ×2 — conclusion unchanged under both). Rough subtractive process: **21–75 % of modes
  already split at $Q_i=2\times10^6$**. Consequences (blessed 2026-06-09): the S0.3 substrate carries a
  **roughness-gated CW/CCW doublet knob, default ON except the clean-damascene corner**; PR-4 gains a
  roughness/splitting sub-parameter, **evaluated at the operating $\kappa_\mathrm{ext}$** (overcoupling
  suppresses the visible doublet); if the single-pole substrate relies on the clean corner, PR-4 states
  that assumption explicitly. **Platform tension, recorded:** the best-memory (highest-$Q$) platforms
  are the most splitting-prone, while low-$Q$ CORNERSTONE is splitting-safe but memory-poor (~33 rt).
  B2's quantitative crossovers are **provisional pending F5 primary-source verification** (S0.L,
  before-paper).
- **Registered but not yet modelled (Critic F8 → S0.3/PR-2):** thermal self-heating at operating power;
  pole-placement precision and state-dimension realizability (how many rings, how finely placeable).

## 5. What this feeds

**PR-2** (architecture = the complex-diagonal layer; readout pinned; task sized against 329–4937 rt) ·
**PR-4** ($(\alpha,Q_i)$ + $\kappa_\mathrm{ext}$ policy + roughness/splitting cell — jointly with
D-08-1) · **S0.3** (substrate: gain saturation, ASE, the doublet knob) · **debt #2** (benchmark transfer
of the coupled generalization) · the **white-space claim wording** (B1 trained set; existence search
under PR-15; final wording PR-2/S0.8).
