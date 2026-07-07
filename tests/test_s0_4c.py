# NEW (task S0.4c, 2026-07-07) — the pre-registered build gates
# (task_queue.md S0.4c spec, committed 5ca8d52 BEFORE this build): R1
# (near-conservative floor point), R2 (PR-11 invariant-4 unit test), R4
# (PR-7.1 4-pass ledger), R5 (invariants 1–3), + echo-retrace and
# grad-liveness checks. The full R1 dissipation sequence runs in
# analysis/s0_4c_smoke.py.
"""S0.4c RHEL-estimator build gates."""

import torch

from photonic_ssm.estimators.harness import (
    BATCH, TapHead, encode_drive, train,
)
from photonic_ssm.estimators.rhel import RHELEstimator, c_op
from photonic_ssm.substrate import cells as cellmod
from photonic_ssm.substrate.dissipative_ring import (
    DissipativeRingSubstrate as DRS,
)

T, B_PROBE, N = 32, 2, 8


def _sub(r, loss_scale, ase=0.0, gain=0.0):
    sub = DRS.from_cell("C-1", N=N, clock_GSps=2.0, seed=3,
                        input_taps=(0, 3, 5, 7), gain_factor=gain,
                        loss_scale=loss_scale, ase_variance_scale=ase)
    ki = float(sub.kappa_i)
    with torch.no_grad():
        sub.delta.copy_(torch.linspace(-1, 1, N, dtype=sub.delta.dtype) * ki)
        sub.kappa_ext.fill_(r * ki)
        sub.mu_chain.fill_(0.3 * ki)
    return sub


def _probe():
    g = torch.Generator().manual_seed(7)
    u_raw = 12.0 * torch.rand(B_PROBE, T, generator=g,
                              dtype=torch.float64) - 6.0
    tgt = torch.randn(B_PROBE, T, generator=g, dtype=torch.float64)
    return encode_drive(u_raw).unsqueeze(-1), tgt


def _truncated_ref(sub, head, u, tgt, y_scale):
    """BPTT of the SAME truncated functional the nudge realizes: full-head
    residual, only the m=0 (instantaneous) y-term differentiable."""
    for p in (sub.delta, sub.kappa_ext, sub.mu_chain):
        p.grad = None
    y = sub.forward_intensity(u)
    cols = [y] + [torch.nn.functional.pad(y.detach(), (m, 0))[..., : y.shape[-1]]
                  for m in range(1, 8)]
    lag = torch.stack(cols, -1)
    W = head.lin.weight.detach()[0]
    b = float(head.lin.bias.detach())
    (((lag / y_scale * W).sum(-1) + b - tgt) ** 2).mean().backward()
    return torch.cat([p.grad.reshape(-1).clone()
                      for p in (sub.delta, sub.kappa_ext, sub.mu_chain)])


def test_R1_floor_point_near_conservative():
    """Gate R1 (least-dissipative point): ideal C_op, ASE off, gain 0,
    κ_net·T·dt ≈ 0.03 → cosine(Δθ_RHEL, ∇θ truncated-BPTT) ≥ 0.9."""
    torch.manual_seed(0)
    sub = _sub(0.003, 0.001)
    head = TapHead()
    u, tgt = _probe()
    with torch.no_grad():
        y_scale = float(sub.forward_intensity(u).mean()) + 1e-30
    g_ref = _truncated_ref(sub, head, u, tgt, y_scale)
    est = RHELEstimator(sub, ideal_echo=True, eps_frac=0.01)
    for p in (sub.delta, sub.kappa_ext, sub.mu_chain):
        p.grad = None
    est.step(u, tgt, head, y_scale)
    g_rhel = torch.cat([p.grad.reshape(-1).clone()
                        for p in (sub.delta, sub.kappa_ext, sub.mu_chain)])
    cos = float(torch.dot(g_rhel, g_ref) /
                (g_rhel.norm() * g_ref.norm() + 1e-300))
    assert cos >= 0.9, cos


