# tests for photonic_ssm/dynamics/coupled_rings.py (NEW S0.1 core).
"""Coupled-ring N-oscillator LinOSS forward model: pole correctness, the
two architecture constraints (3a gradients-through-state, 3b full
trajectory), checkpoint equivalence, and ZOH exactness."""

import math

import torch

from photonic_ssm.dynamics import (
    CoupledRingLinOSS, from_eigenvalues, zoh_discretize, kappa_from_Q,
)

FSR_HZ = 100e9
DT = 1.0 / FSR_HZ


def _model(mu=None):
    ktot = torch.tensor([3e7, 5e7, 2e7], dtype=torch.float64)
    delta = torch.tensor([1e8, -2e8, 5e7], dtype=torch.float64)
    return CoupledRingLinOSS(ktot, delta, DT, mu=mu), ktot, delta


# ---- pole correctness (the gate) ------------------------------------- #

def test_uncoupled_poles_equal_diagonal():
    """Uncoupled (mu=None) system poles == bare ring poles
    -kappa_tot + i*delta to machine precision."""
    m, ktot, delta = _model()
    poles = m.continuous_poles()
    expect = torch.complex(-ktot, delta)
    # eigvals come unordered; match by sorting on imaginary part
    p = poles[poles.imag.argsort()]
    e = expect[expect.imag.argsort()]
    assert (p - e).abs().max().item() < 1e-3


def test_discrete_pole_magnitude_is_exp_minus_kappa_dt():
    """|z_j| = exp(-kappa_tot_j * dt): the per-step memory retention."""
    m, ktot, delta = _model()
    zmag = m.discrete_poles().abs().sort().values
    expect = torch.exp(-ktot * DT).sort().values
    assert (zmag - expect).abs().max().item() < 1e-9


def test_coupling_hybridizes_poles_but_preserves_trace():
    """Inter-ring coupling i*Omega (Omega Hermitian) hybridizes the poles
    but, being anti-Hermitian, conserves total damping: sum Re(poles) ==
    -sum kappa_tot (trace of M is unchanged by the imaginary off-diag)."""
    mu = torch.tensor([[0, 1e7, 0], [1e7, 0, 2e7], [0, 2e7, 0]],
                      dtype=torch.float64)
    m, ktot, delta = _model(mu=mu)
    poles = m.continuous_poles()
    assert abs(poles.real.sum().item() - (-ktot.sum().item())) < 1.0
    # genuinely hybridized: at least one pole's imag moved off the bare set
    bare = set(round(x, 3) for x in delta.tolist())
    moved = any(round(p, 3) not in bare for p in poles.imag.tolist())
    assert moved


def test_zoh_is_exact_for_constant_input():
    """ZOH discretization is exact for piecewise-constant input: a step
    response equals the closed-form a_ss(1 - z^k) accumulation. Check the
    single-ring fixed point a_inf == Gamma/(1-Phi) matches -B/M * u."""
    ktot = torch.tensor([4e7], dtype=torch.float64)
    delta = torch.tensor([0.0], dtype=torch.float64)
    m = CoupledRingLinOSS(ktot, delta, DT)         # B default ones (1,1)
    Phi, Gamma = zoh_discretize(m.M(), m.B, DT)
    a_inf_discrete = Gamma[0, 0] / (1.0 - Phi[0, 0])      # fixed point
    a_inf_cont = (-m.B[0, 0] / m.M()[0, 0])              # -M^{-1} B
    assert (a_inf_discrete - a_inf_cont).abs().item() < 1e-6


# ---- (3a) gradients flow through the optical state ------------------- #

def test_3a_gradient_flows_through_state_from_late_loss_to_early_input():
    """A loss at the LAST step receives gradient through the ring state
    from an input MANY steps earlier — the operational (3a) test (a loss
    at time T gets gradient through the state from input at t << T)."""
    mu = torch.tensor([[0, 1e7, 0], [1e7, 0, 2e7], [0, 2e7, 0]],
                      dtype=torch.float64)
    m, _, _ = _model(mu=mu)
    T = 50
    u = torch.randn(T, 1, dtype=torch.float64, requires_grad=True)
    _, out = m(u)
    loss = (out[-1].abs() ** 2).sum()              # depends only on x_T
    loss.backward()
    g = u.grad.abs().squeeze(-1)
    assert torch.isfinite(g).all()
    assert g[0].item() > 0.0                        # reaches t=0 (49 back)
    # and into every recurrent parameter
    for p in m.parameters():
        assert p.grad is not None and torch.isfinite(p.grad).all()


