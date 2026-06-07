"""photonic_ssm — Stage-0 toolkit for the in-situ-trained photonic SSM on SiN.

Repo layout (S0.0, selective salvage per `shared/tooling_recon.md` §4):

    platforms.py        SiN/Si/InP platform-constants registry      [salvaged]
    gain.py             instantaneous gain / ASE / NL functions     [salvaged]
    dynamic_gain.py     rate-equation gain (incl. autograd path)    [salvaged]
    static_rings.py     static CW ring transfer references + drift  [salvaged + new refs]
    estimators/spsa.py  SPSA + FD diagnostics + pass accounting     [salvaged]
    baselines/          ridge readout (reservoir baseline, §5.3)    [salvaged]
    runner/             resume-safe sweep scaffold + JSONL logging  [pattern salvage]

The SSM core (dynamical CMT ring model, LinOSS layer, S0.3 substrate,
PAT / adjoint / RHEL estimators) is NOT here — it is new code, S0.1+.

Two architecture constraints, binding on all S0.1+ core code
(task S0.0 deliverable 3; recon §3 anti-pattern warning):

(3a) GRADIENTS MUST FLOW THROUGH THE OPTICAL STATE. Substrate dynamics
     must never integrate the optical field inside `torch.no_grad()` or
     detach it (the forward-only style of pnn-multilayer's channel
     models is fatal here: BPTT reference, PAT twin and the adjoint all
     need d(loss)/d(state)). Pattern to copy:
     `dynamic_gain.TrainingAwareDynamicSOAPerMode` (checkpointed unroll).

(3b) EXPOSE FULL STATE TRAJECTORIES. The substrate / forward-model API
     must return (or make retrievable) the full internal state
     trajectory x_{1..T}, not just the output sequence — the adjoint
     and RHEL estimators consume trajectories, and the reservoir
     baseline reads state taps. (pnn-multilayer's `CascadedMRR_RC.forward`
     hides intermediate state; do not repeat that.)
"""

__version__ = "0.0.1"  # S0.0 — salvage skeleton; no SSM core yet
