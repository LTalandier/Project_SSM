# NEW (task S0.1, deliverable 1) — not salvage. The salvaged
# static_rings.py holds the *steady-state/CW* (memoryless) transfer
# functions; this module holds the *dynamical* temporal coupled-mode
# (CMT) single-ring model whose pole IS the recurrence. The recon
# (shared/tooling_recon.md) established that pnn-multilayer has no
# temporal CMT ring code — the SSM core is new under either salvage
# ruling — so nothing here carries a provenance header.
"""Dynamical single-ring temporal coupled-mode (CMT) model — proposal §3.

The intracavity field amplitude a(t) (|a|^2 = stored energy) obeys

    da/dt = (i*Delta - kappa_tot) * a  +  sqrt(2*kappa_ext1) * s_in(t)

with the single Laplace-domain pole

    s_pole = -kappa_tot + i*Delta          (proposal §3: -kappa_tot + i*omega_res)

identified with the SSM/oscillator eigenvalue a_i = -exp(alpha_i) + i*beta_i:

    exp(alpha_i) = kappa_tot   (damping magnitude, real part),
    beta_i       = Delta       (oscillation frequency, imaginary part).

This is the temporal recurrence the salvaged `static_rings` transfer
functions are the CW limit of — the S0.1 gate verifies that limit.

Conventions (Haus energy-amplitude CMT):
  * Delta = omega_drive - omega_res  [rad/s], the detuning of the drive
    (or, in baseband, the per-ring resonance offset that sets beta_i).
  * kappa_i   = omega0 / (2*Qi)       intrinsic amplitude decay rate;
  * kappa_ext = omega0 / (2*Qext)     bus coupling amplitude decay rate;
  * kappa_tot = kappa_i + kappa_ext1 (+ kappa_ext2 for add-drop) - g_amp,
    where g_amp is an optional net amplitude gain rate (proposal §7;
    realized only as a free knob here, full ASE physics is S0.3).
  * Energy-conserving input/output (the factor sqrt(2*kappa_ext) is the
    standard Haus coupling; the proposal's schematic "sqrt(kappa_ext)
    s_in" uses kappa_ext for the *energy* rate 2*kappa_ext — same model,
    factor-2 naming only). Verified by the lossless all-pass |t| = 1
    identity below and by the S0.1 CW-limit test.

Ports:
  * all-pass / single-bus:   kappa_ext2 = 0, only a through port.
  * add-drop (two coupler):  kappa_ext1 (input bus) + kappa_ext2 (drop bus).

CW (steady-state) limit. Driving s_in = S e^{i*omega t}, da/dt -> 0 gives
a_ss = sqrt(2*kappa_ext1) S / (kappa_tot - i*Delta) and the port transfers
below. As ring finesse -> infinity these recover the salvaged
`single_bus_through` / `add_drop_through` / `add_drop_drop` exactly, up to
the documented overall -1 phase convention (T_salvaged ~ -t_cmt). The
S0.1 gate (`tests/test_single_ring_cmt.py`) pins this with O(1/finesse)
convergence.
"""

from __future__ import annotations

import math

import torch

# Reference optical carrier (C-band, 1550 nm) — matches platforms.py /
# static_rings.py (_LAMBDA_REF_M).
_C_M_PER_S = 2.99792458e8
_LAMBDA_REF_M = 1550e-9
F0_HZ = _C_M_PER_S / _LAMBDA_REF_M          # ~1.9341e14 Hz
OMEGA0_RAD_S = 2.0 * math.pi * F0_HZ        # ~1.2153e15 rad/s


# ---------------------------------------------------------------------- #
#  Rate <-> Q and discrete-ring parameter mappings (proposal §3)
# ---------------------------------------------------------------------- #

def kappa_from_Q(Q: float, f0_Hz: float = F0_HZ) -> float:
    """Amplitude decay rate kappa = omega0 / (2 Q)  [rad/s] for a (loaded
    or intrinsic) quality factor Q. The energy decays at 2*kappa; the
    power-FWHM linewidth is 2*kappa [rad/s] = f0/Q [Hz]."""
    return math.pi * f0_Hz / Q


def Q_from_kappa(kappa: float, f0_Hz: float = F0_HZ) -> float:
    """Inverse of `kappa_from_Q`: Q = omega0 / (2 kappa) = pi f0 / kappa."""
    return math.pi * f0_Hz / kappa


def tau_round_trip_s(FSR_Hz: float) -> float:
    """Cavity round-trip time tau = 1 / FSR  [s] (FSR = c / (n_g L))."""
    return 1.0 / FSR_Hz


