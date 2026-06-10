"""S0.2-1R GA-F1: archived regeneration of the ours-annex 600-step trap screens.

Local CPU, torch CPU generators for init/shuffle/dropout (the recorded CPU reference
path), deterministic algorithms on. Per-step training loss + total squared gradient
norm are archived as JSONL. Pre-declared classifier (PREDECLARATION.md §C): TRAP iff
the total gradient is exactly 0.0 from some step k <= 600 onward (transient zeros
followed by recovery do not count); ALIVE otherwise.

Diagnostic only — not a gated run; no eval, no tuning, frozen protocol untouched.

Usage:
    python scripts/annex_trap_screen.py SEED OUTDIR [NTHREADS]
"""
import json
import sys
import time

import torch

from photonic_ssm.linoss.data import OfficialLoaderPort, load_gate_i_dataset
from photonic_ssm.linoss.stack import GateIClassifier

REPO_ROOT = "/home/lucas/Documents/Project_SSM"
N_STEPS = 600


def main() -> None:
    seed = int(sys.argv[1])
    outdir = sys.argv[2]
    nthreads = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    torch.set_num_threads(nthreads)
    torch.use_deterministic_algorithms(True)

    data = load_gate_i_dataset(REPO_ROOT, "EigenWorms", seed)
    g_init = torch.Generator().manual_seed(seed)
    model = GateIClassifier(
        2, data["data_dim"], 64, 128, data["n_classes"], generator=g_init
    )
    g_batch = torch.Generator().manual_seed(seed + 1_000_003)
    g_drop = torch.Generator().manual_seed(seed + 2_000_003)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3, betas=(0.9, 0.999), eps=1e-8)
    batches = OfficialLoaderPort(data["X_train"], data["y_train"]).loop(4, g_batch)
    model.train()

    path = f"{outdir}/EigenWorms_annexscreen_seed{seed}.jsonl"
    dead_from = None
    t0 = time.time()
    with open(path, "w") as fh:
        fh.write(
            json.dumps(
                {
                    "record": "config",
                    "purpose": "S0.2-1R GA-F1 ours-annex 600-step trap screen",
                    "seed": seed,
                    "n_steps": N_STEPS,
                    "device": "cpu",
                    "torch": torch.__version__,
                    "threads": nthreads,
                    "deterministic_algorithms": True,
                    "generators": {
                        "init": "cpu manual_seed(seed)",
                        "batch": "cpu manual_seed(seed + 1000003)",
                        "dropout": "cpu manual_seed(seed + 2000003)",
                    },
                    "loss": "mean(-sum(y*log(p+1e-8)))  # official objective, ported",
                    "classifier": "TRAP iff grad_sq_total == 0.0 from some k<=600 onward",
                }
            )
            + "\n"
        )
        for step in range(N_STEPS):
            Xb, yb = next(batches)
            p = model(Xb, dropout_generator=g_drop)
            loss = (-(yb * torch.log(p + 1e-8)).sum(dim=1)).mean()
            opt.zero_grad()
            loss.backward()
            gsq = sum(
                float((q.grad**2).sum())
                for q in model.parameters()
                if q.grad is not None
            )
            opt.step()
            if gsq == 0.0 and dead_from is None:
                dead_from = step
            elif gsq > 0.0:
                dead_from = None
            fh.write(
                json.dumps({"step": step, "loss": float(loss), "grad_sq_total": gsq})
                + "\n"
            )
        verdict = "TRAP" if dead_from is not None else "ALIVE"
        fh.write(
            json.dumps(
                {
                    "record": "summary",
                    "seed": seed,
                    "verdict": verdict,
                    "trapped_since_step": dead_from,
                    "final_loss": float(loss),
                    "wall_seconds": round(time.time() - t0, 1),
                }
            )
            + "\n"
        )
    tag = f"TRAP since step {dead_from}" if dead_from is not None else "ALIVE"
    print(f"seed {seed}: {tag}  ({time.time() - t0:.0f}s)", flush=True)


if __name__ == "__main__":
    main()
