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
import re
from collections import Counter
from pathlib import Path

# the studio palette (JL 261007: "the tree and lines with box with no much colors, just the color of black,
# with red for uncertainty questions, and green for our previous changes")
INK = "#1e1e1e"        # every line, box, tree and word
RED = "#e03131"        # an uncertain or open question
GREEN = "#2f9e44"      # a change note: what changed, where it changed
PALETTE = (INK, RED, GREEN)
# the one slight fill under a frame's key point (excalidraw-studio, principle 5): part of the studio look, so the
# palette keeps it (found 261012 on b10 s52: a builder writing with the palette on lost every key point)
KEY = "#fff3bf"
# inside a slide of a slide draft only (s61-s69): one accent marks the slide's key thing, a muted gray its
# caption (JL 261007: "make the slide to be a bit colorful by highlight the important things")
# (owned by excalidraw-slide's slide_kit since 261007; kept here, the same values, for builders that read them
# from canvas)
ACCENT, ACCENT_FILL, MUTED = "#1971c2", "#d0ebff", "#868e96"
SLIDE_PALETTE = (ACCENT, MUTED)
# a screen drawn in a studio drawing wears the workbench's own light colours, read from
# servers/workbench/frame.py's CSS (JL 261012: "make the UI to be more colorful, like the same to what we
# see"); the rest of the drawing stays black, red and green. A builder marks the frame with ui_frame().
UI = {"wash": "#f8f9fa", "box": "#ffffff", "line": "#ced4da", "edge": "#adb5bd", "text": "#1c1c1c",
      "mut": "#6f6f6b", "link": "#3e5c84", "on": "#1864ab", "on_bg": "#e7f5ff",
      "new": "#7048e8", "new_bg": "#f3f0ff", "dot": "#3e5c84"}   # dot: the Timeline's bubble, var(--acc) at .8
# a Report group button by its kind, as the workbench colours it (servers/workbench/frame.py --grp-*; b10 s05-D16,
# JL 261012): a box whose customData has ui_kind "fixed" (the theme's, from the Question) or "suggested" (the theme's
# starting group); a Block's own group stays a plain button
UI_KIND = {"fixed": ("#868e96", "#e9ecef"), "suggested": ("#f08c00", "#fff4e6")}
STATUS_UI = {"answered": "#2b8a3e", "done": "#2b8a3e", "sent": "#2b8a3e", "partial": "#e67700",   # a status word
             "draft": "#e67700", "open": "#868e96", "not judged": "#868e96"}
STAGE_UI = {"explore": ("#2b8a3e", "#ebfbee"), "shaping": ("#7048e8", "#f3f0ff"),   # the stage pills
            "agreed": ("#1971c2", "#e7f5ff"), "closed": ("#495057", "#f1f3f5")}


# the studio font (JL 261009: "I think the font should be more readable"): Nunito, Excalidraw's "Normal"
# font, for every word a builder writes; Cascadia, the code font, stays for paths and code. The hand-drawn
# Virgil (1) and Excalifont (5), Lilita One (7) and Comic Shanns (8) read slowly; Helvetica (2) and
# Liberation Sans (9) become Nunito too, so a drawing reads in one font.
FONT, CODE_FONT = 6, 3
# each frame fits the screen: whole and readable at 50% zoom, mostly on screen at 100% (JL 261010)
FRAME_MAX, TEXT_MIN = (2800, 1600), 20   # aim: 2560 x 1440, a 1280 x 720 pane at 50%


def apply_font(els):
    """The studio font applied to what a builder wrote: every text becomes Nunito (6) but code (3).
    The person's own marks never pass through here. Returns how many texts changed."""
    n = 0
    for e in els:
        if e.get("type") == "text" and e.get("fontFamily") not in (FONT, CODE_FONT):
            e["fontFamily"] = FONT
            n += 1
    return n


