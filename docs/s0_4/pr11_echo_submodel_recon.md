# PR-11 recon — the RHEL χ³-FWM echo / phase-conjugation sub-model (menu → freeze at the S0.4c spec)

**Status: RECON (Supervisor, 2026-07-07, single-session mode).** This memo is the PR-5-pattern
recon behind the PR-11 preregistration block: it lays out the concrete conjugation-mechanism
menu with quantified penalty rows and proposes the freeze; **the numeric freeze happens in the
S0.4c task spec (committed before any RHEL run), after the ⚠verify items below are checked.**
Calculations: `analysis/pr11_echo_recon_calc.py` → `results/s0_4c/pr11_recon_calc.json`.

**Provenance:** proposal §5.2 + §6(c) (echo must commit to a concrete mechanism or an explicit
off-chip admission — "no idealized conjugation operator"); roadmap S0.4c (irreversibility
invariants + unit test); ledger PR-11 row (invariants already registered); PR-7 row 4 (1 fwd +
1 echo = 2 device passes; χ³ penalties charged to accuracy-per-pass, not the count).

---

## 1. What the echo sub-model must model (RHEL semantics)

RHEL (Pourcel & Ernoult, arXiv:2506.05259; HEB: López-Pastor & Marquardt, PRX 13, 031020)
trains by a **physical echo**: forward evolution over the sequence, then a **time-reversal
operation on the optical state — phase conjugation —** then a second (echo) evolution through
the *same* physics, with the error signal injected as a perturbation; local interference
carries the update. Working reading (⚠**verify-1** against 2506.05259 at S0.4c build time):
the conjugation is applied **once, to the 2N-mode intracavity state at t = T** (a snapshot
operation between the two passes), not continuously to the propagating drive.

**This reading fixes which bandwidth the conjugator must span** — the decisive quantity:

| requirement | band |
|---|---|
| conjugate the **state snapshot** (working reading) | the pole band: δ-spread ± κ_net ≈ **131 MHz (C-1) · 38 MHz (C-2) · 9 MHz (C-3)** |
| conjugate the **drive stream** (rejected reading, kept as the ⚠verify-1 alternative) | the 2 GS/s input band ≈ **2 GHz** in every cell |

If ⚠verify-1 lands on the drive-stream reading, the resonant option (B) is dead outright and
option (A)'s dispersion window still covers it — the menu survives, the numbers move.

## 2. The freezable sub-model structure

One echo update = **1 forward device pass + C_op + 1 echo device pass** (PR-7: 2 passes). The
conjugation operator, per mode j of the 2N doublet state:

```
C_op:  a_j(T)  →  √η_c,j · e^{iφ_err,j} · a_j(T)*  +  n_conj,j
```

- **η_c,j** — end-to-end conjugation efficiency (energy), the product chain of the chosen
  mechanism (extraction × conversion × re-injection × timing decay; §3). May be
  mode-dependent (band-edge rings conjugate worse) — the freeze states the profile.
- **φ_err,j** — systematic conjugation phase error (pump-phase / path-length systematics).
- **n_conj,j** — added conjugation noise, **≥ the phase-insensitive parametric floor**
  (conjugation is phase-insensitive: the idler carries ≥ 1 vacuum-unit penalty; ⚠**verify-2**
  the exact η<1 form) **+ pump-transfer excess** (pump RIN/ASE transfers to the idler at ×2 in
  field for the degenerate single-pump scheme).
- **Gain-restore (optional, in-model):** the echoed state re-amplifies through the substrate's
  own Er gain during the echo pass — which injects **fresh ASE** exactly as the substrate
  already models. No separate operator; no free re-amplification.

**Invariants (registered in the PR-11 ledger row — bind the implementation):**
1. Independent forward/echo ASE streams — fresh generators, **no common-RNG reversal** (the
   harness tag convention already enforces this shape).
2. **No loss-sign flip:** the echo pass propagates through the *same* dissipative substrate —
   κ_net stays a decay in the echo direction.
3. Gain injects fresh ASE in the echo pass too.
4. **Unit test:** the echo of a noisy forward must **not** recover the noiseless initial state
   — recovery error lower-bounded by (conjugation fidelity × ASE floor).

## 3. Mechanism menu (quantified)

