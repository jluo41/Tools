"""Draw an sNN as one flow in five parts (haipipe-studio, JL 261030: "studio: from idea to delivery"): 1 Idea (why we
must make it, then what it hands over), 2 Now (how far it has got), 3 Design (its sketches, each shaping a piece of
its delivery: the only part an sNN draws itself, with excalidraw-job, -task or -story), 4 Process (its Job, its
Tasks, each Run with its status, agent and skill), 5 Delivery (its delivery/,
then the render out). Everything but Design is read from disk: the face, the Job, delivery/render.yaml. The shape is
excalidraw-studio's (JL 261031, b35 r01 Q1; b35-s01-D16).

    import five_parts as fp
    fp.build(topic, spec, design)        # writes <topic>/<topic>.excalidraw and its card preview <topic>.png

spec: title, sub; why = {question, notes: [3 sticky lines], quote}; what = {head, icon, name, type, parts:
[(icon, name, why, done)], deck_why}; job (a Job folder or None); started (a note, optional); target (where the
render writes, a few words); missing (delivery rows not written yet: [(name, what)]); tasks (optional: the
Job's Task folders Process shows, when the Job holds more than this sNN uses).
design(): the sNN's own sketches, drawn at local size from x 690, y 280; it returns the elements.
"""
import importlib.util
import math
import re
import subprocess
import sys
import textwrap
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from quick_draw import SEM, TITLE, BODY, _el, arrow, heading, line, text, write  # noqa: E402,F401

OR, GR, PU, YE, RE = SEM["start"][1], SEM["end"][1], SEM["agent"][1], SEM["decision"][1], SEM["warn"][1]
INK, ROOM, GHOST, NAVY = "#374151", "#adb5bd", "#f1f3f5", "#1e3a5f"
STICKY = ("#fff3bf", "#e8b500")
RED = (SEM["warn"][0], RE)


def poly(eid, pts, stroke, fill, width=2):
    """A closed, filled shape from points."""
    els = line(eid, pts + [pts[0]], stroke, width)
    els[0].update(backgroundColor=fill, fillStyle="solid", polygon=True, roundness=None)
    return els


def sticky(eid, cx, cy, w, h, words, size=17, angle=0.0, colors=STICKY, color=INK):
    """A sticky note, tilted a little, its words tilted with it."""
    fill, stroke = colors
    els = [_el("rectangle", eid, cx - w / 2, cy - h / 2, w, h, stroke, fill, angle=angle, roundness={"type": 3})]
    t = text(eid + "_t", cx, cy - (words.count("\n") + 1) * size * 0.62, words, size, color, "center")
    t[0]["angle"] = angle
    return els + t


def bubble(eid, x, y, w, h, words, size=26):
    """A speech bubble: the question somebody asks."""
    fill, stroke = SEM["start"]
    els = [_el("ellipse", eid, x, y, w, h, stroke, fill)]
    els += poly(eid + "_tail", [(x + w * 0.22, y + h * 0.84), (x + w * 0.12, y + h + 46), (x + w * 0.38, y + h * 0.93)], stroke, fill)
    return els + text(eid + "_t", x + w / 2, y + h / 2 - size * 1.25, words, size, INK, "center")


def bulb(eid, cx, cy, r=34):
    """An idea: a lit bulb with rays."""
    els = [_el("ellipse", eid, cx - r, cy - r, 2 * r, 2 * r, YE, "#ffe066", strokeWidth=2)]
    els += [_el("rectangle", eid + "_base", cx - r * 0.42, cy + r * 0.86, r * 0.84, r * 0.5, INK, "#ced4da")]
    for k, a in enumerate((-2.4, -1.57, -0.74)):
        x0, y0 = cx + math.cos(a) * (r + 8), cy + math.sin(a) * (r + 8)
        els += line(f"{eid}_ray{k}", [(x0, y0), (cx + math.cos(a) * (r + 22), cy + math.sin(a) * (r + 22))], YE, 2)
    return els


def gift(eid, x, y, w=96, h=74):
    """A delivery: a wrapped box with a ribbon and a bow."""
    fill, stroke = SEM["end"]
    els = [_el("rectangle", eid, x, y, w, h, stroke, fill)]
    els += [_el("rectangle", eid + "_lid", x - 6, y - 16, w + 12, 18, stroke, fill)]
    els += line(eid + "_rv", [(x + w / 2, y - 16), (x + w / 2, y + h)], RE, 3)
    els += [_el("ellipse", eid + "_b1", x + w / 2 - 26, y - 34, 26, 18, RE, "#ffc9c9"),
            _el("ellipse", eid + "_b2", x + w / 2, y - 34, 26, 18, RE, "#ffc9c9")]
    return els


