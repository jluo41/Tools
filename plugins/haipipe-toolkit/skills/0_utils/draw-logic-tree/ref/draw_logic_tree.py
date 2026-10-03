#!/usr/bin/env python3
"""Draw the first version of one Page's RoadMap, the Section's logic (JL 261003: "add the
excalidraw to show the structure of this section"; "the logic just go to the roadmap draw").

The RoadMap drawing is where the Section's logic lives: after this first draw it is edited
on the canvas (Draft › RoadMap Draw), so this script never replaces it without --force.
With --logic <outline> it draws that logic as a top-down tree (claim on top, each box
splitting into the reasons beneath it, Bullets as leaves); without it, a plain tree of the
plan's paragraphs and Bullets.

    python Tools/plugins/haipipe-toolkit/skills/0_utils/draw-logic-tree/ref/draw_logic_tree.py <page.md> --logic <outline>
    python …/draw_logic_tree.py <page.md> --check-scene      # check a drawing someone edited

The rules this script keeps are the `draw-logic-tree` skill (../SKILL.md).

Reads the Page's latest Draft plan (`draft/<stem>-draft-v<G>.<S>.md`, its `## 1 Structure`)
and its Evidence Items (`draft/<stem>-evidence-items.md`), and writes
`<page folder>/studio/<stem>-roadmap.excalidraw`, which Draft › RoadMap Draw shows.

A branching tree read top to bottom (JL 261003: a tree plot, "up to bottom", drawn as the
sketch: one parent, its children side by side below it; "concise and high level, after
reading the structure of the draw, we know what it is about"): the Section's title on top,
each paragraph under it by its one-line job, and each paragraph's Bullets spread below it,
five to a row, each box its role and the gist of its sentence. Reading the boxes left to
right, row by row, tells what the Section argues. A Bullet whose Evidence Items are all
verified (or that needs none) is solid green, one still waiting dashed orange; the items
themselves stay in the Evidence Space.

The scene is generated: change the plan or the Evidence Items and rerun this script; never
edit the drawing. Studio style (haipipe-workbench-studio/ref/draw.md): transparent boxes,
colored strokes, labels bound inside their boxes, arrows bound at both ends, Comic Shanns.
"""
import argparse
import json
import random
import re
import sys
import textwrap
from pathlib import Path

# the Page grammar (Draft plan, Evidence Items) lives with haipipe-page
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "page" / "haipipe-page"))

from src.item_table import read_items  # noqa: E402
from src.outline_version import latest_outline, plan_dir, version_tag  # noqa: E402
from src.plan_shape import iter_plan_bullets  # noqa: E402

INK, MUTED = "#1e1e1e", "#868e96"
BLUE, GREEN, ORANGE = "#1971c2", "#2f9e44", "#e8590c"
INDENT, LEFT, PER_ROW, BOX_W, BOX_H, GAP_X, GAP_Y = 44, 40, 5, 210, 96, 26, 56


