# S0.7-lite systems-advantage envelope (PR-10 🔒 FROZEN)

**Task:** S0.7L-1 · **Author:** Executor · **Date:** 2026-06-10 · **Governing pre-registration:**
**PR-10, 🔒 FROZEN 2026-06-10** (`shared/preregistration.md`, "PR-10 — FROZEN values") — every
load-bearing number below traces to a frozen PR-10 row, cited per use; memo refs (§1–§5, row
numbers) point into the frozen block's source record `docs/s0_7/pr10_assumption_sources.md`.
**No new sourcing was done.** Arithmetic: `analysis/s0_7_lite_envelope.py` (pure arithmetic +
plots; no simulation); raw outputs `results/s0_7/` (JSON, tables, 2 PNGs).

**Verdict semantics (roadmap v3.1 §S0.7-lite, stated up front):** this envelope is
**assumption-driven**. A positive result is **NOT outreach-load-bearing** before the full S0.7;
a negative result escalates as a *Stage-1-reframing* finding and does not kill Stage 0.

**Headline (details in §5–§7):** **conditional positive — a low-latency niche plausibly exists,
and the binding condition is the heater class, not the conversion stack.** The §10 escalation
clause does **not** fire (16 OPT grid cells clear at least one named baseline). But no scenario
beats the Jetson *peak* FoM anywhere, and every class-A (foundry-heater) scenario loses
everywhere inside the registered rate window — the energy case exists only with suspended
(class-B) heaters, which the frozen row itself marks **non-CORNERSTONE** at ms-class τ.

---

## 1. Assumption table (verbatim from frozen PR-10; row ref per use)

