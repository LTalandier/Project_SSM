#!/usr/bin/env python3
# NEW (Stage 0b, S0b.0, 2026-09-13) — inline-scope re-envelope under PR-20
# (shared/preregistration.md, FROZEN 2026-09-13). ARITHMETIC ONLY: no
# simulation, no new sourcing. Every constant carries its ledger row
# (docs/s0b/s0b_0_ledger.md §) or its PR-10 frozen-row origin. Rows flagged
# UNSOURCED in the ledger are removed in the mandatory sensitivity
# re-statement (PR-20 §20.5).
"""Stage 0b / S0b.0: does an inline, passive-or-pumped, class-A/B/C-actuated
ring-lattice filter on SiN clear the digital equalizer block it would
replace, priced per tap, with every former exclusion charged?

Run: python3 analysis/s0b_0_envelope.py   -> results/s0b_0/{envelope.md,
envelope.json, s0b_0_ratio_vs_taps.png}
"""
from __future__ import annotations

import json
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..", "results", "s0b_0")
os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------ frozen rows
CORNERS = ("OPT", "CONS")
CH_PER_RING = {"OPT": 2, "CONS": 4}                 # PR-10 C2
CELL = {8: "C-1", 32: "C-2", 128: "C-3"}            # PR-4 R2
KAPPA_I = {8: 3.038e8, 32: 8.935e7, 128: 2.025e7}   # rad/s, registry (ledger §1 drift)
R_MIN = 0.1606                                       # S0.4-0 frozen
N_GRID = (8, 32, 128)
FS_GRID = (0.1e9, 1.0e9, 2.0e9)
N_TAPS = (4, 8, 16, 32, 64, 128)
P1_TAPS = 8                                          # 7-tap task, N_eff 6-8

# per-control-channel hold [mW] incl. trim electronics (ledger §1)
HOLD_MW = {
    "A":    {"OPT": 60.0 + 2.0, "CONS": 175.0 + 2.0},
    "B":    {"OPT": 1.0 + 2.0,  "CONS": 1.0 + 2.0},
    "Cpz":  {"OPT": 0.1 + 20e-6, "CONS": 2.0 + 300e-6},   # OPT 0.1 = UNSOURCED
    "Cpcm": {"OPT": 0.0, "CONS": 0.0},
}
CLASSES = ("A", "B", "Cpz", "Cpcm", "hybrid")
CLASS_C = ("Cpz", "Cpcm", "hybrid")
UNSOURCED_CPZ_OPT = True

# common-mode drift options [mW] (ledger §3)
DRIFT_CM = {
    "TEC":   {"OPT": 180.0, "CONS": 180.0},   # VERIFIED
    "GHEAT": {"OPT": 10.0,  "CONS": 50.0},    # UNSOURCED
    "TRACK": {"OPT": 1.3,   "CONS": 13.0},    # duty UNSOURCED; A/B/Cpz only
}
TRACK_OK = {"A", "B", "Cpz"}
RETRAIN_E_MJ = {"OPT": 2.6, "CONS": 99.0}     # §7.3 SPSA stack
MCU_MW, EP_S = 130.0, 22.5e-3
T_R_LADDER = (1.0, 10.0, 100.0, 1000.0)
T_R_DEFAULT, T_R_KILL = 100.0, 1000.0

# gain pump (ledger §2), electrical, per ring + module TEC
PUMP_MW_PER_RING = {"OPT": 0.8, "CONS": 17.0}
PUMP_TEC_MW = {"OPT": 0.0, "CONS": 180.0}
GAINS = ("passive", "pumped")

# digital block per tap per sample [pJ] (ledger §5)
E_TAP_PJ = {"OPT": 0.05, "CONS": 0.15}
E_TAP_SENS = (0.03, 0.25)
# secondary rows (PR-10, continuity only)
E_OP_BW_PJ = 1e12 / 287e9
DSP_BLOCK_PJ_PER_BIT = (25.0, 170.0)
ENOB = {"OPT": 9.4, "CONS": 8.4}

