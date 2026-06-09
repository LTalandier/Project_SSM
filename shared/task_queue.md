# Task Queue

Supervisor assigns tasks here. The Executor reads and executes the task marked **ACTIVE**, then
**stops and waits**. The Supervisor marks a task **COMPLETED** (date + one-line summary) before
assigning the next. New tasks go at the top, below this header.

Task format: see `.claude/skills/executor/SKILL.md`.

---

## 🟢 ACTIVE — S0.1.1: S0.1 closeout (decision-free Critic edits before S0.2)

**Assigned:** 2026-06-09
**Supervisor:** Claude Opus 4.8
**Status:** ACTIVE
**Source:** `critic_review_s0-1-results.md` (APPROVE-WITH-EDITS) — the four **decision-free** items the
Critic wants landed before PR-1/PR-2 freeze. The two *framing* items (F2 mapping-class, F6 gain-free κ_ext)
are Supervisor/PR-2 work and wait on Lucas's D-08-2/D-08-3 steer — **not** in this task.

### Goal
Close the validation/hygiene gaps the Critic raised. **Do not touch the architecture framing** (that is the
Supervisor's mapping write-up + PR-2). Small code/prose/test edits only.

### Deliverables
1. **(S0.1-F1, HIGH) Transient-dynamics validation.** The gate currently proves the mapping by
   *construction* (van Loan exact; steady-state + pole algebra) but never integrates the ODE forward and
   compares the *transient* to an independent reference. Add: (i) single-ring **ringdown + step response**
   vs the closed form `a(t)=a₀e^{(iδ−κ)t}` **and** vs an independent integrator (scipy/torchdiffeq RK45 on
   `da/dt=Ma+Bu`), asserting decay rate κ **and** oscillation frequency δ *in the time domain*; (ii) a
   **2-ring μ≠0** case whose hybridized **beat frequency** matches Im(eig(M)) splitting. The contribution
   *is* the dynamical mapping — it deserves a positive time-domain check.
2. **(S0.1-F3, MEDIUM) Fix the 2× memory-units slip** (results-log finding 4 + `mapping_notes` §4). "329
   round trips" pairs with **3.29 ns** (amplitude/state memory `1/κ_i`), not 1.65 ns (photon lifetime
   `Qi/ω₀=1/2κ_i`). The **code already distinguishes them**; fix the **prose** to report the
   **amplitude/state-memory convention consistently** (3.29 ns / 329 rt; **49.4 ns** / 4937 rt at Qi=3e7) —
   this is what PR-2 sizes the task against.
3. **(S0.1-F4, MEDIUM) Fix the B2 high-roughness row + state the criterion band.** The row mixes a
   160-MHz-based `Q_cross=3.0e5` with 125-MHz-based ratios (tabulated 5.2/77.6 vs the consistent 6.6/99).
   Recompute to **one γ**. Add that the criterion is `2γ≳κ_tot` (HWHM, the *conservative* choice) and that
   the FWHM `2γ≳2κ_tot` shifts every `Q_cross` ×2 — carry the ~2× band. (Conclusion unchanged under both.)
4. **(S0.1-F7, MEDIUM) Fix the registry mislabel.** The conservative corner (Qi=2e6 / 0.172 dB/cm) must not
   be attributed to the named foundry product. **Rename it `SiN_foundry_conservative`** (no foundry
   attribution) **and** add a separate `SiN_LIGENTEC_AN800` with the **actual** demonstrated numbers
   (≈0.05 dB/cm, Qi≈6.8e6 derived, primary-sourced). Keep the conservative corner as the Gate-ii candidate
   cell (F13); only the name/citation changes. Re-run loss↔Q + FSR tests over the updated registry.

### Out of scope (Supervisor / later)
- **F2** (mapping-class reframing → diagonal/S4D, LinOSS as special case) — Supervisor mapping write-up +
  PR-1/PR-2, pending the D-08-2 steer. **F6** (gain-free κ_ext actuation vs readout independence) — PR-2.
- **F5** (B2 primary-source verification) — S0.L, before-paper. **F8** (thermal self-heating; pole-region
  realizability completeness — state-dim/placement) — register for the S0.3 substrate + PR-2 sizing.

### Gates
Transient tests pass (decay rate + frequency in the time domain; 2-ring beat matches eig splitting); full
suite green; memory prose one (amplitude) convention; B2 row internally consistent + criterion band stated;
registry relabeled + tests green.

### Deployment
Local CPU; hours. No cloud.

> **Parallel:** Lucas is steering D-08-2/D-08-3 (low-risk — Supervisor + Critic aligned). This closeout is
> decision-free and upstream of the framing, so it runs safely alongside that steer.

---

---

## ✅ DONE — S0.1: Oscillator↔SiN-ring mapping + realizable pole region

**Assigned:** 2026-06-08 · **Closed:** 2026-06-09
**Supervisor:** Claude Opus 4.8
**Status:** ✅ COMPLETED 2026-06-09 — gate PASSED; two architecture decisions surfaced (D-08-2 mapping fork, D-08-3 backscatter) → Critic + Lucas. Results in `results_log.md`.
**Roadmap:** `stage0_roadmap.md` v3 §S0.1 (scope (B) Lucas-blessed 2026-06-08). **Prereqs:**
`photonic-ssm-proposal-v0_5.md` §3 (mapping) + §4 (pole region); the salvaged `static_rings.py` (the
**CW-limit reference** — S0.0); `preregistration.md` (this phase *feeds* **PR-2** task-sizing and **PR-4**
$Q$/$\kappa_\text{ext}$ — it does **not** freeze them); `results_log.md` (S0.0).

