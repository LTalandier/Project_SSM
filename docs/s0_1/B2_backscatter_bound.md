# B2 — Backscatter / CW–CCW mode-splitting bound (S0.1 deliverable 5 / F19)

**Status:** Executor literature-sourced physics input. Sets whether S0.3 needs an optional
mode-splitting knob (F19). Framing is Supervisor/S0.L; the **recommendation** below is the Executor's.

> ⚠️ **"Say it loudly" finding (the task flagged this exact case).** Backscatter splitting is
> **fabrication-roughness-limited, NOT cleanly Q-gated.** It can break the core "one ring = one complex
> pole" abstraction **within the registered Q range** — already at foundry `Qi≈2×10⁶` on a *rough*
> process. This refines (and partly contradicts) the roadmap's prior assumption that splitting is
> "negligible at foundry Q≈2×10⁶, not at 10⁷."

## Physics

Surface roughness backscatters the CW mode into the CCW mode at a **coherent rate `gamma`** (set by the
back-scattered field amplitude ∝ sidewall roughness × cavity length — an **absolute rate**, essentially
independent of `kappa_tot`). The two counter-propagating modes hybridize into standing-wave doublets
split by `2*gamma`. The resonance **resolves into a doublet** (→ "one ring = one pole" fails; the ring
is two modes) when

    2*gamma  ≳  kappa_tot       (undercoupled worst case: kappa_tot → kappa_i = omega0/(2 Qi)).

Because `gamma` is a fixed fabrication rate while `kappa_i = omega0/(2 Qi)` **falls as Qi rises**, a
fixed `gamma` becomes an ever-larger fraction of the linewidth: **splitting grows with Q.** External
coupling (`kappa_ext > 0`) widens the linewidth and *suppresses* visible splitting (an overcoupled
device may hide an intrinsic doublet).

Kernel: `photonic_ssm.dynamics.pole_region.{splitting_linewidth_ratio, crossover_Q,
gamma_rad_s_from_MHz_linear}`. Figure: `results/s0_1/backscatter_crossover.png`.

## Cited SiN data points (measured)

| `gamma/2π` (split `2γ/2π`) | Ring / Q | Source |
|---|---|---|
| **11.8 MHz** (23.6 MHz) | damascene Si₃N₄, Q₀>10⁷, κ_tot/2π=69.3 MHz → 2γ/κ_tot≈0.34 | Kondratiev/Voloshin/Kippenberg, *Nat. Commun.* **12**, 235 (2021), arXiv:1912.11303 |
| **90–160 MHz** (180–320 MHz) | subtractive Si₃N₄, Q_int 0.9–2.8×10⁶, σ_sidewall 1–4 nm; **21–75 % of modes split** | "Process-structure-property … subtractive Si₃N₄", arXiv:2511.02198 (2025), Tables 1–2 ⚠️ |
| ~31 MHz (~63 MHz) | damascene Si₃N₄, Q₀≈6×10⁶, 45 MHz linewidth → split | Pfeiffer et al., damascene process, *IEEE JSTQE* 24 (2018) ⚠️ (63 MHz via search-aggregation — verify) |
| "visible splitting" (qual.) | high-confinement Si₃N₄, **Q_i = 37–67×10⁶**, FWHM 3.3–6.2 MHz — splitting is the *normal* UHQ observation | Bauters/Gondarenko/Lipson, arXiv:1609.08699 / CLEO 2017 ⚠️ |

Mechanism + mitigation reference (non-SiN): coherent backscatter suppression >30 dB, Jin/Kippenberg,
*Light Sci. Appl.* **9**, 41 (2020). Quantitative Si model: Li et al., *Laser Photon. Rev.* **10**, 420
(2016).

## Crossover (computed)

**Criterion band.** A doublet becomes *visible* when the splitting reaches the half-width and *fully
resolves* when it reaches the full width. We register the **conservative (HWHM) criterion `2γ ≳ κ_tot`**
(`κ_tot` is the HWHM in rad/s; the power-FWHM linewidth is `2κ_tot`). The fully-resolved (FWHM) criterion
`2γ ≳ 2κ_tot` needs twice the `γ` — equivalently half the linewidth → **twice the Q** — so **every
`Q_crossover` below shifts ×2 under the FWHM convention** (band shown). The qualitative conclusion is
unchanged under both. Undercoupled worst case `κ_tot → κ_i = ω0/(2 Qi)`; each row uses a **single `γ`**
(the `2γ/κ_i` columns and `Q_crossover` are now computed from the same `γ/2π`).

