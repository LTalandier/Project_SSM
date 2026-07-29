# §8 — Limits of this model

**Status:** DRAFT v1 (2026-07-08, single-session mode — not independently reviewed; disclosed).
**Sources:** PR-4 anchor-risk register · F19 (verbatim seed) · the four verification debts
(proposal closing note) · `shared/critic_review_s0_4_freeze.md` (independence disclosure) ·
PR-1.1 (G3 record). **Open flags:** [CITE-*] keys resolved via `paper/references.md`; the P2 note's send (▢ PI action).

---

## 8.1 Robustness here means robustness to what we modelled

Every robustness statement in §5 is conditioned on the substrate of §3: the methods absorb the
imperfections *we simulated* — saturating gain at a registered operating point, Langevin ASE at
NF 7 dB, resolved backscatter doublets, 5%-class calibration mismatch, fresh noise per pass.
Hardware contains channels we did not model: thermal transients and self-heating at operating
power, polarization rotation, fabrication disorder beyond the derate row, drift at cadences
between our episode and training scales, and mode-splitting behavior that is not captured by a
single always-on γ per process class. Any of these could reorder the §5 ranking on a real chip.
We regard the ranking as a hypothesis the Stage-1 hardware exists to test, with PAT and SPSA
committed precisely because they are the two routes whose chip-level robustness is already
literature-established [CITE-Wright-2022; CITE-SPSA-photonic].

## 8.2 Anchor risks and verification debts, by name

The substrate's realism leans on anchors with stated residual risks: the C-2 loss class
transfers a wide-multimode racetrack result to a single-mode registry ring (priced by the
×2-loss derate row, §3.3); the Er:Si₃N₄ noise budget rests on a **single coupling-loss-limited
measured NF (~7 dB)** in the flagship device paper — debt #3's original "no measured NF" premise
was found false at the S0.3-0 recon and our NF-A = 7.0 dB was frozen to match the measurement
(§3.2); the narrower residue (intrinsic amplifier NF not isolated) keeps the NF sensitivity
rows registered; the recurrent adjoint pass is charged *as if realizable* with no
demonstration in the literature (debt #4 — an inference from absence, time-stamped mid-2026);
and the white-space claim itself is one-sided evidence from a pre-registered search, to be
re-swept before submission (debt #1). The S0.4-0 calibration retired one internal debt (the
drive build-up controversy resolved by measurement: ×0.42, doublet-quenched) and left one open:
the on-resonance floor calibration under worst-case de-saturation (anchor-risk vii, §3.6),
carried as a label.

## 8.3 The benchmark anchor we do not use

An early gate required reproducing a published LinOSS benchmark as an external anchor. Running
the authors' own code on their published seeds reproduced the Heartbeat headline within its
band; on the long-sequence EigenWorms task the rerun mean itself lands within one published
standard deviation ($90.6$ vs $95.0 \pm 4.4$) — what fails is not the mean but the
*dispersion* (per-seed $\sigma = 9.3$, $2.1\times$ the published value, from a bimodal
seed population) and the mechanism behind it: a numerical-precision failure mode in the
training loss (an absorbing zero-gradient state in fp32) that makes the published number
seed-unstable rather than unreproducible (Fig. S1; a separate reproducibility note is in
preparation). The gate was adjudicated purpose-served-with-anchor-void: all
downstream accuracy references in this program are therefore **in-house BPTT-on-substrate
ceilings** measured under our own protocol (§5.1), never transferred published numbers. We flag
fp32-sensitivity generally: our substrate runs float64, and the eval-floor granularity of §5 is
symbol-count-limited, not precision-limited.

## 8.4 Review independence

Through 2026-07-06 every freeze in the ledger passed adversarial review by an independent
reviewer session reporting to the PI, and several results in this paper exist because that
review forced them (the multi-tap input map, the mismatch decomposition, the readout-differential
rule). From 2026-07-07 the program ran in a single-session mode in which the same agent
performed both execution and review, under standing PI delegation; every artifact from that
period is so labelled in the ledger, and the S0.4b/c/S0.5 findings — including the two honest
nulls (the offline tie; RHEL's failure) — should be read with that reduced independence in mind.
The pre-registration discipline (thresholds frozen and committed before runs) is the structural
mitigation — with the caveat stated plainly: from the single-session date onward the registrar
and the registrant are the same agent, so the commit trail is self-graded until it is
externally anchored. The repository, including the full ledger and its commit history, is
published (externally timestamped) before submission precisely so that the freeze-before-run
ordering can be verified by anyone rather than trusted.

## 8.5 Scope limits we chose

The task family is deliberately narrow (continuous-signal channel equalization plus a
synthetic memory family; the registered secondary task is deferred), and the C-3 128-ring cell
never gates anything. Two axes the bake-off itself held fixed were measured afterward in
pre-registered follow-ups (§5.5): calibration-mismatch sensitivity (swept to 30%-class — the
tie holds) and drift (a literature-calibrated random walk under a deploy-then-drift protocol,
two correlation regimes). Drift remains unmodelled *during* training at the bake-off cadence,
and the tested drift magnitude is gentle ($\approx 1.4\,\kappa_i$ accumulated) rather than
worst-case. The systems-advantage question — whether any of this pays once conversion overhead
is counted — is §7's; the strongest current evidence is §5.5's mechanism triple: no advantage
from calibration accuracy at any tested mismatch, none under common-mode drift, and a
declared pre-registered $2.42\times$ advantage specific to uncorrelated per-ring drift —
whose real-hardware relevance rests entirely on how uncorrelated actual on-chip drift is, an
unmeasured quantity we elevate to the sharpest Stage-1 experiment (§9). We consider stating
that plainly to be the paper's job.
