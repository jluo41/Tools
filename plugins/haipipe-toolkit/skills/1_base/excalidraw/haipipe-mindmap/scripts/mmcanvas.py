"""The canvas view of a mind map, both ways: draw it left to right from the file, and read a person's edits back.

Drawn with excalidraw-studio's helpers (draw.py: Drawing, its measure, wrap, key colour and the ⑥ ⑦ badge). Every
element this module draws has an id that starts `mm:` (a node's box `mm:<id>:box`, its words `mm:<id>:text`, the
line to its parent `mm:<id>:edge`), and the frame `mm:frame` keeps in its customData what was drawn last (the base),
so `sync` can tell a person's edit on the canvas from an edit in the file. Anything else on the canvas is the
person's: kept on every render, unless `sync` took it into the file (a box joined to the map by an arrow).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "excalidraw-studio" / "scripts"))     # excalidraw-studio's draw.py
from draw import GREY, INK, KEY, T_FRAME, T_SMALL, Drawing  # noqa: E402
import mmtree as MT  # noqa: E402

SIZE = {0: 48, 1: 36, 2: 30}          # a node's words by depth; 28 px below (principle 7: none a detail)
DEEP, NOTE = 28, 22
MAXW = {0: 600, 1: 520}               # a box's words wrap at this width; 820 px for a leaf's longer line
LEAFW, MINW = 820, 360
PADX, PADY, HGAP, VGAP, LEFT, TOP = 26, 14, 160, 22, 60, 180
FIT_W, FIT_H = 2800 - 2 * LEFT, 1600 - TOP - 60   # principle 1: the frame within 2800 x 1600 when the tree allows
SHAPES = ("rectangle", "ellipse", "diamond")


class Conflict(Exception):
    """An edit made on both sides; `items` names each: (id, what, the file's side, the canvas's side)."""

    def __init__(self, items):
        super().__init__("; ".join(f"{i}: {w}" for i, w, *_ in items))
        self.items = items


def norm(s) -> str:
    return " ".join(str(s or "").split())


# ── draw ───────────────────────────────────────────────────────────────────────────────────────────────────
def _size(depth):
    return SIZE.get(depth, DEEP)


def layout(mm: MT.MindMap) -> dict:
    """{id: (x, y, w, h, depth, wrapped words, note lines)}: columns by depth, each parent centred on its children.
    A tree too wide for one screen wraps its words narrower; one too tall stands its boxes closer."""
    maxw, gap = dict(MAXW), VGAP
    for _ in range(8):
        at, width, height = _layout(mm, maxw, gap)
        if width <= FIT_W and height <= FIT_H:
            break
        if width > FIT_W:
            widest = max(range(max(v[4] for v in at.values()) + 1), key=lambda d: maxw.get(d, LEAFW))
            if maxw.get(widest, LEAFW) <= MINW:
                break
            maxw[widest] = max(MINW, int(maxw.get(widest, LEAFW) * 0.85))
        elif width < FIT_W - 240 and maxw.get(deep := max(v[4] for v in at.values()), LEAFW) < 1200:
            maxw[deep] = maxw.get(deep, LEAFW) + 160    # room to the right: the leaves' lines grow longer, fewer
        elif gap > 10:
            gap = 10
        else:
            break
    return at


def _layout(mm: MT.MindMap, maxws: dict, VGAP: int) -> tuple:
    info, colw = {}, {}
    for n, _p, d, _k in MT.walk(mm.root):
        size, maxw = _size(d), maxws.get(d, LEAFW)
        words = Drawing.wrap(MT.display(n.text) or " ", maxw, size)
        w = max(Drawing.measure(ln, size) for ln in words.split("\n")) + 2 * PADX + 4
        h = len(words.split("\n")) * size * 1.25 + 2 * PADY
        note = Drawing.wrap(" ".join(n.note), maxw, NOTE) if n.note and d else ""
        nh = (len(note.split("\n")) * NOTE * 1.25 + 8) if note else 0
        info[n.id] = [0, 0, w, h, d, words, note, nh]
        colw[d] = max(colw.get(d, 0), w)
    xs = {0: LEFT}
    for d in range(1, max(colw) + 1):
        xs[d] = xs[d - 1] + colw[d - 1] + HGAP
    span = {}

    def height(n):
        own = info[n.id][3] + info[n.id][7]
        kids = sum(height(c) for c in n.children) + VGAP * max(0, len(n.children) - 1)
        span[n.id] = max(own, kids)
        return span[n.id]

    def place(n, top):
        i = info[n.id]
        i[0] = xs[i[4]]
        own = i[3] + i[7]
        if not n.children:
            i[1] = top + (span[n.id] - own) / 2
            return
        kids = sum(span[c.id] for c in n.children) + VGAP * (len(n.children) - 1)
        y = top + (span[n.id] - kids) / 2
        for c in n.children:
            place(c, y)
            y += span[c.id] + VGAP
        first, last = info[n.children[0].id], info[n.children[-1].id]
        mid = (first[1] + first[3] / 2 + last[1] + last[3] / 2) / 2
        i[1] = min(max(mid - i[3] / 2, top), top + span[n.id] - own)

    height(mm.root)
    place(mm.root, TOP)
    return {k: tuple(v) for k, v in info.items()}, xs[max(colw)] + colw[max(colw)] - LEFT, span["root"]


def draw(mm: MT.MindMap, title_note: str = "") -> list:
    """The canvas's own elements for one file, ids `mm:…`; the frame keeps the base for `sync`."""
    at = layout(mm)
    title = MT.display(mm.meta.get("title") or mm.root.text)
    right = max(x + w for x, _y, w, *_ in at.values())
    bottom = max(y + h + nh for _x, y, _w, h, _d, _t, _n, nh in at.values())
    width = max(right + LEFT, Drawing.measure(title, T_FRAME) + 760, 1600)
    height = max(bottom + 60, 900)
    d = Drawing()
    f = d.frame(f"① {title}: the mind map", width, height)
    f["id"] = d.fid = "mm:frame"
    d.text(40, 22, f"🧠 {title}", T_FRAME)["id"] = "mm:title"
    if title_note:                                     # a line under the title only when asked: small words count
        d.text(40, 110, title_note, T_SMALL, GREY)["id"] = "mm:sub"     # against principle 7
    boxes = {}
    for n, p, depth, _k in MT.walk(mm.root):
        x, y, w, h, _d, words, note, _nh = at[n.id]
        b = d.key(x, y, w, h, 4) if p is None else d.box(x, y, w, h, INK, 2.5 if depth == 1 else 1.5)
        b.update(id=f"mm:{n.id}:box", customData={"mindmap": n.id})
        t = d.text(x + PADX, y + PADY, words, _size(depth))
        t.update(id=f"mm:{n.id}:text", containerId=b["id"], originalText=MT.display(n.text), verticalAlign="middle")
        b["boundElements"] = [{"type": "text", "id": t["id"]}]
        boxes[n.id] = b
        if note:
            d.text(x + 4, y + h + 8, note, NOTE, GREY)["id"] = f"mm:{n.id}:note"
        if p is not None:
            pb = boxes[p.id]
            px, py, cy = pb["x"] + pb["width"], pb["y"] + pb["height"] / 2, y + h / 2
            mx = x - HGAP / 2
            pts = [(px, py), (mx, py), (mx, cy), (x, cy)] if abs(py - cy) > 1 else [(px, py), (x, cy)]
            e = d.line(pts, INK, arrow=True, sw=2.5 if depth == 1 else 1.8)
            e.update(id=f"mm:{n.id}:edge", endArrowhead=None,
                     startBinding={"elementId": pb["id"], "focus": 0, "gap": 1},
                     endBinding={"elementId": b["id"], "focus": 0, "gap": 1})
            pb["boundElements"].append({"type": "arrow", "id": e["id"]})
            b["boundElements"].append({"type": "arrow", "id": e["id"]})
    f["customData"] = {"mindmap": {"version": 1, "base": MT.flat(mm)}}
    d.badge(f)                                         # ⑥ ⑦: its words, measured, in the corner
    k = 0
    for e in d.els:
        if not str(e["id"]).startswith("mm:"):
            e["id"], k = f"mm:x{k}", k + 1
    return d.els


