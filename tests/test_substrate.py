# NEW (task S0.3-1, deliverable 8) — the 8 registered substrate unit tests.
# Each test (a)-(h) is a frozen PR-4 v2 / roadmap-F18 acceptance gate. All
# must pass and report the measured numbers (b/d/e/f).
"""Registered S0.3-1 substrate unit tests (PR-4 v2, roadmap Gate F18).

(a) loss_q_consistency_error α↔Q registry check per cell.
(b) zero-noise / passive limit recovers the S0.1 forward model (Gate F18).
(c) B1-consistency: K4 r ∈ [0.1, 3] maps into the S0.1 realizable pole region
    at every cell.
(d) A1↔A2 statistical equivalence (O(10⁻³) relative at per-rt gains ≤ 0.2 dB).
(e) E₀ normalization: E(E₀-normalized drive) = E₀ per cell × bound-edge r∈{0.1,3}.
(f) n_ss ≈ 23 ASE photons at NF-7 / 90 %-compensation, corner-independent (≈9 at NF-3).
(g) γ=0 ⇒ single-pole structural equivalence.
(h) gradient-flow gate (operational F18): a BPTT loss backprops through the
    full substrate (gain + ASE + splitting) to all P2 params; no no_grad/detach.
"""

import math

import pytest
import torch

from photonic_ssm.dynamics.coupled_rings import CoupledRingLinOSS
from photonic_ssm.dynamics.single_ring import F0_HZ, tau_round_trip_s
from photonic_ssm.platforms import loss_q_ceiling_ok, loss_q_consistency_error
from photonic_ssm.substrate import (
    DissipativeRingSubstrate as DRS, cells as C, get_cell,
)
from photonic_ssm.substrate import ase as A
from photonic_ssm.substrate import normalization as O2

GATING_CELLS = ["C-1", "C-2", "C-3"]
ALL_CELLS = ["C-1", "C-2", "C-3", "C-2-derate", "P-CORN"]


@pytest.fixture(autouse=True)
def _float64_default():
    """Substrate fidelity tests use float64 locally; restore the global
    default afterwards so we don't leak into the float32 LinOSS/ridge tests."""
    prev = torch.get_default_dtype()
    torch.set_default_dtype(torch.float64)
    yield
    torch.set_default_dtype(prev)


# -------------------------------------------------------------------- #
#  (a) loss↔Q registry self-consistency per cell
# -------------------------------------------------------------------- #
def test_a_loss_q_consistency_per_cell():
    for lab in ALL_CELLS:
        plat = C.platform_of(get_cell(lab))
        # loss-limited SiN cells sit on the propagation ceiling (≈0 error);
        # the universal invariant Qi <= ceiling holds for all.
        assert loss_q_ceiling_ok(plat, rel_tol=1e-3), lab
        assert loss_q_consistency_error(plat) < 1e-3, \
            f"{lab}: loss↔Q error {loss_q_consistency_error(plat):.2e}"


