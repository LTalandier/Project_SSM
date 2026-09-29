# P1 supplementary material

**Status:** submission preparation, 2026-09-13 (single-session review disclosed in §8.4).
**Contents at submission:** (N1) the pre-registration ledger, (N2) the per-method hardware
ledger, (N3) the white-space search dossier, (N4) the registration→run provenance table,
(N5) reproducibility statement, (N6) S-figures, (N7) eval-F erratum audit,
(N8) repository audit and correction history, (N9) extended notes to the condensed main text.

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
registered for the final pre-submission sweep). Those reads were performed on 2026-07-27 (page-read
memo), and `docs/s0_L/source_refresh_2026-09-13.md` completes the dated record: it checks Zhang,
Ashtiani, Van Assche, Rukh, and Dacha against primary full texts and records the last bounded
search before deposit, run on 2026-09-13. These dossiers are included as ancillary records.

## N4 — Registration and run provenance

The repository `Project_SSM` (branch `main`) is released publicly at
`github.com/LTalandier/Project_SSM` with this preprint. The OpenTimestamps anchor is
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
| PR-20 inline envelope (Stage 0b S0b.0) | `ee137c4` | results `8931d6c` (kill gate fired) |
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
The revised suite had 174 tests at the correction and has 181 at deposit. The checksum-verified reproduction archive now
includes the corrected run records, trained states, and exact source bundle.

## N6 — Supplementary figures

| S-fig | content | source |
|---|---|---|
| S1 | G3 anchor dossier: official-code EigenWorms validation trajectories (published seeds) + final test accuracy vs published 95.0±4.4 (rerun mean 90.56, population SD 8.35; corrected 2026-09-29, N9.8) | `results/s0_2/gate_i/xcheck_official/` |
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

- ✅ **Condensed for the first public deposit 2026-09-29:** main text ~15,700 → ~8,700 words,
  captions and abstract tightened; moved detail collected in N9 keyed by section; §8.3 + Figure S1
  aligned with the 2026-09-20 P2 audit (population SD, mechanism not assigned as cause, Heartbeat
  attributed to the port). Long form at `a508a28`.

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

## N9 — Extended notes to the main text

The main text was condensed on 2026-09-29 for the first public deposit. Detail removed from it is
kept here, keyed to the section it supports. No claim, number, rule or verdict was changed by the
condensation except the corrections listed in N9.8. The full-length text remains in the repository
history at commit `a508a28`.

### N9.1 Mapping (§2)

**Validation, three levels, all thresholds pre-specified.** (i) By construction: uncoupled system
poles match the coupled-mode reference to $<10^{-3}$ and discrete $|z|$ to $<10^{-9}$. (ii) In the
continuous-wave limit: the dynamical model's steady state recovers independently derived static
transfer functions with error scaling as $O(1/\mathcal{F})$, measured $4.5\times10^{-4}$ at
$\mathcal{F} = 1048$ and $4.4\times10^{-5}$ at $\mathcal{F} = 10473$; the registry rings sit at
$\mathcal{F} \approx 10^3$–$1.5\times10^4$. (iii) In the time domain: against an independent RK45
integration, ringdown matches the closed form to $<10^{-9}$, and both pole coordinates ($\kappa$,
$\delta$) re-fitted from the trajectory recover the set values to $<10^{-5}$. All three are
internal checks of one model class.

**Memory and readout.** The maximum amplitude memory $1/\kappa_i$ is twice the photon-energy
lifetime, a convention used throughout. The 3.29–49.4 ns range is a 15× span. The readout–memory
product is bounded by the passive memory length (tested); the same Pareto shape holds at the
class-leading corner with the memory axis scaled ~15×. The operating point is pre-registered (PR-4).

