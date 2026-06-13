# NEW (task S0.3-1, deliverable 5) — the PR-4 v2 cell registry. Extends the
# salvaged SiN platform registry (photonic_ssm/platforms.py) with the frozen
# substrate parameter points. Sets no new physics values: every number traces
# to the 🔒 SIGNED PR-4 v2 block (preregistration.md, §C / §G / §S).
"""PR-4 v2 substrate cell registry.

A *cell* is a registered parameter point of the single shared substrate
model: a base SiN platform (Qᵢ, loss, geometry — from `platforms.py`) plus
the PR-4 v2 cell-level choices — the mode-splitting backscatter rate γ, the
ring-count assignment N, the headline noise figure NF, the gain operating
point, and the cell's role.

Frozen PR-4 v2 cells (preregistration.md §C):

    C-1  P-FND   foundry floor      Qᵢ=2e6   γ/2π=90 MHz   N=8    Gate ii @2GS/s
    C-2  P-AN800 demonstrated MPW   Qᵢ=6.8e6 γ/2π=11.8 MHz N=32   bake-off headline
    C-3  P-UHQ   aspirational       Qᵢ=3e7   γ/2π=11.8 MHz N=128  never gates

NF-A 7.0 dB (n_sp=2.5) is the headline noise value at every cell (rider R1);
NF ∈ {3,5} are sensitivity values only. Gain operating point: every
gain-bearing cell runs at g_rt = 0.9 × intrinsic per-round-trip loss
(⇒ κ_net = 0.1·κᵢ + 2κ_ext); g ∈ {0 passive, 0.5×} are sensitivity rows;
P-CORN is passive-only.

Conventions (inherited from S0.1, restated where load-bearing):
  * κᵢ = ω₀/(2Qᵢ) = π·f0/Qᵢ  (amplitude decay rate, rad/s).
  * γ is reported as the BACKSCATTER RATE γ/2π in MHz (the cell's `gamma_MHz`
    field); the measurable mode splitting is 2γ. So γ_rad_s = 2π·γ_MHz·1e6,
    and the salvaged `gamma_rad_s_from_MHz_linear(2·gamma_MHz)` returns the
    same value (it takes the splitting 2γ/2π). Verified against PR-4 v2's
    2γ/κ_tot table: C-1 2.33 / C-2 1.04 (passive floor), 5.3 / 2.4 (operating
    gain) all reproduce.
  * n_sp = 10^(NF_dB/10) / 2  (NF ≈ 2·n_sp high-gain limit; NF-7 → n_sp=2.5).
"""

from __future__ import annotations

import math
from typing import NamedTuple, Optional

from ..platforms import (
    PlatformConfig,
    PLATFORM_REGISTRY,
    get_platform,
    loss_dB_per_cm_from_qi,
)
from ..dynamics.single_ring import F0_HZ, kappa_from_Q

# Registered PR-4 v2 operating point: gain compensates 90 % of the intrinsic
# per-round-trip loss (the no-lasing ceiling). κ_net = (1-0.9)·κᵢ + 2κ_ext.
GAIN_FACTOR_OPERATING: float = 0.9
# Sensitivity rows (PR-4 v2 §C "gain rows g ∈ {0 (passive floor), 0.5×}").
GAIN_FACTOR_SENSITIVITY: tuple[float, ...] = (0.0, 0.5)
# Registered headline NF (rider R1) and the sensitivity menu.
NF_HEADLINE_DB: float = 7.0
NF_SENSITIVITY_DB: tuple[float, ...] = (3.0, 5.0, 7.0)
# Registered γ sensitivity menu (γ/2π, MHz) — PR-4 v2 §C sensitivity axes.
GAMMA_SENSITIVITY_MHZ: tuple[float, ...] = (0.0, 11.8, 90.0, 160.0)
# θ₀ policy value (the F6 baseline hold): r₀ = κ_ext/κᵢ = 0.3 (PR-4 v2 §K).
R0_THETA0: float = 0.3
# K4 trainable κ_ext bounds, r = κ_ext/κᵢ ∈ [0.1, 3] (PR-4 v2 §K).
R_BOUNDS: tuple[float, float] = (0.1, 3.0)


