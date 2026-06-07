---
name: executor
description: Write an Executor task specification to shared/task_queue.md and provide the launch command. Use when a Stage-0 phase is ready to be implemented.
disable-model-invocation: true
argument-hint: [phase id and brief description, e.g. "S0.3 RHEL trainer + BPTT equivalence"]
---

Write an Executor task for: $ARGUMENTS

## What to do
1. Read `shared/stage0_roadmap.md` to get the phase's objective, deliverables, and gate.
2. Read `shared/task_queue.md` to see what's COMPLETED and what's ACTIVE/PROPOSED.
3. Mark any previous ACTIVE task as **COMPLETED** (date + one-line summary).
4. Write the new task at the top of the queue (below the header).
5. Provide the Executor launch command at the end.

## Task specification format
```markdown
## <ACTIVE> S0.x: Title

**Assigned:** YYYY-MM-DD
**Supervisor:** Claude Opus 4.8
**Status:** ACTIVE
**Prereqs:** roadmap phase + proposal sections + files to read

### Goal
One paragraph: what this accomplishes and why it matters for Stage 0.

### Deliverables
Numbered, concrete: new files (with class/function signatures), files to modify,
sweep grids (with job count), output format (JSON/JSONL fields), figures.

### Key gates and questions
The pre-registered success criterion. What to report honestly if it fails.

### Deployment
Local vs cloud, estimated runtime, seed count.
```

## Key principles
- The Executor implements code and runs experiments. It does **NOT** write the paper or design methodology.
- Be specific: function signatures, class names, parameter grids, output schema.
- Include a smoke-test instruction and a job-count estimate.
- Pre-register the gate's margin in the task *before* the run.

## Executor launch command
Always end with:
```
Launch the Executor (separate terminal):
cd ~/Documents/Project_SSM
claude "Read shared/launch_executor.md and follow it."
```
