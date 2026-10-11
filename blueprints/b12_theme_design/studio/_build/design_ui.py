"""The Design workbench's proposed screens, shared by b12's level topics (s11 Block, s12 Job, s13 Task).

Borrowed from b11's insight_ui.py (JL 261007: "check s11 s12 and s13 … borrow their ideas"): one level is
one drawing: today -> proposed for its Spaces, then one frame per Space holding all its views, each a full
screen on the shared frame (Guide · Block · Job · Task) with "on disk" under it, then the pop-outs a ↗
opens, then the open questions as loose red notes. The design content follows s00: a Job pins one goal,
one method version and one inputs version, and returns N designs, each a Task.

It reads the design method cards (servers/workbench-design/guide/methods/), so a pop-out shows the card
the Guide shows. Draws through b03's build_ladder_v4 helpers, so a builder's canvas.write keeps a person's
marks. Placeholders only.
"""
import random
import re
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = Path(__file__).resolve().parents[4]
B03 = TOOLS / "blueprints" / "b01_haipipe-toolkit" / "j03_project_workbench" / "studio"    # the shared drawing helpers and the canvas writer
sys.path.insert(0, str(B03 / "s01-overall-tree-structure"))
sys.path.insert(0, str(B03 / "_build"))
import build_ladder_v4 as L  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402

INK, GRAY, RED, TEAL, MONO, SANS = L.INK, L.GRAY, L.RED, L.TEAL, L.MONO, L.SANS
GREEN = L.GREEN                                       # a change note: "✎ <date>  what changed" (JL 261007)
text, box, path, base = L.text, L.box, L.path, L.base
TK = TOOLS / "plugins" / "haipipe-toolkit"
METHODS = TK / "servers" / "workbench-design" / "guide" / "methods"

wrap = lambda s, n: textwrap.wrap(s, n, break_on_hyphens=False) or [""]
read = lambda p: p.read_text(encoding="utf-8", errors="ignore") if p.is_file() else ""


# ── the method cards ─────────────────────────────────────────────────────────────────────────
def card(p):
    """A card: its head (`key: value` before What the literature says), and its Applied to AI skill."""
    whole = read(p)
    head_lines = whole.split("What the literature says")[0].splitlines()
    head, key = {"name": head_lines[0].strip(), "file": p}, None
    for line in head_lines[2:]:
        m = re.match(r"^([a-z ]+): (.*)$", line)
        if m:
            key = m.group(1)
            head[key] = m.group(2).strip()
        elif key and line.startswith("  "):
            head[key] += " " + line.strip()
        elif not line.strip():
            key = None
    m = re.search(r"(?m)^skill: (\S+)(.*)$", whole.split("Applied to AI")[-1])
    head["skill"], head["skill note"] = (m.group(1), m.group(2).strip()) if m else ("", "")
    return head


CARDS = [card(p) for p in sorted(METHODS.glob("*.md"))]


def card_window(name="By insight"):
    """The pop-out a method chip opens: one card, opened, read from its file."""
    c = next((c for c in CARDS if c["name"] == name), CARDS[0])
    return (f"{c['name']}  ·  a method card", [
        (c["file"].relative_to(TK).as_posix(), GRAY),
        ("\n".join(wrap("move  " + c.get("move", ""), 92)), INK),
        ("\n".join(wrap("reads  " + c.get("reads", "") + "   →   returns  " + c.get("returns", ""), 96)), INK),
        ("What the literature says         │  Applied to AI", INK),
        ("  rationale · context · steps ·    │  the agent · steps · returns · verify ·\n"
         "  strengths · limitations          │  AI risk · evidence on AI · skill", GRAY),
        (f"  skill: {c['skill']} {c['skill note']}", RED if "proposed" in c["skill note"] else INK),
        ("\n".join(wrap("tested now  " + c.get("test now", "") + "   ·   in use  " + c.get("test in use", ""), 92)), INK),
        ("the same page as Guide › Method at this card", GRAY)])


