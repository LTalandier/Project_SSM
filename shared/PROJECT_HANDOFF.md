# Project_SSM — Handoff Brief

**Purpose.** A single self-contained snapshot so a fresh agent (new Claude Code session, Claude
Science project, or a human collaborator) is fully current without reading the whole repo. It captures
the mission, the **live methodological state** (what's frozen vs. pending signature — the part that is
*not* obvious from the files), the non-negotiable disciplines, and a file map.

**This is a snapshot, not an authority.** The authoritative documents are
`photonic-ssm-proposal-v0_5.md` (the spec) and `shared/preregistration.md` (the ledger). If this brief
and those disagree, **they win** — this file has drifted and should be updated.

**Last updated:** 2026-07-05 (doc-hygiene sweep) · packet-v2 state unchanged since `73099d5`.

---

## 1. Mission (one paragraph)

Build the case for the **first in-situ-trained recurrent photonic system**: an oscillatory
(LinOSS-style) **coupled-microring state-space model (SSM) on ultra-low-loss silicon nitride (SiN)**
whose *recurrence-defining* parameters — pole positions + inter-ring couplings — are trained **on the
physical device** by gradient-based / gradient-estimating methods. No recurrent photonic system has had
its physical recurrence trained in situ by any method. We are at **Stage 0**: theory + simulation, no
fabrication, no compute-cluster commitment — publishable on its own as a methods paper, and the gate to
everything downstream.

**The single load-bearing sentence (the white-space claim, sharpened):**
> *Recurrent parameters updated on the physical device by gradient-based/-estimating training* — never
> done. It must survive pre-emption by reservoir computing, the Bueno/Brunner photonic-RNN RL line, and
> internal-parameter reservoir variants. (Verification debt #1, front-loaded; see §5.)

**The centerpiece of Stage 0:** a **four-method in-situ-training bake-off** — **SPSA, PAT, recurrent
in-situ adjoint, RHEL** — on **one shared, realistic dissipative ring substrate** (finite $Q$, gain
saturation, injected ASE). Primary score: **sample-efficiency-to-target-accuracy under realistic
noise**. Gradient-cosine-error vs BPTT is a **secondary diagnostic only** (it flatters the exact
methods and penalizes SPSA). Rule: **parallel in simulation, singular in hardware** — the chip stays on
**PAT/SPSA** (hardware-committed primary); adjoint/RHEL are simulation-only and earn a *later* hardware
slot only if the bake-off shows one *clearly* beats PAT/SPSA on a metric that matters.

## 2. The four verification debts + the advantage question (track these)

1. **White-space claim** (the sentence above) — the load-bearing existence claim.
2. **LinOSS / D-LinOSS / Mamba-3 benchmark specifics** — the accuracy targets we must transfer to.
3. **Er:Si₃N₄ noise figure** — the flagship gain device has published gain but **no measured NF**
   (we register NF-A = 7.0 dB as the working assumption).
4. **Recurrent-adjoint gap** — inferred from absence of demonstrations (as of mid-2026).

Plus the **§10 advantage question** — *does a photonic SSM beat digital once E/O–O/E + DAC/ADC
conversion overhead is paid?* This is the **largest conceptual risk**, now a Stage-0 deliverable (the
S0.7 systems-advantage envelope). Every design choice that adds conversion channels (e.g. multi-point
optical drive) must be **priced against this envelope** — see §6, D1.

## 3. Where we are — live state (READ THIS)

**Stage 0, phase S0.4 (the fairness contract + first bake-off estimators).** Substrate is built and
green (**128/128 tests**). The immediate business is freezing the **S0.4 fairness/cost/PAT-mismatch
contract** before any estimator runs.

**S0.4 freeze packet — status: v2 committed (`73099d5`), awaiting Critic re-confirm → Lucas signature.**
- Four PROPOSED-v2 blocks live in `preregistration.md` after PR-4: **PR-6** (fairness contract,
  CRITICAL), **PR-7** (cost metric = device passes), **PR-5** (PAT twin-mismatch), **PR-12** (damping
  disposition, R-ii).
- These encode Lucas's three rulings (**saturating gain for all four estimators · clamp policy A ·
  R-ii damping-as-a-knob**) and the Supervisor's resolution of the Critic's two HIGH findings
  (**D1 / D2**, delegated by Lucas "OK I trust you", `E-2026-06-17-1`).
- **Nothing is ACTIVE for the Executor.** The next gate is a **brief Critic re-confirm** of v2 (focused
  spec staged at the end of `shared/critic_instructions_s0_4_freeze.md`), then **Lucas signs**.

**Immediate path:**
```
brief Critic re-confirm of v2  →  Lucas signs the v2 packet  →
S0.4-0 (calibration, $0 local, Executor)  →  S0.4a (PAT + SPSA — first bake-off estimators)
```

