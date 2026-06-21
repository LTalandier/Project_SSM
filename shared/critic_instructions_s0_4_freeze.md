# Critic instructions — S0.4 freeze packet phase-boundary review (the bake-off fairness contract)

**Filed:** 2026-06-17 (Supervisor). **Target:** the four **PROPOSED blocks at the end of
`shared/preregistration.md`** — **PR-6** (fairness contract, CRITICAL), **PR-7** (cost metric),
**PR-5** (PAT twin-mismatch; structure-now/levels-recon-deferred), and the **PR-12 R-ii
disposition**. These govern S0.4 (the four estimators: SPSA · PAT · recurrent in-situ adjoint ·
RHEL) and the S0.5 bake-off on the frozen PR-4 substrate.
**Output:** `shared/critic_review_s0_4_freeze.md`; verdict APPROVE / APPROVE-WITH-EDITS / AMEND /
REJECT, findings tagged **P6-F#** with severity (CRITICAL / HIGH / MEDIUM / LOW). **You report to
Lucas** (who signs after your review), not to the Supervisor.

## Why now
PR-4 (substrate) is signed and built (S0.3-1 + S0.3-1b, 128/128). The next runs are the bake-off
estimators. PR-6 is the **CRITICAL** pre-registration — it defines what makes the four-method
comparison apples-to-apples. Lucas ruled the three open gating questions on 2026-06-17:
**(1)** gain `saturating` for all four estimators; **(2)** κ_ext **clamp A** (a δ-/M1-validity-aware
r_min rule); **(3)** PR-12 **R-ii** (D-LinOSS damping is a distinct trainable-net-loss knob at fixed
g_f=0.9). The packet encodes these. This review is the gate before signature.

## Evidence base — read first (self-contained; assume no Supervisor context)
- The **PROPOSED PR-6/PR-7/PR-5/PR-12 blocks** (end of `shared/preregistration.md`) — the targets.
- **Frozen PR-4 v2** §G (gain M1/saturating, ceiling, validity (i)–(iii)), §K (K4 κ_ext policy,
  bounds [0.1,3], θ₀=0.3), §N (O2 normalization, E₀, power stationarity), §S (splitting), and the
  anchor-risk register — PR-6/7 cross-reference these heavily; verify the cross-refs are faithful.
- **Frozen PR-2 v2** — the partition P2 {δ, κ_ext, μ}, the R2 intensity readout, the **data regime +
  init ownership** (PF-F8a/b: "init distributions registered at PR-6"; "reference default μ(0)=0"),
  the reservoir baseline. PR-6 §B *changes* the μ(0) default — judge whether that is legitimate
  delegated authority or a silent override of a frozen block.
- The **Critic S0.3-1 review** `shared/critic_review_s0_3_1.md` (findings S31-F1 gain-mode HIGH,
  S31-F2 μ(0)=0 signal-starvation HIGH, S31-F8 sweep recipe) — PR-6 claims to discharge these.
- `shared/decisions_needed.md` **D-2026-06-13-1** (the lasing finding + the resolved clamp A) and
  `shared/escalate_to_human.md` **E-2026-06-13-2** (the three rulings, verbatim).
- The substrate code behind the claims: `photonic_ssm/substrate/{dissipative_ring,gain,ase}.py`,
  `photonic_ssm/substrate/calibration.py`, `tests/test_substrate.py` (esp. the hardened `test_h` and
  the `gain_mode` paths). The S0.3-1b results entry in `shared/results_log.md`.
- The **roadmap S0.4/S0.5** sections + the proposal §2/§5.2/§5.3/§10 (PAT/SPSA-default guardrail; the
  offline-deploy and reservoir baselines; the systems-advantage split).

## Stance: adversarial. Three hostile readings to try to make stick
1. **"The contract is rigged for the photonic side / for one estimator."** Does any §A–§F choice give
   one method an edge — e.g. does `saturating`-for-all actually advantage the gradient methods (which
   see ∂g/∂κ_ext) over model-free SPSA (which only sees the forward), or vice-versa? Is the equal-HP-
   budget real or nominal (SPSA's perturbation scale is famously sensitive — does "equal number of
   trials" actually equalize tuning effort)? Does the connected init smuggle the answer in (μ_c=0.3κᵢ
   close to a good solution)?
