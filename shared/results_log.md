# Results Log

The **Executor** appends experiment results here (newest at top). The **Supervisor** reads and
evaluates them, then assigns the next task. The **Critic** reads this file to check claims against data.

Per result, report:
- **Phase / task** and **date**
- **Goal** — what this run tested
- **Config** — grid size, key parameters, seed count
- **Key findings** — numbered, with specific numbers
- **Gates** — passed / failed (vs the pre-registered criterion)
- **Anomalies / concerns** — anything surprising or fragile
- **Data path** — where the raw results live
- **Compute used** — where it ran, wall-clock, cost (if cloud)

---

## S0.7L-0 — PR-10 assumption sourcing (S0.7-lite step 0 of 2) (2026-06-10, Executor)

**Goal:** source the candidate assumption set for PR-10 (S0.7-lite envelope) with primaries, so the
Supervisor can draft the freeze ask for Lucas. **Sourcing only — the envelope was NOT run** (PR-10
stays ⬜ UNSET; running pre-freeze would un-preregister it).

**Config:** literature/datasheet task (no simulation, no compute spend). Four parallel web sweeps
(E/O–O/E energies; DAC/ADC; named digital baselines; SiN heaters + control electronics), 2026-06-09
→ 06-10, ~45 logged queries, ~35 primaries fetched (full text or abstract level); +1 internal
category (operating scale) cited to `docs/s0_1/mapping_result.md` §4 and the registry. Executor
first-hand re-verification of the two most load-bearing novel primaries (CORNERSTONE MPW#9 design
rules PDF; TI ADC12DJ3200 datasheet pp. 13–18) — **both exact-match** vs the sweep quotes.

**Key findings:**
1. **All five PR-10 categories sourced with quoted primaries**; 5 candidate brackets registered
   where sources disagree (E/O device vs incl.-driver spans ~2 orders: ~1 fJ/bit resonant →
   10–20 pJ/bit system; O/E 0.17 → several pJ/bit; ADC at GS/s 32 → 469 pJ/sample
   research-vs-vendor at 8.4–9.4 ENOB; DAC 5–9 → 308 pJ/sample; SiN P_π 60–385 mW/π standard
   vs ~1 mW/π suspended-at-ms-τ).
2. **Strong-baseline (F16) candidates named with author-stated perf/W:** Brainwave (batch-1 GRU on
   Stratix 10, 287 GFLOPS/W) the published high-water mark for streaming recurrent serving; MARCA /
   LightMamba the closest-workload SSM accelerators (LLM-decode-oriented, relative perf/W only);
   coherent-DSP ASIC class 25–170 pJ/bit as the GS/s streaming-FIR anchor; Jetson AGX Orin (275
   peak sparse TOPS, 15–60 W) the embedded-GPU representative.
3. **Four discrepancy flags vs prior project anchors (memo §6):** (i) the pnn-multilayer Ozkaya
   "20–50 mW standing power" attribution is unverifiable (verifiable record: 1.4 pJ/bit @ 64 Gb/s);
   (ii) the "~5 pJ/bit at 800G DSP" number has no primary (it was model-computed) — sourced bracket
   is 25–170 pJ/bit; (iii) measured stoichiometric-SiN P_π (60–385 mW/π, foundry bound <175) is far
   above silicon-derived intuition, and the ~1 mW regime needs undercut (not offered in the
   CORNERSTONE flow) at ms-class τ; (iv) Harris 2014 is actually 24.77±0.43 mW/π **silicon** —
   don't carry "20 mW" into PR-10 as SiN; the 2 mW/shifter trim convention is retroactively
   well-sourced (AD5380, 1.25–1.9 mW/ch).
4. **Lateral-trench vs undercut disambiguation is load-bearing** for the holding-power row:
   AN800-platform lateral trenches cut crosstalk (12%→2.5%) but barely change P_π; only
   undercut/suspension buys the ~20×–97% power reduction, at 0.4–2.6 ms τ (couples to SPSA cadence
   — the envelope must use one heater class consistently across its power and training-time rows).
