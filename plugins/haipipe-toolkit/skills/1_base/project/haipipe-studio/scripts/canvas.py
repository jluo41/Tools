"""Write a seeded drawing without losing what a person drew on it.

A builder draws its elements; write() gives each a stable id from its content, then merges
with the canvas on disk using a snapshot of what the builder drew last time
(`<folder>/.<name>.seed.json`, beside the drawing), not Excalidraw's version numbers (a save re-stamps them all):

  - an element with a non-seed id (anything the person added)       kept
  - a seed element whose content differs from the last snapshot     kept: the person edited it
  - a seed element in the last snapshot but gone from the canvas    stays gone: the person deleted it
    (unless the canvas is a stale copy from an older build: then it is redrawn)
  - every other seed element                                        redrawn from this build

The snapshot keeps the last 8 builds: a seed element that matches any of them was not edited
by the person (an open editor tab may save a copy from an older build). `redraw_frames` names
frames whose seed elements are always redrawn (a frame still being designed).

Frames are layout, and the builder owns layout: a frame moved by hand is put back where the
build places it, and moving it is not an edit of what it holds. A seed element is compared
relative to its frame, and everything kept in a frame (the person's marks, their edits) moves
with that frame to its new place.

The first build after this module exists has no snapshot: the seed elements on the canvas
are taken as the snapshot (nothing counts as edited).

haipipe-studio's merge-safe writer (moved here from b03 studio/_build/ on 261007). A builder adds this
folder to sys.path, imports it as `canvas` and calls `canvas.write(out, els, source)`.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path

# the studio palette (JL 261007: "the tree and lines with box with no much colors, just the color of black,
# with red for uncertainty questions, and green for our previous changes")
INK = "#1e1e1e"        # every line, box, tree and word
RED = "#e03131"        # an uncertain or open question
GREEN = "#2f9e44"      # a change note: what changed, where it changed
PALETTE = (INK, RED, GREEN)
# inside a slide of a slide draft only (s61-s69): one accent marks the slide's key thing, a muted gray its
# caption (JL 261007: "make the slide to be a bit colorful by highlight the important things")
# (owned by excalidraw-slide's slide_kit since 261007; kept here, the same values, for builders that read them
# from canvas)
ACCENT, ACCENT_FILL, MUTED = "#1971c2", "#d0ebff", "#868e96"
SLIDE_PALETTE = (ACCENT, MUTED)


def off_palette(els, slides=False):
    """The elements drawn in a colour outside the studio palette (a stroke not black, red or green, or
    any fill): a builder can print these before it writes. `slides=True` (a slide draft) also allows the
    slide accent, its light fill and the muted caption gray."""
    strokes = PALETTE + (SLIDE_PALETTE if slides else ())
    fills = ("transparent", "#ffffff", "") + ((ACCENT_FILL,) if slides else ())
    return [e for e in els if str(e.get("strokeColor", INK)).lower() not in strokes
            or str(e.get("backgroundColor", "transparent")).lower() not in fills]


def apply_palette(els):
    """The studio look applied to what a builder drew (JL 261007, "Recolour all"): a stroke outside
    black · red · green becomes black (a transparent one stays), a fill becomes transparent (white
    stays). An image keeps its stroke, fill and picture. Returns how many elements changed."""
    n = 0
    for e in els:
        if e.get("type") == "image":
            continue
        stroke, fill = str(e.get("strokeColor", INK)).lower(), str(e.get("backgroundColor", "transparent")).lower()
        if stroke not in PALETTE + ("transparent", ""):          # an invisible stroke stays invisible
            e["strokeColor"] = INK
            n += 1
        if fill not in ("transparent", "#ffffff", ""):
            e["backgroundColor"] = "transparent"
            n += 1
    return n


def is_slide_draft(out):
    """A slide draft (s61-s69) keeps its slide colours (JL 261007: "but for the slide draft, maybe not")."""
    return bool(__import__("re").match(r"^s6\d\b|^s6\d-", Path(out).stem))


def change_note(x, y, what, date=None, frame=None, size=16):
    """A short green note `✎ <YYMMDD> <what changed>`, a text element to place beside the thing that
    changed; list the same words in the title frame. `date` defaults to today."""
    import datetime as _dt
    text = f"✎ {date or _dt.date.today().strftime('%y%m%d')} {what}"
    return {"id": f"note-{x}-{y}", "type": "text", "x": x, "y": y, "width": len(text) * size * 0.55,
            "height": size * 1.25, "angle": 0, "strokeColor": GREEN, "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid", "roughness": 1, "opacity": 100,
            "groupIds": [], "frameId": frame, "roundness": None, "seed": 1, "version": 1, "versionNonce": 1,
            "isDeleted": False, "boundElements": [], "updated": 1, "link": None, "locked": False, "text": text,
            "originalText": text, "fontSize": size, "fontFamily": 1, "textAlign": "left",
            "verticalAlign": "top", "containerId": None, "autoResize": True, "lineHeight": 1.25}


KEYS = ("type", "x", "y", "width", "height", "text", "name", "strokeColor", "backgroundColor", "points",
        "fontSize", "fontFamily", "strokeStyle", "angle", "fileId")


def _sig(e):
    out = {}
    for k in KEYS:
        if e.get("type") in ("text", "line", "arrow") and k in ("width", "height"):
            continue                       # Excalidraw re-measures text, and lines from their points
        v = e.get(k)
        if isinstance(v, float):
            v = round(v)
        elif k == "points" and v:
            v = [[round(a), round(b)] for a, b in v]
        out[k] = v
    return out


def assign_ids(els):
    """Content-based ids: the same drawn thing gets the same id on every build. Ids are given by position,
    so two elements a builder gave one id still come out distinct (b11, 261007)."""
    seen, remap, new_ids, dup = Counter(), {}, [], set()
    for e in els:
        if e["type"] == "text":
            desc = f"text|{e['text']}|{e.get('containerId') and 'bound'}"
        elif e["type"] in ("line", "arrow"):
            desc = f"{e['type']}|{round(e['x'])},{round(e['y'])}|{[[round(a), round(b)] for a, b in e['points']]}"
        elif e["type"] == "frame":
            desc = f"frame|{e.get('name')}"
        elif e["type"] == "image":                  # a picture is its file: the same file, the same id
            desc = f"image|{e.get('fileId')}|{round(e['x'])},{round(e['y'])}"
        else:
            desc = f"{e['type']}|{round(e['x'])},{round(e['y'])},{round(e['width'])},{round(e['height'])}"
        seen[desc] += 1
        new_ids.append("s-" + hashlib.sha1(f"{desc}#{seen[desc]}".encode()).hexdigest()[:12])
        if e["id"] in remap:                        # two elements given one id: each still gets its own
            dup.add(e["id"])                        # (by position); a reference to it means the first
        else:
            remap[e["id"]] = new_ids[-1]
    if dup:
        print(f"canvas: {len(dup)} id(s) given to more than one element ({', '.join(sorted(dup)[:3])}): "
              "each gets its own id; give them distinct ids in the builder")
    for e, new in zip(els, new_ids):
        e["id"] = new
        if e.get("containerId"):
            e["containerId"] = remap.get(e["containerId"], e["containerId"])
        if e.get("frameId"):
            e["frameId"] = remap.get(e["frameId"], e["frameId"])
        for b in e.get("boundElements") or []:
            b["id"] = remap.get(b["id"], b["id"])
    return els


def seed_path(out):
    """The snapshot sits beside its drawing, `<folder>/.<stem>.seed.json`: two Blocks' drawings with the
    same name never share one, and a renamed folder takes its snapshot with it (b16, 261007: two
    s11-… drawings in two Blocks read one snapshot and 520 new elements counted as deleted)."""
    return out.resolve().with_name(f".{out.stem}.seed.json")


# folders that may hold an older snapshot by stem, `.<stem>.seed.json`, from before snapshots sat
# beside their drawings: a Block that keeps such snapshots appends that folder
LEGACY_DIRS: list = []


def legacy_seed(out, old):
    """An older snapshot kept in a LEGACY_DIRS folder by stem, used once if it is this drawing's: most
    of its seed ids are on this canvas. Else None, and the canvas's own seeds become the snapshot."""
    legacy = next((Path(d) / f".{out.stem}.seed.json" for d in LEGACY_DIRS
                   if (Path(d) / f".{out.stem}.seed.json").exists()), None)
    if legacy is None or not old:
        return None
    saved = json.loads(legacy.read_text())
    ids = set(saved.get("current", saved))
    on_canvas = {e["id"] for e in old if e["id"].startswith("s-")}
    return saved if ids and len(ids & on_canvas) >= 0.5 * len(ids) else None