def off_palette(els, slides=False):
    """The elements drawn in a colour outside the studio palette (a stroke not black, red or green, or
    any fill but the key point's): a builder can print these before it writes. `slides=True` (a slide draft)
    also allows the slide accent, its light fill and the muted caption gray."""
    strokes = PALETTE + (SLIDE_PALETTE if slides else ())
    fills = ("transparent", "#ffffff", "", KEY) + ((ACCENT_FILL,) if slides else ())
    return [e for e in els if not is_ui(e) and (str(e.get("strokeColor", INK)).lower() not in strokes
            or str(e.get("backgroundColor", "transparent")).lower() not in fills)]


def apply_palette(els):
    """The studio look applied to what a builder drew (JL 261007, "Recolour all"): a stroke outside
    black · red · green becomes black (a transparent one stays), a fill becomes transparent (white and the
    key point's KEY stay). An image keeps its stroke, fill and picture. Returns how many elements changed."""
    n = 0
    for e in els:
        if e.get("type") == "image" or is_ui(e):          # a screen keeps the workbench's colours (ui_frame)
            continue
        stroke, fill = str(e.get("strokeColor", INK)).lower(), str(e.get("backgroundColor", "transparent")).lower()
        if stroke not in PALETTE + ("transparent", ""):          # an invisible stroke stays invisible
            e["strokeColor"] = INK
            n += 1
        if fill not in ("transparent", "#ffffff", "", KEY):
            e["backgroundColor"] = "transparent"
            n += 1
    return n


def is_slide_draft(out):
    """A slide draft (s61-s69) keeps its slide colours (JL 261007: "but for the slide draft, maybe not")."""
    return bool(__import__("re").match(r"^s6\d\b|^s6\d-", Path(out).stem))


# A text element's width is where Excalidraw stops drawing it: a width guessed for English (0.55 of the size a
# letter) cut Chinese lines in half (JL 261012, on b32 s00's "EB1A 递交": "this is not complete"). Measure instead.
_MEASURE_FONT, _measure_fonts = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf", {}
_EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\u2300-\u23FF]")
_CJK = "\u2E80-\u9FFF\uAC00-\uD7AF\uF900-\uFAFF\uFF00-\uFFEF"


def text_width(s, size):
    """A line's width in px as Excalidraw draws it: Nunito for letters (Arial measured, a little wider), a full
    em for a Chinese character, a little more for an emoji."""
    s = str(s).replace("\ufe0f", "").replace("\u200d", "")
    emoji, rest = len(_EMOJI.findall(s)), _EMOJI.sub("", s)
    try:
        from PIL import ImageFont
        if size not in _measure_fonts:
            _measure_fonts[size] = ImageFont.truetype(_MEASURE_FONT, size)
        width = _measure_fonts[size].getlength(rest) * 1.06
    except Exception:  # no Pillow or no font file: count wide characters as a full em
        import unicodedata
        width = sum(size * (1.0 if unicodedata.east_asian_width(c) in "WF" else 0.56) for c in rest)
    return width + emoji * size * 1.25


def wrap_text(s, size, width):
    """Lines no wider than `width` px: break at a space, before any Chinese character, and inside a word too long
    for a line. An empty paragraph stays an empty line."""
    lines = []
    for para in str(s).split("\n"):
        line = ""
        for tok in re.findall(rf"[{_CJK}]|[^\s{_CJK}]+|\s+", para):
            if text_width(line + tok, size) <= width or not line.strip():
                line += tok
            else:
                lines.append(line.rstrip())
                line = tok.lstrip()
            while text_width(line, size) > width and len(line) > 1:      # one word wider than the line
                k = len(line) - 1
                while k > 1 and text_width(line[:k], size) > width:
                    k -= 1
                lines.append(line[:k])
                line = line[k:]
        lines.append(line.rstrip())
    return lines


