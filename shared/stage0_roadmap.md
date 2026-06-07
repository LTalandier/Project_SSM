# Stage 0 Roadmap — Theory + Simulation (incl. the four-method training bake-off)

**Owner:** Supervisor. **Status:** draft v2 (2026-06-06, aligned to proposal **v0.5**), awaiting Lucas's
go + Critic review of the plan.
**Source of truth:** `photonic-ssm-proposal-v0_5.md` §6 (Stage 0), §3 (mapping), §4 (pole region),
§5 (training), §7 (gain), §10 (advantage). This roadmap decomposes Stage 0 into executable phases; it
adds no scope beyond the proposal without a decision logged in `decisions_needed.md`.

> **v0.5 reframing (vs the v0.2 plan this file replaced).** Platform is **silicon nitride (SiN)**, not
> TFLN. Training is a **four-method bake-off** — SPSA, PAT, recurrent in-situ adjoint, RHEL — on **one
> shared dissipative ring model**, with **PAT/SPSA the hardware-committed primary** and the two exact
> methods evaluated *in simulation only* ("parallel in simulation, singular in hardware"). The primary
> score is **sample-efficiency-to-target-accuracy under realistic noise**; gradient-cosine-error is a
> **secondary diagnostic only**. Damping is now a **free knob** (no conservatism tension). A
> **systems-advantage envelope** is an explicit deliverable.

## Goal of Stage 0

Produce, with **no fabrication**, the deliverables that gate the program:
1. an oscillator↔SiN-ring **mapping** result + realizable pole-region bound;
2. **a comparison of in-situ training methods** (the bake-off) for an oscillatory photonic recurrence
   under realistic loss/gain/ASE — publishable in its own right, and the RHEL-on-SiN finding that
   anchors any collaboration outreach;
3. the **damping/accuracy curve** (D-LinOSS operating point);
4. a **first-pass systems-advantage envelope** (latency/energy incl. E/O–O/E + DAC/ADC overhead vs a
   digital baseline on the target low-latency task).

And clear the two gates:
- **Gate (i):** model reproduces oscillatory-SSM task accuracy within a **pre-registered margin**.
- **Gate (ii):** at realistic SiN noise, **≥1 method trains to the pre-registered accuracy** — with
  **PAT/SPSA the default hardware choice regardless**. Promote the adjoint or RHEL to a hardware slot
  *only if* the bake-off shows it clearly beats PAT/SPSA on a metric that matters (exactness, scaling,
  or hardware simplicity).

## Phase decomposition

> Ordered by dependency. Each is a `task_queue.md` task gated by a Critic review before dependents
> start. Seeds: 4 min, 8+ for high-variance. The four estimators **share one substrate model** (S0.3)
> so the comparison is apples-to-apples.

### S0.0 — Repo + tooling fork + smoke test
- **Do:** stand up the Project_SSM repo; fork from `pnn-multilayer` the ring/MRR forward model, the
  differentiable/batched training engine, and the gain/SOA + thermal-crosstalk tooling (the latter now
  directly on-point for SiN thermo-optic tuning + SPSA crosstalk-robustness). Self-contained.
- **Deliverable:** runnable repo; `physics`-level smoke test (one SiN add-drop ring → its Laplace pole,
  matched to the analytic transfer function); `requirements.txt`; `README` of forked-vs-new.
- **Gate:** smoke test matches the single-ring analytic reference within a stated tolerance.

### S0.1 — Oscillator↔SiN-ring mapping + realizable pole region
- **Do:** formalize proposal §3 (ring pole $s=-\kappa_\text{tot}+i\omega_\text{res}$ ↔ eigenvalue
  $a_i=-e^{\alpha_i}+i\beta_i$); implement a coupled-ring → $N$-oscillator LinOSS forward model; bound
  the pole region per §4 (stability free; **memory loss-limited** → low-loss SiN maximizes passive
  memory; FSR-bounded $\beta_i$; poles placed by drift-stable thermo-optic trim).
- **Deliverable:** mapping write-up (Supervisor) + verified forward model (Executor) + plotted pole
  region with the loss/gain → $|\lambda|$ (memory-length) relation.
- **Gate:** model poles match a coupled-mode/transfer-function reference within tolerance.

### S0.2 — LinOSS / D-LinOSS digital baseline (Gate i)
- **Do:** implement LinOSS (stable for nonnegative-diagonal $A$ → dissipative ring lattice in-regime)
  and D-LinOSS (learnable damping); reproduce a long-range / time-series benchmark within a
  **pre-registered margin** set *before* the run. Resolve verification debt **#2** (LinOSS/D-LinOSS/
  Mamba-3 specifics) here.
- **Deliverable:** baseline accuracy table + the pre-registered margin + the target task for the bake-off.
- **Gate (= Gate i):** idealized oscillatory-SSM accuracy within the pre-registered margin.

