# NEW (task S0.4b, 2026-07-07) — the pre-registered build gates
# (task_queue.md S0.4b spec, committed c85fe62 BEFORE this build): B1
# (fixed-gain noiseless adjoint ≡ BPTT), B4 (PR-7 1+1 ledger), B5
# (detach_gain value invariance), + saturating-channel and fresh-ASE
# liveness checks.
"""S0.4b adjoint-estimator build gates."""

import torch

from photonic_ssm.estimators.adjoint import AdjointEstimator
from photonic_ssm.estimators.harness import (
    BATCH, TapHead, encode_drive, make_substrate, mse_loss, train,
)
from photonic_ssm.substrate import cells as cellmod


def _noiseless_sub(N=8, gain_mode=None):
    sub = make_substrate("C-1", seed=3, N=N)
    sub.ase_variance_scale = 0.0
    if gain_mode is not None:
        sub.gain_mode = gain_mode
    return sub


def _probe_u(batch=2, T=64, seed=5):
    g = torch.Generator().manual_seed(seed)
    u_raw = 12.0 * torch.rand(batch, T, generator=g,
                              dtype=torch.float64) - 6.0
    return encode_drive(u_raw).unsqueeze(-1)


def _flat_grads(sub):
    return torch.cat([p.grad.reshape(-1).clone()
                      for p in (sub.delta, sub.kappa_ext, sub.mu_chain)])


def _adjoint_and_bptt_grads(sub):
    u = _probe_u()
    target = torch.zeros(u.shape[0], u.shape[1], dtype=torch.float64)
    head = TapHead()
    y_scale = 1e6

    est = AdjointEstimator(sub)
    est.step(u, lambda y: mse_loss(head(y / y_scale), target))
    g_adj = _flat_grads(sub)

    for p in (sub.delta, sub.kappa_ext, sub.mu_chain):
        p.grad = None
    for p in head.parameters():
        p.grad = None
    y = sub.forward_intensity(u)
    mse_loss(head(y / y_scale), target).backward()
    return g_adj, _flat_grads(sub)


def test_B1_fixed_gain_noiseless_adjoint_equals_bptt():
    """Gate B1 (the roadmap S0.4 floor check): on the fixed-gain plane with
    ASE off, the adjoint gradient IS the BPTT gradient — cosine ≥ 1−1e-9,
    allclose rtol 1e-8 (same computation by construction in this limit)."""
    g_adj, g_bptt = _adjoint_and_bptt_grads(_noiseless_sub(gain_mode="fixed"))
    cos = torch.dot(g_adj, g_bptt) / (g_adj.norm() * g_bptt.norm())
    assert float(cos) >= 1.0 - 1e-9, float(cos)
    assert torch.allclose(g_adj, g_bptt, rtol=1e-8), \
        (g_adj - g_bptt).abs().max()


def test_saturating_noiseless_adjoint_drops_gain_channel():
    """In saturating mode the frozen-gain adjoint must DIFFER from full BPTT
    on the κ_ext block (detach_gain is live, the ∂g/∂κ_ext channel dropped)
    while remaining finite and nonzero."""
    g_adj, g_bptt = _adjoint_and_bptt_grads(_noiseless_sub())
    assert torch.isfinite(g_adj).all() and g_adj.abs().sum() > 0
    n = 8
    # Purely relative comparison (atol=0): these grads are ~1e-8 in absolute
    # scale, and the dropped channel shifts them by ~10-30 % relative.
    assert not torch.allclose(g_adj[n:2 * n], g_bptt[n:2 * n],
                              rtol=1e-3, atol=0.0)
    # δ / μ blocks see the same frozen-gain dynamics matrix values, but the
    # dropped channel only touches κ_ext paths; δ-block stays close.
    cos = torch.dot(g_adj, g_bptt) / (g_adj.norm() * g_bptt.norm())
    assert float(cos) > 0.0        # sanity; the ≥0.9 expectation is B2 (report)


def test_B5_detach_gain_forward_values_bit_identical():
    """Gate B5: detach_gain changes NO forward value (grads only)."""
    sub = make_substrate("C-1", seed=7, N=8)
    u = _probe_u(seed=11)
    with torch.no_grad():
        y0 = sub.forward_intensity(
            u, generator=torch.Generator().manual_seed(42))
        sub.detach_gain = True
        y1 = sub.forward_intensity(
            u, generator=torch.Generator().manual_seed(42))
        sub.detach_gain = False
    assert torch.equal(y0, y1)


def test_fresh_ase_makes_adjoint_gradient_noisy():
    """With ASE on and distinct fwd/adj generators, the adjoint gradient
    differs from the same-realization BPTT gradient (the fresh-noise path is
    live) — deterministic given the fixed seeds."""
    sub = make_substrate("C-1", seed=3, N=8)          # ASE ON
    u = _probe_u()
    target = torch.zeros(u.shape[0], u.shape[1], dtype=torch.float64)
    head = TapHead()
    y_scale = 1e6

    est = AdjointEstimator(sub)
    est.step(u, lambda y: mse_loss(head(y / y_scale), target),
             gen_fwd=torch.Generator().manual_seed(1),
             gen_adj=torch.Generator().manual_seed(2))
    g_adj = _flat_grads(sub)

    for p in (sub.delta, sub.kappa_ext, sub.mu_chain):
        p.grad = None
    for p in head.parameters():
        p.grad = None
    y = sub.forward_intensity(u, generator=torch.Generator().manual_seed(1))
    mse_loss(head(y / y_scale), target).backward()
    g_bptt = _flat_grads(sub)

    assert torch.isfinite(g_adj).all()
    assert not torch.allclose(g_adj, g_bptt, rtol=1e-3, atol=0.0)


def test_B4_ledger_counts_match_pr7():
    """Gate B4: adjoint = 2×batch device passes/update, digital = 0."""
    n_up = 3
    led = train("adjoint", "C-1", run_seed=1, n_updates=n_up, N=8)
    assert led["device_passes"] == 2 * n_up * BATCH
    assert led["digital_passes"] == 0


def test_adjoint_train_smoke_runs_and_respects_clamp():
    """25-update adjoint run: finite losses, κ_ext inside [r_min, 3]."""
    led = train("adjoint", "C-1", run_seed=2, n_updates=25, N=8)
    assert all(torch.isfinite(torch.tensor(led["loss_trace"])).tolist())
    r = torch.tensor(led["in_situ_r"])
    assert torch.all(r >= cellmod.R_MIN_SATURATING - 1e-9)
    assert torch.all(r <= 3.0 + 1e-9)
    assert led["ser_final"] is not None
