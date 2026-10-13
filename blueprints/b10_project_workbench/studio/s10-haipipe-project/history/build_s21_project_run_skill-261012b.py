"""s21 · Project Run and skill: s21_project-run-skill.excalidraw, three frames, each a folder tree
(JL 261012: "每一个 frame 都太像一张 slide ... 我个人更 prefer 那种 tree 结构，就像 folder tree 那样"):

    ① Background   the words and where the topic sits, for a newcomer
    ② the Tree     every button and the skill it runs, by level and Space; the press step by step; the Run
                   folders; who writes which folder; what is still open, as red ? leaves in place
    ③ Reference    "Each skill is one folder in Tools/": the skills the buttons name, each with its version,
                   what it holds and the buttons that name it; haipipe-report/ opened file by file

Read from disk on every build: every Run button of the base frame and the skill it names
(servers/workbench/frame.py, through frame_buttons() below), the skill folders in Tools/ (version, ref ·
scripts · tests) and the files of haipipe-report/. Typed, since they are the design: the Run folders, the
Block tree and the open points. The 261007 builder and the 261012 four-story builder are in history/.

    python build_s21_project_run_skill.py [out.excalidraw]
"""
import sys
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




# ── drawing helpers ──────────────────────────────────────────────────────────────────────────────
def tree_frame(name, title, line, nodes, width, cols):
    """One frame: a title, one line under it, then the folder tree (canvas.tree). Red '? ' leaves are open
    questions, green '✎ ' leaves are changes."""
    fr = L.open_frame(name)
    L.text(0, 0, title, 34)
    L.text(0, 56, line, 22)
    els, _ = canvas.tree(0, 104, nodes, width, fr["id"], size=20, head=24, cols=cols)
    L.els.extend(els)
    L.close_frame(fr)
    return fr


# ── ① Background ─────────────────────────────────────────────────────────────────────────────────
def background_nodes(buttons):
    total = sum(len(rs) for rs in buttons.values())
    return [
        {"What this topic is about": [
            "Every Run button on the base workbench screen names one skill; this topic lists them all",
            "which skill each button runs, by level (Block, Job, Task, Page Task) and by Space",
            "JL 261007: \"what skill we should have for the studio and for the report ... we need to update "
            "the skills a lot\"",
            "b16's s21-paper-run-skill is the paper's counterpart of this topic"]},
        {"The screen in one minute": [
            "a level is the folder you stand in: Block, Job or Task",
            "a Space is a tab of that level: Description, Studio, Report, Work, Runs, Delivery",
            f"a Space holds Run buttons, {total} in frame.py across the four levels",
            "pressing one opens a Run, a folder in runs/, made by the skill the button names"]},
        {"Words it uses": [
            "skill: a folder in Tools/ whose SKILL.md says what it owns; Claude reads it first",
            "Run: one folder in runs/; a soft Run writes a report, a hard Run writes evidence",
            "pass: a new round on the same Run target, passes/pNN-<MMDD>/",
            "Page Task: a Task that writes one Page; it names seven draft skills",
            "theme: the kind of Block (work, cowork, paper ...); it keeps its own skills over the base"]},
        {"Where it sits": [
            "code: servers/workbench/frame.py gives each button its skills: field (s21-D02)",
            "the whole Run contract is s06-run-workbench-skill",
            "feeds the Questions q05_skill_per_level and q08_workbench_base"]},
        {"How to read this drawing": [
            "① this frame, the words",
            "② the Tree: each button and its skill, the Run folders, red ? leaves still open",
            "③ the reference: each skill as one folder in Tools/, read from disk"]},
    ]


# ── ② the Tree ───────────────────────────────────────────────────────────────────────────────────
SOFT = ["run-report-q03.md: the ticket",
        "run.yaml: the card, kind · type · target · status",
        {"passes/": ["p01-1009/: round 1", "p02-1010/: round 2, the same target"]}]
HARD = ["r03_fit_lstm.sh: the ticket, runnable",
        "config.yaml: its frozen inputs",
        "result/: its own output, evidence",
        "passes/p01-1010/"]