def slides(eid, x, y, w=120, h=78, angle=0.0):
    """A deck: three slides stacked, offset."""
    fill, stroke = SEM["start"]
    els = []
    for k in (2, 1, 0):
        els += [_el("rectangle", f"{eid}_{k}", x + k * 10, y - k * 10, w, h, stroke, "#fff4e6" if k else fill, angle=angle)]
    els += line(eid + "_l1", [(x + 14, y + 22), (x + w - 30, y + 22)], stroke, 2)
    els += line(eid + "_l2", [(x + 14, y + 40), (x + w - 50, y + 40)], stroke, 1)
    return els


def doc(eid, x, y, w, h, title, note, angle=0.0):
    """A document with a folded corner."""
    fill, stroke = SEM["end"]
    f = 26
    els = poly(eid, [(x, y), (x + w - f, y), (x + w, y + f), (x + w, y + h), (x, y + h)], stroke, fill)
    els += poly(eid + "_fold", [(x + w - f, y), (x + w - f, y + f), (x + w, y + f)], stroke, "#d3f9d8")
    for e in els:
        e["angle"] = angle
    return els + text(eid + "_h", x + 16, y + 14, title, 18, GR) + text(eid + "_n", x + 16, y + 42, note, 15, INK)


def stamp(eid, cx, cy, words="agreed?"):
    """A rubber stamp: a person says yes."""
    els = [_el("ellipse", eid, cx - 62, cy - 62, 124, 124, RE, "transparent", strokeWidth=3),
           _el("ellipse", eid + "_in", cx - 50, cy - 50, 100, 100, RE, "transparent", strokeWidth=1)]
    t = text(eid + "_t", cx, cy - 13, words, 21, RE, "center")
    t[0]["angle"] = -0.3
    return els + t


def gear(eid, cx, cy, r=38):
    """Process: a gear, eight teeth."""
    fill = SEM["agent"][0]
    els = []
    for k in range(8):
        a = k * math.pi / 4
        tx, ty = cx + math.cos(a) * r * 0.98, cy + math.sin(a) * r * 0.98
        els += [_el("rectangle", f"{eid}_tooth{k}", tx - r * 0.2, ty - r * 0.22, r * 0.4, r * 0.44, PU, fill, angle=a + math.pi / 2)]
    els += [_el("ellipse", eid, cx - r, cy - r, 2 * r, 2 * r, PU, fill, strokeWidth=2)]
    return els + [_el("ellipse", eid + "_hub", cx - r * 0.38, cy - r * 0.38, r * 0.76, r * 0.76, PU, "#ffffff")]


def checklist(eid, x, y):
    els = [_el("rectangle", eid, x, y, 26, 32, PU, "#ffffff")]
    for k in range(3):
        els += line(f"{eid}_l{k}", [(x + 6, y + 9 + k * 8), (x + 20, y + 9 + k * 8)], PU, 1)
    return els


def play(eid, x, y):
    return poly(eid, [(x, y), (x + 24, y + 14), (x, y + 28)], PU, "#ffffff")


def tick(eid, x, y):
    return line(eid, [(x, y + 12), (x + 9, y + 22), (x + 26, y)], GR, 3)


def part(k, x, y, icon, name, sub, color, gap=90):
    """A part of the flow: a faint giant number behind, a big icon, its name and what it answers."""
    els = text(f"num{k}", x - 150, y - 190, str(k), 260, "#e9ecef")
    els += icon
    return els + text(f"part{k}", x + gap, y - 26, name, 46, color) + text(f"part{k}_sub", x + gap + 2, y + 30, sub, 20, BODY)


def room(k, x, y):
    return text(f"room{k}", x, y, "your room: write, draw, mark here", 16, ROOM)


def i_book(eid, x, y):
    f = "#fff4e6"
    return (poly(eid, [(x, y + 4), (x + 22, y), (x + 22, y + 30), (x, y + 34)], OR, f)
            + poly(eid + "_r", [(x + 22, y), (x + 44, y + 4), (x + 44, y + 34), (x + 22, y + 30)], OR, f))


def i_lens(eid, x, y):
    return [_el("ellipse", eid, x, y, 28, 28, NAVY, SEM["plain"][0], strokeWidth=2)] + line(eid + "_h", [(x + 24, y + 24), (x + 40, y + 38)], NAVY, 4)


def i_page(eid, x, y, c=GR, f=None):
    els = [_el("rectangle", eid, x, y, 46, 34, c, f or SEM["end"][0])] + line(eid + "_bar", [(x, y + 9), (x + 46, y + 9)], c, 1)
    return els + [_el("ellipse", f"{eid}_d{k}", x + 4 + k * 6, y + 3, 4, 4, c, c) for k in range(3)]


