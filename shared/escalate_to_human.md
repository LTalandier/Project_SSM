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

### ⬜ E-2026-09-14-1 — **"Move on with the research": door 1 answered, door 2 corrected and re-framed, Stage 0c proposed (€0 so far)**

> **Door 1 (athermal):** overlay-athermal SiN rings exist at 0.1–2 pm/K (all UNVERIFIED-direct this
> session; publisher pages 403). At the high-Q substrate that is still 0.06–1 K per linewidth — helps,
> does not remove the hold term. **Door 2 corrected:** PR-20's reachability rule over-credited the
> photonic side (an N-state filter matches ≤ N taps at any rate); the f_s² residue is **withdrawn**
> (PR-20b, ledger §20.7), the S0b.0 kill is *more* robust, and P1 §7.4's hedge stays as is for v1
> (sharper sentence → v2). **Re-framed door 2 = Stage 0c:** the *FSR-matched low-Q* ring lattice
> (registered 100 GHz geometry, coupling 5–20 % instead of r ≤ 3) — thermal hold relaxes 40–150× (to
> ~zero with an athermal overlay), and it is the classical all-pass equalizer regime. **Nearest
> neighbor found (VERIFIED):** SJTU, Nat. Commun. 2024 — 8 silicon MRRs, FSR 99.5 GHz, heater + MZI
> coupler per ring (our actuation set), 40 km CD at 0.3 pJ/bit incl. EDFA vs ≈ 0.6 pJ/bit for the
> DSP's CD share: a static 2× edge, 14.8 dB loss. On SiN the loss and EDFA vanish; class-B heaters put
> it at 1.5–4× (at the 3× bar); class A loses. Nobody has *trained* such a lattice in situ (pending a
> proper sweep). Memo: `docs/s0c/fsr_matched_regime.md`.
> **Your calls:** (1) approve **S0c.0** (€0: mapping memo, white-space sweep, PR-22 envelope with the
> SJTU row as anchor, same 3×/CONS kill rule); (2) S0c.1 simulation (≈ €50–100) only if S0c.0 survives,
> spend returns to you then. **Honest prior:** thin window at the bar; the defensible gain is the W1
> science claim in a regime with a product neighbor and no thermal wall. **Door 3 (capacity, PR-21)**
> is subsumed: in the FSR-matched regime capacity = η_IIR, measured by S0c.1.


### E-2026-09-13-3 — correction and publication disposition resolved in session

Lucas's "okay let's do this" accepted the bounded corrected higher-mismatch rerun,
followed by P1 submission preparation; standalone P5 deferred, negative envelope
retained in P1, hardware/higher-rate work paused, P2 contact separate. S0.13 is
complete (`bda989f` protocol → `174558c` results): exact anchor, no fine mismatch
difference resolved at any tested level, no registered crossover, all resources
removed, approximately €1 gross server-cost estimate plus address charges.

P1 submission files are prepared (`paper/SUBMISSION.md`). No authenticated arXiv
session is available here; author submission/license selection and the linked
submission-day repository release remain external steps, not a new rerun decision.
No arXiv receipt, public-release date, or P2 email is claimed.

The item below is retained as the original proposal; this disposition supersedes
its P5/P1 sequencing and automatic P2-email suggestion.


### ◐ E-2026-09-13-2 — **Stage 0b closed at S0b.0 by arithmetic (kill fired); three calls for you**

**2026-09-13 follow-up:** Lucas authorized the audit repairs and preparation. P5
is drafted locally; the higher-rate residue and hardware work remain paused. P1
now includes the negative result and N8 withdrawals. Submission, repo visibility,
and P2 email remain unperformed; this is preparation, not an outward release.

