# §6 — Choosing the damping operating point

**Status:** DRAFT v1 (2026-07-08, single-session mode — not independently reviewed; disclosed).
**Sources of record:** `results/s0_6/{damping.md,damping.json,runs/}` (spec pre-registered at
`5a7f28b`) · PR-12 🔒 R-ii · PR-3 §A eval protocol. **Open flags:** [CITE-*] keys resolved via `paper/references.md`; figure F6 = `paper/figures/F6_damping.*`.

---

The D-LinOSS line's central observation — that damping in an oscillatory SSM is a *performance
knob*, not a defect to minimize — has a sharp physical meaning here: per-ring damping is the net
loss $\kappa_\text{net}(\kappa_\text{ext})$, and the tunable coupler that sets it is already in
the trained partition. The registered disposition (R-ii) therefore frames the question not as
"which damping value do we freeze?" but as "does training *find* the right damping within the
feasible box?" — and the experiment separates the two readings with two arms, six damping points,
eight seeds each, at the headline cell under the convergence-controlled protocol of §5.1.

**The damping value matters enormously.** With $\kappa_\text{ext}$ *pinned* (only detunings and
inter-ring couplings training), the converged error spans a factor of ~300 across the feasible
box: SER 0.39 at light damping ($r = 0.2$ — not chance, which is 0.75 on 4-PAM, but two of
every five symbols wrong) falling to $1.3\times10^{-3}$ at the optimum — which sits at **deep overcoupling** ($r^* = 2.0$, $\kappa_\text{net} \approx
4.1\kappa_i$, about 5.5 samples of memory at 2 GS/s). The direction is instructive: the
equalization task needs only a 7-tap span, and the long memory the light-damping regime supplies
(30–45 samples) is actively harmful — stale symbols interfere. "More memory" is not free
performance in a dissipative recurrence; damping tunes memory *to the task*, which is precisely
the D-LinOSS thesis in physical units, with the optimum on the heavily-damped side for this task
class.

**Training absorbs the knob.** In the second arm the full partition trains inside progressively
wider boxes $[r_\text{min}, r_\text{hi}]$. Every box containing the pinned optimum reaches within
the pre-registered margin of it — in fact reaching $5\times10^{-4}$, the §5 ceiling, *better*
than the best uniform pin: per-ring trainable coupling finds a heterogeneous damping profile no
single design value can express. Boxes that exclude the good regime fail exactly as they must
(training cannot find what the clamp forbids). The registered R-ii test is therefore
**confirmed**: the designer's damping obligation is to make the feasible box *contain* the good
regime; the operating point itself is the trained substrate's job.

Two honest footnotes. The slow mid-grid configurations ($r = 0.3$–$0.5$) had not fully plateaued
at the training ceiling, so the ×300 spread is a budget-bounded statement — but both endpoints
and all winning configurations converged, and the R-ii verdict uses converged points only. And
the result recolors §5 slightly: a large share of what in-situ training accomplished in the
bake-off *is* finding the damping operating point (the θ₀ hold value, pinned, yields 0.038 —
seventy-seven times worse than the trained substrate). Since the offline baseline finds $r^*$ on
its calibrated model just as well (§5.5), the damping result strengthens the trainability story
without moving the advantage question.

**Does the optimum track task memory? A registered prediction, failed.** Because "excess memory
is harmful" measured on one 7-tap task is close to tautological, we froze a transfer test
(PR-17 §17.4–17.5): a second task, T-A-L — the same channel plus a −6 dB replica of its
past-tap profile delayed by 7 symbols, doubling the memory span to 14 — with the registered
prediction that the pinned-damping optimum moves to *lighter* damping ($r^*_L < 2.0$), and a
frozen 30%-separation rule for upgrading the claim. **The prediction failed.** The T-A-L
optimum does not move toward lighter damping at all: the curve keeps falling to the heavy edge
of the grid ($2.2\times10^{-3}$ at $r = 3$ vs $2.5\times10^{-3}$ at $r = 2$, eval-F, within
13% — the separation rule does not fire; Fig. F6, dashed). What doubling the task span
actually did was raise the error floor everywhere (the harder channel) while leaving the
optimal damping regime where it was. The honest reading: on this substrate and task class the
heavy-damping optimum is *robust* to a ×2 change in task memory span — the optimum is set by
the bandwidth/interference trade of the equalization family, not by naive span-matching — and
the "damping tunes memory to the task" sentence above must be read at that class level, not as
a per-task tracking law. A task family engineered to *need* long coherent memory (rather than
a longer ISI to cancel) remains the right probe, and is registered residue, not a claim.
