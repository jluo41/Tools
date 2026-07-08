#!/usr/bin/env python3
"""Render an SVG and place it side-by-side with its source crop for visual verification.

Usage:
    render_compare.py <icon.svg> <source_crop.png> [out.png] [--scale N]

Writes a side-by-side PNG (source | rendered) at matched height so you can eyeball fidelity.
Needs: cairosvg, Pillow. Run with a venv that has them (see SKILL.md setup).
"""
import sys, io, argparse
import cairosvg
from PIL import Image, ImageDraw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svg")
    ap.add_argument("source")
    ap.add_argument("out", nargs="?", default="/tmp/img2svg_cmp.png")
    ap.add_argument("--scale", type=int, default=4, help="upscale factor for visibility")
    a = ap.parse_args()

    src = Image.open(a.source).convert("RGBA")
    # target render height so both panels line up
    H = max(src.size[1] * a.scale, 240)
    src_big = src.resize((src.size[0] * a.scale, src.size[1] * a.scale), Image.NEAREST)

    png = cairosvg.svg2png(url=a.svg, output_height=H, background_color="white")
    ren = Image.open(io.BytesIO(png)).convert("RGBA")

    # composite source onto white too (crops may be transparent)
    def onwhite(im):
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        return bg.convert("RGB")

    s = onwhite(src_big)
    r = onwhite(ren)
    pad, lab = 12, 22
    W = s.size[0] + r.size[0] + pad * 3
    Ht = max(s.size[1], r.size[1]) + lab + pad
    sheet = Image.new("RGB", (W, Ht), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    d.text((pad, 4), "source crop", fill=(160, 0, 0))
    d.text((s.size[0] + pad * 2, 4), "rendered svg", fill=(0, 130, 0))
    sheet.paste(s, (pad, lab))
    sheet.paste(r, (s.size[0] + pad * 2, lab))
    sheet.save(a.out)
    print("wrote", a.out, "  source", src.size, "  svg-render", ren.size)


if __name__ == "__main__":
    main()
