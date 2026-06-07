# Critic Review Spec — Stage-0 Roadmap

**Filed by:** Supervisor (Claude Opus 4.8) · **Date:** 2026-06-08 · **For:** the independent Critic session.

You are the **Critic** of the Photonic-SSM-on-SiN pipeline (read `shared/critic_instructions.md` for your
standing role). You report to **Lucas**, not the Supervisor. You have **no context** from the Supervisor's
conversation — this spec is standalone. Review the **Stage-0 plan itself** (not results — none exist yet).

## Scope
Adversarially review whether the Stage-0 roadmap is the right plan to commit fabrication-gating effort to.
This is a *plan review*, before code. The headline question: **if this plan runs to completion, does it
produce a defensible answer to "can a photonic recurrence be trained in situ, and is it worth building?"**

## Files to read (in this order)
1. `shared/stage0_roadmap.md` — the plan under review (phases S0.0–S0.8 + S0.L, the two gates).
2. `photonic-ssm-proposal-v0_5.md` — the authoritative spec; esp. §4 (pole region), §5 (training:
   PAT/SPSA primary + the four-method bake-off), §6 (Stage 0), §10 (advantage). **Ignore**
   `photonic-ssm-tfln-proposal-v0.2.md` (superseded TFLN-era draft).
3. `shared/tooling_recon.md` — the S0.0a reconnaissance that re-scoped the codebase: `pnn-multilayer`
   ring code is static/CW, so the SSM core (dynamical temporal-CMT ring, LinOSS, substrate, estimators)
   is new code regardless; salvage is confined to the estimator/infra layer.
4. `shared/task_queue.md` (S0.0 as now specced) and `shared/decisions_needed.md` (D-1 salvage / D-2 git-init
   rulings) — context for how the plan starts.

## Review checklist — answer each specifically
1. **Decomposition & dependency order.** Is `S0.0 → S0.1 → S0.2(Gate i) → S0.3 → S0.4{a PAT/SPSA, b
   adjoint, c RHEL+echo} → S0.5(Gate ii) → S0.6 → S0.7 → S0.8` the right order? Any phase misplaced,
   missing, or that should be parallel? **Specifically adjudicate the Supervisor's proposal to pull a
   cheap version of the S0.7 systems-advantage envelope *earlier*** (as a low-cost kill-test of the §10
   premise before the full bake-off) — agree or not, with reasoning.
2. **Primary-metric integrity.** Is **sample-efficiency-to-target-accuracy under realistic noise** correctly
   the *primary* score for the S0.5 bake-off, with **gradient-cosine-error a secondary diagnostic only**?
   Is the stated rationale (cosine-error flatters the exact methods adjoint/RHEL, penalizes SPSA whose
   poor per-step alignment still converges) sound? Does any part of the plan let the diagnostic creep into
   the headline?
3. **Shared-substrate fairness.** Does the plan genuinely train all four estimators through **one** S0.3
   substrate? Identify any hidden asymmetry (e.g. a method given an information advantage, mismatched
   noise realizations, or unequal compute budgets) that would make the bake-off unfair in either direction.
4. **RHEL echo honesty.** Does S0.4c correctly **forbid an idealized conjugation operator** and require a
   *concrete* phase-conjugation mechanism (χ³ FWM with real pump/bandwidth/efficiency/added-noise penalties,
   or an explicit off-chip admission)? Is the **irreducible-ASE-irreversibility floor** represented? Is
   RHEL-on-SiN framed as "odds-improved, not feasibility-reopened" (§5.2) rather than over-claimed?
5. **Gate (ii) + the hardware guardrail.** Is "**≥1 method trains to the pre-registered accuracy at
   realistic SiN noise, PAT/SPSA the default hardware route regardless**" the right gate? Is the guardrail
   ("promote adjoint/RHEL to a hardware slot *only if* it clearly beats PAT/SPSA on a metric that matters")
   strong enough, or could a marginal result smuggle a speculative method onto the chip?
6. **Pre-registration discipline.** Are margins/gates (esp. the S0.2 Gate-i accuracy margin and the S0.5
   target accuracy) set to be fixed **before** the runs that test them? Adjudicate the **parked
   $Q$ decision**: the salvaged SiN registry ships `Qi=2×10⁶` (foundry-grade) but the proposal cites
   `Q>10⁷` (class-leading). Is treating this as an S0.2/S0.3 pre-registration choice correct, and does
   either choice bias the gradient-survival / memory-length story? Recommend how to pre-register it.
7. **Verification debts.** Are the four (sharpened white-space; LinOSS/D-LinOSS/Mamba-3; Er:SiN noise
   figure; recurrent-adjoint gap) tracked (S0.L) and correctly framed? Is the **white-space claim** stated
   in its precise, defensible form (recurrent parameters — pole positions + inter-ring couplings — updated
   *on the physical device* by gradient-based/-estimating training), with reservoir computing / the
   Bueno-Brunner RL line / internal-param reservoir variants pre-empted?
8. **The §10 advantage premise.** Is the S0.7 envelope adequate, and does the plan preserve the distinction
   between the **training** advantage (vs offline-deploy / reservoir baselines) and the **systems**
   advantage (latency/energy vs digital **including** E/O–O/E + DAC/ADC overhead)? Does the plan honestly
   admit the premise could fail *before* MPW spend?
9. **Recon integration.** Given the recon's finding that the ring physics is static/CW, does anything in the
   roadmap still implicitly assume reusable ring *physics*? Are the two architecture constraints
   (gradients-through-state; expose-state-trajectories) reflected where they matter (S0.3, S0.4b/c)?

## Also free to raise
Anything a hostile reviewer of the eventual Stage-0 paper(s) would attack that this checklist misses.

## Expected output
Write `shared/critic_review_stage0-roadmap.md`:
- **Overall verdict:** APPROVE / APPROVE-WITH-EDITS / AMEND / REJECT (of the *plan*).
- **Numbered findings**, each with **severity** (CRITICAL / HIGH / MEDIUM / LOW) + a concrete, actionable
  recommendation. Re-derive/justify rather than asserting. Distinguish "must fix before S0.1 science
  starts" from "fix before the Stage-0 paper."
