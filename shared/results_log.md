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
