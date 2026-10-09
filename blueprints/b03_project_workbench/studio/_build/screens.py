"""Workbench screens drawn at full size, one module for every b03 drawing that shows them.

The style JL chose (261007, "I think the s02 excalidraw is brilliant"; excalidraw-report's "Designing a
workbench"): one full screen per level or per Space, the level tabs, the six Spaces (the open one
outlined), the third row as buttons (the selected one outlined), the content, the Runs panel on the
right; under each screen the folders and files behind it ("on disk"); pop-outs in a last column.
Draws through build_ladder_v4's helpers, so the caller's canvas.write keeps a person's marks.
Used by s02-workbench-shared and s11-block-variants; s04-studio-and-report's studio_report_ui.py keeps
its own copy of the same look for now.
"""
import build_ladder_v4 as L
import run_names

INK, GRAY, RED, TEAL, MONO, SANS = L.INK, L.GRAY, L.RED, L.TEAL, L.MONO, L.SANS
text, path, base = L.text, L.path, L.base
SW, SH, RW, PW = 1500, 760, 360, 900       # a screen; its Runs panel; a pop-out's width
GAP = 120                                  # between two screens
SPACE_ROW = ["Description", "Idea Studio", "Audience Report", "|", "Work Details", "|", "Runs", "Delivery"]
TABS = ["Guide", "Block", "Job · j11 ▾", "Task · t02 ▾"]


def chrome(x, y, tabs, on, space, third, dashed=()):
    """The frame every theme gets: tabs, the six Spaces (the open one outlined), the third row, the panel line."""
    base("rectangle", x, y, SW, SH, INK, 1.5, rough=0)
    tx = x + 24
    for k, tab in enumerate(tabs):
        text(tx, y + 18, tab, 20, INK if k == on else GRAY)
        if k == on:
            path([(tx, y + 48), (tx + len(tab) * 11, y + 48)], arrow=False, color=INK)
        tx += len(tab) * 11 + 46
    sx = x + 24
    for sp in SPACE_ROW:
        if sp == "|":
            text(sx, y + 70, "|", 18, GRAY)
            sx += 26
            continue
        w = len(sp) * 10 + 24
        if sp == space:
            base("rectangle", sx - 8, y + 62, w, 36, INK, 1.5, rough=0)
        elif sp in dashed:                                  # optional: a solid thin line (JL 261008)
            base("rectangle", sx - 8, y + 62, w, 36, GRAY, 1, rough=0)
        text(sx, y + 70, sp, 18, INK if sp == space else GRAY)
        sx += w + 14
    path([(x, y + 112), (x + SW, y + 112)], arrow=False, color=GRAY)
    path([(x + SW - RW, y + 112), (x + SW - RW, y + SH)], arrow=False, color=GRAY)
    px = x + 24
    for k, label in enumerate(third or []):
        w = len(label) * 10 + 34
        base("rectangle", px, y + 128, w, 38, INK if k == 0 else GRAY, 2 if k == 0 else 1, rough=0)
        text(px + 17, y + 136, label, 17, INK if k == 0 else GRAY)
        px += w + 12


def table(x, y, heads, rows, cols=(0, 380, 700)):
    """Column heads, then one boxed row per item; the first cell opens with ↗."""
    for h, c in zip(heads, cols):
        text(x + c + 10, y, h, 16, GRAY)
    for i, row in enumerate(rows):
        ry = y + 30 + i * 70
        base("rectangle", x, ry, SW - RW - 48, 58, GRAY, 1, rough=0)
        for c in cols[1:]:
            path([(x + c, ry), (x + c, ry + 58)], arrow=False, color=GRAY)
        for cell, c in zip(row, cols):
            q = L.question_of(cell) if c == 0 else None
            if q:                                           # the Question cell: label · slug · sentence
                label = f"Question {q[0]}"
                pw = len(label) * 9 + 34
                base("rectangle", x + 10, ry + 6, pw, 22, INK, 1, rough=0)
                text(x + 18, ry + 9, label, 14, INK)
                base("ellipse", x + pw - 6, ry + 12, 9, 9, INK, 1, rough=0)["backgroundColor"] = INK
                text(x + pw + 20, ry + 8, "<slug>" + " ›", 15, INK, MONO)
                text(x + 10, ry + 34, "<one concise sentence: what it asks>", 13, GRAY)
                continue
            text(x + c + 10, ry + 18, cell + (" ↗" if c == 0 else ""), 16, INK, MONO if c == 0 else SANS)


def lines(x, y, rows, size=16):
    """Plain content lines, monospace, top to bottom."""
    for i, ln in enumerate(rows):
        text(x, y + i * 30, ln, size, INK, MONO)


