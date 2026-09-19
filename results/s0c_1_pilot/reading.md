# PR-23-P exploratory local pilot

Cost: €0 cloud; runtime 2.72 s.
Pre-run commit: `b7ca3b47689b99cfb7aac62e999e0e98cbed3013`.

| Seed | Method | Initial NMSE | Final NMSE | Matching FIR taps |
|---|---|---:|---:|---:|
| 11 | BPTT_oracle | 0.866270 | 0.645368 | 4 |
| 11 | SPSA | 0.866270 | 0.785430 | 2 |
| 22 | BPTT_oracle | 0.861853 | 0.550660 | 5 |
| 22 | SPSA | 0.861853 | 0.731210 | 3 |
| 33 | BPTT_oracle | 0.843692 | 0.550521 | 5 |
| 33 | SPSA | 0.843692 | 0.776127 | 2 |

Scalar/delay-only best NMSE: 0.868623.
Largest task/response loss or gradient discrepancy: 5.55e-16.

STOP paid expansion of equivalent-objective comparison; drift protocol not run.

No physical training, PAT, drift test, SER comparison, or energy advantage is established.
FIR lengths are noiseless, cyclic, and channel-specific; they do not validate the PR-22 eta assumption.
A fitted receiver scalar removes attenuation for this noiseless check; it cannot restore SNR in hardware.
BPTT has exact plant gradients and is an oracle, not a feasible calibration algorithm.
The equivalence is between objectives with identical information and estimators, not every possible learning/control method.


Interpretation: NMSE remains 0.55–0.79, so these are poor fits. The small matching
FIR lengths reflect those errors, not the best attainable capacity of eight rings.
The fixed initialization/delay and short untuned search limit optimization; no
confidence interval, convergence claim or hardware ceiling is inferred. FIR delay
is optimized across all cyclic shifts whereas each ring run freezes its selected
receiver delay. No independent noisy test set or symbol-error experiment was run.
