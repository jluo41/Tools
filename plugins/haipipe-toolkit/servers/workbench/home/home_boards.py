"""The SPACE Home's Block discovery: where Boards live below the server root and what each one is.

Finds every `board.md` (without walking into what cannot hold one), reads each Board's title,
kind, Theme and owning Project, and names it by the slug `/b/` and `/w/` resolve. Rendering
lives in home_page.py and home_rows.py, the short addresses in home_routes.py; home.py
re-exports every name, so `from live.home import ...` keeps working.
"""

from __future__ import annotations

import os
import re
import shlex
from pathlib import Path
from urllib.parse import quote

from src.common import page_files
from src.themes import THEMES as THEME_TABLE, kind_of as theme_kind_of


# Folders that cannot contain a board and are expensive to walk. `board` is the
# GENERATED tree under every board; `_WorkSpace` is the gitignored data store.
# `_old` holds retired Blocks and backup copies of a board.md: listing them made
# ghost duplicates on Home (EB-1A Petition three times, JL 261012).
SKIP_PARTS = {".git", ".venv", "node_modules", "__pycache__", "_archive", "_old",
              "_fixture", "fixtures", "board", "_WorkSpace", "site-packages",
              ".pytest_cache", "dist", "build"}
# A Block kept below one of these is a legacy copy: listed, but hidden from the default
# view in the Chart and the List alike (`?archived=1` shows it in both; JL 261012).
LEGACY_PARTS = frozenset({"_legacy", "_old", "_archive"})
TITLE = re.compile(r"^#\s+(.+?)\s*$", re.M)
SPINE = re.compile(r"^spine:\s*(.+?)\s*$", re.M)
STATE = re.compile(r"^state:\s*(✅|🟡|🔴|⏸️)", re.M)
BOARD_KINDS = (
    ("Task Board", "🧪"),
    ("Discovery Board", "🔭"),
    ("CoWork Board", "📨"),
    ("Paper Board", "📄"),
    ("Design Board", "🎨"),
    ("Skill Board", "🧩"),
)
HOME_BRAND = "SPACE Home"      # the heading when settings.env has no SPACE_NAME
PROJECT_FIELD = re.compile(r"^(id|profile|state):\s*(.*?)\s*$")
# the face's own mark and word, whatever the mark (`🟢 RUNNING`, `🔄 ACTIVE`), as the Chart reads it
BOARD_STATE = re.compile(r"^state:[ \t]*([^\w\s]+)?[ \t]*([A-Z][A-Z-]+)?", re.M)

# The Space view: Project -> Theme -> Block. A Theme is the Project-root folder a
# Block sits in (skills/1_base/project/haipipe-project/ref/project-structure.md), listed in
# the order of haipipe-draft's src/themes.py; an old plural folder (`tasks/`, `papers/`, ...)
# is an alias of its singular Theme folder and sorts with it.
THEMES = tuple(folder for _, folder, _ in THEME_TABLE)
THEME_ALIASES = {old: folder for _, folder, old in THEME_TABLE if old}
THEME_KIND = {folder: kind for kind, folder, _ in THEME_TABLE}
# The block type the kind filter toggles: its order, emoji and the label a card shows.
KIND_ORDER = ("task", "discovery", "cowork", "paper", "insight", "design",
              "labeling", "skill")
KIND_ICON = {"task": "🧪", "discovery": "🔭", "cowork": "📨", "paper": "📄",
             "insight": "🔎", "design": "🎨", "labeling": "🏷", "skill": "🧩"}
ROUTE_KIND = {"work-board": "task", "cowork-board": "cowork",
              "discovery-board": "discovery", "paper-board": "paper",
              "insight-board": "insight", "design-board": "design",
              "labeling-board": "labeling"}
# A Board outside any Project Theme (the SPACE / Tools buckets) is grouped under
# the Theme its kind would live in.
KIND_THEME = {kind: theme for theme, kind in THEME_KIND.items()} | {
    "labeling": "labeling", "skill": "skills"}
# Projects start open when the view holds at most this many; more start closed.
FOLD_OPEN_MAX = 5


