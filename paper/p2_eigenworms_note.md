# P2 — reproducibility note (DRAFT v1, 2026-07-07)

**Status:** draft for Lucas's review; decision (a) taken 2026-07-07 under delegation — author
contact first (email draft: `paper/p2_author_email.md`), arXiv after a 14-day reply window.
**Every claim below is the adjudicated PR-1.1 wording** (Critic-approved 2026-06-11, GA-F2/F3
edits applied); evidence = the archived dossier (`results/s0_2/gate_i/` + `xcheck_official/`).
[fill] = mechanical fill from repo/logs before submission; ⚠ = verify at S0.L.

---

**Title:** *On the seed sensitivity of the LinOSS EigenWorms benchmark: an absorbing fp32
optimization collapse in the published objective*

**Authors:** Lucas Talandier (independent researcher, Paris)

## Abstract (draft)

> Oscillatory state-space models (LinOSS; Rusch & Rus, ICLR 2025) report 95.0 ± 4.4 % on the
> UEA EigenWorms long-sequence classification task — the paper's flagship long-range result. Re-running
> the **official code, configuration, and published seeds** unchanged on a 2026 stack (JAX 0.4.28,
> Ampere-class GPU, default matmul precision [fill: exact GPU/driver]), we obtain **90.56 %** with
> per-seed σ **9.34 pp ≈ 2.1× the published dispersion** (per-seed: 97.22 / 83.33 / 97.22 / 97.22 /
> 77.78). We identify the mechanism behind the low seeds: the published objective
> −Σ y·log(softmax(z)+ε) has an **absorbing zero-gradient region in float32** — once any logit gap
> exceeds ≈104 nats, softmax underflows to exactly 0/1 and the loss gradient is *exactly* zero on
> both the wrong-saturated and correct-saturated sides, so Adam cannot escape (momentum decays
> geometrically; dropout would need to cut a >104-nat gap). Collapsed runs carry a distinctive
> signature — best validation = the *first* evaluation, early-stop at exactly 12,000 steps — visible
> in our trails and consistent with the early-stop rule. An independent PyTorch port with
> numerically verified parity (2.4×10⁻⁷ CPU, 1.2×10⁻⁷ GPU, train + inference) reproduces the
> collapse at material incidence, and the standard log-softmax cross-entropy does not exhibit it.
> The published mean is **consistent with a favorable draw from a collapse mode with material
> incidence in both stacks** (point estimates 15–50 %; small-n CIs wide; no detectable stack
> difference — Fisher p = 0.15–0.61 across denominators, 9 % power at n=8+8). The architecture is
> not the issue: we reproduce the LinOSS Heartbeat result within its published band on the same
> stack. We recommend replacing the ε-inside-the-log objective with log-softmax cross-entropy and
> re-evaluating EigenWorms dispersion; we release our rerun trails, parity dossier, and diagnosis
> scripts.

## Section plan

1. **Context.** Why we ran it: a pre-registered reproduction gate for a photonic-SSM research
   program (the anchor was frozen *before* the runs; the miss-response — rerun the official code
   as-is — was pre-specified). This note reports the reproduction finding only.
2. **Setup.** Official repo (github.com/tk-rusch/linoss, MIT; JAX/Equinox), shipped EigenWorms
   config ([fill: lr 1e-3, blocks 2, batch 4, 100k max steps, eval/early-stop rule, hidden/state
   dims from the repo JSON]), published seeds {2345, 3456, 4567, 5678, 6789}; environment [fill:
   jax 0.4.28, GPU model, CUDA]; no flags altered (default matmul precision — noted, see §5).
3. **Result.** Per-seed table; 163/180 = 90.56 %, σ 9.34 vs published 95.0 ± 4.4. The two low
   seeds are *trained-but-degraded*, not chance (83.33, 77.78). Framing per adjudication: **the
   transfer failure is on dispersion and environment-sensitivity, not a 0.04-pp technicality**
   (2.78 pp/seed granularity; one test-sample resolution).
4. **Mechanism.** The ε-inside-log CE analytical derivation: ∂L/∂z = −(p_t/(p_t+ε))·(1_t − p);
   fp32 exp underflow at gap ≳104 ⇒ p_t ≡ 0.0 exactly ⇒ gradient ≡ 0 (and ≡ 0 on the
   correct-saturated side, p_t ≡ 1.0) — verified numerically in float32; healthy log-softmax CE
   gives |p−y| = O(1) in the same state. "Absorbing": Adam momentum tail decays geometrically from
   entry; escape paths enumerated and excluded. The 12,000-step / best-val-=-first-eval collapse
   signature. Elementwise fp32 is identical in both stacks (TF32 touches only matmuls) — the
   mechanism is precision-class-independent even though *which* seeds collapse is
   environment-sensitive.
5. **What is and is not claimed.** Not claimed: that LinOSS is broken (Heartbeat reproduces ✓;
   the architecture's other results untested here); not claimed: misconduct (the collapse is a
   subtle objective-implementation choice; the published draw is plausible). Claimed: the
   EigenWorms 95.0 ± 4.4 point is **fragile as a reproduction anchor** — any material collapse
   incidence makes a 5-seed mean a lottery (at incidence q=0.1, P(≥1 collapsed seed in 5) = 41 %),
   and σ understates the objective's true dispersion. Environment caveats stated (TF32-class
   matmul on our stack vs V100-era published runs [⚠ verify published hardware]).
6. **Recommendation + artifacts.** log-softmax CE; report collapse incidence; release: rerun
   npy/jsonl trails, parity dossier, diagnosis script, this note's repo.

## Fairness / conduct notes (for the cover letter + §5)

- We contacted the authors with the full dossier before posting (date: [fill]; window: 14 days).
- Our own gated 5-seed run (independent port) scored 71.11 % *because* 2/5 seeds collapsed —
  we report our number alongside theirs; the port is exonerated by the parity dossier (on record
  before the reruns), the per-parameter init audit, and the paired 5-seed comparison (p = 0.44).
- The unarchived fresh-8 incidence leg is **not** cited as evidence (indicative only) — all claims
  rest on archived artifacts.

## Venue

arXiv (cs.LG) first; then ReScience C or the venue's reproducibility track as appropriate.
LinOSS's EigenWorms number is being cited widely [⚠ verify citation count at submission]; a
carefully-scoped note has standing value to the long-range-benchmark community.
