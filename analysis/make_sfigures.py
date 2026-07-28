# NEW (P1 finalization, 2026-07-27) — main figure F8 (S0.9) + supplementary
# figures S1/S2/S3/S5 for the P1 manuscript. Same discipline as make_figures.py:
# every number is read from the frozen result files; nothing originates here.
#   F8  S0.9: mismatch-robust tie + drift trajectories (PR-5 SE / PR-16)
#   S1  G3 anchor-instability dossier: official-code EigenWorms reruns   (S0.2)
#   S2  PAT twin-mismatch decomposition at C-1 (+ rhel-ideal control)    (S0.5)
#   S3  PR-11 echo conjugation chain + per-cell feasibility ceilings     (S0.4c)
#   S4  — reserved slot (PR-14 bias/variance, deferred to S0.5-full): no figure.
#   S5  RHEL non-dissipative-limit recovery (R1 cosine sequence)         (S0.4c)
# Output: paper/figures/{F8,S1,S2,S3,S5}_{slug}.{png,pdf}

from __future__ import annotations

import glob
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "paper", "figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.size": 8.5, "axes.titlesize": 9, "axes.labelsize": 8.5,
    "legend.fontsize": 7.5, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 110, "savefig.dpi": 300,
})

COL = {"insitu-pat": "#1f77b4", "insitu-spsa": "#ff7f0e",
       "offline-relock": "#9467bd", "offline-head": "#c5a3d9"}
LBL = {"insitu-pat": "in-situ PAT", "insitu-spsa": "in-situ SPSA",
       "offline-relock": "offline + head-recal + re-lock",
       "offline-head": "offline + head-recal only"}


def jload(rel):
    with open(os.path.join(ROOT, rel)) as fh:
        return json.load(fh)


def save(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


# ---------------------------------------------------------------- F8 (S0.9)
def f8():
    # S0.10 (PR-17): eval-F protocol of record for this comparison
    a = jload("results/s0_10/analysis.json")
    target = a["ser_target"]
    ceiling = a["ceiling_fine"]["bptt"]["median_fine"]   # eval-F reference
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 2.9))

    # (a) mismatch sweep
    ax = axes[0]
    levels = a["s0_10a_mismatch_fine"]["levels"]
    ms = sorted(int(k) for k in levels)
    pct = [5 * m for m in ms]
    for arm, key, col in (("in-situ PAT", "insitu", COL["insitu-pat"]),
                          ("offline-deploy + head-recal", "offline",
                           COL["offline-relock"])):
        med = [levels[str(m)][f"{key}_median"] for m in ms]  # eval-F medians
        ax.plot(pct, med, "o-", color=col, label=arm, ms=4, zorder=3)
        for m, x in zip(ms, pct):
            seeds = levels[str(m)][f"{key}_per_seed"]
            ax.plot([x + (0.35 if key == "offline" else -0.35)] * len(seeds),
                    seeds, ".", color=col, alpha=0.35, ms=4, zorder=2)
    ax.axhline(target, color="0.3", lw=0.8, ls="--")
    ax.axhline(ceiling, color="0.3", lw=0.8, ls=":")
    ax.text(30.5, target, "target", va="center", fontsize=7, color="0.3")
    ax.text(30.5, ceiling, "ceiling (eval-F)", va="center", fontsize=7,
            color="0.3")
    ax.set_yscale("log")
    ax.set_ylim(4e-4, 1.2e-2)
    ax.set_xticks(pct)
    ax.set_xlabel("calibration-mismatch class (%)")
    ax.set_ylabel("median SER (8 seeds)")
    ax.set_title("(a) tie robust to calibration error at eval-F\n(crossover $m^*$ = none; all CIs include 0)")
    ax.legend(frameon=False, loc="upper left")

    # (b),(c) drift trajectories
    for ax, regime, panel in ((axes[1], "common", "(b)"),
                              (axes[2], "independent", "(c)")):
        reg = a["s0_10b_drift_fine"]["regimes"][regime]
        for arm in ("insitu-pat", "insitu-spsa", "offline-relock",
                    "offline-head"):
            traj = reg[arm]["median_traj"]
            ks = np.arange(1, len(traj) + 1)
            ax.plot(ks, traj, "o-", color=COL[arm], label=LBL[arm],
                    ms=3, lw=1.1)
        ax.axhline(target, color="0.3", lw=0.8, ls="--")
        ax.axhline(ceiling, color="0.3", lw=0.8, ls=":")
        ax.set_yscale("log")
        ax.set_ylim(3e-4, 3e-2)
        ax.set_xlabel("drift step $k$ ($\\sigma_{step}=0.40\\,\\kappa_i$)")
        adv = reg["advantage_vs_strong_offline"]
        ratio = adv["ratio"] if isinstance(adv, dict) and "ratio" in adv else None
        sub = {"common": "common-mode drift:\nre-lock absorbs it",
               "independent": "independent per-ring drift:\nre-lock cannot"}[regime]
        ax.set_title(f"{panel} {sub}")
        if regime == "common":
            ax.legend(frameon=False, fontsize=6.5, loc="upper left")
    axes[1].set_ylabel("median SER (8 seeds)")
    fig.tight_layout()
    save(fig, "F8_mismatch_drift")


