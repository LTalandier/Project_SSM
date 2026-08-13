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

# PR-17 §17.4 (frozen 2026-07-27) — T-A-L: the frozen channel plus a −6 dB
# replica of its past-tap profile delayed by 7 symbols (a second reflection).
# c_L[k] = c[k] for k ≤ 7; c_L[7+m] = 0.5·c[m], m = 1..7. Span 7 → 14.
TA_LONG_TAPS = dict(_ISI_TAPS)
TA_LONG_TAPS.update({7 + m: 0.5 * _ISI_TAPS[m] for m in range(1, 8)})


class JaegerHaasChannel:
    """The frozen T-A channel. `apply` maps a 4-PAM symbol stream d(n) to the
    received signal u(n) at the registered SNR. `taps=None` = the frozen
    PR-2 T-A ISI profile (bit-identical); PR-17 passes TA_LONG_TAPS."""

    def __init__(self, snr_dB: float = 28.0, taps: dict | None = None):
        self.snr_dB = float(snr_dB)
        self.taps = _ISI_TAPS if taps is None else taps

    def q(self, d: torch.Tensor) -> torch.Tensor:
        """Linear-ISI output q(n) = Σ_lag c[lag]·d(n−lag) (centered; edges use
        zero-padding via roll-and-mask). d: (T,) real."""
        T = d.shape[0]
        out = torch.zeros_like(d)
        for lag, c in self.taps.items():
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
                    seed: int | None = None, taps: dict | None = None
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
    ch = JaegerHaasChannel(snr_dB, taps=taps)
    u = ch.apply(d, generator=g)
    target = torch.zeros_like(d)
    if TARGET_DELAY < n_symbols:
        target[TARGET_DELAY:] = d[: n_symbols - TARGET_DELAY]
    return u, target, d


# ------------------------------------------------------------------ #
# PR-19 (🔒 SIGNED 2026-08-13) — T-D: unipolar despread-31.
# m-sequence of the primitive polynomial x⁵+x²+1 over GF(2), state 11111,
# Fibonacci recurrence s_n = s_{n−5} ⊕ s_{n−2}; the resulting 31-chip code is
# pinned verbatim below and gate-tested (length 31, weight 16, all 31 cyclic
# 5-bit windows distinct = the m-sequence property).
# ------------------------------------------------------------------ #

def _mseq31() -> list:
    s = [1, 1, 1, 1, 1]
    for n in range(5, 31):
        s.append(s[n - 5] ^ s[n - 2])
    return s


MSEQ31 = _mseq31()
TD_L = 31                    # chips per symbol (PR-19 §19.1)
TD_DECISION_CHIP = 30        # decision position: last chip of the symbol


def make_td_dataset(n_symbols: int = 64, snr_dB: float = 28.0,
                    seed: int | None = None, taps: dict | None = None
                    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """PR-19 T-D sequence. Returns (u, target, mask):
      u      : (31·n_symbols,) received chip stream — each 4-PAM symbol spread
               by MSEQ31, off-chips at the lowest PAM level a(0) = −3 (no new
               encoder levels), then the frozen Jaeger–Haas channel at chip
               rate (ISI + cubic + AWGN, verbatim).
      target : symbol PAM level at decision positions (last chip), 0 elsewhere.
      mask   : bool, True at decision positions.
    Same streaming-seed convention as make_ta_dataset."""
    g = None
    if seed is not None:
        g = torch.Generator().manual_seed(int(seed))
    idx = torch.randint(0, 4, (n_symbols,), generator=g)
    levels = torch.tensor(PAM_LEVELS, dtype=torch.float64)
    d_sym = levels[idx]
    code = torch.tensor(MSEQ31, dtype=torch.float64)
    chips = d_sym[:, None] * code[None, :] \
        + PAM_LEVELS[0] * (1.0 - code)[None, :]
    d = chips.reshape(-1)
    ch = JaegerHaasChannel(snr_dB, taps=taps)
    u = ch.apply(d, generator=g)
    target = torch.zeros_like(d)
    mask = torch.zeros(d.shape[0], dtype=torch.bool)
    pos = torch.arange(n_symbols) * TD_L + TD_DECISION_CHIP
    target[pos] = d_sym
    mask[pos] = True
    return u, target, mask


def symbol_error_rate_td(pred: torch.Tensor, target: torch.Tensor,
                         mask: torch.Tensor, warmup_symbols: int = 2) -> float:
    """SER at the T-D decision positions, skipping the first `warmup_symbols`
    symbols (the ISI/settling transient; PR-19 §19.1)."""
    p = pred[mask][warmup_symbols:]
    t = target[mask][warmup_symbols:]
    return float((nearest_pam(p) != t).double().mean())


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