5. **Operating-scale candidates bounded by S0.1** (no choices made): memory 329→4937 rt
   (3.29→49.4 ns), FSR 100 GHz registry-wide, single-carrier-one-FSR λ-plan (the validated S0.1
   regime; WDM would be an extension), linewidth-derived line-rate class ~0.1–2 GS/s,
   N ∈ [8…128] candidate bracket (S0.1 leaves N open — F8), ≈2–4 control channels/ring (B1).

**Gates:** every load-bearing number primary-sourced + quoted ✅ (verification legend per row;
unreachable primaries consolidated in memo §8, never presented as verified); brackets registered
where sources disagree ✅; **no envelope arithmetic** — exactly one illustrative sanity row,
labelled non-load-bearing (memo §7) ✅; search trail reproducible (memo §9) ✅.

**Anomalies / concerns:** IEEE Xplore (HTTP 418) and Optica (anti-bot interstitial) blocked several
full texts — abstract-level verification used and marked ◑; Analog Devices datasheets timed out
entirely (TI parts substituted as the named-vendor rows). The published SSM-accelerator field is
LLM-decode-centric — no GHz-sample-stream S4/Mamba hardware paper exists, so matched-accuracy
comparability for the closest-workload class will need care at the freeze. Buckwalter 2012 abstract
was reconstructed via OpenAlex word index (flagged in-memo for human spot-check if it becomes
load-bearing).

**Data path:** `docs/s0_7/pr10_assumption_sources.md` (candidate table + quotes + brackets + flags
+ trail).

**Compute used:** local only (web fetches); zero simulation/cloud spend.

---

## S0.L-1 — White-space existence search, debt #1 / PR-15 (2026-06-09, Executor)

**Goal:** run the PR-15-frozen existence search for verification debt #1 — is there ANY prior in
which internal recurrent parameters of a physical photonic system were updated on-device by a
gradient-based/-estimating rule? Kill-rule q1∧q2∧q3 applied **as frozen** (lanes locate, the rule
decides). This is modality (1) of the two-modality protocol; the Critic's independent adversarial
pass is separate.

**Config:** literature task (no simulation). Six parallel lane sweeps (PR-15 lanes i–iv + lane v
split into named-groups / free-forward), 2026-06-09, ~150 logged queries; **~60 candidates
examined**, ~45 primaries fetched in full or in part; Executor **first-hand re-verification of 7
decisive primaries** (Wu eLight 2025 incl. the complete supplementary, Zhou DPU 2021, Pérez-López
2020, Bueno 2018, Böhm 2022, Jayatilleka 2015, Yorke 2026) after WebFetch session-limited → curl.
Full reproducible trail in the memo appendix.

**Key findings:**
1. **No FATAL prior confirmed.** Nothing was confirmed to satisfy q1 (internal) ∧ q2
   (on-device-in-loop) ∧ q3 (gradient-based/-estimating).
2. **One potentially-fatal AMBIGUOUS — escalated (A1): Wu et al., eLight 5:7 (2025)** — first
   monolithic optical RNN chip; recurrence **physically closed on chip** (PD→MRM wavelength relay,
   no ADC/DAC in loop; "W is the feedback weight matrix"); loss "**minimized in-situ** using a
   stochastic parallel gradient descent algorithm" with Adam on "the current voltages U ± δ"
   (q2 ✓, q3 ✓, Executor-verified verbatim). **q1 unresolved:** the trained voltage vector U is
   never enumerated — main text and the complete supplementary (S1–S11 swept; S9 = iteration curves
   only) never state whether the W-mesh heaters are in U. Natural reading → FATAL; restricted
   (reservoir-style) reading also consistent. → Lucas with primary attached (archived in repo).
3. **One potentially-fatal-under-wording AMBIGUOUS class — escalated (A3):** in-loop
   gradient-style updates of pole-defining ring parameters / intracavity laser parameters with
   *device-quality* objectives — **Milanizadeh ECIO 2020** ("Automatic tuning … using gradient
   descent technique" on a 4th-order coupled-ring filter: q1∧q2∧q3 hold *mechanically*; only the
   reading of "training" excludes it), Jayatilleka 2015 (perturb-and-observe sign rule on ring
   detunings, Executor-verified), Mak 2015 (direct search), Pu 2019 (Rosenbrock on intracavity
   EPC), Yan 2021 (DDPG actions on intracavity EPC). The claim wording (PR-2) must settle the
   calibration/self-optimization boundary — escalated, not adjudicated.
