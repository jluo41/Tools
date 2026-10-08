"""Offline PNG preview of an .excalidraw file (haipipe-studio; moved here from b03 studio/_build/ on
261007).

Draws rectangles, ellipses, lines, arrows, embedded images and text with Pillow, so a preview can be rebuilt
without a browser. It is a preview, not Excalidraw's own renderer: open the .excalidraw for
the real drawing.

    python render_png.py <in.excalidraw> <out.png> [scale]
"""
import base64
import io
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONTS = ["/System/Library/Fonts/Supplemental/Arial Unicode.ttf", "/System/Library/Fonts/Helvetica.ttc",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]


MONO = ["/System/Library/Fonts/Menlo.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]


HAND = ["/System/Library/Fonts/Supplemental/ChalkboardSE.ttc", "/System/Library/Fonts/Noteworthy.ttc"]


def font(size, family=2):
    for f in {1: HAND, 3: MONO, 5: HAND}.get(family, []) + FONTS:   # 6 Nunito -> a plain sans
        if Path(f).exists():
            return ImageFont.truetype(f, max(6, int(size)))
    return ImageFont.load_default()


def dashed(dr, p, q, col, w, dash=10):
    n = max(1, int(math.dist(p, q) // dash))
    for i in range(0, n, 2):
        a, b = i / n, min(1, (i + 1) / n)
        dr.line([(p[0] + (q[0] - p[0]) * a, p[1] + (q[1] - p[1]) * a),
                 (p[0] + (q[0] - p[0]) * b, p[1] + (q[1] - p[1]) * b)], fill=col, width=w)


def render(src, dst, s=None):
    data = json.loads(Path(src).read_text())
    els = [e for e in data["elements"] if not e.get("isDeleted")]
    x0 = min(e["x"] for e in els) - 30
    y0 = min(e["y"] for e in els) - 30
    W = max(e["x"] + e["width"] for e in els) - x0 + 30
    H = max(e["y"] + e["height"] for e in els) - y0 + 30
    s = s or min(0.6, 6000 / W)        # a wide multi-frame drawing is scaled to stay under 6000 px
    im = Image.new("RGB", (int(W * s), int(H * s)), "white")
    dr = ImageDraw.Draw(im)
    P = lambda x, y: ((x - x0) * s, (y - y0) * s)
    for e in els:
        if e["type"] == "text":
            continue
        (x, y), w, h = P(e["x"], e["y"]), e["width"] * s, e["height"] * s
        st = e["strokeColor"]
        bg = None if e["backgroundColor"] == "transparent" else e["backgroundColor"]
        sw = max(1, int(e["strokeWidth"] * s))
        if e["type"] == "frame":
            dr.rectangle([x, y, x + w, y + h], outline="#c9ccd1", width=1)
        elif e["type"] == "rectangle":
            r = 10 * s if e.get("roundness") else 0
            if bg:
                dr.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=bg)
            if e["strokeStyle"] == "dashed":
                for p, q in [((x, y), (x + w, y)), ((x + w, y), (x + w, y + h)), ((x + w, y + h), (x, y + h)), ((x, y + h), (x, y))]:
                    dashed(dr, p, q, st, sw)
            elif st != "transparent":
                dr.rounded_rectangle([x, y, x + w, y + h], radius=r, outline=st, width=sw)
        elif e["type"] == "image" and e.get("fileId") in data.get("files", {}):
            raw = base64.b64decode(data["files"][e["fileId"]]["dataURL"].split(",", 1)[1])
            pic = Image.open(io.BytesIO(raw)).convert("RGB").resize((max(1, int(w)), max(1, int(h))))
            im.paste(pic, (int(x), int(y)))
        elif e["type"] == "ellipse":
            dr.ellipse([x, y, x + w, y + h], fill=bg, outline=None if st == "transparent" else st, width=sw)
        elif e["type"] in ("arrow", "line"):
            pts = [P(e["x"] + p[0], e["y"] + p[1]) for p in e["points"]]
            for p, q in zip(pts, pts[1:]):
                (dashed(dr, p, q, st, sw) if e["strokeStyle"] == "dashed" else dr.line([p, q], fill=st, width=sw))
            if e["type"] == "arrow" and e.get("endArrowhead"):
                p, q = pts[-2], pts[-1]
                a, L = math.atan2(q[1] - p[1], q[0] - p[0]), 16 * s
                dr.polygon([q, (q[0] - L * math.cos(a - .45), q[1] - L * math.sin(a - .45)),
                            (q[0] - L * math.cos(a + .45), q[1] - L * math.sin(a + .45))], fill=st)
    for e in els:
        if e["type"] != "text":
            continue
        x, y = P(e["x"], e["y"])
        if e.get("textAlign") == "center":
            dr.multiline_text((x + e["width"] * s / 2, y), e["text"], fill=e["strokeColor"], font=font(e["fontSize"] * s, e.get("fontFamily", 2)),
                              anchor="ma", align="center", spacing=4)
        else:
            dr.multiline_text((x, y), e["text"], fill=e["strokeColor"], font=font(e["fontSize"] * s, e.get("fontFamily", 2)), spacing=4)
    im.save(dst)
    print(Path(dst).name, im.size)


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else None)
