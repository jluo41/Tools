"""The base frame every theme draws in, and the vanilla workbench when no theme is laid over it.

    Guide · Block · Job ▾ · Task ▾                                        level tabs
    Description | Idea Studio · Audience Report | Work Details | Runs · Delivery   the six Spaces
    <subspaces>                                                           the third row
    content                                                  │ Runs panel

The frame owns the levels, the six Spaces, their order and dividers, the third row, the Runs
panel and the look (Tools/blueprints/b01_haipipe-toolkit/j03_project_workbench, Q08 and studio/s02-workbench-shared). A theme
gives only what each Space holds at each level: `servers/workbench-<theme>/<theme>_theme.py`
exports `THEME`, a `Theme`. A Space a theme leaves out shows the vanilla default, read from the
standard folders (the face `.md`, `studio/`, `reports/`, the child `jNN_` / `tNN_` folders,
`runs/`, `delivery/`), so a theme with nothing special works as is.

A theme may name its levels, pick which levels it has, name the subspaces of each Space, fill a
Space's content and list its run types. It may not change the levels, the six Spaces or their
order, draw its own tab rows, or carry its own look.

Read-only: nothing here writes. Every link is origin-relative (`/_board/workbench?path=…`).
"""
from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Callable
from urllib.parse import quote, urlencode

LEVELS = ("Block", "Job", "Task")
# (Space, divider group, optional): the bars in the Spaces row fall between groups
SPACES = (("Description", 0, False), ("Idea Studio", 1, True), ("Audience Report", 1, True),
          ("Work Details", 2, False), ("Runs", 3, False), ("Delivery", 3, True))
SPACE_NAMES = tuple(name for name, _, _ in SPACES)
_LEVEL_OF = {"b": "Block", "j": "Job", "t": "Task"}
_PREFIXED = re.compile(r"^([bjt])\d+_")
# a Project's Theme folder -> the theme that reads it (old plural names read the same, s01-D29)
THEME_FOLDERS = {"tasks": "work", "work": "work", "discoveries": "discovery", "discovery": "discovery",
                 "cowork": "cowork", "papers": "paper", "paper": "paper", "insights": "insight",
                 "insight": "insight", "designs": "design", "design": "design",
                 "labelings": "labeling", "labeling": "labeling"}
ROUTE = "/_board/workbench"
# the skill that owns each level's own buttons (Update the description, Add a Job or Task, Build the delivery);
# every frame button names its skill (b03 s21-D02; haipipe-run ref/run-types-by-space.md)
LEVEL_SKILL = {"Block": "haipipe-board", "Job": "haipipe-job", "Task": "haipipe-task"}


