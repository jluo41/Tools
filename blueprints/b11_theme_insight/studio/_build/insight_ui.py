"""The Insight workbench's proposed screens, shared by b11's level topics (s11 Block, s12 Job, s13 Task)
and its methods topic (s03). One level is one drawing: today -> proposed for its Spaces, then the six
Spaces as full screens on the shared frame (Guide · Block · Job · Task), each with "on disk" under it,
the pop-outs a ↗ opens, and the open questions in red.

It also reads the method cards (their head, their skill, the DIKW levels their taxonomy line fits), so
every drawing names the same cards the Guide shows. Draws through b03's build_ladder_v4 helpers, so a
builder's canvas.write keeps a person's marks.
"""
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
GREEN = "#2f9e44"                                          # a dated "✎ <yymmdd>" change note (JL 261007)
text, box, path, base = L.text, L.box, L.path, L.base
TK = TOOLS / "plugins" / "haipipe-toolkit"
SERVER = TK / "servers" / "workbench-insight"
GUIDE = SERVER / "guide"
PAPERS = SERVER / "related" / "papers.md"
ASKING = TK / "skills" / "1_base" / "question" / "haipipe-question-asking"
INSIGHT = TK / "skills" / "2_theme" / "insight"

wrap = lambda s, n: textwrap.wrap(s, n, break_on_hyphens=False) or [""]
read = lambda p: p.read_text(encoding="utf-8", errors="ignore") if p.is_file() else ""
rel = lambda p: p.relative_to(TOOLS).as_posix()


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
    head["skill exists"] = bool(head["skill"]) and any((TK / "skills").rglob(head["skill"]))
    return head


FAMS = [  # (family, 中文, step, its question, card folder, the step whose tests check it)
    ("Question-asking", "提问", 1, "what exactly are we asking, and what would answer it?", ASKING / "methods", 2),
    ("Question-answering", "求答", 3, "how does the run find the answer: look first, or ask first?", GUIDE / "methods/answer", 4),
    ("Question-results reading", "解读", 5, "does the answer survive the ways it could be wrong?", GUIDE / "methods/read", 5)]
CARDS = {f[0]: [card(p) for p in sorted(f[4].glob("*.md"))] for f in FAMS}
ALL = [c for f in FAMS for c in CARDS[f[0]]]
future = lambda c: c.get("status", "").startswith("future")
LEVELS = "DIKW"


def fits(c):
    """The DIKW levels a card fits, read from its own taxonomy line (D · I = description, K = prediction or
    causal inference, W = a decision that uses them [Hernán 2019]; the mapping is the cards' own)."""
    t = c.get("taxonomy", "")
    if re.search(r"\bany\b|names one", t, re.I) or all(w in t for w in ("Data", "Information", "Knowledge", "Wisdom")):
        return set(LEVELS)
    named = {w[0] for w in ("Data", "Information", "Knowledge", "Wisdom") if re.search(rf"\b{w}\b", t)}
    if named:
        return named
    out = set()
    if "description" in t:
        out |= {"D", "I"}
    if "causal" in t or "prediction" in t:
        out |= {"K"}
    return out


def fitting(level, fams=FAMS, now_only=True):
    """The names of the cards that fit a DIKW level, without "By", the future ones left out."""
    return [c["name"].replace("By ", "") for f in fams for c in CARDS[f[0]]
            if level in fits(c) and not (now_only and future(c))]


# ── one screen on the shared frame ──────────────────────────────────────────────────────────
TABS = {"Guide": "Guide", "Block": "Block", "Job": "Job · j03_p2_<d>v2 ▾", "Task": "Task · K01 ▾"}
SPACES = ["Description", "|", "Idea Studio", "Audience Report", "|", "Work Details", "|", "Runs", "Delivery"]
GUIDE_SPACES = ["Description", "Method", "RoadMap Draw", "Related Paper"]
SW, SH, RW = 1500, 1200, 360                          # one screen; the Runs panel inside it
BAND = {}                                            # tab -> one line beside the level tabs, set by a builder