def i_grid(eid, x, y, c=GR):
    els = [_el("rectangle", eid, x, y, 44, 34, c, SEM["end"][0] if c == GR else SEM["plain"][0])]
    els += line(eid + "_h1", [(x, y + 11), (x + 44, y + 11)], c, 1) + line(eid + "_h2", [(x, y + 22), (x + 44, y + 22)], c, 1)
    return els + line(eid + "_v1", [(x + 15, y), (x + 15, y + 34)], c, 1) + line(eid + "_v2", [(x + 30, y), (x + 30, y + 34)], c, 1)


def i_bars(eid, x, y, c=GR):
    return [_el("rectangle", f"{eid}_{k}", x + k * 15, y + 34 - hh, 11, hh, c, SEM["end"][0] if c == GR else "#ffe066")
            for k, hh in enumerate((14, 26, 34))]


def i_flow(eid, x, y, c=PU):
    els = [_el("rectangle", f"{eid}_{k}", x + k * 16, y + k * 11, 14, 11, c, SEM["agent"][0]) for k in range(3)]
    return els + line(eid + "_l", [(x + 7, y + 11), (x + 23, y + 11), (x + 39, y + 22)], c, 1)


def i_code(eid, x, y, c=GR):
    return [_el("rectangle", eid, x, y, 46, 32, c, SEM["end"][0])] + text(eid + "_glyph", x + 23, y + 7, "</>", 15, c, "center")


def i_mail(eid, x, y, c=GR):
    return [_el("rectangle", eid, x, y, 46, 30, c, SEM["end"][0])] + line(eid + "_v", [(x, y), (x + 23, y + 16), (x + 46, y)], c, 1)


def i_doc(eid, x, y, c=GR):
    return poly(eid, [(x, y), (x + 30, y), (x + 40, y + 10), (x + 40, y + 40), (x, y + 40)], c, SEM["end"][0])


def i_write(eid, x, y, c=NAVY):
    """A Section being written: a page with lines and a pencil."""
    els = [_el("rectangle", eid, x, y, 34, 40, NAVY, "#ffffff")]
    for k in range(4):
        els += line(f"{eid}_l{k}", [(x + 6, y + 9 + k * 7), (x + 26 - (k == 3) * 10, y + 9 + k * 7)], NAVY, 1)
    return els + poly(eid + "_pen", [(x + 30, y + 40), (x + 48, y + 14), (x + 54, y + 18), (x + 36, y + 44)], OR, "#ffe066")


def i_papers(eid, x, y, c=NAVY):
    """A full paper: pages stacked, a title bar on the top one."""
    els = []
    for k in (2, 1, 0):
        els += [_el("rectangle", f"{eid}_{k}", x + k * 5, y + 8 - k * 4, 32, 38, c, "#ffffff" if k else SEM["plain"][0])]
    return els + line(eid + "_bar", [(x + 5, y + 16), (x + 27, y + 16)], c, 3)


def i_slides(eid, x, y):
    return [_el("rectangle", f"{eid}_{k}", x + k * 5, y - k * 5, 40, 28, OR, "#fff4e6" if k else SEM["start"][0]) for k in (2, 1, 0)]


def shapes(eid, x, y, words):
    """The green line under a sketch's title: the delivery piece it shapes."""
    return text(eid, x, y, "shapes \u25b8 " + words, 14, GR)


def data_table(eid, x, y, title, cols, widths, rows, color, fill, note="", rh=22):
    """One step of a data topic's Design: a small table, its name, its real column names and two or three made-up
    rows (JL 261031: "the workflow, how the data is constructed, what is the physical data"); returns (els, bottom)."""
    els = text(eid + "_h", x, y, title, 15, color)
    if note:
        els += text(eid + "_hn", x + 9 * len(title) + 14, y + 2, note, 12, BODY)
    top, w = y + 24, sum(widths)
    els += [_el("rectangle", eid + "_hd", x, top, w, rh, color, fill)]
    els += [_el("rectangle", eid + "_bd", x, top + rh, w, rh * len(rows), color, "#ffffff")]
    cx = x
    for j, (c, cw) in enumerate(zip(cols, widths)):
        els += text(f"{eid}_c{j}", cx + 6, top + 4, c, 12, color)
        if j:
            els += line(f"{eid}_v{j}", [(cx, top), (cx, top + rh * (len(rows) + 1))], ROOM, 1)
        for i, r in enumerate(rows):
            els += text(f"{eid}_r{i}_{j}", cx + 6, top + rh * (i + 1) + 4, str(r[j]), 12, INK)
        cx += cw
    return els, top + rh * (len(rows) + 1)


