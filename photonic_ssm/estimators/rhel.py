# NEW (task S0.4c, 2026-07-07) — RHEL (Recurrent Hamiltonian Echo Learning,
# Pourcel & Ernoult arXiv:2506.05259; HEB: López-Pastor & Marquardt PRX 13,
# 031020) on the shared substrate, with the PR-11 honest χ³-FWM echo
# sub-model. Spec + PR-11 numeric freeze PRE-registered at 5ca8d52 (before
# this build); semantics verified against the paper (PR-11 ⚠verify-1).
"""RHEL estimator + the concrete echo sub-model (roadmap S0.4c; PR-11).

The method, as published (Hamiltonian systems): forward pass; a single
instantaneous state conjugation (momentum flip Σ_z — optically, phase
conjugation of the state snapshot); an echo pass through the SAME dynamics
with the input replayed time-reversed and a continuous nudge force
−(±ε)·i·∂ℓ/∂a* injected; the gradient is the symmetric finite difference of
∇_θH_coh between the (+ε) and (−ε) echo trajectories.

Dissipative-operational realization (PR-7.1 extension): the Hamiltonian
re-traversal chaining is unavailable and state cloning is unphysical, so
each nudged echo needs its own physical forward —

    update = fwd(+) → C_op → echo(+ε)  +  fwd(−) → C_op → echo(−ε)
           = 2 forward + 2 echo = 4 device passes (batch-scaled), digital 0.

The echo sub-model C_op (PR-11 mechanism A, numeric freeze in the S0.4c
spec): per ring j, computed LIVE from the commanded parameters,

    η_c,j = η_ex,j² · η_spiral · exp(−κ_net,j·τ_c),   η_ex,j = 2κ_ext,j/κ_net,j,
    η_spiral = (γ_nl·P_p·L)²  (γ_nl = 0.97 /W/m, P_p = 0.3 W, L = 0.5 m),
    τ_c = 1/mean(κ_net);
    C_op: a_j → √η_c,j · e^{iφ_err} · a_j* · (1 + ξ_RIN) + √(1+η_c,j) · v_j,

with v the phase-insensitive parametric floor (⟨|v|²⟩ = 1 photon,
conservative convention) and ξ_RIN the pump-transfer excess (−145 dBc/Hz
class over the state band). Fresh draws per conjugation event (C_op fires
once per echo pass — twice per update). Invariants (PR-11): fresh
independent ASE streams every pass; NO loss-sign flip (the echo runs the
same dissipative Φ); gain ASE present in echo passes.

Registered sim simplification (nudge): ℓ_k = (ŷ_k − d_k)² with the FIR
head's lag buffer treated as frozen context — only the instantaneous y_k
term is differentiated. The R1 floor check compares against BPTT of this
SAME truncated functional.

Registered structural limitation: ∇_θH_coh sees only the COHERENT generator
(δ|a|², μ couplings, the √(2κ_ext) drive coupling) — κ_ext's dissipative
channel (the 2κ_ext decay) is invisible to the echo update. Measured by the
bake-off, not patched.
"""

from __future__ import annotations

import math
from typing import Optional

import torch

from ..dynamics.coupled_rings import zoh_discretize
from ..substrate.ase import ASEInjector
from ..substrate.dissipative_ring import DissipativeRingSubstrate

# PR-11 numeric freeze (S0.4c spec, 5ca8d52) — mechanism A.
GAMMA_NL = 0.97          # /W/m  (n₂ = 2.4e-19 m²/W, A_eff = 1 µm²)
P_PUMP_W = 0.3           # per arm
L_SPIRAL_M = 0.5
PHI_ERR = 0.0            # headline; ±π/20 = S0.5 sensitivity row
PUMP_RIN_DBC_HZ = -145.0  # class value (⚠cite at S0.8)
ETA_SPIRAL = (GAMMA_NL * P_PUMP_W * L_SPIRAL_M) ** 2


def conjugation_efficiency(sub: DissipativeRingSubstrate) -> torch.Tensor:
    """Per-ring end-to-end η_c (energy), live from the commanded params."""
    kn = sub.kappa_net().detach()
    eta_ex = 2.0 * sub.kappa_ext.detach() / kn
    tau_c = 1.0 / float(kn.mean())
    return eta_ex ** 2 * ETA_SPIRAL * torch.exp(-kn * tau_c)


