# P1 supplementary material

**Status:** submission preparation, 2026-09-13 (single-session review disclosed in §8.4).
**Contents at submission:** (N1) the pre-registration ledger, (N2) the per-method hardware
ledger, (N3) the white-space search dossier, (N4) the registration→run provenance table,
(N5) reproducibility statement, (N6) S-figures, (N7) eval-F erratum audit,
(N8) repository audit and correction history.

## N1 — Pre-registration ledger

`shared/preregistration.md`, included verbatim among the arXiv ancillary records.

Ancillary filename: `shared__preregistration.md`. Every PR-block carries its status history
(PROPOSED → AMEND → SIGNED/FROZEN) and the commit that froze it; the two S0.4-close addenda
(sizing; ceiling) are dated *before* the runs they govern. The ledger is the paper's §3.7
"ledger-as-method" object.

## N2 — Per-method hardware ledger

`docs/s0_4/f8_hardware_ledger.md`: per-route observables, actuators, added components, and
calibration burdens (SPSA simplest → RHEL heaviest); the structural note that adjoint/RHEL
cannot win promotion-rule (b) (strictly-simpler hardware) by construction.

## N3 — White-space search dossier

`docs/s0_L/debt1_whitespace_search.md` (PR-15 two-modality search + kill-criterion, 2026-06-09)
+ `docs/s0_L/whitespace_refresh_2026-07-12.md` (assembly refresh: W1 clean, W0 survives with
qualifiers load-bearing; five named near-misses dispatched in §1.1; four page-level reads
registered for the final pre-submission sweep). The 2026-07-27 page-read memo
and `docs/s0_L/source_refresh_2026-09-13.md` complete the dated record; the latter
checks Zhang, Ashtiani, Van Assche, Rukh, and Dacha against primary full texts and
records a fresh bounded search. These dossiers are included as ancillary records.

## N4 — Registration and run provenance

The repository `Project_SSM` (branch `main`) is released at
`github.com/LTalandier/Project_SSM` at submission. The OpenTimestamps anchor is
`timestamps/head_2026-08-05.txt.ots`. Public access makes the recorded commit
ordering inspectable; the timestamp establishes existence of the anchored material,
not independently verified experiment execution times.

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
| PR-16 drift advantage rule (pre-drift-run) | ledger 2026-07-22/24 | S0.9 drift runs |
| PR-17 eval-F + T-A-L spec | `241204a` | S0.10 runs `017547b` |
| PR-17 §17.7 erratum (registered pre-rerun) | `ccc4385` | corrected rerun `017547b` |
| PR-17 §17.8 decomposition + matched-reference spec | `a8d7ab9` | matched run `967429d` |
| PR-18 converged-operating-point diagnostics (S0.11) | `b585623` | stage-1 `ae1073f` / stage-2 `d108d5f` |
| PR-18 §18.6 follow-ups: taps-only control + N_eff ablation (S0.11b) | `ec2d4e3` | verdicts `21c9bb2` |
| PR-19 T-D long-coherent-memory (S0.12) | signed `e96e76c`; addenda `b55b135`/`a4e6a70` | fleet+verdicts `f7b395a`; §19.6c round-7 amendment `a28e2d2` (no-rise frame withdrawn as floor-degenerate; rule/verdict stand) |
| PAT command-binding correction (S0.13; original PR-5/PR-17 thresholds retained) | code `04c67a6`; bounded rerun protocol `bda989f` | results `174558c`; exact m=1 anchor, all 33 units complete |
| paper section drafts (post-results) | `9e8b4c4`, `db3a8c7`, `14aedff`, `77a93ca`, `436ebbf` | — |

## N5 — Reproducibility statement

All simulations are float64 PyTorch on CPU. Runs executed on a **mixed platform set** —
local x86-64 Linux and Hetzner cpx51 (shared x86-64) cloud instances — with identical code,
identical registered seeds, and per-unit idempotent runners (`analysis/s0_5_run_one.py`,
`analysis/s0_6_run_one.py`) writing one JSON per (method, cell, seed) unit; merge/statistics
stages (`analysis/s0_5_bakeoff.py`) are deterministic over the run files. Evaluation uses
reserved noise streams (`EVAL_SEED_BASE = 900001`) never drawn during training. Training
randomness is seeded per unit; eval SER at the quantization floor (2 errors / 3840 symbols)
is platform-stable. The test suite (150 tests at S0.5-close; 165 at S0.12) pins substrate
bit-identity gates (e.g. adjoint pass-2 forward identity, ledger counts). Total cloud
spend for all Stage-0 compute through S0.10, invoice-exact: 183 shared-vCPU server-hours ≈
**€70 excl. VAT (€84 incl.)**, of which ≈84 h ≈ €32 productive runs (per-phase in
`shared/results_log.md`) and ≈99 h ≈ €38 one disclosed idle-server incident. (Provider
cloud prices rose ≈3.9× for instances created after 2026-06-15; earlier in-session
estimates used the old rate.) The post-assembly PR-19 follow-up (S0.12) added ≈132
server-hours ≈ **€50 excl. VAT** (rate-exact €0.3814/h; includes one server lost to a
hang with its 12 units re-run, and an ssh-outage delay) — Stage-0 total ≈ 315 h ≈
**€120 excl. VAT (≈€145 incl.)**.

