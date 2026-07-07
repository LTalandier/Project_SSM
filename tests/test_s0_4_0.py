# NEW (task S0.4-0, 2026-07-07) — tests for the S0.4-0 freeze-conforming
# substrate extensions: the PR-6 §B multi-tap input map and the §C clamp-A
# saturating-mode floor (measured r_min, frozen by the calibration addendum).
"""S0.4-0 substrate-extension tests.

(i)   default input_taps=(0,) is bit-identical to the pre-S0.4-0 single-port
      substrate (B, rollout, gradients unchanged);
(ii)  the multi-tap CW-equivalent E₀ reading is invariant under the equal
      1/√K amplitude split (the §G-addendum total-energy convention) — the
      frozen §N closed form needs no numeric change;
(iii) input-tap validation rejects malformed tap sets;
(iv)  clamp_to_bounds enforces the OPERATIVE band: r ∈ [R_MIN_SATURATING, 3]
      in the registered saturating mode (gain ON), K4 [0.1, 3] on the
      fixed/passive planes — closing the "clamp projects to r=0.1, unsafe in
      saturating mode" known (D-2026-06-13-1 → PR-6 §C).
"""

import pytest
import torch

from photonic_ssm.substrate import cells as cellmod
from photonic_ssm.substrate import normalization as O2
from photonic_ssm.substrate.dissipative_ring import (
    DissipativeRingSubstrate as DRS,
)


def _flux_drive(T=40, seed=3):
    g = torch.Generator().manual_seed(seed)
    return (O2.P_BAR0_W / O2.H_NU_J) ** 0.5 * torch.rand(T, generator=g)


def test_default_taps_bit_identical_to_single_port():
    a = DRS.from_cell("C-1", clock_GSps=2.0, seed=1, ase_variance_scale=0.0)
    b = DRS.from_cell("C-1", clock_GSps=2.0, seed=1, ase_variance_scale=0.0,
                      input_taps=(0,))
    assert a.input_taps == b.input_taps == (0,)
    assert torch.equal(a.B_doublet(), b.B_doublet())
    u = _flux_drive()
    sa, _ = a(u)
    sb, _ = b(u)
    assert torch.equal(sa, sb)


def test_multi_tap_E0_invariant_under_equal_split():
    """CW-equivalent single-pole reading (δ=0, μ=0, γ=0): total settled
    energy under the 1/√K split equals the single-port frozen closed form
    (identical rings ⇒ K·(2κ_ext·(P̄₀/K)/κ_net²) = E₀)."""
    vals = {}
    for taps in [(0,), (0, 8, 16, 24), (2, 11, 20, 29)]:
        sub = DRS.from_cell("C-2", clock_GSps=2.0, seed=1,
                            ase_variance_scale=0.0, input_taps=taps)
        ki = float(sub.kappa_i)
        with torch.no_grad():
            sub.delta.zero_()
            sub.mu_chain.zero_()
            sub.gamma.zero_()
            sub.kappa_ext.fill_(cellmod.R0_THETA0 * ki)
            flux = (O2.P_BAR0_W / O2.H_NU_J) ** 0.5
            u = torch.full((6000,), flux, dtype=torch.float64)
            states, _ = sub(u)
            vals[taps] = float(states[-1].abs().pow(2).sum())
    closed = O2.E0_photons(cellmod.R0_THETA0 * float(sub.kappa_i),
                           float(sub.kappa_i), gain_factor=sub.gain_factor)
    for taps, E in vals.items():
        assert abs(E / closed - 1.0) < 1e-3, (taps, E, closed)


def test_input_tap_validation():
    with pytest.raises(ValueError):
        DRS.from_cell("C-1", input_taps=())
    with pytest.raises(ValueError):
        DRS.from_cell("C-1", input_taps=(0, 99))
    with pytest.raises(ValueError):
        DRS.from_cell("C-1", input_taps=(-1,))
    sub = DRS.from_cell("C-1", input_taps=(3, 1, 3))   # dedup + sort
    assert sub.input_taps == (1, 3)


def test_clamp_saturating_uses_r_min_fixed_uses_k4():
    lo_k4, hi = cellmod.R_BOUNDS
    r_min = cellmod.R_MIN_SATURATING
    assert r_min > lo_k4                       # the whole point of clamp A

    # Saturating mode (registered bake-off mode): floor = r_min.
    sub = DRS.from_cell("C-2", clock_GSps=2.0, seed=1)
    ki = float(sub.kappa_i)
    with torch.no_grad():
        sub.kappa_ext.fill_(0.05 * ki)         # below r* — would lase
    sub.clamp_to_bounds()
    r = sub.kappa_ext.detach() / ki
    assert torch.all(r >= r_min - 1e-12), r
    # and the clamped point is sub-threshold (κ_net > 0): no lasing.
    assert torch.all(sub.kappa_net().detach() > 0)

    # Fixed (diagnostic) mode: the K4 passive-plane floor applies unchanged.
    sub_f = DRS.from_cell("C-2", clock_GSps=2.0, seed=1, gain_mode="fixed")
    with torch.no_grad():
        sub_f.kappa_ext.fill_(0.05 * float(sub_f.kappa_i))
    sub_f.clamp_to_bounds()
    rf = sub_f.kappa_ext.detach() / float(sub_f.kappa_i)
    assert torch.all(rf >= lo_k4 - 1e-12) and torch.all(rf < r_min)

    # Passive cell: K4 floor too (no gain ⇒ no lasing hazard).
    sub_p = DRS.from_cell("P-CORN", clock_GSps=2.0, seed=1)
    with torch.no_grad():
        sub_p.kappa_ext.fill_(0.05 * float(sub_p.kappa_i))
    sub_p.clamp_to_bounds()
    rp = sub_p.kappa_ext.detach() / float(sub_p.kappa_i)
    assert torch.all(rp >= lo_k4 - 1e-12) and torch.all(rp < r_min)

    # Upper bound unchanged everywhere.
    with torch.no_grad():
        sub.kappa_ext.fill_(5.0 * ki)
    sub.clamp_to_bounds()
    assert torch.all(sub.kappa_ext.detach() / ki <= hi + 1e-12)
