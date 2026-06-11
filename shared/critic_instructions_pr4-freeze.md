# Critic instructions — PR-4 phase-boundary review (substrate freeze)

**Filed:** 2026-06-11 (Supervisor). **Target:** the **PROPOSED PR-4 block** at the end of
`shared/preregistration.md` (substrate cell for S0.3-1 + Gate ii + the S0.5 bake-off).
**Output:** file your review as `shared/critic_review_pr4-freeze.md`; verdict APPROVE /
APPROVE-WITH-EDITS / AMEND / REJECT, findings tagged **P4-F#** with severity. You report to **Lucas** (who signs the
freeze after your review), not to the Supervisor.

**Evidence base you should read first:** `docs/s0_3/substrate_recon.md` (R§n citations) ·
`docs/s0_3/pr4_input_sheet.md` (the menus the block chose from) ·
`results/s0_3/s0_3_0_recon_arithmetic.json` + `analysis/s0_3_0_recon_arithmetic.py` (the
kernel) · the **E-2026-06-11-2 ruling** in `shared/escalate_to_human.md` (M1 + M3 trigger +
riders R1/R2/R3 — recorded verbatim) · frozen PR-2 v2 / PR-13 / PR-10 / PR-1.1 in the ledger.

**Stance:** adversarial. The two hostile readings to try to make stick:
1. *"The substrate cell was chosen to flatter the photonic side"* — e.g. the headline moved
   from the foundry floor (C-1) to the better platform (C-2) exactly where the frozen task
   becomes feasible; θ₀ = 0.3 was picked so the frozen N = 32 packs and the 7-tap span is
   covered.
2. *"The freeze leaves tunable holes"* — anything decided in Executor code at implementation
   time instead of in this block is a pre-registration failure (F12 discipline).

## Checklist (work every item; say CONFIRMED / REFUTED / EDIT per item)

1. **Fork-application fidelity.** Compare the G-section against the E-2026-06-11-2 ruling
   text ¶1–3 and riders R1/R2/R3 — verbatim-faithful? Anything added, dropped, or weakened?
   Specifically: is the **M3 trigger** as registered actually *pre-committable* (its
   quantitative margin form is deferred to the PR-5–9/PR-11 freeze — is that deferral a hole,
   or correctly "frozen before any bake-off results exist")?
2. **M1 validity conditions vs the recon physics** (R§4b–e). Are conditions (i)–(iii)
   complete? Is there any registered task/protocol element that already violates them
   (e.g. SPSA's two perturbed forward passes — do the ± perturbations change average drive
   power episode-to-episode, and does the drift-knob handling cover that)? Check the
   Bononi–Rusch caveat is correctly scoped.
3. **Arithmetic re-derivation** (use the kernel / your own): packing at θ₀ (C-1 ≈ 12.9
   intrinsic-class poles in 2 GHz → N=8 ✓?; C-2 ≈ 44 → N=32 ✓?); memory at θ₀ (4.1 / 14.0
   samples @ 2 GS/s); splitting ratios at θ₀ (C-1 ≈ 1.9, C-2 ≈ 1.0); gain headroom (×6.5–12
   C-1, ×22–41 C-2 vs the 0.9×intrinsic target); n_ss ≈ 23 ASE photons corner-independent;
   P_pk = 2·P̄₀ for equiprobable 4-PAM; E_sym/E_sat at P̄₀ = 1 mW. Flag any number that
   doesn't reproduce.
4. **The two-cell role split** (C-1 Gate ii @ N=8 · C-2 bake-off headline @ N=32). Does it
   violate the "four estimators share ONE substrate" quality standard, or is "one model, two
   registered parameter points" sound? Does moving the bake-off headline to C-2 dodge the
   ledger rule "foundry-grade gates Gate ii"? Verify C-2's foundry-class standing: the block
   cites Cui 2023 as standard-MPW-process — **verify that phrase against the abstract via
   the Semantic Scholar API route that worked at S0.3-0** (SPIE/ADS/researching.cn are
   walled; four routes failed at the freeze date).