def change_note(x, y, what, date=None, frame=None, size=16):
    """A short green note `✎ <YYMMDD> <what changed>`, a text element to place beside the thing that
    changed; list the same words in the title frame. `date` defaults to today."""
    import datetime as _dt
    text = f"✎ {date or _dt.date.today().strftime('%y%m%d')} {what}"
    return {"id": f"note-{x}-{y}", "type": "text", "x": x, "y": y, "width": text_width(text, size) + 4,
            "height": size * 1.25, "angle": 0, "strokeColor": GREEN, "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid", "roughness": 1, "opacity": 100,
            "groupIds": [], "frameId": frame, "roundness": None, "seed": 1, "version": 1, "versionNonce": 1,
            "isDeleted": False, "boundElements": [], "updated": 1, "link": None, "locked": False, "text": text,
            "originalText": text, "fontSize": size, "fontFamily": FONT, "textAlign": "left",
            "verticalAlign": "top", "containerId": None, "autoResize": True, "lineHeight": 1.25}


def grid(els, rows, gap=150):
    """Place the frames in rows, read left to right and then down, never one long column (JL 261009:
    "don't put all the things in one column"). `rows` lists every frame id once, row by row; each frame
    moves with everything drawn in it and everything marked `customData.follows` its id (drawn outside it, as a
    staircase's results), and takes their room in its row. A builder draws each frame where it likes, then calls this once,
    before `write`."""
    frames = {e["id"]: e for e in els if e["type"] == "frame"}
    placed = [fid for row in rows for fid in row]
    assert sorted(placed) == sorted(frames), f"grid() places each frame once: {placed} vs {list(frames)}"

    def follows(e, fid):                    # drawn outside the frame but belonging to it (a staircase's results)
        return (e.get("customData") or {}).get("follows") == fid

    def reach(fid):                         # the frame's width and height, grown by what follows it
        f = frames[fid]
        own = [e for e in els if follows(e, fid)]
        return (max([f["x"] + f["width"]] + [e["x"] + e.get("width", 0) for e in own]) - f["x"],
                max([f["y"] + f["height"]] + [e["y"] + e.get("height", 0) for e in own]) - f["y"])
    y = 0
    for row in rows:
        x, tall = 0, 0
        for fid in row:
            f = frames[fid]
            w, h = reach(fid)
            dx, dy = x - f["x"], y - f["y"]
            for e in els:
                if e["id"] == fid or e.get("frameId") == fid or follows(e, fid):
                    e["x"], e["y"] = e["x"] + dx, e["y"] + dy
            x += w + gap
            tall = max(tall, h)
        y += tall + gap
    return els


def explains(frame):
    """Mark a frame small on purpose: it explains the main frame beside it (JL 261013: "主次分明 … 一个很大的 frame，
    然后有一些小的 frame 是解释这些大的 frame 的", and "大小有致"). check.py then holds it to neither a screen's size nor
    a dense frame's words: its room is the point. Returns it."""
    frame.setdefault("customData", {})["explains"] = True
    return frame


def is_explains(e):
    return bool((e.get("customData") or {}).get("explains"))


def stairs(els, order, gap=260, step=520):
    """Place the frames as stairs, not as left-aligned rows (JL 261013: "你不能每一个都是朝左对齐。你朝左对齐好像就是每一个
    一列都是非常重要的"): the first, the main frame, at the origin; each next one lower and further right, so no two
    share a left edge and the main frame reads first. `order` lists every frame id once, in reading order; an
    `(id, dx)` pair sets that frame's own step right (negative steps back left). Returns the placed frames in order."""
    frames = {e["id"]: e for e in els if e["type"] == "frame"}
    ids = [o[0] if isinstance(o, tuple) else o for o in order]
    assert sorted(ids) == sorted(frames), f"stairs() places each frame once: {ids} vs {list(frames)}"
    x = y = 0
    placed = []
    for k, o in enumerate(order):
        fid, dx = o if isinstance(o, tuple) else (o, step)
        f = frames[fid]
        if k:
            x, y = x + dx, placed[-1]["y"] + placed[-1]["height"] + gap
        mx, my = x - f["x"], y - f["y"]
        for e in els:
            if e["id"] == fid or e.get("frameId") == fid:
                e["x"], e["y"] = e["x"] + mx, e["y"] + my
        placed.append(f)
    return placed


