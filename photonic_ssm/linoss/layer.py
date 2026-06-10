"""The in-house recurrence layer (S0.2-1) + its Gate-i LinOSS-IM configuration.

Two classes share one scan engine:

* ``LinOSSIMLayer`` — the Gate-i configuration (PR-1). Computes the published
  LinOSS-IM recurrence VERBATIM from the official repo (tk-rusch/linoss,
  models/LinOSS.py): ReLU-parametrized diagonal A, learnable per-dimension
  sigmoid timestep, implicit (IM) discretization, complex B/C with the real
  part taken after C, elementwise D feedthrough. The per-mode transition is
  the real 2x2 block

      M = [[M11, M12], [M21, M22]],  s = 1/(1 + dt^2 A),
      M11 = 1 - dt^2*A*s, M12 = -dt*A*s, M21 = dt*s, M22 = s,
      F_k = (M11*Bu_k*dt, M21*Bu_k*dt),   state x_k = (z_k, y_k),

  evaluated by an associative scan exactly as the official code does. The
  expressions above are kept character-identical to the official ones (e.g.
  M11 is computed as ``1 - dt^2*A*s`` even though it simplifies to ``s``) so
  float behavior matches.

* ``ComplexDiagSSM`` — the bake-off core: a first-order complex-diagonal
  (S4D/DSS-class) recurrence  alpha_k = lambda * alpha_{k-1} + W_in u_k  with
  an inter-mode coupling hook ``mu`` (nearest-neighbour, photonic-molecule
  chain — PR-2). Per resolved D-2026-06-08-2, LinOSS is the uncoupled,
  real-I/O conjugate-pair special case of this class:
  ``ComplexDiagSSM.from_linoss_im`` builds, for A > 0, the EXACT equivalent
  (eigenpair lambda = s*(1 + i*dt*sqrt(A)) per mode; two complex modes per
  LinOSS mode, one for each of the real/imag channels of the official complex
  state), and tests assert forward parity. Gate i runs the 2x2 real-block
  form because the similarity transform is undefined on the measure-zero
  ReLU boundary A == 0 (Jordan block: |lambda| = 1 double pole) — same
  recurrence, not an approximation (D-08-2).

  ``mu`` is 0 throughout S0.2-1 (PR-1 scope). The mu != 0 fast path is S0.3
  substrate work; a sequential reference exists for tests.

House architecture constraints (S0.0 deliverable 3): gradients flow through
the full state (no detach / no_grad anywhere on the scan path) and the full
state trajectory is exposed (``return_state=True``).

Complex arithmetic is carried as explicit (real, imag) channel pairs: the
2x2 transition M is real, so the real and imaginary parts of the official
complex state propagate independently — stacking them as a leading channel
gives identical numbers to complex64 while keeping autograd on real tensors.
"""

import math

import torch
from torch import nn

# ---------------------------------------------------------------------------
# Associative-scan engine
# ---------------------------------------------------------------------------


def _combine_2x2(A_i, A_j, b_i, b_j):
    """Compose aggregated affine elements (A_i, b_i) then (A_j, b_j).

    Mirrors the official ``binary_operator`` (models/LinOSS.py): per mode, a
    2x2 matrix product A_j @ A_i and b -> A_j @ b_i + b_j.

    A_*: (..., L', 4, m) stacked rows [iA, iB, iC, iD] (real).
    b_*: (..., L', 2, m) stacked components [b1, b2].
    """
    iA, iB, iC, iD = A_i.unbind(dim=-2)
    jA, jB, jC, jD = A_j.unbind(dim=-2)
    A_new = torch.stack(
        (
            jA * iA + jB * iC,
            jA * iB + jB * iD,
            jC * iA + jD * iC,
            jC * iB + jD * iD,
        ),
        dim=-2,
    )
    b1, b2 = b_i.unbind(dim=-2)
    b_new = torch.stack((jA * b1 + jB * b2, jC * b1 + jD * b2), dim=-2) + b_j
    return A_new, b_new


