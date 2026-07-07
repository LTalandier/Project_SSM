# NEW (task S0.4a phase 1, 2026-07-07) — Physics-Aware Training (PAT) on the
# shared substrate, with the PR-5 v2 twin-mismatch families (levels frozen in
# the S0.4a spec, task_queue.md 2026-07-07). Sets no values: every mismatch
# level, family, and convention traces to the signed PR-5/PR-6 blocks + the
# S0.4-0 calibration addendum.
"""PAT estimator (PR-5/PR-6; S0.4a).

PAT = **physical forward, digital-twin backward** (Wright et al., Nature 601,
549 (2022)): the loss is evaluated on the *measured* (physical) output; the
parameter gradient is taken through a differentiable digital twin evaluated
at the same commanded parameters. Implemented with the standard estimator
identity

    y_pat = y_phys + (y_twin - detach(y_twin))

whose forward value is y_phys and whose backward is the twin's Jacobian.

Twin families (PR-5 v2, decomposed — never conflated):
  * "perfect"  : exact copy of the substrate physics, noiseless (diagnostic).
  * "M-par"    : saturating twin with frozen calibration errors — κᵢ +5 %,
                 γ +5 %, actuation maps κ_ext ×1.05 / μ ×0.95, δ-offset
                 +0.05·κᵢ per ring, gain pair g-factor ×1.10 / P_sat ×0.75.
  * "M-struct" : `gain_mode="fixed"` twin (drops ∂g/∂κ_ext — the S31-F1
                 channel), true parameters.
  * "both"     : M-par ∘ M-struct.
All twins are **noiseless** (M-noise, always on): the substrate runs the
registered ASE; the twin does not model it.

The twin *shares the commanded trainable parameters* with the substrate (the
controller knows what it commanded — mismatch lives in the device constants
and the actuation maps, not in the command): its δ/κ_ext/μ attributes are
re-bound every step to expressions of the substrate's live nn.Parameters, so
twin gradients flow to the physical parameters.

Cost accounting (PR-7): one PAT update = 1×batch physical device passes
(forward) + the twin forward/backward on the DIGITAL side-ledger (never
dropped from reporting, never in the device count).
"""

from __future__ import annotations

from typing import Optional

import torch

from ..substrate import gain as gainmod
from ..substrate.dissipative_ring import DissipativeRingSubstrate

# PR-5 numeric levels — FROZEN in the S0.4a spec (task_queue.md, 2026-07-07).
MPAR_LEVELS = {
    "kappa_i_rel": +0.05,      # intrinsic-loss calibration error
    "gamma_rel": +0.05,        # backscatter-rate calibration error
    "kext_actuation": 1.05,    # tunable-coupler actuation-map error
    "mu_actuation": 0.95,      # ring–ring coupler actuation-map error
    "delta_offset_ki": +0.05,  # resonance-tracking offset, units of κᵢ
    "gain_factor_rel": +0.10,  # Er-gain characterization (debt #3, loose)
    "p_sat_rel": -0.25,        # P_sat characterization (debt #3, loose)
}
FAMILIES = ("perfect", "M-par", "M-struct", "both")


