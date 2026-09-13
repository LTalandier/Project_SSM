# Publication plan — Project_SSM

**Current disposition, 2026-09-13 (supersedes the historical plan below):**
Lucas approved one bounded corrected mismatch rerun, then P1 arXiv preparation.
S0.13 is complete with an exact anchor and no advantage at any tested mismatch
level. P1 includes this correction and the PR-20 negative inline result. Standalone
P5 publication is deferred. Hardware and higher-rate work remain paused; P2
contact is separate. The review PDF, source ZIP, and metadata are documented in
`paper/SUBMISSION.md`; authenticated author submission and linked public release
are the remaining external steps.

**Status:** ⬜ PROPOSED (2026-07-07, Supervisor) — responds to Lucas's goal directive
(2026-07-07): *"make something publishable (and hopefully buildable) from this project —
it can be anything with SSM and photonics."*
**Authority:** this is a plan, not a freeze. Venue choices and unit P2's go/no-go are
**Lucas's decisions** (outward-facing). The roadmap (`stage0_roadmap.md` §S0.8) remains the
methodological authority; this file only maps roadmap outputs onto publishable artifacts
and pulls the *writing* forward — no run, gate, or pre-registered rule changes.

---

## The map in one paragraph

The project produces **one primary paper now in progress (P1, the Stage-0
methods/feasibility paper)**, whose sole blocker is the S0.4 packet-v3 signature; **one
fast, already-data-complete side note (P2, the LinOSS EigenWorms reproducibility
finding)** that could be on arXiv within weeks but needs Lucas's explicit go because it
critiques published work; and **one hardware letter (P3, the "first" itself)** — the
*buildable* arm — which Stage 0 exists to de-risk and which is gated by the S0.7 envelope
before any MPW spend. The pre-registration discipline means roughly half of P1 is
writable **today**, before a single bake-off run.

---

## P1 — Stage-0 methods/feasibility paper (PRIMARY)

**Working claim set** (framing per roadmap S0.8, F19/F22 already binding):
1. First apples-to-apples **in-situ-trainability bake-off** — SPSA vs PAT vs recurrent
   adjoint vs RHEL — for a *recurrent, dissipative* photonic SSM, on one shared realistic
   SiN ring substrate (finite Q, saturating gain, ASE), scored on
   sample-efficiency-to-target under realistic noise (PR-6 fairness contract, PR-7 cost
   accounting).
2. The **oscillator↔SiN-ring mapping** with the realizable pole region (S0.1, B1–B3
   memos in `docs/s0_1/`).
3. The **damping operating point** result (D-LinOSS axis, PR-12 R-ii framing).
4. The **systems-advantage envelope** (S0.7-full; conversion overhead priced — the §10
   question answered honestly either way).