def load_doc(path: Path) -> dict:
    path = Path(path)
    if not path.is_file():
        return {"type": "excalidraw", "version": 2, "elements": [], "files": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, els: list, absorbed: set = frozenset()) -> dict:
    """The canvas: this build's elements, then every element of the person's not taken into the file."""
    old = load_doc(path)
    gone = set(absorbed)
    gone |= {e["id"] for e in old["elements"] if e.get("containerId") in gone}
    kept = [e for e in old["elements"] if not str(e["id"]).startswith("mm:") and e["id"] not in gone
            and not e.get("isDeleted")]
    keep = {e["id"] for e in kept}
    mine = {e["id"]: e for e in els}
    for e in old["elements"]:                          # a person's arrow still bound to a box keeps its binding
        if e["id"] in mine:
            for b in e.get("boundElements") or []:
                if b.get("id") in keep and b not in mine[e["id"]]["boundElements"]:
                    mine[e["id"]]["boundElements"].append(b)
    used = {e.get("fileId") for e in kept if e.get("fileId")}
    doc = {"type": "excalidraw", "version": 2, "source": "haipipe-mindmap", "elements": els + kept,
           "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
           "files": {k: v for k, v in (old.get("files") or {}).items() if k in used}}
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(doc, ensure_ascii=False, indent=1))
    return doc


