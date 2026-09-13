# S0b.0 — inline-scope re-envelope (PR-20, frozen 2026-09-13)

Arithmetic only. Rows and statuses: `docs/s0b/s0b_0_ledger.md`. Rules: `shared/preregistration.md` PR-20.

## 1. Reachability — N_reach = ⌊f_s / κ_net,min⌋ (single-ring amplitude memory at r_min = 0.1606)

| N (cell) | gain | 0.1 GS/s | 1 GS/s | 2 GS/s |
|---|---|---|---|---|
| 8 (C-1) | passive | 0 | 2 | 4 |
| 8 (C-1) | pumped | 0 | 7 | 15 |
| 32 (C-2) | passive | 0 | 8 | 16 |
| 32 (C-2) | pumped | 2 | 26 | 53 |
| 128 (C-3) | passive | 3 | 37 | 74 |
| 128 (C-3) | pumped | 11 | 117 | 234 |

Reading: passive C-2 reaches ≈ 17 taps at 2 GS/s, C-3 ≈ 75; pumped C-2 ≈ 53. N_taps = 128 is unreachable everywhere; 64 only at C-3 (passive) or pumped C-2/C-3.

## 2. Static + maintenance power decomposition [mW] at N = 32 (C-2), T_r = 100 s, passive

| corner | class | hold (N·CH·per-ch) | drift: TEC / GHEAT† / TRACK† | retrain(100 s) | pump (passive) |
|---|---|---|---|---|---|
| OPT | A | 3,968 | 180 / 10 / 1.3 | 0.0553 | 0 |
| OPT | B | 192 | 180 / 10 / 1.3 | 0.0553 | 0 |
| OPT | Cpz | 6.4 | 180 / 10 / 1.3 | 0.0553 | 0 |
| OPT | Cpcm | 0 | 180 / 10 / n/a | 0.0553 | 0 |
| OPT | hybrid | 0.8 | 180 / 10 / n/a | 0.0553 | 0 |
| CONS | A | 22,656 | 180 / 50 / 13 | 1.02 | 0 |
| CONS | B | 384 | 180 / 50 / 13 | 1.02 | 0 |
| CONS | Cpz | 256 | 180 / 50 / 13 | 1.02 | 0 |
| CONS | Cpcm | 0 | 180 / 50 / n/a | 1.02 | 0 |
| CONS | hybrid | 32 | 180 / 50 / n/a | 1.02 | 0 |

† UNSOURCED rows (ledger §3) — removed in the sensitivity re-statement (§6).

Pumped configuration adds OPT: 25.6 mW at N = 32; CONS: 724 mW at N = 32 (ledger §2) — reported, not the product configuration.

## 3. Retraining maintenance power ladder [mW] (uncorrelated residual only)

| T_r [s] | OPT | CONS |
|---|---|---|
| 1 | 5.53 | 102 |
| 10 | 0.552 | 10.2 |
| 100 | 0.0553 | 1.02 |
| 1000 | 0.00552 | 0.102 |

At the drift anchor (one C-2 linewidth per ≈ 1 h) T_r ≈ 10²–10³ s suffices: the retraining term is sub-milliwatt at OPT and ≤ 1 mW at CONS for T_r ≥ 100 s. The common-mode term dominates.

## 4. Digital equalizer block, priced per tap [pJ/sample]

| N_taps | OPT (0.05 pJ/tap) | CONS (0.15 pJ/tap) | P1 DSP-block row (25–170 pJ/bit × ENOB) |
|---|---|---|---|
| 4 | 0.2 | 0.6 | 210–1598 |
| 8 | 0.4 | 1.2 | 210–1598 ← P1 point |
| 16 | 0.8 | 2.4 | 210–1598 |
| 32 | 1.6 | 4.8 | 210–1598 |
| 64 | 3.2 | 9.6 | 210–1598 |
| 128 | 6.4 | 19.2 | 210–1598 |

The function-matched pricing is 30–100× harsher on the photonic side than P1's DSP-block row: P1 compared against a whole coherent DSP, not the equalizer it would replace.

## 5.1 Clearance — OPT corner, T_r = 100 s, best reachable N_taps per cell (ratio = E_digital / E_photonic; clears iff ≥ 3 and reachable; packaging 0.3 dB)

