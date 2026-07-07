# F8 — per-method hardware-requirements ledger (S0.4-close deliverable)

**Status: written at S0.4-close (Supervisor, 2026-07-07, single-session mode).** Feeds Gate-ii's
hardware-simplicity axis (PR-9 promotion criterion (b)), the S0.7 envelope (E/O channel counts +
pump budgets), and Stage-1 planning. Everything here is *architecture-derived* from the frozen
substrate (PR-4) + the S0.4 estimator builds; no new physics assumptions. Roadmap S0.4-close
verbatim: "observables, actuators, added components + their loss, calibration burden."

Common to ALL methods (the shared plant): N-ring SiN lattice, per-ring thermo-optic δ heaters
(N) + tunable κ_ext couplers (N) + chain μ couplers (N−1); the resolved input map B = 4 drive
E/O channels (S0.4-0, charged to the envelope); Er gain + pump; 1 drop-port readout chain
(photodiode + ADC at 2 GS/s) for the R2 intensity y(n); digital head (8-tap FIR, trained
digitally everywhere).

| Axis | **SPSA** | **PAT** | **Recurrent adjoint** | **RHEL** |
|---|---|---|---|---|
| **Observables needed** | scalar loss from y(n) only | y(n) trace only | y(n) **+ per-parameter interference readouts** (the ∇θ readout: local taps or scanning — the Hughes-Fan intensity measurement at each tunable element) | y(n) **+ per-parameter ∇θH readouts along the echo** (local intensity/cross-terms at each δ/μ/κ element, per step) |
| **Actuators beyond the plant** | none (dither = the existing heaters) | none | **counter-propagating error-injection port(s)** (coherent, phase-stable vs forward) | **conjugator bank** (N pumped arms) + **error-nudge E/O injection at the readout port(s), coherent, per echo step** |
| **Added components + loss** | none | none | circulators/taps for the reverse pass (~0.5–1 dB class each crossing); backscatter-separation from the K-pol-3 doublet **unsolved** (debt #4) | N-arm χ³ spiral bank + pump lasers (**N × 0.3 W ≈ 9.6 W on-chip at C-2**, PR-11) + pump-rejection filters per arm + extraction/re-injection routing (η_ex² ≈ 0.73 energy, already in η_c) + layer transitions (ULL↔tight-confinement geometry conflict, PR-11 ⚠verify-4) |
| **Calibration burden** | phase/actuation maps NOT needed (model-free); needs only actuator repeatability | **the digital twin**: full parametric characterization at the PR-5 accuracy class (κᵢ, γ, actuation maps, gain pair) — the M-par families ARE this burden, priced in-data | phase-coherent alignment of the adjoint field with the forward frame; per-element readout calibration; reciprocity verification under gain | conjugation fidelity/phase (φ_err) calibration per arm; pump power servo ×N; echo timing (τ_c) alignment; per-element ∇θH readout calibration |
| **Passes/update (PR-7/7.1)** | 2 | 1 (+2 digital) | 2 | **4** (2 fwd + 2 echo; 2 conjugation events) |
| **E/O channels → envelope** | 4 (drive) | 4 (drive) | 4 + error-injection channel(s) | 4 + error-nudge channel(s) + N pump arms |
| **Demonstrated on chip?** | yes (chip-demonstrated class; crosstalk-robust — the pnn-multilayer finding) | yes (Wright 2022 class) | **no recurrent demonstration** (debt #4 — the count charges the pass *as if* realizable) | no; the conjugation primitive itself is the unsolved element on SiN (§5.2) |
| **Hardware-simplicity rank (this table, qualitative)** | **1 (simplest)** | **2** (digital-side burden only) | 3 | **4 (heaviest by far)** |

## Notes for PR-9 promotion criterion (b)

- Neither adjoint nor RHEL can win "strictly simpler hardware ledger" — both add components and
  calibration the workhorses don't need; promotion for them can only run through criterion (a)
  (≥25 % efficiency + CI). This is a *structural* reading of the table, recorded before the
  bake-off stats.
- SPSA's row is the quiet asset: zero added components, zero model burden — if it lands within
  the PR-3 margin at acceptable pass counts, the Stage-1 chip needs nothing but the plant.
- The S0.4b/S0.4c sim-model limitation disclosures (adjoint optimistic-bound; RHEL
  dissipative-echo bias) ride along wherever this table is cited.
