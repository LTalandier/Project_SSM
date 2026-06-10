"""The published architecture around the SSM layer, ported 1:1 (S0.2-1 / PR-1).

Reference behavior = the official repo (tk-rusch/linoss) under its pinned
dependency equinox==0.11.4 (PR-1 closure rule PF-F8i). Three port-critical
behaviors that differ from torch defaults, each replicated here:

1. **BatchNorm (equinox 0.11.4 semantics, _batch_norm.py @ v0.11.4):** in
   train mode the batch statistics (per channel, over batch x time, BIASED
   variance computed against the global mean) first update the running
   stats — running = (1-momentum)*batch + momentum*running, momentum = 0.99,
   with the FIRST call copying batch stats directly — and normalization then
   uses the just-UPDATED RUNNING stats, not the raw batch stats (torch
   BatchNorm1d normalizes by batch stats; equinox <= 0.11.4 does not).
   Inference uses the stored running stats. channelwise_affine=False,
   eps = 1e-5, and a var clamp at 0.

2. **GELU:** jax.nn.gelu defaults to the tanh approximation; torch defaults
   to exact erf. We use approximate='tanh'.

3. **Dropout key sharing:** the official calc_output vmaps the model over the
   batch with a single PRNG key, so each step's dropout masks are SHARED
   across batch elements (distinct per block and per site). Replicated by
   drawing one (L, H) mask per site and broadcasting over the batch.

Stack (official LinOSSBlock / LinOSS modules):
    encoder Linear(N_in -> H)
    x num_blocks: skip + Drop(GLU(Drop(GELU(SSM(BN(x))))))
    mean-pool over time -> Linear(H -> n_classes) -> softmax (inside model)

Linear init = equinox default = U(+-1/sqrt(in_features)) for weight AND bias
(identical to torch's default; set explicitly for determinism with a local
generator).
"""

import math

import torch
from torch import nn
from torch.nn import functional as F

from photonic_ssm.linoss.layer import LinOSSIMLayer


def _init_linear(lin: nn.Linear, generator):
    lim = 1.0 / math.sqrt(lin.in_features)
    with torch.no_grad():
        lin.weight.uniform_(-lim, lim, generator=generator)
        if lin.bias is not None:
            lin.bias.uniform_(-lim, lim, generator=generator)


class EMABatchNorm(nn.Module):
    """equinox 0.11.4 BatchNorm semantics (see module docstring, item 1)."""

    def __init__(self, num_channels, eps=1e-5, momentum=0.99):
        super().__init__()
        self.eps = eps
        self.momentum = momentum
        self.register_buffer("running_mean", torch.zeros(num_channels))
        self.register_buffer("running_var", torch.ones(num_channels))
        self.register_buffer("first_time", torch.tensor(True))

    def forward(self, x):
        # x: (B, L, C); stats per channel over (B, L).
        if self.training:
            mean = x.mean(dim=(0, 1))
            var = ((x - mean) ** 2).mean(dim=(0, 1))
            var = torch.clamp(var, min=0.0)
            if bool(self.first_time):
                run_mean, run_var = mean, var
            else:
                m = self.momentum
                run_mean = (1 - m) * mean + m * self.running_mean
                run_var = (1 - m) * var + m * self.running_var
            # Store detached; but normalize with the LIVE tensors — in the
            # official jax graph gradients flow through the batch-stat share
            # of the just-updated running stats ((1-momentum) = 1%-weighted;
            # full-weight on the very first call).
            self.running_mean = run_mean.detach()
            self.running_var = run_var.detach()
            self.first_time.fill_(False)
            return (x - run_mean) / torch.sqrt(run_var + self.eps)
        return (x - self.running_mean) / torch.sqrt(self.running_var + self.eps)


class GLU(nn.Module):
    def __init__(self, input_dim, output_dim, *, generator=None):
        super().__init__()
        self.w1 = nn.Linear(input_dim, output_dim, bias=True)
        self.w2 = nn.Linear(input_dim, output_dim, bias=True)
        _init_linear(self.w1, generator)
        _init_linear(self.w2, generator)

    def forward(self, x):
        return self.w1(x) * torch.sigmoid(self.w2(x))


def _shared_dropout(x, p, training, generator):
    """Inverted dropout with the mask SHARED across the batch dim (item 3).

    The mask is drawn on the GENERATOR's device (CPU in all Gate-i runs, so
    the random stream is identical across CPU and GPU executions) and then
    moved to x's device. On the CPU path this is bit-identical to drawing on
    x.device directly (the .to() is a no-op).
    """
    if not training or p == 0.0:
        return x
    keep = 1.0 - p
    draw_device = generator.device if generator is not None else x.device
    mask = (
        torch.rand(x.shape[1:], device=draw_device, generator=generator) < keep
    ).to(device=x.device, dtype=x.dtype) / keep
    return x * mask


class GateIBlock(nn.Module):
    """skip + Drop(GLU(Drop(GELU(SSM(BN(x)))))) — official LinOSSBlock."""

    def __init__(self, ssm_size, H, drop_rate=0.05, *, generator=None):
        super().__init__()
        self.norm = EMABatchNorm(H)
        self.ssm = LinOSSIMLayer(ssm_size, H, generator=generator)
        self.glu = GLU(H, H, generator=generator)
        self.drop_rate = drop_rate

    def forward(self, x, *, dropout_generator=None):
        skip = x
        x = self.norm(x)
        x = self.ssm(x)
        x = _shared_dropout(
            F.gelu(x, approximate="tanh"), self.drop_rate, self.training, dropout_generator
        )
        x = self.glu(x)
        x = _shared_dropout(x, self.drop_rate, self.training, dropout_generator)
        return skip + x


class GateIClassifier(nn.Module):
    """encoder -> num_blocks x GateIBlock -> mean-pool -> linear -> softmax.

    Returns class PROBABILITIES (softmax inside the model, official
    LinOSS.__call__); the loss is -sum(y * log(p + 1e-8)) as in the official
    classification_loss.
    """

    def __init__(self, num_blocks, data_dim, ssm_size, H, n_classes, *, generator=None):
        super().__init__()
        self.encoder = nn.Linear(data_dim, H)
        _init_linear(self.encoder, generator)
        self.blocks = nn.ModuleList(
            GateIBlock(ssm_size, H, generator=generator) for _ in range(num_blocks)
        )
        self.head = nn.Linear(H, n_classes)
        _init_linear(self.head, generator)

    def forward(self, x, *, dropout_generator=None):
        x = self.encoder(x)
        for block in self.blocks:
            x = block(x, dropout_generator=dropout_generator)
        x = x.mean(dim=1)
        return torch.softmax(self.head(x), dim=-1)

    def param_counts(self):
        """(trainable, published-convention) parameter counts.

        The published appendix counts (10,936 G1 / 134,279 G3) tally every
        array leaf of the equinox model INCLUDING the BatchNorm state
        (running mean + running var + the first_time flag = 2H+1 per block),
        which are not trainable parameters. Report both (PR-1 integrity
        check).
        """
        trainable = sum(p.numel() for p in self.parameters() if p.requires_grad)
        state = sum(b.numel() for b in self.buffers())
        return trainable, trainable + state
