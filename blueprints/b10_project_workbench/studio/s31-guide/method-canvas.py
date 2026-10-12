#!/usr/bin/env python3
"""Draw a family's methods canvas from its method file (JL 261003: "create a method canvas as
they do", "I want a new excalidraw for it"; then "make it from up to down, and each space to
be a large frame, and compare it with the aris and nature-paper-skills").

    python method-canvas.py <server>/guide/method.md <server>/guide/methods.excalidraw [--force]

(Before 261007 the files were a skill's `ref/<family>-method.md` and `<family>-methods.excalidraw`;
both names still work.)

The canvas reads top to bottom, one large frame per Space of the workbench, in step order.
Inside a frame each step is one row, left to right: the step (what happens, who signs), our
methods, the tests at that step, and its runs with their agent and skill (from the family's
Workbench Table: `workbench-table.md` beside the method file, else the `table:` its
`guide.yaml` names). Outside the frames, on the right, each compared
skill set's skills and the coverage, with an arrow back to the step.

It reads three kinds of table from the method file:
  `step | what happens | methods | where in the workbench | who signs`   the steps; a step's
        Space is the first words of its "where" cell, before "›", and its runs the names
        after "· runs", each a Run type of the Workbench Table
  `test | asks | when | source`        the tests; "when" names the step numbers ("step 3")
  `step | our methods | <set> … | coverage`   optional: our methods per step beside other
        skill sets, and the coverage; the coverage colours its box (Both green, Ours only
        blue, Gap orange)

This writes the first version only. After that the canvas is the source: the person edits it
in Guide › Method and the edits save back. An existing canvas is replaced only with --force,
when the person asks.
"""
import argparse
import json
import random
import re
import sys
import textwrap
from pathlib import Path

INK, MUTED = "#1e1e1e", "#495057"
SPACE_COLORS = ("#1971c2", "#2f9e44", "#9c36b5", "#e8590c", "#0c8599")   # one per Space, in order
BOTH, OURS, GAP = "#2f9e44", "#1971c2", "#e8590c"
FONT = 8                                                                 # Comic Shanns, the Studio's hand
rng = random.Random(261003)


def tables(text):
    """Every pipe table: (lower-case header words, body rows)."""
    out, block = [], []
    for line in text.splitlines() + [""]:
        if line.startswith("|"):
            block.append([c.strip() for c in line.strip().strip("|").split("|")])
        elif block:
            body = [r for r in block[1:] if not all(re.fullmatch(r":?-{2,}:?", c) for c in r if c)]
            out.append(([c.lower() for c in block[0]], body, block[0]))
            block = []
    return out


def workbench_table(doc):
    """The Workbench Table beside the method file, else the one its guide.yaml names
    (`table: skill:<name>/<rest>`, a skill folder anywhere under the toolkit's skills/)."""
    beside = doc.parent / "workbench-table.md"
    if beside.is_file() or not (doc.parent / "guide.yaml").is_file():
        return beside
    m = re.search(r"(?m)^table:\s*['\"]?skill:([^/\s]+)/([^'\"\s]+)", (doc.parent / "guide.yaml").read_text(encoding="utf-8"))
    skills = next((p / "skills" for p in doc.resolve().parents if (p / "skills").is_dir() and (p / "servers").is_dir()), None)
    found = next(skills.rglob(m.group(1)), None) if m and skills else None
    return found / m.group(2) if found else beside


