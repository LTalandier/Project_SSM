# NEW (S0.10, PR-17, 2026-07-27) — gate tests for the eval-F protocol and the
# T-A-L task override.

import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from photonic_ssm.tasks.equalization import (  # noqa: E402
    _ISI_TAPS, TA_LONG_TAPS, make_ta_dataset)


def test_default_taps_bit_identical():
    """taps=None must reproduce the frozen T-A stream bit-identically
    (PR-17 §17.4 gate)."""
    u1, t1, d1 = make_ta_dataset(256, 28.0, seed=1234)
    u2, t2, d2 = make_ta_dataset(256, 28.0, seed=1234, taps=None)
    assert torch.equal(u1, u2) and torch.equal(t1, t2) and torch.equal(d1, d2)


def test_ta_long_frozen_coefficients():
    """T-A-L = frozen T-A + 0.5x past-tap replica delayed by 7 (PR-17 §17.4)."""
    for k, c in _ISI_TAPS.items():
        assert TA_LONG_TAPS[k] == c
    for m in range(1, 8):
        assert TA_LONG_TAPS[7 + m] == 0.5 * _ISI_TAPS[m]
    assert max(TA_LONG_TAPS) == 14 and len(TA_LONG_TAPS) == 17


def test_ta_long_changes_stream():
    """The override must actually change the received signal (not the symbols
    or targets, which are channel-independent)."""
    u1, t1, d1 = make_ta_dataset(256, 28.0, seed=1234)
    u2, t2, d2 = make_ta_dataset(256, 28.0, seed=1234, taps=TA_LONG_TAPS)
    assert torch.equal(d1, d2) and torch.equal(t1, t2)
    assert not torch.equal(u1, u2)


def test_eval_fine_batch_count():
    """eval-F = 52 batches -> 99,840 scored symbols (PR-17 §17.1)."""
    from photonic_ssm.estimators.harness import (
        BATCH, EVAL_FINE_BATCHES, T_SYMBOLS, WARMUP)
    assert EVAL_FINE_BATCHES * BATCH * (T_SYMBOLS - WARMUP) == 99_840
