# Debt #2 — LinOSS / D-LinOSS benchmark recon (S0.2-0, design input for the PR-1/PR-2 freeze)

**Task:** S0.2-0 · **Author:** Executor · **Date:** 2026-06-10 (snapshot) · **Status: MENU, NOT
CHOICE** — this memo feeds the PR-1/PR-2 freeze (Supervisor drafts the ask; **Lucas freezes**). It
sets no values and ran **zero training runs** (Gate-i material is untouched; S0.2-1 is post-freeze).

**Sourcing protocol (the B2/F5 lesson):** every load-bearing number below is read from a primary
fetched 2026-06-10 — arXiv HTML full text, OpenReview API, official GitHub raw files — by research
subagents, with the decisive numbers **re-verified first-hand by the Executor** against the fetched
HTML/PDF on disk. Markers: **[EV]** = Executor-verified character-exact this session; **[AV]** =
agent-verified in fetched full text; **[ABS]** = abstract/landing page only. Anything unreachable is
marked UNREACHED, not filled.

---

## 1. Paper identities (and one anchoring caveat)

| Paper | ID / version read | Venue status | Code |
|---|---|---|---|
| **LinOSS** — Rusch & Rus, *Oscillatory State-Space Models* | arXiv:2410.03943 **v3** (2025-06-18) [EV: fetched HTML] | **ICLR 2025, Accept (Oral)** — OpenReview decision note, Submission10203 [AV] | github.com/tk-rusch/linoss — **MIT**, JAX/Equinox; per-dataset config JSONs + seeds for UEA+PPG; **weather absent from repo** [AV] |
| **D-LinOSS** — Boyer, Rusch & Rus, *Learning to Dissipate Energy in Oscillatory State-Space Models* | arXiv:2505.12171 **v2** (2025-09-30) [EV: fetched HTML] | **Preprint only as verifiable 2026-06-10**: absent from NeurIPS 2025 (5,286-title scan) and ICLR 2026 (5,351-title scan) accepted lists; DBLP lists CoRR only [AV] | github.com/jaredbmit/damped-linoss — **MIT**, JAX/Equinox; best configs recorded in paper Table 5 (no shipped per-result config files) [AV] |
| **Mamba-3** — Lahoti et al. (Gu/Dao group), *Mamba-3: Improved Sequence Modeling using State Space Principles* | arXiv:2603.15569v1, comment "ICLR 2026" [ABS] | **Context only** (per task spec): LM/retrieval/state-tracking at 1.5B scale; not a Gate-i anchor and not size-relevant to N=32–128 | — |

**Anchoring caveat for PR-1:** the peer-reviewed anchor is **LinOSS (ICLR 2025 Oral)**. D-LinOSS
numbers are primary-sourced and reproducible-in-principle but carry **preprint-only** status at
snapshot — if PR-1 anchors a D-LinOSS number, the freeze should note that status explicitly.
(Mamba-3 context row: *"Guided by an inference-first perspective, we introduce three core
methodological improvements inspired by the state space model (SSM) viewpoint of linear models."*
[ABS] — cited as the modern-SSM-line context, nothing more.)

## 2. What the published results validate — the μ=0 classification (D-08-2)

**Every published LinOSS-family benchmark number is diagonal/uncoupled.** Verbatim:

- LinOSS formulation: *"Note that **A** is a diagonal matrix, i.e., with non-zero entries only on
  its diagonal."* [EV] — and the experiments use the ReLU parametrization of that diagonal: *"we
  decide to focus on the ReLU-parameterization of the diagonal weights **A** in this manuscript"*
  [EV]; code agrees (`A_diag` shape `(ssm_size,)`, `relu(A_diag)`) [AV: `models/LinOSS.py`].
- D-LinOSS: *"The continuous-time parameters **A** and **G** are restricted to diagonal matrices
  with non-negative entries, meaning (1) is an uncoupled second-order system."* [EV]. What it adds
  is **learnable per-mode damping**: x″ = −A x − G x′ + B u with G = ReLU(Ḡ), A clamped to the
  stability band derived from *(G_i − Δt_i A_i)² ≤ 4 A_i*, eigenvalues |λ_i| = 1/√(1+Δt_i G_i) ≤ 1;
  the reachable stable spectrum is the **full complex unit disk** [EV: "full complex unit disk"]
  (vs measure-zero curves for LinOSS-IM/IMEX — their Props 3.3/3.4). Initialization: eigenvalues
  sampled *"within the radial band [0.9,1.0] and the full angular range"* [EV: "radial band"].
