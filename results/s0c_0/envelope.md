# S0c.0 — FSR-matched inline envelope (PR-22, frozen 2026-09-15)

Arithmetic only; rows and statuses in `docs/s0b/s0b_0_ledger.md`, `docs/s0c/fsr_matched_regime.md`, `docs/s0c/mapping_fsr_matched.md`; rules in PR-22.

## 1. Insertion loss [dB] (lattice + packaging) and whether the amplifier row is charged

| N | K | OPT IL | amp? | CONS IL | amp? |
|---|---|---|---|---|---|
| 8 | 5% | 5.26 | yes | 7.96 | yes |
| 8 | 10% | 2.78 | no | 5.48 | yes |
| 8 | 20% | 1.50 | no | 4.20 | yes |
| 16 | 5% | 10.22 | yes | 12.92 | yes |
| 16 | 10% | 5.26 | yes | 7.96 | yes |
| 16 | 20% | 2.70 | no | 5.40 | yes |
| 32 | 5% | 20.14 | yes | 22.84 | yes |
| 32 | 10% | 10.22 | yes | 12.92 | yes |
| 32 | 20% | 5.10 | yes | 7.80 | yes |

## 2.1 Clearance — OPT (ratio = E_digital/E_photonic; η = 4 taps/ring; e_tap 0.05 pJ; showing 64 GS/s cells plus any other cell that clears)