**Backscatter conventions.** The doublet criterion $2\gamma \gtrsim \kappa_\mathrm{tot}$ is the
conservative half-width criterion; the full-width criterion shifts every crossover by ×2 without
changing the conclusion. For the damascene-class process, $2\gamma/\kappa_i \approx 0.5$ at the
foundry corner, with the single-pole picture breaking at $Q \approx 4\times10^6$ (half-width) or
$8\times10^6$ (full-width). The subtractive-process source tabulates average doublet separations of
180–320 MHz depending on etch mask; under the standard $2\gamma$-separation convention these are
modal-coupling rates $\gamma/2\pi \approx 90$–$160$ MHz; the damascene and subtractive sources were
page-verified on 2026-07-12. No single
published SiN crossover exists and no $\gamma$ is published for the specific target processes, so
the assembled crossover curve brackets published data points. Two consequences: a platform tension
(the highest-Q platforms are the most splitting-prone, while the splitting-safe low-Q foundry corner
is memory-poor), and a coupling between the $\kappa_\mathrm{ext}$ policy and splitting risk, since
overcoupling suppresses the visible doublet and the deep-undercoupled maximum-memory regime is the
most exposed.

### N9.2 Substrate (§3)

**Gain validation.** A one-off rate-equation integrator (M2) validated the quasi-static M1 reduction
at the gating cells.

**Noise-figure history.** The program's debt register originally carried "no measured NF for the
flagship Er:Si₃N₄ device" as verification debt #3. The S0.3-0 substrate reconnaissance (2026-06-10)
found that premise false, NF-A = 7.0 dB was frozen to match the measurement, and the value was
re-verified at page level on 2026-07-12.

**Doublet ratios.** At the C-2 initialization, $2\gamma/\kappa_\text{net} \approx 2.4$. At the
lasing-floor calibration point ($\kappa_\text{net} = 0.05\,\kappa_i$) the ratio reaches
$\gamma/\kappa_\text{net} = 16.6$. An earlier draft quoted the floor ratio at the initialization.

**Box and budget checks.** The K4 box was verified to map into the realizable pole region at every
cell. The drive budget $E_0$ is invariant ($1.000000$) under the four-tap input map.

**Input-map resolution.** Two protocol rulings were made during resolution, both strengthening the
gate and both adopted before the finalists were evaluated: the gate references the
*maximum-gradient* ring, because the registered ring-1 reference is gameable when ring 1 is untapped,
and robustness binds on the minimum over five drive seeds, because single-seed margins at the gate
boundary flicker by a factor of ~20. The registered starting guess {1, 9, 17, 25} was not the
winner (28 of 32 rings; its worst ring sat seven hops from a tap), and the best three-tap set
reached 24 of 32.

**Anchor risk (vii), endpoint measurement (PR-18; S0.11).** Under the δ-aware hypothetical, three
of eight SPSA seeds end with at least one ring in the super-threshold corner (minimum
$\kappa_\text{net} = -0.06\,\kappa_i$; rings at $r = 0.17$–$0.22$ with
$|\delta| = 0.65$–$1.0\,\kappa_i$). PAT's endpoints stay sub-threshold ($+0.31\,\kappa_i$ at achieved
detunings), and both §6 arms sit far from the corner ($\geq +1.3\,\kappa_i$). The exposure lives in
the hypothetical, not the runs: the as-built substrate is δ-independent in gain and never lases,
and the measured doublet quench (§3.4) suggests the single-pole build-up the hypothetical assumes
is pessimistic. Mid-training trajectories were not stored, so the measurement binds endpoints only.

### N9.3 Echo sub-model (§4.5)

The penalty chain is: extraction through the ring ports
($\eta_\text{ex} = 2\kappa_\text{ext}/\kappa_\text{net} = 0.86$ at θ₀); single-pass spiral
conversion ($(\gamma_\text{nl} P_p L)^2 \approx -16.7$ dB at 0.3 W pump and 0.5 m); and timing decay,
together −22.4 dB per conjugation. The assumed $\gamma_\text{nl} \approx 0.97\,\text{W}^{-1}
\text{m}^{-1}$ corresponds to a tighter-confinement spiral than the published ultra-low-loss
demonstrations at 0.29–0.51 W⁻¹m⁻¹, which also showed continuous-wave power handling to 7 W. The
direction only strengthens §5.4, and the idealized-conjugator control shows the conclusion does not
hinge on the chain. The parametric quantum floor, with pump-transfer excess included, was measured
negligible at the $10^5$-photon state scale. Off-chip conjugation was priced and excluded: the
state decays in transit (amplitude survival 0.12–0.54 at 10 ns for C-1/C-2), and there is no
storage primitive to wait out a conjugator. The echo of a noisy forward pass must not recover the
noiseless state, and a test enforces this.