# ── one screen on the shared frame ──────────────────────────────────────────────────────────
TABS = {"Guide": "Guide", "Block": "Block", "Job": "Job · j03_<goal>_<design-method> ▾", "Task": "Task · d04 ▾"}
SPACES = ["Description", "|", "Idea Studio", "Audience Report", "|", "Work Details", "|", "Runs", "Delivery"]
GUIDE_SPACES = ["Description", "Method", "RoadMap Draw", "Related Paper"]
SW, SH, RW = 1500, 980, 360                          # one screen; the Runs panel inside it


def screen(x, y, tab, space, third=None, runs=(), recent="", tab_text=None):
    """The level tabs, the Space row, a third row of buttons ("?" = proposed), the Runs panel; returns the
    content box (cx, cy, cw). tab_text: what the open level's tab reads, if not TABS' (e.g. "Task · t00 ▾")."""
    base("rectangle", x, y, SW, SH, INK, 1.5)
    tx = x + 24
    for key, t in TABS.items():
        on = key == tab
        t = tab_text if on and tab_text else t
        text(tx, y + 18, t, 20, INK if on else GRAY)
        if on:
            path([(tx, y + 48), (tx + len(t) * 11, y + 48)], arrow=False, color=INK)
        tx += len(t) * 11 + 46
    sx = x + 24
    for sp in (GUIDE_SPACES if tab == "Guide" else SPACES):
        if sp == "|":
            text(sx, y + 70, "|", 18, GRAY)
            sx += 26
            continue
        w = len(sp) * 10 + 24
        if sp == space:
            base("rectangle", sx - 8, y + 62, w, 36, INK, 1.5, rough=0)
        text(sx, y + 70, sp, 18, INK if sp == space else GRAY)
        sx += w + 14
    path([(x, y + 112), (x + SW, y + 112)], arrow=False, color=GRAY)
    cy = y + 136
    if third:
        px = x + 24
        for label, on in third:
            red = label.startswith("?")
            name = label.lstrip("? ")
            w = len(name) * 10 + 34
            base("rectangle", px, cy - 8, w, 38, RED if red else INK if on else GRAY, 2 if on else 1, dashed=red, rough=0)
            text(px + 17, cy, name, 17, RED if red else INK if on else GRAY)
            px += w + 12
        cy += 56
    path([(x + SW - RW, y + 112), (x + SW - RW, y + SH)], arrow=False, color=GRAY)
    rx = x + SW - RW + 20
    text(rx, y + 132, f"Runs · {space}", 20)
    for i, r in enumerate(runs):                         # each a folding Run card, ▸ its run-<type>-<target> name (JL 261007)
        red = r.startswith("?")
        base("rectangle", rx, y + 176 + i * 54, RW - 40, 40, RED if red else GRAY, 1, dashed=red, rough=0)
        text(rx + 10, y + 185 + i * 54, "▸", 15, GRAY)
        text(rx + 30, y + 185 + i * 54, r.lstrip("? "), 15, RED if red else INK, MONO if r.lstrip("? ").startswith("run-") else SANS)
    text(rx, y + 176 + len(runs) * 54 + 16, recent, 14, GRAY, MONO)
    return x + 24, cy, SW - RW - 48


def chip(x, y, s, w=200, red=False):
    """A small chip: a test or a method; ↗ opens it; red dashed while it is a proposal or a fail."""
    base("rectangle", x, y, w, 26, RED if red else GRAY, 1, dashed=red, rough=0)
    text(x + 8, y + 4, s, 13, RED if red else INK)


def table(cx, cy, cw, heads, cols, rows, mono=(), h=34):
    """A lines-only table: a gray head row, then rows of cells; a string row is a group heading; a cell
    starting "?" is red. Returns its bottom."""
    for t, c in zip(heads, cols):
        text(cx + c + 10, cy, t, 14, GRAY)
    y = cy + 26
    path([(cx, y), (cx + cw, y)], arrow=False, color=GRAY)
    for row in rows:
        if isinstance(row, str):
            text(cx, y + 8, row, 15, INK)
            y += 32
            path([(cx, y), (cx + cw, y)], arrow=False, color=INK)
            continue
        for k, (cell, c) in enumerate(zip(row, cols)):
            red = str(cell).startswith("?")
            text(cx + c + 10, y + 8, str(cell), 14, RED if red else INK, MONO if k in mono else SANS)
        y += h
        path([(cx, y), (cx + cw, y)], arrow=False, color=GRAY)
    return y