def block_theme(card: dict[str, object]) -> str:
    """The Project-root folder a Block sits in (`tasks`, `paper`, ...), or ""."""
    if card.get("project_scope") != "project":
        return ""
    try:
        parts = Path(str(card["path"])).relative_to(str(card["project_path"])).parts
    except ValueError:        # the server root sits inside the Project
        return ""
    return parts[0] if len(parts) >= 2 else ""


def block_kind_key(card: dict[str, object]) -> str:
    """The block type the Space filter uses: the Theme first, then the workbench
    `board.md` declares, then the location-based Board kind."""
    theme = str(card.get("theme") or "")
    theme = THEME_ALIASES.get(theme, theme)
    if theme in THEME_KIND:
        return THEME_KIND[theme]
    if card.get("workbench") in ROUTE_KIND:
        return ROUTE_KIND[str(card["workbench"])]
    kind = str(card.get("kind") or "Task Board")
    return kind.removesuffix(" Board").lower() or "task"


def theme_sort_key(theme: str) -> tuple[int, str]:
    canonical = THEME_ALIASES.get(theme, theme)
    return (THEMES.index(canonical) if canonical in THEMES else len(THEMES),
            theme.lower())


def kind_sort_key(kind: str) -> tuple[int, str]:
    return (KIND_ORDER.index(kind) if kind in KIND_ORDER else len(KIND_ORDER), kind)


def parse_kinds(value: str) -> list[str]:
    """`?kind=task,paper` -> ["task", "paper"]; `all` or nothing -> [] (no filter)."""
    kinds = []
    for token in re.split(r"[,\s]+", (value or "").lower()):
        if token and token != "all" and re.fullmatch(r"[a-z][a-z-]*", token) \
                and token not in kinds:
            kinds.append(token)
    return kinds


def kind_query(kinds, rest: str = "") -> str:
    """The query string that reproduces a kind selection (`?kind=task`), or `?`; `rest`
    (`project=...`) rides along so a kind link keeps the Project it was clicked in."""
    ordered = sorted(set(kinds), key=kind_sort_key)
    parts = (["kind=" + ",".join(ordered)] if ordered else []) + ([rest] if rest else [])
    return "?" + "&".join(parts)


def project_matches(card: dict[str, object], wanted: str) -> bool:
    """`?project=` names a Project by its SPACE-relative folder, its folder name, or its id; or a SPACE bucket
    (SPACE / Shared, Tools & Skills) by its key, `shared:space`, so the Guide's Project link works outside a Project."""
    wanted = (wanted or "").strip().strip("/").lower()
    path = str(card.get("project_path") or "").lower()
    if wanted and wanted == str(card.get("project_key") or "").lower():   # a SPACE bucket, e.g. shared:space
        return True
    return card.get("project_scope") == "project" and wanted in {
        path, path.rsplit("/", 1)[-1], str(card.get("project") or "").lower()}

def frame_url(rel: str) -> str:
    """The focus page's long address for a Block folder, SPACE-relative (what `/w/<block>` and `/b/<block>` open).
    The old tabbed frame opens only on an explicit `layout=frame` (Proj-JHU-REACH report, JL 261118)."""
    return "/_board/workbench?path=" + quote(rel, safe="/") + "&layout=focus"


def _skip(path: Path, root: Path) -> bool:
    return any(part in SKIP_PARTS or part.startswith(".")
               for part in path.relative_to(root).parts)


def board_kind(board: Path, root: Path) -> tuple[str, str]:
    """Classify a Board by its owning location, with Task as the safe default.

    A Board used to design a skill lives beneath ``plugins/*/skills/diagrams``;
    that identity wins even if its topic happens to contain the word "paper".
    Existing paper lifecycle trees are recognised next.  Every other Board stays
    a Task Board without requiring a registry or new source metadata.
    """
    parts = tuple(part.lower() for part in board.relative_to(root).parts)
    if "plugins" in parts and "skills" in parts and "diagrams" in parts:
        return "Skill Board", "🧩"
    if any(theme_kind_of(part) == "discovery" for part in parts):
        return "Discovery Board", "🔭"
    if "cowork" in parts:                       # a CoWork Block (haipipe-cowork), not a Task Board
        return "CoWork Board", "📨"
    if board.name.lower().endswith("-designboard"):
        return "Design Board", "🎨"
    if any(theme_kind_of(part) == "paper" for part in parts) or "0-lifecycle" in parts:
        return "Paper Board", "📄"
    return "Task Board", "🧪"


