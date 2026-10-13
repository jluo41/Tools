"""s21 · Project Run and skill: s21_project-run-skill.excalidraw, drawn as one story read left to right
(JL 261010: "arrange the display with a sentence of telling stories by arranging the frames, and use --> to
connect the frames"):

    ① you press a button  -->  ② it names one skill  -->  ③ the skill opens one Run  -->  ④ the Run writes
                                                                                          one folder, and its
                                                                                          Space shows it
    still open (red)            every button, for reference

Read from disk on every build: every Run button of the base frame and the skill it names
(servers/workbench/frame.py, through frame_buttons() below), so the counts and the grid cannot go stale.
Typed, since they are the design: the example (Job › Report › "write the report"), the Run folders of ③,
the Block tree of ④ and the open points. The 261007 builder (six tables in one column) is kept in
history/ with its preview.

    python build_s21_project_run_skill.py [out.excalidraw]
"""
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDIO = HERE.parent                                      # b10's studio/
TOOLS = HERE.parents[3]                                   # s21 -> studio -> b10 -> blueprints -> Tools
ROOT = TOOLS                                              # frame_buttons() needs a folder under the root
SERVERS = TOOLS / "plugins" / "haipipe-toolkit" / "servers"
sys.path.insert(0, str(STUDIO / "s01-overall-tree-structure"))
sys.path.insert(0, str(SERVERS / "_host"))
import build_ladder_v4 as L  # noqa: E402  (the shared drawing helpers: base, text, path, frames)
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
import canvas  # noqa: E402

TODAY = "261010"                                          # the date of the older notes; new ones carry their own
LEVELS = ("Block", "Job", "Task")
COLUMNS = ("Studio", "Description", "Report", "Work", "Runs", "Delivery")
SPACE_OF = {"Idea Studio": "Studio", "Audience Report": "Report", "Work Details": "Work"}  # the frame's Space names, as the buttons read
EXAMPLE = ("Job", "Report", "run-report-<qNN>")                        # the one press the story follows
T, SUB, BODY, HEAD, CODE = 34, 22, 22, 24, 20                          # frame title · line under it · words · box titles · paths


# ── facts, read from disk ───────────────────────────────────────────────────────────────────────
def frame_buttons():
    """{level: [(Space, Run, what it does, skills it names)]}: the base frame's buttons at Block, Job and Task,
    then the Page Task's (one row per button; a button on every sub-tab once)."""
    from host_paths import bootstrap
    bootstrap()
    from live import frame
    import re
    import tempfile
    spaces = ("Description", "Idea Studio", "Audience Report", "Work Details", "Runs", "Delivery")
    out = {}
    # a real Block › Job › Task, each with its face: a folder without a face gets no Description
    # button, which drew "? no button" (fixed 261010); the probe's tags read back as <bNN> <jNN> <tNN>
    with tempfile.TemporaryDirectory(dir=ROOT, prefix=".s21-probe-") as tmp:
        block = Path(tmp) / "b99_probe"
        folders = {"Block": block, "Job": block / "j99_probe", "Task": block / "j99_probe/t99_probe"}
        for f in folders.values():
            f.mkdir(parents=True)
            (f / f"{f.name}.md").write_text(f"# {f.name}\n", encoding="utf-8")
        tags = {"b99": "<bNN>", "j99": "<jNN>", "t99": "<tNN>"}
        for level in LEVELS:
            views = frame.spaces_for(frame.VANILLA, level, folders[level], ROOT)
            out[level] = [(space, re.sub(r"[bjt]99", lambda m: tags[m.group(0)], k["label"]), k.get("doing", ""),
                           " · ".join(k.get("skills") or []))
                          for space in spaces for k in views[space].run_types]
    page, seen = [], {}
    for space, subs in frame.PAGE_TASK_SUBS.items():
        for sub in subs or ("",):
            for k in frame.page_task_spaces(ROOT / "<tNN>", ROOT, sub)[space].run_types:
                if (space, k["label"]) in seen:
                    continue
                seen[(space, k["label"])] = len(page)
                page.append((space + (f" › {sub}" if sub else ""), k["label"], k.get("doing", ""),
                             " · ".join(k.get("skills") or [])))
    out["Page Task"] = page
    return out


