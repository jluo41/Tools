#!/usr/bin/env bash
# one item -> ESTIMATED
# run from inside this folder
curl -s -X POST http://127.0.0.1:8070/food/normalize \
     -H 'Content-Type: application/json' \
     -d "{\"food\": \"chinese cabbage\"}"
