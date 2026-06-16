# NEW (task S0.3-1, deliverable 3) — A2 continuous Langevin ASE.
# Implements the frozen PR-4 v2 §G ASE convention. Built on the salvaged
# photonic_ssm.gain ASE scaling (n_sp, h_nu); the per-round-trip ASE
# *accumulation inside the rollout* is new S0.3 physics. Sets no values:
# n_sp comes from the cell NF (frozen PR-4 v2 §C).
"""A2 continuous Langevin ASE — the substrate's noise mechanism (PR-4 v2 §G).

Amplified spontaneous emission enters each amplified cavity mode as a
continuous Langevin force F(t) in the CMT ODE

    da/dt = M a + B u + F,    ⟨F_j(t) F_k*(t')⟩ = 2 κ_g,j n_sp δ_jk δ(t−t'),

(photon units; κ_g,j = the per-ring gain rate g, n_sp the spontaneous-
emission factor from the cell's NF). Discretized to compose with the S0.1
ZOH/van-Loan step a_{k+1} = Φ a_k + Γ u_k + η_k, the per-step ASE increment
η_k is complex circular Gaussian with the exact process-noise covariance

    Q_d = ∫₀^dt e^{M s} D e^{M† s} ds,   D = diag(2 κ_g,j n_sp),

computed by Van Loan's augmented-matrix exponential (the SAME exact
discretization as Φ, Γ). **A1** (the registered first-order-equivalent
alternative) uses the per-round-trip discrete kick Q_d ≈ D·dt; the two
agree to O(κ_net·dt) ~ 1e-3 at the registered cells (per-rt gains ≤ 0.2 dB)
— the A1↔A2 statistical-equivalence unit test (d).

Steady state (single mode): ⟨|a|²⟩ = D/(2κ_net) = κ_g n_sp/κ_net. At the
90 %-compensation characterization point (κ_net = 0.1κᵢ, κ_g = 0.9κᵢ) this
is the corner-independent n_ss = 9·n_sp ≈ 23 (NF-7) / 9 (NF-3) — unit test
(f). (The operating κ_net in the rollout additionally carries 2κ_ext.)

PR-11 carry-in: **fresh draws per pass; forward and echo streams
independent** (no common-RNG reversal). The injector takes an explicit
generator; forward and echo must pass DIFFERENT generators. The noise path
does NOT carry a gradient (exogenous); the deterministic Φ a + Γ u path
stays autograd-safe (house constraint 3a) — adding a detached η preserves
∂loss/∂params through Φ, Γ.

**Registered convention (S31-F6 → PR-6): the ASE covariance Q_d AND the
noise realization η are intentionally detached from the parameter gradient.**
Q_d = Q_d(M(δ,κ_ext,μ), g) is a function of the trainable parameters and
η = L·z (L = chol Q_d) is a reparameterized draw, so a reparameterization
gradient ∂η/∂params *through the noise amplitude/covariance* exists in
principle. It is **dropped by design** — `process_noise_cov_A2/A1` and
`sample()` run under `no_grad`. Rationale: ASE is an exogenous, hardware-
faithful noise source whose statistics the device does not let the optimizer
shape; the in-situ training signal must come from the deterministic recurrence,
not from steering the noise floor. This is held **identically across all four
estimators** (SPSA's model-free forward passes never see it; PAT/adjoint/BPTT
would expose it, so they are pinned to the same convention) — preserving the
shared-substrate standard. The freeze says "no detach in the *state* path"; this
registers the companion choice it left open (no reparameterization gradient
through the *noise* path).
"""

from __future__ import annotations

import torch

from .cells import n_sp_from_nf_dB


def diffusion_diag(g_rate_per_mode: torch.Tensor, n_sp: float) -> torch.Tensor:
    """Per-mode ASE diffusion coefficient D_j = 2·κ_g,j·n_sp [photons/s].
    `g_rate_per_mode` is the gain rate of each mode [rad/s] (0 for passive
    modes — no gain ⇒ no ASE). Returns a real (M,) tensor."""
    return 2.0 * g_rate_per_mode * n_sp


def process_noise_cov_A2(M: torch.Tensor, D_diag: torch.Tensor, dt: float
                         ) -> torch.Tensor:
    """Exact per-step ASE process-noise covariance Q_d = ∫₀^dt e^{Ms} D
    e^{M†s} ds via Van Loan's augmented matrix exponential:

        Z = [[ -M ,  D  ],   expm(Z·dt) = [[B11, B12],
             [  0 ,  M† ]]                  [ 0 , B22]],
        Φ = B22† = e^{M dt},   Q_d = Φ · B12.

    M: (n,n) complex; D_diag: (n,) real ASE diffusion. Returns a Hermitian
    PSD (n,n) complex Q_d. Computed under no_grad (the noise path is
    exogenous — house note: noise needs no gradient)."""
    with torch.no_grad():
        n = M.shape[-1]
        cdtype = M.dtype
        D = torch.diag(D_diag.to(cdtype))
        Z = M.new_zeros((2 * n, 2 * n))
        Z[:n, :n] = -M
        Z[:n, n:] = D
        Z[n:, n:] = M.conj().transpose(-1, -2)
        E = torch.matrix_exp(Z * dt)
        B12 = E[:n, n:]
        B22 = E[n:, n:]
        Phi = B22.conj().transpose(-1, -2)
        Qd = Phi @ B12
        # Hermitize against round-off so Cholesky is clean.
        Qd = 0.5 * (Qd + Qd.conj().transpose(-1, -2))
    return Qd


