# S0.7 exclusions ledger — literature-sourced magnitudes (2026-07-27)

**Author:** Supervisor (single-session mode; retrieval by a delegated web agent, page-level
fetches where marked VERIFIED). **Purpose:** the four items the S0.7 envelope deliberately
excluded (laser wall-plug, resonance locking, control compute, packaging) were registered as
*unbudgeted*. This ledger bounds their magnitude from primary sources so §7 can state
"excluded, magnitude ≈ X per named source" instead of a bare exclusion. Status per number:
**VERIFIED** = page-level fetch of the stating document; **UNVERIFIED-direct** = search-snippet
only, page-level re-check registered pre-submission (same protocol as the EdgeDRNN/FWM
verifications). *Derived* = our arithmetic on sourced numbers, labelled.

## 1. Laser wall-plug (C-band, mW-class on-chip)

| number | source | status |
|---|---|---|
| 12.2% waveguide-coupled WPE at ~10 mW, 1550 nm, uncooled (best-in-class hybrid Si/III-V ECL) | Lee et al., Opt. Express 23(9), 12079 (2015), 10.1364/OE.23.012079 | VERIFIED |
| Butterfly single-frequency: 40 mW fiber-coupled at 300 mA × 1.5 V = 0.45 W diode (≈8.9% WPE) + TEC 0.18 W | Thorlabs SFL1550S/P user guide 21060-D02 Rev F spec table | VERIFIED |
| Tunable module class (micro-ITLA): ≈1.2 W typ / 3.6 W max module draw incl. TEC + control | PurePhotonics PPCL500 datasheet, Table 2 | VERIFIED |
| Cross-check: Lumentum micro-ITLA 2.0 W typ / 3.0 W EOL | Lumentum TTX1995 datasheet | UNVERIFIED-direct |
| Benchtop ECL: 40–60 W controller draw (Toptica DL pro class); Santec TSL-570 100 VA | Toptica service KB; Santec TSL-570 datasheet | VERIFIED (both) |
| Het.-integrated SiN laser: >10 mW in-waveguide, no WPE stated; *derived* WPE order 2% (~0.45–0.6 W for ~10 mW) | Xiang et al., Nat. Commun. 12, 6650 (2021) | VERIFIED (paper); derived |

**Derived envelope (ours):** mW-class on-chip power with 3–6 dB coupling ⇒ **~0.2–0.6 W
wall-plug in the integrated class** (incl. TEC hold); **40–100 W in the benchtop class**.

## 2. Resonance locking / stabilization

| number | source | status |
|---|---|---|
| PDH lock-box: Toptica DigiLock 110 ≈13.5 W max | DigiLock 110 manual (±15 V rails) | UNVERIFIED-direct |
| Moku:Lab 20 W typ / Moku:Go 15 W typ (Laser Lock Box platform) | Liquid Instruments KB "Moku Power Consumption" | VERIFIED |
| FPGA PDH: Red Pitaya STEMlab 125-14 ≤10 W (5 V/2 A); Linien lock software | Red Pitaya docs; Wiegand et al., Rev. Sci. Instrum. 93, 063001 (2022) | UNVERIFIED-direct (RP); VERIFIED (Linien) |
| Ring locking demos (Si, heater power only): 31 rings locked at 212 mW total (≈6.8 mW/ring); 14-ring CROW at 64.9 mW (≈4.6 mW/ring); control electronics power not reported (bench instruments) | Jayatilleka et al., Optica 6(1), 84–91 (2019) | VERIFIED (all three numbers) |
| SiN thermo-optic holding: conventional P_π ≈ 20–30 mW; 8 mW/π silicon-rich folded spiral; ~1 mW/π class (dense spiral / suspended) | arXiv:2111.07890 (quote verified); Nejadriahi et al., Opt. Lett. 46(18), 4646 (2021); Opt. Lett. 50(11), 3768 (2025) | VERIFIED / VERIFIED / UNVERIFIED-direct |

**Note:** the Jayatilleka numbers are silicon photoconductive-heater results — quote SiN holding
power from the P_π rows, and the lock-*electronics* overhead from the instrument rows.

