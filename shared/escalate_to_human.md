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

### E-2026-06-05-1 — Stage-0 setup + roadmap *(status 2026-06-08)*
Scaffold realigned to v0.5; running. Progress:
1. ✅ D-1 (salvage) + D-2 (`git init`) **resolved** by Lucas 2026-06-08.
2. ✅ **S0.0 is ACTIVE** (repo init + selective salvage + smoke test) — Executor can start.
3. 🔄 **Roadmap approval pending the Critic's independent review** (in flight,
   `shared/critic_instructions_stage0-roadmap.md` → `critic_review_stage0-roadmap.md`). Final Lucas
   sign-off of `shared/stage0_roadmap.md` after the Critic reports.
**Open for Lucas next:** read the Critic's roadmap verdict when it lands; rule on any AMEND findings;
the parked SiN-$Q$ pre-registration choice (`decisions_needed.md` D-2026-06-08-1) comes due at S0.2/S0.3.

---

## RESOLVED

_(none yet)_