- **Guard-check (coupled variants):** a dedicated sweep (arXiv export API, Semantic Scholar
  citation lists of both papers, full NeurIPS-2025/ICLR-2026 accepted-title scans) found **no
  published work that trains a LinOSS-family oscillatory SSM with a non-diagonal/coupled state
  matrix and validates it on LinOSS-class sequence benchmarks** [AV]. Nearest neighbors, none
  transferable: BioOSS (NeurIPS 2025 — fixed local-grid wave coupling, not trained off-diagonal A);
  CON/Stölzle & Della Santina (NeurIPS 2024 — coupled but control/latent-dynamics benchmarks);
  H-LRU/BD-LRU (block-dense first-order LRU class, not oscillatory); GraphCON; Stuart-Landau OGNN;
  PHAST (all [ABS], one-line verdicts in trail A.2).

**Consequence (as D-08-2 anticipated):** published LinOSS/D-LinOSS results validate **only the μ=0
diagonal reduction** of our ring bank. The trainable inter-ring μ_jk generalization has **no
external accuracy reference anywhere in the literature** — benchmark transfer for the coupled form
rests on the in-house PR-3 BPTT-on-substrate ceiling, exactly as registered. (This is both the
novelty and the risk; the Critic's guard-verdict line is quoted in trail A.2.)

## 3. The headline published results (primary-quoted)

**Protocol provenance (binds all UEA/PPG rows):** both papers run the Walker et al. 2024
(log-NCDE) benchmark — 6 longest UEA-MTSCA datasets + PPG-DaLiA, *"the same pre-selected random
seeds for splitting the datasets into training, validation, and testing parts (using 70/15/15
splits)"* [EV], the same 162-config tuning grid, **5 seeds**, mean±std over runs (seed variation
includes the split draw — the σ below is init+split variance, not init-only). **Competitor numbers
are imported from Walker et al. 2024, not rerun** — LinOSS: *"We note that all other results are
taken from Walker et al. (2024)."* [AV]. LinOSS code repo is an extension of Walker's [AV].

| Task (len) | Metric | LinOSS-IM | LinOSS-IMEX | D-LinOSS | Best non-LinOSS-family |
|---|---|---|---|---|---|
| EigenWorms "Worms" (17,984) | acc % | **95.0 ± 4.4** [EV] | 80.0 ± 2.7 | 93.9 ± 3.2 [EV: "93.9"] | LRU 87.8 ± 2.8 |
| SelfRegulationSCP1 (896) | acc % | 87.8 ± 2.6 [EV] | 87.5 ± 4.0 | 88.9 ± 3.0 | **S5 89.9 ± 4.6** (table best) |
| SelfRegulationSCP2 (1,152) | acc % | 58.2 ± 6.9 | **58.9 ± 8.1** | 58.6 ± 2.3 | NRDE/Log-NCDE 53.7 |
| EthanolConcentration (1,751) | acc % | 29.9 ± 0.6 | 29.9 ± 1.0 | 29.9 ± 0.6 | **Log-NCDE 34.4 ± 6.4** (table best) |
| Heartbeat (405) | acc % | 75.8 ± 3.7 | 75.5 ± 4.3 | 75.8 ± 4.9 | **LRU 78.4 ± 6.7** (table best) |
| MotorImagery "Motor" (3,000) | acc % | 60.0 ± 7.5 | 57.9 ± 5.3 | **61.1 ± 2.0** [EV: "61.1"] | Log-NCDE 53.7 ± 5.3 |
| **UEA average** | acc % | 67.8 | 65.0 | **68.0** [EV: "68.0"] | Log-NCDE 64.3 |
| PPG-DaLiA (49,920-sample windows) | MSE ×10⁻² | **6.4 ± 0.23** [EV] | 7.5 ± 0.46 | **6.16 ± 0.73** [EV] | Log-NCDE 9.56 ± 0.59 (Mamba 10.65 ± 2.20, LRU 12.17 ± 0.49) |
| Weather (720→720 steps) | MAE | 0.528 | 0.508 | **0.486** | S4 0.578 |

PPG window convention: *"a sliding window of length 49920 and step size 4992 is applied"* [EV:
"49920"]; 6 input channels; output = HR every 128 steps through tanh∘linear [AV: `process_ppg.py`
+ code]. The abstract's headline — *"LinOSS outperforms Mamba and LRU by nearly 2x on a sequence
modeling task with sequences of length 50k"* [ABS] — is this PPG row. D-LinOSS headline:
*"consistently outperforms previous LinOSS methods on long-range learning tasks … and reduces the
hyperparameter search space by 50%"* [ABS] (the 50% = dropping the IM-vs-IMEX choice); its UEA-avg
margin over LinOSS-IM is **+0.2 pts** (68.0 vs 67.8), and it is *below* LinOSS-IM on EigenWorms
(93.9 < 95.0, acknowledged in-paper) [AV].

