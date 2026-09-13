# S0b.0 ledger — actuator classes, gain pump, drift management, per-tap digital baseline

**Retrieved 2026-09-13 (single-session mode; the four retrieval subagents were rate-limited before
doing any work, so every row below was fetched and read in the main session).** Status convention
as `docs/s0_7/exclusions_ledger.md`: **VERIFIED** = read on the paper/datasheet text (PDF→pdftotext
or full-text HTML); **UNVERIFIED-direct** = abstract / search snippet / secondary; **derived** =
computed from stated numbers (arithmetic shown); **UNSOURCED-assumption** = a number this ledger
supplies without a primary source — every such row is removed in the PR-20 sensitivity re-statement.
Local copies of the PDFs read: session scratchpad (`liu2022.txt`, `fang_nnano22.txt`,
`ucsb_pzt_ofc22.txt`, `jin2018.txt`, `credo_ck.txt`, `mtk_df.txt`, `lumentum5050.txt`,
`horowitz2014.txt`, `nist_ersin.txt`, `chalmers_dsp.txt`).

## 1. Actuator classes (per control channel unless stated)

### 1A/1B — thermo-optic heaters (P1 classes, unchanged)
| number | source | status |
|---|---|---|
| Class A foundry heater: 60 (OPT) / 175 (CONS) mW/π; τ 38–110 µs | PR-10 frozen rows (2026-06-10) | frozen (P1) |
| Class B suspended / dense-spiral: ~1 mW/π; τ 0.4–2.6 ms | PR-10 frozen; **0.98 mW/π** in a 10-fold dense sinusoidal spiral, Opt. Lett. 50(11), 3768 (2025), PubMed 40445703 | frozen; 0.98 now VERIFIED (abstract) |
| Trim electronics (DAC quiescent) 2 mW/ch, class-independent | PR-10 frozen (C3) | frozen |

### 1C-pz — piezo-optomechanical on Si₃N₄ (PZT or AlN); *volatile, nW actuator, electronics-dominated hold*
| number | source | status |
|---|---|---|
| PZT-actuated Si₃N₄ ring: **Q = 7 million, 0.03 dB/cm, 20 nW consumption, 20 MHz bandwidth**; tuning **−1.6 pm/V** (≈ −200 MHz/V); **> 4 GHz detuning at 20 V**; leakage **< 1 nA** | Wang, Zhao, Rudy, Blumenthal (UCSB), OFC 2022 "Ultra-low loss silicon nitride ring modulator with low power PZT actuation…" (PDF, ocaqpi.ece.ucsb.edu) | VERIFIED |
| PZT-tuned Si₃N₄ ring, 580 µm radius: **V_FSR = 16 V, VπL = 3.6 V·dB, VπLα = 1.1 V·dB, tuning current < 10 nA, flat to 1 MHz** | Jin, Polcawich, Morton, Bowers, Opt. Express 26(3), 3174 (2018) (PDF, siliconphotonics.ece.ucsb.edu) | VERIFIED |
| AlN-on-Si₃N₄ (PORT): **20 pm at 60 V, 0.5 nA (≈ 30 nW)**, loaded Q 64,000 on that device; first bending mode 1.1 MHz | Dong, Tian, Zervas, Kippenberg, Bhave, IEEE MEMS 2018, arXiv:1903.08479 | VERIFIED (abstract) |
| AlN-on-Si₃N₄ microcomb control: **300 nW**, flat actuation to MHz, "high linearity and low hysteresis" | Liu et al., Nature 583, 385 (2020), arXiv:1912.08686 | VERIFIED (abstract) |
| AlN: DC current < 1 nA, "tens of nano-Watts"; 15.7–32 MHz/V (unreleased), ~50 MHz/V (released), 480 MHz/V (bottom-up); **Q₀ > 15×10⁶ unchanged with AlN**; "a small hysteresis is observed" (AlN); PZT actuation limited < 1 GHz by loss tangent | Tian et al., review "Piezoelectric actuation for integrated photonics", arXiv:2405.08836 (full text) | VERIFIED (review text; primary refs inside it not re-read) |
| PZT hysteresis region **0–1.5 V** (blue-light ring, 760 MHz/V outside it, 5 nW at 5 V) and **0–3 V** (1.01 GHz/V outside it) | UCSB CLEO 2025 SS1O.5; arXiv:2601.15695 | UNVERIFIED-direct (search snippets) |
| **Hold electronics for a volatile nW actuator** (the real hold cost): OPT **0.1 mW/ch** (multiplexed HV-DAC + sample-and-hold, refreshed at the nA leakage rate); CONS **2 mW/ch** (the frozen per-channel DAC row) | OPT end: this ledger; CONS end: PR-10 C3 | OPT = **UNSOURCED-assumption**; CONS = frozen |
| Creep / long-term set-point drift of PZT on Si₃N₄ | not found in the sources read | not stated — flagged for S0b.2/S0b.3 |

