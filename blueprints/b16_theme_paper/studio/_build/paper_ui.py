"""The paper workbench's proposed screens, shared by b16's level topics (s11 Block, s12 Job, s13 Task).

One level is one drawing, in the shape of b11's level topics (JL 261007: "add the s11 s12 s13 like
b11"): today -> proposed for that level, then each Space as a full screen on the shared frame
(Guide · Block · Job · Task), "on disk" under it, the pop-outs a ↗ opens, and the open questions as
red notes. Each level also gets one Guide screen: Guide › Method opened from that tab, its level's
section open and the other two folded (b03 s31: one Guide, three sections Block · Job · Task).

The Guide's steps and method cards are read from the paper Guide at build time
(servers/workbench-paper/guide/method.md, its cards in methods/, and the Page Task's guide.yaml), so the
drawings name what the Guide shows. The screen code follows b11's insight_ui.py (paper keeps its own copy:
a theme never depends on another theme) and draws through b03's helpers, so canvas.write keeps a
person's marks. Placeholders only, never project data.
"""
import random
import re
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[3]
B03 = TOOLS / "blueprints" / "b03_project_workbench" / "studio"   # the shared drawing helpers and the canvas writer
sys.path.insert(0, str(B03 / "s01-overall-tree-structure"))
sys.path.insert(0, str(B03 / "_build"))
import build_ladder_v4 as L  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402

INK, GRAY, RED, TEAL, MONO, SANS = L.INK, L.GRAY, L.RED, L.TEAL, L.MONO, L.SANS
GREEN = L.GREEN          # a change note (JL 261007: "add the changes with green color brief comments")
text, path, base = L.text, L.path, L.base
TK = TOOLS / "plugins" / "haipipe-toolkit"
GUIDE = TK / "servers" / "workbench-paper" / "guide"
PAGE_GUIDE = TK / "servers" / "workbench" / "task-page" / "guide" / "guide.yaml"

wrap = lambda s, n: textwrap.wrap(s, n, break_on_hyphens=False) or [""]
read = lambda p: p.read_text(encoding="utf-8", errors="ignore") if p.is_file() else ""


# ── the Guide's steps and cards, read from its files ─────────────────────────────────────────
def md_rows(s, first):
    """The rows of the Markdown table whose head starts with `first`."""
    out, on = [], False
    for line in s.splitlines():
        if line.startswith(f"| {first} |"):
            on = True
            continue
        if on and line.startswith("|---") or on and line.startswith("| ---"):
            continue
        if on and line.startswith("|"):
            out.append([c.strip() for c in line.strip("|").split("|")])
        elif on:
            break
    return out


METHOD = read(GUIDE / "method.md")
CARDS = [r for blk in METHOD.split("| family |")[1:] for r in md_rows("| family |" + blk, "family")]
CARDS = list(dict.fromkeys(tuple(r) for r in CARDS))                    # family · method · card file
FAMILY_LEVEL = {"Framing": "Block", "Story": "Block", "Writing and response": "Job"}


def level_tables(s):
    """{level: [step · what happens · methods · where · who signs]} from method.md's level tables: a bold
    line naming the level (**Block · …**), then a table whose head is `| step |` (the Guide reads the same)."""
    out, level = {}, None
    for line in s.splitlines():
        m = re.match(r"^\*\*(Block|Job|Task)\b", line.strip())
        if m:
            level = m.group(1)
        elif line.startswith("| ") and level and not line.startswith(("| step |", "|---", "| ---")):
            out.setdefault(level, []).append([c.strip() for c in line.strip().strip("|").split("|")])
        elif line.strip() and not line.startswith("|") and level and out.get(level):
            level = None
    return out


STEPS = level_tables(METHOD)


def level_steps(level):
    """(step, what happens, where, signs) for a level, as method.md's level table says."""
    return [(r[0], r[1], r[3], r[4]) for r in STEPS.get(level, [])]


