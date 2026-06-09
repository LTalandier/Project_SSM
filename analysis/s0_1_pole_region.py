#!/usr/bin/env python3
# NEW (task S0.1) — analysis/plotting driver. Lives OUTSIDE the
# photonic_ssm package on purpose: it imports matplotlib + numpy, which
# the package itself must not (the torch-only runtime invariant, enforced
# by tests/test_no_equalization_coupling.py). All physics comes from the
# tested photonic_ssm.dynamics kernels — this script only sweeps + renders.
"""Render the S0.1 realizable-pole-region deliverables:

  (deliverable 3) loss/gain -> |lambda| (memory) vs Q across the registry
                  Q-span (foundry 2e6 -> class-leading 3e7);
  (B3)            the kappa_ext memory-vs-readout-SNR trade;
  (B2)            the backscatter / mode-splitting crossover vs Q.

Writes figures (PNG) and a machine-readable data table (JSON) to
results/s0_1/. Run: python3 analysis/s0_1_pole_region.py
"""

from __future__ import annotations

import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch

from photonic_ssm.dynamics import (
    kappa_from_Q, loss_limited_memory_time_s, photon_lifetime_s,
    discrete_pole_magnitude, memory_length_samples, net_kappa_tot,
    kappa_ext_trade_sweep, gamma_rad_s_from_MHz_linear,
    splitting_linewidth_ratio, crossover_Q, F0_HZ,
)
from photonic_ssm.platforms import PLATFORM_REGISTRY, get_platform

OUT = os.path.join(os.path.dirname(__file__), "..", "results", "s0_1")
os.makedirs(OUT, exist_ok=True)
FSR_HZ = 100e9
DT = 1.0 / FSR_HZ                       # step = round-trip time (10 ps)

# Registered SiN corners (Qi) spanning the roadmap Q-range, from the
# F13.1-reconciled registry. The 2e6 foundry end is the conservative
# corner (S0.1.1/F7 renamed it off the AN800 product name); the demonstrated
# AN800 (Qi=6.8e6) sits between this and the damascene UHQ end.
SIN = {n: get_platform(n).Qi for n in
       ("SiN_CORNERSTONE_300", "SiN_foundry_conservative", "SiN_damascene_UHQ")}

# Literature backscatter scenarios (docs/s0_1/B2_backscatter_bound.md);
# value = reported splitting 2*gamma/2pi in MHz.
BACKSCATTER = {
    "damascene-clean (Nat.Commun.12,235)": 23.6,
    "subtractive-low-roughness (arXiv:2511.02198)": 180.0,
    "subtractive-high-roughness (arXiv:2511.02198)": 320.0,
}


def pole_region_panel():
    """Deliverable 3: memory (samples) and |lambda| vs Qi, passive and
    gain-compensated, across the registry Q span."""
    Qi = torch.logspace(math.log10(1.5e5), math.log10(4e7), 200)
    data = {"Qi": Qi.tolist(), "gain_fraction": {}, "platforms": {}}
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    for frac in (0.0, 0.5, 0.9):                 # net gain = frac * kappa_i
        mem, mag = [], []
        for q in Qi.tolist():
            ki = kappa_from_Q(q)
            ktot = net_kappa_tot(ki, 0.0, frac * ki)
            mem.append(memory_length_samples(ktot, DT))
            mag.append(discrete_pole_magnitude(ktot, DT))
        ax1.loglog(Qi, mem, label=f"net gain = {frac:.0%} of loss")
        ax2.semilogx(Qi, mag, label=f"net gain = {frac:.0%} of loss")
        data["gain_fraction"][f"{frac}"] = {"memory_samples": mem,
                                            "pole_magnitude": mag}
    for name, q in SIN.items():
        ax1.axvline(q, color="k", ls=":", lw=0.8)
        ax1.text(q, ax1.get_ylim()[0] * 1.5, name.replace("SiN_", ""),
                 rotation=90, fontsize=7, va="bottom")
        data["platforms"][name] = {
            "Qi": q,
            "photon_lifetime_ns": photon_lifetime_s(q) * 1e9,
            "passive_memory_time_ns": loss_limited_memory_time_s(q) * 1e9,
            "passive_memory_samples": memory_length_samples(kappa_from_Q(q), DT),
            "passive_pole_magnitude": discrete_pole_magnitude(kappa_from_Q(q), DT),
        }
    ax1.set_xlabel("intrinsic $Q_i$"); ax1.set_ylabel("memory length (round trips)")
    ax1.set_title("Loss/gain-limited memory (deliverable 3)"); ax1.legend(fontsize=8)
    ax1.grid(True, which="both", alpha=0.3)
    ax2.set_xlabel("intrinsic $Q_i$"); ax2.set_ylabel(r"$|\lambda| = e^{-\kappa_{tot}\,\Delta t}$")
    ax2.set_title("Discrete pole magnitude"); ax2.legend(fontsize=8)
    ax2.grid(True, which="both", alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "pole_region_memory.png"), dpi=130)
    plt.close(fig)
    return data


