# §7 — Does it pay? The systems envelope

**Status:** v2, condensed 2026-09-29 for the first public deposit (v1 at commit `a508a28`).
Exclusion magnitudes, baseline detail and the PR-20 provenance moved to supplementary N9.7.

---

## 7.1 The question, and its exclusions

A photonic SSM matters only if, after paying the conversion toll — DAC and modulator in,
photodiode and ADC out, heaters held throughout — it still beats a competent digital
implementation on the axis the niche cares about. We priced this at two frozen corners (OPT = best
published device class; CONS = named vendor parts at ENOB-at-speed, never nominal bits) against
named baselines (Microsoft Brainwave's author-stated batch-1 streaming efficiency, a coherent-DSP
ASIC class, Jetson AGX Orin), with every number traced to a frozen source row. Five known costs
are excluded: laser wall-plug, the substrate's Er:Si₃N₄ gain pump, locking, control compute and
packaging. They only shrink positive cells, so negative findings are robust to them. A
primary-source retrieval puts the integrated-class stack at 0.5–1 W, the same order as the budgeted
N = 128 photonic power (~0.9 W at 2 GS/s), and the erbium pump adds 26–550 mW at N = 32 (derived;
N9.7). A benchtop realization, with 40–100 W of laser and instrument lock, would erase any niche,
so every positive statement below carries an integrated-realization condition.

## 7.2 Inference: the original block-level envelope

The original envelope suggested a conditional low-latency niche: up to ~15× lower energy per
sample than the strongest streaming baseline (Brainwave) at N = 128 and 2 GS/s, with an optical
latency lower bound of tens of nanoseconds per sample against the baseline's reported
milliseconds. That was an estimate, not a measured end-to-end advantage, and it required three
conditions at once: line rates ≳0.5 GS/s (every scenario loses at 0.1 GS/s), N ≳ 32, and suspended
low-power heaters (~1 mW/π, class B). Under the registered worst-case holding convention,
foundry-standard heaters lose to every baseline everywhere in the window at the deployable corner.
Measurement has since undercut the N condition: the deployed equalizer's output rides on
$N_\text{eff} \approx 6$–$8$ of 32 rings (§5.7), so a baseline built to the *function* would carry
~6–8 states. The ~15× was computed against a baseline priced at nominal N, and a baseline built
to the function would shrink by a comparable factor. **The advantage is therefore unmeasured
in magnitude, not merely conditional.** Restoring it needs a workload that exercises N ≳ 32 states
on this substrate, and no such workload exists in our data; the registered long-memory follow-up
(PR-19) could not measure concentration at its degenerate operating point (N9.7). Jetson's peak
rating is never beaten anywhere; the comparison rests on sustained batch-1 behavior, which for
recurrent workloads on edge GPUs is documented at more than 100× below claimed peak
[CITE-EdgeDRNN]. The function-matched follow-up of §7.4 supersedes this block-level reading.

## 7.3 Training: partial energy budgets, unresolved wall-clock cost

The device-pass and digital ledgers yield component estimates at the optimistic corner. These are
not total training energies.

| route | conversion energy | digital-twin compute estimate |
|---|---|---|
| PAT | 0.57 mJ | ≈13–44 J |
| adjoint | 1.1 mJ | 0 in the idealized physical-adjoint ledger |
| SPSA | 2.6 mJ | no digital twin |

PAT's digital estimate uses the registered FLOP model and named accelerator-efficiency classes, not
a measured implementation; the adjoint row is conditional on realizing the reverse pass; SPSA's
vendor-part conversion estimate is 99 mJ. SPSA's 176,000 passes, each of 256 samples at 2 GS/s,
occupy **22.528 ms of optical sequence time**, a lower bound on training duration and not elapsed
wall time. A total estimate must add parameter writes, actuator settling, measurement and
controller latency, reset gaps, and the laser, gain-pump, locking, packaging and thermal-hold power
over the full duration,
$E_{\rm train}=E_{\rm conversion}+E_{\rm digital}+E_{\rm writes}
+\int_0^{t_{\rm wall}}P_{\rm hold}(t)\,dt$. Those quantities have not been established for any
device, so no total-training-energy ranking is claimed; an earlier total-energy claim is withdrawn
(supplementary N8).

## 7.4 Registered inline follow-up: no energy-advantage window

A follow-up envelope (PR-20, frozen before calculation) replaces the block-level comparison with
the per-tap digital equalizer an inline device would replace, and charges actuator, common-mode
thermal-management, gain-pump and maintenance rows. It is a calculated model envelope, not measured
hardware performance. Across the registered 0.1–2 GS/s grid, the best optimistic cell gives
$E_{\rm digital}/E_{\rm photonic}=0.64$: 3.2 pJ/sample digital against ≈5.0 pJ/sample photonic at
2 GS/s, 64 taps, passive C-3 and 10 mW of global thermal hold. The photonic estimate is therefore
**1.56 times the digital energy**, missing both parity and the registered 3× threshold. Removing
the unsourced optimistic rows lowers the best ratio to 0.23, and the conservative maximum is 0.38.
The kill gate fired, and no product simulation or fabrication spend followed.

Thermal management dominates even the most favorable cell with zero actuator hold. Dropping the
gain stage costs memory, though less than a naive tenfold: the frozen minimum-damping model gives a
pumped-to-passive memory ratio of 3.14 at $r_\text{min}$ (N9.7). Longer control and settling times
can only raise modelled photonic energy at a fixed retraining cadence, so they cannot reverse the
gate. The calculation also does not establish that practical retraining is cheap, or that the
chosen cadence maintains accuracy. At fixed power and fixed
tap count the ratio grows only linearly with sample rate; higher rates lie outside PR-20 and have
no trainability result. This function-matched result supersedes the positive reading of §7.2: the
simulated trainability result stands, and energy-competitive hardware has not been demonstrated.