4. **Other AMBIGUOUS — escalated:** Böhm 2022 (RBM weights gradient-trained in-loop but stored in
   the FPGA feedback path of an optoelectronic Ising machine — the PR-15-pre-listed "hybrid digital
   recurrence" type); **8 unreachable primaries** (highest priority: Zhao et al., Laser Photon.
   Rev. 2025 — "in-situ trained microring-based NNs" via optical backprop, Wiley-paywalled, no
   arXiv mirror; plus Shi LPR 2025, Nakajima ADI 2025, NUDT OL 2010, and 4 historical
   1985–1991 optical-NN texts whose reachable companions all indicate non-fatal).
5. **The non-fatal structure is clean and makes every PR-15 qualifier load-bearing** (33
   non-fatal-cites, 12 clears, all primary-quoted): physically recurrent photonic systems are
   readout/encoder-trained (Bueno/Brunner line 2018→2025 — boundary memo delivered: Boolean
   readout flips through 2021, SPSA/PEPG **on input+readout only** by 2025; Hermans physical-BP
   2015/2016 = masks only, with the 2015 primary admitting internal-parameter training was
   "omitted … for reasons of experimental simplicity"), or non-gradient-adapted (Lugnan 2025
   emergent PCM plasticity; Anderson-line photorefractive self-organization 1991/94; GA/ES
   mode-locking on intracavity params — Woodward 2016, Andral 2015), or offline-trained-deployed
   (Tait 2017 "programmed a priori"; Xu eLight 2025 RNN chip = the §10 offline-deploy baseline;
   Marquardt/López-Pastor RHEL = theory only, **no experiment through 2026-06**). In-situ
   gradient(-estimating) training on photonic *hardware* is now routine — but **only feedforward**
   (FICONN 2024 zeroth-order; Pai 2023 in-situ backprop; Xue 2024 FFM; Ashtiani Nature 2026
   on-chip BP; MGD 2025), with FICONN's own outlook deferring "recirculating waveguide meshes …
   trained in situ" to future work.
6. **Negative results logged:** no adaptive recursive/IIR photonic filter with in-loop
   feedback-tap adaptation (4 query formulations); no photonic equilibrium-propagation experiment;
   no photonic FORCE learning; no experimental Hamiltonian-echo demonstration; no 2024–2026 paper
   *claiming* an in-situ-trained recurrent photonic system in the claim's sense.
7. **Strategic context (not verdicts):** the white space, if it survives A1 adjudication, is
   visibly closing — A1's group (SPGD + on-chip recurrence), Skalli 2025 (SPSA/PEPG
   hardware-in-the-loop, one parameter-set from q1), MGD-on-weight-banks (NIST/Queen's 2025, one
   architecture from Tait-style recurrence), Pérez-López (hardware PSO on ring-bearing meshes +
   gradient synthesis in simulation, one recombination away), and Yorke arXiv 2026 (simulation
   concept paper squarely in the driven-dissipative in-situ-learning space).

**Gates (task spec):** every PR-15 lane swept + logged ✓ (memo §5 + trail); every non-clear verdict
grounded in a primary source with the load-bearing sentence quoted ✓ (unreachable ⇒ AMBIGUOUS,
never clear ✓); ambiguities escalated, never resolved in-memo ✓ (E-2026-06-09-3 /
D-2026-06-09-2); memo dated 2026-06 ✓; search trail reproducible ✓. **PR-15 PASS not issued — by
design**: PASS is one-sided *and* now waits on Lucas's adjudication of A1/A3a.

**Anomalies / concerns:** (a) WebFetch hit its session limit mid-verification — all Executor
re-verification completed via curl (trail A.7); (b) the eLight supplementary that 403'd for a
sweep agent was reachable with a referer header — fully swept; (c) ECIO server 403'd the Executor
re-fetch of Milanizadeh (quote stands as sweep-agent primary-fetch; same-class A3b verified
first-hand); (d) Wiley (Zhao, Shi) and SPJ (Nakajima) paywalls block three 2025 primaries — library
retrieval recommended before claim freeze; (e) minor: Bueno node count differs between published
abstract (2025 nodes) and arXiv v1 (2500) — memo cites the published figure.