def _e(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


@dataclass
class Space:
    """What one Space shows: its subspaces (the third row), the open one, its content and run types.

    `run_types` are Runs-panel kinds: {"label", "prompt", "skills"?}; `{folder}` in a prompt is the
    open folder, SPACE-relative. An empty field means "the vanilla default"."""
    html: str = ""
    subspaces: tuple = ()
    open: str = ""
    run_types: tuple = ()
    keep: tuple = ()           # the base's subspaces a theme keeps beside its own (a Task's Page views)
    note: str = ""             # one line at the top of the Runs panel (a view no run changes says so)
    page: bool = False         # laid out by page_task_spaces (a theme that extends it keeps the mark)
    disk: tuple = ()           # what the screen reads: (path under the open folder, what it feeds); a glob counts


@dataclass
class Theme:
    """A theme: its names and, per level, what its Spaces hold. `spaces(level, folder, root, sub)`
    returns {Space name: Space}; anything it leaves out is the vanilla default."""
    name: str = "vanilla"
    label: str = "Workbench"
    icon: str = "🧭"
    guide: str = "shared"                      # the Guide family it mounts (workbench/guide_families.py)
    levels: tuple = LEVELS
    level_names: dict = field(default_factory=dict)
    spaces: Callable | None = None
    hide_empty_levels: bool = False            # a level with no folders: greyed tab (default), or none
    # each of the theme's own buttons -> the Run it makes, `run-<type>-<target>` (haipipe-run rule 6, JL
    # 261007: "for all the soft run, the name of them will be run-xxxx-xxx"): the frame shows the name
    # as the button and the theme's words in small under it; a theme may also name its buttons so itself
    run_names: dict = field(default_factory=dict)
    # the theme's own names for its Job and Task folders, beside jNN_ / tNN_ (b03, 261007): a regex per
    # level matched against a folder's name, e.g. {"Job": r"^B[a-z]-", "Task": r"^S-"} for a paper's
    # version groups and Sections. A Job pattern counts only directly under its Block, a Task pattern only
    # directly under one of its Jobs.
    level_patterns: dict = field(default_factory=dict)
    # claims(block) -> bool: a Block this theme reads although its Theme folder names another (an
    # Insight or labeling Block kept in tasks/, 261007); asked before the Theme folder decides
    claims: Callable | None = None
    # option(folder) -> (label, group) for the Job ▾ / Task ▾ dropdown, or None for the folder's name
    # (b12 s32, 261008: a design Task shows "Task · d04 · reason-then-ask", grouped by its step)
    option: Callable | None = None

    def level_name(self, level: str) -> str:
        return self.level_names.get(level, level)


VANILLA = Theme()


# ── where a folder sits on the ladder ───────────────────────────────────────────────────────────
def level_of(folder: Path) -> str | None:
    """Block, Job or Task, from the folder's name (bNN_, jNN_, tNN_); a Block may also be known by
    its board.md; else by its theme's own names (Theme.level_patterns), one level below its parent's."""
    m = _PREFIXED.match(folder.name)
    if m:
        return _LEVEL_OF[m.group(1)]
    if (folder / "board.md").is_file():
        return "Block"
    patterns = _patterns_for(folder)
    if not patterns:
        return None
    below = {"Block": "Job", "Job": "Task"}.get(level_of(folder.parent) or "")
    return below if below and below in patterns and re.search(patterns[below], folder.name) else None


def _block_above(folder: Path) -> Path | None:
    """The nearest Block holding this folder (a bNN_ folder, or one with a board.md), never itself."""
    for p in folder.parents:
        if (_PREFIXED.match(p.name) and p.name[0] == "b") or (p / "board.md").is_file():
            return p
    return None


def theme_folder(block: Path) -> Path:
    """The Theme folder a Block sits in: its parent, or, for a Block kept in an archive inside a Theme
    folder (`designs/_old/B01_…`, a name starting with "_"), the folder above the archive (b12, JL
    261008: an older board still reads in its theme)."""
    return block.parent.parent if block.parent.name.startswith("_") else block.parent


def _patterns_for(folder: Path) -> dict:
    """The level patterns of the theme whose Block holds this folder (by its Theme folder, in a
    Project); {} for the vanilla frame or a theme that declares none."""
    block = _block_above(folder)
    if block is None or not is_project(theme_folder(block).parent):
        return {}
    name = _claimed(block) or THEME_FOLDERS.get(theme_folder(block).name)
    return _theme_patterns().get(name, {}) if name else {}


_PATTERNS: dict = {}


def _theme_patterns() -> dict:
    """{theme name: level_patterns}, read once from the themes."""
    if not _PATTERNS:
        _PATTERNS.update({name: t.level_patterns for name, t in themes().items()} or {"vanilla": {}})
    return _PATTERNS


def chain(folder: Path, root: Path) -> dict:
    """{level: folder} from the open folder up to its Block, inside root."""
    found, cur = {}, folder
    while True:
        level = level_of(cur)
        if level and level not in found:
            found[level] = cur
        if level == "Block" or cur == root or root not in cur.parents:
            return found
        cur = cur.parent


def children(folder: Path, level: str) -> list:
    """The child folders one level down: a Block's Jobs, a Job's Tasks (jNN_ / tNN_, or the theme's
    own names, Theme.level_patterns)."""
    want = {"Block": "Job", "Job": "Task"}.get(level)
    if not want or not folder.is_dir():
        return []
    return sorted(p for p in folder.iterdir() if p.is_dir() and not p.name.startswith((".", "_"))
                  and level_of(p) == want)


def face(folder: Path) -> Path | None:
    """The folder's face: `<folder>.md`, else a Block's `board.md`."""
    for name in (folder.name + ".md", "board.md"):
        if (folder / name).is_file():
            return folder / name
    return None


def is_project(folder: Path) -> bool:
    """A Project folder: it carries project.yaml, or is named Project-<name> (haipipe-project)."""
    return (folder / "project.yaml").is_file() or folder.name.startswith("Project")


def theme_of(folder: Path, root: Path) -> str:
    """The theme a folder belongs to: the Theme folder its Block sits in (tasks/ or work/ -> work),
    counted only inside a Project, so a design Block of the Tools repo (Tools/blueprints/bNN_*) reads
    as vanilla rather than as the design theme."""
    block = chain(folder, root).get("Block", folder)
    if not is_project(theme_folder(block).parent):
        return "vanilla"
    return _claimed(block) or THEME_FOLDERS.get(theme_folder(block).name, "vanilla")


_CLAIMS: dict = {}


def _claimed(block: Path) -> str:
    """The theme that claims this Block by what it holds (Theme.claims), or ""; asked once per Block
    and board.md version, since level_of asks often."""
    face_md = block / "board.md"
    key = (str(block), face_md.stat().st_mtime if face_md.is_file() else 0)
    if key not in _CLAIMS:
        _CLAIMS[key] = ""
        for name, theme in themes().items():
            try:
                if theme.claims and theme.claims(block):
                    _CLAIMS[key] = name
                    break
            except Exception:                    # a theme's check that fails claims nothing
                continue
    return _CLAIMS[key]


def _rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _title(md: Path) -> str:
    try:
        lines = md.read_text(encoding="utf-8", errors="ignore").splitlines()[:40]
        for i, line in enumerate(lines):
            if line.startswith("# "):
                return line[2:].strip()
            if line.strip() and i + 1 < len(lines) and re.fullmatch(r"={3,}", lines[i + 1].strip()):
                return line.strip()
    except OSError:
        pass
    return md.stem


def _fields(md: Path, keys=("board-kind", "spine", "goal", "state", "close", "answer-status", "status")) -> list:
    out = []
    try:
        for line in md.read_text(encoding="utf-8", errors="ignore").splitlines()[:60]:
            m = re.match(r"^\s*([a-z][a-z-]+):\s*(.+)$", line)
            if m and m.group(1) in keys:
                out.append((m.group(1), m.group(2).strip()))
    except OSError:
        pass
    return out


def _yaml_scalar(text: str, key: str) -> str:
    m = re.search(rf"(?m)^{key}:\s*(.+?)\s*$", text)
    if not m:
        return ""
    value = m.group(1).split("#", 1)[0].strip()
    return value.strip("[]").split(",", 1)[0].strip()


def runs_of(folder: Path) -> list:
    """Every Run in the folder's runs/: one folder each (hard rNN_, soft run-<type>-<target>), or a
    ticket in the older layout; its type and status from run.yaml where it has one."""
    rdir = folder / "runs"
    if not rdir.is_dir():
        return []
    rows = []
    for p in sorted(rdir.iterdir()):
        if p.name.startswith((".", "_")) or p.name == "README.md":
            continue
        name = p.stem if p.is_file() else p.name
        card = p / "run.yaml" if p.is_dir() else None
        text = card.read_text(encoding="utf-8", errors="ignore") if card and card.is_file() else ""
        kind = "soft" if name.startswith("run-") else "hard"
        rtype = _yaml_scalar(text, "type") or (name.split("-")[1] if kind == "soft" and "-" in name else "run")
        rows.append({"run": name, "kind": kind, "type": rtype, "status": _yaml_scalar(text, "status") or "—",
                     "path": p})
    return rows


# ── the vanilla default of each Space ───────────────────────────────────────────────────────────
def _link(href: str, label: str) -> str:
    return f'<a href="{_e(href)}">{_e(label)}</a>'


def pop(href: str, label: str, text: str = "") -> str:
    """A link that opens in the frame's pop-out (an in-page window with an own-tab link); a
    modifier-click still opens it in its own tab."""
    return (f'<a data-pop="{_e(label)}" href="{_e(href)}" target=_blank rel=noopener>{_e(text or label)}</a>')


def _reader(path: Path, root: Path) -> str:
    return "/_board/page?" + urlencode({"path": "/" + _rel(path, root)})


def _table(heads, rows) -> str:
    if not rows:
        return '<p class=mut>Nothing here yet.</p>'
    head = "".join(f"<th>{_e(h)}</th>" for h in heads)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f"<table class=wf-table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


# A Task's Page views (workbench/task-page/), each once a route and a page of its own, shown in place as
# a subspace of the Space it belongs to (JL 261007: "why not merge them into the base"):
# {Space: ((subspace, view), ...)}; the view is served by this route, `?view=<view>&path=<face>`.
PAGE_VIEWS = {"Description": (("Folder", "folder"),),
              "Audience Report": (("Draft", "draft"),),
              "Work Details": (("Evidence", "evidence"), ("Value", "value")),
              "Runs": (("Page Runs", "runs"),),
              "Delivery": (("Lanes", "delivery"),)}


# what each Page view reads, for the Disk box (workbench/task-page/: each module's docstring)
PAGE_VIEW_DISK = {"folder": (("./", "every lane of the Page folder, and how old each is"),),
                  "draft": (("{face}", "the Page: its Content divisions, aims and states"),
                            ("draft/", "the plan versions, Scratch and Revise")),
                  "evidence": (("runs/*/passes/*/result.yaml", "one card per Evidence Result, by type (older Pages: results/*/)"),),
                  "value": (("evidence/probe/*/card.md", "## Values: the numbers a probe card holds"),
                            ("{face}", "the sentences that cite PP<NN>.v<n>")),
                  "runs": (("runs/", "the Page's Runs: planned, registered, done"),),
                  "delivery": (("delivery/", "one segment per lane: latex · word · slide · render"),)}


def page_view(view: str, md: Path, root: Path) -> str:
    """One Page view, in place: the page its route draws, framed."""
    src = ROUTE + "?" + urlencode({"view": view, "path": _rel(md, root)})
    return (f'<iframe class=page-view src="{_e(src)}&amp;embed=1" loading=lazy title="{_e(view)}"></iframe>'
            f'<p class=mut>{_link(src, "open on its own ↗")}</p>')


def with_page_views(out: dict, level: str, folder: Path, root: Path, sub: str, first: dict) -> dict:
    """Add a Task's Page views to its Spaces: each Space's own content becomes its first subspace
    (named in `first`), the views follow; the open one is drawn."""
    md = face(folder)
    if level != "Task" or not md or md.name == "board.md":
        return out
    for space, views in PAGE_VIEWS.items():
        v = out.get(space, Space())
        own = v.subspaces or (first[space],)
        views = tuple((n, view) for n, view in views if n not in own)   # a theme's own view of that name wins
        names = tuple(n for n, _ in views)
        opened = sub if sub in names else (v.open or own[0])
        html_ = next((page_view(view, md, root) for n, view in views if n == sub), v.html)
        disk = next((tuple((d.replace("{face}", md.name), m) for d, m in PAGE_VIEW_DISK[view])
                     for n, view in views if n == sub), v.disk)
        out[space] = replace(v, html=html_, subspaces=own + names, open=opened, keep=names, disk=disk)
    return out


def run_type(name: str, doing: str, prompt: str, skill: str, **more) -> dict:
    """A Runs-panel type named by the soft Run it makes (JL 261007: "for all the soft run, the name of
    them will be run-xxxx-xxx"; haipipe-run ref/run-types-by-space.md), what it does in small under it."""
    return {"label": name, "doing": doing, "prompt": prompt, "skills": [skill], **more}


def named(kinds, names: dict) -> tuple:
    """Each run type whose label is in `names` takes that Run name as its label, its own words kept as
    what it does (the small line under the button)."""
    return tuple(dict(k, label=names[k["label"]], doing=k.get("doing") or k["label"])
                 if k.get("label") in names else k for k in kinds)


def fill_tag(name: str, folder: Path) -> str:
    """A Run name's placeholder for this folder's own level filled with its tag, as the base names its own
    buttons (b17 s32, 261008): run-plan-<tNN> in t01_fit -> run-plan-t01; other placeholders stay."""
    m = _PREFIXED.match(folder.name)
    if not m:
        return name
    return name.replace(f"<{m.group(1)}NN>", folder.name.split("_", 1)[0])


RUN_ANY = run_type("run-<type>-<target>", "start a Run (a work Task's hard Runs: rNN_<slug>)",
                   "Start a Run in {folder}/runs/.", "haipipe-run")


def vanilla(level: str, folder: Path, root: Path, sub: str = "") -> dict:
    """{Space: Space}: what every Space shows when no theme fills it."""
    out = {}
    tag = (_PREFIXED.match(folder.name).group(0).rstrip("_") if _PREFIXED.match(folder.name)
           else {"Block": "<bNN>", "Job": "<jNN>"}.get(level, "<tNN>"))
    md = face(folder)
    if md:
        rows = [(_e(k), _e(v)) for k, v in _fields(md)]
        out["Description"] = Space(
            f'<h2>{_e(_title(md))}</h2><p class=mut>{_link(_reader(md, root), _rel(md, root))}</p>'
            + (_table(("field", "value"), rows) if rows else ""),
            run_types=(run_type(f"run-face-{tag}", "update the description", "Update the face of {folder}.",
                                LEVEL_SKILL.get(level, LEVEL_SKILL["Task"])),))
    else:
        out["Description"] = Space(f'<p class=mut>No face file: {_e(folder.name)}.md is missing.</p>')

    out["Idea Studio"] = Space(studio_cards(folder, root), run_types=(
        run_type("run-draw-<sNN>", "add a topic · redraw it · save this session, each a pass",
                 "/haipipe-studio a topic of {folder}: new topic → studio/sNN-<topic>/ and runs/run-draw-<sNN>/; "
                 "redraw or this session → a pass of run-draw-<sNN>.", "haipipe-studio",
                 rows=studio_sessions(folder, root)),))

    rows_html, groups = question_rows(level, folder, root, sub)
    has_questions = "q-row" in rows_html
    if level == "Task" and not has_questions and md:          # a Task's report is its own face
        rows_html = (f'<div class=q-row><div class=q-l><p class=q-head><b>the Page</b></p></div>'
                     f'<div class=q-w>{" · ".join(_e(r["run"]) for r in runs_of(folder)) or "<span class=mut>no Runs yet</span>"}</div>'
                     f'<div class=q-r>{pop(_reader(md, root), "the Page", _title(md) + " ↗")}</div></div>')
    out["Audience Report"] = Space(rows_html, subspaces=("All",) + tuple(groups) if groups else (),
                                   open=(sub or "All") if groups else "", run_types=(
        run_type("run-ask-<qNN>", "ask a Question", "Ask a new Question of {folder}: its register row and "
                 "reports/qNN_<topic>/.", "haipipe-question"),
        run_type("run-report-<qNN>", "write the report", "Write or update a report of {folder}.", "haipipe-report"),
        run_type("run-figures-<qNN>", "rebuild the report drawing", "Rebuild a report drawing of {folder} from its "
                 "## Figures list: haipipe-report scripts/build_report_drawing.py <report folder>.", "haipipe-report"),
        run_type("run-check-<qNN>", "check a report", "Check a report of {folder} in a fresh context.",
                 "haipipe-report")))

    if level in ("Block", "Job"):
        kids = children(folder, level)
        rows = []
        for k in kids:
            kmd = face(k)
            count = len(children(k, "Job")) if level == "Block" else len(runs_of(k))
            rows.append((_link(ROUTE + "?" + urlencode({"path": _rel(k, root)}), k.name),
                         _e(_title(kmd) if kmd else "—"), _e(count)))
        out["Work Details"] = Space(_table(("Job" if level == "Block" else "Task", "title",
                                            "Tasks" if level == "Block" else "Runs"), rows),
                                    run_types=(run_type("run-add-<jNN>" if level == "Block" else "run-add-<tNN>",
                                                        "add a " + ("Job" if level == "Block" else "Task"),
                                                        "Add a " + ("Job" if level == "Block" else "Task") + " to {folder}.",
                                                        LEVEL_SKILL.get(level, LEVEL_SKILL["Task"])),))
    else:
        rows = [(_e(p.name + "/"), _e(sum(1 for _ in p.rglob("*") if _.is_file())))
                for p in sorted(folder.iterdir()) if p.is_dir() and not p.name.startswith((".", "_"))
                and p.name not in ("runs", "studio", "reports", "delivery")] if folder.is_dir() else []
        out["Work Details"] = Space(_table(("folder", "files"), rows),
                                    run_types=(run_type(f"run-build-{tag}", "build the Task", "Build {folder}.",
                                                        "haipipe-task"),))

    runs = runs_of(folder)
    types = sorted({r["type"] for r in runs})
    shown = [r for r in runs if sub in ("", "All") or r["type"] == sub]
    out["Runs"] = Space(
        _table(("Run", "kind", "type", "status"),
               [(_e(r["run"] + ("/" if r["path"].is_dir() else "")), _e(r["kind"]), _e(r["type"]), _e(r["status"]))
                for r in shown]),
        subspaces=("All",) + tuple(types) if runs else (), open=sub or ("All" if runs else ""),
        run_types=(RUN_ANY,))

    deliv = folder / "delivery"
    rows = [(_e(p.name + ("/" if p.is_dir() else "")), _e(sum(1 for _ in p.rglob("*") if _.is_file()) if p.is_dir() else ""))
            for p in sorted(deliv.iterdir()) if not p.name.startswith(".")] if deliv.is_dir() else []
    out["Delivery"] = Space(_table(("item", "files"), rows),
                            run_types=(run_type(f"run-delivery-{tag}", "build the delivery", "Build the delivery of {folder}.",
                                                LEVEL_SKILL.get(level, LEVEL_SKILL["Task"])),))
    for name, disk in vanilla_disk(level, md.name if md else folder.name + ".md").items():
        out[name] = replace(out[name], disk=disk)
    return with_page_views(out, level, folder, root, sub, {"Description": "Face", "Audience Report": "Report",
                                                           "Work Details": "Folders", "Runs": "All",
                                                           "Delivery": "Files"})


# ── Disk: the files behind the open Space (JL 261007: "add the disks as well, to show what files are
# associated with the content in the screen ... so we have both disks and runs") ─────────────────
def vanilla_disk(level: str, face_name: str) -> dict:
    """{Space: ((path, what it feeds), ...)}: what each vanilla Space reads, under the open folder."""
    kids = {"Block": ("j[0-9]*_*/", "one row per Job: its face's title, its Tasks"),
            "Job": ("t[0-9]*_*/", "one row per Task: its face's title, its Runs")}.get(level)
    return {
        "Description": ((face_name, "the face: its title and fields"),),
        "Idea Studio": (("studio/s*/", "one row per topic"),
                        ("studio/s*/s*.md", "a row's details: decided · open · feeds"),
                        ("studio/s*/*.excalidraw", "the live drawing an open row shows"),
                        ("runs/run-draw-*/passes/", "a topic's sessions, one pass each")),
        "Audience Report": ((face_name, "## Questions: one row per Question, its group"),
                            ("reports/q*/q*.md", "Report: the title and its answer line"),
                            ("reports/q*/q*.png", "Report: the drawing's thumbnail"),
                            ("studio/s*/s*.md", "from the Idea Studio: each topic's feeds: line")),
        "Work Details": ((kids,) if kids else (("./", "its own folders, with their file counts"),)),
        "Runs": (("runs/*/", "one row per Run: kind · type · status, grouped by type"),),
        "Delivery": (("delivery/", "one row per item, with its file count"),),
    }


def disk_markup(entries, folder: Path, root: Path, most: int = 4) -> str:
    """The Disk list: one row per file or folder the open Space reads (JL 261007: "each row is a file
    or folder"), grouped under a short label with its count. A group shows `most` rows and folds the
    rest under "+N more"; a row is the name (a folder ends in /, a .md opens in the reader, the full
    path on hover); what is not there yet is one greyed row."""
    if not entries:
        return ""

    def row(p: Path) -> str:
        rel = p.relative_to(folder).as_posix() if p != folder else "."
        if p.is_dir():
            n = sum(1 for c in p.iterdir() if not c.name.startswith("."))
            return (f'<li title="{_e(rel)}/"><span class=disk-p>{_e(p.name if p != folder else ".")}/</span>'
                    f'<span class=disk-n>{n}</span></li>')
        name = _link(_reader(p, root), p.name) if p.suffix == ".md" else _e(p.name)
        return f'<li title="{_e(rel)}"><span class=disk-p>{name}</span></li>'

    groups = []
    for path, meaning in entries:
        wants_dir = path.endswith("/")
        if any(ch in path for ch in "*?["):
            found = [m for m in sorted(folder.glob(path.rstrip("/"))) if m.is_dir() or not wants_dir]
        else:
            target = folder if path in ("", "./", ".") else folder / path
            found = [target] if target.exists() else []
        if not found:
            body = f'<li class=miss title="{_e(path)}"><span class=disk-p>{_e(path)}</span><span class=disk-n>not yet</span></li>'
        else:
            body = "".join(row(m) for m in found[:most])
            if len(found) > most:
                body += (f'<li class=disk-more><details><summary>+{len(found) - most} more</summary><ul>'
                         + "".join(row(m) for m in found[most:]) + "</ul></details></li>")
        groups.append(f'<li class=disk-g><p class=disk-gl title="{_e(path)}"><span>{_e(meaning)}</span>'
                      f'<span class=disk-n>{len(found) or ""}</span></p><ul>{body}</ul></li>')
    return (f'<div class=disk-in><p class=disk-head><b>Disk</b> <span class=mut>under {_e(folder.name)}/</span></p>'
            f'<ul class=disk-list>{"".join(groups)}</ul></div>')


DISK_CSS = """
.disk-in{padding:0 0 10px;border-bottom:1px solid var(--line);font:13px/1.45 system-ui,sans-serif;min-width:0}
.disk-head{margin:0 0 6px;overflow-wrap:anywhere}
.disk-list,.disk-list ul{list-style:none;margin:0;padding:0}
.disk-list{max-height:36vh;overflow:auto}
.disk-g+.disk-g{margin-top:8px}
.disk-gl{display:flex;justify-content:space-between;gap:8px;margin:0 0 2px;color:var(--mut);font-size:12px}
.disk-gl span:first-child{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.disk-g li{display:flex;align-items:baseline;gap:8px;padding:1px 0 1px 12px;min-width:0}
.disk-p{flex:1 1 auto;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.disk-p a{color:var(--acc);text-decoration:none}.disk-p a:hover{text-decoration:underline}
.disk-n{flex:none;font-size:11.5px;color:var(--mut)}
.disk-g li.miss .disk-p{color:var(--mut);font-style:italic}
.disk-g li.disk-more{display:block;padding-left:12px}
.disk-more summary{cursor:pointer;color:var(--mut);font-size:12px;list-style:none}
.disk-more summary::-webkit-details-marker{display:none}
.disk-more ul li{padding-left:0}
/* the Runs: one row per run type, its count at the right (JL 261007: "each row to be an item") */
.split>.runs-panel .runs-body{min-width:0}
.split>.runs-panel .runs-types{flex-direction:column;flex-wrap:nowrap;align-items:stretch;gap:4px}
.split>.runs-panel .run-type{justify-content:space-between;text-align:left;padding:4px 10px;min-width:0}
.split>.runs-panel .run-list{flex-direction:column;align-items:stretch;overflow-x:visible}
.split>.runs-panel .run-list button{text-align:left}
.split>.runs-panel .runs-detail,.split>.runs-panel .run-card{min-width:0}
.split>.runs-panel .run-card header>b,.split>.runs-panel .run-card p,.split>.runs-panel .run-results{overflow-wrap:anywhere}
.split>.runs-panel .run-card button,.split>.runs-panel .run-state{flex:none;white-space:nowrap}
.split>.runs-panel .run-results,.split>.runs-panel .run-results code{font-size:12px}
"""


# ── Idea Studio: one closed row per studio topic, opened in place (b03 s04-D04, s04-D06) ───────
def _note_facts(md: Path | None) -> dict:
    """What a topic's notes file says: its **Topic:** line, decisions, open points, feeds."""
    if not md:
        return {"topic": "", "decided": 0, "open": 0, "feeds": []}
    text = md.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"\*\*Topic:\*\*\s*(.+?)(?:\n\s*\n|\Z)", text, re.S)
    topic = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    opened = re.search(r"(?ims)^(?:#+\s*)?Open\b[^\n]*\n(?:[-=]{3,}\n)?(.*?)(?=^\S[^\n]*\n[-=]{3,}\n|^#+ |\Z)", text)
    feeds = re.search(r"\*\*Feeds:\*\*(.+?)(?:\n\s*\n|\Z)", text, re.S)
    return {"topic": topic,
            "decided": len(re.findall(r"(?m)^s\d+-D\d+\b", text)),
            "open": len(re.findall(r"(?m)^\d+\.\s", opened.group(1))) if opened else 0,
            "feeds": list(dict.fromkeys(re.findall(r"q\d\d_[A-Za-z0-9_]+", feeds.group(1)))) if feeds else []}


