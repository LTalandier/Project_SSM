# NEW (task S0.1.1, Critic F1) — transient-dynamics validation. The S0.1
# gate proved the oscillator<->ring mapping by *construction* (van Loan
# exact ZOH + steady-state CW limit + pole algebra) but never integrated
# the ODE forward and compared the *transient* to an INDEPENDENT reference.
# These tests close that gap:
#   (i)  single-ring ringdown + step response vs the closed form AND vs an
#        independent scipy RK45 integration of da/dt = M a + B u, asserting
#        the decay rate kappa AND oscillation frequency delta in the TIME
#        domain (fitted from |a(t)| and arg a(t), not read off the pole);
#   (ii) a 2-ring mu!=0 case whose population-beat frequency matches the
#        Im(eig(M)) supermode splitting (and an uncoupled no-beat contrast).
# The contribution *is* the dynamical mapping, so it earns a positive
# time-domain check, independent of the package's discretization path.
"""Time-domain transient validation of the dynamical ring core (S0.1.1/F1)."""

import math

import pytest
import torch

from photonic_ssm.dynamics import CoupledRingLinOSS

# numpy + scipy are TEST-ONLY (independent RK45 reference + spectral peak
# finding); the package itself stays torch-only. Skip cleanly if absent.
np = pytest.importorskip("numpy")
solve_ivp = pytest.importorskip("scipy.integrate").solve_ivp


# ---------------------------------------------------------------------- #
#  Independent references (NOT the van Loan ZOH path under test)
# ---------------------------------------------------------------------- #

def _rk45(M, B, u_const, a0, t_eval, max_step):
    """Independent RK45 integration of da/dt = M a + B u (u held constant),
    fully independent of the package's van Loan ZOH discretization. M (N,N),
    B (N,m), u_const (m,), a0 (N,) numpy complex. scipy solve_ivp works on
    reals, so we stack [Re a; Im a]. Returns (len(t_eval), N) complex."""
    M = np.asarray(M, dtype=np.complex128)
    N = M.shape[0]
    Bu = (np.asarray(B, dtype=np.complex128) @ np.asarray(u_const,
                                                          dtype=np.complex128))

    def rhs(_t, y):
        a = y[:N] + 1j * y[N:]
        da = M @ a + Bu
        return np.concatenate([da.real, da.imag])

    y0 = np.concatenate([np.asarray(a0).real, np.asarray(a0).imag]).astype(float)
    sol = solve_ivp(rhs, (float(t_eval[0]), float(t_eval[-1])), y0,
                    method="RK45", t_eval=t_eval, rtol=1e-10, atol=1e-13,
                    max_step=max_step)
    assert sol.success, sol.message
    Y = sol.y                                       # (2N, T)
    return (Y[:N] + 1j * Y[N:]).T


def _extract_kappa_delta(a_traj, t):
    """Fit the decay rate kappa (from the slope of log|a|) and the
    oscillation frequency delta (from the slope of unwrapped arg a) purely
    in the TIME domain — no reference to the analytic pole."""
    kappa = -np.polyfit(t, np.log(np.abs(a_traj)), 1)[0]
    delta = np.polyfit(t, np.unwrap(np.angle(a_traj)), 1)[0]
    return kappa, delta


def _dominant_angular_freq(sig, dt):
    """Dominant angular frequency of a real tone via windowed rFFT with
    parabolic sub-bin peak interpolation."""
    sig = np.asarray(sig, dtype=float)
    sig = sig - sig.mean()
    spec = np.abs(np.fft.rfft(sig * np.hanning(len(sig))))
    df = np.fft.rfftfreq(len(sig), dt)[1]
    k = int(np.argmax(spec))
    shift = 0.0
    if 0 < k < len(spec) - 1:
        a_, b_, c_ = spec[k - 1], spec[k], spec[k + 1]
        denom = a_ - 2.0 * b_ + c_
        if denom != 0.0:
            shift = 0.5 * (a_ - c_) / denom
    return 2.0 * math.pi * (k + shift) * df


# ---------------------------------------------------------------------- #
#  (i) single-ring transients
# ---------------------------------------------------------------------- #

def test_single_ring_ringdown_matches_closed_form_and_rk45():
    """Free ringdown a(t) = a0 e^{(i delta - kappa) t}: the rollout must
    match the closed form AND an independent RK45, and the decay rate +
    oscillation frequency fitted from the trajectory must recover the pole."""
    kappa_tot, delta = 3.0e8, 5.0e10               # rad/s (Qi~2e6 scale)
    dt, T = 5e-12, 1600                            # 8 ns, ~2.4 e-foldings
    model = CoupledRingLinOSS([kappa_tot], [delta], dt)
    u = torch.zeros(T, 1, dtype=torch.float64)
    a0 = torch.tensor([1.0 + 0.0j], dtype=torch.complex128)
    states, _ = model(u, a0=a0)
    a_model = states[:, 0].detach().numpy()        # (T+1,)
    t = np.arange(T + 1) * dt

    # closed form
    a_cf = np.exp((1j * delta - kappa_tot) * t)
    assert np.max(np.abs(a_model - a_cf)) < 1e-9

    # independent RK45 on da/dt = M a
    M = [[-kappa_tot + 1j * delta]]
    a_rk = _rk45(M, [[1.0]], [0.0], [1.0 + 0j], t,
                 max_step=0.05 * 2 * math.pi / delta)[:, 0]
    assert np.max(np.abs(a_model - a_rk)) < 1e-6

    # decay rate AND oscillation frequency, fitted in the time domain
    k_fit, d_fit = _extract_kappa_delta(a_model, t)
    assert abs(k_fit - kappa_tot) / kappa_tot < 1e-5
    assert abs(d_fit - delta) / delta < 1e-5
    # the independent integrator recovers the same pole from its trajectory
    k_rk, d_rk = _extract_kappa_delta(a_rk, t)
    assert abs(k_rk - kappa_tot) / kappa_tot < 1e-3
    assert abs(d_rk - delta) / delta < 1e-3


