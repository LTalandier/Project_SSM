# tests for photonic_ssm/dynamic_gain.py (salvaged from pnn-multilayer
# channels/dynamic_soa.py @ e2eec80). The gradient-flow tests are the
# S0.0 verification of ARCHITECTURE CONSTRAINT (3a): gradients must flow
# through the optical state — the checkpointed-unroll class is the
# reference pattern for all S0.1+ substrate dynamics.
"""Rate-equation gain tests: steady state, eval/training consistency,
gradient flow (constraint 3a), checkpointing equivalence."""

import math

import pytest
import torch

from photonic_ssm.dynamic_gain import (
    DynamicSOA,
    DynamicSOAPerMode,
    TrainingAwareDynamicSOAPerMode,
    build_matched_dynamic_soa_per_mode,
)


TAU_C = 200e-12
DT = 1.0 / 32e9          # ~31 ps step; dt/tau_c ~ 0.16


def _const_power_input(n_syms, N, amplitude):
    return torch.full((n_syms, N), amplitude, dtype=torch.complex128)


# ---------------------------------------------------------------------- #
#  Steady state
# ---------------------------------------------------------------------- #

def test_steady_state_power_gain_limits():
    """Newton steady state: G(0) = G0 exactly; at P > 0 the solution
    satisfies the transcendental equation h0 - h = (P/P_sat)(e^h - 1)."""
    soa = DynamicSOA(tau_c=TAU_C, G0_dB=20.0, P_sat_mW=10.0)
    assert soa.steady_state_power_gain(0.0) == pytest.approx(soa.G0_power)

    P = 5e-3  # 5 mW
    G = soa.steady_state_power_gain(P)
    h = math.log(G)
    K = P / soa.P_sat_W
    residual = soa.h0 - h - K * (math.exp(h) - 1.0)
    assert abs(residual) < 1e-9
    assert 1.0 < G < soa.G0_power  # saturated below small-signal gain


def test_cw_input_holds_steady_state_gain():
    """Constant-power sequence: h is initialized at the steady state for
    that power, so every output symbol carries exactly the steady-state
    field gain exp(h_ss/2)."""
    N, T = 4, 64
    amp = 0.05  # |z|^2 = 2.5e-3 "W"
    G_field = torch.full((N,), 3.0, dtype=torch.float64)
    alpha = torch.full((N,), 0.4, dtype=torch.float64)
    z = _const_power_input(T, N, amp)

    dyn = DynamicSOAPerMode(G_field=G_field, alpha=alpha, tau_c=TAU_C)
    h_ss = dyn._steady_state_h(torch.full((N,), amp * amp,
                                          dtype=torch.float64))
    expected_gain = torch.exp(h_ss / 2.0)

    out = dyn.apply(z, dt=DT)
    measured_gain = (out.abs() / amp)
    err = (measured_gain - expected_gain).abs().max().item()
    assert err < 1e-9, f"CW gain deviates from steady state by {err:.3e}"


def test_training_aware_matches_eval_class():
    """The autograd-enabled class integrates the same ODE as the
    forward-only eval class: identical outputs on the same sequence
    (same params, same substeps), to float64 round-off."""
    torch.manual_seed(0)
    N, T = 3, 48
    G_field = torch.tensor([2.0, 3.0, 1.5], dtype=torch.float64)
    alpha = torch.tensor([0.3, 0.1, 0.5], dtype=torch.float64)
    z = (0.05 * (torch.randn(T, N, dtype=torch.float64)
                 + 1j * torch.randn(T, N, dtype=torch.float64))
         ).to(torch.complex128)

    eval_soa = DynamicSOAPerMode(G_field=G_field, alpha=alpha, tau_c=TAU_C)
    out_eval = eval_soa.apply(z, dt=DT)

    train_soa = TrainingAwareDynamicSOAPerMode(tau_c=TAU_C, chunk_size=16)
    out_train = train_soa(z, G_field, alpha, dt=DT)

    err = (out_eval - out_train).abs().max().item()
    assert err < 1e-10, f"training-aware vs eval mismatch {err:.3e}"


def test_matched_factory_zero_power_gain():
    """build_matched_dynamic_soa_per_mode: at vanishing power the field
    gain is G_field (power gain G_field^2) — the matching contract."""
    N = 4
    G_field = torch.tensor([1.5, 2.0, 2.5, 3.0], dtype=torch.float64)
    alpha = torch.full((N,), 0.2, dtype=torch.float64)
    dyn = build_matched_dynamic_soa_per_mode(G_field, alpha, tau_c=TAU_C)
    z = _const_power_input(32, N, 1e-7)
    out = dyn.apply(z, dt=DT)
    gain = (out.abs() / 1e-7)
    assert torch.allclose(gain, G_field.unsqueeze(0).expand_as(gain),
                          rtol=1e-6)


