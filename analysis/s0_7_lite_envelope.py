#!/usr/bin/env python3
# NEW (task S0.7L-1) — S0.7-lite systems-advantage envelope. ARITHMETIC +
# PLOTS ONLY: no simulation, no new sourcing. Every load-bearing constant
# below is a frozen PR-10 value (shared/preregistration.md, "PR-10 — FROZEN
# values", 2026-06-10) and carries its row reference; memo refs point into
# docs/s0_7/pr10_assumption_sources.md (the frozen block's source record).
# Mapping conventions C1-C8 are stated here and in the output memo per the
# frozen output convention ("the closest-workload mapping convention is
# stated in the output, not invented post hoc").
"""Render the S0.7-lite envelope (roadmap v3.1 S0.7-lite, F1/F16):

  energy/sample + latency/sample for the photonic SSM at the frozen scale
  grid (N in {8,32,128}; 0.1-2 GS/s; single-carrier-one-FSR), charged the
  full frozen conversion stack, at both corners (OPT/CONS) x both heater
  classes (A/B), vs the named PR-10 digital baselines; crossover rates and
  the section-10 escalation-clause check.

Writes markdown tables (stdout), JSON, and PNGs to results/s0_7/.
Run: python3 analysis/s0_7_lite_envelope.py
"""

from __future__ import annotations

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..", "results", "s0_7")
os.makedirs(OUT, exist_ok=True)

PJ = 1e-12

# ----------------------------------------------------------------------
# Frozen PR-10 rows. Brackets carried as (lo, hi); single values as (v, v).
# ----------------------------------------------------------------------

# Row "E/O incl. driver" [pJ/symbol] - memo S1 (1.4 / 1.5, 1.6).
EO_PJ = {"OPT": (0.135, 0.135), "CONS": (10.0, 20.0)}
# Row "O/E (PD+TIA)" [pJ/symbol] - memo S1 (1.8 / 1.9).
OE_PJ = {"OPT": (0.17, 0.17), "CONS": (1.4, 1.4)}
# Row "ADC at GS/s" [pJ/sample] + ENOB-at-speed - memo S2 (2.9 / 2.4-2.6).
ADC_PJ = {"OPT": (32.0, 32.0), "CONS": (469.0, 469.0)}
ENOB = {"OPT": 9.4, "CONS": 8.4}
# Row "DAC at GS/s" [pJ/sample] - memo S2 (2.10 / 2.7-2.8).
DAC_PJ = {"OPT": (5.0, 9.0), "CONS": (308.0, 308.0)}

# Rows "Heater class A/B" [mW/pi] - memo S4. Class A resolves per corner
# (convention C2): OPT -> 60 (registered measured-span low end), CONS -> 175
# (the registered foundry bound). Class B has no bracket (~1 mW/pi).
# Trim electronics 2 mW/ch charged in ALL scenarios (convention C3).
PPI_MW = {"A": {"OPT": 60.0, "CONS": 175.0}, "B": {"OPT": 1.0, "CONS": 1.0}}
TRIM_MW = 2.0
# Actuation time constants [s]: class B from its frozen row (0.4-2.6 ms);
# class A "fast tau" resolved by the frozen row's memo-S4 reference
# (38-110 us non-isolated class).
TAU_S = {"A": (38e-6, 110e-6), "B": (0.4e-3, 2.6e-3)}

# Row "Operating scale" - N grid, line-rate class, ch/ring, memory corners
# (mapping_result.md S4 via the frozen row's reference).
N_GRID = (8, 32, 128)
FS_GRID = (0.1e9, 1.0e9, 2.0e9)   # registered ends + 1 GS/s interior point
CH_PER_RING = {"OPT": 2, "CONS": 4}   # frozen bracket 2-4, resolved per C2
T_MEM_S = (3.29e-9, 49.4e-9)      # amplitude memory, foundry -> class-leading