5. The **white-space positioning** (debt #1, PR-15 dated search, `docs/s0_L/`) +
   the capacity/controllability finding (effective participating dimension; S0.4-0
   participation profile) as the honest-N reporting layer.

**Robust to outcome:** gate (ii) *failing* (no method trains at realistic noise) is still
a publishable feasibility bound, and the envelope failing to clear digital is a
publishable pre-MPW-spend finding (roadmap S0.7-full gate). P1 does not bet on a positive
result.

**Dependencies (critical path):** packet-v3 Critic re-confirm → **Lucas signs** →
S0.4-0 ($0, Executor) → S0.4a PAT+SPSA → S0.4b/c adjoint+RHEL → S0.5 bake-off (PR-8/9
freeze first) → S0.6 damping → S0.7-full. Every week the signature waits is a week of
S0.4 not running.

**Writable NOW (no results needed) — Supervisor work, starts immediately:**
- Introduction + white-space/prior-work section (from `docs/s0_L/debt1_whitespace_search.md`
  + `whitespace_claim_wording.md`; dated mid-2026 sweep refresh stays S0.8-paced).
- Methods: substrate (frozen PR-4 v2 → prose), the four estimators as specified (PR-5/6/7
  + proposal §5), the fairness contract as a *feature* (registered-report-style
  credibility — the prereg ledger itself is citable supplementary material).
- Mapping section (S0.1 memos are near-final prose already).
- Limits-of-model section (F19 wording exists in the roadmap).
- Figure plan + results-section skeletons keyed to pre-registered gates (numbers blank).

**Venue (Lucas decides; Supervisor recommendation first):** arXiv preprint regardless;
then **APL Photonics or Optica** (photonics-native, methods-friendly) as primary target;
*Nanophotonics* alternative. An ML-side workshop version (NeurIPS ML4PS-type) is optional
visibility, not the primary. Decision needed only at submission time — does not block
writing.

**Artifact home:** `paper/` (new top-level dir; `paper/outline.md` first, then section
files). Supervisor-owned; Critic reviews the manuscript at S0.8 as usual.

## P2 — LinOSS EigenWorms reproducibility note (FAST, DECISION NEEDED)

**Finding (already on record, S0.2 G3 adjudication):** the published LinOSS EigenWorms
anchor **fails a faithful official-code rerun** — 90.56 % mean, seed σ 9.34 ≈ 2.1× the
published σ, plus an fp32 optimization collapse — while the float32-exactness parity
dossier (CPU↔JAX 2.4–2.7e-7) exonerates the port. Evidence: `results/s0_2/`,
`shared/critic_review_g3-adjudication.md`, status memo 2026-06-11. The project already
consumed this finding internally (anchor void; PR-3 in-house ceiling).

**Why publish:** citable within weeks at $0 new compute; strengthens P1 (we anchor
in-house *because* the published anchor is irreproducible — better said once, carefully,
in a dedicated note than compressed into P1's related-work); community value
(reproducibility of long-range-benchmark claims is exactly the kind of finding venues
like ReScience C / ML-reproducibility tracks exist for).

**Why it's Lucas's call, not mine:** it is an outward-facing critique of a published
result. Options: (a) contact the LinOSS authors first with the dossier (collegial,
standard practice, small delay); (b) arXiv note directly; (c) fold into P1's related
work and don't publish standalone; (d) drop. **Supervisor recommendation: (a) then (b)**
— author contact first, note follows regardless of reply within a stated window.
**Not started until Lucas rules.** Filed as **E-2026-07-07-1**.

**If GO:** Supervisor drafts from the dossier; Executor re-verifies every number against
`results/s0_2/` raw data (fresh eyes, no rerun needed); Critic reviews before anything
leaves the repo. Estimated: days, not weeks.

## P3 — Stage-1 hardware letter (the "FIRST"; the *buildable* arm)

**Claim:** the headline — *recurrent parameters (pole positions + inter-ring couplings)
updated on the physical device by gradient-based/-estimating training* — first in-situ-
trained recurrent photonic system. Collectible **only on hardware** (standing frame,
E-2026-06-10-3).

**Path:** Stage-0 gates pass → S0.7-full envelope clears (the pre-MPW spend gate) →
CORNERSTONE/LIGENTEC MPW (SiN, gdsfactory flow) → PAT/SPSA on-chip training (the
hardware-committed methods; adjoint/RHEL only if the bake-off promotes one). Funding
lever: **AI-for-Science compute credits ($30k)** noted in PROJECT_HANDOFF §8 — relevant
to Stage-1 simulation/twin load, application can be prepared once Gate ii passes.
Realistic earliest: MPW submission 2027 (quarterly runs + months of fab). Nothing to
publish here yet; P1 *is* the de-risking document a collaborator/foundry sees first.

## P4 — capacity/controllability finding (FOLDED INTO P1 by default)

The single-drive NN-chain gradient-starvation result (effective dimension ≈3/32 at C-2;
T- and loss-robust; multi-tap remedy) is registered as P1 content (§B v3 participation
profile). **Spin-out to a standalone letter only if** the S0.4-0 measurement makes it
crisp and P1 gets crowded — revisit at S0.4 close. No action now.

---

## Near-term actions

| # | Who | Action | Blocked by |
|---|-----|--------|------------|
| 1 | **Lucas** | Launch Critic v3 re-confirm: `claude "Read shared/critic_instructions_s0_4_freeze.md and follow it."` → on APPROVE, **sign v3** (E-2026-07-05-1) | — |
| 2 | **Lucas** | Rule on **P2** (E-2026-07-07-1): (a) contact-authors-then-note ← rec · (b) note directly · (c) fold into P1 · (d) drop | — |
| 3 | Supervisor | Draft `paper/outline.md` + the pre-writable P1 sections (Intro, Methods-substrate, Mapping, Limits-of-model, figure plan) | nothing — starts now |
| 4 | Executor | S0.4-0 (5 items, $0) then S0.4a | action 1 |
| 5 | Supervisor | P2 draft | action 2 = GO |

**Discipline note:** pulling P1 writing forward changes no methodology — results sections
stay empty until their pre-registered runs produce them, and nothing in `paper/` is
citable/frozen until S0.8. The plan itself is amendable by Lucas at any time.