def reads_down(frame):
    """Mark a frame that is read top to bottom: one piece of writing, or a source's pages marked up. It stays
    one frame however long (JL 261010: "the draft take should be one single frame, and the Written out should
    be one large frame"); its width still fits the screen, only its height may pass FRAME_MAX. Returns it."""
    frame.setdefault("customData", {})["reads"] = "down"
    return frame


def is_read_down(e):
    return (e.get("customData") or {}).get("reads") == "down"


def large(frame):
    """Mark a frame drawn larger than a screen on purpose: a chain of concept boxes wider than FRAME_MAX, read by
    zooming (JL 261012, on a Task's steps: "don't limited yourself of the size of the frame"). Returns it."""
    frame.setdefault("customData", {})["large"] = True
    return frame


def is_large(e):
    return bool((e.get("customData") or {}).get("large"))


def aside(e):
    """Mark a side note: words beside the main content (the page pictures it explains), written smaller than
    it on purpose (JL 261011, on revise mode's notes: "The content or the font size, can be much smaller,
    than the main content"). `small_text` does not count it. Returns it."""
    e.setdefault("customData", {})["aside"] = True
    return e


def is_aside(e):
    return bool((e.get("customData") or {}).get("aside"))


def ui_frame(frame, since=None):
    """Mark a frame that draws the workbench's screen: write() gives what is drawn in it the workbench's own
    colours (UI) instead of black (JL 261012). Red open questions and green change notes in it keep their
    colour and meaning. `since` (YYMMDD): the day it turned to colour, written as a green change note in the
    frame's top right corner. Returns it."""
    frame.setdefault("customData", {})["ui"] = True
    if since:
        frame["customData"]["ui_since"] = since
    return frame


def is_ui(e):
    return bool((e.get("customData") or {}).get("ui"))


def _inside(a, b, pad=2):
    """Box a lies inside box b."""
    return (a["x"] >= b["x"] - pad and a["y"] >= b["y"] - pad and a["x"] + a["width"] <= b["x"] + b["width"] + pad
            and a["y"] + a["height"] <= b["y"] + b["height"] + pad)


