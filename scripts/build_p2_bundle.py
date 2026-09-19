"""Build the self-contained measurement-audit attachment, not a training bundle."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]

def main():
    audit=json.loads((ROOT/'results/p2_audit/audit.json').read_text())
    names=set(audit['evidence_sha256'])|{
        'analysis/p2_audit.py','analysis/s0_2_1r_classify.py','results/p2_audit/audit.json',
        'paper/p2_eigenworms_note.md','docs/p2/README.md','docs/p2/source_refresh_2026-09-20.md',
        'LICENSE','LICENSING.md','paper/LICENSE-CC-BY-4.0.txt'}
    for name,digest in audit['evidence_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    manifest={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in sorted(names)}
    target=ROOT/'paper/p2_evidence.zip'
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for name in sorted(names):
            info=zipfile.ZipInfo(name,(2026,9,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16;z.writestr(info,(ROOT/name).read_bytes())
        info=zipfile.ZipInfo('bundle_manifest.json',(2026,9,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,json.dumps(manifest,indent=2)+'\n')
    (ROOT/'docs/p2/bundle_checksum.json').write_text(json.dumps({'file':str(target.relative_to(ROOT)),
        'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'members':len(names)+1,
        'purpose':'measurement audit; not full training reproduction; not sent'},indent=2)+'\n')
    print(f'Built {target}: {len(names)+1} members, {target.stat().st_size} bytes')

if __name__=='__main__': main()
