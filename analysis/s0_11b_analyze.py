# NEW (PR-18 §18.6, 2026-08-05) — aggregate the 18.6 units and apply the
# frozen rules: (a) taps-only control verdict (paired bootstrap at eval-F,
# S0.9/S0.10 CI convention verbatim) and (b) N_eff summary. Writes
# results/s0_11/s0_11b.{json,md}.
from __future__ import annotations

import glob
import json

import torch


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


def by_seed(pattern, key):
    out = {}
    for f in glob.glob(pattern):
        d = json.load(open(f))
        out[d["seed"]] = d[key]
    return [out[k] for k in sorted(out)], sorted(out)


def main():
    g = torch.Generator().manual_seed(20260805)
    out = {}

    # ---- (a) taps-only control ---------------------------------------- #
    full_fine, seeds_f = by_seed("results/s0_10/runs_a/pat-both_m1_*.json",
                                 "final_ser_fine")
    tap_fine, seeds_t = by_seed("results/s0_11/runs_b/tapsonly_*.json",
                                "final_ser_fine")
    assert seeds_f == seeds_t, (seeds_f, seeds_t)
    ci, med_diff = paired_ci(full_fine, tap_fine, g)   # (tapsonly - full)
    full_coarse, _ = by_seed("results/s0_10/runs_a/pat-both_m1_*.json",
                             "final_ser")
    tap_coarse, _ = by_seed("results/s0_11/runs_b/tapsonly_*.json",
                            "final_ser_coarse")
    verdict = "A-discovers" if (ci[0] > 0 or ci[1] < 0) else "B-inherited"
    out["tapsonly_control"] = {
        "full_fine_by_seed": full_fine, "tapsonly_fine_by_seed": tap_fine,
        "full_fine_median": median(full_fine),
        "tapsonly_fine_median": median(tap_fine),
        "paired_ci_tapsonly_minus_full_fine": ci,
        "median_diff_fine": med_diff,
        "full_coarse_median": median(full_coarse),
        "tapsonly_coarse_median": median(tap_coarse),
        "verdict_18_6a": verdict,
    }

    # ---- (b) N_eff ablation ------------------------------------------- #
    for set_name in ("patC2", "spsaC2"):
        rows = [json.load(open(f)) for f in
                sorted(glob.glob(f"results/s0_11/runs_b/{set_name}_*.json"))]
        neffs = [r["ablation"]["n_eff"] for r in rows]
        refit = [r["ablation"].get("refit_recovers") for r in rows]
        # descriptive: last k with SER within 2x the k=0 baseline
        hold2x = []
        for r in rows:
            curve = r["ablation"]["curve"]
            base = curve[0][1]
            ks = [k for k, s in curve if s <= max(2 * base, base + 1e-12)]
            hold2x.append(max(ks) if ks else 0)
        out[f"neff_{set_name}"] = {
            "n_eff_by_seed": neffs,
            "n_eff_median": median(neffs),
            "n_eff_range": [min(neffs), max(neffs)],
            "refit_recovers_any": any(refit),
            "k_hold_2x_baseline_median": median(hold2x),
            "fingerprints_all_bit": all(r["fingerprint"] == "bit"
                                        for r in rows),
        }

    with open("results/s0_11/s0_11b.json", "w") as fh:
        json.dump(out, fh, indent=1)

    t = out["tapsonly_control"]
    lines = [
        "# S0.11b — PR-18 §18.6 verdicts (frozen rules)", "",
        "## (a) taps-only control",
        f"- full (pat-both m1, S0.10 fine): median {t['full_fine_median']:.3e}"
        f" | taps-only: median {t['tapsonly_fine_median']:.3e}",
        f"- paired CI (tapsonly − full), eval-F: "
        f"[{t['paired_ci_tapsonly_minus_full_fine'][0]:+.2e}, "
        f"{t['paired_ci_tapsonly_minus_full_fine'][1]:+.2e}] "
        f"(median diff {t['median_diff_fine']:+.2e})",
        f"- coarse co-report: full {t['full_coarse_median']:.3e} vs "
        f"taps-only {t['tapsonly_coarse_median']:.3e}",
        f"- **verdict (frozen 18.6a rule): {t['verdict_18_6a']}**", "",
        "## (b) N_eff readout ablation",
    ]
    for s in ("patC2", "spsaC2"):
        a = out[f"neff_{s}"]
        lines.append(
            f"- {s}: N_eff median {a['n_eff_median']} "
            f"(range {a['n_eff_range']}); refit recovers any: "
            f"{a['refit_recovers_any']}; SER holds ≤2× its k=0 baseline "
            f"up to k={a['k_hold_2x_baseline_median']} (median); "
            f"fingerprints all bit: {a['fingerprints_all_bit']}")
    with open("results/s0_11/s0_11b.md", "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
