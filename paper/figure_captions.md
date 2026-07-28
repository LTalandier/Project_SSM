# Figure captions (P1)

**Status:** DRAFT v1 (2026-07-27, single-session mode). One caption per made figure
(F1–F8 main, S1–S3/S5 supplementary). Numbers are restatements of the frozen results the
figures are generated from (`analysis/make_figures.py`, `analysis/make_sfigures.py`); nothing
originates here. Figure "Fn" labels are figure numbers, distinct from finding-IDs.

---

**Figure F1 — Architecture and realizable pole region.** (a) The N = 32 coupled-ring chain
(C-2 cell): trained parameter set {δ_j, κ_ext,j, μ_j,j+1} (ring detunings, bus couplings,
inter-ring couplings), with the resolved four-tap input map B = {3, 12, 21, 30} (§3, §5.7).
(b) Realizable memory (samples at 2 GS/s) versus intrinsic Q at gain fractions
g_f ∈ {0, 0.5, 0.9}, the three registered cells (C-1 foundry-floor, C-2 headline, C-3
aspirational), and the 7-tap task-span line — why the operating point carries gain: at g_f = 0
the foundry-floor cell sits at the task-span line; at the registered g_f = 0.9 all three cells
clear it with margin.

**Figure F2 — The dissipative substrate's operating map.** (a) Settled saturating net loss
κ_net(r) versus the fixed-gain plane, the lasing crossing r\*, the registered clamp band
(r_min = 0.1606 with margin m_κ = 0.05, Δr = 0.02), and the initialization point θ₀. (b)
Off-resonance de-saturation at r_min versus θ₀ — the quantified anchor-risk (vii): a detuned
ring at r_min reaches κ_net = −0.48 κ_i, which is why the clamp is referenced on-resonance
(§3.6).

**Figure F3 — Controllability is a first-class constraint.** Per-ring gradient magnitude
(relative to the maximum ring) under a single input tap versus the resolved four-tap map. The
single-drive profile collapses geometrically with distance from the drive (ring 32 sits ~25
orders below the maximum; participation {1, 3, 5}/32 rings above {10⁻¹, 10⁻², 10⁻³}); the
resolved B = {3, 12, 21, 30} puts all 32 rings above the pre-registered 10⁻³ gate (worst ring
1.42 × 10⁻³, min over five drive seeds).

**Figure F4 — Sample efficiency to target (the headline).** Median held-out SER versus
physical device passes at C-2 (8 seeds; shaded IQR): PAT, recurrent adjoint, SPSA, RHEL
(honest echo, censored at budget), the readout-only reservoir baseline, and the offline-deploy
arm (deployed pre-trained, so it starts low; head recalibration only). Dotted lines mark the
BPTT-on-substrate ceiling (device passes = 0 by the PR-7 convention, drawn as a level only) and
the pre-registered target SER = 5.65 × 10⁻³; the vertical line is the device-pass budget
B = 252,800.

**Figure F5 — Ranking at matched device-pass cost.** Median device passes to target (per-seed
dots) with the digital-computation side-ledger co-reported (hatched; PAT's twin backward =
505,600 digital passes): PAT 38,400 < adjoint 73,600 < SPSA 176,000; RHEL censored 0/8. The
ranking answers the pre-registered promotion question in the negative: neither exact method
beats both workhorses.

**Figure F6 — Damping is a first-order design knob.** Final SER versus uniform pinned
overcoupling r (plateaued endpoints spanning ×302), the deep-overcoupling optimum r\* = 2.0
(κ_net ≈ 4.1 κ_i — *excess* memory is harmful for this task), and the trainable-κ_ext box
(R-ii): boxes containing r\* train to the 5 × 10⁻⁴ ceiling, beating every uniform pin — the
heterogeneous damping profile is found by training, not designed. Dashed red: the T-A-L
transfer test (14-tap span, eval-F; PR-17) — the registered prediction that the optimum moves
to lighter damping *failed*; the harder task raises the floor everywhere while the optimum
stays in the deep-overcoupling plateau (r = 2–3 within 13%), so the heavy-damping optimum is
robust to a ×2 task-memory span (§6).