| class | drift | N | K | GS/s | IL dB | amp | P mW | E_ph pJ | taps | E_dig pJ | ratio | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | TEC | 8 | 10% | 64 | 2.8 | n | 1,172 | 18.3 | 32 | 1.6 | 0.09 | LOSES |
| A | TEC | 16 | 10% | 64 | 5.3 | y | 2,184 | 34.1 | 64 | 3.2 | 0.09 | LOSES |
| A | TEC | 32 | 10% | 64 | 10.2 | y | 4,168 | 65.1 | 128 | 6.4 | 0.10 | LOSES |
| A | GHEAT | 8 | 10% | 64 | 2.8 | n | 1,002 | 15.7 | 32 | 1.6 | 0.10 | LOSES |
| A | GHEAT | 16 | 10% | 64 | 5.3 | y | 2,014 | 31.5 | 64 | 3.2 | 0.10 | LOSES |
| A | GHEAT | 32 | 10% | 64 | 10.2 | y | 3,998 | 62.5 | 128 | 6.4 | 0.10 | LOSES |
| A | TRACK | 8 | 10% | 64 | 2.8 | n | 993 | 15.5 | 32 | 1.6 | 0.10 | LOSES |
| A | TRACK | 16 | 10% | 64 | 5.3 | y | 2,005 | 31.3 | 64 | 3.2 | 0.10 | LOSES |
| A | TRACK | 32 | 10% | 64 | 10.2 | y | 3,989 | 62.3 | 128 | 6.4 | 0.10 | LOSES |
| A | ATHERMAL | 8 | 10% | 64 | 2.8 | n | 992 | 15.5 | 32 | 1.6 | 0.10 | LOSES |
| A | ATHERMAL | 16 | 10% | 64 | 5.3 | y | 2,004 | 31.3 | 64 | 3.2 | 0.10 | LOSES |
| A | ATHERMAL | 32 | 10% | 64 | 10.2 | y | 3,988 | 62.3 | 128 | 6.4 | 0.10 | LOSES |
| B | TEC | 8 | 10% | 64 | 2.8 | n | 228 | 3.56 | 32 | 1.6 | 0.45 | LOSES |
| B | TEC | 16 | 10% | 64 | 5.3 | y | 296 | 4.63 | 64 | 3.2 | 0.69 | LOSES |
| B | TEC | 32 | 10% | 64 | 10.2 | y | 392 | 6.13 | 128 | 6.4 | 1.04 | LOSES |
| B | GHEAT | 8 | 10% | 64 | 2.8 | n | 58.1 | 0.907 | 32 | 1.6 | 1.76 | LOSES |
| B | GHEAT | 16 | 10% | 64 | 5.3 | y | 126 | 1.97 | 64 | 3.2 | 1.62 | LOSES |
| B | GHEAT | 16 | 20% | 100 | 2.7 | n | 106 | 1.06 | 64 | 3.2 | 3.02 | CLEARS (edge) |
| B | GHEAT | 32 | 10% | 64 | 10.2 | y | 222 | 3.47 | 128 | 6.4 | 1.84 | LOSES |
| B | TRACK | 8 | 10% | 64 | 2.8 | n | 49.4 | 0.771 | 32 | 1.6 | 2.07 | LOSES |
| B | TRACK | 8 | 10% | 100 | 2.8 | n | 49.4 | 0.494 | 32 | 1.6 | 3.24 | CLEARS (edge) |
| B | TRACK | 8 | 20% | 100 | 1.5 | n | 49.4 | 0.494 | 32 | 1.6 | 3.24 | CLEARS (edge) |
| B | TRACK | 16 | 10% | 64 | 5.3 | y | 117 | 1.83 | 64 | 3.2 | 1.75 | LOSES |
| B | TRACK | 16 | 20% | 100 | 2.7 | n | 97.4 | 0.974 | 64 | 3.2 | 3.29 | CLEARS (edge) |
| B | TRACK | 32 | 10% | 64 | 10.2 | y | 213 | 3.33 | 128 | 6.4 | 1.92 | LOSES |
| B | ATHERMAL | 8 | 10% | 64 | 2.8 | n | 48.1 | 0.751 | 32 | 1.6 | 2.13 | LOSES |
| B | ATHERMAL | 8 | 10% | 100 | 2.8 | n | 48.1 | 0.481 | 32 | 1.6 | 3.33 | CLEARS (edge) |
| B | ATHERMAL | 8 | 20% | 100 | 1.5 | n | 48.1 | 0.481 | 32 | 1.6 | 3.33 | CLEARS (edge) |
| B | ATHERMAL | 16 | 10% | 64 | 5.3 | y | 116 | 1.81 | 64 | 3.2 | 1.76 | LOSES |
| B | ATHERMAL | 16 | 20% | 100 | 2.7 | n | 96.1 | 0.961 | 64 | 3.2 | 3.33 | CLEARS (edge) |
| B | ATHERMAL | 32 | 5% | 100 | 20.1 | y | 212 | 2.12 | 128 | 6.4 | 3.02 | CLEARS (edge) |
| B | ATHERMAL | 32 | 10% | 64 | 10.2 | y | 212 | 3.31 | 128 | 6.4 | 1.93 | LOSES |
| B | ATHERMAL | 32 | 10% | 100 | 10.2 | y | 212 | 2.12 | 128 | 6.4 | 3.02 | CLEARS (edge) |
| B | ATHERMAL | 32 | 20% | 100 | 5.1 | y | 212 | 2.12 | 128 | 6.4 | 3.02 | CLEARS (edge) |
| Cpz | TEC | 8 | 10% | 64 | 2.8 | n | 182 | 2.84 | 32 | 1.6 | 0.56 | LOSES |
| Cpz | TEC | 16 | 10% | 64 | 5.3 | y | 203 | 3.18 | 64 | 3.2 | 1.01 | LOSES |
| Cpz | TEC | 32 | 5% | 100 | 20.1 | y | 206 | 2.06 | 128 | 6.4 | 3.10 | CLEARS (edge) |
| Cpz | TEC | 32 | 10% | 64 | 10.2 | y | 206 | 3.23 | 128 | 6.4 | 1.98 | LOSES |
| Cpz | TEC | 32 | 10% | 100 | 10.2 | y | 206 | 2.06 | 128 | 6.4 | 3.10 | CLEARS (edge) |
| Cpz | TEC | 32 | 20% | 100 | 5.1 | y | 206 | 2.06 | 128 | 6.4 | 3.10 | CLEARS (edge) |
| Cpz | GHEAT | 8 | 5% | 64 | 5.3 | y | 31.7 | 0.495 | 32 | 1.6 | 3.23 | CLEARS |
| Cpz | GHEAT | 8 | 5% | 100 | 5.3 | y | 31.7 | 0.317 | 32 | 1.6 | 5.05 | CLEARS (edge) |
| Cpz | GHEAT | 8 | 10% | 32 | 2.8 | n | 11.7 | 0.364 | 32 | 1.6 | 4.39 | CLEARS |
| Cpz | GHEAT | 8 | 10% | 64 | 2.8 | n | 11.7 | 0.182 | 32 | 1.6 | 8.79 | CLEARS |
| Cpz | GHEAT | 8 | 10% | 100 | 2.8 | n | 11.7 | 0.117 | 32 | 1.6 | 13.73 | CLEARS (edge) |
| Cpz | GHEAT | 8 | 20% | 32 | 1.5 | n | 11.7 | 0.364 | 32 | 1.6 | 4.39 | CLEARS |
| Cpz | GHEAT | 8 | 20% | 64 | 1.5 | n | 11.7 | 0.182 | 32 | 1.6 | 8.79 | CLEARS |
| Cpz | GHEAT | 8 | 20% | 100 | 1.5 | n | 11.7 | 0.117 | 32 | 1.6 | 13.73 | CLEARS (edge) |
| Cpz | GHEAT | 16 | 5% | 32 | 10.2 | y | 33.3 | 1.04 | 64 | 3.2 | 3.08 | CLEARS |
| Cpz | GHEAT | 16 | 5% | 64 | 10.2 | y | 33.3 | 0.52 | 64 | 3.2 | 6.16 | CLEARS |
| Cpz | GHEAT | 16 | 5% | 100 | 10.2 | y | 33.3 | 0.333 | 64 | 3.2 | 9.62 | CLEARS (edge) |
| Cpz | GHEAT | 16 | 10% | 32 | 5.3 | y | 33.3 | 1.04 | 64 | 3.2 | 3.08 | CLEARS |
| Cpz | GHEAT | 16 | 10% | 64 | 5.3 | y | 33.3 | 0.52 | 64 | 3.2 | 6.16 | CLEARS |
| Cpz | GHEAT | 16 | 10% | 100 | 5.3 | y | 33.3 | 0.333 | 64 | 3.2 | 9.62 | CLEARS (edge) |
| Cpz | GHEAT | 16 | 20% | 32 | 2.7 | n | 13.3 | 0.414 | 64 | 3.2 | 7.73 | CLEARS |
| Cpz | GHEAT | 16 | 20% | 64 | 2.7 | n | 13.3 | 0.207 | 64 | 3.2 | 15.45 | CLEARS |
| Cpz | GHEAT | 16 | 20% | 100 | 2.7 | n | 13.3 | 0.133 | 64 | 3.2 | 24.14 | CLEARS (edge) |
| Cpz | GHEAT | 32 | 5% | 32 | 20.1 | y | 36.5 | 1.14 | 128 | 6.4 | 5.62 | CLEARS |
| Cpz | GHEAT | 32 | 5% | 64 | 20.1 | y | 36.5 | 0.57 | 128 | 6.4 | 11.24 | CLEARS |
| Cpz | GHEAT | 32 | 5% | 100 | 20.1 | y | 36.5 | 0.365 | 128 | 6.4 | 17.56 | CLEARS (edge) |
| Cpz | GHEAT | 32 | 10% | 32 | 10.2 | y | 36.5 | 1.14 | 128 | 6.4 | 5.62 | CLEARS |
| Cpz | GHEAT | 32 | 10% | 64 | 10.2 | y | 36.5 | 0.57 | 128 | 6.4 | 11.24 | CLEARS |
| Cpz | GHEAT | 32 | 10% | 100 | 10.2 | y | 36.5 | 0.365 | 128 | 6.4 | 17.56 | CLEARS (edge) |
| Cpz | GHEAT | 32 | 20% | 32 | 5.1 | y | 36.5 | 1.14 | 128 | 6.4 | 5.62 | CLEARS |
| Cpz | GHEAT | 32 | 20% | 64 | 5.1 | y | 36.5 | 0.57 | 128 | 6.4 | 11.24 | CLEARS |
| Cpz | GHEAT | 32 | 20% | 100 | 5.1 | y | 36.5 | 0.365 | 128 | 6.4 | 17.56 | CLEARS (edge) |
| Cpz | TRACK | 8 | 5% | 64 | 5.3 | y | 23 | 0.359 | 32 | 1.6 | 4.46 | CLEARS |
| Cpz | TRACK | 8 | 5% | 100 | 5.3 | y | 23 | 0.23 | 32 | 1.6 | 6.97 | CLEARS (edge) |
| Cpz | TRACK | 8 | 10% | 32 | 2.8 | n | 2.96 | 0.0924 | 32 | 1.6 | 17.33 | CLEARS |
| Cpz | TRACK | 8 | 10% | 64 | 2.8 | n | 2.96 | 0.0462 | 32 | 1.6 | 34.65 | CLEARS |
| Cpz | TRACK | 8 | 10% | 100 | 2.8 | n | 2.96 | 0.0296 | 32 | 1.6 | 54.14 | CLEARS (edge) |
| Cpz | TRACK | 8 | 20% | 32 | 1.5 | n | 2.96 | 0.0924 | 32 | 1.6 | 17.33 | CLEARS |
| Cpz | TRACK | 8 | 20% | 64 | 1.5 | n | 2.96 | 0.0462 | 32 | 1.6 | 34.65 | CLEARS |
| Cpz | TRACK | 8 | 20% | 100 | 1.5 | n | 2.96 | 0.0296 | 32 | 1.6 | 54.14 | CLEARS (edge) |
| Cpz | TRACK | 16 | 5% | 32 | 10.2 | y | 24.6 | 0.767 | 64 | 3.2 | 4.17 | CLEARS |
| Cpz | TRACK | 16 | 5% | 64 | 10.2 | y | 24.6 | 0.384 | 64 | 3.2 | 8.34 | CLEARS |
| Cpz | TRACK | 16 | 5% | 100 | 10.2 | y | 24.6 | 0.246 | 64 | 3.2 | 13.03 | CLEARS (edge) |
| Cpz | TRACK | 16 | 10% | 32 | 5.3 | y | 24.6 | 0.767 | 64 | 3.2 | 4.17 | CLEARS |
| Cpz | TRACK | 16 | 10% | 64 | 5.3 | y | 24.6 | 0.384 | 64 | 3.2 | 8.34 | CLEARS |
| Cpz | TRACK | 16 | 10% | 100 | 5.3 | y | 24.6 | 0.246 | 64 | 3.2 | 13.03 | CLEARS (edge) |
| Cpz | TRACK | 16 | 20% | 32 | 2.7 | n | 4.56 | 0.142 | 64 | 3.2 | 22.48 | CLEARS |
| Cpz | TRACK | 16 | 20% | 64 | 2.7 | n | 4.56 | 0.0712 | 64 | 3.2 | 44.96 | CLEARS |
| Cpz | TRACK | 16 | 20% | 100 | 2.7 | n | 4.56 | 0.0456 | 64 | 3.2 | 70.25 | CLEARS (edge) |
| Cpz | TRACK | 32 | 5% | 32 | 20.1 | y | 27.8 | 0.867 | 128 | 6.4 | 7.38 | CLEARS |
| Cpz | TRACK | 32 | 5% | 64 | 20.1 | y | 27.8 | 0.434 | 128 | 6.4 | 14.76 | CLEARS |
| Cpz | TRACK | 32 | 5% | 100 | 20.1 | y | 27.8 | 0.278 | 128 | 6.4 | 23.06 | CLEARS (edge) |
| Cpz | TRACK | 32 | 10% | 32 | 10.2 | y | 27.8 | 0.867 | 128 | 6.4 | 7.38 | CLEARS |
| Cpz | TRACK | 32 | 10% | 64 | 10.2 | y | 27.8 | 0.434 | 128 | 6.4 | 14.76 | CLEARS |
| Cpz | TRACK | 32 | 10% | 100 | 10.2 | y | 27.8 | 0.278 | 128 | 6.4 | 23.06 | CLEARS (edge) |
| Cpz | TRACK | 32 | 20% | 32 | 5.1 | y | 27.8 | 0.867 | 128 | 6.4 | 7.38 | CLEARS |
| Cpz | TRACK | 32 | 20% | 64 | 5.1 | y | 27.8 | 0.434 | 128 | 6.4 | 14.76 | CLEARS |
| Cpz | TRACK | 32 | 20% | 100 | 5.1 | y | 27.8 | 0.278 | 128 | 6.4 | 23.06 | CLEARS (edge) |
| Cpz | ATHERMAL | 8 | 5% | 64 | 5.3 | y | 21.7 | 0.338 | 32 | 1.6 | 4.73 | CLEARS |
| Cpz | ATHERMAL | 8 | 5% | 100 | 5.3 | y | 21.7 | 0.217 | 32 | 1.6 | 7.39 | CLEARS (edge) |
| Cpz | ATHERMAL | 8 | 10% | 32 | 2.8 | n | 1.66 | 0.0517 | 32 | 1.6 | 30.93 | CLEARS |
| Cpz | ATHERMAL | 8 | 10% | 64 | 2.8 | n | 1.66 | 0.0259 | 32 | 1.6 | 61.86 | CLEARS |
| Cpz | ATHERMAL | 8 | 10% | 100 | 2.8 | n | 1.66 | 0.0166 | 32 | 1.6 | 96.66 | CLEARS (edge) |
| Cpz | ATHERMAL | 8 | 20% | 32 | 1.5 | n | 1.66 | 0.0517 | 32 | 1.6 | 30.93 | CLEARS |
| Cpz | ATHERMAL | 8 | 20% | 64 | 1.5 | n | 1.66 | 0.0259 | 32 | 1.6 | 61.86 | CLEARS |
| Cpz | ATHERMAL | 8 | 20% | 100 | 1.5 | n | 1.66 | 0.0166 | 32 | 1.6 | 96.66 | CLEARS (edge) |
| Cpz | ATHERMAL | 16 | 5% | 32 | 10.2 | y | 23.3 | 0.727 | 64 | 3.2 | 4.40 | CLEARS |
| Cpz | ATHERMAL | 16 | 5% | 64 | 10.2 | y | 23.3 | 0.363 | 64 | 3.2 | 8.81 | CLEARS |
| Cpz | ATHERMAL | 16 | 5% | 100 | 10.2 | y | 23.3 | 0.233 | 64 | 3.2 | 13.76 | CLEARS (edge) |
| Cpz | ATHERMAL | 16 | 10% | 32 | 5.3 | y | 23.3 | 0.727 | 64 | 3.2 | 4.40 | CLEARS |
| Cpz | ATHERMAL | 16 | 10% | 64 | 5.3 | y | 23.3 | 0.363 | 64 | 3.2 | 8.81 | CLEARS |
| Cpz | ATHERMAL | 16 | 10% | 100 | 5.3 | y | 23.3 | 0.233 | 64 | 3.2 | 13.76 | CLEARS (edge) |
| Cpz | ATHERMAL | 16 | 20% | 32 | 2.7 | n | 3.26 | 0.102 | 64 | 3.2 | 31.46 | CLEARS |
| Cpz | ATHERMAL | 16 | 20% | 64 | 2.7 | n | 3.26 | 0.0509 | 64 | 3.2 | 62.91 | CLEARS |
| Cpz | ATHERMAL | 16 | 20% | 100 | 2.7 | n | 3.26 | 0.0326 | 64 | 3.2 | 98.30 | CLEARS (edge) |
| Cpz | ATHERMAL | 32 | 5% | 32 | 20.1 | y | 26.5 | 0.827 | 128 | 6.4 | 7.74 | CLEARS |
| Cpz | ATHERMAL | 32 | 5% | 64 | 20.1 | y | 26.5 | 0.413 | 128 | 6.4 | 15.48 | CLEARS |
| Cpz | ATHERMAL | 32 | 5% | 100 | 20.1 | y | 26.5 | 0.265 | 128 | 6.4 | 24.19 | CLEARS (edge) |
| Cpz | ATHERMAL | 32 | 10% | 32 | 10.2 | y | 26.5 | 0.827 | 128 | 6.4 | 7.74 | CLEARS |
| Cpz | ATHERMAL | 32 | 10% | 64 | 10.2 | y | 26.5 | 0.413 | 128 | 6.4 | 15.48 | CLEARS |
| Cpz | ATHERMAL | 32 | 10% | 100 | 10.2 | y | 26.5 | 0.265 | 128 | 6.4 | 24.19 | CLEARS (edge) |
| Cpz | ATHERMAL | 32 | 20% | 32 | 5.1 | y | 26.5 | 0.827 | 128 | 6.4 | 7.74 | CLEARS |
| Cpz | ATHERMAL | 32 | 20% | 64 | 5.1 | y | 26.5 | 0.413 | 128 | 6.4 | 15.48 | CLEARS |
| Cpz | ATHERMAL | 32 | 20% | 100 | 5.1 | y | 26.5 | 0.265 | 128 | 6.4 | 24.19 | CLEARS (edge) |
| Cpcm | TEC | 8 | 10% | 64 | 2.8 | n | 180 | 2.81 | 32 | 1.6 | 0.57 | LOSES |
| Cpcm | TEC | 16 | 10% | 64 | 5.3 | y | 200 | 3.13 | 64 | 3.2 | 1.02 | LOSES |
| Cpcm | TEC | 32 | 5% | 100 | 20.1 | y | 200 | 2 | 128 | 6.4 | 3.20 | CLEARS (edge) |
| Cpcm | TEC | 32 | 10% | 64 | 10.2 | y | 200 | 3.13 | 128 | 6.4 | 2.05 | LOSES |
| Cpcm | TEC | 32 | 10% | 100 | 10.2 | y | 200 | 2 | 128 | 6.4 | 3.20 | CLEARS (edge) |
| Cpcm | TEC | 32 | 20% | 100 | 5.1 | y | 200 | 2 | 128 | 6.4 | 3.20 | CLEARS (edge) |
| Cpcm | GHEAT | 8 | 5% | 64 | 5.3 | y | 30.1 | 0.47 | 32 | 1.6 | 3.41 | CLEARS |
| Cpcm | GHEAT | 8 | 5% | 100 | 5.3 | y | 30.1 | 0.301 | 32 | 1.6 | 5.32 | CLEARS (edge) |
| Cpcm | GHEAT | 8 | 10% | 32 | 2.8 | n | 10.1 | 0.314 | 32 | 1.6 | 5.09 | CLEARS |
| Cpcm | GHEAT | 8 | 10% | 64 | 2.8 | n | 10.1 | 0.157 | 32 | 1.6 | 10.18 | CLEARS |
| Cpcm | GHEAT | 8 | 10% | 100 | 2.8 | n | 10.1 | 0.101 | 32 | 1.6 | 15.91 | CLEARS (edge) |
| Cpcm | GHEAT | 8 | 20% | 32 | 1.5 | n | 10.1 | 0.314 | 32 | 1.6 | 5.09 | CLEARS |
| Cpcm | GHEAT | 8 | 20% | 64 | 1.5 | n | 10.1 | 0.157 | 32 | 1.6 | 10.18 | CLEARS |
| Cpcm | GHEAT | 8 | 20% | 100 | 1.5 | n | 10.1 | 0.101 | 32 | 1.6 | 15.91 | CLEARS (edge) |
| Cpcm | GHEAT | 16 | 5% | 32 | 10.2 | y | 30.1 | 0.939 | 64 | 3.2 | 3.41 | CLEARS |
| Cpcm | GHEAT | 16 | 5% | 64 | 10.2 | y | 30.1 | 0.47 | 64 | 3.2 | 6.81 | CLEARS |
| Cpcm | GHEAT | 16 | 5% | 100 | 10.2 | y | 30.1 | 0.301 | 64 | 3.2 | 10.65 | CLEARS (edge) |
| Cpcm | GHEAT | 16 | 10% | 32 | 5.3 | y | 30.1 | 0.939 | 64 | 3.2 | 3.41 | CLEARS |
| Cpcm | GHEAT | 16 | 10% | 64 | 5.3 | y | 30.1 | 0.47 | 64 | 3.2 | 6.81 | CLEARS |
| Cpcm | GHEAT | 16 | 10% | 100 | 5.3 | y | 30.1 | 0.301 | 64 | 3.2 | 10.65 | CLEARS (edge) |
| Cpcm | GHEAT | 16 | 20% | 32 | 2.7 | n | 10.1 | 0.314 | 64 | 3.2 | 10.18 | CLEARS |
| Cpcm | GHEAT | 16 | 20% | 64 | 2.7 | n | 10.1 | 0.157 | 64 | 3.2 | 20.37 | CLEARS |
| Cpcm | GHEAT | 16 | 20% | 100 | 2.7 | n | 10.1 | 0.101 | 64 | 3.2 | 31.82 | CLEARS (edge) |
| Cpcm | GHEAT | 32 | 5% | 32 | 20.1 | y | 30.1 | 0.939 | 128 | 6.4 | 6.81 | CLEARS |
| Cpcm | GHEAT | 32 | 5% | 64 | 20.1 | y | 30.1 | 0.47 | 128 | 6.4 | 13.63 | CLEARS |
| Cpcm | GHEAT | 32 | 5% | 100 | 20.1 | y | 30.1 | 0.301 | 128 | 6.4 | 21.29 | CLEARS (edge) |
| Cpcm | GHEAT | 32 | 10% | 32 | 10.2 | y | 30.1 | 0.939 | 128 | 6.4 | 6.81 | CLEARS |
| Cpcm | GHEAT | 32 | 10% | 64 | 10.2 | y | 30.1 | 0.47 | 128 | 6.4 | 13.63 | CLEARS |
| Cpcm | GHEAT | 32 | 10% | 100 | 10.2 | y | 30.1 | 0.301 | 128 | 6.4 | 21.29 | CLEARS (edge) |
| Cpcm | GHEAT | 32 | 20% | 32 | 5.1 | y | 30.1 | 0.939 | 128 | 6.4 | 6.81 | CLEARS |
| Cpcm | GHEAT | 32 | 20% | 64 | 5.1 | y | 30.1 | 0.47 | 128 | 6.4 | 13.63 | CLEARS |
| Cpcm | GHEAT | 32 | 20% | 100 | 5.1 | y | 30.1 | 0.301 | 128 | 6.4 | 21.29 | CLEARS (edge) |
| Cpcm | ATHERMAL | 8 | 5% | 64 | 5.3 | y | 20.1 | 0.313 | 32 | 1.6 | 5.11 | CLEARS |
| Cpcm | ATHERMAL | 8 | 5% | 100 | 5.3 | y | 20.1 | 0.201 | 32 | 1.6 | 7.98 | CLEARS (edge) |
| Cpcm | ATHERMAL | 8 | 10% | 32 | 2.8 | n | 0.0553 | 0.00173 | 32 | 1.6 | 926.70 | CLEARS |
| Cpcm | ATHERMAL | 8 | 10% | 64 | 2.8 | n | 0.0553 | 0.000863 | 32 | 1.6 | 1853.39 | CLEARS |
| Cpcm | ATHERMAL | 8 | 10% | 100 | 2.8 | n | 0.0553 | 0.000553 | 32 | 1.6 | 2895.93 | CLEARS (edge) |
| Cpcm | ATHERMAL | 8 | 20% | 32 | 1.5 | n | 0.0553 | 0.00173 | 32 | 1.6 | 926.70 | CLEARS |
| Cpcm | ATHERMAL | 8 | 20% | 64 | 1.5 | n | 0.0553 | 0.000863 | 32 | 1.6 | 1853.39 | CLEARS |
| Cpcm | ATHERMAL | 8 | 20% | 100 | 1.5 | n | 0.0553 | 0.000553 | 32 | 1.6 | 2895.93 | CLEARS (edge) |
| Cpcm | ATHERMAL | 16 | 5% | 32 | 10.2 | y | 20.1 | 0.627 | 64 | 3.2 | 5.11 | CLEARS |
| Cpcm | ATHERMAL | 16 | 5% | 64 | 10.2 | y | 20.1 | 0.313 | 64 | 3.2 | 10.21 | CLEARS |
| Cpcm | ATHERMAL | 16 | 5% | 100 | 10.2 | y | 20.1 | 0.201 | 64 | 3.2 | 15.96 | CLEARS (edge) |
| Cpcm | ATHERMAL | 16 | 10% | 32 | 5.3 | y | 20.1 | 0.627 | 64 | 3.2 | 5.11 | CLEARS |
| Cpcm | ATHERMAL | 16 | 10% | 64 | 5.3 | y | 20.1 | 0.313 | 64 | 3.2 | 10.21 | CLEARS |
| Cpcm | ATHERMAL | 16 | 10% | 100 | 5.3 | y | 20.1 | 0.201 | 64 | 3.2 | 15.96 | CLEARS (edge) |
| Cpcm | ATHERMAL | 16 | 20% | 32 | 2.7 | n | 0.0553 | 0.00173 | 64 | 3.2 | 1853.39 | CLEARS |
| Cpcm | ATHERMAL | 16 | 20% | 64 | 2.7 | n | 0.0553 | 0.000863 | 64 | 3.2 | 3706.79 | CLEARS |
| Cpcm | ATHERMAL | 16 | 20% | 100 | 2.7 | n | 0.0553 | 0.000553 | 64 | 3.2 | 5791.86 | CLEARS (edge) |
| Cpcm | ATHERMAL | 32 | 5% | 32 | 20.1 | y | 20.1 | 0.627 | 128 | 6.4 | 10.21 | CLEARS |
| Cpcm | ATHERMAL | 32 | 5% | 64 | 20.1 | y | 20.1 | 0.313 | 128 | 6.4 | 20.42 | CLEARS |
| Cpcm | ATHERMAL | 32 | 5% | 100 | 20.1 | y | 20.1 | 0.201 | 128 | 6.4 | 31.91 | CLEARS (edge) |
| Cpcm | ATHERMAL | 32 | 10% | 32 | 10.2 | y | 20.1 | 0.627 | 128 | 6.4 | 10.21 | CLEARS |
| Cpcm | ATHERMAL | 32 | 10% | 64 | 10.2 | y | 20.1 | 0.313 | 128 | 6.4 | 20.42 | CLEARS |
| Cpcm | ATHERMAL | 32 | 10% | 100 | 10.2 | y | 20.1 | 0.201 | 128 | 6.4 | 31.91 | CLEARS (edge) |
| Cpcm | ATHERMAL | 32 | 20% | 32 | 5.1 | y | 20.1 | 0.627 | 128 | 6.4 | 10.21 | CLEARS |
| Cpcm | ATHERMAL | 32 | 20% | 64 | 5.1 | y | 20.1 | 0.313 | 128 | 6.4 | 20.42 | CLEARS |
| Cpcm | ATHERMAL | 32 | 20% | 100 | 5.1 | y | 20.1 | 0.201 | 128 | 6.4 | 31.91 | CLEARS (edge) |

