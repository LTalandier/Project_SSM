# NEW (task S0.1) — the dynamical SSM core (temporal CMT), distinct from
# the salvaged static/CW transfer functions in photonic_ssm.static_rings.
"""Dynamical photonic-SSM core (proposal §3, §4).

  single_ring   — temporal-CMT single ring; pole = recurrence; CW limit.
  coupled_rings — N-oscillator LinOSS forward model (3a/3b honored).
  pole_region   — realizable pole-region bounds, kappa_ext trade,
                  backscatter crossover.
"""

from .single_ring import (
    F0_HZ,
    OMEGA0_RAD_S,
    kappa_from_Q,
    Q_from_kappa,
    tau_round_trip_s,
    kappa_from_ring_amplitudes,
    finesse,
    single_ring_pole,
    pole_to_eigenvalue,
    cw_through,
    cw_drop,
)
from .coupled_rings import (
    CoupledRingLinOSS,
    from_eigenvalues,
    zoh_discretize,
)
from .pole_region import (
    photon_lifetime_s,
    loss_limited_memory_time_s,
    net_kappa_tot,
    discrete_pole_magnitude,
    memory_length_samples,
    gain_for_target_memory,
    io_residue,
    drop_efficiency_on_resonance,
    kappa_ext_trade_sweep,
    gamma_rad_s_from_MHz_linear,
    splitting_linewidth_ratio,
    crossover_Q,
)

__all__ = [
    "F0_HZ", "OMEGA0_RAD_S", "kappa_from_Q", "Q_from_kappa",
    "tau_round_trip_s", "kappa_from_ring_amplitudes", "finesse",
    "single_ring_pole", "pole_to_eigenvalue", "cw_through", "cw_drop",
    "CoupledRingLinOSS", "from_eigenvalues", "zoh_discretize",
    "photon_lifetime_s", "loss_limited_memory_time_s", "net_kappa_tot",
    "discrete_pole_magnitude", "memory_length_samples",
    "gain_for_target_memory", "io_residue", "drop_efficiency_on_resonance",
    "kappa_ext_trade_sweep", "gamma_rad_s_from_MHz_linear",
    "splitting_linewidth_ratio", "crossover_Q",
]
