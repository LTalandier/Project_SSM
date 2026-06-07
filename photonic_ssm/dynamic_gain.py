# salvaged from pnn-multilayer @ e2eec80 : channels/dynamic_soa.py
# Adaptations for Project_SSM (task S0.0, deliverable 2):
#   - module docstring re-pointed at the S0.3 in-loop-gain role and the
#     architecture-constraint boundary (which classes may appear inside
#     the substrate's training path);
#   - dropped `instantaneous_soa_fieldmodel` (redundant with
#     `gain.soa_activation`).
# Class/function bodies are otherwise unchanged (incl. class names, for
# diffability against the source). NO ASE inside the rollout yet — the
# per-round-trip ASE accumulation is new S0.3 physics, not salvage.
"""Rate-equation (carrier-dynamics) gain for the S0.3 substrate.

Standard single-pass rate equation (Agrawal, *Applications of Nonlinear
Fiber Optics*, §11.3; also *Fiber-Optic Communication Systems* §6.5)
in integrated log-gain form:

    dh(t)/dt = (h0 - h(t)) / tau_c  -  (exp(h(t)) - 1) * P_in(t) / E_sat

    E_out(t) = exp(h(t) / 2) * E_in(t)

where
    h(t)  = integrated log-gain (power gain = exp(h))
    h0    = ln(G0) with G0 the unsaturated power gain
    tau_c = carrier lifetime
    P_in  = instantaneous input power
    E_sat = saturation energy  =  P_sat * tau_c
    P_sat = saturation power

The same parametric form covers the S0.3 gain candidates: III-V/SOA
(tau_c ~ 100s of ps) and erbium gain (tau_c ~ ms — quasi-static at
round-trip timescales). The memoryless tier is `gain.soa_activation`.

ARCHITECTURE-CONSTRAINT BOUNDARY (3a) — read before composing:

  * `TrainingAwareDynamicSOAPerMode` is the ONLY class here that may sit
    inside the substrate's training path: it keeps a live autograd graph
    through the Euler rollout (gradient-checkpointed, memory
    O(n_chunks)). This is the pattern ALL new substrate dynamics copy.

  * `DynamicSOA` / `DynamicSOAPerMode` are forward-only (`no_grad`)
    EVAL/SCREENING references. Correct for what they are; FATAL if
    placed inside the recurrence under BPTT/PAT-twin training — they
    silently cut d(loss)/d(state). Do not "fix" them; use the
    training-aware class.

Approximations (inherited; acceptable for Stage 0 screening tiers):
    - Scalar carrier density (no spatial integration along the device)
    - alpha_H configurable (0 = chirp-free) on the per-mode classes
    - No ASE inside the rollout (S0.3 adds per-round-trip ASE)
    - Constant DC pump; steady-state initialization from first symbol
"""

from __future__ import annotations

import math

import torch


