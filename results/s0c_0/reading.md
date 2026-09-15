# S0c.0 reading (Supervisor, 2026-09-15) — the kill does not fire; the window is at the bar, in the edge cell, three unverified conditions deep

**Verdict of record (PR-22 §22.4, frozen at `7cd72f0` before the run):**
- **Kill gate: does not fire** — but degenerately. The OPT maximum (ratio ≈ 5,800) is the C-pcm +
  athermal cell: a device with 0.06 mW of static power, i.e. zero hold, zero drift, no amplifier.
  PR-22's kill rule admitted that corner; it should have required a non-degenerate cell (lesson
  recorded below). The kill rule therefore carries no information here; the CONS rule does.
- **CONS window (sourced drift): exists, at 3.19 vs the 3.0 bar**, in exactly three cells — C-pcm
  actuators + ATHERMAL overlay, N = 32, K = 5/10/20 %, **100 GS/s (the flagged band-equals-FSR
  edge)**. At 64 GS/s the same configuration is 1.25×. Class B tops out at 1.4×, C-pz at 1.7×
  (both at 100 GS/s, N = 32).
- **Sensitivity:** η = 2 both corners with e_tap at the band ends gives 0.64–5.3 at CONS — the
  verdict flips on the per-tap energy alone.

## What decides it
1. **Packaging loss → amplifier, at CONS.** The CONS packaging row (3.0 dB) alone trips the > 3 dB
   rule, so every CONS cell pays the 300 mW amplifier (UNSOURCED-typical): 3–4.7 pJ/sample at
   100–64 GS/s. That is the whole CONS floor; the SiN lattice's own loss (N × 0.15–0.62 dB) is
   second-order. This is the SJTU device's EDFA, in our ledger's clothes.
2. **Actuator hold, for anything but PCM.** Class B at N = 32 × 4 channels × 3 mW = 384 mW; C-pz 256 mW.
   Only zero-hold C-pcm clears, and C-pcm is the class whose in-situ trainability (quantized,
   write-limited, ~20 µJ/write) has never been tested — that was S0b.2's question, not run.
3. **Rate.** Photonic energy per sample ∝ 1/f_s, digital per sample constant: the window opens only
   at the highest registered rate. 100 GBd is the coherent state of the art, not a comfortable point.
4. **η_IIR.** Derived once from one device (≈ 4 taps per ring); halving it to 2 at CONS is what puts
   the window at the bar rather than above it. Unmeasured.

## Honest reading
The FSR-matched regime removes the thermal wall (that part held: ATHERMAL cells are the ones that
clear, and even TEC-held C-pcm reaches 2.1× at 100 GS/s) and the erbium pump, and it puts the lattice
next to a product-class neighbor. It does **not** produce an energy window that survives the
conservative corner without stacking three unverified conditions (PCM actuation trainable in situ;
an athermal overlay on the lattice; a per-tap energy at the high end of the bracket). Under PR-22's
own go rule this is **"S0c.1 go, conditional"** with the sourcing gaps named: the amplifier row, the
athermal overlay, and η_IIR.

## Recommendation for S0c.1 (Lucas's call, E-2026-09-15-1)
Run S0c.1 **as a science experiment, not a product test**: in-situ trainability (PAT, SPSA; BPTT
ceiling) of an 8–16-ring FSR-matched SiN lattice on a dispersive channel at 64 GBd against a matched-SER
FIR — it measures η_IIR under training (the missing number in every cell above) and it is the W1 claim
in the regime that has a neighbor. ≈ €50–100. Include a quantized-actuator arm (C-pcm levels) only if
the base arms train; that arm is S0b.2's question and stays registered separately.

## Lesson (for the ledger)
Kill rules must require a **non-degenerate** best cell (a floor on static power or an explicit
exclusion of the zero-hold/zero-drift corner); PR-22's did not, so its kill gate was uninformative.
The CONS window rule, which charges every row, did the work.
