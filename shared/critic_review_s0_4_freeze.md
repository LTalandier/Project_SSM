# Critic review — S0.4 freeze packet (the bake-off fairness contract: PR-6 / PR-7 / PR-5 / PR-12)

**Reviewer:** Critic session · **Date:** 2026-06-17 · **Spec:** `shared/critic_instructions_s0_4_freeze.md`
**Target:** the four PROPOSED blocks at the end of `shared/preregistration.md` — **PR-6** (fairness
contract, CRITICAL), **PR-7** (cost metric), **PR-5** (PAT twin-mismatch), **PR-12** (R-ii). Reviewed
against frozen PR-4 v2 §G/§K/§N/§S, frozen PR-2 v2, the Critic S0.3-1 review, D-2026-06-13-1,
E-2026-06-13-2, and the substrate code. All load-bearing physics re-derived from the code (the lasing
crossing, κ_net's δ-dependence, the build-up/E₀ planes, the connected-init chain-decay, the SPSA
boundary) — session scripts, results inline below.

---

## Verdict: **AMEND**

The packet is, on most axes, a careful and honest contract: **PR-7** (device-pass cost unit + the
two-ledger split), **PR-5** (twin-mismatch structure + calibration-error unification), **PR-12 R-ii**
(damping = trainable net loss at fixed g_f=0.9), and PR-6's **§A saturating-for-all** and **§C
A-over-B/C rationale** are all sound and well-argued. I confirm the §C lasing arithmetic **to the
digit** (r\*=0.1336, κ_net/κᵢ=−0.318 at r=0.1, cell-independent). But two **HIGH, signature-blocking**
findings touch the load-bearing parts, and neither is a mechanical edit — both need a decision before
signature:

- **P6-F1 (HIGH).** The §B connected-init remedy **does not de-starve the N=32 headline cell**. The
  registered candidate μ_c=0.3κᵢ leaves ring-32 at a gradient **2.2e-28** of ring-1's; the §B smoke
  ("nonzero gradient reaches rings 2..N") would **pass spuriously** on that 2.2e-28. The deep half of
  the C-2 chain is untrainable in situ from a single-point drive + nearest-neighbor topology, ~regardless
  of μ(0) in the weak-coupling regime. This is the headline bake-off cell.
- **P6-F2 (HIGH).** The "δ-aware r_min rule" Lucas explicitly required is **inert against the as-built
  substrate**: κ_net is δ-independent as built (the gain uses an on-resonance build-up), and clause (b)'s
  "E₀∝1/κ_net² diverges" won't bind if evaluated through the registered §N E₀ formula (which uses the
  *fixed*-plane κ_net, not the saturating one). As written, the S0.4-0 sweep would return r_min from
  clause (a) on-resonance only while *labeling* it δ-aware + M1-validity-governed — neither refinement
  actually binding.

Both are fixable, but the fixes are methodology/substrate decisions (a bigger μ_c moves to a
strong-coupling regime; modeling off-resonance de-saturation is a substrate addition) — so this is
**AMEND**, not APPROVE-WITH-EDITS. The remaining findings (P6-F3..F9) are pre-registration holes and
reporting-honesty edits that should ride the same revision.

### Max-effort re-examination (this pass): both HIGH findings survive, and sharpen

At Lucas's request I re-ran the review at maximum scrutiny, trying to *break* my own AMEND. The two
HIGH findings not only survive — they sharpen, and one packet claim is now outright **REFUTED**:

- **P6-F1 hardens from "deep rings hard to train" to a capacity finding.** The starvation is not a
  finite-sequence transient (ring-32/ring-1 gradient = 3e-45 / 2e-28 / 3e-26 at T=50/200/1000 —
  astronomically small at every length), not loss-specific (2.7e-28 under an independent
  MSE-to-target loss), and structural: the **effective participating dimension of the N=32 headline
  cell is ≈3 rings** — only 1 ring carries ≥0.1·|a₁|, 2 rings ≥0.01, 3 rings ≥0.001 (ring-8 already
  6e-7, ring-16 6e-11; the ±4κᵢ δ-init band doubly suppresses via detuning). So **C-2 is a ~3-active-
  ring model wearing a 32-ring label**; the mode-count/capacity the headline leans on is overstated
  ~10×, and — the deepest bite — a ~3-ring effective recurrence + a digitally-trained readout may show
  **little lift over the reservoir baseline** (§F), which is the in-data falsifier of "training the
  recurrence matters" (debt #1, the single load-bearing sentence). The multi-point-drive fix **works**
  (driving {1,9,17,25} lifts 26/32 rings into the ≥1e-3 band vs 3/32) but is a **frozen-block change**
  (B_doublet is single-port by construction; §N E₀ is single-port-calibrated), confirming this is a
  fork, not a tweak.