### N9.4 Reference, target and ranking (§5.1–§5.3)

**Freeze order.** The fairness contract, cost metric and mismatch families (PR-6/7/5) froze at the
start of S0.4; the target rule, statistical plan and gate semantics (PR-3/8/9) at S0.4-close; the
budget and reference as dated addenda before any contestant ran.

**Reference scope.** The matched-budget diagnostic (PR-17 §17.8) found BPTT still improving past
the bake-off budget, so no asymptotic-capacity claim is made. At eval-F the §5.5 follow-up arms land
slightly below the 12,000-update reference ($8.4$–$9.0\times10^{-4}$ vs $9.8\times10^{-4}$; paired
inversion CI $[-0.1, +3.1]\times10^{-4}$, including zero). The matched reference at 31,600 updates,
registered with its expected direction stated in advance, lands at $8.1\times10^{-4}$ (8 seeds,
per-seed $7.3$–$8.9\times10^{-4}$). The restoration of the expected ordering is median-level and
thin: the matched reference sits $0.3$–$0.9\times10^{-4}$ below the calibration-sweep arms and one
per-seed resolution unit below the drift arm's time-integrated $8.2\times10^{-4}$, with overlapping
per-seed spreads. It is a scope statement, not a separation. An arm below the 12,000-update number
reflects budget, not a physical estimator beating exact gradients.

**Target and budget.** The additive guard of the target rule dominates at a floor-level reference,
by design (PR-3 §B). "Convergence" in the budget definition means the sizing pilot's registered
flatness rule on the coarse trace, a budget-local criterion; the matched run kept improving at the
fine floor past that point.

**Readout-only baseline.** Its $2.2\times10^{-2}$ is scored at the coarse protocol; at ~85 errors
per 3,840-symbol evaluation it sits far from the quantization floor, so eval-F cannot move it
materially.

**Adjoint−PAT interval.** Passes-to-target lives on a 1,600-pass evaluation grid (PR-3's
no-interpolation rule). The eight paired differences fall between $+33{,}600$ and $+36{,}800$,
positive on 8/8 seeds, and a bootstrap over values that concentrated collapses onto the grid, so the
interval's point estimate sits on its own lower bound. PAT's 505,600 digital passes are counted over
the full budget, whereas its device-pass column is to target, so the two columns are not a ratio.

### N9.5 Drift verdict provenance (§5.5)

**Why the re-lock is not a strawman.** It is the strongest response available without per-ring
observability; any per-ring re-trim requires per-ring on-device measurement and actuation feedback,
which is the in-situ stack by another name. The registered arms are the two coherent extremes.

**Why the coarse-to-fine change is not post hoc.** The eval-F drift numbers come from re-executing
the frozen S0.9b unit specifications, and the re-executed trajectories are bit-identical to the
originals: the dynamics are deterministic given the registered seed, and evaluation draws only from
reserved streams never touched by training. The coarse evaluation set is the first 2 of the fine
protocol's 52 batches, a strict subsample, so the coarse reading was underpowered rather than
contradicted. The evaluation-independent device-state fingerprint matches the stored originals on
all 64 drift units, as did the coarse final SER on all 80 historical calibration-sweep units before
the S0.13 correction (ledger §17.8). The ordering is dated: the decision rule froze before any drift
datum existed (PR-16, 2026-07-22/24), and the below-bar coarse estimate was on record when the fine
protocol was registered (PR-17, commit `241204a`, 2026-07-27, before any eval-F measurement; the
same commit froze the rule that both protocols are reported wherever they differ). The finer
floor cuts both ways: at the m=1 calibration point it erased a coarse-floor difference in the
in-situ arm's favor.

**Context-only arms.** The in-situ SPSA arm is plotted for context only. Its per-step
re-convergence transient, and within eval-F a registered per-step scale re-measure convention that
penalizes an arm whose couplings move during the step, inflate its early trajectory; no registered
verdict involves it. The deploy-time $\mathrm{SER}(t{=}0)$ diagnostic of the in-situ arms shares
that convention and is used in no comparison.

