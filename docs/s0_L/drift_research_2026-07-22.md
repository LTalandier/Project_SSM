# Drift-mechanism literature research — 2026-07-22 (for a pre-registered drift model)

**Purpose:** source realistic slow-drift magnitudes/timescales for SiN microrings + Er:SiN gain,
to build a pre-registered drift model testing whether in-situ retraining beats offline-deploy
once a once-calibrated recurrence goes stale (the axis that can break the §5.5 offline-tie null).
**Method:** deep-research workflow (5 angles → 20 sources → 76 claims → 25 adversarially verified,
21 confirmed / 4 refuted). Single-session mode. Every number below is 3-0 or 2-1 verified against
a primary source; refuted numbers are listed so they are NOT used.

## Anchor number (the staleness clock)

- **Free-running SiN microcavity resonance drift ≈ 341 MHz std over 24 h** in a temperature-
  stabilized lab; **≈ 470 MHz** open-loop under an injected heater perturbation. Confirmed SiN
  device, FSR 76 GHz, **loaded Q ≈ 3×10⁶ → linewidth ≈ 64 MHz**. So free-running drift is
  **several cavity linewidths per day** (≈12 linewidths/day at our C-2 linewidth ~28 MHz).
  — Dacha et al., "Frequency-stable nanophotonic microcavities via integrated thermometry,"
  Nature Photonics 2025/26; **arXiv:2506.21692**. [3-0]
- **This is the closest true analogue to our regime** (unlocked high-Q SiN ring) and should anchor
  the model. Our C-2 (Q_i=6.8×10⁶) sits in the same tens-of-MHz-linewidth regime.

## What active stabilization removes (the offline-lock ceiling)

- Integrated thermometry feedback: 341 → **13.7 MHz std** (~25×), **<0.8 pm RMS over days**
  (~100 MHz residual; ceiling set by thermometer contact-resistance drift — the ONLY
  heater/actuator-drift datum in the set). DFB laser locked to it: **±0.5 pm over 50 h** (48×).
  — arXiv:2506.21692. [3-0]

## The coefficients (set the magnitude; material constants, stable)

- **dn/dT(Si₃N₄) = 2.45×10⁻⁵ /K** (measured, stoichiometric LPCVD, 1550 nm); SiO₂ cladding
  0.95×10⁻⁵ /K (~2.6× smaller). Thick well-confined ULL waveguide: dn_eff/dT ≈ material value.
  — Arbabi & Goddard, Opt. Lett. 38(19):3878 (2013) [primary]; reproduced arXiv:2506.21692. [3-0 ×5]
- **Resonance-T sensitivity 1.2–1.9 GHz/K**: 1.23 GHz/K (COMSOL, ULL geometry; = 6.11 MHz/mW
  self-heating at R_th=4.98 K/W) to 1.86 GHz/K (measured conventional ring, 14.9±0.1 pm/K, linear
  15–70 °C). **Consequence: ~1 mK ambient wander → ~1.2–1.9 MHz shift; ~6 MHz per mW absorbed.**
  — UCSB/Morton (suppl. to Nat. Commun. 12, 934); MDPI Photonics 13(4):371. [3-0 ×2]

## Locked residual drift rates (bound the offline-lock case)

- **1.5–10 kHz/s residual detuning drift (≈5–36 MHz/hr)** for locked integrated-SiN references:
  1.54 kHz/s single PDH lock → 51 Hz/s with dual-mode temp locking (Zhao, CLEO 2021 STh2B.7);
  5 kHz/s SiN-coil-locked ECTL (Heim, Nat. Commun. 2025); ~10 kHz/s random-walk from ambient
  (UCSB, Nat. Commun. 12, 934). [3-0 / 3-0 / 2-1]
- **Allan floors**: 1.7×10⁻¹⁰ at ~1000 s (dual-mode lock; drift-dominated beyond); 1.8×10⁻¹³ at
  6.4 ms (coil lock). Past the ADEV minimum, residual detuning grows ∝τ. [3-0 ×3]
- Best-case common-mode bound: two lasers on ONE ring hold their beat to <900 kHz over 10 h
  (67 ppm) — but common-mode-suppressed (~83×), so it UNDERSTATES absolute drift. Lower bound only.
  — ACS Photonics 2025, 5c01183. [medium, single source]

## HARD DATA GAPS (must be modeled from analogue or flagged unquantified)

- **(d) Er:SiN gain aging / photodarkening / pump-drift: NO SiN-specific data exists.** Both leading
  Er:Si₃N₄ amplifier demos (Liu et al. Science 2022 abo2631; Rönn et al. Opt. Express 28:27919, 2020)
  are **static single-session gain characterizations** — zero aging/degradation/long-term/Allan data.
  Negative existence verified against full text. [3-0 ×2] → fill from silica-EDFA / Er:Al₂O₃ /
  Er:LiNbO₃ analogues or leave the amplifier drift term explicitly unquantified.
- **(c) Thermo-optic heater/actuator drift + hysteresis + thermal-crosstalk stability: no SiN datum**
  except the integrated-thermometer contact-resistance drift capping the <0.8 pm/days ceiling.
  → our own `pnn-multilayer` thermal-crosstalk findings are the best available analogue.

## OPEN QUESTIONS that decide whether drift breaks the tie

1. **Spatial correlation across the N=32 rings** — is free-running drift **common-mode**
   (whole-chip temperature wander, largely absorbable by a single global thermometer AND by our
   offline arm's on-device head recalibration) or **ring-independent** (scrambles the coupled
   eigenstructure — only recurrence retraining fixes it)? **All measured numbers are single-cavity.
   This correlation structure is the crux: it is exactly what determines whether offline-deploy
   keeps up.** Must pre-register BOTH regimes.
2. **Short-time (s-to-min) drift PSD of an unlocked ring at operating power** (incl. self-heating
   at 2 GS/s) — bridges the 24-h aggregate to the kHz/s locked rates. Not measured anywhere.

## Refuted (do NOT use)

- "187.56 MHz/K cavity temperature sensitivity" [0-3]. Soliton-comb "stable for hours / ~200 kHz
  over 5 min" passive-stability claims [0-3]. Back-out of "~4×10⁻⁵ single-laser instability at 1 s"
  from the 83× common-mode factor [0-3].

## Bottom line for the drift model

Free-running SiN drift is **aggressive and well-sourced (341 MHz/24 h, ~12 linewidths/day)** — a
genuine staleness clock that favors in-situ retraining on its face. But whether it **breaks the
offline-tie depends entirely on the common-mode-vs-independent correlation structure (open Q1),
which the literature does not measure.** Honest design: pre-register BOTH correlation regimes,
state the expected effect for each, and let the sweep decide. The Er-gain and heater-hysteresis
terms are literature gaps — model from analogue (pnn-multilayer for crosstalk) or flag unquantified.
