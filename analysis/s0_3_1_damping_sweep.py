# NEW (task S0.3-1, deliverable 9) — the coarse BPTT-on-substrate damping
# sweep (F3 → PR-12). Trains the BPTT reference through the frozen substrate
# across a coarse D-LinOSS damping grid (the loss–gain operating point, which
# sets the net damping floor κ_net) at C-1/N=8 and C-2/N=32, θ₀, NF-A, on the
# T-A task, ≥4 seeds/point. Outputs the damping→accuracy curve that selects
# PR-12's central operating cell. The PR-12 FREEZE itself is a Supervisor+Lucas
# step — this reports the curve and stops.
"""Coarse BPTT-on-substrate damping sweep (F3 → PR-12).

D-LinOSS damping is the net loss–gain operating point: κ_net = (1−g_f)·κᵢ +
2κ_ext, so the per-cell damping floor is set by the gain compensation
fraction g_f. This sweep varies g_f over a coarse grid (g_f=0.9 is the
registered operating point; lower g_f ⇒ more damping ⇒ shorter memory),
trains the BPTT-on-substrate reference (in-situ {δ, κ_ext, μ} + a digital
readout/head) on the frozen T-A task at each point, and records test SER. The
resulting damping→accuracy curve selects PR-12's central cell.

Output: results/s0_3/damping_sweep.jsonl, rows
  {cell, N, damping(g_f), seed, clock_GSps, bptt_test_acc, bptt_train_acc,
   ase_var, n_passes, runtime_s, anomaly}.

Run:
  python3 analysis/s0_3_1_damping_sweep.py --smoke      # 1 fast config + timing
  python3 analysis/s0_3_1_damping_sweep.py              # full sweep (see --help)
"""

import argparse
import json
import os
import sys
import time

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from photonic_ssm.runner.sweep import load_existing, save_records, job_key
from photonic_ssm.substrate import DissipativeRingSubstrate as DRS, get_cell
from photonic_ssm.substrate.normalization import P_BAR0_W, H_NU_J
from photonic_ssm.tasks.equalization import make_ta_dataset, symbol_error_rate

DAMPING_GRID = (0.0, 0.3, 0.5, 0.7, 0.9)   # gain fraction g_f (0.9 = registered)
TAP_WINDOW = 8                              # {y(n−m), m=0..7} (PR-2)
MOD_DEPTH = 0.6                             # intensity-encoder modulation depth
KEY_FIELDS = ("cell", "N", "damping", "seed", "clock_GSps")


# ---------------------------------------------------------------------- #
#  The BPTT-on-substrate reference model
# ---------------------------------------------------------------------- #
class BPTTReference(torch.nn.Module):
    """Encoder (O2-frozen intensity map) → substrate (in-situ {δ,κ_ext,μ}) →
    R2 intensity readout y=|Σ c_j a_j|² (c digital) → linear head over the
    8-tap window → d̂(n−2). The in-situ + digital params train jointly by BPTT
    (the reference ceiling)."""

    def __init__(self, cell, N, clock_GSps, gain_factor, seed, mu_init_frac=0.3):
        super().__init__()
        self.sub = DRS(cell, N=N, clock_GSps=clock_GSps,
                       gain_factor=gain_factor, ase_variance_scale=1.0,
                       seed=seed)
        # Training init: a small nonzero nearest-neighbor chain coupling so the
        # ring-1-driven chain propagates the signal to all rings at step 0
        # (PR-2's μ(0)=0 leaves N−1 rings dark → untrainable at N=32). Init is
        # PR-6's to freeze and the roadmap (S0.6) sweeps damping init/range —
        # this is the S0.3-1 sweep's working init, not a substrate default.
        with torch.no_grad():
            ki = float(self.sub.kappa_i)
            self.sub.mu_chain.copy_(mu_init_frac * ki * torch.ones_like(self.sub.mu_chain))
        # digital-trained readout residues c_j (complex via re/im) + head
        g = torch.Generator().manual_seed(seed + 101)
        self.c = torch.nn.Parameter(0.5 * torch.randn(N, 2, dtype=torch.float64,
                                                      generator=g))
        self.head = torch.nn.Linear(TAP_WINDOW, 1).to(torch.float64)
        self.amp = (P_BAR0_W / H_NU_J) ** 0.5     # √(P̄₀/ħω₀)

    def encode(self, u):
        """Intensity encoder: power = P̄₀·(1 + m·ũ), ũ zero-mean unit-var;
        amplitude = √(power/ħω₀). O2-frozen scale (mean power = P̄₀)."""
        u = u.to(torch.float64)
        un = (u - u.mean()) / (u.std() + 1e-12)
        power_frac = torch.clamp(1.0 + MOD_DEPTH * un, min=0.0)   # ×P̄₀
        return (self.amp * power_frac.sqrt()).to(self.sub._dtype)

    def encode_batch(self, u):
        """Batched intensity encoder. u: (B,T) → drive amplitude (B,T,1)."""
        u = u.to(torch.float64)
        un = (u - u.mean(dim=1, keepdim=True)) / (u.std(dim=1, keepdim=True) + 1e-12)
        power_frac = torch.clamp(1.0 + MOD_DEPTH * un, min=0.0)
        return (self.amp * power_frac.sqrt()).to(self.sub._dtype).unsqueeze(-1)

    def forward(self, u, generator=None):
        """u: (T,) single or (B,T) batched. Returns d̂(n−2), matching shape."""
        single = (u.ndim == 1)
        if single:
            u = u.unsqueeze(0)
        s = self.encode_batch(u)                          # (B,T,1)
        states, _ = self.sub(s, generator=generator)      # (B,T+1,2N)
        a_cw = self.sub.cw_states(states)[:, 1:, :]        # (B,T,N) complex
        c = torch.complex(self.c[:, 0], self.c[:, 1])
        z = a_cw @ c                                       # (B,T) complex
        y = (z.abs() ** 2).to(torch.float64)               # R2 intensity
        B, T = y.shape
        taps = torch.zeros(B, T, TAP_WINDOW, dtype=torch.float64)
        for m in range(TAP_WINDOW):
            if m == 0:
                taps[:, :, 0] = y
            else:
                taps[:, m:, m] = y[:, :T - m]
        taps = taps / (taps.std() + 1e-9)
        out = self.head(taps).squeeze(-1)                  # (B,T)
        return out.squeeze(0) if single else out


