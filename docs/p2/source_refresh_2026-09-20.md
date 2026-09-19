# P2 source and claim audit — 2026-09-20

Fetched official repository `https://github.com/tk-rusch/linoss.git` into an isolated
read-only checkout. Main head: `05a835355439ee5500b2c8f891132c53adf020c0`, dated
2026-03-01, identical to the historical reference. Snapshots in `upstream/` retain
Konstantin Rusch's MIT license. Mapping: `LinOSS.py` comes from `models/LinOSS.py`;
`EigenWorms.json` from `experiment_configs/repeats/LinOSS/EigenWorms.json`; the other
files retain their upstream paths relative to the repository root.

Verified directly: train.py probability-space epsilon loss; model softmax output;
postprocess_results.py default population SD; original five seeds/configuration.
This is a source-code refresh, not a new full benchmark run. Do not generalize
its status to the authors' separate Discretax library.

Primary paper: https://arxiv.org/html/2410.03943v3 (Table 1, Appendix B).
Published EigenWorms IM number: 95.0 ± 4.4; reported hardware includes V100 and
RTX 4090, with A100 for PPG. No exact per-seed EigenWorms hardware provenance
was found. The paper also already discusses initialization sensitivity elsewhere;
our note should not claim to discover seed sensitivity in general.

Corrections to the July P2 draft:

1. Compare ddof=0 with ddof=0: rerun SD 8.3518, not the sample SD 9.3376.
2. Separate the official rerun's lower accuracy from the loss-saturation mechanism.
   No archived evidence establishes that exact absorption caused those five scores.
3. Official local fresh-eight screen is 0/8 strict traps; exclude the unarchived
   GPU fresh-eight count, Fisher comparisons, and unsupported incidence ranges.
4. Port local annex has two observed zero-gradient suffixes in three diagnostic
   runs, not proof of an inescapable state under every possible future input.
5. Stable log-softmax has the expected gradient in a numerical probe; no paired
   full benchmark recovery is established. Remove unsupported confidence in that.
6. Author contact never occurred. Remove the past-tense contact claim.
7. GPU model is RTX 3090; the driver and JAX CUDA runtime remain unrecorded.
8. `steps.npy` is a scheduled-step vector, not proof of executed training length.

Contact addresses checked on primary professional pages (draft only):
- T. Konstantin Rusch: tkrusch@tue.ellis.eu — https://camail.org/konstantin-rusch/
- Daniela Rus: rus@csail.mit.edu — https://www.csail.mit.edu/person/daniela-rus

No email was sent and no external issue or publication was created.