**Data path:** `docs/s0_L/debt1_whitespace_search.md` (memo: verdict table §4, Bueno/Brunner
boundary memo §3, A1 analysis §2, reproducible trail App. A); primaries archived at
`docs/s0_L/primaries/` (Wu 2025 publisher PDF, CC-BY + extracted supplementary text).

**Compute used:** local + web only; six research subagents (~0.9 M agent tokens), ~25 min
wall-clock for the sweeps + ~45 min Executor verification/synthesis. **No cloud spend.**

---

## S0.1.1 — S0.1 closeout (Critic decision-free edits) (2026-06-09, Executor)

**Goal:** land the four **decision-free** items from `critic_review_s0-1-results.md` (APPROVE-WITH-EDITS)
before PR-1/PR-2 freeze. The two *framing* items (F2 mapping-class, F6 gain-free κ_ext) are
Supervisor/PR-2 work and are **out of scope** here (await Lucas's D-08-2/D-08-3 steer).

**Config:** local CPU, torch 2.11.0, float64; scipy 1.17.1 added **test-only** (independent RK45). Test
count **99 → 107** (4 new transient tests; +4 from the registry growing 6→7 entries across the three
parametrized registry tests and the split AN800-reconciliation test). No methodology/scope change.

**Key findings / what landed:**
1. **(F1, HIGH) Transient-dynamics validation** (`tests/test_transient_dynamics.py`, new). The S0.1 gate
   proved the mapping by *construction* (van Loan exact + steady-state + pole algebra); this adds the
   missing *time-domain forward-integration* check against an **independent** scipy RK45 of
   `da/dt = M a + B u`: (i) single-ring **ringdown** matches the closed form `a₀e^{(iδ−κ)t}` (<1e-9) and
   RK45 (<1e-6), with the decay rate κ **and** oscillation frequency δ **fitted from the trajectory**
   (log|a| slope, unwrapped-phase slope) recovering the pole to <1e-5; (ii) **step response** tracks RK45
   and settles to `a_ss=Bu/(κ−iδ)` (<2e-3); (iii) a **2-ring μ≠0** case whose population-beat angular
   frequency (envelope-corrected FFT) **matches the Im(eig(M)) supermode splitting = 2μ** to <2%, with a
   μ=0 no-beat contrast. *Positive time-domain confirmation of the dynamical mapping — the contribution.*
2. **(F3, MED) Memory-units slip fixed (prose).** The code already distinguished amplitude memory
   `1/κ_i` from the photon-energy lifetime `Qi/ω₀` (= half); only the prose conflated them. Now reported
   in the **amplitude/state-memory** convention consistently: **3.29 ns / 329 round trips** (Qi=2e6) →
   **49.4 ns / 4937 rt** (Qi=3e7) — what PR-2 sizes the task against. (The earlier 1.65/24.7 ns were the
   photon lifetimes.) Fixed in `mapping_notes §4` + finding 4 below. No code change.
3. **(F4, MED) B2 high-roughness row + criterion band.** The row mixed a 160-MHz `Q_cross=3.0e5` with
   125-MHz ratios (5.2/77.6); recomputed to **one γ (160 MHz)** → the consistent **6.6 / 99**. Added the
   criterion band: the registered `2γ ≳ κ_tot` is the **conservative HWHM** choice; the fully-resolved
   **FWHM** `2γ ≳ 2κ_tot` shifts every `Q_cross` **×2** (band tabulated). **Conclusion unchanged** under
   both (clean holds at foundry / breaks by ~4–8e6; rough splits at foundry). The analysis JSON already
   used the consistent γ — only the doc table is corrected; JSON ↔ doc now agree.
4. **(F7, MED) Registry mislabel fixed** (`platforms.py`). The Qi=2e6 conservative corner is **renamed
   `SiN_foundry_conservative`** (no product attribution; still the Gate-ii/F13 candidate cell). A
   **separate `SiN_LIGENTEC_AN800`** now carries the *demonstrated* numbers — 0.051 dB/cm **primary**
   (q_basis="loss"), **Qi=6.80e6 derived** as the propagation ceiling at n_g=1.97 (reproduces the
   primary-sourced pair). Registry now spans 4 SiN corners (2.3e5 → 2e6 → 6.8e6 → 3e7); loss↔Q + FSR
   tests re-run green over all 7 entries.

**Gates (all PASSED):** transient tests pass (decay rate **and** frequency in the time domain; 2-ring
beat == eig splitting); **107/107 suite green** (~3.6 s); memory prose in one (amplitude) convention; B2
row internally consistent + criterion band stated; registry relabeled + tests green.

**Anomalies / honest flags:**
- **Step-test scaling (not a defect):** with a unit input the steady state is ~2e-11, so model↔RK45 agree
  to ~1e-15 *absolute* but the *relative* error is atol-floored; the test drives the state to O(1)
  (`b=|κ−iδ|`) so the tolerance is meaningful. Documented in-test.
- **n_g=1.97 for AN800** is chosen so the demonstrated 0.051 dB/cm reproduces the demonstrated Qi=6.8e6
  (both primary-sourced for the same ring); a defensible AN800 group index, used only for FSR/radius
  bookkeeping. The conservative corner keeps n_g=1.95.
- **B2 primary-source verification (F5) is NOT done here** — it is S0.L/before-paper (out of scope); the
  ⚠️ verify-before-citing caveats remain in the memo.
- Framing items **F2** (diagonal/S4D mapping-class) and **F6** (gain-free κ_ext) deliberately untouched —
  Supervisor/PR-2, pending the D-08-2/D-08-3 steer.

**Data path:** code+tests in repo; `docs/s0_1/{mapping_notes,B2_backscatter_bound}.md` updated; figures +
JSON regenerated under `results/s0_1/` (git-ignored). **Compute:** local CPU, ~3.6 s tests + <1 s analysis.

---

## S0.1 — Oscillator↔SiN-ring mapping + realizable pole region (2026-06-08, Executor)

**Goal:** build the first **new dynamical core** — the temporal-CMT single-ring model + the coupled-ring
→ N-oscillator LinOSS forward model (not the salvaged static/CW transfer); bound the realizable pole
region (§4); deliver the three scope-(B) results (B1 actuation map, B2 backscatter bound, B3 κ_ext
trade) + the F13.1 registry Q/loss fix. *Model + plots + data only; the formal mapping write-up +
white-space wording are the Supervisor's.*

**Config:** local CPU, python 3.12, torch 2.11.0, float64. New package `photonic_ssm/dynamics/`
(torch-only, hygiene test extended over it). 99 tests (60 from S0.0 + **39 new**). Figures/data via
`analysis/s0_1_pole_region.py` (matplotlib, outside the package).

**Key findings / deliverables:**
1. **Dynamical single-ring temporal-CMT model** (`dynamics/single_ring.py`):
   `da/dt = (iΔ − κ_tot)a + √(2κ_ext)·s_in`, pole `s = −κ_tot + iΔ`, identified with `a_i = −e^{α_i}+iβ_i`
   (`e^{α_i}=κ_tot`, `β_i=Δ`). All-pass + add-drop ports; energy-conserving (lossless `|t|=1`; add-drop
   `|t_t|²+|t_d|²=1` to 1e-16).
2. **CW-limit GATE — PASSED.** Pre-registered: CW limit recovers the S0.0 salvaged statics with
   **O(1/finesse)** error, <1% at finesse ≥1000. Measured: single-bus **4.5e-4 @ F=1048 → 4.4e-5 @
   F=10473** (exact 10×/decade); add-drop through+drop **3.4e-4 → 3.4e-5**. CMT through `= −`salvaged
   single-bus (the documented −1 phase convention). SiN rings sit at F≈1000 (Qi=2e6) → 15000 (Qi=3e7).
3. **Coupled-ring → N-oscillator LinOSS forward model** (`dynamics/coupled_rings.py`,
   `CoupledRingLinOSS`): `M = diag(−κ_tot+iδ) + iΩ`; recurrent params `{log_kappa_tot, delta, mu}`
   (= the trainable recurrence). ZOH van-Loan matrix-exp discretization is **exact** for PWC input
   (discrete poles `= e^{λ dt}` to machine precision); uncoupled poles match `−κ_tot+iδ` <1e-3.
   **Both architecture constraints honored in the NEW model (not inherited):**
   **(3a)** a last-step loss receives gradient through the ring state from the t=0 input (49 steps back),
   all recurrent-param grads finite; the rollout uses no `no_grad`/`detach` (source-grep test).
   **(3b)** `forward` returns the full trajectory x₀..x_T. Gradient-**checkpointed** chunked rollout
   (the `TrainingAwareDynamicSOAPerMode` pattern) is **bit-identical** to the plain rollout in outputs,
   states, AND all gradients (0.0).
4. **Realizable pole region (§4)** (`dynamics/pole_region.py` + `results/s0_1/pole_region_memory.png`):
   stability free; memory **loss-limited** — passive amplitude memory **3.29 ns / 329 round trips**
   (Qi=2e6) → **49.4 ns / 4937 round trips** (Qi=3e7), a **15× gain** (amplitude/state memory `1/κ_i`;
   the photon-energy lifetime is half — 1.65/24.7 ns — corrected S0.1.1/F3); gain pushes `|λ|→1` (plotted at
   net gain 0/50/90 % of loss); `β` FSR-bounded (`|β·dt|≤π`). Coupling hybridizes poles conserving
   `Σ Re(λ) = −Σκ_tot`.
5. **(B1) Trainable-parameter + actuation map** (`docs/s0_1/B1_actuation_map.md`): the in-situ-trainable
   recurrence = `{δ_j` (heaters)`, κ_tot,j` (tunable couplers and/or per-ring gain)`, μ_jk` (ring–ring
   coupling)`}`; residues/B,C (MZI mesh) train-only = the reservoir baseline (explicitly excluded from
   the claim). A **gain-free Stage-1 minimal set already suffices** for the white-space claim. → PR-2.
6. **(B2 / F19) Backscatter bound — "SAY IT LOUDLY"** (`docs/s0_1/B2_backscatter_bound.md` +
   `backscatter_crossover.png`): literature pull (8 SiN-anchored cites) shows splitting is
   **process-roughness-limited, NOT cleanly Q-gated** — *contradicting the roadmap's "negligible at
   foundry Q" assumption.* Crossover (2γ=κ_i): **damascene-clean Q_cross=4.1e6** (foundry single-pole OK,
   3e7 splits 7.3×); **rough subtractive Q_cross=3–5.4e5** (splits 21–75 % of modes already at foundry
   Qi=2e6). **Recommend** S0.3 carry an *optional CW/CCW splitting knob gated by a process-roughness
   flag* (default OFF only for the clean foundry corner). → flag D-2026-06-08-3.
