# §1 — Introduction

**Status:** DRAFT v1 (2026-07-08, single-session mode — not independently reviewed; disclosed).
**Sources of record:** `docs/s0_L/whitespace_claim_wording.md` (W1 = the recommended scope — final
W0-vs-W1 wording choice is the PI's, flagged) · PR-15/15.1 (the two-modality white-space search +
kill-criterion) · `paper/outline.md` claims table · §2–§5 drafts. **Open flags:** [CITE-*] keys resolved via `paper/references.md` (2026-07-12; white-space
refresh folded into §1.1 — Wu/Zhao boundary audits RESOLVED, both clear); a final refresh sweep
re-runs immediately before submission (the claim is time-indexed; 4 page-level reads registered).

---

## 1.1 The gap

Photonic neural networks have learned to train themselves. In feedforward meshes and diffractive
processors, on-chip training is now routine enough to have families: model-free perturbative
methods [CITE-Spall; CITE-SPSA-photonic], hybrid physical-forward/digital-backward methods
[CITE-Wright-2022], and in-situ adjoint methods that read gradients from interference
[CITE-Hughes-2018]. But the systems that most need on-device training — *recurrent* photonic
processors, whose memory lives in the physics — have not received it. Photonic reservoir
computing deliberately avoids the problem: the recurrence is fixed, random, and only a readout is
trained [CITE-reservoir-reviews]. Where internal parameters of a photonic recurrence have been
adjusted at all, it has been by calibration or regime-tuning rather than task-driven training
[CITE-servo-lineage], by reinforcement-style search over a readout while the loop stays fixed
[CITE-Bueno-Brunner], or in systems whose recurrent state is carried digitally between optical
passes [CITE-Boehm-class]. A two-modality literature search with a pre-registered kill-criterion
(§8; supplementary) found no demonstration, by any method, of the following:

> **a continuous-time dissipative-resonator recurrence — pole positions and inter-resonator
> couplings — trained in situ on the physical device by gradient-based or gradient-estimating
> methods on a computational task.**

That sentence is this program's target, with each qualifier load-bearing: *on a computational
task* excludes the servo/calibration lineage; *physical parameters of the recurrence* excludes
hybrid-digital state carriage; *weight-tied recurrence* excludes feedforward meshes folded in
time. A refresh of the search at assembly (2026-07-12; memo in supplementary) confirms the gap
against the strongest 2025–26 neighbors, which we dispatch by name because each is the
"nearest miss" along one qualifier: on-chip all-photonic backpropagation is now demonstrated —
for a *feedforward* network [CITE-Ashtiani-2026]; microring weight banks have been trained in
situ through on-chip optical backprop — as *feedforward* layers [CITE-Zhao-2025]; a
monolithic optical *recurrent* accelerator exists — for inference, training nothing on-device,
with its recurrent state relayed opto-electronically [CITE-Wu-eLight-2025]; a time-synthetic
fiber-loop network trains in situ — with per-step distinct programmed parameters, i.e.
unrolled feedforward rather than a weight-tied recurrence [CITE-time-synthetic]; and an
optoelectronic delay reservoir has had recurrence-defining parameters optimized in situ — by
Bayesian search rather than gradient-based/-estimating training, through a digital feedback
loop [CITE-OERC-insitu]. No coupled-resonator lattice has had its couplings learned on-device
by any method. ▢ [final W0-vs-W1
scope wording: PI decision at S0.8; the search refresh re-runs once more immediately before
submission, with four registered page-level reads (supplementary).]

## 1.2 Why a state-space model, and why silicon nitride

Two developments make this the right moment to close the gap. On the algorithmic side, deep
state-space models showed that *linear* recurrences with well-placed poles — not gated
nonlinear dynamics — carry most of long-sequence performance [CITE-S4; CITE-S4D], and the
oscillatory LinOSS line extended this to second-order units that are exactly coupled damped
oscillators [CITE-LinOSS; CITE-D-LinOSS]. A lattice of coupled microrings *is* such a system:
poles are ring detunings and losses, couplings are physical couplers, and — decisively for
hardware — the LinOSS stability analysis tolerates nonnegative damping, so a lossy-but-high-Q
dissipative lattice is in-regime rather than an approximation to a conservative ideal (§2).
Damping becomes a design knob, not an embarrassment.

On the platform side, the figure of merit for a dissipative ring recurrence is memory per pass —
round-trip loss, hence intrinsic Q. Ultra-low-loss silicon nitride is class-leading and
foundry-accessible ($Q_i$ near $10^7$ on multi-project-wafer runs [CITE-Cui-2023]), thermally
stable enough for the slow thermo-optic actuation that gradient-estimating training wants, and
needs so little gain that the injected amplifier noise stays low (§3). The same choice has a
cost we do not hide: SiN's weak $\chi^{(3)}$ makes the one training route that needs an optical
nonlinearity — Hamiltonian-echo learning, whose echo is phase conjugation — *harder*, not
easier, and §4–§5 treat that honestly rather than idealizing it away.

## 1.3 What this paper does

This is a theory-and-simulation (Stage-0) paper, built to be falsified before it is fabricated.
Its results are gated by a pre-registration ledger — margins, budgets, fairness conventions, and
statistical rules frozen (and PI-signed) before the runs that consume them, with the commit trail
shipped as supplementary material (§3.7). Concretely:

1. **A mapping with a realizable region** (§2): the oscillatory-SSM ↔ coupled-SiN-ring
   correspondence, with the pole region bounded by measured platform numbers, an actuation map
   for {δ, κ_ext, μ}, and the backscatter doublet carried as the model rather than a correction.
2. **A shared dissipative substrate** (§3): saturating Er gain at a registered operating point,
   Langevin ASE at NF 7 dB, three cells from foundry-floor to aspirational, a measured feasible
   box bounded by the lasing crossing, and a measured minimal multi-point input map after
   single-drive controllability was found to collapse (effective dimension ≈3 of 32 rings).
3. **A four-method bake-off under one fairness contract** (§4–§5): SPSA, PAT (with registered
   twin-mismatch), a recurrent in-situ adjoint (charged as if realizable; optimistic bound,
   labelled), and RHEL over a concrete χ³-FWM echo sub-model — scored by device passes to a
   pre-registered target relative to the exact-gradient ceiling, eight seeds, censoring-aware
   statistics.
4. **The result** (§5): both hardware-committed methods train the recurrence to within margin of
   the ceiling on all eight seeds — the sentence in §1.1, demonstrated in simulation at a
   foundry-class noise cell. The ranking (PAT < adjoint < SPSA on device passes; RHEL censored,
   and worse than readout-only under an honest echo) settles the hardware roadmap on PAT/SPSA
   without promotion of the exotic routes. And the comparison the fair design was built to
   expose lands as a null: at 5%-class calibration error, in-situ training buys essentially
   nothing over calibrate-then-deploy — the demonstration stands, the *advantage* claim is
   explicitly not made, and the conditions that would earn it (mismatch, drift, the envelope)
   are named and pre-registered for the next stage (§5.5, §7).
5. **Limits, stated as limits** (§8): robustness is measured against modelled imperfections
   only; the anchor risks, verification debts, and the single-session review period are
   disclosed with the same specificity as the results.

Our position on novelty is deliberately narrow. PAT and SPSA are chip-proven; we do not
re-validate them. What has never existed is a *recurrent, dissipative* photonic system trained
through its own physics — and a demonstration that the recurrence-defining parameters of a
realistic SiN lattice can be so trained, under pre-registered thresholds and honest costing, is
the contribution. Whether it *pays* is a separate question (§7), and this paper reports the
current answer to that question as it falls, not as we might wish it.
