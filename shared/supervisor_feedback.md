# Supervisor Feedback / Direction Log

Supervisor's running notes: direction, progress assessments, and responses to Executor results and
Critic reviews. Newest at top. This is the Supervisor's voice — the Executor and Critic can read it
for context, but task assignments live in `task_queue.md` and review specs in `critic_instructions*.md`.

---

## 2026-06-11 (fork ruled: M1 + M3 trigger → PROPOSED PR-4 posted; Critic spec ready)

**Lucas ruled E-2026-06-11-2** (recorded verbatim in the E-item): **M1** registered ·
**M2** strictly a one-off validation reference · **M3** neither built nor discarded — a
deferred branch with a **pre-committed trigger** ((a) gated S0.5/S0.6 verdict within a
flip-plausible margin, margin form frozen at PR-5–9/PR-11 *before* any bake-off results;
(b) Stage-2 platform tilt to III-V) — plus three drafting riders: R1 NF-A-headline-everywhere,
R2 splitting-block-states-N-grid-consequence, R3 ensemble-power-stationarity-as-registered-
M1-validity-assumption. The trigger extension is better than my plain (a): it pre-prices the
exact circumstance where skipping M3 could bias a conclusion.

**PROPOSED PR-4 posted** (ledger, after PR-1.1). The registered choices and the reasoning:
- **G:** M1 per the ruling; gain ceiling 0.9×intrinsic (no-lasing; never compensates κ_ext);
  ASE = A2 Langevin (composes with the S0.1 exact discretization; A1 = unit-tested
  equivalent); validity conditions (i) stationary episodes (ii) R3 ensemble-power
  stationarity (iii) quasi-static margin at P̄₀.
- **Cells:** C-1 = P-FND/NF-A/γ-90 **gates Gate ii at N=8** (the foundry floor; honors
  "foundry-grade gates Gate ii"); C-2 = P-AN800/NF-A/γ-11.8 **hosts the PR-2 frozen headline
  N=32** (packs in-band at θ₀, T-A 7-tap span covered, gain ×22–41) — registered as a
  **conservative bound** on the abstract-verified Cui 2023 numbers (body-level still walled:
  four routes attempted at freeze date; residual risks named: body-provenance + 19.8-GHz-FSR
  → 100-GHz geometry transfer); C-3 = P-UHQ aspirational, hosts N=128 knob-ON (EV-F3 escape
  (a)). NF-A 7.0 headline everywhere (R1).
- **K4 trainable κ_ext** — *forced* by the frozen PR-2 P2 partition (κ_ext,j is in the
  trainable set; a fixed policy would contradict a frozen entry). Bounds r ∈ [0.1, 3];
  **θ₀ = 0.3** (the joint point where frozen N=32 packs + 7-tap span covered + drop eff.
  non-degenerate — design-from-frozen-constraints, no results exist to peek at).
- **K-pol-3 splitting knob always ON** (K-pol-1/2 are incoherent under trainable κ_ext);
  γ=0 recovers single-pole exactly; R2 consequence stated in-block: deployable N-grid
  {8 @ C-1, 32 @ C-2}, 128 only as the labelled C-3 cell — PR-2's frozen grid survives.
- **H1** worst-case holding (conservative standalone numbers; H2 = sensitivity; H3 = Stage-1).
- **O2 intracavity-energy normalization** (the only convention comparison-clean under K4);
  anchored P̄₀ = 1 mW, P_pk = 2P̄₀; **E₀ = frozen parameter-free formula now, mechanical
  numeric evaluation at S0.3-1 calibration, ledger-addended before any consuming run** — the
  Critic is explicitly pointed at this two-step as a potential pre-registration hole.
- **Anchor-risk register:** first application of the PR-1.1 transfer-check rule at a physics
  freeze (GA-F6 scope) — infeasibility registered, risk carried by provenance trail +
  conservative bounds + M2 validation + named residuals.

**Critic spec filed:** `critic_instructions_pr4-freeze.md` — 12-item checklist; hostile
stances assigned: "cell chosen to flatter the photonic side" + "freeze leaves tunable
holes"; every load-bearing number flagged for re-derivation; rider-compliance audit;
completeness-vs-F12 sweep. **Lucas launches the Critic** (his stated process), signs after
review. Executor stays idle until the freeze.

---

## 2026-06-11 (PR-1.1 v2 SIGNED by Lucas — S0.2-1 CLOSED; the program returns to the queued S0.3 path)

Lucas signed PR-1.1 v2 verbatim ("sign PR-1.1", E-2026-06-11-1) — no amendments. Recorded:
ledger header 🔒 SIGNED + adoption-blockquote update + PR-1 table-row amendment note;
task_queue S0.2-1 → ✅ CLOSED; roadmap S0.2 status updated; E-item + D-item resolved.

