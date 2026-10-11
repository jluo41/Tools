"""The read-only SPACE-level Board Home.

This is deliberately not a Board: no board.md, no chat, no durable state.  It
discovers the Board folders already present below the server root and gives the
reader one stable place from which to enter them.
"""

from __future__ import annotations

import html
import os
import re
import shlex
from pathlib import Path
from urllib.parse import parse_qs, quote, urlencode, urlsplit

from src.body import group_token
from src.common import page_files
from src.parse import parse_dir
from src.themes import THEMES as THEME_TABLE, kind_of as theme_kind_of


# Folders that cannot contain a board and are expensive to walk. `board` is the
# GENERATED tree under every board; `_WorkSpace` is the gitignored data store.
SKIP_PARTS = {".git", ".venv", "node_modules", "__pycache__", "_archive",
              "_fixture", "fixtures", "board", "_WorkSpace", "site-packages",
              ".pytest_cache", "dist", "build"}
TITLE = re.compile(r"^#\s+(.+?)\s*$", re.M)
SPINE = re.compile(r"^spine:\s*(.+?)\s*$", re.M)
STATE = re.compile(r"^state:\s*(✅|🟡|🔴|⏸️)", re.M)
BOARD_KINDS = (
    ("Task Board", "📋"),
    ("Discovery Board", "🔭"),
    ("CoWork Board", "📨"),
    ("Paper Board", "📄"),
    ("Design Board", "🎨"),
    ("Skill Board", "🧩"),
)
HOME_BRAND = "SPACE Home"      # the heading when settings.env has no SPACE_NAME
PROJECT_FIELD = re.compile(r"^(id|profile|state):\s*(.*?)\s*$")
BOARD_STATE = re.compile(r"^state:\s*(✅|🟡|🔴|⏸️)\s*([A-Z][A-Z-]+)?", re.M)

# The Space view: Project -> Theme -> Block. A Theme is the Project-root folder a
# Block sits in (skills/1_base/project/haipipe-project/ref/project-structure.md), listed in
# the order of haipipe-page's src/themes.py; an old plural folder (`tasks/`, `papers/`, ...)
# is an alias of its singular Theme folder and sorts with it.
THEMES = tuple(folder for _, folder, _ in THEME_TABLE)
THEME_ALIASES = {old: folder for _, folder, old in THEME_TABLE if old}
THEME_KIND = {folder: kind for kind, folder, _ in THEME_TABLE}
# The block type the kind filter toggles: its order, emoji and the label a card shows.
KIND_ORDER = ("task", "discovery", "cowork", "paper", "insight", "design",
              "labeling", "skill")
KIND_ICON = {"task": "📋", "discovery": "🔭", "cowork": "📨", "paper": "📄",
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
    """`?project=` names a Project by its SPACE-relative folder, its folder name, or its id."""
    wanted = (wanted or "").strip().strip("/").lower()
    path = str(card.get("project_path") or "").lower()
    return card.get("project_scope") == "project" and wanted in {
        path, path.rsplit("/", 1)[-1], str(card.get("project") or "").lower()}


def frame_url(rel: str) -> str:
    """The base frame's long address for a Block folder, SPACE-relative (what `/w/<block>` opens)."""
    return "/_board/workbench?path=" + quote(rel, safe="/")


def old_page_url(board: Path, root: Path) -> str | None:
    """The Board-level page its theme drew before the frame (`/_board/<route>?path=…`), or None."""
    route = board_workbench_route(board)
    if route is None:
        return None
    rel = board.resolve().relative_to(root.resolve()).as_posix()
    return "/_board/%s?path=%s&file=board.md" % (route, quote(f"{rel}/board.md", safe="/"))


def block_link(card: dict[str, object], slug_counts: dict[str, int]) -> str:
    """`/w/<block>` when its slug is unique; otherwise the frame's long address (an ambiguous
    slug is a 404). Both open the base frame."""
    if card.get("linked_space"):
        return str(card["href"])
    slug = str(card.get("slug") or "")
    if slug and slug_counts.get(slug, 0) == 1:
        return "/w/" + quote(slug, safe="")
    return str(card["href"])


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
    return "Task Board", "📋"


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


def _manifests(root: Path):
    """Every `board.md` below root, WITHOUT walking into what cannot hold one.

    `rglob` descends everywhere and the skip list was applied to the results, so
    the home page walked 366,951 entries — `.venv`, `node_modules`, `.git`,
    `_WorkSpace`, and the generated `board/` tree under every board — to find
    ten files. Warm that is 2.7 s; on a cold filesystem cache it was measured at
    95 s (260802), which is not "slow", it is a page JL could not open at all.
    Pruning in place is the whole fix: the same ten files, without the walk.
    """
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if d not in SKIP_PARTS and not d.startswith(".")]
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
    """Return the short folder address shown below a Home Board title."""
    kind = str(card.get("kind_key") or "").capitalize() or str(card["kind"])
    if kind.endswith(" Board"):
        kind = kind[:-len(" Board")]
    kind = {"Cowork": "CoWork"}.get(kind, kind)
    folder = Path(str(card["path"])).name
    return f"/{kind}/{folder}"


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


