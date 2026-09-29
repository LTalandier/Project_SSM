# P2 author-contact draft — revised 2026-09-29 — NOT SENT

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

I should be upfront that these observations are already public in brief. They
appear in section 8.3 and Figure S1 of a simulation preprint I posted on
29 September (https://zenodo.org/records/23041523), because LinOSS was the
intended external anchor for that work, and the working note is in the project's
public repository (https://github.com/LTalandier/Project_SSM). I have not posted
a standalone note. I will wait at least two weeks for your response before doing
so, can allow more time if useful, and will correct both documents if you find
an error.

The analysis was carried out with AI coding assistance (Anthropic's Claude),
which I mention for transparency.

Thank you for your work and for taking a look.

Lucas Talandier
Independent researcher, Paris

---

Revised 2026-09-29 after P1's public release: discloses that the finding already
appears in P1 §8.3/Figure S1 and in the public repository, and adds an AI-assistance
sentence. Attachment re-verified the same day (SHA-256 matches
`docs/p2/bundle_checksum.json`; its audit reruns from an empty directory).
Addresses verified 2026-09-20; primary links in
`docs/p2/source_refresh_2026-09-20.md`. This file is a draft, not a sent message.
The response window starts only on an actual send date. No send date is recorded.
