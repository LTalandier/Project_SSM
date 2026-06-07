# tests for photonic_ssm/baselines/ridge_readout.py (salvaged from
# pnn-multilayer equalization_mrr_rc.py @ e2eec80, decoupled from the
# MRR cascade / PAM-4 framing).
"""Ridge readout + delay-embedding tests (§5.3 reservoir baseline)."""

import pytest
import torch

from photonic_ssm.baselines import (
    ReservoirReadoutBaseline,
    RidgeReadout,
    delay_embed,
)


def test_ridge_recovers_planted_linear_map():
    gen = torch.Generator().manual_seed(0)
    T, F = 400, 8
    Phi = torch.randn(T, F, generator=gen)
    w_star = torch.randn(F, generator=gen)
    y = Phi @ w_star
    r = RidgeReadout(alpha_R=1e-8)
    r.fit(Phi, y)
    assert (r.w - w_star).abs().max().item() < 1e-3
    pred = r.predict(Phi)
    mse = ((pred - y) ** 2).mean().item()
    assert mse < 1e-8
    assert r.n_params == F


def test_ridge_regularization_shrinks():
    """Larger alpha_R shrinks ||w|| — the Tikhonov property."""
    gen = torch.Generator().manual_seed(1)
    T, F = 200, 6
    Phi = torch.randn(T, F, generator=gen)
    y = Phi @ torch.randn(F, generator=gen)
    norms = []
    for alpha in (1e-6, 1.0, 100.0):
        r = RidgeReadout(alpha_R=alpha)
        r.fit(Phi, y)
        norms.append(r.w.norm().item())
    assert norms[0] > norms[1] > norms[2]


def test_delay_embed_alignment_explicit():
    """Explicit T=4, F=1 example: D=3 window centered on t with
    replicate edge padding -> rows (x_{t-1}, x_t, x_{t+1})."""
    x = torch.tensor([[0.0], [1.0], [2.0], [3.0]])
    out = delay_embed(x, delay_taps=3, add_bias=False)
    expected = torch.tensor([
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 2.0],
        [1.0, 2.0, 3.0],
        [2.0, 3.0, 3.0],
    ])
    assert torch.equal(out, expected)


def test_delay_embed_shapes_and_bias():
    gen = torch.Generator().manual_seed(2)
    x = torch.randn(50, 3, generator=gen)
    out = delay_embed(x, delay_taps=5, add_bias=True)
    assert out.shape == (50, 3 * 5 + 1)
    assert torch.equal(out[:, -1], torch.ones(50))
    out_nb = delay_embed(x, delay_taps=1, add_bias=False)
    assert torch.allclose(out_nb, x, atol=1e-7)


def test_reservoir_baseline_exploits_memory():
    """Target y_t = x_{t-1}: impossible for a memoryless readout (D=1),
    near-exact for D=3 (the lag is inside the tap window). This is the
    property that makes the baseline meaningful for the bake-off."""
    gen = torch.Generator().manual_seed(3)
    T = 500
    x = torch.randn(T, 1, generator=gen)
    y = torch.zeros(T)
    y[1:] = x[:-1, 0]          # pure one-step delay

    base_d1 = ReservoirReadoutBaseline(delay_taps=1, alpha_R=1e-6)
    base_d3 = ReservoirReadoutBaseline(delay_taps=3, alpha_R=1e-6)
    base_d1.fit(x, y)
    base_d3.fit(x, y)
    # Interior only (edge rows see replicate padding).
    sl = slice(2, T - 2)
    mse_d1 = ((base_d1.predict(x) - y)[sl] ** 2).mean().item()
    mse_d3 = ((base_d3.predict(x) - y)[sl] ** 2).mean().item()
    assert mse_d3 < 0.05 * mse_d1, (
        f"delay embedding not exploiting memory: D3 {mse_d3:.4f} "
        f"vs D1 {mse_d1:.4f}")


def test_predict_before_fit_raises():
    r = RidgeReadout()
    with pytest.raises(RuntimeError, match="fit"):
        r.predict(torch.zeros(3, 2))