def screen(x, y, tab, space, third=None, runs=(), recent=""):
    """The level tabs, the Space row, a third row of buttons ("?" = proposed), the Runs panel; returns the
    content box (cx, cy, cw)."""
    base("rectangle", x, y, SW, SH, INK, 1.5)
    tx = x + 24
    for key, t in TABS.items():
        on = key == tab
        text(tx, y + 18, t, 20, INK if on else GRAY)
        if on:
            path([(tx, y + 48), (tx + len(t) * 11, y + 48)], arrow=False, color=INK)
        tx += len(t) * 11 + 46
    if BAND.get(tab):                                    # the level's band: what this tab is, in one line
        text(tx + 10, y + 22, BAND[tab], 14, GRAY, MONO)
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
    for row in (third if third and isinstance(third[0], list) else [third] if third else []):   # one or more rows
        px = x + 24
        for label, on in row:
            if label == "|":                          # a divider between groups of buttons
                text(px, cy, "|", 18, GRAY)
                px += 24
                continue
            if label.endswith(":"):                   # a group's label: Data: Dataset · Partitions
                text(px, cy, label, 16, GRAY)
                px += len(label) * 9 + 10
                continue
            red = label.startswith("?")
            name = label.lstrip("? ")
            w = len(name) * 10 + 34
            base("rectangle", px, cy - 8, w, 38, RED if red else INK if on else GRAY, 2 if on else 1, dashed=red, rough=0)
            text(px + 17, cy, name, 17, RED if red else INK if on else GRAY)
            px += w + 12
        cy += 52
    path([(x + SW - RW, y + 112), (x + SW - RW, y + SH)], arrow=False, color=GRAY)
    rx = x + SW - RW + 20
    text(rx, y + 132, f"Runs · {space}", 20)
    for i, r in enumerate(runs):
        red = r.startswith("?")
        base("rectangle", rx, y + 176 + i * 54, RW - 40, 40, RED if red else GRAY, 1, dashed=red, rough=0)
        text(rx + 12, y + 184 + i * 54, r.lstrip("? "), 17, RED if red else INK)
    text(rx, y + 176 + len(runs) * 54 + 16, recent, 14, GRAY, MONO)
    return x + 24, cy, SW - RW - 48


def chip(x, y, s, w=300):
    """A method chip: the card's name, ↗ opens the card; red dashed while it is a proposal."""
    base("rectangle", x, y, w, 26, RED, 1, dashed=True, rough=0)
    text(x + 8, y + 4, s + " ↗", 13, RED)


def table(cx, cy, cw, heads, cols, rows, mono=(), h=34):
    """A lines-only table: a gray head row, then rows of cells; a cell starting "?" is red. Returns its bottom."""
    for t, c in zip(heads, cols):
        text(cx + c + 10, cy, t, 14, GRAY)
    y = cy + 26
    path([(cx, y), (cx + cw, y)], arrow=False, color=GRAY)
    for row in rows:
        if isinstance(row, str):                    # a group heading across the table
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


# ── the question table: Logic │ Work │ Report under D · I · K · W headings ───────────────────
LEVEL = {"D": ("Data", "counts, what was seen"),        # a DIKW level groups a Job's questions (s00, 261007)
         "I": ("Information", "rates and contrasts, never \"because\""),
         "K": ("Knowledge", "one claim, how sure, its rivals, its limits"),
         "W": ("Wisdom", "advice, signed by a person, for Design")}
ROWS = {  # level -> its questions: (id, ask method, answer method, read method), placeholders for any board
    "D": [("D01", "By level", "By exploring", None)],
    "I": [("I01", "By analysis plan", "By exploring", "By heterogeneity")],
    "K": [("K01", "By estimand", "By hypothesis test", "By multiverse"),
          ("K02", "By partition and power", "By model comparison", "By heterogeneity")],
    "W": [("W01", "By goal-question-metric", None, "By sensemaking")]}
TCOLS = [0, 340, 680]
PARTS = [("Full", 0), ("<partition A>", 1), ("<partition B>", 0), ("Cross", 0)]


