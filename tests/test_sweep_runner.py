# tests for photonic_ssm/runner/ (pattern-salvaged from pnn-multilayer
# sweep_phase4a_mrr1_ringbank.py + evaluate.py JSONL @ e2eec80).
"""Resume-safe sweep runner + JSONL log tests."""

import json
import os

import pytest

from photonic_ssm.runner import (
    load_existing,
    load_results,
    log_experiment,
    run_sweep,
    save_records,
)


# Top-level so mp workers can resolve them.
def _square_job(job):
    return {**job, "y": job["x"] ** 2}


def _must_not_run_job(job):
    raise RuntimeError("resume filter failed — job re-executed")


KEY = ("x",)


def test_run_sweep_completes_and_saves(tmp_path):
    out = str(tmp_path / "sweep.json")
    jobs = [{"x": i} for i in range(10)]
    records = run_sweep(jobs, _square_job, out, key_fields=KEY,
                        workers=1, quiet=True)
    assert len(records) == 10
    on_disk = load_existing(out)
    assert sorted(r["y"] for r in on_disk) == [i ** 2 for i in range(10)]
    with open(out) as f:
        payload = json.load(f)
    assert payload["schema"] == "sweep.v1"


def test_resume_skips_completed(tmp_path):
    out = str(tmp_path / "sweep.json")
    jobs = [{"x": i} for i in range(6)]
    run_sweep(jobs, _square_job, out, key_fields=KEY, workers=1, quiet=True)
    # Second run: nothing remaining -> the failing job fn must never fire.
    records = run_sweep(jobs, _must_not_run_job, out, key_fields=KEY,
                        workers=1, quiet=True)
    assert len(records) == 6


def test_incremental_grid_extension(tmp_path):
    out = str(tmp_path / "sweep.json")
    run_sweep([{"x": i} for i in range(5)], _square_job, out,
              key_fields=KEY, workers=1, quiet=True)
    records = run_sweep([{"x": i} for i in range(8)], _square_job, out,
                        key_fields=KEY, workers=1, quiet=True)
    assert len(records) == 8
    assert sorted(r["x"] for r in load_existing(out)) == list(range(8))


def test_dry_run_executes_nothing(tmp_path):
    out = str(tmp_path / "sweep.json")
    records = run_sweep([{"x": 1}], _must_not_run_job, out, key_fields=KEY,
                        dry_run=True, quiet=True)
    assert records == []
    assert not os.path.exists(out)


def test_summary_only_calls_summarizer_and_skips_jobs(tmp_path):
    out = str(tmp_path / "sweep.json")
    save_records(out, [{"x": 0, "y": 0}])
    seen = []
    run_sweep([{"x": 0}, {"x": 1}], _must_not_run_job, out, key_fields=KEY,
              summary_only=True, summarize_fn=lambda recs: seen.append(recs),
              quiet=True)
    assert len(seen) == 1 and len(seen[0]) == 1


def test_parallel_workers(tmp_path):
    out = str(tmp_path / "sweep.json")
    jobs = [{"x": i} for i in range(8)]
    records = run_sweep(jobs, _square_job, out, key_fields=KEY,
                        workers=2, mp_context="fork", quiet=True)
    assert sorted(r["y"] for r in records) == [i ** 2 for i in range(8)]


def test_jsonl_log_roundtrip(tmp_path):
    path = str(tmp_path / "log.jsonl")
    for k in range(3):
        exp_id = log_experiment(path, {"metric": k}, description=f"run {k}",
                                config={"seed": k}, quiet=True)
        assert exp_id == k
    entries = load_results(path)
    assert len(entries) == 3
    assert entries[1]["metric"] == 1
    assert entries[2]["config"]["seed"] == 2
    assert all("timestamp" in e for e in entries)