def colour_ui(els):
    """The screens in each ui_frame() take the workbench's colours, by what each element is:

    a box holding other boxes  a pane: light wash fill, gray edge (an outer pane wash, an inner one white)
    a box holding none          a button, tab, chip or card: white, light gray edge
    ... drawn bold              the open tab or button: blue edge and wash, its words blue
    ... drawn dashed            a proposed or new one: violet edge and wash
    ... holding a stage word    the stage pill's own colours (explore, shaping, agreed, closed)
    ... thin, holding no words  a bar: filled blue, as the Timeline draws a count
    a word: small · a path/link muted gray · link blue; a status (answered, partial, open) its colour
    a line, an ellipse          a separator gray; a dot or bubble filled blue-gray at 80%, as the Timeline's
    Red and green, arrows, frames and images are left as drawn. A pane now has a fill, so it moves behind what
    it holds (a builder may draw the pane last, to fit it). Returns how many elements it coloured."""
    frames = {e["id"] for e in els if e.get("type") == "frame" and is_ui(e)}
    if not frames:
        return 0
    n, panes = 0, []
    for fid in frames:
        mine = [e for e in els if e.get("frameId") == fid and not e.get("isDeleted")
                and str(e.get("strokeColor", INK)).lower() not in (RED, GREEN)]
        boxes = [e for e in mine if e.get("type") == "rectangle"]
        texts = [e for e in mine if e.get("type") == "text"]
        holds = {id(b): [o for o in boxes if o is not b and _inside(o, b)] for b in boxes}
        within = {id(b): [o for o in boxes if o is not b and _inside(b, o)] for b in boxes}
        for b in boxes:
            words = [t for t in texts if _inside(t, b) and not any(_inside(t, c) for c in holds[id(b)])]
            stage = next((w for t in words for w in STAGE_UI if re.search(rf"\b{w}\b", str(t.get("text", "")))), None)
            if holds[id(b)]:
                stroke, fill = UI["edge"], UI["wash"] if not within[id(b)] else UI["box"]
                colour = None
                panes.append((b, [o for o in mine if o is not b and _inside(o, b)]))
            elif (b.get("customData") or {}).get("ui_kind") in UI_KIND:    # a Report group by its kind
                stroke, fill = UI_KIND[b["customData"]["ui_kind"]]
                colour = None
            elif stage and len(words) <= 2:
                stroke, fill = STAGE_UI[stage]
                colour = stroke
            elif b["height"] <= 14 and not words:                  # a bar: a count drawn as a length
                stroke, fill, colour = UI["on"], UI["on"], None
            elif b.get("strokeStyle") == "dashed":
                stroke, fill, colour = UI["new"], UI["new_bg"], UI["new"]
            elif float(b.get("strokeWidth", 1)) >= 2.5:
                stroke, fill, colour = UI["on"], UI["on_bg"], UI["on"]
            else:
                stroke, fill, colour = UI["line"], UI["box"], None
            b.update(strokeColor=stroke, backgroundColor=fill, fillStyle="solid")
            b.setdefault("customData", {})["ui"] = True
            n += 1
            for t in words if colour else ():
                t["strokeColor"] = colour
                t.setdefault("customData", {})["ui"] = True
        for t in texts:
            if is_ui(t):
                continue
            s = str(t.get("text", ""))
            status = next((c for w, c in STATUS_UI.items() if len(s) <= 40 and re.match(rf"\s*{w}\b", s)), None)
            if status:
                t["strokeColor"] = status
            elif "↗" in s or re.fullmatch(r"[\w./<>@+-]+/[\w./<>@+-]*", s.strip()):
                t["strokeColor"] = UI["link"]
            elif float(t.get("fontSize", 20)) < 20:
                t["strokeColor"] = UI["mut"]
            else:
                t["strokeColor"] = UI["text"]
            t.setdefault("customData", {})["ui"] = True
            n += 1
        for e in mine:
            if e.get("type") == "line":
                e["strokeColor"] = UI["edge"]
            elif e.get("type") == "ellipse":
                e.update(strokeColor=UI["dot"], backgroundColor=UI["dot"], fillStyle="solid", opacity=80)
            else:
                continue
            e.setdefault("customData", {})["ui"] = True
            n += 1
    for f in [e for e in els if e.get("id") in frames and (e.get("customData") or {}).get("ui_since")]:
        what = "the screen in the workbench's colours (JL)"
        w = text_width(f"✎ {f['customData']['ui_since']} {what}", 16)
        els.append(change_note(round(f["x"] + f["width"] - w - 40), round(f["y"] + 16), what,
                               f["customData"]["ui_since"], f["id"]))
    for pane, held in sorted(panes, key=lambda ph: ph[0]["width"] * ph[0]["height"]):   # inner panes first
        first = min((i for i, e in enumerate(els) if any(e is h for h in held)), default=None)
        at = next(i for i, e in enumerate(els) if e is pane)
        if first is not None and first < at:
            els.insert(first, els.pop(at))
    return n


def oversized(els):
    """Frames bigger than FRAME_MAX, as (name, width, height): too big to read whole at 50% zoom (JL 261010:
    "when I zoom in 50% I can read the whole workflow, when I read 100%, I can see most part of the frame").
    A frame marked `reads_down` is checked on its width only."""
    w, h = FRAME_MAX
    return [(e.get("name") or e["id"], round(e["width"]), round(e["height"])) for e in els
            if e["type"] == "frame" and not e.get("isDeleted")
            and (e["width"] > w or (e["height"] > h and not is_read_down(e)))]


