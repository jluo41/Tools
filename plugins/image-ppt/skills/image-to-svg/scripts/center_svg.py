#!/usr/bin/env python3
"""Normalize an icon SVG so its content is centered and self-contained.

Usage:
    center_svg.py <file.svg | dir> [--pad 0.06] [--inplace] [--out DIR]

Renders each SVG (transparent), finds the tight bounding box of the actually-drawn content, and
rewrites the `viewBox` (and width/height) to frame that content with EQUAL padding on all sides.
The shapes are untouched — only the viewBox changes — so the icon becomes centered within its own
canvas regardless of where the primitives were drawn. This removes any off-center framing an author
copied from an imperfect crop, making the SVG a clean, reusable, centered asset.

  --pad P     padding as a fraction of the content's larger side (default 0.06)
  --inplace   overwrite the input file(s)
  --out DIR   write normalized copies here instead (default: alongside, suffix _centered)

Needs: cairosvg, Pillow, numpy.
"""
import argparse, glob, io, os, re
import numpy as np
import cairosvg
from PIL import Image

VB_RE = re.compile(r'viewBox\s*=\s*"([-\d.eE]+)\s+([-\d.eE]+)\s+([-\d.eE]+)\s+([-\d.eE]+)"')
# NOTE: attribute regexes require a WHITESPACE before the name and are only ever applied to the
# opening <svg ...> tag — never the whole document. This is deliberate: a bare \bwidth also matches
# inside stroke-width="..." (the '-w' is a word boundary), which would clobber shape strokes.
ATTR_W = re.compile(r'(\s)width\s*=\s*"[^"]*"')
ATTR_H = re.compile(r'(\s)height\s*=\s*"[^"]*"')


def content_bbox_px(svg_path, render_h=400):
    """Render transparent and return (x0,y0,x1,y1,PW,PH) of non-transparent content, or None."""
    png = cairosvg.svg2png(url=svg_path, output_height=render_h, background_color=None)
    im = np.asarray(Image.open(io.BytesIO(png)).convert("RGBA"))
    alpha = im[:, :, 3]
    ys, xs = np.where(alpha > 12)
    if len(xs) == 0:
        return None
    PH, PW = alpha.shape
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1, PW, PH


def normalize(svg_path, pad=0.06):
    text = open(svg_path, encoding="utf-8").read()
    m = VB_RE.search(text)
    if not m:
        return None, "no viewBox"
    vx, vy, vw, vh = (float(g) for g in m.groups())
    bb = content_bbox_px(svg_path)
    if bb is None:
        return None, "empty render"
    x0, y0, x1, y1, PW, PH = bb
    # pixel -> user units
    ux0 = vx + (x0 / PW) * vw
    ux1 = vx + (x1 / PW) * vw
    uy0 = vy + (y0 / PH) * vh
    uy1 = vy + (y1 / PH) * vh
    cw, ch = ux1 - ux0, uy1 - uy0
    p = pad * max(cw, ch)
    nvx, nvy, nvw, nvh = ux0 - p, uy0 - p, cw + 2 * p, ch + 2 * p
    new_vb = f'viewBox="{nvx:.2f} {nvy:.2f} {nvw:.2f} {nvh:.2f}"'
    out = VB_RE.sub(new_vb, text, count=1)
    # keep width/height proportional to the new viewBox (so standalone display looks right),
    # editing ONLY the opening <svg ...> tag so shape attributes (stroke-width, rect width) are safe
    s = out.find("<svg")
    te = out.find(">", s)
    head, rest = out[s:te], out[te:]
    if ATTR_W.search(head):
        head = ATTR_W.sub(lambda mo: f'{mo.group(1)}width="{nvw:.2f}"', head, count=1)
    else:
        head = head[:4] + f' width="{nvw:.2f}"' + head[4:]
    if ATTR_H.search(head):
        head = ATTR_H.sub(lambda mo: f'{mo.group(1)}height="{nvh:.2f}"', head, count=1)
    else:
        head = head[:4] + f' height="{nvh:.2f}"' + head[4:]
    out = out[:s] + head + rest
    # centering report: how far the content center sits from the viewBox center, as % of size
    off_x = abs((ux0 + cw / 2) - (nvx + nvw / 2)) / nvw * 100
    off_y = abs((uy0 + ch / 2) - (nvy + nvh / 2)) / nvh * 100
    return out, f"vb {vw:.0f}x{vh:.0f}->{nvw:.0f}x{nvh:.0f}, off {off_x:.1f}/{off_y:.1f}%"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--pad", type=float, default=0.06)
    ap.add_argument("--inplace", action="store_true")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    files = ([a.target] if a.target.endswith(".svg")
             else sorted(glob.glob(os.path.join(a.target, "*.svg"))))
    if a.out:
        os.makedirs(a.out, exist_ok=True)
    n = 0
    for f in files:
        new, info = normalize(f, a.pad)
        if new is None:
            print(f"skip {os.path.basename(f)}: {info}")
            continue
        if a.out:
            dst = os.path.join(a.out, os.path.basename(f))
        elif a.inplace:
            dst = f
        else:
            dst = f[:-4] + "_centered.svg"
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(new)
        n += 1
        print(f"centered {os.path.basename(f)}  [{info}]")
    print(f"-- normalized {n}/{len(files)} svgs")


if __name__ == "__main__":
    main()
