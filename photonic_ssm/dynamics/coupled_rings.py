# NEW (task S0.1, deliverable 2) — not salvage. The coupled-ring ->
# N-oscillator LinOSS dynamical forward model. pnn-multilayer has no
# temporal coupled-mode ring code (shared/tooling_recon.md), so this is
# new under either salvage ruling.
"""Coupled-ring -> N-oscillator LinOSS forward model (proposal §3, §1.2).

N microrings with intracavity amplitudes a(t) in C^N obey the linear
time-invariant coupled-mode system

    da/dt = M a + B u(t),     M = diag(-kappa_tot_j + i*delta_j) + i*Omega,

where the diagonal carries each ring's pole -kappa_tot_j + i*delta_j,
identified with the oscillator/SSM eigenvalue a_j = -exp(alpha_j) + i*beta_j
(proposal §3: exp(alpha_j) = kappa_tot_j, beta_j = delta_j), and the
Hermitian off-diagonal Omega (real-symmetric mu_jk) is direct
photonic-molecule inter-ring coupling (i*Omega is anti-Hermitian =>
energy-conserving coupling). The eigenvalues of M are the *system* poles
(coupling hybridizes the bare ring poles). This is the diagonal/
near-diagonal complex-pole SSM of proposal §1.1, H(s) = sum_j c_j b_j /
(s - lambda_j) + D; the LinOSS oscillatory unit is its conjugate-pair-
structured / damped-harmonic special case (D-LinOSS damping = -Re lambda,
a free knob).

Parametrization. The *recurrent* parameters — the load-bearing
"pole positions + inter-ring couplings that define the recurrence" of the
white-space claim — are trainable nn.Parameters:
  * log_kappa_tot (N,)  -> kappa_tot = exp(log_kappa_tot) = exp(alpha_j);
    storing the log enforces the dissipative -exp(alpha) real part and
    kappa_tot > 0 by construction (proposal's a_j = -exp(alpha_j)).
  * delta (N,)          -> beta_j (ring detuning; heater-actuated, B1).
  * mu_offdiag          -> real-symmetric inter-ring coupling (B1).
The input/output maps B, C (the residues b_j, c_j / the MZI mesh, B1) are
provided tensors here; their trainability is the S0.2 LinOSS layer's job.

Discretization. Exact zero-order-hold (input held constant over a step):
    a_{k+1} = Phi a_k + Gamma u_k,
    Phi = expm(M*dt),  Gamma = (integral_0^dt expm(M s) ds) B,
computed together by the van Loan augmented-matrix exponential. expm is
differentiable, so gradients flow through Phi, Gamma into the recurrent
parameters.

Architecture constraints (roadmap F18 gates, baked in from S0.0):
  * (3a) gradients flow through the optical state — the rollout is a plain
    autograd recurrence (NO torch.no_grad / .detach, unlike the salvaged
    forward-only channel style). A gradient-checkpointed chunked rollout
    (the TrainingAwareDynamicSOAPerMode pattern) bounds memory and is
    tested to agree with the plain rollout in value AND gradient.
  * (3b) full state trajectory exposed — `forward` returns x_1..x_T (the
    adjoint/RHEL estimators at S0.4 and the reservoir readout consume it).
"""

from __future__ import annotations

import math
from typing import Optional

import torch
from torch import nn
from torch.utils.checkpoint import checkpoint


def _build_M(kappa_tot: torch.Tensor, delta: torch.Tensor,
             mu: Optional[torch.Tensor]) -> torch.Tensor:
    """Assemble the complex state matrix M = diag(-kappa_tot + i*delta)
    + i*Omega, with Omega = symmetric(mu) (zero diagonal). Returns an
    (N, N) complex tensor; differentiable in all inputs."""
    N = kappa_tot.shape[0]
    diag = torch.complex(-kappa_tot, delta)
    M = torch.diag(diag)
    if mu is not None:
        Omega = 0.5 * (mu + mu.transpose(-1, -2))
        Omega = Omega - torch.diag(torch.diagonal(Omega))  # zero diagonal
        M = M + 1j * Omega.to(M.dtype)
    return M


def zoh_discretize(M: torch.Tensor, B: torch.Tensor, dt: float
                   ) -> tuple[torch.Tensor, torch.Tensor]:
    """Exact zero-order-hold discretization via the van Loan augmented
    matrix exponential:

        [[Phi, Gamma],   = expm( [[M, B],   * dt )
         [0,   I    ]]            [0, 0]]

    M: (N, N) complex; B: (N, m) complex. Returns (Phi (N,N), Gamma (N,m)),
    both differentiable. Exact for piecewise-constant input — no
    integration error, so the discrete poles are expm(lambda*dt) of the
    continuous poles to machine precision.
    """
    N = M.shape[0]
    m = B.shape[1]
    aug = M.new_zeros((N + m, N + m))
    aug[:N, :N] = M
    aug[:N, N:] = B
    E = torch.matrix_exp(aug * dt)
    Phi = E[:N, :N]
    Gamma = E[:N, N:]
    return Phi, Gamma


