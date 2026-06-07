# S0.0a — Tooling Reconnaissance Report: `pnn-multilayer` → Project_SSM

**Task:** S0.0a (read-only recon; input to decision D-2026-06-05-1, salvage vs. clean start)
**Executor:** Claude Code session 2 · **Date:** 2026-06-07
**Source repo:** `~/Documents/pnn-multilayer/` @ commit `e2eec80` (2026-06-06), read-only — not modified.
**Method:** full read of the five assigned modules + their actual dependency targets
(`channels/mrr_primitives.py`, `channels/mrr_platforms.py`, `channels/dynamic_soa.py`,
`adaptation/perturbation_gradient.py`, `equalization_multilayer.py` (header + crosstalk path),
sweep drivers, `tests/`), plus a repo-wide grep for any time-domain ring dynamics.

---

## 0. The load-bearing question, answered directly

> *Is `equalization_ringbank.py` a usable head start for the S0.1 oscillator↔ring mapping, or not?*

**No — not for the mapping core.** Two reasons, both structural:

1. **It contains no ring physics.** It is a ~150-line task wrapper: it subclasses
   `MultiLayerEqualizer` (the fiber-equalization stack) and swaps the MZI meshes for
   `MRRWeightBank` from `channels/mrr_primitives.py`. The ring physics lives there, so that file
   is the real assessment target (§1.1 below).

2. **The ring physics it delegates to is static, not dynamical.** Every MRR primitive in the repo
   models the ring as a **steady-state (CW) transfer function applied memorylessly per sample**:
   - `MRRWeightBank` (`mrr_primitives.py:186`) is not even a Lorentzian — it is a trainable
     complex diagonal weight `y = t·e^{jφ}·z` in *transmission space*, deliberately bypassing
     pole/κ/detuning parameterization (per its docstring, following Tait-2018 heater→transmission
     LUT control convention; "No Lorentzian inversion appears in the gradient path").
   - `CascadedMRR_RC` (`mrr_primitives.py:349`) applies the through-port Lorentzian
     `T(δ) = (a·e^{jδ}−t)/(1−a·t·e^{jδ})` as a **scalar multiplication per sample** — the CW
     response at fixed detuning, with `a = 1` (lossless; loss plumbing marked "future v0.2",
     never landed). Time-independent by construction (`forward` docstring says so).
   - `FCDRingActivation` (`mrr_primitives.py:465`) is again the static Lorentzian, modulated by a
     slow **carrier-density** ODE that is integrated in `torch.no_grad()` and detached.

   A repo-wide grep for coupled-mode/round-trip/ring-state dynamics confirms: **the optical field
   is never a dynamical state anywhere in `pnn-multilayer`.** The only dynamical states are
   carrier densities (FCD `_I_FC`, SOA log-gain `h`) — slow envelopes modulating static optical
   transfer. This is the correct regime for that project (symbol rate ≪ ring linewidth, where a
   ring has *no* optical memory) and exactly the **opposite** regime from an SSM, which exploits
   the ring *as* a memory element. What S0.1 needs — the temporal coupled-mode equation
   `ȧ = (−κ_tot + iΔω)a + √κ_ext·s_in(t)`, whose pole *is* the LinOSS recurrence — **does not
   exist in the codebase and must be written new under either D-1 ruling.**

**However** (and this materially changes the salvage calculus): the recon found several mature,
tested assets *outside* the assigned list that map directly onto S0.3/S0.4a/S0.5 — most notably a
clean SPSA implementation with forward-pass accounting, a rate-equation gain model with an
autograd-checkpointed unrolled variant, and the SiN platform-constants registry. See §2.

---

## 1. The five assigned modules

### 1.1 `equalization_ringbank.py` (+ its real target, `channels/mrr_primitives.py`)

- **What it does:** `RingBankEqualizer` = `MultiLayerEqualizer` with `MRRWeightBank` replacing the
  MZI mesh per layer; adds dual-baseline SOA eval plumbing (instantaneous at train, dynamic at
  eval), thermo-optic drift injection hooks, and a dual-pol SU(2) wrapper (`ParallelPolRingBank`).
