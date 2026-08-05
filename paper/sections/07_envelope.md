# §7 — Does it pay? The systems envelope

**Status:** DRAFT v1 (2026-07-08, single-session mode — not independently reviewed; disclosed).
**Sources of record:** PR-10 🔒 (frozen corners + named F16 baselines; source memo
`docs/s0_7/pr10_assumption_sources.md`) · S0.7-lite (`docs/s0_7/s07_lite_envelope.md`,
`results/s0_7/`) with its Critic findings EV-F1/EV-F2 carried · S0.7-full-core
(`results/s0_7/training_envelope.{json,md}`, rules pre-registered) · S0.5 measured
passes-to-target. **Open flags:** [CITE-*] resolved via `paper/references.md` (EdgeDRNN
page-verified 2026-07-12); the four unbudgeted exclusions remain a named retrieval
(primary-sourced ledger, pre-submission); figure F7 = `paper/figures/F7_envelope.*`.

---

## 7.1 The question, and how we keep it honest

A photonic SSM only matters if, after paying the conversion toll — DAC and modulator in,
photodiode and ADC out, heaters held all the while — it still beats a competent digital
implementation on the axis the niche cares about. We price this at two frozen corners (OPT =
best published device class; CONS = named vendor parts at ENOB-at-speed, never nominal bits),
against named baselines (Microsoft Brainwave's author-stated batch-1 streaming efficiency; a
coherent-DSP ASIC class; Jetson AGX Orin), with every number traced to a frozen source row and
the four known exclusions (laser wall-plug, locking, control compute, packaging) explicitly
unbudgeted — they only shrink positive cells, so negative findings are robust to them. An
assembly-time retrieval bounds their magnitude from primary sources (supplementary ledger): the
integrated-class stack — hybrid-laser wall-plug 0.2–0.6 W at mW-class on-chip power, TEC hold
0.18 W, microcontroller-class control 0.13 W, FPGA-class locking up to ~10 W — totals of order
0.5–1 W, the *same order as the budgeted N = 128 photonic power itself* (~0.9 W at 2 GS/s).
Charging it would compress the positive cells' margin (§7.2) toward single digits, and a
benchtop realization (40–100 W laser and instrument lock) would erase the niche outright. The
niche verdict below therefore carries an integrated-realization condition on all four excluded
items, alongside the heater-class condition it already states.

## 7.2 Inference: a conditional niche, gated by the heater class

