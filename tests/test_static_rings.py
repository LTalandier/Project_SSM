# tests salvaged/extended from pnn-multilayer @ e2eec80 :
#   tests/test_mrr_primitives.py (test_n2_series_matches_madsen,
#   test_fsr_repetition, test_drift_inject_zero_bit_identical,
#   test_drift_distribution — re-pointed at the de-classed pure
#   functions) + NEW analytic add-drop checks (S0.0 smoke-test
#   deliverable (ii)).
"""Static CW ring-reference + drift tests."""

import math

import pytest
import torch

from photonic_ssm.platforms import PLATFORM_REGISTRY
from photonic_ssm.static_rings import (
    add_drop_drop,
    add_drop_through,
    cascade_through,
    drift_sigma_dimensionless,
    sample_drift,
    single_bus_through,
    t_from_kappa,
)


DELTAS = torch.linspace(-math.pi, math.pi, 257, dtype=torch.float64)


# ====================================================================== #
#  Smoke-test deliverable (ii): salvaged static Lorentzian vs the
#  analytic add-drop CW transfer function
# ====================================================================== #

def test_salvaged_single_bus_matches_analytic_add_drop_limit():
    """The salvaged single-bus form IS the analytic add-drop through
    port in the kappa2 -> 0 (t2 = 1) limit, up to the documented overall
    -1 phase-reference convention:

        add_drop_through(phi, t1, t2=1, a) == -single_bus_through(phi, t1, a)

    Checked in full complex value (not just magnitude) over a detuning
    sweep, lossless and lossy. Tolerance 1e-12 (float64)."""
    for t1, a in [(0.95, 1.0), (0.8, 1.0), (0.95, 0.98), (0.6, 0.9)]:
        T_salvaged = single_bus_through(DELTAS, t=t1, a=a)
        T_analytic = add_drop_through(DELTAS, t1=t1, t2=1.0, a=a)
        err = (T_analytic - (-T_salvaged)).abs().max().item()
        assert err < 1e-12, (
            f"t1={t1}, a={a}: max |T_adddrop - (-T_singlebus)| = {err:.3e}")


def test_add_drop_lossless_power_conservation():
    """Lossless add-drop ring: |T_through|^2 + |T_drop|^2 = 1 exactly,
    for every detuning (the two-port CW unitarity check)."""
    for t1, t2 in [(0.95, 0.95), (0.9, 0.8), (0.99, 0.7)]:
        Tt = add_drop_through(DELTAS, t1=t1, t2=t2, a=1.0)
        Td = add_drop_drop(DELTAS, t1=t1, t2=t2, a=1.0)
        total = (Tt.abs() ** 2 + Td.abs() ** 2)
        err = (total - 1.0).abs().max().item()
        assert err < 1e-12, (
            f"t1={t1}, t2={t2}: max | |Tt|^2+|Td|^2 - 1 | = {err:.3e}")


def test_add_drop_critical_coupling_extinction():
    """Critical coupling t1 = t2*a: through port fully extinguishes on
    resonance (T_t(0) = 0); same for the salvaged single-bus at a = t."""
    zero = torch.zeros(1, dtype=torch.float64)
    t2, a = 0.95, 0.98
    t1 = t2 * a
    assert add_drop_through(zero, t1=t1, t2=t2, a=a).abs().item() < 1e-14
    assert single_bus_through(zero, t=0.95, a=0.95).abs().item() < 1e-14


def test_add_drop_far_detuned_passthrough():
    """At phi = pi (half an FSR off resonance) the lossless through port
    transmits nearly everything for weak coupling."""
    pi_t = torch.tensor([math.pi], dtype=torch.float64)
    Tt = add_drop_through(pi_t, t1=0.99, t2=0.99, a=1.0)
    assert Tt.abs().item() > 0.999


# ====================================================================== #
#  Ported salvaged-form tests
# ====================================================================== #

def test_single_bus_allpass_unitarity():
    """Lossless single-bus ring (a=1) is all-pass: |T(delta)| = 1 for
    all detunings (energy has nowhere else to go)."""
    T = single_bus_through(DELTAS, t=0.7, a=1.0)
    err = (T.abs() - 1.0).abs().max().item()
    assert err < 1e-12, f"all-pass unitarity violated: {err:.3e}"


