#!/usr/bin/env bash
# one meal, one frame
# run from inside this folder
# body.json in this folder holds the same frames, base64-encoded
curl -s -X POST http://127.0.0.1:8070/food/normalize/image/batch \
     -H 'Content-Type: application/json' -d @body.json
