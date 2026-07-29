#!/usr/bin/env python3
"""Crop every icon item in items.json out of the source image.

Usage:
    crop_bboxes.py <source.png> <items.json> <out_dir> [--pad 4]

Writes <out_dir>/<id>.png for each item with type == "icon". bbox is [x, y, w, h] in source pixels.
A small --pad adds breathing room. Needs Pillow.
"""
import argparse, json, os
from PIL import Image


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("items")
    ap.add_argument("out_dir")
    ap.add_argument("--pad", type=int, default=4)
    a = ap.parse_args()

    im = Image.open(a.source).convert("RGBA")
    W, H = im.size
    os.makedirs(a.out_dir, exist_ok=True)
    data = json.load(open(a.items))
    n = 0
    for it in data.get("items", []):
        if it.get("type") != "icon":
            continue
        x, y, w, h = it["bbox"]
        box = (max(0, x - a.pad), max(0, y - a.pad),
               min(W, x + w + a.pad), min(H, y + h + a.pad))
        im.crop(box).save(os.path.join(a.out_dir, it["id"] + ".png"))
        n += 1
    print(f"cropped {n} icons -> {a.out_dir}")


if __name__ == "__main__":
    main()
