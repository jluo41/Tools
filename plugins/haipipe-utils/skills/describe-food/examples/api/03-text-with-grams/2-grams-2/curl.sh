#!/usr/bin/env bash
# basis=per_meal
# run from inside this folder
curl -s -X POST http://127.0.0.1:8077/normalize \
     -H 'Content-Type: application/json' \
     -d "{\"food\": \"Egg 50 g\\nRice 25 g\\nVegetable 100 g\"}"
