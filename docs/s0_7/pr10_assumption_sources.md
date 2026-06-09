# PR-10 assumption sourcing — candidate table for the S0.7-lite envelope (S0.7L-0)

**Author:** Executor · **Date:** 2026-06-10 (literature snapshot 2026-06) · **Task:** S0.7L-0
**Status:** SOURCING ONLY. **PR-10 is ⬜ UNSET** — this memo *feeds* the Supervisor's freeze draft; it
does **not** set values, pick operating points, or run the envelope. **No envelope arithmetic** is
performed here (one illustrative sanity row, §7, labelled non-load-bearing). Where sources disagree,
the **bracket + both sources** are given — the freeze registers the bracket, not a midpoint.

**Method.** Four parallel web sweeps (one per external category, §1–§4) under the project's
primary-source rule (the B2/F5 lesson): every load-bearing number from a vendor datasheet or a
measured peer-reviewed paper, with the load-bearing sentence/spec line quoted verbatim; unreachable
primaries are marked UNVERIFIED with the retrieval trail, never presented as verified. Two
first-hand Executor spot-checks of the most load-bearing novel numbers (CORNERSTONE MPW#9 design
rules PDF; TI ADC12DJ3200 datasheet pp. 13–18) reproduced the sweep quotes **exactly**. §5
(operating scale) is internal — cited to `docs/s0_1/mapping_result.md` §4 and the S0.1 registry.
Full search trail: §9.

**Verification legend:** ✅ = primary fetched this session, quote verbatim · ◑ = abstract/metadata
level (full text unreachable) · ✗ = UNVERIFIED, primary unreachable (trail in §8).

---

## 1. E/O + O/E conversion energies (modulator incl. driver; PD/TIA)

| # | Quantity | Value | Rate / conditions | Primary source | V |
|---|----------|-------|-------------------|----------------|---|
| 1.1 | Si microdisk modulator, device-level (resonant best case) | **0.9 fJ/bit** (switching energy 3.65 fJ); 1.03 fJ/bit incl. thermal tuning | 25 Gb/s, 0.5 V_pp, vertical p–n junction | Timurdogan et al., Nat. Commun. 5:4008 (2014), DOI 10.1038/ncomms5008 | ✅ |
| 1.2 | Si MZM, device-level (low-power traveling-wave) | **450 fJ/bit** | 50 Gb/s, diff. 1.5 V_pp, ~1300 nm | Streshinsky et al., Opt. Express 21(25):30350 (2013) | ✅ (abstract via PubMed) |
| 1.3 | Plain Si FCP MZM, device-level (survey statement) | **"a few pJ/bit"** | generic | Miller, J. Lightwave Technol. 35(3):346 (2017), p. 361 | ✅ |
| 1.4 | TX incl. CMOS driver (hybrid-integrated best case) | **1.35 mW total TX** (≈135 fJ/bit, derived) | 10 Gb/s, >7 dB ER | Zheng et al., Opt. Express 19(6):5172 (2011) | ✅ (abstract via PubMed) |
| 1.5 | TX incl. driver (monolithic CMOS SOI) | **driver 7.2 pJ/bit; link 10.2 pJ/bit excl. laser** (256 mW) | 25 Gb/s, BER 10⁻¹² | Buckwalter et al., IEEE JSSC 47(6):1309 (2012) | ◑ (abstract via OpenAlex; IEEE 418) |
| 1.6 | Link electronics class (driver+RX amp+CDR+SERDES) | **"order of picojoules per bit"**; off-chip comms **1–20 pJ/bit** (Table I) | 2017 state of practice | Miller 2017, pp. 347, 349 | ✅ |
| 1.7 | O/E receiver (PD+TIA, hybrid, in-rate-class) | **3.95 mW = 395 fJ/bit** | 10 Gb/s, −17 dBm sens., BER 10⁻¹² | Zheng et al. 2011 (same paper as 1.4) | ✅ |
| 1.8 | O/E receiver, best-case circuit (survey-cited) | **170 fJ/bit** | 25 Gb/s, −14.9 dBm | Miller 2017, p. 362 §V-A (his ref. [112], not independently fetched) | ✅ (Miller quoted directly) |
| 1.9 | O/E receiver data-path (FinFET, high-rate) | **1.4 pJ/bit** (≈90 mW, derived) | 64 Gb/s NRZ | Ozkaya et al., IEEE JSSC 52(12):3458 (2017) | ◑ (abstract via IBM author page; **see flag §6.1**) |
| 1.10 | O/E receiver (balanced PD + diff. TIA) | **0.55 pJ/bit** (0.98 incl. output buffer) | 54 Gb/s (above niche rate) | Li et al., Opt. Express 28(9):14038 (2020) | ✅ (abstract via Europe PMC) |

Load-bearing quotes (verbatim from the primaries):
- **1.1** "Here we demonstrate and characterize the first modulator to achieve simultaneous
  high-speed (25 Gb s−1), low-voltage (0.5 VPP) and efficient 0.9 fJ per bit error-free operation."
  And: "the modulator operated over a 7.5 °C range with 1.03 fJ per bit energy consumption including
  both tuning (0.24 fJ per bit) and modulation energy (0.79 fJ per bit)."
  (pmc.ncbi.nlm.nih.gov/articles/PMC4082639/, acc. 2026-06-09)
