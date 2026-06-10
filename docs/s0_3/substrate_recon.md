# S0.3-0 — Substrate design recon (tasks 1–4): debt #3, (α,Qᵢ) pairs, splitting, gain regime

**Author:** Executor · **Date:** 2026-06-10 · **Status:** recon for the **PR-4 freeze** — **menu,
not choice**: nothing here sets a value, builds substrate code, or runs training.
**Companion:** `docs/s0_3/pr4_input_sheet.md` (task 5 — the assembled PR-4 menus).
**Arithmetic kernel:** `analysis/s0_3_0_recon_arithmetic.py` →
`results/s0_3/s0_3_0_recon_arithmetic.json` (reuses the S0.1 `pole_region` conventions: amplitude
rates, κᵢ = ω₀/(2Qᵢ), symmetric add-drop κ_tot = κᵢ + 2κ_ext, HWHM splitting criterion; **every
reproduced S0.1/PR-10 anchor matched** — §5).

**Source markers** (S0.2-0 standard): **[EV]** = Executor-verified character-exact against a
primary fetched first-hand; **[AV]** = verified at abstract/secondary level (primary identified,
body not fetched); **[ABS]** = abstract-only/aggregated. Verification trail: Appendix A.

---

## 0. Headline findings (read first)

1. **Debt #3's premise is FALSE at the retrieval level.** The flagship Er:Si₃N₄ amplifier paper
   **does** measure its noise figure: *"A noise figure of ca. 7 dB is measured at net gain of
   >20 dB, limited by coupling losses"* (main text) and a full supplementary characterization
   (FIG. S11; 7.1 dB worked example) [EV — §1a]. The proposal-v0.5 debt line ("published gain but
   **no measured NF**") does not survive contact with the primary. **Consequence: the PR-4 noise
   cell anchors on a *measured* device value (~7 dB / n_sp ≈ 2.5), not an inferred bracket** —
   the debt is discharged in the *informative* direction (final wording S0.8, Supervisor).
2. **The D-08-3 roughness statistics are confirmed first-hand.** arXiv:2511.02198v1 Table 2 read
   directly: average doublet splittings **180–320 MHz**, doublet prevalence **21–75 %**, series
   Q_int **0.90(7)–2.8(2) M** — the B2 row is exact [EV — §3a]. (This discharges the *numbers*
   of B2's ⚠️ on that source; the full F5 primary pass stays S0.L-paced.)
3. **Splitting at operating κ_ext** (the blessed D-08-3 evaluation) materially reorders the
   corners: the foundry-conservative cell is **rescued by mild overcoupling** on all but the
   roughest process (2γ/κ_tot: 3.7 → 0.53 from r=0 to r=3, subtractive-low), while the
   **demonstrated AN800 corner is already marginal-split (1.66) under a *clean-process* γ in the
   undercoupled limit**, and the damascene corner un-splits only at r ≥ 3 — at 7× memory cost
   (§3b). The CW/CCW-knob default **"ON except clean-damascene" survives, with one sharpening**
   (§3c).
4. **The Er gain stage is rigorously quasi-static at every registered clock.** The flagship
   device's measured PL lifetime is **τ = 3.4 ms** [EV]; per-symbol gain ripple at the PR-10
   clocks is suppressed by ~10⁻⁵–10⁻⁸ and per-episode gain relaxation is ≤ 3 % even at L = 10⁵
   symbols (§4b). **"Gain saturation" in the SiN-native substrate therefore means a static,
   average-power-set operating point + ASE — not per-symbol gain dynamics.** This is a
   methodology-relevant fork (it decides what nonlinearity the recurrence sees in-loop) —
   **flagged to the Supervisor**, §4e.
5. **New foundry-MPW data point for D-08-1:** the probable primary behind the registry's AN800
   pair (Cui et al., Adv. Photon. Nexus 2023) itself demonstrates **0.033 dB/cm / mean Qᵢ ≈
   10.8 M on the standard AN800 open-MPW process** with a multimode racetrack [AV — §2c]. A
   foundry-process pair *above* the registry's mid-corner exists, with caveats (multimode
   geometry, 65 GHz FSR, unknown γ).
6. **Minor consistency note:** `mapping_result.md` §4 prose says CORNERSTONE memory "~33 rt";
   the registry-consistent value is **38.6 rt** (Qᵢ = 2.347×10⁵ derived from 1.5 dB/cm). The
   "~33" appears to round Qᵢ to 2×10⁵. Non-load-bearing; frozen text untouched (anomaly logged).

---

## 1. Task 1 — Debt #3: the Er:Si₃N₄ noise figure (critical-path item)

### 1a. What the flagship paper states — and what the debt claimed it didn't

**Identity.** Y. Liu, Z. Qiu, X. Ji, J. He, J. Riemensberger, M. Hafermann, R. N. Wang, J. Liu,
C. Ronning, T. J. Kippenberg, *"A photonic integrated circuit based erbium-doped amplifier"*,
arXiv:2204.02202**v2** (12 Apr 2022), fetched as PDF→text first-hand; SA-1 additionally diffed
the v1 and v2 LaTeX sources — **textually identical**, so every quote holds for both arXiv
versions. Journal of record: *Science* **376**, 1309–1313 (2022), DOI 10.1126/science.abo2631
(**published full text unreachable**, HTTP 403 — residual caveat: the published-PDF wording of
the main-text NF sentence is not string-verified; the arXiv source is the submitted manuscript
incl. the full SI). Device: ion-implanted Er in Si₃N₄ (Er ≈ 3.25×10²⁰ cm⁻³ headline device;
0.21-m waveguide for the gain headline, 21 cm for the NF measurement).

**The debt line being tested** (proposal v0.5 closing note / CLAUDE.md): *"Er:Si₃N₄ noise
figure — flagship gain device published gain but no measured NF."*

**What the primary actually says** — all [EV], grep-verified on the fetched text:

- Main text: **"A noise figure of ca. 7 dB is measured at net gain of >20 dB, limited by
  coupling losses (see Supplementary Information)."**
- Supplement (Note 13, *Noise figure of the Er:Si₃N₄ amplifier*): **"The noise figure of the
  Er:Si3N4 amplifier is measured using the commonly used optical source subtraction method[37]
  that can remove the source spontaneous emission (SSE) noise from the total noise emitted by
  the erbium amplifier."**
- Worked example (FIG. S11, 21-cm waveguide, forward 1480 nm pump, −1.9 dBm off-chip input,
  21 dB off-chip net gain): **"Using the Equation 6, a noise figure of 7.1 dB is obtained,
  including the contribution from the input fiber-to-chip coupling loss and relatively large
  spontaneous emission factor nsp upon a 1480 nm pumping (incomplete population inversion)."**
- Caveat stated by the authors: in the high-gain regime (>20 dBm on-chip pump, <−5 dBm signal)
  **"the noise figure measurement is affected by the parasitic lasing effect that limits the
  optical gain"** (FP cavity between chip facets; gain clamps at ~26 dB).
- Class framing (their intro, generic Er property, *not* a device claim): **"...low noise figure
  approaching the quantum mechanical limit of 3 dB for phase insensitive amplification[4]."**
- Gain/power context [EV]: **"30 dB small-signal gain"**; **"on-chip output power of 145 mW
  (21.6 dBm)"** (at 2.61 mW input, 245 mW coupled 1480-nm pump, ~60 % power-conversion
  efficiency); gain clamps at ~26 dB by facet-FP parasitic lasing.
