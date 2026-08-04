# NEW (PR-18, 2026-08-04, registered pre-run at b585623) — one (set, seed)
# unit of the converged-operating-point diagnostics: deterministic
# state-capture reproduction of a stored converged run, bit-identity
# fingerprint (PR-18 §18.2), then the S0.4-0 §B measurements verbatim on the
# converged device (PR-18 §18.3). Writes results/s0_11/runs/<set>_<seed>.json.
"""usage: s0_11_run_one.py SET SEED   (SET ∈ {pinned2, boxed3, patC2, spsaC2})"""

from __future__ import annotations

import json
import math
import os
import sys
import time

import torch

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from photonic_ssm.estimators.harness import train          # noqa: E402
from photonic_ssm.substrate import cells as cellmod        # noqa: E402
from photonic_ssm.substrate import normalization as O2     # noqa: E402
import s0_4_0_calibration as cal                           # noqa: E402

ROBUST_SEEDS = (7, 19, 41, 101, 271)   # S0.4-0 recorded protocol
GATE_RATIO = cal.GATE_RATIO            # 1e-3, PR-6 §B frozen


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


SPECS = {
    "pinned2": dict(
        stored="results/s0_6/runs/pinned_2.0_{seed}.json",
        kw=dict(method="bptt", cell_label="C-2", n_updates=12000,
                eval_every=100, r0=2.0, pin_kext=True)),
    "boxed3": dict(
        stored="results/s0_6/runs/boxed_3.0_{seed}.json",
        kw=dict(method="bptt", cell_label="C-2", n_updates=12000,
                eval_every=100,
                r0=math.sqrt(cellmod.R_MIN_SATURATING * 3.0), r_hi=3.0)),
    "patC2": dict(
        stored="results/s0_5/runs/pat-both_C-2_{seed}.json",
        kw=dict(method="pat-both", cell_label="C-2", n_updates=31600,
                eval_every=100)),
    "spsaC2": dict(
        stored="results/s0_5/runs/spsa_C-2_{seed}.json",
        kw=dict(method="spsa", cell_label="C-2", n_updates=15800,
                eval_every=100)),
}


def fingerprint(led, stored, is_s06: bool):
    """PR-18 §18.2: bit-identity vs the stored run JSON."""
    got_trace = [list(t) for t in led["eval_trace"]]
    ref_trace = stored["eval_trace"]
    got_final = median([s for _, _, s in led["eval_trace"][-3:]])
    det = {"trace_len_ok": len(got_trace) == len(ref_trace),
           "trace_exact": got_trace == ref_trace,
           "final_ser_exact": got_final == stored["final_ser"],
           "final_ser_reproduced": got_final,
           "final_ser_stored": stored["final_ser"]}
    if not det["trace_exact"] and det["trace_len_ok"]:
        diffs = [abs(a[2] - b[2]) for a, b in zip(got_trace, ref_trace)]
        det["first_diff_idx"] = next(
            (i for i, (a, b) in enumerate(zip(got_trace, ref_trace))
             if a != b), None)
        det["max_abs_ser_diff"] = max(diffs)
    if is_s06:
        det["final_r_exact"] = (led["in_situ_r"] == stored["final_r"])
    verdict = "bit" if all(det.get(k, True) for k in
                           ("trace_exact", "final_ser_exact",
                            "final_r_exact")) else "protocol"
    return verdict, det