def pairs(cx, cy, rows, key_w=180, mono=()):
    """Label · value rows, as on a face; a value starting "?" is red. Returns the bottom."""
    for k, (a, b) in enumerate(rows):
        text(cx, cy + k * 32, a, 14, GRAY)
        text(cx + key_w, cy + k * 32, b, 15, RED if b.startswith("?") else INK, MONO if k in mono else SANS)
    return cy + len(rows) * 32


def fold(x, y, w, title, summary, body=None, red=False, mono_title=False):
    """One folding card (the Job's, s12): ▸ closed, its name and one line; ▾ open, its body as label · value rows.
    red: dashed red, a proposal. Returns its bottom."""
    rows = body or []
    h = 46 + (16 + len(rows) * 32 if rows else 0)
    base("rectangle", x, y, w, h, RED if red else GRAY, 1, dashed=red, rough=0)
    text(x + 14, y + 13, "▾" if rows else "▸", 16, GRAY)
    text(x + 40, y + 12, title, 17, RED if red else INK, MONO if mono_title else SANS)
    text(x + 40 + len(title) * (10.4 if mono_title else 9.6) + 24, y + 15, summary, 14, RED if red else GRAY)
    if rows:
        path([(x, y + 46), (x + w, y + 46)], arrow=False, color=GRAY)
        pairs(x + 40, y + 58, rows, key_w=190)
    return y + h + 10


def phone(x, y, msg):
    """A design as the reader sees it (the Job's Design display, s12): a phone, "Text message", one bubble;
    {LINK} in teal. Returns its bottom."""
    lines = wrap(msg, 30)
    h = 70 + len(lines) * 20
    base("rectangle", x, y, 290, h, GRAY, 1.5, rough=0)
    text(x + 105, y + 10, "Text message", 12, GRAY)
    base("rectangle", x + 14, y + 34, 262, len(lines) * 20 + 22, GRAY, 1, rough=0)["backgroundColor"] = "#f1f3f5"
    for k, ln in enumerate(lines):
        text(x + 26, y + 44 + k * 20, ln, 14, TEAL if "{LINK}" in ln else INK)
    return y + h


# ── the Map: goals down × methods across, a Job chain in each cell (borrowed from b11's Map) ─
GOALS = ["G01 <goal>", "G02 <goal>"]
MCOLS = ["M04 · Actionable insights", "M01 · Goal only", "M05 · Raw-data agent"]   # registered methods (s03), 261007
CELLS = {("G01 <goal>", "M04 · Actionable insights"): ["j01 m1·i1", "j02 m1·i2", "j03 m2·i2"],
         ("G01 <goal>", "M01 · Goal only"): ["j04 m1·i2"],
         ("G02 <goal>", "M01 · Goal only"): ["j05 m1·i2"]}


def goal_map(cx, cy, here=None):
    """Goals down, methods across; each cell is the chain of Jobs on that pair, the newest last.
    here: the Job to outline. Returns the bottom."""
    HX, CW_ = 170, 300
    for k, m in enumerate(MCOLS):
        text(cx + HX + k * CW_ + 10, cy, m, 15, INK, MONO)
    y = cy + 30
    path([(cx, y), (cx + HX + len(MCOLS) * CW_, y)], arrow=False, color=INK)
    for g in GOALS:
        text(cx + 10, y + 16, g, 15, INK)
        for k, m in enumerate(MCOLS):
            jobs = CELLS.get((g, m), [])
            for n, j in enumerate(jobs):
                on = here and j.startswith(here)
                base("rectangle", cx + HX + k * CW_ + 6, y + 6 + n * 34, CW_ - 16, 28,
                     INK if on else GRAY, 3 if on else 1, rough=0)
                text(cx + HX + k * CW_ + 14, y + 11 + n * 34, j + ("  ← this Job" if on else ""), 13,
                     INK if on else GRAY, MONO)
            if not jobs:
                text(cx + HX + k * CW_ + 14, y + 14, "+ Add a Job", 13, GRAY)
        y += max(1, max(len(CELLS.get((g, m), [])) for m in MCOLS)) * 34 + 16
        path([(cx, y), (cx + HX + len(MCOLS) * CW_, y)], arrow=False, color=GRAY)
    return y


