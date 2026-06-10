"""S0.2-1R GA-F1(a): run the OFFICIAL LinOSS code on the pre-declared fresh seeds.

Runs tk-rusch/linoss @ 05a8353 UNMODIFIED via its own run_experiments(), in the pinned
local CPU venv (/tmp/linoss_venv: jax 0.4.28 / equinox 0.11.4 / optax 0.2.2), on the
official pickles. The config is the committed copy with exactly three fields changed
(seeds / num_steps / output_parent_dir) — see
results/s0_2/gate_i/xcheck_official_local/PREDECLARATION.md.

Usage:
    /tmp/linoss_venv/bin/python scripts/xcheck_official_local.py <abs_config_dir>
"""
import os
import sys

OFFICIAL_REPO = "/tmp/linoss_official"
PICKLES = os.path.join(
    OFFICIAL_REPO, "data_dir", "processed", "UEA", "EigenWorms", "data.pkl"
)


def main() -> None:
    config_dir = os.path.abspath(sys.argv[1])
    if not os.path.isfile(PICKLES):
        raise SystemExit(f"official pickles not reachable at {PICKLES}")
    os.chdir(OFFICIAL_REPO)
    sys.path.insert(0, OFFICIAL_REPO)
    from run_experiment import run_experiments

    run_experiments(["LinOSS"], ["EigenWorms"], config_dir)


if __name__ == "__main__":
    main()
