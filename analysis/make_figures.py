# NEW (task S0.8, 2026-07-12) — publication figures F1-F7 for the P1 manuscript.
# Every number is read from the frozen result JSONs (or recomputed through the
# frozen substrate via the S0.4-0 calibration helpers); nothing originates here.
#   F1  architecture schematic + realizable pole/memory region      (S0.1)
#   F2  substrate: saturating kappa_net(r), clamp band, de-saturation (S0.4-0)
#   F3  participation profile: single-drive vs resolved 4-tap B      (S0.4-0)
#   F4  headline: SER vs device passes, all arms, C-2                (S0.5)
#   F5  ranking at matched cost + digital side-ledger                (S0.5)
#   F6  damping sweep: pinned vs boxed (R-ii)                        (S0.6)
#   F7  training-energy inversion + inference envelope               (S0.7)
# Output: paper/figures/F{n}_{slug}.{png,pdf}

from __future__ import annotations

import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "analysis"))
OUT = os.path.join(ROOT, "paper", "figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.size": 8.5, "axes.titlesize": 9, "axes.labelsize": 8.5,
    "legend.fontsize": 7.5, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 110, "savefig.dpi": 300,
})

COL = {"bptt": "0.15", "pat-both": "#1f77b4", "adjoint": "#2ca02c",
       "spsa": "#ff7f0e", "rhel": "#d62728", "head-only": "0.55",
       "offline-deploy": "#9467bd"}
LBL = {"bptt": "BPTT (exact-gradient reference)", "pat-both": "PAT",
       "adjoint": "adjoint", "spsa": "SPSA", "rhel": "RHEL (honest echo)",
       "head-only": "readout-only (reservoir)",
       "offline-deploy": "offline-train → deploy"}

SER_TARGET = 0.005651
CEILING = 0.00052083
BUDGET = 252_800


def jload(rel):
    with open(os.path.join(ROOT, rel)) as fh:
        return json.load(fh)


