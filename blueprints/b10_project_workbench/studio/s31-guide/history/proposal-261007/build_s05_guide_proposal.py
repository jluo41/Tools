"""b02 s05 · Guide proposal: s05-guide-proposal.excalidraw: the Guide as it should be in the frame,
beside what we have now, and the questions for JL (JL 261007: "you propose the new design, compare
to what we have now, and then raise the questions").

Four frames, top to bottom:

    now → proposed      one row per part of the Guide: what we have, what it becomes, what changes
    proposed · wireframe the Guide tab in the frame, its four Views, each View's body and the file it reads
    status              one row per Guide family, read live from guide_families at build time
    questions           what JL decides, with room to write

Plain prototype: lines only, placeholders, no project content. Draws through canvas.write, so a
person's marks survive a rebuild.

    python build_s05_guide_proposal.py [out.excalidraw]
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[6]
B03 = TOOLS / "designs" / "b03_project" / "studio"
sys.path.insert(0, str(B03 / "s01-overall-tree-structure"))
sys.path.insert(0, str(B03 / "_build"))
import build_ladder_v4 as L  # noqa: E402  (the drawing helpers)
import canvas  # noqa: E402

SERVERS = TOOLS / "plugins" / "haipipe-toolkit" / "servers"
sys.path.insert(0, str(SERVERS / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()
from live import guide_families as G  # noqa: E402

INK, GRAY, MONO = L.INK, L.GRAY, L.MONO
text, path, box, base = L.text, L.path, L.box, L.base
SIX = ("Description", "Idea Studio", "Audience Report", "Work Details", "Runs", "Delivery")
VIEWS = ("Description", "Method", "RoadMap Draw", "Related Paper")

# ── now → proposed ────────────────────────────────────────────────────────────────────────────
COMPARE = [   # (part, now, proposed, change)
    ("where Guide sits", "old boards: a Guide button first on each\nboard's own Space row; frame: the Guide tab",
     "the first level tab of the frame,\nthe same on every theme", "none in the frame; old boards\nretire as each theme moves"),
    ("its Views", "4: Description · Method · RoadMap Draw ·\nRelated Paper (s02 still draws an older 5:\nSkill set · Methods · Workbench · Folder map)",
     "the same 4 Views, in the third row", "redraw s02"),
    ("Description", "free text about the OLD board's Spaces\n(Scope · Task · Check …) + skills + folders",
     "short text + Spaces by level (Block · Job ·\nTask × six Spaces), read live from\n<theme>_theme.py + skills + folders",
     "each theme rewrites its text;\nthe base adds the live grid"),
    ("Method", "step table; 'where in the workbench'\nnames the old Space › View", "step table; 'where' names a six Space ›\nsubspace; a test flags any other name",
     "each theme rewrites its 'where';\nthe base adds the check"),
    ("methods canvas", "guide/methods.excalidraw\n(design: in its b12 studio)", "the same", "none"),
    ("RoadMap Draw", "the theme's s02-<theme>-workbench\ndrawing: its OLD board's UI", "the theme's s01-<theme>-ladder drawing:\nits Block · Job · Task on the frame ?",
     "repoint explain: in guide.yaml"),
    ("Related Paper", "related/papers.md + related/papers/", "the same", "none"),
    ("where it lives", "servers/workbench-<theme>/guide/ + related/", "the same (done 261007)", "none"),
    ("the base's own", "Description in frame words; RoadMap\nDraw = s03, the old /w/shared site", "RoadMap Draw = the frame itself", "redraw s03"),
]


def frame_compare(y):
    fr = L.open_frame("now → proposed · the Guide")
    text(0, y, "The Guide: what we have now, and what it becomes", 30)
    text(0, y + 46, "One row per part. The move (261007) put every Guide in its own folder; its words still "
                    "describe the old boards.", 16, GRAY)
    cols = (0, 230, 760, 1290)
    top = y + 110
    for x, h in zip(cols, ("part", "now", "proposed", "change")):
        text(x, top, h, 18, INK)
    path([(0, top + 32), (1720, top + 32)], arrow=False, color=INK)
    ry = top + 48
    for row in COMPARE:
        rh = 22 * max(c.count("\n") + 1 for c in row) + 16
        for x, c in zip(cols, row):
            text(x, ry, c, 14, INK if x else INK, MONO if x else L.SANS)
        path([(0, ry + rh - 8), (1720, ry + rh - 8)], arrow=False, color=GRAY)
        ry += rh
    L.close_frame(fr, pad=60)
    return fr["y"] + fr["height"]


# ── proposed · wireframe ──────────────────────────────────────────────────────────────────────
def frame_wireframe(y):
    fr = L.open_frame("proposed · the Guide in the frame")
    text(0, y, "Proposed: the Guide in the frame", 30)
    text(0, y + 46, "Top: the frame's tab row with Guide open, its four Views in the third row. Below: each "
                    "View's body, and the file it reads (arrow).", 16, GRAY)
    top = y + 110
    x = 0
    for k, tab in enumerate(("[Guide]", "Block", "Job ▾", "Task ▾")):
        box(x, top, 130 if k else 120, 40, tab, 16, INK)
        x += 150
    text(640, top + 10, "← Guide is the first tab; the frame body swaps to it", 14, GRAY)
    x = 0
    for k, v in enumerate(VIEWS):
        box(x, top + 60, 200, 36, ("[" + v + "]") if k == 0 else v, 14, INK)
        x += 220
    text(900, top + 68, "← the four Views, in the third row", 14, GRAY)
    vy = top + 130
    W, SRC = 1000, 1080
    # Description
    base("rectangle", 0, vy, W, 420, INK, 1)
    text(16, vy + 12, "Description", 18)
    text(16, vy + 44, "<one paragraph: what this theme does, for whom, what it ends in>", 14, GRAY, MONO)
    text(16, vy + 84, "Spaces by level (read live from <theme>_theme.py)", 15)
    gx, gy, cw = 120, vy + 116, 140
    for i, s in enumerate(SIX):
        text(gx + i * cw, gy, s, 12, INK)
    for r, lvl in enumerate(("Block", "Job", "Task")):
        ry = gy + 28 + r * 34
        text(16, ry + 6, lvl, 14)
        for i in range(6):
            base("rectangle", gx + i * cw, ry, cw - 10, 28, GRAY, 1)
            text(gx + i * cw + 8, ry + 6, "<sub> · <sub>", 11, GRAY, MONO)
    text(16, vy + 270, "skills   <skill> owns · <skill> works · <skill> shows", 14, INK, MONO)
    text(16, vy + 300, "folders  <bNN>/ · jNN_/ · tNN_/ · runs/ · reports/ · studio/ · delivery/", 14, INK, MONO)
    text(16, vy + 330, "boundary <what this theme never writes>", 14, INK, MONO)
    text(SRC, vy + 40, "guide/guide.yaml  (description, skills, folders, boundary)", 14, INK, MONO)
    text(SRC, vy + 130, "<theme>_theme.py  (Theme.spaces per level: the frame's own words)", 14, INK, MONO)
    path([(SRC - 10, vy + 50), (W - 10, vy + 50)])
    path([(SRC - 10, vy + 140), (W - 10, vy + 160)])
    vy += 460
    # Method
    base("rectangle", 0, vy, W, 300, INK, 1)
    text(16, vy + 12, "Method", 18)
    for i, h in enumerate(("step", "what happens", "methods", "where (six Space › subspace)", "who signs")):
        text(16 + i * 190, vy + 50, h, 13)
    for r in range(3):
        for i, c in enumerate(("<n>", "<does>", "<card>", "Work Details › <sub>", "<who>")):
            text(16 + i * 190, vy + 78 + r * 26, c, 12, GRAY, MONO)
    text(16, vy + 170, "cards: one per method → its papers", 14)
    base("rectangle", 16, vy + 200, 400, 80, GRAY, 1, dashed=True)
    text(28, vy + 228, "methods canvas (embedded, view only)", 13, GRAY)
    text(SRC, vy + 50, "guide/method.md + guide/methods/", 14, INK, MONO)
    text(SRC, vy + 80, "check: 'where' ∉ six Spaces → test fails ?", 14, INK, MONO)
    text(SRC, vy + 230, "guide/methods.excalidraw", 14, INK, MONO)
    path([(SRC - 10, vy + 60), (W - 10, vy + 80)])
    path([(SRC - 10, vy + 240), (420, vy + 240)])
    vy += 340
    # RoadMap Draw
    base("rectangle", 0, vy, W, 160, INK, 1)
    text(16, vy + 12, "RoadMap Draw", 18)
    base("rectangle", 16, vy + 50, 600, 90, GRAY, 1, dashed=True)
    text(28, vy + 82, "<the theme's drawing, embedded; open full screen>", 13, GRAY)
    text(SRC, vy + 60, "Tools/designs/bNN_theme_<theme>/studio/\n  s01-<theme>-ladder/…excalidraw ?", 14, INK, MONO)
    path([(SRC - 10, vy + 70), (620, vy + 90)])
    vy += 200
    # Related Paper
    base("rectangle", 0, vy, W, 140, INK, 1)
    text(16, vy + 12, "Related Paper", 18)
    text(16, vy + 50, "group · role · key · paper · venue · doi · why here · pdf", 13, INK, MONO)
    text(16, vy + 80, "<row> …", 12, GRAY, MONO)
    text(SRC, vy + 50, "related/papers.md + related/papers/", 14, INK, MONO)
    path([(SRC - 10, vy + 60), (W - 10, vy + 60)])
    vy += 180
    text(0, vy, "one folder per theme:  servers/workbench-<theme>/ ── <theme>_theme.py · guide/ · related/", 16, INK, MONO)
    L.close_frame(fr, pad=60)
    return fr["y"] + fr["height"]


# ── status, read live ────────────────────────────────────────────────────────────────────────
def _abs(v):
    p = Path(str(v))
    return p if p.is_absolute() else (TOOLS / p if (TOOLS / p).exists() else TOOLS.parent / p)


def status_rows():
    themes = {p.parent.name: p.name for p in SERVERS.glob("workbench-*/*_theme.py")}
    rows = []
    for fam, e in G.FAMILIES.items():
        home = _abs(e.get("guide_home") or "").resolve()
        folder = home.parent.relative_to(SERVERS.resolve()).as_posix() if home.name == "guide" else "?"
        desc = str(e.get("description", ""))
        six_desc = "yes" if any(s in desc for s in SIX[1:4]) or "frame" in desc else "old board"
        where_ok = "—"
        md = e.get("method_doc")
        if md and _abs(md).is_file():
            spaces = []
            for line in _abs(md).read_text(encoding="utf-8").splitlines():
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if "›" in line and len(cells) >= 4:
                    spaces += [w.split("›")[0].strip() for w in cells if "›" in w]
            bad = sorted({s for s in spaces if s and s not in SIX})
            where_ok = "yes" if spaces and not bad else ("old: " + " · ".join(bad[:4]) if bad else "—")
        draw = ((e.get("explain") or {}).get("roadmap-draw") or (None, {}))[1]
        board = (draw or {}).get("board", "") if isinstance(draw, dict) else ""
        rm = ("ladder" if "ladder" in board else "old board UI" if board else "—")
        theme = themes.get(folder, "no theme file yet") if folder.startswith("workbench-") else "the base"
        rows.append((fam, folder, theme, six_desc, where_ok, rm))
    return rows


def frame_status(y):
    fr = L.open_frame("status · each Guide, read live")
    text(0, y, "Status: each Guide, read off the code at build time", 30)
    text(0, y + 46, "guide/ moved = done for all; the rest is what the proposal changes.", 16, GRAY)
    cols = (0, 140, 420, 640, 860, 1260)
    top = y + 110
    for x, h in zip(cols, ("family", "folder", "theme on the frame", "Description", "Method 'where'", "RoadMap Draw")):
        text(x, top, h, 16)
    path([(0, top + 30), (1500, top + 30)], arrow=False, color=INK)
    for k, row in enumerate(status_rows()):
        ry = top + 44 + k * 28
        for x, c in zip(cols, row):
            text(x, ry, str(c), 13, INK, MONO)
    L.close_frame(fr, pad=60)
    return fr["y"] + fr["height"]


# ── questions ─────────────────────────────────────────────────────────────────────────────────
QUESTIONS = [
    "? 1  This drawing becomes s02 (the Guide's design view), and the old s02 · s03 · s04 fold into one history topic?",
    "? 2  Description's 'Spaces by level' read live from <theme>_theme.py: a Theme then declares its subspaces per level",
    "      without a folder (a small static layout beside spaces()). Agree?",
    "? 3  RoadMap Draw = the theme's s01-<theme>-ladder drawing, or a new drawing of its screens on the frame?",
    "? 4  The work family's Guide key is still 'task' (label 'Task'): rename the key to 'work', or only the label?",
    "? 5  One Guide per theme at every level, or Guide shows what the current level (Block · Job · Task) holds?",
    "? 6  Method's 'where' check: fail the tests, or only warn on the Guide page?",
    "? 7  The old Views Skill set and Folder map: folded into Description (skills, folders), as proposed?",
    "? 8  b03's s03 · s04 · s05 (Block · Job · Task variants: folder → skills → screens): move their screens half to",
    "      b02, move them whole, or keep them in b03 and link them from b02?",
]


def frame_questions(y):
    fr = L.open_frame("questions")
    text(0, y, "What JL decides", 30)
    for k, q in enumerate(QUESTIONS):
        text(0, y + 70 + k * 26, q, 16, INK)
    oy = y + 70 + len(QUESTIONS) * 26 + 20
    base("rectangle", 0, oy, 1500, 200, GRAY, 1)
    text(12, oy + 8, "(write here)", 13, GRAY)
    L.close_frame(fr, pad=60)
    return fr["y"] + fr["height"]


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s05-guide-proposal.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    y = 0
    for draw in (frame_compare, frame_wireframe, frame_status, frame_questions):
        y = draw(y) + 160
    canvas.write(out, list(L.els), "build_s05_guide_proposal.py")


if __name__ == "__main__":
    main()