- **1.2** "We demonstrate an open eye at this speed using a differential 1.5 V(pp) signal at 0 V
  reverse bias, achieving an energy efficiency of 450 fJ/bit." (PMID 24514613, acc. 2026-06-10)
- **1.3 / 1.6 / 1.8** "a simple Mach-Zehnder FCP modulator without any optical concentration will
  require a few pJ/bit" · link circuits "currently consume energies of the order of picojoules per
  bit" · Table I "Communicating off chip — 1–20 pJ" · "This example gives a receiver circuit
  operating at 170 fJ/bit at 25 Gb/s with −14.9 dBm noise-limited sensitivity. Such a receiver
  circuit energy per bit is impressively low; other circuits … can dissipate as much as several
  pJ/bit." (www-ee.stanford.edu/~dabm/448.pdf, acc. 2026-06-09)
- **1.4 / 1.7** "the hybrid silicon photonic transmitter achieved better than 7 dB extinction ratio
  for 10 Gbps operation with a record low power consumption of 1.35 mW." · "The all CMOS hybrid
  silicon photonic receiver achieved sensitivity of -17 dBm for a BER of 10(-12) at 10 Gbps,
  consuming an ultra-low power of 3.95 mW (or 395 fJ/bit in energy efficiency)." (PMID 21445153,
  acc. 2026-06-10)
- **1.5** "The total power consumption is 256 mW and demonstrates a link efficiency of 10.2 pJ/bit
  excluding laser power. … At 25 Gb/s, the driver operates at 7.2 pJ/bit." (abstract reconstructed
  from OpenAlex word index — flag for human spot-check if this row becomes load-bearing.)
- **1.9** "The RX … achieves an energy efficiency of 1.4 pJ/bit and -5-dBm optical modulation
  amplitude while recovering PRBS-7 data (bit-error-rate <10-12)" (research.ibm.com publication
  page, acc. 2026-06-09).
- **1.10** "the power efficiency has been optimized to 0.55 pJ/bit (0.98 pJ/bit if output buffer is
  included)" (Europe PMC record, acc. 2026-06-10).

**Candidate brackets for the freeze:**
- **E/O device-level:** [~1 fJ/bit (resonant microdisk, 25 Gb/s) … ~few pJ/bit (plain Si MZM)] —
  device class is the conditioning variable; the fJ end presumes a resonant low-capacitance junction
  modulator.
- **E/O incl. driver/electronics:** [~0.14 pJ/bit (hero hybrid, 10 Gb/s) … ~10–20 pJ/bit
  (monolithic measured / Miller class)] — ~2 orders of magnitude; honest envelope should carry both
  ends.
- **O/E (PD+TIA):** [~0.17 pJ/bit (25 Gb/s best-case) … several pJ/bit], with 0.55–1.4 pJ/bit
  measured at ≥54 Gb/s.

---

## 2. DAC / ADC energy per sample + ENOB at GS/s-class rates

| # | Quantity | Value | Rate / ENOB / conditions | Primary source | V |
|---|----------|-------|--------------------------|----------------|---|
| 2.1 | ADC-survey energy envelope | **0.27 pJ + 0.145 aJ·4^ENOB per Nyquist sample** (floor ≈0.27 pJ/sample at 6–10 ENOB) | all rates pooled, ISSCC+VLSI 1997–2026 | B. Murmann, "ADC Performance Survey 1997-2026," github.com/bmurmann/ADC-survey (`plots/energy_plot.png`) | ✅ |
| 2.2 | ADC-survey speed roll-off | **env = 186.7 dB − 10·log(1+(f_snyq/46.3 MHz)²)** — at GS/s the Schreier-FoM envelope is ~20–25 dB below the LF asymptote | 2026-dataset fit | same survey, `plots/foms_plot.{png,json}` | ✅ |
| 2.3 | Canonical FoM frontiers | **FoM_W = 5 fJ/conv-step; FoM_S = 185 dB**; "Roll-off ≈ −10dB/dec"; energy ×4 per +6 dB when noise-limited | 1997–2021 data | Murmann, ISSCC 2022 Short Course (in survey repo), slides 60–66 | ✅ |
| 2.4 | Named vendor ADC, power | **3.0 W typ** (single-ch 6.4 GS/s, power mode 1); 3.6 W background-cal; 3.8 W dual-ch background-cal | 12-bit, JMODE 1 | TI ADC12DJ3200 datasheet SLVSD97A (2017, rev. 2020) §6.6 | ✅ **(Executor spot-check exact)** |
| 2.5 | Named vendor ADC, ENOB at speed | single-ch 6.4 GS/s: **8.6 typ** @347 MHz, **8.4 typ/7.7 min** @2482 MHz, 7.7 @4997 MHz; dual-ch 3.2 GS/s: **9.0 typ** @347/997 MHz | A_IN −1 dBFS | same datasheet §6.7/§6.8 | ✅ **(Executor spot-check exact)** |
| 2.6 | Vendor ADC energy/sample | **≈469 pJ/sample** (3.0 W / 6.4 GS/s) | derived from quoted P and f_s | derived, TI ADC12DJ3200 | ✅ inputs |
| 2.7 | Named vendor DAC | **9 GS/s max, 14-bit core, 2772 mW typ** @ f_DAC 9 GHz (Mode 5); 2638 mW @6 GHz; SFDR 61 dBc @ f_OUT 951 MHz | dual-channel modes | TI DAC38RF82 datasheet SLASEA6D (2017, rev. 2020) §7.5/§7.7 | ✅ |
| 2.8 | Vendor DAC energy/sample | **≈308 pJ/sample** (2.772 W / 9 GS/s) | derived from quoted P and f_DAC | derived, TI DAC38RF82 | ✅ inputs |
| 2.9 | Research ADC anchor at GS/s | **158.6 mW @ 5 GS/s, 9.4 ENOB** → ≈31.7 pJ/sample (derived) | 28 nm, ISSCC 2019 | Ramkaj et al., ISSCC 2019 (IEEE doc 8662490) — all numbers in the paper title | ◑ (title-level; IEEE 418) |
| 2.10 | Research DAC anchor at GS/s | 14 nm: **286 mW @ 56 GS/s, 8b** (≈5.1 pJ/sample); 7 nm: 560 mW @ 60 GS/s, 8b, SINAD 29.5 dB ≈ **4.6 ENOB at speed** | wireline CS DACs | Greshishchev table as reproduced in Murmann ISSCC 2022 deck, slide 90 | ◑ (read from deck; original not fetched) |

