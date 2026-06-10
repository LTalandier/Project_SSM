"""photonic_ssm.linoss — the in-house recurrence layer + Gate-i (PR-1) stack.

New code (S0.2-1). The layer here is THE one the Stage-0 bake-off extends
downstream (S0.3+): a complex-diagonal (S4D/DSS-class) recurrence with an
inter-mode coupling hook mu — per resolved D-2026-06-08-2, one ring = one
complex pole, LinOSS = the uncoupled, real-I/O conjugate-pair special case.

Modules:
    layer.py   associative-scan engine; LinOSSIMLayer (the Gate-i configuration,
               computing the published LinOSS-IM recurrence verbatim);
               ComplexDiagSSM (the bake-off core, mu hook; mu = 0 in S0.2-1)
               + the exact LinOSS-IM -> complex-diagonal equivalence map.
    stack.py   the published architecture around the layer, ported 1:1 from the
               official repo (tk-rusch/linoss): EMA BatchNorm (equinox 0.11.4
               semantics), GLU, block (BN -> SSM -> GELU -> drop -> GLU -> drop
               -> skip), mean-pool softmax head.
    data.py    Gate-i data: official processed UEA pickles + the PF-F6
               split indices extracted from the official PRNG chain; a 1:1 port
               of the official Dataloader (incl. its tail-batch-dropping loop).
    train.py   the Walker-protocol training loop, ported 1:1 from the official
               train.py (Adam, eval cadence, early stopping, test-at-best-val).

Reference behavior (PR-1, frozen): the official code, not the paper text.
Official repo cloned at /tmp/linoss_official for split extraction and
debugging cross-checks only — it is never the tested object.
"""

from photonic_ssm.linoss.layer import (
    ComplexDiagSSM,
    LinOSSIMLayer,
    assoc_scan_2x2,
    assoc_scan_diag,
)
from photonic_ssm.linoss.stack import GateIClassifier

__all__ = [
    "LinOSSIMLayer",
    "ComplexDiagSSM",
    "GateIClassifier",
    "assoc_scan_2x2",
    "assoc_scan_diag",
]
