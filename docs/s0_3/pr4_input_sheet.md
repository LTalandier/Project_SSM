# S0.3-0 — PR-4 input sheet (task 5): the menus the freeze chooses from

**Author:** Executor · **Date:** 2026-06-10 · **Status:** input to the **PR-4 PROPOSED block**
(Supervisor drafts; **Lucas freezes**). **Menu, not choice** — every section presents options
with provenance + sizing arithmetic; none is selected here. Evidence base:
`docs/s0_3/substrate_recon.md` (cited per row as R§n); arithmetic:
`analysis/s0_3_0_recon_arithmetic.py` → `results/s0_3/s0_3_0_recon_arithmetic.json` (all S0.1 /
PR-10 anchors reproduced — R§5).

PR-4 must register (ledger row + Notes carry-ins): the **(α,Qᵢ) operating pair** (D-08-1), the
**κ_ext policy**, the named **"realistic SiN noise" cell** (Q/α + NF + ASE level), the
**roughness/splitting sub-parameter** evaluated at operating κ_ext (D-08-3), a **holding/trim-
statistics convention** (EV-F1), and an **input-drive-power / intracavity-energy normalization**
(PF-F8f). Foundry-grade gates Gate ii; class-leading is a labelled aspirational sweep axis.

---

## 1. Candidate noise cells (pair × NF/n_sp × ASE convention)

### 1.1 The NF/n_sp axis (R§1, debt #3 discharged-informative)

| Option | NF (dB) | n_sp | Evidence class |
|---|---|---|---|
| NF-A | 7.0 | 2.5 | **measured on-platform** (flagship, fiber-referenced) [EV] |
| NF-B | 5.0 | 1.58 | measured band of nearest integrated hosts (LNOI 4.49–5, EDWA 4.5, Al₂O₃ 5.6–6.5) [EV/AV] |
| NF-C | 3.0 | 1.0 | quantum floor (Caves) — **aspirational label only** |

### 1.2 The ASE-injection convention (the substrate's noise mechanism — convention, not physics)

- **A1 — per-round-trip discrete injection:** complex Gaussian field kick per rt per ring,
  variance ⟨|δa|²⟩ = n_sp·(G_rt−1) photons (G_rt = per-rt power gain of the gain element).
  Matches the discrete-time rollout; the table below gives the magnitudes.
- **A2 — continuous Langevin term** in the CMT ODE: ⟨F(t)F*(t′)⟩ = 2κ_g·n_sp·δ(t−t′) (per
  mode, photon units), discretized by the integrator. Equivalent to A1 at first order in
  κ_g·dt (per-rt gains here are ≤0.2 dB → the two differ at O(10⁻³) relative — a convention
  choice, not a fidelity fork). A2 composes naturally with the ZOH/van-Loan exact
  discretization (S0.1); A1 with the per-rt rollout.
- Either way (PR-11 carry-in): **fresh draws per pass, forward and echo streams independent.**

### 1.3 ASE magnitudes at the candidate cells (kernel output; photons/rt/mode)

