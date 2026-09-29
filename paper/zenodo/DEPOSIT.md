# P1 — Zenodo deposit draft

Prepared 2026-09-19 at Lucas's suggestion. No record has been created or published;
no DOI is reserved. Zenodo replaces the immediate arXiv route for public deposit,
not peer review. The arXiv draft remains available for a later submission.

## Files to upload together

1. [`p1_with_supplement.pdf`](../submission/p1_with_supplement.pdf) — main paper,
   28 pages including scientific supplementary notes and 12 figures; set as preview.
2. [`p1_arxiv_source.zip`](../submission/p1_arxiv_source.zip) — editable XeLaTeX
   source, figures and ancillary audit/reproduction records. The arXiv-oriented
   filename is harmless on Zenodo. This ZIP already includes the 1,065-file
   result archive under `anc/paper__repro__results.tar.gz`; a duplicate upload is
   unnecessary. The numerical results remain the validated P1 snapshot; the bundled ledger
   now also includes the later Stage 0c registrations, not their result files.

`checksums.json` records these exact files and ZIP-integrity checks. The source
ZIP does not contain the entire Git history or all current project source; public
repository release is still needed for the paper's full-history commitment.

## Copy-ready metadata

**Resource type:** Publication → Preprint (not journal article).

**Title:** Can a photonic state-space model be trained on-chip? A pre-registered
in-situ-training bake-off on a realistic silicon-nitride ring substrate

**Creator:** Talandier, Lucas

**Affiliation:** Independent researcher, Paris

**Version:** 1.0

**Publication date:** use the actual first public deposit date, not the draft date.

**DOI:** no existing DOI for this preprint. Reserve one in the upload form if
wanted before publication; otherwise Zenodo assigns one on publication. Do not
enter an OpenTimestamps identifier as a DOI.

**Description:**

Can the physical recurrence of a dissipative photonic state-space model be trained on-device? We study this question in simulation using a pre-registered silicon-nitride coupled-ring substrate with finite Q, saturating gain, and amplifier noise. Physics-aware training (PAT) and model-free SPSA reach the registered margin of an exact-gradient ceiling on all eight seeds; PAT requires 4.6 times fewer device passes. Hamiltonian-echo learning fails its feasibility gate because dissipation defeats the echo. A single input drive reaches approximately three of 32 rings, whereas four taps recover controllability across all 32; the deployed equalizer nevertheless uses only six to eight rings. Against offline calibration, deployment, and readout retraining, a corrected sweep shows no resolved difference at five calibration-error levels spanning 5-30%. Under independent per-ring drift, PAT clears a frozen 2-fold advantage rule with a 2.42-fold median SER ratio; the ratio's own 95% interval is [1.7, 4.6]. Common-mode drift does not clear the rule. A registered prediction that the damping optimum follows task memory span fails. An inline systems follow-up also fails its energy gate: at 0.1-2 GS/s, even the most favorable digital/photonic energy ratio is 0.64 against a per-tap digital equalizer. Total training energy remains unmeasured; optical duration alone is not wall time. The results establish simulated trainability and its limits, without claiming a hardware demonstration or an energy advantage. Code, registrations, and the correction audit trail accompany the paper.

This is an unreviewed simulation preprint. The accompanying source ZIP contains
scientific supplementary notes, figures, pre-registration records, the correction
audit trail, and archived numerical results. The title poses the hardware
question; this deposit reports simulation, not on-chip experimental training.

**Keywords:** photonic computing; state-space models; silicon nitride; microring
resonators; physics-aware training; SPSA; in-situ learning; reproducibility

**Related work / software URL:** https://github.com/LTalandier/Project_SSM
(link as a software/reproduction supplement when the repository is public).
Do not claim that the repository is already public or that Stage 0c results are
included in this P1 snapshot.

**Visibility:** public files.

**Licenses (author confirmed 2026-09-19):** CC BY 4.0 for the paper and
accompanying research material; MIT for project software. Add both applicable
licenses to the record and include the following coverage statement in its
description. The licenses apply to different components, not alternatively to
the whole deposit.

> Copyright © 2026 Lucas Talandier. The paper, original figures, scientific
> supplementary text, and original accompanying result and audit records are
> licensed under CC BY 4.0. Project-authored code, including code inside the
> reproduction archives, and associated software documentation are licensed
> under MIT. Third-party material retains its applicable terms. Full licenses
> and component coverage are included in the source ZIP.

The paper PDF includes the license notice. The ZIP contains `LICENSE.txt` (MIT),
`LICENSE-CC-BY-4.0.txt`, and `LICENSING.md`. The enclosed numerical archives remain
byte-identical to the previously verified results.

## Deposit sequence

Create a new upload while signed in to Zenodo, upload the two files, enter the
metadata and license coverage above, and save/preview the draft. Reserve a DOI if
needed. Publishing registers the DOI; saving a draft does not. Record the actual
public URL/DOI and publication date after publication. The planned repository
release should happen alongside publication to satisfy the manuscript's data
availability statement. P2 contact remains a separate action.

Official guidance checked 2026-09-19:
[quick start](https://help.zenodo.org/docs/get-started/quickstart/),
[upload and metadata](https://help.zenodo.org/docs/deposit/create-new-upload/),
[DOI reservation](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/),
[licenses](https://help.zenodo.org/docs/deposit/describe-records/licenses/).
