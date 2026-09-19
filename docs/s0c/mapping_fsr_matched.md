# S0c.0-a — Mapping memo: the ring lattice in the FSR-matched, low-Q regime (2026-09-15)

> **2026-09-19 audit:** Historical memo retained. Its current interpretation is superseded by
> `docs/s0c/audit_2026-09-19.md` (arithmetic, mapping, budget, and prior-art corrections).

**Purpose.** State how the P1 mapping (S0.1: coupled-mode ODE → ZOH-discretized diagonal SSM) carries
over when the rings are operated at power coupling K = 5–20 % instead of the registered r = κ_ext/κ_i ≤ 3,
what changes, what the existing code can and cannot be trusted for, and what the trainable set is.
Arithmetic only; every number derivable from the registry (`photonic_ssm/platforms.py`, C-2: FSR 100 GHz,
R = 242.2 µm, n_g 1.97, 0.051 dB/cm, Q_i 6.8×10⁶) or from the rows in `fsr_matched_regime.md`.

## 1. The ring as a discrete-time first-order section
A single all-pass ring (one bus, one coupler, round-trip time T_rt = 1/FSR = 10 ps) with field
coupling κ = √K, through-coupling t = √(1−K), round-trip amplitude transmission a = 10^(−α_rt/20)
(α_rt = 0.051 dB/cm × 1.52 mm = 0.0078 dB ⇒ a = 0.9991) and round-trip phase φ has the transfer function
$$H(z)=\frac{t-a\,e^{j\varphi}z^{-1}}{1-t\,a\,e^{j\varphi}z^{-1}},\qquad z=e^{j\omega T_{rt}},$$
i.e. **one pole at $p = t\,a\,e^{j\varphi}$** — magnitude set by the coupler (a ≈ 1 is negligible),
angle set by the detuning heater — and one zero at $a e^{j\varphi}/t$ (all-pass to within the loss).
In the sampled state-space form with the sample period equal to T_rt this *is* the diagonal SSM
recurrence $x_{k+1} = p\,x_k + \ldots$ of S4D/LinOSS with $|p| = t a$: the "damping" knob of §6 is now
the coupler, and the box extends from r ≤ 3 (|p| ≈ 0.996 per round trip at C-2) to |p| ≈ 0.89–0.975.

| K | t = |p|/a | memory 1/(1−|p|) [round trips] | FWHM ≈ FSR(1−|p|)/π | K per FWHM at 14 pm/K |
|---|---|---|---|---|
| 5 % | 0.975 | 39 | 0.5 GHz | 0.29 |
| 10 % | 0.949 | 19 | 1.0 GHz | 0.60 |
| 20 % | 0.894 | 9 | 2.1 GHz | 1.2 |

## 2. Relation to the P1 model and where it stops being valid
The P1 substrate integrates the temporal coupled-mode ODE $\dot a = (j\delta - \kappa_{net}/2)a + \ldots$
and discretizes it by ZOH at dt = 1/f_s. CMT is the small-coupling limit of §1: $\kappa_{net} T_{rt}
= -\ln(t^2 a^2) \approx K + \alpha$, valid when $\kappa_{net} T_{rt} \ll 1$. Numerically:
K = 5 % ⇒ κ_net T_rt = 0.05 (CMT error ~ 1 %); K = 10 % ⇒ 0.105 (~3 %); K = 20 % ⇒ 0.22 (~6 %, and the
per-round-trip phase structure of the true response is no longer captured). **Rule for S0c.1:** the
existing `DissipativeRingSubstrate` may be used with κ_ext extended to K ≤ 10 % (r = κ_ext/κ_i ≈
κ_net T_rt/(κ_i T_rt) ≈ 0.1/0.00089 ≈ 110) *only with a transfer-matrix cross-check* (§1 exact
response vs the ZOH-CMT response at the trained operating point, registered tolerance); above 10 %
the delay-line model of §1 replaces it. The delay-line lattice model is ~50 lines (per-ring §1 section,
cascade product for the SJTU-type all-pass cascade, or the CROW transfer matrix for side-coupled chains).

**Sample rate vs FSR.** The ring's response is periodic in frequency with period FSR; the signal
band must fit inside one FSR (SJTU: 32–50 GHz inside 99.5 GHz). At f_s = 64 GS/s (±32 GHz) the
registered 100 GHz rings qualify; at 100 GBd the band equals the FSR (edge case, flagged). When
f_s ≠ FSR the sampled recurrence has a fractional delay; the ZOH discretization of the CMT ODE handles
that automatically, the delay-line model needs the exact continuous-frequency response sampled — both
fine, neither requires "one round trip per sample".

## 3. Gain
The Er:Si₃N₄ stage is **out**: at K ≥ 5 % the coupling dominates the loss by 50–200× and there is
nothing for gain to compensate; the product configuration is passive, undoped (unpumped Er absorbs
2 dB/cm). This also removes the fifth exclusion.

## 4. Insertion loss (the term that mattered on silicon)
At resonance the all-pass ring transmits $|T|^2 = \left|\frac{t-a}{1-ta}\right|^2$:
K = 5 %: 0.62 dB/ring; K = 10 %: 0.31 dB/ring; K = 20 %: 0.15 dB/ring (worst frequency; less
off-resonance). Eight rings: 1.2–5 dB; sixteen: 2.4–10 dB. Silicon at ~2 dB/cm gives ×40 (SJTU:
14.8 dB, hence their EDFA). This is the SiN advantage, and it is a **loss** advantage that becomes an
**energy** advantage only because the amplifier goes away.

## 5. Trainable set and actuation
Per ring: **detuning δ_j** (pole angle; heater or piezo; range needed ≈ one FWHM to a few, i.e.
0.5–5 GHz — piezo on SiN gives > 4 GHz at 20 V, V_FSR = 16 V) and **coupling K_j** (pole magnitude;
an MZI tunable coupler with one phase shifter — SJTU's construction; range 0–20 % needs ≈ π/4 of arm
phase). Lattice topology: (a) **cascade** of all-pass rings on one bus (SJTU; poles independent,
product of §1 sections — the diagonal SSM, N poles, N zeros); (b) **CROW** side-coupled chain (P1's
μ_chain; coupled poles; richer but the same N-pole bound). The **order bound** of PR-20b holds for
both: N rings ⇒ N poles ⇒ ≈ N degrees of freedom; on smooth channels (chromatic dispersion: quadratic
phase, flat magnitude) an N-section all-pass equals a FIR of ≈ η N taps with η measured, not assumed —
the SJTU device gives η ≈ 4 (8 rings ≈ 40 km at ~50 GBd ≈ 14 symbols of spread ≈ 28–32 FIR taps).

## 6. What is new relative to P1's mapping (for the paper trail)
- Same identification (pole angle ↔ δ, pole magnitude ↔ coupling), same discretization machinery,
  **different box**: |p| per round trip 0.89–0.975 instead of ≈ 0.996; memory 9–39 round trips instead
  of ~250; linewidth GHz instead of tens of MHz.
- Same trainable set (δ, κ_ext or K, μ), same estimators (PAT with a twin that is now a 50-line
  delay-line model; SPSA unchanged), same fairness contract.
- **Different physics of the hold:** a linewidth is 0.3–1.2 K, not 8 mK; with an athermal overlay
  (0.1–2 pm/K, UNVERIFIED-direct) it is 7–140 K.
- **Different neighbor:** a statically configured product-class device (SJTU 2024), not a
  reservoir or an MZI mesh. The W1 claim's wording carries over unchanged; the sweep in
  `whitespace_sweep_s0c.md` tests it in this regime.