WRITES = [  # (folder, written by, shown in)
    ("studio/sNN-<topic>/", "haipipe-studio", "Studio, shared by the Block's levels"),
    ("reports/qNN_<topic>/", "haipipe-report", "Report"),
    ("delivery/<lane>/", "haipipe-block", "Delivery, top row; a Job's or Task's is filtered to it"),
    ("runs/run-<type>-<target>/", "haipipe-run", "Runs"),
    ("jNN_<job>/", "haipipe-job", "Work; keeps its own reports/ and soft runs/"),
    ("jNN_<job>/tNN_<task>/", "haipipe-task", "Work; keeps reports/ and hard runs/rNN_<slug>/"),
]


def level_nodes(buttons):
    """One branch per level; under it one per Space; under that each button: what it does, its Run, its skill."""
    cells = grid_cells(buttons)
    out = []
    for level, rows in buttons.items():
        by_col = {}
        for space, run, doing, skills in rows:
            by_col.setdefault(space, []).append(
                f"{ALIAS.get(doing.strip(), doing.strip())}: {run} · " + (skills.replace("haipipe-", "") or "? none"))
        kids = []
        for space, items in by_col.items():
            items = list(items)
            col = column(space)
            if level == "Block" and col == "Delivery":
                items.append("? s21-D03 kept delivery in haipipe-block because no Block delivered yet; every "
                             "output is now stored in Block/delivery/ (s02-D14), and haipipe-delivery exists: "
                             "re-decide (Open 1)")
            if level == "Block" and col == "Report":
                items.append("? what must each level's report answer? The Studio sets it (Open 2)")
            kids.append({space + (f"  (the example: {EXAMPLE[2]})" if (level, col) == EXAMPLE[:2] else ""): items}
                        if len(items) > 1 else f"{space}: {items[0]}")
        if level != "Page Task" and not cells.get((level, "Description")):
            kids.append("? Description has no button here; s21-D01 gives it to the level skill")
        out.append({f"{level}: {len(rows)} buttons, {sum(1 for r in rows if r[3])} name a skill": kids})
    return out


def tree_nodes(buttons):
    total = sum(len(rs) for rs in buttons.values())
    named = sum(1 for rs in buttons.values() for r in rs if r[3])
    return level_nodes(buttons) + [
        {"The press, step by step": [
            f"① you press a button: {total} in frame.py; the Runs panel lists a Space's buttons",
            f"② it names one skill: {named} of {total} do (s21-D02); one skill per level, one per shared Space",
            "③ the skill opens one Run, a folder in runs/",
            "④ the Run writes one folder, and the Space of that folder shows it",
            "✎ 261012 all 42 buttons name a skill (on 261007: 12 of 49)"]},
        {"③ a soft Run: writes into reports/qNN_<topic>/, not evidence": [
            {"runs/run-report-q03/  (haipipe-report)": SOFT},
            "? a Job holds soft Runs only: where does a batch launch, run-launch-<group>, go? (s06 open 2)"]},
        {"③ a hard Run: its own result/, new inputs make a new Run": [
            {"runs/r03_fit_lstm/  (haipipe-run, a work Task only)": HARD}]},
        {"④ who writes which folder, and where it shows": [
            f"{f}: {s} · {w}" for f, s, w in WRITES] + [
            "✎ 261010 studio and delivery live only in the Block (s02-D03, s02-D14)"]},
    ]