def level_cards(level):
    """(family, method) of the cards a level's section shows: the paper's, or the Page method's at Task."""
    if level == "Task":                              # a Section is a Page: the Page method's cards
        return [(p.parent.name.capitalize(), read(p).splitlines()[0].strip())
                for p in sorted((PAGE_GUIDE.parent / "methods").rglob("*.md"))]
    return [(f.split(":")[0], m) for f, m, _ in CARDS if FAMILY_LEVEL.get(f.split(":")[0]) == level]


# ── one screen on the shared frame ──────────────────────────────────────────────────────────
TABS = {"Guide": "Guide", "Block": "Block", "Job": "Job · j02_v<MMDD>_<desk> ▾", "Task": "Task · t02_method ▾"}
SPACES = ["Description", "|", "Idea Studio", "Audience Report", "|", "Work Details", "|", "Runs", "Delivery"]
GUIDE_SPACES = ["Description", "Method", "RoadMap Draw", "Related Paper"]
SW, SH, RW = 1500, 980, 360                          # one screen; the Runs panel inside it


def screen(x, y, tab, space, third=None, runs=(), recent="", guide=False):
    """The level tabs, the Space row, a third row of buttons ("?" = proposed), the Runs panel; returns the
    content box (cx, cy, cw)."""
    base("rectangle", x, y, SW, SH, INK, 1.5)
    tx = x + 24
    for key, t in TABS.items():
        on = key == ("Guide" if guide else tab)
        text(tx, y + 18, t, 20, INK if on else GRAY)
        if on:
            path([(tx, y + 48), (tx + len(t) * 11, y + 48)], arrow=False, color=INK)
        tx += len(t) * 11 + 46
    sx = x + 24
    for sp in (GUIDE_SPACES if guide else SPACES):
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
    text(rx, y + 132, f"Run types · {space}", 20)
    for i, r in enumerate(runs):
        red = r.startswith("?")
        base("rectangle", rx, y + 176 + i * 54, RW - 40, 40, RED if red else GRAY, 1, dashed=red, rough=0)
        text(rx + 12, y + 184 + i * 54, r.lstrip("? "), 17, RED if red else INK)
    for k, line in enumerate(recent.splitlines()):
        text(rx, y + 176 + len(runs) * 54 + 16 + k * 22, line, 14, GRAY, MONO)
    return x + 24, cy, SW - RW - 48


def changed(cx, y, notes, date="261007"):
    """Brief green notes of what changed here, dated (JL 261007: "for the changes we have made … add the short green
    comments to where we made the changes"); one line each; a note starting "?" was reopened and draws red.
    Returns the bottom."""
    for k, n in enumerate(notes):
        text(cx, y + k * 22, n if n.startswith("?") else f"✎ {date}  {n}", 14, RED if n.startswith("?") else GREEN)
    return y + len(notes) * 22


def third(names, on):
    """A third row: (label, is_open) for each name; "?" marks a proposed one."""
    return [(n, n.lstrip("? ") == on) for n in names]


def table(cx, cy, cw, heads, cols, rows, mono=(), h=34):
    """A lines-only table: a gray head row, then rows of cells; a cell starting "?" is red; a str row is a
    group heading. Returns its bottom."""
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
            text(cx + c + 10, y + 8, str(cell).lstrip("? ") if red and str(cell) != "?" else str(cell), 14,
                 RED if red else INK, MONO if k in mono else SANS)
        y += h
        path([(cx, y), (cx + cw, y)], arrow=False, color=GRAY)
    return y


def lines(cx, cy, rows, size=15, gap=28):
    """Plain lines: (text, color[, mono]); a str is an INK line. Returns the bottom."""
    for i, r in enumerate(rows):
        s, color, font = (r, INK, SANS) if isinstance(r, str) else (r[0], r[1], r[2] if len(r) > 2 else SANS)
        text(cx, cy + i * gap, s, size, color, font)
    return cy + len(rows) * gap


