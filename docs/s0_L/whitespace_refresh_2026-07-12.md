# White-space refresh — 2026-07-12 (S0.8 assembly; pre-submission sweep #1)

> **⚠ SUPERSEDED IN PART (2026-07-27):** the Wu eLight disposition below ("inference-only,
> trains nothing") was REFUTED by the registered page-level read — the paper's ORNN chip is
> SPGD-trained in situ. W0 retracted; W1 stands. See `whitespace_page_reads_2026-07-27.md`.

**Author:** Supervisor (single-session mode — search executed by a delegated web agent under
the PR-15 qualifier frame; not independently reviewed; disclosed). **Refreshes:**
`debt1_whitespace_search.md` (PR-15, 2026-06-09) under the same three qualifiers: (i) on a
computational task; (ii) parameter/state physicality (recurrent state carried optically);
(iii) weight-tied recurrence across the input sequence. **Scope searched:** publications/posts
to July 2026, seven query families (log below).

**BOTTOM LINE: W1 survives cleanly; W0 survives with the three qualifiers visibly
load-bearing.** No work found that trains pole positions or inter-resonator couplings of a
continuous-time dissipative-resonator photonic recurrence on the physical device, by any
method. The CROW/coupled-ring literature contains no learned-coupling experiment at all; the
one in-class device (SCISSOR coupled spiking microrings, arXiv:2602.05918) trains nothing
on-device.

**Referee-likely items — cite and dispatch BY NAME in the §1 white-space paragraph:**
1. **Ashtiani, Idjadi, Kim, Nature 651, 927–932 (2026)** (arXiv:2506.14575) — on-chip
   backpropagation training, all-photonic forward+backward. **Feedforward** (qualifier iii).
   The highest-profile adjacent "first".
2. **Zhao et al., Laser Photon. Rev. (2025), 10.1002/lpor.202501576** — in-situ trained MRR
   networks via on-chip optical backprop. **Feedforward weight banks** (qualifier iii). The
   PR-15 open exposure — now RESOLVED: clears. Strengthens the framing (MRR parameters are
   in-situ-trainable; nobody has done it for a recurrence).
3. **Wu et al., eLight 5, 7 (2025)** — monolithic asynchronous optical recurrent accelerator.
   The PR-15 nearest neighbor — now RESOLVED: **inference only**, no training of any parameter;
   wavelength relay is O/E/O (differential PD → MRM). Clears W0 and W1.
4. **Time-synthetic ONN, arXiv:2507.02297** (coupled fiber loops, >30k effective gates,
   in-situ training) — strongest attack-in-letter on W0; clears on qualifier (iii): each time
   step applies *different* programmed parameters (time-unrolled feedforward, stated in-paper).
5. **Optoelectronic delay-RC in-situ optimization, ACS Photonics 2025** (arXiv:2502.11126) —
   optimizes recurrence-defining params (feedback gain, phase, delay) in situ, BUT by
   Bayesian/random search (not gradient-based/-estimating) and through a *digital* FPGA
   feedback loop (qualifier ii). Clears twice over.

**Also cleared (one line each):** Lugnan Adv. Sci. 2025 (PCM plasticity = unsupervised local
rule + digital readout); Xiang arXiv:2506.14272 (spiking, feedforward broadcast); SPIM-EP
arXiv:2606.13454 (digital relaxation loop); Wang eLight 5, 20 (2025) (RNN weights
offline-programmed); Bueno/Brunner Optica 2018 + Boolean-learning line (readout-only —
pre-registered pre-emption still accurate); arXiv:2506.18041, 2604.02429, 2507.05583 (all
feedforward); frequency-circuit PSO training (method + iii); OE-RNN arXiv:2411.16186
(simulation, O/E/O); HEB/RHEL/Lagrangian-EP (theory/simulation only).

**Pre-submission page-level reads registered (4):** Wu eLight full text (confirm no buried
training subsection); arXiv:2507.02297 (confirm per-step distinct weights); arXiv:2606.13454
(confirm digital relaxation loop); Zhao LPR supplement (confirm no recurrent variant).

**Wording note (binding):** W0's "gradient-based/-estimating" is doing real work against
Bayesian/PSO/plasticity-trained systems — do not soften during editing. W0-vs-W1 remains
**Lucas's ruling at S0.8 close**; this memo only refreshes the evidence under it.

---

## Search log (agent-reported, 7 families)

| # | Query family | Result |
|---|---|---|
| 1 | in-situ / on-chip / HIL training of photonic RNNs 2024–26 | Ashtiani 2026; arXiv 2506.18041; 2506.14272; Bueno 2018; PSO frequency circuits — all feedforward or readout-only |
| 2 | reservoirs with trained internal weights | field readout-only by construction; ACS Phot. 2025 in-situ optimization (digital loop, Bayesian); Lugnan plasticity |
| 3 | Wu eLight 2025 | resolved: inference accelerator, O/E/O relay, no training |
| 4 | Zhao LPR 2025 | resolved: feedforward MRR weight banks, optical backprop |
| 5 | trained coupled-ring / CROW couplings | nothing — no learned inter-resonator coupling experiment exists |
| 6 | Hamiltonian echo / EP on photonic hardware | HEB/RHEL/L-EP theory; SPIM-EP hybrid (digital loop) |
| 7 | "first" + training + photonic recurrent 2025–26 | Ashtiani (feedforward); photonic CNN SPSA (feedforward); time-synthetic ONN (time-unrolled) |