def data_step(eid, pts, words, color=OR, dx=12, dy=-6):
    """The arrow from one data_table to the next, and what the step does, beside it ("a gap of 4-52 weeks").
    Its ids: eid, and eid + "_t" for the words when there are any (data_table uses eid + _h, _hn, _hd, _bd, _cJ, _vJ,
    _rI_J), so give each table and step its own eid."""
    (x0, y0), (x1, y1) = pts[0], pts[-1]
    els = arrow(eid, pts, color, width=2)
    return els + (text(eid + "_t", (x0 + x1) / 2 + dx, (y0 + y1) / 2 + dy, words, 13, color) if words else [])


def tree(prefix, x, y, rows, step=32, note=300):
    """A folder tree drawn with lines: (depth, name, what it is, colour) per row."""
    out = []
    for k, (depth, name, words, color) in enumerate(rows):
        ry, lx = y + k * step, x + depth * 26
        if depth:
            out += line(f"{prefix}{k}_l", [(lx - 18, ry - 16), (lx - 18, ry + 9), (lx - 5, ry + 9)], ROOM, 1)
        out += text(f"{prefix}{k}", lx, ry, name, 15, color)
        if words:
            out += text(f"{prefix}{k}_n", x + note, ry + 1, words, 13, BODY)
    return out


def box_check(eid, x, y, done):
    els = [_el("rectangle", eid, x, y, 30, 30, GR if done else ROOM, "#ffffff", strokeWidth=2)]
    return els + (tick(eid + "_v", x + 3, y + 4) if done else [])


TEAL = "#0b7285"
STAGES = ["explore", "shaping", "agreed", "closed"]
ICONS = {"deck": lambda eid, x, y: i_slides(eid, x, y), "doc": lambda eid, x, y: i_doc(eid, x, y),
         "code": lambda eid, x, y: i_code(eid, x, y), "book": lambda eid, x, y: i_book(eid, x, y),
         "page": lambda eid, x, y: i_page(eid, x, y)}
_rd_spec = importlib.util.spec_from_file_location("render_delivery", Path(__file__).with_name("render_delivery.py"))
render_delivery = importlib.util.module_from_spec(_rd_spec)
_rd_spec.loader.exec_module(render_delivery)


def idea(topic, spec):
    """1 Idea: ① why we must make this sNN, ② what it hands over (JL 261030: "why we must create this studio, and the
    second one will be what this studio will deliver"), no boxes."""
    nn, why, what = topic.name.split("-")[0], spec["why"], spec["what"]
    els = part(1, 0, 190, bulb("icon1", 40, 190, 36), "Idea", "why we do it", OR)
    els += text("why_h", 0, 262, f"\u2460 why we must make {nn}", 18, OR)
    els += bubble("ask", 0, 300, 440, 150, why["question"])
    for k, (cx, cy, w, a) in enumerate(((95, 575, 190, -0.06), (290, 585, 180, 0.05), (480, 575, 190, -0.03))):
        if k < len(why["notes"]):
            els += sticky(f"why{k + 1}", cx, cy, w, 92, why["notes"][k], 15, a)
    els += text("why_q", 0, 640, why["quote"], 13, BODY)
    fill = SEM["end"][0]
    ROW = 58
    els += gift("hands_gift", 16, 732, 44, 34) + text("hands_h", 72, 736, what["head"], 19, GR)
    els += ICONS[what.get("icon", "book")]("hands_skill", 22, 790) + text("hands_skill_t", 84, 790, what["name"], 21, TITLE)
    tx = 84 + len(what["name"]) * 21 * 0.62 + 18
    els += [_el("rectangle", "hands_type", tx, 790, len(what["type"]) * 15 * 0.62 + 26, 26, GR, fill, roundness={"type": 3})]
    els += text("hands_type_t", tx + 14, 793, what["type"], 15, GR)
    for k, (icon, pname, why_, _) in enumerate(what["parts"]):
        y = 850 + ROW * k
        els += line(f"hands_l{k}", [(44, y - 30), (44, y + 14), (70, y + 14)], ROOM, 1)
        els += ICONS[icon](f"hands_i{k}", 78, y)
        els += text(f"hands_{k}", 136, y - 2, pname, 16, TITLE) + text(f"hands_{k}_why", 136, y + 20, why_, 13, BODY)
    y = 850 + ROW * len(what["parts"])          # the deck is the sNN's, not the thing's: it stays in delivery/deck/
    els += i_slides("hands_deck", 22, y) + text("hands_deck_t", 84, y - 2, "+ its deck", 16, TITLE)
    els += text("hands_deck_why", 84, y + 20, what["deck_why"], 13, BODY)
    y1 = y + ROW + 30
    els += text("quote_mark", 0, y1 - 22, "\u201c", 70, "#ffd8a8")
    els += text("quote", 46, y1, "studio: from idea to delivery\none studio, one idea and one\ndelivery   JL 261030", 15, BODY)
    if spec.get("started"):
        els += poly("folder_tab", [(300, y1 - 13), (360, y1 - 13), (370, y1), (300, y1)], PU, SEM["agent"][0])
        els += [_el("rectangle", "folder", 300, y1, 200, 86, PU, SEM["agent"][0])]
        els += text("folder_t", 312, y1 + 12, spec["started"], 14, PU)
    return els + room(1, 0, y1 + 200)