def _project_manifest(project: Path) -> dict[str, str]:
    """Read the tiny identity slice Home needs without becoming a YAML owner."""
    manifest = project / "project.yaml"
    if not manifest.is_file():
        return {}
    fields = {}
    for line in manifest.read_text(encoding="utf-8", errors="ignore").splitlines():
        match = PROJECT_FIELD.match(line)
        if not match:
            continue
        try:
            value = " ".join(shlex.split(match.group(2), comments=True,
                                           posix=True)).strip()
        except ValueError:
            continue
        if value:
            fields[match.group(1)] = value
    return fields


def project_owner(board: Path, root: Path) -> dict[str, str]:
    """Resolve one Board to its durable Project boundary.

    A real ``project.yaml`` wins.  Legacy projects below ``examples*/`` still
    group by their existing root folder, without making their spelling imply a
    profile or Git mode.  Everything else stays visible in one of two explicit
    SPACE-owned buckets instead of being silently assigned to a Project.
    """
    root = root.resolve()
    board = board.resolve()
    # The server may intentionally be started at a project sub-root (for
    # example ``<project>/discoveries``).  That must not erase the owning
    # Project identity: the Home is still rendering the same source tree.
    # Walk through the selected root's parents until the repository boundary,
    # while keeping the nearest project.yaml as the authority.
    for candidate in (board, *board.parents):
        if not (candidate.is_relative_to(root) or root.is_relative_to(candidate)):
            continue
        manifest = _project_manifest(candidate)
        if manifest:
            # A project above the selected root is still the real owner, but
            # its path is outside the served URL space.  Keep the path useful
            # for diagnostics without letting Path.relative_to raise here.
            rel = (candidate.relative_to(root).as_posix()
                   if candidate.is_relative_to(root) else candidate.name)
            return {"project": manifest.get("id", candidate.name),
                    "project_path": rel, "project_key": f"project:{rel}",
                    "project_scope": "project",
                    "project_profile": manifest.get("profile", ""),
                    "project_state": manifest.get("state", "")}
        # Do not cross into an unrelated repository while looking for an
        # owner.  A .git file also marks a worktree boundary.
        if (candidate / ".git").exists():
            break

    parts = board.relative_to(root).parts
    if len(parts) >= 2 and parts[0].lower().startswith("examples"):
        name = parts[1]
        if name.startswith("_"):
            name = ""
        if name:
            candidate = root.joinpath(*parts[:2])
            rel = candidate.relative_to(root).as_posix()
            return {"project": name, "project_path": rel,
                    "project_key": f"project:{rel}",
                    "project_scope": "project", "project_profile": "",
                    "project_state": ""}

    lower = tuple(part.lower() for part in parts)
    if "tools" in lower and "plugins" in lower:
        return {"project": "Tools & Skills", "project_path": "Tools",
                "project_key": "shared:tools", "project_scope": "shared",
                "project_profile": "", "project_state": ""}
    return {"project": "SPACE / Shared", "project_path": ".",
            "project_key": "shared:space", "project_scope": "shared",
            "project_profile": "", "project_state": ""}


def other_space(folder: Path) -> bool:
    """A folder below the served root that is a SPACE of its own: it holds `env.sh`."""
    return (folder / "env.sh").is_file()


def _manifests(root: Path):
    """Every `board.md` below root, WITHOUT walking into what cannot hold one.

    `rglob` descends everywhere and the skip list was applied to the results, so
    the home page walked 366,951 entries — `.venv`, `node_modules`, `.git`,
    `_WorkSpace`, and the generated `board/` tree under every board — to find
    ten files. Warm that is 2.7 s; on a cold filesystem cache it was measured at
    95 s (260802), which is not "slow", it is a page JL could not open at all.
    Pruning in place is the whole fix: the same ten files, without the walk.

    A folder below root holding its own `env.sh` is another SPACE, served by its
    own host (one host per SPACE, JL 261011): a replication package such as
    DrFirst's `platforms/SMSDesign-SPACE/` carries pinned copies of Tools and a
    Project, whose Boards are not this SPACE's (JL 261013).
    """
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if d not in SKIP_PARTS and not d.startswith(".") and not other_space(Path(dirpath) / d)]
        if "board.md" in filenames:
            yield Path(dirpath) / "board.md"


