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
# Adaptations for Project_SSM (task S0.1, deliverable 7 / F13.1):
#   - Q/loss self-consistency fix. Each entry now declares a `q_basis`
#     naming which of (Qi, loss) is the registered PRIMARY; the partner
#     is DERIVED from it via the textbook relation Qi = 2*pi*n_g/(lam*a),
#     so the SiN entries are internally consistent (the salvaged
#     `SiN_LIGENTEC_AN800` previously tabulated Qi=2e6 *and* 0.03 dB/cm,
#     which disagree ~5.7x — flagged independently by the Executor (S0.0)
#     and Critic (F13.1)). `loss_q_consistency_error()` +
#     `loss_q_ceiling_ok()` back a new registry test alongside the FSR
#     check. The operating-Q choice stays parked (D-2026-06-08-1 / PR-4).
# Everything else (derived-FSR consistency check) is lifted unchanged.
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
        q_basis          : str,      # "Qi" | "loss" | "independent"
                                     # (which field is primary; see below)
    )

Redundancy note: `radius_um`, `FSR_GHz`, `n_g` are over-specified.
`derived_FSR_GHz(p)` recomputes FSR from radius + n_g and the registry
test asserts |derived - tabulated| < 0.01 GHz.

Q/loss self-consistency (S0.1 / F13.1). `qi_from_loss()` is the textbook
propagation-loss-limited intrinsic Q, Qi = 2*pi*n_g/(lambda*alpha). Each
entry declares which field is PRIMARY:
  * q_basis="Qi"   — Qi is the registered (published/headline) value;
                     `loss_dB_per_cm` is DERIVED from it. (The SiN entries
                     whose Q anchors the roadmap's Q-span: AN800 2e6,
                     damascene 3e7.)
  * q_basis="loss" — loss is the registered value; Qi is DERIVED. (Entries
                     with no published ring Q, e.g. CORNERSTONE.)
  * q_basis="independent" — Qi and loss are independently published and
                     the ring is NOT propagation-limited (bend-/coupling-
                     limited), so only the physical CEILING holds:
                     Qi <= qi_from_loss(loss). (Si/InP entries.)
`loss_q_consistency_error()` and `loss_q_ceiling_ok()` back the registry
test. Propagation loss sets a Q ceiling; other loss channels only lower
Qi — so Qi <= qi_from_loss(loss) is the invariant for every entry, with
equality for the loss-limited SiN rings.
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
    q_basis: str = "independent"   # "Qi" | "loss" | "independent" (F13.1)


def derived_FSR_GHz(platform: PlatformConfig) -> float:
    """FSR = c / (n_g * L_round_trip), with L_round_trip = 2*pi*R.

    Returns the FSR in GHz computed from radius_um and n_g, independent
    of the tabulated FSR_GHz field. Used by the consistency test.
    """
    L_m = 2.0 * math.pi * (platform.radius_um * 1e-6)
    fsr_hz = _C_M_PER_S / (platform.n_g * L_m)
    return fsr_hz / 1e9


def alpha_per_m_from_loss(loss_dB_per_cm: float) -> float:
    """Power attenuation alpha [1/m] from loss in dB/cm:
    alpha = loss_dB_per_m / (10*log10(e))."""
    return (loss_dB_per_cm * 100.0) / (10.0 * math.log10(math.e))


def qi_from_loss(loss_dB_per_cm: float, n_g: float,
                 lambda_m: float = _LAMBDA_REF_M) -> float:
    """Intrinsic Q implied by propagation loss: Qi = 2*pi*n_g / (lambda*alpha)
    with alpha [1/m] = loss_dB_per_m / (10*log10(e)).

    This is the propagation-loss-limited *ceiling* on intrinsic Q (other
    loss channels — bend, coupler, absorption — only lower Qi). Used by
    the registry self-consistency test, the entries that derive one of
    (Qi, loss) from the other, and the S0.1 pole-region bound.
    """
    return 2.0 * math.pi * n_g / (lambda_m * alpha_per_m_from_loss(loss_dB_per_cm))