class SubstrateCell(NamedTuple):
    """A registered PR-4 v2 substrate parameter point.

    Fields
    ------
    label        : registered cell id ("C-1", "C-2", "C-3", or a sensitivity
                   tag like "C-2-derate", "P-CORN").
    name         : the PR-4 cell name ("P-FND", "P-AN800", "P-UHQ", ...).
    platform_name: key into photonic_ssm.platforms.PLATFORM_REGISTRY (or into
                   the local _DERIVED_PLATFORMS below for synthesized cells).
    gamma_MHz    : backscatter rate γ/2π [MHz] (0 ⇒ splitting OFF / floor).
    N            : registered ring-count assignment (per-cell, NOT a sweep —
                   PR-4 v2 §S rider R2: N=8↔C-1, N=32↔C-2, N=128↔C-3 only).
    nf_dB        : headline noise figure [dB] (NF-A 7.0 by default).
    gain_factor  : fraction of intrinsic loss the gain compensates
                   (0.9 operating, 0.0 passive, 0.5 sensitivity).
    passive_only : True ⇒ the cell never carries gain (P-CORN).
    role         : human-readable role ("gate_ii", "headline", "aspirational",
                   "sensitivity").
    """

    label: str
    name: str
    platform_name: str
    gamma_MHz: float
    N: int
    nf_dB: float = NF_HEADLINE_DB
    gain_factor: float = GAIN_FACTOR_OPERATING
    passive_only: bool = False
    role: str = "sensitivity"


# ---------------------------------------------------------------------- #
#  Derived platforms (sensitivity variants not in the salvaged registry)
# ---------------------------------------------------------------------- #
#  C-2 ×2-loss derate (PR-4 v2 §C / P4-F4): the geometry-transfer risk price
#  — double the registered C-2 loss ⇒ Qᵢ ≈ 3.4e6. Synthesized from the AN800
#  base (n_g, geometry kept; Qᵢ halved, loss doubled, kept self-consistent so
#  loss_q_consistency_error ≈ 0). Cost ≈ 0 in simulation; carried as a label.

def _derate_loss(base: PlatformConfig, factor: float, new_name: str
                 ) -> PlatformConfig:
    """Return a copy of `base` with Qᵢ scaled by 1/factor (loss ×factor),
    loss re-derived from the new Qᵢ so the registry self-consistency holds."""
    new_qi = base.Qi / factor
    return base._replace(
        name=new_name,
        Qi=new_qi,
        loss_dB_per_cm=loss_dB_per_cm_from_qi(new_qi, base.n_g),
        q_basis="Qi",
    )


_DERIVED_PLATFORMS: dict[str, PlatformConfig] = {
    "SiN_AN800_derate2x": _derate_loss(
        PLATFORM_REGISTRY["SiN_LIGENTEC_AN800"], 2.0, "SiN_AN800_derate2x"),
}


def platform_of(cell: SubstrateCell) -> PlatformConfig:
    """Resolve the cell's base platform (salvaged registry or derived)."""
    if cell.platform_name in _DERIVED_PLATFORMS:
        return _DERIVED_PLATFORMS[cell.platform_name]
    return get_platform(cell.platform_name)


# ---------------------------------------------------------------------- #
#  Registered cells (frozen PR-4 v2 §C)
# ---------------------------------------------------------------------- #