def discover_boards(root: Path, *, include_page_state: bool = True, include_linked: bool = False) -> list[dict[str, object]]:
    """Read metadata from every real Board source folder.

    The full form keeps the page counts used by diagnostics and tests.  Home
    does not display those counts, so it opts out of reading every Page file;
    this keeps a refresh proportional to the Board manifests it must list.
    """
    root = root.resolve()
    cards = []
    for manifest in _manifests(root):
        board = manifest.parent
        if _skip(board, root):
            continue
        text = manifest.read_text(encoding="utf-8", errors="ignore")
        title_match = TITLE.search(text)
        spine_match = SPINE.search(text)
        title = title_match.group(1).strip() if title_match else board.name
        spine = spine_match.group(1).strip() if spine_match else "No spine declared."
        pages = list(page_files(board)) if include_page_state else []
        states = [STATE.search(p.read_text(encoding="utf-8", errors="ignore"))
                  for p in pages]
        settled = sum(match is not None and match.group(1) in {"✅", "⏸️"}
                      for match in states)
        rel = board.relative_to(root).as_posix()
        workbench = board_workbench_route(board)          # read once: it probes several presenters
        # Openable without a build (JL 261004: the static site is retired): a declared
        # workbench, or Pages the live reader can show.
        ready = workbench is not None or next(iter(page_files(board)), None) is not None
        kind, icon = board_kind(board, root)
        owner = project_owner(board, root)
        block_kind = re.search(r"(?m)^board-kind:\s*(task-block|cowork-block|discovery-block)\s*$", text)
        task_workbench = bool(block_kind)
        href = frame_url(rel)          # every Block opens in the base frame (JL 261007)
        state_match = BOARD_STATE.search(text)
        card = {"title": title, "spine": spine, "path": rel, "name": board.name,
                "pages": len(pages), "settled": settled, "ready": ready,
                "kind": kind, "icon": icon,
                "slug": board_slug(board.name, board.parent.name),
                "href": href, "workbench_ready": task_workbench,
                "workbench": workbench or "",
                # the Board's own state word only (`🟡 OPEN`), never the free text after it
                "board_state": " ".join(g for g in state_match.groups() if g) if state_match else "",
                "archived": any(part in LEGACY_PARTS for part in Path(rel).parts),
                **owner}
        card["theme"] = block_theme(card)
        card["kind_key"] = block_kind_key(card)
        cards.append(card)
    if include_linked:
        from live.space_chart import linked_home_cards
        cards.extend(linked_home_cards(root))
    return sorted(cards, key=lambda c: (
        0 if c["project_scope"] == "project" else 1,
        str(c["project_path"]).lower(), str(c["kind"]).lower(),
        str(c["path"]).lower()))


def home_folder_path(card: dict[str, object]) -> str:
    """The Block's real folder below its Title: from the Project root (`work/b00_rawdata`), or
    from the SPACE root outside a Project, so the row reads like the file tree (JL 261012)."""
    path = Path(str(card["path"]))
    if card.get("project_scope") == "project":
        try:
            return path.relative_to(str(card["project_path"])).as_posix()
        except ValueError:        # the server root sits inside the Project
            pass
    return path.as_posix()


def home_section(card: dict[str, object]) -> str:
    """Return the SPACE-root folder that owns a Home project section."""
    source = (card["project_path"] if card.get("project_scope") == "project"
              else card["path"])
    parts = Path(str(source)).parts
    return parts[0] if parts else "SPACE"


# A folder name that says what KIND of board it is rather than WHICH one.
# Every paper carries a `0-lifecycle/`, so trimming the ordinal leaves every
# paper on this SPACE claiming `/b/lifecycle` (JL 260803: "the lifecycle is not
# good, I prefer it to be misq-xxxx-lifecycle"). These names take the owning
# folder as a prefix; every other board keeps the slug it already had.
GENERIC_BOARD_NAMES = {
    "lifecycle", "board", "boards", "diagram", "diagrams", "paperboard",
}


