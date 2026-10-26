"""The base frame every theme draws in, and the vanilla workbench when no theme is laid over it.

    Guide · Studio | Block · Job ▾ · Task ▾ | Delivery                top navigation
    Description | Report | Work | Runs                             work mode only
    <subspaces>                                                           the third row
    content                                                  │ Runs panel

Studio and Delivery are the Block's shared views (b10 s09-D05): one Studio and one delivery/ per
Block, opened from every level; Delivery at a Job or Task shows that level's part. Related, the
Block's related/ (what came in), folds inside the Studio, under its topic cards (b10 s04 Open 1,
JL 261011: "put the related as the second collapse part in the box of the studio items"); the Block's
delivery/ (what went out) folds under Related, every result previewed (JL 261014).
The frame owns the levels, shared Guide, Studio (with Related) and Delivery, the work Spaces, their order and
dividers, the third row, the Runs panel and the look (Tools/blueprints/b10_project_workbench, Q08 and studio/s02-studio-workbench-skill). A theme
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

from src.common import delivery_dir, delivery_owner, delivery_relative
import datetime
import html
import os
import json
import re
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Callable
from urllib.parse import quote, urlencode

LEVELS = ("Block", "Job", "Task")
# (Space, divider group, optional): the bars in the Spaces row fall between groups
SPACES = (("Description", 0, False), ("Related", 1, True), ("Idea Studio", 1, True), ("Audience Report", 1, True),
          ("Work Details", 2, False), ("Runs", 3, False), ("Delivery", 3, True))
# the Block's shared views: each has its one entry in the top row, never in the Spaces row
TOP_ROW = ("Idea Studio", "Delivery")
# shown inside the Studio, under its topic cards, never in a row (b10 s04, JL 261011)
IN_STUDIO = ("Related",)
SPACE_NAMES = tuple(name for name, _, _ in SPACES)
# what a Space button says; the key stays, so old space= links keep working
# (s02-D10 Report; s02-D19 Work, JL 261010: "change the Work Details into Work")
SPACE_LABELS = {"Audience Report": "Report", "Work Details": "Work"}
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
LEVEL_SKILL = {"Block": "haipipe-block", "Job": "haipipe-job", "Task": "haipipe-task"}


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
    page: bool = False         # laid out by a Task type's spaces (workbench-task-<type>/; a theme that extends it keeps the mark)
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
    # the Report's groups (b10 s05, JL 261011: "for someother report, the groups are of the special forms,
    # and that ones are fixed, depending on different theme"): report_fixed(row, owner) -> the groups a
    # register row has by the theme's own rule, shown with no × (a paper's from its telling's **Feeds:**, so it
    # gets the owner folder; insight's level letter needs only the row, and report_fixed(row) works too);
    # report_groups, the groups its bar shows from the start, even empty; report_cards(level, folder, root)
    # -> [{id, title, groups, status, html}], the theme's own cards that are no register row (a paper's ideas
    # and its standing Questions, s05-D09, D12), drawn beside the register's, not draggable, their groups
    # fixed. Every other group is a tag, made and added as on a Studio topic.
    report_fixed: Callable | None = None
    report_groups: tuple = ()
    report_cards: Callable | None = None
    # task_action(task, root) -> (label, href) for a Task a person works inside (a labeling Task's rounds), or
    # None; the Work tree gives it its button and a mark (b10 s32, JL 261012: "there are special tasks that human
    # need to interact with"). A Task a person writes (its face's `task-type: draft`) needs no hook: the base opens its Draft.
    task_action: Callable | None = None
    # work_meta(folder, root) -> html: the theme's own words on a Job's or Task's card in the Work tree (a cowork
    # Job's state and who it waits on, a design's verdict), after the base's title and counts; "" for none
    work_meta: Callable | None = None
    # work_body(folder, root) -> html: what an opened Job card shows below its Tasks (a cowork Job's timeline of
    # emails, meetings and steps, which are its work); "" for none
    work_body: Callable | None = None
    # delivery_fixed(item) -> (groups, order): a Delivery result's groups by the theme's rule, shown with no ×, and
    # its place in the list (a paper's whole build, then its Main, Appendix and Letters Sections in reading order;
    # JL 261014: "there should be groups for the section-task group"); None keeps the base's newest-first list
    delivery_fixed: Callable | None = None

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
                  and folder.resolve() in p.resolve().parents and level_of(p) == want)


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


def _fields(md: Path, keys=("board-kind", "spine", "goal", "state", "close", "answers", "answer-status",   # answers:
                            "status")) -> list:                                    # the Job contract's fourth field
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


def vanilla(level: str, folder: Path, root: Path, sub: str = "", theme: "Theme | None" = None) -> dict:
    """{Space: Space}: what every Space shows when no theme fills it; `theme` lends the Report its fixed and
    starting groups (Theme.report_fixed, report_groups)."""
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

    # Related is the Block's (spaces_for gives a Job or Task its Block's)
    out["Related"] = related_view(folder, root, sub) if level == "Block" else Space()
    out["Idea Studio"] = Space(studio_cards(folder, root), run_types=(
        run_type("run-draw-<sNN>", "add a topic · redraw it · save this session, each a pass",
                 "/haipipe-studio a topic of {folder}: new topic → studio/sNN-<topic>/ and runs/run-draw-<sNN>/; "
                 "redraw or this session → a pass of run-draw-<sNN>.", "haipipe-studio",
                 rows=studio_sessions(folder, root)),))

    # the Report: one card per Question under the Studio's group bar (b10 s05, JL 261011: "if the report card to
    # show, it will be the same as the sNN, we can create and add the tags"); the paper Board's four buttons,
    # once drawn on every theme (AUDIENCE_VIEWS, 261009), stay the paper theme's own
    page_row = ""
    if level == "Task" and md:                                   # a Task's report is its own face (s05-D10)
        runs = " · ".join(_e(r["run"]) for r in runs_of(folder)) or "<span class=mut>no Runs yet</span>"
        page_row = (f'<div class="q-row q-two"><div class=q-l><p class=q-head><b>the Page</b></p></div>'
                    f'<div class=q-r>{pop(_reader(md, root), "the Page", _title(md) + " ↗")}'
                    f'<p class=q-work><span class=mut>Work:</span> {runs}</p></div></div>')
    rows_html = report_view(level, folder, root, theme, empty=page_row)
    out["Audience Report"] = Space(rows_html, run_types=(
        run_type("run-ask-<qNN>", "ask a Question", "Ask a new Question of {folder}: its register row and "
                 "reports/qNN_<topic>/.", "haipipe-report"),
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
        # Job → Task → Run → what it found, one tree (b10 s32, JL 261012); the old table when there is none
        out["Work Details"] = Space(work_tree(level, folder, root, theme) or
                                    _table(("Job" if level == "Block" else "Task", "title",
                                            "Tasks" if level == "Block" else "Runs"), rows),
                                    run_types=(run_type("run-add-<jNN>" if level == "Block" else "run-add-<tNN>",
                                                        "add a " + ("Job" if level == "Block" else "Task"),
                                                        "Add a " + ("Job" if level == "Block" else "Task") + " to {folder}.",
                                                        LEVEL_SKILL.get(level, LEVEL_SKILL["Task"])),))
    else:
        rows = [(_e(p.name + "/"), _e(sum(1 for _ in p.rglob("*") if _.is_file())))
                for p in sorted(folder.iterdir()) if p.is_dir() and not p.name.startswith((".", "_"))
                and p.name not in ("runs", "studio", "reports", "delivery")] if folder.is_dir() else []
        out["Work Details"] = Space(work_tree("Task", folder, root, theme) + "<h3>Folders</h3>"
                                    + _table(("folder", "files"), rows),
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

    deliv = delivery_dir(folder)
    rows = [(_e(p.name + ("/" if p.is_dir() else "")), _e(sum(1 for _ in p.rglob("*") if _.is_file()) if p.is_dir() else ""))
            for p in sorted(deliv.iterdir()) if not p.name.startswith(".")] if deliv.is_dir() else []
    out["Delivery"] = Space(delivery_view(folder, root, theme) or _table(("item", "files"), rows),
                            run_types=(run_type(f"run-delivery-{tag}", "build the delivery", "Build the delivery of {folder}.",
                                                LEVEL_SKILL.get(level, LEVEL_SKILL["Task"])),))
    for name, disk in vanilla_disk(level, md.name if md else folder.name + ".md").items():
        out[name] = replace(out[name], disk=disk)
    if level == "Block":
        old_sources = dict.fromkeys(source for source, _, _ in studio_inventory(folder, root) if source != folder.resolve())
        extra = tuple((source.relative_to(folder.resolve()).as_posix() + "/studio/s*/", "existing topics from " + short_name(source.name))
                      for source in old_sources)
        out["Idea Studio"] = replace(out["Idea Studio"], disk=out["Idea Studio"].disk + extra)
    from live.task_draft import with_page_views       # a Task with a Page face: its Page views (workbench-task-draft/)
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
                            ("reports/q*/q*.excalidraw", "Report: its drawing, live (click to pan and zoom)"),
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
        rel = Path(os.path.relpath(p, folder)).as_posix() if p != folder else "."
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
        found = [m for m in found if m.resolve().is_relative_to(root.resolve())
                 and (m.resolve().is_relative_to(folder.resolve())
                      or m.resolve().is_relative_to(delivery_dir(folder)))]
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


# ── Idea Studio: one closed row per studio topic, opened in place (b10 s02-D25, D27) ───────
# a topic's stage, its **Stage:** line (b10 s09-D03): a person moves it; the badge only shows it
STAGES = ("explore", "shaping", "agreed", "closed")   # in order; the badge fills one step per stage


def _note_facts(md: Path | None) -> dict:
    """What a topic's notes file says: its **Topic:** line, stage, decisions, open points, feeds."""
    if not md:
        return {"topic": "", "decided": 0, "open": 0, "feeds": [], "tags": [], "stage": ""}
    text = md.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"\*\*Topic:\*\*\s*(.+?)(?:\n\s*\n|\Z)", text, re.S)
    topic = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    opened = re.search(r"(?ims)^(?:#+\s*)?Open\b[^\n]*\n(?:[-=]{3,}\n)?(.*?)(?=^\S[^\n]*\n[-=]{3,}\n|^#+ |\Z)", text)
    feeds = re.search(r"\*\*Feeds:\*\*(.+?)(?:\n\s*\n|\Z)", text, re.S)
    tags = _split_tags(",".join(re.findall(r"(?mi)^\*\*(?:Tags|Type):\*\*[^\S\n]*([^\n]*)", text)))
    stage = re.search(r"(?mi)^\*\*Stage:\*\*[^\S\n]*`?([A-Za-z]+)", text)
    stage = stage.group(1).lower() if stage and stage.group(1).lower() in STAGES else ""
    return {"topic": topic, "tags": tags, "stage": stage,
            "decided": len(re.findall(r"(?m)^s\d+-D\d+\b", text)),
            "open": len(re.findall(r"(?m)^\d+\.\s", opened.group(1))) if opened else 0,
            # a report's folder name, q08_workbench_base, or its bare id, Q08 (b10 s05 Open 8: s32 wrote `Q08 (...)`)
            "feeds": list(dict.fromkeys(m.group(1) or m.group(2).lower() for m in
                                        re.finditer(r"\b(q\d\d_[A-Za-z0-9_]+)|\b([Qq]\d\d)\b", feeds.group(1))))
                     if feeds else []}


def _split_tags(line: str) -> list:
    """The groups on a **Tags:** line or in a related row's group cell: split at , · or |, backticks off,
    each name once whatever its case."""
    tags = []
    for value in re.split(r"[,·|]", line):
        value = value.strip().strip(chr(96)).strip()
        if value and value.casefold() not in {tag.casefold() for tag in tags}:
            tags.append(value)
    return tags


def _notes(topic: Path) -> Path | None:
    if not topic.is_dir():
        return None
    md = topic / (topic.name + ".md")
    return md if md.is_file() else next(iter(sorted(topic.glob("*.md"))), None)


def _draw_url(d: Path, root: Path, edit: bool = False) -> str:
    return "/_excalidraw/?" + urlencode({"board": _rel(d, root), **({"edit": "1"} if edit else {})})


