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
the five known exclusions (laser wall-plug, the substrate's Er:Si₃N₄ gain pump, locking, control compute, packaging) explicitly
unbudgeted — they only shrink positive cells, so negative findings are robust to them. An
assembly-time retrieval bounds their magnitude from primary sources (supplementary ledger): the
integrated-class stack — hybrid-laser wall-plug 0.2–0.6 W at mW-class on-chip power, TEC hold
0.18 W, microcontroller-class control 0.13 W, FPGA-class locking up to ~10 W — totals of order
0.5–1 W, the *same order as the budgeted N = 128 photonic power itself* (~0.9 W at 2 GS/s).
The fifth item — the 1480/980 nm pump the substrate's g = 0.9 κᵢ erbium stage needs at every
ring — was missing from the original list and was added at the Stage-0b re-envelope (supplementary
ledger; 0.8–17 mW electrical per ring near transparency, derived): 26–550 mW at N = 32, the same
order again, and larger at N = 128.
Charging it would compress the positive cells' margin (§7.2) toward single digits, and a
benchtop realization (40–100 W laser and instrument lock) would erase the niche outright. The
niche verdict below therefore carries an integrated-realization condition on all five excluded
items, alongside the heater-class condition it already states.

## 7.2 Inference: a conditional niche, gated by the heater class

The original lite envelope suggested **a conditional low-latency niche**. The later
function-matched inline follow-up (§7.4) closes the registered product window; the
original calculation is reported below for provenance. At
the registered scale grid, the photonic side clears the strongest streaming baseline (Brainwave)
by up to ~15× in energy per sample at N = 128 and 2 GS/s, with an optical latency lower-bound estimate of
tens of nanoseconds per sample, compared with the baseline's reported milliseconds;
this is not a measured end-to-end latency advantage — but only when three
conditions hold simultaneously: line rates ≳0.5 GS/s (every scenario loses everything at
0.1 GS/s), N ≳ 32 (conversion is N-independent; digital cost scales with N — the structural
effect the architecture banks on), and **suspended low-power heaters** (~1 mW/π, class B).
One measured caveat now bounds the middle condition: at the headline cell the deployed
equalizer's *output* rides on $N_\text{eff} \approx 6$–$8$ of 32 rings (readout ablation on
the stored solutions, PR-18 §18.6b; head-refit recovers none of the zeroed readouts). The
digital baselines in this comparison are priced at the nominal N, but a baseline built to
the *function* would carry ~6–8 states and shrink its cost accordingly — so the N-scaling
premise holds only for workloads that actually exercise the state dimension, which the
7-tap equalization family does not. The registered long-coherent-memory follow-up
(PR-19: unipolar despread-31, run to discharge exactly this condition) did **not**
discharge it — and produced no second measurement of concentration either. At the frozen
28 dB the task's ~16-chip integration gain leaves the entire damping grid error-free
(ledger §19.6a/b), and on a task solved with that much margin the readout-ablation count
measures the margin, not the substrate's utilization: the recorded $N_\text{eff} = 4$
(every seed; a head-refit recovers the target from as few as 3 rings, where on the
equalization task the same refit recovers nothing) is a statement about task slack,
uninformative about concentration in either direction. (The pre-written no-rise text,
drafted for an informative null, asserted the concentration reading; it is withdrawn by
ledger amendment §19.6c.) PR-19 therefore leaves the premise exactly where §18.6b put
it — the one informative $N_\text{eff}$ measurement in this program is the 6–8 above.
The ~15× at N = 128 was computed against a baseline priced at nominal N; a baseline
built to the function would shrink by roughly the same factor — **the advantage is
unmeasured in magnitude, not merely conditional** — and the burden has flipped:
demonstrating a workload that genuinely exercises N ≳ 32 states on this substrate (e.g.
the same family at a registered harder operating point) is what would restore the
premise, and no such demonstration exists in this program's data. Under
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

## 7.3 Training: partial energy budgets, unresolved wall-clock cost

The device-pass and digital ledgers yield the following component estimates at the
optimistic corner. These are not total training energies.

