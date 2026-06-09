# Decisions Needed

The **Executor** posts design questions here when something is unclear or requires a methodology
decision it wasn't given. The **Supervisor** answers (or escalates to Lucas via
`escalate_to_human.md`). Resolved items move to the bottom with the resolution + date.

---

## OPEN

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