def process_noise_cov_A1(M: torch.Tensor, D_diag: torch.Tensor, dt: float,
                         tau_rt: float) -> torch.Tensor:
    """Per-round-trip discrete-kick covariance — convention A1. The ASE is
    injected as a discrete kick D·τ_rt once per round trip and decays between
    kicks; accumulated over one sample period dt (= n_rt round trips) this is
    the Riemann sum

        Q_d^A1 = Σ_{k=0}^{n_rt−1} Φ_rt^k (D·τ_rt) (Φ_rt^k)†,  Φ_rt = e^{M·τ_rt},

    which is the rectangle-rule approximation of the A2 integral ∫₀^dt e^{Ms} D
    e^{M†s} ds. The two agree to O(κ_net·τ_rt) ~ 1e-3 (the per-round-trip
    decay; "per-rt gains ≤ 0.2 dB") — NOT O(κ_net·dt) — because the
    discretization resolves every round trip, not just the sample. This is the
    first-order-equivalent the A1↔A2 unit test (d) measures. (Validation-only;
    the rollout always uses A2.)"""
    with torch.no_grad():
        n = M.shape[-1]
        n_rt = max(1, int(round(dt / tau_rt)))
        Phi_rt = torch.matrix_exp(M * tau_rt)
        cdtype = M.dtype
        Dk = torch.diag(D_diag.to(cdtype)) * tau_rt
        acc = Dk.clone()                     # k = 0 term
        Ak = torch.eye(n, dtype=cdtype)
        for _ in range(1, n_rt):
            Ak = Phi_rt @ Ak
            acc = acc + Ak @ Dk @ Ak.conj().transpose(-1, -2)
        return 0.5 * (acc + acc.conj().transpose(-1, -2))


class ASEInjector:
    """Per-episode ASE injector. The gain operating point (hence D) and M are
    fixed within an episode (M1), so the per-step covariance Q_d and its
    Cholesky factor are precomputed once and reused for all T steps.

    Parameters
    ----------
    M          : (n,n) complex episode system matrix (doublet 2N×2N).
    g_rate_per_mode : (n,) gain rate per mode [rad/s] (0 for passive modes).
    nf_dB      : cell noise figure → n_sp.
    dt         : step [s] (= round-trip time / sampling period).
    convention : "A2" (exact Langevin, default) or "A1" (per-rt kick).
    variance_scale : the registered ASE-variance KNOB (F18; multiplies Q_d;
                 0 ⇒ noiseless limit; 1 ⇒ registered level).
    """

    def __init__(self, M: torch.Tensor, g_rate_per_mode: torch.Tensor,
                 nf_dB: float, dt: float, convention: str = "A2",
                 variance_scale: float = 1.0, tau_rt: float | None = None):
        self.dt = float(dt)
        self.convention = convention
        self.variance_scale = float(variance_scale)
        self.cdtype = M.dtype
        self.rdtype = M.real.dtype
        self.n = M.shape[-1]
        self.n_sp = n_sp_from_nf_dB(nf_dB)
        D_diag = diffusion_diag(g_rate_per_mode.to(self.rdtype), self.n_sp)
        if convention == "A2":
            Qd = process_noise_cov_A2(M, D_diag, self.dt)
        elif convention == "A1":
            if tau_rt is None:
                raise ValueError("A1 (per-round-trip kick) needs tau_rt.")
            Qd = process_noise_cov_A1(M, D_diag, self.dt, float(tau_rt))
        else:
            raise ValueError(f"ASE convention must be 'A1' or 'A2', got {convention!r}")
        self.Qd = Qd * self.variance_scale
        # Cholesky factor L (Qd = L L†); jitter-guarded for the passive/zero
        # rows (modes with no gain have D=0 → a zero row/col).
        with torch.no_grad():
            jitter = 1e-30
            eye = torch.eye(self.n, dtype=self.cdtype)
            try:
                self.L = torch.linalg.cholesky(self.Qd + jitter * eye)
            except Exception:
                # Fall back to a PSD-safe eigen-decomposition sqrt.
                w, V = torch.linalg.eigh(self.Qd)
                w = torch.clamp(w.real, min=0.0)
                self.L = V @ torch.diag(torch.sqrt(w).to(self.cdtype))

    def sample(self, batch: int, generator: torch.Generator | None = None
               ) -> torch.Tensor:
        """Draw `batch` fresh ASE increments η ~ CN(0, Q_d), shape
        (batch, n) complex. Exogenous (no grad). PR-11: pass DIFFERENT
        generators for the forward and echo streams."""
        with torch.no_grad():
            re = torch.randn((batch, self.n), generator=generator,
                             dtype=self.rdtype)
            im = torch.randn((batch, self.n), generator=generator,
                             dtype=self.rdtype)
            z = (re + 1j * im) / (2.0 ** 0.5)   # ⟨|z|²⟩ = 1, circular
            return z.to(self.cdtype) @ self.L.transpose(-1, -2)


def steady_state_photons(D: float, kappa_net: float) -> float:
    """Analytic single-mode steady-state ASE photon number ⟨|a|²⟩ =
    D/(2κ_net) = κ_g n_sp/κ_net (continuous Langevin). The basis of test (f)
    and the A1↔A2 comparison."""
    return D / (2.0 * kappa_net)
