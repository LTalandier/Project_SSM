# Critic Review — Proposed PR-1 + PR-2 freeze blocks (phase boundary, pre-S0.2-1)

**Reviewer:** Critic (independent; reports to Lucas) · **Date:** 2026-06-10
**Spec:** `shared/critic_instructions_pr1-pr2-freeze.md` · **Target:** the PROPOSED PR-1/PR-2 blocks at the
end of `shared/preregistration.md` (Supervisor draft 2026-06-10) — the *choices*, not just the transcription.
**Read:** both blocks · `docs/s0_2/debt2_benchmark_recon.md` · `docs/s0_2/bakeoff_task_candidates.md` ·
ledger Notes + PR-10 + PR-15.1/W1 + rows PR-3/PR-6/PR-7/PR-12/PR-13 · `docs/s0_1/mapping_result.md` ·
`docs/s0_1/B1_actuation_map.md` · roadmap §S0.2/§S0.5.
**Re-derivations:** `/tmp/critic_pr2_linear_floor.py` (channel-equalizer floors, sticky class balance,
M1 gate power, SER resolution — all numbers below re-computed there, 4 seeds, 2×10⁵ test symbols/seed).

---

## Overall verdict: **AMEND** (PR-2 — one structural decision + edits) · PR-1 standalone = **APPROVE-WITH-EDITS**

**The line for Lucas:** **PR-1: sign with the edits below** (completeness pins only; the anchor choice,
margins, and protocol are sound and faithfully transcribed). **PR-2: do not sign as-is.** One finding is
structural (PF-F1: the pinned headline configuration — R1 readout + digital *linear* head — is end-to-end
linear, and a linear system measurably cannot approach the RC anchor this headline cell is built on; floor
re-derived at SER ≈ 0.7 %, ~400× above the anchor, flat across 24–32 dB). It has a clean one-pass fix
(recommended: swap R2 to headline, R1 to alternative — exact text in PF-F1); adopt one of the two fixes,
apply the remaining edits, and PR-2 can be signed in the same pass. Everything else checked clean:
**no silent edits found anywhere** — every number in both blocks traces to an [EV] memo row or a frozen
ledger value; the exclusion reasons are honest; the partition/topology/R3 pins are consistent with
W1, EV-F1/F3/F5, D-08-2/D-08-3, PR-10, and create no contradictions with PR-3/PR-6/PR-7/PR-12/PR-13.

---

## 1. Verified-PASS (what I checked and confirmed)

