# Task Queue

Supervisor assigns tasks here. The Executor reads and executes the task marked **ACTIVE**, then
**stops and waits**. The Supervisor marks a task **COMPLETED** (date + one-line summary) before
assigning the next. New tasks go at the top, below this header.

Task format: see `.claude/skills/executor/SKILL.md`.

---

## 🔥 ACTIVE — S0.2-1: in-house LinOSS layer + the Gate-i reproduction runs (S0.2 step 2 of 2)

**Assigned:** 2026-06-10
**Supervisor:** Claude Opus 4.8
**Status:** 🔥 ACTIVE — the project's first training runs.
**Source:** roadmap §S0.2 (Gate i) + **🔒 PR-1 v2, FROZEN 2026-06-10** (`preregistration.md` —
**the governing document; read it first and follow it to the letter**) + the freeze-review
carry-ins (ledger Notes, last bullet). PR-2 v2 is also frozen — it governs S0.3+, **not** this
task; nothing here implements it.

**Objective:** implement the in-house recurrence layer (the one the bake-off extends
downstream), validate it by reproducing the two frozen published anchors. **The gate, verbatim
from PR-1:** G1 Heartbeat unrounded 5-seed mean ≥ **72.1 %** **AND** G3 EigenWorms unrounded
5-seed mean ≥ **90.6 %**.

### Rider (do first; small; decision-free) — PF-F1 premise re-verification
At **retrieval level** (full text, not abstracts): confirm the Vinckier 2015 anchor system is a
*linear* passive cavity whose task-solving nonlinearity is the **readout photodiode |·|²**
(note also what Paquot 2012 used). One [EV]/[AV]-marked paragraph in the results entry. This is
the PF-F1 premise check (ledger-Notes carry-in); the Critic's linear floor stands regardless —
no frozen text changes either way, just the record.