def assoc_scan_2x2(A, b):
    """Inclusive associative scan of per-mode 2x2 affine recurrences.

    A: (L, 4, m) transition element per step (here constant per step, but the
       scan is generic — the S0.3 substrate will have time-varying elements).
    b: (..., L, 2, m) input elements, leading dims are batch-like.
    Returns x: (..., L, 2, m), the state trajectory x_k = M x_{k-1} + F_k.

    Hillis–Steele doubling scan: same associative reduction as
    ``jax.lax.associative_scan``; association order differs (float-level
    only, both are reductions of the same associative operator).
    """
    L = A.shape[0]
    offset = 1
    while offset < L:
        A_comb, b_comb = _combine_2x2(
            A[:-offset], A[offset:], b[..., : L - offset, :, :], b[..., offset:, :, :]
        )
        A = torch.cat((A[:offset], A_comb), dim=0)
        b = torch.cat((b[..., :offset, :, :], b_comb), dim=-3)
        offset *= 2
    return b


def _apply2x2(P, b):
    """Apply one 2x2-per-mode matrix P (4, m) to b (..., 2, m)."""
    pA, pB, pC, pD = P.unbind(0)
    b1, b2 = b.unbind(-2)
    return torch.stack((pA * b1 + pB * b2, pC * b1 + pD * b2), dim=-2)


def _square2x2(P):
    pA, pB, pC, pD = P.unbind(0)
    return torch.stack(
        (pA * pA + pB * pC, pA * pB + pB * pD, pC * pA + pD * pC, pC * pB + pD * pD),
        dim=0,
    )


class _ConstScan2x2(torch.autograd.Function):
    """The assoc_scan_2x2 specialization for a transition CONSTANT over steps.

    Same Hillis–Steele association as assoc_scan_2x2 — at offset o every
    position's transition aggregate equals M^o (o identical factors), so the
    A-side collapses to repeated squaring of one (4, m) tensor and the b-side
    update is b[o:] += M^o (.) b[:-o], arithmetically identical to the generic
    combine. Backward is analytic BPTT: dL/dF_k = g_k with the reverse suffix
    scan g_k = delta_k + M^T g_{k+1} (run with the same doubling trick), and
    dL/dM_ab = sum_k g_k[a] x_{k-1}[b]. This keeps the 15-level scan graph out
    of autograd (the generic path's backward dominated G3 step time ~3x).
    """

    @staticmethod
    def forward(ctx, M, F):
        # M: (4, m); F: (..., L, 2, m)
        b = F.clone()
        L = F.shape[-3]
        P = M
        offset = 1
        while offset < L:
            b[..., offset:, :, :] += _apply2x2(P, b[..., : L - offset, :, :])
            P = _square2x2(P)
            offset *= 2
        ctx.save_for_backward(M, b)
        return b

    @staticmethod
    def backward(ctx, delta):
        M, xs = ctx.saved_tensors
        MT = torch.stack((M[0], M[2], M[1], M[3]), dim=0)
        g = delta.contiguous().clone()
        L = g.shape[-3]
        P = MT
        offset = 1
        while offset < L:
            g[..., : L - offset, :, :] += _apply2x2(P, g[..., offset:, :, :])
            P = _square2x2(P)
            offset *= 2
        x_prev = torch.zeros_like(xs)
        x_prev[..., 1:, :, :] = xs[..., :-1, :, :]
        g1, g2 = g.unbind(-2)
        x1, x2 = x_prev.unbind(-2)
        dims = tuple(range(g1.dim() - 1))
        dM = torch.stack(
            (
                (g1 * x1).sum(dim=dims),
                (g1 * x2).sum(dim=dims),
                (g2 * x1).sum(dim=dims),
                (g2 * x2).sum(dim=dims),
            ),
            dim=0,
        )
        return dM, g