def screen_rows():
    """The two button rows the frame draws today, as (label, picked) lists: the top row (Studio | Block · Job ·
    Task | Delivery) and the Spaces row, read from frame.render on this Block's Report Space."""
    import re
    from live import frame
    page = frame.render(frame.VANILLA, ROOT, STUDIO.parent, "Audience Report")
    rows = []
    for cls in ("levels", "spaces"):
        m = re.search(r'<nav class="row ' + cls + r'"[^>]*>(.*?)</nav>', page, re.S)
        row = []                                  # a tab, a dropdown's first option, or a divider
        for tag in re.findall(r'<a [^>]*>[^<]*</a>|<button[^>]*>[^<]*</button>|<select[^>]*><option>[^<]*|<span class=bar>',
                              m.group(1) if m else ""):
            label = re.sub(r"<[^>]*>", "", tag).strip()
            row.append(("|", False) if "class=bar" in tag else (label, False))
        rows.append(row)
    return rows


def column(space):
    head = space.split(" › ")[0]
    return SPACE_OF.get(head, head)


def grid_cells(buttons):
    """{(level, column): [skills]} in first-seen order."""
    cells = {}
    for level, rows in buttons.items():
        for space, _run, _doing, skills in rows:
            for s in skills.split(" · "):
                if s and s not in cells.setdefault((level, column(space)), []):
                    cells[(level, column(space))].append(s)
    return cells


# ── drawing helpers (black lines, unfilled boxes; red = open, green = changed) ───────────────────
def rect(x, y, w, h, bold=False, dashed=False, color=L.INK):
    e = L.base("rectangle", x, y, w, h, color, 3 if bold else 1.5, dashed, rough=0)
    return e


def say(x, y, s, size=BODY, color=L.INK, font=L.SANS):
    L.text(x, y, s, size, color, font)
    return y + size * 1.3 * (s.count("\n") + 1)


def wrap(s, n):
    return "\n".join(textwrap.wrap(s, n))


def note(x, y, what, date=TODAY):
    """A green change note where the change is (haipipe-studio: ✎ <date> <what>)."""
    e = canvas.change_note(x, y, what, date, L.FRAME[0], size=18)
    L.els.append(e)
    return e


def heading(n, title, line):
    say(0, 0, f"{n} {title}".strip(), T)
    return say(0, 58, line, SUB)


# ── ① you press a button ─────────────────────────────────────────────────────────────────────────
def frame_press(buttons):
    fr = L.open_frame("You press a button")
    y = heading("①", "You press a button", "Block, Job and Task share one screen; each Space has its own Run buttons.") + 30
    level, col, run = EXAMPLE
    for row in screen_rows():                         # the frame's two rows today, the example's buttons bold
        x = 0
        for label, _ in row:
            if label == "|":
                L.path([(x + 10, y), (x + 10, y + 52)], arrow=False)
                x += 30
                continue
            w = int(len(label) * BODY * 0.55) + 44
            rect(x, y, w, 52, bold=label.startswith(level) or label == col)
            say(x + 22, y + 13, label, BODY)
            x += w + 12
        y += 80
    y += 10
    rows = [r for r in buttons[level] if column(r[0]) == col]
    panel_h = 70 + 64 * len(rows)
    rect(0, y, 1180, panel_h)
    say(24, y + 18, f"Runs panel · {level} › {col}   (read from frame.py)", HEAD)
    by = y + 70
    for _space, r, doing, _skills in rows:
        rect(24, by, 1132, 52, bold=r == run)
        say(44, by + 13, doing, BODY)
        say(520, by + 14, r, CODE, font=L.MONO)
        by += 64
    y += panel_h + 40
    counts = " · ".join(f"{lv} {len(rs)}" for lv, rs in buttons.items())
    total = sum(len(rs) for rs in buttons.values())
    named = sum(1 for rs in buttons.values() for r in rs if r[3])
    y = say(0, y, f"{total} buttons in frame.py: {counts}.", BODY)
    y = say(0, y, f"{named} of {total} name their skill." + ("" if named == total else "  ? the rest name none"),
            BODY, L.INK if named == total else L.RED)
    note(0, y + 10, f"all {total} buttons name a skill (on 261007: 12 of 49)")
    L.close_frame(fr, pad=60)
    return fr