### Main task
1. **The in-house layer (new code, this repo):** complex-diagonal (S4D/DSS-class) recurrence
   with an inter-mode coupling hook **μ (run at μ=0 throughout this task)**, whose Gate-i
   configuration **realizes the published LinOSS-IM recurrence exactly** (per D-08-2: LinOSS =
   the uncoupled, real-I/O conjugate-pair special case — not an approximation of it). PR-1
   reference-behavior pins: **learnable per-dimension sigmoid Δt, ReLU-parametrized diagonal A,
   IM discretization**. Do **not** build the ZOH/CMT substrate mode now (S0.3; PR-1 "Scope of
   Gate i" registers that delta).
2. **The published stack around it, verbatim:** BatchNorm → SSM → GELU → dropout → GLU → skip;
   mean-pool head. Configs frozen (no deviation): **G1** lr 1e-3 / hidden 16 / state 16 /
   blocks 6 / time T; **G3** lr 1e-3 / hidden 128 / state 64 / blocks 2 / time T.
   **Param-count integrity check:** report your counts vs published **10,936 (G1) /
   134,279 (G3)** — a mismatch is an anomaly flag, diagnose before training.
3. **Walker protocol exactly:** the 5 gated seeds {2345, 3456, 4567, 5678, 6789} setting the
   70/15/15 splits. **Split reproduction is pinned (PF-F6):** port the split routine or extract
   split indices from the official repo; if exact reproduction is infeasible in your framework,
   **stop and file `decisions_needed.md` BEFORE any gated run**. Gated statistic = the
   **unrounded** 5-seed mean per anchor. **Annex (non-gating):** +3 seeds {7890, 8901, 9012},
   reported separately.
4. **Closure rule (PF-F8i, frozen):** any protocol detail not stated in PR-1 resolves to the
   official repo's behavior. **No hyperparameter tuning on the gated runs — none.** The
   official MIT JAX repo is a *debugging cross-check only* (divergence diagnosis), never the
   tested object.
5. **On a gate miss: stop — do not tune.** Report per-seed numbers + a divergence diagnosis vs
   the official repo (bug vs systematic offset). A fixed *bug* (diff shown, mechanism named)
   may be rerun and reported as such; a "tweak that happens to help" may not — that is tuning.

### Framework / runtime
Executor's choice within house hygiene (exceptions via `decisions_needed.md`). The official
repo is JAX; the PF-F6 split extraction may be easiest by running its data pipeline once. UEA
datasets (Heartbeat, EigenWorms) — local download is fine. **Estimate runtime before training;**
flag via `decisions_needed.md` if projected wall-clock > ~24 h, or if EigenWorms' sequence
length (~18k steps) forces any workaround that touches the protocol (no silent truncation /
chunking — that is a protocol deviation).

### Gates (all must hold)
- Zero deviation from frozen PR-1 values; configs verbatim; closure rule honored; no tuning.
- 5 gated + 3 annex seeds per anchor, all reported per-seed; gate verdict per anchor + joint.
- Param counts reported vs published; split-reproduction method documented.
- Results entry (house standard): per-seed table, unrounded means ± σ, raw-data paths (JSONL),
  runtimes, anomaly flags, the rider paragraph.

### Out of scope
T-A/T-C task generators, the substrate/CMT mode, μ≠0, anything PR-2-implementing (all S0.3+);
the D-LinOSS damping sweep (S0.6/PR-12); any edit to frozen ledger blocks (Lucas-only).

---

## ✅ DONE — S0.2-0: debt-#2 benchmark recon + bake-off task candidates (S0.2 step 0 of 2) + EV rider

**Assigned:** 2026-06-10 · **Closed:** 2026-06-10
**Supervisor:** Claude Opus 4.8
**Status:** ✅ COMPLETED 2026-06-10 — Supervisor **ACCEPT**. All gates met: [EV]/[AV]/[ABS]
sourcing discipline with a first-hand verification trail (Appendix A.3); 4 Gate-i candidates with
exact published configs + 4 margin bases with per-candidate arithmetic; 3 task candidates with
explicit niche-fit arithmetic vs the registered memory corners; menu-not-choice respected
end-to-end; zero training runs; EV rider applied with citations. High-value catches accepted:
the **paper-vs-code Δt discrepancy** (PR-1 names the code as reference), **D-LinOSS
preprint-only status** (anchoring caveat), **Weather irreproducible at pre-registration grade**
(excluded), the **μ=0 guard-check** (no published coupled LinOSS-class benchmark exists —
debt #2 substantially discharged for Stage 0; final wording at S0.8). → Supervisor drafted the
**PROPOSED PR-1/PR-2 blocks** (preregistration.md) from these menus; Critic review + Lucas
freeze next. Memos: `docs/s0_2/debt2_benchmark_recon.md` + `bakeoff_task_candidates.md`;
results in `results_log.md`; commit `5137cc5`.
**Source:** roadmap §S0.2 (Gate i; F14 — the debt-#2 memo is a *prerequisite* of the PR-1/PR-2
freeze) + **continuation gate GO** (E-2026-06-10-3, Lucas 2026-06-10). **PR-1/PR-2 are ⬜ UNSET —
this task FEEDS the freeze. It does NOT set values and does NOT run anything Gate i will judge:
no LinOSS implementation, no benchmark training runs** (that is S0.2-1, post-freeze — the
S0.7L-0 → PR-10 → S0.7L-1 pattern). Literature/design-input only.

### Rider (do first; decision-free) — Critic envelope-audit fixes
Per the `critic_review_s07lite-envelope.md` fix list (cite EV-F numbers in the edits; no verdict
changes):
1. **results_log S0.7L-1 entry:** (a) replace anomaly (i)'s neutrality sentence per **EV-F2** —
   the two flagged readings are faithful to the frozen source record but **not** verdict-neutral
   (the OPT-corner rate-floor negative is partly C3-borne; CONS×B N=128@1 GS/s vs
   Jetson-sustained is trim-sensitive); (b) strike-correct finding 2's class-A sentence per
   **EV-F1** — class-A-dead is **C4-conditional**: under expected-value (P_π/2) holding, OPT×A
   clears Brainwave in-window (1.32–1.47 GS/s); only CONS×A is dead under any holding convention.
2. **Envelope memo §6:** one sentence per **EV-F3** — the N=128 margins assume the
   class-leading-Q corner (linewidth packing: O(10–20) distinct poles/GHz foundry vs ~150
   class-leading; → PR-4 with D-08-1); name the **single-quadrature/intensity readout** condition
   on C8 per **EV-F5** (→ PR-2 readout pin).
3. **Envelope memo §4:** restate latency per **EV-F4** ("sub-µs unreachable for the serving
   class, <4 ms author bound; ≥10² vs any plausible matched-N FPGA pipeline") + one cadence
   provenance line per **EV-F7**.

### Goal (main) — the design-input memo for the PR-1/PR-2 freeze
1. **Debt #2 (F14): LinOSS / D-LinOSS benchmark specifics, primary-sourced.** For each headline
   published result (LinOSS, D-LinOSS; Mamba-3 as context only): exact task + split + metric +
   model size/config + reported number + seed variance if reported + code availability; which
   results validate only the **μ=0 diagonal reduction** (D-08-2) vs involve coupling; from these,
   identify **2–4 candidate Gate-i reproduction targets** feasible at our scale (N≈32–128 states,
   local compute) with a defensible **margin basis** for PR-1.
2. **Bake-off task candidates sized to the niche** (envelope memo §6 + `mapping_result.md` §4):
   2–3 candidate streaming tasks — **equalization-class GS/s family first** (rate-consistent with
   S0.1's linewidth-derived class), plus ≥1 published-benchmark-aligned alternative — each with:
   effective line rate vs the ≥0.5 GS/s floor; **memory depth required (samples) vs the
   registered corners** (0.33–6.6 foundry / 4.9–98.8 class-leading over 0.1–2 GS/s); N sizing;
   dataset/generator spec; evaluation metric; how the PR-13 synthetic memory family would
   parametrize it.
3. **PR-2 input sheet:** trainable-parameter-partition options (the B1 set {κ_tot,j, δ_j, μ_jk}
   + the S0.1 actuation map); readout options under the **single-quadrature/intensity** condition
   (EV-F5) incl. the F6 κ_ext dual-role note; W1 claim-wording cross-check (does each candidate
   partition train pole positions AND inter-resonator couplings — the W1 set?).

### Deliverables
1. `docs/s0_2/debt2_benchmark_recon.md` — primary-quoted (verify-before-citing; the B2/F5 lesson)
2. `docs/s0_2/bakeoff_task_candidates.md` — the menu with an explicit niche-fit table
3. Results entry in `results_log.md`; rider edits noted there with EV-F citations

### Gates
Every load-bearing number primary-sourced + quoted; ≥2 Gate-i candidates with reproducible
configs + a margin basis; ≥2 task candidates with explicit niche-fit arithmetic (rate, memory
samples, N); **menu, not choice** (no values frozen); **zero training runs**; rider done.

### Out of scope
LinOSS/D-LinOSS implementation or training (S0.2-1, post-freeze); choosing the task/margin
(Supervisor drafts the freeze ask; **Lucas freezes**); new envelope sourcing (PR-10 frozen;
S0.7-full items live in the registry); PR-15 retrievals (Lucas, claim-freeze-paced).

### Deployment
Local; web allowed (literature task). ~1 day. No simulation, no cloud.

---

## ✅ DONE — S0.7L-1: S0.7-lite envelope (PR-10 🔒 FROZEN) + WS-F11/F12 rider

**Assigned:** 2026-06-10 · **Closed:** 2026-06-10
**Supervisor:** Claude Opus 4.8
**Status:** ✅ COMPLETED 2026-06-10 — Supervisor **ACCEPT**. All gates met: every number traces to a
frozen PR-10 row (memo §1 table; the 4 excluded legacy anchors verified absent); all four
corner×heater scenarios reported with full clearance matrices; explicit niche statement (memo §6);
§10 clause checked — **does NOT fire** (16 OPT cells clear ≥1 named baseline). Supervisor
spot-checked 5 cells by hand (conversion sums, control power, Brainwave/Jetson mapping, crossover
rates) — all reproduce. ~~"the class-A negative survives even a P_π/2 duty-credit relaxation …
robust to convention"~~ ← **struck, FALSE (Critic EV-F1; the Supervisor had tested only the
1 GS/s column):** under expected-value (P_π/2) holding, OPT×A clears Brainwave **in-window**
(crossovers 1.32–1.47 GS/s); only the deployable corner (CONS×A) is class-A-dead under any holding
convention — the binding-constraint statement is **C4-conditional**. **Verdict: conditional
POSITIVE, assumption-driven, not outreach-load-bearing — CONFIRMED by Critic audit**
(`critic_review_s07lite-envelope.md`, APPROVE-WITH-EDITS: byte-identical re-run; 36/36 clean-room
cells + 144 verdicts + crossovers reproduce; §10 non-firing robust to every tested perturbation).
The two flagged frozen-row readings are **faithful to the frozen source record but NOT
verdict-neutral** (EV-F2: the neutrality sentence fails both directions — the OPT-corner
rate-floor negative is partly a C3 artifact; one deployable-corner cell is trim-sensitive).
Rider (WS-F11/F12) done, no verdict changes. **Mandatory rider on the next Executor task:**
EV-F1/F2 one-line corrections (results_log anomaly (i)) + memo §6/§4 sentences (EV-F3/F4/F5) per
the review's fix list; EV-F6/F7 → S0.7-full registry.
Memo `docs/s0_7/s07_lite_envelope.md`; results in `results_log.md`; commit `e88fbeb`.
**Source:** roadmap v3.1 §S0.7-lite (F1/F16) + **PR-10 — 🔒 FROZEN 2026-06-10** (`preregistration.md`:
read the frozen block FIRST; **every load-bearing number in the envelope must trace to a frozen PR-10
row** — if a needed number is missing, STOP and post to `decisions_needed.md`; do NOT source new
numbers, that would un-preregister the run).

### Rider (do first; decision-free)
**WS-F11:** fix the S0.L-1 memo's §0 self-undercount (count §4.2 precisely — ≈74 rows / 80+ papers, not
"~60") + the dangling "N28a" pointer. **WS-F12:** add an "S0.8 full-text TODO" section listing the
residual abstract-resting items per the Critic's WS-F12. No verdict changes.

### Goal (main)
Run the **S0.7-lite envelope**: end-to-end **energy/sample + latency/sample** for the photonic SSM at
the frozen scale grid (N∈{8,32,128}; 0.1–2 GS/s; single-carrier-one-FSR), charged the **full frozen
conversion stack**, vs the three named baselines — at **both corners (OPT/CONS) × both heater classes**
(consistency rule: one heater class per scenario for power AND τ/SPSA-cadence). Identify the plausible
low-latency **niche** (→ the S0.2 task choice / PR-2), or state explicitly that none exists. **Check
the §10 escalation clause explicitly:** does even the OPT corner clear any baseline anywhere in the
grid?

### Deliverables
1. `docs/s0_7/s07_lite_envelope.md` — assumption table (verbatim from frozen PR-10, row refs per use);
   per-grid-point result tables; crossover/niche statement; the registered exclusions (laser, locking,
   control compute, packaging) listed as **unbudgeted**; verdict per roadmap semantics (negative →
   draft the Stage-1-reframing escalation; positive → labelled assumption-driven, not
   outreach-load-bearing).
2. `analysis/s0_7_lite_envelope.py` + JSON/plots under `results/s0_7/` — **arithmetic + plots only**;
   no simulation; no new sourcing.
3. Results entry in `results_log.md`; if the §10 clause fires, an `escalate_to_human.md` draft entry.

### Gates
Every number traces to a frozen PR-10 row (cited per use); all four scenario combinations reported (no
cherry-picking); exclusions stated in the output; explicit niche-or-no-niche statement; rider done.

### Out of scope
New sourcing (PR-10 frozen); claim wording (PR-2); PR-15 retrievals (Lucas); simulation code.

### Deployment
Local, arithmetic only; hours. No web needed (numbers are frozen).

---

## ✅ DONE — S0.7L-0: PR-10 assumption sourcing (S0.7-lite, step 0 of 2)

**Assigned:** 2026-06-09 · **Closed:** 2026-06-10
**Supervisor:** Claude Opus 4.8
**Status:** ✅ COMPLETED 2026-06-10 — all 5 categories primary-quoted (~35 primaries; 2 load-bearing
ones Executor-re-verified exact); 5 freeze brackets; **4 discrepancy flags vs legacy anchors caught**
(incl. Harris-2014-is-silicon and the unverifiable Ozkaya standing-power attribution — both excluded
from PR-10); heater-class consistency identified as load-bearing (suspended power ↔ ms-τ ↔ SPSA
cadence). **No envelope arithmetic** (gate held). Supervisor **ACCEPT** → **PR-10 PROPOSED block
drafted** (`preregistration.md`) — awaiting Lucas freeze; then S0.7L-1 runs. Results in
`results_log.md`; memo `docs/s0_7/pr10_assumption_sources.md`.
**Source:** roadmap v3.1 §S0.7-lite (F1) + **PR-10 (⬜ UNSET — this task *feeds* the freeze; it does NOT
set values)**. The pre-S0.2 continuation gate needs the lite envelope regardless of the pending PR-15
rulings (E-2026-06-09-5) — this keeps the pipeline moving while Lucas adjudicates.

### Goal
Source the candidate assumption set for **PR-10** with primaries, so the Supervisor can draft the PR-10
freeze ask for Lucas. **Sourcing only — do NOT run the envelope** (that is step 1, after the freeze;
running it now would un-preregister PR-10).

### Deliverables
1. `docs/s0_7/pr10_assumption_sources.md` — a candidate table, every row primary-sourced (vendor
   datasheet or measured paper, load-bearing number quoted):
   - **E/O + O/E conversion energies** (modulator drive incl. driver; PD/TIA) at the relevant rates;
   - **DAC/ADC** energy/sample + resolution (ENOB) at GS/s-class rates (published ADC-survey data +
     ≥1 named vendor part);
   - **named digital-baseline class + sources** (F16): tuned FPGA and/or embedded-GPU/ASIC
     implementations of comparable streaming SSM/FIR/RNN workloads at matched accuracy — names + cited
     perf/W, *not* an unoptimized GPU;
   - **thermo-optic holding power** per heater (SiN, trench-isolated) + control-electronics overhead —
     reuse pnn-multilayer numbers where primary-sourced (with provenance);
   - **operating scale**: N rings, line rate, λ-plan consistent with S0.1's pole region (cite
     `docs/s0_1/mapping_result.md` §4 numbers).
2. Where sources disagree, give **bracketing values + both sources** (the freeze registers the bracket,
   not a midpoint).
3. Results entry in `results_log.md`.

### Gates
Every number primary-sourced + quoted; brackets where sources disagree; **no envelope arithmetic** (one
illustrative sanity row allowed, labelled non-load-bearing).

### Out of scope
Running the envelope (step 1, post-freeze); the PR-15 re-classification (Critic Part 2); claim wording
(PR-2, Supervisor); A4 retrievals (human-access asks — Lucas, E-2026-06-09-5).

### Deployment
Web + datasheet reading; 1–2 days; no compute spend.

---

## ✅ DONE — S0.L-1: White-space existence search (debt #1, PR-15 — front-loaded pre-S0.2)

**Assigned:** 2026-06-09 · **Closed:** 2026-06-09
**Supervisor:** Claude Opus 4.8
**Status:** ✅ COMPLETED 2026-06-09 — sweep complete per the frozen rule: ~60 candidates / all 5 lanes /
every non-clear verdict primary-quoted / reproducible trail. **0 FATAL confirmed**; 1 potentially-FATAL
AMBIGUOUS (**Wu eLight 2025**, q1 unresolved) + boundary class (= Critic WS-F1, found by both
modalities) + Böhm 2022 + 8 unreachable primaries — **all escalated with primaries, nothing adjudicated
in-pipeline** (E-2026-06-09-4 / D-2026-06-09-2). Supervisor **ACCEPT**: protocol followed exactly; the
cross-modality asymmetry (Executor found Wu/Milanizadeh/Zhao; blind pass found Fisher 1987 + the
criterion defect) is the two-modality design working. PASS not issued — verdict assembly pends Lucas's
four rulings (E-2026-06-09-5) + Critic Part 2.
**Update 2026-06-10:** Critic Part 2 filed (E-2026-06-09-6) — **memo audit CLEAN**; gate = conditional
PASS (one-sided) under PR-15.1, degenerate under the frozen letter. **Follow-up queued (next Executor
task after S0.7L-0, decision-free): WS-F11** (fix the memo's self-undercount: ≈74 rows / 80+ papers,
not "~60"; fix the N28a pointer) **+ WS-F12** (full-text the residual abstract-resting items by S0.8).
**Source:** D-2026-06-09-1 (Lucas-adopted 2026-06-09, "ok go") + **PR-15, 🔒 FROZEN — read its detail
block in `preregistration.md` FIRST and apply it as written** (the kill-rule and lanes are frozen; do not
re-derive or reinterpret them). Roadmap v3.1 §S0.L. This is a **literature task** — no simulation code.

### Goal
Run the **existence search** for verification debt #1: is there ANY prior in which *internal recurrent
parameters of a physical photonic system were updated on the physical device by a gradient-based /
gradient-estimating rule*? This is the project's kill-shot, deliberately front-loaded (cheap + decisive +
potentially fatal). A single FATAL prior falsifies the scientific-first claim — surface it loudly; do
**not** soften or adjudicate it.

