"""s21 · Project Run and skill: s21_project-run-skill.excalidraw, the base's Runs and the skills behind them,
level by level and Space by Space, and the plan to give every Run an owning skill (JL 261007: "what skill we
should have for the studio and for the report … haipipe-board, haipipe-job, haipipe-studio, haipipe-report,
haipipe-run … update the skills a lot"). Drawn in b16's s21-paper-run-skill style: lines-only tables, ink and
gray, red for what is open, green ✎ for what changed.

Read from disk on every build:

- the base frame's Run buttons per level and Space (servers/workbench/frame.py: vanilla() through
  spaces_for, the Page Task's page_task_spaces), and whether each names a skill
- each skill's version and size from its SKILL.md, found by name; the deleted ones said so
- the skill folders of 1_base/project · task · question · page/workbench-studio · display/excalidraw-report,
  and the studio scripts in this Block's _build/

Typed, since they are the proposal: the owning skill of each Run, its run-<type>-<target> name, the skills
table's "owns" and "takes from", the skill × Space grid, the folders after, the plan, and JL's four calls.

    python build_s21_project_run_skill.py [out.excalidraw]
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
B03 = HERE.parent                                         # the studio folder
TOOLS = HERE.parents[3]                                   # s21 -> studio -> b03 -> designs -> Tools
ROOT = HERE.parents[4]                                    # the SPACE root
SERVERS = TOOLS / "plugins" / "haipipe-toolkit" / "servers"
SKILLS = TOOLS / "plugins" / "haipipe-toolkit" / "skills"
sys.path.insert(0, str(B03 / "s01-overall-tree-structure"))
sys.path.insert(0, str(B03 / "_build"))
sys.path.insert(0, str(SERVERS / "_host"))
import build_ladder_v4 as L  # noqa: E402  (the shared drawing helpers)
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402

LEVELS = ("Block", "Job", "Task")
SPACES = ("Description", "Idea Studio", "Audience Report", "Work Details", "Runs", "Delivery")
LEVEL_SKILL = {"Block": "haipipe-board", "Job": "haipipe-job", "Task": "haipipe-task"}

# the proposal: a Run button -> (owning skill, its Run's name); "{level}" is the level's skill
# the proposal: the Run a button makes -> its owning skill; "{level}" is the level's skill. Keyed by the
# Run since the frame names each button by its Run (261007); a Page Task's own Runs are the Page family's
OWNER_BY_RUN = [
    ("run-face-", "{level}"), ("run-draw-", "haipipe-studio"), ("run-ask-", "haipipe-question"),
    ("run-report-", "haipipe-report"), ("run-figures-", "haipipe-report"), ("run-check-<q", "haipipe-report"),
    ("run-check-q", "haipipe-report"), ("run-add-<j", "haipipe-board"), ("run-add-j", "haipipe-board"),
    ("run-add-<t", "haipipe-job"), ("run-add-t", "haipipe-job"), ("run-build-", "haipipe-task"),
    ("run-<type>-<target>", "haipipe-run"), ("run-delivery-", "{level}"),
]

# the skills: name -> (status today, what it owns on the ladder, what it takes from today's skills)
SKILLS_TABLE = [
    ("haipipe-board", "Block: its face board.md, the question register, its six Spaces, a new-Block scaffold, how a theme claims a Block",
     "board.md writes now in each theme; haipipe-task's Block part; the deleted haipipe-board (261005)"),
    ("haipipe-job", "Job: its face, its Tasks in order, a new-Job scaffold, each theme's own Job names (level_patterns)",
     "haipipe-task's job iteration"),
    ("haipipe-task", "Task: unchanged (JL 261007: \"you should not touch the haipipe-task\"); the level skills sit beside it",
     "nothing; it keeps its Task-family door and its task-kind skills (1_data … 10_page)"),
    ("haipipe-studio", "Idea Studio at any level: studio/sNN-<topic>/ (face · drawings · build_*.py that keep marks), "
     "numbering s0x · s1x · s2x · s3x · s5x · s6x, sessions as passes of run-draw-<sNN>; the look: black, "
     "red = open, green = change, enforced by canvas.write",
     "excalidraw-report's scratch mode; b03 _build/ canvas.py · render_png.py; workbench-studio's draw lane"),
    ("haipipe-report", "the Question │ Work │ Report workflow of Audience Report at any level: what each cell reads, "
     "how work links to a question (answers: on a Job or Task face, a need id like QK10.E1), the walk open → partial → "
     "answered (no checked state: s21-D04), the report Page (Opening · Answer · Evidence · Limits · Next), its ## Figures and drawing; "
     "a comments batch is a report kind",
     "haipipe-question's report part; frame.question_rows' column rules; the Q │ W │ R row each theme restates "
     "(cowork · discovery · paper · work); excalidraw-report's report mode and ref/build_report_drawing.py"),
    ("haipipe-question", "the Question cell: asking, a Question's size, its register row, its folder; "
     "haipipe-report runs the rest of the row", "stays, smaller (JL 261007)"),
    ("haipipe-run", "Runs at any level: hard rNN_ and soft run-<type>-<target> (no <MMDD>), run.yaml as the Runs Space "
     "reads it, passes, one Run type table per Space naming its skill", "extends 0.31"),
    ("excalidraw-slide", "a slide draft s61-s69: one slides.py read by its drawing and its deck; frames left to "
     "right (logic flow · the slides · on disk, open); the accent inside a slide; notes under their slide",
     "haipipe-studio 0.3's slide drafts (moved 261007)"),
    ("haipipe-project", "the Project root and its Theme folders; its audit walks every level",
     "unchanged; audits through the level skills"),
]

# the skill folders after (typed)
AFTER = [
    "skills/1_base/project/",
    "├── haipipe-project/          the root, Theme folders, the audit",
    "├── haipipe-board/            NEW  ref/board-contract.md · scripts/new_board.py",
    "├── haipipe-job/              NEW  ref/job-contract.md · scripts/new_job.py",
    "├── haipipe-studio/           NEW  ref/topic-contract.md · scripts/canvas.py · render_png.py · new_topic.py",
    "├── haipipe-report/           NEW  ref/report-contract.md · scripts/build_report_drawing.py · check_report.py",
    "└── haipipe-run/              + ref/run-types-by-space.md · scripts/soft_run.py",
    "skills/1_base/task/           unchanged: haipipe-task, its task kinds, agents, page-types",
    "skills/1_base/question/haipipe-question/   asking only",
    "skills/1_base/display/excalidraw-report/   drawing kit only (plot kit, report frames)",
    "skills/1_base/display/excalidraw-slide/    NEW  ref/slide-draft.md · scripts/slide_kit.py",
]

PLAN = [
    ("1", "haipipe-board · haipipe-job", "the Block and Job face, register and scaffold; the frame's Description and "
     "Work Details buttons name them", "Update the description · Add a Job · Add a Task", "a new Block and Job scaffold and pass the project audit"),
    ("2", "haipipe-studio", "the topic folder contract; canvas.py · render_png.py move from b03 _build/ into it; "
     "every Block's builders import from the skill", "Add a topic · Redraw a topic · Save this session",
     "b03, b11-b17 rebuild from the skill's scripts"),
    ("3", "haipipe-report", "the report Page and its figure list; build_report_drawing.py moves in from excalidraw-report/ref/; "
     "comments batches as a report kind (paper)", "Write the report · Rebuild report drawing · Check a report",
     "every reports/qNN_ builds and checks through it"),
    ("4", "haipipe-run", "names without <MMDD>; run.yaml fields for the Runs Space; a Run type table per Space; "
     "the frame's buttons carry their skill", "Run (every level)", "no button on the frame without a skill"),
    ("5", "all (with b04)", "old words out; folder moves and renames planned with design_b04_skill_folder", "",
     "installers find every skill; no caller names a retired one"),
]

CALLS = [
    "✎ JL 261007 \"go\": the four calls taken as proposed below; red until JL settles each",
    "✎ JL 261007: haipipe-task is not touched; the Task level's buttons name it as they are",
    "✎ 261007 decided: Delivery stays in each level skill (Block · Job), the Page Task's in haipipe-page-delivery; "
    "no haipipe-delivery until a theme's Block delivery needs one",
    "✎ 261007 decided: \"checked\" is not a fourth state; the report Page's CHECK verdict shows beside answered",
    "✎ JL 261007: haipipe-report defines the Question │ Work │ Report workflow; haipipe-question keeps the asking",
    "? folder moves and renames: handed to design_b04_skill_folder (b04's call), 261007",
]


def table(x, y, cols, rows, size=15, row_h=34, mono=("skill", "Run", "button", "folder")):
    """A lines-only table: a header, then one row each; a cell ending in "?" is red. Returns its bottom."""
    w = sum(cw for _, cw in cols)
    cx = x
    for name, cw in cols:
        L.text(cx + 8, y + 8, name, size - 1, L.GRAY)
        cx += cw
    L.path([(x, y + row_h), (x + w, y + row_h)], arrow=False, color=L.INK)
    for i, row in enumerate(rows):
        lines = max(str(c).count("\n") + 1 for c in row)
        ry = y + row_h + sum(row_h * (max(str(c).count("\n") + 1 for c in r)) for r in rows[:i])
        cx = x
        for (name, cw), cell in zip(cols, row):
            cell = str(cell)
            font = L.MONO if name in mono else L.SANS
            L.text(cx + 8, ry + 8, cell, size, L.RED if cell.rstrip().endswith("?") else L.INK, font)
            cx += cw
        L.path([(x, ry + row_h * lines), (x + w, ry + row_h * lines)], arrow=False, color=L.GRAY)
    return y + row_h + sum(row_h * max(str(c).count("\n") + 1 for c in r) for r in rows)


def notes(x, y, lines):
    for k, n in enumerate(lines):
        L.text(x, y + k * 26, n, 16, L.RED if n.startswith("?") else L.GREEN)
    return y + len(lines) * 26


def bottom():
    return max(e["y"] + e.get("height", 0) for e in L.els)


def wrap(text, n):
    import textwrap
    return "\n".join(textwrap.wrap(text, n))


# ── facts, read from disk ───────────────────────────────────────────────────────────────────────
QWR = [  # (column, what it reads, who owns it) -- the row frame.question_rows draws
    ("Question", "the face's ## Questions register row: id · title · group · status, and the studio topics whose "
                 "Feeds: name it", "haipipe-question (ask) · haipipe-report (status)"),
    ("Work", "every Job and Task whose face says answers: <id> (or a need, <id>.E<n>), then the register's work:; "
             "each opens its Runs", "the theme's work skills; haipipe-report the link rule"),
    ("Report", "reports/qNN_<topic>/qNN_<topic>.md: its title, its Opening's first paragraph, its drawing "
               "(qNN_<topic>.png, built from ## Figures), answer-status", "haipipe-report"),
]
WALK = [("open", "asked; no answer yet", "Ask a Question (haipipe-question)"),
        ("partial", "some Work answers part of it", "Write the report (haipipe-report)"),
        ("answered", "the report states the answer from exact Results", "Write the report"),
]


def answer_states():
    """How many reports stand at each answer-status, across the SPACE (read from disk)."""
    from collections import Counter
    c = Counter()
    for md in list(ROOT.glob("examples-*/Project-*/*/*/reports/q*/q*.md")) + list(TOOLS.glob("designs/*/reports/q*/q*.md")):
        m = re.search(r"^answer-status:\s*([a-z-]+)", md.read_text(encoding="utf-8", errors="ignore"), re.M)
        if m:
            c[m.group(1)] += 1
    return c


def owner_of(run, level):
    """The proposed owner of a button, by the Run it makes (the frame names each button by its Run since
    261007, haipipe-run rule 6); a Page Task's own Runs are the Page family's."""
    for prefix, skill in OWNER_BY_RUN:
        if run.startswith(prefix) and not (level == "Page Task" and skill == "{level}" and prefix != "run-face-"):
            return skill.replace("{level}", LEVEL_SKILL.get(level, "haipipe-task"))
    return "the Page family"


def frame_buttons():
    """{level: [(Space, the Run it makes, what it does, the skills it names or "")]} from the base frame's
    defaults, and the Page Task's."""
    from host_paths import bootstrap
    bootstrap()
    from live import frame
    out = {}
    for level in LEVELS:
        views = frame.spaces_for(frame.VANILLA, level, ROOT / f".no-{level.lower()}", ROOT)
        out[level] = [(space, k["label"], k.get("doing", ""), " · ".join(k.get("skills") or [])) for space in SPACES
                      for k in views[space].run_types]
    page, seen = [], {}
    for space, subs in frame.PAGE_TASK_SUBS.items():
        for sub in subs or ("",):
            for k in frame.page_task_spaces(ROOT / ".no-page", ROOT, sub)[space].run_types:
                if (space, k["label"]) in seen:          # one button on every sub-tab: one row, the Space alone
                    page[seen[(space, k["label"])]] = (space, k["label"], k.get("doing", ""),
                                                       " · ".join(k.get("skills") or []))
                    continue
                seen[(space, k["label"])] = len(page)
                page.append((space + (f" › {sub}" if sub else ""), k["label"], k.get("doing", ""),
                             " · ".join(k.get("skills") or [])))
    out["Page Task"] = page
    return out