def save(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


# ---------------------------------------------------------------- F1
def f1():
    pole = jload("results/s0_1/s0_1_pole_region_data.json")
    dt_ns = pole["meta"]["dt_s"] * 1e9              # round-trip step, ns
    fig, (ax0, ax1) = plt.subplots(
        1, 2, figsize=(7.0, 2.6), gridspec_kw={"width_ratios": [1.5, 1.0]})

    # (a) schematic: chain of N=32 rings over a bus, taps highlighted
    N, taps = 32, {3, 12, 21, 30}                    # 1-based, resolved B
    ax0.set_xlim(-0.5, N + 4.5)
    ax0.set_ylim(-2.1, 1.9)
    ax0.axis("off")
    ax0.set_title("(a) trained partition $\\{\\delta_j, \\kappa_{{\\rm ext},"
                  "j}, \\mu_{jk}\\}$, per-ring saturating gain $g$",
                  fontsize=8, loc="left")
    ax0.plot([0.0, N + 0.8], [-0.75, -0.75], color="0.3", lw=1.4, zorder=1)
    xs = np.arange(1, N + 1)
    is_tap = np.array([j in taps for j in xs])
    for j in xs:
        ax0.plot([j, j], [-0.75, 0.12], color="0.75", lw=0.6, zorder=2)
    ax0.scatter(xs[~is_tap], np.full((~is_tap).sum(), 0.45), s=52,
                facecolors="white", edgecolors="0.35", lw=0.8, zorder=3)
    ax0.scatter(xs[is_tap], np.full(is_tap.sum(), 0.45), s=64,
                facecolors="#ffd8a8", edgecolors="#d9480f", lw=1.3,
                zorder=4)
    for j in sorted(taps):
        ax0.annotate("", xy=(j, -0.80), xytext=(j, -1.45),
                     arrowprops=dict(arrowstyle="-|>", color="#d9480f",
                                     lw=1.2))
    ax0.text(16.5, -1.85, "input $u_k$ at taps $\\{3,12,21,30\\}$",
             color="#d9480f", ha="center", fontsize=7.5)
    ax0.annotate("", xy=(N + 3.6, -0.75), xytext=(N + 0.8, -0.75),
                 arrowprops=dict(arrowstyle="-|>", color="0.3", lw=1.2))
    ax0.text(N + 2.4, -0.42, "linear\nhead $\\hat{y}_k$", ha="center",
             fontsize=6.8)
    for x, lab, ytip in ((5, "$\\delta_j$", 0.72),
                         (15.5, "$\\mu_{j,j+1}$", 0.62),
                         (26, "$\\kappa_{{\\rm ext},j}$", -0.25)):
        ax0.text(x, 1.28, lab, fontsize=8, ha="center")
        ax0.annotate("", xy=(x, ytip), xytext=(x, 1.18),
                     arrowprops=dict(arrowstyle="-|>", color="0.2", lw=0.8))

    # (b) memory vs intrinsic Q at three gain-compensation fractions
    Qi = np.array(pole["pole_region"]["Qi"])
    for gf, ls in (("0.0", ":"), ("0.5", "--"), ("0.9", "-")):
        mem_steps = np.array(pole["pole_region"]["gain_fraction"][gf]
                             ["memory_samples"])
        mem_samples = mem_steps * dt_ns / 0.5        # at 2 GS/s
        ax1.plot(Qi, mem_samples, ls, color="0.2", lw=1.1,
                 label=f"$g_f={gf}$")
    ax1.axhline(7, color="#d9480f", lw=0.9)
    ax1.text(1.7e5, 8.5, "task span (7 taps)", color="#d9480f", fontsize=7)
    for q, lab in ((2e6, "C-1"), (6.8e6, "C-2"), (3e7, "C-3")):
        ax1.axvline(q, color="0.75", lw=0.7, zorder=0)
        ax1.text(q, 1400, lab, fontsize=7, ha="center", color="0.4")
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlabel("intrinsic quality factor $Q_i$")
    ax1.set_ylabel("memory (samples at 2 GS/s)")
    ax1.set_title("(b) realizable memory region", fontsize=8, loc="left")
    ax1.legend(frameon=False, loc="upper left")
    save(fig, "F1_architecture_pole_region")


# ---------------------------------------------------------------- F2
def f2():
    import s0_4_0_calibration as cal
    calib = jload("results/s0_4_0/s0_4_0_calibration.json")
    it2 = calib["item2_r_min"]["C-2"]
    r_star, r_a, r_min = (it2["r_star_lasing"], it2["r_a_clause_a"],
                          it2["r_min"])

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(7.0, 2.6))

    # (a) on-resonance settled kappa_net(r) — saturating vs fixed plane
    rr = np.geomspace(0.105, 3.0, 36)
    knet = np.array([cal.kappa_net_over_ki("C-2", float(r)) for r in rr])
    ax0.plot(rr, 0.1 + 2 * rr, "--", color="0.55", lw=1.0,
             label="fixed-gain plane $0.1 + 2r$")
    ax0.plot(rr, knet, "-", color="#1f77b4", lw=1.4,
             label="saturating (settled)")
    ax0.axhline(0, color="0.3", lw=0.7)
    ax0.axvspan(0.1, r_star, color="#ffc9c9", alpha=0.7, lw=0)
    ax0.axvspan(r_a, r_min, color="#ffe066", alpha=0.6, lw=0)
    ax0.axvline(r_star, color="#e03131", lw=0.9)
    ax0.axvline(0.3, color="0.4", lw=0.8, ls=":")
    ax0.axvline(2.0, color="#2ca02c", lw=0.8, ls=":")
    ax0.text(r_star * 1.06, 3.3, "$r^*$ (lasing)", color="#e03131",
             fontsize=7, rotation=90, va="bottom")
    ax0.text(r_min * 1.02, 2.4, "clamp band\n$[r_a, r_{\\min}]$",
             fontsize=6.5, color="#997a00")
    ax0.text(0.3, 0.045, " $\\theta_0$", fontsize=7, color="0.35")
    ax0.text(2.0, 0.045, " $r^*_{\\rm damp}$ (§6)", fontsize=7,
             color="#2ca02c")
    ax0.set_xscale("log")
    ax0.set_xlabel("drive ratio $r = \\kappa_{\\rm ext}/\\kappa_i$")
    ax0.set_ylabel("$\\kappa_{\\rm net}/\\kappa_i$ (on resonance)")
    ax0.set_title("(a) operating plane and lasing clamp", fontsize=8,
                  loc="left")
    ax0.legend(frameon=False, loc="upper left")

    # (b) off-resonance de-saturation at r_min vs theta0 (anchor-risk vii)
    sweep = calib["item3_delta_desaturation"]["sweep_at_r_min"]
    dl = np.array([p["delta_over_ki"] for p in sweep])
    kn = np.array([p["kappa_net_over_ki"] for p in sweep])
    row_t0 = cal.delta_desaturation_row("C-2", 0.3, n_pts=41)
    dl2 = np.array([p["delta_over_ki"] for p in row_t0["sweep"]]) \
        if "sweep" in row_t0 else None
    ax1.plot(dl, kn, "-", color="#e03131", lw=1.4,
             label=f"at $r_{{\\min}}={r_min:.3f}$")
    if dl2 is not None:
        kn2 = np.array([p["kappa_net_over_ki"] for p in row_t0["sweep"]])
        ax1.plot(dl2, kn2, "-", color="0.35", lw=1.1,
                 label="at $\\theta_0$ ($r=0.3$)")
    ax1.axhline(0, color="0.3", lw=0.7)
    ax1.fill_between(dl, np.minimum(kn, 0), 0, color="#ffc9c9", alpha=0.8)
    ax1.text(0, -0.40, "net gain (de-saturated)\nanchor-risk (vii)",
             ha="center", fontsize=6.5, color="#c92a2a")
    ax1.set_xlabel("detuning $\\delta/\\kappa_i$")
    ax1.set_ylabel("$\\kappa_{\\rm net}/\\kappa_i$")
    ax1.set_title("(b) off-resonance de-saturation", fontsize=8, loc="left")
    ax1.legend(frameon=False, loc="upper center")
    save(fig, "F2_substrate_clamp")


