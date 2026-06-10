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

## S0.3-0 — Substrate design recon + PR-4 input sheet: **debt #3 premise FALSE (flagship NF measured = 7 dB)** · menus complete (2026-06-10, Executor)

**Goal:** every input the PR-4 freeze needs, as [EV]-sourced menus (menu-not-choice; zero
substrate code; zero training runs): (1) debt #3 — Er:Si₃N₄ NF; (2) D-08-1 candidate (α,Qᵢ)
pairs + the EV-F3 N=128 packing check; (3) D-08-3 roughness/splitting evaluated at operating
κ_ext + knob policy; (4) gain-stage physics inventory (lifetime vs registered clocks); (5) the
PR-4 input sheet (noise cells, κ_ext policy, EV-F1 holding convention, PF-F8f normalization).
**Sequencing note:** per the task header, the S0.2-1 G3 gated-5 runs were launched FIRST
(D-2026-06-10-2 ruling: local, 3-parallel; see the S0.2-1 addendum below) — this recon ran
while they compute.

**Config:** literature/design task (no simulation, no seeds). 3 parallel web subagents
(flagship exhaustive + post-2022 scan; NF comparables ×6 classes; gain-dynamics timescales) +
Executor first-hand fetches ×4 (arXiv 2204.02202v2, 2511.02198v1, 2412.07627v2, 2108.08044) with
string-exact grep verification of every decisive number; arithmetic kernel
`analysis/s0_3_0_recon_arithmetic.py` reusing the S0.1 `pole_region` conventions (**all
registered anchors reproduced exactly**: foundry 329.1 rt / 0.33/3.29/6.58 samples; UHQ 4937 rt
/ 4.94/49.4/98.7; B3 ladder 274→16 rt + drop efficiencies; B2 undercoupled ratios 0.49/3.7/6.6;
EV-F3 packing 10.3 vs 155 poles/GHz).

**Key findings:**
1. **Debt #3's premise is FALSE at retrieval level [EV, three-way verified].** The flagship
   (Liu et al., Science 376, 1309 (2022) / arXiv:2204.02202, v1≡v2 by LaTeX diff) **measures**
   its NF: main text *"A noise figure of ca. 7 dB is measured at net gain of >20 dB, limited by
   coupling losses"*; SI Note 13 worked example **7.1 dB** (source-subtraction method,
   fiber-referenced, fwd 1480 nm pump). Attribution in-text: input fiber-chip coupling
   (2.9 dB/side @1550) + 1480-pump n_sp (incomplete inversion). Corroborated by the group's own
   2024 system paper (arXiv:2412.07627: "...demonstrated on these EDWAs so far (7.1 dB)") [EV].
   **Post-2022 scan: no other Er:Si₃N₄ NF exists through 2026-06** (295 citing papers screened;
   multi-lane OFC-2024 paper gain-only). The debt dies as worded; what survives: no
   *intrinsic/on-chip* NF decomposition exists. → PR-4 NF menu anchors on a measured number.
2. **NF comparables bracket [decisive rows EV]:** nearest measured integrated-Er hosts span
   **4.49–6.5 dB** (Er:LNOI 4.49 [EV re-grep] and ~5 f2f; Er:Al₂O₃ 6.5/min 5.6 (OE 2025);
   EDWA commercial 4.5; EDFA record 3.1; Caves 3 dB floor fetched). **Two draft assumptions
   killed by the sources** (recorded in the memo): Mu et al. "NF 3–4 dB" untraceable to any
   reachable primary; Frankis Er:TeO₂:SiN has NO NF (full-text zero occurrences). → menu cells
   NF-A 7.0 (as-measured) / NF-B 5.0 (comparable class) / NF-C 3.0 (floor, aspirational label).
3. **(α,Qᵢ) pairs + EV-F3 on numbers:** 4 self-consistent registry corners + 1 new candidate —
   **Cui et al., Adv. Photon. Nexus 2(4) 046007 (2023)** identified as the probable primary of
   the registry's AN800 pair [AV — body JS-walled, **verify at freeze**] AND itself demonstrating
   **0.033 dB/cm / mean Qᵢ≈10.8 M on the standard AN800 open MPW** (multimode racetrack,
   FSR 65 GHz — caveats logged). Packing: **N=128-in-band is realizable ONLY at the
   class-leading pair at r ≲ 1** (155→52 poles/GHz) — exactly its split regime → the EV-F3
   three-way coupling is really **two-against-one** (memo §2b; only knob-ON N=128 survives,
   input sheet §6.1). N=8 ✓ at foundry; N=32 needs ≥AN800-class.
