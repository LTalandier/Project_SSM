# NEW (P1 finalization, 2026-07-27) — deterministic manuscript assembler.
# Concatenates title + abstract + paper/sections/01..09 + figure captions into
# paper/p1_manuscript.md, converting [CITE-*] keys to a numbered bibliography
# resolved from paper/references.md. Section status headers (process metadata
# between the H1 and the first ---) are stripped; everything else passes
# through verbatim. Re-run after any section edit; the output file is generated,
# never hand-edited.

from __future__ import annotations

import glob
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PAPER = os.path.join(ROOT, "paper")

TITLE = ("Can a photonic state-space model be trained on-chip? "
         "A pre-registered in-situ-training bake-off on a realistic "
         "silicon-nitride ring substrate")
AUTHOR = "Lucas Talandier — independent researcher, Paris"

SECTIONS = ["01_intro.md", "02_mapping.md", "03_substrate.md",
            "04_methods.md", "05_results.md", "06_damping.md",
            "07_envelope.md", "08_limits.md", "09_outlook.md"]


def read(rel):
    with open(os.path.join(PAPER, rel)) as fh:
        return fh.read()


# ---------------------------------------------------------------- references
def parse_references():
    """references.md table -> {lowercased key -> (canonical, ref_text)}."""
    alias_map, refs = {}, {}
    for line in read("references.md").splitlines():
        if not line.startswith("| CITE-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        keys = [k.strip() for k in cells[0].split("/")]
        canonical = keys[0]
        refs[canonical] = cells[1]
        for k in keys:
            alias_map[k.lower()] = canonical
    return alias_map, refs


# ---------------------------------------------------------------- sections
def strip_header(text, fname):
    """Keep the H1, drop the status block up to and incl. the first ---."""
    lines = text.splitlines()
    m = re.match(r"^# §(\d+) — (.*)$", lines[0])
    if not m:
        sys.exit(f"{fname}: unexpected H1 {lines[0]!r}")
    head = f"## {m.group(1)}. {m.group(2)}"
    try:
        cut = next(i for i, l in enumerate(lines) if l.strip() == "---")
    except StopIteration:
        sys.exit(f"{fname}: no --- after status header")
    body = "\n".join(lines[cut + 1:]).strip()
    # demote all remaining headings one level (## 1.1 -> ### 1.1)
    body = re.sub(r"(?m)^(#{2,})", r"#\1", body)
    return head + "\n\n" + body


# ---------------------------------------------------------------- abstract
def extract_abstract():
    """Blockquote under '## Draft abstract'; bare '>' lines are paragraph
    breaks (the round-3 abstract is multi-paragraph + footnote)."""
    lines = read("outline.md").splitlines()
    i = next(i for i, l in enumerate(lines)
             if l.startswith("## Draft abstract"))
    paras, cur = [], []
    for l in lines[i + 1:]:
        if l.startswith("> "):
            cur.append(l[2:])
        elif l.strip() == ">":
            if cur:
                paras.append(" ".join(cur))
                cur = []
        elif cur or paras:
            break
    if cur:
        paras.append(" ".join(cur))
    return "\n\n".join(paras)


# ---------------------------------------------------------------- captions
def figure_section():
    text = read("figure_captions.md")
    # drop the status header (everything before the first ---)
    text = text.split("---", 1)[1].strip()
    text = text.replace("\n---\n", "\n")
    out = []
    files = {os.path.basename(p).split("_")[0]: os.path.basename(p)
             for p in glob.glob(os.path.join(PAPER, "figures", "*.png"))}
    for para in text.split("\n\n"):
        m = re.match(r"\*\*Figure ([FS]\d+) —", para.strip())
        if m and m.group(1) in files:
            out.append(f"![{m.group(1)}](figures/{files[m.group(1)]})")
        out.append(para.strip())
    return "## Figures\n\n" + "\n\n".join(p for p in out if p)


# ---------------------------------------------------------------- build
def main():
    alias_map, refs = parse_references()
    body_parts = [strip_header(read(os.path.join("sections", f)), f)
                  for f in SECTIONS]
    abstract = extract_abstract()
    SENTINEL = "\n\nABSXXBODYSPLIT\n\n"
    full = abstract + SENTINEL + "\n\n".join(body_parts)

    order, missing = [], set()

    def resolve(key):
        canon = alias_map.get(key.strip().lower())
        if canon is None:
            missing.add(key.strip())
            return None
        if canon not in order:
            order.append(canon)
        return order.index(canon) + 1

    def repl(m):
        nums = [resolve(k) for k in re.split(r"[;,]", m.group(1))]
        if any(n is None for n in nums):
            return m.group(0)  # leave unresolved keys visible
        return "[" + ", ".join(str(n) for n in nums) + "]"

    full = re.sub(r"\[((?:CITE-[A-Za-z0-9-]+)(?:\s*[;,]\s*CITE-[A-Za-z0-9-]+)*)\]",
                  repl, full)

    bib = "\n".join(f"{i+1}. {refs[k]}" for i, k in enumerate(order))
    abstract_numbered, body_numbered = (s.strip()
                                       for s in full.split("ABSXXBODYSPLIT"))
    manuscript = "\n\n".join([
        f"# {TITLE}",
        f"*{AUTHOR}*",
        f"**Abstract.** {abstract_numbered}",
        body_numbered,
        figure_section(),
        "## References",
        bib,
    ]) + "\n"

    out = os.path.join(PAPER, "p1_manuscript.md")
    with open(out, "w") as fh:
        fh.write(manuscript)

    print(f"wrote {out}")
    print(f"references used: {len(order)}")
    unused = sorted(set(refs) - set(order))
    if unused:
        print("table entries not cited:", ", ".join(unused))
    if missing:
        print("!! UNRESOLVED KEYS:", ", ".join(sorted(missing)))
    leftover = re.findall(r"CITE-[A-Za-z0-9-]+", manuscript)
    if leftover:
        print("!! leftover CITE tokens:", sorted(set(leftover)))
    for glyph in ("▢", "⚠", "[REF-"):
        if glyph in manuscript:
            print(f"!! process marker {glyph!r} present in manuscript")


if __name__ == "__main__":
    main()
