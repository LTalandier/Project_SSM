# S0c.0-b — White-space sweep in the FSR-matched regime (2026-09-15; PR-15 qualifiers applied verbatim)

> **2026-09-19 audit:** Historical memo retained. Its current interpretation is superseded by
> `docs/s0c/audit_2026-09-19.md` (arithmetic, mapping, budget, and prior-art corrections).

**Claim under test (W1, unchanged wording):** recurrent parameters of a dissipative-resonator
photonic system — poles and inter-ring couplings that define the recurrence — updated **on the
physical device** by **gradient-based or gradient-estimating training on a task loss**. The registered
qualifiers (`docs/s0_L/whitespace_claim_wording.md`): parameter-physicality (readout-only training
clears), recurrence (feedforward weight banks clear), and **q4 — the servo/calibration lineage:
filter synthesis toward a *target response* is not task training** (Mak/Poon 2015 already sits on that
boundary in the P1 sweep and is cited as lineage).

**Question for S0c:** does anything in the low-Q ring-lattice / all-pass-equalizer literature attack W1
in this regime? Four searches, seven candidates read at abstract level (two publisher pages 403).

| candidate | what it is | disposition under the qualifiers | status |
|---|---|---|---|
| Liu, Zhang, Liu et al. (SJTU), Nat. Commun. 15 (2024), PMC11058204 | 8-ring Si all-pass CDC, heater + MZI coupler per ring; configured to a target dispersion | **Clears (q4):** configured, not trained on a task loss; no on-device gradient/estimator loop reported. **Cite loudly as the product-class neighbor.** | VERIFIED (full text) |
| Mak, Sacher, …, Poon, arXiv:1507.02129 / IEEE JQE (2015) | 5th-order series-coupled ring filter; feedback on a reference wavelength to center the passband and reduce ripple | Clears (q4) — already dispatched in P1 | VERIFIED (abstract) |
| Shawon & Saxena, arXiv:2205.12048 (2022) | fully automatic in-situ reconfiguration of a 2nd-order RF photonic ring filter to a user-specified response (Butterworth/Chebyshev), two reference wavelengths, PVT compensation | Clears (q4): target-response synthesis; algorithm not stated in abstract | VERIFIED (abstract) |
| "Automated control algorithms for optical all-pass filter on SOI", Opt. Laser Technol. (2025), S003040182500834X | two-stage global + local optimization drives an MRR all-pass filter to the all-pass state in 13 iterations; 0.259 dB ripple | Clears (q4): objective = all-pass flatness, not a task loss; **page read registered** (403 this session) | UNVERIFIED-direct |
| Shi et al., Laser Photonics Rev. (2025), 10.1002/lpor.202501962 | "intelligent configuration" of an integrated microwave photonic filter with self-stabilization and "channel equalization" | **Borderline wording** ("channel equalization" as a filter property): likely q4, but the algorithm and objective must be read; **page read registered** (403 this session) | UNVERIFIED-direct |
| Van Assche, …, Bienstman, arXiv:2503.19911 (2025) | silicon photonic reservoir + programmable readout, real-time equalization of 28 Gb/s OOK over fibre incl. nonlinear regime | Clears (physicality: readout-trained reservoir; recurrence fixed) — **the nearest equalization neighbor; cite** | VERIFIED (abstract) |
| Zhao et al., "In-situ trained microring-based neural networks…", Laser Photonics Rev. (2026), 10.1002/lpor.202501576 | in-situ trained MRR-based NN | Expected to clear (feedforward weight bank) — **page read registered** (403 this session) | UNVERIFIED-direct |
| CLEO 2018 JTh3D.4 "Automated initialization of reconfigurable SiNₓ filters" | feed-forward + iterative feedback on high-order all-pass structures in SiN | Clears (q4); SiN all-pass lattice lineage | UNVERIFIED-direct |

**Verdict:** no attack on W1 found in this regime at the abstract level. Three items are the direct
lineage that a Stage-0c paper must cite in its first paragraph (SJTU 2024; Mak 2015; the 2025 APF
control paper), one is the nearest equalization neighbor (Van Assche 2025, reservoir), and **two page
reads are registered before any S0c claim is written** (Shi 2025; Zhao 2026). The S0c claim, if it is
ever made, is the W1 sentence with "in the FSR-matched regime that has a product-class neighbor" as a
scope note, not a new claim.

**Also noted (not W1-relevant, useful for PR-22):** the 2025 APF-control paper's "13 iterations to
the all-pass state" and its stage-II "maintain long-term stable operation against external
perturbations" are exactly the maintenance loop S0b.3 would have priced — a source for the tracked-lock
duty row once read.
