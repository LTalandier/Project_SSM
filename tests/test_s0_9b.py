# NEW (S0.9b, PR-16, 2026-07-22) — drift-model gate tests.
import math
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from photonic_ssm.estimators.drift import (  # noqa: E402
    D_PER_HOUR, SIGMA_24H_KI, drift_increment, elapsed_minutes,
    sigma_step_ki)


def test_rw_variance_calibration():
    """G1: the RW is calibrated so accumulated std hits σ(24h)=24κ_i.
    Var grows ∝ number of steps (independent increments)."""
    ki = 1.0
    spacing = 5.0                       # minutes/step
    ss = sigma_step_ki(spacing)
    n_steps = int(round(24 * 60 / spacing))     # steps to fill 24 h
    # accumulated variance = n_steps * ss^2 == SIGMA_24H_KI^2
    acc_std = math.sqrt(n_steps * ss ** 2)
    assert abs(acc_std - SIGMA_24H_KI) / SIGMA_24H_KI < 1e-6, acc_std
    # round-trip spacing<->sigma
    assert abs(elapsed_minutes(ss) - spacing) < 1e-9


def test_rw_variance_empirical():
    """G1b: empirically, summing K independent increments gives variance
    ≈ K·(σ_step·κ_i)² (independent regime)."""
    ki, ss, N = 3.0e7, 0.4, 32
    rng = torch.Generator().manual_seed(1)
    K = 4000
    acc = torch.zeros(N, dtype=torch.float64)
    for _ in range(K):
        acc += drift_increment(rng, N, ss, "independent", ki)
    expected_std = math.sqrt(K) * ss * ki
    emp = float(acc.std())
    assert 0.85 < emp / expected_std < 1.15, (emp, expected_std)


def test_common_mode_is_uniform():
    """G2: common-mode increment is identical across all rings; independent
    is not."""
    ki, ss, N = 1.0, 0.5, 16
    rng = torch.Generator().manual_seed(2)
    com = drift_increment(rng, N, ss, "common", ki)
    assert float(com.std()) < 1e-12, "common increment must be uniform"
    assert float(com.abs().mean()) > 0                    # and nonzero
    ind = drift_increment(rng, N, ss, "independent", ki)
    assert float(ind.std()) > 1e-3, "independent increment must vary per ring"


def test_diffusion_constant():
    """G3: D = σ(24h)²/24h reproduces the anchor (24 κ_i²/hour)."""
    assert abs(D_PER_HOUR - 24.0) < 1e-9
    # σ over 1 h = sqrt(24) κ_i; over 10 min = sqrt(4)=2 κ_i
    assert abs(sigma_step_ki(60.0) - math.sqrt(24.0)) < 1e-9
    assert abs(sigma_step_ki(10.0) - 2.0) < 1e-9


def test_zero_sigma_is_no_drift():
    """G4: σ_step=0 leaves δ untouched (zero-drift ≡ static substrate)."""
    rng = torch.Generator().manual_seed(3)
    inc = drift_increment(rng, 32, 0.0, "independent", 3.0e7)
    assert float(inc.abs().max()) == 0.0


if __name__ == "__main__":
    for fn in [test_rw_variance_calibration, test_rw_variance_empirical,
               test_common_mode_is_uniform, test_diffusion_constant,
               test_zero_sigma_is_no_drift]:
        fn()
        print(f"{fn.__name__}  ✓")
    print("all S0.9b gate tests passed")