# ── ② it names one skill ─────────────────────────────────────────────────────────────────────────
def frame_grid(buttons):
    fr = L.open_frame("It names one skill")
    y = heading("②", "The button names one skill",
                "One skill per level, one per shared Space; each theme keeps its own skills over them (s21-D01).") + 40
    cells = grid_cells(buttons)
    widths = {"": 170, "Studio": 250, "Description": 230, "Report": 280, "Work": 310, "Runs": 200, "Delivery": 330}
    xs, x = {}, 0
    for c, w in widths.items():
        xs[c] = x
        x += w
    width = x
    for c in COLUMNS:
        say(xs[c] + 12, y, c, HEAD)
    y += 46
    L.path([(0, y), (width, y)], arrow=False)
    level_rows = list(buttons)
    row_h = 92
    for level in level_rows:
        say(12, y + 14, level, HEAD)
        for c in COLUMNS:
            skills = cells.get((level, c), [])
            if c == "Studio" and not skills and level != "Block":
                say(xs[c] + 12, y + 14, "the Block's,\nshared", BODY)
            elif not skills:
                say(xs[c] + 12, y + 14, "? no button", BODY, L.RED)
            elif len(skills) > 2:
                say(xs[c] + 12, y + 14, f"{len(skills)} page skills\n(see reference)", BODY)
            else:
                say(xs[c] + 12, y + 14, "\n".join(skills), CODE, font=L.MONO)
            if (level, c) == EXAMPLE[:2]:
                rect(xs[c] + 2, y + 4, widths[c] - 8, row_h - 8, bold=True)
        y += row_h
        L.path([(0, y), (width, y)], arrow=False)
    y += 24
    note(xs["Studio"], y, "Studio: one Block room, shared by Job and Task (s02-D09)")
    note(xs["Report"] + 330, y, "Delivery files stored only in Block/delivery/ (s02-D14)")
    y += 50
    say(0, y, "Every button carries its skill in frame.py (s21-D02); Studio and Runs are the same skill at every level.", BODY)
    L.close_frame(fr, pad=60)
    return fr


# ── under ②: each skill is one folder in Tools/ (JL 261011) ─────────────────────────────────────
TOOLKIT = TOOLS / "plugins" / "haipipe-toolkit"
BASE_ORDER = ("haipipe-block", "haipipe-job", "haipipe-studio", "haipipe-report", "haipipe-run",
              "haipipe-delivery", "haipipe-project")                   # s21-D01's order; others after
OPENED = "haipipe-report"                                              # the example's skill, every file shown


def skill_dirs():
    """{name: folder}: every SKILL.md under the toolkit's skills/, by its folder's name."""
    out = {}
    for md in sorted((TOOLKIT / "skills").rglob("SKILL.md")):
        out.setdefault(md.parent.name, md.parent)
    return out


def skill_version(folder):
    import re
    m = re.search(r'^\s*version:\s*"?([\d.]+)', (folder / "SKILL.md").read_text(encoding="utf-8"), re.M)
    return m.group(1) if m else "?"


def skill_parts(folder):
    """'SKILL.md · ref 1 · scripts 2 · tests 1': what the folder holds, counted on disk."""
    def count(sub):
        d = folder / sub
        return len([p for p in d.iterdir() if p.is_file() and not p.name.startswith(".")]) if d.is_dir() else 0
    return " · ".join(["SKILL.md"] + [f"{sub} {count(sub)}" for sub in ("ref", "scripts", "tests") if count(sub)])


def used_by(name, buttons):
    """Where the frame's buttons name this skill: 'Studio, every level' or 'Block › Description · Work'."""
    at = {}
    for level, rows in buttons.items():
        for space, _run, _doing, skills in rows:
            if name in skills.split(" · ") and column(space) not in at.setdefault(level, []):
                at[level].append(column(space))
    at = {lv: cols for lv, cols in at.items() if cols}
    if not at:
        return ""
    cols = {tuple(c) for c in at.values()}
    if len(cols) == 1 and set(LEVELS) <= set(at):
        return f"{' · '.join(cols.pop())}, every level"
    return "  ".join(f"{lv} › {' · '.join(c)}" for lv, c in at.items() if lv in LEVELS) or \
        "  ".join(f"{lv} › {' · '.join(c)}" for lv, c in at.items())


