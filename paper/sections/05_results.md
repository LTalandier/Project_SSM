# §5 — The bake-off: which routes train the recurrence, and at what cost

**Status:** v2, condensed 2026-09-29 for the first public deposit (v1 at commit `a508a28`).
Reference-scope, interval, drift-provenance and at-solution detail moved to supplementary N9.4–N9.6.

---

## 5.1 Pre-registration and the reference

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

## 5.2 Gate ii: the recurrence trains on the device

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
gradient-based or gradient-estimating training [CITE-whitespace-lanes]. The on-chip counterpart
does not exist yet, and every use of "demonstration" in this paper carries this qualifier.

## 5.3 The ranking: sample efficiency at matched device-pass cost

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

## 5.4 RHEL: a feasibility bound on echo learning in dissipative substrates

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

## 5.5 The comparison the fair design was built to expose

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
resonance drift ($\approx 341$ MHz over 24 h $\approx 24\,\kappa_i$ at C-2 [CITE-Dacha-2025]). The
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

## 5.6 What the diagnostics add

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

## 5.7 Controllability: what "N = 32" actually means

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