# ── under a screen, beside the screens ──────────────────────────────────────────────────────
def note(x, y, s, size=14):
    """A short green change note at the spot that changed: "✎ <date>  what changed" (JL 261007: "for the things we
    change, the very short green comments"). Returns the y below it."""
    text(x, y, "✎ " + s, size, GREEN)
    return y + size * 1.25 + 8


HALF = SW // 2                                         # under a screen: on disk (left half) · skills (right half)


def _tree(x, y, title, lines, color):
    """One half under a screen (JL 261007: "make the disk and skill to be half and half, under the UI"): a heading,
    then a tree, each line with what it does here; the notes start after the longest line and wrap within the half.
    A line starting "✎" is a green change note; "?" = proposed (red). Returns the bottom."""
    if not lines:
        return y
    text(x, y, title, 22)
    w = HALF - 40
    tree = [l for l, _ in lines if not l.startswith("✎")]
    CH = 9.2                                             # a monospaced 14 px character, as it renders
    cap = w * 0.62
    off = min(max([200] + [len(l) * CH + 18 for l in tree if len(l) * CH + 18 <= cap]), cap)
    yy = y + 44
    for line, meaning in lines:
        if line.startswith("✎"):
            for ln in wrap(line, int(w / 7.2)):
                text(x, yy + 2, ln, 13, GREEN)
                yy += 22
            continue
        red = "?" in line or meaning.startswith("?")
        text(x, yy, line, 14, RED if red else color, MONO)
        if meaning and len(line) * CH + 18 > off:          # a long line: its note goes underneath, indented
            yy += 22
        rows = wrap(meaning, max(12, int((w - off) / 6.8))) if meaning else [""]
        for k, ln in enumerate(rows):
            if ln:
                text(x + off, yy + 2 + k * 18, ln, 12, RED if red else GRAY)
        yy += max(26, len(rows) * 18 + 8)
    return yy


def files(x, y, lines):
    """"on disk": the folders and files behind a screen, each with what on screen it feeds (the left half)."""
    return _tree(x, y, "on disk", lines, INK)


def skills_tree(x, y, lines):
    """"skills": the skills a screen's Runs use, as a tree from skills/ (the right half; JL 261007: "in the right
    … we will have skills … from the block level of the skill folder")."""
    return _tree(x, y, "skills", lines, U_BLUE)


U_BLUE = L.BLUE                                         # a skill (b03's colour for skills)


def _split(view):
    """A screen tuple, with or without its 7th element (skills)."""
    return (*view[:6], view[6] if len(view) > 6 else ())


def window(x, y, w, title, rows):
    """A pop-out: a title bar and its rows (text, color); a row in [] is a placeholder box. Returns its bottom."""
    h = 72 + sum(150 if r[0].startswith("[") else 26 * (r[0].count("\n") + 1) + 4 for r in rows) + 20
    base("rectangle", x, y, w, h, INK, 2, rough=0)
    text(x + 18, y + 14, "↗ " + title, 20, INK)
    text(x + w - 40, y + 12, "×", 22, GRAY)
    path([(x, y + 54), (x + w, y + 54)], arrow=False, color=GRAY)
    yy = y + 72
    for s, color in rows:
        if s.startswith("["):
            base("rectangle", x + 18, yy, w - 36, 136, GRAY, 1, dashed=True, rough=0)
            text(x + 34, yy + 56, s, 16, GRAY)
            yy += 150
        else:
            text(x + 18, yy, s, 15, color)
            yy += 26 * (s.count("\n") + 1) + 4
    return y + h


def scratch_questions(x0, y0, notes):
    """The open questions as loose red notes, a little crooked; the same scatter on every build."""
    rnd = random.Random(sum(map(ord, "".join(notes))))
    text(x0, y0, "open ?", 26, RED)
    y, row_h = y0 + 60, 0
    for i, q in enumerate(notes):
        ls = wrap(q.lstrip("? "), 36)
        h = 32 + len(ls) * 30
        if i and i % 3 == 0:
            y, row_h = y + row_h + 40, 0
        nx, ny = x0 + (i % 3) * 540 + rnd.uniform(-16, 16), y + rnd.uniform(-8, 20)
        tilt = rnd.uniform(-0.035, 0.035)
        base("rectangle", nx, ny, 480, h, RED, 1, rough=1)["angle"] = tilt
        text(nx + 18, ny + 14, "\n".join(ls), 18, RED)
        L.els[-1]["angle"] = tilt
        row_h = max(row_h, h + 20)


