# Bake-off task candidates + PR-2 input sheet (S0.2-0, design input for the PR-1/PR-2 freeze)

**Task:** S0.2-0 · **Author:** Executor · **Date:** 2026-06-10 · **Status: MENU, NOT CHOICE** —
nothing here is frozen; the Supervisor drafts the freeze ask and **Lucas freezes** (PR-2). Zero
training runs were performed. Companion memo: `debt2_benchmark_recon.md` (Gate-i candidates +
margin bases). Markers [EV]/[AV]/[ABS] as defined there.

**Governing inputs:** envelope niche statement (`s07_lite_envelope.md` §6, incl. the audit-added
condition 4) · `mapping_result.md` §4 (pole/memory bound) · PR-10 frozen operating scale
(`preregistration.md`) · B1 actuation map (`docs/s0_1/B1_actuation_map.md`) · PR-15.1 W1 claim ·
ledger Notes (D-08-2 constraints; EV-F1/F3/F5 carry-ins; F6).

---

## 1. The niche constraints every candidate is sized against

From the frozen PR-10 grid + the audited envelope (§6) + S0.1:

| Constraint | Value | Source |
|---|---|---|
| Line-rate window / floor | registered 0.1–2 GS/s; niche floor **≥ ~0.5 GS/s** (deployable-corner crossover; OPT×B floor ~0.13) | PR-10 row "Operating scale"; envelope §6.2 |
| State dimension | **N = 32–128** (margins grow with N via C8) | envelope §6; PR-10 N grid {8,32,128} |
| Memory yardstick (amplitude/state memory × rate, T_mem·f_s) | foundry corner: **0.33 / 3.29 / 6.58 samples** at 0.1/1/2 GS/s · class-leading: **4.9 / 49.4 / 98.8** | mapping_result §4 (3.29→49.4 ns); envelope §4 |
| Latency relevance | per-sample ≲ 1 µs workloads (serving class can't reach) | envelope §6 |
| N=128 caveat | N=128 margin cells assume the **class-leading-Q corner** (pole packing O(10–20)/GHz foundry vs ~150 class-leading) — splitting-prone, → PR-4×D-08-1 | envelope §6.4 (EV-F3) |
| Readout condition | envelope consistency holds **iff single-quadrature or intensity readout** (I/Q doubles the output chain) | envelope §6.4 (EV-F5) |
| λ-plan | single-carrier-one-FSR; one input stream; no WDM | PR-10 row |

Convention used below: "memory depth required" is counted in samples at the task's clock and
compared against T_mem·f_s (the registered amplitude-memory yardstick, same convention the
envelope's sub-sample exclusion used). Gain (Stage-2, |λ|→1) can extend the foundry corner past
its passive floor — noted as a knob, never assumed.

## 2. The candidates

### T-A — Jaeger–Haas nonlinear channel equalization, clocked at 1–2 GS/s
*(equalization-class family head; published-benchmark-anchored)*

- **Generator (exact, primary-quoted):** 4-PAM i.i.d. symbols d(n) ∈ {−3,−1,1,3}; linear ISI
  *"q(n) = 0.08 d(n+2) − 0.12 d(n+1) + d(n) + 0.18 d(n−1) − 0.1 d(n−2) + 0.091 d(n−3) − 0.05 d(n−4)
  + 0.04 d(n−5) + 0.03 d(n−6) + 0.01 d(n−7)"*; memoryless nonlinearity
  *"u(n) = q(n) + 0.036 q²(n) − 0.011 q³(n) + ν(n)"*; Gaussian ν at SNR 12–32 dB [EV: pdftotext of
  arXiv:1501.03024 (Vinckier et al., Optica 2015), the text restatement of the Jaeger & Haas
  Science 304:78 (2004) channel]. Target: recover d(n−2) (canonical 2-sample-delay convention;
  Vinckier's prose says d(n) — convention gap flagged, the freeze states which). Metric: **SER**
  at registered SNR points (NMSE secondary).
- **Memory required:** full tap span **10 samples** (u(n)…u(n−9) at emission); dominant taps
  (|w| ≥ 0.05) span **7 samples**.
- **Rate:** synthetic clocking — run at 1 and 2 GS/s (floor ✓ by construction). Honesty line: the
  photonic-hardware record on this exact channel is **~0.1–0.9 MS/s** (Paquot 2012: T = 8.504 µs
  loop, 50 nodes [AV]; Vinckier 2015: *"the output refresh rate 1/T′~0.9MHz can be seen as the
  processing speed"*, SER→0 at 28/32 dB with 50 nodes, 3k train / 6k test ×10 [AV/EV]) — three
  orders below the niche; in Stage 0 the GS/s clock sizes the *simulated* niche only.
- **N sizing:** the RC literature solves this channel at ~50 nodes → N=32 expected sufficient,
  N=128 = headroom; {32, 128} brackets the published anchor.
- **Reservoir-baseline contrast:** maximal — this is *the* canonical readout-only-RC benchmark, so
  the trained-recurrence vs trained-readout contrast (§5.3 baseline, W1 story) lands on ground the
  RC field knows.
- **PR-13 parametrization:** generalize the fixed tap vector to a registered family — tap span
  K ∈ {2…100} with a fixed decay profile (published taps = the K=10 anchor cell); the K→pure-delay
  limit is exactly delayed recall.
- **Risks:** anti-causal taps (n+2, n+1) require the 2-sample target delay — a latency-vs-accuracy
  coupling the freeze should state; foundry-corner fit at 1 GS/s is poor (table §3).

### T-B — Band-limited IM-DD PAM-4 link equalization at 1–2 GBd
*(equalization-class, in-house generator lineage; the physically-motivated GS/s task)*

- **Generator (ported, with provenance):** the pnn-multilayer time-domain IM/DD chain
  (`channels/imdd_timedomain.py` @ e2eec80, read 2026-06-10): bits → PAM-4 → RRC (sps=4) → MZM sin
  nonlinearity (drive_ratio) → TX BW filter → SMF CD via FFT → RX BW filter → square-law PD → real
  waveform + metadata (Rs_Hz, β2·L, impulse-response length). Native validated grid: Rs ∈
  {50,100,200} GBd, L ∈ {0–10} km. **Re-rated variant for the niche: Rs = 1–2 GBd.**
- **Where the ISI comes from at GBd rates (honest arithmetic):** CD is inert at this rate —
  Δλ ≈ (λ²/c)·Rs ≈ 16 pm at 2 GHz, so ΔT_CD = D·L·Δλ ≈ 0.27 ps per 10 km ≈ **0.005 symbols** —
  the CD block contributes nothing in-window. ISI is therefore sourced from **TX/RX
  band-limitation** (BW/Rs ∈ 0.3–0.7, the low-cost-optics regime) + RRC tails; nonlinearity from
  MZM sin + PD |·|². **ISI span designable ≈ 2–12 symbols** via the BW ratio — the one candidate
  whose memory depth is a clean experimental knob.
- **Rate:** 1–2 GBd native (floor ✓); the workload class is literally the envelope's niche
  sentence ("equalization-class streaming task at GS/s rates").
- **Metric:** NMSE (house convention; `compute_nmse_field` already salvaged) + SER by PAM-4
  thresholding.
- **N sizing:** ISI ≤ 12 symbols + mild nonlinearity → N=32 ample by linear-tap counting; 128 =
  headroom/packing test.
- **Anchor status (flag):** *not* an external published benchmark at these rates — its authority
  is the in-house, Critic-reviewed pnn-multilayer chain (provenance header on port). Pairs
  naturally with T-A (external anchor) rather than replacing it.
- **PR-13 parametrization:** ISI span (BW ratio) as the lag knob; optionally explicit synthetic
  tap families when a precise lag is needed.
- **Port cost (flag):** `imdd_timedomain.py` was **not** in the 7-asset salvage manifest → one
  extra port-with-provenance at S0.2-1/S0.3. Small but real.

### T-C — PR-13 synthetic memory family: delayed recall / sticky detection at parametric lag
*(the published-benchmark-aligned alternative + the PR-13 secondary, unified)*

- **Definition:** i.i.d. 4-ary input u(n); **(a) delayed recall** — target u(n−k); **(b) sticky
  detection** — binary target 1 iff a designated marker symbol occurred within the last k samples;
  lag grid k ∈ {1, 3, 10, 30, 100}, clocked at 1 GS/s (and 2 GS/s for the cliff cell).
- **Published alignment:** this is the task class the D-LinOSS paper itself uses for mechanism
  ablations — the Adding problem at lengths 500–5,000 (where LinOSS-IMEX *"fails to outperform …
  random guessing"* [AV]) and the Decay regression (D-LinOSS 0.8±0.1 ×10⁻³ vs IM 8.0±1.7 at
  λ=0.8 [AV]) — plus the delay-line memory-capacity family standard across photonic RC. And it
  **is** the PR-13 ledger row ("a synthetic memory-task family with tunable memory length (delayed
  recall / sticky detection at parametric lag)", F20) — choosing it as a bake-off task and
  registering PR-13 become one act.
- **Memory required:** exactly k. The grid deliberately straddles every corner: k=1,3 fit the
  foundry corner at 1–2 GS/s; k=10 needs class-leading (or gain) — it sits right at the foundry
  cliff; k=30 fits class-leading; **k=100 > 98.8 = the class-leading ceiling at 2 GS/s** — the
  designed memory-cliff cell for the memory-vs-Q story.
- **Metric:** NMSE (recall) / accuracy (sticky); sample-efficiency-to-target on each k-cell
  (primary bake-off metric applies per cell).
- **N sizing:** the N-sweep {8, 32, 128} is the point (linear-memory capacity scales with state
  dimension — tested, not assumed).
- **Latency relevance: none** (synthetic probe) — T-C cannot carry the niche narrative alone; it
  stress-tests ranking robustness + memory-vs-Q (its registered purpose).

## 3. Niche-fit table (explicit arithmetic)

Memory fit = required depth vs T_mem·f_s (✓ fits · ◑ marginal · ✗ exceeds passive memory).

| | **T-A** Jaeger–Haas eq. | **T-B** IM-DD PAM-4 eq. | **T-C** memory family |
|---|---|---|---|
| Clock vs ≥0.5 GS/s floor | 1–2 GS/s ✓ (synthetic clocking) | 1–2 GBd ✓ (native class) | 1–2 GS/s ✓ (synthetic) |
| Memory required (samples) | 10 full / 7 dominant | 2–12, **designable** | k ∈ {1,3,10,30,100}, exact |
| Fit: foundry @1 GS/s (3.29) | ✗ (covers ~n−3 only) | ✓ if span ≤3 chosen / ✗ above | k≤3 ✓ · k≥10 ✗ |
| Fit: foundry @2 GS/s (6.58) | ◑ (dominant span ~covered; 10-tap tail lost) | ✓ if span ≤6 / ✗ above | k≤3 ✓ · k=10 ◑ near cliff |
| Fit: class-leading @1 (49.4) / @2 (98.8) | ✓ / ✓ | ✓ / ✓ | k≤30 ✓ · k=100 ✗ @2 (designed cliff) |
| N sizing | 32 sufficient (50-node RC anchor); 128 headroom | 32 ample; 128 headroom | N-sweep {8,32,128} is the experiment |
| Metric | SER @ registered SNR (+NMSE) | NMSE (+SER) | NMSE / accuracy per k-cell |
| Published anchor | Science 2004 + photonic RC (Paquot/Vinckier, ~0.1–0.9 MS/s) [EV/AV] | in-house pnn-multilayer chain (no external benchmark at-rate — flag) | D-LinOSS ablation class [AV] + RC memory-capacity family |
| Sub-µs latency relevance | ✓ (per-symbol decision) | ✓ (per-symbol decision) | n/a (probe) |
| Reservoir-contrast quality | **maximal** (canonical RC task) | good (RC-style readout natural) | good (memory capacity is the classic RC probe) |
| PR-13 parametrization | tap-span family K (published taps = K=10 cell) | ISI span via BW/Rs knob | **is** PR-13 |

Consistency: all candidates respect the frozen PR-10 grid (rates in-window, N in {8,32,128},
single stream / no WDM); every N=128 cell inherits the EV-F3 class-leading-corner caveat; gain
rescue of foundry-corner memory is Stage-2/PR-12 territory and is never assumed in the fits.

**Observation (not a choice):** the three candidates are complementary, not competing — T-A gives
the external anchor + maximal reservoir contrast, T-B gives the niche-native physical workload
with a designable memory knob, T-C gives the parametric memory probe PR-13 wants anyway. A
primary+secondary freeze (one of T-A/T-B as headline, T-C as the registered PR-13 secondary)
would satisfy F20 with no extra task engineering.

## 4. PR-2 input sheet

### 4.1 Trainable-parameter partition options (every estimator trains the SAME partition — PR-6)

Physical knobs and actuators per the B1 map (`B1_actuation_map.md`); counts assume the
nearest-neighbor chain topology (N−1 coupling edges; see 4.3).

| Option | In-situ-trained set | Actuators (B1 map) | Control ch @ N=32 / 128 | vs PR-10 "2–4 ch/ring" |
|---|---|---|---|---|
| **P1 — full B1 (Stage-2, gain-rich)** | {δ_j, κ_tot,j via κ_ext,j **and** g_j, μ_jk} | heaters + tunable couplers (MZI-assisted, 1–2 ch) + ring–ring couplers + pump currents | ≈127–159 / ≈511–639 | 4–5/ring — **at/above** the registered bracket; flag |
| **P2 — gain-free minimal B1 (Stage-1)** | {δ_j (heaters), κ_ext,j (tunable couplers), μ_jk (ring–ring couplers)} | all thermo-optic — drift-stable, SPSA/PAT-friendly (B1 memo: this "already suffices for the white-space claim") | ≈95 / ≈383 | ~3/ring ✓ |
| **P3 — {δ_j, μ_jk}, damping fixed** | detunings + couplings; κ_tot held at the PR-4 policy value | heaters + ring–ring couplers only | ≈63 / ≈255 | ~2/ring ✓ |
| **P4 — {δ_j} only** | heaters only | heaters | 32 / 128 | 1/ring — but see 4.3: **fails W1** |
| **Reservoir baseline (§5.3 contrast)** | B/C residues + ridge head only; **B1 frozen** | readout mesh / digital ridge | — | the contrast, not a partition option |

In all options the digital side of the hybrid (encoder, B/C residues where not the baseline's
knob, head) is trained digitally; the **claim attaches only to the in-situ-trained recurrent
set** (mapping_result §2: residues/B,C are "train-only = the reservoir baseline, explicitly
excluded from the claim").

### 4.2 Readout options (under the EV-F5 condition) + the F6 κ_ext dual-role

| Option | Head class | Envelope consistency (EV-F5) | Benchmark-transfer consequence |
|---|---|---|---|
| **R1 — single-quadrature homodyne** y = Re(Σc_j a_j) | real-linear — **LinOSS-equivalent** (mapping_result §2) | ✓ one O/E + one ADC (C8 holds; C5's 14·N assumes exactly this) | cleanest: Gate-i model class = hybrid model class. Cost: LO + phase locking sit in the §7 exclusions (unbudgeted — listed) |
| **R2 — direct-detection intensity** y = \|Σc_j a_j\|² | nonlinear \|·\|² head | ✓ single chain, no LO | departs from the published (real-linear-head) LinOSS class → transfer leans harder on the PR-3 in-house ceiling; in a single-photonic-layer hybrid, \|·\|² is also the only physical nonlinearity |
| **R3 — I/Q dual-quadrature** | complex-linear head | **✗ envelope-inconsistent** — doubles the output chain; the boundary OPT×B-vs-DSP N=32 cell dies and CONS×B N=32-vs-Brainwave flips LOSES (deployable corner starts at N=128) | choosing R3 re-opens audited envelope cells — if PR-2 wants it, that re-opening must be explicit |

**F6 κ_ext dual-role (must be addressed at the freeze, per the ledger Note):** in P1/P2, κ_ext is
simultaneously the damping actuator and the readout-strength knob (B3 trade: at Q_i=2×10⁶,
274 rt @ 0.028 drop-efficiency ↔ 16 rt @ 0.91 — memory×residue bounded). Policy options:
(a) κ_ext trainable within registered B3 bounds, **and the reservoir baseline holds κ_ext frozen
at the common PR-4 policy value** — the baseline must never gain recurrence-shaping through the
readout knob (keeps the §5.3 contrast clean); or (b) κ_ext excluded from the partition (→ P3) —
cleanest contrast, weakest damping story. D-08-2/audit carry-in: **no conjugate pairing** in the
simulated layer (pairing would also halve the digital-equivalent op count to 7N and kill four
deployable-corner envelope CLEARs — ledger Note).

### 4.3 W1 claim cross-check (PR-15.1 adopted default claim)

W1: *"first continuous-time dissipative-resonator recurrence — **pole positions + inter-resonator
couplings** — trained in situ by gradient-based/-estimating methods on a computational task."*

| Option | Trains pole positions? | Trains inter-resonator couplings? | W1-satisfying? |
|---|---|---|---|
| P1 | ✓ both axes (Re via κ, Im via δ) | ✓ μ_jk | **✓** |
| P2 | ✓ both axes (Re via κ_ext, Im via δ) | ✓ μ_jk | **✓** (B1 memo's Stage-1 minimal) |
| P3 | ◑ Im-axis only (δ; damping fixed) | ✓ μ_jk | **conditional** — "pole positions" satisfied only under the moves-along-iℝ reading; **wording call for the Supervisor at PR-2**. Also surrenders trained damping — the D-LinOSS axis (the published evidence that *learnable* dissipation is what wins) and the proposal's damping-as-free-knob story |
| P4 | ◑ Im-axis only | ✗ none | **✗ fails W1** (no couplings trained) — listed for explicit exclusion |
| Reservoir baseline | ✗ | ✗ | ✗ by design — the contrast that makes the claim falsifiable in our own data |

Task-side W1 note: q4 (task-objective condition) is satisfied by all three candidates — each is a
corpus-of-input-output-examples task with held-out evaluation; none is setpoint regulation.

**Topology fork (B1 flag, must be pinned at PR-2):** *direct photonic-molecule* coupling — fixed
sparsity (chain/ladder mask), strengths trainable, N−1 tunable couplers, deployable-corner-
consistent (the PR-10 2–4 ch/ring bracket covers chain-class counts, not mesh-class) — vs
*bus-mediated MZI mesh* — dense reconfigurable Ω, more loss/area + mesh calibration. The simulated
μ matrix supports both (dense μ + sparsity mask), so the simulation cost of keeping both as sweep
cells is low; the *claim* wording ("inter-resonator couplings") is satisfied by either.

## 5. What this memo does not do

No task/margin/partition/readout choice (Supervisor drafts; **Lucas freezes**); no LinOSS
implementation or training (S0.2-1, post-freeze); no new envelope sourcing (PR-10 frozen — every
envelope number above is cited to its frozen row or the audited memo); no PR-15 retrieval work
(Lucas, claim-freeze-paced). All numbers trace to: the two S0.2-0 sweep memos' primaries
[EV]/[AV], the frozen PR-10 block, `mapping_result.md` §4, `B1_actuation_map.md`, and the audited
envelope memo.