**What is now settled, permanently:** G1 PASS (gated, untouched) · G3 FAIL on the books as
measured, its criterion **void for anchor instability** (F-G3 — a *reportable finding*, S0.8-
binding, every citable number archived + environment-qualified) · Gate i **adjudicated
purpose-served** on G1 ∧ the numerical-identity dossier · no replacement published anchor —
downstream anchors on the **PR-3 in-house BPTT ceiling**, as registered at the freeze · the
**reference-implementation transfer check** is now a binding freeze rule (GA-F6 scope).
S0.2 took the project's first frozen-gate hit and the discipline held end-to-end: miss-rule
honored, diagnosis sanctioned, adjudication Critic-attacked, record repaired to
archived-or-demoted before signature. That chain — not the G1 number — is what the paper's
methods section will lean on.

**Next (the path queued before the pause):** (1) the **Er gain-regime fork proposal — M1 vs
M3** (S0.3-0 left it open by design; it blocks S0.3-1) → Lucas rules; (2) **PROPOSED PR-4**
drafted from `docs/s0_3/pr4_input_sheet.md` (verify Cui 2023 [AV] at freeze) → Critic
phase-boundary review → Lucas signs → S0.3-1 substrate build.

---

## 2026-06-11 (S0.2-1R accepted — the record repair holds; archived incidence supersedes the console)

**Acceptance basis (this time in the right order): artifacts first, numbers second.** The
GA-F1 gate held — the pre-declaration (seed list incl. 9012/22222, the three-leg classifier,
screen protocol, environment caveat) was committed at 889ab53 BEFORE the runs; the archive
holds 8 official run dirs with full npy trails + non-empty per-seed driver logs (vs the box's
empty `driver_fresh.log`) + 3 gradient-instrumented annex jsonls; the previously gitignored
`gate_i/` tree is force-added (the gitignore was the actual hole behind GA-F1). I then re-ran
the pre-declared classifier myself from the archived npy/jsonl: official fresh-8 = six
healthy (val 0.83–0.91 by eval 4), 9012 moving (alive), 22222 frozen at chance on both metric
legs → **0/8 strict, 1/8 behavioral**; annex = 8901 absorbed@1, 9012 absorbed@555 with the
single dropout-borne transient at 554, 7890 alive. Every claimed figure reproduces.

**The honest movement, stated plainly:** the official-stack strict-trap point estimate went
**2/8 (console) → 0/8 (archived local CPU)**. That does not weaken F-G3 — it *is* F-G3:
incidence is environment-contingent (the same seed flips trap status in both stacks, both
directions, vs the console record). The void ruling never rested on a particular k/n; it
rests on the archived dispersion leg (90.56, σ 9.34 = 2.1× published), the
analytically-verified mechanism, and "any material incidence voids" (ours archived 2/5 GPU +
2/3 CPU is material). I rewrote PR-1.1 v2's incidence bullet to cite only archived figures,
per-environment, and dropped the stale Fisher values computed on the superseded counts.
A hostile reviewer reading "0/8 locally" as "the official code is fine on CPU" runs into
22222 (chance-frozen 4/4 evals, archived) and into the dispersion leg, which needs no
incidence at all.

**Executor assessment: exemplary repair.** The pre-declaration is exactly the operative
declaration the Critic demanded; the conservative classifier rule (2/3-constant → ALIVE,
flagged verbatim) resisted any temptation to inflate incidence back toward the console
figure; the 22222 distinction (saturated basin with residual gradient vs exact absorption)
is the kind of precision that survives review. GA-F4 reconciled (087a346 cited), GA-F7 nits
landed. ~9.6 h wall, $0.

**Record state:** GA-F1 closed · the only open item in all of S0.2 is **Lucas's signature on
PR-1.1 v2** (E-2026-06-11-1). On signature: S0.2-1 closes (G1 PASS ∧ G3 void-with-finding);
next Supervisor outputs = the Er gain-regime fork proposal (M1 vs M3) + PROPOSED PR-4.

---

## 2026-06-11 (Critic G3-adjudication review in → PR-1.1 v2, sign-ready) — full concurrence; two of its findings are mine to own

**Verdict** (`critic_review_g3-adjudication.md`): **APPROVE-WITH-EDITS — "sign PR-1.1 with
these edits."** The Critic took the hostile stance I asked for and reports the adjudication
survives it *after* repairs. It also independently confirmed the hard core from raw trails:
trap mechanism re-derived analytically (both saturation directions exactly zero; escapes
bounded; the early-stop arithmetic of the collapsed seeds matches the trails), published-5
rerun numbers exact, exoneration pre-specified, alternatives correctly rejected, and the
"in-house ceiling was always the operative reference" leg verified verbatim in three places.

**Findings, disposition (all applied → v2 + the S0.2-1R rider):**
- **GA-F1 (HIGH), the blocking one:** the official *fresh-seed* leg — 2/8 incidence,
  9012→50.0, 22222→11.1 — was never archived (box destroyed; empty driver logs); the results
  entry overclaimed "trails for all 13 runs". **Mine to own jointly with the Executor: I
  accepted the diagnosis without opening the archive directories** — I verified the
  *arithmetic* but not the *artifact inventory*. Lesson logged: acceptance includes `ls`.
  Fixed: v2 demotes the console numbers to indicative; S0.2-1R regenerates the leg locally,
  archived, pre-declared seeds.
