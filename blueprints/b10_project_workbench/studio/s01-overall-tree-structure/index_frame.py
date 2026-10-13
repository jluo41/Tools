"""s01 frames 3 and 4 · the SPACE Home index: drawn into s01-overall-tree-structure.excalidraw by build_ladder_v4.py,
below frame 2, whose INDEX box they draw out (JL 261012: "for the s01 we want to put the index to it, the design of
the index of the chart and list"). On excalidraw-studio's draw.py: frame 3 a workflow map (what the index reads, its
two views, the Guide's way back in), frame 4 the two screens as they looked when taken.

Every word is the face's `index_drawing:` yaml; the screens are the two .jpg files it names, beside the face.

    draw(L)    L: the build_ladder_v4 module that is drawing; returns (frame ids, embedded files)
"""
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3] / "plugins/haipipe-toolkit/skills/1_base/display/excalidraw-studio/scripts"))
from draw import T_KEY, T_SMALL, W, Drawing, canvas  # noqa: E402


def words():
    text = (HERE / f"{HERE.name}.md").read_text(encoding="utf-8")
    return yaml.safe_load(re.search(r"```yaml\n(index_drawing:.*?)\n```", text, re.S).group(1))["index_drawing"]


def index_map(d, w):
    """③: what the index reads, its two views, the Guide's way back in, what is still open."""
    f = d.frame(w["title"])
    d.heading(w["title"])                            # ⑦: few words, large; the title says what the frame is
    d.key(40, 120, W - 80, 90)
    d.para(66, 142, w["key"], W - 132, T_KEY)
    steps = d.flow(w["flow"], 40, 270, W - 80, gap=170, title=36, leaf=28, labels=w["labels"])
    y = max(sy + sh for _, sy, _, sh in steps) + 110
    d.text(40, y - 64, "how a person gets back to it", 30)
    way = d.flow(w["way_in"], 40, y, 1700, gap=170, title=36, leaf=28, labels=w["way_labels"])
    ox, oy = 1820, y
    for point in w["open"]:
        oy = d.para(ox, oy, point, W - ox - 40, 28) + 14                # red while it starts ❓, black once later
    d.els.append(canvas.change_note(ox, oy, "s01 closed: these points moved to Later (s01-D40)", "261012", d.fid, 20))
    oy += 34
    bottom = max(max(sy + sh for _, sy, _, sh in way), oy) + 30
    d.els.append(canvas.change_note(40, bottom, "new frame: frame 2's INDEX box drawn out, the Chart and the List "
                                    "as built (s01-D38, D39)", "261012", d.fid, 20))
    f["height"] = bottom + 60
    d.badge(f)
    return f


def screens(d, w):
    """④: the two screens, side by side, as pictures (not measured for density)."""
    f = d.frame(w["screens_title"])
    d.heading(w["screens_title"])
    h = d.height(w["screens_sub"], W - 132, T_SMALL + 3)
    d.key(40, 110, W - 80, h + 36)                   # its key point: what the two screens show
    d.para(66, 128, w["screens_sub"], W - 132, T_SMALL + 3)
    pw, gap, top = (W - 80 - 60) / 2, 60, 110 + h + 80
    hs = [d.picture(HERE / name, 40 + k * (pw + gap), top, pw, 900) for k, name in enumerate(w["screens"])]
    f["height"] = top + max(hs) + 60
    d.badge(f)
    return f


def draw(L):
    """Frames 3 and 4 into L's drawing: ids prefixed so they never meet build_ladder_v4's. Returns ([frame 3 id,
    frame 4 id], the embedded pictures for canvas.write's files=)."""
    w = words()
    d = Drawing()
    ids = [index_map(d, w)["id"], screens(d, w)["id"]]
    for e in d.els:                                  # draw.py numbers e0, e1 …; frame 2's notes use e<N> too
        e["id"] = "ix-" + e["id"]
        if e.get("frameId"):
            e["frameId"] = "ix-" + e["frameId"]
    L.els.extend(d.els)
    return ["ix-" + i for i in ids], d.files
