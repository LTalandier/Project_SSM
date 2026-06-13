# Project_SSM — status snapshot, 2026-06-13 (S0.3-1 substrate ACCEPTED)

**Supersedes** `docs/project_status_2026-06-11_s0_2_closed.md`. Resumption-grade: a cold reader
(or a post-compaction session) should be able to pick up the project from this file alone.

Maintained by the **Supervisor** (Claude Opus 4.8). Authoritative spec: `photonic-ssm-proposal-v0_5.md`.
The live ledger is `shared/preregistration.md`; the live plan is `shared/stage0_roadmap.md`.

---

## 1. Where we stand (one paragraph)

We are building the case for the **first in-situ-trained recurrent photonic system** — an
oscillatory (LinOSS-style) coupled-microring state-space model on silicon nitride whose
recurrence-defining parameters (pole positions + inter-ring couplings) are trained *on the
physical device*. We are in **Stage 0** (theory + simulation, no fab, publishable). As of today
the **shared dissipative-ring substrate is built, verified, and accepted** — this is the single
model all four training methods will run on in the S0.5 bake-off. The substrate freeze (**PR-4
v2**) is signed; the build (**S0.3-1**) passed its gate (F18) under both my verification and an
independent Critic re-run, and the Critic returned **APPROVE-WITH-EDITS**. The edits are
freeze-conforming (no methodology change) and are queued for the Executor as **S0.3-1b**. The
project is **not blocked**: two items await Lucas (one confirmation, one freeze reconciliation),
and the next freeze cluster (PR-6/PR-5/PR-7) gates the start of S0.4 (the estimators).

---

## 2. The frozen rulebook (pre-registration ledger)

🔒 = signed/frozen (Lucas-only amendments henceforth). ⬜ = open.

