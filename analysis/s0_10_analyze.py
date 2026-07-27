# NEW (S0.10, PR-17, 2026-07-27) — analyzer for the eval-F re-evaluation +
# T-A-L damping-transfer sweep. Applies the S0.9 verdict rules VERBATIM on the
# eval-F numbers (PR-17 §17.3) and the §17.5 claim rule for T-A-L. Reads
# results/s0_10/runs_{a,b,diagc1,ceiling,talong}; writes
# results/s0_10/analysis.json + a printed summary. Coarse-vs-fine verdict
# deltas are flagged explicitly (both are reported in the paper if they differ).

from __future__ import annotations

import glob
import json
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

R = "results/s0_10"
SER_TARGET = 0.005651
ADV = 2.0


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def paired_ci(a_by_seed, b_by_seed, g):
    """Paired bootstrap 95% CI of median(b) - median(a) (S0.9 rule verbatim)."""
    n = len(a_by_seed)
    diffs = []
    for _ in range(10_000):
        idx = torch.randint(0, n, (n,), generator=g).tolist()
        diffs.append(median([b_by_seed[i] for i in idx])
                     - median([a_by_seed[i] for i in idx]))
    diffs.sort()
    return [diffs[249], diffs[9749]], median(diffs)


def seeds_sorted(d):
    return [d[k] for k in sorted(d)]


def analyze_a(g):
    rows = {}
    for f in glob.glob(f"{R}/runs_a/*.json"):
        d = json.load(open(f))
        rows.setdefault((d["method"], d["mismatch_scale"]), {})[d["seed"]] = \
            d["final_ser_fine"]
    out = {"levels": {}, "crossover_m_star": None,
           "offline_fails_target_at": None}
    for m in sorted({k[1] for k in rows}):
        ins = seeds_sorted(rows[("pat-both", m)])
        off = seeds_sorted(rows[("offline-deploy", m)])
        ci, _ = paired_ci(ins, off, g)
        lvl = {"insitu_median": median(ins), "offline_median": median(off),
               "ratio_off_over_in": median(off) / max(median(ins), 1e-12),
               "ci95_off_minus_in": ci,
               "advantage": (median(off) >= ADV * median(ins)
                             and ci[0] > 0),
               "offline_below_target": median(off) <= SER_TARGET,
               "insitu_per_seed": ins, "offline_per_seed": off}
        out["levels"][str(int(m))] = lvl
        if lvl["advantage"] and out["crossover_m_star"] is None:
            out["crossover_m_star"] = m
        if not lvl["offline_below_target"] and \
                out["offline_fails_target_at"] is None:
            out["offline_fails_target_at"] = m
    return out


def analyze_b(g):
    rows = {}
    for f in glob.glob(f"{R}/runs_b/*.json"):
        d = json.load(open(f))
        rows.setdefault((d["regime"], d["arm"]), {})[d["run_seed"]] = d
    out = {"regimes": {}}
    for regime in ("common", "independent"):
        reg = {}
        for arm in ("insitu-pat", "insitu-spsa", "offline-relock",
                    "offline-head"):
            by_seed = rows[(regime, arm)]
            seeds = sorted(by_seed)
            tints = [sum(s for _, s in by_seed[sd]["ser_traj"]) /
                     len(by_seed[sd]["ser_traj"]) for sd in seeds]
            K = len(by_seed[seeds[0]]["ser_traj"])
            med_traj = [median([by_seed[sd]["ser_traj"][k][1]
                                for sd in seeds]) for k in range(K)]
            reg[arm] = {"median_traj": med_traj,
                        "tint_median": median(tints),
                        "tint_per_seed": tints,
                        "ser0_median": median([by_seed[sd]["ser0"]
                                               for sd in seeds]),
                        "n_seeds": len(seeds)}
        ins = reg["insitu-pat"]["tint_per_seed"]
        off = reg["offline-relock"]["tint_per_seed"]
        ci, _ = paired_ci(ins, off, g)
        ratio = (reg["offline-relock"]["tint_median"] /
                 max(reg["insitu-pat"]["tint_median"], 1e-12))
        reg["advantage_vs_strong_offline"] = {
            "ratio": ratio, "ci95_off_minus_in": ci,
            "ci_excludes_0": ci[0] > 0,
            "advantage": ratio >= ADV and ci[0] > 0}
        out["regimes"][regime] = reg
    return out


