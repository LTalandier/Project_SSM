# salvaged from pnn-multilayer @ e2eec80 : adaptation/perturbation_gradient.py
# Adaptations for Project_SSM (task S0.0, deliverable 2) — the two
# contact points named in the recon, decoupled:
#   1. loss function: hard-coded `compute_nmse_field` import (the fiber
#      equalization NMSE) -> injected `loss_fn(output, target)`;
#   2. forward API: hard-coded `model.forward_batched(...)` -> injected
#      `forward_fn(model, inputs)` (default `model(inputs)`).
# `step()`/`compare_fd_vs_autograd()` math, the Adam update, and the
# forward-pass accounting are unchanged.
"""Hardware-compatible perturbation-gradient estimators (S0.4a SPSA).

Two estimator variants, both using only forward passes + a scalar loss
readout (no autograd, no backprop) — i.e. both are physically realizable
on-chip, which is why SPSA is one of the two hardware-committed methods
in the Stage-0 bake-off (proposal §5.1):

1. **Per-parameter finite-difference (FD)**: for each trainable scalar
   parameter p_i, perturb by +/-eps and measure the loss change.
   Clean but cost = 2*N_params forward passes per update. Used for
   validation against autograd and as a sanity anchor.

2. **SPSA (Simultaneous Perturbation Stochastic Approximation)**: dither
   *all* parameters simultaneously with IID +/-1 signs x eps, measure
   the scalar loss change, and attribute it back to each parameter via
   the dither sign. Cost = 2 forward passes per update, regardless of
   N_params. Matches published on-chip perturbation-controller
   architectures (Pai 2019; Bandyopadhyay 2022; Hughes 2018).

`n_forward_equivalents` counts physical forward passes — this is the
bake-off's PRIMARY-metric bookkeeping (sample-efficiency-to-target-
accuracy = loss reached vs physical forward passes spent), shared by
all four estimators for the apples-to-apples comparison.

The update rule is Adam-style with decoupled step size (stored on the
optimizer, not on the model).

References
----------
- Spall JC. "An overview of the simultaneous perturbation method for
  efficient optimization." Johns Hopkins APL Technical Digest 19, 1998.
- Pai S et al. "Parallel programming of an arbitrary feedforward
  photonic network." IEEE JSTQE 2020.
- Bandyopadhyay S et al. "Single-chip photonic deep neural network with
  forward-only training." Nature Photonics 2024.
"""

from __future__ import annotations

import torch


def _default_forward(model, inputs):
    """Default forward API: the model is a callable."""
    return model(inputs)


def _get_flat_params(model):
    """Return list of (name, param) pairs for all trainable scalar params."""
    return [(n, p) for (n, p) in model.named_parameters() if p.requires_grad]


