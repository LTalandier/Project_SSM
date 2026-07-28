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
from .adjoint import AdjointEstimator
from .pat import MPAR_LEVELS, PATEstimator, scaled_mpar
from .rhel import RHELEstimator
from .spsa import PerturbationAdaptor

U_REF = 6.0          # fixed encoder input range [−U_REF, U_REF] (S0.4a spec)
HEAD_LAGS = 8        # PR-2 registered tap window {y(n−m), m=0..7}
WARMUP = 16          # PR-2/T-A edge transient skipped in loss + SER
T_SYMBOLS = 256      # S0.4a smoke sequence length
TASK_TAPS = None     # PR-17: None = frozen T-A; set to TA_LONG_TAPS for T-A-L
EVAL_FINE_BATCHES = 52   # PR-17 eval-F: 52*8*240 = 99,840 scored symbols
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


def make_substrate(cell_label: str, seed: int, N: Optional[int] = None,
                   r0: Optional[float] = None) -> DissipativeRingSubstrate:
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
        sub.kappa_ext.fill_((cellmod.R0_THETA0 if r0 is None else r0) * ki)
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
                                    seed=run_seed * 1_000_003 + it * 101 + b,
                                    taps=TASK_TAPS)
        us.append(u)
        ts.append(tgt)
    return torch.stack(us), torch.stack(ts)


def ase_gen(run_seed: int, it: int, tag: int) -> torch.Generator:
    """Fresh, method/pass-specific ASE stream (PR-11: noise never shared)."""
    return torch.Generator().manual_seed(
        (run_seed * 7_368_787 + it * 613 + tag) % (2 ** 62))


class RunLedger(dict):
    """PR-7 ledgers + loss trace (+ optional eval trace)."""

    def __init__(self):
        super().__init__(device_passes=0, digital_passes=0, loss_trace=[],
                         ser_final=None, eval_trace=[])


EVAL_SEED_BASE = 900_001     # reserved held-out eval streams (never trained)


def eval_ser(sub, head, y_scale, n_batches: int = 2) -> float:
    """Held-out eval-SER on the FIXED reserved streams (identical for every
    method and seed — PR-8 eval protocol). Eval device passes are excluded
    from the budget B and reported nowhere near the rank (diagnostic
    measurement, uniform across methods)."""
    total = 0.0
    n = 0
    with torch.no_grad():
        for j in range(n_batches):
            us, ts = [], []
            for b in range(BATCH):
                u, tgt, _ = make_ta_dataset(
                    T_SYMBOLS, SNR_DB, seed=EVAL_SEED_BASE + j * 101 + b,
                    taps=TASK_TAPS)
                us.append(u)
                ts.append(tgt)
            u_raw, target = torch.stack(us), torch.stack(ts)
            y = sub.forward_intensity(
                encode_drive(u_raw).unsqueeze(-1),
                generator=torch.Generator().manual_seed(
                    EVAL_SEED_BASE + 7 * j))
            pred = head(y / y_scale)
            for b in range(BATCH):
                total += symbol_error_rate(pred[b], target[b], warmup=WARMUP)
                n += 1
    return total / n


def final_fine_ser(sub, head, y_scale: float,
                   n_batches: int = EVAL_FINE_BATCHES) -> float:
    """PR-17 eval-F on the extended reserved streams, at the head's TRAINED
    normalization y_scale (train() ledger key "y_scale"). S0.10 erratum
    (2026-07-28): the original version re-measured y_scale on the trained
    device, which breaks every arm that moves kappa_ext (the head and its
    scale are one decoder); drift.deploy_then_drift is unaffected (its
    per-step re-measure tracks a near-unchanged device, the registered ser0
    convention)."""
    return eval_ser(sub, head, y_scale, n_batches=n_batches)


