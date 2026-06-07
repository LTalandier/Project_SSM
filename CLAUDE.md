# Photonic State-Space Model on Silicon Nitride

## What this is

A research program to build a **trained, structured photonic state-space model (SSM)** — an
**oscillatory (LinOSS-style) coupled-microring recurrence on silicon nitride (SiN)** — and to **train
its physical recurrence in situ**, which no recurrent photonic system has yet had done by any method.
The authoritative spec is the proposal:

- `photonic-ssm-proposal-v0_5.md` — **the authoritative project document.** Read it first.
  *(`photonic-ssm-tfln-proposal-v0.2.md` is the superseded TFLN-era draft — historical only.)*

**Central target (the headline contribution):** the *first in-situ-trained recurrent photonic
system* — i.e. the recurrent parameters themselves (pole positions + inter-ring couplings that *define*
the recurrence) updated **on the physical device** by gradient-based/-estimating training. This is
platform- and method-independent (proposal §2, §10).

## Key choices (proposal v0.5)

- **Platform: ultra-low-loss silicon nitride.** The dominant figure of merit for a dissipative ring
  recurrence is round-trip loss / intrinsic $Q$ (it bounds memory length); SiN is class-leading
  ($Q>10^7$, single-digit dB/m) and drift-stable (low d$n$/d$T$, good for gradient-free tuning). TFLN
  is now a **fallback only** (§8). Foundries: **CORNERSTONE / LIGENTEC** (gdsfactory-native, open MPW).
- **Architecture: oscillatory LinOSS unit**, valid for any nonnegative-diagonal (dissipative) $A$ — so a
  lossy-but-high-$Q$ ring lattice is in-regime. **Damping is a free design knob** (D-LinOSS for
  performance); the v0.2 conservatism–damping tension is gone.
- **Training: PAT + SPSA primary and hardware-committed.** Physics-Aware Training (digital-twin
  backward) and SPSA (model-free, two physical forward passes) are dissipative-agnostic, absorb
  hardware non-idealities, and are chip-demonstrated. Two exact/physics-native methods — **recurrent
  in-situ adjoint** and **RHEL/Hamiltonian-echo** — are evaluated **in parallel, in simulation only**.
  **Guardrail: parallel in simulation, singular in hardware** — the chip stays on PAT/SPSA; the bake-off
  decides whether adjoint or RHEL earns a *later* hardware slot.

## Current status — Stage 0 (theory + simulation; no fab; publishable)

We are at **Stage 0** (proposal §6): no chip, no compute-cluster commitment yet. Stage 0 is
fabrication-independent, **reuses existing tooling** (`pnn-multilayer`), and gates everything downstream.

Stage 0 objectives (proposal §6):
- **(a)** Formalize the oscillator↔SiN-ring mapping; bound the realizable pole region.
- **(b)** Run the **four-method in-situ-training bake-off** — SPSA, PAT, recurrent in-situ adjoint,
  RHEL — on **one shared realistic dissipative ring model** (finite $Q$, gain saturation, injected ASE).
  **Primary score: sample-efficiency-to-target-accuracy under realistic noise.** Gradient-cosine-error
  vs BPTT is a **secondary diagnostic only** (alone it flatters the exact methods, penalizes SPSA).
- **(c)** Build the **optical-echo sub-model on a concrete phase-conjugation mechanism** (χ³ FWM with
  real pump/bandwidth/efficiency/noise penalties, or an explicit off-chip admission) — not an abstract
  error term. This is RHEL's extra modelling cost and the honest test of its on-SiN feasibility.
- **(d)** Choose the damping operating point for accuracy (D-LinOSS sweep).
- **(e)** Sketch the **systems-advantage envelope**: end-to-end latency/energy for the target
  low-latency niche, *including* E/O–O/E + DAC/ADC overhead, vs a digital baseline.

Stage 0 gates:
- **(i)** Idealized model reproduces oscillatory-SSM task accuracy within a **pre-registered margin**.
- **(ii)** At realistic SiN noise, **≥1 method trains to the pre-registered accuracy** — **PAT/SPSA the
  default hardware route regardless**; promote adjoint/RHEL to hardware only if the bake-off shows it
  *clearly* beats PAT/SPSA on a metric that matters.

Stage 0 decomposition + live state: `shared/stage0_roadmap.md` + `shared/task_queue.md`.

## Four verification debts (proposal v0.5 closing note) — track these

1. **White-space claim**, sharpened form: *recurrent parameters updated on the physical device by
   gradient-based/-estimating training* — never done (pre-empt reservoir computing, the Bueno/Brunner
   photonic-RNN RL line, internal-param reservoir variants). The single load-bearing sentence.