def _report_page(name: str, folder: Path, root: Path) -> Path | None:
    """reports/<name>/<name>.md at this level or one above; a bare id (q08) finds its folder, q08_<topic>/."""
    for f in [folder] + list(chain(folder, root).values()):
        for d in [f / "reports" / name] if "_" in name else sorted((f / "reports").glob(f"{name.lower()}_*/")):
            page = d / (d.name + ".md")
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
    (b10 s02-D27), then the older `chat/` summaries until they move into passes."""
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


def _group_parts(key: str, name: str, tags: list, source: str = "", noun: str = "topic", fixed=()) -> tuple:
    """What a row needs under a group bar (b10 s02-D16), a Studio topic or a Related item alike: its data-
    attributes, the ⋮⋮ handle, the Add to Current button, and its group chips, each with × to take it out;
    a group in `fixed` (a related item's subfolder, a theme's own Report group) has no ×, since only moving the
    file, or the theme, changes it; `data-studio-fixed` keeps it so when the page redraws the chips."""
    fixed = {t.casefold() for t in fixed if t}
    attrs = (f' data-studio-key="{_e(key)}" data-studio-name="{_e(name)}" data-studio-source="{_e(source)}"'
             + (f' data-studio-fixed="{_e(json.dumps(sorted(fixed)))}"' if fixed else ""))
    handle = (f'<span class=studio-drag draggable=false title="Drag this {noun} onto a group"'
              f' aria-label="Drag this {noun} onto a group">⋮⋮</span>')
    current = '<button type=button class=studio-current aria-pressed=false>Add to Current</button>'
    chips = "".join(f'<span class=chip data-tag="{_e(tag)}">{_e(tag)}</span>' if tag.casefold() in fixed else
                    f'<span class=chip data-tag="{_e(tag)}">{_e(tag)}<button type=button class=tag-x title="Take '
                    f'out of {_e(tag)}" aria-label="Take {_e(name)} out of {_e(tag)}">×</button></span>' for tag in tags)
    return attrs, handle, current, f'<span class=topic-tags>{chips}</span>' if chips else ""


def _studio_transcripts(topic: Path, root: Path, topic_id: str) -> str:
    """A topic's transcript originals, read in place. The index names a local PDF (optionally a book
    chapter's page range), its source and raw text; source records and credentials are never served here.
    The PDF may sit anywhere in the topic's Block: the Studio's book, or a video Run's own copy in
    runs/<rid>_…/result/ (JL 261012: each video's transcript PDF lives in its Run)."""
    index = topic / "transcripts" / "index.json" if topic.is_dir() else None
    if index is None or not index.is_file():
        return ""
    try:
        data = json.loads(index.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ""
    if not isinstance(data, dict) or data.get("schema") != "studio-transcripts/v1":
        return ""
    cards = []
    for item in data.get("documents", []):
        if not isinstance(item, dict):
            continue
        try:
            path = (index.parent / str(item.get("file") or "")).resolve()
            path.relative_to(root.resolve())
            path.relative_to(topic.parent.parent.resolve())                 # inside this topic's Block
            page = max(1, int(item.get("page") or 1))
            end = max(page, int(item.get("end_page") or page))
        except (OSError, RuntimeError, ValueError, TypeError):
            continue
        # Only kept PDFs inside this Block; no hidden file, symlink escape or other file kind.
        if path.suffix.lower() != ".pdf" or not path.is_file() or any(p.startswith(".") for p in path.relative_to(root.resolve()).parts):
            continue
        destination = str(item.get("destination") or "")
        fragment = ("#nameddest=" + quote(destination, safe="") if destination else f"#page={page}")
        url = _file_url(path, root) + fragment + "&zoom=page-width"
        rid = str(item.get("rid") or "source")
        name = str(item.get("title") or item.get("bv") or path.stem)
        article = item.get("presentation") == "article"
        presentation = "Article PDF" if article else "Transcript PDF"
        note = ("Article arranged from an automatic transcript; not manually verified." if article else
                "Automatic speech-recognition transcript; not manually verified.")
        if item.get("transcription") != "automatic_unchecked":
            note = "Source transcript; its verification state is recorded with the source."
        warnings = item.get("warnings") or []
        note += " " + " ".join(str(w) for w in warnings)
        links = [f'<a href="{_e(url)}" target="_blank" rel="noopener">Open PDF ↗</a>']
        if article and item.get("original_pdf"):
            try:
                original = (index.parent / str(item["original_pdf"])).resolve()
                original.relative_to(root.resolve())
                original.relative_to(topic.parent.parent.resolve())
                original_page = max(1, int(item.get("original_page") or 1))
                if original.suffix.lower() == ".pdf" and original.is_file():
                    original_url = _file_url(original, root) + f"#page={original_page}&zoom=page-width"
                    links.append(f'<a href="{_e(original_url)}" target="_blank" rel="noopener">逐字原文 PDF ↗</a>')
            except (OSError, RuntimeError, ValueError, TypeError):
                pass
        source = str(item.get("source_url") or "")
        if source.startswith(("https://", "http://")):
            links.append(f'<a href="{_e(source)}" target="_blank" rel="noopener">Video ↗</a>')
        raw = (index.parent / str(item.get("raw_file") or "")).resolve()
        if raw.parent == index.parent.resolve() and raw.suffix == ".md" and raw.is_file():
            links.append(pop(_file_url(raw, root), name + " · Original text", "Original text ↗"))
        cards.append(f'<details class="topic studio-transcript" id="{_e(topic_id + "--transcript-" + rid)}">'
                     f'<summary><b>{_e(rid)} · {_e(name)}</b><span class="topic-meta">{_e("文章版" if article else "逐字原文")} · pp. {page}-{end}</span></summary>'
                     f'<p class="studio-transcript-note">{_e(note)}</p>'
                     f'<p class="studio-transcript-links">{" · ".join(links)}</p>'
                     f'<iframe class="st-frame" title="{_e(name + " · " + presentation)}" data-src="{_e(url)}" '
                     'referrerpolicy="no-referrer"></iframe></details>')
    for item in data.get("missing", []):
        if isinstance(item, dict):
            cards.append(f'<p class="studio-transcript-note">{_e(item.get("rid", ""))} · {_e(item.get("title", ""))}: '
                         'No transcript available; a summary is not a full transcript.</p>')
    return ('<section class="studio-transcripts"><h3>Video articles and transcripts · 视频文章与原文</h3>'
            + "".join(cards) + "</section>") if cards else ""


def studio_parts(topic: Path, drawings: list) -> list:
    """(part, label, drawing) for each of a topic's part drawings, `<topic>.<part>.excalidraw` (JL 261022: "They
    will share the same sNN"); a part named `3a-<kind>` reads as "sNN · ③a <kind>"."""
    if not topic.is_dir():
        return []
    nn = re.match(r"s\d+", topic.name)
    out = []
    for dr in drawings:
        if not dr.name.startswith(topic.name + ".") or dr.name == topic.name + ".excalidraw":
            continue
        part = dr.name[len(topic.name) + 1:-len(".excalidraw")]
        m = re.match(r"(\d)([a-z])-(.+)", part)
        label = f"{'①②③④⑤⑥⑦⑧⑨'[int(m.group(1)) - 1]}{m.group(2)} {m.group(3)}" if m else part
        out.append((part, ((nn.group(0) + " · ") if nn else "") + label, dr))
    return out


def _studio_parts(topic: Path, drawings: list, root: Path, topic_id: str) -> str:
    """A topic's part drawings, `<topic>.<part>.excalidraw` beside its own (JL 261022: "one section to be one
    excalidraw ... They will share the same sNN"): each a row inside the topic's row, opened in place like it.
    A part named `3a-<kind>` reads as ③a <kind>."""
    rows = [f'<details class="topic studio-part" id="{_e(topic_id + "--" + part)}"><summary><b>{_e(label)}</b></summary>'
            f'<iframe class=st-frame title="{_e(dr.stem)}" data-src="{_e(_draw_url(dr, root))}" '
            'referrerpolicy=no-referrer></iframe></details>' for part, label, dr in studio_parts(topic, drawings)]
    return f'<section class="studio-parts">{"".join(rows)}</section>' if rows else ""


def _topic_row(topic: Path, drawings: list, root: Path, folder: Path, shared: Path | None = None) -> str:
    """One closed row with its name, tags and controls; opened in place, its live drawing."""
    md = _notes(topic)
    facts = _note_facts(md)
    name = topic.name if topic.is_dir() else topic.stem
    # A face may give a readable Label (for example, its associated Job names); its folder still owns
    # anchors, grouping keys and paths. Faces without a Label keep the existing folder-name display.
    label = re.search(r"(?m)^\*\*Label:\*\*[^\S\n]*(\S[^\n]*)", md.read_text(encoding="utf-8", errors="ignore")) if md else None
    display_name = label.group(1).strip() if label else name
    drawings = [d for d in drawings if not is_structured(d)]
    first = drawings[0] if drawings else None
    mnn = structured_of(topic)
    full = pop(_draw_url(first, root), f"{display_name} · the topic, full size", "↗") if first else ""
    scripts = sorted(topic.glob("build_*.py")) if topic.is_dir() else []
    # an opened row is only its drawing (JL 261007); a hand-drawn one edits in place from the row. A topic's
    # other drawings get no link on its row (JL 261012, on s02's "studio-and-report ↗ studio-workbench-reference ↗":
    # "for the studio, remove the content in the block box here"): its face lists them
    tools = []
    frame_of = lambda d: (f'<iframe class=st-frame title="{_e(d.stem)}" data-src="{_e(_draw_url(d, root))}" '
                          f'data-edit="{_e(_draw_url(d, root, True))}" referrerpolicy=no-referrer></iframe>')
    if first and not scripts:
        tools.append('<button type=button class=draw-edit>Edit</button>')
    if first:
        body = frame_of(first)
    else:
        files = sorted(p.name for p in topic.iterdir() if p.is_file() and not p.name.startswith(".")) if topic.is_dir() else []
        body = f'<p class="mut none">No drawing; it holds {_e(" · ".join(files)) or "nothing yet"}.</p>'
    sides = ""
    if mnn:                       # Free | Structured: one pane a side. Structured is the topic's mind map drawn as the
        side = "free" if first else "structured"      # draft's §1 Structure map, drawn by the one renderer §1 uses (haipipe-mindmap);
        editable = ["free"] if first and not scripts else []   # Edit opens the free canvas, and only a hand-drawn one
        tools = [t for t in tools if "draw-edit" not in t]
        tools.append('<span class=st-side role=group aria-label="Free or Structured">'
                     f'<button type=button data-side=free aria-pressed="{str(side == "free").lower()}"'
                     f'{"" if first else " disabled"} title="the topic\'s own drawing">Free</button>'
                     f'<button type=button data-side=structured aria-pressed="{str(side == "structured").lower()}"'
                     f' title="{_e(mnn.name)}: its mind map; click a node to type, ＋ adds one">Structured</button></span>')
        if editable:
            tools.append(f'<button type=button class=draw-edit data-sides="free"{"" if side == "free" else " hidden"}>Edit</button>')
        page = mnn.with_name(mnn.name[: -len(".mindmap.md")] + ".mindmap.html")
        links = {"free": (_draw_url(first, root), f"{display_name} · the topic, full size") if first else None,
                 "structured": (_file_url(page, root), f"{display_name} · its mind map") if page.is_file() else None}
        if links[side]:
            href, label = links[side]
            full = (f'<a class=side-link data-pop="{_e(label)}" href="{_e(href)}" target=_blank rel=noopener'
                    + "".join(f' data-href-{k}="{_e(v[0])}" data-pop-{k}="{_e(v[1])}"' for k, v in links.items() if v)
                    + '>↗</a>')
        try:
            opens = lambda f: _draw_url(f, root) if f.suffix == ".excalidraw" else _file_url(f, root)   # a card's file:
            mind = mindmap_module().fragment(mnn, _rel(mnn, root), editable=not READ_ONLY_MAPS, url_of=opens)  # pop-out
        except Exception as e:            # a file that does not parse says why, in the pane, instead of a blank card
            mind = f'<p class="mut none">{_e(mnn.name)} could not be read: {_e(e)}</p>'
        body = (f'<div class=st-pane data-side=free{"" if side == "free" else " hidden"}>{body}</div>'
                f'<div class="st-pane st-map" data-side=structured{"" if side == "structured" else " hidden"}>{mind}</div>')
        sides = f' data-sides="free structured" data-side="{side}"'
    tags = "".join(f'<span class=chip data-tag="{_e(tag)}">{_e(tag)}</span>' for tag in facts["tags"])
    badges = f'<span class=topic-tags>{tags}</span>' if tags else ""
    stage = facts["stage"]
    # a coloured pill with four steps, filled up to the stage (JL 261010: no emoji, more vivid)
    steps = "".join(f'<b class="{"on" if stage and k <= STAGES.index(stage) else ""}"></b>' for k in range(len(STAGES)))
    stage_badge = (f'<span class="stage stage-{stage}" title="Stage {STAGES.index(stage) + 1} of 4: {stage} '
                   f'(its **Stage:** line)"><i class=stage-steps>{steps}</i>{stage}</span>' if stage else
                   '<span class="stage stage-none" title="No **Stage:** line yet">no stage</span>')
    topic_id, attrs, focus = "topic-" + name, "", ""
    if shared is not None:                  # in the shared Studio: the group bar's handle, Current and chips with ×
        topic_id = studio_anchor(topic, folder, shared)
        source = folder.relative_to(shared).as_posix() if folder != shared else ""
        attrs, focus, current, badges = _group_parts(topic.relative_to(shared).as_posix(), name, facts["tags"], source)
        tools.insert(0, current)
    body += _studio_parts(topic, drawings, root, topic_id)
    body += _studio_transcripts(topic, root, topic_id)
    return (f'<details class=topic id="{_e(topic_id)}" data-studio-tags="{_e(json.dumps(facts["tags"]))}"'
            f' data-stage="{_e(stage)}"{sides}{attrs}>'
            f'<summary>{focus}<b>{_e(display_name)}</b>{badges}'
            f'<span class=topic-pop>{" ".join(tools + ([full] if full else []))}</span>'
            f'{stage_badge}</summary>{body}</details>')       # the stage sits at the far right (JL 261010)


STRUCTURED = re.compile(r"^m\d{2}[-_]")          # a topic's structured side, mNN-<topic>.mindmap.md (haipipe-studio)
READ_ONLY_MAPS = False                            # a read-only host draws the map without its editing script


def is_structured(drawing: Path) -> bool:
    """A file of a topic's structured side (`mNN-<topic>.…`): never the topic's main drawing."""
    return bool(STRUCTURED.match(drawing.name)) and bool(re.match(r"s\d{2}[-_]", drawing.parent.name))


def structured_of(topic: Path) -> Path | None:
    """A topic's structured side, its mind map `mNN-<topic>.mindmap.md` with the topic's own number, else any mNN."""
    if not topic.is_dir():
        return None
    found = sorted(d for d in topic.glob("m[0-9][0-9]*.mindmap.md") if is_structured(d))
    own = [d for d in found if d.name[1:3] == topic.name[1:3]]
    return (own or found or [None])[0]


def mindmap_module():
    """haipipe-mindmap's mmmap.py: draws a .mindmap.md with the structure map a draft's §1 is drawn by (mapview.py)
    and writes its edits."""
    import importlib
    import sys
    from host_paths import skill_dir
    scripts = str(skill_dir("haipipe-mindmap") / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    return importlib.import_module("mmmap")


def topic_drawings(topic: Path) -> list:
    """A topic folder's drawings, its own first, never its structured side (mNN, the mind map)."""
    return sorted((f for f in topic.glob("*.excalidraw") if not is_structured(f)),
                  key=lambda f, own=topic.name + ".excalidraw": (f.name != own, f.name))


def _studio_topics(folder: Path) -> list:
    """(topic, drawings) for each `studio/sNN-<topic>/`; a loose drawing is its own topic. A topic's mNN mind map
    is not among its drawings: its row shows it on the Structured side (_topic_row)."""
    studio, out = folder / "studio", []
    if studio.is_dir():
        for p in sorted(studio.iterdir()):
            if p.is_dir() and not p.name.startswith(("_", ".")):
                out.append((p, topic_drawings(p)))       # the topic's own drawing first
            elif p.suffix == ".excalidraw":
                out.append((p, [p]))
    return out


# The Audience Report's views on a level no theme draws itself: the paper Board's four (JL 261009, over its
# Audience Report: "I want you to follow things like this"; b03 s01-D22), each a button, an empty one saying what
# belongs there. A Related Question is one someone else asks: its register group names who.
AUDIENCE_VIEWS = ("Ideation", "Narrative", "High-level logic + Low-level work", "Related Questions")
WHO_ASKS = ("reviewer", "coauthor", "editor", "reader")


def _empty_view(text: str) -> str:
    return f'<p class=space-empty>{text}</p>'


# ── Related: what the Block sits beside (b10 s04-related-workbench-skill, s01-D34) ──────────────────
# One related/ per Block, read by its Jobs and Tasks: meetings/, papers/, files/, emails/ and one table,
# related/related.md (kind · date · item · link · feeds · group); each subfolder is a group of its files
# (s04-D08), and /haipipe-related owns the rule (s04-D09). It folds inside the Studio, the second part
# under the topic cards (JL 261011), since what came in is what the topics think with.


def related_rows(block: Path) -> tuple:
    """(heads, rows) of the Block's related/related.md table: heads lower-cased, each row a dict."""
    table = block / "related" / "related.md"
    heads, rows = [], []
    if not table.is_file():
        return heads, rows
    for line in table.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("|") or set(line.replace("|", "").strip()) <= set("-: "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not heads:
            heads = [c.lower() for c in cells]
            continue
        rows.append(dict(zip(heads, cells + [""] * (len(heads) - len(cells)))))
    return heads, rows


def _related_target(cell: str) -> str:
    return cell.strip().strip("`").strip()


def _related_link(cell: str, block: Path, root: Path) -> str:
    """A related row's link: a web address links out; a file under related/ opens in the pop-out, a .md in
    the reader and a .docx as its preview; anything else stays as written."""
    target = _related_target(cell)
    if not target:
        return ""
    if re.match(r"https?://", target):
        return f'<a href="{_e(target)}" target=_blank rel=noopener>{_e(target.split("//", 1)[1][:48])} ↗</a>'
    path = block / "related" / target
    if path.is_file():
        return pop(_file_url(path, root), path.name, target)
    return _e(target)


def _file_url(path: Path, root: Path) -> str:
    """Where a kept file opens: a .md in the reader, a .docx or an .eml as its preview, anything else as
    itself."""
    if path.suffix == ".md":
        return _reader(path, root)
    if path.suffix.lower() in (".docx", ".eml", ".pptx"):
        return ROUTE + "?" + urlencode({"view": path.suffix.lower()[1:], "path": _rel(path, root)})
    return "/" + quote(_rel(path, root))


PREVIEW_FRAME = {".md", ".docx", ".eml", ".pptx", ".pdf", ".html", ".htm", ".txt", ".csv"}
PREVIEW_IMAGE = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}


def _related_preview(target: str, block: Path, root: Path) -> str:
    """An opened related row: the file itself, read in place (JL 261011: "could we preview the word here?"):
    Word through its package (`docx_preview`), a PDF, a page or a picture; else what it is and a link."""
    if re.match(r"https?://", target):
        return f'<p class="mut none">A web link: {_related_link(target, block, root)}</p>'
    path = block / "related" / target if target else None
    if path is None or not path.is_file():
        return (f'<p class="mut none">Not on this computer: <code>related/{_e(target)}</code> (an office '
                'file stays on the machine that saved it).</p>' if target else '<p class="mut none">No file.</p>')
    url, ext = _file_url(path, root), path.suffix.lower()
    if ext in PREVIEW_IMAGE:
        return f'<img class=related-img loading=lazy src="{_e(url)}" alt="{_e(path.name)}">'
    if ext in PREVIEW_FRAME:
        return (f'<iframe class=st-frame title="{_e(path.name)}" data-src="{_e(url)}" '
                'referrerpolicy=no-referrer></iframe>')
    return f'<p class="mut none">No preview for {_e(ext or "this file")}: {pop(url, path.name, path.name + " ↗")}</p>'


_DOCX_CACHE: dict = {}


def docx_preview(path: Path, root: Path) -> str:
    """A .docx as a page: the Word renderer's projection of its package (text, tables, images, comments in
    the margin; workbench/workbench-task-draft/exporters/docx2pdf.py `docx_html`), read only, cached by the file's stamp."""
    import importlib.util
    stamp = (str(path), path.stat().st_mtime_ns, path.stat().st_size)
    if stamp not in _DOCX_CACHE:
        spec = importlib.util.spec_from_file_location(
            "docx2pdf", Path(__file__).resolve().parent / "workbench-task-draft" / "exporters" / "docx2pdf.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        page, counts = module.docx_html(path)
        line = (f'<p style="font:13px -apple-system,sans-serif;color:#555;margin:0 0 14px">{_e(path.name)} · read '
                f'from the Word package: {counts["paragraphs"]} paragraphs · {counts["tables"]} tables · '
                f'{counts["images"]} images · {counts["comments"]} comments · '
                f'<a href="/{_e(quote(_rel(path, root)))}">the .docx ↓</a></p>')
        screen = ("<style>@media screen{body{line-height:1.5;padding:20px 28px;max-width:8.5in;margin:0 auto;"
                  "background:#fff;color:#111}}</style>")
        _DOCX_CACHE.clear()                   # one file kept: the one being read
        _DOCX_CACHE[stamp] = page.replace("<div class='page'>", screen + line + "<div class='page'>", 1)
    return _DOCX_CACHE[stamp]


# ── a deck read in place (JL 261014: "could we do the preview of the slide as well?") ────────────────────────
# A .pptx is a zip of XML: each slide drawn as one SVG, in points (12,700 EMU), with its shapes (rect, roundRect,
# ellipse, triangle, a free-form path), connector lines and their arrowheads, pictures (cropped as the deck crops
# them), text boxes and tables where the deck puts them, and the theme's colours. A placeholder with no position
# takes its layout's or master's. Charts and diagrams show as a dashed box. Read only; nothing is converted.
_PPTX_CACHE: dict = {}
_PX = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main",
       "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
       "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
_EMU = 12700.0
_DASH = {"dash": (4, 3), "sysDash": (3, 1), "dot": (1, 2), "sysDot": (1, 1), "dashDot": (4, 2, 1, 2),
         "lgDash": (8, 3), "lgDashDot": (8, 3, 1, 3), "sysDashDot": (3, 1, 1, 1)}
_PRESET_COLOURS = {"black": "000000", "white": "FFFFFF", "red": "FF0000", "green": "008000", "blue": "0000FF",
                   "yellow": "FFFF00", "gray": "808080", "grey": "808080"}
_MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
         ".svg": "image/svg+xml", ".webp": "image/webp", ".bmp": "image/bmp"}


def _q(tag: str) -> str:
    ns, name = tag.split(":")
    return "{" + _PX[ns] + "}" + name


class _Deck:
    """One open package: its parts, their relationships, the theme's colours and fonts, and the drawing state."""

    def __init__(self, path: Path, link=None):
        import xml.etree.ElementTree as ET
        self.link = link or (lambda name: "")       # a picture's address: served from the package, never inlined
        import zipfile
        self.ET, self.zf = ET, zipfile.ZipFile(path)
        self.names = set(self.zf.namelist())
        self.pictures, self.markers, self.clips, self.marked = 0, {}, 0, 0
        self.colours, self.fonts = {}, {}
        theme = next((n for n in sorted(self.names) if re.match(r"ppt/theme/theme\d+\.xml$", n)), None)
        if theme:
            t = self.xml(theme)
            scheme = t.find(".//" + _q("a:clrScheme"))
            for el in (list(scheme) if scheme is not None else []):
                c = el.find(_q("a:srgbClr"))
                s = el.find(_q("a:sysClr"))
                val = c.get("val") if c is not None else (s.get("lastClr") if s is not None else None)
                if val:
                    self.colours[el.tag.split("}")[1]] = val
            for key, tag in (("+mj-lt", "a:majorFont"), ("+mn-lt", "a:minorFont")):
                latin = t.find(".//" + _q(tag) + "/" + _q("a:latin"))
                if latin is not None:
                    self.fonts[key] = latin.get("typeface", "")

    def xml(self, name: str):
        return self.ET.fromstring(self.zf.read(name))

    def rels(self, part: str) -> dict:
        import posixpath
        name = posixpath.join(posixpath.dirname(part), "_rels", posixpath.basename(part) + ".rels")
        if name not in self.names:
            return {}
        out = {}
        for r in self.xml(name):
            if r.get("TargetMode") == "External":
                continue
            target = r.get("Target", "")
            target = target.lstrip("/") if target.startswith("/") else posixpath.normpath(
                posixpath.join(posixpath.dirname(part), target))
            out[r.get("Id")] = (r.get("Type", "").rsplit("/", 1)[-1], target)
        return out

    # colours ------------------------------------------------------------------------------------------------
    def colour(self, holder) -> tuple:
        """(#rrggbb or None, opacity) of a fill holder (a:solidFill, a fillRef, a gradient stop)."""
        import colorsys
        if holder is None:
            return None, 1.0
        el = next((c for c in holder if c.tag in (_q("a:srgbClr"), _q("a:schemeClr"), _q("a:sysClr"),
                                                   _q("a:prstClr"))), None)
        if el is None:
            return None, 1.0
        name = el.tag.split("}")[1]
        if name == "srgbClr":
            hexv = el.get("val", "000000")
        elif name == "sysClr":
            hexv = el.get("lastClr", "000000")
        elif name == "prstClr":
            hexv = _PRESET_COLOURS.get(el.get("val", ""), "000000")
        else:
            key = {"tx1": "dk1", "bg1": "lt1", "tx2": "dk2", "bg2": "lt2"}.get(el.get("val", ""), el.get("val", ""))
            hexv = self.colours.get(key, "000000")
        r, g, b = (int(hexv[i:i + 2], 16) / 255 for i in (0, 2, 4)) if len(hexv) == 6 else (0, 0, 0)
        alpha = 1.0
        for m in el:
            v = int(m.get("val", "100000")) / 100000
            kind = m.tag.split("}")[1]
            if kind == "alpha":
                alpha = v
            elif kind in ("lumMod", "lumOff"):
                h, l, s = colorsys.rgb_to_hls(r, g, b)
                l = min(1, max(0, l * v if kind == "lumMod" else l + v))
                r, g, b = colorsys.hls_to_rgb(h, l, s)
            elif kind == "shade":
                r, g, b = r * v, g * v, b * v
            elif kind == "tint":
                r, g, b = (c + (1 - c) * (1 - v) for c in (r, g, b))
        return "#%02x%02x%02x" % tuple(round(min(1, max(0, c)) * 255) for c in (r, g, b)), alpha

    def fill(self, sppr, style) -> tuple:
        for el in (list(sppr) if sppr is not None else []):
            kind = el.tag.split("}")[1]
            if kind == "noFill":
                return None, 1.0
            if kind == "solidFill":
                return self.colour(el)
            if kind == "gradFill":
                stop = el.find(".//" + _q("a:gs"))
                return self.colour(stop)
            if kind == "pattFill":
                return self.colour(el.find(_q("a:fgClr")))
        ref = style.find(_q("a:fillRef")) if style is not None else None
        return self.colour(ref) if ref is not None and ref.get("idx", "0") != "0" else (None, 1.0)

    def line(self, sppr, style, connector: bool) -> dict | None:
        ln = sppr.find(_q("a:ln")) if sppr is not None else None
        ref = style.find(_q("a:lnRef")) if style is not None else None
        colour, alpha = (None, 1.0)
        if ln is not None and ln.find(_q("a:noFill")) is not None:
            return None
        if ln is not None and ln.find(_q("a:solidFill")) is not None:
            colour, alpha = self.colour(ln.find(_q("a:solidFill")))
        elif ln is not None and ln.find(_q("a:gradFill")) is not None:
            colour, alpha = self.colour(ln.find(".//" + _q("a:gs")))
        elif ref is not None and ref.get("idx", "0") != "0":
            colour, alpha = self.colour(ref)
        elif connector:
            colour = "#000000"
        if colour is None:
            return None
        width = int(ln.get("w", "9525")) / _EMU if ln is not None and ln.get("w") else 0.75
        dash = ln.find(_q("a:prstDash")) if ln is not None else None
        ends = {k: (ln.find(_q(f"a:{k}End")).get("type", "none") if ln is not None and ln.find(_q(f"a:{k}End")) is not None
                    else "none") for k in ("head", "tail")}
        return {"colour": colour, "alpha": alpha, "width": max(width, 0.5),
                "dash": _DASH.get(dash.get("val", "solid"), None) if dash is not None else None, **ends}

    def marker(self, colour: str, kind: str) -> str:
        key = (colour, kind)
        if key not in self.markers:
            mid, self.marked = f"pm{self.marked}", self.marked + 1     # unique on the page, every slide
            shape = ('<circle cx="5" cy="5" r="4"/>' if kind == "oval" else
                     '<path d="M0,5 L5,0 L10,5 L5,10 z"/>' if kind == "diamond" else
                     '<path d="M0,0 L10,5 L0,10" fill="none" stroke-width="1.6"/>' if kind == "arrow" else
                     '<path d="M0,0 L10,5 L0,10 z"/>')
            self.markers[key] = (mid, f'<marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="3.5" '
                                      f'markerHeight="3.5" orient="auto-start-reverse"><g fill="{colour}" '
                                      f'stroke="{colour}">{shape}</g></marker>')
        return self.markers[key][0]


def _pptx_xfrm(el, tag: str = "a:xfrm") -> dict | None:
    x = el.find(_q(tag)) if el is not None else None
    off, ext = (x.find(_q("a:off")), x.find(_q("a:ext"))) if x is not None else (None, None)
    if off is None or ext is None:
        return None
    out = {k: int(off.get(k[0], "0")) / _EMU for k in ("x", "y")}
    out.update(w=int(ext.get("cx", "0")) / _EMU, h=int(ext.get("cy", "0")) / _EMU,
               rot=int(x.get("rot", "0")) / 60000, fh=x.get("flipH") in ("1", "true"),
               fv=x.get("flipV") in ("1", "true"))
    ch_off, ch_ext = x.find(_q("a:chOff")), x.find(_q("a:chExt"))
    if ch_off is not None and ch_ext is not None:
        out.update(cx=int(ch_off.get("x", "0")) / _EMU, cy=int(ch_off.get("y", "0")) / _EMU,
                   cw=int(ch_ext.get("cx", "0")) / _EMU, chh=int(ch_ext.get("cy", "0")) / _EMU)
    return out


def _pptx_geometry(sppr, w: float, h: float) -> list:
    """[(svg path d, filled, stroked)] of a shape's geometry in its own box (0..w, 0..h)."""
    import math
    f = lambda v: f"{v:.2f}"
    cust = sppr.find(_q("a:custGeom")) if sppr is not None else None
    if cust is not None:
        out = []
        for path in cust.iter(_q("a:path")):
            pw, ph = int(path.get("w", "0")) or None, int(path.get("h", "0")) or None
            sx = w / pw if pw else 1 / _EMU
            sy = h / ph if ph else 1 / _EMU
            d, cur = [], (0.0, 0.0)
            pt = lambda p: (int(p.get("x", "0")) * sx, int(p.get("y", "0")) * sy)
            for c in path:
                kind = c.tag.split("}")[1]
                pts = [pt(p) for p in c.findall(_q("a:pt"))]
                if kind == "moveTo" and pts:
                    d.append(f"M{f(pts[0][0])},{f(pts[0][1])}"); cur = pts[0]
                elif kind == "lnTo" and pts:
                    d.append(f"L{f(pts[0][0])},{f(pts[0][1])}"); cur = pts[0]
                elif kind == "cubicBezTo" and len(pts) == 3:
                    d.append("C" + " ".join(f"{f(x)},{f(y)}" for x, y in pts)); cur = pts[2]
                elif kind == "quadBezTo" and len(pts) == 2:
                    d.append("Q" + " ".join(f"{f(x)},{f(y)}" for x, y in pts)); cur = pts[1]
                elif kind == "arcTo":
                    rx, ry = int(c.get("wR", "0")) * sx, int(c.get("hR", "0")) * sy
                    st, sw = math.radians(int(c.get("stAng", "0")) / 60000), math.radians(int(c.get("swAng", "0")) / 60000)
                    cx0, cy0 = cur[0] - rx * math.cos(st), cur[1] - ry * math.sin(st)
                    end = (cx0 + rx * math.cos(st + sw), cy0 + ry * math.sin(st + sw))
                    d.append(f"A{f(rx)},{f(ry)} 0 {int(abs(sw) > math.pi)} {int(sw > 0)} {f(end[0])},{f(end[1])}")
                    cur = end
                elif kind == "close":
                    d.append("Z")
            out.append((" ".join(d), path.get("fill", "norm") != "none", path.get("stroke", "1") not in ("0", "false")))
        return out
    prst = sppr.find(_q("a:prstGeom")) if sppr is not None else None
    kind = prst.get("prst", "rect") if prst is not None else "rect"
    adj = {g.get("name"): int(re.sub(r"\D", "", g.get("fmla", "")) or 0)
           for g in (prst.iter(_q("a:gd")) if prst is not None else [])}
    if kind == "roundRect":
        r = min(w, h) * adj.get("adj", 16667) / 100000
        return [(f"M{f(r)},0 H{f(w - r)} A{f(r)},{f(r)} 0 0 1 {f(w)},{f(r)} V{f(h - r)} A{f(r)},{f(r)} 0 0 1 "
                 f"{f(w - r)},{f(h)} H{f(r)} A{f(r)},{f(r)} 0 0 1 0,{f(h - r)} V{f(r)} A{f(r)},{f(r)} 0 0 1 {f(r)},0 Z",
                 True, True)]
    if kind in ("ellipse", "flowChartConnector"):
        return [(f"M0,{f(h / 2)} A{f(w / 2)},{f(h / 2)} 0 1 0 {f(w)},{f(h / 2)} A{f(w / 2)},{f(h / 2)} 0 1 0 0,{f(h / 2)} Z",
                 True, True)]
    if kind in ("triangle", "flowChartExtract"):
        return [(f"M{f(w / 2)},0 L{f(w)},{f(h)} L0,{f(h)} Z", True, True)]
    if kind in ("diamond", "flowChartDecision"):
        return [(f"M{f(w / 2)},0 L{f(w)},{f(h / 2)} L{f(w / 2)},{f(h)} L0,{f(h / 2)} Z", True, True)]
    if kind == "bentConnector2":
        return [(f"M0,0 H{f(w)} V{f(h)}", False, True)]
    if kind.startswith("bentConnector"):
        x = w * adj.get("adj1", 50000) / 100000
        return [(f"M0,0 H{f(x)} V{f(h)} H{f(w)}", False, True)]
    if kind.startswith("curvedConnector"):
        return [(f"M0,0 C{f(w / 2)},0 {f(w / 2)},{f(h)} {f(w)},{f(h)}", False, True)]
    if kind in ("line", "straightConnector1"):
        return [(f"M0,0 L{f(w)},{f(h)}", False, True)]
    return [(f"M0,0 H{f(w)} V{f(h)} H0 Z", True, True)]


def _pptx_text(deck: _Deck, body, w: float, h: float, inherited: dict) -> str:
    """A shape's text as an HTML block in a foreignObject over its box: insets, anchor, wrap, paragraphs, runs."""
    if body is None or not any((t.text or "").strip() for t in body.iter(_q("a:t"))):
        return ""
    pr = body.find(_q("a:bodyPr"))
    pr = pr if pr is not None else deck.ET.Element("x")
    ins = [int(pr.get(k, d)) / _EMU for k, d in (("tIns", "45720"), ("rIns", "91440"), ("bIns", "45720"), ("lIns", "91440"))]
    anchor = {"ctr": "center", "b": "flex-end"}.get(pr.get("anchor") or inherited.get("anchor", "t"), "flex-start")
    nowrap = pr.get("wrap") == "none"
    fit = pr.find(_q("a:normAutofit"))
    scale = int(fit.get("fontScale", "100000")) / 100000 if fit is not None else 1.0
    base = dict(inherited)
    styles = body.find(_q("a:lstStyle"))
    for lvl in ("a:defPPr", "a:lvl1pPr"):
        el = styles.find(_q(lvl)) if styles is not None else None
        if el is not None:
            base.update(_pptx_ppr(deck, el))
    paras, number = [], 0
    for p in body.findall(_q("a:p")):
        ppr = p.find(_q("a:pPr"))
        style = dict(base, **(_pptx_ppr(deck, ppr) if ppr is not None else {}))
        runs, size = [], style.get("sz", 18.0)
        for r in p:
            kind = r.tag.split("}")[1]
            if kind == "br":
                runs.append("<br>")
                continue
            if kind not in ("r", "fld"):
                continue
            rs = dict(style, **_pptx_rpr(deck, r.find(_q("a:rPr"))))
            size = max(size, rs.get("sz", size)) if runs else rs.get("sz", size)
            css = [f"font-size:{rs.get('sz', 18.0) * scale:.2f}px"]
            if rs.get("b"):
                css.append("font-weight:700")
            if rs.get("i"):
                css.append("font-style:italic")
            if rs.get("u"):
                css.append("text-decoration:underline")
            if rs.get("color"):
                css.append(f"color:{rs['color']}")
            if rs.get("font"):
                face = deck.fonts.get(rs["font"], rs["font"])
                css.append(f"font-family:'{_e(face)}',Aptos,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif")
            text = "".join(t.text or "" for t in r.iter(_q("a:t")))
            runs.append(f'<span style="{";".join(css)}">{_e(text)}</span>')
        end = p.find(_q("a:endParaRPr"))
        if not runs and end is not None and end.get("sz"):
            size = int(end.get("sz")) / 100
        bullet = ""
        if runs and style.get("bullet"):
            number += 1
            bullet = f"{number}. " if style["bullet"] == "#" else style["bullet"] + " "
        align = {"ctr": "center", "r": "right", "just": "justify", "dist": "justify"}.get(style.get("algn", "l"), "left")
        css = [f"text-align:{align}", f"font-size:{size * scale:.2f}px", f"line-height:{style.get('lh', 1.2):.2f}",
               f"margin:{style.get('before', 0):.2f}px 0 {style.get('after', 0):.2f}px {style.get('marL', 0):.2f}px"]
        if style.get("indent"):
            css.append(f"text-indent:{style['indent']:.2f}px")
        if nowrap:
            css.append("white-space:pre")
        paras.append(f'<p style="{";".join(css)}">{_e(bullet)}{"".join(runs) or "&#8203;"}</p>')
    return (f'<foreignObject x="0" y="0" width="{w:.2f}" height="{h:.2f}" overflow="visible">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" style="box-sizing:border-box;width:{w:.2f}px;height:{h:.2f}px;'
            f'display:flex;flex-direction:column;justify-content:{anchor};padding:{ins[0]:.2f}px {ins[1]:.2f}px '
            f'{ins[2]:.2f}px {ins[3]:.2f}px;overflow:visible;color:{inherited.get("color") or "#" + deck.colours.get("dk1", "000000")};'
            f'font-family:Aptos,-apple-system,\'Segoe UI\',Helvetica,Arial,sans-serif;'
            f'{"align-items:center;" if nowrap and base.get("algn") == "ctr" else ""}word-wrap:break-word">'
            f'{"".join(paras)}</div></foreignObject>')


def _pptx_rpr(deck: _Deck, el) -> dict:
    """A run's (or a level's defRPr) size in points, bold, italic, underline, colour and typeface."""
    if el is None:
        return {}
    out = {}
    if el.get("sz"):
        out["sz"] = int(el.get("sz")) / 100
    for k in ("b", "i"):
        if el.get(k) is not None:
            out[k] = el.get(k) in ("1", "true")
    if el.get("u") not in (None, "none"):
        out["u"] = True
    fill = el.find(_q("a:solidFill"))
    if fill is not None:
        out["color"] = deck.colour(fill)[0]
    latin = el.find(_q("a:latin"))
    if latin is not None and latin.get("typeface"):
        out["font"] = latin.get("typeface")
    return out


def _pptx_ppr(deck: _Deck, el) -> dict:
    """A paragraph's (or a level's) alignment, spacing, indents and bullet, with its default run style."""
    out = {}
    if el.get("algn"):
        out["algn"] = el.get("algn")
    for k, key in (("marL", "marL"), ("indent", "indent")):
        if el.get(k):
            out[key] = int(el.get(k)) / _EMU
    for tag, key in (("a:spcBef", "before"), ("a:spcAft", "after")):
        pts = el.find(_q(tag) + "/" + _q("a:spcPts"))
        if pts is not None:
            out[key] = int(pts.get("val", "0")) / 100
    pct = el.find(_q("a:lnSpc") + "/" + _q("a:spcPct"))
    if pct is not None:
        out["lh"] = 1.2 * int(pct.get("val", "100000")) / 100000
    if el.find(_q("a:buNone")) is not None:
        out["bullet"] = ""
    elif el.find(_q("a:buChar")) is not None:
        out["bullet"] = el.find(_q("a:buChar")).get("char", "•")
    elif el.find(_q("a:buAutoNum")) is not None:
        out["bullet"] = "#"
    out.update(_pptx_rpr(deck, el.find(_q("a:defRPr"))))
    return out


def _pptx_placeholder(deck: _Deck, sp, holders: list) -> tuple:
    """(xfrm, style) a placeholder takes from its layout, then its master, when the slide gives it no position."""
    ph = sp.find(_q("p:nvSpPr") + "/" + _q("p:nvPr") + "/" + _q("p:ph"))
    if ph is None:
        return None, {}
    kind, idx = ph.get("type", "body"), ph.get("idx")
    same = {"ctrTitle": "title", "subTitle": "body", "obj": "body"}
    xfrm, style = None, {}
    for tree, master_styles in holders:
        for other in tree.iter(_q("p:sp")):
            oph = other.find(_q("p:nvSpPr") + "/" + _q("p:nvPr") + "/" + _q("p:ph"))
            if oph is None:
                continue
            if (idx is not None and oph.get("idx") == idx) or same.get(oph.get("type", "body"), oph.get("type", "body")) \
                    == same.get(kind, kind):
                xfrm = xfrm or _pptx_xfrm(other.find(_q("p:spPr")))
                pr = other.find(_q("p:txBody") + "/" + _q("a:bodyPr"))
                if pr is not None and pr.get("anchor") and "anchor" not in style:
                    style["anchor"] = pr.get("anchor")
                lvl = other.find(_q("p:txBody") + "/" + _q("a:lstStyle") + "/" + _q("a:lvl1pPr"))
                if lvl is not None:
                    style = dict(_pptx_ppr(deck, lvl), **style)
                break
        if master_styles is not None:
            which = "p:titleStyle" if same.get(kind, kind) == "title" else "p:bodyStyle"
            lvl = master_styles.find(_q(which) + "/" + _q("a:lvl1pPr"))
            if lvl is not None:
                style = dict(_pptx_ppr(deck, lvl), **style)
    return xfrm, style


def _pptx_shapes(deck: _Deck, tree, part: str, rels: dict, holders: list) -> str:
    """The children of one shape tree (a slide's, or a group's), drawn in order."""
    out = []
    for el in tree:
        kind = el.tag.split("}")[1]
        nv = next((c for c in el if c.tag.split("}")[1].startswith("nv")), None)
        cnv = nv.find(_q("p:cNvPr")) if nv is not None else None
        if cnv is not None and cnv.get("hidden") in ("1", "true"):
            continue
        if kind == "grpSp":
            x = _pptx_xfrm(el.find(_q("p:grpSpPr")))
            inner = _pptx_shapes(deck, el, part, rels, holders)
            if x and x.get("cw") and x.get("chh"):
                t = (f'translate({x["x"]:.2f} {x["y"]:.2f}) scale({x["w"] / x["cw"]:.5f} {x["h"] / x["chh"]:.5f}) '
                     f'translate({-x["cx"]:.2f} {-x["cy"]:.2f})')
                out.append(f'<g transform="{t}">{inner}</g>')
            else:
                out.append(f"<g>{inner}</g>")
        elif kind in ("sp", "cxnSp", "pic", "graphicFrame"):
            out.append(_pptx_one(deck, el, kind, part, rels, holders))
    return "".join(out)


def _pptx_one(deck: _Deck, el, kind: str, part: str, rels: dict, holders: list) -> str:
    sppr = el.find(_q("p:spPr"))
    style = el.find(_q("p:style"))
    x = _pptx_xfrm(el, "p:xfrm") if kind == "graphicFrame" else _pptx_xfrm(sppr)
    inherited = {}
    if kind == "sp":
        px, inherited = _pptx_placeholder(deck, el, holders)
        x = x or px
        font_ref = style.find(_q("a:fontRef")) if style is not None else None
        if font_ref is not None and deck.colour(font_ref)[0]:
            inherited.setdefault("color", deck.colour(font_ref)[0])
    if not x:
        return ""
    w, h = x["w"], x["h"]
    cx, cy = w / 2, h / 2
    move = f'translate({x["x"]:.2f} {x["y"]:.2f})' + (f' rotate({x["rot"]:.2f} {cx:.2f} {cy:.2f})' if x["rot"] else "")
    flip = (f' transform="translate({cx:.2f} {cy:.2f}) scale({-1 if x["fh"] else 1} {-1 if x["fv"] else 1}) '
            f'translate({-cx:.2f} {-cy:.2f})"') if x["fh"] or x["fv"] else ""
    body = ""
    if kind == "pic":
        blip = el.find(".//" + _q("a:blip"))
        target = rels.get(blip.get(_q("r:embed")) if blip is not None else None)
        ext = Path(target[1]).suffix.lower() if target else ""
        if target and ext in _MIME and target[1] in deck.names:
            deck.pictures += 1
            crop = el.find(".//" + _q("a:srcRect"))
            l, t, r, b = ((int(crop.get(k, "0")) / 100000 for k in ("l", "t", "r", "b")) if crop is not None
                          else (0, 0, 0, 0))
            iw, ih = w / max(1e-6, 1 - l - r), h / max(1e-6, 1 - t - b)
            image = (f'<image href="{_e(deck.link(target[1]))}" x="{-l * iw:.2f}" y="{-t * ih:.2f}" '
                     f'width="{iw:.2f}" height="{ih:.2f}" preserveAspectRatio="none"/>')
            if crop is not None and any((l, t, r, b)):
                deck.clips += 1
                body = (f'<clipPath id="pc{deck.clips}"><rect width="{w:.2f}" height="{h:.2f}"/></clipPath>'
                        f'<g clip-path="url(#pc{deck.clips})">{image}</g>')
            else:
                body = image
        else:
            body = (f'<rect width="{w:.2f}" height="{h:.2f}" fill="#f1f3f5" stroke="#adb5bd" stroke-dasharray="4 3"/>'
                    f'<text x="{cx:.2f}" y="{cy:.2f}" font-size="10" text-anchor="middle" fill="#868e96">picture</text>')
        return f'<g transform="{move}"><g{flip}>{body}</g></g>'
    if kind == "graphicFrame":
        tbl = el.find(".//" + _q("a:tbl"))
        if tbl is None:
            return (f'<g transform="{move}"><rect width="{w:.2f}" height="{h:.2f}" fill="none" stroke="#adb5bd" '
                    f'stroke-dasharray="4 3"/><text x="{cx:.2f}" y="{cy:.2f}" font-size="12" text-anchor="middle" '
                    f'fill="#868e96">chart or diagram</text></g>')
        cols = [int(c.get("w", "0")) / _EMU for c in tbl.iter(_q("a:gridCol"))]
        rows = []
        for tr in tbl.findall(_q("a:tr")):
            cells = []
            for tc in tr.findall(_q("a:tc")):
                if tc.get("hMerge") or tc.get("vMerge"):
                    continue
                fill = deck.colour(tc.find(_q("a:tcPr") + "/" + _q("a:solidFill")))[0] if tc.find(_q("a:tcPr")) is not None else None
                text = " ".join("".join(t.text or "" for t in p.iter(_q("a:t"))) for p in tc.iter(_q("a:p")))
                span = f' colspan="{tc.get("gridSpan")}"' if tc.get("gridSpan") else ""
                cells.append(f'<td{span} style="border:1px solid #ced4da;padding:2px 5px;'
                             f'{f"background:{fill};" if fill else ""}">{_e(text)}</td>')
            rows.append(f'<tr style="height:{int(tr.get("h", "0")) / _EMU:.2f}px">{"".join(cells)}</tr>')
        widths = "".join(f'<col style="width:{c:.2f}px">' for c in cols)
        return (f'<g transform="{move}"><foreignObject width="{w:.2f}" height="{h:.2f}" overflow="visible">'
                f'<table xmlns="http://www.w3.org/1999/xhtml" style="border-collapse:collapse;width:{w:.2f}px;'
                f'font:11px Aptos,-apple-system,Helvetica,Arial,sans-serif">{widths}{"".join(rows)}</table>'
                f'</foreignObject></g>')
    colour, alpha = deck.fill(sppr, style)
    line = deck.line(sppr, style, kind == "cxnSp")
    parts = []
    for d, filled, stroked in _pptx_geometry(sppr, w, h):
        attrs = [f'd="{d}"', f'fill="{colour}"' if filled and colour else 'fill="none"']
        if filled and colour and alpha < 1:
            attrs.append(f'fill-opacity="{alpha:.3f}"')
        if stroked and line:
            attrs += [f'stroke="{line["colour"]}"', f'stroke-width="{line["width"]:.2f}"', 'stroke-linejoin="round"']
            if line["alpha"] < 1:
                attrs.append(f'stroke-opacity="{line["alpha"]:.3f}"')
            if line["dash"]:
                attrs.append('stroke-dasharray="' + " ".join(f"{v * line['width']:.2f}" for v in line["dash"]) + '"')
            if line["head"] != "none":
                attrs.append(f'marker-start="url(#{deck.marker(line["colour"], line["head"])})"')
            if line["tail"] != "none":
                attrs.append(f'marker-end="url(#{deck.marker(line["colour"], line["tail"])})"')
        if 'fill="none"' in attrs and not (stroked and line):
            continue
        parts.append(f'<path {" ".join(attrs)}/>')
    text = _pptx_text(deck, el.find(_q("p:txBody")), w, h, inherited) if kind == "sp" else ""
    if not parts and not text:
        return ""
    return f'<g transform="{move}"><g{flip}>{"".join(parts)}</g>{text}</g>'


def pptx_preview(path: Path, root: Path) -> str:
    """A .pptx as a page: every slide drawn from its package as one SVG picture, in order; read only, cached by the
    file's stamp. A deck's own renders (its `render/` lane) stay the picture that counts; this reads the deck itself."""
    stamp = (str(path), path.stat().st_mtime_ns, path.stat().st_size)
    if stamp in _PPTX_CACHE:
        return _PPTX_CACHE[stamp]
    deck = _Deck(path, lambda name: ROUTE + "?" + urlencode({"view": "pptx", "path": _rel(path, root), "media": name}))
    pres = deck.xml("ppt/presentation.xml")
    size = pres.find(_q("p:sldSz"))
    W, H = (int(size.get("cx")) / _EMU, int(size.get("cy")) / _EMU) if size is not None else (720.0, 405.0)
    prels = deck.rels("ppt/presentation.xml")
    order = [prels.get(s.get(_q("r:id")), ("", ""))[1] for s in pres.iter(_q("p:sldId"))]
    slides = []
    for n, part in enumerate([o for o in order if o in deck.names], 1):
        tree = deck.xml(part)
        rels = deck.rels(part)
        layout = next((t for k, t in rels.values() if k == "slideLayout" and t in deck.names), None)
        holders, backs = [], [tree]
        if layout:
            ltree = deck.xml(layout)
            master = next((t for k, t in deck.rels(layout).values() if k == "slideMaster" and t in deck.names), None)
            mtree = deck.xml(master) if master else None
            holders = [(ltree, None)] + ([(mtree, mtree.find(_q("p:txStyles")))] if mtree is not None else [])
            backs += [ltree] + ([mtree] if mtree is not None else [])
        background = "#ffffff"
        for b in backs:
            bg = b.find(".//" + _q("p:bg"))
            if bg is None:
                continue
            pr, ref = bg.find(_q("p:bgPr")), bg.find(_q("p:bgRef"))
            got = deck.fill(pr, None)[0] if pr is not None else deck.colour(ref)[0] if ref is not None else None
            background = got or background
            break
        deck.markers = {}                        # this slide's arrowheads
        spt = tree.find(".//" + _q("p:spTree"))
        drawn = _pptx_shapes(deck, spt, part, rels, holders) if spt is not None else ""
        defs = "".join(m for _, m in deck.markers.values())
        slides.append(f'<p class=cap>Slide {n}</p><div class=slide><svg xmlns="http://www.w3.org/2000/svg" '
                      f'viewBox="0 0 {W:.2f} {H:.2f}" role="img" aria-label="Slide {n}"><defs>{defs}</defs>'
                      f'<rect width="{W:.2f}" height="{H:.2f}" fill="{background}"/>{drawn}</svg></div>')
    line = (f'<p class=cap>{_e(path.name)} · read from the deck package: {len(slides)} slide'
            f'{"s" if len(slides) != 1 else ""} · {deck.pictures} pictures · '
            f'<a href="/{_e(quote(_rel(path, root)))}">the .pptx ↓</a></p>')
    page = ('<!doctype html><meta charset=utf-8><title>' + _e(path.name) + '</title>'
            '<style>body{margin:0;padding:14px 18px;background:#f1f3f5;font:13px -apple-system,sans-serif;color:#555}'
            '.cap{max-width:1600px;margin:0 auto 6px}.slide{max-width:1600px;margin:0 auto 18px;background:#fff;'
            'box-shadow:0 1px 3px rgba(0,0,0,.18)}.slide svg{display:block;width:100%;height:auto}'
            '.slide p{margin:0}</style>' + line + "".join(slides))
    _PPTX_CACHE.clear()                           # one deck kept: the one being read
    _PPTX_CACHE[stamp] = page
    return page


def pptx_media(path: Path, name: str) -> tuple | None:
    """(bytes, type) of one picture inside a deck (`ppt/media/…`), for its slide's <image>; None when it is not one."""
    import zipfile
    ext = Path(name).suffix.lower()
    if not name.startswith("ppt/media/") or ext not in _MIME:
        return None
    with zipfile.ZipFile(path) as zf:
        return (zf.read(name), _MIME[ext]) if name in zf.namelist() else None


def _related_folder(target: str) -> str:
    """The subfolder of related/ a kept file sits in, read off its link (`meetings/…` → meetings): the
    item's own group, as a topic's **Type:** line is (b10 s04-D08); '' for a web link or a file at the top."""
    if re.match(r"[a-z][a-z0-9+.-]*:", target, re.I) or "/" not in target:
        return ""
    head = target.split("/", 1)[0]
    return "" if head.startswith((".", "_")) or head == ".." else head


def eml_preview(path: Path, root: Path) -> str:
    """An email saved as it came (`related/emails/<date> <subject>.eml`, s04-D08) as a page: its From, To,
    Cc, Date and Subject, its text, and its attachments by name. An HTML-only body shows in a sandboxed
    frame, so nothing in it runs; read only."""
    from email import policy
    from email.parser import BytesParser
    msg = BytesParser(policy=policy.default).parsebytes(path.read_bytes())
    heads = "".join(f"<tr><th>{h}</th><td>{_e(str(msg[h]))}</td></tr>" for h in ("From", "To", "Cc", "Date", "Subject")
                    if msg[h])
    part = msg.get_body(preferencelist=("plain", "html"))
    text = part.get_content() if part is not None else ""
    if part is not None and part.get_content_type() == "text/html":
        body = (f'<iframe sandbox title="the email" style="width:100%;height:70vh;border:1px solid #ddd" '
                f'srcdoc="{_e(text)}"></iframe>')
    else:
        body = f'<pre style="white-space:pre-wrap;font:14px/1.55 -apple-system,sans-serif">{_e(text.strip())}</pre>'
    files = [(a.get_filename() or "attachment", len(a.get_payload(decode=True) or b"")) for a in msg.iter_attachments()]
    kept = ("<p><b>Attachments</b>: " + " · ".join(f"{_e(n)} ({k // 1024 or 1} KB)" for n, k in files) + "</p>"
            if files else "")
    return ('<!doctype html><meta charset=utf-8><title>' + _e(str(msg["Subject"] or path.name)) + '</title>'
            '<style>body{font:15px/1.5 -apple-system,sans-serif;max-width:880px;margin:0 auto;padding:18px 28px;'
            'background:#fff;color:#111}th{text-align:left;padding:2px 14px 2px 0;color:#555;font-weight:500}'
            'table{margin-bottom:12px}</style>'
            f'<p style="font-size:13px;color:#666">{_e(path.name)} · an email, as it came · '
            f'<a href="/{_e(quote(_rel(path, root)))}">the .eml ↓</a></p><table>{heads}</table>{kept}<hr>{body}')


def related_items(block: Path) -> list:
    """Each related item, in the order its rows show: one per related/related.md row, then each file kept in
    a subfolder of related/ that no row names yet ("no row yet"). Its groups are its subfolder first, then
    the row's `group` cell, names split at commas like a topic's **Tags:** line (JL 261011: "for the related,
    we have the things like subfolders and can give them the group name"): a meeting's notes in meetings/
    sit under meetings, not Untagged. A row kept as a web link has no subfolder, so its `kind` stands in
    (JL 261013: the groups are "things like meeting, email, paper"). `key` is the row's link, else its item."""
    folder = block / "related"
    heads, rows = related_rows(block)
    meta_cols = [h for h in heads if h and h not in ("item", "link", "group")]
    items, keys = [], set()
    for n, r in enumerate(rows):
        target = _related_target(r.get("link", ""))
        key = target or "item:" + (r.get("item") or str(n))
        key = key if key not in keys else f"{key}#{n}"
        keys.add(key)
        meta = " · ".join((f"{h} {r[h]}" if h not in ("kind", "date") else r[h]).replace("`", "")
                          for h in meta_cols if r.get(h))
        sub = _related_folder(target) or (r.get("kind") or "").strip().lower()   # its home group: folder, else kind
        items.append({"key": key, "title": r.get("item") or target or "—", "meta": meta, "target": target,
                      "row": n, "folder": sub, "groups": _split_tags(",".join([sub, r.get("group", "")]))})
    for d in sorted(x for x in folder.iterdir() if x.is_dir() and not x.name.startswith((".", "_"))) if folder.is_dir() else []:
        for f in sorted(d.rglob("*")):
            rel_ = f.relative_to(folder).as_posix()
            if f.is_file() and not f.name.startswith(".") and rel_ not in keys:
                keys.add(rel_)
                items.append({"key": rel_, "title": f.name, "meta": f"related/{rel_} · no row yet", "target": rel_,
                              "row": None, "folder": d.name, "groups": [d.name]})
    return _related_versions(folder, items)


def _related_versions(folder: Path, items: list) -> list:
    """Files of one folder that are versions of one thing (`version_roots`: `Proposal-v1.docx` … `-v3.docx`) fold
    into one item, newest version first (JL 261014). The item keeps a row's name, key and groups when one of its
    versions has a row, so a new version dropped in beside it needs no new row."""
    by_dir = {}
    for i in items:
        path = folder / i["target"] if i["target"] and not re.match(r"[a-z][a-z0-9+.-]*:", i["target"], re.I) else None
        if path is not None and path.is_file():
            by_dir.setdefault(path.parent, []).append((i, path))
    gone = set()
    for parent, members in by_dir.items():
        roots = version_roots([path.stem for _, path in members])
        families = {}
        for i, path in members:
            families.setdefault(roots[path.stem], []).append((i, path))
        for root_name, family in families.items():
            if len({path.stem for _, path in family}) < 2:   # one name in two formats (a .docx and its PDF) stays
                continue                                     # as it came: two items, each with its own row
            family.sort(key=lambda m: -m[1].stat().st_mtime)
            stems = [path.stem for _, path in family]
            head = next((i for i, _ in family if i["row"] is not None), family[0][0])
            head["versions"] = [{"label": version_label(path.stem, root_name, True)
                                 + (f" · {path.suffix.lstrip('.')}" if stems.count(path.stem) > 1 else ""),
                                 "target": i["target"], "when": path.stat().st_mtime} for i, path in family]
            if head["row"] is None:
                head["title"] = root_name
            head["meta"] = (head["meta"] + " · " if head["meta"] else "") + f"{len(family)} versions"
            gone.update(id(i) for i, _ in family if i is not head)
    return [i for i in items if id(i) not in gone]


def _related_set_groups(block: Path, item: dict, groups: list) -> None:
    """Write a related item's groups into its row's `group` cell in related/related.md. A table with no
    `group` column gets one at its end; a file with no row yet gets one (its item, link and group). Its
    subfolder's group is never written: the path already says it."""
    groups = [g for g in groups if g.casefold() != (item.get("folder") or "").casefold()]
    table = block / "related" / "related.md"
    lines = table.read_text(encoding="utf-8").splitlines() if table.is_file() else []
    is_rule = lambda line: set(line.replace("|", "").strip()) <= set("-: ")
    cells = lambda line: [c.strip() for c in line.strip().strip("|").split("|")]
    draw = lambda cs: "| " + " | ".join(cs) + " |"
    if not any(line.startswith("|") and not is_rule(line) for line in lines):     # no table yet: the frame's own
        lines += ([""] if lines and lines[-1].strip() else []) + ["| kind | date | item | link | feeds |",
                                                                  "|---|---|---|---|---|"]
    body = [i for i, line in enumerate(lines) if line.startswith("|") and not is_rule(line)]
    head = body.pop(0)
    heads = [c.lower() for c in cells(lines[head])]
    if "group" not in heads:
        n = len(heads)
        for i, line in enumerate(lines):
            if line.startswith("|"):
                fill = "---" if i != head and is_rule(line) else ""
                cs = cells(line) + [fill] * max(0, n - len(cells(line)))
                cs.insert(n, "group" if i == head else fill)
                lines[i] = "|" + "|".join(cs) + "|" if fill else draw(cs)       # a rule line stays |---|
        heads.append("group")
    if item["row"] is None:
        at = max(i for i, line in enumerate(lines) if line.startswith("|")) + 1
        lines.insert(at, draw([{"item": item["title"], "link": f"`{item['target']}`"}.get(h, "") for h in heads]))
    else:
        at = body[item["row"]]
    cs = cells(lines[at]) + [""] * max(0, len(heads) - len(cells(lines[at])))
    cs[heads.index("group")] = ", ".join(groups)
    lines[at] = draw(cs)
    table.write_text("\n".join(lines) + "\n", encoding="utf-8")


def related_view(block: Path, root: Path, sub: str = "") -> Space:
    """The Related view: one folding row per item, opened on its file's preview, under the Studio's group
    bar (group_list, JL 261011): Current, the groups in related/_groups.txt order, Untagged, + Group. Each
    subfolder is a group of its files (meetings/ → meetings, s04-D08); a file no row names yet sits there too,
    and a drag onto another group gives it a row."""
    folder = block / "related"
    items, table_md = related_items(block), folder / "related.md"
    if not items:
        html_ = _empty_view("Nothing related yet. What came in from outside (a meeting's notes, a paper, a file "
                            "we were sent, an email, a repo or dataset) is kept once, here, in a subfolder of "
                            "related/ (meetings/, papers/, files/, emails/), and one row in related/related.md (kind "
                            "· date · item · link · feeds · group); the subfolder is its first group, the group "
                            "column adds more.")
    else:
        rows = []
        for i in items:
            attrs, handle, current, chips = _group_parts(i["key"], i["title"], i["groups"], noun="item",
                                                          fixed=(i["folder"],))
            link = _related_link(i["target"], block, root) if i["target"] else ""
            rows.append(f'<details class="topic{"" if i["row"] is not None else " missing"}" data-studio-tags='
                        f'"{_e(json.dumps(i["groups"]))}"{attrs}><summary>{handle}<span class=related-head>'
                        f'<b>{_e(i["title"])}</b>{chips}'
                        + (f'<br><span class=topic-meta>{_e(i["meta"])}</span>' if i["meta"] else "") + "</span>"
                        + f'<span class=topic-pop>{current} {link}</span>'
                        + "</summary>" + (version_panes(i["versions"], lambda v: (
                            f'<p class="mut dv-files">{_e(v["label"])}: {_related_link(v["target"], block, root)}</p>'
                            + _related_preview(v["target"], block, root))) if i.get("versions")
                            else _related_preview(i["target"], block, root)) + "</details>")
        note = (f'<p class=mut>{_link(_reader(table_md, root), "related/related.md")}: one row per item. A '
                'subfolder is a group of its files (meetings/ → meetings); the row\'s group column adds more. '
                'What lands here is not edited again.</p>' if table_md.is_file() else
                '<p class=mut>No related/related.md yet: these files have no row; a drag onto a group adds one.</p>')
        html_ = note + group_list(block, root, "related", [i["groups"] for i in items], "".join(rows))
    return Space(html_,
                 run_types=(run_type("run-add-related-<slug>", "add a related item",
                                     "Add an item to the related/ of {folder}: the file, as it came, in a subfolder "
                                     "of related/ (meetings/, papers/ (open-licensed PDFs only), files/, emails/), "
                                     "and one row in related/related.md (kind · date · item · link · feeds · group; "
                                     "the subfolder is its first group, more go in the group cell, comma-"
                                     "separated).", "haipipe-related"),),
                 disk=(("related/related.md", "one row per item: kind · date · item · link · feeds · group"),
                       ("related/_groups.txt", "the groups, in button order")))


def studio_related(view: Space, block: Path, root: Path, unfold: bool = False) -> Space:
    """Related inside the Studio: the second folding part, under the topic cards (JL 261011: "put the
    related as the second collapse part in the box of the studio items"). `view` is the Block's Related
    Space as its theme fills it (paper: cards by question), else the vanilla table; folded unless a
    Related link opened the page."""
    view = view if view.html else related_view(block, root)
    _, rows = related_rows(block)
    kinds = {}
    for r in rows:
        kind = r.get("kind", "").lower() or "item"
        kinds[kind] = kinds.get(kind, 0) + 1
    counts = " · ".join(f"{k} {n}" for k, n in kinds.items())
    meta = f'related/ · {len(rows)} item{"s" if len(rows) != 1 else ""}' + (f" · {counts}" if counts else "")
    html_ = (f'<details class=studio-related id=studio-related{" open" if unfold else ""}>'
             f'<summary><b>Related</b><span class=related-meta>{_e(meta)}</span></summary>'
             f'<div class=related-in>{view.html}</div></details>')
    return Space(html_, run_types=view.run_types, disk=view.disk)


def studio_delivery(block: Path, root: Path, theme=None) -> str:
    """Delivery inside the Studio: the third folding part, under Related (JL 261014: "a new item after the
    Related to name it as the delivery ... show all the delivery and preview them here"). What came in, then
    what went out: every result in the Block's delivery/, from every Job and Task, as Delivery's own cards,
    each opened on its preview. The top row's Delivery stays the full view: its parts, by source, its build."""
    items = delivery_items(block)
    kinds = {k: sum(k in i["fixed"] for i in items) for k in dict.fromkeys(DELIVERY_OPENS.values())}
    counts = " · ".join(f"{k} {n}" for k, n in kinds.items() if n)
    meta = f'delivery/ · {len(items)} result{"s" if len(items) != 1 else ""}' + (f" · {counts}" if counts else "")
    full = _link(href(block, root, theme or VANILLA, "Delivery"), "the full Delivery")
    body = (delivery_view(block, root, theme) + f'<p class=mut>Each Job\'s and Task\'s part, by source: {full}.</p>'
            if items else _empty_view(f"Nothing delivered yet. What a Block sends (a PDF, a Word file, a deck, a web "
                                      f"page) is built into its delivery/, under its source's path; {full}."))
    return (f'<details class=studio-related id=studio-delivery><summary><b>Delivery</b>'
            f'<span class=related-meta>{_e(meta)}</span></summary><div class=related-in>{body}</div></details>')


# ── Studio › Timeline: what moved when, the fifth folding part (JL 261011; fourth until Runs came, 261019) ─────────────────
# Read from what is already on disk, nothing new to write: each topic's dated decisions (sNN-DNN …
# (JL 261011)), its sessions (runs/run-draw-<sNN>/passes/pNN-<MMDD>/) and the green change notes in
# its drawing (✎ <YYMMDD> <what>, haipipe-studio's change notes). Newest day first; the page script
# hides a topic's lines when the group bar hides its row.
_YYMMDD = re.compile(r"(?<!\d)(2[4-9])(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])(?!\d)")
_NOTES_SEEN: dict = {}


def _yymmdd(m) -> str:
    return f"20{m.group(1)}-{m.group(2)}-{m.group(3)}"


def _drawing_notes(d: Path) -> list:
    """(day, what) for each green change note in a drawing, read once per version of the file."""
    try:
        stat = d.stat()
    except OSError:
        return []
    key = (str(d), stat.st_mtime_ns, stat.st_size)
    if key not in _NOTES_SEEN:
        try:
            elements = json.loads(d.read_text(encoding="utf-8")).get("elements") or []
        except (OSError, ValueError, AttributeError):
            elements = []
        notes = []
        for el in elements:
            if not isinstance(el, dict) or el.get("type") != "text" or el.get("isDeleted"):
                continue
            text = re.sub(r"\s+", " ", str(el.get("text") or "")).strip()
            m = _YYMMDD.match(text[1:].strip()) if text.startswith("✎") else None
            if m:
                notes.append((_yymmdd(m), text[1:].strip()[m.end():].strip()))
        if len(_NOTES_SEEN) > 2000:
            _NOTES_SEEN.clear()
        _NOTES_SEEN[key] = notes
    return _NOTES_SEEN[key]


def _decisions(md: Path | None) -> list:
    """(day or "", id, what) for each `sNN-DNN · <what>` line of a topic's notes, its indented lines
    included; the day is the first YYMMDD in it, when it was decided."""
    if not md:
        return []
    out, cur = [], None
    for line in md.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = re.match(r"(s\d+-D\d+)\b[ \t]*[·:\-–]?[ \t]*(.*)", line)
        if m:
            cur = [m.group(1), m.group(2)]
            out.append(cur)
        elif cur and line[:1] in (" ", "\t") and line.strip():
            cur[1] += " " + line.strip()
        else:
            cur = None
    found = []
    for did, what in out:
        day = _YYMMDD.search(what)
        found.append((_yymmdd(day) if day else "", did, re.sub(r"\s+", " ", what.replace(chr(96), "")).strip()))
    return found


def _session_day(name: str, md: Path | None) -> str:
    """A session's day: pNN-<MMDD> with the year its notes give it, else the latest year not ahead of today;
    an older chat/ session by the date in its name."""
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", name)
    if m:
        return "-".join(m.groups())
    m = re.match(r"p\d+-(\d{2})(\d{2})$", name)
    if not m:
        return ""
    text = md.read_text(encoding="utf-8", errors="ignore") if md and md.is_file() else ""
    years = [y.group(1) for y in _YYMMDD.finditer(text) if (y.group(2), y.group(3)) == m.groups()]
    if years:
        return f"20{years[0]}-{m.group(1)}-{m.group(2)}"
    today = datetime.date.today()
    try:
        day = datetime.date(today.year, int(m.group(1)), int(m.group(2)))
    except ValueError:
        return ""
    return (day if day <= today else day.replace(year=today.year - 1)).isoformat()


def timeline_events(block: Path, root: Path) -> tuple:
    """(events, undated): every dated thing of the Block's Studio topics, newest first. An event is a dict
    of day, key (the topic's row key under the group bar), name, anchor, tags (its groups), kind (decided ·
    session · drawing) and its html."""
    block, root = block.resolve(), root.resolve()
    events, undated = [], []
    for source, topic, drawings in studio_inventory(block, root):
        name = topic.name if topic.is_dir() else topic.stem
        base = {"key": topic.relative_to(block).as_posix(), "name": name, "anchor": studio_anchor(topic, source, block),
                "tags": _note_facts(_notes(topic))["tags"]}
        for day, did, what in _decisions(_notes(topic)):
            if not day:
                undated.append(did)
                continue
            short = what if len(what) <= 150 else what[:149].rsplit(" ", 1)[0] + " …"
            events.append(dict(base, day=day, kind="decided",
                               html=f'<b>{_e(did)}</b> <span title="{_e(what)}">{_e(short)}</span>'))
        for s in _sessions(topic, source):
            md = s["path"] if s["path"].is_file() else None
            day = _session_day(s["name"], md)
            if day:
                events.append(dict(base, day=day, kind="session",
                                   html=pop(_reader(s["path"], root), f'{name} · {s["name"]}', f'{s["name"]} · {s["title"]}')
                                   if md else _e(f'{s["name"]} · {s["title"]}')))
        for d in drawings:
            by_day = {}
            for day, what in _drawing_notes(d):
                by_day.setdefault(day, []).append(what)
            for day, whats in by_day.items():
                events.append(dict(base, day=day, kind="drawing", n=len(whats),
                                   html=f'{pop(_draw_url(d, root), d.stem, d.stem + " ↗")} '
                                        f'{_e(" · ".join(dict.fromkeys(w for w in whats if w)))}'))
    order = {"decided": 0, "session": 1, "drawing": 2}
    events.sort(key=lambda e: (e["name"], order[e["kind"]]))
    events.sort(key=lambda e: e["day"], reverse=True)          # newest day first, topics in sNN order
    return events, undated


TIMELINE_LEVELS = ("Days", "Topics", "Everything")
TIMELINE_KINDS = (("decided", "decided", "decided"), ("session", "session", "sessions"), ("drawing", "note", "notes"))


def studio_timeline(block: Path, root: Path) -> str:
    """The Studio's fifth folding part, Timeline, under Runs (b10 s08; JL 261011: "add another section of
    the Timeline", "a real timelne ... very concise ... with a axis down", "up to down", "different level of
    details", then "it is not that beautiful ... like using the visualization tools"): time runs down one
    axis, the oldest day at the top. Days, the default, is a chart: a row per day, a column per topic, a
    bubble sized by how much that topic moved that day, and the day's total as a bar. Topics turns each day
    into a line per topic with a stacked bar of its kinds; Everything adds each decision, session and note.
    The chart's columns are the topic groups (the group bar's, in its order, Untagged last) or the topics
    (JL 261011: "the columns can also be the topic groups"); a group's bubble adds up its topics, so a
    topic in two groups counts in both, and the day's bar still counts each change once."""
    events, _ = timeline_events(block, root)
    days, topics = {}, {}
    for e in sorted(events, key=lambda e: e["day"]):          # oldest first; topics stay in sNN order
        days.setdefault(e["day"], {}).setdefault(e["key"], []).append(e)
    try:                       # every day from the first to the last, the quiet ones too: a real axis (JL 261012:
        first, last = (datetime.date.fromisoformat(d) for d in (min(days), max(days)))   # "show the days between them")
        span = [(first + datetime.timedelta(i)).isoformat() for i in range((last - first).days + 1)]
        days = {day: days.get(day, {}) for day in span}
    except ValueError:
        pass
    for e in sorted(events, key=lambda e: e["name"]):
        topics.setdefault(e["key"], (e["name"], e["anchor"]))
    years = {day[:4] for day in days}
    tags = {}
    for e in events:
        tags.setdefault(e["key"], e.get("tags") or [])
    groups, loose = {}, [k for k in topics if not tags.get(k)]
    for name in studio_group_order(block) + sorted({g for gs in tags.values() for g in gs}, key=str.casefold):
        groups.setdefault(name.casefold(), (name, []))
    for k in topics:
        for g in tags.get(k) or []:
            groups[g.casefold()][1].append(k)
    groups = {g: v for g, v in groups.items() if v[1]}
    if loose:
        groups["__untagged__"] = ("Untagged", loose)

    def size(items: list) -> int:
        return sum(e.get("n", 1) for e in items)

    def tally(items: list) -> dict:
        return {k: sum(e.get("n", 1) for e in items if e["kind"] == k) for k, _, _ in TIMELINE_KINDS}

    def says(items: list) -> str:
        t = tally(items)
        return " · ".join(f"{t[k]} {one if t[k] == 1 else many}" for k, one, many in TIMELINE_KINDS if t[k])

    def label(day: str) -> str:
        try:
            return datetime.date.fromisoformat(day).strftime("%a %d %b" + (" %Y" if len(years) > 1 else ""))
        except ValueError:
            return day

    def sid(name: str) -> str:
        m = re.match(r"s\d+", name)
        return m.group(0) if m else name

    cell_peak = max((size(items) for ts in days.values() for items in ts.values()), default=1)
    day_peak = max((size([e for items in ts.values() for e in items]) for ts in days.values()), default=1)
    group_peak = max((sum(size(ts[k]) for k in ks if k in ts) for ts in days.values() for _, ks in groups.values()),
                     default=1) or 1
    cols = "groups" if any(g != "__untagged__" for g in groups) else "topics"
    ghead = "".join(f'<button type=button class=tl-gcol data-tl-group="{_e(g)}" title="{_e(n)}: '
                    f'{_e(" · ".join(sid(topics[k][0]) for k in ks))}">'
                    f'{"" if g == "__untagged__" else _e(group_emoji(n)) + " "}{_e(n)}</button>'
                    for g, (n, ks) in groups.items())
    # Days: the chart, a row per day down the axis and a column per topic
    # a topic's column carries its full name (JL 261012: "for the sNN, here could you give it the full name?"):
    # the sNN straight and bold over the column, the rest slanted up above it; columns 60 px wide (JL 261012:
    # "make the columns width wider, and make the sNN to be more readable"). The header fits the longest name
    head = "".join(f'<a class=tl-col data-tl-key="{_e(k)}" href="#{_e(a)}" title="{_e(n)}"><b>{_e(sid(n))}</b>'
                   f'<span>{_e(n[len(sid(n)):].lstrip("-_ "))}</span></a>' for k, (n, a) in topics.items())
    slant = min(round(max((len(n) - 4 for n, _ in topics.values()), default=0) * 7.2 * 0.71) + 40, 200)
    chart = []
    for day, ts in days.items():
        cells, n_day = [], 0
        for k, (n, a) in topics.items():
            items = ts.get(k)
            if not items:
                cells.append(f'<span class=tl-cell data-tl-key="{_e(k)}"></span>')
                continue
            n_day += size(items)
            px = round(8 + 18 * (size(items) / cell_peak) ** 0.5)
            cells.append(f'<span class=tl-cell data-tl-key="{_e(k)}" data-tl-count={size(items)}>'
                         f'<a class=tl-b href="#{_e(a)}" style="--s:{px}px" '
                         f'title="{_e(n)} · {_e(label(day))} · {_e(says(items))}"></a></span>')
        for g, (gname, ks) in groups.items():
            parts = {k: size(ts[k]) for k in ks if k in ts}
            n_g = sum(parts.values())
            ball = (f'<button type=button class=tl-gb style="--s:{round(8 + 22 * (n_g / group_peak) ** 0.5)}px" '
                    f'title="{_e(gname)} · {_e(label(day))} · {n_g} changes: '
                    f'{_e(" · ".join(f"{sid(topics[k][0])} {v}" for k, v in parts.items()))}"></button>' if n_g else "")
            cells.append(f'<span class=tl-gcell data-tl-group="{_e(g)}" data-tl-parts="{_e(json.dumps(parts))}">{ball}</span>')
        chart.append(f'<div class="tl-mrow{"" if ts else " tl-quiet"}" data-day="{_e(day)}"><time datetime="{_e(day)}">{_e(label(day))}</time>'
                     f'<span class=tl-dot></span>{"".join(cells)}<span class=tl-bar><span class=tl-track>'
                     f'<i style="width:{round(n_day / day_peak * 100)}%"></i></span><b>{n_day}</b></span></div>')
    # Topics and Everything: a line per topic under its day, a stacked bar of its kinds, then its items
    days_html = []
    for day, ts in days.items():
        lines = []
        for k, items in ts.items():
            n, a = topics[k]
            t = tally(items)
            stack = "".join(f'<i class=k-{kind} style="flex:{t[kind]}"></i>' for kind, _, _ in TIMELINE_KINDS if t[kind])
            lis = "".join(f'<li><i class="tl-kd k-{e["kind"]}" title="{dict((k_, o) for k_, o, _ in TIMELINE_KINDS)[e["kind"]]}">'
                          f'</i>{e["html"]}</li>' for e in items)
            lines.append(f'<div class=tl-topic data-tl-key="{_e(k)}" data-tl-count={size(items)}>'
                         f'<a class=tl-name href="#{_e(a)}" title="{_e(n)}"><b>{_e(sid(n))}</b>'
                         f'<span>{_e(n[len(sid(n)):].lstrip("-_ "))}</span></a>'
                         f'<span class=tl-meter title="{_e(says(items))}"><span class=tl-stack style="width:'
                         f'{max(round(size(items) / cell_peak * 240), 6)}px">{stack}</span><span class=tl-n>{size(items)}</span>'
                         f'</span><ul class=tl-items>{lis}</ul></div>')
        days_html.append(f'<li class="tl-day{"" if ts else " tl-quiet"}" data-day="{_e(day)}"><time datetime="{_e(day)}">{_e(label(day))}</time>'
                         f'<div class=tl-body>{"".join(lines)}</div></li>')
    levels = "".join(f'<button type=button data-tl-level={lv.lower()} aria-pressed={"true" if lv == "Days" else "false"}>'
                     f'{lv}</button>' for lv in TIMELINE_LEVELS)
    keys = "".join(f'<i class="tl-kd k-{kind}"></i>{one}' for kind, one, _ in TIMELINE_KINDS)
    # undated decisions are not listed (JL 261012: "I don't want this"); timeline_events still returns them
    body = (f'<div class=tl-wrap data-level=days><nav class=tl-levels aria-label="How much the Timeline shows">{levels}'
            f'<span class="tl-cols tl-legend-b">columns <button type=button data-tl-cols=groups aria-pressed='
            f'{"true" if cols == "groups" else "false"}>by group</button><button type=button data-tl-cols=topics '
            f'aria-pressed={"true" if cols == "topics" else "false"}>by topic</button></span>'
            f'<span class="tl-help tl-legend-b">a bubble: how much moved that day · click a group for its topics, '
            f'a topic to read it</span><span class="tl-help tl-legend-k">{keys}</span></nav>'
            # the group bar's groups again, here, so a group is picked without scrolling up (JL 261012:
            # "我这怎么选其他的？比如说 group 呢，或者说 topic 呢？"); the page script fills it from the bar
            f'<nav class=tl-groups aria-label="Pick a topic group"></nav>'
            f'<div class=tl-map data-cols={cols} style="--tl-slant:{slant}px"><div class=tl-mhead><span></span><span></span>{head}{ghead}'
            f'<span class=tl-bar-h>changes</span>'
            f'</div>{"".join(chart)}</div><div class=tl-picked></div>'
            f'<ol class="tl-axis tl-list">{"".join(days_html)}</ol></div>' if days else
            '<p class=mut>Nothing dated yet: a decision gets its date in brackets, (JL 261011).</p>')
    return (f'<details class="studio-related studio-timeline" id=studio-timeline>'
            f'<summary><b>Timeline</b></summary>'                # no counts (JL 261011: "I don't need this")
            f'<div class=related-in>{body}</div></details>')


FOLDER_SKIP = {"__pycache__", "node_modules", ".ipynb_checkpoints"}
# what a folder of a Block holds, for the names every Block shares (haipipe-block); any other folder says its face's title
FOLDER_WORDS = {"studio": "the Studio: a folder per topic", "reports": "the Questions: a folder each, with its report",
                "runs": "the Runs: a folder each", "related": "what came in from outside, kept as it came",
                "delivery": "what was built to send", "passes": "the sessions, one folder each",
                "result": "what the Run produced", "history": "older copies, kept"}
FILE_ICONS = {".md": "📝", ".excalidraw": "✏️", ".png": "🖼️", ".jpg": "🖼️", ".jpeg": "🖼️", ".gif": "🖼️", ".svg": "🖼️",
              ".webp": "🖼️", ".pdf": "📕", ".py": "🐍", ".ipynb": "📓", ".yaml": "⚙️", ".yml": "⚙️", ".json": "🧾",
              ".csv": "📊", ".tsv": "📊", ".parquet": "📊", ".sh": "▶️", ".docx": "📘", ".pptx": "📙", ".eml": "✉️",
              ".tex": "📜", ".bib": "📚", ".html": "🌐", ".txt": "📄", ".log": "📄"}


def _when(t: float) -> str:
    d = datetime.datetime.fromtimestamp(t)
    return d.strftime("%d %b" if d.year == datetime.date.today().year else "%d %b %Y")


def _shown(p: Path) -> bool:
    return not p.name.startswith(".") and p.name not in FOLDER_SKIP


def _run_word(folder: Path) -> str:
    """A Run folder's one line from its card: `soft · draw · done · 10 passes`; '' without run.yaml."""
    try:
        card = (folder / "run.yaml").read_text(encoding="utf-8", errors="ignore")[:4000]
    except OSError:
        return ""
    get = lambda k: (re.search(rf"(?m)^{k}:[ \t]*(.+)$", card) or [None, ""])[1].strip()
    n = len(re.findall(r"(?m)^- p\d+-", card))
    return " · ".join(x for x in (get("kind"), get("type").strip("[]").replace(",", " +"), get("status"),
                                  f"{n} pass{'es' if n != 1 else ''}" if n else "") if x and x != "null")


def folder_word(p: Path) -> str:
    """What a folder is for, in one line: a shared name's fixed line, a Run's card, else its face's title; '' when
    that would only repeat the folder's name (b10 s09-D13)."""
    word = FOLDER_WORDS.get(p.name) or _run_word(p)
    if not word and (md := face(p)):
        word = _title(md)
    return "" if word == p.name else word


def folder_rows(folder: Path, root: Path, most: int | None = 300) -> str:
    """One folder's rows for Studio › Folder (b10 s09): its folders first, then its files, by name. A folder
    folds, says how many things it holds and what it is for, and its rows load when it is opened
    (`?view=dir&path=`), so a Block of thousands of files stays light (b00_rawdata: 5,317). A file opens in the
    pop-out and says its size and the day it last changed. Past `most` rows, a button loads the rest (None:
    all). Dotfiles and caches are left out, and a link that leaves the root is named but not followed."""
    try:
        kids = sorted((p for p in folder.iterdir() if _shown(p)), key=lambda p: (not p.is_dir(), p.name.casefold()))
    except OSError:
        return '<li class=mut>This folder could not be read.</li>'
    rows, top = [], root.resolve()
    for p in kids[:most]:
        if not p.resolve().is_relative_to(top):
            rows.append(f'<li class=fd-file><span class=fd-row><span class=fd-i>🔗</span>{_e(p.name)}'
                        f'<span class=fd-n>a link outside this root</span></span></li>')
            continue
        rel = _rel(p, root)
        if p.is_dir():
            try:
                n = sum(1 for c in p.iterdir() if _shown(c))
            except OSError:
                n = 0
            word = folder_word(p)
            rows.append(f'<li class=fd-dir><details data-dir="{_e(rel)}"><summary class=fd-row title="{_e(rel)}/">'
                        f'<span class=fd-name>{_e(p.name)}/</span><span class=fd-n>{n}</span>'
                        + (f'<span class=fd-word>{_e(word)}</span>' if word else "") + '</summary><ul></ul></details></li>')
            continue
        try:
            st = p.stat()
        except OSError:
            continue
        href = _draw_url(p, root) if p.suffix == ".excalidraw" else _file_url(p, root)
        rows.append(f'<li class=fd-file><span class=fd-row title="{_e(rel)}"><span class=fd-i>'
                    f'{FILE_ICONS.get(p.suffix.lower(), "📄")}</span>{pop(href, p.name)}'
                    f'<span class=fd-n>{_size(st.st_size)}</span><span class=fd-when>{_when(st.st_mtime)}</span></span></li>')
    if most is not None and len(kids) > most:
        rows.append(f'<li class=fd-more><button type=button data-dir="{_e(_rel(folder, root))}">'
                    f'Show the other {len(kids) - most}</button></li>')
    return "".join(rows) or '<li class=mut>Empty.</li>'


def studio_folder(block: Path, root: Path) -> str:
    """The Studio's sixth folding part, Folder, under Timeline (b10 s09-block-folder; JL 261012: "在 related 和 timeline 下面
    再搞一个 folder，这样我就可以看到这些 folder 里面（也就是这个 block 的 folder）都长什么内容"): the Block's own
    folder as a tree. Its first level is drawn here; each folder's rows load when it is opened."""
    rel = _rel(block, root)
    return (f'<details class="studio-related studio-folder" id=studio-folder><summary><b>Folder</b></summary>'
            f'<div class=related-in><p class=fd-root>{_e(rel)}/</p>'
            f'<ul class=fd-tree>{folder_rows(block, root)}</ul></div></details>')


# ── Studio › Runs: every Task's hard Runs and their status, the fourth folding part (JL 261019) ───────────
_HARD_RUN = re.compile(r"^r\d{2,3}_")
_RUN_SKIP = {"history", "_old", "_archive", "results", "result", "node_modules"}
RUN_MARK = {"complete": "✅", "completed": "✅", "done": "✅", "failed": "❌", "error": "❌", "blocked": "🟧",
            "running": "▶️", "queued": "⏳", "queued_conditional": "⏳", "planned": "⬜", "not run": "⬜",
            "no receipt": "⬜"}


def _receipt(paths) -> tuple:
    """(status, when) from the first of these files that names a status: a finished Run its finish day; a running
    one when it started and its `progress:` line, when its runner writes one (JL 261019: "show the current run
    progress"); none of them, no receipt on this machine (it may have run elsewhere, so never "not run")."""
    for p in paths:
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        m = re.search(r"(?m)^status:\s*['\"]?([A-Za-z_ ]+?)['\"]?\s*$", text)
        if m and m.group(1).strip() not in ("null", "None", ""):
            status = m.group(1).strip()
            if status == "running":
                since = re.search(r"(?m)^started_at:\s*['\"]?\d{4}-(\d{2}-\d{2})[T ](\d{2}:\d{2})", text)
                done = re.search(r"(?m)^progress:\s*['\"]?([^'\"\n]+)", text)
                return status, " · ".join(x for x in (since and f"since {since.group(1)} {since.group(2)}",
                                                     done and done.group(1).strip()) if x)
            day = re.search(r"(?m)^finished_at:\s*['\"]?(\d{4}-\d{2}-\d{2})", text)
            return status, day.group(1) if day else ""
    return "no receipt", ""


def _run_status(run: Path) -> tuple:
    """(status, when) of one hard Run folder: its result's receipt first, else its card."""
    return _receipt((run / "result/runtime.yaml", run / "run.yaml"))


def hard_runs(block: Path) -> list:
    """[(job, task, run, status, day)] for every hard Run (runs/rNN_*) of every Task under the Block, in folder order;
    soft Runs (run-*) and history copies are left out. A Run is a folder, or in the older flat layout a ticket
    runs/rNN_*.sh with its receipt in the Task's results/rNN_*/ or the Job's results/<task>/rNN_*/ (Proj11 b01)."""
    out = []
    def walk(d: Path, job: str, depth: int) -> None:
        if depth > 6:
            return
        try:
            kids = sorted(p for p in d.iterdir() if p.is_dir() and p.name not in _RUN_SKIP and not p.name.startswith("."))
        except OSError:
            return
        for k in kids:
            if k.name == "runs":
                seen = set()
                for r in sorted(p for p in k.iterdir() if _HARD_RUN.match(p.name)):
                    name = r.name if r.is_dir() else r.stem if r.suffix == ".sh" else ""
                    if not name or name in seen:
                        continue
                    seen.add(name)
                    out.append((job, d.name, name, *(_run_status(r) if r.is_dir() else _receipt((
                        d / "results" / name / "runtime.yaml", d.parent / "results" / d.name / name / "runtime.yaml")))))
            elif re.match(r"^[jt]\d{2}", k.name) or depth == 0:
                walk(k, k.name if k.name[:1] == "j" and depth <= 1 else job, depth + 1)
    walk(block, "", 0)
    return out


def runs_tally(rows: list) -> str:
    """The marks of these Runs, counted: `✅12 ⏳4 ⬜35` (the Studio's Runs part and SPACE Home share it)."""
    return _tally(rows)


def run_cells(rows: list) -> str:
    """One Task's hard Runs as the cells of an aligned `rn-grid`: mark · Run · status · finish day (the Studio's
    Runs part and SPACE Home's Job rows share it)."""
    return "".join(f'<span class=rn-mark title="{_e(st)}">{RUN_MARK.get(st, "⬜")}</span><code>{_e(name)}</code>'
                   f'<span class=rn-st>{_e(st)}</span><span class=rn-day>{_e(day)}</span>' for _, _, name, st, day in rows)


def runs_list(rows: list) -> str:
    """Hard Runs as card rows like the Jobs rows (JL 261019, on the bare lists: "they are not in the good format"):
    one folded card per Job, its Task and Run counts and tally on the right; opened, each Task a heading and its
    Runs an aligned table: mark · Run · status · finish day."""
    jobs: dict = {}
    for r in rows:
        jobs.setdefault(r[0] or "(no Job)", {}).setdefault(r[1], []).append(r)
    cards = []
    for job, tasks in jobs.items():
        jrows = [r for rs in tasks.values() for r in rs]
        body = []
        for task, rs in tasks.items():
            body.append(f'<div class=rn-task><b>{_e(task)}</b><span class=rn-meta>{len(rs)} Run{"s" * (len(rs) != 1)}'
                        f'</span><span class=rn-tally>{_tally(rs)}</span></div><div class=rn-grid>{run_cells(rs)}</div>')
        nt, nr = len(tasks), len(jrows)
        cards.append(f'<details class=rn-card><summary><b>{_e(job)}</b><span class=rn-meta>{nt} Task{"s" * (nt != 1)} · '
                     f'{nr} Run{"s" * (nr != 1)}</span><span class=rn-tally>{_tally(jrows)}</span></summary>'
                     f'<div class=rn-body>{"".join(body)}</div></details>')
    return f'<div class=rn-rows>{"".join(cards)}</div>'


RUN_LEGEND = "✅ complete · ❌ failed · 🟧 blocked · ▶️ running, since when · ⏳ queued · ⬜ not run or no receipt here"
RUN_CSS = (".rn-rows{display:grid;gap:6px}.rn-card{border:1px solid var(--line);border-radius:10px;background:var(--bg);overflow:hidden}"
           ".rn-card>summary{display:flex;gap:10px;align-items:baseline;cursor:pointer;padding:8px 12px;list-style:none}"
           ".rn-card>summary::-webkit-details-marker{display:none}.rn-card>summary::before{content:'▸';color:var(--mut)}"
           ".rn-card[open]>summary::before{content:'▾'}.rn-card[open]>summary{border-bottom:1px solid var(--line)}"
           ".rn-card>summary>b{font-size:15px;overflow-wrap:anywhere}.rn-meta{color:var(--mut);font-size:13px}"
           ".rn-tally{margin-left:auto;font:12px/1.4 ui-monospace,Menlo,monospace;white-space:nowrap}"
           ".rn-body{padding:6px 12px 10px 30px}.rn-task{display:flex;gap:10px;align-items:baseline;margin:8px 0 4px}"
           ".rn-task>b{font-size:14px}.rn-grid{display:grid;grid-template-columns:22px minmax(0,1fr) 150px minmax(96px,auto);"
           "column-gap:12px;row-gap:3px;align-items:baseline;margin-left:4px}.rn-grid code{font:13px ui-monospace,Menlo,monospace;"
           "overflow-wrap:anywhere}.rn-st,.rn-day{color:var(--mut);font-size:12px}.rn-day{text-align:right}"
           ".rn-legend{color:var(--mut);font-size:12px;margin:6px 0 0}")


def _tally(rows: list) -> str:
    from collections import Counter
    c = Counter(RUN_MARK.get(r[3], "⬜") for r in rows)
    return " ".join(f"{m}{c[m]}" for m in ("✅", "❌", "🟧", "▶️", "⏳", "⬜") if c[m])


def studio_runs(block: Path, root: Path, theme=None) -> str:
    """The Studio's Runs, under Delivery (JL 261019: "list another one to show the Hard Run, for each task, and just
    show their status"): each Job, each of its Tasks, each hard Run with its mark, status and finish day. Read from
    the Runs' receipts; nothing is written. A Job and a Task each carry their tally."""
    rows = hard_runs(block)
    meta = f"{len(rows)} hard Run{'s' if len(rows) != 1 else ''}" + (f" · {_tally(rows)}" if rows else "")
    if not rows:
        body = _empty_view("No hard Run yet: a Task's executable Runs (runs/rNN_*) list here with their status.")
    else:
        body = runs_list(rows) + f'<p class=rn-legend>{RUN_LEGEND}; read from each Run\'s result/runtime.yaml, else its run.yaml</p>'
    return (f'<details class=studio-related id=studio-runs><summary><b>Runs</b>'
            f'<span class=related-meta>{_e(meta)}</span></summary><div class=related-in>{body}</div></details>')


def _topic_rows(folder: Path, root: Path, words: tuple) -> str:
    """The studio topics whose name holds one of `words`, as Idea Studio draws them; '' when none."""
    return "".join(_topic_row(t, d, root, folder) for t, d in _studio_topics(folder) if any(w in t.name for w in words))


def studio_inventory(folder: Path, root: Path) -> list:
    """One Block list, including existing Job/Task topics until their files are moved.

    Keep each topic's source for its feeds and sessions. Never enter an archive or a link
    outside this Block/root, and count a linked topic only once.
    """
    root, folder = root.resolve(), folder.resolve()
    if folder != root and root not in folder.parents:
        return []
    sources = [folder]
    if level_of(folder) == "Block":
        jobs = children(folder, "Block")
        sources += jobs + children(folder, "Job")
        for job in jobs:
            sources += children(job, "Job")
    out, seen = [], set()
    for source in sources:
        resolved = source.resolve()
        if resolved != folder and folder not in resolved.parents:
            continue
        for topic, drawings in _studio_topics(source):
            actual = topic.resolve()
            if root not in actual.parents or folder not in actual.parents or actual in seen:
                continue
            seen.add(actual)
            drawings = [d for d in drawings if root in d.resolve().parents and folder in d.resolve().parents]
            out.append((source, topic, drawings))
    return out


def studio_anchor(topic: Path, source: Path, block: Path) -> str:
    """Keep Block topic links; qualify older local topics so repeated sNN names stay distinct."""
    prefix = source.relative_to(block).as_posix().replace("/", "--") + "--" if source != block else ""
    return "topic-" + prefix + (topic.name if topic.is_dir() else topic.stem)


_GROUP_BAD = re.compile(r"[`,·|*\n\r\t]")
# A group's emoji comes from its name (JL 261010): the first word of the table found in the name, else a
# fixed pick from the palette, so a new group gets one at once and everyone sees the same. The browser
# reads this same table from the nav's data-studio-emoji to give a group made there its emoji.
GROUP_EMOJI = {
    "current": "🎯", "guide": "🧭", "level": "🪜", "server": "🖥️", "structure": "🏗️", "ui": "🎨",
    "design": "🎨", "workflow": "🔁", "flow": "🔁", "run": "⚙️", "skill": "🛠️", "tool": "🛠️",
    "data": "📊", "model": "🧠", "paper": "📄", "report": "📑", "question": "❓", "idea": "💡",
    "draft": "✏️", "review": "🔍", "test": "🧪", "bug": "🐞", "issue": "🐞", "todo": "📌", "plan": "🗺️",
    "people": "👥", "meeting": "🗓️", "email": "✉️", "delivery": "📦", "method": "🧮", "evidence": "🔎",
    "slide": "🖼️", "chat": "💬", "agent": "🤖", "code": "💻", "focus": "🎯", "archive": "🗄️",
    "当前": "🎯", "指南": "🧭", "层级": "🪜", "服务": "🖥️", "结构": "🏗️", "界面": "🎨", "设计": "🎨",
    "流程": "🔁", "技能": "🛠️", "数据": "📊", "模型": "🧠", "论文": "📄", "报告": "📑", "问题": "❓",
    "想法": "💡", "草稿": "✏️", "测试": "🧪", "计划": "🗺️", "会议": "🗓️", "交付": "📦", "方法": "🧮",
}
GROUP_PALETTE = ("🔷", "🟣", "🟢", "🟠", "🧩", "🔖", "🌱", "📌", "💠", "🪐", "🍀", "🔸")


def group_emoji(label: str) -> str:
    """Pick a group's emoji from its name; the browser's emojiFor() follows the same steps."""
    low = label.lower()
    tokens = [t for t in re.split(r"[ _/&+-]+", low) if t]
    for word, emoji in GROUP_EMOJI.items():
        if word.isascii():
            if any(t == word or (t.endswith("s") and t[:-1] == word) for t in tokens):
                return emoji
        elif word in low:
            return emoji
    return GROUP_PALETTE[sum(ord(c) for c in label) % len(GROUP_PALETTE)]
_GROUP_RESERVED = {"current", "all", "untagged"}


def _set_tags(md: Path, tags: list) -> None:
    """Write a topic's **Tags:** line, placed above **Topic:**; drop it when no tag is left."""
    text = md.read_text(encoding="utf-8")
    line = "**Tags:** " + " · ".join(f"`{t}`" for t in tags) if tags else ""
    found = re.search(r"(?m)^\*\*Tags:\*\*[^\n]*(?:\n|\Z)", text)
    if found:
        end = found.end()
        if not line and re.match(r"[ \t]*\n", text[end:]):
            end += re.match(r"[ \t]*\n", text[end:]).end()
        text = text[:found.start()] + (line + "\n" if line else "") + text[end:]
    elif line:
        topic = re.search(r"(?m)^\*\*Topic:\*\*", text)
        under = re.search(r"(?m)^[=-]{3,}[ \t]*\n", text)
        if topic:
            text = text[:topic.start()] + line + "\n\n" + text[topic.start():]
        elif under:
            text = text[:under.end()] + "\n" + line + "\n" + text[under.end():]
        else:
            text = line + "\n\n" + text
    md.write_text(text, encoding="utf-8")


GROUP_FILE = "_groups.txt"      # studio/_groups.txt, related/_groups.txt: a bar's groups in button order (b10 s02-D17)
# What a group bar sorts: kind -> (its rows are called, its view's name). One bar, one script, one op for both.
GROUP_SHELVES = {"studio": ("topic", "Studio"), "related": ("item", "Related"), "reports": ("question", "Report"),
                 "delivery": ("result", "Delivery")}


def studio_group_order(owner: Path, shelf: str = "studio") -> list:
    """The group names in <shelf>/_groups.txt (studio/ or related/), in order; [] when the file is missing."""
    f = owner / shelf / GROUP_FILE
    if not f.is_file():
        return []
    names, seen = [], set()
    for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
        name = line.strip()
        if name and not name.startswith("#") and name.casefold() not in seen:
            seen.add(name.casefold())
            names.append(name)
    return names


def _write_group_order(owner: Path, names: list, shelf: str = "studio") -> None:
    what = {"studio": "topics are the ones whose **Tags:** line names it",
            "related": "items are the related/related.md rows whose group cell names it",
            "reports": "Questions are the register rows whose group: line names it",
            "delivery": "results are the delivery/result_groups.md rows whose group cell names it"}[shelf]
    (owner / shelf).mkdir(exist_ok=True)
    (owner / shelf / GROUP_FILE).write_text(
        f"# {shelf.title()} groups of this level, in button order. The workbench writes this file when a group is\n"
        f"# made, moved or deleted; a group's {what}.\n"
        + "".join(n + "\n" for n in names), encoding="utf-8")


def _group_members(owner: Path, root: Path, kind: str) -> dict:
    """key -> (name, groups, write) for what a group bar sorts: the Studio's topics (their **Tags:** line) or
    the Block's related items (their row's group cell) or a level's Questions (their register group: line, after
    the theme's fixed groups); write(groups) returns (groups read back, error)."""
    out = {}
    if kind == "reports":
        md, theme = face(owner), themes().get(theme_of(owner, root), VANILLA)
        for row in _register(md):
            qid, fixed = str(row["id"]), _theme_fixed(theme, row, owner)

            def write(new, qid=qid, fixed=fixed):
                drop = {g.casefold() for g in fixed}
                _register_set_groups(md, qid, [g for g in new if g.casefold() not in drop])
                back = next((r for r in _register(md) if str(r["id"]) == qid), {})
                return _split_tags(",".join(fixed + [str(back.get("group") or "")])), None
            out[qid] = (qid, _split_tags(",".join(fixed + [str(row.get("group") or "")])), write)
        return out
    if kind == "delivery":                    # a result's file kinds are fixed; a person's groups in result_groups.md
        for item in delivery_items(owner):
            def write(new, item=item):
                _delivery_set_groups(owner / "delivery", item["key"], [g for g in new if g not in item["fixed"]])
                back = next((i for i in delivery_items(owner) if i["key"] == item["key"]), item)
                return back["groups"], None
            out[item["key"]] = (item["title"], item["groups"], write)
        return out
    if kind == "related":
        for item in related_items(owner):
            def write(new, item=item):
                _related_set_groups(owner, item, new)
                return next((i["groups"] for i in related_items(owner) if i["key"] == item["key"]), []), None
            out[item["key"]] = (item["title"], item["groups"], write)
        return out
    for _, topic, _ in studio_inventory(owner, root):
        md = _notes(topic)

        def write(new, topic=topic, md=md):
            if md is None:
                return None, f"{topic.name} has no notes file to hold its groups."
            _set_tags(md, new)
            return _note_facts(md)["tags"], None
        out[topic.relative_to(owner).as_posix()] = (topic.name, _note_facts(md)["tags"], write)
    return out


def studio_group_op(root: Path, p: dict) -> tuple:
    """Add a row to a group, take it out, or delete the group from every row: the Studio's topics, or with
    `kind: related` the Block's related items (JL 261011: Related's groups work like the Studio's).

    A group is a tag saved on disk beside what it sorts (a topic's **Tags:** line, a related row's group
    cell), so every person and agent sees the same groups (b10 s02-D16). Returns (result, error).
    """
    root = Path(root).resolve()
    owner = (root / str(p.get("path") or "").lstrip("/")).resolve()
    if (owner != root and root not in owner.parents) or not owner.is_dir():
        return None, "No such folder under this root."
    kind = str(p.get("kind") or "studio")
    if kind not in GROUP_SHELVES:
        return None, "kind must be studio, related, reports or delivery."
    op, tag = p.get("op"), str(p.get("tag") or "").strip()
    if op not in ("add", "remove", "delete", "create", "order"):
        return None, "op must be add, remove, delete, create or order."
    bad = lambda name: not name or len(name) > 30 or _GROUP_BAD.search(name) or name.casefold() in _GROUP_RESERVED
    rule = "A group name is 1 to 30 characters, without ` , · | or *, and is not Current, All or Untagged."
    order = studio_group_order(owner, kind)
    if op == "order":                       # the buttons' new order; a name left out keeps its place at the end
        wanted = [str(n).strip() for n in (p.get("groups") or []) if isinstance(n, str)]
        if any(bad(n) for n in wanted):
            return None, rule
        keys = {n.casefold() for n in wanted}
        names = list(dict.fromkeys(wanted)) + [n for n in order if n.casefold() not in keys]
        _write_group_order(owner, names, kind)
        return {"order": names}, None
    if bad(tag):
        return None, rule
    if op == "create":
        if tag.casefold() not in {n.casefold() for n in order}:
            order.append(tag)
            _write_group_order(owner, order, kind)
        return {"order": order}, None
    members, (noun, label) = _group_members(owner, root, kind), GROUP_SHELVES[kind]
    if op == "delete":
        picked = list(members)
    elif str(p.get("topic") or "") in members:
        picked = [str(p.get("topic"))]
    else:
        return None, f"That {noun} is not in this {label}."
    key, out, changed = tag.casefold(), {}, 0
    for k in picked:
        name, tags, write = members[k]
        has = any(t.casefold() == key for t in tags)
        if op == "add" and not has:
            new = tags + [tag]
        elif op != "add" and has:
            new = [t for t in tags if t.casefold() != key]
        else:
            if op != "delete":                      # nothing to change; report its groups as they are
                out[k] = tags
            continue
        after, err = write(new)
        if err:
            return None, err
        if op != "add" and any(t.casefold() == key for t in after):
            return None, (f"{name}: that group is its subfolder, related/{tag}/; it changes only when the file "
                          "moves." if kind == "related" else
                          f"{name}: {tag} is fixed by the theme (s05-D06); it cannot be taken out here."
                          if kind == "reports" else
                          f"{name}: {tag} is its file kind; it cannot be taken out." if kind == "delivery" else
                          f"{name}: that group comes from a **Type:** line; change it in the notes.")
        out[k] = after
        changed += 1
    if op == "delete" and any(n.casefold() == key for n in order):
        _write_group_order(owner, [n for n in order if n.casefold() != key], kind)
    return {"changed": changed, "topics": out}, None


def group_list(owner: Path, root: Path, kind: str, tag_lists: list, listing: str, picker: str = "",
               add: str = "", starting: tuple = (), fixed: tuple = ()) -> str:
    """A list under its group bar, the Studio's topics, Related's items or a Report's Questions (b10 s02-D16,
    D17; Related and Report JL 261011): Current first (kept in the browser), then each group with its count, in
    <kind>/_groups.txt order, then `starting` (a theme's groups, shown even empty), then the rest, Untagged,
    + Group. No group picked shows every row (no All button, JL 261010). `tag_lists` holds each row's groups;
    the page script drives the bar. A group in `fixed` (the theme's, read off the Question) and one in `starting`
    (the theme's suggested ones) each take their own colour, a Block's own stays white (b10 s05-D16, JL 261012:
    "for each group ... the fixed groups (or the suggested default group labels) ... give them different colors")."""
    noun, label = GROUP_SHELVES[kind]
    counts, untagged = {}, 0
    for tags in tag_lists:
        untagged += not tags
        for tag in tags:
            key = tag.casefold()
            name, count = counts.get(key, (tag, 0))
            counts[key] = (name, count + 1)
    options = [("__current__", "Current", 0)]
    for name in studio_group_order(owner, kind) + list(fixed) + list(starting):   # saved order, then the theme's; empty kept
        if any(key == name.casefold() for key, _, _ in options):
            continue
        name, count = counts.pop(name.casefold(), (name, 0))
        options.append((name.casefold(), name, count))
    if kind == "reports":                                  # a name the Studio uses too keeps the Studio's order (s05-D08)
        for name in studio_group_order(owner if level_of(owner) == "Block" else (_block_above(owner) or owner)):
            if name.casefold() in counts:
                name, count = counts.pop(name.casefold())
                options.append((name.casefold(), name, count))
    options += [(key, name, count) for key, (name, count) in sorted(counts.items())]
    if untagged:
        options.append(("__untagged__", "Untagged", untagged))

    def icon(key: str, name: str) -> str:
        return "" if key == "__untagged__" else f'<span class=grp-emoji aria-hidden=true>{group_emoji(name)}</span>'

    fixed_keys = {g.casefold() for g in fixed}
    suggested = {g.casefold() for g in starting} - fixed_keys

    def group_button(key: str, name: str, count: int) -> str:
        cls, why = ("tab grp-fixed", ' title="Fixed by the theme: it comes from the Question itself"') \
            if key in fixed_keys else ("tab grp-suggested", ' title="Suggested by the theme: shown even when empty"') \
            if key in suggested else ("tab", "")
        button = (f'<button type=button class="{cls}"{why} data-studio-label="{_e(name)}" '
                  f'data-studio-tag="{_e(key)}" aria-pressed="false">{icon(key, name)}{_e(name)} <span class=tag-count>{count}</span></button>')
        if key in ("__current__", "__untagged__") or key in fixed_keys:    # a fixed group cannot be deleted
            return button
        # a group is a tag: × deletes it from every row, the rows stay (b10 s02-D16)
        return (f'<span class=grp>{button}<button type=button class=grp-x data-studio-delete="{_e(key)}" '
                f'title="Delete group {_e(name)}" aria-label="Delete group {_e(name)}">×</button></span>')

    buttons = "".join(group_button(*option) + ("<span class=bar></span>" if option[0] == "__current__" else "")
                      for option in options)
    new_group = (f'<button type=button class=grp-new title="Make a new group, then drag {noun}s onto it">+ Group</button>'
                 '<span class=grp-form hidden><input type=text maxlength=30 placeholder="Group name" '
                 'aria-label="New group name"><button type=button class=grp-ok>Add</button>'
                 '<button type=button class=grp-cancel>Cancel</button></span>')
    table = json.dumps({"words": GROUP_EMOJI, "palette": GROUP_PALETTE}, ensure_ascii=False)
    filters = (f'<nav class="row studio-filters" aria-label="{label} {noun} groups" data-studio-emoji="{_e(table)}">'
               f'{buttons}{new_group}</nav>')
    where = {"studio": "each topic's notes", "related": "the group column of related/related.md",
             "reports": "each Question's group: line in the face's ## Questions",
             "delivery": "delivery/result_groups.md"}[kind]
    kinds = " ".join(w for w, on in (("<span class=\"grp-key grp-fixed\">gray</span>: fixed by the theme;", fixed_keys),
                                      ("<span class=\"grp-key grp-suggested\">amber</span>: suggested by the theme, "
                                       "shown even when empty;", suggested)) if on)
    help_ = (f'<p class="mut studio-help">Every {noun} shows until you pick a group; pick it again to see them all. '
             f'Drag a{"n" if noun[0] in "aeiou" else ""} {noun} by ⋮⋮ onto a group; drag a group sideways to move it. '
             f'Groups are saved in {_e(where)}; Current is saved in this browser.'
             + (f' {kinds} white: added here.' if kinds else '') + '</p>')
    empty = '<p class="mut studio-empty" hidden>This group is empty.</p>'
    status = '<p class="mut studio-status" role=status aria-live=polite></p>'
    marks = "" if kind == "studio" else f' data-group-kind={kind} data-group-noun={noun}'
    return (f'<div class=studio-topics data-studio-owner="{_e(_rel(owner, root))}"{marks}>{filters}'
            f'{picker}{help_}{status}{empty}{listing}{add}</div>')


def studio_cards(folder: Path, root: Path) -> str:
    """The Studio's topic rows under their group bar (group_list); sNN is a topic, never a group."""
    folder, root = folder.resolve(), root.resolve()
    topics = studio_inventory(folder, root)
    own = [(t, d) for source, t, d in topics if source == folder]
    last = max([int(m.group(1)) for t, _ in own for m in [re.match(r"s(\d+)", t.name)] if m] or [0])
    add = f'<p class="mut add">+ Add topic → studio/s{last + 1:02d}-&lt;topic&gt;/</p>'
    rows = "".join(_topic_row(t, d, root, source, shared=folder) for source, t, d in topics)
    sources = dict.fromkeys(source for source, _, _ in topics)
    picker = ""
    if len(sources) > 1:
        choices = ''.join(f'<option value="{_e(source.relative_to(folder).as_posix() if source != folder else "")}">'
                          f'{_e(short_name(source.name) if source != folder else "Block")}</option>' for source in sources)
        picker = ('<label class=studio-source>Source <select aria-label="Studio source" data-studio-source-filter>'
                  '<option value="__all__">All sources</option>' + choices + '</select></label>')
    return group_list(folder, root, "studio", [_note_facts(_notes(t))["tags"] for _, t, _ in topics],
                      rows or '<p class=mut>No studio topics yet.</p>', picker, add)


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
        card = run / "run.yaml"                 # its own status (waiting, held …); "done" only when it has no card
        status = _yaml_scalar(card.read_text(encoding="utf-8", errors="ignore"), "status") if card.is_file() else ""
        rows.append({"run_id": f"run-draw-{sid}", "status": status or "done", "target": topic.name,
                     "_display": f"run-draw-{sid}", "_of": f"studio topic {topic.name} · {what}",
                     "result": _rel(run if run.is_dir() else sessions[0]["path"].parent, root),
                     "result_path": str(run / "passes" if run.is_dir() else sessions[0]["path"].parent)})
    return rows


# ── Audience Report: one row per Question, Logic │ Work │ Report (b10 s02-D25) ──────────────
def _register_set_groups(md: Path, qid: str, groups: list) -> None:
    """Write a Question's groups into its register row's `group:` line (b10 s05-D05): the line replaced, or
    added after the row's `title:` (else after its `id:`); no groups, no line. Only that line changes; the rest
    of the face stays as written."""
    text = md.read_text(encoding="utf-8")
    m = re.search(r"(?ms)^## Questions[ \t]*\n.*?```ya?ml\n(.*?)```", text)
    if not m:
        raise ValueError(f"{md.name} has no ## Questions register")
    lines = m.group(1).split("\n")
    start = next((i for i, ln in enumerate(lines)
                  if re.match(rf"""^\s*-\s+id:\s*['"]?{re.escape(qid)}['"]?\s*$""", ln)), None)
    if start is None:
        raise ValueError(f"{qid} is not in the register of {md.name}")
    dash = len(lines[start]) - len(lines[start].lstrip())
    indent = lambda ln: len(ln) - len(ln.lstrip())
    end = next((i for i in range(start + 1, len(lines)) if lines[i].strip() and indent(lines[i]) <= dash), len(lines))
    pad = " " * next((indent(lines[i]) for i in range(start + 1, end) if lines[i].strip()), dash + 2)
    value = ", ".join(groups)
    if re.search(r"""[:#\[\]{}&*!|>'"%@`]""", value) or value[:1] in "-?":
        value = json.dumps(value, ensure_ascii=False)
    at = next((i for i in range(start + 1, end) if lines[i].startswith(pad + "group:")), None)
    if at is not None:
        if groups:
            lines[at] = f"{pad}group: {value}"
        else:
            del lines[at]
    elif groups:
        after = next((i for i in range(start + 1, end) if lines[i].startswith(pad + "title:")), start)
        while after + 1 < end and lines[after + 1].strip() and indent(lines[after + 1]) > len(pad):
            after += 1                                    # past a title that wraps
        lines.insert(after + 1, f"{pad}group: {value}")
    md.write_text(text[:m.start(1)] + "\n".join(lines) + text[m.end(1):], encoding="utf-8")


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


def _answer_ids(md: Path | None) -> set:
    """The Question ids a face's `answers:` line names, lowercased; a need `<id>.E<n>` counts as its id."""
    m = re.search(r"(?m)^answers:\s*(.+)$", md.read_text(encoding="utf-8", errors="ignore")) if md else None
    return {re.sub(r"(?i)\.E\d+$", "", w.strip()).lower() for w in re.split(r"[,\s\[\]]+", m.group(1)) if w.strip()} \
        if m else set()


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


def _studio_links(page: Path) -> list:
    """(link text, drawing) for each link in a report Page to a drawing under a studio/ folder, in order."""
    out = []
    for name, href in re.findall(r"\[([^\]]+)\]\(([^)\s]+\.excalidraw)\)", page.read_text(encoding="utf-8", errors="ignore")):
        p = (page.parent / href).resolve()
        if "studio" in p.parts and p.is_file():
            out.append((name, p))
    return out


def _report_cell(qid: str, page: Path | None, root: Path, work: str = "") -> str:
    """The Report cell: the title (the Page in the pop-out), its answer line, then the work behind it (`work`, the
    Jobs, Tasks and Runs on this Question; b10 s32-D23, JL 261012: "the logic and report (which contains the work
    as well)"), its one drawing embedded live (view only, fitted to the box, loaded as it scrolls into view; JL
    261009), full size in the pop-out, and a tag."""
    line = f'<p class=q-work><span class=mut>Work:</span> {work}</p>' if work else ""
    if not page:
        return '<p class=mut>No report yet</p>' + line
    tag = page.stem.split("_", 1)[0]
    status = dict(_fields(page)).get("answer-status", "open")
    drawing = page.with_suffix(".excalidraw")
    if drawing.is_file():
        pic = (f'<div class=rp-live title="Click to pan and zoom"><iframe class=rp-draw inert loading=lazy '   # inert: it never
               f'title="{_e(page.stem)}" src="{_e(_draw_url(drawing, root))}" referrerpolicy=no-referrer></iframe></div>'  # takes focus
               f'<p class=rp-full>{pop(_draw_url(drawing, root), qid + " · Drawing · generated, view only", "full size ↗")}</p>')
    elif studio := _studio_links(page):                       # a report that draws nothing links the Studio frames
        pic = ('<p class=rp-full><span class=mut>Studio:</span> '   # that show it (b51, JL 261021: "No more draw in
               + " · ".join(pop(_draw_url(p, root), f"{qid} · Studio · {name}", f"{name} ↗") for name, p in studio)
               + '</p>')                                              # the reports")
    else:
        pic = '<p class=mut>no drawing yet</p>'
    answer = _opening(page)
    return (f'<p class=rp-title>{pop(_reader(page, root), qid + " · Report · the Page", _title(page) + " ↗")}</p>'
            + (f'<p class=rp-text>{_e(answer)}</p>' if answer else '<p class=mut>no answer yet</p>')
            + line + pic + f'<p class=rp-tags>report {_e(tag)} · {_e(status)}</p>')


# two columns (b10 s32-D23, JL 261012): the question │ its report, the work behind it inside the report
Q_HEAD = ('<div class="q-row q-two q-head-row"><div>Logic · the question</div>'
          '<div>Report · what it says, and the work behind it</div></div>')


def question_rows(level: str, folder: Path, root: Path, sub: str = "", keep=None) -> tuple:
    """(html, groups): one row per Question of this level: Logic (the question, its status, the
    studio topics that feed it) │ Work (the Jobs and Tasks that answer it) │ Report."""
    _, groups, recs = _question_records(level, folder, root, keep)
    out = [(q["group"], q["html"]) for q in recs if sub in ("", "All") or q["group"] == sub]
    if not out:
        return '<p class=mut>No Questions at this level yet.</p>', groups
    if groups and sub in ("", "All"):              # All: the table grouped the same way, a heading per group (b10 s02-D25)
        return Q_HEAD + "".join(f'<h3 class=q-group>{_e(g or "other")}</h3>' + "".join(h for k, h in out if k == g)
                                for g in groups + ([""] if any(not k for k, _ in out) else [])), groups
    return Q_HEAD + "".join(h for _, h in out), groups


def _theme_fixed(theme: "Theme | None", row: dict, owner: Path) -> list:
    """A theme's fixed Report groups for one register row: report_fixed(row, owner), the owner being the level
    whose register is read (a paper's come from its telling's **Feeds:**, b16 s05-D01), or report_fixed(row)
    for a rule that needs only the row (insight's level letter)."""
    fn = theme.report_fixed if theme is not None else None
    if not fn:
        return []
    import inspect
    try:
        takes_owner = len(inspect.signature(fn).parameters) >= 2
    except (TypeError, ValueError):
        takes_owner = False
    return [str(g) for g in ((fn(row, owner) if takes_owner else fn(row)) or []) if g]


# every theme's Report starts with this suggested group (b10 s05-D06, named by JL 261012, s05-D22): a question that
# came up outside the plan, from anyone, parked here until it finds its group; Untagged is a row with no group yet
REPORT_SUGGESTED = ("Random thoughts",)


def report_view(level: str, folder: Path, root: Path, theme: "Theme | None" = None, empty: str = "") -> str:
    """The Report as the Studio shows its topics (b10 s05-D05, JL 261011: "if the report card to show, it will
    be the same as the sNN, we can create and add the tags"): one folding card per Question under the group
    bar, Current · groups · Untagged · + Group; opened, its Logic │ Work │ Report row. A Question's groups are
    the theme's fixed ones for it (Theme.report_fixed, no ×) and then its register `group:` line, comma-separated;
    a drag writes that line (_register_set_groups); reports/_groups.txt keeps the order. Every level shows its
    bar, Block, Job and Task (b10 s05-D17, JL 261012: "the report group tags for both the block level, job level
    and task level"), even before its first Question: `empty` is then the list under it."""
    owner, _, recs = _question_records(level, folder, root)
    extra = list((theme.report_cards(level, folder, root) or []) if theme is not None and theme.report_cards else [])
    cards, tag_lists, fixed_all = [], [], []
    for c in extra:                     # the theme's own cards (a paper's ideas, its standing Questions): fixed
        groups = _split_tags(",".join(str(g) for g in (c.get("groups") or [])))
        name = f'{c["id"]} · {c.get("title") or ""}'.rstrip(" ·")
        attrs, _, current, chips = _group_parts(str(c["id"]), name, groups, noun="question", fixed=groups)
        fixed_all += groups
        status = str(c.get("status") or "")
        cards.append(f'<details class="topic q-card q-theme" data-studio-tags="{_e(json.dumps(groups))}"{attrs}>'
                     f'<summary><span class=related-head><b>{_e(name)}</b>{chips}'
                     + (f'<br><span class=topic-meta>{_e(status)}</span>' if status else "")
                     + f'</span><span class=topic-pop>{current}</span></summary>{c.get("html") or ""}</details>')
        tag_lists.append(groups)
    for q in recs:
        fixed = _theme_fixed(theme, q["row"], owner)
        fixed_all += fixed
        groups = _split_tags(",".join(fixed + [q["group"]]))
        name = f'{q["id"]} · {q["title"]}'
        attrs, handle, current, chips = _group_parts(q["id"], name, groups, noun="question", fixed=fixed)
        dot = "answered" if q["status"].startswith("answered") else "partial" if q["status"].startswith("partial") else "open"
        meta = f'{q["status"]} · {q["work"]} piece{"" if q["work"] == 1 else "s"} of work'
        cards.append(f'<details class="topic q-card" data-studio-tags="{_e(json.dumps(groups))}"{attrs}><summary>'
                     f'{handle}<span class="q-dot {dot}" title="{_e(q["status"])}"></span><span class=related-head>'
                     f'<b>{_e(name)}</b>{chips}<br><span class=topic-meta>{_e(meta)}</span></span>'
                     f'<span class=topic-pop>{current}</span></summary>{Q_HEAD}{q["html"]}</details>')
        tag_lists.append(groups)
    where = _rel(face(owner), root) if face(owner) else "the face"
    note = (f'<p class=mut>{_link(_reader(face(owner), root), where) if face(owner) else where}: one card per Question; its '
            'groups are its register group: line, made and added as on a Studio topic' +
            (', and the theme\'s own, fixed' if theme is not None and (theme.report_fixed or theme.report_cards)
             else '') + '.</p>')
    if not cards:
        note = ""
    listing = "".join(cards) or empty or '<p class=mut>No Questions at this level yet.</p>'
    return note + group_list(owner, root, "reports", tag_lists, listing,
                             starting=(tuple(theme.report_groups) if theme is not None else ()) + REPORT_SUGGESTED,
                             fixed=tuple(dict.fromkeys(fixed_all)))


def _question_records(level: str, folder: Path, root: Path, keep=None) -> tuple:
    """(owner, groups, records): one record per Question of this level (id, group, its register row, title,
    status, how much work answers it, and its Logic │ Work │ Report row). `owner` is the level whose register
    is read: the folder, or a Job's Block when the Job has none of its own but `answers:` the Block's."""
    md = face(folder)
    register = _register(md)
    owner = folder                              # the level whose register, reports and studio are read
    block = _block_above(folder) if level == "Job" and not register else None
    asked = _answer_ids(md) if block else set()
    if block and not asked:     # or the Block's Questions whose work: names a file of this Job (cowork, s05-D17)
        here = folder.name + "/"
        asked = {str(r["id"]).lower() for r in _register(face(block))
                 if any(str(w.get("task") or w.get("path") or "" if isinstance(w, dict) else w).startswith(here)
                        for w in (r.get("work") if isinstance(r.get("work"), list) else []))}
    if asked:   # a Job with no Questions of its own shows the Block's its face answers: (JL 261011, an empty j51)
        owner = block
        register = [r for r in _register(face(block)) if str(r["id"]).lower() in asked]
    reports = {q.name.split("_", 1)[0].lower(): q for q in sorted((owner / "reports").glob("q*/"))   # q01_x, q-food-1_x
               if re.match(r"(?i)q[a-z-]*\d+_", q.name)} \
        if (owner / "reports").is_dir() else {}
    rows = [dict(r) for r in register]
    known = {str(r["id"]).lower() for r in rows}
    if owner == folder:
        rows += [{"id": k.upper(), "title": ""} for k in reports if k not in known]  # a report not yet registered
    feeders = {}
    for topic, drawings in _studio_topics(owner):
        for q in _note_facts(_notes(topic))["feeds"]:
            feeders.setdefault(q.split("_", 1)[0].lower(), []).append((topic, drawings[0] if drawings else None))
    if keep is not None:                        # keep(group) -> bool: the rows one view shows
        rows = [r for r in rows if keep(str(r.get("group") or ""))]
    groups = list(dict.fromkeys(str(r["group"]) for r in rows if r.get("group")))
    # the level's own Runs on a Question, as the Work column's head says (b10 s05 Open 3, Q05 read "no work yet"
    # under two Runs): a run card whose target: is the Question's id, run-report-q05's and run-check-q05's
    on_q = {}
    for run in runs_of(folder):
        card = run["path"] / "run.yaml" if run["path"].is_dir() else None
        text = card.read_text(encoding="utf-8", errors="ignore") if card and card.is_file() else ""
        target = _yaml_scalar(text, "target")
        if re.fullmatch(r"(?i)q[a-z-]*\d+", target):           # q05, q-food-1
            ticket = run["path"] / (_yaml_scalar(text, "ticket") or "-")
            on_q.setdefault(target.lower(), []).append(
                f'{_link(_reader(ticket if ticket.is_file() else card, root), run["run"])} '
                f'<span class=mut>{_e(run["status"])}</span>')
    out = []
    for r in rows:
        qid = str(r["id"])
        rp = r.get("report")
        page = (owner / rp) if rp and (owner / rp).is_file() else None
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
        if owner != folder:                     # the Block's work under this Job, named from the Job
            here = folder.relative_to(owner).as_posix() + "/"
            work = [w[len(here):] for w in work if w.startswith(here)]
        kids = _answering(folder, level, qid, root)
        named = {_rel(k, folder) for k in kids}  # a Task its face and the register's work: both name, once (b51 261021)
        work = [w for w in dict.fromkeys(work) if w.rstrip("/") not in named]
        runs = on_q.get(qid.lower(), [])
        work_html = " · ".join([_link(ROUTE + "?" + urlencode({"path": _rel(k, root)}), _rel(k, folder)) for k in kids]
                               + [_link(_reader(folder / w, root), w) if (folder / w).is_file() else _e(w)
                                  for w in work if w] + runs) or '<span class=mut>no work yet</span>'   # a file opens in the reader
        out.append({"id": qid, "group": str(r.get("group") or ""), "row": r, "title": str(title),
                    "status": str(status), "work": len(kids) + len([w for w in work if w]) + len(runs),
                    "html": f'<div class="q-row q-two" id="question-{_e(qid)}"><div class=q-l>{logic}</div>'
                            f'<div class=q-r>{_report_cell(qid, page, root, work_html)}</div></div>'})
    return owner, groups, out

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
    """True when a theme laid the Page out in this Space itself: draft_task_spaces marked it
    (Space.page), or its subspaces start with the base's Page Task views; it may add its own after
    them (paper's Reviews, b16 s13)."""
    if space is not None and getattr(space, "page", False):
        return True
    from live.task_draft import DRAFT_TASK_SUBS
    page = DRAFT_TASK_SUBS.get(name)
    return bool(page) and tuple(subspaces)[:len(page)] == page


def spaces_for(theme: Theme, level: str, folder: Path, root: Path, sub: str = "") -> dict:
    """The theme's Spaces over the vanilla default, field by field."""
    base = vanilla(level, folder, root, sub, theme)
    own = theme.spaces(level, folder, root, sub) if theme.spaces else {}
    layout = task_layouts(theme.name).get(task_type(folder)) if level == "Task" else None
    if layout and not any(getattr(s, "page", False) for s in own.values()):
        # a Task type the base lays out (b32 s03): its layout first, the theme's own Spaces on top
        own = {**layout(folder, root, sub), **own}
    if theme.run_names:                        # the theme's buttons named by their Runs, this folder's tag filled
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
        # out in this Space itself (draft_task_spaces: the Page's exact views, embedded)
        if v.keep and not lays_out_page(name, t.subspaces, t):
            theirs = t.subspaces or v.subspaces           # a view the theme names too keeps its place
            merged = replace(merged, subspaces=theirs + tuple(k for k in v.keep if k not in theirs))
            if sub in v.keep and sub not in (t.subspaces or ()):    # a theme's own view of that name wins
                merged = replace(merged, html=v.html, open=sub, disk=v.disk)
        out[name] = merged
    # Studio and Related are Block-owned views, shared with that Block's Jobs and Tasks (b03 s02-D09,
    # b10 s04-related-workbench-skill)
    if level != "Block":
        block = chain(folder, root).get("Block")
        shared = spaces_for(theme, "Block", block, root) if block else {}
        out["Idea Studio"] = shared.get("Idea Studio") or Space('<p class=mut>Studio needs an owning Block.</p>')
        out["Related"] = shared.get("Related") or Space('<p class=mut>Related needs an owning Block.</p>')
    # Delivery has one physical owner, the Block (b10 s03-D06, JL 261011: "for the section, we will do not
    # have the related studio and delivery"; "also for the Jobs"). A Job's or Task's view is only its part of
    # the Block's Delivery, picked in the source row (render), and links back down to its folder.
    destination = delivery_dir(folder)
    block = delivery_owner(folder)
    address = destination.relative_to(block).as_posix() + "/"
    note = (f'<p class=space-reads>The Block\'s delivery/: <code>delivery/</code>; each Job\'s and Task\'s part '
            'is under its own path, picked in the row above.</p>' if folder.resolve() == block else
            f'<p class=space-reads>Its part of the Block\'s Delivery: <code>{_e(address)}</code> · from '
            f'{_link(ROUTE + "?" + urlencode({"path": _rel(folder, root)}), folder.name)}</p>')
    out["Delivery"] = replace(out["Delivery"], html=note + out["Delivery"].html,
                              disk=((delivery_relative(folder) + "/", "Block-owned delivery files for this source"),))
    return out


# ── the page ────────────────────────────────────────────────────────────────────────────────────
CSS = """
:root{--bg:#fff;--fg:#1c1c1c;--mut:#6f6f6b;--line:#e3e3e6;--acc:#3e5c84;--acc-soft:#e6edf5;--card:#fff;--ok:#24733d;--warn:#996b00;--miss:#c92a2a;--tab-line:#ced4da;--tab-on:#1864ab;--tab-wash:#e7f5ff;--wash:#f6f6f7;--grp-fixed-bg:#e9ecef;--grp-fixed-line:#868e96;--grp-sug-bg:#fff4e6;--grp-sug-line:#f08c00}
@media(prefers-color-scheme:dark){:root{--bg:#161719;--fg:#e8e8e6;--mut:#a0a09c;--line:#2c2e33;--acc:#8aa7cc;--acc-soft:#22304a;--card:#161719;--ok:#8bd49a;--warn:#e4bd62;--miss:#ff8787;--tab-line:#414852;--tab-on:#91caff;--tab-wash:#253749;--wash:#1d1f22;--grp-fixed-bg:#2b2f34;--grp-fixed-line:#868e96;--grp-sug-bg:#3b2a12;--grp-sug-line:#d9822b}}
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
.levels select{font:inherit;font-size:14px;padding:3px 8px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--fg);field-sizing:content;max-width:min(56ch,100%);text-overflow:ellipsis}
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
.subs .tab,.studio-filters .tab{font:400 16px system-ui,sans-serif;padding:5px 12px;border:1px solid var(--tab-line);border-radius:6px;
 background:transparent;color:var(--fg)}
.subs .tab.on,.studio-filters .tab.on{border-color:var(--tab-on);color:var(--tab-on);background:var(--tab-wash);font-weight:400}
.subs .tab:hover,.studio-filters .tab:hover{border-color:var(--tab-on)}
.studio-filters{margin:0 0 12px;position:sticky;top:8px;z-index:2;padding:4px 0;background:var(--bg)}.studio-filters button{cursor:pointer}.tag-count{font-size:12px;opacity:.7;margin-left:4px}
.studio-filters .drop-ready{outline:2px dashed var(--tab-on);outline-offset:3px;background:var(--tab-wash)}
.studio-drag{cursor:grab;flex:none;user-select:none;touch-action:none;color:var(--mut);padding:0 4px}
.studio-drag:active{cursor:grabbing}.topic.dragging{opacity:.55}
.studio-drag-preview{position:fixed;z-index:9999;pointer-events:none;padding:8px 12px;border:1px solid var(--tab-on);border-radius:8px;background:var(--bg);color:var(--fg);box-shadow:0 3px 14px #0002;font:600 14px system-ui,sans-serif;max-width:340px}
.studio-current{font:400 12px system-ui,sans-serif;white-space:nowrap;border:1px solid var(--tab-line);border-radius:6px;padding:3px 7px;background:var(--bg);color:var(--fg);cursor:pointer}
.studio-current[aria-pressed=true]{color:var(--tab-on);border-color:var(--tab-on);background:var(--tab-wash)}
/* groups you make and delete (b10 s02-D16): × beside a group deletes it, + Group makes one, × on a topic's chip takes it out */
.studio-filters.row{gap:8px;padding-top:8px}
.studio-filters .bar{background:var(--line);height:20px;margin:0 2px}
/* the × is a small corner badge that shows only under the mouse (JL 261010), so the row keeps even gaps */
.grp{position:relative;display:inline-flex}
.grp-emoji{margin-right:6px;font-size:15px}
.grp>.tab{touch-action:none;user-select:none}.studio-filters.sorting,.studio-filters.sorting .tab{cursor:grabbing}
.grp.moving>.tab{opacity:.6;border-style:dashed;border-color:var(--tab-on)}.grp.moving .grp-x{display:none}
.studio-filters .grp-x{position:absolute;top:-7px;right:-7px;width:18px;height:18px;padding:0;border:1px solid var(--tab-line);
 border-radius:50%;background:var(--bg);color:var(--mut);font:400 12px/16px system-ui,sans-serif;text-align:center;
 opacity:0;pointer-events:none;transition:opacity .12s}
.grp:hover .grp-x,.grp:focus-within .grp-x{opacity:1;pointer-events:auto}
.studio-filters .grp-x:hover{background:var(--warn);border-color:var(--warn);color:#fff}
.studio-filters .tab.grp-fixed:not(.on),.grp-key.grp-fixed{background:var(--grp-fixed-bg);border-color:var(--grp-fixed-line)}
.studio-filters .tab.grp-suggested:not(.on),.grp-key.grp-suggested{background:var(--grp-sug-bg);border-color:var(--grp-sug-line)}
.grp-key{border:1px solid;border-radius:4px;padding:0 5px;color:var(--fg)}
.grp-new{font:400 14px system-ui,sans-serif;border:1px dashed var(--line);border-radius:6px;padding:6px 12px;background:transparent;color:var(--mut)}
.grp-new:hover{border-color:var(--tab-on);border-style:solid;color:var(--tab-on);background:var(--tab-wash)}
.grp-form{display:inline-flex;gap:6px;align-items:center}.grp-form[hidden],.grp-new[hidden]{display:none}
.grp-form input{font:400 15px system-ui,sans-serif;border:1px solid var(--tab-on);border-radius:6px;padding:5px 10px;width:160px;background:var(--bg);color:var(--fg);outline:none}
.grp-ok,.grp-cancel{font:400 13px system-ui,sans-serif;border:1px solid var(--tab-line);border-radius:6px;padding:4px 10px;background:var(--bg);color:var(--fg);cursor:pointer}
.grp-ok{border-color:var(--tab-on);color:var(--tab-on)}
.topic-tags .chip{position:relative}
.tag-x{position:absolute;top:-6px;right:-6px;width:14px;height:14px;padding:0;border:1px solid var(--line);border-radius:50%;
 background:var(--bg);color:var(--mut);font:400 10px/12px system-ui,sans-serif;text-align:center;cursor:pointer;
 opacity:0;pointer-events:none;transition:opacity .12s}
.chip:hover>.tag-x,.chip:focus-within>.tag-x{opacity:1;pointer-events:auto}
.tag-x:hover{background:var(--warn);border-color:var(--warn);color:#fff}
.studio-source{font-size:13px;color:var(--mut);display:flex;align-items:center;gap:8px;margin-bottom:8px}
.studio-source select{font:400 13px system-ui,sans-serif;border:1px solid var(--tab-line);border-radius:6px;padding:4px 8px;background:var(--bg);color:var(--fg)}
.studio-help,.studio-empty,.studio-status{font-size:13px;margin:8px 0 12px}.studio-status:empty{display:none}
.studio-topics .topic-pop{margin-left:auto}
.studio-topics .topic>summary{flex-wrap:nowrap;align-items:center;gap:10px}
.studio-topics .topic>summary>b{flex:0 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.studio-topics .topic-tags{flex:0 1 auto;min-width:0;overflow:hidden;flex-wrap:nowrap}.studio-topics .topic-tags .chip{font-size:11px;white-space:nowrap}
.studio-topics .topic-pop,.studio-topics .topic>summary>.stage{flex:0 0 auto}
.studio-topics .studio-current{opacity:0;transition:opacity .15s}.studio-topics .topic:hover .studio-current,.studio-topics .studio-current:focus,.studio-topics .studio-current[aria-pressed=true]{opacity:1}
.studio-topics .topic>summary>.stage{font-size:0;gap:0;padding:5px 7px}
.topic[hidden]{display:none}.topic-tags{display:inline-flex;gap:6px;flex-wrap:wrap}.topic-tags .chip{font-size:12px;color:var(--mut);border-color:var(--line)}
.wf-table{border-collapse:collapse;width:100%;font-size:14px}.wf-table th,.wf-table td{text-align:left;padding:5px 8px;border-bottom:1px solid var(--line);vertical-align:top}
.wf-table th{font-weight:600;color:var(--mut);font-size:12.5px}
.topic{border:1px solid var(--line);border-radius:10px;background:var(--card);margin:0 0 8px;overflow:hidden}
.topic>summary{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:baseline;cursor:pointer;padding:9px 14px;list-style:none}
.stage{--st:#868e96;--st-bg:#f1f3f5;display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:600;letter-spacing:.02em;padding:2px 10px 2px 8px;border:1px solid var(--st);border-radius:999px;white-space:nowrap;color:var(--st);background:var(--st-bg)}
.stage-explore{--st:#2b8a3e;--st-bg:#ebfbee}.stage-shaping{--st:#7048e8;--st-bg:#f3f0ff}.stage-agreed{--st:#1971c2;--st-bg:#e7f5ff}.stage-closed{--st:#495057;--st-bg:#f1f3f5}
@media(prefers-color-scheme:dark){.stage{--st-bg:transparent}.stage-explore{--st:#8ce99a}.stage-shaping{--st:#b197fc}.stage-agreed{--st:#74c0fc}.stage-closed{--st:#adb5bd}}
.stage-steps{display:inline-flex;gap:2px}.stage-steps b{width:7px;height:7px;border-radius:2px;border:1px solid var(--st);opacity:.55}.stage-steps b.on{background:var(--st);opacity:1}
.stage-none{color:var(--mut);border-style:dashed;font-weight:400}
.topic>summary::-webkit-details-marker{display:none}.topic>summary::before{content:"▸";color:var(--mut)}
.topic[open]>summary::before{content:"▾"}.topic[open]>summary{border-bottom:1px solid var(--line)}
.studio-related{border:1px solid var(--line);border-radius:10px;background:var(--card);margin:16px 0 8px;overflow:hidden}
.related-in .topic>summary{flex-wrap:nowrap}.related-in .topic>summary>.related-head{flex:1 1 auto;min-width:0}.related-in .topic>summary b{font-weight:600}.related-in .topic-pop{margin-left:auto;flex:0 0 auto;max-width:34%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.related-img{display:block;max-width:100%;border-top:1px solid var(--line)}
.studio-related>summary{display:flex;gap:10px;align-items:baseline;cursor:pointer;padding:9px 14px;list-style:none}
.studio-related>summary::-webkit-details-marker{display:none}.studio-related>summary::before{content:"▸";color:var(--mut)}
.studio-related[open]>summary::before{content:"▾"}.studio-related[open]>summary{border-bottom:1px solid var(--line)}
.studio-related>.related-in{padding:6px 14px 12px}.related-meta{color:var(--mut);font-size:13px}
/* a Delivery item's versions, newest first, one pane each (JL 261014) */
.dv-vers{margin:8px 12px 6px;gap:4px}.dv-vers .tab{font-size:13px;padding:2px 10px;cursor:pointer}.dv-vers .tab[aria-pressed=true]{border-color:var(--tab-on);color:var(--tab-on);background:var(--tab-wash)}.dv-files{margin:2px 12px 8px}
.tl-wrap{--tl-time:92px;--tl-dot:28px;--tl-cell:60px;--tl-gcell:100px}.tl-wrap [hidden]{display:none!important}
.tl-levels{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:4px 0 14px}.tl-help{font-size:12px;color:var(--mut);margin-left:8px}
.tl-levels button{font:inherit;font-size:13px;border:1px solid var(--tab-line);border-radius:6px;padding:2px 10px;background:var(--bg);color:var(--fg);cursor:pointer}
.tl-levels button[aria-pressed=true]{border-color:var(--tab-on);color:var(--tab-on);background:var(--tab-wash)}
.tl-kd{display:inline-block;width:9px;height:9px;border-radius:2px;margin:0 6px 0 2px;flex:0 0 auto}.tl-legend-k .tl-kd{margin-left:10px}
.k-decided{background:var(--ok)}.k-session{background:var(--acc)}.k-drawing{background:var(--warn)}
.tl-wrap[data-level=days]:not(.picking) .tl-list,.tl-wrap[data-level=days] .tl-legend-k,.tl-wrap:not([data-level=days]) .tl-map,
.tl-wrap:not([data-level=days]) .tl-legend-b,.tl-wrap[data-level=topics] .tl-items{display:none}
.tl-map{position:relative;overflow-x:auto;padding:0 0 26px;--tl-head:28px}.tl-map[data-cols=topics]{--tl-head:var(--tl-slant,28px)}
.tl-map::before{content:"";position:absolute;left:calc(var(--tl-time) + var(--tl-dot) / 2 - 1px);top:calc(var(--tl-head) + 12px);bottom:9px;border-left:2px solid var(--fg)}
.tl-map::after{content:"";position:absolute;left:calc(var(--tl-time) + var(--tl-dot) / 2 - 6px);bottom:0;border:6px solid transparent;border-top:10px solid var(--fg);border-bottom:0}
.tl-mhead,.tl-mrow{display:flex;align-items:center;min-width:max-content}.tl-mhead{height:var(--tl-head)}
.tl-mhead>span:first-child,.tl-mrow>time{flex:0 0 var(--tl-time);text-align:right;font-size:13px;font-weight:600;white-space:nowrap}
.tl-mhead>span:nth-child(2),.tl-dot{flex:0 0 var(--tl-dot);display:flex;justify-content:center;position:relative;z-index:1}
.tl-dot::before{content:"";width:10px;height:10px;border-radius:50%;background:var(--fg);box-shadow:0 0 0 3px var(--card)}
.tl-col,.tl-cell{flex:0 0 var(--tl-cell);display:flex;align-items:center;justify-content:center;position:relative}
.tl-col{font-size:12px;color:var(--mut);text-decoration:none;align-self:stretch}.tl-col:hover{color:var(--tab-on)}
.tl-col>b{position:absolute;left:0;right:0;bottom:4px;text-align:center;font-size:14px;font-weight:700;color:var(--fg)}
.tl-col>span{position:absolute;left:50%;bottom:28px;transform-origin:0 100%;transform:rotate(-45deg);white-space:nowrap}
.tl-col:hover>b,.tl-col.on>b{color:var(--tab-on)}
.tl-mrow{height:38px;border-radius:8px}.tl-mrow:hover{background:var(--wash)}
.tl-cell{height:38px}.tl-cell::before{content:"";position:absolute;left:50%;top:0;bottom:0;border-left:1px solid var(--line)}
.tl-b{position:relative;display:block;width:var(--s);height:var(--s);border-radius:50%;background:var(--acc);opacity:.8;
 box-shadow:0 0 0 2px var(--card);transition:transform .12s,opacity .12s}.tl-b:hover{transform:scale(1.2);opacity:1}
.tl-bar,.tl-bar-h{flex:0 0 170px;margin-left:14px;display:flex;align-items:center;gap:8px}.tl-bar-h{font-size:11px;color:var(--mut);align-self:flex-end;padding-bottom:4px}
.tl-track{flex:0 0 120px;height:8px;border-radius:4px;background:var(--wash);overflow:hidden}.tl-track i{display:block;height:100%;background:var(--mut);opacity:.6}
.tl-bar b{font-size:12px;font-weight:600;color:var(--mut)}
.tl-axis{list-style:none;margin:0;padding:0 0 26px;position:relative}
.tl-axis::before{content:"";position:absolute;left:111px;top:6px;bottom:9px;border-left:2px solid var(--fg)}
.tl-axis::after{content:"";position:absolute;left:106px;bottom:0;border:6px solid transparent;border-top:10px solid var(--fg);border-bottom:0}
.tl-day{position:relative;display:grid;grid-template-columns:92px minmax(0,1fr);column-gap:40px;padding:0 0 14px}
.tl-day::after{content:"";position:absolute;left:107px;top:5px;width:10px;height:10px;border-radius:50%;background:var(--fg);box-shadow:0 0 0 3px var(--card)}
.tl-day>time{text-align:right;font-size:13px;font-weight:600;white-space:nowrap;line-height:20px}
.tl-topic{display:grid;grid-template-columns:minmax(160px,280px) minmax(0,1fr);column-gap:12px;align-items:center;line-height:20px;padding:1px 0}
.tl-name{font-size:13px;color:var(--fg);text-decoration:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tl-name b{font-weight:600;margin-right:6px}.tl-name span{color:var(--mut)}.tl-name:hover span{color:var(--tab-on)}
.tl-meter{display:flex;align-items:center;gap:8px}.tl-stack{display:flex;flex:0 0 auto;height:8px;border-radius:4px;overflow:hidden}.tl-n{font-size:12px;color:var(--mut)}
.tl-items{grid-column:1/-1;list-style:none;margin:3px 0 8px 3px;padding:0 0 0 12px;border-left:2px solid var(--line);display:grid;gap:2px}
.tl-items li{display:flex;align-items:center;font-size:12.5px;color:var(--mut);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tl-items li>span,.tl-items li>a{overflow:hidden;text-overflow:ellipsis}.tl-items li>a{margin-right:6px}.tl-items li b{color:var(--fg);font-weight:600;margin-right:6px}
.tl-mrow.tl-quiet,.tl-quiet .tl-cell,.tl-quiet .tl-gcell{height:20px}.tl-quiet>time{font-weight:400;font-size:12px;color:var(--mut)}
.tl-quiet .tl-bar,.tl-quiet .tl-b,.tl-quiet .tl-gb{visibility:hidden}
.tl-quiet .tl-dot::before,.tl-day.tl-quiet::after{width:6px;height:6px;border:2px solid var(--mut);background:var(--card)}
.tl-day.tl-quiet{padding-bottom:6px}.tl-day.tl-quiet>time{line-height:20px}
.tl-groups{display:flex;flex-wrap:wrap;gap:4px;align-items:center;margin:-6px 0 12px;font-size:12px;color:var(--mut)}
.tl-groups:empty{display:none}.tl-groups>span{margin-right:4px}
.tl-groups button{font:inherit;font-size:12px;border:1px solid var(--tab-line);border-radius:6px;padding:1px 8px;background:var(--bg);color:var(--fg);cursor:pointer}
.tl-groups button[aria-pressed=true]{border-color:var(--tab-on);color:var(--tab-on);background:var(--tab-wash)}.tl-groups button:hover{border-color:var(--tab-on)}
.tl-groups button i{font-style:normal;opacity:.7;margin-left:4px}
.fd-root{margin:2px 0 8px;font:12px ui-monospace,monospace;color:var(--mut)}
.fd-tree,.fd-tree ul{list-style:none;margin:0;padding:0}.fd-tree ul{margin-left:11px;padding-left:12px;border-left:1px solid var(--line)}
.fd-row{display:flex;align-items:baseline;gap:10px;min-width:0;padding:2px 6px;border-radius:5px;font-size:13.5px;line-height:21px}
.fd-row:hover{background:var(--wash)}.studio-folder summary.fd-row{cursor:pointer;list-style:none}
.studio-folder summary.fd-row::-webkit-details-marker{display:none}
.fd-dir>details>summary .fd-name::before{content:"📁 "}.fd-dir>details[open]>summary .fd-name::before{content:"📂 "}
.fd-name{font-weight:600;white-space:nowrap}.fd-i{flex:0 0 auto;margin-right:-4px}
.fd-file a{color:var(--fg);text-decoration:none;white-space:nowrap}.fd-file a:hover{color:var(--tab-on);text-decoration:underline}
.fd-n,.fd-when{flex:0 0 auto;font-size:12px;color:var(--mut)}
.fd-more button{font:inherit;font-size:12px;margin:4px 6px;border:1px solid var(--tab-line);border-radius:6px;padding:1px 9px;background:var(--bg);color:var(--fg);cursor:pointer}
.fd-word{font-size:12.5px;color:var(--mut);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.tl-map[data-cols=groups] .tl-col,.tl-map[data-cols=groups] .tl-cell,.tl-map[data-cols=topics] .tl-gcol,.tl-map[data-cols=topics] .tl-gcell{display:none}
.tl-gcol,.tl-gcell{flex:0 0 var(--tl-gcell);position:relative}.tl-gcell{height:38px;display:flex;align-items:center;justify-content:center}
.tl-gcell::before{content:"";position:absolute;left:50%;top:0;bottom:0;border-left:1px solid var(--line)}
.tl-gcol{font:inherit;font-size:11px;color:var(--mut);background:none;border:0;cursor:pointer;align-self:flex-end;padding:0 4px 4px;
 white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-align:center}.tl-gcol:hover{color:var(--tab-on)}
.tl-gb{position:relative;display:block;width:var(--s);height:var(--s);border-radius:50%;background:var(--acc);opacity:.8;border:0;padding:0;
 cursor:pointer;box-shadow:0 0 0 2px var(--card);transition:transform .12s,opacity .12s}.tl-gb:hover{transform:scale(1.2);opacity:1}
.tl-cols{display:inline-flex;gap:4px;align-items:center;font-size:12px;color:var(--mut);margin-left:8px}
.tl-levels .tl-cols button{font-size:12px;padding:1px 8px}
.tl-wrap[data-level=days].picking .tl-off,.tl-wrap:not(.picking) .tl-picked,.tl-wrap:not([data-level=days]) .tl-picked{display:none}
.tl-col{cursor:pointer}.tl-col.on{color:var(--tab-on);font-weight:700}.tl-cell.on .tl-b{background:var(--tab-on);opacity:1}
.tl-wrap.picking .tl-cell:not(.on) .tl-b{opacity:.3}
.tl-picked{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:2px 0 12px;font-size:13px}
.tl-picked button{font:inherit;font-size:12px;border:1px solid var(--tab-line);border-radius:6px;padding:1px 8px;background:var(--bg);color:var(--fg);cursor:pointer}
@media(max-width:700px){.tl-wrap{--tl-time:62px}.tl-day{grid-template-columns:62px minmax(0,1fr);column-gap:30px}
 .tl-axis::before{left:76px}.tl-axis::after{left:71px}.tl-day::after{left:72px}.tl-topic{grid-template-columns:minmax(0,1fr) 120px}}
.topic-meta{color:var(--mut);font-size:13px;flex:1}.topic-pop a{text-decoration:none;font-size:15px}
.topic .none{margin:10px 14px}.topic-pop{display:flex;gap:10px;align-items:baseline;font-size:13px}
.chip{display:inline-block;padding:0 8px;margin-right:4px;border:1px solid var(--acc);border-radius:999px;color:var(--acc);font-size:12px;text-decoration:none}
.st-bar{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;padding:8px 14px}
.st-map{overflow-x:auto;padding:10px 14px 16px;border-top:1px solid var(--line)}
.st-side{display:inline-flex;border:1px solid var(--line);border-radius:6px;overflow:hidden}.st-side button{font:500 12.5px -apple-system,sans-serif;border:0;padding:1px 9px;cursor:pointer;background:var(--bg);color:var(--mut)}.st-side button+button{border-left:1px solid var(--line)}.st-side button[aria-pressed=true]{background:var(--tab-wash,var(--line));color:var(--tab-on,var(--fg))}.st-side button:disabled{cursor:default;opacity:.45}.draw-edit[hidden],.side-link[hidden]{display:none}
.draw-edit{font:500 12.5px -apple-system,sans-serif;border:1px solid var(--line);border-radius:6px;padding:1px 9px;cursor:pointer;background:var(--bg);color:var(--fg)}
.studio-parts{margin:10px 14px 16px}.studio-parts>details.topic{margin:0 0 8px}.studio-transcripts{margin:16px 14px}.studio-transcripts>h3{font-size:17px;margin:0 0 12px}.studio-transcript-note,.studio-transcript-links{margin:12px 14px;font-size:14px;line-height:1.5}.studio-transcript-note{color:var(--mut)}
.st-frame{display:block;width:100%;height:calc(100vh - 240px);min-height:520px;border:0;border-top:1px solid var(--line);background:#fff}
.add{margin:6px 2px 0}
.st-ok{color:var(--ok)}.st-warn{color:var(--warn)}
.dl-frame{display:block;width:100%;height:560px;border:0;border-top:1px solid var(--line);background:#fff}
.dl-note{padding:0 14px 10px;margin:0}.dl-src{max-height:420px;overflow:auto;margin:0 14px 12px}
.topic.missing{border:1px dashed var(--miss);background:transparent}.topic.missing>summary b{color:var(--mut)}
.q-row{display:grid;grid-template-columns:1.1fr 1fr 1.3fr;border:1px solid var(--line);border-radius:10px;margin:0 0 8px;background:var(--card)}
.q-row.q-two{grid-template-columns:1fr 1.7fr}.q-work{font-size:13.5px;margin:6px 0 8px}
.q-row>div{padding:10px 12px;min-width:0}.q-row>div+div{border-left:1px solid var(--line)}
.q-head-row{border:0;background:transparent;margin:0;color:var(--mut);font-size:12.5px}.q-head-row>div{padding:2px 12px}.q-head-row>div+div{border-left:0}
/* level rows as the old Insight board drew them (b11, JL 261008): flush grey rows split by thin lines, a ▶
   marker, a small link on the right; the q-rows inside flush, like one table. A theme opts in by the classes. */
.dikw{border-top:1px solid var(--line);margin:4px 0 12px}
.dikw>.topic{border:0;border-bottom:1px solid var(--line);border-radius:0;margin:0;background:var(--wash)}
.dikw>.topic>summary{padding:8px 12px}.dikw>.topic>summary::before{content:"▶";color:var(--fg);font-size:11px}
.dikw>.topic[open]>summary::before{content:"▼"}.dikw .topic-meta{flex:1;font-size:13px}.dikw .lv-link{font-size:12.5px}
/* a report read as one document (insight's Overall Report, JL 261012): one column at a reader's measure */
.report-doc{max-width:1180px;margin:4px 0 24px;font-size:15.5px;line-height:1.6}.report-doc>:not(.rep-glance){max-width:820px}.report-doc h2{font-size:24px;margin:2px 0 4px}
.report-doc>p.mut{margin:0 0 4px}.report-doc .rep-glance-head{margin:14px 0 6px;font-weight:700;font-size:17px}
.report-doc .rep-glance{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:0 0 20px}@media(max-width:1000px){.report-doc .rep-glance{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:600px){.report-doc .rep-glance{grid-template-columns:1fr}}
.rep-glance a{display:block;border:1px solid var(--line);border-radius:8px;padding:8px 10px;color:inherit;text-decoration:none;background:var(--card)}
.rep-glance a:hover{border-color:var(--acc)}.rep-glance span{display:block;font-size:12.5px;color:var(--mut)}
.rep-glance b{display:block;font-size:14px;line-height:1.35;margin:2px 0 6px}.rep-glance img{display:block;width:100%;background:#fff;border-radius:4px}
.report-doc .rep-fig{margin:12px 0 14px;max-width:720px}.report-doc .rep-fig figcaption{font-weight:700;font-size:16px;margin:0 0 6px}
.report-doc .rep-fig img{display:block;width:100%;border:1px solid var(--line);border-radius:8px;background:#fff}.report-doc .rep-fig p{margin:4px 0 0;font-size:13px}
.report-doc section{border-top:1px solid var(--line);padding:16px 0 4px}.report-doc section h3{font-size:19px;margin:0 0 2px}
.report-doc .rep-ask{color:var(--mut);font-style:italic;margin:0 0 10px}.report-doc .rep-lead{font-weight:600;margin:0 0 4px}
.report-doc ol,.report-doc ul{padding-left:24px}.report-doc li{margin:0 0 7px}.report-doc h4{font-size:15.5px;margin:12px 0 4px}
.report-doc details{margin:4px 0 8px}.report-doc details>summary{cursor:pointer;color:var(--acc);font-size:14px}
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
.q-group{margin:22px 0 6px;font-size:16px}.from{margin:8px 0 0!important;font-size:12px;color:var(--mut)}.from-list{margin:2px 0 0;padding-left:16px;font-size:13px}
.q-w{font-size:13.5px}.rp-title{font-weight:600}.rp-title a{color:inherit}.rp-text{font-size:14px}
.rp-thumb{display:block;margin:6px 0}.rp-thumb img{display:block;width:100%;max-height:200px;object-fit:contain;object-position:left top;border:1px dashed var(--line);border-radius:6px;background:#fff}
.rp-live{cursor:zoom-in;margin:6px 0 2px}.rp-live.on{cursor:auto}
.rp-draw{display:block;width:100%;height:300px;border:1px dashed var(--line);border-radius:6px;background:#fff}
.rp-full{font-size:12.5px;margin:0 0 4px!important}
.rp-tags{color:var(--mut);font-size:12.5px}
#frame-pop{width:min(1300px,95vw);height:90vh;max-width:95vw;max-height:90vh;padding:0;border:0;border-radius:12px;background:var(--bg);color:var(--fg);overflow:hidden}
#frame-pop::backdrop{background:rgba(0,0,0,.35)}#frame-pop[open]{display:flex;flex-direction:column}
.pop-bar{display:flex;align-items:center;gap:12px;padding:8px 14px;border-bottom:1px solid var(--line)}
.pop-title{font-weight:650;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pop-x{border:0;background:transparent;font-size:20px;cursor:pointer;color:var(--fg)}.pop-frame{flex:1;border:0;width:100%;background:#fff}
@media(max-width:600px){body{padding:12px}.row{flex-wrap:nowrap;overflow-x:auto}.q-row,.q-row.q-two{grid-template-columns:1fr}.q-row>div+div{border-left:0;border-top:1px solid var(--line)}.q-head-row{display:none}}
"""
CSS += RUN_CSS                                  # the Runs cards, shared with SPACE Home (JL 261019)

# Idea Studio: a topic's canvas loads when its row opens; Edit switches that canvas to the editor in
# place; #topic-<name> in the address opens that row (the Audience Report links here).
STUDIO_JS = """
(function(){
function load(d){var f=d.querySelector(':scope > iframe[data-src], :scope > .dv-pane:not([hidden]) > iframe[data-src], :scope > .st-pane:not([hidden]) > iframe[data-src]');if(d.open&&f&&!f.getAttribute('src'))f.src=f.dataset.src;}
// a Delivery item's versions (JL 261014): a version button shows its pane and loads its preview
document.addEventListener('click',function(ev){var b=ev.target.closest('.dv-vers [data-dv]');if(!b)return;
  var d=b.closest('details');d.querySelectorAll(':scope > .dv-vers [data-dv]').forEach(function(x){x.setAttribute('aria-pressed',String(x===b));});
  d.querySelectorAll(':scope > .dv-pane').forEach(function(p){p.hidden=p.dataset.dv!==b.dataset.dv;});load(d);});
function hashTarget(){
  var id;try{id=decodeURIComponent(location.hash.slice(1));}catch(e){return null;}
  var found=document.getElementById(id);if(found)return found;
  if(id.indexOf('topic-')!==0)return null;
  var name=id.slice(6),path=new URL(location.href).searchParams.get('path')||'';
  var matches=Array.from(document.querySelectorAll('[data-studio-name]')).filter(function(r){return r.dataset.studioName===name&&!r.closest('[data-group-kind]');});
  return matches.find(function(r){return path.endsWith('/'+r.dataset.studioSource);})||matches[0]||null;
}
// a row a person clicks open scrolls so its drawing sits in the middle of the window (JL 261019: "when I click it,
// the draw will in the center of the page"); rows the page opens itself (a #link, a restored Current) do not jump
var clicked=0;document.addEventListener('click',function(e){if(e.target.closest('details.topic > summary'))clicked=Date.now();},true);
document.querySelectorAll('details.topic').forEach(function(d){d.addEventListener('toggle',function(){load(d);
  if(d.open&&Date.now()-clicked<1500){var f=d.querySelector(':scope > iframe.st-frame')||d;
    setTimeout(function(){f.scrollIntoView({behavior:'smooth',block:'center'});},60);}});});
// a #question-QNN link opens that Question's card in the Report (b10 s05: each Question is a folding card)
(function(){var h=decodeURIComponent(location.hash.slice(1));if(h.indexOf('question-')!==0)return;
  var el=document.getElementById(h),card=el&&el.closest('details.q-card');if(card){card.open=true;el.scrollIntoView();}})();
document.querySelectorAll('.studio-topics').forEach(function(list){
  // Groups (b10 s02-D16): Current lives in this browser; every other group is a tag on the topic's
  // **Tags:** line, written by POST /_board/studio-group, so it is the same for everyone. The same bar
  // sorts Related's items (data-group-kind=related, JL 261011): there a group is the row's group cell.
  var rows=Array.from(list.querySelectorAll('details[data-studio-key]'));
  var nav=list.querySelector('.studio-filters');
  var empty=list.querySelector('.studio-empty'),status=list.querySelector('.studio-status');
  var source=list.querySelector('[data-studio-source-filter]');
  var owner=list.dataset.studioOwner,kind=list.dataset.groupKind||'studio',noun=list.dataset.groupNoun||'topic',pre=kind+'_';
  var storageKey='workbench.'+kind+'.current.v1:'+owner,groupsKey='workbench.studio.groups.v1:'+owner;
  var current=new Set(),active='';
  function buttons(){return Array.from(nav.querySelectorAll('[data-studio-tag]'));}
  function button(key){return buttons().find(function(b){return b.dataset.studioTag===key;})||null;}
  function isGroup(key){return key!=='__current__'&&key!=='__untagged__'&&key!=='';}
  function readList(k){try{var v=JSON.parse(localStorage.getItem(k)||'[]');
    return Array.isArray(v)?v.filter(function(x){return typeof x==='string';}):[];}catch(e){return [];}}
  function writeList(k,v){try{localStorage.setItem(k,JSON.stringify(v));return true;}catch(e){return false;}}
  function read(){return new Set(readList(storageKey));}
  current=read();
  function labels(row){try{return JSON.parse(row.dataset.studioTags||'[]');}catch(e){return [];}}
  function tags(row){return labels(row).map(function(t){return t.toLowerCase();});}
  function matches(row,key){var names=tags(row);
    return !key||(key==='__current__'?current.has(row.dataset.studioKey):key==='__untagged__'?names.length===0:names.indexOf(key)>=0);}
  function say(text){status.textContent=text;}
  // the Studio's Timeline follows this bar: a topic's lines show when its row shows (JL 261011)
  function timeline(key){var tl=document.querySelector('.studio-timeline');if(!tl)return;
    var hidden={},shown=0;rows.forEach(function(r){hidden[r.dataset.studioKey]=r.hidden;});
    var peak=0,sums=[];
    tl.querySelectorAll('[data-tl-key]').forEach(function(t){t.hidden=!!hidden[t.dataset.tlKey];});
    tl.querySelectorAll('.tl-mrow').forEach(function(r){var n=0;
      r.querySelectorAll('.tl-cell:not([hidden])').forEach(function(c){n+=Number(c.dataset.tlCount||0);});
      r.dataset.tlN=n;shown+=n;peak=Math.max(peak,n);sums.push([r,n]);});
    sums.forEach(function(s){var i=s[0].querySelector('.tl-track i'),b=s[0].querySelector('.tl-bar b');
      if(i)i.style.width=(peak?Math.round(s[1]/peak*100):0)+'%';if(b)b.textContent=s[1];});
    // a group's bubble adds up its topics that still show; a group with none left drops its column
    var gsum={},gpeak=0,gcells=tl.querySelectorAll('.tl-gcell');
    gcells.forEach(function(c){var n=0,parts={};try{parts=JSON.parse(c.dataset.tlParts||'{}');}catch(e){}
      Object.keys(parts).forEach(function(k){if(!hidden[k])n+=parts[k];});c.dataset.tlNow=n;gpeak=Math.max(gpeak,n);
      gsum[c.dataset.tlGroup]=(gsum[c.dataset.tlGroup]||0)+n;});
    gcells.forEach(function(c){var n=Number(c.dataset.tlNow),b=c.querySelector('.tl-gb');c.hidden=!gsum[c.dataset.tlGroup];
      if(b){b.hidden=!n;if(n)b.style.setProperty('--s',Math.round(8+22*Math.sqrt(n/gpeak))+'px');}});
    tl.querySelectorAll('.tl-gcol').forEach(function(h){h.hidden=!gsum[h.dataset.tlGroup];});
    // the slanted names' header is as tall as the longest name still shown
    var ln=0;tl.querySelectorAll('.tl-col:not([hidden])').forEach(function(c){ln=Math.max(ln,c.title.length);});
    var map=tl.querySelector('.tl-map');if(map)map.style.setProperty('--tl-slant',Math.min(Math.round(Math.max(ln-4,0)*7.2*0.71)+40,200)+'px');
    // the Timeline's own group picker: All, then this bar's buttons, the picked one on (JL 261012)
    var strip=tl.querySelector('.tl-groups');if(strip){strip.textContent='';
      var w=document.createElement('span');w.textContent='groups';strip.appendChild(w);
      [['','All','',rows.length]].concat(buttons().map(function(b){var e=b.querySelector('.grp-emoji'),c=b.querySelector('.tag-count');
        return [b.dataset.studioTag,b.dataset.studioLabel||b.dataset.studioTag,e?e.textContent+' ':'',c?c.textContent:''];}))
      .forEach(function(o){var x=document.createElement('button');x.type='button';x.dataset.tlTag=o[0];
        x.setAttribute('aria-pressed',String(o[0]===key));x.textContent=o[2]+o[1];
        var n=document.createElement('i');n.textContent=o[3];x.appendChild(n);strip.appendChild(x);});}
    tlGaps(tl);tl.dispatchEvent(new Event('tl-shown'));
  }
  function labelOf(key){var b=button(key);return b?(b.dataset.studioLabel||key):key;}
  function paint(){
    buttons().forEach(function(b){var key=b.dataset.studioTag;
      b.querySelector('.tag-count').textContent=rows.filter(function(r){return matches(r,key);}).length;});
    rows.forEach(function(r){var b=r.querySelector('.studio-current'),on=current.has(r.dataset.studioKey);
      b.textContent=on?'Remove from Current':'Add to Current';b.setAttribute('aria-pressed',String(on));});
  }
  function apply(key,save){
    if(!button(key))key='';
    active=key;
    rows.forEach(function(row){row.hidden=!matches(row,key)||(source&&source.value!=='__all__'&&row.dataset.studioSource!==source.value);});
    buttons().forEach(function(b){var on=b.dataset.studioTag===key;b.classList.toggle('on',on);b.setAttribute('aria-pressed',String(on));});
    paint();
    empty.hidden=rows.some(function(r){return !r.hidden;})||rows.length===0;
    if(kind==='studio')timeline(key);
    empty.textContent=key==='__current__'?'Current is empty. Unpick it to see every '+noun+', then add the ones you want to focus on.':
      isGroup(key)?'This group is empty. Unpick it to see every '+noun+', then drag '+noun+'s onto it by ⋮⋮.':'No '+noun+'s in this source.';
    if(save){var url=new URL(location.href);
      url.searchParams.delete(pre+'tag');url.searchParams.delete(pre+'group');
      if(key==='__current__')url.searchParams.set(pre+'group','current');
      else if(key)url.searchParams.set(pre+'tag',key);
      if(source&&source.value!=='__all__')url.searchParams.set('studio_source',source.value);else url.searchParams.delete('studio_source');
      var target=hashTarget();if(target&&target.hidden)url.hash='';history.replaceState(null,'',url);}
  }
  function setCurrent(row,on){
    var next=new Set(current);if(on)next.add(row.dataset.studioKey);else next.delete(row.dataset.studioKey);
    if(!writeList(storageKey,Array.from(next))){say('Could not save Current in this browser. Your selection has not changed.');return false;}
    current=next;apply(active,false);
    say(row.dataset.studioName+(on?' added to Current.':' removed from Current.'));return true;
  }
  function chips(row){
    var box=row.querySelector('.topic-tags');
    if(!box){box=document.createElement('span');box.className='topic-tags';row.querySelector('summary b').after(box);}
    box.textContent='';
    var fixed=[];try{fixed=JSON.parse(row.dataset.studioFixed||'[]');}catch(e){}   // a subfolder's or a theme's: no ×
    labels(row).forEach(function(t){var c=document.createElement('span');c.className='chip';c.dataset.tag=t;c.textContent=t;
      if(fixed.indexOf(t.toLowerCase())<0){var x=document.createElement('button');x.type='button';x.className='tag-x';
        x.title='Take out of '+t;x.setAttribute('aria-label','Take '+row.dataset.studioName+' out of '+t);x.textContent='×';
        c.appendChild(x);}
      box.appendChild(c);});
  }
  function makeGroup(label){
    var key=label.toLowerCase(),b=button(key);if(b)return b;
    var wrap=document.createElement('span');wrap.className='grp';
    b=document.createElement('button');b.type='button';b.className='tab';b.dataset.studioLabel=label;b.dataset.studioTag=key;
    b.setAttribute('aria-pressed','false');
    var em=document.createElement('span');em.className='grp-emoji';em.setAttribute('aria-hidden','true');em.textContent=emojiFor(label);
    b.appendChild(em);b.appendChild(document.createTextNode(label+' '));
    var n=document.createElement('span');n.className='tag-count';n.textContent='0';b.appendChild(n);
    var x=document.createElement('button');x.type='button';x.className='grp-x';x.dataset.studioDelete=key;
    x.title='Delete group '+label;x.setAttribute('aria-label','Delete group '+label);x.textContent='×';
    wrap.appendChild(b);wrap.appendChild(x);nav.insertBefore(wrap,button('__untagged__')||nav.querySelector('.grp-new'));return b;
  }
  var emo={};try{emo=JSON.parse(nav.dataset.studioEmoji||'{}');}catch(e){}
  function emojiFor(label){var low=label.toLowerCase(),words=emo.words||{},pal=emo.palette||[];
    var tokens=low.split(/[ _/&+-]+/).filter(Boolean);
    for(var w in words){var ascii=w.split('').every(function(c){return c.charCodeAt(0)<128;});
      if(ascii?tokens.some(function(t){return t===w||t.replace(/s$/,'')===w;}):low.indexOf(w)>=0)return words[w];}
    if(!pal.length)return '';var n=0;for(var ch of label)n+=ch.codePointAt(0);return pal[n%pal.length];}
  function post(body){body.path=owner;body.kind=kind;
    return fetch('/_board/studio-group',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
      .then(function(r){return r.json().catch(function(){return {ok:false,err:'HTTP '+r.status};})
        .then(function(j){if(!r.ok||!j.ok)throw new Error(j.err||('HTTP '+r.status));return j;});});}
  function update(j){Object.keys(j.topics||{}).forEach(function(k){
    var row=rows.find(function(r){return r.dataset.studioKey===k;});
    if(row){row.dataset.studioTags=JSON.stringify(j.topics[k]);chips(row);}});apply(active,false);}
  function addTo(row,key){
    if(key==='__current__'){setCurrent(row,true);return;}
    var label=labelOf(key),name=row.dataset.studioName;
    post({op:'add',topic:row.dataset.studioKey,tag:label}).then(function(j){update(j);
      say(name+(j.changed?' added to ':' is already in ')+label+'.');})
      .catch(function(e){say('Could not add '+name+' to '+label+': '+e.message);});
  }
  function takeOut(row,label){var name=row.dataset.studioName;
    post({op:'remove',topic:row.dataset.studioKey,tag:label}).then(function(j){update(j);say(name+' taken out of '+label+'.');})
      .catch(function(e){say('Could not take '+name+' out of '+label+': '+e.message);});
  }
  function dropGroup(key){
    var label=labelOf(key),n=rows.filter(function(r){return tags(r).indexOf(key)>=0;}).length;
    function gone(){var b=button(key);if(b)(b.closest('.grp')||b).remove();
      apply(active===key?'':active,active===key);}
    if(!n){post({op:'delete',tag:label}).then(function(){gone();say('Group '+label+' deleted.');})
      .catch(function(e){say('Could not delete '+label+': '+e.message);});return;}
    say('');status.append('Delete group '+label+'? It comes off '+n+' '+noun+(n===1?'':'s')+'; the '+noun+'s stay. ');
    var yes=document.createElement('button');yes.type='button';yes.className='grp-ok';yes.textContent='Delete';
    var no=document.createElement('button');no.type='button';no.className='grp-cancel';no.textContent='Cancel';
    status.append(yes,' ',no);
    no.addEventListener('click',function(){say('');});
    yes.addEventListener('click',function(){say('Deleting '+label+' …');
      post({op:'delete',tag:label}).then(function(j){update(j);gone();
        say('Group '+label+' deleted. Its '+j.changed+' '+noun+(j.changed===1?' is':'s are')+' still listed.');})
        .catch(function(e){say('Could not delete '+label+': '+e.message);});});
  }
  var newBtn=nav.querySelector('.grp-new'),form=nav.querySelector('.grp-form'),input=form.querySelector('input');
  function openForm(on){form.hidden=!on;newBtn.hidden=on;if(on){input.value='';input.focus();}}
  function create(){var label=input.value.trim();
    if(!label){openForm(false);return;}
    if(label.length>30||/[`,·|*]/.test(label)||['current','all','untagged'].indexOf(label.toLowerCase())>=0){
      say('A group name is 1 to 30 characters, without ` , · | or *, and is not Current, All or Untagged.');return;}
    openForm(false);
    if(button(label.toLowerCase())){say('Group '+label+' already exists.');return;}
    post({op:'create',tag:label}).then(function(){makeGroup(label);apply(active,false);
      say('Group '+label+' made. Drag '+noun+'s onto it by ⋮⋮.');}).catch(function(e){say('Could not make '+label+': '+e.message);});}
  // groups made before they were saved on disk waited in this browser: save them once, then forget them
  if(kind==='studio'){readList(groupsKey).forEach(function(label){if(!button(label.toLowerCase()))
    post({op:'create',tag:label}).then(function(){makeGroup(label);apply(active,false);}).catch(function(){});});
  try{localStorage.removeItem(groupsKey);}catch(e){}}
  // drag a group button sideways to move it; the order is saved to studio/ (or related/) _groups.txt (b10 s02-D17)
  var dragged=false;
  nav.addEventListener('pointerdown',function(ev){
    var tab=ev.target.closest('.grp>.tab');if(!tab||ev.button!==0)return;
    var wrap=tab.parentNode,startX=ev.clientX,startY=ev.clientY,moved=false;
    function move(e){if(e.pointerId!==ev.pointerId)return;
      if(!moved&&Math.hypot(e.clientX-startX,e.clientY-startY)<6)return;
      if(!moved){moved=true;wrap.classList.add('moving');nav.classList.add('sorting');}
      var over=Array.from(nav.querySelectorAll('.grp')).find(function(g){if(g===wrap)return false;var r=g.getBoundingClientRect();
        return e.clientX>=r.left&&e.clientX<=r.right&&e.clientY>=r.top-8&&e.clientY<=r.bottom+8;});
      if(over){var r=over.getBoundingClientRect();nav.insertBefore(wrap,e.clientX<r.left+r.width/2?over:over.nextSibling);}
    }
    function finish(e){if(e.pointerId!==ev.pointerId)return;
      document.removeEventListener('pointermove',move);document.removeEventListener('pointerup',finish);document.removeEventListener('pointercancel',finish);
      if(!moved)return;
      wrap.classList.remove('moving');nav.classList.remove('sorting');dragged=true;setTimeout(function(){dragged=false;},0);
      var order=Array.from(nav.querySelectorAll('.grp>.tab')).map(function(b){return b.dataset.studioLabel;});
      post({op:'order',groups:order}).then(function(){say('Group order saved.');})
        .catch(function(e2){say('Could not save the group order: '+e2.message);});
    }
    document.addEventListener('pointermove',move);document.addEventListener('pointerup',finish);document.addEventListener('pointercancel',finish);
  });
  newBtn.addEventListener('click',function(){openForm(true);});
  form.querySelector('.grp-ok').addEventListener('click',create);
  form.querySelector('.grp-cancel').addEventListener('click',function(){openForm(false);});
  input.addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();create();}else if(e.key==='Escape'){openForm(false);}});
  nav.addEventListener('click',function(ev){
    var del=ev.target.closest('[data-studio-delete]');if(del){ev.preventDefault();dropGroup(del.dataset.studioDelete);return;}
    var b=ev.target.closest('[data-studio-tag]');if(!b||dragged)return;
    apply(b.dataset.studioTag===active?'':b.dataset.studioTag,true);});
  list.addEventListener('click',function(ev){var x=ev.target.closest('.tag-x');if(!x)return;
    ev.preventDefault();ev.stopPropagation();var row=x.closest('details[data-studio-key]'),chip=x.closest('.chip');
    if(row&&chip)takeOut(row,chip.dataset.tag);});
  if(source)source.addEventListener('change',function(){apply(active,true);});
  rows.forEach(function(row){
    row.querySelector('.studio-current').addEventListener('click',function(ev){
      ev.preventDefault();ev.stopPropagation();setCurrent(row,!current.has(row.dataset.studioKey));});
    var handle=row.querySelector('.studio-drag');
    if(!handle)return;                      // a theme's own Report card (b10 s05): not draggable, its groups fixed
    handle.addEventListener('click',function(ev){ev.preventDefault();ev.stopPropagation();});
    handle.addEventListener('pointerdown',function(ev){
      if(ev.button!==0)return;ev.preventDefault();ev.stopPropagation();
      var startX=ev.clientX,startY=ev.clientY,ghost=null,moved=false,hot=null;
      if(handle.setPointerCapture)handle.setPointerCapture(ev.pointerId);
      function under(x,y){return buttons().find(function(b){var k=b.dataset.studioTag;if(k==='__untagged__')return false;
        var r=b.getBoundingClientRect();return x>=r.left&&x<=r.right&&y>=r.top&&y<=r.bottom;})||null;}
      function mark(b){if(hot)hot.classList.remove('drop-ready');hot=b;if(hot)hot.classList.add('drop-ready');}
      function move(e){
        if(e.pointerId!==ev.pointerId)return;
        if(!moved&&Math.hypot(e.clientX-startX,e.clientY-startY)<6)return;
        if(!moved){moved=true;row.classList.add('dragging');ghost=document.createElement('div');
          ghost.className='studio-drag-preview';ghost.textContent=row.dataset.studioName;document.body.appendChild(ghost);}
        ghost.style.left=(e.clientX+12)+'px';ghost.style.top=(e.clientY+12)+'px';
        mark(under(e.clientX,e.clientY));
      }
      function finish(e){
        if(e.pointerId!==ev.pointerId)return;
        document.removeEventListener('pointermove',move);document.removeEventListener('pointerup',finish);document.removeEventListener('pointercancel',finish);
        row.classList.remove('dragging');mark(null);if(ghost)ghost.remove();
        var b=moved&&e.type==='pointerup'?under(e.clientX,e.clientY):null;
        if(b)addTo(row,b.dataset.studioTag);
      }
      document.addEventListener('pointermove',move);document.addEventListener('pointerup',finish);document.addEventListener('pointercancel',finish);
    });
  });
  function restore(){var url=new URL(location.href),group=url.searchParams.get(pre+'group');
    var key=url.searchParams.get(pre+'tag')||(group==='current'?'__current__':'');
    if(source){var wanted=url.searchParams.get('studio_source')||'__all__';
      source.value=Array.from(source.options).some(function(o){return o.value===wanted;})?wanted:'__all__';}
    var target=hashTarget();
    if(target&&rows.indexOf(target)>=0){if(!matches(target,key))key='';if(source)source.value='__all__';}
    apply(key,false);
  }
  restore();window.addEventListener('popstate',restore);
  window.addEventListener('storage',function(ev){
    if(ev.key===storageKey){current=read();apply(active,false);}});
});
function tlGaps(tl){
  // one real axis (JL 261012: "show the days between them"): a day with nothing shown, between two that have
  // something, stays as a short row with a hollow dot; a run of more than 3 is one row, "N quiet days".
  // Before the first such day and after the last, nothing shows. The chart counts what the group shows; the
  // list below also what is picked.
  var wrap=tl.querySelector('.tl-wrap');if(!wrap)return;
  var picking=wrap.classList.contains('picking')&&wrap.dataset.level==='days';
  function lay(rs,full){var on=rs.map(full),a=on.indexOf(true),b=on.lastIndexOf(true);
    rs.forEach(function(r,j){var t=r.querySelector('time');if(t.dataset.label===undefined)t.dataset.label=t.textContent;
      t.textContent=t.dataset.label;r.hidden=a<0||j<a||j>b;r.classList.toggle('tl-quiet',!on[j]);});
    for(var j=a;a>=0&&j<=b;j++){if(on[j])continue;var k=j;while(k<=b&&!on[k])k++;
      if(k-j>3){rs[j].querySelector('time').textContent=(k-j)+' quiet days';for(var m=j+1;m<k;m++)rs[m].hidden=true;}j=k;}}
  lay(Array.from(tl.querySelectorAll('.tl-mrow')),function(r){return Number(r.dataset.tlN||0)>0;});
  lay(Array.from(tl.querySelectorAll('.tl-day')),function(d){
    return !!d.querySelector('.tl-topic:not([hidden])'+(picking?':not(.tl-off)':''));});
}
document.querySelectorAll('.studio-timeline .tl-levels').forEach(function(nav){
  // how much the Timeline shows: Days · Topics · Everything (JL 261011), remembered in this browser
  var axis=nav.closest('.tl-wrap'),saved='';if(!axis)return;
  function show(level){axis.dataset.level=level;nav.querySelectorAll('[data-tl-level]').forEach(function(b){
    b.setAttribute('aria-pressed',String(b.dataset.tlLevel===level));});tlGaps(axis.closest('.studio-timeline'));}
  try{saved=localStorage.getItem('workbench.timeline.level.v1')||'';}catch(e){}
  if(nav.querySelector('[data-tl-level="'+saved+'"]'))show(saved);
  nav.addEventListener('click',function(ev){var b=ev.target.closest('[data-tl-level]');if(!b)return;show(b.dataset.tlLevel);
    try{localStorage.setItem('workbench.timeline.level.v1',b.dataset.tlLevel);}catch(e){}});});
document.querySelectorAll('.studio-timeline .tl-map').forEach(function(map){
  // the chart's columns: the topic groups or the topics (JL 261011), remembered in this browser. A picked
  // group shows its topics; by group shows every group, so it unpicks the group (JL 261012: "我好像没法选了")
  var nav=map.closest('.tl-wrap').querySelector('.tl-cols'),saved='',pref=map.dataset.cols;if(!nav)return;
  var bar='.studio-topics:not([data-group-kind]) .studio-filters';
  function on(){return document.querySelector(bar+' [data-studio-tag].on');}
  // a group picked from here hides or shows the topic cards above, so the page grows or shrinks over the
  // Timeline; keep its toolbar where it was on screen (JL 261012: "它会跳到最上面，而不是留在 timeline 这里")
  var levels=map.closest('.tl-wrap').querySelector('.tl-levels');
  function keep(fn){var y=levels.getBoundingClientRect().top;fn();
    var d=levels.getBoundingClientRect().top-y;if(d)window.scrollBy(0,d);}
  function cols(){var c=on()?'topics':pref;map.dataset.cols=c;nav.querySelectorAll('[data-tl-cols]').forEach(function(b){
    b.setAttribute('aria-pressed',String(b.dataset.tlCols===c));});}
  try{saved=localStorage.getItem('workbench.timeline.cols.v1')||'';}catch(e){}
  if(saved==='groups'||saved==='topics')pref=saved;
  cols();
  nav.addEventListener('click',function(ev){var b=ev.target.closest('[data-tl-cols]');if(!b)return;pref=b.dataset.tlCols;
    try{localStorage.setItem('workbench.timeline.cols.v1',pref);}catch(e){}
    var g=on();keep(function(){if(pref==='groups'&&g)g.click();cols();});});
  // the Timeline's group picker clicks the bar's own button: picking the picked one again, or All, unpicks it
  var strip=map.closest('.tl-wrap').querySelector('.tl-groups');
  if(strip)strip.addEventListener('click',function(ev){var x=ev.target.closest('[data-tl-tag]');if(!x)return;
    var k=x.dataset.tlTag,t=k?document.querySelector(bar+' [data-studio-tag="'+CSS.escape(k)+'"]'):on();
    if(t)keep(function(){t.click();});});
  // pick topics in the chart (JL 261011: "we can select the topics we are interest in we show there content"):
  // their decisions, sessions and notes show under it, on the same axis; pick again to drop one
  var wrap=map.closest('.tl-wrap'),list=wrap.querySelector('.tl-list'),line=wrap.querySelector('.tl-picked'),picked=new Set();
  function pick(){wrap.classList.toggle('picking',picked.size>0);
    map.querySelectorAll('.tl-col,.tl-cell').forEach(function(c){c.classList.toggle('on',picked.has(c.dataset.tlKey));});
    list.querySelectorAll('.tl-topic').forEach(function(t){t.classList.toggle('tl-off',!picked.has(t.dataset.tlKey));});
    tlGaps(wrap.closest('.studio-timeline'));
    line.textContent='';if(!picked.size)return;
    var names=Array.from(map.querySelectorAll('.tl-col')).filter(function(c){return picked.has(c.dataset.tlKey);})
      .map(function(c){return c.title||c.textContent;});
    line.appendChild(document.createTextNode('Reading '+names.join(' · ')));
    var x=document.createElement('button');x.type='button';x.textContent='Clear';
    x.addEventListener('click',function(){picked.clear();pick();});line.appendChild(x);}
  // a group or source picked anywhere: the columns follow, and a picked topic that no longer shows is dropped
  map.closest('.studio-timeline').addEventListener('tl-shown',function(){cols();
    map.querySelectorAll('.tl-col[hidden]').forEach(function(c){picked.delete(c.dataset.tlKey);});pick();});
  map.addEventListener('click',function(ev){var g=ev.target.closest('.tl-gcol,.tl-gb');
    if(g){var key=(g.closest('[data-tl-group]')||g).dataset.tlGroup;
      var t=document.querySelector(bar+' [data-studio-tag="'+CSS.escape(key)+'"]');
      keep(function(){if(t&&!t.classList.contains('on'))t.click();cols();});return;}
    var c=ev.target.closest('.tl-col,.tl-cell');if(!c||(c.classList.contains('tl-cell')&&!c.querySelector('.tl-b')))return;
    ev.preventDefault();var k=c.dataset.tlKey;if(picked.has(k))picked.delete(k);else picked.add(k);pick();});});
document.querySelectorAll('.studio-timeline .tl-name').forEach(function(a){a.addEventListener('click',function(ev){
  // a topic's name in the Timeline opens its row above
  var d=document.getElementById(decodeURIComponent(a.hash.slice(1)));if(!d)return;
  ev.preventDefault();d.open=true;load(d);d.scrollIntoView({block:'start'});history.replaceState(null,'',a.hash);});});
document.querySelectorAll('.studio-folder').forEach(function(box){
  // Folder (b10 s09): a folder's rows load the first time it is opened, from ?view=dir (toggle does not bubble)
  box.addEventListener('toggle',function(ev){var d=ev.target;
    if(!d.matches('details[data-dir]')||!d.open||d.dataset.loaded)return;
    var ul=d.querySelector(':scope>ul');d.dataset.loaded='1';ul.innerHTML='<li class=mut>Loading…</li>';
    fetch('/_board/workbench?'+new URLSearchParams({view:'dir',path:d.dataset.dir}))
      .then(function(r){if(!r.ok)throw r.status;return r.text();}).then(function(h){ul.innerHTML=h;})
      .catch(function(){ul.innerHTML='<li class=mut>This folder could not be read.</li>';delete d.dataset.loaded;});},true);
  // past 300 rows a folder stops; its button loads them all
  box.addEventListener('click',function(ev){var b=ev.target.closest('.fd-more button');if(!b)return;
    var ul=b.closest('ul');b.disabled=true;b.textContent='Loading…';
    fetch('/_board/workbench?'+new URLSearchParams({view:'dir',path:b.dataset.dir,all:'1'}))
      .then(function(r){if(!r.ok)throw r.status;return r.text();}).then(function(h){ul.innerHTML=h;})
      .catch(function(){b.disabled=false;b.textContent='Could not load; try again';});});});
document.querySelectorAll('details.topic .draw-edit').forEach(function(b){b.addEventListener('click',function(ev){
  ev.preventDefault();ev.stopPropagation();
  var d=b.closest('details'),f=d.querySelector(':scope > .st-pane:not([hidden]) > iframe')||d.querySelector('iframe'),on=b.textContent==='Edit';
  d.open=true;f.src=on?f.dataset.edit:f.dataset.src;b.textContent=on?'Finish editing':'Edit';});});
// a topic with a structured side (mNN, haipipe-studio's mind map): Free | Structured, one pane a side, the mind map drawn and
// edited in place as the draft's §1 map; Edit (the free canvas) shows only on Free; the ↗ opens the side showing; the
// card remembers the choice in this browser
document.querySelectorAll('details.topic[data-sides]').forEach(function(d){
  var key='workbench.studio.side.v1:'+d.id,bar=d.querySelector(':scope > summary .st-side');
  function show(side,save){
    bar.querySelectorAll('[data-side]').forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.side===side));});
    d.querySelectorAll(':scope > .st-pane').forEach(function(p){p.hidden=p.dataset.side!==side;
      var f=p.querySelector(':scope > iframe');if(f&&f.dataset.edit&&f.getAttribute('src')===f.dataset.edit)f.src=f.dataset.src;});
    var ed=d.querySelector(':scope > summary .draw-edit');
    if(ed){ed.hidden=(ed.dataset.sides||'').split(' ').indexOf(side)<0;ed.textContent='Edit';}
    var a=d.querySelector(':scope > summary a.side-link'),h=a&&a.getAttribute('data-href-'+side);
    if(a){a.hidden=!h;if(h){a.href=h;a.dataset.pop=a.getAttribute('data-pop-'+side);}}
    d.dataset.side=side;if(save){try{localStorage.setItem(key,side);}catch(e){}}load(d);if(window.mmDraw)setTimeout(window.mmDraw,0);}
  var saved=null;try{saved=localStorage.getItem(key);}catch(e){}
  var ok=function(s){var b=bar.querySelector('[data-side="'+s+'"]');return b&&!b.disabled;};
  show(saved&&ok(saved)?saved:d.dataset.side,false);
  bar.addEventListener('click',function(ev){var b=ev.target.closest('[data-side]');if(!b||b.disabled)return;
    ev.preventDefault();ev.stopPropagation();d.open=true;show(b.dataset.side,true);});});
document.querySelectorAll('.rp-live').forEach(function(b){b.addEventListener('click',function(){
  var f=b.querySelector('iframe');if(f&&f.hasAttribute('inert')){f.removeAttribute('inert');b.classList.add('on');}});});
var t=hashTarget();if(t&&t.tagName==='DETAILS'){for(var a=t;a;a=a.parentElement){if(a.tagName==='DETAILS'){a.open=true;load(a);}}t.scrollIntoView({block:'start'});}
})();
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


# an old theme page's view -> the frame Space it became (cowork-board, work-board, discovery-board)
OLD_VIEW_SPACE = {"scope": "Description", "block": "Description", "people": "Description",
                  "resources": "Description", "work": "Work Details", "jobs": "Work Details",
                  "tasks": "Work Details", "task": "Work Details", "papers": "Work Details",
                  "questions": "Audience Report", "reports": "Audience Report", "check": "Audience Report",
                  "runs": "Runs", "delivery": "Delivery", "related": "Related"}


def frame_redirect(handler, block: Path, root: Path, view: str = "") -> None:
    """Send an old theme page's Block to the shared frame (JL 261011: every workbench has the one
    structure, Studio | Block · Job · Task | Delivery). Its pop-outs, reports and JSON stay where they are;
    an `--only` host serves no frame and keeps its own page."""
    query = {"path": _rel(block.resolve(), root.resolve())}
    space = OLD_VIEW_SPACE.get((view or "").lower(), "")
    if space and space != "Description":
        query["space"] = space
    handler.send_response(302)
    handler.send_header("Location", ROUTE + "?" + urlencode(query))
    handler.send_header("Content-Length", "0")
    handler.end_headers()


def href(folder: Path, root: Path, theme: Theme, space: str = "", sub: str = "", *, studio: bool = False) -> str:
    query = {"path": _rel(folder, root)}
    if theme.name != "vanilla":
        query["theme"] = theme.name
    if space:
        query["space"] = space
    if sub:
        query["sub"] = sub
    if studio:
        query["studio"] = "1"
    return ROUTE + "?" + urlencode(query)


def _level_row(theme: Theme, root: Path, folder: Path, level: str, space: str, sub: str = "", *, studio: bool = False) -> str:
    """Guide (mounted first) · Studio | Block · Job ▾ · Task ▾ | Delivery; context stays in the title.
    Studio and Delivery are the Block's shared views (b10 s09-D05, JL 261010: "Studio | Block Job Task |
    Delivery"); Related opens the Studio, where it folds under the topics (b10 s04, JL 261011: "I might
    just want to keep Guide, Studio | Block, Job, Task | Delivery"); a level button goes back to its work view."""
    up = chain(folder, root)
    studio = studio or space in ("Idea Studio", "Studio") or space in IN_STUDIO
    delivery = space == "Delivery" and not studio
    if delivery or space in IN_STUDIO:
        sub = ""
    space = "Description" if space in ("Idea Studio", "Studio", "Delivery") + IN_STUDIO else space
    shared_on = studio or delivery
    current = ' aria-current="page"'
    tab = lambda label, url, on: (f'<a class="tab{" on" if on else ""}" href="{_e(url)}"'
                                  f'{current if on else ""}>{label}</a>')
    parts = [tab("Studio", href(folder, root, theme, space, sub, studio=True), studio),
             '<span class=bar></span>']
    for lv in theme.levels:
        name = theme.level_name(lv)
        here = up.get(lv)
        on = " on" if lv == level and not shared_on else ""
        if lv == "Block":
            if here:
                parts.append(f'<a class="tab{on}" href="{_e(href(here, root, theme, space, sub if here == folder else ""))}" '
                             f'title="{_e(here.name)}">{_e(name)}</a>')
            continue
        parent = up.get({"Job": "Block", "Task": "Job"}[lv])
        options = children(parent, {"Job": "Block", "Task": "Job"}[lv]) if parent else []
        if not options:                          # the tab stays, greyed, so every page has the same row
            if theme.hide_empty_levels:
                continue
            parts.append(f'<select disabled aria-label="{_e(name)}"><option>{_e(name)} ▾</option></select>')
            continue
        if here and (lv != level or shared_on):
            # below this level (a Task under its Job): the open item is a button that goes up to its tab, and a
            # ▾ beside it switches to a sibling; a dropdown alone ignores a click on the item already picked
            # (JL 261008: "I want to click the job button at the top, but it is not react")
            parts.append(f'<span class=lvl><a class=tab href="{_e(href(here, root, theme, space, sub if here == folder else ""))}" title="{_e(here.name)}">'
                         f'{_e(_label(theme, here))}</a><select aria-label="Switch {_e(name)}" '
                         f'onchange="if(this.value)location.href=this.value"><option value="" selected>▾</option>'
                         f'{_options(theme, root, space, options, None)}</select></span>')
            continue
        opts = _options(theme, root, space, options, here, sub if lv == level else "")
        pick = "" if here else f'<option value="" selected>{_e(name)} ▾</option>'
        parts.append(f'<select class="{on.strip()}" aria-label="{_e(name)}" '
                     f'onchange="if(this.value)location.href=this.value">{pick}{opts}</select>')
    parts += ['<span class=bar></span>', tab("Delivery", href(folder, root, theme, "Delivery"), delivery)]
    return '<nav class="row levels">' + "".join(parts) + "</nav>"


def short_name(name: str, most: int = 26) -> str:
    """A folder's name for the Job ▾ / Task ▾ dropdown: the folder name exactly as it is on disk (b10 s32-D15,
    JL 261011: "could we do not use · … like the folder name of the j01"). A folder name is made readable where it
    is made (a design Job is jNN_<goal name>_<method name>), so the screen shows it as is, never cut to its ids.
    `most` is kept for callers that pass it; nothing is cut."""
    return name


def _label(theme: Theme, folder: Path) -> str:
    """A folder's label in the level row: the theme's, else its short name."""
    got = None
    if theme.option:
        try:
            got = theme.option(folder)
        except Exception:                        # a theme's label must not break the frame
            got = None
    return got[0] if got else short_name(folder.name)


def _options(theme: Theme, root: Path, space: str, options: list, here, sub: str = "") -> str:
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
            f'<option value="{_e(href(o, root, theme, space, sub if o == here else ""))}" title="{_e(o.name)}"'
            f'{" selected" if o == here else ""}>{_e(label)}</option>')
    return "".join("".join(opts) if not g else f'<optgroup label="{_e(g)}">{"".join(opts)}</optgroup>'
                   for g, opts in groups.items())


def _spaces_row(theme, root, folder, space, sub="", views=None) -> str:
    out, last = [], None
    for name, group, optional in SPACES:
        if name in TOP_ROW or name in IN_STUDIO:  # the top row's own, or folded in the Studio (b10 s09-D05, s04)
            continue
        if last is not None and group != last:
            out.append('<span class=bar></span>')
        last = group
        cls = "tab" + (" on" if name == space else "") + (" opt" if optional else "")
        label = SPACE_LABELS.get(name, name)
        shared = (sub if space in ("Audience Report", "Work Details")
                  and name in ("Audience Report", "Work Details")
                  and sub in (views or {}).get(name, Space()).subspaces else "")
        out.append(f'<a class="{cls}" href="{_e(href(folder, root, theme, name, shared))}">{_e(label)}</a>')
    return '<nav class="row spaces">' + "".join(out) + "</nav>"


def delivery_parts(block: Path) -> list:
    """[(source folder, depth)] for each Job, and each Task under it, that has a part in the Block's
    delivery/ (b10 s03-D06): the path is the link, delivery/jNN_<job>/tNN_<task>/ -> jNN_<job>/tNN_<task>/."""
    out = []
    for job in children(block, "Block"):
        tasks = [t for t in children(job, "Job") if delivery_dir(t).is_dir()]
        if delivery_dir(job).is_dir() or tasks:
            out.append((job, 1))
            out += [(t, 2) for t in tasks]
    return out


def _delivery_row(theme, root, block: Path, folder: Path) -> str:
    """Delivery's source row: Block, then each Job with a part (and the open Job or Task even before it has
    one); the open folder is picked. A Task shows beside its Job, `jNN › tNN`."""
    up = chain(folder, root)
    shown = [(f, d) for f, d in delivery_parts(block) if d == 1 or f in (folder, up.get("Task"))]
    for lv, d in (("Job", 1), ("Task", 2)):              # the open one, even with nothing built yet
        f = up.get(lv)
        if f and f not in [x for x, _ in shown]:
            at = next((i + 1 for i, (x, _) in enumerate(shown) if x == up.get("Job")), len(shown))
            shown.insert(at if lv == "Task" else len(shown), (f, d))
    current = ' aria-current="true"'                  # the page's own mark stays on the top row's Delivery
    chip = lambda f, label: (f'<a class="tab{" on" if f == folder else ""}" href="{_e(href(f, root, theme, "Delivery"))}"'
                             f'{current if f == folder else ""}>{_e(label)}</a>')
    parts = [chip(block, theme.level_name("Block"))]
    for f, d in shown:
        parts.append(chip(f, (f.parent.name.split("_", 1)[0] + " › " if d == 2 else "") + _label(theme, f)))
    return '<nav class="row subs delivery-parts">' + "".join(parts) + "</nav>"


def delivery_by_source(theme, block: Path, root: Path) -> str:
    """The Block's Delivery, by source: one row per Job's and Task's part, its files, and links to that part
    and back down to its folder."""
    rows, parts = [], delivery_parts(block)
    task_parts = {delivery_dir(f) for f, d in parts if d == 2}
    for f, d in parts:
        part = delivery_dir(f)                   # a Job's own files: not its Tasks' parts under it
        n = sum(1 for x in part.rglob("*") if x.is_file() and not any(t != part and t in x.parents for t in task_parts)) \
            if part.is_dir() else 0
        rows.append((("└ " if d == 2 else "") + _link(href(f, root, theme, "Delivery"),
                                                                       part.relative_to(block).as_posix() + "/"),
                     _link(ROUTE + "?" + urlencode({"path": _rel(f, root)}), f.name), _e(n)))
    if not rows:
        return ""
    return "<h3>By source</h3>" + _table(("part", "from", "files"), rows)


# ── Delivery: one card per result under the group bar (b10 s03-D08; JL 261012: "for the delivery, we should
# also have the group tags as well, and have the delivery card, similar to the studio") ──────────────────────
# A result is a file a reader opens; its twins (a .docx and the .pdf beside it) are one card. Build files, logs
# and the pieces a build puts together are not results (the same rule the s03 drawing counts by).
DELIVERY_OPENS = {".pdf": "PDF", ".docx": "Word", ".pptx": "Deck", ".html": "Web page", ".xlsx": "Sheet",
                  ".png": "Image"}
DELIVERY_PIECES = {"history", "__pycache__", "svg", "displays", "sections", "appendices", "draft-bibliography",
                   "figures", "draft-sections"}
RESULT_GROUPS = "result_groups.md"          # delivery/result_groups.md: | result | group |, the groups a person added


def _result_groups(deliv: Path) -> dict:
    """{result key: [groups]} from delivery/result_groups.md."""
    f = deliv / RESULT_GROUPS
    out = {}
    if not f.is_file():
        return out
    for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("|") else []
        if len(cells) >= 2 and cells[0] not in ("result", "") and not set(cells[0]) <= set("-: "):
            out[cells[0].strip("`")] = _split_tags(cells[1])
    return out


def _delivery_set_groups(deliv: Path, key: str, groups: list) -> None:
    """Write one result's added groups into delivery/result_groups.md (a row per result a person grouped;
    no groups, no row)."""
    rows = _result_groups(deliv)
    rows[key] = groups
    lines = ["Result groups · written by the workbench", "========================================", "",
             "The groups a person gave each result in Delivery (drag a card onto a group). A result's file kind",
             "(PDF, Word, Deck, ...) is its fixed group and is not written here; delivery/_groups.txt keeps the",
             "buttons' order.", "", "| result | group |", "|---|---|"]
    kept = [f"| `{k}` | {', '.join(v)} |" for k, v in sorted(rows.items()) if v]
    if not kept:                                  # the last group taken out: no file left behind
        (deliv / RESULT_GROUPS).unlink(missing_ok=True)
        return
    deliv.mkdir(exist_ok=True)
    (deliv / RESULT_GROUPS).write_text("\n".join(lines + kept) + "\n", encoding="utf-8")


# A deliverable is one item (JL 261014: "for the delivery, I think we just make the item to be the same ... all of
# them should one Delivery Item, and within it, we can see different versions"): its lanes (a Section's web/,
# word/ and latex/ builds; a deck's slide/ and its picture in render/) and its versions (`-v1` ... `-v12`) fold into
# it. A version is one stem, its twins and its lanes; which stems are versions of one item is `version_roots`.
DELIVERY_LANES = {"latex", "word", "slide", "slides", "render", "web"}
_VERSION = re.compile(r"^(?P<base>.+?)[-_ .]v(?P<n>\d+)$", re.I)


def _version_of(stem: str) -> tuple:
    """(base, number) of a stem: `Deck-Visual-v12` -> ("Deck-Visual", 12), `Deck` -> ("Deck", None)."""
    m = _VERSION.match(stem)
    return (m.group("base"), int(m.group("n"))) if m else (stem, None)


def version_roots(stems) -> dict:
    """{stem: the item it is a version of}, for the names in one folder; the one version rule Delivery and Related
    share (b10 s03-D10; JL 261014: "一个东西，我们会有一个 version 又一个 version ... item 谁谁谁，然后里面可能有 version 1、
    version 2、version 3"). Stems that differ only by `-v<N>` are one item; a numbered stem whose name starts with
    another's joins it (`…-Evaluation-Visual-v12` → `…-Evaluation`); then an unnumbered variant of an item that has
    numbers joins too (`…-Workflow-Symmetric` → `…-Workflow`). Names with no number and no numbered kin stay apart
    (`FairGlucose-npjDM-SI` is not a version of `FairGlucose-npjDM`)."""
    families = {}
    for stem in dict.fromkeys(stems):
        base, n = _version_of(stem)
        families.setdefault(base, []).append((stem, n))
    root_of = {b: b for b in families}
    numbered = lambda members: any(n is not None for _, n in members)
    for base, members in families.items():
        heads = [b for b in families if b != base and base.startswith(b + "-")]
        if numbered(members) and heads:
            root_of[base] = max(heads, key=len)

    def final(b):
        while root_of[b] != b:
            b = root_of[b]
        return b
    with_numbers = {final(b) for b, members in families.items() if numbered(members)}
    for base in families:
        if root_of[base] == base and base not in with_numbers:
            heads = [b for b in families if b != base and base.startswith(b + "-") and final(b) in with_numbers]
            if heads:
                root_of[base] = max(heads, key=len)
    return {stem: final(base) for base, members in families.items() for stem, _ in members}


def version_label(stem: str, root: str, many: bool) -> str:
    """What a version's button says: the part of its name after the item's (`Visual-v12`, `v5`)."""
    tail = stem[len(root):].lstrip("-_ .") if stem.startswith(root) else stem
    return tail or ("first" if many else "")


def version_panes(versions: list, pane) -> str:
    """A row of version buttons, newest first and picked, over one pane per version (`pane(version)` fills it);
    a single version is its pane alone. Each version is a dict with at least `label` and `when`."""
    row = ""
    if len(versions) > 1:
        row = ('<nav class="row dv-vers" aria-label="Versions">' + "".join(
            f'<button type=button class=tab data-dv="{n}" aria-pressed="{"true" if n == 0 else "false"}">'
            f'{_e(v["label"])} <span class=tag-count>{datetime.date.fromtimestamp(v["when"]).strftime("%m-%d")}</span>'
            f'</button>' for n, v in enumerate(versions)) + "</nav>")
    return row + "".join(f'<div class=dv-pane data-dv="{n}"{"" if n == 0 else " hidden"}>{pane(v)}</div>'
                         for n, v in enumerate(versions))


def delivery_items(block: Path, part: Path | None = None) -> list:
    """The deliverables under the Block's delivery/ (or under one part of it), newest first: {key, title, files
    (every file of every version), fixed (their kinds), groups, source (jNN_<job> › tNN_<task>, or the Block),
    folder (the source folder), when, size (the newest version's), versions}. Each version is {label, number,
    files, when, size}, newest first."""
    deliv = block / "delivery"
    top = part if part is not None else deliv
    if not top.is_dir():
        return []
    builds = {}                                   # (where, stem) -> files: one version of one deliverable
    for f in sorted(top.rglob("*")):
        rel = f.relative_to(deliv)
        if (not f.is_file() or f.name.startswith((".", "_")) or f.suffix.lower() not in DELIVERY_OPENS
                or set(rel.parts[:-1]) & DELIVERY_PIECES or any(x.startswith((".", "_")) for x in rel.parts[:-1])
                or f.stem == "master" or f.stem.endswith("-view")):
            continue
        where = f.parent.parent if f.parent.name.lower() in DELIVERY_LANES and f.parent != deliv else f.parent
        stem = f.stem.removesuffix("-tracked")
        if stem == "index" and where != deliv:    # a web lane's page is named by its part (t04_methods/web/index)
            stem = where.name
        builds.setdefault((where, stem), []).append(f)
    by_where = {}
    for where, stem in builds:
        by_where.setdefault(where, []).append(stem)
    grouped = {}                                  # (where, item) -> [(stem, number)]
    for where, stems in by_where.items():
        roots = version_roots(stems)
        for stem in stems:
            grouped.setdefault((where, roots[stem]), []).append((stem, _version_of(stem)[1]))
    added, order = _result_groups(deliv), list(DELIVERY_OPENS.values())
    out = []
    for (where, base), members in grouped.items():
        versions = []
        for stem, n in members:
            files = sorted(builds[(where, stem)], key=lambda f: (
                -1 if f.suffix.lower() == ".docx" else order.index(DELIVERY_OPENS[f.suffix.lower()]), f.parent.name, f.name))
            versions.append({"label": version_label(stem, base, len(members) > 1), "number": n, "files": files,
                             "when": max(f.stat().st_mtime for f in files), "size": sum(f.stat().st_size for f in files)})
        versions.sort(key=lambda v: -v["when"])
        files = [f for v in versions for f in v["files"]]
        key = (where / base).relative_to(deliv).as_posix()
        kinds = [k for k in order if any(DELIVERY_OPENS[f.suffix.lower()] == k for f in files)]
        olds = [(f.parent / f.stem.removesuffix("-tracked")).relative_to(deliv).as_posix() for f in files]
        mine = [g for k in [key] + olds for g in added.get(k, [])]
        src = [p for p in where.relative_to(deliv).parts[:2] if _PREFIXED.match(p)]
        source = block.joinpath(*src) if src else block
        out.append({"key": key, "title": base, "files": files, "fixed": kinds,
                    "groups": kinds + [g for g in dict.fromkeys(mine) if g not in kinds],
                    "source": " › ".join(src) or "the Block", "folder": source,
                    "when": versions[0]["when"], "size": versions[0]["size"], "versions": versions})
    return sorted(out, key=lambda i: -i["when"])


def _size(n: int) -> str:
    return f"{n / 1e6:.1f} MB" if n >= 1e6 else f"{max(1, round(n / 1e3))} KB"


def _delivery_preview(files: list, root: Path) -> str:
    """One version, shown: a PDF or web page in a frame, a picture, a deck drawn slide by slide, a Word file read
    from its package; else how to open it."""
    url = lambda f: "/" + _rel(f, root)
    frame_of = lambda src, name: (f'<iframe class=st-frame title="{_e(name)}" data-src="{_e(src)}" '
                                  f'referrerpolicy=no-referrer></iframe>')
    for ext in (".pdf", ".html", ".png", ".pptx", ".docx"):
        f = next((f for f in files if f.suffix.lower() == ext), None)
        if f is None:
            continue
        if ext == ".png":
            return f'<img class=related-img loading=lazy alt="{_e(f.name)}" src="{_e(url(f))}">'
        if ext in (".pptx", ".docx"):           # read from the package (JL 261014: "the preview of the slide as well")
            return frame_of(ROUTE + "?" + urlencode({"view": ext[1:], "path": _rel(f, root)}), f.name)
        return frame_of(url(f), f.name)
    kind = DELIVERY_OPENS[files[0].suffix.lower()] if files else "this"
    return f'<p class="mut none">No preview of a {_e(kind)} file here: open it from the links above.</p>'


def _delivery_links(files: list, root: Path) -> str:
    """Each file of one version, as a pop-out link named by its kind (and its lane when two share a kind)."""
    kinds = [DELIVERY_OPENS[f.suffix.lower()] for f in files]
    return " ".join(pop("/" + _rel(f, root), f.name,
                        k + (f" · {f.parent.name}" if kinds.count(k) > 1 else "") + " ↗")
                    for f, k in zip(files, kinds))


def _delivery_card(i: dict, root: Path) -> str:
    """One closed row per deliverable, as a Studio topic's: ⋮⋮, its name and groups and its newest version's files ↗,
    with no line under the name and no Add to Current (JL 261014: "too hard to read, why you give so many unnecessary
    information", then "remove the add to current, this is not good to see": where it came from, when it was built,
    its size and its sends are gone, delivery.md keeps the sends; a card still drops on Current by its ⋮⋮); opened,
    a row of its versions (newest first, picked) over the picked version itself."""
    attrs, handle, _, chips = _group_parts(i["key"], i["title"], i["groups"], noun="result", fixed=i["fixed"])
    versions = i.get("versions") or [{"label": "", "number": None, "files": i["files"], "when": i["when"],
                                      "size": i["size"]}]
    newest = versions[0]
    many = len(versions) > 1
    body = version_panes(versions, lambda v: (f'<p class="mut dv-files">{_e(v["label"])}: '
                                              f'{_delivery_links(v["files"], root)}</p>' if many else "")
                         + _delivery_preview(v["files"], root))
    return (f'<details class=topic data-studio-tags="{_e(json.dumps(i["groups"]))}"{attrs}><summary>{handle}'
            f'<span class=related-head><b>{_e(i["title"])}</b>{chips}</span>'
            f'<span class=topic-pop>{_delivery_links(newest["files"], root)}</span></summary>'
            f'{body}</details>')


def delivery_view(folder: Path, root: Path, theme=None) -> str:
    """Delivery's cards: every result of the Block (from the Block), or of the picked Job's or Task's part,
    under the Block's group bar; the file kinds are fixed groups, + Group adds a person's own."""
    block = delivery_owner(folder)
    items = delivery_items(block, None if folder.resolve() == block.resolve() else delivery_dir(folder))
    if not items:
        return ""
    theme = theme or VANILLA
    extra = ()
    if theme.delivery_fixed:                       # the theme's own groups (no ×) and reading order
        placed = [(i, theme.delivery_fixed(i)) for i in items]
        for i, (groups, _) in placed:
            i["fixed"] = list(groups) + i["fixed"]
            i["groups"] = list(groups) + [g for g in i["groups"] if g not in groups]
        extra = tuple(dict.fromkeys(g for _, (groups, _) in placed for g in groups))
        items = [i for i, _ in sorted(placed, key=lambda p: (p[1][1], -p[0]["when"]))]
    rows = "".join(_delivery_card(i, root) for i in items)
    kinds = extra + tuple(k for k in DELIVERY_OPENS.values() if any(k in i["fixed"] for i in items))
    return group_list(block, root, "delivery", [i["groups"] for i in items], rows, fixed=kinds)


# ── Work: the Jobs, their Tasks, each Task's Runs and what each Run found, one tree (JL 261012: "for the work, I
# want it can show the job to the task to the run results, show all the content. and there are special tasks
# that human need to interact with as well") ────────────────────────────────────────────────────────────────
def task_action(task: Path, root: Path, theme=None):
    """(label, href) when a person works inside this Task, else None: the theme's own rule (a labeling Task's
    rounds), or a draft a person writes (its face says `task-type: draft`), opened on its Work, at the step that
    waits (b32 s41)."""
    theme = theme or VANILLA
    if theme.task_action:
        got = theme.task_action(task, root)
        if got:
            return got
    if task_type(task) == "draft":
        return "✎ Write", href(task, root, theme, "Work Details")
    return None


def _short_title(md: Path | None, name: str) -> str:
    """A face's title without the folder's own name or tag in front ("t00_abstract · Abstract" -> "Abstract")."""
    title = _title(md) if md else ""
    for lead in (name, name.split("_", 1)[0]):
        title = re.sub(rf"^{re.escape(lead)}\b\s*[·:\-–]?\s*", "", title, flags=re.I) or title
    return "" if title == name else title


def _run_passes(p: Path, root: Path) -> str:
    """A soft Run's passes (passes/pNN-MMDD/pass.md), newest last, each a link to its pass; with none, what its
    card says it wrote (`writes:`, relative to its scope, the folder whose runs/ holds it)."""
    passes = sorted(d for d in (p / "passes").iterdir() if d.is_dir()) if (p / "passes").is_dir() else []
    links = [pop(_reader(d / "pass.md", root), d.name, d.name) if (d / "pass.md").is_file() else _e(d.name)
             for d in passes]
    if links:
        return f'<div class=work-files>passes: {" · ".join(links)}</div>'
    card = (p / "run.yaml").read_text(encoding="utf-8", errors="ignore") if (p / "run.yaml").is_file() else ""
    m = re.search(r"(?ms)^writes:\s*\n((?:\s*-\s.*\n?)+)", card)
    scope = p.parent.parent
    block = _block_above(scope) or scope
    wrote = []
    for w in (re.findall(r"-\s*(.+)", m.group(1)) if m else []):
        target = (scope / w.strip().strip("'\"")).resolve()
        try:
            wrote.append(target.relative_to(block.resolve()).as_posix() + ("/" if w.strip().endswith("/") else ""))
        except ValueError:
            wrote.append(w.strip())
    return (f'<div class=work-files>wrote: {" · ".join(f"<code>{_e(x)}</code>" for x in wrote[:4])}</div>' if wrote
            else '<div class="work-files mut">no pass yet</div>')


def _run_line(run: dict, root: Path) -> str:
    """One Run: its name, kind and type, status, then what it found: a hard Run's headline and result/ files, a
    soft Run's passes."""
    p = run["path"]
    res = next((p / d for d in ("result", "results") if (p / d).is_dir()), None) if p.is_dir() else None
    head = ""
    if res and (res / "headline.txt").is_file():
        head = (res / "headline.txt").read_text(encoding="utf-8", errors="ignore").strip().splitlines()[0][:240] \
            if (res / "headline.txt").read_text(encoding="utf-8", errors="ignore").strip() else ""
    files = sorted(f for f in res.rglob("*") if f.is_file() and not f.name.startswith(".")) if res else []
    link = lambda f: pop(_reader(f, root) if f.suffix == ".md" else "/" + _rel(f, root), f.name,
                         f.relative_to(res).as_posix())
    shown = " · ".join(link(f) for f in files[:6]) + (f" · +{len(files) - 6} more" if len(files) > 6 else "")
    status = run["status"] if run["status"] not in ("—", "null", "None") else ""
    rtype = run["type"] if run["type"] not in ("null", "None", "") else ""
    return (f'<li><code>{_e(run["run"])}</code> <span class=mut>{_e(run["kind"])}{" · " + _e(rtype) if rtype else ""}</span>'
            + (f' <span class="st st-{_e(status)}">{_e(status)}</span>' if status else "")
            + (f'<div class=work-head>{_e(head)}</div>' if head else "")
            + (_run_passes(p, root) if run["kind"] == "soft" and p.is_dir() else
               f'<div class=work-files>result/: {shown}</div>' if shown else
               ('<div class="work-files mut">no result/ yet</div>' if p.is_dir() else ""))
            + '</li>')


def _work_runs(folder: Path, root: Path) -> str:
    runs = runs_of(folder)
    if not runs:
        return '<p class="mut work-none">No Runs yet.</p>'
    return '<ul class=work-runs>' + "".join(_run_line(r, root) for r in runs) + '</ul>'


def _theme_meta(theme, folder: Path, root: Path) -> str:
    """The theme's own words on a Work card (Theme.work_meta), as ' · words', or ""."""
    try:
        extra = theme.work_meta(folder, root) if theme is not None and theme.work_meta else ""
    except Exception:                            # a theme's words never break the base's tree
        extra = ""
    return f" · {extra}" if extra else ""


def _work_task(task: Path, root: Path, theme, open_: bool = False) -> str:
    md, runs = face(task), runs_of(task)
    act = task_action(task, root, theme)
    button = f'<a class=work-act href="{_e(act[1])}">{_e(act[0])}</a> ' if act else ""
    title = _short_title(md, task.name)
    meta = ((f'{_e(title)} · ' if title else "") + f'{len(runs)} Run{"s" * (len(runs) != 1)}'
            + _theme_meta(theme, task, root))
    return (f'<details class="topic work-task{" work-human" if act else ""}"{" open" if open_ else ""}><summary>'
            f'<span class=related-head><b>{_e(task.name)}</b><br><span class=topic-meta>{meta}</span></span>'
            f'<span class=topic-pop>{button}{_link(ROUTE + "?" + urlencode({"path": _rel(task, root)}), "↗")}</span>'
            f'</summary><div class=work-body>{task_card(task, root, getattr(theme, "name", ""))}'
            f'{_work_runs(task, root)}</div></details>')


def _work_job(job: Path, root: Path, theme, open_: bool = False) -> str:
    md, tasks = face(job), children(job, "Job")
    human = sum(1 for t in tasks if task_action(t, root, theme))
    own = runs_of(job)
    n = sum(len(runs_of(t)) for t in tasks) + len(own)
    title = _short_title(md, job.name)
    meta = ((f'{_e(title)} · ' if title else "")
            + f'{len(tasks)} Task{"s" * (len(tasks) != 1)} · {n} Run{"s" * (n != 1)}'
            + (f' · {human} for a person ✎' if human else "") + _theme_meta(theme, job, root))
    body = "".join(_work_task(t, root, theme) for t in tasks)
    if own:
        body += '<p class=work-sub>the Job\'s own Runs</p>' + _work_runs(job, root)
    try:
        body += theme.work_body(job, root) if theme is not None and theme.work_body else ""
    except Exception:                            # a theme's part never breaks the base's tree
        pass
    return (f'<details class="topic work-job"{" open" if open_ else ""}><summary>'
            f'<span class=related-head><b>{_e(job.name)}</b><br><span class=topic-meta>{meta}</span></span>'
            f'<span class=topic-pop>{_link(ROUTE + "?" + urlencode({"path": _rel(job, root)}), "↗")}</span></summary>'
            f'<div class=work-body>{body or "<p class=mut>No Tasks yet.</p>"}</div></details>')


def work_tree(level: str, folder: Path, root: Path, theme=None, jobs: list | None = None) -> str:
    """Block: one card per Job; Job: one card per Task, open; Task: its Runs. Each opens down to its Runs and
    what each found (its headline, its result/ files); a Task a person works in carries its button (✎ Write,
    🏷 Label) and a mark."""
    theme = theme or VANILLA
    if level == "Block":                         # `jobs`: a theme's filter of them (cowork's open · waiting · done)
        jobs = children(folder, "Block") if jobs is None else jobs
        return ''.join(_work_job(j, root, theme) for j in jobs) if jobs else ""
    if level == "Job":
        tasks = children(folder, "Job")
        own = runs_of(folder)
        return (''.join(_work_task(t, root, theme, open_=True) for t in tasks)
                + (('<p class=work-sub>the Job\'s own Runs</p>' + _work_runs(folder, root)) if own else ""))
    act = task_action(folder, root, theme)
    return ((f'<p><a class=work-act href="{_e(act[1])}">{_e(act[0])}</a> <span class=mut>a person works in this '
             'Task</span></p>' if act else "") + _work_runs(folder, root))


WORK_CSS = """
/* shared looks a theme's Spaces may use (b15 s41, 261014): a scoreboard, its numbers large and labels small; cards side
   by side, one marked .key */
.stat-row{display:flex;flex-wrap:wrap;gap:10px 44px;margin:8px 0 4px}.stat-row>div{min-width:84px}
.stat-row b{display:block;font-size:30px;line-height:1.2;font-weight:700;color:var(--fg)}.stat-row span{color:var(--mut);font-size:13px}
.stat-line{font-size:16px;margin:6px 0 18px}
.card-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:10px;margin:8px 0 14px}
.card-row>div{border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--card);min-width:0;font-size:13.5px;line-height:1.5}
.card-row>div.key{border-color:var(--tab-on);background:var(--tab-wash)}.card-row h4{margin:0 0 2px;font-size:14px}.card-row .mut{margin:0 0 6px}
.card-row code{overflow-wrap:anywhere}
.work-body{padding:6px 14px 10px}.work-task{margin:6px 0}.work-runs{margin:6px 0 4px;padding-left:18px}
.work-runs li{margin:4px 0}.work-head{font-size:14px;margin:2px 0}.work-files{font-size:13px}
.work-files a{text-decoration:none}.work-sub{color:var(--mut);font-size:13px;margin:10px 0 2px}
.work-act{display:inline-block;padding:2px 10px;border:1px solid var(--tab-on);border-radius:6px;color:var(--tab-on);
background:var(--tab-wash);text-decoration:none;font-size:13px}.work-human>summary b::after{content:" ✎";color:var(--tab-on)}
.workflow-view .work-table-scroll{overflow-x:auto;max-width:100%}
.workflow-view .wf-table{width:100%;overflow-wrap:anywhere}
.workflow-view details{margin:10px 0}.workflow-view summary{overflow-wrap:anywhere}
.workflow-view .work-execution-table{table-layout:fixed}
.work-execution-table th:nth-child(1){width:22%}.work-execution-table th:nth-child(2){width:9%}
.work-execution-table th:nth-child(3){width:11%}.work-execution-table th:nth-child(4){width:17%}
.work-execution-table th:nth-child(5){width:9%}.work-execution-table th:nth-child(6){width:32%}
@media(max-width:720px){.workflow-view .work-table-scroll>.wf-table{min-width:700px}}
.work-none{margin:6px 0}.st{font-size:12px;padding:0 6px;border:1px solid var(--line);border-radius:999px}
.st-done,.st-ok,.st-answered{color:var(--ok);border-color:var(--ok)}.st-failed,.st-error{color:var(--miss);border-color:var(--miss)}
"""


def _subs_row(theme, root, folder, space, view: Space) -> str:
    if not view.subspaces:
        return ""
    return ('<nav class="row subs">' + "".join(
        f'<a class="tab{" on" if s == view.open else ""}" href="{_e(href(folder, root, theme, space, s))}">{_e(s)}</a>'
        for s in view.subspaces) + "</nav>")


def render(theme: Theme, root: Path, folder: Path, space: str = "", sub: str = "", *, studio: bool = False) -> str:
    """One work level, or its shared Block Studio; Guide can replace either body."""
    from live.runs_panel import PANEL_CSS, PANEL_JS, SPLIT_CSS, panel_markup
    from live.space_views import SPACE_VIEW_CSS
    from live.work_items import WORK_ITEM_CSS
    from live.workbench_guide import mount_guide

    root, folder = root.resolve(), folder.resolve()
    level = level_of(folder) or "Block"
    # a Related link (space=Related, or the older Description › Related) opens the Studio with its
    # Related part unfolded (b10 s04, JL 261011)
    unfold = space in IN_STUDIO or (space == "Description" and sub in IN_STUDIO)
    studio = studio or space in ("Idea Studio", "Studio") or unfold   # saved Space links still open Studio
    space = space if space in SPACE_NAMES and space not in ("Idea Studio",) + IN_STUDIO else "Description"
    if unfold:
        sub = ""
    block = chain(folder, root).get("Block")
    owner = block if studio and block else folder      # the Block's, at every level
    owner_level = "Block" if studio and block else level
    views = spaces_for(theme, owner_level, owner, root, "" if studio else sub)
    view = views["Idea Studio" if studio else space]
    if studio:                                  # Related, the second folding part under the topic cards
        part = studio_related(views.get("Related") or Space(), owner, root, unfold)
        # then Delivery, the third: what went out (JL 261014); Runs, the fourth: each Task's hard Runs and their
        # status (JL 261019); Timeline, the fifth: what moved when (JL 261011); Folder, the sixth: what the folder holds
        view = replace(view, html=view.html + part.html + studio_delivery(owner, root, theme)
                       + studio_runs(owner, root, theme) + studio_timeline(owner, root) + studio_folder(owner, root),
                       run_types=tuple(view.run_types) + tuple(part.run_types),
                       disk=tuple(view.disk) + tuple(part.disk))
    rel = _rel(owner, root)
    kinds = [dict(k, prompt=k.get("prompt", "").replace("{folder}", rel)) for k in view.run_types]
    panel = panel_markup("Idea Studio" if studio else space, kinds, [list(k.get("rows") or []) for k in kinds], base=root, fill=lambda row: {"page": rel, "folder": rel},
                         whole=f"this {theme.level_name(owner_level)}",
                         extra=f'<p class=mut style="margin:6px 0">{_e(view.note)}</p>' if view.note else "",
                         top=disk_markup(view.disk, owner, root),   # Disk folds with the Runs (JL 261007)
                         title="Disk · Runs" if view.disk else "Runs", compact=True, folded=True)
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
    block_tag = block.name.split("_", 1)[0] if block and _PREFIXED.match(block.name) else ""
    block_context = f"{theme.level_name('Block')} {block_tag or short_name(block.name)}" if block else ""
    lead = f"{theme.level_name(level)} {tag}".strip()
    if level != "Block" and block_context:
        lead = f"{block_context} · {lead}"
    guide_title = f"{theme.icon} {theme.label} · Guide" + (f" · {block_context}" if block_context else "")
    heading = (f'{_e(theme.icon)} {_e(theme.label)} · <span class=lv>{_e(lead)} ·</span> {_e(named)}'
               if named != folder.name or tag else f'{_e(theme.icon)} {_e(theme.label)} · {_e(named)}')
    delivery = not studio and space == "Delivery"
    if studio or (delivery and block):          # a Block-owned view: the Block's name, from any level
        studio_context = block_tag or (short_name(block.name) if block else "No Block")
        block_md = face(block) if block else None
        block_name = _title(block_md) if block_md else (block.name if block else "")
        if block_tag:
            block_name = re.sub(rf"^{re.escape(block_tag)}\b\s*[·:\-–]?\s*", "", block_name, flags=re.I) or block_name
        elif block_name.startswith(studio_context):          # an untagged Board's title starts with its name: once
            block_name = block_name[len(studio_context):].lstrip(" ·:-–") or block_name
        heading = (f'{_e(theme.icon)} {_e(theme.label)} · {"Studio" if studio else "Delivery"} · '
                   f'<span class=lv>{_e(studio_context)}</span>')
        if block_name and block_name != studio_context:
            heading += f' · {_e(block_name)}'
    if delivery and block and folder == block:  # the Block's own Delivery lists every part, by source
        view = replace(view, html=view.html + delivery_by_source(theme, block, root))
    if studio:
        work_rows = ""
    elif delivery:                              # no Spaces row: the source row (Block · jNN · tNN), then a
        work_rows = ((_delivery_row(theme, root, block, folder) if block else "")   # lanes row if there is a choice
                     + (_subs_row(theme, root, folder, space, view) if len(view.subspaces or ()) > 1 else ""))
    else:
        work_rows = _spaces_row(theme, root, folder, space, view.open, views) + _subs_row(theme, root, folder, space, view)
    body_class = ("frame-body studio-body" if studio else "frame-body delivery-body" if delivery
                  else "frame-body")
    # No band line: the title keeps the Block context when the top button just says Block
    # (b03 s02-D08, JL 261010); the folder's path stays one hover away, on the title.
    where = f"{theme.level_name(level)} · {_rel(folder, root)} · " + (f"{theme.label} theme" if theme.name != "vanilla" else "vanilla")
    document = ('<!doctype html><html lang=en><head><meta charset=utf-8>'
                '<meta name=viewport content="width=device-width,initial-scale=1">'
                f'<title>{_e(title)}</title><link rel="icon" href="data:,">'
                # the base's shared view styles, which a theme's Spaces may use; never a theme's own
                # (b03, JL 261007: "base styles only": a theme carries no look of its own)
                f'<style>{CSS}{PANEL_CSS}{SPLIT_CSS}{SPACE_VIEW_CSS}{WORK_ITEM_CSS}{DISK_CSS}{WORK_CSS}</style></head><body><main>'
                + _level_row(theme, root, folder, level, space, sub, studio=studio)
                + f'<header class=page-title><h1 title="{_e(where)} · {_e(folder.name)}" '
                  f'data-guide="{_e(guide_title)}">{heading}</h1></header>'
                + f'<section class="{body_class}" data-owner="{_e(rel)}">'  # Guide replaces either body
                + work_rows
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


# ── a Task's type picks its layout (b32 s03, JL 261014: "for the theme, we can have different type of tasks,
# and the tasks can have different layout"; s41-D15, JL 261016: one folder per type) ──────────────────────────
# A Task's face says its type (`task-type: draft`). Each type has its own folder, `workbench-task-<type>/`, holding its layout
# `task_<type>.py` (TASK_TYPE, spaces) and every view and asset it shows: servers/workbench/workbench-task-<type>/ for a type
# every theme uses, servers/workbench-<theme>/workbench-task-<type>/ for a theme's own. The theme's own Spaces go on top.
_TASK_TYPE = re.compile(r"(?m)^\**task-type\**:\s*`?([\w-]+)")


def task_type(folder: Path) -> str:
    """The `task-type:` a Task's face declares, or "" when it names none."""
    md = face(folder) if folder else None
    if not md:
        return ""
    m = _TASK_TYPE.search(md.read_text(encoding="utf-8", errors="ignore")[:3000])
    return m.group(1) if m else ""


def task_layouts(theme: str = "") -> dict:
    """{task type: spaces(folder, root, sub)} for one theme: every `workbench-task-<type>/task_<type>.py` in
    servers/workbench/ (every theme's), then the theme's own in servers/workbench-<theme>/ (that theme's only, so
    a labeling `task-type: eval` never lays out a work Task). A layout names its TASK_TYPE, or several TASK_TYPES."""
    return {name: layout.spaces for name, layout in _task_modules(theme).items()}


def _task_modules(theme: str = "") -> dict:
    """{task type: its layout module} for one theme (task_layouts' search)."""
    import importlib
    from host_registry import task_folders, workbench_name
    found = {}
    for folder in task_folders():
        owner = folder.parent.name
        if owner != "workbench" and workbench_name(folder.parent) != theme:
            continue
        kind = folder.name[len("workbench-task-"):]
        module = f"task_{kind.replace('-', '_')}"
        if (folder / f"{module}.py").is_file():
            layout = importlib.import_module(f"live.{module}")
            for name in getattr(layout, "TASK_TYPES", None) or (layout.TASK_TYPE,):
                found[name] = layout
    return found


def task_card(task: Path, root: Path, theme: str = "") -> str:
    """A Task type's own lines on the Task's Work card in its Job (its layout's optional `work_card(task, root)`):
    a draft Task's seven steps, each a link to its tab (b32 s41); "" for a type that has none."""
    layout = _task_modules(theme).get(task_type(task))
    try:
        return layout.work_card(task, root) if layout is not None and hasattr(layout, "work_card") else ""
    except Exception:                            # a Task type's lines never break the base's tree
        return ""


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
