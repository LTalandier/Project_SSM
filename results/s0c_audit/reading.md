# PR-22 arithmetic and physical-budget audit

No validated product window; frozen PR-22 arithmetic retained as historical scenario.

At 64 GS/s the stored favorable CONS cell is 2.0411×, not 1.25×.
At 100 GS/s, holding photonic costs fixed and using 0.05 pJ/tap gives 1.0631×, not 3.1892×.

| Loss dB/cm | K | Cavity FWHM GHz | Memory round trips | Resonance loss dB/ring | Assumed gain dB | Assumed output SNR dB |
|---:|---:|---:|---:|---:|---:|---:|
| 0.051 | 0.05 | 0.845 | 37.68 | 0.606 | 32.38 | 13.39 |
| 0.051 | 0.1 | 1.706 | 18.67 | 0.295 | 22.43 | 22.57 |
| 0.051 | 0.2 | 3.584 | 8.89 | 0.139 | 17.46 | 26.13 |
| 0.4 | 0.05 | 1.040 | 30.62 | 4.871 | 168.87 | -123.01 |
| 0.4 | 0.1 | 1.901 | 16.75 | 2.325 | 87.41 | -41.55 |
| 0.4 | 0.2 | 3.779 | 8.43 | 1.094 | 48.00 | -2.14 |

Amplifier scenario: input −10 dBm before lattice, target 0 dBm after amplifier; NF 5 dB, 64 GHz noise bandwidth, receiver SNR 30 dB, efficiency 10%, unknown idle power. Numbers outside assumed gain/output limits are infeasible in that scenario, not predictions of real devices.

0.4 dB/cm is a different athermal platform, transplanted here only as loss sensitivity.
Adding N on-resonance losses assumes coincident resonances; actual trained spectrum must be evaluated.
Amplifier inputs, targets, NF, efficiency, limits and receiver SNR are explicit sensitivity assumptions, not sourced product specifications.
No idle/control/thermal/actuator number or taps-per-ring equivalence has been validated for a co-integrated device.