### Deliverables
1. **`docs/s0_L/debt1_whitespace_search.md`** — dated memo (snapshot 2026-06):
   - **Per-candidate verdict table:** citation · system · what was *physically* updated · q1 internal?
     · q2 on-device-in-the-loop? · q3 update-rule class · **verdict** (FATAL / non-fatal-cite /
     AMBIGUOUS→escalate / clear), with the **load-bearing sentence quoted from each primary source**.
     No aggregator-snippet citations (the B2/F5 lesson) — if you can't reach the primary, the verdict is
     AMBIGUOUS, not clear.
   - **All five PR-15 lanes swept** (i: zeroth-order/perturbative internal updates; ii:
     REINFORCE/policy-gradient internal updates; iii: HIL delay-reservoir feedback/internal adaptation;
     iv: evolutionary/Boolean — non-fatal, cite; v: free search + the named-group minimum set, extended
     as needed).
   - **The Bueno/Brunner boundary memo** (lane ii): verify in the primary sources exactly what that line
     physically updates (readout-only?) — the claim's most likely confuser; quote, don't paraphrase.
   - **Reproducible search trail appendix:** queries run, databases/engines, dates, hit counts.
2. **Any FATAL or AMBIGUOUS finding → stop and escalate**: post to `decisions_needed.md` +
   `escalate_to_human.md` with the primary attached. Adjudication is Lucas's, per PR-15 disposition.
