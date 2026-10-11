"""s02 · Workbench shared: s02-workbench-shared.excalidraw: what workbench holds today, how
every other workbench leans on it, and the proposal that it owns the Block / Job / Task frame.

Three discussion frames lead; the eight older frames stay as references:

    Shared workbench across levels  Block, Job and Task screens with their sources (Q08)
    Block topics construct Jobs    Block-owned topics lead to linked execution Jobs (Q07)
    Studio and Report separate Spaces connected by source links (Q09)

Older reference material:

    today · who owns which part   one column per workbench, one row per part; each cell read off the
                                  workbench's own Python at build time (an import of a shared part, or
                                  its own stylesheet), so the grid is what the code does now
    today → proposed trees        the servers/ tree as it is on disk, beside the tree once shared owns the frame
    today · the Spaces drawn      each workbench's Space row as the server renders it (level_views.SERVER)
    proposed · the frame          what workbench would own, what a family would fill
    the base and a theme          shared holds Block · Job · Task × the six Spaces with defaults; three themes filled in
    steps and open points         in red ? where JL decides

Placeholders only: no project content. This builder draws through canvas.write, so every mark a
person adds survives a rebuild.

Was b03's s08, then b02's s01; back in b03 as s07 when b02 merged into b03, s02 since the renumbering (JL 261007: "project and
workbench are the same things").

    python build_s02_workbench_shared.py [out.excalidraw]
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
B03 = HERE.parent                                     # b03 studio: the shared definitions and the canvas writer
sys.path.insert(0, str(B03 / "s01-overall-tree-structure"))
sys.path.insert(0, str(B03 / "_build"))
import build_ladder_v4 as L  # noqa: E402  (the drawing helpers)
sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402
import level_views as LV  # noqa: E402  (today's Space rows, read from the server code)
import screens as UI  # noqa: E402  (the workbench screens, drawn large: one module for every b03 drawing)

INK, GRAY, RED, TEAL, MONO = L.INK, L.GRAY, L.RED, L.TEAL, L.MONO
text, path, box, base = L.text, L.path, L.box, L.base
SERVERS = L.PLUGINS / "haipipe-toolkit/servers"
LABELING = L.PLUGINS / "haipipe-toolkit/servers/workbench-labeling"

# the workbenches, left to right: (column name, folder, its bench in level_views.SERVER)
BENCHES = [("work", SERVERS / "workbench-work", "task"), ("discovery", SERVERS / "workbench-discovery", "discovery"),
           ("cowork", SERVERS / "workbench-cowork", "cowork"), ("insight", SERVERS / "workbench-insight", "insight"),
           ("paper", SERVERS / "workbench-paper", "paper"), ("page", SERVERS / "workbench" / "task-page", "page"),
           ("design", SERVERS / "workbench-design", "design"), ("labeling", LABELING, "labeling")]
SHARED = SERVERS / "workbench"
# the parts, top to bottom: (label, where it lives, pattern that shows a workbench uses it)
PARTS = [("the frame: levels · six Spaces", "workbench · frame, frame_view (261007)", r"live\.frame\b|from live import frame"),
         ("Guide", "workbench · guide_families, workbench_guide", r"mount_guide|guide_families"),
         ("Studio: draw · chat · terminal", "workbench · xcal, chat, term", r"\bxcal\b|excalidraw_proxy|/_excalidraw|/_board/excalidraw|/_board/chat|/_board/term"),
         ("Runs panel", "workbench · runs_panel (moved in, 261007)", r"runs_panel"),
         ("BJTR tree (Block › Job › Task › Run)", "workbench · work_items", r"\bwork_item"),
         ("Related Papers cards", "workbench · related_papers", r"related_papers"),
         ("header · band · Space row · CSS", "each workbench, its own copy", r":root\s*\{|\.css\b")]


def own_files(folder):
    """The workbench's own source files (Python, CSS, JS), without its studio/ drawings and tests."""
    if not folder.exists():
        return []
    out = []
    for p in sorted(folder.rglob("*")):
        rel = p.relative_to(folder)
        if (p.suffix in (".py", ".css", ".js") and p.is_file()
                and not {"studio", "tests", "__pycache__", "checks"} & set(rel.parts)
                and not (folder.name == "workbench" and rel.parts[0] == "task-page")):
            out.append(p)               # the base's Page Task views (once workbench-page) are their own column
    return out


def nlines(p):
    return p.read_text(errors="ignore").count("\n")


def code(folder):
    return "\n".join(p.read_text(errors="ignore") for p in own_files(folder) if p.suffix == ".py")


def lines_of(folder):
    return sum(nlines(p) for p in own_files(folder) if p.suffix == ".py")


# where each part lives in the base: its own files
BASE_FILES = {"the frame": ["frame.py", "frame_view.py"], "Guide": ["guide_families.py", "workbench_guide.py"],
              "Studio": ["xcal.py", "chat.py", "term.py", "excalidraw_proxy.py"], "Runs panel": ["runs_panel.py"],
              "BJTR tree": ["work_items.py"], "Related Papers": ["related_papers.py"], "header": []}


def users(part, folder):
    """The files of one workbench that use this part, each with its line count."""
    label, _, pat = part
    hits = []
    for p in own_files(folder):
        if label.startswith("header"):
            if p.suffix == ".css" or (p.suffix == ".py" and re.search(r":root\s*\{", p.read_text(errors="ignore"))):
                hits.append(p)
        elif p.suffix == ".py" and re.search(pat, p.read_text(errors="ignore")):
            hits.append(p)
    return [(p.relative_to(folder).as_posix(), nlines(p)) for p in hits]


def file_cell(x, y, files, color=INK, most=4):
    """A cell: one file a line, name and line count; an empty cell says not used. Returns its height."""
    if not files:
        text(x, y, "not used", 13, GRAY)
        return 22
    for k, (name, n) in enumerate(files[:most]):
        text(x, y + k * 19, f"{name} · {n:,}", 13, color, MONO)
    if len(files) > most:
        text(x, y + most * 19, f"+ {len(files) - most} more", 13, GRAY)
        return (most + 1) * 19
    return len(files) * 19


