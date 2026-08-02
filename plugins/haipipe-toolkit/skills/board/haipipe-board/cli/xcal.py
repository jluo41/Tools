#!/usr/bin/env python3
"""board.md + the pages' ASCII figures -> ONE `fig/board.excalidraw` (QA4a).

    python xcal.py <board-folder>            regenerate fig/board.excalidraw
    python xcal.py <board-folder> --wire     ... and put each frame's URL in its
                                             page's ## Diagram

ONE excalidraw per board, one FRAME per page (JL 260726). Never a file per page:
a single surface is the only thing that can say how the pages RELATE, which is
the whole argument for drawing at all. A page's Diagram opens at its own frame
through `serve.py`'s `?frame=<ID>` projection; the file on disk is one scene.

Each frame is SEEDED with the ASCII figure that page already has in its
`## Diagram`, as one monospace text element. A frame holding nothing is a blank
box that tells the reader the feature is broken (JL 260726, on opening QB3 and
finding an empty rectangle), and a seeded one gives them something to redraw.
The ASCII stays the truth on the page: this is a one-way seed, not a source.

IDs ARE STABLE — `frame-QA4a`, `t-QA4a-fig` — so regenerating is not a re-share:
nothing renames, no page's link dies. That is the acceptance bar QA4a set, and
it is what makes the two rules below possible.

TWO THINGS THIS WILL NOT TOUCH, so a regen never eats work someone did:
  · any element whose id this script did not mint is KEPT (a human's drawing)
  · a frame that already exists KEEPS its x/y (a human's layout)
Only new frames are placed by the layout below.
"""
import argparse
import json
import re
import sys
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.common import sec                      # noqa: E402
from src.parse import parse_dir                 # noqa: E402

FIG_SIZE = 12          # monospace, the figure
FIG_CW, FIG_LH = 7.3, 15.0
TITLE_SIZE = 18
GROUP_SIZE = 28
PAD_X, PAD_TOP, PAD_BOT = 24, 56, 24
MIN_W, MIN_H = 360, 220
GAP_X, GAP_Y = 90, 190       # the vertical gap leaves room for the group label


def stable(*parts):
    """deterministic small int from an id, so a regen produces no git noise"""
    return zlib.crc32("·".join(parts).encode()) % 2_000_000_000


def base(el_id, kind, x, y, w, h, frame=None):
    return {
        "id": el_id, "type": kind, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": "#1e1e1e", "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 1, "opacity": 100, "groupIds": [], "frameId": frame,
        "roundness": None, "seed": stable(el_id, "seed"), "version": 1,
        "versionNonce": stable(el_id, "nonce"), "isDeleted": False,
        "boundElements": None, "updated": 1, "link": None, "locked": False,
    }


def text(el_id, s, x, y, size, mono, frame=None, color="#1e1e1e"):
    lines = s.split("\n")
    cw = FIG_CW if mono else size * 0.55
    lh = 1.25
    el = base(el_id, "text", x, y,
              round(max(len(l) for l in lines) * (cw if mono else cw), 1),
              round(len(lines) * size * lh, 1), frame)
    el.update({
        "text": s, "originalText": s, "fontSize": size,
        "fontFamily": 3 if mono else 2, "textAlign": "left",
        "verticalAlign": "top", "containerId": None, "lineHeight": lh,
        "strokeColor": color,
    })
    return el


def figure_of(page):
    """that page's ## Diagram ASCII figure — the first fenced block, verbatim.

    Only ## Diagram: a fenced block under ## Content belongs to a paragraph's
    argument, not to the page's picture of itself."""
    d = sec(page.get("sec", {}), "Diagram")
    if not d:
        return ""
    m = re.search(r"^```[^\n]*\n(.*?)^```", d, re.S | re.M)
    return m.group(1).rstrip("\n") if m else ""


