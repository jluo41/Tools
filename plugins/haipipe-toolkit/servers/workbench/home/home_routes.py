"""The SPACE Home's short addresses: `/b/<board>[/<page>]` and `/w/<board>[/<page>[/<tab>]]`.

Each resolves, from what is on disk, to the long `/_board/...` URL the server redirects to.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote, urlencode

from src.body import group_token
from src.common import page_files
from src.parse import parse_dir

from live.home_boards import board_by_slug, board_workbench_route, frame_url


def old_page_url(board: Path, root: Path) -> str | None:
    """The Board-level page its theme drew before the frame (`/_board/<route>?path=…`), or None."""
    route = board_workbench_route(board)
    if route is None:
        return None
    rel = board.resolve().relative_to(root.resolve()).as_posix()
    return "/_board/%s?path=%s&file=board.md" % (route, quote(f"{rel}/board.md", safe="/"))


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


# A tab of a Task's Page -> its Space and subspace in the frame (workbench-task-draft/task_draft.py PAGE_VIEWS, JL 261007)
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
