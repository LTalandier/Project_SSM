"""S0.2-1 Gate-i run: one (dataset, seed) Walker-protocol training run.

Usage (from repo root):
    PYTHONPATH=. python3 scripts/run_gate_i.py --dataset Heartbeat --seed 2345

Frozen config (PR-1, verbatim — no other values accepted):
    G1 Heartbeat:  lr 1e-3, hidden 16,  state 16, blocks 6, batch 32
    G3 EigenWorms: lr 1e-3, hidden 128, state 64, blocks 2, batch 4
    num_steps 100_000, print_steps 1_000, T = 1, include_time = True,
    seeds: gated {2345, 3456, 4567, 5678, 6789} + annex {7890, 8901, 9012}.

Output: results/s0_2/gate_i/{dataset}_seed{seed}.jsonl (eval trajectory)
        + a final "summary" record (test-at-best-val, steps, wall time,
        param counts, split hash).
"""

import argparse
import json
import os
import sys
import time

import torch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from photonic_ssm.linoss.data import load_gate_i_dataset
from photonic_ssm.linoss.stack import GateIClassifier
from photonic_ssm.linoss.train import train_gate_i

CONFIGS = {
    "Heartbeat": dict(num_blocks=6, H=16, ssm=16, batch_size=32),
    "EigenWorms": dict(num_blocks=2, H=128, ssm=64, batch_size=4),
}
PUBLISHED_COUNTS = {"Heartbeat": 10_936, "EigenWorms": 134_279}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, choices=list(CONFIGS))
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--threads", type=int, default=0)
    ap.add_argument("--num-steps", type=int, default=100_000)
    ap.add_argument("--print-steps", type=int, default=1_000)
    ap.add_argument("--device", default="cpu",
                    help="cpu (default) or cuda. cuda runs true fp32 "
                         "(TF32 off) + deterministic algorithms; all RNG "
                         "streams stay on CPU generators (identical to the "
                         "CPU run design). Gated by parity_gpu_side.py.")
    args = ap.parse_args()

    if args.threads > 0:
        torch.set_num_threads(args.threads)

    device = torch.device(args.device)
    gpu_name = None
    if device.type == "cuda":
        # True float32: the gated statistic must not silently move to TF32.
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.backends.cudnn.allow_tf32 = False
        # Reproducibility of the reported number on this environment
        # (requires CUBLAS_WORKSPACE_CONFIG=:4096:8 in the env).
        torch.use_deterministic_algorithms(True)
        gpu_name = torch.cuda.get_device_name(0)

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cfg = CONFIGS[args.dataset]
    data = load_gate_i_dataset(root, args.dataset, args.seed)
    for k in list(data):
        if k.startswith(("X_", "y_")):
            data[k] = data[k].to(device)

    # init on CPU with the seeded CPU generator (identical weight bits to a
    # CPU run), then move
    g_init = torch.Generator().manual_seed(args.seed)
    model = GateIClassifier(
        cfg["num_blocks"], data["data_dim"], cfg["ssm"], cfg["H"],
        data["n_classes"], generator=g_init,
    ).to(device)
    trainable, published_conv = model.param_counts()

    out_dir = os.path.join(root, "results", "s0_2", "gate_i")
    os.makedirs(out_dir, exist_ok=True)
    jsonl = os.path.join(out_dir, f"{args.dataset}_seed{args.seed}.jsonl")
    with open(jsonl, "a") as f:
        f.write(json.dumps({
            "record": "config", "dataset": args.dataset, "seed": args.seed,
            "gated": data["gated"], "config": cfg, "lr": 1e-3,
            "num_steps": args.num_steps, "print_steps": args.print_steps,
            "data_dim": data["data_dim"], "n_classes": data["n_classes"],
            "split_sizes": [len(data["X_train"]), len(data["X_val"]), len(data["X_test"])],
            "param_count_trainable": trainable,
            "param_count_published_convention": published_conv,
            "param_count_published_reference": PUBLISHED_COUNTS[args.dataset],
            "data_sha256": data["data_sha256"],
            "torch_version": torch.__version__,
            "threads": torch.get_num_threads(),
            "device": str(device),
            "gpu_name": gpu_name,
            "tf32_disabled": device.type == "cuda",
            "deterministic_algorithms": device.type == "cuda",
            "started_unix": time.time(),
        }) + "\n")

    res = train_gate_i(
        model, data, lr=1e-3, batch_size=cfg["batch_size"],
        num_steps=args.num_steps, print_steps=args.print_steps,
        seed=args.seed, jsonl_path=jsonl,
    )
    with open(jsonl, "a") as f:
        f.write(json.dumps({"record": "summary", "dataset": args.dataset,
                            "seed": args.seed, **res}) + "\n")
    print(f"[{args.dataset} seed {args.seed}] test={res['test_acc']:.6f} "
          f"best_val={res['best_val']:.6f} steps={res['steps_run']} "
          f"wall={res['wall_s']}s")


if __name__ == "__main__":
    main()
