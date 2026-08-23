#!/usr/bin/env bash
# the before/after pair CGMacros logs for one meal
# run from inside this folder
curl -s -F files=@00000007-PHOTO-2020-5-1-20-48-0.jpg -F files=@00000008-PHOTO-2020-5-1-20-57-0.jpg \
     http://127.0.0.1:8077/normalize/image
