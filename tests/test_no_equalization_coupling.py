# pattern-port of pnn-multilayer tests/test_mrr_primitives.py::
#   test_mrr_primitives_no_soa_coupling (the source-grep negative test)
"""Decoupling hygiene: the salvaged package must carry NO references to
the source repo's equalization TRAINING STACK (the 'honest flag' gate of task
S0.0 — salvaged assets must not drag in the source equalization implementation).

S0.3-1b rewrite (S31-F5): the gate asserts the REAL invariant — the specific
source-stack *symbols/modules* are absent (the Critic-verified list) — NOT a
generic task token. The old gate banned task-framing words ("PAM4", "QPSK",
"HD_FEC", "ber_curve") that collide with the project's OWN registered PR-2 T-A
4-PAM equalization task; that forced legitimate vocabulary to be renamed and,
worse, would have let a contributor re-import the source stack under a neutral
name and slip past. Banning the source symbols is the invariant that actually
matters; the project's registered 4-PAM task vocabulary is allowed."""

import os
import re

import photonic_ssm


# The source-repo equalization training stack: module names, fiber-channel and
# DSP classes, and batched-engine entry points (Critic-verified absent from
# photonic_ssm/). These — not task-framing tokens — are the salvage-hygiene
# invariant: their presence would mean the MZI-specific training engine or the
# fiber-equalization assumptions leaked in.
FORBIDDEN = [
    # source equalization modules
    "equalization_multilayer", "equalization_nonlinear",
    "equalization_ringbank", "equalization_mrr_rc",
    # fiber channel / dual-pol DSP
    "ManakovFiber", "manakov", "generate_dp_qpsk", "viterbi_viterbi",
    "ParallelPol",
    # source training-engine classes / entry points
    "MultiLayerEqualizer", "MRRWeightBank",
    "compute_nmse_field", "forward_batched",
]


def _iter_package_sources():
    root = os.path.dirname(os.path.abspath(photonic_ssm.__file__))
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith(".py"):
                yield os.path.join(dirpath, fn)


def _strip_comments_and_docstrings(src: str) -> str:
    src = re.sub(r'"""[\s\S]*?"""', "", src)
    src = re.sub(r"'''[\s\S]*?'''", "", src)
    src = re.sub(r"#.*$", "", src, flags=re.MULTILINE)
    return src


def test_package_has_no_equalization_coupling():
    hits = []
    for path in _iter_package_sources():
        with open(path) as f:
            code = _strip_comments_and_docstrings(f.read())
        for tok in FORBIDDEN:
            if tok in code:
                hits.append((os.path.basename(path), tok))
    assert not hits, f"equalization coupling leaked into package: {hits}"


def test_package_runtime_is_torch_only():
    """requirements.txt promise: the package imports only torch + stdlib
    (no numpy, no scipy, no source-repo modules)."""
    import sys
    stdlib = set(sys.stdlib_module_names)
    offenders = []
    for path in _iter_package_sources():
        with open(path) as f:
            code = _strip_comments_and_docstrings(f.read())
        for m in re.finditer(
                r"^\s*(?:import|from)\s+([A-Za-z_][A-Za-z0-9_]*)",
                code, flags=re.MULTILINE):
            mod = m.group(1)
            if mod in ("torch", "photonic_ssm"):
                continue
            if mod not in stdlib:
                offenders.append((os.path.basename(path), mod))
    assert not offenders, f"non-torch third-party imports: {offenders}"
