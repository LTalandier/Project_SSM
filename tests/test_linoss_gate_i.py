"""S0.2-1 unit tests: the in-house layer + Gate-i stack.

Covers (PR-1 integrity items):
  * scan correctness: assoc_scan_2x2 / assoc_scan_diag vs sequential refs;
  * the published LinOSS-IM recurrence reproduced step-by-step (hand unroll);
  * D-08-2 made computational: ComplexDiagSSM.from_linoss_im forward parity
    with LinOSSIMLayer (A > 0), + the Jordan guard at A == 0;
  * mu hook: mu = 0 reduces to the diagonal scan; mu != 0 changes outputs
    (the hook is real) and the sequential reference is exercised;
  * EMABatchNorm: equinox-0.11.4 semantics (first-call copy, EMA mixing,
    normalization by UPDATED running stats, inference path, biased var);
  * shared dropout: mask shared across batch, off in eval;
  * param counts: G1/G3 configs vs published 10,936 / 134,279 under the
    published counting convention (trainable + BN state buffers).
"""

import math

import pytest
import torch

from photonic_ssm.linoss.layer import (
    ComplexDiagSSM,
    LinOSSIMLayer,
    assoc_scan_2x2,
    assoc_scan_diag,
)
from photonic_ssm.linoss.stack import EMABatchNorm, GateIClassifier, _shared_dropout

TOL = dict(rtol=1e-4, atol=1e-5)


def _sequential_2x2(A, b):
    L = A.shape[0]
    x = torch.zeros_like(b[..., 0, :, :])
    out = []
    for k in range(L):
        iA, iB, iC, iD = A[k].unbind(dim=-2)
        x1, x2 = x.unbind(dim=-2)
        x = torch.stack((iA * x1 + iB * x2, iC * x1 + iD * x2), dim=-2) + b[..., k, :, :]
        out.append(x)
    return torch.stack(out, dim=-3)


def test_assoc_scan_2x2_matches_sequential():
    g = torch.Generator().manual_seed(0)
    L, m, batch = 37, 3, 2  # odd, non-power-of-two length
    A = torch.randn(L, 4, m, generator=g) * 0.4
    b = torch.randn(batch, L, 2, m, generator=g)
    torch.testing.assert_close(assoc_scan_2x2(A, b), _sequential_2x2(A, b), **TOL)


def test_assoc_scan_diag_matches_sequential():
    g = torch.Generator().manual_seed(1)
    L, m, batch = 33, 4, 2
    lam = 0.95 * torch.exp(1j * torch.rand(m, generator=g) * 3.0)
    lam_re = lam.real.unsqueeze(0).expand(L, m).contiguous()
    lam_im = lam.imag.unsqueeze(0).expand(L, m).contiguous()
    b_re = torch.randn(batch, L, m, generator=g)
    b_im = torch.randn(batch, L, m, generator=g)
    a_re, a_im = assoc_scan_diag(lam_re, lam_im, b_re, b_im)
    s = torch.zeros(batch, m, dtype=torch.complex64)
    ref_re, ref_im = [], []
    for k in range(L):
        s = lam * s + torch.complex(b_re[:, k], b_im[:, k])
        ref_re.append(s.real)
        ref_im.append(s.imag)
    torch.testing.assert_close(a_re, torch.stack(ref_re, dim=1), **TOL)
    torch.testing.assert_close(a_im, torch.stack(ref_im, dim=1), **TOL)


def test_const_scan_forward_matches_generic_and_layer_paths_agree():
    from photonic_ssm.linoss.layer import _ConstScan2x2

    g = torch.Generator().manual_seed(10)
    L, m = 100, 5
    M = torch.randn(4, m, generator=g) * 0.4
    F = torch.randn(2, 3, L, 2, m, generator=g)
    A_el = M.unsqueeze(0).expand(L, 4, m)
    torch.testing.assert_close(_ConstScan2x2.apply(M, F), assoc_scan_2x2(A_el, F), **TOL)
    # full layer: fast path == generic path, values and gradients
    layer_f = LinOSSIMLayer(6, 4, generator=torch.Generator().manual_seed(11))
    layer_g = LinOSSIMLayer(6, 4, generator=torch.Generator().manual_seed(11),
                            use_generic_scan=True)
    u = torch.randn(2, 57, 4, generator=g)
    out_f, out_g = layer_f(u), layer_g(u)
    torch.testing.assert_close(out_f, out_g, **TOL)
    out_f.square().mean().backward()
    out_g.square().mean().backward()
    for (n1, p1), (n2, p2) in zip(layer_f.named_parameters(), layer_g.named_parameters()):
        torch.testing.assert_close(p1.grad, p2.grad, rtol=1e-3, atol=1e-5)


