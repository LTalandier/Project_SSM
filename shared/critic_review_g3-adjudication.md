# Critic Review — G3 failure diagnosis + PROPOSED PR-1.1 (gate adjudication)

**Reviewer:** Critic (independent; reports to Lucas) · **Date:** 2026-06-11
**Spec:** `shared/critic_instructions_g3-adjudication.md` · **Targets:** the G3 diagnosis (results_log
S0.2-1 addenda + `results/s0_2/gate_i/` + `xcheck_official/`) and the PROPOSED PR-1.1 amendment.
**Re-derivations:** `/tmp/critic_g3_rederive.py` (Fisher/power/CIs/dodge probabilities, fp32
absorbing-state algebra, granularity) + direct loads of every per-seed npy/jsonl trail.
**Stance taken, per the spec:** I tried to make "they failed their reproduction gate and then changed
the gate" stick. Where it can stick today is identified below (GA-F1, GA-F3); the edits remove it.

---

## Overall verdict: **APPROVE-WITH-EDITS — sign PR-1.1 with these edits**

The adjudication choice (G3 criterion VOID for anchor instability · FAIL permanent and unamended ·
no replacement published anchor · gate purpose adjudicated served on G1 + the pre-specified parity
dossier · F-G3 reportable · transfer-check freeze rule) is the most defensible option on the menu,
and the conduct record is clean: the frozen miss-rule was followed to the letter (stop, zero tuning,
zero gated reruns; the official-repo cross-check was the *pre-registered* miss response — task_queue
S0.2-1 spec, written before any run). **But two evidentiary repairs must land before signature:**
the official **fresh-8** incidence leg currently has **zero archived artifacts** (GA-F1), and the
amendment leans rhetorically on its two weakest numbers — the 0.044-pp shortfall and the ~25 %
incidence point estimate — when its strongest legs are fully archived and precision-robust (GA-F2/F3).

## 1. Verified from raw (independent re-derivation — PASS)

1. **Our gated-5, per-seed, from the jsonl trails:** 19.4444/88.8889/94.4444/97.2222/55.5556 → mean
   **0.7111111224** ✓ exact. G1 from trails: **0.7290322542** ✓ PASS untouched. All values quantize
   to k/36 (k/62 for G1) ✓.
2. **Official published-5 rerun, per-seed, from the npy trails + console:** 97.22(2345)/83.33(3456)/
   97.22(4567)/97.22(5678)/77.78(6789) = **163/180 = 90.5556 %**, σ = **9.34 pp** ✓ both claimed
   numbers exact. The harness is faithful as evidenced: the official runner's own console format and
   output-directory schema, early stops at 13k–20k steps, no precision/determinism flags anywhere in
   the logs (consistent with "official code as-is"). No traps on these 5 ✓ (all trained; the low
   seeds are degraded, not chance).
3. **The trap mechanism, re-derived analytically and numerically (checklist 1):** for
   L = −Σ y·log(softmax+ε), ∂L/∂z = −(p_t/(p_t+ε))·(1_t − p). In fp32, exp underflows to exactly 0
   at logit gap ≳ 104 → p_t ≡ 0.0 → gradient **exactly 0** (the −1/ε is multiplied by the Jacobian's
   p_t ≡ 0); the correct-saturated side gives p_t ≡ 1.0 exactly → gradient exactly 0 as well (both
   verified in float32). A healthy log-softmax CE would give |p−y| = O(1) in the same state — the
   ε-inside-the-log form is the bug, and it is precision-class-independent (elementwise fp32 in both
   stacks; TF32 touches only matmuls). Escape paths checked: Adam's momentum tail decays
   geometrically from entry (and Adam's scale-invariance is moot at gradient ≡ 0 exactly — the truly
   absorbing basin is the exact-underflow region, which is where these runs sit); dropout would need
   to cut a >104-nat gap to <~20 with frozen weights — negligible, and the trails show it never
   happened. **"Absorbing" is the right word.**
4. **Internal-consistency check nobody claimed:** both collapsed seeds stopped at exactly 12,000
   steps with best-val = their first eval (6/35, 15/35) — precisely what trap-at-step-≤1000 + the
   ">10 non-improving evals" stop rule predicts (eval 1 sets best-val; stop after eval 12). The
   collapse signature is visible in our archived gated trails independent of any diagnosis script.
