# P1 supplementary material — assembly plan + provenance table

**Status:** S0.8 assembly, 2026-07-12 (single-session mode; disclosed in §8.4).
**Contents at submission:** (S1) the pre-registration ledger, (S2) the per-method hardware
ledger, (S3) the white-space search dossier, (S4) the registration→run provenance table,
(S5) reproducibility statement, (S6) S-figures.

## S1 — Pre-registration ledger

`shared/preregistration.md`, included verbatim. Every PR-block carries its status history
(PROPOSED → AMEND → SIGNED/FROZEN) and the commit that froze it; the two S0.4-close addenda
(sizing; ceiling) are dated *before* the runs they govern. The ledger is the paper's §3.7
"ledger-as-method" object.

## S2 — Per-method hardware ledger (F8)

`docs/s0_4/f8_hardware_ledger.md`: per-route observables, actuators, added components, and
calibration burdens (SPSA simplest → RHEL heaviest); the structural note that adjoint/RHEL
cannot win promotion-rule (b) (strictly-simpler hardware) by construction.

## S3 — White-space search dossier

`docs/s0_L/debt1_whitespace_search.md` (PR-15 two-modality search + kill-criterion, 2026-06-09)
+ `docs/s0_L/whitespace_refresh_2026-07-12.md` (assembly refresh: W1 clean, W0 survives with
qualifiers load-bearing; five named near-misses dispatched in §1.1; four page-level reads
registered for the final pre-submission sweep).

## S4 — Registration → run provenance (git, repository `Project_SSM`, branch `main`)

Rule being evidenced: **every threshold/spec commit predates the run that consumes it.**

| object | registered (commit) | consumed/measured (commit) |
|---|---|---|
| PR-1.1 G3 adjudication (v2 signed) | `f659558` → `408e082` | — (S0.2 record) |
| PR-4 substrate freeze v2 (signed) | `b1af15d` → `55746b5` | substrate build `c0b7359`/`2d0673b` |
| S0.4 packet: PR-6 v3 / PR-7 v2 / PR-5 / PR-12 (signed by delegation) | `497f790` → `73099d5` → `a3c0c21` → `cde3f4a` | S0.4-0 calibration `991aef0` |
| S0.4a spec + PR-5 mismatch levels | `0b8c817` | PAT/SPSA build+smoke `502e26e` |
| S0.4b adjoint spec (gates B1–B5) | `c85fe62` | build+smoke `ade7795` |
| PR-11 echo sub-model (proposed → verify-1 → numeric freeze) | `965680d` → `2fab8e9` → `5ca8d52` | RHEL build `b77aa60`, results `eb21520` |
| PR-3 target rule + PR-8 stats + PR-9 gates | `ae16f6d` | — |
| Sizing addendum (U_conv, B) | `7bcbcb9` | — |
| Ceiling addendum (SER_target, Δ_M3) | `4fca58d` | bake-off `15405fd`, C-1 diagnostics `ac0f1d2` |
| S0.6 damping spec (arms, grid, C7 rule) | `5a7f28b` | results `7808596` |
| S0.7 training-envelope accounting rules | `bd37703` | results `dc2d561`/`fae0512` |
| paper section drafts (post-results) | `9e8b4c4`, `db3a8c7`, `14aedff`, `77a93ca`, `436ebbf` | — |

## S5 — Reproducibility statement (draft)

All simulations are float64 PyTorch on CPU. Runs executed on a **mixed platform set** —
local x86-64 Linux and Hetzner cpx51 (shared x86-64) cloud instances — with identical code,
identical registered seeds, and per-unit idempotent runners (`analysis/s0_5_run_one.py`,
`analysis/s0_6_run_one.py`) writing one JSON per (method, cell, seed) unit; merge/statistics
stages (`analysis/s0_5_bakeoff.py`) are deterministic over the run files. Evaluation uses
reserved noise streams (`EVAL_SEED_BASE = 900001`) never drawn during training. Training
randomness is seeded per unit; eval SER at the quantization floor (2 errors / 3840 symbols)
is platform-stable. The test suite (150 tests at S0.5-close) pins substrate bit-identity
gates (e.g. adjoint pass-2 forward identity, ledger counts). Total cloud spend for all
Stage-0 compute: <€10 (disclosed per-phase in `shared/results_log.md`).

## S6 — S-figures (✅ MADE 2026-07-27, `analysis/make_sfigures.py` → `paper/figures/S*.{png,pdf}`; frozen result files only)

| S-fig | content | source |
|---|---|---|
| S1 ✅ | G3 anchor-instability dossier: official-code EigenWorms val trajectories (published seeds, collapse events visible) + final test acc vs published 95.0±4.4 (rerun 90.56, σ 9.34) | `results/s0_2/gate_i/xcheck_official/` |
| S2 ✅ | PAT twin-mismatch decomposition at C-1 (perfect / M-par / M-struct ≡ ceiling) + rhel-ideal control | `results/s0_5/bakeoff_diag_c1.json` |
| S3 ✅ | echo conjugation-chain waterfall (−22.4 dB, mechanism A) + per-cell Q_L ceilings / transit survival (mechanisms B/C) | `results/s0_4c/pr11_recon_calc.json` |
| S4 ▢ | PR-14 gradient bias/variance | deferred (S0.5-full) — slot reserved |
| S5 ✅ | RHEL non-dissipative-limit recovery (R1 cosine −0.75→+1.0000 vs κ_net·T·dt) | `results/s0_4c/smoke.json` |

Main-figure addendum: **F8** (S0.9 mismatch+drift, 3 panels) added 2026-07-27 alongside F1–F7;
generator `analysis/make_sfigures.py`. Note: figure "F8" is distinct from finding-ID F8 (the
hardware-realism ledger); prose always writes figures as "Fig. Fn".

## Assembly residue (tracked)

- ✅ Lucas rulings RESOLVED 2026-07-26 by delegation: **title = candidate 1**; scope initially
  W0-in-prose — **superseded 2026-07-27: W1 only** (the registered Wu eLight page read refuted
  the W0 clearance; `docs/s0_L/whitespace_page_reads_2026-07-27.md`, E-2026-07-27-1).
- ✅ The 4 registered page-level reads PERFORMED 2026-07-27 (3 clear, Wu refuted) + fresh
  June–July sweep (no new attack). **Still registered before submission:** Zhang eLight 6:6
  page read; one last sweep re-run (July 2026 not yet indexed); UNVERIFIED-direct rows of the
  exclusions ledger.
- ✅ Eval-floor + damping-transfer follow-up (PR-17, S0.10): pre-reg `241204a` → runs →
  erratum §17.7 `ccc4385` (registered before the corrected rerun) → verdicts in
  `results/s0_10/s0_10.md`; §5.5 drift advantage declared at eval-F, T-A-L prediction failed
  (reported failed).
- ✅ S0.7 exclusions ledger primary-sourced: `docs/s0_7/exclusions_ledger.md` (§7.1 states the
  integrated-class ~0.5–1 W consequence).
- ✅ [CITE-*] → numbered bibliography + assembled manuscript: `analysis/build_manuscript.py` →
  `paper/p1_manuscript.md`. Venue-specific formatting (LaTeX, journal template) remains.
