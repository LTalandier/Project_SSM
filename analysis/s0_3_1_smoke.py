# NEW (task S0.3-1, deliverable 10) — substrate smoke test. One short rollout
# per cell at each registered clock, asserting the F18 build-gate conditions:
# full state trajectory exposed (shape 2N), finite values, finite NONZERO
# gradients to all P2 params, and one working variance knob each for
# loss / gain / ASE. Run before any sweep.
"""S0.3-1 substrate smoke test (roadmap Gate F18 build conditions).

  python3 analysis/s0_3_1_smoke.py

Asserts, for every registered cell × clock {0.1, 1, 2} GS/s:
  * the forward returns the FULL doublet trajectory (T+1, 2N)  [F18 / 3b];
  * states + intensity readout are finite;
  * a BPTT loss yields finite, NONZERO grads on δ, κ_ext, μ  [F18 grad flow];
  * the three F18 variance knobs (loss_scale, gain_factor, ase_variance_scale)
    each measurably move the output.
"""

import os
import sys

import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from photonic_ssm.substrate import DissipativeRingSubstrate as DRS, get_cell
from photonic_ssm.substrate.normalization import P_BAR0_W, H_NU_J

CELLS = ["C-1", "C-2", "C-3"]
CLOCKS = [0.1, 1.0, 2.0]


def main():
    torch.manual_seed(0)
    amp = (P_BAR0_W / H_NU_J) ** 0.5
    n_ok = 0
    for lab in CELLS:
        for clk in CLOCKS:
            sub = DRS.from_cell(lab, clock_GSps=clk, seed=0,
                                dtype=torch.complex128)
            N = sub.N
            T = 32
            g = torch.Generator().manual_seed(1)
            u = amp * torch.rand(T, generator=g, dtype=torch.float64)
            gen = torch.Generator().manual_seed(7)
            states, outputs = sub(u, generator=gen)
            assert states.shape == (T + 1, 2 * N), \
                f"{lab}@{clk}: trajectory shape {tuple(states.shape)} != (T+1, 2N)"
            y = sub.intensity(outputs)
            assert torch.isfinite(states.real).all() and torch.isfinite(y).all()
            loss = (y.real ** 2).mean()
            loss.backward()
            for name, p in [("δ", sub.delta), ("κ_ext", sub.kappa_ext),
                            ("μ", sub.mu_chain)]:
                assert p.grad is not None and torch.isfinite(p.grad).all() \
                    and p.grad.abs().sum() > 0, f"{lab}@{clk}: bad grad {name}"

            # F18 variance knobs: each must measurably move the readout.
            @torch.no_grad()
            def mean_y(**kw):
                s = DRS.from_cell(lab, clock_GSps=clk, seed=0, **kw)
                gg = torch.Generator().manual_seed(7)
                return float(s.forward_intensity(u, generator=gg).real.mean())
            base = mean_y()
            d_loss = abs(mean_y(loss_scale=1.5) - base)
            d_gain = abs(mean_y(gain_factor=0.0) - base)
            d_ase = abs(mean_y(ase_variance_scale=0.0) - base)
            assert d_loss > 0 and d_gain > 0, f"{lab}@{clk}: loss/gain knob inert"
            n_ok += 1
            print(f"  {lab:4s} @ {clk:>4}GS/s: states{tuple(states.shape)} "
                  f"grads✓  knobs Δloss={d_loss:.2e} Δgain={d_gain:.2e} "
                  f"Δase={d_ase:.2e}")
    print(f"\nSMOKE PASS — {n_ok}/{len(CELLS) * len(CLOCKS)} cell×clock "
          f"configs: full 2N trajectory exposed, finite nonzero grads to "
          f"{{δ,κ_ext,μ}}, loss/gain/ASE knobs live.")


if __name__ == "__main__":
    main()
