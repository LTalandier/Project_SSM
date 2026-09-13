# Repository audit repairs — 2026-09-13

User authorized repairs following the repository review and the Stage 0b closure.
No new training runs, paid compute, external release, or email were performed.

## Changes

- PAT binds all command-map errors at the requested mismatch scale. Regression
  covers values and Jacobians at m=0,1,2,6, with separate estimator levels isolated.
- Historical m>1 mismatch comparisons are withdrawn rather than silently relabeled.
  Base-scale bake-off and drift results are unaffected by this specific defect.
  F8 omits higher-level points. N8 and the appended post-run ledger erratum explain
  the defect, impact, correction, and absence of corrected runs.
- P1 includes the negative PR-20 inline-envelope result. Ratio direction, 3.14 memory
  ratio, and fixed-tap rate scaling are corrected. No frozen inputs or gates changed.
- Optical sequence time is labeled as a duration lower bound. Total training energy
  and total-energy ranking claims are withdrawn pending writes/settling/control costs.
- P5 companion note drafted locally. Hardware and higher-rate continuation paused.
- Sweep persistence uses same-directory temporary files plus atomic replacement.
  Legacy list-form records load correctly; malformed payloads fail explicitly.
- Reproduction bundle contains 991 local JSON/NPY/Markdown result files with SHA-256
  manifest; README and handoff now reflect current state. Dependencies used for
  validation are recorded, including the manuscript rendering dependency.

## Validation

- `python3 -m pytest -q`: **169 passed**, two pre-existing multiprocessing fork warnings.
- `python3 scripts/reproduce_paper.py verify`: all 991 records verified.
- Results-free checkout: restore followed by both figure generators and manuscript
  assembly reproduces **all 12 PNGs and the manuscript byte-for-byte**.
- Repeated restore succeeds; a conflicting local result is rejected and preserved.
- Final F8 label and provenance edits were rebuilt and compared in the isolated checkout.
- PDF regenerated using headless Chromium after MathJax and fonts finished loading:
  **337 math containers and 12 successfully loaded images**. Extracted PDF text
  includes the withdrawals, optical-time correction, and PR-20 conclusion.
- `git diff --check`: clean. No independent scientific review is claimed.

## Remaining limits

Higher-mismatch results remain withdrawn until distinct, versioned reruns are
performed. Full timing/energy and higher-rate trainability remain unmeasured.
P5 source verification and publication bibliography, venue formatting, licensing,
and final release review remain before any submission. The result archive supports
figure reconstruction, not a full recreation of external benchmark datasets/cloud
training environments. The repair changes are local; no commit, push, publication,
repository visibility change, or author email was made by this session.
