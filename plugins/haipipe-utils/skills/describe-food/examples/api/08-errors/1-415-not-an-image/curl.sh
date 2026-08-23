#!/usr/bin/env bash
# 415 - only image types are accepted
# run from inside this folder
curl -s -F files=@notes.txt http://127.0.0.1:8077/normalize/image