| PR | Scope | Status |
|----|-------|--------|
| **PR-1 v2** | Gate (i) accuracy criterion | 🔒 FROZEN 2026-06-10 · **amended by PR-1.1** |
| **PR-1.1 v2** | G3-FAIL adjudication | 🔒 **SIGNED 2026-06-11** — G3 criterion **void for anchor instability** (F-G3); Gate i adjudicated **purpose-served** (G1 PASS ∧ numerical-parity dossier); no replacement anchor (downstream reference = PR-3 in-house BPTT ceiling); **transfer-check freeze rule binding** |
| **PR-2 v2** | Bake-off task + architecture | 🔒 FROZEN 2026-06-10 — T-A Jaeger–Haas 4-PAM channel-eq @ 2 GS/s headline (+ MS/s honesty line); intensity \|·\|² readout; trainable partition **P2 = {δ_j, κ_ext,j, μ_jk}**; N-grid {8,32,128} headline 32; nearest-neighbor chain; Vinckier-class reservoir baseline; F6 κ_ext held at θ₀; F12 same-SNR train/test |
| **PR-3** | S0.5 target rule + ceiling | ⬜ — *rule* before S0.4 close; *ceiling* measured + frozen at S0.4 close |
| **PR-4 v2** | **Shared substrate + Gate ii cell** | 🔒 **SIGNED 2026-06-13** — see §2a |
| **PR-5** | PAT twin-mismatch | ⬜ — freeze before S0.4a |
| **PR-6** | **Fairness contract** (CRITICAL) | ⬜ — freeze before S0.4a; now also owns the connected-init + gain-mode-for-all-estimators + sweep-recipe registrations (see §5) |
| **PR-7** | Cost metric (device passes) | ⬜ — freeze before S0.4 |
| **PR-8** | S0.5 statistical plan | ⬜ — ≥8 seeds headline |
| **PR-9** | Gate-ii semantics + promotion | ⬜ |
| **PR-10** | S0.7-lite envelope assumptions | 🔒 FROZEN 2026-06-10 — clocks {0.1, 1, 2} GS/s |
| **PR-11** | RHEL echo invariants | ⬜ — freeze at S0.4c |
| **PR-12** | Central damping cell | ⬜ — **deferred** (see §5); freeze after a convergence-controlled rerun |
| **PR-13** | Synthetic memory-task secondary | 🔒 FROZEN 2026-06-10 — sticky-marker family, k ∈ {1,3,10,30,100} |
| **PR-14** | Secondary diagnostic (bias/var) | ⬜ |
| **PR-15 / 15.1** | White-space continuation gate (debt #1) | 🔒 FROZEN 2026-06-09 / AMENDED+signed 2026-06-10 — one-sided PASS (provisional; final sweep at S0.8) |

### 2a. PR-4 v2 — the frozen substrate (the centerpiece of this snapshot)

One substrate model; the cells are registered parameter points of it. Conventions inherited from
S0.1 (amplitude rates; κᵢ = ω₀/2Qᵢ; κ_tot = κᵢ + 2κ_ext symmetric add-drop; ZOH/van-Loan; 100-GHz
FSR; λ = 1550 nm).

- **Gain — M1 static saturated operating point** (ruling E-2026-06-11-2): differentiable
  g(P̄) = g₀/(1+P̄/P_sat) at the **intracavity** plane, **operating point g_rt = 0.9 × intrinsic
  per-rt loss** ⇒ κ_net = 0.1·κᵢ + 2κ_ext; passive (g=0) and 0.5× are labelled sensitivity rows.
  Three registered validity conditions (stationary episodes / ensemble-power stationarity /
  quasi-static margin); bursty inputs void. **M2** = one-off rate-equation validation (τ=3.4 ms)
  at C-2/θ₀ and C-1/θ₀. **M3** (sub-ns rate equation) = deferred branch, pre-committed trigger
  (margin form freezes with PR-5–9/PR-11, before any bake-off results; or a Stage-2 III-V tilt).
- **ASE — A2 Langevin** ⟨FF*⟩ = 2κ_g n_sp δ, van-Loan-discretized; A1 per-rt-kick = registered
  first-order equivalent (unit-tested); n_sp from NF-A (n_sp = 2.5); fresh draws per pass,
  forward/echo independent (PR-11).
- **Cells — C-1 P-FND** (Qᵢ=2×10⁶, γ 90 MHz, **N=8, Gate ii @ 2 GS/s**) · **C-2 P-AN800**
  (Qᵢ=6.8×10⁶, γ 11.8 MHz, **N=32, bake-off headline**) · **C-3 P-UHQ** (Qᵢ=3×10⁷, **N=128,
  aspirational**). **NF-A 7.0** headline everywhere (rider R1). Sensitivity: P-CORN (passive),
  C-2-derate ×2 loss, γ/NF menus.
- **κ_ext — K4 trainable** r ∈ [0.1, 3] (forced by the PR-2 P2 partition), **θ₀ = 0.3**.
- **Splitting — K-pol-3 always ON** (γ=0 recovers single-pole); rider R2 N-grid pinning in-block.
- **Holding — H1** worst-case. **Normalization — O2** intracavity-energy budget @ P̄₀ = 1 mW,
  P_pk = 2P̄₀ (4-PAM); **E₀ = 2·κ_ext,θ₀·(P̄₀/ħω₀)/κ_net²** (closed form, inputs pinned).
- **C-2 anchor (Cui 2023):** registered as a **conservative bound** on the platform numbers;
  **body-level numbers confirmed [EV] 2026-06-13** via an independent peer-reviewed commentary
  (Ye & Marpaung, *Adv. Photon.* 5(5) 050503, CC-BY, reproduces Cui's figures; archived
  `docs/s0_3/refs/`). Our 6.8M sits below the worst device in Cui's 249-resonance distribution.
  Residual risk (i) closed; geometry-transfer risk (ii) priced by the ×2-loss derate row.
- **Calibration addendum (2026-06-13, the registered deferral, discharged):** numeric E₀ — C-1
  3.14×10⁷ / C-2 1.07×10⁸ / C-3 4.72×10⁸ photons. **Reachability (honest):** on the operative
  intracavity plane the operating point needs ≈380 dB/cm (C-2) / 403 (C-3) small-signal gain vs
  demonstrated Er ≤ 1.9 dB/cm ⇒ **all gain-bearing cells are material-aspirational** (Stage-1
  integration risk, anchor-risk (v)). Does not affect runtime (g₀ is a model knob).

---

## 3. Results on the books (with exact figures)

- **G1 Heartbeat GATE — PASS.** In-house LinOSS layer 72.9032 ≥ 72.1 pre-registered; float32-exact
  vs the official implementation (~2×10⁻⁷). The port is exonerated.
- **G3 EigenWorms — FAIL on record, criterion VOID (PR-1.1).** Our port 71.11 < 90.6; **the
  official code faithfully rerun also fails its own anchor** (90.56 < 90.6, σ 9.34 ≈ 2.1×
  published 4.4) — an fp32 zero-gradient absorbing state, an *optimization* collapse with
  environment-contingent seed incidence. The void rests on dispersion + mechanism, not any k/n.
  Reportable finding **F-G3** (S0.8-binding). Archived per-environment evidence regenerated
  (S0.2-1R).
- **S0.3-1 substrate build — F18 build gate PASS (Supervisor 9/9, Critic re-run 9/9).** Passive
  limit bit-identical to the S0.1 forward model (1.4×10⁻²⁰); every registered PR-4 number
  reproduces from the substrate (2γ/κ, memory 9.4/32.0, in-band 29.5/100, n_ss 22.55/8.98,
  A1↔A2 2.1×10⁻³); E₀ to ~1e-15; gradient-flow + checkpoint exact. **M2 quasi-static confirmed**
  (ripple 2×10⁻⁵ ≪ 3% bound, both cells). Coarse BPTT damping sweep produced (→ PR-12, confounded).
- **Critic S0.3-1 review — APPROVE-WITH-EDITS.** Build correct + freeze-faithful. **Finding S-F1
  confirmed and elevated HIGH**: the default `gain_mode="fixed"` drops ∂g/∂κ_ext (27% of the
  κ_net gradient at θ₀, 6× and sign-flipped at the r=0.1 edge); freeze §G/§N-E6 mandate the
  `saturating` mode → code-conformance fix, no freeze change. Plus S31-F2..F8 (see §5).

---

## 4. Spend

- **GPU (S0.2 Gate-i cross-checks):** $1.15 of Lucas's $7.44 vast.ai credits (E-2026-06-10-5).
- **S0.3-1 substrate build:** $0 — local CPU, ~15 min.
- **Forward look:** the S0.5 bake-off grid (≈6 methods × ≥8 seeds × C-2) is **near the
  local/cluster boundary** — to be sized at the PR-6/PR-7 freeze; C-3/N=128 stays the aspirational
  axis, out of the gating path. Any cluster spend escalates to Lucas.

---

## 5. Open decisions and queued work

**For Lucas (E-2026-06-13-2 — neither blocks today):**
1. **CONFIRM** (not reinterpret): all four estimators run `gain_mode="saturating"` (the freeze
   mandates it; the consequence — SPSA and the gradient methods target one function — is a **PR-6**
   registration).
2. **RECONCILE PR-4 §G ↔ PR-12** (touches signed PR-4): the damping sweep's g_f axis *is* the
   registered g_f=0.9 operating point, so PR-12 can't freely pick a g_f. Reading (R-i) PR-12 is
   subsumed by §G; reading (R-ii, Supervisor's lean) D-LinOSS damping is a distinct knob (the
   trainable per-ring loss range at fixed g_f=0.9) and the rerun should vary that.

**ACTIVE (Executor) — S0.3-1b, freeze-conforming edits:** flip `gain_mode` default → `saturating`;
harden `test_h` (run faithful mode + assert the gain path is live + a connected-init variant);
surface the intracavity reachability in the calibration artifact; rewrite `test_no_equalization_coupling`
to assert the source-stack symbols absent (not a token); register the ASE-detach convention in code.

**Deferred / carried (gated on the above):**
- **PR-12** — convergence-controlled damping rerun (train-to-fixed-loss, not fixed-steps) + 8 seeds
  at the candidate point, after the PR-4/PR-12 reconcile. *Why deferred:* the coarse curve conflates
  achievable accuracy with training speed at a fixed 500-step budget.
- **PR-6 / PR-5 / PR-7** freeze before S0.4a — PR-6 now also owns: the **connected init** (μ(0)=0
  signal-starves rings 2..N → the N=32 headline cell is untrainable from cold — top S0.4 risk); the
  **gain-mode-for-all-estimators** registration; the **sweep recipe** (batch/LR/grad-clip/δ-band).
- **PR-11** generator-distinctness (independent forward/echo ASE streams) — enforced at S0.4c.
- **M3 trigger margin form** — frozen with PR-5–9/PR-11, before any bake-off results.

---

## 6. Path ahead

```
S0.3-1b edits (Executor)  ∥  Lucas CONFIRM + RECONCILE
        └────────────┬───────────────┘
                     ▼
   PR-6 / PR-5 / PR-7 freeze  (+ PR-12 disposition, + PR-3 rule)   ← Supervisor drafts, Lucas signs
                     ▼
   S0.4a  PAT + SPSA on the substrate   (the hardware-committed workhorses)
   S0.4b  recurrent in-situ adjoint     (parallel, simulation only)
   S0.4c  RHEL + concrete χ³ echo sub-model + PR-11 invariants
   S0.4 close: measure + freeze the BPTT-on-substrate ceiling (PR-3); per-method hardware ledger
                     ▼
   S0.5  the bake-off + baselines → Gate ii   (sample-efficiency-to-target the headline metric)
                     ▼
   S0.6 (damping init/range sweep) → S0.7-full envelope (§10 advantage question) → S0.8 (paper)
```

S0.L (literature) runs alongside: debt #1 (done, provisional) · #2 (discharged) · #3 (resolved) ·
**#4 at S0.8**. The §10 advantage question (does a photonic SSM beat digital once conversion
overhead is paid?) is the largest conceptual risk — answered by the S0.7-full envelope.

