# §4 — Four routes to on-chip gradients

**Status:** v2, condensed 2026-09-29 for the first public deposit (v1 at commit `a508a28`).
Echo-chain penalty detail moved to supplementary N9.3.

---

## 4.1 What counts as a physical gradient

The fairness contract (PR-6) fixes one invariant: **a training method may obtain gradient
information only from simulated device passes on the shared substrate, with fresh noise on every
pass.** Automatic differentiation through the substrate is reserved for the BPTT reference, never
a contestant. Per seed, all methods share the initialization (detunings spread over
$[-\kappa_i, \kappa_i]$, $r_0 = 0.3$, connected chain $\mu_c = 0.3\kappa_i$), the data stream, the
head cadence, the clamp and the pre-registered hyperparameters. Cost is counted in **physical
device passes, any direction** (PR-7), one pass being one sequence through the substrate. Digital
compute sits on a side-ledger that is always co-reported and never folded into the rank: saving
device passes by spending digital FLOPs is a real but different advantage from needing no model.

## 4.2 SPSA — model-free, two passes

Simultaneous-perturbation stochastic approximation [CITE-Spall] perturbs the whole partition by
$\pm c\Delta$ (a random sign vector) and measures the loss twice: **2 device passes per update**,
no model, no twin, no hardware beyond the plant's own actuators and readout (supplementary N2).
Perturbations at the clamp boundary are one-sided. SPSA is chip-demonstrated
[CITE-SPSA-photonic] and was crosstalk-robust in our prior thermo-optic work
[CITE-pnn-multilayer]; its gradient variance, growing with parameter count, is what the
sample-efficiency metric prices.

## 4.3 PAT — physical forward, twin backward

Physics-aware training [CITE-Wright-2022] evaluates the loss on the *measured* output and takes
the gradient through a differentiable digital twin at the commanded parameters: **1 device pass
per update**, plus a twin forward and backward on the digital ledger. Its honesty depends on the
twin being imperfect in a registered way (PR-5). **M-par** applies 5%-class parametric errors
($\kappa_i{+}5\%$, $\gamma{+}5\%$, actuation ×1.05/×0.95, detuning offset $0.05\kappa_i$, gain
pair ×1.10/×0.75). **M-struct** drops the gain's dependence on the trained coupling, the one
channel a fixed-gain model cannot see. **M-noise**, always on, makes the twin noiseless. The
headline PAT carries the composed mismatch; §5.6 decomposes it. With mismatch off, PAT's gradient
equals BPTT's to machine precision.

## 4.4 Recurrent in-situ adjoint — a physical reverse pass, by hypothesis

The adjoint route extends feedforward in-situ backpropagation [CITE-Hughes-2018] to the cavity:
the error field propagates backward through the same dissipative substrate, and the gradient is
read from forward/adjoint interference. No recurrent photonic demonstration of this pass exists
(verification debt #4). The simulation charges it **as if realizable** — 1 forward + 1 adjoint =
**2 device passes per update**, zero digital — and leaves realizability to the hardware ledger
(circulators, phase-coherent injection, separating the counter-propagating field from the
backscatter doublet). The simulated reverse pass carries fresh noise, and the saturating gain is
frozen at its operating-point value. On the fixed-gain plane the adjoint gradient equals BPTT to
machine precision; in saturating mode the frozen-gain approximation costs 0.6% of gradient
direction at C-1 but **7.5% at C-2**. It omits a noise term on the adjoint field itself, which awaits an unresolved error-launch
power convention. These simplifications flatter the adjoint, so its arm is an **optimistic bound**
wherever it appears.

## 4.5 RHEL — Hamiltonian echoes on a substrate that forgets

Recurrent Hamiltonian echo learning [CITE-Pourcel-2025; CITE-Lopez-Pastor-2023] trains by time
reversal: evolve forward, apply one conjugation to the state snapshot (for optical fields, phase
conjugation), evolve again through the same physics with the input replayed time-reversed and a
small error nudge, and take the symmetric finite difference of $\nabla_\theta H$ between a
$+\varepsilon$ and a $-\varepsilon$ echo. Taking the published algorithm seriously on a
dissipative substrate has three registered consequences: **4 device passes per update**
operationally (3 in the Hamiltonian limit, but the echo does not return a reusable state and
state cloning is unphysical; PR-7.1); the conjugation fires **twice per update**; and the update
reads only the coherent generator, so the dissipative channel of $\kappa_\text{ext}$ is invisible
to it.

The echo is modelled concretely (PR-11): a $\chi^{(3)}$ four-wave-mixing conjugation stage whose
extraction, spiral-conversion and timing penalties total **−22.4 dB per conjugation** (Fig. S3; N9.3),
plus the parametric quantum floor, at $\gamma_\text{nl} \approx 0.97\,\text{W}^{-1}\text{m}^{-1}$
[CITE-SiN-FWM]. Published ultra-low-loss demonstrations reach 0.29–0.51 W⁻¹m⁻¹, so the chain is
optimistic for RHEL by ~6 dB. Conjugating N spectrally overlapping rings needs N pumped arms,
**≈9.6 W of on-chip pump at the headline cell**, charged to the envelope. Implementation
invariants — independent forward and echo noise, no loss-sign flip, fresh amplifier noise in the
echo — are test-enforced, and as dissipation is removed the implemented gradient converges to the
exact reference (cosine $\to 1.0000$; Fig. S5).

## 4.6 The guardrail

The four routes are *parallel in simulation, singular in hardware*: a Stage-1 chip is committed to
the two chip-demonstrated workhorses, PAT and SPSA, whatever the ranking, and an exact-gradient
route can earn a later hardware slot only by clearly beating both on a pre-registered outcome
(PR-9).
