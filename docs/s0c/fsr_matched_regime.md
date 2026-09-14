# Stage 0c proposal memo — the FSR-matched regime (2026-09-14, Supervisor; single-session mode)

**Status: PROPOSED, €0 spent, nothing registered yet.** This memo records (i) a correction to how
Stage 0b bounded what a ring lattice can emulate, (ii) what the athermal literature offers, (iii) the
regime the correction points at, with its arithmetic and its nearest published neighbor, and (iv) what a
Stage 0c would register and cost. Retrieval statuses follow the exclusions-ledger convention.

## 1. The correction (PR-20b, ledger §20.7)
PR-20 §20.4 bounded reachable taps by single-ring memory × line rate. For a broadband input that is
wrong in the photonic side's favour: an N-state LTI filter's impulse response is a sum of N complex
exponentials, so it matches at most ≈ N degrees of freedom of a FIR, at any rate. The S0b.0 kill is
therefore *more* robust, the "f_s² lever" is withdrawn (linear at fixed N at best), and the only route
to "N states ≈ more than N taps" is the IIR-vs-FIR efficiency of all-pass structures on smooth channel
responses — chromatic dispersion — which is a known device class, not a hope.

## 2. Athermal SiN rings (door 1) — what exists
| number | source | status |
|---|---|---|
| Hybrid TiO₂–Si₃N₄ ring, "athermal and high-Q": **0.14 pm/°C** (25–60 °C); another hybrid **~0.1 pm/K** | Qiu et al., ACS Photonics 2(5), 405 (2015), 10.1021/ph500450n (page 403 this session) | UNVERIFIED-direct |
| TiO₂-clad SiNₓ ring **0.073 pm/°C** | search snippet (thesis/ResearchGate) | UNVERIFIED-direct |
| Polymer (PMMA)-clad SiN ring **< 2.0 ± 0.1 pm/K** over 15–70 °C; geometry-tailored athermal point **−1.2 … +2.0 pm/K** with a nonlinear (second-order) residual | Photonics 13(4), 371 (2026), MDPI (page 403) | UNVERIFIED-direct |
| Polymer-clad SiN ring **0.018 pm/°C**; **0.5 pm/°C over 40 °C** | conference reports (2014-era), ResearchGate | UNVERIFIED-direct |
| Near-athermal SiN O-band demux **~2 pm/K** by geometry alone | PubMed 42295907 (2026) | UNVERIFIED-direct |
| Physics tension: overlay athermalization needs cladding overlap; class-leading SiN Q (thick, confined cores) has little. Q of the athermal hybrids not read this session. | — | open |

Reading: 0.1–2 pm/K is 7–140× below the registry's 14 pm/K. At the high-Q substrate (C-2 linewidth
14 MHz) that is still only 0.06–1 K per linewidth — it helps, it does not remove the hold term. At the
low-Q regime below it removes it.

## 3. The regime the correction points at: FSR-matched low-Q ring lattice
The registered ring geometry (FSR 100 GHz, R ≈ 242 µm) has a round trip of 10 ps — one symbol at
100 GBd, 0.64 at 64 GBd. Operated with **power coupling K = 5–20 %** instead of the registered
r = κ_ext/κ_i ≤ 3, the ring is a discrete-time first-order IIR section whose pole magnitude per round
trip is set by the coupler, not the loss:

| K | |λ| per round trip | memory (samples) | linewidth | K per linewidth at 14 pm/K |
|---|---|---|---|---|
| 5 % | 0.975 | 39 | 0.5 GHz | 0.29 K |
| 10 % | 0.949 | 19 | 1.0 GHz | 0.60 K |
| 20 % | 0.894 | 9 | 2.1 GHz | 1.2 K |

(intrinsic transmission per round trip at C-2 = 0.9991, i.e. loss is negligible next to coupling — the
"damping = coupling" knob of §6 exactly, with the box extended two orders of magnitude). Thermal hold
relaxes **40–150×** versus the high-Q regime (8 mK per linewidth → 0.3–1.2 K); with an athermal overlay
it becomes tens of K, i.e. **no hold at all** inside a module. This is the classical optical all-pass /
lattice equalizer regime (Lenz & Madsen, JLT 17(7) 1248 (1999); Madsen et al., OL 24(22) 1555 (1999);
PTL 11(12) 1623 (1999) — UNVERIFIED-direct, citations from search).

**The workload** (arithmetic, D = 17 ps/nm/km, 1550 nm): dispersion memory in symbols =
6 / 11 / 17 / 70 / 139 at 32 GBd for 40 / 80 / 120 / 500 / 1000 km; 22 / 45 / 67 / 279 / 558 at 64 GBd.
So the ≥ 64-tap equalizer that S0b.0 needed exists at 64 GBd beyond ≈ 120 km, and the 8–32-tap one at
40–80 km — where the coherent DSP's CD block is a real power item.