def now(topic, spec):
    """2 Now, read from the face on every rebuild (JL 261030: "here is basically no information?"; before: "too many
    words"): the stage, the thing part by part, each decision as its short phrase, the first open questions."""
    face = (topic / f"{topic.name}.md").read_text(encoding="utf-8")
    nn = topic.name.split("-")[0]
    els = arrow("go1n", [(445, 380), (560, 300), (640, 300)], TEAL, width=3)
    pin = [_el("ellipse", "icon2", 664, 158, 30, 30, TEAL, "#c5f6fa", strokeWidth=2)]
    pin += poly("icon2_tip", [(666, 180), (692, 180), (679, 210)], TEAL, "#c5f6fa")
    els += part(2, 660, 190, pin, "Now", "how far this sNN has got", TEAL, 60)
    stage = (re.search(r"(?m)^\*\*Stage:\*\*\s*`?(\w+)", face) or [None, "explore"])[1]
    els += line("now_stage_line", [(680, 300), (1220, 300)], TEAL, 2)
    for k, st in enumerate(STAGES):
        cx, here = 700 + k * 170, st == stage
        els += [_el("ellipse", f"now_st{k}", cx - (12 if here else 7), 300 - (12 if here else 7), 24 if here else 14,
                    24 if here else 14, OR if here else ROOM, SEM["start"][0] if here else "#ffffff", strokeWidth=2)]
        els += text(f"now_st{k}_t", cx, 318, st, 16 if here else 13, OR if here else ROOM, "center")
    decided = re.findall(rf"(?m)^({nn}-D\d+) · (.+)$", face)
    section = face.split("\nOpen\n----", 1)[1] if "\nOpen\n----" in face else ""
    section = re.split(r"(?m)^(?:#.*|.+\n[-=]{3,})$", section, maxsplit=1)[0]   # the Open section only, to its next heading
    open_ = re.findall(r"(?m)^(\d+)\. (.+)$", section)
    plain = lambda x: re.sub(r"[`*]", "", re.sub(r"\s*\(JL [^)]*\)\.?", "", x))
    short = lambda x, n: textwrap.shorten(re.split(r":|;| \(|\. ", plain(x), maxsplit=1)[0], n, placeholder="\u2026")
    y = 360
    els += text("now_parts_h", 680, y, f"the {spec['what']['type']}, part by part", 16, TEAL)
    for k, (_, pname, _, done) in enumerate(spec["what"]["parts"]):
        els += text(f"now_part{k}", 686, y + 28 + 24 * k, ("\u2705 " if done else "\u2b1c ") + pname, 14, INK)
    y += 28 + 24 * len(spec["what"]["parts"]) + 22
    els += text("now_dec_h", 680, y, "decided", 16, GR)
    for k, (_, words) in enumerate(decided):
        gone = "Replaced by" in words                   # a replaced decision stays, greyed, so the history reads
        els += [] if gone else tick(f"now_dec{k}", 682, y + 26 + 23 * k)
        els += text(f"now_dec{k}_t", 714, y + 28 + 23 * k, short(words, 44) + (" (replaced)" if gone else ""), 13,
                    ROOM if gone else INK)
    y += 26 + 23 * len(decided) + 22
    els += text("now_open_h", 680, y, "still open", 16, RE)
    for k, (_, words) in enumerate(open_[:3]):
        els += [_el("rectangle", f"now_open{k}", 684, y + 30 + 26 * k, 18, 18, RE, "#ffffff")]
        els += text(f"now_open{k}_t", 714, y + 28 + 26 * k, textwrap.shorten(plain(words), 56, placeholder="\u2026"), 13,
                    OR if k == 0 else INK)
    if len(open_) > 3:
        els += text("now_open_more", 714, y + 28 + 26 * 3, f"and {len(open_) - 3} more on the face", 13, ROOM)
    y += 30 + 26 * 4 + 20
    els += text("now_note", 660, y, "read from disk \u00b7 redrawn every time", 13, ROOM)
    return els + room(2, 660, y + 60)


MOVE, GROW, OX, OY = 710, 1.25, 1400, 190      # Design, the biggest part, moved right past Now, then grown