2. **"The clamp/connected-init quietly change the claim or the registered physics."** Clamp A narrows
   the trainable κ_ext band from [0.1,3] to [r_min,3] — does that **shrink the K4 pole region the
   white-space claim needs** (W1: "trains pole positions")? Does the connected init μ(0)≠0 mean the
   recurrence is **not** trained from scratch — and is the "μ *is* trained, just from μ_c" defense
   honest, or does it concede the in-situ claim rests on a hand-set coupling? Is r_min being
   **measured at S0.4-0 rather than frozen now** a pre-registration hole (a tunable number that lands
   after the freeze) or a legitimate measure-then-addend (like PR-4's E₀)?
3. **"The freeze leaves tunable holes (F12)."** Anything decided in Executor code at S0.4-0/S0.4a
   instead of in these blocks is a pre-registration failure. Hunt: the exact δ-band (block says
   "pinned at signature" — is it actually pinned, or hand-waved?); the LR schedule / clip / c-grid;
   the validation cell used for HP tuning; the PR-5 numeric levels (deferred — is the *structure*
   genuinely freezeable without them, or does the deferral hide a load-bearing choice?).

## Checklist (work every item; say CONFIRMED / REFUTED / EDIT per item)

1. **Saturating-for-all integrity (PR-6 §A).** Verify against PR-4 §G that `saturating` is the
   freeze-mandated mode (the §G "differentiable function of the episode drive statistics, no detach"
   + §N-E6) and `fixed` is genuinely just a diagnostic. **Then attack the fairness consequence:** the
   four estimators see the *same* g(P̄), but do they see it *the same way*? SPSA perturbs κ_ext and
   the gain follows (1 forward = 1 episode); PAT/adjoint backprop *through* g(P̄). Is there any cell
   where the saturating response **helps the method that can see ∂g/∂κ_ext and hurts the one that
   can't** — i.e. does `saturating`-for-all, intended as the level field, actually encode a
   gradient-method advantage that should be reported as a finding rather than hidden? Check the ASE
   "fresh per pass, not shared across methods" convention (§A) — is *not* sharing noise the right
   fairness call (it is the physical one), and does it inflate SPSA's variance unfairly vs the
   gradient methods?

2. **The lasing finding + clamp A, re-derived (PR-6 §C; D-2026-06-13-1).** Reproduce the core claim
   from the code: in `saturating` mode at the connected (or current) init, κ_net crosses 0 at
   r*≈0.134 and is −0.318κᵢ at r=0.1 (run a rollout / evaluate `kappa_net` / `gain_rate_per_ring`).
   **Is the divergence real** — i.e. is the in-episode dynamics genuinely linear with the gain held
   fixed (so no in-rollout saturation clamps the runaway)? Then judge clamp **A vs B vs C**: is the
   Supervisor's argument sound that **B** (hard-cap g≤0.9κᵢ) adds an unregistered mechanism + kinks
   ∂g/∂κ_ext at θ₀, and **C** (soft barrier) cannot stand alone because the divergence is in the
   forward recurrence not the loss? Or is there a cleaner option the packet dismissed? **Attack the
   r_min rule**: are clauses (a) κ_net≥m_κ·κᵢ and (b) M1 §G(iii)-margin the right two constraints?
   Is m_κ=0.05 / Δr=0.02 defensible, or arbitrary? Is "measure r_min at S0.4-0 + addend" a hole?

3. **r\* inside M1 validity (PR-6 §C clause (b); Lucas's explicit requirement).** The packet claims
   that near threshold the build-up diverges (E₀∝1/κ_net², §N) so the M1 quasi-static margin §G(iii)
   erodes **before** κ_net hits 0, hence r_min may be governed by the M1-validity boundary r_M1 > r*.
   **Verify this is physically right** (does the saturating self-consistency actually let build-up
   diverge, or does saturation itself bound it?) and that the rule takes the **more conservative** of
   (lasing+margin, r_M1). Is the "clamp is a physical-validity bound, strengthening anchor-risk"
   framing legitimate or spin?

4. **Connected init vs the white-space claim (PR-6 §B; S31-F2).** Confirm μ(0)=0 signal-starves rings
   2..N (the S31-F2 mechanism — exactly-zero task gradient noiseless; zero-mean noise gradient with
   ASE) and that N=32 (C-2 headline) is the binding cell. **Judge the supersession**: PR-2 said
   "reference default μ(0)=0" but "registered at PR-6" — is PR-6 changing it *delegated authority* or
   a frozen-block override needing Lucas? **Judge the honesty framing**: is "μ is trained in situ from
   μ_c, W1 untouched" sound, or does the result now rest on a hand-set connected init that the paper
   must foreground? Is registering the μ(0)=0 cold-start as a *sensitivity row* sufficient, or must
   the cold-start failure be a headline caveat? Is μ_c=0.3κᵢ a defensible candidate, and is deferring
   its confirmation to the S0.4-0 smoke acceptable?

5. **PR-12 R-ii soundness (PR-12 block; RECONCILE 1).** Verify the knot: the coarse sweep varied g_f,
   but g_f=0.9 *is* PR-4 §G's operating point, so a g_f sweep contradicts signed PR-4. Is **R-ii**
   (damping = trainable net loss via κ_ext over the clamped box at fixed g_f=0.9) the right reading,
   or is **R-i** (subsume into §G, drop PR-12) actually cleaner? Does R-ii's "convergence-controlled
   rerun, ≥8 seeds" correctly fix the S0.3-1 anomaly-B confound (fixed-budget conflates accuracy with
   training speed)? Check the **PR-12/K4/PR-6 init-consistency** requirement is complete (init + δ-band
   + κ_ext-init + damping-sweep-range all inside [r_min,3]).

6. **Cost-metric integrity (PR-7) — the bake-off's load-bearing axis.** The PRIMARY score is
   **sample-efficiency-to-target-accuracy in device passes** (cosine-error is secondary-only and
   flatters the exact methods — confirm PR-14 keeps it confined). Attack the per-method table: is
   **SPSA=2 fwd, PAT=1 fwd (+twin-backward on the digital side-ledger), adjoint=2, RHEL=2** the right
   accounting? **Is putting PAT's twin-backward on the digital side-ledger rather than the device-pass
   count the honest call, or does it flatter PAT** (the method's whole efficiency claim rides on this
   split)? Is the batch convention (1 device pass = 1 sequence; efficiency in total passes not steps)
   unambiguous? Does the adjoint "charge 1 physical adjoint pass as if realizable" correctly quarantine
   debt #4 (the recurrent-adjoint gap) to the §5.2 hardware-slot question? Does RHEL's echo-penalty
   land in accuracy-per-pass (PR-11) and not get lost?

7. **PAT twin-mismatch honesty (PR-5).** Is the structure (M-par parametric / M-struct omission /
   M-noise) the right family set? **Is the headline "twin linearizes gain (fixed) while substrate
   saturates" a genuine, well-chosen omission** (it directly tests whether PAT absorbs the dropped
   ∂g/∂κ_ext = the S31-F1 quantity) — or is it too soft / too hard? Is the **calibration-error
   unification** (offline-deploy baseline's weight-mapping error drawn from the *same* M-par family)
   the correct apples-to-apples for the in-situ-vs-offline contrast the white-space claim leans on?
   Is freezing the *structure* now while the *numeric levels* ride an S0.4-0 recon legitimate (the
   menu-source-then-freeze discipline) or a pre-registration dodge? Name what the recon must source.

8. **F12 hole-hunt (completeness).** List every value a downstream run needs that these blocks do
   **not** pin: the explicit δ-band numbers; the LR schedule + clip value + SPSA c-grid; the HP-tuning
   validation cell; seed lists; the target-accuracy definition feeding "to-target" (is it PR-3's
   ceiling-relative rule, whose *rule* must freeze before S0.4 close — is that dependency stated?).
   For each: is it correctly deferred-with-owner, or a silent hole?

9. **Guardrail + debts.** Does the packet preserve the **PAT/SPSA-default guardrail** (proposal §5.2:
   the chip stays on PAT/SPSA; adjoint/RHEL earn a hardware slot only by clearly beating them — PR-9,
   not here, but check PR-6/7 don't pre-bias it)? Does anything here touch the **four debts** (#1
   sharpened white-space — see attack 2; #2 LinOSS benchmark transfer; #3 Er:SiN NF; #4 recurrent-
   adjoint gap — see item 6)? Does the **M3-trigger-margin pointer** (PR-7 §E → PR-9) correctly honor
   PR-4 §G's "frozen with PR-5–9/PR-11 before any bake-off results"?

## Expected output
`shared/critic_review_s0_4_freeze.md` — verdict + numbered **P6-F#** findings with severity, each
CONFIRMED/REFUTED/EDIT, load-bearing claims independently re-derived from the code where checkable
(esp. items 2, 4). If you would not sign, say which finding is signature-blocking and what the
one-pass revision is.

Launch the Critic (separate terminal):
```
cd ~/Documents/Project_SSM
claude "Read shared/critic_instructions_s0_4_freeze.md and follow it."
```