3. Results entry in `results_log.md` (candidate counts per lane, verdict summary, anomalies).

### Gates
Every PR-15 lane swept + logged; every non-clear verdict grounded in a primary source with quote;
ambiguities escalated, never resolved in-memo; memo dated 2026-06; search trail reproducible.

### Out of scope
Claim **wording** (PR-2/S0.8 — Supervisor); roadmap/ledger edits; any simulation code; the S0.7-lite
envelope (separate task, after PR-10 freezes); debt #2/#3 memos (separate S0.L tasks, due at S0.2/S0.3).

### Deployment
Web search + primary-source reading (web access required); expected days, not hours; no compute spend.

---

## ✅ DONE — S0.1.1: S0.1 closeout (decision-free Critic edits before S0.2)

**Assigned:** 2026-06-09 · **Closed:** 2026-06-09
**Supervisor:** Claude Opus 4.8
**Status:** ✅ COMPLETED 2026-06-09 — all four edits landed + gates PASSED (107/107; transient F1 validation
**positive**: ringdown <1e-9 vs closed form, pole recovered from trajectory <1e-5, 2-ring beat = eig
splitting <2%). Supervisor ACCEPT (no Critic gate needed — this *executed* the Critic's own prescribed
edits; scope held, F2/F6 untouched). S0.1 is now **fully closed**. Results in `results_log.md`.
**Next ACTIVE task:** pending Lucas — D-08-2/D-08-3 steer + **D-2026-06-09-1** (front-load debt #1 /
PR-15 white-space gate; see `decisions_needed.md` + `escalate_to_human.md` E-2026-06-09-2).
**Source:** `critic_review_s0-1-results.md` (APPROVE-WITH-EDITS) — the four **decision-free** items the
Critic wants landed before PR-1/PR-2 freeze. The two *framing* items (F2 mapping-class, F6 gain-free κ_ext)
are Supervisor/PR-2 work and wait on Lucas's D-08-2/D-08-3 steer — **not** in this task.