class PerturbationAdaptor:
    """Hardware-realizable perturbation-gradient optimizer.

    Exposes a uniform `.step(inputs, target)` interface.

    Estimator variants (chosen at construction):
      - 'spsa'      : 2 forward passes per update (primary)
      - 'per_param' : 2*N_params forward passes per update (validation)

    Update rule: vanilla gradient descent with learnable step size (lr).
    An Adam-style moment accumulator can be enabled via `use_adam=True`.
    """

    def __init__(self, model, loss_fn, estimator='spsa', eps=0.01, lr=1e-2,
                 use_adam=True, beta1=0.9, beta2=0.999, adam_eps=1e-8,
                 rng_seed=0, forward_fn=None):
        """
        Args:
            model: nn.Module (or anything exposing .named_parameters())
                whose trainable parameters are dithered in-place.
            loss_fn: callable (output, target) -> scalar tensor. Injected
                (decoupled contact point 1).
            estimator: 'spsa' or 'per_param'
            eps: dither magnitude — applied to all trainable params in
                their native units (e.g. rad for phases)
            lr: step size applied to the estimated gradient
            use_adam: if True, use Adam moment estimator on top of the
                perturbation-estimated gradient
            beta1, beta2, adam_eps: Adam hyperparameters
            rng_seed: seed for the SPSA Bernoulli sign generator
            forward_fn: callable (model, inputs) -> output. Injected
                (decoupled contact point 2); default `model(inputs)`.
        """
        assert estimator in ('spsa', 'per_param')
        self.model = model
        self.loss_fn = loss_fn
        self.forward_fn = forward_fn if forward_fn is not None \
            else _default_forward
        self.estimator = estimator
        self.eps = eps
        self.lr = lr
        self.use_adam = use_adam
        self.beta1 = beta1
        self.beta2 = beta2
        self.adam_eps = adam_eps

        self.params = _get_flat_params(model)
        self.n_params = sum(p.numel() for _, p in self.params)

        # Adam moments (flat, aligned with params list)
        if use_adam:
            self._m = [torch.zeros_like(p) for _, p in self.params]
            self._v = [torch.zeros_like(p) for _, p in self.params]
        self.adam_t = 0

        self._rng = torch.Generator()
        self._rng.manual_seed(int(rng_seed))

        # Fair-compute accounting: counts physical forward-pass
        # equivalents (the bake-off primary-metric bookkeeping).
        self.n_updates = 0
        self.n_forward_equivalents = 0

    def _eval_loss(self, inputs, target):
        """Single forward pass + scalar loss. No gradient."""
        with torch.no_grad():
            out = self.forward_fn(self.model, inputs)
            return float(self.loss_fn(out, target).item())

    # --- Estimator kernels ------------------------------------------------

    def _spsa_gradient(self, inputs, target):
        """SPSA: 2 forward passes, 1 scalar Delta -> full gradient estimate.

        g_i ~ (L(+) - L(-)) / (2*eps*c_i)   with  c_i in {+1, -1}
        """
        # Generate +/-1 Bernoulli dither per parameter
        signs = []
        for _, p in self.params:
            s = (torch.randint(0, 2, p.shape, generator=self._rng,
                               dtype=torch.float32) * 2.0 - 1.0)
            # Cast to param dtype (float32 always, but be safe)
            signs.append(s.to(p.dtype))

        # +eps perturbation
        with torch.no_grad():
            for (_, p), s in zip(self.params, signs):
                p.data.add_(s, alpha=self.eps)
            L_plus = self._eval_loss(inputs, target)

            # -2*eps -> net -eps perturbation
            for (_, p), s in zip(self.params, signs):
                p.data.add_(s, alpha=-2 * self.eps)
            L_minus = self._eval_loss(inputs, target)

            # Restore nominal
            for (_, p), s in zip(self.params, signs):
                p.data.add_(s, alpha=self.eps)

        delta_L = L_plus - L_minus
        # Gradient estimate: g_i = dL / (2*eps) * (1 / c_i) = dL / (2*eps*c_i)
        # Since c_i in {+1,-1}, 1/c_i = c_i. So g_i = dL * c_i / (2*eps).
        grads = [s * (delta_L / (2.0 * self.eps)) for s in signs]

        return grads, L_plus, L_minus

    def _per_param_gradient(self, inputs, target):
        """Per-parameter two-sided FD. Cost 2*N_params forward passes."""
        grads = [torch.zeros_like(p) for _, p in self.params]

        with torch.no_grad():
            # Iterate over each scalar parameter
            for p_idx, (_, p) in enumerate(self.params):
                flat = p.data.reshape(-1)
                g_flat = grads[p_idx].reshape(-1)
                for i in range(flat.numel()):
                    orig = flat[i].item()
                    flat[i] = orig + self.eps
                    L_plus = self._eval_loss(inputs, target)
                    flat[i] = orig - self.eps
                    L_minus = self._eval_loss(inputs, target)
                    flat[i] = orig
                    g_flat[i] = (L_plus - L_minus) / (2.0 * self.eps)

        # Also return nominal loss for logging
        L0 = self._eval_loss(inputs, target)
        return grads, L0, L0

    # --- Optimizer update ---------------------------------------------------

    def _apply_update(self, grads):
        """Apply lr*g (optionally Adam-scaled) to params in-place."""
        self.adam_t += 1
        with torch.no_grad():
            for i, (_, p) in enumerate(self.params):
                g = grads[i]
                if self.use_adam:
                    self._m[i].mul_(self.beta1).add_(g, alpha=1 - self.beta1)
                    self._v[i].mul_(self.beta2).addcmul_(g, g, value=1 - self.beta2)
                    m_hat = self._m[i] / (1 - self.beta1 ** self.adam_t)
                    v_hat = self._v[i] / (1 - self.beta2 ** self.adam_t)
                    step = m_hat / (v_hat.sqrt() + self.adam_eps)
                    p.data.add_(step, alpha=-self.lr)
                else:
                    p.data.add_(g, alpha=-self.lr)

    def step(self, inputs, target):
        """One adaptation step. Returns the loss measured at the probes."""
        if self.estimator == 'spsa':
            grads, L_plus, L_minus = self._spsa_gradient(inputs, target)
            loss_sample = 0.5 * (L_plus + L_minus)
            self.n_forward_equivalents += 2
        else:
            grads, L0, _ = self._per_param_gradient(inputs, target)
            loss_sample = L0
            self.n_forward_equivalents += 2 * self.n_params + 1

        self._apply_update(grads)
        self.n_updates += 1
        return loss_sample

    # --- Utilities ------------------------------------------------------------

    def current_params_vector(self):
        return torch.cat([p.detach().reshape(-1) for _, p in self.params])