def _notes(topic: Path) -> Path | None:
    if not topic.is_dir():
        return None
    md = topic / (topic.name + ".md")
    return md if md.is_file() else next(iter(sorted(topic.glob("*.md"))), None)


def _draw_url(d: Path, root: Path, edit: bool = False) -> str:
    return "/_excalidraw/?" + urlencode({"board": _rel(d, root), **({"edit": "1"} if edit else {})})


def _report_page(name: str, folder: Path, root: Path) -> Path | None:
    """reports/<name>/<name>.md at this level or one above."""
    for f in [folder] + list(chain(folder, root).values()):
        page = f / "reports" / name / (name + ".md")
        if page.is_file():
            return page
    return None


def _feed_chip(name: str, folder: Path, root: Path) -> str:
    """A Question the topic feeds: its report in the pop-out."""
    label = name.split("_", 1)[0].upper()
    page = _report_page(name, folder, root)
    if page:
        return f'<a class=chip data-pop="{_e(label)} · Report" href="{_e(_reader(page, root))}" title="{_e(name)}">{_e(label)}</a>'
    return f'<span class=chip title="{_e(name)}">{_e(label)}</span>'


def _sessions(topic: Path, folder: Path) -> list:
    """A topic's sessions: the passes of its soft Run `runs/run-draw-<sNN>/passes/pNN-<MMDD>/`
    (s04-D06), then the older `chat/` summaries until they move into passes."""
    out = []
    m = re.match(r"(s\d+)", topic.name)
    passes = folder / "runs" / f"run-draw-{m.group(1)}" / "passes" if m else None
    if passes and passes.is_dir():
        for p in sorted((p for p in passes.iterdir() if p.is_dir()), reverse=True):
            md = next(iter(sorted(p.glob("*.md"))), None)
            out.append({"name": p.name, "title": _title(md) if md else p.name, "path": md or p})
    if topic.is_dir() and (topic / "chat").is_dir():
        for md in sorted((topic / "chat").glob("*.md"), reverse=True):
            out.append({"name": md.stem, "title": _title(md), "path": md})
    return out


def _topic_row(topic: Path, drawings: list, root: Path, folder: Path) -> str:
    """One closed row, its name and one line; opened in place, the live drawing across the row."""
    md = _notes(topic)
    facts = _note_facts(md)
    name = topic.name if topic.is_dir() else topic.stem
    sessions = _sessions(topic, folder)
    meta = ([f'decided {facts["decided"]}', f'open {facts["open"]}'] if md else [])
    meta.append(f'{len(sessions)} session' + ("" if len(sessions) == 1 else "s"))
    feeds = (" · feeds " + " ".join(_feed_chip(q, folder, root) for q in facts["feeds"])) if facts["feeds"] else ""
    first = drawings[0] if drawings else None
    full = pop(_draw_url(first, root), f"{name} · the topic, full size", "↗") if first else ""
    scripts = sorted(topic.glob("build_*.py")) if topic.is_dir() else []
    # an opened row is only its drawing (JL 261007); a hand-drawn one edits in place from the row
    tools = [pop(_draw_url(d, root), d.stem, d.stem + " ↗") for d in drawings[1:]]
    if first and not scripts:
        tools.append('<button type=button class=draw-edit>Edit</button>')
    if first:
        body = (f'<iframe class=st-frame title="{_e(first.stem)}" data-src="{_e(_draw_url(first, root))}" '
                f'data-edit="{_e(_draw_url(first, root, True))}" referrerpolicy=no-referrer></iframe>')
    else:
        files = sorted(p.name for p in topic.iterdir() if p.is_file() and not p.name.startswith(".")) if topic.is_dir() else []
        body = f'<p class="mut none">No drawing; it holds {_e(" · ".join(files)) or "nothing yet"}.</p>'
    return (f'<details class=topic id="topic-{_e(name)}"><summary><b>{_e(name)}</b>'
            f'<span class=topic-meta>{" · ".join(meta)}{feeds}</span>'
            f'<span class=topic-pop>{" ".join(tools + ([full] if full else []))}</span></summary>{body}</details>')