def write(out, els, source, redraw_frames=(), files=None, palette=None):
    """`files`: the images this build embeds ({fileId: {mimeType, dataURL, ...}}); the files of the
    person's own kept images stay too. `palette`: apply the studio look (black, red, green) to what this
    build draws; by default on for every drawing but a slide draft (s61-s69). The person's own marks are
    never recoloured."""
    out = Path(out)
    snap_path = seed_path(out)
    if palette if palette is not None else not is_slide_draft(out):
        apply_palette(els)
    assign_ids(els)
    old_doc = json.loads(out.read_text()) if out.exists() else {}
    old = old_doc.get("elements", [])
    saved = json.loads(snap_path.read_text()) if snap_path.exists() else legacy_seed(out, old)
    if saved is None:
        snap, history = {e["id"]: _sig(e) for e in old if e["id"].startswith("s-")}, []
        if old and not snap:                        # a canvas no canvas.write ever wrote (b11, 261007)
            print(f"{out.name}: no seed snapshot and no seed ids on the canvas, so all {len(old)} elements "
                  "on it are kept as a person's marks. If another writer made them, move the drawing aside "
                  "and rebuild, or the drawing doubles")
    elif "current" in saved:
        snap, history = saved["current"], saved.get("history", [])
    else:                                  # an older single-snapshot file
        snap, history = saved, []
    in_frames = set()                      # seed elements of frames this build redraws whole
    for fe in old:
        if fe["type"] == "frame" and fe.get("name") in (redraw_frames or ()):
            in_frames.add(fe["id"])
    in_frames |= {e["id"] for e in old if e.get("frameId") in in_frames}
    on_canvas = {e["id"] for e in old}
    def differs(cur, ref):  # compare only the fields both record (a field may stop being compared)
        return any(abs(cur[k] - v) > 2 if k in ("x", "y") and isinstance(v, (int, float))
                   and isinstance(cur.get(k), (int, float)) else cur.get(k) != v
                   for k, v in ref.items() if k in cur)   # x, y: a frame's move rounds by a pixel

    old_frames = {e["id"]: e for e in old if e["type"] == "frame"}

    def rel(e, ref_snap):   # e's signature with its frame's hand move taken out (the builder owns layout)
        cur = _sig(e)
        if e["type"] == "frame":
            cur.pop("x"), cur.pop("y")
            return cur
        fr, ref_fr = old_frames.get(e.get("frameId")), ref_snap.get(e.get("frameId"))
        if fr and ref_fr and "x" in ref_fr and isinstance(cur.get("x"), int):
            cur["x"] = round(e["x"] - (fr["x"] - ref_fr["x"]))
            cur["y"] = round(e["y"] - (fr["y"] - ref_fr["y"]))
        return cur

    def edited(e):          # differs from this build's last drawing AND from every recent one
        if e["id"] in in_frames:
            return False
        if not differs(rel(e, snap), snap[e["id"]]):
            return False
        return all(differs(rel(e, h), h[e["id"]]) for h in history if e["id"] in h)

    kept = [e for e in old if not e["id"].startswith("s-") or (e["id"] in snap and edited(e) and e["type"] != "frame")]
    new_frames = {e["id"]: e for e in els if e["type"] == "frame"}
    for e in kept:          # what is kept in a frame moves with it, to where this build puts the frame
        fr, to = old_frames.get(e.get("frameId")), new_frames.get(e.get("frameId"))
        if fr and to:
            e["x"] += to["x"] - fr["x"]
            e["y"] += to["y"] - fr["y"]
    taken = {e["id"] for e in kept}
    # A canvas still holding seed elements from an older build is a stale copy (an editor tab
    # open on an old version saved over the last build): its missing elements were never
    # deleted by the person, so redraw them instead of honouring them as deletions.
    stale = any(e["id"].startswith("s-") and e["id"] not in snap for e in old)
    deleted = set() if stale else {i for i in snap if i not in on_canvas}
    if stale:
        print(f"{out.name}: the canvas is older than the last build (an open editor tab saved over it?); "
              "missing seed elements are redrawn, not treated as deletions")
    fresh = [e for e in els if e["id"] not in taken and e["id"] not in deleted]
    used = {e.get("fileId") for e in fresh + kept if e.get("fileId")}
    all_files = {k: v for k, v in {**old_doc.get("files", {}), **(files or {})}.items() if k in used}
    out.write_text(json.dumps({"type": "excalidraw", "version": 2, "source": source, "elements": fresh + kept,
                               "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": all_files},
                              ensure_ascii=False, indent=1))
    history = ([snap] + history)[:8]       # recent builds: a stale copy matches one of them
    snap_path.write_text(json.dumps({"current": {e["id"]: _sig(e) for e in els}, "history": history},
                                    ensure_ascii=False))
    mine = sum(not e["id"].startswith("s-") for e in kept)
    print(f"{out.name}: {len(fresh)} drawn, {mine} of yours kept, {len(kept) - mine} seed edits kept, "
          f"{len(deleted)} deletions respected")