def read(doc):
    text = doc.read_text(encoding="utf-8")
    title = doc.stem.replace("-", " ").capitalize()      # `paper-method.md` → "Paper method"
    if doc.stem == "method":                             # `workbench-paper/guide/method.md` → "Paper method"
        title = f"{doc.parent.parent.name.removeprefix('workbench-').replace('-', ' ')} method".capitalize()
    steps, tests, compare, sets, space_info = [], {}, {}, [], {}
    for head, rows, raw in tables(text):
        if head[0] == "step" and "where in the workbench" in head:
            col = {k: head.index(k) for k in head}
            for r in rows:
                where = r[col["where in the workbench"]]
                runs = re.search(r"·\s*runs?\s+(.+)$", where)
                views = re.sub(r"\s*·\s*runs?\s+.*$", "", where).partition("›")[2].strip()
                steps.append({"name": r[0], "does": r[col.get("what happens", 1)],
                              "signs": r[col["who signs"]] if "who signs" in col else "",
                              "space": where.split("›")[0].strip(), "views": views,
                              "runs": [x.strip() for x in runs.group(1).split(",")] if runs else []})
        elif head[:2] == ["space", "what it is for"]:   # each Space: what it is for, its Views
            last = ""
            for r in rows:
                last = r[0] or last
                sp = space_info.setdefault(last, {"for": "", "views": []})
                sp["for"] = sp["for"] or r[1]
                sp["views"].append((r[2], r[3]))
        elif head[:2] == ["test", "asks"]:
            when = head.index("when") if "when" in head else None
            for r in rows:
                for n in re.findall(r"step (\d+)", r[when] if when is not None else ""):
                    tests.setdefault(int(n), []).append(r[0])
        elif head[0] == "step" and "coverage" in head and "our methods" in head:
            ours, cov = head.index("our methods"), head.index("coverage")
            sets = [(i, raw[i]) for i in range(ours + 1, cov)]          # the table's own spelling
            for r in rows:
                compare[r[0]] = {"ours": r[ours], "coverage": r[cov],
                                 "sets": {h: r[i] for i, h in sets}}
    # our runs, agents and skills: the family's Workbench Table beside its method file
    agents = {}
    table = workbench_table(doc)
    if table.is_file():
        for head, rows, _ in tables(table.read_text(encoding="utf-8")):
            if "run type" in head and "agent" in head and "skill" in head:
                for r in rows:
                    agents[r[head.index("run type")]] = (r[head.index("agent")], r[head.index("skill")])
    return title, steps, tests, compare, [h for _, h in sets], agents, space_info


class Scene:
    def __init__(self):
        self.elements = []

    def _base(self, kind, id_, x, y, w, h, **extra):
        e = {"id": id_, "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
             "strokeColor": extra.pop("stroke", INK), "backgroundColor": "transparent", "fillStyle": "solid",
             "strokeWidth": extra.pop("strokeWidth", 2), "strokeStyle": extra.pop("strokeStyle", "solid"),
             "roughness": 0, "opacity": 100, "groupIds": [], "frameId": None, "roundness": extra.pop("roundness", None),
             "seed": rng.randrange(1, 2 ** 31), "version": 1, "versionNonce": rng.randrange(1, 2 ** 31),
             "isDeleted": False, "boundElements": [], "updated": 1790976316209, "link": None, "locked": False}
        e.update(extra)
        self.elements.append(e)
        return e

    def text(self, id_, x, y, value, size=16, color=INK, container=None, w=None, align="left"):
        lines = value.split("\n")
        width = w or max(len(l) for l in lines) * size * 0.62
        return self._base("text", id_, x, y, width, len(lines) * size * 1.25, stroke=color, text=value,
                          originalText=value, fontSize=size, fontFamily=FONT, textAlign=align,
                          verticalAlign="middle" if container else "top", containerId=container,
                          autoResize=container is None, lineHeight=1.25)

    def box(self, id_, x, y, w, h, label, color, size=15, dashed=False, width=2):
        box = self._base("rectangle", id_, x, y, w, h, stroke=color, roundness={"type": 3},
                         strokeStyle="dashed" if dashed else "solid", strokeWidth=width)
        body = self.text(id_ + "-t", x + 10, y + 8, label, size, INK, container=id_, w=w - 20)
        body["y"] = y + (h - body["height"]) / 2
        box["boundElements"].append({"id": body["id"], "type": "text"})
        return box

    def arrow(self, id_, a, b, down=False, left=False, free=False):
        """A straight arrow between two boxes, bound at both ends: right edge to left edge, or,
        `down`, bottom edge to top edge."""
        if free:
            x0, y0 = a["x"] + a["width"] + 4, a["y"] + a["height"] / 2
            dx, dy = b["x"] - x0 - 4, b["y"] + b["height"] / 2 - y0
        elif left:
            x0, y0 = a["x"] - 4, a["y"] + a["height"] / 2
            dx, dy = b["x"] + b["width"] - x0 + 4, 0
        elif down:
            x0, y0 = a["x"] + 60, a["y"] + a["height"] + 4
            dx, dy = 0, b["y"] - y0 - 4
        else:
            x0, y0 = a["x"] + a["width"] + 4, a["y"] + a["height"] / 2
            dx, dy = b["x"] - x0 - 4, 0
        e = self._base("arrow", id_, x0, y0, abs(dx), abs(dy), stroke=MUTED, points=[[0, 0], [dx, dy]],
                       lastCommittedPoint=None, startArrowhead=None, endArrowhead="arrow", elbowed=False,
                       startBinding={"elementId": a["id"], "focus": 0, "gap": 4},
                       endBinding={"elementId": b["id"], "focus": 0, "gap": 4})
        a["boundElements"].append({"id": id_, "type": "arrow"})
        b["boundElements"].append({"id": id_, "type": "arrow"})
        return e


