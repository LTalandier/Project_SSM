# NEW (task S0.4a phase 1, 2026-07-07) — the shared T-A training harness:
# frozen PR-2 hybrid (fixed affine encoder → substrate → R2 intensity →
# digital 8-tap linear head), PR-6 common-θ₀/common-stream conventions,
# PR-7 device/digital ledgers. Sets no values beyond the S0.4a spec
# (task_queue.md 2026-07-07): T=256, batch 8, 28 dB, head lags 0..7,
# warmup 16, smoke learning rates.
"""S0.4a training harness (one loop, four methods).

Methods: "bptt" (the PR-3 reference — autodiff THROUGH the substrate;
digital ledger only, never a bake-off contestant), "pat-<family>"
(PATEstimator; families per PR-5), "spsa" (the salvaged
PerturbationAdaptor over the P2 set), "head-only" (frozen substrate,
head trained — the reservoir-flavored context arm, ungated).

Fairness conventions implemented here (PR-6):
  * common per-seed θ₀ (δ-band [−κᵢ,κᵢ] linspace, r₀=0.3, μ_c=0.3κᵢ) and
    common per-seed data stream (generator = f(run_seed, iteration),
    method-independent);
  * ASE fresh per pass, independent across methods (generator = f(run_seed,
    iteration, pass, method) — noise is NOT shared);
  * identical digital-head cadence (one Adam step per update, same lr);
  * clamp to the operative band [R_MIN_SATURATING, 3] after every in-situ
    update.
"""

from __future__ import annotations

from typing import Optional

import torch

from ..substrate import cells as cellmod
from ..substrate import normalization as O2
from ..substrate.dissipative_ring import DissipativeRingSubstrate
from ..tasks.equalization import make_ta_dataset, symbol_error_rate
from .pat import PATEstimator
from .spsa import PerturbationAdaptor

U_REF = 6.0          # fixed encoder input range [−U_REF, U_REF] (S0.4a spec)
HEAD_LAGS = 8        # PR-2 registered tap window {y(n−m), m=0..7}
WARMUP = 16          # PR-2/T-A edge transient skipped in loss + SER
T_SYMBOLS = 256      # S0.4a smoke sequence length
BATCH = 8            # PR-6 §D batch (= device passes per forward eval, PR-7)
SNR_DB = 28.0        # PR-2 headline cell
RESOLVED_TAPS = (2, 11, 20, 29)   # S0.4-0 resolved B {3,12,21,30}, 0-based


def encode_drive(u: torch.Tensor) -> torch.Tensor:
    """Fixed affine intensity encoder (S0.4a spec): u∈[−U_REF,U_REF] →
    P ∈ [0, P_pk] (T-A P_pk = 2·P̄₀; §N E₀ scale = 1 at θ₀) → photon-flux
    amplitude √(P/ħν). Not trainable (registered simplification)."""
    P_pk = O2.P_pk_for_family("T-A")
    frac = ((u + U_REF) / (2.0 * U_REF)).clamp(0.0, 1.0)
    return torch.sqrt(frac * P_pk / O2.H_NU_J)


def taps_for_N(N: int) -> tuple:
    """The resolved B at N=32; the proportional image of its geometry for
    other (smoke) cells — round(t·N/32), deduped (documented S0.4a rule;
    the §B gate itself was measured and binds at C-2/N=32)."""
    if N == 32:
        return RESOLVED_TAPS
    return tuple(sorted({min(N - 1, max(0, round(t * N / 32)))
                         for t in RESOLVED_TAPS}))


