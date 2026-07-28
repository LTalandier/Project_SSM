# Task Queue

Supervisor assigns tasks here. The Executor reads and executes the task marked **ACTIVE**, then
**stops and waits**. The Supervisor marks a task **COMPLETED** (date + one-line summary) before
assigning the next. New tasks go at the top, below this header.

Task format: see `.claude/skills/executor/SKILL.md`.

---

## ✅ DONE — S0.10 (2026-07-28, PR-17 + §17.7 erratum): **eval-F fine floor (99,840 symbols) + T-A-L transfer.** (1) **Mismatch tie statistically CLEAN at all 5–30%** (ratio ≤1.05, all CIs incl 0 — coarse "real differences" were floor artifacts); (2) **DRIFT ADVANTAGE FORMALLY DECLARED: independent-regime 2.42× CI excl 0 clears the frozen 2× bar** (coarse 1.84× co-reported; common 1.34× none); (3) ceiling-fine 9.8e-4 (coarse 5.2e-4 lucky-floor); (4) diag-fine M-par +18% resolved, rhel-ideal thin-margin pass; (5) **T-A-L registered prediction FAILED** (heavy-damping optimum robust to ×2 span; 30% rule not fired — reported as failure). Scale-convention erratum caught same-day, registered pre-rerun, gate-tested. 320 units total ≈€2.3, servers deleted. §5.1/5.5/5.6/6/1.3/8.5 + abstract + F6/F8/S2 updated.

## ✅ DONE — P1 finalization (2026-07-27): **figures F8+S1/S2/S3/S5 made** (`analysis/make_sfigures.py`) + captions (`paper/figure_captions.md`) · **manuscript assembled** (`analysis/build_manuscript.py` → `paper/p1_manuscript.md`, numbered bib, 35 refs) · **4 registered page reads PERFORMED: Wu eLight REFUTED → scope re-ruled W1-only** (E-2026-07-27-1; §1.1/abstract/§5.5 re-scoped; Wu = nearest neighbor cited loudly) · **fresh sweep: no new attack** (Zhang eLight 6:6 = new nearest miss, PSO-cleared, read registered; Zhao×Wu merge watch) · **S0.7 exclusions ledger primary-sourced** (`docs/s0_7/exclusions_ledger.md`; §7.1 integrated-class ~0.5–1 W consequence stated). Remaining pre-submission: Zhang read, final sweep re-run, UNVERIFIED-direct re-checks, venue/LaTeX formatting. P2 send = Lucas.

## ✅ DONE — P1 PI rulings (2026-07-26, delegated — Lucas: "you can chose the title and W0/W1"): **title = candidate 1** (question form, recorded CHOSEN in `paper/outline.md`) · **white-space scope = W0-in-prose + W1-core-sentence** (§1.1 ▢ removed; abstract + §1.3 refreshed to post-S0.9 §5.5). E-2026-07-12-1 RESOLVED — **P1 has no open PI gates**; remaining items non-PI (S-figs, venue formatting, final refresh sweep + 4 page reads, S0.7 exclusions ledger). P2 send still Lucas's physical action.

## ✅ DONE — S0.9 (2026-07-24): **mismatch tie ROBUST to 30% (stronger null); drift produces a real sub-2× in-situ edge specific to UNCORRELATED drift a re-lock can't catch (1.84×, CI excludes 0; ~3–4× at peak drift)** — no formal 2× advantage declared, but the advantage case is now directional + mechanism-identified. §5.5 upgraded. See `results/s0_9/s0_9.md` + results_log. ≈€0.75 cloud, servers deleted.

*(Spec below retained as executed — PR-5 §E + PR-16 pre-registered `45a5e13`, σ_step addendum `§16.7`, margins ratified 2026-07-24.)*

## (executed) — S0.9: break (or confirm) the offline-tie null (2026-07-22, single-session mode)

**Origin:** Lucas 2026-07-22 "go with (1) and (2)" — the two highest-leverage moves from the
recommendation ladder for turning the §5.5 offline-tie null into either a demonstrated in-situ
advantage or a stronger, more surprising null. Both **pre-registered before any run** (specs
committed this turn: PR-5 §E + PR-16). Skips ladder item (3) foundry-PDK (Stage-1).

**S0.9a — mismatch-sensitivity sweep (PR-5 §E).** Sweep the M-par calibration/actuation level
m ∈ {1,2,3,4,6} (5–30 %-class); in-situ PAT-both vs offline-deploy, C-2, 8 seeds, same budget.
Deliverable: SER-vs-mismatch curve + the crossover m* where offline degrades ≥2× past in-situ
(CI excludes 0), or the registered stronger-null if none. Reuses substrate/harness + a small
level-scaled runner. Cheap.

**S0.9b — drift model + deploy-then-drift (PR-16).** Literature-sourced drift (341 MHz/24h RW =
σ(24h)≈24κᵢ on δ; `docs/s0_L/drift_research_2026-07-22.md`). New: `drift_schedule` substrate
capability + `deploy-then-drift` harness protocol + gate tests. Both correlation regimes
(common-mode / independent), both offline variants (head-recal / +global re-lock), {PAT,SPSA}
in-situ, K=12 steps. Deliverable: SER(k) trajectories + per-regime advantage verdict. S0.6-scale
cloud sweep.

**Path:** specs committed → build S0.9a runner + S0.9b drift model/harness/tests → local smoke →
**surface pre-registered margins to Lucas to ratify (escalation-sensitive)** → cloud runs →
results → §5.5 upgrade (curve + drift result) or stronger-null. **Cost:** few € cloud.
**NOT in scope:** foundry-PDK co-sim; method-symmetric physics; Er-gain/heater drift terms
(literature gaps, flagged unquantified).

---

## ✅ DONE — S0.8: P1 manuscript assembly core (2026-07-12, same day): **figures F1–F7 ALL MADE** (`paper/figures/`, generator `analysis/make_figures.py`) · **§5.7/5.8 drafted** (controllability first-class; PR-14 honest deferral) · **citation sweep DONE** (`paper/references.md`, 30+ keys, 4 page-level verifications — EdgeDRNN >100× VERIFIED verbatim [cite JETCAS arXiv:2012.13600 not 1912.12193]; Er:SiN measured NF ≈7 dB CONFIRMS frozen NF-A [debt-#3 rewritten to the S0.3-0-accurate history]; SiN-FWM γ: our 0.97 optimistic vs measured ULL 0.29–0.51 → disclosed in §4, direction favors RHEL conclusion; SUBTRACTIVE splitting = separations 180–320 MHz, 2γ convention now stated in §2) · **white-space refresh DONE** (`docs/s0_L/whitespace_refresh_2026-07-12.md`: **W1 clean, W0 survives**; Wu eLight = inference-only CLEAR, Zhao LPR = feedforward CLEAR; 5 near-misses dispatched by name in §1.1; 4 pre-submission page reads registered) · **abstract ▢-FILLED** · `paper/supplementary.md` (provenance commit table + repro statement). Remaining: Lucas rulings (title, W0-vs-W1) → E-2026-07-12-1; S-figs; venue formatting; final refresh sweep.

*(Spec below retained as executed.)*

## (executed spec) — S0.8: P1 manuscript assembly (2026-07-12, single-session mode)

