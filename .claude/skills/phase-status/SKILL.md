---
name: phase-status
description: Show where we are in the Stage-0 roadmap — completed phases, active phase, next phases, and blocking gates.
---

Report the current Stage-0 status.

## What to do
1. Read `shared/stage0_roadmap.md` — the master plan (S0.0–S0.7 + S0.L).
2. Read `shared/task_queue.md` — scan COMPLETED / ACTIVE / PROPOSED markers.
3. Read `shared/results_log.md` — which phases have results.
4. Read `shared/decisions_needed.md` and `shared/escalate_to_human.md` — open blockers.
5. Build a dashboard:

```
STAGE 0 STATUS

Completed:
  [x] S0.x — one-line outcome

Active:
  [ ] S0.x — title (status: running / awaiting Critic / blocked)

Next (in order):
  [ ] S0.x — title

Blocked / awaiting decision:
  - ...

Gates:
  [PASS/PENDING] Gate (i)  — idealized model reproduces oscillatory-SSM accuracy within margin
  [PASS/PENDING] Gate (ii) — at realistic SiN noise, ≥1 method (of SPSA/PAT/adjoint/RHEL) trains to
                             the pre-registered accuracy; PAT/SPSA = default hardware route regardless

Verification debts:
  [ ] white-space (sharpened)   [ ] LinOSS/D-LinOSS/Mamba-3   [ ] Er:SiN noise figure   [ ] recurrent-adjoint gap

Advantage envelope (S0.7):
  [ ] systems advantage vs digital incl. E/O–O/E + DAC/ADC overhead sketched (the §10 premise)
```

## Output format
Concise dashboard. Checkboxes, not prose. Include dates and job counts where available.