class Scene:
    """Deterministic Excalidraw elements in the Studio style."""

    def __init__(self, seed):
        self.rng, self.elements = random.Random(seed), []

    def element(self, key, kind, x, y, w, h, stroke=INK, dashed=False, **extra):
        item = {"id": key, "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
                "strokeColor": stroke, "backgroundColor": "transparent", "fillStyle": "solid",
                "strokeWidth": 2, "strokeStyle": "dashed" if dashed else "solid", "roughness": 1,
                "opacity": 100, "groupIds": [], "frameId": None,
                "roundness": {"type": 3} if kind == "rectangle" else None,
                "seed": self.rng.randint(1, 2**31 - 1), "version": 1,
                "versionNonce": self.rng.randint(1, 2**31 - 1), "isDeleted": False,
                "boundElements": [], "updated": 0, "link": None, "locked": False}
        item.update(extra)
        self.elements.append(item)
        return item

    def text(self, key, x, y, value, size=16, color=INK, container=None, align="left"):
        lines = value.split("\n")
        w = max(len(line) for line in lines) * size * 0.6
        return self.element(key, "text", x, y, w, len(lines) * size * 1.25, color, text=value,
                            originalText=value, fontSize=size, fontFamily=8, textAlign=align,
                            verticalAlign="middle" if container else "top", containerId=container,
                            autoResize=True, lineHeight=1.25)

    def box(self, key, x, y, w, h, label, stroke=INK, size=14, dashed=False, align="left"):
        rect = self.element(key, "rectangle", x, y, w, h, stroke, dashed)
        label_h = len(label.split("\n")) * size * 1.25
        inner = self.text(key + "-label", x + 10, y + (h - label_h) / 2, label, size, INK, key, align)
        inner["width"] = w - 20
        rect["boundElements"].append({"type": "text", "id": inner["id"]})
        return rect

    def elbow(self, key, a, b):
        """Parent to child in the tree: down from the parent's left side, then right into
        the child's left edge; bound at both ends."""
        x0, y0 = a["x"] + 20, a["y"] + a["height"]
        x1, y1 = b["x"], b["y"] + b["height"] / 2
        self.element(key, "arrow", x0, y0 + 4, abs(x1 - x0), abs(y1 - y0), MUTED,
                     points=[[0, 0], [0, y1 - y0 - 4], [x1 - x0 - 6, y1 - y0 - 4]],
                     lastCommittedPoint=None, startArrowhead=None, endArrowhead="arrow", elbowed=False,
                     startBinding={"elementId": a["id"], "focus": 0, "gap": 4},
                     endBinding={"elementId": b["id"], "focus": 0, "gap": 4})
        a["boundElements"].append({"type": "arrow", "id": key})
        b["boundElements"].append({"type": "arrow", "id": key})

    def connect(self, key, a, b, pts, color=MUTED):
        """A connector from `a` to `b` along `pts` (relative to its start), bound at both ends."""
        x0, y0 = a["x"] + a["width"] / 2 + pts[0][0], a["y"] + a["height"] + 4
        self.element(key, "arrow", x0, y0, max(abs(p[0]) for p in pts) or 1, max(abs(p[1]) for p in pts),
                     color, points=[[px - pts[0][0], py] for px, py in pts], lastCommittedPoint=None,
                     startArrowhead=None, endArrowhead="arrow", elbowed=False,
                     startBinding={"elementId": a["id"], "focus": 0, "gap": 4},
                     endBinding={"elementId": b["id"], "focus": 0, "gap": 4})
        a["boundElements"].append({"type": "arrow", "id": key})
        b["boundElements"].append({"type": "arrow", "id": key})

    def arrow(self, key, a, b):
        """Bound at both ends: side to side within a row, else bottom to top."""
        if abs(a["y"] - b["y"]) < 1:
            x0, y0 = a["x"] + a["width"], a["y"] + a["height"] / 2
            x1, y1 = b["x"], b["y"] + b["height"] / 2
            pts = [[0, 0], [x1 - x0 - 8, 0]]
            x0 += 4
        else:
            x0, y0 = a["x"] + a["width"] / 2, a["y"] + a["height"]
            x1, y1 = b["x"] + b["width"] / 2, b["y"]
            pts = [[0, 0], [0, (y1 - y0) / 2], [x1 - x0, (y1 - y0) / 2], [x1 - x0, y1 - y0 - 8]]
            y0 += 4
        self.element(key, "arrow", x0, y0, abs(x1 - x0), abs(y1 - y0), INK, points=pts,
                     lastCommittedPoint=None, startArrowhead=None, endArrowhead="arrow", elbowed=False,
                     startBinding={"elementId": a["id"], "focus": 0, "gap": 4},
                     endBinding={"elementId": b["id"], "focus": 0, "gap": 4})
        a["boundElements"].append({"type": "arrow", "id": key})
        b["boundElements"].append({"type": "arrow", "id": key})