def frame_today(y):
    fr = L.open_frame("today · who owns which part")
    text(0, y, "Today: which files use each shared part", 30)
    text(0, y + 46, "Read off the code at every build. Each cell lists the files in that workbench that use the part, "
                    "with their line counts; \"not used\" = none of its files do. The last column is where the part "
                    "lives in the base.", 16, GRAY)
    PX, WX, CW = 0, 430, 300
    top = y + 110
    text(PX, top, "part", 15, INK)
    cols = BENCHES + [("shared", SHARED, None)]
    for i, (name, folder, _) in enumerate(cols):
        cx = WX + i * CW
        text(cx, top, folder.relative_to(SERVERS).as_posix() + "/" + ("  (the base)" if name == "shared" else ""),
             15, TEAL if name == "shared" else INK, MONO)
        text(cx, top + 22, f"{lines_of(folder):,} lines of Python in all", 13, GRAY)
    path([(PX, top + 50), (WX + len(cols) * CW, top + 50)], arrow=False, color=GRAY)
    ry = top + 66
    for part in PARTS:
        text(PX, ry, part[0], 16, INK)
        text(PX, ry + 22, part[1], 13, GRAY)
        h = 44
        for i, (name, folder, _) in enumerate(BENCHES):
            h = max(h, file_cell(WX + i * CW, ry, users(part, folder)))
        key = next(k for k in BASE_FILES if part[0].startswith(k))
        base_files = ([(f, nlines(SHARED / f)) for f in BASE_FILES[key] if (SHARED / f).exists()]
                      if BASE_FILES[key] else users(part, SHARED))
        h = max(h, file_cell(WX + len(BENCHES) * CW, ry, base_files, TEAL))
        ry += h + 24
        path([(PX, ry - 12), (WX + len(cols) * CW, ry - 12)], arrow=False, color="#dee2e6")
    def who(label, used=True):                     # the workbenches that use (or do not use) a part, by the scan above
        part = next(pt for pt in PARTS if pt[0].startswith(label))
        return ", ".join(n for n, f, _ in BENCHES if bool(users(part, f)) == used) or "none"
    for k, note in enumerate([
            f"So, from the scan: on the frame already: {who('the frame')}; not yet: {who('the frame', False)}.",
            f"Still carrying their own look (last row): {who('header')}. The BJTR tree is used by: {who('BJTR')}.",
            "A theme moves onto the frame when its session (b11-b17) builds its <theme>_theme.py; this table follows on the next build."]):
        text(PX, ry + 10 + k * 24, note, 16, INK)
    L.close_frame(fr, pad=60)
    return fr["y"] + fr["height"]


def frame_spaces(y):
    fr = L.open_frame("today · the Spaces drawn")
    text(0, y, "Today: each workbench names its own Spaces, at one level", 30)
    text(0, y + 46, "As the server code renders them (level_views.SERVER). No workbench has a Job level; "
                    "Board = a Block, page = one Page (a Task).", 16, GRAY)
    ry = y + 110
    for (bench, level), layout in LV.SERVER.items():
        text(0, ry + 6, f"workbench-{bench}", 15, INK)
        text(230, ry + 6, "Block" if level == "board" else "Task (one Page)", 13, GRAY)
        tx = 400
        for space, views in layout:
            w = len(space) * 15 * 0.58 + 22
            base("rectangle", tx, ry, w, 30, GRAY if space == "Guide" else INK, 1)
            text(tx + 11, ry + 6, space, 15, GRAY if space == "Guide" else INK)
            tx += w + 8
        text(tx + 16, ry + 8, " · ".join(v for _, vs in layout[1:2] for v in vs)[:70], 12, GRAY)
        ry += 44
    ry += 20
    text(0, ry, "261010: shared Studio opens Block topics from Block, Job and Task; work Spaces below:", 16, TEAL)
    tx = 520
    for space in ["Description", "|", "Report", "|", "Work Details", "|", "Runs", "Delivery"]:
        if space == "|":
            path([(tx + 2, ry + 30), (tx + 2, ry + 72)], arrow=False, color=INK)
            tx += 14
            continue
        w = len(space) * 15 * 0.58 + 22
        base("rectangle", tx, ry + 36, w, 30, TEAL, 1.5)
        text(tx + 11, ry + 42, space, 15, TEAL)
        tx += w + 8
    text(0, ry + 42, "Guide · Studio | Block · Job ▾ · Task ▾", 15, TEAL)
    L.els.append(canvas.change_note(0, ry + 84, "Live: Studio hides the five work Space buttons",
                                    date="261010", frame=L.FRAME[0], size=16))
    L.close_frame(fr, pad=60)
    return fr["y"] + fr["height"]


# ── today → proposed: the servers/ tree ──────────────────────────────────────────────────────
DIR_MEANING = {"_host": "the transport: serve, auth, config, the live namespace",
               "haipipe-page": "the standalone Page server", "space-home": "SPACE Home, Board-level writes",
               "workbench": "the base: the frame, Runs panel, Studio, Guide; vanilla with no theme",
               "workbench-work": "the work theme (once task): work_theme.py on the frame"}
FILE_MEANING = {"runs_panel.py": ("the Runs panel, every theme's (moved in from the Page code)", GRAY),
                "frame.py": ("the frame: levels, six Spaces, third row, vanilla defaults", TEAL),
                "frame_view.py": ("its route, /_board/workbench", TEAL),
                "work_theme.py": ("the work theme on the frame", TEAL),
                "work_items.py": ("the BJTR tree: only paper uses it", GRAY),
                "xcal.py": ("Studio: draw (Excalidraw editor, save)", GRAY), "chat.py": ("Studio: chat", GRAY),
                "term.py": ("Studio: terminal", GRAY), "guide_families.py": ("Guide: each family's entry", GRAY),
                "workbench_guide.py": ("Guide: the presenter", GRAY), "related_papers.py": ("Related Papers cards", GRAY),
                "shared_workbench.py": ("its own site: Guide is its only Space", GRAY)}


def today_tree():
    """servers/ as it is on disk: each folder, its Python files (a run of name_*.py folded into one line)."""
    rows = [("servers/", "", INK)]
    dirs = sorted(d for d in SERVERS.iterdir() if d.is_dir() and not d.name.startswith("__"))
    for i, d in enumerate(dirs):
        last = i == len(dirs) - 1
        name = d.name + "/"
        mean = DIR_MEANING.get(d.name, "a family: its own page, Space row, CSS")
        rows.append((("└── " if last else "├── ") + name, mean, INK))
        files = sorted(f.name for f in d.glob("*.py") if f.name != "__init__.py")
        files += [s.name + "/" for s in sorted(d.iterdir()) if s.is_dir() and any(s.glob("*.py"))
                  and s.name not in ("studio", "tests", "checks", "exporters", "assets", "live")]
        groups = {}
        for f in files:
            groups.setdefault(f.split("_")[0] if "_" in f else f, []).append(f)
        shown = []
        for key, fs in groups.items():
            special = [f for f in fs if f in FILE_MEANING]
            if len(fs) >= 3 and not special:
                shown.append((f"{key}_*.py  ×{len(fs)}", "", GRAY))
            else:
                shown += [(f, *FILE_MEANING.get(f, ("the Page Task's own views (once workbench-page)", TEAL)
                                                if f == "task-page/" else ("", GRAY))) for f in fs]
        for k, (f, m, c) in enumerate(shown):
            pre = ("    " if last else "│   ") + ("└── " if k == len(shown) - 1 else "├── ")
            rows.append((pre + f, m, c))
    return rows