5. **Port exoneration architecture (checklist 4/5):** the parity dossier (2.4–2.7e-7 CPU↔JAX both
   anchors; 1.2–1.5e-7 GPU; train+inference) was reported in the *original* S0.2-1 entry — i.e. on
   record **before** the G3 runs — and the cross-check harness is in the pre-run task spec: nothing
   about the exoneration is post-hoc. Init audit covers every trainable parameter class (Linears
   incl. biases, A/steps, B, C, D); BN constants are init-trivial (nit, GA-F7). The healthy-band
   comparison conditions on the **mechanism flag** (|grad| ≡ 0 entry), not on accuracy — that is
   conditioning on an independent variable, legitimate as *corroboration*; it is correctly listed
   third behind parity + init audit. The 5-shared-seed paired comparison (ours 2/5 trap vs official
   0/5) gives p = 0.44 — also indistinguishable.
6. **Cross-references (checklist 9):** PF-F9d v2 text says verbatim "the bake-off's operative
   reference is the PR-3 in-house ceiling, not the published number" ✓; the D-08-2 Notes bullet and
   the PR-3 row say the same ✓ — the "registered downstream reference was always in-house" leg is
   real, pre-dated the failure, and I signed its calibration knowing a miss meant
   diagnose-don't-tune. Annex-3 cancellation is non-gating by construction ✓. Spend: $1.1512 ≤
   $7.44, Lucas-initiated in-session, parity gate run before any gated step ✓ (one condition needs a
   reconciliation note — GA-F4).
7. **Alternatives correctly rejected (checklist 6):** (a) re-anchoring on 90.5556-or-band = anchoring
   on a number this review shows is environment-fragile (GA-F2) with fresh-seed outcomes that are a
   trap lottery (P(≥1 trap in 5) ≈ 0.6–0.9 over the credible incidence range) — worse than no anchor;
   (b) MotorImagery re-opens a *registered* exclusion post-failure — textbook forking paths, and
   carries the exact transfer risk that just fired, now unmitigated by any pre-check; (c) bare
   FAIL-and-proceed leaves the ledger's standing summary ("Gate i FAIL") asserting the opposite of
   what the evidence shows about the in-house layer. Void-plus-adjudication with the letter-FAIL
   permanent is the honest minimum. **Re-registering a criterion whose evidence already exists is
   laundering only if the evidence was constructed for the purpose or the gate's consequences are
   eased retroactively** — here the dossier pre-dates the outcome, was pre-specified, and the
   amendment confers no downstream benefit (GA-F5 makes the block say so explicitly).

## 2. Findings

### GA-F1 (HIGH) — the official fresh-8 leg has no archived evidence; the results entry's data-path claim is false as synced
The addendum states "per-seed npy trails for all 13 official runs" were synced. **The archive
contains 6 run directories** (the published-5, fully evidenced, plus a seed-7890 directory that is
anomalous/incomplete: 2 eval records, steps.npy ending at 0). `driver_fresh.log` is **empty** (219
bytes of warning header; zero runs) and `driver_2345.log` likewise. The fresh-8 numbers the
amendment cites — **2/8 incidence, 9012 → 50.0 %, 22222 → 11.1 %, fresh mean 73.26 %** — and the
ours-annex 600-step entries (7890@7, 8901@1) exist **only as prose**; the box is destroyed. The
load-bearing archived legs (published-5 rerun; our gated trails; the mechanism) are unaffected, but
as drafted PR-1.1 cites unverifiable numbers — exactly the nail a hostile reader needs.
**Edit (pick one, before signature):**
(a) *Regenerate reproducibly (recommended, ~1–2 h, $0):* rerun the official code on 8+ fresh seeds in
the pinned **local CPU-jax venv**, commit the trails, and cite those numbers in PR-1.1/F-G3 — with
the sentence "incidence is stream- and environment-dependent; the rented-box observations (2/8) are
superseded by the archived local estimate (k/n)". A different incidence is expected and immaterial —
any material incidence breaks the anchor (GA-F3 logic).
(b) *Demote:* mark every fresh-8 number "console-observed on the destroyed instance, unarchived —
indicative only", and let the amendment rest on the archived legs (published-5 rerun + our gated
trails + mechanism). In both cases: **correct the results-log sentence to "per-seed trails for the
5 published-seed runs (archived); fresh-8 unarchived"** — the permanent record must not overclaim
its own evidence.

