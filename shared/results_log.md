# Results Log

The **Executor** appends experiment results here (newest at top). The **Supervisor** reads and
evaluates them, then assigns the next task. The **Critic** reads this file to check claims against data.

Per result, report:
- **Phase / task** and **date**
- **Goal** — what this run tested
- **Config** — grid size, key parameters, seed count
- **Key findings** — numbered, with specific numbers
- **Gates** — passed / failed (vs the pre-registered criterion)
- **Anomalies / concerns** — anything surprising or fragile
- **Data path** — where the raw results live
- **Compute used** — where it ran, wall-clock, cost (if cloud)

---

## S0.1 — Oscillator↔SiN-ring mapping + realizable pole region (2026-06-08, Executor)

**Goal:** build the first **new dynamical core** — the temporal-CMT single-ring model + the coupled-ring
→ N-oscillator LinOSS forward model (not the salvaged static/CW transfer); bound the realizable pole
region (§4); deliver the three scope-(B) results (B1 actuation map, B2 backscatter bound, B3 κ_ext
trade) + the F13.1 registry Q/loss fix. *Model + plots + data only; the formal mapping write-up +
white-space wording are the Supervisor's.*

**Config:** local CPU, python 3.12, torch 2.11.0, float64. New package `photonic_ssm/dynamics/`
(torch-only, hygiene test extended over it). 99 tests (60 from S0.0 + **39 new**). Figures/data via
`analysis/s0_1_pole_region.py` (matplotlib, outside the package).

**Key findings / deliverables:**
1. **Dynamical single-ring temporal-CMT model** (`dynamics/single_ring.py`):
   `da/dt = (iΔ − κ_tot)a + √(2κ_ext)·s_in`, pole `s = −κ_tot + iΔ`, identified with `a_i = −e^{α_i}+iβ_i`
   (`e^{α_i}=κ_tot`, `β_i=Δ`). All-pass + add-drop ports; energy-conserving (lossless `|t|=1`; add-drop
   `|t_t|²+|t_d|²=1` to 1e-16).
2. **CW-limit GATE — PASSED.** Pre-registered: CW limit recovers the S0.0 salvaged statics with
   **O(1/finesse)** error, <1% at finesse ≥1000. Measured: single-bus **4.5e-4 @ F=1048 → 4.4e-5 @
   F=10473** (exact 10×/decade); add-drop through+drop **3.4e-4 → 3.4e-5**. CMT through `= −`salvaged
   single-bus (the documented −1 phase convention). SiN rings sit at F≈1000 (Qi=2e6) → 15000 (Qi=3e7).
3. **Coupled-ring → N-oscillator LinOSS forward model** (`dynamics/coupled_rings.py`,
   `CoupledRingLinOSS`): `M = diag(−κ_tot+iδ) + iΩ`; recurrent params `{log_kappa_tot, delta, mu}`
   (= the trainable recurrence). ZOH van-Loan matrix-exp discretization is **exact** for PWC input
   (discrete poles `= e^{λ dt}` to machine precision); uncoupled poles match `−κ_tot+iδ` <1e-3.
   **Both architecture constraints honored in the NEW model (not inherited):**
   **(3a)** a last-step loss receives gradient through the ring state from the t=0 input (49 steps back),
   all recurrent-param grads finite; the rollout uses no `no_grad`/`detach` (source-grep test).
   **(3b)** `forward` returns the full trajectory x₀..x_T. Gradient-**checkpointed** chunked rollout
   (the `TrainingAwareDynamicSOAPerMode` pattern) is **bit-identical** to the plain rollout in outputs,
   states, AND all gradients (0.0).