The S0.13 correction used four temporary CPX62 servers and 3.006 server-hours in
aggregate. At the retrieved rate, rounding each server up to one billed hour gives
approximately **€1 incl. VAT**, plus small IPv4 charges; this is an estimate, not an
invoice. All servers and addresses were removed after retrieval. Per-unit Python
and Torch versions, source hashes, and cleanup evidence accompany the correction.
The revised suite has 174 tests. The checksum-verified reproduction archive now
includes the corrected run records, trained states, and exact source bundle.

## N6 — Supplementary figures

| S-fig | content | source |
|---|---|---|
| S1 | G3 anchor-instability dossier: official-code EigenWorms val trajectories (published seeds, collapse events visible) + final test acc vs published 95.0±4.4 (rerun 90.56, σ 9.34) | `results/s0_2/gate_i/xcheck_official/` |
| S2 | PAT twin-mismatch decomposition at C-1 (perfect / M-par / M-struct ≡ ceiling) + rhel-ideal control | `results/s0_5/bakeoff_diag_c1.json` |
| S3 | echo conjugation-chain waterfall (−22.4 dB, mechanism A) + per-cell Q_L ceilings / transit survival (mechanisms B/C) | `results/s0_4c/pr11_recon_calc.json` |
| S4 (deferred) | PR-14 gradient bias/variance | deferred (S0.5-full) — slot reserved |
| S5 | RHEL non-dissipative-limit recovery (R1 cosine −0.75→+1.0000 vs κ_net·T·dt) | `results/s0_4c/smoke.json` |

Main-figure addendum: **F8** (S0.9 mismatch+drift, 3 panels) added 2026-07-27 alongside F1–F7;
generator `analysis/make_sfigures.py`. Namespace ruling (round-3 review): in the paper "F8"
names *only* the figure; the hardware-realism ledger is always cited as supplementary note N2 (round-4: supplementary sections renamed S→N so "S2" names only Figure S2)
(its internal finding-ID "F8" stays a docs-tree label), and internal ledger sub-labels such
as PR-5 "§F7.3" are cited as their parent PR block only.

## N7 — eval-F erratum audit (PR-17 §17.7)

The eval-F re-scoring shipped with one implementation erratum, disclosed in §5.1 and made
auditable here rather than attested. **Bug:** the fine-evaluation helper re-measured the
output normalization $y_\text{scale}$ on the *trained* device; the trained readout is
calibrated to the *training-time* normalization — head and scale are one decoder. **Signature
(before, first pass):** chance-level fine SER on exactly the arms that move
$\kappa_\text{ext}$, with coarse SER at ceiling — e.g. in-situ PAT (m=1) fine $0.667$ vs
coarse $7.8\times10^{-4}$; BPTT ceiling fine $0.742$ vs coarse $5.2\times10^{-4}$ — while
scale-consistent arms (offline-deploy; all drift units, whose registered per-step re-measure
tracks a near-unchanged device) were unaffected. **Fix:** `train()` exposes the head's trained
normalization (`y_scale` ledger key); the fine evaluation consumes it. **Gate test** (in the
released suite): evaluation at the trained scale reproduces the in-training trace evaluation
to $<10^{-12}$. **After (corrected rerun):** in-situ PAT (m=1) fine $8.5\times10^{-4}$;
BPTT ceiling fine $9.8\times10^{-4}$. **Ordering:** registration `241204a` → first pass →
erratum registered + fix committed `ccc4385` *before* the 108-unit corrected rerun → results
`017547b`; first-pass outputs quarantined in the results tree (`invalid_scalebug/`), not
overwritten. The valid-by-construction subsets (drift units; offline arms) are identical in
both passes.

## Assembly residue (tracked)