| Quantity used | Value used (verbatim) | Frozen PR-10 row | Memo ref |
|---|---|---|---|
| E/O incl. driver, OPT | 0.135 pJ/bit (hybrid TX, 10 Gb/s) | "E/O incl. driver", OPT | §1 (1.4) |
| E/O incl. driver, CONS | 10–20 pJ/bit (monolithic measured / Miller class) | "E/O incl. driver", CONS | §1 (1.5, 1.6) |
| O/E (PD+TIA), OPT | 0.17 pJ/bit (25 Gb/s best-case) | "O/E (PD+TIA)", OPT | §1 (1.8) |
| O/E (PD+TIA), CONS | 1.4 pJ/bit (measured 64 Gb/s) | "O/E (PD+TIA)", CONS | §1 (1.9) |
| ADC, OPT | ≈32 pJ/sample @ 9.4 ENOB | "ADC at GS/s", OPT | §2 (2.9) |
| ADC, CONS | ≈469 pJ/sample @ 8.4 ENOB (TI ADC12DJ3200) | "ADC at GS/s", CONS | §2 (2.4–2.6) |
| DAC, OPT | 5–9 pJ/sample (8b research, ~4.6 ENOB at extreme rate) | "DAC at GS/s", OPT | §2 (2.10) |
| DAC, CONS | ≈308 pJ/sample (TI DAC38RF82) | "DAC at GS/s", CONS | §2 (2.7–2.8) |
| Heater class A power | P_π ≤175 mW/π (foundry bound; 60–385 measured span) + 2 mW/ch trim | "Heater class A" | §4 |
| Heater class A τ | fast τ (per the row's §4 ref: ~38–110 µs non-isolated class) | "Heater class A" | §4 (4.2, 4.4) |
| Heater class B | ~1 mW/π at τ = 0.4–2.6 ms (**non-CORNERSTONE**; couples to SPSA cadence) | "Heater class B" | §4 |
| N grid | {8, 32, 128} | "Operating scale" | §5 |
| Line-rate class | 0.1–2 GS/s | "Operating scale" | §5 |
| λ-plan | single-carrier-one-FSR (WDM = labelled extension, NOT used) | "Operating scale" | §5 |
| Control channels | 2–4 ch/ring | "Operating scale" | §5 |
| Memory | 329→4937 rt = 3.29→49.4 ns by platform corner (S0.1) | "Operating scale" | §5 + `mapping_result.md` §4 |
| Baseline: Brainwave | batch-1 GRU streaming, 287 GFLOPS/W (author-stated); <4 ms batch-1 | "Digital baselines (F16)" | §3 (3.1) |
| Baseline: coherent-DSP ASIC | 25–170 pJ/bit (GS/s streaming-FIR anchor) | "Digital baselines (F16)" | §3 (3.7, 3.8) |
| Baseline: Jetson AGX Orin | 275 peak sparse INT8 TOPS / 15–60 W → ≈4.6 TOPS/W peak (derived); caveat peak ≠ sustained, <13% measured GPU util. on small-batch RNNs | "Digital baselines (F16)" | §3 (3.9 + class notes) |
| Baseline: MARCA / LightMamba | qualitative only (relative-only perf/W) | "Digital baselines (F16)" | §3 (3.3, 3.4) |

The baselines are **not corner-split** (frozen row). The frozen block's adopted discrepancy
corrections are honored: no Ozkaya standing-power, no "~5 pJ/bit DSP", no Harris-silicon heater
number appears anywhere in this envelope.

## 2. Stated mapping conventions (per the frozen output convention)

The frozen block states: *"no GHz-sample-stream SSM accelerator exists in the literature, so the
closest-workload mapping convention is stated in the output, not invented post hoc."* The
conventions, fixed before the arithmetic ran (mirrored in the script header):

- **C1 — E/O and O/E charged per symbol (= per sample).** The cited pJ/bit figures are NRZ
  per-symbol measurements; modulator/receiver energy is per modulation event, not per bit of
  amplitude resolution.
- **C2 — corner-bound bracket ends.** Within a corner, every frozen bracket resolves to its
  corner-consistent end (OPT favorable, CONS unfavorable): class-A P_π → 60 mW (OPT) / 175 mW
  (CONS, the registered foundry bound); ch/ring → 2 (OPT) / 4 (CONS). Brackets that stay wide at
  one corner (CONS E/O 10–20, OPT DAC 5–9, DSP class 25–170) are carried as ranges through the
  arithmetic — result cells are ranges, no midpoints.
- **C3 — trim electronics (2 mW/ch) charged in all four scenarios.** The frozen figure is a
  per-channel DAC-quiescent number (heater-class-independent); it appears typographically in the
  class-A row only. Omitting it for class B would flatter the photonic side. **Flagged reading.**
- **C4 — holding power = full P_π per control channel at 100% duty** (streaming inference;
  worst-case phase holding). No duty-factor credit taken.
- **C5 — digital workload = diagonal complex SSM, 14·N ops/sample** (state update a_j·x_j: 6 ops,
  + b_j·u: 2+2 ops; readout Re(c_j·x_j): 3 ops + 1 accumulate; 1 MAC = 2 ops, matching the
  FLOPS/TOPS conventions of the baseline sources).
- **C6 — DSP-class pJ/bit → pJ/sample via bits/sample = the corner's ADC ENOB-at-speed** (9.4
  OPT / 8.4 CONS — the information content of one analog sample). The anchor is N-independent
  (streaming-FIR class), so it is a workload-*class* comparison, not matched-N.
- **C7 — frozen converter pJ/sample used flat across the 0.1–2 GS/s grid.** Favorable to the
  photonic side below the named parts' native rates; flagged.
- **C8 — one DAC/ADC + E/O + O/E chain per sample, N-independent** (single-carrier-one-FSR plan:
  the recurrence is fully optical; conversion happens once per sample, not per ring). This is the
  architecture's structural premise and the source of the large-N scaling advantage in §3.
- **Heater-class consistency rule (frozen):** each scenario uses ONE heater class for both its
  power row and its τ/SPSA-cadence row. All four corner × class combinations are reported — no
  cherry-picking.

