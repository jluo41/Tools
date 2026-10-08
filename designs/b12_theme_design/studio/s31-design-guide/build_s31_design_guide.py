"""s31 · design Guide: s31-design-guide.excalidraw, the design workbench's Guide tab, cut by level, in the
style of b03's s31-guide (four Views, each split Block · Job · Task, cards in one shape per View).

One frame per level: the four Views opened from that level's tab (its section open, the other two folded),
"on disk" under each, then that level's open points in red. Each level's content is its own file (JL 261007:
follow b16's s31-paper-guide and b03's s31-guide): guide_block.py · guide_job.py · guide_task.py, each exporting LEVEL = {View: items}, ON_DISK = {View: [(line, meaning)]} and OPEN = ["? …"].
A level with no file yet draws "(not drawn yet)". Items are s31's kinds (c cards · w drawing cards ·
t line · m mono line); a text with "?" draws red (a proposal or an open point).

Edit a level's file, not this one; the builder is b16's, with the design Guide's words. Written through canvas.write (b03), so every
mark a person adds survives a rebuild.

    python build_s31_design_guide.py [out.excalidraw]
"""
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[3]
S03 = TOOLS / "designs" / "b03_project_workbench" / "studio" / "s31-guide"
sys.path.insert(0, str(S03))
sys.path.insert(0, str(HERE))
import build_s31_guide as S3  # noqa: E402  (s31's Guide screen, cards and helpers; draws nothing on import)

L, canvas = S3.L, S3.canvas
text, INK, GRAY, RED = L.text, L.INK, L.GRAY, L.RED
LEVELS, VIEWS = S3.LEVELS, S3.GUIDE_VIEWS
TAB = {"Block": "the Design Board tab", "Job": "a goal × method tab", "Task": "a design's tab"}
# the design Guide's own header line per View (s31 HEAD, in the design's words)
HEAD = {"Description": ("Design · what this family is for",
                        "N designs for one goal by one method, checked, released, then tested in the Exp"),
        "Method": ("how a design is made, by level", "set the goals and inputs · one goal × one method → N · check each design"),
        "RoadMap Draw": ("the design's drawings, by level", "the structure and ladder, then each level's screens"),
        "Related Paper": ("the papers behind the method, by level", "each paper under the level its method serves")}
FOLDED = {"Description": "6 Spaces · skills · folders", "Method": "{steps} steps · {cards} method cards",
          "RoadMap Draw": "{n} drawings", "Related Paper": "{n} papers"}


def part(level):
    """A level's file (guide_<level>.py), or None while its session has not written it."""
    try:
        return importlib.import_module(f"guide_{level.lower()}")
    except ModuleNotFoundError:
        return None


LINE, HEADLINE = 110, 104           # a card's mono line, and its title + what-it-is line, in characters


def _cut(s, n):
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"


def fit(kind, s):
    """Keep a card inside its box: an over-long title line or mono line ends in "…" (the Guide shows it whole)."""
    if kind == "c":
        return [(t, _cut(d, max(20, HEADLINE - len(t))), _cut(line, LINE)) for t, d, line in s]
    if kind == "w":
        return [(t, _cut(d, max(20, HEADLINE - len(t))), _cut(line, LINE), o) for t, d, line, o in s]
    if kind in ("t", "m"):
        return _cut(s, LINE + 10)
    return s


def items(p, view, level):
    if p is None or view not in getattr(p, "LEVEL", {}):
        return [("t", f"? (not drawn yet: guide_{level.lower()}.py, the {level} session's)")]
    return [(k, fit(k, s)) for k, s in p.LEVEL[view]]


def redden(start):
    """Every text drawn since `start` that carries a "?" turns red: a proposal or an open point."""
    for e in L.els[start:]:
        if e.get("type") == "text" and "?" in e.get("text", ""):
            e["strokeColor"] = RED


def frame_level(x0, y0, level, p):
    """The four Views opened from this level's tab: its section open, the other two folded."""
    fr = L.open_frame(f"{level} · Guide from {TAB[level]}")
    text(x0, y0, f"{level} · the design Guide, opened from {TAB[level]}", 34)
    text(x0, y0 + 50, f"Each View: the {level} section open, the other two folded (b03 s31-D05 to D08). "
                      "Read from the design Guide's files; red = proposed or open.", 20, GRAY)
    folded = tuple(lv for lv in LEVELS if lv != level)
    mark = len(L.els)                                         # measure the open section, then drop the draft
    tall = max(S3.draw_items(0, 0, S3.SW - S3.RW - 28, items(p, v, level), level) for v in VIEWS)
    del L.els[mark:]
    S3.PH[0] = max(S3.SH, 136 + 80 + 52 + tall + 2 * 60 + 80)
    for i, view in enumerate(VIEWS):
        x, y = x0 + i * (S3.SW + 120), y0 + 110
        text(x, y, f"Guide › {view}, from {TAB[level]}", 24)
        start = len(L.els)
        S3.guide_screen(x, y + 40, "proposed", view, folded=folded)
        redden(start)
        rows = getattr(p, "ON_DISK", {}).get(view, []) if p else []
        ty = y + 40 + S3.screen_h("proposed") + 50
        text(x, ty, "on disk", 22)
        for k, (line, meaning) in enumerate(rows):
            red = "?" in line or "?" in meaning
            text(x, ty + 44 + k * 28, line, 16, RED if red else INK, L.MONO)
            if meaning:
                text(x + 640, ty + 45 + k * 28, meaning, 15, RED if red else GRAY)
    notes = getattr(p, "OPEN", []) if p else []
    ny = y0 + 110 + 40 + S3.screen_h("proposed") + 50 + 44 + 8 * 28 + 80
    text(x0, ny, f"open at the {level} level", 24, RED)
    for k, q in enumerate(notes):
        text(x0, ny + 44 + k * 30, q, 17, RED)
    L.close_frame(fr)
    return fr


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s31-design-guide.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    parts = {lv: part(lv) for lv in LEVELS}
    S3.HEAD.update(HEAD)
    for v in VIEWS:                                       # the folded lines count the open level's items
        for lv in LEVELS:
            S3.LEVEL_CONTENT[(v, lv)] = items(parts[lv], v, lv)
    y = 0
    for lv in LEVELS:
        S3.FOLDED_LINE.update({v: _folded(v, parts, lv) for v in VIEWS})
        fr = frame_level(0, y, lv, parts[lv])
        y = fr["y"] + fr["height"] + 300
    canvas.write(out, list(L.els), "build_s31_design_guide.py")


def _folded(view, parts, open_level):
    """What a folded level heading says; s31 has one line per View, so it names the counts in general."""
    return FOLDED[view].format(steps="N", cards="N", n="N")


if __name__ == "__main__":
    main()
