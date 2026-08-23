#!/usr/bin/env bash
# a hit, a declaration and an item the bank does not have
# run from inside this folder
curl -s -X POST http://127.0.0.1:8077/normalize/batch \
     -H 'Content-Type: application/json' \
     -d "{\"foods\": [\"Cucumber 100g\", \"Just Carbs\", \"xiaolongbao\"]}"