### 1C-pcm — phase-change Sb₂Se₃ on Si₃N₄; *non-volatile, zero hold, quantized, write-limited, lossy*
| number | source | status |
|---|---|---|
| Sb₂Se₃ on Si₃N₄, ITO transparent heaters, 8-inch wafer process, C-band: **endurance 1.4×10⁸ cycles** (failure = ITO breakdown; phase change decays 0.001 rad/µm per 5×10⁶ cycles late in life); **65 repeatable levels** (284 distinguishable over 27 dB); **SET (amorphization) 15.4 V/40 µs ≈ 19.2 µJ; RESET (crystallization) 10.4 V per level ≈ 22.4 µJ/level** (80 µm cell; endurance device 30 µm); pulse power densities 0.006 W/µm × 20 µs (amorph.) and 0.0035 W/µm × 600 µs (cryst.); **propagation loss 0.018 dB/µm amorphous, 0.021 dB/µm crystalline**; MZI IL ≈ 1.5 dB (C-band) | Yu, Chakraborty, …, Pleros, Gardes, arXiv:2604.11649 (13 Apr 2026), full HTML | VERIFIED |
| Retention duration; standby power | not stated in the paper (non-volatile by design) | not stated — hold charged at 0, flagged |
| Graphene-heater PCM (Si platform, transferable to Si₃N₄ per authors): **amorphization 5.55 nJ; SET 0.380 ± 0.062 nJ; > 1,000–1,500 cycles; 14 phase levels (ring); graphene absorption 0.002 ± 0.001 dB/µm** | Fang, Khan, … Pop, Nat. Nanotechnol. 17, 842 (2022) (PDF) | VERIFIED |
| Sb₂S₃ on Si₃N₄ microrings: 0.15–0.2 nm shift for 10–20 µm cells; Q decreases 14.7–18.4 per µm of PCM (low-Q rings); ER 12.5–22.7 dB; switching by anneal / CW-laser trimming only | Ilie, Faneca, Zeimpekis et al., Sci. Rep. 12 (2022), 10.1038/s41598-022-21590-w | VERIFIED (PMC) |
| Sb₂Se₃ optical constants: Δn ≈ 0.77 (bulk, 1550 nm), k < 10⁻⁵ both states | Delaney et al., Sci. Adv. 7, eabg3500 (2021) | UNVERIFIED-direct (widely reproduced; page not read this session) |
| Thin-film effective **Δn_PCM = 0.1** (30 nm film on 220 nm SOI); laser-written; ~0.4 dB IL growth after 10 cycles | Radford et al., Nano Lett. 26(16), 5370 (2026), 10.1021/acs.nanolett.5c05838 (PMC full text) | VERIFIED |
| **Ring-Q compatibility (derived, C-2 cell):** intrinsic round-trip loss = 0.051 dB/cm × 2π·242 µm = **0.0078 dB/rt**. A **1 µm** full-overlap Sb₂Se₃ cell adds 0.018–0.021 dB ⇒ Q_i 6.8×10⁶ → ≈ **1.9×10⁶** (memory ×0.28); a 10 µm cell ⇒ Q ≈ 2.5×10⁵. Resonance range per µm at Δn_eff = 0.1: Δν = ν·Δn_eff·L/(n_g·2πR) = 193 THz × 0.1 × 1 µm/(1.97 × 1.52 mm) ≈ **6.4 GHz/µm**, i.e. **≈ 100 MHz per level** at 65 levels vs a C-2 linewidth κ_i/2π = **14 MHz** — 7 linewidths per step, unusable for δ-setting. **Weak-overlap design** (Δn_eff 0.01, loss scaled ∝ overlap to 0.002 dB/µm — assumption): 640 MHz/µm, **≈ 10 MHz/level ≈ 0.7 linewidth**, +0.002 dB/rt ⇒ Q ×0.8. | this ledger, from the rows above + `photonic_ssm/platforms.py` (C-2: 0.051 dB/cm, R = 242.2 µm, n_g 1.97, Q_i 6.8×10⁶) | derived; weak-overlap loss scaling = UNSOURCED-assumption |
| Consequence for S0b.2: the trainable-through-quantization question is posed at **L ≈ 65 levels, ≈ 0.7 linewidth/level, ~20 µJ/write, 10⁸ writes** — and the write count per training run (PAT/SPSA ≈ 10⁴ updates × 2N channels) is what S0b.2 must budget against. | — | scope note |

