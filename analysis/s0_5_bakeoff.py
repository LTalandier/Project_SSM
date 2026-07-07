# NEW (task S0.4-close + S0.5-core, 2026-07-07) — the staged runner for the
# ceiling measurement + the gated 8-seed bake-off, under the PR-3/PR-8/PR-9
# blocks FROZEN at ae16f6d (before the sizing pilot) and the sizing numbers
# recorded in results/s0_5/sizing.json (committed before any estimator run).
"""Stages (run in order, committing the addendum between 2 and 3):

  python3 analysis/s0_5_bakeoff.py sizing    # derive U_conv/U_max/B from the pilot
  python3 analysis/s0_5_bakeoff.py ceiling   # PR-3 §A: 8-seed C-2 + C-1 + Δ_M3 spot
  python3 analysis/s0_5_bakeoff.py bakeoff   # PR-8 arms × 8 seeds at C-2 (+ C-1 tier)
  python3 analysis/s0_5_bakeoff.py stats     # PR-8 §B stats + PR-9 gates → bakeoff.json

Everything reads/writes results/s0_5/.
"""

from __future__ import annotations

import json
import os
import sys
import time

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from photonic_ssm.estimators.harness import BATCH, train  # noqa: E402

OUT = "results/s0_5"
SEEDS8 = (11, 23, 47, 61, 83, 101, 127, 151)     # PR-3 §A / PR-8 §A
SEEDS3 = (11, 23, 47)
EVAL_EVERY = 100

# PR-7/PR-7.1 device passes per update at batch 8.
PASSES_PER_UPDATE = {"pat-both": 8, "spsa": 16, "adjoint": 16, "rhel": 32,
                     "head-only": 8, "offline-deploy": 8}
RANKED = ("pat-both", "spsa", "adjoint", "rhel")
BASELINES = ("head-only", "offline-deploy")


def _load(name):
    with open(os.path.join(OUT, name)) as fh:
        return json.load(fh)


def _dump(obj, name):
    with open(os.path.join(OUT, name), "w") as fh:
        json.dump(obj, fh, indent=2)
    print("wrote", os.path.join(OUT, name))


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def final_ser(led):
    """PR-3 §A statistic: median of the last 3 eval points."""
    return median([s for _, _, s in led["eval_trace"][-3:]])


