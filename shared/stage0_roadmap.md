# Stage 0 Roadmap — Theory + Simulation (incl. the four-method training bake-off)

**Owner:** Supervisor. **Status:** **v3 (2026-06-08)** — Critic review (`critic_review_stage0-roadmap.md`,
APPROVE-WITH-EDITS) folded in; **Lucas signed off 2026-06-08** ("accept all, scope (B) blessed").
**Source of truth:** `photonic-ssm-proposal-v0_5.md` §6 (Stage 0), §3 (mapping), §4 (pole region),
§5 (training), §7 (gain), §10 (advantage). This roadmap decomposes Stage 0 into executable phases; it
adds no scope beyond the proposal without a decision logged in `decisions_needed.md`.
**Companion file:** `preregistration.md` — every tunable margin/gate/cell/budget freezes there *before*
its run (Critic F12). PR-IDs below point into it.

> **v0.5 reframing (vs the v0.2 plan this file replaced).** Platform is **silicon nitride (SiN)**, not
> TFLN. Training is a **four-method bake-off** — SPSA, PAT, recurrent in-situ adjoint, RHEL — on **one
> shared dissipative ring model**, with **PAT/SPSA the hardware-committed primary** and the two exact
> methods evaluated *in simulation only* ("parallel in simulation, singular in hardware"). The primary
> score is **sample-efficiency-to-target-accuracy under realistic noise**; gradient-cosine-error is a
> **secondary diagnostic only**. Damping is now a **free knob** (no conservatism tension). A
> **systems-advantage envelope** is an explicit deliverable.

> **v3 changelog — what the Critic review folded in (all Lucas-approved 2026-06-08).**
> **F17** S0.0 rewritten to the actual selective-salvage manifest (the "fork ring model + training engine"
> text was stale — the recon found that code static/CW + MZI-structural; ✅ done). · **F1** an early
> **S0.7-lite** envelope runs before the S0.2 task choice (task-selection input). · **F2** S0.2 pins the
> task + hybrid architecture + trainable-parameter partition + actuation map, and the bake-off scores
> **relative to the BPTT-on-substrate ceiling**. · **F3** a coarse damping sweep moves to S0.3-close. ·
> **F5/F6** cost unit = physical device passes (any direction) + digital side-ledger; secondary diagnostic
> = bias/variance vs BPTT (not raw cosine). · **F7 (CRITICAL)** an estimator **fairness contract** +
> PAT twin-mismatch protocol before S0.4. · **F8** per-method hardware-requirements ledger at S0.4. ·
> **F9** RHEL echo irreversibility invariants + unit test. · **F10** Gate ii decomposed (capacity vs
> trainability) + escalate corner + quantified promotion + "exactness" struck. · **F11** ≥8 seeds all
> methods (headline) + censored statistics. · **F13** foundry-grade $Q$ gates, class-leading sweeps
> (resolves D-2026-06-08-1). · **F14** debts #2/#3 are critical-path (front-loaded). · **F15** named
> white-space search queries. · **F16** S0.7 content floor. · **F18** architecture constraints promoted
> to S0.3/S0.4 gates. · **F19** backscatter/mode-splitting bound (S0.1) + optional knob (S0.3). · **F20**
> synthetic memory-task secondary. · **F21** compute sizing. · **F22** pre-draft both RHEL conclusions.

> **v3.1 changelog (2026-06-09, Lucas "ok go" — three resolutions folded in).**
> **D-2026-06-08-2 resolved:** the simulated layer is the **diagonal complex-pole SSM (S4D/DSS class)** —
> one ring = one complex pole; LinOSS is its uncoupled + real-I/O conjugate-pair special case; trainable
> inter-ring μ is a mild generalization beyond diagonal-A LinOSS; "oscillatory LinOSS" branding softened;
> benchmark transfer = **debt #2** (validated via the PR-3 BPTT-on-substrate ceiling); **readout pinned at
> PR-2** (coherent-quadrature vs intensity, + the F6 κ_ext dual-role). · **D-2026-06-08-3 resolved:** S0.3
> carries the **roughness-gated CW/CCW splitting knob**, default **ON except the clean-damascene corner**;
> PR-4 gains a roughness/splitting sub-parameter, evaluated at the **operating κ_ext**, resolved jointly
> with D-2026-06-08-1; B2 numbers provisional until F5 (S0.L). · **D-2026-06-09-1 adopted:** verification
> **debt #1 is front-loaded** — the white-space existence search runs **now, pre-S0.2**, under frozen
> **PR-15** (rule-form kill-criterion q1∧q2∧q3; two-modality Executor+Critic protocol; one-sided PASS);
> S0.2–S0.5 authorization sits behind a **pre-S0.2 continuation gate** = PR-15 verdict + S0.7-lite
> envelope + **Lucas's program-level call** (the "first" is collectible only at Stage 1+; Stage 0 alone =
> methods paper — E-2026-06-09-2). Wording refinement stays at PR-2/S0.8; the dated S0.8 sweep stays.

