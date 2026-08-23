#!/usr/bin/env bash
# 422 - foods must be a list, not a string
# run from inside this folder
curl -s -X POST http://127.0.0.1:8077/normalize/batch \
     -H 'Content-Type: application/json' \
     -d "{\"foods\": \"rice\"}"