PROPOSED_TREE = [   # what is done (teal) and what is left (red), 261007
    ("servers/", "", INK),
    ("├── _host/", "+ the route /_board/workbench (done)", TEAL),
    ("├── workbench/   (done: was workbench-shared)", "the base; vanilla with no theme", TEAL),
    ("│   ├── frame.py · frame_view.py   (done)", "levels, six Spaces, third row, vanilla defaults", TEAL),
    ("│   ├── runs_panel.py   (done, moved)", "the Runs panel, every theme's", TEAL),
    ("│   ├── task-page/   (done: was workbench-page)", "the Page Task's own views", TEAL),
    ("│   ├── guide/ · related/   (done)", "the base's own Guide, read from guide/guide.yaml", TEAL),
    ("│   ├── work_items.py   open ?", "the BJTR tree under every Work Details: the frame lists only the children", RED),
    ("│   ├── one look   open ?", "the frame has one CSS; the old pages keep theirs until each theme moves", RED),
    ("│   └── Studio", "Studio: one card per studio topic (done, 261007)", TEAL),
    ("├── workbench-work/   (done: was workbench-task)", "work_theme.py on the frame; b17 owns it", TEAL),
    ("├── workbench-cowork/ · -design/   (done)", "cowork_theme.py · design_theme.py on the frame", TEAL),
    ("├── workbench-<theme>/   open ?", "theme left: discovery · labeling · paper · insight (waits on DIKW)", RED),
    ("├── every workbench-*/guide/ · related/   (done)", "all nine Guides read from guide.yaml (261007)", TEAL),
    ("├── workbench-labeling/   (done: moved in)", "its write door and `--only labeling` host stay", TEAL),
    ("└── haipipe-page/ · space-home/", "unchanged", GRAY),
    ("", "", INK),
    ("skills/…/workbench-frame/   open ?", "the frame contract (today: servers/workbench/README.md)", RED),
]


def draw_tree(x, y, rows, title, color):
    text(x, y, title, 18, color)
    name_w = max(len(n) for n, _, _ in rows) * 14 * 0.6 + 24
    for k, (n, m, c) in enumerate(rows):
        ry = y + 36 + k * 22
        text(x, ry, n, 14, c if n.lstrip("│├└─ ").endswith(("(new)", "(moved)", "?")) or c in (RED, TEAL)
             and n.strip() else INK, MONO)
        if m:
            text(x + name_w, ry + 1, m, 13, c if c != INK else GRAY)
    return x + name_w + max(len(m) for _, m, _ in rows) * 13 * 0.55, y + 36 + len(rows) * 22


def frame_trees(y):
    fr = L.open_frame("today → proposed · the servers/ tree")
    text(0, y, "The servers/ tree: today, and what is done and left", 30)
    text(0, y + 46, "Left read off the disk at build time; right the proposal: red = new, moved or open (?), "
                    "gray = unchanged.", 16, GRAY)
    right, b1 = draw_tree(0, y + 100, today_tree(), "today", INK)
    path([(right + 40, y + 300), (right + 160, y + 300)], color=INK)
    _, b2 = draw_tree(right + 200, y + 100, PROPOSED_TREE, "proposed", TEAL)
    L.close_frame(fr, pad=60)
    return fr["y"] + fr["height"]



SHARED_OWNS = ["top: Guide · Studio | Block · Job · Task", "shared Studio; five Spaces in work mode",
               "the third row (draws it)", "Studio: same Block topics at every level", "Runs panel, grouped by run type",
               "Report: Question │ Work │ Report", "BJTR tree under Work", "Guide", "header · band · look (one CSS)"]
FAMILY_FILLS = ["which levels it has (a Page family: Task only)", "what each Space shows, at each level",
                "the names in it (Code · Review · Notebooks …)", "which drawings", "its run types (its workbench table)",
                "its questions and reports", "its folders", "its guide/ and related/ folders (done)", "its title and band line"]


def frame_proposed(y):
    fr = L.open_frame("proposed · the frame")
    text(0, y, "The frame: the base owns it, a theme fills it (built 261007)", 30)
    text(0, y + 46, "One row per part: left the frame, right what a family hands it. A family never draws a tab "
                    "row; the frame never learns a family's words.", 16, GRAY)
    LX, RX, top = 0, 760, y + 110
    box(LX, top, 620, 44, "workbench  (the frame)", 18, TEAL)
    box(RX, top, 700, 44, "a family workbench  (task · paper · insight · …)", 18, INK)
    for k, (a, b) in enumerate(zip(SHARED_OWNS, FAMILY_FILLS)):
        ry = top + 70 + k * 30
        text(LX + 16, ry, a, 15, TEAL)
        text(RX + 16, ry, b, 15, INK)
        path([(RX - 10, ry + 10), (LX + 630, ry + 10)], color=GRAY)
    hy = top + 70 + len(SHARED_OWNS) * 30 + 30
    text(LX, hy, "the hand-over, one call per level:", 15, INK)
    text(LX, hy + 26, "spaces(level, path) → {Space: (subspaces, content, run types)}", 15, INK, MONO)
    text(LX, hy + 56, "and a skill to match the server, as workbench-page / workbench-paper: "
                      "skills/…/workbench-frame, the frame contract ?  (open)", 15, RED)
    L.els.append(canvas.change_note(LX, hy + 90, "sNN topics now belong to the Block only", date="261010", frame=L.FRAME[0], size=16))
    L.close_frame(fr, pad=60)
    return fr["y"] + fr["height"]