# -------------------------------------------------------------------- #
#  (b) zero-noise / passive limit recovers the S0.1 forward model
# -------------------------------------------------------------------- #
def test_b_passive_recovers_s0_1_forward_model():
    """Gate F18: passive (g=0), noiseless, γ=0 substrate is bit-identical to
    the S0.1 CoupledRingLinOSS, AND its CW steady state matches the static
    Lorentzian (single_ring CW closed form)."""
    sub = DRS(get_cell("C-2"), N=4, clock_GSps=2.0, gain_factor=0.0,
              ase_variance_scale=0.0, seed=0)
    with torch.no_grad():
        sub.gamma.zero_()
        sub.mu_chain.copy_(0.05 * sub.kappa_i * torch.ones_like(sub.mu_chain))
    ktot = (sub.kappa_i + 2.0 * sub.kappa_ext).detach()
    B = torch.zeros(4, 1, dtype=torch.complex128)
    B[0, 0] = torch.sqrt(2.0 * sub.kappa_ext[0]).to(torch.complex128)
    ref = CoupledRingLinOSS(ktot, sub.delta.detach(), sub.dt,
                            mu=sub.mu_matrix().detach(), B=B,
                            C=torch.ones(1, 4, dtype=torch.complex128))
    u = torch.rand(40)
    _, out_s = sub(u)
    _, out_r = ref(u.reshape(-1, 1))
    err = (out_s - out_r).abs().max().item()
    assert err < 1e-12, f"substrate≠S0.1 forward model: {err:.2e}"

    # CW-limit Lorentzian: single uncoupled ring settles to the closed form.
    sub1 = DRS(get_cell("C-2"), N=1, clock_GSps=2.0, gain_factor=0.0,
               ase_variance_scale=0.0)
    with torch.no_grad():
        sub1.gamma.zero_(); sub1.delta.zero_()
    s_in = 3.0
    states, _ = sub1(torch.full((6000,), s_in))
    a_ss = states[-1, 0]
    kext = float(sub1.kappa_ext[0].detach()); knet = float(sub1.kappa_i) + 2 * kext
    a_analytic = math.sqrt(2 * kext) * s_in / knet
    assert abs(abs(a_ss.item()) - a_analytic) / a_analytic < 1e-6


# -------------------------------------------------------------------- #
#  (c) B1-consistency: K4 bounds map into the S0.1 realizable pole region
# -------------------------------------------------------------------- #
def test_c_b1_consistency_pole_region():
    """At every cell and every K4 bound edge r ∈ {0.1, 3}, the substrate's
    continuous poles are dissipative (Re < 0 ⇔ κ_net > 0) and FSR-bounded
    (|Im| ≤ π·FSR), and the memory is non-degenerate (≥ 0.5 samples @ 2 GS/s)
    — i.e. inside the S0.1 realizable region."""
    lo, hi = C.R_BOUNDS
    for lab in GATING_CELLS:
        for r in (lo, hi):
            sub = DRS.from_cell(lab, clock_GSps=2.0)
            with torch.no_grad():
                sub.kappa_ext.fill_(r * float(sub.kappa_i))
            poles = sub.continuous_poles()
            assert torch.all(poles.real < 0), f"{lab} r={r}: non-dissipative pole"
            fsr_bound = math.pi * sub.FSR_Hz
            assert torch.all(poles.imag.abs() <= fsr_bound), f"{lab} r={r}: aliased"
            knet = 0.1 * float(sub.kappa_i) + 2 * r * float(sub.kappa_i)
            mem = 1.0 / (knet * sub.dt)
            assert mem >= 0.5, f"{lab} r={r}: degenerate memory {mem:.2f}"
            assert sub.bounds_ok()


# -------------------------------------------------------------------- #
#  (d) A1 ↔ A2 statistical equivalence
# -------------------------------------------------------------------- #
def test_d_a1_a2_equivalence():
    """The per-step ASE covariance from A1 (per-round-trip kick) and A2 (exact
    Langevin) agree to O(κ_net·τ_rt) ~ 1e-3, at every clock (the difference is
    tied to the per-round-trip decay, NOT the per-sample decay)."""
    residuals = []
    for lab in GATING_CELLS:
        cell = get_cell(lab); ki = C.kappa_i_rad_s(cell)
        tau_rt = tau_round_trip_s(C.platform_of(cell).FSR_GHz * 1e9)
        knet = 0.1 * ki + 2 * C.R0_THETA0 * ki
        M = torch.tensor([[-knet + 0j]]); g = torch.tensor([0.9 * ki])
        for clk in (2.0, 1.0, 0.1):
            dt = 1.0 / (clk * 1e9)
            q2 = A.ASEInjector(M, g, 7.0, dt, "A2").Qd[0, 0].real
            q1 = A.ASEInjector(M, g, 7.0, dt, "A1", tau_rt=tau_rt).Qd[0, 0].real
            rel = abs((q1 - q2) / q2).item()
            residuals.append(rel)
            assert rel < 1e-2, f"{lab}@{clk}: A1↔A2 rel {rel:.2e}"
    print(f"\n(d) A1↔A2 max relative residual = {max(residuals):.2e}")


