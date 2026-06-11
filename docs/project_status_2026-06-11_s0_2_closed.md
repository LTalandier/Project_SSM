# Project status — 2026-06-11: S0.2 closed, S0.3 opening

**Author:** Supervisor · **Supersedes:** `docs/project_status_2026-06-10_pause.md` (the pause
snapshot — the project resumed via the GPU route the same evening and S0.2 is now fully closed).
**Audience:** Lucas + any session re-orienting cold.

---

## 1. Where we stand, in one paragraph

Stage 0 has cleared its first measured gate cycle. The in-house LinOSS layer is built and
**proven numerically identical to the published reference implementation** (float32-exact,
~2×10⁻⁷ full-model, both anchor configs); the Heartbeat anchor **passed its frozen gate**
(G1: 72.90 % ≥ 72.1); the EigenWorms anchor **failed as measured** (G3: 71.11 % < 90.6) — and
the gate-miss diagnosis produced the project's first reportable finding (**F-G3**): *the
published anchor itself does not survive a faithful rerun of its own implementation*. After
independent Critic review and an archived record repair, Lucas signed **PR-1.1** (2026-06-11):
the FAIL stays on the books, the G3 criterion is void for anchor instability, Gate i is
adjudicated purpose-served on G1 + the parity dossier, and all downstream accuracy anchoring
moves to the in-house BPTT ceiling (PR-3) as registered. S0.2-1 is closed. The next move is
S0.3: one open decision (the gain-regime fork, **E-2026-06-11-2**, recommendation M1), then
the PR-4 substrate freeze, then the S0.3-1 build.

---

## 2. The frozen rulebook (`shared/preregistration.md`)

| Entry | Status | Content (one line) |
|---|---|---|
| **PR-15 / PR-15.1** | 🔒 signed | White-space gate: claim W1 (first in-situ-trained recurrent photonic system — pole positions + couplings trained on-device). **Provisional one-sided PASS**; NTT/Fisher/Shi full-texts re-paced to the claim-wording freeze (Lucas). Final sweep at S0.8. |
| **PR-10** | 🔒 2026-06-10 | S0.7-lite envelope assumptions (conversion energies, DAC/ADC, digital-baseline class, clocks {0.1, 1, 2} GS/s). Envelope ran: conditional-positive, Critic-audited. |
| **PR-1 v2** | 🔒 2026-06-10 | Gate i: G1 Heartbeat ≥ 72.1 AND G3 EigenWorms ≥ 90.6, Walker 5-seed protocol, official code = reference behavior, no-tuning closure rule, miss-rule "stop, don't tune". |
| **PR-1.1 v2** | 🔒 **SIGNED 2026-06-11** | G3 FAIL recorded permanently · G3 criterion **void for anchor instability** (F-G3) · Gate i **adjudicated purpose-served** (G1 PASS ∧ numerical-identity dossier) · **no replacement published anchor** — downstream reference = PR-3 in-house ceiling · F-G3 = reportable finding (S0.8-binding; every citable number archived + environment-qualified) · **new binding rule: reference-implementation transfer check before any externally-anchored accuracy/threshold freeze** (physics freezes out of scope per GA-F6). |
| **PR-2 v2** | 🔒 2026-06-10 | Bake-off object: T-A Jaeger–Haas channel eq @ 2 GS/s headline (+ binding MS/s honesty line) · **R2 direct-detection intensity \|·\|² readout** (Critic PF-F1 fix — the v1 R1+linear-head hybrid was end-to-end linear) · trainable partition P2 {δ_j, κ_ext,j, μ_jk}, all thermo-optic · N grid {8, 32, 128}, headline 32 · nearest-neighbor chain · reservoir baseline = Vinckier-class (F6 hygiene: κ_ext at θ₀) · F12 conventions (streaming, μ(0)=0, dt≡1/f_s, same-SNR train/test). |
| **PR-13** | 🔒 2026-06-10 (early) | Secondary memory-task family: sticky detection, k ∈ {1, 3, 10, 30, 100}, class-balanced rare marker P(marker) = 1−2^(−1/k). |
| PR-3 | ⬜ | The in-house BPTT-ceiling anchoring *rule* — freeze before S0.4 close. Now the project's only accuracy-anchoring layer (per PR-1.1). |
| **PR-4** | ⬜ **next** | The substrate cell: (α,Qᵢ) pair · NF/ASE · κ_ext policy · splitting sub-parameter · holding convention · drive normalization · **the registered gain-model class (M1/M3 — the open fork)**. Input sheet ready: `docs/s0_3/pr4_input_sheet.md`. Verify Cui 2023 [AV] at freeze. |
| PR-5–9, PR-11, PR-12, PR-14 | ⬜ | Estimator/bake-off details · RHEL echo invariants · damping cell (after S0.3 coarse sweep) · misc. |

