#!/usr/bin/env bash
# S0.2-1: run seeds for one anchor, N_PAR at a time.
# Usage: bash scripts/run_gate_i_all.sh <Heartbeat|EigenWorms> <N_PAR> <THREADS_PER_RUN>
# SEEDS_OVERRIDE="2345 3456 ..." restricts the seed list (default: 5 gated + 3 annex).
# D-2026-06-10-2 ruling: G3 runs gated-5 first (3-parallel), annex-3 trails at idle.
set -u
DS="$1"; NPAR="${2:-4}"; THREADS="${3:-5}"
cd "$(dirname "$0")/.."
read -ra SEEDS <<< "${SEEDS_OVERRIDE:-2345 3456 4567 5678 6789 7890 8901 9012}"
mkdir -p results/s0_2/gate_i/logs
running=0
for s in "${SEEDS[@]}"; do
  PYTHONPATH=. OMP_NUM_THREADS=$THREADS python3 scripts/run_gate_i.py \
    --dataset "$DS" --seed "$s" --threads "$THREADS" \
    > "results/s0_2/gate_i/logs/${DS}_seed${s}.log" 2>&1 &
  running=$((running+1))
  if [ "$running" -ge "$NPAR" ]; then wait -n; running=$((running-1)); fi
done
wait
echo "all $DS seeds done"
grep -h '"record": "summary"' results/s0_2/gate_i/${DS}_seed*.jsonl
