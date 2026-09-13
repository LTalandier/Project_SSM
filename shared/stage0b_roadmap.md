# Stage 0b Roadmap — The product question P1 did not ask (simulation + envelope; no chip)

**Owner:** Supervisor (single-session mode). **Status:** **v0.1 APPROVED for S0b.0 (Lucas, "Ok go", 2026-09-13; E-2026-09-13-1 item 1)** — S0b.0
runs now (€0); S0b.1–S0b.3 spend returns to Lucas at the post-S0b.0 continuation gate. Nothing here touches P1.
**Source of truth:** P1 §7 (the frozen envelope and its four exclusions), `docs/s0_7/exclusions_ledger.md`
(primary-sourced overhead numbers), PR-18/PR-19 (§18.6b N_eff path; §19.6c floor-degeneracy lesson),
and the 2026-09-13 PI discussion that scoped this stage. **Companion file:** `preregistration.md` —
PR-20 … PR-23 freeze there before the run each governs.

> **Why a Stage 0b exists.** P1 answers "can the recurrence be trained on a realistic SiN substrate"
> (yes; PAT/SPSA; one formal drift win) and gives a first-pass systems envelope whose verdict is
> *unmeasured in magnitude* (§7.2). That envelope was one workload (7-tap equalization, N_eff = 6–8),
> one actuator class (thermo-optic heaters, A/B), one deployment scope (local laser, full E/O in +
> O/E out), and baselines priced at nominal N. Each of those is a clause, and each clause is a door.
> Stage 0b measures the other corners of that space **before anyone spends on a wafer**. Its honest
> prior is negative: the fixed per-device overheads (laser, heater hold, locking, conversion) are the
> same order as the photonic compute itself (§7.1), and the only way they shrink is by re-scoping
> what the device is (inline, not a detour), what actuates it (non-volatile, not thermal), and what
> it is compared to (the DSP block it would replace, priced to the function).

## The question, stated so it can fail

**Does a differently specified photonic recurrence — an inline, trainable, linear-time-invariant
optical filter with state, on SiN — clear the digital block it would replace, at the conservative
corner, on a workload that measurably exercises its state dimension?**

Three conditions, each with a phase that measures it, each able to kill the stage:

| condition | why it is open | phase |
|---|---|---|
| The signal is already optical, so the device pays no E/O in and shares the receiver's O/E out | §7 charged a local laser + full conversion; the exclusions ledger has the numbers to re-scope | S0b.0 |
| A workload needs more state than a few taps (N_eff ≥ 16 on this substrate) | §7.2 burden-flip: no such workload in P1's data; PR-19 was floor-degenerate, not negative | S0b.1 |
| The actuators hold state at near-zero power and can still be trained through | heater hold is the largest static term; non-volatile classes exist but are quantized + write-limited, and no in-situ method has been shown to train through them | S0b.2 |

Plus one lever already in-data: **retraining instead of locking** (S0b.3) — the 2.42× drift result
(§5.5) is evidence that periodic in-situ retraining absorbs drift; if it can replace the lock loop at
some duty cycle, the locking term drops out too.

**Framing rule (from the software-SSM state of the art, 2026-09-13):** the shipping SSMs are
*selective* (input-gated recurrence); a ring lattice is *time-invariant* (poles set by actuators,
fixed at the symbol rate). Stage 0b therefore frames the device as an S4/LinOSS-class **trainable
optical LTI filter**, targets the workloads where LTI SSMs still hold their own (streaming signal
data: equalization, RF, audio-class time series), and does not use "SSM" as a capacity claim
anywhere a filter description would do. Thirty-two rings is a small state by software standards;
S0b.1 is where that number stops being a toy or is shown to be one.

## Non-goals

- **No chip, no fab quote, no MPW application** until S0b.4's verdict — Stage 0b is the pre-MPW-spend
  finding the S0.7 gate asked for, now with the corners P1 left unmeasured.