- **P6-F2 sharpens; the "M1-validity-governed r_min" claim is REFUTED.** §G(iii) registers only the
  *value* at θ₀ (E_sym/E_sat ≈ 5e-6–9e-5), **no void ceiling** — so clause (b)'s "≤ the registered
  ceiling" has no threshold to compare against. And even fixed to use the *saturating* κ_net, clause
  (b) **never binds before clause (a)**: at the clause-(a) floor (κ_net=0.05κᵢ, r≈0.14) the circulating
  energy is ×37 vs θ₀ ⇒ E_sym/E_sat ≈ 3e-3, still ≪1 (M1 voids nearer O(1)). Lucas's check "r* inside
  M1 validity" therefore **passes** (r* is comfortably inside — E_sym/E_sat ~1e-2 at r*), but its
  intended *consequence* (r_M1 > r* governing r_min) **does not occur**. Net: the δ-aware + M1-validity
  machinery is inert/decorative; the honest rule is **clause (a) alone** (r_min = smallest r with
  κ_net ≥ m_κ·κᵢ, +Δr ≈ 0.16), δ-independent and evaluable — with the off-resonance de-saturation
  hazard moved to anchor-risk (or a scoped substrate change), not dressed up as a clamp the substrate
  cannot compute.
- **One thing that does NOT break (balance).** The §N E₀ normalization is robust to the connected
  init — energy localizes on the driven ring, so Σⱼ|aⱼ|² shifts <5% from μ_c=0 to μ_c=0.3κᵢ. The
  frozen-E₀ ride-along one might have worried about is fine; I am not flagging it.

## Findings

