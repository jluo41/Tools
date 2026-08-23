#!/usr/bin/env bash
# basis=per_meal
# run from inside this folder
curl -s -X POST http://127.0.0.1:8077/normalize \
     -H 'Content-Type: application/json' \
     -d "{\"food\": \"Coarse grain steamed bread 50 g\\nEgg 39 g\\nSteamed pork dumplings 64 g\"}"
