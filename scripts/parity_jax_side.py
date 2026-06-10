"""S0.2-1 parity check, jax side (step 2 of 3). Run with /tmp/linoss_venv.

Loads torch_side.npz, builds the OFFICIAL LinOSS model (tk-rusch/linoss @
/tmp/linoss_official, equinox 0.11.4), transplants the torch weights leaf by
leaf, runs the same inputs, saves outputs for compare_parity.py.
"""

import os
import sys

import numpy as np

sys.path.insert(0, "/tmp/linoss_official")

import equinox as eqx
import jax
import jax.numpy as jnp
import jax.random as jr

from models.LinOSS import LinOSS, LinOSSLayer

OUT = "/tmp/parity_gate_i"
Z = np.load(os.path.join(OUT, "torch_side.npz"))


def build_official(tag, num_blocks, data_dim, ssm, H, n_classes):
    model = LinOSS(
        num_blocks, data_dim, ssm, H, n_classes,
        classification=True, output_step=1, discretization="IM",
        key=jr.PRNGKey(0),
    )
    state = eqx.nn.State(model)

    def rep(model, where, val):
        return eqx.tree_at(where, model, jnp.asarray(val))

    model = rep(model, lambda m: m.linear_encoder.weight, Z[f"{tag}_enc_w"])
    model = rep(model, lambda m: m.linear_encoder.bias, Z[f"{tag}_enc_b"])
    model = rep(model, lambda m: m.linear_layer.weight, Z[f"{tag}_head_w"])
    model = rep(model, lambda m: m.linear_layer.bias, Z[f"{tag}_head_b"])
    for i in range(num_blocks):
        p = f"{tag}_b{i}_"
        model = rep(model, lambda m, i=i: m.blocks[i].ssm.A_diag, Z[p + "A"])
        model = rep(model, lambda m, i=i: m.blocks[i].ssm.B, Z[p + "B"])
        model = rep(model, lambda m, i=i: m.blocks[i].ssm.C, Z[p + "C"])
        model = rep(model, lambda m, i=i: m.blocks[i].ssm.D, Z[p + "D"])
        model = rep(model, lambda m, i=i: m.blocks[i].ssm.steps, Z[p + "steps"])
        model = rep(model, lambda m, i=i: m.blocks[i].glu.w1.weight, Z[p + "glu_w1_w"])
        model = rep(model, lambda m, i=i: m.blocks[i].glu.w1.bias, Z[p + "glu_w1_b"])
        model = rep(model, lambda m, i=i: m.blocks[i].glu.w2.weight, Z[p + "glu_w2_w"])
        model = rep(model, lambda m, i=i: m.blocks[i].glu.w2.bias, Z[p + "glu_w2_b"])
        # transplant BN running stats + clear first_time
        state = state.set(
            model.blocks[i].norm.state_index,
            (jnp.asarray(Z[f"{tag}_bn{i}_mean"]), jnp.asarray(Z[f"{tag}_bn{i}_var"])),
        )
        state = state.set(model.blocks[i].norm.first_time_index, jnp.array(False))
    return model, state


def run_model(tag, num_blocks, data_dim, ssm, H, n_classes, arrs):
    model, state = build_official(tag, num_blocks, data_dim, ssm, H, n_classes)
    x = jnp.asarray(Z[f"{tag}_x"])
    key = jr.PRNGKey(42)

    inf_model = eqx.tree_inference(model, value=True)
    out_inf, _ = jax.vmap(
        inf_model, axis_name="batch", in_axes=(0, None, None), out_axes=(0, None)
    )(x, state, key)
    arrs[f"{tag}_out_inf_jax"] = np.asarray(out_inf)

    # train mode with p = 0 dropout (BN train path: EMA update + normalize)
    train_model = model
    for i in range(num_blocks):
        train_model = eqx.tree_at(
            lambda m, i=i: m.blocks[i].drop.p, train_model, 0.0
        )
    out_train, state_after = jax.vmap(
        train_model, axis_name="batch", in_axes=(0, None, None), out_axes=(0, None)
    )(x, state, key)
    arrs[f"{tag}_out_train_jax"] = np.asarray(out_train)
    bn0_mean, bn0_var = state_after.get(train_model.blocks[0].norm.state_index)
    arrs[f"{tag}_bn0_mean_after_jax"] = np.asarray(bn0_mean)
    arrs[f"{tag}_bn0_var_after_jax"] = np.asarray(bn0_var)


def run_layer_only(tag, ssm, H, arrs):
    layer = LinOSSLayer(ssm, H, "IM", key=jr.PRNGKey(0))
    key_map = {"A_diag": "A", "B": "B", "C": "C", "D": "D", "steps": "steps"}
    for attr, zkey in key_map.items():
        layer = eqx.tree_at(
            lambda l, attr=attr: getattr(l, attr),
            layer,
            jnp.asarray(Z[f"{tag}_{zkey}"]),
        )
    u = jnp.asarray(Z[f"{tag}_u"])
    out = jax.vmap(layer)(u)
    arrs[f"{tag}_out_jax"] = np.asarray(out)


if __name__ == "__main__":
    arrs = {}
    run_model("g1", 6, 62, 16, 16, 2, arrs)
    run_model("g3", 2, 7, 64, 128, 5, arrs)
    run_layer_only("l3", 64, 128, arrs)
    np.savez(os.path.join(OUT, "jax_side.npz"), **arrs)
    print("wrote", os.path.join(OUT, "jax_side.npz"), "| keys:", len(arrs))
