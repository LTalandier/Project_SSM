#!/usr/bin/env python3
# NEW (Stage 0c, S0c.0-c, 2026-09-15) — FSR-matched inline envelope under PR-22
# (shared/preregistration.md, FROZEN 2026-09-15 before this script's first run).
# ARITHMETIC ONLY. Rows: PR-10, docs/s0b/s0b_0_ledger.md, docs/s0c/*.md.
"""Stage 0c / S0c.0: does an inline, passive, low-Q (K = 5-20 %) SiN ring-lattice
equalizer at 32-100 GS/s clear the per-tap digital block it would replace
(function-matched via eta_IIR), with actuator hold, drift management, insertion
loss (amplifier where > 3 dB) charged?  Run: python3 analysis/s0c_0_envelope.py
"""
from __future__ import annotations
import json, math, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..", "results", "s0c_0")
os.makedirs(OUT, exist_ok=True)
PJ = 1e-12
CORNERS = ("OPT", "CONS")
CH = {"OPT": 2, "CONS": 4}
N_GRID = (8, 16, 32)
FS_GRID = (32e9, 64e9, 100e9)
K_GRID = (0.05, 0.10, 0.20)
IL_RING_DB = {0.05: 0.62, 0.10: 0.31, 0.20: 0.15}          # mapping memo §4
HOLD_MW = {"A": {"OPT": 62.0, "CONS": 177.0}, "B": {"OPT": 3.0, "CONS": 3.0},
           "Cpz": {"OPT": 0.1, "CONS": 2.0}, "Cpcm": {"OPT": 0.0, "CONS": 0.0}}
CLASSES = ("A", "B", "Cpz", "Cpcm")
VERDICT_CLASSES = ("B", "Cpz", "Cpcm")
DRIFT = {"TEC": {"OPT": 180.0, "CONS": 180.0}, "GHEAT": {"OPT": 10.0, "CONS": 50.0},
         "TRACK": {"OPT": 1.3, "CONS": 13.0}, "ATHERMAL": {"OPT": 0.0, "CONS": 0.0}}
TRACK_OK = {"A", "B", "Cpz"}
UNSOURCED_DRIFT = {"GHEAT", "TRACK"}
SOURCED_DRIFT = {"TEC", "ATHERMAL"}
RETRAIN_MW = {"OPT": 2.6 / 100 + 130 * 22.5e-3 / 100, "CONS": 99 / 100 + 130 * 22.5e-3 / 100}
PKG_DB = {"OPT": 0.3, "CONS": 3.0}
AMP_MW = {"OPT": 20.0, "CONS": 300.0}                      # UNSOURCED-typical
ETA = {"OPT": 4.0, "CONS": 2.0}
E_TAP = {"OPT": 0.05, "CONS": 0.15}
E_TAP_SENS = (0.03, 0.25)
DSP_SHARE_PJ_PER_SAMPLE = 1.25
BAR = 3.0


def il_total_db(n, k, corner):
    return n * IL_RING_DB[k] + PKG_DB[corner]


def p_total_mw(cls, corner, n, k, drift):
    p = n * CH[corner] * HOLD_MW[cls][corner] + DRIFT[drift][corner] + RETRAIN_MW[corner]
    if il_total_db(n, k, corner) > 3.0:
        p += AMP_MW[corner]
    return p


def rows(corner, eta=None, e_tap=None, drop_unsourced=False):
    out = []
    for cls in CLASSES:
        for drift in DRIFT:
            if drift == "TRACK" and cls not in TRACK_OK:
                continue
            if drop_unsourced and drift in UNSOURCED_DRIFT:
                continue
            for n in N_GRID:
                for k in K_GRID:
                    for fs in FS_GRID:
                        p = p_total_mw(cls, corner, n, k, drift)
                        if drop_unsourced and corner == "OPT" and cls == "Cpz":
                            p += n * CH[corner] * (HOLD_MW["Cpz"]["CONS"] - HOLD_MW["Cpz"]["OPT"])
                        eph = p * 1e-3 / fs / PJ
                        taps = (eta or ETA[corner]) * n
                        edig = taps * (e_tap or E_TAP[corner])
                        r = edig / eph
                        out.append(dict(corner=corner, cls=cls, drift=drift, N=n, K=k, fs=fs / 1e9,
                                        IL_dB=il_total_db(n, k, corner), amp=il_total_db(n, k, corner) > 3.0,
                                        P_mW=p, E_ph=eph, taps=taps, E_dig=edig, ratio=r,
                                        clears=r >= BAR, edge=(fs == 100e9)))
    return out


