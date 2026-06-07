# salvaged from pnn-multilayer @ e2eec80 : channels/mrr_primitives.py
#   (the static Lorentzian transfer math of CascadedMRR_RC._ring_transfer /
#    FCDRingActivation._through_port_transmission, re-housed as pure
#    functions; and BaseMRR.drift_inject's pm/K -> dimensionless
#    conversion + seeded sampling, re-housed as pure functions)
# Adaptations for Project_SSM (task S0.0, deliverable 2):
#   - de-classed: the source put these inside nn.Module subclasses wired
#     to the equalization stack; here they are pure torch functions
#     (their new role is CW-limit *test references* + the S0.3 drift
#     knob, not trainable layers);
#   - NEW (not salvage, marked below): the two-coupler ADD-DROP analytic
#     transfer functions — the textbook CW references the S0.0 smoke
#     test checks the salvaged form against, and the S0.1 dynamical
#     model's CW limit must reproduce.
"""Static (CW, steady-state) ring transfer functions + thermo-optic drift.

ROLE BOUNDARY — read this first. Everything in this module is
*memoryless*: a ring evaluated at a fixed detuning under CW
illumination. These are the correct physics when symbol rate <<
linewidth, and they are exactly what the SSM core must NOT be built
from (the recurrence needs the temporal CMT pole, S0.1). They live here
as (i) unit-test references — the S0.1 dynamical model's CW limit must
reproduce them — and (ii) the S0.3 drift-injection knob.

Conventions:
  * `single_bus_through` is the SALVAGED Madsen-convention single-bus
    (all-pass) form:  T(delta) = (a*e^{j*delta} - t) / (1 - a*t*e^{j*delta}).
    At delta=0, a=t (critical coupling): T = 0 (full extinction);
    a=1 (lossless): |T| = 1 for all delta (all-pass).
  * `add_drop_through` / `add_drop_drop` are the NEW two-coupler
    add-drop references (Bogaerts et al., Laser Photon. Rev. 6, 47
    (2012) conventions). The single-bus form is the kappa2 -> 0
    (t2 -> 1) limit of the add-drop through port UP TO an overall -1
    (phase-reference convention):
        add_drop_through(phi, t1, t2=1, a) == -single_bus_through(phi, t1, a)
    Magnitudes agree exactly; the smoke test pins this identity.
  * delta / phi is the round-trip phase detuning (radians); one FSR = 2*pi.
  * t_i = sqrt(1 - kappa_i^2) for a lossless coupler with field coupling
    kappa_i; a = round-trip field amplitude (1 = lossless).
"""

from __future__ import annotations

import math

import torch


# Speed of light + reference wavelength used for thermo-optic drift
# unit conversion. Wavelength fixed at 1550 nm for the C-band (same
# convention as the source repo and `platforms._LAMBDA_REF_M`).
_C_M_PER_S = 2.99792458e8
_LAMBDA_REF_M = 1550e-9


# ---------------------------------------------------------------------- #
#  Coupler helper
# ---------------------------------------------------------------------- #

def t_from_kappa(kappa: float) -> float:
    """Lossless-coupler through amplitude t = sqrt(1 - kappa^2)."""
    return math.sqrt(max(0.0, 1.0 - kappa * kappa))


# ---------------------------------------------------------------------- #
#  SALVAGED: single-bus (all-pass) through-port Lorentzian
# ---------------------------------------------------------------------- #

def single_bus_through(delta: torch.Tensor, t: float,
                       a: float = 1.0) -> torch.Tensor:
    """Single-bus through-port complex transfer (Madsen convention):

        T(delta) = (a*e^{j*delta} - t) / (1 - a*t*e^{j*delta})

    delta: real tensor of any shape (round-trip phase detuning, rad);
    t: through-coupler field amplitude; a: round-trip field amplitude.
    Returns a complex tensor of the same shape.

    (Source: CascadedMRR_RC._ring_transfer with a=1 and
    FCDRingActivation._through_port_transmission with a=t=0.95; unified
    here with both knobs exposed.)
    """
    delta = torch.as_tensor(delta)
    phase = torch.exp(1j * delta.to(torch.complex128))
    num = a * phase - t
    den = 1.0 - a * t * phase
    return num / den


def cascade_through(delta: torch.Tensor, kappas, a: float = 1.0
                    ) -> torch.Tensor:
    """Series cascade of single-bus rings sharing the same detuning:
    T_total(delta) = prod_i T_i(delta) with t_i = sqrt(1 - kappa_i^2).

    (Source: CascadedMRR_RC.forward's series composition, de-classed.)
    """
    delta = torch.as_tensor(delta)
    T = torch.ones_like(delta.to(torch.complex128))
    for kappa in kappas:
        T = T * single_bus_through(delta, t_from_kappa(float(kappa)), a)
    return T


