# NEW (task S0.3-1, deliverable 2) — M1 static saturated gain operating point.
# Implements the frozen PR-4 v2 §G choice. Sets no values: P_sat (−15 dBm),
# A_eff (1.2 µm²), the Er-gain anchor span (1.0–1.9 dB/cm), and the operating
# point (g_rt = 0.9× intrinsic) are all frozen PR-4 v2 §G entries; the numeric
# g₀/reachability are computed mechanically by calibration.py.
"""M1 static saturated gain operating point (PR-4 v2 §G).

The Er:Si₃N₄ gain stage is **quasi-static** at all registered clocks (PL
lifetime τ = 3.4 ms ≫ symbol period; E_sym/E_sat ≈ 5e-6–9e-5), so within an
episode the gain is a single saturated operating point, not a dynamical
state (the M2 rate-equation reference confirms the ≤3 % relaxation bound).

    g(P̄) = g₀ / (1 + P̄/P_sat),   fixed within the rollout, differentiable.

**Reference plane (P4-F2): P̄ and P_sat both live at the intracavity plane —
the field the gain medium sees.** P_sat is the flagship's measured INPUT
saturation power −15 dBm [EV] mapped through the registered geometry by
I_sat = P_sat,wg/A_eff (A_eff = 1.2 µm²), applied to the ring's circulating
intensity I_circ = P_circ/A_eff, P_circ = Σⱼ|aⱼ|²·ħω₀/τ_rt. With one A_eff
the intensity criterion reduces to P_circ vs P_sat,wg.

**Operating point (registered):** every gain-bearing cell runs at g_rt =
0.9 × intrinsic per-round-trip loss (the no-lasing ceiling) ⇒ κ_net =
0.1·κᵢ + 2κ_ext. g₀ is set per cell by the saturated solve so that
g(P̄ at the registered drive P̄₀ = 1 mW, θ₀) = 0.9·κᵢ. Sensitivity rows
g ∈ {0 passive, 0.5×}; P-CORN passive-only.

**Reachability (P4-F2, reported by calibration.py, not papered over):** the
small-signal gain headroom = Er-anchor span (1.0–1.9 dB/cm [EV]) ÷ the cell
operating-point gain (0.9·α). At the registered drive the gain must supply a
saturation-depth multiplier of ≈ P̄₀/P_sat ≈ ×32 (bus-referenced;
cell-independent) — so C-1 (headroom ×6.5–12) is **material-aspirational**,
C-2 (headroom ×22–41) straddles. The intracavity build-up (×260 at C-2/θ₀)
is the more demanding alternative plane.

House constraint 3a/3b: g(P̄) is differentiable in the episode drive
statistics and in κ_ext (through the build-up); no detach. The substrate
holds g fixed across the T steps within an episode (M1 — one evaluation per
rollout) but lets it RESPOND to the trained κ_ext between episodes: the
registered default is **`saturating`** (g(P̄(κ_ext)), faithful to §G/§N-E6,
the bake-off mode for all four estimators); **`fixed`** (g = factor·κᵢ
constant) is a diagnostic/sensitivity floor and the plane the frozen
operating-point numbers (B1 pole region, E₀) are quoted at. Caveat
(S0.3-1b): under `saturating`, reducing κ_ext below θ₀ lowers the build-up,
de-saturates g upward, and drives κ_net→0 (super-threshold) for r ≲ 0.13 at
the cell-independent operating point — the effective trainable κ_ext floor in
saturating mode is above the K4 r=0.1 bound; flagged for the bake-off clamp
policy (PR-6).
"""

from __future__ import annotations

import math
from typing import NamedTuple

import torch

# Photon energy at 1550 nm [J] — matches photonic_ssm.gain (h·c/λ).
H_NU_J: float = 1.282e-19
# Flagship measured input saturation power −15 dBm [EV, R§4b].
P_SAT_DBM: float = -15.0
P_SAT_WG_W: float = 1e-3 * (10.0 ** (P_SAT_DBM / 10.0))  # 31.6 µW
# Effective mode area [m²] [EV, R§4b SI §10].
A_EFF_M2: float = 1.2e-12
# Saturation intensity I_sat = P_sat,wg / A_eff [W/m²].
I_SAT_W_PER_M2: float = P_SAT_WG_W / A_EFF_M2
# Demonstrated Er:Si₃N₄ small-signal gain coefficient span [dB/cm] [EV, R§4f].
ER_ANCHOR_DB_PER_CM: tuple[float, float] = (1.0, 1.9)
# Registered drive (O2): per-sequence mean bus power [W] (PR-4 v2 §N).
P_BAR0_W: float = 1e-3


def buildup_factor(kappa_ext: float, kappa_i: float, FSR_Hz: float,
                   g_amp: float = 0.0) -> float:
    """On-resonance single-driven-ring intracavity power build-up
    P_circ/P_bus = 2·κ_ext·FSR / κ_tot², κ_tot = κᵢ + 2κ_ext − g_amp (the CW
    steady state |a|² = 2κ_ext(P/ħω)/κ_tot² times ħω·FSR over P). Evaluated
    at the passive floor (g=0) for the saturation estimate, matching the
    frozen ×260 at C-2/θ₀."""
    kappa_tot = kappa_i + 2.0 * kappa_ext - g_amp
    return 2.0 * kappa_ext * FSR_Hz / (kappa_tot ** 2)