def _short(text, width, lines):
    out = textwrap.wrap(re.sub(r"\s+", " ", text or "").strip(), width) or [""]
    return out[:lines - 1] + [textwrap.shorten(" ".join(out[lines - 1:]), width, placeholder="…")] \
        if len(out) > lines else out


def _item_label(item_id, row):
    num = re.match(r"E(\d+)", item_id)
    return "E%s %s" % (num.group(1) if num else "?", row.get("label") or row.get("type", "").lower())


def parse_logic(text):
    """An indented outline (two spaces a level) -> nested nodes. A line is `- <label>`,
    `- <label> · B<n> [· B<m>]`, or just `- B<n>` for a Bullet leaf."""
    root, stack = {"label": "", "refs": [], "kids": []}, []
    for raw in text.splitlines():
        m = re.match(r"^(\s*)-\s+(.*\S)\s*$", raw)
        if not m:
            continue
        depth, body = len(m.group(1)) // 2, m.group(2)
        parts = [x.strip() for x in body.split(" · ")]
        refs = [x for x in parts if re.fullmatch(r"B\d+", x)]
        label = " · ".join(x for x in parts if x not in refs)
        node = {"label": label, "refs": refs, "kids": []}
        while stack and stack[-1][0] >= depth:
            stack.pop()
        (stack[-1][1]["kids"] if stack else root["kids"]).append(node)
        stack.append((depth, node))
    return root["kids"]