def make_substrate(cell_label: str, seed: int, N: Optional[int] = None
                   ) -> DissipativeRingSubstrate:
    """Common θ₀ (PR-6 §B): δ linspace over [−κᵢ,+κᵢ] (§D numeric band),
    r₀ = 0.3, connected chain μ_c = 0.3κᵢ, resolved input taps."""
    sub = DissipativeRingSubstrate.from_cell(
        cell_label, N=N, clock_GSps=2.0, seed=seed, input_taps=(0,))
    sub = DissipativeRingSubstrate.from_cell(
        cell_label, N=N, clock_GSps=2.0, seed=seed,
        input_taps=taps_for_N(sub.N))
    ki = float(sub.kappa_i)
    with torch.no_grad():
        sub.delta.copy_(torch.linspace(-1.0, 1.0, sub.N,
                                       dtype=sub.delta.dtype) * ki)
        sub.kappa_ext.fill_(cellmod.R0_THETA0 * ki)
        sub.mu_chain.fill_(0.3 * ki)
    return sub


class TapHead(torch.nn.Module):
    """Digital linear head over the registered lag window {y(n−m), m=0..7}."""

    def __init__(self):
        super().__init__()
        self.lin = torch.nn.Linear(HEAD_LAGS, 1, dtype=torch.float64)

    @staticmethod
    def taps(y: torch.Tensor) -> torch.Tensor:
        """(batch,T) → (batch,T,HEAD_LAGS) lagged copies (zero left-pad)."""
        cols = []
        for m in range(HEAD_LAGS):
            cols.append(torch.nn.functional.pad(y, (m, 0))[..., : y.shape[-1]])
        return torch.stack(cols, dim=-1)

    def forward(self, y_norm: torch.Tensor) -> torch.Tensor:
        return self.lin(self.taps(y_norm)).squeeze(-1)