### GA-F2 (MEDIUM) — the 0.044-pp leg is one test sample and one precision setting wide; re-weight the wording
Passing needs 164/180 correct; the rerun scored 163 — **one test-sample classification** (2.78 pp/seed
granularity). The rerun ran jax-default matmul precision (TF32-class on the Ampere box; no flags in
the logs) while the published numbers came at least partly from V100s (no TF32). The diagnosis's
"rounding-noise difference only" is true per-op but not in effect: 13k+ steps of batch-4 training
amplify 1e-3-class matmul deltas into whole-accuracy-quantum outcome shifts — that is *also* why the
same-seed rerun differs from the paper at all. What is precision-robust: the **trap threshold**
(elementwise fp32, identical in both stacks — verified), the **σ inflation** (9.34 vs 4.4: the 77.78
and 83.33 seeds sit 7–13 pp below the mean — far beyond any rounding effect), and **non-transfer**
itself. **Edits:** in PR-1.1 bullet 1 and E-2026-06-11-1, replace "itself below the frozen 90.6
gate" framing with: "scores 90.56 % — at/below the frozen gate within one test-sample's granularity
(163 vs the 164/180 required), on a 2026 stack (jax 0.4.28, Ampere, default matmul precision), with
per-seed σ 9.34 pp ≈ 2.1× the published 4.4 — the criterion's transfer premise fails on dispersion
and environment-sensitivity, not on a 0.04-pp technicality." Strike or qualify the "rounding-noise
difference only" clause in the addendum (keep "the fp32 softmax underflow threshold is identical",
which is correct and sufficient).

### GA-F3 (MEDIUM) — incidence and "favorable draw" are stated beyond the sample's resolution; the sufficient argument is already in hand
Re-derived: Fisher two-tailed = **0.608** (fresh-only) but **0.146** using all 13 official runs and
0.444 paired on the shared seeds — report the range, not the single most favorable denominator.
Power of the 8-vs-8 design at the observed rates (0.5 vs 0.25): **8.7 %** — "statistically
indistinguishable" is an absence-of-power statement, not equivalence evidence (this design only
detects ~9:1 incidence ratios reliably). Clopper-Pearson 95 % CIs: official-fresh 2/8 → q ∈
[0.03, 0.65]; pooled 6/16 → [0.15, 0.65]; the published-set "dodge" probability (1−q)⁵ therefore
spans **[0.005, 0.85]** — the frozen "≈ 0.10–0.24" is a point-estimate band only, and at the
official-only evidence the published draw is not even surprising. The Supervisor's own fallback is
the correct and sufficient argument: **any material incidence breaks the anchor** (at q as low as
0.1, P(≥1 trap in a fresh 5-seed gate) = 41 %; the criterion is a lottery either way), and the
dispersion/non-transfer leg (GA-F2) needs no incidence estimate at all. **Edits:** (i) PR-1.1
bullet 3: replace "Fisher p ≈ 0.61, statistically indistinguishable" with "no detectable stack
difference (Fisher p = 0.15–0.61 across denominators; n=8+8 has 9 % power at the observed rates —
equivalence is not claimed and not needed: any material incidence voids the criterion)". (ii)
Replace "the published 95.0 ± 4.4 **sits on** a favorable draw of a ~25 %-incidence collapse" with
"is **consistent with** a favorable draw from a collapse mode with material incidence in both
stacks (point estimates 15–50 %, small-n CIs wide)". (iii) Everywhere (PR-1.1, D-item, E-packet):
"fp32 **init** collapse" → "fp32 **optimization** collapse of the published objective
−Σ y·log(softmax+1e-8)" — it is entered by training steps 1–7, not at initialization, and the
LinOSS authors would rightly object to the misnomer. (iv) Harmonize the D-item's "P ≈ 20 %" with
whatever band survives (i)–(ii). With these, the F-G3 paper wording passes the
authors-reading-it test (checklist 7): every remaining claim is archived, environment-qualified,
and mechanism-named.

### GA-F4 (MEDIUM) — RNG-stream record: an approved condition was altered mid-flight and the addendum asserts the opposite
E-2026-06-10-5 condition (iii), as recorded at approval: "all RNG streams stay on CPU generators."
Commit `087a346` (during the GPU campaign) moved **dropout-mask generation device-native** for
performance ("fixes 950 ms/step CPU-draw stall"), and the addendum still says "Gated-5 launched …
(same frozen protocol, **CPU RNG streams**, …)". Stream identity is genuinely framework-inherent
non-protocol content (the lottery framing absorbs any stream), and the outcome stands as measured —
but a Lucas-approved condition was deviated from without a recorded deviation, and the claimed
declaration location ("declared framework-inherent in this entry's original config note") does not
exist in the committed config records (the jsonl config blocks carry no such note; the earliest
committed declaration is the `087a346` commit message). **Edit:** one reconciliation sentence in the
results addendum: "Deviation from E-5(iii), recorded: dropout masks moved to a device generator
(commit 087a346) for throughput; init/shuffle remained CPU-drawn; stream bits were never protocol
content (PR-1 pins behavior, not bit-streams) — the gated outcome is conditional on the realized
stream either way, which is precisely the property F-G3 establishes." And fix the "original config
note" pointer to cite the commit, not a note that isn't there.

