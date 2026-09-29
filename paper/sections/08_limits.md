# §8 — Limits of this model

**Status:** v2, condensed 2026-09-29 for the first public deposit (v1 at commit `a508a28`).
§8.3 aligned with the audited P2 note (2026-09-20); review record moved to supplementary N9.8.

---

## 8.1 Robustness here means robustness to what we modelled

Every robustness statement in §5 is conditioned on the substrate of §3: the methods absorb the
imperfections *we simulated* — saturating gain at a registered operating point, Langevin amplifier
noise at NF 7 dB, resolved backscatter doublets, 5%-class calibration mismatch, fresh noise per
pass. Hardware contains channels we did not model: thermal transients and self-heating, polarization
rotation, fabrication disorder beyond the derate row, drift at cadences between our episode and
training scales, and mode-splitting behavior not captured by one always-on γ per process class. Any
of these could reorder the §5 ranking on a real chip. We regard the ranking as a hypothesis for
hardware to test, with PAT and SPSA committed because their chip-level robustness is already
established [CITE-Wright-2022; CITE-SPSA-photonic].

## 8.2 Anchor risks and verification debts, by name

The C-2 loss class transfers a wide-multimode racetrack result to a single-mode ring, priced by the
×2-loss derate row (§3.3). The Er:Si₃N₄ noise budget rests on a single coupling-loss-limited system
NF of ~7 dB, with the intrinsic amplifier NF not isolated (§3.2). The recurrent adjoint pass is
charged as if realizable with no demonstration in the literature (debt #4, an inference from
absence as of mid-2026). The white-space claim is one-sided evidence from a pre-registered search, last refreshed by a
bounded search on 2026-09-13 (debt #1; N3). The on-resonance clamp calibration under worst-case de-saturation remains a labelled
risk, with the δ-aware clamp ($r \approx 0.2547$) as its computed mitigation (§3.6).

## 8.3 The benchmark anchor we do not use

An early gate required reproducing a published LinOSS benchmark as an external anchor. Our port of
the model reproduced the Heartbeat result within its published band. On EigenWorms, five runs of
the authors' official code on their published seeds averaged 90.56%, against the published
95.0 ± 4.4%, with a population standard deviation of 8.35 percentage points (Fig. S1). Five runs
are descriptive; they do not show that the published mean or dispersion is wrong. We also found that
the implementation's classification loss, $-\log(p_\text{true} + 10^{-8})$ on softmax
probabilities, loses its gradient when the correct-class probability underflows. Our port shows
finite windows of exactly zero gradient, but an archived screen of the official code found no strict traps in eight runs under its registered classifier, so this mechanism is not established as the cause of the lower scores;
a separate note is in preparation. The gate was adjudicated purpose-served with the external anchor void (PR-1.1), and every
accuracy reference in this program is therefore an in-house
BPTT-on-substrate measurement under our own protocol (§5.1), never a transferred published number.
Our substrate runs in float64.

## 8.4 Review independence

Through 2026-07-06 every freeze in the ledger passed adversarial review by an independent reviewer
session reporting to the PI, and several results exist because that review forced them (the
multi-tap input map, the mismatch decomposition, the readout-differential rule). From 2026-07-07 the
program ran in a single-session mode in which one agent performed both execution and review under
standing PI delegation. Everything from that date, including the S0.4b/c and S0.5 findings and the
two honest nulls (the offline tie; RHEL's failure), should be read with that reduced independence
in mind. Pre-registration is the structural mitigation, with a stated caveat: once registrar and
registrant are the same agent, the commit trail is self-graded until it is externally anchored.
Two anchors exist. An OpenTimestamps proof of the ledger head certifies existence by date,
independently of repository access, though not the actual execution times of experiments. The
repository, with the full ledger and commit history, is released publicly with this preprint at
`github.com/LTalandier/Project_SSM`, which makes the recorded commit ordering inspectable. Seven
post-assembly review rounds and a later repository audit found errata concentrated in unregistered
connective prose, one pre-written consumption text applied to a degenerate outcome, one
implementation defect and one optical-time versus wall-time error. The affected claims were
corrected or withdrawn, and the defect was repaired by a registered rerun; the record is in
supplementary N8 and N9.8.

## 8.5 Scope limits we chose

The task family is deliberately narrow — continuous-signal channel equalization plus a synthetic
memory family, with the registered secondary task deferred — and the 128-ring C-3 cell never gates
anything. Calibration mismatch and drift, held fixed in the bake-off, were measured afterward in
pre-registered follow-ups (§5.5). Drift remains unmodelled *during* training at the bake-off cadence, and the tested drift
is gentle ($\approx 1.4\,\kappa_i$ accumulated) rather than worst-case. A follow-up task's operating
point must be registered against its own processing gain, the lesson of the degenerate memory probe
in §6. The strongest current evidence on the advantage question is §5.5's triple: no resolved
difference at five calibration levels spanning 5–30%, none under common-mode drift, and a declared
2.42× advantage specific to uncorrelated per-ring drift, whose hardware relevance rests on the
unmeasured correlation of real on-chip drift. The 2026-09-13 repository audit and its correction
were implemented and checked in one session without independent review (N8).
