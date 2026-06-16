# NEW (task S0.3-1) — bake-off task generators (PR-2). The T-A Jaeger–Haas
# equalization generator is built here because the S0.3-1 damping sweep
# (deliverable 9) trains the BPTT reference on it; the S0.5 bake-off reuses it.
# Symbol names (PAM_LEVELS, nearest_pam) are clear and kept as-is; the 4-PAM
# semantics live in the docstrings and the (-3,-1,1,3) level values. (S0.3-1b /
# S31-F5: the hygiene gate now bans the source-repo equalization STACK SYMBOLS,
# not the generic "PAM4" task token — so these names are a clarity choice, no
# longer a gate workaround.) The source-repo equalization stack is genuinely
# absent — clean new code for a registered PR-2 task, not a salvage.
"""photonic_ssm.tasks — frozen PR-2 bake-off task generators.

  equalization — T-A Jaeger–Haas 4-PAM nonlinear channel equalization
                 (the headline task; target d(n−2); metric SER).
"""

from .equalization import (
    JaegerHaasChannel,
    make_ta_dataset,
    symbol_error_rate,
    nearest_pam,
    PAM_LEVELS,
)

__all__ = [
    "JaegerHaasChannel",
    "make_ta_dataset",
    "symbol_error_rate",
    "nearest_pam",
    "PAM_LEVELS",
]
