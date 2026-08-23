#!/usr/bin/env bash
# 3 distinct foods, order preserved
# run from inside this folder
curl -s -X POST http://127.0.0.1:8077/normalize/batch \
     -H 'Content-Type: application/json' \
     -d "{\"foods\": [\"white rice\", \"butter\", \"lettuce\"]}"
