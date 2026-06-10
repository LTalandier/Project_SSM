"""S0.2-1 GPU environment-parity gate (the D-2026-06-10-2 cloud condition).

Validation chain composition: the S0.2-1 record established
CPU-torch ≡ official-JAX (transplanted weights, full-model probs ~2.4e-7,
BN updates ≤1.2e-7, L=17,984 layer 1.5e-5). This script establishes
GPU-torch ≡ CPU-torch on the SAME fixtures (identical weights/inputs by
seed), so GPU-torch ≡ official-JAX by composition. Run ON the GPU box
BEFORE any gated run; a FAIL blocks the gated runs.

Also self-checks training-step determinism on CUDA (deterministic
algorithms + TF32 off + CUBLAS_WORKSPACE_CONFIG): two identical 20-step
mini-trainings must produce bit-equal losses — the reported gated number
must be reproducible in this environment.

Fixture builders mirror scripts/parity_torch_side.py construction order
exactly (same seeds 11/12/13 -> identical weight/input bits).
"""

import os
import sys

import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from photonic_ssm.linoss.layer import LinOSSIMLayer
from photonic_ssm.linoss.stack import GateIClassifier

# thresholds: ~10x the CPU<->JAX deltas of record (2.4e-7 / 1.2e-7 / 1.5e-5)
TOL_FULL_MODEL = 2e-6
TOL_BN_STATS = 2e-6
TOL_LAYER_LONG = 1e-4


def _build_model(num_blocks, data_dim, ssm, H, n_classes, L, batch, seed):
    """Same construction order as parity_torch_side.export_model (seeds
    11/12): model, input, then BN buffer randomization from one generator."""
    g = torch.Generator().manual_seed(seed)
    model = GateIClassifier(num_blocks, data_dim, ssm, H, n_classes, generator=g)
    x = torch.randn(batch, L, data_dim, generator=g)
    for blk in model.blocks:
        mean = torch.randn(H, generator=g) * 0.3
        var = torch.rand(H, generator=g) + 0.5
        blk.norm.running_mean.copy_(mean)
        blk.norm.running_var.copy_(var)
        blk.norm.first_time.fill_(False)
        blk.drop_rate = 0.0
    return model, x


def _outputs(model, x):
    model.eval()
    with torch.no_grad():
        out_inf = model(x)
    model.train()
    with torch.no_grad():
        out_train = model(x)
    bn0_m = model.blocks[0].norm.running_mean.clone()
    bn0_v = model.blocks[0].norm.running_var.clone()
    return out_inf, out_train, bn0_m, bn0_v


def check_full_model(tag, cfg, results):
    model_cpu, x_cpu = _build_model(*cfg)
    inf_c, tr_c, m_c, v_c = _outputs(model_cpu, x_cpu)

    model_gpu, x_gpu = _build_model(*cfg)  # identical bits by seed
    model_gpu = model_gpu.to("cuda")
    inf_g, tr_g, m_g, v_g = _outputs(model_gpu, x_gpu.to("cuda"))

    d_inf = (inf_c - inf_g.cpu()).abs().max().item()
    d_tr = (tr_c - tr_g.cpu()).abs().max().item()
    d_bn = max((m_c - m_g.cpu()).abs().max().item(),
               (v_c - v_g.cpu()).abs().max().item())
    results.append((f"{tag} full-model inference probs", d_inf, TOL_FULL_MODEL))
    results.append((f"{tag} full-model train-mode probs", d_tr, TOL_FULL_MODEL))
    results.append((f"{tag} BN running stats after train pass", d_bn, TOL_BN_STATS))


def check_layer_long(results):
    g = torch.Generator().manual_seed(13)
    layer = LinOSSIMLayer(64, 128, generator=g)
    u = torch.randn(2, 17_984, 128, generator=g)
    with torch.no_grad():
        out_c = layer(u)
        out_g = layer.to("cuda")(u.to("cuda"))
    d = (out_c - out_g.cpu()).abs().max().item()
    results.append(("L=17,984 SSM layer (G3 size)", d, TOL_LAYER_LONG))


def check_train_determinism(results):
    """Two identical 20-step trainings on CUDA -> bit-equal loss streams."""
    def run_once():
        g_init = torch.Generator().manual_seed(99)
        model = GateIClassifier(2, 7, 64, 128, 5, generator=g_init).to("cuda")
        g_data = torch.Generator().manual_seed(100)
        X = torch.randn(8, 512, 7, generator=g_data).to("cuda")
        y = torch.zeros(8, 5)
        y[torch.arange(8), torch.randint(0, 5, (8,), generator=g_data)] = 1.0
        y = y.to("cuda")
        g_drop = torch.Generator().manual_seed(101)
        opt = torch.optim.Adam(model.parameters(), lr=1e-3,
                               betas=(0.9, 0.999), eps=1e-8)
        model.train()
        losses = []
        for _ in range(20):
            p = model(X, dropout_generator=g_drop)
            loss = (-(y * torch.log(p + 1e-8)).sum(dim=1)).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
            losses.append(loss.detach().cpu().clone())
        return torch.stack(losses)

    l1, l2 = run_once(), run_once()
    d = (l1 - l2).abs().max().item()
    results.append(("20-step train determinism (bit-equal)", d, 0.0))


def main():
    assert torch.cuda.is_available(), "no CUDA device"
    if os.environ.get("CUBLAS_WORKSPACE_CONFIG") != ":4096:8":
        print("WARNING: CUBLAS_WORKSPACE_CONFIG != :4096:8 — determinism "
              "check may fail or be meaningless")
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.use_deterministic_algorithms(True)

    results = []
    # (num_blocks, data_dim, ssm, H, n_classes, L, batch, seed) — fixture
    # configs identical to parity_torch_side.py
    check_full_model("G1", (6, 62, 16, 16, 2, 405, 8, 11), results)
    check_full_model("G3", (2, 7, 64, 128, 5, 1024, 2, 12), results)
    check_layer_long(results)
    check_train_determinism(results)

    print(f"\nGPU: {torch.cuda.get_device_name(0)} | torch {torch.__version__} "
          f"| cuda {torch.version.cuda}")
    ok = True
    for name, delta, tol in results:
        verdict = "PASS" if delta <= tol else "FAIL"
        ok &= delta <= tol
        print(f"  [{verdict}] {name}: max|delta| = {delta:.3e} (tol {tol:g})")
    print("\nPARITY GATE:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
