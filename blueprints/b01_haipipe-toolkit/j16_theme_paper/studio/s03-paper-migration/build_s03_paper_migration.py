"""b16 s03 · paper migration: s03-paper-migration.excalidraw, how the old paper folders and the old paper page
move to the new ladder and the shared frame, as a plain prototype (JL 261007: rewritten, "very badly written"
before; lines-only boxes, few words, red only for the open points).

Frames, top to bottom: 00 the move in one picture (old tree → new tree, a level beside each line); one frame per
level, Block · Job · Task, each the old tree │ the new tree with one word per line (kept · new · moved · rebuilt ·
regenerated · open) and a short why, then the screen change and what is found on disk today (counts only);
then the steps as boxes and arrows; then what is open.

The shell is shared, the level parts are their sessions' files, as in s31: migration_block.py and
migration_job.py (-job session), migration_task.py (-task session). Each exports LEVEL, OLD, NEW, SCREEN,
COUNTS and OPEN, and may export CHANGES ["what changed, briefly"], drawn green under its frame (JL 261007: "add the
short green comments to where we made the changes"); a why starting "✎" draws green too. Earlier versions, with their tables, are kept in history/. Drawn with b04's studio helpers
through b03's canvas.write, so a person's marks survive a rebuild.

    python build_s03_paper_migration.py [out.excalidraw]
"""
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2].parent / "b01_haipipe-toolkit" / "j04_skill_folder" / "studio" / "_build"))
from sketch import GRAY, GREEN, INK, MONO, RED, SANS, arrow, base, close_frame, open_frame, save, text  # noqa: E402

LINE = 26                                              # one tree line
STEPS = [("settle", "you", "a yes per open point"),
         ("readers read both", "agent", "tests on two demo Boards, old and new layout"),
         ("dry run", "agent", "a printed plan: every move, heading, toml path, link"),
         ("one Board", "agent + you", "it opens, builds, its links resolve"),
         ("the rest", "agent + you", "the same checks, one Board at a time"),
         ("retire the old page", "agent", "nothing reads the old layout")]
ONE_PICTURE_OLD = ["Paper-<Name>/", "├── board.md", "├── A1-Story/", "│   ├── Story00-<direction>/",
                   "│   └── Story<L>-<desk>-<idea>/", "├── Ba-<desk>-Main/S-…/", "├── Bb-<desk>-Appendix/S-…/",
                   "├── Bc-<desk>-Round/RD<NN>/", "├── delivery/", "├── _venue/", "└── studio/ · reports/"]
ONE_PICTURE_NEW = [("Paper-<Name>/", "Block"), ("├── board.md", ""),
                   ("├── studio/s01-ideation/ · sNN-story-<telling>/", ""),
                   ("├── reports/qNN_<question>/  (## Questions in board.md)", ""),
                   ("├── j01_v<MMDD>_<desk>/", "Job"), ("│   ├── t0N_<title>/ · t2N_<title>/", "Task"),
                   ("│   ├── t31_cover-letter/ · t32_response/", "Task"),
                   ("│   ├── studio/ · runs/ · reports/  (reports/qNN_<kind>-<MMDD>/: comments)", ""),
                   ("│   └── delivery/", ""), ("├── venues/<venue>/ · related/", ""), ("└── reports/", "")]
CHANGES = ["Sections are renamed t0N_<title>/ (t2N_ appendix) and the version dated j01_v<MMDD>_<desk>/ (was: names stay)",
           "the Story is not a j00_story/ Job",
           "the Story becomes studio topics (s01-ideation/, sNN-story-<telling>/) and Board Questions with reports (Q04)",
           "a version carries studio/ · reports/ · runs/; a comments batch is not a Task",
           "a comments batch is a report of type comments: reports/qNN_<kind>-<MMDD>/ (page-type: comments)",
           "t3N_ is Letters: t31 cover letter · t32 response"]


def changed(x, y, notes, date="261007"):
    """Brief green notes of what changed, dated; returns the bottom."""
    for k, n in enumerate(notes):                       # a note starting "?" was reopened: red
        text(x, y + k * 24, n if n.startswith("?") else f"✎ {date}  {n}", 16, RED if n.startswith("?") else GREEN)
    return y + len(notes) * 24


def part(level):
    """A level's file, or None when its session has not written it."""
    try:
        return importlib.import_module(f"migration_{level.lower()}")
    except ModuleNotFoundError:
        return None


def box(x, y, title, lines, w=None, mono=True):
    """A lines-only box with a title above it; a line starting "?" draws red. Returns (right, bottom)."""
    w = w or max(len(l) for l in lines) * 15 * 0.6 + 40
    text(x, y, title, 18, GRAY)
    top = y + 32
    base("rectangle", x, top, w, 20 + len(lines) * LINE, INK, sw=1, rough=0)
    for i, l in enumerate(lines):
        text(x + 18, top + 12 + i * LINE, l, 15, RED if l.lstrip().startswith("?") or " ? " in l else INK, MONO if mono else SANS)
    return x + w, top + 20 + len(lines) * LINE


