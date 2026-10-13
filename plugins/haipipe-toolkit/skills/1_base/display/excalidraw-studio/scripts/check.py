"""Check a Studio drawing against excalidraw-studio's drawing principles, frame by frame.

    python check.py <drawing>.excalidraw [more …]       a report per drawing: each frame, then each principle

What it can read from the file it checks; what only a person can judge it says so (👤):
  ① a frame fills a screen and stays within FRAME_MAX (one read down, canvas.reads_down: its width only); few
    frames, none a slide (under a third of a screen)
  ② inside: boxes joined by arrows or lines (a map) or text (then 👤: a list, or a map drawn in words?)
  ③ acts named at the left of the rows; an arrow between frames only where one leads on, none through a third
  ④ folder-tree lines (├── └──) in a frame: 👤 are they real folders?
  ⑤ words 20 px or more (a green change note not counted, as in ⑥); a frame title large; one key-point
    colour (#fff3bf) per frame
  ⑥ a text frame's words per million px against its floor (120); a map is measured by ⑦; a picture or screen
    not measured
  ⑦ a map (a workflow, a mind map) holds few words: at most MAP_WORDS (200), at most SMALL_SHARE (a quarter) of
    them under SMALL (28 px, a detail's size); the badge and green notes not counted
A slide draft (s61-s69) keeps its own layout, sizes and words (excalidraw-slide): ① ③ ⑤ ⑥ ⑦ name it, not judge.
A Block's s00 keeps its own words (block_index.py: an index names every topic and Job): ⑦ names it, not judge.
A detail frame (Drawing.detail: a video's full frame) holds the detail ⑦ sends out: ⑥ measures it instead.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from draw import FLOOR, KEY, MAP_WORDS, SMALL, SMALL_SHARE, Drawing, canvas  # noqa: E402

WALL_WORDS = 600   # ⑨: a frame with no picture and more words than this is a wall of text (asked 261012: "things like
                   # this should be forbiden, so rigid, not vivid, no one have the incentive to zoom in and read")

SCREEN = 2560 * 1440


def frames_of(els):
    return sorted((e for e in els if e.get("type") == "frame" and not e.get("isDeleted")), key=lambda e: (e["y"], e["x"]))


def inside(e, f):
    return e.get("frameId") == f["id"] and not e.get("isDeleted")


SLIDE_OWN = "🎞️ a slide draft's own (excalidraw-slide)"
DETAIL_OWN = "📖 a detail frame: the detail ⑦ sends out; ⑥ measures it (draw.Drawing.detail)"
S00_OWN = "🗂️ s00's own: an index names every topic and Job (block_index.py)"
# a badge's own words, as draw.py writes them now (canvas.aside) and wrote them before 0.3.0; a node that only starts
# with the same emoji (a principle titled "📊 ⑥ …") is counted (found on b31 s01, 261012: ⑦'s count was 17 short)
BADGE = re.compile(r"^(📊 \d+ words per million px|🪶 \d+ words, \d+% small|[✅❌] a (map|text)[ :]|🖼️ holds)")


def is_badge(e):
    return bool((e.get("customData") or {}).get("aside")) or bool(BADGE.match(str(e.get("text", ""))))


def check_frame(els, f, slide=False, s00=False):
    mine = [e for e in els if inside(e, f)]
    texts = [e for e in mine if e["type"] == "text" and not is_badge(e)]         # the badge counts the rest
    words = sum(Drawing.words_in(t.get("text", "")) for t in texts if t.get("strokeColor") != canvas.GREEN)
    kind = Drawing.kind(els, f)
    per = round(words / max(Drawing.area_of(els, f) / 1e6, 0.01))    # ⑧: a frame with room is measured over its boxes
    detail = Drawing.is_detail(f)                              # the detail ⑦ sends out: ⑥ measures it
    floor = None if kind == "map" and not detail else FLOOR    # a map: ⑦ measures it, not a floor
    tiny = sum(Drawing.words_in(t.get("text", "")) for t in texts
               if t.get("fontSize", 20) < SMALL and t.get("strokeColor") != canvas.GREEN)
    small = sum(Drawing.words_in(t.get("text", "")) for t in texts
                if t.get("fontSize", 20) < canvas.TEXT_MIN and t.get("strokeColor") != canvas.GREEN)
    biggest = max([t.get("fontSize", 0) for t in texts] or [0])
    tree = sum(str(t.get("text", "")).count("├──") + str(t.get("text", "")).count("└──") for t in texts)
    keys = sum(1 for e in mine if e.get("backgroundColor") == KEY)
    area = f["width"] * f["height"]
    out = {"name": f.get("name") or f["id"], "size": f"{round(f['width'])} x {round(f['height'])}", "kind": kind,
           "per": per, "floor": floor, "words": words}
    big = getattr(canvas, "is_large", lambda e: False)(f)         # larger than a screen on purpose (canvas.large)
    over = not big and (f["width"] > canvas.FRAME_MAX[0] or
                        (f["height"] > canvas.FRAME_MAX[1] and not canvas.is_read_down(f)))
    out["①"] = "✅ large on purpose: zoom to read" if big else ("❌ over " + "x".join(map(str, canvas.FRAME_MAX))) if over else \
        ("❌ a slide: under a third of a screen" if area < SCREEN / 3 else
         "✅ read down: its width fits" if canvas.is_read_down(f) else "✅")
    out["②"] = "✅ a map" if kind == "map" else "🖼️ a picture" if kind == "picture" else "👤 text: a list, or a map in words?"
    out["④"] = f"👤 {tree} folder-tree lines: real folders?" if tree else "✅ none"
    out["⑤"] = ("❌" if small > 0.2 * max(words, 1) or biggest < 40 or keys == 0 else "✅") + \
        f" words under {canvas.TEXT_MIN} px: {round(100 * small / max(words, 1))}% · largest {round(biggest)} px · " \
        f"key point {'yes' if keys else 'none'}"
    out["⑥"] = "🖼️ not measured" if kind == "picture" else "🗺️ a map: ⑦ measures it" if kind == "map" else \
        ("✅" if per >= floor else "❌") + f" {per} (floor {floor})"
    out["⑦"] = (("✅" if words <= MAP_WORDS and tiny <= SMALL_SHARE * max(words, 1) else "❌") +
                f" {words} words (at most {MAP_WORDS}), {round(100 * tiny / max(words, 1))}% under {SMALL} px "
                f"(at most {round(100 * SMALL_SHARE)}%)") if kind == "map" else \
        "🖼️ not measured" if kind == "picture" else "— a text frame: ⑥ measures it"
    if detail and kind != "picture":                     # a detail frame is read up close: ⑥, its floor by its type
        dfloor = Drawing.detail_floor(els, f["id"])
        out["floor"] = dfloor
        out["⑥"] = ("✅" if per >= dfloor else "❌") + f" {per} (floor {dfloor}, a detail frame at its type size)"
        out["⑦"] = DETAIL_OWN if kind == "map" else out["⑦"]
    out["⑨"] = ("❌ a wall of text: " + f"{words} words and no picture (at most {WALL_WORDS}); draw a chart, a real row, "
                "a screenshot or a scoreboard, and keep the words in the face") \
        if kind != "picture" and words > WALL_WORDS and tree < 10 \
        else "✅ vivid: a picture, a folder tree (④), or few enough words"
    if s00 and kind == "map":                            # s00's index names each topic and Job: its own words
        out["⑦"] = S00_OWN
    if s00:
        out["⑨"] = "— s00's index keeps its own shape"
    if slide:                                            # a slide draft keeps its own sizes and words
        out["①"] = out["⑤"] = out["⑥"] = out["⑦"] = out["⑨"] = SLIDE_OWN
    return out


def _cuts(p, q, f, pad=40):
    """Does the segment p-q run inside frame f (its edges, `pad` px deep, not counted)?"""
    t0, t1 = 0.0, 1.0
    for s, d, lo, hi in ((p[0], q[0] - p[0], f["x"] + pad, f["x"] + f["width"] - pad),
                         (p[1], q[1] - p[1], f["y"] + pad, f["y"] + f["height"] - pad)):
        if d == 0:
            if not lo < s < hi:
                return False
            continue
        a, b = sorted(((lo - s) / d, (hi - s) / d))
        t0, t1 = max(t0, a), min(t1, b)
        if t0 >= t1:
            return False
    return True


def _nearest(p, fs):
    return min(fs, key=lambda f: max(f["x"] - p[0], 0, p[0] - f["x"] - f["width"]) ** 2 +
               max(f["y"] - p[1], 0, p[1] - f["y"] - f["height"]) ** 2)


def crossings(arrows, fs):
    """An arrow between frames that runs through a third frame, as that frame's name, once per arrow and frame
    (found on b10 s52, 261012: an act's turn drawn halfway down crossed a taller frame)."""
    out = []
    for a in arrows:
        pts = [(a["x"] + px, a["y"] + py) for px, py in a.get("points") or []]
        if len(pts) < 2 or len(fs) < 3:
            continue
        ends = {_nearest(pts[0], fs)["id"], _nearest(pts[-1], fs)["id"]}
        out += [f.get("name") or f["id"] for f in fs
                if f["id"] not in ends and any(_cuts(p, q, f) for p, q in zip(pts, pts[1:]))]
    return out


def check(path):
    path = Path(path)
    els = [e for e in json.loads(path.read_text(encoding="utf-8"))["elements"] if not e.get("isDeleted")]
    fs = frames_of(els)
    slide = canvas.is_slide_draft(path)                  # s61-s69: excalidraw-slide's sizes and words
    s00 = canvas.is_s00(path)                            # a Block's s00: block_index.py's words (⑦)
    rows = [check_frame(els, f, slide, s00) for f in fs]
    free = [e for e in els if not e.get("frameId") and e["type"] in ("text", "arrow")]
    acts = [e for e in free if e["type"] == "text" and re.match(r"(?i)^act\s*\d", str(e.get("text", "")))]
    arrows = [e for e in free if e["type"] == "arrow"]
    if slide:                                            # its frames read left to right, no acts
        story = SLIDE_OWN + ": logic flow · the slides · on disk, left to right"
    elif len(fs) <= 1:                                   # one frame: no step between frames to name
        story = f"✅ one frame{', its act named' if acts else ''}"
    else:
        through = crossings(arrows, fs)
        # named acts are enough; an arrow between frames only where one leads to the next (asked 261012: "no need to
        # have the --> all the time"), never one running through a third frame
        story = ("❌" if through else "✅" if acts else "🔶" if arrows else "❌") + \
            f" {len(acts)} acts named, {len(arrows)} arrows between frames" + \
            "".join(f" · an arrow runs through '{n[:40]}'" for n in through)
    return {"drawing": path.name, "frames": len(fs), "③": story, "rows": rows, "slide": slide, "s00": s00}


def report(r):
    out = [f"{r['drawing']}: {r['frames']} frames · ③ {r['③']}" +
           (" · a slide draft: sizes and words are excalidraw-slide's" if r.get("slide") else "")]
    for f in r["rows"]:
        out.append(f"  {f['name'][:58]:58} {f['size']:>11} {f['kind']:>7} · {f['words']} words")
        for p in ("①", "②", "④", "⑤", "⑥", "⑦", "⑨"):
            out.append(f"      {p} {f[p]}")
    return "\n".join(out)


def main(argv=None):
    paths = (argv if argv is not None else sys.argv[1:])
    if not paths:
        print(__doc__)
        return 2
    for p in paths:
        print(report(check(p)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
