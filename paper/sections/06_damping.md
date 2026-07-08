# §6 — Choosing the damping operating point

**Status:** DRAFT v1 (2026-07-08, single-session mode — not independently reviewed; disclosed).
**Sources of record:** `results/s0_6/{damping.md,damping.json,runs/}` (spec pre-registered at
`5a7f28b`) · PR-12 🔒 R-ii · PR-3 §A eval protocol. **Open flags:** [CITE-D-LinOSS]; figure F6 ▢.

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
box: near-chance performance at light damping ($r = 0.2$: SER 0.39) falling to $1.3\times10^{-3}$
at the optimum — which sits at **deep overcoupling** ($r^* = 2.0$, $\kappa_\text{net} \approx
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
