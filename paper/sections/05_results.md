# §5 — The bake-off: which routes train the recurrence, and at what cost

**Status:** DRAFT v1 (2026-07-08, single-session mode — Critic suspended since 2026-07-07; this
draft is NOT independently reviewed and the paper's methods note must disclose the single-session
period). **Sources of record:** `shared/preregistration.md` (PR-3/6/7/8/9 blocks + the two
S0.4-close addenda, all committed before the runs they govern) · `results/s0_5/bakeoff.md` +
`bakeoff.json` + `bakeoff_diag_c1.json` + `ceiling.json` + `sizing.json` ·
`shared/results_log.md` (S0.4a/b/c, S0.5-core) · `docs/s0_4/f8_hardware_ledger.md`. Every number
below is from those frozen artifacts; none originate in this draft. **Open flags:** [CITE-*]
placeholders; C-2 mismatch-sensitivity, damping (§6), and the full envelope (§7) are S0.5-full /
S0.6 / S0.7 rows, marked ▢ where they belong.

---

## 5.1 Pre-registration and the reference ceiling

Every threshold in this section was fixed in the ledger *before* the run it judges, in the order
the runs consumed them: the fairness contract, cost metric, and twin-mismatch families (PR-6/7/5)
at the start of S0.4; the target rule, statistical plan, and gate semantics (PR-3/8/9) at
S0.4-close; and the two measured numbers a rule cannot supply — the budget and the ceiling — as
dated addenda committed before any contestant ran. We state this not as ceremony but because the
central claim is a *threshold-crossing* claim, and a threshold chosen after seeing the curve is
worthless.

The reference is backpropagation-through-time on the substrate itself (BPTT), which is not a
physical training method — it reads gradients the device cannot expose — but bounds what the
task admits at this cell. On the headline cell (C-2: 32 rings, $Q_i = 6.8\times10^6$; 4-PAM
channel equalization at 28 dB, §3), BPTT drives the symbol-error rate to a median of
$5.2\times10^{-4}$ across eight seeds (seven of eight at $5\times10^{-4}$ — two errors in the
3840-symbol evaluation set, the quantization floor). **The frozen substrate has ample capacity
for the task; the open question is purely which physical training routes reach it, and at what
cost.** The pre-registered target follows mechanically: a method *reaches target* if its
held-out SER falls to $\text{SER}_\text{target} = 1.25\times\text{ceiling} + 0.005 = 5.65\times
10^{-3}$ at any evaluation point within the device-pass budget (the additive guard dominates at a
floor-level ceiling, by design — PR-3 §B). The budget $B = 252{,}800$ device passes is twice the
BPTT convergence point measured in a seed-7 sizing pilot excluded from the eight scored seeds.

A note this cell settles for free: the ceiling is *identical* under fixed-gain and saturating-gain
substrate models ($\Delta_{M3}=0$). The gain-model class — the largest modelling uncertainty in
the substrate (§3) — cannot move the achievable accuracy, so it cannot flip any ranking below.
The pre-registered M3 sensitivity trigger is therefore un-triggerable at this cell.

## 5.2 Gate ii: the recurrence trains on the device