- The decomposition inputs the paper *does* give [EV, SA-1]: **"fiber-to-chip coupling losses
  are 2.9 dB and 3.3 dB per side for 1550 nm and 1480 nm, respectively"** (SI §12) — i.e. the
  input-coupling term alone accounts for ~2.9 dB of the 7.1 dB fiber-referenced NF; per-cm
  **net gain coefficients 1.0 / 1.4 / 1.9 dB/cm** at Er concentrations 0.67/1.35/3.25×10²⁰ cm⁻³
  (1550 nm) — the gain-budget input used in §4f; **input saturation power ≈ −15 dBm measured
  (−14 dBm theory)** with A_eff = 1.2 µm² (SI §10).
- **Independent corroboration** (the same line's 2024 system paper, arXiv:2412.07627v2,
  Executor-re-grepped): *"the question remains whether the noise figure demonstrated on these
  EDWAs so far (7.1 dB) ..."* and *"The noise figure of the current EDWA setup is mainly limited
  by the fiber-to-chip coupling"* [EV] — the 7.1 dB and its coupling-loss attribution are how
  the authors' own group cites the result.
- **Post-2022 scan (SA-1, TARGET 2): no other measured Er:Si₃N₄ NF exists through 2026-06.**
  All 295 Semantic-Scholar-indexed papers citing the Science DOI screened for "noise figure":
  10 hits, none an Er:Si₃N₄ amplifier NF. The 2024 multi-lane Er:Si₃N₄ OFC paper (M4A.5,
  15 dB/lane) reports no NF (abstract; full text paywalled); the 2026 Er:Si₃N₄ laser paper
  (Nat. Commun. 17, 3722) has the qualitative class sentence only.

**Verdict on debt #3:** the flagship's NF **is measured: ≈7 dB (7.1 dB worked example) at
>20 dB net gain, forward 1480 nm pumping, including input-coupling loss.** The debt as worded
is factually dead; what *survives* of it is the **decomposition question** — how much of the
7 dB is (i) input fiber-to-chip coupling loss (the paper's own attribution; NF_dB adds the input
loss directly), (ii) 1480-pump incomplete inversion (their n_sp attribution; 980-pump erbium
systems reach lower n_sp), vs (iii) intrinsic medium penalties. The paper does not decompose it
numerically; no per-component budget exists. **For PR-4 this is a *bracket* question, not an
existence question** (§1c).

### 1b. Measured-NF brackets from the nearest comparables

The point of this table: locate the plausible NF range for an Er-doped *waveguide* gain element
of our class, so the PR-4 cell's value is an evidenced choice, not folklore. Subagent-gathered
(SA-2, full trail in its report → Appendix A.2); decisive rows Executor-re-verified as marked.
**Two of the Executor's draft assumptions died against the sources** — recorded honestly: the
sometimes-cited Mu et al. Er:Al₂O₃ "NF ~3–4 dB" could not be traced to any reachable primary
(abstract has no NF; an aggregator paraphrase was rejected), and Frankis et al. Er:TeO₂:Si₃N₄
reports **no NF at all** (full text verified: zero occurrences).

