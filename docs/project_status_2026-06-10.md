# Project_SSM — Where we stand (2026-06-10)

*Point-in-time summary written by the Supervisor for Lucas at the pre-S0.2 continuation gate.
Plain-language companion to the authoritative sources: `photonic-ssm-proposal-v0_5.md` (the
science), `shared/stage0_roadmap.md` v3.1 (the plan), `shared/preregistration.md` (the frozen
rules and numbers). Repo head at writing: `2ecf335`.*

---

## 1. What this project is

We are trying to demonstrate the **first recurrent photonic system whose recurrence is trained on
the physical device** — a bank of coupled silicon-nitride microrings that acts as a state-space
model (an "SSM", the LinOSS/S4D family of machine-learning models), where the parameters that
*define* the recurrence (each ring's resonance and damping = the model's poles; the inter-ring
couplings) are updated by gradient-based training **with the chip itself in the loop**. Nobody has
done this for any recurrent photonic system, by any method — that claim has now been adversarially
searched and survives (see §3).

We are in **Stage 0**: theory and simulation only. No chip, no fabrication commitment, no cloud
compute. Stage 0's product is (a) the physics mapping, (b) a four-way "bake-off" of candidate
in-situ training methods on one shared realistic ring model, and (c) an honest answer to "would
this beat digital electronics at anything, once you pay for converting signals between the
electrical and optical worlds?" Stage 0 alone yields a methods paper; the headline "first" is only
collectible later, on hardware (Stage 1+).

## 2. What has been done (chronological)