def frame_tools(buttons):
    fr = L.open_frame("Each skill is one folder in Tools/")
    y = heading("", "Each skill is one folder in Tools/",
                "The button names the skill; the skill is a folder: its SKILL.md says what it owns, its scripts do "
                "the work.") + 40
    dirs = skill_dirs()
    rel = lambda p: p.relative_to(TOOLS).as_posix()                       # noqa: E731
    named = {s for rows in buttons.values() for r in rows for s in r[3].split(" · ") if s}
    project = TOOLKIT / "skills/1_base/project"
    base = sorted((d for d in project.iterdir() if (d / "SKILL.md").is_file()),
                  key=lambda d: (BASE_ORDER.index(d.name) if d.name in BASE_ORDER else 99, d.name))
    homes = {}                                   # the other skills the buttons name, by the folder that holds them
    for s in sorted(named - {d.name for d in base} - {"haipipe-question", "haipipe-task"}):
        homes.setdefault(dirs[s].parent, []).append(s)
    themes = sorted(d.name for d in (TOOLKIT / "skills/2_theme").iterdir() if d.is_dir())
    servers = sorted(d.name for d in (TOOLKIT / "servers").iterdir() if d.name.startswith("workbench-"))
    # (tree line, skill folder or None, what it is, red?)
    rows = [("Tools/", None, "", False),
            ("└── plugins/haipipe-toolkit/", None, "", False),
            ("    ├── servers/workbench/frame.py", None, f"draws the buttons; each names its skill "
             f"({sum(len(r) for r in buttons.values())})", False),
            ("    ├── servers/workbench/runs_panel.py", None, "the Runs panel beside each Space", False),
            ("    ├── servers/workbench-<theme>/", None, f"a theme's frame over the base: {len(servers)}", False),
            ("    ├── skills/1_base/project/", None, "the base: one skill per level, one per shared Space", False)]
    for k, d in enumerate(base):
        where = used_by(d.name, buttons)
        if not where:
            where, red = ("? no button names it (s21 Open 1)", True) if d.name == "haipipe-delivery" else \
                ("the Project, above the frame; no button", False)
        else:
            red = False
        rows.append((f"    │   {'└' if k == len(base) - 1 else '├'}── {d.name}/", d, where, red))
    for name in ("haipipe-question", "haipipe-task"):
        rows.append((f"    ├── {rel(dirs[name].parent)[len('plugins/haipipe-toolkit/'):]}/{name}/", dirs[name],
                     used_by(name, buttons), False))
    short = lambda p: p.relative_to(TOOLKIT).as_posix()                   # noqa: E731
    for home, names in sorted(homes.items(), key=lambda h: -len(h[1])):
        if len(names) > 1:                       # a folder of several (the Page's draft skills): one line
            at = {}
            for level, items in buttons.items():
                for space, _run, _doing, skills in items:
                    if set(names) & set(skills.split(" · ")) and column(space) not in at.setdefault(level, []):
                        at[level].append(column(space))
            rows.append((f"    ├── {short(home)}/", None, f"{len(names)} skills · " + "  ".join(
                f"{lv} › {' · '.join(c)}" for lv, c in at.items() if c), False))
        else:
            rows.append((f"    ├── {short(dirs[names[0]])}/", dirs[names[0]], used_by(names[0], buttons), False))
    rows.append(("    └── skills/2_theme/<theme>/", None, f"a theme's own skills over the base: {len(themes)}", False))
    cx = (0, 740, 860, 1390)                                    # tree · version · what it holds · its buttons
    for c, label in zip(cx, ("folder", "version", "what it holds", "the buttons that name it")):
        say(c, y, label, HEAD)
    y += 46
    L.path([(0, y - 6), (2040, y - 6)], arrow=False)
    for line, folder, what, red in rows:
        say(cx[0], y, line, CODE, font=L.MONO)
        if folder is not None:
            say(cx[1], y, skill_version(folder), CODE, font=L.MONO)
            say(cx[2], y, skill_parts(folder), CODE, font=L.MONO)
            if folder.name == OPENED:
                rect(-10, y - 6, 2050, 36, bold=True)
        say(cx[3] if folder is not None else cx[2], y, what, BODY, L.RED if red else L.INK)
        y += 36
    y = say(0, y + 8, "~/.claude/skills/<name>   a link to the folder above, one per skill, made on each machine",
            BODY) + 40
    # one skill opened: the example's, every file read from disk
    folder = dirs[OPENED]
    say(0, y, f"{OPENED}/ opened: the example's skill (Job › Report › write the report)", HEAD)
    y += 46
    kinds = {"SKILL.md": "what it owns; Claude reads it first", "CHANGELOG.md": "what each version changed",
             "agents": "its name and prompt for Codex", "ref": "the full contract, read when needed",
             "scripts": "code a Run calls", "tests": "checks the scripts"}
    files = sorted((p for p in folder.rglob("*") if p.is_file() and not any(
        q.startswith(".") or q == "__pycache__" for q in p.relative_to(folder).parts)),
        key=lambda p: (p.name != "SKILL.md", len(p.relative_to(folder).parts), p.relative_to(folder).as_posix()))
    for k, p in enumerate(files):
        part = p.relative_to(folder).as_posix()
        say(0, y, f"{'└' if k == len(files) - 1 else '├'}── {part}", CODE, font=L.MONO)
        say(560, y, kinds.get(part.split("/")[0], ""), BODY)
        y += 34
    note(0, y + 16, "skill folders in Tools/ added under ②, read from disk (JL)", "261011")
    L.close_frame(fr, pad=60)
    return fr


