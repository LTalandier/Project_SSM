# Project_SSM — current handoff

Updated 2026-09-13 following the repository audit and user-authorized repairs.
This snapshot supersedes the stale July S0.4 onboarding state. Frozen methods and
post-run corrections remain in `shared/preregistration.md`; history is in Git.

## State and conclusions

- Stage 0 simulation study is complete through S0.12; P1 source is under `paper/`.
- Stage 0b is CLOSED at S0b.0: PR-20 frozen at ee137c4, result at 8931d6c.
  Best E_digital/E_photonic = 0.64, bar 3; 0.23 without unsourced optimistic rows;
  conservative product window maximum 0.38. No later Stage 0b runs or wafer spend.
- User authorized the audit repairs: PAT command binding fixed and regression-tested;
  higher-mismatch comparisons withdrawn, not rerun. m=1 and drift results unaffected
  by this defect. N8 is the authoritative result-disposition explanation.
- Full training-energy claims withdrawn: optical pass time is not wall time.
  Component costs remain. PR-20's maintenance estimate inherits this lower bound;
  missing nonnegative costs cannot reverse its negative gate at fixed cadence.
- P1 now includes the negative inline follow-up. P5 is a local companion draft.
  Product hardware development and higher-rate exploration are paused.

## Reproduction and development

Run `python3 -m pytest -q` (169 tests at this revision).
`paper/repro/README.md` documents the checksum-verified results archive and figure
rebuild commands. Old m>1 mismatch and invalid-scale records are retained as
historical evidence. Do not resume repaired experiments into those paths; no
corrected higher-mismatch experiment exists yet.

The same session implemented and reviewed these repairs; no independent review
is claimed. The single-session coordination mode remains in force. Existing
critic/executor launch instructions are historical, not active tasks.

## Remaining release work

Final scientific/source review, venue formatting, and release/licensing decisions
remain. Public submission, repo visibility changes, and the P2 author email have
not been performed. A future higher-rate study requires a concrete workload,
collaborator, and new registration. A corrected high-mismatch experiment would
require distinct outputs and explicit source-version provenance; withdrawal is
the current manuscript disposition.
