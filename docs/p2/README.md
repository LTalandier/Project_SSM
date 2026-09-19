# P2 audit bundle

The working note is `paper/p2_eigenworms_note.md`. The author-contact draft is
`paper/p2_author_email.md`; no contact has occurred. The September audit corrects
unsupported claims in the July draft; the original remains in Git history.

Extract `paper/p2_evidence.zip` into an empty directory and, from its root, run:

```bash
python3 -m analysis.p2_audit
```

The audit requires Python, NumPy and PyTorch. It recomputes descriptive statistics
from archived arrays, classifies the official local screens, recomputes exact-zero
gradient suffixes from the port's per-step traces, and runs a small float32 loss
probe. It does not rerun LinOSS training or download data. New probe metadata will
reflect the reviewer's local PyTorch version. Historical evidence hashes can be
checked against `results/p2_audit/audit.json`; the ZIP also has a complete
`bundle_manifest.json`. The frozen official source is supplied for inspection,
not as a complete installable upstream environment.

The evidence bundle includes all inputs actually read by `analysis/p2_audit.py`,
the two analysis scripts, the source-refresh memo, licenses, and working note.
Training reproduction still requires the original upstream repository, dataset
preprocessing, pinned dependencies and an explicitly captured execution environment.
The historical GPU driver/JAX CUDA versions were not recovered.

Build the attachment from this repository with `python3 scripts/build_p2_bundle.py`.
No cloud compute is used. Dataset subject-level examples are not included.
