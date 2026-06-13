# NEW (task S0.3-1, deliverable 9) — the frozen PR-2 T-A task generator.
# Verbatim [EV] Jaeger–Haas channel (arXiv:1501.03024, restating Jaeger & Haas
# Science 304:78 (2004)). Sets no values: the coefficients, target index, and
# SNR grid are frozen PR-2 entries.
"""T-A — Jaeger–Haas nonlinear channel equalization (PR-2 headline task).

4-PAM i.i.d. symbols d(n) ∈ {−3,−1,1,3} pass through a linear-ISI +
memoryless-cubic channel with AWGN; the task is to recover d(n−2) (the
canonical 2-sample-delay convention, frozen by PR-2 — PF-F9c invariant: the
verbatim *centered* generator's output at time n estimates d(n−2); do NOT
re-shift the polynomial to causal form while keeping the target index).

    q(n) = 0.08 d(n+2) − 0.12 d(n+1) + d(n) + 0.18 d(n−1) − 0.1 d(n−2)
           + 0.091 d(n−3) − 0.05 d(n−4) + 0.04 d(n−5) + 0.03 d(n−6) + 0.01 d(n−7)
    u(n) = q(n) + 0.036 q²(n) − 0.011 q³(n) + ν(n),   ν Gaussian at SNR.

Metric: SER (symbol error rate after a nearest-4-PAM decision). Registered
SNR grid {16, 24, 28, 32} dB, headline cell 28 dB (PR-2).
"""

from __future__ import annotations

import math

import torch

PAM_LEVELS = (-3.0, -1.0, 1.0, 3.0)
# Verbatim centered ISI taps, indexed by lag relative to n: lag −2 (future)
# … lag +7 (past). q(n) = Σ_lag c[lag] · d(n − lag).
_ISI_TAPS = {
    -2: 0.08, -1: -0.12, 0: 1.0, 1: 0.18, 2: -0.1,
    3: 0.091, 4: -0.05, 5: 0.04, 6: 0.03, 7: 0.01,
}
TARGET_DELAY = 2          # recover d(n−2)


class JaegerHaasChannel:
    """The frozen T-A channel. `apply` maps a 4-PAM symbol stream d(n) to the
    received signal u(n) at the registered SNR."""

    def __init__(self, snr_dB: float = 28.0):
        self.snr_dB = float(snr_dB)

    def q(self, d: torch.Tensor) -> torch.Tensor:
        """Linear-ISI output q(n) = Σ_lag c[lag]·d(n−lag) (centered; edges use
        zero-padding via roll-and-mask). d: (T,) real."""
        T = d.shape[0]
        out = torch.zeros_like(d)
        for lag, c in _ISI_TAPS.items():
            shifted = torch.zeros_like(d)
            if lag >= 0:
                if lag < T:
                    shifted[lag:] = d[: T - lag]
            else:
                k = -lag
                if k < T:
                    shifted[: T - k] = d[k:]
            out = out + c * shifted
        return out

    def apply(self, d: torch.Tensor, generator: torch.Generator | None = None
              ) -> torch.Tensor:
        """Received u(n) = q + 0.036 q² − 0.011 q³ + ν, ν Gaussian at SNR
        (noise power set relative to the clean signal power)."""
        q = self.q(d)
        clean = q + 0.036 * q ** 2 - 0.011 * q ** 3
        sig_power = float((clean ** 2).mean())
        noise_power = sig_power / (10.0 ** (self.snr_dB / 10.0))
        noise = math.sqrt(noise_power) * torch.randn(
            clean.shape, generator=generator, dtype=clean.dtype)
        return clean + noise


def make_ta_dataset(n_symbols: int, snr_dB: float = 28.0,
                    seed: int | None = None
                    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Generate one T-A sequence. Returns (u, target, d):
      u      : (T,) received signal (the substrate drive).
      target : (T,) d(n−2) — the symbol to recover.
      d      : (T,) transmitted 4-PAM symbols.
    Streaming-fresh i.i.d. draws (PR-2a) when called per iteration with a
    fresh seed."""
    g = None
    if seed is not None:
        g = torch.Generator().manual_seed(int(seed))
    idx = torch.randint(0, 4, (n_symbols,), generator=g)
    levels = torch.tensor(PAM_LEVELS, dtype=torch.float64)
    d = levels[idx]
    ch = JaegerHaasChannel(snr_dB)
    u = ch.apply(d, generator=g)
    target = torch.zeros_like(d)
    if TARGET_DELAY < n_symbols:
        target[TARGET_DELAY:] = d[: n_symbols - TARGET_DELAY]
    return u, target, d


def nearest_pam(x: torch.Tensor) -> torch.Tensor:
    """Nearest-4-PAM decision (the SER decision rule)."""
    levels = torch.tensor(PAM_LEVELS, dtype=x.dtype, device=x.device)
    return levels[(x.reshape(-1, 1) - levels.reshape(1, -1)).abs().argmin(dim=1)]


def symbol_error_rate(pred: torch.Tensor, target: torch.Tensor,
                      warmup: int = 16) -> float:
    """SER after a nearest-4-PAM decision, skipping `warmup` edge symbols (the
    ISI/target-delay transient)."""
    p = nearest_pam(pred[warmup:])
    t = target[warmup:]
    return float((p != t).double().mean())