> **Result:** under PR-20 (frozen before the run), the most favourable inline, non-volatile-actuated,
> passive ring-lattice equalizer reaches **E_digital/E_photonic = 0.64**, consuming **1.56×**
> the digital energy (advantage bar: 3; ratio 0.23 with unsourced optimistic rows removed). The binding term is the
> **common-mode thermal hold** (SiN 14 pm/K; a C-2 linewidth is 8 mK), not actuation; the registered
> 0.1–2 GS/s window cannot amortize even a 10 mW hold. `results/s0b_0/reading.md` has the full reading.
> €0 spent. S0b.1–S0b.3 not run.
> **Found on the way:** P1 §7.1 listed four exclusions; the substrate's own **Er:Si₃N₄ pump** is a fifth
> (0.8–17 mW electrical per ring, derived). Fixed in §7.1 + exclusions ledger §5 + supplementary
> (direction against photonic; no verdict changes). Manuscript + PDF rebuilt.
> **Your calls:** (1) **P5** — publish the negative envelope as a short note ("inline photonic equalizer
> on SiN: the thermal-hold floor vs a per-tap digital baseline")? It is the honest companion to P1 §7
> and costs only writing. (2) **The one residue** — the ratio scales as f_s², so the arithmetic reopens
> at ≳ 10 GS/s *if* hold ≤ 10 mW and the workload needs ≥ 64 taps; that is outside the S0.1-registered
> window and trainability there is unmeasured. Opening it = a PR-20a addendum + an S0.1 re-mapping
> (scope change). My recommendation: **do not**, unless a collaborator brings a concrete ≥ 10 GS/s
> inline workload. (3) **P1 sequencing** now that S0b.0 is done: submit (arXiv first) — repo flip +
> P2 email on the day it moves.


### ✅ E-2026-09-13-1 — **Approve the Stage 0b roadmap (v0.1) — the product question P1 did not ask** — APPROVED 2026-09-13 ("Ok go"): S0b.0 running (€0); P1 sequencing: S0b.0 first, then the submission decision; §8.4/N4 re-worded to "public at submission" + OTS anchor; repo flip + P2 email deferred to the day P1 moves

> **What it is:** `shared/stage0b_roadmap.md`. Simulation + envelope only, no chip, no P1 edits.
> Four phases behind one kill gate: **S0b.0** re-prices the §7 envelope under an *inline* scope
> (no local laser, no E/O in, receiver's O/E shared), with the four former exclusions *charged*,
> a non-volatile actuator class C added, and the DSP baseline priced per tap to the function
> (€0 compute; if no cell clears even at OPT the stage ends there). Then, in parallel:
> **S0b.1** an informative N_eff on a long-span dispersive-ISI task T-E with a registered
> SNR ceiling-band rule so the §19.6c floor degeneracy cannot recur (≈€50–80); **S0b.2**
> PAT/SPSA trained through quantized, write-limited actuators — the open problem that decides
> whether heater hold can go (≈€40–60); **S0b.3** retraining duty cycle vs locking power
> (≈€15–25). **S0b.4** applies the PR-20 verdict rule (CONS corner, ≥3×, N_eff ≥ 16, all
> exclusions charged) → **P5**, positive or negative in the same form.
> **Framing:** trainable optical *LTI filter* with state (S4/LinOSS-class), not "Mamba in glass" —
> per the 2026-09-13 software-SSM check (shipping SSMs are selective; rings are time-invariant).
> **Prior:** negative; the point is to measure the corners P1 left unmeasured *before* any wafer
> spend, per the 2026-09-13 ruling (not worth building as specified; worth researching whether a
> differently specified version is).
> **Your calls:** (1) approve v0.1 + S0b.0 (€0); (2) P1 sequencing — default is *submit P1 first*,
> Stage 0b becomes P5; (3) each later phase's spend comes back separately per the standing rule.
> **Unchanged and still blocking P1:** repo re-public + P2 send.


### ✅ E-2026-07-27-1 — **White-space scope RE-RULED W1-only: the registered Wu eLight page read REFUTED the W0 clearance** (resolved same day under the standing delegation; recorded here so you see it)

> **What happened:** the 4 registered pre-submission page-level reads ran (delegated agents,
> P1 finalization). Three cleared (Zhao SI feedforward-only; arXiv:2507.02297 per-step-distinct
> verbatim; SPIM-EP digital loop). **Wu eLight 5:7 did NOT:** the paper's second chip (ORNN)
> **is trained in situ** by SPGD (two-evaluation perturbation + Adam — SPSA-family,
> gradient-estimating) on Japanese-vowels classification, weight-tied mesh across
> wavelength-encoded steps, *analog* O/E/O state relay. The 2026-07-12 "inference-only"
> disposition described only the paper's other chip. **Consequence: W0's broad form is
> attacked under the natural reading; W1 is untouched** (Wu trains mesh-weight voltages, not
> resonator poles/couplings; its MRRs are static; discrete-time electronic state regeneration).
> **Ruling (same standing delegation as 2026-07-26): retract W0, claim W1 only, cite Wu
> loudly as the nearest neighbor** — the exact retreat the June freeze-low-reclaim-high memo
> pre-planned; cost = one paragraph, pre-publication, zero external exposure. §1.1, abstract,
> §5.5, references, claims table all edited; memo `docs/s0_L/whitespace_page_reads_2026-07-27.md`.
> **Also from the fresh sweep (no new attack):** Zhang et al. eLight 6:6 = new nearest miss
> (in-situ PSO-trained recurrent MRR loop — clears only on the gradient-method qualifier;
> page read registered); watch a possible Zhao×Wu merge (same HUST group). **If you disagree
> with the W1-only ruling, the W0 route needs an author query to Wu et al. on whether the
> recurrent mesh W is in the trained voltage set U — say so and I draft it.**

**Filed + resolved:** 2026-07-27 (Supervisor, by delegation). **Status: ✅ RESOLVED — FYI +
optional override.**

### E-2026-07-27-2 — ✅ **RESOLVED 2026-08-02**: repo public at github.com/LTalandier/Project_SSM (Lucas re-authenticated `gh` in-session and delegated creation+push; full history through `f5bfa5a` pushed 18:14 UTC, unauthenticated visibility verified; §8.4 swapped to past tense). Original entry kept below for the record.

Your point that self-graded pre-registration (single-session, PI = registrant) only counts if
externally anchored is now stated in §8.4, which commits to publishing the repository +
commit history before submission. **The publish action is yours:** either (a) flip
`Project_SSM` public on GitHub (github.com/LTalandier — one click, keeps history = the
timestamp), or (b) an OSF registration snapshot. Recommendation: (a), plus pushing `main`
beforehand (I commit but never push, per standing rule). Until one of these happens the
§8.4 sentence is a forward commitment. **Status: OPEN — Lucas.**

**Re-ping 2026-08-01 (round-3 review sharpened this):** the timestamp only certifies the
freeze-before-run ordering if it **precedes any circulation of the manuscript** — a
timestamp that follows disclosure certifies nothing. It is now doubly load-bearing: §5.5's
entire flip-pattern defense cites commit dates (`241204a`, `ccc4385`, `a8d7ab9`) that a
referee must be able to verify, and §8.4 states publication as a precondition. **Please push
`main` + flip the repo public before this PDF goes to anyone beyond this review loop.**

---

### ✅ E-2026-07-12-1 — **RESOLVED 2026-07-26 by delegation (Lucas: "you can chose the title and W0/W1")** — Supervisor rulings recorded: (1) title = candidate 1 · (2) W0-in-prose + W1-core-sentence

> **RESOLVED 2026-07-26.** Lucas delegated both rulings. Supervisor adopted the standing
> recommendations: **(1) Title = candidate 1** (question form: *"Can a photonic state-space
> model be trained on-chip? A pre-registered four-method bake-off on a realistic
> silicon-nitride ring substrate"*) — recorded as CHOSEN in `paper/outline.md`.
> **(2) White-space scope = W0 claimed in prose with W1 as the precise core sentence**
> (§1.1 edited: the ▢ placeholder replaced by the broad-form claim, the boxed W1 sentence
> kept as its precise instantiation; retreat path if a W0 attack surfaces in review = one
> paragraph edit, W1 core untouched). The 4 registered page-level reads remain the
> pre-submission diligence before the stronger wording ships. Abstract + §1.3 also
> refreshed to the post-S0.9 state of §5.5 in the same edit. P1 now has **no open PI
> gates**; remaining items are non-PI (S-figs, venue formatting, final refresh sweep,
> S0.7 exclusions ledger) + the P2 send (E-2026-07-07-1, physical action).

*(Original filing kept below for the record.)*

**State:** all nine sections drafted (§5.7/5.8 filled today) · figures F1–F7 made
(`paper/figures/`) · abstract filled from landed gates · citation sweep done
(`paper/references.md`, 4 page-level verifications) · white-space refresh done
(`docs/s0_L/whitespace_refresh_2026-07-12.md`) · supplementary skeleton + provenance table
(`paper/supplementary.md`). Remaining non-PI items (S-figs, venue formatting, final refresh
sweep + 4 registered page reads) hang off your two rulings.

**(1) Title** — candidates in `paper/outline.md`; Supervisor recommendation unchanged: **#1**
(question form: *"Can a photonic state-space model be trained on-chip? A pre-registered
four-method bake-off on a realistic silicon-nitride ring substrate"*) — honest about Stage 0
being simulation; "pre-registered" is the differentiator.

**(2) W0-vs-W1** — the refresh strengthens the case for either, and the June freeze-low-
reclaim-high logic still holds, but the facts moved: **Wu eLight resolved = inference-only
(clears W0)** and **Zhao LPR resolved = feedforward weight banks (clears W0)** — the two
exposures that originally forced the W1 hedge are both gone. **Updated Supervisor
recommendation: claim W0 in the intro prose with W1 as the stated precise form** (the
"first" sentence stays W1-shaped — it is exactly what we built — while the surrounding text
now safely says no photonic recurrence of *any* kind has had recurrence-defining parameters
trained on-device by gradient methods). Cost if a W0 attack surfaces in review: retreat to
pure W1 = one paragraph edit; the W1 core claim is untouched. The 4 registered page-level
reads (Wu full text, arXiv:2507.02297, arXiv:2606.13454, Zhao supplement) are the remaining
diligence before the stronger wording ships.

**Also standing:** the P2 author-email send (E-2026-07-07-1 below — your physical action).

**Filed:** 2026-07-12 (Supervisor, single-session mode). **Status: ✅ RESOLVED 2026-07-26 by
delegation — rulings recorded above.**

---

### E-2026-07-07-1 — **Publication plan proposed + one go/no-go: the LinOSS EigenWorms reproducibility note (P2)**

**Context:** your goal directive 2026-07-07 ("make something publishable — and hopefully buildable —
anything with SSM and photonics") → Supervisor wrote **`shared/publication_plan.md`** (PROPOSED):
**P1** = the Stage-0 methods/feasibility paper (primary; ~half writable now, Supervisor starting
`paper/` immediately; sole blocker for its results = the v3 signature, E-2026-07-05-1 below) ·
**P2** = standalone reproducibility note on the G3 finding · **P3** = the Stage-1 hardware letter
(the "first"; buildable arm, gated by the S0.7 envelope as designed) · P4 folded into P1.

**The decision (P2):** we hold an on-record, Critic-adjudicated finding that the published LinOSS
EigenWorms anchor fails a faithful official-code rerun (90.56 % mean, seed σ 9.34 ≈ 2.1× published,
fp32 optimization collapse; port exonerated by the 2.4–2.7e-7 parity dossier). Publishing it
standalone is **outward-facing critique of published work** → your call, not the pipeline's. Options:
**(a) contact the LinOSS authors first with the dossier, note follows within a stated window ← Supervisor
recommendation** · (b) arXiv note directly · (c) fold into P1 related-work only · (d) drop.
*(Venue for P1 is also yours but only binds at submission — not blocking.)*

> **UPDATE 2026-07-07 (after "do everything"):** the Supervisor will **draft** P2 (internal,
> reversible) under the general delegation — but nothing leaves the repo (no arXiv post, no author
> contact) without your explicit (a)/(b) ruling: external release is not covered by "do everything."

> **✅ RESOLUTION (2026-07-07, later — Lucas: "take the decision yourself I trust you go and
> complete the goal").** Decision delegated → **(a) taken**: author contact first, note follows
> within a 14-day window. Drafts written the same day: **`paper/p2_eigenworms_note.md`** (the note;
> every claim = the adjudicated PR-1.1 wording, archived-legs-only, GA-F2/F3 framing) +
> **`paper/p2_author_email.md`** (the contact email + send checklist). **The physical send remains
> Lucas's action** (his name/email/arXiv account): fill the dossier link + addresses, send, log the
> date. The 14-day clock starts at his send, not at this resolution.

**Filed:** 2026-07-07 (Supervisor). **Status: ✅ RESOLVED by delegation — (a); execution gated only
on Lucas physically sending (see checklist in the email draft).**

---

### E-2026-07-05-1 — ✅ **RESOLVED 2026-07-07: S0.4 freeze packet v3 SIGNED (by delegation)** (PR-6/PR-7/PR-5/PR-12)

> **✅ RESOLUTION (2026-07-07).** Lucas: *"don't use the critic for now on do everything."* Read as:
> (1) the **Critic role is suspended** "for now" — no further Critic-session reviews until reinstated;
> (2) packet **closure is delegated** to the Supervisor, who now also absorbs Executor work
> (single-session mode). Executed same day: the focused v3 re-confirm was **Supervisor-performed**
> against the Critic's own staged checklist (verdict APPROVE-WITH-EDITS; 3 stale cross-refs fixed
> pre-signature; independence disclosure recorded at the tail of `critic_review_s0_4_freeze.md` —
> reviews from 2026-07-07 are non-independent and the paper must disclose it). **PR-6 v3 / PR-7 v2 /
> PR-5 v2(structure) / PR-12 v2 are 🔒 SIGNED 2026-07-07 by delegation**; the signature ratifies the
> PR-6 §G-addendum (multi-tap E₀ ride-on on frozen PR-4 §N). **S0.4-0 is now ACTIVE**, executed by
> this session. *(Entry retained below as filed, for the record.)*

> **UPDATE 2026-07-05 (later the same day) — the Critic's max-effort pass landed
> (`critic_review_s0_4_freeze.md` updated in place): verdict AMEND stands; do NOT sign v2.
> Two decisions (D3/D4) gate a v3.** Supervisor assessment: the sharpened findings are **verified** —
> the clause-(b) refutation checked *textually* against frozen PR-4 §G(iii) (it registers only the θ₀
> value E_sym/E_sat ≈ 5e-6–9e-5; **no void ceiling is frozen**, so clause (b) has no threshold), and
> the floor-margin arithmetic cross-checked to order of magnitude (E_sym/E_sat ≲ 1e-2 at the clause-(a)
> floor whether the build-up ratio is the Critic's ×37 or the naive ×91 — conclusion insensitive; the
> factor lands with the S0.4-0 measurement). Several of the review's menu items are **already encoded
> in v2** (multi-point-measured B + the 10⁻³ meaningful-ratio gate + fallback (c); m_κ=0.05/Δr=0.02
> frozen; numeric δ-band; §G-addendum ride-on) — the genuinely new deltas:
> - **D3 (P6-F1 hardened → a capacity finding).** C-2's effective participating dimension ≈ **3 of 32
>   rings**; the reservoir baseline is the **in-data falsifier of debt #1**; the Critic *verified*
>   taps {1,9,17,25} lift 26/32 rings ≥1e-3 — which also previews that the strict *every-ring* gate
>   at K=4 likely triggers fallback (c) (a ~26/32 down-scope, still a massive de-starve vs 3/32).
>   **Supervisor recommends:** keep the v2 §B rule unchanged (the fork stays decided as
>   multi-point-measured + honest fallback); **add** (i) a registered effective-dimension
>   (participation-profile) measurement at S0.4-0 + reporting requirement, (ii) the explicit
>   falsifier-consequence sentence (quantitative margin → PR-9, as already deferred), (iii)
>   {1,9,17,25} as the registered *seed* of the S0.4-0 minimal-tap search, (iv) fallback wording
>   "controllable subset" (taps spread ⇒ not a "front").
> - **D4 (P6-F2 sharpened → clause (b) REFUTED).** Clause (b) can never bind (r_M1 < r_a always;
>   E_sym/E_sat ≈ 3e-3 ≪ O(1) at the floor; and §G(iii) froze no ceiling). **Supervisor recommends:
>   drop clause (b) as a live governor** — r_min = clause (a) + Δr (candidate ≈ 0.16) — and register
>   your required M1-validity check as **performed and PASSED across the whole clamped box** (the
>   check is satisfied; its contingency arm is dead code citing an unregistered ceiling). Anchor-risk
>   (vii) + the S0.4-0 §G-conformance check stay unchanged from v2.
> **✅ D3/D4 RESOLVED 2026-07-05 by delegation (Lucas: "go").** The Supervisor wrote **v3** the same
> day, per the recommendations above verbatim: §C clause-(a)-only r_min (candidate ≈ 0.16; clause (b)
> dropped with the three-part refutation recorded; the M1-validity check registered PERFORMED +
> PASSED) · §B effective-dimension report + falsifier consequence (margin → PR-9) + {1,9,17,25}
> search seed + "controllable subset" wording. PR-7/PR-5/PR-12 untouched. **Remaining sequence:**
> (1) launch the **focused v3 re-confirm** — the v3 addendum at the end of
> `critic_instructions_s0_4_freeze.md` supersedes the v2 one; (2) on its APPROVE, **sign v3**
> (also ratifies the §G-addendum). *Original v2-signature item below (superseded in sequence,
> retained for record).*

**Filed:** 2026-07-05 (Supervisor — housekeeping: this pending action was previously tracked only in
the `task_queue.md` banner; it belongs here). **Sequence:**
1. Launch the **brief Critic re-confirm** of v2 — the addendum at the end of
   `shared/critic_instructions_s0_4_freeze.md` scopes it to the two HIGH fixes (P6-F1→§B,
   P6-F2→§C/§D), the PR-6 §G-addendum ride-on, and the mechanical folds:
   `claude "Read shared/critic_instructions_s0_4_freeze.md and follow it."`
2. On its APPROVE, **sign** (e.g. "sign the S0.4 packet"). Your signature also **ratifies the PR-6
   §G-addendum** (the multi-tap E₀ re-derivation riding on frozen PR-4 §N — supersession discipline).

**Unblocks:** S0.4-0 calibration ($0, local, 5 items staged in `task_queue.md`) → S0.4a (PAT + SPSA).

## ✅ RESOLVED (retained in filing order, newest first)

### ✅ E-2026-06-17-1 — Critic AMEND on the S0.4 packet → **RESOLVED 2026-06-17 by delegation ("OK I trust you")**; Supervisor's D1/D2 calls recorded below; writing v2

> **RESOLVED 2026-06-17 (Lucas: "OK I trust you" — delegated the two HIGH calls to the Supervisor).**
> Supervisor's resolution (transparent, veto-window left open):
> - **D1 (P6-F1) → measured-minimal-controllable input map + honest fallback.** Register the *rule*,
>   not a blind topology: the input map B = the **fewest input taps** (spread along the chain) that lift
>   ring-N task-gradient to **≥ 10⁻³·ring-1 at C-2**, measured at S0.4-0; **report the E/O channel count
>   to the S0.7 envelope** (multi-point drive costs conversion overhead — the §10 risk — so the
>   trainability fix is priced against it). If no bounded-tap B clears the gate → **fall back to (c)**:
>   down-scope the C-2 claim to "front-of-chain trained in situ," N=32 as a capacity study. (= the
>   well-specified version of (b) with (c) as safety net; not (a) strong-coupling.) §B smoke →
>   meaningful-ratio gate. **New consideration surfaced to Lucas:** multi-point drive ↑ E/O channels ↑
>   conversion overhead → priced, not assumed.
> - **D2 (P6-F2) → clamp on-resonance now + Executor §G-conformance check.** Evaluate clauses (a)/(b)
>   on the *saturating* κ_net; freeze m_κ=0.05, Δr=0.02; **drop the "δ-aware" label**, log off-resonance
>   de-saturation as explicit anchor-risk — unless S0.4-0 finds δ-dependent build-up is a §G
>   P_circ=Σ|aⱼ|² *conformance* fix (then fold in, margin becomes genuinely δ-aware + conservative).
> - **F3–F9** fold in mechanically.
> - **Frozen-block touch:** both D1's input-map and D2's possible δ-fix re-derive the PR-4 §N E₀
>   injection convention → they ride **Lucas's signature on v2**, not a unilateral edit (supersession
>   discipline preserved). **Path:** Supervisor writes v2 → brief Critic re-confirm → Lucas signs →
>   S0.4-0 → S0.4a. *Original escalation (the two decisions as options) below.*

### E-2026-06-17-1 — Critic AMEND on the S0.4 packet → **2 HIGH decisions are yours before I write v2** (the other 7 findings fold in mechanically)

**Filed:** 2026-06-17 (Supervisor). **Source:** `shared/critic_review_s0_4_freeze.md`, verdict
**AMEND** ("do not sign as written; two HIGH findings need a decision, then it signs cleanly").
**Supervisor position: I concur with the review in full** — no push-back on any of the 9 findings.
The Critic re-derived the load-bearing physics from the code (lasing crossing r*=0.1336 to the digit,
the connected-init chain-decay, the SPSA boundary, the δ-independence of the as-built gain). The
packet's spine is sound (PR-7 cost unit, PR-5 twin-mismatch, PR-12 R-ii, PR-6 §A saturating-for-all,
the A-over-B/C clamp rationale — all CONFIRMED). But two HIGH findings sit **under the headline** and
need **your** call because they touch the white-space claim and the frozen substrate, not just wording.

**DECISION 1 — P6-F1 (HIGH): the N=32 headline cell isn't trainable where it counts.** The §B
connected-init fix I drafted (μ_c = 0.3κᵢ) **does not work on C-2**: with the input driven into ring 1
and a nearest-neighbor chain, the per-ring task-gradient decays ~(μ/κ_net)^hop, so ring-32 sits at
**2.2e-28** of ring-1's gradient — the deep half of the 32-ring chain stays frozen at init. (N=8/C-1
reaches 4.9e-7 — marginal; the problem is specific to the long chain.) My §B "smoke" (nonzero gradient
reaches rings 2..N) is **hollow** — 2.2e-28 passes it. This is structural: a single input point + a
32-ring NN chain starves the far end *regardless of μ(0)* in the weak-coupling regime. It's really a
**controllability** problem — in SSM terms the input matrix is B = e₁ (drive ring 1 only), which is a
badly-conditioned B for a 32-state chain. **Note it affects both arms equally** (the reservoir baseline's
deep rings are dead too), so the SSM-vs-reservoir *comparison* stays fair — but the cell is effectively
N≈8, and "a 32-ring recurrence trained in situ" is not what's demonstrated. **Options:**
- **(b) — register a controllable input map (multi-point drive), my recommendation.** Drive the input
  into several rings (a richer B than e₁ — the encoder is digital → multiple DACs/taps, physically
  standard). This is the **SSM-principled fix**: it restores controllability so all 32 rings see signal,
  keeps the weak-coupling one-ring-one-pole physics (no supermodes), and **doesn't touch the claim** (B is
  digital-side, trained in both arms — the in-situ claim is about the *recurrence* μ/poles, not B; the
  reservoir contrast stays clean). Cost: it's an architecture change touching frozen PR-2 (which implied
  single-point drive) + re-derives the §N E₀ normalization — so it's **yours to bless**, and the Critic
  should re-confirm the v2.