def plan_state(buttons):
    """Each plan phase's state, read from disk: the skill folders, the old copies gone, every builder
    importing canvas from haipipe-studio, the frame's buttons."""
    has = lambda *names: all(skill_dir(n) for n in names)
    gone = lambda f: not f.exists()
    def builders_switched():
        for f in (TOOLS / "blueprints").glob("*/studio/**/*.py"):
            text = "" if "history" in f.parts else f.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"(?m)^\s*import canvas\b", text) and "haipipe-studio/scripts" not in text:
                return False
        return True
    named = all(n for rows in buttons.values() for *_, n in rows)
    return {
        "1": "✎ built" if has("haipipe-board", "haipipe-job") else "? not yet",
        "2": "✎ built" if has("haipipe-studio") else "? not yet",
        "3": "✎ built" if has("haipipe-report") else "? not yet",
        "4": "✎ built; every button names its skill" if named and (skill_dir("haipipe-run") / "ref" /
                                                                  "run-types-by-space.md").is_file() else "? not yet",
        "5": ("✎ old copies retired, builders switched, old words out; ? folder moves: b04's call"
              if builders_switched() and gone(B03 / "_build" / "canvas.py") and gone(
                  SKILLS / "1_base/display/excalidraw-report/ref/build_report_drawing.py") else "? not yet"),
    }


