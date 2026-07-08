# P1 — Stage-0 methods/feasibility paper: OUTLINE

**Status:** working skeleton (2026-07-07, Supervisor). Owned by the Supervisor per
`shared/publication_plan.md` (P1). **Nothing here is frozen or citable until S0.8**; results
slots stay EMPTY until their pre-registered runs produce them (the governing PR-ID is named
on every slot). Critic reviews the manuscript at S0.8 as usual.

**Working title candidates** (pick at S0.8):
1. *Can a photonic state-space model be trained on-chip? A pre-registered four-method
   bake-off on a realistic silicon-nitride ring substrate*
2. *In-situ trainability of dissipative photonic state-space models: SPSA, physics-aware
   training, adjoint, and Hamiltonian-echo compared under realistic noise*
3. *Toward the first in-situ-trained recurrent photonic system: a simulation bake-off on
   ultra-low-loss SiN microrings*

Recommendation: (1) — the question form is honest about Stage 0 being simulation, and
"pre-registered" is a differentiator worth putting on the cover.

---

## Draft abstract (numbers ▢-blanked until governed runs land)

> Recurrent photonic processors promise low-latency, low-energy sequence processing, but no
> recurrent photonic system has ever had its recurrence-defining parameters — pole positions
> and inter-ring couplings — trained on the physical device by any gradient-based or
> gradient-estimating method [debt #1 / PR-15 dated search]. We ask whether such in-situ
> training is feasible for a structured photonic state-space model: an oscillatory
> (LinOSS-class) coupled-microring recurrence on ultra-low-loss silicon nitride. We (i)
> derive the mapping from the discrete oscillatory SSM to a physically realizable coupled-ring
> lattice and bound its realizable pole region; (ii) build one shared dissipative substrate
> model — finite Q, saturating gain, amplified-spontaneous-emission noise — with all
> parameters pre-registered before any training run; and (iii) run a four-method
> in-situ-training bake-off — SPSA, physics-aware training, recurrent in-situ adjoint, and
> Hamiltonian-echo learning — under a pre-registered fairness contract, scored on
> sample-efficiency-to-target-accuracy at matched device-pass cost. At realistic SiN noise,
> ▢ of the four methods reach the pre-registered accuracy target; the best requires ▢×
> fewer device passes than ▢ [PR-8/9]. A measured participation profile shows the
> single-drive lattice trains an effective dimension of ▢ of N=32 rings, rising to ▢ with
> ▢ input taps [S0.4-0] — a controllability constraint that any hardware implementation
> inherits. An end-to-end systems envelope including electro-optic conversion and
> DAC/ADC overhead finds ▢ [S0.7-full / §10]. We conclude that on-chip training of a
> photonic SSM is ▢, identify the operating regime where it pays, and release the
> pre-registration ledger, substrate model, and all training code.

(Every ▢ maps to a gate: sentence 5 → Gate ii · sentence 6 → S0.4-0 participation profile ·
sentence 7 → S0.7-full envelope gate · sentence 8 → the honest either-way conclusion.)

## Claims → evidence table

| # | Claim | Evidence source | Status |
|---|-------|-----------------|--------|
| C1 | White-space: no prior in-situ gradient-based/-estimating training of recurrent-internal photonic params | PR-15 two-modality search, `docs/s0_L/` (+ S0.8 refresh sweep) | ✅ one-sided PASS on record |
| C2 | Oscillatory SSM ↔ SiN ring lattice mapping + realizable pole region | S0.1, `docs/s0_1/` (B1–B3) | ✅ done |
| C3 | Idealized model reproduces oscillatory-SSM task accuracy within pre-registered margin | Gate (i), PR-1/PR-2/PR-3 in-house ceiling | ✅ S0.2 closed (G1 PASS; G3 anchor void → in-house ceiling) |
| C4 | ≥1 method trains to pre-registered accuracy at realistic SiN noise | Gate (ii), PR-8/PR-9, S0.5 bake-off | ✅ **PASS 2026-07-07 — PAT-both AND SPSA 8/8 to target at C-2** (`results/s0_5/bakeoff.md`) |
| C5 | Method ranking at matched device-pass cost (+ digital-ledger co-report) | PR-6/PR-7, S0.5 | ✅ **PAT 38.4k < adjoint 73.6k < SPSA 176k; RHEL censored; no promotion; + offline-tie null** |
| C6 | Effective participating dimension / controllability constraint + multi-tap remedy | PR-6 §B v3, S0.4-0 participation profile | ✅ measured (3/32 → 32/32 at K=4 taps {3,12,21,30}); §5.7 prose ▢ |
| C7 | Damping operating point improves accuracy (D-LinOSS, R-ii trainable-κ_ext framing) | PR-12, S0.6 | ✅ **×302 spread; r*=2.0; R-ii CONFIRMED (boxed 0.0005 beats pin 0.0013)** |
| C8 | Systems-advantage envelope verdict incl. conversion overhead | PR-10 lite (✅ conditional-positive) → S0.7-full | ✅ **core done: lite verdict stands + training-energy inversion (SPSA 2.6 mJ vs PAT 13–44 J); exclusions ledger → S0.8 list** |
| C9 | RHEL-on-SiN feasibility via concrete χ³-FWM echo sub-model (or explicit off-chip admission) | PR-11, S0.4c | ✅ **template B: censored + worse-than-readout under honest echo; dissipative-echo bias (idealized-C_op control isolates); F22 record** |

## Section plan (source → prose; ✍ = writable now)

1. **Introduction** ✍ DRAFT v1 (`sections/01_intro.md`, 2026-07-08; W1 scope used, W0-vs-W1 = PI
   call at S0.8; search refresh required pre-submission) — the in-situ-training gap for *recurrent* photonics; why SSMs (LinOSS
   line) are the right recurrence class for rings; the sharpened white-space sentence
   (exact PR-15 wording from `docs/s0_L/whitespace_claim_wording.md`); contributions list =
   claims table. Pre-empt: reservoir computing, Bueno/Brunner RL line, internal-param
   reservoir variants (F15 lanes).
2. **From oscillatory SSMs to coupled SiN microrings** ✍ — the LinOSS/D-LinOSS unit; the
   dissipative-A validity argument; the mapping + realizable pole region (S0.1 figures);
   actuation map (B1), backscatter/splitting (B2, K-pol-3 always-ON), κ_ext trade-off (B3).
3. **A pre-registered dissipative substrate** ✍ DRAFT v1 (`sections/03_substrate.md`, 2026-07-08)
   — PR-4 v2 as prose: M1 saturating gain at
   g_rt=0.9×intrinsic, A2 Langevin ASE (van-Loan covariance), NF-A 7.0 dB, the three cells
   (P-FND/8 · P-AN800/32 headline · P-UHQ/128), K4 drive box + the lasing-boundary clamp
   (r*≈0.134 → operative band [r_min, 3], r_min rule PR-6 §C v3); why one shared substrate =
   the apples-to-apples condition. Sidebar: the pre-registration ledger as method (what was
   frozen when; supplementary = `shared/preregistration.md`).
4. **Four routes to on-chip gradients** ✍ DRAFT v1 (`sections/04_methods.md`, 2026-07-08) — SPSA; PAT (+ PR-5
   twin-mismatch protocol); recurrent in-situ adjoint; RHEL + the concrete echo/
   phase-conjugation sub-model (PR-11). The fairness contract (PR-6) and the cost metric
   (PR-7: device passes primary, digital ledger co-reported). The
   parallel-in-simulation/singular-in-hardware guardrail (§5.2).
5. **Bake-off results** ✍ DRAFT v1 (`sections/05_results.md`, 2026-07-08) — 5.1 pre-reg+ceiling ·
   5.2 Gate ii PASS (C4) · 5.3 ranking PAT<adjoint<SPSA, RHEL censored (C5) · 5.4 RHEL honest echo
   (C9) · 5.5 offline-tie honest-null · 5.6 diagnostics; 5.7 participation/eff-dim (C6) ▢ + 5.8
   PR-14 cosine ▢ still to draft — sample-efficiency-to-target curves per cell (C4/C5); the
   participation-profile / effective-dimension result (C6) incl. the reservoir-readout
   baseline as debt-#1 falsifier; secondary diagnostic (PR-14 gradient-cosine) demoted to
   an appendix-grade subsection.
6. **Choosing the damping operating point** ✍ DRAFT v1 (`sections/06_damping.md`, 2026-07-08) — S0.6 sweep under R-ii framing (C7).
7. **Does it pay? The systems envelope** ✍ DRAFT v1 (`sections/07_envelope.md`, 2026-07-08) — S0.7-full vs the strong digital baseline
   (F16 floor: named FPGA/ASIC/embedded-GPU sources, full power ledger incl. thermo-optic
   holding + locking + E/O–O/E + DAC/ADC, precision–accuracy link). Honest either-way
   verdict (§10).
8. **Limits of this model** ✍ DRAFT v1 (`sections/08_limits.md`, 2026-07-08) — F19 verbatim seed: robustness measured against *modelled*
   imperfections only; thermal transients, polarization, fab variation, un-knobbed
   mode-splitting could reorder methods on hardware. Plus: G3 anchor status (one careful
   paragraph; expanded treatment → P2 if Lucas rules GO), fp32 sensitivity, single-seed
   caveats where they exist.
9. **Outlook: Stage 1** ✍ DRAFT v1 (`sections/09_outlook.md`, 2026-07-08) — MPW path (CORNERSTONE/LIGENTEC), PAT/SPSA hardware-committed,
   promotion rule for adjoint/RHEL (PR-9), what the first on-chip demonstration would
   require. Frame per F22: the novelty is the recurrent dissipative setting, not
   re-validating chip-proven PAT/SPSA.

## Figure plan

| Fig | Content | Source phase |
|-----|---------|--------------|
| F1 | Architecture: oscillatory unit ↔ ring lattice; realizable pole region overlay | S0.1 ✅ (replot to pub quality) |
| F2 | Substrate: saturating vs fixed κ_net(r); lasing crossing r*; clamp band; ASE/NF anchor | S0.3 ✅ + S0.4-0 floor numbers |
| F3 | Participation profile: per-ring gradient magnitude, single-drive vs {1,9,17,25} taps; effective dimension | S0.4-0 |
| F4 | **Headline:** sample-efficiency-to-target, 4 methods × 3 cells, realistic noise | S0.5 |
| F5 | Cost-normalized ranking: device passes (primary) + digital ledger (co-report) | S0.5 |
| F6 | Damping sweep: accuracy vs trainable-κ_ext damping at fixed g_f | S0.6 |
| F7 | Systems envelope: latency/energy waterfall vs digital baseline incl. conversion | S0.7-full |
| S-figs | G3 dossier summary; twin-mismatch (PR-5); echo sub-model penalties (PR-11); secondary diagnostic (PR-14) | various |

## Writing order (Supervisor)

1. §2 mapping (closest to done — `docs/s0_1/mapping_result.md` is near-prose) →
2. §3 substrate (PR-4/PR-6 → prose) → 3. §1 intro (needs the white-space wording lifted
   verbatim) → 4. §4 methods specs → 5. §8 limits skeleton → 6. results sections as runs land.

Venue formatting deferred until Lucas picks (plan: arXiv first regardless).