### Goal
Build the **first new dynamical core**: the temporal-CMT single-ring model and the coupled-ring →
$N$-oscillator LinOSS forward model (the recon established this is new code — `pnn-multilayer`'s ring code
is static/CW). Bound the realizable pole region, and deliver the three scope-(B) results that the headline
claim and the downstream pre-registration depend on. **This is simulation + model-building + a literature-
sourced physics bound; the formal mapping write-up + white-space wording are the Supervisor's** (role
boundary) — you produce the verified model, the plots, and the data/tables those will cite.

### Deliverables
1. **Dynamical single-ring temporal-CMT model** — $\dot a = (-\kappa_\text{tot}+i\Delta\omega)\,a +
   \sqrt{\kappa_\text{ext}}\,s_\text{in}(t)$, pole $s=-\kappa_\text{tot}+i\omega_\text{res}$ (with
   $\kappa_\text{tot}=\kappa_i+\kappa_\text{ext}$). **Not** the salvaged static transfer function. Verify
   the **CW limit recovers the S0.0 salvaged Lorentzian + the analytic add-drop reference** within a
   stated tolerance (this is the S0.1 gate).
2. **Coupled-ring → $N$-oscillator LinOSS forward model** — map to the eigenvalue form
   $a_i=-e^{\alpha_i}+i\beta_i$; integrate in time. **Honor both architecture constraints (now roadmap
   gates, F18): (3a)** gradients flow through the optical state (checkpointed unroll — the
   `TrainingAwareDynamicSOAPerMode` pattern, no `no_grad`/detach); **(3b)** expose **full state
   trajectories** in the API (adjoint/RHEL will need them at S0.4).
3. **Realizable pole-region bound (§4)** — stability is free; memory is **loss-limited**; $\beta_i$ is
   **FSR-bounded**; poles placed by drift-stable thermo-optic trim. Plot the pole region with the
   **loss/gain → $|\lambda|$ (memory-length) relation** across the registry's $Q$ span (foundry
   $2\times10^6$ → class-leading $3\times10^7$).
4. **(B1) Trainable-parameter set + actuation map** — a table: which physical parameters are
   in-situ-trainable and by what actuator — detunings $\beta_i$ (heaters); pole **real** parts (tunable
   bus–ring coupling, e.g. MZI-assisted couplers, and/or per-ring gain); inter-ring coupling topology
   (direct photonic-molecule vs bus-mediated). Flag the device-complexity cost of each. *(Load-bearing for
   the white-space sentence — feeds PR-2; the Supervisor writes the claim wording from this.)*
5. **(B2 / F19) Backscatter / CW–CCW mode-splitting bound** — literature-sourced: plug cited
   surface-roughness backscatter splitting-rate figures into splitting-rate-vs-$\kappa_\text{tot}$ across
   the registered $Q$ range; state **where "one ring = one complex pole" breaks down** (expected
   negligible at foundry $Q\approx2\times10^6$, *not* at $\sim10^7$). **Recommend** whether S0.3 needs an
   optional mode-splitting knob. Cite sources (this is the physics input; framing is Supervisor/S0.L).
6. **(B3 / F13.3) Memory-vs-readout-SNR ($\kappa_\text{ext}$) trade** — derive/plot it: deep undercoupling
   maximizes memory ($|\lambda|$) but collapses I/O residues + detector SNR. Show the realizable region as
   a function of the $\kappa_\text{ext}$ policy. *(Feeds PR-4 — you characterize the trade; you do **not**
   pick the operating point.)*
7. **(F13.1) Registry Q/loss self-consistency fix** — each SiN entry must be internally consistent:
   register one of $(\alpha, Q_i)$ as primary and **derive** the other ($Q_i=\omega n_g/(c\,\alpha)$); add
   a **loss↔Q self-consistency test** alongside the existing FSR check; reconcile `SiN_LIGENTEC_AN800`
   (currently $Q_i=2\times10^6$ *and* 0.03 dB/cm, which disagree ~5.7×). **Do NOT pick the operating $Q$**
   — that is PR-4 at S0.3 (foundry-gated). Keep all registry entries; just make each self-consistent.

### Key gates and questions
- **Gate:** dynamical poles match a coupled-mode/transfer-function reference within a stated tolerance,
  **and** the CW limit recovers the S0.0 static reference. Report the tolerance you pre-state.
- Confirm (3a)/(3b) are honored in the new dynamical model (not just inherited from the salvaged layer) —
  a test that a loss at time $T$ receives gradient through the ring state from an input at $t\ll T$.
- B2: if the literature says splitting bites *within* the registered $Q$ range, say so loudly — it
  threatens the core one-ring-one-pole abstraction and changes S0.3.
- Flag anything that makes the §3 mapping less clean than the proposal assumes (e.g. dispersion, TPA/FCA
  at the powers gain requires, thermal nonlinearity) → `decisions_needed.md`.

### Deployment
Local CPU; model-building + analysis + a focused literature pull for B2. Minutes-to-~1–2 days. No cloud.

> **Next:** Executor stops at completion and reports to `results_log.md`. Per the gate model, the **Critic
> reviews S0.1 results before S0.2 starts**. The Supervisor then writes the mapping result + white-space
> wording, and specs S0.2 (which freezes PR-1/PR-2/PR-10).

---

---

## ✅ DONE — S0.0: Repo init + selective salvage + smoke test

**Assigned:** 2026-06-08 · **Closed:** 2026-06-08
**Supervisor:** Claude Opus 4.8
**Status:** ✅ COMPLETED 2026-06-08 — all S0.0 gates passed (7/7 assets ported + tested; SPSA anchor reproduced; both architecture constraints honored; smoke i–iii green). Results in `results_log.md`.
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