| # | Severity | One line |
|---|---|---|
| P6-F1 | **HIGH** | §B connected-init μ_c=0.3κᵢ leaves ring-32 at **2.2e-28** rel. gradient (T-robust: 3e-45/2e-28/3e-26 at T=50/200/1000; loss-robust: 2.7e-28 under MSE-to-target). Structural: single-port drive + NN chain ⇒ the N=32 headline cell has an **effective participating dimension ≈3 rings** (1 ring ≥0.1·|a₁|, 3 ≥1e-3) — a ~3-ring model wearing a 32-ring label; capacity overstated ~10× and **may not beat the reservoir baseline** (debt #1). The §B "nonzero gradient" smoke is **hollow** (2.2e-28 passes). Multi-point drive fixes it (26/32 rings ≥1e-3) but is a **frozen-block change** (single-port B, single-port E₀). **Signature-blocking.** |
| P6-F2 | **HIGH** | The §C δ-aware / M1-validity r_min rule is inert/decorative as-built: κ_net is **δ-independent** (on-resonance gain build-up; max Δ=0.0 over ±4κᵢ); §G(iii) registers **no void ceiling** (only the θ₀ *value*), so clause (b) has no threshold; and even fixed to the *saturating* κ_net, clause (b) **never binds before clause (a)** (E_sym/E_sat≈3e-3≪1 at the κ_net=0.05κᵢ floor) → **"r_min governed by r_M1 > r*" REFUTED**. Honest rule = clause (a) alone (r_min≈0.16). Off-resonance de-saturation (g→g₀≈187κᵢ) is a real *unmodeled* hazard → on-resonance r_min is a lower bound (belongs in anchor-risk or a substrate change). **Signature-blocking.** |
| P6-F3 | MEDIUM | "Measure r_min + addend" is a legitimate deferral (E₀ precedent) **only if** m_κ and Δr are frozen *now*. As written both are "candidate" and the δ-band is a description, so S0.4-0 retains free knobs that move r_min → a pre-registration hole. Freeze m_κ, Δr, and the explicit δ-band at signature. |
| P6-F4 | MEDIUM | §D says the δ-band is "pinned in this block at signature" but **no number is in the block** — only "candidate radial-band image." r_min (§C) and the PR-12 init-consistency check both depend on it → double-deferred. Put the numeric band in §D before signing. |
| P6-F5 | MEDIUM | Saturating-for-all is **fair to SPSA** (it sees ∂g/∂κ_ext through its forwards — refutes "rigged for gradient methods"). But the headline PAT twin (PR-5 M-struct = gain-linearization) is handed *exactly* the ∂g/∂κ_ext omission the white-space claim rests on; the M-struct penalty must be reported **decomposed** (M-par-only, M-struct-only, both, perfect-twin), never only combined, or PAT-the-method is conflated with PAT-handed-the-gain-omission. |
| P6-F6 | MEDIUM | SPSA boundary bias: at κ_ext=r_min, any c ≥ ~0.02 pushes the −c arm sub-r\* → rollout diverges; clamping it to r_min makes the two-sided difference asymmetric (biased) — a hazard with **no gradient-method analogue**. "Equal HP budget = equal #trials" (§E) is necessary but doesn't equalize this; the SPSA c-grid must respect the feasible box (register it). |
| P6-F7 | MEDIUM | The PR-7→PR-9 rank tiebreaker = **median device-passes** structurally favors the 1-pass method (PAT: 1 pass/step vs 2 for SPSA/adjoint/RHEL) independent of per-update efficiency. Defensible as a device-efficiency rank, but whether the digital side-ledger enters the rank is **unregistered and outcome-determining** — pin that decision (now or explicitly at PR-9); never report "most sample-efficient" without the digital ledger. |
| P6-F8 | LOW | F12 residue: LR schedule/clip/SPSA-c numeric grids, the HP-tuning validation-cell identity, explicit seed lists, and the "target accuracy" definition (depends on PR-3's ceiling-relative *rule*, not yet frozen) are deferred. Most are correctly owner-tagged; state explicitly that **S0.4 cannot close until PR-3's rule freezes** (S0.4a may start). |
| P6-F9 | LOW | PR-12 R-ii is **sound** (CONFIRMED) but recasts objective (d) from "choose a damping point" to "characterize a curve" — reword roadmap (d). The init-consistency wording ("μ_c, δ-band, κ_ext-init all inside [r_min,3]") is a **category error**: μ_c (coupling) and δ (detuning) are not κ_ext ratios; only the κ_ext-init and the damping(κ_ext) sweep-range live in the box. Fix the wording (it also means the check, as written, wouldn't catch F1). |

---

## The three hostile readings, adjudicated

**Reading 1 — "the contract is rigged for the photonic side / one estimator": STICKS in two specific
forms, REFUTES the headline worry.** It does **not** rig for the gradient methods over SPSA: SPSA's two
forward passes evaluate the true saturating g(κ_ext), so its finite difference captures ∂g/∂κ_ext —
SPSA is not blind to the gain channel (P6-F5). The method structurally short of that channel is
*PAT-with-the-fixed-twin*, and that is a deliberate PR-5 test, not a rig. Where reading 1 **does** stick:
(i) the **headline cell is partly degenerate** — only the front ~8 of C-2's 32 rings are in-situ
trainable (P6-F1), so the bake-off's marquee N=32 cell can't actually exercise deep-ring training, which
flatters compact-effective-model behavior and overstates the demonstrated capacity; (ii) two metric
choices touch PAT asymmetrically and must be reported transparently — the M-struct gain-linearization
(P6-F5) and the device-pass rank tiebreaker (P6-F7).

**Reading 2 — "the clamp / connected-init quietly change the claim or the registered physics": STICKS,
and P6-F1 sharpens it.** Clamp A narrows the trainable pole region [0.1,3]→[r_min,3], removing the
longest-memory near-threshold corner — legitimately (device physics), but the white-space pole region
shrinks and the freeze rightly logs it as anchor-risk. The deeper bite is on the **in-situ claim
itself**: the freeze concedes the result rests on a *nonzero coupling init* (§B) — but P6-F1 shows the
honest concession is larger: on C-2 the deep rings are **not trained in situ at all** from this
drive+topology; they sit at μ_c. So W1 on the headline cell is "the front of the chain is trained in
situ"; the paper must carry that, not "a 32-ring recurrence trained in situ."

**Reading 3 — "the freeze leaves tunable holes (F12)": STICKS.** The load-bearing cluster is the r_min
machinery: m_κ/Δr are "candidate" not frozen (P6-F3), the δ-band is promised-but-absent (P6-F4), and the
clause-(a)/(b) evaluation planes are unspecified (P6-F2). Plus the standard residue (P6-F8). The r_min
cluster is the serious one because it *is* the clamp that contains the SPSA lasing hazard.

---

## Checklist dispositions (1–9)

**1. Saturating-for-all integrity (§A) — CONFIRMED faithful; fairness consequence = EDIT (P6-F5).**
`saturating` is the freeze-mandated mode (§G "differentiable function of the episode drive statistics,
no detach" + §N-E6); `fixed` is correctly demoted. Re-derived ∂g/∂κ_ext = −0.750 at θ₀ (all cells),
dκ_net/dκ_ext = 2.75 (sat) vs 2.0 (fixed) → fixed drops 27.3% — matches §A. **Fairness:** all four see
the *same* g(P̄); SPSA sees it through forwards, adjoint/RHEL/BPTT through the physical reverse pass,
PAT only if its twin models it. So saturating-for-all does not advantage gradient methods over SPSA; it
*does* load the PAT headline with the gain omission (P6-F5 — report decomposed). **ASE-not-shared is the
correct physical/fair call** (no common-random-numbers exist on hardware); it raises SPSA's variance
honestly, budgeted by ≥8 seeds — but register explicitly that the SPSA ± pair gets *independent* ASE (no
within-step CRN), so an implementer can't unphysically variance-reduce it.

**2. Lasing finding + clamp A, re-derived (§C) — CONFIRMED to the digit.** From the code, saturating
mode, all cells: r\* = 0.1336 / 0.1337 / 0.1337 (cell-independent ✓), κ_net/κᵢ = −0.3183/−0.3186/−0.3187
at r=0.1 ✓, +0.70 at θ₀ ✓. **The divergence is real**: M1 holds g fixed within the episode, so the
in-rollout dynamics are linear and a κ_net<0 pole diverges with no in-loop saturation clamp — exactly
the §C argument. **A over B/C is right**: B (hard-cap g≤0.9κᵢ) injects an unregistered mechanism + kinks
∂g/∂κ_ext at θ₀ (the trained gradient), C (soft barrier) can't bite a *forward-recurrence* divergence —
A is the only containment that preserves §G's form. **But the r_min *rule* is under-specified** (P6-F2,
F3) — see item 3. Note a physical fragility the clamp rationale should own: the operating point holds g
saturated only via a ×262 on-resonance build-up saturating a small-signal g₀≈**187κᵢ** down to 0.9κᵢ;
anything that drops the build-up (κ_ext↓ — handled; **detuning — not handled, P6-F2**) de-saturates g
catastrophically. The clamp covers the κ_ext axis, not the δ axis.

**3. r\* inside M1 validity (§C clause b) — REFUTED as written; clause (b) is decorative (P6-F2).**
The check Lucas asked for **passes** — r* *is* comfortably inside M1's validity (E_sym/E_sat ~1e-2 at
r*, four+ orders below the ~O(1) void). But precisely *because* it passes, the consequence the packet
built on it does not occur: I re-derived that clause (b) **never binds before clause (a)**. Three gaps,
each independently fatal to the clause as written: (i) the §N E₀ formula
(`normalization.py`/`calibration.py`) uses the **fixed**-plane κ_net = 0.1κᵢ+2κ_ext (0.38κᵢ at r=0.14,
never diverges), not the saturating κ_net (≈0.003κᵢ) — so via §N E₀ clause (b) is trivially inert;
(ii) §G(iii) registers only the θ₀ *value* (E_sym/E_sat ≈ 5e-6–9e-5), **not a void ceiling** — so
"E_sym/E_sat ≤ the registered ceiling" has no number to test against; (iii) even fixing (i) to the
saturating κ_net and picking a physical ceiling, at the clause-(a) floor (κ_net=0.05κᵢ, r≈0.14) the
circulating energy is only ×37 vs θ₀ ⇒ E_sym/E_sat ≈ 3e-3 ≪ 1, so M1 stays valid well past the
lasing-margin floor and **r_M1 < r_a always**. **Recommendation: drop clause (b).** The honest rule is
clause (a) alone — r_min = smallest r with κ_net(saturating) ≥ m_κ·κᵢ, +Δr ≈ 0.16 — which is evaluable
and δ-independent. The real physics Lucas was reaching for (near-threshold M1 breakdown; off-resonance
de-saturation, g→g₀≈187κᵢ) is **not captured by the as-built substrate** and should be logged as
anchor-risk, or bought with a substrate change (δ-dependent + circulating-energy-consistent gain) — not
presented as a clamp the code computes. The "physical-validity bound, strengthening anchor-risk" framing
is spin until that physics is actually modeled.

**4. Connected init vs the white-space claim (§B) — CONFIRMED problem, REFUTED remedy, now a CAPACITY
finding (P6-F1).** μ(0)=0 signal-starves rings 2..N (re-confirmed: exactly-zero gradient noiseless).
**The §B fix fails on the headline cell.** Per-ring |∂loss/∂δ_j| at μ_c=0.3κᵢ, drive on ring 1, C-2
noiseless: ring1 2.0 · ring2 0.20 · ring4 8.1e-3 · ring8 3.3e-5 · ring16 7.1e-11 · **ring32 4.4e-28**
— T-robust (3e-45/2e-28/3e-26 at T=50/200/1000) and loss-robust (2.7e-28 under MSE-to-target). **The
sharper framing (max-effort pass):** the settled-state amplitude profile gives C-2 an **effective
participating dimension ≈3 rings** (1 ring ≥0.1·|a₁|, 2 ≥0.01, 3 ≥0.001; the ±4κᵢ δ-band suppresses via
detuning on top of the spatial hops) — so the N=32 headline runs an effectively ~3-mode recurrence, and
the memory/capacity that "N=32" advertises is overstated ~10×. **The deepest consequence:** a ~3-ring
recurrence with a digitally-trained readout may not clear the **reservoir baseline** (§F, readout-only)
— which would collapse the very thing the bake-off exists to show, that *training the recurrence*
matters (debt #1). To de-starve ring-32 needs μ_c≈2κᵢ (μ/κ_net≈2.9, mode-delocalizing — different
physics, interacts with the realizable-pole region / K4 box); or **multi-point drive**, which I verified
works (driving {1,9,17,25} lifts 26/32 rings ≥1e-3·max) but is a **frozen-block change** (B_doublet is
single-port; §N E₀ is single-port-calibrated → re-derive for a multi-tap injection). **The supersession
is legitimate authority** (PR-2 PF-F8b delegated init to PR-6) — but the *value* and the *smoke* are
wrong: 0.3κᵢ doesn't work, and the smoke ("nonzero gradient reaches rings 2..N") passes on 2.2e-28
(hollow — make it a *meaningful-ratio* gate, ring-N grad ≥ 10⁻³·ring-1). **Honesty framing:** "μ trained
from μ_c, W1 untouched" is sound for the front ~3 rings; for the rest the honest statement is "not
trained in situ from this drive/topology." A μ(0)=0 sensitivity row is **not** sufficient; the effective-
dimension limit must be a stated structural caveat, or the headline cell / drive map changed.

**5. PR-12 R-ii soundness — CONFIRMED (R-ii correct, cleaner than R-i).** κ_net = κᵢ−g+2κ_ext *is* the
pole real part; training it via κ_ext at fixed g_f=0.9 is exactly D-LinOSS damping mapped onto the
physical knob, so R-ii (not R-i) preserves Stage-0 objective (d) — but as a **curve**, not a point
(reword (d); P6-F9). The g_f sweep was indeed an illegal DOF under §G; the convergence-controlled +
≥8-seed rerun correctly fixes the anomaly-B confound (fixed-budget conflates accuracy with speed). The
init-consistency check is the right idea but mis-worded (P6-F9: δ/μ aren't κ_ext ratios) and, as worded,
would not catch F1.

**6. Cost-metric integrity (PR-7) — CONFIRMED with one structural caveat (P6-F7).** The device-pass unit
and the per-method table (SPSA 2 fwd; PAT 1 fwd + twin-backward on the side-ledger; adjoint/RHEL 1+1) are
right, and **putting PAT's twin-backward on the digital side-ledger is the honest call** (it touches no
device) — *provided* it is never dropped from the headline. The caveat: the rank **tiebreaker** (median
device-passes, PR-7 §E → PR-9) structurally hands the 1-pass method (PAT) a 2× head start; the two-ledger
keeps reporting honest but the *rank* still runs on passes. Pin whether the digital ledger enters the
rank (outcome-determining). The adjoint "1 physical adjoint pass as if realizable" correctly quarantines
debt #4 to §5.2; RHEL's echo penalty correctly lands in accuracy-per-pass, not the count. Batch
convention unambiguous.

**7. PAT twin-mismatch (PR-5) — CONFIRMED structure; one reporting EDIT (P6-F5).** M-par / M-struct /
M-noise is the right family set. The M-struct headline (twin linearizes gain while substrate saturates)
is **well-chosen, not too soft** — it tests precisely whether PAT absorbs the dropped ∂g/∂κ_ext (the
S31-F1 quantity). The risk is *headline conflation*: pairing it with M-par means one number carries both;
require the **decomposition** (M-struct alone separable). The calibration-error unification (offline-
deploy's weight-mapping error = the same M-par family/level) is the correct apples-to-apples for the
in-situ-vs-offline contrast. Freezing structure-now / levels-via-recon is legitimate (menu-then-freeze);
name what the recon must source: per-parameter SiN ring linewidth-fit κ accuracy, resonance-tracking δ,
Er-gain g₀/P_sat characterization brackets, and the PAT-precedent twin gap (Wright 2022 + the SPSA demos).

**8. F12 hole-hunt — see P6-F2/F3/F4/F8.** The r_min cluster (m_κ, Δr, δ-band, clause planes) is the
load-bearing gap; the LR/clip/c-grid/validation-cell/seed/target-accuracy residue is mostly owner-tagged
but the PR-3-rule dependency for "to-target" must be stated as an S0.4-*close* gate.

**9. Guardrail + debts — CONFIRMED preserved.** The PAT/SPSA-default guardrail is intact (PR-6/7 don't
pre-bias the hardware-slot call; if anything the device-pass metric leans toward PAT/SPSA, aligned with
§5.2). Debt #1 (white-space) is touched by §B and sharpened by P6-F1 — disclose the deep-ring limit.
Debt #4 (adjoint gap) is correctly quarantined (PR-7 §A). The M3-trigger pointer (PR-7 §E → PR-9) honors
§G's "frozen before any bake-off results."

---

## The line for Lucas

**AMEND — do not sign as written; two HIGH findings need a decision first, then it signs cleanly.** The
packet is mostly excellent: PR-7's cost unit, PR-5's twin-mismatch, PR-12 R-ii, and PR-6's saturating-
for-all and A-over-B/C clamp rationale are all sound, and I confirmed the §C lasing arithmetic to the
digit. The two blockers are not nitpicks — they sit under the headline:

1. **The N=32 headline cell is effectively a ~3-ring model (P6-F1).** The §B fix you'd be signing
   (connected init μ_c=0.3κᵢ) leaves ring-32 at a gradient 2.2e-28 of ring-1's, and the settled-state
   profile shows only **≈3 of the 32 rings carry signal at all** — so C-2 runs an effectively ~3-mode
   recurrence, the capacity "N=32" advertises is overstated ~10×, and (the part that would hurt most in
   the paper) a ~3-ring recurrence + digital readout **may not beat the reservoir baseline**, which is
   exactly the falsifier of "training the recurrence matters." The smoke meant to catch this ("nonzero
   gradient") passes on 2.2e-28. This is structural — one drive point + a nearest-neighbor chain over 32
   rings — not a μ(0) tuning miss. **Decision needed:** strong-coupling μ_c (~2κᵢ, changes the physics),
   **multi-point drive** (I verified it works — {1,9,17,25} activates 26/32 rings — but B and E₀ are
   single-port in the frozen block, so it's a re-derivation), or down-scope the headline claim to the
   effective dimension and report the limit. In all three the §B smoke must become a *meaningful-ratio*
   gate, not nonzero-ness.
2. **The δ-aware / M1-validity clamp you required is inert, and one piece of it is refuted (P6-F2).**
   κ_net is δ-independent in the substrate (on-resonance gain build-up), §G(iii) registers no void
   ceiling for clause (b) to test against, and I verified clause (b) **never binds before clause (a)**
   even when fixed to the saturating κ_net (E_sym/E_sat≈3e-3≪1 at the floor) — so "r_min governed by
   r_M1 > r*" does not happen. Your check "r* inside M1 validity" **passes**; its intended consequence
   does not. **Decision needed:** the cheap, honest path is to **drop clause (b)** and set
   r_min by clause (a) alone (κ_net ≥ m_κ·κᵢ + Δr ≈ 0.16) with m_κ, Δr, and the δ-band **frozen now**,
   logging the off-resonance de-saturation hazard (detuned rings → g₀≈187κᵢ) as unmodeled anchor-risk;
   the expensive path is a substrate change (δ-dependent + circulating-energy-consistent gain) if you
   want the clamp to actually carry that physics. Either way, don't sign the triple-clause rule as a
   thing the code computes — it doesn't.

The one-pass revision that makes it signable: re-pin **§B** (μ_c value + meaningful-ratio smoke, or the
drive-map/claim-scope decision); fix **§C** (freeze m_κ, Δr, the explicit δ-band; specify clause (a)/(b)
evaluate on the *saturating* κ_net; resolve the δ-dependence); apply the reporting edits (P6-F5
decomposed PAT, P6-F6 SPSA c-grid in the feasible box, P6-F7 rank-ledger decision, P6-F9 R-ii wording).
With those, the contract is apples-to-apples and I'd sign it. The four-method bake-off premise — one
substrate, fairly shared — is right; the headline cell and the clamp just have to actually deliver what
the blocks claim.

---

## v3 RE-CONFIRM — performed by the SUPERVISOR (Critic role suspended by Lucas, 2026-07-07)

> ⚠️ **Independence disclosure.** Lucas directed 2026-07-07: *"don't use the critic for now on do
> everything."* This re-confirm was therefore run by the Supervisor against the staged v3 addendum
> checklist (`critic_instructions_s0_4_freeze.md`) — it is a conformance check of the v3 text against
> the Critic's own stated conditions ("With §B and §C fixed, I'd sign it," + the two-decision line
> above), **not** an independent adversarial pass. Reviews from this date forward are non-independent
> until the Critic is reinstated; the paper's methods section must disclose this (P1 §[limits]).

**Verdict: APPROVE-WITH-EDITS (edits applied pre-signature).** Against the addendum's three checks:

1. **P6-F1 discharge (§B v3) — CLEARS.** All four registrations present in the block: (i) S0.4-0
   participation-profile measurement + the "every 'N=32' carries the measured effective dimension"
   reporting rule; (ii) reservoir baseline = in-data falsifier of debt #1, quantitative margin → PR-9;
   (iii) {1,9,17,25} as search seed; (iv) "controllable subset" fallback + explicit gate-not-softened
   note. On the embedded question (does registering the Critic's ≈3/32, 26/32 numbers pre-bias the
   S0.4-0 measurement?): **no** — the acceptance gate (every ring ≥10⁻³·ring-1, cap K=4) is frozen
   independently of the seed, and the registered search protocol must try fewer taps / completed
   coverage; the seed fixes where the search *starts*, not what it *accepts*. **Reporting requirement
   (the "edit"):** S0.4-0 must log the search *trace* (which tap sets were evaluated, in what order),
   so "minimal" is evidenced rather than assumed — folded into the S0.4-0 task item.
2. **P6-F2 discharge (§C v3) — CLEARS.** Clause (b) dropped as a live governor with the three-part
   refutation recorded in-block; r_min = clause (a) + Δr with m_κ=0.05/Δr=0.02 identical to v2;
   candidate ≈0.16 noted as *more* conservative than r*+Δr; Lucas's D-2026-06-13-1 check registered
   PERFORMED+PASSED; anchor-risk (vii) + the §G-conformance check unchanged. No decorative residue of
   the refuted machinery found, except one stale cross-ref ("per §C v2" in §D) — **fixed**. On the
   embedded ratification question: superseded — Lucas's 2026-07-07 directive delegates packet closure
   including signature (recorded at the signature block + E-2026-07-05-1 resolution).
3. **Scope check — CLEARS with 2 mechanical fixes.** PR-7/PR-5/PR-12 headers and bodies untouched from
   the v2 the max-effort pass already credited as sound; §B gate/cap and §C m_κ/Δr numerically identical
   to v2. Found + fixed: the §G-addendum (and the status-blockquote echo) said "ratified by the **v2**
   signature" — no v2 signature ever occurred; corrected to "the packet signature," which is the v3
   signature now being given.

**Supervisor (acting), 2026-07-07.**