class DynamicSOA:
    """Forward-only rate-equation gain (screening/eval reference).

    NOT for use inside the substrate training path — see module
    docstring (constraint 3a)."""

    def __init__(
        self,
        tau_c: float = 200e-12,
        G0_dB: float = 20.0,
        P_sat_mW: float = 10.0,
        L_soa: float = 1e-3,
        substeps_per_symbol: int = 10,
    ):
        """
        Args:
            tau_c: carrier lifetime in seconds (default 200 ps — typical
                InGaAsP bulk SOA).
            G0_dB: small-signal (unsaturated) *power* gain in dB.
            P_sat_mW: saturation power in mW. Defines E_sat = P_sat * tau_c.
            L_soa: device length in m (recorded for metadata only; the
                scalar rate-equation form already integrates along the
                device).
            substeps_per_symbol: forward Euler substeps per symbol. The
                actual step count used is
                max(substeps_per_symbol, ceil(10 * T_sym / tau_c))
                to keep dt < tau_c / 10 for stability.
        """
        self.tau_c = float(tau_c)
        self.G0_dB = float(G0_dB)
        self.G0_power = 10.0 ** (G0_dB / 10.0)      # unsaturated power gain
        self.h0 = math.log(self.G0_power)           # log power gain
        self.P_sat_W = float(P_sat_mW) * 1e-3       # saturation power (W)
        self.E_sat = self.P_sat_W * self.tau_c      # saturation energy (J)
        self.L_soa = float(L_soa)
        self.substeps_request = int(substeps_per_symbol)
        # QA counters — useful for asserting the torch.clamp safety rail
        # never actually fires during production integration.
        self.h_clamp_hit_count = 0

    # ------------------------------------------------------------------ #
    #  Utilities
    # ------------------------------------------------------------------ #

    def steady_state_power_gain(self, P_in_W: float) -> float:
        """Analytical steady-state power gain for CW input.

        Solves 0 = (h0 - h)/tau_c - (exp(h) - 1) * P_in / E_sat, i.e.
            h0 - h = (tau_c * P_in / E_sat) * (exp(h) - 1)
                   = (P_in / P_sat) * (exp(h) - 1)
        via Newton iteration. Returns G = exp(h).

        For P_in << P_sat this reproduces Agrawal Eq. 11.14:
            G(P_in) ~ G0 / (1 + (G0 - 1) * P_in / (G0 * P_sat))
        In the limit G0 >> 1 this is G0 / (1 + P_in / P_sat).
        """
        K = P_in_W / self.P_sat_W
        if K == 0.0:
            return self.G0_power
        # Initial guess from first-order expansion.
        h = self.h0 / (1.0 + K * math.exp(self.h0 / 2.0))
        for _ in range(200):
            f = self.h0 - h - K * (math.exp(h) - 1.0)
            fp = -1.0 - K * math.exp(h)
            dh = -f / fp
            h += dh
            if abs(dh) < 1e-12:
                break
        return math.exp(h)

    def _initial_h(self, P_in: torch.Tensor) -> torch.Tensor:
        """Vectorized steady-state h per mode from the first-symbol power."""
        P_cpu = P_in.detach().to(torch.float64).cpu()
        out = torch.empty_like(P_cpu)
        for i in range(P_cpu.numel()):
            G = self.steady_state_power_gain(P_cpu.view(-1)[i].item())
            out.view(-1)[i] = math.log(G)
        return out

    # ------------------------------------------------------------------ #
    #  Forward pass
    # ------------------------------------------------------------------ #

    @torch.no_grad()
    def apply(self, z: torch.Tensor, dt: float,
              warmup_symbols: int = 0) -> torch.Tensor:
        """Apply dynamic gain to a symbol sequence (forward-only).

        Args:
            z: [batch, N] complex envelope in field units where |z|^2 is
                input *power* in Watts. (The caller is responsible for the
                normalization; calibrate P_sat_mW accordingly.)
            dt: step period in seconds.
            warmup_symbols: int
                Number of leading symbols passed through the ODE but NOT
                written to the returned tensor. Allows the state h(t)
                to settle away from the steady-state initialization before
                output measurement begins. Recommended:
                    ceil(10 * tau_c / T_sym)
                For `warmup_symbols > 0` the first `warmup_symbols` rows of
                z are consumed to advance h, and the returned tensor has
                shape [n_syms - warmup_symbols, N].

        Returns:
            complex tensor with per-symbol field gain applied. Shape
            [n_syms - warmup_symbols, N].
        """
        if z.dim() != 2:
            raise ValueError(f"expected [batch, N] input, got shape {tuple(z.shape)}")
        if warmup_symbols < 0:
            raise ValueError(f"warmup_symbols must be >= 0, got {warmup_symbols}")

        n_syms, N = z.shape
        if warmup_symbols >= n_syms:
            raise ValueError(
                f"warmup_symbols={warmup_symbols} must be < n_syms={n_syms}")

        dtype_in = z.dtype
        # Use double precision internally for stable Euler integration.
        z64 = z.to(torch.complex128)

        # Step count: honor the request but enforce dt_sub < tau_c / 10.
        substeps = max(self.substeps_request,
                       int(math.ceil(10.0 * dt / self.tau_c)))
        dt_sub = dt / substeps

        # Initialize h at steady state for the first symbol.
        P0 = (z64[0].real ** 2 + z64[0].imag ** 2)
        h = self._initial_h(P0).to(torch.float64)

        out = torch.empty((n_syms - warmup_symbols, N),
                          dtype=torch.complex128)

        h_max_allowed = self.h0 * 1.1
        for k in range(n_syms):
            P_in = (z64[k].real ** 2 + z64[k].imag ** 2)  # [N], W
            for _ in range(substeps):
                G_pow = torch.exp(h)
                dh_dt = ((self.h0 - h) / self.tau_c
                         - (G_pow - 1.0) * P_in / self.E_sat)
                h = h + dt_sub * dh_dt
                # Guard against numerical blowup; physical h in [0, h0].
                clipped_low = (h < 0.0).sum().item()
                clipped_high = (h > h_max_allowed).sum().item()
                if clipped_low or clipped_high:
                    self.h_clamp_hit_count += int(clipped_low + clipped_high)
                h = torch.clamp(h, min=0.0, max=h_max_allowed)

            if k >= warmup_symbols:
                field_gain = torch.exp(h / 2.0)
                out[k - warmup_symbols] = field_gain.to(torch.complex128) * z64[k]

        return out.to(dtype_in)