## 3. Energy per sample — results (pJ/sample; ranges from frozen brackets per C2)

Photonic = conversion stack (N-independent, C8) + control holding power / f_s.

### Photonic, four scenarios

| Scenario | conversion [pJ] | control [mW] | N=8 @1GS/s | N=32 @1GS/s | N=128 @1GS/s | N=128 @0.1 | N=128 @2 |
|---|---|---|---|---|---|---|---|
| OPT×A | 37–41 | 124·N | 1 029–1 033 | 4 005–4 009 | 15 909–15 913 | 158 757–158 761 | 7 973–7 977 |
| **OPT×B** | 37–41 | 6·N | **85–89** | **229–233** | **805–809** | 7 717–7 721 | **421–425** |
| CONS×A | 788–798 | 708·N | 6 452–6 462 | 23 444–23 454 | 91 412–91 422 | 907 028–907 038 | 46 100–46 110 |
| CONS×B | 788–798 | 12·N | 884–894 | 1 172–1 182 | 2 324–2 334 | 16 148–16 158 | 1 556–1 566 |

(Full 4 × 3 × 3 grid: `results/s0_7/s0_7_lite_tables.md` + JSON.)

### Named baselines (C5/C6)

| N | Brainwave (287 GFLOPS/W) | Jetson-peak (4.6 TOPS/W) | Jetson-sustained (13% util) | DSP-ASIC class (C6, N-indep.) |
|---|---|---|---|---|
| 8 | 390 | 24 | 187 | 235–1 598 (OPT) / 210–1 428 (CONS) |
| 32 | 1 561 | 97 | 749 | (same — workload-class anchor) |
| 128 | 6 244 | 390 | 2 997 | (same) |

MARCA / LightMamba: cited qualitatively per the frozen row (relative-only perf/W; LLM-decode
workload, not a GS/s sample stream) — no numeric cell.

### Clearance (photonic conservative high end vs baseline) — the load-bearing pattern

- **OPT×B:** CLEARS Brainwave, Jetson-sustained at all N at 1–2 GS/s (margins 4.4× → 14.7× vs
  Brainwave); CLEARS the full DSP band at N ≤ 32 — at N=32 by ~1% only (233 vs 235 pJ) —
  (overlaps it at N=128); LOSES to everything at
  0.1 GS/s except a DSP overlap at N=8. **LOSES to Jetson-peak everywhere.**
- **OPT×A:** LOSES everywhere in the grid (two DSP overlaps at N=8 are the only non-losses).
- **CONS×A:** LOSES everywhere, vs everything (16–30 GS/s would be needed to cross Brainwave).
- **CONS×B:** CLEARS Brainwave at N ≥ 32 at 1–2 GS/s and Jetson-sustained at N=128; otherwise
  loses/overlaps. The deployable-converter corner is rescued at large N by C8 (conversion is
  N-independent while digital cost ∝ N).

### Crossover rate vs Brainwave (GS/s; "never" = conversion alone exceeds the baseline)

| N | OPT×A | OPT×B | CONS×A | CONS×B |
|---|---|---|---|---|
| 8 | 2.84 | **0.14** | never | never |
| 32 | 2.61 | **0.13** | 29.7 | **0.50** |
| 128 | 2.56 | **0.12** | 16.6 | **0.28** |

**Class-A crossovers sit at or above the 2 GS/s registered ceiling in every cell** — the
foundry-heater scenarios cannot win inside the frozen rate window even with hero conversions.

## 4. Latency per sample

Converter pipeline latency is **not a frozen PR-10 row** → only a lower bound is reported
(ring amplitude-memory timescale + 1 sample period per converter stage); the pipeline adder is a
registered gap for S0.7-full.