At net gain = 90 % of intrinsic loss (the S0.1 plot's deep-compensation convention):

| Pair | NF 3 dB | NF 5 dB* | NF 7 dB | steady-state intracavity ASE photons (90 % comp, NF 7) |
|---|---|---|---|---|
| P-CORN | 4.8e-2 | ~7.6e-2 | 1.2e-1 | ≈ 23 |
| P-FND | 5.5e-3 | ~8.7e-3 | 1.4e-2 | ≈ 23 |
| P-AN800 | 1.6e-3 | ~2.5e-3 | 4.0e-3 | ≈ 23 |
| P-UHQ | 3.6e-4 | ~5.8e-4 | 9.1e-4 | ≈ 23 |

*NF-5 column interpolated (kernel tabulates 3/4.5/6/7 dB; JSON carries all).
Steady state n_ss ≈ n_inj/rt ÷ (2κ_net·dt_rt); at 90 % compensation κ_net = 0.1κᵢ the
accumulation factor is 5× the passive memory in rt — the per-corner injection and accumulation
exactly offset, so **n_ss is corner-independent (~23 photons at NF 7 / ~9 at NF 3)**; what
differs per corner is the *signal* energy the same drive builds up (→ the PF-F8f normalization,
§5, decides the SNR bookkeeping).

### 1.4 Assembled candidate cells (the menu rows PR-4 names)

| Cell | Pair | NF | ASE conv. | splitting sub-param (§3) | role |
|---|---|---|---|---|---|
| **C-1 "foundry-deployable"** | P-FND (Qᵢ=2e6 / 0.172 dB/cm) | NF-A 7.0 | A1 or A2 | γ per process class; knob per §3 policy | **the Gate-ii candidate cell** (ledger: foundry-grade gates Gate ii) |
| **C-2 "demonstrated mid"** | P-AN800 (0.051 dB/cm / 6.8e6) [AV — verify primary at freeze, R§2a] | NF-A 7.0 | same | **knob ON even clean-process** (2γ/κ_tot=1.66 undercoupled, R§3b) | demonstrated-numbers sensitivity cell |
| **C-3 "aspirational"** | P-UHQ (Qᵢ=3e7) | NF-B 5.0 | same | knob ON (split until r≥3) | labelled aspirational sweep axis (EV-F3 N=128 lives here) |
| sensitivity axes | + P-CORN, P-MPW-MM (R§2a) | NF ∈ {3, 5, 7} | — | γ ∈ {0, 11.8, 90, 160 MHz} | reported, never headline |

**Gain-budget constraint on the cell choice (R§4f):** loss-compensation (net-gain 50/90 %
conventions) is **infeasible at P-CORN** with demonstrated Er:Si₃N₄ gain (headroom ×0.7–1.3
unloaded, <×0.5 loaded) — if PR-4 keeps a CORNERSTONE cell it is a **passive-only** cell.
P-FND closes with ×1.9–3.7 headroom at r=1.

---

## 2. κ_ext policy options (vs the B3 bound + the frozen PR-2 cells)

Ladder arithmetic at P-FND (the Gate-ii candidate; full per-pair tables in the JSON; memory in
**samples**, 1/e amplitude):

| r = κ_ext/κᵢ | mem @ 1 GS/s | mem @ 2 GS/s | drop eff. | 2γ/κ_tot (sub-low γ=90 MHz) | vs T-A 7-tap @ 2 GS/s | vs PR-13 k-grid @ 1 GS/s |
|---|---|---|---|---|---|---|
| 0.1 | 2.74 | 5.49 | 0.028 | 3.10 split | ✗ (5.5 < 7) | k=1 in; k=3 marginal (×1.1 over); k≥10 out |
| 0.3 | 2.06 | 4.11 | 0.141 | 2.33 split | ✗ | k=1 in; k=3 ×1.5 over |
| 1 | 1.10 | 2.19 | 0.444 | 1.24 split | ✗ | k=1 in; k=3 ×2.7 over |
| 3 | 0.47 | 0.94 | 0.735 | 0.53 OK | ✗ | k=1 marginal |
| 10 | 0.16 | 0.31 | 0.907 | 0.18 OK | ✗ | all out |

(P-FND **passive** memory is already only 6.58 samples @ 2 GS/s — the registered "honestly
marginal" T-A cell; *any* loading pushes it below the 7-tap span. The T-A-at-foundry story
therefore couples to the κ_ext choice harder than to NF. At P-UHQ the same ladder keeps
14.1 samples @ 2 GS/s even at r=3 — above the 7-tap span with the splitting knob OFF-able, R§3b.)

- **K1 — fixed deep-undercoupled (r ≈ 0.1):** max memory (83 % of passive); drop efficiency
  0.028 → the readout SNR cost is the PF-F8f mechanism's problem; **most splitting-exposed**;
  most reliant on the §5 normalization being honest.
- **K2 — fixed near-critical (r ≈ 1):** the balanced cell (44 % drop eff.); foundry memory
  1.1–2.2 samples at GS/s clocks (T-A at foundry dies; PR-13 k≤3 only).
- **K3 — fixed moderate overcoupling (r ≈ 3):** splitting-suppressed on subtractive-low at the
  foundry corner (0.53); SNR-rich (0.735); memory-poor. The "single-pole-by-engineering" option.
- **K4 — trainable κ_ext within registered bounds [r_min, r_max]:** folds the B3 trade into the
  recurrence training (κ_ext is a B1 pole-real-part actuator); **requires** (i) the PR-2 v2 F6
  hygiene (reservoir baseline holds κ_ext at the θ₀ policy value — already frozen), (ii) the
  PF-F8f normalization (else training buys SNR through κ_ext — the F6 contamination channel),
  (iii) the splitting sub-parameter re-evaluated across the *whole* registered range (the knob
  validity must hold at r_min, the most-split end).

---

## 3. Roughness/splitting sub-parameter (D-08-3 blessed constraints → concrete options)

**γ menu (R§3a):** 0 (ideal) · 11.8 MHz (damascene-clean [AV]) · 90 MHz (subtractive-low [EV])
· 160 MHz (subtractive-high [EV]). No AN800/CORNERSTONE-specific γ exists (re-checked; absence
row R§3a) — the registered γ is a **process-class assumption, stated as such**.

**Knob default policy (R§3c):**
- **K-pol-1 (blessed default, confirmed + sharpened):** ON except *foundry-Q + clean-process*;
  the sharpening — **P-AN800 does not qualify for OFF even clean-process** (1.66 undercoupled).
- **K-pol-2 (κ_ext-conditional OFF):** OFF wherever 2γ/κ_tot < 1 at the registered (γ, r) —
  cheaper, but couples the knob's validity to the κ_ext freeze (re-open one ⇒ re-open both).
- **K-pol-3 (always ON, γ registered per cell; γ=0 recovers single-pole exactly):** one code
  path, most honest, ~×2 ring-update cost; same 2×2 machinery the coupled-μ hook needs anyway.

**The joint condition PR-4 must state explicitly (ledger carry-in):** if the substrate's
single-pole abstraction is claimed anywhere, it must name the cell (process class + Q + r) where
2γ/κ_tot < 1 — at every other cell the knob is ON.

---

## 4. Holding/trim-statistics convention (EV-F1 carry-in)

For the substrate's standing-power bookkeeping (heater trim holding) → Gate-ii hardware ledger +
S0.7-full; EV-F1 showed the convention flips a class-A envelope verdict, so it must be frozen,
not implied:

- **H1 — full-P_π worst case:** every heater charged P_π/2-class holding at max trim. Most
  conservative; the envelope's CONS reading.
- **H2 — expected-value P_π/2** (uniform trim distribution): the envelope's OPT reading; the
  EV-F1 flip case (OPT×A clears Brainwave in-window under H2 only).
- **H3 — measured-distribution convention:** defer to Stage-1 calibration data; Stage 0
  registers H1 *or* H2 with H3 named as the upgrade path.

(PR-4 registers one for the substrate's power/energy side-ledger; the envelope already reports
both corners — the freeze makes the *substrate's* convention explicit rather than inherited.)

---

## 5. PF-F8f — input-drive-power / intracavity-energy normalization (concrete mechanisms)

The requirement (frozen carry-in): **the digital encoder must not be able to buy SNR against
the registered noise cell**, in either arm (SSM and reservoir baseline alike).

- **O1 — registered input-power budget (bus-referenced):** freeze P̄₀ = per-sequence mean
  optical power at the bus input (and a peak bound P_pk for 4-PAM headroom); the encoder's
  digital→optical scale is **fixed**, not trainable; the substrate asserts P̄ ≤ P̄₀ per sequence
  (a clamp + a logged assertion, not a trainable path). *Cheapest; one number.* Weakness: the
  same P̄₀ builds κ_ext-policy-dependent intracavity energy (drop eff. table §2) — cross-policy
  SNR comparisons skew unless κ_ext is also frozen (fine under K1–K3; leaky under K4).
- **O2 — registered intracavity-energy budget:** freeze E₀ = steady-state Σⱼ|aⱼ|² at the cell
  (photon units); the encoder scale is *derived* per κ_ext policy to hit E₀ under the task's
  stationary statistics (closed-form for stationary inputs — cheap in simulation; its hardware
  analogue is a calibration convention, flagged for Stage 1). *Normalizes across κ_ext policies
  (incl. K4); the natural partner of the corner-independent n_ss (§1.3) — SNR then compares
  cells honestly.* Weakness: one more derived map to validate (unit test: E(E₀-normalized
  drive) = E₀ within tolerance).
- **O3 — registered budget + trainable bounded digital pre-gain:** P̄₀ as in O1 plus trainable
  g_dig ∈ [0, g_max] with P̄₀·g_max = the cell's registered ceiling, g_dig counted in the
  trainable partition and the PR-7 energy side-ledger. *Most flexible (lets training spend
  headroom);* the bound IS the normalization — g_max must bind to the same ceiling or it is the
  contamination channel reopened.

Interaction rows: PR-7 (energy/pass accounting charges the optical drive at the registered
budget); PR-10 (modulator-drive rows price the same P̄₀); PR-6 (both arms get the identical
budget); B3/K4 (O2 is the only option that stays comparison-clean under trainable κ_ext).

---

## 6. Joint-adjudication notes (what couples with what — for the freeze discussion)

1. **D-08-1 ⇄ EV-F3 ⇄ splitting (the two-against-one, R§2b):** N=128-in-band exists only at
   P-UHQ at r ≲ 1 — exactly where clean-process 2γ/κ_tot = 2.4–7.3 (split). So PR-4 can have
   at most two of {N=128 in-band, class-leading-Q, splitting-knob-OFF}. Escape hatches, both
   register-able: (a) N=128 with knob ON (the doublet *is* the model — costs the 2×2 path);
   (b) N=128 at r=3 (knob marginal-OFF, memory 14.1 samples @ 2 GS/s — still above T-A's 7-tap
   span, packing 44 in-band at 2 GS/s < 128 though — so (b) actually fails packing; **(a) is
   the only true N=128 option**). If neither is palatable, the deployable N-grid is {8, 32}.
2. **Gain budget (R§4f):** any cell that wants the 50/90 % compensation conventions must sit at
   P-FND or above; P-CORN is passive-only.
3. **The Er-regime fork (R§4e, flagged):** PR-4 (or a ledger note) should name the registered
   gain-model class — M1 static-saturated (SiN-native, in-loop physics linear + ASE) vs M3
   rate-equation (III-V fallback, per-symbol nonlinearity). This decides what the estimators
   face and what the PAT twin omits; it is a Supervisor/ledger call, not an Executor default.
4. **PF-F1 echo:** under M1 the substrate's task-solving nonlinearity is the readout |·|² —
   the same structure the Critic's linear floor argument lives on (R§4e); the PR-2 readout pin
   (R1 single-quadrature vs R2 intensity) becomes the substrate's nonlinearity choice too.
5. **D-2026-06-08-1 closure:** the pair menu (R§2a) + packing (R§2b) + splitting-at-r (R§3b) +
   gain budget (R§4f) are all the inputs that parked decision named; it can now be adjudicated
   on numbers at the freeze, jointly with the κ_ext policy and the splitting sub-parameter.