# ---------------------------------------------------------------- S1 (G3)
PUBLISHED_SEEDS = ("2345", "3456", "4567", "5678", "6789")
PUB_MEAN, PUB_STD = 95.0, 4.4  # LinOSS EigenWorms, Rusch & Rus ICLR 2025


def s1():
    base = ("results/s0_2/gate_i/xcheck_official/outputs/LinOSS_IM/"
            "EigenWorms")
    dirs = {d.split("seed_")[-1]: d
            for d in glob.glob(os.path.join(ROOT, base, "*seed_*"))}
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.9),
                             gridspec_kw={"width_ratios": [1.6, 1.0]})

    ax = axes[0]
    finals = {}
    for i, seed in enumerate(PUBLISHED_SEEDS):
        val = np.load(os.path.join(dirs[seed], "all_val_metric.npy")) * 100
        test = float(np.load(os.path.join(dirs[seed], "test_metric.npy"))) * 100
        finals[seed] = test
        ax.plot(np.arange(len(val)), val, "-", lw=1.1,
                color=plt.cm.tab10(i), label=f"seed {seed}")
    ax.set_xlabel("validation checkpoint (official schedule, early-stopped)")
    ax.set_ylabel("validation accuracy (%)")
    ax.set_title("(a) official LinOSS-IM code, published seeds")
    ax.legend(frameon=False, fontsize=6.5, ncol=2, loc="lower right")

    ax = axes[1]
    xs = np.arange(len(PUBLISHED_SEEDS))
    vals = [finals[s] for s in PUBLISHED_SEEDS]
    ax.axhspan(PUB_MEAN - PUB_STD, PUB_MEAN + PUB_STD, color="0.9",
               label=f"published {PUB_MEAN}$\\pm${PUB_STD}")
    ax.axhline(PUB_MEAN, color="0.5", lw=0.8)
    ax.bar(xs, vals, color=["#1f77b4" if v > 90 else "#d62728" for v in vals],
           width=0.6)
    mean, std = float(np.mean(vals)), float(np.std(vals, ddof=1))
    ax.axhline(mean, color="k", lw=1.0, ls="--",
               label=f"rerun mean {mean:.2f} ($\\sigma$ {std:.2f})")
    ax.set_xticks(xs)
    ax.set_xticklabels(PUBLISHED_SEEDS, fontsize=6.5)
    ax.set_xlabel("published seed")
    ax.set_ylabel("test accuracy (%)")
    ax.set_ylim(70, 102)
    ax.set_title("(b) final test accuracy vs published")
    ax.legend(frameon=False, fontsize=6.5, loc="lower left")
    fig.tight_layout()
    save(fig, "S1_g3_anchor_dossier")


# ---------------------------------------------------------------- S2 (C-1 diag)
def s2():
    d = jload("results/s0_5/bakeoff_diag_c1.json")
    fine = jload("results/s0_10/analysis.json")["diag_c1_fine"]
    ceiling, target = d["_ref"]["c1_ceiling"], d["_ref"]["c1_target"]
    arms = ["pat-perfect", "pat-M-par", "pat-M-struct", "rhel-ideal"]
    labels = ["PAT\nperfect twin", "PAT\nM-par twin", "PAT\nM-struct twin",
              "RHEL\nideal conjugator"]
    cols = ["#1f77b4", "#5599cc", "#88bbdd", "#d62728"]
    fig, ax = plt.subplots(figsize=(4.4, 2.9))
    xs = np.arange(len(arms))
    for x, arm, c in zip(xs, arms, cols):
        med = fine[arm]["median_fine"]                 # eval-F (PR-17)
        ax.bar(x, med, width=0.62, color=c)
        seeds = fine[arm]["per_seed_fine"]
        ax.plot([x] * len(seeds), seeds, "k.", ms=5, alpha=0.6, zorder=3)
    ax.axhline(ceiling, color="0.3", lw=0.9, ls=":")
    ax.axhline(target, color="0.3", lw=0.9, ls="--")
    ax.text(len(arms) - 0.4, ceiling * 1.05, "C-1 ceiling (BPTT, coarse floor)",
            fontsize=6.5, color="0.3", ha="right", va="bottom")
    ax.text(len(arms) - 0.4, target * 1.05, "C-1 target", fontsize=6.5,
            color="0.3", ha="right", va="bottom")
    ax.set_yscale("log")
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_ylabel("final SER at eval-F (median, 3 seeds)")
    ax.set_title("C-1 diagnostic: twin-mismatch decomposition (eval-F)\n"
                 "(M-struct $\\equiv$ perfect; small M-par excess resolves; "
                 "channels grow with cell)")
    fig.tight_layout()
    save(fig, "S2_twin_mismatch_c1")