---

## 3. Results on the books (`shared/results_log.md`)

- **S0.0 ✅** — tooling recon + 7-asset salvage manifest from `pnn-multilayer` (SPSA engine,
  gain/ASE, rate-equation SOA, platform registry, static Lorentzians as CW test references,
  ridge readout, sweep runner). Key overturn: the ring/training code is *not* liftable — the
  dynamical SSM core is new code.
- **S0.1 / S0.1.1 ✅** — dynamical CMT ring core + N-oscillator LinOSS forward model + the
  realizable pole region; Critic-driven closeout (transient validation, B2/units/registry).
- **PR-15 white-space gate ✅ (provisional)** — one-sided PASS for W1; final dated re-sweep at S0.8.
- **S0.7-lite ✅** — envelope conditional-positive on frozen PR-10, Critic-audited; **Lucas
  ruled GO** on the continuation gate (E-2026-06-10-3) → S0.2–S0.5 authorized.
- **S0.2-0 ✅** — debt-#2 benchmark recon + task candidates → fed the PR-1/PR-2 freeze.
- **S0.2-1 ✅ CLOSED** — the headline block:
  - **In-house layer = the official computation, proven:** float32-exact parity vs official
    JAX with transplanted weights (max|Δ| 2.4×10⁻⁷ G1 / 2.7×10⁻⁷ G3 full-model, train +
    inference; 1.2–1.5×10⁻⁷ re-verified on GPU); 12/12 unit tests; param counts reconciled
    exactly (published = trainable + BN state); official splits reproduced exactly
    (EigenWorms N=236 after the official dedup — 23 duplicates removed).
  - **G1 Heartbeat: GATE PASS** — gated 5-seed mean **72.9032 % ≥ 72.1** (+0.80 pp;
    −0.78σ_published; sd 3.85 pp); annex mean 75.81 %.
  - **G3 EigenWorms: GATE FAIL as measured** — gated mean **71.1111 %** (2/5 seeds in the
    collapse; healthy-3 = 93.52 %, inside the published band). Frozen miss-rule executed to
    the letter (stop, zero tuning, sanctioned cross-check only).
- **F-G3 (the finding; all citable figures archived + environment-qualified):**
  - The **official code, faithfully rerun** on the 5 published seeds: **90.56 %** — below its
    own frozen gate by one test-sample (163 vs 164/180) — with **σ = 9.34 pp ≈ 2.1× the
    published 4.4** (seeds at 77.78 and 83.33). The transfer premise fails on **dispersion +
    environment sensitivity**, not a 0.04-pp technicality.
  - **Mechanism:** fp32 zero-gradient absorbing state of the published objective
    −Σ y·log(softmax+1e-8) — softmax saturation → p_true underflows to exactly 0 → gradient
    exactly 0 forever; entered at training steps 1–7; an **optimization collapse of the
    published method** (Critic re-derived analytically).
  - **Incidence (per-environment, archived):** ours 2/5 gated (GPU) + 2/3 annex (local CPU);
    official fresh-8 local: 0/8 strict, **1/8 behaviorally collapsed** (22222 chance-frozen);
    **the same seed's trap status flips with the compute environment in both stacks** —
    incidence is itself environment-contingent. Any material incidence voids the criterion.
  - **The port is exonerated:** parity dossier + line-by-line init audit + healthy seeds in
    the published band — all on record before the G3 runs.
- **S0.2-1R ✅** — Critic-mandated record repair: pre-declared, archived local regeneration of
  every console-only figure; results-log corrections (GA-F1/F4/F7). $0.
- **S0.3-0 ✅** — substrate recon + PR-4 input sheet:
  - **Debt #3's premise was FALSE:** the flagship Er:Si₃N₄ amplifier (Liu et al., Science
    376, 1309 (2022)) **did measure its noise figure — NF ≈ 7 dB** (7.1 dB worked example),
    three-way verified. NF menu: NF-A 7.0 (measured) / NF-B 5.0 (host band) / NF-C 3.0
    (quantum floor, aspirational label).
  - **Erbium gain is rigorously quasi-static** at all registered clocks (τ = 3.4 ms [EV];
    per-symbol ripple ≤ 5×10⁻⁷; E_sym/E_sat ≈ 5×10⁻⁶–9×10⁻⁵ with the large-signal check) →
    the **M1-vs-M3 gain-regime fork** (the one open decision, §5).
  - **Gain budget per corner:** loss-compensation closes at P-FND and above; **CORNERSTONE is
    passive-only** (headroom ×0.7–1.3 unloaded).
  - **EV-F3 sharpened:** N=128-in-band exists only at class-leading Q with the splitting knob
    ON — the deployable N-grid is {8, 32} unless that cell is registered.
  - Menus ready for PR-4: cells C-1/C-2/C-3 · ASE conventions A1/A2 · κ_ext policies K1–K4 ·
    splitting policies K-pol-1/2/3 · holding H1/H2/H3 · drive normalization O1/O2/O3.