def test_fsr_repetition():
    """T(delta) is 2*pi-periodic (one FSR = 2*pi round-trip phase).
    [port of test_fsr_repetition]"""
    T0 = single_bus_through(DELTAS, t=0.9, a=0.97)
    T1 = single_bus_through(DELTAS + 2.0 * math.pi, t=0.9, a=0.97)
    err = (T1 - T0).abs().max().item()
    assert err < 1e-12, f"FSR-repetition error {err:.3e}"


def test_n2_series_matches_madsen():
    """N=2 series cascade matches the analytic product
    T_total = T_ring1 * T_ring2 (Madsen 1999 §4.4.3 single-bus cascade).
    [port of test_n2_series_matches_madsen; tolerance tightened to
    float64 since the cascade is now a pure function]"""
    kappa1, kappa2 = 0.3, 0.5
    t1, t2 = t_from_kappa(kappa1), t_from_kappa(kappa2)
    deltas = torch.linspace(-math.pi / 2, math.pi / 2, 64,
                            dtype=torch.float64)
    T_cascade = cascade_through(deltas, [kappa1, kappa2], a=1.0)
    T_expected = (single_bus_through(deltas, t1, 1.0)
                  * single_bus_through(deltas, t2, 1.0))
    err = (T_cascade - T_expected).abs().max().item()
    assert err < 1e-12, f"N=2 cascade vs Madsen analytical: {err:.3e}"


# ====================================================================== #
#  Drift machinery (ported)
# ====================================================================== #

def test_drift_zero_sigma_is_exact_zero():
    """sigma = 0 -> drift phases exactly zero (the zero-drift path stays
    bit-identical to no-drift). [port of
    test_drift_inject_zero_bit_identical, now trivially exact since the
    de-classed function returns the additive phases]"""
    drift_dim, drift_phase = sample_drift(
        N=8, sigma_pm_per_K=0.0, FSR_GHz=100.0, seed=42)
    assert torch.equal(drift_dim, torch.zeros(8))
    assert torch.equal(drift_phase, torch.zeros(8))


def test_drift_deterministic_per_seed():
    a1, p1 = sample_drift(N=16, sigma_pm_per_K=14.0, FSR_GHz=100.0, seed=7)
    a2, p2 = sample_drift(N=16, sigma_pm_per_K=14.0, FSR_GHz=100.0, seed=7)
    b1, _ = sample_drift(N=16, sigma_pm_per_K=14.0, FSR_GHz=100.0, seed=8)
    assert torch.equal(a1, a2) and torch.equal(p1, p2)
    assert not torch.equal(a1, b1)


def test_drift_distribution():
    """sigma = 14 pm/K, dT = 1 K over 1000 realizations gives a sample
    distribution with mean ~ 0 and std consistent with the pm/K ->
    dimensionless conversion. [port of test_drift_distribution]

    sigma_lambda = 14 pm -> sigma_f = sigma_lambda*c/lambda^2 ~ 1.748 GHz
    For FSR = 100 GHz (SiN_LIGENTEC_AN800): sigma_dim ~ 0.01748."""
    N, n_real = 4, 1000
    sigma_pm_per_K, delta_T_K = 14.0, 1.0
    FSR_GHz = PLATFORM_REGISTRY["SiN_LIGENTEC_AN800"].FSR_GHz

    samples = []
    for k in range(n_real):
        dim, _ = sample_drift(N=N, sigma_pm_per_K=sigma_pm_per_K,
                              FSR_GHz=FSR_GHz, seed=10_000 + k,
                              delta_T_K=delta_T_K)
        samples.append(dim)
    s = torch.stack(samples).flatten()

    expected_sigma = (
        sigma_pm_per_K * 1e-12 * delta_T_K
        * 2.99792458e8 / (1550e-9 ** 2)
    ) / (FSR_GHz * 1e9)

    assert abs(s.mean().item()) < expected_sigma * 0.05, \
        f"sample mean {s.mean().item():.5f} far from 0"
    rel_err = abs(s.std().item() - expected_sigma) / expected_sigma
    assert rel_err < 0.05, (
        f"sample std {s.std().item():.5f} vs expected {expected_sigma:.5f} "
        f"(rel err {rel_err:.3f} > 0.05)")


def test_drift_sigma_dimensionless_value():
    """Pin the converted value itself (Critic-audited conversion)."""
    sigma_dim = drift_sigma_dimensionless(14.0, 100.0, 1.0)
    assert sigma_dim == pytest.approx(0.017479, rel=1e-3)