4. **Realizable pole region (§4)** (`dynamics/pole_region.py` + `results/s0_1/pole_region_memory.png`):
   stability free; memory **loss-limited** — passive amplitude memory **1.65 ns / 329 round trips**
   (Qi=2e6) → **24.7 ns / 4937 round trips** (Qi=3e7), a **15× gain**; gain pushes `|λ|→1` (plotted at
   net gain 0/50/90 % of loss); `β` FSR-bounded (`|β·dt|≤π`). Coupling hybridizes poles conserving
   `Σ Re(λ) = −Σκ_tot`.
5. **(B1) Trainable-parameter + actuation map** (`docs/s0_1/B1_actuation_map.md`): the in-situ-trainable
   recurrence = `{δ_j` (heaters)`, κ_tot,j` (tunable couplers and/or per-ring gain)`, μ_jk` (ring–ring
   coupling)`}`; residues/B,C (MZI mesh) train-only = the reservoir baseline (explicitly excluded from
   the claim). A **gain-free Stage-1 minimal set already suffices** for the white-space claim. → PR-2.
6. **(B2 / F19) Backscatter bound — "SAY IT LOUDLY"** (`docs/s0_1/B2_backscatter_bound.md` +
   `backscatter_crossover.png`): literature pull (8 SiN-anchored cites) shows splitting is
   **process-roughness-limited, NOT cleanly Q-gated** — *contradicting the roadmap's "negligible at
   foundry Q" assumption.* Crossover (2γ=κ_i): **damascene-clean Q_cross=4.1e6** (foundry single-pole OK,
   3e7 splits 7.3×); **rough subtractive Q_cross=3–5.4e5** (splits 21–75 % of modes already at foundry
   Qi=2e6). **Recommend** S0.3 carry an *optional CW/CCW splitting knob gated by a process-roughness
   flag* (default OFF only for the clean foundry corner). → flag D-2026-06-08-3.
7. **(B3 / F13.3) Memory-vs-readout-SNR (κ_ext) trade** (`docs/s0_1/B3_kappa_ext_tradeoff.md` +
   `kappa_ext_tradeoff.png`): undercoupling maximizes memory but collapses readout residue + drop
   efficiency; `memory × residue ≤ passive memory` (bounded, tested). At Qi=2e6: 274 rt / 0.028 drop-eff
   (kext=0.1κ_i) → 16 rt / 0.91 (kext=10κ_i). κ_ext also couples to B2 (overcoupling hides the doublet).
   → PR-4 (I characterize; I do not pick the operating point).
8. **(F13.1) Registry Q/loss self-consistency fix** (`platforms.py`): added `q_basis` (Qi|loss|
   independent) — each entry registers a primary, derives the partner. **AN800 reconciled:** Qi=2e6
   primary (foundry corner), loss 0.03→**0.172 dB/cm** (the 0.03 implied Qi=1.14e7, 5.7× off). CORNERSTONE
   loss-primary (Qi=2.347e5 derived); damascene Qi=3e7 primary (loss 0.0123 dB/cm derived). New
   `loss_q_ceiling_ok` invariant (Qi ≤ propagation ceiling) holds for all 6 entries; SiN entries on the
   ceiling (err ≤2e-5). **Operating Q still NOT chosen** (D-2026-06-08-1 / PR-4).

**Gates:** **S0.1 gate PASSED** — dynamical poles match the CMT/transfer reference (uncoupled <1e-3,
discrete `|z|` <1e-9, ZOH exact), and the CW limit recovers the S0.0 static reference (O(1/F), <1%).
(3a)/(3b) confirmed in the new model. All 99 tests pass (~1.4 s).

**Anomalies / honest flags:**
- **B2 contradicts a roadmap assumption** (splitting bites at foundry Q for rough process) — surfaced
  loudly per the task's instruction; recommendation made, decision left to Supervisor/Lucas
  (D-2026-06-08-3).
- **Mapping subtlety flagged (D-2026-06-08-2):** one optical ring = one *complex* pole (diagonal complex
  SSM / S4D), whereas a real LinOSS oscillator is a conjugate *pair*. Both supported; the PR-2
  architecture choice is the Supervisor's.
