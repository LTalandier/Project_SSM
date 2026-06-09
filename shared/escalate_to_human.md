# Escalate to Human (Lucas)

Either agent posts here when a decision is **above the pipeline's pay grade** — anything that changes
what the paper will claim, commits money/compute, or where Supervisor and Critic disagree and can't
resolve it. Lucas is the human PI and final authority. Newest at top.

Escalate (don't decide autonomously):
- Scope changes beyond the approved proposal / roadmap
- Methodology changes (metrics, training setup, evaluation) that affect conclusions
- Any cloud-compute spend
- Supervisor ↔ Critic deadlock
- Pre-registered margins/gates, before the run that tests them
- Invoking a baseline/fallback (proposal §5.3: offline-train-deploy; reservoir-readout)
- Promoting an exact method (recurrent adjoint or RHEL) toward a hardware slot (§5.2 guardrail)
- The S0.7 systems-advantage-envelope verdict, if even the optimistic envelope fails to clear digital (§10)

---

## OPEN FOR LUCAS

### 🚦 E-2026-06-10-3 — THE PRE-S0.2 CONTINUATION GATE: one go/no-go on the bake-off (S0.2–S0.5)
**Filed:** 2026-06-10 (Supervisor). Both gate inputs are now in hand. One decision: **authorize the
four-method training bake-off (S0.2–S0.5), or stop/reframe.**

**Input 1 — "is the claim still ours?" (PR-15 kill-search): provisional one-sided PASS.**
80+ papers / 74 candidates across two independent searches; **0 fatal** under the rule you signed
(PR-15.1). Wu is contained by the W1 claim wording you adopted; Zhao you resolved non-fatal from
the figures; the three unread full-texts (NTT, Fisher, Shi) all carry documented non-fatal leans
and are re-paced to the claim-wording freeze — not this gate. Caveat by design: a clean search
proves absence of *found* priors, not absence of priors; the dated final sweep at S0.8 stands.

**Input 2 — "is it worth building?" (S0.7-lite envelope on the numbers you froze): conditional
POSITIVE — Critic-audited: APPROVE-WITH-EDITS, "conditional positive" SURVIVES**
(`critic_review_s07lite-envelope.md`: clean-room recompute reproduces all 36 photonic cells, all
144 clearance verdicts and all crossovers; the §10 non-firing is robust to every perturbation
tested). The §10 escalation clause does **not** fire: 16 optimistic-corner cells clear at least
one named digital baseline (up to **14.7×** vs the Microsoft Brainwave FPGA serving anchor);
sub-µs latency is unreachable for that serving class (<4 ms author-stated; honest matched-N
contrast is **≥10²**, not the ~10⁵ this packet first stated — corrected per EV-F4). The niche:
**GS/s streaming signal-processing, N=32–128 states, sub-µs latency**. Conditions, as corrected
by the audit:
(1) the **deployable**-corner advantage requires suspended (class-B, ~1 mW/π) heaters — not
offered in the named CORNERSTONE flow — under any holding convention; the **hero**-conversion
corner clears the FPGA anchor with standard foundry heaters above ~1.3–1.5 GS/s under
expected-value (P_π/2) holding. [EV-F1: this packet's earlier flat "only with class-B" — and a
Supervisor robustness assurance behind it — were wrong; the corrected statement *softens* the
Stage-1 fab condition in the program's favor.]
(2) Rate floor ≈0.5 GS/s deployable / ≈0.13 GS/s hero, **±2× soft** pending rate-matched converter
sourcing (EV-F6); sub-sample ring memory independently excludes 0.1 GS/s at the foundry corner.
(3) The embedded-GPU *peak* FoM is never beaten — the comparison survives only via the registered
peak≠sustained caveat (the single most case-threatening S0.7-full retrieval).
(4) **New (EV-F3/F5):** the N=128 margins assume the **class-leading-Q platform corner** — exactly
the splitting-prone one (goes to PR-4, jointly with D-08-1) — and a **single-quadrature/intensity
readout** (goes to the PR-2 readout pin; I/Q detection kills the boundary DSP cell and pushes the
deployable corner to N=128). Labelled assumption-driven, NOT outreach-load-bearing.

**GO authorizes:** S0.2 (task + architecture pre-registration, PR-1/PR-2 incl. the W1 wording +
readout pin), S0.3 (shared dissipative substrate, PR-4: operating Q + roughness knob, D-08-1),
S0.4 (the four estimators incl. the RHEL echo sub-model), S0.5 (the bake-off). All local
simulation — no fab, no outreach, no cloud spend without a separate escalation. Scale reminder:
the "first" itself is only collectible at Stage 1+ (hardware); Stage 0 alone yields a methods
paper.

**NO-GO means:** stop at an envelope/methods-survey publication, or reframe the program now,
before bake-off effort is sunk.

**Supervisor recommendation: GO.** Both kill-shots cleared at the level Stage 0 can test them; the
downside of GO is local simulation time only; the bake-off's methods value survives even if the
§10 niche narrows further; and the strategic window is ~one publication cycle (the Wu group is
active in exactly this space). Conditions attached: S0.2's task sized to the niche
(equalization-class GS/s streaming, N≈32–128 — envelope memo §6); the audit's PR-2/PR-4 carry-ins
(readout pin; N=128⇄Q-corner⇄splitting; holding convention) now logged in the ledger Notes; the
residual EV-F1/F2 wording corrections + EV-F3/F4/F5 memo sentences ride the next Executor task.

**→ Your move: "GO" / "NO-GO" / amendments.** (The Critic audit you launched has landed and is
folded in above — nothing further is pending on this decision.)

### 📥 E-2026-06-10-2 — Retrievals + the continuation gate (coming next)
- **✅ Retrieval #1 RESOLVED (2026-06-10):** **Zhao LPR 2025 → NON-FATAL.** Lucas obtained figs. 1–2
  (archived in `docs/s0_L/primaries/`); feedforward MLP with bidirectional optical BP — rings are
  static weight elements, fails q1. Becomes a prominent must-cite; full-text check rides S0.8.
  **The main gate contingency is cleared.**
- **Remaining (claim-freeze-paced, NOT gate-blocking):** NTT Compute-in-Wire (ADI 2025,
  doi 10.34133/adi.0121), Fisher 1987 (Appl. Opt. 26:5039), Shi LPR 2025 — all carry documented
  non-fatal leans; needed before the PR-2/S0.8 wording freeze.
- **Wu outreach:** held per your ruling ("don't send yet — maybe later"); draft + addresses in the
  session log when wanted. W1 is the adopted default claim meanwhile.
- **Next decision to reach you:** → **landed as E-2026-06-10-3 (above)** — S0.7L-1 is complete.

---

## ✅ RESOLVED 2026-06-10 — the PR-15 / PR-10 ruling cluster (Lucas: "1. ok · 2. ok · 3. don't send yet · 4. [title given]")
**PR-10 🔒 FROZEN** (envelope dispatched as S0.7L-1) · **PR-15.1 SIGNED** (q4 + q1 riders + q3 positive
definition; servo class → lineage, **Böhm → boundary-cite**) · **Wu → no outreach yet; W1 = adopted
default claim** (W0 reclaimable on later evidence) · gate state: **provisional one-sided PASS under
PR-15.1, contingent on the retrievals above**. Full record: `preregistration.md` (PR-15.1 block) +
`decisions_needed.md` D-2026-06-09-2. The five entries below are kept as filed (superseded):

### 🧊 E-2026-06-10-1 (Supervisor) — **Freeze PR-10** (S0.7-lite assumptions) — the last pipeline-side gate input
S0.7L-0 done (results_log; Supervisor ACCEPT — it also caught 4 bad legacy anchors, now excluded). The
**PROPOSED PR-10 block** is in `preregistration.md`: OPT/CONS corners per category (E/O 0.135 → 10–20
pJ/bit; O/E 0.17 → 1.4; ADC 32 → 469 pJ/sample at ENOB-at-speed; DAC 5–9 → 308), two heater classes
with a consistency rule (no mixing suspended-heater power with standard-heater speed), named F16
baselines (Brainwave 287 GFLOPS/W · coherent-DSP ASIC 25–170 pJ/bit · Jetson Orin), scale grid
N∈{8,32,128} @ 0.1–2 GS/s, and registered lite-exclusions (laser, locking, control compute — listed as
unbudgeted, deferred to S0.7-full). **Say "freeze PR-10" (or amend rows) → S0.7L-1 runs the envelope**
→ the continuation gate then has everything except your PR-15 rulings.

### 🏁 E-2026-06-09-6 (Critic) — PR-15 Part 2 filed: memo audit CLEAN; merged verdict table; **gate = conditional PASS (one-sided) under PR-15.1, degenerate under the frozen letter**
**Filed by the Critic** (Part 2 of `critic_review_whitespace-pr15.md`, §6–§9 + Appendix B). In brief:
1. **The Executor memo passes the audit.** Every overlap-set verdict matches Critic-verified primaries;
   no verdict rests on an unreached source; the Bueno/Brunner boundary memo survives a hostile re-read;
   the trail is reproducible (I re-ran two load-bearing legs). Two LOW bookkeeping fixes (WS-F11/F12).
2. **Wu (M1) audit:** I re-read the full archived PDF + hostile-grepped the SI with a disjoint query
   set — "U is never enumerated" **confirmed**. New evidence (WS-F9): the text affirmatively supports
   only the *natural/fatal* reading (no fixed-W statement exists; one FPGA-DAC drives all phase
   shifters; OHMM-programmed vs ORNN-trained contrast). Wu's q4 is YES — **the amendment is no
   escape**. Recommend: author query = urgent; **W1 hedge = default plan, not contingency** (I
   verified W1 true under both Wu readings — consistent with the Supervisor's freeze-low/reclaim-high
   draft).
3. **Milanizadeh upgraded AV→CV** (live fetch where both prior attempts 403'd): literal "gradient
   descent" on coupled-ring poles, on chip — the cleanest proof the frozen letter is defective.
   **Zhao paywall reproduced** (Wiley 402) — retrieval ask #1 is genuine.
4. **Merged table** (§7): escalation set M1–M9 + merged must-cite list + 9-item S0.8 watchlist.
   **Reconciliation** (§8): each modality missed where its method predicts — including that my own
   blind pass *made contact with Wu and dropped it* (no candidate→disposition ledger); six concrete
   S0.8 sweep fixes filed.
5. **Verdict (§9):** under the **frozen letter — degenerate** (mechanically satisfied by filter
   servos; "FATAL" would be true-but-empty, "PASS" would be false — the letter is worth nothing
   without amendment). Under **PR-15.1 — conditional PASS (one-sided)**, conditions: sign PR-15.1 ·
   disposition Wu (per 2.) · adopt the Böhm physicality qualifier · retrieve Zhao/NTT/Fisher before
   any claim freeze. The continuation gate then closes on your rulings + the S0.7-lite envelope, per
   E-09-5.

### 🎯 E-2026-06-09-5 (Supervisor) — PR-15 synthesis: **four rulings needed**; recommendations attached; pipeline re-tasked around your ruling
**Read this first; E-09-4 (Executor) + E-09-3 (Critic) below are the underlying modality reports.**

> **Supervisor postscript (2026-06-10, after Critic Part 2 / E-09-6 above): the four rulings stand,
> with ruling 2 sharpened.** The Part-2 audit is CLEAN (Supervisor concurs — verdict structure is
> right, and its strongest new argument for ruling 1 is that *declining* PR-15.1 forces the q4 content
> into un-pre-registered prose later, exactly the post-hoc lawyering the ledger exists to prevent;
> the letter-verdict is formally degenerate, mechanically satisfied by Milanizadeh's literal on-chip
> "gradient descent" filter tuning). **Delta on ruling 2 (Wu):** WS-F9's hostile re-read found the
> textual evidence *leans toward the fatal reading* (no fixed-W sentence exists; one DAC drives all
> phase shifters; programmed-OHMM vs trained-ORNN contrast) — so **W1 is now the default plan, not the
> contingency** (three-role consensus: Critic verified W1 true under both Wu readings — no resonator
> pole or inter-resonator coupling is in Wu's trainable set on any reading), and the author/code query
> is decisive-and-urgent. Rulings 1/3/4 unchanged. **Gate inputs remaining: your rulings + the
> S0.7-lite envelope** (Executor running S0.7L-0). WS-F11/F12 (LOW bookkeeping: memo under-counts its
> own coverage ≈74 rows/80+ papers; full-text residuals) → queued as a decision-free Executor follow-up
> after S0.7L-0.

**State.** Modality-1 sweep + blind adversarial pass both complete: **no confirmed FATAL**. The
two-modality design worked — each pass found what the other missed (Executor: Wu, Milanizadeh, Zhao ↔
Critic: Fisher 1987 + the criterion defect itself). The gate stays **OPEN**; nothing below was
adjudicated in-pipeline, per the frozen disposition.

**Your four rulings — Supervisor recommendation attached to each; adjudication is yours:**
1. **PR-15.1 amendment** (q4 task-objective + weight-tied-recurrence rider + q3 taxonomy — Critic
   WS-F1/F3/F5). **RECOMMEND: SIGN.** All three roles converged independently (the Critic derived it
   blind; the Executor hit the same wall as its A3 boundary class; and it matches what the proposal
   always meant — a *trained* SSM is task-training). Consequences: servo + laser-regime classes become
   citable lineage; the claim sentence gains "**on a computational task**"; logged as a dated amendment
   with v1 kept (supersession discipline); Critic Part 2 re-classifies the merged table under it.
2. **A1 — Wu et al., eLight 5:7 (2025)** (potentially-fatal; q1 unresolved — trained voltage set U never
   enumerated). **RECOMMEND: paths (a)+(b) in parallel.** (a) You send the author/code query now (their
   data-availability statement invites it; this needs your name, not the pipeline's). (b) I draft
   re-scoped wording variants at PR-2 regardless — the natural hedge **W1**: *first **continuous-time
   dissipative-resonator** recurrence (pole positions + inter-resonator couplings) trained in situ by
   gradient-based/-estimating methods on a computational task* — true under **both** Wu readings (their
   routing MRRs are calibrate-once-static; the trained U is relay/mesh voltages, not resonator
   poles/couplings), with Wu cited loudly as the nearest neighbor. The gate need not block on their
   reply: it can close on "PASS-under-amendment + Wu carried as potentially-pre-empting + W1 hedge" if
   you judge that sufficient — exactly the program-level call the gate exists for.
   **→ Drafted: `docs/s0_L/whitespace_claim_wording.md`** (W0/W1/W2 variants, what kills/survives each,
   and the recommendation: **freeze low (W1), reclaim high (W0)** — retreating after outreach costs
   credibility; reclaiming costs a wording edit).
3. **A2 — Böhm 2022** (hybrid-digital recurrence; found by both modalities). **RECOMMEND: adopt the
   Critic's parameter-physicality qualifier** (trained params = physical/analog degrees of freedom of a
   photonic recurrence; recurrent state carried photonically) **+ cite Böhm by name** as the hybrid
   boundary case. Under it Böhm is non-fatal (its J_ij live as digital numbers in the in-loop FPGA).
   Note: Wu does **not** die by this qualifier (its loop is analog O/E/O) — A1 stands or falls on
   q1/W1, independently of this ruling.
4. **A4 — retrievals (human-access asks):** **Zhao LPR 2025 is the priority** (Wiley-paywalled; title
   claims "in-situ trained microring-based neural networks" with optical backprop physically updating
   MRR parameters — must be read before any claim freezes; most MRR-NN work is feedforward weight
   banks, but *verify, don't assume*). Also: NTT Compute-in-Wire ADI 2025, Fisher 1987, Shi LPR 2025.
   Paths: library access / author email / ResearchGate request — these need a human identity.

**Strategic note (Executor's, Supervisor-concurred):** the adjacent capability lines are converging on
this result from several directions; if the claim survives adjudication, the window looks like **order
one publication cycle**. That feeds your continuation calculus both ways — the first is worth less if
it can't be defended long, and worth moving on fast if you want it.

**Pipeline (Supervisor-actioned, decision-free):** S0.L-1 → **DONE** (accepted — protocol followed
exactly: stopped, escalated, nothing adjudicated in-pipeline). Critic **Part 2 green-lit** (audit +
merged verdict table; re-classification under PR-15.1 once you sign). Executor re-tasked to
**S0.7L-0** (source the PR-10 assumption table with primaries → I draft PR-10 → you freeze → the lite
envelope runs) so the gate's *other* input advances while you rule. **The gate closes on:** your
rulings + Critic Part 2 + the lite envelope.

### ⚠ E-2026-06-09-4 (Executor) — PR-15 systematic sweep done: 0 FATAL confirmed, **1 potentially-FATAL AMBIGUOUS (Wu eLight 2025)** + boundary class + retrievals — adjudication needed
**Filed 2026-06-09 by the Executor** (modality 1 — systematic sweep, written **before** reading the
Critic's blind-pass entry below; cross-references added after). Memo:
`docs/s0_L/debt1_whitespace_search.md` (~60 candidates, all five frozen lanes, every non-clear
verdict primary-quoted; reproducible trail). Results entry in `results_log.md`. Verdicts against
the **unamended frozen rule**, ambiguity escalated not resolved, per PR-15.

1. **A1 — Wu et al., "Monolithically integrated asynchronous optical recurrent accelerator,"
   eLight 5:7 (2025). Potentially FATAL — the top adjudication item. Not in the Critic's blind
   list (the key cross-modality asymmetry).** First monolithic optical RNN chip; recurrence
   **physically closed on chip** (PD-driven wavelength relay, no ADC/DAC in the loop; "W is the
   feedback weight matrix for the hidden vector"); loss "**minimized in-situ** using a stochastic
   parallel gradient descent algorithm", two-sided SPGD + Adam on "the current voltages U ± δ" —
   **q2 and q3 hold verbatim** (Executor-verified in the publisher PDF). **Open question = q1: U is
   never enumerated** — main text + complete supplementary swept (S1–S11; S9 = iteration curves
   only; routing MRRs are calibrate-once-static): nothing states whether the recurrent W-mesh
   heaters are trained or fixed. Natural reading (no stated restriction) → q1∧q2∧q3 → **falsifies
   the existence claim as frozen**; restricted reservoir-style reading (only W_in/W_out) also
   consistent (their SPGD antecedent, ref. 49, is feedforward). **Primary attached:**
   `docs/s0_L/primaries/wu2025_elight5-7_ornn.pdf` + extracted supplementary. Resolution paths
   (your call): (a) author/code query (paper: data "available from the corresponding author upon
   reasonable request"); (b) treat as fatal-pending-clarification and let PR-2 re-scope the wording
   (e.g. continuous-time dissipative-resonator / pole-defining recurrence); (c) carry as loudest
   must-cite under the restricted reading. Even on the fatal reading: recurrence is analog O/E/O
   (optoelectronic; *not* the hybrid-digital escape).
2. **A3 — calibration/self-optimization boundary class = the Critic's WS-F1, found independently
   by both modalities.** Strongest member: **Milanizadeh ECIO 2020** — literal "gradient descent"
   auto-tuning of a 4th-order coupled-ring filter on chip: **q1∧q2∧q3 hold mechanically**; only
   the reading of "training" excludes it. Also Jayatilleka 2015 (perturb-and-observe sign rule on
   ring detunings, Executor-verified), Mak 2015 (direct search), Pu 2019 / Yan 2021 (intracavity
   EPC). My memo escalates the boundary; the Critic proposes the **q4 amendment** — same issue,
   one ruling needed from you (rule is frozen; neither pipeline role may amend it).
3. **A2 — Böhm et al., Nat. Commun. 13:5847 (2022)** — found independently by **both** modalities,
   same diagnosis: gradient-in-the-loop training of couplings/weights held in the FPGA feedback
   path of an optoelectronic Ising machine = the PR-15-pre-listed "hybrid digital recurrence"
   ambiguity. Needs your reading of "parameters of a *physical photonic* system".
4. **A4 — unreachable primaries (retrieval asks):** top: **Zhao et al., Laser Photonics Rev. 2025**
   (10.1002/lpor.202501576, "In-situ trained microring-based neural networks…", optical backprop
   physically updating MRR parameters; Wiley-paywalled, no arXiv mirror — must be read before the
   claim freezes). Also Shi LPR 2025; **Nakajima Compute-in-Wire ADI 2025** (= also on the
   Critic's list; abstract says digital-twin-trained → likely fails q2); NUDT OL 35:950 (2010);
   4 historical 1985–1991 texts (all lean non-fatal via reachable companions; memo §4.1).
   **Reconciliation note for the Critic's Part-2 audit:** the Critic's blind pass surfaced
   **Fisher 1987** (Appl. Opt. 26:5039, Widrow-Hoff on LCLV associative hardware, loop topology
   unresolved) — **my sweep missed it**; conversely my A1/A3a/A4a are not in the blind list.
   Two-modality protocol working as designed.

**Strategic context (not verdicts):** the adjacent capabilities are converging — Skalli 2025
(SPSA/PEPG hardware-in-the-loop, one parameter-set from q1), NIST/Queen's MGD 2025 (one
architecture from a trained Tait-style recurrent network), FICONN 2024's outlook naming
recirculating-mesh in-situ training as future work, Pérez-López (hardware PSO on ring-bearing
meshes + gradient synthesis in simulation), Yorke arXiv 2026 (simulation paper squarely in the
driven-dissipative in-situ-learning space). If the claim survives adjudication, the window looks
like **order one publication cycle** — relevant to your D-09-1 value-at-risk scheduling logic.

**Process state:** Executor has **stopped** (S0.L-1 deliverables complete; PASS not issued — it is
one-sided *and* pends your A1/A3 ruling). Critic Part-2 audit of my memo can proceed immediately.

### 🔶 E-2026-06-09-3 (Critic) — PR-15 amendment required + 4 AMBIGUOUS priors with primaries
**Filed 2026-06-09 by the Critic** (blind adversarial pass done **before** the Executor memo, which is
still pending — full detail + reproducible trail: `critic_review_whitespace-pr15.md`, Part 1).
**Blind-pass outcome: no prior kills the *intended* claim** (~100 logged queries, 5 lanes). But:
1. **Amendment needed (WS-F1, CRITICAL):** the frozen q1∧q2∧q3 rule has no task-objective condition, so
   it is satisfied *by the letter* by cavity-servo demos (dither-locked rings/FFPs, 1988→2015) and
   laser regime-optimization (explicit finite-difference gradient on intracavity waveplates, Pu 2023;
   deep-RL on hardware, Yan 2021 / Kokhanovskiy 2024). Proposed **q4** (loss over input→output behavior
   on a computational task; setpoint/regime regulation excluded) + a weight-tied recurrence definition
   (WS-F3) + q3 taxonomy enumeration (WS-F5). PR-15 is frozen → **your sign-off**; the Executor is
   classifying against the unamended rule right now, so steer early.
2. **AMBIGUOUS → you, with primaries (frozen disposition):** **Böhm 2022** Nat. Commun. 13:5847
   (BM-likelihood-gradient training of optoelectronic Ising-machine couplings, hardware in loop — the
   one prior that survives q4 and dies only on parameter physicality/hybrid-digital q1;
   https://pmc.ncbi.nlm.nih.gov/articles/PMC9532389/) · **NTT Compute-in-Wire** ADI 2025
   (doi 10.34133/adi.0121 — intra-loop trained modulations, "in-situ on-the-fly training" claimed, full
   text unreached) · **Mak/Bois/Poon 2016** (+kin: ring poles AND inter-ring couplings auto-tuned on
   chip to a target Butterworth shape; algorithm class unverified, reportedly Nelder-Mead) ·
   **Fisher 1987** Appl. Opt. 26:5039 (Widrow-Hoff on LCLV associative hardware; loop topology
   unresolved).
3. **Gate:** final verdict pends the Executor memo audit (Part 2). Provisional: consistent with
   **PASS (one-sided)** under the amended rule.

*(Also coming to you per the standing list: **PR-10** (S0.7-lite assumptions — Supervisor drafting) and
the **pre-S0.2 continuation gate** once the PR-15 verdict + lite envelope are in hand.)*

**Standing per-phase touchpoints** — pre-registered values come to Lucas before
the run that tests them (`preregistration.md`):
- **pre-S0.2:** PR-10 (S0.7-lite assumptions, *before* the lite run) · the **continuation gate**
  (PR-15 verdict + lite envelope + your program-level call — D-09-1) · any FATAL/AMBIGUOUS PR-15 finding
  comes to you immediately with primaries.
- **S0.2:** PR-1 (Gate-i margin) · PR-2 (bake-off task + architecture + parameter partition + readout —
  carries the blessed D-08-2/D-08-3 constraints).
- **S0.3:** PR-4 (the $(\alpha,Q_i)$ pair + $\kappa_\text{ext}$ policy + noise cell incl.
  roughness/splitting — resolves **D-2026-06-08-1**) · compute sizing (escalate if it implies cluster
  spend).
- **S0.4:** PR-6 (fairness contract, **CRITICAL**) · PR-5 (PAT twin-mismatch) · PR-3 (BPTT-ceiling rule).
- **S0.5:** PR-8 / PR-9 (statistics + Gate-ii semantics + promotion criteria).
- Plus the **Critic gates each phase's results** before dependents start (gate model).

---

## RESOLVED

### ✅ E-2026-06-09-2 — D-2026-06-09-1 (front-load white-space kill-search) + strategic flag — **RESOLVED 2026-06-09**
**Lucas: "ok go."** Debt #1 front-loaded pre-S0.2 under **PR-15 (🔒 FROZEN** — rule-form kill-criterion
q1∧q2∧q3, two-modality protocol, one-sided PASS; full detail in `preregistration.md`). Roadmap → v3.1:
S0.2–S0.5 authorization now sits behind the **pre-S0.2 continuation gate** = PR-15 verdict + S0.7-lite
envelope + Lucas's program-level call (the "first" is collectible only at Stage 1+; Stage 0 alone =
methods paper). Executor search task **S0.L-1 ACTIVE**; Critic adversarial spec filed
(`critic_instructions_whitespace-pr15.md`). F14 reconciliation routed to the Critic.

### ✅ E-2026-06-09-1 — Steer the two S0.1 architecture decisions — **RESOLVED 2026-06-09**
**Lucas: "ok go."** **D-08-2** → complex-diagonal **S4D/DSS** layer, LinOSS as conjugate-pair special
case (Critic's corrected framing); readout + F6 pinned at PR-2; benchmark transfer = debt #2. **D-08-3**
→ roughness-gated CW/CCW knob (default ON off the clean-damascene corner) + PR-4 roughness/splitting
sub-parameter at the operating κ_ext, jointly with D-08-1; B2 numbers provisional until F5. Constraints
logged in `preregistration.md` Notes; mapping write-up at `docs/s0_1/mapping_result.md`. Prior progress:
S0.1 gate PASSED (Critic APPROVE-WITH-EDITS); **S0.1.1 closeout DONE** (107/107; F1 transient validation
positive — S0.1 fully closed).

### ✅ E-2026-06-05-1 — Stage-0 setup + roadmap — **RESOLVED 2026-06-08**
**Lucas: "accept all, scope (B) blessed."** Critic review (APPROVE-WITH-EDITS) adopted in full and folded
into `stage0_roadmap.md` **v3**; CLAUDE.md "Codebase plan" F17-fixed; `preregistration.md` adopted (14
entries, UNSET, freeze per-phase); **S0.1 ACTIVE** with the scope-(B) deliverables. Prior progress: D-1
(salvage) + D-2 (`git init`) resolved 2026-06-08; S0.0 DONE (all gates green, 60/60 tests, SPSA anchor RMS
1.1e-7); Critic verdict 1 CRITICAL · 9 HIGH · 11 MEDIUM · 1 LOW, Supervisor concurred in full. Load-bearing
adopted edits: F7 (fairness contract), F10 (Gate-ii decomposition + escalate corner + "exactness" struck),
F2 (score vs BPTT ceiling), F1 (early S0.7-lite), F11 (≥8 seeds + censoring), F13 (foundry-$Q$ gates).
