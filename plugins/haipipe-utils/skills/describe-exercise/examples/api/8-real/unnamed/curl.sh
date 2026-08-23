#!/usr/bin/env bash
# Run from inside this folder.
curl -sS "${EXNORM_URL:-http://127.0.0.1:8088}/normalize" \
  -H "content-type: application/json" \
  --data @request.json | python3 -m json.tool