# ── ③ Reference: each skill is one folder in Tools/ ──────────────────────────────────────────────
def tools_nodes(buttons):
    dirs = skill_dirs()
    rel = lambda p: p.relative_to(TOOLKIT).as_posix()                     # noqa: E731
    named = {s for rows in buttons.values() for r in rows for s in r[3].split(" · ") if s}
    project = TOOLKIT / "skills/1_base/project"
    base = sorted((d for d in project.iterdir() if (d / "SKILL.md").is_file()),
                  key=lambda d: (BASE_ORDER.index(d.name) if d.name in BASE_ORDER else 99, d.name))
    homes = {}
    for s in sorted(named - {d.name for d in base} - {"haipipe-question", "haipipe-task"}):
        homes.setdefault(dirs[s].parent, []).append(s)
    themes = sorted(d.name for d in (TOOLKIT / "skills/2_theme").iterdir() if d.is_dir())
    servers = sorted(d.name for d in (TOOLKIT / "servers").iterdir() if d.name.startswith("workbench-"))

    def skill(d, where, red=False):
        kids = [f"holds: {skill_parts(d)}"]
        kids.append(("? " if red else "named by: ") + where)
        return {f"{d.name}/  {skill_version(d)}": kids}

    base_kids = []
    for d in base:
        where = used_by(d.name, buttons)
        red = False
        if not where:
            where, red = ("no button names it (s21 Open 1)", True) if d.name == "haipipe-delivery" else \
                ("no button; the Project sits above the frame", False)
        base_kids.append(skill(d, where, red))
    other = []
    for name in ("haipipe-question", "haipipe-task"):
        other.append(skill(dirs[name], used_by(name, buttons)))
    for home, names in sorted(homes.items(), key=lambda h: -len(h[1])):
        if len(names) > 1:
            other.append({f"{rel(home)}/  {len(names)} skills": [", ".join(n.replace("haipipe-", "") for n in names)]})
        else:
            other.append(skill(dirs[names[0]], used_by(names[0], buttons)))
    folder = dirs[OPENED]
    kinds = {"SKILL.md": "what it owns; Claude reads it first", "CHANGELOG.md": "what each version changed",
             "agents": "its name and prompt for Codex", "ref": "the full contract, read when needed",
             "scripts": "code a Run calls", "tests": "checks the scripts"}
    files = sorted((p for p in folder.rglob("*") if p.is_file() and not any(
        q.startswith(".") or q == "__pycache__" for q in p.relative_to(folder).parts)),
        key=lambda p: (p.name != "SKILL.md", len(p.relative_to(folder).parts), p.relative_to(folder).as_posix()))
    return [
        {"servers/": [f"workbench/frame.py: draws the buttons; each names its skill ({sum(len(r) for r in buttons.values())})",
                      "workbench/runs_panel.py: the Runs panel beside each Space",
                      f"workbench-<theme>/: a theme's frame over the base, {len(servers)}"]},
        {"skills/1_base/project/: the base, one skill per level, one per shared Space": base_kids},
        {"skills/1_base/ (the others the buttons name)": other},
        {f"skills/2_theme/<theme>/: a theme's own skills over the base, {len(themes)}": []} if False else
        f"skills/2_theme/<theme>/: a theme's own skills over the base, {len(themes)}",
        {f"{OPENED}/ opened: the example's skill (Job › Report › write the report)": [
            f"{p.relative_to(folder).as_posix()}: {kinds.get(p.relative_to(folder).parts[0], '')}" for p in files]},
        "~/.claude/skills/<name>: a link to the skill's folder, one per skill, made on each machine",
        "✎ 261012 haipipe-board is now haipipe-block (2.1.0, alias haipipe-board; s21-D07)",
    ]


# ── the drawing ──────────────────────────────────────────────────────────────────────────────────
def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s21_project-run-skill.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    buttons = frame_buttons()
    bg = tree_frame("Background: buttons and their skills", "Background: which skill each button runs",
                    "The words this topic uses, and where it sits. The topic itself is the Tree.",
                    background_nodes(buttons), 1500, 1)
    tree = tree_frame("The Tree: every button and its skill", "Every button and the skill it runs",
                      "By level and Space, read from frame.py; then a Run's folders; red ? leaves are still open.",
                      tree_nodes(buttons), 2500, 3)
    ref = tree_frame("Each skill is one folder in Tools/", "Each skill is one folder in Tools/",
                     "The button names the skill; the skill is a folder: its SKILL.md says what it owns, its "
                     "scripts do the work. Read from disk.", tools_nodes(buttons), 1900, 2)
    canvas.grid(L.els, [[bg["id"], tree["id"]], [ref["id"]]])
    canvas.write(out, list(L.els), "build_s21_project_run_skill.py")


if __name__ == "__main__":
    main()