def c_op(sub: DissipativeRingSubstrate, aT: torch.Tensor, ideal: bool,
         generator: Optional[torch.Generator] = None) -> torch.Tensor:
    """One physical conjugation event on the (batch, 2N) state snapshot."""
    if ideal:
        return aT.conj()
    eta = conjugation_efficiency(sub)
    eta2 = torch.cat([eta, eta]).to(aT.real.dtype)        # CW ++ CCW
    # Pump-transfer excess: integrated RIN over the state band.
    kn = sub.kappa_net().detach()
    band_hz = (2.0 * float(sub.kappa_i) + float(kn.max())) / (2.0 * math.pi)
    sigma_rin = math.sqrt(10.0 ** (PUMP_RIN_DBC_HZ / 10.0) * band_hz)
    shape = aT.shape
    xi = sigma_rin * torch.randn(shape[0], generator=generator,
                                 dtype=aT.real.dtype).unsqueeze(-1)
    # Phase-insensitive parametric floor, ⟨|v|²⟩ = 1 photon per mode.
    v = (torch.randn(*shape, generator=generator, dtype=aT.real.dtype)
         + 1j * torch.randn(*shape, generator=generator,
                            dtype=aT.real.dtype)) / math.sqrt(2.0)
    phase = complex(math.cos(PHI_ERR), math.sin(PHI_ERR))
    return (torch.sqrt(eta2) * phase * aT.conj() * (1.0 + xi)
            + torch.sqrt(1.0 + eta2) * v.to(aT.dtype))


def coherent_H(sub: DissipativeRingSubstrate, a: torch.Tensor,
               u_k: torch.Tensor) -> torch.Tensor:
    """The coherent generator H_coh(θ; a, u) per step, summed over batch —
    the θ-bearing part only (γ backscatter is fixed → omitted; the
    dissipative κ terms are NOT Hamiltonian → structurally absent).
    Signs fixed by da/dt = −i ∂H/∂a* matching the substrate EOM
    (+iδa, +iΩa, +Bu):  H = −Σδ|a|² − a†Ωa − 2·Im(a†Bu)."""
    N = sub.N
    a_cw, a_ccw = a[..., :N], a[..., N:]
    h = -(sub.delta * (a_cw.abs() ** 2 + a_ccw.abs() ** 2)).sum()
    if N >= 2:
        cross = (a_cw[..., :-1].conj() * a_cw[..., 1:]
                 + a_ccw[..., :-1].conj() * a_ccw[..., 1:])
        h = h - 2.0 * (sub.mu_chain * cross.real).sum()
    # Drive coupling: taps only, weight w = 1/√K, b_t = w·√(2κ_ext,t).
    K = len(sub.input_taps)
    w = 1.0 / math.sqrt(K)
    taps = list(sub.input_taps)
    b = w * torch.sqrt(2.0 * sub.kappa_ext[taps])
    z = (a_cw[..., taps].conj() * b.to(a.dtype) * u_k.reshape(-1, 1)).sum()
    return h - 2.0 * z.imag