def test_3a_no_detach_in_rollout_source():
    """Guard against the salvaged forward-only anti-pattern leaking in:
    the dynamical rollout must not call no_grad/detach."""
    import inspect

    from photonic_ssm.dynamics import coupled_rings
    src = inspect.getsource(coupled_rings.CoupledRingLinOSS._rollout)
    src += inspect.getsource(
        coupled_rings.CoupledRingLinOSS._rollout_checkpointed)
    # check for the actual anti-pattern CALLS, not the words in the
    # docstring that documents their absence.
    assert "torch.no_grad(" not in src and ".detach()" not in src
    assert ".data" not in src


# ---- (3b) full state trajectory exposed ------------------------------ #

def test_3b_full_trajectory_exposed():
    """forward returns x_0..x_T (T+1 states incl. the initial), the
    contract the adjoint/RHEL/reservoir-readout consume."""
    m, _, _ = _model()
    T = 30
    u = torch.randn(T, 1, dtype=torch.float64)
    states, out = m(u)
    assert states.shape == (T + 1, m.N)             # includes x_0
    assert out.shape == (T, m.N)                     # C = I default
    # x_0 is the (zero) initial state; x_1.. evolve
    assert states[0].abs().max().item() == 0.0


def test_batched_rollout_shapes():
    m, _, _ = _model()
    T = 20
    ub = torch.randn(7, T, 1, dtype=torch.float64)
    states, out = m(ub)
    assert states.shape == (7, T + 1, m.N) and out.shape == (7, T, m.N)


# ---- checkpoint == plain (value AND gradient) ------------------------ #

def test_checkpointed_rollout_matches_plain_value_and_grad():
    """The gradient-checkpointed chunked rollout (the
    TrainingAwareDynamicSOAPerMode memory pattern) is bit-equivalent to
    the plain autograd rollout in outputs, states, and all gradients."""
    mu = torch.tensor([[0, 1e7, 0], [1e7, 0, 2e7], [0, 2e7, 0]],
                      dtype=torch.float64)
    T = 40
    u = torch.randn(T, 1, dtype=torch.float64)

    m, _, _ = _model(mu=mu)
    sA, oA = m(u)
    (oA.abs() ** 2).sum().backward()
    gA = {n: p.grad.clone() for n, p in m.named_parameters()}

    m.zero_grad()
    sB, oB = m(u, checkpoint_chunk=7)
    (oB.abs() ** 2).sum().backward()
    gB = {n: p.grad.clone() for n, p in m.named_parameters()}

    assert (sA - sB).abs().max().item() == 0.0
    assert (oA - oB).abs().max().item() == 0.0
    for n in gA:
        assert (gA[n] - gB[n]).abs().max().item() == 0.0


# ---- eigenvalue-form constructor ------------------------------------- #

def test_from_eigenvalues_matches_physical():
    """from_eigenvalues(alpha, beta) builds kappa_tot=exp(alpha),
    delta=beta — the a_i = -exp(alpha_i) + i*beta_i parametrization."""
    alpha = torch.tensor([math.log(3e7), math.log(5e7)], dtype=torch.float64)
    beta = torch.tensor([1e8, -2e8], dtype=torch.float64)
    m = from_eigenvalues(alpha, beta, DT)
    a, b = m.alpha_beta()
    assert (a - alpha).abs().max().item() < 1e-9
    assert (b - beta).abs().max().item() < 1e-3
    assert (m.kappa_tot - torch.tensor([3e7, 5e7], dtype=torch.float64)
            ).abs().max().item() < 1.0


def test_rejects_nondissipative_kappa():
    """kappa_tot <= 0 is rejected (the -exp(alpha) parametrization needs a
    damped pole)."""
    import pytest
    with pytest.raises(ValueError):
        CoupledRingLinOSS(torch.tensor([0.0]), torch.tensor([0.0]), DT)
