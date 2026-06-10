# Pre-declaration — S0.2-1R G3 record repair (GA-F1): regenerated diagnostic screens

**Committed BEFORE any declared run executes** (task gate). Date: 2026-06-11. Executor.
Scope: diagnostic record repair only — zero gated numbers touched, zero tuning, zero
gated reruns. The frozen protocol (PR-1 v2) is not exercised by anything below.

## A. Official fresh-seed leg (GA-F1a)

- **Seeds (n = 8, fixed):** 7890, 8901, 9012, 11111, 22222, 33333, 44444, 55555.
  Includes 9012 and 22222 (continuity with the destroyed-box console observations, per the
  task spec). To the session's best record this is the same set the box ran, but the box
  list is not recoverable from the synced archive (`driver_fresh.log` is an empty warning
  header — the GA-F1 finding), so the list is declared fresh here and **this declaration is
  the operative one**.
- **Code:** official repo tk-rusch/linoss @ `05a8353`, **zero source edits**.
- **Environment:** the pinned local CPU venv (`/tmp/linoss_venv`): jax 0.4.28 / jaxlib
  0.4.28 / equinox 0.11.4 / optax 0.2.2 / numpy 1.26.4 (+ diffrax 0.5.1, signax 0.1.1,
  lineax 0.0.5 added for runner imports; load-bearing pins re-verified after install).
  CPU: AMD Ryzen AI 9 365, 20 threads. No GPU.
- **Data:** the official pickles (`data.pkl` / `labels.pkl` / `original_idxs.pkl`) produced
  by the official `process_uea.py` at S0.2-1 (sha-recorded in the S0.2-1 entry), symlinked
  into the official repo's expected `data_dir/processed/UEA` path.
- **Runner:** the official `run_experiments(["LinOSS"], ["EigenWorms"], <config_dir>)` —
  their seed loop, their training loop, their saving.
- **Config** (`config/LinOSS/EigenWorms.json`, committed here): a copy of the official
  `experiment_configs/repeats/LinOSS/EigenWorms.json` with **exactly three fields
  changed**: (1) `seeds` → the declared 8; (2) `num_steps` 100000 → **4000** (screen
  depth, §C); (3) `output_parent_dir` `""` → this archive directory (trails land
  in-place). All other fields byte-identical.
- This is a **diagnostic screen**, not a gated run and not a rerun of the gated statistic:
  it regenerates the **trap-incidence estimate (k/n)** with archived trails. Full-run final
  accuracies are **not** regenerated; the box console fresh-8 accuracies (incl. the 73.26 %
  mean) remain demoted per GA-F1(b): console-observed on the destroyed instance,
  unarchived, indicative only.

## B. Ours-annex screens (GA-F1, second leg)

- **Seeds (fixed):** 7890, 8901 (the prose-only entries the task names) **+ 9012** (the
  third annex seed: its alive-status is equally prose-only, and the archived protocol-8
  incidence denominator needs it).
- 600 training steps, no evals; **per-step loss + total squared gradient norm** archived
  (JSONL, `ours_annex_screens/`).
- Our stack (`photonic_ssm.linoss`), local CPU, torch CPU generators throughout
  (init / shuffle / dropout — the recorded CPU reference path), deterministic algorithms on.
- The box ran this screen on CUDA; this is the archived **local** estimate — §D applies.

## C. Pre-declared trap classifier (decision-free at read time)

Trap entry was step-instrumented at training step ≤ 7 in every observed case, and the state
is absorbing (total gradient exactly 0.0; Critic re-derivation, review §1.3). Hence:

- **Official screens** (4 eval cycles @ print_steps 1000): **TRAP ⟺** val metric AND train
  metric bit-identical across evals 2/3/4 AND console cycle-mean loss identical to ≥ 6
  significant digits across cycles 2/3/4. (Frozen weights ⇒ deterministic inference evals ⇒
  constancy; an alive run at lr 1e-3 / batch 4 cannot hold the cycle-mean training loss
  still.) **ALIVE ⟺** any of the three moves. The conjunction guards against val-metric
  ties from 35-sample quantization. The loss *value* is recorded as color (fully-wrong
  saturation ⇒ −log(1e-8) ≈ 18.4207; mixed right/wrong saturation ⇒ 18.42 × wrong-fraction)
  but **constancy, not value, classifies**. A run constant on two of the three indicators
  but not the third is reported verbatim, classified ALIVE (conservative toward fewer
  traps), and flagged.
- **Ours screens:** **TRAP ⟺** total gradient ≡ 0.0 exactly from some step k ≤ 600 onward
  (k reported; transient zeros followed by recovery do not count). **ALIVE** otherwise.
  (Direct gradient instrumentation — available because this is our code.)
- **Why 4000 steps suffices:** entry beyond the first eval cycle has never been observed
  (all known entries ≤ step 7); evals 2–4 give three corroborating constancy checks. The
  official early-stop (> 10 non-improving evals) cannot fire within 4 cycles; runs simply
  end at step 4000. No early-stop or final-accuracy numbers are produced or cited from
  these screens.

## D. Environment caveat (the operative sentence, per the Critic)

> Incidence is stream- and environment-dependent; the rented-box console observations
> (official-fresh 2/8; ours-annex 7890@7 / 8901@1 / 9012 alive) are **superseded by this
> archived local estimate**.

A different incidence than the console values is **expected and immaterial** — any material
incidence voids the criterion (PR-1.1 v2 logic, GA-F3).

## E. Benchmark exclusion

One timing run (seed 1, `config_bench/`, num_steps 1000) precedes the declared runs to size
wall-clock. Seed 1 is **not** part of the estimate and is excluded from all reported
statistics.

## F. What gets committed

All trails from these screens (official npy run dirs + console logs + ours-annex JSONLs)
under this directory; **plus**, closing GA-F1's "archived" semantics for the existing
evidence, the previously gitignored `results/s0_2/gate_i/` tree (G1 + gated-G3 jsonls, run
logs, the box-synced `xcheck_official/` published-5 trails — 312 KB total) is force-added
to git in the same pass.
