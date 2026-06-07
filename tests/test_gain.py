# tests for photonic_ssm/gain.py (salvaged from pnn-multilayer physics.py
# lines ~57-136 @ e2eec80; these tests are new — the source repo
# exercised these functions only indirectly through its meshes).
"""Instantaneous gain / ASE / NL primitive tests."""

import math

import pytest
import torch

from photonic_ssm.gain import (
    modReLU,
    mzm_nonlinearity,
    photodetect,
    saturating_absorption,
    soa_activation,
    soa_activation_with_ase,
)


def test_photodetect_square_law():
    z = torch.tensor([3 + 4j, 1 + 0j, 0 + 0j], dtype=torch.complex128)
    I = photodetect(z)
    assert torch.allclose(I, torch.tensor([25.0, 1.0, 0.0],
                                          dtype=torch.float64))


def test_soa_activation_formula_and_phase_preservation():
    """f(z) = G*z/(1+alpha*|z|^2): check gain at zero power, the
    half-gain knee at |z|^2 = 1/alpha, and that the phase of z is
    untouched."""
    G, alpha = 4.0, 0.5
    gain = torch.tensor(G, dtype=torch.float64)
    al = torch.tensor(alpha, dtype=torch.float64)

    # Small-signal: |f(z)|/|z| -> G
    z = torch.tensor([1e-8 * (1 + 1j)], dtype=torch.complex128)
    out = soa_activation(z, gain, al)
    assert (out / z).real.item() == pytest.approx(G, rel=1e-6)

    # Knee: at |z|^2 = 1/alpha the field gain halves
    z = torch.tensor([math.sqrt(1 / alpha) + 0j], dtype=torch.complex128)
    out = soa_activation(z, gain, al)
    assert abs(out.item()) / abs(z.item()) == pytest.approx(G / 2, rel=1e-12)

    # Phase preservation at arbitrary phase
    z = torch.tensor([0.7 * math.e ** (1j * 1.234)], dtype=torch.complex128)
    out = soa_activation(z, gain, al)
    assert torch.angle(out).item() == pytest.approx(1.234, abs=1e-12)


def test_saturating_absorption_never_amplifies():
    z = torch.randn(64, dtype=torch.complex128) * 2.0
    alpha = torch.tensor(0.3, dtype=torch.float64)
    out = saturating_absorption(z, alpha)
    assert (out.abs() <= z.abs() + 1e-15).all()


def test_modrelu_known_values():
    z = torch.tensor([2.0 + 0j, 0.5 + 0j], dtype=torch.complex128)
    bias = torch.tensor(-1.0, dtype=torch.float64)
    out = modReLU(z, bias)
    # |z|=2, b=-1 -> (2-1)*z/|z| = 1.0 ; |z|=0.5, b=-1 -> relu(-0.5)=0
    assert abs(out[0].item() - 1.0) < 1e-6
    assert abs(out[1].item()) < 1e-12


def test_mzm_small_signal_linear():
    drive = torch.tensor(0.1, dtype=torch.float64)
    z = torch.tensor([0.01 + 0j], dtype=torch.complex128)
    out = mzm_nonlinearity(z, drive)
    expected = (math.pi / 2) * 0.01 * 0.1
    assert out.real.item() == pytest.approx(expected, rel=1e-3)


# ---------------------------------------------------------------------- #
#  ASE injection
# ---------------------------------------------------------------------- #

def test_ase_no_noise_when_no_net_gain():
    """G_eff <= 1 -> P_ase = 0 -> output identical to noiseless path
    (up to the deterministic 1e-30 std floor, i.e. ~1e-15 noise std)."""
    z = torch.randn(256, dtype=torch.complex128)
    gain = torch.tensor(0.9, dtype=torch.float64)   # net loss
    alpha = torch.tensor(0.1, dtype=torch.float64)
    gen = torch.Generator().manual_seed(0)
    out_ase = soa_activation_with_ase(z, gain, alpha, generator=gen)
    out_clean = soa_activation(z, gain, alpha)
    assert (out_ase - out_clean).abs().max().item() < 1e-12


def test_ase_seeded_generator_reproducible():
    z = torch.randn(128, dtype=torch.complex128) * 0.1
    gain = torch.tensor(10.0, dtype=torch.float64)
    alpha = torch.tensor(0.01, dtype=torch.float64)
    out1 = soa_activation_with_ase(
        z, gain, alpha, generator=torch.Generator().manual_seed(5))
    out2 = soa_activation_with_ase(
        z, gain, alpha, generator=torch.Generator().manual_seed(5))
    out3 = soa_activation_with_ase(
        z, gain, alpha, generator=torch.Generator().manual_seed(6))
    assert torch.equal(out1, out2)
    assert not torch.equal(out1, out3)


def test_ase_variance_matches_formula():
    """Statistical check of the ASE power scaling:
    P_ase = n_sp*(G_eff-1)*h_nu*B_opt, complex Gaussian with variance
    P_ase/2 per quadrature. Use a high-gain, low-power regime so G_eff
    is constant across elements; 200k samples -> ~0.3% std error on the
    variance estimate; assert within 3%."""
    n = 200_000
    n_sp, B_opt = 1.5, 32e9
    h_nu = 1.282e-19
    G = 100.0  # field-gain param; G_eff = |G| at zero power
    z = torch.zeros(n, dtype=torch.complex128)  # zero signal: pure ASE out
    gain = torch.tensor(G, dtype=torch.float64)
    alpha = torch.tensor(0.1, dtype=torch.float64)
    gen = torch.Generator().manual_seed(123)
    out = soa_activation_with_ase(z, gain, alpha, n_sp=n_sp, B_opt=B_opt,
                                  generator=gen)
    P_ase_expected = n_sp * (G - 1.0) * h_nu * B_opt
    # Total noise power = E[|noise|^2] = 2 * (P_ase/2) = P_ase
    P_measured = (out.abs() ** 2).mean().item()
    assert P_measured == pytest.approx(P_ase_expected, rel=0.03)


def test_ase_autograd_safe():
    """The deterministic signal path through soa_activation_with_ase
    carries gradients (no no_grad/detach) — constraint (3a) hygiene."""
    z = (torch.randn(16, dtype=torch.complex128)
         * 0.1).requires_grad_(True)
    gain = torch.tensor(5.0, dtype=torch.float64, requires_grad=True)
    alpha = torch.tensor(0.05, dtype=torch.float64, requires_grad=True)
    out = soa_activation_with_ase(
        z, gain, alpha, generator=torch.Generator().manual_seed(1))
    loss = out.abs().pow(2).sum()
    loss.backward()
    assert z.grad is not None and torch.isfinite(z.grad).all()
    assert gain.grad is not None and torch.isfinite(gain.grad).all()
    assert alpha.grad is not None and torch.isfinite(alpha.grad).all()