# ── the base and a theme: shared holds the levels, a workbench-xxx gives its theme ─────────────
BASE_SPACES = ["Description", "Studio", "Report", "Work Details", "Runs", "Delivery"]
BASE_GROUP = [0, 1, 2, 3, 4, 5]               # each Space has its own column and divider
BASE = {   # level -> what each Space reads by default, from the standard folder layout
    "Block": ["bNN_<topic>.md", "studio/sNN-<topic>/", "reports/qNN_<topic>/\nQuestion │ Work │ Report",
              "its Jobs: jNN_<job>/", "runs/<run>/ by type\n+ from below", "delivery/"],
    "Job": ["jNN_<job>.md", "same Block Studio", "reports/ (optional)", "its Tasks: tNN_<task>/", "runs/<run>/ by type\n+ from below",
            "delivery/"],
    "Task": ["tNN_<task>.md", "same Block Studio", "its report", "how the work is done", "hard rNN_ · soft run-\nrun.yaml cards",
             "delivery/"]}
THEMES = [   # (theme folder, [(field, value, colour)]); views/ = a Space's own body, where config is not enough
    ("workbench-work/work_theme.py   (done)", [
        ("levels", "Block · Job · Task", INK), ("theme", "work (once task); the level stays Task", INK),
        ("Description (Task)", "Scope · Plan", INK), ("Report", "Draft · Report", INK),
        ("Work Details (Task)", "Code · Review · Notebooks", INK), ("Runs", "run · build · report", INK),
        ("run types", "Plan · Build · Run · Check a Task", INK), ("Guide", "workbench-work/guide/ (done)", INK),
        ("views/", "none", GRAY)]),
    ("workbench-paper/   config + views", [
        ("levels", "Block · Job · Task", INK), ("names", "paper Board · paper version · Section", INK),
        ("Description (Block)", "+ Venue: venues/<venue>/", INK), ("Studio", "Ideation", INK),
        ("Work Details (Job)", "its Sections, in compile order", INK), ("Delivery (Job)", "the whole paper: LaTeX · Word", INK),
        ("run types", "its workbench table", INK), ("Guide", "workbench-paper/guide/ (done)", INK),
        ("views/", "story.py: the Story (spine, claims) ?  open", RED)]),
    ("workbench/task-page/   (in the base)", [
        ("level", "Task: a Page Task  (a Section is one)", INK), ("theme", "any: the Page views of the base", INK),
        ("Report", "Table · Reading", INK),
        ("Work Details", "Draft-Scratch · Draft-Revise ·\nEvidence-Citation · -Display ·\n-Value · -Supporting Runs", INK),
        ("Runs", "structure · section · display · delivery", INK), ("Guide", "task-page/guide/ (done)", INK),
        ("views", "outline editor · evidence · exports\n(moved in from workbench-page)", TEAL)])]
MAY = ["name its levels", "pick which levels it has", "name the subspaces in each Space", "add fields to a Space",
       "list its run types", "keep its own guide/ and related/", "replace one Space's body with its own view"]
MAY_NOT = ["change the levels (Block · Job · Task)", "change the six Spaces or their order", "draw its own tab rows",
           "carry its own look (CSS)"]


def frame_base(y):
    fr = L.open_frame("proposed · the base and a theme")
    text(0, y, "The base: workbench holds Block · Job · Task; a workbench-xxx gives its theme", 30)
    text(0, y + 46, "Top: the base, one row per level, one column per Space, each cell what it reads by default "
                    "(a theme with nothing special works as is). Below: three themes filled in.", 16, GRAY)
    LX, CX, CW, RH, top = 0, 160, 260, 76, y + 110
    text(LX, top + 8, "workbench", 16, TEAL)
    for i, sp_ in enumerate(BASE_SPACES):
        cx = CX + i * CW + BASE_GROUP[i] * 24
        base("rectangle", cx, top, CW - 12, 34, TEAL, 1.5)
        text(cx + 12, top + 8, sp_, 15, TEAL)
        if i and BASE_GROUP[i] != BASE_GROUP[i - 1]:                   # the dividers
            path([(cx - 18, top - 6), (cx - 18, top + 44 + 3 * RH)], arrow=False, color=INK)
    for r, (level, cells) in enumerate(BASE.items()):
        ry = top + 48 + r * RH
        text(LX, ry + 18, level, 18, INK)
        for i, c in enumerate(cells):
            cx = CX + i * CW + BASE_GROUP[i] * 24
            base("rectangle", cx, ry, CW - 12, RH - 10, GRAY, 1)
            text(cx + 10, ry + 10, c, 13, INK, MONO)
    ty = top + 48 + 3 * RH + 50
    text(LX, ty, "a theme, one folder per Theme of the Project (tasks/ · papers/ · …): workbench-xxx/theme.py "
                 "(declared) + views/ (optional code)", 16, INK)
    TW = 640
    bottom = ty
    for k, (name, rows) in enumerate(THEMES):
        tx = LX + k * (TW + 40)
        box(tx, ty + 34, TW - 20, 40, name, 16, INK)
        ry = ty + 90
        for field, value, color in rows:
            text(tx + 12, ry, field, 14, GRAY)
            text(tx + 220, ry, value, 14, color, MONO if field != "Guide" else L.SANS)
            ry += 24 + 18 * value.count("\n")
        base("rectangle", tx, ty + 80, TW - 20, ry - (ty + 80) + 8, GRAY, 1, dashed=True)
        bottom = max(bottom, ry + 8)
    for k, (head, items, color) in enumerate([("a theme may", MAY, INK), ("a theme may not", MAY_NOT, RED)]):
        mx = LX + k * 700
        text(mx, bottom + 40, head, 18, color)
        for j, it in enumerate(items):
            text(mx + 12, bottom + 72 + j * 24, ("· " if color == INK else "✗ ") + it, 15, color)
    L.els.append(canvas.change_note(LX, bottom + 258, "Job and Task open the same Block-owned Studio", date="261010", frame=L.FRAME[0], size=16))
    L.close_frame(fr, pad=60)
    return fr["y"] + fr["height"]



STEPS = [("1 ✓", "runs_panel.py moved into the base", "done 261007"),
         ("2 ✓", "The frame built in the base; the work theme on it", "frame.py, /_board/workbench, test_frame.py"),
         ("3", "Each theme writes its <theme>_theme.py and moves onto the frame", "3 of 7: work · cowork · design"),
         ("4 ✓", "Each theme's own guide/ and related/, read from guide/guide.yaml", "all nine families, 261007"),
         ("5", "The vanilla Job and Task filled from s12 · s13", "")]