**Goal:** assemble the P1 manuscript from the nine drafted sections. No new runs; no gates
consumed. Directed by Lucas 2026-07-12 ("figures F1–F7, the §5.7/5.8 stubs, citation sweep,
white-space refresh").

**Scope:**
- **(a) §5.7/§5.8** — expand from the S0.4-0 record (`results/s0_4_0/s0_4_0_calibration.json`);
  §5.8 = the honest PR-14-deferred paragraph (registered S0.5-full residue, no data invented).
- **(b) Figures F1–F7** — `analysis/make_figures.py` → `paper/figures/F*.{png,pdf}`, all from
  frozen result JSONs (s0_1 pole region · s0_4_0 calibration · s0_5 bakeoff+runs · s0_6 damping ·
  s0_7 envelopes). Figures are committed (paper assets); `results/` stays gitignored.
- **(c) Citation sweep** — resolve every `[CITE-*]` key into `paper/references.md` with a
  per-entry verification status; **page-level verifications** for the load-bearing four:
  EdgeDRNN >100× batch-1 deflator (arXiv:1912.12193), SiN-FWM chain numbers (PR-11 ⚠verify-2..6),
  RHEL semantics quotes (arXiv:2506.05259), Cui-2023 Q anchor. Web-agent sourced, cross-checked.
- **(d) White-space refresh** — re-run the PR-15 two-modality search dated 2026-07-12 →
  `docs/s0_L/whitespace_refresh_2026-07-12.md`; specifically re-audit the Wu-eLight and Zhao-LPR
  exposures and any 2025–26 newcomers. **W0-vs-W1 stays Lucas's ruling** — this task only
  refreshes the evidence under it.
- **(e) Assembly residue** — abstract ▢-fill from landed gates; `paper/supplementary.md`
  (pre-registration ledger pointer + F8 + phase→commit-hash table + mixed-platform repro
  statement); outline claim/figure statuses updated.

**NOT in scope:** title pick + W0-vs-W1 (Lucas rulings, flagged at close); S0.5-full residue
rows; P2 send (Lucas's physical action). **Cost:** web retrievals + local matplotlib, $0.

---

## ✅ DONE — S0.7-full-core (2026-07-08, same day): **training-energy metric INVERTS the device-pass rank (SPSA 2.6 mJ all-in vs PAT ~13–44 J digital-dominated); RHEL pump ×42 its conversion; EdgeDRNN >100× batch-1 deflator resolves the lite's case-threatening retrieval favorably**; §7 drafted. See `results/s0_7/training_envelope.md`. Remaining full-S0.7 items (registered → S0.8 list): exclusions ledger, page-level cite verification.

*(Spec below retained as executed — pre-registered at `bd37703`.)*

**Scope (registered):** S0.7-lite (PR-10 🔒, conditional-positive) stands as the inference
envelope; this task adds **(a)** the per-method TRAINING-mode energy envelope from the S0.5
measured passes-to-target + the S0.4 method adders (4-tap drive E/O; adjoint error-injection;
RHEL 2×N-arm pump 9.6 W/echo; PAT digital-twin ledger 505,600 digital passes — FLOP-costed at
the named F16 accelerator classes), computed at both PR-10 corners; **(b)** the lite's single
most case-threatening retrieval (a measured *sustained* embedded-GPU number on a matched
streaming workload — lite finding 5); **(c)** §7 draft. **Registered accounting rules (before
computing):** per-sample conversion stack = the lite's frozen per-sample envelopes (cited, not
re-derived); pass duration = T/f_s; digital FLOPs/pass estimated from the 2N-dim ZOH matvec
(formula in-script, order-of-magnitude honesty class, labelled); the four lite exclusions
(laser wall-plug, locking, control compute, packaging) remain UNBUDGETED here with the lite's
only-shrinks-positive-cells direction statement — their primary-sourced ledger = a named S0.8
retrieval item, not silently absorbed. **Deliverables:** `analysis/s0_7_training_envelope.py`
→ `results/s0_7/training_envelope.{json,md}` · §7 draft · trackers. **Cost:** arithmetic + 1
web retrieval, $0.

---

## ✅ DONE — S0.6: damping characterization (2026-07-08, same day) — **×302 spread, optimum r*=2.0 deep overcoupling; R-ii CONFIRMED (boxed training finds it, 0.0005 = ceiling, beats best pin)**; see results_log + `results/s0_6/damping.md`; §6 drafted. Next: S0.7-full envelope → S0.8 assembly.

*(Spec below retained as executed — pre-registered at `5a7f28b`.)*

**Goal:** the accuracy-vs-damping curve under the signed R-ii framing — damping = the trainable
per-ring net loss κ_net(κ_ext) at **fixed g_rt = 0.9κᵢ** — convergence-controlled (the S0.3-1
anomaly-B fix), BPTT-reference diagnostic (never a bake-off contest; estimator-independence
rides S0.5's methods≈BPTT result). Corrects the S0.3-1 coarse sweep's illegal g_f axis.

**Design (registered):** two arms × 6-point grid × 8 seeds {11,23,47,61,83,101,127,151}, C-2
headline, BPTT, U_max = 12000, eval/100 (identical PR-3 §A protocol: final = median-last-3;
plateau required — non-plateaued runs flagged, not silently included):
- **Arm B ("pinned"; the classic operating-point curve):** κ_ext FROZEN at
  r_pin ∈ {0.2, 0.3, 0.5, 1.0, 2.0, 3.0}; only {δ, μ} train. Reads: does the damping *value*
  matter when it is a fixed design choice?
- **Arm A ("boxed"; the R-ii trainable-range curve):** full P2 partition, clamp sub-box
  [r_min, r_hi] with r_hi ∈ {0.2, 0.3, 0.5, 1.0, 2.0, 3.0}; init r₀ = √(r_min·r_hi)
  (registered formula, in-box by construction). Reads: does trainable κ_ext *find* the good
  operating point within a given range — i.e., is damping a knob training absorbs (R-ii's
  claim) or a choice the designer must make?
- **C7 evaluation rule (registered):** (i) the pinned curve's spread = the damping stakes
  (max/min median SER across r_pin); (ii) R-ii is CONFIRMED if every arm-A box whose span
  contains the arm-B optimum reaches within the PR-3 margin factor (1.25×+0.005 absolute) of
  the best pinned point — else the operating point must be designed, not trained (recorded
  either way; feeds §6 + PR-12 closure).
- Baseline context row: the S0.5 ceiling (full box [r_min, 3], r₀ = 0.3) is arm-A-adjacent
  and reused, not rerun.

**Deliverables:** `analysis/s0_6_run_one.py` + cloud manifests · `results/s0_6/{runs/,
damping.json,damping.md}` · results_log entry · §6 draft. **Cost:** 96 units ≈ 3,600 unit-min
on 4× Hetzner cpx51 (~32 workers, OMP=2) ≈ **~2 h wall, <€1**; mixed-platform disclosure as
S0.5.

---

## ✅ DONE — S0.4-close + S0.5-core: **Gate ii PASS (both ii-a ×21.5 & ii-b via PAT-both AND SPSA 8/8)** — the headline Stage-0 trainability result is in-data (2026-07-07, same day). Rank PAT<adjoint<SPSA, RHEL censored (template B); no promotion → PAT/SPSA hardware roadmap; **offline-deploy ties in-situ PAT at 5% mismatch (advantage-vs-offline NOT in-data — F7.3 working as designed).** See results_log + `results/s0_5/bakeoff.md`. Next: S0.6 damping → S0.7-full envelope → S0.8 paper (§3 substrate + §4 results now writable).

*(Spec below retained as executed — PR-3/8/9 frozen `ae16f6d`, sizing `7bcbcb9`, ceiling `4fca58d`, all before the runs.)*

**Governing freezes (committed with this spec, BEFORE the pilot):** PR-3 rule 🔒 · PR-8 🔒 ·
PR-9 🔒 (ledger blocks). Sequence + deliverables:

1. **Sizing pilot (seed 7, excluded from the 8):** BPTT at C-2, U = 3000 updates, eval every
   100 → U_conv = the plateau point (first eval after which no >1 % relative median-of-3
   improvement occurs). Sets **U_max = ceil(1.5 × U_conv, to the nearest 500)** and
   **B = 2 × U_conv × 16 passes** (PR-8 §C). Numbers → the S0.4-close addendum, committed
   BEFORE any estimator run at C-2.
2. **Ceiling (PR-3 §A):** BPTT × 8 seeds at C-2 (U_max, eval/100); + fixed-gain 3-seed spot →
   Δ_M3. C-1 secondary ceiling (8 seeds, same protocol). Ceiling SER (median + IQR) → the
   addendum; **SER_target derives mechanically** (1.25× + 0.005).
3. **F8 per-method hardware-requirements ledger** → `docs/s0_4/f8_hardware_ledger.md`
   (observables · actuators · added components + loss · calibration burden · per-method E/O
   channel count for the envelope).
4. **The gated bake-off (S0.5-core):** ranked arms {pat-both, spsa, adjoint, rhel} + baselines
   {head-only, offline-deploy} × 8 seeds at C-2 under budget B (per-method update counts per
   PR-8 §C conversion); C-1 diagnostic tier (pat families + rhel-ideal, 3 seeds).
   → `results/s0_5/bakeoff.{json,md}`: PR-8 stats (success fractions, censored medians,
   paired-bootstrap CIs), Gate ii-a/ii-b verdicts, R3b-rule differentials, both ledgers
   per arm, M3-trigger check, F22 template re-derivation.
5. Results-log entry + ledger addendum + trackers. **NOT in scope (registered):** the S0.5-full
   loss/gain/ASE sweeps, PR-13 secondary task, PR-14 bias/variance diagnostic, the genuine
   equal-budget HP search (S0.5-full tier, after this core lands).

**Expected runtime:** pilot ~3 min · ceilings ~30 min · bake-off ~2–4 h CPU background · $0.

---

## ✅ DONE — S0.4c: RHEL + honest echo sub-model built; R1/R2/R4/R5 PASS (2026-07-07, same day) — see results_log + `results/s0_4c/smoke.md`; 150/150. **Key finding: RHEL ≡ head-only at the registered cell even with idealized echo (dissipative-echo bias binding); R3b template rule mislabels → PR-9 protocol note.** All four estimators now built. Next: S0.4-close (PR-3 ceiling + F8 ledger) → S0.5 freeze (PR-8/9) → the gated bake-off.

*(Spec below retained as executed — pre-registered at `5ca8d52` before the build/run.)*

**Goal:** the fourth estimator — RHEL per Pourcel & Ernoult arXiv:2506.05259 (semantics verified
2026-07-07, PR-11 ⚠verify-1) — on the shared substrate with the **honest echo sub-model**
(PR-11: no idealized conjugation operator). Sim-only; §5.2 guardrail; RHEL-on-SiN framed
"odds-improved, not feasibility-reopened".

**PR-11 numeric freeze (mechanism A headline — recon `docs/s0_4/pr11_echo_submodel_recon.md`):**
- η_c,j = η_ex,j² · η_spiral · e^(−κ_net,j·τ_c) per ring j, computed **live** from the
  commanded parameters: η_ex,j = 2κ_ext,j/κ_net,j (mode-dependent for free);
  η_spiral = (γ_nl P_p L)² with **γ_nl = 0.97 W⁻¹m⁻¹** (n₂ = 2.4×10⁻¹⁹ m²/W, A_eff = 1 µm²;
  class-consistent with the OL 40,875 (2015) CW low-loss-SiN conversion demo + γ = 1.19 W⁻¹m⁻¹
  in Photonics 8,161), **P_p = 0.3 W/arm**, **L = 0.5 m**; **τ_c = τ_net** (per-cell mean).
- φ_err = 0 headline; ±π/20 = an ungated sensitivity row (S0.5).
- n_conj = √(1+η_c)·v with ⟨|v|²⟩ = 1 photon (conservative one-photon-per-mode convention;
  the phase-insensitive parametric floor b = √η a* + √(1+η)v — expect **negligible** at the
  ~1e8-photon state scale; measure + record the ratio). Pump-RIN excess: −145 dBc/Hz class
  over the state band (⚠cite at S0.8) — expect negligible; measure + record.
- **C_op fires once per echo pass** (independent draws) — twice per update.
- **N-arm pump (N × 0.3 W) + the error-injection E/O channels → S0.7 envelope rows** (the
  S0.4-0 multi-tap precedent).

**RHEL estimator (registered semantics, from the verified paper):**
- Forward (device, fresh ASE tag): drive u(0..T), measure y (head/loss/SER on this), store
  a(T) conceptually — *operationally each echo needs its own forward* (below).
- **C_op** on a(T) (frozen chain above), then **echo pass** (device, fresh ASE tag): the SAME
  dissipative dynamics (no loss-sign flip) from the conjugated state, **drive replayed
  time-reversed**, with the **continuous nudge force ∓iε·∂ℓ/∂a\*** injected per step
  (ε_frac = 0.05 of the state-RMS scale, smoke value; equal-HP search at S0.5).
- **Registered sim simplification (nudge):** ℓ(t) = the instantaneous per-step loss
  (ŷ_k − d_k)² with the head's lag buffer treated as frozen context (m=0 term differentiated) —
  the FIR head makes the true loss non-instantaneous; RHEL's theorem wants ℓ(Φ(t),t). The R1
  floor check compares against BPTT **of this same truncated functional** (apples-to-apples);
  the bake-off judges task loss/SER as for every method.
- **Update rule:** Δθ ∝ −(1/2ε)·Σ_k dt·(∇_θH_coh[Φᵉ(t_k,+ε)] − ∇_θH_coh[Φᵉ(t_k,−ε)]), with
  H_coh the **coherent generator only** (δ|a|² + μ couplings + the √(2κ_ext) drive coupling).
  **Registered structural limitation:** κ_ext's *dissipative* channel (the 2κ_ext decay) is
  invisible to ∇H_coh — RHEL trains κ_ext only through the drive-coupling term. A measured
  bake-off property, not a bug.
- **Pass accounting (PR-7.1 extension, registered in the ledger):** on a dissipative substrate
  the paper's 3-pass chaining (Hamiltonian re-traversal) is unavailable and state cloning is
  unphysical → **operational count = 2 forward + 2 echo = 4 device passes/update** (headline;
  the split-state 3-pass variant — 3 dB + vacuum on both echoes — noted, not run). Digital = 0.

**Pre-registered gates (BEFORE the runs):**
- **R1 (floor check, operational form — refines PR-11 §D to the theorem's validity domain):**
  RHEL's theorem is stated for **non-dissipative** systems, so the floor check runs a
  **dissipation sequence**: C-1 variant, gain 0, loss_scale ∈ {1.0, 0.1, 0.01}, r = 0.1, short
  T = 32, C_op ideal (η_c = 1, n_conj = 0, φ_err = 0), ASE off, ε_frac = 0.01. Gate:
  |cosine(Δθ_RHEL, ∇θ_BPTT-of-truncated-loss)| ≥ 0.9 at the least-dissipative point AND
  monotone improvement with decreasing dissipation. (Sign convention resolved empirically at
  the first point and recorded.)
- **R2 (PR-11 invariant-4 unit test):** the echo of a noisy forward does NOT recover the
  noiseless initial state — recovery error ≥ the (1−fidelity)+ASE floor bound; test-enforced.
- **R3a (mechanics trainability):** with C_op **idealized** (η_c=1, n_conj=0) at C-1/N=8,
  28 dB: RHEL cuts T-A MSE ≥20 % within ≤300 updates on ≥2/3 seeds {11,23,47} (tests the
  estimator mechanics, not the echo physics).
- **R3b (honest-echo smoke, report-only):** same runs at the **frozen** penalty chain — the
  outcome selects which F22 template the data currently favors (recorded; S0.5 owns the gated
  verdict either way).
- **R4 (PR-7.1 ledger):** 4×batch device passes/update exactly; digital 0 — test-enforced.
- **R5 (invariants 1–3):** fresh independent ASE/conjugation streams per pass; echo κ_net > 0
  (no loss-sign flip); gain ASE present in echo passes — test-enforced.

**F22 conclusion templates (pre-drafted, per roadmap S0.4-close):**
- **Template A (RHEL-competitive):** "Under the registered echo sub-model (η_c ≈ −18 dB chain,
  PR-11), RHEL trains to within the PR-3 margin at ≤ [X]× the PAT/SPSA device-pass cost; its
  4-pass updates and N-arm pump ([N×0.3] W) remain the hardware barrier (F8/envelope)."
- **Template B (RHEL-fails-under-honest-echo):** "Under the registered echo sub-model, RHEL
  [does not reach target / needs [X]× the passes] at the registered cell; the decomposition
  attributes the gap to [η_c attenuation / conjugation noise / dissipative-echo bias /
  κ_ext-channel invisibility]; the idealized-C_op control (R3a) confirms the mechanics train,
  isolating the echo physics as the binding constraint. RHEL-on-SiN stays sim-only."

**Deliverables:** `photonic_ssm/estimators/rhel.py` (C_op + H_coh + estimator) + harness
methods (`rhel`, `rhel-ideal`) + `tests/test_s0_4c.py` + `analysis/s0_4c_smoke.py` +
`results/s0_4c/smoke.{json,md}` + results_log entry + PR-7.1 extension in the ledger.
Expected runtime: ~5 min CPU, $0.

---

## ✅ DONE — S0.4b: recurrent in-situ adjoint built; gates B1–B5 ALL PASS (2026-07-07, same day) — see results_log + `results/s0_4b/smoke.md`; 144/144. Adjoint ≈ BPTT-grade at SPSA's device cost; C-2 gain-channel cosine 0.925 → S0.5 flag. Next: PR-11 draft → S0.4c (RHEL) → S0.5 freeze.

*(Spec below retained as executed — pre-registered at `c85fe62` before the build/run.)*

**Goal:** the third estimator — the recurrent in-situ adjoint (Hughes/Fan/Pai lineage,
time-domain/cavity extension per roadmap S0.4b) — built on the shared substrate and the S0.4a
harness under the signed PR-6 contract, cost-accounted per the signed PR-7 row
(**1 forward + 1 adjoint = 2 device passes/update; digital side-ledger = 0**). Sim-only:
the §5.2 guardrail keeps hardware on PAT/SPSA; PR-7's registered realizability caveat applies
(the count charges the adjoint pass *as if* realizable; debt #4 is the separate hardware question).

**Registered simulation model (the design decisions, recorded BEFORE the build):**
- **Pass 1 (device):** physical forward, registered ASE, fresh generator (tag `fwd`), no autograd —
  a measurement. The error signal e = ∂L/∂y at the *measured* y_phys is computed digitally
  (uncharged, same convention as SPSA's digital loss evals).
- **Pass 2 (device):** the physical adjoint pass, simulated as autodiff through a **fresh-ASE
  replay of the device itself** — same commanded parameters (it IS the device: no twin, no PR-5
  mismatch), **gain frozen at its operating-point saturated value** (`detach_gain`: the
  counter-propagating adjoint field sees the medium's saturation state; it cannot implement the
  ∂g/∂P̄(κ_ext) self-consistency Jacobian channel — the S31-F1 channel is structurally absent from
  a physical adjoint, as it is from the M-struct twin, but here frozen at the *correct saturated
  value*, not the fixed-plane value), **fresh ASE (tag `adj`)** — PR-11 irreversibility invariant:
  no common-RNG reversal; the adjoint pass is its own noisy device pass (roadmap S0.4b verbatim).
  Estimator identity y_adj = y_phys + (y_replay − detach(y_replay)); backward = the exact adjoint
  recursion of the (frozen-gain, adj-ASE-realization) linearization applied to the physical error.
  The replay + its autodiff backward together simulate ONE physical adjoint pass (the gradient is
  physically read out by forward/adjoint-field interference, Hughes-Fan; that readout's hardware
  burden goes to the F8 per-method ledger at S0.4-close, not the pass count).
- **Registered sim-model limitations (disclosed, both flattering to adjoint):** (i) ASE enters
  through the replay *trajectory* (the linearization point), not additionally as an additive term
  on the adjoint field itself — the additive-λ channel needs an error-launch power convention that
  is unresolved hardware design (debt #4); (ii) non-reciprocity of the gain medium and the
  CW/CCW-doublet interaction of a counter-propagating adjoint field are handled *in-model* by the
  exact 2N×2N adjoint (autograd) — their hardware separability is an F8-ledger item. The bake-off
  adjoint arm is therefore an **optimistic bound**; the paper must say so.
- Harness integration: method `"adjoint"` in the S0.4a `train()` loop — identical θ₀/data/head
  cadence/clamp conventions (PR-6); ASE tags distinct from all other methods' tags.

**Pre-registered gates (BEFORE the runs):**
- **B1 (structural floor — the roadmap S0.4-gate floor check):** on the fixed-gain plane
  (`gain_mode="fixed"`), ASE off in both passes → adjoint gradient ≡ BPTT gradient (cosine
  ≥ 1 − 10⁻⁹, allclose rtol 10⁻⁸), test-enforced. (In this limit the replay is bit-identical to
  the forward and detach_gain is inert — they are the same computation by construction.)
- **B2 (saturating-noiseless diagnostic, report-only):** `saturating` mode, ASE off → cosine
  (adjoint vs full BPTT) at θ₀, C-1/N=8 and C-2/N=32. **Registered expectation: ≥ 0.9** (the
  dropped ∂g/∂κ_ext channel was ≈free for M-struct at smoke scale). A miss is a *finding* about
  adjoint-vs-saturation (recorded, investigated), not a build failure.
- **B3 (trainability smoke, mirrors S2 exactly):** adjoint cuts T-A MSE ≥20 % within ≤300 updates
  at C-1/N=8, 28 dB, on ≥2 of 3 seeds {11,23,47}; same operationalization (init = mean loss[0:5],
  final = mean loss[−20:]).
- **B4 (PR-7 ledger):** device passes = 2×batch×updates exactly; digital = 0 — test-enforced.
- **B5 (value invariance):** `detach_gain=True` changes NO forward value (bit-identical
  trajectories; only gradients differ) — test-enforced.
- C-2/N=32 spot run (1 seed × 100 updates, adjoint) reported, ungated (extends the S0.4a
  sizing-flag row).

**Deliverables:** `photonic_ssm/estimators/adjoint.py` + `detach_gain` substrate flag +
harness method + `tests/test_s0_4b.py` + `analysis/s0_4b_smoke.py` +
`results/s0_4b/smoke.{json,md}` + results_log entry. Expected runtime: ~2 min CPU, $0.

---

## ✅ DONE — S0.4a phase 1: PAT + SPSA built; smoke gates S1/S2/S3 ALL PASS (2026-07-07, same day) — see results_log + `results/s0_4a/smoke.md`; 138/138. Next: S0.4b/c (adjoint + RHEL, sim-only) → S0.5 freeze (PR-8/9 + PR-3 rule) → the gated bake-off.

*(Spec below retained as executed — the PR-5 levels frozen here now govern all S0.4/S0.5 PAT runs.)*

**Goal:** working PAT + SPSA (+ the PR-3 BPTT reference) on the shared substrate under the signed
PR-6 contract, with the PR-5 twin-mismatch machinery decomposed per family. Phase 1 = build +
smoke; the gated 8-seed to-target bake-off is S0.5 (PR-8/9 freeze first).

**PR-5 numeric levels — FROZEN HERE (from the recon menu, before any PAT run):**
- **M-par (L2 headline):** multiplicative errors on the twin's fixed constants + actuation maps —
  κᵢ +5 % · γ +5 % · κ_ext-actuation ×1.05 · μ-actuation ×0.95 · δ-offset +0.05κᵢ per ring (fixed
  signs = worst-case-coherent systematic calibration error; per-seed random signs = S0.5
  sensitivity row) · gain pair g-factor ×1.10, P_sat ×0.75 (the loose debt-#3 bracket).
- **M-struct:** twin runs `gain_mode="fixed"` (drops ∂g/∂κ_ext — the S31-F1 channel), true params.
- **Both:** M-par + M-struct. **Perfect twin:** exact copy (diagnostic only, per PR-5 v2).
- **M-noise (always on):** twin is noiseless; the substrate runs registered ASE (NF-A 7.0).
- Decomposed reporting {M-par / M-struct / both / perfect} per PR-5 v2 — never conflated.

**Registered S0.4a run conventions (smoke-scale; PR-8 re-freezes statistics at S0.5):**
- Model = frozen PR-2 architecture: **fixed** affine encoder (u ∈ [−6,6] → P ∈ [0, P_pk],
  T-A P_pk = 2P̄₀, E₀ scale = 1 at θ₀ per §N) → substrate (resolved B = taps {3,12,21,30},
  connected init μ_c = 0.3κᵢ, δ-init [−κᵢ,κᵢ], r₀ = 0.3) → R2 intensity (c_readout fixed uniform
  in phase 1) → digital linear head over {y(n−m), m=0..7}, trained by Adam on the *measured* y
  (identical cadence/budget for every method — one head step per update). **Registered
  simplifications (identical for all methods, strictly less digital freedom — conservative):**
  fixed encoder + fixed c_readout; revisit at S0.5 only by re-registration.
- Sequences: T=256 symbols @ 2 GS/s, batch 8 (= 8 device passes per forward eval, PR-7 §C),
  headline 28 dB, warmup 16 skipped in loss + SER. In-situ partition {δ, κ_ext, μ} per P2;
  clamp = the operative band [0.1606, 3] (S0.4-0).
- Cost ledger (PR-7): SPSA 2×batch device passes/update; PAT 1×batch; BPTT reference = 0 device
  (digital ledger only, reserved as the PR-3 ceiling).

**Pre-registered smoke gates (phase-1 pass/fail, BEFORE the runs):**
- **S1 (PAT correctness):** perfect-twin PAT gradient ≡ BPTT-through-twin gradient — cosine
  ≥ 1 − 10⁻⁹ on a noiseless probe (they are the same computation by construction).
- **S2 (trainability):** each of {BPTT, PAT×{perfect, M-par, M-struct, both}, SPSA} reduces T-A
  MSE by ≥20 % of its initial value within ≤300 updates at C-1/N=8, 28 dB, ≥2 of 3 seeds.
  (Modest by design — this is "the estimators train at all", NOT Gate ii.)
- **S3 (ledger):** device/digital pass counts match the PR-7 table exactly.
- C-2/N=32 spot run (1 seed, BPTT + PAT-both + SPSA) reported, ungated (context for S0.5 sizing).

**Deliverables:** `photonic_ssm/estimators/{pat.py,harness.py}` + `tests/test_s0_4a.py` +
`analysis/s0_4a_smoke.py` + `results/s0_4a/smoke.{json,md}` + results_log entry.

---

## ✅ DONE — S0.4-0: calibration + PR-5 recon (2026-07-07, single-session mode) — **resolved B {3,12,21,30} (gate PASSES, no fallback) · r_min 0.1606 frozen · addendum in ledger · 132/132**

> **Completed same day it went ACTIVE.** All 5 items discharged; see the S0.4-0 entry in
> `results_log.md` + the 🔒 calibration addendum in `preregistration.md` (PR-6 §G block) +
> `results/s0_4_0/s0_4_0_calibration.md`. Highlights: B = {3,12,21,30} K=4, every-ring gate PASSES
> robustly (fallback (c) not triggered; registered seed was not the winner — search protocol worked);
> r_min = 0.1606 cell-independent, clamp code-enforced; ×37-vs-×91 moot (measured ×0.42,
> doublet-quenched; M1 check PASSED with measured factors); anchor-risk (vii) quantified (δ-aware
> floor would be 0.2547 → F19); multi-tap E₀ invariant (encoder unchanged); PR-5 menu written
> (`docs/s0_4/pr5_twin_mismatch_recon.md`; levels freeze at the S0.4a spec). Two single-session
> protocol rulings recorded in the addendum (gate-reference = max ring; min-over-5-seeds
> robustness) — both strengthen the gate; flagged for Lucas's review.
> **Next: S0.4a (PAT + SPSA estimator builds + twin-mismatch runs) — spec to be written.**

> *(Original mode-change note, retained: Lucas 2026-07-07 "don't use the critic for now on do
> everything" → Critic suspended, main session absorbs Executor work; packet v3 🔒 SIGNED by
> delegation, E-2026-07-05-1 resolution.)*

> **Update 2026-07-05:** the max-effort Critic pass (`critic_review_s0_4_freeze.md`, updated in place)
> kept AMEND and sharpened both HIGHs: **P6-F1 → capacity finding** (C-2 effective participating
> dimension ≈3/32 rings; reservoir baseline = debt-#1 in-data falsifier; taps {1,9,17,25} verified
> 26/32 ≥1e-3 — strict every-ring gate at K=4 likely → fallback (c)); **P6-F2 → clause (b) REFUTED**
> (never binds before clause (a); §G(iii) froze no void ceiling — Supervisor verified textually) →
> v3 will drop it to clause-(a)-only (r_min cand. ≈0.16) with the M1-validity check recorded as
> PASSED. Decisions D3/D4 + Supervisor recommendations: **E-2026-07-05-1 (updated)**.
> **Lucas delegated ("go") → v3 written + committed the same day:** §C clause-(a)-only (candidate
> r_min ≈ 0.16; M1 check PASSED-recorded), §B effective-dimension report + falsifier consequence +
> {1,9,17,25} seed + "controllable subset." The **v3 re-confirm addendum** is staged at the end of
> `critic_instructions_s0_4_freeze.md` (supersedes the v2 addendum). S0.4-0 items 1–2 updated to v3.

**State:** S0.3-1b ACCEPTED + committed (2d0673b). Lucas ruled the three S0.4-gating questions
(saturating-all · clamp A · R-ii) **and delegated the Critic-AMEND's two HIGH calls** ("OK I trust
you", E-2026-06-17-1). The Supervisor wrote **packet v2** (PR-6/PR-7/PR-5/PR-12 PROPOSED v2 in
`preregistration.md`). **Nothing is ACTIVE for the Executor** — next gate is the **brief Critic
re-confirm of v2** (`shared/critic_instructions_s0_4_freeze.md` + the v2 addendum at its end) →
**Lucas signs** → then **S0.4-0** goes ACTIVE.

**QUEUED (gated on PR-6 v3 signature — DO NOT START) — S0.4-0: calibration + PR-5 recon.** Local, $0.
1. **Input-map controllability measurement (PR-6 §B v3, D1/D3):** find the **minimal input-tap set**
   (≤ K=4 taps) s.t. at C-2/N=32, connected init μ_c=0.3κᵢ, on-resonance, **every** ring's task
   gradient ≥ **10⁻³·ring-1** (the meaningful-ratio gate). **Start at the registered seed
   {1,9,17,25}** (Critic-verified 26/32); try fewer taps, then completed coverage within K. **Measure
   + register the participation profile** (per-ring settled |a_j|/max + count ≥10⁻³) under the
   resolved B — every "N=32" use carries this effective dimension (v3). **Report the tap count to the
   S0.7 envelope** (E/O-channel cost). **If no ≤K-tap B clears it → fallback (c):** report the
   measured effective trainable depth, down-scope the C-2 claim to "controllable subset in situ."
2. **r_min measurement (PR-6 §C v3, clause (a) alone, on-resonance):** smallest r s.t. on-resonance
   the **saturating** κ_net ≥ 0.05κᵢ, then r_min = that + Δr=0.02; addend (candidate ≈0.16). Clause
   (b) is DROPPED (v3) — do NOT evaluate an M1-validity governor; DO report E_sym/E_sat at r* and at
   the clause-(a) floor (pins the ×37-vs-×91 build-up factor; goes into the PASSED-check record).
   **κ_ext-axis init-consistency:** κ_ext-init(0.3) + the PR-12 damping range inside [r_min,3].
3. **§G-conformance check (PR-6 §C/§G, D2):** determine whether δ-dependent build-up (PR-4 §G's
   P_circ=Σ|aⱼ|²) is a **conformance fix** (no freeze change) or a model addition; if conformance-cheap,
   fold in → r_min becomes δ-aware; else log anchor-risk (vii). Sweep δ over [−κᵢ,+κᵢ] to characterize
   off-resonance de-saturation.
4. **Multi-point E₀ re-derivation (PR-6 §G-addendum):** re-evaluate E₀ for the resolved input map
   (total-energy budget over the taps); single S0.4-0 addendum consumed before any bake-off run.
5. **PR-5 recon (lit):** source twin-mismatch levels (SiN ring + Er-gain characterization accuracy;
   Wright et al. *Nature* 2022 + SPSA hardware demos) → menu for the [RECON-DEFERRED] levels.
*(Post-signature the Supervisor promotes this to ACTIVE with full deliverable/gate spec.)*

---

## ✅ DONE — S0.3-1b: substrate edits from the Critic APPROVE-WITH-EDITS (freeze-conforming) — **ACCEPTED 2026-06-13 (Supervisor-verified)**

> **Supervisor ACCEPT 2026-06-13 (verified; re-confirmed green on resumption 2026-06-17).** All 5
> freeze-conforming edits landed; **full suite 128/128**. Gain default flipped `fixed`→`saturating`
> (faithful to §G/§N-E6 — code now conforms to the signed freeze, no freeze change); `test_h`
> de-hollowed (gain-path-live assert PASS @saturating / FAIL @fixed; ∂g/∂κ_ext reproduces the
> Critic to the digit — −0.750 @θ₀, edges −10.1..+0.41, sign-flip @r≈0.5) + a connected-init
> variant exercising rings 2..N; hygiene gate rewritten to ban the real source-stack symbols
> (dropping the PR-2-colliding task-token bans) and planted-symbol-proven; intracavity-reachability
> column surfaced in the calibration artifact (all gain cells material-aspirational on the operative
> plane); ASE-grad-detached convention registered in `ase.py`. `test_c`/`test_e` pin
> `gain_mode="fixed"` (the plane the frozen B1/E₀ numbers live on). $0/local.
> **One new finding surfaced — D-2026-06-13-1** (saturating default makes the K4 lower bound r=0.1
> super-threshold: κ_net crosses 0 at r\*≈0.134, so the effective trainable band is [≈0.134, 3],
> not the registered [0.1, 3]; `clamp_to_bounds(r=0.1)` is unsafe in saturating mode) → routed to
> **PR-6 / S0.4a** (κ_ext-clamp policy; Supervisor leans option A, raise the saturating-mode clamp
> to r_min≈0.15). The freeze-gated items (PR-12 rerun, PR-6 registrations) remain on Lucas
> (E-2026-06-13-2 + D-2026-06-13-1).

**Assigned:** 2026-06-13
**Supervisor:** Claude Opus 4.8
**Status:** ✅ DONE 2026-06-13 — ACCEPTED (Supervisor-verified 128/128); freeze-conforming, $0;
finding D-2026-06-13-1 surfaced → PR-6. The freeze-gated items wait on Lucas (E-2026-06-13-2).
**Prereqs / read first:** `shared/critic_review_s0_3_1.md` (verdict APPROVE-WITH-EDITS, findings
S31-F1..F8) · the frozen PR-4 v2 §G + §N-E6 · `photonic_ssm/substrate/{dissipative_ring,gain,
ase}.py` · `tests/test_substrate.py` · `tests/test_no_equalization_coupling.py` ·
`results/s0_3/e0_reachability_addendum.{md,json}`.

### Goal
Apply the Critic edits that **conform the code to the already-signed freeze** (no freeze change,
no new methodology) — the Critic established §G/§N-E6 *mandate* the saturating gain mode, so
flipping the default is a correctness fix. The freeze-gated items (PR-12 rerun, PR-6
registrations) are NOT in this task — they wait on Lucas (see the ACCEPTED block below + the
roadmap S0.3 banner).

### Deliverables (each maps to a Critic finding)
1. **(S31-F1) Flip the rollout default** `gain_mode="fixed"` → `"saturating"` in
   `DissipativeRingSubstrate`. Keep `"fixed"` as a **documented diagnostic/sensitivity** mode
   (the gain-channel floor, analogous to γ=0). Add a one-line docstring note that the registered
   bake-off mode is `"saturating"` for all four estimators (the PR-6 registration is the
   Supervisor's; the code default conforms now).
2. **(S31-F1/F2) Harden `test_h`** so the F18 gate is not hollow on the gain path: (a) run the
   **faithful** (`saturating`) mode; (b) assert the **gain path is live** — the autograd
   κ_ext-gradient of `kappa_net()` in saturating mode differs from the fixed-mode value by the
   predicted ∂g/∂κ_ext (equivalently: saturating κ_ext-grad ≠ fixed κ_ext-grad on one
   loss/seed); (c) add a **connected-init variant** (nonzero μ) so the gate actually exercises
   rings 2..N — without it even the hardened test only proves ring-1's gain path. Keep the
   existing assertions. Report the measured ∂g/∂κ_ext (≈ −0.75 at θ₀, the Critic's number) and
   the at-edge values (−10.1 @ r=0.1 … +0.41 @ r=3, sign-flip @ r=0.5) as a printed diagnostic.
3. **(S31-F3) Surface the intracavity reachability** in the calibration outputs: the addendum
   `.md` already has the bus number — add the `g0_required_intracavity_dB_per_cm` column (already
   in the `.json`: C-2 ≈ 380, C-3 ≈ 403) beside it, and state the corrected verdict (all
   gain-bearing cells material-aspirational on the operative intracavity plane; the bus number is
   a floor). The Supervisor has already corrected the ledger addendum — make the artifact match.
4. **(S31-F5) Rewrite `test_no_equalization_coupling`** to assert the **real invariant**: the
   source training-stack symbols are absent — at minimum `equalization_multilayer`,
   `ManakovFiber`, `MRRWeightBank`, `MultiLayerEqualizer`, `ParallelPol`, `generate_dp_qpsk`,
   `viterbi_viterbi`, `compute_nmse_field`, `forward_batched` (the Critic-verified list). **Drop
   the generic task-token bans** (`PAM4`/`PAM-4`/`QPSK`/`HD_FEC`/`ber_curve`) that collide with
   the project's own registered PR-2 T-A 4-PAM task. Then the neutral renames in
   `tasks/equalization.py` are no longer needed (rename back to clear 4-PAM vocabulary if you
   like, or leave them — your call, but the gate must test the stack, not a token).
   `test_package_runtime_is_torch_only` stays.
5. **(S31-F6) Register the ASE-covariance-gradient convention in code:** a docstring/comment in
   `ase.py` stating that the noise covariance Q_d and the noise realization are intentionally
   detached from the parameter gradient (exogenous-noise / hardware-faithful; the reparameterization
   gradient through the noise *amplitude* is dropped by design), consistent across all estimators.
   (The ledger registration is the Supervisor's PR-6 item; the code comment makes the intent local.)

### Gate / acceptance
All existing tests still pass; the **hardened `test_h` now fails in `"fixed"` mode and passes in
`"saturating"`** (proving it's no longer hollow); the rewritten hygiene gate passes and is
re-run-proven to **catch** a planted source-stack symbol (add+remove a temporary `MRRWeightBank`
reference in a scratch file to confirm it trips, then delete). Report the ∂g/∂κ_ext diagnostics.

### Deployment
Local, minutes, $0. No sweeps. Smoke: one `saturating`-mode rollout per gating cell with finite
nonzero gain-path gradient before running the suite.

### NOT in this task (gated on Lucas / freezes — do not start)
- **PR-12 convergence-controlled damping rerun + 8 seeds** (S31-F4) — blocked on Lucas's
  **PR-4 §G ↔ PR-12 reconciliation** (does PR-12 = the registered g_f=0.9 operating point, or a
  distinct D-LinOSS-damping/δ-init knob swept at fixed g_f=0.9?). Supervisor brings this to Lucas.
- **PR-6 registrations** (S31-F2 connected init; S31-F1 mode-for-all-estimators; S31-F8 sweep
  recipe: batch 8 / cosine LR / grad-clip / μ-init / δ-band) — freeze before S0.4a (Supervisor
  drafts, Lucas signs).
- **PR-11 generator-distinctness** (S31-F7) — an S0.4 RHEL-echo requirement; carry to S0.4.

**Launch the Executor (separate terminal):**
```
cd ~/Documents/Project_SSM
claude "Read shared/launch_executor.md and follow it."
```

---

## ✅ ACCEPTED — S0.3-1: build the shared dissipative-ring substrate (PR-4 🔒 SIGNED)

> **Supervisor ACCEPT 2026-06-13 (verified, artifacts-first).** Ran `tests/test_substrate.py`
> myself → **9/9 pass** (8 registered a–h + checkpoint); read each test to confirm it is
> *substantive* (b is bit-identical to S0.1 to 1.4e-20 + analytic Lorentzian; e is a 5000-step
> end-to-end E₀ measurement; h asserts the registered operating point + finite nonzero grads on
> all P2 families). Hand-verified the load-bearing E₀ number (C-2 = 1.07e8 ✓) and the
> reachability prediction (C-1 material-aspirational, C-2 straddles — matches §G/P4-F2). E₀
> addendum **pasted into PR-4** (the registered deferral, discharged). M2 quasi-static confirmed
> at both cells. Compute $0/local. The Executor's transparency is exemplary (5 anomalies flagged,
> incl. one it could have buried). **Build gate F18 PASS — accepted.**
>
> **Two items NOT closed by this acceptance (carried, not blockers to acceptance):**
> 1. **PR-12 deferred — NOT frozen on this curve.** The damping sweep is confounded by a
>    fixed-budget trainability artifact (anomaly B; the Executor flagged it and correctly left
>    PR-12 to Supervisor+Lucas). A clean PR-12 needs a convergence-controlled rerun (train-to-
>    fixed-loss, not fixed-steps) OR a documented confound-aware selection. Held for S0.3-close.
> 2. **Finding S-F1 (MEDIUM, pre-S0.4 must-resolve + freeze-interpretation for Lucas):** the
>    rollout defaults to `gain_mode="fixed"` (g ≡ 0.9·κᵢ constant); `test_h` runs that default,
>    so the F18 gate's κ_ext grads flow through the coupling/loss path, **not through the gain**.
>    The frozen §G ("differentiable function of the episode drive statistics") + §N E6 ("trained
>    κ_ext excursions change intracavity energy *as physics, not renormalization*") require the
>    gain to **respond** to κ_ext (the implemented-but-non-default `gain_mode="saturating"`). Risk:
>    if SPSA perturbs the real saturating gain while PAT/adjoint/BPTT backprop through fixed gain,
>    the four estimators are **not training one substrate** (violates the shared-substrate
>    standard). → Critic review item #1; Lucas freeze-interpretation question (is the rollout gain
>    pinned at 0.9κᵢ, or saturating-responsive?); the default + the F18 gate's gain-path coverage
>    must be settled **before S0.4a**. Does not affect the calibration, M2, or tests a–g.
>
> **Critic verdict 2026-06-13: APPROVE-WITH-EDITS** (`shared/critic_review_s0_3_1.md`,
> independently re-run 9/9). **S-F1 CONFIRMED and elevated to HIGH** (S31-F1): the dropped
> ∂g/∂κ_ext is 27% of the κ_net gradient at θ₀ and **6× the retained term, sign-flipped, at the
> r=0.1 trainable edge** — structurally different, not benign. Disposition APPROVE-WITH-EDITS not
> AMEND: the freeze §G/§N-E6 *already mandate* saturating, so flipping the default conforms code
> to the signed freeze (no freeze change); Lucas **confirms** (not reinterprets) the bake-off-wide
> consequence (all four estimators use `saturating` — a PR-6 registration). Edits → **S0.3-1b
> (ACTIVE, above)** for the freeze-conforming subset. New Critic catches folded in: **S31-F3**
> (reachability is worse on the operative intracavity plane — all gain cells material-aspirational;
> ledger addendum corrected), **S31-F4** (PR-12's sweep axis *is* PR-4 §G's g_f — needs PR-4/PR-12
> reconciliation by Lucas before PR-12), **S31-F5** (hygiene gate → test the real invariant),
> **S31-F2** (μ(0)=0 = signal-starvation, top S0.4 risk → PR-6), **F6/F7/F8** (register conventions).

**Assigned:** 2026-06-13
**Supervisor:** Claude Opus 4.8
**Status:** ✅ ACCEPTED 2026-06-13 — F18 build gate PASS (Supervisor-verified); PR-12 deferred; finding S-F1 (gain-mode) → Critic + Lucas before S0.4a
**Prereqs / read first:** roadmap §S0.3 (Do / Deliverable / Gate F18) · **the frozen PR-4 v2
block** in `shared/preregistration.md` (the substrate spec — this task *implements* it, sets
no new values) · PR-2 v2 (partition P2, N-grid, F6, F12) · PR-13 (memory family) · PR-10
(clocks) · PR-11 (irreversibility/ASE-stream carry-ins) · S0.1 (`results/s0_1/…` + the
`pole_region` / discretization / `loss_q_consistency_error` functions — inherited conventions)
· `docs/s0_3/substrate_recon.md` (R§ physics) · `docs/s0_3/pr4_input_sheet.md` · the 7-asset
salvage manifest (S0.0). **The dynamical SSM core is new code** (S0.0a: the salvaged ring/MRR
code is static-CW, the training engine MZI-specific — not liftable); **salvage** the gain/ASE
functions, the rate-equation SOA (for M2 only), the SiN registry, static Lorentzians (CW-limit
test refs), ridge readout (reservoir baseline), and the sweep/JSONL runner, with provenance
headers.

### Goal
Build the **single shared dissipative-ring substrate** that all four estimators (S0.4) and the
bake-off (S0.5) train through — finite-Q rings, M1 static-saturated gain, injected ASE, the
splitting doublet — exactly as frozen in PR-4 v2, with full state trajectories exposed and the
BPTT reference able to train through it end-to-end (the gradient-flow gate). This is the
substrate the entire Stage-0 headline result is measured on; its fidelity and its
no-`detach`/no-`no_grad` discipline are load-bearing. Plus the two registered numeric
calibrations (E₀, saturated reachability) and the coarse BPTT damping sweep that selects
PR-12's central cell.

### Deliverables
1. **Core substrate** — `substrate/dissipative_ring.py :: DissipativeRingSubstrate`. N-ring CMT
   recurrence in **amplitude rates**, S0.1 conventions inherited (κᵢ = ω₀/2Qᵢ; κ_tot = κᵢ +
   2κ_ext symmetric add-drop; **ZOH/van-Loan exact discretization**; 100-GHz-FSR geometry; λ =
   1550 nm). Nearest-neighbor chain coupling μ_jk. **Trainable params = the frozen PR-2 P2
   partition: {δ_j, κ_ext,j, μ_jk}** (gain-free). **Full state trajectory exposed in the API**
   (Gate F18). Readout = intensity |·|² (PR-2 R2). Clock-parametric over PR-10 {0.1, 1, 2}
   GS/s.
2. **M1 gain** — `substrate/gain.py`. Per-episode operating point **g(P̄) = g₀/(1+P̄/P_sat)**,
   fixed within the rollout, **differentiable** (no detach — house constraint 3a/3b). **P̄ and
   P_sat at the intracavity plane**: P_sat,ring = I_sat·A_eff (A_eff = 1.2 µm²) from the
   flagship −15 dBm; P_circ = Σⱼ|aⱼ|²·ħω₀/τ_rt. **Operating point g_rt = 0.9× intrinsic per-rt
   loss** ⇒ κ_net = 0.1·κᵢ + 2κ_ext; g₀ set by the saturated solve so g(P̄₀ at the registered
   drive) hits 0.9×. **Sensitivity rows g ∈ {0 passive, 0.5×}**; P-CORN passive-only.
3. **A2 ASE** — `substrate/ase.py`. Continuous Langevin term ⟨F F*⟩ = 2κ_g n_sp δ(t−t′) (photon
   units), discretized to compose with the ZOH/van-Loan step; n_sp from **NF-A (n_sp = 2.5)**.
   **A1** (per-rt discrete kick) implemented as the registered first-order-equivalent. **Fresh
   draws per pass; forward and echo streams independent** (PR-11). Expose an ASE-variance knob.
4. **Splitting** — `substrate/splitting.py`. **K-pol-3** 2×2 CW/CCW doublet per ring, **always
   ON**; γ per cell (C-1 90, C-2 11.8, C-3 per menu, MHz); **γ = 0 recovers the single-pole
   model exactly** (assert in a test).
5. **Cells** — `substrate/cells.py` (extend the salvaged SiN registry): **C-1 P-FND** (Qᵢ =
   2×10⁶, γ 90 MHz, N=8), **C-2 P-AN800** (Qᵢ = 6.8×10⁶, γ 11.8 MHz, N=32), **C-3 P-UHQ** (Qᵢ =
   3×10⁷, N=128); NF-A 7.0 headline. Sensitivity cells: P-CORN (passive), **C-2 ×2-loss derate
   (Qᵢ ≈ 3.4×10⁶)**, γ ∈ {0,11.8,90,160}, NF ∈ {3,5,7}. Each cell carries its
   `loss_q_consistency_error()` check (deliverable 8a).
6. **O2 normalization + E₀ calibration** — `substrate/normalization.py` + `calibration.py`.
   Implement the **frozen E₀ formula E₀ = 2·κ_ext,θ₀·(P̄₀/ħω₀)/κ_net²** (C-2, θ₀, δ=0, μ=0,
   CW-equivalent reading); encoder scale derived **once per arm at θ₀ and frozen** (trained
   κ_ext excursions thereafter are physics, not renormalization). **Numeric E₀ per cell** +
   the **saturated reachability solve** (required g₀ vs the Er-anchor span 1.0–1.9 dB/cm, per
   cell) → **emit a one-line ledger addendum** (`results/s0_3/e0_reachability_addendum.md` +
   JSON) for the Supervisor to paste into PR-4 **before any consuming run**.
7. **M2 one-off validation** — run the **salvaged rate-equation integrator at τ = 3.4 ms** once
   at **C-2/θ₀ and once at C-1/θ₀** (P4-F9); confirm the quasi-static reduction (per-episode
   relaxation ≤ 3 % bound); archive the comparison with the validation set. **M2 is not a
   substrate-matrix member** — do not wire it into the estimator path.
8. **Registered unit tests** (`tests/`, all must pass and be reported):
   (a) `loss_q_consistency_error()` α↔Q registry check per cell;
   (b) **zero-noise / passive limit recovers the S0.1 forward model** (vs the static Lorentzian
   CW-limit references) within tolerance — Gate F18;
   (c) **B1-consistency**: K4 bounds r ∈ [0.1, 3] map into the S0.1 realizable pole region at
   **every** cell;
   (d) **A1↔A2 statistical equivalence** (difference O(10⁻³) relative at per-rt gains ≤ 0.2 dB);
   (e) **E₀ normalization**: E(E₀-normalized drive) = E₀ within tol, **per cell × bound-edge r ∈
   {0.1, 3}**;
   (f) **n_ss ≈ 23 ASE photons** at NF-7 / 90 %-compensation, corner-independent (≈ 9 at NF-3);
   (g) **γ=0 ⇒ single-pole** structural equivalence;
   (h) **gradient-flow gate (the operational F18 test)**: a BPTT loss backpropagates through the
   full substrate (gain + ASE + splitting) to all P2 params — **no `no_grad`/`detach`** in the
   rollout path; assert nonzero grads on δ, κ_ext, μ.
9. **Coarse BPTT damping sweep at close (F3 → PR-12)** — `analysis/s0_3_1_damping_sweep.py` +
   JSONL. Train the **BPTT-on-substrate reference** across a coarse D-LinOSS damping grid at
   **C-1/N=8 and C-2/N=32** (θ₀, NF-A), ≥4 seeds/point (8 for any high-variance point), on the
   T-A task (PR-2). Output the damping→accuracy curve. **This selects PR-12's central operating
   cell — but the PR-12 freeze itself is a Supervisor+Lucas step, not yours; report the curve
   and stop.** (Distinct from PR-3, the final ceiling measured at S0.4 close.)
10. **Compute estimate (F21)** — aggregate order-of-magnitude for the substrate + the damping
    sweep (+ a forward-looking note for S0.4/S0.5). **If anything implies cluster spend, stop
    and escalate to Lucas via `escalate_to_human.md` before running it** (the C-3/N=128
    aspirational axis is the likely heavy one — keep it out of the gating path).

### Output schema
- Damping sweep JSONL: `{cell, N, damping, seed, clock_GSps, bptt_test_acc, bptt_train_acc,
  ase_var, n_passes, runtime_s, anomaly}` per row.
- Calibration JSON: `{cell, E0_photons, kappa_i, kappa_ext_theta0, kappa_net, g0_required,
  er_anchor_span_dB_per_cm, reachable_bool, sat_depth}` per cell.
- Test report: pass/fail + the measured numbers for (b)/(d)/(e)/(f) (the equivalence residuals,
  the n_ss value, the E₀ tolerances).
- `results_log.md` entry with raw-data paths, summary stats, variance, anomaly flags.

### Key gates and questions
- **Build gate = roadmap F18:** substrate reproduces expected limits (test b), one variance
  knob each for loss/gain/ASE, full state trajectories exposed, **and the BPTT reference trains
  through end-to-end with verified gradient flow (test h)** — the operational proof the
  detach/no_grad anti-pattern was avoided. **All registered unit tests (8a–h) must pass.**
- **Report honestly if:** any cell fails B1-consistency (c) — that bounds the realizable region
  and is a finding, not a silent clamp; the saturated reachability solve (6) shows a
  gain-bearing cell can't reach 0.9× at the registered drive (C-1 is already flagged
  material-aspirational in PR-4 — confirm the number, don't paper over it); A1↔A2 diverge beyond
  O(10⁻³) (the integrator choice then needs the Supervisor); E₀/n_ss miss their registered
  values.
- **Do not decide** anything left to the freeze — every value is in PR-4 v2. If you find a gap
  the freeze didn't cover, **escalate via `decisions_needed.md`; do not invent a value.**

### Deployment
Local first: substrate + all unit tests + a **smoke test** (one short rollout per cell at each
clock, asserting state-trajectory shape + finite gradients) before any sweep. The coarse
damping sweep at C-1/N=8 and C-2/N=32 should be local-feasible; **produce the compute estimate
(deliverable 10) before launching it**, and escalate if it implies cluster spend. Seeds: ≥4
per damping point, 8 for high-variance points. No cloud spend without Lucas's approval.

---

## ✅ DONE — S0.3-0: substrate design recon + PR-4 input sheet (S0.3 step 0 of 2)

**Assigned:** 2026-06-10 · **Closed:** 2026-06-10
**Supervisor:** Claude Opus 4.8
**Status:** ✅ COMPLETED 2026-06-10 — Supervisor **ACCEPT**. All gates met: [EV]/[AV]/[ABS]
discipline with a re-grep verification trail; menu-not-choice end-to-end; zero substrate code /
zero training; every registered anchor reproduced exactly by the arithmetic kernel. Headline
catches accepted: **debt #3's premise is FALSE** (the flagship *measured* NF ≈ 7 dB — three-way
verified; S0.8 reword = Supervisor's, and it is a process datum for debt #4, the other
inferred-absence debt); two draft assumptions killed by sources (Mu "3–4 dB" untraceable;
Frankis no-NF); **EV-F3 resolves two-against-one** (N=128-in-band only at class-leading r≲1 —
its split regime; only knob-ON survives); **AN800 never qualifies for knob-OFF**; **Er is
rigorously quasi-static** at all registered clocks (τ = 3.4 ms measured) → the **M1-vs-M3
gain-regime fork is left open by design — it is the first methodology decision on resumption
and S0.3-1 is blocked behind it** (anomaly v; note the M1 structure — linear in-loop + static
gain + ASE + readout |·|² — *echoes* the frozen PF-F1 architecture, which is consistency, not
coincidence, and must be named deliberately at PR-4); gain budget: **CORNERSTONE cell is
passive-only**; Cui 2023 = probable AN800 primary **[AV — verify at the PR-4 freeze]**; the
foundry-corner T-A memory death under any loading is exactly the pre-registered PF-F3 path
(the freeze anticipated it; nothing to amend). Memos: `docs/s0_3/substrate_recon.md` +
`pr4_input_sheet.md`; results in `results_log.md`; commit `aa8e982`.
→ Next on resumption: Supervisor names the gain-regime fork (decision → Lucas), drafts the
PROPOSED PR-4 block from the input sheet, Critic phase-boundary review, Lucas freeze — then
S0.3-1 (substrate build). **Project paused by Lucas 2026-06-10 (eve)** — see
`docs/project_status_2026-06-10_pause.md`.
**Source:** roadmap §S0.3 + ledger Notes **PR-4 constraint bullets** (D-08-3 roughness/splitting;
EV-F1 holding/trim convention; EV-F3 N=128⇄class-leading-Q⇄splitting; **PF-F8f input-power
normalization**) + parked **D-2026-06-08-1** ((α, Q_i) pair — adjudicated by F13, formalized at
PR-4) + **debt #3** (Er:Si₃N₄ NF — front-loaded per F14: the sourced NF bracket is a
*prerequisite* of the substrate's ASE knob). Pattern: S0.x-0 recon → **PR-4 freeze (Critic
review + Lucas)** → S0.3-1 substrate build. **Menu, not choice** — this task feeds the PR-4
freeze; it sets no values and builds no substrate.

**Objective:** every input the PR-4 freeze needs, as [EV]-sourced menus; plus the
substrate-physics decision inventory so S0.3-1 has zero invent-at-implementation-time gaps (F12).

### Tasks
1. **Debt #3 — Er:Si₃N₄ noise figure (the critical-path item).** (a) What the flagship
   Er:Si₃N₄ amplifier paper states and measurably does NOT state about NF [EV-quoted]; (b)
   measured NF brackets from the nearest comparables (EDWA / Er:Al₂O₃ / Er:LNOI waveguide
   amps + the 3 dB quantum-limit floor, each with provenance); (c) 2–3 candidate conservative
   NF values for the PR-4 noise cell, with the argument for each.
2. **D-08-1 inputs — candidate (α, Q_i) operating pairs:** foundry-grade + class-leading, each
   self-consistent (derive one from the other; apply the S0.1 registry loss↔Q fix), with
   provenance; for each candidate, the EV-F3 check — informationally distinct poles/GHz at
   N=128 (linewidth packing), so the PR-4 freeze can adjudicate the N=128⇄Q⇄splitting coupling
   on numbers.
3. **Roughness/splitting sub-parameter (D-08-3):** sourced backscatter/mode-splitting statistics
   per roughness/platform class; splitting evaluated **at operating κ_ext** (not undercoupled
   worst case); CW/CCW-knob default policy options (ON except clean-damascene corner — confirm
   or revise from sources).
4. **Gain-stage physics inventory (decides what "gain saturation" means in the substrate):**
   Er upper-state lifetime (~ms) vs the registered GS/s clocks — show the regime arithmetic
   (is gain quasi-static per-symbol at 0.1–2 GS/s? at training-relevant envelope timescales?);
   consequences for the salvaged SOA rate-equation model's role (its ~ns dynamics are a
   *different* regime); menu of substrate gain-model classes (static saturated gain + ASE vs
   full rate-equation) with what each costs/buys. Flag explicitly if this forks methodology —
   the Supervisor takes it to the ledger/decision file.
5. **PR-4 input sheet** (`docs/s0_3/pr4_input_sheet.md`): candidate noise cells (Q/α + NF + ASE
   level), κ_ext policy options vs the B3 bounds, holding/trim-statistics convention options
   (EV-F1), and a concrete **input-drive-power / intracavity-energy normalization mechanism**
   (PF-F8f — how the encoder is power-bounded so it cannot buy SNR against the noise cell).
   Menu-not-choice; the Supervisor drafts the PROPOSED PR-4 block from this.

### Gates
- [EV]/[AV]/[ABS] sourcing discipline with a verification trail (the S0.2-0 standard).
- Menu-not-choice end-to-end; **zero substrate code; zero training runs**; no edits to frozen
  ledger blocks.
- Each menu row carries provenance + the arithmetic that sizes it against registered values
  (PR-10 grid, B1/B3 ranges, the frozen PR-2 cells).

### Deliverables
`docs/s0_3/substrate_recon.md` (tasks 1–4) + `docs/s0_3/pr4_input_sheet.md` (task 5) +
`results_log.md` entry (house standard; anomaly flags; subagent/token accounting as in S0.2-0).

### Out of scope
Substrate implementation (S0.3-1, post-PR-4-freeze); any PR-2 task-generator work; the F5
B2-crossover primary-source pass (S0.L-paced); D-LinOSS damping sweep (S0.6/PR-12); touching
the in-flight G3 runs beyond health checks.

---

## ✅ DONE — S0.2-1R: G3 record repair (Critic GA-F1/F4/F7) — **ACCEPTED 2026-06-11, Supervisor-verified from archived trails**

**Assigned:** 2026-06-11 · **Completed + accepted:** 2026-06-11
**Supervisor:** Claude Opus 4.8
**Status:** ✅ DONE (Executor commits 889ab53 pre-declaration → 268e6a6 annex screens +
GA-F2/F3/F4/F7 corrections → 60f665b fresh-8 + closing; ~9.6 h wall, local CPU, **$0**).
**Acceptance verification (artifacts first, numbers second):** 8 archived official run dirs +
non-empty per-seed driver logs + `PREDECLARATION.md` committed at 889ab53 BEFORE any run +
3 gradient-instrumented annex jsonls under `results/s0_2/gate_i/xcheck_official_local/`;
previously gitignored `gate_i/` tree force-added (the actual hole behind GA-F1). Supervisor
re-ran the pre-declared classifier from the archived npy/jsonl: **official fresh-8 = 0/8
strict-trap, 1/8 behaviorally collapsed** (22222 chance-frozen on both metric legs, loss
drifting → ALIVE under the conservative conjunction, flagged verbatim; 9012 plateau-moving =
alive; six healthy at val 0.83–0.91) · **ours annex-local = 8901 TRAP@1 · 9012 TRAP@555 (one
dropout-borne transient at 554) · 7890 ALIVE** — every claimed figure reproduces. Console 2/8
superseded per the pre-declared sentence; GA-F4 reconciliation (commit 087a346 cited) + GA-F7
nits verified in the results entry. PR-1.1 v2's incidence bullet now cites the archived
figures (Supervisor-side ledger edit done). **Sole remaining S0.2 item: Lucas signs PR-1.1 v2
(E-2026-06-11-1).**
**Source:** `critic_review_g3-adjudication.md` (verdict **APPROVE-WITH-EDITS — "sign PR-1.1
with these edits"**; GA-F1 was the signature-blocking item — resolved *now* by demotion in
PR-1.1 v2, and *upgraded* by this regeneration). **Not a gated run.** Nothing here touches
gated numbers or the frozen protocol — it repairs the *diagnostic* record under the already-
sanctioned cross-check. Zero tuning; zero gated reruns.

### Tasks
1. **GA-F1(a) — regenerate the official fresh-seed leg, archived this time.** Pre-declare the
   fresh-seed list (n ≥ 8; include 9012 and 22222 for continuity with the console
   observations) **in a commit BEFORE running**; rerun the official code (pinned commit
   05a8353; the local pinned CPU venv jax 0.4.28 / eqx 0.11.4 / optax 0.2.2; official
   pickles; official runner) on those seeds; archive per-seed trails under
   `results/s0_2/gate_i/xcheck_official_local/`; report k/n trap incidence + per-seed
   outcomes with the Critic's superseding sentence ("incidence is stream- and
   environment-dependent; the rented-box console observations (2/8) are superseded by this
   archived local estimate"). **A different incidence than 2/8 is expected and immaterial**
   (any material incidence voids the criterion — PR-1.1 v2 logic).
2. **Regenerate the unarchived ours-annex 600-step trap screens** (seeds 7890, 8901 —
   currently prose-only) locally; archive alongside.
3. **Results-log corrections (GA-F1/F4/F7), in the S0.2-1 addenda:** (a) the data-path
   sentence → "per-seed trails for the 5 published-seed runs (archived); fresh-8 console-only
   (superseded by the local regeneration)"; (b) the **GA-F4 reconciliation** — insert the
   Critic's exact sentence on the E-5(iii) deviation (dropout masks → device generator,
   commit 087a346; init/shuffle stayed CPU; stream bits were never protocol content) and fix
   the "original config note" pointer to cite commit 087a346; (c) GA-F7 nits: write
   **90.56** (never "90.6 ± 9.3"); one sentence on official seed-6789's val→test gap
   (97.14 → 77.78 on 35/36-sample sets — the published selection convention swings ~20 pp
   here); the init-audit BN completeness note; the `solver_Heun` directory-template
   clarification.
4. Append a short addendum to the S0.2-1 results entry; the Supervisor then cites the
   archived k/n in PR-1.1 v2's incidence sentence (ledger edits stay Supervisor-side).

### Gates
Pre-declared seed list committed before any run · zero gated-number changes · zero tuning ·
all trails archived + committed · corrections cite GA-F numbers.

---

## ✅ CLOSED — S0.2-1: in-house LinOSS layer + Gate-i runs — **G1 ✅ PASS · G3 ❌ FAIL on record · PR-1.1 v2 🔒 SIGNED by Lucas 2026-06-11: G3 criterion void for anchor instability; Gate i adjudicated purpose-served (G1 PASS ∧ parity dossier)**

> **MEASURED OUTCOME (2026-06-11; GPU route per E-2026-06-10-5, Lucas-approved in-session,
> $1.15 of $7.44):** GPU parity gate passed (1.2–1.5e-7) → gated-5 ran to completion →
> **G3 FAIL 71.1111 %** (2/5 seeds in a zero-gradient absorbing state of the *official*
> objective). Frozen miss-rule executed to the letter: stop, no tuning, sanctioned
> divergence cross-check → **the official code itself, faithfully rerun, ALSO fails the
> frozen gate (90.5556 % < 90.6, σ 9.3 vs published 4.4; fresh-seed trap incidence 2/8 vs
> our 4/8, Fisher p ≈ 0.61).** Port exonerated (parity + line-by-line init audit +
> healthy-3 = 93.52 in published band). **Supervisor verified all statistics independently
> and accepts the diagnosis.** Adjudication: **D-2026-06-11-1** (Supervisor recommendation
> = O3 as the PROPOSED **PR-1.1**: FAIL recorded permanently · G3 criterion void for anchor
> instability · no replacement anchor · Gate i = G1 PASS ∧ parity dossier, purpose served ·
> F-G3 = reportable finding + new transfer-check freeze rule) → **Critic review
> (`critic_instructions_g3-adjudication.md`, Lucas launches) → Lucas signs** (E-2026-06-11-1).
> **No Executor work exists until the adjudication lands.** Annex-3 EigenWorms cancelled
> under the proposal; G1 + its annex stand untouched. S0.2-1 closes on the signed
> adjudication.

**Assigned:** 2026-06-10 · **G1 portion accepted:** 2026-06-10
**Supervisor:** Claude Opus 4.8
**Status:** ✅ CLOSED 2026-06-11 — **PR-1.1 v2 signed by Lucas** ("sign PR-1.1",
E-2026-06-11-1): G1 PASS ∧ G3 void-with-finding (FAIL on the permanent record; F-G3 binds
S0.8 wording); downstream proceeds on the PR-3 in-house-ceiling anchoring path as registered.
**G1 Heartbeat: GATE PASS, Supervisor-verified**
(gated mean 72.9032 % ≥ 72.1 reproduced from the per-seed table; per-seed values are exact n/62
counts; −0.78σ_published, inside the registered allowance; margin = 2.5 mean-granules of test-set
quantization — priced in by the frozen PF-F9d calibration, no re-litigation either direction).
Acceptance highlights: float32-exact cross-framework parity (~2e-7 transplanted-weight probs) is
the load-bearing validation; param-count convention diagnosed pre-training (published = trainable
+ BN state — quote it downstream, anomaly v); **PF-F6 vindicated** — the official-pipeline run
surfaced EigenWorms N=236 (23 dups deleted), which a reimplemented split would have silently
missed; PF-F1 rider confirmed [EV] (Vinckier linear cavity + photodiode |·|²; Paquot in-loop MZ).
Zero protocol deviations; the >24 h flag was raised exactly per spec.
~~→ Executor, on relaunch, FIRST action: start the G3 gated-5 runs~~ **DONE 2026-06-10 18:48,
then PAUSED by Lucas 19:36 — see the PAUSE STATE block above. Do NOT relaunch the runs; the
route decision (resume local / cloud / stay paused) is Lucas's at resumption.** S0.2-1 closes
when the G3 results + joint Gate-i verdict file in `results_log.md` (amend the existing entry).
**Source:** roadmap §S0.2 (Gate i) + **🔒 PR-1 v2, FROZEN 2026-06-10** (`preregistration.md` —
**the governing document; read it first and follow it to the letter**) + the freeze-review
carry-ins (ledger Notes, last bullet). PR-2 v2 is also frozen — it governs S0.3+, **not** this
task; nothing here implements it.

**Objective:** implement the in-house recurrence layer (the one the bake-off extends
downstream), validate it by reproducing the two frozen published anchors. **The gate, verbatim
from PR-1:** G1 Heartbeat unrounded 5-seed mean ≥ **72.1 %** **AND** G3 EigenWorms unrounded
5-seed mean ≥ **90.6 %**.

### Rider (do first; small; decision-free) — PF-F1 premise re-verification
At **retrieval level** (full text, not abstracts): confirm the Vinckier 2015 anchor system is a
*linear* passive cavity whose task-solving nonlinearity is the **readout photodiode |·|²**
(note also what Paquot 2012 used). One [EV]/[AV]-marked paragraph in the results entry. This is
the PF-F1 premise check (ledger-Notes carry-in); the Critic's linear floor stands regardless —
no frozen text changes either way, just the record.

### Main task
1. **The in-house layer (new code, this repo):** complex-diagonal (S4D/DSS-class) recurrence
   with an inter-mode coupling hook **μ (run at μ=0 throughout this task)**, whose Gate-i
   configuration **realizes the published LinOSS-IM recurrence exactly** (per D-08-2: LinOSS =
   the uncoupled, real-I/O conjugate-pair special case — not an approximation of it). PR-1
   reference-behavior pins: **learnable per-dimension sigmoid Δt, ReLU-parametrized diagonal A,
   IM discretization**. Do **not** build the ZOH/CMT substrate mode now (S0.3; PR-1 "Scope of
   Gate i" registers that delta).
2. **The published stack around it, verbatim:** BatchNorm → SSM → GELU → dropout → GLU → skip;
   mean-pool head. Configs frozen (no deviation): **G1** lr 1e-3 / hidden 16 / state 16 /
   blocks 6 / time T; **G3** lr 1e-3 / hidden 128 / state 64 / blocks 2 / time T.
   **Param-count integrity check:** report your counts vs published **10,936 (G1) /
   134,279 (G3)** — a mismatch is an anomaly flag, diagnose before training.
3. **Walker protocol exactly:** the 5 gated seeds {2345, 3456, 4567, 5678, 6789} setting the
   70/15/15 splits. **Split reproduction is pinned (PF-F6):** port the split routine or extract
   split indices from the official repo; if exact reproduction is infeasible in your framework,
   **stop and file `decisions_needed.md` BEFORE any gated run**. Gated statistic = the
   **unrounded** 5-seed mean per anchor. **Annex (non-gating):** +3 seeds {7890, 8901, 9012},
   reported separately.
4. **Closure rule (PF-F8i, frozen):** any protocol detail not stated in PR-1 resolves to the
   official repo's behavior. **No hyperparameter tuning on the gated runs — none.** The
   official MIT JAX repo is a *debugging cross-check only* (divergence diagnosis), never the
   tested object.
5. **On a gate miss: stop — do not tune.** Report per-seed numbers + a divergence diagnosis vs
   the official repo (bug vs systematic offset). A fixed *bug* (diff shown, mechanism named)
   may be rerun and reported as such; a "tweak that happens to help" may not — that is tuning.

### Framework / runtime
Executor's choice within house hygiene (exceptions via `decisions_needed.md`). The official
repo is JAX; the PF-F6 split extraction may be easiest by running its data pipeline once. UEA
datasets (Heartbeat, EigenWorms) — local download is fine. **Estimate runtime before training;**
flag via `decisions_needed.md` if projected wall-clock > ~24 h, or if EigenWorms' sequence
length (~18k steps) forces any workaround that touches the protocol (no silent truncation /
chunking — that is a protocol deviation).

### Gates (all must hold)
- Zero deviation from frozen PR-1 values; configs verbatim; closure rule honored; no tuning.
- 5 gated + 3 annex seeds per anchor, all reported per-seed; gate verdict per anchor + joint.
- Param counts reported vs published; split-reproduction method documented.
- Results entry (house standard): per-seed table, unrounded means ± σ, raw-data paths (JSONL),
  runtimes, anomaly flags, the rider paragraph.

### Out of scope
T-A/T-C task generators, the substrate/CMT mode, μ≠0, anything PR-2-implementing (all S0.3+);
the D-LinOSS damping sweep (S0.6/PR-12); any edit to frozen ledger blocks (Lucas-only).

---

## ✅ DONE — S0.2-0: debt-#2 benchmark recon + bake-off task candidates (S0.2 step 0 of 2) + EV rider

**Assigned:** 2026-06-10 · **Closed:** 2026-06-10
**Supervisor:** Claude Opus 4.8
**Status:** ✅ COMPLETED 2026-06-10 — Supervisor **ACCEPT**. All gates met: [EV]/[AV]/[ABS]
sourcing discipline with a first-hand verification trail (Appendix A.3); 4 Gate-i candidates with
exact published configs + 4 margin bases with per-candidate arithmetic; 3 task candidates with
explicit niche-fit arithmetic vs the registered memory corners; menu-not-choice respected
end-to-end; zero training runs; EV rider applied with citations. High-value catches accepted:
the **paper-vs-code Δt discrepancy** (PR-1 names the code as reference), **D-LinOSS
preprint-only status** (anchoring caveat), **Weather irreproducible at pre-registration grade**
(excluded), the **μ=0 guard-check** (no published coupled LinOSS-class benchmark exists —
debt #2 substantially discharged for Stage 0; final wording at S0.8). → Supervisor drafted the
**PROPOSED PR-1/PR-2 blocks** (preregistration.md) from these menus; Critic review + Lucas
freeze next. Memos: `docs/s0_2/debt2_benchmark_recon.md` + `bakeoff_task_candidates.md`;
results in `results_log.md`; commit `5137cc5`.
**Source:** roadmap §S0.2 (Gate i; F14 — the debt-#2 memo is a *prerequisite* of the PR-1/PR-2
freeze) + **continuation gate GO** (E-2026-06-10-3, Lucas 2026-06-10). **PR-1/PR-2 are ⬜ UNSET —
this task FEEDS the freeze. It does NOT set values and does NOT run anything Gate i will judge:
no LinOSS implementation, no benchmark training runs** (that is S0.2-1, post-freeze — the
S0.7L-0 → PR-10 → S0.7L-1 pattern). Literature/design-input only.

### Rider (do first; decision-free) — Critic envelope-audit fixes
Per the `critic_review_s07lite-envelope.md` fix list (cite EV-F numbers in the edits; no verdict
changes):
1. **results_log S0.7L-1 entry:** (a) replace anomaly (i)'s neutrality sentence per **EV-F2** —
   the two flagged readings are faithful to the frozen source record but **not** verdict-neutral
   (the OPT-corner rate-floor negative is partly C3-borne; CONS×B N=128@1 GS/s vs
   Jetson-sustained is trim-sensitive); (b) strike-correct finding 2's class-A sentence per
   **EV-F1** — class-A-dead is **C4-conditional**: under expected-value (P_π/2) holding, OPT×A
   clears Brainwave in-window (1.32–1.47 GS/s); only CONS×A is dead under any holding convention.
2. **Envelope memo §6:** one sentence per **EV-F3** — the N=128 margins assume the
   class-leading-Q corner (linewidth packing: O(10–20) distinct poles/GHz foundry vs ~150
   class-leading; → PR-4 with D-08-1); name the **single-quadrature/intensity readout** condition
   on C8 per **EV-F5** (→ PR-2 readout pin).
3. **Envelope memo §4:** restate latency per **EV-F4** ("sub-µs unreachable for the serving
   class, <4 ms author bound; ≥10² vs any plausible matched-N FPGA pipeline") + one cadence
   provenance line per **EV-F7**.

### Goal (main) — the design-input memo for the PR-1/PR-2 freeze
1. **Debt #2 (F14): LinOSS / D-LinOSS benchmark specifics, primary-sourced.** For each headline
   published result (LinOSS, D-LinOSS; Mamba-3 as context only): exact task + split + metric +
   model size/config + reported number + seed variance if reported + code availability; which
   results validate only the **μ=0 diagonal reduction** (D-08-2) vs involve coupling; from these,
   identify **2–4 candidate Gate-i reproduction targets** feasible at our scale (N≈32–128 states,
   local compute) with a defensible **margin basis** for PR-1.
2. **Bake-off task candidates sized to the niche** (envelope memo §6 + `mapping_result.md` §4):
   2–3 candidate streaming tasks — **equalization-class GS/s family first** (rate-consistent with
   S0.1's linewidth-derived class), plus ≥1 published-benchmark-aligned alternative — each with:
   effective line rate vs the ≥0.5 GS/s floor; **memory depth required (samples) vs the
   registered corners** (0.33–6.6 foundry / 4.9–98.8 class-leading over 0.1–2 GS/s); N sizing;
   dataset/generator spec; evaluation metric; how the PR-13 synthetic memory family would
   parametrize it.
3. **PR-2 input sheet:** trainable-parameter-partition options (the B1 set {κ_tot,j, δ_j, μ_jk}
   + the S0.1 actuation map); readout options under the **single-quadrature/intensity** condition
   (EV-F5) incl. the F6 κ_ext dual-role note; W1 claim-wording cross-check (does each candidate
   partition train pole positions AND inter-resonator couplings — the W1 set?).

### Deliverables
1. `docs/s0_2/debt2_benchmark_recon.md` — primary-quoted (verify-before-citing; the B2/F5 lesson)
2. `docs/s0_2/bakeoff_task_candidates.md` — the menu with an explicit niche-fit table
3. Results entry in `results_log.md`; rider edits noted there with EV-F citations

### Gates
Every load-bearing number primary-sourced + quoted; ≥2 Gate-i candidates with reproducible
configs + a margin basis; ≥2 task candidates with explicit niche-fit arithmetic (rate, memory
samples, N); **menu, not choice** (no values frozen); **zero training runs**; rider done.

### Out of scope
LinOSS/D-LinOSS implementation or training (S0.2-1, post-freeze); choosing the task/margin
(Supervisor drafts the freeze ask; **Lucas freezes**); new envelope sourcing (PR-10 frozen;
S0.7-full items live in the registry); PR-15 retrievals (Lucas, claim-freeze-paced).

### Deployment
Local; web allowed (literature task). ~1 day. No simulation, no cloud.

---

## ✅ DONE — S0.7L-1: S0.7-lite envelope (PR-10 🔒 FROZEN) + WS-F11/F12 rider

**Assigned:** 2026-06-10 · **Closed:** 2026-06-10
**Supervisor:** Claude Opus 4.8
**Status:** ✅ COMPLETED 2026-06-10 — Supervisor **ACCEPT**. All gates met: every number traces to a
frozen PR-10 row (memo §1 table; the 4 excluded legacy anchors verified absent); all four
corner×heater scenarios reported with full clearance matrices; explicit niche statement (memo §6);
§10 clause checked — **does NOT fire** (16 OPT cells clear ≥1 named baseline). Supervisor
spot-checked 5 cells by hand (conversion sums, control power, Brainwave/Jetson mapping, crossover
rates) — all reproduce. ~~"the class-A negative survives even a P_π/2 duty-credit relaxation …
robust to convention"~~ ← **struck, FALSE (Critic EV-F1; the Supervisor had tested only the
1 GS/s column):** under expected-value (P_π/2) holding, OPT×A clears Brainwave **in-window**
(crossovers 1.32–1.47 GS/s); only the deployable corner (CONS×A) is class-A-dead under any holding
convention — the binding-constraint statement is **C4-conditional**. **Verdict: conditional
POSITIVE, assumption-driven, not outreach-load-bearing — CONFIRMED by Critic audit**
(`critic_review_s07lite-envelope.md`, APPROVE-WITH-EDITS: byte-identical re-run; 36/36 clean-room
cells + 144 verdicts + crossovers reproduce; §10 non-firing robust to every tested perturbation).
The two flagged frozen-row readings are **faithful to the frozen source record but NOT
verdict-neutral** (EV-F2: the neutrality sentence fails both directions — the OPT-corner
rate-floor negative is partly a C3 artifact; one deployable-corner cell is trim-sensitive).
Rider (WS-F11/F12) done, no verdict changes. **Mandatory rider on the next Executor task:**
EV-F1/F2 one-line corrections (results_log anomaly (i)) + memo §6/§4 sentences (EV-F3/F4/F5) per
the review's fix list; EV-F6/F7 → S0.7-full registry.
Memo `docs/s0_7/s07_lite_envelope.md`; results in `results_log.md`; commit `e88fbeb`.
**Source:** roadmap v3.1 §S0.7-lite (F1/F16) + **PR-10 — 🔒 FROZEN 2026-06-10** (`preregistration.md`:
read the frozen block FIRST; **every load-bearing number in the envelope must trace to a frozen PR-10
row** — if a needed number is missing, STOP and post to `decisions_needed.md`; do NOT source new
numbers, that would un-preregister the run).

### Rider (do first; decision-free)
**WS-F11:** fix the S0.L-1 memo's §0 self-undercount (count §4.2 precisely — ≈74 rows / 80+ papers, not
"~60") + the dangling "N28a" pointer. **WS-F12:** add an "S0.8 full-text TODO" section listing the
residual abstract-resting items per the Critic's WS-F12. No verdict changes.

### Goal (main)
Run the **S0.7-lite envelope**: end-to-end **energy/sample + latency/sample** for the photonic SSM at
the frozen scale grid (N∈{8,32,128}; 0.1–2 GS/s; single-carrier-one-FSR), charged the **full frozen
conversion stack**, vs the three named baselines — at **both corners (OPT/CONS) × both heater classes**
(consistency rule: one heater class per scenario for power AND τ/SPSA-cadence). Identify the plausible
low-latency **niche** (→ the S0.2 task choice / PR-2), or state explicitly that none exists. **Check
the §10 escalation clause explicitly:** does even the OPT corner clear any baseline anywhere in the
grid?

### Deliverables
1. `docs/s0_7/s07_lite_envelope.md` — assumption table (verbatim from frozen PR-10, row refs per use);
   per-grid-point result tables; crossover/niche statement; the registered exclusions (laser, locking,
   control compute, packaging) listed as **unbudgeted**; verdict per roadmap semantics (negative →
   draft the Stage-1-reframing escalation; positive → labelled assumption-driven, not
   outreach-load-bearing).
2. `analysis/s0_7_lite_envelope.py` + JSON/plots under `results/s0_7/` — **arithmetic + plots only**;
   no simulation; no new sourcing.
3. Results entry in `results_log.md`; if the §10 clause fires, an `escalate_to_human.md` draft entry.

### Gates
Every number traces to a frozen PR-10 row (cited per use); all four scenario combinations reported (no
cherry-picking); exclusions stated in the output; explicit niche-or-no-niche statement; rider done.

### Out of scope
New sourcing (PR-10 frozen); claim wording (PR-2); PR-15 retrievals (Lucas); simulation code.

### Deployment
Local, arithmetic only; hours. No web needed (numbers are frozen).

---

## ✅ DONE — S0.7L-0: PR-10 assumption sourcing (S0.7-lite, step 0 of 2)

**Assigned:** 2026-06-09 · **Closed:** 2026-06-10
**Supervisor:** Claude Opus 4.8
**Status:** ✅ COMPLETED 2026-06-10 — all 5 categories primary-quoted (~35 primaries; 2 load-bearing
ones Executor-re-verified exact); 5 freeze brackets; **4 discrepancy flags vs legacy anchors caught**
(incl. Harris-2014-is-silicon and the unverifiable Ozkaya standing-power attribution — both excluded
from PR-10); heater-class consistency identified as load-bearing (suspended power ↔ ms-τ ↔ SPSA
cadence). **No envelope arithmetic** (gate held). Supervisor **ACCEPT** → **PR-10 PROPOSED block
drafted** (`preregistration.md`) — awaiting Lucas freeze; then S0.7L-1 runs. Results in
`results_log.md`; memo `docs/s0_7/pr10_assumption_sources.md`.
**Source:** roadmap v3.1 §S0.7-lite (F1) + **PR-10 (⬜ UNSET — this task *feeds* the freeze; it does NOT
set values)**. The pre-S0.2 continuation gate needs the lite envelope regardless of the pending PR-15
rulings (E-2026-06-09-5) — this keeps the pipeline moving while Lucas adjudicates.

### Goal
Source the candidate assumption set for **PR-10** with primaries, so the Supervisor can draft the PR-10
freeze ask for Lucas. **Sourcing only — do NOT run the envelope** (that is step 1, after the freeze;
running it now would un-preregister PR-10).

### Deliverables
1. `docs/s0_7/pr10_assumption_sources.md` — a candidate table, every row primary-sourced (vendor
   datasheet or measured paper, load-bearing number quoted):
   - **E/O + O/E conversion energies** (modulator drive incl. driver; PD/TIA) at the relevant rates;
   - **DAC/ADC** energy/sample + resolution (ENOB) at GS/s-class rates (published ADC-survey data +
     ≥1 named vendor part);
   - **named digital-baseline class + sources** (F16): tuned FPGA and/or embedded-GPU/ASIC
     implementations of comparable streaming SSM/FIR/RNN workloads at matched accuracy — names + cited
     perf/W, *not* an unoptimized GPU;
   - **thermo-optic holding power** per heater (SiN, trench-isolated) + control-electronics overhead —
     reuse pnn-multilayer numbers where primary-sourced (with provenance);
   - **operating scale**: N rings, line rate, λ-plan consistent with S0.1's pole region (cite
     `docs/s0_1/mapping_result.md` §4 numbers).
2. Where sources disagree, give **bracketing values + both sources** (the freeze registers the bracket,
   not a midpoint).
3. Results entry in `results_log.md`.

### Gates
Every number primary-sourced + quoted; brackets where sources disagree; **no envelope arithmetic** (one
illustrative sanity row allowed, labelled non-load-bearing).

### Out of scope
Running the envelope (step 1, post-freeze); the PR-15 re-classification (Critic Part 2); claim wording
(PR-2, Supervisor); A4 retrievals (human-access asks — Lucas, E-2026-06-09-5).

### Deployment
Web + datasheet reading; 1–2 days; no compute spend.

---

## ✅ DONE — S0.L-1: White-space existence search (debt #1, PR-15 — front-loaded pre-S0.2)

**Assigned:** 2026-06-09 · **Closed:** 2026-06-09
**Supervisor:** Claude Opus 4.8
**Status:** ✅ COMPLETED 2026-06-09 — sweep complete per the frozen rule: ~60 candidates / all 5 lanes /
every non-clear verdict primary-quoted / reproducible trail. **0 FATAL confirmed**; 1 potentially-FATAL
AMBIGUOUS (**Wu eLight 2025**, q1 unresolved) + boundary class (= Critic WS-F1, found by both
modalities) + Böhm 2022 + 8 unreachable primaries — **all escalated with primaries, nothing adjudicated
in-pipeline** (E-2026-06-09-4 / D-2026-06-09-2). Supervisor **ACCEPT**: protocol followed exactly; the
cross-modality asymmetry (Executor found Wu/Milanizadeh/Zhao; blind pass found Fisher 1987 + the
criterion defect) is the two-modality design working. PASS not issued — verdict assembly pends Lucas's
four rulings (E-2026-06-09-5) + Critic Part 2.
**Update 2026-06-10:** Critic Part 2 filed (E-2026-06-09-6) — **memo audit CLEAN**; gate = conditional
PASS (one-sided) under PR-15.1, degenerate under the frozen letter. **Follow-up queued (next Executor
task after S0.7L-0, decision-free): WS-F11** (fix the memo's self-undercount: ≈74 rows / 80+ papers,
not "~60"; fix the N28a pointer) **+ WS-F12** (full-text the residual abstract-resting items by S0.8).
**Source:** D-2026-06-09-1 (Lucas-adopted 2026-06-09, "ok go") + **PR-15, 🔒 FROZEN — read its detail
block in `preregistration.md` FIRST and apply it as written** (the kill-rule and lanes are frozen; do not
re-derive or reinterpret them). Roadmap v3.1 §S0.L. This is a **literature task** — no simulation code.

### Goal
Run the **existence search** for verification debt #1: is there ANY prior in which *internal recurrent
parameters of a physical photonic system were updated on the physical device by a gradient-based /
gradient-estimating rule*? This is the project's kill-shot, deliberately front-loaded (cheap + decisive +
potentially fatal). A single FATAL prior falsifies the scientific-first claim — surface it loudly; do
**not** soften or adjudicate it.

### Deliverables
1. **`docs/s0_L/debt1_whitespace_search.md`** — dated memo (snapshot 2026-06):
   - **Per-candidate verdict table:** citation · system · what was *physically* updated · q1 internal?
     · q2 on-device-in-the-loop? · q3 update-rule class · **verdict** (FATAL / non-fatal-cite /
     AMBIGUOUS→escalate / clear), with the **load-bearing sentence quoted from each primary source**.
     No aggregator-snippet citations (the B2/F5 lesson) — if you can't reach the primary, the verdict is
     AMBIGUOUS, not clear.
   - **All five PR-15 lanes swept** (i: zeroth-order/perturbative internal updates; ii:
     REINFORCE/policy-gradient internal updates; iii: HIL delay-reservoir feedback/internal adaptation;
     iv: evolutionary/Boolean — non-fatal, cite; v: free search + the named-group minimum set, extended
     as needed).
   - **The Bueno/Brunner boundary memo** (lane ii): verify in the primary sources exactly what that line
     physically updates (readout-only?) — the claim's most likely confuser; quote, don't paraphrase.
   - **Reproducible search trail appendix:** queries run, databases/engines, dates, hit counts.
2. **Any FATAL or AMBIGUOUS finding → stop and escalate**: post to `decisions_needed.md` +
   `escalate_to_human.md` with the primary attached. Adjudication is Lucas's, per PR-15 disposition.
3. Results entry in `results_log.md` (candidate counts per lane, verdict summary, anomalies).

### Gates
Every PR-15 lane swept + logged; every non-clear verdict grounded in a primary source with quote;
ambiguities escalated, never resolved in-memo; memo dated 2026-06; search trail reproducible.

### Out of scope
Claim **wording** (PR-2/S0.8 — Supervisor); roadmap/ledger edits; any simulation code; the S0.7-lite
envelope (separate task, after PR-10 freezes); debt #2/#3 memos (separate S0.L tasks, due at S0.2/S0.3).

### Deployment
Web search + primary-source reading (web access required); expected days, not hours; no compute spend.

---

## ✅ DONE — S0.1.1: S0.1 closeout (decision-free Critic edits before S0.2)

**Assigned:** 2026-06-09 · **Closed:** 2026-06-09
**Supervisor:** Claude Opus 4.8
**Status:** ✅ COMPLETED 2026-06-09 — all four edits landed + gates PASSED (107/107; transient F1 validation
**positive**: ringdown <1e-9 vs closed form, pole recovered from trajectory <1e-5, 2-ring beat = eig
splitting <2%). Supervisor ACCEPT (no Critic gate needed — this *executed* the Critic's own prescribed
edits; scope held, F2/F6 untouched). S0.1 is now **fully closed**. Results in `results_log.md`.
**Next ACTIVE task:** pending Lucas — D-08-2/D-08-3 steer + **D-2026-06-09-1** (front-load debt #1 /
PR-15 white-space gate; see `decisions_needed.md` + `escalate_to_human.md` E-2026-06-09-2).
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
