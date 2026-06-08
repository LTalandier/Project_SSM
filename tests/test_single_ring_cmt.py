# tests for photonic_ssm/dynamics/single_ring.py (NEW S0.1 core).
"""S0.1 GATE — the dynamical temporal-CMT single ring's CW (steady-state)
limit must recover the S0.0 salvaged static references.

Pre-registered tolerance (stated before the run): in the high-finesse
regime the CMT CW transfer matches the exact ring transfer
(static_rings.single_bus_through / add_drop_through / add_drop_drop) with
a max relative magnitude error that scales as O(1/finesse); at finesse
>= 1000 (the registry's SiN rings: F ~ 1000 at Qi=2e6 ... ~15000 at
Qi=3e7, FSR=100 GHz) the error is < 1e-2 over a +-5-linewidth window, and
falls ~10x per 10x finesse. The CMT through-port equals MINUS the
salvaged single-bus form (the documented -1 phase convention).
"""

import math

import torch

from photonic_ssm.dynamics import (
    cw_through, cw_drop, kappa_from_ring_amplitudes, tau_round_trip_s,
    finesse, single_ring_pole, pole_to_eigenvalue, kappa_from_Q, Q_from_kappa,
)
from photonic_ssm.static_rings import (
    single_bus_through, add_drop_through, add_drop_drop,
)

FSR_HZ = 100e9
GATE_TOL = 1e-2          # pre-registered: < 1% at finesse >= 1000
F0_HZ = 2.99792458e8 / 1550e-9


def _window(kappa_tot, n=401, span=5.0):
    return torch.linspace(-span * kappa_tot, span * kappa_tot, n)


def test_cw_limit_recovers_single_bus_through():
    """All-pass CMT |t(Delta)| == salvaged single_bus_through magnitude at
    high finesse (the gate), and t_cmt == -single_bus_through (phase)."""
    a, t = 0.999, 0.998
    ki, ke = kappa_from_ring_amplitudes(a, t, FSR_HZ)
    ktot = ki + ke
    assert finesse(ktot, FSR_HZ) > 1000.0
    tau = tau_round_trip_s(FSR_HZ)
    delta = _window(ktot)
    T_cmt = cw_through(delta, ki, ke)
    T_exact = single_bus_through(delta * tau, t, a)
    assert (T_cmt.abs() - T_exact.abs()).abs().max().item() < GATE_TOL
    # -1 phase convention: T_cmt == -T_exact
    assert (T_cmt - (-T_exact)).abs().max().item() < GATE_TOL


def test_cw_limit_convergence_is_order_one_over_finesse():
    """Error falls ~10x per 10x finesse (confirms CMT is the high-finesse
    limit of the exact ring, not a coincidental match at one point)."""
    tau = tau_round_trip_s(FSR_HZ)
    errs = []
    for a, t in [(0.999, 0.998), (0.9999, 0.9998)]:
        ki, ke = kappa_from_ring_amplitudes(a, t, FSR_HZ)
        ktot = ki + ke
        delta = _window(ktot)
        e = (cw_through(delta, ki, ke).abs()
             - single_bus_through(delta * tau, t, a).abs()).abs().max().item()
        errs.append(e)
    # 10x finesse -> error should drop by > 5x (measured ~10x)
    assert errs[0] / errs[1] > 5.0


def test_cw_limit_recovers_add_drop_through_and_drop():
    """Two-coupler add-drop: CMT through+drop magnitudes recover the
    salvaged analytic add-drop references at high finesse."""
    t1 = t2 = 0.999
    a = 0.9995
    tau = tau_round_trip_s(FSR_HZ)
    ke1 = (1 - t1 * t1) / (2 * tau)
    ke2 = (1 - t2 * t2) / (2 * tau)
    ki = (1 - a * a) / (2 * tau)
    ktot = ki + ke1 + ke2
    assert finesse(ktot, FSR_HZ) > 1000.0
    delta = _window(ktot)
    et = (cw_through(delta, ki, ke1, ke2).abs()
          - add_drop_through(delta * tau, t1, t2, a).abs()).abs().max().item()
    ed = (cw_drop(delta, ki, ke1, ke2).abs()
          - add_drop_drop(delta * tau, t1, t2, a).abs()).abs().max().item()
    assert et < GATE_TOL and ed < GATE_TOL


def test_cw_add_drop_energy_conservation_and_full_drop():
    """Lossless symmetric add-drop: |t_through|^2 + |t_drop|^2 == 1 and
    on-resonance drop == 1 (the CMT model is energy-conserving — confirms
    the sqrt(2 kappa_ext) Haus coupling convention)."""
    tau = tau_round_trip_s(FSR_HZ)
    ke = (1 - 0.999 ** 2) / (2 * tau)
    delta = _window(2 * ke)
    tt = cw_through(delta, 0.0, ke, ke)
    td = cw_drop(delta, 0.0, ke, ke)
    assert (tt.abs() ** 2 + td.abs() ** 2 - 1.0).abs().max().item() < 1e-12
    # on resonance (delta=0 is the midpoint): full transfer to drop port
    mid = delta.shape[0] // 2
    assert abs(td.abs()[mid].item() - 1.0) < 1e-9


def test_lossless_all_pass_is_unit_magnitude():
    """kappa_i = g = 0 all-pass: |t(Delta)| == 1 for all detunings."""
    delta = torch.linspace(-1e9, 1e9, 201)
    t = cw_through(delta, 0.0, 3e7)        # kappa_ext only
    assert (t.abs() - 1.0).abs().max().item() < 1e-12


def test_critical_coupling_full_extinction():
    """kappa_i == kappa_ext (critical coupling): through(0) == 0."""
    t0 = cw_through(torch.tensor(0.0), 3e7, 3e7)
    assert t0.abs().item() < 1e-12


def test_pole_to_eigenvalue_identity():
    """s = -kappa_tot + i*Delta <-> a_i = -exp(alpha) + i*beta exactly."""
    s = single_ring_pole(delta=3e8, kappa_i=2e7, kappa_ext1=1e7)
    assert s == complex(-3e7, 3e8)
    alpha, beta = pole_to_eigenvalue(s)
    assert abs(math.exp(alpha) - 3e7) < 1.0       # exp(alpha) == kappa_tot
    assert beta == 3e8


def test_gain_reduces_net_kappa_and_pole_moves_to_axis():
    """Net gain g_amp reduces kappa_tot (pole -> imaginary axis = longer
    memory); g_amp == kappa_i+kappa_ext is the marginal limit."""
    s_passive = single_ring_pole(0.0, 2e7, 1e7, g_amp=0.0)
    s_gain = single_ring_pole(0.0, 2e7, 1e7, g_amp=2.5e7)
    assert -s_gain.real < -s_passive.real            # closer to axis
    s_marg = single_ring_pole(0.0, 2e7, 1e7, g_amp=3e7)
    assert abs(s_marg.real) < 1e-6                   # marginal


def test_kappa_Q_roundtrip():
    """kappa_from_Q / Q_from_kappa are inverses; kappa_i = omega0/(2Qi)."""
    for Q in [2e6, 3e7]:
        k = kappa_from_Q(Q)
        assert abs(Q_from_kappa(k) - Q) / Q < 1e-12
        assert abs(k - math.pi * F0_HZ / Q) / k < 1e-12