### GA-F5 (LOW) — make the amendment's strongest structural defense explicit
Two sentences close the remaining rhetorical surface: (i) reframe "Gate i is **re-registered** as
G1 ∧ dossier" → "Gate i is **adjudicated** on the surviving pre-specified evidence (G1, gated PASS;
the numerical-identity dossier, on record before the G3 runs); **no new accuracy criterion is
registered** — none is needed, the registered downstream reference is PR-3"; (ii) add: "**this
amendment changes no downstream behavior** — no task, threshold, or budget consumed by S0.3+
depends on G3; its only effects are the permanent record and S0.8 wording." Both claims verified
true (§1.6). "Re-registered" is the one word in the block that feeds the goalpost-moving reading;
"adjudicated" is what is actually happening.

### GA-F6 (LOW) — transfer-check rule: scope + cost clause
Well-formed and cheap here, but add: "applies to externally-anchored **accuracy/threshold** freezes
(PR-4-class physics freezes have no reference implementation — out of scope); run at the smallest
scale that exercises the gating statistic; if the check is infeasible at proportionate cost, that
infeasibility is itself registered as anchor risk at the freeze."

### GA-F7 (LOW) — record nits
F-G3's "90.6 ± 9.3" → write **90.56** (the rounding collides with the threshold value and reads as
rhetoric). Official seed-6789's val→test gap (best-val 97.14 → test 77.78 on 35/36-sample sets) is
worth one sentence as anchor-noise color — the published protocol's own selection convention swings
~20 pp on this dataset. Init-audit completeness: add "BN scale/bias init-trivial (1/0), state arrays
excluded from trainables — covered by the param-count reconciliation". The `solver_Heun` field in
the official output paths is the Walker-codebase directory template, not the integrator used —
pre-empt the pattern-matcher with half a sentence in the data-path note.

## 3. Checklist disposition
1 Trap real/attributed — **CONFIRMED** (re-derived analytically + numerically; both saturation
directions exactly zero; escapes bounded; early-stop arithmetic matches raw) (§1.3–1.4). 2 Official
rerun faithful — **published-5 leg verified from raw**; the −0.044 pp is one test sample (GA-F2);
77.78/83.33 verified from npy ✓; **fresh-8 leg unarchived** (GA-F1). 3 TF32 — threshold claim sound,
"rounding-noise only" overbroad; conclusions survive on the precision-robust legs (GA-F2).
4 Port exoneration — parity+init audit sound and pre-specified; stream freedom existed (official-init
transplant was feasible) but is non-load-bearing since the official code fails without any port in
the loop; 4/8-vs-2/8 power = 8.7 % — "indistinguishable" must be downgraded; Supervisor's
"either-incidence-breaks-it" is the sufficient logic (GA-F3). 5 Healthy-band — legitimate
(mechanism-conditioned), correctly subordinated (§1.5). 6 Adjudication — most defensible option;
alternatives rejected for verified reasons; SERVED-vs-PASS + permanent FAIL survive the hostile
reading **after** GA-F1/F3/F5 (§1.7). 7 F-G3 wording — fixed by GA-F2/F3/F7. 8 Process rule —
GA-F6. 9 Cross-refs — all verified (§1.6); GA-F4 is the one process-record conflict found.

## 4. The line for Lucas
**Sign PR-1.1 with these edits** — specifically: GA-F1 (archive or demote the fresh-8 leg; correct
the data-path sentence) is the only item I would treat as blocking signature; GA-F2/F3/F4 are
wording/record repairs that should land in the same pass; GA-F5/F6/F7 are one-liners. The
adjudication itself is sound: the gate failed, nobody tuned, the criterion's premise is measurably
broken on archived evidence, and the amendment as edited gains the program nothing downstream —
which is exactly why it survives the hostile reading.

---
**Protocol note:** findings go to Lucas; the Supervisor responds, if needed, via a revised PR-1.1 or
a new instructions spec — not by editing this review.