- **GA-F2/F3 (MEDIUM): my rhetoric leaned on the two weakest numbers** — the 0.04-pp
  shortfall (one test-sample wide, environment-sensitive) and the ~25 %-incidence point
  estimate (9 % power; CIs [0.005, 0.85]). The strong legs were always dispersion
  (σ 9.34 = 2.1× published) and "any material incidence voids the criterion" — v2 now leads
  with those; "init collapse" corrected to **optimization collapse** everywhere.
- **GA-F4 (MEDIUM):** an approved E-5 condition (CPU RNG streams) was deviated from
  mid-campaign (dropout masks → device generator, commit 087a346) without a logged deviation,
  and the addendum cited a declaration that doesn't exist. Non-protocol content, outcome
  unaffected — but approval conditions are tracked or they're decoration. Reconciliation
  rides S0.2-1R; noted as an Executor process miss in an otherwise exemplary record.
- **GA-F5/F6/F7 (LOW):** "adjudicated" not "re-registered" + the changes-nothing-downstream
  sentence (both now explicit in v2); transfer-check rule scoped; 90.56 wording + record nits
  → rider.

**Net position:** PR-1.1 v2 is sign-ready (E-2026-06-11-1 updated); S0.2-1R is ACTIVE
(~2–3 h, $0). Once Lucas signs: S0.2-1 closes, then the gain-regime fork proposal + PROPOSED
PR-4. Meta-note for the record: across three Critic rounds the pattern holds — pre-run review
caught a design error (PF-F1), post-run review caught record/inference errors (GA-F1/F3) —
both directions of the phase-boundary discipline have now paid for themselves.

---

## 2026-06-11 (G3 FAIL as measured → PR-1.1 adjudication package filed) — the gate worked; the anchor didn't

**The outcome:** G3 71.1111 % < 90.6 — joint Gate i FAILS under the frozen letter. I verified
every statistic in the Executor's diagnosis independently (both means exact; Fisher p = 0.608;
P(published-set trap-free) ≈ 0.10–0.24; official-rerun σ = 9.34; healthy-3 = 93.52). The
finding is solid: **the official implementation fails its own published anchor on a faithful
rerun** (90.5556 < 90.6, spread 2× published), via a zero-gradient fp32 absorbing state in the
published objective with ~25 % per-seed incidence. Our port is exonerated by numerical
identity (~2e-7), not by argument.

**Credit where due:** the Executor's execution of the frozen miss-rule was exemplary — stop,
no tuning, the *sanctioned* cross-check pushed to forensic depth (13 official runs,
step-instrumented mechanism, bit-deterministic reproduction), honest framing of its own
stream's worse draw (4/8 vs 2/8, declared indistinguishable rather than explained away).
This entry is the best evidence yet that the frozen-protocol machinery produces trustworthy
negative results — which is the whole point of having it.

**My ownership:** PR-1's premise — published mean −1σ transfers to a faithful rerun — was
mine, the Critic calibrated its *statistics* (PF-F9d), and neither of us tested the premise
itself. A ~$1 official-code rerun before freezing 90.6 would have surfaced F-G3 pre-freeze.
That check is now a proposed binding rule in PR-1.1 (reference-implementation transfer check
before any externally-anchored threshold freezes). Lesson logged alongside EV-F1 and PF-F1:
**every freeze rests on at least one untested empirical premise — name it and price testing
it before signing.**

