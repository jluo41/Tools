"""s07 · The venue’s displays, as examples: s07-paper-display-examples.excalidraw, drawn by this builder.

How it looks and reads: /excalidraw-studio, its principles and scripts/draw.py (frames, a map, the key point,
the density badge, acts). The topic, its face and sessions: /haipipe-studio. A rebuild keeps whatever a person drew
on the canvas (canvas.write, a seed snapshot beside the drawing). Check it: excalidraw-studio's scripts/check.py.

The words come from the face's ### Examples yaml block: one column per display of ours, the venue's examples for it
on top as placeholder boxes (a picture of the published display is pasted over each), an arrow down to ours.

    python build_s07_paper_display_examples.py
"""
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../../../plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts").resolve()))
from draw import Drawing, RED, canvas  # noqa: E402  (excalidraw-studio's helpers; canvas.write keeps a person's marks)

# every change to this drawing: (date YYMMDD, what changed). Each gets a green note where it changed
# (canvas.change_note beside the changed thing) and a line in the title frame (asked 261007)
CHANGES = []
COL, CARD, GAP = 800, 370, 60          # a column per display of ours; two example cards side by side in it
TOP, CARD_H, OURS_Y, OURS_H = 300, 460, 900, 200


def face_yaml() -> dict:
    face = (HERE / "s07-paper-display-examples.md").read_text(encoding="utf-8")
    m = re.search(r"(?ms)^### Examples\s*\n.*?```yaml\n(.*?)```", face)
    return yaml.safe_load(m.group(1)) if m else {}


def sketch(d: Drawing, kind: str, x: float, y: float, w: float, h: float) -> None:
    """A placeholder for the published display's picture: a dashed box with the shape of what it shows."""
    d.box(x, y, w, h, dashed=True)
    l, r, t, b = x + 30, x + w - 30, y + 24, y + h - 24
    if kind == "table":
        for k in range(5):
            yy = t + k * (b - t) / 4
            d.line([(l, yy), (r, yy)], arrow=False, sw=1 if 0 < k < 4 else 2)
        return
    d.line([(l, t), (l, b), (r, b)], arrow=False)                          # the axes
    if kind == "bars":
        for k, frac in enumerate((0.45, 0.7, 0.55, 0.85)):
            bw = (r - l - 40) / 4 - 16
            d.box(l + 20 + k * (bw + 16), b - frac * (b - t), bw, frac * (b - t))
    elif kind == "line":
        pts = [(l + 10 + k * (r - l - 20) / 5, b - f * (b - t)) for k, f in enumerate((0.2, 0.35, 0.3, 0.55, 0.6, 0.8))]
        d.line(pts, arrow=False, sw=2)
    else:                                                                    # dots: estimates with their intervals
        for k, (mid, half) in enumerate(((0.5, 0.2), (0.62, 0.15), (0.4, 0.25), (0.55, 0.12))):
            cy = t + (k + 0.5) * (b - t) / 4
            cx = l + mid * (r - l)
            d.line([(cx - half * (r - l), cy), (cx + half * (r - l), cy)], arrow=False)
            d.box(cx - 6, cy - 6, 12, 12, fill="#1e1e1e")


def main():
    data = face_yaml()
    out = HERE / "s07-paper-display-examples.excalidraw"
    d = Drawing()
    f1 = d.frame("① The venue’s displays, as examples")                     # one idea, one screen-sized frame
    d.heading("s07 · The venue’s displays, as examples")
    d.key(40, 160, 2480, 96)                                               # the frame's key point, the one slight colour
    d.para(64, 186, data.get("key", "<the key point, in one line>"), 2420, 30)
    ours = data.get("ours") or []
    for c, mine in enumerate(ours):
        x0 = 40 + c * (COL + 40)
        cards = [e for e in data.get("examples") or [] if e.get("ours") == mine["name"]]
        for k, ex in enumerate(cards[:2]):
            x = x0 + k * (CARD + GAP)
            d.box(x, TOP, CARD, CARD_H)
            d.para(x + 18, TOP + 16, ex["name"], CARD - 36, 30)
            sketch(d, ex.get("sketch", "bars"), x + 20, TOP + 110, CARD - 40, 220)
            d.para(x + 18, TOP + 350, ex.get("shows", ""), CARD - 36, 28)
            d.line([(x + CARD / 2, TOP + CARD_H), (x + CARD / 2, OURS_Y)], sw=2)      # compared with ours, below
        if len(cards) < 2 and data.get("open") and c == len(ours) - 1:            # the open choice, in red
            x = x0 + CARD + GAP
            d.box(x, TOP, CARD, CARD_H, RED, dashed=True)
            d.para(x + 18, TOP + 140, data["open"], CARD - 36, 34, RED)
        d.text(x0 + COL / 2 + 16, OURS_Y - 80, "compare with", 28)
        d.box(x0 + 100, OURS_Y, COL - 200, OURS_H, sw=3)
        d.text(x0 + 130, OURS_Y + 28, f"{mine['name']} · ours", 38)
        d.para(x0 + 130, OURS_Y + 96, mine.get("kind", ""), COL - 260, 30)
    for i, (date, what) in enumerate(CHANGES):                             # the title frame's list of changes
        e = canvas.change_note(1480, 1220 + i * 26, what, date, f1["id"])
        e["id"] = f"c{i}"
        d.els.append(e)
    d.badge(f1)                                                            # its density, measured
    d.acts([{"name": "Act 1 · the venue’s displays beside ours", "frames": [f1["id"]]}])
    d.write(out, "build_s07_paper_display_examples.py")


if __name__ == "__main__":
    main()