def analyze_simple(kind, key="final_ser_fine"):
    rows = {}
    for f in glob.glob(f"{R}/runs_{kind}/*.json"):
        d = json.load(open(f))
        tag = d["tag"].rsplit("_", 1)[0]
        rows.setdefault(tag, []).append(d)
    return {t: {"median_fine": median([x[key] for x in v]),
                "median_coarse": median([x["final_ser_coarse"] for x in v]),
                "per_seed_fine": sorted(x[key] for x in v),
                "n": len(v)}
            for t, v in rows.items()}


def analyze_talong():
    rows = {}
    for f in glob.glob(f"{R}/runs_talong/*.json"):
        d = json.load(open(f))
        rows.setdefault(d["r"], []).append(d)
    curve = {}
    for r, v in sorted(rows.items()):
        curve[f"{r:g}"] = {
            "median_fine": median([x["final_ser_fine"] for x in v]),
            "median_coarse": median([x["final_ser_coarse"] for x in v]),
            "plateaued_n": sum(1 for x in v if x["plateaued"]),
            "n": len(v)}
    # §17.5 claim rule over plateaued-majority points
    plateaued = {r: c for r, c in curve.items() if c["plateaued_n"] >= 5}
    verdict = {"r_star_L": None, "claim_upgraded": False, "note": None}
    if plateaued:
        r_star = min(plateaued, key=lambda r: plateaued[r]["median_fine"])
        verdict["r_star_L"] = float(r_star)
        ref = curve.get("2", curve.get("2.0"))
        if ref is None or ref["plateaued_n"] < 5:
            verdict["note"] = "r=2.0 not plateaued — rule can't evaluate"
        else:
            verdict["claim_upgraded"] = (
                float(r_star) != 2.0 and
                plateaued[r_star]["median_fine"] < 0.7 * ref["median_fine"])
            verdict["sep_ratio_at_rstar"] = (
                plateaued[r_star]["median_fine"] /
                max(ref["median_fine"], 1e-12))
    return {"curve": curve, "verdict": verdict}


def main():
    g = torch.Generator().manual_seed(20260727)
    out = {"ser_target": SER_TARGET, "adv_factor": ADV,
           "eval_protocol": "eval-F (99,840 symbols, PR-17)",
           "s0_10a_mismatch_fine": analyze_a(g),
           "s0_10b_drift_fine": analyze_b(g),
           "diag_c1_fine": analyze_simple("diagc1"),
           "ceiling_fine": analyze_simple("ceiling"),
           "talong": analyze_talong()}
    with open(f"{R}/analysis.json", "w") as fh:
        json.dump(out, fh, indent=1)

    a = out["s0_10a_mismatch_fine"]
    print("== a-fine (mismatch, eval-F) ==")
    for m, lvl in sorted(a["levels"].items(), key=lambda kv: int(kv[0])):
        print(f" m={m}: in {lvl['insitu_median']:.5f} off "
              f"{lvl['offline_median']:.5f} ratio "
              f"{lvl['ratio_off_over_in']:.2f} CI {lvl['ci95_off_minus_in']} "
              f"adv={lvl['advantage']}")
    print(f" crossover m* = {a['crossover_m_star']}")
    b = out["s0_10b_drift_fine"]
    print("== b-fine (drift, eval-F) ==")
    for reg, r in b["regimes"].items():
        adv = r["advantage_vs_strong_offline"]
        print(f" {reg}: in-pat tint {r['insitu-pat']['tint_median']:.5f} "
              f"relock {r['offline-relock']['tint_median']:.5f} ratio "
              f"{adv['ratio']:.2f} CIexcl0={adv['ci_excludes_0']} "
              f"adv={adv['advantage']}")
    print("== diag C-1 fine ==")
    for t, v in out["diag_c1_fine"].items():
        print(f" {t}: fine {v['median_fine']:.5f} "
              f"(coarse {v['median_coarse']:.5f})")
    print("== ceiling fine ==")
    for t, v in out["ceiling_fine"].items():
        print(f" {t}: fine {v['median_fine']:.5f} "
              f"(coarse {v['median_coarse']:.5f})")
    t = out["talong"]
    print("== T-A-L ==")
    for r, c in t["curve"].items():
        print(f" r={r}: fine {c['median_fine']:.5f} "
              f"plateaued {c['plateaued_n']}/{c['n']}")
    print(f" verdict: {t['verdict']}")


if __name__ == "__main__":
    main()