**Figure F7 — The systems envelope.** (a) Training-energy inversion: SPSA trains the C-2 cell
all-in for ~2.6 mJ (optimistic conversion accounting; 99 mJ conservative) while PAT's device
side is 0.57 mJ but its digital twin backward costs 13–44 J — the energy metric inverts the
device-pass ranking. (b) Inference energy per sample versus state dimension N at 2 GS/s against the named digital
baselines: the photonic envelope (optimistic corner, low-power heater class) clears the
measured embedded-GPU (Jetson sustained) and Brainwave batch-1 lines at all N and enters the
DSP-ASIC class at N = 128 — while never beating the Jetson *peak-spec* line, which we report
alongside: the niche is conditional, as §7 states.

**Figure F8 — What breaks the offline tie (pre-registered follow-ups, §5.5; eval-F protocol
of record, PR-17).** (a) Calibration-mismatch sweep, 5→30%-class (8 seeds): in-situ PAT
(8.4–8.6 × 10⁻⁴) and offline-deploy (8.7–9.0 × 10⁻⁴) are statistically indistinguishable at
every level (ratio ≤ 1.05, every paired-bootstrap CI including zero) — crossover m\* = none.
(b) Deploy-then-drift, common-mode regime (σ_step = 0.40 κ_i per step on all detunings
coherently): the offline laser re-lock absorbs the drift and keeps pace (ratio 1.34, CI
including zero). (c) Independent per-ring drift: the re-lock cannot fix per-ring pole scatter;
in-situ retraining holds near-ceiling while the re-locking offline baseline degrades with
accumulated drift — **time-integrated ratio 2.42×, CI [+0.71, +2.84] × 10⁻³ excluding zero,
clearing the pre-registered 2× advantage threshold** (the coarse-floor estimate, 1.84×, sat
below the bar and is co-reported per the frozen both-protocols rule). The in-situ SPSA curve
is context only (per-step re-convergence transient; no registered verdict involves it).
Dashed/dotted lines: target and the eval-F BPTT ceiling.

---

**Figure S1 — The benchmark anchor we do not use (G3 dossier, §8.3).** (a) Validation-accuracy
trajectories of the *official* LinOSS-IM code on the published EigenWorms seeds (our rerun,
2026 stack): two of five seeds visibly collapse mid-training (the fp32 absorbing-zero-gradient
mode). (b) Final test accuracy per seed against the published 95.0 ± 4.4%: rerun mean 90.56%,
σ 9.34 ≈ 2.1× the published dispersion (per-seed 97.22 / 83.33 / 97.22 / 97.22 / 77.78).

**Figure S2 — Twin-mismatch decomposition at C-1 (§5.6; eval-F).** Final SER (3 seeds) for
PAT with a perfect twin, a parametric-error (M-par) twin, and a structural-omission (M-struct)
twin: perfect and M-struct land identically (1.11 × 10⁻³) while the fine floor resolves a
small M-par excess (1.31 × 10⁻³, +18% — invisible at the coarse floor). Mismatch channels
remain ≈ 0 at this cell only (the dropped gain channel grows to ~8% of gradient direction at
C-2, §5.6). The idealized-conjugator RHEL control clears the C-1 target with a thin margin
(7.2 vs 7.3 × 10⁻³), localizing RHEL's C-2 failure to echo physics, not mechanics.

**Figure S3 — The concrete echo sub-model (PR-11, §4).** (a) Conjugation-chain waterfall at
the frozen operating point (mechanism A, shared spiral bank): ring-port extraction η_ex²,
single-pass χ³-FWM spiral conversion (0.3 W pump, 0.5 m), routing/insertion — chain
η_c = −22.4 dB per conjugation. (b) Per-cell feasibility ceilings for the alternative
mechanisms: resonant-ring loaded-Q ceiling from the state bandwidth (mechanism B) and 10-ns
off-chip transit amplitude survival (mechanism C).

**Figure S5 — RHEL recovers its own theorem's limit (§5.4).** Cosine between the RHEL update
and the exact BPTT gradient as the substrate is made progressively less dissipative: −0.75 at
κ_net T dt ≈ 1.0, monotonically to +1.0000 at 0.03 — exact recovery of the non-dissipative
limit. The registered C-2 operating point sits at κ_net T dt ≈ 27, far beyond the anti-aligned
regime: the C-2 failure is dissipative-echo bias, not implementation error.