def tagged(x, y, title, rows):
    """The new tree: a line, what happens to it (one word), why; "open" draws red. Returns (right, bottom)."""
    lw = max(len(l) for l, _, _ in rows) * 15 * 0.6 + 30
    ww = max(len(w) for _, _, w in rows) * 15 * 0.55 + 20
    w = 18 + lw + 120 + ww + 20
    text(x, y, title, 18, GRAY)
    top = y + 32
    base("rectangle", x, top, w, 20 + len(rows) * LINE, INK, sw=1, rough=0)
    for i, (line, tag, why) in enumerate(rows):
        yy, c = top + 12 + i * LINE, RED if tag == "open" else INK
        text(x + 18, yy, line, 15, c, MONO)
        text(x + 18 + lw, yy, tag, 15, c)
        text(x + 18 + lw + 120, yy, why, 15, RED if tag == "open" else GREEN if why.startswith("✎") else GRAY)
    return x + w, top + 20 + len(rows) * LINE


def frame_one_picture(y0):
    fr = open_frame("00 · the move in one picture")
    text(0, y0, "00 · the move in one picture", 30)
    text(0, y0 + 44, "Folders move and Sections take their Task names; a record file lets the rename roll back.",
         18, GRAY)
    r1, b1 = box(0, y0 + 100, "old: today", ONE_PICTURE_OLD)
    r2, _ = box(r1 + 200, y0 + 100, "new: the ladder", [l for l, _ in ONE_PICTURE_NEW])
    mid = (y0 + 132 + b1) / 2
    arrow(r1 + 30, mid, r1 + 170, mid)
    for i, (_, lvl) in enumerate(ONE_PICTURE_NEW):
        if lvl:
            text(r2 + 20, y0 + 144 + i * LINE, lvl, 15, GRAY)
    changed(0, max(b1, y0 + 152 + len(ONE_PICTURE_NEW) * LINE) + 30, CHANGES)
    return close_frame(fr)


def frame_level(y0, level, p):
    fr = open_frame(f"{level} · old → new, on disk and on screen")
    text(0, y0, level, 30)
    if p is None:
        text(0, y0 + 50, f"(not drawn yet: its session writes migration_{level.lower()}.py)", 18, GRAY)
        return close_frame(fr)
    r1, b1 = box(0, y0 + 60, "old on disk", p.OLD)
    r2, b2 = tagged(r1 + 160, y0 + 60, "new on disk  ·  what happens  ·  why", p.NEW)
    arrow(r1 + 30, y0 + 132, r1 + 130, y0 + 132)
    y = max(b1, b2) + 50
    r3, b3 = box(0, y, "on screen: the old page", [a for a, _ in p.SCREEN],
                 w=max(len(a) for a, _ in p.SCREEN) * 15 * 0.55 + 40, mono=False)
    r4, b4 = box(r3 + 160, y, "→ the new tab", [b for _, b in p.SCREEN], mono=False)
    for i in range(len(p.SCREEN)):
        yy = y + 53 + i * LINE
        arrow(r3 + 20, yy, r3 + 140, yy)
    y = max(b3, b4) + 40
    text(0, y, "found on disk today:  " + "  ·  ".join(f"{what} {n}" for what, n in p.COUNTS), 16, GRAY)
    changed(0, y + 40, getattr(p, "CHANGES", []))
    return close_frame(fr)


def frame_steps(y0):
    fr = open_frame("the steps")
    text(0, y0, "the steps", 30)
    text(0, y0 + 44, "One Board at a time, only when no session works in it; the old page stays linked until the last "
                     "step.", 18, GRAY)
    x, y, w, h = 0, y0 + 110, 330, 150
    for i, (name, who, check) in enumerate(STEPS):
        base("rectangle", x, y, w, h, INK, sw=1, rough=0)
        text(x + 18, y + 14, f"{i} · {name}", 19, INK)
        text(x + 18, y + 52, who, 15, GRAY)
        line, ly = "", y + 84
        for wd in check.split():                       # wrap the check inside the box
            if len(line) + len(wd) > 34:
                text(x + 18, ly, line, 15, INK)
                line, ly = wd, ly + 24
            else:
                line = (line + " " + wd).strip()
        text(x + 18, ly, line, 15, INK)
        if i < len(STEPS) - 1:
            arrow(x + w + 8, y + h / 2, x + w + 62, y + h / 2)
        x += w + 70
    return close_frame(fr)


def frame_open(y0, parts):
    fr = open_frame("open")
    text(0, y0, "open", 30, RED)
    lines = [o for lv in ("Block", "Job", "Task") if parts[lv] for o in parts[lv].OPEN]
    for i, o in enumerate(lines):
        text(0, y0 + 56 + i * 32, o, 18, RED)
    return close_frame(fr)


def main():
    parts = {lv: part(lv) for lv in ("Block", "Job", "Task")}
    text(0, -110, "b16 s03 · moving the old paper folders and the old paper page to the new ladder", 40)
    text(0, -52, "A plain prototype: placeholders only; counts read from disk, never a name. Red = open. "
                 "Green ✎ = what changed, dated.", 18, GRAY)
    y = frame_one_picture(60) + 220
    for lv in ("Block", "Job", "Task"):
        y = frame_level(y, lv, parts[lv]) + 220
    y = frame_steps(y) + 220
    frame_open(y, parts)
    save(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s03-paper-migration.excalidraw",
         "build_s03_paper_migration.py")


if __name__ == "__main__":
    main()
