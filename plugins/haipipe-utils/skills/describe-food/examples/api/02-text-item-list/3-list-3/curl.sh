#!/usr/bin/env bash
# ESTIMATED / per_meal
# run from inside this folder
curl -s -X POST http://127.0.0.1:8077/normalize \
     -H 'Content-Type: application/json' \
     -d "{\"food\": \"Nacho Cheese Tortilla Chips (28g); Diet Coke\"}"
