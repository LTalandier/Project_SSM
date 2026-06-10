"""S0.2-1 / PF-F6: run the OFFICIAL LinOSS preprocessing once + extract the exact
per-seed 70/15/15 split indices.

Run with the scratch venv (/tmp/linoss_venv: jax 0.4.28, sktime 0.30.1 — the repo pins),
NOT the project torch env:

    /tmp/linoss_venv/bin/python scripts/extract_official_splits.py

Step 1 calls the official `convert_all_files` (tk-rusch/linoss @ data_dir/process_uea.py,
cloned at /tmp/linoss_official) on data/raw/UEA/Multivariate_arff/{Heartbeat,EigenWorms}.
NOTE the official dedup step uses np.unique(axis=0), which both removes duplicates AND
re-orders samples lexicographically — data.pkl order != ARFF order. The split permutation
indexes into THIS order, which is why we run their pipeline verbatim instead of re-implementing.

Step 2 replicates, character-for-character, the PRNG chain that produces the split:
  train.py:        key = jr.PRNGKey(seed)
                   datasetkey, modelkey, trainkey, key = jr.split(key, 4)
  datasets.py (dataset_generator, use_presplit=False, idxs=None):
                   permkey, key = jr.split(key)        # key here IS datasetkey
                   bound1 = int(N * 0.7)
                   bound2 = int(N * 0.85)
                   idxs_new = jr.permutation(permkey, N)
                   train = idxs_new[:bound1]; val = idxs_new[bound1:bound2]; test = idxs_new[bound2:]

Output: data/processed/UEA/{name}/splits_official.json  (+ sha256 of data.pkl/labels.pkl).
"""

# pickle use is safe here: every .pkl read below is created on THIS machine, in this
# same run, by the official preprocessing acting on plain-text ARFF inputs (the official
# pipeline's on-disk format, kept for protocol fidelity). No foreign pickles are loaded.
import hashlib
import json
import os
import pickle
import sys

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT, "data")
OFFICIAL = "/tmp/linoss_official"

GATED_SEEDS = [2345, 3456, 4567, 5678, 6789]   # PR-1 gated (Walker protocol)
ANNEX_SEEDS = [7890, 8901, 9012]               # PR-1 non-gating annex (PF-F8g)
DATASETS = ["Heartbeat", "EigenWorms"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    sys.path.insert(0, OFFICIAL)
    from data_dir.process_uea import convert_all_files  # official, verbatim

    print("=== Step 1: official preprocessing (process_uea.convert_all_files) ===")
    convert_all_files(DATA_DIR)

    print("=== Step 2: split extraction (official PRNG chain, replicated verbatim) ===")
    import jax.random as jr

    import numpy as np

    for name in DATASETS:
        proc = os.path.join(DATA_DIR, "processed", "UEA", name)
        with open(os.path.join(proc, "data.pkl"), "rb") as f:
            data = pickle.load(f)
        with open(os.path.join(proc, "labels.pkl"), "rb") as f:
            labels = pickle.load(f)
        # value-exact plain-numpy copies for the torch env (no jax there)
        np.save(os.path.join(proc, "data.npy"), np.asarray(data, dtype=np.float32))
        np.save(os.path.join(proc, "labels.npy"), np.asarray(labels, dtype=np.int64))
        N = len(data)
        out = {
            "dataset": name,
            "N_after_official_dedup": N,
            "data_shape": list(data.shape),
            "data_pkl_sha256": sha256(os.path.join(proc, "data.pkl")),
            "labels_pkl_sha256": sha256(os.path.join(proc, "labels.pkl")),
            "official_repo": "https://github.com/tk-rusch/linoss",
            "jax_version": __import__("jax").__version__,
            "splits": {},
        }
        for seed in GATED_SEEDS + ANNEX_SEEDS:
            key = jr.PRNGKey(seed)
            datasetkey, modelkey, trainkey, key = jr.split(key, 4)   # train.py order
            permkey, key2 = jr.split(datasetkey)                      # dataset_generator
            bound1 = int(N * 0.7)
            bound2 = int(N * 0.85)
            idxs_new = jr.permutation(permkey, N)
            out["splits"][str(seed)] = {
                "gated": seed in GATED_SEEDS,
                "train": [int(i) for i in idxs_new[:bound1]],
                "val": [int(i) for i in idxs_new[bound1:bound2]],
                "test": [int(i) for i in idxs_new[bound2:]],
            }
            print(f"{name} seed {seed}: N={N} train={bound1} val={bound2-bound1} "
                  f"test={N-bound2} head={[int(i) for i in idxs_new[:5]]}")
        dst = os.path.join(proc, "splits_official.json")
        with open(dst, "w") as f:
            json.dump(out, f)
        print(f"wrote {dst}")


if __name__ == "__main__":
    main()