def loss_dB_per_cm_from_qi(Qi: float, n_g: float,
                           lambda_m: float = _LAMBDA_REF_M) -> float:
    """Inverse of `qi_from_loss`: the propagation loss (dB/cm) consistent
    with a propagation-limited intrinsic Q. alpha = 2*pi*n_g/(lambda*Qi);
    loss_dB_per_cm = alpha * 10*log10(e) / 100."""
    alpha_per_m = 2.0 * math.pi * n_g / (lambda_m * Qi)
    return alpha_per_m * (10.0 * math.log10(math.e)) / 100.0


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
    # Qi=2e6 is the registered foundry-grade corner used across the
    # roadmap (D-2026-06-08-1's "2x10^6" end); loss is DERIVED from it
    # (q_basis="Qi"). The salvaged entry's 0.03 dB/cm was inconsistent
    # (it implies Qi=1.14e7, ~5.7x off) and is superseded; 0.172 dB/cm is
    # the loss consistent with Qi=2e6 at n_g=1.95 — physically sensible
    # for a foundry SiN ring (AN800 has separately *demonstrated* up to
    # Qi=6.8e6 at 0.051 dB/cm; we register the conservative corner, not
    # the best result — the operating Q stays parked, PR-4).
    "SiN_LIGENTEC_AN800": PlatformConfig(
        name="SiN_LIGENTEC_AN800",
        loss_dB_per_cm=0.171647,  # DERIVED from Qi=2e6 (q_basis="Qi")
        Qi=2e6,
        radius_um=244.6843671,  # FSR = 100 GHz at n_g=1.95
        FSR_GHz=100.0,
        n_g=1.95,
        drift_pm_per_K=14.0,    # midpoint of 10-18 pm/K range
        dn_dT_per_K=2.45e-5,
        sigma_FC_m3=0.0,        # SiN has no measurable FCD at 1550 nm
        q_basis="Qi",
    ),
    # --- NEW (S0.0): CORNERSTONE open-MPW SiN (proposal §8 foundry) --- #
    # 300 nm stoichiometric SiN platform. Loss: ~1.5 dB/cm in the C-band
    # (Littlejohns et al., Appl. Sci. 10, 8201 (2020) — CORNERSTONE
    # platform paper; 300 nm film, single-mode strip, e-beam; their
    # O-band figure is <1 dB/cm). loss is PRIMARY (q_basis="loss"); Qi has
    # NO published ring measurement and is DERIVED via
    # qi_from_loss(1.5, 2.0) = 2.347e5. n_g ≈ 2.0 is an ESTIMATE for a
    # 300 nm SiN strip at 1550 nm (used only for the FSR-radius
    # bookkeeping; verify against the PDK when S0.7/Stage-1 needs it).
    "SiN_CORNERSTONE_300": PlatformConfig(
        name="SiN_CORNERSTONE_300",
        loss_dB_per_cm=1.5,
        Qi=2.347314e5,          # DERIVED from loss=1.5 dB/cm (q_basis="loss")
        radius_um=238.5672580,  # FSR = 100 GHz at n_g=2.00
        FSR_GHz=100.0,
        n_g=2.00,
        drift_pm_per_K=14.0,    # SiN family value (AN800 midpoint reused)
        dn_dT_per_K=2.45e-5,
        sigma_FC_m3=0.0,
        q_basis="loss",
    ),
    # --- NEW (S0.0): class-leading ultra-high-Q SiN ------------------- #
    # Photonic-damascene SiN: mean intrinsic Q0 > 30e6 at ~1.0 dB/m
    # (Liu et al., Nat. Commun. 12, 2236 (2021), wafer-scale; the
    # proposal's "Q>10^7, single-digit dB/m" class). Qi=3e7 is PRIMARY
    # (q_basis="Qi") — the registered "3x10^7" aspirational corner used
    # by the roadmap/pole-region span; loss is DERIVED = 0.01227 dB/cm
    # (1.23 dB/m), within the device spread of Liu's ~1 dB/m headline
    # (loss=1 dB/m alone would imply Qi=3.68e7). n_g = 2.09 per the EPFL
    # damascene microcomb family (100-GHz-FSR rings, R ≈ 228 um). NOT an
    # open-MPW process — anchors the aspirational Q end (D-2026-06-08-1 /
    # PR-4 sensitivity sweep).
    "SiN_damascene_UHQ": PlatformConfig(
        name="SiN_damascene_UHQ",
        loss_dB_per_cm=0.012265,  # DERIVED from Qi=3e7 (q_basis="Qi")
        Qi=3e7,
        radius_um=228.2940268,  # FSR = 100 GHz at n_g=2.09
        FSR_GHz=100.0,
        n_g=2.09,
        drift_pm_per_K=14.0,    # SiN family value (AN800 midpoint reused)
        dn_dT_per_K=2.45e-5,
        sigma_FC_m3=0.0,
        q_basis="Qi",
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
        q_basis="independent",  # bend-/coupling-limited: Qi < loss ceiling
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
        q_basis="independent",  # bend-/coupling-limited: Qi < loss ceiling
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
        q_basis="independent",  # bend-/coupling-limited: Qi < loss ceiling
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


def loss_q_consistency_error(platform: PlatformConfig) -> float:
    """Relative mismatch |Qi_tabulated - qi_from_loss(loss)| / Qi_tabulated.

    For q_basis in {"Qi", "loss"} the partner field is derived from the
    primary, so this should be ~0 (float round-off only). For
    q_basis="independent" it is the *fractional headroom below the
    propagation-loss ceiling* (Qi sits below qi_from_loss(loss)), which is
    physical and NOT required to be small — use `loss_q_ceiling_ok` there.
    """
    ceil = qi_from_loss(platform.loss_dB_per_cm, platform.n_g)
    return abs(platform.Qi - ceil) / platform.Qi


def loss_q_ceiling_ok(platform: PlatformConfig, rel_tol: float = 1e-3) -> bool:
    """The universal Q/loss invariant (F13.1): intrinsic Q cannot exceed
    the propagation-loss-limited ceiling, Qi <= qi_from_loss(loss). Other
    loss channels (bend, coupler, absorption) only lower Qi.

    Returns True iff Qi <= qi_from_loss(loss) * (1 + rel_tol). The small
    tolerance admits float round-off for the loss-limited SiN entries
    (q_basis in {"Qi","loss"}) that sit *on* the ceiling by construction.
    """
    ceil = qi_from_loss(platform.loss_dB_per_cm, platform.n_g)
    return platform.Qi <= ceil * (1.0 + rel_tol)
