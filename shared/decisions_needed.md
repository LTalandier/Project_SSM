# Decisions Needed

The **Executor** posts design questions here when something is unclear or requires a methodology
decision it wasn't given. The **Supervisor** answers (or escalates to Lucas via
`escalate_to_human.md`). Resolved items move to the bottom with the resolution + date.

---

## OPEN

### 🔴 D-2026-06-11-1 — Gate-i G3 adjudication: gate FAILED as measured, and the published anchor itself does not survive a faithful official-code rerun

**Raised by:** Executor, 2026-06-11. **Supersedes the route question in D-2026-06-10-2's
addendum:** Lucas chose route (a)-variant in-session same evening — his own vast.ai credits
($7.44 ceiling, E-2026-06-10-5, RTX 3090 @ $0.245/h) — the GPU parity gate passed
(1.2–1.5e-7, bit-deterministic), the gated-5 ran to completion, and the frozen gate-miss
diagnosis is complete. **Blocks:** the joint Gate-i verdict / S0.2-1 closure. **No tuning;
no gated rerun; the measurement stands as measured.** Evidence: results_log S0.2-1 addenda;
raw `results/s0_2/gate_i/` (ours) + `results/s0_2/gate_i/xcheck_official/` (official).

**Measured facts (one RTX 3090; strict-fp32 torch / pinned-version jax):**

| run | per-seed (2345/3456/4567/5678/6789) | gated mean | gate ≥ 90.6 |
|---|---|---|---|
| published (paper) | σ = 4.4 claimed | 95.0 | (anchor) |
| **official code, faithful rerun** (commit 05a8353; jax 0.4.28 / eqx 0.11.4 / optax 0.2.2; official pickles; their runner) | 97.22 / 83.33 / 97.22 / 97.22 / 77.78 (σ ≈ 9.3) | **90.5556** | **FAIL (−0.044 pp, unrounded per PF-F8h)** |
| **our port** (GPU parity 1.2–1.5e-7; CPU≡JAX 2.4e-7 of record) | 19.44 / 88.89 / 94.44 / 97.22 / 55.56 | **71.1111** | FAIL |

**Diagnosis (closed; neither mechanism is a port bug):**
1. **Zero-gradient absorbing state of the official objective** (`−Σ y·log(softmax+1e-8)`,
   their train.py L87, ported verbatim per the closure rule): fp32 softmax saturation →
   p_true underflows to exactly 0 → total gradient exactly 0.0 forever. Step-instrumented
   (entry at steps 1–7; step-0 |grad| ~4×10³ then ≡0); bit-deterministically reproduced.
   **Incidence: ours 4/8 protocol seeds (2345@1, 6789@4, 7890@7, 8901@1); official code on
   8 fresh seeds 2/8 (9012 → 50.0 %, 22222 → 11.1 %, same flat-loss signature).** Fisher
   p ≈ 0.6 — the frameworks are statistically indistinguishable; **the trap belongs to the
   published method at this anchor.** The published Walker set is trap-free by draw
   (P ≈ 20 % at the observed rate).
2. **Anchor non-transfer:** trap-free official seeds still spread σ ≈ 9.3 (incl. 77.8, 83.3)
   ≈ 2× the published σ = 4.4, and the official rerun mean sits below the frozen gate. The
   PF-F9d premise (published mean −1σ transfers to a faithful rerun) is empirically false
   for G3. Port-side checks all clean: init distributions audited line-by-line vs
   models/LinOSS.py + eqx 0.11.4 source (lim = 1/√in everywhere; A/steps U[0,1), B ±1/√H,
   C ±1/√ssm, D N(0,1)); healthy-seed means agree (ours 93.5; official non-trap band
   77.8–97.2, mean 90.6).

