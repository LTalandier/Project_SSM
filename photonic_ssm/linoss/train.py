"""The Walker-protocol training loop, ported 1:1 from the official train.py
(S0.2-1 / PR-1 closure rule: every unstated protocol detail resolves to the
official repo's behavior; NO hyperparameter tuning).

Official behaviors replicated exactly:
  * optax.adam(lr) == torch.optim.Adam(lr, betas=(0.9, 0.999), eps=1e-8),
    constant lr (config lr_scheduler = identity), no weight decay, no clip.
  * loss = mean_batch( -sum_c y_c * log(p_c + 1e-8) ) on softmax outputs.
  * Train on `loop` batches (shuffled, tail-dropped) for up to num_steps =
    100_000 steps; every print_steps = 1_000 steps evaluate train + val
    accuracy over `loop_epoch` in inference mode (dropout off, BN running
    stats, no BN state update).
  * Early stopping / model selection, official operators kept verbatim:
    improvement if val >= best (ties INCLUDE re-evaluating test);
    no-improvement counter incremented if val <= best (ties count); counter
    reset only on strict improvement; break when counter > 10. The reported
    test accuracy is the one measured at the LAST improvement event
    (test-at-best-val). Initial best = 0.0.
  * BN state updates happen only on training steps (the eval passes use a
    frozen copy of the running stats).

Differences inherent to the framework (logged, PR-1-compatible): jax PRNG
streams (init draws / batch order / dropout masks) are replaced by a
per-run torch.Generator seeded with the SAME seed; distributions and the
split assignment are identical (PF-F6 pins the split, not the PRNG bits).
"""

import json
import time

import torch

from photonic_ssm.linoss.data import OfficialLoaderPort


def _accuracy(model, X, y, batch_size):
    """Full-epoch accuracy in inference mode (official eval loops)."""
    model.eval()
    preds = []
    labs = []
    loader = OfficialLoaderPort(X, y)
    with torch.no_grad():
        for Xb, yb in loader.loop_epoch(batch_size):
            p = model(Xb)
            preds.append(p.argmax(dim=1))
            labs.append(yb.argmax(dim=1))
    model.train()
    return float((torch.cat(preds) == torch.cat(labs)).float().mean())


def train_gate_i(
    model,
    data,
    *,
    lr=1e-3,
    batch_size,
    num_steps=100_000,
    print_steps=1_000,
    seed,
    jsonl_path=None,
):
    """Returns a result dict; optionally streams eval records to JSONL."""
    g_batch = torch.Generator().manual_seed(seed + 1_000_003)
    # Dropout-mask generator is DEVICE-NATIVE (CPU MT19937 on CPU runs —
    # bit-identical to the G1 gated record; CUDA Philox on GPU runs). The
    # stream identity is framework-inherent and not protocol-pinned (PR-1
    # pins the split assignment, not PRNG bits — see module docstring);
    # distribution, batch-shared semantics, and per-run seeding are
    # unchanged. Drawing the (L, H)-sized masks on the compute device
    # avoids a ~950 ms/step CPU-draw+transfer stall at G3 length.
    dev = data["X_train"].device
    g_drop = torch.Generator(device=dev).manual_seed(seed + 2_000_003)

    opt = torch.optim.Adam(model.parameters(), lr=lr, betas=(0.9, 0.999), eps=1e-8)
    train_loader = OfficialLoaderPort(data["X_train"], data["y_train"])

    log_f = open(jsonl_path, "a") if jsonl_path else None

    def log(rec):
        if log_f:
            log_f.write(json.dumps(rec) + "\n")
            log_f.flush()

    best_vals = [0.0]  # official val_metric_for_best_model
    no_improv = 0
    test_metric = None
    running_loss = 0.0
    t0 = time.time()
    model.train()
    stopped_at = num_steps

    batches = train_loader.loop(batch_size, g_batch)
    for step in range(num_steps):
        Xb, yb = next(batches)
        p = model(Xb, dropout_generator=g_drop)
        loss = (-(yb * torch.log(p + 1e-8)).sum(dim=1)).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        running_loss += float(loss.detach())

        if (step + 1) % print_steps == 0:
            train_acc = _accuracy(model, data["X_train"], data["y_train"], batch_size)
            val_acc = _accuracy(model, data["X_val"], data["y_val"], batch_size)
            rec = {
                "step": step + 1,
                "loss": running_loss / print_steps,
                "train_acc": train_acc,
                "val_acc": val_acc,
                "elapsed_s": round(time.time() - t0, 1),
            }
            best = max(best_vals)
            # Official ordering kept verbatim: the no-improv branch breaks
            # IMMEDIATELY (before the improvement/test-eval check) — a tie
            # (val == best) both increments the counter and, if not broken,
            # re-evaluates test.
            stop = False
            if val_acc <= best:
                no_improv += 1
                if no_improv > 10:
                    stop = True
            else:
                no_improv = 0
            if not stop and val_acc >= best:
                best_vals.append(val_acc)
                test_metric = _accuracy(model, data["X_test"], data["y_test"], batch_size)
                rec["test_acc_at_improv"] = test_metric
            running_loss = 0.0
            log(rec)
            if stop:
                stopped_at = step + 1
                break

    if log_f:
        log_f.close()
    return {
        "test_acc": test_metric,
        "best_val": max(best_vals),
        "steps_run": stopped_at,
        "wall_s": round(time.time() - t0, 1),
    }