def main():
    set_name, seed = sys.argv[1], int(sys.argv[2])
    spec = SPECS[set_name]
    stored_path = spec["stored"].format(seed=seed)
    with open(stored_path) as fh:
        stored = json.load(fh)
    if "n_updates" in stored:
        assert stored["n_updates"] == spec["kw"]["n_updates"], \
            (stored["n_updates"], spec["kw"]["n_updates"])

    t0 = time.time()
    led, sub, head = train(run_seed=seed, return_state=True, **spec["kw"])
    verdict, det = fingerprint(led, stored, is_s06=set_name in
                               ("pinned2", "boxed3"))

    # ---- measurements on the converged device (PR-18 §18.3) ---------- #
    sub.ase_variance_scale = 0.0       # registered noiseless calibration mode
    ki = float(sub.kappa_i)

    per_ring_min = {}
    for kind in ("mse_zero", "mse_target"):
        pm = None
        for s in ROBUST_SEEDS:
            g = cal.per_ring_gradient(sub, loss_kind=kind, seed=s)
            r = g / g.max().clamp_min(1e-300)
            pm = r if pm is None else torch.minimum(pm, r)
        per_ring_min[kind] = pm
    gate = {
        "count_ge_gate_mse_zero":
            int((per_ring_min["mse_zero"] >= GATE_RATIO).sum()),
        "worst_ratio_mse_zero": float(per_ring_min["mse_zero"].min()),
        "count_ge_gate_mse_target":
            int((per_ring_min["mse_target"] >= GATE_RATIO).sum()),
        "worst_ratio_mse_target": float(per_ring_min["mse_target"].min()),
        "per_ring_min_mse_zero":
            [float(f"{x:.4g}") for x in per_ring_min["mse_zero"]],
    }
    part = cal.participation_profile(sub)

    with torch.no_grad():
        kext = sub.kappa_ext.detach().clone()
        delta = sub.delta.detach().clone()
        mu = sub.mu_chain.detach().clone()
        knet_op = sub.kappa_net().detach().clone()

        # (iv) vii endpoint row — S0.4-0 Item-3 Lorentzian convention,
        # the substrate's own gain model (g0, P_sat), passive κ_tot build-up.
        gm = sub.gain_model
        FSR = sub.FSR_Hz
        ktot_pass = ki + 2.0 * kext
        bu_ach = 2.0 * kext * FSR / (ktot_pass ** 2 + delta ** 2)
        g_ach = gm.g0 / (1.0 + bu_ach * O2.P_BAR0_W / gm.P_sat_W)
        knet_aw_ach = (ki - g_ach + 2.0 * kext) / ki
        bu_band = 2.0 * kext * FSR / (ktot_pass ** 2 + ki ** 2)
        g_band = gm.g0 / (1.0 + bu_band * O2.P_BAR0_W / gm.P_sat_W)
        knet_aw_band = (ki - g_band + 2.0 * kext) / ki

    r_j = (kext / ki).tolist()
    row = {
        "set": set_name, "seed": seed, "stored": stored_path,
        "registered": "PR-18 (b585623)",
        "fingerprint": verdict, "fingerprint_detail": det,
        "gate_at_solution": gate,
        "participation_at_solution": {k: part[k] for k in
                                      ("count_ge_1e-1", "count_ge_1e-2",
                                       "count_ge_1e-3")},
        "params": {
            "r_j": [round(x, 6) for x in r_j],
            "delta_over_ki": [round(x, 6) for x in (delta / ki).tolist()],
            "mu_over_ki": [round(x, 6) for x in (mu / ki).tolist()],
            "knet_op_over_ki": [round(x, 6) for x in (knet_op / ki).tolist()],
            "mu_median_over_ki": median((mu / ki).tolist()),
            "r_sd": float(torch.std(kext / ki, correction=0)),
        },
        "vii_endpoint": {
            "knet_aware_achieved_over_ki":
                [round(float(x), 6) for x in knet_aw_ach],
            "min_achieved": float(knet_aw_ach.min()),
            "argmin_ring_1based": int(knet_aw_ach.argmin()) + 1,
            "min_band": float(knet_aw_band.min()),
        },
        "wall_s": round(time.time() - t0, 1),
    }
    os.makedirs("results/s0_11/runs", exist_ok=True)
    out = f"results/s0_11/runs/{set_name}_{seed}.json"
    with open(out, "w") as fh:
        json.dump(row, fh)
    print(f"done {set_name}_{seed}: fp={verdict} "
          f"gate {gate['count_ge_gate_mse_zero']}/32 "
          f"worst {gate['worst_ratio_mse_zero']:.2e} "
          f"mu_med {row['params']['mu_median_over_ki']:.3f} "
          f"vii_min {row['vii_endpoint']['min_achieved']:.3f} "
          f"[{row['wall_s']}s]")


if __name__ == "__main__":
    main()