Load-bearing quotes:
- **2.1/2.2/2.3** plot legend "0.27 pJ + 0.145 aJ · 4^ENOB" (P/f_snyq vs SNDR, ISSCC & VLSI
  1997-2026) · legend "env = 186.7 dB - 10log(1+(f_snyq/46.3 MHz)²)" with foms_plot.json
  `foms_db_asymp = 186.72`, `f_corner = 46.29 MHz` · slides: "FoM_S = 185 dB", "FoM_W = 5
  fJ/conv-step", "Roll-off ≈ -10dB/dec", "P/f_s ∝ kT × SNR … Energy increases 4x per 6 dB"
  (survey repo, acc. 2026-06-09/10). Survey's requested citation form used above.
- **2.4** §6.6: "P_DIS Power dissipation | Power mode 1: Single channel mode, JMODE 1 (16 lanes,
  DDC bypassed), foreground calibration | TYP 3.0 | W" — **re-read first-hand by the Executor from
  the datasheet PDF (p. 13), exact match** (also 3.6 W mode 3, 3.8 W mode 4).
- **2.5** §6.8: "ENOB … f_IN = 2482 MHz, A_IN = −1 dBFS | MIN 7.7 TYP 8.4 | Bits" (8.6 typ @347
  MHz); §6.7 dual-ch: "f_IN = 347 MHz … TYP 9.0 | bits" — **re-read first-hand (pp. 14–18), exact
  match.**
- **2.7** "14-Bit resolution, 9-GSPS DAC with multimode operation" · "P_DIS … MODE 5: dual channel,
  8-bit input mode, 1x Interpolation, Sin(x)/x enabled, f_DAC = 9 GHz, CLKTX Disabled | TYP 2772 |
  mW" · SFDR "f_CLK = 9 GHz, f_OUT = 951 MHz | 61 | dBc" (ti.com/lit/ds/symlink/dac38rf82.pdf,
  acc. 2026-06-10).
- **2.9** title: "A 5GS/s 158.6mW 12b Passive-Sampling 8×-Interleaved Hybrid ADC with 9.4 ENOB and
  160.5dB FoMS in 28nm CMOS."

**Candidate brackets for the freeze:**
- **ADC at GS/s:** research best **≈32 pJ/sample (9.4 ENOB)** vs named vendor part **≈469
  pJ/sample (8.4 ENOB)** — ≈15× energy/sample. Cross-check: by *Schreier* FoM the vendor part
  computes to ≈142 dB, close to the survey's GS/s envelope — the FoM convention changes the apparent
  research-vs-vendor gap; the freeze should state which FoM it registers (recommend registering
  energy/sample + ENOB-at-speed directly).
- **DAC at GS/s:** research ≈5–9 pJ/sample (8b nominal, ~4.6 ENOB at speed) vs vendor ≈308
  pJ/sample (14-bit core) — different resolution/drive points; register with ENOB attached.
- **Rule for the freeze:** use **ENOB at-speed, never nominal bits** (12-bit parts deliver 7.7–9.0
  ENOB at GHz inputs; 8b research DACs ≈4.6 ENOB at 60 GS/s).

---

## 3. Named digital-baseline class + sources (F16: strong baseline, not an unoptimized GPU)