---

## 4. Spend + infrastructure

- **Cloud:** $1.15 of Lucas's $7.44 vast.ai credits (E-2026-06-10-5; G3 GPU campaign incl.
  the full diagnosis; box destroyed after sync). Everything else local CPU, $0.
- **Code:** `photonic_ssm/` (CMT core, pole region, LinOSS layer/stack/data/train),
  `scripts/` (splits, gate runs, parity), `tests/` (12/12 green), `analysis/` kernels.
  Archived runs: `results/s0_2/gate_i/` (+ `xcheck_official/`, `xcheck_official_local/`),
  `results/s0_3/`. Scratch official venv: `/tmp/linoss_venv` (jax 0.4.28, equinox 0.11.4,
  optax 0.2.2 — the reference pins).

---

## 5. The one open decision — E-2026-06-11-2 (gain-regime fork)

Which gain-model class does the shared S0.3-1 substrate register?

- **M1 — SiN-native static-saturated operating point + ASE + slow drift** (recommended):
  matches the measured Er physics at every registered clock; in-loop physics is **linear**,
  task-solving nonlinearity = readout |·|² (exactly the frozen PR-2 R2 structure); validity
  conditions registered (stationary episodes — satisfied by the frozen tasks; bursty inputs
  void; differentiable operating point; drift at training cadence).
- **M2** — rate equation at τ = 3.4 ms: M1's one-off validation reference only.
- **M3** — rate equation at τ_c ~ 0.1–0.5 ns: the **III-V/SOA fallback platform's** physics;
  recommendation = named but unbuilt in Stage 0 (option (b): a labelled non-gating
  sensitivity row in S0.5/S0.6, at ~2× substrate-matrix cost).

It matters because it fixes what all four estimators face (PAT twin mismatch, adjoint
linearity, what RHEL's echo conjugates, the reservoir contrast). **Awaiting Lucas's ruling.**

---

## 6. The path ahead

1. **Lucas rules E-2026-06-11-2** (M1 / M1+M3-row / M3).
2. **Supervisor drafts PROPOSED PR-4** from the input sheet (verify Cui 2023 [AV]; apply the
   new transfer-check rule's scope clause — physics freeze, no reference implementation, so
   the infeasibility is registered as anchor risk).
3. **Critic phase-boundary review** of PR-4 → **Lucas freezes**.
4. **S0.3-1 (Executor):** build the shared dissipative substrate (finite Q, registered gain
   model, per-round-trip ASE, splitting knob per policy) + coarse BPTT-on-substrate sweep
   (feeds PR-12 damping cell).
5. **PR-3 rule freeze** (before S0.4 close) → **S0.4:** the four estimators (PAT, SPSA,
   recurrent adjoint, RHEL + the concrete χ³ FWM echo sub-model; PR-5–9, PR-11).
6. **S0.5:** the bake-off (primary score: sample-efficiency-to-target under realistic noise).
   **S0.6:** D-LinOSS damping sweep. **S0.7:** full systems-advantage envelope.
   **S0.8:** writeup + the dated novelty re-sweep + debt wording.

## 7. Verification debts

| # | Debt | Status |
|---|---|---|
| 1 | White-space claim (W1) | **Provisional one-sided PASS** (PR-15.1); final sweep at S0.8; NTT/Fisher/Shi full-texts Lucas-paced. |
| 2 | LinOSS/D-LinOSS/Mamba-3 benchmark specifics | **Discharged** (S0.2-0) — and F-G3 now adds first-hand evidence on the LinOSS headline number's stability. |
| 3 | Er:Si₃N₄ noise figure | **Resolved — premise false:** the flagship *did* measure NF ≈ 7 dB. Reword at S0.8 (the sharpened form is in the S0.3-0 memo §1a). |
| 4 | Recurrent-adjoint gap (inferred from absence) | **Outstanding** — same inferred-absence type that just burned us at G3; re-verify at first full-text contact. |

## 8. Coordination state

- **Supervisor (this session):** active — next output is PROPOSED PR-4, on Lucas's fork ruling.
- **Executor:** idle, no task posted. Next task = S0.3-1 (post-PR-4-freeze).
- **Critic:** idle. Next engagement = the PR-4 phase-boundary review.
- Standing non-blocking: optional courtesy report to the LinOSS authors (Lucas-paced, **not
  before the S0.8 wording freeze**); F5 primary-source pass (S0.L); debt-#4 full-text check.

```bash
# Executor session:
cd ~/Documents/Project_SSM && claude "Read shared/launch_executor.md and follow it."
# Critic session:
cd ~/Documents/Project_SSM && claude "Read shared/critic_instructions.md, then review the target it names."
```
