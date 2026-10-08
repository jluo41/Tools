#!/usr/bin/env python3
"""Overlay a labeled coordinate grid on an image so bounding boxes can be read by eye.

Usage:
    grid_overlay.py <source.png> <out.png> [--step 50] [--crop x0 y0 x1 y1] [--scale N]

Minor gridlines every --step px; bold labeled lines every 2*step. With --crop, only that region is
shown (upscaled by --scale, default 3) for tight box reading. Needs Pillow.
"""
import argparse
from PIL import Image, ImageDraw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("out")
    ap.add_argument("--step", type=int, default=50)
    ap.add_argument("--crop", type=int, nargs=4, metavar=("x0", "y0", "x1", "y1"))
    ap.add_argument("--scale", type=int, default=3)
    a = ap.parse_args()

    im = Image.open(a.source).convert("RGB")
    ox = oy = 0
    scale = 1
    if a.crop:
        x0, y0, x1, y1 = a.crop
        im = im.crop((x0, y0, x1, y1))
        ox, oy = x0, y0
        scale = a.scale
        im = im.resize((im.size[0] * scale, im.size[1] * scale))
    W, H = im.size
    d = ImageDraw.Draw(im)
    step = a.step
    major = step * 2
    # vertical lines
    gx = ox - (ox % step)
    while (gx - ox) * scale < W:
        X = (gx - ox) * scale
        if X >= 0:
            bold = gx % major == 0
            d.line([(X, 0), (X, H)], fill=(255, 0, 0) if bold else (255, 190, 190))
            if bold:
                d.text((X + 1, 1), str(gx), fill=(200, 0, 0))
        gx += step
    # horizontal lines
    gy = oy - (oy % step)
    while (gy - oy) * scale < H:
        Y = (gy - oy) * scale
        if Y >= 0:
            bold = gy % major == 0
            d.line([(0, Y), (W, Y)], fill=(0, 0, 255) if bold else (190, 190, 255))
            if bold:
                d.text((1, Y + 1), str(gy), fill=(0, 0, 200))
        gy += step
    im.save(a.out)
    print("wrote", a.out, im.size, "origin", (ox, oy), "scale", scale)


if __name__ == "__main__":
    main()