**Adjudication options (Supervisor → Lucas; any PR-1 change is Lucas-only re-registration):**
- **(O1)** Record Gate-i = **G1 PASS ∧ G3 FAIL-as-measured** with the anchor-instability
  finding attached. The gate's *purpose* (validate the in-house layer against published
  behavior) is arguably served — G1 passed, and for G3 the layer matches the official
  implementation's behavior distribution while the published anchor fails its own faithful
  rerun. Costs: the letter of the gate fails; the roadmap consequence of a Gate-i miss
  needs naming.
- **(O2)** **Re-register the G3 criterion** (e.g. anchor on official-as-rerun-on-named-
  hardware; a trap-conditional statistic; or swap the anchor to the S0.2-0 menu's next
  candidate — MotorImagery / D-LinOSS 61.1±2.0, the tightest published σ). Cleanest
  pre-registration hygiene; costs a re-freeze round.
- **(O3)** Both: record FAIL-as-measured + register a replacement anchor going forward.
- **Carry regardless (debt #2 / paper record):** the LinOSS-IM EigenWorms 95.0±4.4 headline
  is consistent with a favorable seed draw from an fp32 **optimization** collapse of its own
  objective (−Σ y·log(softmax+1e-8); entered by training steps 1–7, not at init) with
  material incidence in both stacks (point estimates 15–50 %, small-n CIs wide), and does
  not reproduce under a faithful rerun (90.56, σ 9.34) — first-hand support for the
  project's "in-house BPTT ceiling, not published numbers" anchoring philosophy (PR-3).
  *(Wording per Critic GA-F3(ii)/(iii) + GA-F7, applied 2026-06-11 in the S0.2-1R pass.)*

**Executor state:** stopped on this item per PR-1 ("on a miss: stop"). Annex-3 not run
(post-verdict idle work — moot pending adjudication). Box destroyed; spend ≈ $1.0 of $7.44
(exact figure in the results entry).

**Supervisor analysis + recommendation (2026-06-11):** I independently re-derived every
load-bearing statistic — both gated means (71.1111 exact; official rerun 90.5556 < 90.6,
σ 9.34), Fisher two-tailed p = 0.608, P(published-set trap-free) ≈ 0.10–0.24 at observed
incidence, healthy-3 = 93.52 inside the published band — all reproduce. The Executor's conduct
under the frozen miss-rule was exactly right (stop; sanctioned cross-check only; zero tuning).
**Recommendation: O3, in the form of the PROPOSED PR-1.1 amendment** now in
`preregistration.md`: (1) the G3 FAIL stays on the permanent record as measured — no
retroactive pass; (2) the G3 criterion is declared **void for anchor instability** (its frozen
premise — published mean −1σ transfers to a faithful rerun — is empirically false: the
reference implementation fails its own threshold); (3) **no replacement published anchor**
(MotorImagery re-opens the registered preprint exclusion; any replacement carries the same
just-fired transfer risk; the registered downstream reference is the PR-3 in-house ceiling
anyway); (4) Gate i re-registered as **G1 PASS ∧ the numerical-identity parity dossier** —
adjudicated *purpose-served*, letter-FAIL recorded beside it; (5) F-G3 becomes a reportable
finding (binding S0.8 wording) + a new freeze rule: **reference-implementation transfer check
before any externally-anchored threshold freezes**. Process: this is squarely
pre-registered-gate territory → **Critic review of the diagnosis + the amendment**
(`critic_instructions_g3-adjudication.md`), then **Lucas signs** (E-2026-06-11-1). S0.2-1
stays open until the adjudication lands; no Executor work exists in the meantime.

**Update (2026-06-11, post-Critic — supersedes two figures above):** verdict
**APPROVE-WITH-EDITS, "sign PR-1.1 with these edits"** — all applied (v2 in the ledger).
Per **GA-F3**, my "P(trap-free) ≈ 0.10–0.24" above (and the entry's "P ≈ 20 %" / "Fisher
p ≈ 0.6") are point-estimate readings only — the 95 % CIs span [0.005, 0.85], Fisher ranges
0.15–0.61 across denominators, and the 8-vs-8 design has ~9 % power; the operative logic is
the fallback already stated: **any material incidence voids the criterion.** Per **GA-F2**
the operative transfer evidence is dispersion (σ 9.34 = 2.1× published) + environment
sensitivity, not the 0.04-pp shortfall. **GA-F1:** the official fresh-8 numbers were
console-only (unarchived; box destroyed) → demoted in v2; archived local regeneration =
**Executor task S0.2-1R** (ACTIVE). **GA-F4** (E-5(iii) RNG deviation unrecorded)
reconciliation rides S0.2-1R. Awaiting Lucas on E-2026-06-11-1.

**Update (2026-06-11, S0.2-1R landed + accepted):** the archived local regeneration
supersedes the console figures — official fresh-8: **0/8 strict-trap, 1/8 behaviorally
collapsed** (22222 chance-frozen across all 4 evals); ours annex-local: **2/3** (8901@1;
9012@555, the first observed late entry; 7890 alive); the same seed's trap status flips with
environment in both stacks. I re-ran the pre-declared classifier from the archived npy/jsonl
trails — every claimed figure reproduces. GA-F4 reconciliation + GA-F7 corrections are on the
record; PR-1.1 v2's incidence bullet now cites only archived, per-environment figures (the
stale Fisher values computed on superseded counts are dropped; the operative logic — any
material incidence voids, ruling rests on dispersion + mechanism — is unchanged). **Sole
remaining step: Lucas signs PR-1.1 v2 (E-2026-06-11-1).**

### ✅ D-2026-06-10-2 — S0.2-1 G3 runtime flag → **RESOLVED 2026-06-10 by Supervisor: option 1+3 (local, gated-5 first)**

**Ruling:** run G3 **locally, gated-5 seeds first** (3-parallel as proposed, ~3–4 days), **annex-3
trails at idle** after the gate verdict files. Cloud (option 2) **declined as default**: the entire
validation chain (parity at ~2e-7, BN bit-exactness) is CPU-float32 — moving the *gated* statistic to
a new numerical environment buys ~4 calendar days at the cost of a GPU-parity revalidation on the
measurement itself, plus a spend approval, for $0-stakes runs on an otherwise-idle machine. The gate
verdict is complete with gated-5 (annex is non-gating by construction, PF-F8g). *Standing offer to
Lucas (no action needed):* if calendar time matters, say so — option 2 is ~$30–60 and would then go
through the spend escalation; default is local. **While G3 computes, the Executor proceeds to S0.3-0
(now ACTIVE in task_queue.md)** — the G3 runs need no babysitting; results file when they land.

**Addendum 2026-06-10 (eve) — ruling executed, then Lucas paused: route choice REOPENED for
resumption.** The runs launched 18:48 (seeds 2345/3456/4567 in flight, 5678/6789 queued); Lucas
SIGSTOPped them 19:36 (~47 min in, pre-first-eval; PIDs 1412412 + 1412415/16/17, state T verified,
~3.2 GB resident) — **the 3–4-day local calendar cost is rejected.** At resumption, Lucas picks:
**(a) cloud A100 ~$30–60** (spend escalation pro forma + a GPU parity-revalidation pass before the
gated runs — the harness is rerunnable there); **(b) resume local** (`kill -CONT` the PIDs; survives
session closure, NOT reboot; reboot = protocol-clean restart from step 0); **(c) stay paused.**
Full pause state: `docs/project_status_2026-06-10_pause.md`.

**Raised by:** Executor, 2026-06-10. **Blocks:** the G3 (EigenWorms) gated runs only. **Not blocked:**
G1 (Heartbeat) — in-budget (~1.5 min per 1000-step eval cycle, all 8 seeds projected ≲ 2–3 h total,
4-parallel), launched under the frozen PR-1 protocol; the PF-F1 rider; everything else in S0.2-1.

**This is a wall-clock/logistics question only — zero protocol content.** No truncation, no chunking
of sequences, no config change is on the table (PR-1 frozen; the task spec itself names sequence
truncation a protocol deviation). The in-house layer is validated: 12 unit tests + cross-framework
forward parity vs the official JAX model (transplanted weights) at float32 precision — full-model
probs agree to ~2e-7 (both anchors, train + inference modes), BN state updates bit-exact (G1), and
the full-length L=17,984 SSM layer to 1.5e-5 abs. Param counts reconciled exactly (trainable 10,738 /
133,765; published 10,936 / 134,279 = trainable + BatchNorm state buffers, 2H+1 per block).

**Measured (this machine: 20-core CPU, torch 2.11 fp32, no GPU), after optimization** (custom
analytic-backward associative scan — same recurrence, ~1.9× faster than the naive autograd path):
- G3 per training step (batch 4, L=17,984): **4.38 s** → one 1000-step eval cycle (incl. the official
  full train+val inference evals): **74.5 min**.
- Early stopping (official: break after 11 consecutive non-improving evals) is the unknown:
  at a realistic 16–40 cycles to stop → **20–50 h per seed** (central ~31 h); hard cap (no early
  stop, 100 cycles) 124 h/seed.
- 8 seeds: sequential ~250 h; **3-parallel (6 threads each, RAM-safe) ≈ 4.5–6 days wall-clock**;
  gated-5 only ≈ 3–4 days, annex-3 following ≈ +1.5–2 days.

**Options:**
1. **Run locally as-is (recommended).** Zero spend, zero protocol risk. Start the 5 gated seeds now
   (3-parallel, ~3–4 days), annex 3 after. The machine is otherwise idle; G1 finishes today and its
   results entry can be filed meanwhile (results entry then amended with G3, or split G1/G3 entries).
2. **Cloud GPU** (would need Lucas approval via `escalate_to_human.md` — house rule). A single A100
   runs the official-scale job fast (the paper's own runs were GPU); est. ≲ $30–60 spot for all
   8 seeds incl. setup risk. Buys ~4 days of calendar time at the cost of an approval round-trip +
   environment-parity revalidation on GPU (the parity harness is rerunnable there).
3. **Reduced-seed interim** (run gated-5 only, defer annex-3 to idle time later) — halves the wait;
   annex is non-gating by construction (PF-F8g), so the gate verdict is complete with option 3.

**Executor recommendation:** option 1 (or 1+3: gated-5 first — the gate verdict lands ~2 days sooner,
annex trails). Will hold G3 until the Supervisor rules.

### ✅ D-2026-06-09-2 — PR-15 search verdicts → **RESOLVED 2026-06-10 by Lucas** (rulings: PR-15.1 signed · Böhm boundary-cite · Wu no-outreach-yet, W1 default · retrievals pending)
Resolution recorded in `preregistration.md` **PR-15.1 amendment block** (the authoritative record) +
`escalate_to_human.md` (RESOLVED cluster). Gate state: provisional one-sided PASS under PR-15.1,
contingent on Zhao/NTT/Fisher reading non-fatal. Original item (kept as filed):

**Raised by:** Executor, 2026-06-09. **Blocks:** the pre-S0.2 continuation gate (and hence
S0.2–S0.5 authorization). S0.L-1 sweep complete: **0 FATAL confirmed**, but **1 potentially-FATAL
AMBIGUOUS** (Wu et al., eLight 5:7 (2025) — on-chip optical RNN trained in-situ by SPGD; trained
voltage set U unenumerated → q1 unresolved; q2/q3 verified verbatim), the
**calibration-vs-training boundary class** (Milanizadeh 2020 gradient-descent ring-filter tuning
satisfies q1∧q2∧q3 *mechanically* — same issue as the Critic's WS-F1/q4 amendment, found
independently by both modalities), **Böhm 2022** (hybrid digital recurrence, also found by both),
and **8 unreachable primaries** (top: Zhao LPR 2025, Wiley-paywalled). Everything filed with
primaries at `escalate_to_human.md` **E-2026-06-09-4**; memo `docs/s0_L/debt1_whitespace_search.md`;
results entry in `results_log.md`. **Not for the Supervisor to adjudicate** (PR-15: ambiguous →
Lucas; rule frozen — no in-pipeline amendment); Supervisor action = reconcile scheduling (Critic
Part-2 audit + PR-10/S0.7-lite) around the pending ruling. Executor stopped.

**Supervisor (2026-06-09) — scheduling actioned; adjudication untouched (it is Lucas's).** S0.L-1
accepted → DONE. Critic **Part 2 green-lit** (+ addendum in `critic_instructions_whitespace-pr15.md`:
merge both candidate tables, reconcile the asymmetries both ways, re-classify under PR-15.1 once
signed). Executor re-tasked to **S0.7L-0** (PR-10 assumption sourcing — the gate's other input advances
while the ruling pends; envelope itself waits for the PR-10 freeze). Synthesis + recommendations on the
four rulings (amendment / Wu / Böhm / retrievals): **E-2026-06-09-5**. Gate closes on: Lucas's rulings +
Critic Part 2 + the lite envelope.

### D-2026-06-08-1 (parked) — SiN operating $Q$ for the substrate (pre-registration)
**Raised by:** Supervisor (from the S0.0a recon). **Blocks:** nothing yet; **due at S0.2/S0.3.**
The salvaged platform registry ships SiN `Qi=2×10⁶` (foundry-conservative corner), but the proposal
cites `Q>10⁷` (class-leading, e.g. damascene SiN). Which do we pre-register as the operating point for
the S0.3 substrate (and the memory-length / gradient-survival story)? S0.0 adds both as registry entries
but does **not** choose. **To decide at S0.2/S0.3 pre-registration**, with the Critic's roadmap review
weighing in (checklist item 6). Likely: register a *range* (conservative foundry → aspirational) and
report sensitivity, rather than a single value.
**Update (2026-06-09):** now **coupled to D-08-3 (resolved)** — PR-4's realistic cell gains a
roughness/splitting sub-parameter (evaluated at the operating κ_ext), and the platform tension (high-Q
best-memory vs splitting-prone; CORNERSTONE low-Q splitting-safe but memory-poor ~33 rt) is part of this
same operating-point choice. **Resolve together at PR-4** (blessed constraints logged in
`preregistration.md` Notes). Registry now spans 4 SiN corners: 2.3e5 → 2e6 → 6.8e6 → 3e7 (S0.1.1/F7).

---

## RESOLVED

### ✅ D-2026-06-09-1 — Front-load debt #1 (white-space kill-search) to pre-S0.2 → **ADOPTED IN FULL**
**Resolved 2026-06-09 by Lucas ("ok go", E-2026-06-09-2).** Raised by the pnn-multilayer Supervisor
session (cross-project crosscheck Lucas requested); Supervisor **CONCURRED** with four strengthenings —
all adopted: (1) **rule-form kill-criterion** (FATAL iff q1 *internal-to-recurrence* ∧ q2
*on-device-in-the-loop* ∧ q3 *gradient-based/-estimating*; F15 lanes locate, the rule decides; (iv)-type
evolutionary priors non-fatal but cited; ambiguous → Lucas with primaries); (2) **one-sided PASS**
semantics (a clean search does not certify; dated S0.8 sweep + wording refinement stay); (3)
**two-modality search** (Executor systematic sweep, primary-source-verified — the B2/F5 lesson — +
independent Critic adversarial pass + F14 reconciliation); (4) **one pre-S0.2 continuation gate** =
PR-15 verdict + S0.7-lite envelope + Lucas's program-level call (the "first" is collectible only at
Stage 1+; Stage 0 alone = methods paper). **Landed as:** `preregistration.md` **PR-15 (🔒 FROZEN
2026-06-09** — the full rule lives there**)**; roadmap **v3.1** (re-paced S0.L, dependency graph, S0.2
precondition, Lucas-gates); Executor task **S0.L-1 ACTIVE**; Critic spec
`critic_instructions_whitespace-pr15.md`. F14 stands as a *data-dependency* statement for #2/#3; D-09-1
adds a *value-at-risk scheduling* principle — no conflict (Critic to confirm in its pass). Full original
argument + adjudication: git `954d2d2`.

### ✅ D-2026-06-08-2 — Mapping class: diagonal-complex-SSM vs real-LinOSS pairs → **(a) COMPLEX-DIAGONAL (S4D/DSS), corrected framing**
**Resolved 2026-06-09 by Lucas ("ok go").** The bake-off simulates the **diagonal complex-pole SSM
(S4D/DSS class)** — one ring = one trainable complex pole (hardware-minimal; conjugate-pairing would
double the ring count). **Framing per the Critic's S0.1-F2 correction (adopted over the Supervisor's
initial "it *is* diagonalized LinOSS"):** the ring bank *natively realizes* the S4D/DSS class; uncoupled
+ real-I/O it reduces **exactly** to LinOSS (conjugate-pair special case); trainable inter-ring μ is a
**mild generalization beyond** standard diagonal-A LinOSS. Conditions adopted: soften the "oscillatory
LinOSS" branding; benchmark transfer = **debt #2** (published LinOSS validates only the μ=0 reduction;
the coupled form is validated via the PR-3 BPTT-on-substrate ceiling); **pin the readout at PR-2**
(coherent-quadrature = real-linear/LinOSS-equivalent vs intensity = nonlinear) + address the F6 κ_ext
dual-role; white-space claim unaffected (trains the B1 set {κ_tot,j, δ_j, μ_jk}). **Landed as:**
`preregistration.md` Notes (PR-2 constraints); roadmap v3.1 (S0.2); `docs/s0_1/mapping_result.md` (the
Supervisor write-up). Full thread: git `954d2d2`.