## 2.2 Clearance — CONS (ratio = E_digital/E_photonic; η = 2 taps/ring; e_tap 0.15 pJ; showing 64 GS/s cells plus any other cell that clears)

| class | drift | N | K | GS/s | IL dB | amp | P mW | E_ph pJ | taps | E_dig pJ | ratio | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | TEC | 8 | 10% | 64 | 5.5 | y | 6,145 | 96 | 16 | 2.4 | 0.02 | LOSES |
| A | TEC | 16 | 10% | 64 | 8.0 | y | 11,809 | 185 | 32 | 4.8 | 0.03 | LOSES |
| A | TEC | 32 | 10% | 64 | 12.9 | y | 23,137 | 362 | 64 | 9.6 | 0.03 | LOSES |
| A | GHEAT | 8 | 10% | 64 | 5.5 | y | 6,015 | 94 | 16 | 2.4 | 0.03 | LOSES |
| A | GHEAT | 16 | 10% | 64 | 8.0 | y | 11,679 | 182 | 32 | 4.8 | 0.03 | LOSES |
| A | GHEAT | 32 | 10% | 64 | 12.9 | y | 23,007 | 359 | 64 | 9.6 | 0.03 | LOSES |
| A | TRACK | 8 | 10% | 64 | 5.5 | y | 5,978 | 93.4 | 16 | 2.4 | 0.03 | LOSES |
| A | TRACK | 16 | 10% | 64 | 8.0 | y | 11,642 | 182 | 32 | 4.8 | 0.03 | LOSES |
| A | TRACK | 32 | 10% | 64 | 12.9 | y | 22,970 | 359 | 64 | 9.6 | 0.03 | LOSES |
| A | ATHERMAL | 8 | 10% | 64 | 5.5 | y | 5,965 | 93.2 | 16 | 2.4 | 0.03 | LOSES |
| A | ATHERMAL | 16 | 10% | 64 | 8.0 | y | 11,629 | 182 | 32 | 4.8 | 0.03 | LOSES |
| A | ATHERMAL | 32 | 10% | 64 | 12.9 | y | 22,957 | 359 | 64 | 9.6 | 0.03 | LOSES |
| B | TEC | 8 | 10% | 64 | 5.5 | y | 577 | 9.02 | 16 | 2.4 | 0.27 | LOSES |
| B | TEC | 16 | 10% | 64 | 8.0 | y | 673 | 10.5 | 32 | 4.8 | 0.46 | LOSES |
| B | TEC | 32 | 10% | 64 | 12.9 | y | 865 | 13.5 | 64 | 9.6 | 0.71 | LOSES |
| B | GHEAT | 8 | 10% | 64 | 5.5 | y | 447 | 6.98 | 16 | 2.4 | 0.34 | LOSES |
| B | GHEAT | 16 | 10% | 64 | 8.0 | y | 543 | 8.48 | 32 | 4.8 | 0.57 | LOSES |
| B | GHEAT | 32 | 10% | 64 | 12.9 | y | 735 | 11.5 | 64 | 9.6 | 0.84 | LOSES |
| B | TRACK | 8 | 10% | 64 | 5.5 | y | 410 | 6.41 | 16 | 2.4 | 0.37 | LOSES |
| B | TRACK | 16 | 10% | 64 | 8.0 | y | 506 | 7.91 | 32 | 4.8 | 0.61 | LOSES |
| B | TRACK | 32 | 10% | 64 | 12.9 | y | 698 | 10.9 | 64 | 9.6 | 0.88 | LOSES |
| B | ATHERMAL | 8 | 10% | 64 | 5.5 | y | 397 | 6.2 | 16 | 2.4 | 0.39 | LOSES |
| B | ATHERMAL | 16 | 10% | 64 | 8.0 | y | 493 | 7.7 | 32 | 4.8 | 0.62 | LOSES |
| B | ATHERMAL | 32 | 10% | 64 | 12.9 | y | 685 | 10.7 | 64 | 9.6 | 0.90 | LOSES |
| Cpz | TEC | 8 | 10% | 64 | 5.5 | y | 545 | 8.52 | 16 | 2.4 | 0.28 | LOSES |
| Cpz | TEC | 16 | 10% | 64 | 8.0 | y | 609 | 9.52 | 32 | 4.8 | 0.50 | LOSES |
| Cpz | TEC | 32 | 10% | 64 | 12.9 | y | 737 | 11.5 | 64 | 9.6 | 0.83 | LOSES |
| Cpz | GHEAT | 8 | 10% | 64 | 5.5 | y | 415 | 6.48 | 16 | 2.4 | 0.37 | LOSES |
| Cpz | GHEAT | 16 | 10% | 64 | 8.0 | y | 479 | 7.48 | 32 | 4.8 | 0.64 | LOSES |
| Cpz | GHEAT | 32 | 10% | 64 | 12.9 | y | 607 | 9.48 | 64 | 9.6 | 1.01 | LOSES |
| Cpz | TRACK | 8 | 10% | 64 | 5.5 | y | 378 | 5.91 | 16 | 2.4 | 0.41 | LOSES |
| Cpz | TRACK | 16 | 10% | 64 | 8.0 | y | 442 | 6.91 | 32 | 4.8 | 0.69 | LOSES |
| Cpz | TRACK | 32 | 10% | 64 | 12.9 | y | 570 | 8.91 | 64 | 9.6 | 1.08 | LOSES |
| Cpz | ATHERMAL | 8 | 10% | 64 | 5.5 | y | 365 | 5.7 | 16 | 2.4 | 0.42 | LOSES |
| Cpz | ATHERMAL | 16 | 10% | 64 | 8.0 | y | 429 | 6.7 | 32 | 4.8 | 0.72 | LOSES |
| Cpz | ATHERMAL | 32 | 10% | 64 | 12.9 | y | 557 | 8.7 | 64 | 9.6 | 1.10 | LOSES |
| Cpcm | TEC | 8 | 10% | 64 | 5.5 | y | 481 | 7.52 | 16 | 2.4 | 0.32 | LOSES |
| Cpcm | TEC | 16 | 10% | 64 | 8.0 | y | 481 | 7.52 | 32 | 4.8 | 0.64 | LOSES |
| Cpcm | TEC | 32 | 10% | 64 | 12.9 | y | 481 | 7.52 | 64 | 9.6 | 1.28 | LOSES |
| Cpcm | GHEAT | 8 | 10% | 64 | 5.5 | y | 351 | 5.48 | 16 | 2.4 | 0.44 | LOSES |
| Cpcm | GHEAT | 16 | 10% | 64 | 8.0 | y | 351 | 5.48 | 32 | 4.8 | 0.88 | LOSES |
| Cpcm | GHEAT | 32 | 10% | 64 | 12.9 | y | 351 | 5.48 | 64 | 9.6 | 1.75 | LOSES |
| Cpcm | ATHERMAL | 8 | 10% | 64 | 5.5 | y | 301 | 4.7 | 16 | 2.4 | 0.51 | LOSES |
| Cpcm | ATHERMAL | 16 | 10% | 64 | 8.0 | y | 301 | 4.7 | 32 | 4.8 | 1.02 | LOSES |
| Cpcm | ATHERMAL | 32 | 5% | 100 | 22.8 | y | 301 | 3.01 | 64 | 9.6 | 3.19 | CLEARS (edge) |
| Cpcm | ATHERMAL | 32 | 10% | 64 | 12.9 | y | 301 | 4.7 | 64 | 9.6 | 2.04 | LOSES |
| Cpcm | ATHERMAL | 32 | 10% | 100 | 12.9 | y | 301 | 3.01 | 64 | 9.6 | 3.19 | CLEARS (edge) |
| Cpcm | ATHERMAL | 32 | 20% | 100 | 7.8 | y | 301 | 3.01 | 64 | 9.6 | 3.19 | CLEARS (edge) |

