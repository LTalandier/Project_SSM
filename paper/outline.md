# P1 — Stage-0 methods/feasibility paper: OUTLINE

**Status:** working skeleton (2026-07-07, Supervisor). Owned by the Supervisor per
`shared/publication_plan.md` (P1). **Nothing here is frozen or citable until S0.8**; results
slots stay EMPTY until their pre-registered runs produce them (the governing PR-ID is named
on every slot). Critic reviews the manuscript at S0.8 as usual.

**Title — CHOSEN 2026-07-26 (PI-delegated ruling, E-2026-07-12-1):**

> ***Can a photonic state-space model be trained on-chip? A pre-registered four-method
> bake-off on a realistic silicon-nitride ring substrate***

(Candidate 1; the question form is honest about Stage 0 being simulation, and
"pre-registered" is a differentiator worth putting on the cover. Rejected alternates kept
for the record: 2. *In-situ trainability of dissipative photonic state-space models: SPSA,
physics-aware training, adjoint, and Hamiltonian-echo compared under realistic noise*;
3. *Toward the first in-situ-trained recurrent photonic system: a simulation bake-off on
ultra-low-loss SiN microrings*.)

---

## Draft abstract (▢-FILLED at S0.8 from landed gates, 2026-07-12; numbers frozen-source)

> Recurrent photonic processors promise low-latency, low-energy sequence processing, but no
> recurrent photonic system has ever had its recurrence-defining parameters — pole positions
> and inter-ring couplings — trained on the physical device by any gradient-based or
> gradient-estimating method [PR-15 search + 2026-07-12 refresh]. We ask whether such in-situ
> training is feasible for a structured photonic state-space model: an oscillatory
> (LinOSS-class) coupled-microring recurrence on ultra-low-loss silicon nitride. We (i)
> derive the mapping from the discrete oscillatory SSM to a physically realizable coupled-ring
> lattice and bound its realizable pole region; (ii) build one shared dissipative substrate
> model — finite Q, saturating gain, amplified-spontaneous-emission noise — with all
> parameters pre-registered before any training run; and (iii) run a four-method
> in-situ-training bake-off — SPSA, physics-aware training (PAT), recurrent in-situ adjoint,
> and Hamiltonian-echo learning (RHEL) — under a pre-registered fairness contract, scored on
> sample-efficiency-to-target-accuracy at matched device-pass cost. At realistic SiN noise,
> three of the four reach the pre-registered target on 8/8 seeds — both hardware-committed
> workhorses among them — with PAT needing 4.6× fewer device passes than model-free SPSA
> (38,400 vs 176,000) but a digital-twin side-ledger four orders of magnitude more energy
> than SPSA's entire training bill (13–44 J vs 2.6 mJ); RHEL is censored at budget, its echo
> defeated by the very dissipation the recurrence needs. A measured participation profile
> shows the single-drive lattice trains an effective dimension of ≈3 of N=32 rings, rising
> to all 32 with four input taps — a controllability constraint, and conversion cost, that
> any hardware implementation inherits. Trained damping is a first-order design knob (×300
> in error across the feasible box), and training finds a heterogeneous damping profile that
> beats every uniform setting. An end-to-end envelope including electro-optic conversion and
> DAC/ADC overhead finds a conditional low-latency niche (GS/s line rates, N ≳ 32, low-power
> heater class) — while an equally-calibrated offline-train-then-deploy baseline
> statistically ties in-situ training at calibration errors up to 30%-class; the tie breaks
> only under uncorrelated per-ring drift, where in-situ retraining holds a statistically
> significant, drift-growing edge that a global laser re-lock cannot absorb (1.84×
> time-integrated, below our pre-registered 2× bar, so no formal advantage is declared):
> the demonstration is in-data; the advantage case is directional and drift-specific, and we
> say so. We release the pre-registration ledger, substrate model, and all training code.