class RHELEstimator:
    """4-device-pass RHEL gradient on the shared substrate (PR-7.1 ext).

    step(u, target, head, y_scale, gens) assigns .grad on {δ, κ_ext, μ}
    from measured trajectories only (no autodiff through the substrate:
    ∇_θH_coh is a local analytic readout on detached states — the PR-6
    physical-operations invariant holds structurally). Returns y (forward
    pass 1) for the harness' loss trace + head step."""

    def __init__(self, sub: DissipativeRingSubstrate, ideal_echo: bool,
                 eps_frac: float = 0.05):
        self.sub = sub
        self.ideal_echo = ideal_echo
        self.eps_frac = eps_frac
        self.n_device_passes = 0
        self.n_digital_passes = 0
        # Sign convention resolved empirically per the R1 protocol (probe
        # 2026-07-07): with +1, cosine(Δθ, ∇θ) → +0.9986 monotonically as
        # dissipation → 0 (κ_net·T·dt: 1.02→0.034 gives 0.72→0.9986).
        self.sign = +1.0

    # -- device passes ------------------------------------------------- #
    def _matrices(self):
        with torch.no_grad():
            M = self.sub.M_doublet()
            B = self.sub.B_doublet()
            Phi, Gamma = zoh_discretize(M, B, self.sub.dt)
            inject = None
            g = self.sub.gain_rate_per_ring()
            g2 = torch.cat([g, g])
            if self.sub.ase_variance_scale > 0.0 and float(g2.abs().sum()) > 0:
                inject = ASEInjector(M, g2, self.sub.nf_dB, self.sub.dt,
                                     convention=self.sub.ase_convention,
                                     variance_scale=self.sub.ase_variance_scale,
                                     tau_rt=self.sub.tau_rt)
        return Phi, Gamma, inject

    def _forward_pass(self, u, generator):
        """Physical forward: returns (states (b,T+1,2N), y (b,T)). Device."""
        with torch.no_grad():
            states, outputs = self.sub.forward(u, generator=generator)
            y = self.sub.intensity(outputs).squeeze(-1)     # (batch, T)
        self.n_device_passes += u.shape[0]
        return states, y

    def _echo_pass(self, u, a0, sgn_eps, eps_eff, w0_over_ys, resid_rev,
                   generator):
        """Physical echo: same dissipative Φ, time-reversed phase-flipped
        drive replay, nudge force ±ε·G_k with
        G_k = −i·∂ℓ_k/∂a*_k = −i·2·resid·(w0/y_scale)·conj(C)·(C·ã).
        The residuals are the STORED forward-pass errors replayed
        time-reversed (digitally stored, optically injected — in the
        theorem's conservative limit these coincide with the echo-state
        residuals; with dissipation the stored form is the faithful
        realization of 'error computed at the output, injected back').
        Returns the echo state trajectory (b, T, 2N). Device."""
        Phi, Gamma, inject = self._matrices()
        batch, T, _ = u.shape
        u_rev = torch.flip(u, dims=[1])
        C_row = self.sub.C_doublet()[0]                    # (2N,)
        with torch.no_grad():
            # Time-reversed replay: the retracing recursion is
            # ã_{j+1} = Φ(ã_j − Γ*·u(T−1−j)) — the CONJUGATE drive,
            # subtracted BEFORE propagation (exact discrete inverse of the
            # forward step under conservative Φ; the phase-flipped replay
            # is what "un-writes" the input on the way back).
            forcing = (u_rev.to(Gamma.dtype)
                       @ Gamma.conj().transpose(0, 1))
            a = a0.clone()
            states = []
            PhiT = Phi.transpose(0, 1)
            for k in range(T):
                a = (a - forcing[:, k, :]) @ PhiT
                if inject is not None:
                    a = a + inject.sample(batch, generator).to(a.dtype)
                Ca = a @ C_row
                # G_k = −i·2·resid·(w0/y_scale)·conj(C)·(C·ã)
                dl_da_conj = (2.0 * resid_rev[:, k] * w0_over_ys
                              ).unsqueeze(-1) \
                    * (C_row.conj().unsqueeze(0) * Ca.unsqueeze(-1))
                a = a + sgn_eps * eps_eff * (-1j) * dl_da_conj * self.sub.dt
                states.append(a.clone())
        self.n_device_passes += batch
        return torch.stack(states, dim=1)

    # -- the update ----------------------------------------------------- #
    def _grad_H(self, states, u_rev):
        """Σ_k dt·∇_θ H_coh along a measured echo trajectory (autograd on
        H_coh only — states detached). The echo's actual drive is the
        phase-flipped replay d = −u(−t) (see _echo_pass), so H_coh is
        evaluated with that drive."""
        T = states.shape[1]
        H = 0.0
        for k in range(T):
            H = H + coherent_H(self.sub, states[:, k, :],
                               -u_rev[:, k, 0])
        H = H * self.sub.dt
        return torch.autograd.grad(
            H, (self.sub.delta, self.sub.kappa_ext, self.sub.mu_chain),
            allow_unused=False)

    def step(self, u, target, head, y_scale,
             gen_f1=None, gen_e1=None, gen_f2=None, gen_e2=None,
             gen_c1=None, gen_c2=None):
        """One RHEL update: assigns .grad on the in-situ partition.
        Returns y (forward pass 1, measured)."""
        w0_over_ys = float(head.lin.weight.detach()[0, 0]) / y_scale
        u_rev = torch.flip(u, dims=[1])

        # Pass pair (+ε): its own physical forward, conjugation, echo.
        st1, y1 = self._forward_pass(u, gen_f1)
        aT1 = c_op(self.sub, st1[:, -1, :], self.ideal_echo, gen_c1)
        # The error signal: full-head residuals on the MEASURED forward
        # output (digital), stored and replayed time-reversed in the echo.
        with torch.no_grad():
            resid = head(y1 / y_scale) - target        # (batch, T)
            resid_rev = torch.flip(resid, dims=[1])
            # Nudge scale from measured forward quantities (a calibration
            # knob: force sized to ε_frac of the state scale).
            a_rms = float(st1[:, 1:, :].abs().pow(2).mean().sqrt())
            C_row = self.sub.C_doublet()[0]
            Ca = st1[:, 1:, :] @ C_row
            G_f = (2.0 * resid * w0_over_ys).unsqueeze(-1) \
                * (C_row.conj().unsqueeze(0) * Ca.unsqueeze(-1))
            g_rms = float(G_f.abs().pow(2).mean().sqrt()) + 1e-300
        eps_eff = self.eps_frac * a_rms / g_rms

        e_plus = self._echo_pass(u, aT1, +1.0, eps_eff, w0_over_ys,
                                 resid_rev, gen_e1)
        # Pass pair (−ε).
        st2, _ = self._forward_pass(u, gen_f2)
        aT2 = c_op(self.sub, st2[:, -1, :], self.ideal_echo, gen_c2)
        e_minus = self._echo_pass(u, aT2, -1.0, eps_eff, w0_over_ys,
                                  resid_rev, gen_e2)

        g_plus = self._grad_H(e_plus, u_rev)
        g_minus = self._grad_H(e_minus, u_rev)
        for p, gp, gm in zip(
                (self.sub.delta, self.sub.kappa_ext, self.sub.mu_chain),
                g_plus, g_minus):
            g = self.sign * (gp - gm) / (2.0 * eps_eff)
            p.grad = g if p.grad is None else p.grad + g
        # The harness computes the reported loss on y1 (identical convention
        # to every other method); this estimator only fills the grads.
        return y1
