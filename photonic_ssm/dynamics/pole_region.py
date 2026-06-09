# NEW (task S0.1, deliverables 3, 5-compute, 6) — not salvage. Pure
# analysis kernels for the realizable pole region (proposal §4): the
# loss/gain -> |lambda| memory relation, the kappa_ext memory-vs-readout
# trade (B3), and the backscatter mode-splitting crossover (B2).
"""Realizable pole-region bounds (proposal §4).

Stability is free (passive rings give |lambda| < 1); the binding limits
are: memory is **loss-limited** (min damping = intrinsic loss), beta is
**FSR-bounded**, and the readable region is set by the **kappa_ext
policy**. These pure functions produce the numbers the S0.1 plots and the
B2/B3 memos cite; the analysis script `analysis/s0_1_pole_region.py`
renders them.

All rates are amplitude decay rates [rad/s]; kappa_i = omega0/(2 Qi).
"""

from __future__ import annotations

import math

import torch

from .single_ring import F0_HZ, OMEGA0_RAD_S, kappa_from_Q


# ---------------------------------------------------------------------- #
#  Memory length / |lambda| vs loss & gain  (deliverable 3)
# ---------------------------------------------------------------------- #

def photon_lifetime_s(Qi: float, f0_Hz: float = F0_HZ) -> float:
    """Energy (1/e) photon lifetime tau_ph = Qi/omega0 = Qi/(2 pi f0) [s].
    The amplitude memory time is 2*tau_ph = 1/kappa_i."""
    return Qi / (2.0 * math.pi * f0_Hz)


def loss_limited_memory_time_s(Qi: float, f0_Hz: float = F0_HZ) -> float:
    """Maximum *passive* amplitude memory time = 1/kappa_i = 2 Qi/omega0
    [s] (no external coupling, no gain). This is the loss-limited ceiling
    of proposal §4: the lowest-loss platform (largest Qi) maximizes
    passive memory."""
    return 1.0 / kappa_from_Q(Qi, f0_Hz)


def net_kappa_tot(kappa_i: float, kappa_ext: float = 0.0,
                  g_amp: float = 0.0) -> float:
    """Net amplitude decay kappa_tot = kappa_i + kappa_ext - g_amp. Gain
    (proposal §7) reduces net loss; kappa_tot -> 0 is the marginal
    (non-fading-memory / lasing-threshold) limit."""
    return kappa_i + kappa_ext - g_amp


def discrete_pole_magnitude(kappa_tot: float, dt: float) -> float:
    """|lambda| = |exp(lambda*dt)| = exp(-kappa_tot*dt): per-step memory
    retention. |lambda| -> 1 (kappa_tot*dt -> 0) is long memory."""
    return math.exp(-kappa_tot * dt)


def memory_length_samples(kappa_tot: float, dt: float) -> float:
    """1/e amplitude memory length in samples = 1/(kappa_tot*dt). With the
    step dt = round-trip time this is roughly the cavity photon lifetime
    in round trips (the finesse/2pi)."""
    return 1.0 / (kappa_tot * dt)


def gain_for_target_memory(kappa_i: float, kappa_ext: float,
                           target_memory_time_s: float) -> float:
    """Net amplitude gain g_amp needed to reach a target memory time
    1/kappa_tot. g = kappa_i + kappa_ext - 1/target. Negative => target is
    reachable passively; g >= kappa_i+kappa_ext is past threshold
    (unstable) — flagged by the caller."""
    return kappa_i + kappa_ext - 1.0 / target_memory_time_s


# ---------------------------------------------------------------------- #
#  Memory-vs-readout-SNR (kappa_ext) trade  (deliverable 6 / B3)
# ---------------------------------------------------------------------- #

def io_residue(kappa_ext1: float, kappa_ext2: float | None = None) -> float:
    """SSM residue scale |c_j b_j| of the ring's contribution to H(s).
    Input/output couple as b_j = sqrt(2 kappa_ext1), c_j = sqrt(2
    kappa_ext2) (drop bus) or sqrt(2 kappa_ext1) (same bus), so the
    residue ~ 2 sqrt(kappa_ext1*kappa_ext2). Deep undercoupling
    (kappa_ext -> 0) collapses the residue -> the kernel amplitude / the
    readable signal vanishes."""
    if kappa_ext2 is None:
        kappa_ext2 = kappa_ext1
    return 2.0 * math.sqrt(kappa_ext1 * kappa_ext2)


def drop_efficiency_on_resonance(kappa_i: float, kappa_ext1: float,
                                 kappa_ext2: float, g_amp: float = 0.0
                                 ) -> float:
    """On-resonance drop-port power transmission |t_drop(0)|^2 =
    (2 sqrt(k1 k2)/kappa_tot)^2 — the fraction of input power delivered to
    the readout. Lossless symmetric add-drop (kappa_i=g=0, k1=k2) -> 1.
    A direct proxy for detector-arm signal power, hence shot/thermal
    detector SNR (SNR ~ this * P_in / noise)."""
    kappa_tot = kappa_i + kappa_ext1 + kappa_ext2 - g_amp
    return (2.0 * math.sqrt(kappa_ext1 * kappa_ext2) / kappa_tot) ** 2