- **(c) — honest down-scope (clean fallback).** Keep single-point drive; report the deep-ring starvation
  as a measured **controllability limit**; state the C-2 claim as "the front ~8 rings are trained in
  situ" and treat N=32 as a capacity-vs-controllability study, not a 32-ring in-situ demonstration.
  Cheapest, most honest, but a weaker headline.
- **(a) — push μ_c to strong coupling (~2κᵢ): not recommended.** It de-starves the chain only by
  delocalizing the rings into supermodes — which breaks the "one ring = one pole" framing (D-08-2) and
  likely exits the K4/realizable-pole box. Buys trainability by damaging the claim.
- **Regardless of choice:** the §B smoke becomes a **meaningful-ratio gate** (ring-N grad ≥ 10⁻³·ring-1),
  not nonzero-ness.
- *My lean: (b) if a multi-point input is acceptable to you as the architecture (it makes the N=32
  headline genuine and is the principled SSM fix); (c) if you'd rather not reopen PR-2 — in which case
  C-1/N=8 effectively becomes the honest headline and C-2 is a capacity study.*

**DECISION 2 — P6-F2 (HIGH): the "δ-aware" r_min margin you asked for can't be evaluated as-built.** The
substrate's gain uses an **on-resonance** build-up, so κ_net is **δ-independent** as built (flat over
±4κᵢ of detuning) — the δ-sweep would return the on-resonance r_min while *labeling* it δ-aware. And
clause (b)'s "energy ∝ 1/κ_net² diverges near threshold" is computed through the §N E₀ formula, which
uses the **fixed**-plane κ_net (never diverges) — so as written it's inert too. **You were right that
detuning matters** — the Critic confirms detuned rings de-saturate toward g₀ ≈ 187κᵢ and lase *more*
easily, so the on-resonance r_min is a **lower bound** (the clamp could be slightly too permissive) — but
the as-built model can't see it. **Options:**
- **(ii) — clamp on-resonance now + log the off-resonance hazard as explicit anchor-risk (my interim
  recommendation, unblocks S0.4a).** Evaluate clause (a) on the *saturating* κ_net on-resonance; add the
  Δr safety margin; **drop the "δ-aware / M1-validity-governed" labels** in favor of an honest "on-resonance
  clamp; detuned-ring de-saturation is an unmodeled lasing hazard, logged." Fixes clause (b)'s plane
  (evaluate on saturating κ_net, not §N E₀) so the M1-validity arm *can* bind on-resonance.
