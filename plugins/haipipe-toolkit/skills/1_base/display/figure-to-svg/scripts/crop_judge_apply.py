#!/usr/bin/env python3
"""Apply LLM-as-judge crop verdicts — the semantic judgement, made precise by code.

Usage:
    crop_judge_apply.py <source.png> <items.json> <crop_dir> <verdicts.json> [--margin 14]

The judge (a subagent, see Step 2.6) says WHAT and WHICH SIDE is wrong; this script makes the
pixel-exact change. verdicts.json:
  {"verdicts": [
     {"id": "A04_clinical_context", "usable": true, "clipped_sides": ["bottom"],
      "contaminated": false, "unclear": false, "note": "clock cut off at the bottom"},
     {"id": "M203_automation_cloud_service", "usable": true, "clipped_sides": [],
      "contaminated": true, "unclear": false, "note": "left panel line inside the box"},
     {"id": "B02_risk_score", "usable": false, "clipped_sides": [], "contaminated": false,
      "unclear": true, "note": "too blurry to reduce to primitives"}
  ]}

Actions:
  clipped_sides  -> grow the bbox outward on those sides by --margin (reveals the cut-off part;
                    follow with `crop_qc.py --apply` to snap the box tight to the now-fuller icon).
  contaminated   -> left to crop_qc's component filter (it drops marks not touching the icon); noted.
  usable=false+unclear -> set "keep_raster": true so the composer embeds the PNG instead of a vector.

Backs up items.json to .bak, rewrites bboxes/flags, and re-crops. Needs Pillow.
"""
import argparse, json, os, shutil
from PIL import Image

SIDES = {"left", "right", "top", "bottom"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("items")
    ap.add_argument("crop_dir")
    ap.add_argument("verdicts")
    ap.add_argument("--margin", type=int, default=14)
    a = ap.parse_args()

    src = Image.open(a.source).convert("RGB")
    W, H = src.size
    data = json.load(open(a.items, encoding="utf-8"))
    verds = {v["id"]: v for v in json.load(open(a.verdicts, encoding="utf-8")).get("verdicts", [])}
    by_id = {it["id"]: it for it in data.get("items", []) if it.get("type") == "icon"}

    grown = raster = 0
    for vid, v in verds.items():
        it = by_id.get(vid)
        if not it:
            print(f"  ? unknown id in verdicts: {vid}")
            continue
        x, y, w, h = it["bbox"]
        sides = set(v.get("clipped_sides", [])) & SIDES
        if sides:
            m = a.margin
            nx = max(0, x - (m if "left" in sides else 0))
            ny = max(0, y - (m if "top" in sides else 0))
            nx1 = min(W, x + w + (m if "right" in sides else 0))
            ny1 = min(H, y + h + (m if "bottom" in sides else 0))
            it["bbox"] = [nx, ny, nx1 - nx, ny1 - ny]
            grown += 1
        if not v.get("usable", True) and v.get("unclear"):
            it["keep_raster"] = True
            raster += 1

    shutil.copy(a.items, a.items + ".bak")
    json.dump(data, open(a.items, "w", encoding="utf-8"), indent=2)
    os.makedirs(a.crop_dir, exist_ok=True)
    for it in by_id.values():
        x, y, w, h = it["bbox"]
        src.crop((x, y, x + w, y + h)).save(os.path.join(a.crop_dir, it["id"] + ".png"))

    print(f"grew {grown} clipped bboxes, marked {raster} keep_raster; re-cropped {len(by_id)} icons "
          f"(backup items.json.bak)")
    if grown:
        print("next: run crop_qc.py --apply to snap the grown boxes tight to the revealed content")


if __name__ == "__main__":
    main()