## 3. Control compute (kHz-class SPSA update loop)

| number | source | status |
|---|---|---|
| MCU class: STM32F407 238 µA/MHz ⇒ ≈0.13 W at full 168 MHz (upper bound; kHz loop needs far less) | ST DS8626 | UNVERIFIED-direct |
| FPGA class: Red Pitaya ≤10 W; Moku:Go 15 W typ | above | as above |
| SBC class: RPi 4B measured 2.7 W idle / 6.4 W full load (PSU spec 5 V/3 A) | RPi 4B datasheet RP-008341-DS §4.1 (VERIFIED) + pidramble.com measurements (VERIFIED, independent) | VERIFIED |

## 4. Packaging

| number | source | status |
|---|---|---|
| SiN edge coupling: 0.15 dB/facet (UHNA-7) and ≈1.5 dB/facet (SMF-28) published best | Micromachines 16 (2025), PMC12734521 | VERIFIED |
| LIGENTEC process ≈1 dB/facet (lensed fiber); <1.5 dB via photonic wire bonds | arXiv:2504.00311v2 (secondhand statement); LIGENTEC PR 2024-09-16 | VERIFIED (quote) / UNVERIFIED-direct |
| MPW grating couplers (honest floor): CORNERSTONE 300 nm SiN <10 dB/grating (TE, 1.57 µm) | CORNERSTONE platform documentation | UNVERIFIED-direct |
| TEC holding at near-ambient: 0.18 W typ (butterfly, T_case 25 °C); module class Qmax 5.8 W | Thorlabs 21060-D02 (VERIFIED); TEC Microsystems 1ML06-017-03 (UNVERIFIED-direct) | mixed |

## Consequence for §7 (stated in-text)

The **integrated-class excluded stack** — hybrid laser 0.2–0.6 W + TEC hold 0.18 W + MCU-class
control 0.13 W, before any locking electronics (FPGA class ≤10 W) — totals **~0.5–1 W**, which
is the *same order as the budgeted N = 128 photonic power itself* (~0.9 W at 450 pJ/sample ×
2 GS/s). Charging it compresses the positive cells' ~15× Brainwave margin toward single digits;
a benchtop realization (40–100 W laser + instrument lock) erases the niche outright. The §7
niche verdict therefore carries a fourth condition alongside the heater class: an
integrated-class realization of all five excluded items (§5 below, added 2026-09-13). Direction of every number is against
the photonic side, consistent with the registered only-shrinks-positive-cells rule — negative
findings are unaffected.

**Dropped as unsourceable (recorded per protocol):** "DFB WPE 18%@10 mW → 35%@250 mW"
(search-attributed to arXiv:2310.01615; the paper does not contain it); per-ring lock-electronics
power in the Jayatilleka papers (not reported).

## 5. Gain pump — the fifth excluded item (ADDENDUM 2026-09-13, found at the Stage-0b re-envelope)

The S0.7 envelope charged conversion + heaters; the substrate's Er:Si₃N₄ gain stage (g = 0.9 κᵢ at
every ring, PR-4 §G) needs a 1480/980 nm pump that no row above carried. Rows and statuses in
`docs/s0b/s0b_0_ledger.md` §2 (Liu et al. Science 2022 absorption/gain/lifetime VERIFIED; transparency
intensity derived from two UNSOURCED inputs; Lumentum 5050 WPE ≥ 13.9 % VERIFIED from datasheet
maxima). **Magnitude:** 0.24–2.4 mW optical ⇒ **0.8–17 mW electrical per ring**, i.e. 26–550 mW at
N = 32 plus a cooled pump module (0.18 W TEC). Direction: against the photonic side (shrinks positive
cells only) — the registered only-shrinks rule holds, negative findings unaffected. **Consequence for
§7.1:** "four known exclusions" → five; the integrated-realization condition covers all five. The
S0b.0 re-envelope (`results/s0b_0/`, PR-20) prices both the pumped and the passive (undoped)
configurations; the product configuration is passive.
