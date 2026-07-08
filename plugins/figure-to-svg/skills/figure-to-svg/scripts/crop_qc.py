#!/usr/bin/env python3
"""Quality-check (and optionally auto-fix) the icon crops before vectorizing.

Usage:
    crop_qc.py <source.png> <items.json> <crop_dir> [--apply] [--grow 10] [--pad 3]

Imperfect crops are the #1 upstream cause of a bad replica: a box can clip its icon, swallow a
neighbour's stroke, or leave the icon off to one side in a sea of padding. For each icon item this
analyses a slightly-expanded window around its bbox and reports:
  fill%   : how much of the bbox the icon actually fills (low => loose/padded)
  clip    : icon ink runs off an edge of the bbox (content continues outside)
  bleed   : disconnected specks near the border (a neighbour panel line / stray mark)
  center  : icon is off to one side of its bbox

With --apply it rewrites each item's `bbox` to the icon's TRUE content box — dropping specks that
don't belong to the icon (kept = components that touch the original bbox), reclaiming clipped parts
that sat just outside, and removing dead padding — then re-crops. items.json is backed up to
items.json.bak. Needs Pillow, numpy (scipy strongly recommended for the component filtering).
"""
import argparse, json, os, shutil
import numpy as np
from PIL import Image

try:
    from scipy import ndimage
    _HAS_SCIPY = True
except Exception:
    _HAS_SCIPY = False


def content_mask(win):
    """Ink = pixels that differ from the crop's BACKGROUND, where background is estimated from the
    border ring. Works for both white-background icons and light icons on a dark panel (e.g. the
    footer shield), unlike a plain non-white test."""
    a = np.asarray(win.convert("RGB")).astype(np.int16)
    H, W = a.shape[:2]
    border = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]], axis=0)
    bg = np.median(border, axis=0)
    return np.abs(a - bg).max(axis=2) > 34


def analyse(src, item, grow, minfrac=0.004):
    W, H = src.size
    x, y, w, h = item["bbox"]
    X0, Y0 = max(0, x - grow), max(0, y - grow)
    X1, Y1 = min(W, x + w + grow), min(H, y + h + grow)
    win = src.crop((X0, Y0, X1, Y1))
    mask = content_mask(win)
    ox0, oy0, ox1, oy1 = x - X0, y - Y0, x - X0 + w, y - Y0 + h
    orig = np.zeros_like(mask)
    orig[max(0, oy0):oy1, max(0, ox0):ox1] = True

    dropped = 0
    if _HAS_SCIPY and mask.any():
        lab, n = ndimage.label(mask)
        minarea = minfrac * mask.size
        keep = []
        for k in range(1, n + 1):
            comp = lab == k
            if comp.sum() < minarea:
                continue
            (comp & orig).any() and keep.append(k)
            if not (comp & orig).any():
                dropped += 1
        kept = np.isin(lab, keep) if keep else (mask & orig)
    else:
        kept = mask & orig

    ys, xs = np.where(kept)
    if len(xs) == 0:
        return None
    cx0, cy0, cx1, cy1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    # new bbox in source coords, padded and clamped
    nx0, ny0 = max(0, X0 + cx0), max(0, Y0 + cy0)
    nx1, ny1 = min(W, X0 + cx1), min(H, Y0 + cy1)
    fill = kept.sum() / max(1, w * h)
    # clip: a whole edge of the bbox is substantially inked AND real content continues outside it.
    # (mere presence of ink near an edge is normal — an icon can fill its box — so require both.)
    m = (mask & orig)[max(0, oy0):oy1, max(0, ox0):ox1]
    if m.size == 0:
        m = np.zeros((1, 1), bool)
    edge = max(m[0, :].mean(), m[-1, :].mean(), m[:, 0].mean(), m[:, -1].mean())
    grew = max(x - nx0, y - ny0, nx1 - (x + w), ny1 - (y + h))
    clip = edge > 0.30 and grew > 4
    ccx, ccy = (cx0 + cx1) / 2, (cy0 + cy1) / 2
    center_off = max(abs(ccx - (ox0 + ox1) / 2) / max(1, w), abs(ccy - (oy0 + oy1) / 2) / max(1, h)) * 100
    return dict(fill=fill, clip=bool(clip), bleed=dropped, center_off=center_off,
                new_bbox=[int(nx0), int(ny0), int(nx1 - nx0), int(ny1 - ny0)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("items")
    ap.add_argument("crop_dir")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--grow", type=int, default=10)
    ap.add_argument("--pad", type=int, default=3)
    a = ap.parse_args()
    if not _HAS_SCIPY:
        print("WARN: scipy not found — speck/bleed filtering disabled (fill/clip still work)")

    src = Image.open(a.source).convert("RGB")
    data = json.load(open(a.items, encoding="utf-8"))
    icons = [it for it in data.get("items", []) if it.get("type") == "icon"]
    flagged, changes = [], 0
    print(f"{'id':44s} {'fill%':>6} {'ctr%':>6}  flags")
    for it in icons:
        r = analyse(src, it, a.grow)
        if r is None:
            print(f"{it['id']:44s} {'--':>6} {'--':>6}  EMPTY (no ink in bbox)")
            flagged.append(it["id"])
            continue
        fl = []
        if r["fill"] < 0.28:
            fl.append("LOOSE")
        if r["clip"]:
            fl.append("CLIP")
        if r["bleed"]:
            fl.append(f"BLEED×{r['bleed']}")
        if r["center_off"] > 12:
            fl.append("OFF-CTR")
        if fl:
            flagged.append(it["id"])
        print(f"{it['id']:44s} {r['fill']*100:6.0f} {r['center_off']:6.0f}  {','.join(fl) or 'ok'}")
        if a.apply:
            nb = [max(0, r["new_bbox"][0] - a.pad), max(0, r["new_bbox"][1] - a.pad),
                  r["new_bbox"][2] + 2 * a.pad, r["new_bbox"][3] + 2 * a.pad]
            if nb != it["bbox"]:
                it["bbox"] = nb
                changes += 1

    if a.apply:
        shutil.copy(a.items, a.items + ".bak")
        json.dump(data, open(a.items, "w", encoding="utf-8"), indent=2)
        os.makedirs(a.crop_dir, exist_ok=True)
        for it in icons:
            x, y, w, h = it["bbox"]
            src.crop((x, y, x + w, y + h)).save(os.path.join(a.crop_dir, it["id"] + ".png"))
        print(f"\n--apply: rewrote {changes} bboxes (backup items.json.bak) and re-cropped {len(icons)} icons")
    else:
        print(f"\n{len(flagged)} flagged / {len(icons)} icons. Re-run with --apply to auto-tighten & re-crop,"
              f" or hand-edit bboxes in items.json.")


if __name__ == "__main__":
    main()
