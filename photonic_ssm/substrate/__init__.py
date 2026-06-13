# NEW (task S0.3-1) — the shared dissipative-ring substrate that all four
# in-situ-training estimators (S0.4) and the bake-off (S0.5) train through.
# Implements the frozen PR-4 v2 substrate block (preregistration.md,
# 🔒 SIGNED 2026-06-13). This package sets NO new values: every parameter
# traces to a frozen PR-4 v2 entry or an inherited S0.1 convention. The one
# registered deferral — the numeric E₀ and the saturated reachability solve —
# is computed mechanically by `calibration.py` from the in-block formula.
"""photonic_ssm.substrate — frozen PR-4 v2 dissipative-ring substrate.

  cells          — PR-4 cell registry (C-1/C-2/C-3 + sensitivity axes),
                   built on the salvaged `platforms` registry.
  gain           — M1 static saturated operating point g(P̄)=g₀/(1+P̄/P_sat).
  ase            — A2 continuous Langevin ASE (+ A1 per-rt-kick equivalent).
  splitting      — K-pol-3 CW/CCW backscatter doublet (always ON; γ=0⇒single).
  dissipative_ring — DissipativeRingSubstrate: the N-ring CMT recurrence the
                   estimators train through (P2 partition, full trajectory,
                   intensity readout, F18 gradient-flow discipline).
  normalization  — O2 intracavity-energy encoder budget.
  calibration    — numeric E₀ + saturated reachability solve (the registered
                   one-line ledger addendum).

House constraint (3a/3b, photonic_ssm/__init__.py): no `no_grad`/`detach` in
the rollout path; full state trajectory exposed. Runtime imports: torch +
stdlib only.
"""

from .cells import (
    SubstrateCell,
    CELLS,
    get_cell,
    kappa_i_rad_s,
    gamma_rad_s,
    n_sp_from_nf_dB,
    n_ss_compensation,
    platform_of,
    GAIN_FACTOR_OPERATING,
    GAIN_FACTOR_SENSITIVITY,
    R0_THETA0,
    R_BOUNDS,
)
from .dissipative_ring import DissipativeRingSubstrate

__all__ = [
    "SubstrateCell",
    "CELLS",
    "get_cell",
    "kappa_i_rad_s",
    "gamma_rad_s",
    "n_sp_from_nf_dB",
    "n_ss_compensation",
    "platform_of",
    "GAIN_FACTOR_OPERATING",
    "GAIN_FACTOR_SENSITIVITY",
    "R0_THETA0",
    "R_BOUNDS",
    "DissipativeRingSubstrate",
]