def best(rs, classes, drifts=None):
    c = [r for r in rs if r["cls"] in classes and (drifts is None or r["drift"] in drifts)]
    return max(c, key=lambda r: r["ratio"]) if c else None


def f(x):
    return "—" if x is None else (f"{x:,.0f}" if abs(x) >= 100 else f"{x:.3g}")


L = []
P = L.append
P("# S0c.0 — FSR-matched inline envelope (PR-22, frozen 2026-09-15)\n")
P("Arithmetic only; rows and statuses in `docs/s0b/s0b_0_ledger.md`, `docs/s0c/fsr_matched_regime.md`, "
  "`docs/s0c/mapping_fsr_matched.md`; rules in PR-22.\n")
P("## 1. Insertion loss [dB] (lattice + packaging) and whether the amplifier row is charged\n")
P("| N | K | OPT IL | amp? | CONS IL | amp? |")
P("|---|---|---|---|---|---|")
for n in N_GRID:
    for k in K_GRID:
        a, b = il_total_db(n, k, "OPT"), il_total_db(n, k, "CONS")
        P(f"| {n} | {k:.0%} | {a:.2f} | {'yes' if a > 3 else 'no'} | {b:.2f} | {'yes' if b > 3 else 'no'} |")
P("")
res = {"meta": {"task": "S0c.0", "date": "2026-09-15", "frozen": "PR-22", "bar": BAR}, "cells": {}, "verdicts": {}}
for corner in CORNERS:
    rs = rows(corner)
    res["cells"][corner] = rs
    P(f"## 2.{1 if corner == 'OPT' else 2} Clearance — {corner} (ratio = E_digital/E_photonic; η = {ETA[corner]:g} taps/ring; "
      f"e_tap {E_TAP[corner]} pJ; showing 64 GS/s cells plus any other cell that clears)\n")
    P("| class | drift | N | K | GS/s | IL dB | amp | P mW | E_ph pJ | taps | E_dig pJ | ratio | verdict |")
    P("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rs:
        if r["fs"] != 64 and not r["clears"]:
            continue
        if r["K"] != 0.10 and not r["clears"]:
            continue
        P(f"| {r['cls']} | {r['drift']} | {r['N']} | {r['K']:.0%} | {r['fs']:g} | {r['IL_dB']:.1f} | "
          f"{'y' if r['amp'] else 'n'} | {f(r['P_mW'])} | {f(r['E_ph'])} | {r['taps']:g} | {f(r['E_dig'])} | "
          f"{r['ratio']:.2f} | {'CLEARS' if r['clears'] else 'LOSES'}{' (edge)' if r['edge'] and r['clears'] else ''} |")
    P("")
P(f"Secondary anchor (SJTU convention): DSP CD share ≈ {DSP_SHARE_PJ_PER_SAMPLE} pJ/sample at 56 GBd PAM4 — "
  "compare with the E_ph column directly.\n")

opt = res["cells"]["OPT"]; cons = res["cells"]["CONS"]
kill_best = best(opt, VERDICT_CLASSES)
kill = kill_best is None or kill_best["ratio"] < BAR
win_sourced = best(cons, VERDICT_CLASSES, SOURCED_DRIFT)
win_any = best(cons, VERDICT_CLASSES)
window_sourced = win_sourced is not None and win_sourced["ratio"] >= BAR
window_any = win_any is not None and win_any["ratio"] >= BAR
sens = {}
for corner in CORNERS:
    for e in E_TAP_SENS:
        b = best(rows(corner, eta=2.0, e_tap=e, drop_unsourced=True), VERDICT_CLASSES)
        sens[f"{corner}@eta2@{e}"] = b
# count of clearing CONS cells under sourced drift, by class and drift
clear_cons = [r for r in cons if r["clears"] and r["cls"] in VERDICT_CLASSES and r["drift"] in SOURCED_DRIFT]

P("## 3. Verdicts (PR-22 §22.4)\n")
P(f"**Kill gate (OPT, classes B/C-pz/C-pcm, any drift):** max ratio = **{kill_best['ratio']:.2f}** at "
  f"{kill_best['cls']}/{kill_best['drift']}, N={kill_best['N']}, K={kill_best['K']:.0%}, {kill_best['fs']:g} GS/s "
  f"(P {f(kill_best['P_mW'])} mW → {f(kill_best['E_ph'])} pJ vs {f(kill_best['E_dig'])} pJ). **Kill fires: {kill}.**\n")
P(f"**CONS window, sourced drift (TEC/ATHERMAL):** max ratio = **{win_sourced['ratio']:.2f}** at "
  f"{win_sourced['cls']}/{win_sourced['drift']}, N={win_sourced['N']}, K={win_sourced['K']:.0%}, {win_sourced['fs']:g} GS/s. "
  f"**Window exists: {window_sourced}** ({len(clear_cons)} clearing cells"
  + (", incl. band-edge 100 GS/s cells" if any(r['edge'] for r in clear_cons) else "") + ").\n")
P(f"**CONS window, any drift (incl. UNSOURCED):** max ratio = **{win_any['ratio']:.2f}** at "
  f"{win_any['cls']}/{win_any['drift']}, N={win_any['N']}. Window: {window_any}.\n")
P("**Sensitivity (UNSOURCED rows removed; η = 2 both corners; e_tap at band ends):**\n")
P("| corner | e_tap | max ratio | at |")
P("|---|---|---|---|")
for key, b in sens.items():
    corner, _, e = key.split("@")
    P(f"| {corner} | {e} | {b['ratio']:.2f} | {b['cls']}/{b['drift']}, N={b['N']}, K={b['K']:.0%}, {b['fs']:g} GS/s |")
P("")
P("**Clearing CONS cells under sourced drift (the S0c.1 grid if go):**\n")
P("| class | drift | N | K | GS/s | ratio |")
P("|---|---|---|---|---|---|")
for r in sorted(clear_cons, key=lambda r: -r["ratio"])[:24]:
    P(f"| {r['cls']} | {r['drift']} | {r['N']} | {r['K']:.0%} | {r['fs']:g}{' (edge)' if r['edge'] else ''} | {r['ratio']:.2f} |")
res["verdicts"] = {"kill_best": kill_best, "kill_fires": kill, "cons_window_sourced_best": win_sourced,
                   "cons_window_sourced": window_sourced, "cons_window_any_best": win_any,
                   "cons_window_any": window_any, "sensitivity": sens,
                   "clearing_cons_sourced": clear_cons}
with open(os.path.join(OUT, "envelope.json"), "w") as fh:
    json.dump(res, fh, indent=2)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), sharey=True)
