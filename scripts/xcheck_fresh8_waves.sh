#!/usr/bin/env bash
# S0.2-1R GA-F1(a): run the pre-declared official fresh-8 screens in two waves of 4.
#
# Scheduling only — each wave runs 4 independent single-seed drivers (configs are
# mechanical one-seed copies of the committed config; the official runner's seed loop
# is per-seed independent by construction). Two waves of 4 because each jax-CPU driver
# holds ~3.6 GB RSS and ~3.3 effective cores (measured on the seed-1 benchmark).
set -u
cd "$(dirname "$0")/.."
BASE=results/s0_2/gate_i/xcheck_official_local
WAVE1=(7890 8901 9012 11111)
WAVE2=(22222 33333 44444 55555)

run_wave() {
  for s in "$@"; do
    /tmp/linoss_venv/bin/python scripts/xcheck_official_local.py \
      "$BASE/config_perseed/seed${s}" \
      > "$BASE/logs/driver_seed${s}.log" 2>&1 &
  done
  wait
}

echo "wave 1 start: $(date -Is)  seeds: ${WAVE1[*]}"
run_wave "${WAVE1[@]}"
echo "wave 1 done:  $(date -Is)"
echo "wave 2 start: $(date -Is)  seeds: ${WAVE2[*]}"
run_wave "${WAVE2[@]}"
echo "wave 2 done:  $(date -Is)"
echo "FRESH8 ALL DONE"