1. **Transcription integrity (checklist 1) — PASS.** Re-traced every load-bearing number:
   G1 75.8 ± 3.7 → threshold 72.1 ✓; G3 95.0 ± 4.4 → 90.6 ✓ (and 90.6 > LRU 87.8 ✓ — the implication
   claimed is true); both configs character-match recon §4 ([EV] rows); seeds {2345…6789} ✓; 70/15/15 ✓;
   the 10 channel taps + 0.036/−0.011 coefficients match the memo's [EV] quote of arXiv:1501.03024 ✓;
   SNR grid {16,24,28,32} sits inside the sourced 12–32 dB range with the 28 dB anchor faithfully read ✓;
   k-grid {1,3,10,30,100} + the 2 GS/s k=100 cell match the memo and **are** the PR-13 ledger row (early
   registration is earlier than the row's "freeze before S0.5" — permitted, not a contradiction) ✓;
   P2 ≈ 3 ch/ring inside the frozen 2–4 bracket ✓; N grid = PR-10 ✓; no banned/legacy value appears.
2. **PR-1 anchor choice (checklist 2) — sound.** G1+G3 = cheap-fidelity + flagship-long-range; the
   exclusions are honestly stated and match the memo (G2: preprint anchor / σ=7.5 alternative; G4:
   compute; Weather: irreproducible at pre-registration grade; Ethanol: spectral, near-chance).
   **M1 power, re-derived:** −1σ applied to a 5-seed mean is a **2.24-SE one-sided allowance** →
   false-kill ≈ 1.3 % per anchor, ≈ 2.5 % joint under a faithful-implementation null (and less, since
   running the *same* five seeds removes the split-draw component our side). A G3 mean of 89 % would sit
   ≈ 3 SE below published — strong evidence of a real implementation difference, so the gate *is*
   measuring what Gate i means. Caveat carried honestly: M1 catches gross breaks, not subtle ≤1σ
   systematic offsets — acceptable because the bake-off's downstream reference is the in-house PR-3
   ceiling, not the published number (state this; PF-F9d). Both-must-pass + 5-published-seed gated
   statistic with a non-gating 3-seed annex: clean separation ✓ (annex seeds unnamed — PF-F8g).
3. **PR-1 implementation-under-test (checklist 3) — right reading.** Gate i validates *our* layer (μ=0)
   inside the published stack; testing the official repo would validate nothing of ours. Configs are
   pinned to the published per-task values (no tuning surface); "reference behavior = the official code"
   resolves residual protocol ambiguity — make that closure rule explicit (PF-F8i) and pin split
   reproduction (PF-F6), and the wiggle room is closed.
4. **T-A over T-B (checklist 4) — the right cut, conditional on PF-F1 + PF-F2.** T-A buys the only
   external anchor and the canonical reservoir contrast; T-B is anchorless at-rate and stays a labelled
   extension; T-C is PR-13 anyway. T-B-headline would trade the field-credible falsifier for a
   guaranteed-fit memory story — strictly worse for the W1 claim, *provided* the headline model class can
   actually express the task (PF-F1) and the MS/s honesty line survives into the frozen text (PF-F2).
5. **F6 κ_ext policy (a) (checklist 6) — sound, with one carry-in.** Residue freedom is symmetric (both
   arms train B/C digitally), so κ_ext's readout-side effect is largely redundant with residues; its
   non-redundant physical effect (pole damping, noise-injection locus) is honestly part of "training the
   recurrence"; B3 bounds cap the range. The baseline stays a bona-fide reservoir. The real contamination
   channel is elsewhere: an unbounded digital encoder can buy SNR against the noise cell for *both* arms —
   an input-power normalization must be registered at PR-4 (PF-F8f). Also reconcile "frozen at init" vs
   "frozen at the PR-4 policy value" (PF-F8e).
6. **Architecture/partition/readout pins vs the record (checklist 6) — exact.** P2 trains pole positions
   on both axes + μ couplings → W1 ✓ (memo 4.3); P3/P4 exclusions match the memo's W1 table and the
   D-LinOSS trained-damping argument; R3 exclusion matches EV-F5 verbatim; chain topology = the B1 fork,
   pinned, deployable-corner-consistent; no-conjugate-pairing carried ✓. Cross-references both ways
   (checklist 8): no contradictions created in PR-3/PR-6/PR-7/PR-12/PR-13; one informative item dropped
   memo→block (the MS/s honesty line — PF-F2).

---

## 2. Findings

### PF-F1 (CRITICAL) — the pinned headline configuration is end-to-end linear; the anchor it is built on is not reachable by a linear system
The block pins: affine encoder → linear photonic recurrence → **R1** y = Re(Σc_j a_j) → **digital linear
head**. Every stage is linear, so the headline hybrid is a linear (affine) map of the symbol stream. The
Jaeger–Haas channel is nonlinear (0.036 q² − 0.011 q³ at |q| up to ~7 against symbol spacing 2), and the
RC anchor justifying the 28 dB headline cell — Vinckier's SER→0 at 50 nodes — was achieved with a *linear*
cavity whose task-solving nonlinearity is the **readout photodiode |·|²** (i.e., the anchor system is our
R2 class, not our R1 class; Executor to re-verify that sentence at retrieval level, but the floor below
stands regardless). **Re-derived floor:** the best *non-causal* linear equalizer (±15 taps — strictly more
information than any causal N-pole IIR with decision delay 2) floors at **SER = 2.9 % / 0.84 % / 0.71 % /
0.66 % at 16/24/28/32 dB** — distortion-limited, nearly flat over 24–32 dB, **~400× above the anchor**.
A Volterra-2/3 feature readout (nonlinear-readout-class proxy) reaches **1.4 % / 0.015 % / 0.003 % /
0.001 %** — anchor-class at 28 dB. Consequences if frozen as-is: the BPTT ceiling at the headline cell
floors near 0.7 % for *all* methods **and** the reservoir baseline (both linear → the §5.3 contrast
compresses exactly where the memo promised it would be maximal); the SNR grid is uninformative above
24 dB; any reader comparing our headline SER to the anchor reads failure; and Gate ii-a's utility floor
is hostage to an architecture choice, not to noise or memory.
**Fix (i), recommended — swap R2 to headline.** Replace the readout sentence with:
> → readout **R2 = direct-detection intensity** y(n) = |Σ_j c_j a_j(n)|² (single chain, EV-F5-consistent;
> the |·|² is the hybrid's only physical nonlinearity and the RC-anchor-native readout class — the ring
> states are time-mixtures of the input, so |·|² supplies the cross-lag quadratic features channel
> inversion needs) → digital linear head over the registered tap window {y(n−m), m = 0…7}. **R1
> (single-quadrature homodyne, real-linear — the LinOSS-equivalent-head cell) = registered alternative
> sweep cell**; an end-to-end-linear hybrid floors at SER ≈ 0.7 % on this channel at 24–32 dB (Critic
> re-derivation), so R1 cells are reported against the linear-class ceiling, never against the RC anchor.
> **R3 (I/Q) excluded** — envelope-inconsistent (EV-F5; choosing it would re-open audited envelope cells).
Add to the baseline bullet: "Under R2 the baseline is Vinckier-class — linear fixed dynamics + quadratic
readout + trained linear weights — so the §5.3 contrast lands on the RC field's own configuration."
Consistency check, done: R2 keeps one O/E + one ADC (C8 ✓), needs no LO (removes one §7 unbudgeted
exclusion), leaves W1/PR-10/D-08-2 untouched; the digital-equivalent op count rises ~14N→~18N, which only
*helps* the audited envelope margins (favorable direction; no re-opening). Cost: departs the
LinOSS-equivalent head → benchmark transfer leans on the PR-3 in-house ceiling — a cost D-08-2 already
accepted for μ≠0. **Fix (ii), not recommended:** keep R1 and insert a registered digital nonlinearity
(GELU, applied identically to both arms — the published LinOSS stack is itself nonlinear between SSM
layers, so a linear-head single block is *not* the published class). Honest but weaker: the digital head
then does the channel-inversion work, inviting "the digital nonlinearity did it" against the W1 story,
and it adds digital-head ops the envelope never charged.

### PF-F2 (HIGH) — the MS/s honesty line was dropped from the frozen text
The memo carries it loudly ("photonic-hardware record on this exact channel is ~0.1–0.9 MS/s … the GS/s
clock sizes the *simulated* niche only"); the PR-2 block — the text that governs S0.8 wording — omits it.
The spec's own test ("can the GS/s clock be read as a hardware claim?") currently fails at the block
level. **Edit:** append to the T-A clock sentence:
> Honesty line (binding for S0.8 wording): the photonic-hardware record on this exact channel is
> ~0.1–0.9 MS/s (Paquot 2012; Vinckier 2015); the GS/s clock sizes the *simulated* niche only and is not
> a hardware-demonstrated rate claim.

### PF-F3 (HIGH) — "the ceiling-relative PR-3 rule absorbs this" conflates the ranking rule with Gate ii-a
The ceiling-relative rule absorbs the ◑ memory limitation for *ranking* (ii-b) only. Gate ii-a is an
**absolute** utility floor (PR-3) evaluated at the foundry-grade cell (PR-4 constraint) — a ◑ headline
cell puts ii-a genuinely at risk on memory grounds, and the block's justification sentence papers over
that. That outcome would be the honest memory-vs-Q finding, not a bake-off failure — but only if the
freeze says so *now*. **Edit:** replace "— the ceiling-relative PR-3 rule absorbs this; class-leading
fits fully" with:
> — the ceiling-relative PR-3 *ranking* rule absorbs this for the method comparison; Gate ii-a's
> *absolute* floor does not inherit that absorption: PR-3 must register the floor on a cell-set containing
> ≥1 foundry-feasible cell (e.g. T-C k≤3, or T-A at the class-leading corner), and an ii-a miss at the
> foundry headline cell is recorded as the memory-vs-Q / Stage-1-reframing finding (roadmap v3.1
> semantics), not as a bake-off failure; class-leading fits fully.

### PF-F4 (HIGH) — the sticky-detection arm is class-degenerate at k ≥ 10 as frozen
With a uniform 4-ary marker, P(target=1) = 1 − 0.75^k = **94.4 % / 99.98 % / ≈100 % at k = 10/30/100** —
the always-1 classifier wins 3 of 5 grid cells and the arm is vacuous at exactly the interesting lags.
(The delayed-recall arm is fine.) **Edit:** replace the sticky definition with:
> **(b) sticky detection** — binary target 1 iff a marker occurred within the last k samples, the marker
> drawn as a separate registered rare-event stream with per-cell P(marker) = 1 − 2^(−1/k) (class-balanced
> at every k by construction); metric = balanced accuracy.

### PF-F5 (MEDIUM) — 10⁴ test symbols cannot resolve anchor-class SER at the top cells
P(zero errors | true SER 10⁻⁴) = 0.37 at 10⁴ symbols — a method at 10⁻⁴ "reaches SER 0" more than a third
of the time, and anchor-class performance (10⁻⁴–10⁻⁵, reachable under the PF-F1 fix) is unresolvable.
**Edit:** "held-out test 10⁵ symbols/seed at the 28/32 dB cells, 10⁴ at 16/24 dB" (cost is trivial for a
linear-time simulation; alternatively register the target SER no lower than 10⁻³ and say why).

### PF-F6 (MEDIUM) — split reproduction is unpinned across frameworks
The five seeds set the 70/15/15 *splits* through Walker's pipeline; a reimplementation with different RNG
semantics silently produces different splits, degrading the same-seed comparability the protocol buys.
**Edit (PR-1 protocol bullet):** "The five seeds must reproduce the published split assignment (port the
split routine or extract split indices from the official repo); if exact split reproduction is infeasible
in the chosen framework, declare via decisions_needed.md *before* the gated runs."

### PF-F7 (MEDIUM) — the Gate-i ↔ bake-off discretization delta is unstated
Gate i validates the in-house stack in **LinOSS-IM** mode (learnable sigmoid Δt, IM discretization — per
the reference-behavior pin); the bake-off substrate runs **exact-ZOH/CMT** with dt ≡ 1/f_s and no
learnable Δt. The architecture distinction is stated; the discretization distinction is not — S0.8
claim-drift risk ("our model reproduces published accuracy" while the bake-off object integrates
differently). **Edit (one sentence, either block):** "Gate i validates the stack under the published
LinOSS-IM discretization; the bake-off substrate runs exact-ZOH/CMT — that delta is bridged by the PR-3
BPTT-on-substrate ceiling, not by Gate i."

### PF-F8 (MEDIUM) — F12 completeness: items S0.2-1/S0.3 would otherwise invent (checklist 7)
One line each; (a)–(f) are the substantive ones:
- **(a) Data regime:** "Bake-off training data = streaming fresh i.i.d. draws per iteration (no fixed
  corpus); per-seed generator streams common across methods (PR-6)." Streaming-vs-corpus changes what
  sample-efficiency *means* — it cannot be an implementation choice.