- **B2 verify-before-citing:** the 63 MHz Pfeiffer figure + some author lists came via search-aggregation
  — flagged in the memo for primary-source confirmation before proposal use (no published γ for AN800/
  CORNERSTONE specifically; the crossover curve is assembled from bracketing SiN points).
- The proposal's schematic `√κ_ext s_in` vs the energy-conserving Haus `√(2κ_ext) s_in` — same model,
  factor-2 naming; documented in `mapping_notes.md §1` for the write-up.
- Per-round-trip ASE inside the rollout remains S0.3 (the single-ring/coupled model here is the clean
  linear-optical forward model, as scoped).

**Data path:** code+tests in repo; figures + JSON under `results/s0_1/` (git-ignored, regenerable via
`python3 analysis/s0_1_pole_region.py`); memos under `docs/s0_1/`. **Compute:** local CPU, ~1.4 s tests
+ <1 s analysis.

---

## S0.0 — Repo init + selective salvage + smoke test (2026-06-08, Executor)

**Goal:** stand up the Project_SSM repo under git; salvage the 7 manifest assets
(`shared/tooling_recon.md` §4) with provenance headers, decoupled contact points and passing ported
tests; prove the toolchain with the salvage-validation smoke test. No SSM core (that is S0.1+).

**Config:** local CPU, python 3.12.3, torch 2.11.0+cpu. Source `~/Documents/pnn-multilayer` @
`e2eec80` (read-only, untouched). New package `photonic_ssm/` (torch-only runtime, enforced by a
hygiene test); 60 tests.

**Key findings / deliverables:**
1. **Repo:** `git init` (D-2) → 2 commits: `a6de34f` (docs/coordination snapshot), `19e64d4`
   (salvage + tests). `.gitignore`, `requirements.txt` (torch-only + pytest), `README.md` with the
   salvaged-vs-new table and the two architecture constraints.
2. **All 7 assets ported** with `# salvaged from pnn-multilayer @ e2eec80 : <path>` headers:
   `platforms.py`, `gain.py`, `dynamic_gain.py`, `static_rings.py`, `estimators/spsa.py`,
   `baselines/ridge_readout.py`, `runner/` (pattern-salvage per manifest). **60/60 tests pass**
   (~1.3 s).