def _batch_dataset(batch, seq_len, snr_dB, base_seed):
    """Stack `batch` fresh T-A sequences → (u (B,T), target (B,T))."""
    us, ts = [], []
    for b in range(batch):
        u, tgt, _ = make_ta_dataset(seq_len, snr_dB, seed=base_seed * 31 + b)
        us.append(u); ts.append(tgt)
    return torch.stack(us), torch.stack(ts)


def train_one(cell_label, N, gain_factor, seed, clock_GSps=2.0, snr_dB=28.0,
              n_steps=400, seq_len=512, lr=8e-3, batch=8, eval_len=5000,
              verbose=False):
    """Train the BPTT reference at one damping point; return the result row.
    Batched BPTT (smoother gradients) + grad clip + cosine LR decay."""
    torch.manual_seed(seed)
    cell = get_cell(cell_label)
    model = BPTTReference(cell, N, clock_GSps, gain_factor, seed)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, n_steps, eta_min=lr * 0.1)
    gen = torch.Generator().manual_seed(seed + 7)         # ASE stream
    t0 = time.time()
    last = float("nan")
    for step in range(n_steps):
        u, target = _batch_dataset(batch, seq_len, snr_dB, seed * 1000 + step)
        pred = model(u, generator=gen)
        loss = ((pred - target) ** 2)[:, 16:].mean()      # skip ISI transient
        opt.zero_grad(); loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
        opt.step(); sched.step()
        model.sub.clamp_to_bounds()                       # K4 box constraint
        last = float(loss.detach())
        if verbose and step % 50 == 0:
            print(f"    step {step:3d}  mse={last:.4f}")
    runtime = time.time() - t0

    # Train SER (a fresh train-distribution sequence) + held-out test SER.
    with torch.no_grad():
        u_tr, tg_tr, _ = make_ta_dataset(eval_len, snr_dB, seed=seed * 13 + 1)
        ser_tr = symbol_error_rate(model(u_tr, generator=gen), tg_tr)
        u_te, tg_te, _ = make_ta_dataset(eval_len, snr_dB, seed=seed * 99991 + 5)
        ser_te = symbol_error_rate(model(u_te, generator=gen), tg_te)
    anomaly = None
    if not (last == last):                                # NaN guard
        anomaly = "nan_loss"
    return {
        "cell": cell_label, "N": N, "damping": gain_factor, "seed": seed,
        "clock_GSps": clock_GSps, "snr_dB": snr_dB,
        "bptt_test_acc": 1.0 - ser_te, "bptt_train_acc": 1.0 - ser_tr,
        "test_ser": ser_te, "train_ser": ser_tr,
        "ase_var": 1.0, "n_passes": n_steps, "batch": batch,
        "n_seq_passes": n_steps * batch, "seq_len": seq_len, "lr": lr,
        "final_mse": last, "runtime_s": round(runtime, 2), "anomaly": anomaly,
    }


# ---------------------------------------------------------------------- #
#  Sweep driver (resume-safe)
# ---------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="S0.3-1 coarse BPTT damping sweep")
    ap.add_argument("--smoke", action="store_true",
                    help="one fast config (C-1, g_f=0.9, 1 seed) + timing")
    ap.add_argument("--cells", nargs="+", default=["C-1", "C-2"])
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--steps", type=int, default=500)
    ap.add_argument("--seq-len", type=int, default=384)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--out", default="results/s0_3/damping_sweep.jsonl")
    args = ap.parse_args()

    if args.smoke:
        t0 = time.time()
        row = train_one("C-1", 8, 0.9, seed=0, n_steps=30, seq_len=256,
                        verbose=True)
        print(json.dumps(row, indent=2))
        print(f"smoke wall: {time.time()-t0:.1f}s for 30 steps "
              f"→ full-run estimate ~{(time.time()-t0)/30*args.steps:.0f}s/config")
        return

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    existing = load_existing(args.out)
    done = {job_key(r, KEY_FIELDS) for r in existing}
    cell_N = {"C-1": 8, "C-2": 32, "C-3": 128}
    rows = list(existing)
    total = len(args.cells) * len(DAMPING_GRID) * args.seeds
    i = 0
    for cl in args.cells:
        N = cell_N[cl]
        for g_f in DAMPING_GRID:
            for seed in range(args.seeds):
                i += 1
                key = (cl, N, g_f, seed, 2.0)
                if key in done:
                    print(f"[{i}/{total}] skip (done) {key}")
                    continue
                print(f"[{i}/{total}] train {cl} N={N} damping(g_f)={g_f} seed={seed}")
                row = train_one(cl, N, g_f, seed, n_steps=args.steps,
                                seq_len=args.seq_len, batch=args.batch)
                rows.append(row)
                save_records(args.out, rows)
                print(f"    test_acc={row['bptt_test_acc']:.3f} "
                      f"train_acc={row['bptt_train_acc']:.3f} "
                      f"({row['runtime_s']}s)")
    print(f"wrote {args.out} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