**S0.4-0 (queued, gated on signature — 5 items, all $0/local):**
1. **Input-map controllability measurement** (PR-6 §B / D1): find the minimal ≤K=4 input-tap set s.t.
   at cell C-2 (N=32), connected init, on-resonance, **every** ring's task gradient ≥ 10⁻³·ring-1.
   **Report tap count to the §10 envelope** (E/O cost). Fallback (c): down-scope to "front-of-chain in
   situ" if no bounded tap-set clears the gate.
2. **r_min measurement** (PR-6 §C v2): smallest r s.t. on-resonance the *saturating* κ_net ≥ 0.05κᵢ
   and the M1 §G(iii) margin holds; r_min = max(r*+0.02, r_M1) (candidate ≈ 0.15).
3. **§G-conformance check** (D2): is δ-dependent build-up a conformance fix (→ restore δ-awareness) or
   a model addition (→ log anchor-risk (vii))? Sweep δ over [−κᵢ, +κᵢ].
4. **Multi-point E₀ re-derivation** (PR-6 §G-addendum): re-evaluate the injection budget for the
   resolved input map (total-energy over taps).
5. **PR-5 recon** (lit): source twin-mismatch levels (Wright et al. *Nature* 2022 + SPSA hardware
   demos) to fill the [RECON-DEFERRED] levels.

## 4. What's frozen vs. what's proposed

**FROZEN — signed, Lucas-only to amend (supersession discipline):**
- **Roadmap v3.1** (signed 2026-06-08/09) — the S0.0–S0.8 + S0.L phase decomposition, the two gates,
  the diagonal complex-pole SSM (S4D/DSS-class) architecture with trainable inter-ring μ.
