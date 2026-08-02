# §4 — Four routes to on-chip gradients

**Status:** DRAFT v1 (2026-07-08, single-session mode — not independently reviewed; disclosed).
**Sources of record:** `shared/preregistration.md` PR-5/6/7(+7.1)/11 · roadmap S0.4a–c ·
`photonic_ssm/estimators/{spsa,pat,adjoint,rhel}.py` + gate tests (150/150) ·
`results/s0_4{a,b,c}/smoke.md` · `docs/s0_4/{pr5_twin_mismatch_recon,pr11_echo_submodel_recon,
f8_hardware_ledger}.md`. **Open flags:** [CITE-*] keys resolved via `paper/references.md` (2026-07-12; RHEL source page-verified; SiN-FWM γ disclosure added in-text).

---

## 4.1 What counts as a physical gradient

The fairness contract (PR-6) fixes one invariant above all: **a training method may obtain
gradient information only from simulated device passes on the shared substrate, with fresh noise
on every pass.** Autodifferentiation through the substrate is reserved for the BPTT reference —
the ceiling, never a contestant. All methods share, per seed: the same initialization (detunings
spread over $[-\kappa_i, \kappa_i]$, $r_0 = 0.3$, connected chain $\mu_c = 0.3\kappa_i$), the
same data stream (a function of seed and iteration only), the same head cadence, the same clamp
to the operative box, and the same pre-registered hyperparameters. Cost is counted in **physical
device passes, any direction** (PR-7): one pass = one sequence through the substrate. Digital
compute (a twin's forward/backward, the head update) lives on a side-ledger that is always
co-reported and never folded into the rank — a method that saves device passes by spending
digital FLOPs has a real but *different* advantage than a model-free one, and merging the ledgers
would hide exactly the distinction the comparison exists to draw.

## 4.2 SPSA — model-free, two passes

Simultaneous-perturbation stochastic approximation [CITE-Spall] perturbs the entire in-situ
partition by $\pm c\Delta$ (a random sign vector), measures the scalar loss twice, and forms a
descent direction from the difference: **2 device passes per update**, no model, no twin, no
added hardware beyond the plant's own actuators and its single readout (the simplest row of the
hardware ledger, supplementary note N2). Perturbations at the clamp boundary are one-sided. SPSA is
chip-demonstrated [CITE-SPSA-photonic] and inherits the crosstalk-robustness observed in our
prior thermo-optic work [CITE-pnn-multilayer]; its known weakness — gradient variance growing
with parameter count — is precisely what the sample-efficiency metric prices.

## 4.3 PAT — physical forward, twin backward

Physics-aware training [CITE-Wright-2022] evaluates the loss on the *measured* physical output
and takes the parameter gradient through a differentiable digital twin at the commanded
parameters: **1 device pass per update**, plus a twin forward/backward on the digital ledger.
PAT's value proposition is exactly this exchange, and its honesty hinges on the twin being
*imperfect in a registered way*. The twin-mismatch protocol (PR-5) freezes three families:
**M-par** — 5%-class parametric calibration errors on the constants and actuation maps
($\kappa_i{+}5\%$, $\gamma{+}5\%$, actuation ×1.05/×0.95, detuning offset $0.05\kappa_i$, a
loose gain pair ×1.10/×0.75 reflecting debt #3); **M-struct** — a structural omission (the twin
drops the gain's dependence on the trained coupling, the one channel a fixed-gain model cannot
see); and **M-noise** (always on) — the twin is noiseless. The headline PAT is the *composed*
mismatch; the decomposition is reported separately (§5.6). A perfect-twin gate verifies the
implementation: with mismatch off, PAT's gradient equals BPTT's to machine precision.

## 4.4 Recurrent in-situ adjoint — a physical reverse pass, by hypothesis