def closed_rows(x, y, names, opened=None):
    """Rows by name only; one may be open, its live drawing across the row (Idea Studio)."""
    w = SW - RW - 48
    for i, name in enumerate(names):
        is_open = i == opened
        base("rectangle", x, y, w, 48, INK if is_open else GRAY, 1, rough=0)
        text(x + 14, y + 12, ("▾ " if is_open else "▸ ") + name, 18, INK, MONO)
        y += 48
        if is_open:
            base("rectangle", x, y, w, 260, GRAY, 1, rough=0)
            base("rectangle", x + 14, y + 14, w - 28, 232, GRAY, 1, dashed=True, rough=0)
            text(x + 34, y + 110, "[ the live drawing: draw here, saved as you go ]", 17, GRAY)
            y += 260
        y += 10
    return y


def runs_panel(x, y, buttons, recent, disk=()):
    """The right panel as the frame draws it (JL 261008): Disk, the files behind the Space, one row each;
    then Runs, one row per button named by the Run it makes, its words small under it (red: no Run name
    yet, open); then the recent Run."""
    rx = x + SW - RW + 20
    text(rx, y + 128, "Disk · Runs", 20)
    yy = y + 166
    files = [ln.strip("├└│─ ") for ln, _ in disk if ln.strip("├└│─ ")][:3]
    for f in files:
        text(rx, yy, "▫ " + L.short(f, 34), 14, GRAY, MONO)
        yy += 24
    text(rx, yy + 8, "Runs", 18)
    yy += 42
    for r in buttons:
        known = run_names.named(r)
        base("rectangle", rx, yy, RW - 40, 50, INK if known else RED, 1, rough=0)
        text(rx + 12, yy + 6, L.short(run_names.name_of(r) if known else r + " ?", 30), 15,
             INK if known else RED, MONO if known else SANS)
        if known:
            text(rx + 12, yy + 28, r.lstrip("+ "), 13, GRAY)
        yy += 58
    if recent:
        text(rx, yy + 8, "recent:\n" + recent, 14, GRAY, MONO)


def note(x, y, line, color=GRAY):
    """A line just under the screen: what the theme changes, or "same as the base"."""
    text(x, y, line, 17, color)


def on_disk(x, y, rows):
    """The folders and files behind the screen, each with what on screen it feeds."""
    text(x, y, "on disk", 22)
    for i, (line, meaning) in enumerate(rows):
        text(x, y + 44 + i * 28, line, 16, INK, MONO)
        if meaning:
            text(x + 520, y + 45 + i * 28, meaning, 15, GRAY)
    return y + 44 + len(rows) * 28


def window(x, y, w, h, title, rows):
    """A pop-out window: a title bar with its close button, then its content; "[ … ]" is a placeholder box."""
    base("rectangle", x, y, w, h, INK, 2, rough=0)
    text(x + 18, y + 14, "↗ " + title, 20, INK)
    text(x + w - 40, y + 12, "×", 22, GRAY)
    path([(x, y + 54), (x + w, y + 54)], arrow=False, color=GRAY)
    yy = y + 72
    for ln in rows:
        if ln.startswith("[") and ln.endswith("]"):
            base("rectangle", x + 18, yy, w - 36, 150, GRAY, 1, dashed=True, rough=0)
            text(x + 34, yy + 62, ln, 16, GRAY)
            yy += 168
        else:
            text(x + 18, yy, ln, 16, INK if ln and not ln.startswith(" ") else GRAY)
            yy += 28


def variant(x0, y0, title, subtitle, tabs, on, spaces, popouts=()):
    """One variant on screen: one full screen per Space, left to right, each with what the theme changes,
    what today shows instead, and the files behind it; the pop-outs last. spaces: a list of dicts with
    space, third, kind (lines | table | rows), content, heads, runs, recent, note, changed, today, disk.
    Returns the frame (open it with L.open_frame before calling, close it after)."""
    text(x0, y0, title, 34)
    text(x0, y0 + 50, subtitle, 20, GRAY)
    for i, sp in enumerate(spaces):
        x, y = x0 + i * (SW + GAP), y0 + 150
        text(x, y0 + 110, sp["space"] + (" › " + sp["third"][0] if sp.get("third") and sp["kind"] == "lines" else ""), 24)
        chrome(x, y, tabs, on, sp["space"], sp.get("third"), dashed=sp.get("dashed", ()))
        top = y + (190 if sp.get("third") else 140)
        if sp["kind"] == "table":
            table(x + 24, top, sp["heads"], sp["content"], sp.get("cols", (0, 380, 700)))
        elif sp["kind"] == "rows":
            closed_rows(x + 24, top, sp["content"], sp.get("opened"))
        else:
            lines(x + 24, top, sp["content"])
        runs_panel(x, y, sp["runs"], sp.get("recent", ""), sp.get("disk", ()))
        note(x, y + SH + 24, sp["note"], TEAL if sp.get("changed") else GRAY)
        note(x, y + SH + 56, "today: " + sp["today"], GRAY)
        on_disk(x, y + SH + 110, sp["disk"])
    px = x0 + len(spaces) * (SW + GAP)
    if popouts:
        text(px, y0 + 110, "pop-out, from a row's ↗", 24)
    py = y0 + 150
    for title_, rows in popouts:
        h = 72 + sum(168 if r.startswith("[") else 28 for r in rows) + 20
        window(px, py, PW, h, title_, rows)
        py += h + 40
