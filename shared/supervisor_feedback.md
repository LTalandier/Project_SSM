# Supervisor Feedback / Direction Log

Supervisor's running notes: direction, progress assessments, and responses to Executor results and
Critic reviews. Newest at top. This is the Supervisor's voice — the Executor and Critic can read it
for context, but task assignments live in `task_queue.md` and review specs in `critic_instructions*.md`.

---

## 2026-06-09 (night) — PR-15 both modalities in: 0 confirmed FATAL, 4 rulings to Lucas; S0.L-1 ACCEPTED; S0.7L-0 ACTIVE

Both modality outputs landed within hours of dispatch. **The two-modality protocol earned its keep on
day one:** the Executor's sweep found **Wu eLight 2025** (the one potentially-fatal candidate — q1
unresolved), Milanizadeh, and Zhao LPR 2025 — none in the Critic's blind list; the Critic's blind pass
found **Fisher 1987** and, more importantly, **the criterion defect itself** (WS-F1: no task-objective
condition → the frozen letter is satisfied by cavity-servo and laser-regime literature nobody would
call training). Both independently hit the same calibration-boundary wall — the strongest possible
internal evidence the q4 amendment is right.

**Supervisor positions (recommendations only; adjudication is Lucas's per the frozen disposition):**
sign **PR-15.1** (q4 + WS-F3 weight-tied rider + WS-F5 taxonomy); on **Wu**, author-query + the **W1
dissipative-resonator wording hedge** in parallel, gate not blocked on the reply; on **Böhm**, the
parameter-physicality qualifier + cite-by-name; **Zhao LPR 2025 retrieval is the top human ask**. Full
packet: **E-2026-06-09-5**.

**Pipeline:** S0.L-1 ACCEPTED → DONE (protocol followed exactly — stopped, escalated, adjudicated
nothing). Critic **Part 2 green-lit** with addendum (merge tables, reconcile asymmetries both ways,
re-classify under PR-15.1 once signed; scrutiny list included). Executor → **S0.7L-0** (PR-10
assumption sourcing; envelope waits for the freeze). **No PASS issued by anyone** — the gate closes on
Lucas's rulings + Part 2 + the lite envelope. My next deliverables: PR-10 draft (from S0.7L-0 output) +
the W1/W2 wording variants for PR-2.

---

## 2026-06-09 (evening) — Lucas "ok go" → all three resolutions executed; S0.L-1 (PR-15 search) ACTIVE

Lucas blessed D-08-2 + D-08-3 + D-09-1 in one word. Executed, in order:
1. **PR-15 registered + 🔒 FROZEN** (`preregistration.md` — the ledger's first frozen entry): rule-form
   kill-criterion (q1∧q2∧q3), five search lanes + named-group minimum set, two-modality protocol,
   one-sided PASS, disposition (FATAL/AMBIGUOUS → Lucas with primaries). PR-2/PR-4 constraint notes added.
2. **Roadmap → v3.1**: S0.2–S0.5 behind the **pre-S0.2 continuation gate** (PR-15 + S0.7-lite + Lucas's
   program call); S0.L re-paced (#1 front-loaded; F14 pacing stands for #2/#3); dependency graph,
   S0.2 precondition + D-08-2 architecture resolution, Lucas-gates section updated.
3. **Decisions resolved**: D-09-1, D-08-2, D-08-3 → RESOLVED (condensed; full threads in git `954d2d2`).
   E-09-1/E-09-2 → RESOLVED; touchpoints list updated (next asks: PR-10, then the gate).
4. **Mapping result written** (`docs/s0_1/mapping_result.md`) — the Stage-0 objective-(a) statement with
   the corrected S4D/DSS framing, the validated mapping table, the pole-region envelope (3.29→49.4 ns),
   B1/B2/B3, and the claim-discipline section. Paper section drafts from this.
5. **Dispatched**: Executor task **S0.L-1 ACTIVE** (the PR-15 existence search — apply the frozen rule,
   primaries only, escalate FATAL/AMBIGUOUS); Critic spec `critic_instructions_whitespace-pr15.md`
   (blind adversarial pass first, then memo audit + criterion audit + F14 reconciliation; reports to
   Lucas; gate waits on it).

**Next Supervisor deliverable:** the **PR-10 draft** (S0.7-lite assumptions: conversion energies,
DAC/ADC rates, named digital-baseline class + sources, operating scale) → Lucas freezes → S0.7-lite runs
as the next Executor task after S0.L-1. Then the continuation gate with both probes in hand.

---

## 2026-06-09 (latest) — S0.1.1 ACCEPTED (S0.1 fully closed); D-2026-06-09-1 (front-load debt #1) → CONCUR

**S0.1.1 closeout: ACCEPT, no reservations.** All four decision-free edits landed exactly to spec;
107/107 green. The load-bearing one is **F1 positive**: the dynamical mapping now has a *time-domain*
confirmation against an independent RK45 — ringdown <1e-9 vs closed form, pole (κ *and* δ) recovered from
the trajectory <1e-5, 2-ring beat = Im(eig) splitting (2μ) <2%, with a μ=0 no-beat contrast. F3 (memory
now in one amplitude convention: 3.29 ns/329 rt → 49.4 ns/4937 rt — the numbers PR-2 sizes against), F4
(B2 one-γ row + HWHM/FWHM ×2 band; conclusion unchanged, matching the Critic's own re-derivation), F7
(conservative corner de-attributed; real AN800 entry primary-sourced, 0.051 dB/cm primary / Qi=6.8e6
derived). Honest flags are good practice (step-test scaling; n_g=1.97 bookkeeping choice). Scope held —
F2/F6 untouched, as specced. No Critic gate needed: this *executed* the Critic's own prescribed edits.

**D-2026-06-09-1 (cross-project: front-load the white-space kill-search): CONCUR, adopt (a)+(b)+(c)**
with four strengthenings — rule-form kill-criterion (q1 internal-to-recurrence ∧ q2 on-device-in-the-loop
∧ q3 gradient-based/-estimating; F15 (i)–(iv) are search *lanes*, the rule decides; (iv)-type priors
non-fatal but cited; ambiguous → Lucas with primary sources); one-sided PASS semantics (clean search ≠
certification; S0.8 dated sweep stays); two-modality search (Executor systematic sweep, primary-source
verified — the B2/F5 lesson — + independent Critic adversarial pass + F14 reconciliation); and folding
PR-15 + S0.7-lite + the value call into **one pre-S0.2 continuation gate**. Sharpening for Lucas: the
"first" is only collectible on hardware (Stage 1+), so this gate is really the **program-level
continuation call**. Full adjudication in `decisions_needed.md`; escalated as **E-2026-06-09-2**. Nothing
folded into roadmap/ledger until Lucas blesses (PR-15 must be registered *before* the search it governs).

**Pipeline state:** no ACTIVE task. Three items at Lucas: D-08-2 + D-08-3 (steer; Supervisor+Critic
converged) and E-2026-06-09-2 (the reorder + strategic flag). On the steers: mapping write-up + PR-15
registration + roadmap re-pace + S0.2 spec (PR-1/PR-2/PR-10 freeze) + Executor/Critic dispatches.

---

## 2026-06-09 (later) — Critic reviewed S0.1 → APPROVE-WITH-EDITS; closeout ACTIVE; decisions ready for Lucas

Strong independent review (re-derived every load-bearing number — most reproduce to the digit). 2 HIGH ·
7 MEDIUM · 1 LOW; **S0.2 can proceed** after four before-PR-freeze edits. I concur with the whole review;
the one that matters most is a correction to **my own** framing:
- **F2 (HIGH) — I over-claimed.** The ring bank is a **diagonal complex-pole SSM (S4D/DSS class)**, not
  "diagonalized LinOSS" flatly; LinOSS is the **conjugate-pair special case** (uncoupled + real-I/O), and
  trainable inter-ring μ is a *generalization beyond* standard diagonal-A LinOSS. Benchmark transfer is
  open debt #2, not a given. **Adopting in full** — honest framing, pre-empts "you said LinOSS but trained
  a coupled S4D." Reshapes the mapping write-up + PR-1/PR-2.
- **F1 (HIGH)** — the gate proves the mapping by *construction* (van Loan), never validates the transient
  vs an independent integrator. Real gap for a *dynamical*-mapping contribution → closeout.
- **F3** units slip (329 rt = 3.29 ns *state* memory, not 1.65 ns photon lifetime — matters for PR-2
  sizing); **F4** B2 row arithmetic + criterion band; **F6** gain-free κ_ext is *both* damping actuator and
  readout knob (muddies the reservoir-baseline contrast → PR-2 + the F7 fairness contract); **F7** registry
  mislabel (conservative corner ≠ named AN800); **F8** thermal self-heating + realizability completeness
  (state-dim / pole-placement precision) → **register for S0.3 substrate + PR-2 sizing.**

Both decisions now have **converged Supervisor + Critic** recommendations (Critic sharpened both;
`decisions_needed.md`): **D-08-2** → diagonal/S4D class with LinOSS as special case, pin the readout;
**D-08-3** → roughness-gated knob, evaluate at the operating κ_ext, default-ON off the clean corner.

**Actioned:** S0.1.1 closeout ACTIVE (F1 transient test, F3 units, F4 B2 row, F7 registry relabel — all
decision-free). **Held for Lucas:** the D-08-2/D-08-3 steer (low-risk — aligned). **Next once steered:** I
write the mapping result with the corrected diagonal/S4D framing, fold F6/F8 into PR-2, spec S0.2 (freezing
PR-1/PR-2/PR-10).

## 2026-06-09 — S0.1 DONE (gate passed); two architecture decisions surfaced; Critic dispatched on S0.1 results

S0.1 is a strong result — gate genuinely passed (poles match the CMT ref: uncoupled <1e-3, ZOH exact for
PWC; CW limit recovers the S0.0 static at $O(1/\text{finesse})$, <1% at the $F\approx1000$–15000 SiN rings
sit at; both architecture constraints verified in the **new** model, checkpointed==plain to 0.0 grads;
99 tests). It did what good S0.1 work should: surfaced two findings that move the downstream plan.

**Two decisions (both → Lucas, recommendations in `decisions_needed.md`; both routed to the Critic):**
- **D-08-2 mapping fork** — one optical ring = one *complex* pole (complex-diagonal SSM / S4D-like), not a
  real-LinOSS conjugate pair. **My rec: (a) complex-diagonal, framed as the *diagonalized* LinOSS/D-LinOSS**
  (hardware-minimal — 1 ring = 1 trainable complex pole; damping = pole real part = κ_tot = the proposal's
  loss=damping story; white-space claim intact). Caveat → debt #2: confirm equivalence + benchmark
  transfer; real-valued I/O handled at the readout. Freezes at PR-2.
- **D-08-3 backscatter** — splitting is **roughness-limited, not Q-gated**, and bites at foundry Q for
  rough subtractive processes (the roadmap's F19-derived "negligible at foundry Q" assumption is wrong for
  rough SiN). **My rec: accept the optional roughness-gated splitting knob in S0.3; promote
  roughness/splitting to a PR-4 sub-parameter.** Platform tension to carry: high-Q = best memory = most
  splitting-prone, while CORNERSTONE's low Q is splitting-safe but memory-poor (~33 rt). B2's *quantitative*
  crossover is provisional (search-aggregated → verify-before-citing); act on the qualitative finding now,
  confirm primary sources (S0.L) before any paper claim.

Also good: **B1** — a **gain-free minimal trainable set suffices for the white-space claim** (strengthens
it); **B3** $\kappa_\text{ext}$ trade bounded + tested; **F13.1** registry reconciled (AN800 Qi=2e6 primary
→ loss 0.172 dB/cm). **Held my own deliverable — the mapping write-up + white-space wording — until D-08-2
settles** (central content; writing it on an unresolved fork would be premature).

**Next:** Critic reviews S0.1 results (gate before S0.2) → Lucas decides D-08-2/D-08-3 with Critic input →
I write the mapping result + spec S0.2 (freezing PR-1 / PR-2 / PR-10).

## 2026-06-08 (later still) — Lucas signed off ("accept all, scope (B) blessed"); roadmap v3 issued; S0.1 ACTIVE

Folded the entire Critic review into **`stage0_roadmap.md` v3** (changelog block at top maps each phase
edit to its finding) and fixed the stale "fork ring model + training engine" line in **CLAUDE.md** (F17).
`preregistration.md` is adopted — 14 entries, structure locked, all UNSET, freezing per-phase. **S0.1 is
ACTIVE** (`task_queue.md`) with the scope-(B) deliverables: the dynamical temporal-CMT core + LinOSS
forward model + pole region, the trainable-parameter/actuation map (B1, → PR-2 + the white-space wording),
the literature-sourced backscatter/mode-splitting bound (B2/F19), the memory-vs-readout-SNR
$\kappa_\text{ext}$ trade (B3, → PR-4), and the registry Q/loss self-consistency fix (F13.1). Role
boundary held: Executor builds the model + plots + data; **I** write the mapping result + white-space
sentence from them.

**Next Supervisor actions:** (1) when S0.1 reports → the Critic reviews S0.1 results before S0.2 (gate
model); (2) write the mapping result; (3) spec S0.2 — which freezes PR-1 (Gate-i margin), PR-2 (bake-off
task + architecture + partition), and PR-10 (S0.7-lite, due *before* the task choice), all to Lucas first.
The standing per-phase pre-registration touchpoints are tracked in `escalate_to_human.md`.

## 2026-06-08 (later) — Both parallel tracks back: S0.0 DONE (green), Critic APPROVE-WITH-EDITS

S0.0 closed clean — all gates green (60/60 tests; SPSA FD-vs-autograd anchor RMS 1.1e-7; both architecture
constraints enforced by tests; operating $Q$ correctly left unchosen). Honest flags are all the right
ones; notably the Executor independently surfaced the same `SiN_LIGENTEC_AN800` Q/loss inconsistency the
Critic re-derived in F13.1 — two sessions, one defect → real.

Critic filed **APPROVE-WITH-EDITS** (1 CRITICAL · 9 HIGH · 11 MEDIUM · 1 LOW). I concur **in full** — a
model review; no phase moves; every defect is a pre-registration entry or a text edit. Load-bearing:
**F7** (fairness contract — twin==substrate makes PAT trivially win), **F10.1** (Gate-ii corner case lets
a failed PAT/SPSA still walk onto hardware), **F2** (score vs the BPTT-on-substrate ceiling), **F12** (the
pre-registration ledger).

**Actioned now (decision-free):** S0.0 → DONE in `task_queue`; created `shared/preregistration.md` (the
F12 ledger, 14 entries, all UNSET); banner on the roadmap flagging the v3 fold + the F17 stale-S0.0 text;
escalation updated with the decision surface. **Held for Lucas** (`escalate_to_human.md` E-2026-06-05-1):
accept-in-full sign-off; the consequential gate/metric/$Q$ framings; the F2/F13/F19 expansion of S0.1's
scope. **Roadmap v3 + the CLAUDE.md "Codebase plan" fix (F17) happen in one pass once Lucas signs off** —
deliberately not front-running his adjudication of a CRITICAL methodology finding by silently rewriting
the gates.

## 2026-06-08 — Rulings in; S0.0 ACTIVE; Critic dispatched on the roadmap (parallel)

Evaluated the S0.0a recon (`tooling_recon.md`) — high quality; its central correction stands: the
`pnn-multilayer` ring code is static/CW, so the SSM core is new under either ruling and the salvage value
is the estimator/infra layer. Lucas ruled **D-1 → (a) selective salvage**, **D-2 → git init**.
- **S0.0 rewritten and flipped ACTIVE:** repo init + git + the 7-asset salvage manifest (provenance
  headers, contact-point decoupling, re-run tests) + two architecture constraints baked in from line one
  — **(3a)** gradients must flow through the optical state (no `no_grad`/`detach`; checkpointed unroll),
  **(3b)** expose full state trajectories (adjoint/RHEL need them) — + a salvage-validation smoke test.
  The dynamical ring→pole core is deferred to S0.1 (kept S0.0 to infra/salvage only).
- **Critic dispatched on the Stage-0 roadmap, in parallel** (`critic_instructions_stage0-roadmap.md`):
  9-item checklist incl. the advantage-envelope-pull-earlier question, metric integrity, shared-substrate
  fairness, RHEL echo honesty, Gate-(ii) guardrail, the parked SiN-$Q$ pre-registration, the four debts,
  and recon integration. Verdict → `critic_review_stage0-roadmap.md`. Safe to run alongside S0.0 (S0.0 is
  upstream infra; Critic findings hit S0.1+).
- **Parked decision logged:** D-2026-06-08-1 — SiN operating $Q$ (`2×10⁶` foundry vs `>10⁷` class-leading),
  due at S0.2/S0.3 pre-registration.
- **Next Supervisor action:** ingest the Critic's roadmap verdict, fold AMEND findings into the roadmap,
  bring it to Lucas for sign-off; then `/executor S0.1` once S0.0 reports DONE.

## 2026-06-07 — First task = read-only tooling reconnaissance (S0.0a)

Rather than guess on D-1 (salvage `pnn-multilayer` vs. clean start), the first Executor task is a
**read-only reconnaissance** (S0.0a, now ACTIVE): assess per-module liftability — especially whether
`equalization_ringbank.py` is a usable head start for the S0.1 oscillator↔ring mapping — and recommend
(a) salvage / (b) clean start with evidence, written to `shared/tooling_recon.md`. Writes no code,
modifies nothing, commits to no decision. Lucas rules on D-1 after reading the report; then S0.0 (repo
build + smoke test) goes ACTIVE. "Fork" was sloppy terminology on my part — corrected to "salvage"
(copy + adapt into a new repo; `pnn-multilayer` stays untouched) throughout.

## 2026-06-06 — Realigned scaffold to proposal v0.5

Lucas replaced the proposal with `photonic-ssm-proposal-v0_5.md` (supersedes the TFLN-era v0.2). Major
shifts absorbed into the whole scaffold (CLAUDE.md, roadmap, task_queue, executor/critic instructions,
skills, memory):
- **Platform TFLN → silicon nitride** (round-trip loss / intrinsic $Q$ is the binding FOM; SiN class-leading).
  TFLN is now fallback-only. Foundries: CORNERSTONE / LIGENTEC.
- **Training: RHEL demoted; PAT + SPSA now primary + hardware-committed.** Stage 0 is a **four-method
  bake-off** (SPSA, PAT, recurrent adjoint, RHEL) on **one shared dissipative ring model**. Guardrail:
  parallel in simulation, singular in hardware.
- **Primary metric flipped** to sample-efficiency-to-target-accuracy under realistic noise;
  gradient-cosine-error demoted to a secondary diagnostic (old Gate (ii) retired).
- **Conservatism–damping tension dissolved** → damping is a free knob (D-LinOSS for accuracy).
- **Systems-advantage envelope** (latency/energy incl. conversion overhead) is now an explicit Stage-0
  deliverable (S0.7); the §10 advantage premise is the largest conceptual risk.
- Verification debts now **four**: sharpened white-space; LinOSS/D-LinOSS/Mamba-3; **Er:SiN NF**;
  **recurrent-adjoint gap**.
- RHEL must commit to a **concrete phase-conjugation echo sub-model** (no idealized operator).

Roadmap rewritten to v2: S0.0 fork → S0.1 mapping → S0.2 LinOSS baseline (Gate i) → S0.3 shared substrate
→ S0.4{a PAT/SPSA, b adjoint, c RHEL+echo} → S0.5 bake-off (Gate ii, headline) → S0.6 damping → S0.7
advantage envelope → S0.8 write-up; S0.L literature in parallel. **Next Supervisor actions once approved:**
`/critic stage0-roadmap`; then flip S0.0 → ACTIVE and `/executor S0.0`.

## 2026-06-05 — Project bootstrapped

- Read the proposal (`photonic-ssm-tfln-proposal-v0.2.md`) and replicated the `pnn-multilayer`
  3-session setup (Supervisor / Executor / Critic) into this repo.
- Drafted `stage0_roadmap.md` (S0.0–S0.7 + S0.L literature track) from proposal §6.
- Queued S0.0 (repo + tooling fork + smoke test) as **PROPOSED**, pending Lucas's go and Critic review
  of the plan. Two open decisions logged (`decisions_needed.md`): fork vs. fresh; `git init` now.
- **Next Supervisor actions once approved:** (1) `/critic stage0-roadmap` to get an independent read on
  the plan and the pre-registered margins; (2) flip S0.0 → ACTIVE and `/executor S0.0`.