(Sentence→gate map: trainability → Gate ii (PR-8/9) · ranking/energy → S0.5 + S0.7 ·
participation → S0.4-0 · damping → S0.6/PR-12 R-ii · niche + offline-tie/drift → S0.7 +
§5.5 as upgraded by S0.9 (PR-5 §E + PR-16). The abstract states the null and the sub-2×
drift verdict; these are the paper's most falsifiable sentences.)

## Claims → evidence table

| # | Claim | Evidence source | Status |
|---|-------|-----------------|--------|
| C1 | White-space: no prior in-situ gradient-based/-estimating training of recurrent-internal photonic params | PR-15 two-modality search, `docs/s0_L/` (+ S0.8 refresh sweep) | ✅ one-sided PASS on record |
| C2 | Oscillatory SSM ↔ SiN ring lattice mapping + realizable pole region | S0.1, `docs/s0_1/` (B1–B3) | ✅ done |
| C3 | Idealized model reproduces oscillatory-SSM task accuracy within pre-registered margin | Gate (i), PR-1/PR-2/PR-3 in-house ceiling | ✅ S0.2 closed (G1 PASS; G3 anchor void → in-house ceiling) |
| C4 | ≥1 method trains to pre-registered accuracy at realistic SiN noise | Gate (ii), PR-8/PR-9, S0.5 bake-off | ✅ **PASS 2026-07-07 — PAT-both AND SPSA 8/8 to target at C-2** (`results/s0_5/bakeoff.md`) |
| C5 | Method ranking at matched device-pass cost (+ digital-ledger co-report) | PR-6/PR-7, S0.5 | ✅ **PAT 38.4k < adjoint 73.6k < SPSA 176k; RHEL censored; no promotion; + offline-tie null** |
| C6 | Effective participating dimension / controllability constraint + multi-tap remedy | PR-6 §B v3, S0.4-0 participation profile | ✅ measured (3/32 → 32/32 at K=4 taps {3,12,21,30}); §5.7 DRAFTED 2026-07-12 |
| C7 | Damping operating point improves accuracy (D-LinOSS, R-ii trainable-κ_ext framing) | PR-12, S0.6 | ✅ **×302 spread; r*=2.0; R-ii CONFIRMED (boxed 0.0005 beats pin 0.0013)** |
| C8 | Systems-advantage envelope verdict incl. conversion overhead | PR-10 lite (✅ conditional-positive) → S0.7-full | ✅ **core done: lite verdict stands + training-energy inversion (SPSA 2.6 mJ vs PAT 13–44 J); exclusions ledger → S0.8 list** |
| C9 | RHEL-on-SiN feasibility via concrete χ³-FWM echo sub-model (or explicit off-chip admission) | PR-11, S0.4c | ✅ **template B: censored + worse-than-readout under honest echo; dissipative-echo bias (idealized-C_op control isolates); F22 record** |

## Section plan (source → prose; ✍ = writable now)

1. **Introduction** ✍ DRAFT v2 (`sections/01_intro.md`, 2026-07-26; scope RULED: W0-in-prose +
   W1-core-sentence; search refresh required pre-submission) — the in-situ-training gap for *recurrent* photonics; why SSMs (LinOSS
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
5. **Bake-off results** ✍ DRAFT v2 (`sections/05_results.md`; 5.1–5.6 2026-07-08, **5.7/5.8
   drafted 2026-07-12**) — 5.1 pre-reg+ceiling · 5.2 Gate ii PASS (C4) · 5.3 ranking
   PAT<adjoint<SPSA, RHEL censored (C5) · 5.4 RHEL honest echo (C9) · 5.5 offline-tie
   honest-null · 5.6 diagnostics · 5.7 controllability/participation (C6, Fig. F3) ·
   5.8 PR-14 registered-deferred (appendix-grade, S0.5-full).
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

## Figure plan — **ALL F1–F7 MADE 2026-07-12** (`paper/figures/F*.{png,pdf}`, generator `analysis/make_figures.py`, data = frozen result JSONs only)

| Fig | Content (as built) | Source phase |
|-----|---------|--------------|
| F1 ✅ | (a) 32-ring chain schematic, trained partition, resolved taps {3,12,21,30}; (b) memory-vs-Qi region at g_f∈{0,0.5,0.9}, task-span line, cells | S0.1 |
| F2 ✅ | (a) settled saturating vs fixed κ_net(r), lasing r*, clamp band, θ₀, r*_damp cross-link; (b) off-resonance de-saturation at r_min vs θ₀ (anchor-risk vii) | S0.3/S0.4-0 |
| F3 ✅ | Participation: per-ring gradient ratio, single-drive cliff vs resolved B flat ≥ gate 10⁻³ (resolved taps {3,12,21,30}, not the {1,9,17,25} seed) | S0.4-0 |
| F4 ✅ | **Headline:** median SER vs device passes, 6 arms + target/ceiling/budget lines, IQR bands, C-2 8 seeds | S0.5 |
| F5 ✅ | Ranking bars: device passes (per-seed dots) + digital side-ledger hatched; RHEL censored | S0.5 |
| F6 ✅ | Damping: pinned vs boxed curves, ceiling line, r*=2.0, plateau flags | S0.6 |
| F7 ✅ | (a) training-energy inversion (conversion OPT/CONS + PAT digital 13–44 J); (b) inference pJ/sample vs N at 2 GS/s vs 4 baselines | S0.7 |
| F8 ✅ | (a) mismatch sweep 5–30%: tie robust, m\*=none; (b) common-mode drift absorbed by re-lock; (c) independent drift: in-situ edge (made 2026-07-27, `analysis/make_sfigures.py`) | S0.9 |
| S-figs ✅ | S1 G3 dossier · S2 twin-mismatch C-1 · S3 echo chain+ceilings · S5 RHEL R1 recovery (all made 2026-07-27, `analysis/make_sfigures.py`); S4 = reserved slot (PR-14, deferred) | various |

## Writing order (Supervisor)

1. §2 mapping (closest to done — `docs/s0_1/mapping_result.md` is near-prose) →
2. §3 substrate (PR-4/PR-6 → prose) → 3. §1 intro (needs the white-space wording lifted
   verbatim) → 4. §4 methods specs → 5. §8 limits skeleton → 6. results sections as runs land.

Venue formatting deferred until Lucas picks (plan: arXiv first regardless).
