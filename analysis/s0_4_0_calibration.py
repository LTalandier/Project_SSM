# NEW (task S0.4-0, single-session mode 2026-07-07) — the signed-packet
# calibration: PR-6 §B input-map controllability search + participation
# profile, §C clause-(a) r_min sweep + E_sym/E_sat build-up factors, §C/§G
# δ-de-saturation characterization (conformance check input), §G-addendum
# multi-tap E₀ re-derivation. Sets no rule: every criterion below (10⁻³ gate,
# K=4 cap, seed {1,9,17,25}, m_κ=0.05, Δr=0.02, δ-band [−κᵢ,κᵢ]) is quoted
# from the 🔒 SIGNED PR-6 v3 block; this script measures the deferred numbers.
"""S0.4-0 calibration (PR-6 v3 signed 2026-07-07).

Outputs results/s0_4_0/s0_4_0_calibration.{json,md} — the single S0.4-0
calibration addendum's evidence, consumed before any bake-off run.

Conventions (all registered):
  * Cell C-2 (headline, N=32), clock 2 GS/s, noiseless (deterministic
    calibration; ASE is exogenous and grad-detached anyway), splitting ON
    (cell default), gain `saturating` (PR-6 §A).
  * Connected init μ_c = 0.3·κᵢ (§B), on-resonance δ=0 (§B gate condition).
  * Task gradient = |∂L/∂δ_j| per ring on a T=200 registered-encoder 4-PAM
    drive, L = mean(y²) (the test-h convention, the Critic's primary);
    sensitivity row: MSE to a delayed-symbol target (loss-robustness).
  * Gate (§B): every ring ≥ 10⁻³ · ring-1's gradient, tap cap K=4; the
    ratio is ALSO reported vs the max ring (identical when ring 1 is the
    strongest; the stricter reading is recorded either way).
  * r_min (§C, clause (a) alone): smallest uniform r with saturating
    on-resonance κ_net ≥ m_κ·κᵢ (m_κ=0.05) + Δr=0.02.
"""

from __future__ import annotations

import json
import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from photonic_ssm.substrate.dissipative_ring import DissipativeRingSubstrate as DRS
from photonic_ssm.substrate import cells as cellmod
from photonic_ssm.substrate import gain as gainmod
from photonic_ssm.substrate import normalization as O2

OUT_DIR = "results/s0_4_0"
M_KAPPA = 0.05          # PR-6 §C frozen net-loss floor (fraction of κᵢ)
DELTA_R = 0.02          # PR-6 §C frozen safety margin
GATE_RATIO = 1e-3       # PR-6 §B frozen meaningful-ratio gate
K_CAP = 4               # PR-6 §B registered tap cap (candidate K=4)
MU_C_FRAC = 0.3         # PR-6 §B connected init μ_c = 0.3 κᵢ
T_GRAD = 200            # gradient probe length (the Critic's T-robust midpoint)
N_SETTLE = 6000         # settling steps for steady-state readings


def make_sub(label="C-2", taps=(0,), r_uniform=cellmod.R0_THETA0,
             mu_frac=MU_C_FRAC, N=None):
    """Registered calibration configuration: noiseless, on-resonance,
    connected chain, uniform κ_ext = r·κᵢ, taps per PR-6 §B."""
    sub = DRS.from_cell(label, N=N, clock_GSps=2.0, seed=1,
                        ase_variance_scale=0.0, input_taps=taps)
    ki = float(sub.kappa_i)
    with torch.no_grad():
        sub.delta.zero_()                          # on-resonance (§B gate)
        sub.mu_chain.fill_(mu_frac * ki)           # connected init (§B)
        sub.kappa_ext.fill_(r_uniform * ki)
    return sub


