"""A topic's drawing from its face: each frame a folder tree, or boxes joined by named arrows, each box with its
own tree (haipipe-studio, The look; JL 261012: "so we can have both tree and box, and -->").

    python topic_map.py <topic folder>      draw <topic>.excalidraw and its preview from the face's frames: yaml

The face holds one fenced yaml block that starts `frames:`; three frames at most:

    - title: 🧭 <what the frame says>
      intro: <one line under the title>                 (optional)
      notes: [{date: "261012", text: <a change>}]       (optional: green notes)
      tree: [<a node>, ...]                             a folder tree: a string is a leaf, {label: [children]}
      cols: 2                                           a branch; "❓" or "? " first draws red, "✎ " green
    - title: ...
      boxes:                                            or boxes on a grid, each with its own tree
      - {id: a, at: [0, 0], title: 🧠 <name>, why: <why it is there>, tree: [...], most: 2}
      arrows:                                           named arrows between them; "?" first: red and dashed
      - {from: a, to: b, label: feeds, dashed: false}

block_index.py draws every Block's s00 with these same frames. A builder that needs a frame no yaml can say (a
screen in its colours) passes it to draw_topic(folder, extra=...).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import canvas  # noqa: E402

W, PAD = 2560, 40                                      # one screen (canvas.FRAME_MAX), its margin
TALL = 1450                                            # a frame takes one more column past this height
COL_W, WIDE = 700, 0.6                                 # one tree column; a frame's height to width, about a screen's
# the sizes, largest first, so a map reads zoomed out and its trees zoomed in (JL 261012: "If I just zoom in, how
# could I make it still readabale? SHould we give the box a large font size things?")
FRAME_SIZE, BOX_SIZE, WHY_SIZE, LABEL_SIZE = 48, 36, 24, 24


def frame_el(fid: str, name: str, w: float = W, h: float = 1) -> dict:
    return canvas._tree_base("frame", 0, 0, w, h, None, id=fid, name=name)


def draw_frame(els: list, fid: str, name: str, title: str, lines: list, nodes: list, cols: int, notes=(),
               w: float = canvas.FRAME_MAX[0]) -> None:
    """One frame: a title, a few lines under it, green change notes, then the tree, as wide as the tree needs. It tries
    one column of COL_W, then more, and keeps the first layout about as wide as a screen's shape (height at most
    WIDE x width); past `cols` columns only while it is still taller than TALL. Never wider than `w`."""
    best = None
    for c in range(1, cols + 3):
        width = min(w, c * COL_W + 2 * PAD)
        drawn, height = _layout(fid, name, title, lines, nodes, c, notes, width)
        best = (drawn, height)
        if height <= WIDE * width or (c >= cols and height <= TALL):
            break
    els += best[0]


def _layout(fid, name, title, lines, nodes, cols, notes, w):
    f = frame_el(fid, name, w)
    out = [f]
    e, h = canvas.tree_text(PAD, 28, title, FRAME_SIZE, w - 2 * PAD, fid)
    out.append(e)
    y = 28 + h + 10
    for ln in lines:
        e, h = canvas.tree_text(PAD, y, ln, 22, w - 2 * PAD, fid)
        out.append(e)
        y += h + 6
    for note in notes:
        out.append(canvas.change_note(PAD, y, note.get("text", ""), note.get("date"), fid))
        y += 22
    tr, th = canvas.tree(PAD, y + 24, nodes, w - 2 * PAD, fid, cols=cols)
    out += tr
    f["height"] = y + 24 + th + 40
    return out, f["height"]


# ── a map: boxes, each with a tree, joined by named arrows ────────────────────────────────────────────────────
# A tree alone lists what is there; the boxes and the arrows say why each part is there and how one leads to the
# next (JL 261012: "the tree is the pure tree here, there are no logic between them ... we need to display, show
# the index, and also need to explain, why we have them, so we can have both tree and box, and -->").
BOX_COL, BOX_PAD = 440, 24                             # one tree column inside a box; its margin
BOX_TALL = (700, 850, 1000, 1200, 1450)                # a box takes one more column past this; taller only to fit
GAP_X, GAP_Y = 180, 110                                # room between boxes for an arrow and its words


def _box(fid: str, b: dict, x: float, y: float, cols: int) -> tuple:
    """One box at (x, y): its title, why it is there, then its tree in `cols` columns. Returns (elements, w, h).
    `proposed: true`: not made yet, its edge and title red and dashed."""
    w = cols * BOX_COL + 2 * BOX_PAD
    out = []
    red = canvas.RED if b.get("proposed") else None
    e, h = canvas.tree_text(x + BOX_PAD, y + 18, b["title"], BOX_SIZE, w - 2 * BOX_PAD, fid, color=red)
    out.append(e)
    yy = y + 18 + h + 6
    if b.get("why"):
        e, h = canvas.tree_text(x + BOX_PAD, yy, b["why"], WHY_SIZE, w - 2 * BOX_PAD, fid)
        out.append(e)
        yy += h + 4
    if b.get("tree"):
        tr, th = canvas.tree(x + BOX_PAD, yy + 4, b["tree"], w - 2 * BOX_PAD, fid, cols=cols)
        out += tr
        yy += 4 + th
    h = yy - y + 14
    out.insert(0, canvas._tree_base("rectangle", x, y, w, h, fid, strokeWidth=3, roundness={"type": 3},
                                    strokeColor=red or canvas.INK, strokeStyle="dashed" if red else "solid"))
    return out, w, h


def _arrow(fid: str, a: tuple, b: tuple, label: str, dashed: bool = False) -> list:
    """A named arrow from box a to box b (each x, y, w, h), between their facing sides; its words above its middle.
    A label that starts with "?" draws red and dashed: a link not recorded yet."""
    (ax, ay, aw, ah), (bx, by, bw, bh) = a, b
    red = label.startswith(("?", "❓"))
    if ax + aw <= bx or bx + bw <= ax:                  # side by side: right side to left side, or back
        x1, x2 = (ax + aw, bx) if ax + aw <= bx else (ax, bx + bw)
        lo, hi = max(ay, by), min(ay + ah, by + bh)
        y1 = y2 = lo + min(90, (hi - lo) / 2) if lo < hi else None
        if y1 is None:                                  # no shared height: from near a's end to near b's
            y1 = ay + 60 if by < ay else ay + ah - 60
            y2 = by + bh - 60 if by < ay else by + 60
    else:                                               # one above the other: bottom to top
        lo, hi = max(ax, bx), min(ax + aw, bx + bw)
        x1 = x2 = lo + min(140, (hi - lo) / 2)
        y1, y2 = (ay + ah, by) if ay + ah <= by else (ay, by + bh)
    arrow = canvas._tree_base("arrow", x1, y1, max(1, abs(x2 - x1)), max(1, abs(y2 - y1)), fid, strokeWidth=3,
                              strokeStyle="dashed" if dashed or red else "solid",
                              strokeColor=canvas.RED if red else canvas.INK, points=[[0, 0], [x2 - x1, y2 - y1]],
                              lastCommittedPoint=None, startBinding=None, endBinding=None, startArrowhead=None,
                              endArrowhead="arrow")
    width = GAP_X - 30 if y1 == y2 else 230
    words, h = canvas.tree_text(0, 0, label, LABEL_SIZE, width, fid)
    words["x"] = (x1 + x2) / 2 - words["width"] / 2 if y1 == y2 else (x1 + x2) / 2 + 12
    words["y"] = (y1 + y2) / 2 - h - 8 if y1 == y2 else (y1 + y2) / 2 - h / 2
    return [arrow, words]


def draw_map(els: list, fid: str, name: str, title: str, lines: list, boxes: list, arrows: list, notes=(),
             stack: bool = False) -> None:
    """One frame: a title, a few lines, then `boxes` on a grid (each box's `at: [col, row]`), each as wide as its
    tree needs (one more column of BOX_COL past BOX_TALL, `most` columns at most), and `arrows` [from, to, label,
    dashed] between them. `stack`: each column stacks its own boxes, so a tall box leaves no empty cell beside it."""
    ncol, nrow = max(b["at"][0] for b in boxes) + 1, max(b["at"][1] for b in boxes) + 1
    for tall in BOX_TALL:                               # boxes grow down before the frame grows past the screen
        sized = {}
        for b in boxes:
            for c in ([int(b["cols"])] if b.get("cols") else range(1, int(b.get("most", 3)) + 1)):
                _, w, h = _box(fid, b, 0, 0, c)
                if h <= tall:
                    break
            sized[b["id"]] = (c, w, h)
        colw = [max([sized[b["id"]][1] for b in boxes if b["at"][0] == c] or [0]) for c in range(ncol)]
        rowh = [max([sized[b["id"]][2] for b in boxes if b["at"][1] == r] or [0]) for r in range(nrow)]
        width = sum(colw) + GAP_X * (ncol - 1) + 2 * PAD
        if width <= canvas.FRAME_MAX[0]:
            break
    for b in boxes:                                     # a box as wide as its column allows: the room is there anyway
        if b.get("cols"):
            continue
        c0 = b["at"][0]
        for c in range(int(b.get("most", 3)), sized[b["id"]][0], -1):
            _, w, h = _box(fid, b, 0, 0, c)
            if w <= colw[c0] and h < sized[b["id"]][2]:
                sized[b["id"]] = (c, w, h)
                break
    rowh = [max([sized[b["id"]][2] for b in boxes if b["at"][1] == r] or [0]) for r in range(nrow)]
    f = frame_el(fid, name, width)
    f["customData"] = {"map": True}                     # its boxes and arrows carry meaning (canvas.sparse)
    out = [f]
    e, h = canvas.tree_text(PAD, 28, title, FRAME_SIZE, width - 2 * PAD, fid)
    out.append(e)
    y = 28 + h + 10
    for ln in lines:
        e, h = canvas.tree_text(PAD, y, ln, 22, width - 2 * PAD, fid)
        out.append(e)
        y += h + 6
    for note in notes:
        out.append(canvas.change_note(PAD, y, note.get("text", ""), note.get("date"), fid))
        y += 22
    xs = [PAD + sum(colw[:c]) + GAP_X * c for c in range(ncol)]
    ys = [y + 30 + sum(rowh[:r]) + GAP_Y * r for r in range(nrow)]
    at, below = {}, {}
    for b in sorted(boxes, key=lambda b: (b["at"][1], b["at"][0])):
        c, r = b["at"]
        top = below.get(c, y + 30) if stack else ys[r]
        drawn, w, h = _box(fid, b, xs[c], top, sized[b["id"]][0])
        out += drawn
        at[b["id"]] = (xs[c], top, w, h)
        below[c] = top + h + GAP_Y
    for a in arrows:
        if a[0] in at and a[1] in at:
            out += _arrow(fid, at[a[0]], at[a[1]], a[2], bool(a[3]) if len(a) > 3 else False)
    f["height"] = max(v[1] + v[3] for v in at.values()) + PAD
    els += out


def frames_of(face: Path, key: str = "frames") -> list:
    """The face's fenced yaml block that starts `<key>:`, as a list of frames."""
    import yaml
    text = face.read_text(encoding="utf-8") if face.is_file() else ""
    m = re.search(rf"```yaml\n({key}:.*?)\n```", text, re.S)
    return (yaml.safe_load(m.group(1)) or {}).get(key) or [] if m else []


def draw_frames(els: list, frames: list, prefix: str) -> None:
    """Each frame as a tree or as a map, ids `frame-<prefix>-<n>`, names `<prefix> · <title>`."""
    for i, fr in enumerate(frames, 1):
        fid, name, title = f"frame-{prefix}-{i}", f"{prefix} · {fr.get('title', i)}", fr.get("title", f"{prefix} {i}")
        lines = [fr["intro"]] if fr.get("intro") else []
        if fr.get("boxes"):
            draw_map(els, fid, name, title, lines, fr["boxes"],
                     [(a["from"], a["to"], a.get("label", ""), a.get("dashed", False)) for a in fr.get("arrows") or []],
                     fr.get("notes") or ())
        else:
            draw_frame(els, fid, name, title, lines, fr.get("tree") or [], int(fr.get("cols", 2)), fr.get("notes") or ())


def draw_topic(folder: Path, extra=None, source: str = "", fill=None, lead=None) -> Path:
    """Draw <topic>.excalidraw: `lead(els)` first (the topic's own main picture, when a builder draws it: a screen),
    then the face's frames, then `extra(els)`, in one row; the person's marks are kept (canvas.write) and the
    preview rendered. `fill(frames)` puts facts read from disk into the face's frames first and returns them. A topic
    leads with its own picture, never with the index's shape (JL 261012: "why s07 following the index????? it is
    very weird")."""
    folder = Path(folder).resolve()
    els, frames = [], frames_of(folder / f"{folder.name}.md")
    if fill:
        frames = fill(frames) or frames
    if lead:
        lead(els)
    draw_frames(els, frames, re.match(r"s\d+", folder.name).group(0))
    if extra:
        extra(els)
    canvas.grid(els, [[e["id"] for e in els if e["type"] == "frame"]])
    out = folder / f"{folder.name}.excalidraw"
    canvas.write(out, els, source or f"haipipe-studio scripts/topic_map.py {folder.name}")
    from render_png import render
    render(out, out.with_suffix(".png"))
    return out


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        print(draw_topic(Path(arg)))