def wrap(value, width_px, size):
    return "\n".join(textwrap.fill(p, max(12, int(width_px / (size * 0.62)))) for p in value.split("\n"))


def coverage_color(text):
    t = text.lower()
    return GAP if "gap" in t else OURS if "ours only" in t else BOTH if t.startswith("both") else MUTED


def coverage_text(text):
    """`Ours only · x. Gap · y` → "Ours only: x." and "Gap: y" on their own lines."""
    parts = [p.strip() for p in re.split(r"(?:^|\.?\s)(?=(?:Both|Ours only|Gap) · )", text) if p.strip()]
    return "\n".join(p.replace(" · ", ": ", 1).rstrip(":") for p in parts)


def draw(doc):
    title, steps, tests, compare, sets, agents, space_info = read(doc)
    if not steps:
        raise SystemExit(f"{doc}: needs a `step | what happens | methods | where in the workbench` table")
    s = Scene()
    # inside a Space's frame, ours: the step, its methods, its tests, its runs with their agent and
    # skill; outside, on the right, the compared skill sets and the coverage, each row pointing back
    # to its step with an arrow (JL 261003: "put it in the right and use <--- to link them")
    inner = ([("Space · its Views", 360)] if space_info else []) + \
        [("Step", 340), ("Our methods", 260), ("Tests", 160), ("Our runs · agent · skill", 470)]
    lead = 1 if space_info else 0                     # the Space column spans the frame's rows
    outer = [(name, 320) for name in sets] + ([("Coverage", 320)] if compare else [])
    gap, pad, link = 22, 34, 110
    xs, x = [], 40 + pad
    for i, (_, w) in enumerate(inner):
        xs.append(x)
        x += w + gap + (90 if lead and i == 0 else 0)  # room for the View → step arrows
    frame_w = x - gap + pad - 40
    ox, x = [], 40 + frame_w + link
    for _, w in outer:
        ox.append(x)
        x += w + gap
    # no file notes on the canvas (JL 261003): it says what it shows, not where it is kept
    s.text("title", 40, 30, f"{title} · in one picture", 32)
    s.text("note", 40, 80, "Top to bottom, one frame per Space. Inside a frame, each row is one step and how we "
                           "do it; on the right, what other skill sets use for that step.", 16, MUTED)
    y = 124
    if compare:
        lx = ox[0]
        for key, label, color in (("both", "Both cover it", BOTH), ("ours", "Ours only", OURS),
                                  ("gap", "Gap: they have it, we do not", GAP)):
            s.box(f"legend-{key}", lx, y, 300, 40, label, color, 14)
            lx += 320
        y += 70
    for i, (name, _) in enumerate(inner):
        s.text(f"col{i}", xs[i], y, name, 18, MUTED)
    for i, (name, _) in enumerate(outer):
        s.text(f"ocol{i}", ox[i], y, name, 18, MUTED)
    y += 40
    spaces = []
    for st in steps:
        if not spaces or spaces[-1][0] != st["space"]:
            spaces.append((st["space"], []))
        spaces[-1][1].append(st)
    frames, number = [], 0
    for f, (space, rows) in enumerate(spaces):
        color = SPACE_COLORS[f % len(SPACE_COLORS)]
        top, ry = y, y + 62
        row_boxes, step_boxes = [], []
        for st in rows:
            number += 1
            cmp = compare.get(st["name"], {})
            ours = [m.strip() for m in cmp.get("ours", "").split("·") if m.strip() and m.strip() != "none"]
            runs = []
            for run in st["runs"]:
                agent, skill = agents.get(run, ("", ""))
                runs.append(f"{run}\n  {agent}\n  {skill}" if agent else run)
            cells = [
                (f"{number} · {st['name']}\n{st['does']}" + (f"\nin: {st['views']}" if st["views"] else "")
                 + (f"\nsigns: {st['signs']}" if st["signs"] else ""), color, False, inner[lead][1]),
                ("\n".join(ours) or "no method of ours", color, not ours, inner[lead + 1][1]),
                ("\n".join(tests.get(number, [])) or "no test", MUTED, not tests.get(number), inner[lead + 2][1]),
                ("\n".join(runs) or "no run", color, not runs, inner[lead + 3][1]),
            ]
            right = [("\n".join(x.strip() for x in cmp.get("sets", {}).get(name, "").split("·") if x.strip()) or "-",
                      MUTED, False, w) for name, w in outer[:len(sets)]]
            if compare:
                cov = cmp.get("coverage", "")
                right.append((coverage_text(cov), coverage_color(cov), False, outer[-1][1]))
            wrapped = [(wrap(t, w - 24, 14), c, d) for t, c, d, w in cells + right]
            h = max(54, max(28 + 18 * (t.count("\n") + 1) for t, _, _ in wrapped))
            where = xs[lead:] + ox
            widths = inner[lead:] + outer
            boxes = [s.box(f"s{number}-c{c}", where[c], ry, widths[c][1], h, t, col, 14,
                           dashed=dashed, width=3 if c == 0 else 2)
                     for c, (t, col, dashed) in enumerate(wrapped)]
            s.arrow(f"s{number}-a", boxes[0], boxes[1])
            if right:                                        # the comparison points back to our step: <---
                s.arrow(f"s{number}-cmp", boxes[len(inner) - lead], boxes[len(inner) - lead - 1], left=True)
            row_boxes.append(boxes[0])
            step_boxes.append((boxes[0], st))
            ry += h + 24
        if lead:
            # the Space: what it is for, then one box per View with what it shows (JL 261003: "I want
            # each view to be a box", "explain that views as well"), each pointing to its steps
            info = space_info.get(space, {"for": "", "views": []})
            first, w0 = top + 62, inner[0][1]
            purpose = wrap(info["for"], w0, 15)
            s.text(f"space{f}-for", xs[0], first, purpose, 15, color)
            vy = first + 19 * (purpose.count("\n") + 1) + 16
            for v, (name, what) in enumerate(info["views"]):
                body = wrap(what, w0 - 24, 13)
                vh = 36 + 17 * (body.count("\n") + 1)
                view = s.box(f"space{f}-v{v}", xs[0], vy, w0, vh, f"{name}\n{body}", color, 13)
                for box, st in step_boxes:
                    if any(tok.strip() and tok.strip() in st["views"] for tok in name.split("·")):
                        s.arrow(f"space{f}-v{v}-{box['id']}", view, box, free=True)
                vy += vh + 12
            ry = max(ry, vy + 12)
        frame = s._base("rectangle", f"space{f}", 40, top, frame_w, ry - top + 10, stroke=color,
                        roundness={"type": 3}, strokeWidth=3)
        s.text(f"space{f}-t", 60, top + 16, space, 26, color)
        frames.append(frame)
        for a, b in zip(row_boxes, row_boxes[1:]):          # the steps inside a Space follow each other
            s.arrow(f"{a['id']}-next", a, b, down=True)
        y = ry + 10 + 60
    for i, (a, b) in enumerate(zip(frames, frames[1:])):    # Space to Space, down the page
        s.arrow(f"space-a{i}", a, b, down=True)
    s.text("back", 40, y - 34, "A failed check goes back up to the step it is about.", 16, MUTED)
    return {"type": "excalidraw", "version": 2, "source": "haipipe-method-canvas",
            "elements": s.elements, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("doc", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--force", action="store_true", help="replace an existing canvas: only when the person asks")
    args = ap.parse_args()
    if args.out.exists() and not args.force:
        sys.exit(f"{args.out} exists and is the source now; pass --force only when the person asks to redraw it")
    scene = draw(args.doc)
    args.out.write_text(json.dumps(scene, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    kinds = {}
    for e in scene["elements"]:
        kinds[e["type"]] = kinds.get(e["type"], 0) + 1
    print(f"{args.out.name}: {len(scene['elements'])} elements {kinds}")


if __name__ == "__main__":
    main()
