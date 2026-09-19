# P2 author-contact draft — 2026-09-20 — NOT SENT

To: T. Konstantin Rusch <tkrusch@tue.ellis.eu>; Daniela Rus <rus@csail.mit.edu>
From: Lucas Talandier <lucas.talandier@free.fr>
Attachment: `p2_evidence.zip` (portable audit bundle; includes the working note)

Subject: LinOSS EigenWorms rerun and a probability-space loss diagnostic

Dear Dr. Rusch and Prof. Rus,

While evaluating LinOSS as a reference for a photonic simulation project, I reran
your EigenWorms configuration at commit 05a8353 using the five shipped seeds.
The archived official-code runs scored 97.22, 83.33, 97.22, 97.22 and 77.78%,
for a mean of 90.56% and population SD of 8.35 percentage points, compared with
the paper's 95.0 ± 4.4%. My historical environment used an RTX 3090 and JAX
0.4.28; the exact GPU driver and JAX CUDA runtime were not preserved, which limits
how precisely I can reconstruct the comparison.

Separately, I noticed that the classification loss applies log(p + 1e-8) to
softmax probabilities. Its logit gradient is attenuated by p_true/(p_true+1e-8)
and becomes zero if the true-class probability underflows. Instrumented diagnostic
runs of my PyTorch port show finite windows of zero parameter gradients. However,
the archived official-code CPU screen had zero strict traps in eight 4,000-step
runs, and I do not claim that exact-gradient absorption explains the five-seed
accuracy difference. Nor have I completed a paired full benchmark with a stable
log-softmax replacement.

The attachment contains the raw metric arrays, diagnostic traces, source hashes,
a numerical gradient probe and a short note separating these observations. I
would appreciate any corrections, relevant environment details, or advice on a
paired comparison that you consider informative.

I would like to give you at least two weeks to respond before considering a
public note, and can allow more time if useful. Nothing has been submitted as a
standalone reproducibility note.

Thank you for your work and for taking a look.

Lucas Talandier
Independent researcher, Paris

---

Addresses verified 2026-09-20; primary links in
`docs/p2/source_refresh_2026-09-20.md`. This file is a draft, not a sent message.
The response window starts only on an actual send date. No send date is recorded.
