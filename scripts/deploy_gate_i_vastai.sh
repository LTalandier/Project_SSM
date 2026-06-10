#!/bin/bash
# S0.2-1 G3 on vast.ai (D-2026-06-10-2 cloud option, Lucas-approved in-session,
# budget ceiling = remaining vast.ai credits ~$7.44; E-2026-06-10-5).
# Pattern after PNN_topology_search/deploy_stage3_vastai.sh.
#
# Usage: SSH_HOST=sshN.vast.ai SSH_PORT=NNNNN bash scripts/deploy_gate_i_vastai.sh
set -e
cd "$(dirname "$0")/.."

SSH_HOST="${SSH_HOST:?Set SSH_HOST=ssh<N>.vast.ai}"
SSH_PORT="${SSH_PORT:?Set SSH_PORT=<port>}"
SSH_OPTS="-p $SSH_PORT -o StrictHostKeyChecking=accept-new"

echo "=== Gate-i G3 vast.ai upload -> $SSH_HOST:$SSH_PORT ==="
ssh $SSH_OPTS root@$SSH_HOST 'mkdir -p /workspace/Project_SSM/data/processed/UEA/EigenWorms /workspace/Project_SSM/results/s0_2/gate_i/logs'

echo "  Uploading code (git-tracked tree only)..."
git ls-files -z | rsync -az -e "ssh $SSH_OPTS" --files-from=- --from0 \
    ./ "root@$SSH_HOST:/workspace/Project_SSM/"

echo "  Uploading EigenWorms data (~102 MB: data.npy, labels.npy, splits)..."
rsync -az -e "ssh $SSH_OPTS" \
    data/processed/UEA/EigenWorms/data.npy \
    data/processed/UEA/EigenWorms/labels.npy \
    data/processed/UEA/EigenWorms/splits_official.json \
    "root@$SSH_HOST:/workspace/Project_SSM/data/processed/UEA/EigenWorms/"

echo "  Environment check..."
ssh $SSH_OPTS root@$SSH_HOST 'bash -s' <<'REMOTE'
set -e
cd /workspace/Project_SSM
python3 -c "import torch; print('torch', torch.__version__, '| cuda ok:', torch.cuda.is_available())"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
REMOTE

echo ""
echo "=== Upload complete. Next: ==="
echo "  ssh $SSH_OPTS root@$SSH_HOST 'cd /workspace/Project_SSM && nohup bash scripts/run_gate_i_gpu_remote.sh > results/s0_2/gate_i/logs/gpu_remote_driver.log 2>&1 &'"
