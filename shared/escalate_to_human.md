# Escalate to Human (Lucas)

Either agent posts here when a decision is **above the pipeline's pay grade** — anything that changes
what the paper will claim, commits money/compute, or where Supervisor and Critic disagree and can't
resolve it. Lucas is the human PI and final authority. Newest at top.

Escalate (don't decide autonomously):
- Scope changes beyond the approved proposal / roadmap
- Methodology changes (metrics, training setup, evaluation) that affect conclusions
- Any cloud-compute spend
- Supervisor ↔ Critic deadlock
- Pre-registered margins/gates, before the run that tests them
- Invoking a baseline/fallback (proposal §5.3: offline-train-deploy; reservoir-readout)
- Promoting an exact method (recurrent adjoint or RHEL) toward a hardware slot (§5.2 guardrail)
- The S0.7 systems-advantage-envelope verdict, if even the optimistic envelope fails to clear digital (§10)

---

## OPEN FOR LUCAS

### E-2026-06-09-1 — Steer the two S0.1 architecture decisions (low-risk; Supervisor + Critic aligned)
S0.1 done (gate passed); Critic reviewed → **APPROVE-WITH-EDITS** (`critic_review_s0-1-results.md`); S0.2
can proceed after four decision-free edits (now ACTIVE as **S0.1.1**). **Your steer is needed on the two
decisions** — both now carry *converged* Supervisor + Critic recommendations (`decisions_needed.md`):
- **D-08-2 (mapping class):** simulate the **diagonal complex-pole SSM (S4D/DSS)**, with LinOSS as its
  conjugate-pair special case; soften the "oscillatory LinOSS" branding; benchmark-transfer becomes
  **debt #2**; pin the readout (coherent-quadrature vs intensity) at PR-2. *(The Critic corrected the
  Supervisor's "it is LinOSS" framing — adopted in full.)*
- **D-08-3 (backscatter):** optional roughness-gated splitting knob + PR-4 sub-parameter; evaluate at the
  operating κ_ext; default-ON off the clean-damascene corner; verify B2 numbers before the paper.
Bless these (or redirect) → I write the mapping result + spec S0.2 (freezing PR-1 / PR-2 / PR-10).

**Standing per-phase touchpoints** — pre-registered values come to Lucas before
the run that tests them (`preregistration.md`):
- **S0.2:** PR-1 (Gate-i margin) · PR-2 (bake-off task + architecture + parameter partition) · PR-10
  (S0.7-lite assumptions, *before* the task choice).
- **S0.3:** PR-4 (the $(\alpha,Q_i)$ pair + $\kappa_\text{ext}$ policy + noise cell — resolves
  **D-2026-06-08-1**) · compute sizing (escalate if it implies cluster spend).
- **S0.4:** PR-6 (fairness contract, **CRITICAL**) · PR-5 (PAT twin-mismatch) · PR-3 (BPTT-ceiling rule).
- **S0.5:** PR-8 / PR-9 (statistics + Gate-ii semantics + promotion criteria).
- Plus the **Critic reviews S0.1 results** before S0.2 starts (gate model).

---

## RESOLVED

### ✅ E-2026-06-05-1 — Stage-0 setup + roadmap — **RESOLVED 2026-06-08**
**Lucas: "accept all, scope (B) blessed."** Critic review (APPROVE-WITH-EDITS) adopted in full and folded
into `stage0_roadmap.md` **v3**; CLAUDE.md "Codebase plan" F17-fixed; `preregistration.md` adopted (14
entries, UNSET, freeze per-phase); **S0.1 ACTIVE** with the scope-(B) deliverables. Prior progress: D-1
(salvage) + D-2 (`git init`) resolved 2026-06-08; S0.0 DONE (all gates green, 60/60 tests, SPSA anchor RMS
1.1e-7); Critic verdict 1 CRITICAL · 9 HIGH · 11 MEDIUM · 1 LOW, Supervisor concurred in full. Load-bearing
adopted edits: F7 (fairness contract), F10 (Gate-ii decomposition + escalate corner + "exactness" struck),
F2 (score vs BPTT ceiling), F1 (early S0.7-lite), F11 (≥8 seeds + censoring), F13 (foundry-$Q$ gates).