5. **K4 necessity + parameters.** Verify the claim "K4 is forced by the frozen PR-2 P2
   partition" against the frozen PR-2 v2 text. Attack the bounds [0.1, 3] (why not 10 — is
   the exclusion rationale sound?) and **θ₀ = 0.3**: it is chosen jointly so the frozen
   constraints co-satisfy — legitimate design-from-frozen-constraints (no results exist yet)
   or constraint-shopping? Check the F6 "one value" requirement (PR-2 v2: baseline holds
   κ_ext at θ₀ ≡ the PR-4 policy value) is satisfied with exactly one registered value.
6. **The O2 two-step** (formula frozen now; numeric E₀ evaluated at S0.3-1 calibration and
   ledger-addended before any gated/bake-off-consumed run). Is the formula actually
   **parameter-free** as claimed (closed-form for stationary inputs at C-2/θ₀/δ=0)? Is the
   two-step a pre-registration hole or a mechanical evaluation? Also: is P_sat's "scaled to
   the ring per the registered geometry" pinned tightly enough, or is that a hidden knob?
7. **K-pol-3 always-ON.** Is the incoherence argument against K-pol-1/2 under K4 valid? Are
   the per-cell γ assignments honest (90 MHz subtractive-low at C-1 [EV]; 11.8 MHz
   damascene-clean at C-2 [AV] — process-class assumptions, no AN800-specific γ exists)?
   Check the registered claim condition ("no registered cell supports a knob-OFF single-pole
   claim at θ₀") against the arithmetic.
8. **Rider compliance audit.** R1: NF-A 7.0 headline everywhere, NF-C never headline —
   any leak? R2: is the N-grid consequence stated **in the splitting block** and is the
   {8 @ C-1, 32 @ C-2, 128 @ C-3-labelled} pinning consistent with frozen PR-2's
   {8, 32, 128}-headline-32? R3: is ensemble-power stationarity registered as an **M1
   validity assumption** (G(ii)) and cross-referenced from N, not buried as a line item?
9. **H1 choice.** EV-F1 showed the convention flips an envelope verdict — is registering the
   conservative corner (H1) for the substrate's standalone numbers right, with H2 as
   sensitivity? Any place a downstream claim would quietly inherit H2?
10. **Anchor-risk register** (the PR-1.1 transfer-check rule's first post-signature
    application, GA-F6 physics scope). Is the conservative-bound construction for C-2 sound
    (registered values strictly worse than the abstract-verified demonstration)? Is the
    **geometry-transfer risk** (Cui = 19.8-GHz-FSR racetrack vs our 100-GHz registry ring;
    bend-loss-neutral assumption) correctly named — and is it *enough* to name it, or should
    C-2 carry a quantitative derate? Is anything else un-named (e.g. the Er-gain coefficient
    applied to a different process — R§4f's Stage-1 integration flag)?
11. **Cross-consistency sweep vs every frozen entry:** PR-2 v2 (partition, N-grid, F6, F12
    same-SNR ↔ R3), PR-13 (does the k-grid fit C-1/C-2 memory at θ₀ — which k's are
    in-memory at 1 GS/s?), PR-10 (clocks {0.1, 1, 2} GS/s — the block quotes 2 GS/s
    arithmetic; spot-check 0.1/1), PR-11 carry-in (independent ASE streams), PR-1.1 (rule
    application), S0.1 conventions (κ definitions, pole region, ZOH/van-Loan), the
    ledger-row demands (α↔Q self-consistency check registered?).
12. **Completeness vs the F12 discipline.** List anything the S0.3-1 Executor would still
    have to *decide* (not merely evaluate) at implementation time. Each such item is a
    finding.

**Format:** lead with the verdict + a findings table (P4-F#, severity, one-line). Then the
per-item dispositions. The Supervisor responds with a revised block (supersession
discipline), not by editing your review.
