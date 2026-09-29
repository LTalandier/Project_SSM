# P1 submission preparation

**2026-09-29: published on Zenodo, DOI 10.5281/zenodo.23041523 (<https://zenodo.org/records/23041523>),** from the condensed build
recorded in `submission/verification.json`. The arXiv notes below remain for a possible later
submission.

**2026-09-19 route update:** Lucas proposed a Zenodo public preprint deposit to
avoid the immediate arXiv endorsement dependency. Copy-ready metadata and links
to the verified PDF + source ZIP are in [`zenodo/DEPOSIT.md`](zenodo/DEPOSIT.md).
Licenses are applied: CC BY 4.0 for the paper and MIT for code. No deposit/DOI
exists yet; the actual account upload remains.
The arXiv instructions below remain available for later use.

The correction sweep is complete (`174558c`): the anchor matches exactly, all
33 units completed, and no tested mismatch level clears the advantage rule. Standalone P5 publication is deferred, with the negative
inline result retained in P1. P2 contact is a separate action.

## Files and build

The maintained sources are `outline.md`, `sections/`, `references.md`,
`figure_captions.md`, and `supplementary.md`. Rebuild the manuscript after editing:

```bash
python3 analysis/build_manuscript.py
python3 analysis/build_arxiv.py
```

The second command needs Pandoc (tested 3.9; available through
`python3 -m pip install pypandoc_binary==1.17`), XeLaTeX with TeX Live packages
(tested Ubuntu `texlive-xetex` 2023), and Poppler `pdffonts`. The Python script
also accepts `--pandoc /path/to/pandoc` and `--output-dir /path/to/output`.
The source ZIP compiles directly with XeLaTeX; Pandoc is not needed by arXiv.
All fonts are selected by filename from standard Latin Modern packages.

Outputs under `paper/submission/`:

- `p1_with_supplement.pdf` (also copied to `paper/p1_manuscript.pdf` by the default build):
  main manuscript, figures, references, and scientific
  supplementary notes. Editorial assembly history stays in the repository.
- `p1_arxiv_source.zip`: `main.tex`, 12 PNG figures, and `anc/` supporting records.
  License texts and component coverage are included at the ZIP root.
  No intermediate TeX files or prebuilt PDF are included in the upload ZIP.
- `main.tex`: editable generated source, with figure paths relative to the ZIP root.
- `build_report.json`: source-file checksums, fonts, layout warnings, and ZIP hash.

The PDF build rejects missing characters, font substitutions, Type 3 fonts, and
unembedded fonts. Layout warnings are recorded for visual review. Source ZIP bytes
are deterministic for identical inputs. PDF metadata uses the current commit's
SOURCE_DATE_EPOCH; a different TeX installation can still produce different bytes.

## Verified release checks

`submission/verification.json` records the checks. For the condensed 2026-09-29 revision
(28 pages): 181 tests pass, the result archive verifies, the extracted ZIP compiles standalone,
and only Figure S1 changed among the figures. The earlier release checks: 174 tests pass; the
1,065-file result archive verifies; a results-free clone reproduces all 12 PNG
figures, the manuscript Markdown, and the corrected analysis JSON exactly. The
extracted upload ZIP compiles by itself with XeLaTeX and passes font/glyph/layout
checks. The corrected table, Figure F8, and N8 PDF pages were visually inspected.

## arXiv entry

Title: Can a photonic state-space model be trained on-chip? A pre-registered
in-situ-training bake-off on a realistic silicon-nitride ring substrate

Author: Lucas Talandier (independent researcher, Paris)

Suggested primary category: `physics.optics`. Comments: 28 pages, 12 figures;
includes supplementary notes and ancillary reproducibility records. No journal reference or DOI exists
for P1. `arxiv_abstract.txt` contains ASCII metadata text under 1,920 characters;
it is an abridgement of the manuscript abstract.

Use the source ZIP with compiler **XeLaTeX**, inspect arXiv's compiled PDF, and
complete the author account's submission and license selection. This workspace
has no authenticated arXiv session. No submission receipt or public arXiv ID is
claimed. The repository remains private until the agreed submission-day release.
Record the actual release date and submission receipt after those actions happen.
P2 is not an automatic email task in this preparation workflow.

Official requirements checked 2026-09-13:
[TeX submission](https://info.arxiv.org/help/submit_tex.html),
[TeX Live and XeLaTeX](https://info.arxiv.org/help/faq/texlive.html),
[ancillary records](https://info.arxiv.org/help/ancillary_files.html), and
[ASCII metadata and abstract length](https://info.arxiv.org/help/prep.html).