def skill_dir(name):
    found = sorted(SKILLS.glob(f"**/{name}/SKILL.md"))
    return found[0].parent if found else None


def version(name):
    d = skill_dir(name)
    if not d:
        return "deleted 261005" if name == "haipipe-board" else "new"
    m = re.search(r"^\s*version:\s*\"?([\w.\-]+)", (d / "SKILL.md").read_text(encoding="utf-8"), re.M)
    return (m.group(1) if m else "?") + f" · {sum(1 for _ in open(d / 'SKILL.md'))} lines"


TASK_KINDS = {  # a folder of skills/1_base/task -> what it is (typed); its skill count is read from disk
    "1_data": "Stage 1-4 data: Source · Record · Case · AIData", "2_nn": "Stage 5 models: algo · tuner · instance · modelset",
    "3_end": "Stage 6 endpoints: develop · package · deploy", "4_individual": "individual inference and its report",
    "5_fit": "fit Tasks and GPU training", "6_eval": "evaluation Tasks", "7_display": "display Tasks (figures, tables)",
    "8_stata": "Stata Tasks", "9_agent": "agent and LLM-engine Tasks", "10_page": "Page Tasks (writing as a Task)",
    "agents": "the Task creator · orchestrator · reviewer agents", "page-types": "Insight Page type",
    "haipipe-task": "the Task-family door: Block → Job → Task → Run, P-B-E-R",
    "haipipe-workflow": "a Workflow as a list of Runs: specs, routes, gates",
    "haipipe-page-task": "a Task's reader Page from its Results",
}


