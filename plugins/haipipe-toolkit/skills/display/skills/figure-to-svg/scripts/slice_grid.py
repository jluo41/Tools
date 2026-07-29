#!/usr/bin/env python3
"""Slice a regular NxM icon grid (from gen_icon_grid.py) into individual
content-tight, centered icon PNGs.

Robust against neighbour-bleed: within each equal-division cell, keep only the
connected component(s) that reach the cell's CENTRAL region, and drop detached
blobs that sit only in the outer margin (an oversized neighbour icon crossing the
cut line). Then tight-trim + center. See lesson/14.

Usage:
    slice_grid.py <grid.png> <rows> <cols> <out_dir> '<names_json>'
where names_json is a row-major list of ids (len == rows*cols; "" => skip cell).
Needs Pillow, numpy, scipy.
"""
import sys, json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

grid_png = Path(sys.argv[1])
rows, cols = int(sys.argv[2]), int(sys.argv[3])
out_dir = Path(sys.argv[4]); out_dir.mkdir(parents=True, exist_ok=True)
names = json.loads(sys.argv[5])
pad_frac = 0.10
CENTRAL = 0.62          # a kept blob must intersect this central box (frac of cell)
MIN_AREA = 0.0008       # ignore specks smaller than this frac of cell area

im = Image.open(grid_png).convert("RGBA")
W, H = im.size
cw, ch = W / cols, H / rows

def keep_central_content(cell):
    rgb = np.asarray(cell.convert("RGB")).astype(int)
    h, w = rgb.shape[:2]
    ink = rgb.min(axis=2) < 245
    if not ink.any():
        return None
    lbl, n = ndimage.label(ink)
    mx0, my0 = int(w*(1-CENTRAL)/2), int(h*(1-CENTRAL)/2)
    mx1, my1 = w - mx0, h - my0
    central = np.zeros_like(ink); central[my0:my1, mx0:mx1] = True
    minarea = MIN_AREA * w * h
    keep = np.zeros_like(ink)
    for k in range(1, n+1):
        comp = lbl == k
        if comp.sum() < minarea:
            continue
        if (comp & central).any():
            keep |= comp
    if not keep.any():
        return None
    ys, xs = np.where(keep)
    return (xs.min(), ys.min(), xs.max()+1, ys.max()+1)

saved = 0; total = sum(1 for n in names if n)
for i, name in enumerate(names):
    if not name:
        continue
    r, c = divmod(i, cols)
    cell = im.crop((round(c*cw), round(r*ch), round((c+1)*cw), round((r+1)*ch)))
    bb = keep_central_content(cell)
    if bb is None:
        print(f"[skip] {name}: empty"); continue
    icon = cell.crop(bb); iw, ih = icon.size
    side = int(max(iw, ih) * (1 + 2*pad_frac))
    canvas = Image.new("RGBA", (side, side), (255, 255, 255, 255))
    canvas.paste(icon, ((side-iw)//2, (side-ih)//2))
    canvas.save(out_dir / f"{name}.png")
    saved += 1
    print(f"[ok] {name}: {iw}x{ih} -> {side}x{side}")
print(f"\nsliced {saved}/{total} -> {out_dir}")
