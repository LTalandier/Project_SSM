#!/usr/bin/env python3
"""Pack, verify, or restore the paper's result inputs (standard library only).

Pack is maintainer-only: it snapshots existing local outputs, never runs experiments.
Verify is read-only. Restore refuses to overwrite different local files.
"""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'paper/repro/results.tar.gz'
MANIFEST = ROOT / 'paper/repro/manifest.json'
EXTENSIONS = {'.json', '.npy', '.md'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pack():
    paths = sorted(p for p in (ROOT / 'results').rglob('*')
                   if p.is_file() and (p.suffix in EXTENSIONS
                       or (p.parent == ROOT / 'results/s0_13/states' and p.suffix == '.pt')
                       or p == ROOT / 'results/s0_13/source_bundle.tar.gz'))
    if not paths:
        raise SystemExit('No local result files to archive')
    entries = []
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    with ARCHIVE.open('wb') as raw, gzip.GzipFile(fileobj=raw, mode='wb', mtime=0, filename='') as gz:
        with tarfile.open(fileobj=gz, mode='w') as tar:
            for path in paths:
                data = path.read_bytes()
                name = path.relative_to(ROOT).as_posix()
                info = tarfile.TarInfo(name)
                info.size = len(data)
                info.mode = 0o644
                tar.addfile(info, io.BytesIO(data))
                entries.append({'path': name, 'bytes': len(data), 'sha256': digest(data)})
    manifest = {
        'schema': 'paper-results.v1',
        'historical_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'scope': 'Local JSON/NPY/Markdown results plus S0.13 states/source bundle; includes historical invalid runs. See supplementary N7/N8.',
        'archive_sha256': digest(ARCHIVE.read_bytes()),
        'files': entries,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Packed {len(entries)} files, {ARCHIVE.stat().st_size:,} compressed bytes')


def verify(restore=False):
    manifest = json.loads(MANIFEST.read_text())
    if digest(ARCHIVE.read_bytes()) != manifest['archive_sha256']:
        raise SystemExit('Archive checksum mismatch')
    expected = {e['path']: e for e in manifest['files']}
    if len(expected) != len(manifest['files']):
        raise SystemExit('Duplicate manifest path')
    payloads = {}
    with tarfile.open(ARCHIVE, 'r:gz') as tar:
        for member in tar:
            path = Path(member.name)
            if (not member.isfile() or path.is_absolute() or '..' in path.parts
                    or not path.parts or path.parts[0] != 'results'
                    or member.name in payloads or member.name not in expected):
                raise SystemExit(f'Invalid archive member: {member.name}')
            data = tar.extractfile(member).read()
            row = expected[member.name]
            if len(data) != row['bytes'] or digest(data) != row['sha256']:
                raise SystemExit(f'Checksum mismatch: {member.name}')
            payloads[member.name] = data
    if payloads.keys() != expected.keys():
        raise SystemExit('Archive/manifest membership mismatch')
    if restore:
        # Preflight every destination before writing any files.
        for name, data in payloads.items():
            path = ROOT / name
            if path.resolve() != path or any(p.is_symlink() for p in path.parents):
                raise SystemExit(f'Refusing symlink destination: {name}')
            if path.exists() and path.read_bytes() != data:
                raise SystemExit(f'Refusing to overwrite different local result: {name}')
        for name, data in payloads.items():
            path = ROOT / name
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
    print(f'{"Restored/verified" if restore else "Verified"} {len(payloads)} result files')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['pack', 'verify', 'restore'])
    args = parser.parse_args()
    if args.action == 'pack':
        pack()
    else:
        verify(restore=args.action == 'restore')