# ---------------------------------------------------------------- F3
def f3():
    calib = jload("results/s0_4_0/s0_4_0_calibration.json")
    it1 = calib["item1_controllability"]
    single = np.array(it1["registered_search_trace"][0]
                      ["grad_ratio_vs_ring1"])
    fin = next(f for f in it1["finalist_robustness"]
               if f["taps_1based"] == [3, 12, 21, 30])
    resolved = np.array(fin["per_ring_min_ratio"])
    rings = np.arange(1, 33)

    fig, ax = plt.subplots(figsize=(4.6, 2.8))
    floor = 1e-16
    ax.semilogy(rings, np.maximum(single, floor), "o-", ms=3, lw=0.9,
                color="0.45", label="single drive (ring 1)")
    ax.semilogy(rings, resolved, "s-", ms=3.5, lw=1.1, color="#d9480f",
                label="resolved $B$: taps $\\{3,12,21,30\\}$ "
                      "(min over 5 seeds)")
    ax.axhline(1e-3, color="#1f77b4", lw=1.0, ls="--")
    ax.text(32.2, 1.3e-3, "gate $10^{-3}$", color="#1f77b4", fontsize=7,
            va="bottom", ha="right")
    for t in (3, 12, 21, 30):
        ax.axvline(t, color="#ffd8a8", lw=3.5, zorder=0)
    n_trunc = int((single < floor).sum())
    ax.annotate(f"single-drive tail continues to $\\sim10^{{-25}}$\n"
                f"({n_trunc} rings below axis)",
                xy=(24, 2e-16), fontsize=6.5, color="0.45", ha="center")
    ax.set_ylim(floor / 3, 4)
    ax.set_xlim(0.5, 32.5)
    ax.set_xlabel("ring index $j$")
    ax.set_ylabel("per-ring gradient ratio (vs max ring)")
    ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0))
    save(fig, "F3_participation_profile")