def tree_today():
    lines = []
    for rel in ("1_base/project", "1_base/task", "1_base/question", "1_base/page/workbench-studio",
                "1_base/display"):
        d = SKILLS / rel
        if not d.is_dir():
            continue
        kids = sorted((p for p in d.iterdir() if p.is_dir() and not p.name.startswith(("_", "."))),
                      key=lambda p: (int(p.name.split("_")[0]) if p.name.split("_")[0].isdigit() else 99, p.name))
        lines.append(f"skills/{rel}/")
        if rel == "1_base/task":                          # a family of task kinds: one line each, what it is
            for k in kids:
                n = sum(1 for _ in k.rglob("SKILL.md"))
                lines.append(f"    {k.name + '/':<20}{n:>3} skill{'s' if n != 1 else ' '}  {TASK_KINDS.get(k.name, '')}")
            continue
        names = [k.name for k in kids if rel != "1_base/display" or k.name.startswith("excalidraw")]
        for i in range(0, len(names), 4):                 # four a line, so the column stays narrow
            lines.append("    " + " · ".join(names[i:i + 4]))
    tools = sorted(p.name for p in (B03 / "studio" / "_build").glob("*.py")) if (B03 / "studio" / "_build").is_dir() else \
        sorted(p.name for p in (B03 / "_build").glob("*.py"))
    lines.append("blueprints/b03_project_workbench/studio/_build/")
    for i in range(0, len(tools), 4):
        lines.append("    " + " · ".join(tools[i:i + 4]))
    return lines


