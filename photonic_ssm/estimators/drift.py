# NEW (S0.9b, PR-16, 2026-07-22) — the drift model + deploy-then-drift
# protocol. Tests whether in-situ retraining beats a stale offline calibration
# once the substrate drifts (the §5.5 advantage axis). Drift magnitude is
# literature-sourced: free-running SiN resonance drift ≈ 341 MHz std / 24 h
# (Dacha et al., Nat. Photonics 2025, arXiv:2506.21692) = σ(24h) ≈ 24 κ_i at
# C-2 (κ_i/2π ≈ 14.2 MHz). Random walk: σ²(t) = D·t, D = 24 κ_i²/h.
# Full spec: shared/preregistration.md PR-16; source memo
# docs/s0_L/drift_research_2026-07-22.md.

from __future__ import annotations

import math

import torch

from .harness import EVAL_SEED_BASE, eval_ser, train  # noqa: F401

# --- drift magnitude anchor (PR-16 §16.1) --------------------------------
SIGMA_24H_KI = 24.0            # σ(24 h) in units of κ_i, from 341 MHz/24h @ C-2
D_PER_HOUR = SIGMA_24H_KI ** 2 / 24.0    # random-walk diffusion, κ_i²/hour = 24


def sigma_step_ki(spacing_minutes: float) -> float:
    """RW per-step std (in κ_i units) for a deployment step of the given
    wall-clock spacing, calibrated to the 341 MHz/24h anchor."""
    return math.sqrt(D_PER_HOUR * spacing_minutes / 60.0)


def elapsed_minutes(sigma_step: float) -> float:
    """Inverse: the wall-clock spacing a given per-step σ corresponds to."""
    return (sigma_step ** 2) / D_PER_HOUR * 60.0


# --- correlation regimes (PR-16 §16.3) -----------------------------------
def drift_increment(rng: torch.Generator, N: int, sigma_step: float,
                    regime: str, ki: float, dtype=torch.float64
                    ) -> torch.Tensor:
    """One RW increment on the per-ring detuning δ (rad/s). `regime`:
    'common' — one shared Wiener increment on all rings (whole-chip thermal
    wander); 'independent' — i.i.d. per-ring (local drift)."""
    scale = sigma_step * ki
    if regime == "common":
        z = torch.randn(1, generator=rng, dtype=dtype)
        return z.expand(N).clone() * scale
    if regime == "independent":
        return torch.randn(N, generator=rng, dtype=dtype) * scale
    raise ValueError(f"regime must be 'common'|'independent', got {regime!r}")


# --- the deploy-then-drift protocol (PR-16 §16.2) ------------------------
ARMS = {
    # arm -> (t=0 convergence method, per-step drift-phase method, relock?)
    "insitu-pat":    ("pat-both",       "pat-both",  False),
    "insitu-spsa":   ("spsa",           "spsa",      False),
    "offline-head":  ("offline-deploy", "head-only", False),
    "offline-relock":("offline-deploy", "head-only", True),
}


def deploy_then_drift(arm: str, run_seed: int, regime: str, K: int,
                      b_updates: int, sigma_step: float, n_converge: int,
                      cell: str = "C-2"):
    """Converge at t=0, then step K times: apply a drift increment to δ, let
    the arm adapt for `b_updates` on the (now-drifted) device, evaluate SER.
    Returns {arm, regime, ser0, ser_traj:[(k, ser)], device_passes,
    delta_rms_ki:[...]}. Offline arms adapt head-only (+global re-lock for
    'offline-relock', which subtracts the common-mode shift = a laser re-lock);
    in-situ arms retrain the recurrence {δ,κ_ext,μ}+head."""
    conv_method, drift_method, relock = ARMS[arm]
    led0, sub, head = train(conv_method, cell, run_seed, n_converge,
                            eval_every=None, return_state=True)
    ki = float(sub.kappa_i)
    dtype = sub.delta.dtype
    with torch.no_grad():
        delta0_mean = float(sub.delta.mean())
        # y_scale re-measured on the current device for the t=0 eval.
        from .harness import ase_gen, encode_drive, fresh_batch
        u0, _ = fresh_batch(run_seed, 0)
        y0 = sub.forward_intensity(encode_drive(u0).unsqueeze(-1),
                                   generator=ase_gen(run_seed, 0, 0))
        y_scale0 = float(y0.mean()) + 1e-30
    ser0 = eval_ser(sub, head, y_scale0)

    rng = torch.Generator().manual_seed(run_seed + 777)
    ser_traj, delta_rms = [], []
    total_passes = 0
    for k in range(1, K + 1):
        inc = drift_increment(rng, sub.N, sigma_step, regime, ki, dtype)
        with torch.no_grad():
            sub.delta.add_(inc)
            if relock:            # global re-lock: remove the common-mode shift
                sub.delta.add_(-(sub.delta.mean() - delta0_mean))
            sub.clamp_to_bounds()
            delta_rms.append(float((sub.delta / ki).std()))
        # adapt for b_updates on the drifted device (reuses train() machinery);
        # a distinct per-step seed keeps the fresh-noise streams independent.
        led, sub, head = train(drift_method, cell, run_seed * 1000 + k,
                               b_updates, warm=(sub, head),
                               eval_every=b_updates, return_state=True)
        ser_k = led["eval_trace"][-1][2] if led["eval_trace"] else float("nan")
        ser_traj.append((k, ser_k))
        total_passes += led["device_passes"]
    return {"arm": arm, "regime": regime, "cell": cell, "run_seed": run_seed,
            "K": K, "b_updates": b_updates, "sigma_step_ki": sigma_step,
            "spacing_min": elapsed_minutes(sigma_step),
            "ser0": ser0, "ser_traj": ser_traj,
            "delta_rms_ki": delta_rms, "device_passes": total_passes}