def logic_tree(page_md: Path, logic_text: str):
    """The Section's logic as a top-down tree (JL 261003: "the logic just go to the roadmap
    draw"): the claim on top, each box splitting into the reasons beneath it, the Bullets
    as leaves with their role, gist and evidence state. Returns (scene, plan, counts)."""
    plan = latest_outline(plan_dir(page_md.parent), page_md.stem)
    by_bullet = {}
    if plan is not None:
        for b in iter_plan_bullets(plan.read_text(encoding="utf-8", errors="replace")):
            by_bullet.setdefault(b["bullet"], b)
    items = read_items(page_md)
    needs = {}
    for item_id, row in items.items():
        needs.setdefault(row.get("target", ""), []).append((item_id, row))
    tops = parse_logic(logic_text)
    if not tops:
        raise SystemExit("the logic outline is empty")
    W, GAPX, GAPY = 176, 22, 70
    s = Scene(sum(map(ord, page_md.stem)) + 7)

    def lines(node, size=13):
        cols = int((W - 16) / (size * 0.6))
        if node["label"]:
            out = _short(node["label"], cols, 4 if size > 13 else 3)
            if node["refs"]:
                out.append(" · ".join(node["refs"]))
            return out
        b = by_bullet.get(node["refs"][0]) if node["refs"] else None
        if b is None:
            return [" · ".join(node["refs"]) or "?"]
        point = b.get("point") or {}
        sentence = point.get("statement") or re.sub(r"^\[[^\]]*\]\s*", "", b["head"])
        return ["%s · %s" % (b["bullet"], point.get("role") or "")] + _short(sentence.rstrip("."), cols, 3)

    def width(node):
        node["w"] = max(W, sum(width(k) for k in node["kids"]) + GAPX * (len(node["kids"]) - 1)) \
            if node["kids"] else W
        return node["w"]

    # every Bullet starts on one shared row, the deepest a reason reaches; a Bullet that
    # supports another Bullet sits one row below it (JL 261003: "could you make the Bullet
    # point to be in the same start in the same level?")
    def is_bullet(node):
        return not node["label"] and bool(node["refs"])

    def first_bullets(node, depth, out):
        for k in node["kids"]:
            if is_bullet(k) and not is_bullet(node):
                out.append(depth + 1)
            first_bullets(k, depth + 1, out)
        return out

    starts = [d for t in tops for d in first_bullets(t, 0, [])] + [0]
    bullet_row = max(starts)
    level_h = {}

    def heights(node, depth, parent=None):
        if is_bullet(node):
            depth = parent["level"] + 1 if parent is not None and is_bullet(parent) else bullet_row
        node["level"] = depth
        size = 15 if depth == 0 else 13
        node["lines"] = lines(node, size)
        node["h"] = len(node["lines"]) * size * 1.25 + 16
        level_h[depth] = max(level_h.get(depth, 0), node["h"])
        for k in node["kids"]:
            heights(k, depth + 1, node)

    for t in tops:
        width(t)
        heights(t, 0)
    ys, y = {}, 40
    for d in sorted(level_h):
        ys[d] = y
        y += level_h[d] + GAPY
    waiting = [0]

    def place(node, x, _depth, key, parent=None):
        depth = node["level"]
        cx = x + node["w"] / 2
        refs = [r for r in node["refs"]]
        open_ = [k for r in refs for k, row in needs.get((by_bullet.get(r) or {}).get("address", ""), [])
                 if "✅" not in (row.get("verified") or "")]
        leaf_bullet = not node["label"] and refs
        waiting[0] += bool(open_) and bool(leaf_bullet)
        stroke = (ORANGE if open_ else GREEN) if leaf_bullet else BLUE
        box = s.box(key, cx - W / 2, ys[depth], W, node["h"], "\n".join(node["lines"]), stroke,
                    15 if depth == 0 else 13, dashed=bool(open_) and bool(leaf_bullet), align="center")
        if parent is not None:
            px = parent["x"] + parent["width"] / 2
            py = parent["y"] + parent["height"]
            mid = ys[depth] - GAPY / 2 - py      # the bus sits just above the child's row
            s.connect("e-" + key, parent, box, [[0, 0], [0, mid], [cx - px, mid], [cx - px, ys[depth] - py - 8]])
        kx = x + (node["w"] - (sum(k["w"] for k in node["kids"]) + GAPX * (len(node["kids"]) - 1))) / 2
        for i, k in enumerate(node["kids"]):
            place(k, kx, depth + 1, "%s.%d" % (key, i), box)
            kx += k["w"] + GAPX

    x = 0
    for i, t in enumerate(tops):
        place(t, x, 0, "n%d" % i)
        x += t["w"] + GAPX * 3
    s.text("subtitle", 0, 0, "%s · the Section's logic: each box rests on the boxes below it; Bullets are "
           "the leaves (dashed = evidence waiting)" % page_md.stem, 13, MUTED)
    scene = {"type": "excalidraw", "version": 2, "source": "haipipe-page-roadmap",
             "elements": s.elements, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
             "files": {}}
    return scene, plan, {"bullets": sum(1 for r in by_bullet), "paragraphs": 0, "waiting": waiting[0],
                         "elements": len(s.elements)}