7. **(B3 / F13.3) Memory-vs-readout-SNR (κ_ext) trade** (`docs/s0_1/B3_kappa_ext_tradeoff.md` +
   `kappa_ext_tradeoff.png`): undercoupling maximizes memory but collapses readout residue + drop
   efficiency; `memory × residue ≤ passive memory` (bounded, tested). At Qi=2e6: 274 rt / 0.028 drop-eff
   (kext=0.1κ_i) → 16 rt / 0.91 (kext=10κ_i). κ_ext also couples to B2 (overcoupling hides the doublet).
   → PR-4 (I characterize; I do not pick the operating point).
8. **(F13.1) Registry Q/loss self-consistency fix** (`platforms.py`): added `q_basis` (Qi|loss|
   independent) — each entry registers a primary, derives the partner. **Conservative corner reconciled**
   (then named `SiN_LIGENTEC_AN800`; **renamed `SiN_foundry_conservative` in S0.1.1/F7** — the 2e6 corner
   is not the AN800 product): Qi=2e6 primary (foundry corner), loss 0.03→**0.172 dB/cm** (the 0.03 implied
   Qi=1.14e7, 5.7× off). CORNERSTONE
   loss-primary (Qi=2.347e5 derived); damascene Qi=3e7 primary (loss 0.0123 dB/cm derived). New
   `loss_q_ceiling_ok` invariant (Qi ≤ propagation ceiling) holds for all 6 entries; SiN entries on the
   ceiling (err ≤2e-5). **Operating Q still NOT chosen** (D-2026-06-08-1 / PR-4).

