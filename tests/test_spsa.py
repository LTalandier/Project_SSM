# tests for photonic_ssm/estimators/spsa.py (salvaged from
# pnn-multilayer adaptation/perturbation_gradient.py @ e2eec80).
# Reproduces the source repo's G3 validation anchor — FD vs autograd
# RMS relative error < 1% — on a decoupled toy model built from
# salvaged primitives (the original anchor ran on the equalization
# mesh, which was not salvaged).
"""SPSA / perturbation-gradient tests (S0.0 key gate: FD-vs-autograd
anchor reproduced after decoupling)."""

import pytest
import torch
import torch.nn as nn

from photonic_ssm.estimators import PerturbationAdaptor, compare_fd_vs_autograd
from photonic_ssm.gain import soa_activation


# ---------------------------------------------------------------------- #
#  Toy models (top-level: also used by the runner integration test)
# ---------------------------------------------------------------------- #

class ToyRingWeightModel(nn.Module):
    """Differentiable stand-in for a photonic forward model: complex
    diagonal transmission weights t*e^{j*phi} (the transmission-space
    ring-bank parameterization) followed by saturable gain (salvaged
    `soa_activation`). float64 throughout so the FD anchor is limited
    by truncation, not round-off."""

    def __init__(self, N: int = 6, seed: int = 0):
        super().__init__()
        gen = torch.Generator().manual_seed(seed)
        self.t_raw = nn.Parameter(
            0.3 * torch.randn(N, generator=gen, dtype=torch.float64))
        self.phi = nn.Parameter(
            0.3 * torch.randn(N, generator=gen, dtype=torch.float64))
        self.register_buffer("gain", torch.tensor(2.0, dtype=torch.float64))
        self.register_buffer("alpha", torch.tensor(0.2, dtype=torch.float64))

    def forward(self, z):                      # z: [batch, N] complex128
        t = torch.sigmoid(self.t_raw) * 0.95
        w = (t * torch.exp(1j * self.phi))     # [N] complex128
        return soa_activation(z * w, self.gain, self.alpha)


class VectorModel(nn.Module):
    """theta-only model for optimizer convergence tests."""

    def __init__(self, n: int = 12, seed: int = 0):
        super().__init__()
        gen = torch.Generator().manual_seed(seed)
        self.theta = nn.Parameter(
            torch.randn(n, generator=gen, dtype=torch.float64))

    def forward(self, _inputs):
        return self.theta


def nmse_loss(out, target):
    return ((out - target).abs() ** 2).mean() / (target.abs() ** 2).mean()


def quadratic_loss(out, target):
    return ((out - target) ** 2).mean()


def _toy_batch(N=6, batch=32, seed=100):
    gen = torch.Generator().manual_seed(seed)
    z = (torch.randn(batch, N, generator=gen, dtype=torch.float64)
         + 1j * torch.randn(batch, N, generator=gen, dtype=torch.float64))
    target = (torch.randn(batch, N, generator=gen, dtype=torch.float64)
              + 1j * torch.randn(batch, N, generator=gen,
                                 dtype=torch.float64))
    return 0.5 * z, 0.5 * target


# ---------------------------------------------------------------------- #
#  The anchor (task S0.0 key gate)
# ---------------------------------------------------------------------- #

def test_fd_vs_autograd_anchor_below_1pct():
    """FD gradient vs autograd on a static noiseless model:
    RMS relative error < 1% (the inherited G3 anchor). With float64 and
    eps=1e-3 the agreement is far tighter; assert both the inherited
    anchor and a tight sanity bound."""
    model = ToyRingWeightModel(N=6, seed=0)
    z, target = _toy_batch()
    fd, ag, rms_rel = compare_fd_vs_autograd(
        model, z, target, loss_fn=nmse_loss, eps=1e-3)
    assert fd.shape == ag.shape == (12,)
    assert rms_rel < 0.01, f"FD-vs-autograd anchor broken: {rms_rel:.3e}"
    assert rms_rel < 1e-5, f"float64 FD should be ~truncation-limited: " \
                           f"{rms_rel:.3e}"


