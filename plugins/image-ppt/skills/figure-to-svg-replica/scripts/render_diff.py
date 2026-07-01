#!/usr/bin/env python3
"""Render the composed master SVG and place it side-by-side with the original figure.

Usage:
    render_diff.py <replica.svg> <source.png> [out.png] [--overlay]

Renders the SVG at the source's pixel size and writes a comparison sheet: source | replica. With
--overlay, adds a third panel showing a 50/50 blend so misalignments pop out.
Needs: cairosvg, Pillow. Run with the fig2svg venv (see SKILL.md setup).
"""
import argparse, io
import cairosvg
from PIL import Image, ImageChops, ImageDraw


def on_white(im):
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    bg.alpha_composite(im.convert("RGBA"))
    return bg.convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svg")
    ap.add_argument("source")
    ap.add_argument("out", nargs="?", default="/tmp/fig2svg_diff.png")
    ap.add_argument("--overlay", action="store_true",
                    help="add a blended overlay panel to spot misalignment")
    a = ap.parse_args()

    src = on_white(Image.open(a.source))
    W, H = src.size

    png = cairosvg.svg2png(url=a.svg, output_width=W, output_height=H, background_color="white")
    rep = Image.open(io.BytesIO(png)).convert("RGB")
    if rep.size != (W, H):
        rep = rep.resize((W, H))

    panels = [("original", src), ("replica", rep)]
    if a.overlay:
        panels.append(("overlay 50/50", Image.blend(src, rep, 0.5)))

    pad, lab = 14, 24
    sheet_w = sum(p[1].size[0] for p in panels) + pad * (len(panels) + 1)
    sheet_h = H + lab + pad
    sheet = Image.new("RGB", (sheet_w, sheet_h), (245, 245, 245))
    d = ImageDraw.Draw(sheet)
    x = pad
    for name, img in panels:
        d.text((x, 6), name, fill=(40, 40, 40))
        sheet.paste(img, (x, lab))
        x += img.size[0] + pad
    sheet.save(a.out)

    # quick numeric signal
    diff = ImageChops.difference(src, rep)
    bbox = diff.getbbox()
    print(f"wrote {a.out}  source={src.size} replica={rep.size}"
          f"  diff-bbox={bbox}")


if __name__ == "__main__":
    main()
