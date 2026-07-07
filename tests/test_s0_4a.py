# NEW (task S0.4a phase 1, 2026-07-07) — the pre-registered build gates
# (task_queue.md S0.4a spec): S1 (perfect-twin PAT ≡ BPTT gradient), S3
# (PR-7 ledger counts), + mismatch-family sanity and a tiny train smoke.
"""S0.4a estimator-build gates."""

import torch

from photonic_ssm.estimators.harness import (
    BATCH, TapHead, encode_drive, fresh_batch, make_substrate, mse_loss,
    taps_for_N, train,
)
from photonic_ssm.estimators.pat import FAMILIES, PATEstimator, build_twin
from photonic_ssm.substrate import cells as cellmod
from photonic_ssm.substrate.dissipative_ring import (
    DissipativeRingSubstrate as DRS,
)


def _noiseless_sub(N=8):
    sub = make_substrate("C-1", seed=3, N=N)
    sub.ase_variance_scale = 0.0
    return sub


def _probe_u(batch=2, T=64, seed=5):
    g = torch.Generator().manual_seed(seed)
    u_raw = 12.0 * torch.rand(batch, T, generator=g,
                              dtype=torch.float64) - 6.0
    return encode_drive(u_raw).unsqueeze(-1)


def _flat_grads(sub):
    return torch.cat([p.grad.reshape(-1).clone()
                      for p in (sub.delta, sub.kappa_ext, sub.mu_chain)])


def test_S1_perfect_twin_pat_equals_bptt_gradient():
    """Gate S1: on a noiseless probe the perfect-twin PAT gradient is the
    BPTT-through-substrate gradient (same computation) — cosine ≥ 1−1e-9."""
    sub = _noiseless_sub()
    u = _probe_u()
    target = torch.zeros(u.shape[0], u.shape[1], dtype=torch.float64)
    head = TapHead()
    y_scale = 1e6

    est = PATEstimator(sub, "perfect")
    est.step(u, lambda y: mse_loss(head(y / y_scale), target))
    g_pat = _flat_grads(sub)

    for p in (sub.delta, sub.kappa_ext, sub.mu_chain):
        p.grad = None
    y = sub.forward_intensity(u)
    mse_loss(head(y / y_scale), target).backward()
    g_bptt = _flat_grads(sub)

    cos = torch.dot(g_pat, g_bptt) / (g_pat.norm() * g_bptt.norm())
    assert float(cos) >= 1.0 - 1e-9, float(cos)
    assert torch.allclose(g_pat, g_bptt, rtol=1e-8), \
        (g_pat - g_bptt).abs().max()


def test_mismatch_families_alter_but_do_not_break_gradients():
    """M-par / M-struct / both give finite, nonzero gradients that differ
    from the perfect twin's (the mismatch is live)."""
    u = _probe_u()
    target = torch.zeros(u.shape[0], u.shape[1], dtype=torch.float64)
    y_scale = 1e6
    grads = {}
    for fam in FAMILIES:
        sub = _noiseless_sub()
        head = TapHead()
        torch.manual_seed(0)
        est = PATEstimator(sub, fam)
        est.step(u, lambda y: mse_loss(head(y / y_scale), target))
        grads[fam] = _flat_grads(sub)
        assert torch.isfinite(grads[fam]).all(), fam
        assert grads[fam].abs().sum() > 0, fam
    for fam in ("M-par", "M-struct", "both"):
        assert not torch.allclose(grads[fam], grads["perfect"]), fam
    # M-struct kills the gain channel: its κ_ext-grad differs from perfect's.
    n = 8
    assert not torch.allclose(grads["M-struct"][n:2 * n],
                              grads["perfect"][n:2 * n])


def test_S3_ledger_counts_match_pr7():
    """Gate S3: device/digital pass counts per the PR-7 table."""
    n_up = 3
    led_pat = train("pat-both", "C-1", run_seed=1, n_updates=n_up, N=8)
    assert led_pat["device_passes"] == n_up * BATCH
    assert led_pat["digital_passes"] == 2 * n_up * BATCH
    led_spsa = train("spsa", "C-1", run_seed=1, n_updates=n_up, N=8)
    assert led_spsa["device_passes"] == 2 * n_up * BATCH
    assert led_spsa["digital_passes"] == 0
    led_bptt = train("bptt", "C-1", run_seed=1, n_updates=n_up, N=8)
    assert led_bptt["device_passes"] == 0
    assert led_bptt["digital_passes"] == 2 * n_up * BATCH


def test_train_smoke_runs_and_respects_clamp():
    """25-update PAT-perfect run: finite losses, in-situ params moved, κ_ext
    inside the operative band [r_min, 3] (S0.4-0 clamp)."""
    led = train("pat-perfect", "C-1", run_seed=2, n_updates=25, N=8)
    assert all(torch.isfinite(torch.tensor(led["loss_trace"])).tolist())
    r = torch.tensor(led["in_situ_r"])
    assert torch.all(r >= cellmod.R_MIN_SATURATING - 1e-9)
    assert torch.all(r <= 3.0 + 1e-9)
    assert led["ser_final"] is not None


def test_taps_for_N_proportional_rule():
    assert taps_for_N(32) == (2, 11, 20, 29)
    t8 = taps_for_N(8)
    assert len(t8) >= 2 and min(t8) >= 0 and max(t8) <= 7


def test_twin_shares_command_parameters():
    """bind_command routes twin gradients to the substrate's parameters."""
    sub = _noiseless_sub()
    twin = build_twin(sub, "M-par")
    from photonic_ssm.estimators.pat import bind_command
    bind_command(twin, sub)
    y = twin.forward_intensity(_probe_u())
    y.mean().backward()
    assert sub.delta.grad is not None and sub.delta.grad.abs().sum() > 0
    assert sub.kappa_ext.grad is not None
    assert sub.mu_chain.grad is not None
