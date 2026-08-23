#!/usr/bin/env bash
# 413 - one meal is one or two frames
# run from inside this folder
curl -s -F files=@f0.jpg -F files=@f1.jpg -F files=@f2.jpg -F files=@f3.jpg -F files=@f4.jpg http://127.0.0.1:8077/normalize/image