OPEN = ["insight fits the frame (its session, 261007): partitions = Report's third row, DIKW levels = Jobs,",
        "   its Insight table = Question │ Work │ Report, its question map = a generated, view-only Studio row",
        "labeling: its theme goes on the frame (b15); its write door and `--only labeling` host stay as they are",
        "? insight's DIKW: at the Block level or the Job level (b11 waits on this to write insight_theme.py)",
        "? insight's Check (a question's gates) has no Space: chips on each question row?",
        "? the paper's Job tab: workbench-paper as the version Job (s12)",
        "? a Run opened in the pop-out (the base pop-out is built: frame.pop, [data-pop]), and Plan · Build · Run · Report chips on child rows (b17)",
        "? the README's Space order (each family names its Spaces) gives way to the six Spaces"]


def frame_steps(y):
    fr = L.open_frame("steps and open points")
    text(0, y, "Steps (✓ done), and what JL decides", 30)
    for k, (n, what, note) in enumerate(STEPS):
        ry = y + 70 + k * 34
        text(0, ry, n, 18, INK)
        text(30, ry, what, 16, INK)
        text(700, ry + 2, note, 14, GRAY)
    oy = y + 70 + len(STEPS) * 34 + 30
    for k, q in enumerate(OPEN):
        text(0, oy + k * 26, q, 16, RED if q.startswith("?") else INK)
    base("rectangle", 0, oy + len(OPEN) * 26 + 20, 1300, 160, GRAY, 1)     # room to write
    text(12, oy + len(OPEN) * 26 + 28, "(write here)", 13, GRAY)
    L.close_frame(fr, pad=60)
    return fr["y"] + fr["height"]


# ── on screen: the frame the base draws, drawn large as s04 draws its Spaces (JL 261007: "I want the real ui") ──
VANILLA = {  # level -> (tabs, active tab, open Space, third row, table heads, rows, runs panel, recent, on disk)
    "Block": (["Guide", "Block", "Job · j11 ▾", "Task · t02 ▾"], 1, "Work Details", ["All", "j0N", "j1N", "j5N"],
              ["Job", "Tasks", "state"],
              [("j01_<data>", "3 Tasks", "done"), ("j11_<job>", "4 Tasks", "running"), ("j12_<job>", "2 Tasks", "planned")],
              ["Add a Job", "Plan the Jobs"], "run-plan-jobs   p01 closed",
              [("bNN_<topic>/", ""), ("├── bNN_<topic>.md", "the band: title · state; Description"),
               ("├── j01_<data>/ · j11_<job>/ …", "Work Details: one row per Job folder"),
               ("│   └── jNN_<job>.md", "the row: its title and state"),
               ("├── studio/ · reports/ · delivery/", "Studio · Report · Delivery"),
               ("└── runs/", "the Runs panel: the Block's own soft Runs"),
               ("servers/workbench/", "the base, which draws all of it:"),
               ("├── frame.py", "the tabs, the six Spaces, the third row"),
               ("├── frame_view.py", "each Space's rows, read from the folders"),
               ("├── runs_panel.py", "the Runs panel"),
               ("└── work_items.py  ?", "the BJTR tree under each row (open)")]),
    "Job": (["Guide", "Block", "Job · j11 ▾", "Task · t02 ▾"], 2, "Work Details", ["All", "t0N", "t1N"],
            ["Task", "kind · Runs", "state"],
            [("t01_<task>", "work · 3 Runs", "done"), ("t02_<task>", "Page · 2 Runs", "draft"),
             ("t03_<task>", "work · 1 Run", "planned")],
            ["Add a Task", "Launch all"], "run-launch-<group>   p02 open",
            [("jNN_<job>/", ""), ("├── jNN_<job>.md", "the band; its own Questions, if any"),
             ("├── t01_<task>/ · t02_<task>/ …", "Work Details: one row per Task folder"),
             ("│   └── tNN_<task>.md", "the row: kind · state"),
             ("├── src/ · sbatch/", "they mark a Job; listed in Description"),
             ("└── runs/", "soft only: run-plan-tasks · run-launch-<group>"),
             ("servers/workbench/frame.py", "the same frame, one level down")]),
    "Task": (["Guide", "Block", "Job · j11 ▾", "Task · t02 ▾"], 3, "Runs", ["All", "hard", "soft"],
             ["Run", "kind · type", "status · passes"],
             [("r01_<slug>", "hard · fit", "closed · 2"), ("r02_<slug>", "hard · evaluate", "open · 1"),
              ("run-report-<target>", "soft · report", "closed · 1")],
             ["Plan a Run", "Run it", "Check a Task"], "r02_<slug>   p01 running",
             [("tNN_<task>/", ""), ("├── tNN_<task>.md", "the band: the Task's face"),
              ("├── runs/", "the Space: one row per Run folder"),
              ("│   ├── r01_<slug>/run.yaml", "the row: kind · type · status · passes"),
              ("│   ├── r01_<slug>/result/", "the Run pop-out's preview"),
              ("│   └── run-<type>-<target>/run.yaml", "a soft Run's row"),
              ("└── scripts/ · config/", "Work Details (the work theme: Code)"),
              ("servers/workbench/runs_panel.py", "the panel; run.yaml cards from frame_view.py")])}
THEMED = {  # theme -> one Block screen through its theme: (tabs, third row, rows, on disk)
    "work theme": (["Guide", "Block", "Job · j11 ▾", "Task · t02 ▾"], ["All", "j0N", "j1N", "j5N"],
                   [("j01_<data>", "3 Tasks", "done"), ("j11_<job>", "4 Tasks", "running"),
                    ("j51_<dataset>", "5 Tasks", "planned")],
                   [("servers/workbench-work/", ""),
                    ("└── work_theme.py", "levels Block · Job · Task; the third row j0N · j1N · j5N;"),
                    ("", "names: Code · Review · Notebooks; run types"),
                    ("<Project>/work/bNN_<topic>/ …", "the folders it reads")]),
    "paper theme": (["Guide", "Paper Board", "Version · j02 ▾", "Section · S-2 ▾"], ["All", "versions", "grants", "slides"],
                    [("j01_v1_<venue>", "11 Sections", "submitted"), ("j02_v2_<venue>", "11 Sections", "drafting"),
                     ("j21_grant_<name>", "3 Pages", "planned")],
                    [("servers/workbench-paper/", ""),
                     ("├── paper_theme.py  ?", "names its levels: Paper Board · Version · Section;"),
                     ("│", "the third row versions · grants · slides"),
                     ("└── views/story.py  ?", "the Story: its own body in one Space (open)"),
                     ("<Project>/paper/Paper-<Name>/ …", "the folders it reads")])}


table, runs_panel, on_disk = UI.table, UI.runs_panel, UI.on_disk