def assoc_scan_diag(lam_re, lam_im, b_re, b_im):
    """Inclusive scan of a first-order complex-diagonal recurrence.

    alpha_k = lambda * alpha_{k-1} + b_k, carried as (re, im) pairs.
    lam_*: (L, m) per-step diagonal transition; b_*: (..., L, m).
    Returns (alpha_re, alpha_im): (..., L, m).
    """
    L = lam_re.shape[0]
    offset = 1
    while offset < L:
        a_re_i, a_im_i = lam_re[:-offset], lam_im[:-offset]
        a_re_j, a_im_j = lam_re[offset:], lam_im[offset:]
        b_re_i, b_im_i = b_re[..., : L - offset, :], b_im[..., : L - offset, :]
        b_re_j, b_im_j = b_re[..., offset:, :], b_im[..., offset:, :]
        a_re_new = a_re_j * a_re_i - a_im_j * a_im_i
        a_im_new = a_re_j * a_im_i + a_im_j * a_re_i
        b_re_new = a_re_j * b_re_i - a_im_j * b_im_i + b_re_j
        b_im_new = a_re_j * b_im_i + a_im_j * b_re_i + b_im_j
        lam_re = torch.cat((lam_re[:offset], a_re_new), dim=0)
        lam_im = torch.cat((lam_im[:offset], a_im_new), dim=0)
        b_re = torch.cat((b_re[..., :offset, :], b_re_new), dim=-2)
        b_im = torch.cat((b_im[..., :offset, :], b_im_new), dim=-2)
        offset *= 2
    return b_re, b_im


# ---------------------------------------------------------------------------
# Gate-i layer: the published LinOSS-IM recurrence, verbatim
# ---------------------------------------------------------------------------


class LinOSSIMLayer(nn.Module):
    """One LinOSS-IM SSM layer, parametrized exactly as the official repo.

    Parameters and init (official names / shapes / distributions):
        A_diag (m,)      ~ U[0, 1)      -> forward uses relu(A_diag)
        B      (m, H, 2) ~ U(+-1/sqrt(H))   [..., 0] real, [..., 1] imag
        C      (H, m, 2) ~ U(+-1/sqrt(m))
        D      (H,)      ~ N(0, 1)
        steps  (m,)      ~ U[0, 1)      -> forward uses sigmoid(steps)

    forward(u): u (batch, L, H) real -> (batch, L, H) real,
    out = Re(C @ y) + D*u with y the second state component.
    """

    def __init__(self, ssm_size, H, *, generator=None, use_generic_scan=False):
        super().__init__()
        self.ssm_size = ssm_size
        self.H = H
        self.use_generic_scan = use_generic_scan
        g = generator
        self.A_diag = nn.Parameter(torch.rand(ssm_size, generator=g))
        stdB = 1.0 / math.sqrt(H)
        self.B = nn.Parameter(torch.rand(ssm_size, H, 2, generator=g) * 2.0 * stdB - stdB)
        stdC = 1.0 / math.sqrt(ssm_size)
        self.C = nn.Parameter(torch.rand(H, ssm_size, 2, generator=g) * 2.0 * stdC - stdC)
        self.D = nn.Parameter(torch.randn(H, generator=g))
        self.steps = nn.Parameter(torch.rand(ssm_size, generator=g))

    def transition(self):
        """The per-mode IM transition rows (M11, M12, M21, M22) and dt, A.

        Expressions kept character-identical to the official apply_linoss_im.
        """
        A = torch.relu(self.A_diag)
        dt = torch.sigmoid(self.steps)
        schur = 1.0 / (1.0 + dt**2.0 * A)
        M11 = 1.0 - dt**2.0 * A * schur
        M12 = -1.0 * dt * A * schur
        M21 = dt * schur
        M22 = schur
        return M11, M12, M21, M22, dt, A

    def forward(self, u, return_state=False):
        B_, L, H = u.shape
        m = self.ssm_size
        M11, M12, M21, M22, dt, _ = self.transition()

        # Bu_k = B_complex @ u_k, carried as (re, im) stacked on a leading axis.
        Bre, Bim = self.B[..., 0], self.B[..., 1]  # (m, H)
        Bu = torch.stack((u @ Bre.T, u @ Bim.T), dim=0)  # (2, B, L, m)

        # F = (M11 * Bu * dt, M21 * Bu * dt), official order of factors.
        F = torch.stack((M11 * Bu * dt, M21 * Bu * dt), dim=-2)  # (2, B, L, 2, m)

        M = torch.stack((M11, M12, M21, M22), dim=0)  # (4, m)
        if self.use_generic_scan:
            A_elems = M.unsqueeze(0).expand(L, 4, m)
            xs = assoc_scan_2x2(A_elems, F)  # (2, B, L, 2, m)
        else:
            xs = _ConstScan2x2.apply(M, F)  # same scan, constant-M fast path
        y_re, y_im = xs[0, :, :, 1, :], xs[1, :, :, 1, :]  # (B, L, m)

        Cre, Cim = self.C[..., 0], self.C[..., 1]  # (H, m)
        out = y_re @ Cre.T - y_im @ Cim.T + self.D * u
        if return_state:
            return out, xs
        return out