# `/w/<board>/<page>/<tab>` · the tab word a person types -> the long route.
# Only routes that take `path=` + `file=` for one Page belong here; Studio's
# drawing is an Excalidraw pane with its own address and stays out.
WORKBENCH_TABS = {
    "": "draft", "draft": "draft", "outline": "draft", "page": "draft",
    "runs": "runs", "run": "runs", "pageruns": "pageruns",
    "delivery": "delivery", "folder": "folderstat", "folderstat": "folderstat",
    "evidence": "evidence", "value": "value",
    "design": "design", "insight": "insight", "labeling": "labeling",
}
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


def resolve_workbench(root: Path, slug: str, anchor: str = "",
                      tab: str = "", only=frozenset()) -> tuple[str | None, str]:
    """`/w/<slug>[/<page-id>[/<tab>]]` -> (long `/_board/...` URL, reason).

    The workbench twin of `resolve_short`: the same slug, the same page id,
    and a redirect so the address bar lands on the canonical route. The server
    fills in `path=` and `file=` itself, which is the whole point: the two
    query values a caller had to compose by hand (and got wrong, 404) are
    derived here from what is on disk.

    No page id -> the Board-level workbench that `board.md` declares, or None
    with the reason. A page id -> that Page's 📃 Page tab, or the named tab.
    """
    root = root.resolve()
    board = board_by_slug(root, slug)
    if board is None and slug == "shared":
        # The Shared Workbench has no Board: `/w/shared[/<guide view>]` opens its own site.
        view = (anchor or "").strip().strip("/").lower()
        return "/w/shared" + (f"?guide={quote(view)}" if view else ""), "ok"
    if board is None:
        return None, "no such board"
    rel = board.relative_to(root).as_posix()
    anchor = (anchor or "").strip().strip("/")
    tab = (tab or "").strip().strip("/").lower()
    if not anchor:
        if tab:
            return None, "a Board-level workbench has no tabs; name a page first"
        if not only:
            # every Block opens in the base frame, in its theme (JL 261007); the frame links the
            # theme's older page (`old_page_url`) until that theme is on the frame
            return frame_url(rel), "ok"
        # an `--only` host is one theme's door and serves no frame: its own page, as before
        old = old_page_url(board, root)
        return (old, "ok") if old else (None, (
            "this Board declares no board-level workbench "
            "(no Task, CoWork or Discovery Block, `dialect: paper`, Design, Insight, or labeling Board)"))
    if tab not in WORKBENCH_TABS:
        return None, "unknown tab %r; one of %s" % (
            tab, ", ".join(sorted(k for k in WORKBENCH_TABS if k)))
    route = WORKBENCH_TABS[tab]
    pages = _page_source(board, anchor)
    if len(pages) != 1:
        return None, ("no such page" if not pages else "ambiguous page id")
    page_rel = pages[0].relative_to(board).as_posix()
    if route == "labeling":
        # The 🏷 view binds to the Page it sits beside: `path` is the Board source,
        # `file` the Page Face, `page` that Page in the live reader (see
        # workbench-labeling's `generated_page_url`; the built site is retired, JL 261005).
        from live.page_reader import page_url
        reader = page_url(pages[0], root)
        if not reader:
            return None, "the page sits outside the served root"
        return ("/_board/labeling?path=%s&file=%s&page=%s"
                % (quote(f"/{rel}/board.md", safe="/"), quote(page_rel, safe="/"),
                   quote(reader, safe="/"))), "ok"
    in_frame = _task_space(pages[0], route, root)
    if in_frame:
        return in_frame, "ok"
    return ("/_board/%s?path=%s&file=%s"
            % (route, quote(f"{rel}/{page_rel}", safe="/"), quote(page_rel, safe="/"))), "ok"


# A tab of a Task's Page -> its Space and subspace in the frame (frame.PAGE_VIEWS, JL 261007)
TAB_SPACE = {"draft": ("Audience Report", "Draft"), "runs": ("Runs", "Page Runs"),
             "delivery": ("Delivery", "Lanes"), "folderstat": ("Description", "Folder"),
             "evidence": ("Work Details", "Evidence"), "value": ("Work Details", "Value")}


def _task_space(page: Path, route: str, root: Path) -> str | None:
    """The frame's address for a Task's Page tab, when the Page is a Task folder's face; else None
    (a Page outside a Task folder keeps its own view)."""
    if route not in TAB_SPACE:
        return None
    try:
        from live import frame
    except ImportError:
        return None
    folder = page.parent
    if frame.level_of(folder) != "Task" or frame.face(folder) != page:
        return None
    space, sub = TAB_SPACE[route]
    return frame.ROUTE + "?" + urlencode({"path": folder.resolve().relative_to(root).as_posix(),
                                          "space": space, "sub": sub})