**Calibration sweep correction.** The bounded correction protocol (`bda989f`) added 32 fresh PAT
units at m = {2, 3, 4, 6} over all eight original seeds with unchanged budgets and PR-17
evaluation; 40 unchanged offline units and eight PAT m=1 units were reused, and an extra m=1
seed-11 anchor reproduced every coarse evaluation, final SER and pass ledger exactly. Results are
at `174558c`. Coarse intervals are positive at 5–20% and touch zero at 30%. Full audit in N8.

### N9.6 Structure at the solutions, damping and memory tasks (§5.7, §6)

**Reproductions.** PR-18 reproduced the winning routes' and both §6 arms' converged solutions
bit-identically (32/32 seed-runs eval-trace-exact) before re-running the gates.

**Profiles.** Driven-ring medians are $r = 1.29$ (PAT) and $1.32$ (SPSA). Undriven rings sit at
median $r \approx 0.30$ against $r_0 = 0.3$ (within-band SD 0.05–0.07); the whole-profile
$\mathrm{sd}(r) \approx 0.33$ reported in S0.11 is carried almost entirely by the four-tap
excursion. "Same structure" is a claim about the two winning routes: the §6 boxed arm shares the
shape but its undriven rings float to $r \approx 0.7$ (operating $\kappa_\text{net} \approx
1.5\kappa_i$), keeping 30 of 32 rings above the gate (worst $2.3\times10^{-4}$; the two residual
dark rings sit at segment midpoints). The uniform pin at $r^* = 2.0$ trains to $1.3\times10^{-3}$
with 20 of 32 rings above the gate: rings 6–9, 15–18 and 24–27 go gradient-dark (worst ratio
$5\times10^{-7}$), and the trained couplings do not rescue them (converged $\mu$ median exactly at
its $0.3\kappa_i$ initialization; no link past $0.35\kappa_i$). This is a second reading of the
×2.5 gap between the best pin and the trained boxes. Settled-amplitude participation decouples from
gradient reach at the solutions ({8, 15, 22} of 32 above {10⁻¹, 10⁻², 10⁻³}, against {4, 26, 32}
at θ₀); the gradient gate is the trainability-relevant quantity.

**Follow-ups.** In the output-participation ablation a registered head-refit row recovers none of
the zeroed readouts. In the taps-only control the restricted arm is not the full one truncated: its
taps compensate asymmetrically ($r \approx \{1.52, 1.30, 0.74, 1.34\}$, seed-consistent) against the
full arm's near-uniform ≈1.3. At 3,840 symbols the taps-only arm reads two symbols better; eval-F
resolves the true ordering.

**Optimum.** The fixed-gain estimate of $\kappa_\text{net}$ at $r^* = 2.0$ is $4.1\kappa_i$; the
measured value at the converged solutions is $3.7\kappa_i$.

**Spread-spectrum probe (PR-19; S0.12).** Decisions integrate 31 chips, far beyond the 8-lag head's
reach. At the frozen SNR the task's integration gain leaves every grid point at zero error; even
$r = 3$, whose ~5-sample memory the mechanism said should be fatal, clears on partial-correlation
margin (ledger §19.6b). At zero error the gradients vanish early and freeze the parameters, and
every arm ends essentially at its initialization (taps ≈ 0.34, interior ≈ 0.30; eight seeds plus
the pilot), where the equalization task drove its taps to ≈ 1.3. A task solved at initialization
induces nothing, so this is not a second, independent instance of structure discovery. The
damping-tracks-memory hypothesis stands at zero for two genuine tests, with the equalization task
the observation that generated it rather than a test of it.

### N9.7 Systems envelope (§7)

**Excluded costs, bounded.** From the primary-sourced exclusions ledger: hybrid-laser wall-plug
0.2–0.6 W at mW-class on-chip power, TEC hold 0.18 W, microcontroller-class control 0.13 W and
FPGA-class locking up to ~10 W, totalling of order 0.5–1 W for the integrated class. The 1480/980 nm
pump for the substrate's $g = 0.9\,\kappa_i$ erbium stage was missing from the original exclusion
list and was added at the Stage-0b re-envelope: 0.8–17 mW electrical per ring near transparency
(derived), hence 26–550 mW at N = 32 and more at N = 128. Charging these would compress the positive
cells' margin toward single digits.

