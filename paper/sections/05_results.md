# §5 — The bake-off: which routes train the recurrence, and at what cost

**Status:** DRAFT v1 (2026-07-08, single-session mode — Critic suspended since 2026-07-07; this
draft is NOT independently reviewed and the paper's methods note must disclose the single-session
period). **Sources of record:** `shared/preregistration.md` (PR-3/6/7/8/9 blocks + the two
S0.4-close addenda, all committed before the runs they govern) · `results/s0_5/bakeoff.md` +
`bakeoff.json` + `bakeoff_diag_c1.json` + `ceiling.json` + `sizing.json` ·
`shared/results_log.md` (S0.4a/b/c, S0.5-core) · `docs/s0_4/f8_hardware_ledger.md`. Every number
below is from those frozen artifacts; none originate in this draft. **Open flags:** [CITE-*] keys resolved via `paper/references.md`; figures F3–F5 made
(`paper/figures/`); C-2 mismatch-sensitivity and PR-14 are S0.5-full rows, marked where they
belong (§5.6, §5.8).

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
3840-symbol evaluation set, the quantization floor). Because that floor is too coarse for
comparisons *between* near-ceiling arms — a two-symbol band can manufacture or erase a
"statistically real" difference — every such comparison in this section (§5.5, §5.6) was
re-scored under a pre-registered fine protocol (**eval-F**, PR-17: the same reserved held-out
streams extended to 99,840 scored symbols, per-seed resolution $1.0\times10^{-5}$), with the
frozen coarse protocol remaining the protocol of record for every gate, target, and ranking
verdict, and both reported wherever they differ. At eval-F the BPTT reference itself settles at
$9.8\times10^{-4}$ (the coarse $5.2\times10^{-4}$ was a lucky-two-errors reading — an
illustration of exactly the floor hazard). One implementation erratum in the eval-F tooling
(an evaluation-normalization inconsistency, caught the same day by its chance-level signature,
registered, fixed under a machine-precision gate test, and re-run) is documented in the ledger
(PR-17 §17.7). **The frozen substrate has ample capacity
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
To our knowledge this is the first demonstration — **in simulation, on a pre-registered
realistic substrate model** — of a continuous-time dissipative-resonator recurrence whose poles
and couplings are updated by device-protocol gradient-based or gradient-estimating training
(the white-space claim, §1; [CITE-whitespace-lanes]). The on-chip counterpart does not exist
yet; it is what Stage 1 is designed to earn (§9), and every use of "demonstration" in this
paper carries this qualifier.

## 5.3 The ranking: sample-efficiency at matched device-pass cost

The primary metric is sample-efficiency: device passes to reach target, one physical pass being
one sequence through the substrate in any direction (PR-7). Ranked lexicographically by success
fraction then median passes (PR-8), with the digital-compute side-ledger co-reported but never
folded into the rank:

| route | success | median device passes → target | final SER (median) | digital ledger |
|---|---|---|---|---|
| **PAT** (twin-backward) | 8/8 | **38,400** | $8\times10^{-4}$ | 505,600 |
| **adjoint**† (physical reverse pass) | 8/8 | 73,600 | $5\times10^{-4}$ | 0 |
| **SPSA** (model-free) | 8/8 | 176,000 | $1.3\times10^{-3}$ | 0 |
| **RHEL**‡ (Hamiltonian echo) | 0/8 | censored at $B$ | $1.4\times10^{-1}$ | 0 |