def chrome(x, y, tabs, on, space, third, dashed=()):
    """Draw s02's reference screens with the live Studio entry and five lower Space buttons."""
    tabs = list(tabs)
    tabs[1:1] = ["Studio", "|"]
    old_row = UI.SPACE_ROW
    try:
        UI.SPACE_ROW = ["Description", "|", "Report", "|", "Work Details", "|", "Runs", "Delivery"]
        UI.chrome(x, y, tabs, on + 2, space, third, dashed=dashed)
    finally:
        UI.SPACE_ROW = old_row
    L.els.append(canvas.change_note(x + 24, y + UI.SH + 8,
                                    "Live: work mode keeps five Spaces; Studio hides them",
                                    date="261010", frame=L.FRAME[0], size=20))


def frame_screens(x0, y0):
    """The base on screen: one level per screen, each opening the Space that shows its children or its Runs."""
    fr = L.open_frame("on screen · the base, at Block, Job and Task")
    text(x0, y0, "The base on screen: the frame every theme gets, at each level", 34)
    text(x0, y0 + 50, "No theme: the vanilla frame reads the standard folders. A row's ↗ opens the level below "
                      "(a Job, a Task) or, for a Run, its pop-out.", 20, GRAY)
    for i, level in enumerate(["Block", "Job", "Task"]):
        tabs, on, space, third, heads, rows, buttons, recent, disk = VANILLA[level]
        x, y = x0 + i * (UI.SW + 120), y0 + 150
        text(x, y0 + 110, f"{level} tab · {space}", 24)
        chrome(x, y, tabs, on, space, third)
        table(x + 24, y + 190, heads, rows)
        runs_panel(x, y, buttons, recent)
        on_disk(x, y + UI.SH + 50, disk)
    px = x0 + 3 * (UI.SW + 120)
    text(px, y0 + 110, "pop-out, from a Run row's ↗", 24)
    UI.window(px, y0 + 150, UI.PW, 560, "r01_<slug>  ·  the Run", [
        "run.yaml: kind hard · type fit · target t02", "  skill · agent · signs (the person)",
        "passes: p01 1001 failed · p02 1003 ok", "[ result/ preview: metrics · the first figure ]",
        "  heavy.yaml -> ProjectResult/<...>/<run>/", "  open the folder · Rerun · Check"])
    L.close_frame(fr, pad=60)
    return fr


def frame_themed(x0, y0):
    """A theme on the base: the same Block screen, two themes; only the words and the rows change."""
    fr = L.open_frame("on screen · a theme on the base")
    text(x0, y0, "A theme on the base: the same Block screen, two themes", 34)
    text(x0, y0 + 50, "A theme may name its levels, set the third row and add views; it may not change the levels, "
                      "the six Spaces, their order, or draw its own tabs.", 20, GRAY)
    for i, (name, (tabs, third, rows, disk)) in enumerate(THEMED.items()):
        x, y = x0 + i * (UI.SW + 120), y0 + 150
        text(x, y0 + 110, f"{name} · Block › Work Details", 24)
        chrome(x, y, tabs, 1, "Work Details", third)
        table(x + 24, y + 190, ["Job", "Tasks" if "work" in name else "Sections", "state"], rows)
        runs_panel(x, y, ["Add a Job", "Plan the Jobs"] if "work" in name else ["Add a version", "Compile the paper"],
                   "run-plan-jobs   p01 closed" if "work" in name else "run-delivery-latex   p03 closed")
        on_disk(x, y + UI.SH + 50, disk)
    L.close_frame(fr, pad=60)
    return fr


# The current discussion row: Block topics, linked Jobs, separate Studio and Report.
DISCUSSION_NAMES = (
    "Shared workbench across levels",
    "Block topics construct Jobs",
    "Studio and Report",
)


def changed(x, y, words):
    L.els.append(canvas.change_note(x, y, words, date="261010", frame=L.FRAME[0], size=20))


def card(x, y, w, h, title, body):
    base("rectangle", x, y, w, h, INK, 1.5, rough=0)
    text(x + 20, y + 16, title, 23)
    if body:
        text(x + 20, y + 56, body, 20)


def compact_chrome(x, y, w, h, level, space, filters=()):
    """The live top Studio entry and Block context, with proposed topic content below."""
    base("rectangle", x, y, w, h, INK, 1.5, rough=0)
    tx = x + 24
    for label in ("Guide", "Studio", "|", "Block", "Job jNN", "Task tNN"):
        text(tx, y + 20, label, 20)
        if (label == "Studio" if space == "Studio" else label.startswith(level)):
            path([(tx, y + 49), (tx + len(label) * 11, y + 49)], arrow=False, color=INK)
        tx += len(label) * 11 + (20 if label == "|" else 40)
    if space == "Studio":
        text(x + 24, y + 78, "Workbench · Studio · bNN · Block name", 23)
    else:
        sx = x + 24
        for name in (s for s in BASE_SPACES if s != "Studio"):
            if name in ("Report", "Work Details", "Runs"):
                path([(sx, y + 76), (sx, y + 102)], arrow=False, color=INK)
                sx += 18
            bw = len(name) * 11 + 24
            base("rectangle", sx, y + 68, bw, 42, INK, 2 if name == space else 1, rough=0)
            text(sx + 12, y + 77, name, 20)
            sx += bw + 18
    path([(x, y + 126), (x + w, y + 126)], arrow=False, color=INK)
    fx = x + 24
    for label in filters:
        bw = len(label) * 11 + 28
        base("rectangle", fx, y + 144, bw, 42, INK, 1, rough=0)
        text(fx + 14, y + 152, label, 20)
        fx += bw + 12


