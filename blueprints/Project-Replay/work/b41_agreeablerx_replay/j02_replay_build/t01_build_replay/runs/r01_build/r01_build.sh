#!/bin/sh
# Rebuild everything generated from the decision logs; the build's own print lines are the receipt.
cd "$(dirname "$0")/../../../../src" && python3 build.py
