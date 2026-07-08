# NEW (task S0.3-1, deliverable 1) — the single shared dissipative-ring
# substrate that all four in-situ-training estimators (S0.4) and the bake-off
# (S0.5) train through. Implements the frozen PR-4 v2 substrate (M1 gain / A2
# ASE / K-pol-3 splitting / K4 trainable κ_ext / cells C-1..C-3 / O2). Sets no
# values; every parameter traces to PR-4 v2 or an inherited S0.1 convention.
"""DissipativeRingSubstrate — the shared Stage-0 substrate (PR-4 v2).

The N-ring coupled-mode recurrence the headline result is measured on:

    da/dt = M a + B u + F,    a_{k+1} = Φ a_k + Γ u_k + η_k  (ZOH/van-Loan),

with M the 2N×2N CW/CCW doublet (K-pol-3 always ON), gain folded into the
net loss at the registered operating point (M1, g_rt = 0.9·κᵢ ⇒ κ_net =
0.1κᵢ + 2κ_ext), and η the per-step A2 Langevin ASE increment. The gain is
**`saturating` by default** (g(P̄(κ_ext)) responds to the trained κ_ext as
physics, §G/§N-E6 — the registered bake-off mode for all four estimators, so
SPSA's two forward passes and the gradient methods' backward pass target one
function; `"fixed"` is a diagnostic floor, see `gain_mode`). It extends the
S0.1 forward model (`dynamics.coupled_rings`) — same _build_M / van-Loan
discretization, same amplitude-rate conventions — with the realistic
dissipative physics the recon flagged.

Trainable recurrent parameters = the frozen PR-2 P2 partition {δ_j, κ_ext,j,
μ_jk} (gain-free; κᵢ is a fixed per-cell buffer). κ_ext is trainable within
the K4 bounds r = κ_ext/κᵢ ∈ [0.1, 3]; μ is the nearest-neighbor chain
(N−1 couplers, fixed sparsity, μ(0)=0). No learnable Δt — dt ≡ 1/f_s (PR-2c).

Three F18 variance knobs — `loss_scale` (×κᵢ), `gain_factor` (the M1
operating fraction), `ase_variance_scale` (×Q_d ASE). Full state trajectory
(2N) exposed (F18 / constraint 3b). Intensity readout R2: y = |Σ_j c_j a_j|²
(c the digital-trained residues; the |·|² is the only physical nonlinearity).
No `no_grad`/`detach` in the state path (constraint 3a) — the BPTT reference
trains end-to-end through gain+ASE+splitting (F18 gradient-flow gate, test h).
"""

from __future__ import annotations

from typing import Optional

import torch
from torch import nn

from ..dynamics.coupled_rings import _build_M, zoh_discretize
from ..dynamics.single_ring import tau_round_trip_s
from . import cells as cellmod
from . import gain as gainmod
from . import splitting as splitmod
from .ase import ASEInjector