### Drift coefficient (needed for every class-C option)
| number | source | status |
|---|---|---|
| Si₃N₄ resonance drift **14 pm/K ≈ 1.75 GHz/K**; dn/dT 2.45×10⁻⁵/K | `photonic_ssm/platforms.py` registry (PR-4 frozen) | frozen |
| Linewidth κ_i/2π: C-1 48 MHz, C-2 14 MHz, C-3 3.2 MHz ⇒ a linewidth is **27 / 8 / 1.8 mK** | derived from registry κ_i | derived |
| Uncorrelated per-ring drift anchor 341 MHz / 24 h ⇒ 3.9 kHz/s ⇒ one C-2 linewidth in ≈ 1 h | `photonic_ssm/estimators/drift.py` (S0.9, PR-16 anchor) | frozen |

## 2. Gain pump — the fifth unbudgeted item (found 2026-09-13)
The S0.7 envelope charged conversion + heaters only; the substrate's Er:Si₃N₄ stage (g = 0.9 κ_i at
every ring, PR-4 §G) needs a 1480/980 nm pump that no §7 row carries. Rows:

| number | source | status |
|---|---|---|
| Er:Si₃N₄ (Liu et al.): 0.21-m coil, **245 mW total on-chip 1480 nm pump** for the headline net gain (>20 dB, 145 mW out); net gain coefficients **1.0 / 1.4 / 1.9 dB/cm** at N₀ = 0.67 / 1.35 / 3.25 ×10²⁰ cm⁻³; unpumped erbium absorption **≈ 2 dB/cm at 1535 nm** (κ₀/2π ≈ 1000 MHz) vs 0.08 dB/cm at 1600 nm; PL lifetime τ = 3.4 ms | Liu et al., Science 376, 1309 (2022), arXiv:2204.02202 (PDF text) | VERIFIED |
| Transparency pump power on that device | not stated in text (Fig. 3C only) | not stated |
| **Transparency intensity (derived):** I_tr = hν_p/(σ_a τ) with hν(1480 nm) = 1.34×10⁻¹⁹ J, τ = 3.4 ms (VERIFIED), σ_a(1480) ≈ 2×10⁻²¹ cm² (typical Er, **UNSOURCED-assumption**) ⇒ **≈ 2×10⁴ W/cm² = 0.20 mW/µm²**; A_eff ≈ 1.2 µm² (AN800 core, assumption) ⇒ **≈ 0.24 mW optical per ring at transparency**, × (1–10) for pump coupling into the ring ⇒ **0.24–2.4 mW/ring optical** | this ledger | derived (two UNSOURCED inputs) |
| 980 nm pump module, 300 mW class: **I_op ≤ 900 mA, V_f ≤ 2.4 V** (datasheet maxima) ⇒ **WPE ≥ 300/(900×2.4) = 13.9 %**; cooled 14-pin butterfly (TEC) | Lumentum 5050 series datasheet (PDF) | VERIFIED (maxima ⇒ WPE lower bound) |
| Pump-diode E/O efficiency "typically > 30 %"; ~0.6 W/A | search snippets (vendor pages) | UNVERIFIED-direct |
| **Electrical pump per ring:** 0.24–2.4 mW / (0.30–0.14) ⇒ **0.8–17 mW/ring**; N = 32 ⇒ **26–550 mW** + pump-module TEC 0.18 W (cooled part; uncooled at OPT flagged) | derived | derived |
| Unpumped Er absorption **2 dB/cm** would raise the C-2 ring loss 40× (0.051 → ~2 dB/cm) ⇒ the **passive** configuration means *undoped* rings, not unpumped doped rings | Liu et al. row above | derived |

## 3. Drift management (the locking exclusion, charged) — options priced side-by-side
| option | power | source | status |
|---|---|---|---|
| TEC hold (near-ambient) | **0.18 W** | Thorlabs 21060-D02 (exclusions ledger §4) | VERIFIED |
| Global chip heater in an isolated package (no TEC) | **10 (OPT) – 50 (CONS) mW** (5–10 K above ambient at 200–500 K/W package resistance) | this ledger | **UNSOURCED-assumption** — removed in sensitivity |
| Actuator-tracked common-mode lock (classes A, B, C-pz: the actuator follows the carrier) | control compute MCU-class 0.13 W × duty; duty **1 % (OPT) / 10 % (CONS)** ⇒ **1.3 / 13 mW**; thermal hold 0 | MCU row: exclusions ledger §3 (STM32F407, UNVERIFIED-direct); duty = assumption | derived; duty = UNSOURCED-assumption |
| Per-ring heater locking demos | 4.6–6.8 mW/ring (heater power only; electronics not reported) | Jayatilleka et al., Optica 6, 84 (2019) | VERIFIED (lower bound) |
| **Periodic in-situ retraining** of the uncorrelated residual at cadence T_r | E_episode / T_r + 0.13 W × (22.5 ms / T_r); E_episode = **2.6 mJ (OPT) / 99 mJ (CONS)** (§7.3 SPSA conversion stack) | §7.3 frozen; drift anchor ⇒ T_r ≈ 10²–10³ s suffices at C-2 | derived |
| Class C-pcm cannot track continuous drift (µJ and an endurance count per write) ⇒ its drift options are TEC / global heater only, + retraining for the residual | — | scope rule |

