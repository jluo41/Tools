"""s10 · the related-work map of a paper Board: one main frame and small frames that explain it, as stairs.

    python related_map.py draw <studio/s10-related-work-map>      what the topic's forwarding builder calls

Every word comes from the topic face's yaml blocks; the closest papers are read on every build from the Board's
`related/related.md`, every row whose `bears on` cell (older tables: `group`) has a name starting "Closest:". A
Closest row the face does not place is drawn red on the map, so a paper added to the table shows up at once.

    map       ① the main frame: every closest paper in four quadrants (two axes the face names), our papers as the
              key point, clusters of cards, what is off the map, what is not placed yet (red)
    nearest   ② the nearest papers side by side with ours, a table (optional)
    gaps      ③ what each kind of closest work leaves open, and what we add (optional)
    lessons   ④ what the papers teach our methods (optional)
    papers    ⑤ on: one frame per type of paper, each paper a step: how it helps us, its method in short (optional)

Generalized from Paper-LLMRecPhy-Jama's s05 builder (JL 261013: one big main frame, small frames, a staircase, white
space); haipipe-paper-related 0.1.0 (JL 261019: "for the related work we can do things like s10-related-work").
How it looks: /excalidraw-studio (draw.py); a rebuild keeps a person's marks (haipipe-studio canvas.write).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
SKILLS = next(p for p in HERE.parents if p.name == "skills")
sys.path.insert(0, str(SKILLS / "1_base/excalidraw/excalidraw-studio/scripts"))
from draw import GREY, INK, RED, T_ACT, T_KEY, T_NODE, Drawing, canvas  # noqa: E402

CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚㉛㉜㉝㉞㉟"
TAG = {"borrow-method": "we borrow its method", "borrow-evaluation": "we borrow its evaluation",
       "baseline": "a number to compare with", "gap-we-fill": "a gap we fill", "threat": "a threat we must answer"}
MAP = {"title": "① Where our paper sits among the closest work", "sub": "★ closest in its type",
       "key": "{closest} closest papers; {placed} placed on the map.",
       "left": "◀ left axis word", "right": "right axis word ▶", "top": "top axis word", "bottom": "bottom axis word"}


def face_yaml(face: Path, key: str) -> dict:
    """One `<key>:` yaml block of the face; {} when the face has none."""
    m = re.search(rf"```yaml\n({key}:.*?)\n```", face.read_text(encoding="utf-8"), re.S) if face.is_file() else None
    return ((yaml.safe_load(m.group(1)) or {}).get(key) or {}) if m else {}


def related_rows(board: Path) -> list[dict]:
    """The Board's related/related.md rows, each a dict keyed by its lower-cased column names."""
    heads, rows = [], []
    table = board / "related" / "related.md"
    for line in table.read_text(encoding="utf-8").splitlines() if table.is_file() else []:
        if not line.startswith("|") or set(line.replace("|", "").strip()) <= set("-: "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not heads:
            heads = [c.lower() for c in cells]
            continue
        rows.append(dict(zip(heads, cells + [""] * (len(heads) - len(cells)))))
    return rows


def bears(r: dict) -> list[str]:
    """What a row bears on, one name per comma; since 261013 the research grouping is `bears on`, before it `group`."""
    return [g.strip() for g in (r.get("bears on") or r.get("group", "")).split(",") if g.strip()]


def item_name(r: dict) -> str:
    return r.get("item", "").split(" · ")[0].strip()


def closest_rows(board: Path) -> list[dict]:
    """The Closest rows of related/related.md, in their order: {name, type, star, why, read}."""
    out = []
    for r in related_rows(board):
        kinds = [g.split(":", 1)[1].strip() for g in bears(r) if g.startswith("Closest:")]
        if kinds:
            out.append({"name": item_name(r), "item": r.get("item", ""), "type": kinds[0], "star": "★" in r.get("key", ""),
                        "why": r.get("why here", ""), "read": r.get("read", "")})
    return out


def short(name: str) -> str:
    return name.replace(" et al.", "")


# ── cards ──────────────────────────────────────────────────────────────────────────────────────────────────
def card_h(name, label, w):
    return 16 + Drawing.height(name, w - 36, 30) + 4 + Drawing.height(label, w - 36, 28) + 18


def card(d, x, y, w, h, name, label, star=False, red=False):
    col = RED if red else INK
    d.box(x, y, w, h, col, 3 if star else 1.5)
    yy = d.para(x + 18, y + 14, name, w - 36, 30, col)
    d.para(x + 18, yy + 4, label, w - 36, 28, col)


def grid_cards(d, items, x, y, w, cols, gap=24, draw=True):
    """Cards in `cols` columns from (x, y); returns (bottom y, {name: (x, y, w, h)})."""
    cw = (w - gap * (cols - 1)) / cols
    at, top = {}, y
    for i in range(0, len(items), cols):
        row = items[i:i + cols]
        rh = max(card_h(n, lb, cw) for n, lb, _ in row)
        for k, (n, lb, star) in enumerate(row):
            cx = x + k * (cw + gap)
            if draw:
                card(d, cx, top, cw, rh, n, lb, star)
            at[n] = (cx, top, cw, rh)
        top += rh + gap
    return (top - gap if items else y), at


# ── ① the map ──────────────────────────────────────────────────────────────────────────────────────────────
def cluster_h(title, lines, w):
    return 16 + Drawing.height(title, w - 40, T_KEY) + 8 + sum(Drawing.height(ln, w - 40, 28) + 4 for ln in lines) + 20


def map_frame(d, m, rows):
    m = {**MAP, **(m or {})}
    W = 2560
    f = d.frame(m["title"], W, 1440)
    d.heading(m["title"], m.get("sub", ""))
    place = m.get("placements") or {}
    by_q = {"TL": [], "TR": [], "BL": [], "BR": []}
    off, unplaced = [], []
    for r in rows:
        p = place.get(r["name"])
        if not p:
            unplaced.append(short(r["name"]))
        elif p.get("at") in ("off", False):                     # YAML reads a bare off as false
            off.append(f"{short(r['name'])}, {p.get('label', '')}")
        else:
            by_q.setdefault(p["at"], []).append((("★ " if r["star"] else "") + short(r["name"]), p.get("label", ""),
                                                 r["star"]))
    n = {q: len(v) for q, v in by_q.items()}
    key = m["key"].format(builds=n["BL"] + n["TL"], audits=n["TR"] + n["BR"], left=n["BL"] + n["TL"],
                          right=n["TR"] + n["BR"], closest=len(rows), placed=sum(n.values()), **n)
    kh = Drawing.height(key, 2400, T_KEY) + 40
    d.key(40, 160, W - 80, kh)
    d.para(64, 180, key, 2420, T_KEY)
    x0, x1 = 100, W - 100
    mx = x0 + 0.36 * (x1 - x0)                                  # the right half holds the audits and our papers
    left_w, right_w = mx - 40 - x0, x1 - (mx + 40)
    yt = 160 + kh + 90                                          # the top of the map, under the top axis words
    q = m.get("quadrants") or {}
    title_h = T_NODE * 1.25 + 22 if q else 10

    # top right: our papers (the key point), then the closest work there
    ours = m.get("ours") or []
    ow = (right_w - 24) / max(len(ours), 1)
    oh = max(16 + Drawing.height(o["title"], ow - 40, 34) + sum(Drawing.height(ln, ow - 40, 28) + 4
                                                               for ln in o.get("lines", [])) + 20 for o in ours) if ours else 0
    tr_y = yt + title_h + oh + 30
    tr_bottom, _ = grid_cards(d, by_q["TR"], mx + 40, tr_y, right_w, 4, draw=False)
    tl_bottom, _ = grid_cards(d, by_q["TL"], x0, yt + title_h, left_w, 2, draw=False)   # the top left too: its
    tl_bottom += sum(Drawing.height(s, left_w, 28) + 16 for s in                         #   cards, then what is off
                     (["off the map: " + "; ".join(off)] if off else []) +                #   the map or not placed,
                     (["❓ not placed yet: " + ", ".join(unplaced)] if unplaced else [])) #   never run over the axis
    my = max(tr_bottom, tl_bottom + 24, yt + title_h + 200) + 50

    # bottom left: its clusters, side by side
    named = {x[0].removeprefix("★ "): x for x in by_q["BL"]}
    blocks = []
    for c in (m.get("clusters") or {}).get("BL") or []:
        lines = [f"{named[short(k)][0]} · {named[short(k)][1]}" for k in c["keys"] if short(k) in named]
        if lines:
            blocks.append((c["title"], lines))
    used = {ln.split(" · ")[0].removeprefix("★ ") for _, ls in blocks for ln in ls}
    loose = [x for x in by_q["BL"] if x[0].removeprefix("★ ") not in used]
    cw = (left_w - 24 * (len(blocks) - 1)) / max(len(blocks), 1)
    bl_h = title_h + max([cluster_h(tt, ls, cw) for tt, ls in blocks] or [0]) + (160 if loose else 0)
    br_bottom, _ = grid_cards(d, by_q["BR"], mx + 40, my + 60 + title_h, right_w, 4, draw=False)
    y1 = max(my + 60 + bl_h, br_bottom, my + 60 + title_h + 120) + 30

    # the axes: four arrows out from the centre, each to the words of its end
    for end in ((x0, my), (x1, my), (mx, yt - 40), (mx, y1)):
        d.line([(mx, my), end], INK, sw=3)
    top_w, bot_w = d.measure(m["top"], T_KEY), d.measure(m["bottom"], T_KEY)
    d.text(mx - top_w / 2, yt - 90, m["top"], T_KEY)
    d.text(mx - bot_w / 2, y1 + 10, m["bottom"], T_KEY)
    d.text(x0, my + 10, m["left"], T_KEY)
    d.text(x1 - d.measure(m["right"], T_KEY), my + 10, m["right"], T_KEY)

    for at, (qx, qy) in (("TL", (x0, yt)), ("TR", (mx + 40, yt)), ("BL", (x0, my + 60)), ("BR", (mx + 40, my + 60))):
        if q.get(at):
            d.text(qx, qy, q[at], T_NODE)
    yy = yt + title_h
    if by_q["TL"]:
        yy, _ = grid_cards(d, by_q["TL"], x0, yy, left_w, 2)
        yy += 24
    elif q.get("TL"):
        yy = d.para(x0, yy, "none", left_w, 28, GREY) + 40
    if off:                                                     # what is not on the map, in the top left
        yy = d.para(x0, yy, "off the map: " + "; ".join(off), left_w, 28, GREY) + 16
    if unplaced:
        d.para(x0, yy, "❓ not placed yet: " + ", ".join(unplaced), left_w, 28, RED)

    for i, o in enumerate(ours):                                # ours: the frame's key point
        ox, oy = mx + 40 + i * (ow + 24), yt + title_h
        d.key(ox, oy, ow, oh)
        y2 = d.para(ox + 20, oy + 14, o["title"], ow - 40, 34)
        for ln in o.get("lines", []):
            y2 = d.para(ox + 20, y2 + 4, ln, ow - 40, 28)
    grid_cards(d, by_q["TR"], mx + 40, tr_y, right_w, 4)

    for k, (title, lines) in enumerate(blocks):
        bx, by, h = x0 + k * (cw + 24), my + 60 + title_h, cluster_h(title, lines, cw)
        d.box(bx, by, cw, h)
        y2 = d.para(bx + 20, by + 14, title, cw - 40, T_KEY)
        for ln in lines:
            y2 = d.para(bx + 20, y2 + 6, ln, cw - 40, 28)
    if loose:
        top = my + 60 + title_h + (max(cluster_h(tt, ls, cw) for tt, ls in blocks) + 24 if blocks else 0)
        grid_cards(d, loose, x0, top, left_w, 2)
    grid_cards(d, by_q["BR"], mx + 40, my + 60 + title_h, right_w, 4)

    f["height"] = y1 + 10 + T_KEY * 1.25 + 50
    d.badge(f)
    return f


# ── ② the nearest papers, side by side with ours ───────────────────────────────────────────────────────────
def nearest_frame(d, n):
    cols = len(n["columns"])
    widths = [180] + [380] * (cols - 1)
    W = sum(widths) + 80
    f = Drawing.detail(d.frame(n["title"], W, 1200))
    d.heading(n["title"], n.get("sub", ""), W - 680)
    kh = Drawing.height(n["key"], W - 160, T_KEY) + 40
    d.key(40, 160, W - 80, kh)
    d.para(64, 180, n["key"], W - 128, T_KEY)
    rows = []
    for r in n.get("rows") or []:
        cells = []
        for c in r:
            if isinstance(c, dict):
                c = dict(c, color=RED if c.get("color") == "red" else None, size=40)
            cells.append(c)
        rows.append({"cells": cells})
    bottom = d.grid_table(40, 160 + kh + 50, n["columns"], rows, widths, size=30)
    if n.get("note"):
        bottom = d.para(40, bottom + 30, n["note"], W - 80, 24, GREY)
    f["height"] = bottom + 60
    d.badge(f)
    return f


# ── ③ what each leaves open, and what we add ───────────────────────────────────────────────────────────────
def gaps_frame(d, g):
    W = 1820
    f = d.frame(g["title"], W, 1200)
    d.heading(g["title"], g.get("sub", ""))
    kh = Drawing.height(g["key"], W - 160, T_KEY) + 40
    d.key(40, 160, W - 80, kh)
    d.para(64, 180, g["key"], W - 128, T_KEY)
    cols = [("kind", 40, 480), ("open", 640, 520), ("add", 1280, 500)]
    y = 160 + kh + 90
    for i, r in enumerate(g.get("rows") or []):
        h = max(Drawing.height(r[k], w - 40, 30) for k, _, w in cols) + 40
        for k, x, w in cols:
            d.box(x, y, w, h, RED if str(r[k]).startswith("❓") else INK, 1.5)
            d.para(x + 20, y + 20, r[k], w - 40, 30)
        for (_, xa, wa), (_, xb, _) in zip(cols, cols[1:]):
            d.line([(xa + wa + 12, y + h / 2), (xb - 12, y + h / 2)], INK, sw=2.5)
        if i == 0:
            d.text(cols[0][1] + cols[0][2] + 20, y - 44, "leaves open", 28)
            d.text(cols[1][1] + cols[1][2] + 20, y - 44, "we add", 28)
        y += h + 40
    for ln in g.get("open") or []:
        y = d.para(40, y, ln, W - 80, 30) + 10
    f["height"] = y + 40
    d.badge(f)
    return f


# ── ④ what the papers teach our methods, ⑤ on: one frame per type of paper ─────────────────────────────────
def lessons_frame(d, ls):
    """The cross-paper lessons for our methods: a flow from what the papers do to what we change."""
    W = 1820
    f = Drawing.detail(d.frame(ls["title"], W, 1000))
    d.heading(ls["title"], ls.get("sub", ""))
    kh = Drawing.height(ls["key"], W - 160, T_KEY) + 40
    d.key(40, 160, W - 80, kh)
    d.para(64, 180, ls["key"], W - 128, T_KEY)
    y = 160 + kh + 60
    d.text(40, y, "WHAT SEVERAL PAPERS DO", 28, GREY)
    d.text(960, y, "WHAT WE CHANGE IN OUR METHODS", 28, GREY)
    y += 56
    for r in ls["rows"]:
        h = max(Drawing.height(r["they"], 780 - 40, 28), Drawing.height(r["we"], 820 - 40, 28)) + 40
        d.box(40, y, 780, h)
        d.para(60, y + 20, r["they"], 740, 28)
        d.box(960, y, 820, h, dashed=True)
        d.para(980, y + 20, r["we"], 780, 28)
        d.line([(826, y + h / 2), (954, y + h / 2)], INK, sw=2.5)
        y += h + 30
    f["height"] = y + 40
    d.badge(f)
    return f


def group_frame(d, n, g, recs):
    """One type of paper as a small staircase: each paper a step lower and further right, its name, how it helps
    us, and its method in short. The full four sentences stay in the face's papers block."""
    keys = [k for k in g["keys"] if k in recs]
    W = 1500 + 50 * (len(keys) - 1) + 80
    name = f"{CIRCLED[n]} {g['act'].split(' · ', 1)[-1]}"
    f = d.frame(name, W, 800)
    d.text(40, 22, g["act"].split(" · ", 1)[-1], 44)
    y = d.para(40, 90, f"{len(keys)} papers · the four sentences of each are in the face", W - 80, 22, GREY) + 30
    for i, k in enumerate(keys):
        p = recs[k]
        x = 40 + i * 50
        tag = TAG.get(p.get("relation", ""), p.get("relation", ""))
        lines = [(f"{k} · {tag}", 28, RED if p.get("relation") == "threat" else INK),
                 (p.get("helps_us", ""), 24, INK),
                 (f"method: {p.get('method', '')}", 22, GREY)]
        h = sum(Drawing.height(s, 1420 - 44, z) + 6 for s, z, _ in lines) + 34
        d.box(x, y, 1420, h, sw=1.5)
        yy = y + 16
        for s, z, col in lines:
            yy = d.para(x + 22, yy, s, 1420 - 44, z, col) + 6
        y += h + 24
    f["height"] = y + 30
    canvas.explains(f)
    if f["height"] > canvas.FRAME_MAX[1]:
        canvas.reads_down(f)                    # a list read top to bottom; only its width must fit
    return f


def move(els, f, x, y):
    dx, dy = x - f["x"], y - f["y"]
    for e in els:
        if e["id"] == f["id"] or e.get("frameId") == f["id"]:
            e["x"], e["y"] = e["x"] + dx, e["y"] + dy


def draw(topic: Path, changes=()) -> Path:
    """One main frame (① the map) and small frames that explain it, placed as stairs (JL 2026-10-13: one big main
    frame, small frames, a staircase, white space; never a filled board). `changes`: (YYMMDD, what changed), each a
    green note on ①."""
    topic = Path(topic).resolve()
    face, board = topic / f"{topic.name}.md", topic.parents[1]
    out = topic / f"{topic.name}.excalidraw"
    builder = next((p.name for p in sorted(topic.glob("build_*.py"))), "related_map.py")
    d = Drawing()
    f1 = map_frame(d, face_yaml(face, "map"), closest_rows(board))
    d.badge = lambda f: None                                     # a small frame explains; its words are the point
    small = []
    for key, make in (("nearest", nearest_frame), ("gaps", gaps_frame), ("lessons", lessons_frame)):
        spec = face_yaml(face, key)
        if spec:
            small.append(make(d, spec))
    for f in small:
        canvas.explains(f)
    groups, papers = [], face_yaml(face, "papers")
    if papers:
        recs = {r["key"]: r for r in papers.get("records") or []}
        for i, g in enumerate(papers.get("groups") or []):
            groups.append(group_frame(d, len(small) + 1 + i, g, recs))
    for i, (date, what) in enumerate(changes):
        e = canvas.change_note(1480, 120 + i * 26, what, date, f1["id"])
        e["id"] = f"c{i}"
        d.els.append(e)
    # ① at the origin; ② to ④ step down and to the right of it; the paper types step right below it
    move(d.els, f1, 0, 0)
    x, y = f1["width"] + 360, 0
    for f in small:
        move(d.els, f, x, y)
        x, y = x + f["width"] + 220, y + 300
    low = max([f1["y"] + f1["height"]] + [f["y"] + f["height"] for f in small])
    gx, gy = 300, low + 360
    for f in groups:
        move(d.els, f, gx, gy)
        gx, gy = gx + f["width"] + 200, gy + 240
    d.fid = None
    if small:
        a, b = f1, small[0]
        ya = a["y"] + 200
        d.line([(a["x"] + a["width"] + 14, ya), (b["x"] - 14, ya)], sw=5)
        d.text(a["x"] + a["width"] + 30, ya - 56, "up close", 36)
    for p, q in zip(small, small[1:]):
        d.line([(p["x"] + p["width"] + 14, q["y"] + 100), (q["x"] - 14, q["y"] + 100)], sw=2)
    if groups:
        px = groups[0]["x"] + 260
        d.line([(px, f1["height"] + 14), (px, groups[0]["y"] - 14)], sw=5)
        d.text(px + 20, f1["height"] + 150, "each paper", 36)
    # each row named at its left, as excalidraw-studio's acts are (its check.py ③), the stairs kept as laid out
    d.para(f1["x"] - 820, f1["y"] + 20, "Act 1 · Where our paper sits", 760, T_ACT)
    if small:
        d.text(small[0]["x"], small[0]["y"] - 110, "Act 2 · Up close", T_ACT)
    if groups:
        d.para(groups[0]["x"] - 820, groups[0]["y"] + 20, f"Act {2 + bool(small)} · Each type, paper by paper",
               760, T_ACT)
    d.write(out, builder)
    sys.path.insert(0, str(SKILLS / "1_base/project/haipipe-studio/scripts"))
    from render_png import render                                # its preview, as excalidraw-read's topics have
    render(out, out.with_suffix(".png"))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("draw")
    p.add_argument("topic", type=Path)
    a = ap.parse_args(argv)
    print(draw(a.topic))
    return 0


if __name__ == "__main__":
    sys.exit(main())