def _page_source(board: Path, anchor: str) -> list[Path]:
    """The Page sources a page id names: the Board's own ids first (`QA1`, `S-Label-1`),
    then a file stem, its prefix, or its folder (`t01_adhd_cohort_universe`)."""
    wanted, pages = anchor.lower(), []
    try:
        _, declared, _ = parse_dir(board)
    except Exception:  # noqa: BLE001  an unparsable board.md falls back to file names
        declared = []
    for page in declared:
        file = page.get("file") or ""
        if file and str(page.get("id") or "").lower() == wanted:
            pages.append(board / file)
    if not pages:
        for source in page_files(board):
            aliases = {source.stem.lower(), source.stem.split("-")[0].lower(),
                       source.parent.name.lower()}
            # a Design page under a method folder, 2-Design-M01-<slug>/Design-01-…/: the same task
            # recurs under every method, so its id names the method too (m01-design-01-…, m01-design-01)
            method = re.match(r"^2-Design-(M\d+)-", source.parent.parent.name)
            if method:
                key = method.group(1).lower()
                aliases |= {f"{key}-{source.stem.lower()}", f"{key}-" + "-".join(source.stem.lower().split("-")[:2])}
            if wanted in aliases:
                pages.append(source)
    return sorted(set(pages))


def resolve_short(root: Path, slug: str, anchor: str = "", only=frozenset()) -> str | None:
    """QE2 · `/b/<slug>[/<page-id>]` -> where a reader lands.

    A page id opens that Page in the shared live reader (`/_board/page`), the same document
    the web delivery writes; no page id opens the Board's workbench. The Board's static
    site is retired (JL 261004: the workbench is the one reader), so nothing here needs a
    build. An unknown board or page is None and the caller sends 404: a redirect to the
    wrong page is worse than a miss.
    """
    root = root.resolve()
    board = board_by_slug(root, slug)
    if board is None:
        return None
    anchor = (anchor or "").strip().strip("/")
    landing = (resolve_workbench(root, slug, only=only)[0]
               or "/" + quote(f"{board.relative_to(root).as_posix()}/board.md", safe="/"))
    if not anchor:
        return landing
    pages = _page_source(board, anchor)
    if len(pages) == 1:
        from live.page_reader import page_url
        return page_url(pages[0], root) or None
    try:                                  # a group code (`QA`) opens the Board, as its index did
        _, declared, _ = parse_dir(board)
    except Exception:  # noqa: BLE001
        declared = []
    groups = {group_token(page.get("group") or "").lower() for page in declared} - {""}
    groups |= {source.parent.name.split("-")[0].lower() for source in page_files(board)}
    return landing if not pages and anchor.lower() in groups else None


def _home_row(card: dict[str, object], project_name: str, href: str,
              shown: bool) -> str:
    """One Block card: kind emoji, title, folder, and the Board's state word."""
    kind_key = str(card["kind_key"])
    title = html.escape(str(card["title"]))
    folder = html.escape(home_folder_path(card))
    icon = html.escape(KIND_ICON.get(kind_key, str(card.get("icon") or "")))
    kind_label = html.escape(kind_key.capitalize(), quote=True)
    state = html.escape(str(card.get("board_state") or ""))
    state_html = (f'<span class="home-state" title="Board state">{state}</span>'
                  if state else "")
    row_search = html.escape(
        " ".join((project_name, str(card["title"]), str(card["slug"]),
                  str(card["path"]), str(card["spine"]), str(card["kind"]),
                  kind_key, str(card.get("theme") or ""))),
        quote=True,
    )
    hidden = "" if shown else " hidden"
    return (f'''<a class="ir home-row" href="{html.escape(href, quote=True)}" data-kind="{html.escape(kind_key, quote=True)}"
  data-search="{row_search}" role="listitem"{hidden}><span class="home-kind" role="img"
  aria-label="{kind_label}" title="{kind_label}">{icon}</span><span class="home-copy"><span class="t">{title}</span>
  <span class="home-folder">{folder}</span></span>{state_html}</a>''')