# ── read the canvas back ───────────────────────────────────────────────────────────────────────────────────
def base_of(doc: dict) -> dict | None:
    f = next((e for e in doc.get("elements", []) if e.get("id") == "mm:frame" and not e.get("isDeleted")), None)
    return ((f or {}).get("customData") or {}).get("mindmap", {}).get("base")


def _inside(pt, e, pad=12):
    return e["x"] - pad <= pt[0] <= e["x"] + e["width"] + pad and e["y"] - pad <= pt[1] <= e["y"] + e["height"] + pad


def read(doc: dict) -> dict:
    """The tree the canvas shows now, against its base: {"flat": {id: {text, parent, order}}, "new": {temp id:
    shape id}, "absorbed": element ids a sync takes into the file}. None when the canvas holds no base."""
    base = base_of(doc)
    if base is None:
        return None
    els = [e for e in doc["elements"] if not e.get("isDeleted")]
    by = {e["id"]: e for e in els}
    label = {e["containerId"]: norm(e.get("originalText") or e.get("text")) for e in els
             if e.get("type") == "text" and e.get("containerId") in by}
    node_of = {}                                       # shape id -> node id (or "new:<shape id>")
    for e in els:
        m = re.fullmatch(r"mm:(.+):box", str(e["id"]))
        if m and m.group(1) in base and (label.get(e["id"]) or m.group(1) == "root"):
            node_of[e["id"]] = m.group(1)
    for e in els:                                      # a person's box or words: a node only once joined
        if str(e["id"]).startswith("mm:"):
            continue
        if e.get("type") in SHAPES and label.get(e["id"]):
            node_of[e["id"]] = "new:" + e["id"]
        elif e.get("type") == "text" and not e.get("containerId") and norm(e.get("text")):
            node_of[e["id"]] = "new:" + e["id"]
            label[e["id"]] = norm(e.get("originalText") or e.get("text"))
    shapes = [by[s] for s in node_of]

    def end_of(a, which):
        bind = a.get("startBinding" if which == 0 else "endBinding") or {}
        if bind.get("elementId") in node_of:
            return node_of[bind["elementId"]]
        pts = a.get("points") or [[0, 0]]
        p = pts[0] if which == 0 else pts[-1]
        pt = (a["x"] + p[0], a["y"] + p[1])
        hits = sorted((s for s in shapes if _inside(pt, s)), key=lambda s: s["width"] * s["height"])
        return node_of[hits[0]["id"]] if hits else None

    parent, used = {}, {}
    arrows = sorted((e for e in els if e.get("type") in ("arrow", "line")), key=lambda e: str(e["id"]).startswith("mm:"))
    for a in arrows:                                   # a person's arrow first: it says what they meant now
        s, t = end_of(a, 0), end_of(a, 1)
        if s and t and s != t and t != "root" and t not in parent:
            parent[t] = s
            used[t] = a["id"]
    present = set(node_of.values())

    def up(nid):                                       # a node with no line in: its base parent, or the nearest
        p = base[nid]["parent"]                        # one still on the canvas
        while p is not None and p not in present:
            p = base[p]["parent"]
        return p or "root"

    for nid in present:
        if not nid.startswith("new:") and nid != "root" and nid not in parent:
            parent[nid] = up(nid)
    for nid in list(parent):                           # no loops; a new box must hang from the map
        seen, p = {nid}, parent.get(nid)
        while p and p != "root" and p not in seen:
            seen.add(p)
            p = parent.get(p)
        if p != "root":
            if nid.startswith("new:"):
                parent.pop(nid)
            else:
                parent[nid] = up(nid)
                used.pop(nid, None)
    nodes = {"root"} | set(parent)
    shape = {v: by[k] for k, v in node_of.items()}
    kids = {}
    for nid in nodes - {"root"}:
        kids.setdefault(parent[nid], []).append(nid)
    out = {"root": {"text": label.get("mm:root:box") or base["root"]["text"], "parent": None, "order": 0}}
    for p, cs in kids.items():
        cs.sort(key=lambda c: (shape[c]["y"] + shape[c]["height"] / 2, shape[c]["x"]))
        for k, c in enumerate(cs):
            out[c] = {"text": label[next(s for s, v in node_of.items() if v == c)], "parent": p, "order": k}
    new = {nid: nid[4:] for nid in out if nid.startswith("new:")}
    absorbed = set(new.values()) | {a for t, a in used.items() if not str(a).startswith("mm:")}
    return {"flat": out, "new": new, "absorbed": absorbed}