- **(b) Init ownership:** "B1 init distributions (δ, κ_ext, μ at θ₀) are registered at PR-6 with the
  common-θ₀ convention; reference default = D-LinOSS radial-band init mapped through B1 ranges, μ(0)=0."
- **(c) Hybrid Δt:** "No learnable Δt in the hybrid: dt ≡ 1/f_s; pole-placement freedom is carried
  entirely by (δ_j, κ_ext,j) within B1/B3 ranges" (the published learnable-Δt freedom is absorbed,
  range-bounded — and a digitally-learnable per-ring dt would be unphysical).
- **(d) SNR convention:** "Train and test at the same registered SNR per cell."
- **(e) Baseline κ_ext reconciliation:** "the reservoir baseline holds κ_ext frozen at the common θ₀ =
  the PR-4 policy value" (the block currently says "at init" in one bullet and "at the PR-4 policy value"
  in another — they coincide only if init(κ_ext) ≡ policy value; say so).
- **(f) PR-4 carry-in (input power):** "PR-4 must register an input-drive-power / intracavity-energy
  normalization — the digital encoder must not be able to buy SNR against the registered noise cell."
- (g) Name the 3 annex seeds. (h) "Thresholds compared against the unrounded 5-seed mean." (i) Make the
  closure rule explicit: "any protocol detail not stated here resolves to the official repo's behavior;
  no hyperparameter tuning is permitted for the gated runs."