| class | gain | drift | N | GS/s | P [mW] | E_ph [pJ] | N_reach | taps | E_dig [pJ] | ratio | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | passive | TEC | 8 | 2 | 1,172 | 586 | 4 | 4 | 0.2 | 0.000341 | LOSES |
| A | passive | TEC | 32 | 2 | 4,148 | 2,074 | 16 | 16 | 0.8 | 0.000386 | LOSES |
| A | passive | TEC | 128 | 2 | 16,052 | 8,026 | 74 | 64 | 3.2 | 0.000399 | LOSES |
| A | passive | GHEAT | 8 | 2 | 1,002 | 501 | 4 | 4 | 0.2 | 0.000399 | LOSES |
| A | passive | GHEAT | 32 | 2 | 3,978 | 1,989 | 16 | 16 | 0.8 | 0.000402 | LOSES |
| A | passive | GHEAT | 128 | 2 | 15,882 | 7,941 | 74 | 64 | 3.2 | 0.000403 | LOSES |
| A | passive | TRACK | 8 | 2 | 993 | 497 | 4 | 4 | 0.2 | 0.000403 | LOSES |
| A | passive | TRACK | 32 | 2 | 3,969 | 1,985 | 16 | 16 | 0.8 | 0.000403 | LOSES |
| A | passive | TRACK | 128 | 2 | 15,873 | 7,937 | 74 | 64 | 3.2 | 0.000403 | LOSES |
| A | pumped | TEC | 8 | 2 | 1,178 | 589 | 15 | 8 | 0.4 | 0.000679 | LOSES |
| A | pumped | TEC | 32 | 2 | 4,174 | 2,087 | 53 | 32 | 1.6 | 0.000767 | LOSES |
| A | pumped | TEC | 128 | 2 | 16,154 | 8,077 | 234 | 128 | 6.4 | 0.000792 | LOSES |
| A | pumped | GHEAT | 8 | 2 | 1,008 | 504 | 15 | 8 | 0.4 | 0.000793 | LOSES |
| A | pumped | GHEAT | 32 | 2 | 4,004 | 2,002 | 53 | 32 | 1.6 | 0.000799 | LOSES |
| A | pumped | GHEAT | 128 | 2 | 15,984 | 7,992 | 234 | 128 | 6.4 | 0.000801 | LOSES |
| A | pumped | TRACK | 8 | 2 | 1,000 | 500 | 15 | 8 | 0.4 | 0.0008 | LOSES |
| A | pumped | TRACK | 32 | 2 | 3,995 | 1,997 | 53 | 32 | 1.6 | 0.000801 | LOSES |
| A | pumped | TRACK | 128 | 2 | 15,976 | 7,988 | 234 | 128 | 6.4 | 0.000801 | LOSES |
| B | passive | TEC | 8 | 2 | 228 | 114 | 4 | 4 | 0.2 | 0.00175 | LOSES |
| B | passive | TEC | 32 | 2 | 372 | 186 | 16 | 16 | 0.8 | 0.0043 | LOSES |
| B | passive | TEC | 128 | 2 | 948 | 474 | 74 | 64 | 3.2 | 0.00675 | LOSES |
| B | passive | GHEAT | 8 | 2 | 58.1 | 29 | 4 | 4 | 0.2 | 0.00689 | LOSES |
| B | passive | GHEAT | 32 | 2 | 202 | 101 | 16 | 16 | 0.8 | 0.00792 | LOSES |
| B | passive | GHEAT | 128 | 2 | 778 | 389 | 74 | 64 | 3.2 | 0.00823 | LOSES |
| B | passive | TRACK | 8 | 2 | 49.4 | 24.7 | 4 | 4 | 0.2 | 0.0081 | LOSES |
| B | passive | TRACK | 32 | 2 | 193 | 96.7 | 16 | 16 | 0.8 | 0.00827 | LOSES |
| B | passive | TRACK | 128 | 2 | 769 | 385 | 74 | 64 | 3.2 | 0.00832 | LOSES |
| B | pumped | TEC | 8 | 2 | 234 | 117 | 15 | 8 | 0.4 | 0.00341 | LOSES |
| B | pumped | TEC | 32 | 2 | 398 | 199 | 53 | 32 | 1.6 | 0.00805 | LOSES |
| B | pumped | TEC | 128 | 2 | 1,050 | 525 | 234 | 128 | 6.4 | 0.0122 | LOSES |
| B | pumped | GHEAT | 8 | 2 | 64.5 | 32.2 | 15 | 8 | 0.4 | 0.0124 | LOSES |
| B | pumped | GHEAT | 32 | 2 | 228 | 114 | 53 | 32 | 1.6 | 0.0141 | LOSES |
| B | pumped | GHEAT | 128 | 2 | 880 | 440 | 234 | 128 | 6.4 | 0.0145 | LOSES |
| B | pumped | TRACK | 8 | 2 | 55.8 | 27.9 | 15 | 8 | 0.4 | 0.0143 | LOSES |
| B | pumped | TRACK | 32 | 2 | 219 | 109 | 53 | 32 | 1.6 | 0.0146 | LOSES |
| B | pumped | TRACK | 128 | 2 | 872 | 436 | 234 | 128 | 6.4 | 0.0147 | LOSES |
| Cpz | passive | TEC | 8 | 2 | 182 | 90.8 | 4 | 4 | 0.2 | 0.0022 | LOSES |
| Cpz | passive | TEC | 32 | 2 | 186 | 93.2 | 16 | 16 | 0.8 | 0.00858 | LOSES |
| Cpz | passive | TEC | 128 | 2 | 206 | 103 | 74 | 64 | 3.2 | 0.0311 | LOSES |
| Cpz | passive | GHEAT | 8 | 2 | 11.7 | 5.83 | 4 | 4 | 0.2 | 0.0343 | LOSES |
| Cpz | passive | GHEAT | 32 | 2 | 16.5 | 8.23 | 16 | 16 | 0.8 | 0.0972 | LOSES |
| Cpz | passive | GHEAT | 128 | 2 | 35.7 | 17.8 | 74 | 64 | 3.2 | 0.179 | LOSES |
| Cpz | passive | TRACK | 8 | 2 | 2.96 | 1.48 | 4 | 4 | 0.2 | 0.135 | LOSES |
| Cpz | passive | TRACK | 32 | 2 | 7.76 | 3.88 | 16 | 16 | 0.8 | 0.206 | LOSES |
| Cpz | passive | TRACK | 128 | 2 | 27 | 13.5 | 74 | 64 | 3.2 | 0.237 | LOSES |
| Cpz | pumped | TEC | 8 | 2 | 188 | 94 | 15 | 8 | 0.4 | 0.00425 | LOSES |
| Cpz | pumped | TEC | 32 | 2 | 212 | 106 | 53 | 32 | 1.6 | 0.0151 | LOSES |
| Cpz | pumped | TEC | 128 | 2 | 308 | 154 | 234 | 128 | 6.4 | 0.0416 | LOSES |
| Cpz | pumped | GHEAT | 8 | 2 | 18.1 | 9.03 | 15 | 8 | 0.4 | 0.0443 | LOSES |
| Cpz | pumped | GHEAT | 32 | 2 | 42.1 | 21 | 53 | 32 | 1.6 | 0.0761 | LOSES |
| Cpz | pumped | GHEAT | 128 | 2 | 138 | 69 | 234 | 128 | 6.4 | 0.0927 | LOSES |
| Cpz | pumped | TRACK | 8 | 2 | 9.36 | 4.68 | 15 | 8 | 0.4 | 0.0855 | LOSES |
| Cpz | pumped | TRACK | 32 | 2 | 33.4 | 16.7 | 53 | 32 | 1.6 | 0.0959 | LOSES |
| Cpz | pumped | TRACK | 128 | 2 | 129 | 64.7 | 234 | 128 | 6.4 | 0.0989 | LOSES |
| Cpcm | passive | TEC | 8 | 2 | 180 | 90 | 4 | 4 | 0.2 | 0.00222 | LOSES |
| Cpcm | passive | TEC | 32 | 2 | 180 | 90 | 16 | 16 | 0.8 | 0.00889 | LOSES |
| Cpcm | passive | TEC | 128 | 2 | 180 | 90 | 74 | 64 | 3.2 | 0.0355 | LOSES |
| Cpcm | passive | GHEAT | 8 | 2 | 10.1 | 5.03 | 4 | 4 | 0.2 | 0.0398 | LOSES |
| Cpcm | passive | GHEAT | 32 | 2 | 10.1 | 5.03 | 16 | 16 | 0.8 | 0.159 | LOSES |
| Cpcm | passive | GHEAT | 128 | 2 | 10.1 | 5.03 | 74 | 64 | 3.2 | 0.636 | LOSES |
| Cpcm | pumped | TEC | 8 | 2 | 186 | 93.2 | 15 | 8 | 0.4 | 0.00429 | LOSES |
| Cpcm | pumped | TEC | 32 | 2 | 206 | 103 | 53 | 32 | 1.6 | 0.0156 | LOSES |
| Cpcm | pumped | TEC | 128 | 2 | 282 | 141 | 234 | 128 | 6.4 | 0.0453 | LOSES |
| Cpcm | pumped | GHEAT | 8 | 2 | 16.5 | 8.23 | 15 | 8 | 0.4 | 0.0486 | LOSES |
| Cpcm | pumped | GHEAT | 32 | 2 | 35.7 | 17.8 | 53 | 32 | 1.6 | 0.0897 | LOSES |
| Cpcm | pumped | GHEAT | 128 | 2 | 112 | 56.2 | 234 | 128 | 6.4 | 0.114 | LOSES |
| hybrid | passive | TEC | 8 | 2 | 181 | 90.4 | 4 | 4 | 0.2 | 0.00221 | LOSES |
| hybrid | passive | TEC | 32 | 2 | 181 | 90.4 | 16 | 16 | 0.8 | 0.00885 | LOSES |
| hybrid | passive | TEC | 128 | 2 | 181 | 90.4 | 74 | 64 | 3.2 | 0.0354 | LOSES |
| hybrid | passive | GHEAT | 8 | 2 | 10.9 | 5.43 | 4 | 4 | 0.2 | 0.0368 | LOSES |
| hybrid | passive | GHEAT | 32 | 2 | 10.9 | 5.43 | 16 | 16 | 0.8 | 0.147 | LOSES |
| hybrid | passive | GHEAT | 128 | 2 | 10.9 | 5.43 | 74 | 64 | 3.2 | 0.59 | LOSES |
| hybrid | pumped | TEC | 8 | 2 | 187 | 93.6 | 15 | 8 | 0.4 | 0.00427 | LOSES |
| hybrid | pumped | TEC | 32 | 2 | 206 | 103 | 53 | 32 | 1.6 | 0.0155 | LOSES |
| hybrid | pumped | TEC | 128 | 2 | 283 | 142 | 234 | 128 | 6.4 | 0.0452 | LOSES |
| hybrid | pumped | GHEAT | 8 | 2 | 17.3 | 8.63 | 15 | 8 | 0.4 | 0.0464 | LOSES |
| hybrid | pumped | GHEAT | 32 | 2 | 36.5 | 18.2 | 53 | 32 | 1.6 | 0.0878 | LOSES |
| hybrid | pumped | GHEAT | 128 | 2 | 113 | 56.6 | 234 | 128 | 6.4 | 0.113 | LOSES |

