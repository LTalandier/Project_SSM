"""S0.3-0 substrate-recon arithmetic (menu-sizing only — NO substrate code).

Computes, for the four registered SiN platform corners (photonic_ssm.platforms),
the numbers the PR-4 input sheet needs, reusing the S0.1 kernel conventions
(photonic_ssm.dynamics.pole_region: amplitude rates, kappa_i = omega0/(2 Qi),
symmetric add-drop kappa_tot = kappa_i + 2*kappa_ext, HWHM splitting criterion
2*gamma >= kappa_tot with the FWHM band = x2):

  (a) self-consistent (alpha, Q_i) pair identity + passive memory at the
      registered clocks (PR-10 grid 0.1/1/2 GS/s);
  (b) EV-F3 linewidth packing: informationally distinct poles/GHz (1-FWHM
      separation) at the kappa_ext ladder, + max in-band N at 1/2 GS/s vs the
      PR-10 N grid {8,32,128};
  (c) B2 splitting ratio 2*gamma/kappa_tot AT OPERATING kappa_ext (the D-08-3
      blessed constraint) for the three B2 process-class gamma values;
  (d) kappa_ext policy ladder: memory (rt + samples at each clock) + drop
      efficiency — sized against the frozen PR-2 cells (T-A 7-tap @ 2 GS/s,
      PR-13 k-grid @ 1 GS/s + k=100 @ 2 GS/s);
  (e) noise-cell sizing: per-round-trip loss, compensating gain at 0/50/90 %
      net-gain conventions (S0.1 plot convention), ASE photons/round-trip
      n_sp*(G_rt-1) with n_sp = 10^(NF/10)/2 (high-G convention; the per-pass
      low-gain caveat is prose, not arithmetic).

Output: markdown tables to stdout + results/s0_3/s0_3_0_recon_arithmetic.json.
Round-trip dt = 10 ps (FSR 100 GHz registry convention, mapping_result.md §4).
"""

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from photonic_ssm.dynamics.pole_region import (
    F0_HZ,
    kappa_from_Q,
    memory_length_samples,
    splitting_linewidth_ratio,
)
from photonic_ssm.platforms import PLATFORM_REGISTRY

DT_RT = 10e-12          # round trip @ FSR 100 GHz (registry convention)
CLOCKS_GSPS = [0.1, 1.0, 2.0]
KEXT_RATIOS = [0.0, 0.1, 0.3, 1.0, 3.0, 10.0]   # r = kappa_ext/kappa_i (per coupler, symmetric add-drop)
GAMMA_CLASSES_MHZ = {                            # B2 table, gamma/2pi (one-direction rate)
    "damascene-clean": 11.8,
    "subtractive-low": 90.0,
    "subtractive-high": 160.0,
}
NF_CANDIDATES_DB = [3.0, 4.5, 6.0, 7.0]
NET_GAIN_FRACTIONS = [0.0, 0.5, 0.9]             # S0.1 plot convention: net gain as fraction of loss
N_GRID = [8, 32, 128]                            # PR-10 operating-scale grid

SIN_CORNERS = [
    "SiN_CORNERSTONE_300",
    "SiN_foundry_conservative",
    "SiN_LIGENTEC_AN800",
    "SiN_damascene_UHQ",
]


