# Critic Review Spec — the G3 failure diagnosis + the PROPOSED PR-1.1 amendment

**Filed by:** Supervisor, 2026-06-11 · **Verdict file:** `shared/critic_review_g3-adjudication.md`
**Stakes:** this adjudication decides whether the program proceeds past a FAILED pre-registered
gate. It is the single most attackable moment in the project's history so far — "they failed
their reproduction gate and then changed the gate" is the exact hostile reading S0.8 will face.
Your job is to try to make that reading stick. Findings go to Lucas; he signs (or refuses)
PR-1.1 with them in hand.

## Target

1. **The G3 diagnosis** — results_log S0.2-1 addenda (the 2026-06-10/11 blocks) + raw trails
   `results/s0_2/gate_i/` (ours) and `results/s0_2/gate_i/xcheck_official/` (13 official runs)
   + the diagnostic scripts in the repo.
2. **The PROPOSED PR-1.1 block** at the end of `shared/preregistration.md` (Supervisor draft
   2026-06-11) — the adjudication *choices*, not just the transcription.
3. Context: frozen PR-1 v2 (esp. the miss-rule, closure rule, PF-F9d margin calibration —
   your own review signed that calibration; treat your prior reasoning as in-scope for
   attack), D-2026-06-11-1, E-2026-06-10-5 (the GPU route record).

## Checklist

1. **Is the trap real and correctly attributed?** Re-derive analytically: in fp32, does
   −Σ y·log(softmax + 1e-8) produce *exactly* zero total gradient once p_true underflows
   (consider the ε inside the log; the softmax Jacobian; could a tiny-but-nonzero gradient
   re-escape?). Check the step-instrumented trails (step-0 |grad| ~4×10³ → ≡0.0 at entry
   steps 1/4/7/1). Is "absorbing" the right claim (any escape path: dropout stochasticity,
   BN drift, lr schedule)?
2. **Is the official rerun faithful?** Audit `xcheck_official/`: pinned commit, the
   reference-venv versions, official pickles, their runner, the seed list. Anything in the
   harness that could depress the official mean (the −0.044 pp miss is razor-thin — a single
   harness artifact could flip it; conversely σ ≈ 9.3 with values 77.8/83.3 is the heavier
   evidence — verify those per-seed values from raw trails, not the summary).
3. **The TF32 asymmetry question.** The official code sets no matmul-precision flags (JAX
   default = TF32-class on Ampere); ours ran strict-fp32. The entry claims the fp32 softmax
   underflow threshold is identical and the difference is rounding-noise only. Is that sound,
   or could matmul precision plausibly shift *trap incidence* (4/8 vs 2/8) or healthy-seed
   accuracy? If plausible, does it change any conclusion (note both stacks FAIL the letter
   regardless)?
4. **Is the port exoneration airtight?** Weight-transplant parity is blind to init bugs by
   construction — was the line-by-line init audit complete (every parameter group, incl.
   biases, A/steps, B, C, D, BN)? The RNG-stream difference is declared framework-inherent:
   is there any *protocol-relevant* freedom in stream construction the port could have chosen
   differently (and would PR-1's closure rule have permitted it)? Power-check the 4/8-vs-2/8
   comparison: at n=8+8, what incidence ratio *could* this design have detected? State plainly
   whether "indistinguishable" is evidence of equivalence or just low power — and whether that
   distinction matters for the amendment (the Supervisor's claim: it does not, because either
   incidence breaks the anchor).
5. **The healthy-band agreement argument.** Comparing healthy-3 (ours, 93.52) to the official
   non-trap band conditions on the outcome — selection on the dependent variable. Is the
   conditional comparison legitimate for the *implementation-equivalence* purpose it serves
   here? Propose better framing if not.
6. **The adjudication itself (the big one).** Void-with-no-replacement vs the alternatives:
   (a) re-register on the official-rerun value (90.5556 or a band around it) with fresh seeds;
   (b) MotorImagery swap (weigh against its registered preprint exclusion); (c) record FAIL
   and require nothing (proceed bare). Is the Supervisor's choice the most defensible? Probe
   the re-registered criterion (G1 ∧ parity dossier): the parity dossier already exists — is
   re-registering a criterion *known to be satisfied* laundering, or is it the honest
   recognition that the strongest implementation evidence was always the parity (note the
   cross-check harness WAS pre-specified in the S0.2-1 spec before any run)? Does the
   SERVED-vs-PASS wording + permanent letter-FAIL record survive the hostile reading at the
   top of this spec?
7. **The F-G3 finding as paper material.** Is the claim "the published 95.0±4.4 rests on a
   favorable seed draw of a ~25 %-incidence collapse" fairly stated at our evidence level
   (16 total seeds, two stacks)? What wording would survive the LinOSS authors reading it?
   (The optional upstream courtesy report is Lucas-paced — out of scope here, but flag
   wording risks.)
8. **The new process rule** (reference-implementation transfer check before any
   externally-anchored threshold freezes): well-formed? Should it bind PR-4 (no external
   anchor there) or only future anchor-type freezes? Any cost blind spot?
9. **Cross-references:** PR-3/PF-F9d/D-08-2 consistency (the "in-house ceiling was always the
   operative reference" leg — verify those texts actually say this); G1 PASS untouched;
   annex-3 cancellation vs PF-F8g; the spend record E-2026-06-10-5 (in-session Lucas approval,
   $1.15 actual ≤ $7.44 ceiling) — process-clean?

## Out of scope

Re-running any training (the raw trails are the evidence base; small analytic re-derivations
fine); PR-2/PR-4 content; the upstream-report decision (Lucas's, later); re-litigating the
PR-1 v2 freeze itself (your review + his signature stand — the question is what follows the
measured outcome).

## Verdict

Standard format: APPROVE / APPROVE-WITH-EDITS / AMEND / REJECT + numbered severity-rated
findings, ending with the line Lucas needs: **"sign PR-1.1 as-is" / "sign with these edits" /
"different adjudication: <which>"** — with exact replacement text for any edit.
