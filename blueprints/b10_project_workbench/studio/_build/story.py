"""Lay a topic's frames out as a story in acts, not one strip (JL 261012: "we should not put all the frames just
always from left to right ... it needs a better arrangement").

    import story
    story.arrange(els, acts, bridges)

`key_point` and `big_titles` bring a topic_map frame to excalidraw-studio's principle 5 (b31-s01's ask, 261012):
one box per frame in the slight colour, the frame's title at 60 px. Call both before `arrange`; write with
`canvas.write(..., palette=False)`, or the writer drops the key point's fill.

`acts` is a list of {"title": "Act 1 · <what this row says>", "frames": [frame id, ...]}: one act is one row,
read left to right, its title large in a margin on the left; the acts are read top to bottom. `bridges` names the
step from each frame to the next, in reading order: an arrow across inside a row, and between rows an arrow that
turns down from the last frame of one act to the first frame of the next. Call it once, after the frames are
drawn and before canvas.write; every element of a frame moves with it.
"""
from __future__ import annotations

import sys
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/skills/1_base"
sys.path.insert(0, str(SKILLS / "project/haipipe-studio/scripts"))
sys.path.insert(0, str(SKILLS / "excalidraw/excalidraw-studio/scripts"))
import canvas  # noqa: E402
from draw import KEY, T_FRAME  # noqa: E402  (excalidraw-studio principle 5: the key point's colour, a title's size)

GUTTER, GAP_X, GAP_Y = 760, 260, 420            # the act titles' margin; room between frames, and between acts
ACT_SIZE, BRIDGE_SIZE = 56, 28


def _move(els: list, fid: str, x: float, y: float) -> None:
    f = next(e for e in els if e["id"] == fid)
    dx, dy = x - f["x"], y - f["y"]
    for e in els:
        if e["id"] == fid or e.get("frameId") == fid:
            e["x"], e["y"] = e["x"] + dx, e["y"] + dy


def _arrow(aid: str, points: list) -> dict:
    (x0, y0) = points[0]
    rel = [[x - x0, y - y0] for x, y in points]
    xs, ys = [p[0] for p in rel], [p[1] for p in rel]
    return canvas._tree_base("arrow", x0, y0, max(1, max(xs) - min(xs)), max(1, max(ys) - min(ys)), None,
                             id=aid, strokeWidth=4, points=rel, lastCommittedPoint=None, startBinding=None,
                             endBinding=None, startArrowhead=None, endArrowhead="arrow")


def _words(tid: str, text: str, x: float, y: float, size: int, width: float) -> dict:
    t, h = canvas.tree_text(0, 0, text, size, width, None)
    t.update(id=tid, x=x, y=y - h)
    return t


def arrange(els: list, acts: list, bridges: list, aside: dict | None = None) -> list:
    """`aside` = {"title": ..., "frames": [ids]}: frames outside the story (what comes later), set in one column to
    the right of every act, under their own title, with no story arrow (JL 261012: "put a new frame in the
    rightmost and put all the later in that new frame")."""
    frames = {e["id"]: e for e in els if e["type"] == "frame"}
    side = list((aside or {}).get("frames") or [])
    placed = [fid for act in acts for fid in act["frames"]]
    assert sorted(placed + side) == sorted(frames), f"arrange() places each frame once: {placed + side} vs {list(frames)}"
    y = 0
    for i, act in enumerate(acts):
        x = GUTTER
        for fid in act["frames"]:
            _move(els, fid, x, y)
            x += frames[fid]["width"] + GAP_X
        title, h = canvas.tree_text(0, 0, act["title"], ACT_SIZE, GUTTER - 120, None)
        title.update(id=f"story-act-{i}", x=0, y=y + 20)
        els.append(title)
        y += max(frames[fid]["height"] for fid in act["frames"]) + GAP_Y
    if side:
        right = max(frames[fid]["x"] + frames[fid]["width"] for fid in placed) + GAP_X + 140
        title, h = canvas.tree_text(0, 0, aside.get("title", ""), ACT_SIZE, 1600, None)
        title.update(id="story-aside", x=right, y=-h - 30)
        els.append(title)
        yy = 0
        for fid in side:
            _move(els, fid, right, yy)
            yy += frames[fid]["height"] + GAP_Y
    row = {fid: i for i, act in enumerate(acts) for fid in act["frames"]}
    floor = [max(frames[f]["y"] + frames[f]["height"] for f in act["frames"]) for act in acts]   # each act's bottom
    for n, (a, b) in enumerate(zip(placed, placed[1:])):
        fa, fb, label = frames[a], frames[b], bridges[n] if n < len(bridges) else ""
        if row[a] == row[b]:                          # across, in the gap between two frames of one act
            x1, x2, yy = fa["x"] + fa["width"] + 20, fb["x"] - 20, fa["y"] + 120
            els.append(_arrow(f"story-{n}", [(x1, yy), (x2, yy)]))
            els.append(_words(f"story-{n}-words", label, x1 + 10, yy - 10, BRIDGE_SIZE, x2 - x1 - 20))
        else:                                         # down from the end of one act, back to the start of the next
            xa, ya = fa["x"] + fa["width"] / 2, fa["y"] + fa["height"] + 20
            xb, yb = fb["x"] + fb["width"] / 2, fb["y"] - 20
            mid = (floor[row[a]] + 20 + yb) / 2       # below the act's tallest frame, never through it
            els.append(_arrow(f"story-{n}", [(xa, ya), (xa, mid), (xb, mid), (xb, yb)]))
            els.append(_words(f"story-{n}-words", label, min(xa, xb) + 40, mid - 12, BRIDGE_SIZE, abs(xa - xb) - 80))
    return els


def key_point(els: list, fid: str, title: str) -> None:
    """Principle 5: the box whose title is `title`, in frame `fid`, filled with the one slight colour, its edge bold."""
    norm = " ".join(str(title).split())
    t = next((e for e in els if e.get("frameId") == fid and e["type"] == "text"
              and " ".join(str(e.get("text", "")).split()) == norm), None)
    assert t is not None, f"key_point: no box titled {title!r} in {fid}"
    box = min((e for e in els if e.get("frameId") == fid and e["type"] == "rectangle"
               and e["x"] <= t["x"] <= e["x"] + e["width"] and e["y"] <= t["y"] <= e["y"] + e["height"]),
              key=lambda e: e["width"] * e["height"])
    box.update(backgroundColor=KEY, fillStyle="solid", strokeWidth=4.5)


def big_titles(els: list, size: int = T_FRAME) -> None:
    """Principle 5: each frame's title (its largest, topmost words) set at `size`; what sits below moves down."""
    for f in [e for e in els if e["type"] == "frame"]:
        mine = [e for e in els if e.get("frameId") == f["id"]]
        texts = [e for e in mine if e["type"] == "text"]
        if not texts:
            continue
        top = max(texts, key=lambda e: (e.get("fontSize", 0), -e["y"]))
        if top.get("fontSize", 0) >= size:
            continue
        new, h = canvas.tree_text(top["x"], top["y"], " ".join(str(top["text"]).split()), size,
                                  f["width"] - 2 * top["x"], f["id"])
        dh = h - top["height"]
        for e in mine:
            if e is not top and e["y"] > top["y"]:
                e["y"] += dh
        top.update({k: new[k] for k in ("text", "originalText", "fontSize", "width", "height")})
        f["height"] += dh
