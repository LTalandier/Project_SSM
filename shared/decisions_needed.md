# Decisions Needed

The **Executor** posts design questions here when something is unclear or requires a methodology
decision it wasn't given. The **Supervisor** answers (or escalates to Lucas via
`escalate_to_human.md`). Resolved items move to the bottom with the resolution + date.

---

## OPEN

### D-2026-06-09-1 (strategic, pre-S0.2) — Front-load verification debt #1 (white-space prior-art search) from S0.8 to before S0.2, with a go/no-go kill-criterion
**Raised by:** pnn-multilayer Supervisor session, via a cross-project "is this even worth running?"
crosscheck Lucas requested 2026-06-09 — **not** the Project_SSM Executor/Supervisor/Critic. **Blocks:**
proposes a **new pre-S0.2 gate**; does **not** block the S0.1-F* edits already scheduled before
PR-1/PR-2 freeze. **Partially revisits** Critic roadmap-review **F14** (which left debt #1 S0.8-paced) —
a different lens, not a contradiction; see below.

**The decision.** Move verification debt #1 — the white-space prior-art search (the four F15
kill-queries) — off the S0.8 critical-path tail and run it **now, in parallel with S0.7-lite, before the
S0.2 bake-off is authorized.** Add a pre-registration entry (proposed **PR-15**) with an explicit
go/no-go: *if the search surfaces a prior matching F15 query (i) [zeroth-order/perturbative updates of
internal recurrent-photonic params] or (ii) [policy-gradient updates of internal recurrent params], the
scientific-first claim is falsified → escalate to Lucas before authorizing the S0.2–S0.5 spend.*

