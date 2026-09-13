# salvaged (pattern) from pnn-multilayer @ e2eec80 : sweep_phase4a_mrr1_ringbank.py
#   (the orchestration skeleton ONLY: pre-registered job list -> resume
#    filter on a job key -> sequential or mp.Pool execution -> periodic
#    keyed-JSON saves -> progress/ETA prints -> summary hook -> the
#    --workers/--quick/--dry-run/--summary-only CLI convention. All
#    fiber/QPSK/BER content stripped — recon §1.2 verdict
#    "rewrite-with-pattern".)
"""Generic resume-safe sweep runner for pre-registered experiment grids.

House rules this scaffold enforces (project quality standards):
  * the job grid is built up-front (pre-registered), each job a plain
    dict of config fields incl. its seed;
  * every completed job is keyed by `key_fields`; re-running the sweep
    only executes jobs whose key is absent from the output file —
    crash-safe and incrementally extensible;
  * records are saved every `save_every` completions and at the end;
  * `run_job` must be a TOP-LEVEL function (picklable) taking the job
    dict and returning a record dict that includes the key fields.

Typical driver:

    JOBS = [dict(method=m, sigma=s, seed=k) ...]          # pre-registered
    def run_job(job): ...; return record
    def main():
        ap = standard_argparser("S0.5 bake-off sweep")
        args = ap.parse_args()
        jobs = build_jobs(quick=args.quick)
        run_sweep(jobs, run_job, args.output,
                  key_fields=("method", "sigma", "seed"),
                  workers=args.workers, dry_run=args.dry_run,
                  summary_only=args.summary_only, summarize_fn=summarize)
"""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import tempfile
import time
from typing import Callable, Iterable, Optional, Sequence


def job_key(rec: dict, key_fields: Sequence[str]) -> tuple:
    """Stable identity of a job/record: the tuple of its key fields
    (missing fields -> None, so optional axes like 'sigma' are safe)."""
    return tuple(rec.get(f, None) for f in key_fields)


def load_existing(path: str) -> list[dict]:
    """Load previously-completed records (resume support)."""
    if not os.path.exists(path):
        return []
    with open(path) as f:
        data = json.load(f)
    records = data.get("records") if isinstance(data, dict) else data
    if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
        raise ValueError(f"Invalid sweep records in {path}")
    return records


def save_records(path: str, records: list[dict],
                 schema: str = "sweep.v1") -> None:
    parent = os.path.dirname(os.path.abspath(path))
    os.makedirs(parent, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", dir=parent,
                                         prefix=".sweep-", delete=False) as f:
            temp_path = f.name
            json.dump({"records": records, "schema": schema}, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, path)
    finally:
        if temp_path is not None and os.path.exists(temp_path):
            os.unlink(temp_path)


def standard_argparser(description: str = "") -> argparse.ArgumentParser:
    """The house CLI convention for sweep drivers."""
    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--output", default=None)
    ap.add_argument("--quick", action="store_true",
                    help="reduced grid for smoke runs (driver-defined)")
    ap.add_argument("--dry-run", action="store_true",
                    help="list remaining jobs without running")
    ap.add_argument("--summary-only", action="store_true",
                    help="summarize the existing output file and exit")
    return ap


def run_sweep(jobs: Iterable[dict],
              run_job: Callable[[dict], dict],
              output_path: str,
              key_fields: Sequence[str],
              workers: int = 1,
              schema: str = "sweep.v1",
              dry_run: bool = False,
              summary_only: bool = False,
              summarize_fn: Optional[Callable[[list[dict]], None]] = None,
              save_every: int = 10,
              mp_context: str = "spawn",
              label: str = "sweep",
              quiet: bool = False) -> list[dict]:
    """Run (the remaining part of) a pre-registered job grid, resume-safely.

    Args:
        jobs: full pre-registered job list (dicts; must carry key_fields).
        run_job: top-level callable job -> record (record must echo the
            key fields; raising inside a worker aborts the sweep — keep
            per-job error handling inside run_job if partial failure is
            acceptable).
        output_path: keyed-JSON output file ({"records": [...], "schema"}).
        key_fields: fields identifying a job (e.g. ("method","sigma","seed")).
        workers: 1 = sequential (in-process); >1 = mp.Pool(workers).
        mp_context: "spawn" (default, torch-safe) or "fork".
        summarize_fn: optional records -> None, called at the end (and
            for summary_only).

    Returns the full record list (existing + newly computed).
    """
    jobs = list(jobs)
    existing = load_existing(output_path)

    if summary_only:
        if summarize_fn is not None:
            summarize_fn(existing)
        return existing

    done = {job_key(r, key_fields) for r in existing}
    remaining = [j for j in jobs if job_key(j, key_fields) not in done]
    total = len(jobs)

    if not quiet:
        print(f"\n{label}: total {total}, done {total - len(remaining)}, "
              f"remaining {len(remaining)}, workers {workers}")

    if dry_run:
        for j in remaining[:50]:
            print(f"  {j}")
        if len(remaining) > 50:
            print(f"  ... ({len(remaining) - 50} more)")
        return existing

    if not remaining:
        if not quiet:
            print("All done!")
        if summarize_fn is not None:
            summarize_fn(existing)
        return existing

    records = list(existing)
    t0 = time.time()

    def _progress(rec: dict) -> None:
        if quiet:
            return
        n_new = len(records) - len(existing)
        dt = time.time() - t0
        rate = n_new / dt if dt > 0 else 0.0
        eta_s = (len(remaining) - n_new) / rate if rate > 0 else float("inf")
        key_str = " ".join(f"{f}={rec.get(f)}" for f in key_fields)
        print(f"[{len(records)}/{total}] {key_str} "
              f"(rate {rate:.2f}/s, ETA {eta_s / 60:.1f}m)", flush=True)

    if workers <= 1:
        for j in remaining:
            rec = run_job(j)
            records.append(rec)
            _progress(rec)
            if len(records) % save_every == 0:
                save_records(output_path, records, schema)
    else:
        ctx = mp.get_context(mp_context)
        with ctx.Pool(workers) as pool:
            for rec in pool.imap_unordered(run_job, remaining):
                records.append(rec)
                _progress(rec)
                if len(records) % save_every == 0:
                    save_records(output_path, records, schema)

    save_records(output_path, records, schema)
    if summarize_fn is not None:
        summarize_fn(records)
    if not quiet:
        print(f"Saved to {output_path}")
    return records
