# Critic review — S0.3-1 shared dissipative-ring substrate build

**Reviewer:** Critic session · **Date:** 2026-06-13 · **Spec:** `shared/critic_instructions_s0_3_1.md`
**Target:** `photonic_ssm/substrate/` (6 modules + `calibration`), `tests/test_substrate.py`,
`analysis/s0_3_1_*.py`, `results/s0_3/*`, against the **frozen PR-4 v2** block and roadmap Gate F18.
All decisive claims re-derived independently (the 9-test suite re-run 9/9; gradients, poles, E₀,
reachability, cold-start, and the token gate probed directly — session scripts).

---

## Verdict: **APPROVE-WITH-EDITS**

The build is **correct and freeze-faithful where it counts**: the passive/zero-noise limit reproduces
the S0.1 forward model to 1.4e-20 (test b, re-confirmed), every registered PR-4 v2 number reproduces
exactly from the substrate itself (2γ/κ_net = 5.318/2.371/10.459 vs 5.3/2.4/10.5; memory 9.4/32.0;
in-band 29.5/100; E₀ C-2 = 1.07e8; n_ss 22.55/8.98; A1↔A2 2.1e-3), the splitting doublet has real part
−κ_net to 1e-7 and splits by exactly 2γ, the reachability solve is honest and no cell's status is
overstated, and the gradient-checkpointing is value- and gradient-exact. The reporting is unusually
candid (the Executor flagged its own five anomalies). **I confirm S-F1** and find it more structurally
serious than MEDIUM, but it is fixable without touching the freeze — **flip the `gain_mode` default to
`"saturating"`, harden `test_h`, and register the mode for all four estimators**. None of the findings
below impugn the build's correctness; they are one faithfulness gap, one correctly-flagged trainability
risk, and several visibility/hygiene repairs.

