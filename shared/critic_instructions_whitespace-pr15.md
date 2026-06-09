# Critic review spec — PR-15 white-space gate (adversarial pass + criterion audit + F14 reconciliation)

**Filed:** 2026-06-09 (Supervisor). **You report to Lucas, not the Supervisor.**
**Context:** D-2026-06-09-1 adopted (Lucas "ok go", 2026-06-09): verification debt #1 — the white-space
prior-art search — is front-loaded pre-S0.2 under **PR-15 (🔒 FROZEN)**. Read the PR-15 detail block in
`preregistration.md` first; then D-2026-06-09-1 (RESOLVED) in `decisions_needed.md` for the full
rationale (original argument: git `954d2d2`). The Executor is running the systematic sweep (task S0.L-1)
→ `docs/s0_L/debt1_whitespace_search.md` + a `results_log.md` entry.

**Your pass is the second modality of a two-modality protocol, and your brief is adversarial: KILL THE
CLAIM.** The claim under test (existence form): *recurrent parameters — parameters that define the
recurrence of a physical photonic system — updated on the physical device by gradient-based/-estimating
training: never demonstrated.* You succeed by finding the prior everyone else missed, not by agreeing.

## Checklist

1. **Blind adversarial search FIRST.** Before reading the Executor memo, run your own hunt for a prior
   satisfying the PR-15 kill-rule (q1 *internal-to-recurrence* ∧ q2 *on-device-in-the-loop* ∧ q3
   *gradient-based/-estimating*). Hunt where the Executor is least likely to look: adjacent fields
   (RF/microwave-photonic adaptive filters; optoelectronic oscillators; coupled-laser-array control;
   physical-learning demos outside mainstream photonics that contain a photonic recurrence; analog
   electronic-photonic hybrids where the recurrence is optical), theses, conference-only papers,
   non-English venues, pre-2015 literature. Log your queries (your trail must be reproducible too).
2. **Then audit the Executor memo, verdict by verdict, against the primaries.** Highest scrutiny on:
   (a) every **q1 call** — internal vs readout is where motivated reasoning would hide; (b) every
   "clear" verdict on lanes (ii)/(iii); (c) the **Bueno/Brunner boundary memo** — give it a hostile
   read (does any paper in that line update *feedback/internal* params on hardware with a
   policy-gradient?); (d) any verdict resting on a source the Executor did not actually reach.
3. **Criterion audit (PR-15 itself).** Is the q1∧q2∧q3 rule sound and complete? Construct adversarial
   prior-*classes*: anything that *should* falsify the claim but slips the rule, or vice versa
   (e.g. partially-internal parameter sets; a digital recurrence with photonic in-loop elements;
   on-device fine-tuning after offline training — does q2 handle it?). If the rule is defective,
   propose an amendment — it goes to **Lucas** (PR-15 is frozen; amendment requires his sign-off).
4. **F14 reconciliation (routed to you by D-09-1).** Your roadmap-review F14 left debt #1 S0.8-paced on
   data-dependency grounds; D-09-1 front-loads it on value-at-risk grounds. The Supervisor holds both
   lenses are compatible (F14 = dependency statement for #2/#3; D-09-1 = scheduling principle for cheap
   kill-shots). Confirm or rebut, and state whether the go/no-go belongs in the PR ledger.
5. **Your verdict on the gate:** PASS (one-sided — say so explicitly) / FATAL / AMBIGUOUS-escalate,
   with your own candidate table for anything you found that the Executor didn't.

## Output

`shared/critic_review_whitespace-pr15.md` — findings F1, F2, … with severity (CRITICAL/HIGH/MED/LOW),
your candidate table, the criterion audit, the F14 reconciliation, and the gate verdict. Lucas reads it
directly; any FATAL/AMBIGUOUS candidate goes to him with the primary attached, regardless of what the
Executor memo concluded.

**Timing:** your blind phase (item 1) can start immediately; items 2–5 need the Executor memo. The
pre-S0.2 continuation gate waits on your review (gate model).

---

## Part-2 addendum (Supervisor, 2026-06-09 — after both modality outputs landed)

1. The Executor memo is in (`docs/s0_L/debt1_whitespace_search.md` + E-2026-06-09-4): Part 2 (spec
   items 2 + 5) is **green-lit now**. Part 1 received — strong work; the WS-F1 hole is real and the
   Supervisor has recommended Lucas sign your amendment (E-2026-06-09-5).
2. **Merge the two candidate tables into one** (the gate's verdict table) and reconcile the
   cross-modality asymmetries **both ways** (your Fisher 1987 ↔ their Wu / Milanizadeh / Zhao): state
   *why* each modality missed what it missed — that diagnosis directly improves the S0.8 final-sweep
   design.
3. If/when Lucas signs **PR-15.1** (q4 + WS-F3 rider + WS-F5 taxonomy), **re-classify the merged table
   under the amended rule** (keep your L/A dual-column convention). If he declines, return the verdict
   under the frozen letter and say plainly what that verdict is worth.
4. Highest-scrutiny items for the audit, from the Supervisor's read of E-09-4: the Wu q1 evidence
   trail (is "U is never enumerated" actually exhaustive of paper + SI?); the Milanizadeh
   q4-boundary call; any Executor "clear" verdict resting on an abstract.
5. Your final gate verdict goes to **Lucas**, as before. The continuation gate waits on it.