def kappa_from_ring_amplitudes(a: float, t: float, FSR_Hz: float
                               ) -> tuple[float, float]:
    """Map a discrete-ring (round-trip amplitude a, through-coupler
    amplitude t) onto CMT amplitude rates (kappa_i, kappa_ext).

    Energy lost per round trip: intrinsic 1 - a^2, coupler 1 - t^2;
    energy decay *rate* = (loss fraction)/tau = 2*kappa, so

        kappa_i   = (1 - a^2) / (2 tau),
        kappa_ext = (1 - t^2) / (2 tau),   tau = 1/FSR.

    High-finesse (a, t -> 1) is where the CMT pole approximates the exact
    ring transfer; the S0.1 gate sweeps finesse and checks O(1/F)
    convergence.
    """
    tau = tau_round_trip_s(FSR_Hz)
    kappa_i = (1.0 - a * a) / (2.0 * tau)
    kappa_ext = (1.0 - t * t) / (2.0 * tau)
    return kappa_i, kappa_ext


def finesse(kappa_tot: float, FSR_Hz: float) -> float:
    """Ring finesse F = FSR / FWHM = pi*FSR / (kappa_tot/pi)  ... i.e.
    F = pi / (kappa_tot * tau) with tau = 1/FSR (FWHM_power = 2*kappa_tot
    [rad/s] = kappa_tot/pi [Hz]). High F => CMT ~ exact ring."""
    return math.pi * FSR_Hz / kappa_tot


# ---------------------------------------------------------------------- #
#  Pole
# ---------------------------------------------------------------------- #

def single_ring_pole(delta: float, kappa_i: float, kappa_ext1: float,
                     kappa_ext2: float = 0.0, g_amp: float = 0.0
                     ) -> complex:
    """Complex Laplace pole s = -kappa_tot + i*Delta of one ring, with
    kappa_tot = kappa_i + kappa_ext1 + kappa_ext2 - g_amp (net amplitude
    decay; g_amp is the optional net gain rate, proposal §7). Marginal
    (lossless / gain-compensated) when kappa_tot -> 0."""
    kappa_tot = kappa_i + kappa_ext1 + kappa_ext2 - g_amp
    return complex(-kappa_tot, delta)


def pole_to_eigenvalue(s_pole: complex) -> tuple[float, float]:
    """Identify a ring pole s = -kappa_tot + i*Delta with the oscillator
    eigenvalue a_i = -exp(alpha_i) + i*beta_i (proposal §3). Returns
    (alpha_i, beta_i) with exp(alpha_i) = kappa_tot, beta_i = Delta.
    Requires kappa_tot > 0 (a dissipative pole)."""
    kappa_tot = -s_pole.real
    if kappa_tot <= 0.0:
        raise ValueError(
            f"non-dissipative pole (kappa_tot={kappa_tot:.3e} <= 0): "
            "the -exp(alpha) parametrization requires a damped pole.")
    return math.log(kappa_tot), s_pole.imag


# ---------------------------------------------------------------------- #
#  CW (steady-state) port transfers — the dynamical model's CW limit.
#  These are written from the SAME CMT model and the S0.1 gate checks
#  they match the salvaged static_rings references (the CW limit).
# ---------------------------------------------------------------------- #

def cw_through(delta, kappa_i: float, kappa_ext1: float,
               kappa_ext2: float = 0.0, g_amp: float = 0.0):
    """CW through-port transfer t(Delta) = 1 - 2*kappa_ext1/(kappa_tot - i*Delta).

    All-pass (kappa_ext2 = 0): lossless (kappa_i = g = 0) gives |t| = 1;
    critical coupling (kappa_i = kappa_ext1) gives t(0) = 0. Recovers the
    salvaged `single_bus_through` magnitude in the high-finesse limit (up
    to the overall -1 phase convention).
    """
    delta = torch.as_tensor(delta, dtype=torch.float64)
    kappa_tot = kappa_i + kappa_ext1 + kappa_ext2 - g_amp
    den = kappa_tot - 1j * delta.to(torch.complex128)
    return 1.0 - (2.0 * kappa_ext1) / den


def cw_drop(delta, kappa_i: float, kappa_ext1: float, kappa_ext2: float,
            g_amp: float = 0.0):
    """CW drop-port transfer t_d(Delta) = 2*sqrt(kappa_ext1*kappa_ext2) /
    (kappa_tot - i*Delta). Lossless symmetric add-drop (kappa_i = g = 0,
    kappa_ext1 = kappa_ext2) gives t_d(0) = 1 (full drop on resonance) and
    |t_through|^2 + |t_drop|^2 = 1. Recovers salvaged `add_drop_drop`."""
    delta = torch.as_tensor(delta, dtype=torch.float64)
    kappa_tot = kappa_i + kappa_ext1 + kappa_ext2 - g_amp
    den = kappa_tot - 1j * delta.to(torch.complex128)
    return (2.0 * math.sqrt(kappa_ext1 * kappa_ext2)) / den