def corner_block(name):
    p = PLATFORM_REGISTRY[name]
    ki = kappa_from_Q(p.Qi)                      # amplitude rate, rad/s
    out = {
        "name": name,
        "q_basis": p.q_basis,
        "Qi": p.Qi,
        "loss_dB_per_cm": p.loss_dB_per_cm,
        "kappa_i_over_2pi_MHz": ki / (2 * math.pi) / 1e6,
        "intrinsic_FWHM_MHz": F0_HZ / p.Qi / 1e6,   # FWHM(Hz) = f0/Qi = 2*kappa_i/2pi... checked below
        "passive_memory_ns": 1.0 / ki * 1e9,
        "passive_memory_rt": 1.0 / ki / DT_RT,
        "passive_memory_samples": {
            f"{c:g} GS/s": (1.0 / ki) * c * 1e9 for c in CLOCKS_GSPS
        },
        "ladder": [],
        "noise": [],
    }
    # consistency: FWHM(rad/s) = 2*kappa_tot; intrinsic (r=0): 2*kappa_i ->
    # FWHM(Hz) = kappa_i/pi; equals f0/Qi since kappa_i = pi*f0/Qi.
    assert abs(out["intrinsic_FWHM_MHz"] - ki / math.pi / 1e6) < 1e-6 * out["intrinsic_FWHM_MHz"]

    for r in KEXT_RATIOS:
        ktot = ki * (1.0 + 2.0 * r)              # symmetric add-drop
        fwhm_hz = ktot / math.pi
        poles_per_GHz = 1e9 / fwhm_hz            # 1-FWHM separation criterion
        drop_eff = 0.0 if r == 0 else (2.0 * (r * ki) / ktot) ** 2
        row = {
            "r": r,
            "kappa_tot_over_2pi_MHz": ktot / (2 * math.pi) / 1e6,
            "loaded_FWHM_MHz": fwhm_hz / 1e6,
            "poles_per_GHz": poles_per_GHz,
            "max_inband_N": {f"{c:g} GS/s": poles_per_GHz * c for c in [1.0, 2.0]},
            "memory_rt": 1.0 / ktot / DT_RT,
            "memory_samples": {
                f"{c:g} GS/s": memory_length_samples(ktot, 1.0 / (c * 1e9))
                for c in CLOCKS_GSPS
            },
            "drop_efficiency": drop_eff,
            "splitting_2g_over_ktot_HWHM": {
                cls: splitting_linewidth_ratio(
                    g_mhz * 1e6 * 2 * math.pi, p.Qi, kappa_ext=2.0 * r * ki
                )
                for cls, g_mhz in GAMMA_CLASSES_MHZ.items()
            },
        }
        out["ladder"].append(row)

    # (e) noise-cell sizing: per-rt amplitude loss kappa_i*dt; power loss/rt
    loss_amp_per_rt = ki * DT_RT
    loss_power_frac_per_rt = 1.0 - math.exp(-2.0 * loss_amp_per_rt)
    for frac in NET_GAIN_FRACTIONS:
        g_amp = frac * ki                        # net gain as fraction of intrinsic loss
        G_rt_power = math.exp(2.0 * g_amp * DT_RT)
        nf_rows = {}
        for nf_db in NF_CANDIDATES_DB:
            n_sp = (10 ** (nf_db / 10.0)) / 2.0  # NF ~= 2 n_sp (high-G convention)
            nf_rows[f"{nf_db:g} dB"] = n_sp * (G_rt_power - 1.0)
        out["noise"].append({
            "net_gain_fraction_of_loss": frac,
            "G_rt_power": G_rt_power,
            "G_rt_dB": 10 * math.log10(G_rt_power),
            "ase_photons_per_rt_per_mode": nf_rows,
        })
    out["loss_power_frac_per_rt"] = loss_power_frac_per_rt
    out["loss_amp_per_rt"] = loss_amp_per_rt
    return out


def main():
    blocks = [corner_block(n) for n in SIN_CORNERS]

    os.makedirs("results/s0_3", exist_ok=True)
    with open("results/s0_3/s0_3_0_recon_arithmetic.json", "w") as f:
        json.dump({"dt_rt_s": DT_RT, "f0_Hz": F0_HZ, "corners": blocks}, f, indent=1)

    for b in blocks:
        print(f"\n## {b['name']}  (q_basis={b['q_basis']}; Qi={b['Qi']:.4g}; "
              f"alpha={b['loss_dB_per_cm']:.4g} dB/cm)")
        print(f"kappa_i/2pi = {b['kappa_i_over_2pi_MHz']:.3f} MHz; intrinsic FWHM = "
              f"{b['intrinsic_FWHM_MHz']:.3f} MHz; passive memory = "
              f"{b['passive_memory_ns']:.3f} ns = {b['passive_memory_rt']:.1f} rt; samples "
              + ", ".join(f"{k}: {v:.3g}" for k, v in b["passive_memory_samples"].items()))
        print(f"per-rt power loss = {100*b['loss_power_frac_per_rt']:.4f} %")
        print("\n| r=kext/ki | ktot/2pi MHz | FWHM MHz | poles/GHz | maxN@1G | maxN@2G | "
              "mem rt | mem smp @0.1/1/2 GS/s | drop eff | 2g/ktot clean | sub-low | sub-high |")
        print("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for row in b["ladder"]:
            ms = row["memory_samples"]
            sp = row["splitting_2g_over_ktot_HWHM"]
            print(f"| {row['r']:g} | {row['kappa_tot_over_2pi_MHz']:.2f} | "
                  f"{row['loaded_FWHM_MHz']:.2f} | {row['poles_per_GHz']:.1f} | "
                  f"{row['max_inband_N']['1 GS/s']:.0f} | {row['max_inband_N']['2 GS/s']:.0f} | "
                  f"{row['memory_rt']:.0f} | "
                  f"{ms['0.1 GS/s']:.2f} / {ms['1 GS/s']:.2f} / {ms['2 GS/s']:.2f} | "
                  f"{row['drop_efficiency']:.3f} | "
                  f"{sp['damascene-clean']:.2f} | {sp['subtractive-low']:.2f} | "
                  f"{sp['subtractive-high']:.2f} |")
        print("\nASE photons / round trip / mode  (n_sp*(G_rt-1), NF columns):")
        print("| net gain (frac of loss) | G_rt dB | " +
              " | ".join(f"NF {nf:g} dB" for nf in NF_CANDIDATES_DB) + " |")
        print("|---|---|" + "---|" * len(NF_CANDIDATES_DB))
        for nr in b["noise"]:
            cells = " | ".join(f"{v:.3e}" for v in nr["ase_photons_per_rt_per_mode"].values())
            print(f"| {nr['net_gain_fraction_of_loss']:g} | {nr['G_rt_dB']:.4f} | {cells} |")


if __name__ == "__main__":
    main()
