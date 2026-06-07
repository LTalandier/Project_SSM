"""In-situ training estimators (S0.4).

S0.0 ships only the salvaged SPSA workhorse (`spsa.py`). PAT, the
recurrent in-situ adjoint, and RHEL (+ its concrete chi^3-FWM echo
sub-model) are S0.4 new code — all four train through the ONE shared
S0.3 substrate, scored primarily by sample-efficiency-to-target-accuracy
(physical forward passes; see `PerturbationAdaptor.n_forward_equivalents`).
"""

from photonic_ssm.estimators.spsa import (  # noqa: F401
    PerturbationAdaptor,
    compare_fd_vs_autograd,
)