# ---------------------------------------------------------------------- #
#  NEW (S0.0, test reference — not salvage): two-coupler add-drop ring
# ---------------------------------------------------------------------- #

def add_drop_through(phi: torch.Tensor, t1: float, t2: float,
                     a: float = 1.0) -> torch.Tensor:
    """Add-drop THROUGH-port complex transfer (Bogaerts 2012 convention):

        T_t(phi) = (t1 - t2*a*e^{j*phi}) / (1 - t1*t2*a*e^{j*phi})

    t1, t2: input/drop coupler through amplitudes; a: FULL round-trip
    field amplitude. Critical coupling (t1 = t2*a) gives T_t(0) = 0.
    """
    phi = torch.as_tensor(phi)
    phase = torch.exp(1j * phi.to(torch.complex128))
    num = t1 - t2 * a * phase
    den = 1.0 - t1 * t2 * a * phase
    return num / den


def add_drop_drop(phi: torch.Tensor, t1: float, t2: float,
                  a: float = 1.0) -> torch.Tensor:
    """Add-drop DROP-port complex transfer (Bogaerts 2012 convention):

        T_d(phi) = -kappa1*kappa2*sqrt(a)*e^{j*phi/2}
                   / (1 - t1*t2*a*e^{j*phi})

    with kappa_i = sqrt(1 - t_i^2). The sqrt(a)*e^{j*phi/2} factor is the
    half-round-trip from input coupler to drop coupler. Lossless (a=1):
    |T_t|^2 + |T_d|^2 = 1 exactly (checked by the unit tests).
    """
    phi = torch.as_tensor(phi)
    kappa1 = math.sqrt(max(0.0, 1.0 - t1 * t1))
    kappa2 = math.sqrt(max(0.0, 1.0 - t2 * t2))
    half_trip = math.sqrt(a) * torch.exp(1j * phi.to(torch.complex128) / 2.0)
    den = 1.0 - t1 * t2 * a * torch.exp(1j * phi.to(torch.complex128))
    return -(kappa1 * kappa2) * half_trip / den


# ---------------------------------------------------------------------- #
#  SALVAGED: thermo-optic drift conversion + seeded per-ring sampling
# ---------------------------------------------------------------------- #

def drift_sigma_dimensionless(sigma_pm_per_K: float, FSR_GHz: float,
                              delta_T_K: float = 1.0) -> float:
    """pm/K -> dimensionless (fraction-of-FSR) drift std conversion:

        sigma_lambda [m]  = sigma_pm_per_K * 1e-12 * delta_T_K
        sigma_f [Hz]      = sigma_lambda * c / lambda_ref^2
        sigma_dim         = sigma_f / FSR_Hz

    (Source: BaseMRR.drift_inject, Critic-audited conversion.)
    """
    sigma_lambda_m = sigma_pm_per_K * 1e-12 * delta_T_K
    sigma_f_Hz = sigma_lambda_m * _C_M_PER_S / (_LAMBDA_REF_M ** 2)
    return sigma_f_Hz / (FSR_GHz * 1e9)


def sample_drift(N: int, sigma_pm_per_K: float, FSR_GHz: float,
                 seed: int = 0, delta_T_K: float = 1.0
                 ) -> tuple[torch.Tensor, torch.Tensor]:
    """Sample per-ring thermo-optic detuning drift.

    Returns (drift_dim, drift_phase):
        drift_dim   [N] — dimensionless (fractions of one FSR), Gaussian
                          with std = drift_sigma_dimensionless(...)
        drift_phase [N] — 2*pi * drift_dim (radians), ready to add to a
                          ring's round-trip phase detuning.

    Seeded and deterministic: same (N, sigma, FSR, seed, delta_T) ->
    bit-identical sample. sigma_pm_per_K = 0 -> exact zeros (the
    zero-drift path stays bit-identical to no-drift).

    (Source: BaseMRR.drift_inject, de-classed; the S0.3 substrate
    applies drift_phase to its ring detunings.)
    """
    sigma_dim = drift_sigma_dimensionless(sigma_pm_per_K, FSR_GHz, delta_T_K)
    gen = torch.Generator().manual_seed(int(seed))
    sample = torch.randn(N, generator=gen)
    drift_dim = sigma_dim * sample
    drift_phase = 2.0 * math.pi * drift_dim
    return drift_dim, drift_phase
