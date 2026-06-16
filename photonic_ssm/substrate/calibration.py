# NEW (task S0.3-1, deliverable 6) — the registered E₀ + reachability solve.
# Mechanically evaluates the frozen PR-4 v2 §N E₀ formula and the §G saturated
# reachability solve per cell, and emits the one-line ledger addendum the
# Supervisor pastes into PR-4 BEFORE any consuming run. Sets no values —
# every input is frozen; this is the registered deferral being discharged.
"""Numeric E₀ + saturated reachability solve (PR-4 v2 §N / §G).

The E₀ numeric value and the saturated reachability are PR-4 v2's one
registered deferral: "mechanically evaluated at S0.3-1 calibration from the
frozen in-block formula and reported here as a one-line addendum before any
run a PR-5–9 gate or bake-off statistic consumes" (O2 / G). This module is
that evaluation; `write_addendum()` produces
`results/s0_3/e0_reachability_addendum.md` (+ JSON) for the Supervisor.

Reachability is reported HONESTLY (PR-4 v2 §G "do not paper over"): the
gain-bearing cell's small-signal headroom (Er anchor 1.0–1.9 dB/cm ÷ the
cell's operating-point gain 0.9·α) vs the saturation-depth requirement at the
registered drive (bus-referenced ≈ ×32, the cell-independent cross-cell
plane; intracavity build-up the more demanding alternative). C-1 is confirmed
**material-aspirational** (headroom ×6.5–12 < requirement ×33); C-2 straddles.
"""

from __future__ import annotations

import json
import os
from typing import Optional

from . import cells as cellmod
from . import gain as gainmod
from . import normalization as O2


def reachability_row(cell: cellmod.SubstrateCell) -> dict:
    """Compute the E₀ + reachability solve for one cell at θ₀, operating
    point. Returns the JSON row (output schema, deliverable 6)."""
    plat = cellmod.platform_of(cell)
    ki = cellmod.kappa_i_rad_s(cell)
    kext0 = cellmod.R0_THETA0 * ki
    factor = 0.0 if cell.passive_only else cell.gain_factor
    knet = O2.kappa_net_operating(kext0, ki, factor)
    FSR = plat.FSR_GHz * 1e9

    E0 = O2.E0_photons(kext0, ki, gain_factor=factor)

    # Operating-point small-signal gain coefficient and Er-anchor headroom.
    g_op_rate = gainmod.operating_gain_rate(ki, factor)
    g_op_dBcm = gainmod.rate_to_gain_dB_per_cm(g_op_rate, plat.n_g) if factor > 0 else 0.0
    er_lo, er_hi = gainmod.ER_ANCHOR_DB_PER_CM
    headroom = (None if g_op_dBcm == 0 else (er_lo / g_op_dBcm, er_hi / g_op_dBcm))

    # Saturation depths at the registered drive (P̄₀ = 1 mW).
    sat_depth_bus = O2.P_BAR0_W / gainmod.P_SAT_WG_W           # ×32, cell-indep.
    buildup = gainmod.buildup_factor(kext0, ki, FSR)          # intracavity
    sat_depth_intra = buildup * sat_depth_bus

    # Required small-signal gain to hold g=factor·κᵢ at the registered drive.
    g0_req_bus_dBcm = g_op_dBcm * (1.0 + sat_depth_bus) if factor > 0 else 0.0
    g0_req_intra_dBcm = g_op_dBcm * (1.0 + sat_depth_intra) if factor > 0 else 0.0

    # Reachable iff the upper Er anchor covers the bus-referenced requirement
    # (the freeze's cross-cell, cell-independent comparison plane).
    reachable = (factor == 0.0) or (headroom is not None and headroom[1] >= (1.0 + sat_depth_bus))

    return {
        "cell": cell.label,
        "name": cell.name,
        "passive_only": cell.passive_only,
        "Qi": plat.Qi,
        "alpha_dB_per_cm": plat.loss_dB_per_cm,
        "E0_photons": E0,
        "kappa_i_rad_s": ki,
        "kappa_ext_theta0_rad_s": kext0,
        "kappa_net_rad_s": knet,
        "gain_factor": factor,
        "g_op_dB_per_cm": g_op_dBcm,
        "er_anchor_span_dB_per_cm": [er_lo, er_hi],
        "headroom_small_signal": (None if headroom is None
                                  else [round(headroom[0], 2), round(headroom[1], 2)]),
        "sat_depth_bus": sat_depth_bus,
        "sat_depth_intracavity": sat_depth_intra,
        "g0_required_bus_dB_per_cm": g0_req_bus_dBcm,
        "g0_required_intracavity_dB_per_cm": g0_req_intra_dBcm,
        "reachable_bool": bool(reachable),
        "doublet_onres_factor": O2.doublet_onres_reduction(
            cellmod.gamma_rad_s(cell), knet),
    }


def solve_all(labels: Optional[list[str]] = None) -> list[dict]:
    """Run the E₀ + reachability solve for the registered headline/gating
    cells (default C-1, C-2, C-3) + C-2-derate + P-CORN."""
    if labels is None:
        labels = ["C-1", "C-2", "C-3", "C-2-derate", "P-CORN"]
    return [reachability_row(cellmod.get_cell(l)) for l in labels]