def _studio_topics(folder: Path) -> list:
    """(topic, drawings) for each `studio/sNN-<topic>/`; a loose drawing is its own topic."""
    studio, out = folder / "studio", []
    if studio.is_dir():
        for p in sorted(studio.iterdir()):
            if p.is_dir() and not p.name.startswith(("_", ".")):
                out.append((p, sorted(p.glob("*.excalidraw"))))
            elif p.suffix == ".excalidraw":
                out.append((p, [p]))
    return out


def studio_cards(folder: Path, root: Path) -> str:
    """Idea Studio's default body: one closed row per studio topic, by name; a click opens it in
    place with its details and the live drawing across the row. Then where the next topic goes."""
    topics = _studio_topics(folder)
    last = max([int(m.group(1)) for t, _ in topics for m in [re.match(r"s(\d+)", t.name)] if m] or [0])
    add = f'<p class="mut add">+ Add topic → studio/s{last + 1:02d}-&lt;topic&gt;/</p>'
    rows = "".join(_topic_row(t, d, root, folder) for t, d in topics)
    return ('<p class=mut>One topic per row, by name; click one and it opens in place.</p>' + rows + add
            if rows else '<p class=mut>No studio topics yet.</p>' + add)


def studio_sessions(folder: Path, root: Path) -> list:
    """One Runs-panel row per topic that has sessions: its soft Run `run-draw-<sNN>`, its passes, and
    the older `chat/` sessions kept until they move into passes (JL 261007: the card read as a
    stray session; it is a pass of the topic's Run)."""
    rows = []
    for topic, _ in _studio_topics(folder):
        sessions = _sessions(topic, folder)
        if not sessions:
            continue
        sid = topic.name.split("-", 1)[0]
        run = folder / "runs" / f"run-draw-{sid}"
        older = sum(1 for s in sessions if s["path"].parent.name == "chat")
        passes = len(sessions) - older
        what = " · ".join(x for x in (f"{passes} pass{'es' if passes != 1 else ''}" if passes else "",
                                      f"{older} older chat/ session{'s' if older != 1 else ''}" if older else "") if x)
        rows.append({"run_id": f"run-draw-{sid}", "status": "done", "target": topic.name,
                     "_display": f"run-draw-{sid}", "_of": f"studio topic {topic.name} · {what}",
                     "result": _rel(run if run.is_dir() else sessions[0]["path"].parent, root),
                     "result_path": str(run / "passes" if run.is_dir() else sessions[0]["path"].parent)})
    return rows


# ── Audience Report: one row per Question, Logic │ Work │ Report (b03 s04-D04) ──────────────
def _register(md: Path | None) -> list:
    """The face's `## Questions` register (a fenced yaml `questions:` list), or []."""
    if not md:
        return []
    text = md.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"(?ms)^## Questions[ \t]*\n.*?```ya?ml\n(.*?)```", text)
    if not m:
        return []
    try:
        import yaml
        rows = (yaml.safe_load(m.group(1)) or {}).get("questions") or []
    except Exception:  # a broken register reads as none; the checker reports it
        return []
    return [r for r in rows if isinstance(r, dict) and r.get("id")]


def _opening(page: Path) -> str:
    """The report's answer line: the first paragraph of its Opening."""
    text = page.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"(?ms)^## Opening[ \t]*\n(.*?)(?=^## |\Z)", text)
    para = (m.group(1).strip().split("\n\n", 1)[0] if m else "")
    para = re.sub(r"<!--.*?-->", "", para, flags=re.S)
    para = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", para)
    return re.sub(r"\s+", " ", para.replace("**", "").replace("`", "")).strip()


def _answering(folder: Path, level: str, qid: str, root: Path) -> list:
    """The Jobs and Tasks under this level whose face says `answers: <qid>`."""
    found = []
    for kid in children(folder, level) if level in ("Block", "Job") else []:
        for f in [kid] + (children(kid, "Job") if level == "Block" else []):
            md = face(f)
            m = re.search(r"(?m)^answers:\s*(.+)$", md.read_text(encoding="utf-8", errors="ignore")) if md else None
            # haipipe-report's link rule: `answers: <id>`, or a need of it, `<id>.E<n>`
            if m and qid.lower() in [re.sub(r"(?i)\.E\d+$", "", w.strip()).lower()
                                     for w in re.split(r"[,\s\[\]]+", m.group(1))]:
                found.append(f)
    return found


def _report_cell(qid: str, page: Path | None, root: Path) -> str:
    """The work theme's Report cell: the title (the Page in the pop-out), its answer line, its one
    drawing as a thumbnail (generated, view only, in the pop-out), and a tag."""
    if not page:
        return '<p class=mut>No report yet</p>'
    tag = page.stem.split("_", 1)[0]
    status = dict(_fields(page)).get("answer-status", "open")
    drawing = page.with_suffix(".excalidraw")
    png = page.with_suffix(".png")
    if drawing.is_file() and png.is_file():
        pic = (f'<a class=rp-thumb data-pop="{_e(qid)} · Drawing · generated, view only" href="{_e(_draw_url(drawing, root))}" '
               f'target=_blank rel=noopener><img loading=lazy alt="{_e(page.stem)}" src="/{_e(_rel(png, root))}"></a>')
    elif drawing.is_file():
        pic = f'<p class=mut>{pop(_draw_url(drawing, root), qid + " · Drawing · generated, view only", "its drawing ↗")}</p>'
    else:
        pic = '<p class=mut>no drawing yet</p>'
    answer = _opening(page)
    return (f'<p class=rp-title>{pop(_reader(page, root), qid + " · Report · the Page", _title(page) + " ↗")}</p>'
            + (f'<p class=rp-text>{_e(answer)}</p>' if answer else '<p class=mut>no answer yet</p>')
            + pic + f'<p class=rp-tags>report {_e(tag)} · {_e(status)}</p>')


def question_rows(level: str, folder: Path, root: Path, sub: str = "") -> tuple:
    """(html, groups): one row per Question of this level: Logic (the question, its status, the
    studio topics that feed it) │ Work (the Jobs and Tasks that answer it) │ Report."""
    md = face(folder)
    reports = {q.name.split("_", 1)[0].lower(): q for q in sorted((folder / "reports").glob("q[0-9]*/"))} \
        if (folder / "reports").is_dir() else {}
    register = _register(md)
    rows = [dict(r) for r in register]
    known = {str(r["id"]).lower() for r in rows}
    rows += [{"id": k.upper(), "title": ""} for k in reports if k not in known]     # a report not yet registered
    feeders = {}
    for topic, drawings in _studio_topics(folder):
        for q in _note_facts(_notes(topic))["feeds"]:
            feeders.setdefault(q.split("_", 1)[0].lower(), []).append((topic, drawings[0] if drawings else None))
    groups = list(dict.fromkeys(str(r["group"]) for r in rows if r.get("group")))
    out = []
    for r in rows:
        if sub not in ("", "All") and str(r.get("group") or "") != sub:
            continue
        qid = str(r["id"])
        rp = r.get("report")
        page = (folder / rp) if rp and (folder / rp).is_file() else None
        if not page and qid.lower() in reports:
            q = reports[qid.lower()]
            page = q / (q.name + ".md") if (q / (q.name + ".md")).is_file() else None
        title = r.get("title") or (_title(page) if page else qid)
        status = dict(_fields(page)).get("answer-status", "open") if page else "open"
        studio = "".join(f'<li>{pop(_draw_url(d, root), t.name + " · from the Idea Studio", t.name + " ↗") if d else _e(t.name)}</li>'
                         for t, d in feeders.get(qid.lower(), []))
        logic = question_cell(qid, r, title, status) + (
            f'<p class=from>from the Idea Studio</p><ul class=from-list>{studio}</ul>' if studio else "")
        work = [str(w.get("task") or w.get("path") or w) if isinstance(w, dict) else str(w) for w in (r.get("work") or [])]
        kids = _answering(folder, level, qid, root)
        work_html = " · ".join([_link(ROUTE + "?" + urlencode({"path": _rel(k, root)}), _rel(k, folder)) for k in kids]
                               + [_e(w) for w in work if w]) or '<span class=mut>no work yet</span>'
        out.append(f'<div class=q-row id="question-{_e(qid)}"><div class=q-l>{logic}</div>'
                   f'<div class=q-w>{work_html}</div><div class=q-r>{_report_cell(qid, page, root)}</div></div>')
    if not out:
        return '<p class=mut>No Questions at this level yet.</p>', groups
    head = ('<div class="q-row q-head-row"><div>Logic · the question</div><div>Work · the Jobs, Tasks and Runs</div>'
            '<div>Report · what it says</div></div>')
    return head + "".join(out), groups

def _first_sentence(text: str, most: int = 160) -> str:
    """The question's first sentence, cut at `most` characters: the short explanation under its name."""
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    m = re.match(r"(.+?[.?!])(\s|$)", text)
    one = m.group(1) if m else text
    return one if len(one) <= most else one[:most].rsplit(" ", 1)[0] + " …"


def question_cell(qid: str, row: dict, title: str, status: str) -> str:
    """The Question cell, as the Insight row has it (JL 261007): a label (Question 1) and its state
    dot, the Question's short name, one short sentence of what is asked, then › More with the rest;
    no "builds on" line."""
    num = re.match(r"^[A-Za-z]*0*(\d+)$", qid)
    label = f"Question {num.group(1)}" if num else qid
    state = str(status or "open").lower()
    dot = "answered" if state.startswith("answered") else "partial" if state.startswith("partial") else "open"
    name = str(row.get("slug") or row.get("name") or title or qid)
    ask = str(row.get("question") or "")
    short = _first_sentence(ask) if ask and ask.strip() != name.strip() else ""
    more = [(k, row.get(k)) for k in ("question", "hypothesis", "acceptance") if row.get(k)]
    more_html = ("<details class=q-more><summary>› More</summary>" + "".join(
        f'<p><span class=mut>{_e(k)}</span> {_e(v)}</p>' for k, v in more) + "</details>") if more else ""
    return (f'<p class=q-top><span class=q-label>{_e(label)}</span>'
            f'<span class="q-dot {dot}" title="{_e(status or "open")}"></span></p>'
            f'<p class=q-slug>{_e(name)}</p>' + (f'<p class=q-text>{_e(short)}</p>' if short else "") + more_html)


