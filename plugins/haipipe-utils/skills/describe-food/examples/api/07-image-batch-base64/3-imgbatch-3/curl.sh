#!/usr/bin/env bash
# two meals in one call: a hit and an honest MISS
# run from inside this folder
# body.json in this folder holds the same frames, base64-encoded
curl -s -X POST http://127.0.0.1:8077/normalize/image/batch \
     -H 'Content-Type: application/json' -d @body.json
