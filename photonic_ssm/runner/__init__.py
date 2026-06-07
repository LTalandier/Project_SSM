"""Experiment orchestration: resume-safe sweeps + JSONL experiment log.

Pattern-salvaged scaffolding (see module headers). The S0.5 bake-off
runner builds its job grids and per-job metrics ON this scaffold; the
scaffold itself knows nothing about photonics.
"""

from photonic_ssm.runner.jsonl_log import (  # noqa: F401
    log_experiment,
    load_results,
)
from photonic_ssm.runner.sweep import (  # noqa: F401
    run_sweep,
    load_existing,
    save_records,
    standard_argparser,
)