| route | conversion energy | digital-twin compute estimate |
|---|---|---|
| PAT | 0.57 mJ | ≈13–44 J |
| adjoint | 1.1 mJ | 0 in the idealized physical-adjoint ledger |
| SPSA | 2.6 mJ | no digital twin |

PAT's digital estimate uses the registered FLOP model and named accelerator-efficiency
classes; it is not a measured implementation. The physical-adjoint row remains conditional
on realizing the reverse pass. SPSA's vendor-part conversion estimate is 99 mJ.

SPSA's 176,000 passes, each containing 256 samples at 2 GS/s, occupy **22.528 ms
of optical sequence time**. This is a lower bound on training duration, not elapsed
wall time. The earlier wording treated it as wall time and inferred a total of tens
of millijoules; that total-energy claim is withdrawn (supplementary N8).
A complete estimate must include parameter writes and actuator settling between
perturbations, measurement and controller latency, reset gaps, and the laser, gain-pump,
locking, packaging, and thermal-hold power over the full duration. In symbols,
$E_{\rm train}=E_{\rm conversion}+E_{\rm digital}+E_{\rm writes}
+\int_0^{t_{\rm wall}}P_{\rm hold}(t)\,dt$, without double-counting components.
Those timing and write-energy quantities have not been established for a device.

The component ledger makes PAT's digital-twin cost visible and motivates measuring
SPSA's full hardware loop. It does not establish a four-orders-of-magnitude advantage
in total training energy. RHEL's registered pump adder is likewise a component estimate;
its accuracy censoring is unchanged.

## 7.4 Registered inline follow-up: no energy-advantage window

The later Stage 0b envelope (PR-20, frozen at `ee137c4` before calculation;
results `8931d6c`) replaces the block-level comparison with the per-tap digital
equalizer an inline device would replace. It charges the registered actuator,
common-mode thermal-management, gain-pump, and maintenance rows. This is a
calculated model envelope, not measured hardware performance.

Across the registered 0.1–2 GS/s grid, the best optimistic class-C cell has
$E_{\rm digital}/E_{\rm photonic}=0.64$: 3.2 pJ/sample digital versus approximately
5.0 pJ/sample photonic at 2 GS/s, 64 taps, passive C-3, and 10 mW global thermal
hold. Thus the photonic estimate is **1.56 times the digital energy**, missing
both parity and the registered 3-times advantage threshold. Removing the unsourced
optimistic rows lowers the best ratio to 0.23 (about 4.35 times the digital energy).
The conservative product-window maximum is 0.38. The PR-20 kill gate fires;
S0b.1–S0b.3 were not run, and no new simulation or fabrication spend followed.
The full ledger and results accompany the paper in `docs/s0b/` and `results/s0b_0/`.

Thermal management dominates the most favorable cell even with zero actuator hold.
The frozen minimum-damping model gives a pumped-to-passive memory ratio of
$(1+2r_{\min})/(0.1+2r_{\min})=3.14$ at $r_{\min}=0.1606$; removing gain does
not give a tenfold reduction at this operating point. These corrections change
interpretation, not the frozen arithmetic or gate.

The maintenance term inherits §7.3's optical-time lower bound. Accounting for
longer control and settling time can only increase modeled photonic energy at a
fixed retraining cadence, so it cannot reverse this negative gate. It does mean
that the calculation has not established that practical retraining is cheap or
that the chosen cadence maintains accuracy.

For fixed power and fixed workload tap count the energy ratio grows linearly with
sample rate. Quadratic scaling is an approximation only while usable tap count
also grows proportionally with rate; finite tap-grid limits and task capacity
interrupt that scaling. Higher-rate scenarios are outside PR-20 and have no
trainability result. They remain dormant pending a concrete workload and collaborator.

The earlier §7.2 nominal-dimension envelope is retained as the historical calculation.
This function-matched follow-up supersedes its positive product interpretation
within the registered inline window. The simulation trainability result survives;
energy-competitive hardware has not been demonstrated.