(Rows below 2 GS/s omitted unless they clear — a fixed-power device only gets worse at lower rates.)

## 5.2 Clearance — CONS corner, T_r = 100 s, best reachable N_taps per cell (ratio = E_digital / E_photonic; clears iff ≥ 3 and reachable; packaging 3.0 dB)

| class | gain | drift | N | GS/s | P [mW] | E_ph [pJ] | N_reach | taps | E_dig [pJ] | ratio | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | passive | TEC | 8 | 2 | 5,845 | 2,923 | 4 | 4 | 0.6 | 0.000205 | LOSES |
| A | passive | TEC | 32 | 2 | 22,837 | 11,419 | 16 | 16 | 2.4 | 0.00021 | LOSES |
| A | passive | TEC | 128 | 2 | 90,805 | 45,403 | 74 | 64 | 9.6 | 0.000211 | LOSES |
| A | passive | GHEAT | 8 | 2 | 5,715 | 2,858 | 4 | 4 | 0.6 | 0.00021 | LOSES |
| A | passive | GHEAT | 32 | 2 | 22,707 | 11,354 | 16 | 16 | 2.4 | 0.000211 | LOSES |
| A | passive | GHEAT | 128 | 2 | 90,675 | 45,338 | 74 | 64 | 9.6 | 0.000212 | LOSES |
| A | passive | TRACK | 8 | 2 | 5,678 | 2,839 | 4 | 4 | 0.6 | 0.000211 | LOSES |
| A | passive | TRACK | 32 | 2 | 22,670 | 11,335 | 16 | 16 | 2.4 | 0.000212 | LOSES |
| A | passive | TRACK | 128 | 2 | 90,638 | 45,319 | 74 | 64 | 9.6 | 0.000212 | LOSES |
| A | pumped | TEC | 8 | 2 | 6,161 | 3,081 | 15 | 8 | 1.2 | 0.00039 | LOSES |
| A | pumped | TEC | 32 | 2 | 23,561 | 11,781 | 53 | 32 | 4.8 | 0.000407 | LOSES |
| A | pumped | TEC | 128 | 2 | 93,161 | 46,581 | 234 | 128 | 19.2 | 0.000412 | LOSES |
| A | pumped | GHEAT | 8 | 2 | 6,031 | 3,016 | 15 | 8 | 1.2 | 0.000398 | LOSES |
| A | pumped | GHEAT | 32 | 2 | 23,431 | 11,716 | 53 | 32 | 4.8 | 0.00041 | LOSES |
| A | pumped | GHEAT | 128 | 2 | 93,031 | 46,516 | 234 | 128 | 19.2 | 0.000413 | LOSES |
| A | pumped | TRACK | 8 | 2 | 5,994 | 2,997 | 15 | 8 | 1.2 | 0.0004 | LOSES |
| A | pumped | TRACK | 32 | 2 | 23,394 | 11,697 | 53 | 32 | 4.8 | 0.00041 | LOSES |
| A | pumped | TRACK | 128 | 2 | 92,994 | 46,497 | 234 | 128 | 19.2 | 0.000413 | LOSES |
| B | passive | TEC | 8 | 2 | 277 | 139 | 4 | 4 | 0.6 | 0.00433 | LOSES |
| B | passive | TEC | 32 | 2 | 565 | 283 | 16 | 16 | 2.4 | 0.0085 | LOSES |
| B | passive | TEC | 128 | 2 | 1,717 | 859 | 74 | 64 | 9.6 | 0.0112 | LOSES |
| B | passive | GHEAT | 8 | 2 | 147 | 73.5 | 4 | 4 | 0.6 | 0.00816 | LOSES |
| B | passive | GHEAT | 32 | 2 | 435 | 218 | 16 | 16 | 2.4 | 0.011 | LOSES |
| B | passive | GHEAT | 128 | 2 | 1,587 | 794 | 74 | 64 | 9.6 | 0.0121 | LOSES |
| B | passive | TRACK | 8 | 2 | 110 | 55 | 4 | 4 | 0.6 | 0.0109 | LOSES |
| B | passive | TRACK | 32 | 2 | 398 | 199 | 16 | 16 | 2.4 | 0.0121 | LOSES |
| B | passive | TRACK | 128 | 2 | 1,550 | 775 | 74 | 64 | 9.6 | 0.0124 | LOSES |
| B | pumped | TEC | 8 | 2 | 593 | 297 | 15 | 8 | 1.2 | 0.00405 | LOSES |
| B | pumped | TEC | 32 | 2 | 1,289 | 645 | 53 | 32 | 4.8 | 0.00745 | LOSES |
| B | pumped | TEC | 128 | 2 | 4,073 | 2,037 | 234 | 128 | 19.2 | 0.00943 | LOSES |
| B | pumped | GHEAT | 8 | 2 | 463 | 232 | 15 | 8 | 1.2 | 0.00518 | LOSES |
| B | pumped | GHEAT | 32 | 2 | 1,159 | 580 | 53 | 32 | 4.8 | 0.00828 | LOSES |
| B | pumped | GHEAT | 128 | 2 | 3,943 | 1,972 | 234 | 128 | 19.2 | 0.00974 | LOSES |
| B | pumped | TRACK | 8 | 2 | 426 | 213 | 15 | 8 | 1.2 | 0.00563 | LOSES |
| B | pumped | TRACK | 32 | 2 | 1,122 | 561 | 53 | 32 | 4.8 | 0.00856 | LOSES |
| B | pumped | TRACK | 128 | 2 | 3,906 | 1,953 | 234 | 128 | 19.2 | 0.00983 | LOSES |
| Cpz | passive | TEC | 8 | 2 | 245 | 123 | 4 | 4 | 0.6 | 0.0049 | LOSES |
| Cpz | passive | TEC | 32 | 2 | 437 | 219 | 16 | 16 | 2.4 | 0.011 | LOSES |
| Cpz | passive | TEC | 128 | 2 | 1,205 | 603 | 74 | 64 | 9.6 | 0.0159 | LOSES |
| Cpz | passive | GHEAT | 8 | 2 | 115 | 57.5 | 4 | 4 | 0.6 | 0.0104 | LOSES |
| Cpz | passive | GHEAT | 32 | 2 | 307 | 154 | 16 | 16 | 2.4 | 0.0156 | LOSES |
| Cpz | passive | GHEAT | 128 | 2 | 1,075 | 538 | 74 | 64 | 9.6 | 0.0179 | LOSES |
| Cpz | passive | TRACK | 8 | 2 | 78 | 39 | 4 | 4 | 0.6 | 0.0154 | LOSES |
| Cpz | passive | TRACK | 32 | 2 | 270 | 135 | 16 | 16 | 2.4 | 0.0178 | LOSES |
| Cpz | passive | TRACK | 128 | 2 | 1,038 | 519 | 74 | 64 | 9.6 | 0.0185 | LOSES |
| Cpz | pumped | TEC | 8 | 2 | 561 | 281 | 15 | 8 | 1.2 | 0.00428 | LOSES |
| Cpz | pumped | TEC | 32 | 2 | 1,161 | 581 | 53 | 32 | 4.8 | 0.00827 | LOSES |
| Cpz | pumped | TEC | 128 | 2 | 3,561 | 1,781 | 234 | 128 | 19.2 | 0.0108 | LOSES |
| Cpz | pumped | GHEAT | 8 | 2 | 431 | 216 | 15 | 8 | 1.2 | 0.00557 | LOSES |
| Cpz | pumped | GHEAT | 32 | 2 | 1,031 | 516 | 53 | 32 | 4.8 | 0.00931 | LOSES |
| Cpz | pumped | GHEAT | 128 | 2 | 3,431 | 1,716 | 234 | 128 | 19.2 | 0.0112 | LOSES |
| Cpz | pumped | TRACK | 8 | 2 | 394 | 197 | 15 | 8 | 1.2 | 0.00609 | LOSES |
| Cpz | pumped | TRACK | 32 | 2 | 994 | 497 | 53 | 32 | 4.8 | 0.00966 | LOSES |
| Cpz | pumped | TRACK | 128 | 2 | 3,394 | 1,697 | 234 | 128 | 19.2 | 0.0113 | LOSES |
| Cpcm | passive | TEC | 8 | 2 | 181 | 90.5 | 4 | 4 | 0.6 | 0.00663 | LOSES |
| Cpcm | passive | TEC | 32 | 2 | 181 | 90.5 | 16 | 16 | 2.4 | 0.0265 | LOSES |
| Cpcm | passive | TEC | 128 | 2 | 181 | 90.5 | 74 | 64 | 9.6 | 0.106 | LOSES |
| Cpcm | passive | GHEAT | 8 | 2 | 51 | 25.5 | 4 | 4 | 0.6 | 0.0235 | LOSES |
| Cpcm | passive | GHEAT | 32 | 2 | 51 | 25.5 | 16 | 16 | 2.4 | 0.0941 | LOSES |
| Cpcm | passive | GHEAT | 128 | 2 | 51 | 25.5 | 74 | 64 | 9.6 | 0.376 | LOSES |
| Cpcm | pumped | TEC | 8 | 2 | 497 | 249 | 15 | 8 | 1.2 | 0.00483 | LOSES |
| Cpcm | pumped | TEC | 32 | 2 | 905 | 453 | 53 | 32 | 4.8 | 0.0106 | LOSES |
| Cpcm | pumped | TEC | 128 | 2 | 2,537 | 1,269 | 234 | 128 | 19.2 | 0.0151 | LOSES |
| Cpcm | pumped | GHEAT | 8 | 2 | 367 | 184 | 15 | 8 | 1.2 | 0.00654 | LOSES |
| Cpcm | pumped | GHEAT | 32 | 2 | 775 | 388 | 53 | 32 | 4.8 | 0.0124 | LOSES |
| Cpcm | pumped | GHEAT | 128 | 2 | 2,407 | 1,204 | 234 | 128 | 19.2 | 0.016 | LOSES |
| hybrid | passive | TEC | 8 | 2 | 213 | 107 | 4 | 4 | 0.6 | 0.00563 | LOSES |
| hybrid | passive | TEC | 32 | 2 | 213 | 107 | 16 | 16 | 2.4 | 0.0225 | LOSES |
| hybrid | passive | TEC | 128 | 2 | 213 | 107 | 74 | 64 | 9.6 | 0.0901 | LOSES |
| hybrid | passive | GHEAT | 8 | 2 | 83 | 41.5 | 4 | 4 | 0.6 | 0.0145 | LOSES |
| hybrid | passive | GHEAT | 32 | 2 | 83 | 41.5 | 16 | 16 | 2.4 | 0.0578 | LOSES |
| hybrid | passive | GHEAT | 128 | 2 | 83 | 41.5 | 74 | 64 | 9.6 | 0.231 | LOSES |
| hybrid | pumped | TEC | 8 | 2 | 529 | 265 | 15 | 8 | 1.2 | 0.00454 | LOSES |
| hybrid | pumped | TEC | 32 | 2 | 937 | 469 | 53 | 32 | 4.8 | 0.0102 | LOSES |
| hybrid | pumped | TEC | 128 | 2 | 2,569 | 1,285 | 234 | 128 | 19.2 | 0.0149 | LOSES |
| hybrid | pumped | GHEAT | 8 | 2 | 399 | 200 | 15 | 8 | 1.2 | 0.00601 | LOSES |
| hybrid | pumped | GHEAT | 32 | 2 | 807 | 404 | 53 | 32 | 4.8 | 0.0119 | LOSES |
| hybrid | pumped | GHEAT | 128 | 2 | 2,439 | 1,220 | 234 | 128 | 19.2 | 0.0157 | LOSES |