| When | What | Outcome |
|---|---|---|
| 06-07 | **S0.0a** tooling recon | The old `pnn-multilayer` ring code is static (no dynamics) and its trainer is MZI-specific — the SSM core must be new code. 7 reusable assets identified. |
| 06-08 | **S0.0** repo + salvage | Repo stood up; 7 assets ported with provenance (SPSA trainer, gain/ASE, dynamic SOA, platform registry, static rings as test references, ridge readout, sweep runner). All tests green. |
| 06-08/09 | **S0.1 (+S0.1.1)** ring↔SSM mapping | **Gate PASSED.** Dynamical coupled-ring model validated against analytic references (99 tests). One ring = one trainable complex pole (S4D/DSS class; LinOSS is the uncoupled special case). Ring memory: 3.3 ns (329 round trips) at the conservative foundry corner → 49.4 ns (≈4 900 rt) at the class-leading corner. Surprise finding: backscatter mode-splitting is roughness-limited, not Q-gated → now a registered model knob. |
| 06-09 | **D-09-1** re-plan | The two existential risks were pulled *forward*, before any bake-off effort is sunk: the novelty kill-search (S0.L-1) and an early systems-advantage envelope (S0.7-lite). Both now feed one **continuation gate** (this decision). |
| 06-09/10 | **S0.L-1** novelty kill-search | 80+ papers / 74 candidates, two independent search modalities (Executor sweep + Critic blind pass). **0 fatal priors** under the pre-registered kill-rule, which you amended (PR-15.1) and signed when both modalities exposed the same defect in it. The one serious threat (Wu 2025, on-chip optical RNN trained by SPGD) is contained by the adopted claim wording **W1**; Zhao 2025 you resolved non-fatal from its figures (feedforward network — no recurrence). Verdict: **provisional one-sided PASS** (a clean search can't *prove* novelty; a dated re-sweep rides the paper write-up). |
| 06-10 | **S0.7L-0 → PR-10 freeze** | Every envelope assumption primary-sourced (~35 documents); 4 bad legacy numbers caught and banned; you froze the assumption set (PR-10) before the arithmetic ran. |
| 06-10 | **S0.7L-1** systems envelope (lite) | **Conditional POSITIVE** — details in §4. The §10 "abandon-the-premise" clause does **not** fire. |
| 06-10 | **Critic audit** of the envelope | **APPROVE-WITH-EDITS; the verdict survives.** Independent clean-room recompute reproduced every cell. Caught one Supervisor error (a false robustness assurance — corrected; the corrected statement is *more* favorable) and several wording/coupling fixes, all folded in. |

## 3. Kill-shot A — "is the claim still ours?" → provisional PASS

The load-bearing sentence: *recurrent parameters — pole positions and inter-resonator couplings —
updated on the physical device by gradient-based/-estimating training, against a computational
task.* A prior demonstration kills the project's headline.

- The kill-rule (what would count as fatal) was **frozen before searching** and amended once,
  with your signature, when both search modalities independently found the same hole (regulation/
  calibration loops — e.g. locking a filter — mechanically satisfied the old rule; the amendment
  requires a *task* objective).
- Result: **nothing fatal found.** The near-misses are now assets: a lineage section (decades of
  photonic servo/locking), boundary citations (Böhm's hybrid digital recurrence), and a sharpened
  gap statement — Zhao proves *feedforward* in-situ optical backprop on microrings exists, which
  makes "the *recurrent* version has never been done" sharper, not weaker.
- Adopted claim wording, **W1**: "first continuous-time dissipative-resonator recurrence — pole
  positions + inter-resonator couplings — trained in situ by gradient-based/-estimating methods on
  a computational task." True under *both* readings of the one ambiguous prior (Wu). The broader
  W0 stays reclaimable if Wu's ambiguity ever resolves our way (outreach to the authors: held, per
  your ruling — "maybe later").
- Still open, deliberately non-blocking: three full-texts (NTT, Fisher 1987, Shi) to read before
  the paper's wording freezes — all carry documented non-fatal leans.

## 4. Kill-shot B — "is it worth building?" → conditional positive (audited)

The envelope charges the photonic SSM its *full* conversion stack (lasers excluded but listed:
modulator, photodetector, DAC, ADC, heater holding power) and compares energy per processed sample
against three named, well-implemented digital baselines — across optimistic/conservative component
corners, two heater technologies, N = 8–128 rings, 0.1–2 GS/s sample rates.

**The positive:** at GS/s rates the photonic side clears the published FPGA recurrent-serving
anchor (Microsoft Brainwave) by up to **14.7×** on energy, and sub-microsecond latency is simply
unreachable for that serving class (<4 ms published, vs tens of ns photonic; honest matched-size
contrast ≥100×). Conversion cost is paid **once per sample regardless of N** (one optical
carrier), while digital cost grows with N — so margins *grow* with model size.

**The conditions (post-audit, all four carried into upcoming pre-registrations):**
1. With conservative (vendor-part) converters, the advantage needs **suspended low-power heaters**
   — which our named foundry flow (CORNERSTONE) does not offer. With hero-class converters,
   standard foundry heaters suffice above ~1.3–1.5 GS/s at expected holding power. Either way this
   is the principal **Stage-1 fab condition**, not a Stage-0 blocker.
2. The niche lives at **≥~0.5 GS/s** (below that, heater holding power dominates and the
   conservative ring's memory is shorter than one sample anyway).
3. An embedded GPU's *peak* efficiency is never beaten — our case rests on the measured fact that
   such GPUs sustain <13 % of peak on this workload class. A measured sustained number is the one
   retrieval that could still hurt, queued for the full S0.7.
4. The large-N margins assume the high-Q platform corner (which is the splitting-prone one — goes
   to the PR-4 decision) and a single-quadrature/intensity readout (goes to the PR-2 readout pin).

**Verdict semantics:** assumption-driven, *not* load-bearing for any external claim — but the
"even the optimistic corner loses everywhere" escalation clause **did not fire**, which is what
this gate needed to know. Identified niche: **GS/s streaming signal processing (equalization
class), N ≈ 32–128, sub-µs latency** — this directly sizes the bake-off task choice.

## 5. The decision now on the table (E-2026-06-10-3)

**GO / NO-GO on the bake-off arm, S0.2–S0.5:**

- **S0.2** — digital LinOSS/D-LinOSS baseline + bake-off setup; freezes PR-1/PR-2 (task choice
  sized to the niche above; architecture; readout pin; W1 claim wording). Tests Stage-0 Gate (i).
- **S0.3** — the shared realistic dissipative ring substrate (finite Q, gain saturation, ASE,
  splitting knob); freezes PR-4 (operating Q, roughness, the N⇄Q⇄splitting coupling, holding
  convention).
- **S0.4** — the four training estimators on that one substrate: PAT, SPSA (the
  hardware-committed pair) + recurrent adjoint, RHEL with a concrete phase-conjugation echo
  sub-model (simulation-only contenders).
- **S0.5** — the bake-off itself; primary metric **sample-efficiency-to-target-accuracy under
  realistic noise** (pre-registered; gradient-cosine is a secondary diagnostic only). Tests
  Gate (ii): ≥1 method trains to the pre-registered accuracy at realistic SiN noise.

Then S0.6 (damping operating point), S0.7-full (envelope with the lite gaps closed), S0.8
(write-up + dated novelty re-sweep). All of it local simulation — no fab, no outreach, no cloud
spend without a separate escalation.

**Supervisor recommendation: GO.** Both kill-shots cleared at the level Stage 0 can test them; the
downside of GO is local simulation time; the bake-off's methods value survives even if the niche
narrows; and the competitive window (the Wu/HUST group is active exactly here) is roughly one
publication cycle.

## 6. Open items not blocking this decision

- **For Lucas, paced to the claim-wording freeze (PR-2/S0.8):** NTT ADI 2025
  (doi 10.34133/adi.0121), Fisher 1987 (Appl. Opt. 26:5039), Shi LPR 2025 full-texts; the held Wu
  outreach ("maybe later" — draft ready in the session log).
- **Rides the next Executor task:** two one-line corrections in the results log + three memo
  sentences (Critic findings EV-F1…F5 — all folded into the decision record already).
- **Parked decisions, due at their pre-registrations:** D-08-1 operating Q (PR-4, jointly with
  splitting and the N=128⇄Q coupling); the PR-2 readout pin.
- **Standing verification debts:** #2 LinOSS benchmark transfer (validated in-house via the PR-3
  BPTT ceiling); #3 Er:Si₃N₄ noise figure (no published NF — Stage-1 relevance); #4 the
  recurrent-adjoint gap (now sharpened by Zhao); plus the S0.8 watchlist (9 items) and the B2
  primary-source pass.

## 7. How the work runs (and one process correction)

Three separate Claude Code sessions coordinate through `shared/`: **Supervisor** (methodology,
analysis, writing, task specs — no simulation code), **Executor** (code + runs + results), and
**Critic** (independent adversarial review, reporting to Lucas, not the Supervisor). Every
consequential rule or number is **frozen in `shared/preregistration.md` before the run it
governs**; ambiguous calls and money/scope decisions escalate to Lucas. Corrected on 06-10:
sessions are **launched by Lucas in separate terminals** — the Supervisor briefly ran the others
as background subprocesses, which undermined Critic independence and caused one working-tree
collision; that pattern is retired and the rule is in memory.

The audit trail of this whole period is in git (`a6de34f` → `2ecf335`), with every decision,
review, and result in `shared/` — nothing load-bearing lives only in a chat session.

## 8. Map of the repo

| Path | What's there |
|---|---|
| `photonic-ssm-proposal-v0_5.md` | The authoritative proposal (read first) |
| `shared/stage0_roadmap.md`, `task_queue.md`, `results_log.md` | Plan · task assignments · results |
| `shared/preregistration.md` | The frozen-rules ledger (PR-15/PR-15.1 kill-rule; PR-10 numbers; PR-2/PR-4 constraint notes) |
| `shared/escalate_to_human.md` | Decisions for Lucas — **E-2026-06-10-3 is the live one** |
| `shared/critic_review_*.md` | Critic verdicts (roadmap, S0.1, white-space, envelope) |
| `photonic_ssm/` + tests | The package: salvaged assets + the new dynamical ring/SSM core (99 tests) |
| `docs/s0_1/`, `docs/s0_L/`, `docs/s0_7/` | Memos: mapping + pole region · novelty search + claim wording · envelope + sources |
| `analysis/`, `results/` | Runnable analysis scripts and their outputs |