def grow(e):
    e["x"] += MOVE
    if e["id"].startswith(("num3", "part3", "icon3")):          # the part's name and number keep their size
        return
    e["x"], e["y"] = OX + (e["x"] - OX) * GROW, OY + (e["y"] - OY) * GROW
    e["width"], e["height"] = e["width"] * GROW, e["height"] * GROW
    if "fontSize" in e:
        e["fontSize"] = round(e["fontSize"] * GROW)
    if "points" in e:
        e["points"] = [[px * GROW, py * GROW] for px, py in e["points"]]


def design_part(sketches):
    els = arrow("gond", [(1240, 560), (1320, 520), (1390, 560)], TITLE, width=3)
    d0 = len(els)
    pencil = poly("icon3", [(690, 160), (722, 160), (722, 214), (706, 236), (690, 214)], TITLE, "#d0ebff")
    pencil += poly("icon3_tip", [(690, 214), (722, 214), (706, 236)], TITLE, "#ffe066")
    els += part(3, 690, 190, pencil, "Design", "proposals for the idea; changed a lot along the way", TITLE, 60)
    els += sketches
    for e in els[d0:]:
        grow(e)
    return els + room(3, 1400, max(2250, max(e["y"] + e["height"] for e in els[d0:]) + 80))


def process(topic, spec):
    """4 Process: the sNN's Job, its Tasks and Runs, each ticked from disk; no Job yet says so."""
    job = spec.get("job")
    els = arrow("go23", [(2020, 600), (2110, 560), (2170, 620)], PU, width=3)
    els += part(4, 2210, 250, gear("icon4", 2250, 250), "Process", "how: one Job, its Tasks, their Runs", PU, 110)
    if not job or not Path(job).is_dir():
        els += text("job_none", 2210, 360, "no Job yet: the work that makes this delivery\nstarts once its Design is agreed", 18, INK)
        return els + room(4, 2210, 520)
    job = Path(job)
    els += [_el("rectangle", "job", 2210, 340, 640, 84, PU, SEM["agent"][0], roundness={"type": 3})]
    els += poly("job_tab", [(2228, 352), (2268, 352), (2276, 362), (2228, 362)], PU, "#ffffff")
    els += [_el("rectangle", "job_folder", 2228, 362, 52, 38, PU, "#ffffff")]
    blk = job.parent.name
    els += text("job_t", 2298, 350, job.name, 22, PU) + text("job_n", 2298, 384, f"Job: make {topic.name.split('-')[0]}'s delivery \u00b7 {blk.split('_')[0]}/{job.name}/", 16, INK)
    tasks = []
    keep = spec.get("tasks")                               # only the Tasks this sNN uses, when its Job holds others too
    for t in sorted(job.glob("t[0-9]*_*")):                # (JL 261102, a 68-Task Job: "this is too much, and not readable")
        if keep and t.name not in keep:
            continue
        face = (t / f"{t.name}.md").read_text()
        runs = []                                          # each Run: its status, agent and skill from its card (JL 261031,
        for c in sorted(t.glob("runs/*/run.yaml")):        # b35 r01 Q3: "Yes, we should do it")
            card = yaml.safe_load(c.read_text()) or {}
            words = " \u00b7 ".join(str(w) for w in (card.get("status"), card.get("agent") or card.get("by"),
                                                      card.get("skill")) if w)
            runs.append((c.parent.name.removeprefix("run-"), card.get("status") == "done", words))
        goal = re.search(r"(?m)^goal:\s*(.+)$", face)
        tasks.append((t.name, textwrap.shorten(goal.group(1) if goal else "", 58, placeholder="\u2026"), runs,
                      "CLOSED" in face.split("\n", 3)[1]))
    y, last = 450, 450
    for i, (tn, what, runs, closed) in enumerate(tasks):
        rows = max(1, len(runs))                           # one Run a row: its name, then status · agent · skill
        done = closed and all(d for _, d, _ in runs)
        last = y
        els += line(f"twig{i}", [(2250, y + 24), (2290, y + 24)], PU, 2)
        els += box_check(f"tc{i}", 2296, y + 9, done)
        els += [_el("rectangle", f"task{i}", 2340, y, 540, 96 + 34 * (rows - 1), PU, "#f3f0ff", roundness={"type": 3})]
        els += checklist(f"task{i}_icon", 2352, y + 10)
        els += text(f"task{i}_n", 2392, y + 8, tn, 18, PU) + text(f"task{i}_w", 2392, y + 36, what, 15, INK)
        for k, (rn, rd, words) in enumerate(runs):
            rx, ry = 2392, y + 64 + 34 * k
            name = rn if len(rn) <= 24 else rn[:23] + "\u2026"   # a Run name has no spaces: shorten() left only "\u2026" (261031)
            els += play(f"run{i}_{k}", rx, ry) + text(f"run{i}_{k}_t", rx + 32, ry + 2, name, 14, PU)
            if words:
                els += text(f"run{i}_{k}_w", rx + 230, ry + 2, textwrap.shorten(words, 30, placeholder="\u2026"), 13, INK)
            els += box_check(f"rc{i}_{k}", rx + 450, ry - 4, rd)
            els[-1 if not rd else -2]["width"] = els[-1 if not rd else -2]["height"] = 26
        y += 130 + 34 * (rows - 1)
    els += line("trunk", [(2250, 424), (2250, last + 34)], PU, 2)
    y += 20
    els += text("proc_note", 2210, max(1120, y), f"read from {job.name.split('_')[0]}'s Task faces and Run cards \u00b7 redrawn every time", 15, BODY)
    return els + room(4, 2210, max(1180, y + 60))