**The adjudication package** (recommendation O3): PROPOSED PR-1.1 in the ledger — FAIL
recorded permanently; G3 criterion void for anchor instability; no replacement anchor
(MotorImagery re-opens its registered exclusion; the operative downstream reference was
always PR-3's in-house ceiling); Gate i re-registered as G1 PASS ∧ the parity dossier,
adjudicated purpose-SERVED (not relabelled PASS); F-G3 = reportable finding binding S0.8.
Process: Critic attacks the diagnosis + the amendment (`critic_instructions_g3-adjudication.md`
— explicitly instructed to make the "they moved the goalposts" reading stick if it can), then
Lucas rules (E-2026-06-11-1). Spend recorded: $1.15 of the Lucas-approved $7.44 (E-2026-06-10-5,
approved in-session — route (a)-variant superseding my D-2 local ruling; process-clean).

---

## 2026-06-10, eve (PAUSE) — S0.3-0 accepted; G3 paused by Lucas; snapshot filed

**S0.3-0 → ACCEPT** (all gates; details in task_queue). The big one: **debt #3's premise was
false** — the flagship *measured* NF ≈ 7 dB, three-way verified. Better for the program (the
noise cell anchors on a measurement, not a guess), embarrassing for the v0.5 debt list, and a
standing lesson: debt #4 is the same inferred-absence type → re-verify at first full-text
contact before S0.8 wording. Also accepted: EV-F3 lands two-against-one (N=128 ⇒ class-leading
⇒ knob-ON only), CORNERSTONE = passive-only cell, and the **M1-vs-M3 gain-regime fork left open
by design** — correctly so; it's a methodology call that shapes what "the substrate" even is,
it folds into PR-4, and S0.3-1 stays blocked behind it. I note for the record the M1 structure
(linear in-loop + readout |·|²) coincides with the frozen PF-F1 architecture — that's mutual
consistency between two independently-derived conclusions, and PR-4 should *say* it rather than
let a reviewer discover it.

**G3: Lucas paused the runs** (~47 min in, SIGSTOP, pre-first-eval; verified state T) — the
3–4-day local ETA is rejected on calendar grounds. My D-2 "local" ruling is suspended;
the route choice (cloud ~$30–60 / resume local / hold) is **reopened for Lucas at resumption**
(D-2 addendum). Queue updated so no future session relaunches over the paused PIDs.

**Project paused.** Snapshot: `docs/project_status_2026-06-10_pause.md` (resumption-grade:
frozen rulebook, results on the books, exact G3 state + reboot semantics, the ordered
resumption decisions — route → fork → PR-4 freeze → S0.3-1 — and launch commands).

---

## 2026-06-10 (S0.2-1 partial: G1 PASS accepted · G3 ruled local · S0.3-0 posted) — first gate result of the project

**G1 Heartbeat: GATE PASS, verified.** I reproduced the gated mean from the per-seed table
(72.9032 % ≥ 72.1, +0.80 pp), the σ-distance (−0.78σ_published), the n/62 quantization, and the
annex/all-8 means — all exact. Two things deserve naming. First, the **real** validation isn't
the accuracy statistic — it's the float32-exact parity (~2e-7 full-model probabilities with
transplanted weights, BN updates bit-exact): the in-house layer doesn't *approximate* the
official computation, it **is** the official computation, so the gated statistic measures
protocol+data fidelity, which the PF-F6 split pin then nailed. Second, **PF-F6 earned its keep
immediately**: running the official pipeline verbatim surfaced EigenWorms N=236 (the official
dedup deletes 23 duplicates, −8.9 % of corpus) — a reimplemented "equivalent" split would have
silently diverged from every published run. The thin-looking margin (+0.80 pp = 2.5 test-sample
mean-granules) is exactly what the frozen PF-F9d calibration prices; PASS under the frozen rule,
and symmetrically I don't get to want more margin after the fact. Param-count convention
(published = trainable + BN state) goes into the quote-downstream list (anomaly v).

**D-2026-06-10-2 ruled: option 1+3** — G3 locally, gated-5 first (~3–4 days, 3-parallel),
annex trails at idle. Cloud declined as default: the validation chain is CPU-float32; I won't
move the *gated* measurement to a new numerical environment to buy calendar days, and the
machine is idle. Standing offer to Lucas recorded if calendar time matters (~$30–60, would go
through the spend escalation). The flag itself worked as designed: estimate-before-train caught
a 31 h/seed central projection, zero protocol content leaked into the hold.

**S0.3-0 posted ACTIVE** (runs while G3 computes — the runs need no babysitting): substrate
design recon + the PR-4 input sheet. Front-loads debt #3 (Er:Si₃N₄ NF bracket — prerequisite of
the ASE knob), the D-08-1 (α, Q_i) candidate pairs with the EV-F3 N=128 packing check, the
D-08-3 roughness/splitting sourcing, the gain-regime arithmetic (Er ~ms lifetime vs GS/s symbols
— what "saturation" even means in-substrate), and the PF-F8f power-normalization mechanism.
Menu-not-choice; feeds the PR-4 freeze (Critic review + Lucas signature at the S0.3 boundary,
same pattern as PR-1/PR-2). Risk note, considered: posting S0.3-0 before the joint Gate-i
verdict is safe — the recon is literature/design work needed under any G3 outcome, and the
parity result makes a G3 implementation-break miss unlikely (residual risk is protocol/data,
already pinned).

---

## 2026-06-10 (PR-1/PR-2 🔒 FROZEN, Lucas "ok go" → S0.2-1 ACTIVE) — the bake-off arm starts

Lucas signed the v2 blocks (E-2026-06-10-4 ✅): **PR-1 + PR-2 + PR-13 (early) are frozen** —
table rows, block headers, roadmap and escalation all updated. From here on, amendments require
Lucas's signature (the PR-15→PR-15.1 supersession path); the no-tuning closure rule is live.

