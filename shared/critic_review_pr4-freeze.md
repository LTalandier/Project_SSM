# Critic review — PROPOSED PR-4 (substrate freeze, phase-boundary review)

**Reviewer:** Critic session · **Date:** 2026-06-12 · **Spec:** `shared/critic_instructions_pr4-freeze.md`
**Target:** the PROPOSED PR-4 block (`shared/preregistration.md` L527–690), against `docs/s0_3/substrate_recon.md`,
`docs/s0_3/pr4_input_sheet.md`, the arithmetic kernel + JSON, the E-2026-06-11-2 ruling, and the frozen
PR-2 v2 / PR-13 / PR-10 / PR-1.1 texts. All decisive arithmetic re-derived independently with the repo's
own `pole_region` functions (`/tmp` session script; values quoted below); the Cui 2023 anchor re-verified
via the Semantic Scholar API route this review's spec names, plus Unpaywall, plus two fresh fetch attempts.

---

## Verdict: **AMEND** — one revision pass, then sign

**Every registered *choice* survives attack.** M1 (+M2 one-off validation, +M3 pre-committed trigger),
the C-1/C-2/C-3 role split, NF-A headline, K4 with r ∈ [0.1, 3] and θ₀ = 0.3, K-pol-3 always-ON, H1,
and O2 @ P̄₀ = 1 mW are each the defensible option, faithfully applied from the Lucas ruling, and I could
not make either hostile reading stick against the *choices* (dispositions below). What fails is
**completeness of the numbers around the choices**: the block leaves the substrate's **operating gain
unregistered** (P4-F1) and the **saturation reference plane unregistered** (P4-F2) — together these mean
several of the block's own registered consequence numbers are evaluated at mutually inconsistent
operating points, and the Executor would have to *decide* (not evaluate) the single most
physics-significant substrate parameter at implementation time. That is precisely the hostile reading 2
("the freeze leaves tunable holes"), and it is real. Two C-2 anchor corrections (P4-F4, P4-F5) also
change registered text. None of this re-opens the ruling or any frozen entry.

**Why AMEND rather than APPROVE-WITH-EDITS:** the F1/F2 repairs require the Supervisor to make one
registered choice (the per-cell operating g_rt) and recompute the block's consequence table at it —
a section redraft under supersession discipline, not a wording patch I can supply as drop-in text alone.
The corrected numbers are supplied below so the revision is mechanical.

## Findings table