def test_single_ring_step_response_matches_rk45():
    """Forced step (a0=0, u const): the spiralling transient must track an
    independent RK45 pointwise, and the settled state must equal the
    analytic steady state a_ss = B u / (kappa_tot - i delta)."""
    kappa_tot, delta = 3.0e8, 5.0e10
    # scale the input so the steady state |a_ss| = b/|kappa - i delta| ~ 1
    # (an O(1) state keeps the comparison — and scipy's atol — meaningful).
    b = math.hypot(kappa_tot, delta)
    dt, T = 5e-12, 6000                            # 30 ns, settles to ~e^-9
    model = CoupledRingLinOSS([kappa_tot], [delta], dt,
                              B=torch.tensor([[b]], dtype=torch.complex128))
    u = torch.ones(T, 1, dtype=torch.float64)
    states, _ = model(u)                           # a0 = 0
    a_model = states[:, 0].detach().numpy()
    t = np.arange(T + 1) * dt

    M = [[-kappa_tot + 1j * delta]]
    a_rk = _rk45(M, [[b]], [1.0], [0.0 + 0j], t,
                 max_step=0.05 * 2 * math.pi / delta)[:, 0]
    assert np.max(np.abs(a_model - a_rk)) < 1e-6   # O(1) state, abs == rel

    a_ss = b / (kappa_tot - 1j * delta)            # |a_ss| ~ 1
    assert abs(a_model[-1] - a_ss) / abs(a_ss) < 2e-3


# ---------------------------------------------------------------------- #
#  (ii) two-ring hybridization: beat frequency == Im(eig(M)) splitting
# ---------------------------------------------------------------------- #

def test_two_ring_beat_frequency_matches_eig_splitting():
    """Two degenerate rings coupled by mu hybridize into supermodes split
    in Im by 2*mu. Driving ring 0 only, energy sloshes 0<->1 at the beat
    frequency; the measured population-beat angular frequency must equal the
    Im(eig(M)) splitting, and the rollout must match an independent RK45."""
    kappa_tot, delta, mu = 1.0e6, 0.0, 3.0e9       # high-Q (slow decay)
    dt, T = 5e-12, 8192                            # ~16 beats, flat envelope
    mu_mat = torch.tensor([[0.0, mu], [mu, 0.0]], dtype=torch.float64)
    model = CoupledRingLinOSS([kappa_tot, kappa_tot], [delta, delta], dt,
                              mu=mu_mat)
    u = torch.zeros(T, 1, dtype=torch.float64)
    a0 = torch.tensor([1.0 + 0j, 0.0 + 0j], dtype=torch.complex128)
    states, _ = model(u, a0=a0)
    a = states.detach().numpy()                    # (T+1, 2)
    t = np.arange(T + 1) * dt

    # prediction: Im(eig(M)) splitting
    M = [[-kappa_tot + 1j * delta, 1j * mu],
         [1j * mu, -kappa_tot + 1j * delta]]
    w = np.linalg.eigvals(np.asarray(M, dtype=np.complex128))
    S = abs(w[0].imag - w[1].imag)                 # = 2 mu
    assert abs(S - 2 * mu) / (2 * mu) < 1e-9       # splitting sanity

    # independent RK45 — same sloshing
    a_rk = _rk45(M, np.zeros((2, 1)), [0.0], [1.0 + 0j, 0.0], t,
                 max_step=0.02 * math.pi / mu)
    assert np.max(np.abs(a - a_rk)) < 1e-6

    # energy fully transfers ring0 -> ring1 (a genuine beat, not numerics)
    p0 = np.abs(a[:, 0]) ** 2
    p1 = np.abs(a[:, 1]) ** 2
    assert p1.max() > 0.95 and p0.min() < 0.05

    # measured population-beat angular frequency == eig splitting
    env = np.exp(-2.0 * kappa_tot * t)             # known (slow) envelope
    beat = _dominant_angular_freq(p0 / env, dt)
    assert abs(beat - S) / S < 0.02


def test_two_ring_no_coupling_no_beat():
    """Contrast: mu=0 -> degenerate, uncoupled rings. Ring 1 is never
    populated, ring 0 decays monotonically (no beat), and the Im(eig(M))
    splitting is zero. Confirms the beat above is caused by the coupling."""
    kappa_tot, delta = 1.0e6, 0.0
    dt, T = 5e-12, 4096
    model = CoupledRingLinOSS([kappa_tot, kappa_tot], [delta, delta], dt)
    a0 = torch.tensor([1.0 + 0j, 0.0 + 0j], dtype=torch.complex128)
    states, _ = model(torch.zeros(T, 1, dtype=torch.float64), a0=a0)
    a = states.detach().numpy()
    assert np.max(np.abs(a[:, 1])) < 1e-12         # ring 1 stays empty
    p0 = np.abs(a[:, 0]) ** 2
    assert np.all(np.diff(p0) <= 1e-15)            # monotone decay, no beat
    w = np.linalg.eigvals(np.diag([-kappa_tot + 1j * delta] * 2))
    assert abs(w[0].imag - w[1].imag) < 1e-9       # zero Im-splitting
