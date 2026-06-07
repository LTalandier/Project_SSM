# Supervisor Feedback / Direction Log

Supervisor's running notes: direction, progress assessments, and responses to Executor results and
Critic reviews. Newest at top. This is the Supervisor's voice — the Executor and Critic can read it
for context, but task assignments live in `task_queue.md` and review specs in `critic_instructions*.md`.

---

## 2026-06-08 — Rulings in; S0.0 ACTIVE; Critic dispatched on the roadmap (parallel)

Evaluated the S0.0a recon (`tooling_recon.md`) — high quality; its central correction stands: the
`pnn-multilayer` ring code is static/CW, so the SSM core is new under either ruling and the salvage value
is the estimator/infra layer. Lucas ruled **D-1 → (a) selective salvage**, **D-2 → git init**.
- **S0.0 rewritten and flipped ACTIVE:** repo init + git + the 7-asset salvage manifest (provenance
  headers, contact-point decoupling, re-run tests) + two architecture constraints baked in from line one
  — **(3a)** gradients must flow through the optical state (no `no_grad`/`detach`; checkpointed unroll),
  **(3b)** expose full state trajectories (adjoint/RHEL need them) — + a salvage-validation smoke test.
  The dynamical ring→pole core is deferred to S0.1 (kept S0.0 to infra/salvage only).
- **Critic dispatched on the Stage-0 roadmap, in parallel** (`critic_instructions_stage0-roadmap.md`):
  9-item checklist incl. the advantage-envelope-pull-earlier question, metric integrity, shared-substrate
  fairness, RHEL echo honesty, Gate-(ii) guardrail, the parked SiN-$Q$ pre-registration, the four debts,
  and recon integration. Verdict → `critic_review_stage0-roadmap.md`. Safe to run alongside S0.0 (S0.0 is
  upstream infra; Critic findings hit S0.1+).
- **Parked decision logged:** D-2026-06-08-1 — SiN operating $Q$ (`2×10⁶` foundry vs `>10⁷` class-leading),
  due at S0.2/S0.3 pre-registration.
- **Next Supervisor action:** ingest the Critic's roadmap verdict, fold AMEND findings into the roadmap,
  bring it to Lucas for sign-off; then `/executor S0.1` once S0.0 reports DONE.

## 2026-06-07 — First task = read-only tooling reconnaissance (S0.0a)

Rather than guess on D-1 (salvage `pnn-multilayer` vs. clean start), the first Executor task is a
**read-only reconnaissance** (S0.0a, now ACTIVE): assess per-module liftability — especially whether
`equalization_ringbank.py` is a usable head start for the S0.1 oscillator↔ring mapping — and recommend
(a) salvage / (b) clean start with evidence, written to `shared/tooling_recon.md`. Writes no code,
modifies nothing, commits to no decision. Lucas rules on D-1 after reading the report; then S0.0 (repo
build + smoke test) goes ACTIVE. "Fork" was sloppy terminology on my part — corrected to "salvage"
(copy + adapt into a new repo; `pnn-multilayer` stays untouched) throughout.

## 2026-06-06 — Realigned scaffold to proposal v0.5

Lucas replaced the proposal with `photonic-ssm-proposal-v0_5.md` (supersedes the TFLN-era v0.2). Major
shifts absorbed into the whole scaffold (CLAUDE.md, roadmap, task_queue, executor/critic instructions,
skills, memory):
- **Platform TFLN → silicon nitride** (round-trip loss / intrinsic $Q$ is the binding FOM; SiN class-leading).
  TFLN is now fallback-only. Foundries: CORNERSTONE / LIGENTEC.
- **Training: RHEL demoted; PAT + SPSA now primary + hardware-committed.** Stage 0 is a **four-method
  bake-off** (SPSA, PAT, recurrent adjoint, RHEL) on **one shared dissipative ring model**. Guardrail:
  parallel in simulation, singular in hardware.
- **Primary metric flipped** to sample-efficiency-to-target-accuracy under realistic noise;
  gradient-cosine-error demoted to a secondary diagnostic (old Gate (ii) retired).
- **Conservatism–damping tension dissolved** → damping is a free knob (D-LinOSS for accuracy).
- **Systems-advantage envelope** (latency/energy incl. conversion overhead) is now an explicit Stage-0
  deliverable (S0.7); the §10 advantage premise is the largest conceptual risk.
- Verification debts now **four**: sharpened white-space; LinOSS/D-LinOSS/Mamba-3; **Er:SiN NF**;
  **recurrent-adjoint gap**.
- RHEL must commit to a **concrete phase-conjugation echo sub-model** (no idealized operator).

Roadmap rewritten to v2: S0.0 fork → S0.1 mapping → S0.2 LinOSS baseline (Gate i) → S0.3 shared substrate
→ S0.4{a PAT/SPSA, b adjoint, c RHEL+echo} → S0.5 bake-off (Gate ii, headline) → S0.6 damping → S0.7
advantage envelope → S0.8 write-up; S0.L literature in parallel. **Next Supervisor actions once approved:**
`/critic stage0-roadmap`; then flip S0.0 → ACTIVE and `/executor S0.0`.

## 2026-06-05 — Project bootstrapped

- Read the proposal (`photonic-ssm-tfln-proposal-v0.2.md`) and replicated the `pnn-multilayer`
  3-session setup (Supervisor / Executor / Critic) into this repo.
- Drafted `stage0_roadmap.md` (S0.0–S0.7 + S0.L literature track) from proposal §6.
- Queued S0.0 (repo + tooling fork + smoke test) as **PROPOSED**, pending Lucas's go and Critic review
  of the plan. Two open decisions logged (`decisions_needed.md`): fork vs. fresh; `git init` now.
- **Next Supervisor actions once approved:** (1) `/critic stage0-roadmap` to get an independent read on
  the plan and the pre-registered margins; (2) flip S0.0 → ACTIVE and `/executor S0.0`.