# ── compare and merge ──────────────────────────────────────────────────────────────────────────────────────
def changes(base: dict, side: dict) -> dict:
    """What one side changed since the base: words, deletions, moves, new order under a parent, additions."""
    ch = {"text": {}, "deleted": set(), "moved": {}, "order": {}, "added": set()}
    for i, b in base.items():
        s = side.get(i)
        if s is None:
            if i != "root":
                ch["deleted"].add(i)
            continue
        if norm(s["text"]) != norm(b["text"]):
            ch["text"][i] = s["text"]
        if s["parent"] != b["parent"]:
            ch["moved"][i] = s["parent"]
    ch["added"] = {i for i in side if i not in base}
    for p in {b["parent"] for b in base.values()} - {None}:
        both = [i for i in base if base[i]["parent"] == p and i in side and side[i]["parent"] == p]
        was = sorted(both, key=lambda i: base[i]["order"])
        now = sorted(both, key=lambda i: side[i]["order"])
        if was != now:
            ch["order"][p] = now
    return ch


def any_change(ch: dict) -> bool:
    return any(ch[k] for k in ch)


def conflicts(md: dict, cv: dict, md_flat: dict, cv_flat: dict) -> list:
    out = []
    for i, t in cv["text"].items():
        if i in md["deleted"]:
            out.append((i, "words changed on the canvas, node deleted in the file", "deleted", t))
        elif i in md["text"] and norm(md_flat[i]["text"]) != norm(t):
            out.append((i, "words changed on both sides", md_flat[i]["text"], t))
    for i in cv["deleted"]:
        if i in md["text"] or i in md["moved"]:
            out.append((i, "deleted on the canvas, changed in the file", md_flat[i]["text"], "deleted"))
    for i, p in cv["moved"].items():
        if i in md["deleted"]:
            out.append((i, "moved on the canvas, deleted in the file", "deleted", f"under {p}"))
        elif i in md["moved"] and md["moved"][i] != p:
            out.append((i, "moved on both sides", f"under {md['moved'][i]}", f"under {p}"))
    for p, order in cv["order"].items():
        if p in md["order"] and md["order"][p] != order:
            out.append((p, "children reordered on both sides", " · ".join(md["order"][p]), " · ".join(order)))
    for i in cv["added"]:
        p = cv_flat[i]["parent"]
        if p in md["deleted"]:
            out.append((i, f"added on the canvas under {p}, which the file deleted", "deleted", cv_flat[i]["text"]))
    return out


