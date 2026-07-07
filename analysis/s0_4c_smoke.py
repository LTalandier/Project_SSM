# NEW (task S0.4c, 2026-07-07) — the pre-registered S0.4c smoke
# (task_queue.md S0.4c spec, committed 5ca8d52 BEFORE this run):
# R1 (full dissipation-sequence floor check), R3a (idealized-echo
# trainability, gated), R3b (honest-echo smoke, report-only — selects the
# F22 template the data currently favors), PR-11 noise-floor records
# (quantum + pump-RIN vs the state scale), + the ungated C-2 spot.
"""S0.4c smoke. Writes results/s0_4c/smoke.{json,md}."""

from __future__ import annotations

import json
import math
import os
import sys
import time

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from photonic_ssm.estimators.harness import (          # noqa: E402
    TapHead, encode_drive, make_substrate, train,
)
from photonic_ssm.estimators.rhel import (             # noqa: E402
    RHELEstimator, conjugation_efficiency,
)
from photonic_ssm.substrate.dissipative_ring import (  # noqa: E402
    DissipativeRingSubstrate as DRS,
)

OUT = "results/s0_4c"
SEEDS = (11, 23, 47)
N_UPDATES = 300
REDUCTION = 0.20
T_PROBE, B_PROBE, N_PROBE = 32, 2, 8


def _sub(r, loss_scale):
    sub = DRS.from_cell("C-1", N=N_PROBE, clock_GSps=2.0, seed=3,
                        input_taps=(0, 3, 5, 7), gain_factor=0.0,
                        loss_scale=loss_scale, ase_variance_scale=0.0)
    ki = float(sub.kappa_i)
    with torch.no_grad():
        sub.delta.copy_(torch.linspace(-1, 1, N_PROBE,
                                       dtype=sub.delta.dtype) * ki)
        sub.kappa_ext.fill_(r * ki)
        sub.mu_chain.fill_(0.3 * ki)
    return sub


def r1_sequence():
    """Cosine(Δθ_RHEL, ∇θ truncated-BPTT) across decreasing dissipation."""
    g = torch.Generator().manual_seed(7)
    u = encode_drive(12.0 * torch.rand(B_PROBE, T_PROBE, generator=g,
                                       dtype=torch.float64) - 6.0
                     ).unsqueeze(-1)
    tgt = torch.randn(B_PROBE, T_PROBE, generator=g, dtype=torch.float64)
    rows = []
    for r, ls in ((0.1, 0.01), (0.03, 0.01), (0.01, 0.01), (0.003, 0.001)):
        torch.manual_seed(0)
        sub = _sub(r, ls)
        head = TapHead()
        with torch.no_grad():
            y_scale = float(sub.forward_intensity(u).mean()) + 1e-30
        # truncated-BPTT reference (m=0 differentiable, full-head residual)
        for p in (sub.delta, sub.kappa_ext, sub.mu_chain):
            p.grad = None
        y = sub.forward_intensity(u)
        cols = [y] + [torch.nn.functional.pad(y.detach(), (m, 0)
                                              )[..., : y.shape[-1]]
                      for m in range(1, 8)]
        lag = torch.stack(cols, -1)
        W = head.lin.weight.detach()[0]
        b = float(head.lin.bias.detach())
        (((lag / y_scale * W).sum(-1) + b - tgt) ** 2).mean().backward()
        g_ref = torch.cat([p.grad.reshape(-1).clone() for p in
                           (sub.delta, sub.kappa_ext, sub.mu_chain)])
        est = RHELEstimator(sub, ideal_echo=True, eps_frac=0.01)
        for p in (sub.delta, sub.kappa_ext, sub.mu_chain):
            p.grad = None
        est.step(u, tgt, head, y_scale)
        g_rhel = torch.cat([p.grad.reshape(-1).clone() for p in
                            (sub.delta, sub.kappa_ext, sub.mu_chain)])
        cos = float(torch.dot(g_rhel, g_ref) /
                    (g_rhel.norm() * g_ref.norm() + 1e-300))
        kn = float(sub.kappa_net().detach().mean())
        rows.append({"r": r, "loss_scale": ls,
                     "kappa_net_T_dt": kn * T_PROBE * sub.dt,
                     "cosine": cos})
        print(f"  r={r} ls={ls}: κ_net·T·dt={kn * T_PROBE * sub.dt:.3f} "
              f"cosine={cos:+.4f}")
    return rows