# ── the drawing ──────────────────────────────────────────────────────────────────────────────────
def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s21_project-run-skill.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    buttons = frame_buttons()

    # 1 · Runs by level and Space
    fr = L.open_frame("1 · Runs by level and Space")
    L.text(0, 0, "Every Run button of the base frame, by level and Space, and who owns it", 30)
    L.text(0, 46, "read from servers/workbench/frame.py at build time (the vanilla Spaces through spaces_for, and the Page "
                  "Task's page_task_spaces) · a button is named by the Run it makes, what it does under it · "
                  "names (read): the skills its run type carries · proposed: its owner · red ? = open", 16, L.GRAY)
    cols = [("Space", 300), ("button = its Run (read)", 380), ("what it does (read)", 360), ("names (read)", 260),
            ("proposed skill", 260)]
    y, unnamed, total = 100, 0, 0
    for level, rows in buttons.items():
        L.text(0, y + 4, level, 20)
        body = []
        for space, run, doing, named in rows:
            skill = owner_of(run, level)
            body.append([space, run, wrap(doing, 44), named or "no ?", skill])
            unnamed += 0 if named else 1
            total += 1
        y = table(140, y, cols, body) + 40
    L.text(0, y, f"{total - unnamed} of {total} buttons name a skill today" + (
        "; every button the frame draws names its owner." if not unnamed else
        "; the frame's own buttons copy a plain prompt that no skill answers."), 18)
    notes(0, y + 40, [("✎ 261007 built (s21-D02): every frame run type carries skills:, as the Page's run cards do; "
                       "haipipe-run ref/run-types-by-space.md lists them" if not unnamed else
                       "? a frame button should carry its skill (run type field skills:), as the Page's run cards do"),
                      "✎ 261007 the Page Task's buttons come from run-cards.md by label; they already name theirs"])
    L.close_frame(fr, pad=40)

    # 2 · the skills
    y = bottom() + 200
    fr = L.open_frame("2 · The skills")
    L.text(0, y, "The skills: one per level, one per shared Space, each theme keeps its own", 30)
    L.text(0, y + 46, "version read from each SKILL.md (new = no folder yet); owns and takes from are the proposal", 16, L.GRAY)
    rows = [[n, version(n), wrap(o, 70), wrap(t, 58)] for n, o, t in SKILLS_TABLE]
    yb = table(0, y + 100, [("skill", 220), ("today", 200), ("owns on the ladder", 600), ("takes from", 520)], rows, row_h=30)
    notes(0, yb + 30, ["✎ 261007 JL: \"haipipe-board, haipipe-job, haipipe-studio, haipipe-report, haipipe-run\"",
                       "✎ 261007 built: " + " · ".join(f"{n} {version(n).split(' ·')[0]}" for n in
                                                     ("haipipe-board", "haipipe-job", "haipipe-studio", "haipipe-report",
                                                      "haipipe-run", "haipipe-question")),
                       "✎ 261008 excalidraw-slide " + version("excalidraw-slide").split(" ·")[0]
                       + ": slide drafts moved out of haipipe-studio; haipipe-studio enforces the black · red · green look",
                       "✎ 261008 decided (s21-D01): each theme keeps its own skills (haipipe-paper, haipipe-insight …) over these, as its <theme>_theme.py does over the frame"])
    L.close_frame(fr, pad=40)

    # 3 · skill × Space
    y = bottom() + 200
    fr = L.open_frame("3 · skill × Space")
    L.text(0, y, "Who owns each Space at each level", 30)
    L.text(0, y + 46, "level skills own their face and their children; the studio, report and run skills are the same at "
                      "every level; Guide is each theme's", 16, L.GRAY)
    grid = []
    for level in LEVELS:
        own = LEVEL_SKILL[level]
        grid.append([level, own, "haipipe-studio", "haipipe-report" + (" *" if level == "Task" else ""), own,
                     "haipipe-run", own if level != "Task" else "haipipe-page-delivery"])
    grid.append(["Guide", "workbench-<theme>", "", "", "", "", ""])
    yb = table(0, y + 100, [("level", 120)] + [(s, 250) for s in SPACES], grid, mono=SPACES)
    L.text(0, yb + 20, "* a Page Task's Table · Reading · Questions stay the Page family's views; haipipe-report owns a "
                       "Question's report Page", 15, L.GRAY)
    notes(0, yb + 50, ["✎ 261007 Delivery decided: haipipe-board · haipipe-job keep it at Block and Job (was ?)"])
    L.close_frame(fr, pad=40)

    # 3b · the Question │ Work │ Report workflow
    y = bottom() + 200
    fr = L.open_frame("3b · Question │ Work │ Report")
    L.text(0, y, "Question │ Work │ Report: the workflow haipipe-report defines for every Audience Report", 30)
    L.text(0, y + 46, "the row is what frame.question_rows draws at every level; the walk's counts are every report's "
                      "answer-status in the SPACE, read at build time", 16, L.GRAY)
    yb = table(0, y + 100, [("column", 140), ("what it reads", 1000), ("owner", 420)],
               [[c, wrap(r, 120), wrap(o, 50)] for c, r, o in QWR], row_h=30, mono=())
    counts = answer_states()
    xb, yw = 0, yb + 60
    L.text(0, yw - 34, "the walk", 20)
    for i, (state, what, run) in enumerate(WALK):
        L.base("rectangle", xb, yw, 300, 64, L.INK if state != "checked" else L.RED, 1.5)
        L.text(xb + 16, yw + 10, f"{state}   {counts.get(state, 0)}", 20, L.RED if state == "checked" else L.INK)
        L.text(xb + 16, yw + 38, what, 13, L.GRAY)
        L.text(xb, yw + 76, run, 14, L.GRAY)
        if i:
            L.path([(xb - 72, yw + 32), (xb - 8, yw + 32)])
        xb += 380
    notes(0, yw + 130, ["✎ 261007 JL: \"a haipipe-report as well to define the question - work - report workflow in the Audience report\"",
                        "✎ 261007 decided: no fourth state \"checked\"; the report Page's CHECK verdict (run-check-<qNN>) "
                        "shows beside answered"])
    L.close_frame(fr, pad=40)

    # 4 · skill folders
    y = bottom() + 200
    fr = L.open_frame("4 · skill folders: before → after")
    L.text(0, y, "Skill folders: today (read from disk) → proposed", 30)
    today = tree_today()
    for i, line in enumerate(today):
        L.text(0, y + 100 + i * 28, line, 15, L.INK, L.MONO)
    for i, line in enumerate(AFTER):
        L.text(1500, y + 100 + i * 28, line, 15, L.RED if line.rstrip().endswith("?") else L.INK, L.MONO)
    L.text(0, y + 70, "today, all kept (read from disk)", 18, L.GRAY)
    L.text(1500, y + 70, "proposed: adds only; nothing deleted", 18, L.GRAY)
    notes(1500, y + 100 + len(AFTER) * 28 + 30,
          ["✎ 261007 built as drawn",
           "✎ 261007 phase 5: canvas.py · render_png.py left b03 _build/ and build_report_drawing.py left "
           "excalidraw-report/ref/; every builder imports them from the skills",
           "✎ 261008 excalidraw-slide added beside excalidraw-report (slide drafts, from haipipe-studio)"])
    L.close_frame(fr, pad=40)

    # 5 · plan and JL's calls
    y = bottom() + 200
    fr = L.open_frame("5 · skill update plan")
    L.text(0, y, "The plan: every button gets an owning skill", 30)
    L.text(0, y + 46, "contracts first, so each later skill has a folder to write and a button to answer; moves and "
                      "renames last, with b04", 16, L.GRAY)
    state = plan_state(buttons)
    yp = table(0, y + 100, [("phase", 80), ("skill", 300), ("what it learns", 760), ("buttons it answers", 520),
                            ("done when", 460), ("now (read)", 300)],
               [[p, s, wrap(w, 90), wrap(b, 60), wrap(d, 54), wrap(state.get(p, ""), 34)] for p, s, w, b, d in PLAN],
               row_h=30)
    notes(0, yp + 30, CALLS)
    L.close_frame(fr, pad=40)
    canvas.write(out, list(L.els), "build_s21_project_run_skill.py")


if __name__ == "__main__":
    main()