### Goal
Close the validation/hygiene gaps the Critic raised. **Do not touch the architecture framing** (that is the
Supervisor's mapping write-up + PR-2). Small code/prose/test edits only.

### Deliverables
1. **(S0.1-F1, HIGH) Transient-dynamics validation.** The gate currently proves the mapping by
   *construction* (van Loan exact; steady-state + pole algebra) but never integrates the ODE forward and
   compares the *transient* to an independent reference. Add: (i) single-ring **ringdown + step response**
   vs the closed form `a(t)=a₀e^{(iδ−κ)t}` **and** vs an independent integrator (scipy/torchdiffeq RK45 on
   `da/dt=Ma+Bu`), asserting decay rate κ **and** oscillation frequency δ *in the time domain*; (ii) a
   **2-ring μ≠0** case whose hybridized **beat frequency** matches Im(eig(M)) splitting. The contribution
   *is* the dynamical mapping — it deserves a positive time-domain check.
2. **(S0.1-F3, MEDIUM) Fix the 2× memory-units slip** (results-log finding 4 + `mapping_notes` §4). "329
   round trips" pairs with **3.29 ns** (amplitude/state memory `1/κ_i`), not 1.65 ns (photon lifetime
   `Qi/ω₀=1/2κ_i`). The **code already distinguishes them**; fix the **prose** to report the
   **amplitude/state-memory convention consistently** (3.29 ns / 329 rt; **49.4 ns** / 4937 rt at Qi=3e7) —
   this is what PR-2 sizes the task against.