# ── ③ the skill opens one Run ────────────────────────────────────────────────────────────────────
SOFT = ["runs/run-report-q03/      ◀ haipipe-report",
        "├── run-report-q03.md     the ticket",
        "├── run.yaml              the card: kind · type · target · status",
        "└── passes/",
        "    ├── p01-1009/         round 1",
        "    └── p02-1010/         round 2, the same target"]
HARD = ["runs/r03_fit_lstm/        ◀ haipipe-run, a work Task only",
        "├── r03_fit_lstm.sh       the ticket, runnable",
        "├── config.yaml           its frozen inputs",
        "├── result/               its own output: evidence",
        "└── passes/p01-1010/"]


def frame_run():
    fr = L.open_frame("The skill opens one Run")
    y = heading("③", "The skill opens one Run",
                "A Run is one folder in runs/: a new round on the same target is a pass (s06).") + 40
    say(0, y, "soft: writes into reports/q03_<topic>/; not evidence   (example names)", HEAD)
    y += 46
    for k, line in enumerate(SOFT):
        say(0, y + k * 30, line, CODE, font=L.MONO)
    y += len(SOFT) * 30 + 50
    say(0, y, "hard: its own result/; new inputs make a new Run", HEAD)
    y += 46
    for k, line in enumerate(HARD):
        say(0, y + k * 30, line, CODE, font=L.MONO)
    y += len(HARD) * 30 + 40
    say(0, y, "→ the whole Run contract: s06-run-workbench-skill", BODY)
    L.close_frame(fr, pad=60)
    return fr


# ── ④ the Run writes one folder, and its Space shows it ──────────────────────────────────────────
TREE = [  # (folder, written by, shown in, change note)
    ("bNN_<topic>/", "", "", ""),
    ("├── studio/sNN-<topic>/", "haipipe-studio", "Studio, shared", "Studio only in the Block (s02-D03)"),
    ("├── reports/qNN_<topic>/", "haipipe-report", "Report", ""),
    ("├── delivery/<lane>/", "haipipe-block", "Delivery, top row", "delivery only in the Block (s02-D14)"),
    ("│   └── jNN_<job>/tNN_<task>/<lane>/", "haipipe-job · haipipe-task", "Delivery, filtered to it", ""),
    ("├── runs/run-<type>-<target>/", "haipipe-run", "Runs", ""),
    ("└── jNN_<job>/", "haipipe-job", "Work", ""),
    ("    ├── reports/qNN_<topic>/", "haipipe-report", "Report (Job)", ""),
    ("    ├── runs/   soft only", "haipipe-run", "Runs", ""),
    ("    └── tNN_<task>/", "haipipe-task", "Work", ""),
    ("        ├── reports/qNN_<topic>/", "haipipe-report", "Report (Task)", ""),
    ("        └── runs/rNN_<slug>/", "haipipe-run", "Runs: hard, evidence", ""),
]