def four_pam_drive(T=T_GRAD, seed=7):
    """Registered T-A encoder drive: equiprobable 4-PAM, P_pk = 2·P̄₀."""
    g = torch.Generator().manual_seed(seed)
    symbols = torch.randint(0, 4, (T,), generator=g)
    P_pk = O2.P_pk_for_family("T-A")
    return O2.encode_amplitude(symbols, P_pk), symbols


def per_ring_gradient(sub, loss_kind="mse_zero", seed=7):
    """|∂L/∂δ_j| per ring under the registered drive (noiseless)."""
    u, symbols = four_pam_drive(seed=seed)
    y = sub.forward_intensity(u)
    if loss_kind == "mse_zero":
        loss = (y ** 2).mean()
    elif loss_kind == "mse_target":                # delayed-symbol target
        y_n = y / y.detach().mean().clamp_min(1e-300)
        tgt = torch.roll(symbols.to(torch.float64), 1) / 3.0
        loss = ((y_n - tgt) ** 2).mean()
    else:
        raise ValueError(loss_kind)
    sub.zero_grad()
    loss.backward()
    return sub.delta.grad.detach().abs().clone()


def participation_profile(sub):
    """Settled per-ring |a_j| (CW half) under a constant P̄₀ drive."""
    flux = (O2.P_BAR0_W / O2.H_NU_J) ** 0.5
    u = torch.full((N_SETTLE,), flux, dtype=torch.float64)
    with torch.no_grad():
        states, _ = sub(u)
    a_cw = sub.cw_states(states)[-1].abs()          # (N,)
    prof = (a_cw / a_cw.max()).tolist()
    return {
        "profile_rel": [round(p, 12) for p in prof],
        "count_ge_1e-1": int((a_cw / a_cw.max() >= 1e-1).sum()),
        "count_ge_1e-2": int((a_cw / a_cw.max() >= 1e-2).sum()),
        "count_ge_1e-3": int((a_cw / a_cw.max() >= 1e-3).sum()),
        "settled_total_energy_photons": float((a_cw ** 2).sum()),
    }


def eval_tap_set(taps, loss_kind="mse_zero"):
    """One §B candidate: gradient gate + participation profile."""
    sub = make_sub(taps=taps)
    g = per_ring_gradient(sub, loss_kind=loss_kind)
    ref_ring1 = float(g[0])
    ref_max = float(g.max())
    ratio_r1 = (g / max(ref_ring1, 1e-300)).tolist()
    ratio_max = (g / max(ref_max, 1e-300)).tolist()
    n_pass_r1 = int(sum(r >= GATE_RATIO for r in ratio_r1))
    n_pass_max = int(sum(r >= GATE_RATIO for r in ratio_max))
    worst = min(ratio_max)
    sub2 = make_sub(taps=taps)
    part = participation_profile(sub2)
    return {
        "taps_0based": list(taps),
        "taps_1based": [t + 1 for t in taps],
        "K": len(taps),
        "grad_ring1": ref_ring1,
        "grad_max": ref_max,
        "grad_ratio_vs_ring1": [float(f"{r:.6g}") for r in ratio_r1],
        "n_rings_ge_gate_vs_ring1": n_pass_r1,
        "n_rings_ge_gate_vs_max": n_pass_max,
        "worst_ring_ratio_vs_max": float(f"{worst:.6g}"),
        "gate_pass_all32_vs_ring1": bool(n_pass_r1 == sub.N),
        "gate_pass_all32_vs_max": bool(n_pass_max == sub.N),
        "participation": part,
    }


# ------------------------------------------------------------------ #
#  Item 2 — r_min sweep (clause (a) alone) + build-up factors
# ------------------------------------------------------------------ #

def kappa_net_over_ki(label, r):
    sub = make_sub(label, taps=(0,), r_uniform=r, N=1)
    return float((sub.kappa_net()[0] / sub.kappa_i).detach())