**Gates:** **S0.1 gate PASSED** — dynamical poles match the CMT/transfer reference (uncoupled <1e-3,
discrete `|z|` <1e-9, ZOH exact), and the CW limit recovers the S0.0 static reference (O(1/F), <1%).
(3a)/(3b) confirmed in the new model. All 99 tests pass (~1.4 s).

**Anomalies / honest flags:**
- **B2 contradicts a roadmap assumption** (splitting bites at foundry Q for rough process) — surfaced
  loudly per the task's instruction; recommendation made, decision left to Supervisor/Lucas
  (D-2026-06-08-3).
- **Mapping subtlety flagged (D-2026-06-08-2):** one optical ring = one *complex* pole (diagonal complex
  SSM / S4D), whereas a real LinOSS oscillator is a conjugate *pair*. Both supported; the PR-2
  architecture choice is the Supervisor's.
- **B2 verify-before-citing:** the 63 MHz Pfeiffer figure + some author lists came via search-aggregation
  — flagged in the memo for primary-source confirmation before proposal use (no published γ for AN800/
  CORNERSTONE specifically; the crossover curve is assembled from bracketing SiN points).
- The proposal's schematic `√κ_ext s_in` vs the energy-conserving Haus `√(2κ_ext) s_in` — same model,
  factor-2 naming; documented in `mapping_notes.md §1` for the write-up.