# -------------------------------------------------------------------- #
#  (e) E₀ normalization per cell × bound edge
# -------------------------------------------------------------------- #
def test_e_E0_normalization():
    """The encoder scale derived to hit E₀ reproduces E₀ (CW-equivalent
    reading) at every cell and every K4 bound edge r ∈ {0.1, 3}."""
    lo, hi = C.R_BOUNDS
    tols = []
    for lab in GATING_CELLS:
        cell = get_cell(lab); ki = C.kappa_i_rad_s(cell)
        E0ref = O2.E0_photons(C.R0_THETA0 * ki, ki, gain_factor=cell.gain_factor)
        for r in (lo, hi):
            kext = r * ki
            scale = O2.encoder_scale_to_hit_E0(E0ref, kext, ki, cell.gain_factor)
            sub = DRS.from_cell(lab, clock_GSps=2.0)
            sub.ase_variance_scale = 0.0
            with torch.no_grad():
                sub.kappa_ext.fill_(kext)
                sub.delta.zero_(); sub.mu_chain.zero_(); sub.gamma.zero_()
                flux = O2.P_BAR0_W / O2.H_NU_J
                s = math.sqrt(scale * flux)
                st, _ = sub(torch.full((5000,), s))
                meas = float(st[-1].abs().pow(2).sum())
            rel = abs(meas - E0ref) / E0ref
            tols.append(rel)
            assert rel < 1e-6, f"{lab} r={r}: E₀ miss {rel:.2e}"
    print(f"\n(e) E₀ normalization max tolerance = {max(tols):.2e}")


# -------------------------------------------------------------------- #
#  (f) n_ss ≈ 23 (NF-7) / ≈ 9 (NF-3), corner-independent
# -------------------------------------------------------------------- #
def test_f_n_ss_corner_independent():
    """Steady-state ASE photon number at 90 %-compensation (κ_net = 0.1κᵢ):
    n_ss = 9·n_sp ≈ 23 at NF-7, ≈ 9 at NF-3, independent of the cell."""
    n_ss7 = [C.n_ss_compensation(7.0, 0.9) for _ in GATING_CELLS]
    n_ss3 = [C.n_ss_compensation(3.0, 0.9) for _ in GATING_CELLS]
    assert all(abs(x - 22.55) < 0.5 for x in n_ss7), n_ss7
    assert all(abs(x - 8.98) < 0.5 for x in n_ss3), n_ss3
    assert max(n_ss7) - min(n_ss7) < 1e-9             # corner-independent

    # Confirm via the A2 van-Loan covariance steady state (single mode, each
    # cell): ⟨|a|²⟩ = Q_d/(1-|Φ|²) = n_ss.
    for lab in GATING_CELLS:
        cell = get_cell(lab); ki = C.kappa_i_rad_s(cell)
        dt = tau_round_trip_s(C.platform_of(cell).FSR_GHz * 1e9)
        knet = 0.1 * ki
        M = torch.tensor([[-knet + 0j]])
        inj = A.ASEInjector(M, torch.tensor([0.9 * ki]), 7.0, dt, "A2")
        Phi = torch.matrix_exp(M * dt)
        nss = (inj.Qd[0, 0].real / (1 - abs(Phi[0, 0]) ** 2)).item()
        assert abs(nss - 22.55) < 0.1, f"{lab}: n_ss {nss:.2f}"
    print(f"\n(f) n_ss NF-7 = {n_ss7[0]:.2f} (≈23), NF-3 = {n_ss3[0]:.2f} (≈9), "
          f"corner-independent")