- **(i) — make the gain δ-dependent (the real fix, needs a substrate check first).** PR-4 §G's registered
  formula is P_circ = Σⱼ|aⱼ|², which **is** δ-dependent if it uses the actual field — so the on-resonance
  proxy may be an **implementation simplification, not a registered choice**, and conforming it to §G
  (δ-dependent build-up) could be a *conformance fix* (no freeze change, like the S31-F1 gain-mode flip)
  rather than a model addition. **I'd have the Executor check this at S0.4-0**; if it's a cheap conformance
  fix, we do it and your δ-aware margin becomes real and conservative; if it's a genuine model addition,
  we stay with (ii) and log the hazard.
- *My lean: approve the **path** — clamp on-resonance (ii) so S0.4a isn't blocked, AND task the S0.4-0
  Executor to check whether δ-dependent build-up is a §G-conformance fix; fold it in if cheap, else (ii)
  stands with the hazard logged. You approve a path, not a binary.*

**The other 7 findings (P6-F3..F9) — I fold these into v2 mechanically, no decision needed** (flagging
for transparency): F3 freeze m_κ=0.05 / Δr=0.02 as registered (not "candidate"); F4 put the explicit
numeric δ-band in §D (coupled to Decision 2); F5 report PAT **decomposed** (M-par-only / M-struct-only /
both / perfect-twin), never only combined; F6 register the SPSA c-grid so the −c arm can't cross r*
(boundary-bias handling, no gradient-method analogue); F7 pin the rank principle (device-passes primary,
digital side-ledger **always co-reported**, never claim "most sample-efficient" without both; exact
tiebreaker explicitly deferred to PR-9); F8 state S0.4 can't *close* until PR-3's ceiling rule freezes
(S0.4a may start); F9 fix the PR-12 init-consistency wording (category error — μ_c/δ aren't κ_ext ratios;
only κ_ext-init + the damping sweep-range live in [r_min,3]) + reword roadmap objective (d) "characterize
a curve," not "choose a point."