- Per-round-trip ASE inside the rollout remains S0.3 (the single-ring/coupled model here is the clean
  linear-optical forward model, as scoped).

**Data path:** code+tests in repo; figures + JSON under `results/s0_1/` (git-ignored, regenerable via
`python3 analysis/s0_1_pole_region.py`); memos under `docs/s0_1/`. **Compute:** local CPU, ~1.4 s tests
+ <1 s analysis.

---

## S0.0 — Repo init + selective salvage + smoke test (2026-06-08, Executor)

**Goal:** stand up the Project_SSM repo under git; salvage the 7 manifest assets
(`shared/tooling_recon.md` §4) with provenance headers, decoupled contact points and passing ported
tests; prove the toolchain with the salvage-validation smoke test. No SSM core (that is S0.1+).

**Config:** local CPU, python 3.12.3, torch 2.11.0+cpu. Source `~/Documents/pnn-multilayer` @
`e2eec80` (read-only, untouched). New package `photonic_ssm/` (torch-only runtime, enforced by a
hygiene test); 60 tests.

**Key findings / deliverables:**
1. **Repo:** `git init` (D-2) → 2 commits: `a6de34f` (docs/coordination snapshot), `19e64d4`
   (salvage + tests). `.gitignore`, `requirements.txt` (torch-only + pytest), `README.md` with the
   salvaged-vs-new table and the two architecture constraints.
2. **All 7 assets ported** with `# salvaged from pnn-multilayer @ e2eec80 : <path>` headers:
   `platforms.py`, `gain.py`, `dynamic_gain.py`, `static_rings.py`, `estimators/spsa.py`,
   `baselines/ridge_readout.py`, `runner/` (pattern-salvage per manifest). **60/60 tests pass**
   (~1.3 s).
