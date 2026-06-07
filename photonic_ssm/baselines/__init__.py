"""Bake-off baselines (proposal §5.3).

S0.0 ships the salvaged ridge-readout machinery (`ridge_readout.py`) —
the trainable-readout half of the reservoir-computing baseline. The
baseline becomes runnable once the S0.3 substrate exposes state
trajectories (architecture constraint 3b). The offline-train-deploy
baseline is S0.5 wiring, not code here.
"""

from photonic_ssm.baselines.ridge_readout import (  # noqa: F401
    RidgeReadout,
    ReservoirReadoutBaseline,
    delay_embed,
)
