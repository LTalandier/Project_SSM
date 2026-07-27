# NEW (P1 finalization, 2026-07-27) — render paper/p1_manuscript.md to
# paper/p1_manuscript.html (print-styled, MathJax). PDF is then produced by
# headless Chromium:
#   chromium --headless --print-to-pdf=paper/p1_manuscript.pdf \
#       --virtual-time-budget=30000 file://$PWD/paper/p1_manuscript.html
# Math spans ($...$) are shielded from the markdown converter and restored
# verbatim for MathJax.

from __future__ import annotations

import os
import re

import markdown

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "paper", "p1_manuscript.md")
OUT = os.path.join(ROOT, "paper", "p1_manuscript.html")

CSS = """
@page { size: A4; margin: 22mm 20mm; }
body { font-family: 'STIX Two Text', 'Times New Roman', Georgia, serif;
       font-size: 10.5pt; line-height: 1.45; color: #111;
       max-width: 17cm; margin: 0 auto; }
h1 { font-size: 17pt; line-height: 1.25; margin: 0 0 4pt; }
h2 { font-size: 13pt; margin-top: 18pt; border-bottom: 0.5pt solid #999;
     padding-bottom: 2pt; }
h3 { font-size: 11pt; margin-top: 12pt; }
p  { text-align: justify; margin: 6pt 0; }
blockquote { margin: 8pt 18pt; padding: 6pt 10pt; background: #f4f4f4;
             border-left: 3pt solid #555; }
img { max-width: 100%; display: block; margin: 10pt auto 4pt; }
table { border-collapse: collapse; font-size: 9pt; margin: 8pt auto; }
th, td { border: 0.5pt solid #888; padding: 3pt 6pt; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 9pt; }
ol li, ul li { margin: 3pt 0; }
h2, h3 { page-break-after: avoid; }
img, blockquote { page-break-inside: avoid; }
"""

MATHJAX = """
<script>
MathJax = { tex: { inlineMath: [['$', '$']], displayMath: [['$$', '$$']] } };
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
"""


def main():
    with open(SRC) as fh:
        text = fh.read()

    # shield math from the markdown converter
    stash = []

    def shield(m):
        stash.append(m.group(0))
        return f"MATH{len(stash)-1}"

    text = re.sub(r"\$\$.+?\$\$", shield, text, flags=re.S)
    text = re.sub(r"\$[^$\n]+\$", shield, text)

    html = markdown.markdown(text, extensions=["tables", "smarty"])

    def restore(m):
        return stash[int(m.group(1))]

    html = re.sub("MATH(\\d+)", restore, html)

    page = (f"<!doctype html><html><head><meta charset='utf-8'>"
            f"<title>P1 manuscript</title><style>{CSS}</style>{MATHJAX}"
            f"</head><body>{html}</body></html>")
    with open(OUT, "w") as fh:
        fh.write(page)
    print("wrote", OUT, f"({len(stash)} math spans shielded)")


if __name__ == "__main__":
    main()
