# Project_SSM — Pause Snapshot (2026-06-10, evening)

**What this is:** Lucas paused the project this evening (the EigenWorms benchmark runs need
3–4 days of local compute — too long to sit through right now). This file is the
resumption-grade record: what stands, what's mid-flight, what decision comes first when work
restarts. It supersedes the morning snapshot (`docs/project_status_2026-06-10.md`, written at
the continuation gate) as the current state of record.

---

## 1. The thirty-second version

We are building the case for the **first in-situ-trained recurrent photonic system** — a
coupled-microring state-space model on silicon nitride whose recurrence-defining parameters
(pole positions + inter-ring couplings) get trained on the physical device. Stage 0 = theory +
simulation only; its centerpiece is a four-method training bake-off (SPSA, PAT, recurrent
adjoint, RHEL) on one shared realistic ring model.

As of this pause: the claim survived a structured novelty kill-search; the build-it-at-all
economics survived a Critic-audited envelope analysis; Lucas ruled **GO** on the bake-off arm;
the two freezes that define the bake-off (PR-1, PR-2) are signed after an independent Critic
review that caught one critical design error before anything ran; **the project's first
training runs happened — and the first reproduction gate PASSED** (Heartbeat, 72.90% vs the
frozen 72.1% threshold). The second, longer gate run (EigenWorms) is paused mid-flight. The
substrate design recon for the next phase is already done and waiting.

## 2. The frozen rulebook (pre-registration ledger)

Five entries are 🔒 FROZEN (Lucas-signed; amendments need his signature):