def find_crossing(label, level, lo=0.10, hi=0.60, iters=60):
    """Smallest r with κ_net/κᵢ ≥ level (κ_net monotone ↑ in r here)."""
    flo = kappa_net_over_ki(label, lo)
    if flo >= level:
        return lo
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if kappa_net_over_ki(label, mid) >= level:
            hi = mid
        else:
            lo = mid
    return hi


def self_consistent_gain(label, r, mix=0.5, iters=500, tol=1e-12):
    """The circulating-field-consistent M1 fixed point (analysis-only; the
    as-built substrate uses the passive-build-up estimate — this pins the
    ×37-vs-×91 question, it does NOT change the substrate). Solve
    g = g₀/(1+P_circ/P_sat), P_circ = 2κ_ext·FSR·P̄₀/κ_net², κ_net = κᵢ−g+2κ_ext."""
    cell = cellmod.get_cell(label)
    ki = cellmod.kappa_i_rad_s(cell)
    plat = cellmod.platform_of(cell)
    FSR = plat.FSR_GHz * 1e9
    kext = r * ki
    gm = gainmod.build_gain_model(ki, cellmod.R0_THETA0 * ki,
                                  cell.gain_factor, FSR)
    g = gm.rate_fixed
    for _ in range(iters):
        knet = ki - g + 2.0 * kext
        knet = max(knet, 1e-6 * ki)                 # guard during iteration
        P_circ = 2.0 * kext * FSR * O2.P_BAR0_W / knet ** 2
        g_new = gm.g0 / (1.0 + P_circ / gm.P_sat_W)
        if abs(g_new - g) < tol * ki:
            g = g_new
            break
        g = (1 - mix) * g + mix * g_new
    knet = ki - g + 2.0 * kext
    P_circ = 2.0 * kext * FSR * O2.P_BAR0_W / knet ** 2
    return {"g_over_ki": g / ki, "kappa_net_over_ki": knet / ki,
            "P_circ_W": P_circ}


def measured_settled_energy(label, r, taps=(0,)):
    """Settled total CW intracavity photon number at uniform r, connected
    init, constant P̄₀ drive — the as-built rollout's actual field."""
    sub = make_sub(label, taps=taps, r_uniform=r)
    return participation_profile(sub)["settled_total_energy_photons"]


# ------------------------------------------------------------------ #
#  Item 3 — δ-de-saturation characterization (conformance-check input)
# ------------------------------------------------------------------ #

def delta_desaturation_row(label, r, n_pts=41):
    """Hypothetical δ-aware (Lorentzian) build-up: P̄(δ) ∝ 1/(κ_tot²+δ²).
    Characterizes how far the on-resonance clamp is permissive when a ring
    is detuned (anchor-risk (vii) magnitude). Passive κ_tot in the build-up,
    matching the as-built estimator convention."""
    cell = cellmod.get_cell(label)
    ki = cellmod.kappa_i_rad_s(cell)
    plat = cellmod.platform_of(cell)
    FSR = plat.FSR_GHz * 1e9
    kext = r * ki
    gm = gainmod.build_gain_model(ki, cellmod.R0_THETA0 * ki,
                                  cell.gain_factor, FSR)
    ktot_pass = ki + 2.0 * kext
    rows = []
    for f in torch.linspace(-1.0, 1.0, n_pts):
        delta = float(f) * ki
        buildup = 2.0 * kext * FSR / (ktot_pass ** 2 + delta ** 2)
        P = buildup * O2.P_BAR0_W
        g = gm.g0 / (1.0 + P / gm.P_sat_W)
        rows.append({"delta_over_ki": float(f),
                     "kappa_net_over_ki": (ki - g + 2 * kext) / ki})
    worst = min(rr["kappa_net_over_ki"] for rr in rows)
    onres = min(rows, key=lambda rr: abs(rr["delta_over_ki"])
                )["kappa_net_over_ki"]
    return {"r": r, "kappa_net_onres_over_ki": onres,
            "kappa_net_worst_over_ki": worst,
            "worst_at_delta_over_ki": 1.0, "sweep": rows}