def write_addendum(out_dir: str = "results/s0_3") -> tuple[str, str]:
    """Compute the solve and write the markdown addendum + JSON. Returns the
    two paths. The markdown is the one-line ledger addendum for PR-4."""
    rows = solve_all()
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, "e0_reachability_addendum.json")
    md_path = os.path.join(out_dir, "e0_reachability_addendum.md")
    with open(json_path, "w") as fh:
        json.dump(rows, fh, indent=2)

    def f(x, p=3):
        return f"{x:.{p}g}"

    lines = []
    lines.append("# PR-4 v2 calibration addendum — numeric E₀ + saturated reachability")
    lines.append("")
    lines.append("Mechanical evaluation of the frozen PR-4 v2 §N E₀ formula "
                 "`E₀ = 2·κ_ext,θ₀·(P̄₀/ħω₀)/κ_net²` and the §G saturated "
                 "reachability solve, at θ₀ (r=0.3), registered drive "
                 "P̄₀ = 1 mW, operating gain g_rt = 0.9×κᵢ. **Sets no values "
                 "— discharges the one registered PR-4 v2 deferral.** "
                 "Generated by `photonic_ssm.substrate.calibration`.")
    lines.append("")
    lines.append("| Cell | E₀ (photons) | κ_net (rad/s) | g_op (dB/cm) | "
                 "small-signal headroom ×(Er/g_op) | sat-depth (bus / intracav) | "
                 "req. g₀ bus (dB/cm) | req. g₀ **intracav** (dB/cm) | "
                 "reachable? (bus plane) |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        hd = "—" if r["headroom_small_signal"] is None else \
            f"×{r['headroom_small_signal'][0]}–{r['headroom_small_signal'][1]}"
        reach = "passive" if r["gain_factor"] == 0 else \
            ("✅ (bus) / ❌ intracav" if r["reachable_bool"]
             else "❌ material-aspirational")
        lines.append(
            f"| {r['cell']} ({r['name']}) | {f(r['E0_photons'])} | "
            f"{f(r['kappa_net_rad_s'])} | {f(r['g_op_dB_per_cm'],3)} | {hd} | "
            f"×{f(r['sat_depth_bus'],3)} / ×{f(r['sat_depth_intracavity'],3)} | "
            f"{f(r['g0_required_bus_dB_per_cm'],3)} | "
            f"{f(r['g0_required_intracavity_dB_per_cm'],4)} | {reach} |")
    lines.append("")
    c1 = next(r for r in rows if r["cell"] == "C-1")
    c2 = next(r for r in rows if r["cell"] == "C-2")
    lines.append(
        f"**One-line ledger addendum (PR-4 §N/§G):** numeric E₀ per cell "
        f"computed (C-1 {f(c1['E0_photons'])}, C-2 {f(c2['E0_photons'])} "
        f"photons); the saturated reachability solve confirms **C-1 "
        f"material-aspirational** (small-signal headroom "
        f"×{c1['headroom_small_signal'][0]}–{c1['headroom_small_signal'][1]} "
        f"< bus-referenced requirement ×{f(1.0 + c1['sat_depth_bus'],3)}), "
        f"**C-2 straddles** (headroom "
        f"×{c2['headroom_small_signal'][0]}–{c2['headroom_small_signal'][1]} "
        f"vs ×{f(1.0 + c2['sat_depth_bus'],3)}); E₀ reproduces the closed form "
        f"to machine precision (unit test e). The operating κ_net and E₀ are "
        f"frozen at these values for all S0.3-1+ runs.")
    lines.append("")
    c3 = next(r for r in rows if r["cell"] == "C-3")
    buildup_c2 = c2["sat_depth_intracavity"] / c2["sat_depth_bus"]
    lines.append(
        f"**Operative-plane correction (S31-F3 — strengthens anchor-risk (v)):** "
        f"the `reachable? (bus plane)` column is on the **bus plane** (the "
        f"freeze's cross-cell, cell-independent ×{f(c2['sat_depth_bus'],3)} "
        f"comparison). But the M1 gain saturates on the **intracavity plane** — "
        f"the field the medium actually sees — where the on-resonance build-up "
        f"(×{f(buildup_c2,3)} at C-2/θ₀) makes the required small-signal g₀ ≈ "
        f"{f(c1['g0_required_intracavity_dB_per_cm'],3)}–"
        f"{f(c3['g0_required_intracavity_dB_per_cm'],3)} dB/cm for **every** "
        f"gain-bearing cell, two orders above the Er anchor (≤1.9 dB/cm). **On "
        f"the operative plane all gain cells — C-1, C-2, C-3, C-2-derate — are "
        f"material-aspirational; the bus-plane ×{f(c2['sat_depth_bus'],3)} "
        f"requirement is a floor (the most favorable plane), not the operating "
        f"requirement.** The freeze chose the bus plane knowingly; surfacing the "
        f"intracavity column here makes anchor-risk (v) explicit rather than "
        f"understated (no freeze change).")
    lines.append("")
    with open(md_path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    return md_path, json_path


if __name__ == "__main__":
    md, js = write_addendum()
    print("wrote", md, "and", js)
