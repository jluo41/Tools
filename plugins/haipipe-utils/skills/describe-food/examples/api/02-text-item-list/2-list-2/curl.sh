#!/usr/bin/env bash
# MEASURED / per_serving
# run from inside this folder
curl -s -X POST http://127.0.0.1:8077/normalize \
     -H 'Content-Type: application/json' \
     -d "{\"food\": \"Cheese Pizza; Greek Salad; Banana Berry Muffin\"}"