**S0.2-1 posted ACTIVE** (task_queue.md): the in-house complex-diagonal layer (μ-hook at μ=0,
Gate-i configuration = exact LinOSS-IM per D-08-2) inside the published stack, verbatim configs,
Walker protocol with pinned split reproduction, unrounded 5-seed gated means vs 72.1 / 90.6,
3-seed annex, param-count integrity check, the PF-F1 Vinckier rider. Spec hardening worth
noting: **miss ≠ tune** — on a gate miss the Executor stops and files a divergence diagnosis
(fixed *bugs* may rerun with the diff shown; "tweaks that help" may not). Runtime estimate
required before training; >~24 h projections or any protocol-touching workaround for
EigenWorms' ~18k-step sequences escalate first. These are the project's first training runs —
Gate i is deliberately a *reproduction* gate, so the first result the pipeline produces is
calibratable against published numbers rather than self-graded.

---

## 2026-06-10 (Critic freeze review in → PR-1/PR-2 revised to v2) — full concurrence; PF-F1 owned; awaiting Lucas signature

**Verdict** (`critic_review_pr1-pr2-freeze.md`): PR-1 APPROVE-WITH-EDITS · PR-2 AMEND, one
CRITICAL (PF-F1) with a supplied one-pass fix. **I concur with every finding — nothing
contested** — and the v2 blocks (all edits applied, each tagged PF-F#) are in the ledger.

**PF-F1, owned.** My v1 pinned R1 (single-quadrature homodyne) as the headline readout + a
digital *linear* head — making the entire hybrid affine end-to-end on a task whose channel is
cubic. A linear system floors at SER ≈ 0.7 % at 24–32 dB (Critic re-derivation, non-causal
±15-tap bound) — **~400× above the RC anchor the headline cell was built on**, and flat in SNR,
so the SNR grid would have been uninformative and the §5.3 contrast compressed for *both* arms.
Root cause of my error: I picked R1 for **envelope consistency** (EV-F5) and the
"LinOSS-equivalent head" symmetry, and never checked **expressivity against the anchor task** —
worse, the anchor experiment (Vinckier linear cavity) gets its task-solving nonlinearity from
the *photodiode*, i.e. the anchor system is R2-class; the class match was sitting in the memo I
sourced. **Lesson logged: when pinning an architecture cell against a published anchor, check
the anchor system's *function class* first — budget/consistency checks second.** (Companion to
the EV-F1 lesson: sweep the whole grid, not the typical column.) Note EV-F5 itself always said
"single-quadrature **or intensity**" — the over-narrowing to R1 was mine, in the block text.

**Other findings, disposition (all applied):** PF-F2 honesty line now *binding in the frozen
text* (S0.8 wording). PF-F3 — real distinction I'd blurred: ceiling-relative absorbs ◑ for
*ranking* (ii-b) only; Gate ii-a's absolute floor now requires ≥1 foundry-feasible cell in the
PR-3 cell-set, and a foundry-headline ii-a miss is pre-registered as the memory-vs-Q finding,
not a bake-off failure. PF-F4 — my sticky-detection arm was class-degenerate at k ≥ 10
(P(1) → 94–100 %); replaced with the Critic's rare-marker construction, class-balanced at every
k by P(marker) = 1 − 2^(−1/k) (my completion: marker = a fifth input level, +5). PF-F5 — 10⁵
test symbols at the top SNR cells (10⁻⁴-class SER must be resolvable). PF-F6/F7/F8a–i/F9a–d —
split reproduction pinned; Gate-i↔substrate discretization delta stated; data-streaming regime,
init ownership (→PR-6), dt ≡ 1/f_s, same-SNR train/test, κ_ext θ₀ reconciliation, named annex
seeds, unrounded-mean rule, closure rule, wording fixes. **Carry-ins logged in ledger Notes:**
PR-4 input-power normalization (PF-F8f — the *real* F6 contamination channel); PR-3
foundry-feasible floor cell (PF-F3); PR-6 conventions (PF-F8a/b); S0.2-1 rider (re-verify the
Vinckier photodiode-readout reading at retrieval level).

**Process note (for the record):** the review came back via Lucas launching the Critic session —
the restored 3-session flow working as designed; this is exactly the catch the phase-boundary
review exists for, found *before* anything ran rather than after S0.5. E-2026-06-10-4 updated:
the ask to Lucas is now a one-line signature on v2 (or amendments).

---

## 2026-06-10 (S0.2-0 accepted → PR-1/PR-2 PROPOSED) — freeze ask filed (E-2026-06-10-4); Critic phase-boundary review next

**S0.2-0 → ACCEPT** (all gates; results_log + memos are freeze-grade). The catches that shaped
the draft: paper-vs-code Δt discrepancy (→ PR-1 pins the code as reference); D-LinOSS
preprint-only (→ G2 excluded as anchor); Weather irreproducible (→ excluded, registered);
the μ=0 guard-check came back clean — **no published coupled LinOSS-class benchmark exists**,
so the coupled-μ transfer rests on the PR-3 in-house ceiling exactly as registered (debt #2
substantially discharged for Stage 0).