def stage_sizing():
    pilot = _load("pilot_seed7.json")
    evals = [(it, s) for it, _, s in pilot["eval_trace"]]
    # U_conv = first eval point after which no >1% relative improvement of
    # the median-of-3 smoothed curve occurs (spec item 1).
    sm = [(evals[i][0], median([evals[j][1] for j in
                                range(max(0, i - 1), min(len(evals), i + 2))]))
          for i in range(len(evals))]
    u_conv = sm[-1][0]
    for i in range(len(sm)):
        tail_best = min(s for _, s in sm[i:])
        if sm[i][1] <= 0 or (sm[i][1] - tail_best) / max(sm[i][1], 1e-12) <= 0.01:
            u_conv = sm[i][0]
            break
    u_max = int(-(-1.5 * u_conv // 500) * 500)          # ceil to 500
    B = 2 * u_conv * 16
    sizing = {"U_conv": u_conv, "U_max": u_max, "B_device_passes": B,
              "updates_per_arm": {m: B // p for m, p in
                                  PASSES_PER_UPDATE.items()},
              "pilot_final_ser": median([s for _, s in evals[-3:]])}
    _dump(sizing, "sizing.json")
    print(sizing)


def _run(method, cell, seed, n_updates, gain_mode=None):
    t0 = time.time()
    led = train(method, cell, run_seed=seed, n_updates=n_updates,
                eval_every=EVAL_EVERY, gain_mode=gain_mode,
                N=8 if cell == "C-1" else None)
    row = {"seed": seed, "final_ser": final_ser(led),
           "eval_trace": led["eval_trace"],
           "device_passes": led["device_passes"],
           "digital_passes": led["digital_passes"],
           "wall_s": round(time.time() - t0, 1)}
    print(f"  {method}@{cell} seed {seed}: final SER {row['final_ser']:.4f} "
          f"dev {row['device_passes']} dig {row['digital_passes']} "
          f"[{row['wall_s']}s]", flush=True)
    return row


def stage_ceiling():
    sz = _load("sizing.json")
    out = {"U_max": sz["U_max"]}
    print(f"[ceiling C-2, BPTT x 8 seeds, U_max={sz['U_max']}]", flush=True)
    out["c2"] = [_run("bptt", "C-2", s, sz["U_max"]) for s in SEEDS8]
    out["ceiling_ser_c2"] = median([r["final_ser"] for r in out["c2"]])
    print(f"[fixed-gain sensitivity spot, 3 seeds]", flush=True)
    out["c2_fixed"] = [_run("bptt", "C-2", s, sz["U_max"],
                            gain_mode="fixed") for s in SEEDS3]
    out["delta_m3"] = abs(out["ceiling_ser_c2"]
                          - median([r["final_ser"] for r in out["c2_fixed"]]))
    print(f"[ceiling C-1 secondary, 8 seeds]", flush=True)
    out["c1"] = [_run("bptt", "C-1", s, sz["U_max"]) for s in SEEDS8]
    out["ceiling_ser_c1"] = median([r["final_ser"] for r in out["c1"]])
    out["ser_target_c2"] = 1.25 * out["ceiling_ser_c2"] + 0.005   # PR-3 §B
    out["ser_target_c1"] = 1.25 * out["ceiling_ser_c1"] + 0.005
    _dump(out, "ceiling.json")
    print({k: out[k] for k in ("ceiling_ser_c2", "delta_m3",
                               "ceiling_ser_c1", "ser_target_c2")})


def stage_bakeoff():
    sz = _load("sizing.json")
    runs = {}
    for m in RANKED + BASELINES:
        n_up = sz["updates_per_arm"][m]
        print(f"[C-2 arm {m}: {n_up} updates x 8 seeds]", flush=True)
        runs[m] = [_run(m, "C-2", s, n_up) for s in SEEDS8]
        _dump(runs, "bakeoff_runs.json")          # checkpoint after each arm
    print("[C-1 diagnostic tier: PAT families + rhel-ideal, 3 seeds]",
          flush=True)
    diag = {}
    for m in ("pat-perfect", "pat-M-par", "pat-M-struct", "rhel-ideal"):
        p = PASSES_PER_UPDATE.get(m, 8 if m.startswith("pat") else 32)
        n_up = sz["B_device_passes"] // p
        diag[m] = [_run(m, "C-1", s, n_up) for s in SEEDS3]
        _dump(diag, "bakeoff_diag_c1.json")
    print("bakeoff runs complete")


def _to_target(row, ser_target, B):
    for it, passes, ser in row["eval_trace"]:
        if ser <= ser_target and passes <= B:
            return True, passes
    return False, None


def stage_stats():
    sz, ceil_, runs = _load("sizing.json"), _load("ceiling.json"), \
        _load("bakeoff_runs.json")
    B, tgt = sz["B_device_passes"], ceil_["ser_target_c2"]
    g = torch.Generator().manual_seed(20260707)
    stats = {"B": B, "ser_target_c2": tgt,
             "ceiling_ser_c2": ceil_["ceiling_ser_c2"],
             "delta_m3": ceil_["delta_m3"], "arms": {}}
    per_seed_passes = {}
    for m, rows in runs.items():
        outcomes = [_to_target(r, tgt, B) for r in rows]
        succ = [o[0] for o in outcomes]
        passes_cens = [o[1] if o[0] else B * 10 for o in outcomes]  # B+ sentinel
        per_seed_passes[m] = passes_cens
        med = median(passes_cens)
        stats["arms"][m] = {
            "success_fraction": sum(succ) / len(succ),
            "n_censored": len(succ) - sum(succ),
            "median_passes_censored_at_Bplus":
                (med if med < B * 10 else "censored"),
            "final_ser_median": median([r["final_ser"] for r in rows]),
            "final_ser_per_seed": [r["final_ser"] for r in rows],
            "digital_passes": rows[0]["digital_passes"],
        }
    # Paired-by-seed bootstrap (PR-8 §B) on median-passes differences.
    stats["paired_bootstrap"] = {}
    n = len(SEEDS8)
    for a in RANKED:
        for b in RANKED:
            if a >= b:
                continue
            diffs = []
            for _ in range(10_000):
                idx = torch.randint(0, n, (n,), generator=g).tolist()
                diffs.append(median([per_seed_passes[a][i] for i in idx])
                             - median([per_seed_passes[b][i] for i in idx]))
            diffs.sort()
            stats["paired_bootstrap"][f"{a} - {b}"] = {
                "ci95": [diffs[249], diffs[9749]],
                "median_diff": median(diffs)}
    # PR-9 gates.
    res_med = stats["arms"]["head-only"]["final_ser_median"]
    stats["gate_ii_a"] = {
        "ceiling_ser": ceil_["ceiling_ser_c2"], "reservoir_ser": res_med,
        "rule": "ceiling <= 0.5 * reservoir",
        "pass": bool(ceil_["ceiling_ser_c2"] <= 0.5 * res_med)}
    ii_b = {m: sum(_to_target(r, tgt, B)[0] for r in runs[m])
            for m in ("pat-both", "spsa")}
    stats["gate_ii_b"] = {"successes": ii_b,
                          "rule": "PAT-both or SPSA >= 5/8",
                          "pass": bool(max(ii_b.values()) >= 5)}
    only_exotic = (not stats["gate_ii_b"]["pass"]) and any(
        sum(_to_target(r, tgt, B)[0] for r in runs[m]) >= 5
        for m in ("adjoint", "rhel"))
    stats["only_adjoint_rhel_pass_escalate"] = bool(only_exotic)
    # R3b readout-only differentials (PR-9 rule).
    stats["readout_differential"] = {
        m: stats["arms"][m]["final_ser_median"] - res_med
        for m in RANKED + ("offline-deploy",)}
    _dump(stats, "bakeoff.json")
    print(json.dumps({k: stats[k] for k in
                      ("gate_ii_a", "gate_ii_b", "readout_differential")},
                     indent=2))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    {"sizing": stage_sizing, "ceiling": stage_ceiling,
     "bakeoff": stage_bakeoff, "stats": stage_stats}[sys.argv[1]]()
