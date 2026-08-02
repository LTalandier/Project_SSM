# §9 — Outlook: Stage 1

**Status:** DRAFT v1 (2026-07-08, single-session mode — not independently reviewed; disclosed).
**Sources:** roadmap Stage-1 · F8 hardware ledger · PR-9 promotion record · F22 framing ·
proposal §6–§8. **Open flags:** [CITE-*] keys resolved via `paper/references.md`; S0.6/S0.7 numbers landed (final-number sweep at venue formatting).

---

## 9.1 What the first chip must be

The bake-off fixes the Stage-1 chip's training stack by evidence rather than taste: **PAT and
SPSA, nothing else in the loop.** Neither exotic route earned promotion (§5.3), and the hardware
ledger (supplementary note N2) shows why that is unlikely to reverse on hardware grounds alone: the
adjoint adds circulators, phase-coherent reverse injection, and an unsolved separation of the
counter-propagating field from the backscatter doublet; RHEL adds a pumped conjugator bank whose
power budget (≈9.6 W at 32 rings) exceeds the entire rest of the system. SPSA's row is the
quiet asset — zero added components, zero model burden — so the minimal viable demonstration is:
the §3 plant (N = 8–32 rings, foundry-floor Q suffices per C-1's gate), thermo-optic {δ,
κ_ext, μ} actuation, one drop-port readout chain, the four-tap drive map of §3.6, and SPSA as
the first-light training route with PAT layered on once the twin is characterized to the
5%-class the mismatch protocol assumed.

The multi-project-wafer path is concrete: the registered cells were chosen to be
foundry-realizable (C-1 at generic-foundry loss; C-2 bounded by a demonstrated MPW result
[CITE-Cui-2023]), and the actuation map of §2 uses only standard thermo-optic tuners. The E/O
overhead the four-tap drive and the eval protocol add is exactly what §7's envelope prices.

## 9.2 What would change our mind

Three pre-registered forks, with their triggers on record: (i) **adjoint promotion** — if a
Stage-1-adjacent demonstration retires debt #4 (a physical recurrent reverse pass), the PR-9
criterion re-opens with the S0.5 data as prior; the sim says it would arrive at ceiling-grade
accuracy at 2× PAT's device cost, zero digital. (ii) **The in-situ advantage** — the offline
tie (§5.5) at 5%-class mismatch sets the burden: in-situ training earns its place on hardware
only where calibration is worse than 5%-class, drifts on deployment timescales, or where the
envelope penalizes the twin's digital ledger. The Stage-1 experiment should be *designed to
measure exactly this differential* — same chip, offline-deploy vs PAT/SPSA arms — rather than
assume it. (iii) **RHEL** — nothing on SiN; the sim verdict (dissipation-fatal at the operating
point even with a perfect conjugator) would need a *conservative* platform regime, not a better
conjugator, to reopen.

## 9.3 Beyond the linear unselective core

The frozen architecture is deliberately the unselective LTI core — poles and couplings, the part
photonics builds natively. The selectivity axis (input-dependent dynamics in the Mamba direction
[CITE-Mamba]) maps onto the same lattice as input-dependent $C$ then $B$ actuation and is
scoped for a later stage only behind its own gate (per-step tuning without per-state DACs);
nothing in this paper's claims depends on it. Likewise the damping operating point (§6) and
the D-LinOSS accuracy question ride the *trainable* κ_ext axis established here rather than new
hardware.

## 9.4 Closing

The program set out to answer a narrow question with unusual bookkeeping: can the physics of a
dissipative photonic recurrence be trained through itself, and at what honest cost? In
simulation, under pre-registered thresholds: yes — by the two methods a chip can already run,
at device-pass costs now quantified, with the exotic routes priced out by data and the
advantage-over-offline question left honestly open. The next sentence worth writing requires a
chip.