3. **(S0.1-F4, MEDIUM) Fix the B2 high-roughness row + state the criterion band.** The row mixes a
   160-MHz-based `Q_cross=3.0e5` with 125-MHz-based ratios (tabulated 5.2/77.6 vs the consistent 6.6/99).
   Recompute to **one γ**. Add that the criterion is `2γ≳κ_tot` (HWHM, the *conservative* choice) and that
   the FWHM `2γ≳2κ_tot` shifts every `Q_cross` ×2 — carry the ~2× band. (Conclusion unchanged under both.)
4. **(S0.1-F7, MEDIUM) Fix the registry mislabel.** The conservative corner (Qi=2e6 / 0.172 dB/cm) must not
   be attributed to the named foundry product. **Rename it `SiN_foundry_conservative`** (no foundry
   attribution) **and** add a separate `SiN_LIGENTEC_AN800` with the **actual** demonstrated numbers
   (≈0.05 dB/cm, Qi≈6.8e6 derived, primary-sourced). Keep the conservative corner as the Gate-ii candidate
   cell (F13); only the name/citation changes. Re-run loss↔Q + FSR tests over the updated registry.

### Out of scope (Supervisor / later)
- **F2** (mapping-class reframing → diagonal/S4D, LinOSS as special case) — Supervisor mapping write-up +
  PR-1/PR-2, pending the D-08-2 steer. **F6** (gain-free κ_ext actuation vs readout independence) — PR-2.
- **F5** (B2 primary-source verification) — S0.L, before-paper. **F8** (thermal self-heating; pole-region
  realizability completeness — state-dim/placement) — register for the S0.3 substrate + PR-2 sizing.

### Gates
Transient tests pass (decay rate + frequency in the time domain; 2-ring beat matches eig splitting); full
suite green; memory prose one (amplitude) convention; B2 row internally consistent + criterion band stated;
registry relabeled + tests green.

### Deployment
Local CPU; hours. No cloud.

> **Parallel:** Lucas is steering D-08-2/D-08-3 (low-risk — Supervisor + Critic aligned). This closeout is
> decision-free and upstream of the framing, so it runs safely alongside that steer.

---

---

## ✅ DONE — S0.1: Oscillator↔SiN-ring mapping + realizable pole region

**Assigned:** 2026-06-08 · **Closed:** 2026-06-09
**Supervisor:** Claude Opus 4.8
**Status:** ✅ COMPLETED 2026-06-09 — gate PASSED; two architecture decisions surfaced (D-08-2 mapping fork, D-08-3 backscatter) → Critic + Lucas. Results in `results_log.md`.
**Roadmap:** `stage0_roadmap.md` v3 §S0.1 (scope (B) Lucas-blessed 2026-06-08). **Prereqs:**
`photonic-ssm-proposal-v0_5.md` §3 (mapping) + §4 (pole region); the salvaged `static_rings.py` (the
**CW-limit reference** — S0.0); `preregistration.md` (this phase *feeds* **PR-2** task-sizing and **PR-4**
$Q$/$\kappa_\text{ext}$ — it does **not** freeze them); `results_log.md` (S0.0).

### Goal
Build the **first new dynamical core**: the temporal-CMT single-ring model and the coupled-ring →
$N$-oscillator LinOSS forward model (the recon established this is new code — `pnn-multilayer`'s ring code
is static/CW). Bound the realizable pole region, and deliver the three scope-(B) results that the headline
claim and the downstream pre-registration depend on. **This is simulation + model-building + a literature-
sourced physics bound; the formal mapping write-up + white-space wording are the Supervisor's** (role
boundary) — you produce the verified model, the plots, and the data/tables those will cite.

