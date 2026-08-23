#!/usr/bin/env bash
# a sealed opaque bottle: nothing edible is visible
# run from inside this folder
curl -s -F files=@00000002-PHOTO-2020-4-30-8-53-0.jpg \
     http://127.0.0.1:8077/normalize/image