| # | System / class | Measured NF | Conditions | Source | Marker |
|---|---|---|---|---|---|
| B1 | **Er:Si₃N₄ (the flagship — the only on-platform number)** | **≈7 dB (7.1 dB example)** | net gain >20 dB, fwd 1480 nm pump, **fiber-referenced** (incl. 2.9 dB input coupling) | Liu et al., arXiv:2204.02202v2 / Science 376, 1309 (2022) | **[EV]** (Executor grep ×2 + SA-1/SA-2 + 2412.07627 corroboration) |
| B2 | Er:Al₂O₃ (reactively sputtered, manufacturable platform) | **6.5 ± 0.1 dB @ 1550 nm; min 5.6 ± 0.1 dB @ 1566 nm** (fiber-to-fiber) | external f2f net gain device | Osornio-Martinez, Bonneville, Dijkstra, García-Blanco, Opt. Express 33(11), 22458 (2025), DOI 10.1364/OE.558707; conf. BGPP 2024 JTh4A.1 "~6 dB" | **[AV]** (official NCBI abstract record; full text bot-blocked) |
| B3a | Er:LNOI / Er:TFLN | **4.49 dB min** (@1531.6 nm, −50 dBm input; ~6 dB plateau −45…−28 dBm) | 2.58 cm, 16 dB internal net gain; polarization-extinction method | Cai et al., IEEE JSTQE 28, 2022, arXiv:2108.08044 | **[EV]** (Executor re-grep of the fetched PDF) |
| B3b | Er:TFLN (monolithic, f2f) | **≈5 dB (4.9 dB worked example)** fiber-to-fiber | 18 dB f2f net gain; source-subtraction method | Li et al., arXiv:2508.11941 (2025) | **[AV]** (SA-2 full-text quotes) |
| B4 | Er:TeO₂-coated Si₃N₄ | **ABSENT — no NF reported** | 5 dB net gain device | Frankis et al., Photon. Res. 8(2), 127 (2020) — full text verified: zero "noise figure"/"NF"/"OSNR" occurrences | **[EV/absence]** (SA-2 full-text sweep) |
| B5 | EDWA class (Er phosphate glass, commercial) | **4.5 dB over the C-band** (vendor-stated product perf.) | 15 dB gain, 7 dBm out | Barbier (Teem Photonics CTO), Lightwave, Nov 2000 | **[AV]** (trade-primary, fetched) |
| B6 | EDFA reference class | **3.1 dB record** (54 dB gain); commercial **typ 4.5 / max 6 dB** | 980-pump record; C-band DWDM product | Laming/Zervas/Payne, IEEE PTL 4, 1345 (1992) (Soton ePrints); FS.com datasheet | **[AV]** |
| B7 | Quantum floor (phase-insensitive, high-G) | **3 dB** | half-quantum theorem | Caves, PRD 26, 1817 (1982) (fetched, MIT mirror) + RP Photonics "at least 3 dB"; the flagship's own sentence [EV] | **[EV]** |

*(Reading: the nearest **measured** integrated-Er comparables span ≈4.5–6.5 dB
(LNOI 4.49–5, EDWA 4.5, Al₂O₃ 5.6–6.5); the flagship's 7 dB sits just above that band and its
authors attribute the excess to input coupling + 1480-pump inversion. No integrated Er
waveguide amplifier has a measured NF at the 3-dB floor; the record EDFA reaches 3.1 dB.)*

### 1c. Candidate NF values for the PR-4 noise cell (menu — argument per row)

The substrate's ASE knob is cleaner parametrized by **n_sp** (the spontaneous-emission factor the
in-ring Langevin/per-round-trip injection actually uses) with NF ≈ 2·n_sp the high-gain
lumped-amp equivalent (the low-per-pass-gain caveat is a convention note in the input sheet §1).