def frame_shared_levels():
    fr = L.open_frame(DISCUSSION_NAMES[0])
    text(0, 0, "Shared workbench across levels", 38)
    text(0, 62, "Q08: one shared frame; the Block owns ideation, Jobs and Tasks open related Block topics.", 23)
    sy = 160
    compact_chrome(0, sy, 1500, 820, "Block", "Studio",
                   filters=("Current", "Guide", "Server", "Structure", "UI", "Workflow", "All"))
    path([(1160, sy + 126), (1160, sy + 820)], arrow=False, color=INK)
    text(24, sy + 210, "Studio: one row per Block bNN topic", 23)
    for yy, label in ((sy + 266, "s01-<topic>  [Structure]  ·  exploring  ·  no Job yet"),
                      (sy + 338, "s02-<topic>  [Structure] [UI]  ·  linked Jobs j01, j02")):
        base("rectangle", 24, yy, 1110, 56, INK, 1, rough=0)
        text(42, yy + 15, label, 20)
    card(24, sy + 410, 1110, 205, "s02: working drawing and topic notes",
         "Ideas -> choices -> agreed plan\nFrames hold the plan and its supporting material.\n[Create Job from topic]   [Open linked Job]")
    text(24, sy + 662, "Topic source: Block / studio / s02-<topic>", 21)
    text(24, sy + 710, "Drag cards into Current; All shows the whole Block list.", 20)
    text(24, sy + 758, "sNN = topic; group = references. Source keeps old local topics distinct.", 20)
    text(1180, sy + 152, "Disk: Block source", 21)
    for k, line in enumerate(("studio/", "s02-<topic>/", "topic notes", "source drawing", "builder / preview")):
        text(1180, sy + 200 + k * 34, line, 20)
    text(1180, sy + 430, "Runs: topic history", 21)
    text(1180, sy + 478, "run-draw-s02\nworking sessions\nredraw / save", 20)
    card(1600, 160, 830, 235, "Studio from a Job: same Block topics",
         "Studio alone is selected; no work Space row.\nTopics, Disk and sessions use the Block.\nThe Job remains context in the top controls.\n[Job] returns to its work Space and view.")
    card(1600, 440, 830, 225, "Studio from a Task: same Block topics",
         "The Task opens the same Block Studio.\nThe Task remains context in the controls.\n[Task] returns to its work Space and view.\nNew topics and topic Runs belong to the Block.")
    card(1600, 710, 830, 270, "Guide's Index and the separate Report",
         "Guide: [Index] [Description] [Method]\n[RoadMap Draw] [Related Paper]\nIndex returns to the SPACE studio overview.\nReport: Question -> supporting work -> answer\nReports use selected topic frames and evidence.\nReport ownership follows its own rules.")
    changed(1600, 1004, "s02-D13: Current first, All last; drag or use Add to Current")
    card(0, 1060, 740, 140, "Block source",
         "bNN_<block>/studio/sNN-<topic>/\nOne topic and one source drawing.")
    card(850, 1060, 740, 140, "Job link and execution",
         "bNN_<block>/jNN_<job>/\nJob face -> Block topic; Tasks below.")
    card(1700, 1060, 740, 140, "Task and actual Runs",
         "jNN_<job>/tNN_<task>/runs/<run>/\nResults come from actual executions.")
    path([(740, 1130), (850, 1130)], color=INK)
    path([(1590, 1130), (1700, 1130)], color=INK)
    changed(0, 1260, "sNN topics now belong to the Block only")
    changed(0, 1300, "Jobs are constructed from and linked to Block topics")
    changed(0, 1340, "Studio and Report are separate Spaces")
    changed(0, 1380, "Live: Studio and Block buttons; Block bNN stays in the title")
    changed(0, 1420, "s02-D08: shorter button names; existing Studio links still work")
    changed(0, 1450, "s02-D09: shared Studio; only Studio selected; no work Space row")
    changed(1400, 1260, "s02-D11: Block name + Index + topic tag filters")
    changed(1400, 1300, "Tags live in each topic; buttons read this Block")
    changed(1400, 1340, "s02-D12: top row is Guide / Studio / Block / Job / Task")
    L.close_frame(fr, pad=60)
    return fr


def frame_topic_jobs():
    fr = L.open_frame(DISCUSSION_NAMES[1])
    text(0, 0, "Block topics construct Jobs", 38)
    text(0, 62, "Q07: ideation stays in the Block; a ready topic supplies the plan for a linked Job.", 23)
    card(0, 160, 740, 245, "Block / s02-<topic>",
         "Explore the idea and compare choices.\nRecord the agreed plan and open questions.\nKeep the drawing and its history here.\nA topic may remain exploratory.")
    card(850, 160, 740, 245, "Job j01_<job>",
         "Create a Job from the agreed plan.\nRecord its goal, close and source topic.\nThe Job link opens Block / s02.\nThe Job keeps its jNN identity.")
    card(1700, 160, 740, 245, "Task tNN -> Run rNN",
         "Tasks split the Job into pieces of work.\nRuns are the actual executions.\nResults provide evidence for Reports.\nFind the topic through the Job link.")
    path([(740, 278), (850, 278)], color=INK)
    path([(1590, 278), (1700, 278)], color=INK)
    card(0, 495, 1130, 320, "Block Studio: topics and linked Jobs", "")
    for dx, head in ((20, "Topic"), (410, "State"), (750, "Linked Jobs")):
        text(dx, 558, head, 20)
    for yy, row in ((606, ("s01-<topic>", "exploring", "none yet")),
                    (680, ("s02-<topic>", "plan agreed", "j01 · j02"))):
        base("rectangle", 20, yy, 1090, 58, INK, 1, rough=0)
        for dx, value in zip((36, 410, 750), row):
            text(dx, yy + 16, value, 20)
    text(20, 766, "Select s02 -> its drawing, decisions and linked Jobs.", 20)
    card(1310, 495, 1130, 320, "Job face: plan and source link", "")
    for k, line in enumerate(("Source topic: Block / s02 (link)", "Goal: <work agreed in the topic>",
                              "Close: <what must be true when done>", "Tasks: t01_<task> · t02_<task>",
                              "Answers: Q01 (when it answers a Question)")):
        text(1330, 560 + k * 44, line, 20)
    text(0, 875, "One Block topic can lead to zero, one or several Jobs; sNN and jNN stay linked and distinct.", 23)
    card(0, 955, 740, 170, "Topic source stays in the Block",
         "bNN_<block>/studio/s02-<topic>/\nTopic notes, drawing and topic sessions.")
    card(850, 955, 740, 170, "The Job owns its execution plan",
         "bNN_<block>/j01_<job>/j01_<job>.md\nIts source-topic link points back to s02.")
    card(1700, 955, 740, 170, "Evidence stays with the actual Run",
         "j01_<job>/tNN_<task>/runs/rNN_<run>/\nThe Report cites the resulting evidence.")
    path([(740, 1040), (850, 1040)], color=INK)
    path([(1590, 1040), (1700, 1040)], color=INK)
    changed(0, 1200, "Jobs are constructed from and linked to Block topics")
    text(0, 1260, "? Where is the durable source-topic link stored on the Job face?", 22, RED)
    text(0, 1304, "? How do existing Job and Task Studios move into the Block without losing links?", 22, RED)
    L.close_frame(fr, pad=60)
    return fr