def merge(mm: MT.MindMap, base: dict, seen: dict, take: dict | None = None) -> dict:
    """Apply the canvas's edits (`seen`, from read) to the file's tree, in place. An edit made on both sides raises
    Conflict unless `take` picks a side: {"*": "file"|"canvas", "<id>": ...}. Returns counts and the new ids."""
    take = take or {}
    md_flat, cv_flat = MT.flat(mm), seen["flat"]
    md, cv = changes(base, md_flat), changes(base, cv_flat)
    items = conflicts(md, cv, md_flat, cv_flat)
    pick = lambda i: take.get(i) or take.get("*")
    open_ = [c for c in items if pick(c[0]) not in ("file", "canvas")]
    if open_:
        raise Conflict(open_)
    skip = {c[0] for c in items if pick(c[0]) == "file"}
    fresh = MT.next_ids(set(md_flat) | set(base))
    ids = {i: (next(fresh) if i.startswith("new:") else i) for i in cv_flat}
    nodes = {n.id: n for n, *_ in MT.walk(mm.root)}
    done = {"words": 0, "added": 0, "deleted": 0, "moved": 0, "reordered": 0}

    def detach(n):
        for p in nodes.values():
            if n in p.children:
                k = p.children.index(n)
                p.children.remove(n)
                return p, k
        return None, 0

    for i, t in cv["text"].items():
        if i not in skip and i in nodes:
            nodes[i].text = t
            done["words"] += 1
    for i in sorted(cv["added"], key=lambda i: _depth(cv_flat, i)):
        p = cv_flat[i]["parent"]
        if i in skip or ids[p] not in nodes:
            continue
        nodes[ids[i]] = MT.Node(ids[i], cv_flat[i]["text"])
        nodes[ids[p]].children.append(nodes[ids[i]])
        done["added"] += 1
    for i, p in cv["moved"].items():
        if i in skip or i not in nodes or ids.get(p, p) not in nodes:
            continue
        detach(nodes[i])
        nodes[ids.get(p, p)].children.append(nodes[i])
        done["moved"] += 1
    for i in cv["deleted"]:
        if i in skip or i not in nodes:
            continue
        p, k = detach(nodes[i])
        if p is not None:
            p.children[k:k] = nodes[i].children        # what only the file holds under it moves up
        nodes.pop(i)
        done["deleted"] += 1
    placed = {cv_flat[i]["parent"] for i in cv["added"] | set(cv["moved"]) if i not in skip} | \
             {p for p in cv["order"] if p not in skip}
    for p in placed:
        node = nodes.get(ids.get(p, p))
        if node is None:
            continue
        rank = {ids[c]: cv_flat[c]["order"] for c in cv_flat if cv_flat[c]["parent"] == p}
        slots = [k for k, c in enumerate(node.children) if c.id in rank]
        ordered = sorted((node.children[k] for k in slots), key=lambda c: rank[c.id])
        if [c.id for c in ordered] != [node.children[k].id for k in slots]:
            done["reordered"] += 1
        for k, c in zip(slots, ordered):
            node.children[k] = c
    done["conflicts taken"] = len(items)
    return done


def _depth(fl, i):
    d = 0
    while fl[i]["parent"] is not None and d < 99:
        i, d = fl[i]["parent"], d + 1
    return d
