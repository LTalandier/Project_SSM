# S0.1 mapping notes — oscillator ↔ SiN ring (proposal §3, §4)

**Status:** Executor technical reference for the Supervisor's formal mapping write-up + white-space
wording (role boundary: the Supervisor writes the paper; this is the verified model + derivation it
cites). Code: `photonic_ssm.dynamics.{single_ring, coupled_rings, pole_region}`. Gate tests:
`tests/test_single_ring_cmt.py`, `tests/test_coupled_rings.py`.

## 1. The dynamical model + conventions

Single ring, temporal coupled-mode theory (Haus energy-amplitude convention; `|a|²` = stored energy):

    da/dt = (i*Delta - kappa_tot) a + sqrt(2*kappa_ext1) s_in(t)        (all-pass: through port only)
    s_through = s_in - sqrt(2*kappa_ext1) a ;   s_drop = sqrt(2*kappa_ext2) a   (add-drop)

- `kappa_i = omega0/(2 Qi)`, `kappa_ext = omega0/(2 Qext)` — **amplitude** decay rates [rad/s]; energy
  decays at `2*kappa`; power-FWHM linewidth `= 2*kappa_tot` [rad/s] `= f0/Q` [Hz].
- `kappa_tot = kappa_i + kappa_ext1 (+ kappa_ext2) - g_amp` (optional net gain `g_amp`, §7).
- **Convention note for the write-up:** the proposal's schematic `sqrt(kappa_ext) s_in` and the Haus
  `sqrt(2*kappa_ext) s_in` are the same model — the factor of 2 is whether `kappa_ext` names the
  amplitude rate (Haus, ours) or the energy rate. We use the amplitude rate so `kappa_tot = Σ kappa`
  adds cleanly; the `sqrt(2·)` form is the one that makes the lossless ring **energy-conserving**
  (verified: lossless all-pass `|t|=1`; lossless symmetric add-drop `|t_through|²+|t_drop|²=1` to 1e-16;
  on-resonance drop `=1`).

## 2. Pole ↔ eigenvalue identity (the §3 table, formalized)

The single Laplace pole `s = -kappa_tot + i*Delta` is identified with the SSM/oscillator eigenvalue
`a_i = -exp(alpha_i) + i*beta_i`:

    exp(alpha_i) = kappa_tot   (damping magnitude = -Re pole),
    beta_i       = Delta       (oscillation frequency = Im pole).

Storing `alpha_i = log(kappa_tot)` (code: `log_kappa_tot`) enforces the dissipative `-exp(alpha)` real
part and `kappa_tot > 0` by construction — the proposal's exact parametrization. The discrete-time pole
is `z = exp(s*dt)`, `|z| = exp(-kappa_tot*dt)` (the per-step memory retention; `|z|→1` = long memory).

## 3. CW-limit gate (S0.1 gate — PASSED)

**Pre-registered criterion:** the dynamical model's CW (steady-state) limit recovers the S0.0 salvaged
static references (`single_bus_through`, `add_drop_through`, `add_drop_drop`) with a max relative
magnitude error that scales **O(1/finesse)**, `< 1%` at finesse ≥ 1000 over a ±5-linewidth window.

**Result:** single-bus error `4.5×10⁻⁴` at finesse 1048, `4.4×10⁻⁵` at finesse 10473 (exact 10×-per-10×
`O(1/F)` convergence); add-drop through/drop `3.4×10⁻⁴ → 3.4×10⁻⁵`. The CMT through-port equals **minus**
the salvaged single-bus form — the `-1` phase convention already documented in `static_rings.py`
(`add_drop_through == -single_bus_through` at `κ₂→0`). The SiN registry rings have finesse ≈ 1000
(Qi=2×10⁶) to ≈ 15000 (Qi=3×10⁷) at FSR=100 GHz, so the CMT pole is an excellent model there.

