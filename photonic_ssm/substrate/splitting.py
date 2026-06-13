# NEW (task S0.3-1, deliverable 4) — K-pol-3 CW/CCW backscatter doublet.
# Implements the frozen PR-4 v2 §S choice: the 2x2 doublet machinery runs at
# every cell (always ON); γ=0 recovers the single-pole model exactly. Sets no
# values — γ per cell comes from cells.py (frozen PR-4 v2 §C).
"""CW/CCW mode-splitting doublet (K-pol-3, always ON) — proposal §4 / B2.

Fabrication roughness back-couples a ring's clockwise (CW) and
counter-clockwise (CCW) travelling modes at a rate γ [rad/s]; the
resonance resolves into a doublet split by 2γ (the measurable splitting;
see `pole_region.splitting_linewidth_ratio`). PR-4 v2 §S registers this
knob **always ON** at every cell (under the K4 trainable-κ_ext policy the
κ_ext-conditional knob-off policies are incoherent — trained κ_ext moves
through their validity boundary mid-run).

Representation. State is ordered [cw_1..cw_N, ccw_1..ccw_N] (two N-blocks).
The 2N×2N continuous matrix is

    M_doublet = [[ M_dir ,  iΓ   ],
                 [  iΓ   , M_dir ]],     Γ = diag(γ_j)  (N×N),

where M_dir = diag(-κ_net,j + i·δ_j) + iΩ(μ) is the single-direction
coupled-ring matrix the S0.1 `coupled_rings._build_M` already builds (the
inter-ring photonic-molecule coupling μ acts identically in each direction
sector — a substrate-internal basis choice; PR-4 pins only "the same 2×2
machinery the coupled-μ hook needs anyway"). The bus drives the CW modes
only and the drop-port readout reads the CW modes only, so:

  * the per-ring CW/CCW pair has eigenvalues -κ_net + i(δ ± γ) — the doublet
    split by 2γ;
  * **γ = 0 ⇒ the CCW block decouples and stays undriven (zero) ⇒ the model
    is bit-identical to the single-direction S0.1 coupled-ring model.** This
    is the registered reduction (unit test g).

All functions are torch-only and differentiable in (M_dir, γ).
"""

from __future__ import annotations

import torch


def doublet_matrix(M_dir: torch.Tensor, gamma: torch.Tensor) -> torch.Tensor:
    """Assemble the 2N×2N CW/CCW doublet matrix from the N×N single-direction
    matrix `M_dir` and the per-ring backscatter rates `gamma` (N,) [rad/s].

    Returns a (2N, 2N) complex tensor [[M_dir, iΓ],[iΓ, M_dir]],
    differentiable in both inputs. γ=0 ⇒ block-diagonal (two decoupled
    copies of M_dir).
    """
    N = M_dir.shape[-1]
    if gamma.shape[-1] != N:
        raise ValueError(f"gamma length {gamma.shape[-1]} != N {N}")
    cdtype = M_dir.dtype
    iGamma = (1j * torch.diag(gamma.to(M_dir.real.dtype))).to(cdtype)
    top = torch.cat([M_dir, iGamma], dim=-1)
    bot = torch.cat([iGamma, M_dir], dim=-1)
    return torch.cat([top, bot], dim=-2)


def embed_input(B_dir: torch.Tensor) -> torch.Tensor:
    """Lift an N×m single-direction input map B_dir to the 2N×m doublet input
    map: the bus drives the CW block only (CCW rows zero). γ then routes drive
    into the CCW modes dynamically."""
    N, m = B_dir.shape
    zeros = B_dir.new_zeros((N, m))
    return torch.cat([B_dir, zeros], dim=-2)


def embed_readout(C_dir: torch.Tensor) -> torch.Tensor:
    """Lift a p×N single-direction readout map C_dir to p×2N: the drop-port
    detector reads the CW block only (CCW columns zero)."""
    p, N = C_dir.shape
    zeros = C_dir.new_zeros((p, N))
    return torch.cat([C_dir, zeros], dim=-1)


def cw_block(states_2N: torch.Tensor) -> torch.Tensor:
    """Slice the CW half (first N modes) out of a doublet state/trajectory
    whose last dim is 2N. Used by readouts and reductions."""
    twoN = states_2N.shape[-1]
    N = twoN // 2
    return states_2N[..., :N]


def ccw_block(states_2N: torch.Tensor) -> torch.Tensor:
    """Slice the CCW half (last N modes) out of a doublet state/trajectory."""
    twoN = states_2N.shape[-1]
    N = twoN // 2
    return states_2N[..., N:]