def train(method: str, cell_label: str, run_seed: int, n_updates: int,
          N: Optional[int] = None, lr_phys_frac: float = 1e-3,
          lr_head: float = 3e-2, spsa_c_frac: float = 0.01,
          eval_every: Optional[int] = None,
          gain_mode: Optional[str] = None,
          r0: Optional[float] = None, r_hi: Optional[float] = None,
          pin_kext: bool = False, mismatch_scale: float = 1.0,
          warm=None, return_state: bool = False):
    """One training run. `method` ∈ {"bptt","pat-perfect","pat-M-par",
    "pat-M-struct","pat-both","spsa","adjoint","rhel","rhel-ideal",
    "head-only"}. Smoke HPs from the S0.4a spec; the equal-HP *search* is
    S0.5 (PR-8). `mismatch_scale` (PR-5 §E / S0.9a) scales the M-par
    calibration/actuation gap for pat-* and offline-deploy; 1.0 == headline.
    `warm=(sub, head)` (S0.9b) continues on an EXISTING substrate+head instead
    of constructing fresh (the deploy-then-drift loop); `return_state` also
    returns (led, sub, head)."""
    torch.manual_seed(run_seed)
    if warm is not None:               # S0.9b: continue on a live (drifted) device
        sub, head = warm
    else:
        sub = make_substrate(cell_label, run_seed, N=N, r0=r0)
        if gain_mode is not None:      # PR-3 §A fixed-gain sensitivity spot
            sub.gain_mode = gain_mode
        if r_hi is not None:           # S0.6 sub-box (PR-12 R-ii)
            sub.r_hi_train = r_hi
        head = TapHead()
    ki = float(sub.kappa_i)
    led = RunLedger()

    # Fixed per-seed output normalization (common across methods: same θ₀ +
    # same data stream + a method-independent ASE tag).
    u0, _ = fresh_batch(run_seed, 0)
    with torch.no_grad():
        y0 = sub.forward_intensity(encode_drive(u0).unsqueeze(-1),
                                   generator=ase_gen(run_seed, 0, 0))
        y_scale = float(y0.mean()) + 1e-30

    # S0.6 arm B: κ_ext pinned at its init (damping = a fixed design point);
    # only {δ, μ} train. Arm A / default: the full P2 partition.
    in_situ = ([sub.delta, sub.mu_chain] if pin_kext
               else [sub.delta, sub.kappa_ext, sub.mu_chain])
    opt_head = torch.optim.Adam(head.parameters(), lr=lr_head)
    method_base = method.split("-")[0]

    if method_base == "pat":
        family = method[len("pat-"):]
        est = PATEstimator(sub, family, mismatch_scale=mismatch_scale)
        opt_phys = torch.optim.Adam(in_situ, lr=lr_phys_frac * ki)
    elif method == "adjoint":
        est = AdjointEstimator(sub)
        opt_phys = torch.optim.Adam(in_situ, lr=lr_phys_frac * ki)
    elif method in ("rhel", "rhel-ideal"):
        est = RHELEstimator(sub, ideal_echo=(method == "rhel-ideal"))
        opt_phys = torch.optim.Adam(in_situ, lr=lr_phys_frac * ki)
    elif method == "offline-deploy":
        # The §10 baseline (PR-5 F7.3 calibration-error unification): phase A
        # trains {δ, κ_ext, μ} + head fully DIGITALLY on the offline
        # designer's model, which is wrong by the SAME frozen M-par family
        # as PAT's twin; the trained values are then deployed through
        # actuation maps carrying the same family errors; phase B (the
        # budgeted loop below) is on-device HEAD recalibration only.
        lv = scaled_mpar(mismatch_scale)     # PR-5 §E: 1.0 == frozen headline
        off = DissipativeRingSubstrate.from_cell(
            cell_label, N=sub.N, clock_GSps=2.0, seed=run_seed,
            input_taps=taps_for_N(sub.N),
            loss_scale=1.0 + lv["kappa_i_rel"],
            gain_factor=sub.gain_factor
            * (1.0 + lv["gain_factor_rel"]),
            ase_variance_scale=0.0)
        with torch.no_grad():
            off.gamma.mul_(1.0 + lv["gamma_rel"])
            off.gain_model = off.gain_model._replace(
                P_sat_W=off.gain_model.P_sat_W
                * (1.0 + lv["p_sat_rel"]))
            off.delta.copy_(sub.delta)
            off.kappa_ext.copy_(sub.kappa_ext)
            off.mu_chain.copy_(sub.mu_chain)
        off_in_situ = [off.delta, off.kappa_ext, off.mu_chain]
        opt_off = torch.optim.Adam(off_in_situ, lr=lr_phys_frac * ki)
        opt_head_off = torch.optim.Adam(head.parameters(), lr=lr_head)
        with torch.no_grad():
            y0o = off.forward_intensity(encode_drive(u0).unsqueeze(-1))
            ys_off = float(y0o.mean()) + 1e-30
        for it in range(1, n_updates + 1):
            u_raw, target = fresh_batch(run_seed, it)
            y = off.forward_intensity(encode_drive(u_raw).unsqueeze(-1))
            loss = mse_loss(head(y / ys_off), target)
            opt_head_off.zero_grad()
            for p in off_in_situ:
                p.grad = None
            loss.backward()
            torch.nn.utils.clip_grad_norm_(
                off_in_situ + list(head.parameters()), 1.0)
            opt_off.step()
            opt_head_off.step()
            off.clamp_to_bounds()
            led["digital_passes"] += 2 * BATCH        # all-digital phase A
        # Deploy: commands realized through M-par actuation maps.
        with torch.no_grad():
            sub.delta.copy_(off.delta
                            + lv["delta_offset_ki"] * ki)
            sub.kappa_ext.copy_(off.kappa_ext
                                * lv["kext_actuation"])
            sub.mu_chain.copy_(off.mu_chain
                               * lv["mu_actuation"])
            sub.clamp_to_bounds()
            y0d = sub.forward_intensity(encode_drive(u0).unsqueeze(-1),
                                        generator=ase_gen(run_seed, 0, 14))
            y_scale = float(y0d.mean()) + 1e-30       # re-measured on device
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
        elif method == "adjoint":
            def adj_loss(y_adj):
                return mse_loss(head(y_adj / y_scale), target)
            opt_head.zero_grad()
            for p in in_situ:
                p.grad = None
            # Distinct ASE tags: 6 = pass 1 (fwd), 7 = pass 2 (adjoint) —
            # fresh, never shared (PR-11 irreversibility invariant).
            loss_val, _ = est.step(u, adj_loss,
                                   gen_fwd=ase_gen(run_seed, it, 6),
                                   gen_adj=ase_gen(run_seed, it, 7))
            torch.nn.utils.clip_grad_norm_(
                in_situ + list(head.parameters()), 1.0)
            opt_phys.step()
            opt_head.step()
        elif method in ("rhel", "rhel-ideal"):
            for p in in_situ:
                p.grad = None
            # ASE tags 8/9 = the two forwards, 10/11 = the two echoes,
            # 12/13 = the two conjugation events — all fresh, never shared
            # (PR-11 invariant 1; C_op fires once per echo pass).
            y = est.step(u, target, head, y_scale,
                         gen_f1=ase_gen(run_seed, it, 8),
                         gen_e1=ase_gen(run_seed, it, 10),
                         gen_f2=ase_gen(run_seed, it, 9),
                         gen_e2=ase_gen(run_seed, it, 11),
                         gen_c1=ase_gen(run_seed, it, 12),
                         gen_c2=ase_gen(run_seed, it, 13))
            torch.nn.utils.clip_grad_norm_(in_situ, 1.0)
            opt_phys.step()
            # Digital head step on the measured forward y (identical
            # cadence; head grads only — y is detached).
            pred = head(y / y_scale)
            loss_h = mse_loss(pred, target)
            opt_head.zero_grad()
            loss_h.backward()
            opt_head.step()
            loss_val = float(loss_h.detach())
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
        else:                    # head-only / offline-deploy phase B
            tag = 15 if method == "offline-deploy" else 4
            with torch.no_grad():
                y = sub.forward_intensity(u,
                                          generator=ase_gen(run_seed, it, tag))
            led["device_passes"] += BATCH
            pred = head(y.detach() / y_scale)
            loss = mse_loss(pred, target)
            opt_head.zero_grad()
            loss.backward()
            opt_head.step()
            loss_val = float(loss.detach())

        if method_base in ("bptt", "pat", "adjoint", "rhel"):
            sub.clamp_to_bounds()
        elif method == "spsa":
            sub.clamp_to_bounds()
        led["loss_trace"].append(loss_val)

        if eval_every is not None and it % eval_every == 0:
            if method_base in ("pat", "adjoint", "rhel"):
                passes_now = est.n_device_passes
            elif method == "spsa":
                passes_now = adaptor.n_forward_equivalents * BATCH
            elif method in ("head-only", "offline-deploy"):
                passes_now = it * BATCH
            else:                                    # bptt reference
                passes_now = 0
            led["eval_trace"].append(
                (it, passes_now, eval_ser(sub, head, y_scale)))

    # Ledger totals (PR-7).
    if method_base in ("pat", "adjoint", "rhel"):
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
    if return_state:
        led["y_scale"] = y_scale       # the head's trained normalization —
        return led, sub, head          # REQUIRED for any post-hoc eval (S0.10
    led["y_scale"] = y_scale           # erratum: re-measuring it breaks arms
    return led                         # that move kappa_ext)