**S-F1 disposition (the spec's explicit question): APPROVE-WITH-EDITS, not AMEND.** The freeze text
already *mandates* the saturating mode — §G "the operating point enters the autograd graph as a
**differentiable function of the episode drive statistics** (no detach)" and §N-E6 "trained κ_ext
excursions change intracavity energy **as physics, not as renormalization**." `"saturating"` *is* that;
`"fixed"` is the unfaithful one. So flipping the default conforms the code to the signed freeze — **no
freeze change**. The one thing for Lucas to *confirm* (not reinterpret) is the bake-off-wide
consequence: all four estimators must run the same `gain_mode`, which is a PR-6 registration, not a
PR-4 edit.

## Findings

| # | Severity | One line |
|---|---|---|
| S31-F1 | **HIGH** | `gain_mode="fixed"` default drops ∂g/∂κ_ext (27% of the true κ_ext→κ_net gradient at θ₀; **6× the retained term and sign-flipped** across the K4 range), is unfaithful to §G/§N-E6, and makes `test_h` a hollow gate (passes with the gain path dead) → shared-substrate risk for the bake-off. **Confirms S-F1.** |
| S31-F2 | **HIGH** | μ(0)=0 cold-start: rings 2..N are **signal-starved** — *exactly* zero gradient in the noiseless limit (7/7, 31/31 verified), signal-free noise gradient with ASE on → the **N=32 headline cell is untrainable from cold**. Top S0.4 risk; correctly PR-6-scoped by the Executor; mechanism statement needs sharpening. |
| S31-F3 | MEDIUM | Reachability is reported on the **bus plane** (×32) but the gain model *saturates on the intracavity plane* (×8292 at C-2 → required g₀ ≈ 380 dB/cm); on the plane the model actually uses, **C-2 and C-3 are material-aspirational too**, not just C-1. Build is freeze-faithful; surface g₀_req_intracavity so anchor-risk (v) isn't understated. |
| S31-F4 | MEDIUM | The damping sweep cannot cleanly freeze PR-12 (fixed-budget trainability confound — Executor anomaly B, confirmed); **additionally** its g_f axis *is* PR-4's registered gain operating point, so a PR-12 pick of g_f≠0.9 contradicts PR-4 §G — the PR-4/PR-12 relationship needs Supervisor reconciliation before PR-12. |
| S31-F5 | MEDIUM | Token-hygiene gate: the source training stack **is** genuinely absent (verified), but the gate asserts a *token* ("PAM4"), not the real invariant, and the build renamed legitimate 4-PAM vocabulary to keep it green. Rewrite the gate to assert the source-stack symbols absent; drop the generic task-token bans that now collide with the registered T-A task. |
| S31-F6 | LOW | The ASE covariance Q_d is detached from the parameter gradient (reparameterization-gradient through the noise amplitude dropped). Defensible, consistent across estimators, hardware-faithful — but an un-registered modeling decision the freeze didn't cover; register it. |
| S31-F7 | LOW | PR-11 forward/echo-independent ASE streams are **supported** (generator arg) but not **enforced**; the RHEL echo path (S0.4) must pass a distinct generator — carry to S0.4. |
| S31-F8 | LOW | The sweep training recipe (batch 8, cosine LR, grad-clip, nonzero μ-init 0.3κᵢ, δ-band 4κᵢ) is un-registered and was load-bearing for N=32 trainability — these become PR-6 freeze items; enumerate them. |

---

## The two hostile readings, adjudicated

**Reading 1 — "F18 is green but hollow": STICKS on the gain path (S31-F1).** `test_h` asserts nonzero
grads on {δ, κ_ext, μ}. In the default `"fixed"` mode g ≡ 0.9·κᵢ is a constant, so κ_ext's gradient
flows only through the `+2κ_ext` loss term and the input map `B = √(2κ_ext,1)` — **never through the
gain.** The test passes anyway, so it *cannot distinguish* "the gain gradient flows" from "the gain
gradient is dropped." It would pass identically with the gain explicitly detached, because in `"fixed"`
mode it already is. That is the hollow gate. (It does *not* stick on the rest of F18: the passive-limit
equality, checkpoint gradient-equivalence, and no-detach state path are all genuine.)

**Reading 2 — "not actually one model": STICKS conditionally (S31-F1d).** SPSA is model-free — its two
forward passes evaluate the substrate at θ ± cΔ. If those passes use the faithful `"saturating"` gain,
SPSA estimates the gradient of the *true* κ_ext-dependent function; if PAT/adjoint/BPTT backprop through
`"fixed"`, they target a function whose κ_ext gradient differs by the dropped ∂g/∂κ_ext. Measured on one
shared loss at θ₀: ‖g_fixed − g_sat‖/‖g_sat‖ = 0.11 (cos 0.9998 at C-2 — ring-1's huge B-path dominates
the norm and is identical in both), but the divergence is **not** uniform: the dropped term is 27% of
the κ_net channel at θ₀ and grows to **6× the retained term at r = 0.1** (the undercoupled edge training
pushes toward), and it **changes sign at r = 0.5**. So "fixed" is not a benign small bias — it is a
structurally different operating-point model over the K4 range. The clean fix that closes *both*
readings: make `"saturating"` the default and the registered bake-off mode, so all four estimators train
the one true function.

---

## Checklist dispositions (1–7)

**1. S-F1 — CONFIRMED (HIGH).** (a) `"fixed"` is *not* a faithful reading of §G: §G's "runs at g_rt =
0.9×intrinsic" is the operating-point *target* (reached by the saturated solve at the registered drive,
θ₀), not a κ_ext-independent constant — the very next clause ("differentiable function of the episode
drive statistics, no detach") and §N-E6 ("as physics, not renormalization") foreclose the constant
reading. The faithful mode is `"saturating"` (g(P̄(κ_ext)) computed once per episode, held fixed across
the T steps — which `gain_rate_per_ring()` does: one evaluation per `forward()`, M1-correct). (b)
**Quantified dropped gradient** (autograd, registered operating points): ∂g/∂κ_ext = −0.750 at all three
cells' θ₀ ⇒ true dκ_net/dκ_ext = 2.75 vs the fixed 2.0 → **fixed drops 27.3%**. Across the K4 bounds at
C-2: −10.1 (r=0.1) / −0.75 (r=0.3) / 0.0 (r=0.5) / +0.32 (r=1) / +0.41 (r=3) — at the undercoupled edge
the dropped term is 6× the retained one and the sign flips at the build-up peak. **Material, not
negligible.** (c) **`"saturating"` trains** — finite, nonzero κ_ext grads, no NaN, at C-1/N=8 and
C-2/N=32 (verified). (d) Shared-substrate risk per Reading 2 above: a PR-6 registration item, resolved
by registering `"saturating"` for all estimators.

**2. F18 gradient-flow gate — EDIT.** Hollow on the gain path (Reading 1). The ASE `no_grad` blocks are
**correct**: `process_noise_cov_A2/A1` and `sample()` detach the *noise realization and its covariance*
— adding an exogenous, parameter-independent η to the state preserves ∂a/∂params through the
Φa + Γu path (test_h grads are nonzero with ASE ON; the deterministic path is intact). Minimal
strengthening (spec's ask): in `"saturating"` mode assert `dκ_net/dκ_ext ≠ 2` (i.e. the gain path is
live) — concretely, that the autograd κ_ext-gradient of `kappa_net()` differs from the fixed-mode value
by the predicted ∂g/∂κ_ext, and that the gate **runs the faithful mode**. (A weaker but sufficient form:
assert the saturating κ_ext grad ≠ the fixed κ_ext grad on the same loss/seed.)

**3. Calibration re-derivation — CONFIRMED.** E₀ = 2·κ_ext,θ₀·(P̄₀/ħω₀)/κ_net² re-derived from the CMT
steady state and matches per cell: **C-1 3.14e7, C-2 1.07e8 (Supervisor hand-check ✓), C-3 4.72e8**,
C-2-derate 5.34e7, P-CORN 7.06e5. Reachability re-derived independently: required small-signal g₀(bus) =
g_op·(1+P̄₀/P_sat); C-1 5.04, C-2 **1.50**, C-3 0.36 dB/cm vs Er 1.0–1.9. **The C-2 downgrade is exactly
right** — C-2 is reachable iff Er ≥ 1.5 (my check: reachable@1.5 True, @1.0 False; the boundary
Er_hi/g_op ≥ 1+×31.6 lands at 1.497). **No other cell overstated**: C-1 and C-2-derate correctly
material-aspirational, C-3 ✓, P-CORN passive. Build-up ×262 / bus depth ×31.6 reproduce §G. **One
caveat → S31-F3:** the verdict is on the *bus* plane; the gain model's own *intracavity* plane (the
field the medium actually sees) requires g₀ ≈ 380 dB/cm at C-2 — see below.

