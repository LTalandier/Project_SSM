# §6 — Choosing the damping operating point

**Status:** DRAFT v1 (2026-07-08, single-session mode — not independently reviewed; disclosed).
**Sources of record:** `results/s0_6/{damping.md,damping.json,runs/}` (spec pre-registered at
`5a7f28b`) · PR-12 🔒 R-ii · PR-3 §A eval protocol · PR-18/S0.11 at-solution diagnostics
(reg. `b585623` pre-run; `results/s0_11/`). **Open flags:** [CITE-*] keys resolved via `paper/references.md`; figure F6 = `paper/figures/F6_damping.*`.

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
every five symbols wrong) falling to $1.3\times10^{-3}$ at the optimum — which sits at **deep overcoupling** ($r^* = 2.0$; measured
operating $\kappa_\text{net} = 3.7\kappa_i$ at the converged solutions, the fixed-gain
estimate being $4.1\kappa_i$; about 6 samples of memory at 2 GS/s). The direction is instructive: the
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

**Why the pin loses: controllability at the solutions (PR-18).** A pre-registered diagnostic
(PR-18; S0.11) reproduced both arms' converged states bit-identically (16/16 seed-runs,
eval-trace-exact) and re-ran the S0.4-0 controllability gate *at the solutions* rather than at
θ₀. The uniform pin pays for its damping in gradient reach: at $r^* = 2.0$ only **20 of 32**
rings keep gradients above the registered $10^{-3}$-of-max gate — the three inter-tap interior
segments (rings 6–9, 15–18, 24–27) go gradient-dark (worst ratio $5\times10^{-7}$), and the
trained couplings do not rescue them (converged $\mu$ median exactly at its $0.3\kappa_i$
init; no link grows past $0.35\kappa_i$). The boxed winner escapes the trade: every seed
converges to the *same* structure — the four **driven** rings damped hard ($r \approx 1.3$)
and the 28 undriven rings held light ($r \approx 0.7$, operating
$\kappa_\text{net} \approx 1.5\kappa_i$) — which keeps **30 of 32** rings above the gate
(worst $2.3\times10^{-4}$; the two residual dark rings sit at segment midpoints) while still
damping where the input lands. The heterogeneous profile above is therefore not an
overparameterization curiosity: it is the mechanism by which the trained substrate buys
task-optimal damping *and* its own trainability at once — a combination a uniform design
value structurally cannot express, and a second, sharper reading of the ×2.5
pinned-vs-trained gap. The structure is not an artifact of this arm: the bake-off's winning
routes converge to the same tap-heavy profile at their solutions (§5.7), and a registered
taps-only control bounds how much of the performance the structure's interior carries —
real but thin (§5.7): "discovers" survives its own falsifier, narrowly. (Settled-amplitude participation decouples from gradient reach at the
solutions — winner counts $\{8, 15, 22\}$ of 32 above $\{10^{-1}, 10^{-2}, 10^{-3}\}$ vs
$\{4, 26, 32\}$ at θ₀ — the trainability-relevant quantity is the gradient gate; both are
reported in S0.11.)

Two honest footnotes. The slow mid-grid configurations ($r = 0.3$–$0.5$) had not fully plateaued
at the training ceiling, so the ×300 spread is a budget-bounded statement — but both endpoints
and all winning configurations converged, and the R-ii verdict uses converged points only. And
the result recolors §5 slightly: a large share of what in-situ training accomplished in the
bake-off *is* finding the damping operating point (the θ₀ hold value, pinned, yields 0.038 —
seventy-seven times worse than the trained substrate). Since the offline baseline finds $r^*$ on
its calibrated model just as well (§5.5), the damping result strengthens the trainability story
without moving the advantage question. It also recolors §2's motivation: the optimum sits deep
in the heavily-damped regime, far from the weakly-damped near-conservative corner where the
oscillatory (LinOSS) parameterization is most distinctive relative to plain diagonal SSMs — on
this task class the substrate's results are evidence about the broader dissipative
diagonal-SSM class that §2.2 deliberately claims, with LinOSS as its boundary case, not
evidence for LinOSS-specific expressivity.

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
a longer ISI to cancel) remains the right probe.

That probe has since run (PR-19; S0.12, post-assembly): a spread-spectrum task whose
decisions integrate 31 chips — a span far beyond the 8-lag head's reach — with the
registered prediction that the optimum moves light ($r^*_D \leq 1.0$). The prediction
**failed by degeneracy**: at the frozen SNR the task's integration gain leaves every grid
point at zero error — even $r = 3$, whose ~5-sample memory the mechanism said should be
fatal, clears on partial-correlation margin — so the separation rule could not fire
(ledger §19.6b). Two facts survive the floor. The trained actuator structure is
*task-dependent*: on T-D every arm stays at its initialization (taps $\approx 0.34$,
interior $\approx 0.30$; eight seeds plus the pilot) where T-A drove its taps to
$\approx 1.3$ — a reading itself bounded by the floor, since at zero error the gradients
vanish early and freeze the parameters where they stand. And the damping-tracks-memory
hypothesis now stands at zero for three: two informative nulls (T-A, T-A-L) and one
degenerate (T-D). We leave it as a hypothesis this substrate has three times declined to
confirm.
