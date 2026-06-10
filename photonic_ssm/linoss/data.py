"""Gate-i data plumbing (S0.2-1 / PR-1, PF-F6). torch + stdlib only (house rule).

Loads the OFFICIAL preprocessed UEA arrays (data.npy / labels.npy — value-exact
copies of the official data.pkl / labels.pkl jax arrays, converted once by
`scripts/extract_official_splits.py`, which runs the official process_uea.py
verbatim; its np.unique dedup both removes duplicates AND re-orders samples,
which is why the official pipeline is run rather than re-implemented) and the
per-seed split indices extracted from the official PRNG chain
(splits_official.json). Splits are therefore IDENTICAL to the published runs'
sample assignment (PR-1 split-reproduction pin).

Time channel: the official create_uea_dataset prepends ts = (T/L)*arange(L)
(T = 1 for both anchors) as channel 0. Labels: one-hot.

``OfficialLoaderPort`` replicates data_dir/dataloaders.py exactly:
  * loop(batch_size): infinite; fresh shuffle each epoch; yields only batches
    with end < size — the tail batch is ALWAYS dropped (even a full one when
    size % batch_size == 0; official quirk, kept).
  * loop_epoch(batch_size): sequential full batches with end < size, then the
    remainder batch always.
The shuffle permutations come from a torch.Generator (the official ones come
from jax PRNG; PR-1 pins the SPLIT assignment, not the batch-order stream —
framework-inherent, logged in the results entry).
"""

import ast
import json
import os
import struct

import torch

_NPY_DTYPES = {
    "<f4": torch.float32,
    "<f8": torch.float64,
    "<i4": torch.int32,
    "<i8": torch.int64,
}


def _load_npy(path):
    """Minimal NPY v1/v2 reader (C-order, little-endian) — keeps the package
    runtime torch+stdlib-only per the S0.0 requirements promise."""
    with open(path, "rb") as f:
        magic = f.read(6)
        if magic != b"\x93NUMPY":
            raise ValueError(f"{path}: not an NPY file")
        major = f.read(1)[0]
        f.read(1)  # minor
        if major == 1:
            hlen = struct.unpack("<H", f.read(2))[0]
        else:
            hlen = struct.unpack("<I", f.read(4))[0]
        header = ast.literal_eval(f.read(hlen).decode("latin1"))
        if header["fortran_order"]:
            raise ValueError(f"{path}: fortran order unsupported")
        dtype = _NPY_DTYPES[header["descr"]]
        buf = bytearray(f.read())  # writable copy: frombuffer needs it
    return torch.frombuffer(buf, dtype=dtype).reshape(header["shape"]).clone()


def load_gate_i_dataset(project_root, name, seed):
    """Returns dict with train/val/test tensors (time channel prepended,
    one-hot labels) for the official split of `seed`, + metadata."""
    proc = os.path.join(project_root, "data", "processed", "UEA", name)
    data = _load_npy(os.path.join(proc, "data.npy")).to(torch.float32)
    labels = _load_npy(os.path.join(proc, "labels.npy")).to(torch.int64)
    with open(os.path.join(proc, "splits_official.json")) as f:
        splits = json.load(f)

    n_classes = int(labels.max()) + 1
    onehot = torch.zeros(len(labels), n_classes, dtype=torch.float32)
    onehot[torch.arange(len(labels)), labels] = 1.0

    N, L, _C = data.shape
    # T = 1 (both anchors). Multiply form, NOT arange/L: the official jax code
    # computes (T/L) * arange as a float32 multiply, and ulp-level rounding
    # differs between f32(i)*f32(1/L) and f32(i)/f32(L).
    ts = torch.arange(L, dtype=torch.float32) * (1.0 / L)
    ts = ts.view(1, L, 1).expand(N, L, 1)
    data = torch.cat([ts, data], dim=2)

    sp = splits["splits"][str(seed)]
    out = {}
    for part in ("train", "val", "test"):
        idx = torch.tensor(sp[part], dtype=torch.int64)
        out[f"X_{part}"] = data[idx].contiguous()
        out[f"y_{part}"] = onehot[idx].contiguous()
    out["data_dim"] = data.shape[2]
    out["n_classes"] = n_classes
    out["N"] = N
    out["gated"] = sp["gated"]
    out["data_sha256"] = splits["data_pkl_sha256"]
    return out


class OfficialLoaderPort:
    """1:1 port of the official Dataloader (raw time-series branch)."""

    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.size = len(X)

    def loop(self, batch_size, generator):
        if batch_size > self.size:
            raise ValueError("Batch size larger than dataset size")
        if batch_size == self.size:
            while True:
                yield self.X, self.y
        while True:
            perm = torch.randperm(self.size, generator=generator)
            start, end = 0, batch_size
            while end < self.size:  # official: strict < — tail always dropped
                sel = perm[start:end]
                yield self.X[sel], self.y[sel]
                start = end
                end = start + batch_size

    def loop_epoch(self, batch_size):
        if batch_size > self.size:
            raise ValueError("Batch size larger than dataset size")
        if batch_size == self.size:
            yield self.X, self.y
            return
        start, end = 0, batch_size
        while end < self.size:
            yield self.X[start:end], self.y[start:end]
            start = end
            end = start + batch_size
        yield self.X[start:], self.y[start:]