| Entry | What it locks |
|---|---|
| **PR-15 / PR-15.1** | The novelty kill-rule + the W1 claim wording. Verdict: provisional one-sided PASS (0 fatal priors in 80+ papers; final dated sweep at S0.8). |
| **PR-10** | All S0.7-lite envelope assumptions (conversion energies, baselines, N/rate grid). |
| **PR-1** | Gate i: reproduce published LinOSS — Heartbeat ≥ 72.1% AND EigenWorms ≥ 90.6%, official 5-seed protocol, official code = reference, no tuning. |
| **PR-2** | The bake-off object: Jaeger–Haas channel equalization @ 2 GS/s headline (binding MS/s honesty line), one photonic ring layer N=32 headline, **intensity \|·\|² readout** (the Critic's PF-F1 fix), trainable set {detunings, coupler strengths, inter-ring couplings}, reservoir baseline = same physics with recurrence frozen. |
| **PR-13** | The synthetic memory-task family (lags 1→100; class-balanced sticky marker), frozen early with PR-2. |

Still open (each freezes at its phase boundary): PR-3 (BPTT-ceiling rule), **PR-4 (substrate
operating point + noise cell — the next freeze)**, PR-5–PR-9, PR-11, PR-12, PR-14.

## 3. Results on the books

- **S0.1 — ring↔oscillator mapping:** realizable pole region bounded; the memory yardsticks
  everything is sized against (e.g. 6.58 samples of 1/e memory @ 2 GS/s at the foundry corner;
  98.7 at class-leading).
- **S0.L-1 — novelty search (debt #1):** no prior in-situ gradient-trained recurrent photonic
  system found under the frozen rule; claim provisionally ours.
- **S0.7-lite — systems envelope:** conditional positive, Critic-audited. Optimistic corner
  clears the FPGA serving anchor by up to 14.7×; embedded-GPU *peak* never beaten; niche =
  GS/s streaming, N=32–128, sub-µs latency.
- **S0.2-0 — benchmark recon (debt #2):** every published LinOSS-class number is uncoupled
  (μ=0); **no published coupled result exists** — our coupled generalization leans on the
  in-house BPTT ceiling (PR-3), as registered.
- **S0.2-1 (partial) — the first training runs:**
  - The in-house layer is **float32-exact** against the official JAX model (transplanted
    weights agree to ~2×10⁻⁷) — our code *is* the published computation.
  - **G1 Heartbeat: GATE PASS** — gated 5-seed mean 72.9032% ≥ 72.1% (+0.80 pp,
    −0.78σ of published; Supervisor-verified from the per-seed table). Zero tuning.
  - Split-pinning paid off: the official pipeline deletes 23 duplicate EigenWorms samples
    (N=236, not 259) — a reimplementation would have silently diverged.
  - **G3 EigenWorms: paused mid-run** (see §4).
- **S0.3-0 — substrate recon + PR-4 inputs (done, accepted):**
  - **Verification debt #3 is dead — its premise was false.** The flagship Er:Si₃N₄ amplifier
    (Liu, Science 2022) *did* measure its noise figure: **≈7 dB** (7.1 dB worked example),
    three-way verified; nothing else in the literature through 2026-06. The PR-4 noise menu
    now anchors on a *measured* number (menu: 7.0 measured / 5.0 comparable-class / 3.0
    floor-aspirational). Lesson recorded: debt #4 is the same "inferred absence" type — re-verify
    at first full-text contact.
  - **Erbium gain is rigorously quasi-static** at our clocks (τ = 3.4 ms vs ns symbols) — which
    opens the one methodology fork now standing (§5).
  - **N=128 is only realizable at the class-leading-Q corner** (and exactly in its
    mode-splitting regime — only the CW/CCW knob ON survives); N=8 works at the foundry corner;
    N=32 needs mid-grade. The foundry-corner memory death of the headline task was
    **pre-registered** as an interpretable outcome (PF-F3), so nothing needs amending.
  - **CORNERSTONE can only host a passive cell** (gain budget doesn't close there).
  - PR-4 input sheet ready: 3 candidate noise cells, κ_ext policies, holding conventions,
    encoder power-normalization mechanisms. One [AV] to verify at freeze: Cui 2023 as the
    AN800 registry primary.

## 4. Mid-flight: the paused G3 runs (exact state)

Seeds 2345/3456/4567 launched 18:48, **SIGSTOPped by Lucas 19:36** (~47 min in, before the
first eval record). Verified at pause-snapshot time: driver PID 1412412 + workers
1412415/16/17 in state T, ~3.2 GB resident.

- **The state survives closing sessions/terminals — it does NOT survive a reboot.** A reboot
  simply restarts the affected seeds from step 0, which is protocol-clean (no mid-run state is
  ever reused); the only loss is ~47 min × 3 of compute.
- **Resume local:** `kill -CONT 1412412 1412415 1412416 1412417` → ~3–4 days to the gate
  verdict (seeds 5678/6789 queue behind the first wave; annex-3 trails at idle).
- **Cloud route:** one A100, ~$30–60 spot, all 8 seeds fast. Needs Lucas's spend approval
  (pro forma — he'd be the one choosing it) + one GPU parity-revalidation pass before the gated
  runs (the harness is rerunnable there).
- **Or stay paused.** Nothing degrades except the reboot-fragility above; $0 committed.

Gate i's joint verdict (and S0.2-1's closure) waits on G3. Given the float32-exact parity and
the pinned splits, the residual G3 risk is statistical, not implementation.

## 5. First decisions on resumption (in order)

1. **G3 compute route** — Lucas: cloud (~$30–60, days→hours), resume local (free, 3–4 days),
   or keep holding. (D-2026-06-10-2 addendum.)
2. **The erbium gain-regime fork (M1 vs M3)** — the one methodology decision standing. Because
   Er responds in milliseconds and symbols pass in nanoseconds, the SiN-native substrate (M1)
   has *linear* in-loop physics: static saturated gain + ASE, with the task-solving
   nonlinearity at the readout photodiode — structurally the same configuration the PF-F1 fix
   froze into PR-2, which is consistent, but it must be named deliberately (the alternative M3
   = III-V/SOA-class dynamic gain is a different platform story). Supervisor proposes, Lucas
   blesses; it folds into the PR-4 freeze. **S0.3-1 (substrate build) is blocked behind this
   by design.**
3. **The PR-4 freeze** — Supervisor drafts the PROPOSED block from the input sheet (operating
   (α,Qᵢ) pairs, noise cell, κ_ext policy, splitting knob, holding convention, power
   normalization; verify the Cui [AV] at freeze) → Critic phase-boundary review → Lucas
   signature. Same pattern that caught PF-F1 last time.
4. Then **S0.3-1**: build the shared dissipative substrate all four estimators train through.

Standing non-blocking items: NTT/Fisher/Shi full-texts (Lucas, claim-wording-paced); debt-#3
reword at S0.8 (Supervisor); annex-3 Heartbeat seeds already done, EigenWorms annex trails the
verdict.

## 6. Process health

The three-session protocol (Supervisor / Executor / Critic, launched by Lucas in separate
terminals) is restored and demonstrably working: the Critic's pre-run review caught a
critical design error (PF-F1 — an end-to-end-linear headline that could never approach its
anchor) *before* a single training step; the split-reproduction pin it demanded surfaced the
N=236 dedup; the Executor's runtime flag fired exactly per spec and held G3 rather than
improvising. Verification debts: #1 provisionally cleared (final sweep at S0.8), #2
substantially discharged, #3 resolved (premise false — measured 7 dB), #4 outstanding (S0.8;
now flagged same-type-as-#3).

## 7. How to resume

```bash
# Supervisor (this session's role):
cd ~/Documents/Project_SSM && claude
#   → say "resume from docs/project_status_2026-06-10_pause.md" and give the G3 route ruling.

# Executor (only after the route ruling; do NOT relaunch runs over the paused PIDs):
cd ~/Documents/Project_SSM && claude "Read shared/launch_executor.md and follow it."

# Critic (next needed at the PR-4 phase boundary):
cd ~/Documents/Project_SSM && claude "Read shared/critic_instructions.md, then review the target it names."
```

Queue state at pause: **no ACTIVE task** (S0.3-0 closed-accepted; S0.2-1 ⏸️ awaiting the G3
route). The next Supervisor outputs are the fork proposal + the PROPOSED PR-4 block.
