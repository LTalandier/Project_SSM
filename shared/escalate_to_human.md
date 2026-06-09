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

*(Nothing open — 2026-06-09 "ok go" resolved E-09-1 + E-09-2; both below. Next asks coming to you:
**PR-10** (S0.7-lite assumptions — Supervisor drafting now) and then the **pre-S0.2 continuation gate**
itself, once the PR-15 search verdict + the lite envelope are both in hand.)*

**Standing per-phase touchpoints** — pre-registered values come to Lucas before
the run that tests them (`preregistration.md`):
- **pre-S0.2:** PR-10 (S0.7-lite assumptions, *before* the lite run) · the **continuation gate**
  (PR-15 verdict + lite envelope + your program-level call — D-09-1) · any FATAL/AMBIGUOUS PR-15 finding
  comes to you immediately with primaries.
- **S0.2:** PR-1 (Gate-i margin) · PR-2 (bake-off task + architecture + parameter partition + readout —
  carries the blessed D-08-2/D-08-3 constraints).
- **S0.3:** PR-4 (the $(\alpha,Q_i)$ pair + $\kappa_\text{ext}$ policy + noise cell incl.
  roughness/splitting — resolves **D-2026-06-08-1**) · compute sizing (escalate if it implies cluster
  spend).
- **S0.4:** PR-6 (fairness contract, **CRITICAL**) · PR-5 (PAT twin-mismatch) · PR-3 (BPTT-ceiling rule).
- **S0.5:** PR-8 / PR-9 (statistics + Gate-ii semantics + promotion criteria).
- Plus the **Critic gates each phase's results** before dependents start (gate model).

---

## RESOLVED

### ✅ E-2026-06-09-2 — D-2026-06-09-1 (front-load white-space kill-search) + strategic flag — **RESOLVED 2026-06-09**
**Lucas: "ok go."** Debt #1 front-loaded pre-S0.2 under **PR-15 (🔒 FROZEN** — rule-form kill-criterion
q1∧q2∧q3, two-modality protocol, one-sided PASS; full detail in `preregistration.md`). Roadmap → v3.1:
S0.2–S0.5 authorization now sits behind the **pre-S0.2 continuation gate** = PR-15 verdict + S0.7-lite
envelope + Lucas's program-level call (the "first" is collectible only at Stage 1+; Stage 0 alone =
methods paper). Executor search task **S0.L-1 ACTIVE**; Critic adversarial spec filed
(`critic_instructions_whitespace-pr15.md`). F14 reconciliation routed to the Critic.

### ✅ E-2026-06-09-1 — Steer the two S0.1 architecture decisions — **RESOLVED 2026-06-09**
**Lucas: "ok go."** **D-08-2** → complex-diagonal **S4D/DSS** layer, LinOSS as conjugate-pair special
case (Critic's corrected framing); readout + F6 pinned at PR-2; benchmark transfer = debt #2. **D-08-3**
→ roughness-gated CW/CCW knob (default ON off the clean-damascene corner) + PR-4 roughness/splitting
sub-parameter at the operating κ_ext, jointly with D-08-1; B2 numbers provisional until F5. Constraints
logged in `preregistration.md` Notes; mapping write-up at `docs/s0_1/mapping_result.md`. Prior progress:
S0.1 gate PASSED (Critic APPROVE-WITH-EDITS); **S0.1.1 closeout DONE** (107/107; F1 transient validation
positive — S0.1 fully closed).

### ✅ E-2026-06-05-1 — Stage-0 setup + roadmap — **RESOLVED 2026-06-08**
**Lucas: "accept all, scope (B) blessed."** Critic review (APPROVE-WITH-EDITS) adopted in full and folded
into `stage0_roadmap.md` **v3**; CLAUDE.md "Codebase plan" F17-fixed; `preregistration.md` adopted (14
entries, UNSET, freeze per-phase); **S0.1 ACTIVE** with the scope-(B) deliverables. Prior progress: D-1
(salvage) + D-2 (`git init`) resolved 2026-06-08; S0.0 DONE (all gates green, 60/60 tests, SPSA anchor RMS
1.1e-7); Critic verdict 1 CRITICAL · 9 HIGH · 11 MEDIUM · 1 LOW, Supervisor concurred in full. Load-bearing
adopted edits: F7 (fairness contract), F10 (Gate-ii decomposition + escalate corner + "exactness" struck),
F2 (score vs BPTT ceiling), F1 (early S0.7-lite), F11 (≥8 seeds + censoring), F13 (foundry-$Q$ gates).