### Deliverables
1. **Dynamical single-ring temporal-CMT model** — $\dot a = (-\kappa_\text{tot}+i\Delta\omega)\,a +
   \sqrt{\kappa_\text{ext}}\,s_\text{in}(t)$, pole $s=-\kappa_\text{tot}+i\omega_\text{res}$ (with
   $\kappa_\text{tot}=\kappa_i+\kappa_\text{ext}$). **Not** the salvaged static transfer function. Verify
   the **CW limit recovers the S0.0 salvaged Lorentzian + the analytic add-drop reference** within a
   stated tolerance (this is the S0.1 gate).
2. **Coupled-ring → $N$-oscillator LinOSS forward model** — map to the eigenvalue form
   $a_i=-e^{\alpha_i}+i\beta_i$; integrate in time. **Honor both architecture constraints (now roadmap
   gates, F18): (3a)** gradients flow through the optical state (checkpointed unroll — the
   `TrainingAwareDynamicSOAPerMode` pattern, no `no_grad`/detach); **(3b)** expose **full state
   trajectories** in the API (adjoint/RHEL will need them at S0.4).
3. **Realizable pole-region bound (§4)** — stability is free; memory is **loss-limited**; $\beta_i$ is
   **FSR-bounded**; poles placed by drift-stable thermo-optic trim. Plot the pole region with the
   **loss/gain → $|\lambda|$ (memory-length) relation** across the registry's $Q$ span (foundry
   $2\times10^6$ → class-leading $3\times10^7$).
4. **(B1) Trainable-parameter set + actuation map** — a table: which physical parameters are
   in-situ-trainable and by what actuator — detunings $\beta_i$ (heaters); pole **real** parts (tunable
   bus–ring coupling, e.g. MZI-assisted couplers, and/or per-ring gain); inter-ring coupling topology
   (direct photonic-molecule vs bus-mediated). Flag the device-complexity cost of each. *(Load-bearing for
   the white-space sentence — feeds PR-2; the Supervisor writes the claim wording from this.)*
5. **(B2 / F19) Backscatter / CW–CCW mode-splitting bound** — literature-sourced: plug cited
   surface-roughness backscatter splitting-rate figures into splitting-rate-vs-$\kappa_\text{tot}$ across
   the registered $Q$ range; state **where "one ring = one complex pole" breaks down** (expected
   negligible at foundry $Q\approx2\times10^6$, *not* at $\sim10^7$). **Recommend** whether S0.3 needs an
   optional mode-splitting knob. Cite sources (this is the physics input; framing is Supervisor/S0.L).
6. **(B3 / F13.3) Memory-vs-readout-SNR ($\kappa_\text{ext}$) trade** — derive/plot it: deep undercoupling
   maximizes memory ($|\lambda|$) but collapses I/O residues + detector SNR. Show the realizable region as
   a function of the $\kappa_\text{ext}$ policy. *(Feeds PR-4 — you characterize the trade; you do **not**
   pick the operating point.)*
7. **(F13.1) Registry Q/loss self-consistency fix** — each SiN entry must be internally consistent:
   register one of $(\alpha, Q_i)$ as primary and **derive** the other ($Q_i=\omega n_g/(c\,\alpha)$); add
   a **loss↔Q self-consistency test** alongside the existing FSR check; reconcile `SiN_LIGENTEC_AN800`
   (currently $Q_i=2\times10^6$ *and* 0.03 dB/cm, which disagree ~5.7×). **Do NOT pick the operating $Q$**
   — that is PR-4 at S0.3 (foundry-gated). Keep all registry entries; just make each self-consistent.

### Key gates and questions
- **Gate:** dynamical poles match a coupled-mode/transfer-function reference within a stated tolerance,
  **and** the CW limit recovers the S0.0 static reference. Report the tolerance you pre-state.
- Confirm (3a)/(3b) are honored in the new dynamical model (not just inherited from the salvaged layer) —
  a test that a loss at time $T$ receives gradient through the ring state from an input at $t\ll T$.
- B2: if the literature says splitting bites *within* the registered $Q$ range, say so loudly — it
  threatens the core one-ring-one-pole abstraction and changes S0.3.
- Flag anything that makes the §3 mapping less clean than the proposal assumes (e.g. dispersion, TPA/FCA
  at the powers gain requires, thermal nonlinearity) → `decisions_needed.md`.

### Deployment
Local CPU; model-building + analysis + a focused literature pull for B2. Minutes-to-~1–2 days. No cloud.

> **Next:** Executor stops at completion and reports to `results_log.md`. Per the gate model, the **Critic
> reviews S0.1 results before S0.2 starts**. The Supervisor then writes the mapping result + white-space
> wording, and specs S0.2 (which freezes PR-1/PR-2/PR-10).

---

---

## ✅ DONE — S0.0: Repo init + selective salvage + smoke test

**Assigned:** 2026-06-08 · **Closed:** 2026-06-08
**Supervisor:** Claude Opus 4.8
**Status:** ✅ COMPLETED 2026-06-08 — all S0.0 gates passed (7/7 assets ported + tested; SPSA anchor reproduced; both architecture constraints honored; smoke i–iii green). Results in `results_log.md`.
**Rulings:** D-1 → **(a) selective salvage** (Lucas, 2026-06-08); D-2 → **`git init`** (Lucas, 2026-06-08).
**Prereqs:** read `shared/tooling_recon.md` (**the salvage manifest, §4** — authoritative for this task);
`shared/stage0_roadmap.md` (S0.0, S0.1, S0.3); `photonic-ssm-proposal-v0_5.md` §3. Reference repo
`~/Documents/pnn-multilayer/` @ `e2eec80` is **read-only — do not modify it.**