def dikw_table(cx, cy, cw, levels, report=None, run="r02_<partition A>", work=None, chips=None, heads=None, note=None):
    """Questions under D · I · K · W, a row each: Logic │ Work │ Report, a line in each cell and a chip under it.
    The Job draws its own Runs and the questions' three methods; the Block's readings pass their own cells:
    work(level, id) the Work line, report(level, id) the Report line, chips(level, id, ask, answer, read) the
    three chips (None skips one), heads the column heads, note(level) a line beside each heading."""
    heads = heads or ["Logic · the question (Prototype p2)", f"Work · its run, {run}", "Report · its page"]
    for h, c in zip(heads, TCOLS):
        text(cx + c + 10, cy, h, 15, GRAY)
    ry = cy + 30
    for lv in levels:
        name, say = LEVEL[lv]
        n = len(ROWS[lv])
        text(cx, ry, f"{lv} · {name}  ·  {n} question{'s' if n > 1 else ''}", 16, INK)
        line = note(lv) if note else "may say: " + say
        text(cx + 420, ry + 2, line, 13, TEAL if note else GRAY)
        path([(cx, ry + 26), (cx + cw, ry + 26)], arrow=False, color=INK)
        ry += 36
        for qid, ask, ans, rd in ROWS[lv]:
            base("rectangle", cx, ry, cw, 96, GRAY, 1, rough=0)
            for c in TCOLS[1:]:
                path([(cx + c, ry), (cx + c, ry + 96)], arrow=False, color=GRAY)
            text(cx + 10, ry + 8, f"{qid} · <question> ↗   signed ✅", 14, INK)
            wk = work(lv, qid) if work else (f"{run} ● ok ↗" if lv != "W" else "cites K01 · I01")
            text(cx + TCOLS[1] + 10, ry + 8, "\n".join(wrap(wk, 36)), 13, INK, MONO)
            rep = report(lv, qid) if report else "Answer: <one line> · CHECK ✅"     # report(level, id): the Report cell
            text(cx + TCOLS[2] + 10, ry + 8, "\n".join(wrap(rep, 44)), 14, RED if rep.startswith("?") else INK)
            marks = chips(lv, qid, ask, ans, rd) if chips else [ask and f"ask: {ask}", ans and f"answer: {ans}", rd and f"read: {rd}"]
            for c, m in zip(TCOLS, marks):
                if m:
                    chip(cx + c + 10, ry + 60, m, 310)
            ry += 106
        ry += 8
    return ry


def qwr(cx, cy, cw, heads, groups):
    """Any Question │ Work │ Report table (the shape every Audience Report keeps): groups = [(heading, note,
    rows)], each row (logic, work, report, chips), chips = [(column 0-2, text)]; a cell starting "?" is red."""
    for h, c in zip(heads, TCOLS):
        text(cx + c + 10, cy, h, 15, GRAY)
    ry = cy + 30
    for heading, note, rows in groups:
        text(cx, ry, heading, 16, INK)
        if note:
            text(cx + 360, ry + 2, note, 13, TEAL)
        path([(cx, ry + 26), (cx + cw, ry + 26)], arrow=False, color=INK)
        ry += 36
        for logic, work, rep, chips in rows:
            cells = [wrap(logic, 40), [ln for part in work.split("\n") for ln in wrap(part, 38)], wrap(rep, 46)]
            lines = max(len(c) for c in cells)
            h = 22 + lines * 19 + (34 if chips else 0)
            base("rectangle", cx, ry, cw, h, GRAY, 1, rough=0)
            for c in TCOLS[1:]:
                path([(cx + c, ry), (cx + c, ry + h)], arrow=False, color=GRAY)
            text(cx + 10, ry + 8, "\n".join(cells[0]), 14, INK)
            text(cx + TCOLS[1] + 10, ry + 8, "\n".join(cells[1]), 13, INK, MONO)
            text(cx + TCOLS[2] + 10, ry + 8, "\n".join(cells[2]), 14, RED if rep.startswith("?") else INK)
            for col, chip_text in chips:
                chip(cx + TCOLS[col] + 10, ry + h - 32, chip_text, 310)
            ry += h + 10
        ry += 8
    return ry


# ── under a screen, beside the screens ──────────────────────────────────────────────────────
def files(x, y, lines):
    """"on disk": the folders and files behind a screen, each with what on screen it feeds; "?" = proposed."""
    text(x, y, "on disk", 22)
    for i, (line, meaning) in enumerate(lines):
        red = "?" in line or meaning.startswith("?")
        text(x, y + 44 + i * 28, line, 15, RED if red else INK, MONO)
        if meaning:
            text(x + 560, y + 45 + i * 28, meaning, 15, RED if red else GRAY)


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


def card_window(name="By hypothesis test"):
    """The pop-out a method chip opens: one card, opened, read from its file."""
    c = next((c for c in ALL if c["name"] == name), ALL[0])
    return (f"{c['name']}  ·  a method card", [
        (f"{c['file'].relative_to(TK).as_posix()}", GRAY),
        ("\n".join(wrap(c.get("move", ""), 92)), INK),
        ("\n".join(wrap("reads  " + c.get("reads", "") + "   →   returns  " + c.get("returns", ""), 96)), INK),
        ("What the literature says         │  Applied to AI", INK),
        ("  Rationale · Context · Steps ·  │  The agent · Steps · Returns · Verify ·\n"
         "  Strengths · Limitations        │  AI risk · Evidence on AI · Skill", GRAY),
        (f"  skill: {c['skill']} {c['skill note']}", INK if c["skill exists"] else RED),
        ("\n".join(wrap("tested now  " + c.get("test now", "") + "   ·   in use  " + c.get("test in use", ""), 92)), INK),
        ("the same page as Guide › Method at this card", GRAY)])


