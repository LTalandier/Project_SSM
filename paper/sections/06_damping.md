# §6 — Choosing the damping operating point

**Status:** v2, condensed 2026-09-29 for the first public deposit (v1 at commit `a508a28`).
At-solution and memory-task detail moved to supplementary N9.6.

---

The D-LinOSS observation that damping in an oscillatory SSM is a *performance knob* has a direct
physical meaning here: per-ring damping is the net loss $\kappa_\text{net}(\kappa_\text{ext})$,
set by a coupler already in the trained partition. The registered disposition (R-ii) therefore
asks whether training *finds* the right damping inside the feasible box. Two arms, six damping
points and eight seeds each were run at the headline cell under convergence control.

**The damping value matters enormously.** With $\kappa_\text{ext}$ *pinned*, so that only
detunings and inter-ring couplings train, the converged error spans a factor of ~300 across the
box: SER 0.39 at light damping ($r = 0.2$; chance on 4-PAM is 0.75) down to $1.3\times10^{-3}$ at
**deep overcoupling**, $r^* = 2.0$ (measured $\kappa_\text{net} = 3.7\kappa_i$ at the converged
solutions, about 6 samples of memory at 2 GS/s). The task needs only a 7-tap span, and the 30–45
samples of memory supplied at light damping are harmful because stale symbols interfere. Damping
tunes memory to the task class, with the optimum on the heavily damped side.

**Training absorbs the knob.** When the full partition trains inside progressively wider boxes
$[r_\text{min}, r_\text{hi}]$, every box containing the pinned optimum reaches $5\times10^{-4}$, the
§5 reference, *better* than the best uniform pin; boxes that exclude the good regime fail. R-ii is
confirmed: the designer must make the box contain the good regime, and the trained substrate sets
the operating point. The mechanism is controllability at the solutions (PR-18; §5.7). The uniform
pin leaves the three inter-tap interior segments gradient-dark, with only 20 of 32 rings above the
gate. The boxed winner damps the four driven rings hard ($r \approx 1.3$) and holds the 28 undriven
rings light ($r \approx 0.7$), keeping 30 of 32 rings trainable. Heterogeneous damping buys
task-optimal damping and trainability at once, which no uniform design value can express.

Two qualifications. The slow mid-grid configurations ($r = 0.3$–$0.5$) had not fully plateaued,
so the ×300 spread is budget-bounded, although both endpoints and every winning configuration
converged and the verdict uses converged points only. And much of what in-situ training does in §5
is finding this operating point: the θ₀ hold value, pinned, yields 0.038, seventy-seven times
worse than the trained substrate. The offline baseline finds $r^*$ on its calibrated model just as
well, so this strengthens the trainability result without moving the advantage question. The
optimum also sits far from the weakly damped corner where the LinOSS parameterization is most
distinctive, so on this task class the results are evidence about the broader dissipative
diagonal-SSM class claimed in §2.2, not about LinOSS-specific expressivity.

**Does the optimum track task memory? A registered prediction, failed.** Because "excess memory is
harmful" on one 7-tap task is close to tautological, we froze a transfer test (PR-17): task T-A-L
adds a −6 dB replica of the channel's past-tap profile delayed by 7 symbols, doubling the memory
span to 14, with the prediction that the optimum moves to lighter damping ($r^*_L < 2.0$) under a
30%-separation rule. **The prediction failed.** The error keeps falling to the heavy edge of the
grid ($2.2\times10^{-3}$ at $r = 3$ vs $2.5\times10^{-3}$ at $r = 2$, eval-F, within 13%; Fig. F6,
dashed); the harder task raised the floor everywhere and left the optimum in place. On this
substrate the heavy-damping optimum is robust to a ×2 change in memory span, set by the
bandwidth/interference trade of the equalization family rather than by span matching. A second
probe (PR-19), a spread-spectrum task whose decisions integrate 31 chips, predicted
$r^*_D \leq 1.0$ and **failed by degeneracy**: at the frozen SNR every grid point reached zero
error, so the separation rule could not fire, and every arm ended near its initialization. The
damping-tracks-memory hypothesis therefore has one informative null and one degenerate attempt
against it; we leave it as a hypothesis that one probe declined to confirm and a second could not
reach (N9.6).
