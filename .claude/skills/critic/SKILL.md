---
name: critic
description: Write Critic review instructions for a specific Stage-0 phase, plan, or paper section, save to shared/critic_instructions_<topic>.md, and provide the launch command.
disable-model-invocation: true
argument-hint: [topic, e.g. "stage0-roadmap" or "S0.5 gradient-survival" or "S0.1 mapping code"]
---

Write Critic review instructions for: $ARGUMENTS

## What to do
1. Read the relevant results (`shared/results_log.md`), plan (`shared/stage0_roadmap.md`), code, and/or
   proposal sections so the spec is fully grounded.
2. Write a focused, **self-contained** instructions file to `shared/critic_instructions_<topic>.md`.
3. Provide the Critic launch command at the end.

## Instructions file must contain
- **Date and scope** — what is being reviewed and why now.
- **Files to review** — exact paths (data, code, roadmap, proposal sections).
- **Review checklist** — numbered; each item a specific question the Critic must answer.
- **Weaknesses to probe** — what a hostile reviewer attacks. Always include the relevant ones of:
  **bake-off metric integrity** (primary = sample-efficiency-to-target-accuracy; cosine-error is
  secondary-only and flatters the exact methods); **one shared substrate** across all four estimators;
  **RHEL echo honesty** (concrete phase-conjugation mechanism, no idealized operator; ASE-irreversibility
  floor); the **four verification debts** (sharpened white-space; LinOSS/D-LinOSS/Mamba-3; Er:SiN NF;
  recurrent-adjoint gap); the **§10 advantage** split (training vs systems, conversion overhead paid);
  the **PAT/SPSA-default guardrail**; pre-registration; sweep/seed artifacts.
- **Expected output** — path `shared/critic_review_<topic>.md`; format = verdict + numbered findings
  with severity (CRITICAL / HIGH / MEDIUM / LOW).

## Key principle
The Critic session is **INDEPENDENT** — it has no context from this Supervisor conversation and reports
to Lucas, not the Supervisor. The instructions must be fully self-contained: state what was done, what
is claimed, and what to check. Do not assume the Critic knows anything unless you tell it to read a file.

## Critic launch command
Always end with:
```
Launch the Critic (separate terminal):
cd ~/Documents/Project_SSM
claude "Read shared/critic_instructions_<topic>.md and follow it."
```