## 4. Packaging (insertion-loss co-condition)
| number | source | status |
|---|---|---|
| Edge coupling **0.15 dB/facet** (UHNA-7 best) / **≈ 1–1.5 dB/facet** (LIGENTEC lensed fibre; SMF-28 best) ⇒ 2 facets: **0.3 (OPT) – 3 (CONS) dB** | exclusions ledger §4 | VERIFIED / VERIFIED (quote) |
| Grating couplers < 10 dB/grating (CORNERSTONE) — fails the 3 dB co-condition outright | exclusions ledger §4 | UNVERIFIED-direct |

## 5. Digital baseline, priced to the function (energy per tap per sample)
| number | context | source | status |
|---|---|---|---|
| TX 8-tap FIR: **32 mW at 106.25 Gb/s** (53.1 GBd) ⇒ 32 mW/(8 × 53.1 GS/s) = **0.075 pJ/tap/sample** | DAC-based TX FFE, node not stated (2018-era 16/14/7 nm) | Sun (Credo), IEEE 802.3ck "100G SERDES power study", sun_3ck_01a_0918 (PDF) | VERIFIED (numbers) / node not stated |
| RX 24-tap FFE + 10-tap DFE design: total **545 mW with, 360 mW without FFE/DFE** ⇒ 185 mW for 34 taps at 53.1 GBd ⇒ **0.10 pJ/tap/sample** | ADC-DSP RX, node not stated | same | VERIFIED (numbers) / derived |
| DSP-based 112 G PAM-4 transceivers, whole lane: **4.5–6.5 pJ/bit** with 22–30-tap RX FFE (7 nm / 5 nm class); XSR 1.55–1.71 pJ/bit without long FFE | per-lane totals incl. AFE/ADC/clocking | Li & Wu (MediaTek), IEEE 802.3df prli_3df_01_2211 (PDF), citing Park ISSCC, Guo, Varzaghani, LaCroix (7 nm, 6 pJ/b), Mishra, Yousry | VERIFIED (table) |
| ADC-DMT 56 Gb/s RX in 14 nm: DSP **1.2 pJ/b**, whole RX 2.9 pJ/b, 161 mW | DMT, not FFE-tap-structured | IBM ISSCC 2019 (30.2) | UNVERIFIED-direct |
| 45 nm reference energies (Fig. 1.1.9): 8-bit add 0.03 pJ, 8-bit multiply 0.2 pJ ⇒ **0.23 pJ per 8-bit MAC at 45 nm**; 7 nm scaling ×0.1–0.25 ⇒ **0.02–0.06 pJ/MAC** (logic only) | reference floor | Horowitz, ISSCC 2014 (PDF; figure caption present, values as universally reproduced) | VERIFIED (figure) / values UNVERIFIED-direct in this extract; scaling = derived |
| Coherent CD equalization "> 20 % of total DSP power"; pilot-based CPR 0.38–1.1 pJ/bit; DSP ASIC energy ~1 pJ/bit class | block-level, not per tap | arXiv:2412.17536 (FPGA CD-EQ paper, statement without a pJ figure); Larsson-Edefors & Börjeson, SUM 2020 | UNVERIFIED-direct / VERIFIED |
| **Frozen per-tap bracket:** e_tap = **0.05 pJ (OPT) / 0.15 pJ (CONS)** per tap per sample; sensitivity band **[0.03, 0.25]** | OPT = Credo TX FIR 0.075 rounded toward the Horowitz-scaled floor; CONS = Credo RX FFE/DFE 0.10 × 1.5 for adaptation and data movement | this ledger | derived — **the load-bearing row**; both ends within measured ASIC-class data |

## 6. Numbers dropped as unsourceable this session (recorded per protocol)
- Sb₂Se₃ switching by nanosecond laser pulses with pJ energies (arXiv:2111.13182): abstract gives timescales only, no energies read.
- Delaney 2021 Δn/k page not read (science.org); carried UNVERIFIED-direct via Radford 2026.
- PZT creep on Si₃N₄: no source found.
- Global-heater hold power in an isolated package: no primary source; carried as UNSOURCED-assumption and removed in the PR-20 sensitivity re-statement.
