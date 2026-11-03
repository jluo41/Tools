"""s06's Design sketch: the design workflow as areas, block by block (JL 261102: "do not use the stair anymore ...
use the area, block by block"). Each act is one outlined area in a row, A to E left to right; its steps stand
inside it top to bottom, a short down arrow between them; one named arrow joins an area to the next.

The words are s06-design-workflow-workflow.yaml. Your four steps wear the one slight colour (excalidraw-studio ⑤);
the loop back is drawn short, inside its area; the open points are red under the row. A function
(x, y) -> (els, y_bottom), as excalidraw-studio's example sketches.
"""
from pathlib import Path

import yaml

import five_parts as fp
from quick_draw import TITLE, arrow, ask, box, text

HERE = Path(__file__).resolve().parent
SIZE, H, STEP_GAP, PAD, AREA_GAP = 20, 62, 58, 26, 110   # words, a step's height, between steps, inside an area, between areas
HEAD, FOOT = 84, 70                                       # an area's title band and its note band
KEY = ("#fff3bf", "#1e1e1e")
ICON = [fp.checklist, lambda e, x, y: fp.i_flow(e, x, y, fp.PU), fp.i_write,       # set up · launch · design
        lambda e, x, y: fp.i_bars(e, x, y, fp.PU), fp.i_lens]                     # release · learn


def width(words):
    return max(200, max(len(ln) for ln in words.split("\n")) * SIZE * 0.6 + 40)


def sketch(x0, y0):
    w = yaml.safe_load((HERE / "s06-design-workflow-workflow.yaml").read_text(encoding="utf-8"))
    acts = w["acts"]
    els = text("wf_h", x0, y0, "How a design travels, area by area", 30, TITLE)
    els += text("wf_c", x0, y0 + 46, w["clocks"], 17, fp.ROOM)
    most = max(len(a["steps"]) for a in acts)
    area_h = HEAD + most * H + (most - 1) * STEP_GAP + FOOT
    top, x = y0 + 120, x0
    prev = None
    for a_i, act in enumerate(acts):
        bw = max(width(s) for s in act["steps"])
        aw = bw + 2 * PAD + (40 if act.get("back") else 0)
        els += box(f"wf_a{a_i}", x, top, aw, area_h, "", "none")           # the area
        els[-1]["strokeWidth"] = 2
        letter, name = act["name"].split(" · ")
        els += text(f"wf_a{a_i}_l", x + aw - 74, top + 6, letter, 84, fp.GHOST)         # a big faint letter, as the parts' numbers
        els += ICON[a_i](f"wf_a{a_i}_i", x + PAD, top + 16)
        els += text(f"wf_a{a_i}_h", x + PAD + 62, top + 20, name, 28, TITLE)
        sx, y = x + PAD, top + HEAD
        cx = sx + bw / 2
        boxes = []
        for s_i, step in enumerate(act["steps"]):
            eid = f"wf_s{a_i}_{s_i}"
            if step in act.get("you", []):
                els += box(eid, sx, y, bw, H, step, "none", SIZE)
                els[-2]["backgroundColor"], els[-2]["fillStyle"], els[-2]["strokeWidth"] = KEY[0], "solid", 3
            else:
                els += box(eid, sx, y, bw, H, step, "plain", SIZE)
            if s_i:
                words = (act.get("arrows") or [""] * 9)[s_i - 1]
                els += arrow(f"{eid}_in", [(cx, y - STEP_GAP + 4), (cx, y - 4)], fp.INK, words,
                             at=(cx + 14 + len(words) * 16 * 0.31, y - STEP_GAP / 2 - 10) if words else None)
            boxes.append(y)
            y += H + STEP_GAP
        if act.get("back"):                                               # the loop back, short, at the area's right
            rx = sx + bw + 22
            els += arrow(f"wf_back{a_i}", [(sx + bw + 4, boxes[-1] + H / 2), (rx, boxes[-1] + H / 2),
                                           (rx, boxes[0] + H / 2), (sx + bw + 4, boxes[0] + H / 2)],
                         fp.PU, act["back"], at=(sx + bw / 2, boxes[-1] + H + 14), dashed=True)
        if act.get("note"):
            els += text(f"wf_n{a_i}", x + PAD, top + area_h - FOOT + 22, act["note"], 17, fp.ROOM)
        if prev is not None:                                              # one named arrow joins it to the area before
            mid = top + area_h / 2
            els += arrow(f"wf_d{a_i}", [(prev + 6, mid), (x - 6, mid)], fp.INK, w["drops"][a_i - 1],
                         at=((prev + x) / 2, mid - 34), width=3)
        prev = x + aw
        x += aw + AREA_GAP
    yy = top + area_h + 40
    for k, words in enumerate(w["open"]):
        els += ask(f"wf_q{k}", x0, yy + k * 60, words)
    return els, yy + 60 * len(w["open"])