- **No edits to P1.** P1 submits as frozen (round 7). Stage 0b output is a separate unit (P5 below);
  if S0b.1 lands an informative N_eff ≥ 16, P1's "no such demonstration exists in this program's data"
  stays true *of P1's data* and P5 cites it as the follow-up P1 explicitly asked for.
- **No new estimator bake-off.** PAT and SPSA are the hardware-committed routes; S0b.2 trains *them*
  through a new actuator model. Adjoint/RHEL stay where Gate ii left them.
- **No claim of a first.** Stage 0b is an envelope-and-feasibility stage; the "first" remains
  collectible only on hardware.

## Phase decomposition

### S0b.0 — Envelope re-scope (the kill gate; no new physics code; ~2–3 days)
- **Goal:** re-price the §7 envelope under an **inline receiver scope** with the four exclusions
  *charged*, at three actuator classes, against a **function-matched** digital baseline — and state
  whether any cell can go positive at all. This is the cheapest phase and the one most likely to end
  the stage; it runs first for that reason.
- **Method:** extend `analysis/s0_7_lite_envelope.py` (same corner/scenario structure, same frozen
  conversion rows) with:
  1. **Scope switch** `inline`: no E/O in (light is the transmitter's); O/E out = the receiver's
     photodiode + ADC, charged as *incremental* only where the photonic stage forces a different
     ADC (rate/ENOB) than the digital receiver already runs; laser term = 0 for the device
     (charged to the link, stated as such). Control-compute, locking, packaging charged from the
     exclusions ledger — no longer excluded.
  2. **Actuator class C** (non-volatile / near-zero hold) alongside A/B: per-class hold power,
     write energy per set, endurance (write count), and resolution (levels per π) — every number
     primary-sourced into a new `docs/s0b/actuator_ledger.md` with the exclusions-ledger status
     convention (VERIFIED / UNVERIFIED-direct / derived). Candidate classes to source: phase-change
     (Sb₂Se₃ / GST on SiN), piezo-optomechanical (AlN/PZT on SiN), MEMS-tuned SiN. Only the
     actuators that P1 shows carry the trained structure (4 driven taps + couplings) need be class C;
     the rest may be held by class A/B trim — both configurations priced.
  3. **Function-matched baseline:** the coherent-DSP equalizer block priced **per tap** at the
     ledger's pJ/bit bracket, at the tap count a digital equalizer needs to reach the same SER on
     the same channel (measured, not nominal — S0b.1 supplies it; S0b.0 runs parametric in
     tap count and marks the P1 point at ~6–8 taps). Brainwave and Jetson stay as secondary rows.
- **Pre-registration — PR-20 (freeze before the script runs):** the inline-scope charging rules
  (what is incremental, what is the link's), the actuator-class rows with sources, the per-tap DSP
  pricing rule, the operating grid (N, rate, tap count), and the **stage verdict rule** used again
  at S0b.4: *a product window exists iff at the CONS corner, with a function-matched baseline, at
  least one cell clears ≥ 3× in energy per sample at a workload with measured N_eff ≥ 16, with all
  four former exclusions charged.* OPT-corner-only clearance is reported and labelled not
  load-bearing, as in S0.7-lite.
- **Gate / kill:** if **no cell clears at the OPT corner under inline scope with class C** (the most
  favourable specification this stage will ever consider), the product door is closed by
  arithmetic; S0b.1–S0b.3 are not run, the negative is written up as a short addendum to the S0.7
  exclusions ledger, and Stage 0b ends. Otherwise the surviving cells define the (N, rate, tap
  count, actuator class) grid S0b.1–S0b.3 must hit.
- **Cost:** €0 compute. Runtime: the retrieval for the actuator ledger dominates.

### S0b.1 — Capacity: an informative N_eff on a product workload (PR-21)
- **Goal:** the measurement P1 §7.2 says would restore the N-scaling premise — a workload on which
  the trained device's output measurably rides on ≥ 16 of 32 rings — done so that the §19.6c floor
  degeneracy **cannot recur**.
- **Task T-E (long-span ISI equalization):** the product workload itself. Same frozen 4-PAM source
  and 2 GS/s as T-A; channel = a **dispersive ISI response of registered span S ∈ {32, 48, 64}
  samples** (chromatic-dispersion-class all-pass phase, magnitude-flat, so memory is required and
  cannot be integrated away — the exact failure of T-D), applied at sample rate; decision at every
  symbol; SER per symbol. T-E is chosen over a lower-SNR T-D because (a) it *is* the DSP block the
  baseline prices, so N_eff and the function-matched tap count come from one run, and (b) a phase-
  only channel has no integration gain to void the target rule.
- **The anti-degeneracy protocol (the §19.6c lesson, made mechanical):**
  1. **Ceiling-band rule, registered:** SNR is *not* frozen; the **search rule** is. Arm-(ii) BPTT
     ceiling is measured at a registered SNR ladder and the run SNR is the lowest rung at which the
     8-seed median ceiling SER lies in **[1×10⁻³, 3×10⁻²]** — solvable but not free. Outside the
     band at every rung → the span is reported unsolvable/trivial at this N and the next span is
     tried; no grid runs on a floor.
  2. **Consumption texts carry a degenerate branch:** rise / no-rise / intermediate / **degenerate
     (ceiling out of band, or head-refit recovers from < N_eff/2 rings)** — the fourth branch is the
     one PR-19 lacked.
  3. **Function-matched digital tap count** measured in the same run: the minimum FIR/DFE length
     reaching the photonic arm's SER on the same channel (ridge/LMS, registered), which prices the
     S0b.0 baseline to the function.
- **Arms:** (i) pinned-damping sweep, §6 protocol verbatim (r ∈ {0.2, 0.3, 0.5, 1.0, 2.0, 3.0});
  (ii) BPTT free-partition reference at matched budget; (iii) PAT pat-both; (iv) **SPSA** (added
  back — S0b.2 needs an SPSA endpoint on this task as its own comparator). C-2, 8 seeds, pilot seed
  excluded; PR-6 fairness contract verbatim.
- **Registered predictions (PR-21):** **P2′** N_eff by the §18.6b path: rise iff median ≥ 16;
  no-rise iff ≤ 10; degenerate per the branch above. **P1′** (the damping-tracks-memory test,
  now well-posed because span ≫ head reach and no integration gain): r*_E ≤ 1.0 with the §17.5
  upgrade rule; this is the hypothesis' third genuine test after T-A-L and the degenerate T-D,
  and it is reported as pass/fail either way. **P3′** the function-matched tap count ≥ 16 (if the
  digital function needs fewer taps than the photonic N_eff, the N-scaling premise fails from the
  baseline side even with a rise — reported as such).
- **Gate:** an informative P2′ (rise or no-rise, not degenerate) is the deliverable regardless of
  direction. **Rise → S0b.0's surviving cells are re-priced at the measured N_eff and tap count.
  No-rise → the capacity door closes on this substrate at N = 32**: the stage verdict at S0b.4 is
  negative on the capacity condition, and S0b.2/S0b.3 are completed only for the P5 record.
- **Cost:** PR-19-scale — ≈ 130–200 server-hours ≈ €50–80 excl. VAT (pilot + 4 arms × 8 seeds ×
  up to 3 spans; ceiling ladder adds ≈ 30%). Servers deleted and independently verified after use.

### S0b.2 — Training through write-limited, quantized actuators (PR-22)
- **Goal:** whether PAT and SPSA still reach target when the actuators are class C: **quantized to
  L levels per π, each write costs registered energy, and the total write count is budgeted** —
  the open problem that decides whether the heater-hold term can be removed *without losing the
  in-situ training result*. Nobody has shown in-situ training of a recurrence through such actuators.
- **Method:** a new `photonic_ssm/substrate/actuators.py` layer between the trainable parameters
  (δ, κ_ext per ring) and the substrate: quantizer (L levels, registered from the S0b.0 ledger),
  write counter + energy accumulator (per parameter, per step), optional hysteresis/asymmetry
  (set vs reset cost) from the ledger. Estimator adaptations, each registered: SPSA perturbation
  ε ≥ 1 level (its two forward passes now cost two writes each — the SPSA cost row changes);
  PAT with a straight-through or stochastic-rounding backward (twin knows the quantizer).
  **Configurations:** class C on all 32 rings vs **class C on the 4 driven taps only** (P1 §5.7:
  the trained structure lives there; undriven rings sit at initialization) with class B trim on
  the rest — the second is the realistic device and the one S0b.0 prices.
- **Registered rules (PR-22):** the level ladder L ∈ {8, 16, 32, 64, continuous}; the write budget
  W per parameter from the ledger's endurance row; **target = the PR-3/PR-17 target of the task**
  (T-A at the frozen cell for continuity with Gate ii; T-E at S0b.1's registered SNR if S0b.1
  cleared); success = target reached within W writes at level L; deliverable = the **minimum L
  and the write energy** at which each route reaches target, plus the sample-efficiency ratio to
  the continuous case. Prediction: SPSA degrades first (ε floor), PAT tolerates L ≥ 16.
- **Gate:** if **neither** route reaches target at any L ≤ 64 within the ledger's endurance, class
  C is not trainable in situ on this substrate → the actuator condition fails, S0b.4 verdict
  negative on that axis, and the heater-class result stands as P1 left it.
- **Cost:** ≈ 100–150 server-hours ≈ €40–60 (T-A cell, 2 routes × 5 levels × 2 configurations ×
  8 seeds, reduced budgets).

### S0b.3 — Retraining instead of locking (PR-23)
- **Goal:** the drift lever already in-data, priced. Under the S0.9 drift model (per-ring Wiener
  drift calibrated to the 341 MHz/24 h anchor; uncorrelated + common-mode regimes), find the
  **retraining duty cycle** (updates per unit wall-clock) that holds SER at target *without* a lock
  loop, and convert it to power (updates/s × energy per update from §7.3, class-dependent) to set
  against the ledger's locking rows (4.6–6.8 mW/ring heater-locking demos; ~10 W FPGA-class lock).
- **Method:** extend `deploy_then_drift` with a periodic-retraining schedule (registered ladder of
  K-spacings and update budgets per burst); the S0.9 "re-lock" control arm stays as the locked
  comparator. Runs on class A/B first; **a class-C addendum after S0b.2** charges each retraining
  burst against the write budget — the real trade (non-volatile hold vs finite endurance) appears
  only there.
- **Registered rule (PR-23):** the maintenance power P_retrain(duty) at which the 8-seed median SER
  stays within 1.25× target over the registered horizon, per regime; verdict *retraining replaces
  locking* iff P_retrain < the lowest sourced locking power at the same drift rate, at CONS.
- **Gate:** informational; feeds S0b.4 as the locking-term replacement or as its confirmation.
- **Cost:** ≈ 40–60 server-hours ≈ €15–25 (S0.9-scale).

### S0b.4 — Full re-envelope, verdict, write-up (P5)
- **Goal:** apply the PR-20 stage verdict rule to measured inputs: N_eff and function-matched tap
  count (S0b.1), actuator class C resolution/write energy or its failure (S0b.2), locking term or
  its replacement (S0b.3), all four former exclusions charged, CONS corner, inline scope.
- **Output:** **P5** — either *"An inline trainable optical filter on SiN: a measured product
  envelope"* (positive: the (N, rate, actuator, workload) cell that clears, with every number
  traced) or the negative in the same form (*"…does not clear, and here is which condition fails"*).
  Both are publishable; the negative is the more likely and the more useful to the field. P1
  unchanged; P3 (hardware letter) is gated on a positive verdict or on a collaboration that funds
  the "first" without it.
- **Kill criteria carried forward:** any of S0b.0 no-OPT-clearance, S0b.1 no-rise, S0b.2 untrainable
  → the verdict is negative on that condition and says so in the title.

### S0b.L — Literature / verification track (parallel)
- Actuator classes primary-sourced (S0b.0 ledger) — hold power, write energy, endurance, levels,
  wavelength (must be C-band on SiN, not silicon-only demos), with the exclusions-ledger status tags.
- DSP equalizer power **per tap** from coherent-ASIC papers (the ledger holds only pJ/bit per block).
- The LTI-filter framing: cite S4/S4D, LinOSS, and reservoir-equalization work as the neighbors;
  check for any 2026 photonic non-volatile-actuator training demonstration (the S0b.2 white space —
  registered page reads before S0b.2 claims novelty).

## Dependency graph
```
S0b.0 (PR-20; envelope re-scope; kill gate) ──┬─▶ S0b.1 (PR-21; T-E capacity) ──┐
       [Lucas: continuation gate]             ├─▶ S0b.2 (PR-22; class-C actuators) ┼─▶ S0b.4 (verdict → P5)
                                              └─▶ S0b.3 (PR-23; retrain-vs-lock) ─┘   [Lucas: MPW/collab gate]
                                                       └── class-C addendum after S0b.2
S0b.L ∥ throughout (actuator ledger before PR-20 freezes; per-tap DSP before PR-20; page reads before S0b.2)
```
S0b.1, S0b.2, S0b.3 are independent and can run in parallel once S0b.0 passes.

## Pre-registration index (freeze in `preregistration.md` before the governing run)
- **PR-20** — S0b.0: inline-scope charging rules, actuator-class rows + sources, per-tap DSP rule,
  grid, **stage verdict rule** (reused at S0b.4).
- **PR-21** — S0b.1: T-E channel family + spans, SNR ceiling-band search rule, four-branch
  consumption texts (incl. degenerate), P1′/P2′/P3′ rules, function-matched tap-count protocol,
  arms/seeds/budget.
- **PR-22** — S0b.2: actuator model, level ladder, write budget, estimator adaptations, target rule,
  success/deliverable rule, prediction.
- **PR-23** — S0b.3: retraining schedule ladder, maintenance-power rule, locking comparator rows.

## Decision gates owned by Lucas
- ✅ **E-2026-09-13-1 — approve this roadmap (v0.1) and the S0b.0 spend (€0).** Approved 2026-09-13 ("Ok go"); P1 sequencing = submit-first default, S0b.0 runs before the submission decision (Lucas's 2026-09-13 reading: run the free gate first, then decide P1).
- ⬜ **Continuation gate after S0b.0:** the OPT-corner clearance verdict + PR-21/22/23 freezes +
  the compute envelope (total ≈ €105–165 excl. VAT for S0b.1–S0b.3; each phase escalated
  separately per standing rule).
- ⬜ **P1 sequencing:** submit P1 before Stage 0b results exist (recommended — P1 is frozen and its
  burden-flip sentence is the motivation for S0b.1), or hold P1 to fold S0b.1 in. Default: submit.
- ⬜ **S0b.4 verdict → MPW/collaboration decision.** Positive: P3 becomes fundable on evidence.
  Negative: P3 is a "first" only, pursued solely as a collaboration where the hardware cost is not
  Lucas's (the 2026-09-13 ruling).

## Standing disciplines (unchanged from Stage 0)
Single-session mode (self-review disclosed); pre-register before consuming; `results/` gitignored
(explicit adds); commit **and push** after every commit; servers deleted and independently verified;
4 seeds minimum, 8 for SPSA; the §19.6c lesson is now protocol: **every pre-written consumption text
carries a degenerate branch**, and the premise each text assumes is named in the text.
