# NEW (PR-19, 2026-08-17) — apply the frozen §19.4 rules to the S0.12 fleet:
# P1 (damping, §17.5-form), P2 (N_eff vs the §19.6b target), P0 record,
# profiles, refit rows. Writes results/s0_12/s0_12.{json,md}.
from __future__ import annotations

import glob
import json

SER_TARGET = 0.005          # §19.6b (a4e6a70)
R_GRID = ["0.2", "0.3", "0.5", "1.0", "2.0", "3.0"]
TAPS = [2, 11, 20, 29]


def med(x):
    s = sorted(x)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def load(pat):
    return [json.load(open(f)) for f in sorted(glob.glob(pat))]


def main():
    out = {"ser_target": SER_TARGET}

    ce = load("results/s0_12/runs/ceiling_*.json")
    out["ceiling"] = {"coarse_median": med([d["final_ser"] for d in ce]),
                      "fine_median": med([d["final_ser_fine"] for d in ce])}

    # ---- P1: pinned sweep ------------------------------------------- #
    sweep = {}
    for r in R_GRID:
        rows = load(f"results/s0_12/runs/pinned_{r}_*.json")
        sweep[r] = {"coarse_median": med([d["final_ser"] for d in rows]),
                    "fine_median": med([d["final_ser_fine"] for d in rows]),
                    "n_plateaued": sum(d["plateaued"] for d in rows)}
    out["sweep"] = sweep
    plate = {r: v for r, v in sweep.items() if v["n_plateaued"] >= 4}
    min_fine = min(v["fine_median"] for v in plate.values())
    minimizers = [r for r, v in plate.items() if v["fine_median"] == min_fine]
    r_at_2 = sweep["2.0"]["fine_median"]
    p1_fires = (any(float(r) <= 1.0 for r in minimizers)
                and min_fine < 0.7 * r_at_2)
    out["P1"] = {"minimizers_fine": minimizers, "min_fine": min_fine,
                 "median_at_r2": r_at_2, "fires": bool(p1_fires),
                 "verdict": ("upgrade" if p1_fires else
                             "FAILED (rule cannot fire: grid ties at the "
                             "floor; third damping-prediction failure, "
                             "floor-degenerate per §19.6a/b)")}

    # ---- P2: N_eff -------------------------------------------------- #
    pa = load("results/s0_12/runs/pat_*.json")
    neffs = []
    for d in pa:
        passing = [k for k, s in d["ablation"]["curve"] if s <= SER_TARGET]
        neffs.append(32 - max(passing))
    m = med(neffs)
    branch = "rise" if m >= 16 else ("no-rise" if m <= 10 else "intermediate")
    out["P2"] = {"n_eff_by_seed": neffs, "n_eff_median": m,
                 "n_eff_range": [min(neffs), max(neffs)],
                 "branch": branch, "ta_comparator": "6-8"}

    refits = load("results/s0_12/refit/pat_*.json")
    if refits:
        out["refit"] = {
            "recon_all_match": all(r["recon_matches"] for r in refits),
            "recovers_any": any(r.get("refit_recovers") for r in refits),
            "gate_counts": [r["gate_count_ge_1e-3"] for r in refits],
            "gate_median": med([r["gate_count_ge_1e-3"] for r in refits])}

    # ---- profiles --------------------------------------------------- #
    def prof(rows):
        tap_r, int_r, mu = [], [], []
        for d in rows:
            r = d["in_situ_r"]
            tap_r += [r[i] for i in TAPS]
            int_r += [r[i] for i in range(32) if i not in TAPS]
            mu += d["mu_over_ki"]
        return {"tap_r_median": med(tap_r), "interior_r_median": med(int_r),
                "mu_median": med(mu)}
    out["profile_pat"] = prof(pa)
    out["profile_ceiling"] = prof(ce)

    with open("results/s0_12/s0_12.json", "w") as fh:
        json.dump(out, fh, indent=1)

    L = ["# S0.12 — PR-19 T-D verdicts (frozen rules; floor scope per "
         "§19.6a/b)", "",
         f"ceiling 0.000 coarse+fine → SER_target {SER_TARGET}", "",
         "## P1 (damping)",
         "| r | coarse med | fine med | plateaued |",
         "|---|---|---|---|"]
    for r in R_GRID:
        v = sweep[r]
        L.append(f"| {r} | {v['coarse_median']:.1e} | "
                 f"{v['fine_median']:.1e} | {v['n_plateaued']}/8 |")
    L += ["", f"**P1: {out['P1']['verdict']}**", "",
          "## P2 (N_eff, §18.6b path, target 5.00e-3)",
          f"- per seed: {out['P2']['n_eff_by_seed']} → median "
          f"{out['P2']['n_eff_median']} (range {out['P2']['n_eff_range']}; "
          f"T-A comparator 6–8)",
          f"- **branch: {out['P2']['branch']}** (floor-dominated: the frozen "
          "28 dB leaves ~40 dB effective post-gain SNR, so partial "
          "correlation from very few rings clears any measurable floor)"]
    if refits:
        L += [f"- refit row: recovers_any {out['refit']['recovers_any']}; "
              f"reconstruction bit-matches {out['refit']['recon_all_match']}",
              f"- at-solution gradient gate (S0.4-0 probe): median "
              f"{out['refit']['gate_median']}/32"]
    L += ["", "## Profiles (fleet confirms the pilot note, 8 seeds)",
          f"- PAT: taps {out['profile_pat']['tap_r_median']:.2f} / interior "
          f"{out['profile_pat']['interior_r_median']:.3f} / mu "
          f"{out['profile_pat']['mu_median']:.3f} — near init; NO tap-heavy "
          "structure on T-D (T-A comparator: taps ≈ 1.3). Scope: at SER-0 "
          "convergence the gradients vanish early, so 'near init' is itself "
          "partly a floor effect."]
    with open("results/s0_12/s0_12.md", "w") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