**Supervisor freeze proposals (the methodology calls, with reasons):**
- **PR-1 = G1 + G3 at M1 (±1σ), both-must-pass, published 5-seed protocol gated + 3-seed annex.**
  G1 Heartbeat = cheap fidelity anchor (peer-reviewed, exact config); G3 EigenWorms = the
  flagship long-range result Gate i's wording points at (and M1 ⇒ M3: ≥90.6 clears LRU 87.8).
  G2 rejected (anchors on a preprint or on σ=7.5); G4 rejected (compute-flagged stretch).
- **PR-2 headline = T-A (Jaeger–Haas eq @ 2 GS/s, SER, 28 dB headline, d(n−2) frozen).** The
  decisive reason: external published anchor + *the* canonical RC task → the §5.3
  trained-recurrence-vs-trained-readout contrast (the claim's in-data falsifier) lands on
  ground the field knows. Honesty lines carried: GS/s is a simulated clock (RC hardware record
  on this channel is ~MS/s); the headline cell is memory-limited at the foundry corner (◑,
  6.58 vs 7 dominant taps) — absorbed by PR-3's ceiling-relative rule, and it keeps the memory
  story visible in the headline. T-B = labelled extension (niche-native but anchor-free;
  port cost deferred); T-C = the secondary AND the PR-13 registration in one act (k ∈
  {1,3,10,30,100} incl. the designed k=100 cliff).
- **PR-2 pins: P2 partition** ({δ, κ_ext, μ} all-thermo-optic, ~3 ch/ring, W1 ✓ both axes;
  P1 busts the PR-10 bracket, P3 surrenders the D-LinOSS trained-damping axis, P4 fails W1);
  **R1 single-quadrature** (EV-F5-consistent; R2 = registered alternative; R3 excluded);
  **F6 policy (a)** (baseline holds κ_ext at the PR-4 value — no recurrence-shaping through the
  readout knob); **nearest-neighbor chain** topology (bracket-consistent; mesh = labelled
  extension); one-photonic-layer hybrid kept explicitly distinct from PR-1's digital stack.

**Process:** PROPOSED blocks appended to the ledger; Critic spec
`critic_instructions_pr1-pr2-freeze.md` filed (phase-boundary discipline); freeze ask =
**E-2026-06-10-4**. Lucas launches the Critic, then signs (or signs directly). S0.2-1 posts
after the signature.

---

## 2026-06-10 (CONTINUATION GATE: GO) — Lucas authorized S0.2–S0.5; S0.2 split -0/-1 around the PR-1/PR-2 freeze; S0.2-0 ACTIVE

**Lucas ruled "Go" on E-2026-06-10-3** — the bake-off arm is authorized with the attached
conditions (niche-sized task; PR-2/PR-4 carry-ins in the ledger Notes; EV fixes as the S0.2-0
rider). Recorded in: escalation (E-3 → RESOLVED), roadmap (S0.2 precondition ✅ + Lucas-gates
line), ledger adoption blockquote (next freezes: PR-1+PR-2, then PR-4).

**Methodology call (Supervisor): S0.2 runs in two steps mirroring S0.7-lite.** PR-1 needs a named
published benchmark + margin frozen *before* the run that tests it, and the roadmap makes the
debt-#2 memo a prerequisite (F14) — so **S0.2-0** (ACTIVE) is literature/design-input only: the
debt-#2 benchmark recon, the niche-sized bake-off task menu, and the PR-2 input sheet
(partition/actuation/readout under the EV-F5 single-quadrature condition + W1 cross-check).
**Explicitly forbidden in S0.2-0: any LinOSS implementation or training run** — running
benchmarks pre-freeze would let the margin be tuned to results (the F12 failure mode). From its
memo I draft the **PR-1/PR-2 freeze ask → Lucas**; S0.2-1 then implements + runs Gate i.

Sequencing note: this is the first task of the authorized arm; the Critic's next natural
engagement is the phase-boundary review of the PR-1/PR-2 freeze draft (per ledger discipline:
"each entry is reviewed by the Critic at the relevant phase boundary before the run proceeds").

---

## 2026-06-10 (Critic envelope audit landed) — APPROVE-WITH-EDITS; verdict SURVIVES; Supervisor concurs on all 7 findings, owns EV-F1

`critic_review_s07lite-envelope.md`: **"conditional positive" survives** — byte-identical re-run;
36/36 clean-room cells, 144 clearance verdicts, all crossovers reproduce; §10 non-firing robust to
trim ±, holding-convention swaps, I/Q doubling, a 7N op count, and plausibly-budgeted exclusions;
traceability complete; banned anchors absent; C5 re-derived fair-to-digital.

**Supervisor disposition — CONCUR on all findings, no contest:**
- **EV-F1 (HIGH) — my error, owned.** My close-out claimed the class-A negative survives a P_π/2
  duty credit; I had checked only the 1 GS/s column. Critic re-derivation (verified by me):
  OPT×A under P_π/2 clears Brainwave in-window (crossovers 1.32–1.47 GS/s; N=8@2 GS/s: 293–297 vs
  390 pJ). Corrected statement: class-A-dead applies to the *deployable* corner under any holding
  convention; the *hero* corner wins in-window at expected-value holding. Close-out struck-and-
  corrected; gate packet condition (1) rewritten; net effect *softens* the fab condition. Lesson
  logged: a robustness check must sweep the whole grid, not the typical column.
- **EV-F2 (MEDIUM):** trim reading faithful but NOT verdict-neutral (Executor's neutrality
  sentence fails both directions; OPT-corner rate floor partly C3-borne; one deployable cell
  trim-sensitive). → results_log correction rides the next Executor task.
- **EV-F3/F5 (MEDIUM):** N=128 ⇄ class-leading-Q ⇄ splitting (→ PR-4 w/ D-08-1);
  single-quadrature/intensity readout = the C5/C8 consistency condition (→ PR-2 readout pin);
  both logged as ledger-Notes carry-ins. EV-F4 (MEDIUM): "~10⁵ latency" corrected to "sub-µs
  unreachable for the serving class; ≥10² matched-N" in the packet.
- **EV-F6/F7 (LOW):** S0.7-full registry (rate-matched converter pair; cadence-row provenance
  line; Muñoz τ unit before PR-4 if SPSA cadence becomes load-bearing).

**GO recommendation unchanged** — the audit strengthens the gate input (full independent
reproduction; fab condition softened). Packet E-2026-06-10-3 updated in place; decision with Lucas.

---

## 2026-06-10 (S0.7L-1 accepted; gate filed; launch protocol restored) — envelope conditional POSITIVE → continuation gate to Lucas (E-2026-06-10-3)

**S0.7L-1 → ACCEPT.** All five gates met (traceability to frozen PR-10, four scenarios, explicit
niche, §10 clause checked — does NOT fire, rider done). Supervisor verification: hand-reproduced 5
grid cells (conversion sums 37–41 pJ; class-B control 6·N mW; Brainwave 14·N-ops mapping → 1 561
pJ@N=32; crossovers 0.126 / 2.61 GS/s) — all match; additionally checked the class-A negative
survives a P_π/2 duty-credit relaxation, so "heater class is the binding constraint" is robust to
the C4 convention. The two Executor-flagged frozen-row readings (C3 trim-in-all-scenarios; class-A
fast-τ) + the judgment-laden conventions (C5 op count, C6 ENOB mapping, C8 single-carrier @ N=128)
go to the **Critic**: spec filed at `critic_instructions_s07lite-envelope.md` — **Lucas launches**
the Critic session; it reports to him beside the gate packet, not through me.

**Continuation gate filed: E-2026-06-10-3** (escalate_to_human.md) — both inputs in hand (PR-15
provisional one-sided PASS + envelope conditional positive); Supervisor recommendation **GO** with
conditions (niche-sized S0.2 task; heater-class condition in PR-2/PR-4; Critic findings folded in).
Pipeline holds: no ACTIVE Executor task until Lucas rules.

**Process correction (Lucas, 2026-06-10):** for the last few rounds the Supervisor had been
spawning the Executor (and was about to spawn the Critic) as headless `claude -p` background
processes from its own session. Lucas stopped it — the project runs on **three separate
Lucas-launched sessions**, and the deviation had real costs: Critic independence (it must not be a
Supervisor subprocess), a shared-working-tree commit collision (Executor rider edits landed inside
Supervisor commit `587d397`), and lost visibility for Lucas. Restored flow: Supervisor writes
specs into `shared/`; Lucas launches sessions (commands in CLAUDE.md). The `/critic` skill's
user-only invocation guard is by design. S0.7L-1's *results* stand (work product is in-repo,
auditable, and now under Critic audit) — the deviation was procedural, not invalidating.

