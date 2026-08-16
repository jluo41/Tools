#!/usr/bin/env bash
# run_scan — pairs with results/run_scan/
cd "$(dirname "$0")/.." || exit 1
bash 01_probe_landing_path_scan.sh \
  /Users/floydluo/Desktop/Tools-SPACE/plugins/haipipe-toolkit \
  results/run_scan
