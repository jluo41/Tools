"""The frame's ground: levels, Spaces, the Space and Theme classes, where a folder sits on the ladder, and the small
link, table and face helpers every part uses (re-exported by live.frame)."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
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
    guide: str = "shared"                      # the Guide family it mounts (workbench/guide/guide_families.py)
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
        from live import frame                # frame.themes, so a test that swaps it is read here too
        _PATTERNS.update({name: t.level_patterns for name, t in frame.themes().items()} or {"vanilla": {}})
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
    counted only inside a Project; the Tools repo's Blocks sit in Projects too since 261028
    (Tools/blueprints/Project-<name>/work/bNN_*), so they read as the work theme."""
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
        from live import frame                # frame.themes, so a test that swaps it is read here too
        for name, theme in frame.themes().items():
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


# ── links, the pop-out, the Page reader and the frame's table ──────────────────────────────────
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


def _empty_view(text: str) -> str:
    return f'<p class=space-empty>{text}</p>'


def _file_url(path: Path, root: Path) -> str:
    """Where a kept file opens: a .md in the reader, a .docx or an .eml as its preview, anything else as
    itself."""
    if path.suffix == ".md":
        return _reader(path, root)
    if path.suffix.lower() in (".docx", ".eml", ".pptx"):
        return ROUTE + "?" + urlencode({"view": path.suffix.lower()[1:], "path": _rel(path, root)})
    rel = _rel(path, root)
    if (path.suffix == ".html" and path.stem == path.parent.name and re.match(r"^r\d\d_collect_", path.stem)
            and "labeling" in (part.casefold() for part in Path(rel).parts)):
        # a labeling folder is never a static file (host_registry.static_path_allowed): a meaning Task's interaction
        # form opens through its own route, the path kept so the form's copied form: line names its Run (b15 s58)
        return "/_board/labeling/form/" + quote(rel)
    return "/" + quote(rel)


# The helpers a theme may use, by public name (the underscore names stay as aliases):
# esc(text) · link(href, label) · reader(md, root) -> the Page reader's URL · rel(path, root) ->
# SPACE-relative · table(heads, rows) -> the frame's table · title(md) · fields(md) · runs_of(folder) ·
# studio_cards(folder, root) -> Idea Studio's topic cards · pop(href, label, text) -> a link that opens
# in the frame's pop-out (a Run, a drawing, a page)
esc, link, reader, rel, table, title, fields = _e, _link, _reader, _rel, _table, _title, _fields  # + studio_cards


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


def short_name(name: str, most: int = 26) -> str:
    """A folder's name for the Job ▾ / Task ▾ dropdown: the folder name exactly as it is on disk (b10 s32-D15,
    JL 261011: "could we do not use · … like the folder name of the j01"). A folder name is made readable where it
    is made (a design Job is jNN_<goal name>_<method name>), so the screen shows it as is, never cut to its ids.
    `most` is kept for callers that pass it; nothing is cut."""
    return name