class DissipativeRingSubstrate(nn.Module):
    """The shared PR-4 v2 dissipative-ring substrate.

    Parameters
    ----------
    cell        : a registered SubstrateCell (or its label via `from_cell`).
    N           : ring count (default = the cell's registered N).
    clock_GSps  : sampling clock in GS/s (PR-10 {0.1, 1, 2}); dt = 1/f_s.
    delta_band_rad_s : half-width of the δ init band [rad/s] (default a few κᵢ).
    loss_scale, ase_variance_scale : F18 variance knobs (default 1).
    gain_factor : M1 operating fraction (default = cell.gain_factor; 0.9 op,
                  0 passive, 0.5 sensitivity). Passive cells forced to 0.
    gain_mode   : "saturating" (DEFAULT, faithful — g(P̄(κ_ext)) responds to
                  the trained κ_ext as physics, §G/§N-E6; the registered
                  bake-off mode for ALL FOUR estimators, PR-6) or "fixed"
                  (diagnostic/sensitivity floor: g≡factor·κᵢ constant, the
                  gain-channel analogue of γ=0 — drops ∂g/∂κ_ext; the plane the
                  frozen operating-point numbers and the B1/E₀ calibrations are
                  quoted at).
    input_taps  : ring indices (0-based) the single bus drive is split into
                  (PR-6 §B v3 multi-tap input map B; §G-addendum ride-on on
                  PR-4 §N). Default (0,) = the original single-port ring-1
                  convention, bit-identical to the pre-S0.4-0 substrate. With
                  K taps the drive amplitude is split equally, weight 1/√K per
                  tap (total injected power conserved; the §G-addendum
                  total-energy E₀ budget is over the tap sum, not per ring).
    ase_convention : "A2" (default, exact Langevin) or "A1" (per-rt kick).
    dtype       : complex128 (default, S0.1 fidelity) or complex64.
    seed        : init RNG seed for δ (reproducibility).
    """

    def __init__(self, cell: cellmod.SubstrateCell, N: Optional[int] = None,
                 clock_GSps: float = 2.0,
                 delta_band_rad_s: Optional[float] = None,
                 loss_scale: float = 1.0, ase_variance_scale: float = 1.0,
                 gain_factor: Optional[float] = None,
                 gain_mode: str = "saturating", ase_convention: str = "A2",
                 input_taps: Optional[tuple] = None,
                 dtype: torch.dtype = torch.complex128,
                 seed: Optional[int] = None):
        super().__init__()
        self.cell = cell
        self.N = int(N if N is not None else cell.N)
        if input_taps is None:
            input_taps = (0,)
        taps = tuple(sorted({int(t) for t in input_taps}))
        if not taps or any(t < 0 or t >= self.N for t in taps):
            raise ValueError(
                f"input_taps must be non-empty 0-based ring indices < N={self.N}, "
                f"got {input_taps}")
        self.input_taps = taps
        self.clock_GSps = float(clock_GSps)
        self._dtype = dtype
        self._rdtype = torch.float64 if dtype == torch.complex128 else torch.float32
        self.gain_mode = gain_mode
        self.ase_convention = ase_convention
        self.loss_scale = float(loss_scale)
        self.ase_variance_scale = float(ase_variance_scale)
        # S0.4b: freeze g(P̄) at its operating-point value in the autograd
        # graph (adjoint pass: the counter-propagating field sees the medium's
        # saturation state but cannot realize the ∂g/∂κ_ext Jacobian channel).
        # Forward VALUES are bit-identical either way (gate B5).
        self.detach_gain = False
        # S0.6 (PR-12 R-ii): optional training-time upper bound on r = κ_ext/κᵢ
        # (a sub-box of the registered K4 band; None = the full band).
        self.r_hi_train = None

        plat = cellmod.platform_of(cell)
        self.FSR_Hz = plat.FSR_GHz * 1e9
        self.n_g = plat.n_g
        self.tau_rt = tau_round_trip_s(self.FSR_Hz)
        self.dt = 1.0 / (self.clock_GSps * 1e9)          # sample period (PR-2c)
        self.nf_dB = cell.nf_dB

        # Fixed per-cell physics (NOT trainable; gain-free partition).
        ki = cellmod.kappa_i_rad_s(cell)
        self.register_buffer("kappa_i",
                             torch.tensor(ki, dtype=self._rdtype))
        gvec = cellmod.gamma_rad_s(cell)
        self.register_buffer("gamma",
                             torch.full((self.N,), gvec, dtype=self._rdtype))

        # M1 operating fraction (passive cells forced passive).
        gf = cell.gain_factor if gain_factor is None else float(gain_factor)
        if cell.passive_only:
            gf = 0.0
        self.gain_factor = float(gf)
        kext0 = cellmod.R0_THETA0 * ki                    # θ₀ hold value
        self.gain_model = gainmod.build_gain_model(
            ki, kext0, self.gain_factor, self.FSR_Hz)

        # --- Trainable P2 partition {δ_j, κ_ext,j, μ_jk} ------------------ #
        gen = None
        if seed is not None:
            gen = torch.Generator().manual_seed(int(seed))
        if delta_band_rad_s is None:
            # In-band, resolvable default: spread poles over a few intrinsic
            # linewidths. The PR-6 bake-off init freeze supersedes this.
            delta_band_rad_s = 4.0 * ki
        if self.N == 1:
            delta0 = torch.zeros(1, dtype=self._rdtype)
        else:
            delta0 = torch.linspace(-1.0, 1.0, self.N, dtype=self._rdtype) \
                * float(delta_band_rad_s)
        self.delta = nn.Parameter(delta0)
        self.kappa_ext = nn.Parameter(
            torch.full((self.N,), kext0, dtype=self._rdtype))
        # Nearest-neighbor chain couplers (N−1 strengths), μ(0)=0 (PR-2b).
        self.mu_chain = nn.Parameter(
            torch.zeros(max(self.N - 1, 0), dtype=self._rdtype))

        # Digital-trained readout residues c_j over the CW modes (R2). Default
        # uniform; the bake-off trains these digitally (not the in-situ set).
        self.register_buffer(
            "c_readout", torch.ones(self.N, dtype=self._dtype))

    # ------------------------------------------------------------------ #
    #  Construction helpers
    # ------------------------------------------------------------------ #
    @classmethod
    def from_cell(cls, label: str, **kw) -> "DissipativeRingSubstrate":
        """Build from a registered cell label ("C-1", "C-2", ...)."""
        return cls(cellmod.get_cell(label), **kw)

    # ------------------------------------------------------------------ #
    #  Rates / matrices
    # ------------------------------------------------------------------ #
    def gain_rate_per_ring(self) -> torch.Tensor:
        """The M1 gain rate g_j [rad/s] per ring at the current operating
        point. `saturating` (default, registered bake-off mode): g(P̄(κ_ext,
        drive)) — differentiable in κ_ext, so ∂g/∂κ_ext enters the autograd
        graph (§G/§N-E6). `fixed` (diagnostic): g = factor·κᵢ constant — drops
        ∂g/∂κ_ext (the gain-channel floor, the plane the frozen numbers use)."""
        ki = self.kappa_i
        if self.gain_factor == 0.0:
            return torch.zeros(self.N, dtype=self._rdtype)
        if self.gain_mode == "fixed":
            return torch.full((self.N,), self.gain_factor * float(ki),
                              dtype=self._rdtype)
        # saturating: g(P̄) per ring from each ring's κ_ext (drive on head;
        # build-up is the per-ring on-resonance estimate).
        g = self.gain_model.rate_saturating(self.kappa_ext).to(self._rdtype)
        return g.detach() if self.detach_gain else g

    def kappa_net(self) -> torch.Tensor:
        """Net amplitude decay κ_net,j = loss_scale·κᵢ − g_j + 2κ_ext,j
        [rad/s] (the operating-point pole real part). > 0 (sub-threshold) by
        construction at the registered points."""
        ki = self.loss_scale * self.kappa_i
        return ki - self.gain_rate_per_ring() + 2.0 * self.kappa_ext

    def mu_matrix(self) -> torch.Tensor:
        """Assemble the (N,N) real symmetric nearest-neighbor coupling Ω from
        the N−1 chain strengths (fixed tridiagonal sparsity mask)."""
        M = torch.zeros((self.N, self.N), dtype=self._rdtype)
        if self.N >= 2:
            idx = torch.arange(self.N - 1)
            M[idx, idx + 1] = self.mu_chain
            M[idx + 1, idx] = self.mu_chain
        return M

    def M_dir(self) -> torch.Tensor:
        """Single-direction (CW) coupled-ring matrix diag(−κ_net + iδ) + iΩ(μ)
        — the S0.1 builder at the operating point (N×N complex)."""
        return _build_M(self.kappa_net(), self.delta,
                        self.mu_matrix()).to(self._dtype)

    def M_doublet(self) -> torch.Tensor:
        """The full 2N×2N CW/CCW doublet matrix (K-pol-3 always ON)."""
        return splitmod.doublet_matrix(self.M_dir(), self.gamma)

    def B_doublet(self) -> torch.Tensor:
        """Input map B (PR-6 §B v3): the single bus drive split equally over
        `input_taps` (CW modes), weight 1/√K per tap so total injected power
        is conserved. b_t = sqrt(2κ_ext,t)/√K — differentiable in κ_ext,t
        (physical coupling). Default taps (0,) = the original single-port
        ring-1 §N convention (weight 1, bit-identical)."""
        K = len(self.input_taps)
        w = 1.0 / (K ** 0.5)
        rows = torch.zeros((self.N, 1), dtype=self._dtype)
        B_dir = rows.index_put(
            (torch.tensor(self.input_taps), torch.zeros(K, dtype=torch.long)),
            (w * torch.sqrt(2.0 * self.kappa_ext[list(self.input_taps)])
             ).to(self._dtype))
        return splitmod.embed_input(B_dir)

    def C_doublet(self) -> torch.Tensor:
        """Readout map: c_j over the CW modes (drop-port detection)."""
        C_dir = self.c_readout.reshape(1, self.N)
        return splitmod.embed_readout(C_dir)

    # ------------------------------------------------------------------ #
    #  Pole / region accessors
    # ------------------------------------------------------------------ #
    def continuous_poles(self) -> torch.Tensor:
        """System poles = eigenvalues of the 2N×2N doublet M (hybridized by μ
        and split by γ). Each is −κ + iω."""
        return torch.linalg.eigvals(self.M_doublet())

    def discrete_poles(self) -> torch.Tensor:
        """Discrete-time poles = eig(Φ), |z| = per-step memory retention."""
        Phi, _ = zoh_discretize(self.M_doublet(), self.B_doublet(), self.dt)
        return torch.linalg.eigvals(Phi)

    def r_ratios(self) -> torch.Tensor:
        """Per-ring κ_ext/κᵢ — the K4 ratios (bounds [0.1, 3])."""
        return self.kappa_ext.detach() / self.kappa_i

    def bounds_ok(self, eps: float = 1e-9) -> bool:
        """True iff every κ_ext is within the K4 bounds r ∈ [0.1, 3]."""
        r = self.r_ratios()
        lo, hi = cellmod.R_BOUNDS
        return bool(torch.all(r >= lo - eps) and torch.all(r <= hi + eps))

    @torch.no_grad()
    def clamp_to_bounds(self) -> None:
        """Project κ_ext back into the operative trainable band (training-time
        box constraint; not used inside the autograd rollout). In the
        registered `saturating` mode with gain ON, the lower bound is the
        S0.4-0-measured r_min (PR-6 v3 §C clamp A — below r*≈0.134 the ring
        lases and the linear rollout diverges); in `fixed`/passive modes the
        K4 passive-plane bound r=0.1 applies."""
        lo, hi = cellmod.R_BOUNDS
        if self.gain_mode == "saturating" and self.gain_factor > 0.0:
            lo = cellmod.R_MIN_SATURATING
        if self.r_hi_train is not None:          # S0.6 sub-box (PR-12 R-ii)
            hi = self.r_hi_train
        self.kappa_ext.clamp_(lo * float(self.kappa_i),
                              hi * float(self.kappa_i))

    # ------------------------------------------------------------------ #
    #  Forward rollout
    # ------------------------------------------------------------------ #
    def forward(self, u: torch.Tensor, a0: Optional[torch.Tensor] = None,
                generator: Optional[torch.Generator] = None,
                checkpoint_chunk: Optional[int] = None,
                ) -> tuple[torch.Tensor, torch.Tensor]:
        """Integrate the substrate under drive u.

        u : (T,) / (T,1) / (batch,T,1) drive (photon-flux amplitude s_in;
            |u|² = P/ħω₀). One input channel (ring-1 bus).
        a0 : optional initial 2N state (default zeros).
        generator : ASE RNG. PR-11 — pass DIFFERENT generators for the forward
            and echo streams (fresh draws per pass).
        checkpoint_chunk : gradient-checkpointed chunked rollout (constraint
            3a memory bound) — bit-equivalent to the plain rollout.

        Returns
        -------
        states  : (..., T+1, 2N) complex — FULL doublet trajectory x_0..x_T
                  (F18 / 3b: exposed for adjoint/RHEL/reservoir).
        outputs : (..., T, p) complex — the linear readout C@x_k, k=1..T
                  (apply |·|² for the R2 intensity readout).
        """
        u = torch.as_tensor(u, dtype=self._dtype)
        if u.ndim == 1:
            u = u.reshape(1, -1, 1); squeeze = True
        elif u.ndim == 2:
            u = u.unsqueeze(0); squeeze = True
        elif u.ndim == 3:
            squeeze = False
        else:
            raise ValueError("u must be (T,), (T,1) or (batch,T,1)")
        batch, T, m = u.shape
        if m != 1:
            raise ValueError(f"substrate has 1 input channel, got m={m}")

        M = self.M_doublet()
        B = self.B_doublet()
        Phi, Gamma = zoh_discretize(M, B, self.dt)
        forcing = u @ Gamma.transpose(0, 1)              # (batch,T,2N)

        # ASE injector (M1: gain & M fixed within the rollout → covariance
        # precomputed once). variance_scale=0 ⇒ the noiseless limit.
        n2 = 2 * self.N
        g_per_ring = self.gain_rate_per_ring()
        g_per_mode = torch.cat([g_per_ring, g_per_ring])   # CW & CCW
        inject = None
        if self.ase_variance_scale > 0.0 and \
                float(g_per_mode.detach().abs().sum()) > 0:
            inject = ASEInjector(
                M, g_per_mode, self.nf_dB, self.dt,
                convention=self.ase_convention,
                variance_scale=self.ase_variance_scale,
                tau_rt=self.tau_rt)

        if a0 is None:
            a = torch.zeros((batch, n2), dtype=self._dtype)
        else:
            a = torch.as_tensor(a0, dtype=self._dtype)
            if a.ndim == 1:
                a = a.unsqueeze(0).expand(batch, n2).contiguous()

        if checkpoint_chunk is None:
            states = self._rollout(Phi, forcing, a, inject, batch, generator)
        else:
            states = self._rollout_chunked(Phi, forcing, a, inject, batch,
                                           generator, int(checkpoint_chunk))
        outputs = states[:, 1:, :] @ self.C_doublet().transpose(0, 1)
        if squeeze:
            states = states.squeeze(0)
            outputs = outputs.squeeze(0)
        return states, outputs

    def _rollout(self, Phi, forcing, a, inject, batch, generator):
        """Plain autograd recurrence a_{k+1} = Φ a_k + forcing_k + η_k. NO
        no_grad/detach on the state path (3a); η is exogenous (no grad)."""
        T = forcing.shape[1]
        PhiT = Phi.transpose(0, 1)
        states = [a]
        for k in range(T):
            a = a @ PhiT + forcing[:, k, :]
            if inject is not None:
                a = a + inject.sample(batch, generator).to(a.dtype)
            states.append(a)
        return torch.stack(states, dim=1)

    def _rollout_chunked(self, Phi, forcing, a, inject, batch, generator,
                         chunk):
        """Gradient-checkpointed chunked rollout (constraint 3a memory bound).
        ASE draws happen OUTSIDE the checkpointed function (noise must not be
        re-drawn on recomputation) and are passed in as fixed tensors."""
        T = forcing.shape[1]
        PhiT = Phi.transpose(0, 1)
        # Pre-draw all ASE increments (fixed across recomputation).
        if inject is not None:
            noise = torch.stack(
                [inject.sample(batch, generator).to(self._dtype)
                 for _ in range(T)], dim=1)            # (batch,T,2N)
        else:
            noise = None
        from torch.utils.checkpoint import checkpoint

        def run_chunk(a_start, f_chunk, n_chunk):
            outs = []
            a_loc = a_start
            for k in range(f_chunk.shape[1]):
                a_loc = a_loc @ PhiT + f_chunk[:, k, :]
                if n_chunk is not None:
                    a_loc = a_loc + n_chunk[:, k, :]
                outs.append(a_loc)
            return torch.stack(outs, dim=1)

        segs = [a.unsqueeze(1)]
        a_start = a
        for c0 in range(0, T, chunk):
            f_chunk = forcing[:, c0:c0 + chunk, :]
            n_chunk = None if noise is None else noise[:, c0:c0 + chunk, :]
            seg = checkpoint(run_chunk, a_start, f_chunk, n_chunk,
                             use_reentrant=False)
            segs.append(seg)
            a_start = seg[:, -1, :]
        return torch.cat(segs, dim=1)

    # ------------------------------------------------------------------ #
    #  Readout
    # ------------------------------------------------------------------ #
    def cw_states(self, states: torch.Tensor) -> torch.Tensor:
        """The CW half (N modes) of a doublet trajectory (for reservoir taps
        / adjoint)."""
        return splitmod.cw_block(states)

    @staticmethod
    def intensity(outputs: torch.Tensor) -> torch.Tensor:
        """R2 direct-detection readout y = |Σ_j c_j a_j|² from the complex
        linear readout (the substrate's only physical nonlinearity)."""
        return outputs.abs() ** 2

    def forward_intensity(self, u, **kw) -> torch.Tensor:
        """Convenience: rollout and return the R2 intensity readout y(n),
        shape (..., T). Real, autograd-safe."""
        _, outputs = self.forward(u, **kw)
        return self.intensity(outputs).squeeze(-1)