def frame_write():
    fr = L.open_frame("The Run writes one folder")
    y = heading("④", "The Run writes into one folder, and its Space shows it",
                "Studio and delivery live only in the Block; every level keeps its own reports and Runs.") + 40
    cx = (0, 560, 940)
    for c, label in zip(cx, ("folder", "written by", "shown in")):
        say(c, y, label, HEAD)
    y += 48
    L.path([(0, y - 6), (1380, y - 6)], arrow=False)
    for folder, skill, space, changed in TREE:
        say(cx[0], y, folder, CODE, font=L.MONO)
        if skill:
            say(cx[1] - 40, y, "◀", CODE, font=L.MONO)
            say(cx[1], y, skill, CODE, font=L.MONO)
            say(cx[2], y, space, BODY)
        if changed:
            note(1420, y + 2, changed)
        y += 40
    L.close_frame(fr, pad=60)
    return fr


# ── still open, and every button ─────────────────────────────────────────────────────────────────
def frame_open(buttons):
    fr = L.open_frame("Still open")
    y = say(0, 0, "Still open", T) + 20
    cells = grid_cells(buttons)
    missing = [lv for lv in LEVELS if not cells.get((lv, "Description"))]
    items = []
    if missing:
        items.append(f"? Description at {', '.join(missing)} has no button in frame.py; s21-D01 gives it to the level skill.")
    items += [
        "? s21-D03 kept delivery in the level skills because no Block or Job delivered yet. Now every output is "
        "stored in Block/delivery/ (s02-D14) and Delivery has its own skill, haipipe-delivery: re-decide D03.",
        "? What must each level's report answer? The Studio sets it, each level reports (meeting 261010).",
        "? A Job holds soft Runs only: where does a batch launch, run-launch-<group>, go? (s06 open 2)",
    ]
    for k, item in enumerate(items, 1):
        y = say(0, y, wrap(f"{k}. {item[2:]}", 74), BODY, L.RED) + 18
    L.close_frame(fr, pad=60)
    return fr


ALIAS = {"build": "build the delivery", "check": "check the delivery"}   # the Page Task's short Delivery words


def button_rows(buttons):
    """One row per button across the levels: (column, what it does, its Runs, {level: skill}), in the
    order of the grid's columns, first seen first."""
    rows = {}
    for level, items in buttons.items():
        for space, run, doing, skills in items:
            col, does = column(space), ALIAS.get(doing.strip(), doing.strip())
            key = (col, does.lower())
            r = rows.setdefault(key, {"col": col, "does": does, "runs": [], "at": {}})
            if run not in r["runs"]:
                r["runs"].append(run)
            r["at"][level] = skills
    order = {c: i for i, c in enumerate(COLUMNS)}
    return sorted(rows.values(), key=lambda r: order.get(r["col"], 99))


def run_pattern(runs):
    """run-delivery-<bNN> · run-delivery-<jNN> … -> run-delivery-<bNN|jNN|…>: one name when they share a stem."""
    if len(runs) == 1:
        return runs[0]
    stems = {r.split("<", 1)[0] for r in runs}
    if len(stems) == 1 and all("<" in r for r in runs):
        return stems.pop() + "<" + "|".join(r.split("<", 1)[1].rstrip(">") for r in runs) + ">"
    return " · ".join(runs)