def render_home(root: Path, space_name: str = "", public_url: str = "",
                kind: str = "", project: str = "") -> str:
    """Render the Space view: every Project, its Themes, and their Block cards.

    Home offers a live hierarchy chart and an entry list. Only Boards that can be
    opened (a declared workbench, or Pages the live reader shows) are listed, so
    every card is actionable.  Inside a Project the cards group by Theme, the
    Project-root folder they sit in, in the order ``THEMES`` gives.  ``kind``
    (``?kind=task`` or ``?kind=task,paper``) filters by block type; the same
    filter runs in the browser and is written back to the address bar, so a
    link reproduces the view.  ``project`` (``?project=examples/Project-A``, or
    the folder name, or the project.yaml id) shows that one Project alone, with
    a link back to every Project; a name that matches none shows them all and
    says so (``/wb <Project>`` opens this view).  Projects start open when the
    view holds at most ``FOLD_OPEN_MAX`` of them.  Collapse choices and Project order are
    browser-local preferences, never source files or a second registry.  The
    card shows folder names, titles, kinds, the Board's state word and counts;
    never a Result value.
    """
    cards = discover_boards(root, include_page_state=False, include_linked=True)
    scoped = [card for card in cards if project_matches(card, project)] if project else []
    if scoped:
        cards = scoped
    rest = "project=" + quote(str(scoped[0]["project_path"]), safe="/") if scoped else ""
    open_cards = [card for card in cards if card["ready"] or card.get("workbench_ready")]
    slug_counts: dict[str, int] = {}
    for card in cards:   # the same match board_by_slug makes: a slug or a full folder name
        if card.get("linked_space"):
            continue
        for key in {str(card["slug"]), str(card["name"]).lower()}:
            slug_counts[key] = slug_counts.get(key, 0) + 1

    present = sorted({str(card["kind_key"]) for card in open_cards}, key=kind_sort_key)
    kinds = [k for k in parse_kinds(kind) if k in present]
    selected = set(kinds)

    def shown(card):
        return not selected or card["kind_key"] in selected

    section_groups: dict[str, dict[str, list[dict[str, object]]]] = {}
    for card in open_cards:
        section = home_section(card)
        projects = section_groups.setdefault(section, {})
        projects.setdefault(str(card["project_key"]), []).append(card)
    visible_projects = sum(any(shown(card) for card in group)
                           for projects in section_groups.values()
                           for group in projects.values())
    open_default = visible_projects <= FOLD_OPEN_MAX

    groups = []
    project_index = 0
    ordered_sections = sorted(
        section_groups,
        key=lambda section: (0 if section.lower() == "examples" else 1,
                             section.lower()),
    )
    hide_implicit_space = (
        len(ordered_sections) == 1
        and ordered_sections[0] == "SPACE"
        and open_cards
        and all(card.get("project_scope") == "project" for card in open_cards)
    )
    for section in ordered_sections:
        project_groups = section_groups[section]
        project_rows = []
        section_label = html.escape(section, quote=True)
        section_shown = False
        for project_key, group_cards in project_groups.items():
            project_name = str(group_cards[0]["project"])
            project_label = html.escape(project_name, quote=True)
            project_key_attr = html.escape(project_key, quote=True)
            group_search = html.escape(
                " ".join((project_name, str(group_cards[0]["project_path"]))),
                quote=True,
            )
            themes: dict[str, list[dict[str, object]]] = {}
            for card in group_cards:
                label = str(card["theme"] or KIND_THEME.get(str(card["kind_key"]),
                                                            str(card["kind_key"])))
                themes.setdefault(label, []).append(card)
            theme_html = []
            project_count = 0
            for theme in sorted(themes, key=theme_sort_key):
                theme_cards = sorted(themes[theme], key=lambda c: (
                    "/_" in "/" + str(c["path"]), str(c["path"]).lower()))
                count = sum(shown(card) for card in theme_cards)
                project_count += count
                rows = "".join(_home_row(card, project_name,
                                         block_link(card, slug_counts), shown(card))
                               for card in theme_cards)
                theme_attr = html.escape(theme, quote=True)
                hidden = "" if count else " hidden"
                theme_html.append(
                    f'''<section class="theme-group" data-theme="{theme_attr}" aria-label="{theme_attr}"{hidden}>
  <h3 class="theme-heading"><span class="theme-name">{html.escape(theme)}</span>
  <span class="theme-count" aria-label="{count} blocks">{count}</span></h3>
  <div class="theme-list" role="list">{rows}</div></section>''')
            group_id = f"project-list-{project_index}"
            project_index += 1
            section_shown = section_shown or bool(project_count)
            fold = " open" if open_default else ""
            hidden = "" if project_count else " hidden"
            project_rows.append(
                f'''<details class="project-group" data-project-key="{project_key_attr}"
  data-search="{group_search}" role="listitem"{hidden}{fold}><summary class="project-summary"
  aria-controls="{group_id}"><span class="project-grip"
  role="img" aria-label="Drag to reorder {project_label}" title="Drag to reorder">⠿</span>
  <span class="project-name">{project_label}</span>
  <span class="project-count" aria-label="{project_count} blocks">{project_count}</span></summary>
  <div id="{group_id}" class="project-list" aria-label="{project_label} blocks">
  {''.join(theme_html)}</div></details>''')
        section_id = f"space-title-{len(groups)}"
        hide_heading = hide_implicit_space and section == "SPACE"
        section_heading = "" if hide_heading else (
            f'<h2 class="space-heading" id="{section_id}">{section_label}</h2>')
        section_accessibility = ('aria-label="Boards"' if hide_heading else
                                 f'aria-labelledby="{section_id}"')
        groups.append(
            f'''<section class="space-section" data-space-key="{section_label}"
  data-search="{section_label}" {section_accessibility}{"" if section_shown else " hidden"}>
  {section_heading}
  <div class="space-projects" role="list" aria-label="{section_label} projects">
  {''.join(project_rows)}</div></section>''')
    if groups:
        body = "\n".join(groups)
    elif cards:
        body = '<p class="empty">No boards are ready to open.</p>'
    else:
        body = '<p class="empty">No boards found below this SPACE root.</p>'

    # The block-type toggles: `all` plus each kind present.  Each href is the view
    # that clicking it gives, so the bar works without script too.
    toggles = []
    if present:
        toggles.append(
            f'<a class="kind-toggle" role="button" href="{html.escape(kind_query((), rest), quote=True)}" data-kind="all" '
            f'aria-pressed="{"false" if selected else "true"}">all</a>')
        for key in present:
            after = selected ^ {key}
            count = sum(card["kind_key"] == key for card in open_cards)
            toggles.append(
                f'<a class="kind-toggle" role="button" href="{html.escape(kind_query(after, rest), quote=True)}" '
                f'data-kind="{html.escape(key, quote=True)}" '
                f'aria-pressed="{"true" if key in selected else "false"}">'
                f'<span aria-hidden="true">{KIND_ICON.get(key, "")}</span> {html.escape(key)} '
                f'<span class="kind-count">{count}</span></a>')
    kind_bar = (f'<nav class="kind-filter" aria-label="Block type">{"".join(toggles)}</nav>'
                if toggles else "")
    any_shown = any(shown(card) for card in open_cards)
    heading = html.escape(space_name.strip() or HOME_BRAND)
    title = heading
    scope_line = ""
    if scoped:
        name = html.escape(str(scoped[0]["project"]))
        title = f"{name} · {heading}"
        scope_line = (f'<p class="home-scope">Project <b>{name}</b> · '
                      f'<a href="{html.escape(kind_query(kinds), quote=True)}">all Projects</a></p>')
    elif project:
        scope_line = (f'<p class="home-scope">No Project matches “{html.escape(project)}”; '
                      'showing every Project.</p>')
    from live.space_chart import chart_parts
    chart_markup, chart_css, chart_js = chart_parts(root, open_cards, space_name.strip() or HOME_BRAND)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><style>
