# PR-19 task candidates — long-coherent-memory family (STEP 1 of the PI prompt)

**Status: PROPOSED 2026-08-13 — candidates only; nothing registered, nothing run.**
Provenance: proposed at external review (round-5/6 walkthrough), discharge path for the
N_eff finding (PR-18 §18.6b → §7.2). Controls it builds on: PR-18 taps-only + ablation.
PI picks the task; PR-19 is then drafted with both consumption texts and signed before
any measurement.

## A re-diagnosis that constrains the design (proposed for the PR-19 preamble)

T-A-L (PR-17 §17.4) added a −6 dB replica at delay 7, span 14. The digital head is an
**8-lag FIR**, and the substrate's θ₀ memory is ~then-current samples: much of the added
span sat within the *head's* reach, so the probe could be — and per the §5.5 head-absorbs
lesson plausibly was — partially discharged digitally, leaving the damping optimum
unmoved. That is a *head-reach confound*, not only the "more ISI to cancel" objection.
Design rule for every candidate below: **required coherent span ≫ 8 lags**, so the frozen
head structurally cannot carry it and the recurrence must.

## Candidate T-D — unipolar spread-spectrum despreading (optical-CDMA style) — RECOMMENDED

**Task.** Source symbols (4-PAM, frozen encoder family) are spread at chip rate by a fixed,
registered **length-31 m-sequence** in unipolar {A_lo, A_hi} form (standard optical-CDMA
convention — direct detection admits no field sign). The receiver recovers the symbol
stream; SER scored per symbol (each symbol = 31 chips). Channel: the frozen T-A 7-tap ISI
at 28 dB stays on top, unchanged.

- **(a) combining:** each decision coherently integrates 31 chips — combination across a
  span 31 ≫ 7, not cancellation.
- **(b) linear-solvable:** despreading = a fixed length-31 linear correlator on the (chip)
  amplitude stream; the substrate core is linear in field amplitude and the unipolar DC
  offset is a constant the FIR head removes. No nonlinear memory required.
- **(c) not rigged:** spreading factor 31 is the standard m-sequence length (2⁵−1), not a
  number tuned to N = 32. The non-tautology argument: an m-sequence is **spectrally flat**,
  and flat-spectrum FIR kernels are the worst case for low-order pole approximation — the
  required order is high for an *independently statable* reason, and degradation is
  graceful (correlation gain ∝ taps realized), so N_eff is genuinely measured, not implied
  by task success. Minimal digital filter: order ≈ 31 (the correlator) + the existing
  ~7-tap equalizer ≈ 38; a k-pole truncation loses ≈ 10·log10(k/31) dB of processing gain
  — smooth, measurable.
- **(d) metric:** SER unchanged; eval-F and the PR-3 target rule transfer verbatim
  (ceiling re-measured on-task per §5.1's protocol, as always).

**Expected N_eff under the §5.7 mechanism:** implementing a flat length-31 kernel with
exponential ring modes plus an 8-lag head needs ~
20–31 effective modes; per-hop transport at the light damping the task forces (below)
keeps the chain gradient-alive, so **N_eff ≈ 20–30** if the architecture can do it at all.

**Registered-prediction shape (STEP 2, joint):** memory ≥ 31 samples requires
κ_net ≲ 1.0 κᵢ, i.e. the pinned-damping optimum must move from the deep-overcoupling
plateau (r\* = 2.0–3.0 on T-A/T-A-L) to **r\*_D ≤ 1.0** — a large, falsifiable movement —
and by (μ/κ_net)²·hops the same move raises controllability, so *lighter optimum and
higher N_eff are one mechanism*. Separation rule of §17.5's form (30% median-SER
separation at the minimizer).

**What a null means:** if the optimum stays heavy and/or N_eff stays ≈ 8 while the task
passes, the chain implemented the correlator some other way than distributed memory —
report the mechanism; if the task *fails* at every damping (BPTT cannot reach target),
that is the citable negative: a nearest-neighbor coupled-ring chain cannot realize
flat-spectrum long kernels — §7.2's conditional becomes a stated architectural limit
(with the parallel-bank / non-chain topology named as the untested alternative).

## Candidate T-C — dense-comb crosstalk rejection (notch family)

**Task.** Frozen T-A equalization plus an additive **comb of K = 12 coherent interfering
tones** at registered pseudo-random in-band detunings (minimum spacing ~f_s/40), C/I ≈
10 dB, injected at the encoder so the interference propagates through the same field path.
Rejecting a tone *before* direct detection is a field-domain (ring-notch) operation —
post-detection linear filtering cannot remove the |s+i|² beat terms — so the photonic core
is forced to do the work in-field.

- (a) resolving tones spaced ~f_s/40 requires coherent observation ~40 samples ≫ 7 —
  combining (spectral estimation), not ISI cancellation.
- (b) notching is linear filtering; solvable by poles placed on the tones.
- (c) minimal digital (pre-detection, field-domain) order ≈ 7 + 2K ≈ 31 — set by the
  interference scenario (dense-WDM adjacent-carrier crosstalk / RFI excision, an
  independently motivated workload), not by our N; degradation is graceful (notch the
  strongest tones first).
- (d) SER unchanged.

**Expected N_eff:** ~2 rings per resolved tone + the equalizer subpopulation → 24–30.
**Sharpened profile prediction:** the converged damping profile should go **bimodal** —
notch rings light/narrowband, equalizer rings heavy — a stronger, more specific form of
the §6 heterogeneity claim. **Null meaning:** hybridized chain supermodes cannot isolate
narrow lines → chains can't notch; same architectural-negative consumption as T-D.
**Risk vs T-D:** more free parameters to freeze (K, spacings, C/I), and solvability-at-
ceiling needs the pilot to confirm before the fleet; T-D's solvability argument is cleaner.

## Candidate T-E — long-delay echo inversion (weaker; (a)-tension stated)

Channel gains a single strong echo at delay **D = 21** (α = 0.5): inverse has memory
~D/(1−α) ≫ 8, unreachable by the head (unlike T-A-L's delay-7). Independently motivated
(long multipath / radio-over-fiber reflections); linear; SER transfers. Honest tension:
it is still *cancellation* lengthened — the letter of criterion (a) disfavors it; it earns
its slot only as the minimal-change probe that fixes T-A-L's head-reach confound while
staying inside the equalization family. Expected N_eff ~15–25; a null here would be the
*third* no-movement result and, with T-A-L, would establish the pattern the PI prompt
names.

## Considered and rejected

**Delay-D recall / memory-capacity probe:** minimal order = D *by construction* and the
motivation is benchmark-internal — disqualified under (c) exactly as the prompt's
tautology test intends. **Parity/XOR-span tasks:** need nonlinear memory — violate (b).

## Recommendation

**T-D primary** (cleanest required-order argument, head structurally cannot cheat,
sharpest single registered prediction r\*_D ≤ 1.0), **T-C as the PI-choice alternative**
if scenario realism is preferred over benchmark cleanliness (its bimodal-profile
prediction is the scientifically richest). T-E only if the PI wants the minimal-change
probe. One task goes to PR-19; the others are named in the block as considered
alternatives with their criteria scores, so the choice is on record.

Sizing note (STEP 3 preview, not registered here): chip-rate clocking multiplies sequence
length ×31 per symbol at fixed scored-symbol count — the pilot on excluded seed 7 must
price this before any fleet; expect wall-clock ≫ T-A per unit and plan the budget
accordingly (report before committing, per the prompt).
