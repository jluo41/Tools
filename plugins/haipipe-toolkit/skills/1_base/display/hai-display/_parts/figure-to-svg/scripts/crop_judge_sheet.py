#!/usr/bin/env python3
"""Build the input images for the LLM-as-judge crop review (Step 2.6).

Usage:
    crop_judge_sheet.py <source.png> <items.json> <out_dir> [--scale 5] [--context 64] [--only id,id]

For each icon item, writes <out_dir>/<id>.png — a two-panel image the judge subagent looks at:
  LEFT  : the isolated crop (what will actually be vectorized), enlarged.
  RIGHT : the same region IN CONTEXT — the source neighbourhood with the crop's bbox drawn in red —
          so the judge can see whether the icon is clipped by the box or whether a neighbour's mark
          has bled inside it (judgements that need the surroundings, not just the crop).

Also writes <out_dir>/manifest.json listing the ids. Feed each panel image to a judge agent; see the
figure skill's Step 2.6 for the verdict schema. Needs Pillow.
"""
import argparse, json, os
from PIL import Image, ImageDraw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("items")
    ap.add_argument("out_dir")
    ap.add_argument("--scale", type=int, default=5)
    ap.add_argument("--context", type=int, default=64)
    ap.add_argument("--only", default=None, help="comma-separated ids to limit to (escalation mode)")
    a = ap.parse_args()

    src = Image.open(a.source).convert("RGB")
    W, H = src.size
    data = json.load(open(a.items, encoding="utf-8"))
    only = set(a.only.split(",")) if a.only else None
    os.makedirs(a.out_dir, exist_ok=True)

    ids = []
    for it in data.get("items", []):
        if it.get("type") != "icon":
            continue
        if only and it["id"] not in only:
            continue
        x, y, w, h = it["bbox"]
        crop = src.crop((x, y, x + w, y + h))
        iso = crop.resize((w * a.scale, h * a.scale), Image.NEAREST)

        c = a.context
        cx0, cy0 = max(0, x - c), max(0, y - c)
        cx1, cy1 = min(W, x + w + c), min(H, y + h + c)
        ctx = src.crop((cx0, cy0, cx1, cy1)).copy()
        d = ImageDraw.Draw(ctx)
        d.rectangle((x - cx0, y - cy0, x - cx0 + w - 1, y - cy0 + h - 1), outline=(230, 20, 20), width=2)
        # scale context so its height matches the isolated panel
        s = iso.size[1] / ctx.size[1]
        ctx = ctx.resize((max(1, int(ctx.size[0] * s)), iso.size[1]), Image.NEAREST)

        pad, lab = 10, 20
        sheet = Image.new("RGB", (iso.size[0] + ctx.size[0] + pad * 3, iso.size[1] + lab + pad), (245, 245, 245))
        dr = ImageDraw.Draw(sheet)
        dr.text((pad, 4), f"{it['id']}   LEFT: isolated crop   RIGHT: context (red = crop box)", fill=(20, 20, 20))
        sheet.paste(iso, (pad, lab))
        sheet.paste(ctx, (iso.size[0] + pad * 2, lab))
        sheet.save(os.path.join(a.out_dir, it["id"] + ".png"))
        ids.append(it["id"])

    json.dump({"source": os.path.basename(a.source), "ids": ids},
              open(os.path.join(a.out_dir, "manifest.json"), "w"), indent=2)
    print(f"wrote {len(ids)} judge panels -> {a.out_dir}  (+ manifest.json)")


if __name__ == "__main__":
    main()
