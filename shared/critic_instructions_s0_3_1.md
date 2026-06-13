# Critic instructions — S0.3-1 substrate-build review (the shared dissipative-ring model)

**Filed:** 2026-06-13 (Supervisor). **Target:** the S0.3-1 build — `photonic_ssm/substrate/`
(6 modules + `calibration`), `tests/test_substrate.py`, `analysis/s0_3_1_*.py`, and the
outputs in `results/s0_3/` — against the **frozen PR-4 v2** block in `shared/preregistration.md`
and the roadmap §S0.3 Gate F18. **Output:** `shared/critic_review_s0_3_1.md`; verdict
APPROVE / APPROVE-WITH-EDITS / AMEND / REJECT, findings tagged **S31-F#** with severity. You
report to **Lucas**, not the Supervisor.

**Why a build (not a freeze) gets a Critic pass:** this substrate is the single model all four
estimators and the entire bake-off run on — its correctness and its fidelity to the freeze are
load-bearing for everything in S0.4–S0.8. The Supervisor has already ACCEPTED the build (gate
F18 passes, independently re-run: 9/9) and flagged one finding (S-F1, gain-mode) — your job is
to **independently confirm or refute that finding and hunt for others**, not to re-bless the
green tests.

**Evidence base / read first:** the frozen **PR-4 v2** block (esp. §G gain, §N/O2 + E6 cadence,
the calibration addendum) · `tests/test_substrate.py` · `photonic_ssm/substrate/{gain,
dissipative_ring,ase,normalization,cells,splitting}.py` · `results/s0_3/*` · the S0.3-1
`results_log.md` entry (the Executor's own 5 flagged anomalies A–E) · frozen PR-2 v2 (P2
partition, μ(0)=0, F12), PR-13, PR-10, PR-11, S0.1 conventions.

## Stance: adversarial. Two hostile readings to try to make stick:
1. *"The F18 gate is green but hollow"* — the substrate passes its tests without faithfully
   implementing the freeze where it's hardest to test (the differentiable gain operating point).
2. *"The substrate the four estimators will share is not actually one model"* — a mode/convention
   choice makes SPSA and the gradient methods train different functions.

## Checklist (work every item; CONFIRMED / REFUTED / EDIT per item)

1. **S-F1, the central item — gain-mode fidelity (verify or refute the Supervisor's reading).**
   The rollout defaults to `gain_mode="fixed"` (g ≡ 0.9·κᵢ, a constant); `test_h` uses that
   default, so its κ_ext gradients flow through the coupling/loss/input path, **not through the
   gain**. The freeze §G says the operating point is "a **differentiable function of the episode
   drive statistics**" and §N E6 says "trained κ_ext excursions change intracavity energy **as
   physics, not as renormalization**." (a) Is "fixed" a faithful reading of §G's "runs at g_rt =
   0.9×intrinsic", or does the freeze require the **saturating** mode (g(P̄(κ_ext)) computed once
   per episode, held fixed within the rollout)? (b) **Quantify the dropped gradient**: at the
   registered deep-saturation point (P_circ/P_sat ≈ 8.3e3 @ C-2), how large is ∂g/∂κ_ext that
   "fixed" omits — material or negligible? (c) **Does `gain_mode="saturating"` actually train** —
   finite, nonzero grads through the gain to κ_ext, no NaNs at the deep-saturation operating
   point? (Run it.) (d) **Shared-substrate risk**: if SPSA's ± passes use real saturating gain
   while PAT/adjoint/BPTT backprop through fixed gain, are the four estimators training the *same*
   function? Is this a PR-6 item, a freeze-interpretation question for Lucas, or a non-issue?
2. **F18 gradient-flow gate — is it non-trivial?** Does `test_h` actually prove the no-detach
   property the in-situ thesis rests on, or could it pass with the gain detached? Propose the
   minimal strengthening (e.g. assert the saturating-mode κ_ext grad ≠ the gain-detached grad).
   Check the ASE `no_grad` blocks are genuinely the **exogenous-noise** path (correct — you don't
   backprop into a noise realization) and not silently breaking the state-path gradient.
3. **Calibration re-derivation (independent).** Re-derive E₀ = 2·κ_ext,θ₀·(P̄₀/ħω₀)/κ_net² for
   all cells (Supervisor hand-checked C-2 = 1.07e8). Re-derive the reachability solve: required
   small-signal g₀ (bus) vs the Er span 1.0–1.9 dB/cm. **The Supervisor downgraded C-2 from the
   source table's "✅" to "reachable iff Er ≥ 1.5 dB/cm" — confirm that, and check no other cell's
   status is overstated.** Is the build-up ×262 / bus-depth ×31.6 correct?
4. **Fidelity-to-freeze sweep.** Every registered PR-4 v2 number, re-derived: 2γ/κ at passive
   floor AND operating gain (2.33/1.04/4.58 ↔ 5.3/2.4/10.5); memory 9.4/32.0; in-band 29.5/100
   (2 GS/s) + 14.8/50/222 (1 GS/s); n_ss 22.55/8.98; A1↔A2 ≤ O(1e-3). Conventions: κᵢ=ω₀/2Qᵢ,
   κ_net=0.1κᵢ+2κ_ext at the operating point, symmetric add-drop, ZOH/van-Loan, doublet =
   single-direction eigenvalues duplicated. Cells C-1/C-2/C-3 + sensitivity (C-2 derate, P-CORN
   passive, γ/NF menus) all present and correct?
5. **Anomaly audit (the Executor flagged 5 — are they correctly scoped?).** (A) μ(0)=0 leaves the
   chain disconnected at init → untrainable at N=32; the sweep used a labelled nonzero μ-init.
   Is μ(0)=0 a real PR-2/PR-6 init convention, and is "disconnected cold-start" a genuine risk
   the **bake-off** (all four methods) must confront, or a sweep-only artifact? **This is likely
   the most consequential finding for S0.4 — weight it.** (B) damping-curve fixed-budget confound
   → is PR-12 freezable off this data at all, or is a convergence-controlled rerun required?
   (C) 4-seed high variance — which point(s) need 8? (E) **token-hygiene gate**: the new T-A
   generator uses neutral names (`PAM_LEVELS`/`nearest_pam`) to keep `test_no_equalization_coupling`
   green. Transparent — but is *naming around a gate* acceptable, or should the gate be rewritten
   to assert the real invariant (the source equalization stack is absent) so no one codes around
   it? Is the source stack genuinely absent (spot-check the forbidden tokens)?
6. **Cross-consistency vs frozen entries.** PR-2 (P2 partition {δ,κ_ext,μ}, μ(0)=0, F12), PR-13
   (does the k-grid sit where the memory-at-operating-point puts it, per the report's table?),
   PR-10 (clocks 0.1/1/2), PR-11 (independent forward/echo ASE streams — present in the ASE
   injector?), S0.1 (the substrate reduces to `CoupledRingLinOSS` in the passive limit — test b).
7. **Anything the build silently decided that the freeze didn't cover** (an F12-style sweep): list
   each. The Supervisor found one (gain-mode default); are there others (e.g. the 8-tap readout
   head, the mini-batch/LR/grad-clip training recipe in the sweep, the A1 tau_rt convention)?

**Format:** lead with the verdict + a findings table (S31-F#, severity, one-line). Then the
per-item dispositions. If you confirm S-F1, say whether it's APPROVE-WITH-EDITS (flip the default
+ strengthen the gate, no freeze touched) or AMEND (needs a Lucas freeze-interpretation first).
The Supervisor responds with the disposition; the Executor implements fixes. You report to Lucas.