def frame_separate_spaces():
    fr = L.open_frame(DISCUSSION_NAMES[2])
    text(0, 0, "Studio and Report", 38)
    text(0, 62, "Q09: separate Spaces with separate purposes, connected by topic, work and figure links.", 23)
    sy, rx, sw = 160, 1340, 1240
    compact_chrome(0, sy, sw, 860, "Block", "Studio")
    compact_chrome(rx, sy, sw, 860, "Block", "Report", ("Questions", "Reading"))
    text(24, sy + 212, "s02-<topic> · Block-owned thinking", 23)
    card(24, sy + 270, 1192, 310, "Working drawing: ideas, choices and plan", "")
    for x, title, body in ((44, "Idea", "<what to explore>"),
                            (440, "Choice", "<agreed approach>"),
                            (836, "Plan", "<work for a Job>")):
        card(x, sy + 360, 360, 110, title, body)
    path([(404, sy + 415), (440, sy + 415)], color=INK)
    path([(800, sy + 415), (836, sy + 415)], color=INK)
    text(44, sy + 520, "? <choice still being discussed>", 20, RED)
    text(24, sy + 638, "Feeds: Q01 · Q02   [Open Report]", 21)
    text(24, sy + 692, "Linked Jobs: j01 · j02   [Create Job from topic]", 21)
    text(24, sy + 752, "Drafts, alternatives, decisions and marks live here.", 20)
    text(24, sy + 800, "Jobs return to this same Block-owned topic.", 20)
    qx = rx + 24
    for dx, head in ((0, "Question"), (250, "Supporting work"), (670, "Report")):
        text(qx + dx, sy + 212, head, 22)
    for yy, question, work, answer in ((sy + 270, "Q01 · <question>", "Job j01 · j02", "<current answer; partial>"),
                                      (sy + 450, "Q02 · <question>", "Job j02 / Tasks", "<answer with evidence>")):
        base("rectangle", qx, yy, 1192, 145, INK, 1, rough=0)
        for dx in (232, 652):
            path([(qx + dx, yy), (qx + dx, yy + 145)], arrow=False, color=INK)
        text(qx + 16, yy + 20, question, 20)
        text(qx + 250, yy + 20, work, 20)
        text(qx + 250, yy + 70, "<Tasks / Run evidence>", 20)
        text(qx + 670, yy + 20, answer, 20)
        text(qx + 670, yy + 70, "Topic frames: s02 (link)", 20)
        text(qx + 670, yy + 110, "[Read]  [Open source topic]", 20)
    text(qx, sy + 638, "Opening · Answer · Evidence · Limits · Next", 21)
    text(qx, sy + 692, "Report figures use selected Block topic frames.", 20)
    text(qx, sy + 752, "A topic can feed several Reports, and vice versa.", 20)
    text(qx, sy + 800, "[Open source] returns to Studio and its topic.", 20)
    path([(1240, sy + 650), (1340, sy + 650)], color=INK)
    path([(1340, sy + 790), (1240, sy + 790)], color=INK)
    text(0, 1060, "Open Report -> work mode / Report. Open source -> shared Studio; topic and canvas return proposed.", 22)
    card(0, 1120, 1240, 145, "Studio source and topic history",
         "Block / studio / sNN-<topic> / drawing + notes\nBlock / runs / run-draw-<sNN> / working sessions")
    card(rx, 1120, 1240, 145, "Report source and work evidence",
         "reports/qNN_<topic>/qNN_<topic>.md + figure list\nLinked Jobs -> Tasks -> actual Runs and their results")
    changed(0, 1310, "Studio and Report are separate Spaces")
    changed(0, 1350, "Live: Studio hides work buttons; Report belongs to work mode")
    changed(24, 1380, "s02-D10: Report button; existing Audience Report links still work")
    text(0, 1410, "? Keep topic, frame, Job filter and canvas position when moving between the Spaces?", 22, RED)
    L.close_frame(fr, pad=60)
    return fr


def discussion_row():
    """Place the current model above the reference drawing, without moving reference frames."""
    start = len(L.els)
    frames = [frame_shared_levels(), frame_topic_jobs(), frame_separate_spaces()]
    new_elements = L.els[start:]
    canvas.grid(new_elements, [[fr["id"] for fr in frames]], gap=180)
    bottom = max(fr["y"] + fr["height"] for fr in frames)
    for element in new_elements:
        element["y"] -= bottom + 500
    L.FRAME[0] = None



ROWS = [  # the reading order (JL 261007: "arrange well the current ones"): heading, then its frames left to right
    ("1 · The proposal: the base owns the frame, a theme fills it",
     [("proposed · the frame", "1 · the frame: who owns what"),
      ("proposed · the base and a theme", "2 · the base and a theme")]),
    ("2 · On screen: what that looks like",
     [("on screen · the base, at Block, Job and Task", "3 · on screen: the base at Block, Job, Task"),
      ("on screen · a theme on the base", "4 · on screen: a theme on the base")]),
    ("3 · Today: what the code does now",
     [("today · who owns which part", "5 · today: which files use each part"),
      ("today · the Spaces drawn", "6 · today: each workbench's Spaces"),
      ("today → proposed · the servers/ tree", "7 · today → proposed: the servers/ tree")]),
    ("4 · Next", [("steps and open points", "8 · steps and open points")]),
]


def arrange():
    """Move each frame, with everything in it, into its row; rows top to bottom, a heading over each."""
    frames = {e["name"]: e for e in L.els if e["type"] == "frame"}
    # Keep the established reference rows in place as the code inventory grows.
    row_tops = (0, 1620.75, 3554.75, 5614.25)
    row_xs = ((0, 1880), (0, 6180), (0, 3550, 5202.2), (0,))
    for (heading, names), y, xs in zip(ROWS, row_tops, row_xs):
        text(0, y, heading, 48)
        y += 110
        row_h = 0
        for (old, new), x in zip(names, xs):
            fr = frames[old]
            dx, dy = x - fr["x"], y - fr["y"]
            for e in L.els:
                if e is fr or e.get("frameId") == fr["id"]:
                    e["x"] += dx
                    e["y"] += dy
            fr["name"] = new
            row_h = max(row_h, fr["height"])
        y += row_h + 400


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s02-workbench-shared.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    y = 0
    for draw in (frame_today, frame_trees, frame_spaces, frame_proposed, frame_base, frame_steps):
        y = draw(y) + 160
    a = frame_screens(0, y)
    frame_themed(0, a["y"] + a["height"] + 300)
    arrange()
    discussion_row()
    canvas.write(out, list(L.els), "build_s02_workbench_shared.py")


if __name__ == "__main__":
    main()