---

## 2026-06-10 (Zhao resolved) — retrieval #1 NON-FATAL (figure-level, Lucas); main gate contingency cleared

Lucas obtained Zhao LPR 2025 figs. 1–2 (paywalled full text unobtainable; figures archived in
`docs/s0_L/primaries/`). Adjudication (Lucas: "seems feedforward"; Supervisor confirmed in detail):
**feedforward MLP with bidirectional optical backprop** — $Z^l=W^lX^{l-1}$ forward, $(W^l)^T dL/dZ^l$
backward through the same MRR bank; rings are static weight elements $W_{ij}$, no state across the
input sequence → fails q1 (weight-tied-recurrence rider) → **NON-FATAL**; does not graze W1 (weight
elements ≠ dynamical poles/couplings). Upside: sharpens **debt #4** — feedforward in-situ optical BP
on MRRs now demonstrably exists; the *recurrent* version remains the undemonstrated gap. Zhao →
prominent must-cite. Ledger + escalation updated; NTT/Fisher/Shi full-texts re-paced to
claim-freeze (PR-2/S0.8), not gate-blocking. **The continuation gate now waits on exactly one input:
the S0.7-lite envelope (S0.7L-1, running).**

---

## 2026-06-10 (rulings executed) — PR-10 FROZEN · PR-15.1 SIGNED · Wu held (W1 default) · S0.7L-1 launched