# The helpers a theme may use, by public name (the underscore names stay as aliases):
# esc(text) · link(href, label) · reader(md, root) -> the Page reader's URL · rel(path, root) ->
# SPACE-relative · table(heads, rows) -> the frame's table · title(md) · fields(md) · runs_of(folder) ·
# studio_cards(folder, root) -> Idea Studio's topic cards · pop(href, label, text) -> a link that opens
# in the frame's pop-out (a Run, a drawing, a page)
esc, link, reader, rel, table, title, fields = _e, _link, _reader, _rel, _table, _title, _fields  # + studio_cards


def lays_out_page(name: str, subspaces, space=None) -> bool:
    """True when a theme laid the Page out in this Space itself: page_task_spaces marked it
    (Space.page), or its subspaces start with the base's Page Task views; it may add its own after
    them (paper's Reviews, b16 s13)."""
    if space is not None and getattr(space, "page", False):
        return True
    page = PAGE_TASK_SUBS.get(name)
    return bool(page) and tuple(subspaces)[:len(page)] == page


def spaces_for(theme: Theme, level: str, folder: Path, root: Path, sub: str = "") -> dict:
    """The theme's Spaces over the vanilla default, field by field."""
    base = vanilla(level, folder, root, sub)
    own = theme.spaces(level, folder, root, sub) if theme.spaces else {}
    if theme.run_names:                         # the theme's buttons named by their Runs, this folder's tag filled
        names = {k: fill_tag(n, folder) for k, n in theme.run_names.items()}
        own = {k: replace(v, run_types=named(v.run_types, names)) for k, v in own.items()}
    out = {}
    for name in SPACE_NAMES:
        v, t = base.get(name, Space()), own.get(name)
        if t is None:
            out[name] = v
            continue
        merged = replace(v, **{k: getattr(t, k) for k in ("html", "subspaces", "open", "run_types", "note", "disk")
                               if getattr(t, k)})
        if lays_out_page(name, t.subspaces, t):
            # the Page laid out: its runs and its third row as set, even none (Delivery has no third row)
            merged = replace(merged, run_types=t.run_types, subspaces=t.subspaces,
                             open=t.open if t.subspaces else "")
        # the base's Page views stay beside the theme's own subspaces, unless the theme laid the Page
        # out in this Space itself (page_task_spaces: the Page's exact views, embedded)
        if v.keep and not lays_out_page(name, t.subspaces, t):
            theirs = t.subspaces or v.subspaces           # a view the theme names too keeps its place
            merged = replace(merged, subspaces=theirs + tuple(k for k in v.keep if k not in theirs))
            if sub in v.keep and sub not in (t.subspaces or ()):    # a theme's own view of that name wins
                merged = replace(merged, html=v.html, open=sub, disk=v.disk)
        out[name] = merged
    return out


# ── the page ────────────────────────────────────────────────────────────────────────────────────
CSS = """
:root{--bg:#fff;--fg:#1c1c1c;--mut:#6f6f6b;--line:#e3e3e6;--acc:#3e5c84;--acc-soft:#e6edf5;--card:#fff;--ok:#24733d;--warn:#996b00;--miss:#c92a2a;--tab-line:#ced4da;--tab-on:#1864ab;--tab-wash:#e7f5ff;--wash:#f6f6f7}
@media(prefers-color-scheme:dark){:root{--bg:#161719;--fg:#e8e8e6;--mut:#a0a09c;--line:#2c2e33;--acc:#8aa7cc;--acc-soft:#22304a;--card:#161719;--ok:#8bd49a;--warn:#e4bd62;--miss:#ff8787;--tab-line:#414852;--tab-on:#91caff;--tab-wash:#253749;--wash:#1d1f22}}
*{box-sizing:border-box}body{margin:0;padding:16px;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
main{max-width:1600px}h1{font-size:18px;margin:0 0 2px}
/* the level row is the page index, the title under it the page's own title, wide gaps (b03 s32-D13, JL 261008) */
nav.levels{margin:0;padding-bottom:12px;border-bottom:1px solid var(--line)}
/* a faint line between the Spaces row and the view row, as light as the one under the index (JL 261008) */
nav.subs{border-top:1px solid var(--line);padding-top:10px;margin-top:10px}
header.page-title h1{font-size:26px;margin:22px 0 18px;line-height:1.25}header.page-title .lv{color:var(--mut);font-weight:400}h2{font-size:16px;margin:0 0 6px}a{color:var(--acc)}.mut{color:var(--mut);font-size:13px}
.row{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin:8px 0}
.tab{display:inline-block;padding:4px 12px;border:1px solid var(--line);border-radius:999px;color:var(--fg);text-decoration:none;font-size:14px;background:var(--card)}
.tab.on{border-color:var(--acc);color:var(--acc);font-weight:600}.tab.opt{border-style:dashed}
.levels select{font:inherit;font-size:14px;padding:3px 8px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--fg);field-sizing:content;max-width:32ch;text-overflow:ellipsis}
.levels select.on{border-color:var(--acc);color:var(--acc);font-weight:600}
.levels select:disabled{opacity:.45;cursor:default}
/* top tabs: the Insight and Design board pages' buttons (b03 s32-element-ui, picked D · E, JL 261007):
   16px, 6px corners, a grey border, the open one washed blue; the third row keeps its own until picked */
.levels .tab,.spaces .tab,.levels select{font:400 16px system-ui,sans-serif;padding:6px 14px;border:1px solid var(--tab-line);
 border-radius:6px;background:var(--bg);color:var(--fg)}
.levels select{padding:6px 10px}
.levels .lvl{display:inline-flex}.levels .lvl .tab{border-radius:6px 0 0 6px}
.levels .lvl select{border-radius:0 6px 6px 0;border-left:0;padding:6px 10px;appearance:none;-webkit-appearance:none;cursor:pointer}
.levels .tab.on,.spaces .tab.on,.levels select.on{border-color:var(--tab-on);color:var(--tab-on);background:var(--tab-wash);font-weight:400}
.levels .tab:hover,.spaces .tab:hover{border-color:var(--tab-on)}
.spaces .tab.opt{border-style:solid}   /* an optional Space looks like any other (JL 261007) */
.bar{display:inline-block;width:1px;height:22px;background:var(--fg);margin:0 6px}
.page-view{display:block;width:100%;height:calc(100vh - 260px);min-height:560px;border:1px solid var(--line);border-radius:8px;background:var(--bg)}
/* the view row (third row): the Page workbench's view buttons (b03 s32-element-ui, picked E, JL 261007; not the
   small pills): 16px, 6px corners, padding 5px 12px, the open one washed blue */
.subs .tab{font:400 16px system-ui,sans-serif;padding:5px 12px;border:1px solid var(--tab-line);border-radius:6px;
 background:transparent;color:var(--fg)}
.subs .tab.on{border-color:var(--tab-on);color:var(--tab-on);background:var(--tab-wash);font-weight:400}
.subs .tab:hover{border-color:var(--tab-on)}
.wf-table{border-collapse:collapse;width:100%;font-size:14px}.wf-table th,.wf-table td{text-align:left;padding:5px 8px;border-bottom:1px solid var(--line);vertical-align:top}
.wf-table th{font-weight:600;color:var(--mut);font-size:12.5px}
.topic{border:1px solid var(--line);border-radius:10px;background:var(--card);margin:0 0 8px;overflow:hidden}
.topic>summary{display:flex;gap:12px;align-items:baseline;cursor:pointer;padding:9px 14px;list-style:none}
.topic>summary::-webkit-details-marker{display:none}.topic>summary::before{content:"▸";color:var(--mut)}
.topic[open]>summary::before{content:"▾"}.topic[open]>summary{border-bottom:1px solid var(--line)}
.topic-meta{color:var(--mut);font-size:13px;flex:1}.topic-pop a{text-decoration:none;font-size:15px}
.topic .none{margin:10px 14px}.topic-pop{display:flex;gap:10px;align-items:baseline;font-size:13px}
.chip{display:inline-block;padding:0 8px;margin-right:4px;border:1px solid var(--acc);border-radius:999px;color:var(--acc);font-size:12px;text-decoration:none}
.st-bar{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;padding:8px 14px}
.draw-edit{font:500 12.5px -apple-system,sans-serif;border:1px solid var(--line);border-radius:6px;padding:1px 9px;cursor:pointer;background:var(--bg);color:var(--fg)}
.st-frame{display:block;width:100%;height:calc(100vh - 240px);min-height:520px;border:0;border-top:1px solid var(--line);background:#fff}
.add{margin:6px 2px 0}
.st-ok{color:var(--ok)}.st-warn{color:var(--warn)}
.dl-frame{display:block;width:100%;height:560px;border:0;border-top:1px solid var(--line);background:#fff}
.dl-note{padding:0 14px 10px;margin:0}.dl-src{max-height:420px;overflow:auto;margin:0 14px 12px}
.topic.missing{border:1px dashed var(--miss);background:transparent}.topic.missing>summary b{color:var(--mut)}
.q-row{display:grid;grid-template-columns:1.1fr 1fr 1.3fr;border:1px solid var(--line);border-radius:10px;margin:0 0 8px;background:var(--card)}
.q-row>div{padding:10px 12px;min-width:0}.q-row>div+div{border-left:1px solid var(--line)}
.q-head-row{border:0;background:transparent;margin:0;color:var(--mut);font-size:12.5px}.q-head-row>div{padding:2px 12px}.q-head-row>div+div{border-left:0}
/* level rows as the old Insight board drew them (b11, JL 261008): flush grey rows split by thin lines, a ▶
   marker, a small link on the right; the q-rows inside flush, like one table. A theme opts in by the classes. */
.dikw{border-top:1px solid var(--line);margin:4px 0 12px}
.dikw>.topic{border:0;border-bottom:1px solid var(--line);border-radius:0;margin:0;background:var(--wash)}
.dikw>.topic>summary{padding:8px 12px}.dikw>.topic>summary::before{content:"▶";color:var(--fg);font-size:11px}
.dikw>.topic[open]>summary::before{content:"▼"}.dikw .topic-meta{flex:1;font-size:13px}.dikw .lv-link{font-size:12.5px}
.q-table{padding:8px 0 12px;background:var(--bg)}.q-table>p.mut{margin:0 12px 6px;font-size:13px}
.q-table>.q-row{border-radius:0;margin:0;border-bottom-width:0}.q-table>.q-row:last-child{border-bottom-width:1px}
.q-head{margin:0}.kind{color:var(--mut);font-size:12.5px;font-weight:600}
.q-top{display:flex;align-items:center;gap:6px}
.q-label{display:inline-block;border:1px solid var(--tab-on);color:var(--tab-on);border-radius:999px;padding:0 8px;font:600 11.5px/1.6 system-ui,sans-serif}
.q-dot{display:inline-block;width:12px;height:12px;border-radius:50%;border:1px solid var(--tab-line);background:var(--bg)}
.q-dot.partial{background:#fcc419;border-color:#f59f00}.q-dot.answered{background:#40c057;border-color:#2f9e44}
.q-slug{margin:6px 0 2px!important;font-weight:700}.q-text{margin:0 0 4px!important}
.q-more summary{cursor:pointer;color:var(--acc);font-size:13px;list-style:none}.q-more summary::-webkit-details-marker{display:none}
.q-more p{font-size:13px}.q-row p{margin:0 0 4px}
.from{margin:8px 0 0!important;font-size:12px;color:var(--mut)}.from-list{margin:2px 0 0;padding-left:16px;font-size:13px}
.q-w{font-size:13.5px}.rp-title{font-weight:600}.rp-title a{color:inherit}.rp-text{font-size:14px}
.rp-thumb{display:block;margin:6px 0}.rp-thumb img{display:block;width:100%;max-height:200px;object-fit:contain;object-position:left top;border:1px dashed var(--line);border-radius:6px;background:#fff}
.rp-tags{color:var(--mut);font-size:12.5px}
#frame-pop{width:min(1300px,95vw);height:90vh;max-width:95vw;max-height:90vh;padding:0;border:0;border-radius:12px;background:var(--bg);color:var(--fg);overflow:hidden}
#frame-pop::backdrop{background:rgba(0,0,0,.35)}#frame-pop[open]{display:flex;flex-direction:column}
.pop-bar{display:flex;align-items:center;gap:12px;padding:8px 14px;border-bottom:1px solid var(--line)}
.pop-title{font-weight:650;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pop-x{border:0;background:transparent;font-size:20px;cursor:pointer;color:var(--fg)}.pop-frame{flex:1;border:0;width:100%;background:#fff}
@media(max-width:600px){body{padding:12px}.row{flex-wrap:nowrap;overflow-x:auto}.q-row{grid-template-columns:1fr}.q-row>div+div{border-left:0;border-top:1px solid var(--line)}.q-head-row{display:none}}
"""

