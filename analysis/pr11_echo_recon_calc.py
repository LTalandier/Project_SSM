# NEW (PR-11 recon, 2026-07-07) — the quantitative rows behind
# docs/s0_4/pr11_echo_submodel_recon.md (RHEL χ³-FWM echo sub-model menu).
# Recon-grade: scale estimates for the mechanism menu; the S0.4c spec
# freezes the committed mechanism + numbers (with sources verified).
"""PR-11 echo-sub-model recon calculations.

Writes results/s0_4c/pr11_recon_calc.json and prints the memo tables:
  1. per-cell state band vs drive band (which band must the conjugator span);
  2. single-pass spiral FWM conversion efficiency eta_c = (gamma P L)^2;
  3. per-cell extraction fraction into the bus, 2*kappa_ext/kappa_net at θ₀;
  4. conjugation-window / off-chip-transit decay e^{-kappa_net * tau};
  5. resonant-conjugator Q_L ceiling from the state-band requirement.
"""

from __future__ import annotations

import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from photonic_ssm.estimators.harness import make_substrate  # noqa: E402

OUT = "results/s0_4c"

# SiN nonlinearity (recon-grade; ⚠verify before the S0.4c freeze):
N2_M2_PER_W = 2.4e-19        # n₂ of Si₃N₄ (Ikeda 2008 / Moss 2013 class)
LAMBDA_M = 1.55e-6
A_EFF_M2 = 1.0e-12           # ~1 µm² effective area
NU_HZ = 193.4e12


def main():
    os.makedirs(OUT, exist_ok=True)
    out = {}

    gamma_nl = 2.0 * math.pi * N2_M2_PER_W / (LAMBDA_M * A_EFF_M2)
    out["gamma_nl_per_W_m"] = gamma_nl
    print(f"[FWM] gamma_nl (n2={N2_M2_PER_W:.1e}, Aeff=1 um^2) = "
          f"{gamma_nl:.2f} /W/m")
    out["spiral_eta_c"] = {}
    print("[FWM] single-pass spiral conversion eta_c = (gamma*Pp*L)^2:")
    for Pp, L in ((0.1, 0.5), (0.3, 0.5), (1.0, 0.5), (0.3, 2.0)):
        eta = (gamma_nl * Pp * L) ** 2
        out["spiral_eta_c"][f"Pp={Pp}W,L={L}m"] = eta
        print(f"    Pp={Pp:4.1f} W, L={L:3.1f} m: eta_c = {eta:.2e} "
              f"({10 * math.log10(eta):+.1f} dB)")

    out["cells"] = {}
    print("[cells] state band / extraction / decay at θ₀ "
          "(drive band = 2 GS/s ≈ 2 GHz in all cells):")
    for label in ("C-1", "C-2", "C-3"):
        sub = make_substrate(label, seed=3)
        ki = float(sub.kappa_i)
        kn = sub.kappa_net().detach()
        kn_mean = float(kn.mean())
        kext = float(sub.kappa_ext.detach().mean())
        state_band_Hz = (2.0 * ki + float(kn.max())) / (2.0 * math.pi)
        eta_ex = 2.0 * kext / kn_mean          # bus fraction of total decay
        row = {
            "N": sub.N,
            "kappa_i_over_2pi_MHz": ki / (2 * math.pi) / 1e6,
            "kappa_net_over_2pi_MHz_mean": kn_mean / (2 * math.pi) / 1e6,
            "tau_net_ns": 1.0 / kn_mean * 1e9,
            "state_band_MHz": state_band_Hz / 1e6,
            "eta_extraction_bus_fraction": eta_ex,
            "QL_ceiling_state_band": NU_HZ / state_band_Hz,
            "transit_amp_survival": {
                f"{t}ns": math.exp(-kn_mean * t * 1e-9)
                for t in (5.0, 10.0, 20.0)},
        }
        out["cells"][label] = row
        print(f"  {label} (N={sub.N}): κᵢ/2π={row['kappa_i_over_2pi_MHz']:.1f} MHz"
              f" · κ_net/2π={row['kappa_net_over_2pi_MHz_mean']:.1f} MHz"
              f" · τ_net={row['tau_net_ns']:.1f} ns"
              f" · state band ≈ {row['state_band_MHz']:.0f} MHz"
              f" · η_ex=2κ_ext/κ_net={eta_ex:.2f}"
              f" · Q_L ceiling (state band) ≈ {row['QL_ceiling_state_band']:.1e}")
        print(f"        transit amplitude survival: "
              + " · ".join(f"{t} ns → {v:.2f}"
                           for t, v in [(5, row['transit_amp_survival']['5.0ns']),
                                        (10, row['transit_amp_survival']['10.0ns']),
                                        (20, row['transit_amp_survival']['20.0ns'])]))

    with open(os.path.join(OUT, "pr11_recon_calc.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote", os.path.join(OUT, "pr11_recon_calc.json"))


if __name__ == "__main__":
    main()