**Path:** your two rulings → I write the packet **v2** (your D1/D2 choices + F3–F9 folded) → **brief Critic
re-confirm** (the Critic offered "with those, I'd sign it"; D1-(b) especially warrants a re-look since it
reopens PR-2) → your signature → S0.4-0 → S0.4a. **You can answer in a couple of lines** — e.g. *"D1: b
(multi-point drive ok); D2: approve the path (clamp on-resonance, Executor checks the conformance fix)."*

---

### ✅ E-2026-06-13-2 — all three S0.4-gating rulings RESOLVED 2026-06-17 (saturating-all · clamp A · R-ii) → **S0.4 freeze packet PR-6/7/5/12 PROPOSED, ready for Critic review then your signature**

> **RESOLVED 2026-06-17.** Lucas ruled all three: **(1)** gain `saturating` for all four estimators
> ("let's do the saturating"); **(2)** κ_ext **clamp A** (δ-/M1-validity-aware r_min rule); **(3)**
> PR-12 **R-ii** (distinct trainable-damping knob at fixed g_f=0.9). Supervisor drafted the packet
> into `preregistration.md`: **PR-6** (fairness contract, CRITICAL — saturating-all, clamp A §C,
> connected init §B, sweep recipe §D, equal budgets §E), **PR-7** (cost metric = device passes),
> **PR-5** (PAT twin-mismatch — structure now, numeric levels recon-deferred to S0.4-0), **PR-12**
> (R-ii disposition). All ⬜ PROPOSED. **Next: Lucas launches the Critic phase-boundary review**
> (`critic_instructions_s0_4_freeze.md` staged) → signature → S0.4-0 calibration (δ-aware r_min +
> connected-init smoke + PR-5 recon) → S0.4a. *Original item (the three asks) below, for the record.*

### E-2026-06-13-2 — S0.3-1 ACCEPTED + Critic APPROVE-WITH-EDITS → CONFIRM 1 ✅ DONE (2026-06-17, saturating) · RECONCILE 1 + κ_ext-clamp (D-2026-06-13-1) ✅ DONE 2026-06-17

**Filed:** 2026-06-13 (Supervisor). **Updated 2026-06-13 after the Critic report**
(`critic_review_s0_3_1.md`, verdict **APPROVE-WITH-EDITS**, independently re-run 9/9).
**Context:** the Executor delivered the shared dissipative-ring substrate (S0.3-1); I verified
and **ACCEPTED** it (re-ran tests 9/9, read them for substance, hand-checked E₀, pasted the
calibration into PR-4). The Critic then independently confirmed the build is correct and
freeze-faithful, **confirmed my one finding (now HIGH)**, and added three catches. The substrate
is sound to carry into S0.4. **The freeze-conforming code edits are already posted to the
Executor (S0.3-1b, ACTIVE). Two items are yours.**

**✅ CONFIRM 1 — RESOLVED 2026-06-17: Lucas — "let's do the saturating."** All four estimators run
`gain_mode="saturating"`, so SPSA's two forward passes and the gradient methods' backward passes
target *one* function. The substrate already defaults to it (S0.3-1b); I register the bake-off-wide
consequence in **PR-6**. **Consequence now binding:** locking saturating is exactly what makes the
K4 r=0.1 edge lase (D-2026-06-13-1), so the κ_ext-clamp policy is now a *required* pre-S0.4a
decision (Supervisor leans option A), not optional. *Original ask, for the record:*

