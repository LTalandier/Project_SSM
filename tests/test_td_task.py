# NEW (PR-19, 🔒 2026-08-13) — T-D task gates: the pinned m-sequence, the
# dataset invariants, the harness threading, and the arm guard.
import sys
import os

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from photonic_ssm.tasks.equalization import (   # noqa: E402
    MSEQ31, PAM_LEVELS, make_td_dataset, symbol_error_rate_td)
from photonic_ssm.estimators.harness import train, fresh_batch_td  # noqa: E402


def test_mseq31_is_an_m_sequence():
    assert len(MSEQ31) == 31
    assert sum(MSEQ31) == 16                      # weight of any 31-chip m-seq
    ext = MSEQ31 + MSEQ31
    windows = {tuple(ext[i:i + 5]) for i in range(31)}
    assert len(windows) == 31                     # all nonzero 5-bit states
    assert (0, 0, 0, 0, 0) not in windows


def test_td_dataset_invariants():
    u, target, mask = make_td_dataset(64, 28.0, seed=1234)
    assert u.shape == (1984,) and mask.sum() == 64
    pos = mask.nonzero().flatten()
    assert bool(((pos % 31) == 30).all())
    lv = set(float(x) for x in target[mask])
    assert lv.issubset(set(PAM_LEVELS))
    # determinism
    u2, t2, _ = make_td_dataset(64, 28.0, seed=1234)
    assert torch.equal(u, u2) and torch.equal(target, t2)


def test_td_ser_helper_perfect_prediction():
    _, target, mask = make_td_dataset(64, 28.0, seed=7)
    assert symbol_error_rate_td(target, target, mask) == 0.0


def test_td_batch_and_train_smoke():
    u, t, m = fresh_batch_td(11, 1)
    assert u.shape == (8, 1984) and t.shape == (8, 1984)
    led = train("bptt", "C-1", run_seed=11, n_updates=6, N=8,
                eval_every=None, task="td")
    assert all(torch.isfinite(torch.tensor(led["loss_trace"])).tolist())
    assert 0.0 <= led["ser_final"] <= 1.0


def test_td_arm_guard():
    try:
        train("spsa", "C-1", run_seed=11, n_updates=2, N=8, task="td")
        raise AssertionError("guard did not fire")
    except ValueError as e:
        assert "bptt/pat" in str(e)
