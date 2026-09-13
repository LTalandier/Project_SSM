# S0.13 — bounded correction of the PAT mismatch sweep

Approved by Lucas ("okay let's do this"), 2026-09-13, following the recommendation
for one corrected comparison before P1 submission. This is a post-result bug-fix
rerun, not a newly blinded experiment. It does not change PR-5 §E or PR-17 thresholds.

## Fixed scope

- Corrected code: PAT command binding in `04c67a6`, now scales the detuning offset
  and both coupling maps as well as the constructor's intrinsic-loss/backscatter.
- Fresh PAT-both: C-2, m={2,3,4,6}, seeds {11,23,47,61,83,101,127,151}: 32 runs.
- One full PAT m=1 seed-11 anchor: compare coarse trace and fine SER with the original;
  this is a reproducibility diagnostic, not an additional statistical replicate.
- Reuse unchanged offline-deploy records at all five m levels and PAT m=1 records.
  Original file hashes will accompany the combined analysis. No original overwritten.
- Exactly 31,600 updates; eval_every=100; original hyperparameters and float64
  harness; fresh common-per-seed data and original method noise streams; one CPU
  thread per process. No tuning, early stopping, seed replacement, or selection.
- PR-17 final fine SER at the trained normalization, 99,840 symbols. Coarse final
  median of last three evals co-reported. Stored model/head state permits evaluation
  recovery without changing the trajectory. Results at `results/s0_13/runs/`.
- PR-5 §E/PR-17 analysis unchanged: paired-by-seed bootstrap 10,000 draws, seed
  20260727, interval order statistics [249,9749], median difference offline−PAT;
  advantage iff median ratio ≥2 and difference interval lower bound >0. All five
  levels consumed in order, with m* and target failures reported. A nonsignificant
  difference is not proof of equivalence. Both possible directions disclosed.
- If the anchor differs, disclose the numerical/platform difference and determine
  whether reuse remains valid before declaring a combined result. No silently
  substituted seeds or historical runs.

## Execution and spending

Live Hetzner API queried 2026-09-13: CPX62 (16 shared x86 vCPU, 32 GiB) in fsn1
€0.24996/hour as displayed by the CLI. Four temporary servers, 8–9 single-thread
units each. Budget under €5, including billing rounding/IP overhead; three-hour
fleet deadline (about €3 server time before rounding). All owned server IDs are
logged; local supervisor retrieves results/states and deletes each completed
server. Timeout/failure also retrieves available outputs then deletes the server.
No unrelated servers are modified. Account server list was empty before launch.

Source bundle includes this pre-run committed protocol, the runner, all package
code, exact file hashes, source commit, and installed Python/Torch versions.
PyTorch version pinned to the audit environment (2.11.0+cpu); no model optimization
or compiler substitution. The local timing check (200 updates, one CPU thread)
took 10.9 s, while historical shared-cloud units took roughly 4,600 s each;
these are scheduling estimates, not scientific results. No literature claims,
new workloads, hardware, or higher-rate studies are part of this rerun.

## Publication disposition

P1 incorporates the corrected result either way and retains the N8 erratum trail.
The negative PR-20 result stays in P1; separate P5 submission is deferred. Hardware
and higher-rate work remain paused. Public release follows completion of the rerun
and source/reproduction checks; P2 author contact is a separate decision.
