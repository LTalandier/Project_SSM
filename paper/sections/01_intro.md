# §1 — Introduction

**Status:** DRAFT v3 (2026-07-27, single-session mode — not independently reviewed; disclosed).
**Scope ruling:** **W1 only** — re-ruled 2026-07-27 under the same standing delegation after the
registered Wu eLight page-level read REFUTED the prior clearance (its ORNN chip is SPGD-trained
in situ → W0's broad form is attacked; W1 survives cleanly, Wu cited as nearest neighbor).
Supersedes the 2026-07-26 W0-in-prose ruling; memo `docs/s0_L/whitespace_page_reads_2026-07-27.md`.
**Sources of record:** `docs/s0_L/whitespace_claim_wording.md` · PR-15/15.1 (the two-modality white-space search +
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
processors, whose memory lives in the physics — have barely begun to receive it. Photonic reservoir
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
time. Refreshes of the search at assembly (2026-07-12) and a page-level verification round
(2026-07-27), followed by primary-source checks and a bounded search on
2026-09-13 (memos in supplementary), map the boundary against the strongest 2025–26 neighbors,
which we dispatch by name because each is the "nearest miss" along one qualifier — and one of
them moved the boundary. The **nearest neighbor** is the monolithic optical recurrent
accelerator of Wu et al. [CITE-Wu-eLight-2025]: its ORNN chip *is* trained in situ, by a
model-free perturbative method (SPGD, two physical evaluations per update) on a classification
task, with a weight-tied mesh applied across wavelength-encoded time steps — to our knowledge
the first in-situ-trained optical recurrent network of any kind, and we cite it as such. What
it does not do is train the parameters in the boxed sentence: its trained weights are
interferometer-mesh voltages, its recurrent state is re-generated electronically at every step
through a photodetector–modulator relay, and its resonators are calibrated once and held
static — the continuous-time dissipative-resonator recurrence, whose *poles and couplings are
themselves the memory*, remains untrained. The remaining near-misses each fall along one
qualifier: on-chip all-photonic backpropagation is now demonstrated — for a *feedforward*
network [CITE-Ashtiani-2026]; microring weight banks have been trained in situ through on-chip
optical backprop — as *feedforward* layers [CITE-Zhao-2025]; a time-synthetic fiber-loop
network trains in situ — with per-step distinct programmed parameters, i.e. unrolled
feedforward rather than a weight-tied recurrence [CITE-time-synthetic]; a
modulation-and-weighting microring array trains weights sitting *inside* an analog recurrent
loop on-device — by particle-swarm search, explicitly without gradients
[CITE-Zhang-eLight-2026]; an optoelectronic delay reservoir has had recurrence-defining
parameters optimized in situ — by Bayesian search, through a digital feedback loop
[CITE-OERC-insitu]; and a silicon photonic reservoir equalizer is "trained in hardware" — its
readout only, by an evolution strategy, the reservoir couplings fixed by fabrication
[CITE-spatial-RC]. No coupled-resonator lattice has had its couplings learned on-device by any
method. (The claim is time-indexed: the search refresh re-runs once more immediately before
submission, with the registered page-level reads listed in supplementary.)

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
   expose shows no resolved calibration difference at five levels spanning
   5–30%-class error after the corrected binding rerun (§5.5), and no advantage
   under common-mode drift, which a laser re-lock absorbs — while under uncorrelated per-ring drift, which a global laser re-lock cannot absorb,
   in-situ retraining holds a **declared, pre-registered 2.42× advantage** (both conditions
   of the frozen rule hold — point ratio ≥ 2× *and* difference-CI excluding zero; the
   coarse-floor estimate 1.84× is co-reported), a gap that grows with accumulated drift
   (§5.5, §7).
5. **Limits, stated as limits** (§8): robustness is measured against modelled imperfections
   only; the anchor risks, verification debts, and the single-session review period are
   disclosed with the same specificity as the results.

Our contribution is a simulation test of training the pole positions and couplings
that define a dissipative SiN memory lattice, under registered thresholds and
explicit cost accounting. PAT and SPSA have prior chip demonstrations; the
literature distinction is the specific recurrence in §1.1. A physical demonstration
of this architecture remains future work. Its systems value is assessed separately
in §7, including the negative inline follow-up.