# ---------------------------------------------------------------------- #
#  Validation: FD vs autograd
#  (also the template for the bake-off's SECONDARY diagnostic — gradient
#   cosine error vs a BPTT reference; never the headline metric)
# ---------------------------------------------------------------------- #

def compare_fd_vs_autograd(model, inputs, target, loss_fn, eps=1e-3,
                           forward_fn=None):
    """Compare per-parameter finite-difference gradient against autograd.

    Returns (fd_vec, autograd_vec, rms_relative_error).

    RMS relative error = sqrt(mean((g_fd - g_ag)^2)) / sqrt(mean(g_ag^2))
    Anchor (inherited from the source repo's G3 gate): < 0.01 (1%) on a
    static, noiseless model.
    """
    if forward_fn is None:
        forward_fn = _default_forward
    params = _get_flat_params(model)

    # Autograd gradient
    for _, p in params:
        if p.grad is not None:
            p.grad.zero_()
    out = forward_fn(model, inputs)
    loss = loss_fn(out, target)
    loss.backward()
    ag_flat = torch.cat([p.grad.detach().reshape(-1) for _, p in params]).clone()
    for _, p in params:
        if p.grad is not None:
            p.grad.zero_()

    # FD gradient
    fd_flat = torch.zeros_like(ag_flat)
    idx = 0
    with torch.no_grad():
        for _, p in params:
            flat = p.data.reshape(-1)
            for i in range(flat.numel()):
                orig = flat[i].item()
                flat[i] = orig + eps
                out_p = forward_fn(model, inputs)
                L_p = loss_fn(out_p, target).item()
                flat[i] = orig - eps
                out_m = forward_fn(model, inputs)
                L_m = loss_fn(out_m, target).item()
                flat[i] = orig
                fd_flat[idx] = (L_p - L_m) / (2.0 * eps)
                idx += 1

    # RMS relative error
    num = torch.sqrt(torch.mean((fd_flat - ag_flat) ** 2)).item()
    denom = torch.sqrt(torch.mean(ag_flat ** 2)).item() + 1e-30
    rms_rel = num / denom
    return fd_flat, ag_flat, rms_rel