**Block-level envelope.** Conversion cost is N-independent while digital cost scales with N, the
structural effect the architecture relied on. The expected-value holding sensitivity, under which
the optimistic corner clears in-window, is reported alongside the worst-case convention. One
boundary cell, the DSP-class comparison at N = 32, clears by ~1% and is treated as a tie.

**Edge-GPU deflator.** Measured batch-1 GRU throughput of 1.9 and 3.5 GOp/s against claimed peaks
of 0.5 and 0.8 TOp/s on two Jetson-class devices (ratios ≈263× and ≈229×), with the source's own
conclusion stating "a factor of over 100X" (page-verified). The Orin DLA path falls back to the GPU
for recurrent layers.

**The degenerate long-memory measurement.** PR-19 recorded $N_\text{eff} = 4$ on every seed, with a
head-refit recovering the target from as few as 3 rings. At the frozen 28 dB the task's ~16-chip
integration gain leaves the damping grid error-free, so the ablation count measures task slack, not
utilization, and is uninformative in either direction. The pre-written no-rise text asserted the
concentration reading and is withdrawn by ledger amendment §19.6c. The one informative
$N_\text{eff}$ measurement remains the 6–8 of §5.7.

**PR-20 provenance and arithmetic.** Frozen at `ee137c4` before calculation; results at `8931d6c`.
The frozen minimum-damping model gives a pumped-to-passive memory ratio of
$(1+2r_{\min})/(0.1+2r_{\min})=3.14$ at $r_{\min}=0.1606$, so removing gain does not give a tenfold
reduction at this operating point. Quadratic rate scaling holds only while usable tap count grows in
proportion to rate; finite tap-grid limits and task capacity interrupt it. The S0.13 correction
repairs P1 evidence and does not reopen Stage 0b. The ledger and results are in `docs/s0b/` and
`results/s0b_0/`.

### N9.8 Review record and this revision (§8.4)

**Repository visibility.** The repository was first published on 2026-08-02 and set private on
2026-08-04 for the PI's content review; it is public again from the date of this deposit. The
OpenTimestamps proof `timestamps/head_2026-08-05.txt.ots` was committed before the external review
recorded below.

**Seven post-assembly review rounds, 2026-08-01 to 2026-08-17.** The first five found six errata —
control-cell numbers transplanted into headline contexts, a cross-scope ratio, a protocol-mixing
claim — all in unregistered connective prose, none touching a pre-registered number, rule or
verdict. The seventh found a pre-written consumption text (PR-19's no-rise branch), drafted for an
informative outcome, applied verbatim to a floor-degenerate one; it overstated the paper's caveat
rather than its claim, and it is withdrawn by ledger amendment §19.6c, with same-root instances in
prose and stale figure annotations corrected alongside. The discipline's seams — connective prose,
outcome branches its texts did not anticipate, and derived artifacts — are named from measurement.

**2026-09-13 audit.** See N8.

**This revision (2026-09-29).** The main text was condensed from about 15,700 to about 8,700 words
by moving the material above out of it. Two corrections were made at the same time, both aligning
P1 with the evidence audit of the separate LinOSS note (2026-09-20). §8.3 and Figure S1 now report
the EigenWorms rerun's population standard deviation, 8.35 percentage points, the convention of the
published 95.0 ± 4.4 (the earlier 9.34 was a sample standard deviation). They no longer attribute
the lower scores to the zero-gradient mechanism, which an archived screen of the official code does
not support. §8.3 also attributes the Heartbeat reproduction to our port of the model and describes
the gate's adjudication as purpose-served with the anchor void, without restating an instability
reason the five runs cannot establish. One sentence was added to §9.1 pointing to a later,
separately registered exploration of a low-Q ring regime (Stage 0c; PR-22, PR-23 in the ledger),
which found no validated energy window and is not part of this paper's results. An independent
read-only comparison of the old and new text was run before the build; the caveats it found
missing from the condensed main text were restored. The S1
generator was corrected accordingly; no other figure changed.