2. **LinOSS / D-LinOSS / Mamba-3** benchmark specifics.
3. **Er:Si₃N₄ noise figure** — flagship gain device published gain but **no measured NF**.
4. **Recurrent-adjoint gap** — inferred from absence of demonstrations (mid-2026).

Plus the **§10 advantage question** (does a photonic SSM beat digital once conversion overhead is paid?)
is the largest conceptual risk — now a Stage-0 deliverable (the S0.7 envelope), tested against the
offline-deploy and reservoir baselines.

## Codebase plan (Stage 0)

**New project = new repository** (do not modify previous projects). The Executor forks the relevant
pieces from `pnn-multilayer` — now *more* on-point under v0.5, since SiN relies on trench-isolated
thermo-optic tuning and SPSA's crosstalk-robustness, matching that project's thermal-crosstalk and
perturbation-tolerance findings:
- ring / MRR forward models; differentiable + batched training engine; gain/SOA + crosstalk tooling.

New Stage-0 code (Executor builds, per roadmap): the LinOSS/D-LinOSS oscillator + coupled-ring
realization; the **shared dissipative ring substrate** (finite $Q$, gain saturation, ASE); the **four
estimators** (PAT, SPSA, recurrent adjoint, RHEL + the concrete echo/phase-conjugation sub-model); the
systems-advantage budget.

## Multi-agent coordination

Three local Claude Code sessions coordinate through `shared/`:

| Role | Session | Responsibility |
|------|---------|----------------|
| **Supervisor** | Claude Code session 1 (Opus 4.8) | Methodology design, result analysis, paper writing, task assignment |
| **Executor** | Claude Code session 2 | Code implementation, simulation execution, result reporting |
| **Critic** | Claude Code session 3 | Adversarial methodology/result review (independent; reports to Lucas, **not** the Supervisor) |

**Role boundaries:**
- The Supervisor does **not** write or run simulation code; the Executor does.
- The Executor does **not** design methodology or write the paper; the Supervisor does.
- The Critic only reviews — and reports to **Lucas**, so the Supervisor cannot dismiss its concerns
  without escalation.
- **Always ask before significant decisions** (scope/methodology/architecture, compute spend,
  pre-registered margins). Log to `shared/decisions_needed.md` or `shared/escalate_to_human.md`.

### Coordination files (`shared/`)
- `stage0_roadmap.md` — master Stage-0 plan (S0.0–S0.8 + S0.L; the bake-off; gates)
- `task_queue.md` — Supervisor assigns; Executor executes the **ACTIVE** task
- `results_log.md` — Executor writes results; Supervisor evaluates
- `decisions_needed.md` — Executor escalates design questions to the Supervisor
- `escalate_to_human.md` — either agent escalates to Lucas (human PI)
- `supervisor_feedback.md` — Supervisor progress notes / direction
- `launch_executor.md` — Executor onboarding prompt
- `executor_instructions.md` — Executor full role definition
- `critic_instructions.md` — Critic onboarding + how review specs are filed

### Supervisor helper skills (`.claude/skills/`)
- `/executor <phase>` — write an Executor task spec into `task_queue.md` + give the launch command
- `/critic <topic>` — write Critic review instructions into `shared/critic_instructions_<topic>.md`
- `/phase-status` — dashboard from roadmap + task_queue + results_log
- `/results [phase]` — summarize `results_log.md`

### Launch commands
```bash
# Supervisor session (this one):
cd ~/Documents/Project_SSM
claude

# Executor session (separate terminal):
cd ~/Documents/Project_SSM
claude "Read shared/launch_executor.md and follow it."

# Critic session (separate terminal):
cd ~/Documents/Project_SSM
claude "Read shared/critic_instructions.md, then review the target it names."
```

## Quality standards
- Every experiment specifies: parameter ranges, seed count, success metric, expected runtime.
- Results report: raw-data path, summary stats, variance, anomaly flags.
- 4 seeds minimum per configuration; 8+ for high-variance configurations (esp. SPSA).
- The four estimators share **one** substrate model so the bake-off is apples-to-apples.
- Pre-register margins/gates *before* the run that tests them.

## Related repositories (the research ecosystem)
- `Project_AR_ParetoPNN` — Paper 1: Pareto MZI-topology benchmark (handoff complete).
- `pnn-multilayer` — Paper 2: multi-layer photonic equalization (135 pp draft) + chip β-track
  (ring-bank, SOA/gain, thermal-crosstalk). **Primary Stage-0 tooling source.**
- `PNN_topology_search` — Paper 3: photonic-mesh topology search.
- `Project_research_orchestr` — the Paperclip cloud orchestration framework (agent role defs).

## Owner
Lucas Talandier — independent photonics researcher, Paris. GitHub: LTalandier.
