#!/usr/bin/env bash
# Run from inside this folder.
curl -sS "${MEDNORM_URL:-http://127.0.0.1:8079}/normalize/batch" \
  -H "content-type: application/json" \
  --data @request.json | python3 -m json.tool
