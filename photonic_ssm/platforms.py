# salvaged from pnn-multilayer @ e2eec80 : channels/mrr_platforms.py
# Adaptations for Project_SSM (task S0.0, deliverable 2):
#   - module docstring re-pointed at the Stage-0 role (S0.1 mapping /
#     S0.3 substrate constants);
#   - ADDED two SiN entries: "SiN_CORNERSTONE_300" (open-MPW foundry,
#     proposal §8) and "SiN_damascene_UHQ" (class-leading ultra-high-Q,
#     Liu et al. 2021). The operating-Q choice (foundry 2e6 vs
#     class-leading 3e7) is deliberately NOT made here — parked decision
#     D-2026-06-08-1, due at S0.2/S0.3 pre-registration. The registry
#     carries the whole range.
# Everything else (schema, derived-FSR consistency check, original four
# entries) is lifted unchanged.
"""Ring-platform constants registry for the photonic-SSM Stage-0 models.

Defines the `PlatformConfig` schema and `PLATFORM_REGISTRY`. Each
platform records foundry-/literature-grade values for loss, intrinsic Q,
geometry, group index, thermo-optic drift, and free-carrier
cross-section. Consumers: the S0.1 oscillator<->ring mapping (pole decay
rates from loss/Q), the S0.3 dissipative substrate (loss/drift knobs),
and the S0.7 systems envelope.

Schema:
    PlatformConfig(
        name             : str,
        loss_dB_per_cm   : float,    # waveguide propagation loss
        Qi               : float,    # intrinsic quality factor
        radius_um        : float,    # ring physical radius
        FSR_GHz          : float,    # nominal free-spectral range
        n_g              : float,    # group index
        drift_pm_per_K   : float,    # nominal wavelength drift coefficient
        dn_dT_per_K      : float,    # thermo-optic coefficient (1/K)
        sigma_FC_m3      : float,    # free-carrier dispersion cross-section
                                     # (signed; negative = blue-shift); 0 for
                                     # platforms without measurable FCD
    )

Redundancy note: `radius_um`, `FSR_GHz`, `n_g` are over-specified.
`derived_FSR_GHz(p)` recomputes FSR from radius + n_g and the registry
test asserts |derived - tabulated| < 0.01 GHz.

`Qi` and `loss_dB_per_cm` are tabulated independently (published values,
not derived from each other); `qi_from_loss()` provides the textbook
relation Qi = 2*pi*n_g / (lambda*alpha) for cross-checks and for entries
with no published ring Q.
"""

from __future__ import annotations

import math
from typing import Mapping, NamedTuple


# Speed of light in vacuum (m/s); used for FSR consistency check.
_C_M_PER_S = 2.99792458e8

# Reference wavelength for Qi<->loss conversion (C-band).
_LAMBDA_REF_M = 1550e-9


class PlatformConfig(NamedTuple):
    name: str
    loss_dB_per_cm: float
    Qi: float
    radius_um: float
    FSR_GHz: float
    n_g: float
    drift_pm_per_K: float
    dn_dT_per_K: float
    sigma_FC_m3: float


def derived_FSR_GHz(platform: PlatformConfig) -> float:
    """FSR = c / (n_g * L_round_trip), with L_round_trip = 2*pi*R.

    Returns the FSR in GHz computed from radius_um and n_g, independent
    of the tabulated FSR_GHz field. Used by the consistency test.
    """
    L_m = 2.0 * math.pi * (platform.radius_um * 1e-6)
    fsr_hz = _C_M_PER_S / (platform.n_g * L_m)
    return fsr_hz / 1e9


def qi_from_loss(loss_dB_per_cm: float, n_g: float,
                 lambda_m: float = _LAMBDA_REF_M) -> float:
    """Intrinsic Q implied by propagation loss: Qi = 2*pi*n_g / (lambda*alpha)
    with alpha [1/m] = loss_dB_per_m / (10*log10(e)).

    Cross-check utility — registry entries tabulate *published* Qi where
    one exists; this function backs the entries that derive Qi from loss
    (flagged per entry) and the S0.1 pole-region bound.
    """
    alpha_per_m = (loss_dB_per_cm * 100.0) / (10.0 * math.log10(math.e))
    return 2.0 * math.pi * n_g / (lambda_m * alpha_per_m)


def _radius_um_for_FSR(FSR_GHz: float, n_g: float) -> float:
    """Registry convention: radius computed from c/(n_g * 2*pi * FSR) so
    the derived-FSR consistency test passes by construction."""
    return _C_M_PER_S / (n_g * 2.0 * math.pi * FSR_GHz * 1e9) * 1e6


# ---------------------------------------------------------------------- #
#  Registry
# ---------------------------------------------------------------------- #