PKG_DB = {"OPT": 0.3, "CONS": 3.0}                   # ledger §4
CLEAR_RATIO = 3.0

PJ = 1e-12


# ------------------------------------------------------------- arithmetic
def hold_total_mw(cls, corner, n):
    ch = CH_PER_RING[corner]
    if cls == "hybrid":
        n_pz = min(4, n)
        return ch * (n_pz * HOLD_MW["Cpz"][corner] + (n - n_pz) * HOLD_MW["Cpcm"][corner])
    return n * ch * HOLD_MW[cls][corner]


def retrain_mw(corner, t_r):
    return RETRAIN_E_MJ[corner] / t_r + MCU_MW * EP_S / t_r


def pump_mw(gain, corner, n):
    if gain == "passive":
        return 0.0
    return n * PUMP_MW_PER_RING[corner] + PUMP_TEC_MW[corner]


def p_total_mw(cls, corner, n, gain, drift, t_r):
    return (hold_total_mw(cls, corner, n) + DRIFT_CM[drift][corner]
            + retrain_mw(corner, t_r) + pump_mw(gain, corner, n))


def e_ph_pj(p_mw, fs):
    return p_mw * 1e-3 / fs / PJ


def n_reach(n, fs, gain):
    k = (1.0 + 2 * R_MIN) * KAPPA_I[n] if gain == "passive" else (0.1 + 2 * R_MIN) * KAPPA_I[n]
    return int(math.floor(fs / k))


def e_dig_pj(n_taps, corner, e_tap=None):
    return n_taps * (E_TAP_PJ[corner] if e_tap is None else e_tap)


def drift_options(cls):
    return [d for d in DRIFT_CM if d != "TRACK" or cls in TRACK_OK]


def best_reachable_taps(n, fs, gain):
    r = n_reach(n, fs, gain)
    ok = [t for t in N_TAPS if t <= r]
    return (max(ok) if ok else None), r


# ---------------------------------------------------------------- sweeps
def cell_rows(corner, t_r, e_tap=None, drop_unsourced=False):
    rows = []
    for cls in CLASSES:
        for gain in GAINS:
            for drift in drift_options(cls):
                if drop_unsourced and drift in ("GHEAT", "TRACK"):
                    continue
                for n in N_GRID:
                    for fs in FS_GRID:
                        p = p_total_mw(cls, corner, n, gain, drift, t_r)
                        if drop_unsourced and UNSOURCED_CPZ_OPT and corner == "OPT" and cls in ("Cpz", "hybrid"):
                            ch = CH_PER_RING[corner]
                            n_pz = n if cls == "Cpz" else min(4, n)
                            p += n_pz * ch * (HOLD_MW["Cpz"]["CONS"] - HOLD_MW["Cpz"]["OPT"])
                        eph = e_ph_pj(p, fs)
                        taps, reach = best_reachable_taps(n, fs, gain)
                        edig = e_dig_pj(taps, corner, e_tap) if taps else float("nan")
                        ratio = edig / eph if taps else float("nan")
                        clears = bool(taps) and ratio >= CLEAR_RATIO and PKG_DB[corner] <= 3.0
                        rows.append(dict(corner=corner, cls=cls, gain=gain, drift=drift, N=n,
                                         fs_GSps=fs / 1e9, P_mW=p, E_ph_pJ=eph, N_reach=reach,
                                         best_taps=taps, E_dig_pJ=edig, ratio=ratio,
                                         clears=clears, t_r=t_r))
    return rows


def max_ratio(rows, classes=None, min_taps=None):
    best = None
    for r in rows:
        if classes and r["cls"] not in classes:
            continue
        if min_taps and (r["best_taps"] is None or r["best_taps"] < min_taps):
            continue
        if r["best_taps"] is None or math.isnan(r["ratio"]):
            continue
        if best is None or r["ratio"] > best["ratio"]:
            best = r
    return best