| # | Name | Platform | Workload | Throughput / power → perf/W | Primary source | V |
|---|------|----------|----------|------------------------------|----------------|---|
| 3.1 | **Microsoft Brainwave NPU** (Fowers et al., ISCA 2018) | Intel Stratix 10 280 FPGA, ms-fp8 BFP | **batch-1 GRU/LSTM streaming serving**, <4 ms | 35.9 eff. TFLOPS / 125 W peak → **287 GFLOPS/W (author-stated)** | ISCA 2018 camera-ready PDF (microsoft.com) | ✅ |
| 3.2 | ESE (Han et al., FPGA 2017) | Xilinx XCKU060, 200 MHz | sparse LSTM speech rec. (20× compressed, matched accuracy) | 282 GOPS sparse / 41 W → 6.9 GOPS/W (61.5 dense-eq, derived) | arXiv:1612.00694 / FPGA'17 | ✅ |
| 3.3 | **MARCA** (Li et al., ICCAD 2024) | ASIC, 28 nm, 1 GHz, 10.44 W | Mamba LLM inference (closest workload class: selective-SSM recurrence) | up to 11.66× A100 speedup, **242.52× A100 energy efficiency (relative only)** | arXiv:2409.11440 | ✅ |
| 3.4 | LightMamba (DATE 2025) | AMD Versal VCK190 / Alveo U280 | Mamba2-2.7B decode, W4A4 | 7.21 tok/s @ 2.25 tokens/J (VCK190, stated); 4.65–6.06× vs GPU | arXiv:2502.15260 | ✅ |
| 3.5 | SpecMamba (ICCAD 2025) | AMD VHK158/VCK190 | Mamba + speculative decoding | 2.27× GPU speedup; 5.41×/1.26× energy eff. (referents ambiguous from abstract) | arXiv:2509.19873 | ◑ |
| 3.6 | AMD Versal AI Core VC1902 | Versal AIE, 7 nm | vendor-listed CNN/**RNN**/MLP; GS/s vector DSP | 133 peak INT8 TOPS / 87 W (XPE estimate) → ≈1.5 TOPS/W peak (derived) | AMD/Xilinx solution brief PID 231846771-B | ✅ |
| 3.7 | **NTT 400ZR coherent DSP** (7 nm) | DSP ASIC | GS/s streaming FIR/equalization (the most direct streaming-filter anchor) | "<10W" DSP in 15 W module → **≤25 pJ/bit DSP-only (derived)** at 400 Gb/s | NTT Innovative Devices technical article (vendor) | ✅ |
| 3.8 | Coherent RX ADC+DSP, 40 nm | ASIC estimate | 100 Gb/s DP-QPSK RX DSP | ~17 W → 170 pJ/bit (derived) | Perin, Shastri & Kahn, JLT 35(21):4650 (2017), author PDF | ✅ |
| 3.9 | NVIDIA Jetson AGX Orin 64GB | embedded GPU module | general INT8 inference (incl. RNN via TensorRT) | 275 peak sparse INT8 TOPS / 15–60 W → ≈4.6 TOPS/W peak (derived; **peak ≠ sustained**) | NVIDIA Technical Brief TB_10749-001_v1.2 | ✅ |
| 3.10 | Google Coral Edge TPU | edge ASIC | INT8 CNN-class (limited op set; weak recurrence support) | **4 TOPS / 2 W → 2 TOPS/W (vendor-stated)** | coral.ai Edge TPU FAQ | ✅ |

Load-bearing quotes:
- **3.1** "The BW NPU can run *all* DeepBench layers at under 4ms at batch 1, reaching up to 35.9
  effective TFLOPS for a large GRU over hundreds of timesteps." · "We measured the peak chip power
  consumption of a Stratix 10 280 FPGA to be 125W by running a power virus design … a conservative
  estimate … would put the power efficiency of BW at 287 GFLOPS/W when running large models at high
  device utilization." (ISCA18 camera-ready, acc. 2026-06-09.)
- **3.2** "Implemented on Xilinx XCKU060 FPGA running at 200MHz, ESE has a performance of 282 GOPS
  working directly on the compressed LSTM network, corresponding to 2.52 TOPS on the uncompressed
  one, and processes a full LSTM for speech recognition with a power dissipation of 41 Watts."
- **3.3** "MARCA achieves up to 463.22×/11.66× speedup and up to 9761.42×/242.52× energy efficiency
  compared to Intel Xeon 8358P CPU and NVIDIA Tesla A100 GPU implementations, respectively." · "The
  total power and area of MARCA are only 10.44 W and 221.88 mm²."
- **3.6** "Up to 133 INT8 TOPS with the Versal AI Core VC1902 device" · benchmark table "Total
  Power … 87 Watts⁵" (footnote 5: XPE device estimate).
- **3.7** "A 7nm DSP for 400ZR application needs to have less than 10W power dissipation in order to
  fit into a 15W transceiver module."
- **3.8** "…polarization demultiplexing, carrier recovery (CR), and timing recovery, which,
  combined, consume roughly 17 W in 40-nm complementary metal-oxide semiconductor (CMOS) for a 100
  Gbit/s dual-polarization (DP) quaternary phase-shift keying (QPSK) receiver [12]."
- **3.9** "delivering up to 275 TOPS of AI performance" · Table 1 "Power — 15W - 60W".
- **3.10** "An individual Edge TPU can perform 4 trillion (fixed-point) operations per second
  (4 TOPS), using only 2 watts of power—in other words, you get 2 TOPS per watt."