# ---------------------------------------------------------------- F4/F5
def load_traces(method, cell="C-2"):
    runs_dir = os.path.join(ROOT, "results", "s0_5", "runs")
    out = []
    for fn in sorted(os.listdir(runs_dir)):
        if fn.startswith(f"{method}_{cell}_") and fn.endswith(".json") \
                and "fixed" not in fn:
            r = json.load(open(os.path.join(runs_dir, fn)))
            tr = np.array(r["eval_trace"], dtype=float)   # it, passes, ser
            out.append(tr)
    return out


def f4():
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    order = ["pat-both", "adjoint", "spsa", "offline-deploy",
             "head-only", "rhel"]
    for m in order:
        traces = load_traces(m)
        if not traces:
            continue
        grid = traces[0][:, 1]
        sers = np.stack([np.interp(grid, t[:, 1], t[:, 2]) for t in traces])
        med = np.median(sers, axis=0)
        q1, q3 = np.percentile(sers, [25, 75], axis=0)
        ls = "--" if m in ("bptt", "offline-deploy") else "-"
        ax.plot(grid, np.maximum(med, 2e-4), ls, color=COL[m], lw=1.3,
                label=LBL[m])
        ax.fill_between(grid, np.maximum(q1, 2e-4), np.maximum(q3, 2e-4),
                        color=COL[m], alpha=0.18, lw=0)
    ax.axhline(SER_TARGET, color="0.25", lw=0.9, ls=":")
    ax.text(8e2, SER_TARGET * 1.25, "pre-registered target", fontsize=7,
            color="0.25")
    ax.axhline(CEILING, color="0.25", lw=0.7, ls=":")
    ax.text(8e2, CEILING * 1.25, "BPTT ceiling (exact-gradient, digital)",
            fontsize=7, color="0.25")
    ax.axvline(BUDGET, color="0.6", lw=0.8)
    ax.text(BUDGET * 0.90, 0.5, "budget $B$", rotation=90, fontsize=7,
            color="0.5", va="top")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("device passes")
    ax.set_ylabel("held-out symbol-error rate")
    ax.set_xlim(7e2, 3.4e5)
    ax.set_ylim(2.5e-4, 1.1)
    ax.legend(frameon=False, loc="center left", bbox_to_anchor=(1.01, 0.5),
              fontsize=7.2)
    save(fig, "F4_sample_efficiency")


def f5():
    bo = jload("results/s0_5/bakeoff.json")["arms"]
    runs_passes = {}
    for m in ("pat-both", "adjoint", "spsa"):
        traces = load_traces(m)
        pts = []
        for t in traces:
            hit = t[t[:, 2] <= SER_TARGET]
            pts.append(hit[0, 1] if len(hit) else np.nan)
        runs_passes[m] = np.array(pts)

    order = ["pat-both", "adjoint", "spsa", "rhel"]
    ypos = np.arange(len(order))[::-1]
    fig, ax = plt.subplots(figsize=(4.8, 2.5))
    for y, m in zip(ypos, order):
        arm = bo[m]
        if arm["median_passes_censored_at_Bplus"] == "censored":
            ax.barh(y, BUDGET, color="none", edgecolor=COL[m], hatch="///",
                    lw=1.0, height=0.55)
            ax.text(5.2e4, y, "censored at $B$ (0/8)", va="center",
                    ha="center", fontsize=7, color=COL[m],
                    bbox=dict(facecolor="white", edgecolor="none", pad=1.2))
        else:
            med = arm["median_passes_censored_at_Bplus"]
            ax.barh(y, med, color=COL[m], alpha=0.75, height=0.55)
            ax.plot(runs_passes[m], [y] * 8, "o", ms=3, color="0.15",
                    zorder=5)
            ax.text(med * 1.05, y + 0.16,
                    f"{int(med):,} ({arm['success_fraction']*8:.0f}/8)",
                    va="center", fontsize=7)
        dig = arm["digital_passes"]
        if dig:
            ax.barh(y - 0.13, dig, color="none", edgecolor="0.4",
                    hatch="....", lw=0.8, height=0.22)
            ax.text(dig * 1.05, y - 0.22, f"digital ledger {dig:,}",
                    va="center", fontsize=6.3, color="0.35")
    ax.set_yticks(ypos)
    ax.set_yticklabels([LBL[m] for m in order], fontsize=8)
    ax.set_xscale("log")
    ax.set_xlim(1e4, 1.5e6)
    ax.set_xlabel("device passes to pre-registered target")
    save(fig, "F5_ranking")