# Row "Digital baselines (F16, named)" - memo S3; NOT corner-split.
E_OP_BW_PJ = 1e12 / 287e9          # Brainwave 287 GFLOPS/W (author-stated)
BW_LATENCY_S = 4e-3                # "<4 ms at batch 1" (memo row 3.1 quote)
E_OP_JET_PEAK_PJ = 1e12 / 4.6e12   # Jetson ~4.6 TOPS/W peak (registered derived)
JET_UTIL = 0.13                    # memo S3 caveat: peak != sustained; <13%
                                   # measured GPU utilization on small-batch RNNs
DSP_PJ_PER_BIT = (25.0, 170.0)     # coherent-DSP ASIC class bracket

# ----------------------------------------------------------------------
# Stated mapping conventions (C1-C8) - see memo section 2 for prose.
# C1 E/O + O/E charged per symbol (= per sample): cited pJ/bit are NRZ
#    per-symbol measurements; drive energy is per modulation event.
# C2 corner-bound bracket ends: within a corner every frozen bracket
#    resolves to its corner-consistent end (OPT favorable, CONS unfavorable);
#    bracket rows that stay wide at one corner (CONS E/O, OPT DAC, DSP class)
#    are carried as ranges through the arithmetic.
# C3 trim electronics (2 mW/ch) charged in all four scenarios (the frozen
#    figure is per-channel DAC quiescent, heater-class-independent).
# C4 holding power = full P_pi per control channel, 100% duty (streaming).
# C5 digital workload = diagonal complex SSM, ops/sample = 14*N
#    (state: a_j*x_j 6 ops + b_j*u 2 + add 2; readout Re(c_j*x_j) 3 + acc 1;
#    1 MAC = 2 ops, matching the FLOPS/TOPS conventions of the baselines).
# C6 DSP-class pJ/bit -> pJ/sample via bits/sample = corner ADC ENOB-at-speed
#    (the information content of one analog sample); N-independent anchor.
# C7 frozen converter pJ/sample used flat across the 0.1-2 GS/s grid
#    (favorable to the photonic side below the parts' native rates - flagged).
# C8 single DAC/ADC + E/O + O/E pair per sample (single-carrier-one-FSR
#    plan: the recurrence is fully optical; conversion is N-independent).
# ----------------------------------------------------------------------

SCENARIOS = [(c, h) for c in ("OPT", "CONS") for h in ("A", "B")]


def conv_pj(corner):
    lo = DAC_PJ[corner][0] + EO_PJ[corner][0] + OE_PJ[corner][0] + ADC_PJ[corner][0]
    hi = DAC_PJ[corner][1] + EO_PJ[corner][1] + OE_PJ[corner][1] + ADC_PJ[corner][1]
    return lo, hi


def ctrl_mw(corner, hclass, n_rings):
    per_ch = PPI_MW[hclass][corner] + TRIM_MW
    return n_rings * CH_PER_RING[corner] * per_ch


def e_photonic_pj(corner, hclass, n_rings, fs_hz):
    clo, chi = conv_pj(corner)
    e_ctrl = ctrl_mw(corner, hclass, n_rings) * 1e-3 / fs_hz / PJ
    return clo + e_ctrl, chi + e_ctrl


def baselines_pj(corner, n_rings):
    ops = 14 * n_rings
    return {
        "Brainwave": (ops * E_OP_BW_PJ,) * 2,
        "Jetson-peak": (ops * E_OP_JET_PEAK_PJ,) * 2,
        "Jetson-sustained": (ops * E_OP_JET_PEAK_PJ / JET_UTIL,) * 2,
        "DSP-ASIC-class": (DSP_PJ_PER_BIT[0] * ENOB[corner],
                           DSP_PJ_PER_BIT[1] * ENOB[corner]),
    }


def verdict(ph, base):
    if ph[1] < base[0]:
        return "CLEARS"
    if ph[0] > base[1]:
        return "LOSES"
    return "OVERLAP"


