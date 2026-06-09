# Decisions Needed

The **Executor** posts design questions here when something is unclear or requires a methodology
decision it wasn't given. The **Supervisor** answers (or escalates to Lucas via
`escalate_to_human.md`). Resolved items move to the bottom with the resolution + date.

---

## OPEN

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