def aside(x, y, title, rows):
    """A note to the right of a frame's screens: a heading, then (name, what) rows."""
    text(x, y, title, 22)
    for i, (name, what) in enumerate(rows):
        text(x, y + 44 + i * 58, name, 16, RED if name.startswith("?") else INK, MONO)
        text(x, y + 68 + i * 58, what, 14, GRAY)


# ── one level, one drawing ──────────────────────────────────────────────────────────────────
def placed_note(x, y, q):
    """An open question at the screen it decides (JL 261007: "put the questions … to the places for that
    question"): a red box under the screen's "on disk" lines. A note starting "✎" is a decision taken: green."""
    done = q.startswith("✎")
    ls = wrap(q.lstrip("?✎ "), 70)
    base("rectangle", x, y, SW, 30 + len(ls) * 30, GREEN if done else RED, 1.5, rough=1)
    text(x + 18, y + 12, ("✎ " if done else "? ") + "\n".join(ls), 19, GREEN if done else RED)
    return y + 30 + len(ls) * 30 + 16


def _columns(y, level, screens, bands, placed):
    """The bands side by side (level_drawing's side_by_side): one frame per Space, a column per band. Returns
    the y below the last frame."""
    order = [sp for sp in SPACES if sp != "|"]
    cols, x0 = [], 0
    for band, heading, tab_text, scs in bands:
        by = {}
        for sc in (screens if scs is None else scs):
            by.setdefault(sc[0], []).append(sc)
        width = max(len(v) for v in by.values()) * (SW + 120)
        cols.append((band, heading, tab_text, by, x0))
        x0 += width + 240
    for k, (band, heading, tab_text, by, x) in enumerate(cols):   # each column's heading, above the first frame
        text(x, y, heading, 44)
        if k:                                            # the columns' dividing line (JL 261007: vertical lines)
            path([(x - 180, y - 20), (x - 180, y + 110)], arrow=False, color=GRAY)
    y += 140
    for space in order:
        if not any(space in c[3] for c in cols):
            continue
        fr = L.open_frame(f"{level} › {space}")
        text(0, y, f"{level} › {space}", 34)
        text(0, y + 50, "one column per kind of Task, left to right   ·   each a full screen, the folders and files "
                        "behind it underneath; red dashed = proposed", 20, GRAY)
        bottom = y + 300
        for band, heading, tab_text, by, x0 in cols:
            views = by.get(space, [])
            label = heading.split("  ·  ")[0]
            if not views:
                text(x0, y + 120, f"{label} · no {space} at this Task", 24, GRAY)
                continue
            names = [next((lab.lstrip("? ") for lab, on in v[1] or [] if on), "") for v in views]
            for i, view in enumerate(views):
                sp, third, runs, recent, body, lines, sk = _split(view)
                x = x0 + i * (SW + 120)
                text(x, y + 120, f"{label} · {names[i] or space}", 24)
                body(*screen(x, y + 160, level, sp, third, runs, recent, tab_text))
                fb = files(x, y + 160 + SH + 50, lines)
                sb = skills_tree(x + HALF, y + 160 + SH + 50, sk)
                ny = max(fb, sb) + 24
                for band_, sp_, view_, q in placed:
                    if band_ == band and sp_ == sp and view_ in (names[i], ""):
                        ny = placed_note(x, ny, q)
                bottom = max(bottom, ny)
        for band, heading, tab_text, by, x0 in cols[1:]:  # a vertical line between columns, the frame's height
            path([(x0 - 180, y + 100), (x0 - 180, bottom)], arrow=False, color=GRAY)
        L.close_frame(fr, pad=60)
        y = fr["y"] + fr["height"] + 200
    return y