# Idea Studio: a topic's canvas loads when its row opens; Edit switches that canvas to the editor in
# place; #topic-<name> in the address opens that row (the Audience Report links here).
STUDIO_JS = """
(function(){function load(d){var f=d.querySelector('iframe');if(d.open&&f&&!f.getAttribute('src'))f.src=f.dataset.src;}
document.querySelectorAll('details.topic').forEach(function(d){d.addEventListener('toggle',function(){load(d);});});
document.querySelectorAll('details.topic .draw-edit').forEach(function(b){b.addEventListener('click',function(ev){
  ev.preventDefault();ev.stopPropagation();          // in the row's header: edit, never fold
  var d=b.closest('details'),f=d.querySelector('iframe'),on=b.textContent==='Edit';
  d.open=true;f.src=on?f.dataset.edit:f.dataset.src;b.textContent=on?'Finish editing':'Edit';});});
var h=decodeURIComponent(location.hash.slice(1)),t=h&&document.getElementById(h);
if(t&&t.tagName==='DETAILS'){t.open=true;load(t);t.scrollIntoView({block:'start'});}})();
"""

# The pop-out (Insight's pop box, as the old boards had it): any [data-pop] link opens in it.
POP_HTML = ('<dialog id=frame-pop aria-label="Pop-out"><div class=pop-bar><span class=pop-title id=frame-pop-title>Pop-out</span>'
            '<a id=frame-pop-new target=_blank rel=noopener>Open in its own tab ↗</a>'
            '<button type=button class=pop-x id=frame-pop-x aria-label=Close>×</button></div>'
            '<iframe class=pop-frame id=frame-pop-frame title="Pop-out"></iframe></dialog>')
# A page the frame shows inside a Space (a Page view, an older theme page) keeps only its content: its own
# top (the title, back link and band in <body>'s <header>, its tab row in <body>'s <nav>, a bare <h1>) is
# hidden, so the frame's top is the only one (b03 s32-D14, JL 261008: "update all of them"). Same-origin
# pages only; a page that already drops its top for embed=1 is left as it is.
EMBED_JS = """
(function(){
  var CSS='html.wb-embed body>header,html.wb-embed body>nav,html.wb-embed body>h1,html.wb-embed .wb-band,'
   +'html.wb-embed .wb-links{display:none!important}html.wb-embed body{padding-top:4px}';
  function tidy(f){try{var d=f.contentDocument;if(!d||!d.documentElement)return;
    var h=d.documentElement;if(h.classList.contains('wb-embed-top'))return;h.classList.add('wb-embed','wb-embed-top');
    var st=d.createElement('style');st.textContent=CSS;(d.head||h).appendChild(st);}catch(e){}}
  function hook(f){f.addEventListener('load',function(){tidy(f);});tidy(f);}
  document.querySelectorAll('iframe.page-view,iframe.space-frame').forEach(hook);
  new MutationObserver(function(ms){ms.forEach(function(m){m.addedNodes.forEach(function(n){
    if(n.nodeType!==1)return;(n.matches('iframe.page-view,iframe.space-frame')?[n]:
      [].slice.call(n.querySelectorAll('iframe.page-view,iframe.space-frame'))).forEach(hook);});});})
   .observe(document.body,{childList:true,subtree:true});
})();
"""

# The Guide opens under the page's title, not above it, and the title reads "<theme> · Guide" while it is open
# (JL 261008: "seems we have issues in the guide"): the Guide's mount puts its frame after the level row
GUIDE_TITLE_JS = """
document.addEventListener('DOMContentLoaded',function(){
  var f=document.getElementById('wb-guide-frame'),hd=document.querySelector('header.page-title'),h=hd&&hd.querySelector('h1');
  if(!f||!hd||!h)return;hd.after(f);var own=h.innerHTML,g=h.getAttribute('data-guide');
  function sync(){var open=document.body.classList.contains('wb-guide-open');
    if(open&&h.textContent!==g)h.textContent=g;else if(!open&&h.innerHTML!==own)h.innerHTML=own;}
  new MutationObserver(sync).observe(document.body,{attributes:true,attributeFilter:['class']});sync();
});
"""

POP_JS = """
(function(){var dlg=document.getElementById('frame-pop'),fr=document.getElementById('frame-pop-frame');if(!dlg)return;
document.addEventListener('click',function(ev){var a=ev.target.closest('a[data-pop]');
  if(!a||ev.ctrlKey||ev.metaKey||ev.shiftKey||ev.altKey||!dlg.showModal)return;ev.preventDefault();
  document.getElementById('frame-pop-title').textContent=a.dataset.pop;document.getElementById('frame-pop-new').href=a.href;
  // Excalidraw refuses a same-site embed: a drawing opens with no referrer, as the folds do
  fr.referrerPolicy=new URL(a.href,location.href).pathname.indexOf('/_excalidraw/')===0?'no-referrer':'';
  fr.src=a.href;dlg.showModal();});
document.getElementById('frame-pop-x').addEventListener('click',function(){dlg.close();});
dlg.addEventListener('click',function(ev){if(ev.target===dlg)dlg.close();});
dlg.addEventListener('close',function(){fr.removeAttribute('src');});})();
"""


def href(folder: Path, root: Path, theme: Theme, space: str = "", sub: str = "") -> str:
    query = {"path": _rel(folder, root)}
    if theme.name != "vanilla":
        query["theme"] = theme.name
    if space:
        query["space"] = space
    if sub:
        query["sub"] = sub
    return ROUTE + "?" + urlencode(query)


def _level_row(theme: Theme, root: Path, folder: Path, level: str, space: str) -> str:
    """Guide (mounted by the Guide) · Block · Job ▾ · Task ▾: a level with siblings is a dropdown."""
    up = chain(folder, root)
    parts = []
    for lv in theme.levels:
        name = theme.level_name(lv)
        here = up.get(lv)
        on = " on" if lv == level else ""
        if lv == "Block":
            if here:
                parts.append(f'<a class="tab{on}" href="{_e(href(here, root, theme, space))}">{_e(name)}</a>')
            continue
        parent = up.get({"Job": "Block", "Task": "Job"}[lv])
        options = children(parent, {"Job": "Block", "Task": "Job"}[lv]) if parent else []
        if not options:                          # the tab stays, greyed, so every page has the same row
            if theme.hide_empty_levels:
                continue
            parts.append(f'<select disabled aria-label="{_e(name)}"><option>{_e(name)} ▾</option></select>')
            continue
        if here and lv != level:
            # below this level (a Task under its Job): the open item is a button that goes up to its tab, and a
            # ▾ beside it switches to a sibling; a dropdown alone ignores a click on the item already picked
            # (JL 261008: "I want to click the job button at the top, but it is not react")
            parts.append(f'<span class=lvl><a class=tab href="{_e(href(here, root, theme, space))}" title="{_e(here.name)}">'
                         f'{_e(_label(theme, here))}</a><select aria-label="Switch {_e(name)}" '
                         f'onchange="if(this.value)location.href=this.value"><option value="" selected>▾</option>'
                         f'{_options(theme, root, space, options, None)}</select></span>')
            continue
        opts = _options(theme, root, space, options, here)
        pick = "" if here else f'<option value="" selected>{_e(name)} ▾</option>'
        parts.append(f'<select class="{on.strip()}" aria-label="{_e(name)}" '
                     f'onchange="if(this.value)location.href=this.value">{pick}{opts}</select>')
    return '<nav class="row levels">' + "".join(parts) + "</nav>"


def short_name(name: str, most: int = 26) -> str:
    """A folder's short name for the Job ▾ / Task ▾ dropdown (b03 s32-D13): its tag and its parts' ids
    (j04_g01-<goal>_m04-<method> -> j04 · g01 · m04), or its tag and first words (j11_fit_the_model ->
    j11 · fit the model); a name without a tag stays as it is."""
    m = _PREFIXED.match(name)
    if not m:
        return name
    tag, rest = name.split("_", 1)
    ids = re.findall(r"(?:^|_)([a-z]\d{2,})(?=-|_|$)", rest)
    if ids and re.fullmatch(r"(?:[a-z]\d{2,}(?:-[^_]*)?_?)+", rest):
        return " · ".join([tag] + ids)
    words = rest.replace("_", " ").replace("-", " ")
    return f"{tag} · " + (words if len(words) <= most else words[:most].rsplit(" ", 1)[0] + " …")


def _label(theme: Theme, folder: Path) -> str:
    """A folder's label in the level row: the theme's, else its short name."""
    got = None
    if theme.option:
        try:
            got = theme.option(folder)
        except Exception:                        # a theme's label must not break the frame
            got = None
    return got[0] if got else short_name(folder.name)