def build(folder, root, fresh=False):
    meta, pages, _ = parse_dir(folder)
    pages = [p for p in pages if p.get("file")]
    # The scene sits at the Board root, beside board.md and generated board/, because
    # it is a first-class citizen of the board rather than one of its figures
    # (JL 260729). Boards opened before that keep theirs under fig/, so an
    # existing fig/ scene is used where it lies: migrating it is that board
    # owner's call, and forking the scene in two would lose whichever half the
    # editor did not open.
    out = folder / "board.excalidraw"
    legacy = folder / "fig" / "board.excalidraw"
    if legacy.exists() and not out.exists():
        out = legacy

    old = {}
    if out.exists() and not fresh:
        try:
            old = {e["id"]: e for e in json.loads(
                out.read_text(encoding="utf-8")).get("elements", [])}
        except Exception as e:
            sys.exit(f"{out} exists and is not a scene: {e}")

    # group -> its pages, in board.md's ## Pages order
    groups, order = {}, []
    for p in pages:
        g = p.get("group") or "·"
        if g not in groups:
            groups[g], _ = [], order.append(g)
        groups[g].append(p)

    mine, seeded, kept_xy = [], 0, 0
    y = 0.0
    for gi, g in enumerate(order):
        row = []
        for p in groups[g]:
            f = figure_of(p)
            if f:
                seeded += 1
            lines = f.split("\n") if f else []
            w = max(MIN_W, round(max((len(l) for l in lines), default=0)
                                 * FIG_CW) + 2 * PAD_X)
            h = max(MIN_H, round(len(lines) * FIG_LH) + PAD_TOP + PAD_BOT)
            row.append((p, f, w, h))
        rh = max(h for *_, h in row)

        mine.append(text(f"t-group-{gi}", g, 0, y - 52, GROUP_SIZE, False,
                         color="#6a5acd"))
        x = 0.0
        for p, f, w, h in row:
            pid = p["id"]
            fid = f"frame-{pid}"
            fx, fy = x, y
            if fid in old:                       # a human may have moved it
                fx, fy = old[fid].get("x", x), old[fid].get("y", y)
                kept_xy += 1
            fr = base(fid, "frame", fx, fy, w, rh)
            fr.update({"name": pid, "strokeColor": "#bbb"})
            mine.append(fr)
            mine.append(text(f"t-{pid}-title", f"{pid} · {p['title']}",
                             fx + PAD_X, fy + 16, TITLE_SIZE, False, fid,
                             color="#4a4a6a"))
            mine.append(text(f"t-{pid}-fig",
                             f or "(this page has no ASCII figure yet)",
                             fx + PAD_X, fy + PAD_TOP, FIG_SIZE, True, fid,
                             color="#1e1e1e" if f else "#999"))
            x += w + GAP_X
        y += rh + GAP_Y

    # Excalidraw ENRICHES what it loads: it adds `index` (the z-order), `autoResize`,
    # `boundElements`, and bumps version/versionNonce/updated. If a regen wrote its
    # plainer version back, the next person to open the editor would save that
    # normalisation again, so `xcal.py` and the browser would each dirty the file in
    # turn forever. So: when the generated element says nothing new, keep the one
    # already on disk, whatever the app has since added to it.
    # `boundElements` is in here because the app rewrites our null to [], and a
    # real binding it later records is the app's to own, not this script's.
    VOLATILE = {"version", "versionNonce", "updated", "boundElements"}
    same = 0
    for i, e in enumerate(mine):
        o = old.get(e["id"])
        if o and all(o.get(k) == v for k, v in e.items() if k not in VOLATILE):
            mine[i] = o
            same += 1

    # Anything this script mints is prefixed; Excalidraw's own ids are random,
    # so the prefix is what tells a human's drawing from ours. Without it a
    # RETIRED page's frame would survive every regen as if a human had drawn
    # it, which is exactly the dead frame QA4a said must not be left behind.
    ids = {e["id"] for e in mine}
    human = [e for e in old.values()
             if e["id"] not in ids and not re.match(r"^(?:frame-|t-)", e["id"])]
    stale = [e for e in old.values()
             if e["id"] not in ids and re.match(r"^(?:frame-|t-)", e["id"])]
    dropped = sorted({e.get("name") or e["id"] for e in stale if e["type"] == "frame"})
    out.write_text(json.dumps({
        "type": "excalidraw", "version": 2, "source": "haipipe-board/xcal.py",
        "elements": mine + human,
        "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
        "files": {},
    }, indent=1), encoding="utf-8")

    rel = out.resolve().relative_to(root.resolve()).as_posix()
    host = (meta.get("excalidraw") or "").rstrip("/")
    print(f"{out.relative_to(folder)} · {len(mine)} elements · "
          f"{len(groups)} groups · {len([p for p in pages])} frames")
    print(f"   seeded with an ASCII figure : {seeded}/{len(pages)}")
    print(f"   kept a human's frame position: {kept_xy}")
    print(f"   kept a human's element       : {len(human)}")
    print(f"   unchanged, left exactly as-is: {same}/{len(mine)}")
    if dropped:
        print(f"   dropped the frame of a page that is gone: {', '.join(dropped)}")
    # A kept position and a recomputed width can collide: a page whose figure
    # grew widens its frame in place, into whatever sits to its right.
    frames = [e for e in mine if e["type"] == "frame"]
    hits = [(a["name"], b["name"]) for i, a in enumerate(frames) for b in frames[i + 1:]
            if a["x"] < b["x"] + b["width"] and b["x"] < a["x"] + a["width"]
            and a["y"] < b["y"] + b["height"] and b["y"] < a["y"] + a["height"]]
    if hits:
        print(f"   ! {len(hits)} overlapping frame pair(s): "
              f"{', '.join(f'{a}/{b}' for a, b in hits[:4])}"
              f"{' …' if len(hits) > 4 else ''}")
        print("     a figure outgrew its frame's kept position; "
              "`--fresh` relayouts (and drops anything drawn)")
    return meta, pages, rel, host


