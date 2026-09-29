# §9 — Outlook: Stage 1

**Status:** v2, condensed 2026-09-29 for the first public deposit (v1 at commit `a508a28`).

---

## 9.1 Hardware development paused

The inline kill gate (§7.4) closes the registered product route, and no wafer or
product-development spend is planned. A later exploratory study of a low-Q ring regime, registered
in the same ledger (PR-22, PR-23), found no validated energy window either; it is not part of this
paper's results. What follows describes a possible collaborator-led research demonstrator, not a
fabrication plan.

The bake-off fixes that demonstrator's training stack by evidence: **PAT and SPSA, nothing else in
the loop.** Neither exotic route earned promotion (§5.3), and the hardware ledger (supplementary
N2) shows why hardware grounds are unlikely to reverse that: the adjoint adds circulators,
phase-coherent reverse injection and an unsolved separation of the counter-propagating field from
the backscatter doublet, and RHEL adds a pumped conjugator bank whose ≈9.6 W budget at 32 rings
exceeds the rest of the system. The minimal demonstrator is the §3 plant with 8–32 rings
(foundry-floor Q suffices, per C-1's gate), thermo-optic $\{\delta, \kappa_\text{ext}, \mu\}$
actuation, one drop-port readout chain, the four-tap drive map of §3.6, SPSA as the first-light
route and PAT once the twin is characterized to the 5%-class accuracy the mismatch protocol
assumed. SPSA runs under the δ-aware clamp $r \geq 0.2547$ from the start, because its solutions
are the ones that approached the hypothetical super-threshold corner (§3.6). The registered cells
are foundry-realizable, with C-2 bounded by a demonstrated multi-project-wafer result
[CITE-Cui-2023], and the actuation uses standard thermo-optic tuners.

## 9.2 What would change our mind

Three pre-registered forks. (i) **Adjoint promotion**: if a physical recurrent reverse pass is
demonstrated (debt #4), the PR-9 criterion reopens with these data as prior; the simulation
predicts ceiling-grade accuracy at 2× PAT's device passes and zero digital cost. (ii) **The in-situ
advantage**: with no resolved calibration difference across 5–30%, in-situ training earns a place
on hardware only through a measured differential. Independent drift is the modelled candidate, and
the experiment should be designed to measure it on one chip, offline-deploy against PAT/SPSA arms,
rather than assume it; mismatch beyond the tested grid and total training energy remain
unresolved. (iii) **RHEL**: nothing on SiN. The idealized-conjugator control shows a perfect echo
contributing ≈0 through the recurrence (§5.4), so reopening it needs a conservative platform
regime, not a better conjugator.

## 9.3 Beyond the linear unselective core

The frozen architecture is the unselective linear time-invariant core — poles and couplings, the
part photonics builds natively. Input-dependent dynamics in the Mamba direction [CITE-Mamba] would
map onto the same lattice as input-dependent $C$ and then $B$ actuation, behind its own gate;
nothing in this paper depends on it.

## 9.4 Closing

The program asked a narrow question with unusual bookkeeping: can the physics of a dissipative
photonic recurrence be trained through itself, and at what honest cost? In simulation, under
pre-registered thresholds, yes — by the two methods a chip can already run, at quantified
device-pass cost, with the exotic routes priced out by data and the independent-drift advantage
bounded by its simulation assumptions. The function-matched inline envelope is negative within the registered window. A chip
would test physical trainability, but these results do not justify product development or
fabrication spend.