CELLS: dict[str, SubstrateCell] = {
    # --- Headline / gating cells (deployable grid {8@C-1, 32@C-2}) -------- #
    "C-1": SubstrateCell(
        label="C-1", name="P-FND",
        platform_name="SiN_foundry_conservative",  # Qᵢ=2e6, α=0.172 dB/cm
        gamma_MHz=90.0, N=8, nf_dB=7.0,
        gain_factor=GAIN_FACTOR_OPERATING, role="gate_ii",
    ),
    "C-2": SubstrateCell(
        label="C-2", name="P-AN800",
        platform_name="SiN_LIGENTEC_AN800",  # Qᵢ=6.8e6, α=0.051 dB/cm
        gamma_MHz=11.8, N=32, nf_dB=7.0,
        gain_factor=GAIN_FACTOR_OPERATING, role="headline",
    ),
    "C-3": SubstrateCell(
        label="C-3", name="P-UHQ",
        platform_name="SiN_damascene_UHQ",  # Qᵢ=3e7
        gamma_MHz=11.8, N=128, nf_dB=7.0,
        gain_factor=GAIN_FACTOR_OPERATING, role="aspirational",
    ),
    # --- Sensitivity cells (reported, never headline; PR-4 v2 §C) -------- #
    "P-CORN": SubstrateCell(
        label="P-CORN", name="P-CORN",
        platform_name="SiN_CORNERSTONE_300",  # Qᵢ=2.35e5, passive-only
        gamma_MHz=90.0, N=8, nf_dB=7.0,
        gain_factor=0.0, passive_only=True, role="sensitivity",
    ),
    "C-2-derate": SubstrateCell(
        label="C-2-derate", name="P-AN800-derate2x",
        platform_name="SiN_AN800_derate2x",  # Qᵢ≈3.4e6 (×2 loss, P4-F4)
        gamma_MHz=11.8, N=32, nf_dB=7.0,
        gain_factor=GAIN_FACTOR_OPERATING, role="sensitivity",
    ),
}


def get_cell(label: str) -> SubstrateCell:
    """Lookup a registered cell by label; KeyError on miss with the menu."""
    if label not in CELLS:
        raise KeyError(
            f"Unknown substrate cell '{label}'. Known: {sorted(CELLS)}")
    return CELLS[label]


# ---------------------------------------------------------------------- #
#  Derived quantities
# ---------------------------------------------------------------------- #

def kappa_i_rad_s(cell: SubstrateCell) -> float:
    """Intrinsic amplitude decay rate κᵢ = ω₀/(2Qᵢ) = π·f0/Qᵢ [rad/s]."""
    return kappa_from_Q(platform_of(cell).Qi)


def gamma_rad_s(cell: SubstrateCell) -> float:
    """Backscatter coupling rate γ [rad/s] from the cell's γ/2π [MHz]. The
    measurable mode splitting is 2γ; γ=0 ⇒ the single-pole model (no
    doublet). Equivalent to the salvaged
    `gamma_rad_s_from_MHz_linear(2*gamma_MHz)`."""
    return 2.0 * math.pi * cell.gamma_MHz * 1e6


def n_sp_from_nf_dB(nf_dB: float) -> float:
    """Spontaneous-emission factor n_sp = 10^(NF/10)/2 (NF ≈ 2·n_sp in the
    high-gain limit). NF-7 → 2.5; NF-5 → 1.58; NF-3 → 0.998 (≈ quantum
    floor, aspirational)."""
    return (10.0 ** (nf_dB / 10.0)) / 2.0


def n_sp(cell: SubstrateCell) -> float:
    """The cell's headline n_sp (from its NF)."""
    return n_sp_from_nf_dB(cell.nf_dB)


def n_ss_compensation(nf_dB: float = NF_HEADLINE_DB,
                      gain_factor: float = GAIN_FACTOR_OPERATING) -> float:
    """The registered ASE characterization number (PR-4 v2 §G / input sheet
    §1.3): the steady-state intracavity ASE photon number at `gain_factor`
    compensation of the INTRINSIC loss, with κ_ext excluded from the net —
    `n_ss = n_inj/rt ÷ (2κ_net·dt_rt)` with both ∝ κᵢ, so n_ss is
    CORNER-INDEPENDENT:

        n_ss = n_sp · gain_factor / (1 - gain_factor).

    At the operating point (gain_factor=0.9): n_ss = 9·n_sp ≈ 23 at NF-7,
    ≈ 9 at NF-3. (This is the substrate-characterization figure of test (f);
    the OPERATING κ_net that the rollout uses additionally carries 2κ_ext.)
    """
    if gain_factor >= 1.0:
        raise ValueError("gain_factor must be < 1 (no-lasing).")
    return n_sp_from_nf_dB(nf_dB) * gain_factor / (1.0 - gain_factor)