Baseline nonlinearity: γ_nl = 2πn₂/(λA_eff) ≈ **0.97 W⁻¹m⁻¹** for tight-confinement Si₃N₄
(n₂ ≈ 2.4×10⁻¹⁹ m²/W, A_eff ≈ 1 µm²; ⚠**verify-3**). Single-pass small-signal conversion
η_spiral = (γ_nl P_p L)²:

| P_p (on-chip, CW) | L | η_spiral |
|---|---|---|
| 0.1 W | 0.5 m | 2.4×10⁻³ (−26.3 dB) |
| 0.3 W | 0.5 m | 2.1×10⁻² (−16.7 dB) |
| 1.0 W | 0.5 m | 2.4×10⁻¹ (−6.3 dB) |
| 0.3 W | 2.0 m | 3.4×10⁻¹ (−4.7 dB) |

### (A) On-chip shared-spiral conjugator (extraction → FWM → re-injection) — **proposed headline**

The state is extracted through each ring's bus port (ring-down over a few τ_net), conjugated in
a pumped spiral, re-injected. **Physics note:** phase conjugation of the extracted ring-down
train *time-reverses it into the matched re-injection waveform* — extraction and injection
efficiencies are symmetric (the same η_ex).

Penalty chain (energy): **η_c = η_ex · η_spiral · η_ex · e^(−κ_net·τ_c)** with, at θ₀
(computed): η_ex = 2κ_ext/κ_net = **0.86** (all cells — θ₀ sets the ratio), so
η_ex² ≈ 0.73. At P_p = 0.3 W / 0.5 m and τ_c ≈ τ_net: **η_c ≈ −18 to −20 dB.**

Honest costs (all F8-ledger / envelope items):
- **N parallel arms** — the ring fields overlap spectrally (δ-spread ~ ±κᵢ), so they are *not*
  wavelength-separable: one pumped arm per ring. **Total pump = N × P_p ≈ 9.6 W on-chip for
  C-2 at the 0.3 W point.** This single number is the honest headline cost of on-chip RHEL.
- **Geometry conflict:** the ULL dilute/thin-core SiN the recurrence wants (C-3-class Qᵢ) has
  A_eff ≫ 1 µm² → γ_nl ~10× smaller; the tight-confinement conjugator spiral is a *different*
  waveguide geometry (layer transitions, taper loss) on the same chip (⚠**verify-4**:
  per-platform γ_nl for the actual CORNERSTONE/LIGENTEC ULL geometry).
- Pump lasers + amplifiers (EDFA ASE onto the pump transfers to the idler), pump-rejection
  filters per arm.

### (B) Resonant conjugator ring — the registered enhancement↔bandwidth tension, quantified

A conjugator ring buys intracavity pump build-up (η ∝ enhancement⁴-class) at the price of
linewidth. Under the state-snapshot reading the conjugator must span the pole band, giving a
**loaded-Q ceiling** Q_L ≤ ν/Δν_state: **1.5×10⁶ (C-1) · 5.0×10⁶ (C-2) · 2.2×10⁷ (C-3)** —
i.e. resonant enhancement is *not* trivially excluded for the state band (it IS excluded, by
~×70, under the drive-band reading — ⚠verify-1 decides). Still second to (A) because: the same
N-arm multiplicity applies (spectrally overlapping modes), each conjugator ring must be
actively tuned onto its source ring (N extra heaters + calibration — F8), and the enhancement
claim needs a specific demonstrated SiN-ring FWM operating point (⚠**verify-5**) before it can
be frozen. Kept as the recorded alternative, not the headline.

### (C) Off-chip conjugation — the explicit admission, priced

Off-chip (HNLF / PPLN) conjugation is efficient and broadband, but the state must survive the
round trip: **amplitude survival e^(−κ_net·τ_transit)** at 10 ns (≈2 m fiber + conjugator):
**0.12 (C-1) · 0.54 (C-2) · 0.87 (C-3)** — before facet losses (~1–3 dB × 2–4 crossings × N
channels) and N-channel parallelism (same spectral-overlap argument). The **storage/timing
primitive the admission must state** (roadmap S0.4c verbatim): there is none available — the
state cannot be held while the conjugator works; the transit decay IS the price. Off-chip is
therefore only even conceivable for C-3-class cells, and stays an admission, not a mechanism.

## 4. Proposed freeze (for the S0.4c spec, after ⚠verify-1..5)