### Goal
Stand up the Project_SSM repo under git, **selectively salvage** the seven manifest assets (copy + adapt
into the new repo, *not* a git fork), and prove the toolchain with a salvage-validation smoke test. **The
SSM core is NOT built here** — the dynamical ring model, LinOSS layer, substrate, and estimators are
S0.1+. This task is infrastructure + salvage + toolchain proof only.

### Deliverables
1. **`git init`** the repo; `.gitignore` (Python, `__pycache__`, `.venv`, results/data); initial commit.
   `requirements.txt` (torch-only after decoupling, per recon). A `README` listing salvaged-vs-new.
2. **Salvage the 7 manifest assets** (recon §4 table). Each salvaged file carries a provenance header
   `# salvaged from pnn-multilayer @ e2eec80 : <original path>`, has its 1–2 contact points decoupled,
   and its associated test ported and **passing**:
   - `adaptation/perturbation_gradient.py` → SPSA estimator + FD/autograd diagnostic + **forward-pass
     accounting**; inject the loss-fn + forward API (decouple `compute_nmse_field` / `forward_batched`);
     re-run the FD-vs-autograd validation (<1% RMS anchor).
   - `physics.py` ~57–136 (gain / ASE / NL functions) → substrate gain + ASE knobs (lift-as-is).
   - `channels/dynamic_soa.py` (esp. `TrainingAwareDynamicSOAPerMode`) → dynamic in-loop gain +
     checkpointed-unroll pattern. **See constraint (3a).**
   - `channels/mrr_platforms.py` → SiN platform registry (lift-as-is). **Add** CORNERSTONE SiN and a
     class-leading ultra-high-$Q$ entry as *additional* entries. **Do NOT pick the operating $Q$** — the
     `2×10⁶` (foundry) vs `>10⁷` (class-leading) choice is a parked S0.2/S0.3 pre-registration decision.
   - `mrr_primitives.py` static Lorentzians + `drift_inject` + their tests → CW-limit **test
     references** + S0.3 drift knob.
   - `equalization_mrr_rc.py` ridge readout + delay-embedding → §5.3 reservoir-readout baseline stub.
   - one sweep skeleton (`sweep_phase4a_mrr1`) + `evaluate.py` JSONL pattern → generic bake-off runner
     scaffold (strip task-specific content; keep the resume-safe keyed-JSON orchestration pattern).
3. **Two architecture constraints, baked into the new skeleton from line one** (recon §3 warnings):
   - **(3a) Gradients must flow through the optical state.** Do **not** copy the repo's `no_grad`/`detach`
     ODE-integration style (correct for forward-only channels, fatal for our substrate where BPTT/PAT/
     adjoint need state gradients). Use the `TrainingAwareDynamicSOAPerMode` checkpointed-unroll pattern.
   - **(3b) Expose full state trajectories** in the forward/substrate API (the adjoint and RHEL
     estimators need them; the old `CascadedMRR_RC.forward` hides intermediate state — don't repeat that).
4. **Smoke test (salvage-validation, not core):** (i) all salvaged assets import and their ported tests
   pass; (ii) the salvaged **static Lorentzian** reproduces the analytic add-drop CW transfer function
   within a stated tolerance; (iii) the platform-registry FSR self-consistency test passes. *(The
   dynamical single-ring → pole model and its CW-limit match are the first task of S0.1, not here.)*

### Key gates and questions
- All 7 assets ported with provenance headers + passing re-run tests; SPSA FD-vs-autograd anchor reproduced.
- Report which contact points needed decoupling, any assets that resisted lifting, and confirm the two
  architecture constraints are honored in the skeleton.
- Honest flag if any salvaged asset drags in equalization assumptions that couldn't be cleanly severed.

### Deployment
Local CPU; minutes-to-~1 day. No cloud.

> **Parallel track:** the Critic is reviewing the Stage-0 roadmap concurrently
> (`shared/critic_instructions_stage0-roadmap.md`). S0.0 is pure infrastructure/salvage — upstream of any
> roadmap change — so the two run safely in parallel; Critic findings would affect S0.1+ (the science),
> not S0.0.

---

## ✅ DONE — S0.0a: Tooling reconnaissance (read-only)

**CLOSED 2026-06-07.** Report `shared/tooling_recon.md`. Finding: `pnn-multilayer` ring code is
static/CW (no optical-memory dynamics) → the SSM core is new under either ruling; salvage value is in the
estimator/infrastructure layer (SPSA + pass-accounting, rate-equation gain, SiN registry, drift, ridge
readout, sweep scaffold, static Lorentzians as CW-limit test refs). Recommended (a) selective salvage
(~1 day vs ~3–5 days for clean start). → Lucas ruled (a) + `git init` on 2026-06-08; folded into S0.0 above.

<!-- COMPLETED tasks accumulate below, newest first -->