def test_const_scan_gradients_vs_autograd_float64():
    """Analytic backward (reverse scan + outer-product reduction) checked
    against autograd through the generic scan in float64."""
    from photonic_ssm.linoss.layer import _ConstScan2x2

    g = torch.Generator().manual_seed(12)
    L, m = 23, 3
    M0 = (torch.randn(4, m, generator=g) * 0.4).double()
    F0 = torch.randn(2, L, 2, m, generator=g).double()
    w = torch.randn(2, L, 2, m, generator=g).double()  # fixed projection

    M1, F1 = M0.clone().requires_grad_(), F0.clone().requires_grad_()
    (_ConstScan2x2.apply(M1, F1) * w).sum().backward()
    M2, F2 = M0.clone().requires_grad_(), F0.clone().requires_grad_()
    A_el = M2.unsqueeze(0).expand(L, 4, m)
    (assoc_scan_2x2(A_el, F2) * w).sum().backward()
    torch.testing.assert_close(M1.grad, M2.grad, rtol=1e-9, atol=1e-9)
    torch.testing.assert_close(F1.grad, F2.grad, rtol=1e-9, atol=1e-9)


def test_linoss_im_layer_matches_hand_unroll():
    """The layer output equals the published recurrence unrolled by hand:
    z_k = z_{k-1} + dt*(-A y_k + Bu_k) solved implicitly, y_k = y_{k-1} + dt z_k,
    out = Re(C (z,y)_y) + D*u  — i.e. the official M_IM / F construction."""
    g = torch.Generator().manual_seed(2)
    m, H, L, batch = 5, 4, 23, 3
    layer = LinOSSIMLayer(m, H, generator=g)
    u = torch.randn(batch, L, H, generator=g)
    out = layer(u)

    with torch.no_grad():
        A = torch.relu(layer.A_diag)
        dt = torch.sigmoid(layer.steps)
        Bc = torch.complex(layer.B[..., 0], layer.B[..., 1])
        Cc = torch.complex(layer.C[..., 0], layer.C[..., 1])
        z = torch.zeros(batch, m, dtype=torch.complex64)
        y = torch.zeros(batch, m, dtype=torch.complex64)
        outs = []
        S = 1.0 + dt**2 * A
        for k in range(L):
            Bu = u[:, k].to(torch.complex64) @ Bc.T
            z = (z - dt * A * y + dt * Bu) / S
            y = y + dt * z
            outs.append((y @ Cc.T).real + layer.D * u[:, k])
        ref = torch.stack(outs, dim=1)
    torch.testing.assert_close(out, ref, **TOL)


def test_d082_equivalence_complex_diag_realizes_linoss_im():
    """D-08-2: LinOSS-IM == uncoupled conjugate-pair special case of the
    complex-diagonal class — exact forward parity via from_linoss_im."""
    g = torch.Generator().manual_seed(3)
    m, H, L, batch = 8, 6, 64, 2
    layer = LinOSSIMLayer(m, H, generator=g)
    with torch.no_grad():
        layer.A_diag.clamp_(min=0.05)  # strictly inside the diagonalizable region
    eq = ComplexDiagSSM.from_linoss_im(layer)
    u = torch.randn(batch, L, H, generator=g)
    torch.testing.assert_close(eq(u), layer(u), **TOL)


def test_from_linoss_im_raises_on_jordan_boundary():
    g = torch.Generator().manual_seed(4)
    layer = LinOSSIMLayer(4, 3, generator=g)
    with torch.no_grad():
        layer.A_diag[1] = -0.3  # relu -> exactly 0: Jordan cell
    with pytest.raises(ValueError, match="Jordan"):
        ComplexDiagSSM.from_linoss_im(layer)