def fmt(x, d=3):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "—"
    if abs(x) >= 100:
        return f"{x:,.0f}"
    return f"{x:.{d}g}"


lines = []
P = lines.append
P("# S0b.0 — inline-scope re-envelope (PR-20, frozen 2026-09-13)\n")
P("Arithmetic only. Rows and statuses: `docs/s0b/s0b_0_ledger.md`. Rules: `shared/preregistration.md` PR-20.\n")

# --- reachability table
P("## 1. Reachability — N_reach = ⌊f_s / κ_net,min⌋ (single-ring amplitude memory at r_min = 0.1606)\n")
P("| N (cell) | gain | " + " | ".join(f"{fs/1e9:g} GS/s" for fs in FS_GRID) + " |")
P("|---|---|" + "---|" * len(FS_GRID))
for n in N_GRID:
    for gain in GAINS:
        P(f"| {n} ({CELL[n]}) | {gain} | " + " | ".join(str(n_reach(n, fs, gain)) for fs in FS_GRID) + " |")
P("")
P("Reading: passive C-2 reaches ≈ 17 taps at 2 GS/s, C-3 ≈ 75; pumped C-2 ≈ 53. N_taps = 128 is "
  "unreachable everywhere; 64 only at C-3 (passive) or pumped C-2/C-3.\n")

# --- static power decomposition at N=32, 2 GS/s, default T_r
P("## 2. Static + maintenance power decomposition [mW] at N = 32 (C-2), T_r = 100 s, passive\n")
P("| corner | class | hold (N·CH·per-ch) | drift: TEC / GHEAT† / TRACK† | retrain(100 s) | pump (passive) |")
P("|---|---|---|---|---|---|")
for corner in CORNERS:
    for cls in CLASSES:
        h = hold_total_mw(cls, corner, 32)
        d = " / ".join(fmt(DRIFT_CM[k][corner]) if (k != "TRACK" or cls in TRACK_OK) else "n/a"
                       for k in ("TEC", "GHEAT", "TRACK"))
        P(f"| {corner} | {cls} | {fmt(h)} | {d} | {fmt(retrain_mw(corner, T_R_DEFAULT))} | 0 |")
P("\n† UNSOURCED rows (ledger §3) — removed in the sensitivity re-statement (§6).\n")
P("Pumped configuration adds " + "; ".join(f"{corner}: {fmt(pump_mw('pumped', corner, 32))} mW at N = 32"
                                          for corner in CORNERS) + " (ledger §2) — reported, not the product configuration.\n")

# --- retrain ladder
P("## 3. Retraining maintenance power ladder [mW] (uncorrelated residual only)\n")
P("| T_r [s] | OPT | CONS |")
P("|---|---|---|")
for t in T_R_LADDER:
    P(f"| {t:g} | {fmt(retrain_mw('OPT', t))} | {fmt(retrain_mw('CONS', t))} |")
P("\nAt the drift anchor (one C-2 linewidth per ≈ 1 h) T_r ≈ 10²–10³ s suffices: the retraining term "
  "is sub-milliwatt at OPT and ≤ 1 mW at CONS for T_r ≥ 100 s. The common-mode term dominates.\n")

# --- digital block
P("## 4. Digital equalizer block, priced per tap [pJ/sample]\n")
P("| N_taps | OPT (0.05 pJ/tap) | CONS (0.15 pJ/tap) | P1 DSP-block row (25–170 pJ/bit × ENOB) |")
P("|---|---|---|---|")
for t in N_TAPS:
    blk = f"{DSP_BLOCK_PJ_PER_BIT[0]*ENOB['CONS']:.0f}–{DSP_BLOCK_PJ_PER_BIT[1]*ENOB['OPT']:.0f}"
    mark = " ← P1 point" if t == P1_TAPS else ""
    P(f"| {t} | {fmt(e_dig_pj(t,'OPT'))} | {fmt(e_dig_pj(t,'CONS'))} | {blk}{mark} |")