def kappa_ext_panel():
    """B3: memory-vs-readout-SNR trade as kappa_ext sweeps, at the foundry
    and class-leading corners."""
    ratios = torch.logspace(-2, 2, 80)
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    data = {"ratio": ratios.tolist(), "by_Qi": {}}
    for q, style in ((2e6, "-"), (3e7, "--")):
        sw = kappa_ext_trade_sweep(q, ratios, DT)
        ax.plot(sw["memory_samples"], sw["drop_efficiency"], style,
                label=f"$Q_i$={q:.0e}")
        data["by_Qi"][f"{q:.0e}"] = {
            "memory_samples": sw["memory_samples"].tolist(),
            "drop_efficiency": sw["drop_efficiency"].tolist(),
            "residue_norm": sw["residue_norm"].tolist(),
        }
    ax.set_xscale("log")
    ax.set_xlabel("memory length (round trips)  ← deep undercoupling")
    ax.set_ylabel("on-resonance drop efficiency (detector-SNR proxy)")
    ax.set_title(r"Memory vs readout-SNR trade ($\kappa_{ext}$ policy, B3 / PR-4)")
    ax.legend(); ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "kappa_ext_tradeoff.png"), dpi=130)
    plt.close(fig)
    return data


def backscatter_panel():
    """B2: 2*gamma/kappa_i vs Qi for the cited fabrication scenarios; the
    crossover (=1) is where 'one ring = one complex pole' fails."""
    Qi = torch.logspace(5, 8, 200)
    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    data = {"Qi": Qi.tolist(), "scenarios": {}}
    for label, split_MHz in BACKSCATTER.items():
        g = gamma_rad_s_from_MHz_linear(split_MHz)
        ratio = [splitting_linewidth_ratio(g, q) for q in Qi.tolist()]
        ax.loglog(Qi, ratio, label=f"{label.split(' (')[0]} "
                  fr"($\gamma/2\pi$={g/2/math.pi/1e6:.0f} MHz)")
        data["scenarios"][label] = {
            "gamma_over_2pi_MHz": g / 2 / math.pi / 1e6,
            "split_2gamma_over_2pi_MHz": split_MHz,
            "crossover_Q": crossover_Q(g),
            "ratio_at_2e6": splitting_linewidth_ratio(g, 2e6),
            "ratio_at_3e7": splitting_linewidth_ratio(g, 3e7),
        }
    ax.axhline(1.0, color="k", lw=1.0)
    ax.text(1.2e5, 1.15, "doublet resolved → NOT one pole", fontsize=8)
    for name, q in SIN.items():
        ax.axvline(q, color="gray", ls=":", lw=0.8)
        ax.text(q, ax.get_ylim()[1] * 0.5, name.replace("SiN_", ""),
                rotation=90, fontsize=7, va="top")
    ax.set_xlabel("intrinsic $Q_i$")
    ax.set_ylabel(r"$2\gamma / \kappa_{tot}$  (splitting / linewidth)")
    ax.set_title("Backscatter mode-splitting crossover (B2 / F19)")
    ax.legend(fontsize=7.5, loc="lower right"); ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "backscatter_crossover.png"), dpi=130)
    plt.close(fig)
    return data


def main():
    out = {
        "meta": {"FSR_Hz": FSR_HZ, "dt_s": DT, "f0_Hz": F0_HZ,
                 "step_is_round_trip_time": True},
        "pole_region": pole_region_panel(),
        "kappa_ext_trade": kappa_ext_panel(),
        "backscatter": backscatter_panel(),
    }
    path = os.path.join(OUT, "s0_1_pole_region_data.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    # console summary
    print("Pole-region memory (passive, dt=round-trip):")
    for name, d in out["pole_region"]["platforms"].items():
        print(f"  {name:22s} Qi={d['Qi']:.2e}  tau_ph={d['photon_lifetime_ns']:6.2f} ns  "
              f"mem={d['passive_memory_samples']:7.1f} rt  |lambda|={d['passive_pole_magnitude']:.5f}")
    print("Backscatter crossover Q (2*gamma = kappa_i):")
    for label, d in out["backscatter"]["scenarios"].items():
        verdict = ("splits BELOW foundry 2e6" if d["crossover_Q"] < 2e6
                   else "single-pole at 2e6, splits by 3e7"
                   if d["crossover_Q"] < 3e7 else "single-pole across range")
        print(f"  {label.split(' (')[0]:42s} Q_cross={d['crossover_Q']:.2e}  [{verdict}]")
    print(f"\nFigures + data -> {os.path.relpath(OUT)}")


if __name__ == "__main__":
    main()