def f_cross_hz(corner, hclass, n_rings, e_base_pj, conv_end):
    """Rate above which the photonic side beats a (scalar) baseline energy."""
    p_w = ctrl_mw(corner, hclass, n_rings) * 1e-3
    margin_pj = e_base_pj - conv_pj(corner)[conv_end]
    return p_w / (margin_pj * PJ) if margin_pj > 0 else float("inf")


def fmt_rng(lo, hi, unit=""):
    if abs(hi - lo) < 1e-9:
        return f"{lo:,.0f}{unit}" if lo >= 10 else f"{lo:.3g}{unit}"
    return f"{lo:,.0f}-{hi:,.0f}{unit}" if lo >= 10 else f"{lo:.3g}-{hi:.3g}{unit}"


# ---------------------------------------------------------------- tables
results = {"meta": {
    "task": "S0.7L-1", "date": "2026-06-10",
    "frozen_source": "shared/preregistration.md PR-10 FROZEN 2026-06-10",
    "conventions": "C1-C8 (see script header / memo section 2)",
    "units": "pJ/sample unless noted",
}, "grid": {"N": list(N_GRID), "fs_GSps": [f / 1e9 for f in FS_GRID]},
    "photonic": {}, "baselines": {}, "clearance": {}, "crossover_GSps": {}}

print("## Per-scenario photonic energy/sample [pJ] (rows: N; cols: GS/s)\n")
for corner, hclass in SCENARIOS:
    key = f"{corner}x{hclass}"
    results["photonic"][key] = {}
    clo, chi = conv_pj(corner)
    print(f"### {key}  (conversion {fmt_rng(clo, chi)} pJ/sample; "
          f"control {ctrl_mw(corner, hclass, 1):,.0f} mW/ring x N)")
    print("| N | " + " | ".join(f"{f/1e9:g} GS/s" for f in FS_GRID) + " |")
    print("|---|" + "---|" * len(FS_GRID))
    for n in N_GRID:
        row = []
        for fs in FS_GRID:
            lo, hi = e_photonic_pj(corner, hclass, n, fs)
            results["photonic"][key][f"N{n}@{fs/1e9:g}"] = [lo, hi]
            row.append(fmt_rng(lo, hi))
        print(f"| {n} | " + " | ".join(row) + " |")
    print()

print("## Baseline energy/sample [pJ] (per corner where the C6 ENOB mapping applies)\n")
for corner in ("OPT", "CONS"):
    results["baselines"][corner] = {}
    print(f"### {corner} corner (DSP bits/sample = ENOB {ENOB[corner]})")
    names = list(baselines_pj(corner, N_GRID[0]).keys())
    print("| N | " + " | ".join(names) + " |")
    print("|---|" + "---|" * len(names))
    for n in N_GRID:
        b = baselines_pj(corner, n)
        results["baselines"][corner][f"N{n}"] = {k: list(v) for k, v in b.items()}
        print(f"| {n} | " + " | ".join(fmt_rng(*b[k]) for k in names) + " |")
    print()

print("## Clearance matrix (photonic conservative high end vs baseline; "
      "CLEARS / LOSES / OVERLAP)\n")
for corner, hclass in SCENARIOS:
    key = f"{corner}x{hclass}"
    results["clearance"][key] = {}
    print(f"### {key}")
    names = list(baselines_pj(corner, N_GRID[0]).keys())
    print("| N @ GS/s | " + " | ".join(names) + " |")
    print("|---|" + "---|" * len(names))
    for n in N_GRID:
        for fs in FS_GRID:
            ph = e_photonic_pj(corner, hclass, n, fs)
            b = baselines_pj(corner, n)
            vs = {k: verdict(ph, b[k]) for k in names}
            results["clearance"][key][f"N{n}@{fs/1e9:g}"] = vs
            print(f"| {n} @ {fs/1e9:g} | " + " | ".join(vs[k] for k in names) + " |")
    print()

