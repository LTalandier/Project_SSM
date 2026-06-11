"""S0.2-1R GA-F1: classify the regenerated screens per the PRE-DECLARED criterion.

Reads (a) the official fresh-8 screen trails (npy run dirs + driver console log) and
(b) the ours-annex 600-step screen JSONLs, applies the classifier pre-declared in
results/s0_2/gate_i/xcheck_official_local/PREDECLARATION.md §C (committed 889ab53,
BEFORE any run), and prints the per-seed verdict tables + k/n incidence.

Classifier (official screens, 4 eval cycles): TRAP iff val metric AND train metric
bit-identical across evals 2/3/4 AND console cycle-mean loss identical to >=6
significant digits across cycles 2/3/4; ALIVE if any of the three moves; two-of-three
constancy -> ALIVE (conservative) + flag.
Classifier (ours screens): TRAP iff grad_sq_total == 0.0 from some k <= 600 onward.

Usage: python3 analysis/s0_2_1r_classify.py
"""
import json
import os
import re

import numpy as np

BASE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "results", "s0_2", "gate_i", "xcheck_official_local",
)
SEEDS = [7890, 8901, 9012, 11111, 22222, 33333, 44444, 55555]
OUT_TMPL = (
    "outputs/LinOSS_IM/EigenWorms/"
    "T_1.00_time_True_nsteps_4000_lr_0.001_num_blocks_2_hidden_dim_128_"
    "vf_depth_None_vf_width_None_ssm_dim_64_ssm_blocks_2_dt0_None_solver_Heun_"
    "stepsize_controller_ConstantStepSize_scale_0_lambd_None_seed_{seed}"
)
ANNEX_SEEDS = [7890, 8901, 9012]
FULLY_WRONG_LOSS = 18.420680743952367  # -log(1e-8)


def sig6(x: float) -> str:
    return f"{x:.6g}"


def parse_driver_log(path):
    """Segment the driver console log per seed; return {seed: [loss_cycle1..4]}."""
    if not os.path.isfile(path):
        return {}
    with open(path, errors="replace") as fh:
        text = fh.read()
    # Runs are announced by their output-directory line containing seed_N.
    chunks = re.split(r"(seed_(\d+) has been created)", text)
    losses = {}
    # re.split with 2 groups yields [pre, full, seed, body, full, seed, body, ...]
    for i in range(2, len(chunks), 3):
        seed = int(chunks[i])
        body = chunks[i + 1] if i + 1 < len(chunks) else ""
        vals = [float(m) for m in re.findall(r"Loss: ([0-9eE.+-]+),", body)]
        losses[seed] = vals
    return losses


def classify_official():
    print("== Official fresh-8 screens (4 cycles @ 1000 steps, pinned CPU venv) ==")
    log_losses = {}
    import glob
    for lp in sorted(glob.glob(os.path.join(BASE, "logs", "driver_seed*.log"))) + [
        os.path.join(BASE, "logs", "driver_fresh8.log")
    ]:
        log_losses.update(parse_driver_log(lp))
    rows, k = [], 0
    for seed in SEEDS:
        run_dir = os.path.join(BASE, OUT_TMPL.format(seed=seed))
        val_p = os.path.join(run_dir, "all_val_metric.npy")
        tr_p = os.path.join(run_dir, "all_train_metric.npy")
        if not (os.path.isfile(val_p) and os.path.isfile(tr_p)):
            rows.append((seed, "MISSING", None, None, None, None))
            continue
        val = np.load(val_p)
        tr = np.load(tr_p)
        if len(val) < 5 or len(tr) < 5:
            rows.append((seed, "INCOMPLETE", None, None, None, len(val)))
            continue
        val_const = val[2] == val[3] == val[4]
        tr_const = tr[2] == tr[3] == tr[4]
        ls = log_losses.get(seed, [])
        loss_const = (
            len(ls) >= 4 and sig6(ls[1]) == sig6(ls[2]) == sig6(ls[3])
        )
        n_const = sum([val_const, tr_const, loss_const])
        verdict = "TRAP" if n_const == 3 else "ALIVE"
        flag = " [2/3-constant — flagged]" if n_const == 2 else ""
        if verdict == "TRAP":
            k += 1
        rows.append(
            (seed, verdict + flag,
             [round(float(v), 6) for v in val[1:5]],
             [round(float(t), 6) for t in tr[1:5]],
             [sig6(x) for x in ls[:4]],
             None)
        )
    for seed, verdict, val, tr, ls, extra in rows:
        if val is None:
            print(f"  seed {seed}: {verdict} (evals seen: {extra})")
        else:
            wrong_frac = (
                round(float(ls[1].replace(',', '')) / FULLY_WRONG_LOSS, 3)
                if "TRAP" in verdict and ls else None
            )
            color = f" wrong-frac~{wrong_frac}" if wrong_frac else ""
            print(f"  seed {seed}: {verdict}")
            print(f"    val e1..e4   {val}")
            print(f"    train e1..e4 {tr}")
            print(f"    loss c1..c4  {ls}{color}")
    n_done = sum(1 for r in rows if r[2] is not None)
    print(f"  => official-fresh incidence (local CPU): {k}/{n_done} trapped"
          f" ({len(SEEDS) - n_done} missing/incomplete)")
    return k, n_done


def classify_annex():
    print("== Ours-annex 600-step screens (local CPU, torch) ==")
    k, n = 0, 0
    for seed in ANNEX_SEEDS:
        p = os.path.join(
            BASE, "ours_annex_screens", f"EigenWorms_annexscreen_seed{seed}.jsonl"
        )
        if not os.path.isfile(p):
            print(f"  seed {seed}: MISSING")
            continue
        summary = None
        with open(p) as fh:
            for line in fh:
                rec = json.loads(line)
                if rec.get("record") == "summary":
                    summary = rec
        if summary is None:
            print(f"  seed {seed}: INCOMPLETE (no summary record)")
            continue
        n += 1
        if summary["verdict"] == "TRAP":
            k += 1
            print(f"  seed {seed}: TRAP since step {summary['trapped_since_step']}"
                  f" (final loss {summary['final_loss']:.4f})")
        else:
            print(f"  seed {seed}: ALIVE (final loss {summary['final_loss']:.4f})")
    print(f"  => ours-annex (local CPU): {k}/{n} trapped")
    return k, n


if __name__ == "__main__":
    classify_official()
    print()
    classify_annex()
