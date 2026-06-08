# B1 — Trainable-parameter set + actuation map (S0.1 deliverable 4)

**Status:** Executor physics input for **PR-2** (bake-off trainable-parameter partition +
in-situ-trainable physical-parameter set) and the **white-space sentence** wording. The Supervisor
writes the claim wording from this; Lucas freezes PR-2 at S0.2.

The white-space claim is that *the recurrent parameters themselves — the pole positions and inter-ring
couplings that **define** the recurrence — are updated on the physical device*. This memo enumerates
exactly which physical knobs those are, the actuator for each, and the device-complexity cost. The
recurrent parameters live in the state matrix `M = diag(-kappa_tot_j + i*delta_j) + i*Omega` of
`photonic_ssm.dynamics.CoupledRingLinOSS`; B/C (residues) are the injection/readout mesh.

## The map

| SSM / pole quantity | Physical parameter | Actuator | In-situ trainable? | Device-complexity cost | Defines the recurrence? |
|---|---|---|---|---|---|
| **detuning `beta_j` = Im(pole)** (oscillation frequency) | ring resonance offset `delta_j` | **thermo-optic heater** (trench-isolated TiN), per ring | **Yes — primary** | Low. 1 heater + DAC channel/ring. SiN's low dn/dT → drift-stable, SPSA-friendly (Stage-1 gate ii). | **Yes** |
| **damping `exp(alpha_j)` = -Re(pole)** = `kappa_tot,j` | bus–ring coupling `kappa_ext,j` | **tunable coupler** (MZI-assisted directional coupler / tunable bus gap) | **Yes** | Medium. Extra MZI + 1–2 heaters/ring; also sets the κ_ext readout trade (B3). | **Yes** |
| same, alternative/additive | per-ring **net gain** `g_j` | Er:SiN or III-V SOA pump current | Yes (Stage 2) | High. Needs in-loop gain (Stage-2 fab); ASE/NF cost (debt #3). The only way to push `kappa_tot → 0` (memory past the passive loss floor). | **Yes** |
| **inter-ring coupling `mu_jk` / `Omega`** (pole hybridization; off-diagonal recurrence) | ring–ring coupling | **direct photonic-molecule** tunable coupler (compact, fixed topology) **or bus-mediated MZI mesh** (reconfigurable, more area/loss) | **Yes** | Medium–High. Direct = 1 tunable coupler/edge; bus-mediated = full MZI mesh. Topology is a design choice (see flag below). | **Yes — load-bearing** |
| **residues `c_j b_j`** / B, C (input/output, skip D) | injection + readout couplings, MZI mesh phases | thermo-optic MZI mesh | Optional (reservoir baseline trains only these) | Medium (shared readout mesh). | **No** — these are read-in/out, not the recurrence. Training *only* these = the reservoir baseline (§5.3). |
| step `Delta` (= round-trip time τ) | path length / delay | fixed by layout (not a live knob) | No | — | Sets the sampling, not trainable. |

## What "training the recurrence" must include (for the claim to hold)

The load-bearing partition for PR-2: a method earns the white-space claim only if it updates the
**pole-defining** parameters — at minimum the `delta_j` (heater detunings) **and** the damping/coupling
(`kappa_ext,j` and/or `g_j`) **and** the inter-ring `mu_jk`. Training residues (B/C) alone is the
reservoir baseline and explicitly does **not** count (pre-empts the Bueno/Brunner readout-RL line — the
load-bearing distinction of debt #1). Every bake-off method must train the **same** partition (PR-6
fairness); B1 says that partition is `{delta_j, kappa_tot,j (via coupling and/or gain), mu_jk}`.

## Minimal vs full demonstrator

- **Stage-1 minimal (no gain):** trainable `{delta_j (heaters), kappa_ext,j (tunable couplers), mu_jk
  (tunable ring–ring couplers)}`. All thermo-optic — drift-stable, SPSA/PAT-friendly. This **already
  suffices** for the white-space claim (pole real part is set by coupling; imaginary by detuning;
  off-diagonal by ring–ring coupling). No Stage-2 gain required for the headline.
- **Stage-2 (gain-rich):** add per-ring `g_j` to push `kappa_tot → 0` (memory past the passive floor,
  proposal §7) — higher complexity + ASE/NF cost.

## Flag → `decisions_needed.md` (PR-2 architecture)

**Inter-ring coupling topology is a real design fork** the Supervisor must pin at PR-2: *direct
photonic-molecule* coupling (compact, but the topology/sparsity of `Omega` is fixed at fab — only the
coupling *strengths* on existing edges are trainable) vs *bus-mediated MZI mesh* (any `Omega`, fully
reconfigurable, but more loss/area and it re-introduces mesh calibration). The simulated bake-off
architecture (PR-2) should commit to one; the realizable-pole-region model supports either (the `mu`
parameter is a dense symmetric matrix; a fixed sparsity mask encodes the direct-coupling topology).
See also the **diagonal-complex-SSM vs real-LinOSS-conjugate-pair** clarification (mapping_notes.md §4),
which also feeds the PR-2 architecture choice.
