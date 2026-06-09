# Critic Review — S0.1 Results (mapping + pole region + scope-B)

**Reviewer:** Critic (independent session; reports to **Lucas**, not the Supervisor)
**Date:** 2026-06-09
**Spec:** `shared/critic_instructions_s0-1-results.md` · **Gates:** this review gates **S0.2**.
**Reviewed:** `results_log.md` (S0.1 entry) · proposal §3/§4/§5 · `stage0_roadmap.md` v3 §S0.1 + F19 ·
`preregistration.md` (PR-2, PR-4) · `docs/s0_1/{mapping_notes, B1_actuation_map, B2_backscatter_bound,
B3_kappa_ext_tradeoff}.md` · code `photonic_ssm/dynamics/{single_ring,coupled_rings,pole_region}.py`,
`platforms.py` · tests `test_{single_ring_cmt,coupled_rings,pole_region}.py` ·
`decisions_needed.md` (D-2026-06-08-2, -3). **Method:** independent re-derivation of every load-bearing
number (registry reconciliation, memory bounds, B2 crossover table, B3 trade) in a fresh script;
full read of the new dynamical core + its gate tests.

---

## Overall verdict: **APPROVE-WITH-EDITS**

The S0.1 gate is **genuinely passed for what it tests**, the new dynamical core is correctly implemented,
the two architecture constraints are **genuinely honored in the new model** (not inherited — the
checkpoint==plain bit-identical-gradient test and the 49-step gradient-flow test are real and strong),
the F13.1 registry fix is **exactly right** and resolves the inconsistency I raised last review, and the
B3 bound is correct. Most of the headline numbers reproduce to the digit under independent
re-derivation. The Executor's honest flags (B2 verify-before-cite; the diagonal-vs-LinOSS subtlety; the
κ_ext↔readout coupling) are exactly the right things to have surfaced.

I am withholding unqualified APPROVE for six tightening items that bite **before these numbers harden into
PR-1/PR-2/PR-4 or the paper** — none of which is a defect in the code, all of which are
validation/framing/arithmetic gaps:

1. **The gate validates the *steady-state* limit and pole *algebra*, but never the *transient* dynamics
   against an independent reference** (S0.1-F1, HIGH). For a result whose entire contribution is the
   *dynamical* mapping, that is a real gap — cheap to close, should close before S0.2 builds the substrate
   on this forward model.
2. **The mapping-fork recommendation conflates two SSM classes** (S0.1-F2, HIGH). The ring bank natively
   realizes a **diagonal complex-pole SSM (S4D/DSS class)**; LinOSS is the *conjugate-pair special case*,
   recovered **only** under real I/O and **only** when the inter-ring coupling μ is off. "It *is*
   diagonalized LinOSS" is half-true and the benchmark-transfer it assumes is literally open debt #2.
3. **A 2× units slip in the headline memory figure** (S0.1-F3, MEDIUM): "329 round trips" pairs with
   **3.29 ns** (amplitude/state memory), not the quoted **1.65 ns** (photon/energy lifetime). PR-2 sizes
   the task against this — pick the amplitude convention.
4. **B2's high-roughness row is internally inconsistent** (S0.1-F4, MEDIUM): Q_cross=3.0×10⁵ implies
   2γ/κ_i=6.6 at foundry, not the tabulated 5.2 (and 99 not 77 at 3×10⁷). Plus the splitting **criterion
   carries a ~2× convention band** that must be stated. Qualitative finding is robust to both (verified).
5. **B1's "gain-free minimal set suffices" has a wrinkle** (S0.1-F6, MEDIUM): in the gain-free device the
   only damping actuator (κ_ext) is *also* the readout-residue knob, so recurrence and readout are not
   physically independent there — the white-space claim survives, but the reservoir-baseline contrast does
   not cleanly, and PR-2 must resolve it.
6. **The conservative corner is mislabeled as a real foundry process** (S0.1-F7, MEDIUM): registering
   Qi=2×10⁶ / 0.172 dB/cm under the name `SiN_LIGENTEC_AN800` is fine for gating but must **not** be cited
   as "AN800's parameters" — the real AN800 is *better* (≈0.05 dB/cm, Qi≈6.8×10⁶).

**On the two decisions:** I **agree with D-08-3** (optional roughness-gated splitting knob + PR-4
sub-parameter) with three strengthenings, and I **agree with the substance of D-08-2** (simulate the
complex-diagonal layer) **but reject its framing** — see the explicit adjudications at the end.