- ✅ Lucas rulings RESOLVED 2026-07-26 by delegation: **title = candidate 1**; scope initially
  W0-in-prose — **superseded 2026-07-27: W1 only** (the registered Wu eLight page read refuted
  the W0 clearance; `docs/s0_L/whitespace_page_reads_2026-07-27.md`, E-2026-07-27-1).
- ✅ The 4 registered page-level reads PERFORMED 2026-07-27 (3 clear, Wu refuted) + fresh
  June–July sweep (no new attack). **Completed 2026-09-13:** Zhang and the five named primary-paper checks,
  a bounded final search, and exclusions-source refresh; the TTX1995 row remains
  unverified and excluded from quantitative support (`docs/s0_L/source_refresh_2026-09-13.md`).
- ✅ Eval-floor + damping-transfer follow-up (PR-17, S0.10): pre-reg `241204a` → runs →
  erratum §17.7 `ccc4385` (registered before the corrected rerun) → verdicts in
  `results/s0_10/s0_10.md`; §5.5 drift advantage declared at eval-F, T-A-L prediction failed
  (reported failed).
- ✅ S0.7 exclusions ledger primary-sourced: `docs/s0_7/exclusions_ledger.md` (§7.1 states the
  integrated-class ~0.5–1 W consequence).
- ✅ [CITE-*] → numbered bibliography + assembled manuscript: `analysis/build_manuscript.py` →
  `paper/p1_manuscript.md`. XeLaTeX source and a source ZIP are generated by `analysis/build_arxiv.py`;
  journal-specific formatting remains a later step.
- ✅ Round-3 review (2026-08-01): ceiling declared protocol-local + matched-budget reference
  run (PR-17 §17.8b, drawn in Fig. F8); resolution-vs-re-draw decomposition closed by
  bit-identity (§17.8a); degenerate adjoint−PAT interval explained as grid-bound; title
  count dropped; abstract recompressed (~250 w, 3 paragraphs, Wu footnoted, ratio-CI +
  integrated-realization caveats carried); F-namespace collision resolved (figure-only F8).
- ✅ **Fifth exclusion added 2026-09-13 (Stage-0b S0b.0 retrieval):** the substrate's Er:Si₃N₄ gain pump
  was missing from §7.1's exclusion list; now listed with its derived magnitude (exclusions ledger §5;
  `docs/s0b/s0b_0_ledger.md` §2). Direction against the photonic side; no verdict changes.
- ✅ **§8.4 tense swap DONE 2026-08-02**: repo public at `github.com/LTalandier/Project_SSM`
  (E-2026-07-27-2 resolved); §8.4 states the publication in past tense with date + URL.
  **Amended 2026-09-13:** repo private since 2026-08-04 (PI content review); §8.4/N4 now say
  "public at submission" + the OTS anchor as the visibility-independent certificate; the
  past-tense date claim is withdrawn until the re-flip (then re-dated to the re-flip date).
- ✅ Round-5 walkthrough COMPLETE, clusters A–E (2026-08-04/05): PR-18 §18.1–18.5 + §18.6
  registered→run→consumed (all reproductions bit-identical); §5.7/§6 mechanism + §3.6/§8.2
  vii exposure + §9.1 Stage-1 δ-aware-clamp design input; six errata fixed (§2.2 κ_tot,
  §3.4 floor-ratio transplant, §5.7 head-only attribution, §5.3 ledger scoping, §5.5 m1
  protocol-mixing, §5.4+S5 C-1→C-2 transplant); §7.3 historical energy scope (subsequently withdrawn by N8); §18.6
  verdicts: taps-only control → A-discovers narrowly (abstract clause restored,
  "estimator-independent"); N_eff = 6–8 → §7.2 bounds its own N-scaling premise + abstract
  niche condition; §8.4 review-as-measurement sentence. OTS anchor in `timestamps/`
  (receipt upgraded 2026-09-13; local Bitcoin-node verification remains documented in `timestamps/README.md`). Candidate S-figure (converged profiles + ablation
  curves) undecided — PI call at venue-format time.
- ✅ PR-19/S0.12 (2026-08-13→17, PI-signed): T-D despread-31 fleet run + consumed —
  P0 solvable (ceiling 0.000), P1 failed by degeneracy (grid ties at zero; §6
  zero-for-three), P2 no-rise (N_eff = 4; §7.2 unsoftened restatement + burden-flip),
  §8.5 operating-point lesson. Harder-SNR T-D variant = open registration if pursued.
  Abstract NOT re-touched for S0.12 (post-assembly follow-up; §7.2/§6 carry it) — PI may
  revisit at venue-format time.