def _options(theme: Theme, root: Path, space: str, options: list, here) -> str:
    """The dropdown's options: each folder's name, or the theme's label for it; the theme's groups as
    <optgroup>s, in the order they first come."""
    groups: dict = {}
    for o in options:
        got = None
        if theme.option:
            try:
                got = theme.option(o)
            except Exception:                    # a theme's label must not break the frame
                got = None
        label, group = got if got else (short_name(o.name), "")
        groups.setdefault(group or "", []).append(
            f'<option value="{_e(href(o, root, theme, space))}" title="{_e(o.name)}"'
            f'{" selected" if o == here else ""}>{_e(label)}</option>')
    return "".join("".join(opts) if not g else f'<optgroup label="{_e(g)}">{"".join(opts)}</optgroup>'
                   for g, opts in groups.items())


def _spaces_row(theme, root, folder, space) -> str:
    out, last = [], None
    for name, group, optional in SPACES:
        if last is not None and group != last:
            out.append('<span class=bar></span>')
        last = group
        cls = "tab" + (" on" if name == space else "") + (" opt" if optional else "")
        out.append(f'<a class="{cls}" href="{_e(href(folder, root, theme, name))}">{_e(name)}</a>')
    return '<nav class="row spaces">' + "".join(out) + "</nav>"


def _subs_row(theme, root, folder, space, view: Space) -> str:
    if not view.subspaces:
        return ""
    return ('<nav class="row subs">' + "".join(
        f'<a class="tab{" on" if s == view.open else ""}" href="{_e(href(folder, root, theme, space, s))}">{_e(s)}</a>'
        for s in view.subspaces) + "</nav>")


def render(theme: Theme, root: Path, folder: Path, space: str = "", sub: str = "") -> str:
    """The whole page for one folder: its level's tabs, the six Spaces, the open Space."""
    from live.runs_panel import PANEL_CSS, PANEL_JS, SPLIT_CSS, panel_markup
    from live.space_views import SPACE_VIEW_CSS
    from live.work_items import WORK_ITEM_CSS
    from live.workbench_guide import mount_guide

    root, folder = root.resolve(), folder.resolve()
    level = level_of(folder) or "Block"
    space = space if space in SPACE_NAMES else "Description"
    views = spaces_for(theme, level, folder, root, sub)
    view = views[space]
    rel = _rel(folder, root)
    kinds = [dict(k, prompt=k.get("prompt", "").replace("{folder}", rel)) for k in view.run_types]
    panel = panel_markup(space, kinds, [list(k.get("rows") or []) for k in kinds], base=root, fill=lambda row: {"page": rel, "folder": rel},
                         whole=f"this {theme.level_name(level)}",
                         extra=f'<p class=mut style="margin:6px 0">{_e(view.note)}</p>' if view.note else "",
                         top=disk_markup(view.disk, folder, root),   # Disk folds with the Runs (JL 261007)
                         title="Disk · Runs" if view.disk else "Runs", compact=True)
    md = face(folder)
    title = f"{theme.icon} {theme.label} · {folder.name}"     # the browser tab: the full folder name
    # the page's own title, under the level row (b03 s32-D13, JL 261008: "make the first line like the
    # page index and the second line to be the title of the webpage"): the theme, the level and its tag,
    # then the folder's own title (its face's heading)
    m = _PREFIXED.match(folder.name)
    tag = folder.name.split("_", 1)[0] if m else ""
    named = _title(md) if md else folder.name
    if tag and named != folder.name:            # a heading that starts with its own tag: said once
        named = re.sub(rf"^{re.escape(tag)}\b\s*[·:\-–]?\s*", "", named, flags=re.I) or named
    lead = f"{theme.level_name(level)} {tag}".strip()
    heading = (f'{_e(theme.icon)} {_e(theme.label)} · <span class=lv>{_e(lead)} ·</span> {_e(named)}'
               if named != folder.name or tag else f'{_e(theme.icon)} {_e(theme.label)} · {_e(named)}')
    # no band line (JL 261007: "why I still have this? please remove that"): the level tabs say where
    # you are; the folder's path stays one hover away, on the title
    where = f"{theme.level_name(level)} · {rel} · " + (f"{theme.label} theme" if theme.name != "vanilla" else "vanilla")
    document = ('<!doctype html><html lang=en><head><meta charset=utf-8>'
                '<meta name=viewport content="width=device-width,initial-scale=1">'
                f'<title>{_e(title)}</title><link rel="icon" href="data:,">'
                # the base's shared view styles, which a theme's Spaces may use; never a theme's own
                # (b03, JL 261007: "base styles only": a theme carries no look of its own)
                f'<style>{CSS}{PANEL_CSS}{SPLIT_CSS}{SPACE_VIEW_CSS}{WORK_ITEM_CSS}{DISK_CSS}</style></head><body><main>'
                + _level_row(theme, root, folder, level, space)
                + f'<header class=page-title><h1 title="{_e(where)} · {_e(folder.name)}" '
                  f'data-guide="{_e(theme.icon)} {_e(theme.label)} · Guide">{heading}</h1></header>'
                + '<section class="frame-body">'          # the Guide replaces all of this while it is open
                + _spaces_row(theme, root, folder, space)
                + _subs_row(theme, root, folder, space, view)
                + f'<div class=split><div class=space-main>{view.html}</div>'
                  f'{panel}</div></section>'
                f'{POP_HTML}</main><script>{PANEL_JS}{STUDIO_JS}{POP_JS}{EMBED_JS}{GUIDE_TITLE_JS}</script></body></html>')
    # as every workbench mounts it: the face's SPACE-relative path, and its file name
    # `level`: the Guide opens this level's section and folds the other two (b03 s31-D07)
    context = {"path": _rel(md, root) if md else rel, "file": md.name if md else "", "level": level}
    return mount_guide(document, theme.guide, context, "nav.levels", ".frame-body")


def themes() -> dict:
    """{name: Theme} from every workbench folder that has a `<name>_theme.py` exporting THEME."""
    import importlib
    from host_registry import workbench_folders, workbench_name
    found = {"vanilla": VANILLA}
    for folder in workbench_folders():
        name = workbench_name(folder)
        if (folder / f"{name}_theme.py").is_file():
            try:
                found[name] = importlib.import_module(f"live.{name}_theme").THEME
            except Exception:                    # a broken theme falls back to vanilla, never the page
                continue
    return found


# ── a Page Task on the frame (b03 s13-task-variants, b16 s13-paper-task; 261007) ───────────────────
# A Task that is a Page (its face is a Page under its Block, as a paper Section is) shows the Page's own
# views in the six Spaces. Each view is the Page itself, embedded (`/_board/draft?…&embed=1`, task-page/
# outline.py EMBED_HTML), so its tables, Scratch and Revise work exactly as in the Page workbench. A theme
# whose Tasks are Pages returns page_task_spaces(...) from its spaces() at Task level, and adds its own.
PAGE_TASK_SUBS = {
    "Description": ("Scope", "Plan", "Requirement", "Records"),
    "Audience Report": ("Table", "Reading", "Questions"),
    "Work Details": ("Draft-Scratch", "Draft-Revise", "Evidence-Citation", "Evidence-Display",
                     "Evidence-Value", "Evidence-Supporting"),
    "Runs": (),                # no third row: the Page's own Runs view, by lane, a card per Run (b16 s13)
    "Delivery": (),            # no third row: one card per kind of delivery, its result embedded
}
# a Work Details or Delivery view -> its run cards, by label, from the Page's run-cards.md (b16 s13
# Decided 5, JL 261007): the Audience Report is for reading, so Table and Reading carry none; the
# Runs in Work Details change the content. A card not in run-cards.md yet is left out.
PAGE_TASK_RUNS = {
    "Draft-Scratch": ("Scratch", "Structure revise", "Evidence embed"),
    "Draft-Revise": ("Section revise", "Paragraph revise", "Revise edits", "Auto write"),
    "Evidence-Citation": ("Bind / update citation",), "Evidence-Display": ("Build figure / table",),
    "Evidence-Value": ("Bind / update value",), "Evidence-Supporting": ("Task runs", "Discovery runs"),
    "Delivery": ("Build", "Check"),
}
# a Page run card -> the Run it makes (JL 261007: buttons named by their Runs; the Page skills' own
# names: haipipe-page-scratch · -structure · -writing · -revise · -evidence, haipipe-display); the two
# Supporting kinds are hard Runs of other Tasks
PAGE_RUN_NAMES = {"Scratch": "run-scratch-<target>", "Structure revise": "run-structure-<slug>",
                  "Evidence embed": "run-<value|display|citation>-<slug>", "Section revise": "run-section-<slug>",
                  "Paragraph revise": "run-paragraph-<slug>", "Revise edits": "run-revise-<target>",
                  "Auto write": "run-section-<slug>", "Bind / update citation": "run-citation-<slug>",
                  "Build figure / table": "run-display-<slug>", "Bind / update value": "run-value-<slug>",
                  "Task runs": "rNN_<slug> (a work Task)", "Discovery runs": "rNN_<author><year>_<subject>",
                  "Build": "run-delivery-<target>", "Check": "run-check-<page>"}
PAGE_QUESTION_RUNS = (
    {"label": "run-ask-<qNN>", "doing": "ask a question",
     "prompt": "Ask a new question of {folder}: its ## Questions row and reports/qNN_<topic>/.",
     "skills": ["haipipe-question"]},
    {"label": "run-report-<qNN>", "doing": "write the report",
     "prompt": "Write or update a question's report in {folder}/reports/qNN_<topic>/: "
               "Answer · Evidence · Limits · Next, and what it changed in the draft.",
     "skills": ["haipipe-report"]})
RUBRIC = Path(__file__).resolve().parents[2] / "skills/1_base/writing/haipipe-writing/ref/evaluation-rubric.md"
# a subspace -> the Page's (Space, Draft view, tab) it opens embedded
PAGE_TASK_VIEWS = {
    "Table": ("bullet", "table", ""), "Reading": ("bullet", "reading", ""),
    "Draft-Scratch": ("bullet", "scratch", ""), "Draft-Revise": ("bullet", "revise", ""),
    "Evidence-Citation": ("evidence", "", "citations"), "Evidence-Display": ("evidence", "", "displays"),
    "Evidence-Value": ("evidence", "", "values"), "Evidence-Supporting": ("evidence", "", "supporting"),
}


def page_view_url(folder: Path, root: Path, sub: str) -> str:
    """The Page workbench's address for one of its views, embedded: path= the Block's face, file= the
    Task's face from the Block, as every Page link of a Board has it."""
    block, md = chain(folder, root).get("Block"), face(folder)
    if not block or not md or not face(block):
        return ""
    space, mode, tab = PAGE_TASK_VIEWS[sub]
    query = {"path": _rel(face(block), root), "file": md.relative_to(block).as_posix(), "embed": "1",
             "space": space, **({"view": mode} if mode else {}), **({"tab": tab} if tab else {})}
    return "/_board/draft?" + urlencode(query)