3. **Decoupling points** (exactly the recon's predictions; nothing resisted lifting):
   SPSA — hard-coded `compute_nmse_field` → injected `loss_fn`, `model.forward_batched` → injected
   `forward_fn`; ridge readout — severed from the MRR cascade + PAM-4/sps framing, now consumes
   arbitrary `[T, F]` state trajectories; static Lorentzians + drift — de-classed from the
   `BaseMRR`/nn.Module lifecycle to pure functions; gain/dynamic-gain/platforms — none needed.
4. **Smoke gates (all pass, pinned numbers):**
   (i) all salvaged assets import; full suite green.
   (ii) salvaged single-bus Lorentzian == analytic add-drop through-port in the κ₂→0 limit
   **exactly** (max err 0.0 at float64, after the documented −1 phase-convention factor); add-drop
   references self-validate: lossless |T_t|²+|T_d|² −1 ≤ 1.6e-15, critical-coupling extinction
   < 1e-14.
   (iii) FSR self-consistency: worst |tabulated−derived| = 1.2e-05 GHz over 6 registry entries
   (tol 0.01).
   **SPSA FD-vs-autograd anchor reproduced after decoupling: RMS rel err = 1.1e-07** (inherited
   gate < 1e-2) on a float64 toy model built from salvaged primitives; SPSA+Adam drives a 12-dim
   quadratic 0.81 → <5e-7 in 400 updates = 800 physical forward passes (`n_forward_equivalents`
   accounting verified exact: 2/update SPSA, 2N+1/update FD).
5. **Architecture constraints baked in + enforced by tests:**
   **(3a)** gradients flow through the optical state — `test_gradient_flows_through_state_and_params`
   proves a last-symbol loss receives gradient from inputs ~5 symbols earlier *through the carrier
   memory* of `TrainingAwareDynamicSOAPerMode` (the reference pattern); checkpointed vs
   non-checkpointed rollouts agree in outputs AND grads to <1e-10; the forward-only eval classes are
   documented as eval-only and tested to build no graph.
   **(3b)** full-state-trajectory exposure — encoded as the API contract (`ReservoirReadoutBaseline`
   consumes `[T, F]` trajectories; requirement documented in the package docstrings); the actual
   substrate API that honors it is S0.1/S0.3 work.
6. **Platform registry extended, operating Q deliberately NOT chosen** (parked D-2026-06-08-1):
   added `SiN_CORNERSTONE_300` (1.5 dB/cm C-band per the CORNERSTONE platform paper, Littlejohns
   2020; Qi=2.3e5 *derived* from loss — no published ring Q; n_g=2.0 flagged as estimate) and
   `SiN_damascene_UHQ` (0.01 dB/cm / Qi=3e7, Liu et al. Nat. Commun. 12, 2236 (2021); internally
   consistent: loss-implied Qi=3.7e7). Registry now spans Qi 2.3e5 → 2e6 → 3e7.

**Anomalies / honest flags:**
- The task's smoke item (ii) presumed the salvaged Lorentzian was add-drop; **the source repo has
  only the single-bus (all-pass) form** — no two-coupler add-drop transfer exists anywhere in
  `pnn-multilayer`. The analytic add-drop references are therefore NEW code (clearly marked, in
  `static_rings.py`), validated against textbook properties, with the salvaged form checked against
  their exact κ₂→0 limit. S0.1's CW-limit gate gets both references.
- **Inherited registry tension, input to D-2026-06-08-1:** `SiN_LIGENTEC_AN800` tabulates Qi=2e6
  (foundry quote) alongside 0.03 dB/cm, but 0.03 dB/cm *implies* Qi≈1.14e7 — the entry's Q and loss
  are independently sourced, not mutually consistent. The two new entries are internally consistent.
- Dynamic gain classes still have **no ASE inside the rollout** (only the instantaneous
  `soa_activation_with_ase` has ASE) — per-round-trip ASE accumulation is new S0.3 physics, as the
  recon flagged.
- No equalization assumptions survived: enforced by a ported negative source-grep test
  (`test_no_equalization_coupling.py`) — zero references to the equalization stack, zero non-torch
  third-party imports in the package.
- The sweep-runner mp test uses the `fork` context (`spawn` requires importable job functions;
  production drivers keep the torch-safe `spawn` default with their own top-level job fns).
- `shared/critic_review_stage0-roadmap.md` (Critic, parallel track) appeared during the task and is
  committed with the coordination state in `19e64d4`; not read/acted on by the Executor.

**Gates:** all S0.0 gates **PASSED** (7/7 assets ported + tested; anchor reproduced; constraints
honored; smoke i–iii green).

**Data path:** code+tests in repo (commits `a6de34f`, `19e64d4`); no experiment data generated
(infrastructure task). **Compute:** local CPU, total test wall-time ~1.3 s.

---

**S0.0a — Tooling recon (2026-06-07, Executor):** report at [`shared/tooling_recon.md`](tooling_recon.md) — `equalization_ringbank.py` is **not** a head start for the S0.1 mapping (all `pnn-multilayer` ring code is static/CW transfer functions; the dynamical CMT core is new code either way), but SPSA + pass-accounting, rate-equation gain (autograd-checkpointed), SiN platform registry, drift machinery, ridge readout and sweep scaffolding are liftable → recommendation: **(a) selective salvage** (≈1 day port vs ≈3–5 days extra for clean start). Read-only; no code written. Awaiting Lucas's D-1/D-2 rulings.