**Coupled-ring gate:** uncoupled system poles `= -kappa_tot + i*delta` to <1e-3; discrete `|z| =
exp(-kappa_tot*dt)` to <1e-9; ZOH (van Loan matrix-exp) discretization is **exact** for piecewise-
constant input (the discrete poles are `exp(λ*dt)` to machine precision — no integration error).

## 4. Realizable pole region (proposal §4)

- **Stability is free.** Passive rings give `kappa_tot > 0` ⇒ `|z| < 1`. LinOSS is valid for any
  nonnegative-diagonal (dissipative) `A`, so the ring lattice is in-regime.
- **Memory is loss-limited.** Min damping = intrinsic loss: `kappa_tot ≥ kappa_i = omega0/(2 Qi)`. Max
  passive amplitude memory time `= 1/kappa_i = 2 Qi/omega0`; photon lifetime `= Qi/omega0`. Across the
  registry: **1.65 ns / 329 round trips** (Qi=2×10⁶) → **24.7 ns / 4937 round trips** (Qi=3×10⁷) — a 15×
  memory gain from the foundry to the class-leading corner. Gain (§7) extends it: `kappa_tot → 0`
  (lasing threshold) pushes `|z| → 1` (figure `pole_region_memory.png`).
- **`beta` is FSR-bounded.** Detuning aliases at one free spectral range: `|beta_j| ≤ π·FSR` (rad/s),
  i.e. `|beta_j*dt| ≤ π` (half a round-trip phase per step) with `dt = 1/FSR`. The reachable imaginary
  axis is one FSR wide.
- **Poles are *placed* by drift-stable thermo-optic trim** (B1). SiN's low dn/dT makes this a tractable
  post-fab calibration (Stage-1 gate ii).
- **Coupling hybridizes poles, conserving total damping.** Inter-ring `i*Omega` (Omega real-symmetric)
  is anti-Hermitian ⇒ energy-conserving; it moves the imaginary parts (photonic-molecule supermodes)
  while `Σ Re(poles) = -Σ kappa_tot` is invariant (test `test_coupling_hybridizes_poles_but_preserves_trace`).

## 4b. Mapping subtlety → `decisions_needed.md` (feeds PR-2 architecture)

**One optical ring = one *complex* pole** (the optical envelope is genuinely complex — it carries a
carrier). This is the **diagonal complex-pole SSM** of proposal §1.1, `H(s)=Σ c_j b_j/(s-λ_j)+D` (the
S4D/DSS form), which the code realizes directly. A **real-valued** LinOSS / D-LinOSS oscillator block,
as usually implemented in ML, is a real 2nd-order system = a **conjugate pole pair** `{-γ ± iω}`. So the
ring bank maps *most cleanly* onto a **complex-diagonal** SSM (one ring ↔ one complex pole), and the
"oscillatory LinOSS" structure is recovered either by (a) treating the complex-diagonal SSM as the
target (cleanest for optics), or (b) pairing rings to synthesize real conjugate-pair blocks. This is not
a defect — §1.1 already uses the diagonal-pole framing — but it is a **deliberate choice the Supervisor
should pin at PR-2** (what layer is simulated): *complex-diagonal SSM* vs *real-LinOSS-with-paired-rings*.
The realizable-pole-region model and the bake-off substrate support either. Flagged to
`decisions_needed.md`.

## 5. What this delivers downstream

- **PR-2** (S0.2 task sizing): the memory bound (329 → 4937 round trips passive) sizes the bake-off
  task's required sequence/memory length; the B1 actuation map fixes the trainable partition; the §4b
  choice fixes the simulated architecture.
- **PR-4** (S0.3 substrate): the F13.1-reconciled `(α, Qi)` registry + the B3 κ_ext trade + the B2
  splitting-knob recommendation.
- The white-space wording (Supervisor): B1 says the in-situ-trainable recurrence parameters are
  `{delta_j (heaters), kappa_tot,j (couplers/gain), mu_jk (ring–ring)}` — the pole positions and
  inter-ring couplings that *define* the recurrence.
