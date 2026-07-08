# NEW (task S0.7-full-core, 2026-07-08) — the per-method TRAINING-mode energy
# envelope, per the accounting rules PRE-registered at bd37703: the S0.5
# measured passes-to-target × the PR-10 frozen per-sample conversion stack
# (lite envelope values, cited not re-derived) + the S0.4 method adders.
"""Writes results/s0_7/training_envelope.{json}. All constants frozen/cited:

  * passes-to-target: results/s0_5/bakeoff.json (measured medians, 8 seeds)
  * per-sample conversion stack: the S0.7-lite per-sample envelope at N=32,
    1-2 GS/s (results/s0_7/s0_7_lite_envelope.json OPT/CONS rows) — the
    4-tap drive multiplies the DAC+E/O rows by 4 (S0.4-0; the lite charged
    2-4 control ch/ring separately; drive taps are the per-sample stream)
  * pass duration: T/f_s = 256 / 2 GS/s = 128 ns
  * RHEL pump: N × 0.3 W = 9.6 W per conjugation window (PR-11), 2 echoes/update
  * PAT digital ledger: 505,600 digital passes (measured); FLOPs/pass from the
    2N-dim ZOH matvec: ~8·(2N)²·T complex-MAC-FLOPs fwd, ×3 for fwd+bwd
    (order-of-magnitude class, labelled); costed at the named F16 classes
    (Brainwave 287 GFLOPS/W author-stated; generic accelerator 1 TFLOPS/W class)
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

T, FS = 256, 2e9
PASS_S = T / FS                       # 128 ns
N = 32
TAPS = 4                              # S0.4-0 resolved B
SAMPLES_PER_PASS = T

# PR-10 frozen per-sample conversion (pJ/sample) — lite memo §1/§2 rows.
STACK = {
    "OPT":  {"dac_eo_per_ch": 5.0 + 0.135 * 8,   # DAC 5 pJ + E/O 0.135 pJ/bit ×8b
             "adc_oe": 32.0 + 0.17 * 8},          # ADC 32 pJ + O/E 0.17 pJ/bit ×8b
    "CONS": {"dac_eo_per_ch": 308.0 + 15.0 * 8,   # TI DAC + 10-20 pJ/bit E/O (15 mid → labelled)
             "adc_oe": 469.0 + 1.4 * 8},
}
# NOTE: CONS uses the bracket midpoint 15 pJ/bit for E/O ONLY as a labelled
# convenience (the lite carried ranges); the range endpoints are reported too.

PASSES = {"pat-both": 38_400, "spsa": 176_000, "adjoint": 73_600,
          "rhel": None}                # censored — reported per-update instead
DIGITAL_PASSES_PAT = 505_600
RHEL_PUMP_W = N * 0.3
RHEL_UPDATE_PASSES = 4                 # 2 fwd + 2 echo (PR-7.1)

FLOPS_PER_DIGITAL_PASS = 8 * (2 * N) ** 2 * T * 3     # fwd+bwd, order-of-mag
F16 = {"Brainwave_287GFLOPSW": 287e9, "accel_1TFLOPSW_class": 1e12}


def per_pass_pj(corner):
    s = STACK[corner]
    return SAMPLES_PER_PASS * (TAPS * s["dac_eo_per_ch"] + s["adc_oe"])


def main():
    out = {"rules": "pre-registered at bd37703", "N": N, "taps": TAPS,
           "pass_duration_ns": PASS_S * 1e9,
           "per_pass_pj": {c: per_pass_pj(c) for c in STACK}}
    res = {}
    for m, p in PASSES.items():
        if p is None:
            continue
        row = {}
        for c in STACK:
            row[f"conversion_{c}_uJ"] = p * per_pass_pj(c) * 1e-6
        if m == "pat-both":
            fl = DIGITAL_PASSES_PAT * FLOPS_PER_DIGITAL_PASS
            row["digital_flops"] = fl
            for name, eff in F16.items():
                row[f"digital_J_{name}"] = fl / eff
        res[m] = row
    # RHEL per-update adder (censored overall)
    res["rhel_per_update"] = {
        "pump_uJ": RHEL_PUMP_W * PASS_S * 2 * 1e6,
        "conversion_uJ": {c: RHEL_UPDATE_PASSES * per_pass_pj(c) * 1e-6
                          for c in STACK},
    }
    out["training_energy_to_target"] = res
    os.makedirs("results/s0_7", exist_ok=True)
    with open("results/s0_7/training_envelope.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