**4. Fidelity-to-freeze sweep — CONFIRMED.** Every number reproduces from the substrate (not just the
kernel): 2γ/κ at passive floor 2.327/1.037/4.576 and operating gain 5.318/2.371/10.459; memory
9.4/32.0; in-band 29.5/100 @ 2 GS/s and 14.8/50/222 @ 1 GS/s; n_ss 22.55/8.98; A1↔A2 max 2.1e-3.
Conventions correct (κᵢ=ω₀/2Qᵢ, κ_net=0.1κᵢ+2κ_ext, symmetric add-drop, ZOH/van-Loan, doublet =
single-direction eigenvalues duplicated at γ=0, test g). Cells C-1/C-2/C-3 + C-2-derate (Qᵢ≈3.4e6,
self-consistent) + P-CORN (passive) + γ/NF menus all present and correct.

**5. Anomaly audit.**
- **(A) μ(0)=0 cold-start — CONFIRMED, sharpen the mechanism (S31-F2).** The substance holds and it is
  the most consequential S0.4 item: with the bus driving ring 1 and μ=0, rings 2..N never see the task
  signal. **In the noiseless limit the gradient to their {δ_j, κ_ext,j} is *exactly* zero (7/7 at C-1,
  31/31 at C-2, verified).** But the Executor's wording "disconnected → zero gradient" is not literally
  what the as-built (ASE-on) substrate does: ASE populates every amplified ring, so rings 2..N carry a
  *nonzero but signal-free noise* gradient (CW energy ~4 orders below ring-1). That is arguably worse
  than zero — it is gradient *noise* with zero task-signal mean, which can destabilize rather than
  merely stall. **All four methods are signal-starved on rings 2..N** (SPSA's ± finite difference on a
  dark ring's δ is noise-dominated; the gradient methods see the zero-mean cross-term). The Executor's
  scoping is right: μ(0)=0 is the registered PR-2/PR-6 convention, the fix (a connected init) is PR-6's,
  and the substrate default correctly stays μ(0)=0. **Recommendation:** register a connected init at
  PR-6 (the sweep's 0.3κᵢ is a candidate) **or** register that the in-situ claim's trainability rests on
  a non-zero coupling init; and state the mechanism as signal-starvation, not literal disconnection.
- **(B) Damping confound — CONFIRMED (S31-F4).** At fixed 500-step budget the curve conflates accuracy
  with trainability (the convergence sub-check C-1/g_f=0.9: 0.41→0.46→0.50 at 400→800→1200 steps proves
  it). PR-12 is **not** cleanly freezable off this data — a convergence-controlled rerun (or a
  documented confound-aware selection) is required, as the Supervisor carried. **Additional finding:**
  the sweep's g_f axis *is* PR-4 §G's registered gain operating point (g_f=0.9 ⇔ κ_net=0.1κᵢ+2κ_ext);
  the curve makes g_f=0.9 the *lowest-accuracy* point at fixed budget, so a naive PR-12 pick (g_f≈0.3
  at C-1) would **contradict the signed PR-4 operating point.** The Supervisor must reconcile the
  PR-4/PR-12 relationship (does PR-12 refine PR-4 §G, or is PR-12 a different — δ-init/D-LinOSS-band —
  knob?) before PR-12 freezes.
- **(C) Seed variance — CONFIRMED.** C-1 points span σ up to 0.137 (g_f=0.9: 0.705±0.137) — these are
  the house-standard "high-variance configs" needing 8 seeds; the coarse sweep's 4 is fine for *informing*
  but the PR-12-candidate point must be re-run at 8 before the freeze. C-2 is tight (σ≤0.056).
- **(E) Token-hygiene — CONFIRMED, gate should be rewritten (S31-F5).** The real invariant holds: the
  source training stack (`equalization_multilayer`, `ManakovFiber`, `MRRWeightBank`, `MultiLayerEqualizer`,
  `ParallelPol`, `generate_dp_qpsk`, `viterbi_viterbi`, `compute_nmse_field`, `forward_batched`) is
  **genuinely absent** from `photonic_ssm/` code (the only matches are in SPSA *provenance comments*
  documenting what the salvage removed — stripped by the gate). But `test_no_equalization_coupling`
  asserts a *token* ("PAM4"/"PAM-4"/"QPSK"/"HD_FEC"/"ber_curve") that now collides with the
  *legitimately required* PR-2 T-A 4-PAM task, and the build renamed real vocabulary (`PAM_LEVELS`,
  `nearest_pam`) to keep it green. Transparent, but a smell: the gate no longer means what its name says,
  and the next contributor could re-add the source stack under a neutral name and the gate would miss it.
  **Fix:** rewrite the gate to assert the *source-stack symbols* (the module/class list above) are absent
  — the salvage-hygiene invariant that actually matters — and drop the generic task-framing tokens that
  collide with the project's own registered task. (`test_package_runtime_is_torch_only` is fine.)

**6. Cross-consistency — CONFIRMED.** PR-2 partition {δ,κ_ext,μ} with μ(0)=0 (mu_chain inits to zeros)
✓; F12 conventions inherited ✓. PR-13 k-grid vs memory @ 1 GS/s at the operating point reproduces PR-4
exactly: **C-1 4.7 samples → k∈{1,3}; C-2 16.0 → k≤10; C-3 70.5 → k≤30** ✓. PR-10 clocks {0.1,1,2}
parametric ✓. PR-11 forward/echo independence **supported but not enforced** (S31-F7). S0.1 reduction
(test b) bit-identical ✓. The T-A generator (`tasks/equalization.py`) is PR-2-faithful: the verbatim
10-tap Jaeger–Haas channel, u=q+0.036q²−0.011q³+ν, target d(n−2), the (−3,−1,1,3) levels, and the
PF-F9c centered-vs-causal invariant pinned in the docstring.

**7. Silently decided (beyond the gain-mode default).** (i) ASE covariance detached from the gradient
(S31-F6) — defensible and consistent, but un-registered; the freeze says "no detach in the *state* path"
and is silent on the noise-amplitude gradient. (ii) The sweep recipe (S31-F8) — batch 8, cosine LR,
grad-clip, μ-init 0.3κᵢ, δ-band 4κᵢ — un-registered and load-bearing for N=32 trainability; these are
PR-6's to freeze. (iii) The saturating-mode build-up uses the *passive* κ_tot (documented, to avoid the
g→P_circ→g circularity) — internally consistent and freeze-faithful (§G's ×260 is the passive value);
note only that it makes the saturating gradient a passive-build-up derivative. (iv) c_readout default
uniform (a buffer; the bake-off trains it digitally) — correct.

---

## The edits (Executor implements; Supervisor dispositions; Lucas confirms the S-F1 interpretation)

1. **(S31-F1) Flip the default** `gain_mode="fixed"` → `"saturating"` in `DissipativeRingSubstrate`.
   Keep `"fixed"` as a documented diagnostic/sensitivity mode (it is the γ=0-style floor for the gain
   channel). Register in PR-6 that **all four estimators use `gain_mode="saturating"`** so SPSA's
   forward passes and the gradient methods' backward passes target one function.
2. **(S31-F1/F2) Harden `test_h`:** (a) run the faithful mode; (b) assert the gain path is live —
   autograd `dκ_net/dκ_ext ≠ 2` in saturating mode (or saturating κ_ext-grad ≠ fixed κ_ext-grad on the
   same loss); (c) add a **connected-init** variant (nonzero μ) so the gate actually exercises rings
   2..N — without it, even the hardened test only proves ring-1's gain path.
3. **(S31-F3) Surface the intracavity reachability** in the addendum verdict: report
   `g0_required_intracavity_dB_per_cm` (already in the JSON: C-2 ≈ 380 dB/cm) beside the bus number, and
   state that on the plane the gain model uses, C-2/C-3 are material-aspirational too — strengthening,
   not weakening, anchor-risk (v). (No freeze change; the freeze chose the bus plane knowingly.)
4. **(S31-F4) PR-12:** convergence-controlled rerun + 8 seeds at the candidate point; Supervisor
   reconciles PR-4 §G g_f=0.9 vs the damping-curve optimum before PR-12 freezes.
5. **(S31-F5) Rewrite `test_no_equalization_coupling`** to assert the source-stack symbol list absent;
   drop the generic task-token bans (PAM4/PAM-4/QPSK/HD_FEC/ber_curve). Then the neutral renames are
   unnecessary and the gate tests the real invariant.
6. **(S31-F6/F7/F8) Register the conventions:** ASE-covariance-detached-from-gradient as the intended
   noise model; PR-11 generator-distinctness as an S0.4 RHEL requirement; the sweep recipe + connected
   init as PR-6 freeze items.

## The line for Lucas

**APPROVE-WITH-EDITS.** The substrate is a correct, freeze-faithful implementation — the passive limit,
every registered number, the calibration, and the gradient plumbing all check out independently, and the
Executor's self-flagging is exemplary. **S-F1 is confirmed and is the one that matters:** the default
`gain_mode="fixed"` silently drops the gain's κ_ext-dependence (27% of the κ_net gradient at the
operating point, 6× and sign-flipped at the trainable edge), and `test_h` is hollow on that path — so
the F18 gate green-lights a substrate that, as-defaulted, would have SPSA and the gradient methods
training subtly different functions in the S0.5 bake-off. The fix needs **no freeze change** (the
saturating mode the freeze already mandates exists and trains): flip the default, harden the gate,
register the mode for all estimators. The one thing to **confirm** (not reinterpret) when you accept the
edit is that consequence — saturating gain is the registered bake-off mode for all four methods.
Alongside it, weight **S31-F2** (μ(0)=0 leaves the N=32 headline cell untrainable from cold — the top
S0.4 risk, correctly PR-6-scoped) and note **S31-F3** (the gain's own intracavity plane makes the
reachability materially more aspirational than the ×32 headline). With these applied, the build is sound
to carry into S0.4.