---

## 7. The four verification debts (proposal v0.5)

1. **White-space claim** (recurrent params trained on the physical device — never done) —
   **provisional PASS** (PR-15.1 one-sided gate); final dated re-sweep at S0.8.
2. **LinOSS / D-LinOSS / Mamba-3 benchmark specifics** — **discharged** (PR-2/PR-13).
3. **Er:Si₃N₄ noise figure** — **resolved, premise false**: the flagship NF is *measured* ≈ 7 dB
   (three-way verified). NF-A 7.0 is the registered headline noise. (S0.8 reword owed.)
4. **Recurrent-adjoint gap** (inferred from absence of demonstrations) — **outstanding**;
   re-verify at first full-text pass.

---

## 8. Coordination state + launch commands

Three local Claude Code sessions coordinate through `shared/`:

| Role | Session | Now |
|------|---------|-----|
| **Supervisor** (this one) | Opus 4.8 | drafting PR-6/5/7 next (after Lucas's confirm/reconcile); maintains the ledger |
| **Executor** | separate terminal | **S0.3-1b ACTIVE** — can run now (freeze-conforming) |
| **Critic** | separate terminal | idle (last: APPROVE-WITH-EDITS on S0.3-1) — reports to **Lucas** |

```bash
# Executor (run S0.3-1b):
cd ~/Documents/Project_SSM && claude "Read shared/launch_executor.md and follow it."

# Critic (when next spec'd):
cd ~/Documents/Project_SSM && claude "Read shared/critic_instructions.md, then review the target it names."
```

**Live files:** `shared/preregistration.md` (ledger) · `shared/stage0_roadmap.md` (plan) ·
`shared/task_queue.md` (S0.3-1b ACTIVE; S0.3-1 ACCEPTED block) · `shared/results_log.md`
(+ Supervisor evaluations) · `shared/escalate_to_human.md` (E-2026-06-13-2 OPEN) ·
`shared/supervisor_feedback.md` · `shared/critic_review_s0_3_1.md`. Code: `photonic_ssm/substrate/`,
`tests/test_substrate.py`. Latest commit at write time: `42e27ed`.