# ---------------------------------------------------------------------- #
#  Per-mode variant (forward-only eval reference)
# ---------------------------------------------------------------------- #

class DynamicSOAPerMode:
    """Per-mode rate-equation gain with heterogeneous (G_field, alpha).

    Forward-only EVAL reference — see module docstring (constraint 3a).

    Integrates h(t) independently per mode with forward-Euler substeps.
    Used to evaluate a model trained with the instantaneous gain under
    dynamic conditions *without* reparameterizing the trained weights:

        instantaneous model per mode i:
            f(z_i) = G_field_i * z_i / (1 + alpha_i * |z_i|^2)
            power gain at |z_i|^2 = 0:  G_field_i^2
            saturation knee:            |z_i|^2 = 1 / alpha_i

    For each mode i the rate-equation gain is built with
        G0_power_i = G_field_i^2
        P_sat_i    = 1 / alpha_i      (same normalized "power" units)
    so that in the tau_c -> 0 limit the per-mode static gain curve
    matches the rate equation's own steady state. Only tau_c > 0
    introduces memory.
    """

    def __init__(self, G_field: torch.Tensor, alpha: torch.Tensor,
                 tau_c: float = 200e-12, substeps_per_symbol: int = 10,
                 alpha_H: float = 0.0):
        # Allow alpha == 0 (unsaturated) by clamping to a tiny epsilon.
        alpha = torch.clamp(alpha.to(torch.float64), min=1e-12)
        G_field = G_field.to(torch.float64)
        self.G0_power = G_field ** 2                       # [N]
        self.h0 = torch.log(self.G0_power)                 # [N]
        self.P_sat = 1.0 / alpha                           # [N]
        self.tau_c = float(tau_c)
        self.E_sat = self.P_sat * self.tau_c               # [N]
        self.substeps_request = int(substeps_per_symbol)
        # Linewidth-enhancement factor (Henry's alpha). alpha_H > 0
        # introduces self-phase modulation coupled to gain change:
        #     phi_chirp(t) = -(alpha_H/2) * (h(t) - h(0))
        # applied as phase on the output field. alpha_H = 0 recovers the
        # chirp-free baseline.
        self.alpha_H = float(alpha_H)
        self.h_clamp_hit_count = 0

    def _steady_state_h(self, P_in: torch.Tensor) -> torch.Tensor:
        """Per-mode Newton solve of h0 - h = (P_in/P_sat) (exp(h) - 1)."""
        K = P_in / self.P_sat                               # [N]
        h = self.h0 / (1.0 + K * torch.exp(self.h0 / 2.0))
        for _ in range(200):
            f = self.h0 - h - K * (torch.exp(h) - 1.0)
            fp = -1.0 - K * torch.exp(h)
            dh = -f / fp
            h = h + dh
            if torch.max(torch.abs(dh)).item() < 1e-12:
                break
        return h

    @torch.no_grad()
    def apply(self, z: torch.Tensor, dt: float,
              warmup_symbols: int = 0) -> torch.Tensor:
        """Dynamic gain on [batch, N]. Uses per-mode (G0, P_sat).

        Same semantics as DynamicSOA.apply (including warmup_symbols).
        Returns [batch - warmup_symbols, N].
        """
        if z.dim() != 2:
            raise ValueError(f"expected [batch, N], got {tuple(z.shape)}")
        if warmup_symbols < 0:
            raise ValueError(f"warmup_symbols must be >= 0, got {warmup_symbols}")

        n_syms, N = z.shape
        if N != self.G0_power.numel():
            raise ValueError(
                f"mode count mismatch: z has {N}, params have "
                f"{self.G0_power.numel()}")
        if warmup_symbols >= n_syms:
            raise ValueError(
                f"warmup_symbols={warmup_symbols} must be < n_syms={n_syms}")

        z64 = z.to(torch.complex128)
        substeps = max(self.substeps_request,
                       int(math.ceil(10.0 * dt / self.tau_c)))
        dt_sub = dt / substeps

        P0 = z64[0].real ** 2 + z64[0].imag ** 2            # [N]
        h = self._steady_state_h(P0)
        # Reference gain for alpha_H phase chirp — frozen at the
        # steady-state initialization so phi_chirp = -(alpha_H/2)*(h(t) - h0_ref).
        h0_ref = h.clone()

        out = torch.empty((n_syms - warmup_symbols, N),
                          dtype=torch.complex128)
        h_max_allowed = self.h0 * 1.1
        h_min_allowed = torch.zeros_like(h)

        use_chirp = self.alpha_H != 0.0
        for k in range(n_syms):
            P_in = z64[k].real ** 2 + z64[k].imag ** 2      # [N]
            for _ in range(substeps):
                G_pow = torch.exp(h)
                dh_dt = ((self.h0 - h) / self.tau_c
                         - (G_pow - 1.0) * P_in / self.E_sat)
                h = h + dt_sub * dh_dt
                clipped_low = (h < h_min_allowed).sum().item()
                clipped_high = (h > h_max_allowed).sum().item()
                if clipped_low or clipped_high:
                    self.h_clamp_hit_count += int(clipped_low + clipped_high)
                h = torch.clamp(h, min=h_min_allowed, max=h_max_allowed)

            if k >= warmup_symbols:
                field_gain = torch.exp(h / 2.0)
                if use_chirp:
                    phi = -(self.alpha_H / 2.0) * (h - h0_ref)
                    phase = torch.cos(phi) + 1j * torch.sin(phi)
                    out[k - warmup_symbols] = (
                        field_gain.to(torch.complex128) * phase * z64[k])
                else:
                    out[k - warmup_symbols] = (
                        field_gain.to(torch.complex128) * z64[k])

        return out.to(z.dtype)