# ---------------------------------------------------------------- S3 (PR-11)
def s3():
    d = jload("results/s0_4c/pr11_recon_calc.json")
    smoke = jload("results/s0_4c/smoke.json")
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.9))

    # (a) conjugation-chain waterfall at the frozen operating point
    ax = axes[0]
    eta_ex = d["cells"]["C-2"]["eta_extraction_bus_fraction"]
    spiral = d["spiral_eta_c"]["Pp=0.3W,L=0.5m"]
    comps = [("extraction $\\eta_{ex}^2$", 20 * np.log10(eta_ex)),
             ("FWM spiral $\\eta$\n(0.3 W, 0.5 m)", 10 * np.log10(spiral)),
             ("routing/insertion\n($e^{-1}$)", 10 * np.log10(np.exp(-1)))]
    total = sum(v for _, v in comps)
    cum = 0.0
    for i, (lbl, v) in enumerate(comps):
        ax.bar(i, v, bottom=cum, width=0.6, color="#d62728", alpha=0.75)
        cum += v
    ax.bar(len(comps), total, width=0.6, color="0.25")
    ax.set_xticks(range(len(comps) + 1))
    ax.set_xticklabels([c[0] for c in comps] + ["chain $\\eta_c$"],
                       fontsize=6.5)
    ax.axhline(0, color="k", lw=0.6)
    for i, (_, v) in enumerate(comps + [("t", total)]):
        y = (sum(x for _, x in comps[:i]) + v if i < len(comps) else total)
        ax.text(i, y - 0.9, f"{v:.1f} dB", ha="center", fontsize=6.5)
    ax.set_ylabel("conjugation efficiency (dB)")
    ax.set_title("(a) echo conjugation chain (mechanism A,\nfrozen point "
                 f"$\\eta_c$ = {10*np.log10(np.prod([eta_ex**2, spiral, np.exp(-1)])):.1f} dB)")

    # (b) per-cell feasibility: Q_L ceiling + transit survival
    ax = axes[1]
    cells = ["C-1", "C-2", "C-3"]
    xs = np.arange(len(cells))
    ql = [d["cells"][c]["QL_ceiling_state_band"] for c in cells]
    ax.bar(xs - 0.18, np.array(ql) / 1e6, width=0.34, color="#1f77b4",
           label="resonant-ring $Q_L$ ceiling ($\\times 10^6$,\nstate-band, mech. B)")
    ax2 = ax.twinx()
    surv = [d["cells"][c]["transit_amp_survival"]["10.0ns"] for c in cells]
    ax2.bar(xs + 0.18, surv, width=0.34, color="#ff7f0e",
            label="10 ns off-chip transit\namplitude survival (mech. C)")
    ax2.set_ylim(0, 1.0)
    ax2.spines["top"].set_visible(False)
    ax.set_yscale("log")
    ax.set_xticks(xs)
    ax.set_xticklabels(cells)
    ax.set_ylabel("$Q_L$ ceiling ($\\times 10^6$)")
    ax2.set_ylabel("amplitude survival")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=6.2, loc="upper left")
    ax.set_title("(b) per-cell echo-feasibility ceilings")
    fig.tight_layout()
    save(fig, "S3_echo_chain")


# ---------------------------------------------------------------- S5 (R1)
def s5():
    smoke = jload("results/s0_4c/smoke.json")
    rows = sorted(smoke["R1_rows"], key=lambda r: r["kappa_net_T_dt"])
    x = [r["kappa_net_T_dt"] for r in rows]
    y = [r["cosine"] for r in rows]
    fig, ax = plt.subplots(figsize=(4.0, 2.8))
    ax.semilogx(x, y, "o-", color="#d62728", ms=5)
    for xi, yi in zip(x, y):
        ax.annotate(f"{yi:+.3f}", (xi, yi), textcoords="offset points",
                    xytext=(6, -9), fontsize=6.5)
    ax.axhline(1.0, color="0.3", lw=0.8, ls=":")
    ax.axhline(0.0, color="0.3", lw=0.6)
    ax.set_xlabel("dissipation per window  $\\kappa_{net} T\\, dt$")
    ax.set_ylabel("cosine(RHEL update, BPTT gradient)")
    ax.set_title("R1: exact recovery of the non-dissipative limit\n"
                 "(operating point sits at $\\kappa_{net} T dt \\approx 27$, "
                 "far right)")
    ax.set_ylim(-1.05, 1.15)
    fig.tight_layout()
    save(fig, "S5_rhel_r1_recovery")


if __name__ == "__main__":
    f8()
    s1()
    s2()
    s3()
    s5()