- **Dependencies:** `channels.mrr_primitives`, `equalization_multilayer` (the entire 43 kB
  equalization stack: SOA sigmoidal param clamps, O-E-O losses, `[N, batch]` conventions),
  `physics.soa_activation`, eval-time `channels.dynamic_soa`.
- **Entanglement:** total, by design — it exists to slot ring banks into the fiber-equalization
  pipeline (QPSK/PAM, BER/SNR@FEC, dual-pol). The 10 useful lines are the MRRWeightBank delegation.
- **Ring-pole exposure:** none. Neither the wrapper nor `MRRWeightBank` exposes
  $s=-\kappa_\text{tot}+i\omega_\text{res}$ or even (κ, detuning) — transmission-space is the
  trainable quantity, deliberately.
- **Verdict: `rewrite`** (do not lift the wrapper). Within `mrr_primitives.py`: the static
  Lorentzian transfer functions are **`lift-as-is` as unit-test references** — the CW limit of the
  new dynamical CMT model must reproduce them (S0.0/S0.1 gate tests); the `BaseMRR.drift_inject`
  machinery (pm/K → dimensionless detuning conversion, seeded per-ring Gaussian, bit-identical
  zero-drift path, distribution tests) is **`lift-with-adaptation`** for the S0.3 drift knob
  (hours).

### 1.2 `equalization_mrr_rc.py` (+ `sweep_phase4a_mrr1/2/3`)

- **What it does:** Kühl-2025 cascaded-MRR reservoir computer: fixed static ring cascade →
  per-ring PD intensities → delay-embedding → **closed-form Tikhonov ridge readout**
  (`w = (ΦᵀΦ + αI)⁻¹Φᵀy`), plus a 21-tap FFE baseline. The sweeps are the Phase-4a drivers
  (ring-bank vs mesh; Kühl RC reproduction; FCD-ring R* boundary).
- **Dependencies:** `channels.mrr_primitives`; sweeps additionally pull Manakov fiber / EML O-band
  channels, BER utils, carrier recovery — all task-specific.
- **Reusable for S0.3 substrate?** The cascade: no (static, see §0). The **ridge readout +
  delay-embedding** (~120 self-contained lines): yes — it is precisely the §5.3
  **reservoir-readout baseline** machinery for the S0.5 bake-off, re-pointed at state read-outs of
  the new substrate. Note its `_reservoir_features` re-implements the ring loop *inline* because
  `CascadedMRR_RC.forward` doesn't expose intermediate state — an API lesson for the new substrate
  (estimators, esp. adjoint/RHEL, need full state trajectories exposed).
- **Verdict:** readout + embedding **`lift-with-adaptation`** (~½ day); cascade **`rewrite`**
  (becomes the new substrate with training frozen); sweeps **`rewrite`** for content, but the
  orchestration skeleton (pre-registered grid → job list → `mp.Pool` → resume-safe keyed JSON →
  `--quick/--dry-run/--summary-only` → `summarize`) is the house pattern the bake-off runner
  should copy (~½ day to strip one driver, `mrr1` is the cleanest, into a generic runner).

### 1.3 `batched_engine.py`

- **What it does:** trains M models simultaneously: parameters stacked `[M, n_mzis]`, state
  `[M, batch, N]`, vectorized MC noise trials with per-trial σ vectors, per-model losses summed,
  per-model seeded re-init (`init_model_params`), per-model classifiers.
- **The assigned question — is "direct MZI application" baked in?** **Yes.** The forward is
  `apply_mzi_layer_direct(state, port_i, port_j, thetas, phis, …)` (`batched_engine.py:21`) —
  port-pair indexing and (θ, φ) parameterization are structural, and `BatchedPNN` hard-codes the
  MZI nonlinearity menu and classification heads. There is no abstraction layer separating the
  batching engine from MZI physics.
