#!/usr/bin/env bash
# a duplicate returns the identical record
# run from inside this folder
curl -s -X POST http://127.0.0.1:8077/normalize/batch \
     -H 'Content-Type: application/json' \
     -d "{\"foods\": [\"fried rice; egg\", \"milk\", \"fried rice; egg\"]}"