def card(cx, cy, cw, title, second, h=62, red=False, mark="▸"):
    """A Guide card (b03 s31-D06): a title line and a second line, one box; returns its bottom."""
    base("rectangle", cx, cy, cw, h, RED if red else GRAY, 1, dashed=red, rough=0)
    text(cx + 14, cy + 8, f"{mark} {title}", 16, RED if red else INK)
    text(cx + 34, cy + 34, second, 13, RED if red else GRAY)
    return cy + h + 10


def drawing_box(cx, cy, cw, h, label):
    base("rectangle", cx, cy, cw, h, GRAY, 1, dashed=True, rough=0)
    text(cx + 20, cy + h / 2 - 10, label, 15, GRAY)
    return cy + h + 10


def files(x, y, rows):
    """"on disk": the folders and files behind a screen, each with what on screen it feeds; "?" = proposed."""
    text(x, y, "on disk", 22)
    for i, (line, meaning) in enumerate(rows):
        red = "?" in line or meaning.startswith("?")
        text(x, y + 44 + i * 28, line, 15, RED if red else INK, MONO)
        if meaning:
            text(x + 620, y + 45 + i * 28, meaning, 15, RED if red else GRAY)


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


def guide_method(level):
    """Guide › Method, opened from a level's tab: that level's section open (its steps and cards), the other
    two folded to one line (b03 s31-D05, D07). A screen spec for level_drawing."""
    def body(cx, cy, cw):
        text(cx, cy, "how a paper is made, cut by level: the steps, then the method cards", 15, GRAY)
        y = cy + 40
        for lv in ("Block", "Job", "Task"):
            steps, cards = level_steps(lv), level_cards(lv)
            if lv != level:
                text(cx, y, f"▸ {lv}   {len(steps)} steps · {len(cards)} cards", 18, GRAY)
                y += 40
                continue
            text(cx, y, f"▾ {lv}", 20, INK)
            y += 38
            for i, (s, w, where, signs) in enumerate(steps, start=1):
                red = where.startswith("?") or where.endswith("?")
                y = card(cx, y, cw, f"{s if s[:1].isdigit() else f'{i} · {s}'}   {w[:70]}", f"where: {where}" + (f" · signs: {signs}" if signs else ""),
                         red=red)
            text(cx, y + 4, "method cards", 15, GRAY)
            y += 30
            for k, (fam, m) in enumerate(cards):               # one line each, two columns, so a level fits
                col, row = k % 2, k // 2
                text(cx + 14 + col * (cw // 2), y + row * 30, f"▸ {m} ↗   · {fam}", 15, INK)
            y += ((len(cards) + 1) // 2) * 30 + 10
        return y
    return ("Method", None, ["Add a method", "Add a paper"], "",
            body, [("servers/workbench-paper/guide/method.md", "the steps · ? a Block · Job · Task part each"),
                   ("servers/workbench-paper/guide/methods/<family>/", "one card per method"),
                   ("servers/workbench/task-page/guide/guide.yaml", "the Task section: the Page method")], True)


# ── the open questions, loose ───────────────────────────────────────────────────────────────
def scratch_questions(x0, y0, notes):
    """The open questions as loose red notes, a little crooked, the same scatter on every build."""
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


# ── one level, one drawing ──────────────────────────────────────────────────────────────────
GAP = 220                                            # between two Space frames, across and down


def level_drawing(out, source, level, title, subtitle, moves, screens, popouts, questions, notes=None,
                  today=None, changes=()):
    """moves: [(today, proposed)]; screens: [(space, third, runs, recent, body(cx, cy, cw), files[, guide])];
    popouts: [(title, rows)]; questions: ["? …"]. Each Space is its own frame (JL 261007: "each space to be a
    frame"), named for the screen, holding the screen and its "on disk"; the pop-outs and the open questions
    are a frame each. notes: one [(heading, text)] per screen; given, each Space is a row, the screen on the
    left and its explanation on the right (JL 261007: "each space to be a row … in the right … text to
    explain them"); left out, three screens to a row. Writes `out` through canvas.write."""
    L.els.clear()
    L.FRAME[0] = None
    fr = L.open_frame(f"{level} level · today → proposed")
    text(0, 0, title, 34)
    text(0, 50, subtitle, 20, GRAY)
    for k, (a, b) in enumerate(moves):
        text(0, 120 + k * 32, a, 17, GRAY)
        text(460, 120 + k * 32, "→  " + b, 17, RED if "?" in b else INK)
    changed(0, 120 + len(moves) * 32 + 16, changes)       # what changed on this drawing, in green
    L.close_frame(fr)
    y0 = fr["y"] + fr["height"] + 300
    text(0, y0, f"{level} tab: one {'row' if notes else 'frame'} per Space, then Guide › Method from this tab", 34)
    text(0, y0 + 50, ("Green ✎ = what changed, dated. " if changes else "") + ("Each row is one Space: its screen, the folders and files behind it, and what it is and why on the "
                      "right. " if notes else "Each frame is one Space as a full screen, the folders and files behind it "
                      "under it. ") + "Red = proposed or open, not on screen today. Placeholders only.", 20, GRAY)
    ty = y0 + 320                                       # room above the first frame for its name
    if notes:
        return _rows_drawing(out, source, level, ty, screens, popouts, questions, notes, today or {})
    row_h = 40 + SH + 50 + 44 + max(len(s[5]) for s in screens) * 28 + GAP
    for i, spec in enumerate(screens):
        space, thr, runs, recent, body, rows = spec[:6]
        guide = len(spec) > 6 and spec[6]
        x, y = (i % 3) * (SW + GAP), ty + (i // 3) * row_h
        sel = next((lab.lstrip("? ") for lab, on in thr or [] if on), None)
        head = f"Guide › {space}, from the {level} tab" if guide else \
            f"{level} tab › {space}" + (f" › {sel}" if sel and len(thr) > 1 else "")
        fr = L.open_frame(f"{i + 1:02d} · {head}")
        text(x, y, head, 24)
        body(*screen(x, y + 40, level, space, thr, runs, recent, guide))
        files(x, y + 40 + SH + 50, rows)
        L.close_frame(fr, pad=40)
    px, py = 3 * (SW + GAP), ty
    fr = L.open_frame("pop-outs")
    text(px, py, "pop-out, from a ↗", 24)
    py += 40
    for t, rows in popouts:
        py = window(px, py, 900, t, rows) + 40
    L.close_frame(fr, pad=40)
    bottom = max(e["y"] + e.get("height", 0) for e in L.els)
    fr = L.open_frame("open ?")
    scratch_questions(0, bottom + 260, questions)
    L.close_frame(fr, pad=50)
    canvas.write(out, list(L.els), source)


NW = 1400                                            # the explanation column beside a row's screen


def explain(x, y, paras):
    """The text beside a screen: a heading, then its paragraph, wrapped; "?" in a paragraph draws it red.
    Returns the bottom."""
    for head, body in paras:
        ink = GREEN if head.startswith("✎") else INK         # a "✎ <date>" paragraph says what changed, in green
        text(x, y, head, 22, ink)
        y += 40
        settled, _, open_ = body.partition("? ")              # the open part, from its "?", draws red
        for part, color in ((settled, ink), ("? " + open_ if open_ else "", RED)):
            for line in (wrap(part, 112) if part.strip() else []):
                text(x, y, line, 18, color)
                y += 28
        y += 26
    return y


def _rows_drawing(out, source, level, ty, screens, popouts, questions, notes, today=None):
    """One frame per Space (JL 261007: "they are from the same space … should be in one frame"): its screens,
    one per third-row choice, stacked top to bottom, each with its "on disk" on the left and its explanation
    on the right; the pop-outs to the right of the first frames; the open questions under all."""
    groups = []                                          # consecutive screens of one Space share a frame
    for spec, paras in zip(screens, notes):
        key = ("Guide", spec[0]) if len(spec) > 6 and spec[6] else ("tab", spec[0])
        if groups and groups[-1][0] == key:
            groups[-1][1].append((spec, paras))
        else:
            groups.append((key, [(spec, paras)]))
    y, right = ty, 0
    for i, ((kind, space), rows_) in enumerate(groups):
        title = f"Guide › {space}, from the {level} tab" if kind == "Guide" else f"{level} tab › {space}"
        fr = L.open_frame(f"{i + 1:02d} · {title}")
        y += 70                                          # the frame's name sits in this band, above the screens
        x, bottom, paras_all = 0, y, []
        for spec, paras in rows_:                        # one Space's screens, left to right (JL 261007, as s13)
            _, thr, runs, recent, body, rows = spec[:6]
            sel = next((lab.lstrip("? ") for lab, on in thr or [] if on), None)
            sub = f"› {sel}" if sel and len(thr) > 1 else title
            text(x, y, sub, 24)
            body(*screen(x, y + 40, level, space, thr, runs, recent, kind == "Guide"))
            files(x, y + 40 + SH + 50, rows)
            low = y + 40 + SH + 50 + 44 + len(rows) * 28
            was = (today or {}).get((space, sel or ""))
            if was:                                      # today's screen under it: the old page doing this job
                text(x, low + 60, "today · " + was[0], 22, GRAY)
                low = old_screen(x, low + 100, *was[1:])
            bottom = max(bottom, low)
            paras_all += ([(sub, "")] if len(rows_) > 1 else []) + list(paras)
            x += SW + 120
        bottom = max(bottom, explain(x, y + 40, paras_all))  # one text column after the last screen
        right = max(right, x + NW)
        L.close_frame(fr, pad=40)
        fr["y"] -= 50                                    # make room for the name inside the frame's top band
        fr["height"] += 50
        y = bottom + GAP
    px, py = right + GAP, ty
    fr = L.open_frame("pop-outs")
    text(px, py, "pop-out, from a ↗", 24)
    py += 40
    for t, rows in popouts:
        py = window(px, py, 900, t, rows) + 40
    L.close_frame(fr, pad=40)
    fr = L.open_frame("open ?")
    scratch_questions(0, y + 60, questions)
    L.close_frame(fr, pad=50)
    canvas.write(out, list(L.els), source)


# ── today: the old paper page (/_board/paper-board), the screen a proposal replaces ─────────────────
OLD_SPACES = ["Guide", "Ideation", "Story", "Sections", "Delivery"]


def old_screen(x, y, space, views, view, lines, runs=()):
    """The old paper page as it is today: its band, its four Spaces after Guide, the open Space's views, the
    content, and the Runs panel folded to a strip on the right. Gray and dashed: it is what exists, not the
    proposal. Returns the bottom."""
    h = 560
    base("rectangle", x, y, SW, h, GRAY, 1, dashed=True, rough=0)
    base("rectangle", x + 20, y + 16, SW - 40, 36, GRAY, 1, rough=0)
    text(x + 34, y + 24, "<desk> · Story v<n> · <N> questions · <N> Sections · built or not", 15, GRAY)
    sx = x + 20
    for sp in OLD_SPACES:
        w = len(sp) * 10 + 30
        base("rectangle", sx, y + 66, w, 34, INK if sp == space else GRAY, 1.5 if sp == space else 1, rough=0)
        text(sx + 14, y + 73, sp, 17, INK if sp == space else GRAY)
        sx += w + 10
    vx = x + 34
    for v in views:
        w = len(v) * 9 + 26
        base("rectangle", vx, y + 120, w, 30, INK if v == view else GRAY, 1.5 if v == view else 1, rough=0)
        text(vx + 12, y + 126, v, 15, INK if v == view else GRAY)
        vx += w + 8
    for k, line in enumerate(lines):
        red = line.startswith("?")
        text(x + 34, y + 176 + k * 28, line, 15, RED if red else INK, MONO if line.startswith(("│", "RQ", "S-")) else SANS)
    base("rectangle", x + SW - 60, y + 66, 36, 120, GRAY, 1, rough=0)
    text(x + SW - 52, y + 84, "R\nu\nn\ns", 14, GRAY)
    if runs:
        text(x + 34, y + h - 40, "Runs (folded): " + " · ".join(runs), 14, GRAY)
    return y + h