> **v3.2 changelog (2026-07-05, Supervisor doc-hygiene under Critic P6-F9 + Lucas "ok go").** All
> PR-12 mentions reworded to the **R-ii disposition** (PR-12 PROPOSED v2, 2026-06-17): D-LinOSS
> damping is a **trainable per-ring net-loss knob via κ_ext at the fixed §G operating point
> g_f = 0.9** — *not* a frozen "central damping cell." The S0.3-close coarse sweep swept the wrong
> axis (g_f *is* PR-4 §G's registered operating point) and is **re-run convergence-controlled
> (≥8 seeds) at S0.4** over the PR-6 §C/§D clamped box. No scope change — this aligns the roadmap
> with `preregistration.md` PR-12.

## Goal of Stage 0

Produce, with **no fabrication**, the deliverables that gate the program:
1. an oscillator↔SiN-ring **mapping** result + realizable pole-region bound (+ the in-situ-trainable
   parameter/actuation map, the backscatter bound, and the memory-vs-readout-SNR trade);
2. **a comparison of in-situ training methods** (the bake-off) for an oscillatory photonic recurrence
   under realistic loss/gain/ASE — publishable in its own right, and the RHEL-on-SiN finding;
3. the **damping/accuracy curve** (D-LinOSS operating point);
4. a **systems-advantage envelope** (an early **S0.7-lite** that informs the task choice, then the full
   latency/energy budget incl. E/O–O/E + DAC/ADC overhead vs a strong digital baseline).

And clear the two gates:
- **Gate (i):** model reproduces oscillatory-SSM task accuracy within a **pre-registered margin** (PR-1).
- **Gate (ii):** decomposed (F10) — **(ii-a) capacity:** the BPTT-on-substrate ceiling at the registered
  realistic-noise cell clears the absolute task-utility floor; **(ii-b) trainability:** **PAT or SPSA**
  reaches within the pre-registered margin of that ceiling. *If only adjoint/RHEL reach target while both
  PAT and SPSA fail → Gate ii **fails its hardware purpose → escalate to Lucas** (not an auto-pass).*
  Promote adjoint/RHEL to a hardware slot **only if** it *clearly beats* PAT/SPSA on a quantified outcome
  metric (PR-9) — "exactness" alone is **not** a promotion axis.

## Phase decomposition

> Ordered by dependency. Each is a `task_queue.md` task gated by a Critic review of its **results** before
> dependents start. Seeds: 4 min for exploratory grid scoping, **≥8 for all methods in headline cells**
> (F11). The four estimators **share one substrate model** (S0.3) under one **fairness contract** (PR-6)
> so the comparison is apples-to-apples.

### S0.0 — Repo + selective salvage + smoke test ✅ DONE (2026-06-08)
- **Did:** stood up the Project_SSM repo under git; **selectively salvaged** the 7-asset manifest
  (`tooling_recon.md` §4 — SPSA + pass-accounting, gain/ASE, rate-equation dynamic-gain SOA, SiN registry,
  static Lorentzians as CW-limit test refs + drift, ridge readout, sweep/JSONL scaffold) with provenance
  headers + ported tests; baked in the two architecture constraints. **The SSM core is new code** (recon:
  ring physics is static/CW, training engine MZI-structural — *not liftable*).
- **Delivered:** runnable repo (60/60 tests); **salvage-validation** smoke test (salvaged Lorentzian ==
  analytic add-drop in the κ₂→0 limit; FSR self-consistency; SPSA FD-vs-autograd anchor RMS 1.1e-7).
- **Gate:** ✅ all passed. *(The dynamical single-ring→pole test is **S0.1's** gate, not S0.0's.)* Results:
  `results_log.md`.

### S0.1 — Oscillator↔SiN-ring mapping + realizable pole region  *(scope (B), Lucas-blessed 2026-06-08)*
- **Do:** formalize proposal §3 (ring pole $s=-\kappa_\text{tot}+i\omega_\text{res}$ ↔ eigenvalue
  $a_i=-e^{\alpha_i}+i\beta_i$); implement a **dynamical** coupled-ring → $N$-oscillator LinOSS forward
  model (temporal CMT, **not** the salvaged static/CW transfer function); bound the pole region per §4
  (stability free; **memory loss-limited**; FSR-bounded $\beta_i$; poles placed by drift-stable
  thermo-optic trim). **Plus the three scope-(B) deliverables:**
  - **(B1) trainable-parameter set + actuation map** — which physical parameters are in-situ-trainable
    and by what actuator: detunings $\beta_i$ (heaters); pole *real* parts (tunable bus–ring coupling,
    e.g. MZI-assisted couplers, and/or per-ring gain); inter-ring coupling topology (direct
    photonic-molecule vs bus-mediated). The white-space sentence's wording depends on this (→ PR-2).
  - **(B2 / F19) backscatter / CW–CCW mode-splitting bound** — literature-sourced: where surface-roughness
    backscatter splits a resonance into a doublet (splitting rate vs $\kappa_\text{tot}$) across the
    registered $Q$ range; flag where "one ring = one complex pole" breaks down (negligible at foundry
    $Q\approx2\times10^6$; *not* at the aspirational $10^7$). Sets whether S0.3 needs a splitting knob.
  - **(B3 / F13.3) memory-vs-readout-SNR ($\kappa_\text{ext}$) trade** — show it explicitly: deep
    undercoupling maximizes memory but collapses I/O residues + detector SNR; the realizable region is
    set by the $\kappa_\text{ext}$ policy (→ PR-4).
- **Also (F13.1):** fix the salvaged registry's Q/loss inconsistency — register one of $(\alpha,Q_i)$ as
  primary, derive the other, add a **loss↔Q self-consistency test** alongside the FSR check.
- **Deliverable:** mapping write-up (Supervisor) + verified dynamical forward model (Executor) + plotted
  pole region with the loss/gain → $|\lambda|$ (memory-length) relation; (B1)/(B2)/(B3) memos. Feeds the
  S0.2 task sizing (PR-2) and the S0.3 $Q$/$\kappa_\text{ext}$ registration (PR-4).
- **Gate:** dynamical model poles match a coupled-mode/transfer-function reference within tolerance (incl.
  the CW limit recovering the S0.0 static reference).

### S0.2 — LinOSS / D-LinOSS digital baseline (Gate i) + bake-off setup
- **Precondition — the continuation gate (D-2026-06-09-1):** S0.2 (and the S0.2–S0.5 chain, S0.3
  included) is authorized only after the **PR-15 white-space verdict** + the **S0.7-lite envelope** are in
  and **Lucas makes the program-level continuation call** (E-2026-06-09-2).
  **✅ SATISFIED 2026-06-10 — Lucas ruled GO (E-2026-06-10-3):** PR-15.1 provisional one-sided PASS +
  Critic-audited conditional-positive lite envelope (APPROVE-WITH-EDITS, verdict survives). S0.2 runs as
  **S0.2-0** (debt-#2 recon + task/benchmark candidates — feeds the freeze) → **PR-1/PR-2 freeze (Lucas)**
  → **S0.2-1** (implementation + the Gate-i run), mirroring the S0.7L-0→PR-10→S0.7L-1 pattern.
  **Status: S0.2-0 ✅ (2026-06-10) → PR-1/PR-2 (+PR-13 early) 🔒 FROZEN 2026-06-10** (Critic-reviewed v2 —
  AMEND→fix applied: R2-intensity headline readout, PF-F1; Lucas "ok go", E-2026-06-10-4) → **S0.2-1
  ✅ CLOSED 2026-06-11**: **G1 Heartbeat PASS** (72.9032 ≥ 72.1, Supervisor-verified; in-house layer
  float32-exact vs official) · **G3 EigenWorms FAIL on record** — the published anchor itself fails a
  faithful official-code rerun (F-G3: 90.56 %, σ 9.34 = 2.1× published, + fp32 optimization collapse) →
  **PR-1.1 v2 🔒 SIGNED by Lucas** (Critic-reviewed; S0.2-1R archived record repair): G3 criterion **void
  for anchor instability**, **Gate i adjudicated purpose-served** (G1 PASS ∧ numerical-identity parity
  dossier); downstream anchors on the **PR-3 in-house BPTT ceiling** as registered; F-G3 binds S0.8
  wording; transfer-check freeze rule now binding.
- **Do:** implement LinOSS (stable for nonnegative-diagonal $A$) + D-LinOSS (learnable damping); reproduce
  a long-range / time-series benchmark within a **pre-registered margin** (PR-1) set *before* the run.
  Resolve verification debt **#2** here (its S0.L memo is a *prerequisite* — F14; sharpened by D-08-2:
  published LinOSS results validate only the μ=0 diagonal reduction). **Pin the bake-off**
  (F2, → PR-2): the **task** (sized against S0.1's pole/memory bound + the S0.7-lite niche), the **hybrid
  architecture** — *resolved D-2026-06-08-2:* the **complex-diagonal (S4D/DSS) layer**, LinOSS as its
  special case; **pin the readout** (coherent-quadrature vs intensity) + the F6 κ_ext dual-role — the
  **trainable-parameter partition** (every estimator trains the *same* partition), and the **actuation
  map** from S0.1 (B1).
- **Deliverable:** baseline accuracy table + the pre-registered margin + the pinned bake-off task/arch.
- **Gate (= Gate i):** idealized oscillatory-SSM accuracy within the pre-registered margin (PR-1).

### S0.3 — Shared realistic dissipative ring substrate model
> **Status 2026-06-13: S0.3-0 ✅ DONE · PR-4 🔒 SIGNED v2 · S0.3-1 build ✅ ACCEPTED (F18 gate PASS, Supervisor-verified 9/9).** Frozen substrate (PR-4 v2 in the ledger): gain class **M1** at operating point **g_rt = 0.9× intrinsic** per cell (E-2026-06-11-2: M1 + M2 ×2-cell validation + M3 pre-committed trigger); **A2 Langevin ASE** (A1↔A2 unit test); **K4** trainable κ_ext r∈[0.1,3], θ₀=0.3; **K-pol-3** splitting knob always ON; cells **C-1 P-FND/N=8 (Gate ii @ 2 GS/s)**, **C-2 P-AN800/N=32 (bake-off headline; Cui anchor body-[EV])**, **C-3 P-UHQ/N=128 (aspirational)**; **NF-A 7.0** headline; **H1** holding; **O2** intracavity-energy budget @ P̄₀=1 mW (E₀ numeric addendum pasted 2026-06-13: C-1 3.14e7 / C-2 1.07e8 / C-3 4.72e8 photons; reachability — C-1 material-aspirational, C-2 reachable iff Er≥1.5 dB/cm). Substrate `photonic_ssm/substrate/`; 9/9 tests. Critic review verdict AMEND → all P4-F1..F12 folded into v2.
> **Critic 2026-06-13: APPROVE-WITH-EDITS** (`critic_review_s0_3_1.md`, re-run 9/9). S-F1 **confirmed HIGH** (dropped ∂g/∂κ_ext = 27% of κ_net at θ₀, 6× + sign-flipped at the trainable edge); fix conforms code to the signed freeze (no freeze change). **Open before S0.4a:** (1) **S0.3-1b ACTIVE** — freeze-conforming Executor edits (flip gain default `fixed`→`saturating`, harden test_h, surface intracavity reachability, rewrite the hygiene gate to test the source-stack invariant, register ASE-detach). (2) **Lucas CONFIRM** saturating is the bake-off mode for all four estimators (→PR-6) + **RECONCILE PR-4 §G ↔ PR-12** (the sweep's g_f axis *is* the registered operating point; PR-12 = subsumed, or a distinct D-LinOSS-damping knob at fixed g_f=0.9? — lean latter). (3) **PR-12 deferred** — convergence-controlled rerun + 8 seeds after the reconcile. (4) **PR-6** must register the **connected init** (μ(0)=0 signal-starves rings 2..N → N=32 untrainable from cold) + the sweep recipe. **S31-F3:** on the operative intracavity plane *all* gain cells are material-aspirational (≈380 dB/cm req vs Er ≤1.9) — anchor-risk (v) strengthened; ledger addendum corrected. **PR-6/5/7 freeze before S0.4a.**
- **Do:** build the **single substrate** all four estimators train through: finite $Q$ / round-trip loss,
  erbium (or III-V) gain saturation, **injected ASE** (per-round-trip, inside the rollout — new physics
  the recon flagged). Conservative NF (debt **#3** front-loaded — F14; its sourced NF bracket is a
  prerequisite of the ASE knob). Parametric in loss/gain/ASE. **Register** the self-consistent
  $(\alpha,Q_i)$ pair + $\kappa_\text{ext}$ policy + the realistic-noise cell (PR-4; **foundry-grade is
  the Gate-ii cell**, class-leading a labelled aspirational sweep). Carry an **optional mode-splitting
  knob** iff S0.1's bound (B2) says it bites in-range (F19). **Coarse damping sweep at close** (F3): train
  the BPTT-on-substrate reference at each damping point → register the central operating cell (PR-12).
  *[Superseded by PR-12 R-ii (2026-06-17, v3.2): the sweep ran but parametrized the wrong axis (g_f =
  the §G operating point); no cell was frozen from it — the convergence-controlled re-run happens at
  S0.4 on the κ_ext axis.]*
  **Compute sizing** (F21): aggregate order-of-magnitude estimate before substrate fidelity is fixed;
  escalate to Lucas if it implies cluster spend.
- **Deliverable:** documented substrate with named, cited parameter ranges; unit tests (zero-noise limit
  recovers the S0.1 forward model); the coarse damping curve; the compute estimate.
- **Gate (F18):** substrate reproduces expected limits; one knob each for loss/gain/ASE variance; **full
  state trajectories exposed in the API**; **the BPTT reference trains through the substrate end-to-end
  (gradient flow verified)** — the operational test that the `no_grad`/detach anti-pattern was avoided.

### S0.4 — Implement the four in-situ-training estimators (on the shared substrate)
**Before S0.4a starts, freeze the fairness contract (PR-6, CRITICAL) + the PAT twin-mismatch protocol
(PR-5) + the cost-accounting conventions (PR-7).** Sub-phases (RHEL split out for its echo cost):
- **S0.4a — PAT + SPSA (the hardware-committed workhorses).** SPSA: gradient of all params from **two
  physical forward passes**, model-free; verify it absorbs injected noise + crosstalk. PAT: forward on the
  substrate (unrolled, gradient flows through state), backward on a differentiable digital **twin** — and
  **the twin must differ from the substrate by the pre-registered mismatch (PR-5)**; report PAT as a
  *function* of mismatch level (headline = registered level). The **offline-train-deploy baseline's
  weight-mapping error is drawn from the same calibration-error family** as PAT's twin mismatch (F7.3).
- **S0.4b — Recurrent in-situ photonic adjoint.** Time-domain/cavity extension of the feedforward adjoint
  (Hughes/Fan/Pai lineage); the **adjoint backward pass is a *physical* device pass through the same
  noisy dissipative substrate** (fresh noise) — *not* autodiff-through-the-substrate (that is the BPTT
  reference only). Solve adjoint-field interaction with gain + non-reciprocity.
- **S0.4c — RHEL + concrete optical-echo sub-model.** Implement RHEL on the LinOSS oscillator **and** the
  echo's physical primitive honestly: a **specific χ³ FWM phase-conjugation scheme** with real
  pump-power / bandwidth / conversion-efficiency / added-noise penalties (note the **resonant-enhancement
  ↔ bandwidth tension**: enhancement buys FWM efficiency in low-$n_2$ SiN but narrows the band the N-ring
  spectrum needs) — or an explicit **off-chip / non-SiN admission** (which must then *say so*, incl. the
  field storage/timing primitive). **No idealized conjugation operator.** Bake in the **irreversibility
  invariants + unit test (PR-11):** independent forward/echo ASE streams (no common-RNG reversal); no
  loss-sign flip (echo through the same dissipative substrate); gain injects fresh ASE in the echo too;
  *the echo of a noisy forward must not recover the noiseless state* (bounded by conjugation-fidelity ×
  ASE floor). RHEL-on-SiN is framed "odds-improved, not feasibility-reopened" (§5.2).
- **At S0.4 close:** **measure + freeze the BPTT-on-substrate ceiling** at the registered cell (PR-3, the
  bake-off's reference); produce the **per-method hardware-requirements ledger** (observables, actuators,
  added components + their loss, calibration burden — F8, feeds Gate-ii hardware-simplicity + Stage-1);
  **pre-draft both RHEL conclusion templates** (competitive / fails-under-honest-echo — F22).
- **Gate:** each estimator runs on the shared substrate; idealized/zero-noise floor checks pass (adjoint &
  RHEL → BPTT in the relevant limit — a **floor check, not the headline**); the fairness contract is
  audited per estimator.

### S0.5 — The bake-off (the headline Stage-0 result + Gate ii)
- **Do:** run all four estimators **+ the baselines** (offline-train-deploy; reservoir-readout, §5.3) on
  the shared substrate as loss/gain/ASE are swept, at the registered realistic-noise cell (PR-4);
  damping is **not a frozen cell** but the trainable κ_ext-axis knob of PR-12 R-ii, exercised over the
  PR-6 §C/§D clamped box (v3.2 reword). **Primary metric: sample-efficiency-to-target-accuracy** — passes-to-reach
  **within the pre-registered margin of the BPTT-on-substrate ceiling** (PR-3), cost in **physical device
  passes, any direction** (PR-7), under the **statistical plan (PR-8)**: right-censoring treatment,
  lexicographic ranking (success-fraction then median passes), paired-by-seed bootstrap CIs, **≥8 seeds
  all methods**. Also run the **synthetic memory-task secondary** (PR-13). **Secondary diagnostic only:**
  the **bias/variance decomposition of the gradient estimate vs the BPTT reference** (PR-14) — *never the
  headline* (it flatters exact methods + penalizes SPSA in *both* directions).
- **Deliverable:** the in-situ-training-method comparison under realistic loss/gain/ASE, incl. the
  concrete RHEL-on-SiN finding (whichever pre-drafted template the metric selects).
- **Gate (= Gate ii, F10/PR-9):** **(ii-a)** BPTT ceiling clears the utility floor; **(ii-b)** PAT or SPSA
  within margin of ceiling. **Only-adjoint/RHEL-pass → escalate-and-redesign.** Promotion of adjoint/RHEL
  toward a *later* hardware slot requires *clearly beats* on a **quantified** outcome metric (e.g. ≥X%
  better pass-to-target with non-overlapping 95% CIs, or strictly-better scaling over the swept range, or
  a strictly-simpler hardware ledger at non-inferior efficiency) — **"exactness" is struck** from the menu.
  *If SPSA variance is prohibitive at the target parameter count → lean on PAT, reserve SPSA for
  fine-tuning (risk #2).*

### S0.6 — Damping operating point (D-LinOSS)
- **Do:** *(reworded v3.2 per PR-12 R-ii — the S0.3-close coarse sweep froze no cell; it swept the
  wrong axis.)* Damping is the **trainable per-ring net loss via κ_ext at fixed g_f = 0.9** (PR-12
  v2); here, flesh out the full damping/accuracy curve from the convergence-controlled ≥8-seed re-run
  over the PR-6 §C clamped box (or merge into the S0.5 sweep analysis). The sweep is over the
  physical damping **floor** (loss–gain operating point) + any damping init/range — **not** a fixed value
  (D-LinOSS damping is trainable). The v0.2 "conservatism–damping frontier" is retired.
- **Deliverable:** the damping/accuracy curve + a recommended operating point.
- **Gate:** a defensible operating point identified (or a documented "damping-insensitive" result).

### S0.7 — Systems-advantage envelope (§10 deliverable) — **lite (early) + full**
- **S0.7-lite (runs now, ∥ the PR-15 search; due *before* the S0.2 task choice — F1; feeds the
  pre-S0.2 continuation gate — D-09-1):** assumption-driven, no new code,
  parametric in memory length where S0.1 numbers don't exist yet. Pre-register its assumptions (PR-10:
  conversion energies, DAC/ADC rates, named digital-baseline class + sources, operating scale). **Output
  identifies the plausible low-latency niche → input to the S0.2 task choice** (so the bake-off isn't
  benchmarked on a task irrelevant to the claimed niche). Handle both outcomes honestly: a negative lite
  envelope → escalate as a *Stage-1-reframing* finding (it does **not** kill Stage 0 — §10: the science
  stands without a systems advantage); a positive one stays labelled assumption-driven, **not** load-
  bearing in outreach until the full S0.7.
- **S0.7-full (after S0.5):** the end-to-end latency/energy budget. **Content floor (F16):** a **strong
  digital baseline** (tuned FPGA/ASIC or embedded-GPU at matched accuracy — named sources; *not* an
  unoptimized GPU); a **full power ledger** (thermo-optic *holding* power × N heaters, control
  electronics, active locking — *plus* E/O–O/E + DAC/ADC); a **precision–accuracy link** (detector-state
  SNR from the S0.3 noise model → achievable task accuracy); the operating scale (N rings, rates) stated.
- **Gate:** envelope exists and states whether an advantage window plausibly exists. **If even the
  optimistic envelope fails to clear digital, that is a pre-MPW-spend finding → escalate** (§10).

### S0.8 — Write-up
- **Do:** Supervisor assembles the Stage-0 outputs: mapping result (+ B1/B2/B3) + bake-off comparison +
  damping curve + advantage envelope. Resolve the framing of debts **#1** (sharpened white-space) + **#4**
  (recurrent-adjoint gap). Reconcile the proposal §6 "exactness" wording with the struck promotion axis
  (F10.3). Frame PAT/SPSA novelty as the **recurrent dissipative setting** (not re-validating chip-proven
  methods — F22). **Limits-of-model section (F19):** state that the bake-off measures robustness to
  *modelled* imperfections only — unmodelled physics (thermal transients, polarization, fab variation of
  coupling gaps, mode-splitting if un-knobbed) could reorder methods on hardware.
- **Deliverable:** arxiv-ready Stage-0 manuscript(s); the finding to take to a potential collaborator.

### S0.L — (parallel) Literature / verification-debt track
- **Do:** re-verify the four debts against primary sources, dated memos with citations. **#2 and #3 are
  critical-path (F14):** **#2** (LinOSS/D-LinOSS/Mamba-3 specifics) feeds **S0.2**; **#3** (Er:Si₃N₄ NF)
  feeds **S0.3**. **#1 is front-loaded pre-S0.2** (D-2026-06-09-1 — kill-shot first; existence search
  under frozen **PR-15**, feeding the continuation gate; F14's data-dependency pacing stands for #2/#3 —
  the two lenses are compatible). **#4** stays S0.8-paced.
  1. **white-space** — sharpened form: *recurrent parameters (pole positions + inter-ring couplings)
     updated on the physical device by gradient-based/-estimating training, never done.* Pre-empt:
     reservoir computing; the Bueno/Brunner photonic-RNN RL line; internal-param reservoir variants.
     **Named search queries that could actually kill the claim (F15):** (i) zeroth-order/perturbative
     (SPSA/FD) updates of *internal* params of any recurrent photonic system (a single such prior is
     fatal); (ii) REINFORCE/policy-gradient updates of *internal* recurrent params (reward-*gradient* is
     gradient-estimating — pre-draft the boundary vs the Bueno/Brunner readout-only line); (iii)
     hardware-in-the-loop adaptation of delay-reservoir *feedback/internal* params; (iv)
     evolutionary/Boolean-search internal-weight training (claim survives via "gradient-based/-estimating"
     — say so explicitly). Date the search (mid-2026 snapshot).
     **Operationalized (D-09-1, PR-15 🔒 FROZEN 2026-06-09):** existence search runs **now** —
     two-modality (Executor systematic sweep, primary-source-verified — the B2/F5 lesson — + independent
     Critic adversarial pass); FATAL iff *internal-to-recurrence* ∧ *on-device-in-the-loop* ∧
     *gradient-based/-estimating* (lanes locate, the rule decides); (iv)-type priors non-fatal but cited;
     ambiguous → Lucas; **PASS is one-sided** — the dated S0.8 sweep + wording refinement stay.
  2. **LinOSS / D-LinOSS / Mamba-3** benchmark specifics → S0.2.
  3. **Er:Si₃N₄ noise figure** (flagship device unmeasured) → S0.3 ASE knob.
  4. **recurrent-adjoint gap** (inferred from absence of demonstrations; confirm) → S0.8.
- **Deliverable:** one short memo per debt; #2/#3 before their consuming phases, #1/#4 feed S0.8.

## Dependency graph
```
                     ┌─▶ PR-15 white-space search (debt #1 — D-09-1) ─┐
S0.0 ✅ ─▶ S0.1 ✅ ──┤                                                ├─▶ ⟦pre-S0.2 continuation gate:
                     └─▶ S0.7-lite (PR-10 freeze → run; F1) ──────────┘    PR-15 + lite envelope + Lucas⟧
                                                                                      │
                                             ┌────────────────────────────────────────┘
                                             ├─▶ S0.2 ── Gate i ──┐  (Gate i = spend gate before S0.4/S0.5)
                                             └─▶ S0.3 ────────────┴─▶ S0.4{a,b,c} ─▶ S0.5 ── Gate ii ──▶ S0.6 ─▶ S0.7-full ─▶ S0.8
                                                 (S0.3 ∥ S0.2 — F4; needs S0.1's model, not Gate i's outcome)

S0.L (literature): debt #1 → pre-S0.2 (PR-15, front-loaded) · debt #2 → S0.2 · debt #3 → S0.3 (critical-path) · debt #4 → S0.8
```

## Pre-registration (freeze before the governing run — see `preregistration.md`)
- **pre-S0.2 (continuation gate):** **PR-15** (white-space existence gate — 🔒 **FROZEN 2026-06-09**),
  PR-10 (S0.7-lite assumptions — freeze *before* the lite run).
- **S0.2:** PR-1 (Gate-i margin + benchmark), PR-2 (task + architecture + parameter partition + actuation;
  carries the blessed D-08-2/D-08-3 constraints — see ledger Notes). **Both 🔒 FROZEN 2026-06-10**
  (Critic-reviewed v2; Lucas E-2026-06-10-4; PR-13 frozen early in the same act).
- **S0.3:** PR-4 ($(\alpha,Q_i)$ pair + $\kappa_\text{ext}$ + noise cell — 🔒 **SIGNED v2 2026-06-13**);
  PR-12 reframed by **R-ii** (⬜ PROPOSED v2 2026-06-17 — damping = trainable κ_ext-axis knob at fixed
  g_f=0.9; the "damping cell at close" framing is superseded, v3.2).
- **S0.4:** PR-5 (PAT twin-mismatch), PR-6 (fairness contract, CRITICAL), PR-7 (cost accounting), PR-3
  (BPTT ceiling rule before close; ceiling frozen at close), PR-11 (RHEL echo invariants).
- **S0.5:** PR-8 (statistics + seeds), PR-9 (Gate-ii semantics + promotion), PR-13 (secondary task), PR-14
  (secondary diagnostic).

## Decision gates owned by Lucas
- ✅ Approved this roadmap (v3) + scope (B) — 2026-06-08. Each **pre-registered value** (PR-IDs) still
  comes to Lucas at its phase boundary before the run that tests it.
- ✅ Adopted v3.1 ("ok go", 2026-06-09): D-08-2 (S4D/DSS framing) + D-08-3 (roughness-gated knob) +
  D-09-1 (debt-#1 front-load, PR-15 frozen).
- ✅ **Pre-S0.2 continuation gate → GO (2026-06-10, E-2026-06-10-3):** with the PR-15 verdict
  (provisional one-sided PASS under signed PR-15.1) + the Critic-audited conditional-positive S0.7-lite
  envelope in hand, **Lucas authorized S0.2–S0.5**. Standing frame unchanged: the "first" is collectible
  only on hardware (Stage 1+); Stage 0 alone yields a methods/feasibility paper.
- ✅ **PR-1/PR-2 freeze → signed ("ok go", 2026-06-10, E-2026-06-10-4):** the Critic-reviewed v2 blocks
  (PR-2 amended per PF-F1: R2-intensity headline readout) + PR-13 early. Gate i + the bake-off object are
  now fully governed; S0.2-1 runs under them.
- The parked $Q$ choice (D-2026-06-08-1) → adjudicated by F13: foundry-grade gates, class-leading sweeps;
  formalized at PR-4.
- Gate (ii) outcome → proceed to Stage 1 on **PAT/SPSA**; whether to reserve a *later* hardware slot for
  adjoint/RHEL (only on a quantified clearly-beats — PR-9).
- The S0.7 advantage-envelope verdict (lite *and* full) → whether the §10 premise justifies MPW spend
  (fallbacks §5.3: offline-deploy, reservoir-readout).
- Compute sizing (S0.3/S0.4) → any cluster spend escalates.