# ---------------------------------------------------------------------- #
#  Constraint (3a): gradients flow through the optical state
# ---------------------------------------------------------------------- #

def test_gradient_flows_through_state_and_params():
    """Loss on the LAST output symbol must receive gradient from EARLIER
    input symbols via the carrier memory h(t) — the defining property
    the substrate needs (BPTT/PAT/adjoint all differentiate through
    state). Also: gradients reach (G_field, alpha)."""
    N, T = 2, 32
    tau_c = 10 * DT  # memory ~ 10 symbols
    torch.manual_seed(1)
    z = (0.1 * (torch.randn(T, N, dtype=torch.float64)
                + 1j * torch.randn(T, N, dtype=torch.float64))
         ).to(torch.complex128).requires_grad_(True)
    G_field = torch.tensor([2.0, 2.5], dtype=torch.float64,
                           requires_grad=True)
    alpha = torch.tensor([0.3, 0.2], dtype=torch.float64,
                         requires_grad=True)

    dyn = TrainingAwareDynamicSOAPerMode(tau_c=tau_c, chunk_size=8)
    out = dyn(z, G_field, alpha, dt=DT)
    loss = out[-1].abs().pow(2).sum()   # depends on z[<T-1] only via h
    loss.backward()

    assert z.grad is not None
    assert torch.isfinite(z.grad).all()
    # Direct dependence on the last symbol:
    assert z.grad[-1].abs().max().item() > 0
    # THE constraint-(3a) check — gradient through the state memory
    # (symbol T-5 is within ~tau_c of the loss symbol):
    assert z.grad[T - 5].abs().max().item() > 0, (
        "no gradient through the carrier state — the no_grad/detach "
        "anti-pattern would produce exactly this failure")
    assert G_field.grad is not None and G_field.grad.abs().min().item() > 0
    assert alpha.grad is not None and torch.isfinite(alpha.grad).all()


def test_checkpointed_equals_noncheckpointed_outputs_and_grads():
    """use_checkpoint=True must change memory behavior only: outputs and
    gradients identical to the non-checkpointed rollout."""
    N, T = 2, 40
    torch.manual_seed(2)
    z_base = (0.08 * (torch.randn(T, N, dtype=torch.float64)
                      + 1j * torch.randn(T, N, dtype=torch.float64))
              ).to(torch.complex128)

    results = {}
    for use_cp in (True, False):
        z = z_base.clone().requires_grad_(True)
        G_field = torch.tensor([2.0, 3.0], dtype=torch.float64,
                               requires_grad=True)
        alpha = torch.tensor([0.25, 0.15], dtype=torch.float64,
                             requires_grad=True)
        dyn = TrainingAwareDynamicSOAPerMode(
            tau_c=TAU_C, chunk_size=8, use_checkpoint=use_cp)
        out = dyn(z, G_field, alpha, dt=DT)
        loss = out.abs().pow(2).sum()
        loss.backward()
        results[use_cp] = (out.detach(), z.grad.clone(),
                           G_field.grad.clone(), alpha.grad.clone())

    for a, b in zip(results[True], results[False]):
        assert (a - b).abs().max().item() < 1e-10


def test_warmup_symbols_shape_and_validation():
    N, T, W = 3, 24, 8
    z = _const_power_input(T, N, 0.05)
    G_field = torch.full((N,), 2.0, dtype=torch.float64)
    alpha = torch.full((N,), 0.2, dtype=torch.float64)
    dyn = TrainingAwareDynamicSOAPerMode(tau_c=TAU_C, chunk_size=5)
    out = dyn(z, G_field, alpha, dt=DT, warmup_symbols=W)
    assert out.shape == (T - W, N)
    with pytest.raises(ValueError):
        dyn(z, G_field, alpha, dt=DT, warmup_symbols=T)


def test_forward_only_classes_do_not_build_graph():
    """The eval-only classes are documented forward-only: their output
    must NOT carry autograd history (this is what makes them unusable
    inside the substrate training path — by design, not by accident)."""
    N, T = 2, 16
    z = _const_power_input(T, N, 0.05).requires_grad_(True)
    dyn = DynamicSOAPerMode(
        G_field=torch.full((N,), 2.0, dtype=torch.float64),
        alpha=torch.full((N,), 0.2, dtype=torch.float64), tau_c=TAU_C)
    out = dyn.apply(z, dt=DT)
    assert not out.requires_grad