:root{{color-scheme:light;--bg:#ffffff;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4e7;--card:#f7f7f8;--accent:#1f5aa8;--focus:#075fbd;--radius-control:7px;--radius-surface:10px}}
@media(prefers-color-scheme:dark){{:root{{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;--line:#2c2e33;--card:#1d1f23;--accent:#6ea8f0;--focus:#9dc8ff}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.7 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif}}
:where(a,input):focus-visible{{outline:3px solid var(--focus);outline-offset:3px;border-radius:var(--radius-control)}}
main{{max-width:820px;margin:0 auto;padding:34px 22px 90px}}
.site-head{{margin:0 0 22px}}h1{{font-size:26px;line-height:1.35;margin:0;font-weight:700}}
.toolbar{{margin:0 0 12px}}.search{{display:block;max-width:420px}}.search input{{width:100%;min-height:38px;border:1px solid var(--line);border-radius:var(--radius-control);background:var(--card);color:var(--fg);font:inherit;padding:5px 9px;outline:none}}.search input::placeholder{{color:var(--mut)}}.search input:focus{{border-color:var(--accent)}}
.kind-filter{{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0}}.kind-toggle{{display:inline-flex;align-items:center;gap:4px;min-height:30px;padding:2px 10px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--fg);font-size:14px;text-decoration:none}}.kind-toggle:hover{{border-color:var(--accent)}}.kind-toggle[aria-pressed="true"]{{border-color:var(--accent);background:var(--accent);color:var(--bg)}}.kind-count{{color:inherit;opacity:.7;font:12px/1 ui-monospace,Menlo,monospace}}
.board-list{{min-width:0}}.space-section{{margin:26px 0 0}}.space-heading{{margin:0;padding:0 0 7px;border-bottom:2px solid var(--fg);font-size:12px;line-height:1.4;letter-spacing:.15em;text-transform:uppercase;color:var(--mut)}}.space-projects{{min-width:0}}.project-group{{margin:17px 0 0;min-width:0}}.project-summary{{display:flex;align-items:center;gap:7px;min-height:34px;padding:0 0 7px;border-bottom:1px solid var(--line);list-style:none;cursor:pointer;color:var(--fg);font-size:16px;font-weight:700}}.project-summary::-webkit-details-marker{{display:none}}.project-summary::before{{content:"▸";width:11px;color:var(--accent);font-size:11px;line-height:1}}.project-group[open]>.project-summary::before{{content:"▾"}}.project-grip{{color:var(--mut);font:14px/1 ui-monospace,Menlo,monospace;cursor:grab;user-select:none;touch-action:none;opacity:.72}}.project-grip:active{{cursor:grabbing}}.project-name{{min-width:0;overflow-wrap:anywhere}}.project-count,.theme-count{{color:var(--mut);font:12px/1 ui-monospace,Menlo,monospace;font-weight:400}}.project-list{{min-width:0;padding-top:2px}}.theme-group{{margin:10px 0 0 18px}}.theme-heading{{display:flex;align-items:baseline;gap:7px;margin:0;font-size:12px;line-height:1.5;letter-spacing:.08em;text-transform:lowercase;color:var(--mut);font-weight:600}}.theme-name::before{{content:"– "}}.project-group.dragging{{opacity:.55}}.project-group.drag-over>.project-summary{{border-color:var(--accent)}}.ir{{position:relative;display:flex;gap:10px;align-items:baseline;padding:9px 13px;border:1px solid var(--line);border-radius:var(--radius-surface);margin:6px 0;text-decoration:none;color:var(--fg);background:var(--card);overflow:hidden}}.ir:hover{{border-color:var(--accent)}}.home-kind{{flex:none;font-size:15px;line-height:1}}.home-copy{{display:flex;flex:1;min-width:0;flex-direction:column;gap:1px}}.ir .t{{min-width:0;overflow-wrap:anywhere;font-weight:600}}.home-folder{{min-width:0;color:var(--mut);font:12px/1.55 ui-monospace,Menlo,monospace;overflow-wrap:anywhere;word-break:break-word}}.home-state{{flex:none;color:var(--mut);font:12px/1.4 ui-monospace,Menlo,monospace;white-space:nowrap}}.empty,.no-results{{color:var(--mut);padding:14px 0}}.home-scope{{margin:4px 0 0;color:var(--mut);font-size:14px}}.home-scope b{{color:var(--fg)}}.home-scope a{{color:var(--accent)}}[hidden]{{display:none!important}}.sr-only{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}}
@media (max-width:680px){{main{{padding:28px 14px 62px}}.site-head{{margin-bottom:18px}}h1{{font-size:24px}}.search input{{min-height:40px}}.ir{{padding:9px 12px}}.project-summary{{gap:5px}}.theme-group{{margin-left:8px}}}}
{chart_css}
</style></head><body><main><header class="site-head"><h1>{heading}</h1>{scope_line}</header>
<div class="toolbar"><label class="search"><span class="sr-only">Search boards</span><input id="board-filter" type="search" placeholder="Search boards" aria-label="Search boards" autocomplete="off"></label>{kind_bar}</div>
{chart_markup}
<div id="board-list" class="board-list project-groups" role="list" aria-label="Projects">{body}</div><p id="no-results" class="no-results"{" hidden" if (any_shown or not open_cards) else ""}>No matching boards.</p></main><script>
const filter = document.getElementById('board-filter');
const noResults = document.getElementById('no-results');
const groups = Array.from(document.querySelectorAll('.project-group'));
const projectLists = Array.from(document.querySelectorAll('.space-projects'));
const kindToggles = Array.from(document.querySelectorAll('.kind-toggle'));
const FOLD_OPEN_MAX = {FOLD_OPEN_MAX};
const KIND_ORDER = kindToggles.map((toggle) => toggle.dataset.kind).filter((k) => k !== 'all');
const storagePrefix = 'fusion-space:home:' + location.origin + location.pathname;
const orderStorageKey = storagePrefix + ':project-order';
// v3 keeps only the folds a person chose ({{key: open}}); every other Project
// follows the default: open when the view holds at most FOLD_OPEN_MAX Projects.
const collapsedStorageKey = storagePrefix + ':project-collapsed:v3';
let selectedKinds = new Set(kindToggles
  .filter((toggle) => toggle.dataset.kind !== 'all' && toggle.getAttribute('aria-pressed') === 'true')
  .map((toggle) => toggle.dataset.kind));

function readStorage(key, fallback) {{
  try {{
    const value = JSON.parse(window.localStorage.getItem(key) || 'null');
    return value === null ? fallback : value;
  }} catch (error) {{
    return fallback;
  }}
}}
function writeStorage(key, value) {{
  try {{ window.localStorage.setItem(key, JSON.stringify(value)); }}
  catch (error) {{ /* private browsing or a restricted origin */ }}
}}
function currentGroups() {{
  return Array.from(document.querySelectorAll('.project-group'));
}}
function saveOrder() {{
  writeStorage(orderStorageKey, currentGroups().map((group) => group.dataset.projectKey));
}}
function restoreOrder() {{
  const saved = readStorage(orderStorageKey, []);
  if (!Array.isArray(saved)) return;
  const order = new Map(saved.map((key, index) => [String(key), index]));
  projectLists.forEach((projectList) => {{
    const ordered = Array.from(projectList.children)
      .filter((child) => child.classList.contains('project-group'))
      .sort((left, right) =>
        (order.get(left.dataset.projectKey) ?? Number.MAX_SAFE_INTEGER) -
        (order.get(right.dataset.projectKey) ?? Number.MAX_SAFE_INTEGER));
    ordered.forEach((group) => projectList.appendChild(group));
  }});
}}
function foldChoices() {{
  const saved = readStorage(collapsedStorageKey, {{}});
  return saved && typeof saved === 'object' && !Array.isArray(saved) ? saved : {{}};
}}
function saveCollapsed(group) {{
  const choices = foldChoices();
  choices[group.dataset.projectKey] = group.open;
  writeStorage(collapsedStorageKey, choices);
}}
function restoreCollapsed() {{
  const choices = foldChoices();
  const visible = groups.filter((group) => !group.hidden).length;
  groups.forEach((group) => {{
    const key = group.dataset.projectKey;
    group.open = Object.prototype.hasOwnProperty.call(choices, key)
      ? Boolean(choices[key]) : visible <= FOLD_OPEN_MAX;
  }});
}}
function projectAtPoint(x, y) {{
  const node = document.elementFromPoint(x, y);
  return node ? node.closest('.project-group') : null;
}}
function placeGroup(group, target, clientY) {{
  if (!group || !target || group === target) return false;
  const projectList = group.parentElement;
  if (!projectList || target.parentElement !== projectList) return false;
  const rect = target.getBoundingClientRect();
  if (clientY < rect.top + rect.height / 2) projectList.insertBefore(group, target);
  else {{
    const reference = target.nextElementSibling;
    if (reference === group) return false;
    if (reference) projectList.insertBefore(group, reference);
    else projectList.appendChild(group);
  }}
  return true;
}}
let draggedGroup = null;
let pointerGroup = null;
let pointerId = null;
let pointerStartX = 0;
let pointerStartY = 0;
let pointerMoved = false;
function clearDragState() {{
  if (draggedGroup) draggedGroup.classList.remove('dragging');
  groups.forEach((group) => group.classList.remove('drag-over'));
  draggedGroup = null;
  pointerGroup = null;
  pointerId = null;
  pointerMoved = false;
}}
groups.forEach((group) => {{
  // Only a person's click on the fold is remembered; a fold the page opens
  // itself (a search hit, the default) is not a choice.
  const summary = group.querySelector('.project-summary');
  summary.addEventListener('click', () => {{ group.dataset.userToggle = '1'; }});
  group.addEventListener('toggle', () => {{
    if (group.dataset.userToggle !== '1') return;
    delete group.dataset.userToggle;
    saveCollapsed(group);
  }});
  const grip = group.querySelector('.project-grip');
  grip.addEventListener('click', (event) => {{
    event.preventDefault();
    event.stopPropagation();
  }});
  grip.addEventListener('pointerdown', (event) => {{
    pointerGroup = group;
    pointerId = event.pointerId;
    pointerStartX = event.clientX;
    pointerStartY = event.clientY;
    pointerMoved = false;
    draggedGroup = group;
    if (grip.setPointerCapture) grip.setPointerCapture(event.pointerId);
    event.preventDefault();
  }});
  grip.addEventListener('pointermove', (event) => {{
    if (pointerGroup !== group || pointerId !== event.pointerId) return;
    const distance = Math.hypot(event.clientX - pointerStartX,
                                event.clientY - pointerStartY);
    if (!pointerMoved && distance < 8) return;
    pointerMoved = true;
    draggedGroup = group;
    group.classList.add('dragging');
    event.preventDefault();
    groups.forEach((candidate) => candidate.classList.remove('drag-over'));
    const target = projectAtPoint(event.clientX, event.clientY);
    if (target && target !== group) target.classList.add('drag-over');
  }});
  const finishPointerDrag = (event) => {{
    if (pointerGroup !== group || pointerId !== event.pointerId) return;
    if (pointerMoved) {{
      event.preventDefault();
      const target = projectAtPoint(event.clientX, event.clientY);
      if (placeGroup(group, target, event.clientY)) saveOrder();
    }}
    if (grip.hasPointerCapture && grip.hasPointerCapture(event.pointerId))
      grip.releasePointerCapture(event.pointerId);
    clearDragState();
  }};
  grip.addEventListener('pointerup', finishPointerDrag);
  grip.addEventListener('pointercancel', finishPointerDrag);
}});
restoreOrder();
restoreCollapsed();
function kindQuery(kinds) {{
  const ordered = KIND_ORDER.filter((kind) => kinds.has(kind));
  return ordered.length ? '?kind=' + ordered.join(',') : '';
}}
// a kind link keeps every other part of the address (`project=`), as the server writes it
function kindHref(kinds) {{
  const params = new URLSearchParams(location.search);
  params.delete('kind');
  const rest = params.toString();
  const kq = kindQuery(kinds);
  return kq ? kq + (rest ? '&' + rest : '') : (rest ? '?' + rest : '?');
}}
function syncKindToggles() {{
  kindToggles.forEach((toggle) => {{
    const kind = toggle.dataset.kind;
    const pressed = kind === 'all' ? selectedKinds.size === 0 : selectedKinds.has(kind);
    toggle.setAttribute('aria-pressed', pressed ? 'true' : 'false');
    const after = new Set(selectedKinds);
    if (kind !== 'all') {{ if (after.has(kind)) after.delete(kind); else after.add(kind); }}
    toggle.setAttribute('href', kindHref(kind === 'all' ? new Set() : after));
  }});
}}
function applyFilter() {{
  const query = filter.value.trim().toLowerCase();
  let visible = 0;
  groups.forEach((group) => {{
    const groupMatch = !query || group.dataset.search.toLowerCase().includes(query);
    let groupVisible = 0;
    group.querySelectorAll('.theme-group').forEach((theme) => {{
      let themeVisible = 0;
      theme.querySelectorAll('.home-row').forEach((row) => {{
        const kindMatch = selectedKinds.size === 0 || selectedKinds.has(row.dataset.kind);
        const match = kindMatch && (groupMatch || row.dataset.search.toLowerCase().includes(query));
        row.hidden = !match;
        if (match) themeVisible += 1;
      }});
      theme.hidden = themeVisible === 0;
      const count = theme.querySelector('.theme-count');
      count.textContent = themeVisible;
      count.setAttribute('aria-label', themeVisible + ' blocks');
      groupVisible += themeVisible;
    }});
    group.hidden = groupVisible === 0;
    const count = group.querySelector('.project-count');
    count.textContent = groupVisible;
    count.setAttribute('aria-label', groupVisible + ' blocks');
    if (query && groupVisible) group.open = true;
    visible += groupVisible;
  }});
  document.querySelectorAll('.space-section').forEach((section) => {{
    section.hidden = !Array.from(section.querySelectorAll('.project-group'))
      .some((group) => !group.hidden);
  }});
  noResults.hidden = visible !== 0 || (!query && selectedKinds.size === 0);
  document.dispatchEvent(new CustomEvent('space-home-filter', {{detail: {{query, kinds: [...selectedKinds]}}}}));
}}
kindToggles.forEach((toggle) => {{
  toggle.addEventListener('click', (event) => {{
    event.preventDefault();
    const kind = toggle.dataset.kind;
    if (kind === 'all') selectedKinds = new Set();
    else if (selectedKinds.has(kind)) selectedKinds.delete(kind);
    else selectedKinds.add(kind);
    syncKindToggles();
    // the address bar carries the view, so a copied link reproduces it
    const search = kindHref(selectedKinds);
    history.replaceState(null, '', location.pathname + (search === '?' ? '' : search) + location.hash);
    applyFilter();
    if (!filter.value.trim()) restoreCollapsed();
  }});
}});
filter.addEventListener('input', applyFilter);
</script><script>{chart_js}</script></body></html>'''


class HomeMixin:
    def serve_home(self):
        # `?kind=task[,paper]` and `?project=<Project>` render the filtered view, so a shared
        # link reproduces it
        query = parse_qs(urlsplit(self.path).query)
        kind = ",".join(query.get("kind", []))
        project = (query.get("project") or [""])[0]
        body = render_home(
            self.root,
            getattr(self, "space_name", ""),
            getattr(self, "public_url", ""),
            kind=kind,
            project=project,
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def is_home_request(self):
        path = urlsplit(self.path).path.rstrip("/") or "/"
        return path in {"/", "/boards"}

    def short_request(self):
        """`/b/<slug>` or `/b/<slug>/<page-id>`, or None for anything else."""
        path = urlsplit(self.path).path.rstrip("/")
        m = re.match(r"^/b/([^/]+)(?:/([^/]+))?$", path)
        return (m.group(1), m.group(2) or "") if m else None

    def workbench_request(self):
        """`/w/<slug>[/<page-id>[/<tab>]]` -> (slug, page-id, tab), else None."""
        path = urlsplit(self.path).path.rstrip("/")
        m = re.match(r"^/w/([^/]+)(?:/([^/]+))?(?:/([^/]+))?$", path)
        return (m.group(1), m.group(2) or "", m.group(3) or "") if m else None

    def serve_workbench(self, slug, anchor, tab):
        """302 to the long `/_board/<route>?path=…&file=…` URL, or a 404 that says why.

        The Location is path-only on purpose: the browser keeps whatever host
        it arrived on, so one link body works for every DOMAIN the server is
        reachable at (127.0.0.1, the Tailscale IP, a configured public URL).
        Extra query (`?run=…`, `&lens=…`) is carried across.
        """
        if slug == "shared" and not anchor and board_by_slug(self.root.resolve(), slug) is None:
            # The Shared Workbench is served at its short address itself; the bar keeps /w/shared.
            return self.shared_view(head_only=self.command == "HEAD")
        target, reason = resolve_workbench(self.root, slug, anchor, tab, getattr(self, "only", None) or frozenset())
        if target is None:
            return self.send_error(404, reason)
        query = urlsplit(self.path).query
        if query:
            target = f"{target}&{query}"
        self.send_response(302)
        self.send_header("Location", target)
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def serve_short(self, slug, anchor):
        """302 to the live Page reader (or the Board workbench), keeping the query string.

        A redirect rather than serving the bytes here, so the address bar ends
        up on the canonical URL: every relative link, asset and write-back path
        inside the page is written against that location, and serving the file
        from `/b/...` would break all of them.
        """
        target = resolve_short(self.root, slug, anchor, getattr(self, "only", None) or frozenset())
        if target is None:
            return self.send_error(404, "no such board or page")
        query = urlsplit(self.path).query
        if query:
            target = f"{target}?{query}"
        self.send_response(302)
        self.send_header("Location", target)
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Content-Length", "0")
        self.end_headers()