print("## Crossover rate vs Brainwave [GS/s] (photonic high end; inf = never)\n")
print("| N | " + " | ".join(f"{c}x{h}" for c, h in SCENARIOS) + " |")
print("|---|" + "---|" * len(SCENARIOS))
for n in N_GRID:
    row = []
    for corner, hclass in SCENARIOS:
        e_bw = baselines_pj(corner, n)["Brainwave"][0]
        fx = f_cross_hz(corner, hclass, n, e_bw, conv_end=1)
        results["crossover_GSps"].setdefault(f"{corner}x{hclass}", {})[f"N{n}"] = (
            fx / 1e9 if fx != float("inf") else None)
        row.append(f"{fx/1e9:.2f}" if fx != float("inf") else "never")
    print(f"| {n} | " + " | ".join(row) + " |")
print()

# Section-10 escalation clause: does even the OPT corner (either heater
# class, photonic FAVORABLE low end) clear any baseline anywhere in the grid?
clause_clears = []
for hclass in ("A", "B"):
    for n in N_GRID:
        for fs in FS_GRID:
            ph = e_photonic_pj("OPT", hclass, n, fs)
            for bname, bval in baselines_pj("OPT", n).items():
                if ph[0] < bval[0]:   # favorable end vs baseline low end
                    clause_clears.append(f"OPTx{hclass} N={n} @{fs/1e9:g}GS/s vs {bname}")
results["s10_clause"] = {
    "fires": len(clause_clears) == 0,
    "n_clearing_cells": len(clause_clears),
    "examples": clause_clears[:8],
}
print(f"## Section-10 clause: fires = {len(clause_clears) == 0} "
      f"({len(clause_clears)} OPT grid cells clear at least one baseline)\n")

# Latency lower bounds (conversion pipeline latency is NOT a frozen row ->
# bound = ring amplitude-memory timescale + 1 sample period per converter).
results["latency_lb_ns"] = {}
print("## Photonic per-sample latency LOWER BOUND [ns] vs Brainwave <4 ms\n")
print("| GS/s | foundry corner (3.29 ns mem) | class-leading (49.4 ns mem) |")
print("|---|---|---|")
for fs in FS_GRID:
    lo = (T_MEM_S[0] + 2.0 / fs) / 1e-9
    hi = (T_MEM_S[1] + 2.0 / fs) / 1e-9
    results["latency_lb_ns"][f"{fs/1e9:g}"] = [lo, hi]
    print(f"| {fs/1e9:g} | {lo:.1f} | {hi:.1f} |")
print(f"\nBrainwave batch-1 serving latency: <{BW_LATENCY_S*1e3:.0f} ms "
      f"(author-stated) -> ratio ~1e5.\n")

# Memory depth in SAMPLES at each line rate (frozen memory corners x rate
# grid): couples the rate window to the platform corner for the S0.2 sizing.
results["memory_samples"] = {}
print("## Ring memory in samples at the line rate (T_mem x f_s)\n")
print("| GS/s | foundry corner (3.29 ns) | class-leading (49.4 ns) |")
print("|---|---|---|")
for fs in FS_GRID:
    lo, hi = T_MEM_S[0] * fs, T_MEM_S[1] * fs
    results["memory_samples"][f"{fs/1e9:g}"] = [lo, hi]
    print(f"| {fs/1e9:g} | {lo:.2f} | {hi:.1f} |")
print()

# SPSA-cadence consistency rows (heater-class tau -> 2 settles/iteration).
results["spsa_cadence_ms_per_iter"] = {
    h: [2 * TAU_S[h][0] * 1e3, 2 * TAU_S[h][1] * 1e3] for h in ("A", "B")}
print("## SPSA cadence floor (2 settles/iteration): "
      + "; ".join(f"class {h}: {2*TAU_S[h][0]*1e3:.2f}-{2*TAU_S[h][1]*1e3:.2f} ms"
                  for h in ("A", "B")) + "\n")

