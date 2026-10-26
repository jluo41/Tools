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
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Mac, then Linux, then Windows (a Windows laptop has none of the first two, 261024): the first that exists is used
WIN = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
FONTS = ["/System/Library/Fonts/Supplemental/Arial Unicode.ttf", "/System/Library/Fonts/Helvetica.ttc",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         str(WIN / "arialuni.ttf"), str(WIN / "msyh.ttc"), str(WIN / "segoeui.ttf"), str(WIN / "arial.ttf")]


MONO = ["/System/Library/Fonts/Menlo.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        str(WIN / "CascadiaMono.ttf"), str(WIN / "consola.ttf")]


HAND = ["/System/Library/Fonts/Supplemental/ChalkboardSE.ttc", "/System/Library/Fonts/Noteworthy.ttc",
        str(WIN / "segoepr.ttf")]
# emoji draw in colour, as Excalidraw shows them (JL 261012: "add the things like the emoji"): a bitmap font,
# drawn once at its own size and scaled to the line; Windows' Segoe UI Emoji where Apple's is missing
EMOJI_FONT = next((f for f in ("/System/Library/Fonts/Apple Color Emoji.ttc", str(WIN / "seguiemj.ttf"))
                   if Path(f).exists()), "/System/Library/Fonts/Apple Color Emoji.ttc")
_BASE = ("[\\U0001F000-\\U0001FAFF\\u2600-\\u27BF\\u2B05-\\u2B07\\u2B1B\\u2B1C\\u2B50\\u23E9-\\u23FA"
         "\\u231A\\u231B][\\uFE0F\\U0001F3FB-\\U0001F3FF]?")
EMOJI = re.compile("((?:[0-9#*]\\uFE0F?\\u20E3)|(?:" + _BASE + "(?:\\u200D" + _BASE + ")*))")   # whole: 7️⃣, 👩‍⚕️
_emoji = {}


def emoji(seq, px):
    """The emoji `seq` as an RGBA picture `px` high, or None when no emoji font is there."""
    key = (seq, int(px))
    if key not in _emoji:
        if not Path(EMOJI_FONT).exists():
            return None
        try:
            f = ImageFont.truetype(EMOJI_FONT, 160)   # Apple's is a bitmap font drawn only at 160
        except OSError:
            _emoji[key] = None
            return None
        pic = Image.new("RGBA", (200 * max(1, len(seq)), 200), (0, 0, 0, 0))
        ImageDraw.Draw(pic).text((0, 0), seq, font=f, embedded_color=True)
        box = pic.getbbox()
        _emoji[key] = pic.crop(box).resize((max(1, int(px * (box[2] - box[0]) / 160)), max(1, int(px)))) if box else None
    return _emoji[key]


# Chinese, Japanese and Korean characters, which the code font (Menlo) lacks: drawn in the first FONTS face that
# has them (Arial Unicode), so a Chinese cell shows as itself, not as boxes (b51 s01 ②, 261021)
CJK = re.compile("([\u2E80-\u303F\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\uFF00-\uFFEF]+)")


def line_with_emoji(im, dr, x, y, line, f, fill, size):
    """Draw one line left-aligned: its words in `f`, each emoji as a colour picture, each run of Chinese in a face
    that has it; returns nothing."""
    for part in EMOJI.split(line):
        if not part:
            continue
        pic = emoji(part, size * 0.95) if EMOJI.fullmatch(part) else None
        if pic is not None:
            im.paste(pic, (int(x), int(y + size * 0.1)), pic)
            x += pic.width + size * 0.15
            continue
        for run in CJK.split(part):
            if not run:
                continue
            g = cjk_font(f) if CJK.fullmatch(run) else f
            dr.text((x, y), run, fill=fill, font=g)
            x += g.getlength(run)


_cjk = {}


def cjk_font(f):
    """A face of `f`'s size that has Chinese characters, or `f` itself when none is installed."""
    if f.size not in _cjk:
        path = next((p for p in FONTS if Path(p).exists() and ("Unicode" in p or p.endswith("msyh.ttc"))), None)
        _cjk[f.size] = ImageFont.truetype(path, f.size) if path else f
    return _cjk[f.size]


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
    data = json.loads(Path(src).read_text(encoding="utf-8"))   # a drawing is UTF-8 (Windows reads cp1252 by default)
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
            data_url = data["files"][e["fileId"]]["dataURL"]
            raw = base64.b64decode(data_url.split(",", 1)[1])
            if data_url.startswith("data:image/svg+xml"):
                converter = shutil.which("rsvg-convert")
                if not converter:
                    raise RuntimeError("SVG preview requires rsvg-convert")
                raw = subprocess.run(
                    [converter, "--width", str(max(1, int(w))),
                     "--height", str(max(1, int(h)))],
                    input=raw, capture_output=True, check=True, timeout=15,
                ).stdout
            pic = Image.open(io.BytesIO(raw)).convert("RGBA").resize((max(1, int(w)), max(1, int(h))))
            im.paste(pic, (int(x), int(y)), pic)
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
        f = font(e["fontSize"] * s, e.get("fontFamily", 2))
        step = e["fontSize"] * e.get("lineHeight", 1.25) * s   # the canvas's line height, so lines stack as there
        for i, line in enumerate(e["text"].split("\n")):
            if e.get("textAlign") == "center":
                dr.text((x + e["width"] * s / 2, y + i * step), line, fill=e["strokeColor"], font=f, anchor="ma")
            elif EMOJI.search(line) or CJK.search(line):
                line_with_emoji(im, dr, x, y + i * step, line, f, e["strokeColor"], e["fontSize"] * s)
            else:
                dr.text((x, y + i * step), line, fill=e["strokeColor"], font=f)
    save_preview(im, dst)
    print(Path(dst).name, im.size)


PREVIEW_W = 2400   # JL 261013: a 6000 px preview was 19 MB; 2400 px in 256 colours is 2 MB and still reads


def save_preview(im, dst):
    """Drawn at full scale, then shrunk to PREVIEW_W wide and saved in a 256-colour palette."""
    if im.width > PREVIEW_W:
        im = im.resize((PREVIEW_W, max(1, round(im.height * PREVIEW_W / im.width))), Image.LANCZOS)
    im.quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).save(dst, optimize=True)


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else None)