**Not Gate-i material:** the **Weather** rows carry **no std/seed count anywhere** in either paper
(UNREACHED), the lrs come from random search, and the experiment is absent from the LinOSS repo —
irreproducible at pre-registration grade. **EthanolConcentration** is a wavelength *spectrum*
(0.5 nm steps — not a time series; native-rate n/a [AV: timeseriesclassification.com]) sitting
near 4-class chance (29.9 %); poor anchor. D-LinOSS's synthetic ablations (Decay: D-LinOSS RMSE
0.8±0.1 ×10⁻³ vs IM 8.0±1.7 at λ=0.8, 3 seeds; Adding at 500–5,000: IMEX *"fails to outperform …
random guessing"* [AV]) are useful design references for the bake-off task family (see the
companion task-candidates memo), not Gate-i anchors.

## 4. Configs as published — and feasibility at our scale

Tuning grid (both papers, Walker protocol): lr ∈ {1e-5, 1e-4, 1e-3} × blocks ∈ {2,4,6} × hidden ∈
{16,64,128} × **SSM state dim ∈ {16,64,256}** × include-time ∈ {T,F} [EV: "state-space dimension"
grid sentence]. Training: 100k steps, batch 32 (4 for EigenWorms/PPG), 5 fixed seeds
[2345,3456,4567,5678,6789], constant lr [AV: repo configs].

Best configs (LinOSS Table 4 + D-LinOSS Table 5 — **all rows below re-verified [EV]** against the
fetched HTML):

| Task | LinOSS-IM (lr / hidden / state / blocks / time / params) | D-LinOSS (lr / hidden / state / blocks / time / params) |
|---|---|---|
| Worms | 0.001 / 128 / **64** / 2 / T / 134,279 | 1e-3 / 128 / **64** / 2 / F / 134,279-class |
| SCP1 | 0.0001 / 128 / **256** / 6 / T / 991,240 | 1e-4 / 128 / **256** / 6 / T / 992,776 |
| SCP2 | 0.0001 / 128 / **64** / 6 / F / 399,112 | 1e-5 / 128 / **64** / 6 / F / 399,496 |
| Ethanol | 0.00001 / 16 / **16** / 4 / F / 6,728 | 1e-5 / 16 / **256** / 4 / F / 71,112 |
| Heartbeat | 0.001 / 16 / **16** / 6 / T / 10,936 | 1e-4 / 16 / **16** / 2 / F / **4,356** |
| Motor | 0.00001 / 128 / **16** / 2 / F / 91,844 | 1e-3 / 16 / **64** / 4 / F / **20,598** |
| PPG-DaLiA | 0.001 / 16 / **64** / 6 / T / (params UNREACHED) | 1e-3 / 64 / **64** / 4 / T / (UNREACHED) |
| Weather | 0.0006 / 64 / **32** / 8 / T | 7.95e-5 / 128 / **128** / 3 / F |

Feasibility readings for the freeze:

1. **State-dim ↔ N mapping.** LinOSS `ssm_size` m = number of second-order oscillators; under the
   adopted D-08-2 architecture (one ring = one independent complex pole; the conjugate partner is
   synthesized by real-linear readout — `mapping_result.md` §1–2), m oscillators ↔ **N = m rings**.
   The winning configs sit at m = 16–64 for 5 of 8 LinOSS tasks and 6 of 8 D-LinOSS tasks —
   **inside or below our registered N grid {8, 32, 128}**. Only SCP1 (m=256 both papers) and
   D-LinOSS-Ethanol exceed it → flag those as oversize for any photonic-relevant reproduction.