4. **Splitting at operating κ_ext (D-08-3 evaluation) reorders the corners:** foundry+sub-low
   rescued by r≈3 overcoupling (3.72→0.53); **AN800 marginal-split even clean-process
   undercoupled (1.66)** — the blessed knob default "ON except clean-damascene" **confirmed,
   sharpened: AN800 never qualifies for OFF**; UHQ un-splits only at r≥3 (memory 4937→705 rt =
   14.1 samples @2 GS/s, still ≥ T-A's 7-tap). Subtractive statistics now first-hand [EV]:
   arXiv:2511.02198v1 Table 2 read directly (splittings 180–320 MHz, prevalence 21–75 %, Qint
   0.90(7)–2.8(2) M) — B2's row exact; its ⚠️ discharged at the numbers level (F5 stays S0.L).
5. **Gain regime (task 4): Er is rigorously quasi-static at every registered clock.** Flagship
   measured τ = 3.4 ms [EV]; per-symbol ripple suppression 2×10⁻⁸–5×10⁻⁷ (low-pass) AND
   E_sym/E_sat ≈ 5×10⁻⁶–9×10⁻⁵ at 1 mW drive (E_sat ≈ 108 nJ from the measured −15 dBm
   saturation power [EV]) — both criteria, with the Bononi&Rusch avalanche caveat handled by
   the stationarity of the registered task streams (memo §4b). Comparables fetched: silica
   10.5–12 ms, Al₂O₃ 7.6 ms, LNOI 2.3 ms; SOA 50 ps/0.1–1 ns contrast. **→ M1/M2/M3 gain-model
   menu; ⚠️ METHODOLOGY FORK flagged (memo §4e): under the SiN-native M1 the in-loop physics is
   LINEAR + static gain + ASE — the substrate's task-solving nonlinearity is the readout |·|²
   (the PF-F1 structure). Supervisor/ledger names the registered regime (M1 vs III-V M3).**
6. **New feasibility row — gain budget (memo §4f):** flagship gain coefficients (1.0–1.9 dB/cm
   [EV]) × ring circumference vs per-rt loss: closes ×5.8–11 at the foundry corner (×1.9–3.7 at
   r=1), **marginal-to-infeasible at CORNERSTONE** (×0.7–1.3 unloaded) — a CORNERSTONE cell is
   passive-only; 50/90 % compensation conventions need P-FND or better.
7. **PR-4 input sheet delivered** (`docs/s0_3/pr4_input_sheet.md`): 3 assembled noise cells
   (C-1 foundry-deployable Gate-ii candidate / C-2 demonstrated-mid / C-3 aspirational) +
   sensitivity axes; ASE conventions A1/A2 (equivalent at O(10⁻³) here; steady-state intracavity
   ASE ≈ 23 photons at NF-7/90 %-comp, corner-independent — derivation in-sheet); κ_ext policies
   K1–K4 with the per-cell arithmetic vs the frozen PR-2 cells (T-A 7-tap dies at foundry under
   ANY loading — passive is already the marginal 6.58; PR-13 k-cells tabulated); splitting knob
   policies K-pol-1/2/3; holding conventions H1/H2/H3 (EV-F1); **PF-F8f mechanisms O1
   (bus-power budget) / O2 (intracavity-energy budget — the only K4-clean option) / O3 (bounded
   trainable pre-gain)**; joint-adjudication notes incl. D-08-1 closure inputs.

**Gates:** [EV]/[AV]/[ABS] discipline with verification trail ✅ (memo Appendix A; every
decisive number Executor-re-grepped or carrying named fetch provenance); menu-not-choice ✅ (no
value selected anywhere); **zero substrate code** ✅ (the kernel imports existing modules only);
**zero training runs** ✅; every menu row carries provenance + sizing arithmetic vs registered
values (PR-10 grid/N-grid, B1/B3, frozen PR-2 T-A/PR-13 cells) ✅; no frozen-block edits ✅.

**Anomalies / concerns:** (i) **the debt-#3 premise itself was wrong** — proposal v0.5's
verification-debt list carried a claim that dies at first full-text contact; S0.8 must reword
debt #3 (Supervisor; suggested sharpened form in memo §1a) and this is a process datum for the
other debts (#4 "recurrent-adjoint gap" is the same inferred-absence type); (ii) the registry's
AN800 pair "primary-sourced" claim had **no recorded citation in-repo** — probable primary now
identified (Cui 2023) but its body is unfetched [AV] → verify at the PR-4 freeze; (iii)
`mapping_result.md` §4 "~33 rt" CORNERSTONE prose vs 38.6 rt registry-consistent (rounding
legacy; non-load-bearing; frozen text untouched); (iv) Science published full text unreachable
(403) — flagship quotes rest on arXiv v1≡v2 (submitted ms incl. SI); residual wording risk on
the published PDF only; (v) the Er-regime fork (finding 5) — left open BY DESIGN for the
Supervisor/ledger; S0.3-1 must not start before it's named.

**Data path:** `docs/s0_3/substrate_recon.md` (tasks 1–4 + Appendix A trail);
`docs/s0_3/pr4_input_sheet.md` (task 5); `analysis/s0_3_0_recon_arithmetic.py` +
`results/s0_3/s0_3_0_recon_arithmetic.json` (full ladders/all corners).

**Compute used:** local + web only; 3 research subagents (~300k agent tokens, 169 tool calls,
~15 min each) + 4 Executor primary fetches; arithmetic seconds-class; **zero simulation, zero
cloud spend**. (Machine concurrently running the S0.2-1 G3 gated-5 at 18/20 threads —
untouched by this task beyond health checks.)

---

## S0.2-1 — In-house LinOSS-IM layer + Gate-i runs: **G1 PASS (72.9032% ≥ 72.1%)** · G3 HELD on runtime flag D-2026-06-10-2 (2026-06-10, Executor)

> **ADDENDUM 2026-06-10 (eve): G3 gated-5 LAUNCHED per the D-2026-06-10-2 ruling** (local,
> gated-5 first, 3-parallel × 6 threads; cloud declined). Seeds 2345/3456/4567 in flight since
> 18:48 (5678/6789 queued behind the wave); detached via setsid so the runs survive session
> closure. Config records verified: param counts 133,765 / 134,279 (= published), official
> splits 165/35/36 (N=236 post-dedup), data sha match, frozen protocol unchanged. Driver log
> `results/s0_2/gate_i/logs/EigenWorms_gated5_driver.log`; launcher gained a `SEEDS_OVERRIDE`
> env knob (logistics only — zero protocol content). ETA ~3–4 days; per-seed table + the joint
> Gate-i verdict will be appended here when they land; annex-3 trails at idle after the verdict
> (PF-F8g: non-gating).
> **PAUSED 2026-06-10 19:36 by Lucas** (~47 min in, before the first eval record), then
> **MOVED TO CLOUD same evening per Lucas (E-2026-06-10-5** — his own vast.ai credits, ceiling
> $7.44; the D-2 option-2 standing offer exercised). **GPU PARITY GATE: PASS** on the rented
> box (RTX 3090, instance 40443827, $0.245/h, torch 2.12.0+cu126, TF32 off, deterministic):
> full-model probs GPU↔CPU **1.2–1.5e-7** (same magnitude as the CPU↔JAX record), BN stats
> 0.0/1.5e-8, L=17,984 layer 3.8e-6, 20-step train **bit-deterministic** → the chain GPU-torch
> ≡ CPU-torch ≡ official-JAX is closed (`scripts/parity_gpu_side.py`; box log
> `logs/parity_gpu.log`). Gated-5 launched sequentially on cuda (same frozen protocol, CPU RNG
> streams, identical seeds/splits/configs). The paused local workers were then killed (partial
> state discarded — protocol-clean; nothing reused) and their config-only JSONLs removed.
> First instance (40442878) had dead proxy-SSH, destroyed at ~$0.06 sunk. Per-seed table +
> joint verdict + $ actuals follow when the runs land.
>
> **G3 MEASUREMENT COMPLETE 2026-06-10 (late eve) — GATE FAIL. Diagnosis per the frozen
> gate-miss rule in flight; NO tuning performed or planned.**
>
> | seed | test-at-best-val | best val | steps | reading |
> |---|---|---|---|---|
> | 2345 | **0.1944444477558136** | 0.1714 | 12k | **collapsed — chance (5-class)** |
> | 3456 | 0.8888888955116272 | 0.9143 | 15k | healthy |
> | 4567 | 0.9444444775581360 | 0.9143 | 18k | healthy |
> | 5678 | 0.9722222089767456 | 0.9429 | 13k | healthy |
> | 6789 | **0.5555555820465088** | 0.4286 | 12k | **partial collapse** |
>
> **Unrounded gated 5-seed mean = 0.7111111223697663 = 71.1111 % < 90.6 % → G3 FAIL** (and
> joint Gate i FAIL: G1 PASS ∧ G3 FAIL). Healthy-3 mean **93.52 %** — inside the published
> 95.0±4.4. Per PR-1 on a miss: **stop — do not tune; divergence diagnosis vs the official
> repo** (the sanctioned cross-check). Diagnosis so far (all on the box, GPU, deterministic):
> 1. **Mechanism identified and reproduced bit-exactly:** the official objective
>    `−Σ y·log(softmax + 1e-8)` (their train.py line 87, ported verbatim per the closure rule)
>    has a **zero-gradient absorbing state** in fp32 — once softmax fully saturates on a wrong
>    class, p_true underflows to exactly 0 and the epsilon makes the total gradient exactly
>    0.0 forever. Step-instrumented: seed 2345 enters at **step 1** (step-0 |grad| ≈ 4×10³,
>    then |grad| ≡ 0.0); seed 6789 at step 4 (frozen at its step-4 accuracy → the 55.6 %).
> 2. **Incidence in our (framework-inherent, declared) RNG stream: 4 of 8 protocol seeds**
>    trap within 600 steps (2345@1, 6789@4, 7890@7, 8901@1; 3456/4567/5678/9012 alive). The
>    600-step diagnostic reproduces every gated outcome exactly (determinism verified).
> 3. **Init audit clean:** every parameter group's init distribution matches the official
>    (eqx Linear lim = 1/√in for weight+bias = our `_init_linear`; A/steps U[0,1), B ±1/√H,
>    C ±1/√ssm, D N(0,1)) — weight-transplant parity is blind to init bugs by construction,
>    so this was checked line-by-line against models/LinOSS.py + eqx 0.11.4 source. Only the
>    stream BITS differ (declared framework-inherent in this entry's original config note).
> 4. **Official-repo cross-check IN FLIGHT** (the decisive evidence): the official JAX code —
>    pinned commit 05a8353, jax 0.4.28 / eqx 0.11.4 / optax 0.2.2 (the S0.2-1 reference-venv
>    pins), official pickles, their own run_experiment.py, one config copy with seeds
>    reordered [2345, 6789, 3456, 4567, 5678] — training on the same GPU. If the official
>    stream also traps → published-anchor anomaly (escalate to Lucas). If clean → the
>    absorbing state is a shared property of the official objective entered stochastically
>    per-stream; the gate-semantics adjudication (PR-1, stream-sensitive anchor) goes to the
>    Supervisor/Lucas via decisions_needed.md. Note for that reading: the official code sets
>    no matmul-precision flags → jax default (TF32-class on Ampere GPUs) vs our strict-fp32 —
>    rounding-noise difference only; the fp32 softmax underflow threshold is identical.
> Spend so far ≈ $0.8 of the $7.44 ceiling (incl. all diagnosis runs).

**Goal:** implement the in-house recurrence layer (the bake-off object downstream), validate it,
and reproduce the two frozen PR-1 anchors under the exact Walker protocol. Gate i (PR-1 verbatim):
G1 Heartbeat unrounded 5-seed mean ≥ 72.1% **AND** G3 EigenWorms ≥ 90.6%. Rider first (PF-F1
premise re-verification, retrieval level). **Status: G1 complete (5 gated + 3 annex seeds) — PASS.
G3 not started — held on the pre-registered >24 h runtime flag (D-2026-06-10-2), awaiting the
Supervisor's compute-logistics ruling. Zero protocol deviations; no tuning anywhere.**

**Config:** PR-1 frozen values only — G1: lr 1e-3, hidden 16, state 16, blocks 6, batch 32;
num_steps 100,000, print_steps 1,000, T=1, time-channel on, IM discretization, learnable
per-dim sigmoid Δt, ReLU diagonal A; seeds gated {2345, 3456, 4567, 5678, 6789} + annex
{7890, 8901, 9012}; splits = the official per-seed 70/15/15 assignment (below). Framework:
torch 2.11.0+cpu (in-house code, this repo); official MIT JAX repo (tk-rusch/linoss @ 05a8353,
equinox 0.11.4 / jax 0.4.28 scratch venv) used ONLY for split extraction + parity cross-checks
per the PR-1 closure rule.

**Rider — PF-F1 premise re-verification (retrieval level) [EV]:** Vinckier et al. 2015
(arXiv:1501.03024, full text): the anchor system is a **linear passive cavity** — *"an
experimental implementation of a photonic reservoir computer based on a coherently driven
passive fiber cavity"*; *"our reservoir is a passive optical cavity, with very low intra-cavity
losses"*; *"absence of active elements in the cavity"* — whose states are linear in the input:
*"the reservoir states xi(n) are given by a linear combination of the previous inputs u(n−l)"*.
The task-solving nonlinearity is the **readout photodiode |·|²**: *"All the reservoir states …
are recovered by a photodiode which performs a quadratic transformation on A(t), since the
photodiode output is proportional to |xi(n)|²"*, with y(n) = Σᵢ Wᵢ|xᵢ(n)|² (their eq. 3).
Honesty note: the *experimental* input encoding passes the input Mach–Zehnder sine
(A_in ∝ sin{V(t)π/(2Vπ)}); the authors verified both codings *"give the same performance of the
reservoir, except for the evaluation of the memory capacities"* — performance-neutral input
preprocessing, not reservoir nonlinearity. Paquot et al. 2012 (arXiv:1111.7219, Sci Rep 2:287,
full text): that anchor's nonlinearity is **in-loop** — *"As nonlinear element we exploit the
sine nonlinearity of an integrated Mach-Zehnder intensity modulator"* (single nonlinear node +
delay loop). **PF-F1 premise confirmed; the Critic's linear floor stands; no frozen text touched.**

**Key findings:**
1. **The in-house layer is built and validated as the official computation.** Architecture: a
   complex-diagonal (S4D/DSS-class) scan engine with an inter-mode coupling hook μ (zero
   throughout this task), whose Gate-i configuration computes the published LinOSS-IM recurrence
   verbatim (per-mode 2×2 IM blocks; official expressions kept character-identical). **D-08-2
   made computational:** `ComplexDiagSSM.from_linoss_im` constructs the exact conjugate-pair
   complex-diagonal equivalent (λ = s·(1 + i·dt·√A)) and a unit test asserts forward parity;
   the Gate-i path runs the 2×2 real form because the diagonalization is undefined on the
   measure-zero ReLU boundary A = 0 (Jordan cell) — same recurrence, not an approximation.
   12/12 unit tests pass (`tests/test_linoss_gate_i.py`), incl. analytic-backward-vs-autograd
   at 1e-9 (float64) and gradient flow through the full state (house constraint 3a/3b).
2. **Cross-framework parity vs the official JAX model (transplanted weights): float32-exact.**
   Full-model class probabilities, both anchor configs: max|Δ| = 2.4e-7 (G1) / 2.7e-7 (G3) in
   BOTH inference and train modes; BatchNorm running-stat updates bit-exact (G1) / ≤1.2e-7 (G3);
   SSM-layer-only at full EigenWorms length L=17,984: 1.5e-5 abs on O(3) outputs (scan
   association order, fp-inherent). Port-critical reference behaviors replicated: equinox-0.11.4
   BatchNorm (normalize-by-just-updated-EMA, momentum 0.99, first-call copy, biased var),
   jax tanh-GELU, batch-shared dropout masks, tail-batch-dropping shuffle loop, softmax-inside-
   model with −Σy·log(p+1e-8) loss, Adam(0.9, 0.999, 1e-8) constant lr, eval cadence 1000,
   early-stop >10 non-improving evals (ties count both ways; break precedes the tie test-eval),
   reported metric = test-at-best-val.
3. **Param-count integrity check (PR-1): reconciled exactly, diagnosed pre-training.** Trainable:
   10,738 (G1) / 133,765 (G3). Published appendix counts 10,936 / 134,279 = trainable + the
   BatchNorm state arrays (2H+1 per block: 6×33 = 198 / 2×257 = 514) — the published convention
   tallies every array leaf of the equinox model incl. non-trainable state. Not a layer mismatch.
4. **PF-F6 split reproduction: exact.** Official process_uea.py run verbatim (its np.unique dedup
   both removes duplicates AND lexicographically re-orders samples — the split permutation indexes
   that order, so the official pipeline was run, not re-implemented); per-seed indices from the
   official PRNG chain (PRNGKey(seed)→split(4)[0]→split(2)[0]→permutation(N)). Heartbeat: N=409
   (0 dups) → 286/61/62. **EigenWorms: the official dedup deletes 23 duplicate samples → N=236**
   (not the nominal 259) → 165/35/36. `splits_official.json` + data sha256 recorded per dataset.
5. **G1 Heartbeat — GATE PASS.** Unrounded gated 5-seed mean = **0.7290322542190552 (72.9032%)
   ≥ 0.721** (margin **+0.80 pp**); per-seed sd 3.85 pp (published σ 3.7). Sits at −0.78σ_published
   of the 75.8% mean — inside the registered −1σ allowance (PF-F9d: the margin catches gross
   breaks; a sub-σ offset is the expected cross-framework regime). Per-seed (test %, best-val %,
   steps-to-stop, wall): 2345: 69.3548, 81.97, 28k, 121 min · 3456: 70.9677, 75.41, 13k, 55 min ·
   4567: 74.1935, 73.77, 23k, 99 min · 5678: 79.0323, 73.77, 18k, 80 min · 6789: 70.9677, 75.41,
   13k, 56 min. **Annex (non-gating, PF-F8g):** 7890: 67.7419 · 8901: 80.6452 · 9012: 79.0323
   (annex mean 75.81%; all-8 mean 73.99% ± 4.99 pp). All runs early-stopped (13k–28k of the 100k
   cap); no tuning of any kind.
6. **G3 EigenWorms — held on the pre-registered runtime flag.** Measured on this 20-core CPU
   after optimization (custom analytic-backward constant-transition scan; 6.63 → 4.38 s/step):
   74.5 min per 1000-step eval cycle → central ~31 h/seed (16–40-cycle early-stop range:
   20–50 h), 8 seeds ≈ 4.5–6 days at 3-parallel — over the task's ~24 h threshold ⇒ flagged
   **D-2026-06-10-2** (options + recommendation: run locally, gated-5 first), G3 runs NOT
   started. No protocol-touching workaround used or proposed (no truncation/chunking; the scan
   optimization is the same associative reduction, parity-verified).

**Gates (PR-1):** G1 **PASS** (72.9032% ≥ 72.1%, unrounded). G3 **pending** (runs held on
D-2026-06-10-2) ⇒ **joint Gate-i verdict pending G3**. Process gates: zero deviation from frozen
values ✔ · configs verbatim ✔ · closure rule honored (all unstated details resolved to the
official repo, documented in code) ✔ · no tuning ✔ · 5+3 seeds per anchor reported per-seed
(G1 done; G3 pending) ✔ · param counts reported + reconciled ✔ · split-reproduction method
documented ✔ · rider done ✔.

**Anomalies / concerns:** (i) **EigenWorms N=236 after official dedup** (23 duplicates deleted,
−8.9% of corpus) — official-pipeline behavior, inherited by every published run; recorded since
the nominal UEA size is 259. (ii) Seed-2345 val/test divergence (best-val 81.97% vs test 69.35%)
— 61/62-sample val/test sets; ±1 sample = ±1.6 pp; within-protocol variance, gated mean
unaffected. (iii) Per-seed test values quantize to n/62 (62 test samples) — sd comparisons with
the published σ carry that granularity. (iv) The G1 PASS margin (+0.80 pp) is one test-set sample
above threshold (45/62 mean-equivalent); fragile-looking but exactly what the pre-registered
−1σ calibration prices in (false-kill ≈1.3%/anchor). (v) The published-count convention (finding
3) should be quoted whenever param counts are compared downstream.

**Data paths:** runs `results/s0_2/gate_i/Heartbeat_seed{2345..9012}.jsonl` (config record +
per-cycle train/val + test-at-improvement trail + summary) · logs `results/s0_2/gate_i/logs/` ·
splits `data/processed/UEA/{Heartbeat,EigenWorms}/splits_official.json` (+ data.npy/labels.npy,
sha256 in-file: HB 253d513a…, EW e1d1f145…) · code `photonic_ssm/linoss/{layer,stack,data,train}.py`,
`scripts/{extract_official_splits,run_gate_i,parity_torch_side,parity_jax_side}.py`,
`tests/test_linoss_gate_i.py` · parity artifacts /tmp/parity_gate_i/ (regenerable).

**Compute:** local 20-core CPU only (no GPU, no cloud, $0). G1: 8 runs, 9.5 h summed process
time ≈ 3.1 h wall at 4-parallel × 5 threads. Validation/parity/timing: ~0.5 h. Scratch venv
/tmp/linoss_venv (jax 0.4.28 CPU, equinox 0.11.4, optax 0.2.2, sktime 0.30.1 — the official pins).

---

## S0.2-0 — Debt-#2 benchmark recon + bake-off task candidates + PR-2 input sheet + EV rider (2026-06-10, Executor)

**Goal:** design-input for the PR-1/PR-2 freeze (S0.2 step 0 of 2; continuation-gate GO
E-2026-06-10-3): (1) debt #2 — LinOSS/D-LinOSS benchmark specifics, primary-sourced, with 2–4
Gate-i reproduction candidates + a margin basis; (2) 2–3 bake-off task candidates sized to the
envelope §6 niche with explicit fit arithmetic; (3) the PR-2 input sheet (partitions, readouts,
W1 cross-check). **Menu, not choice — no values frozen, zero training runs.** Rider first: the
Critic envelope-audit fix list (EV-F1/F2/F3/F4/F5/F7).

**Config:** literature/design task (no simulation, no seeds). Three parallel web sweeps
(LinOSS primary; D-LinOSS primary + coupled-variant guard-check; Mamba-3 context + task metadata
+ equalization-channel primary), ~94 tool calls, 2026-06-10; Executor first-hand re-verification
of every decisive number by string-exact grep on the fetched primaries (arXiv HTML 2410.03943v3
+ 2505.12171v2; Vinckier arXiv:1501.03024 PDF→text) — all matched.

**Key findings:**
1. **Rider done (no verdict changes), citations in-place:** EV-F1 strike-correct on this log's
   S0.7L-1 finding 2 (class-A-dead is **C4-conditional**; OPT×A clears Brainwave in-window at
   P_π/2 holding, crossovers 1.32–1.47 GS/s; only CONS×A dead under any convention); EV-F2
   replacement of anomaly (i)'s neutrality sentence (both flagged readings faithful but **not**
   verdict-neutral); EV-F4 latency restatement + EV-F7 cadence-provenance lines in envelope memo
   §4; EV-F3 (N=128 ⇒ class-leading corner) + EV-F5 (single-quadrature/intensity condition on C8)
   added as §6 condition 4.
2. **Debt #2 sourced.** LinOSS = ICLR 2025 **Oral** (OpenReview decision note), arXiv:2410.03943v3,
   MIT-licensed JAX repo with per-config seeds. **D-LinOSS (arXiv:2505.12171v2) is preprint-only
   at snapshot** — absent from NeurIPS-2025 (5,286 titles) and ICLR-2026 (5,351) accepted-list
   scans, DBLP CoRR-only → PR-1 anchoring caveat stated.
3. **μ=0 classification confirmed (D-08-2 vindicated):** LinOSS *"A is a diagonal matrix"* +
   ReLU-diagonal parametrization [EV]; D-LinOSS *"uncoupled second-order system"* [EV]; dedicated
   guard-check (citation lists + venue scans) found **no published coupled/non-diagonal
   LinOSS-class benchmark through 2026-06** — every published number validates only the μ=0
   reduction; the coupled-μ transfer rests on the PR-3 in-house ceiling, as registered.
4. **Four Gate-i candidates with [EV]-verified published configs** (state dims 16–64 ↔ N
   in/below the registered grid): Heartbeat (75.8±3.7, cheapest), MotorImagery (D-LinOSS
   61.1±2.0 — tightest σ, state 64), EigenWorms (95.0±4.4 — the long-range flagship, state 64),
   PPG-DaLiA (6.4±0.23 ×10⁻² MSE — the 50k headline; compute-flagged). Four margin-basis options
   (±1σ / ±2σ / clear-best-non-oscillatory-competitor / fixed band) with per-candidate
   arithmetic; published σ includes split-draw variance (5-seed Walker protocol).
5. **Reproduction-relevant discrepancy caught:** the LinOSS paper states Δt=1 but the official
   code trains a per-dimension learnable timestep (sigmoid) — PR-1 should name the **code** as
   the reference behavior. Weather rows excluded from the menu (no σ/seed count anywhere, no
   code — irreproducible at pre-registration grade).
6. **Three bake-off candidates with explicit niche-fit arithmetic** (vs memory corners
   0.33/3.29/6.58 foundry and 4.9/49.4/98.8 class-leading samples at 0.1/1/2 GS/s): **T-A**
   Jaeger–Haas nonlinear channel equalization clocked at 1–2 GS/s (channel taps + nonlinearity
   quoted verbatim [EV]; 10-tap/7-dominant memory; photonic-RC anchors at 0.1–0.9 MS/s; maximal
   reservoir contrast); **T-B** band-limited IM-DD PAM-4 equalization at 1–2 GBd (pnn-multilayer
   `imdd_timedomain.py` lineage; **CD inert at-rate** — ≈0.005 symbols per 10 km — ISI from
   TX/RX band-limitation, span designable 2–12 symbols; generator port flagged); **T-C** the
   PR-13 synthetic memory family (k ∈ {1,3,10,30,100} straddling every corner; k=100 = the
   designed class-leading cliff cell; unifies the bake-off secondary with the PR-13 row).
   Complementarity observation recorded (headline + PR-13 secondary), no choice made.
7. **PR-2 input sheet:** partitions P1 (full B1 + gain; 4–5 ch/ring — at/above the PR-10
   bracket, flagged) / P2 (gain-free minimal B1, ~3/ring ✓) / P3 ({δ,μ}, damping fixed) / P4
   ({δ} only); readouts R1 single-quadrature (LinOSS-equivalent, envelope-consistent) / R2
   intensity (consistent, nonlinear head) / R3 I/Q (**envelope-inconsistent per EV-F5** — flag);
   F6 policy options incl. baseline-holds-κ_ext; **W1 cross-check: P1/P2 satisfy W1, P3
   conditional (pole-positions wording call → Supervisor), P4 fails W1**; B1 topology fork
   (photonic-molecule vs bus-mesh) carried to the freeze.

**Gates:** every load-bearing number primary-sourced + quoted ✅ (markers [EV]/[AV]/[ABS];
Executor string-exact re-verification trail in memo Appendix A.3); ≥2 Gate-i candidates with
reproducible configs + margin basis ✅ (4 given); ≥2 task candidates with explicit niche-fit
arithmetic ✅ (3 given: rate, memory samples, N per cell); menu-not-choice ✅ (no value frozen
anywhere in either memo); zero training runs ✅; rider done ✅ (EV-F citations in each edit).

**Anomalies / concerns:** (i) D-LinOSS venue status (preprint-only) — if PR-1 anchors on its
numbers the freeze must say so; (ii) the Δt paper-vs-code discrepancy (finding 5) — silent
reproduction risk if PR-1 cites the paper text; (iii) PPG-DaLiA rate bookkeeping (LinOSS "128 Hz"
vs UCI-native 64 Hz wrist max) — irrelevant to Gate i, fatal to any claim that the published
suite is niche-rate-relevant (native rates are Hz-class); (iv) Jaeger-channel target convention
gap (Vinckier prose says recover d(n), canonical is d(n−2)) — the freeze states which; (v) UEA
native wall-clock rates mostly unstated in primaries (EthanolConcentration is spectral, not
temporal) — same niche-rate caution.

**Data path:** `docs/s0_2/debt2_benchmark_recon.md` (incl. Appendix A search/verification trail);
`docs/s0_2/bakeoff_task_candidates.md`; rider edits in this file's S0.7L-1 entry +
`docs/s0_7/s07_lite_envelope.md` §4/§6.

**Compute used:** local only — 3 research subagents (~244k agent tokens) + curl/grep
verification; zero simulation; zero cloud spend.

---

## S0.7L-1 — S0.7-lite envelope (PR-10 🔒 FROZEN) + WS-F11/F12 rider (2026-06-10, Executor)

**Goal:** run the S0.7-lite energy/latency envelope strictly from the frozen PR-10 block (every
load-bearing number traced to a frozen row, cited per use; zero new sourcing), at both corners
(OPT/CONS) × both heater classes (A/B), vs the named F16 baselines; check the §10 escalation
clause explicitly. Rider first: WS-F11 count/pointer fixes + WS-F12 S0.8 full-text-TODO section
in the S0.L-1 memo.

**Config:** pure arithmetic + plots (`analysis/s0_7_lite_envelope.py`; no simulation, no seeds
applicable, deterministic). Grid: N ∈ {8,32,128} × {0.1, 1, 2} GS/s (registered ends + interior
point) × 4 scenarios. Frozen brackets carried as ranges (no midpoints); 8 stated mapping
conventions (C1–C8, in script header + memo §2) per the frozen output convention; heater-class
consistency rule honored (one class per scenario for power AND τ/SPSA cadence).

**Key findings:**
1. **§10 clause does NOT fire:** 16 OPT grid cells clear ≥1 named baseline (all OPT×B at
   ≥1 GS/s; e.g. N=32 @1 GS/s: 229–233 pJ/sample vs Brainwave 1 561 pJ/sample = 6.7×; up to
   14.7× at N=128 @2 GS/s). No Stage-1-reframing escalation drafted.
2. **The binding constraint is the heater class, not the conversion stack — C4-conditional
   (Critic EV-F1).** ~~Class-A (foundry, 60–175 mW/π) scenarios lose to every baseline everywhere
   inside the registered 0.1–2 GS/s window~~ ← true only under the registered worst-case holding
   convention (C4, full P_π at 100% duty): there the Brainwave crossovers sit at 2.56–2.84 GS/s
   (OPT×A) and 16.6–29.7 GS/s or never (CONS×A), all above the registered ceiling. Under
   expected-value holding (P_π/2 — the uniform-trim-statistics expectation), **OPT×A clears
   Brainwave in-window (crossovers 1.32–1.47 GS/s); only the deployable corner (CONS×A) is
   class-A-dead under any holding convention** (EV-F1). Only class-B (~1 mW/π suspended) wins
   under C4 — and the frozen row itself marks class B **non-CORNERSTONE** at τ = 0.4–2.6 ms (SPSA
   cadence floor 0.8–5.2 ms/iteration). The energy niche as computed is not reachable in the
   currently-named foundry flow → Stage-1 platform constraint, flagged for PR-2/PR-4 framing.
3. **Even the deployable corner wins at large N:** CONS×B (vendor TI converters) clears
   Brainwave at N ≥ 32 above 0.28–0.50 GS/s and Jetson-sustained at N=128 — the C8 structural
   effect (conversion is N-independent, digital cost ∝ N).
4. **Rate floor:** every scenario loses everything at 0.1 GS/s (OPT×B crossover ≈ 0.12–0.14
   GS/s); independently, foundry-corner ring memory is sub-sample at 0.1 GS/s (0.33 samples).
   The niche lives at the 1–2 GS/s end.
5. **Jetson-peak (4.6 TOPS/W) is never beaten anywhere by any scenario** — the embedded-GPU case
   rests entirely on the registered peak≠sustained caveat (<13% measured batch-1-RNN util.). A
   measured sustained embedded-GPU number on a matched streaming workload is the single most
   case-threatening S0.7-full retrieval.
6. **Latency:** photonic lower bound 4.3–69.4 ns/sample (ring memory + 2 sample periods;
   converter pipeline latency is not a frozen row → reported as a registered gap) vs Brainwave
   <4 ms batch-1 (~10⁵). Robust to any plausible pipeline adder.
7. **Niche statement (explicit, memo §6):** plausible low-latency niche EXISTS, conditionally —
   ≥~0.5 GS/s streaming, N=32–128, sub-µs latency relevance, class-B heaters required, vs
   serving-class/sustained baselines only. S0.2 input: equalization-class streaming task at
   GS/s rates, not LLM-decode. **Verdict: conditional POSITIVE — assumption-driven, NOT
   outreach-load-bearing** (roadmap semantics); exclusions (laser, locking, control compute,
   packaging) listed unbudgeted — they only shrink positive cells, negative findings robust.
8. **Rider done (no verdict changes):** S0.L-1 memo counts corrected (47 non-fatal-cite rows;
   74 rows / 80+ papers, was "~60"); N28a pointer fixed (→ N28 experiment (a)); §7 S0.8
   full-text TODO added (Wan OEA 2024 / C9 de-compression / Mak-Bois-Poon 2016).

**Gates:** every number traces to a frozen PR-10 row, cited per use ✅ (memo §1 table; adopted
discrepancy corrections honored — no Ozkaya standing-power / "~5 pJ/bit DSP" / Harris-Si number
used); all four scenario combinations reported ✅ (no cherry-picking; full clearance matrices);
exclusions stated in the output ✅; explicit niche-or-no-niche statement ✅ (memo §6); §10 clause
checked explicitly ✅ (does not fire); rider done ✅.

**Anomalies / concerns:** (i) two frozen-block readings had to be fixed by stated convention and
are flagged for Critic audit: trim electronics charged in all scenarios (C3) and class-A "fast τ"
resolved via the row's memo-§4 reference (38–110 µs) — both faithful to the frozen source record
but **not verdict-neutral** (Critic EV-F2; replaces the prior "neither affects any clearance
verdict" sentence, which failed in both tested directions): the OPT-corner rate-floor negative is
partly C3-borne (trim dropped → 15 verdicts flip favorably, incl. OPT×B clearing at 0.1 GS/s), and
one deployable-corner niche cell (CONS×B N=128 @1 GS/s vs Jetson-sustained) is trim-sensitive
(4 mW/ch stress → CLEARS→LOSES). The adopted charge-everywhere reading stands (provenance-faithful;
the AD5380-class 2 mW/ch pairing is the well-sourced one for class B). (ii) The OPT×B-vs-DSP
clearance at N=32 is by ~1% (233 vs 235 pJ) — treat as boundary, not margin. (iii) Converter
pipeline latency has no frozen row — latency is a lower bound only.

**Data path:** `docs/s0_7/s07_lite_envelope.md` (memo); `analysis/s0_7_lite_envelope.py`;
`results/s0_7/` (JSON + tables.md + 2 PNGs).

**Compute used:** local CPU, <1 s arithmetic; zero simulation/cloud spend.

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
