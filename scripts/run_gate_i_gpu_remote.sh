#!/bin/bash
# Runs ON the vast.ai box: GPU parity gate FIRST (hard stop on fail), then the
# 5 gated EigenWorms seeds sequentially on cuda (frozen PR-1 protocol; the
# only deltas vs local are environment: fp32 CUDA arithmetic, gated by parity).
set -e
cd "$(dirname "$0")/.."
export CUBLAS_WORKSPACE_CONFIG=:4096:8
export PYTHONPATH=.

echo "=== [1/2] GPU parity gate (blocks the gated runs on FAIL) ==="
python3 scripts/parity_gpu_side.py 2>&1 | tee results/s0_2/gate_i/logs/parity_gpu.log

echo ""
echo "=== [2/2] Gated-5 EigenWorms, sequential, device=cuda ==="
for s in 2345 3456 4567 5678 6789; do
  echo "--- seed $s start: $(date -u +%H:%M:%S) ---"
  python3 scripts/run_gate_i.py --dataset EigenWorms --seed "$s" --device cuda \
    > "results/s0_2/gate_i/logs/EigenWorms_seed${s}_gpu.log" 2>&1
  tail -1 "results/s0_2/gate_i/logs/EigenWorms_seed${s}_gpu.log"
done

echo "all 5 gated seeds done"
grep -h '"record": "summary"' results/s0_2/gate_i/EigenWorms_seed*.jsonl
