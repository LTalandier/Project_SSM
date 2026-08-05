# §3 — A pre-registered dissipative substrate

**Status:** DRAFT v1 (2026-07-08, single-session mode — not independently reviewed; disclosed).
**Sources of record:** `shared/preregistration.md` PR-4 🔒 v2 (signed 2026-06-13) + PR-6 §B/§C/§D
+ the S0.4-0 calibration addendum · `photonic_ssm/substrate/` (tests 128/128 at freeze) ·
`results/s0_4_0/` · `docs/s0_3/`. Every number is from the signed blocks or their registered
calibration addenda; none originate in this draft. **Open flags:** [CITE-*] keys resolved via `paper/references.md` (2026-07-12; Cui/Er:SiN page-verified, debt-#3 rewording folded in); the C-2 anchor's
geometry-transfer caveat and the §G-conformance anchor-risk (vii) are carried verbatim (§3.6).

---

## 3.1 Why one shared substrate

The bake-off's conclusions are comparisons, and comparisons inherit the honesty of their common
ground. All four training routes therefore run on a *single* simulated substrate — one dynamical
model, one noise model, one parameter partition, one initialization and data convention (PR-6) —
frozen and signed before any estimator existed. Nothing in the substrate was chosen with
knowledge of which method it would favor; the freeze order is auditable in the ledger.

The model is the 2N-mode coupled-mode-theory (CMT) lattice of §2: N rings, each carrying a
clockwise/counter-clockwise doublet (backscatter coupling is always on, §3.4), with the linear
readout followed by direct detection $y(n) = |\sum_j c_j a_j(n)|^2$ — the substrate's only
nonlinearity apart from gain saturation. The trainable (in-situ) partition is fixed by the
architecture freeze (PR-2): per-ring detunings $\delta_j$, per-ring tunable bus couplings
$\kappa_{\text{ext},j}$, and nearest-neighbor inter-ring couplings $\mu_{j,j+1}$ — the parameters
that *define* the recurrence, as opposed to reservoir-style approaches that train only the
readout. The digital head (an 8-lag linear FIR on $y$) and the fixed affine intensity encoder
bracket the photonic core; both are identical across methods, and the head's training cadence is
part of the fairness contract.

## 3.2 Loss, gain, and the operating point

The per-ring net decay is
$\kappa_{\text{net},j} = \kappa_i - g_j + 2\kappa_{\text{ext},j}$: intrinsic loss, minus Er gain,
plus the loading of the through/drop ports. Gain follows the **M1 static-saturated** class: a
per-episode operating point $g(\bar P) = g_0/(1+\bar P/P_\text{sat})$, differentiable in the
drive statistics and in $\kappa_{\text{ext}}$ (the coupling changes the intracavity power the
medium sees), fixed within a rollout — valid under the registered conditions (stationary
within-episode drive statistics, pinned train/test power statistics, quasi-static margin
$E_\text{sym}/E_\text{sat} \sim 10^{-6}$–$10^{-5}$, all [EV]-anchored; bursty inputs void M1).
Every gain-bearing cell runs at the registered ceiling $g_\text{rt} = 0.9\times$ the intrinsic
round-trip loss — gain never compensates port loading — so
$\kappa_\text{net} = 0.1\kappa_i + 2\kappa_\text{ext}$ at the operating point, with the passive
floor ($g=0$) as a labelled sensitivity row. A one-off rate-equation integrator (the salvaged M2)
validated the quasi-static reduction at the gating cells.

Amplified spontaneous emission enters as a continuous Langevin term (convention A2),
$\langle FF^*\rangle = 2\kappa_g n_\text{sp}\,\delta(t{-}t')$ in photon units, discretized
exactly alongside the ZOH/van-Loan propagator, with **fresh draws on every physical pass** —
noise is never shared between passes, methods, or the forward/reverse directions (this single
convention carries much of the fairness burden, and one of RHEL's irreversibility invariants).
The headline noise figure is **NF = 7.0 dB** ($n_\text{sp}=2.5$). The program's original debt
register carried "no measured NF for the flagship Er:Si₃N₄ device" as verification debt #3; the
S0.3-0 substrate reconnaissance (2026-06-10) found that premise false — the full text reports
"a noise figure of ca. 7 dB … at net gain of >20 dB, limited by coupling losses" [CITE-Er-SiN]
— and NF-A = 7.0 dB was frozen *to match that measurement* (re-verified at page level during
assembly, 2026-07-12). The residue of the debt is narrower than its original form: what exists
is a single coupling-loss-limited *system* NF, not an isolated intrinsic amplifier NF, so
NF ∈ {3, 5} remain registered sensitivity values.

## 3.3 The three cells

| cell | platform class | $Q_i$ | N | role |
|---|---|---|---|---|
| C-1 | foundry floor (P-FND) | $2\times10^6$ | 8 | Gate-ii gating cell |
| **C-2** | demonstrated MPW class (P-AN800) | $6.8\times10^6$ | **32** | **bake-off headline** |
| C-3 | aspirational (P-UHQ) | $3\times10^7$ | 128 | labelled sweep axis; never gates |

C-2 is registered as a *conservative bound* on a demonstrated MPW result (3.3 dB/m, mean
$Q_i \approx 10.8$M [CITE-Cui-2023]); our pair ($5.1$ dB/m, $Q_i = 6.8\times10^6$) is strictly
worse than the broadest-linewidth device in that paper's full 249-resonance distribution, whose
figures are independently assessed in an invited peer commentary [CITE-Ye-Marpaung-2023]. The
residual anchor risk is geometry transfer (the demonstrated loss is achieved *by* a wide
multimode Euler-bend racetrack; our registry ring is single-mode) — flagged by the commentary
itself and priced by a registered ×2-loss derate row. At the operating point, C-2 holds ~32
samples of memory at 2 GS/s and packs the 32-ring spectrum in-band; C-1 holds ~9.4 (covering the
task's 7-tap span at the operating point; marginal only at its passive floor).

## 3.4 Backscatter and the doublet

Surface roughness couples the CW/CCW modes at rate $\gamma$ (11.8 MHz at C-2, damascene-clean
process class; 90 MHz at C-1), splitting each ring resonance into a doublet — at high $Q_i$ the
splitting is *resolved*: at C-2/θ₀ the separation clears the §2.4 criterion with
$2\gamma/\kappa_\text{net} \approx 2.4$, and at the S0.4-0 lasing-floor calibration point
(clause (a), $\kappa_\text{net} = 0.05\,\kappa_i$) the ratio reaches
$\gamma/\kappa_\text{net} = 16.6$ — so the substrate is
the full $2N$-mode doublet lattice **always**, not an N-mode idealization with a correction term.
(An earlier draft quoted the floor ratio at θ₀; the operating points are distinct and both are
given here.)
This choice was consequential: the S0.4-0 calibration measured the drive build-up at the lasing
floor to be $\times0.42$ of the hold value — the doublet plus chain hybridization *quench* the
single-pole build-up that two independent prior estimates (×37 and ×91) had presumed, mooting
both. Modelled imperfections cannot be un-modelled by a reviewer; unmodelled ones are the subject
of §8.

## 3.5 The feasible box, the lasing boundary, and the drive budget

The trainable couplings live in a registered box $r_j = \kappa_{\text{ext},j}/\kappa_i \in
[0.1, 3]$ (K4), verified to map into the realizable pole region at every cell. With saturating
gain the box's lower edge is unsafe: below $r^* \approx 0.134$ the ring crosses threshold and the
linear rollout diverges. The operative bound is the S0.4-0-measured
$\mathbf{r_\text{min} = 0.1606}$ (crossing $+$ registered margins), enforced as the training-time
clamp; the θ₀ hold value is $r_0 = 0.3$. Damping, in the D-LinOSS sense, is deliberately *not* a
frozen cell: it is the trainable per-ring net loss the estimators explore through
$\kappa_\text{ext}$ over this box at fixed $g_\text{rt}$ (the R-ii disposition), characterized
separately (§6).

Drive is normalized by an intracavity-energy budget (O2): the registered $\bar P_0 = 1$ mW bus
drive corresponds to $E_0 = 1.069\times10^8$ intracavity photons at θ₀, and the digital encoder
is *not permitted to buy SNR* by rescaling drive power against the registered noise cell — the
budget is held fixed across methods and across the in-situ/offline comparison. The S0.4-0
calibration confirmed the budget is invariant ($1.000000$) under the four-tap input map below.

## 3.6 The measured input map, and what it says about controllability

A single bus port cannot train a 32-ring chain: with drive on ring 1 only, the per-ring gradient
magnitude collapses with hop distance — an effective participating dimension of ≈3 of 32 rings.
The registered remedy is a measured, minimal multi-point input map: S0.4-0 searched tap sets
under a pre-registered every-ring controllability gate (each ring's gradient $\ge 10^{-3}$ of the
maximum, min over five drive seeds) and resolved **B = taps {3, 12, 21, 30}** at $K=4$ (32/32
rings pass, worst $1.42\times10^{-3}$; no $K\le3$ set passes). The four E/O drive channels this
costs are charged to the systems envelope (§7) — multi-point drive raises exactly the
conversion overhead the envelope exists to price. Two protocol rulings made during the
measurement (gate referenced to the maximum ring; min-over-seeds robustness) both strengthen the
gate and are recorded for review. One anchor risk stays open (vii): the calibration's floor
numbers are computed on-resonance; a detuned ring at $r_\text{min}$ can reach
$\kappa_\text{net} = -0.48\kappa_i$ under worst-case de-saturation, and a δ-aware floor would sit
at $0.2547$ — the conformance check that would settle it was measured to be not-cheap and is
carried as a labelled risk, not silently absorbed. A pre-registered endpoint diagnostic
(PR-18; S0.11) later measured the label against the trained solutions themselves: under the
same δ-aware hypothetical, three of eight SPSA seeds end with at least one ring in the
super-threshold corner (min $\kappa_\text{net} = -0.06\,\kappa_i$; rings at $r = 0.17$–$0.22$
with $|\delta| = 0.65$–$1.0\,\kappa_i$), while PAT's endpoints stay sub-threshold
($+0.31\,\kappa_i$ at achieved detunings) and both §6 arms sit far from the corner
($\geq +1.3\,\kappa_i$). The exposure lives in the hypothetical, not the runs (the as-built
substrate is δ-independent in gain and never lases, and the measured doublet quench of §3.4
suggests the single-pole build-up it assumes is pessimistic) — but the label is no longer
vacuous, and every exposed endpoint sits below the δ-aware clamp $r \approx 0.2547$, which is
therefore the concrete mitigation Stage 1 inherits. Mid-training trajectories are not stored;
the measurement binds endpoints only.

## 3.7 The ledger as method

Every consequential choice above — the gain class and its validity conditions, the NF axis, the
cells, the box, the clamp, the input map, the drive budget — was written into a pre-registration
ledger, in most cases signed by the PI, *before* the run that consumed it, with measured
deferrals returned to the ledger as dated addenda (the $E_0$ value, $r_\text{min}$, the resolved
input map, the budget $B$, the BPTT ceiling). Supersessions retain the superseded text. The
ledger, its review trail (independent adversarial review through 2026-07-06; single-session
self-review thereafter, disclosed), and the frozen-before-run commit hashes ship as
supplementary material. We treat this as part of the method: a bake-off whose thresholds,
budgets, and fairness conventions are set after seeing results would not support the claims of
§5.
