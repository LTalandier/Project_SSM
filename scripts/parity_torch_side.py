"""S0.2-1 parity check, torch side (step 1 of 3).

Builds the in-house Gate-i model at both anchor configs, exports weights +
fixed inputs + outputs to /tmp/parity_gate_i/torch_side.npz. The jax side
(parity_jax_side.py, scratch venv) transplants the SAME weights into the
OFFICIAL model and saves its outputs; compare_parity.py asserts closeness.
This is the PR-1-sanctioned use of the official repo: a debugging
cross-check, never the tested object.

Covered: (a) full-model inference forward (dropout off, BN running stats
transplanted); (b) full-model train-mode forward with dropout p=0 (exercises
the eqx BN train path: EMA update + normalize-by-updated-stats);
(c) SSM-layer-only forward at G3 size with L = 17,984 (fp accumulation over
the full EigenWorms length).
"""

import os

import numpy as np
import torch

from photonic_ssm.linoss.layer import LinOSSIMLayer
from photonic_ssm.linoss.stack import GateIClassifier

OUT = "/tmp/parity_gate_i"
os.makedirs(OUT, exist_ok=True)


def export_model(tag, num_blocks, data_dim, ssm, H, n_classes, L, batch, seed):
    g = torch.Generator().manual_seed(seed)
    model = GateIClassifier(num_blocks, data_dim, ssm, H, n_classes, generator=g)
    x = torch.randn(batch, L, data_dim, generator=g)

    # give the BN buffers non-trivial values for the inference parity
    rs = {}
    for i, blk in enumerate(model.blocks):
        mean = torch.randn(H, generator=g) * 0.3
        var = torch.rand(H, generator=g) + 0.5
        blk.norm.running_mean.copy_(mean)
        blk.norm.running_var.copy_(var)
        blk.norm.first_time.fill_(False)
        rs[f"{tag}_bn{i}_mean"] = mean.numpy()
        rs[f"{tag}_bn{i}_var"] = var.numpy()

    model.eval()
    with torch.no_grad():
        out_inf = model(x)
    # train-mode pass with p=0 dropout (BN train path)
    for blk in model.blocks:
        blk.drop_rate = 0.0
    model.train()
    with torch.no_grad():
        out_train = model(x)
    bn0_after = (
        model.blocks[0].norm.running_mean.clone().numpy(),
        model.blocks[0].norm.running_var.clone().numpy(),
    )

    arrs = {
        f"{tag}_x": x.numpy(),
        f"{tag}_out_inf": out_inf.numpy(),
        f"{tag}_out_train": out_train.numpy(),
        f"{tag}_bn0_mean_after": bn0_after[0],
        f"{tag}_bn0_var_after": bn0_after[1],
        f"{tag}_enc_w": model.encoder.weight.detach().numpy(),
        f"{tag}_enc_b": model.encoder.bias.detach().numpy(),
        f"{tag}_head_w": model.head.weight.detach().numpy(),
        f"{tag}_head_b": model.head.bias.detach().numpy(),
        **rs,
    }
    for i, blk in enumerate(model.blocks):
        p = f"{tag}_b{i}_"
        arrs[p + "A"] = blk.ssm.A_diag.detach().numpy()
        arrs[p + "B"] = blk.ssm.B.detach().numpy()
        arrs[p + "C"] = blk.ssm.C.detach().numpy()
        arrs[p + "D"] = blk.ssm.D.detach().numpy()
        arrs[p + "steps"] = blk.ssm.steps.detach().numpy()
        arrs[p + "glu_w1_w"] = blk.glu.w1.weight.detach().numpy()
        arrs[p + "glu_w1_b"] = blk.glu.w1.bias.detach().numpy()
        arrs[p + "glu_w2_w"] = blk.glu.w2.weight.detach().numpy()
        arrs[p + "glu_w2_b"] = blk.glu.w2.bias.detach().numpy()
    return arrs


def export_layer_only(tag, ssm, H, L, batch, seed):
    g = torch.Generator().manual_seed(seed)
    layer = LinOSSIMLayer(ssm, H, generator=g)
    u = torch.randn(batch, L, H, generator=g)
    with torch.no_grad():
        out = layer(u)
    return {
        f"{tag}_u": u.numpy(),
        f"{tag}_out": out.numpy(),
        f"{tag}_A": layer.A_diag.detach().numpy(),
        f"{tag}_B": layer.B.detach().numpy(),
        f"{tag}_C": layer.C.detach().numpy(),
        f"{tag}_D": layer.D.detach().numpy(),
        f"{tag}_steps": layer.steps.detach().numpy(),
    }


if __name__ == "__main__":
    arrs = {}
    # G1 config, full length
    arrs.update(export_model("g1", 6, 62, 16, 16, 2, L=405, batch=8, seed=11))
    # G3 config, shortened L for the full-model check
    arrs.update(export_model("g3", 2, 7, 64, 128, 5, L=1024, batch=2, seed=12))
    # G3-size SSM layer at FULL EigenWorms length
    arrs.update(export_layer_only("l3", 64, 128, L=17984, batch=2, seed=13))
    np.savez(os.path.join(OUT, "torch_side.npz"), **arrs)
    print("wrote", os.path.join(OUT, "torch_side.npz"),
          "| keys:", len(arrs))