- **Mechanism = (A) shared-spiral bank**, headline parameters: P_p = 0.3 W/arm, L = 0.5 m,
  τ_c = τ_net, η_ex from the live θ₀ (computed, not assumed) → η_c ≈ −18 dB class, uniform
  profile across modes (mode-dependence = a registered sensitivity row); n_conj = the
  ⚠verify-2 quantum form + a pump-transfer excess term; φ_err = 0 headline + a registered
  sensitivity row. **N-arm pump total flows to the S0.7 envelope** (as the S0.4-0 E/O channels
  did).
- **(B)** recorded as the quantified alternative (revisit only if ⚠verify-1 confirms the
  state-band reading AND ⚠verify-5 produces a demonstrated operating point).
- **(C)** recorded as the explicit off-chip admission with its transit-decay pricing; not run
  in the bake-off headline.
- **Both F22 conclusion templates** (RHEL competitive / RHEL fails-under-honest-echo)
  pre-drafted in the S0.4c spec before any run.

## 5. What S0.4c builds

1. `C_op` conjugation stage (η_c chain, φ_err, n_conj) + the echo pass in the harness
   (fresh ASE tags; invariants 1–3 by construction).
2. The **PR-11 unit test** (invariant 4: noisy-forward echo ≠ noiseless state, bounded below).
3. The RHEL estimator per 2506.05259 (⚠verify-1 settles the update rule + injection point).
4. Smoke gates mirroring S0.4a/b (trainability + ledger + floor check: as η_c → 1, n_conj → 0,
   ASE → 0, the echo update must approach the exact gradient — the roadmap floor check).

## ⚠verify ledger (before the S0.4c freeze — none are load-bearing for this memo's structure)

1. **RHEL echo semantics** — ✅ **RESOLVED 2026-07-07** (arXiv:2506.05259 abstract + HTML body,
   fetched same day). Findings, which **supersede §1's working reading where they differ**:
   - **Conjugation = a single instantaneous state-snapshot operation** at the forward/echo
     boundary: Σ_z·Φ = (φ, −π) — momentum flip; for an optical field, **phase conjugation of
     the snapshot**. The §1 working reading is CONFIRMED → the conjugator spans the **state
     band**, and option (B)'s Q_L ceilings stand.
   - **THREE passes per update, not two:** forward + echo(+ε) + echo(−ε) — the gradient is the
     **symmetric finite difference** of ∇_θH between the two nudged echo trajectories,
     Δθ ∝ −(1/2ε)(∇_θH[Φᵉ(t,+ε)] − ∇_θH[Φᵉ(t,−ε)]) integrated over the echo. **The signed PR-7
     row-4 count (1 fwd + 1 echo = 2) is corrected by amendment PR-7.1** (RHEL = 3 device
     passes/update). Consequence for this sub-model: **C_op fires TWICE per update** (each echo
     pass starts from its own physical conjugation event — fresh η_c, φ_err, n_conj each), and
     each echo pass carries fresh ASE.
   - **Inputs are replayed time-reversed** during the echo; the **error enters as a continuous
     nudge force −εJ∇_Φℓ throughout the echo pass** (not a boundary kick) — physically a
     modulated optical error drive at the readout ports during the echo → **error-injection E/O
     channels are an envelope cost** (same class as the S0.4-0 multi-tap drive channels).
   - RHEL is stated for **non-dissipative Hamiltonian systems**; the authors do not treat
     dissipation — the bake-off's dissipative substrate tests exactly this extrapolation.
   - Demonstrations: coupled harmonic oscillators + Hamiltonian SSM stacks (HRUs, leapfrog),
     seq-length ~50k — the LinOSS-adjacent regime, good news for task comparability.
2. **Phase-insensitive conjugation quantum-noise form at η_c < 1** (idler vacuum penalty).
3. **n₂ / γ_nl sources** for Si₃N₄ (Ikeda 2008 / Moss 2013 class numbers).
4. **γ_nl of the actual ULL foundry geometry** (CORNERSTONE/LIGENTEC dilute core) + transition
   losses to a tight-confinement conjugator layer.
5. **Demonstrated SiN FWM operating points** (spiral + microring conversion efficiencies at
   stated pump powers), for whichever of (A)/(B) survives.
6. **W-class CW power handling** on-chip SiN (thermal/damage) for the N-arm pump total.