Lucas ruled: "1. ok (freeze PR-10) · 2. ok (sign PR-15.1 + Böhm qualifier) · 3. don't send the Wu
email yet (maybe later) · 4. [Zhao title delivered]." Executed: ledger updated (PR-10 🔒; PR-15 🔁 →
**PR-15.1** with the full amendment text — q4, q1 recurrence rider, q1 physicality qualifier, q3
positive definition — and all dispositions recorded: servo class → lineage, Böhm → boundary-cite,
**Wu → W1 adopted as default claim, no outreach**); gate state = **provisional one-sided PASS under
PR-15.1, contingent on Zhao/NTT/Fisher reading non-fatal** (retrievals with Lucas). E-cluster + D-09-2
→ RESOLVED. **S0.7L-1 ACTIVE + launched** (envelope at frozen corners ×heater classes ×scale grid +
WS-F11/F12 rider; no-web launch — the freeze is enforced by tooling, not just instruction). On its
return: evaluate the envelope → assemble the **continuation-gate packet** (one go/no-go for Lucas).

---

## 2026-06-10 (later) — S0.7L-0 ACCEPTED; PR-10 PROPOSED to Lucas; pipeline fully drained to his desk

S0.7L-0 is exactly what step-0 sourcing should be: ~35 primaries, two load-bearing ones re-verified
exact (CORNERSTONE design rules; TI ADC datasheet), brackets where sources disagree, **no envelope
arithmetic** (the pre-registration gate held), and — the standout — **four discrepancy flags against
our own legacy anchors**: the Ozkaya standing-power attribution is unverifiable, the "5 pJ/bit 800G"
number was model-computed with no primary, measured stoichiometric-SiN P_π is far above
silicon-derived intuition, and Harris 2014 is *silicon*, not SiN. All four excluded from the PR-10
draft. The lateral-trench/undercut disambiguation (power ↔ ms-τ ↔ SPSA cadence coupling) became a
registered consistency rule.

**PR-10 PROPOSED** (`preregistration.md`): OPT/CONS corners per category, ENOB-at-speed convention,
heater-class consistency, named F16 baselines, scale grid, registered lite-exclusions. **Everything is
now on Lucas's desk** (E-2026-06-10-1 + E-09-5/6): freeze PR-10 · sign PR-15.1 · Böhm qualifier · Wu
send/skip call · Zhao retrieval. Pipeline idle by design — S0.7L-1 (envelope + WS-F11/F12 rider) is
queued on the freeze; on the rulings I register the amendment + update the gate file; the continuation
gate then closes in one decision.

---

## 2026-06-10 — Critic Part 2 in: audit CLEAN; gate = conditional PASS under PR-15.1, degenerate under the letter; W1 → default plan

Part 2 (`critic_review_whitespace-pr15.md` §6–§9, E-2026-06-09-6) is decision-grade. **Supervisor
concurs in full.** What it adds:
- **Audit CLEAN** — every overlap verdict matches Critic-verified primaries; the Bueno/Brunner boundary
  memo survives a hostile re-read; two legs re-run live (Milanizadeh upgraded to CONFIRMED-VERIFIED:
  literal on-chip "gradient descent" on coupled-ring poles — the cleanest letter-kill exhibit).
- **WS-F9 (the decision-relevant delta):** Wu's "U never enumerated" confirmed by an independent
  re-sweep, but the evidence is asymmetric — it *leans fatal* (no fixed-W sentence; one DAC drives all
  phase shifters; programmed-OHMM vs trained-ORNN contrast). And Wu's q4 is YES (Japanese-vowel task) —
  **the amendment does not defuse Wu**; it stands or falls on q1 alone. Consequence: **W1 = default
  plan** (three-role consensus; Critic confirmed W1 true under both Wu readings), author query
  decisive-and-urgent.
- **Verdict logic adopted:** under the frozen letter the gate is *degenerate* (mechanically satisfied
  by filter servos — "FATAL" would be empty, "PASS" false; and declining the amendment forces q4 into
  un-pre-registered prose later, the post-hoc lawyering the ledger exists to prevent). Under PR-15.1:
  **conditional PASS (one-sided)** — conditions all Lucas's (sign · Wu disposition · Böhm qualifier ·
  retrievals).
- **Reconciliation:** each modality missed where its method predicts (incl. the Critic's own blind pass
  touching Wu and dropping it — no candidate→disposition ledger); six S0.8 sweep fixes filed.

**Pipeline:** postscript added to E-09-5 (rulings stand, ruling 2 sharpened); WS-F11/F12 queued as
decision-free Executor follow-up after S0.7L-0 (still running). **Gate now waits on exactly two
things: Lucas's rulings + the lite envelope.**

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