class CoupledRingLinOSS(nn.Module):
    """Dynamical coupled-ring (N-oscillator LinOSS) forward model.

    Parameters
    ----------
    kappa_tot : (N,) total amplitude decay rates [rad/s] (pole real parts;
        = exp(alpha_j)). Stored as log for the dissipative parametrization.
    delta : (N,) ring detunings [rad/s] (= beta_j).
    dt : step [s] (the SSM step Delta = round-trip time / sampling period).
    mu : (N, N) optional real inter-ring coupling rates [rad/s]
        (photonic-molecule); symmetrized, diagonal ignored.
    B : (N, m) complex input map (default sqrt(2*kappa_ext) injection if
        kappa_ext given, else ones into a single input channel).
    C : (p, N) complex output map (default identity -> state is the output).
    kappa_ext : (N,) optional external coupling rates, only used to build a
        physical default B = diag(sqrt(2*kappa_ext)) (m = N).
    dtype : complex dtype (default complex128 for numerical fidelity).
    """

    def __init__(self, kappa_tot, delta, dt: float, mu=None, B=None, C=None,
                 kappa_ext=None, dtype: torch.dtype = torch.complex128):
        super().__init__()
        rdtype = torch.float64 if dtype == torch.complex128 else torch.float32
        kappa_tot = torch.as_tensor(kappa_tot, dtype=rdtype)
        delta = torch.as_tensor(delta, dtype=rdtype)
        if kappa_tot.ndim != 1 or delta.shape != kappa_tot.shape:
            raise ValueError("kappa_tot and delta must be matching 1-D (N,)")
        if torch.any(kappa_tot <= 0):
            raise ValueError("kappa_tot must be > 0 (dissipative pole; the "
                             "-exp(alpha) parametrization needs a damped pole)")
        N = kappa_tot.shape[0]
        self.N = N
        self.dt = float(dt)
        self._dtype = dtype
        self._rdtype = rdtype

        # Recurrent parameters (the trainable recurrence — B1 / white-space).
        self.log_kappa_tot = nn.Parameter(torch.log(kappa_tot))
        self.delta = nn.Parameter(delta.clone())
        if mu is not None:
            mu = torch.as_tensor(mu, dtype=rdtype)
            self.mu = nn.Parameter(mu.clone())
        else:
            self.register_parameter("mu", None)

        # Input/output maps (residues / MZI mesh — provided, not trained here).
        if B is None:
            if kappa_ext is not None:
                kext = torch.as_tensor(kappa_ext, dtype=rdtype)
                B = torch.diag(torch.sqrt(2.0 * kext)).to(dtype)
            else:
                B = torch.ones((N, 1), dtype=dtype)
        else:
            B = torch.as_tensor(B, dtype=dtype)
            if B.ndim == 1:
                B = B.reshape(N, 1)
        self.register_buffer("B", B)
        if C is None:
            C = torch.eye(N, dtype=dtype)
        else:
            C = torch.as_tensor(C, dtype=dtype)
        self.register_buffer("C", C)

    # ---- matrix / pole accessors ------------------------------------- #

    @property
    def kappa_tot(self) -> torch.Tensor:
        return torch.exp(self.log_kappa_tot)

    def alpha_beta(self) -> tuple[torch.Tensor, torch.Tensor]:
        """The (alpha_j, beta_j) eigenvalue parameters: a_j = -exp(alpha_j)
        + i*beta_j, so alpha_j = log_kappa_tot, beta_j = delta."""
        return self.log_kappa_tot, self.delta

    def M(self) -> torch.Tensor:
        return _build_M(self.kappa_tot, self.delta, self.mu).to(self._dtype)

    def continuous_poles(self) -> torch.Tensor:
        """System poles = eigenvalues of M (= bare ring poles when
        uncoupled; hybridized by mu). Each is -kappa + i*omega."""
        return torch.linalg.eigvals(self.M())

    def discrete_poles(self) -> torch.Tensor:
        """Discrete-time poles = eigenvalues of Phi = expm(M*dt). Magnitude
        |z| = exp(-kappa*dt) is the per-step memory retention (|lambda| ->
        1 = long memory)."""
        Phi, _ = zoh_discretize(self.M(), self.B, self.dt)
        return torch.linalg.eigvals(Phi)

    # ---- forward rollout --------------------------------------------- #

    def forward(self, u: torch.Tensor, a0: Optional[torch.Tensor] = None,
                checkpoint_chunk: Optional[int] = None
                ) -> tuple[torch.Tensor, torch.Tensor]:
        """Integrate the recurrence under input u.

        u : (T, m) or (batch, T, m) real or complex drive (m = B's input dim).
        a0 : optional initial state (..., N) complex (default zeros).
        checkpoint_chunk : if set, run the rollout in gradient-checkpointed
            chunks of this many steps ((3a) memory bound, the
            TrainingAwareDynamicSOAPerMode pattern). None = plain autograd.

        Returns
        -------
        states : (..., T+1, N) complex — the FULL trajectory x_0..x_T,
            including the initial state ((3b): exposed for adjoint/RHEL/
            reservoir readout).
        outputs : (..., T, p) complex — C @ x_k for k = 1..T.
        """
        u = torch.as_tensor(u)
        if u.ndim == 2:
            u = u.unsqueeze(0)
            squeeze = True
        elif u.ndim == 3:
            squeeze = False
        else:
            raise ValueError("u must be (T, m) or (batch, T, m)")
        u = u.to(self._dtype)
        batch, T, m = u.shape
        if m != self.B.shape[1]:
            raise ValueError(f"input dim {m} != B input dim {self.B.shape[1]}")

        Phi, Gamma = zoh_discretize(self.M(), self.B, self.dt)
        # Precompute the per-step forcing Gamma @ u_k for all k: (batch,T,N).
        forcing = u @ Gamma.transpose(0, 1)

        if a0 is None:
            a = torch.zeros((batch, self.N), dtype=self._dtype)
        else:
            a = torch.as_tensor(a0, dtype=self._dtype)
            if a.ndim == 1:
                a = a.unsqueeze(0).expand(batch, self.N).contiguous()

        if checkpoint_chunk is None:
            states = self._rollout(Phi, forcing, a)
        else:
            states = self._rollout_checkpointed(Phi, forcing, a,
                                                int(checkpoint_chunk))
        outputs = states[:, 1:, :] @ self.C.transpose(0, 1)
        if squeeze:
            states = states.squeeze(0)
            outputs = outputs.squeeze(0)
        return states, outputs

    def _rollout(self, Phi, forcing, a):
        """Plain autograd recurrence a_{k+1} = Phi a_k + forcing_k.
        NO no_grad / detach — (3a). Returns (batch, T+1, N)."""
        batch, T, N = forcing.shape
        states = [a]
        PhiT = Phi.transpose(0, 1)
        for k in range(T):
            a = a @ PhiT + forcing[:, k, :]
            states.append(a)
        return torch.stack(states, dim=1)

    def _rollout_checkpointed(self, Phi, forcing, a, chunk):
        """Gradient-checkpointed chunked rollout (the
        TrainingAwareDynamicSOAPerMode pattern): O(n_chunks) stored
        activations instead of O(T). Bit-equivalent to `_rollout` in value
        and gradient (tested)."""
        batch, T, N = forcing.shape
        PhiT = Phi.transpose(0, 1)

        def run_chunk(a_start, f_chunk):
            outs = []
            a_loc = a_start
            for k in range(f_chunk.shape[1]):
                a_loc = a_loc @ PhiT + f_chunk[:, k, :]
                outs.append(a_loc)
            return torch.stack(outs, dim=1)  # (batch, chunk_len, N)

        chunks = [a.unsqueeze(1)]               # (batch, 1, N) initial state
        a_start = a
        for c0 in range(0, T, chunk):
            f_chunk = forcing[:, c0:c0 + chunk, :]
            seg = checkpoint(run_chunk, a_start, f_chunk, use_reentrant=False)
            chunks.append(seg)
            a_start = seg[:, -1, :]
        return torch.cat(chunks, dim=1)


# ---------------------------------------------------------------------- #
#  Convenience constructors
# ---------------------------------------------------------------------- #

def from_eigenvalues(alpha, beta, dt: float, **kw) -> CoupledRingLinOSS:
    """Build from the oscillator/SSM eigenvalue parameters directly:
    a_j = -exp(alpha_j) + i*beta_j, i.e. kappa_tot = exp(alpha), delta =
    beta (proposal §3)."""
    alpha = torch.as_tensor(alpha, dtype=torch.float64)
    beta = torch.as_tensor(beta, dtype=torch.float64)
    return CoupledRingLinOSS(torch.exp(alpha), beta, dt, **kw)