def small_text(els):
    """Frames whose words are mostly below TEXT_MIN, as (name, median size): they will not read at 50% zoom, as
    after scaling a whole drawing down. Change notes (green) and side notes (`aside`) may be smaller and are
    not counted."""
    frames = {e["id"]: e for e in els if e["type"] == "frame" and not e.get("isDeleted")}
    sizes = {}
    for e in els:
        if e["type"] == "text" and e.get("frameId") in frames and e.get("strokeColor") != GREEN \
                and not is_aside(e) and not e.get("isDeleted"):
            sizes.setdefault(e["frameId"], []).append(e["fontSize"])
    out = []
    for fid, s in sizes.items():
        mid = sorted(s)[len(s) // 2]
        if mid < TEXT_MIN:
            out.append((frames[fid].get("name") or fid, round(mid, 1)))
    return out


def numbered_frames(els):
    """One piece cut into numbered frames ("X · 1", "X · 2", ...), as {stem: count}: the shape JL turned down
    (261010: "the draft take should be one single frame, and the Written out should be one large frame")."""
    stems = Counter()
    for e in els:
        if e["type"] == "frame" and not e.get("isDeleted"):
            m = re.match(r"^(.*\S)\s*·\s*\d+$", e.get("name") or "")
            if m:
                stems[m.group(1)] += 1
    return {stem: n for stem, n in stems.items() if n >= 2}


def one_column(els):
    """True when 4 or more frames stand in one column, the layout JL turned down (261009)."""
    xs = [round(e["x"]) for e in els if e["type"] == "frame"]
    return len(xs) >= 4 and len(set(xs)) == 1


# a frame is not a slide (JL 261012: "每一个 frame 都太像一张 slide，而且每个 frame 里的内容又太少，它本身又不是一个
# tree 结构 ... 我个人更 prefer 那种 tree 结构，就像 folder tree 那样"): a full 2560 x 1440 screen holds 440 words or
# more; b04's slide-like s00 frames held 38 to 113 words per million px, its dense ones 150 to 210
SPARSE_MIN = 120          # words per million px of frame
MAP_SHARE = 2 / 3          # a map's boxes and named arrows say what words would: it needs two thirds the words
MAX_FRAMES = 3            # a Block's s00: its background (two at most) and its index; a reads_down piece not counted


def is_s00(out):
    """The Block's s00, its background and index: the one drawing the tree rules are for (JL 261012: "I just mean for
    the s00 to have the tree, why you make all the others to be the tree as well")."""
    return Path(out).parent.name.startswith("s00-")


def frame_limit(out):
    """How many frames a drawing may hold: MAX_FRAMES for a Block's s00; no limit for any other topic's drawing."""
    return MAX_FRAMES if is_s00(out) else None


def sparse(els):
    """Frames that read like a slide: fewer than SPARSE_MIN words per million px, as (name, words, per million).
    A frame that holds a picture, draws a screen (`ui_frame`), writes no word at all, is over FRAME_MAX (oversized()
    names it) or belongs to a slide draft is not counted; a map (topic_map's boxes and arrows, customData map) needs
    MAP_SHARE of the words."""
    frames = {e["id"]: e for e in els if e["type"] == "frame" and not e.get("isDeleted") and not is_ui(e)}
    words, pictures = Counter(), set()
    for e in els:
        if e.get("frameId") in frames and not e.get("isDeleted"):
            if e["type"] == "image":
                pictures.add(e["frameId"])
            elif e["type"] == "text" and e.get("strokeColor") != GREEN:
                # a word counts by the room it takes: a 40 px heading fills four times a 20 px line's
                words[e["frameId"]] += len(e.get("text", "").split()) * (e.get("fontSize", 20) / 20) ** 2
    out = []
    for fid, f in frames.items():
        per = words[fid] / max(f["width"] * f["height"] / 1e6, 0.01)
        big = f["width"] > FRAME_MAX[0] or f["height"] > FRAME_MAX[1]     # oversized() already names it
        need = SPARSE_MIN * (MAP_SHARE if (f.get("customData") or {}).get("map") else 1)
        if fid not in pictures and words[fid] and not big and per < need:          # nor a frame with no words
            out.append((f.get("name") or fid, round(words[fid]), round(per)))
    return out


# ── a tree, like a folder tree (JL 261012) ─────────────────────────────────────────────────────────────────────
# A node is a string (a leaf), a one-key mapping {label: [children]}, or {text: ..., children: [...]}; so a
# yaml list in a topic's face is a tree as written. A leaf that starts "? " or "❓" is red (open), "✎ " green (a
# change). An emoji in front of a node makes the tree easy to scan (JL 261012: "add the things like the emoji").
TREE_INDENT, TREE_GAP = 34, 6
_tree_n = [0]


def _tree_node(n):
    if isinstance(n, str):
        return n, []
    if isinstance(n, dict) and "text" in n:
        return str(n["text"]), list(n.get("children") or [])
    if isinstance(n, dict) and len(n) == 1:
        (k, v), = n.items()
        return str(k), list(v or []) if isinstance(v, list) else [str(v)]
    return str(n), []


def _tree_base(kind, x, y, w, h, frame, **kw):
    _tree_n[0] += 1
    e = {"id": f"tree-{_tree_n[0]}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
         "strokeColor": INK, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 2,
         "strokeStyle": "solid", "roughness": 0, "opacity": 100, "groupIds": [], "frameId": frame, "roundness": None,
         "seed": _tree_n[0], "version": 1, "versionNonce": _tree_n[0], "isDeleted": False, "boundElements": [],
         "updated": 1, "link": None, "locked": False}
    e.update(kw)
    return e


def tree_text(x, y, text, size=20, width=None, frame=None, color=None):
    """A text element wrapped to `width` px (Nunito's measure), its colour from its first mark unless given.
    Returns (element, height)."""
    text = "\n".join(wrap_text(text, size, width)) if width else str(text)
    color = color or (RED if text.startswith(("?", "❓")) else GREEN if text.startswith("✎") else INK)
    lines = text.split("\n")
    h = len(lines) * size * 1.25
    return _tree_base("text", x, y, max(text_width(ln, size) for ln in lines) + 4, h, frame, strokeColor=color,
                      strokeWidth=1, text=text, originalText=text, fontSize=size, fontFamily=FONT,
                      textAlign="left", verticalAlign="top", containerId=None, autoResize=True,
                      lineHeight=1.25), h


def tree_line(points, frame=None, width=2):
    """A plain line through `points` (a tree's spine or tick)."""
    x0, y0 = points[0]
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    return _tree_base("line", x0, y0, max(1, max(xs) - min(xs)), max(1, max(ys) - min(ys)), frame,
                      strokeWidth=width, points=[[px - x0, py - y0] for px, py in points], lastCommittedPoint=None,
                      startBinding=None, endBinding=None, startArrowhead=None, endArrowhead=None)


def _tree_draw(out, node, x, y, width, frame, size, depth, head):
    """Draw one node and its children at (x, y); return (bottom y, the middle of its first line)."""
    label, kids = _tree_node(node)
    s = head if depth == 0 else size
    e, h = tree_text(x, y, label, s, width, frame)
    out.append(e)
    mid, below, y = y + s * 0.65, y + h, y + h + TREE_GAP
    spine, ticks = x + 10, []
    for k in kids:
        y, kmid = _tree_draw(out, k, x + TREE_INDENT, y, width - TREE_INDENT, frame, size, depth + 1, head)
        ticks.append(kmid)
    if ticks:                                           # the folder-tree lines: a spine and a tick per child
        out.append(tree_line([(spine, below + 2), (spine, ticks[-1])], frame))
        out += [tree_line([(spine, t), (x + TREE_INDENT - 6, t)], frame) for t in ticks]
    return y + (TREE_GAP if depth == 0 else 0), mid


def tree_height(nodes, width, size=20, head=24):
    """The height a tree would take, drawn nowhere."""
    out, y = [], 0
    for n in nodes:
        y, _ = _tree_draw(out, n, 0, y, width, None, size, 0, head)
    return y


def tree(x, y, nodes, width, frame=None, size=20, head=24, cols=1, gap=60):
    """Draw `nodes` as a folder tree, in `cols` columns side by side, each `(width - gap) / cols` wide: the
    top-level nodes are split into columns of about equal height, in order, and a bus line along the top
    joins the columns into one tree. Returns (elements, height). The frame's own title is the tree's root:
    the builder writes it above `y`."""
    cols = max(1, min(cols, len(nodes)))
    cw = (width - gap * (cols - 1)) / cols
    hs = [tree_height([n], cw - TREE_INDENT, size, head) for n in nodes]
    groups, target, cur = [[]], sum(hs) / cols, 0
    for n, h in zip(nodes, hs):                          # contiguous split near equal heights
        if groups[-1] and cur + h / 2 > target * len(groups) and len(groups) < cols:
            groups.append([])
        groups[-1].append(n)
        cur += h
    out, bottom, top = [], y, y + 22
    if len(groups) > 1:
        out.append(tree_line([(x + 10, y), (x + (len(groups) - 1) * (cw + gap) + 10, y)]))
    for i, group in enumerate(groups):
        cx, yy, ticks = x + i * (cw + gap), top, []
        for n in group:
            yy, mid = _tree_draw(out, n, cx + TREE_INDENT, yy, cw - TREE_INDENT, frame, size, 0, head)
            ticks.append(mid)
        out.append(tree_line([(cx + 10, y), (cx + 10, ticks[-1])], frame))
        out += [tree_line([(cx + 10, t), (cx + TREE_INDENT - 6, t)], frame) for t in ticks]
        bottom = max(bottom, yy)
    for e in out:
        e["frameId"] = frame
    return out, bottom - y


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
    person's own kept images stay too. `palette`: apply the studio look (black, red, green, and the
    readable font) to what this build draws; by default on for every drawing but a slide draft (s61-s69). The person's own marks are
    never recoloured."""
    out = Path(out)
    snap_path = seed_path(out)
    if palette if palette is not None else not is_slide_draft(out):
        colour_ui(els)
        apply_palette(els)
        apply_font(els)
    if not is_slide_draft(out) and one_column(els):
        print(f"{out.name}: {sum(e['type'] == 'frame' for e in els)} frames in one column; set them in rows "
              "with canvas.grid (JL 261009: \"don't put all the things in one column\")")
    for stem, n in ([] if is_slide_draft(out) else numbered_frames(els).items()):
        print(f"{out.name}: '{stem}' is cut into {n} numbered frames; one piece read top to bottom is one frame "
              "that grows down, marked canvas.reads_down (JL 261010)")
    for name, w, h in ([] if is_slide_draft(out) else oversized(els)):
        print(f"{out.name}: frame '{name}' is {w} x {h} px, over {FRAME_MAX[0]} x {FRAME_MAX[1]}: fit it to one "
              "screen at 50% zoom with fewer words and boxes sized to them; a piece read top to bottom stays one frame, "
              "marked canvas.reads_down, and only its width must fit (JL 261010)")
    for name, size in ([] if is_slide_draft(out) else small_text(els)):
        print(f"{out.name}: frame '{name}' writes its words at {size} px, under {TEXT_MIN}: they will not read at 50% "
              "zoom; keep the words' size and make room by cutting words (JL 261010)")
    for name, n, per in (sparse(els) if is_s00(out) else []):              # s00's rule, not every topic's
        print(f"{out.name}: frame '{name}' holds {n} words, {per} per million px, under {SPARSE_MIN}: it reads like a "
              "slide; merge it into a fuller frame and draw it as a tree, canvas.tree (JL 261012)")
    n_frames, limit = sum(e["type"] == "frame" and not is_read_down(e) for e in els), frame_limit(out)
    if limit and n_frames > limit:
        print(f"{out.name}: {n_frames} frames, over {limit}: a topic is ① its Background, ② its Tree, ③ one more "
              "(a screen, or the reference), not a row of slides; merge them (JL 261012: \"如果有 background，大概三个 "
              "frame 就差不多了\")")
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
