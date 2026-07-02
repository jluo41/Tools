#!/usr/bin/env python3
"""Make icon PNGs' background transparent by removing ONLY the border-connected
white region — so whites *inside* an icon (a robot's face, calendar cells, a
shield fill) are preserved. See lesson/15.

Usage:
    transparentize.py <src_dir> <out_dir> [--thresh 234]
Needs Pillow, numpy, scipy.
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

src_dir = Path(sys.argv[1])
out_dir = Path(sys.argv[2]); out_dir.mkdir(parents=True, exist_ok=True)
THRESH = 234
if "--thresh" in sys.argv:
    THRESH = int(sys.argv[sys.argv.index("--thresh")+1])

for p in sorted(src_dir.glob("*.png")):
    if p.name.startswith("_"):
        continue
    im = Image.open(p).convert("RGBA")
    a = np.array(im)
    whiteish = a[..., :3].astype(int).min(axis=2) > THRESH
    lbl, n = ndimage.label(whiteish)
    border = set(lbl[0, :]) | set(lbl[-1, :]) | set(lbl[:, 0]) | set(lbl[:, -1])
    border.discard(0)
    bg = np.isin(lbl, list(border))
    opaque = ndimage.binary_erosion(~bg, iterations=1, border_value=1)  # eat AA halo
    a[..., 3] = np.where(opaque, 255, 0).astype(np.uint8)
    Image.fromarray(a, "RGBA").save(out_dir / p.name)
    print(f"[ok] {p.name}: bg removed ({int(bg.sum())} px)")
print(f"-> {out_dir}")
