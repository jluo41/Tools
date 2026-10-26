#!/usr/bin/env python3
"""Score one authored SVG against its source crop — the icon's own self-evaluation.

Usage:
    score_icon.py <icon.svg> <source_crop.png> [--size 160] [--pass 0.62]

Both images are trimmed to their content first (largest connected component, so a crop's edge-bleed
or a stray speck doesn't distort the score), size-normalized, then compared:
  shape : dilation-coverage F1 of the ink masks (robust to thin-stroke misalignment)
  color : match of the dominant ink color
  sim   : 0.75*shape + 0.25*color   (0..1)
  center: how far the SVG's content sits from its own viewBox centre (%, ~0 = self-contained)

Prints the numbers and a PASS/REVISE verdict. Exit code 0 if sim >= --pass and centered, else 1 —
so a subagent can loop on it. Needs cairosvg, Pillow, numpy (scipy optional, improves de-noising).
"""
import argparse, io, sys
import numpy as np
import cairosvg
from PIL import Image, ImageFilter

try:
    from scipy import ndimage
    _HAS_SCIPY = True
except Exception:
    _HAS_SCIPY = False


def ink_mask(im):
    a = np.asarray(im.convert("RGBA"))
    rgb = a[:, :, :3].astype(np.int16)
    nonwhite = (255 - rgb).max(axis=2) > 24
    alpha = a[:, :, 3]
    return (alpha > 12) & nonwhite if alpha.min() < 255 else nonwhite


def denoise(mask, keep=0.15):
    if not _HAS_SCIPY:
        return mask
    lab, n = ndimage.label(mask)
    if n <= 1:
        return mask
    sizes = ndimage.sum(mask, lab, range(1, n + 1))
    return np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= keep * sizes.max()])


def trim(im):
    m = denoise(ink_mask(im))
    ys, xs = np.where(m)
    if len(xs) == 0:
        return im
    return im.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))


def fit_center(im, S):
    inner = int(S * 0.86)
    w, h = im.size
    s = min(inner / w, inner / h)
    im2 = im.resize((max(1, int(w * s)), max(1, int(h * s))), Image.LANCZOS)
    c = Image.new("RGBA", (S, S), (255, 255, 255, 255))
    c.alpha_composite(im2.convert("RGBA"), ((S - im2.size[0]) // 2, (S - im2.size[1]) // 2))
    return c.convert("RGB")


def dilate(mask, r):
    im = Image.fromarray((mask * 255).astype("uint8")).filter(ImageFilter.MaxFilter(2 * r + 1))
    return np.asarray(im) > 127


def center_offset(svg_path):
    png = cairosvg.svg2png(url=svg_path, output_height=300, background_color=None)
    a = np.asarray(Image.open(io.BytesIO(png)).convert("RGBA"))[:, :, 3]
    ys, xs = np.where(a > 12)
    if len(xs) == 0:
        return 0.0
    PH, PW = a.shape
    return max(abs((xs.min() + xs.max() + 1) / 2 - PW / 2) / PW,
              abs((ys.min() + ys.max() + 1) / 2 - PH / 2) / PH) * 100


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svg")
    ap.add_argument("crop")
    ap.add_argument("--size", type=int, default=160)
    ap.add_argument("--pass", dest="thr", type=float, default=0.62)
    ap.add_argument("--center-max", type=float, default=6.0)
    a = ap.parse_args()
    S = a.size
    svg_png = cairosvg.svg2png(url=a.svg, output_height=260, background_color=None)
    sc = fit_center(trim(Image.open(io.BytesIO(svg_png)).convert("RGBA")), S)
    cc = fit_center(trim(Image.open(a.crop).convert("RGBA")), S)
    ms, mc = ink_mask(sc), ink_mask(cc)
    na, nb = ms.sum() or 1, mc.sum() or 1
    covs = []
    for f in (0.015, 0.03, 0.05):
        r = max(1, int(S * f))
        pa = (ms & dilate(mc, r)).sum() / na
        pb = (mc & dilate(ms, r)).sum() / nb
        covs.append(2 * pa * pb / ((pa + pb) or 1))
    shape = float(np.mean(covs))
    ca = np.asarray(sc).astype(float)[ms].mean(0) if ms.any() else np.array([255.] * 3)
    cb = np.asarray(cc).astype(float)[mc].mean(0) if mc.any() else np.array([255.] * 3)
    color = 1 - float(np.abs(ca - cb).mean()) / 255
    sim = 0.75 * shape + 0.25 * color
    off = center_offset(a.svg)
    ok = sim >= a.thr and off <= a.center_max
    print(f"sim={sim:.2f}  shape={shape:.2f}  color={color:.2f}  center_off={off:.1f}%  "
          f"=> {'PASS' if ok else 'REVISE'}")
    if not ok:
        if sim < a.thr:
            print(f"  low similarity (< {a.thr}): re-check shape/colors against the crop")
        if off > a.center_max:
            print(f"  off-center (> {a.center_max}%): run center_svg.py --inplace or re-center shapes")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