def build_matched_dynamic_soa_per_mode(
    G_field: torch.Tensor, alpha: torch.Tensor,
    tau_c: float = 200e-12, substeps_per_symbol: int = 10,
    alpha_H: float = 0.0,
) -> DynamicSOAPerMode:
    """Factory: build DynamicSOAPerMode from trained (G_field, alpha)."""
    return DynamicSOAPerMode(
        G_field=G_field.detach().cpu().to(torch.float64),
        alpha=alpha.detach().cpu().to(torch.float64),
        tau_c=tau_c,
        substeps_per_symbol=substeps_per_symbol,
        alpha_H=alpha_H,
    )


# ---------------------------------------------------------------------- #
#  Training-aware per-mode rate-equation gain (autograd-enabled)
#  >>> THE pattern for all S0.1+ substrate dynamics (constraint 3a) <<<
# ---------------------------------------------------------------------- #

def _train_soa_chunk(z_chunk: torch.Tensor,
                     h_init: torch.Tensor,
                     h0_ref: torch.Tensor,
                     G_field: torch.Tensor, alpha: torch.Tensor,
                     tau_c: float, dt_sub: float, substeps: int,
                     alpha_H: float,
                     emit: bool) -> tuple:
    """Forward one chunk of symbols through the per-mode rate equation.

    This is the unit that gets wrapped in torch.utils.checkpoint.checkpoint
    so only inputs (z_chunk, h_init, h0_ref, G_field, alpha) are saved for
    backward; intermediate per-substep state is re-materialized.

    Args:
        z_chunk:  [n_chunk, N] complex (autograd-tracked input)
        h_init:   [N] float64 — integrated log-gain at chunk start
        h0_ref:   [N] float64 — reference h for alpha_H chirp
        G_field:  [N] float64 — per-mode unsaturated field gain (Parameter)
        alpha:    [N] float64 — per-mode saturation coefficient (Parameter)
        tau_c:    scalar carrier lifetime
        dt_sub:   sub-step size (< tau_c/10)
        substeps: sub-steps per symbol
        alpha_H:  linewidth-enhancement factor (0 = chirp-free)
        emit:     True -> produce out tensor; False -> only advance state
                  (for warmup symbols that should not contribute to loss).

    Returns:
        out_chunk: [n_chunk or 0, N] complex — field-gain-applied outputs
                   (empty if emit=False)
        h_final:   [N] float64 — integrated log-gain at chunk end
    """
    # Rebuild per-mode constants from (G, alpha) — Parameters are float
    # tensors so we promote to float64 here for numerical stability.
    G64 = G_field.to(torch.float64)
    a64 = torch.clamp(alpha.to(torch.float64), min=1e-12)
    G0_power = G64 ** 2                     # [N]
    h0 = torch.log(G0_power)                # [N]
    P_sat = 1.0 / a64                       # [N]
    E_sat = P_sat * tau_c                   # [N]

    n_chunk = z_chunk.shape[0]
    h = h_init  # float64

    h_max_allowed = h0 * 1.1
    use_chirp = alpha_H != 0.0

    z64 = z_chunk.to(torch.complex128)
    outs = []
    for k in range(n_chunk):
        P_in = z64[k].real ** 2 + z64[k].imag ** 2   # [N] float64
        for _ in range(substeps):
            G_pow = torch.exp(h)
            dh_dt = ((h0 - h) / tau_c
                     - (G_pow - 1.0) * P_in / E_sat)
            h = h + dt_sub * dh_dt
            # Soft clamp using torch.clamp (differentiable with zero grad in
            # the clipped regions). In practice the Euler step is stable for
            # dt_sub <= tau_c/10 and |h| well-bounded; clamp is a safety rail.
            h = torch.clamp(h, min=torch.zeros_like(h), max=h_max_allowed)

        if emit:
            field_gain = torch.exp(h / 2.0)
            if use_chirp:
                phi = -(alpha_H / 2.0) * (h - h0_ref)
                phase = torch.cos(phi) + 1j * torch.sin(phi)
                outs.append(field_gain.to(torch.complex128) * phase * z64[k])
            else:
                outs.append(field_gain.to(torch.complex128) * z64[k])

    if emit and outs:
        out_chunk = torch.stack(outs, dim=0)
    else:
        # Empty but correctly-shaped tensor so cat() downstream works.
        out_chunk = torch.empty((0, z_chunk.shape[1]), dtype=torch.complex128,
                                device=z_chunk.device)
    return out_chunk, h