def roadmap(page_md: Path):
    """Build the scene for `page_md`; returns (scene dict, plan path, counts)."""
    plan = latest_outline(plan_dir(page_md.parent), page_md.stem)
    if plan is None:
        raise SystemExit(f"{page_md}: no Draft plan in draft/")
    bullets = list(iter_plan_bullets(plan.read_text(encoding="utf-8", errors="replace")))
    items = read_items(page_md)
    needs = {}
    for item_id, row in items.items():
        needs.setdefault(row.get("target", ""), []).append((item_id, row))

    s = Scene(sum(map(ord, page_md.stem)))
    paragraphs_ = list(dict.fromkeys(b["paragraph"] for b in bullets))
    divisions = list(dict.fromkeys(b["division"] for b in bullets))
    title = re.split(r"\s+·\s+", bullets[0]["division_title"])[0] if len(divisions) == 1 else page_md.stem
    waiting = sum(1 for b in bullets
                  if any("✅" not in (r.get("verified") or "") for _i, r in needs.get(b["address"], [])))
    s.text("subtitle", 0, 0, "%d paragraph%s · %d Bullets · %d waiting on evidence (dashed)   ·   %s"
           % (len(paragraphs_), "" if len(paragraphs_) == 1 else "s", len(bullets), waiting, plan.name),
           13, MUTED)
    width = PER_ROW * BOX_W + (PER_ROW - 1) * GAP_X
    root = s.box("root", LEFT, 30, width, 50, title, BLUE, 22, align="center")
    y = 30 + 50 + 46
    for p_id in paragraphs_:
        rows = [b for b in bullets if b["paragraph"] == p_id]
        gist = re.split(r"\s+·\s+", rows[0]["paragraph_title"])[0]
        par = s.box("par-" + p_id, LEFT, y, width, 40, _short(gist, 100, 1)[0], BLUE, 15, align="center")
        # the Section to its paragraph: straight down when there is one, else down the trunk
        s.elbow("e-" + par["id"], root, par) if len(paragraphs_) > 1 else \
            s.connect("e-" + par["id"], root, par, [[0, 0], [0, y - (30 + 50) - 10]], BLUE)
        top = y + 40 + 50
        for i, b in enumerate(rows):
            col, row = i % PER_ROW, i // PER_ROW
            n_row = min(PER_ROW, len(rows) - row * PER_ROW)
            x0 = LEFT + (width - (n_row * BOX_W + (n_row - 1) * GAP_X)) / 2     # each row centred
            bx, by = x0 + col * (BOX_W + GAP_X), top + row * (BOX_H + GAP_Y)
            point = b.get("point") or {}
            role = point.get("role") or b["bullet"]
            sentence = point.get("statement") or re.sub(r"^\[[^\]]*\]\s*", "", b["head"])
            open_ = [k for k, r in needs.get(b["address"], []) if "✅" not in (r.get("verified") or "")]
            # a Bullet: its role, then the gist of its sentence (JL 261003: a branching tree,
            # "concise and high level, after reading the structure of the draw, we know what it is about")
            child = s.box("b-" + b["address"], bx, by, BOX_W, BOX_H,
                          "\n".join([role] + _short(sentence.rstrip("."), 24, 3)),
                          ORANGE if open_ else GREEN, 13, dashed=bool(open_), align="center")
            # the paragraph to each Bullet: down to a bus over the row, across, down
            cx, bus = bx + BOX_W / 2 - (LEFT + width / 2), by - GAP_Y / 2 - (y + 40 + 4)
            if row == 0:
                pts = [[0, 0], [0, bus], [cx, bus], [cx, by - (y + 40 + 4) - 4]]
            else:                                     # later rows: down the left margin first
                mx = LEFT - 24 - (LEFT + width / 2)
                pts = [[0, 0], [0, 18], [mx, 18], [mx, bus], [cx, bus], [cx, by - (y + 40 + 4) - 4]]
            s.connect("e-" + child["id"], par, child, pts)
        n_rows = (len(rows) - 1) // PER_ROW + 1
        y = top + n_rows * (BOX_H + GAP_Y) + 20
    paragraphs = paragraphs_
    scene = {"type": "excalidraw", "version": 2, "source": "haipipe-page-roadmap",
             "elements": s.elements, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
             "files": {}}
    return scene, plan, {"bullets": len(bullets), "paragraphs": len(paragraphs), "waiting": waiting,
                         "elements": len(s.elements)}


