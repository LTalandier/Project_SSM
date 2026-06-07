# salvaged from pnn-multilayer @ e2eec80 : evaluate.py (log_experiment /
#   load_all_results JSONL pattern only — the MZI evaluation protocol
#   around it was NOT salvaged, per recon §1.4)
# Adaptations for Project_SSM (task S0.0, deliverable 2):
#   - path is an explicit argument (no module-global results dir);
#   - record content is caller-defined (no MZI-specific fields);
#   - optional quiet mode (no print).
"""Append-only JSONL experiment log.

One JSON object per line; each entry gets a sequential `id` and a UTC
timestamp. Used for run-level bookkeeping (configs, summary metrics,
data paths) — bulk sweep records live in the keyed-JSON files managed
by `runner.sweep`.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone


def log_experiment(path: str, results: dict, description: str = "",
                   config: dict | None = None, quiet: bool = False) -> int:
    """Append an experiment entry to the JSONL log at `path`.

    Returns the experiment ID (= line index)."""
    parent = os.path.dirname(os.path.abspath(path))
    os.makedirs(parent, exist_ok=True)

    # Count existing experiments
    exp_id = 0
    if os.path.exists(path):
        with open(path) as f:
            exp_id = sum(1 for _ in f)

    entry = {
        "id": exp_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "description": description,
        "config": config or {},
        **results,
    }

    with open(path, "a") as f:
        f.write(json.dumps(entry) + "\n")

    if not quiet:
        print(f"[LOG] Experiment {exp_id}: {description}")
    return exp_id


def load_results(path: str) -> list[dict]:
    """Load all experiment entries from the JSONL log."""
    if not os.path.exists(path):
        return []
    results = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    return results