def kappa_ext_trade_sweep(Qi: float, ratios, dt: float,
                          f0_Hz: float = F0_HZ):
    """Sweep symmetric add-drop coupling kappa_ext = ratio * kappa_i over
    `ratios` and return parallel tensors of the memory/readout trade
    (deliverable 6 / B3). kappa_ext1 = kappa_ext2 = kappa_ext.

    Returns dict of 1-D tensors:
      ratio              kappa_ext/kappa_i
      memory_samples     1/(kappa_tot*dt)
      pole_magnitude     exp(-kappa_tot*dt)
      residue            2*kappa_ext  (normalized to kappa_i below)
      residue_norm       residue/kappa_i  (-> 0 undercoupled, ->large over)
      drop_efficiency    on-resonance drop power (detector SNR proxy)
      mem_x_residue      memory_samples * residue_norm (the bounded product
                         showing you cannot maximize both)
    """
    kappa_i = kappa_from_Q(Qi, f0_Hz)
    r = torch.as_tensor(ratios, dtype=torch.float64)
    kext = r * kappa_i
    kappa_tot = kappa_i + 2.0 * kext            # symmetric add-drop
    mem = 1.0 / (kappa_tot * dt)
    polemag = torch.exp(-kappa_tot * dt)
    residue = 2.0 * kext
    residue_norm = residue / kappa_i
    drop_eff = (2.0 * kext / kappa_tot) ** 2
    return {
        "ratio": r,
        "kappa_i": kappa_i,
        "memory_samples": mem,
        "pole_magnitude": polemag,
        "residue": residue,
        "residue_norm": residue_norm,
        "drop_efficiency": drop_eff,
        "mem_x_residue": mem * residue_norm,
    }


# ---------------------------------------------------------------------- #
#  Backscatter / CW-CCW mode-splitting crossover  (deliverable 5 / B2)
# ---------------------------------------------------------------------- #
#  Criterion (literature-sourced, see docs/s0_1/B2_backscatter_bound.md):
#  a resonance resolves into a CW/CCW doublet when the coherent back-
#  coupling 2*gamma exceeds the (intrinsic) linewidth kappa_tot, i.e.
#  2*gamma >= kappa_i in the undercoupled worst case. gamma is set by
#  fabrication roughness (an absolute rate), essentially independent of
#  kappa_tot — so as Qi rises (kappa_i falls) a fixed gamma becomes an
#  ever larger fraction of the linewidth: splitting GROWS with Q.
#  This is the conservative HWHM criterion (kappa_tot is the half-width);
#  the fully-resolved FWHM criterion 2*gamma >= 2*kappa_tot needs twice
#  gamma, so every crossover_Q shifts x2. crossover_Q() below uses the
#  HWHM (2*gamma = kappa_tot) form; double it for the FWHM band.

def gamma_rad_s_from_MHz_linear(split_MHz_2gamma: float) -> float:
    """Convert a reported *splitting* 2*gamma/2pi [MHz] (the measured
    doublet peak separation in linear-frequency units) to the back-
    coupling rate gamma [rad/s]: gamma = 2*pi*(split_MHz/2)*1e6."""
    return 2.0 * math.pi * (split_MHz_2gamma / 2.0) * 1e6


def splitting_linewidth_ratio(gamma_rad_s: float, Qi: float,
                              kappa_ext: float = 0.0,
                              f0_Hz: float = F0_HZ) -> float:
    """2*gamma / kappa_tot with kappa_tot = kappa_i + kappa_ext. >= 1 =>
    the doublet is resolved and 'one ring = one complex pole' fails; the
    ring is two hybridized standing-wave modes. Undercoupled (kappa_ext=0)
    is the worst case (narrowest linewidth)."""
    kappa_tot = kappa_from_Q(Qi, f0_Hz) + kappa_ext
    return 2.0 * gamma_rad_s / kappa_tot


def crossover_Q(gamma_rad_s: float, kappa_ext: float = 0.0,
                f0_Hz: float = F0_HZ) -> float:
    """Intrinsic Q at which 2*gamma = kappa_tot (the splitting crossover).
    Solving 2*gamma = omega0/(2 Q) + kappa_ext for Q:
        Q_cross = omega0 / (2*(2*gamma - kappa_ext)).
    Above Q_cross the resonance splits. Returns +inf if backscatter never
    dominates (2*gamma <= kappa_ext, i.e. coupling already broadens past
    the splitting)."""
    denom = 2.0 * gamma_rad_s - kappa_ext
    if denom <= 0.0:
        return math.inf
    return OMEGA0_RAD_S / (2.0 * denom)