# ── the open questions, loose ───────────────────────────────────────────────────────────────
def scratch_questions(x0, y0, notes):
    """The open questions as loose sticky notes (JL 261007: "make this free style, too structurable"):
    sketchy and a little crooked, readable Nunito, no frame, no form to fill. Returns their bounds, as a frame would."""
    import random
    rnd = random.Random(sum(map(ord, "".join(notes))))   # the same scatter on every build
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
    return {"x": x0, "y": y0, "width": 3 * 540, "height": y + row_h - y0}


# ── one level, one drawing ──────────────────────────────────────────────────────────────────
def aside(x, y, title, rows):
    """A note to the right of a frame's screens: a heading, then (name, what) rows, e.g. a Space's typical topics."""
    text(x, y, title, 22)
    for i, (name, what) in enumerate(rows):
        text(x, y + 44 + i * 58, name, 16, GREEN if name.startswith("✎") else RED if name.startswith("?") else INK, MONO)
        text(x, y + 68 + i * 58, what, 14, GRAY)


def level_drawing(out, source, level, title, subtitle, moves, screens, popouts, questions, asides=None, changes=None):
    """moves: [(today, proposed)]; screens: [(space, third, runs, recent, body(cx, cy, cw), files)];
    popouts: [(title, rows)]; questions: ["? …"]; asides: {space: (title, [(name, what)])}, drawn to the
    right of that Space's screens; changes: ["✎ <yymmdd>  <what changed>"], listed green on the title frame.
    Writes `out` through canvas.write."""
    L.els.clear()
    L.FRAME[0] = None
    fr = L.open_frame(f"{level} level · today → proposed")
    text(0, 0, title, 34)
    text(0, 50, subtitle, 20, GRAY)
    for k, (a, b) in enumerate(moves):
        text(0, 120 + k * 32, a, 17, GRAY)
        text(420, 120 + k * 32, "→  " + b, 17, RED if "?" in b else INK)
    for k, c in enumerate(changes or []):                  # the drawing's own history, newest last
        text(0, 120 + (len(moves) + 1) * 32 + k * 30, c, 16, GREEN)
    L.close_frame(fr)
    y = fr["y"] + fr["height"] + 300
    spaces = []                                          # one frame per Space, its sub-views side by side
    for sc in screens:
        if not spaces or spaces[-1][0] != sc[0]:
            spaces.append((sc[0], []))
        spaces[-1][1].append(sc)
    order = [sp for sp in SPACES if sp != "|"]           # the frames follow the Space row (JL 261007)
    spaces.sort(key=lambda sv: order.index(sv[0]) if sv[0] in order else len(order))
    for space, views in spaces:
        flat = lambda third: [b for r in third for b in r] if third and isinstance(third[0], list) else third or []
        names = [" · ".join(lab.lstrip("? ") for lab, on in flat(v[1]) if on) for v in views]
        fr = L.open_frame(f"{level} › {space}")
        text(0, y, f"{level} › {space}", 34)
        text(0, y + 50, (" · ".join(n for n in names if n) if len(views) > 1 else "one view") +
             "   ·   each a full screen, the folders and files behind it underneath; red dashed = proposed", 20, GRAY)
        for i, (sp, third, runs, recent, body, lines) in enumerate(views):
            x = i * (SW + 120)
            text(x, y + 120, names[i] or space, 24)
            body(*screen(x, y + 160, level, sp, third, runs, recent))
            files(x, y + 160 + SH + 50, lines)
        if space in (asides or {}):
            aside(len(views) * (SW + 120), y + 160, *asides[space])
        L.close_frame(fr, pad=60)
        y = fr["y"] + fr["height"] + 200
    fr = L.open_frame(f"{level} › pop-outs")
    text(0, y, "pop-outs, from a ↗ on any screen", 30)
    for i, (t, rows) in enumerate(popouts):                # side by side, one per opener
        window(i * 960, y + 60, 900, t, rows)
    L.close_frame(fr, pad=60)
    scratch_questions(0, fr["y"] + fr["height"] + 200, questions)
    canvas.write(out, list(L.els), source)
