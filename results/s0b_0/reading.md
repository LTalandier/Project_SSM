# S0b.0 reading (Supervisor, 2026-09-13; single-session mode) — the door is closed by arithmetic

**Verdict of record (PR-20 §20.5, frozen before the run at `ee137c4`):** the S0b.0 **kill fires**.
The maximum E_digital / E_photonic over every OPT-corner class-C cell — passive or pumped, every
drift option including the two UNSOURCED optimistic ones, retraining at 1000 s, best reachable tap
count — is **0.64** (C-pcm, passive, 10 mW global-heater hold, N = 128 / C-3, 2 GS/s, 64 taps:
5.0 pJ/sample photonic vs 3.2 pJ/sample digital). The bar is 3. The CONS product window does not
exist (max 0.38). With UNSOURCED rows removed the maxima fall to 0.23 (OPT) and 0.18 (CONS).
**S0b.1–S0b.3 do not run.** Stage 0b ends at its first phase, as the roadmap said it most likely would.

## What closed it (in order of weight)

1. **Thermal management, not actuation.** With non-volatile actuators the hold term is zero and the
   photonic stage's entire static power is the common-mode thermal hold that keeps 14 pm/K resonances
   (8 mK per C-2 linewidth) aligned to an external carrier: 180 mW for a TEC (VERIFIED), 10–50 mW for
   an isolated-package heater (UNSOURCED, optimistic). Even the optimistic 10 mW at 2 GS/s is
   5 pJ/sample — more than a 64-tap digital equalizer costs at 7-nm-class energy per tap.
2. **The registered line-rate window.** A fixed-power device's energy per sample is P/f_s, and its
   reachable tap count is T_mem·f_s, so the ratio scales as **f_s²**. At the S0.1-registered
   0.1–2 GS/s the photonic side cannot amortize even 10 mW. This is the one lever outside the frozen
   grid (see residue below).
3. **The per-tap pricing.** P1's DSP baseline was a coherent-DSP *block* (25–170 pJ/bit × ENOB
   ≈ 210–1600 pJ/sample). The equalizer it would actually replace costs 0.05–0.15 pJ per tap per
   sample (Credo 802.3ck study; Horowitz-scaled floor), i.e. 3–10 pJ/sample at 64 taps. The function-
   matched baseline is 30–100× cheaper than the block P1 compared against. P1's ~15× at N = 128 was
   already stated as "unmeasured in magnitude"; S0b.0 measures it: negative.
4. **The gain pump** (found this session: a fifth unbudgeted item in P1 §7). Pumped rings cost 0.8–17 mW
   electrical each (derived) — 26–550 mW at N = 32, plus a cooled pump module. The product device must
   be passive (undoped: unpumped Er absorbs 2 dB/cm), which shortens memory ~10× and pushes 64 taps
   to the aspirational C-3 corner.
5. **Phase-change actuators on a high-Q ring** (ledger §1C-pcm, derived): a 1 µm full-overlap Sb₂Se₃
   cell adds 0.02 dB per round trip against 0.0078 dB intrinsic at C-2 (Q ×0.28) and its 65 levels
   span 6.4 GHz — 100 MHz per level against a 14 MHz linewidth. Only a weak-overlap design (assumed
   loss scaling) gets to ≈ 0.7 linewidth per level at Q ×0.8. Not what closed the door, but it means
   S0b.2's question would have been posed at ~65 levels and ~20 µJ per write.

## What did not matter
- The retraining term: at the drift anchor (one C-2 linewidth per ≈ 1 h), T_r ≈ 10²–10³ s costs
  ≤ 0.03 mW (OPT) / ≤ 1 mW (CONS). S0b.3's question is answered by arithmetic: retraining is cheap;
  it just does not address the common-mode term that dominates.
- Actuator class beyond "not thermal": C-pz vs C-pcm differ by the hold-electronics row, which is
  second-order next to the thermal hold.

## Residue (flagged, not a result)
The ratio's f_s² scaling means the arithmetic reopens the door at line rates ≳ 10 GS/s *if* the common-
mode hold is ≤ 10 mW and the workload needs ≥ 64 taps: at 10 GS/s the C-3 passive reach is ≈ 370 taps,
a 128-tap digital block costs 6.4–19 pJ/sample, and a 10 mW stage costs 1 pJ/sample. Whether the ring
lattice can be *trained* at a per-step decay exp(−κ_net dt) ≈ 0.999 — the S4D/LinOSS mapping regime of
S0.1 at dt = 0.1 ns — is unmeasured, and the 0.1–2 GS/s window is a Stage-0 registration (S0.1 mapping,
PR-10), not a physics bound. Opening it is a scope change (a PR-20a addendum + an S0.1 re-mapping) and
is Lucas's call (E-2026-09-13-2). Nothing in Stage 0's data supports it either way.

## Consequences
- **Stage 0b: CLOSED at S0b.0** (negative). No compute spent (€0). S0b.1–S0b.3 not run; S0b.4 is this
  file plus the exclusions-ledger addendum.
- **P1 correction (the one edit the Stage-0b non-goal is overridden for):** §7.1 listed *four* known
  exclusions; the substrate's Er:Si₃N₄ pump is a fifth, of the same order as the four. Direction is
  against the photonic side (shrinks positive cells only), so P1's negative findings and its
  "unmeasured in magnitude" verdict are unaffected; the list and the integrated-realization condition
  now say five. Recorded in `docs/s0_7/exclusions_ledger.md` §5 and the supplementary checklist.
- **Stage 1:** the 2026-09-13 ruling stands and is now quantified: the first in-situ-trained recurrent
  photonic system is worth building as a *first*, on a collaborator's bench, not as a technology.
- **P5:** a negative envelope note is publishable ("inline photonic equalizer on SiN: the thermal-hold
  floor vs a per-tap digital baseline") and is the honest companion to P1 §7. Lucas's call.