def test_mu_hook_off_is_diagonal_and_on_changes_output():
    g = torch.Generator().manual_seed(5)
    m, H, L, batch = 6, 5, 40, 2
    ssm = ComplexDiagSSM(m, H, generator=g)
    u = torch.randn(batch, L, H, generator=g)
    out0 = ssm(u)
    # mu = 0: parallel diagonal scan must equal the sequential coupled path.
    lam_re, lam_im = ssm.lam[:, 0], ssm.lam[:, 1]
    bu_re = u @ ssm.W_in[..., 0].T
    bu_im = u @ ssm.W_in[..., 1].T
    with torch.no_grad():
        a_re, a_im = ssm._sequential_coupled(bu_re, bu_im, lam_re, lam_im)
        ref = a_re @ ssm.W_out[..., 0].T - a_im @ ssm.W_out[..., 1].T + ssm.D * u
    torch.testing.assert_close(out0, ref, **TOL)
    with torch.no_grad():
        ssm.mu[:, 0] = 0.05
    assert not torch.allclose(ssm(u), out0, rtol=1e-3, atol=1e-4)


def test_ema_batchnorm_equinox_semantics():
    bn = EMABatchNorm(3)
    bn.train()
    g = torch.Generator().manual_seed(6)
    x1 = torch.randn(4, 7, 3, generator=g) * 2.0 + 1.0
    m1 = x1.mean(dim=(0, 1))
    v1 = ((x1 - m1) ** 2).mean(dim=(0, 1))  # biased, global-mean
    y1 = bn(x1)
    torch.testing.assert_close(bn.running_mean, m1, **TOL)  # first call: copy
    torch.testing.assert_close(y1, (x1 - m1) / torch.sqrt(v1 + 1e-5), **TOL)

    x2 = torch.randn(4, 7, 3, generator=g) * 0.5 - 2.0
    m2 = x2.mean(dim=(0, 1))
    v2 = ((x2 - m2) ** 2).mean(dim=(0, 1))
    y2 = bn(x2)
    rm = 0.01 * m2 + 0.99 * m1
    rv = 0.01 * v2 + 0.99 * v1
    torch.testing.assert_close(bn.running_mean, rm, **TOL)
    # normalization uses the UPDATED running stats, not the batch stats
    torch.testing.assert_close(y2, (x2 - rm) / torch.sqrt(rv + 1e-5), **TOL)

    bn.eval()
    x3 = torch.randn(2, 7, 3, generator=g)
    torch.testing.assert_close(bn(x3), (x3 - rm) / torch.sqrt(rv + 1e-5), **TOL)
    torch.testing.assert_close(bn.running_mean, rm, **TOL)  # eval: no update


def test_shared_dropout_mask_is_batch_shared():
    g = torch.Generator().manual_seed(7)
    x = torch.ones(8, 50, 10)
    y = _shared_dropout(x, 0.5, True, g)
    assert not torch.allclose(y, x)
    for b in range(1, 8):  # identical mask across the batch
        torch.testing.assert_close(y[b], y[0])
    assert _shared_dropout(x, 0.5, False, g) is x


def test_param_counts_match_published_convention():
    g = torch.Generator().manual_seed(8)
    # G1 Heartbeat: data_dim 61+1, hidden 16, state 16, blocks 6, classes 2
    g1 = GateIClassifier(6, 62, 16, 16, 2, generator=g)
    trainable, published = g1.param_counts()
    assert trainable == 10_738
    assert published == 10_936  # = trainable + 6*(2*16+1) BN state arrays
    # G3 EigenWorms: data_dim 6+1, hidden 128, state 64, blocks 2, classes 5
    g3 = GateIClassifier(2, 7, 64, 128, 5, generator=g)
    trainable, published = g3.param_counts()
    assert trainable == 133_765
    assert published == 134_279  # = trainable + 2*(2*128+1)


def test_gradients_flow_through_scan_state():
    """House constraint 3a: d(loss)/d(params) nonzero through the full scan."""
    g = torch.Generator().manual_seed(9)
    model = GateIClassifier(2, 5, 4, 8, 3, generator=g)
    x = torch.randn(3, 30, 5, generator=g)
    p = model(x, dropout_generator=g)
    loss = -(torch.log(p + 1e-8)[:, 0]).mean()
    loss.backward()
    for name, param in model.named_parameters():
        assert param.grad is not None, name
    a_grad = model.blocks[0].ssm.A_diag.grad
    assert torch.isfinite(a_grad).all() and a_grad.abs().sum() > 0
