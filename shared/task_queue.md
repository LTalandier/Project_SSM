# Task Queue

Supervisor assigns tasks here. The Executor reads and executes the task marked **ACTIVE**, then
**stops and waits**. The Supervisor marks a task **COMPLETED** (date + one-line summary) before
assigning the next. New tasks go at the top, below this header.

Task format: see `.claude/skills/executor/SKILL.md`.

---

## 🟢 ACTIVE — S0.0: Repo init + selective salvage + smoke test

**Assigned:** 2026-06-08
**Supervisor:** Claude Opus 4.8
**Status:** ACTIVE
**Rulings:** D-1 → **(a) selective salvage** (Lucas, 2026-06-08); D-2 → **`git init`** (Lucas, 2026-06-08).
**Prereqs:** read `shared/tooling_recon.md` (**the salvage manifest, §4** — authoritative for this task);
`shared/stage0_roadmap.md` (S0.0, S0.1, S0.3); `photonic-ssm-proposal-v0_5.md` §3. Reference repo
`~/Documents/pnn-multilayer/` @ `e2eec80` is **read-only — do not modify it.**

### Goal
Stand up the Project_SSM repo under git, **selectively salvage** the seven manifest assets (copy + adapt
into the new repo, *not* a git fork), and prove the toolchain with a salvage-validation smoke test. **The
SSM core is NOT built here** — the dynamical ring model, LinOSS layer, substrate, and estimators are
S0.1+. This task is infrastructure + salvage + toolchain proof only.

### Deliverables
1. **`git init`** the repo; `.gitignore` (Python, `__pycache__`, `.venv`, results/data); initial commit.
   `requirements.txt` (torch-only after decoupling, per recon). A `README` listing salvaged-vs-new.
2. **Salvage the 7 manifest assets** (recon §4 table). Each salvaged file carries a provenance header
   `# salvaged from pnn-multilayer @ e2eec80 : <original path>`, has its 1–2 contact points decoupled,
   and its associated test ported and **passing**:
   - `adaptation/perturbation_gradient.py` → SPSA estimator + FD/autograd diagnostic + **forward-pass
     accounting**; inject the loss-fn + forward API (decouple `compute_nmse_field` / `forward_batched`);
     re-run the FD-vs-autograd validation (<1% RMS anchor).
   - `physics.py` ~57–136 (gain / ASE / NL functions) → substrate gain + ASE knobs (lift-as-is).
   - `channels/dynamic_soa.py` (esp. `TrainingAwareDynamicSOAPerMode`) → dynamic in-loop gain +
     checkpointed-unroll pattern. **See constraint (3a).**
   - `channels/mrr_platforms.py` → SiN platform registry (lift-as-is). **Add** CORNERSTONE SiN and a
     class-leading ultra-high-$Q$ entry as *additional* entries. **Do NOT pick the operating $Q$** — the
     `2×10⁶` (foundry) vs `>10⁷` (class-leading) choice is a parked S0.2/S0.3 pre-registration decision.
   - `mrr_primitives.py` static Lorentzians + `drift_inject` + their tests → CW-limit **test
     references** + S0.3 drift knob.
   - `equalization_mrr_rc.py` ridge readout + delay-embedding → §5.3 reservoir-readout baseline stub.
   - one sweep skeleton (`sweep_phase4a_mrr1`) + `evaluate.py` JSONL pattern → generic bake-off runner
     scaffold (strip task-specific content; keep the resume-safe keyed-JSON orchestration pattern).
3. **Two architecture constraints, baked into the new skeleton from line one** (recon §3 warnings):
   - **(3a) Gradients must flow through the optical state.** Do **not** copy the repo's `no_grad`/`detach`
     ODE-integration style (correct for forward-only channels, fatal for our substrate where BPTT/PAT/
     adjoint need state gradients). Use the `TrainingAwareDynamicSOAPerMode` checkpointed-unroll pattern.
   - **(3b) Expose full state trajectories** in the forward/substrate API (the adjoint and RHEL
     estimators need them; the old `CascadedMRR_RC.forward` hides intermediate state — don't repeat that).
4. **Smoke test (salvage-validation, not core):** (i) all salvaged assets import and their ported tests
   pass; (ii) the salvaged **static Lorentzian** reproduces the analytic add-drop CW transfer function
   within a stated tolerance; (iii) the platform-registry FSR self-consistency test passes. *(The
   dynamical single-ring → pole model and its CW-limit match are the first task of S0.1, not here.)*

### Key gates and questions
- All 7 assets ported with provenance headers + passing re-run tests; SPSA FD-vs-autograd anchor reproduced.
- Report which contact points needed decoupling, any assets that resisted lifting, and confirm the two
  architecture constraints are honored in the skeleton.
- Honest flag if any salvaged asset drags in equalization assumptions that couldn't be cleanly severed.

### Deployment
Local CPU; minutes-to-~1 day. No cloud.

> **Parallel track:** the Critic is reviewing the Stage-0 roadmap concurrently
> (`shared/critic_instructions_stage0-roadmap.md`). S0.0 is pure infrastructure/salvage — upstream of any
> roadmap change — so the two run safely in parallel; Critic findings would affect S0.1+ (the science),
> not S0.0.

---

## ✅ DONE — S0.0a: Tooling reconnaissance (read-only)

**CLOSED 2026-06-07.** Report `shared/tooling_recon.md`. Finding: `pnn-multilayer` ring code is
static/CW (no optical-memory dynamics) → the SSM core is new under either ruling; salvage value is in the
estimator/infrastructure layer (SPSA + pass-accounting, rate-equation gain, SiN registry, drift, ridge
readout, sweep scaffold, static Lorentzians as CW-limit test refs). Recommended (a) selective salvage
(~1 day vs ~3–5 days for clean start). → Lucas ruled (a) + `git init` on 2026-06-08; folded into S0.0 above.

<!-- COMPLETED tasks accumulate below, newest first -->