**Why (the firm argument).**
1. **Two value legs, gated asymmetrically.** The systems-advantage leg (conceded niche-at-best,
   likely-negative) is correctly front-loaded and gated — S0.7-lite (F1) runs before the task choice,
   F16 sets a content floor, the escalation clause fires pre-MPW. Good. But the **scientific-first leg —
   the *primary* contribution (proposal §10: "the scientific first stands without a systems advantage;
   the commercial thesis does not") — has its kill-shot (the white-space claim) scheduled dead last
   (S0.8) with no pre-registered gate.** The leg that carries the whole project is the one whose decisive
   check is deferred.
2. **The deferral is dependency-correct but strategy-wrong.** F14 left #1 S0.8-paced because it is not a
   critical-path *input* to S0.2/S0.3 (unlike debts #2/#3). True. But "not a prerequisite input" ≠ "safe
   to defer." The search is **cheap** (literature, days, no compute, no fab) and **potentially fatal**
   (Critic's own F15: "a single such prior is **fatal**, since it is precisely our Stage-1 claim").
   Cheap + decisive + potentially-fatal belongs *first*, independent of dependency order.
3. **Cross-project precedent (the reason this crosscheck exists).** The sibling project (pnn-multilayer,
   chip track) deferred its single decisive value probe — β-10, "does the chip beat DSP at deployment
   charging every real cost?" — to the end of a ten-rung ladder, for *exactly* this reason: it wasn't a
   prerequisite for the earlier rungs. β-10 returned a definitive NO, and the rungs before it
   characterized a device the kill-shot then falsified. Post-mortem lesson, verbatim: **front-load the
   kill-shot — β-10 should have been β-1.** Debt #1 is this project's β-10. (See
   `pnn-multilayer/shared/project_postmortem.md`, 2026-06-09.)
4. **It can run now.** The exact claim *wording* legitimately depends on S0.1's B1 actuation map (done) +
   PR-2 — but the *existence* search (F15 i–iv) does not. Separate the existence gate (now) from the
   wording (PR-2/S0.8).

**Recommended resolution.**
- (a) Re-pace debt #1 to **run before S0.2**, alongside S0.7-lite, on the dependency graph.
- (b) Register **PR-15** (white-space go/no-go) with the kill-criterion above; the wording refinement
  stays at PR-2/S0.8.
- (c) If it clears → proceed to S0.2 with the novelty de-risked (strictly stronger than discovering a
  prior at S0.8). If it surfaces a fatal prior → escalate; the residual contribution collapses to a
  methods-comparison-only result (heavily discounted without the "first"), and Lucas decides whether that
  alone justifies the bake-off.

**Related strategic flag for Lucas (larger than this reorder; flagged, not folded in).** The project's
*primary* payoff is a scientific-first / priority result — the axis Lucas has said he values least
("paper is a human-readable trace only; cares about truth and chip engineering"). The axis he values —
producibility / chip engineering — is the one §10 disclaims, and S0.7 is predicted negative on the *same*
O-E-O + thermo-optic-holding-power physics that floored the β-10 chip. Most of the *truth*-value Lucas
would actually want (does it train? would it ever pay?) is obtainable from the two cheap front-loaded
probes (this debt #1 + S0.7-lite). Whether the expensive remainder (full bake-off → multi-year niche fab)
is worth a scientific-first he may not intrinsically value is a Lucas-level call.

**Routing.** → **Project_SSM Supervisor**: fold the re-pacing into `stage0_roadmap.md` +
`preregistration.md`, or rebut. → **Critic**: reconcile with F14 (value-at-risk / kill-shot-ordering
lens vs data-dependency lens — both can hold; does the go/no-go belong in the PR ledger?). → **Lucas**:
adjudicate the reorder + the related strategic flag.

**Supervisor adjudication (2026-06-09) → CONCUR; adopt (a)+(b)+(c) with four strengthenings.** Precedent
verified (`pnn-multilayer/shared/project_postmortem.md` exists; lesson verbatim: "the kill-shot question
came last and should have come first"). The argument also stands without it: **cheap + potentially-fatal +
(one-sidedly) decisive ⇒ run first**; dependency order only constrains expensive or input-producing work.
No conflict with F14 — F14 is a *data-dependency* statement (#2/#3 are inputs; #1 isn't), D-09-1 adds a
*value-at-risk scheduling* principle on top; both hold (→ Critic to confirm).

1. **State the kill-criterion in rule form, not query-indexed form.** As drafted ("matching (i) or (ii)")
   it under-covers: F15 query (iii) — HIL adaptation of delay-reservoir *feedback/internal* params — is
   fatal *iff the update rule is gradient-based/-estimating*. PR-15 rule: a prior is **FATAL iff all three
   hold** — **(q1)** params *internal to the recurrence* (feedback/coupling/pole-defining; readout-only or
   input-mask-only does **not** count), **(q2)** updated **on the physical device in the loop** (not
   simulate-train-then-deploy), **(q3)** by a **gradient-based or gradient-estimating** rule
   (backprop/adjoint/PAT-hybrid; SPSA/FD zeroth-order; REINFORCE/policy-gradient). F15 (i)–(iv) are the
   *search lanes*; the rule decides. (iv)-type priors (evolutionary/Boolean) are **non-fatal but must be
   cited** — they make the "gradient-based/-estimating" qualifier load-bearing. **Ambiguous cases**
   (partially-internal params; hybrid digital recurrence; unclear what was physically updated) →
   **escalate to Lucas with primary sources attached**, never adjudicated inside the pipeline.
2. **One-sided PASS semantics.** A found prior is decisive; a clean search is *not* a certification
   (bounded by search quality). PR-15 PASS = *no falsifying prior under the registered lanes + an
   independent adversarial Critic pass*; the claim stays **provisional until the S0.8 dated final sweep**
   (which stays — D-09-1's existence-now / wording-later split is right).
3. **Two-modality search (the B2 lesson).** **Executor** runs the systematic sweep (S0.L lane; it ran the
   B2 pull) → dated memo, every candidate prior **verified in the primary source** — no aggregator-snippet
   citations (the F5 failure mode). **Critic** runs an *independent adversarial pass* (its brief: kill the
   claim), plus reconciles F14 and reviews the PR-15 criterion **before the search runs**. Lucas
   adjudicates anything found/ambiguous.
4. **Fold into ONE pre-S0.2 continuation gate.** v3 already runs S0.7-lite before the S0.2 task choice;
   add PR-15 alongside → the pre-S0.2 touchpoint becomes a single **continuation review**:
   {S0.1+S0.1.1 ✅} + PR-15 verdict + S0.7-lite envelope + the strategic-flag value call — one Lucas
   decision with both kill-shots in hand, instead of three scattered asks.

**On the strategic flag — one sharpening that raises its stakes.** The "first" is **not a Stage-0
deliverable at all**: it can only be *collected* on hardware (Stage 1+). Stage 0's standalone output is a
methods/feasibility paper (bake-off + mapping + envelope). So PR-15 protects the value of a payoff that
only materializes **if Lucas later commits to fab**; if he already knows he would not fab a
niche-at-best chip, the bake-off must justify itself as **methods science alone** — and that bar should be
set at the new gate, not discovered at S0.8. Decision tree: **PR-15 fatal** → headline gone at every stage
→ near-certain stop (residual = methods comparison; Lucas decides). **PR-15 clear + S0.7-lite
hard-negative** → a collectible first with no advantage story (§10 says it stands scientifically; Lucas's
stated values discount it) → his call, at the gate. **Both clear-ish** → continue, novelty de-risked.
Under *every* branch the two probes are worth running now: days, no compute spend, and they convert the
continuation call from speculative to informed.

**Order (pre-registration discipline).** Nothing folded into roadmap/ledger yet: PR-15 *governs* the
search, so the criterion must be registered + Lucas-blessed **before** the search runs (else hindsight
bias in what counts as a match). On bless: (1) register **PR-15** (rule + lanes + databases/venues +
mid-2026 date-snapshot + disposition rule); (2) roadmap re-pace (#1 → pre-S0.2 ∥ S0.7-lite; dependency
graph + S0.L edits; the joint continuation gate); (3) Executor search task + Critic
adversarial/F14-reconciliation spec; (4) the gate itself. **→ Escalated as E-2026-06-09-2.**

### D-2026-06-08-2 (flag, S0.1) — Diagonal-complex-SSM vs real-LinOSS-conjugate-pair architecture
**Raised by:** Executor (S0.1, `docs/s0_1/mapping_notes.md` §4b). **Blocks:** nothing now; **feeds PR-2**
(S0.2 bake-off architecture). One optical ring = one **complex** pole (the field carries a carrier), so
the ring bank maps most cleanly onto a **diagonal complex-pole SSM** (S4D/DSS form, proposal §1.1) — which
the S0.1 code realizes directly. A real-valued LinOSS/D-LinOSS oscillator block is a real 2nd-order system
= a **conjugate pole pair**. Both are supported by the model; the Supervisor should **pin which layer the
bake-off simulates** at PR-2: (a) complex-diagonal SSM (one ring ↔ one complex pole, cleanest for optics)
vs (b) real-LinOSS with rings paired into conjugate blocks. Not a defect — a deliberate framing choice.

**Supervisor recommendation (2026-06-09) → (a) complex-diagonal SSM, framed as the *diagonalized*
LinOSS/D-LinOSS.** Rationale: (1) **hardware-minimal** — each physical ring is one trainable complex pole;
(b) doubles the ring count for the same state dim (reticle-bounded, §9 risk 5); (2) the complex-diagonal
form **is** the standard diagonalized realization of LinOSS/D-LinOSS — damping = pole real part = κ_tot,
which is exactly the proposal's "loss = damping, a free knob" story — so this does **not** abandon LinOSS,
it is its photonic-native realization; (3) the white-space claim is unaffected (trains the B1 set
{κ_tot,j, δ_j, μ_jk}). **Caveat (→ debt #2):** confirm the LinOSS↔complex-diagonal equivalence + that the
oscillatory-SSM benchmark results transfer to the diagonal realization, and handle real-valued I/O at the
**readout** (not by constraining the recurrence). **→ Escalated to Lucas (PR-2 framing) + routed to the
Critic (S0.1-results review) for an independent read before PR-2 freezes.**

**Critic adjudication (2026-06-09, `critic_review_s0-1-results.md` S0.1-F2):** AGREE with simulating the
complex-diagonal layer; **REJECT the "it *is* diagonalized LinOSS" framing** as conflating two classes.
Honest statement: *the ring bank natively realizes a **diagonal complex-pole SSM (S4D/DSS class)**;
uncoupled + with real I/O it reduces **exactly** to LinOSS; trainable inter-ring μ is a **mild
generalization beyond** standard diagonal-A LinOSS.* Conditions: (1) own the diagonal class + soften the
"oscillatory LinOSS" branding; (2) benchmark transfer is open **debt #2** — published LinOSS validates
only the μ=0 diagonal reduction; the coupled generalization is validated by the BPTT-on-substrate ceiling;
(3) **pin the readout** (coherent-quadrature = real-linear → LinOSS-equivalent vs intensity = nonlinear) at
PR-2; (4) white-space claim unaffected. **Supervisor: adopt in full** — the correction is right, improves
the framing, and pre-empts a hostile-reviewer attack ("you said LinOSS but trained a coupled S4D"). → Lucas
to bless the corrected framing (PR-2).

### D-2026-06-08-3 (flag, S0.1/F19) — Backscatter mode-splitting bites *within* the registered Q range
**Raised by:** Executor (S0.1 B2, `docs/s0_1/B2_backscatter_bound.md`). **Blocks:** nothing now; **feeds
S0.3 (F19) + PR-4.** The literature pull found splitting is **process-roughness-limited, NOT cleanly
Q-gated** — contradicting the roadmap's "negligible at foundry Q≈2×10⁶" assumption. Clean damascene-class
process: single-pole holds at foundry Qi, crosses by ~4×10⁶, broken at 3×10⁷. **Rough subtractive process:
splits 21–75 % of modes already at foundry Qi=2×10⁶.** Executor **recommends** S0.3 carry an *optional*
CW/CCW splitting knob **gated by a process-roughness flag** (default OFF only for the *clean* foundry
corner). The Supervisor/Lucas should decide whether PR-4 makes the clean-process assumption explicit, or
S0.3 must model the doublet at the foundry corner too. (Executor produced the physics + recommendation;
the framing/decision is Supervisor/S0.L per role boundary.)

**Supervisor recommendation (2026-06-09) → accept the optional roughness-gated splitting knob; promote
roughness/splitting to a PR-4 sub-parameter.** (1) Carry the optional CW/CCW splitting knob in S0.3 — the
S0.1 bound *triggers* the roadmap's conditional ("knob iff S0.1 says it bites"); it bites for rough
processes. (2) The "realistic SiN noise" cell (PR-4) gains a **roughness/splitting dimension** → the cell
is now ~(Q, loss, κ_ext, roughness/splitting, NF, ASE). (3) **Load-bearing platform tension for PR-4 +
S0.7-lite:** the lowest-loss / highest-Q platforms (best memory) are the *most* splitting-prone, while
foundry CORNERSTONE's low Q (Qi≈2.3×10⁵) is splitting-safe but memory-poor (~33 round trips) —
best-memory and clean-single-pole pull in opposite directions. (4) **Act conservatively now** (carry the
knob) on the *qualitative* finding, which is robust; but **B2's quantitative crossover is provisional**
(search-aggregated figures — the Executor's verify-before-citing flag) → **S0.L confirms primary sources
before any proposal/paper claim.** **→ Escalated to Lucas + routed to the Critic** (B2 literature rigor is
exactly what the Critic should stress-test).

**Critic adjudication (2026-06-09, `critic_review_s0-1-results.md` §5/S0.1-F5):** AGREE with the knob +
PR-4 sub-parameter, with **three strengthenings**: (1) evaluate splitting at the **operating κ_ext**, not
the undercoupled worst case (overcoupling widens the linewidth and *suppresses* visible splitting → may
materially relax the constraint; couples to the κ_ext policy → **resolve with D-08-1 together at PR-4**);
(2) **default the knob ON except the clean-damascene corner**, and PR-4 states the clean-process
assumption explicitly if the single-pole substrate relies on it; (3) verify B2 primary sources (F5, S0.L)
+ fix the F4 row arithmetic before the crossover numbers enter the proposal. The Critic independently
re-derived the crossover table and confirmed the **qualitative finding is robust** under both criterion
conventions. **Supervisor: adopt in full.** → Lucas to bless (PR-4).

### D-2026-06-08-1 (parked) — SiN operating $Q$ for the substrate (pre-registration)
**Raised by:** Supervisor (from the S0.0a recon). **Blocks:** nothing yet; **due at S0.2/S0.3.**
The salvaged platform registry ships SiN `Qi=2×10⁶` (LIGENTEC AN800, foundry-grade), but the proposal
cites `Q>10⁷` (class-leading, e.g. damascene SiN). Which do we pre-register as the operating point for
the S0.3 substrate (and the memory-length / gradient-survival story)? S0.0 adds both as registry entries
but does **not** choose. **To decide at S0.2/S0.3 pre-registration**, with the Critic's roadmap review
weighing in (checklist item 6). Likely: register a *range* (conservative foundry → aspirational) and
report sensitivity, rather than a single value.
**Update (2026-06-09):** now **coupled to D-08-3** — PR-4's realistic cell gains a roughness/splitting
dimension, and the platform tension (high-Q best-memory vs splitting-prone; CORNERSTONE low-Q
splitting-safe but memory-poor) is part of this same operating-point choice. Resolve them together at PR-4.

---

## RESOLVED

### D-2026-06-05-1 — Salvage `pnn-multilayer` code vs. clean start → **(a) SALVAGE**
**Resolved 2026-06-08 by Lucas.** Selective salvage per the `shared/tooling_recon.md` §4 manifest (7
assets: SPSA+accounting, gain/ASE functions, dynamic rate-equation SOA, SiN registry, static Lorentzians
+drift, ridge readout, sweep/JSONL scaffold). Copy + adapt with provenance headers (`pnn-multilayer @
e2eec80`), decouple contact points, re-run tests. SSM core written fresh either way. Folded into S0.0
(now ACTIVE). `pnn-multilayer` stays read-only.

### D-2026-06-05-2 — `git init` Project_SSM now? → **YES**
**Resolved 2026-06-08 by Lucas.** Repo initialized under git as part of S0.0; provenance of salvaged
code tracked from the first commit.