- ✅ Round-7 review (2026-08-17): PR-19's N_eff = 4 recognized as **floor-degenerate** —
  the §19.5 no-rise frame ("still concentrates") was drafted for an informative null and
  is withdrawn by ledger amendment `§19.6c` (`a28e2d2`; frozen blocks untouched — the
  first erratum inside registered prose, though not inside any number, rule, or verdict).
  §7.2 now states PR-19 is evidence-free on N_eff (the informative measurement remains
  §18.6b's 6–8); §6 inverted floor-first and re-counted zero-for-two (T-A = the
  generating observation, per §19.4-P1's own two-probes framing); §8.4 updated to seven
  rounds with the seam classes named. Same-root figure artifacts regenerated (F6 label
  ≈6 samples at measured 3.7 κᵢ; S5 in-image title C-2 ≈8; F7 caption budgeted-stack
  scope + §7.3 ‡ footnote). §5.7 undriven-band center stated (median r ≈ 0.30 = init);
  abstract niche clause carries "magnitude is unmeasured"; "ample capacity" → headroom.
  Refs [10]/[13]/[15]/[25]/[33] (Ashtiani/Zhang/Ghent-reservoir/Rukh/Dacha) were
  checked in the 2026-09-13 source refresh; the Van Assche final-publication metadata was updated.

## N8 — Repository audit erratum (2026-09-13)

**PAT mismatch scaling.** PR-5 §E required five parametric errors to scale with m.
The twin constructor scaled intrinsic loss and backscatter, but command binding
used m=1 values for detuning offset, external coupling, and inter-ring coupling.
At m=6 the command offsets/factors were 0.05 κ_i, 1.05, and 0.95 instead of
0.30 κ_i, 1.30, and 0.70. Offline deployment used the intended scaled values.
The original m>1 comparisons and the claimed tie through 30% were withdrawn.
Historical S0.9a/S0.10a files, including `runs_a_patboth`, remain unchanged in the
reproduction archive and remain invalid for those comparisons. The m=1 bake-off,
diagnostics, and separate drift results are unaffected. The corrected binding
stores each twin's scaled levels; regressions check values and command Jacobians
at m=0,1,2,6.

**Correction completed (S0.13).** Protocol `bda989f` preceded 32 fresh PAT units
at m={2,3,4,6} and all eight original seeds, plus one m=1 seed-11 anchor. Each unit
used 31,600 updates, the original hyperparameters, and PR-17 fine evaluation at the
trained normalization. All 33 units finished, with no seed replacement or tuning.
The anchor exactly reproduced all 316 coarse evaluations, coarse/fine SER, and
pass ledgers, supporting reuse of 40 unaffected offline and eight PAT m=1 records.
The anchor is not an extra statistical replicate. Source commit, versions, input
hashes, and trained-state hashes are retained. Results are recorded at `174558c`;
this is a post-result implementation repair, not a new blind registration.

`results/s0_13/analysis.json` replaces only the affected mismatch block and records
the imported S0.10 drift/reference blocks by provenance. All five fine intervals
include zero; ratios range from 0.994 to 1.053. Neither coarse nor fine evaluation
finds a registered crossover. Figure F8a now shows the corrected complete grid.
The fine result resolves no difference at the tested levels; it does not prove
equivalence. The original withdrawal and defect remain part of this audit trail.

**Energy and timing.** The reported 22.528 ms is 176,000 × 256 / (2 GS/s), the
optical sequence duration. It excludes parameter writes, settling, reset gaps,
measurement/controller latency, and holding power over those intervals. The earlier
"tens of millijoules all-in" and total-energy ranking are withdrawn. Figure F7
retains the conversion and digital-twin component budgets, explicitly labeled as
partial. Stage 0b inherited this lower-bound duration for maintenance; its negative
energy gate cannot improve when nonnegative missing costs are added at fixed cadence.

**Stage 0b interpretation.** The unchanged PR-20 result is E_digital/E_photonic =
0.64 (photonic 1.56× digital energy), or 0.23 with unsourced optimistic rows removed.
The implemented pumped/passive memory ratio at r_min=0.1606 is 3.14. Quadratic rate
scaling requires usable tap count to grow with rate; fixed-tap scaling is linear.
The higher-rate residue has no trainability evidence and remains dormant.

**Reproduction.** `paper/repro/README.md` documents the checksum-verified archive of
local result records and benchmark metric arrays, and the commands to regenerate
figures and manuscript. The archive includes invalid historical runs for audit;
their presence does not reinstate withdrawn claims. This revision was reviewed in
one session; automated tests are not an independent scientific review.
