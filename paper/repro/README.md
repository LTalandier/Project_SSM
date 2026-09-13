# Reproducing the revised paper

`results.tar.gz` contains the local JSON result records, NumPy benchmark metric
arrays, and result memos needed to rebuild the figures. `manifest.json` records
SHA-256 checksums for every file and the archive. This is a data snapshot, not a
claim that every experiment was rerun with the repaired code. The historical
source commit is recorded in the manifest; the corrections are described in N8.

From a clean checkout, with the Python dependencies installed:

```bash
python3 scripts/reproduce_paper.py verify
python3 scripts/reproduce_paper.py restore
python3 analysis/make_figures.py
python3 analysis/make_sfigures.py
python3 analysis/build_manuscript.py
python3 analysis/render_manuscript_pdf.py
python3 -m pytest -q
```

Restore verifies every member before writing, and refuses to replace differing
local results. The figure commands read the historical data; they do not train
models. F8 includes only the unaffected m=1 mismatch point and the drift panels.
N7's `invalid_scalebug/` outputs and N8's higher-mismatch records are retained for
audit. Neither is valid evidence for the withdrawn claims. Do not resume repaired
mismatch experiments into old output directories: idempotent runners would skip
historical files. Any future rerun needs a new directory and source-version record.

HTML rendering needs the `Markdown` dependency. It currently loads MathJax from a
CDN, so browser PDF rendering needs access to that resource. The checked-in PDF is
a convenience output, not byte-for-byte reproducible: browser, font, and PDF metadata
versions affect it. For PDF, print the HTML with Chromium after MathJax has finished.

This bundle reproduces figures from stored results. It does not include the full
EigenWorms dataset, external official-code checkout, or cloud provisioning state
needed to rerun training. Those are separate requirements described by the existing
`scripts/` and `photonic_ssm/linoss/` code. Runtime dependencies are not yet locked;
`environment.txt` records the environment used for this revision's checks.

Maintainer snapshot command (after auditing local outputs):
`python3 scripts/reproduce_paper.py pack`.
