# White-space claim — wording variants (Supervisor draft for the A1 ruling + PR-2 freeze)

**Author:** Supervisor · **Date:** 2026-06-09 · **Status:** DRAFT — feeds Lucas's A1 ruling
(E-2026-06-09-5) and the PR-2 wording freeze. Nothing here is frozen.
**Inputs:** PR-15 sweep + blind pass (E-09-3/E-09-4); B1 actuation map; `mapping_result.md`.

All variants carry the three qualifiers from the pending rulings, which are needed under **every**
outcome: **"on a computational task"** (q4 — excludes the servo/regime-tuning lineage), the
**parameter-physicality qualifier** (trained parameters are physical/analog degrees of freedom of the
photonic recurrence, with the recurrent state carried photonically — excludes Böhm-class hybrid-digital),
and the **weight-tied recurrence definition** (state carried across the input sequence — excludes
folded-in-time feedforward).

## W0 — broadest (the current claim)

> *The first physical photonic system whose **recurrent parameters** — the parameters defining its
> recurrence — are updated **on the physical device** by **gradient-based or gradient-estimating
> training on a computational task**.*

- **Killed by:** Wu eLight 2025 under its natural reading (if the recurrent W-mesh voltages are in the
  trained set U); Zhao LPR 2025 if its in-situ-trained MRR parameters form a weight-tied recurrence.
- **Survives:** the entire servo/calibration lineage (q4), Böhm (physicality), NTT CiW (weight-tying),
  Bueno/Brunner (readout-only, pending the boundary memo's hostile audit).
- **Use only if:** Wu resolves to readout/IO-only **and** Zhao clears. Highest value, highest fragility.

## W1 — dissipative-resonator scope (recommended hedge)

> *The first **continuous-time dissipative-resonator recurrence** — pole positions and inter-resonator
> couplings — **trained in situ** on the physical device by gradient-based/-estimating methods on a
> computational task.*

- **True under both Wu readings:** Wu's trained U drives an O/E/O wavelength-relay loop (its routing
  MRRs are calibrate-once-static); it does not train resonator poles/couplings. Wu is then cited loudly
  as the nearest neighbor (first in-situ-trained optical RNN of *any* kind, under its natural reading).
- **Exposure:** Zhao LPR 2025 is the remaining unknown (microring parameters trained in situ — if
  recurrent, it attacks W1 too; if a feedforward weight bank, it clears). Mak/Bois/Poon sits on the q4
  boundary (filter synthesis, not task training) — cite as lineage.
- **Cost vs W0:** narrower, but it is *exactly* what we build (the B1 set {κ_tot,j, δ_j, μ_jk}) and
  exactly what the LinOSS/S4D mapping makes meaningful — the "first" then coincides with the
  architecture's actual substance (poles = memory = the trained physics) rather than a category win.
  Honest framing bonus: the claim sentence and the contribution become the same sentence.

## W2 — all-optical-recurrence scope (fallback if W1 is also attacked)

> *The first recurrence whose **state circulates optically** (no O/E/O conversion inside the loop) with
> its recurrent parameters trained in situ by gradient-based/-estimating methods on a computational task.*

- **Survives Wu under any reading** (their loop is PD-driven O/E/O) and Böhm (electronic coupling
  memory). Orthogonal to W1 — could compound ("first all-optical dissipative-resonator recurrence…")
  if both axes are needed.
- **Cost:** "all-optical" invites scrutiny of our own gain block (Er:Si₃N₄/SOA in-loop is still optical
  amplification — defensible, but the boundary must be stated); weaker as a *learning* claim, stronger
  as a *photonics* claim.

## Recommendation

Adopt **W1 as the default PR-2 wording**, with W0 reclaimed only if Wu resolves to readout-only **and**
Zhao clears (both are live possibilities — the author query and the retrieval decide). Do not compound
W1+W2 unless an attack on W1 materializes; every added qualifier reads as a retreat. Under all variants
the paper cites Wu, Böhm, Milanizadeh/Jayatilleka (servo lineage), and Mak/Bois/Poon by name in a
prior-art boundary paragraph — the "first" is defended by drawing the map, not by omission.

**Decision coupling:** W1 does not require re-running anything in S0.1 (the B1 set *is* W1's object);
PR-2's task/architecture freeze is unaffected by the W0↔W1 choice. So the continuation gate can close
on W1 even with the Wu query unanswered — reclaiming W0 later costs only a wording edit before
submission, while the reverse (retreating from W0 to W1 after outreach) costs credibility. Freeze low,
reclaim high.