def build_twin(sub: DissipativeRingSubstrate, family: str
               ) -> DissipativeRingSubstrate:
    """Construct the digital twin of `sub` for a PR-5 family. The twin is a
    DissipativeRingSubstrate whose trainable attributes are UNBOUND (turned
    into plain tensors by `bind_command`) and whose fixed constants carry the
    frozen M-par errors where the family says so."""
    if family not in FAMILIES:
        raise ValueError(f"family must be one of {FAMILIES}, got {family!r}")
    mpar = family in ("M-par", "both")
    mstruct = family in ("M-struct", "both")

    twin = DissipativeRingSubstrate(
        sub.cell, N=sub.N,
        clock_GSps=sub.clock_GSps,
        loss_scale=sub.loss_scale * (1.0 + (MPAR_LEVELS["kappa_i_rel"] if mpar else 0.0)),
        ase_variance_scale=0.0,                    # M-noise: noiseless twin
        gain_factor=sub.gain_factor * (1.0 + (MPAR_LEVELS["gain_factor_rel"] if mpar else 0.0)),
        gain_mode=("fixed" if mstruct else "saturating"),
        input_taps=sub.input_taps, dtype=sub._dtype, seed=None)
    with torch.no_grad():
        if mpar:
            twin.gamma.mul_(1.0 + MPAR_LEVELS["gamma_rel"])
            twin.gain_model = twin.gain_model._replace(
                P_sat_W=twin.gain_model.P_sat_W * (1.0 + MPAR_LEVELS["p_sat_rel"]))
        else:
            twin.gamma.copy_(sub.gamma)
    # Unbind the trainable parameters: delete the nn.Parameters so plain
    # (autograd-tracking) tensors can be assigned per step by bind_command.
    del twin.delta, twin.kappa_ext, twin.mu_chain
    twin._family = family
    twin._mpar = mpar
    return twin


def bind_command(twin: DissipativeRingSubstrate,
                 sub: DissipativeRingSubstrate) -> None:
    """Re-bind the twin's trainable attributes to expressions of the
    substrate's live nn.Parameters (the commanded values), applying the
    frozen actuation-map errors for M-par families. Twin forward gradients
    then flow to the substrate's parameters."""
    if twin._mpar:
        ki = float(sub.kappa_i)
        twin.delta = sub.delta + MPAR_LEVELS["delta_offset_ki"] * ki
        twin.kappa_ext = sub.kappa_ext * MPAR_LEVELS["kext_actuation"]
        twin.mu_chain = sub.mu_chain * MPAR_LEVELS["mu_actuation"]
    else:
        twin.delta = sub.delta
        twin.kappa_ext = sub.kappa_ext
        twin.mu_chain = sub.mu_chain


class PATEstimator:
    """Physical forward / twin backward on the shared substrate.

    step(u, loss_fn) -> (loss_value, y_phys):
      * physical forward (registered ASE, fresh generator per pass — PR-11)
        with NO autograd on the substrate;
      * twin forward at the commanded parameters (noiseless);
      * loss on y_pat = y_phys + (y_twin − y_twin.detach()); backward fills
        substrate-parameter grads via the twin Jacobian.
    The caller owns the optimizer step + clamp (harness). Ledgers per PR-7.
    """

    def __init__(self, sub: DissipativeRingSubstrate, family: str = "both"):
        self.sub = sub
        self.family = family
        self.twin = build_twin(sub, family)
        self.n_device_passes = 0          # PR-7 primary (physical) ledger
        self.n_digital_passes = 0         # twin fwd+bwd side-ledger

    def forward_physical(self, u: torch.Tensor,
                         generator: Optional[torch.Generator] = None
                         ) -> torch.Tensor:
        """Measured R2 intensity trace, no autograd (a device measurement)."""
        with torch.no_grad():
            y = self.sub.forward_intensity(u, generator=generator)
        batch = u.shape[0] if u.ndim == 3 else 1
        self.n_device_passes += batch
        return y

    def step(self, u: torch.Tensor, loss_fn,
             generator: Optional[torch.Generator] = None):
        """One PAT gradient evaluation: fills .grad on the substrate's
        in-situ parameters {δ, κ_ext, μ}. Returns (loss, y_phys)."""
        y_phys = self.forward_physical(u, generator=generator)
        bind_command(self.twin, self.sub)
        y_twin = self.twin.forward_intensity(u)          # noiseless, autograd
        y_pat = y_phys + (y_twin - y_twin.detach())
        loss = loss_fn(y_pat)
        loss.backward()
        batch = u.shape[0] if u.ndim == 3 else 1
        self.n_digital_passes += 2 * batch               # twin fwd + bwd
        return float(loss.detach()), y_phys
