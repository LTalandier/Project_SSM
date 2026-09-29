# §3 — A pre-registered dissipative substrate

**Status:** v2, condensed 2026-09-29 for the first public deposit (v1 at commit `a508a28`).
Calibration history and anchor-risk (vii) endpoint detail moved to supplementary N9.2.

---

## 3.1 Why one shared substrate

The bake-off's conclusions are comparisons, so all four training routes run on a *single*
simulated substrate — one dynamical model, noise model, parameter partition, initialization and
data convention (PR-6) — frozen before any estimator existed. The model is the 2N-mode
coupled-mode lattice of §2: N rings, each a clockwise/counter-clockwise doublet, read by direct
detection $y(n) = |\sum_j c_j a_j(n)|^2$, the only nonlinearity besides gain saturation. The
trainable partition (PR-2) is the per-ring detunings $\delta_j$, per-ring bus couplings
$\kappa_{\text{ext},j}$ and nearest-neighbor couplings $\mu_{j,j+1}$. A digital head (an 8-lag
linear FIR on $y$) and a fixed affine intensity encoder bracket the photonic core; both are
identical across methods.

## 3.2 Loss, gain, and noise

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
value for the flagship Er:Si₃N₄ amplifier, "ca. 7 dB … limited by coupling losses" [CITE-Er-SiN].
That is a system NF, not an isolated intrinsic one, so NF ∈ {3, 5} remain sensitivity values.

## 3.3 The three cells

| cell | platform class | $Q_i$ | N | role |
|---|---|---|---|---|
| C-1 | foundry floor (P-FND) | $2\times10^6$ | 8 | Gate-ii gating cell |
| **C-2** | demonstrated MPW class (P-AN800) | $6.8\times10^6$ | **32** | **bake-off headline** |
| C-3 | aspirational (P-UHQ) | $3\times10^7$ | 128 | labelled sweep axis; never gates |

C-2 is a conservative bound on a demonstrated multi-project-wafer result (3.3 dB/m, mean
$Q_i \approx 10.8$M [CITE-Cui-2023], independently assessed in [CITE-Ye-Marpaung-2023]): our
5.1 dB/m and $Q_i = 6.8\times10^6$ are worse than the broadest-linewidth device in that paper's
249-resonance distribution. The residual risk is geometry transfer, since the demonstrated loss
comes from a wide multimode racetrack and our ring is single-mode; a registered ×2-loss derate row
prices it. At the operating point C-2 holds ~32 samples of memory at 2 GS/s, and C-1 holds ~9.4,
covering the task's 7-tap span at the operating point and marginal only at its passive floor.

## 3.4 Backscatter and the doublet

Roughness couples the clockwise and counter-clockwise modes at $\gamma$ = 11.8 MHz at C-2
(damascene-clean class) and 90 MHz at C-1. At the C-2 initialization $2\gamma/\kappa_\text{net}
\approx 2.4$, so the doublet is resolved, and the substrate is always the full $2N$-mode lattice
rather than an $N$-mode idealization. This mattered: calibration measured the drive build-up at
the lasing floor at ×0.42 of the hold value, the doublet and chain hybridization quenching the
single-pole build-up that two earlier estimates (×37 and ×91) had assumed.

## 3.5 The feasible box and the drive budget

The trainable couplings live in a registered box $r_j = \kappa_{\text{ext},j}/\kappa_i \in
[0.1, 3]$. With saturating gain, a ring below $r^* \approx 0.134$ crosses threshold and the linear
rollout diverges, so the training clamp is the measured $\mathbf{r_\text{min} = 0.1606}$ (crossing
plus registered margins); the initialization is $r_0 = 0.3$. Damping in the D-LinOSS sense is not
a frozen cell: it is the trainable per-ring net loss explored through $\kappa_\text{ext}$ at fixed
$g_\text{rt}$ (§6). Drive is normalized by an intracavity-energy budget: the registered
$\bar P_0 = 1$ mW bus drive corresponds to $E_0 = 1.069\times10^8$ intracavity photons at the
initialization θ₀, held fixed across methods and across the in-situ/offline comparison so that the
encoder cannot buy SNR.

## 3.6 The measured input map

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

## 3.7 The ledger as method

Every choice above — the gain class and its validity conditions, the NF axis, the cells, the box,
the clamp, the input map, the drive budget — was written into a pre-registration ledger before the
run that consumed it, in most cases signed by the PI, with measured quantities ($E_0$,
$r_\text{min}$, the input map, the budget, the reference) returned as dated addenda. Superseded
text is retained. The ledger and the registration-to-run commit table accompany the paper
(supplementary N1, N4). A bake-off whose thresholds were set after seeing results would not
support the claims of §5.
