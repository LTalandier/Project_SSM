# Project_SSM — current handoff

Updated 2026-09-20 after the P2 evidence audit and PR-23-C capacity diagnostic. This
supersedes older active-run notes. P1's validated numerical snapshot is unchanged.

## Latest work — 2026-09-20

Lucas authorized continuing P2 preparation and the bounded capacity diagnostic.
No email, deposit, hardware step, or cloud compute was executed.

**PR-23-C:** frozen in `947d877` before 36 local fits (21.60 s, €0).
All three nearby synthetic starts recover an exactly realizable response; distant
starts fail, confirming local-minimum sensitivity. Best original-range K=.05–.20
CD fit has dense normalized MSE .461321. One of 15 expanded K=.01–.95 starts
reaches .00238687; its actual K values span .3282–.9500, all above .20. This is a
constructive noiseless approximation outside the registered device window, not
a product go, BER result, or proof the narrow range cannot work. Independent
NumPy evaluation verifies the saved response. See `results/s0c_capacity/`.
Next prerequisite for any drift protocol: a credible broad-coupling actuator/loss
model and an explicit matched-observation adaptive baseline. No fleet launched.

**P2:** revised `paper/p2_eigenworms_note.md` and unsent author email. Upstream
main remains `05a8353` on retrieval. Archived five official runs give 90.5556%
with population SD 8.3518 pp; old 9.3376 was sample SD and mismatched the upstream
convention. Exact-gradient collapse cannot be assigned as the cause of this
accuracy gap. Official local screen: 0/8 strict traps. Port local annex: 2/3
finite-window zero-gradient suffixes; different protocols cannot be pooled.
GPU driver/JAX CUDA runtime and a full paired stable-loss benchmark are missing.
Do not claim definitive population dispersion, inevitable absorption, author
contact already made, or corrected-loss benchmark recovery.
Portable attachment: `paper/p2_evidence.zip`, rebuilt/checked from raw evidence;
reviewer instructions and upstream provenance in `docs/p2/`. The attachment is
a measurement audit, not a complete training reproduction package. Authors'
professional addresses verified; **email remains unsent**, no response window
started. P2 is ready for feedback, not an unconditional publication claim.

**Validation:** 179 tests pass with two existing fork deprecation warnings;
portable P2 audit reproduces in an empty directory; capacity source hashes match
the pre-run commit. P1's licensed upload files are unchanged by this research turn.

## Current Stage 0c decision

Lucas authorized the staged recommendation: €0 repairs, exploratory pilot capped
at €20, possible total ≤€100 only if justified; no hardware. PR-23-P was committed
at `b7ca3b4` before execution. The local preflight cost €0 cloud and took 2.72 s.
All 179 tests pass (two existing fork deprecation warnings).

- PR-22's stored 64-GS/s ratio is 2.0411, not 1.25. The 100-GS/s 3.1892 ratio
  drops to 1.0631 with the cheaper digital comparator at fixed photonic cost.
- Athermal source loss is 0.4 dB/cm, not the bare-SiN 0.051. Gain/noise/idle,
  platform co-integration and measured FIR equivalence remain missing. There is
  no validated product window; original PR-22 results remain historical evidence.
- Exact ring model validated against an independent round-trip recurrence and
  gradient finite differences. In the 8-ring, 64-GBd, 20-km noiseless pilot, BPTT
  NMSE is .551–.645; SPSA .731–.785; poor fits, not useful link performance.
- Task waveform-MSE and response-fit objectives/gradients agree within 5.55e-16
  under identical full-field information. **Stop paid expansion of that comparison.**
  This is not evidence that every adaptive method is equivalent, nor a hardware
  capacity bound. No PAT/drift/measurement-budget comparison has been run.
- A future drift experiment needs a separately frozen observation/noise/actuator
  model and adaptive identification-and-synthesis baseline. No fleet or hardware
  was provisioned. Do not treat the remaining budget as a mandate to spend.
- Shi's full preprint + SI establishes an adaptive response-control baseline;
  Zhao main text and APF full article still have access gaps. No priority claim.

Evidence: `docs/s0c/audit_2026-09-19.md`, `results/s0c_audit/`,
`results/s0c_1_pilot/`. Reproduce with `python3 -m analysis.s0c_audit` and
`python3 -m analysis.s0c_1_pilot` (a rerun records its new execution revision).


## Current result and decisions

- S0.13 completed: 32 corrected higher-mismatch PAT units plus one m=1 seed-11
  anchor; 48 unchanged historical controls reused. The anchor exactly matches its
  316-point trace, coarse/fine SER, and ledgers. Protocol `bda989f`, result `174558c`.
- All five fine mismatch intervals include zero; offline/PAT ratios 0.994–1.053.
  No registered advantage/crossover under either evaluation protocol. This does
  not establish equivalence. Old invalid m>1 PAT files remain withdrawn.
- P1 incorporates the correction and the PR-20 negative inline envelope. Stage 0b
  stays closed: best E_digital/E_photonic 0.64, versus the 3× bar; 0.23 excluding
  unsourced optimistic rows; conservative product window maximum 0.38.
- Total training energy remains unmeasured. Optical sequence time excludes control,
  settling, and idle costs. Conversion/digital-twin component budgets remain.
- Hardware and paid higher-rate exploration stay paused after the local preflight. Standalone P5 publication is
  deferred; P2 author contact is separate. No emails have been sent by this session.

## Execution and reproduction

All 33 correction units succeeded without tuning, replacement seeds, or early
stopping. Four CPX62 servers used 3.006 aggregate server-hours; approximately €1
including VAT with per-node hour rounding, plus small IPv4 costs (not an invoice).
All servers and primary addresses were removed. Evidence: `results/s0_13/`.

The archive under `paper/repro/` includes raw corrected records, trained states,
source bundle, hashes, and historical evidence. `paper/repro/README.md` separates
figure regeneration from training. `analysis/s0_13_analyze.py` rejects incomplete
or inconsistent evidence. F8 uses the corrected summary, with unchanged drift and
reference blocks explicitly identified. The suite has 174 tests.

## Submission state

P1 source, a PDF with scientific supplementary notes, ASCII metadata abstract,
and an arXiv source ZIP are prepared; see `paper/SUBMISSION.md`. The local
XeLaTeX export checks embedded fonts and missing glyphs. Primary-source refresh:
`docs/s0_L/source_refresh_2026-09-13.md`.

The original OTS receipt is upgraded with completed attestations; local full
verification needs a Bitcoin RPC node (`timestamps/README.md`). This older anchor
does not cover S0.13 or independently establish experimental execution times.

Lucas now proposes Zenodo for immediate public deposit instead of waiting for an
arXiv endorser. `paper/zenodo/DEPOSIT.md` contains metadata and links to the two
validated upload files; `checksums.json` verifies the P1 snapshot and ZIP members.
The ZIP includes the result archive. Lucas confirmed CC BY 4.0 for the paper
and MIT for code; both are applied, included in the rebuilt PDF/source ZIP, and
described in `LICENSING.md`. Numerical archives are unchanged. No authenticated
Zenodo connector is available, no record/DOI has been created, and no publication
or repository visibility change occurred. The arXiv draft remains optional later.
Complete the public repository release alongside the eventual deposit, consistent
with the manuscript. No P2 email is automatically authorized by this handoff.

Execution and review remain in one session; tests and commits are not an
independent scientific review. Old critic/executor instructions are historical.
