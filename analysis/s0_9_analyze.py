# NEW (S0.9, 2026-07-24) — analyze the mismatch sweep (PR-5 §E) + the
# deploy-then-drift sweep (PR-16) against the ratified margins:
#   advantage iff offline_median >= 2x insitu_median AND paired-by-seed
#   bootstrap 95% CI of (offline - insitu) excludes 0.
"""usage: s0_9_analyze.py            # runs both A and B, writes results/s0_9/analysis.json"""

from __future__ import annotations

import glob
import json
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

SEEDS = [11, 23, 47, 61, 83, 101, 127, 151]
SER_TARGET = 0.005651
CEILING = 0.00052083
ADV_FACTOR = 2.0                       # ratified 2026-07-24
RUNS_A = "results/s0_9/runs_a"
RUNS_B = "results/s0_9/runs_b"


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def paired_ci(insitu_by_seed, offline_by_seed, g):
    """Paired-by-seed bootstrap 95% CI of median(offline) - median(insitu)."""
    n = len(insitu_by_seed)
    diffs = []
    for _ in range(10_000):
        idx = torch.randint(0, n, (n,), generator=g).tolist()
        diffs.append(median([offline_by_seed[i] for i in idx])
                     - median([insitu_by_seed[i] for i in idx]))
    diffs.sort()
    return [diffs[249], diffs[9749]], median(diffs)


def load_a():
    rows = {}
    for f in glob.glob(f"{RUNS_A}/*.json"):
        d = json.load(open(f))
        rows.setdefault((d["method"], d["mismatch_scale"]), {})[d["seed"]] = \
            d["final_ser"]
    return rows


def analyze_a(g):
    rows = load_a()
    if not rows:
        return {"status": "no runs_a yet"}
    out = {"levels": {}, "crossover_m_star": None, "offline_fails_target_at": None}
    for m in [1, 2, 3, 4, 6]:
        ins = rows.get(("pat-both", m))
        off = rows.get(("offline-deploy", m))
        if not ins or not off:
            continue
        ib = [ins[s] for s in SEEDS if s in ins]
        ob = [off[s] for s in SEEDS if s in off]
        if len(ib) < len(SEEDS) or len(ob) < len(SEEDS):
            out["levels"][m] = {"incomplete": [len(ib), len(ob)]}
            continue
        im, om = median(ib), median(ob)
        ci, mdiff = paired_ci(ib, ob, g)
        adv = (om >= ADV_FACTOR * im) and (ci[0] > 0)
        out["levels"][m] = {
            "insitu_median": im, "offline_median": om,
            "ratio_off_over_in": om / im if im > 0 else None,
            "ci95_off_minus_in": ci, "advantage": adv,
            "offline_below_target": om <= SER_TARGET,
            "insitu_below_target": im <= SER_TARGET,
            "insitu_per_seed": ib, "offline_per_seed": ob}
        if adv and out["crossover_m_star"] is None:
            out["crossover_m_star"] = m
        if om > SER_TARGET and out["offline_fails_target_at"] is None:
            out["offline_fails_target_at"] = m
    # m=1 validation vs S0.5 (pat 0.00078, offline 0.00104)
    if 1 in out["levels"] and "insitu_median" in out["levels"][1]:
        out["m1_validation"] = {
            "insitu": out["levels"][1]["insitu_median"],
            "offline": out["levels"][1]["offline_median"],
            "s0_5_ref": {"insitu": 0.00078, "offline": 0.00104}}
    return out


def load_b():
    rows = {}
    for f in glob.glob(f"{RUNS_B}/*.json"):
        d = json.load(open(f))
        # time-integrated (mean over k) SER, per seed
        traj = [s for _, s in d["ser_traj"]]
        tint = sum(traj) / len(traj) if traj else float("nan")
        rows.setdefault((d["arm"], d["regime"]), {})[d["run_seed"]] = {
            "tint": tint, "traj": traj, "ser0": d["ser0"]}
    return rows


def analyze_b(g):
    rows = load_b()
    if not rows:
        return {"status": "no runs_b yet"}
    out = {"regimes": {}}
    for regime in ["common", "independent"]:
        insitu = rows.get(("insitu-pat", regime))
        offline = rows.get(("offline-relock", regime))   # strong offline
        offhead = rows.get(("offline-head", regime))
        spsa = rows.get(("insitu-spsa", regime))
        block = {}
        # median trajectories for reporting
        for arm, r in [("insitu-pat", insitu), ("insitu-spsa", spsa),
                       ("offline-relock", offline), ("offline-head", offhead)]:
            if r:
                seeds = [s for s in SEEDS if s in r]
                K = len(r[seeds[0]]["traj"])
                med_traj = [median([r[s]["traj"][k] for s in seeds])
                            for k in range(K)]
                block[arm] = {
                    "median_traj": med_traj,
                    "tint_median": median([r[s]["tint"] for s in seeds]),
                    "ser0_median": median([r[s]["ser0"] for s in seeds]),
                    "n_seeds": len(seeds)}
        # advantage verdict: strong-offline (relock) vs insitu-pat
        if insitu and offline and all(s in insitu and s in offline
                                      for s in SEEDS):
            ib = [insitu[s]["tint"] for s in SEEDS]
            ob = [offline[s]["tint"] for s in SEEDS]
            im, om = median(ib), median(ob)
            ci, mdiff = paired_ci(ib, ob, g)
            block["advantage_vs_strong_offline"] = {
                "insitu_tint_median": im, "offline_relock_tint_median": om,
                "ratio": om / im if im > 0 else None,
                "ci95_off_minus_in": ci,
                "advantage": (om >= ADV_FACTOR * im) and (ci[0] > 0),
                "insitu_below_target": im <= SER_TARGET}
        out["regimes"][regime] = block
    return out


def main():
    g = torch.Generator().manual_seed(20260724)
    res = {"ser_target": SER_TARGET, "ceiling": CEILING,
           "adv_factor": ADV_FACTOR,
           "s0_9a_mismatch_sweep": analyze_a(g),
           "s0_9b_drift": analyze_b(g)}
    os.makedirs("results/s0_9", exist_ok=True)
    with open("results/s0_9/analysis.json", "w") as fh:
        json.dump(res, fh, indent=2)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