3. **Decoupling points** (exactly the recon's predictions; nothing resisted lifting):
   SPSA — hard-coded `compute_nmse_field` → injected `loss_fn`, `model.forward_batched` → injected
   `forward_fn`; ridge readout — severed from the MRR cascade + PAM-4/sps framing, now consumes
   arbitrary `[T, F]` state trajectories; static Lorentzians + drift — de-classed from the
   `BaseMRR`/nn.Module lifecycle to pure functions; gain/dynamic-gain/platforms — none needed.
4. **Smoke gates (all pass, pinned numbers):**
   (i) all salvaged assets import; full suite green.
   (ii) salvaged single-bus Lorentzian == analytic add-drop through-port in the κ₂→0 limit
   **exactly** (max err 0.0 at float64, after the documented −1 phase-convention factor); add-drop
   references self-validate: lossless |T_t|²+|T_d|² −1 ≤ 1.6e-15, critical-coupling extinction
   < 1e-14.
   (iii) FSR self-consistency: worst |tabulated−derived| = 1.2e-05 GHz over 6 registry entries
   (tol 0.01).
   **SPSA FD-vs-autograd anchor reproduced after decoupling: RMS rel err = 1.1e-07** (inherited
   gate < 1e-2) on a float64 toy model built from salvaged primitives; SPSA+Adam drives a 12-dim
   quadratic 0.81 → <5e-7 in 400 updates = 800 physical forward passes (`n_forward_equivalents`
   accounting verified exact: 2/update SPSA, 2N+1/update FD).
5. **Architecture constraints baked in + enforced by tests:**
   **(3a)** gradients flow through the optical state — `test_gradient_flows_through_state_and_params`
   proves a last-symbol loss receives gradient from inputs ~5 symbols earlier *through the carrier
   memory* of `TrainingAwareDynamicSOAPerMode` (the reference pattern); checkpointed vs
   non-checkpointed rollouts agree in outputs AND grads to <1e-10; the forward-only eval classes are
   documented as eval-only and tested to build no graph.
   **(3b)** full-state-trajectory exposure — encoded as the API contract (`ReservoirReadoutBaseline`
   consumes `[T, F]` trajectories; requirement documented in the package docstrings); the actual
   substrate API that honors it is S0.1/S0.3 work.
6. **Platform registry extended, operating Q deliberately NOT chosen** (parked D-2026-06-08-1):
   added `SiN_CORNERSTONE_300` (1.5 dB/cm C-band per the CORNERSTONE platform paper, Littlejohns
   2020; Qi=2.3e5 *derived* from loss — no published ring Q; n_g=2.0 flagged as estimate) and
   `SiN_damascene_UHQ` (0.01 dB/cm / Qi=3e7, Liu et al. Nat. Commun. 12, 2236 (2021); internally
   consistent: loss-implied Qi=3.7e7). Registry now spans Qi 2.3e5 → 2e6 → 3e7.

**Anomalies / honest flags:**
- The task's smoke item (ii) presumed the salvaged Lorentzian was add-drop; **the source repo has
  only the single-bus (all-pass) form** — no two-coupler add-drop transfer exists anywhere in
  `pnn-multilayer`. The analytic add-drop references are therefore NEW code (clearly marked, in
  `static_rings.py`), validated against textbook properties, with the salvaged form checked against
  their exact κ₂→0 limit. S0.1's CW-limit gate gets both references.
- **Inherited registry tension, input to D-2026-06-08-1:** `SiN_LIGENTEC_AN800` tabulates Qi=2e6
  (foundry quote) alongside 0.03 dB/cm, but 0.03 dB/cm *implies* Qi≈1.14e7 — the entry's Q and loss
  are independently sourced, not mutually consistent. The two new entries are internally consistent.
- Dynamic gain classes still have **no ASE inside the rollout** (only the instantaneous
  `soa_activation_with_ase` has ASE) — per-round-trip ASE accumulation is new S0.3 physics, as the
  recon flagged.
- No equalization assumptions survived: enforced by a ported negative source-grep test
  (`test_no_equalization_coupling.py`) — zero references to the equalization stack, zero non-torch
  third-party imports in the package.
- The sweep-runner mp test uses the `fork` context (`spawn` requires importable job functions;
  production drivers keep the torch-safe `spawn` default with their own top-level job fns).
- `shared/critic_review_stage0-roadmap.md` (Critic, parallel track) appeared during the task and is
  committed with the coordination state in `19e64d4`; not read/acted on by the Executor.

**Gates:** all S0.0 gates **PASSED** (7/7 assets ported + tested; anchor reproduced; constraints
honored; smoke i–iii green).

**Data path:** code+tests in repo (commits `a6de34f`, `19e64d4`); no experiment data generated
(infrastructure task). **Compute:** local CPU, total test wall-time ~1.3 s.

---

**S0.0a — Tooling recon (2026-06-07, Executor):** report at [`shared/tooling_recon.md`](tooling_recon.md) — `equalization_ringbank.py` is **not** a head start for the S0.1 mapping (all `pnn-multilayer` ring code is static/CW transfer functions; the dynamical CMT core is new code either way), but SPSA + pass-accounting, rate-equation gain (autograd-checkpointed), SiN platform registry, drift machinery, ridge readout and sweep scaffolding are liftable → recommendation: **(a) selective salvage** (≈1 day port vs ≈3–5 days extra for clean start). Read-only; no code written. Awaiting Lucas's D-1/D-2 rulings.