def delivery(topic, spec):
    """5 Delivery, two halves (JL 261030: "studio/sNN/delivery, this is the delivery, and then we do the render"): what
    sits in the sNN's delivery/, then where the render writes it; each mark read from disk, no links."""
    DX = 3110
    els = arrow("go34", [(2900, 760), (2980, 740), (DX - 20, 800)], GR, width=3)
    els += stamp("agreed", 2990, 620)
    els += part(5, DX, 300, gift("icon5", DX - 5, 285, 76, 58), "Delivery", "what this sNN hands over", GR)
    rendered = render_delivery.render(topic)
    ink = {"\u2705": GR, "\u2b1c": RE}
    els += text("dl_in_h", DX, 380, f"in {topic.name}/delivery/", 17, GR)
    deck = any(p for p in (topic / "delivery" / "deck").glob("*") if not p.name.startswith("."))   # a .gitkeep is no deck
    rows = [("deck", "deck/", "its slides \u00b7 they stay here", "\u2705" if deck else "\u2b1c")]
    rows += [(f"p{k}", pc["from"], f"a {Path(pc['to']).name} {'section' if pc['to'].endswith('.md') else 'piece'}" if "to" in pc else f"for {pc.get('rendered_by', 'its Theme')}",
              "\u2705" if st != "no source" else "\u2b1c") for k, (pc, st, _) in enumerate(rendered) if "from" in pc]
    rows += [(f"h{k}", name, what, "\u2705") for k, (name, what) in enumerate(spec.get("have", []))]   # done, not a render piece
    rows += [(f"m{k}", name, what, "\u2b1c") for k, (name, what) in enumerate(spec.get("missing", []))]
    y = 420
    for rid, name, what, mark in rows:
        els += text(f"dl_{rid}_m", DX, y, mark, 20, ink[mark])
        els += text(f"dl_{rid}_h", DX + 36, y, name, 16, TITLE) + text(f"dl_{rid}_x", DX + 36, y + 22, what, 12, BODY)
        y += 52
    els += i_slides("dl_deck_icon", DX + 470, 418)
    yr = y + 30
    els += arrow("dl_render", [(DX + 40, yr), (DX + 40, yr + 60), (DX + 120, yr + 60)], GR, width=3)
    els += text("dl_render_t", DX + 56, yr + 8, "render  (render_delivery.py)", 15, GR)
    els += i_book("dl_skill_icon", DX + 130, yr + 44) + text("dl_target", DX + 186, yr + 46, spec["target"], 18, TITLE)
    y2 = yr + 100
    for k, (pc, st, _) in enumerate(rendered):
        name = pc.get("block") or (pc["code"].split()[0] if "code" in pc else pc.get("from"))
        built = st == "code" and _closed(topic, pc.get("by", ""))
        mark = "\u2705" if st in ("same", "rendered") or built else "\u2b1c"
        by = pc.get("by", "")
        bits = by.split("/")                                      # j02_x/t01_y[/runs/run-z] -> j02 t01
        tag = f"  (built by {bits[0].split('_')[0]} {next((b.split('_')[0] for b in bits[1:] if re.match(r't\d+_', b)), '')})" if st == "code" else ""
        els += text(f"dl_t{k}", DX + 186, y2 + 26 * k, f"{mark} {textwrap.shorten(name, 40, placeholder='\u2026')}{tag}", 14, INK)
    y = y2 + 26 * len(rendered) + 10
    return els + room(5, DX, max(1180, y + 160))


def _closed(topic, by):
    """A code piece is built when what builds it is done: a Run whose card says done, or a Task whose face says CLOSED."""
    t = topic.parent / by
    if (t / "run.yaml").is_file():
        return (yaml.safe_load((t / "run.yaml").read_text()) or {}).get("status") == "done"
    face = t / f"{t.name}.md"
    return face.is_file() and "CLOSED" in face.read_text().split("\n", 3)[1]