- **What survives:** the *pattern* — stack M parameter sets, one vectorized forward, per-model
  loss reduction, per-trial σ broadcast, seeded per-model re-init. That is exactly what 4–8-seed
  bake-off cells (esp. SPSA's 8+ seeds) need, and re-implementing it for a LinOSS/ring recurrence
  is *easier* than for MZI meshes (the oscillator update is (block-)diagonal element-wise algebra —
  batching is a clean einsum, no port scatter/gather).
- **Verdict: `rewrite`** (pattern-level salvage only; ~1–2 days as part of the new engine, low
  risk).

### 1.4 `evaluate.py`

- **What it does:** the Paper-1 fixed evaluation protocol — multi-σ phase-noise MC accuracy for
  MZI-mesh classifiers (`get_mzi_count`, `optical_depth`, `mesh.thetas/phis` clamping inside its
  training loops) + JSONL experiment logging.
- **Reusable as-is for the bake-off?** No — it is welded to MZI-mesh classification and its noise
  axis is MZI phase noise σ; the bake-off's axes are loss/gain/ASE and its primary metric is
  sample-efficiency-to-target-accuracy (forward-pass cost), which this file has no concept of.
- **Verdict: `rewrite`.** Keep the JSONL append/load pattern (~50 lines, trivial). The bake-off
  evaluator must be built around: (i) physical-forward-pass accounting per method, (ii) the
  pre-registered S0.2 target accuracy, (iii) loss/gain/ASE sweep axes.

### 1.5 `physics.py`

- **What it does:** two distinct things. (a) MZI primitives + six mesh topology generators +
  `PhotonicMesh`/`PhotonicNeuralNetwork` (lines ~140–880) — MZI-specific. (b) **The gain/noise
  primitives** (lines ~57–136): `photodetect`, `modReLU`, `saturating_absorption`,
  `soa_activation` (phase-preserving `G·z/(1+α|z|²)`), and `soa_activation_with_ase` —
  physically-scaled ASE injection (`P_ase = n_sp·max(G_eff−1,0)·hν·B_opt`, complex Gaussian per
  element).
- **Feed the S0.3 substrate:** (b) is directly the substrate's **gain-saturation and
  ASE-injection knobs** in memoryless per-step form — to be applied per round trip *inside* the
  new recurrence rather than per symbol between layers. **`lift-as-is`** (~80 self-contained
  lines, torch-only).
- **Not reusable now:** the mesh machinery — though `PhotonicMesh` is a plausible *later* lift for
  the B/C input/output coupling mesh (proposal §3 maps B, C to a thermo-optic MZI mesh) and for
  S0.7 hardware-realism. Shelve, don't port.
- **Verdict: split — gain/noise functions `lift-as-is`; MZI mesh `not-needed-now` (shelf); PNN
  wrapper irrelevant.**

---

## 2. Finds beyond the assigned list (these change the salvage calculus)

| Asset | What it is | Why it matters for Stage 0 | Verdict / effort |
|---|---|---|---|
| `adaptation/perturbation_gradient.py` (260 ln) | **SPSA** (2 forward passes, ±1 Bernoulli dither, optional Adam) + per-param FD validation variant + `compare_fd_vs_autograd` + **`n_forward_equivalents` fair-compute accounting** | This *is* the S0.4a SPSA estimator, chip-convention-aligned (Spall; Pai; Bandyopadhyay). The forward-pass accounting is literally the bake-off's primary-metric bookkeeping; the FD-vs-autograd harness is the template for the cosine-error secondary diagnostic. Validated in Phase 2e G3 at <1 % RMS vs autograd on a static channel. | **`lift-with-adaptation`** — decouple 2 contact points (hard-coded `compute_nmse_field` loss → injected loss fn; `model.forward_batched` API). ~½ day incl. re-running the FD validation on the new substrate. |
| `channels/dynamic_soa.py` (589 ln) | Agrawal rate-equation gain `ḣ = (h₀−h)/τ_c − (e^h−1)P/E_sat`: forward-only screening version, per-mode matched version, **`TrainingAwareDynamicSOAPerMode`** — autograd *through* the Euler rollout with **gradient checkpointing** (chunked; memory O(n_chunks)), Newton steady-state init | Gain saturation **with carrier dynamics** for the S0.3 substrate (the instantaneous `soa_activation` is its memoryless limit — good, the substrate gets both fidelity tiers). The checkpointed-unroll pattern is exactly what PAT's digital twin / the BPTT reference needs over long sequences. | **`lift-with-adaptation`** (~1 day) — re-house as an in-loop gain element; **add ASE injection inside the loop** (the dynamic classes have no ASE; only the instantaneous `_with_ase` variant does — small new work, and the per-round-trip ASE accumulation is new physics to get right). |
| `channels/mrr_platforms.py` (131 ln) | `PlatformConfig` registry: `SiN_LIGENTEC_AN800` (0.03 dB/cm, Qi 2×10⁶, FSR 100 GHz, n_g 1.95, 14 pm/K, dn/dT 2.45×10⁻⁵), Si, InP entries + FSR self-consistency check | Direct S0.1/S0.3 input: named, sourced SiN constants with a consistency test. | **`lift-as-is`** (+ hours to add CORNERSTONE SiN and a literature ultra-high-Q SiN entry; note Qi=2×10⁶ is conservative foundry-grade vs the proposal's Q>10⁷ class-leading figures — parameter *ranges* for S0.3 are a Supervisor/pre-registration decision, the schema carries them fine). λ_ref hard-coded 1550 nm (also in `mrr_primitives` drift conversion) — fine for us. |
| Thermal-crosstalk model (`equalization_multilayer.py:214–340` + `sweep_phase2d_crosstalk.py`, `tests/test_phase_crosstalk.py`) | Spatially-correlated (κ) phase noise + rigid drift on thermo-optic phases, eval-time, seeded/reproducible | The proposal §12 explicitly calls these findings "directly on-point" for SiN thermo-optic tuning + SPSA crosstalk-robustness. Implementation is MZI-phase-specific; the noise *model* (correlated Gaussian + rigid offset on thermo-optic parameters) transfers to ring detunings/couplings. | **`rewrite-with-pattern`** on ring detunings (hours). |
| `tests/test_mrr_primitives.py` (16 tests) + `test_mrr_gradient_sanity.py` | Energy conservation, Madsen N=2 series-cascade match, far-detuned identity, FSR repetition, drift distribution, zero-drift bit-identity, gradient-isolation | Test-design template for the new substrate's unit tests (the executor instructions require exactly this kind of kernel testing); several tests port nearly verbatim once the CW-limit references are lifted. | **`lift-with-adaptation`** (hours, alongside the substrate). |
| Phase 2e online-adaptation sweep (`sweep_phase2e_online.py`) | SPSA tracking a drifting channel vs offline L-BFGS bound, with strategy/drift-rate/seed grid | Direct methodological precedent for "SPSA absorbs drift/crosstalk" claims in the bake-off; also shows how `PerturbationAdaptor` is driven. | Read-reference only (content task-specific). |

---

## 3. What does NOT exist (new code under either ruling)

The entire Stage-0 *core* is new regardless of D-1 — the salvage decision touches only the periphery:

1. **Time-domain dynamical ring model** (temporal CMT: pole as recurrence), single ring → coupled
   lattice — the S0.1 forward model. *Nothing to fork; the existing static Lorentzians serve as
   its CW-limit test references.*
2. **LinOSS / D-LinOSS layer** (oscillatory SSM, IMEX discretization, learnable damping) + the
   oscillator↔ring parameter mapping.
3. **The S0.3 shared substrate** as an integrated object: finite-Q loop + in-loop saturating gain
   + per-round-trip ASE accumulation (+ drift/crosstalk knobs), with state trajectories exposed.
4. **PAT** (physical forward / digital-twin backward, twin-mismatch characterization).
5. **Recurrent in-situ adjoint** (time-domain/cavity adjoint, gain interaction).
6. **RHEL + the concrete χ³-FWM echo/phase-conjugation sub-model** (pump/bandwidth/efficiency/
   added-noise penalties + fidelity/systematic terms) — no echo or conjugation code exists anywhere.
7. **Bake-off evaluator** around sample-efficiency-to-target-accuracy (forward-pass accounting
   exists in the SPSA class; the protocol does not).
8. Generic batched multi-seed engine for recurrent models (§1.3 pattern rewrite).

One **anti-pattern warning** for the new code: the repo's house style for dynamics
(`FCDRingActivation`, `DynamicSOA`) integrates ODEs in `no_grad` and detaches — correct for
forward-only channel models, but **fatal if naively copied into the substrate**, where gradients
must flow through the optical state for the BPTT reference and PAT twin.
`TrainingAwareDynamicSOAPerMode` is the right pattern to copy instead.

---

## 4. Overall recommendation

**(a) Salvage — selectively** (recommendation only; D-1 is Lucas's ruling).

**Rationale.** The original "likely liftable" list (D-2026-06-05-1: ring/MRR model, batched
engine, gain/SOA + crosstalk tooling) is **half right, and the recon re-scopes it**: the ring/MRR
forward models and the batched engine are *not* liftable for the SSM core (static transfer
functions; MZI application baked in), but the **SPSA estimator with forward-pass accounting, the
rate-equation gain with its autograd-checkpointed unroll, the SiN platform registry, the
drift-injection machinery, the ridge-readout baseline, the static Lorentzians as test references,
and the sweep/orchestration skeleton** are mature, *tested* code mapping directly onto S0.3, S0.4a
and S0.5 — roughly 1.5–2.5 k lines that would otherwise be rewritten with fresh bugs and a
re-validation burden (the SPSA <1 %-vs-autograd anchor, energy-conservation tests, Critic-reviewed
drift conversion). That is perhaps 25–40 % of the expected Stage-0 codebase by volume — but ~0 %
of the S0.1 mapping core, which is new either way. So neither a wholesale fork nor a purist clean
start is right: copy the named assets into the new repo with provenance headers
(`pnn-multilayer @ e2eec80`, file path), decouple their 1–2 contact points each, re-run their
tests, and build the core fresh around them.

**Effort, either way:**
- **Selective salvage:** ~1 day to port + decouple + re-test the named assets into the new repo
  skeleton; core development proceeds on top.
- **Clean start:** the same core development **plus** ~3–5 days re-implementing SPSA+accounting,
  rate-equation gain (incl. checkpointed autograd variant), platform registry/drift conversion,
  and the orchestration/eval scaffolding — plus re-establishing their validation anchors from
  scratch. No offsetting benefit identified: the liftable assets are small-surface,
  dependency-light (torch-only after decoupling), and already match the project's quality
  conventions.

**Suggested salvage manifest (if (a) is ruled):**

| # | Source | → New-repo role | Verdict |
|---|---|---|---|
| 1 | `adaptation/perturbation_gradient.py` | S0.4a SPSA estimator + FD/autograd diagnostic + pass accounting | lift-with-adaptation |
| 2 | `physics.py` lines ~57–136 (gain/ASE/NL functions) | S0.3 instantaneous gain + ASE knobs | lift-as-is |
| 3 | `channels/dynamic_soa.py` | S0.3 dynamic in-loop gain; checkpointed-unroll pattern for PAT/BPTT | lift-with-adaptation |
| 4 | `channels/mrr_platforms.py` | SiN constants registry (extend entries) | lift-as-is |
| 5 | `mrr_primitives.py`: static Lorentzians + `drift_inject` + tests | CW-limit test references; S0.3 drift knob | lift-with-adaptation |
| 6 | `equalization_mrr_rc.py` ridge readout + delay-embed | §5.3 reservoir-readout baseline | lift-with-adaptation |
| 7 | One sweep driver skeleton (`sweep_phase4a_mrr1`) + `evaluate.py` JSONL pattern | bake-off runner scaffolding | rewrite-with-pattern |

Not lifted: `equalization_ringbank.py`, `batched_engine.py`, `evaluate.py` protocol,
`equalization_multilayer.py`, all channel models (fiber/IMDD/EML), MZI meshes (shelved for a
possible B/C-mesh / S0.7 reuse later).

---

*Read-only task: no Project_SSM code was written, no salvage performed, `pnn-multilayer`
untouched. Awaiting Lucas's D-1 (salvage vs clean start) and D-2 (`git init`) rulings before S0.0.*