| Cell | NF (dB) | n_sp | Argument | Risk it absorbs / ignores |
|---|---|---|---|---|
| **NF-A (as-measured, conservative)** | **7.0** | **2.5** | the only *measured* Er:Si₃N₄ number [EV]; foundry-grade conservatism: take the device as demonstrated, pump scheme and coupling overhead included | over-charges the *intracavity* model with an input-coupling penalty that is physically outside the ring (≈2.9 dB of the 7.1 is the input facet); harshest on memory-SNR |
| **NF-B (integrated-class best-comparable)** | **5.0** | **1.58** | the measured band of the nearest integrated hosts — Er:LNOI 4.49–5 [EV/AV], EDWA 4.5 [AV], Er:Al₂O₃ 5.6–6.5 [AV] — + the flagship authors' own attribution of their excess to coupling + 1480-pump n_sp [EV]; ≈ the coupling-decontaminated flagship (7.1 − 2.9 ≈ 4.2, +margin) | assumes coupling-decontamination / pump-scheme improvement never *demonstrated* on Er:Si₃N₄ (TARGET-2: nothing else measured through 2026-06) |
| **NF-C (quantum-floor, aspirational label only)** | **3.0** | **1.0** | the class limit (Caves theorem, fetched; flagship's own framing sentence [EV]); no integrated Er device measures there (EDFA record 3.1) | not a design point; sensitivity axis only — flag exactly like the class-leading-Q corner |

**Executor note (menu discipline):** house conservatism (foundry-grade gates Gate ii) points the
*headline* cell at **NF-A**, with NF-B/NF-C as labelled sensitivity cells; but the *choice* is
the freeze's (PR-4, Lucas), not made here. Sizing of all three against the (α,Qᵢ) corners — ASE
photons/round-trip — is in the input sheet §1 (from §5's kernel).

---

## 2. Task 2 — Candidate (α, Qᵢ) operating pairs (D-08-1 inputs)

### 2a. The self-consistent pairs

All four registry corners are already self-consistent by construction (S0.1/F13.1: one field
primary, the partner derived via Qᵢ = 2πn_g/(λα), λ = 1550 nm; `loss_q_consistency_error()`
test-enforced). Values below recomputed by the §5 kernel (they reproduce the registry exactly).

| Pair | Primary field | Derived partner | κᵢ/2π (MHz) | Intrinsic FWHM (MHz) | Passive memory | Provenance | Marker |
|---|---|---|---|---|---|---|---|
| **P-CORN** `SiN_CORNERSTONE_300` | α = 1.5 dB/cm | Qᵢ = 2.35×10⁵ | 412.0 | 824.0 | 0.39 ns = **38.6 rt** | Littlejohns et al., Appl. Sci. 10, 8201 (2020) (C-band ~1.5 dB/cm; no published ring Q) | [AV] (registry-carried) |
| **P-FND** `SiN_foundry_conservative` | Qᵢ = 2×10⁶ | α = 0.172 dB/cm | 48.4 | 96.7 | 3.29 ns = **329 rt** | constructed conservative cell (deliberately unattributed, S0.1.1/F7); the Gate-ii / F13 candidate | n/a (by design) |
| **P-AN800** `SiN_LIGENTEC_AN800` | α = 0.051 dB/cm | Qᵢ = 6.80×10⁶ | 14.2 | 28.4 | 11.2 ns = **1119 rt** | **Cui et al., Adv. Photon. Nexus 2(4), 046007 (2023)** — identified this recon as the probable primary ("(6.8±0.4)×10⁶ … 0.051±0.003 dB/cm … standard LIGENTEC-AN800") | **[AV]** — body JS-walled; **verify at freeze** (Appendix A) |
| **P-UHQ** `SiN_damascene_UHQ` | Qᵢ = 3×10⁷ | α = 0.0123 dB/cm | 3.2 | 6.4 | 49.4 ns = **4937 rt** | Liu et al., Nat. Commun. 12, 2236 (2021) (wafer-scale damascene, Q₀ > 30 M) | [AV] (registry-carried) |
| **P-MPW-MM** *(new candidate, not in registry)* | α = 0.033 dB/cm (3.3 dB/m) | Qᵢ ≈ 10.8×10⁶ (their mean measured) | ≈9.0 | ≈17.9 | ≈17.8 ns ≈ **1780 rt** | same Cui et al. 2023: multimode racetrack **on the standard AN800 MPW**, effective radius 195 µm, width 3 µm, FSR 65 GHz | **[AV]** (abstract quoted verbatim via S2 API) |

**P-MPW-MM caveats (stated, not resolved):** multimode geometry (higher-order-mode suppression by
design — interaction with backscatter/γ unknown; **no published γ**); FSR 65 GHz ≠ the 100-GHz
registry convention (rt = 15.4 ps — memory-in-rt rescales, memory-in-ns doesn't); single
published device family. It enters the menu as evidence that **"foundry-grade" need not mean
Qᵢ = 2×10⁶** — an open-MPW pair at 10.8 M exists — not as a registered cell.

### 2b. The EV-F3 check — informationally distinct poles/GHz at N = 128

Convention: poles count as informationally distinct at **1 loaded-FWHM separation**
(FWHM = κ_tot/π Hz); "in-band N" = poles/GHz × signal band (≈ the line rate: 1 GHz @ 1 GS/s,
2 GHz @ 2 GS/s). Undercoupled limit (r → 0) reproduces the envelope's EV-F3 figures exactly
(foundry 10.3/GHz ~ "O(10–20)", class-leading 155/GHz ~ "~150").

| Pair | poles/GHz (r=0 / r=1 / r=3) | max in-band N @ 1 GS/s (r=0/1/3) | @ 2 GS/s (r=0/1/3) | PR-10 N-grid verdict |
|---|---|---|---|---|
| P-CORN | 1.2 / 0.4 / 0.2 | 1 / 0 / 0 | 2 / 1 / 0 | supports **no** grid cell in-band |
| P-FND | 10.3 / 3.4 / 1.5 | 10 / 3 / 1 | 21 / 7 / 3 | **N=8 ✓** (r ≲ 1 @ 1 GS/s; r ≲ 3 @ 2 GS/s); N=32 ✗; N=128 ✗ |
| P-AN800 | 35.2 / 11.7 / 5.0 | 35 / 12 / 5 | 70 / 23 / 10 | **N=8 ✓ all r; N=32 ✓ undercoupled** (r ≲ 0.3 @ 1 GS/s, r ≲ 1 @ 2 GS/s); N=128 ✗ |
| P-UHQ | 155.1 / 51.7 / 22.2 | 155 / 52 / 22 | 310 / 103 / 44 | **N=128 ✓ only here** — and only undercoupled-to-critical (r ≲ 0.1 @ 1 GS/s, r ≲ 1 @ 2 GS/s) |
| P-MPW-MM | ≈55.7 / 18.6 / 8.0 | 56 / 19 / 8 | 111 / 37 / 16 | N=32 ✓ to r≈1 @ 1 GS/s; **N=128 ✗ at 1 GS/s, marginal-✗ @ 2 GS/s** (111 < 128 at r=0) |

**The EV-F3 adjudication, on numbers:** the PR-10 grid's N=128 cell is realizable **only at the
class-leading pair, only at κ_ext ≲ critical** — which §3b shows is exactly the
**splitting-broken** regime of that pair (2γ/κ_tot = 2.4–7.3 clean-process for r ≤ 1). So
{N=128 ⇄ class-leading-Q ⇄ splitting} is not a three-way tension but a **two-against-one**: the
N=128 cell *requires* the CW/CCW doublet knob ON (or an explicit doublet-tolerant architecture
statement). Joint-adjudication options → input sheet §6. *(Alternative reading: if poles are
spread over the full FSR rather than the signal band, packing is unconstrained at every corner —
but then most poles are spectrally outside the encoded band and act as weak shoulders; the
envelope's C5/C8 op-count consistency used the in-band reading. The freeze should state which
reading PR-4 adopts; both are tabulated in the JSON.)*

### 2c. Memory at the registered clocks (the PR-2-cell sizing)

Passive (r=0) memory in **samples** (1/e amplitude), from §5's kernel — these reproduce the
registered corners (0.33/3.29/6.58 foundry; 4.94/49.4/98.7 class-leading):

| Pair | @ 0.1 GS/s | @ 1 GS/s | @ 2 GS/s | vs T-A 7-tap span @ 2 GS/s | vs PR-13 k-grid @ 1 GS/s |
|---|---|---|---|---|---|
| P-CORN | 0.04 | 0.39 | 0.77 | ✗ (≪7) | k=1 already ≫ memory |
| P-FND | 0.33 | 3.29 | 6.58 | **marginal-✗ (6.58 < 7)** — the registered "honestly marginal" cell | k ≤ 3 in-memory; k ≥ 10 over the cliff |
| P-AN800 | 1.12 | 11.2 | 22.4 | ✓ (3.2× span) | k ≤ 10 in-memory; k = 30 marginal (×2.7 over) |
| P-UHQ | 4.94 | 49.4 | 98.7 | ✓ (14× span) | k ≤ 30 in-memory; **k = 100 = the designed cliff** (×2.03 over; e⁻²·⁰ ≈ 0.13 retention) |
| P-MPW-MM | 1.78 | 17.8 | 35.6 | ✓ | k ≤ 10 in; k = 30 ×1.7 over |

κ_ext loading shrinks every number (×1/(1+2r)); the full ladder is in the input sheet §2.

---

## 3. Task 3 — Roughness / mode-splitting sub-parameter (D-08-3)

### 3a. Sourced statistics per process class — first-hand status

The B2 source set is reused (it is the registered evidence base; the full F5 primary pass stays
S0.L-paced). What this recon adds: **first-hand verification of the decisive subtractive-process
source**, and the γ menu rows below.

| Process class | γ/2π (one-direction rate) | Evidence | Marker |
|---|---|---|---|
| damascene-clean | **11.8 MHz** (2γ/2π = 23.6) | Kondratiev/.../Kippenberg, Nat. Commun. 12, 235 (2021): Q₀>10⁷ device, 2γ/κ_tot ≈ 0.34 | [AV] (B2-carried; F5-paced) |
| subtractive-low | **90 MHz** (180) | arXiv:2511.02198v1 Table 2 (polymer-mask series S1–S3): avg doublet splittings **180–210 MHz**, prevalence **21–27 %**, Qint 2.7(2)–2.8(2) M | **[EV]** — Table 2 read first-hand this recon |
| subtractive-high | **160 MHz** (320) | same, metal-mask series H1–H4: avg splittings **230–320 MHz**, prevalence **62–75 %**, Qint 0.90(7) M | **[EV]** — first-hand |
| AN800 / CORNERSTONE specific | **no published γ** (B2 caveat b) — re-checked this recon: still none found | Appendix A queries | [absence] |

Identity of the subtractive source, now read directly: L. Rukh, G. M. Colación, F. H. Buck,
T. E. Drake (Univ. New Mexico), *"Process-structure-property relationships in subtractive
fabrication of silicon nitride microresonators for nonlinear photonics"*, arXiv:2511.02198v1
(4 Nov 2025). B2's row ("90–160 MHz, 21–75 %, Qint 0.9–2.8×10⁶") is **exact** [EV].

### 3b. Splitting evaluated AT OPERATING κ_ext (the blessed D-08-3 constraint)

2γ/κ_tot under the registered **HWHM criterion** (≥1 ⇒ doublet resolves; the FWHM convention
halves every ratio — band note as in B2); κ_tot = (1+2r)κᵢ, r = κ_ext/κᵢ per coupler
(symmetric add-drop). Full tables: §5 JSON; decision-relevant rows:

| Pair | process | r=0 | r=0.3 | r=1 | r=3 | r=10 | reading |
|---|---|---|---|---|---|---|---|
| P-FND | clean | 0.49 | 0.31 | 0.16 | 0.07 | 0.02 | single-pole at any r |
| P-FND | sub-low | 3.72 | 2.33 | 1.24 | **0.53** | 0.18 | split undercoupled → **rescued at r ≳ 3** |
| P-FND | sub-high | 6.62 | 4.14 | 2.21 | **0.95** | 0.32 | marginal at r=3, clean at r=10 |
| P-AN800 | clean | **1.66** | 1.04 | 0.55 | 0.24 | 0.08 | **already marginal-split undercoupled even clean-process**; rescued by r ≳ 0.3–1 |
| P-AN800 | sub-low | 12.7 | 7.9 | 4.2 | 1.8 | 0.60 | split until deep overcoupling |
| P-UHQ | clean | 7.32 | 4.58 | 2.44 | **1.05** | 0.35 | split through critical; **un-splits only at r ≳ 3** (memory 4937 → 705 rt) |
| P-CORN | sub-high | 0.78 | 0.49 | 0.26 | 0.11 | 0.04 | splitting-safe at every r (even roughest process) |

**What this changes vs the undercoupled-worst-case reading:** (i) the foundry cell's
"already split on a rough process" verdict is **κ_ext-conditional** — a near-critical-to-
overcoupled policy (r ≈ 1–3) restores single-pole on subtractive-low and is marginal on
subtractive-high, at the documented memory cost (329 → 110–47 rt); (ii) the **κ_ext policy and
the splitting knob cannot be registered independently** (B3's coupling, now quantified); (iii)
the class-leading N=128 story (§2b) lives entirely in the split regime unless r ≥ 3, which
collapses its packing advantage (155 → 22 poles/GHz) *and* its memory (→ 705 rt ≈ 14.1 samples
@ 2 GS/s — still ≥ the T-A 7-tap span, notable).

### 3c. CW/CCW-knob default policy options (confirm-or-revise verdict)

The blessed default — **knob ON except the clean-damascene corner** — **survives the sources,
with one sharpening and one κ_ext condition**:

- **K-pol-1 (blessed default, confirmed):** ON for any subtractive/rough process at any Q and
  for any pair at Qᵢ ≳ 4×10⁶ (the B2 clean-process crossover); OFF only for damascene-clean at
  foundry-Q (P-FND-clean: 0.49 undercoupled). *Sharpening from §3b:* **P-AN800 does not qualify
  for OFF even clean-process** in undercoupled policies (1.66 at r=0) — the OFF cell is
  *foundry-Q + clean-process + any r*, not "clean process" generally.
- **K-pol-2 (κ_ext-conditional OFF):** OFF additionally wherever the *registered* κ_ext policy
  puts 2γ/κ_tot < 1 at the registered γ (e.g. P-FND/sub-low at r ≥ 3). Cheaper substrate; ties
  the knob's validity to the κ_ext freeze — must be re-evaluated if PR-4 ever revisits κ_ext.
- **K-pol-3 (always ON, γ as a registered noise parameter):** one substrate code path; γ = 0
  recovers single-pole exactly; the registered cell sets γ per process class (menu §3a). Most
  honest; costs a 2×2 block per ring in the substrate (compute ×~2 on the ring update).

(The S0.3-1 implementation cost of the 2×2 CW/CCW block is the same machinery the coupled-μ
hook already needs — flagged for the Supervisor's S0.3-1 spec, not decided here.)

---

## 4. Task 4 — Gain-stage physics inventory (what "gain saturation" means on SiN)

### 4a. The lifetimes, sourced

All fetched first-hand by SA-3 (PDFs/HTML retrieved + quoted; trail in Appendix A.2); the
flagship value additionally Executor-grep-verified.

| Medium | τ (⁴I₁₃/₂) | Source (fetched) | Marker |
|---|---|---|---|
| **Er:Si₃N₄ (the flagship device)** | **3.4 ms** (1/e PL decay, post-anneal; 1.5 ms pre-anneal) | arXiv:2204.02202v2: "τ = 3.4 ms is the PL lifetime extracted from the temporal measurement" + SI §8: "An increased lifetime τ of 3.4 ms ... compared to 1.5 ms before annealing" | **[EV]** |
| Er:Al₂O₃ | **7.6 ± 0.2 ms intrinsic** (7.5→6.1 ms vs concentration; radiative 8.6 ± 0.5) | Bradley PhD thesis (U. Twente 2009, OA PDF), §4.3.4 — same group/data as the (paywalled) Bradley & Pollnau LPR 2011 review | [AV] (fetched by SA-3) |
| Er:silica (EDFA) | **10.5 ms / 12 ms** worked examples; "order of 10 ms" | Bononi & Rusch, JLT 16(5), 945 (1998) (author-hosted PDF); RP Photonics EDFA article | [AV] (fetched by SA-3) |
| Er:LNOI | **2.3 ms** (1/e fluorescence) | Cai et al., arXiv:2108.08044 | [AV] (fetched) |
| SOA (III-V) carrier | **~50 ps**; recovery 0.1–1 ns with bit-pattern ("code type") effects | Bradley thesis §5.3.1; Cui/Zoiros/Kotb review, Nanomaterials 16, 202 (2026) (PMC, verbatim-verified) | [AV] (fetched) |
| Class statement | "long ms-lifetime ... leads to **slow gain dynamics and negligible inter-channel crosstalk** in multiwavelength amplification" | the flagship's own intro | **[EV]** |
| The operative quasi-static statement | "the amplifier gain stays quite precisely constant when amplifying a bit stream, as the energy per bit usually stays orders of magnitude below the saturation energy. ... Only over thousands or millions of data symbols, the gain adjusts itself to the average signal power level." | RP Photonics, "Erbium-doped Fiber Amplifiers" (verbatim-verified vs raw HTML) | [AV] (fetched) |
| SOA-vs-EDFA contrast | "Unlike EDFAs, SOAs have a much shorter carrier lifetime, below a nanosecond, so that the gain relaxation is sufficiently fast to track the data stream when the SOA enters saturation." | Moscoso-Mártir et al., arXiv:1605.08668 / Sci. Rep. 7, 13857 (2017) | [AV] (fetched) |

### 4b. The regime arithmetic (vs the registered clocks)

With τ = 3.4 ms [EV], rt = 10 ps, PR-10 clocks {0.1, 1, 2} GS/s, first-order gain low-pass
(corner f_c = 1/2πτ = **46.8 Hz** unsaturated; ~×2 under deep saturation):

| Timescale | value | τ / timescale | gain response |
|---|---|---|---|
| round trip | 10 ps | 3.4×10⁸ | frozen |
| symbol @ 2 / 1 / 0.1 GS/s | 0.5 / 1 / 10 ns | 6.8×10⁶ / 3.4×10⁶ / 3.4×10⁵ | frozen — per-symbol gain ripple suppressed ×2.3×10⁻⁸ / 4.7×10⁻⁸ / 4.7×10⁻⁷ |
| episode/sequence L = 10³–10⁵ @ 1 GS/s | 1–100 µs | 3400 → 34 | quasi-frozen — ≤ 2.9 % relaxation toward a moved operating point per episode (1.5 % @ 2 GS/s, L=10⁵) |
| batch/epoch, heater settle, SPSA cadence | ≥ ms | ≲ 3.4 | **gain follows** (adiabatically tracks average power / pump / trim changes) |

**The large-signal check (the low-pass argument alone is not sufficient).** Bononi & Rusch's
honest caveat [AV, fetched]: *"the gain dynamics can be extremely fast upon strong signal pulse
arrivals, due to the stimulated-emission avalanche depletion of the reservoir"* — i.e. ms-τ does
not protect against *energy*-scale transients; the correct quasi-static criterion is
**E_symbol ≪ E_sat plus stationary average power**. With the flagship's measured input
saturation power (−15 dBm ≈ 31.6 µW [EV]) and τ = 3.4 ms: E_sat ≈ 108 nJ;
E_symbol = 0.5–10 pJ at 1 mW drive across the clock grid → **E_sym/E_sat ≈ 5×10⁻⁶–9×10⁻⁵**
(1.3×10⁻² even at 145-mW-class power × 10 ns) — quasi-static holds with ≥4 orders of margin.
The remaining condition is **stationarity of the drive statistics within an episode**: the
registered task families are i.i.d./stationary symbol streams (PR-2 T-A 4-PAM i.i.d.; PR-13
synthetic family), so the average power is episode-constant by construction. **Bursty/packeted
inputs would void this** (Bononi & Rusch: ~1–2 dB sag on a 1 µs, 2 mW packet in a fiber EDFA) —
registered as M1's validity condition, not a hidden assumption.

**Conclusion (load-bearing for S0.3-1):** at every registered clock the Er gain element is a
**static, average-power-saturated operating point within an episode**; gain dynamics live only at
the *training* cadence (batch-to-batch drift, SPSA perturbation tracking, add/drop-class
average-power changes — the µs–ms regime per Bononi & Rusch) — where the existing
`drift_inject` machinery and a slow operating-point update model them, not the in-rollout ODE.

### 4c. Consequence for the salvaged rate-equation model

`dynamic_gain.TrainingAwareDynamicSOAPerMode` (τ_c ~ 100s ps) models a regime the SiN-native
Er stage **does not have** (T_sym/τ_c ≈ 2.5 at 2 GS/s for an SOA → real inter-symbol patterning;
T_sym/τ_Er ≈ 10⁻⁷ → none). Its roles, accurately stated:
- **III-V/SOA fallback candidate** (the proposal's §8 fallback platform): per-symbol dynamic
  saturation as-is — the regime it was built for (its own docstring already says erbium is
  "quasi-static at round-trip timescales" — confirmed quantitatively here);
- **τ-swapped slow tier:** the same integrator with τ_c = 3.4 ms is *numerically correct* for Er
  but integrates a near-constant — it buys nothing in-episode (§4b) at full rollout cost;
- **NOT** the SiN-native saturation model: that is the static operating-point solve (§4d M1).

### 4d. Menu — substrate gain-model classes

| Model | What it is | Cost | What it buys / loses | Regime fit |
|---|---|---|---|---|
| **M1 — static saturated gain + ASE** | per-episode operating point g(P̄) = g₀/(1+P̄/P_sat) (or the log-gain equivalent), fixed within the rollout; ASE injected per round trip at n_sp (§1c); slow drift via the existing drift knob between episodes | cheapest; no extra state in the rollout | loses nothing the Er physics has in-episode (§4b); loses cross-episode gain memory *if* average drive power varies episode-to-episode (can be reintroduced as the drift knob) | **the Er:Si₃N₄-native cell** at all registered clocks |
| **M2 — full rate equation, τ = 3.4 ms** | the salvaged training-aware integrator, τ swapped | full rollout integration + checkpoint memory | physically exact; in-episode it integrates ≤3 %-relaxation dynamics (numerically inert); only matters if episodes are ms-long (none registered are) | correct but wasteful for Er; defensible only as a validation reference for M1 |
| **M3 — rate equation, τ_c ~ 0.1–0.5 ns** | the salvaged model as-is | same as M2 | real per-symbol patterning + nonlinearity in-loop | **the III-V/SOA fallback platform**, not SiN-native |

(All three keep architecture constraints 3a/3b: M1's operating point enters the graph as a
differentiable function of the drive statistics — no detach.)

### 4e. ⚠️ METHODOLOGY FORK — flagged to the Supervisor (per the task spec)

The choice between M1 and M3-as-headline is **not a fidelity knob, it changes what the
estimators face**: under M1 the in-loop physics of the SiN-native substrate is **linear**
(dissipative ring + static gain) with additive ASE — the only task-solving nonlinearity is the
readout |·|² (exactly the PF-F1 structure; the Critic's linear floor becomes the *substrate's
own* structure at the SiN-native cell). Per-symbol gain nonlinearity exists only on the III-V
fallback (M3). This affects: PAT twin-mismatch families (what structural omission means), the
adjoint's linearity assumptions, RHEL's echo (conjugating a linear vs gain-patterned field), and
the reservoir-baseline contrast. **The roadmap's S0.3 line "erbium (or III-V) gain saturation"
silently spans both regimes; PR-4 (or a ledger note) should name which regime the registered
cell is in.** Recommendation implicit in the physics (M1 = SiN-native); the *decision* is the
Supervisor's/ledger's — this flag is the deliverable.

### 4f. Gain-budget feasibility per (α,Qᵢ) corner (new sizing row)

Does flagship-class Er gain even cover the ring's round-trip loss? Available per-round-trip gain
= demonstrated net gain coefficient (1.0–1.9 dB/cm at 1550 nm [EV], §1a) × ring circumference
(L = c/(n_g·FSR) ≈ 1.43–1.54 mm at the 100-GHz registry convention); required = the corner's
per-rt loss × (1+2r) at coupling load r:

| Pair | intrinsic loss/rt (dB) | available Er gain/rt (dB) | headroom r=0 | r=1 | r=3 |
|---|---|---|---|---|---|
| P-CORN | 0.2248 | 0.150–0.285 | **×0.7–1.3 (marginal)** | ×0.22–0.42 ✗ | ×0.10–0.18 ✗ |
| P-FND | 0.0264 | 0.154–0.292 | ×5.8–11.1 ✓ | ×1.9–3.7 ✓ | ×0.8–1.6 marginal |
| P-AN800 | 0.0078 | 0.152–0.289 | ×20–37 ✓ | ×6.5–12 ✓ | ×2.8–5.3 ✓ |
| P-UHQ | 0.0018 | 0.143–0.273 | ×82–155 ✓ | ×27–52 ✓ | ×12–22 ✓ |

**Reading:** the Er-gain budget **closes with margin at P-FND and above** for moderate coupling;
at **P-CORN it is marginal at zero load and infeasible loaded** — i.e. the loss-compensation
story (the S0.1 plot's net-gain 50/90 % conventions) is *not* available at the CORNERSTONE
corner with demonstrated Er:Si₃N₄ gain. **Assumption flag:** this applies the flagship's
*straight-implanted-waveguide* gain coefficient to a ring on a different process — a Stage-1
integration assumption (doping a foundry ring is undemonstrated); the menu row says "if
flagship-class implantation were applied", nothing stronger. (Pump-power accounting is S0.7
territory, not re-budgeted here.)

---

## 5. Arithmetic kernel + reproduced-anchor validation

`analysis/s0_3_0_recon_arithmetic.py` (pure arithmetic; imports only `photonic_ssm.platforms` +
`photonic_ssm.dynamics.pole_region` — **zero substrate code added**), output
`results/s0_3/s0_3_0_recon_arithmetic.json`. Conventions inherited: amplitude rates;
κᵢ = ω₀/(2Qᵢ); κ_tot = κᵢ + 2κ_ext (symmetric add-drop); HWHM splitting criterion (FWHM = ×2
band); memory = 1/κ_tot; FWHM(Hz) = κ_tot/π; ASE photons/rt = n_sp(G_rt−1), n_sp = 10^(NF/10)/2.

**Reproduced registered anchors (all exact):** foundry passive 329.1 rt & samples
0.33/3.29/6.58 @ 0.1/1/2 GS/s; class-leading 4937 rt & 4.94/49.4/98.7; B3 κ_ext ladder
274/206/110/47/16 rt with drop efficiencies 0.028/0.141/0.444/0.735/0.907; B2 undercoupled
ratios 0.49/3.7/6.6 (foundry corner); EV-F3 packing 10.3 vs 155.1 poles/GHz.

---

## Appendix A — search / verification trail (reproducible)

### A.1 Executor first-hand fetches (decisive items; 2026-06-10)

| Item | URL | Format | Verified strings |
|---|---|---|---|
| Flagship NF + lifetime + gain/power | arxiv.org/abs/2204.02202 → /pdf/2204.02202 (v2) | PDF→pdftotext (3041 lines) | "noise figure of ca. 7 dB is measured at net gain of >20 dB"; "a noise figure of 7.1 dB is obtained, including the contribution from the input fiber-to-chip coupling loss and relatively large spontaneous emission factor nsp upon a 1480 nm pumping"; "optical source subtraction method[37]"; "τ = 3.4 ms is the PL lifetime"; "compared to 1.5 ms before annealing"; "quantum mechanical limit of 3 dB for phase insensitive amplification[4]"; "30 dB small-signal gain"; "on-chip output power of 145 mW"; parasitic-lasing sentences. grep terms: "noise figure" (15 hits), "NF", "PL lifetime", "ca. 7 dB", "7.1 dB" |
| Subtractive roughness stats | arxiv.org/pdf/2511.02198 (v1) | PDF→pdftotext (1164 lines) | Table 2 rows S1–S3 (210/180/180 MHz; 27/27/21 %), H1–H4 (280/300/230/320 MHz; 62/75/62/65 %); "average Qint of 2.7(2) million"; "0.90(7) million"; "2.8(2)M"; title/authors first-hand |
| Corroborator (flagship NF as cited by its own line) | arxiv.org/pdf/2412.07627 (v2) | PDF→pdftotext | "the question remains whether the noise figure demonstrated on these EDWAs so far (7.1 [dB]" ; "The noise figure of the current EDWA setup is mainly limited by the fiber-to-chip coupling" ; "slightly lower noise figure (about 7 dB on average [12])" |
| Er:LNOI 4.49 dB (decisive comparable) | arxiv.org/pdf/2108.08044 | PDF→pdftotext | "4.49 dB noise figure at 1531.6 nm" (abstract + body) |
| AN800 pair primary (identity) | api.semanticscholar.org DOI:10.1117/1.APN.2.4.046007 | JSON (abstract verbatim) | Cui, Cao, Pan, Gao, Yu, Zhang; APN 2(4) 046007 (2023); abstract: "propagation loss of only 3.3 dB/m and a mean intrinsic Q of around 10.8 million"; SPIE full text + researching.cn mirror both unreachable (JS-wall / TLS error) → **0.051/6.8 body sentence = [AV], verify at PR-4 freeze** |

### A.2 Subagent sweeps (3 parallel, 2026-06-10; prompts in the session record)

| Agent | Mission | Key returns | Accounting |
|---|---|---|---|
| SA-1 | Er:Si₃N₄ flagship exhaustive + post-2022 NF scan | v1/v2 LaTeX diff identical; **all 13 "noise figure" occurrences quoted**; coupling losses 2.9/3.3 dB/side; gain coefficients 1.0/1.4/1.9 dB/cm; input sat −15 dBm; TARGET-2 verdict (no other Er:Si₃N₄ NF; 295 citing papers screened); CLEO-2022 "saturation output power exceeding 25 mW" companion | ~105k tokens, 57 tool calls, ~14 min |
| SA-2 | Waveguide-amp NF comparables (6 classes) | Osornio-Martinez OE 2025 (6.5/5.6 dB); Cai JSTQE 2022 (4.49); Li arXiv:2508.11941 (~5 f2f); Frankis NF-ABSENT (full-text-verified); Teem/Barbier 4.5; Laming 3.1; Caves PRD fetched; **killed two draft assumptions** (Mu et al. NF untraceable; Frankis bound nonexistent) | ~101k tokens, 65 tool calls, ~16 min |
| SA-3 | Er gain-dynamics timescales | lifetimes fetched: silica 10.5/12 ms (Bononi & Rusch PDF), Al₂O₃ 7.6 ms (Bradley thesis), LNOI 2.3 ms, Er:Si₃N₄ 3.4 ms; the RP-Photonics quasi-static statement verbatim; the **avalanche-depletion caveat** (Bononi & Rusch) that sharpened §4b; SOA 50 ps / 0.1–1 ns contrast quotes | ~94k tokens, 47 tool calls, ~15 min |

Total subagent spend ≈ 300k agent tokens, 169 tool calls. Their full per-query search trails
(engines, hit counts, failed/blocked fetches incl. Science 403, LPR-2011 Wiley wall, IEEE walls,
Optica full-text gates) are in the session record; every decisive number was either
Executor-re-verified ([EV] rows) or carries the subagent's fetch provenance ([AV] rows).

### A.3 Executor tool/query summary

WebSearch ×2 (AN800 pair → Cui-paper identity), Semantic Scholar API ×1 (Cui metadata/abstract),
arXiv PDF fetches ×4 (2204.02202, 2511.02198, 2412.07627, 2108.08044) + targeted greps as in
A.1; SPIE/researching.cn fetch attempts failed (JS-wall / TLS) — recorded against the
P-AN800 [AV] marker. Date of record for all retrievals: **2026-06-10**.