Secondary anchor (SJTU convention): DSP CD share ≈ 1.25 pJ/sample at 56 GBd PAM4 — compare with the E_ph column directly.

## 3. Verdicts (PR-22 §22.4)

**Kill gate (OPT, classes B/C-pz/C-pcm, any drift):** max ratio = **5791.86** at Cpcm/ATHERMAL, N=16, K=20%, 100 GS/s (P 0.0553 mW → 0.000553 pJ vs 3.2 pJ). **Kill fires: False.**

**CONS window, sourced drift (TEC/ATHERMAL):** max ratio = **3.19** at Cpcm/ATHERMAL, N=32, K=5%, 100 GS/s. **Window exists: True** (3 clearing cells, incl. band-edge 100 GS/s cells).

**CONS window, any drift (incl. UNSOURCED):** max ratio = **3.19** at Cpcm/ATHERMAL, N=32. Window: True.

**Sensitivity (UNSOURCED rows removed; η = 2 both corners; e_tap at band ends):**

| corner | e_tap | max ratio | at |
|---|---|---|---|
| OPT | 0.03 | 1737.56 | Cpcm/ATHERMAL, N=16, K=20%, 100 GS/s |
| OPT | 0.25 | 14479.64 | Cpcm/ATHERMAL, N=16, K=20%, 100 GS/s |
| CONS | 0.03 | 0.64 | Cpcm/ATHERMAL, N=32, K=5%, 100 GS/s |
| CONS | 0.25 | 5.32 | Cpcm/ATHERMAL, N=32, K=5%, 100 GS/s |

**Clearing CONS cells under sourced drift (the S0c.1 grid if go):**

| class | drift | N | K | GS/s | ratio |
|---|---|---|---|---|---|
| Cpcm | ATHERMAL | 32 | 5% | 100 (edge) | 3.19 |
| Cpcm | ATHERMAL | 32 | 10% | 100 (edge) | 3.19 |
| Cpcm | ATHERMAL | 32 | 20% | 100 (edge) | 3.19 |