2. **Published numbers are multi-block stacks, not one SSM layer.** The benchmark architecture is:
   affine encoder → L × [BatchNorm → linear SSM layer (complex B,C; +Du) → **GELU** → dropout 0.05
   → **GLU** → skip] → pooled linear head (classification: time-mean-pool; regression: tanh∘linear
   every 128 steps) [AV: code; paper App. A: *"a LinOSS layer … directly followed by a nonlinear
   layer using the Gaussian error linear unit activation function (GELU) …, the Gated Linear Unit
   (GLU) …, and a skip connection"*]. **Single-layer LinOSS accuracy is unpublished** on every
   task. Gate i as worded (idealized model reproduces published accuracy) is a *digital*
   reproduction of the published stack; the PR-2 hybrid (how many photonic layers, what
   encoder/head) is a separate pin — the freeze should keep these two distinct.
3. **Paper-vs-code Δt discrepancy (reproduction-relevant).** The paper states Δt=1 (*"we decide to
   initialize **A** according to **A**_kk ∼ U([0,1]) … while setting Δt=1"* [AV]) but the official
   code makes the timestep **learnable per state dimension** (`steps = sigmoid(steps)` ∈ (0,1))
   [AV: `LinOSS.py`]; D-LinOSS makes learnable Δt explicit (*"learnable time-step parameters
   Δt ∈ ℝ^m"* [AV]). A reproduction that follows the paper text would not match the code that
   produced the numbers. **PR-1 should name the code behavior as the reference.**
4. **Compute.** Paper hardware: V100/RTX-4090 class; PPG *"due to higher memory demands"* on A100
   [AV]. The two heavy tasks are EigenWorms (len 17,984, batch 4) and PPG (len 49,920, batch 4);
   Heartbeat/Motor are light. The MIT-licensed JAX repo runs UEA+PPG out of the box with shipped
   configs — the cheapest faithful reference path; a torch reimplementation (needed eventually for
   the photonic stack) lacks a native associative scan and will be slow at len ≥17,984 unless
   scan-compiled. Implementation choice = S0.2-1, post-freeze; flagged here as a cost asymmetry
   between candidates.

## 5. Gate-i reproduction candidates (the menu — 2–4 per the task gates)

All four below have: published mean±σ from §3 [EV], an exact published config (§4 [EV]), shipped
seeds, and local-compute feasibility. **No value is chosen here.**

| ID | Candidate | Published target | State dim (↔N) | Cost | Fit notes |
|---|---|---|---|---|---|
| **G1** | **Heartbeat**, LinOSS-IM | 75.8 ± 3.7 % | 16 (below N-grid; cheap) | ~minutes–hours (len 405, 10,936 params) | Cheapest smoke anchor. **Weakness:** LinOSS is *not* table-best here (LRU 78.4) — reproducing it shows fidelity, not class superiority; σ moderate. |
| **G2** | **MotorImagery**, D-LinOSS (or LinOSS-IM) | **61.1 ± 2.0 %** (IM: 60.0 ± 7.5) | 64 — in-window | low–mid (len 3,000; 20,598 params) | Tightest σ of any oscillatory-SSM win; state dim 64 matches the niche N. **Caveat:** D-LinOSS anchor = preprint (§1); LinOSS-IM alternative has σ=7.5. |
| **G3** | **EigenWorms**, LinOSS-IM | **95.0 ± 4.4 %** | 64 — in-window | high-ish (len 17,984, batch 4, 100k steps) | The flagship long-range result (beats LRU by 7.2 pts; ICLR-Oral headline); 2 blocks only; the strongest "oscillatory-SSM task accuracy" anchor for Gate i as the roadmap words it. |
| **G4** | **PPG-DaLiA**, LinOSS-IM | **6.4 ± 0.23 ×10⁻² MSE** | 64 — in-window | highest (len 49,920; paper used A100 for memory) | The 50k-length abstract headline ("~2× over Mamba/LRU"); regression metric diversifies Gate i beyond accuracy. Stretch target — compute-flagged. |

**Margin-basis options for PR-1** (menu; arithmetic shown so the freeze ask is one line):

- **M1 — within 1σ(published) of the published mean.** Defensible because the published σ already
  includes split-draw variance (§3 protocol note). G1: ≥72.1 % · G2: ≥59.1 % (D-LinOSS) · G3:
  ≥90.6 % · G4: ≤6.63 ×10⁻². Tight where σ is tight (G2), forgiving where the task is volatile (G3).
- **M2 — within 2σ.** G3: ≥86.2 % · G4: ≤6.86 ×10⁻². Safer against reimplementation variance
  (framework port, Δt discrepancy §4.3); weaker as a claim.
- **M3 — clear the best non-oscillatory competitor in the published table** ("the idealized model
  is oscillatory-SSM-class on this task"): G3: ≥87.8 % (LRU) · G2: ≥53.7 % (Log-NCDE) · G4:
  ≤9.56 ×10⁻² (Log-NCDE). **Inapplicable to G1** (LinOSS itself sits below LRU there). Decoupled
  from σ; arguably the most meaning-bearing form for Gate i's purpose (the bake-off needs an
  in-class digital reference, not a leaderboard win).
- **M4 — fixed absolute band** (e.g., published mean − X pts, X frozen): simplest to state;
  arbitrary unless X is derived from M1–M3 arithmetic anyway.

Seed-count note: published = 5 seeds; house standard = 4 minimum / 8 for high-variance. G3
(σ=4.4) and G1 under LinOSS-IM Motor-style σs qualify as high-variance → 8 seeds if chosen.
A two-candidate freeze (one cheap + one flagship, e.g. G1+G3 or G2+G3) would test fidelity and
the long-range headline independently — stated as an observation, not a recommendation.

## 6. Anomalies / caveats (carried loudly)

1. **D-LinOSS venue status** (§1) — preprint-only at snapshot; PR-1 anchoring implication stated.
2. **Weather is irreproducible at pre-registration grade** (no σ, no seeds, no code) — excluded
   from the candidate menu despite being a headline table.
3. **Competitor numbers are imported** from Walker et al. 2024 (both papers) — a Gate-i
   reproduction targets the LinOSS-family number; it does not re-establish the competitor gaps.
4. **Paper-vs-code Δt discrepancy** (§4.3) — PR-1 must name the code as the reference behavior.
5. **PPG-DaLiA rate bookkeeping:** LinOSS says *"maximum rate of 128 Hz"*; the UCI primary gives
   wrist-native max 64 Hz (BVP), 32/4/4 Hz others, 700 Hz chest [AV: UCI page] — a resampled
   common grid. Irrelevant to Gate i (digital), relevant to any niche-rate storytelling (the
   companion memo handles niche fit; native rates here are Hz-class, **not** GS/s).
6. **EigenWorms/Heartbeat native wall-clock rates are unstated** in the primaries;
   EthanolConcentration is spectral, not temporal [AV] — same niche-rate caution.

## Appendix A — search/verification trail (reproducible)

**A.1 Subagent sweeps (2026-06-10, ~94 tool calls across 3 agents):** (i) LinOSS primary — arXiv
abs + arXiv HTML v3 + OpenReview API v2 (forum GRMfXcAAFh) + repo README/`models/LinOSS.py`/
`process_ppg.py`/7 config JSONs via raw.githubusercontent. (ii) D-LinOSS primary — arXiv abs +
HTML v2 + GitHub API/raw (jaredbmit/damped-linoss) + DBLP search API + full accepted-title scans
of NeurIPS 2025 (5,286) and ICLR 2026 (5,351) via OpenReview API2 + Semantic Scholar citation
lists (32 LinOSS / 4 D-LinOSS citers). (iii) Task metadata — timeseriesclassification.com dataset
pages ×6, UCI PPG-DaLiA page, ar5iv log-NCDE (2402.18512), arXiv export API (`ti:"Mamba-3"` →
unique hit 2603.15569).

**A.2 Guard-check candidates examined (lane: coupled/non-diagonal LinOSS-class):** Dubinin et al.
arXiv:2602.12021 (H-LRU/BD-LRU); Yuan et al. BioOSS arXiv:2510.10790 (NeurIPS 2025 poster);
Stölzle & Della Santina CON arXiv:2409.08439 (NeurIPS 2024); GraphCON arXiv:2202.02296 (ICML
2022); Zhang et al. Stuart-Landau OGNN arXiv:2511.08094; PHAST arXiv:2602.17998; plus downstream
LinOSS users (Looped-SSMs arXiv:2605.16048, PINN-OSS arXiv:2606.02623, SHaRe-SSM
arXiv:2510.14386) — all diagonal or non-LinOSS-benchmark; none trains a coupled LinOSS-class
recurrence on this suite. Bounded by the Semantic Scholar citation index at snapshot ("not found",
not proof of absence).

**A.3 Executor first-hand verifications (curl + grep/python on the fetched files, /tmp,
2026-06-10):** `arxiv.org/html/2410.03943` (1.77 MB) — diagonal-A sentence ×1, ReLU-param ×1,
49920 ×1, pre-selected-seeds ×1, "95.0 ± 4.4", "6.4 ± 0.23", "87.8 ± 2.6", Table-4 rows for
Worms/Heartbeat/PPG/Weather/Ethanol/Motor/SCP2 [EV]. `arxiv.org/html/2505.12171` (299 kB) —
"uncoupled second-order system" ×2, "full complex unit disk" ×2, "radial band" ×1, 93.9/6.16/
0.73/68.0/61.1, Table-5 rows Worms/SCP1/SCP2/Heartbeat/Motor/PPG/Weather, param counts
4356/20598/134279 [EV]. `arxiv.org/pdf/1501.03024` → pdftotext — used in the companion memo [EV].

**A.4 Known-unreached:** LinOSS PPG/Weather param counts (Table 5 is UEA-only); weather σ/seeds
(both papers); Reiss-2019 8 s/2 s HR-window convention (MDPI blocked); per-dataset UEA input
channel counts in the LinOSS paper (taken from timeseriesclassification.com instead [AV]).
