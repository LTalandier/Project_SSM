# P2 author-contact email — DRAFT for Lucas to send (decision (a), 2026-07-07)

**To:** T. Konstantin Rusch, Daniela Rus [fill: current addresses — Rusch's academic page / the
arXiv:2410.03943 contact] · **From:** lucas.talandier@free.fr
**Attach / link:** the dossier (rerun trails + parity dossier + diagnosis script — [fill: repo or
archive link once Lucas creates it])

---

Subject: EigenWorms LinOSS-IM result — a reproducibility finding you may want to see first

Dear Dr. Rusch, Dear Prof. Rus,

I'm an independent photonics researcher using LinOSS as the architectural basis for a photonic
state-space-model program, and as part of a pre-registered reproduction gate I re-ran your
EigenWorms benchmark. I'm writing to share a finding with you before I make it public, in case
you want to check it, correct me, or coordinate timing.

Running your official repository unchanged — shipped EigenWorms config, your published seeds
{2345, 3456, 4567, 5678, 6789} — on a 2026 stack (JAX 0.4.28, Ampere GPU, default settings), I
obtain 90.56 % with per-seed σ = 9.34 pp (97.22 / 83.33 / 97.22 / 97.22 / 77.78), versus the
published 95.0 ± 4.4.

The mechanism appears to be in the objective rather than the model: −Σ y·log(softmax(z)+ε) has an
absorbing zero-gradient region in float32 — once a logit gap exceeds ≈104 nats, softmax underflows
exactly and the gradient is exactly zero on both saturated sides, so optimization freezes
(collapsed runs show best-val = first eval and early-stop at exactly 12,000 steps). The standard
log-softmax cross-entropy does not exhibit this. An independent PyTorch port with verified
numerical parity (≈2×10⁻⁷) reproduces the collapse at material incidence, so which seeds collapse
looks environment-sensitive while the mechanism itself is not.

To be clear about scope: your Heartbeat result reproduces cleanly on my stack, I am not suggesting
anything beyond a subtle objective-implementation fragility, and my note says so explicitly. I
attach the full dossier (per-seed trails, the parity evidence, and the analytical/numerical
derivation). I intend to post a short, carefully-scoped reproducibility note to arXiv in about two
weeks; I would genuinely welcome corrections before then, and I'd be happy to include a response
or to note any fix you push to the repo.

Thank you for LinOSS — the dissipative extension of it is load-bearing for my hardware program,
which is rather the point of caring this much about the benchmark.

Best regards,
Lucas Talandier
Independent researcher, Paris — github.com/LTalandier

---

**Send checklist (Lucas):** [ ] create the public dossier repo/archive and fill the link ·
[ ] fill recipient addresses · [ ] adjust the 14-day window if you prefer · [ ] send · [ ] log the
date in `paper/p2_eigenworms_note.md` §"Fairness" and in E-2026-07-07-1.