**Candidate baseline classes for the freeze (recommendation-shaped, decision is the freeze's):**
- **Tuned-FPGA recurrent serving (strongest published match in spirit):** Brainwave — batch-1
  streaming GRU/LSTM, 287 GFLOPS/W author-stated. Newer embedded-FPGA LSTM papers (2023–2025,
  11–15 GOPS/W) are *weaker*, not stronger.
- **SSM accelerators (closest workload, weakest numbers-comparability):** MARCA / LightMamba — all
  published SSM accelerators are LLM-decode-oriented; none target GHz-rate sample streams; only
  relative perf/W published for MARCA.
- **GS/s streaming FIR (the latency-niche anchor):** coherent-DSP ASIC class, **25–170 pJ/bit
  bracket** (7 nm 400ZR vendor → 40 nm JLT measured-estimate). **The prior project's "~5 pJ/bit at
  800G" number found no primary — see flag §6.2.**
- **Embedded GPU (F16's named representative):** Jetson AGX Orin, 275 peak sparse TOPS at 15–60 W —
  with the explicit caveat that peak ≠ sustained on recurrent workloads (Brainwave measured GPUs
  at <13% utilization on small-batch RNNs).

---

## 4. Thermo-optic holding power per heater (SiN) + control-electronics overhead

| # | Quantity | Value | Conditions (platform, isolation, τ) | Primary source | V |
|---|----------|-------|-------------------------------------|----------------|---|
| 4.1 | **CORNERSTONE SiN foundry heater spec** | **< 175 mW/π** (quality-assessment target); 900 nm filament recommended | 300 nm LPCVD SiN, 2 µm top cladding, TiN-class filament + pads; **no undercut in this flow**; no τ given | CORNERSTONE Design Guidelines, SiN MPW #9, Oct. 2024 (U. Southampton) | ✅ **(Executor spot-check exact)** |
| 4.2 | **LIGENTEC AN800 measured P_π** | **≈60 mW/π**; I_π 41.91 mA (trench) / 44.55 mA (no trench); BW 9.2 kHz; crosstalk 12%→2.5% with deep trench | AN800, C-band; **lateral** deep trench (crosstalk tool — barely changes P_π) | Muñoz et al., IEEE JSTQE 28 (2022), DOI 10.1109/JSTQE.2022.3162577 (arXiv:2203.16956) | ✅ |
| 4.3 | Standard SiN P_π, research platforms | **350 mW** (CNM 300 nm LPCVD, Cr/Au, 270×5 µm²); **~385 mW/π** (TriPleX Pt, 1 mm) | fully clad, no isolation; no τ reported | Pérez et al., arXiv:1604.02958 (2016); Taballione et al., arXiv:2012.05673 (2020) | ✅ |
| 4.4 | Suspended/undercut SiN P_π | **0.78–1.20 mW/π** (visible-λ, measured; same-chip non-suspended ref. 15.9–23.0 mW/π = **~20× factor**); rise/fall ≈570/590 µs | AMF SiN, undercut via deep trenches + SiO₂ anchors | Yong et al., arXiv:2111.07890 (Poon group, 2021) | ✅ |
| 4.5 | Suspended SiN at 1550 nm | **0.98 mW/π** (suspended 10-fold spiral); τ ~2.6 ms and 158 mW/π conventional ref. **UNVERIFIED** (paywalled body) | dense sinusoidal spiral, 300×150 µm² | Zeng et al., Opt. Lett. 50(11):3768 (2025), DOI 10.1364/OL.562570 | ✅ abstract / ✗ body |
| 4.6 | Trench/undercut reduction factors (SIMULATION) | deep trenches **−70%** power, BW 11.8 kHz; trenches+undercut **−97%**, BW 0.9 kHz; crosstalk −1/−2 orders | CNM SiN platform, 2D heat-transfer model | Alemany et al., Photonics 8(11):496 (2021) | ✅ abstract (MDPI 403) — **simulation, not measurement** |
| 4.7 | Per-channel DAC quiescent (control electronics) | **0.25 mA/ch typ (boost off)** → ≈1.25 mW/ch at 5 V; 0.375 mA/ch max ≈ 1.9 mW/ch; 80 mW max package (40 ch, unloaded) | AD5380 40-ch 14-bit denseDAC | AD5380 datasheet Rev. D (ADI; Farnell-hosted official) | ✅ |
| 4.8 | Per-channel control, HV precision bracket | I_AA 20 mA typ + I_CC 10 mA typ shared across 16 ch (±20 V range, unloaded) | upper electronics bracket | TI DAC81416 datasheet SLASEO0C §5.5 | ✅ |
| 4.9 | Published per-element budgeting precedent | P_heater assumptions **2.8 mW (insulated) / 40 mW (no insulation) per FSR**; "Doped Si heaters on SOI … ∼20 mW for a π-shift" | **SOI accelerator-scaling analysis, not SiN measurement** | Al-Qadasi et al., APL Photonics 7:020902 (2022) | ✅ |
| 4.10 | **Harris 2014 provenance check** (pnn-multilayer's "20 mW/MZI" anchor) | actual **P_π = 24.77 ± 0.43 mW**; BW 130 kHz, τ 2.69 µs, IL 0.23 dB | **silicon (220 nm SOI), NOT SiN**; doped-Si ridge heater | Harris et al., Opt. Express 22(9):10487 (2014), arXiv:1410.3616 | ✅ |

Load-bearing quotes:
- **4.1** Table 3 (Quality assessment parameters): "MZI integrated with the PDK heater | Phase shift
  efficiency | **< 175mW/π phase shift**" · "It is recommended to use a filament width of 900 nm for
  the best compromise between heater power efficiency, phase tunability and robustness." —
  **re-read first-hand by the Executor from the foundry PDF (pp. 8, 11–12), exact match.** (Noted in
  passing, same doc Table 3: propagation loss target "< 0.6 dB/cm for TE mode in C-band" — registry
  `SiN_CORNERSTONE_300` carries 1.5 dB/cm from its own primary; not a PR-10 row, logged for S0.L.)
- **4.2** "the power consumption for a π phase shift was inferred to be ≈60 mW." · Table I:
  "Iπ [mA]: (T) 41.91 // (NT) 44.55; … BW [kHz]: (NT) 9.2; X_NT: 12%; X_T: 2.5%". Caveat: ar5iv
  renders the rise-time unit "[ms]" but tr = 0.35/9.2 kHz = 38 µs exactly — unit ambiguity flagged;
  verify against the IEEE version before the freeze if τ becomes load-bearing.
- **4.3** "Tuners with footprint of 270x5 μm² and switching power of 350 mW are reported." · "a π
  phase shift is achieved at V_π ≅ 10 V, corresponding to an electrical power of ~385 mW per
  element."
- **4.4** "The measured power consumption to achieve a π phase shift (averaged over multiple
  devices) was 0.78, 0.93, 1.09, and 1.20 mW at wavelengths of 445, 488, 532, and 561 nm,
  respectively." · "10−90% rise(fall) times of about 570(590) μs were measured." · non-suspended
  ref. "about 20× higher".
- **4.5** "By further suspending the device, we achieve a submilliwatt power consumption of 0.98
  mW/π in a 10-fold device."
- **4.6** "Deep air-filled trenches are shown to reduce the power consumption up to 70%, … The
  design with trenches and substrate undercut lowers the power consumption up to 97%, … at the cost
  of less than one order of magnitude in bandwidth (0.9 kHz)."
- **4.7** "Power consumption is typically 0.25 mA/channel with boost off."
- **4.10** "we obtain a P_π of 24.77 ± 0.43 mW. This corresponds to V_π = 4.36 V given the device
  resistance of 769.00 ± 1.24 Ω."

**Candidate brackets for the freeze:**
- **Standard (non-isolated) SiN P_π at 1550 nm: [≈60 … ≈385] mW/π**, with the foundry
  acceptance bound <175 mW/π (CORNERSTONE) inside it. **The informal "20–40 mW SiN class"
  assumption did not survive primary sourcing — see flag §6.3.**
- **Isolated SiN P_π: ≈1 mW/π floor** (measured, suspended), **at a speed cost: τ ≈ 0.4–2.6 ms
  class** (vs ~38–110 µs non-isolated). The freeze must disambiguate "trench-isolated": **lateral
  trenches cut crosstalk, not holding power** (4.2); only **undercut/suspension** buys the ~20×–97%
  power reduction (4.4/4.6) — and CORNERSTONE's MPW flow does not offer undercut (4.1).
- **Control electronics: [≈1.25 … ≈2] mW/channel** (AD5380-class typ→max) for low-voltage trim;
  tens-of-mW/ch for HV precision parts (4.8). The legacy "2 mW/shifter DAC-trim" convention is
  **compatible and now primary-sourced** at the AD5380-class max spec (0.375 mA × 5 V ≈ 1.9 mW) —
  see flag §6.4.
- **SPSA-cadence note for the envelope (not a number pick):** the isolation choice couples holding
  power to actuation bandwidth (ms-class τ when suspended) — the envelope's training-time and
  locking assumptions must use the *same* heater class as its power ledger.

---

## 5. Operating scale — N rings, line rate, λ-plan (internal; cites S0.1)

All from `docs/s0_1/mapping_result.md` §4, `docs/s0_1/{mapping_notes,B1_actuation_map,B3_kappa_ext_tradeoff}.md`, and `photonic_ssm/platforms.py` (the S0.1.1-reconciled registry). **No new physics here; the freeze picks values inside these S0.1-bounded candidates.**

| Quantity | S0.1-consistent candidate (bracket) | Internal source |
|----------|--------------------------------------|-----------------|
| Memory length (amplitude convention) | **3.29 ns / 329 round trips** (Q_i=2×10⁶, foundry-conservative) → **49.4 ns / 4937 rt** (Q_i=3×10⁷, class-leading); CORNERSTONE corner ~33 rt | `mapping_result.md` §4 (the PR-2 sizing numbers) |
| κ_ext policy interaction | undercoupling 0.1κ_i: 274 rt @ 0.028 drop-efficiency → overcoupling 10κ_i: 16 rt @ 0.91 (Q_i=2×10⁶) — operating point is **PR-4**, not PR-10 | `mapping_result.md` §4 / B3 |
| FSR / ring geometry | **100 GHz FSR** across all four registry entries (radius ≈ 238–245 µm, n_g 1.95–2.00) | `platforms.py` registry |
| Detuning span (λ-plan inside one FSR) | \|β_j\| ≤ π·FSR — "the reachable imaginary axis is one FSR wide" | `mapping_notes.md` §4 |
| Signal-bandwidth class (sets the line-rate + DAC/ADC-rate assumption) | intrinsic linewidth f₀/Q_i at 1550 nm (f₀=193.4 THz): **96.7 MHz** (Q_i=2e6) · 28.4 MHz (6.8e6) · **6.4 MHz** (3e7) · 824 MHz (CORNERSTONE 2.35e5) — *derived from registered Q_i, unit conversion only*; loaded linewidth widens with the PR-4 κ_ext policy (B3: κ_ext swept 0.1–10 κ_i) | registry + `mapping_notes.md` ("power-FWHM linewidth = f0/Q") |
| → line-rate candidate | **~0.1–2 GS/s class** I/O sampling (linewidth-matched streaming at foundry-Q; the GS/s-class converter rows in §2 are rate-consistent with this) — exact rate = freeze + PR-2 task choice | derived bracket from the row above |
| λ-plan candidate | **single carrier + per-ring thermo-optic detunings within one FSR** (the S0.1 model's regime). A WDM multi-carrier plan is *outside* the validated S0.1 model — if the freeze wants it, flag as an extension, not an assumption | `mapping_notes.md` §4, `mapping_result.md` §3 |
| N rings | **not set by S0.1** (state-dimension realizability = registered open item F8). Candidate bracket for the freeze: **N ∈ [8 … 128]** — lower end: Stage-1 MPW unit-cell scale (proposal §8); upper anchor: the pnn-multilayer ring-bank precedent (128 rings, 2L-N64, `beta_8_5_finding.md`). | proposal §8; pnn-multilayer β-8.5 (precedent only, not a measurement) |
| Control channels per ring (multiplies §4 rows) | **≈2–4 actuators/ring**: 1 detuning heater + 1–2 heaters for the tunable κ_ext coupler + ~1 tunable coupler per ring–ring edge (μ) | B1 actuation map table |

---

## 6. Discrepancy flags vs existing project anchors (for the Supervisor's freeze draft)

1. **Ozkaya 2017 standing-power anchor (pnn-multilayer `oeo_static_mW` = 20–50 mW/NOFU "Ozkaya 2017
   JSSC class").** The verifiable record (abstract via IBM author page) states **1.4 pJ/bit at 64
   Gb/s ≈ 90 mW data-path** (derived); no 20–50 mW standing-power figure is reachable — the internal
   power breakdown is behind the IEEE paywall. **Re-point the anchor at the verified 1.4 pJ/bit or
   obtain IEEE access before freezing** any standing-power row that cites it.
2. **"~5 pJ/bit at 800G DSP" (pnn-multilayer RESEARCH_SUMMARY "5.02 pJ/bit").** No primary found at
   that value; it appears to be pnn-multilayer's own *model-computed* number (MAC-count ×
   Horowitz-class pJ/MAC), not a sourced DSP figure. Nearest verified streaming-DSP anchors: **≤25
   pJ/bit DSP-only (7 nm 400ZR, vendor) to 170 pJ/bit (40 nm, JLT)**. PR-10 should register the
   sourced bracket, not the inherited 5 pJ/bit.
3. **SiN heater holding-power class.** Measured stoichiometric-SiN P_π at 1550 nm is **60–385
   mW/π** (foundry bound <175 mW/π) — substantially above silicon-derived intuitions (Harris Si:
   24.77 mW/π). The ~1 mW/π regime exists only with **undercut/suspension** at ms-class τ, which
   CORNERSTONE's flow does not offer. The proposal's "trench-isolated heaters" phrasing needs the
   lateral-trench (crosstalk) vs undercut (power) distinction made explicit at the freeze.
4. **"20 mW/MZI + 2 mW DAC-trim" (pnn-multilayer conventions).** Harris 2014 actually reports
   **24.77 ± 0.43 mW/π and is silicon, not SiN** — do not carry "20 mW" into PR-10 as a SiN number
   (use §4 brackets). The 2 mW/shifter trim convention is **retroactively well-sourced** (AD5380:
   0.375 mA/ch max × 5 V ≈ 1.9 mW; 1.25 mW typ) — reusable with the new provenance.

---

## 7. Illustrative sanity row — **NON-LOAD-BEARING** (the one permitted; no envelope conclusions)

At a 1 GS/s line rate with *vendor-class* converters (§2: ADC ≈469 pJ/sample + DAC ≈308 pJ/sample),
one I/O channel's conversion chain alone holds ≈0.78 W; N=32 standard AN800-class heaters (§4: ≈60
mW/π scale) hold ≈1.9 W. Conversion overhead and thermo-optic holding power are **the same order of
magnitude** at this scale — neither is negligible, which is exactly why PR-10 freezes both before
the envelope runs. *(Illustration only: real envelope arithmetic — duty factors, actual phase
holdings vs P_π, research-vs-vendor converter choice, baseline side — is the post-freeze S0.7-lite
run.)*

---

## 8. Unreachable primaries (consolidated; all marked ✗/◑ above)

- **Ozkaya et al., IEEE JSSC 2017 full text** — IEEE paywall/418; abstract via IBM author page +
  Crossref. The 20–50 mW standing-power attribution unverifiable (flag §6.1).
- **Buckwalter et al., IEEE JSSC 2012** — IEEE 418; abstract reconstructed via OpenAlex inverted
  index (row 1.5 caveat).
- **Optica full texts** (Streshinsky 2013, Zheng 2011, Li 2020, Zeng 2025) — anti-bot interstitial;
  abstracts verified via PubMed/Europe PMC. Body-only figures NOT registered (Streshinsky 800
  fJ/bit @2 V_pp; Zheng 320 fJ/bit @5 Gb/s; Zeng τ≈2.6 ms + 158 mW/π reference).
- **Analog Devices datasheets (AD9213 ADC, AD9172 DAC)** — analog.com fetch timeouts ×7 total;
  search-listing figures (AD9213: 12-bit 10.25 GS/s "<4.6 W") UNVERIFIED — TI parts substituted as
  the named-vendor rows.
- **Ramkaj ISSCC 2019 full text** — IEEE 418; all registered numbers are in the paper title
  (title-level verification).
- **LIGENTEC AN800 official heater spec** — PDK is NDA; public press release has no number. The
  published AN800 anchor is Muñoz JSTQE 2022 (row 4.2).
- **MDPI Photonics 8:496 full text** — mdpi.com 403; abstract via Semantic Scholar API.
- **Ciena Neutron 800ZR infobrief** — 403. **IEEE/VDE Photonic Networks 2017 coherent-DSP power
  trends** — paywalled, no mirror.
- **"2 mW/shifter (AIM PDK)" as a written primary** — not found public; superseded by AD5380
  sourcing (flag §6.4).

---

## 9. Reproducible search trail (appendix)

Four parallel sweeps, 2026-06-09 → 2026-06-10, WebSearch + WebFetch (sandbox `curl` unavailable;
binary PDFs read from WebFetch's local cache). ~45 logged queries, ~50 URLs opened, ~35 primaries
fetched in full or at abstract level. Executor first-hand re-verification: CORNERSTONE MPW#9 PDF
(13 pp read) and TI ADC12DJ3200 datasheet (pp. 13–18 read) — both exact-match vs the sweep quotes.

**Sweep 1 (E/O–O/E), key queries:** "Timurdogan Nature Communications 2014 athermal silicon
microdisk 0.9 fJ/bit" (8 hits → PMC4082639 full text); "Miller Attojoule Optoelectronics JLT 2017
pdf" (10 → Stanford author PDF); "Ozkaya IEEE JSSC 2017 optical receiver 64 Gb/s power" (8 → IBM
page, Crossref); "Streshinsky low power 50 Gb/s silicon MZM 2013 fJ/bit" (8 → PubMed 24514613);
"Zheng ring modulator hybrid CMOS driver Optics Express 2011 fJ/bit" (9 → PubMed 21445153);
Buckwalter JSSC 2012 (IEEE 418 → OpenAlex). Failed fetchers logged: opg.optica.org ×3,
ieeexplore ×2, semanticscholar 429 ×2, nature.com auth wall.

**Sweep 2 (DAC/ADC), key queries:** "TI ADC12DJ3200 datasheet power ENOB site:ti.com" (10 →
ti.com PDF, read); "AD9213 datasheet 10.25 GSPS power" (10 → timeouts ×4); "AD9172 datasheet"
(timeouts ×3); "Murmann Race for the Extra Decibel ADC FoM envelope" (9 → github.com/bmurmann/
ADC-survey identified as canonical); fetched survey README, energy_plot.{png,ipynb},
foms_plot.{png,json,ipynb}, ISSCC-2022 Short Course PDF (jsDelivr mirror of repo file; slides 1–4,
37–66, 86–93 read); "Ramkaj ISSCC 2019 5GS/s 158.6mW" (8 → IEEE listing, 418 on full text);
"DAC38RF82 datasheet" (→ ti.com PDF, read).

**Sweep 3 (digital baselines), key queries:** "ESE sparse LSTM FPGA Han GOPS watts" (9 → arXiv
1612.00694); "Brainwave Fowers ISCA 2018 Stratix 10 teraflops watts" (10 → microsoft.com
camera-ready PDF, pp. 9–12 read); "MARCA Mamba accelerator" (6 → arXiv 2409.11440 + html);
"LightMamba FPGA Mamba 2025 energy tokens" (10 → arXiv 2502.15260); "state space model FPGA
accelerator 2024 2025" (7 → SpecMamba 2509.19873; no GHz-stream S4/S5 FPGA paper exists — Mamba-LLM
-centric field); "AMD Versal AI Engine INT8 TOPS specification" (10 → xilinx.com solution brief);
"coherent DSP ASIC 800G pJ/bit" (9 → vendor blogs rejected; Ciena 403; Acacia no numbers); "Jetson
AGX Orin 275 TOPS technical brief" (11 → nvidia.com PDF); JLT/NTT anchors via "coherent transceiver
DSP power JLT 7nm" (8 → Stanford Kahn PDF + NTT article). 2023–2025 embedded-FPGA LSTM survey
sweep: 11–15 GOPS/W class, noted, not tabled.

**Sweep 4 (SiN heaters + control), key queries:** "silicon nitride thermo-optic phase shifter Pπ mW
measured" (9); "suspended SiN thermo-optic sub-milliwatt undercut response time" (8 → Zeng OL
2025); "CORNERSTONE silicon nitride MPW heater design rules" (8 → MPW#9 PDF, read); "LIGENTEC AN800
heater Ppi" (10 → press release no-number; Muñoz arXiv 2203.16956 via OPA paper search); "Harris
2014 thermo-optic silicon" (→ arXiv 1410.3616 PDF, 6 pp read); "AD5380 datasheet supply current
per channel" (10 → Farnell-hosted official Rev. D, read); "Al-Qadasi scaling silicon photonic
accelerators DAC power" (9 → ar5iv 2109.08025); "AIM Photonics PDK 2 mW DAC trim" (6 → none with
the number → UNVERIFIED). Failed: mdpi.com 403 ×2, analog.com timeouts, UGent 503,
cornerstone.sotonfab.co.uk platform page 404 (the MPW#9 PDF itself fetched fine).

**Executor spot-checks (2026-06-10):** cornerstone.sotonfab.co.uk MPW#9 Design Rules PDF →
"< 175mW/π phase shift" + 900 nm filament + process stack, exact match (§4.1); ti.com ADC12DJ3200
SLVSD97A pp. 13–18 → 3.0/3.6/3.8 W and ENOB 8.6/8.4/7.7-min/9.0, exact match (§2.4–2.5).