def test_per_param_estimator_matches_autograd():
    """The 'per_param' estimator path inside PerturbationAdaptor
    produces the same FD gradient compare_fd_vs_autograd computes."""
    model = ToyRingWeightModel(N=4, seed=1)
    z, target = _toy_batch(N=4, seed=101)
    adaptor = PerturbationAdaptor(
        model, loss_fn=nmse_loss, estimator='per_param', eps=1e-3,
        use_adam=False, lr=0.0)   # lr=0: estimate only, no movement
    grads, L0, _ = adaptor._per_param_gradient(z, target)
    fd_flat = torch.cat([g.reshape(-1) for g in grads])

    _, ag_flat, _ = compare_fd_vs_autograd(
        model, z, target, loss_fn=nmse_loss, eps=1e-3)
    rms = torch.sqrt(torch.mean((fd_flat - ag_flat) ** 2)).item()
    denom = torch.sqrt(torch.mean(ag_flat ** 2)).item()
    assert rms / denom < 1e-5


# ---------------------------------------------------------------------- #
#  SPSA mechanics
# ---------------------------------------------------------------------- #

def test_spsa_probe_restores_params():
    """After a gradient estimate (probes +eps, -2eps, +eps) the params
    must be back at nominal to float64 round-off."""
    model = ToyRingWeightModel(N=6, seed=2)
    z, target = _toy_batch(seed=102)
    before = torch.cat([p.detach().clone().reshape(-1)
                        for _, p in model.named_parameters()])
    adaptor = PerturbationAdaptor(model, loss_fn=nmse_loss,
                                  estimator='spsa', eps=0.01, rng_seed=3)
    adaptor._spsa_gradient(z, target)
    after = torch.cat([p.detach().clone().reshape(-1)
                       for _, p in model.named_parameters()])
    assert (before - after).abs().max().item() < 1e-12


def test_forward_pass_accounting():
    """n_forward_equivalents is the bake-off's primary-metric
    bookkeeping — it must count exactly."""
    z, target = _toy_batch(N=4, seed=103)

    m1 = ToyRingWeightModel(N=4, seed=3)
    spsa = PerturbationAdaptor(m1, loss_fn=nmse_loss, estimator='spsa',
                               rng_seed=0)
    for _ in range(5):
        spsa.step(z, target)
    assert spsa.n_updates == 5
    assert spsa.n_forward_equivalents == 10          # 2 per update

    m2 = ToyRingWeightModel(N=4, seed=3)
    fd = PerturbationAdaptor(m2, loss_fn=nmse_loss, estimator='per_param',
                             rng_seed=0)
    fd.step(z, target)
    assert fd.n_params == 8
    assert fd.n_forward_equivalents == 2 * 8 + 1     # 2N + 1 per update


def test_spsa_seeded_reproducibility():
    z, target = _toy_batch(seed=104)
    trajs = []
    for seed in (7, 7, 8):
        model = ToyRingWeightModel(N=6, seed=4)
        adaptor = PerturbationAdaptor(model, loss_fn=nmse_loss,
                                      estimator='spsa', eps=0.01, lr=1e-2,
                                      rng_seed=seed)
        for _ in range(10):
            adaptor.step(z, target)
        trajs.append(adaptor.current_params_vector())
    assert torch.equal(trajs[0], trajs[1])           # same seed -> identical
    assert not torch.equal(trajs[0], trajs[2])       # diff seed -> different


def test_spsa_converges_on_quadratic():
    """SPSA + Adam reduces a 12-dim quadratic by >20x within 400
    updates (deterministic given seeds). This is the 'does the
    estimator actually optimize' smoke check, not a performance claim."""
    model = VectorModel(n=12, seed=5)
    target = torch.zeros(12, dtype=torch.float64)
    adaptor = PerturbationAdaptor(model, loss_fn=quadratic_loss,
                                  estimator='spsa', eps=0.02, lr=0.05,
                                  use_adam=True, rng_seed=11)
    initial = quadratic_loss(model(None), target).item()
    for _ in range(400):
        adaptor.step(None, target)
    final = quadratic_loss(model(None), target).item()
    assert final < initial / 20, (
        f"SPSA failed to converge: {initial:.4f} -> {final:.4f}")


def test_injected_forward_fn_used():
    """The decoupled forward API: a custom forward_fn must be honored
    (here: model called with a transformed input)."""
    calls = []

    def custom_forward(model, inputs):
        calls.append(1)
        return model(inputs * 2.0)

    model = ToyRingWeightModel(N=4, seed=6)
    z, target = _toy_batch(N=4, seed=105)
    adaptor = PerturbationAdaptor(model, loss_fn=nmse_loss,
                                  estimator='spsa', rng_seed=0,
                                  forward_fn=custom_forward)
    adaptor.step(z, target)
    assert len(calls) == 2   # exactly the two SPSA probes