def delta_aware_r_crossing(label, level, lo=0.10, hi=0.80, iters=60):
    """Smallest r with min_δ κ_net(r,δ)/κᵢ ≥ level over the [−κᵢ,κᵢ] band
    (the hypothetical δ-aware clause (a))."""
    def worst(r):
        return delta_desaturation_row(label, r, n_pts=21)["kappa_net_worst_over_ki"]
    if worst(lo) >= level:
        return lo
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if worst(mid) >= level:
            hi = mid
        else:
            lo = mid
    return hi


# ------------------------------------------------------------------ #
#  Item 4 — multi-tap E₀ (§G-addendum)
# ------------------------------------------------------------------ #

def multi_tap_E0(label, taps):
    """CW-equivalent single-pole E₀ reading (δ=0, μ=0, γ=0) with the drive
    split over `taps` — vs the frozen single-port closed form."""
    sub = DRS.from_cell(label, clock_GSps=2.0, seed=1,
                        ase_variance_scale=0.0, input_taps=taps)
    ki = float(sub.kappa_i)
    with torch.no_grad():
        sub.delta.zero_()
        sub.mu_chain.zero_()
        sub.gamma.zero_()
        sub.kappa_ext.fill_(cellmod.R0_THETA0 * ki)
        flux = (O2.P_BAR0_W / O2.H_NU_J) ** 0.5
        u = torch.full((N_SETTLE,), flux, dtype=torch.float64)
        states, _ = sub(u)
        E_meas = float(states[-1].abs().pow(2).sum())
    E_closed = O2.E0_photons(cellmod.R0_THETA0 * ki, ki,
                             gain_factor=sub.gain_factor)
    return {"taps_1based": [t + 1 for t in taps], "E0_measured": E_meas,
            "E0_closed_form_single_port": E_closed,
            "ratio": E_meas / E_closed}


