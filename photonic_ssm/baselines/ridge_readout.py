# salvaged from pnn-multilayer @ e2eec80 : equalization_mrr_rc.py
#   (the Tikhonov-ridge closed-form solve + the delay-embedding block of
#    `_reservoir_features` / `LinearFFE_Intensity._build_design`)
# Adaptations for Project_SSM (task S0.0, deliverable 2):
#   - decoupled from the fixed MRR cascade, PAM-4/sps framing and PD
#     noise model (equalization content, not salvaged): the readout now
#     consumes ARBITRARY state-feature trajectories [T, F] — by design
#     the substrate's exposed state trajectories (constraint 3b);
#   - time-major [T, F] convention (torch RNN style) instead of the
#     source's [N, n_sym];
#   - solver, regularization and padding semantics unchanged.
"""Tikhonov-ridge readout + delay embedding (reservoir baseline, §5.3).

The reservoir-computing baseline of the bake-off: the photonic
recurrence stays FIXED (untrained) and only a linear readout is trained,
in closed form. Whatever the in-situ methods achieve must beat this to
claim that training the *physical recurrence* matters (proposal §5.3 —
"forfeit the novelty, but make it meaningful").

    w = (Phi^T Phi + alpha_R * I)^{-1} Phi^T y        (normal equation)

Pipeline: state trajectories [T, F] -> delay_embed (tap window) ->
ridge fit/predict. All torch, CPU-cheap, deterministic.
"""

from __future__ import annotations

import time
from typing import Optional

import torch


def delay_embed(features: torch.Tensor, delay_taps: int,
                add_bias: bool = True) -> torch.Tensor:
    """Delay-embed a time-major feature trajectory.

    Each output row t carries a window of `delay_taps` symbol-spaced
    copies of the features, centered on t (replicate padding at the
    edges — same semantics as the source's `_reservoir_features`).

    Args:
        features: [T, F] real tensor (state/feature trajectory).
        delay_taps: number of taps D in the window.
        add_bias: append a constant-1 column for the ridge intercept.

    Returns:
        [T, F*D (+1)] float32 design matrix.
    """
    if features.dim() != 2:
        raise ValueError(f"expected [T, F], got {tuple(features.shape)}")
    T, F = features.shape
    D = int(delay_taps)
    if D < 1:
        raise ValueError(f"delay_taps must be >= 1, got {delay_taps}")

    # Source convention: pad (half, D - half - 1) with replicate mode on
    # the time axis, then stack D shifted views.
    half = D // 2
    feat_tf = features.t().to(torch.float32)                  # [F, T]
    padded = torch.nn.functional.pad(
        feat_tf, (half, D - half - 1), mode="replicate")      # [F, T+D-1]
    cols = []
    for m in range(D):
        cols.append(padded[:, m: m + T])                      # [F, T]
    block = torch.stack(cols, dim=0)                          # [D, F, T]
    block = block.permute(2, 0, 1).contiguous().view(T, D * F)

    if add_bias:
        bias = torch.ones(T, 1, dtype=torch.float32)
        return torch.cat([block, bias], dim=1).contiguous()
    return block


class RidgeReadout:
    """Closed-form Tikhonov-regularized linear readout.

        fit:     w = (Phi^T Phi + alpha_R I)^{-1} Phi^T y
        predict: y_hat = Phi w

    Phi is any [T, F] design matrix (caller decides whether/how to
    delay-embed and whether a bias column is present).
    """

    def __init__(self, alpha_R: float = 1.0) -> None:
        self.alpha_R = float(alpha_R)
        self.w: Optional[torch.Tensor] = None
        self.fit_time_sec = 0.0
        self.n_params = 0

    def fit(self, Phi: torch.Tensor, y: torch.Tensor) -> None:
        """Phi: [T, F] real design matrix; y: [T] real targets."""
        t0 = time.time()
        Phi = Phi.to(torch.float32)
        y = y.to(torch.float32)
        if Phi.dim() != 2 or y.dim() != 1 or Phi.shape[0] != y.shape[0]:
            raise ValueError(
                f"shape mismatch: Phi {tuple(Phi.shape)}, y {tuple(y.shape)}")
        T, F = Phi.shape
        PhiTPhi = Phi.T @ Phi + self.alpha_R * torch.eye(F)
        PhiTy = Phi.T @ y
        self.w = torch.linalg.solve(PhiTPhi, PhiTy)           # [F]
        self.n_params = F
        self.fit_time_sec = time.time() - t0

    def predict(self, Phi: torch.Tensor) -> torch.Tensor:
        if self.w is None:
            raise RuntimeError("fit() first")
        return (Phi.to(torch.float32) @ self.w).to(torch.float32)


class ReservoirReadoutBaseline:
    """Reservoir baseline stub: fixed recurrence + trained linear readout.

    Consumes state-feature trajectories produced by a *frozen* forward
    model (the S0.3 substrate run with training disabled, per
    constraint 3b its API exposes them), delay-embeds, and ridge-fits.

    The S0.0 stub is fully functional on any [T, F] trajectory; wiring
    it to the substrate is S0.5 work.
    """

    def __init__(self, delay_taps: int = 11, alpha_R: float = 1.0) -> None:
        self.delay_taps = int(delay_taps)
        self.readout = RidgeReadout(alpha_R=alpha_R)

    def fit(self, states: torch.Tensor, targets: torch.Tensor) -> None:
        """states: [T, F] real feature trajectory; targets: [T] real."""
        Phi = delay_embed(states, self.delay_taps, add_bias=True)
        self.readout.fit(Phi, targets)

    def predict(self, states: torch.Tensor) -> torch.Tensor:
        Phi = delay_embed(states, self.delay_taps, add_bias=True)
        return self.readout.predict(Phi)

    @property
    def n_params(self) -> int:
        return self.readout.n_params
