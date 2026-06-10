# Critic Review Spec — the PROPOSED PR-1 + PR-2 freeze blocks (phase boundary, pre-S0.2-1)

**Filed by:** Supervisor, 2026-06-10 · **Verdict file:** `shared/critic_review_pr1-pr2-freeze.md`
**Context weight:** ledger discipline (`preregistration.md` header): *"Each entry is reviewed by
the Critic at the relevant phase boundary before the run proceeds."* PR-1/PR-2 define Gate i and
the entire bake-off object — an error frozen here propagates through S0.2–S0.5 and into the
paper. Lucas signs after (or despite) your findings; they go to him directly.

## Target

The **PROPOSED PR-1 and PR-2 blocks** at the end of `shared/preregistration.md` (Supervisor
draft, 2026-06-10) — the *choices*, not just the transcription.

Read: (1) the two blocks; (2) their design inputs — `docs/s0_2/debt2_benchmark_recon.md` +
`docs/s0_2/bakeoff_task_candidates.md` (incl. the niche-fit table §3 and PR-2 input sheet §4);
(3) the ledger constraints they must honor — Notes bullets (D-08-2, D-08-3, EV-F1/F3/F5
carry-ins, F6), the frozen PR-10 block, PR-15.1/W1; (4) `mapping_result.md` §2/§4 +
`B1_actuation_map.md`; (5) roadmap §S0.2 (Gate-i wording) + §S0.5 and the PR-3/PR-6/PR-13 ledger
rows these blocks touch.

## Checklist

1. **Transcription integrity.** Every number in both blocks traces to an [EV]-verified memo row
   or a frozen ledger value — margins (72.1 / 90.6), configs, seeds, taps/nonlinearity
   coefficients, SNR points, k-grid, channel counts. Hunt for silent edits vs the memos.
2. **PR-1 anchor choice.** G1+G3 vs the excluded G2/G4 — are the exclusion reasons sound and
   honestly stated? Is the **±1σ margin (M1)** defensible given (a) the published σ includes
   split-draw variance, (b) the Δt paper-vs-code discrepancy, (c) reimplementation/framework
   risk? Would M1 pass a hostile reviewer as "reproduced", and would a miss at e.g. 89 % on G3
   (within 2σ, above LRU) really mean the implementation is broken — i.e., is the gate
   *measuring* what Gate i means? Probe the both-must-pass rule and the 5-published-seed gated
   statistic (is the annex/gate separation clean?).
3. **PR-1 "implementation under test".** The block pins the **in-house layer** (μ=0) as the
   tested object with the official repo as cross-check only. Is that the right reading of
   Gate i (roadmap: "idealized model reproduces oscillatory-SSM task accuracy")? Any wiggle room
   an Executor could exploit unconsciously (e.g. tuning beyond the published config grid)?
4. **PR-2 headline-task choice (the big one).** T-A over T-B: the draft buys an external anchor
   (Science 2004 channel; canonical reservoir benchmark → maximal §5.3 contrast) at the cost of
   (a) a synthetic GS/s relabeling of a task the photonic-RC field ran at ~MS/s, and (b) a
   headline cell that is **memory-limited at the foundry corner** (7-dominant-tap span vs 6.58
   samples at 2 GS/s, ◑). Challenge this: does the ◑ headline cell poison Gate ii-a (capacity:
   the BPTT ceiling must clear the PR-3 utility floor) at the PR-4 foundry-grade noise cell, or
   is "ceiling-relative absorbs it" sound? Is the honesty line (RC hardware record 0.1–0.9 MS/s)
   carried loudly enough that the GS/s clock can't be read as a hardware claim? Would T-B
   headline + T-A secondary have been strictly better, or is the draft's complementarity
   (T-A headline + T-C/PR-13 secondary, T-B labelled extension) the right cut?
5. **PR-2 task parameters.** d(n−2) target convention (vs Vinckier's prose d(n)) — right call?
   SNR grid {16,24,28,32} with the 28 dB headline — is the RC anchor (SER→0 at 28/32 dB,
   50 nodes) correctly read, and is 10⁴ test symbols enough SER resolution at plausible target
   rates? The PR-13 early-registration (k-grid incl. the designed k=100 cliff) — sound, and
   consistent with the PR-13 ledger row as written?
6. **PR-2 architecture/partition/readout pins vs the record.** P2 over P1/P3/P4 (W1 cross-check
   on both axes; the D-LinOSS trained-damping argument against P3; the PR-10 ch/ring bracket
   against P1) — verify each leg against `B1_actuation_map.md` + the W1 wording. R1 pin + R2
   alternative + R3 exclusion vs EV-F5 — exact. F6 policy (a): does
   "baseline-holds-κ_ext-frozen" actually keep the reservoir contrast clean, or does the
   trainable-κ_ext arm gain a readout-strength advantage that contaminates the
   trained-recurrence-vs-trained-readout comparison itself (not just the baseline)? Chain
   topology vs the PR-10 bracket; the one-photonic-layer hybrid vs PR-1's multi-block digital
   stack (is the Gate-i ↔ bake-off-object distinction stated cleanly enough to survive S0.8?).
7. **Completeness against F12.** Anything S0.2-1/S0.3 would still have to *invent* at
   implementation time that belongs in the freeze (init distributions? Δt/timestep handling in
   the hybrid? batch/data-budget conventions? what "mean test accuracy" rounds to?) — list each
   as a finding. Conversely: anything frozen here that is properly PR-3/PR-4/PR-8 territory and
   should stay open?
8. **Cross-references both ways:** memos → blocks (informative content dropped?) and blocks →
   ledger rows PR-3/PR-6/PR-7/PR-13 (no contradictions created).

## Out of scope

Re-running the S0.2-0 sweeps (their sourcing was the run's gate, marked [EV] with a trail —
spot-check at most); the PR-3/PR-4 values themselves (later freezes); PR-15 retrievals (Lucas);
any training runs.

## Verdict

Standard format: APPROVE / APPROVE-WITH-EDITS / AMEND / REJECT + numbered severity-rated
findings. End with the one line Lucas needs: **"sign as-is" / "sign with these edits" /
"redraft"** — and if edits, give the exact replacement text per edit so the freeze can happen in
one pass.