class TrainingAwareDynamicSOAPerMode(torch.nn.Module):
    """Autograd-enabled per-mode rate-equation gain for training.

    Wraps the same rate equation as :class:`DynamicSOAPerMode` but keeps a
    live autograd graph through the per-symbol sub-step Euler integration,
    so the trainable (G_field, alpha) parameters — and the optical input
    trajectory — receive gradients from a downstream loss. This is the
    constraint-(3a) reference pattern for the S0.3 substrate: gradients
    flow through the *state*, with memory bounded by checkpointing.

    Gradient checkpointing breaks the [n_syms, N] roll-out into K chunks;
    inside each chunk, per-symbol and per-substep Python loops run with
    autograd; across chunks, the intermediate state (h) and output tensor
    are saved / re-materialized on backward. This bounds activation memory
    to O(n_chunks), not O(n_syms * n_substeps).

    Usage (inside a training step):
        dyn = TrainingAwareDynamicSOAPerMode(tau_c=200e-12, alpha_H=0.0,
                                             chunk_size=32)
        state_nl = dyn(state, G_field, alpha, dt,
                       warmup_symbols=W)
    """

    def __init__(self,
                 tau_c: float = 200e-12,
                 substeps_per_symbol: int = 10,
                 alpha_H: float = 0.0,
                 chunk_size: int = 32,
                 use_checkpoint: bool = True):
        """
        Args:
            tau_c:                carrier lifetime (s)
            substeps_per_symbol:  target sub-steps per symbol. Will be
                                  raised if dt > tau_c/10 for stability.
            alpha_H:              linewidth-enhancement factor (0 = chirp-free)
            chunk_size:           symbols per gradient-checkpoint chunk.
                                  Memory ~ (n_syms / chunk_size); compute
                                  cost ~ 2x (re-materialized in backward).
            use_checkpoint:       when False, disable checkpointing (for
                                  debugging/smoke-test memory profiles).
        """
        super().__init__()
        self.tau_c = float(tau_c)
        self.substeps_request = int(substeps_per_symbol)
        self.alpha_H = float(alpha_H)
        self.chunk_size = int(chunk_size)
        self.use_checkpoint = bool(use_checkpoint)

    def _initial_h_steady(self, P_in: torch.Tensor,
                          G_field: torch.Tensor,
                          alpha: torch.Tensor) -> torch.Tensor:
        """Per-mode Newton solve of h0 - h = (P_in/P_sat)(exp(h) - 1).

        Returns float64 [N] tensor. Runs under no_grad — the steady state
        is an initialization and does not need to contribute gradient paths
        (matches the eval-only path's semantics).
        """
        with torch.no_grad():
            G64 = G_field.detach().to(torch.float64)
            a64 = torch.clamp(alpha.detach().to(torch.float64), min=1e-12)
            h0 = torch.log(G64 ** 2)
            P_sat = 1.0 / a64
            K = P_in.detach().to(torch.float64) / P_sat
            h = h0 / (1.0 + K * torch.exp(h0 / 2.0))
            for _ in range(200):
                f = h0 - h - K * (torch.exp(h) - 1.0)
                fp = -1.0 - K * torch.exp(h)
                dh = -f / fp
                h = h + dh
                if torch.max(torch.abs(dh)).item() < 1e-12:
                    break
            return h

    def forward(self,
                z: torch.Tensor,
                G_field: torch.Tensor,
                alpha: torch.Tensor,
                dt: float,
                warmup_symbols: int = 0) -> torch.Tensor:
        """Apply training-aware dynamic gain to a [batch, N] sequence.

        The `batch` axis is the time axis (one symbol per row). This
        matches the eval-only :class:`DynamicSOAPerMode.apply` convention.

        Args:
            z:              [n_syms, N] complex (autograd-tracked).
            G_field, alpha: [N] float tensors (typically Parameters of
                            the model owning the gain slot).
            dt:             step period (s).
            warmup_symbols: leading symbols used only to advance h;
                            output tensor has shape [n_syms - warmup, N].

        Returns:
            complex tensor [n_syms - warmup_symbols, N] in the input dtype.
        """
        if z.dim() != 2:
            raise ValueError(f"expected [batch, N], got {tuple(z.shape)}")
        if warmup_symbols < 0:
            raise ValueError(f"warmup_symbols must be >= 0, got {warmup_symbols}")
        n_syms, N = z.shape
        if warmup_symbols >= n_syms:
            raise ValueError(
                f"warmup_symbols={warmup_symbols} >= n_syms={n_syms}")

        substeps = max(self.substeps_request,
                       int(math.ceil(10.0 * dt / self.tau_c)))
        dt_sub = dt / substeps

        # Steady-state h for the first symbol (no gradient — init only).
        P0 = (z[0].real.to(torch.float64) ** 2
              + z[0].imag.to(torch.float64) ** 2)
        h = self._initial_h_steady(P0, G_field, alpha)
        h0_ref = h.clone()          # for alpha_H chirp (frozen reference)

        # Two-phase rollout:
        #   Phase A  (warmup symbols): emit=False, still integrates h
        #   Phase B  (emitted symbols): emit=True, contributes to loss
        chunk = self.chunk_size
        out_pieces = []

        cursor = 0
        emit_cursor = 0
        while cursor < n_syms:
            end = min(cursor + chunk, n_syms)
            # Split the chunk at the warmup boundary so one chunk is
            # either fully warmup (emit=False) or fully emitted (emit=True)
            # — never a partial mix.
            if cursor < warmup_symbols < end:
                end = warmup_symbols
            emit = cursor >= warmup_symbols
            z_chunk = z[cursor:end]

            if self.use_checkpoint and emit:
                # Checkpoint only emitted chunks — saves memory on the
                # path that contributes to grad. Warmup chunks run under
                # no_grad (no need to preserve history at all).
                out_chunk, h = torch.utils.checkpoint.checkpoint(
                    _train_soa_chunk,
                    z_chunk, h, h0_ref, G_field, alpha,
                    self.tau_c, dt_sub, substeps, self.alpha_H, emit,
                    use_reentrant=False)
            else:
                if emit:
                    out_chunk, h = _train_soa_chunk(
                        z_chunk, h, h0_ref, G_field, alpha,
                        self.tau_c, dt_sub, substeps, self.alpha_H, emit)
                else:
                    with torch.no_grad():
                        out_chunk, h = _train_soa_chunk(
                            z_chunk, h, h0_ref, G_field, alpha,
                            self.tau_c, dt_sub, substeps, self.alpha_H, emit)

            if emit and out_chunk.numel() > 0:
                out_pieces.append(out_chunk)
                emit_cursor += out_chunk.shape[0]
            cursor = end

        if not out_pieces:
            raise RuntimeError("no emitted symbols — check warmup_symbols")
        out = torch.cat(out_pieces, dim=0)
        return out.to(z.dtype)
