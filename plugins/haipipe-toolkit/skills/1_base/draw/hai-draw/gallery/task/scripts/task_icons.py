"""Vivid first (hai-draw principle ⑨): the real things a Task's frames are about, drawn as icons lit by their state.

    task_icon(d, f, runs, noun)   ① and ⓪: the Task's sources as one screen (videos) or one server (Runs), lit by
                                  their states, and how many are checked or done as a big number, right of the title
    run_icon(d, f, run)           a source's own frame: its screen or its server, lit by its state, right of the title
    notes_icon(d, width, opens)   ②: the page its words come from, orange while a point is open

Each sits right of the widest heading line and left of the badge (draw.py's badge: the top right 590 px), and is
marked aside, so fit() sizes the frame by its boxes and check.py counts its words without them. The small marks the
frames share live here too: a source's checked state (`video_checked`) and a passage's numbered circle.
"""
from __future__ import annotations

import re

import canvas
import icons
import job_results as jr
from draw import INK, Drawing

MARKER = "#ffe86e"                                              # read_paper's HIGHLIGHT, the yellow on the pages
HEAD_W = 430                                                    # an icon and its big number, side by side
GAP = 70                                                        # between the heading's words and the icon
SIZES = {"monitor": (170, 150), "server": (100, 130)}           # what each icon takes, at the size drawn here


def video_checked(state: str) -> bool:
    """A source checked against its video: the state says the video (or its claims) was checked, and nothing in it is
    still pending; "paper sections checked … video review pending" is not (b12 t07 r05)."""
    s = str(state).lower()
    if re.search(r"not checked|unchecked|pending|not yet", s):
        return False
    return bool(re.search(r"checked against the video|\b(video|claims?)\b[^;]*\bchecked\b", s))


def circled(n: int) -> str:
    return chr(0x2460 + n - 1) if 1 <= n <= 20 else f"({n})"


def number_badge(d: Drawing, x: float, y: float, n: int, size: float = 66) -> None:
    """A passage's number in a circle of the highlight's own yellow, drawn beside the passage and beside its note,
    so no arrow has to cross between them."""
    d.el("ellipse", x, y, size, size, strokeColor=INK, strokeWidth=2.5, backgroundColor=MARKER, fillStyle="solid")
    s, fs = str(n), 36
    d.text(x + (size - Drawing.measure(s, fs) - 4) / 2, y + (size - fs * 1.25) / 2, s, fs)


# ── the icons ────────────────────────────────────────────────────────────────────────────────────────────────
def state_of(run: dict) -> str:
    """A source's light: red when it failed, green when done (a video: checked against the video), orange otherwise."""
    st = str(run.get("state") or "?")
    m = jr.mark(st)
    if m == "❌":
        return "bad"
    return "ok" if m == "✅" or (not run.get("work") and video_checked(st)) else "wait"


def head_right(d: Drawing, f: dict, below: float = 160) -> float:
    """Where the frame's heading words end: the right edge of its widest line above the key point."""
    texts = [e for e in d.els if e.get("frameId") == f["id"] and e["type"] == "text" and e["y"] < below
             and not (e.get("customData") or {}).get("aside")]
    return max((e["x"] + max(Drawing.measure(ln, e.get("fontSize", 20)) for ln in str(e.get("text", "")).split("\n"))
                for e in texts), default=40)


def put(d: Drawing, name: str, eid: str, x: float, y: float, *args, **kw) -> list:
    """One icon into the current frame, aside: fit() and the word counts leave it out."""
    return [canvas.aside(e) for e in d.icon(name, eid, x, y, *args, **kw)]


def icon_of(work: bool, eid: str, d: Drawing, x: float, y: float, state: str) -> float:
    """A video's screen or a Run's server, lit; returns its width."""
    name = "server" if work else "monitor"
    w, h = SIZES[name]
    put(d, name, eid, x, y + (150 - h) / 2, state, **({"w": w, "h": h} if work else {}))
    return w


def task_icon(d: Drawing, f: dict, runs: list, noun: str) -> None:
    """The Task's sources as one icon lit by all their states (red when one failed, green when all are done or
    checked, orange otherwise, grey when there is none), and how many are, as a big number in the same colour."""
    d.fid = f["id"]
    work = noun.lower().startswith("run")
    lights = [state_of(r) for r in runs]
    state = "off" if not lights else "bad" if "bad" in lights else "ok" if set(lights) == {"ok"} else "wait"
    x = head_right(d, f) + GAP
    w = icon_of(work, f"{f['id']}_task", d, x, 12, state)
    label = "Runs done" if work else "videos checked"
    put(d, "big_number", f"{f['id']}_done", x + w + 120, 40, f"{lights.count('ok')}/{len(lights)}", label,
        icons.lit(state)[0], 52)


def run_icon(d: Drawing, f: dict, run: dict) -> None:
    """One source's screen (a video) or server (a Run), lit by its own state, right of its frame's title."""
    d.fid = f["id"]
    icon_of(bool(run.get("work")), f"{f['id']}_src", d, head_right(d, f) + GAP, 12, state_of(run))


def notes_icon(d: Drawing, width: float, opens: list) -> None:
    """The page the words come from, at the frame's top right: orange while a point is still open."""
    put(d, "document", "notes_doc", width - 140, 14, "wait" if opens else "ok", w=80, h=96)
