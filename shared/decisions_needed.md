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

### D-2026-06-08-1 (parked) — SiN operating $Q$ for the substrate (pre-registration)
**Raised by:** Supervisor (from the S0.0a recon). **Blocks:** nothing yet; **due at S0.2/S0.3.**
The salvaged platform registry ships SiN `Qi=2×10⁶` (LIGENTEC AN800, foundry-grade), but the proposal
cites `Q>10⁷` (class-leading, e.g. damascene SiN). Which do we pre-register as the operating point for
the S0.3 substrate (and the memory-length / gradient-survival story)? S0.0 adds both as registry entries
but does **not** choose. **To decide at S0.2/S0.3 pre-registration**, with the Critic's roadmap review
weighing in (checklist item 6). Likely: register a *range* (conservative foundry → aspirational) and
report sensitivity, rather than a single value.

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
