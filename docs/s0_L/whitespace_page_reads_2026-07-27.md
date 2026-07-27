# White-space page-level reads + fresh sweep — 2026-07-27 (pre-submission round #2)

**Author:** Supervisor (single-session mode; two delegated web agents — one executing the 4
registered page-level reads, one sweeping June–July 2026; not independently reviewed;
disclosed). **Supersedes** the Wu/Zhao dispositions of `whitespace_refresh_2026-07-12.md`
where they conflict (Wu: REFUTED — see below).

## BOTTOM LINE

**W1 survives both reports cleanly. W0 is REFUTED at page level and has been retracted** (scope
re-ruled W1-only, 2026-07-27, under the standing PI delegation of 2026-07-26; supersedes the
one-day-old W0-in-prose ruling — retreat cost as designed by the June freeze-low-reclaim-high
logic: one paragraph, pre-publication, zero external exposure).

## The four registered page-level reads

1. **Wu et al., eLight 5, 7 (2025) — prior clearance REFUTED.** Full text + SI obtained. The
   paper contains TWO chips; the June/July "inference-only, trains nothing" disposition
   described only the OHMM chip. The **ORNN chip is trained in situ** — §2.3: entropy loss
   "minimized in-situ using a stochastic parallel gradient descent algorithm" (Methods 5.1:
   U±δ two-evaluation perturbation + Adam — SPSA-family, unambiguously gradient-estimating) on
   Japanese-vowels classification (97%/95% train/test; 8-class 87.7%). The recurrence is
   weight-tied (one physical incoherent MZI mesh W applied across wavelength-encoded time
   steps, Eq. 6), and the state relay is *analog* O/E/O (PD sum → MRM drive; no digitization
   inside the 4-step loop) — so the "carried digitally" exclusion does not catch it.
   **Consequence: W0's broad form ("no physical photonic system of any architecture…") is
   attacked under the natural reading** (the paper never enumerates the trained voltage set U,
   but nothing restricts it away from the recurrent mesh; resolvable only by author query).
   **W1 is untouched:** the trained parameters are mesh-weight voltages, not resonator
   poles/couplings; the MRRs are calibrated once and held static (SI S10); the system is
   discrete-time with electronic state regeneration, not a continuous-time dissipative-resonator
   recurrence. §1.1 now cites Wu loudly as *the nearest neighbor — the first in-situ-trained
   optical recurrent network of any kind* — exactly the posture the June wording memo
   pre-planned for this outcome.
2. **Zhao et al., LPR 10.1002/lpor.202501576 — CLEARS (partial access).** Abstract +
   **full SI** verified (no preprint exists; main body paywalled). SI keyword scan: recurrent
   / RNN / feedback / reservoir / temporal all = 0; content is MZI signal loading, 4×4 MRR
   weight bank, feedforward CNN. Residual risk (main-text-only recurrent variant) very low,
   registered. **Watch item:** same HUST group as Wu (shared authors Wu/Zhou/Dong/Zhang) —
   a Zhao(optical-BP)×Wu(ORNN) merge would attack head-on; monitor at final refresh.
3. **arXiv:2507.02297 — CLEARS on qualifier (iii), verbatim.** Full PDF read: β(m,n), G(m,n),
   φ(m,n) indexed by time layer n; product of distinct W^(n); "each time gate" modulated to
   realize arbitrary N×N transforms; no tied-weight experiment anywhere (MNIST/CIFAR/matrix
   fidelity all per-layer-distinct). **Citation note: paper retitled** "Time-synthetic optical
   neural networks with stable programmable gain" (Wu, Ren et al., Zhejiang U.). Secondary:
   its in-situ loop is digital (DSO→GPU→AWG).
4. **arXiv:2606.13454 (SPIM-EP) — CLEARS on qualifier (ii).** "Hybrid optical-digital"
   (abstract, direct); state stored digitally and re-encoded on the SLM every relaxation
   iteration; gradients assembled digitally (one term evaluated digitally outright); updates
   via SGD/Adam. The recurrent/relaxation state never persists physically.

## Fresh sweep (June–July 2026; ~20 searches, 15 page-level fetches, 8 query families)

**No new attack.** Coverage caveat: deepest new items are June 2026 (arXiv 2606.x, APL Phot.
11(6), Q.ANT ISC 2026-06-23); no 2607.x photonic-training item indexed yet — July is "nothing
indexed," not "nothing exists"; final refresh at submission stands. ~30 items screened (table
in the agent report, this memo records the near-misses):

- **Zhang et al., eLight 6, 6 (2026) (arXiv:2505.11369, Princeton/Prucnal+Shastri) — THE new
  nearest miss; added to §1.1 by-name dispatch + registered page-level read.**
  Modulation-and-weighting 10-MRR array with a genuine analog recurrent mode (MRR weights
  inside the PD→delay→re-modulation feedback path) and **in-situ on-device training of all ten
  ring currents — by particle-swarm optimization, explicitly "without requiring gradient
  calculations."** Clears **solely on the excluded-method boundary** (same thinnest boundary
  as Bueno/Brunner). Registered read: confirm no SPSA/gradient variant anywhere (incl. drift
  compensation) and whether in-situ PSO ran in the recurrent-mode demo.
- **Ghent/imec spatial reservoir equalizer, Nat. Photonics 2026 (arXiv:2503.19911)** — abstract
  says "recurrent … trained in hardware"; page-level: readout-only (8-MZI readout, CMA-ES),
  internal couplings fixed by fabrication. Clears doubly; dispatched by name in §1.1 because
  the abstract phrase is referee-bait.
- **Xiang et al., Optica 13, 457 (2026)** — published version of cleared 2506.14272
  (feedforward mesh + spiking lasers, hw-sw collaborative RL); cite the Optica version.
- Q.ANT xLSTM/TiRex NPU demo (inference-only); EP-CIM 2606.09117 (simulation, digital updates,
  static EBM); self-pulsing MRR reservoirs (readout-only); frequency-circuit PSO (feedforward +
  excluded method); others — all clear (screening table in agent report).
- **Standing negatives re-confirmed:** no RHEL/HEB photonic-hardware demo; no recurrent
  extension of Ashtiani on-chip backprop; **no competing photonic-SSM paper.**

## Actions taken (same day)

§1.1 rewritten (Wu = nearest-neighbor treatment; Zhang + Ghent-RC added to dispatch; broad-W0
paragraph removed); abstract first sentence re-scoped to W1; §5.5 demonstration-claim wording
re-scoped; references.md updated (Wu note refuted→nearest-neighbor; new keys
CITE-Zhang-eLight-2026, CITE-spatial-RC; time-synthetic retitle). **Registered pre-submission
reads now: Zhang eLight 6:6 (new) + final sweep re-run + UNVERIFIED-direct rows of the S0.7
exclusions ledger.** E-2026-07-27-1 records the scope re-ruling for Lucas.
