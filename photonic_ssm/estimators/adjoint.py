# NEW (task S0.4b, 2026-07-07) — the recurrent in-situ photonic adjoint on
# the shared substrate, per the S0.4b spec PRE-registered at c85fe62 (before
# this build) and the signed PR-7 row (1 forward + 1 adjoint = 2 device
# passes/update; digital side-ledger = 0).
"""Recurrent in-situ adjoint estimator (roadmap S0.4b; PR-7 row 3).

The method (Hughes/Fan/Pai lineage, time-domain/cavity extension): the
gradient is obtained from TWO physical device passes —

  * pass 1 (device): the physical forward. Measured y_phys, registered ASE,
    no autograd. The error signal e = dL/dy at y_phys is computed digitally
    (uncharged, like SPSA's loss evaluations).
  * pass 2 (device): the physical ADJOINT pass — the error field propagated
    through the same noisy dissipative substrate (fresh ASE; roadmap S0.4b:
    "*not* autodiff-through-the-substrate", which is the BPTT reference).

Simulation of pass 2: autodiff through a **fresh-ASE replay of the device
itself** — same commanded parameters (it IS the device: no twin, no PR-5
mismatch), with the saturating gain FROZEN at its operating-point value
(`detach_gain=True`): a counter-propagating adjoint field sees the medium's
saturation state but cannot realize the ∂g/∂κ_ext self-consistency Jacobian
channel (the S31-F1 channel — structurally absent from a physical adjoint,
as from the M-struct twin, but frozen here at the *correct saturated value*,
not the fixed-plane value). Estimator identity

    y_adj = y_phys + (y_replay - detach(y_replay))

whose backward is the exact adjoint recursion of the (frozen-gain,
adj-ASE-realization) linearization applied to the physical error. The replay
plus its autodiff backward together simulate ONE physical adjoint pass (the
physical gradient readout is forward/adjoint-field interference; that
readout's hardware burden is an F8-ledger item, not a pass count).

Registered sim-model limitations (S0.4b spec; both flattering to adjoint —
the bake-off adjoint arm is an OPTIMISTIC bound and the paper must say so):
(i) ASE enters through the replay trajectory, not additionally as an
additive term on the adjoint field (the additive-λ channel needs an
error-launch power convention = unresolved hardware design, debt #4);
(ii) gain-medium non-reciprocity and the CW/CCW-doublet interaction of a
counter-propagating field are exact in-model (autograd's 2N×2N adjoint) —
their hardware separability is an F8-ledger item.

Cost accounting (PR-7): one update = 2×batch device passes, 0 digital.
"""

from __future__ import annotations

from typing import Optional

import torch

from ..substrate.dissipative_ring import DissipativeRingSubstrate


class AdjointEstimator:
    """1-forward + 1-adjoint device-pass gradient on the shared substrate.

    step(u, loss_fn, gen_fwd, gen_adj) -> (loss_value, y_phys):
      * physical forward (fresh ASE, generator `gen_fwd`), no autograd;
      * fresh-ASE device replay (generator `gen_adj` — PR-11: never the same
        stream; the adjoint pass is its own noisy device pass) with
        detach_gain=True, building the autograd graph on the substrate's own
        live nn.Parameters;
      * loss on y_adj = y_phys + (y_replay − detach(y_replay)); backward
        fills the in-situ parameter grads via the frozen-gain adjoint.
    The caller owns the optimizer step + clamp (harness). Ledgers per PR-7.
    """

    def __init__(self, sub: DissipativeRingSubstrate):
        self.sub = sub
        self.n_device_passes = 0          # PR-7 primary (physical) ledger
        self.n_digital_passes = 0         # stays 0 (PR-7 row 3)

    def forward_physical(self, u: torch.Tensor,
                         generator: Optional[torch.Generator] = None
                         ) -> torch.Tensor:
        """Measured R2 intensity trace, no autograd (device pass 1)."""
        with torch.no_grad():
            y = self.sub.forward_intensity(u, generator=generator)
        batch = u.shape[0] if u.ndim == 3 else 1
        self.n_device_passes += batch
        return y

    def step(self, u: torch.Tensor, loss_fn,
             gen_fwd: Optional[torch.Generator] = None,
             gen_adj: Optional[torch.Generator] = None):
        """One adjoint gradient evaluation: fills .grad on the substrate's
        in-situ parameters {δ, κ_ext, μ}. Returns (loss, y_phys)."""
        y_phys = self.forward_physical(u, generator=gen_fwd)
        self.sub.detach_gain = True
        try:
            y_replay = self.sub.forward_intensity(u, generator=gen_adj)
        finally:
            self.sub.detach_gain = False
        y_adj = y_phys + (y_replay - y_replay.detach())
        loss = loss_fn(y_adj)
        loss.backward()
        batch = u.shape[0] if u.ndim == 3 else 1
        self.n_device_passes += batch     # device pass 2 (the adjoint pass)
        return float(loss.detach()), y_phys