Two decompositions of the Stage-0 gate were pre-registered (PR-9). **Capacity (ii-a):** the
ceiling must clear a task-utility floor set at half the readout-only error — the reservoir
baseline that freezes the recurrence and trains only the digital head. It clears it by
$21.5\times$ ($5.2\times10^{-4}$ vs the reservoir's $2.2\times10^{-2}$). **Trainability (ii-b):**
at least one of the two hardware-committed routes — physics-aware training (PAT) or SPSA — must
reach target on at least five of eight seeds.

**Both reach target on all eight.** This is the load-bearing result of the program: the
parameters that *define* the recurrence — the per-ring detunings, the tunable ring–bus couplings,
and the inter-ring couplings $\{\delta_j, \kappa_{\text{ext},j}, \mu_{jk}\}$ — are trained on the
(simulated) physical substrate, through physical-operation-only gradient methods with fresh
injected noise on every pass, to within the pre-registered margin of the exact-gradient ceiling.
To our knowledge this is the first demonstration, by any method, of a recurrent photonic system
whose recurrence-internal parameters are updated by on-device gradient-based or gradient-estimating
training (the white-space claim, §1; [CITE-whitespace-lanes]).

## 5.3 The ranking: sample-efficiency at matched device-pass cost

The primary metric is sample-efficiency: device passes to reach target, one physical pass being
one sequence through the substrate in any direction (PR-7). Ranked lexicographically by success
fraction then median passes (PR-8), with the digital-compute side-ledger co-reported but never
folded into the rank:

| route | success | median device passes → target | final SER (median) | digital ledger |
|---|---|---|---|---|
| **PAT** (twin-backward) | 8/8 | **38,400** | $8\times10^{-4}$ | 505,600 |
| **adjoint** (physical reverse pass) | 8/8 | 73,600 | $5\times10^{-4}$ | 0 |
| **SPSA** (model-free) | 8/8 | 176,000 | $1.3\times10^{-3}$ | 0 |
| **RHEL** (Hamiltonian echo) | 0/8 | censored at $B$ | $1.4\times10^{-1}$ | 0 |

All three ordered pairs among the passing routes separate with paired-by-seed bootstrap 95%
confidence intervals excluding zero (PAT−SPSA $=-137{,}600$ passes, CI $[-155{,}200,-123{,}200]$;
adjoint−PAT $=+35{,}200$, CI $[+35{,}200,+36{,}800]$; adjoint−SPSA $=-102{,}400$, CI
$[-120{,}000,-88{,}000]$). The three routes trade the same axes the theory predicts they should.
**PAT** is cheapest on the physical device but spends a $13\times$-larger digital ledger and
carries the full burden of characterizing a differentiable twin (§4, F8). **The adjoint** matches
the exact-gradient ceiling in accuracy at zero digital cost and $1.9\times$ PAT's device passes —
though its count charges one physical reverse pass *as if* realizable, which no recurrent photonic
system has yet demonstrated (a caveat we quarantine, §4). **SPSA** costs $4.6\times$ PAT's device
passes but needs no model, no twin, and no added hardware — the simplicity anchor of the Stage-1
plan.

No route earns promotion toward a later hardware slot (PR-9): the adjoint beats SPSA but loses to
PAT on device passes, and clearing the bar requires clearly beating *both* workhorses. The
hardware roadmap therefore stays on PAT and SPSA — the outcome the guardrail was built to protect,
now settled by data rather than assertion.

## 5.4 RHEL under an honest echo

The fourth route, recurrent Hamiltonian echo learning (RHEL), is the one whose physical primitive
SiN is least suited to supply. Rather than an idealized conjugation operator, we model the echo as
a concrete $\chi^{(3)}$ four-wave-mixing phase-conjugation stage with its measured penalty chain —
extraction, single-pass spiral conversion at 0.3 W pump, timing decay — totalling $-22.4$ dB per
conjugation, plus the phase-insensitive parametric noise floor (§4, PR-11; [CITE-SiN-FWM]).

RHEL does not reach target on any seed; its final SER of $0.14$ is *worse than the readout-only
baseline* (a $+0.118$ readout differential). Two controls locate the cause. A floor check confirms
the estimator is correct: as the substrate is made progressively less dissipative, the RHEL
gradient converges to the exact reference (direction cosine $\to 1.0000$) — the non-dissipative
limit RHEL's theorem assumes. And an idealized-conjugator control at the smaller C-1 cell — a
*perfect* echo, no conjugation loss or noise — *does* reach target ($5.7\times10^{-3} \le
7.3\times10^{-3}$). So the failure at the headline cell is neither broken mechanics nor the
conjugation chain: it is dissipative-echo bias, the irreducible mismatch between an echo that
assumes time-reversal and a substrate that forgets its state within roughly nine of the
sequence's steps. This is the honest instantiation of the platform argument (§1, §5.4 of the
proposal): silicon nitride's low loss improves RHEL's *noise* budget, but the *dissipation* the
recurrence itself requires is fatal to the echo at the operating point. RHEL-on-SiN stays a
simulation result.