def check_scene(page_md: Path, scene_path: Path) -> list[str]:
    """Findings for a RoadMap someone drew or edited: every Bullet is a leaf, the Bullets that
    hang from a reason share one row, nothing is filled, every connector is bound."""
    els = [e for e in json.loads(scene_path.read_text(encoding="utf-8"))["elements"] if not e.get("isDeleted")]
    by = {e["id"]: e for e in els}
    label = {e["containerId"]: e["text"] for e in els if e["type"] == "text" and e.get("containerId")}
    boxes = {k: by[k] for k in label if by.get(k, {}).get("type") == "rectangle"}
    bullet_of = {k: re.match(r"^(B\d+)\b", v).group(1) for k, v in label.items()
                 if k in boxes and re.match(r"^B\d+\b", v)}
    out = []
    plan = latest_outline(plan_dir(page_md.parent), page_md.stem)
    if plan is not None:
        want = {b["bullet"] for b in iter_plan_bullets(plan.read_text(encoding="utf-8", errors="replace"))}
        named = {m for k, v in label.items() if k in boxes for m in re.findall(r"\bB\d+\b", v)}
        missing = sorted(want - named, key=lambda x: int(x[1:]))   # a claim box may name its Bullet (· B8)
        if missing:
            out.append("Bullets with no box: " + " ".join(missing))
    parent = {}
    for e in els:
        if e["type"] == "arrow":
            a, b = (e.get("startBinding") or {}).get("elementId"), (e.get("endBinding") or {}).get("elementId")
            if not (a and b):
                out.append("connector %s is not bound at both ends" % e["id"])
            else:
                parent[b] = a
    first = {k: boxes[k]["y"] for k in bullet_of if parent.get(k) not in bullet_of}
    if first and max(first.values()) - min(first.values()) > 8:
        out.append("Bullets under a reason do not share one row: " + ", ".join(
            "%s y=%d" % (bullet_of[k], v) for k, v in sorted(first.items(), key=lambda kv: kv[1])))
    for k in bullet_of:
        if parent.get(k) in bullet_of and boxes[k]["y"] <= boxes[parent[k]]["y"]:
            out.append("%s should sit below %s, the Bullet it supports" % (bullet_of[k], bullet_of[parent[k]]))
    filled = [e["id"] for e in els if e["type"] in ("rectangle", "ellipse", "diamond")
              and e.get("backgroundColor") not in (None, "transparent")]
    if filled:
        out.append("filled shapes (keep boxes transparent): " + " ".join(filled[:8]))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("page", type=Path, help="the Page's .md file")
    ap.add_argument("--check", action="store_true", help="build the scene and print counts; write nothing")
    ap.add_argument("--logic", type=Path, help="an indented logic outline to draw as the tree "
                    "(a working note of the drawing agent; it is not kept in the Page)")
    ap.add_argument("--check-scene", action="store_true",
                    help="check the existing RoadMap against the rules; write nothing")
    ap.add_argument("--force", action="store_true",
                    help="replace an existing RoadMap; it is the Section's logic and may hold the person's edits")
    args = ap.parse_args(argv)
    page_md = args.page.resolve()
    if args.check_scene:
        scene_path = page_md.parent / "studio" / ("%s-roadmap.excalidraw" % page_md.stem)
        if not scene_path.is_file():
            raise SystemExit("%s: no RoadMap yet" % scene_path.name)
        found = check_scene(page_md, scene_path)
        print("\n".join("  " + f for f in found) or "  no findings")
        print("check: %s" % ("FAIL" if found else "PASS"))
        raise SystemExit(1 if found else 0)
    if args.logic:
        scene, plan, counts = logic_tree(page_md, args.logic.read_text(encoding="utf-8"))
    else:
        scene, plan, counts = roadmap(page_md)
    out = page_md.parent / "studio" / ("%s-roadmap.excalidraw" % page_md.stem)
    if out.exists() and not args.force and not args.check:
        raise SystemExit("%s exists: the RoadMap is the Section's logic and may hold edits made on the "
                         "canvas; pass --force to replace it" % out.name)
    if not args.check:
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps(scene, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("%s %s: %d paragraphs, %d Bullets, %d waiting on evidence, %d elements (from %s)"
          % ("would write" if args.check else "wrote", out.name, counts["paragraphs"], counts["bullets"],
             counts["waiting"], counts["elements"], plan.name if plan else "no plan"))


if __name__ == "__main__":
    main()
