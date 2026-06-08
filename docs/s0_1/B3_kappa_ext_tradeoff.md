# B3 — Memory vs readout-SNR (κ_ext) trade (S0.1 deliverable 6 / F13.3)

**Status:** Executor characterization for **PR-4** (κ_ext policy). *I characterize the trade; I do **not**
pick the operating point* — that is PR-4 at S0.3, Lucas-frozen, foundry-gated.

Kernel: `photonic_ssm.dynamics.pole_region.kappa_ext_trade_sweep`. Figure:
`results/s0_1/kappa_ext_tradeoff.png`. Data: `results/s0_1/s0_1_pole_region_data.json`.

## The trade

The external coupling `kappa_ext` sets both the memory and the readability, in opposite directions:

- **Memory** `~ 1/kappa_tot = 1/(kappa_i + 2*kappa_ext)` (symmetric add-drop). Deep **undercoupling**
  (`kappa_ext ≪ kappa_i`) → `kappa_tot → kappa_i` → **maximum** (loss-limited) memory.
- **Readout residue** `|c_j b_j| ~ 2*kappa_ext` and **on-resonance drop efficiency**
  `(2*kappa_ext/kappa_tot)²` (the detector-arm signal power, hence shot/thermal **detector SNR**). Deep
  undercoupling → residue and drop efficiency **collapse**: the SSM kernel amplitude and the readable
  signal vanish.

So you cannot maximize both. The product **memory × residue saturates at the passive memory length**
(`1/(kappa_i*dt)`) — formally bounded, demonstrated in `test_memory_times_residue_bounded_by_passive_memory`.

## Numbers (Qi = 2×10⁶ foundry corner, dt = round-trip time = 10 ps)

| `kappa_ext/kappa_i` | regime | memory (round trips) | drop efficiency | residue (norm) |
|---|---|---|---|---|
| 0.1 | deep undercoupling | 274 | 0.028 | 0.20 |
| 0.3 | undercoupling | 206 | 0.141 | 0.60 |
| 1.0 | near-critical | 110 | 0.444 | 2.0 |
| 3.0 | overcoupling | 47 | 0.735 | 6.0 |
| 10.0 | deep overcoupling | 16 | 0.907 | 20.0 |

(Passive ceiling at this Qi: 329 round trips.) At the class-leading Qi=3×10⁷ corner the same *shape*
holds with the memory axis scaled ~15× longer (`results/s0_1/s0_1_pole_region_data.json` → `kappa_ext_trade.by_Qi["3e+07"]`).

## Input to PR-4

- The realizable operating region is the **Pareto front** of (memory, detector-SNR) traced by the
  `kappa_ext` policy. The choice interacts with: the task's required memory length (PR-2, sized against
  this bound), the detector noise floor + available optical power (S0.7 budget), and the ASE/NF cell
  (PR-4). A **trainable `kappa_ext` within registered bounds** (vs a fixed regime) is itself a PR-4
  option — and note `kappa_ext` is also a **pole-real-part actuator** (B1), so making it trainable folds
  the readout trade into the recurrence training.
- **Interaction with B2:** overcoupling (large `kappa_ext`) widens the linewidth and *suppresses* visible
  backscatter splitting — so the κ_ext policy and the mode-splitting risk are coupled. A deep-undercoupled
  (max-memory) policy is the **most exposed** to the B2 doublet at high Qi.

PR-4 must register the κ_ext policy (fixed regime or trainable bounds) **before** the S0.3 substrate
build / S0.5 gate.
