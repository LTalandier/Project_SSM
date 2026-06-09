# Critic Review — S0.7-lite systems-advantage envelope (S0.7L-1)

**Reviewer:** Critic session · **Date:** 2026-06-10 · **Spec:** `critic_instructions_s07lite-envelope.md`
**Target:** the S0.7L-1 run (commit `e88fbeb`) + its verdict "conditional POSITIVE — §10 clause does
not fire; binding constraint = heater class; niche = GS/s streaming, N=32–128, sub-µs, class-B required."

## Overall verdict: **APPROVE-WITH-EDITS**

**The line Lucas needs: "conditional positive" SURVIVES this audit — with its conditions restated.**
The arithmetic is fully verified (every cell reproduces in a clean-room recompute), the §10 non-firing
is robust to every perturbation I threw at it, traceability to the frozen PR-10 block is complete, and
the negatives are carried honestly. What does NOT survive: (1) the Supervisor close-out's claim that
the class-A negative is robust to a P_π/2 duty credit — it is arithmetically false at the hero
conversion corner, so the gate packet's condition "exists **only** with class-B heaters" needs a
convention qualifier (the corrected statement is *more* favorable to the program, but Lucas was given
a false robustness assurance); (2) the Executor's claim that the two flagged frozen-row readings are
verdict-neutral — both directions flip cells, including one deployable-niche cell; (3) the "~10⁵
latency edge" as phrased (it pairs our small-N bound against Brainwave's large-model bound). None of
these reverses the verdict; all three should be corrected before the gate packet is treated as final.

**What I verified independently (all PASS):**
- **Arithmetic:** deterministic re-run is byte-identical (JSON, tables, PNGs). Clean-room recompute
  from my own reading of the frozen rows: 36/36 photonic grid cells, all baseline cells, all 144
  clearance verdicts, all 12 Brainwave crossovers, and the §10 count (16 favorable-end OPT cells, all
  OPT×B at ≥1 GS/s) match exactly. Spot-checked margins: 4.4× (N=8@1) → 14.7× (6244/425, N=128@2) ✓.
- **Traceability:** every load-bearing number in script + memo traces to a frozen PR-10 row verbatim;
  the four banned legacy anchors (Ozkaya standing-power, "~5 pJ/bit DSP", Harris-2014 silicon P_π,
  silicon-derived SiN intuition) appear nowhere in the envelope artifacts (grep + read). The two
  flagged readings are **faithful to the frozen block's own source record**: 2 mW/ch is sourced there
  as per-channel DAC quiescent (AD5380, §4.7/§6.4 — heater-class-independent by provenance), and
  "38–110 µs" appears verbatim in the §4 candidate-bracket text. Neither is post-hoc convention.