The adjoint route extends feedforward in-situ backpropagation [CITE-Hughes-2018] to the
time-domain cavity setting: the error field is physically propagated *backward* through the same
dissipative substrate, and the gradient is read from forward/adjoint interference. No recurrent
photonic demonstration of this pass exists (verification debt #4); the simulation charges it **as
if realizable** — 1 forward + 1 adjoint = **2 device passes per update**, zero digital — and
quarantines the realizability question in the hardware ledger (circulators, phase-coherent
injection, separability of the counter-propagating field from the backscatter doublet). The
simulated adjoint pass is honest about two physical limits: it carries **fresh noise** (the
reverse pass is its own noisy traversal), and the saturating gain is **frozen at its
operating-point value** in the backward linearization — a counter-propagating field experiences
the medium's saturation state but cannot realize the $\partial g/\partial\kappa_\text{ext}$
self-consistency channel. Both simplifications flatter the adjoint (a third, an additive noise
term on the adjoint field itself, awaits an error-launch power convention that is unresolved
hardware design), so the bake-off's adjoint arm is an **optimistic bound** and is labelled as
such wherever it appears. Floor checks: on the fixed-gain plane the adjoint gradient equals BPTT
to machine precision; in saturating mode the frozen-gain approximation costs 0.6% of gradient
direction at C-1 but **7.5% at C-2** — the one method-relevant quantity we measured to *grow*
with cell size.

## 4.5 RHEL — Hamiltonian echoes on a substrate that forgets

Recurrent Hamiltonian echo learning [CITE-Pourcel-2025; CITE-Lopez-Pastor-2023] trains by
time-reversal: evolve forward; apply a single conjugation to the state snapshot (for optical
fields, phase conjugation); evolve again through the *same* physics with the input replayed
time-reversed and a small error nudge injected continuously; the gradient is the symmetric finite
difference of $\nabla_\theta H$ between a $+\varepsilon$ and a $-\varepsilon$ echo. Three
consequences of taking the published algorithm seriously on a dissipative substrate, each
registered before the runs: (i) the count is **3 passes in the Hamiltonian limit but 4
operationally** (2 forward + 2 echo) — the echo does not return the state re-usable, and state
cloning is unphysical (PR-7.1); (ii) the conjugation fires **twice per update**, paying its
penalty chain independently each time; (iii) the update rule reads only the *coherent* generator,
so the dissipative channel of $\kappa_\text{ext}$ is structurally invisible to it.

The echo's physical primitive is modelled concretely (PR-11), not as an idealized operator:
a $\chi^{(3)}$ four-wave-mixing conjugation stage with the full penalty chain — extraction
through the ring ports ($\eta_\text{ex} = 2\kappa_\text{ext}/\kappa_\text{net} = 0.86$ at θ₀),
single-pass spiral conversion ($(\gamma_\text{nl} P_p L)^2 \approx -16.7$ dB at 0.3 W pump,
0.5 m; $\gamma_\text{nl} \approx 0.97\,\text{W}^{-1}\text{m}^{-1}$ for tight-confinement SiN
[CITE-SiN-FWM]), and timing decay — totalling **−22.4 dB per conjugation** (Fig. S3), plus the
phase-insensitive parametric quantum floor. A page-level check at assembly found published
*ultra-low-loss-geometry* demonstrations at $\gamma \approx 0.29$–$0.51\,\text{W}^{-1}
\text{m}^{-1}$ (with CW power handling demonstrated to 7 W) [CITE-SiN-FWM]; our 0.97 assumes a
tighter-confinement spiral than those demos, so the frozen chain is, if anything, *optimistic*
for RHEL — at the measured ULL values the conjugation penalty deepens by a further ~6 dB. The
direction only strengthens §5.4's conclusion, which the idealized-conjugator control shows does
not hinge on the chain at all. The quantum floor itself was measured negligible at the
$10^5$-photon state scale (as registered-to-measure), with pump-transfer excess included.
Because the ring fields overlap
spectrally, conjugating N rings needs N pumped arms: **≈9.6 W of on-chip pump at the headline
cell**, charged to the envelope. Off-chip conjugation was priced and excluded (the state decays
in transit: amplitude survival 0.12–0.54 at 10 ns for C-1/C-2; there is no storage primitive to
wait out a conjugator). Three irreversibility invariants bind the implementation and are
test-enforced: independent forward/echo noise streams (no common-RNG reversal); no loss-sign
flip (the echo traverses the same dissipative lattice); gain injects fresh ASE in the echo too —
and the echo of a noisy forward must *not* recover the noiseless state. The floor check
completes the picture: as dissipation is removed, the implemented RHEL gradient converges to the
exact reference (cosine $\to 1.0000$), so whatever §5.4 finds is the physics, not the code.

## 4.6 The guardrail

The four routes are *parallel in simulation, singular in hardware*: the Stage-1 chip is committed
to the two chip-demonstrated workhorses (PAT, SPSA) regardless of the bake-off's ranking, and an
exact-gradient route can earn a *later* hardware slot only by clearly beating both on a
pre-registered outcome criterion (PR-9; "exactness" is struck from the promotion menu). §5
reports how this resolved.
