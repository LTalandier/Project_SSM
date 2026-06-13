# NEW (task S0.3-1, deliverable 7) — M2 one-off validation of the M1
# quasi-static reduction. Runs the SALVAGED rate-equation integrator
# (photonic_ssm.dynamic_gain.DynamicSOA) with the Er lifetime τ = 3.4 ms once
# at C-2/θ₀ and once at C-1/θ₀ (P4-F9), confirming the per-episode relaxation
# ≤ 3 % bound (R§4b). M2 is NOT a substrate-matrix member — this is its only
# use; it is never wired into the estimator path.
"""M2 validation: does the full Er rate equation stay quasi-static (M1)?

PR-4 v2 §G registers M1 (static saturated operating point within an episode)
as the Er:Si₃N₄-native gain class and keeps M2 (the full rate equation at the
measured PL lifetime τ = 3.4 ms) strictly as M1's **one-off validation
reference**. This script is that reference: it integrates the salvaged
rate-equation gain over a registered-drive 4-PAM episode at C-2/θ₀ and
C-1/θ₀ and confirms the within-episode gain excursion is ≤ 3 % — i.e. M1's
static reduction loses ≤ 3 % (R§4b), justifying the static operating point.

Quasi-static physics (R§4b): the saturated carrier-recovery time is
τ_eff = τ_c/(1 + P̄/P_sat) ≈ 104 µs at the bus plane (P̄₀ = 1 mW, P_sat =
−15 dBm), still ≫ the symbol period and the registered episode lengths, so
the gain tracks only the long-term average and the per-symbol ripple is
negligible (E_sym/E_sat ≈ 5e-6). M2 confirms this numerically.

Output: results/s0_3/m2_validation.json + a short note. Run:
    python3 analysis/s0_3_1_m2_validation.py
"""

import json
import math
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from photonic_ssm.dynamic_gain import DynamicSOA
from photonic_ssm.substrate import cells as C
from photonic_ssm.substrate.gain import P_SAT_WG_W
from photonic_ssm.substrate.normalization import P_BAR0_W

TAU_ER = 3.4e-3          # measured Er:Si₃N₄ PL lifetime [s] [EV]
G0_DB = 30.0             # flagship small-signal gain [EV, R§4b]
P_SAT_MW = P_SAT_WG_W * 1e3   # −15 dBm = 0.0316 mW (bus plane, R§4b)
CLOCK_GSPS = 2.0
EPISODE_SYMS = 4000      # 2 µs episode at 2 GS/s (registered-scale)
RELAX_BOUND = 0.03       # the registered ≤3 % quasi-static bound


def make_4pam_episode(n: int, seed: int) -> torch.Tensor:
    """A registered-drive 4-PAM episode: power levels {0,⅓,⅔,1}·P_pk,
    P_pk = 2·P̄₀, equiprobable mean = P̄₀ = 1 mW. Returns z [n,1] with
    |z|² = power [W]."""
    g = torch.Generator().manual_seed(seed)
    syms = torch.randint(0, 4, (n,), generator=g)
    P_pk_W = 2.0 * P_BAR0_W
    power_W = (syms.to(torch.float64) / 3.0) * P_pk_W
    return torch.sqrt(power_W).reshape(n, 1).to(torch.complex128)


def run_cell(label: str) -> dict:
    cell = C.get_cell(label)
    dt = 1.0 / (CLOCK_GSPS * 1e9)
    soa = DynamicSOA(tau_c=TAU_ER, G0_dB=G0_DB, P_sat_mW=P_SAT_MW,
                     substeps_per_symbol=4)

    z = make_4pam_episode(EPISODE_SYMS, seed=hash(label) % 9999)
    # Track the log-gain h(t) over the episode by instrumenting apply: we
    # re-run the integration here to record h per symbol (the salvaged apply
    # returns only the amplified field, so we mirror its Euler loop for the
    # diagnostic — same equation, same steps).
    P_sat_W = soa.P_sat_W
    E_sat = soa.E_sat
    h0 = soa.h0
    substeps = max(soa.substeps_request, int(math.ceil(10.0 * dt / TAU_ER)))
    dt_sub = dt / substeps

    P = (z.real ** 2 + z.imag ** 2).reshape(-1)         # [n] W
    P_mean = float(P.mean())
    # Initialize at the average-power steady state (the M1 operating point).
    h = torch.tensor(math.log(soa.steady_state_power_gain(P_mean)),
                     dtype=torch.float64)
    h_trace = torch.empty(EPISODE_SYMS, dtype=torch.float64)
    for k in range(EPISODE_SYMS):
        Pk = P[k]
        for _ in range(substeps):
            dh = (h0 - h) / TAU_ER - (torch.exp(h) - 1.0) * Pk / E_sat
            h = h + dt_sub * dh
        h_trace[k] = h

    field_gain = torch.exp(h_trace / 2.0)               # amplitude gain
    g_mean = float(field_gain.mean())
    ripple = float((field_gain.max() - field_gain.min()) / field_gain.mean())
    # Drift of the running mean (slow component): compare first-tenth vs
    # last-tenth episode-mean field gain.
    tenth = EPISODE_SYMS // 10
    drift = float(abs(field_gain[:tenth].mean() - field_gain[-tenth:].mean())
                  / field_gain.mean())
    tau_eff = TAU_ER / (1.0 + P_mean / P_sat_W)
    E_sym = P_mean * dt
    return {
        "cell": label,
        "tau_c_s": TAU_ER,
        "clock_GSps": CLOCK_GSPS,
        "episode_syms": EPISODE_SYMS,
        "episode_duration_s": EPISODE_SYMS * dt,
        "P_mean_W": P_mean,
        "P_sat_W": P_sat_W,
        "tau_eff_s": tau_eff,
        "E_sym_over_E_sat": E_sym / E_sat,
        "mean_field_gain": g_mean,
        "within_episode_ripple": ripple,
        "running_mean_drift": drift,
        "relax_bound": RELAX_BOUND,
        "quasi_static_pass": bool(ripple <= RELAX_BOUND and drift <= RELAX_BOUND),
    }


def main():
    rows = [run_cell("C-2"), run_cell("C-1")]
    out_dir = "results/s0_3"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "m2_validation.json"), "w") as fh:
        json.dump(rows, fh, indent=2)
    print("M2 quasi-static validation (τ = 3.4 ms; ≤3% bound, R§4b):")
    for r in rows:
        print(f"  {r['cell']}/θ₀: ripple={r['within_episode_ripple']:.2e}  "
              f"drift={r['running_mean_drift']:.2e}  τ_eff={r['tau_eff_s']*1e6:.1f}µs  "
              f"E_sym/E_sat={r['E_sym_over_E_sat']:.2e}  "
              f"PASS={r['quasi_static_pass']}")
    print(f"wrote {out_dir}/m2_validation.json")


if __name__ == "__main__":
    main()
