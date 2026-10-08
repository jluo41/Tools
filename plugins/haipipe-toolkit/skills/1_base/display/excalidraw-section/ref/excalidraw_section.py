#!/usr/bin/env python3
"""Draw a paper's Sections, or one Section, as a map read left to right (JL 261003: "for
drawing the sections only, I mean the paper and paragraph", "in the right part add the
evidence card as well").

    python excalidraw_section.py <page.md>                     one Section, down to its evidence
    python excalidraw_section.py --paper <paper folder>        the whole paper
        --depth section|paragraph|bullet|evidence              how far right it goes
        --check                                                build and print counts; write nothing
        --force                                                replace a map someone edited

A Section map: the Section, its paragraphs by their one-line job, each Bullet a row (role
and gist), then a Text column left empty for writing and an Evidence column, one card per
Evidence Item on its Bullet's row. The paper map: the paper, its groups (Main, Appendix,
Round), its Sections in board order, and below them as deep as `--depth` asks.

It is generated, never edited by hand: the structure lives in each Section's Draft plan
(`draft/<stem>-draft-v<G>.<S>.md`) and its Evidence Items, so the map is redrawn from them.
Its `source` names this script, which marks it generated. A map someone edited on the canvas
is not replaced without --force. The logic of a Section (why its claim holds) is the other
drawing, `draw-logic-tree`; this one shows where each part sits.

Writes `<page folder>/studio/<stem>-sections.excalidraw`, or
`<paper folder>/studio/paper-sections.excalidraw`, which Story › RoadMap Draw lists.
"""
import argparse
import json
import re
import sys
from pathlib import Path

SKILLS = next(p for p in Path(__file__).resolve().parents if p.name == "skills")
sys.path.insert(0, str(SKILLS / "1_base" / "page" / "haipipe-page"))
sys.path.insert(0, str(SKILLS / "0_utils" / "draw-logic-tree" / "ref"))

from src.item_table import read_items  # noqa: E402
from src.outline_version import latest_outline, plan_dir  # noqa: E402
from src.plan_shape import iter_plan_bullets  # noqa: E402
from draw_logic_tree import (BLUE, CARD_W, GREEN, MUTED, ORANGE, TEXT_W, Scene,  # noqa: E402
                             _cards, _short, _side_link, _stack_height)

SOURCE = "Tools/plugins/haipipe-toolkit/skills/1_base/display/excalidraw-section/ref/excalidraw_section.py"
DEPTHS = ("section", "paragraph", "bullet", "evidence")
KINDS = ("paper", "group", "section", "division", "paragraph", "bullet")
W, WB, GAPX, GAPY, GROUP = 190, 300, 64, 14, 26


def cols(width, size):
    """How many characters fit on one line of a box `width` wide, in the Studio's hand."""
    return int((width - 18) / (size * 0.62))


def nice(stem):
    """`S-ManSci-Main-1-Introduction` → "1 · Introduction"; `…-Abstract` → "Abstract"."""
    parts = stem.split("-")
    name = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", parts[-1])
    return "%s · %s" % (parts[-2], name) if len(parts) > 1 and parts[-2].isdigit() else name


def node(kind, lines, kids=(), stroke=BLUE, dashed=False, items=()):
    return {"kind": kind, "lines": list(lines), "kids": list(kids), "stroke": stroke,
            "dashed": dashed, "items": list(items)}


def section_node(page_md, depth):
    """One Section: its paragraphs (under their part when it has several), its Bullets, and
    their Evidence Items."""
    plan = latest_outline(plan_dir(page_md.parent), page_md.stem)
    title = _short(nice(page_md.stem), cols(W, 15), 2)
    if plan is None:
        return node("section", title + ["no plan yet"], stroke=MUTED, dashed=True)
    bullets = list(iter_plan_bullets(plan.read_text(encoding="utf-8", errors="replace")))
    needs = {}
    for item_id, row in read_items(page_md).items():
        needs.setdefault(row.get("target", ""), []).append((item_id, row))
    if depth == "section" or not bullets:
        return node("section", title + ["%d Bullets" % len(bullets)])
    divisions = list(dict.fromkeys(b["division"] for b in bullets))
    many = len(divisions) > 1

    def paragraphs(rows):
        out = []
        for p in dict.fromkeys(b["paragraph"] for b in rows):
            mine = [b for b in rows if b["paragraph"] == p]
            gist = re.split(r"\s+·\s+", mine[0]["paragraph_title"])[0]
            lines = _short("%s · %s" % (p.split(".")[-1], gist), cols(W, 13), 3)
            kids = [] if depth == "paragraph" else [bullet_node(b) for b in mine]
            out.append(node("paragraph", lines, kids))
        return out

    def bullet_node(b):
        point = b.get("point") or {}
        sentence = point.get("statement") or re.sub(r"^\[[^\]]*\]\s*", "", b["head"])
        items = needs.get(b["address"], []) if depth == "evidence" else []
        waiting = any("✅" not in (r.get("verified") or "") for _i, r in needs.get(b["address"], []))
        return node("bullet", ["%s · %s" % (b["bullet"], point.get("role") or "")] + _short(sentence.rstrip("."), cols(WB, 13), 2),
                    stroke=ORANGE if waiting else GREEN, dashed=waiting, items=items)

    if many:
        kids = [node("division", _short("%s · %s" % (d, re.split(r"\s+·\s+", next(
            b["division_title"] for b in bullets if b["division"] == d))[0]), cols(W, 13), 3),
            paragraphs([b for b in bullets if b["division"] == d])) for d in divisions]
    else:
        kids = paragraphs(bullets)
    return node("section", title + [plan.name.split("-draft-")[-1].replace(".md", "")], kids)