P("\nThe function-matched pricing is 30–100× harsher on the photonic side than P1's DSP-block row: P1 "
  "compared against a whole coherent DSP, not the equalizer it would replace.\n")

# --- main clearance tables
results = {"meta": {"task": "S0b.0", "date": "2026-09-13", "frozen": "PR-20 (2026-09-13)",
                    "ledger": "docs/s0b/s0b_0_ledger.md", "clear_ratio": CLEAR_RATIO},
           "reach": {f"N{n}/{g}": {f"{fs/1e9:g}": n_reach(n, fs, g) for fs in FS_GRID}
                     for n in N_GRID for g in GAINS},
           "cells": {}, "verdicts": {}}

for corner in CORNERS:
    rows = cell_rows(corner, T_R_DEFAULT)
    results["cells"][corner] = rows
    P(f"## 5.{'1' if corner=='OPT' else '2'} Clearance — {corner} corner, T_r = 100 s, best reachable N_taps per cell "
      f"(ratio = E_digital / E_photonic; clears iff ≥ {CLEAR_RATIO:g} and reachable; packaging {PKG_DB[corner]} dB)\n")
    P("| class | gain | drift | N | GS/s | P [mW] | E_ph [pJ] | N_reach | taps | E_dig [pJ] | ratio | verdict |")
    P("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        if r["fs_GSps"] < 2.0 and not r["clears"]:
            continue   # keep the table readable: sub-2 GS/s rows shown only if they clear
        v = "CLEARS" if r["clears"] else ("UNREACHABLE" if r["best_taps"] is None else "LOSES")
        P(f"| {r['cls']} | {r['gain']} | {r['drift']} | {r['N']} | {r['fs_GSps']:g} | {fmt(r['P_mW'])} | "
          f"{fmt(r['E_ph_pJ'])} | {r['N_reach']} | {r['best_taps'] or '—'} | {fmt(r['E_dig_pJ'])} | "
          f"{fmt(r['ratio'])} | {v} |")
    P("")
    P("(Rows below 2 GS/s omitted unless they clear — a fixed-power device only gets worse at lower rates.)\n")

# --- verdicts
opt_rows = cell_rows("OPT", T_R_KILL)
kill_best = max_ratio(opt_rows, classes=CLASS_C)
kill_fires = kill_best is None or kill_best["ratio"] < CLEAR_RATIO
cons_rows = results["cells"]["CONS"]
window_best = max_ratio(cons_rows, min_taps=16)
window = window_best is not None and window_best["ratio"] >= CLEAR_RATIO

# sensitivity: drop UNSOURCED rows (GHEAT, TRACK, Cpz-OPT hold), e_tap at band ends
sens = {}
for corner in CORNERS:
    for e_tap in E_TAP_SENS:
        rows = cell_rows(corner, T_R_KILL, e_tap=e_tap, drop_unsourced=True)
        b = max_ratio(rows, classes=CLASS_C)
        sens[f"{corner}@{e_tap}"] = b
best_ratio_unsourced_dropped_opt = sens[f"OPT@{E_TAP_SENS[1]}"]

P("## 6. Verdicts (PR-20 §20.5)\n")
if kill_best:
    P(f"**Kill gate (OPT, class C, T_r = 1000 s, best reachable taps):** maximum ratio = "
      f"**{kill_best['ratio']:.2f}** at {kill_best['cls']}/{kill_best['gain']}/{kill_best['drift']}, "
      f"N = {kill_best['N']}, {kill_best['fs_GSps']:g} GS/s, {kill_best['best_taps']} taps "
      f"(P = {fmt(kill_best['P_mW'])} mW → {fmt(kill_best['E_ph_pJ'])} pJ/sample vs digital "
      f"{fmt(kill_best['E_dig_pJ'])} pJ/sample). **Kill fires: {kill_fires}.**\n")
else:
    P("**Kill gate:** no reachable class-C cell at OPT. **Kill fires: True.**\n")
if window_best:
    P(f"**CONS product window (N_taps ≥ 16, all rows charged):** maximum ratio = "
      f"**{window_best['ratio']:.2f}** at {window_best['cls']}/{window_best['gain']}/{window_best['drift']}, "
      f"N = {window_best['N']}, {window_best['fs_GSps']:g} GS/s, {window_best['best_taps']} taps. "
      f"**Window exists: {window}.**\n")
else:
    P("**CONS product window:** no reachable cell with N_taps ≥ 16. **Window exists: False.**\n")
P("**Sensitivity re-statement (UNSOURCED rows removed: TEC-only drift, C-pz hold at the frozen 2 mW/ch "
  "at both corners; e_tap at the band ends):**\n")
P("| corner | e_tap [pJ] | max ratio (class C) | at |")
P("|---|---|---|---|")
for k, b in sens.items():
    corner, e = k.split("@")
    if b:
        P(f"| {corner} | {e} | {b['ratio']:.2f} | {b['cls']}/{b['gain']}/{b['drift']}, N={b['N']}, "
          f"{b['fs_GSps']:g} GS/s, {b['best_taps']} taps |")
    else:
        P(f"| {corner} | {e} | — | no reachable cell |")
P("")
results["verdicts"] = {
    "kill_gate_best": kill_best, "kill_fires": kill_fires,
    "cons_window_best": window_best, "cons_window_exists": window,
    "sensitivity": sens,
}

with open(os.path.join(OUT, "envelope.json"), "w") as f:
    json.dump(results, f, indent=2)

# --- one figure: ratio vs N_taps for the best class-C configuration per corner, 2 GS/s, N=32/128
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), sharey=True)
for ax, corner in zip(axes, CORNERS):
    for n, mk in ((32, "o"), (128, "s")):
        for cls, ls in (("Cpcm", "-"), ("hybrid", "--"), ("B", ":")):
            for drift, col in (("TEC", "tab:red"), ("GHEAT", "tab:orange"), ("TRACK", "tab:green")):
                if drift == "TRACK" and cls not in TRACK_OK:
                    continue
                p = p_total_mw(cls, corner, n, "passive", drift, T_R_DEFAULT)
                eph = e_ph_pj(p, 2e9)
                reach = n_reach(n, 2e9, "passive")
                xs = [t for t in N_TAPS if t <= reach]
                ys = [e_dig_pj(t, corner) / eph for t in xs]
                ax.plot(xs, ys, ls, color=col, marker=mk, ms=4, lw=1.2,
                        label=f"{cls}/{drift}, N={n}")
    ax.axhline(CLEAR_RATIO, color="k", lw=1.5, label="clears (≥3×)")
    ax.axhline(1.0, color="k", lw=0.8, ls="--")
    ax.set_xscale("log", base=2); ax.set_yscale("log")
    ax.set_xticks(N_TAPS); ax.set_xticklabels(N_TAPS)
    ax.set_xlabel("N_taps (reachable only), 2 GS/s, passive")
    ax.set_title(f"{corner} corner")
    ax.grid(True, which="both", alpha=0.3)
axes[0].set_ylabel("E_digital / E_photonic")
axes[1].legend(fontsize=6, ncol=2, loc="lower right")
fig.suptitle("S0b.0 inline re-envelope (PR-20): per-tap digital block vs photonic stage, all exclusions charged")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "s0b_0_ratio_vs_taps.png"), dpi=160)

with open(os.path.join(OUT, "envelope.md"), "w") as f:
    f.write("\n".join(lines) + "\n")
print("\n".join(lines))
print(f"\nWrote envelope.md, envelope.json, PNG to {os.path.normpath(OUT)}")