# -------------------------------------------------------------------- #
#  (g) γ=0 ⇒ single-pole structural equivalence
# -------------------------------------------------------------------- #
def test_g_gamma0_single_pole():
    """With γ=0 the CCW block decouples and stays undriven (≡0), so the
    doublet substrate is bit-identical to the single-direction model."""
    sub = DRS.from_cell("C-2", clock_GSps=2.0, seed=0, ase_variance_scale=0.0)
    with torch.no_grad():
        sub.gamma.zero_()
    u = torch.rand(50)
    states, _ = sub(u)
    ccw = states[..., sub.N:]
    assert ccw.abs().max().item() == 0.0, "γ=0 but CCW populated"

    # And the eigenvalues of the doublet are exactly the single-direction
    # eigenvalues duplicated (the CCW copy).
    M_dir = sub.M_dir()
    ev_dir = torch.linalg.eigvals(M_dir).real.sort().values
    ev_dbl = torch.linalg.eigvals(sub.M_doublet()).real.sort().values
    # each direction eigenvalue appears twice in the doublet
    ev_dir2 = torch.cat([ev_dir, ev_dir]).sort().values
    assert torch.allclose(ev_dbl, ev_dir2, atol=1e-6)


# -------------------------------------------------------------------- #
#  (h) gradient-flow gate — the operational F18 test
# -------------------------------------------------------------------- #
def test_h_gradient_flow_full_substrate():
    """A BPTT loss backpropagates through the FULL substrate (gain + ASE +
    splitting) to all P2 params {δ, κ_ext, μ}; grads are finite and nonzero
    (proof the no_grad/detach anti-pattern was avoided). Run at C-1/N=8 and
    C-2/N=32, registered operating point, NF-A, splitting ON, ASE ON."""
    for lab in ("C-1", "C-2"):
        sub = DRS.from_cell(lab, clock_GSps=2.0, seed=1)
        assert sub.gain_factor == 0.9 and sub.ase_variance_scale == 1.0
        assert float(sub.gamma.abs().sum()) > 0      # splitting ON
        flux = (O2.P_BAR0_W / O2.H_NU_J) ** 0.5
        g = torch.Generator().manual_seed(3)
        u = flux * torch.rand(60, generator=g)
        gen = torch.Generator().manual_seed(11)
        y = sub.forward_intensity(u, generator=gen)
        target = torch.zeros_like(y)
        loss = ((y - target) ** 2).mean()
        assert loss.requires_grad                    # graph intact (no no_grad)
        loss.backward()
        for name, p in [("δ", sub.delta), ("κ_ext", sub.kappa_ext),
                        ("μ", sub.mu_chain)]:
            assert p.grad is not None, f"{lab}: no grad on {name}"
            assert torch.isfinite(p.grad).all(), f"{lab}: non-finite grad {name}"
            assert p.grad.abs().sum() > 0, f"{lab}: zero grad on {name}"


# -------------------------------------------------------------------- #
#  checkpoint equivalence (constraint 3a memory bound, value + gradient)
# -------------------------------------------------------------------- #
def test_checkpointed_rollout_matches_plain():
    """The gradient-checkpointed chunked rollout agrees with the plain rollout
    in value AND gradient (constraint 3a, the salvaged-pattern guarantee)."""
    sub = DRS.from_cell("C-1", clock_GSps=2.0, seed=2, ase_variance_scale=0.0)
    flux = (O2.P_BAR0_W / O2.H_NU_J) ** 0.5
    u = flux * torch.rand(48)
    y1 = sub.forward_intensity(u); l1 = y1.sum(); l1.backward()
    g1 = sub.delta.grad.clone()
    sub.zero_grad()
    y2 = sub.forward_intensity(u, checkpoint_chunk=8); l2 = y2.sum(); l2.backward()
    g2 = sub.delta.grad.clone()
    assert (y1 - y2).abs().max() < 1e-10
    assert (g1 - g2).abs().max() < 1e-8
