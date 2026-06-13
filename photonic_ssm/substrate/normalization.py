# NEW (task S0.3-1, deliverable 6) — O2 intracavity-energy normalization.
# Implements the frozen PR-4 v2 §N choice (O2) and the in-block E₀ formula.
# Sets no values: P̄₀ = 1 mW, the encoder map, the P_pk factors, and the E₀
# formula are all frozen PR-4 v2 §N entries.
"""O2 registered intracavity-energy budget (PR-4 v2 §N).

The encoder cannot buy SNR against the noise cell: every arm (SSM and
reservoir baseline) and every κ_ext policy point derives its encoder scale
to hit the SAME registered intracavity energy E₀ (the natural partner of the
corner-independent n_ss ≈ 23 ASE photons).

Encoder map (P4-F12, explicit): the unipolar affine map
{0,1,2,3} → {0,⅓,⅔,1}·P_pk; equiprobable mean = P_pk/2 = P̄₀. Peak-to-average
is task-family-scoped: P_pk = 2·P̄₀ for the equiprobable 4-PAM T-A family;
≈ 2.7·P̄₀ for the PR-13 marker family (fifth level on the same map).

E₀ — the frozen closed form (P4-F6), the steady-state intracavity photon
number under a stationary P̄₀ drive at the cell, θ₀, on-resonance (δ≡0),
μ=0, CW-equivalent stationarity reading, calibration injection on ring-1's
bus (|s_in|² = P̄₀/ħω₀ photon flux):

    E₀ = 2·κ_ext,θ₀ · (P̄₀/ħω₀) / κ_net²,
    κ_net = (1-gain_factor)·κᵢ + 2κ_ext (operating gain; κ_tot at the passive
    floor). No free parameter remains.

Encoder-scale cadence (P4-F6): the scale is derived once per arm at θ₀ and
frozen for the run; trained κ_ext excursions thereafter change intracavity
energy AS PHYSICS, not as renormalization. The unit test (e) validates the
normalization machinery itself — at each K4 bound edge r ∈ {0.1, 3} the
encoder scale derived to hit E₀ reproduces E₀ (CW-equivalent reading).
"""

from __future__ import annotations

import torch

H_NU_J: float = 1.282e-19      # photon energy at 1550 nm [J]
P_BAR0_W: float = 1e-3         # registered per-sequence mean bus power [W]

# Task-family peak-to-average ratios (P4-F12).
P_PK_FACTOR = {
    "T-A": 2.0,        # equiprobable 4-PAM
    "PR-13": 2.7,      # marker family (fifth level)
}


def kappa_net_operating(kappa_ext: float, kappa_i: float,
                        gain_factor: float = 0.9) -> float:
    """κ_net = (1-gain_factor)·κᵢ + 2κ_ext (operating gain; gain_factor=0 ⇒
    passive floor κ_tot)."""
    return (1.0 - gain_factor) * kappa_i + 2.0 * kappa_ext


def E0_photons(kappa_ext: float, kappa_i: float, P_bar0_W: float = P_BAR0_W,
               gain_factor: float = 0.9, hnu: float = H_NU_J) -> float:
    """The frozen E₀ closed form (PR-4 v2 §N): the on-resonance CW-equivalent
    steady-state intracavity photon number for a single driven ring."""
    knet = kappa_net_operating(kappa_ext, kappa_i, gain_factor)
    flux = P_bar0_W / hnu
    return 2.0 * kappa_ext * flux / (knet ** 2)


def doublet_onres_reduction(gamma_rad_s: float, kappa_net: float) -> float:
    """The K-pol-3 on-resonance steady-state reduction factor E_doublet/E₀ =
    1/(1+(γ/κ_net)²): with the splitting ON, driving at the bare resonance
    sits in the dip between the two split peaks. A documented physical effect
    (NOT a renormalization); the E₀ formula is the single-pole/CW-equivalent
    reference the freeze registers."""
    return 1.0 / (1.0 + (gamma_rad_s / kappa_net) ** 2)


# ---------------------------------------------------------------------- #
#  Encoder
# ---------------------------------------------------------------------- #

def P_pk_for_family(family: str = "T-A", P_bar0_W: float = P_BAR0_W) -> float:
    """Peak power P_pk for a task family (T-A: 2·P̄₀; PR-13 marker: 2.7·P̄₀)."""
    if family not in P_PK_FACTOR:
        raise KeyError(f"Unknown task family {family!r}; known {sorted(P_PK_FACTOR)}")
    return P_PK_FACTOR[family] * P_bar0_W


def symbol_to_power_W(symbols: torch.Tensor, P_pk_W: float) -> torch.Tensor:
    """Affine encoder {0,1,2,3} → {0,⅓,⅔,1}·P_pk (power [W]). Marker level 4
    (PR-13) maps to (4/3)·P_pk on the same /3 ladder (peak ≈ 2.7·P̄₀ via
    P_pk = 2.7·P̄₀ with the 4-level being the peak under that scale)."""
    return (symbols.to(torch.float64) / 3.0) * P_pk_W


def encode_amplitude(symbols: torch.Tensor, P_pk_W: float,
                     scale: float = 1.0, hnu: float = H_NU_J) -> torch.Tensor:
    """Encode symbols to a real bus drive amplitude s_in (photon-flux
    amplitude; |s_in|² = P/ħω₀ photon flux). `scale` is the frozen per-arm
    encoder scale (default 1 = the nominal P_pk map)."""
    P = scale * symbol_to_power_W(symbols, P_pk_W)
    return torch.sqrt(P / hnu)


def encoder_scale_to_hit_E0(E0_target: float, kappa_ext: float,
                            kappa_i: float, gain_factor: float = 0.9,
                            P_bar0_W: float = P_BAR0_W,
                            hnu: float = H_NU_J) -> float:
    """The per-arm power-scale that makes the on-resonance CW-equivalent
    steady-state energy equal E0_target at this κ_ext. Since E ∝ (mean bus
    power) ∝ scale, scale = E0_target / E0_photons(κ_ext,...,P̄₀). This is the
    machinery the encoder-cannot-buy-SNR guarantee rests on; validated at the
    K4 bound edges by test (e)."""
    e_nominal = E0_photons(kappa_ext, kappa_i, P_bar0_W, gain_factor, hnu)
    return E0_target / e_nominal


def measure_E0_cw_equivalent(substrate, n_settle: int = 4000) -> float:
    """Measure the substrate's CW-equivalent on-resonance steady-state photon
    number Σⱼ|aⱼ|² under a stationary P̄₀ drive (δ=0, μ=0, γ=0 — the
    single-pole reading the E₀ closed form registers). Drives ring-1's bus
    with a constant amplitude |s_in|² = P̄₀/ħω₀ and reads the settled state.
    Used by test (e) to validate the E₀ formula + encoder."""
    import copy
    sub = copy.deepcopy(substrate)
    sub.ase_variance_scale = 0.0     # deterministic steady state
    with torch.no_grad():
        sub.delta.zero_()
        sub.mu_chain.zero_()
        sub.gamma.zero_()            # CW-equivalent (single-pole) reading
        flux = P_BAR0_W / H_NU_J
        s_in = (flux ** 0.5)
        u = torch.full((n_settle,), s_in, dtype=sub._rdtype).to(sub._dtype)
        states, _ = sub(u, generator=None)
        a_last = states[-1]          # (2N,)
        return float(a_last.abs().pow(2).sum())