### PF-F9 (LOW) — wording accuracy
- (a) P1 exclusion: "busts the PR-10 bracket" → "sits at/above the bracket (4–5 ch/ring)" (4 is inside;
  the load-bearing exclusion ground is Stage-2 gain, which the block already states).
- (b) "Designed memory-cliff cell": the yardstick is a 1/e time, not a wall — amplitude retention at
  k=100 @ 2 GS/s class-leading is e^(−100/98.8) ≈ 0.36, and noiseless linear memory capacity scales with
  N, so the cliff is an SNR-dependent *hypothesis* completed by the PR-4 noise cell, not a guaranteed
  failure. Also note k=100 already exceeds the 1 GS/s class-leading yardstick (100 > 49.4) — the 2 GS/s
  cell is the *marginal* cliff. One clause: "(cliff = registered hypothesis; the 1/e yardstick is not a
  hard wall — outcome interpreted jointly with the PR-4 noise cell)".
- (c) d(n−2) invariant pin: "with the verbatim (centered) generator, the output at time n estimates
  d(n−2); implementations must not re-shift the polynomial to causal form while keeping the target index"
  (the shifted-generator + d(n−2) combination is a *different, harder* task — decision delay 0).
- (d) M1 parenthetical: "(−1σ on a 5-seed mean = a 2.24-SE one-sided allowance; false-kill ≈ 1.3 % per
  anchor, ≈ 2.5 % joint; calibrated to catch gross breaks, not ≤1σ systematic offsets — the bake-off's
  operative reference is the PR-3 in-house ceiling)."