def mse_loss(pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    return ((pred[..., WARMUP:] - target[..., WARMUP:]) ** 2).mean()


def fresh_batch(run_seed: int, it: int):
    """PR-6 common-per-seed data stream: batch of fresh T-A sequences whose
    seeds depend only on (run_seed, iteration) — method-independent."""
    us, ts = [], []
    for b in range(BATCH):
        u, tgt, _ = make_ta_dataset(T_SYMBOLS, SNR_DB,
                                    seed=run_seed * 1_000_003 + it * 101 + b)
        us.append(u)
        ts.append(tgt)
    return torch.stack(us), torch.stack(ts)


def ase_gen(run_seed: int, it: int, tag: int) -> torch.Generator:
    """Fresh, method/pass-specific ASE stream (PR-11: noise never shared)."""
    return torch.Generator().manual_seed(
        (run_seed * 7_368_787 + it * 613 + tag) % (2 ** 62))


class RunLedger(dict):
    """PR-7 ledgers + loss trace."""

    def __init__(self):
        super().__init__(device_passes=0, digital_passes=0, loss_trace=[],
                         ser_final=None)


def train(method: str, cell_label: str, run_seed: int, n_updates: int,
          N: Optional[int] = None, lr_phys_frac: float = 1e-3,
          lr_head: float = 3e-2, spsa_c_frac: float = 0.01) -> RunLedger:
    """One training run. `method` ∈ {"bptt","pat-perfect","pat-M-par",
    "pat-M-struct","pat-both","spsa","head-only"}. Smoke HPs from the S0.4a
    spec; the equal-HP *search* is S0.5 (PR-8)."""
    torch.manual_seed(run_seed)
    sub = make_substrate(cell_label, run_seed, N=N)
    ki = float(sub.kappa_i)
    head = TapHead()
    led = RunLedger()

    # Fixed per-seed output normalization (common across methods: same θ₀ +
    # same data stream + a method-independent ASE tag).
    u0, _ = fresh_batch(run_seed, 0)
    with torch.no_grad():
        y0 = sub.forward_intensity(encode_drive(u0).unsqueeze(-1),
                                   generator=ase_gen(run_seed, 0, 0))
        y_scale = float(y0.mean()) + 1e-30

    in_situ = [sub.delta, sub.kappa_ext, sub.mu_chain]
    opt_head = torch.optim.Adam(head.parameters(), lr=lr_head)
    method_base = method.split("-")[0]

    if method_base == "pat":
        family = method[len("pat-"):]
        est = PATEstimator(sub, family)
        opt_phys = torch.optim.Adam(in_situ, lr=lr_phys_frac * ki)
    elif method == "bptt":
        opt_phys = torch.optim.Adam(in_situ, lr=lr_phys_frac * ki)
    elif method == "spsa":
        state = {"u": None, "it": 0, "pass": 0}

        def spsa_forward(model, inputs):
            state["pass"] += 1
            return model.forward_intensity(
                inputs, generator=ase_gen(run_seed, state["it"],
                                          100 + state["pass"]))

        def spsa_loss(y, target):
            state["last_y"] = y.detach()      # reused for the head step
            with torch.no_grad():
                return mse_loss(head(y / y_scale), target)

        adaptor = PerturbationAdaptor(
            sub, spsa_loss, estimator="spsa", eps=spsa_c_frac * ki,
            lr=lr_phys_frac * ki, use_adam=True, rng_seed=run_seed,
            forward_fn=spsa_forward)
    elif method != "head-only":
        raise ValueError(method)

    for it in range(1, n_updates + 1):
        u_raw, target = fresh_batch(run_seed, it)
        u = encode_drive(u_raw).unsqueeze(-1)

        if method == "bptt":
            y = sub.forward_intensity(u, generator=ase_gen(run_seed, it, 1))
            loss = mse_loss(head(y / y_scale), target)
            opt_head.zero_grad()
            for p in in_situ:
                p.grad = None
            loss.backward()
            torch.nn.utils.clip_grad_norm_(
                in_situ + list(head.parameters()), 1.0)
            opt_phys.step()
            opt_head.step()
            led["digital_passes"] += 2 * BATCH      # reference: digital only
            loss_val = float(loss.detach())
        elif method_base == "pat":
            def pat_loss(y_pat):
                return mse_loss(head(y_pat / y_scale), target)
            opt_head.zero_grad()
            for p in in_situ:
                p.grad = None
            loss_val, _ = est.step(u, pat_loss,
                                   generator=ase_gen(run_seed, it, 2))
            torch.nn.utils.clip_grad_norm_(
                in_situ + list(head.parameters()), 1.0)
            opt_phys.step()
            opt_head.step()
        elif method == "spsa":
            state["it"] = it
            loss_val = adaptor.step(u, target)      # 2 physical evals only
            # Digital head step REUSES the last (−c) probe measurement —
            # O(c) off nominal; no extra device pass (PR-7 SPSA = 2/update).
            pred = head(state["last_y"] / y_scale)
            loss_h = mse_loss(pred, target)
            opt_head.zero_grad()
            loss_h.backward()
            opt_head.step()
        else:                                        # head-only
            with torch.no_grad():
                y = sub.forward_intensity(u, generator=ase_gen(run_seed, it, 4))
            led["device_passes"] += BATCH
            pred = head(y.detach() / y_scale)
            loss = mse_loss(pred, target)
            opt_head.zero_grad()
            loss.backward()
            opt_head.step()
            loss_val = float(loss.detach())

        if method_base in ("bptt", "pat"):
            sub.clamp_to_bounds()
        elif method == "spsa":
            sub.clamp_to_bounds()
        led["loss_trace"].append(loss_val)

    # Ledger totals (PR-7).
    if method_base == "pat":
        led["device_passes"] = est.n_device_passes
        led["digital_passes"] = est.n_digital_passes
    elif method == "spsa":
        led["device_passes"] += adaptor.n_forward_equivalents * BATCH
        led["digital_passes"] = 0

    # Final SER on one fresh held-out batch (context, ungated at S0.4a).
    u_raw, target = fresh_batch(run_seed, 999_983)
    with torch.no_grad():
        y = sub.forward_intensity(encode_drive(u_raw).unsqueeze(-1),
                                  generator=ase_gen(run_seed, 999_983, 5))
        pred = head(y / y_scale)
        led["ser_final"] = sum(
            symbol_error_rate(pred[b], target[b], warmup=WARMUP)
            for b in range(BATCH)) / BATCH
    led["in_situ_r"] = (sub.kappa_ext.detach() / ki).tolist()
    return led
