#!/usr/bin/env python3
"""Evaluate hand-authored icon SVGs against their source crops.

Usage:
    evaluate_icons.py <svg_dir> <crop_dir> <out_sheet.png> [--size 160] [--flag 0.70]

For every id present in BOTH folders it measures, framing-independently (both are trimmed to their
own content first, so uneven padding / off-centering does NOT distort the score):
  - shape IoU   : overlap of the ink masks after size-normalizing
  - color score : 1 - mean color distance over the union
  - similarity  : 0.6*IoU + 0.4*color  (0..1, higher = closer to the crop)
  - center off  : how far the SVG's drawn content sits from its own viewBox center (% of size);
                  ~0 means the SVG is properly centered / self-contained.

Writes a contact sheet (crop | svg, worst-first) annotated with scores and flags, prints a summary,
and writes <out_sheet>.json with the raw numbers. Needs: cairosvg, Pillow, numpy.
"""
import argparse, io, json, os, glob
import numpy as np
import cairosvg
from PIL import Image, ImageDraw, ImageFilter


try:
    from scipy import ndimage
    _HAS_SCIPY = True
except Exception:
    _HAS_SCIPY = False


def ink_mask_rgba(im):
    """Content mask: alpha>12 OR visibly non-white. Returns (mask, rgb)."""
    a = np.asarray(im.convert("RGBA"))
    rgb = a[:, :, :3].astype(np.int16)
    alpha = a[:, :, 3]
    nonwhite = (255 - rgb).max(axis=2) > 24
    mask = (alpha > 12) & nonwhite if alpha.min() < 255 else nonwhite
    return mask, a[:, :, :3]


def denoise(mask, keep_frac=0.15):
    """Drop small disconnected specks (crop edge-bleed / stray marks): keep the largest connected
    component and any component at least keep_frac of its area. No-op without scipy."""
    if not _HAS_SCIPY:
        return mask
    lab, n = ndimage.label(mask)
    if n <= 1:
        return mask
    sizes = ndimage.sum(mask, lab, range(1, n + 1))
    keep = [i + 1 for i, s in enumerate(sizes) if s >= keep_frac * sizes.max()]
    return np.isin(lab, keep)


def trim(im):
    mask = denoise(ink_mask_rgba(im)[0])
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return im, (0, 0, im.size[0], im.size[1])
    box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    return im.crop(box), box