# ---------------------------------------------------------------------------
# Bake-off core: complex-diagonal recurrence + coupling hook
# ---------------------------------------------------------------------------


class ComplexDiagSSM(nn.Module):
    """First-order complex-diagonal recurrence with an inter-mode coupling hook.

        alpha_k = (diag(lambda) + Mu) alpha_{k-1} + W_in u_k
        out_k   = Re(W_out alpha_k) + D u_k

    One mode = one complex pole (one ring, D-08-2; no conjugate pairing).
    ``mu`` (nearest-neighbour strengths, complex as (m-1, 2)) is the coupling
    hook — zero throughout S0.2-1. With mu == 0 the scan is diagonal and
    parallel; mu != 0 currently runs a sequential reference (the efficient
    coupled scan is S0.3 substrate work).
    """

    def __init__(self, n_modes, H, H_out=None, *, generator=None):
        super().__init__()
        H_out = H if H_out is None else H_out
        self.n_modes = n_modes
        g = generator
        # Placeholder stable init (overwritten by from_linoss_im / PR-6 init
        # conventions downstream): poles uniform in the stable half-disk.
        r = 0.9 + 0.1 * torch.rand(n_modes, generator=g)
        th = math.pi * torch.rand(n_modes, generator=g)
        self.lam = nn.Parameter(torch.stack((r * torch.cos(th), r * torch.sin(th)), dim=-1))
        std = 1.0 / math.sqrt(H)
        self.W_in = nn.Parameter(torch.rand(n_modes, H, 2, generator=g) * 2 * std - std)
        stdo = 1.0 / math.sqrt(n_modes)
        self.W_out = nn.Parameter(torch.rand(H_out, n_modes, 2, generator=g) * 2 * stdo - stdo)
        self.D = nn.Parameter(torch.zeros(H_out) if H_out != H else torch.randn(H, generator=g))
        self.mu = nn.Parameter(torch.zeros(n_modes - 1, 2))  # coupling hook, OFF

    def forward(self, u, return_state=False):
        B_, L, H = u.shape
        m = self.n_modes
        lam_re, lam_im = self.lam[:, 0], self.lam[:, 1]
        bu_re = u @ self.W_in[..., 0].T  # (B, L, m)
        bu_im = u @ self.W_in[..., 1].T

        if torch.any(self.mu != 0):
            a_re, a_im = self._sequential_coupled(bu_re, bu_im, lam_re, lam_im)
        else:
            lam_re_e = lam_re.unsqueeze(0).expand(L, m)
            lam_im_e = lam_im.unsqueeze(0).expand(L, m)
            a_re, a_im = assoc_scan_diag(lam_re_e, lam_im_e, bu_re, bu_im)

        out = a_re @ self.W_out[..., 0].T - a_im @ self.W_out[..., 1].T
        if self.D.shape[0] == H:
            out = out + self.D * u
        if return_state:
            return out, (a_re, a_im)
        return out

    def _sequential_coupled(self, bu_re, bu_im, lam_re, lam_im):
        """Sequential reference for mu != 0 (tests only; fast path = S0.3).

        Transition T = diag(lambda) + Mu with Mu the nearest-neighbour
        coupling matrix (mu_j on the j<->j+1 off-diagonals, symmetric).
        """
        m = self.n_modes
        T_re = torch.diag(lam_re)
        T_im = torch.diag(lam_im)
        idx = torch.arange(m - 1)
        T_re[idx, idx + 1] = T_re[idx, idx + 1] + self.mu[:, 0]
        T_re[idx + 1, idx] = T_re[idx + 1, idx] + self.mu[:, 0]
        T_im[idx, idx + 1] = T_im[idx, idx + 1] + self.mu[:, 1]
        T_im[idx + 1, idx] = T_im[idx + 1, idx] + self.mu[:, 1]
        B_, L, _ = bu_re.shape
        a_re = torch.zeros(B_, L, m, dtype=bu_re.dtype)
        a_im = torch.zeros(B_, L, m, dtype=bu_re.dtype)
        s_re = torch.zeros(B_, m, dtype=bu_re.dtype)
        s_im = torch.zeros(B_, m, dtype=bu_re.dtype)
        for k in range(L):
            n_re = s_re @ T_re.T - s_im @ T_im.T + bu_re[:, k]
            n_im = s_re @ T_im.T + s_im @ T_re.T + bu_im[:, k]
            s_re, s_im = n_re, n_im
            a_re[:, k] = s_re
            a_im[:, k] = s_im
        return a_re, a_im

    @classmethod
    def from_linoss_im(cls, layer: LinOSSIMLayer):
        """Build the EXACT complex-diagonal equivalent of a LinOSS-IM layer.

        Defined for relu(A_diag) > 0 strictly (D-08-2: the conjugate-pair
        special case). Per LinOSS mode j the 2x2 block M has eigenpair
        lambda_j = s*(1 + i*dt*sqrt(A)), eigenvector v = (i*sqrt(A), 1) for
        the state ordering x = (z, y); a real 2-state x = alpha*v + conj
        gives y = 2*Re(alpha). The official state is complex (F complex), so
        each LinOSS mode maps to TWO modes here — one per real/imag channel
        of Bu. The input element is g = (V^-1 F)_1 = (F1 + i*sqrt(A)*F2) /
        (2*i*sqrt(A)); with F1 = M11*Bu*dt = s*Bu*dt and F2 = M21*Bu*dt =
        s*Bu*dt^2 this reduces to g = Bu * dt*s * (dt/2 - i/(2*sqrt(A))).
        Output weights: +2*C_re (re-channel), -2*C_im (im-channel). On the
        A == 0 ReLU boundary the block is a Jordan cell (non-diagonalizable)
        — this map raises, and Gate i therefore runs the 2x2 real form
        (same recurrence).
        """
        with torch.no_grad():
            M11, M12, M21, M22, dt, A = layer.transition()
            if torch.any(A <= 0):
                raise ValueError(
                    "from_linoss_im: relu(A_diag) has zero entries — the 2x2 "
                    "block is a Jordan cell there; no diagonal equivalent."
                )
            m, H = layer.ssm_size, layer.H
            s = M22  # = 1/(1+dt^2 A)
            sqrtA = torch.sqrt(A)
            lam_re = s * torch.ones_like(A)
            lam_im = s * dt * sqrtA
            # complex input scale w = dt*s*(dt/2 - i/(2 sqrt(A)))
            w_re = dt * s * (dt / 2.0)
            w_im = dt * s * (-1.0 / (2.0 * sqrtA))
            Bre, Bim = layer.B[..., 0], layer.B[..., 1]  # (m, H)
            Cre, Cim = layer.C[..., 0], layer.C[..., 1]  # (H, m)

            eq = cls(2 * m, H, generator=torch.Generator().manual_seed(0))
            eq.lam.data = torch.cat(
                (
                    torch.stack((lam_re, lam_im), dim=-1),
                    torch.stack((lam_re, lam_im), dim=-1),
                ),
                dim=0,
            )
            # re-channel modes driven by Re(Bu) = B_re @ u; im-channel by Im.
            Win_re_ch = torch.stack((w_re[:, None] * Bre, w_im[:, None] * Bre), dim=-1)
            Win_im_ch = torch.stack((w_re[:, None] * Bim, w_im[:, None] * Bim), dim=-1)
            eq.W_in.data = torch.cat((Win_re_ch, Win_im_ch), dim=0)
            Wout_re_ch = torch.stack((2.0 * Cre, torch.zeros_like(Cre)), dim=-1)
            Wout_im_ch = torch.stack((-2.0 * Cim, torch.zeros_like(Cim)), dim=-1)
            eq.W_out.data = torch.cat((Wout_re_ch, Wout_im_ch), dim=1)
            eq.D.data = layer.D.data.clone()
            eq.mu.data = torch.zeros(2 * m - 1, 2)
        return eq