| # | Severity | One line |
|---|---|---|
| P4-F1 | **HIGH** | The per-cell operating gain g_rt is unregistered; the block's memory/packing/splitting numbers are computed at g = 0 while its ASE level (n_ss ≈ 23) assumes g = 0.9×intrinsic — the "named noise cell (Q/α, NF, **ASE level**)" ledger demand is unmet and the registered consequence table is internally inconsistent. |
| P4-F2 | **HIGH** | P̄ and P_sat reference planes unregistered; at P̄₀ = 1 mW the bus-referenced saturation depth is ≈ ×32 (CW-resonant intracavity ≈ ×260 at C-2/θ₀), so the "headroom closes ×6.5–12 / ×22–41" rows are small-signal statements that do **not** establish the 0.9×intrinsic operating point is reachable at the registered drive (bus-referenced, C-1 *fails*: need ≈ ×33, have ×6.5–12). |
| P4-F3 | MEDIUM | C-1 splitting ratio "≈ 1.9" does not reproduce: kernel and recon §3b both give **2.33** at θ₀ (C-2's ≈ 1.0 = 1.04 ✓); at the 0.9-gain point the pair becomes 5.3 / 2.4. Verdict ("split"; no knob-OFF cell) unchanged — strengthened. |
| P4-F4 | MEDIUM | The Cui geometry in the anchor-risk register is wrong: abstract-verified **perimeter 2.226 mm, effective radius 195 µm, 3-µm multimode waveguide** → FSR ≈ 64 GHz (recon's 65 ✓), not "19.8-GHz-FSR (0.21 mm²)". Corrected, the transfer risk *shrinks* on ring size (registry equivalent bend radius ≈ 228 µm is gentler than Cui's 195 µm) and re-aims at the real residual: the loss was demonstrated *by* the wide-multimode Euler-bend design the registry ring doesn't have. |
| P4-F5 | MEDIUM | "Body remains paywalled / four routes failed / deeper verification infeasible at proportionate cost" is superseded: the paper is **Gold OA, CC-BY** (Semantic Scholar `openAccessPdf` + Unpaywall, both verified this review; the OA link was in the same API response the abstract came from). Programmatic fetches are bot-walled (re-confirmed ×2 today), but one human browser click retrieves it — resolve residual risk (i) **before signature**. |
| P4-F6 | MEDIUM | O2's "frozen formula — no free parameter" is not actually written anywhere, and its value depends on unpinned inputs (CW-equivalent vs at-clock-PSD reading, pulse shape, B-injection convention, μ(0)=0, N, δ-config) plus an unstated encoder-scale **cadence** under trainable κ_ext. As drafted, the two-step would launder Executor choices through a "mechanical evaluation". |
| P4-F7 | MEDIUM | Anchor-risk register omissions: (v) the Er-gain coefficient transfer (flagship straight implanted waveguide → undoped foundry ring; R§4f's own Stage-1 integration flag) and (vi) the P_sat ring-scaling assumption; plus the γ = 11.8 MHz damascene-class assignment at C-2 needs its lineage basis stated (no AN800-specific γ exists). |
| P4-F8 | LOW | The R2 N-pinning lacks its clock qualifier: in-band counts are 2 GS/s figures. At 1 GS/s: C-1 ≈ 6.5 (< 8!), C-2 ≈ 22 (< 32), C-3 ≈ 97 (< 128). Gate ii's clock must be stated (2 GS/s), and 1-GS/s cells (incl. PR-13's) need a stated N or an out-of-band-poles caveat; also state assignment-vs-sweep semantics for {8, 32, 128}. |
| P4-F9 | LOW | M2 validation runs only at C-2/θ₀; Gate ii gates at C-1 — add a C-1 episode (trivial cost) or register the corner-independence argument for the ≤ 3 % relaxation bound. |
| P4-F10 | LOW | The S0.1 §4 F8 carry-ins (thermal self-heating at operating power; pole-placement precision) and the drift-knob *magnitudes* are unowned in the block — name the freeze point (PR-6 / PR-5–9) or the explicit deferral. |
| P4-F11 | LOW | The ledger row's "loss↔Q registry check" demand: cite the existing test-enforced `loss_q_consistency_error()` as the registered check (one clause). |
| P4-F12 | LOW | P_pk = 2·P̄₀ presumes the unipolar affine map {0..3} — make the encoder convention explicit; and PR-13's fifth level (marker, +5 on the {−3..3} scale → 4 unipolar) gives P_pk ≈ 2.7·P̄₀ at mean ≈ 1.5 — scope the peak bound per task family or restate it. |

---

## The two hostile readings, adjudicated

**Reading 1 — "the cell was chosen to flatter the photonic side": does not stick, with three caveats.**
The direction of fit runs the other way: N = 32 (headline) was frozen at PR-10/PR-2 — anchored to the
50-node Vinckier RC, before any substrate cell existed — and C-1 *cannot* host it (12.9 in-band poles
< 32 at θ₀, my re-derivation). The options were: break a frozen grid, or register a demonstrated-MPW
cell that hosts it and keep the gate on the foundry floor. The block did the second and kept Gate ii at
C-1 — the conservative cell gates; the better platform only carries the headline figure, labelled. θ₀ =
0.3 is not a knife-edge pick: the C-2 co-satisfaction band is wide (N = 32 packs for r ≤ 0.6; the 7-tap
span is covered for r ≤ 1.0; drop efficiency is non-degenerate from r ≈ 0.3), and 0.3 is an existing B3
ladder rung — design-from-frozen-constraints, made before any results exist. The caveats that *feed*
reading 1 and must be repaired: the favorable γ class at the headline cell needs its stated basis
(P4-F7), the geometry-transfer text must be corrected (P4-F4 — note the correction *helps*), and the
operating-gain hole (P4-F1) must close, because an unregistered gain knob at the headline cell is the
one genuinely flattering degree of freedom left in the draft.

**Reading 2 — "the freeze leaves tunable holes": sticks, on two parameters.** The operating gain
(P4-F1) and the saturation plane/solve (P4-F2), plus the smaller F6/F8/F12 items. The fix list is short
and mechanical; everything else I checked is genuinely pinned (the block even pre-registers its own unit
tests: B1-consistency, A1↔A2 equivalence, E₀ normalization at both bound edges — good practice).

---

## Checklist dispositions (spec items 1–12)

**1. Fork-application fidelity — CONFIRMED.** G-section vs the recorded ruling ¶1–3: verbatim-faithful;
nothing dropped or weakened. Additions are strengthenings: G(iii) quasi-static margin (from the
recommendation's own evidence), the M2 cell pin, the A1 equivalence unit test. **The M3 trigger is
genuinely pre-committable as registered**: the *commitment* (build iff in-margin, or iff Stage-2 tilts
III-V) is frozen now; only the margin's quantitative form is deferred — to PR-5–9/PR-11, which freeze
**before any bake-off results exist**. That is the correct freeze point, not a hole (the margin form
depends on the gated-statistic definitions that are PR-5–9's content). Riders: R1 compliant everywhere
I checked, including the C-3 change from the input sheet's NF-B to NF-A (a deliberate, correct R1
application — worth one "changed from the input sheet per R1" note for the audit trail); R2 compliant
(in-block, with the F8 clock qualifier owed); R3 compliant (G(ii) + the O2 cross-reference — one
assumption stated once, binding both, exactly as the rider demanded).

**2. M1 validity conditions vs the recon physics — EDIT (P4-F2).** Conditions (i)–(iii) are sound and
the Bononi–Rusch caveat is correctly scoped (energy criterion, not just the low-pass argument; bursty
voids; the frozen families are i.i.d. by construction). The SPSA question resolves cleanly **iff** P̄ is
the power at the gain element: the ± perturbations of {δ, κ_ext, μ} don't change the bus drive, but a
κ_ext perturbation changes the intracavity power the gain medium sees; M1's per-episode operating-point
form handles this automatically (each SPSA pass is an episode; the ≥ ms inter-pass cadence is exactly
where the recon says gain follows adiabatically) — but only under the intracavity reading of P̄. The
block never says which plane P̄ (or P_sat) lives at. Register the plane (P4-F2 text below).

**3. Arithmetic re-derivation — CONFIRMED except one number (P4-F3) and one coherence failure (P4-F1).**
Reproduced exactly with the repo's own functions: packing at θ₀ 12.9 (C-1) / 43.9 (C-2) in 2 GHz ✓;
memory at θ₀ 4.11 / 13.99 samples @ 2 GS/s ✓; C-2 splitting 1.04 ✓; r = 10 exclusion (0.31 < 0.5
samples) ✓; drop-efficiency span 0.028 → 0.735 ✓; gain headroom ×6.5–12.3 (C-1) and ×21.7–41.2 (C-2)
vs the 0.9×intrinsic target ✓, P-CORN ×0.67–1.27 vs full intrinsic ✓; n_ss = 9·n_sp = 22.5 ≈ 23,
corner-independent ✓ (and ≈ 9 at NF 3 ✓); P_pk = 2·P̄₀ under the unipolar {0..3} map ✓ (P4-F12);
E_sym/E_sat = 4.65×10⁻⁶ / 9.31×10⁻⁶ / 9.31×10⁻⁵ at 2/1/0.1 GS/s ✓. **REFUTED: C-1 splitting "≈ 1.9"**
— the kernel, the recon §3b table, and my independent evaluation all give **2.327** at (γ = 90 MHz,
r = 0.3). No convention I could construct yields 1.9 (the FWHM-band value is 1.16; 1.9 looks like
2γ/κᵢ with the loading dropped). Same-direction verdict, wrong registered number. **The coherence
failure:** every number above is a g = 0 evaluation, while n_ss ≈ 23 (quoted in G and O2) is a
g = 0.9×intrinsic evaluation — see P4-F1.

**4. The two-cell role split — CONFIRMED sound; Cui verified; two anchor corrections (P4-F4/F5).**
"One substrate model, two registered parameter points" does not violate the one-substrate standard: the
four estimators all run the *same* model at the *same* cell for any given comparison (the bake-off
headline = C-2 for all four; Gate ii = C-1 for all methods) — apples-to-apples is per-comparison, and
no comparison mixes cells. The ledger rule "foundry-grade gates Gate ii" is honored, not dodged: the
gate stays on the foundry floor; C-2 carries only the labelled headline. Direction-of-fit defense per
reading 1 above — recommend adding it to the block in one sentence. **Cui verification (the spec's
named check): done via the Semantic Scholar API.** The abstract is verbatim-exact as quoted in the
block, including *"The MRR is fabricated by the standard multi project wafer (MPW) foundry process"*
and *"based on the widely used MPW process, a propagation loss of only 3.3 dB/m and a mean intrinsic Q
of around 10.8 million are achieved for the first time"* — the "standard-MPW-foundry process" phrase is
abstract-supported, [EV]-class. The conservative-bound construction is sound and survives even if the
body sentence is never retrieved: registered 5.1 dB/m / 6.8×10⁶ is strictly worse than the
abstract-verified 3.3 dB/m / 10.8×10⁶ on both axes. But the register's geometry text is wrong (P4-F4)
and the paywall/infeasibility sentence is superseded (P4-F5) — fixes below.

**5. K4 necessity + parameters — CONFIRMED.** PR-2 v2's frozen partition text reads "P2, gain-free
minimal B1 = {δ_j (heaters), **κ_ext,j (tunable couplers)**, μ_jk}" — κ_ext,j is in the trainable set;
a fixed-κ_ext substrate would contradict a frozen entry. K4 is forced, as claimed. Bounds [0.1, 3]:
the r = 10 exclusion reproduces (memory 0.31 samples < 0.5 @ C-1/2 GS/s; and r = 10 would put the B3
ladder at its SNR-degenerate end); the low edge 0.1 keeps the most-split, lowest-drop rung in range —
non-degenerate span confirmed. θ₀ = 0.3: legitimate design-from-frozen-constraints (wide feasible band,
existing ladder rung, chosen before any results; see reading 1). F6 "one value": exactly one r₀ = 0.3
registered, matching PR-2 v2's "common θ₀ ≡ the PR-4 policy value" — satisfied.

**6. The O2 two-step — EDIT (P4-F6).** The two-step *mechanism* is pre-registration-clean (numeric
addended before any consuming run, frozen there) — **provided the formula is actually frozen now**, and
it is not: no closed form appears in the block, the input sheet, or the recon. "Parameter-free" is
overclaimed as drafted — the steady-state Σⱼ⟨|aⱼ|²⟩ under "a stationary P̄₀ drive" depends on: the
stationarity reading (CW-equivalent vs the registered clock's modulated PSD — these differ by ~×30 in
intracavity build-up at C-2/θ₀), the pulse shape, the B-injection convention, μ(0) = 0, N, and the
δ-configuration beyond ring 1. Each unpinned input is an Executor decision. Also unstated: the
encoder-scale **cadence** under trainable κ_ext. Recommended completion (Supervisor drafts): write the
closed form into the block with inputs pinned to {CW-equivalent stationary reading at P̄₀, δ ≡ 0,
μ = μ(0) = 0, the PR-6 B-init convention, the cell's registered N}, and register: *"the encoder scale is
derived once per arm at the registered θ₀ and frozen for the run; trained κ_ext excursions thereafter
change intracavity energy as physics, not as renormalization"* (the only reading under which "the
encoder cannot buy SNR" and "the task input is fixed" are simultaneously true). P_sat's "scaled to the
ring per the registered geometry" needs its formula for the same reason (folded into P4-F2).

**7. K-pol-3 always-ON — CONFIRMED.** The incoherence argument is valid: under K4, per-ring trained
κ_ext moves through any (γ, r) validity boundary mid-run, so K-pol-1/2's conditional OFF would switch
model structure mid-training — incoherent. γ assignments are honest *as labelled* (process-class
assumptions, stated as such; the [EV]/[AV] markers are correct per the recon), with one repair: the
damascene-clean assignment at C-2 is the favorable class at the headline cell, so its basis must be
stated (if the LIGENTEC-AN damascene lineage is the basis, write that sentence; otherwise justify or
reassign) — P4-F7. The registered claim condition checks out against my arithmetic and *strengthens*
under both repairs: at θ₀, C-1 = 2.33 (not 1.9), C-2 = 1.04, C-3 = 4.58 — and at the 0.9-gain operating
point 5.3 / 2.4 / 10.5 — no registered cell supports a knob-OFF single-pole claim at θ₀, passive or
compensated.

**8. Rider compliance — R1 COMPLIANT (no leaks found; C-3's NF-B→NF-A change is the rider working);
R2 COMPLIANT in-block with the F8 clock qualifier owed; R3 COMPLIANT** (registered as M1 validity
condition G(ii), cross-referenced from O2 — not a line item). The {8@C-1, 32@C-2, 128@C-3-labelled}
pinning is consistent with frozen PR-2's {8, 32, 128}-headline-32, at 2 GS/s (P4-F8 for the qualifier).

**9. H1 — CONFIRMED.** Registering the conservative corner for the substrate's standalone numbers, with
H2 as a labelled sensitivity row and H3 named as the Stage-1 path, matches the EV-F1 carry-in exactly;
the envelope continues to report both corners by its own convention, so no downstream claim quietly
inherits H2. I found no H2 leak.

**10. Anchor-risk register — EDIT (P4-F4/F5/F7).** The construction (provenance trail + conservative
bound + M2 validation + named residuals + registered infeasibility) is the right shape and is a correct
first application of the PR-1.1 rule's GA-F6 physics scope. Three repairs: the geometry correction
(P4-F4 — naming *is* enough once the named thing is correct, because the corrected risk is
narrower and one cheap sensitivity row prices it: register a **C-2-derate row at ×2 the registered loss
(Qᵢ ≈ 3.4×10⁶)**, cost ≈ 0 in simulation, and the hostile reading dies); the OA-fetch execution
(P4-F5 — the infeasibility sentence is false as registered; the fetch is one click and should happen
before signature, with either outcome acceptable); and the two un-named risks (P4-F7: the Er-gain
process/geometry transfer the recon itself flags at R§4f, and the P_sat scaling).

**11. Cross-consistency sweep — CONFIRMED except as already filed.** PR-2 v2: partition ✓ (verbatim),
N-grid ✓, F6 one-value ✓, F12 same-SNR ↔ R3 ✓ (G(ii) cites it). PR-13 vs memory at θ₀ @ 1 GS/s
(the spec's question — passive-loaded): **C-1: k = 1 in-memory, k = 3 ×1.5 over, k ≥ 10 out; C-2: k ≤ 3
in, k = 10 marginal (×1.43 over); C-3: k ≤ 30 in, k = 100 the cliff** — and all of these shift ×2.3 at
the 0.9-gain point (P4-F1 again: the PR-13 cliff *hypothesis* is uninterpretable until g is registered).
PR-10: clocks/N/2–4-ch bracket consistent; 0.1/1 GS/s spot-checks are where the F8 qualifiers come from.
PR-11 carry-in ✓ (fresh draws; forward/echo streams independent — in the G ASE bullet). PR-1.1 rule ✓
(correctly applied, GA-F6 scope; the infeasibility-registration *mechanism* used exactly as designed —
the content just turned out wrong, P4-F5). S0.1 conventions ✓ (header inheritance; κᵢ = ω₀/2Qᵢ;
symmetric add-drop; HWHM; my re-derivations used the repo functions and matched). α↔Q check: exists and
is test-enforced — cite it (P4-F11).

**12. F12 completeness — the Executor-decides list (each already filed):** operating g_rt per cell
(P4-F1); P̄/P_sat reference plane + saturated solve (P4-F2); E₀ formula inputs + encoder-scale cadence
(P4-F6); N-assignment semantics + per-clock N for 1-GS/s cells + Gate ii's clock (P4-F8); drift
magnitudes + self-heating owner (P4-F10); encoder map + PR-13 peak bound (P4-F12). Nothing else found:
the ASE integrator choice is pinned behaviorally by the registered A1↔A2 equivalence test; the M2 bound,
γ menu, bounds tests, and sensitivity axes are genuinely registered.

---

## Replacement / addition texts

**E1 (P4-F1) — add to G after the gain-ceiling bullet, and recompute the C/S consequence numbers at the
registered point** (recommended registration; the at-gain numbers below are my re-derivations, kernel
conventions):
> **Operating point (registered):** every gain-bearing cell runs at **g_rt = 0.9 × intrinsic per-rt
> loss** (the ceiling value — the S0.1 deep-compensation convention; the same point the registered
> ASE level n_ss ≈ 23 is computed at), giving κ_net = 0.1·κᵢ + 2κ_ext; **g = 0 (passive floor) and
> g = 0.5× are labelled sensitivity rows**; P-CORN is passive-only per G. All in-block consequence
> numbers are quoted at the registered operating point, with the passive floor in parentheses:
> memory at θ₀ @ 2 GS/s — C-1 **9.4** (4.1), C-2 **32.0** (14.0); in-band packing at θ₀ in 2 GHz —
> C-1 **29.5** (12.9), C-2 **100** (43.9); splitting 2γ/κ_net at θ₀ — C-1 **5.3** (2.33), C-2 **2.4**
> (1.04). Gate ii and the bake-off headline run at the registered operating point.

If the Supervisor instead intends a different g_rt (or passive headline cells), that is equally
freezable — but then the ASE level must be recomputed (passive ⇒ no ASE ⇒ no noise cell, which
contradicts the ledger row), and the C-1 "honestly-marginal" sentence must be reconciled either way:
at 0.9×, C-1's memory (9.4) *covers* the 7-tap span — the marginal framing is true only at the passive
floor, and the block currently asserts both.

**E2 (P4-F2) — add to the G Form bullet:**
> P̄ and P_sat are referenced at the **same plane — the field the gain medium sees** (intracavity):
> P_sat,ring is the flagship's measured input saturation mapped through the registered geometry by the
> formula registered here: I_sat = P_sat,wg/A_eff (A_eff = 1.2 µm² [EV]), applied to the ring's
> circulating intensity P_circ = Σⱼ|aⱼ|²·ħω₀/τ_rt. **Reachability:** the saturated operating-point
> solve at the registered drive (O2, P̄₀ = 1 mW) is computed at S0.3-1 calibration alongside E₀ and
> reported to the ledger with the achieved g_rt vs the ceiling; the ×6.5–12 / ×22–41 headroom rows are
> **small-signal material-plausibility statements, not operating-point claims** (at P̄₀ = 1 mW the
> bus-referenced saturation depth alone is ≈ ×32).

**E3 (P4-F3) — in S, replace** "at θ₀: C-1 2γ/κ_tot ≈ 1.9 (split), C-2 ≈ 1.0 (doublet-class)" **with**
"at θ₀: C-1 2γ/κ_tot ≈ 2.33 (split), C-2 ≈ 1.04 (doublet-class) at the passive floor — ≈ 5.3 / 2.4 at
the registered operating gain".

**E4 (P4-F4) — replace the geometry-transfer risk sentence with:**
> (ii) **geometry transfer** — Cui's demonstration is a racetrack of perimeter 2.226 mm (effective
> radius 195 µm, 3-µm-wide multimode waveguide, modified Euler bends; FSR ≈ 64 GHz)
> [abstract-verified]; applying its loss class to the 100-GHz-FSR registry ring (L ≈ 1.43–1.54 mm)
> assumes the loss class survives the **single-mode, narrower-waveguide geometry** — the demonstrated
> number is achieved *by* the wide-multimode Euler-bend design, so the residual risk is mode/width
> geometry, not ring size (the registry ring's equivalent bend radius ≈ 228 µm is no tighter than
> Cui's 195 µm). Priced by the registered **C-2-derate sensitivity row: ×2 registered loss
> (Qᵢ ≈ 3.4×10⁶)**.

**E5 (P4-F5) — replace the four-routes sentence with:**
> The article is **Gold OA (CC-BY)**: the Semantic Scholar record and Unpaywall both carry the
> publisher-PDF link (verified 2026-06-12, Critic). Programmatic fetches are bot-walled (six attempts
> across two sessions: SPIE ×2 slugs, ADS, researching.cn, direct OA-PDF curl, rendered fetch), but a
> human browser fetch is one click. **Pre-signature action (Lucas or Executor, headed browser):**
> download the OA PDF and grep for the 0.051 dB/cm / 6.8×10⁶ sentence — found ⇒ P-AN800 flips
> [AV]→[EV] and residual risk (i) closes; not found ⇒ the registered pair stands on the
> conservative-bound construction alone (strictly worse than the abstract-verified 3.3 dB/m / 10.8 M
> on both axes). Either outcome is freeze-compatible; what is *not* is registering retrieval
> infeasibility for a CC-BY document.

**E6 (P4-F6) — in O2:** write the E₀ closed form into the block with its inputs pinned (stationarity
reading, pulse shape, B convention, μ(0) = 0, N, δ ≡ 0), and add: "the encoder scale is derived **once
per arm at the registered θ₀** and frozen for the run; trained κ_ext excursions thereafter change
intracavity energy as physics, not as renormalization."

**E7 (P4-F7) — append to the anchor-risk register:**
> (v) the Er-gain budget applies the flagship's straight-implanted-waveguide coefficient
> (1.0–1.9 dB/cm [EV]) to an undoped foundry ring on a different process — a Stage-1 integration
> assumption (R§4f), carried as a label on every gain-bearing cell; (vi) P_sat's ring scaling (formula
> in G) is an anchor-transfer assumption validated only at Stage 1. — And in C-2: state the basis for
> the damascene-class γ (LIGENTEC-AN process lineage, if that is the basis) or reassign/justify.

**E8–E12 (LOW):** add the clock qualifier + assignment-vs-sweep sentence to the R2 paragraph (text in
finding P4-F8), including "Gate ii runs at 2 GS/s" explicitly; add the C-1 episode to the M2 validation
(or the corner-independence sentence); add the F8-carry-in owner line (self-heating + pole-placement
precision + drift magnitudes → PR-6/PR-5–9, named); cite `loss_q_consistency_error()` as the registered
α↔Q check; make the unipolar {0..3} encoder map explicit and scope the P_pk bound per task family
(PR-13's marker level reaches ≈ 2.7·P̄₀).

---

## The line for Lucas

**AMEND — do not sign this draft; sign the revision.** Every registered choice (M1 + M2 validation +
M3 trigger · C-1/C-2/C-3 roles · NF-A · K4, r ∈ [0.1, 3], θ₀ = 0.3 · K-pol-3 · H1 · O2 @ 1 mW) survives
adversarial review and none needs reopening — the ruling was applied faithfully and the two-cell split
is sound, not flattering. The revision must: (1) register the per-cell operating gain and recompute the
block's consequence numbers at it [P4-F1]; (2) register the P̄/P_sat reference plane + the saturated
reachability solve, demoting the headroom rows to small-signal statements [P4-F2]; (3) fix the C-1
splitting number (2.33, not 1.9) [P4-F3]; (4) correct the Cui geometry and execute the one-click OA
fetch before signature [P4-F4/F5]; (5) write the E₀ formula and the encoder-scale cadence into O2
[P4-F6]; (6) apply the register additions and LOW edits [P4-F7..F12]. With those applied, this becomes
a freeze I could not attack.