- **PR-15** (+ signed amendment **PR-15.1**) — the white-space existence-search kill-criterion (debt #1).
- **PR-10** — the S0.7-lite envelope assumption values.
- **PR-1** (FROZEN v2) + **PR-1.1** (SIGNED v2) — Gate-i margin/benchmark + the G3 adjudication
  (G3 FAIL on record, criterion void for anchor instability; PR-3 in-house ceiling = downstream anchor).
- **PR-2** — task + trainable-parameter partition P2={δ, κ_ext, μ} + readout (R2 intensity);
  **jointly freezes PR-13** (the secondary memory task — no standalone block; it lives inside PR-2).
- **PR-4 v2 (signed 2026-06-13)** — the S0.3 dissipative-ring substrate:
  - **M1 saturating gain** at operating point g_rt = 0.9×intrinsic → κ_net = 0.1κᵢ + 2κ_ext.
  - **A2** Langevin ASE; **NF-A** = 7.0 dB.
  - **K4** trainable band r = κ_ext ∈ [0.1, 3], θ₀ = 0.3; **K-pol-3** CW/CCW mode-splitting always-ON.
  - **Cells:** **C-1** P-FND / N=8 (Gate-ii @ 2 GS/s) · **C-2** P-AN800 / N=32 (**headline**) ·
    **C-3** P-UHQ / N=128 (aspirational).
  - **O2** intensity readout @ P̄₀ = 1 mW; **E₀** = 2·κ_ext,θ₀·(P̄₀/ħω₀)/κ_net² (single-port injection
    on bus of ring 1 — **being re-derived to multi-tap under D1**, ride-on registered as PR-6 §G-addendum).

**PROPOSED v2 — awaiting Critic re-confirm → Lucas signature (NOT yet frozen):** PR-6, PR-7, PR-5, PR-12.

**Key live finding — `D-2026-06-13-1` (the lasing threshold):** under saturating gain, κ_net crosses 0
at **r\* ≈ 0.134** (cell-independent). Below r\* the ring lases and the linear rollout diverges. So the
*effective* trainable band is [≈0.134, 3], not the registered K4 [0.1, 3]. **Clamp A** raises the
saturating-mode lower bound to **r_min** (measured at S0.4-0; candidate ≈ 0.15) rather than hard-capping
gain (B) or adding a soft loss barrier (C).

## 5. Non-negotiable disciplines (do not violate)

- **Three roles, hard boundaries.** **Supervisor** = methodology, analysis, paper, task assignment —
  does **not** write or run simulation code (may *run existing tests* to verify as evaluation).
  **Executor** = writes/runs simulation code, reports results — does **not** design methodology or write
  the paper. **Critic** = adversarial review only, and **reports to Lucas, not the Supervisor** — the
  Supervisor cannot dismiss a Critic finding without escalation. This independence has caught real
  signature-blockers; **preserve it in any new environment** (a subordinate reviewer agent is not the
  same guarantee).
- **Sessions are launched by Lucas** in separate terminals. **Never** spawn Executor/Critic as headless
  background agents.
- **Supersession discipline.** Frozen ledger entries are **Lucas-only** to amend. A change that touches
  a frozen block is registered as an *addendum ratified by Lucas's signature*, never a unilateral edit.
- **Pre-register before the run.** Every tunable margin / gate / cell / budget freezes in
  `preregistration.md` *before* the run that tests it. Measure-then-freeze: register the *rule*, measure
  the *number*, addend before consuming the run.
- **Always ask before significant decisions** (scope / methodology / architecture, compute spend,
  pre-registered margins). Log to `shared/decisions_needed.md` (→ Supervisor) or
  `shared/escalate_to_human.md` (→ Lucas). **Cloud-compute spend needs Lucas's approval.**
- **Quality bar:** ≥ 4 seeds/config (≥ 8 for high-variance, esp. SPSA); every experiment specifies
  ranges/seeds/metric/runtime; results report raw-data path + summary + variance + anomalies. The four
  estimators share **one** substrate so the bake-off is apples-to-apples.
- **Environment:** `python3` (not `python`). Commit to `main` (single-branch coordination convention),
  no push unless asked. Prior repos (`pnn-multilayer`, `Project_AR_ParetoPNN`, `PNN_topology_search`,
  `Project_research_orchestr`) are **read-only reference**. Commit-message trailer:
  `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.

## 6. Glossary of the calls in flight

- **Saturating gain** = g(P̄) = g₀/(1+P̄/P_sat), the faithful M1 form (∂g/∂κ_ext = −0.75 at θ₀); chosen
  for all four estimators. `fixed` (g ≡ 0.9κᵢ, ∂g/∂κ_ext ≡ 0) is a demoted diagnostic that the frozen
  B1/E₀ numbers live on.
- **Clamp A** = operative saturating band κ_ext ∈ [r_min, 3]; r_min rule frozen (m_κ = 0.05,
  Δr = 0.02), number measured at S0.4-0. Chosen over B (hard-cap g — adds unregistered mechanism +
  kinks ∂g/∂κ_ext) and C (soft barrier — can't stand alone; divergence is in the forward recurrence).
- **PR-12 R-ii** = D-LinOSS damping treated as a *trainable per-ring net loss* via κ_ext over the
  clamped box at fixed g_f = 0.9 — **not** a g_f sweep (which would contradict signed PR-4 §G).
- **D1** (Critic P6-F1, deep-ring starvation) = single-drive + NN chain leaves ring-32 at ~2.2e-28 rel.
  gradient. Resolved: **measured-minimal-controllable input map** (fewest taps, gate ≥ 10⁻³·ring-1, E/O
  cost priced to §10 envelope, honest down-scope fallback).
- **D2** (Critic P6-F2, inert δ-aware clamp) = the "δ-aware" clamp was inert as-built (clause (b) used
  the fixed-plane κ_net, which never diverges). Resolved: **clamp on-resonance on the *saturating*
  κ_net**, drop the "δ-aware" label, log off-resonance de-saturation as **anchor-risk (vii)**, with an
  S0.4-0 §G-conformance check that may restore genuine δ-awareness.

## 7. File map

**Authoritative:**
- `photonic-ssm-proposal-v0_5.md` — the spec. Read first. (`…-tfln-proposal-v0.2.md` is superseded.)
- `shared/preregistration.md` — **the ledger** (PR-#). The heart of the methodology.

**Coordination (`shared/`):**
- `stage0_roadmap.md` — master Stage-0 plan (S0.0–S0.8 + S0.L, the bake-off, the two gates).
- `task_queue.md` — Supervisor assigns; Executor runs the **ACTIVE** task (currently NO ACTIVE TASK).
- `results_log.md` — Executor writes results; Supervisor evaluates.
- `decisions_needed.md` — Executor → Supervisor design questions.
- `escalate_to_human.md` — either agent → Lucas (holds `E-2026-06-17-1`, the D1/D2 delegation).
- `supervisor_feedback.md` — Supervisor progress notes.
- `launch_executor.md` / `executor_instructions.md` / `critic_instructions.md` — role onboarding.
- `critic_instructions_s0_4_freeze.md` — the S0.4 packet review spec (+ v2 re-confirm addendum at end).
- `critic_review_s0_4_freeze.md` — the Critic's AMEND review (the two HIGH findings).
- `tooling_recon.md` — the S0.0a salvage manifest (7 assets from `pnn-multilayer`).

**Project instructions:** `CLAUDE.md` — roles, launch commands, quality standards, ecosystem.

**Code:** the dissipative-ring substrate + the four estimators (new Stage-0 code) + salvaged
estimator/infrastructure layer. Tests: `tests/` (`test_substrate.py` et al.) — **128 passing**.

**Memory (auto-loaded each session):**
`/home/lucas/.claude/projects/-home-lucas-Documents-Project-SSM/memory/` — `MEMORY.md` (index) +
`project-ssm-stage0.md` (full running state) + `research-workflow.md`.

## 8. If you are onboarding into a *new* environment (e.g. Claude Science)

- **Bring the git repo** — it *is* the portable state. Point the new project at it; `CLAUDE.md` is
  already a strong project brief.
- **This file** is the live-state layer the raw files don't spell out. Read it, then read
  `preregistration.md` and `stage0_roadmap.md`.
- **Preserve the disciplines in §5** — especially independent-Critic review and supersession. Do not
  collapse the three roles into one coordinating agent without deliberately reconstructing Critic
  independence.
- **Do not start Executor work** (anything that writes/runs simulation code) — it is gated on Lucas's
  signature of the v2 packet and is the Executor's job, launched by Lucas.
