# salvaged from pnn-multilayer @ e2eec80 : physics.py (lines ~57-136)
# Adaptations for Project_SSM (task S0.0, deliverable 2):
#   - lifted ONLY the gain/noise/NL primitives (the MZI mesh machinery
#     stays shelved in pnn-multilayer per recon §1.5);
#   - `soa_activation_with_ase` gained an optional `generator=` kwarg so
#     ASE draws can be seeded (project reproducibility rule); default
#     None reproduces the original global-RNG behavior exactly;
#   - docstrings re-pointed at the S0.3 substrate role.
# Function bodies are otherwise unchanged.
"""Instantaneous (memoryless) gain, ASE and nonlinearity primitives.

S0.3 substrate role: these are the *memoryless-limit* gain and ASE
knobs, applied per round trip inside the ring recurrence (not per
symbol between feedforward layers as in the source repo). The
carrier-dynamics tier lives in `dynamic_gain.py`; the per-round-trip
ASE *accumulation* model is new S0.3 physics built on
`soa_activation_with_ase`'s scaling.

All functions are torch-only, phase-preserving where stated, and safe
inside an autograd graph (no `no_grad`, no `detach` — architecture
constraint (3a)).
"""

from __future__ import annotations

import math

import torch


def photodetect(amplitudes: torch.Tensor) -> torch.Tensor:
    """Square-law detection: I = |E|^2"""
    return torch.abs(amplitudes) ** 2


def modReLU(z: torch.Tensor, bias: torch.Tensor) -> torch.Tensor:
    """modReLU(z) = (|z| + b) * z/|z| if |z| + b > 0, else 0"""
    mag = torch.abs(z)
    phase = z / (mag + 1e-8)
    return torch.relu(mag + bias) * phase


def saturating_absorption(z: torch.Tensor, alpha: torch.Tensor) -> torch.Tensor:
    """Saturating absorber: sat(z) = z / (1 + alpha*|z|^2)

    Phase-preserving, soft saturation. Models saturable absorption
    or two-photon absorption in waveguides.
    alpha: learnable saturation coefficient per port.
    """
    intensity = torch.abs(z) ** 2
    return z / (1 + alpha * intensity)


def soa_activation(z: torch.Tensor, gain: torch.Tensor,
                   alpha: torch.Tensor) -> torch.Tensor:
    """Gain saturation: f(z) = G0 * z / (1 + alpha*|z|^2)

    Phase-preserving with net gain. Models semiconductor-optical-
    amplifier-style gain saturation (Shi et al. 2022); the memoryless
    (tau_c -> 0) limit of the rate-equation model in `dynamic_gain.py`
    up to the exact saturation law (see that module's docstring).

    gain: learnable unsaturated field gain G0 per port (initialized > 1)
    alpha: learnable saturation coefficient per port
    """
    intensity = torch.abs(z) ** 2
    return gain * z / (1 + alpha * intensity)


def mzm_nonlinearity(z: torch.Tensor, drive_gain) -> torch.Tensor:
    """MZM-driven nonlinear activation: f(z) = sin(pi * z * drive_gain / 2)

    Physically a Mach-Zehnder modulator biased at quadrature with the
    signal applied to the modulation port. For small |z*drive_gain|,
    f(z) ~ (pi/2) * z * drive_gain (linear); at |z*drive_gain| = 1 the
    response saturates; beyond that it folds back.

    drive_gain is a learnable per-layer scalar (torch.Tensor, scalar or
    shape [N] for per-mode drive). Phase-preserving: operates on the
    complex amplitude without photodetection.

    Contrast with SOA: no net gain (MZM is passive), no ASE, but the
    sinusoidal response provides a strong instantaneous nonlinearity.
    """
    arg = (math.pi / 2.0) * z * drive_gain
    return torch.sin(arg)


def soa_activation_with_ase(z: torch.Tensor, gain: torch.Tensor,
                            alpha: torch.Tensor, n_sp: float = 1.5,
                            B_opt: float = 32e9,
                            generator: torch.Generator | None = None
                            ) -> torch.Tensor:
    """Gain saturation with per-element ASE noise.

    Same as soa_activation but adds per-element ASE noise proportional
    to the effective gain of each port:

        P_ase_i = n_sp * max(G_eff_i - 1, 0) * h_nu * B_opt

    where G_eff_i = |gain_i| / (1 + alpha_i * |z_i|^2) is the per-element
    effective gain, h_nu = 1.282e-19 J (photon energy at 1550 nm),
    and B_opt is the optical bandwidth per mode (Hz).

    S0.3 note: this is the per-application ASE injection; n_sp is the
    inversion factor (NF ~ 2*n_sp in the high-gain limit). The Er:SiN
    flagship device has NO published NF (verification debt #3) — the
    substrate must treat n_sp as a swept, conservatively-ranged knob.

    generator: optional seeded torch.Generator for the noise draw
    (reproducibility); None uses the global RNG (original behavior).
    The noise injection itself does not need a gradient path; the
    deterministic signal path stays autograd-safe.
    """
    h_nu = 1.282e-19  # Planck * (c / 1550nm) in Joules

    intensity = torch.abs(z) ** 2
    G_eff = torch.abs(gain) / (1 + alpha * intensity)
    out = gain * z / (1 + alpha * intensity)

    # Per-element ASE: complex Gaussian with variance P_ase/2 per component
    P_ase = n_sp * torch.clamp(G_eff - 1, min=0) * h_nu * B_opt
    noise_std = torch.sqrt(P_ase / 2 + 1e-30)
    if generator is None:
        re = torch.randn_like(z.real)
        im = torch.randn_like(z.real)
    else:
        re = torch.randn(z.real.shape, generator=generator,
                         dtype=z.real.dtype, device=z.device)
        im = torch.randn(z.real.shape, generator=generator,
                         dtype=z.real.dtype, device=z.device)
    noise = noise_std * (re + 1j * im)
    return out + noise.to(z.dtype)