---

## 3. Checklist disposition (spec items 1–8)
1 Transcription — **PASS** (§1.1). 2 PR-1 anchors/margin — **sound**, edits PF-F6/F8g/F8h/F9d (§1.2).
3 Implementation-under-test — **right reading**, closure rule PF-F8i (§1.3). 4 Headline task —
**right cut, two conditions**: PF-F1 (CRITICAL, fix supplied) + PF-F2 (honesty line); ii-a question
resolved by PF-F3. 5 Task parameters — d(n−2) ✓ canonical + self-consistent (PF-F9c pin); SNR grid ✓
anchored; 10⁴ symbols → PF-F5; k-grid ✓ = PR-13 row (PF-F9b). 6 Pins vs record — **exact** (§1.5–1.6);
F6 policy (a) sound with PF-F8e/f. 7 F12 completeness — PF-F8a–i; nothing over-frozen found (PR-3/PR-4
territory correctly left open). 8 Cross-references — no contradictions; one informative drop (PF-F2).

## 4. Re-derivation appendix
`/tmp/critic_pr2_linear_floor.py` (numpy, 4 seeds × 2×10⁵ test symbols): linear ±15-tap ridge equalizer
SER 2.87/0.84/0.71/0.66 % at 16/24/28/32 dB (non-causal — upper bound on any causal R1-class hybrid);
Volterra-2/3 readout 1.42/0.015/0.003/0.001 %; sticky P(1) = 0.25/0.578/0.944/0.9998/1.000 at
k = 1/3/10/30/100; M1 false-kill 1.27 % per anchor (joint ≈ 2.5 %); P(0 errors in 10⁴ | SER 1e-4) = 0.368.

---
**Protocol note:** findings go to Lucas (this file + escalation summary); the Supervisor responds, if
needed, via a revised draft or a new instructions spec — not by editing this review. If fix (i) vs (ii)
on PF-F1 is contested, that is a Lucas decision; my recommendation is (i) (R2 headline).