(Rows below 2 GS/s omitted unless they clear — a fixed-power device only gets worse at lower rates.)

## 6. Verdicts (PR-20 §20.5)

**Kill gate (OPT, class C, T_r = 1000 s, best reachable taps):** maximum ratio = **0.64** at Cpcm/passive/GHEAT, N = 128, 2 GS/s, 64 taps (P = 10 mW → 5 pJ/sample vs digital 3.2 pJ/sample). **Kill fires: True.**

**CONS product window (N_taps ≥ 16, all rows charged):** maximum ratio = **0.38** at Cpcm/passive/GHEAT, N = 128, 2 GS/s, 64 taps. **Window exists: False.**

**Sensitivity re-statement (UNSOURCED rows removed: TEC-only drift, C-pz hold at the frozen 2 mW/ch at both corners; e_tap at the band ends):**

| corner | e_tap [pJ] | max ratio (class C) | at |
|---|---|---|---|
| OPT | 0.03 | 0.03 | Cpcm/pumped/TEC, N=128, 2 GS/s, 128 taps |
| OPT | 0.25 | 0.23 | Cpcm/pumped/TEC, N=128, 2 GS/s, 128 taps |
| CONS | 0.03 | 0.02 | Cpcm/passive/TEC, N=128, 2 GS/s, 64 taps |
| CONS | 0.25 | 0.18 | Cpcm/passive/TEC, N=128, 2 GS/s, 64 taps |

