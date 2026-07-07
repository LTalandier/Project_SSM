# PR-5 recon — twin-mismatch level sources (S0.4-0 item 5)

**Status:** recon memo (2026-07-07, single-session mode) → the **menu** for PR-5's
[RECON-DEFERRED] numeric levels. The *families* (M-par / M-struct / M-noise + decomposed
reporting) are 🔒 SIGNED (PR-5 v2, 2026-07-07); the numeric levels freeze in the **S0.4a task
spec** before the PAT runs. Literature discipline: ⚠-flagged figures came from memory/aggregation
and must be primary-source-verified at S0.L **before the paper quotes them** (the B2/F5 lesson);
the *level menu itself* only needs bracketing plausibility, which is why it can freeze at S0.4a
with the ⚠ flags carried.

## What PR-5 needs numbers for

PAT = physical forward, digital-twin backward. Its headline is trained-through-mismatch, so the
twin must be *registered-wrong* by realistic amounts. The recon question: **how wrong is a
realistic twin of this substrate?** — per parameter (M-par), in structure (M-struct), in noise
(M-noise).

## M-par — parameter-characterization accuracy (the "how well can you measure the device" gap)

| Twin parameter | Realistic characterization route | Accuracy bracket | Source status |
|---|---|---|---|
| κᵢ, κ_ext (per ring) | Lorentzian / split-Lorentzian linewidth fit against a calibrated-MZI frequency ruler | **1–5 %** typical; ≤10 % conservative for near-critical coupling ambiguity (under/over-coupled branch) | ⚠ standard SiN-characterization practice (e.g. damascene/AN800-class papers); verify a citable per-fit error bar at S0.L |
| δ (resonance position) | swept-laser + wavemeter; thermal drift between calibration and run | **1–10 % of κᵢ** with active tracking; O(κᵢ) without | ⚠ drift/locking figures platform-dependent; SiN low-dn/dT favors the low end |
| μ_jk (ring–ring) | supermode-splitting fit (2μ) | **2–10 %** (splitting fits are differential → cleaner than absolute κ) | ⚠ verify |
| g₀, P_sat (Er gain) | gain-vs-input-power curve fit | **±0.5–1 dB on gain (~10–25 %)**; P_sat bracket ±3 dB — the flagship reports gain but **no NF** (debt #3), and its P_sat = −15 dBm input is an [EV] entry | Er:Si₃N₄ flagship = Liu et al., *Science* **376**, 1309 (2022) ⚠ verify exact error bars |

**Menu (M-par levels, per-parameter multiplicative errors, frozen at S0.4a):**
L1 = 1 % · L2 = 5 % · L3 = 15 % (κ, μ, δ/κᵢ); gain pair (g₀, P_sat) always at the loose end
{10 %, 25 %} reflecting the debt-#3 characterization gap. Recommended headline: **L2 with the
loose gain pair** (the "competent-lab" twin); L1/L3 as sensitivity.

## M-struct — structural omission (the S31-F1 quantity)

The registered headline family: **the twin runs `gain_mode="fixed"`** (g ≡ 0.9κᵢ constant —
drops ∂g/∂κ_ext entirely, the exact channel S31-F1 measured at −0.75 @θ₀, sign-flipping at
r≈0.5) while the substrate runs `saturating`. This is the *natural* structural error — it is
literally the plane the frozen calibration numbers live on, so it is what a naive twin-builder
would ship. Second family member (milder): saturating twin with the **wrong build-up plane**
(bus-referenced vs intracavity). Recommended headline: **fixed-mode twin**, decomposed reporting
per PR-5 v2 ({M-par only / M-struct only / both / perfect-twin}).

## M-noise — noise-model gap

Twin ASE ∈ {absent (noiseless twin — the common shortcut), NF 3 dB (quantum-limit optimist)} vs
substrate NF-A 7.0. Recommended headline: **noiseless twin** (hardest honest case; PAT's backward
pass sees no stochasticity the device has).

## PAT / SPSA precedent (what mismatch magnitudes are survivable — context, not levels)

- **Wright et al., *Nature* 601, 549 (2022)** — PAT origin. Demonstrates training *through*
  twin error where in-silico-trained-then-transferred networks degrade badly; the PAT-vs-in-silico
  gap on their photonic system is the canonical precedent that M-par/M-struct at the above levels
  is survivable-in-principle. ⚠ verify the quantitative transfer-gap figures at S0.L before
  quoting.
- **SPSA/forward-only photonic demos** (model-free — no twin, the natural PAT foil):
  Bandyopadhyay et al. (single-chip photonic DNN, in-situ/forward training) ⚠ verify venue+year;
  Spall et al., *Optica* (hybrid/optical-backprop line) ⚠; plus the in-house `pnn-multilayer`
  β-track SPSA-under-thermal-crosstalk results (internal, citable as prior work — the S0.0 salvage
  provenance).
- Implication for PR-6 fairness: none of these trained a *recurrent* substrate — the precedent
  says nothing about mismatch interacting with pole positions near a stability boundary (r_min).
  That interaction is precisely what S0.4a measures; flagged so the paper does not over-claim the
  precedent (F22 framing).

## Recommended S0.4a freeze (the menu's default row)

M-par **L2** (5 %; gain pair 10 %/25 %) · M-struct **fixed-mode twin** · M-noise **noiseless twin**
· decomposed reporting {M-par / M-struct / both / perfect-twin} per PR-5 v2 · L1/L3 sensitivity
rows if budget allows. Freeze these (or amended values) in the S0.4a task spec **before** the
first PAT run.