PLATFORM_REGISTRY: Mapping[str, PlatformConfig] = {
    # Radii are computed from c / (n_g * 2*pi * FSR_Hz) so that derived FSR
    # matches the tabulated value within 0.01 GHz (registry sanity test).
    "SiN_LIGENTEC_AN800": PlatformConfig(
        name="SiN_LIGENTEC_AN800",
        loss_dB_per_cm=0.03,
        Qi=2e6,
        radius_um=244.6843671,  # FSR = 100 GHz at n_g=1.95
        FSR_GHz=100.0,
        n_g=1.95,
        drift_pm_per_K=14.0,    # midpoint of 10-18 pm/K range
        dn_dT_per_K=2.45e-5,
        sigma_FC_m3=0.0,        # SiN has no measurable FCD at 1550 nm
    ),
    # --- NEW (S0.0): CORNERSTONE open-MPW SiN (proposal §8 foundry) --- #
    # 300 nm stoichiometric SiN platform. Loss: ~1.5 dB/cm in the C-band
    # (Littlejohns et al., Appl. Sci. 10, 8201 (2020) — CORNERSTONE
    # platform paper; 300 nm film, single-mode strip, e-beam; their
    # O-band figure is <1 dB/cm). Qi has NO published ring measurement —
    # derived from loss via qi_from_loss(1.5, 2.0) ≈ 2.3e5 (flagged).
    # n_g ≈ 2.0 is an ESTIMATE for a 300 nm SiN strip at 1550 nm (used
    # only for the FSR-radius bookkeeping; verify against the PDK when
    # the S0.7/Stage-1 design needs it).
    "SiN_CORNERSTONE_300": PlatformConfig(
        name="SiN_CORNERSTONE_300",
        loss_dB_per_cm=1.5,
        Qi=2.3e5,               # derived from loss (no published ring Q)
        radius_um=238.5672580,  # FSR = 100 GHz at n_g=2.00
        FSR_GHz=100.0,
        n_g=2.00,
        drift_pm_per_K=14.0,    # SiN family value (AN800 midpoint reused)
        dn_dT_per_K=2.45e-5,
        sigma_FC_m3=0.0,
    ),
    # --- NEW (S0.0): class-leading ultra-high-Q SiN ------------------- #
    # Photonic-damascene SiN: 1.0 dB/m (= 0.01 dB/cm) propagation loss,
    # mean intrinsic Q0 > 30e6 (Liu et al., Nat. Commun. 12, 2236
    # (2021), wafer-scale; the proposal's "Q>10^7, single-digit dB/m"
    # class). Self-consistent: qi_from_loss(0.01, 2.09) ≈ 3.7e7.
    # n_g = 2.09 per the EPFL damascene microcomb device family
    # (100-GHz-FSR rings at R ≈ 228 um). NOT an open-MPW process —
    # this entry anchors the aspirational end of the Q range for
    # D-2026-06-08-1 and the S0.3 sensitivity sweep.
    "SiN_damascene_UHQ": PlatformConfig(
        name="SiN_damascene_UHQ",
        loss_dB_per_cm=0.01,
        Qi=3e7,
        radius_um=228.2940268,  # FSR = 100 GHz at n_g=2.09
        FSR_GHz=100.0,
        n_g=2.09,
        drift_pm_per_K=14.0,    # SiN family value (AN800 midpoint reused)
        dn_dT_per_K=2.45e-5,
        sigma_FC_m3=0.0,
    ),
    "Si_AIM_low_loss": PlatformConfig(
        name="Si_AIM_low_loss",
        loss_dB_per_cm=0.25,
        Qi=1.2e6,
        radius_um=5.5480758,    # FSR = 2000 GHz at n_g=4.3
        FSR_GHz=2000.0,
        n_g=4.3,
        drift_pm_per_K=83.5,    # midpoint of 77-90 pm/K
        dn_dT_per_K=1.86e-4,
        sigma_FC_m3=-1.35e-21,  # Soref+Bennett c-Si FCD at 1550 nm
    ),
    "Si_NEC": PlatformConfig(
        name="Si_NEC",
        loss_dB_per_cm=0.15,
        Qi=3e5,
        radius_um=5.5480758,
        FSR_GHz=2000.0,
        n_g=4.3,
        drift_pm_per_K=83.5,
        dn_dT_per_K=1.86e-4,
        sigma_FC_m3=-1.35e-21,
    ),
    "InP_IMEC_Generic": PlatformConfig(
        name="InP_IMEC_Generic",
        loss_dB_per_cm=0.5,
        Qi=5e4,
        radius_um=28.9172434,   # FSR = 500 GHz at n_g=3.3
        FSR_GHz=500.0,
        n_g=3.3,
        drift_pm_per_K=25.0,    # midpoint of 20-30 pm/K
        dn_dT_per_K=2.0e-4,
        sigma_FC_m3=-2e-21,
    ),
}


def get_platform(name: str) -> PlatformConfig:
    """Lookup PlatformConfig by name; raises KeyError on miss with a
    helpful message listing available platforms."""
    if name not in PLATFORM_REGISTRY:
        raise KeyError(
            f"Unknown ring platform '{name}'. "
            f"Known: {sorted(PLATFORM_REGISTRY)}"
        )
    return PLATFORM_REGISTRY[name]


def fsr_consistency_error_GHz(platform: PlatformConfig) -> float:
    """Absolute mismatch between tabulated FSR_GHz and derived FSR.
    Used by the registry sanity test (< 0.01 GHz)."""
    return abs(platform.FSR_GHz - derived_FSR_GHz(platform))
