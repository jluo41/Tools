#!/usr/bin/env python3
"""Build a labeled contact sheet of all icon crops — the artifact you (and an LLM judge) eyeball.

Usage:
    contact_sheet.py <crop_dir> <out.png> [--cols 6] [--cell 160]

Tiles every <id>.png in the crop dir into one labeled grid so a human — and an LLM-as-judge — can
review all crops at a glance for clipping / contamination / wrong content, instead of trusting
numbers. This is `_crop_sheet.png`; the icon-vs-svg equivalent is `_icon_eval.png` from
`evaluate_icons.py`. Both must be looked at. Needs Pillow.
"""
import argparse, glob, math, os
from PIL import Image, ImageDraw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("crop_dir")
    ap.add_argument("out")
    ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--cell", type=int, default=160)
    a = ap.parse_args()

    files = sorted(glob.glob(os.path.join(a.crop_dir, "*.png")))
    if not files:
        print("no crops found in", a.crop_dir)
        return
    cols = a.cols
    rows = math.ceil(len(files) / cols)
    cell, lab = a.cell, 22
    sheet = Image.new("RGB", (cols * cell, rows * cell), (235, 235, 235))
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(files):
        im = Image.open(f).convert("RGB")
        s = min((cell - 16) / im.width, (cell - lab - 12) / im.height)
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))))
        cx, cy = (i % cols) * cell, (i // cols) * cell
        sheet.paste(im, (cx + (cell - im.width) // 2, cy + lab + (cell - lab - im.height) // 2))
        name = os.path.splitext(os.path.basename(f))[0]
        d.text((cx + 3, cy + 4), name[:26], fill=(20, 20, 20))
        d.rectangle((cx, cy, cx + cell - 1, cy + cell - 1), outline=(200, 200, 200))
    sheet.save(a.out)
    print(f"wrote {a.out}  ({len(files)} crops, {cols}x{rows})")


if __name__ == "__main__":
    main()
