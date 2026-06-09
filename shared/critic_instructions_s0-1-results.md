# Critic Review Spec — S0.1 Results (mapping + pole region)

**Filed by:** Supervisor (Claude Opus 4.8) · **Date:** 2026-06-09 · **For:** the independent Critic session.

You are the **Critic** of the Photonic-SSM-on-SiN pipeline (read `shared/critic_instructions.md` for your
standing role). You report to **Lucas**, not the Supervisor. You have **no context** from the Supervisor's
conversation — this spec is standalone. Review the **S0.1 results** (the first new dynamical core + the
three scope-(B) deliverables), the gate, and the **two architecture decisions** the results surfaced.

## Scope
S0.1 built the dynamical temporal-CMT ring model + the coupled-ring → $N$-oscillator LinOSS forward model
(replacing the salvaged static/CW transfer), bounded the realizable pole region (§4), and delivered B1
(actuation map), B2 (backscatter bound), B3 ($\kappa_\text{ext}$ trade) + the F13.1 registry fix. The S0.1
gate is reported **PASSED**. **This review gates S0.2.** Your job: (1) is the gate genuinely passed?
(2) are the claims rigorous and the numbers defensible? (3) **independently adjudicate the two decisions**
the results raise (the complex-pole-vs-conjugate-pair mapping fork; the backscatter knob + roughness-as-
pre-registration).

## Files to read (in order)
1. `shared/results_log.md` — the **S0.1 entry** (top).
2. `photonic-ssm-proposal-v0_5.md` — §3 (mapping), §4 (pole region), §5 (training / LinOSS).
3. `shared/stage0_roadmap.md` v3 §S0.1 + the F19 framing; `shared/preregistration.md` (PR-2, PR-4 — this
   phase *feeds* them).
4. Executor artifacts: `docs/s0_1/mapping_notes.md`, `B1_actuation_map.md`, `B2_backscatter_bound.md`,
   `B3_kappa_ext_tradeoff.md`; code `photonic_ssm/dynamics/{single_ring,coupled_rings,pole_region}.py`,
   `photonic_ssm/platforms.py`; figures under `results/s0_1/` (regenerate via `analysis/s0_1_pole_region.py`).
5. `shared/decisions_needed.md` — **D-2026-06-08-2** (mapping fork) + **D-2026-06-08-3** (backscatter),
   each with the **Supervisor's recommendation** — adjudicate these independently.

## Review checklist — answer each specifically
1. **Gate integrity.** Is the S0.1 gate genuinely passed? The pole-match tolerances (uncoupled <1e-3,
   discrete $|z|$ <1e-9, ZOH exact for PWC input) and the CW-limit recovery ($O(1/\text{finesse})$, <1% at
   $F\geq1000$; SiN rings at $F\approx1000$–15000) — are these the right tests, are the tolerances
   adequate, and do they validate the **dynamical** mapping (not merely re-confirm the static limit)?
2. **Architecture-constraint reality.** Are (3a) gradient-through-state and (3b) full-trajectory exposure
   genuinely honored in the **new** model (the checkpointed==plain bit-identical-gradients test; the
   49-step gradient-flow test)? Any path where state gradients are silently dropped?
3. **The mapping fork (D-08-2).** One optical ring = one complex pole (complex-diagonal SSM / S4D-like) vs
   a real-LinOSS conjugate pair. The Supervisor recommends **the complex-diagonal realization, framed as
   the diagonalized LinOSS/D-LinOSS.** Is that sound — does the LinOSS↔complex-diagonal equivalence hold,
   do the LinOSS/D-LinOSS **benchmark results transfer** to the diagonal realization, and does the
   **white-space claim** survive the reframing? Any hidden cost (real-valued I/O, conjugate symmetry,
   D-LinOSS damping semantics) the recommendation glosses?
4. **B2 backscatter rigor — be hostile here.** The finding "splitting is roughness-limited, NOT Q-gated,
   bites at foundry Q for rough processes" rests partly on **search-aggregated figures** (the 63 MHz
   Pfeiffer value + some author lists) flagged as not-yet-primary-source-confirmed. (a) Is the crossover
   ($Q_\text{cross}\approx4\times10^6$ clean; $3$–$5.4\times10^5$ rough) **defensible enough to act on**
   (carry an optional S0.3 knob) ahead of primary-source confirmation? (b) What exactly must be
   primary-source-verified before it enters the proposal/paper? (c) Is the **qualitative** claim robust
   *independent* of the shaky numbers?
5. **The backscatter decision (D-08-3).** Is "optional CW/CCW splitting knob, process-roughness-gated, +
   promote roughness/splitting to a PR-4 sub-parameter" the right response? Does it adequately protect the
   "one ring = one complex pole" abstraction, and is the **platform tension** (high-Q = best-memory =
   most-splitting-prone vs CORNERSTONE low-Q = splitting-safe = memory-poor, ~33 round trips) correctly
   load-bearing for PR-4 / the platform choice?
6. **B1 white-space-minimal-set.** The claim that a **gain-free** minimal trainable set {δ (heaters),
   κ_tot (couplers), μ (coupling)} suffices for the white-space sentence, with residues / B,C excluded as
   the reservoir baseline. Is the trainable/excluded partition clean? Does it support "recurrent
   parameters updated on the device" without smuggling the readout into the claim?
7. **B3 + the bound.** Is `memory × residue ≤ passive memory` correct, and the $\kappa_\text{ext}$ trade
   (274 rt / 0.028 drop-eff → 16 rt / 0.91) honestly characterized? Is the B2↔B3 coupling (overcoupling
   hides the doublet) sound?
8. **F13.1 registry fix.** Is deriving the loss↔Q partner from a primary basis correct; is the AN800
   reconciliation (Qi=2×10⁶ primary → loss 0.172 dB/cm, vs the 0.03 dB/cm that implied 1.14×10⁷) the right
   call; is the `loss_q_ceiling` invariant sound?

## Also free to raise
Anything a hostile reviewer would attack: §3 mapping subtleties not yet modelled (dispersion, TPA/FCA at
the powers gain requires, thermal nonlinearity); whether the pole-region bound is complete; whether the
coupled-ring hybridization claim ($\Sigma\,\mathrm{Re}\,\lambda = -\Sigma\kappa_\text{tot}$) is correct.

## Expected output
Write `shared/critic_review_s0-1-results.md`:
- **Overall verdict:** APPROVE / APPROVE-WITH-EDITS / AMEND / REJECT (of the S0.1 results + the gate).
- **Numbered findings**, each with **severity** (CRITICAL / HIGH / MEDIUM / LOW) + a concrete actionable
  recommendation; distinguish "must fix before S0.2" from "fix before the paper."
- **An explicit, independent recommendation on D-2026-06-08-2 and D-2026-06-08-3** (agree / disagree with
  the Supervisor's, with reasoning).