### S0.3 — Shared realistic dissipative ring substrate model
- **Do:** build the **single substrate** all four estimators train through: finite $Q$ / round-trip
  loss, erbium (or III-V) gain saturation, and **injected ASE**. Conservative NF assumptions (the
  flagship Er:SiN device has **no published NF** — verification debt #3). Parametric in loss/gain/ASE.
- **Deliverable:** documented substrate model with named, cited parameter ranges; unit tests (zero-noise
  limit recovers the S0.1 forward model).
- **Gate:** substrate reproduces expected limits; one knob each for loss, gain, ASE variance.

### S0.4 — Implement the four in-situ-training estimators (on the shared substrate)
Sub-phases (RHEL is split out because of its extra echo-modelling cost):
- **S0.4a — PAT + SPSA (the hardware-committed workhorses).** PAT: forward on the substrate (unrolled),
  backward on a differentiable digital twin; characterize twin-mismatch bias. SPSA: gradient of all
  params from **two physical forward passes**, model-free; verify it absorbs injected noise + crosstalk.
- **S0.4b — Recurrent in-situ photonic adjoint.** Time-domain/cavity extension of feedforward adjoint
  (Hughes/Fan/Pai lineage); solve adjoint-field interaction with gain and (under dynamic drive)
  non-reciprocity. SiN-friendly (clean low-loss interference sharpens the gradient).
- **S0.4c — RHEL + concrete optical-echo sub-model.** Implement RHEL on the LinOSS oscillator **and**
  the echo's physical primitive honestly: a **specific phase-conjugation mechanism** (e.g. a defined
  χ³ FWM scheme with real pump-power, bandwidth, conversion-efficiency, added-noise penalties) — or an
  explicit **off-chip / non-SiN admission** — plus a conjugation-fidelity + systematic-error term on
  top. **No idealized conjugation operator** (it would let the bake-off promote RHEL on a primitive SiN
  may not deliver). Note the irreducible ASE-irreversibility floor (§5.2).
- **Gate:** each estimator runs on the shared substrate; idealized/zero-noise sanity checks pass (e.g.
  adjoint & RHEL → BPTT as the relevant limit is taken — used as a *floor check*, not the headline metric).

### S0.5 — The bake-off (the headline Stage-0 result + Gate ii)
- **Do:** run all four estimators **+ the baselines** (offline-train-deploy; reservoir-readout, §5.3)
  on the shared substrate as loss/gain/ASE are swept. **Primary metric: sample-efficiency-to-target-
  accuracy under realistic noise** (does it reach the S0.2 pre-registered accuracy, and at what cost in
  physical forward passes). **Secondary diagnostic only: gradient-cosine-error vs a BPTT reference**
  (state explicitly it flatters adjoint/RHEL and penalizes SPSA — never use it as the headline).
- **Deliverable:** the **in-situ-training-method comparison under realistic loss/gain/ASE**, incl. the
  concrete RHEL-on-SiN finding.
- **Gate (= Gate ii):** ≥1 method reaches the pre-registered accuracy at realistic SiN noise. **PAT/SPSA
  is the default hardware route regardless;** record whether adjoint or RHEL *clearly* beats it on a
  metric that matters → candidate for a *later* hardware slot (Stage 3). *If SPSA variance is
  prohibitive at the target parameter count → lean on PAT, reserve SPSA for fine-tuning (risk #2).*

### S0.6 — Damping operating point (D-LinOSS)
- **Do:** sweep the damping knob purely **for accuracy** (no conservatism constraint anymore); pick the
  operating point. The v0.2 "conservatism–damping frontier" framing is retired.
- **Deliverable:** the damping/accuracy curve + a recommended operating point.
- **Gate:** a defensible operating point identified (or a documented "damping-insensitive" result).

### S0.7 — Systems-advantage envelope (§10 deliverable)
- **Do:** pick the target low-latency niche; write the **end-to-end latency/energy budget including
  E/O–O/E and DAC/ADC conversion overhead**; compare to a digital baseline on the same task.
- **Deliverable:** first-pass advantage envelope. **If even the optimistic envelope fails to clear
  digital, that is a pre-MPW-spend finding** — escalate to Lucas (§10: the load-bearing un-audited premise).
- **Gate:** envelope exists and states whether an advantage window plausibly exists.

### S0.8 — Write-up
- **Do:** Supervisor assembles the Stage-0 outputs: mapping result + bake-off comparison + damping curve
  + advantage envelope. Resolve the framing of verification debts **#1** (sharpened white-space) and
  **#4** (recurrent-adjoint gap) in the text.
- **Deliverable:** arxiv-ready Stage-0 manuscript(s); the finding to take to a potential collaborator.

### S0.L — (parallel) Literature / verification-debt track
- **Do:** re-verify the four debts against primary sources, dated memos with citations:
  1. **white-space** — sharpened Gap-2 form: *recurrent parameters (pole positions + inter-ring
     couplings) updated on the physical device by gradient-based/-estimating training, never done.*
     Pre-empt: reservoir computing (fixed recurrence), the Bueno/Brunner photonic-RNN RL line (trains
     readout by reward), internal-param reservoir variants (no gradient training of the recurrence).
  2. **LinOSS / D-LinOSS / Mamba-3** benchmark specifics.
  3. **Er:Si₃N₄ noise figure** (flagship device unmeasured).
  4. **recurrent-adjoint gap** (inferred from absence of demonstrations; confirm).
- **Deliverable:** one short memo per debt; feeds S0.8.

## Dependency graph
```
S0.0 ─▶ S0.1 ─▶ S0.2 (Gate i)
                 └─▶ S0.3 ─▶ S0.4{a,b,c} ─▶ S0.5 (Gate ii, headline) ─▶ S0.6
                                                                          └─▶ S0.7 ─▶ S0.8
S0.L runs in parallel and feeds S0.8.   (S0.7 advantage envelope can also start earlier, in parallel.)
```

## Decision gates owned by Lucas
- Approve this roadmap + the pre-registered margins (S0.2) before the runs that test them.
- Gate (ii) outcome → proceed to Stage 1 on **PAT/SPSA**; whether to reserve a Stage-3 hardware slot for
  adjoint/RHEL.
- The S0.7 advantage-envelope verdict → whether the §10 premise justifies MPW spend (fallbacks §5.3:
  offline-deploy, reservoir-readout).