def fit_center(im, S, inner):
    """Resize im to fit an inner x inner square, paste centered on white SxS."""
    w, h = im.size
    s = min(inner / w, inner / h)
    im2 = im.resize((max(1, int(w * s)), max(1, int(h * s))), Image.LANCZOS)
    canvas = Image.new("RGBA", (S, S), (255, 255, 255, 255))
    canvas.alpha_composite(im2.convert("RGBA"), ((S - im2.size[0]) // 2, (S - im2.size[1]) // 2))
    return canvas.convert("RGB")


def svg_center_offset(svg_path):
    """Content-center vs viewBox-center, as % of the rendered canvas (0 = perfectly centered)."""
    png = cairosvg.svg2png(url=svg_path, output_height=300, background_color=None)
    im = np.asarray(Image.open(io.BytesIO(png)).convert("RGBA"))
    a = im[:, :, 3]
    ys, xs = np.where(a > 12)
    if len(xs) == 0:
        return 0.0, 0.0
    PH, PW = a.shape
    cx = (xs.min() + xs.max() + 1) / 2
    cy = (ys.min() + ys.max() + 1) / 2
    return abs(cx - PW / 2) / PW * 100, abs(cy - PH / 2) / PH * 100


def dilate(mask, r):
    im = Image.fromarray((mask * 255).astype("uint8")).filter(ImageFilter.MaxFilter(2 * r + 1))
    return np.asarray(im) > 127


def score_pair(svg_path, crop_path, S):
    """Framing-independent similarity. Shape via dilation-coverage (robust to thin-stroke
    misalignment — what fraction of each drawing's ink lies within a small radius of the other's),
    plus a match of the dominant ink color. Far more discriminative for line-art than raw IoU."""
    inner = int(S * 0.86)
    svg_png = cairosvg.svg2png(url=svg_path, output_height=260, background_color=None)
    svg_c = fit_center(trim(Image.open(io.BytesIO(svg_png)).convert("RGBA"))[0], S, inner)
    crop_c = fit_center(trim(Image.open(crop_path).convert("RGBA"))[0], S, inner)
    ms, _ = ink_mask_rgba(svg_c)
    mc, _ = ink_mask_rgba(crop_c)
    na, nb = ms.sum() or 1, mc.sum() or 1

    covs = []
    for f in (0.015, 0.03, 0.05):
        r = max(1, int(S * f))
        pa = (ms & dilate(mc, r)).sum() / na      # svg ink covered by crop
        pb = (mc & dilate(ms, r)).sum() / nb      # crop ink covered by svg
        covs.append(2 * pa * pb / ((pa + pb) or 1))  # F1 of the two coverages
    shape = float(np.mean(covs))

    iou = float(np.logical_and(ms, mc).sum() / (np.logical_or(ms, mc).sum() or 1))
    a = np.asarray(svg_c).astype(float)
    b = np.asarray(crop_c).astype(float)
    ca = a[ms].mean(axis=0) if ms.any() else np.array([255., 255., 255.])
    cb = b[mc].mean(axis=0) if mc.any() else np.array([255., 255., 255.])
    color = 1 - float(np.abs(ca - cb).mean()) / 255
    sim = 0.75 * shape + 0.25 * color
    ox, oy = svg_center_offset(svg_path)
    return dict(iou=iou, shape=shape, color=float(color), sim=float(sim),
                center_off=float(max(ox, oy)), thumb_crop=crop_c, thumb_svg=svg_c)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svg_dir")
    ap.add_argument("crop_dir")
    ap.add_argument("out")
    ap.add_argument("--size", type=int, default=160)
    ap.add_argument("--flag", type=float, default=0.55, help="similarity below this is flagged")
    ap.add_argument("--center-flag", type=float, default=6.0, help="center-offset %% above this is flagged")
    a = ap.parse_args()

    ids = sorted(os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(a.svg_dir, "*.svg")))
    rows = []
    for i in ids:
        crop = os.path.join(a.crop_dir, i + ".png")
        if not os.path.exists(crop):
            continue
        r = score_pair(os.path.join(a.svg_dir, i + ".svg"), crop, a.size)
        r["id"] = i
        rows.append(r)

    rows.sort(key=lambda r: r["sim"])  # worst first
    S, pad, lab, colw = a.size, 12, 20, a.size * 2 + 24
    sheet = Image.new("RGB", (colw + pad, len(rows) * (S + lab) + pad), (245, 245, 245))
    d = ImageDraw.Draw(sheet)
    for k, r in enumerate(rows):
        y = pad + k * (S + lab)
        flags = []
        if r["sim"] < a.flag:
            flags.append("LOW-SIM")
        if r["center_off"] > a.center_flag:
            flags.append("OFF-CENTER")
        tag = f'{r["id"]}  sim={r["sim"]:.2f} shape={r["shape"]:.2f} col={r["color"]:.2f} ctr={r["center_off"]:.1f}%'
        if flags:
            tag += "  [" + ",".join(flags) + "]"
        d.text((pad, y + 3), tag, fill=(180, 0, 0) if flags else (30, 30, 30))
        sheet.paste(r["thumb_crop"], (pad, y + lab))
        sheet.paste(r["thumb_svg"], (pad + S + 12, y + lab))
    sheet.save(a.out)

    summary = [{k: r[k] for k in ("id", "sim", "shape", "color", "iou", "center_off")} for r in rows]
    json.dump(summary, open(a.out + ".json", "w"), indent=2)
    flagged = [r for r in rows if r["sim"] < a.flag or r["center_off"] > a.center_flag]
    mean = sum(r["sim"] for r in rows) / (len(rows) or 1)
    print(f"evaluated {len(rows)} icons  mean-sim={mean:.3f}  wrote {a.out}")
    print(f"left column = source crop, right column = your svg (both trimmed & centered)")
    if flagged:
        print(f"FLAGGED {len(flagged)}:")
        for r in flagged:
            why = []
            if r["sim"] < a.flag:
                why.append(f'sim {r["sim"]:.2f}')
            if r["center_off"] > a.center_flag:
                why.append(f'off-center {r["center_off"]:.1f}%')
            print(f'  {r["id"]:42s} {", ".join(why)}')
    else:
        print("no icons flagged")


if __name__ == "__main__":
    main()
