# Ledger timestamp

`head_2026-08-05.txt` is the original anchored record; it has not been changed.
On 2026-09-13, `ots upgrade head_2026-08-05.txt.ots` retrieved completed Bitcoin
attestations from the original calendars. The upgraded proof includes heights
961165, 961189, and 961200. The original pending receipt remains in Git history.

`ots info` parses the completed paths. `ots verify` checked the local file linkage
but could not complete chain verification here because no Bitcoin RPC node is
configured. A verifier with a trusted Bitcoin node can run:

```bash
ots verify timestamps/head_2026-08-05.txt.ots
```

A verified proof establishes existence of the anchored material by the relevant
block date. It does not independently establish the actual execution times of
experiments, and this older anchor does not cover the September correction run.
