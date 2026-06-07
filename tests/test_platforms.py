# tests salvaged/extended from pnn-multilayer @ e2eec80 :
#   tests/test_mrr_primitives.py::test_platform_fsr_consistency
# Extended for Project_SSM: the two new SiN entries enter the
# parameterized consistency test automatically; added qi_from_loss
# cross-checks for the entries whose Qi is derived/literature-anchored.
"""Platform-registry tests (S0.0 smoke-test deliverable (iii))."""

import math

import pytest

from photonic_ssm.platforms import (
    PLATFORM_REGISTRY,
    fsr_consistency_error_GHz,
    get_platform,
    qi_from_loss,
)


@pytest.mark.parametrize("platform_name", list(PLATFORM_REGISTRY))
def test_platform_fsr_consistency(platform_name):
    """For every platform: |tabulated FSR - derived FSR| < 0.01 GHz.

    Guards the radius values (radius/FSR/n_g are over-specified by
    design; this is the smoke-test deliverable (iii))."""
    p = PLATFORM_REGISTRY[platform_name]
    err = fsr_consistency_error_GHz(p)
    assert err < 0.01, (
        f"{platform_name}: tabulated FSR={p.FSR_GHz} GHz, "
        f"derived mismatch={err:.4f} GHz"
    )


def test_get_platform_unknown_raises():
    with pytest.raises(KeyError, match="Unknown ring platform"):
        get_platform("definitely_not_a_platform")


def test_get_platform_known():
    p = get_platform("SiN_LIGENTEC_AN800")
    assert p.name == "SiN_LIGENTEC_AN800"
    assert p.Qi == 2e6


def test_new_sin_entries_present():
    """S0.0 added CORNERSTONE + class-leading UHQ entries; together with
    AN800 they span the Q range for the parked operating-point decision
    (D-2026-06-08-1). No operating Q is chosen anywhere in the package."""
    corner = get_platform("SiN_CORNERSTONE_300")
    uhq = get_platform("SiN_damascene_UHQ")
    an800 = get_platform("SiN_LIGENTEC_AN800")
    # All SiN: no FCD, same thermo-optic material coefficient.
    for p in (corner, uhq, an800):
        assert p.sigma_FC_m3 == 0.0
        assert p.dn_dT_per_K == pytest.approx(2.45e-5)
    # The range spans > 2 orders of magnitude in Qi.
    assert corner.Qi < an800.Qi < uhq.Qi
    assert uhq.Qi / corner.Qi > 100


def test_qi_from_loss_cross_checks():
    """Qi <-> loss textbook relation backs the new entries:

    - CORNERSTONE Qi is DERIVED from its loss (no published ring Q):
      tabulated must match qi_from_loss to ~3%.
    - damascene UHQ: published loss (0.01 dB/cm) and published Q (3e7)
      must be mutually consistent within ~25% (1.0 dB/m <-> Qi~3.7e7).
    """
    corner = get_platform("SiN_CORNERSTONE_300")
    qi_derived = qi_from_loss(corner.loss_dB_per_cm, corner.n_g)
    assert abs(corner.Qi - qi_derived) / qi_derived < 0.03, (
        f"CORNERSTONE tabulated Qi={corner.Qi:.3e} vs derived "
        f"{qi_derived:.3e}")

    uhq = get_platform("SiN_damascene_UHQ")
    qi_derived = qi_from_loss(uhq.loss_dB_per_cm, uhq.n_g)
    assert abs(uhq.Qi - qi_derived) / qi_derived < 0.25, (
        f"UHQ tabulated Qi={uhq.Qi:.3e} vs loss-derived {qi_derived:.3e}")