- **§10 clause integrity:** the script tests exactly the registered clause ("does even the OPT corner
  clear any baseline anywhere"), favorable-end semantics correct for a kill-switch on the optimistic
  envelope, no weakening. The non-firing survives: trim dropped/doubled (≥15 cells remain), P_π/2 or
  full-P_π holding, I/Q doubling of the output chain (≥14), a 7N digital op count, and §7 exclusions
  budgeted at plausible magnitudes (laser 10–50 pJ/sample leaves all N=8–32 OPT×B cells clearing).
  The §7 asymmetry claim is correct: all four exclusions are photonic-side adders — negatives robust,
  positives shrink.
- **C5 re-derivation (fair to digital): 14·N is correct and matched.** Complex state update 6 ops +
  input 4 + readout-Re 3 + accumulate 1 = 14; 1 MAC = 2 ops consistent with the baselines' FLOPS
  conventions. The real-block (conjugate-pair section) digital equivalent also costs 14 ops/pole, so
  no hidden halving exists **for the adopted D-08-2 architecture** (one ring = one independent pole).
  Coupling worth recording: if PR-2 ever reverted to conjugate-paired rings on a real-I/O task, the
  digital side halves to 7N and four deployable-corner CLEARS die (CONS×B N=32 vs Brainwave at 1 and
  2 GS/s; N=128 vs Jetson-sustained at both) — D-08-2's no-pairing choice is load-bearing here too.
- **Honesty checks:** Jetson-peak-never-beaten is in the headline, §5.1, results_log, and the gate
  packet at equal volume ✓; class-A-loses and the 0.1-GS/s double exclusion (energy AND sub-sample
  memory) carried ✓; the class-B-vs-CORNERSTONE tension is visible in the memo verdict paragraph
  itself and in the packet ✓; verdict semantics ("assumption-driven, NOT outreach-load-bearing")
  stated identically in memo, results_log, close-out, packet ✓. One conservative asymmetry the memo
  doesn't claim credit for: the digital baselines are charged **zero** front-end conversion although
  the niche workload is an analog stream (a digital competitor would also pay an ADC) — direction
  favors the baselines; honest.

---

## Findings

### EV-F1 (HIGH) — The close-out's robustness claim is false: under a P_π/2 duty credit, hero-corner class A *does* win inside the window; "class-B required" is C4-conditional

Task-queue close-out: *"the class-A negative survives even a P_π/2 duty-credit relaxation, so the
'heater class is the binding constraint' finding is robust to convention."* **Re-derived: false.**
With holding = P_π/2 (trim kept at 2 mW/ch), OPT×A clears Brainwave at N=8/32/128 @ 2 GS/s
(e.g. N=8: 293–297 vs 390 pJ), with crossovers at **1.32–1.47 GS/s — inside the registered window**
(the unrelaxed crossovers 2.56–2.84 sit only 1.3–1.4× above the 2 GS/s ceiling, so any ≥1.4× credit
pulls them in; this is visible from the memo's own crossover table). CONS×A remains dead under the
same credit (8.4–15 GS/s) ✓. Note P_π/2 is not a generous credit: for uniform fab placement the
short-way trim is uniform in [0, π], so **P_π/2 is the *expected* holding power** and C4's full-P_π
is the per-ring worst case (≈2× conservative in expectation, on top of trim being charged additively).

The envelope memo itself is internally honest (C4 stated up front, no credit taken, direction
declared). The error is in transit: the close-out asserts a robustness that does not exist, and the
gate packet's condition (1) — "it exists **only** with suspended (class-B) heaters" — inherits the
flat form. **Corrected statement for the gate:** *under the registered worst-case holding convention
(C4), class A never wins in-window; at expected-value holding (P_π/2), the hero-conversion corner
(OPT×A) clears the FPGA serving anchor above ~1.3–1.5 GS/s with foundry heaters — but the deployable
corner (CONS×A) requires class B under any holding convention.* This *softens* the principal Stage-1
fab condition in the program's favor while removing a false assurance. **Fix:** one-line correction
in `task_queue.md` close-out + the packet; carry both holding conventions as labelled rows at
S0.7-full (and PR-4 should eventually register a trim-statistics convention).

### EV-F2 (MEDIUM) — The C3 trim reading is load-bearing, not verdict-neutral; the Executor's "neither affects any clearance verdict" fails in both tested directions

Results-log anomaly (i) claims neutrality, argued via class-A proportions ("≤2/62 of class-A channel
power") — but the exposure is in class B, where trim (2 mW) is 2× the heater power (1 mW/π).
Re-derived: **dropped** (the typographic reading — trim absent from class B): **15 verdicts flip
favorably**, including OPT×B clearing Brainwave at N=8–128 @ 0.1 GS/s — i.e. the §3/§4 *rate-floor
negative* ("everything loses at 0.1 GS/s") is partly a C3 artifact at the OPT corner (the memory-depth
exclusion at 0.1 GS/s is foundry-corner-only: class-leading holds 4.9 samples there). **Doubled**
(4 mW/ch): 3 flips — the boundary DSP cell (OPT×B N=32@1: CLEARS→OVERLAP), CONS×B N=32@1 vs DSP
(OVERLAP→LOSES), and **CONS×B N=128@1 vs Jetson-sustained (CLEARS→LOSES)** — the last is one of the
deployable-corner niche cells cited in results-log finding 3. The adopted reading (charge everywhere)
is provenance-faithful and the right choice — keep it — but the neutrality sentence must be replaced
with: *the rate-floor finding at the OPT corner and two deployable-corner cells are sensitive to
±2 mW/ch of control-electronics assumption.* (For class B, the AD5380-class low-voltage part is the
consistent pairing, so 2 mW/ch is well-sourced; 4 mW is a stress test, not a sourced alternative.)

### EV-F3 (MEDIUM) — The N=128 advantage cells inherit S0.1's open item F8: no WDM needed, but N=128 *distinct* poles needs the class-leading corner

Answer to the spec's C8 question: **single-carrier-one-FSR is λ-plan-consistent at N=128** — the
reachable detuning span is one FSR wide (±π·FSR ≈ 314 Grad/s, `mapping_notes.md` §4) while the signal
band at 2 GS/s needs only ±π·f_s ≈ 6.3 Grad/s; placement and holding are covered by C4's full-P_π
charging. WDM is **not** required; that fear is resolved. The real constraint is linewidth packing:
poles useful to the task must sit within the signal band, and the foundry corner's intrinsic
linewidth (96.7 MHz at Q_i=2×10⁶; wider once loaded per the B3 κ_ext policy) caps the number of
*informationally distinct* poles per GHz of band at O(10–20). The class-leading corner (6.4 MHz)
supports ~150. So the §6 sentence "margins grow with N via C8" and the CONS×B large-N rescue
implicitly assume the class-leading platform corner — which is exactly the splitting-prone corner
(D-08-3) that PR-4 must adjudicate jointly with D-08-1. The frozen block is internally honest (its
own source record §5 states N is "not set by S0.1 — registered open item F8"), but the memo claims
the N=128 cells without restating that caveat. **Fix:** one sentence in §6 + carry the
{N=128 ⇄ class-leading-Q ⇄ splitting} coupling into the PR-2/PR-4 framing. Damping diversity
(trainable κ_tot spread) relaxes the cap somewhat — quantifying that is legitimate S0.3/S0.4 work,
not a lite assumption.

### EV-F4 (MEDIUM) — The "~10⁵ latency edge" pairs a small-N photonic bound with Brainwave's large-model bound; the honest matched-N ratio is ~10²–10³

Brainwave's "<4 ms" is the author bound for *all DeepBench layers* (large GRUs, hundreds of
timesteps). A 14·N ≈ 450-op step on the same FPGA class would serve in µs-class, not ms. The frozen
row registers only "<4 ms author-stated" — so the envelope could not do better numerically; but the
ratio that travels ("~10⁵", now in the gate packet) overstates the matched-workload contrast by ~2
orders. The niche-defining claim survives untouched: tens-of-ns photonic vs µs-class FPGA pipelines
vs ms-class serving stacks still forces sub-µs workloads off digital serving. **Fix:** restate as
"sub-µs unreachable by the serving class (<4 ms author bound); ≥10² vs any plausible matched-N FPGA
pipeline" and register a matched-N FPGA latency row at S0.7-full. Side note (conservative, fine): the
photonic LB includes T_mem, which is response depth, not pipeline delay — it inflates the photonic
side's own bound; keep, but label at S0.7-full.

### EV-F5 (MEDIUM) — The OPT×B-vs-DSP N=32 cell is boundary (confirmed treated as such) and dies under any output-chain doubling; single-quadrature homodyne is the configuration that keeps C5/C8 consistent

Confirmed: the ~1% clearance (233.3 vs 235 pJ) is called "boundary, not margin" in memo §3, anomaly
(ii), and nowhere upgraded ✓. My sensitivity check: if PR-2 pins a complex-output readout requiring
I/Q detection (2× ADC + O/E), that cell goes OVERLAP, and **CONS×B N=32@1 vs Brainwave flips to
LOSES** (1643–1653 vs 1561) — the deployable corner then starts at N=128. The consistency point: C5's
op count already assumes a *real* output y = Re(Σc_j x_j), and a real output needs only
single-quadrature homodyne = one O/E + one ADC, which is exactly C8's single chain. So the envelope
is self-consistent **iff** the readout is single-quadrature (or intensity); the LO and its phase
locking sit in the §7 exclusions (listed ✓). **Fix:** make "single-quadrature/intensity readout" an
explicit named condition of C8 in the memo, and a stated input to the PR-2 readout pin (F6 thread).

### EV-F6 (LOW) — C7 (flat pJ/sample) is defensible as vendor-class density but does heavy lifting at the 0.28–0.5 GS/s crossovers

Read literally (the named TI parts run below native rate), CONS conversion at 1 GS/s would be
~3–6× worse and CONS×B N=32 would die even at 2 GS/s. Read as "a rate-matched vendor part of equal
pJ/sample-at-ENOB" — the correct class reading, consistent with the Murmann envelope's near-flat
energy/sample at fixed ENOB — the cells stand; vendor parts at ~1 GS/s with ~hundreds of pJ/sample
exist. The memo's flag is adequate for lite. **Fix at S0.7-full:** source one named ~1-GS/s-class
converter pair to close the loop; treat the CONS×B crossovers (0.28–0.50) as ±2× soft until then.

### EV-F7 (LOW) — Cadence-row provenance niceties

"38–110 µs": 38 µs = 0.35/9.2 kHz exactly (Muñoz BW, with the source record's own unit-ambiguity
caveat flagged there); 110 µs ≈ 1/(9.2 kHz) — a full-period settle convention, derivable but
unstated. Class-B "0.4 ms" low end traces to the *simulation* row (Alemany BW 0.9 kHz → 0.39 ms)
while 2.6 ms is the unverified-body Zeng value. All cadence-only (no clearance impact). **Fix:** one
provenance line in memo §4; verify the Muñoz τ unit before PR-4 if SPSA cadence becomes load-bearing.

---

## Checklist disposition (spec §Checklist)

1. **Traceability:** PASS (banned anchors absent; all rows trace; flagged readings faithful to the
   frozen source record). 2. **Flagged readings:** faithful, but **not** verdict-neutral → EV-F2.
3. **Conventions:** C5 re-derived fair and matched (no conjugate-halving for the D-08-2 architecture);
   C6 conservative direction (ENOB < nominal bits) ✓, boundary cell honestly labelled ✓; C8 λ-plan
   consistent, no WDM needed, but N=128 capacity caveat → EV-F3; C4 conservative as stated, but the
   binding-constraint *interpretation* is C4-conditional → EV-F1; C7 adequate at lite → EV-F6.
4. **Re-run + re-derivation:** byte-identical re-run; 36/36 cells + all verdicts + all crossovers
   reproduce; >6 cells hand-checked across all four scenarios ✓. 5. **§10 clause:** exact clause,
   correct semantics, non-firing robust to all tested perturbations and exclusions ✓.
6. **Niche/verdict honesty:** semantics label correct everywhere; negatives at equal volume;
   class-B/CORNERSTONE tension visible in the verdict paragraph ✓; residual wording fixes → EV-F1/F4.
7. **§10 soft spot (conversion honesty):** full chain charged per sample, no duty credits, no
   double-counting; baselines charged zero front-end conversion (conservative) ✓.
8. **Claim drift:** memo ↔ results_log ↔ close-out ↔ gate packet consistent **except** the close-out's
   false robustness sentence (EV-F1) and the packet's flat condition (1) + "~10⁵" (EV-F1/EV-F4).
   Packet's "rate floor ≈0.5 GS/s" is the deployable-corner floor (memo: 0.15–0.5) — acceptable, the
   honest single number.

## Effect on the gate input

**"Conditional POSITIVE" stands.** The §10 clause non-firing is the audit's most robust result. The
conditions should read, post-audit: (1) *deployable-corner* energy advantage requires class-B
heaters (non-CORNERSTONE) under any holding convention; the *hero* corner clears the FPGA anchor
with foundry heaters at ≥1.3–1.5 GS/s under expected-value holding (C4-conditional statement —
EV-F1); (2) rate floor ≈0.5 GS/s deployable / ≈0.13 GS/s hero, ±2× soft pending rate-matched
converter sourcing (EV-F6), reinforced by sub-sample memory at the foundry corner only (EV-F2);
(3) Jetson-peak is never beaten — unchanged, and the peak≠sustained caveat remains the single most
case-threatening S0.7-full retrieval; (4) **new:** the N=128 margins assume the class-leading-Q
corner (couples to the PR-4 splitting decision — EV-F3) and a single-quadrature/intensity readout
(couples to the PR-2 readout pin — EV-F5). Fixes EV-F1/F2 are one-line corrections to close-out +
packet + results_log; EV-F3/F4/F5 are sentences in the memo §6/§4 + PR-2/PR-4 carry-ins; EV-F6/F7
are S0.7-full items.
