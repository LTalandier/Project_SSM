# Figure captions (P1)

**Status:** v2, condensed 2026-09-29 for the first public deposit (v1 at commit `a508a28`). One
caption per figure (F1–F8 main, S1–S3/S5 supplementary). Numbers restate the frozen results the
figures are generated from (`analysis/make_figures.py`, `analysis/make_sfigures.py`).

---

**Figure F1 — Architecture and realizable pole region.** (a) The N = 32 coupled-ring chain (C-2):
trained set {δ_j, κ_ext,j, μ_j,j+1} with the resolved four-tap input map B = {3, 12, 21, 30}
(§3.6). (b) Realizable memory (samples at 2 GS/s) versus intrinsic Q at gain fractions
g_f ∈ {0, 0.5, 0.9}, the three registered cells and the 7-tap task span: at g_f = 0 the
foundry-floor cell sits at the task span; at the registered g_f = 0.9 all three cells clear it.

**Figure F2 — The substrate's operating map.** (a) Settled saturating net loss κ_net(r) against the
fixed-gain plane, the lasing crossing r\*, the clamp band (r_min = 0.1606; margins m_κ = 0.05,
Δr = 0.02) and the initialization θ₀. (b) Off-resonance de-saturation at r_min: a detuned ring
reaches κ_net = −0.48 κ_i, the open anchor risk of §3.6.

**Figure F3 — Controllability is a first-class constraint.** Per-ring gradient magnitude relative to
the maximum ring, under one input tap and under the resolved four-tap map. The single-drive profile
collapses with distance (ring 32 ~25 orders below the maximum); B = {3, 12, 21, 30} puts all 32
rings above the 10⁻³ gate (worst 1.42 × 10⁻³, minimum over five drive seeds).

**Figure F4 — Sample efficiency to target.** Median held-out SER versus device passes at C-2 (8
seeds; shaded IQR) for PAT, adjoint, SPSA, RHEL (censored), the readout-only baseline and the
offline-deploy arm, which starts low because it is pre-trained. Dotted lines: the BPTT reference,
drawn as a level because it uses no device passes, and the target SER = 5.65 × 10⁻³. Vertical
line: the budget B = 252,800.

**Figure F5 — Ranking at matched device-pass cost.** Median device passes to target, per-seed dots,
with the digital side-ledger hatched (PAT's twin = 505,600 digital passes): PAT 38,400 < adjoint
73,600 < SPSA 176,000; RHEL censored 0/8. Neither exact method beats both workhorses.

**Figure F6 — Damping is a first-order design knob.** Final SER versus uniform pinned overcoupling r
(plateaued endpoints spanning ×302), with the optimum r\* = 2.0 (measured κ_net = 3.7 κ_i). Boxes
containing r\* train to the 5 × 10⁻⁴ reference, beating every uniform pin. Dashed red: the T-A-L
transfer task (14-tap span, eval-F), whose predicted shift to lighter damping failed; r = 2–3 lie
within 13% (§6).

**Figure F7 — Historical systems-envelope components.** (a) Conversion-energy estimates (SPSA
2.6 mJ OPT / 99 mJ CONS; PAT 0.57 mJ OPT) and PAT's 13–44 J digital-twin estimate. Writes, settling
and full-duration holding costs are excluded, so the panel does not rank total training energy
(§7.3, N8). (b) The original nominal-N inference comparison at 2 GS/s, superseded by the
function-matched result of §7.4.

**Figure F8 — Pre-registered follow-ups to the offline comparison (§5.5; eval-F).** (a) Corrected
5–30%-class calibration sweep (S0.13), eight seeds per arm and level; lines are medians, dots
seeds. All five paired intervals include zero; offline/PAT ratios span 0.994–1.053. (b)
Common-mode drift (σ_step = 0.40 κ_i on all detunings coherently): the offline re-lock keeps pace
(ratio 1.34, CI including zero). (c) Independent per-ring drift: in-situ retraining holds near the
reference while the re-locking offline arm degrades — time-integrated ratio 2.42×, difference CI
[+0.71, +2.84] × 10⁻³, both conditions of the frozen rule (PR-16). The coarse-floor estimate of the same bit-identical trajectories, 1.84×, sat below the bar and is
co-reported; the ratio's own CI, [1.7, 4.6], is given in §5.5. The in-situ SPSA curve is context
only. Dashed and dotted
lines: the target and the matched-budget BPTT reference (31,600 updates).

---

**Figure S1 — The benchmark anchor we do not use (§8.3).** (a) Validation-accuracy trajectories of
the official LinOSS-IM code on the five published EigenWorms seeds (our rerun). Two trails drop
sharply late in training. Test accuracy is taken at the validation-selected checkpoint, and the
trails carry no per-step gradient measurements, so they do not explain the two low test scores.
(b) Final test
accuracy per seed (97.22 / 83.33 / 97.22 / 97.22 / 77.78%) against the published 95.0 ± 4.4%: rerun
mean 90.56%, population SD 8.35 percentage points.

**Figure S2 — Twin-mismatch decomposition at C-1 (§5.6; eval-F).** Final SER (3 seeds) for PAT
with a perfect, a parametric-error (M-par) and a structural-omission (M-struct) twin: perfect and
M-struct coincide (1.11 × 10⁻³) and M-par shows a small excess (1.31 × 10⁻³, +18%). Mismatch
channels are ≈ 0 at this cell only (§5.6). The idealized-conjugator RHEL control clears the C-1
target narrowly (7.2 vs 7.3 × 10⁻³), locating RHEL's C-2 failure in echo physics.

**Figure S3 — The concrete echo sub-model (§4.5).** (a) Conjugation-chain waterfall at the frozen
operating point: ring-port extraction η_ex², single-pass χ³-FWM spiral conversion (0.3 W pump,
0.5 m) and routing, η_c = −22.4 dB per conjugation. (b) Per-cell ceilings for the alternatives: a
resonant-ring loaded-Q ceiling (mechanism B) and 10-ns off-chip transit amplitude survival
(mechanism C).

**Figure S5 — RHEL recovers its own theorem's limit (§5.4).** Cosine between the RHEL update and
the exact gradient as the substrate is made less dissipative: −0.75 at κ_net T dt ≈ 1.0, rising
monotonically to +1.0000 at 0.03. The C-2 operating point sits at κ_net T dt ≈ 8 (C-1 at ≈ 27).