| Scenario | `γ/2π` (split `2γ/2π`) | **Q_crossover** (HWHM → FWHM band) | At foundry `Qi=2×10⁶` | At class-leading `Qi=3×10⁷` |
|---|---|---|---|---|
| damascene-clean | 11.8 MHz (23.6) | **4.1×10⁶ → 8.2×10⁶** | `2γ/κ_i = 0.49` → **single-pole OK** | `2γ/κ_i = 7.3` → **split** |
| subtractive-low-roughness | 90 MHz (180) | **5.4×10⁵ → 1.1×10⁶** | `2γ/κ_i = 3.7` → **already split** | `55.8` → split |
| subtractive-high-roughness | 160 MHz (320) | **3.0×10⁵ → 6.0×10⁵** | `2γ/κ_i = 6.6` → **already split** | `99` → split |

(The high-roughness row previously mixed a 160-MHz `Q_crossover` with 125-MHz ratios — `5.2/77.6`; with a
single `γ/2π = 160 MHz` the consistent ratios are **`6.6/99`**, as tabulated.)

So **clean (damascene-class) process**: single-pole holds at foundry Qi, breaks by ~4×10⁶ (HWHM; ~8×10⁶
FWHM) and is firmly broken at the aspirational 3×10⁷. **Rough (subtractive) process**: splits a large
fraction of modes already at foundry Qi=2×10⁶ — under **either** criterion (its `Q_crossover` band, ≤1.1×10⁶,
stays below the foundry Qi).

## Recommendation (Executor → S0.3 / F19)

**Add an *optional* CW/CCW mode-splitting knob to the S0.3 substrate — gated by a process-roughness
flag, NOT strictly by Q.** Concretely: a 2×2 coupled-mode block per ring (degenerate CW/CCW pair with
coherent coupling `gamma`), default:

- **OFF** for the *clean foundry corner* (damascene-class, Qi≈2×10⁶) — single complex pole is defensible
  (`2γ/κ_i≈0.49`);
- **ON** for the *aspirational corner* (Qi≈3×10⁷, any process) and for *any rough/subtractive corner
  even at foundry Q*.

This matters because the bake-off's "one ring = one pole" assumption is **not unconditionally safe at
the registered foundry corner** if that corner is a rough subtractive process — it must be tied to a
fabrication assumption that PR-4 should make explicit. If S0.3 omits the knob, the substrate is only
valid for a *clean-process* foundry corner; say so.

## ⚠️ Verify-before-proposal caveats (flagged by the literature pull)

Before any of these go in the proposal (consistent with the proposal's "verify against primary sources"
discipline): (a) the **63 MHz** Pfeiffer figure and the **author lists of arXiv:2511.02198,
arXiv:1609.08699, arXiv:1205.4448** came partly via search-aggregation / PDF extraction — numbers and
titles look solid but confirm against the primary PDFs; (b) no published backscatter `gamma` was found
for the *specific* LIGENTEC AN800 or CORNERSTONE processes (closest SiN analogs are the table above; a
documented AN800 point is Qi=6.8×10⁶ at 0.051 dB/cm, no γ); (c) the `2γ vs κ_tot` crossover curve is
**assembled here** from bracketing SiN data points — no single published SiN crossover-Q curve exists.

## Full reference list

1. Kondratiev, Voloshin, … Kippenberg, Bilenko. *Nat. Commun.* **12**, 235 (2021). arXiv:1912.11303. DOI:10.1038/s41467-020-20196-y.
2. "Process-structure-property relationships in subtractive fabrication of Si₃N₄ microresonators." arXiv:2511.02198 (2025). ⚠️ verify authors.
3. Bauters/Gondarenko/…/Lipson. "Breaking the loss limitation of on-chip high-confinement resonators." arXiv:1609.08699 (2016)/CLEO 2017. ⚠️ verify authors/venue.
4. Pfeiffer, Liu, … Kippenberg. "Photonic Damascene process…" *IEEE JSTQE* 24, 6101411 (2018). ⚠️ verify the 63 MHz.
5. Jin, … Kippenberg. "Coherent suppression of backscattering in optical microresonators." *Light Sci. Appl.* **9**, 41 (2020). (silica — mechanism/mitigation.)
6. Li et al. "Backscattering in silicon microring resonators." *Laser Photon. Rev.* **10**, 420 (2016). (silicon — quantitative model.)
7. Zhu, Yang et al. "A unified approach to mode splitting and scattering loss in high-Q WGM microresonators." arXiv:1205.4448 (2012). ⚠️ verify authors.
8. "Methods to achieve ultra-high-Q Si₃N₄ resonators." *APL Photonics* **6**, 071101 (2021). (roughness/width dilution mitigation.)