def noise_floor_record():
    """PR-11 records: frozen η_c chain + quantum/RIN noise vs state scale
    at the registered C-1/C-2 θ₀ (spec: 'expect negligible — measure')."""
    recs = {}
    for cell, n in (("C-1", 8), ("C-2", 32)):
        sub = make_substrate(cell, seed=3, N=n)
        eta = conjugation_efficiency(sub)
        # state photon scale at θ₀ from a short driven run
        g = torch.Generator().manual_seed(5)
        u = encode_drive(12.0 * torch.rand(1, 64, generator=g,
                                           dtype=torch.float64) - 6.0
                         ).unsqueeze(-1)
        with torch.no_grad():
            st, _ = sub.forward(u)
            state_ph = float(st[:, 1:, :].abs().pow(2).mean())
        q_noise_ph = float((1.0 + eta).mean())      # ⟨|n_conj|²⟩ photons
        recs[cell] = {
            "eta_c_mean": float(eta.mean()),
            "eta_c_dB": 10.0 * math.log10(float(eta.mean()) + 1e-300),
            "state_photons_mean_mode": state_ph,
            "conj_quantum_noise_photons": q_noise_ph,
            "quantum_over_state": q_noise_ph / (state_ph + 1e-300),
            "eta_scaled_state_over_quantum":
                float(eta.mean()) * state_ph / q_noise_ph,
        }
        print(f"  {cell}: η_c={recs[cell]['eta_c_dB']:.1f} dB · state "
              f"{state_ph:.2e} ph/mode · conj quantum noise "
              f"{q_noise_ph:.2f} ph → quantum/state = "
              f"{recs[cell]['quantum_over_state']:.2e}")
    return recs


def summarize(led):
    tr = led["loss_trace"]
    init = sum(tr[:5]) / 5.0
    final = sum(tr[-20:]) / 20.0
    return {"loss_init_mean5": init, "loss_final_mean20": final,
            "reduction_frac": 1.0 - final / init,
            "ser_final": led["ser_final"],
            "device_passes": led["device_passes"],
            "digital_passes": led["digital_passes"]}


def run_arm(method):
    rows = []
    for s in SEEDS:
        t0 = time.time()
        led = train(method, "C-1", run_seed=s, n_updates=N_UPDATES, N=8)
        row = summarize(led)
        row["seed"] = s
        row["wall_s"] = round(time.time() - t0, 1)
        rows.append(row)
        print(f"  {method} seed {s}: init {row['loss_init_mean5']:.4f} -> "
              f"final {row['loss_final_mean20']:.4f} "
              f"({row['reduction_frac']:+.1%}); SER {row['ser_final']:.3f}; "
              f"dev {row['device_passes']} [{row['wall_s']}s]")
    n_pass = sum(r["reduction_frac"] >= REDUCTION for r in rows)
    return rows, n_pass


def main():
    os.makedirs(OUT, exist_ok=True)
    out = {"spec": "task_queue.md S0.4c (pre-registered at 5ca8d52)"}

    print("[R1 — dissipation-sequence floor check (gate: ≥0.9 at the least-"
          "dissipative point + monotone improvement)]")
    out["R1_rows"] = r1_sequence()
    cosines = [r["cosine"] for r in out["R1_rows"]]
    out["R1_pass"] = bool(cosines[-1] >= 0.9
                          and all(cosines[i] <= cosines[i + 1] + 0.02
                                  for i in range(len(cosines) - 1)))
    print(f"  => R1: {'PASS' if out['R1_pass'] else 'FAIL'}")

    print("[PR-11 noise-floor records (report-only)]")
    out["noise_floors"] = noise_floor_record()

    print(f"[R3a — idealized-echo trainability ({N_UPDATES} updates, "
          f"seeds {SEEDS}; gate ≥2/3)]")
    rows, n_pass = run_arm("rhel-ideal")
    out["R3a_runs"] = rows
    out["R3a_pass"] = bool(n_pass >= 2)
    print(f"  => R3a: {n_pass}/3 seeds {'PASS' if n_pass >= 2 else 'FAIL'}")

    print("[R3b — honest-echo smoke (frozen PR-11 chain; report-only, "
          "selects the F22 template)]")
    rows_h, n_pass_h = run_arm("rhel")
    out["R3b_runs"] = rows_h
    out["R3b_seeds_passing"] = n_pass_h
    out["F22_template_favored"] = ("A (competitive-track)" if n_pass_h >= 2
                                   else "B (fails-under-honest-echo track)")
    print(f"  => R3b: {n_pass_h}/3 seeds train → smoke favors template "
          f"{out['F22_template_favored']}")

    print("[C-2/N=32 spot, 1 seed x 100 updates — ungated]")
    t0 = time.time()
    led = train("rhel", "C-2", run_seed=11, n_updates=100)
    row = summarize(led)
    row["wall_s"] = round(time.time() - t0, 1)
    out["c2_spot"] = row
    print(f"  rhel: init {row['loss_init_mean5']:.4f} -> final "
          f"{row['loss_final_mean20']:.4f} ({row['reduction_frac']:+.1%}) "
          f"[{row['wall_s']}s]")

    with open(os.path.join(OUT, "smoke.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("gates:", "R1", "PASS" if out["R1_pass"] else "FAIL",
          "| R3a", "PASS" if out["R3a_pass"] else "FAIL")
    print("wrote", os.path.join(OUT, "smoke.json"))


if __name__ == "__main__":
    main()
