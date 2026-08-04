# NEW (PR-18, 2026-08-04) — aggregate the S0.11 converged-operating-point
# diagnostics (analysis/s0_11_run_one.py units) and apply the PR-18 §18.4
# frozen interpretation rules. Writes results/s0_11/s0_11.{json,md}.
from __future__ import annotations

import glob
import json
import os

SETS = ("pinned2", "boxed3", "patC2", "spsaC2")
MU_C = 0.3          # registered init, μ_c/κᵢ
THETA0_REF = {"gate": 32, "worst": 1.42e-3, "part": (4, 26, 32)}  # S0.4-0


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def load(set_name):
    rows = []
    for f in sorted(glob.glob(f"results/s0_11/runs/{set_name}_*.json")):
        rows.append(json.load(open(f)))
    return rows


def analyze_set(rows):
    counts = [r["gate_at_solution"]["count_ge_gate_mse_zero"] for r in rows]
    counts_t = [r["gate_at_solution"]["count_ge_gate_mse_target"]
                for r in rows]
    med = median(counts)
    if med >= 30:
        verdict = "maintained"
    elif med <= 16:
        verdict = "collapsed"
    else:
        verdict = "intermediate"
    mu_meds = [r["params"]["mu_median_over_ki"] for r in rows]
    mu_all = [m for r in rows for m in r["params"]["mu_over_ki"]]
    r_sds = [r["params"]["r_sd"] for r in rows]
    mech = {
        "repair_by_mu": median(mu_meds) >= 2 * MU_C,
        "repair_by_profile": (verdict == "maintained"
                              and median(mu_meds) < 2 * MU_C
                              and median(r_sds) > 0.15),
        "dark_but_converged": verdict == "collapsed",
    }
    return {
        "n": len(rows),
        "fingerprints": sorted({r["fingerprint"] for r in rows}),
        "fp_all_bit": all(r["fingerprint"] == "bit" for r in rows),
        "gate_count_median": med,
        "gate_count_range": [min(counts), max(counts)],
        "gate_counts": counts,
        "gate_count_mse_target_median": median(counts_t),
        "worst_ratio_median": median(
            [r["gate_at_solution"]["worst_ratio_mse_zero"] for r in rows]),
        "participation_median": [
            median([r["participation_at_solution"][k] for r in rows])
            for k in ("count_ge_1e-1", "count_ge_1e-2", "count_ge_1e-3")],
        "mu_median_over_seeds": median(mu_meds),
        "mu_min": min(mu_all), "mu_max": max(mu_all),
        "r_sd_median": median(r_sds),
        "vii_min_achieved": min(r["vii_endpoint"]["min_achieved"]
                                for r in rows),
        "vii_min_band": min(r["vii_endpoint"]["min_band"] for r in rows),
        "verdict_18_4": verdict,
        "mechanism": mech,
    }


def main():
    out = {"theta0_reference": THETA0_REF, "sets": {}}
    for s in SETS:
        rows = load(s)
        if rows:
            out["sets"][s] = analyze_set(rows)
    done_sets = [s for s in SETS if s in out["sets"]]
    if done_sets:
        out["vii_min_overall"] = min(
            out["sets"][s]["vii_min_achieved"] for s in done_sets)
        out["vii_endpoint_closed"] = out["vii_min_overall"] > 0
    os.makedirs("results/s0_11", exist_ok=True)
    with open("results/s0_11/s0_11.json", "w") as fh:
        json.dump(out, fh, indent=1)

    lines = ["# S0.11 — converged-operating-point diagnostics (PR-18)", "",
             f"θ₀ reference (S0.4-0): gate 32/32, worst 1.42e-3, "
             f"participation {THETA0_REF['part']}", ""]
    for s in done_sets:
        a = out["sets"][s]
        lines += [
            f"## {s} (n={a['n']}, fingerprints {a['fingerprints']})",
            f"- gate at solution (mse_zero, min-over-5-drive-seeds): median "
            f"{a['gate_count_median']}/32 (range {a['gate_count_range']}), "
            f"worst ratio median {a['worst_ratio_median']:.2e} → "
            f"**{a['verdict_18_4']}** (18.4 rule)",
            f"- mse_target co-report: median "
            f"{a['gate_count_mse_target_median']}/32",
            f"- participation at solution (median): "
            f"{a['participation_median']}",
            f"- μ/κᵢ: median-over-seeds {a['mu_median_over_seeds']:.3f} "
            f"(init 0.3; range [{a['mu_min']:.3f}, {a['mu_max']:.3f}]) — "
            f"repair-by-μ: {a['mechanism']['repair_by_mu']}",
            f"- r profile sd (median): {a['r_sd_median']:.3f} — "
            f"repair-by-profile: {a['mechanism']['repair_by_profile']}",
            f"- vii endpoint: min κ_net^δ-aware at achieved δ "
            f"{a['vii_min_achieved']:.3f} κᵢ (band worst "
            f"{a['vii_min_band']:.3f})",
            "",
        ]
    if done_sets:
        lines += [f"**vii endpoint overall:** min {out['vii_min_overall']:.3f}"
                  f" κᵢ → closed at endpoints: {out['vii_endpoint_closed']}"]
    with open("results/s0_11/s0_11.md", "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
