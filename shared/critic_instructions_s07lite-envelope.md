# Critic Review Spec — S0.7-lite systems-advantage envelope (S0.7L-1)

**Filed by:** Supervisor, 2026-06-10 · **Verdict file:** `shared/critic_review_s07lite-envelope.md`
**Context weight:** this result is one of the two inputs to the **pre-S0.2 continuation gate**
(`shared/escalate_to_human.md` E-2026-06-10-3) — Lucas's go/no-go on the entire bake-off arm
(S0.2–S0.5). Lucas may rule before your audit lands (his choice); file your findings regardless —
they reach him directly, not through the Supervisor.

## Target

The S0.7-lite envelope run (Executor, 2026-06-10, commit `e88fbeb`) and its verdict:
**conditional POSITIVE — §10 escalation clause does NOT fire; the binding constraint is the
heater class, not the conversion stack; niche = GS/s streaming, N=32–128, sub-µs latency,
class-B heaters required.**

Read (in this order):
1. `shared/preregistration.md` — the **PR-10 🔒 FROZEN block** (the governing pre-registration)
2. `docs/s0_7/s07_lite_envelope.md` — the envelope memo (assumption table §1, conventions §2,
   results §3–§4, §10-clause check §5, niche §6, exclusions §7, verdict §8)
3. `analysis/s0_7_lite_envelope.py` + `results/s0_7/` (JSON, tables, 2 PNGs)
4. `docs/s0_7/pr10_assumption_sources.md` — the frozen block's source record (memo refs §1–§5)
5. `shared/results_log.md` — the S0.7L-1 entry (top)
6. `shared/stage0_roadmap.md` §S0.7-lite — the verdict semantics the memo claims to follow

## Checklist

1. **Traceability audit (the run's primary gate).** Every load-bearing number in the memo and
   script must trace to a frozen PR-10 row. Hunt for: numbers not in the frozen block; frozen rows
   misquoted; and the four excluded legacy anchors (Ozkaya standing-power; "~5 pJ/bit 800G DSP";
   Harris-2014 silicon heater number; silicon-derived SiN P_π intuition) appearing anywhere.
2. **The two Executor-self-flagged frozen-row readings** (results entry, "Anomalies"):
   (a) **C3** — 2 mW/ch trim electronics charged in **all four** scenarios although the figure sits
   typographically in the class-A row; (b) class-A "fast τ" resolved via the row's memo-§4
   reference (38–110 µs non-isolated). Are these faithful readings of the frozen block or post-hoc
   convention? Does either change ANY clearance verdict (Executor claims no — verify both
   directions: dropped and doubled)?
3. **Mapping conventions C1–C8** — stated *before* the arithmetic per the frozen output
   convention (check the script header mirrors memo §2). Probe hardest at:
   - **C5** (digital workload = 14·N ops/sample, diagonal complex SSM): is the op count fair *to
     the digital side*? Re-derive it.
   - **C6** (DSP-class pJ/bit → pJ/sample via ENOB-at-speed bits): defensible, or does it flatter
     the photonic side? The OPT×B-vs-DSP clearance at N=32 is **by ~1%** (233 vs 235 pJ) — the
     Executor calls it boundary, not margin; confirm it is not presented as margin anywhere.
   - **C8** (one conversion chain per sample, N-independent — the source of ALL large-N
     advantage): is single-carrier-one-FSR actually consistent with N=128 rings, given the frozen
     scale row and S0.1's pole-region/FSR numbers (`docs/s0_1/mapping_result.md` §4)? If N=128
     requires WDM (a labelled extension, NOT frozen), say so loudly — it would cut the niche to
     N≈32.
   - **C4** (full P_π holding, 100% duty): direction of conservatism per scenario.
   - **C7** (frozen converter pJ/sample flat across 0.1–2 GS/s): the memo flags it favorable
     below native rates — adequate, or does it change a verdict cell?
4. **Independent arithmetic re-run.** The script is pure arithmetic (<1 s, no seeds): re-execute
   it; check outputs match `results/s0_7/`; independently re-derive ≥6 grid cells across all four
   scenarios + the full crossover-rate table. (The Supervisor hand-checked 5 cells and a
   duty-credit relaxation of the class-A negative — do NOT trust that; re-derive your own.)
5. **§10 escalation-clause integrity.** The clause: "does even the OPT corner clear any baseline
   anywhere in the grid?" Verify the memo checked exactly that clause (no weakening), and stress
   the non-firing: does it survive the §2-flagged readings, plausible C-convention perturbations,
   and the §7 unbudgeted exclusions (which the memo claims only shrink positive cells — verify
   that asymmetry claim)?
6. **Honesty of the niche statement (§6) and verdict label (§8).** Roadmap v3.1 semantics:
   positive = "assumption-driven, NOT outreach-load-bearing". Is anything in the memo or
   results-log entry stated more strongly than that? Are the negatives carried at equal volume
   (Jetson-*peak* never beaten anywhere; class-A loses everywhere in-window; 0.1 GS/s dead on
   energy AND memory)? Is the class-B-vs-CORNERSTONE fab tension (the niche is NOT reachable in
   the currently-named foundry flow) stated where a reader of the verdict alone would see it?
7. **The standing §10 soft spot (your onboarding):** is the conversion overhead paid honestly —
   full E/O–O/E + DAC/ADC chain, charged per the stated conventions, no double-counting credits?
8. **Claim-drift check:** results_log entry vs memo vs `task_queue.md` close-out vs the
   E-2026-06-10-3 gate packet — same verdict, same conditions, no strengthening in transit.

## Out of scope

PR-15/white-space (closed — your Part 2 verdict stands); the S0.2 task choice (PR-2, pending the
gate); re-sourcing assumptions (PR-10 is frozen — if a frozen value is *wrong*, that is a finding
about the freeze, severity-rated, for Lucas, not a license to re-source the envelope).

## Verdict

Standard format (`critic_instructions.md`): APPROVE / APPROVE-WITH-EDITS / AMEND / REJECT +
numbered severity-rated findings. State explicitly whether any finding **changes the gate input's
weight** (i.e. whether "conditional positive" survives your audit) — that one line is what Lucas
needs from you.
