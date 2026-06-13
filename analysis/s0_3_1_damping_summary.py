# NEW (task S0.3-1, deliverable 9) — summarize the coarse damping sweep into
# the damping→accuracy curve (mean ± σ over seeds, per cell) that selects
# PR-12's central operating cell. Reporting only — the PR-12 freeze is a
# Supervisor+Lucas step.
"""Summarize results/s0_3/damping_sweep.jsonl → the damping→accuracy curve.

  python3 analysis/s0_3_1_damping_summary.py

Writes results/s0_3/damping_curve.json (+ a PNG if matplotlib is available)
and prints the per-cell curve with seed variance. Flags the convergence
caveat: at a fixed training budget the low-damping (high-κ_net) points train
faster, so the curve conflates achievable accuracy with trainability — the
PR-12 reading must weigh this (Supervisor)."""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

SWEEP = "results/s0_3/damping_sweep.jsonl"


def _load(path):
    with open(path) as fh:
        d = json.load(fh)
    return d["records"] if isinstance(d, dict) else d


def summarize():
    rows = _load(SWEEP)
    by = {}
    for r in rows:
        by.setdefault((r["cell"], r["N"]), {}).setdefault(r["damping"], []).append(r)
    curve = {}
    for (cell, N), dmap in sorted(by.items()):
        print(f"\n=== {cell} (N={N}) — damping→accuracy (test, mean±σ over seeds) ===")
        pts = []
        for g_f in sorted(dmap):
            accs = [x["bptt_test_acc"] for x in dmap[g_f]]
            tr = [x["bptt_train_acc"] for x in dmap[g_f]]
            mean = sum(accs) / len(accs)
            var = (sum((a - mean) ** 2 for a in accs) / len(accs)) ** 0.5
            mem = 1.0 / (((1 - g_f) + 2 * 0.3) * 1.0)  # ∝ 1/κ_net (relative)
            pts.append({"damping_g_f": g_f, "test_acc_mean": mean,
                        "test_acc_std": var, "train_acc_mean": sum(tr) / len(tr),
                        "n_seeds": len(accs)})
            print(f"  g_f={g_f:.1f} (κ_net∝{(1-g_f)+0.6:.2f}): "
                  f"test_acc={mean:.3f}±{var:.3f}  "
                  f"train_acc={sum(tr)/len(tr):.3f}  (n={len(accs)})")
        best = max(pts, key=lambda p: p["test_acc_mean"])
        print(f"  → peak test_acc at g_f={best['damping_g_f']:.1f} "
              f"({best['test_acc_mean']:.3f})")
        curve[f"{cell}_N{N}"] = {"points": pts,
                                 "peak_g_f": best["damping_g_f"],
                                 "peak_test_acc": best["test_acc_mean"]}

    out = "results/s0_3/damping_curve.json"
    with open(out, "w") as fh:
        json.dump({"curve": curve,
                   "caveat": ("Fixed-budget (500-step) BPTT; low-damping points "
                              "train faster, so the curve conflates achievable "
                              "accuracy with trainability. PR-12 selection is "
                              "Supervisor+Lucas."),
                   "protocol": {"steps": 500, "batch": 8, "seq_len": 384,
                                "snr_dB": 28, "clock_GSps": 2.0,
                                "mu_init_frac": 0.3, "readout": "R2 |Σc_j a_j|²"}},
                  fh, indent=2)
    print(f"\nwrote {out}")
    _maybe_plot(curve)


def _maybe_plot(curve):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        print("(matplotlib unavailable — skipping PNG)")
        return
    fig, ax = plt.subplots(figsize=(6, 4))
    for key, c in curve.items():
        gs = [p["damping_g_f"] for p in c["points"]]
        ms = [p["test_acc_mean"] for p in c["points"]]
        ss = [p["test_acc_std"] for p in c["points"]]
        ax.errorbar(gs, ms, yerr=ss, marker="o", capsize=3, label=key)
    ax.set_xlabel("gain compensation g_f  (damping floor: κ_net=(1−g_f)κᵢ+2κ_ext)")
    ax.set_ylabel("T-A test accuracy (1−SER)")
    ax.set_title("S0.3-1 coarse BPTT damping→accuracy curve (→ PR-12)")
    ax.legend(); ax.grid(alpha=0.3)
    fig.tight_layout()
    png = "results/s0_3/damping_curve.png"
    fig.savefig(png, dpi=120)
    print(f"wrote {png}")


if __name__ == "__main__":
    summarize()