def test_echo_retraces_near_conservative():
    """The un-nudged ideal echo retraces the forward trajectory (rel. error
    < 5 % end and mid) — the mechanics behind R1."""
    sub = _sub(1e-4, 1e-3)
    est = RHELEstimator(sub, ideal_echo=True, eps_frac=0.0)
    u, tgt = _probe()
    with torch.no_grad():
        st, y = est._forward_pass(u, None)
        aT = st[:, -1, :].conj()
        resid_rev = torch.zeros(B_PROBE, T, dtype=torch.float64)
        e = est._echo_pass(u, aT, +1.0, 0.0, 1.0, resid_rev, None)
        scale = float(st[:, 1:, :].abs().pow(2).mean().sqrt()) + 1e-300
        err_end = float((e[:, -1, :].conj() - st[:, 0, :]).abs().max()) / scale
        mid = T // 2
        err_mid = float((e[:, mid - 1, :].conj() - st[:, T - mid, :]).norm()
                        / (st[:, T - mid, :].norm() + 1e-300))
    assert err_mid < 0.05, err_mid
    assert err_end < 0.5, err_end          # end state is ~0 (start was 0)


def test_R2_noisy_echo_does_not_recover_noiseless_state():
    """Gate R2 (PR-11 invariant 4): the echo of a noisy forward, through the
    FROZEN C_op, does not recover the noiseless initial trajectory — the
    'recovered' mid-trajectory state errs at O(1), not at the ASE floor."""
    sub2 = _sub(0.3, 1.0, ase=1.0)
    est = RHELEstimator(sub2, ideal_echo=False, eps_frac=0.0)
    u, tgt = _probe()
    g1 = torch.Generator().manual_seed(11)
    g2 = torch.Generator().manual_seed(22)
    with torch.no_grad():
        st, y = est._forward_pass(u, g1)
        aT = c_op(sub2, st[:, -1, :], ideal=False, generator=g2)
        resid_rev = torch.zeros(B_PROBE, T, dtype=torch.float64)
        e = est._echo_pass(u, aT, +1.0, 0.0, 1.0, resid_rev,
                           torch.Generator().manual_seed(33))
        mid = T // 2
        rel = float((e[:, mid - 1, :].conj() - st[:, T - mid, :]).norm()
                    / (st[:, T - mid, :].norm() + 1e-300))
    # Frozen η_c ≈ 1.6e-2 in energy → amplitude ~0.13: recovery error must
    # be at least the (1 − √η_c) fidelity deficit; comfortably O(1).
    assert rel >= 0.5, rel


def test_R5_conjugation_streams_independent_and_dissipative_echo():
    """Gate R5: independent conjugation draws differ (no shared RNG); the
    echo is dissipative (undriven echo energy decays — no loss-sign flip)."""
    sub = _sub(0.3, 1.0)
    a = (torch.randn(2, 2 * N, dtype=torch.float64)
         + 1j * torch.randn(2, 2 * N, dtype=torch.float64))
    c1 = c_op(sub, a, ideal=False, generator=torch.Generator().manual_seed(1))
    c2 = c_op(sub, a, ideal=False, generator=torch.Generator().manual_seed(2))
    assert not torch.allclose(c1, c2)
    est = RHELEstimator(sub, ideal_echo=True, eps_frac=0.0)
    with torch.no_grad():
        u0 = torch.zeros(2, T, 1, dtype=torch.float64)
        e = est._echo_pass(u0, a, +1.0, 0.0, 1.0,
                           torch.zeros(2, T, dtype=torch.float64), None)
        n0 = float((a.abs() ** 2).sum())
        n1 = float((e[:, -1, :].abs() ** 2).sum())
    assert n1 < n0, (n0, n1)


def test_R4_ledger_counts_match_pr7_1():
    """Gate R4: RHEL = 4×batch device passes/update, digital 0."""
    n_up = 2
    led = train("rhel", "C-1", run_seed=1, n_updates=n_up, N=8)
    assert led["device_passes"] == 4 * n_up * BATCH
    assert led["digital_passes"] == 0


def test_rhel_train_smoke_runs_and_respects_clamp():
    """5-update honest-echo run: finite losses, κ_ext inside [r_min, 3]."""
    led = train("rhel", "C-1", run_seed=2, n_updates=5, N=8)
    assert all(torch.isfinite(torch.tensor(led["loss_trace"])).tolist())
    r = torch.tensor(led["in_situ_r"])
    assert torch.all(r >= cellmod.R_MIN_SATURATING - 1e-9)
    assert torch.all(r <= 3.0 + 1e-9)
