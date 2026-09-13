# Thermal-management cost closes a registered inline SiN equalizer energy window

*Lucas Talandier — draft companion note to P1, 2026-09-13. Model calculation;
not submitted; standalone publication deferred in favor of including the result in P1. Source provenance is in the accompanying ledger; a publication
bibliography and independent source review remain release tasks.*

## Abstract

A successful simulation of in-situ training does not establish that a photonic
recurrence can replace a digital equalizer efficiently. We evaluate an inline
silicon-nitride ring-lattice envelope under a rule frozen before calculation,
pricing the digital competitor per equalizer tap. The best optimistic cell in
the registered 0.1–2 GS/s window reaches E_digital/E_photonic = 0.64, below both
parity and the registered threefold advantage threshold. Removing unsourced
optimistic assumptions lowers that maximum to 0.23; the conservative product
window reaches at most 0.38. Common-mode thermal management dominates even when
non-volatile actuators have zero holding power. The gate terminates further
product simulations and fabrication planning within this window. These are
conditional arithmetic bounds, not measurements of a device or a universal
limit on photonic signal processing.

## Question and registered model

P1 established simulation trainability and compared an initial photonic envelope
with digital block-level costs. Its deployed equalizer used only 6–8 of 32 rings,
so an advantage based on nominal state dimension remained unsubstantiated.
Stage 0b asks a different question: whether an inline optical filter can beat
the digital equalizer function it would replace when static costs are charged.

PR-20 froze the model and kill rule at commit `ee137c4`; calculated results were
recorded at `8931d6c`. The grid uses N = 8, 32, 128; rates 0.1, 1, 2 GS/s; and
4–128 digital taps. Actuator classes include thermal, piezoelectric, phase-change,
and hybrid cases. Pumped and passive cases, common-mode management options, and
maintenance estimates are included. Assumptions and verification status are in
[the source ledger](../docs/s0b/s0b_0_ledger.md), not newly measured in this note.

The calculation uses E_ph = P_total/f_s and E_dig = n_taps e_tap. Registered
per-tap coefficients are 0.05 and 0.15 pJ/tap/sample, with sensitivity values
0.03 and 0.25. Reachability is the registered single-ring memory proxy
floor(f_s/κ_net,min), not a demonstrated task capacity. The maximum ratio among
optimistic class-C configurations must reach 3 to continue. Failure terminates
S0b.1–S0b.3; no post-result threshold adjustment is made.

## Result

| Registered case | Best E_digital/E_photonic | Interpretation |
|---|---:|---|
| Optimistic class-C kill gate | 0.64 | Photonic energy ≈1.56× digital |
| Optimistic, unsourced rows removed | 0.23 | Photonic energy ≈4.35× digital |
| Conservative product-window gate | 0.38 | No cell reaches the 3× bar |

The optimistic best cell is passive C-3 with phase-change actuation, 64 reachable
taps at 2 GS/s, and a 10 mW global-heater assumption. Its thermal term alone costs
5 pJ/sample, against 3.2 pJ/sample for the digital equalizer. The 10 mW row is
explicitly unsourced and optimistic; removing such rows worsens the result.
The complete grid and mandatory sensitivities are available in
[the calculation record](../results/s0b_0/envelope.md), restored from the P1
reproduction bundle when necessary. No training simulation is run by this envelope.

## Interpretation and limits

Zero actuator holding power does not imply zero thermal-management power. In this
model, alignment to the external carrier remains a static cost. Charging an erbium
pump also worsens active-ring cases; pump power was a fifth omission in P1's
original component envelope and is now disclosed there. At the registered minimum
damping r=0.1606, the implemented pumped/passive memory ratio is
(1+2r)/(0.1+2r)=3.14, not ten.

The maintenance estimate uses optical sequence time and omits actual parameter
writes, settling, and controller latency. It is a lower-bound component estimate,
not evidence of inexpensive practical retraining. Added nonnegative costs cannot
improve the negative energy gate at fixed cadence. Accuracy at the assumed
maintenance cadence has not been demonstrated for this inline design.

At fixed tap count and power, increasing rate improves the energy ratio linearly.
Approximately quadratic improvement requires usable tap count to increase with
rate as well, before reaching capacity or grid limits. Consequently an extrapolated
higher-rate opening is a hypothesis, not a registered result. Filter shape, usable
capacity, actuation precision, drift, and trainability must all be established for
an actual workload. No such follow-up is initiated here.

The decision is scoped to this architecture, cost model, memory proxy, and rate
window. It supplies a reason to stop the registered product program, while leaving
P1's simulation study of training methods as a separate contribution. Any hardware
continuation would need a collaborator-led scientific objective and a new decision.

## Availability and review

Model: `analysis/s0b_0_envelope.py`; frozen rules: PR-20 in
`shared/preregistration.md`; inputs: `docs/s0b/s0b_0_ledger.md`; outputs:
`results/s0b_0/`. P1's `paper/repro/` archive preserves the output records with
SHA-256 checksums. The source ledger includes unverified and derived rows; this
note does not upgrade their evidence status. This draft and the associated repairs
were prepared in one session and do not constitute independent review.