def board_slug(name: str, parent: str = "") -> str:
    """The name a person says out loud for a board folder.

    `01-boardform-260722` becomes `boardform`: the `NN-` ordinal orders a topic
    series and the `-YYMMDD` records the day it was opened, and neither is
    something anyone says. Same rule as `status.py`'s fallback label, kept here
    because the ROUTE has to resolve it and `status.py` only has to print it.

    A GENERIC folder name is qualified by its parent, because it names a kind
    and not a board: `0-lifecycle` inside `Paper-Personality2Opioid-MISQ2026`
    is `personality2opioid-misq2026-lifecycle`, and the second paper on this
    SPACE would otherwise answer to the same URL as the first. The `Paper-` and
    `Project-` prefixes are dropped for the same reason the `NN-` ordinal is:
    they say what the folder IS, which the reader already knows.
    """
    trimmed = re.sub(r"^\d+[-_]", "", name)
    trimmed = re.sub(r"[-_]\d{6}$", "", trimmed)
    trimmed = (trimmed or name).lower()
    if trimmed in GENERIC_BOARD_NAMES and parent:
        owner = re.sub(r"^(?:Paper|Project|Proj[A-Z])[-_]", "", parent)
        owner = re.sub(r"[^A-Za-z0-9]+", "-", owner).strip("-").lower()
        if owner:
            return f"{owner}-{trimmed}"
    return trimmed


def board_by_slug(root: Path, slug: str) -> Path | None:
    """The one Board folder below root that answers to `slug`, or None.

    Shared by `/b/` and `/w/`: the slug is `board_slug()` of the folder (or the
    full folder name), matched against the Boards Home already discovers, so
    there is no second registry. Zero or several matches are None; the caller
    sends 404 rather than guessing.
    """
    root = root.resolve()
    folded = (slug or "").strip().lower()
    if not folded:
        return None
    matches = []
    for manifest in _manifests(root):
        candidate = manifest.parent
        if _skip(candidate, root):
            continue
        if folded in (board_slug(candidate.name, candidate.parent.name),
                      candidate.name.lower()):
            matches.append(candidate)
    return matches[0] if len(matches) == 1 else None


_DIALECT = re.compile(r"(?m)^dialect:\s*([a-z][a-z0-9-]*)\s*$")
_BOARD_KIND = re.compile(r"(?m)^board-kind:\s*([a-z][a-z0-9-]*)\s*$")


def board_workbench_route(board: Path) -> str | None:
    """Which board-level workbench `board.md` declares, or None.

    The same rule the drawer applies when it decides whether to register a
    Board-level tab, so `/w/<board>` cannot resolve to a tab the Board would
    refuse: `dialect: paper` -> paper-board; a Design Board -> design-board; an
    InsightBoard -> insight-board; `board-kind: labeling-board` -> labeling-board.
    """
    try:
        text = (board / "board.md").read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    m = _DIALECT.search(text)
    if m and m.group(1) == "paper":
        return "paper-board"
    kind = (_BOARD_KIND.search(text) or [None, ""])[1]
    if kind == "task-block":                 # an Insight Block opens the Insight workbench (block-contract.md)
        return "insight-board" if re.search(r"(?m)^workbench:\s*insight\s*$", text) else "work-board"
    if kind == "cowork-block":
        return "cowork-board"
    if kind == "discovery-block":
        return "discovery-board"
    if kind in {"labeling", "labeling-board"}:
        return "labeling-board"
    try:
        from live.designboard import is_design_board
        if is_design_board(board):
            return "design-board"
    except ImportError:
        pass
    try:
        from live.insightboard import is_insight_board
        if is_insight_board(board):
            return "insight-board"
    except ImportError:
        pass
    try:  # a Board whose Pages own labeling jobs, even without a board-kind line
        from live.labeling import board_jobs
        found = board_jobs(board, f"{board.name}/board.md", probe=True)
        if found.get("jobs") or found.get("empty"):
            return "labeling-board"
    except Exception:  # noqa: BLE001  subjective-label absent or a broken job: not this route
        pass
    return None