def _page_runs(sub: str) -> tuple:
    """The run cards of one Page view, as Runs-panel kinds; none for a view with no cards."""
    try:
        from live.runs_panel import run_types
        cards = {c["label"]: c for c in run_types()}
    except Exception:                               # no run cards: the view still opens
        return ()
    def skills(value):                              # run-cards.md gives a list, or "a · b"
        items = value if isinstance(value, (list, tuple)) else str(value or "").split("·")
        return [str(x).strip() for x in items if str(x).strip()]
    return tuple({"label": PAGE_RUN_NAMES.get(c["label"], c["label"]), "doing": c["label"].lower(),
                  "prompt": c["prompt"], "skills": skills(c.get("skills"))}
                 for c in (cards.get(label) for label in PAGE_TASK_RUNS.get(sub, ())) if c)


def _rubric(root: Path) -> str:
    """The shared prose rubric the draft is judged by (haipipe-writing base-v1), folded."""
    if not RUBRIC.is_file():
        return ""
    inside = root.resolve() in RUBRIC.parents                  # a reader link only for a file the root serves
    body = (_source(RUBRIC, root, "") if inside else
            f'<pre class=space-source>{_e(RUBRIC.read_text(encoding="utf-8", errors="replace"))}</pre>')
    return (f'<details class=topic><summary><b>Rubric · Mechanics · Function · Evidence · Readability</b>'
            f'<span class=topic-meta>the four axes the draft is judged by</span></summary>'
            f'<div style="padding:8px 14px">{body}</div></details>')


def _source(path: Path | None, root: Path, empty: str) -> str:
    """A Markdown file shown as it is, with a link to the Page reader; or why there is none."""
    if not path or not path.is_file():
        return f'<p class=space-empty>{_e(empty)}</p>'
    return (f'<p class=space-reads>{pop(_reader(path, root), path.name, _rel(path, root) + " ↗")}</p>'
            f'<pre class=space-source>{_e(path.read_text(encoding="utf-8", errors="replace"))}</pre>')


LANE_ICON = {"web": "🌐", "latex": "📄", "word": "📝", "slide": "🖥", "render": "🖼"}


def _delivery_cards(folder: Path, root: Path, md: Path | None) -> str:
    """Delivery (JL 261007: "each card is a type of delivery … the card and the preview of the results,
    the embedded content", as the old paper page's Preview did): one card per kind of delivery, from
    the Page's own read-only check (task-page/delivery.py check_delivery). Its head: the kind, its
    state (current · stale · not built), its files as ↗ links; its body: the result embedded (the web
    page, the PDF, Word through the PDF twin the build writes beside the .docx, the deck), a LaTeX
    piece with no PDF yet shown as it is, or "not built yet: run Build"."""
    stem = md.stem if md else folder.name
    try:
        from live.delivery import check_delivery
        lanes = check_delivery(md).get("lanes", []) if md else []
    except Exception:                               # no Page engine: no cards, never no page
        lanes = []
    url = lambda f: "/" + quote(_rel(f, root))
    cards = []
    for lane in lanes:
        key = lane.get("lane", "")
        ldir = folder / "delivery" / key
        files = sorted(f for f in ldir.rglob("*") if f.is_file() and not f.name.startswith(".")) if ldir.is_dir() else []
        state = lane.get("state", "")
        mark = {"pass": "st-ok", "stale": "st-warn"}.get(state, "mut")
        word = {"pass": "current", "stale": "stale", "not-built": "not built"}.get(state, state)
        show = {"web": [ldir / "index.html"], "latex": [ldir / f"{stem}.pdf"], "word": [ldir / f"{stem}.pdf"],
                "slide": [ldir / f"{stem}-deck.html"]}.get(key, [f for f in files if f.suffix in (".pdf", ".html")][:1])
        shown = next((f for f in show if f.is_file()), None)
        links = " · ".join(pop(url(f), f.name, f.relative_to(ldir).as_posix()) for f in files)
        head = (f'<div class=st-bar><span><b>{LANE_ICON.get(key, "")} {_e(lane.get("label", key))}</b> '
                f'<span class={mark}>{_e(word)}</span></span><span class=mut>{links}</span></div>')
        if shown:
            body = f'<iframe class=dl-frame loading=lazy title="{_e(shown.name)}" src="{_e(url(shown))}"></iframe>'
        elif key == "latex" and (ldir / f"{stem}.tex").is_file():     # no PDF compiled yet: the piece itself
            body = (f'<p class="mut dl-note">{_e(stem)}.pdf is not compiled yet; the piece:</p>'
                    f'<pre class="space-source dl-src">{_e((ldir / f"{stem}.tex").read_text(encoding="utf-8", errors="replace"))}</pre>')
        elif files:
            body = '<p class="mut dl-note">built; no preview for this kind yet</p>'
        else:
            body = '<p class="mut dl-note">not built yet: run Build</p>'
        cards.append(f'<div class=topic>{head}{body}</div>')
    return ("<h2>Deliveries</h2>" + "".join(cards) if cards else
            '<p class=space-empty>Nothing built yet: delivery/ holds no files. Run Build.</p>')


def page_task_spaces(folder: Path, root: Path, sub: str = "") -> dict:
    """{Space: Space} for a Page Task: Description is Scope (its face) · Plan · Requirement · Records;
    Audience Report, Work Details and Delivery each open the Page's own view, embedded. Idea Studio
    and Runs are the vanilla defaults."""
    folder, root = folder.resolve(), root.resolve()
    md = face(folder)
    out = {}
    for space, subs in PAGE_TASK_SUBS.items():
        if space == "Runs":                             # the Page Runs view, embedded (JL 261007: "is this
            block = chain(folder, root).get("Block")    # a table what what?"): lanes, counts, a card per Run
            src = ("/_board/runs?" + urlencode({"path": _rel(face(block), root), "file": md.relative_to(block).as_posix(),
                                                "embed": "1"}) if block and md and face(block) else "")
            out[space] = Space(html=(f'<iframe class=space-frame title="Runs" src="{_e(src)}"></iframe>' if src else
                                     '<p class=space-empty>This Task has no face under a Block, so it shows no Page Runs.</p>'),
                               run_types=(RUN_ANY,), page=True)
            continue
        if space == "Delivery":                         # no third row: item cards, Build · Check
            out[space] = Space(html=_delivery_cards(folder, root, md), run_types=_page_runs("Delivery"), page=True)
            continue
        opened = sub if sub in subs else subs[0]
        if space == "Description":
            if opened == "Scope":
                body = ""                               # the vanilla Description: the face and its fields
            elif opened == "Plan":
                try:
                    from src.outline_version import latest_outline, plan_dir
                    plan = latest_outline(plan_dir(folder), md.stem) if md else None
                except Exception:                       # no Page engine: say so, never break the frame
                    plan = None
                body = _source(plan, root, "No plan yet: the Page's plan is written by its Structure Run.")
            elif opened == "Requirement":                # its V (venue) and W (own) rules, then the rubric
                req = folder / "draft" / "records" / f"{md.stem if md else folder.name}-requirement.md"
                body = (_source(req, root, "No requirement record yet (draft/records/<stem>-requirement.md).")
                        + _rubric(root))
            else:
                recs = sorted((folder / "draft" / "records").glob("*.md")) if (folder / "draft" / "records").is_dir() else []
                body = (_table(("record", "bytes"), [(pop(_reader(r, root), r.name, r.name + " ↗"), _e(r.stat().st_size))
                                                     for r in recs]) if recs else
                        '<p class=space-empty>No records yet (draft/records/).</p>')
            out[space] = Space(html=body, subspaces=subs, open=opened, page=True, run_types=(
                {"label": f"run-face-{folder.name.split('_', 1)[0]}", "doing": "update the description",
                 "prompt": "Update the face of {folder}.", "skills": [LEVEL_SKILL["Task"]]},))
            continue
        if opened == "Questions":                   # the Section's questions, Question │ Work │ Report
            rows, _ = question_rows("Task", folder, root)
            out[space] = Space(html=rows, subspaces=subs, open=opened, run_types=PAGE_QUESTION_RUNS, page=True)
            continue
        url = page_view_url(folder, root, opened)
        body = (f'<iframe class=space-frame title="{_e(opened)}" src="{_e(url)}"></iframe>' if url else
                '<p class=space-empty>This Task has no face under a Block, so it opens no Page view.</p>')
        # no read-only note in the Runs panel (JL 261008: "we don't need to add these details")
        out[space] = Space(html=body, subspaces=subs, open=opened, run_types=_page_runs(opened), page=True)
    return out


# ── what the Guide's Space cards read live (b03 s31-D06): each level's sub · runs, from here ─────
def theme_for_guide(family: str) -> Theme:
    """The theme whose Guide family this is (its `guide`, or its own name), else vanilla."""
    for theme in themes().values():
        if family in (theme.guide, theme.name):
            return theme
    return VANILLA


def level_folders(folder: Path, root: Path) -> dict:
    """{level: folder} for the open folder's ladder: its own chain upward, then the first child of
    each level below it (a Block's first Job and that Job's first Task). A level with no folder is
    left out."""
    folder = folder.resolve()
    found = dict(chain(folder, root.resolve()))
    for parent, below in (("Block", "Job"), ("Job", "Task")):
        if below not in found and parent in found:
            kids = children(found[parent], parent)
            if kids:
                found[below] = kids[0]
    return found


def space_cards(theme: Theme, level: str, folder: Path | None, root: Path) -> list:
    """[(Space, subspaces, run type labels)] of one level, as its tabs show them: the base, then the
    theme (spaces_for). With no folder at that level, the theme's defaults: the same call over a
    folder that does not exist, so nothing on disk is read."""
    root = root.resolve()
    at = folder.resolve() if folder else root / f".no-{level.lower()}"
    views = spaces_for(theme, level, at, root)
    return [(name, tuple(views[name].subspaces), [k["label"] for k in views[name].run_types])
            for name in SPACE_NAMES]


def frame_json(theme: Theme, root: Path, folder: Path, sub: str = "") -> str:
    """The same frame as data: levels, Spaces and each Space's subspaces and run types (for tests
    and for a theme checking what it fills)."""
    level = level_of(folder.resolve()) or "Block"
    views = spaces_for(theme, level, folder.resolve(), root.resolve(), sub)
    return json.dumps({"theme": theme.name, "level": level, "levels": list(theme.levels),
                       "spaces": [{"name": n, "group": g, "optional": o, "subspaces": list(views[n].subspaces),
                                   "open": views[n].open, "run_types": [k["label"] for k in views[n].run_types],
                                   "run_doing": [k.get("doing") or k["label"] for k in views[n].run_types]}
                                  for n, g, o in SPACES]}, ensure_ascii=False)