## 5.5 The comparison the fair design was built to expose

One baseline result is more consequential for the program than the ranking. The
offline-train-then-deploy route — train the full parameter set digitally on a designer's model,
then deploy through actuation maps, recalibrating only the digital head on-device — was given the
*same* 5%-class calibration errors as PAT's twin (the mismatch families are drawn from one frozen
set, so the comparison cannot be rigged by giving in-situ training a secretly-wronger competitor;
PR-5 F7.3). At that mismatch level it reaches $1.0\times10^{-3}$ — statistically
indistinguishable from in-situ PAT's $8\times10^{-4}$.

We state the consequence plainly, because the fair-comparison design exists precisely to force it:
**at 5% calibration accuracy on this task, training in situ buys essentially nothing over
calibrate-then-deploy.** The demonstration claim — the first on-device-trained recurrent photonic
recurrence — stands regardless; it is a claim about *what was done*, not about beating an
alternative. But any claim that in-situ training is *advantageous* is not in evidence at this
mismatch level, and this paper does not make one. The conditions under which the advantage would
appear — larger or unknown calibration error, drift over a deployment lifetime (unmodelled here),
or the systems envelope — are named as open, and two of them are pre-registered sensitivity axes
for the next stage (PR-5 mismatch rows; §6–§7). Reporting a null advantage where the design was
built to detect one is the honest core of the result, not a hedge around it.

## 5.6 What the diagnostics add

Two mechanism rows, at three seeds each on C-1, support the mismatch narrative without inflating
it. Decomposing PAT's twin mismatch — perfect twin, parametric-error twin, structural-omission
twin (dropping the gain self-consistency channel) — all three reach the C-1 ceiling identically:
PAT absorbs both mismatch families at this cell. We flag explicitly that this does **not**
extrapolate to C-2, where the dropped gain channel was measured to carry ~8% of the gradient
direction (§4, the adjoint cosine dropping from 0.994 to 0.925 with cell size); the C-2 mismatch
sensitivity is a Stage-0.5-full measurement, not an inference from C-1. And the idealized-RHEL row
is the control cited in §5.4. Neither row is a headline; both are the pre-registered controls that
let the headlines mean what they say.

## 5.7 Controllability and effective dimension ▢

▢ *To draft from S0.4-0 (`results/s0_4_0/`, the resolved input map + participation profile).*
The single-drive substrate has an effective participating dimension of ≈3 of 32 rings (the
gradient-magnitude profile decays steeply from the drive); the resolved four-tap input map
$\{3,12,21,30\}$ raises every ring's gradient above the pre-registered $10^{-3}$ controllability
threshold (32/32, worst $1.42\times10^{-3}$, min over five drive seeds). This is claim C6 and the
in-data form of the debt-#1 reservoir falsifier: it is *why* the readout-only baseline is weak and
*why* the multi-tap drive is required — at the cost of four E/O channels charged to the envelope
(§7). The strict every-ring gate and the min-over-seeds robustness protocol are the two S0.4-0
rulings flagged for review.

## 5.8 Secondary diagnostic (appendix-grade) ▢

▢ *PR-14 bias/variance of the gradient estimate vs the BPTT reference.* Registered as a secondary
diagnostic only — never the headline, since gradient-direction agreement structurally flatters the
exact methods (adjoint, RHEL) and penalizes SPSA, whose poor per-step alignment averages to good
convergence. Deferred to S0.5-full; belongs in an appendix, not this section's argument.