for ax, corner in zip(axes, CORNERS):
    for cls, col in (("B", "tab:blue"), ("Cpz", "tab:green"), ("Cpcm", "tab:purple"), ("A", "tab:red")):
        for drift, ls in (("ATHERMAL", "-"), ("TEC", "--")):
            ys = [next(r["ratio"] for r in res["cells"][corner]
                       if r["cls"] == cls and r["drift"] == drift and r["N"] == n and r["K"] == 0.10 and r["fs"] == 64)
                  for n in N_GRID]
            ax.plot(N_GRID, ys, ls, color=col, marker="o", label=f"{cls}/{drift}")
    ax.axhline(BAR, color="k", lw=1.5, label="bar 3×"); ax.axhline(1, color="k", lw=0.8, ls=":")
    ax.set_xscale("log", base=2); ax.set_yscale("log"); ax.set_xticks(N_GRID); ax.set_xticklabels(N_GRID)
    ax.set_xlabel("N rings (K = 10 %, 64 GS/s)"); ax.set_title(f"{corner} corner"); ax.grid(True, which="both", alpha=0.3)
axes[0].set_ylabel("E_digital / E_photonic"); axes[1].legend(fontsize=7, ncol=2)
fig.suptitle("S0c.0 FSR-matched inline envelope (PR-22): per-tap digital block (η·N taps) vs low-Q SiN lattice")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "s0c_0_ratio_vs_N.png"), dpi=160)
with open(os.path.join(OUT, "envelope.md"), "w") as fh:
    fh.write("\n".join(L) + "\n")
print("\n".join(L[L.index("## 3. Verdicts (PR-22 §22.4)\n"):]))