| GS/s | photonic LB, foundry corner | photonic LB, class-leading | Brainwave (batch-1, author-stated) |
|---|---|---|---|
| 0.1 | ≥23.3 ns | ≥69.4 ns | <4 ms |
| 1 | ≥5.3 ns | ≥51.4 ns | <4 ms |
| 2 | ≥4.3 ns | ≥50.4 ns | <4 ms |

Restated per Critic **EV-F4** (the earlier "~10⁵" ratio paired our small-N bound against
Brainwave's *large-model* author bound — all DeepBench layers, not a matched workload): **sub-µs
latency is unreachable for the batch-1 FPGA serving class (<4 ms author-stated bound), and
against any plausible matched-N FPGA pipeline (µs-class for a 14·N ≈ 450-op step on the same
FPGA class) the photonic edge is ≥10²** — tens-of-ns photonic vs µs-class matched pipelines vs
ms-class serving stacks; a matched-N FPGA latency row is registered for S0.7-full. The
coherent-DSP ASIC class operates natively at GS/s line rates (no registered latency row — not
numerically compared). Jetson: no registered latency row.

**Memory-depth coupling (frozen memory corners × rate grid):** T_mem·f_s = 0.33 / 3.29 / 6.58
samples (foundry corner at 0.1/1/2 GS/s) and 4.9 / 49.4 / 98.8 (class-leading). At 0.1 GS/s the
foundry corner holds **less than one sample** of memory — the bottom of the rate window is
excluded by memory arithmetic as well as by energy (§3).

**SPSA-cadence consistency (frozen rule):** class A: ≥0.08–0.22 ms/iteration (2 settles);
class B: **≥0.8–5.2 ms/iteration**. Every energy-winning scenario is class B and therefore buys
its inference-energy case at ms-class in-situ training cadence (~10⁴ SPSA iterations ≈ 8–52 s
physical time floor) — consistent pairing, reported, decision deferred.

Cadence provenance (Critic **EV-F7**): class-A "38 µs" = 0.35/9.2 kHz exactly (Muñoz bandwidth,
carrying the source record's own unit-ambiguity caveat); "110 µs" ≈ 1/(9.2 kHz) — a full-period
settle convention, derivable but unstated in the source. Class-B "0.4 ms" low end traces to the
*simulation* row (Alemany BW 0.9 kHz → 0.39 ms); 2.6 ms is the unverified-body Zeng value.
Cadence-only — no clearance impact; verify the Muñoz τ unit before PR-4 if SPSA cadence becomes
load-bearing.

## 5. §10 escalation-clause check (explicit)

**Clause: does even the OPT corner clear any baseline anywhere in the grid? — YES → the clause
does NOT fire.** 16 OPT grid cells (favorable end; all in OPT×B at ≥1 GS/s) clear at least one
named baseline; example: OPT×B, N=32, 1 GS/s = 229–233 pJ/sample vs Brainwave 1 561 pJ/sample.
No `escalate_to_human.md` entry is drafted (the negative branch was not triggered).

Honest qualifiers attached to the non-firing:
1. **No scenario beats the Jetson peak FoM anywhere** (24–390 pJ/sample). The case against the
   embedded GPU rests entirely on the registered peak ≠ sustained caveat (<13% measured
   utilization on batch-1 RNN serving). If an embedded GPU sustained peak TOPS on this workload,
   no photonic cell in this envelope would win. For S0.7-full: a *measured* sustained embedded-GPU
   number on a matched streaming workload is the single most case-threatening retrieval.
2. The OPT corner is **hero-class by construction** (0.135 pJ/bit hybrid TX; 32 pJ/sample
   research ADC) — that is what the frozen two-corner design intends OPT to be, and it is why a
   positive lite verdict is labelled assumption-driven.

## 6. Niche statement (explicit) — input to the S0.2 task choice / PR-2

**A plausible low-latency niche EXISTS, conditionally:**

> GS/s-class streaming inference — line rate ≥ ~0.5 GS/s (covering the CONS×B crossover at
> N=32; the OPT×B floor is ~0.13 GS/s), state dimension N = 32–128 (margins grow with N via C8),
> per-sample latency requirement ≲ 1 µs (which the batch-1 FPGA serving class cannot meet at
> <4 ms, and which forces the comparison onto the DSP-ASIC/embedded classes) — **provided the
> platform has suspended/undercut (class-B) heaters.**

Three conditions, stated as sharply as the arithmetic gives them:
1. **Heater class is the binding constraint** — not conversion. Class-B (~1 mW/π) wins; class-A
   (60–175 mW/π) never wins inside the rate window. The frozen class-B row is
   **non-CORNERSTONE** (no undercut in that MPW flow): the energy niche as computed is **not
   reachable in the currently-named foundry flow** — a Stage-1 platform/fab constraint to carry
   into PR-2/PR-4 framing and any MPW decision.
2. **Rate floor ~0.15–0.5 GS/s** (energy amortization of holding power) — reinforced
   independently by memory arithmetic (sub-sample foundry-corner memory at 0.1 GS/s). The niche
   lives at the 1–2 GS/s end of the registered window.
3. **The advantage is vs serving-class and utilization-limited digital** (Brainwave,
   Jetson-sustained, DSP-band at small-mid N) — never vs peak-FoM silicon (§5.1).
4. **Two audit-added conditions (Critic carry-ins).** The N=128 margin cells additionally assume
   the **class-leading-Q platform corner**: linewidth packing caps the number of informationally
   distinct poles per GHz of signal band at O(10–20) at the foundry corner (96.7 MHz intrinsic
   linewidth) vs ~150 class-leading (6.4 MHz) — and class-leading is exactly the splitting-prone
   corner, so this couples to the PR-4 decision jointly with D-08-1 (**EV-F3**). And C8's single
   conversion chain holds **iff the readout is single-quadrature (homodyne) or intensity** — an
   I/Q readout doubles the output chain, kills the boundary OPT×B-vs-DSP N=32 cell and flips
   CONS×B N=32 vs Brainwave to LOSES — a stated input to the PR-2 readout pin (F6 thread)
   (**EV-F5**).

**S0.2 task-choice implication (input only; the choice is PR-2/Supervisor):** the bake-off task
should be a streaming signal-processing task at an effective ≥0.5 GS/s line rate with
N≈32–128 states and sub-µs latency relevance — the equalization-class family is rate-consistent
with S0.1's linewidth-derived class; an LLM-decode-style task would sit outside the niche this
envelope identifies.

## 7. Registered exclusions — UNBUDGETED (frozen "registered exclusions at lite")

Deferred to the S0.7-full F16 ledger, charged **nowhere** in §3: **laser wall-plug power · active
locking · control-loop digital compute · packaging/thermal.** All four would add to the photonic
side only. Therefore: the **negative** findings (class-A loses; sub-0.13 GS/s loses; Jetson-peak
never beaten) are robust to the exclusions, while every **positive** cell is an upper bound on
advantage and shrinks as exclusions are budgeted. The OPT DAC's ~4.6-ENOB-at-extreme-rate caveat
and the precision→accuracy link are likewise S0.7-full scope (F16).

## 8. Verdict (per roadmap v3.1 semantics)

**Conditional POSITIVE — labelled assumption-driven, NOT outreach-load-bearing.** The §10 clause
does not fire; no Stage-1-reframing escalation is drafted. The niche exists in the frozen-number
arithmetic only under {OPT or CONS conversions} × {class-B heaters} × {≥0.5 GS/s} × {N ≥ 32 for
the deployable corner}, against serving-class/sustained baselines, with the §7 exclusions
unbudgeted and the class-B-vs-CORNERSTONE fab tension (§6.1) flagged as the principal Stage-1
condition. Pipeline consequence: the pre-S0.2 continuation gate's envelope input is in hand;
S0.2 task registration (PR-2) can size against §6.