def build(topic: Path, spec: dict, design, shift: int = 1050) -> Path:
    topic = Path(topic)
    out = topic / f"{topic.name}.excalidraw"
    els = heading(spec["title"], spec.get("sub", "from idea to delivery, in five parts"))
    els += idea(topic, spec) + now(topic, spec) + design_part(design()) + process(topic, spec) + delivery(topic, spec)
    p0 = [i for i, e in enumerate(els) if e["id"] == "go23"][0]
    for e in els[p0:]:                                       # Process and Delivery move right, past the bigger Design
        e["x"] += shift
    ids = [e["id"] for e in els]
    assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1][:5]
    print(write(out, els))
    card(out)
    return out


def headings(md: Path) -> list:
    """A Markdown file's section titles in order (## or underlined), past its front matter and outside code fences."""
    lines = md.read_text(encoding="utf-8").split("\n")
    start = next(i for i in range(1, len(lines)) if lines[i] == "---") + 1 if lines and lines[0] == "---" else 0
    out, fence = [], False
    for i in range(start, len(lines)):
        ln = lines[i]
        if ln.startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        if ln.startswith("## "):
            out.append(ln[3:].strip())
        elif i + 1 < len(lines) and re.fullmatch(r"-{3,}", lines[i + 1]) and ln.strip() and not ln.startswith(("|", "<!--")):
            out.append(ln.strip())
    return out


def listing(prefix, x, y, title, rows, green=lambda r: False, size=13, step=22):
    """A file and its parts in order, one a line; the ones this sNN makes in green."""
    els = text(prefix, x, y, title, 15, INK)
    for k, r in enumerate(rows):
        els += text(f"{prefix}{k}", x + 20, y + 28 + step * k, textwrap.shorten(r, 46, placeholder="…"), size,
                    GR if green(r) else BODY)
    return els


def card(drawing: Path) -> Path:
    """Its card preview, <topic>.png: the drawing's start (title, Idea, Now), since the whole canvas is unreadable at
    card size. Rendered from only the elements in a fixed region, 1350 x 820 of the canvas, so a wide Design (an old
    drawing kept whole) neither shifts nor shrinks what the card shows (JL 261030)."""
    import json
    import tempfile
    from PIL import Image
    doc = json.loads(Path(drawing).read_text(encoding="utf-8"))
    els = [e for e in doc.get("elements", []) if not e.get("isDeleted")]
    x0, y0 = min(e["x"] for e in els), min(e["y"] for e in els)
    near = [e for e in els if e["x"] < x0 + 1350 and e["y"] < y0 + 820]
    png = Path(drawing).with_suffix(".png")
    with tempfile.TemporaryDirectory() as tmp:
        part = Path(tmp) / "card.excalidraw"
        part.write_text(json.dumps(dict(doc, elements=near, files=doc.get("files") or {})), encoding="utf-8")
        subprocess.run(["uv", "run", "--no-project", "-q", "--with", "pillow", "python", str(Path(__file__).with_name("render_png.py")),
                        str(part), str(png), "0.6"], check=True, stdout=subprocess.DEVNULL)
    im = Image.open(png)
    x1, y1 = max(e["x"] + e["width"] for e in near), max(e["y"] + e["height"] for e in near)
    im.crop((0, 0, min(im.width, int(im.width * 1350 / (x1 - x0))), min(im.height, int(im.height * 820 / (y1 - y0))))).save(png)
    return png


def kept_first(topic: Path, top: float, name="first-drawing.excalidraw", label=None) -> list:
    """The sNN's first drawing, kept whole below the Design (JL 261030: "We should keep them"): its elements from
    result/<name>, moved down to `top`, ids prefixed kept_."""
    src = topic / "result" / name
    if not src.is_file():
        return []
    import json
    old = [e for e in json.loads(src.read_text(encoding="utf-8"))["elements"] if not e.get("isDeleted")]
    if not old:
        return []
    x0, y0 = min(e["x"] for e in old), min(e["y"] for e in old)
    for e in old:
        e["id"], e["x"], e["y"] = "kept_" + e["id"], e["x"] - x0 + 690, e["y"] - y0 + top + 70
        for k in ("containerId",):
            if e.get(k):
                e[k] = "kept_" + e[k]
        if e.get("boundElements"):
            e["boundElements"] = [dict(b, id="kept_" + b["id"]) for b in e["boundElements"]]
        for k in ("startBinding", "endBinding"):
            if e.get(k):
                e[k] = dict(e[k], elementId="kept_" + e[k]["elementId"])
    head = text("kept_h", 690, top, label or f"kept: {topic.name.split('-')[0]}'s first drawing, as it was", 20, TITLE)
    return head + line("kept_rule", [(690, top + 40), (2300, top + 40)], ROOM, 1, True) + old
