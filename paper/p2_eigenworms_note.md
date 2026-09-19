# EigenWorms rerun variability and loss saturation in a LinOSS implementation

*Lucas Talandier — evidence-audited working note, 2026-09-20. Not submitted;
authors have not been contacted. Supersedes the 2026-07-07 draft in Git history.*

## Summary

An archived five-seed rerun of the official LinOSS-IM EigenWorms implementation
scores **90.56%**, with **8.35 percentage points population standard deviation**
(ddof=0), versus the published **95.0 ± 4.4%**. The sample standard deviation
(ddof=1) is 9.34 pp; comparing that directly with the upstream population standard
deviation was inconsistent. These are descriptive results from five runs, not a
test establishing that the published population mean or variance is incorrect.

Separately, the implementation's probability-space loss
`-log(softmax(z)[target] + 1e-8)` attenuates the logit gradient when the correct-class
probability is small, and has zero logit gradient when that probability underflows
to zero. Archived instrumented runs of our PyTorch port exhibit finite windows
of exact zero parameter gradients. However, the archived official-code CPU
screen finds **0/8 strict traps** under its registered trail-based classifier.
We cannot attribute the official five-seed accuracy difference to exact-gradient
absorption, or claim that a corrected loss has restored the full benchmark.

## Source and configuration

Primary references: [Rusch & Rus, Oscillatory State-Space Models, Table 1 and Appendix B](https://arxiv.org/html/2410.03943v3),
and the [official implementation at commit 05a8353](https://github.com/tk-rusch/linoss/tree/05a835355439ee5500b2c8f891132c53adf020c0).
On 2026-09-20, the fetched upstream main head is still that commit. Its `train.py`
uses the epsilon-inside-log classification loss; `models/LinOSS.py` supplies
softmax probabilities; `postprocess_results.py` uses `numpy.std` with default
ddof=0. Relevant source files and the original MIT license are included in
`docs/p2/upstream/`. This finding concerns that implementation, not all later
libraries or every LinOSS result.

The shipped EigenWorms configuration uses seeds 2345, 3456, 4567, 5678, 6789;
LinOSS-IM, two blocks, hidden dimension 128, SSM dimension 64, two SSM blocks,
time channel enabled, batch size 4, constant learning rate .001, maximum 100,000
steps and evaluation every 1,000 steps. The training script stops after more
than ten consecutive non-improving validation evaluations. Test performance is
recorded at validation-selected checkpoints, with the script's tie convention.

The historical record identifies RTX 3090 hardware for the rerun machine and
JAX 0.4.28 / Equinox 0.11.4 / Optax 0.2.2 for the official rerun. The saved GPU
parity log directly records RTX 3090, PyTorch 2.12.0+cu126 and Torch CUDA 12.6.
**The GPU driver version and JAX CUDA runtime were not recovered.** Torch's CUDA
version is not proof of the JAX runtime. No JAX matmul precision override was
recorded; effective backend precision was not independently measured. The paper
lists V100 and RTX 4090 hardware (A100 for PPG); it does not identify the exact
GPU for each EigenWorms seed. Describing the comparison as simply Ampere versus
V100 was unsupported.

## Archived observations

| Seed | Official JAX test accuracy | Correct / 36 |
|---|---:|---:|
| 2345 | 97.22% | 35 |
| 3456 | 83.33% | 30 |
| 4567 | 97.22% | 35 |
| 5678 | 97.22% | 35 |
| 6789 | 77.78% | 28 |

Mean: 163/180 = 90.5556%. Across these five accuracies: population SD 8.3518 pp;
sample SD 9.3376 pp. Five runs and 36 test cases per seed limit what this says
about population dispersion. Repeated evaluation of the same small dataset does
not create 180 independent test subjects. The older draft's claim that the
published SD understates the true dispersion is withdrawn.

The historical log says the official five did not exhibit the early exact-trap
pattern. Some trails degrade later; they contain no direct per-step gradient
measurements. Their selected test accuracies do not identify the cause of the
accuracy gap. The saved `steps.npy` contains the configured schedule, including
steps not executed after early stopping; completed evaluation counts are read
from the actual metric arrays instead.

Our port's five gated EigenWorms runs average **71.11%**. Two have flat training
and validation accuracy and stop at step 12,000. This is a behavioral signature,
not direct archived gradient evidence for those particular GPU runs. On Heartbeat,
the port averages **72.90%**, within the reference's reported 75.8 ± 3.7 band.
Cross-framework/CPU-GPU parity checks support the port on tested fixtures; they
do not prove equal stochastic training trajectories across frameworks.

The separately registered, archived **official CPU fresh-eight screen** runs
4,000 steps per seed. Recomputing its conservative classifier gives **0/8 strict
traps**, with two partial-constancy flags (9012 and 22222). Seed 22222 remains at
low train/validation accuracy while cycle loss changes, so it is not an exact
trap under that rule. The older GPU fresh-eight observation was not archived and
is excluded from quantitative evidence.

The archived **port CPU annex** records parameter-gradient norm at each of 600
steps. Recomputed exact-zero suffixes begin at step 1 for seed 8901 and step 555
for seed 9012; seed 7890 remains active. These establish observed finite-window
zero gradients for two of three selected diagnostic seeds. These windows,
classifiers and seed sets differ from the official screen and must not be pooled
into one incidence estimate or used to claim cross-framework equivalence.

## Numerical mechanism and limits

For one-hot target t, probability p_t and epsilon e,

`dL/dz_j = [p_t / (p_t + e)] * [p_j - 1(j=t)]`.

The gradient is attenuated well before underflow. A fresh, CPU float32 two-logit
probe has gradient magnitude about .171 at wrong-class gap 20, 1.80e-27 at gap 80,
and zero at gap 104; stable log-softmax cross-entropy retains magnitude about one
for these confidently wrong predictions. The exact underflow boundary depends
on implementation and floating-point handling; 104 is not a universal threshold
across all backends. This probe demonstrates a numerical property, not training
incidence or benchmark recovery.

A zero gradient on a particular batch does not prove that every future stochastic
batch, dropout mask, optimizer momentum update or other loss term leaves the
parameters fixed. We therefore use finite-window observations rather than the
old draft's unconditional assertion that escape is impossible. The appropriate
follow-up is a paired, same-seed full-training comparison using logits and stable
cross-entropy, with diagnostic logging and explicit environment capture. It has
not been performed here.

## Reproduction and contact status

`python3 -m analysis.p2_audit` recomputes the descriptive statistics, strict-screen
classifications, zero-gradient suffixes and numerical probe. Inputs are hashed
in `results/p2_audit/audit.json`. `paper/p2_evidence.zip` is a portable audit bundle
of these measurements and scripts, not a complete training environment or raw
EigenWorms dataset. See `docs/p2/README.md`.

No author contact has occurred. `paper/p2_author_email.md` is the revised unsent
request for feedback. The planned response window is 14 days after actual sending;
it has not started. No publication date or venue decision is implied. Missing
historical runtime details and the lack of a paired corrected-loss benchmark are
explicit limitations, not fields filled by inference.