# ---------------------------------------------------------------- F6
def f6():
    dj = jload("results/s0_6/damping.json")
    fig, ax = plt.subplots(figsize=(4.6, 2.9))
    for arm, col, lab, mk in (("pinned_curve", "0.35",
                               "$\\kappa_{\\rm ext}$ pinned at $r$", "o"),
                              ("boxed_curve", "#2ca02c",
                               "trained in box $[r_{\\min}, r]$", "s")):
        cur = dj[arm]
        items = sorted(cur.items(), key=lambda kv: float(kv[0]))
        rs = np.array([float(k) for k, _ in items])
        med = np.array([v["median_ser"] for _, v in items])
        lo = np.array([v["iqr"][0] for _, v in items])
        hi = np.array([v["iqr"][1] for _, v in items])
        plateau = np.array([v["no_plateau"] == 0 for _, v in items])
        ax.errorbar(rs, med, yerr=[med - lo, hi - med], fmt=mk + "-",
                    color=col, lw=1.2, ms=4, capsize=2, label=lab,
                    markerfacecolor="white", markeredgecolor=col)
        ax.plot(rs[plateau], med[plateau], mk, ms=4, color=col, zorder=5)
    try:                                # PR-17 T-A-L overlay (S0.10)
        tl = jload("results/s0_10/analysis.json")["talong"]["curve"]
        rs = np.array(sorted(float(r) for r in tl))
        med = np.array([tl[f"{r:g}"]["median_fine"] for r in rs])
        ax.plot(rs, med, "^--", color="#d62728", lw=1.1, ms=4,
                label="pinned, T-A-L (14-tap span, eval-F)")
    except FileNotFoundError:
        pass
    ax.axhline(CEILING, color="0.25", lw=0.7, ls=":")
    ax.text(0.205, CEILING * 1.25, "§5 ceiling", fontsize=7, color="0.25")
    ax.axvline(0.3, color="0.6", lw=0.7, ls=":")
    ax.text(0.3, 0.62, " $\\theta_0$", fontsize=7, color="0.5")
    ax.annotate("$r^* = 2.0$ (deep overcoupling,\n$\\approx$6 samples memory at\n"
                "measured $\\kappa_{net} = 3.7\\kappa_i$)", xy=(2.0, 1.3e-3), xytext=(0.55, 2.2e-2),
                fontsize=7, arrowprops=dict(arrowstyle="-|>", color="0.3",
                                            lw=0.8))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([0.2, 0.3, 0.5, 1.0, 2.0, 3.0])
    ax.set_xticklabels(["0.2", "0.3", "0.5", "1", "2", "3"])
    ax.set_xlabel("damping point / box edge  $r = \\kappa_{\\rm ext}/"
                  "\\kappa_i$")
    ax.set_ylabel("median SER (8 seeds)")
    ax.legend(frameon=False, loc="upper right", fontsize=7.5)
    ax.text(0.2, 1.4e-4,
            "open markers: not fully plateaued at budget (flagged)",
            fontsize=6.3, color="0.4")
    ax.set_ylim(1e-4, 1.4)
    save(fig, "F6_damping")


