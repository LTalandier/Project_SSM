# tests salvaged/extended from pnn-multilayer @ e2eec80 :
#   tests/test_mrr_primitives.py::test_platform_fsr_consistency
# Extended for Project_SSM: the two new SiN entries enter the
# parameterized consistency test automatically; S0.1/F13.1 added the
# loss<->Q self-consistency test alongside the FSR check.
"""Platform-registry tests (S0.0 smoke-test deliverable (iii) +
S0.1/F13.1 loss<->Q self-consistency)."""

import pytest

from photonic_ssm.platforms import (
    PLATFORM_REGISTRY,
    fsr_consistency_error_GHz,
    get_platform,
    qi_from_loss,
    loss_dB_per_cm_from_qi,
    loss_q_consistency_error,
    loss_q_ceiling_ok,
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


@pytest.mark.parametrize("platform_name", list(PLATFORM_REGISTRY))
def test_loss_q_ceiling_invariant(platform_name):
    """F13.1: the universal Q/loss invariant — intrinsic Q cannot exceed
    the propagation-loss-limited ceiling Qi <= qi_from_loss(loss). Holds
    for EVERY entry (loss-limited SiN sits on the ceiling; bend/coupling-
    limited Si/InP sit below it)."""
    p = PLATFORM_REGISTRY[platform_name]
    assert loss_q_ceiling_ok(p), (
        f"{platform_name}: Qi={p.Qi:.3e} exceeds loss ceiling "
        f"{qi_from_loss(p.loss_dB_per_cm, p.n_g):.3e}")


@pytest.mark.parametrize("platform_name", [
    n for n, p in PLATFORM_REGISTRY.items() if p.q_basis in ("Qi", "loss")])
def test_loss_q_mutually_consistent_for_derived_entries(platform_name):
    """F13.1: where one of (Qi, loss) is primary and the other DERIVED
    (q_basis in {Qi, loss} — the SiN entries), the two must be mutually
    consistent (loss_q_consistency_error ~ 0, float round-off only)."""
    p = PLATFORM_REGISTRY[platform_name]
    err = loss_q_consistency_error(p)
    assert err < 1e-3, (
        f"{platform_name} (q_basis={p.q_basis}): Qi={p.Qi:.4e} vs "
        f"loss-implied {qi_from_loss(p.loss_dB_per_cm, p.n_g):.4e}, "
        f"rel err {err:.2e}")


def test_AN800_q_loss_reconciled():
    """F13.1 reconciliation: SiN_LIGENTEC_AN800 previously tabulated
    Qi=2e6 AND 0.03 dB/cm, which disagree ~5.7x (0.03 dB/cm implies
    Qi~1.14e7). Qi=2e6 is now the registered primary (foundry corner) and
    loss is derived consistently (~0.172 dB/cm)."""
    p = get_platform("SiN_LIGENTEC_AN800")
    assert p.q_basis == "Qi" and p.Qi == 2e6
    expected_loss = loss_dB_per_cm_from_qi(2e6, p.n_g)
    assert abs(p.loss_dB_per_cm - expected_loss) < 1e-4
    # the OLD value (0.03) would have implied a ~5.7x-too-high Qi
    assert qi_from_loss(0.03, p.n_g) / p.Qi > 5.0


def test_non_sin_entries_below_ceiling():
    """The bend-/coupling-limited Si/InP entries (q_basis='independent')
    sit strictly BELOW the propagation ceiling (Qi < qi_from_loss),
    which is physical — only SiN is propagation-limited here."""
    for name in ("Si_AIM_low_loss", "Si_NEC", "InP_IMEC_Generic"):
        p = get_platform(name)
        assert p.q_basis == "independent"
        assert p.Qi < qi_from_loss(p.loss_dB_per_cm, p.n_g)
