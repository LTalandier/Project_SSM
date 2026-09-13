# S0.13 execution and cleanup

Protocol committed before launch: bda989f. Source hashes are in source_manifest.json;
source_bundle.tar.gz preserves the exact shipped code. All 33 units completed,
without seed replacement, tuning, or early stopping. All 33 saved-state checksums
were verified before analysis. The m=1 anchor exactly matches the historical full
316-point evaluation trace, coarse/fine SER, and pass ledgers.

Four CPX62 fsn1 nodes, Python 3.12, PyTorch 2.11.0+cpu, one CPU thread per process.
Per-unit version metadata is in the run JSONs. Read-only py-spy samples on two
nodes inspected iteration counters for progress; they did not alter training
settings or consume intermediate accuracy for decisions. NumPy was not installed
on the workers; Torch's startup warning did not affect this torch-only harness.

Fleet lifetime summed across nodes: 3.005723 server-hours. Provider quote
(price_quote.json): EUR 0.2083 net / 0.24996 gross per hour. Prorated server cost
is EUR 0.7513 gross; rounding each server to a whole billed hour gives
EUR 0.99984 gross, plus small IPv4 charges.
This is an estimate, not an invoice. It is within the under-EUR-5 cap.

All four servers were deleted after successful retrieval; the provider API then
reported zero servers and zero primary IPs (cleanup.json). No resources remain.
Node tarballs are local transport backups; the reproduction archive preserves the
run JSONs, trained states, source bundle, manifests, analysis, and this memo.