# ---------------------------------------------------------------- F7
def f7():
    env = jload("results/s0_7/training_envelope.json")
    tr = env["training_energy_to_target"]
    lite = jload("results/s0_7/s0_7_lite_envelope.json")

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(7.0, 2.8))

    # (a) training energy to target — the inversion
    methods = ["pat-both", "adjoint", "spsa"]
    x = np.arange(len(methods))
    conv_opt = [tr[m]["conversion_OPT_uJ"] * 1e-6 for m in methods]
    conv_cons = [tr[m]["conversion_CONS_uJ"] * 1e-6 for m in methods]
    ax0.bar(x - 0.18, conv_opt, 0.32,
            color=[COL[m] for m in methods], alpha=0.9,
            label="conversion, OPT corner")
    ax0.bar(x + 0.18, conv_cons, 0.32,
            color=[COL[m] for m in methods], alpha=0.35,
            label="conversion, CONS corner")
    dig_lo = tr["pat-both"]["digital_J_accel_1TFLOPSW_class"]
    dig_hi = tr["pat-both"]["digital_J_Brainwave_287GFLOPSW"]
    ax0.bar([0], [dig_hi - dig_lo], 0.7, bottom=[dig_lo], color="none",
            edgecolor="0.25", hatch="....", lw=0.9)
    ax0.annotate("PAT digital-twin ledger 13–44 J", xy=(0.36, 25),
                 xytext=(0.62, 220), fontsize=7,
                 arrowprops=dict(arrowstyle="-|>", color="0.3", lw=0.8))
    ax0.set_yscale("log")
    ax0.set_ylim(1e-4, 3e3)
    ax0.set_xticks(x)
    ax0.set_xticklabels([LBL[m] for m in methods])
    ax0.set_ylabel("training energy to target (J)")
    ax0.set_title("(a) training: the energy metric inverts the rank",
                  fontsize=8, loc="left")
    ax0.legend(frameon=False, fontsize=6.8, loc="center right")

    # (b) inference per-sample energy vs N at 2 GS/s (lite, OPT x class-B)
    Ns = [8, 32, 128]
    ph = [np.mean(lite["photonic"]["OPTxB"][f"N{n}@2"]) for n in Ns]
    bw = [np.mean(lite["baselines"]["OPT"][f"N{n}"]["Brainwave"])
          for n in Ns]
    js = [np.mean(lite["baselines"]["OPT"][f"N{n}"]["Jetson-sustained"])
          for n in Ns]
    jp = [np.mean(lite["baselines"]["OPT"][f"N{n}"]["Jetson-peak"])
          for n in Ns]
    dsp = [lite["baselines"]["OPT"][f"N{n}"]["DSP-ASIC-class"] for n in Ns]
    ax1.plot(Ns, ph, "o-", color="#1f77b4", lw=1.5,
             label="photonic SSM (OPT, class-B heaters)")
    ax1.plot(Ns, bw, "s--", color="0.3", lw=1.1, label="Brainwave (batch-1)")
    ax1.plot(Ns, js, "^--", color="0.55", lw=1.1, label="Jetson sustained")
    ax1.plot(Ns, jp, "v:", color="0.55", lw=1.1, label="Jetson peak")
    ax1.fill_between(Ns, [d[0] for d in dsp], [d[1] for d in dsp],
                     color="#e9c46a", alpha=0.35, lw=0,
                     label="DSP-ASIC class")
    ax1.set_xscale("log", base=2)
    ax1.set_yscale("log")
    ax1.set_xticks(Ns)
    ax1.set_xticklabels([str(n) for n in Ns])
    ax1.set_xlabel("state dimension $N$")
    ax1.set_ylabel("energy per sample (pJ), 2 GS/s")
    ax1.set_title("(b) inference envelope at 2 GS/s", fontsize=8,
                  loc="left")
    ax1.legend(frameon=False, fontsize=6.5, loc="upper left")
    save(fig, "F7_envelope")


if __name__ == "__main__":
    which = sys.argv[1:] or ["f1", "f2", "f3", "f4", "f5", "f6", "f7"]
    for w in which:
        globals()[w]()
