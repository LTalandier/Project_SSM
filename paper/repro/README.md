# Reproducing the revised paper

`results.tar.gz` contains the result JSONs, benchmark metric arrays, and memos used
by the figures. It also includes S0.13's 33 trained states and exact source bundle.
`manifest.json` records every file's SHA-256 and the archive checksum. This is a
snapshot of multiple experimental generations, not a claim that all historical
experiments were rerun with the current code. The corrections are described in N7/N8.

From a results-free checkout, install `requirements.txt`, then:

```bash
python3 scripts/reproduce_paper.py verify
python3 scripts/reproduce_paper.py restore
python3 analysis/s0_13_analyze.py
python3 analysis/make_figures.py
python3 analysis/make_sfigures.py
python3 analysis/build_manuscript.py
python3 -m pytest -q
```

Restore checks every member before writing and refuses to overwrite differing
local results. The analysis verifies the full correction grid, source revisions,
saved-state hashes, historical controls, and exact m=1 reproducibility anchor.
Figure F8 reads `results/s0_13/analysis.json`: corrected mismatch results and
explicitly retained S0.10 drift/reference blocks. All 12 figures can be rebuilt
without training. N7's `invalid_scalebug/` outputs and the original m>1 PAT outputs
remain in the archive for audit; they remain invalid evidence.

For the submission PDF and editable source:

```bash
python3 analysis/build_arxiv.py
```

See `paper/SUBMISSION.md` for Pandoc/XeLaTeX dependencies and the generated source
ZIP. The default build also updates `paper/p1_manuscript.pdf`, including the
scientific supplementary notes. HTML remains an optional preview via
`python3 analysis/render_manuscript_pdf.py`; it loads MathJax from a CDN and is not
the submission PDF route. PDF bytes depend on TeX/font versions and commit metadata;
figure PNGs and manuscript Markdown are checked separately for exact reproduction.

## Rerunning the correction experiment

This is separate from regenerating figures. Extract
`results/s0_13/source_bundle.tar.gz` into a new empty directory; it includes
`source_manifest.json`, the pinned runner, and all package code. Use Python 3.12,
PyTorch 2.11.0+cpu, and one CPU thread per process. From that directory:

```bash
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 analysis/s0_13_mismatch_rerun.py 11 2
```

The frozen grid and anchor are listed in `docs/s0_13_rerun_protocol.md`. One unit
runs 31,600 updates and then the 99,840-symbol fine evaluation; the completed run
JSON records its environment and state checksum. The runner validates the source
manifest and writes only the separate S0.13 paths. Do not resume into historical
S0.9/S0.10 directories. Stored states support fine-evaluation recovery without
retraining, but a full independent rerun must start with empty output directories.

The archive does not include the full EigenWorms dataset or its external official
code checkout; rerunning that earlier benchmark has separate prerequisites.
`environment.txt` records the local analysis environment. Historical experiment
versions and registered commits remain documented in the provenance notes.

Maintainer snapshot command, after outputs and cleanup records are final:
`python3 scripts/reproduce_paper.py pack`.