### ✅ D-2026-06-08-3 — Backscatter mode-splitting bites within the registered Q range → **ROUGHNESS-GATED KNOB + PR-4 SUB-PARAMETER**
**Resolved 2026-06-09 by Lucas ("ok go").** S0.1-B2 found splitting is **process-roughness-limited, NOT
cleanly Q-gated** (clean damascene-class: single-pole holds at foundry Qi, crosses ~4×10⁶ HWHM / ~8×10⁶
FWHM; rough subtractive: 21–75 % of modes split at Qi=2×10⁶ already) — contradicting the roadmap's
"negligible at foundry Q" assumption. Adopted (Executor recommendation + Supervisor + Critic
strengthenings): S0.3 carries an **optional CW/CCW splitting knob gated by a process-roughness flag**,
default **ON except the clean-damascene corner**; PR-4's realistic cell gains a **roughness/splitting
sub-parameter**, splitting evaluated at the **operating κ_ext** (overcoupling suppresses the doublet);
if the single-pole substrate relies on the clean corner, PR-4 states that assumption explicitly;
**resolve jointly with D-08-1** at PR-4. B2 crossover numbers **provisional** until F5 primary-source
verification (S0.L, before-paper). Platform tension recorded: best-memory (high-Q) ↔ most
splitting-prone. **Landed as:** `preregistration.md` Notes (PR-4 constraints); roadmap v3.1. Full
thread: git `954d2d2`.

### ✅ D-2026-06-05-1 — Salvage `pnn-multilayer` code vs. clean start → **(a) SALVAGE**
**Resolved 2026-06-08 by Lucas.** Selective salvage per the `shared/tooling_recon.md` §4 manifest (7
assets: SPSA+accounting, gain/ASE functions, dynamic rate-equation SOA, SiN registry, static Lorentzians
+drift, ridge readout, sweep/JSONL scaffold). Copy + adapt with provenance headers (`pnn-multilayer @
e2eec80`), decouple contact points, re-run tests. SSM core written fresh either way. Folded into S0.0
(now ACTIVE). `pnn-multilayer` stays read-only.

### ✅ D-2026-06-05-2 — `git init` Project_SSM now? → **YES**
**Resolved 2026-06-08 by Lucas.** Repo initialized under git as part of S0.0; provenance of salvaged
code tracked from the first commit.