The lite envelope's verdict stands: **a plausible low-latency niche exists, conditionally.** At
the registered scale grid, the photonic side clears the strongest streaming baseline (Brainwave)
by up to ~15× in energy per sample at N = 128 and 2 GS/s, with end-to-end latency bounded at
tens of nanoseconds per sample against the baseline's milliseconds — but only when three
conditions hold simultaneously: line rates ≳0.5 GS/s (every scenario loses everything at
0.1 GS/s), N ≳ 32 (conversion is N-independent; digital cost scales with N — the structural
effect the architecture banks on), and **suspended low-power heaters** (~1 mW/π, class B).
One measured caveat now bounds the middle condition: at the headline cell the deployed
equalizer's *output* rides on $N_\text{eff} \approx 6$–$8$ of 32 rings (readout ablation on
the stored solutions, PR-18 §18.6b; head-refit recovers none of the zeroed readouts). The
digital baselines in this comparison are priced at the nominal N, but a baseline built to
the *function* would carry ~6–8 states and shrink its cost accordingly — so the N-scaling
premise holds only for workloads that actually exercise the state dimension, which the
7-tap equalization family does not. The niche verdict inherits that scope condition
(§8.5's narrow-task-family limit, here quantified), and a task engineered to *need* N
states — the registered long-coherent-memory residue — is what would discharge it. Under
the registered worst-case holding convention the foundry-standard heater class loses to every
baseline everywhere in the window at the deployable corner; the demonstrated-foundry path
therefore does not reach the energy niche as computed — a Stage-1 platform constraint stated as
such, with the expected-value-holding sensitivity (under which the optimistic corner clears
in-window) reported alongside per the review finding. Jetson's *peak* rating is never beaten
anywhere; the niche claim rests on measured sustained behavior, for which batch-1 recurrent
workloads on edge GPUs are documented at >100× below claimed peak — page-verified: measured
batch-1 GRU throughput of 1.9 and 3.5 GOp/s against claimed peaks of 0.5 and 0.8 TOp/s on the
two Jetson-class devices (ratios ≈263× and ≈229×), with the source's own conclusion stating
"a factor of over 100X" [CITE-EdgeDRNN]; the Orin DLA path falls back to GPU for recurrent
layers. One boundary cell (the DSP-class
comparison at N = 32) clears by ~1% and is treated as a tie.

## 7.3 Training: the energy metric inverts the sample-efficiency ranking

The bake-off's primary metric (§5) counts device passes, under a registered principle that the
digital side-ledger is always co-reported and never merged. The envelope is where that principle
pays off, because converting both ledgers to joules **inverts the ranking**. Training to the
pre-registered target at the headline cell costs, at the optimistic corner:

| route | conversion energy | digital compute | total |
|---|---|---|---|
| PAT | 0.57 mJ | **≈13–44 J** (twin ledger, 1.3×10¹³ FLOP at named accelerator classes) | ≈13–44 J |
| adjoint | 1.1 mJ | 0 | 1.1 mJ (†realizability) |
| **SPSA** | **2.6 mJ** | 0 | **2.6 mJ** |

PAT reaches target in the fewest device passes but its digital twin bill exceeds SPSA's *entire
training energy* by roughly four orders of magnitude — and our FLOP estimate is charitable to
PAT (real accelerator utilization on a 64-dimensional complex recurrence sits far below peak).
The nominal winner of this table is the adjoint (1.1 mJ) — but its row is charged as-if-realizable
(§5.3), so among demonstrated routes the energy story is SPSA's: no model, no twin, no added
hardware, the physical recurrence trained to target for **about 2.6 millijoules in the budgeted
conversion stack** at the optimistic corner (99 mJ at the vendor-part corner). Scope, so no one
has to derive it: the §7.1 exclusions are per-time holds, and SPSA's 176,000 passes occupy
22.5 ms of wall time — class-B heater hold adds ≈4 mJ and an integrated-class laser ≈5–14 mJ —
so the honest figure is *tens of millijoules, not single digits*; the four-orders inversion
against PAT's 13–44 J is insensitive to this, and a benchtop laser would break the training-energy
claim exactly as it breaks the inference niche (§7.1).
RHEL's echo, censored on accuracy grounds anyway, is also energy-dominated by its own conjugator
pump (×42 its conversion stack per update). For Stage 1 this sharpens §9's ordering: SPSA is not
merely the simplest route but by far the cheapest to *run as training*, and PAT's role is best
cast as the high-device-throughput option for settings where digital compute is free and device
time is scarce — which is a real regime (a shared testbed), but a different claim than
"efficient."

## 7.4 The advantage question, answered as far as the data allows

Assembling §5.5, §6, and this section: the *demonstration* is in-data; the *advantage* is
conditional and partly open. In-situ training buys nothing over calibrate-then-deploy at
5%-class calibration accuracy (§5.5) — and much of what training achieves on this task is
finding the damping operating point, which a well-calibrated offline model also finds (§6). The
inference-mode niche exists but is gated by a heater class the named foundry flow does not
supply, and rests on sustained-vs-peak baseline conventions we document rather than hide. What
survives all of it: a recurrent photonic SSM at GS/s line rates with class-B actuation is
energy-competitive at scale for streaming workloads, can be *trained through its own physics for
tens of millijoules* when calibration is unavailable or stale, and offers latency headroom no digital
baseline in our set approaches. Whether the conjunction of those conditions describes a market
or only an experiment is a Stage-1 question, and §9 designs the experiment to answer it.