# ------------------------------------------------------------------ #
#  Main
# ------------------------------------------------------------------ #

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    out = {"date": "2026-07-07", "task": "S0.4-0",
           "governing": "PR-6 v3 SIGNED 2026-07-07 (+PR-7/5/12); PR-4 v2 §N/§G",
           "conventions": {"cell": "C-2", "clock_GSps": 2.0, "noiseless": True,
                           "splitting": "cell default ON", "delta_init": 0.0,
                           "mu_c_frac_ki": MU_C_FRAC, "T_grad": T_GRAD,
                           "gate_ratio": GATE_RATIO, "K_cap": K_CAP,
                           "m_kappa": M_KAPPA, "Delta_r": DELTA_R}}

    # ---- Item 1: controllability search (registered trace) ----------- #
    print("[1] input-map controllability search (C-2, N=32)")
    trace = []
    candidates = [
        ("single-drive baseline (capacity-finding verification)", (0,)),
        ("REGISTERED SEED {1,9,17,25}", (0, 8, 16, 24)),
        ("fewer taps: K=2 centered {8,24}", (7, 23)),
        ("fewer taps: K=2 alt {9,25}", (8, 24)),
        ("fewer taps: K=2 alt {7,23}", (6, 22)),
        ("fewer taps: K=3 centered {6,17,27}", (5, 16, 26)),
        ("fewer taps: K=3 alt {5,16,27}", (4, 15, 26)),
        ("fewer taps: K=3 alt {6,16,26}", (5, 15, 25)),
        ("fewer taps: K=3 head-anchored {1,12,23}", (0, 11, 22)),
        ("fewer taps: K=3 tail-covered {3,16,29}", (2, 15, 28)),
        ("fewer taps: K=3 tail-covered {2,16,30}", (1, 15, 29)),
        ("fewer taps: K=3 tail-covered {4,17,30}", (3, 16, 29)),
        ("completed coverage at K=4: centered {4,12,20,28}", (3, 11, 19, 27)),
        ("completed coverage at K=4: head-anchored {1,10,19,28}", (0, 9, 18, 27)),
        ("completed coverage at K=4: shifted {5,13,21,29}", (4, 12, 20, 28)),
        ("completed coverage at K=4: tail-covered {4,13,22,30}", (3, 12, 21, 29)),
        ("completed coverage at K=4: tail-covered {3,12,21,30}", (2, 11, 20, 29)),
    ]
    for tag, taps in candidates:
        row = eval_tap_set(taps)
        row["trace_tag"] = tag
        trace.append(row)
        print(f"    {tag}: K={row['K']} — ≥gate vs ring1 "
              f"{row['n_rings_ge_gate_vs_ring1']}/32, vs max "
              f"{row['n_rings_ge_gate_vs_max']}/32, worst ratio "
              f"{row['worst_ring_ratio_vs_max']:.3g}")
    # loss-robustness row on the seed
    sub = make_sub(taps=(0, 8, 16, 24))
    g_alt = per_ring_gradient(sub, loss_kind="mse_target")
    ratio_alt = (g_alt / g_alt.max()).tolist()
    seed_row = next(r for r in trace if r["taps_0based"] == [0, 8, 16, 24])
    seed_row["loss_robustness_mse_target_n_ge_gate_vs_max"] = int(
        sum(r >= GATE_RATIO for r in ratio_alt))

    # Finalists: single-seed measurement is ambiguous at the gate boundary
    # (worst ratios hover ×0.1–×2 around 1e-3 and move ×20 with the drive
    # seed), so a ROBUSTNESS PROTOCOL is adopted before evaluating finalists
    # under it (recorded): per-ring ratio = min over 5 fixed drive seeds
    # {7,19,41,101,271}; the gate binds on that min. Finalists = the 6 best
    # candidates by single-seed worst margin (any K ≤ K_cap, vs-max reading).
    ROBUST_SEEDS = (7, 19, 41, 101, 271)
    finalists = sorted([r for r in trace if 1 < r["K"] <= K_CAP],
                       key=lambda r: -r["worst_ring_ratio_vs_max"])[:8]
    robustness = []
    for r in finalists:
        per_ring_min = None
        for s in ROBUST_SEEDS:
            subr = make_sub(taps=tuple(r["taps_0based"]))
            gr = per_ring_gradient(subr, seed=s)
            ratios = gr / gr.max()
            per_ring_min = (ratios if per_ring_min is None
                            else torch.minimum(per_ring_min, ratios))
        n_robust = int((per_ring_min >= GATE_RATIO).sum())
        row = {"taps_1based": r["taps_1based"], "K": r["K"],
               "robust_count_ge_gate": n_robust,
               "robust_worst_ratio": float(per_ring_min.min()),
               "robust_gate_pass_all32": bool(n_robust == 32),
               "per_ring_min_ratio": [float(f"{x:.4g}")
                                      for x in per_ring_min]}
        robustness.append(row)
        print(f"    robust {r['taps_1based']}: {n_robust}/32 ≥ gate "
              f"(min-over-{len(ROBUST_SEEDS)}-seeds), worst "
              f"{row['robust_worst_ratio']:.2e}")
    robust_clearing = [r for r in robustness if r["robust_gate_pass_all32"]]
    if robust_clearing:
        resolved = min(robust_clearing,
                       key=lambda r: (r["K"], -r["robust_worst_ratio"]))
        fallback = False
    else:
        # Fallback (c): resolved B = the set maximizing the robust
        # controllable subset (tie: smaller K, then worst-ratio margin).
        resolved = max(robustness,
                       key=lambda r: (r["robust_count_ge_gate"], -r["K"],
                                      r["robust_worst_ratio"]))
        fallback = True
    out["item1_controllability"] = {
        "registered_search_trace": trace,
        "gate_reading_ruling": (
            "PR-6 §B letter references ring-1's gradient; when ring 1 is not "
            "a tap that reference is itself starved and K=2 sets pass with "
            "rings at ~1e-5 of the max — the hollow-gate pathology the gate "
            "replaces. Operative reading (recorded): reference = the max "
            "ring. Both co-reported per candidate."),
        "robustness_protocol": (
            f"per-ring ratio = min over drive seeds {list(ROBUST_SEEDS)}; "
            "gate binds on the min (adopted before finalist evaluation — "
            "single-seed worst margins flicker ×20 with the realization)"),
        "finalist_robustness": robustness,
        "fallback_c_triggered": fallback,
        "resolved_B": {"taps_1based": resolved["taps_1based"],
                       "K": resolved["K"],
                       "robust_count_ge_gate": resolved["robust_count_ge_gate"],
                       "robust_worst_ratio": resolved["robust_worst_ratio"]},
    }
    print(f"    → resolved B = taps {resolved['taps_1based']} "
          f"({resolved['robust_count_ge_gate']}/32 robust; fallback (c) "
          f"{'TRIGGERED' if fallback else 'not triggered'})")

    # ---- Item 2: r_min sweep + build-up factors ---------------------- #
    print("[2] r_min sweep (clause (a) alone)")
    item2 = {}
    for lab in ("C-1", "C-2", "C-3"):
        r_star = find_crossing(lab, 0.0)
        r_a = find_crossing(lab, M_KAPPA)
        item2[lab] = {"r_star_lasing": round(r_star, 6),
                      "r_a_clause_a": round(r_a, 6),
                      "r_min": round(r_a + DELTA_R, 6),
                      "kappa_net_over_ki_at_r_min":
                          round(kappa_net_over_ki(lab, r_a + DELTA_R), 6)}
        print(f"    {lab}: r*={r_star:.4f}  r_a={r_a:.4f}  "
              f"r_min={r_a + DELTA_R:.4f}")
    r_a_c2 = item2["C-2"]["r_a_clause_a"]
    r_min_c2 = item2["C-2"]["r_min"]
    # E-ratios (C-2): as-built measured, closed-form, self-consistent.
    E_theta0 = measured_settled_energy("C-2", cellmod.R0_THETA0)
    E_floor = measured_settled_energy("C-2", r_a_c2)
    E_rmin = measured_settled_energy("C-2", r_min_c2)

    def closed(r):
        kn = kappa_net_over_ki("C-2", r)
        return 2.0 * r / kn ** 2
    cf_ratio_floor = closed(r_a_c2) / closed(cellmod.R0_THETA0)
    sc_theta0 = self_consistent_gain("C-2", cellmod.R0_THETA0)
    sc_floor = self_consistent_gain("C-2", r_a_c2)
    sc_rstar = self_consistent_gain("C-2", item2["C-2"]["r_star_lasing"])
    esym_band_theta0 = (5e-6, 9e-5)      # frozen §G(iii) registered band
    item2["C-2_energy_ratios"] = {
        "settled_E_theta0_photons": E_theta0,
        "settled_E_at_clause_a_floor_photons": E_floor,
        "settled_E_at_r_min_photons": E_rmin,
        "measured_buildup_factor_floor_vs_theta0": E_floor / E_theta0,
        "measured_buildup_factor_r_min_vs_theta0": E_rmin / E_theta0,
        "closed_form_factor_floor_vs_theta0_asbuilt": cf_ratio_floor,
        "self_consistent_P_circ_ratio_floor_vs_theta0":
            sc_floor["P_circ_W"] / sc_theta0["P_circ_W"],
        "self_consistent_P_circ_ratio_rstar_vs_theta0":
            sc_rstar["P_circ_W"] / sc_theta0["P_circ_W"],
        "E_sym_over_E_sat_band_theta0": esym_band_theta0,
        "E_sym_over_E_sat_band_at_floor_asbuilt": [
            esym_band_theta0[0] * E_floor / E_theta0,
            esym_band_theta0[1] * E_floor / E_theta0],
        "E_sym_over_E_sat_band_at_rstar_selfconsistent": [
            esym_band_theta0[0] * sc_rstar["P_circ_W"] / sc_theta0["P_circ_W"],
            esym_band_theta0[1] * sc_rstar["P_circ_W"] / sc_theta0["P_circ_W"]],
        "note": ("as-built rollout has no steady state AT r* (κ_net→0); "
                 "r* row uses the field-consistent solve (finite there)."),
    }
    out["item2_r_min"] = item2
    print(f"    C-2 build-up floor/θ₀: measured ×{E_floor / E_theta0:.1f}, "
          f"closed-form ×{cf_ratio_floor:.1f}, self-consistent "
          f"×{sc_floor['P_circ_W'] / sc_theta0['P_circ_W']:.1f}")

    # ---- Item 3: δ-de-saturation characterization -------------------- #
    print("[3] δ-de-saturation sweep (band [−κᵢ, +κᵢ])")
    d_rmin = delta_desaturation_row("C-2", r_min_c2)
    d_theta0 = delta_desaturation_row("C-2", cellmod.R0_THETA0)
    r_a_daware = delta_aware_r_crossing("C-2", M_KAPPA)
    out["item3_delta_desaturation"] = {
        "at_r_min": {k: d_rmin[k] for k in
                     ("r", "kappa_net_onres_over_ki", "kappa_net_worst_over_ki")},
        "at_theta0": {k: d_theta0[k] for k in
                      ("r", "kappa_net_onres_over_ki", "kappa_net_worst_over_ki")},
        "sweep_at_r_min": d_rmin["sweep"],
        "hypothetical_delta_aware_r_a": round(r_a_daware, 6),
        "hypothetical_delta_aware_r_min": round(r_a_daware + DELTA_R, 6),
        "delta_aware_minus_onres_r_min": round(r_a_daware - r_a_c2, 6),
    }
    print(f"    κ_net/κᵢ at r_min: on-res {d_rmin['kappa_net_onres_over_ki']:.4f}"
          f" → worst-δ {d_rmin['kappa_net_worst_over_ki']:.4f}; "
          f"δ-aware r_min would be {r_a_daware + DELTA_R:.4f} "
          f"(+{r_a_daware - r_a_c2:.4f})")

    # ---- Item 4: multi-tap E₀ ---------------------------------------- #
    print("[4] multi-tap E₀ (CW-equivalent reading)")
    e_single = multi_tap_E0("C-2", (0,))
    e_seed = multi_tap_E0("C-2", (0, 8, 16, 24))
    resolved_taps = (tuple(t - 1 for t in
                           out["item1_controllability"]["resolved_B"]
                           ["taps_1based"])
                     if out["item1_controllability"]["resolved_B"] else None)
    e_resolved = (multi_tap_E0("C-2", resolved_taps)
                  if resolved_taps else None)
    out["item4_multi_tap_E0"] = {
        "single_port": e_single, "seed_taps": e_seed,
        "resolved_B": e_resolved,
        "invariance_ratio_seed_vs_single":
            e_seed["E0_measured"] / e_single["E0_measured"],
        "invariance_ratio_resolved_vs_single":
            (None if e_resolved is None else
             e_resolved["E0_measured"] / e_single["E0_measured"])}
    print(f"    E₀ single {e_single['E0_measured']:.4g} vs seed-taps "
          f"{e_seed['E0_measured']:.4g} vs resolved "
          f"{(e_resolved or {'E0_measured': float('nan')})['E0_measured']:.4g} "
          f"(closed form {e_single['E0_closed_form_single_port']:.4g})")

    with open(os.path.join(OUT_DIR, "s0_4_0_calibration.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote", os.path.join(OUT_DIR, "s0_4_0_calibration.json"))


if __name__ == "__main__":
    main()