def circulating_power_W(kappa_ext, kappa_i: float, FSR_Hz: float,
                        P_bus_W=P_BAR0_W):
    """Episode-mean intracavity circulating power P_circ [W] at bus power
    P_bus_W. Differentiable in κ_ext (torch tensor) for the M1 operating
    point's drive-statistics dependence; accepts floats for the calibration
    arithmetic. Uses the passive build-up (non-circular in g)."""
    if isinstance(kappa_ext, torch.Tensor):
        kappa_tot = kappa_i + 2.0 * kappa_ext
        buildup = 2.0 * kappa_ext * FSR_Hz / (kappa_tot ** 2)
    else:
        buildup = buildup_factor(kappa_ext, kappa_i, FSR_Hz)
    return buildup * P_bus_W


def gain_rate(g0, P_bar_W, P_sat_W: float = P_SAT_WG_W):
    """Saturated gain rate g(P̄) = g₀/(1 + P̄/P_sat) [rad/s]. Differentiable
    in g0 and P_bar_W (torch tensors) — the M1 form (no detach)."""
    return g0 / (1.0 + P_bar_W / P_sat_W)


def g0_for_operating_point(kappa_i: float, kappa_ext: float,
                           factor: float = 0.9,
                           P_bar_ref_W: float = P_BAR0_W,
                           FSR_Hz: float = 100e9,
                           P_sat_W: float = P_SAT_WG_W) -> float:
    """Solve g₀ such that g(P̄ at the registered drive) = factor·κᵢ.
    g₀ = factor·κᵢ·(1 + P̄_ref/P_sat) with P̄_ref the passive-build-up
    intracavity circulating power at the registered drive."""
    P_bar_ref = circulating_power_W(kappa_ext, kappa_i, FSR_Hz, P_bar_ref_W)
    return factor * kappa_i * (1.0 + P_bar_ref / P_sat_W)


def operating_gain_rate(kappa_i: float, factor: float = 0.9) -> float:
    """The registered FIXED operating-point gain rate g = factor·κᵢ [rad/s]
    (0.9·κᵢ headline ⇒ κ_net = 0.1κᵢ + 2κ_ext; 0 passive; 0.5·κᵢ sensitivity).
    This is what the substrate rollout uses by default (M1: fixed within the
    rollout, at the registered drive)."""
    return factor * kappa_i


class GainModel(NamedTuple):
    """A per-cell M1 operating point. `factor` is the registered fraction of
    intrinsic loss compensated (0.9 operating / 0 passive / 0.5 sensitivity).
    `g0` and `P_sat_W` carry the saturating form for the reachability solve /
    SPSA realism; `rate_fixed` is the registered operating value used in the
    rollout."""

    kappa_i: float
    kappa_ext0: float
    factor: float
    g0: float
    P_sat_W: float
    FSR_Hz: float

    @property
    def rate_fixed(self) -> float:
        """g = factor·κᵢ — the fixed operating-point rate used in the rollout."""
        return self.factor * self.kappa_i

    def rate_saturating(self, kappa_ext, P_bus_W=P_BAR0_W):
        """g(P̄(κ_ext, drive)) — the saturating form, differentiable in κ_ext.
        Equals rate_fixed at the calibration point (κ_ext0, registered drive)."""
        P_bar = circulating_power_W(kappa_ext, self.kappa_i, self.FSR_Hz, P_bus_W)
        return gain_rate(self.g0, P_bar, self.P_sat_W)


def build_gain_model(kappa_i: float, kappa_ext0: float, factor: float = 0.9,
                     FSR_Hz: float = 100e9) -> GainModel:
    """Assemble the per-cell GainModel at the registered operating point."""
    g0 = (0.0 if factor == 0.0
          else g0_for_operating_point(kappa_i, kappa_ext0, factor,
                                      FSR_Hz=FSR_Hz))
    return GainModel(kappa_i=kappa_i, kappa_ext0=kappa_ext0, factor=factor,
                     g0=g0, P_sat_W=P_SAT_WG_W, FSR_Hz=FSR_Hz)


# ---------------------------------------------------------------------- #
#  Gain-coefficient <-> rate, for the reachability report (dB/cm plane)
# ---------------------------------------------------------------------- #

def rate_to_gain_dB_per_cm(g_rate: float, n_g: float,
                           lambda_m: float = 1550e-9) -> float:
    """Convert an amplitude gain rate g [rad/s] to a material gain
    coefficient [dB/cm]. A rate g ⇔ a 'gain Q' Q_g = ω₀/(2g); the propagation
    relation (same kernel as the loss↔Q registry) gives the dB/cm. Amplitude
    growth e^{g·τ_rt} per round trip ⇒ power gain coefficient
    γ = 2·g·n_g/c [1/m]."""
    c = 2.99792458e8
    gamma_per_m = 2.0 * g_rate * n_g / c
    return gamma_per_m * (10.0 * math.log10(math.e)) / 100.0
