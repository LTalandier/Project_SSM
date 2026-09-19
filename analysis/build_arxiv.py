#!/usr/bin/env python3
"""Build editable XeLaTeX, an outline-font PDF, and an arXiv source ZIP.

Requires Pandoc 3.9, XeLaTeX (TeX Live 2023+), and Poppler pdffonts.
The ZIP contains only main.tex, its figures, and supporting ancillary records.
Compilation happens in a temporary directory; no TeX intermediates are published.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'paper'


def supplementary():
    text = (PAPER / 'supplementary.md').read_text()
    # Keep the scientific notes and audit trail, omit the editorial task history.
    text = re.sub(r'(?ms)^## Assembly residue \(tracked\).*?(?=^## N8)', '', text)
    text = text[text.index('## N1'):]
    return '\n\n\\clearpage\n\n# Supplementary notes\n\n' + text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pandoc', help='Pandoc executable (otherwise discover PATH or pypandoc_binary)')
    parser.add_argument('--output-dir', type=Path, default=PAPER / 'submission')
    args = parser.parse_args()
    if args.pandoc is None:
        args.pandoc = shutil.which('pandoc')
        if args.pandoc is None:
            try:
                import pypandoc
                args.pandoc = pypandoc.get_pandoc_path()
            except (ImportError, OSError):
                raise SystemExit('Install Pandoc or pypandoc_binary==1.17, or pass --pandoc.')
    version = subprocess.check_output([args.pandoc, '--version'], text=True).splitlines()[0]
    epoch = subprocess.check_output(['git', 'show', '-s', '--format=%ct', 'HEAD'], cwd=ROOT, text=True).strip()
    env = dict(os.environ, SOURCE_DATE_EPOCH=epoch, FORCE_SOURCE_DATE='1')
    with tempfile.TemporaryDirectory(prefix='ssm-arxiv-') as folder:
        work = Path(folder)
        source = (PAPER / 'p1_manuscript.md').read_text() + supplementary()
        (work / 'manuscript.md').write_text(source)
        figure_names = re.findall(r'!\[[^\]]*\]\((figures/[^)]+)\)', source)
        for name in figure_names:
            dest = work / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(PAPER / name, dest)
        cmd = [args.pandoc, 'manuscript.md', '--from=markdown', '--standalone',
               '--pdf-engine=xelatex', '-V', 'geometry:margin=20mm', '-V', 'fontsize=10pt',
               '-V', 'mainfont:lmroman10-regular.otf',
               '-V', 'mainfontoptions:BoldFont=lmroman10-bold.otf',
               '-V', 'mainfontoptions:ItalicFont=lmroman10-italic.otf',
               '-V', 'mainfontoptions:BoldItalicFont=lmroman10-bolditalic.otf',
               '-V', 'mathfont:latinmodern-math.otf', '-V', 'monofont:lmmono10-regular.otf',
               '-V', 'monofontoptions:BoldFont=lmmonolt10-bold.otf',
               '-V', 'monofontoptions:ItalicFont=lmmono10-italic.otf',
               '-H', str(PAPER / 'tex/header.tex'), '-o', 'main.tex']
        subprocess.run(cmd, cwd=work, check=True)
        for _ in range(2):
            run = subprocess.run(['xelatex', '-interaction=nonstopmode', '-halt-on-error', 'main.tex'],
                                 cwd=work, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if run.returncode:
                raise SystemExit(run.stdout[-5000:])
        log = (work / 'main.log').read_text()
        if 'Missing character:' in log or 'LaTeX Font Warning:' in log:
            raise SystemExit('Missing glyph/font in PDF; inspect source before publishing.\n' + log[-5000:])
        fonts = subprocess.check_output(['pdffonts', 'main.pdf'], cwd=work, text=True)
        if 'Type 3' in fonts or any(' no ' in line for line in fonts.splitlines()[2:]):
            raise SystemExit('PDF font audit failed:\n' + fonts)
        ancillary = ['shared/preregistration.md', 'docs/s0_4/f8_hardware_ledger.md',
                     'docs/s0_7/exclusions_ledger.md', 'docs/s0_13_rerun_protocol.md',
                     'docs/s0b/s0b_0_ledger.md', 'paper/repro/README.md',
                     'timestamps/head_2026-08-05.txt', 'timestamps/head_2026-08-05.txt.ots',
                     'timestamps/README.md',
                     'paper/repro/manifest.json', 'paper/repro/results.tar.gz']
        ancillary += [str(p.relative_to(ROOT)) for p in sorted((ROOT / 'docs/s0_L').glob('*.md'))]
        for name in ancillary:
            dest = work / 'anc' / name.replace('/', '__')
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, dest)
        (work / 'anc/README.txt').write_text(
            'Supporting records for P1. Double underscores in filenames replace repository slashes.\n'
            'The pre-registration ledger and literature dossiers are preserved verbatim.\n'
            'The results archive contains historical invalid records as disclosed in notes N7/N8.\n'
            'Code and full path layout: https://github.com/LTalandier/Project_SSM\n')
        for name, dest_name in [('LICENSE', 'LICENSE.txt'),
                                ('LICENSING.md', 'LICENSING.md'),
                                ('paper/LICENSE-CC-BY-4.0.txt', 'LICENSE-CC-BY-4.0.txt')]:
            shutil.copyfile(ROOT / name, work / dest_name)
        upload = [work / n for n in ['LICENSE.txt', 'LICENSING.md', 'LICENSE-CC-BY-4.0.txt']] + [work / 'main.tex'] + [work / n for n in sorted(set(figure_names))] + sorted((work / 'anc').glob('*'))
        out = args.output_dir.resolve()
        out.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(out / 'p1_arxiv_source.zip', 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for p in upload:
                info = zipfile.ZipInfo(p.relative_to(work).as_posix(), (2026, 9, 13, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, p.read_bytes())
        shutil.copyfile(work / 'main.tex', out / 'main.tex')
        shutil.copyfile(work / 'main.pdf', out / 'p1_with_supplement.pdf')
        if out == (PAPER / 'submission').resolve():
            shutil.copyfile(work / 'main.pdf', PAPER / 'p1_manuscript.pdf')
        (out / 'build_report.json').write_text(json.dumps({
            'pandoc': version, 'source_date_epoch': epoch, 'fonts': fonts,
            'overfull_boxes': re.findall(r'Overfull[^\n]+', log),
            'files': {p.relative_to(work).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in upload},
            'zip_sha256': hashlib.sha256((out / 'p1_arxiv_source.zip').read_bytes()).hexdigest(),
        }, indent=2) + '\n')
        print(f'Built {out}: {len(upload)} source/figure/ancillary files; fonts embedded, no missing glyphs.')
        print(f'Overfull boxes: {len(re.findall("Overfull", log))}')


if __name__ == '__main__':
    main()