def frame_reference(buttons):
    fr = L.open_frame("Every button, for reference")
    y = say(0, 0, "Every button: which level has it, and the skill it names", T) + 6
    y = say(0, y, "read from frame.py on every build · one row per button, one column per level · "
                  "a cell names the skill (haipipe- left off) · \u00b7 = not at this level", SUB) + 30
    levels = list(buttons)
    cx = {"Space": 0, "button": 210, "Run": 640, **{lv: 1180 + 230 * i for i, lv in enumerate(levels)}}
    width = cx[levels[-1]] + 260
    for name, x in cx.items():
        say(x, y, name, HEAD)
    y += 44
    L.path([(0, y), (width, y)], arrow=False)
    y += 12
    last = None
    for r in button_rows(buttons):
        if r["col"] != last and last is not None:
            L.path([(0, y - 6), (width, y - 6)], arrow=False)
            y += 6
        does = wrap(r["does"], 32)
        lines = does.count("\n") + 1
        if r["col"] != last:
            say(cx["Space"], y, r["col"], BODY)
        say(cx["button"], y, does, BODY)
        say(cx["Run"], y, run_pattern(r["runs"]), CODE, font=L.MONO)
        for lv in levels:
            skill = r["at"].get(lv)
            text = "\u00b7" if skill is None else (skill.replace("haipipe-", "") or "? none")
            say(cx[lv], y, text, CODE, L.RED if skill == "" else L.INK, L.MONO)
            if (lv, r["col"], r["does"]) == (EXAMPLE[0], EXAMPLE[1], "write the report"):
                rect(cx[lv] - 10, y - 6, 220, 36, bold=True)
        last = r["col"]
        y += 30 * lines + 10
    L.path([(0, y), (width, y)], arrow=False)
    note(0, y + 16, "one row per button, a column per level (was 37 rows, one per level and button)")
    L.close_frame(fr, pad=60)
    return fr


# ── the story ────────────────────────────────────────────────────────────────────────────────────
def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s21_project-run-skill.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    buttons = frame_buttons()
    story = [frame_press(buttons), frame_grid(buttons), frame_run(), frame_write()]
    tall = max(f["height"] for f in story)
    for f in story:                                   # one strip: every chapter the same height
        f["height"] = tall
    below = [frame_open(buttons), frame_tools(buttons), frame_reference(buttons)]   # the skill folders under ②
    canvas.grid(L.els, [[f["id"] for f in story], [f["id"] for f in below]], gap=260)

    # the sentence that tells the story, above the strip, and the arrows that join its chapters
    top = story[0]["y"]
    L.text(0, top - 250, "s21 in one sentence: you press a button ①, it names one skill ②, the skill opens one Run ③, "
                         "and the Run writes into one folder that its Space shows ④.", 40)
    L.text(0, top - 180, "Read left to right along the arrows. Below the strip: what is still open, each skill's "
                         "folder in Tools/, and every button for reference.", BODY)
    for k, what in enumerate(("✎ 261010 redrawn as one story in four frames (JL); the 261007 tables are in history/",
                              "✎ 261010 Studio and delivery only in the Block; all buttons name a skill",
                              "✎ 261011 under ②, each skill's folder in Tools/, read from disk (JL)")):
        L.els.append(canvas.change_note(0, top - 130 + k * 26, what[9:], what[2:8], None, size=18))
    for a, b, word in zip(story, story[1:], ("names", "opens", "writes")):
        ay = a["y"] + 180
        x0, x1 = a["x"] + a["width"] + 20, b["x"] - 20
        L.path([(x0, ay), (x1, ay)])
        L.els[-1]["strokeWidth"] = 3
        L.text(x0 + 30, ay - 44, word, HEAD)
    grid_fr, tools, ref = story[1], below[1], below[2]
    y0, y1 = grid_fr["y"] + grid_fr["height"] + 20, tools["y"] - 20
    ax = max(grid_fr["x"], tools["x"]) + 200          # ② down to its skills' folders (JL 261011)
    L.path([(ax, y0), (ax, y1)])
    L.els[-1]["strokeWidth"] = 3
    L.text(ax + 20, y0 + 40, "each skill is one folder in Tools/", HEAD)
    bx = grid_fr["x"] + grid_fr["width"] - 200        # and, dashed, to every button by level
    mid = (y0 + y1) / 2 + 60
    L.path([(bx, y0), (bx, mid), (ref["x"] + 200, mid), (ref["x"] + 200, y1)], dashed=True)
    L.text(bx + 20, y0 + 40, "every button, by level", HEAD)
    canvas.write(out, list(L.els), "build_s21_project_run_skill.py")


if __name__ == "__main__":
    main()