**CONFIRM 1 — gain mode (downgraded from "decide" to "confirm": the Critic foreclosed the other
option).** I'd offered you fixed-vs-saturating as an open interpretation. The Critic's textual
read closes it: §G's "runs at g_rt = 0.9×intrinsic" is the operating-point *target* (hit by the
saturated solve at the registered drive), and the **next clause** ("differentiable function of
the episode drive statistics, no detach") + §N-E6 ("as physics, not renormalization") **mandate
the saturating mode** — "fixed" is simply unfaithful. So this is **not a freeze reinterpretation**;
flipping the code default conforms it to the signed freeze (S0.3-1b does this). It matters: the
Critic measured the dropped gain gradient at **27% of the κ_net channel at θ₀ and 6× the retained
term (sign-flipped) at the trainable edge** — "fixed" is a structurally different model, and the
F18 gate was hollow on that path. **The one thing for you to confirm (not reinterpret): the
bake-off-wide consequence — all four estimators run `gain_mode="saturating"`, so SPSA's forward
passes and the gradient methods' backward passes target one function.** I'll register that in
**PR-6**. Say "confirmed" (or flag it) when convenient; it's a PR-6 item, not urgent today.

**✅ RECONCILE 1 — RESOLVED 2026-06-17 by Lucas: R-ii** ("R-ii, with PR-12/K4/PR-6
init-consistency checked and r* verified inside M1's validity"). D-LinOSS damping = the **trainable
per-ring net loss** (κ_ext over the clamped §C box) at **fixed g_f=0.9**, not a g_f sweep. The
coarse sweep used the wrong axis → **convergence-controlled rerun** varies the trainable-damping
range at fixed g_f=0.9 (gated on this signature). PR-12 collapses into PR-6 §C/§D + a BPTT-reference
diagnostic. Registered as **PR-12 R-ii PROPOSED** + the init-consistency + r*-in-M1-validity checks
(S0.4-0). *Original ask below.*

**RECONCILE 1 — PR-4 §G ↔ PR-12 (a real knot the Critic surfaced; touches signed PR-4, so it's
yours).** The damping sweep parametrized "damping" as the gain compensation g_f — **but g_f=0.9
*is* PR-4 §G's registered gain operating point** (κ_net = 0.1κᵢ + 2κ_ext). So PR-12 can't freely
"select" a g_f: a pick of g_f≠0.9 would contradict the signed PR-4. Two readings, your call:
- **(R-i) PR-12 is subsumed by PR-4 §G** — the "damping cell" *is* the registered g_f=0.9
  operating point; no separate PR-12 sweep/freeze is needed (drop PR-12 or make it a pointer to
  §G).
- **(R-ii) D-LinOSS damping is a distinct knob** (my lean) — the *trainable* per-ring net loss
  (the κ_ext/pole-placement range K4 explores) at **fixed** g_f=0.9, which is what S0.6 actually
  sweeps. Then the coarse sweep used the wrong axis (it varied g_f instead of the trainable-damping
  range at fixed g_f), and the convergence-controlled rerun should vary *that*.
I lean **(R-ii)** but this is a methodology+freeze question, so I want your read before I commission
the PR-12 rerun. (Independent of this, the rerun must be convergence-controlled + 8 seeds at the
candidate point — the fixed-budget curve conflates accuracy with training speed, confirmed.)

**FYI (no action) — the gain story got more honest, and more aspirational.** The Critic's S31-F3:
I had reported gain reachability on the *bus* plane (C-2 reachable iff Er ≥ 1.5 dB/cm). But the
gain model saturates on the **intracavity** plane (P4-F2's own registered plane), where the
required small-signal gain is ≈**380 dB/cm** (C-2) / 403 (C-3) vs demonstrated Er ≤ 1.9 — so on
the operative plane **every gain-bearing cell, not just C-1, is material-aspirational**. I've
corrected the ledger addendum. This doesn't affect the substrate at runtime (g₀ is a model knob)
and doesn't change any freeze, but it strengthens anchor-risk (v): the M1 gain operating point is
a Stage-1+ aspiration not supplied by demonstrated Er on the plane it saturates on. Worth knowing
for how we frame the gain realism in the paper.

**Carry-forward (for the PR-6 freeze, before S0.4a):** (a) the **connected init** — μ(0)=0 leaves
rings 2..N **signal-starved** (the Critic sharpened "disconnected": exactly-zero task-signal
gradient noiseless, zero-mean *noise* gradient with ASE on — arguably worse than stalled; all four
methods hit it, the N=32 headline cell is untrainable from cold) → PR-6 must register a connected
init (the sweep's 0.3κᵢ is a candidate) or register that the in-situ claim rests on a nonzero
coupling init; (b) the **mode-for-all-estimators** (CONFIRM 1); (c) the **sweep recipe** (batch /
LR schedule / grad-clip / δ-band) — all load-bearing for trainability.

**Path (updated 2026-06-17 — your three rulings landed; packet drafted):** ✅ S0.3-1b ACCEPTED +
committed · ✅ your three rulings → ✅ **PR-6/PR-7/PR-5/PR-12 PROPOSED in the ledger** → **Critic
phase-boundary review (you launch; spec staged)** → **your signature** → S0.4-0 calibration
(δ-aware r_min measure + connected-init smoke + PR-5 recon, Executor, $0) → **S0.4a (PAT + SPSA on
the substrate)** — the project's first bake-off estimators.

---

### ✅ E-2026-06-13-1 — PR-4 v2 → **RESOLVED 2026-06-13: Lucas signed ("sign PR-4")**

**Resolution (2026-06-13):** Lucas signed PR-4 v2. **PR-4 🔒 FROZEN — the S0.3 substrate
freeze is complete.** Ask (a) was discharged pre-signature (Cui body confirmed [EV] via the
independent commentary; risk (i) closed). One registered deferral carries forward: the E₀
numeric value + saturated reachability solve, evaluated at S0.3-1 calibration and
ledger-addended before any consuming run. **The S0.3-1 substrate-build task is now ACTIVE in
`task_queue.md`; Executor launches.** Original item below.

---

**Filed:** 2026-06-13 (Supervisor). **Context:** the Critic's phase-boundary review
(`shared/critic_review_pr4-freeze.md`, 2026-06-12) returned **AMEND — "don't sign this draft;
sign the one-pass revision."** Its bottom line: *every registered choice survives attack*
(M1 + M2 validation + M3 trigger · C-1/C-2/C-3 roles · NF-A · K4, r ∈ [0.1, 3], θ₀ = 0.3 ·
K-pol-3 · H1 · O2 @ 1 mW — none reopened); what failed was completeness of the numbers
around the choices — chiefly the **unregistered operating gain** (P4-F1) and the
**unregistered saturation reference plane** (P4-F2), exactly its hostile reading 2. The
**v2 revision is now posted** in the ledger with all twelve findings applied (revision log
at the top of the PR-4 block; v1 preserved at commit 713efd4). The one registered choice v2
adds: **every gain-bearing cell runs at g_rt = 0.9× intrinsic** (the ceiling — the point the
registered ASE level was already computed at; Critic-recommended), with g = 0 and 0.5× as
labelled sensitivity rows, and all consequence numbers recomputed at it.

**Ask (a) — DISCHARGED 2026-06-13 by the Supervisor; no longer needs you.** You couldn't
reach the SPIE link (it's JS-walled to everyone, not just you). I retrieved the body numbers
a different way: an **independent peer-reviewed commentary** on the Cui paper — Ye &
Marpaung (Univ. Twente), *"Compact multi-mode silicon-nitride micro-ring resonator with low
loss,"* Adv. Photon. 5(5) 050503 (2023), CC-BY — whose explicit subject is Cui 046007 (their
Ref. 4) and which **reproduces Cui's Figures 1–2**. It confirms, at body level: loss reduced
20 → 3.3 dB/m; intrinsic linewidth 18–20 MHz → Qᵢ ≈ 10.8M; a **249-resonance histogram of
intrinsic linewidth spanning ≈ 13–25 MHz**; 3-µm multimode waveguide, modified Euler bends,
FSR 65 GHz. Our registered C-2 cell (6.8M ⇔ ≈ 28 MHz linewidth, 5.1 dB/m) is **worse than the
single broadest-linewidth device in their entire measured distribution** (≈ 25 MHz ⇔ 7.7M) —
so the conservative bound holds against the distribution, not just the mean. **Residual risk
(i) is closed**; P-AN800's platform numbers are now [EV] (via an independent secondary
source reproducing the primary figures). The commentary also independently flags the same
multimode-fabrication-yield concern that is our geometry-transfer risk (ii) — which stays
priced by the ×2-loss derate row. PDF archived at `docs/s0_3/refs/`. (Note: the "0.051 dB/cm
/ 6.8M" pair was always *our* conservative registry value, never a sentence to find in Cui —
the real question was whether the body supports the platform class we bound against, and it
does.)

**Ask (b) — the only thing left: sign PR-4 v2** (e.g. "sign PR-4"). On signature: PR-4
flips 🔒, S0.3 freeze complete, and the **S0.3-1 substrate-build task goes to the Executor**
(M1 @ g_rt = 0.9×, A2 ASE, splitting knob, K4 bounds + B1-consistency unit test, M2
validation episodes at C-2/θ₀ + C-1/θ₀, E₀ + reachability calibration with the ledger
addendum, coarse BPTT sweep feeding PR-12). If instead you want any registered value changed,
say which — it is your freeze.

---

### ✅ E-2026-06-11-2 — S0.3 gain-regime fork → **RESOLVED 2026-06-11 by Lucas: M1, with a registered M3 trigger** (extension of option (a); ruling recorded verbatim below)

**RULING (Lucas, 2026-06-11 — binding content, recorded in full):**
1. **M1 is the registered gain-model class** for the S0.3-1 shared substrate: static
   saturated operating point + ASE + slow drift, under the validity conditions as proposed
   (stationary episodes — the frozen tasks qualify; bursty inputs void; differentiable
   operating point; drift at training cadence).
2. **M2 is retained strictly as M1's one-off validation reference:** run once to confirm the
   quasi-static reduction against the rate equation at τ = 3.4 ms; not a substrate-matrix
   member; archive the comparison with the S0.3-1 validation set.
3. **M3 is neither built nor discarded: a deferred branch with a pre-committed trigger.**
   The M3 sensitivity row is built iff (a) a gated S0.5/S0.6 comparison lands within a
   margin where the gain-model class could plausibly flip the verdict — **the quantitative
   form of that margin is frozen with the bake-off pre-registrations (PR-5–9/PR-11), before
   any bake-off results exist** — or (b) the Stage-2 platform assessment tilts to III-V/SOA.
   Until a trigger fires, M3 stays named and unbuilt at $0.

**Riders for the PROPOSED PR-4 draft (drafting instructions, not post-hoc amendments):**
- **R1:** NF-A 7.0 (measured) is the headline noise cell everywhere; NF-C 3.0 may appear
  only as a clearly-labeled aspirational sensitivity, never in a headline figure.
- **R2:** the splitting-policy block must state its N-grid consequence in the same block
  (the policy is the de facto {8,32} vs {8,32,128} decision).
- **R3:** whichever drive-normalization cell is proposed, the ensemble-power stationarity
  assumption (gain operating point follows average power; train/test power statistics
  pinned) is written as a **registered assumption of M1's validity**, not a line item.

**Process (per the ruling):** Supervisor drafts PROPOSED PR-4 → Lucas launches the Critic
for the phase-boundary review once posted → Lucas signs after review. Executor idle until
the freeze.

*Original item as filed:*

**Filed:** 2026-06-11 (Supervisor). **Gates:** the PROPOSED PR-4 draft (my next output) and
S0.3-1 (the substrate build). **Source:** the S0.3-0 recon flagged this as a methodology fork
and left it open by design (`docs/s0_3/substrate_recon.md` §4e; `docs/s0_3/pr4_input_sheet.md`
§6.3) — the roadmap's S0.3 line "erbium (or III-V) gain saturation" silently spans two
physically different regimes.

**The physics (Executor-verified, [EV]):** the flagship Er:Si₃N₄ gain medium has τ = 3.4 ms.
At every registered clock (0.1–2 GS/s) the gain is frozen within an episode by 5–7 orders of
magnitude in time and ≥4 orders in energy (E_sym/E_sat ≈ 5×10⁻⁶–9×10⁻⁵, large-signal
avalanche check included). Erbium-on-SiN measurably does **not** have per-symbol gain
dynamics; sub-ns gain response is the III-V/SOA regime (carrier τ ~ 50–500 ps — the native
regime of the salvaged `pnn-multilayer` rate-equation model).

**The menu (recon §4d):**
- **M1 — static average-power-saturated operating point** g(P̄), fixed within the rollout +
  per-round-trip ASE + slow drift between episodes. The SiN-native cell at all registered
  clocks. In-loop physics: **linear** (dissipative rings + static gain); the task-solving
  nonlinearity is the readout |·|² — exactly the structure PR-2 v2 froze (R2).
- **M2 — rate equation at τ = 3.4 ms:** physically exact but numerically inert in-episode
  (integrates ≤3 %-relaxation dynamics at full rollout cost); useful only as M1's validation
  reference.
- **M3 — rate equation at τ_c ~ 0.1–0.5 ns** (the salvaged model as-is): real per-symbol gain
  patterning + in-loop nonlinearity — **the III-V fallback platform's physics, not SiN's**.

**Why this can't be defaulted:** it is not a fidelity knob — it changes what all four
estimators face: PAT's twin-mismatch families (what "structural omission" means), the
adjoint's linearity assumptions, what RHEL's echo must conjugate (a linear field vs a
gain-patterned one), and the reservoir-baseline contrast.

**Recommendation — (a) M1 headline · M2 registered as M1's one-off validation test · M3
deferred to the §8 III-V fallback axis (named, not built in S0.3-1):**
1. The proposal's platform is SiN (v0.5 §3). Registering M3 would have the bake-off train
   against physics the headline platform measurably does not have — indefensible at review.
2. Quasi-static is **measured, not assumed** ([EV]: τ = 3.4 ms; input saturation −15 dBm;
   the large-signal criterion holds with ≥4 orders of margin).
3. Registered validity conditions go into PR-4: within-episode **stationary drive
   statistics** — satisfied by construction by the frozen task families (PR-2 T-A i.i.d.
   4-PAM; PR-13 synthetic); **bursty/packeted inputs void M1** (stated boundary, per
   Bononi & Rusch). Cross-episode gain memory + pump/thermal drift live at *training*
   cadence via the existing drift knob + a slow operating-point update. The operating point
   enters the autograd graph differentiably (house constraint 3a/3b — no detach).
4. **The honest consequence, stated up front:** under M1 the substrate's in-loop physics is
   linear; the expressivity story is *trained dissipative recurrence + |·|² readout* — which
   is already exactly what PR-2 v2 froze (R2 headline; Vinckier-class reservoir baseline;
   the linear-class ceiling comparison). The white-space claim (W1: pole positions +
   couplings trained on-device) is untouched by in-loop linearity.
5. Cost: M1 is the cheapest in-rollout (no added state); the salvaged integrator stays in
   the repo for the M2 validation test and any future III-V fallback work.

**Coupling to name now (recon §4f):** the 50/90 % loss-compensation conventions only close
at P-FND and above — a CORNERSTONE cell is **passive-only** (no gain model; the fork is moot
at that corner).

**Ask — rule one of:**
- **(a) M1 (recommended)** — SiN-native cell; M3 stays a named fallback, unbuilt.
- (b) M1 headline + an **M3 sensitivity row** in the S0.5/S0.6 sweeps (labelled, non-gating
  III-V fallback evidence; roughly doubles the substrate matrix for a demoted platform).
- (c) M3 headline (would need a platform-story justification I don't see).

On your ruling I draft **PROPOSED PR-4** from the ready input sheet → Critic phase-boundary
review → your freeze → S0.3-1 substrate build (Executor).

---

### ✅ E-2026-06-11-1 — Gate-i adjudication → **RESOLVED 2026-06-11 by Lucas: "sign PR-1.1"** — PR-1.1 v2 signed as written

**RESOLUTION:** Lucas signed PR-1.1 v2 verbatim (no amendments). Ledger header flipped to
🔒 SIGNED; **S0.2-1 is closed** (G1 PASS · G3 FAIL on record, criterion void for anchor
instability · Gate i adjudicated purpose-served). Downstream proceeds on the PR-3
in-house-ceiling anchoring path; the transfer-check freeze rule is now binding. Next:
the Er gain-regime fork proposal (M1 vs M3) → PROPOSED PR-4.

*Original item as filed (for the record):*

**Filed:** 2026-06-11 (Supervisor). **Updated same day: the Critic review is in —
APPROVE-WITH-EDITS, bottom line "sign PR-1.1 with these edits" — and all edits are applied
(v2 in the ledger).** The Critic was explicitly instructed to make "they failed their gate
and moved the goalposts" stick; it reports the adjudication survives, *after* repairs it
identified: one evidentiary gap (the official fresh-seed collapse numbers were observed on
the destroyed cloud box's console but never archived — now demoted to "indicative" in v2,
with an archived local regeneration **since landed and Supervisor-verified** (S0.2-1R, 2026-06-11, $0)), two
overstatement fixes (the rerun's 0.04-pp shortfall is one test-sample wide and
environment-sensitive — the *real* evidence is the 2.1× dispersion; the collapse-incidence
statistics get honest small-sample error bars), one process-record repair (a GPU-run RNG
condition was deviated from for throughput without being logged — now reconciled; it never
touched protocol content), and sharper wording ("adjudicated", not "re-registered"; plus the
verified sentence: **this amendment changes no downstream behavior whatsoever**).

**The decision in one line:** our EigenWorms gate run missed badly (71.1% vs the frozen
90.6%) — but the diagnosis proves the *anchor* is broken, not our code, so I'm asking you to
sign an amendment that records the FAIL forever, retires that anchor, and lets the program
proceed on the validation evidence that actually holds.

**What happened (verified by me, all statistics re-derived):**
- Our gated 5-seed mean: **71.11% — FAIL.** Two of five seeds fell into a training collapse.
- The collapse is a property of the *published* method: their loss function can hit a state
  where the gradient becomes exactly zero forever (fp32 underflow) — reproduced
  bit-deterministically, entering within the first 7 steps.
- The decisive test: **the official code itself, rerun faithfully** (their runner, their exact
  library versions, their data files, the 5 published seeds, same GPU) **scores 90.56% — at
  the frozen gate's edge (one test-sample short), with seed-to-seed spread 2.1× what the
  paper reports** (individual published seeds landing at 77.8 and 83.3 — archived,
  Critic-verified from raw). Per the Critic (GA-F2): the anchor fails on **dispersion and
  environment-sensitivity**, not on a 0.04-pp technicality. The collapse fires beyond our gated run, and its
  incidence moves with the compute environment (all archived now, S0.2-1R): our stack shows
  2/5 gated seeds (GPU) and 2/3 annex seeds (local CPU) trapped; the official code's fresh
  seeds, rerun locally, show 0/8 in the strict zero-gradient sense but 1/8 frozen at chance
  anyway (seed 22222) — and the *same seed* flips between trapped and healthy across
  environments, in both stacks. No equivalence between stacks is claimed and none is needed:
  **any material incidence makes the gate a seed lottery**, and the incidence itself being
  environment-dependent is the instability in its purest form. The published 95.0 ± 4.4 is
  *consistent with* a favorable draw from that collapse mode.
- **Our implementation is exonerated** by evidence stronger than any accuracy score: with
  the same weights, our code and theirs agree to ~2×10⁻⁷ — numerically the same model. The
  init code was audited line-by-line. Our non-collapsed seeds score 93.5%, inside the
  published band. And the Heartbeat gate (G1) passed cleanly and is untouched.
- Protocol integrity: zero tuning, zero reruns of gated numbers, the Executor stopped exactly
  as the frozen miss-rule commands. Spend: $1.15 of your $7.44 ($6.29 remains).

**What I propose (PROPOSED PR-1.1, in the ledger):** record the G3 FAIL permanently as
measured · declare the G3 criterion **void for anchor instability** (the reference
implementation fails its own threshold — the criterion measures seed luck, not our fidelity)
· register **no replacement** published anchor (the alternates re-open registered exclusions
or carry the same risk; our downstream reference was always the in-house BPTT ceiling, PR-3)
· re-register Gate i as **G1 PASS + the numerical-identity dossier** → purpose served,
proceed to S0.3 · report the anchor instability as a *finding* in the paper (it genuinely
strengthens our "anchor in-house, not on published numbers" methodology) · new rule: before
any future externally-anchored threshold freezes, rerun the reference implementation once
(a ~$1 check that would have caught this pre-freeze).

**Why this isn't "moving the goalposts":** the FAIL stays on the books next to the amendment;
the amendment is signed by you, after independent Critic review, on evidence that the *gate's
premise* — not our model — failed. The hostile reading is priced in and the Critic is
explicitly instructed to attack it.

**Your move now — one item left (Critic review ✅ done; S0.2-1R record repair ✅ done,
landed 2026-06-11, ~9.6 h local CPU, $0, Supervisor-verified from the archived trails):**
1. **Rule on PR-1.1 v2** — reply "sign PR-1.1" / amendments / a different option from
   D-2026-06-11-1 (O1 record-FAIL-only · O2 replacement anchor · O3 = the proposal above).
   Every citable number in v2 is now archived; nothing else blocks on you.

On your signature: S0.2-1 closes (G1 PASS ∧ G3 void-with-finding), and the next Supervisor
outputs are the erbium gain-regime proposal + the PROPOSED PR-4 — the path that was queued
before the pause.

---

### ✅ E-2026-06-10-5 (Executor) — G3 cloud spend on vast.ai → **APPROVED 2026-06-10 by Lucas in-session** (record entry)
**What:** run the S0.2-1 G3 gated-5 EigenWorms seeds on a rented vast.ai GPU instead of the
~3–4-day local CPU run (which Lucas paused at ~47 min in, pre-first-eval). This exercises the
**option 2 standing offer in the D-2026-06-10-2 ruling** ("if calendar time matters, say so —
option 2 ... would then go through the spend escalation").
**Approval basis:** Lucas, in the Executor session, 2026-06-10 eve: *"I have still a 7.44$
credits on my vast.ai account ... the access to vast ai are in /home/lucas/Documents/
PNN_topology_search"* + "let's pause it for now" on the local runs — initiated and funded by
Lucas directly. **Budget ceiling = the existing credits, $7.44; zero new money.** Estimate:
~$2–4 for the gated-5 on a 4090-class box (annex-3 only if budget clearly allows, after the
verdict).
**Protocol conditions honored (per the D-2 ruling):** (i) **GPU parity gate**
(`scripts/parity_gpu_side.py`) runs on the box BEFORE any gated run and blocks on fail —
composition: GPU-torch ≡ CPU-torch (new gate) ∘ CPU-torch ≡ official-JAX (S0.2-1 record,
~2.4e-7); (ii) **TF32 disabled** (true fp32) + **deterministic algorithms** + bit-equal 20-step
train self-check; (iii) all RNG streams stay on CPU generators — identical run design, only the
fp32 arithmetic environment differs; (iv) frozen PR-1 protocol byte-identical (no truncation,
no tuning, same seeds/splits/configs). The paused local runs are kept as fallback until parity
passes; then killed (their partial state is discarded — protocol-clean, nothing reused).
**Spend reporting:** actuals to the results entry (instance id, $ consumed, wall-clock).

### ✅ E-2026-06-10-4 — PR-1/PR-2 freeze → **RESOLVED 2026-06-10 by Lucas: "ok go" — FROZEN**
**Ruling:** signed on the Critic-reviewed v2 blocks. **PR-1 + PR-2 (+ PR-13, early) are 🔒 in the
ledger**; S0.2-1 (in-house layer + the Gate-i runs) posted to the Executor. The ask as resolved:

**Filed:** 2026-06-10 (Supervisor). **Updated same day: the Critic phase-boundary review is done**
(`critic_review_pr1-pr2-freeze.md`) **and the blocks are revised to v2 — ready for your
signature.**

**Critic verdict:** PR-1 **approve-with-edits** (anchor choice, margins, protocol all verified
sound; edits were completeness pins). PR-2 **amend** — it caught **one real structural error in
my draft (PF-F1, CRITICAL)**: the headline configuration I pinned (single-quadrature readout +
linear digital head) made the *entire* system linear end-to-end, and the channel-equalization
task is nonlinear — a linear system measurably floors ~400× above the published anchor the
headline was built on (the Critic re-derived the floor numerically: SER ≈ 0.7 % flat across
24–32 dB, vs anchor ≈ 0). The published anchor experiment itself used a linear cavity with a
**photodiode** as the nonlinearity — i.e. the intensity readout I had relegated to "alternative."
The fix (Critic-recommended, I concur): **swap them — direct-detection intensity |·|² is the
headline readout** (still one detector + one ADC, so every audited envelope cell survives; it
even *removes* the local-oscillator the envelope never budgeted), and the single-quadrature cell
stays as a registered sweep cell reported against the linear-class ceiling. Everything else
checked clean: every number traces, no silent edits, all exclusions honest, no contradictions
with the frozen entries. The Critic also fixed a degenerate secondary-task cell (the sticky-
detection target was 94–100 % "yes" at long lags — now a rare-marker variant, class-balanced at
every lag by construction) and pinned ~a dozen conventions the Executor would otherwise have had
to invent (data streaming, init ownership, test-set sizes, split reproduction, no-tuning rule).

**I concur with every finding — all edits are applied in the v2 blocks** at the end of
`preregistration.md` (each tagged with its PF-F# for audit). What you're signing, in one breath
each:

- **PR-1 (proves our digital model is legit):** reproduce two published LinOSS results with the
  official protocol and seeds — **Heartbeat** (pass ≥ 72.1 %) and **EigenWorms** (the long-range
  flagship, pass ≥ 90.6 %, which also beats the best non-oscillatory competitor) — both within
  1σ of the published means; the official *code* (not the paper text) is the reference behavior;
  no hyperparameter tuning permitted on the gated runs.
- **PR-2 (what the bake-off actually trains):** headline task = the **canonical channel-
  equalization benchmark** (Science 2004 family) at 2 GS/s, SER at 28 dB SNR — with a binding
  honesty line that the photonic-hardware record on this channel is ~MS/s and our GS/s clock
  sizes the simulated niche only. Secondary = the synthetic memory family (lags 1→100, the
  long-lag cells registered as a memory-cliff *hypothesis*; registers PR-13 early).
  Architecture: one photonic ring-bank layer (N=32 headline), **direct-detection intensity
  readout** (the photodiode's |·|² = the one physical nonlinearity, anchor-native — the PF-F1
  fix), trainable set = **detunings + coupler strengths + inter-ring couplings** (all
  thermo-optic, ~3 channels/ring, satisfies the W1 claim on both axes); reservoir baseline =
  same physics, recurrence frozen — under the new readout it is exactly the RC field's own
  configuration, which makes our "training the recurrence beats training only the readout"
  contrast as fair as it can be. I/Q readout and the gain-rich partition stay excluded.

**Your move (one line):** **"freeze PR-1/PR-2"** — or amendments. The Critic's review is already
in hand, so signature closes the loop. On your signature, S0.2-1 (implementation + the Gate-i
run — the project's first training runs) is posted to the Executor, and you launch it as usual.

### ✅ E-2026-06-10-3 — PRE-S0.2 CONTINUATION GATE → **RESOLVED 2026-06-10 by Lucas: GO**
**Ruling:** "Go." **S0.2–S0.5 are authorized**, with the attached conditions active: task sized to
the envelope niche (S0.2/PR-2); the audit's PR-2/PR-4 carry-ins (ledger Notes); EV fixes riding
the next Executor task (S0.2-0, now ACTIVE). **Next to reach Lucas: the PR-1/PR-2 freeze ask**
(Gate-i benchmark + margin; bake-off task/architecture/partition), drafted from S0.2-0's recon.
The packet as filed (post-audit form), for the record:

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