## 4. The nearest published neighbor (found this session; VERIFIED, PMC full text)
Liu, Zhang, Liu et al. (SJTU), *Nat. Commun.* 15 (2024), PMC11058204: a silicon **cascade of 8
identical MRRs, FSR ≈ 99.5 GHz**, each with a **thermal heater on the resonance and an MZI tunable
coupler on the coupling** — the same actuation set as this program's substrate — compensating
**−682.9 ps/nm (40 km SMF) over 32 GHz**, 50 GHz bandwidth for 20 km; 15 × 112 Gbit/s DMT = 1.68
Tbit/s over 20 km; **insertion loss ≈ 14.8 dB** (silicon, so an EDFA is charged); energy **≈ 0.3 pJ/bit
including the EDFA**, against 400G-ZR at ≈ 5 pJ/bit of which ≈ 12.5 % (≈ 0.6 pJ/bit) is CD compensation
— a **≈ 2× edge, statically configured**. Implications:
- The device class is real and the *static* energy question is already answered at ≈ 2×, below this
  program's 3× bar, on silicon, with the loss paid by an amplifier.
- **On SiN the loss term collapses** (0.051 dB/cm vs ~2 dB/cm: 8 rings × 2.4 mm at 10 % coupling ≈ a
  fraction of a dB), so the EDFA goes away and the energy is heaters only: class B, 8 rings × 2 ch ×
  3 mW = 48 mW at 112 Gb/s ⇒ **≈ 0.4 pJ/bit** (0.14 at 1 mW/π heaters without trim) vs 0.6 ⇒ 1.5–4×;
  class A foundry heaters (60–175 mW/π, full-π tuning needed at low Q) ⇒ 9–25 pJ/bit ⇒ loses outright.
  Same heater-class condition as P1 §7.2, unchanged.
- **8 rings ≈ 30 FIR taps** on that channel (272 ps spread at 50 GBd ≈ 14 symbols; a FIR needs ≈ 2×):
  the IIR efficiency is ≈ 4 taps per ring for CD. Against a 32-tap digital block at 0.05–0.15 pJ/tap
  (1.6–4.8 pJ/sample) the class-B SiN lattice at 0.75–1.5 pJ/sample sits at **2.1–3.2×** — at the bar.
- **What no one has done, pending a PR-15-style sweep:** *train* such a lattice in situ by gradient
  estimation (PAT/SPSA on δ + coupler), i.e. the program's W1 claim in the regime where the product
  neighbor lives. Nearest misses seen this session: MRR weight-bank zeroth-order on-chip training
  (feedforward weights, not a recurrence) and model-free in-situ RL of optical processors (LSA 2025,
  device not read). The SJTU CDC is configured, not trained.

## 5. What Stage 0c would be (all registered before any run)
- **S0c.0 (€0):** (a) the FSR-matched mapping memo — the discrete-time pole/coupler relation replaces
  the CMT ODE above K ≈ 10 % (temporal coupled-mode theory is marginal there; the delay-line ring model
  is a few lines and *is* the diagonal SSM recurrence); (b) a PR-15-style white-space sweep for "in-situ
  gradient-estimating training of a ring-lattice equalizer"; (c) PR-22: an envelope at 32–112 GBd with
  the SJTU device as the anchored neighbor row, SiN loss, class A/B/piezo actuation, athermal-overlay
  drift rows, the order bound N_reach ≤ N·η_IIR with η measured from the neighbor (≈ 4), and the same
  3× / CONS verdict rule. Kill if no class-B or piezo cell clears 3× at CONS.
- **S0c.1 (≈ €50–100, only if S0c.0 survives):** in-situ training bake-off (PAT, SPSA; BPTT ceiling) of
  an 8–16-ring FSR-matched lattice on a dispersive channel at 64 GBd against a FIR baseline of matched
  SER — the trainability question in the new regime, and the first datum on η_IIR under training.
- **Honest prior:** the window is thin (2–3× at class B, at the bar), the neighbor already holds the
  static 2×, and the heater-class condition is the same one P1 could not discharge. What is new and
  defensible is the *science*: the W1 claim in a regime that has a product neighbor and no thermal
  wall. That is a better Stage 1 pitch than the high-Q substrate ever was.

## 6. P1 consequence
§7.4's "quadratic only while usable tap count grows" is superseded by the order bound (linear at fixed
N). The current text is hedged and not wrong; the sharper sentence goes into arXiv **v2** with any
Stage-0c result, not into the v1 package now in submission.