def level_drawing(out, source, level, title, subtitle, moves, screens, popouts, questions, asides=None, changes=(),
                  bands=(), side_by_side=False):
    """moves: [(today, proposed)]; screens: [(space, third, runs, recent, body(cx, cy, cw), files)];
    popouts: [(title, rows)]; questions: ["? …"] (loose, at the end) or (space, view, "? …") (drawn under
    that screen); asides: {space: (title, [(name, what)])}. Writes `out` through canvas.write.
    bands: one level drawn in bands, one per kind of folder at it (s13: a Task per method step):
    [(band, heading, tab_text, screens or None)], in order; None = `screens`. A band's frames are named
    "<level> › <band> › <space>" (band None: "<level> › <space>"), its open tab reads tab_text; a question
    (band, space, view, "? …") and an aside keyed (band, space) belong to it.
    side_by_side: the bands as columns, left to right, instead of one below another: one frame per Space,
    each band's views of that Space in its own column (the columns line up down the drawing), so a row
    compares one Space across the kinds; a band with no view of a Space says so in its column."""
    placed = [q if len(q) == 4 else (None, *q) for q in questions if isinstance(q, tuple)]
    questions = [q for q in questions if not isinstance(q, tuple)]
    L.els.clear()
    L.FRAME[0] = None
    fr = L.open_frame(f"{level} level · today → proposed")
    text(0, 0, title, 34)
    text(0, 50, subtitle, 20, GRAY)
    for k, (a, b) in enumerate(moves):
        text(0, 120 + k * 32, a, 17, GRAY)
        text(520, 120 + k * 32, "→  " + b, 17, RED if "?" in b else INK)
    for k, c in enumerate(changes):                      # changes: green notes for what moved across the drawing
        note(0, 120 + (len(moves) + k) * 32 + 24, c, 17)
    L.close_frame(fr)
    y = fr["y"] + fr["height"] + 300
    if bands and side_by_side:
        y = _columns(y, level, screens, bands, placed)
    for band, heading, tab_text, scs in ((bands or [(None, None, None, None)]) if not side_by_side else []):
        if heading:                                      # a band's heading, above its frames
            text(0, y, heading, 44)
            y += 120
        spaces = []                                      # one frame per Space, its views side by side
        for sc in (screens if scs is None else scs):
            if not spaces or spaces[-1][0] != sc[0]:
                spaces.append((sc[0], []))
            spaces[-1][1].append(sc)
        order = [sp for sp in SPACES if sp != "|"]       # the frames follow the Space row
        spaces.sort(key=lambda sv: order.index(sv[0]) if sv[0] in order else len(order))
        for space, views in spaces:
            names = [next((lab.lstrip("? ") for lab, on in v[1] or [] if on), "") for v in views]
            name = f"{level} › {space}" if band is None else f"{level} › {band} › {space}"
            fr = L.open_frame(name)
            text(0, y, name, 34)
            text(0, y + 50, (" · ".join(n for n in names if n) if len(views) > 1 else "one view") +
                 "   ·   each a full screen, the folders and files behind it underneath; red dashed = proposed", 20, GRAY)
            for i, view in enumerate(views):
                sp, third, runs, recent, body, lines, sk = _split(view)
                x = i * (SW + 120)
                text(x, y + 120, names[i] or space, 24)
                body(*screen(x, y + 160, level, sp, third, runs, recent, tab_text))
                fb = files(x, y + 160 + SH + 50, lines)
                sb = skills_tree(x + HALF, y + 160 + SH + 50, sk)
                ny = max(fb, sb) + 24
                for band_, sp_, view_, q in placed:
                    if band_ == band and sp_ == sp and view_ in (names[i], ""):
                        ny = placed_note(x, ny, q)
            key = space if band is None else (band, space)
            if key in (asides or {}):
                aside(len(views) * (SW + 120), y + 160, *asides[key])
            L.close_frame(fr, pad=60)
            y = fr["y"] + fr["height"] + 200
    fr = L.open_frame(f"{level} › pop-outs")
    text(0, y, "pop-outs, from a ↗ on any screen", 30)
    for i, (t, rows) in enumerate(popouts):
        window(i * 960, y + 60, 900, t, rows)
    L.close_frame(fr, pad=60)
    if questions:
        scratch_questions(0, fr["y"] + fr["height"] + 200, questions)
    canvas.write(out, list(L.els), source)
