# Project_SSM — current handoff

Updated 2026-09-13 after the user-authorized bounded correction rerun and P1
submission preparation. This supersedes earlier onboarding and active-run notes.

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
- Hardware and higher-rate exploration stay paused. Standalone P5 publication is
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

The workspace has no authenticated arXiv session. Actual author submission,
license selection, arXiv-generated PDF review, and the linked submission-day
repository visibility change remain. Do not claim an arXiv ID or public-release
date before they exist. No P2 email is automatically authorized by this handoff.

Execution and review remain in one session; tests and commits are not an
independent scientific review. Old critic/executor instructions are historical.