def paper_groups(board):
    """The board's Section groups and their Pages, in board.md order (its `## Pages`), the
    Story group left out: [(group name, [page.md, …])]."""
    text = (board / "board.md").read_text(encoding="utf-8")
    pages = text.split("\n## Pages", 1)[-1].split("\n## ", 1)[0]
    groups, cur = [], None
    for line in pages.splitlines():
        head = re.match(r"^###\s+\S+\s+·\s+(\S+)", line)
        if head:
            cur = None if "story" in head.group(1).lower() else (head.group(1), [])
            if cur:
                groups.append(cur)
        elif cur and re.fullmatch(r"\S+\.md", line.strip()):
            page = board / cur[0] / line.strip()[:-3] / line.strip()
            if page.is_file():
                cur[1].append(page)
    return groups


def layout(root, depth):
    """Left to right: one column a kind, each leaf a row, a parent level with the middle of
    what it holds; a Bullet's row grows to hold its evidence cards."""
    s = Scene(sum(map(ord, root["lines"][0])))
    kinds = []

    def walk(n):
        kinds.append(n["kind"])
        for k in n["kids"]:
            walk(k)
    walk(root)
    xs, x = {}, 40
    for kind in KINDS:
        if kind in kinds:
            xs[kind] = x
            x += (WB if kind == "bullet" else W) + GAPX
    ev_x = xs.get("bullet", 40) + WB + TEXT_W
    cursor = [70.0]

    def place(n, key):
        size = 15 if n["kind"] in ("paper", "section") else 13
        w = WB if n["kind"] == "bullet" else W
        h = len(n["lines"]) * size * 1.25 + 16
        if n["kids"]:
            spans = []
            for i, k in enumerate(n["kids"]):
                if i and n["kind"] in ("paper", "group"):
                    cursor[0] += GROUP
                spans.append(place(k, "%s.%d" % (key, i)))
            y = (spans[0][0] + spans[-1][1]) / 2 - h / 2
        else:
            y = cursor[0]
            cursor[0] += max(h, _stack_height(n["items"], CARD_W) if n["items"] else 0) + GAPY
        n["box"] = s.box(key, xs[n["kind"]], y, w, h, "\n".join(n["lines"]), n["stroke"], size,
                         dashed=n["dashed"], align="left" if n["kind"] == "bullet" else "center")
        if n["items"]:
            _cards(s, n["items"], ev_x, y, CARD_W)
        for i, k in enumerate(n["kids"]):
            _side_link(s, "e-%s.%d" % (key, i), n["box"], k["box"], GAPX)
        return min([y] + [k["box"]["y"] for k in n["kids"]]), \
            max([y + h] + [k["box"]["y"] + k["box"]["height"] for k in n["kids"]])

    place(root, "s0")
    s.text("subtitle", 40, 10, "%s · where each part sits, read left to right (generated from the plans; "
           "dashed = evidence waiting)" % root["lines"][0], 13, MUTED)
    if depth == "evidence" and "bullet" in xs:
        s.text("ev-head-text", xs["bullet"] + WB + 24, 40, "Text · write each point here", 14, MUTED)
        s.text("ev-head-evidence", ev_x, 40, "Evidence", 14, MUTED)
    return {"type": "excalidraw", "version": 2, "source": SOURCE, "elements": s.elements,
            "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}


def edited(path):
    """Has someone changed this map on the canvas (any element past its first version)?"""
    try:
        return any(e.get("version", 1) > 1 for e in json.loads(path.read_text(encoding="utf-8"))["elements"])
    except (OSError, ValueError, KeyError):
        return False


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("page", nargs="?", type=Path, help="one Section's .md file")
    ap.add_argument("--paper", type=Path, help="the paper board's folder (holds board.md)")
    ap.add_argument("--depth", choices=DEPTHS, help="paper default: paragraph; a Section: evidence")
    ap.add_argument("--check", action="store_true", help="build and print counts; write nothing")
    ap.add_argument("--force", action="store_true", help="replace a map someone edited on the canvas")
    args = ap.parse_args(argv)
    if bool(args.page) == bool(args.paper):
        ap.error("give one Section's page.md, or --paper <folder>")
    if args.paper:
        board = args.paper.resolve()
        depth = args.depth or "paragraph"
        groups = [node("group", [nice(g)], [section_node(p, depth) for p in pages]) for g, pages in paper_groups(board)]
        root = node("paper", _short(re.sub(r"(?<=[a-z])(?=[A-Z])", " ", board.name.replace("Paper-", "")), cols(W, 15), 3), groups)
        out = board / "studio" / "paper-sections.excalidraw"
    else:
        page = args.page.resolve()
        depth = args.depth or "evidence"
        root = section_node(page, depth)
        out = page.parent / "studio" / ("%s-sections.excalidraw" % page.stem)
    scene = layout(root, depth)
    kinds = {}
    for e in scene["elements"]:
        if e["type"] == "rectangle":
            kind = "card" if e["id"].startswith("ev-") else "box"
            kinds[kind] = kinds.get(kind, 0) + 1
    if out.exists() and edited(out) and not args.force and not args.check:
        raise SystemExit("%s was edited on the canvas; it is generated, so pass --force to redraw it" % out.name)
    if not args.check:
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps(scene, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("%s %s: depth %s, %d boxes, %d evidence cards, %d elements"
          % ("would write" if args.check else "wrote", out.name, depth, kinds.get("box", 0), kinds.get("card", 0),
             len(scene["elements"])))


if __name__ == "__main__":
    main()