# an excalidraw URL sitting alone on a line — NOT `\s*`, which spans newlines
# and so swallows the blank lines around it (found 260726, after one run left 28
# pages with `## Aims` welded to the URL above it)
XURL = re.compile(r"^[ \t]*(https?://[^\s]*excalidraw[^\s]*)[ \t]*$\n?", re.M)


def wire(folder, pages, rel, host, port):
    """put each frame's URL in its page's ## Diagram, replacing any older one.

    Rebuilds the section rather than splicing: every old excalidraw line comes
    out, the new one goes on the end with one blank line either side. Same
    result whatever shape the page was in, which is the only way this stays
    safe to re-run."""
    if not host:
        sys.exit("board.md has no `excalidraw:` line, so there is no host to "
                 "compose a URL from")
    n_rep = n_add = n_new = 0
    theirs = []
    for p in pages:
        f = folder / p["file"]
        txt = f.read_text(encoding="utf-8")
        # NOT `#url=`: that loader always asks to "Replace my content" and saves
        # to the browser, so switching pages threw the drawing away (JL 260726).
        # `?board=&frame=` is read by the injected boot script instead, which
        # seeds the editor from the file and writes back to it.
        # ROOT-RELATIVE on purpose. An absolute `http://127.0.0.1:5599/…` is
        # correct only for a reader sitting on the serving machine: open the same
        # board over a tunnel or a tailnet address and all 28 embeds point at the
        # READER'S own loopback, where nothing is listening (JL 260726). A leading
        # `/` resolves against whatever host the board was loaded from, so the
        # page stops caring where it is being served.
        url = f"{host}/?board={rel}&frame={p['id']}"
        if len(re.findall(r"^## Diagram\s*$", txt, re.M)) > 1:
            print(f"   ! {p['file']} has more than one ## Diagram; "
                  "merge them by hand, this only writes into the first")
        # `[ \t]*$\n?` and not `\s*$`: the second spans blank lines, so group(1)
        # starts at a place that depends on how the page was spaced
        m = re.search(r"^## Diagram[ \t]*$\n?(.*?)(?=^## |\Z)", txt, re.S | re.M)
        if not m:
            # on-stage order (QA4): Diagram sits after Question/Boundary and
            # before everything else, so anchor on the first section that is
            # allowed to follow it. Not `## Content` alone: a short page may
            # have none, and two did (QB5, QC3).
            anchor = re.search(r"^## (?:Content|Aims|Items to Finish|Done when|"
                               r"States|State|Where we are|Now|Files)\s*$", txt, re.M)
            if not anchor:
                print(f"   ! {p['file']} has no section to put a Diagram before")
                continue
            txt = (txt[:anchor.start()] + "## Diagram\n\n" + url + "\n\n"
                   + txt[anchor.start():])
            n_new += 1
        else:
            # A page may deliberately hold a link to somebody ELSE'S excalidraw,
            # pasted by hand from the page itself (QD7). That is a human's work
            # in exactly the sense the scene rules protect, so leave it: this
            # command wires a page to ITS frame, it does not claim the section.
            # "Ours" is decided by what the URL POINTS AT, not by how it is
            # spelled. A url that names this board's own scene is ours however it
            # was written: `#url=http://127.0.0.1:5599/…/board.excalidraw`, the
            # absolute `?board=` form, or the root-relative one. Testing the host
            # prefix alone was wrong the moment the host changed, and it silently
            # refused to migrate all 28 pages (260726).
            held = [u.strip() for u in XURL.findall(m.group(1))]
            def mine(u):
                return u.startswith(host + "/") or rel in u
            if any(not mine(u) for u in held):
                theirs.append(p["file"])
                continue
            body, n = XURL.subn("", m.group(1))
            n_rep += bool(n)
            n_add += not n
            body = body.strip("\n")
            body = "\n" + (body + "\n\n" if body else "") + url + "\n\n"
            txt = txt[:m.start(1)] + body + txt[m.end(1):]
        f.write_text(txt, encoding="utf-8")
    print(f"   ## Diagram: replaced {n_rep} · appended {n_add} · created {n_new}")
    if theirs:
        print(f"   left alone, holds an excalidraw that is not this board's: "
              f"{', '.join(theirs)}")


def find_root(start):
    for d in [start, *start.parents]:
        if (d / "pyproject.toml").exists():
            return d
    return start


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", type=Path)
    ap.add_argument("--root", type=Path, default=None,
                    help="what serve.py serves; default = nearest pyproject.toml")
    ap.add_argument("--port", type=int, default=5599)
    ap.add_argument("--wire", action="store_true",
                    help="also put each frame's URL in its page's ## Diagram")
    ap.add_argument("--fresh", action="store_true",
                    help="ignore the existing scene: relayout every frame and "
                         "DROP anything a human drew. Needed when the layout "
                         "itself changes; destructive, so it is never default.")
    a = ap.parse_args()
    folder = a.folder.resolve()
    root = (a.root or find_root(folder)).resolve()
    meta, pages, rel, host = build(folder, root, a.fresh)
    if a.wire:
        wire(folder, pages, rel, host, a.port)
