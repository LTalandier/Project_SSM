# tests for photonic_ssm/dynamics/pole_region.py (NEW S0.1 analysis).
"""Realizable pole-region bounds: loss-limited memory (deliverable 3),
the kappa_ext memory-vs-readout trade (B3), and the literature-sourced
backscatter mode-splitting crossover (B2). The B2 assertions encode the
load-bearing finding: splitting is process-roughness-limited, NOT cleanly
Q-gated."""

import math

import torch

from photonic_ssm.dynamics import (
    loss_limited_memory_time_s, photon_lifetime_s, kappa_from_Q,
    discrete_pole_magnitude, memory_length_samples, net_kappa_tot,
    gain_for_target_memory, kappa_ext_trade_sweep, crossover_Q,
    splitting_linewidth_ratio, gamma_rad_s_from_MHz_linear, OMEGA0_RAD_S,
)

FSR_HZ = 100e9
DT = 1.0 / FSR_HZ


# ---- loss-limited memory (deliverable 3) ----------------------------- #

def test_photon_lifetime_scales_with_Q():
    """tau_ph = Qi/omega0; higher Q = longer memory. Class-leading
    (3e7) gives ~15x the foundry (2e6) passive memory."""
    t_lo = loss_limited_memory_time_s(2e6)
    t_hi = loss_limited_memory_time_s(3e7)
    assert t_hi > t_lo
    assert abs((t_hi / t_lo) - 15.0) / 15.0 < 0.01     # ratio == Q ratio
    assert abs(photon_lifetime_s(2e6) - 2e6 / OMEGA0_RAD_S) < 1e-15


def test_passive_pole_magnitude_increases_with_Q():
    """|lambda|_passive = exp(-kappa_i*dt) -> 1 as Qi grows (memory)."""
    z2 = discrete_pole_magnitude(kappa_from_Q(2e6), DT)
    z30 = discrete_pole_magnitude(kappa_from_Q(3e7), DT)
    assert 0.99 < z2 < z30 < 1.0
    assert memory_length_samples(kappa_from_Q(3e7), DT) > \
        memory_length_samples(kappa_from_Q(2e6), DT)


def test_gain_extends_memory_to_threshold():
    """Net gain reduces kappa_tot; the gain needed for a target memory is
    g = kappa_i+kappa_ext-1/target, and g==kappa_i+kappa_ext is marginal."""
    ki = kappa_from_Q(2e6)
    # passive memory time
    t_passive = 1.0 / net_kappa_tot(ki)
    # to double the memory time, need positive gain < ki
    g = gain_for_target_memory(ki, 0.0, 2 * t_passive)
    assert 0.0 < g < ki
    assert net_kappa_tot(ki, 0.0, g) > 0.0              # still stable


# ---- kappa_ext memory-vs-readout trade (B3) -------------------------- #

def test_kappa_ext_trade_is_monotonic_pareto():
    """Deep undercoupling maximizes memory but collapses readout: as
    kappa_ext/kappa_i grows, memory falls and drop efficiency rises —
    a genuine trade (proposal §4 / B3 / PR-4)."""
    sw = kappa_ext_trade_sweep(2e6, [0.1, 0.3, 1.0, 3.0, 10.0], DT)
    mem = sw["memory_samples"]
    drop = sw["drop_efficiency"]
    res = sw["residue_norm"]
    # memory strictly decreasing, drop efficiency + residue strictly increasing
    assert torch.all(mem[1:] < mem[:-1])
    assert torch.all(drop[1:] > drop[:-1])
    assert torch.all(res[1:] > res[:-1])


def test_memory_times_residue_bounded_by_passive_memory():
    """memory * residue saturates at the passive memory length (you cannot
    have both maximal memory and maximal readout residue)."""
    sw = kappa_ext_trade_sweep(2e6, [0.01, 0.1, 1.0, 10.0, 100.0], DT)
    passive = memory_length_samples(kappa_from_Q(2e6), DT)
    assert torch.all(sw["mem_x_residue"] <= passive * (1.0 + 1e-9))


# ---- backscatter mode-splitting crossover (B2) ----------------------- #
#  These encode the load-bearing 'say it loudly' finding: splitting is set
#  by fabrication roughness (absolute gamma) and BITES WITHIN the registered
#  Q range for rough process, while clean process stays single-pole at
#  foundry Q but splits at the aspirational 3e7.

def test_clean_process_single_pole_at_foundry_splits_at_uhq():
    """Damascene-clean backscatter (2g/2pi ~ 23.6 MHz, Nat. Commun. 12,
    235): single-pole holds at foundry Qi=2e6 but FAILS at Qi=3e7."""
    g = gamma_rad_s_from_MHz_linear(23.6)
    assert splitting_linewidth_ratio(g, 2e6) < 1.0     # not split (0.49)
    assert splitting_linewidth_ratio(g, 3e7) > 1.0     # split (7.3)
    Qc = crossover_Q(g)
    assert 2e6 < Qc < 3e7                              # crossover in-range


def test_rough_process_splits_already_at_foundry_Q():
    """Rough subtractive SiN (2g/2pi ~ 180-250 MHz, arXiv:2511.02198)
    splits a large fraction of modes ALREADY at foundry Qi=2e6 — so
    'one ring = one pole' is NOT automatically safe at foundry Q; it is
    process-roughness-gated, not Q-gated (the B2 recommendation)."""
    for split2g in (180.0, 250.0):
        g = gamma_rad_s_from_MHz_linear(split2g)
        assert splitting_linewidth_ratio(g, 2e6) > 1.0  # already split
        assert crossover_Q(g) < 2e6                      # crosses below foundry


def test_crossover_Q_solves_2gamma_equals_kappa():
    """crossover_Q returns the Q where 2*gamma == kappa_i exactly."""
    g = gamma_rad_s_from_MHz_linear(23.6)
    Qc = crossover_Q(g)
    assert abs(splitting_linewidth_ratio(g, Qc) - 1.0) < 1e-9


def test_coupling_suppresses_visible_splitting():
    """Adding external coupling widens the linewidth and pushes the
    crossover to higher Q (overcoupling hides the doublet) — the physical
    reason a measured overcoupled device may not show splitting even when
    intrinsically split."""
    g = gamma_rad_s_from_MHz_linear(23.6)
    ki = kappa_from_Q(3e7)
    r_under = splitting_linewidth_ratio(g, 3e7, kappa_ext=0.0)
    r_over = splitting_linewidth_ratio(g, 3e7, kappa_ext=5 * ki)
    assert r_over < r_under
