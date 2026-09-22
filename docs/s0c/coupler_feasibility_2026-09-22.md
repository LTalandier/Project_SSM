# Wide-coupler feasibility — 2026-09-22

**Decision:** the required coupling range is physically plausible with an ideal
balanced MZI, but a complete, sourced 100-GHz-FSR SiN implementation is not yet
established. The saved numerical design has demanding excess-loss and control
requirements. No hardware or product go follows. This audit and PR-23-D sensitivity
cost €0; no optimizer, paid fleet, external contact or publication was run.

## Sources and what they establish

| Primary source, accessed 2026-09-22 | Evidence | Limit for this design |
|---|---|---|
| [LIGENTEC technology page](https://www.ligentec.com/technology/) | Lists tunable MZIs/rings, record thermal tuning Pπ <15 mW, and an AN800 table with MZI rejection >22 dB and thermal Pπ <100 mW. | The page contains different performance tiers. Neither number is a measurement of our 16-control design; no joint coupler insertion-loss, length, bandwidth, thermal cross-talk or actuator-transfer specification is supplied. |
| [Liu et al., Chinese Physics B 31, 014201 (2022)](https://cpb.iphy.ac.cn/fileCPB/journal/article/cpb/html/2022/1674-1056/cpb_31_1_014201.shtml), DOI 10.1088/1674-1056/ac2e64; full HTML read | Demonstrates heater-tuned dual-interferometer SiN rings. Reported 700-µm ring length, 700-µm arm imbalance, 0.17 dB/cm propagation loss and 8 dB fiber coupling loss. | Its asymmetric, dual-bus structure is not our balanced single-bus section; coupling varies with frequency. It establishes device lineage, not a flat K=.33–.95 coupler across 64 GHz. No usable heater-power number was found in the text. |
| [Sommer et al., Optics Letters 49, 5332–5335 (2024)](https://opg.optica.org/ol/abstract.cfm?uri=ol-49-18-5332), DOI 10.1364/OL.533706; publisher abstract only | Telecom SiN electrostatic MEMS directional coupler: 0.67 dB insertion loss and 1.1±0.1 µs rise time. | Full article unavailable through the current access path. Required continuous K range, spectral S-matrix, leakage/driver power, footprint, and loss partition are unresolved. Abstract insertion loss cannot be equated to our symmetric per-pass loss model as a device prediction. |
| [Qiu et al., ACS Photonics (2015)](https://pubs.acs.org/doi/abs/10.1021/ph500450n); previously checked abstract | Athermal device reports 0.4 dB/cm propagation loss. | Different platform; retain only as propagation-loss sensitivity, never combine its drift with the bare-SiN loss as a demonstrated device. |

The existing PZT/PCM entries in `docs/s0b/s0b_0_ledger.md` remain component-level
references. Nanowatt actuator leakage does not price the high-voltage driver,
ring tuning range, or complete coupler. The 1 mW/π scenario is optimistic; this
audit does not verify a compact, sufficiently low-loss 100-GHz-FSR implementation.
No commercial availability or manufacturing yield is inferred from these sources.

## Mapping the saved design to controls

PR-23-C's best broad candidate uses K=.3282–.9500, all above the old .20 limit.
For an ideal balanced MZI, K=sin²(theta/2), so one differential phase control can
cover the required range. A single-arm phase shift also contributes common
phase theta/2. We compensate it with the ring trim
`phi_ring=(phi_saved-theta/2) mod 2pi`; the remaining constant through phase can
be absorbed by the receiver's complex scalar. Ignoring this coupling between
controls would mis-price and mis-quantize the device.

Two identical splitters with power split u have Kmax=4u(1-u). Reaching K≈.95
therefore requires u roughly between .388 and .612 in that simple model. This
is a necessary idealized range condition, not measured broadband accuracy.
For a .01 absolute K error tolerance, the bound |dK/dtheta|<=1/2 over ±32 GHz
requires differential arm delay <=.0995 ps (about 15 µm physical length mismatch
at assumed group index 1.97). Thermal dispersion, splitter wavelength dependence
and fabrication biases also matter; the bound does not validate them.

The entire 100-GHz round-trip delay is 10 ps, corresponding to about 1.522 mm
at group index 1.97. Coupler and tuning-section delay must fit within that total;
adding long phase shifters without changing the ring would change its FSR. The
public component records do not supply a complete compatible layout.

## Loss belongs inside the recurrence

With power coupling K, t=sqrt(1-K), amplitude survival s=10^(-ell/20), and
round-trip field q, model the coupler as the passive symmetric matrix
`S=s[[t,i sqrt(K)],[i sqrt(K),t]]`. Closing the feedback path gives

`H = s (t - s q) / (1 - s t q)`.

Thus coupler loss changes poles and zeros as well as through attenuation.
`tests/test_lossy_coupler.py` validates this expression against a separate 2×2
linear-system solve, its lossless limit, passivity and MZI common-phase mapping.
Actual unequal arm loss or dispersive complex S parameters need a richer model.

PR-23-D fixes the saved eight-ring controls and evaluates the stated loss grid.
It permits only receiver scalar fitting. The results are **frozen-candidate
sensitivity**, not reoptimized capacity or proof of impossibility. They include
3 dB packaging for insertion loss and receiver-noise accounting. Full numerical
outputs and a plot: `results/s0c_coupler/reading.md`.

At bare-SiN propagation loss, the .01 shape-error screen passes at .10 dB/coupler
(NMSE .00613) and fails at .20 (NMSE .01599). At .67 dB/coupler it is .12573,
with about 13.97 dB mean insertion loss including packaging. The .67 case is a
scenario inspired by a published insertion-loss scale, not a prediction of that
MEMS device. Receiver gain restores amplitude, not lost SNR.

The ideal zero-added-loss phase-quantization tests give NMSE .02736 at 6 bits,
.005064 at 8 bits, .002409 at 10 bits and .002396 at 12 bits. The tests quantize
both MZI differential phase and ring trim, then reconstruct their coupled phase.
Do not translate these into an unconditional DAC-bit or PCM-level requirement:
noise, transfer nonlinearity, hysteresis, drift and the available phase span are
absent. Loss and quantization tests are separate, not a verified joint window.

## Conditional power, not an energy verdict

Under zero cold-phase offsets and this MZI convention, the saved phases require
10.976 π-equivalents across eight coupler controls and eight ring trims. At
Pπ=15 mW this is 164.64 mW heater power. Adding the historical **assumed**
2 mW/control gives 196.64 mW, or 3.073 pJ/sample at 64 GS/s, before lock,
amplifier, monitoring and refresh costs. The public Pπ<15 claim is not a lower
bound: a better device could consume less. Fabricated biases or static trimming
could also change the allocation. The 1/15/60/100 mW scenarios remain separate.

Digital budgets in the output explicitly assume 16/32/64 taps and .03/.05/.15
pJ/tap/sample. They are not function-matched benchmarks. For illustration, a
64-tap block at .05 pJ/tap costs 3.2 pJ/sample; a threefold advantage would allow
only 68.27 mW total optical-system overhead at 64 GS/s. The 15-mW/π heater
scenario alone exceeds that budget. This cannot decide every device or workload.

## Next research gate

A credible continuation requires one compatible coupler/phase-shifter design with
complex transfer response across the occupied band, total group delay, excess
loss versus setting, phase precision, tuning range and hold/control power. Until
then, the source-backed device claim remains incomplete. A future simulation may
explicitly test assumed joint loss/precision and reoptimization, but must not
upgrade the assumptions into a demonstrated platform. Adaptive-drift comparisons
still need a separately frozen observation/noise model and an adapting baseline.
P1/P2 release artifacts are unchanged. No broader experimental outcome is claimed.