**Severity count:** 2 HIGH · 7 MEDIUM · 1 LOW.

### Fix-by schedule

| Deadline | Findings |
|---|---|
| **Before S0.2 science / PR-1/PR-2 freeze** | S0.1-F1 (transient gate test), S0.1-F2 (mapping-class framing → PR-1 benchmark + debt #2 scope), S0.1-F3 (memory convention → PR-2 sizing), S0.1-F6 (κ_ext↔readout → PR-2 partition) |
| **Before S0.3 / PR-4 freeze** | D-08-3 strengthenings (evaluate splitting at operating κ_ext, not just undercoupled), S0.1-F7 (registry labeling if PR-4 cites it) |
| **Before the Stage-0 paper** | S0.1-F4 (B2 arithmetic + criterion band), S0.1-F5 (B2 primary-source verification — already self-flagged), S0.1-F7 (labeling), S0.1-F8 (thermal self-heating + pole-region realizability completeness), S0.1-F9 (low) |

---

## 1. Gate integrity

**Answer: the gate is genuinely passed *for what it tests* — but what it tests is the CW/steady-state
limit plus pole *algebra*, not the *transient* dynamics. The dynamical claim is under-validated (S0.1-F1).**

I re-derived the pre-registered gate numbers and read every gate test. The CW-limit recovery is real and
well-designed: `test_cw_limit_convergence_is_order_one_over_finesse` checks the error *scales* O(1/F)
across two finesse points (not just a single coincidental match) — exactly the right test to prove the
CMT model *is* the high-finesse limit of the exact ring rather than agreeing at one point. Energy
conservation (|t|²+|t_d|²−1 < 1e-12), critical-coupling extinction, lossless all-pass |t|=1, and the
pole↔eigenvalue identity all pass cleanly. Tolerances (CW <1% at F≥1000; the SiN rings sit at F≈1034 →
15511, which I confirmed) are adequate and honestly pre-registered.

### S0.1-F1 (HIGH) — No independent validation of the *transient* time-domain response; add a ringdown/step test before S0.2 builds on this model
Every single-ring test is **steady-state** (`cw_through`/`cw_drop`, energy conservation, pole-movement
under gain). Every coupled-ring "pole" test is **algebra**:
- `test_uncoupled_poles_equal_diagonal` — eigenvalues of a diagonal matrix equal its diagonal. Nearly
  tautological; tests `_build_M` + `eigvals` compose, not dynamics.
- `test_discrete_pole_magnitude` — |eigvals(expm(M·dt))| = exp(−κ·dt). Tautological for diagonal M.
- `test_zoh_is_exact_for_constant_input` — checks the single-ring (δ=0) **fixed point** Γ/(1−Φ) = −M⁻¹B.
  A genuine check, but **steady-state**, single-ring, real-M only.

There is **no test that integrates the ODE forward in time and compares the transient trajectory against
an independent reference** — no cavity ringdown `a(t)=a₀e^{(iδ−κ)t}`, no step-response rise, no
coupled-ring supermode *beating* (the one genuinely dynamical signature of μ≠0). The ZOH being "exact for
PWC input" and the discrete poles being "exp(λdt) to machine precision" are **exact by construction**
(van Loan) — they verify the *implementation is bug-free*, not that the model *matches the physics it
claims*. A fixed-point match pins −M⁻¹B but exercises the decay/oscillation *rate* only through the
structurally-asserted Φ=expm(M·dt).

The model is very likely correct (van Loan is standard; the steady-state, pole-algebra, and
gradient-flow tests are mutually consistent with a correct implementation). So this is **validation debt,
not a suspected bug.** But S0.1's contribution *is* the dynamical recurrence, and the paper's central
claim is that rings realize it — that deserves a positive time-domain check, not exactness-by-construction.
**Recommendation (hours):** add (i) single-ring ringdown + step response vs the closed-form CMT solution
**and** vs an independent integrator (`scipy`/`torchdiffeq` RK45 on `da/dt=Ma+Bu`), asserting both the
decay rate κ and oscillation frequency δ in the *time domain*; (ii) a 2-ring μ≠0 case showing the
hybridized **beat frequency** matches Im(eig(M)) splitting. Close before S0.3 builds the substrate forward
model on this core.

---

## 2. Architecture-constraint reality

**Answer: genuinely honored in the new model, with strong tests. No path found where state gradients are
silently dropped.**

I read the rollout and its tests. (3a): `_rollout` is a plain autograd recurrence — no
`no_grad`/`detach`/`.data` (and `test_3a_no_detach_in_rollout_source` greps the *source* of both rollout
methods to guard the salvaged forward-only anti-pattern from leaking back in — a good defensive test).
`test_3a_gradient_flows...` drives a 50-step rollout, takes a loss on **x_T only**, and asserts the
gradient reaches the **t=0 input** (49 steps back) finite and >0, and into every recurrent parameter.
(3b): `forward` returns the full `x_0..x_T` trajectory (verified shape + that x_0 is the zero initial
state). The checkpointed chunked rollout is **bit-identical to the plain rollout in outputs, states, AND
every gradient (==0.0 difference)** — this is the strongest possible form of the F18 gate and it genuinely
demonstrates the `TrainingAwareDynamicSOAPerMode` memory pattern preserves exactness. The adjoint/RHEL
estimators (S0.4b/c) will need exactly this trajectory exposure and gradient flow; both are in place.

One forward-looking note (not a defect): the checkpoint test uses T=40, chunk=7. At the bake-off's real
sequence lengths (hundreds–thousands of round trips, per the memory bound) the checkpoint **value/grad**
equivalence should re-pass at large T (it will mathematically; just confirm numerically once the task
length is set at PR-2, since float128 isn't in play and long products of Φ can lose precision). Minor.

---

## 3. The mapping fork (D-2026-06-08-2)

**Answer: agree with simulating the complex-diagonal layer; the "it *is* diagonalized LinOSS/D-LinOSS"
framing is half-true and must be tightened, because PR-1's benchmark and verification debt #2 ride on it.**
Full adjudication is below under *Decision recommendations*; the finding it generates:

### S0.1-F2 (HIGH) — Pin the SSM *class* the bake-off simulates; LinOSS-equivalence holds only under real I/O *and* μ=0; benchmark transfer is open debt #2, not a given
The Supervisor's rationale asserts "(2) the complex-diagonal form **is** the standard diagonalized
realization of LinOSS/D-LinOSS." This conflates two different SSM classes:

- **What rings natively are:** the intracavity field `a∈ℂ^N` evolves under a **complex** M with **N
  complex poles** that are *not* conjugate pairs (M is complex; without backscatter there is no λ* mode).
  This is the **diagonal complex-pole SSM = S4D/DSS class** (proposal §1.1's `H(s)=Σ c_jb_j/(s−λ_j)+D`),
  which the code realizes directly. Standard **LinOSS** is a system of *real* 2nd-order oscillators =
  conjugate-pair-structured = a **special case** of the diagonal complex class.
- **When they coincide:** an **uncoupled** ring (μ=0) with **real I/O** (real drive + coherent-quadrature
  or otherwise real-linear readout) real-ifies to a 2×2 block `[[−κ,−δ],[δ,−κ]]` with eigenvalues
  {−κ±iδ} — *exactly* a real damped oscillator with independently tunable damping κ and frequency δ. So
  **uncoupled + real-I/O ring bank ≡ diagonal LinOSS.** Here the Supervisor's framing is fully defensible.
- **Where it breaks (two ways the recommendation glosses):**
  1. **Inter-ring coupling μ is *beyond* standard LinOSS.** Published LinOSS/D-LinOSS use a **diagonal**
     state matrix (oscillators independent; mixing only in B/C). The trainable off-diagonal `iΩ` makes the
     *recurrence* non-diagonal — a *generalization* ("coupled oscillatory SSM"). This is a feature for the
     white-space claim (which *wants* "inter-ring couplings" trained), but it means **the published
     LinOSS benchmark numbers do not validate the coupled model**, and the Supervisor's "the
     oscillatory-SSM benchmark results transfer" is **assertion, not result — it is exactly open
     verification debt #2.**
  2. **Real I/O is a *modelling choice with consequences*, not free.** The equivalence needs a real-linear
     readout. Optical detection is either **coherent-quadrature** (linear, real → recovers LinOSS) or
     **intensity |·|²** (a *nonlinearity*, not a linear readout — which may be the *desired* inter-layer
     activation, but then the layer is not a clean linear SSM). "Handle real I/O at the readout"
     (Supervisor's caveat) must specify *which* optical readout, because the choice determines whether the
     LinOSS-equivalence holds at all and feeds the S0.7 precision–accuracy link.

**The white-space claim survives the reframing intact** (it is about *training the recurrence in situ*,
class-independent; B1's `{δ, κ_tot, μ}` defines the recurrence either way) — the Supervisor's point (3) is
correct. **Recommendation:** at PR-2, *name the class actually simulated* and make the dependent choices
consistent: (a) if the bake-off trains μ (coupled), PR-1's Gate-i reproduction validates only the μ=0
diagonal reduction against published LinOSS, and the coupled generalization is validated by the
BPTT-on-substrate ceiling (roadmap-review F2.3) — state this explicitly; (b) debt #2's scope **widens** to
cover *both* LinOSS *and* the diagonal/coupled realization the rings actually are (S4D/DSS lineage +
whether coupling helps/hurts), and "benchmark transfer" must be *shown*, not cited; (c) pin the readout
(coherent-quadrature vs intensity) and propagate it to PR-2/S0.7. Also check the **conjugate-residue
constraint**: each ring's real realization ties the residues of λ and λ* (you cannot set them
independently) — confirm this costs no expressivity vs the benchmarked LinOSS (likely fine, but it is the
"conjugate symmetry hidden cost" the spec asks about, and it is real).

---

## 4. B2 backscatter rigor (hostile pass)

**Answer: (a) the crossover is defensible enough to act on (carry the optional knob) — the qualitative
finding is robust under independent re-derivation; (b) three things must be primary-source-verified before
the proposal/paper; (c) yes, the qualitative claim is robust to the shaky numbers — but I found a concrete
arithmetic inconsistency in one row and a factor-2 convention ambiguity in the criterion (S0.1-F4).**

I re-derived the whole crossover table from `Q_cross = ω₀/(4γ)` (the code's `2γ=κ_i` criterion):

| Scenario | γ/2π | Q_cross (mine) | memo | 2γ/κ_i @2e6 (mine) | memo | @3e7 (mine) | memo |
|---|---|---|---|---|---|---|---|
| damascene-clean | 11.8 MHz | 4.10×10⁶ | 4.1×10⁶ ✓ | 0.49 | 0.49 ✓ | 7.3 | 7.3 ✓ |
| subtractive-low | 90 MHz | 5.37×10⁵ | 5.4×10⁵ ✓ | 3.72 | 3.7 ✓ | 55.8 | 55.8 ✓ |
| **subtractive-high** | **160 MHz** | **3.02×10⁵** | 3.0×10⁵ ✓ | **6.62** | **5.2 ✗** | **99.3** | **77.6 ✗** |

### S0.1-F4 (MEDIUM) — One B2 row is internally inconsistent; and state the splitting criterion's ~2× convention band
1. **Arithmetic slip (high-roughness row).** Q_cross=3.0×10⁵ (from γ/2π=160) forces 2γ/κ_i = Qi/Q_cross =
   2e6/3.0e5 = **6.6** at foundry and **99** at 3e7 — but the memo tabulates **5.2** and **77.6**, which
   instead correspond to γ/2π≈125 MHz (Q_cross≈3.85×10⁵). The row mixes a 160-based Q_cross with
   125-based ratios. Harmless to the conclusion (5.2 and 6.6 are both ≫1 → "splits hard at foundry" either
   way) but it is exactly the kind of slip the verify-before-cite flag exists for. Fix the row to one γ.
2. **Criterion convention (state it).** The code/memo use **2γ ≳ κ_tot** (→ doublet "visible" when the
   splitting exceeds the *HWHM*). The stricter "fully resolved doublet" convention is **2γ ≳ 2κ_tot** (→
   splitting exceeds the *FWHM*), which shifts every Q_cross **×2** (e.g. damascene-clean 4.1×10⁶ →
   8.2×10⁶, which I verified). The chosen criterion is the *conservative* one (flags splitting earlier =
   the safe direction for a risk bound) — good — but the paper must **state which criterion** and carry
   the ~2× band, because Q_cross is the headline number. **Robustness check (passes):** the qualitative
   conclusion holds under *both* conventions — damascene-clean stays in (2×10⁶, 3×10⁷) (4.1 or 8.2×10⁶);
   rough stays below foundry. So the "process-roughness-gated, not Q-gated" finding does **not** depend on
   the shaky figures.

### S0.1-F5 (MEDIUM) — Primary-source verification owed before any proposal/paper use (affirming the Executor's own flag, sharpened)
The Executor flagged this honestly; I confirm it is **required**, and specify exactly what:
(i) the **63 MHz Pfeiffer** value and the **author lists** of arXiv:2511.02198 / 1609.08699 / 1205.4448
came via search-aggregation — confirm against the primary PDFs before citing; (ii) the
**2γ-vs-κ_tot crossover curve is *assembled* here** from bracketing SiN points — there is **no single
published SiN crossover-Q curve**, so the paper must present it as *our construction from cited points*,
not as a literature result; (iii) **no published γ exists for the specific AN800/CORNERSTONE processes** —
so "splits at the foundry corner" is a statement about *rough SiN generally*, and **which** foundry
process the bake-off assumes (clean-damascene-like vs rough-subtractive) is a PR-4 assumption that must be
made explicit, not left to the reader. This is a literature-track (S0.L) deliverable before S0.8;
acting on the *qualitative* finding now (carry the knob) is correct and does not wait on it.

---

## 5. The backscatter decision (D-2026-06-08-3)

**Answer: agree — the optional roughness-gated knob + PR-4 sub-parameter is the right response; the
platform tension is correctly load-bearing. Three strengthenings.** Full adjudication below; the substance:

The knob correctly *triggers on the S0.1 bound* rather than on Q alone, which is the honest reading of the
physics (γ is an absolute fabrication rate; splitting grows as κ_i falls). The platform tension
— **highest-Q = best-memory = most splitting-prone, while CORNERSTONE's low Q (≈2.3×10⁵, ~33 round
trips) is splitting-safe but memory-poor** — is real and *should* be load-bearing for PR-4 and S0.7-lite.
My strengthenings (carried into the adjudication): (1) **evaluate splitting at the *operating* κ_ext, not
just the undercoupled worst case** — the B2↔B3 interaction (overcoupling widens the linewidth and
suppresses visible splitting) means a *readout-viable* operating point tolerates more γ than the
undercoupled crossover suggests, so PR-4 should register the splitting risk *at its κ_ext policy*, which
may materially relax it; (2) make the knob **default-ON for anything but the clean-damascene corner**, and
have PR-4 state the **clean-process assumption explicitly** if the single-pole substrate relies on it;
(3) primary-source verification (S0.1-F5) before the crossover numbers enter the proposal.

---

## 6. B1 white-space-minimal-set

**Answer: the trainable/excluded *partition* is clean and supports "recurrent parameters updated on the
device" without smuggling in the readout — the load-bearing distinction (vs the Bueno/Brunner readout-RL
line, debt #1) is correctly drawn. But the *physical actuation* of the gain-free minimal set has a wrinkle
the "suffices" claim glosses (S0.1-F6).**

The partition is right: the recurrence is `M = diag(−κ_tot+iδ)+iΩ`; B1 trains exactly `{δ_j, κ_tot,j,
μ_jk}` = M's parameters = "pole positions + inter-ring couplings." Residues/B,C (the MZI mesh) are
excluded and explicitly identified as the reservoir baseline — training only those does **not** count.
This is exactly the form that defends the white-space sentence and pre-empts readout-only priors. Good.

### S0.1-F6 (MEDIUM) — In the gain-free minimal set, the damping actuator (κ_ext) is *also* the readout-residue knob; recurrence and readout are not physically independent there
B1 says the gain-free Stage-1 set `{δ (heaters), κ_ext (couplers), μ (ring–ring)}` "already suffices."
But the **only** gain-free actuator for the pole *real part* is κ_ext — and κ_ext simultaneously sets the
readout residue (`|c_jb_j|~2κ_ext`) and drop efficiency (B3). The B3 memo notes this coupling; B1's
"suffices" framing does not carry it through. Consequences:
- **White-space claim: survives.** δ and μ are clean recurrence-only knobs; modulating κ_ext is still a
  legitimate recurrent-parameter update. The headline is safe. ✓
- **Reservoir-baseline contrast: muddied.** The §10 *training-advantage* test ("train recurrence" vs
  "freeze recurrence, train only readout") assumes recurrence and readout are separable knobs. In the
  gain-free device they are not: you cannot hold the readout fixed while training the pole real part via
  κ_ext. Either (i) the reservoir baseline must freeze {δ,κ_ext,μ} and train a *separate* readout
  attenuator/mesh (added component), or (ii) the minimal set trains only {δ,μ} (pole real parts fixed at
  the passive/coupling value) to keep the readout clean — in which case "train the full recurrence" needs
  Stage-2 gain after all. **Recommendation:** PR-2 must specify *how* κ_tot is actuated in the gain-free
  architecture and how the readout is held independent for the reservoir baseline (this is also the
  physical-realizability half of the roadmap-review F7 fairness contract — the baseline must run on the
  *same* device). An add-drop ring's two couplers (κ_ext1, κ_ext2) give a constrained 2-knob freedom
  (adjust κ_tot along a path that partly holds the residue) — worth noting, but it does not fully
  decouple them; PR-2 should pick a concrete scheme.

---

## 7. B3 + the bound

**Answer: correct and honestly characterized. The `memory × residue ≤ passive memory` bound is right, the
κ_ext trade numbers reproduce exactly, and the B2↔B3 coupling is sound.**

I re-derived the bound: `mem×residue_norm = 2κ_ext/(κ_i·κ_tot·dt)`, passive memory `= 1/(κ_i·dt)`, ratio
`= 2κ_ext/κ_tot = 2κ_ext/(κ_i+2κ_ext) < 1`, → the product is bounded by passive memory and *saturates* it
in the overcoupled limit. Correct, and `test_memory_times_residue_bounded_by_passive_memory` checks it.
The trade table reproduces **to the digit** (kext/κ_i = 0.1 → 274 rt / 0.028 drop-eff / 0.20 residue; →
10 → 16 rt / 0.907 / 20.0; passive ceiling 329 rt). The B2↔B3 coupling — overcoupling widens the
linewidth and suppresses visible splitting, so the deep-undercoupled max-memory policy is the *most*
exposed to the doublet — is physically sound and `test_coupling_suppresses_visible_splitting` confirms the
direction. This is the cleanest of the three memos. No finding beyond folding the B2↔B3 interaction into
PR-4 (covered in §5/the adjudication).

---

## 8. F13.1 registry fix

**Answer: exactly right. Resolves the inconsistency I raised last review. Re-derived every number.**

Independent re-derivation (n_g=1.95, λ=1550 nm): 0.03 dB/cm → Qi=**1.144×10⁷** (memo: 1.14e7 ✓; this is
the ~5.7× inconsistency in the salvaged entry); Qi=2×10⁶ → loss=**0.1716 dB/cm** (memo: 0.172 ✓);
Qi=3×10⁷ @ n_g=2.09 → **0.01226 dB/cm** (memo: 0.0123 ✓); CORNERSTONE 1.5 dB/cm @ n_g=2.0 → Qi=**2.347×10⁵**
(memo: 2.347e5 ✓). The `q_basis` scheme (register one of (α,Q_i) as primary, derive the partner) is the
correct fix, and the **`loss_q_ceiling_ok` invariant (Qi ≤ qi_from_loss(loss)) is sound physics** —
propagation loss sets a Q *ceiling*; bend/coupler/absorption channels only lower Qi, so the loss-limited
SiN entries sit *on* the ceiling (equality) while bend-limited Si/InP sit *below* it (`q_basis=
"independent"`, headroom). This is exactly the right invariant and the right per-class treatment.

### S0.1-F7 (MEDIUM) — The conservative corner is sound for gating but is mislabeled as a real foundry process
The reconciled entry registers Qi=2×10⁶ / 0.172 dB/cm under the name **`SiN_LIGENTEC_AN800`**. The code
comment is honest that this is a *deliberately conservative corner*, not AN800's best (it notes AN800 has
*demonstrated* Qi≈6.8×10⁶ at 0.051 dB/cm). But the **real LIGENTEC AN800 is substantially better** than
the registered numbers (lower loss, higher Q). For internal modeling, registering a conservative corner is
the right call (it gates Gate ii on memory the foundry will actually deliver — consistent with
roadmap-review F13). For the **paper**, citing "LIGENTEC AN800: 0.172 dB/cm, Qi=2×10⁶" would be a
**misattribution** — attributing to a named foundry numbers it does not publish and that are worse than
its real product. **Recommendation:** before PR-4/paper, either (a) rename to
`SiN_foundry_conservative` (a hypothetical conservative corner, no foundry attribution), or (b) register
the *actual* AN800 numbers (≈0.05 dB/cm, Qi≈6.8×10⁶ derived) as `SiN_LIGENTEC_AN800` and keep 2×10⁶ as a
*separate* labelled conservative corner. The Gate-ii cell can still be the conservative corner (F13); only
the *name/citation* needs fixing. Citation integrity — fits the proposal's "verify against primary
sources" discipline.

---

## Beyond the checklist (hostile-reviewer sweep)

### S0.1-F3 (MEDIUM) — 2× units slip in the headline memory figure; PR-2 task sizing must use the amplitude convention
The results-log finding 4 and `mapping_notes` §4 report "**1.65 ns / 329 round trips**" (Qi=2e6) and
"**24.7 ns / 4937 round trips**" (Qi=3e7). These pairings are internally inconsistent by **2×**:
- 329 round trips × 10 ps (τ_rt) = **3.29 ns** = the *amplitude* memory time 1/κ_i (the SSM **state**
  memory — what the recurrence actually retains, since |z|=exp(−κ_tot·dt) is an *amplitude* retention).
- **1.65 ns** = Qi/ω₀ = 1/(2κ_i) = the *photon/energy* lifetime (|a|² decay) — relevant to power/SNR, not
  to state memory.

The **code is correct and distinguishes them** (`loss_limited_memory_time_s`=1/κ_i=3.29 ns vs
`photon_lifetime_s`=Qi/ω₀=1.65 ns); the slip is purely in the *prose pairing* — it grabbed the photon
lifetime for the ns figure while the round-trip count uses the amplitude memory. This matters because
**PR-2 sizes the bake-off task's required sequence length against this number**, and the two conventions
differ by 2× (329 vs ~165 round trips of usable memory). **Recommendation:** report one convention
consistently — for an SSM the **amplitude/state memory (3.29 ns / 329 rt; 49.4 ns / 4937 rt)** is the
right one — and have PR-2 size against it explicitly. (The 15× foundry→class-leading ratio and the
round-trip counts are correct; only the ns labels are off.)

### S0.1-F8 (MEDIUM) — Un-modelled §3 effects with real downstream consequences; and pole-region "realizability" completeness
The model is a single-pole-per-ring **linear LTI** CMT. Reasonable for the Stage-0 mapping, but two gaps
should be on the register, not discovered at S0.3/S0.7:
1. **Thermal self-heating (resonance ∝ circulating power).** In high-Q SiN at the circulating powers
   detection needs, self-heating shifts the resonance with |a|² (thermal bistability) — a **power-dependent
   pole δ** that directly threatens the LTI assumption and the "δ set by heater only" actuation, and it
   *worsens with Q* (the same high-Q the memory story wants). This is the most important un-modelled
   effect; flag it for the S0.3 substrate (bounds usable optical power → detector SNR → the B3 trade and
   the S0.7 precision–accuracy link). **SiN's compensating advantage** (worth stating positively): unlike
   Si, SiN has negligible TPA/FCA at 1550 nm (large bandgap), so free-carrier effects — a major Si ring
   nonlinearity — are genuinely minor here. Dispersion across the N-ring detuning comb (FSR varies with
   n_g(λ)) is a minor Stage-0 omission; note for completeness.
2. **"Realizable pole region" is the *continuous envelope*, not the *realizable set*.** It bounds
   stability (free), memory (loss-limited), β (FSR-bounded), readout (κ_ext), splitting (B2) — but omits
   (i) the **number of rings / state-dimension bound** (reticle area vs ring count, §9 risk 5 — feeds PR-2
   state-dim sizing) and (ii) the **pole-*placement* precision** (thermo-optic tuning resolution, DAC
   bits, residual drift — the reachable poles are a quantized/uncertain *subset* of the envelope). For a
   bound titled "realizable," add at least a note on N and on placement precision; both feed PR-2/S0.7.

### S0.1-F9 (LOW) — Convention/provenance hygiene for the write-up
The `√κ_ext` (proposal schematic) vs `√(2κ_ext)` (Haus, code) factor-2 is correctly documented as a
naming convention in `mapping_notes` §1 — good; just ensure the formal write-up states it once so a
reader checking the proposal against the code is not tripped. The `−1` phase convention
(`T_cmt = −T_salvaged`) is likewise documented. No action beyond carrying both into the paper's
conventions paragraph.

---

## Decision recommendations (independent)

### D-2026-06-08-2 (mapping fork) — **AGREE with the choice, REJECT the framing as stated**
**Simulate the complex-diagonal layer: yes.** It is the honest representation of what rings do and it is
hardware-minimal. **But not because "it *is* diagonalized LinOSS"** — that conflates the
diagonal complex-pole SSM (S4D/DSS class, what the rings are) with LinOSS (the conjugate-pair special
case). The defensible statement (S0.1-F2): *the ring bank natively realizes a diagonal complex-pole SSM;
uncoupled and with real I/O it reduces exactly to LinOSS; with trainable inter-ring coupling μ it is a
mild generalization beyond standard (diagonal-A) LinOSS.* Conditions on the recommendation, all feeding
PR-1/PR-2/debt #2:
1. **The "2× rings for the same state dim" benefit and the "it's LinOSS" claim are in tension** — you get
   the 2× by *not* pairing poles (S4D), but then it is not LinOSS. Own one: I recommend **target the
   diagonal class** (take the hardware-minimality, cite the S4D/DSS lineage *and* LinOSS as its
   oscillatory special case), and **soften the "oscillatory LinOSS" branding** to "an
   oscillatory/diagonal photonic SSM" where the rings aren't conjugate-paired.
2. **Benchmark transfer is open debt #2, not a given.** PR-1's named benchmark must match the class
   actually simulated, and debt #2 must *show* transfer to the diagonal (and, if μ≠0, the coupled)
   realization — published LinOSS numbers validate only the μ=0 diagonal reduction.
3. **Pin the readout** (coherent-quadrature = real-linear → LinOSS-equivalent; intensity = nonlinear) at
   PR-2; it determines whether the equivalence holds and feeds S0.7.
4. **White-space claim is unaffected** (correct, per the Supervisor) — keep that point.

### D-2026-06-08-3 (backscatter) — **AGREE, with three strengthenings**
The optional roughness-gated splitting knob + promoting roughness/splitting to a PR-4 sub-parameter is the
right response; it correctly triggers on the S0.1 *bound* (process-roughness-gated) rather than on Q
alone, and the platform tension (high-Q best-memory = most splitting-prone vs CORNERSTONE low-Q
splitting-safe/memory-poor) is correctly load-bearing for PR-4 and S0.7-lite. Strengthen:
1. **Evaluate splitting at the *operating* κ_ext, not just the undercoupled worst case.** The B2↔B3
   interaction means a readout-viable (overcoupled) operating point *suppresses* visible splitting — so
   the undercoupled crossover is the *worst* case, and PR-4 should register the splitting risk at its
   actual κ_ext policy, which may materially relax the constraint (and couples this decision to the κ_ext
   policy decision — resolve them together, as D-08-1's update already anticipates).
2. **Default the knob ON for anything but the clean-damascene corner**, and have **PR-4 state the
   clean-process assumption explicitly** if the single-pole substrate relies on it (a rough-subtractive
   foundry run breaks "one ring = one pole" at the foundry corner — the substrate is then only valid for a
   *clean*-process foundry, which must be said).
3. **Primary-source verification (S0.1-F5) and the row-arithmetic fix (S0.1-F4) before the crossover
   numbers enter the proposal/paper.** Act on the *qualitative* finding now (robust under independent
   re-derivation, both criterion conventions); gate the *quantitative* crossover-Q on S0.L confirmation.

---

## Bottom line for Lucas

S0.1 is solid work: the gate is genuinely passed for what it tests, the dynamical core is correctly built,
the architecture constraints are honored with strong tests, and the F13.1 fix and B3 bound are exactly
right — most numbers reproduce to the digit under independent re-derivation. **S0.2 can proceed**, but
four edits should land *before* PR-1/PR-2 freeze: add a transient-dynamics validation (S0.1-F1 — the one
real gate gap, since the paper's claim is the *dynamical* mapping and the gate currently proves it only by
construction); reframe the mapping fork as a diagonal/S4D-class SSM with LinOSS as its special case and
widen debt #2 accordingly (S0.1-F2 — the most important conceptual finding, and the Supervisor's "it is
LinOSS" framing should not freeze into PR-1 unexamined); fix the headline memory figure's 2× units slip so
PR-2 sizes the task correctly (S0.1-F3); and pin how the gain-free device actuates damping vs holds the
readout for the reservoir baseline (S0.1-F6). The B2 arithmetic/criterion/labeling items (S0.1-F4/F5/F7)
and the thermal/realizability completeness (S0.1-F8) are before-paper, not before-S0.2. On the decisions:
agree with simulating the complex-diagonal layer (reject only the "it is LinOSS" framing) and agree with
the roughness-gated splitting knob (evaluate it at the operating κ_ext, default it on off the clean
corner, verify the numbers before citing).

*Filed by the Critic, 2026-06-09. Independent review; not subject to Supervisor revision — disputes
escalate via `shared/escalate_to_human.md`.*