with open(os.path.join(OUT, "s0_7_lite_envelope.json"), "w") as f:
    json.dump(results, f, indent=2)

# ----------------------------------------------------------------- plots
SC_STYLE = {"OPTxB": ("tab:green", "-"), "OPTxA": ("tab:olive", "--"),
            "CONSxB": ("tab:blue", "-"), "CONSxA": ("tab:red", "--")}

fig, axes = plt.subplots(1, len(FS_GRID), figsize=(15, 4.6), sharey=True)
for ax, fs in zip(axes, FS_GRID):
    for corner, hclass in SCENARIOS:
        key = f"{corner}x{hclass}"
        los = [e_photonic_pj(corner, hclass, n, fs)[0] for n in N_GRID]
        his = [e_photonic_pj(corner, hclass, n, fs)[1] for n in N_GRID]
        c, ls = SC_STYLE[key]
        ax.plot(N_GRID, his, ls, color=c, marker="o", label=f"photonic {key}")
        ax.fill_between(N_GRID, los, his, color=c, alpha=0.25)
    bw = [14 * n * E_OP_BW_PJ for n in N_GRID]
    jp = [14 * n * E_OP_JET_PEAK_PJ for n in N_GRID]
    js = [v / JET_UTIL for v in jp]
    ax.plot(N_GRID, bw, "k-", lw=2, label="Brainwave 287 GFLOPS/W")
    ax.plot(N_GRID, jp, "k:", label="Jetson peak (4.6 TOPS/W)")
    ax.plot(N_GRID, js, "k-.", label="Jetson sustained (13% util)")
    ax.axhspan(DSP_PJ_PER_BIT[0] * ENOB["CONS"], DSP_PJ_PER_BIT[1] * ENOB["OPT"],
               color="gray", alpha=0.18, label="DSP-ASIC class (C6)")
    ax.set_xscale("log", base=2); ax.set_yscale("log")
    ax.set_xticks(N_GRID); ax.set_xticklabels(N_GRID)
    ax.set_xlabel("N rings / states"); ax.set_title(f"{fs/1e9:g} GS/s")
    ax.grid(True, which="both", alpha=0.3)
axes[0].set_ylabel("energy / sample [pJ]")
axes[-1].legend(fontsize=7, loc="upper left")
fig.suptitle("S0.7-lite envelope: photonic (4 frozen scenarios) vs named digital "
             "baselines (PR-10 frozen 2026-06-10; conventions C1-C8)")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "s0_7_lite_energy_vs_N.png"), dpi=160)

fig2, ax = plt.subplots(figsize=(6.4, 4.4))
for corner, hclass in SCENARIOS:
    key = f"{corner}x{hclass}"
    fx = [f_cross_hz(corner, hclass, n, baselines_pj(corner, n)["Brainwave"][0], 1)
          for n in N_GRID]
    fx = [v / 1e9 if v != float("inf") else float("nan") for v in fx]
    c, ls = SC_STYLE[key]
    ax.plot(N_GRID, fx, ls, color=c, marker="s", label=key)
ax.axhspan(0.1, 2.0, color="tab:purple", alpha=0.12,
           label="registered rate window 0.1-2 GS/s")
ax.set_xscale("log", base=2); ax.set_yscale("log")
ax.set_xticks(N_GRID); ax.set_xticklabels(N_GRID)
ax.set_xlabel("N rings / states")
ax.set_ylabel("crossover rate vs Brainwave [GS/s]")
ax.set_title("Rate above which the photonic side beats Brainwave\n"
             "(absent = conversion alone already exceeds the baseline)")
ax.grid(True, which="both", alpha=0.3); ax.legend(fontsize=8)
fig2.tight_layout()
fig2.savefig(os.path.join(OUT, "s0_7_lite_crossover.png"), dpi=160)

print(f"Wrote JSON + 2 PNGs to {os.path.normpath(OUT)}")