† *Charged as-if-realizable: no recurrent physical reverse pass has been demonstrated on any
platform (debt #4, §8.2); this row is an optimistic bound on a hypothetical implementation and
competes with chip-proven routes only in that idealized sense (§4).* ‡ *Reported as a measured
feasibility bound on echo learning in dissipative substrates, not as a competitive entry —
see §5.4.*

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

## 5.4 RHEL: a feasibility bound on echo learning in dissipative substrates

The fourth route, recurrent Hamiltonian echo learning (RHEL), is best read not as a contestant
but as a *measured feasibility bound* — and we say plainly that its headline outcome was
foreseeable in direction, if not in magnitude, before the run: the theorem behind the echo
assumes a non-dissipative system, and the registered operating point sits at
$\kappa_\text{net} T\, dt \approx 27$, two orders beyond the $\lesssim 0.1$ regime where our
own recovery curve shows the update aligning with the true gradient (Fig. S5). What the
bake-off adds is the *quantified boundary* — where echo learning breaks on a dissipative
substrate, by how much, and through which mechanism — under the same fairness contract as the
routes that pass; that, not a horse race it could not win, is the result we consider citable.
RHEL is also the route whose physical primitive SiN is least suited to supply. Rather than an
idealized conjugation operator, we model the echo as a concrete $\chi^{(3)}$ four-wave-mixing
phase-conjugation stage with its measured penalty chain — extraction, single-pass spiral
conversion at 0.3 W pump, timing decay — totalling $-22.4$ dB per conjugation, plus the
phase-insensitive parametric noise floor (§4, PR-11; [CITE-SiN-FWM]).

RHEL does not reach target on any seed; its final SER of $0.14$ is *worse than the readout-only
baseline* (a $+0.118$ readout differential). Two controls locate the cause. A floor check confirms
the estimator is correct: as the substrate is made progressively less dissipative, the RHEL
gradient converges to the exact reference (direction cosine $\to 1.0000$; Fig. S5) — the non-dissipative
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
calibrate-then-deploy.** The demonstration claim — the first dissipative-resonator recurrence
whose poles and couplings train on-device — stands regardless; it is a claim about *what was
done*, not about beating an
alternative. The question this raises — *under what conditions does the advantage appear?* — we
then answered with two pre-registered follow-up experiments rather than leaving it open (PR-5 §E,
PR-16; both frozen before the runs).

**Calibration accuracy is not the axis** (Fig. F8a). Sweeping the shared mismatch level from 5% to 30%-class
(in-situ and offline drawing from one frozen family at every level, §5.1), the two arms are —
at the eval-F floor — statistically indistinguishable at *every* level: in-situ holds at
$8.4$–$8.6\times10^{-4}$, offline at $8.7$–$9.0\times10^{-4}$ (ratio $\le 1.05$, every
paired-bootstrap CI including zero), and offline *never fails the accuracy target*. The
coarse-floor reading had shown small "statistically real" differences (CI excluding zero up to
20%) — a floor artifact that dissolves at 26× resolution, which is precisely why the fine
protocol was registered. On this task the offline arm's on-device head recalibration absorbs
static parametric error completely: a wrong recurrence with a well-fit head still equalizes,
and in-situ *recurrence* training does not earn its keep against calibration error at any
tested magnitude.

**Drift is the axis — specifically the part a re-lock cannot catch** (Fig. F8b,c). We then let the substrate
*drift*: a random walk on the ring detunings calibrated to a measured free-running silicon-nitride
resonance drift ($\approx 341$ MHz over 24 h $\approx 24\,\kappa_i$ at C-2 [CITE-Dacha-2025]),
deployed after convergence, with each arm allowed its on-device response — offline recalibrates the
head and re-locks the laser (a single global detuning re-centering); in-situ retrains the
recurrence. The pre-registered contrast holds cleanly, and at the eval-F protocol of record the
verdict is now formal. Under **common-mode** drift (whole-chip thermal wander) the laser
re-lock absorbs it and offline keeps pace ($0.98$ vs $0.73\times10^{-3}$ time-integrated,
ratio $1.34$, CI including zero — no advantage). Under **independent** per-ring drift the
re-lock *cannot* fix the scrambled pole scatter, and in-situ retraining pulls ahead:
$0.82\times10^{-3}$ versus the re-locking offline's $1.98\times10^{-3}$ time-integrated — a
$\mathbf{2.42\times}$ separation with paired-bootstrap CI $[+0.71, +2.84]\times10^{-3}$
excluding zero, **clearing the pre-registered $2\times$ advantage threshold: this is the one
comparison in the paper where in-situ training formally beats the strong offline baseline.**
Per the both-protocols rule (PR-17 §17.3) we co-report that the coarse-floor estimate of the
same quantity was $1.84\times$ — *below* the bar; the finer floor did not manufacture the
effect (the trajectories are the same data) but resolved the offline degradation that
two-symbol granularity had been compressing. The gap *grows with accumulated drift* (~3–4× at
the largest drift step), exactly as the mechanism predicts. Two protocol notes for honesty:
the in-situ SPSA arm is plotted for context only — its per-step re-convergence transient
(and, within eval-F, a registered per-step scale-re-measure convention that penalizes an arm
whose couplings move during the step) inflate its early trajectory, and no registered verdict
involves it; and the deploy-time $\mathrm{SER}(t{=}0)$ diagnostic of the in-situ arms shares
that convention and is not used in any comparison.

The section's shape is now a mechanism triple, each leg pre-registered: calibration error —
null, to 30% (the head absorbs it); common-mode drift — null (the re-lock absorbs it);
uncorrelated per-ring drift — a declared $2.42\times$ advantage (nothing else can absorb it).
In-situ training's value on this substrate is not calibration robustness; it is tracking the
drift a laser lock cannot see — and quantifying *how uncorrelated real on-chip drift is*
becomes the sharpest Stage-1 measurement (§9).

## 5.6 What the diagnostics add

Two mechanism rows, at three seeds each on C-1, support the mismatch narrative without inflating
it (Fig. S2; eval-F). Decomposing PAT's twin mismatch — perfect twin, parametric-error twin,
structural-omission twin (dropping the gain self-consistency channel) — the perfect and
M-struct twins land identically ($1.11\times10^{-3}$), and the fine floor resolves a small
M-par excess ($1.31\times10^{-3}$, +18% relative — invisible at the coarse floor, where all
three had read as one number): PAT absorbs the structural omission completely and the
parametric family almost completely at this cell. We flag explicitly that this does **not**
extrapolate to C-2, where the dropped gain channel was measured to carry ~8% of the gradient
direction (§4, the adjoint cosine dropping from 0.994 to 0.925 with cell size); the C-2 mismatch
sensitivity is a Stage-0.5-full measurement, not an inference from C-1. The idealized-RHEL row
is the control cited in §5.4 — at eval-F it still clears the C-1 target, barely
($7.2\times10^{-3} \le 7.3\times10^{-3}$), which we note because a two-symbol coarse floor
could not have resolved how thin that margin is. Neither row is a headline; both are the
pre-registered controls that let the headlines mean what they say.

## 5.7 Controllability: what "N = 32" actually means

The bake-off's cell label understates a constraint that any hardware implementation inherits, so
we report it as a first-class result (Fig. F3). Under a single input tap, the per-ring gradient
magnitude collapses geometrically with distance from the drive — by ring 32 it sits some
twenty-five orders of magnitude below the maximum — and the *participation profile* (settled
per-ring amplitude relative to the maximum) counts only $\{1, 3, 5\}$ of 32 rings above
$\{10^{-1}, 10^{-2}, 10^{-3}\}$. A nominally 32-ring lattice driven at one port is, effectively,
a three-ring computer with 29 passengers. This is the in-data form of the program's
reservoir-falsifier: it is *why* the readout-only baseline stalls at $2.2\times10^{-2}$ (§5.2),
and it is a controllability property of the chain physics, not of any training method.

The pre-registered remedy is a measured, minimal input map: the smallest tap set (capped at
$K = 4$) under which *every* ring's gradient clears $10^{-3}$ of the maximum. The resolved map,
taps $\{3, 12, 21, 30\}$, clears the gate for all 32 rings with worst ratio $1.42\times10^{-3}$
— taken as a *minimum over five drive realizations*, because single-seed margins at the gate
boundary flicker by a factor of ~20. No three-tap set clears (best: 24 of 32), and the
registered starting guess $\{1, 9, 17, 25\}$ was not the winner (28 of 32 — its worst ring sat
seven hops from a tap). Under the resolved map the participation counts rise to
$\{4, 26, 32\}$, and every use of "$N = 32$" in this paper carries that measured profile rather
than the nominal dimension. Two protocol rulings made during resolution are on record: the
gate references the *maximum-gradient* ring (the registered ring-1 reference is gameable when
ring 1 is untapped), and robustness binds on the min-over-seeds. Both strengthen the gate; both
were adopted before the finalists were evaluated. The price of controllability is charged
honestly where it lands: four drive E/O channels instead of one, priced in the systems envelope
(§7) — trainability of the deep lattice is bought with exactly the conversion overhead the
advantage question (§7.4) must then carry.

## 5.8 Secondary diagnostic (registered, deferred)

PR-14 — the bias/variance decomposition of each estimator's gradient against the BPTT reference
— is registered as a secondary diagnostic only and was not run in the core bake-off; it is a
Stage-0.5-full row. The reason it is secondary is structural: gradient-direction agreement
flatters the exact methods (adjoint, RHEL) and penalizes SPSA, whose per-step alignment is poor
by construction while its *averaged* trajectory converges (§5.3) — scoring on cosine alone would
have reproduced the known failure mode of ranking estimators by a proxy the task does not pay
for. The fragments that exist (the adjoint's 0.994/0.925 cell-dependent cosine, §5.6; RHEL's
non-dissipative-limit recovery, §5.4) are reported where they carry mechanistic weight, and the
full decomposition belongs in an appendix when the S0.5-full rows run.
