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
from urllib.parse import quote, urlsplit

from src.body import group_token
from src.common import page_files
from src.parse import parse_dir


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
    ("Discovery Board", "🔎"),
    ("Paper Board", "📄"),
    ("Design Board", "🎨"),
    ("Skill Board", "🧩"),
)
HOME_BRAND = "SPACE Home"      # the heading when settings.env has no SPACE_NAME
PROJECT_FIELD = re.compile(r"^(id|profile|state):\s*(.*?)\s*$")


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
    if "discoveries" in parts:
        return "Discovery Board", "🔎"
    if board.name.lower().endswith("-designboard"):
        return "Design Board", "🎨"
    if "papers" in parts or "paper" in parts or "0-lifecycle" in parts:
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


def discover_boards(root: Path, *, include_page_state: bool = True) -> list[dict[str, object]]:
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
        ready = (board / "board" / "index.html").is_file()
        kind, icon = board_kind(board, root)
        owner = project_owner(board, root)
        cards.append({"title": title, "spine": spine, "path": rel,
                      "pages": len(pages), "settled": settled, "ready": ready,
                      "kind": kind, "icon": icon,
                      "slug": board_slug(board.name, board.parent.name),
                      "href": "/" + quote((board.relative_to(root) / "board" / "index.html").as_posix(), safe="/"),
                      **owner})
    return sorted(cards, key=lambda c: (
        0 if c["project_scope"] == "project" else 1,
        str(c["project_path"]).lower(), str(c["kind"]).lower(),
        str(c["path"]).lower()))


def home_folder_path(card: dict[str, object]) -> str:
    """Return the short folder address shown below a Home Board title."""
    kind = str(card["kind"])
    if kind.endswith(" Board"):
        kind = kind[:-len(" Board")]
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
    "": "outline", "outline": "outline", "page": "outline",
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
    refuse: `dialect: paper` -> paper; a Design Board -> design-board; an
    InsightBoard -> insight-board; `board-kind: labeling-board` -> labeling-board.
    """
    try:
        text = (board / "board.md").read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    m = _DIALECT.search(text)
    if m and m.group(1) == "paper":
        return "paper"
    kind = (_BOARD_KIND.search(text) or [None, ""])[1]
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
                      tab: str = "") -> tuple[str | None, str]:
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
    if board is None:
        return None, "no such board"
    rel = board.relative_to(root).as_posix()
    anchor = (anchor or "").strip().strip("/")
    tab = (tab or "").strip().strip("/").lower()
    if not anchor:
        if tab:
            return None, "a Board-level workbench has no tabs; name a page first"
        route = board_workbench_route(board)
        if route is None:
            return None, ("this Board declares no board-level workbench "
                          "(no `dialect: paper`, Design, Insight, or labeling Board)")
        return ("/_board/%s?path=%s&file=board.md"
                % (route, quote(f"{rel}/board.md", safe="/"))), "ok"
    if tab not in WORKBENCH_TABS:
        return None, "unknown tab %r; one of %s" % (
            tab, ", ".join(sorted(k for k in WORKBENCH_TABS if k)))
    route = WORKBENCH_TABS[tab]
    wanted = anchor.lower()
    pages = []
    try:  # the Board's own page ids first (`QA1`, `S-Label-1`): the grammar knows them
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
            if wanted in aliases:
                pages.append(source)
    pages = sorted(set(pages))
    if len(pages) != 1:
        return None, ("no such page" if not pages else "ambiguous page id")
    page_rel = pages[0].relative_to(board).as_posix()
    if route == "labeling":
        # The 🏷 view binds to the generated Page it sits beside: `path` is the
        # Board source, `file` the Page Face, `page` the built html (see
        # workbench-labeling's `studio_chat_page_url`). All three come from disk.
        generated = resolve_short(root, slug, anchor)
        if generated is None:
            return None, "the labeling tab needs the built Board page; run build.py first"
        # `path` and `page` must share one spelling: the view compares them as
        # strings, and the drawer sends both with the leading slash of a URL path.
        return ("/_board/labeling?path=%s&file=%s&page=%s"
                % (quote(f"/{rel}/board.md", safe="/"), quote(page_rel, safe="/"),
                   quote(generated, safe="/"))), "ok"
    return ("/_board/%s?path=%s&file=%s"
            % (route, quote(f"{rel}/{page_rel}", safe="/"), quote(page_rel, safe="/"))), "ok"


def resolve_short(root: Path, slug: str, anchor: str = "") -> str | None:
    """QE2 · `/b/<slug>[/<page-id>]` -> the path of the real generated file.

    The long half of a board URL is the path from the SPACE root down to the
    board folder: 78 of the 131 characters JL measured on 260802, and the part
    that says nothing to the person reading the strip. This resolves the slug
    against the boards already discovered for the Home page, so there is no
    second registry to keep honest.

    `anchor` is a page id (`QE2`), a group code (`QE`), or empty for the Index.
    An unknown board or an unknown page is None, and the caller sends 404
    rather than guessing: a redirect to the wrong board is worse than a miss.
    """
    root = root.resolve()
    board = board_by_slug(root, slug)
    if board is None:
        return None

    site = board / "board"
    rel = board.relative_to(root).as_posix()
    if not (site / "index.html").is_file():
        return None
    anchor = (anchor or "").strip().strip("/")
    if anchor:
        for page in sorted(site.glob("*/*.html")):
            aliases = {page.stem.lower(), page.stem.split("-")[0].lower()}
            # a Task Board page is built as `b01j21t01-adhd_cohort_universe`,
            # but people link it by its Task FOLDER, `t01_adhd_cohort_universe`
            task = re.fullmatch(r"b\d+j\d+(t\d+)-(.+)", page.stem.lower())
            if task:
                aliases.add(f"{task.group(1)}_{task.group(2)}")
            if anchor.lower() in aliases:
                return "/" + quote(f"{rel}/board/{page.parent.name}/{page.name}",
                                   safe="/")
        # a page id with hyphens (`S-Label-1`) is not a stem prefix: ask the
        # Board grammar, which knows every page's id, file and group token
        try:
            _, declared, _ = parse_dir(board)
        except Exception:  # noqa: BLE001
            declared = []
        for page in declared:
            if str(page.get("id") or "").lower() != anchor.lower() or not page.get("file"):
                continue
            group = group_token(page.get("group") or "") or "_ungrouped"
            generated = site / group / (Path(page["file"]).stem + ".html")
            if generated.is_file():
                return "/" + quote(f"{rel}/board/{group}/{generated.name}", safe="/")
        group = site / f"{anchor}.html"
        if group.is_file():
            return "/" + quote(f"{rel}/board/{anchor}.html", safe="/")
        return None
    return "/" + quote(f"{rel}/board/index.html", safe="/")


def render_home(root: Path, space_name: str = "", public_url: str = "") -> str:
    """Render a compact, mobile-first directory for the boards in one SPACE.

    Home is an entry index, not a status dashboard.  Only Boards with a
    generated index are shown because every visible row must be actionable.
    The source metadata remains available to the search index and to the
    Board itself, but it is deliberately not repeated in the directory.
    Project grouping is derived from the same ownership metadata as before;
    collapse state and ordering are browser-local preferences, never source
    files or a second registry.
    """
    cards = discover_boards(root, include_page_state=False)
    open_cards = [card for card in cards if card["ready"]]
    section_groups: dict[str, dict[str, list[dict[str, object]]]] = {}
    for card in open_cards:
        section = home_section(card)
        projects = section_groups.setdefault(section, {})
        projects.setdefault(str(card["project_key"]), []).append(card)

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
        for project_key, group_cards in project_groups.items():
            project_name = str(group_cards[0]["project"])
            project_label = html.escape(project_name, quote=True)
            project_key_attr = html.escape(project_key, quote=True)
            group_search = html.escape(
                " ".join((project_name, str(group_cards[0]["project_path"]))),
                quote=True,
            )
            rows = []
            for card in group_cards:
                title = html.escape(str(card["title"]))
                folder = html.escape(home_folder_path(card))
                href = html.escape(str(card["href"]), quote=True)
                row_search = html.escape(
                    " ".join((project_name, str(card["title"]),
                              str(card["slug"]), str(card["path"]),
                              str(card["spine"]), str(card["kind"]))),
                    quote=True,
                )
                rows.append(
                    f'''<a class="ir home-row" href="{href}" data-search="{row_search}"
  role="listitem"><span class="home-copy"><span class="t">{title}</span>
  <span class="home-folder">{folder}</span></span></a>''')
            group_id = f"project-list-{project_index}"
            project_index += 1
            project_rows.append(
                f'''<details class="project-group" data-project-key="{project_key_attr}"
  data-search="{group_search}" role="listitem"><summary class="project-summary"
  aria-controls="{group_id}"><span class="project-grip"
  role="img" aria-label="Drag to reorder {project_label}" title="Drag to reorder">⠿</span>
  <span class="project-name">{project_label}</span></summary>
  <div id="{group_id}" class="project-list" role="list" aria-label="{project_label} boards">
  {''.join(rows)}</div></details>''')
        section_id = f"space-title-{len(groups)}"
        hide_heading = hide_implicit_space and section == "SPACE"
        section_heading = "" if hide_heading else (
            f'<h2 class="space-heading" id="{section_id}">{section_label}</h2>')
        section_accessibility = ('aria-label="Boards"' if hide_heading else
                                 f'aria-labelledby="{section_id}"')
        groups.append(
            f'''<section class="space-section" data-space-key="{section_label}"
  data-search="{section_label}" {section_accessibility}>
  {section_heading}
  <div class="space-projects" role="list" aria-label="{section_label} projects">
  {''.join(project_rows)}</div></section>''')
    if groups:
        body = "\n".join(groups)
    elif cards:
        body = '<p class="empty">No boards are ready to open.</p>'
    else:
        body = '<p class="empty">No boards found below this SPACE root.</p>'
    heading = html.escape(space_name.strip() or HOME_BRAND)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{heading}</title><style>
:root{{color-scheme:light;--bg:#ffffff;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4e7;--card:#f7f7f8;--accent:#1f5aa8;--focus:#075fbd;--radius-control:7px;--radius-surface:10px}}
@media(prefers-color-scheme:dark){{:root{{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;--line:#2c2e33;--card:#1d1f23;--accent:#6ea8f0;--focus:#9dc8ff}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.7 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif}}
:where(a,input):focus-visible{{outline:3px solid var(--focus);outline-offset:3px;border-radius:var(--radius-control)}}
main{{max-width:820px;margin:0 auto;padding:34px 22px 90px}}
.site-head{{margin:0 0 22px}}h1{{font-size:26px;line-height:1.35;margin:0;font-weight:700}}
.toolbar{{margin:0 0 12px}}.search{{display:block;max-width:420px}}.search input{{width:100%;min-height:38px;border:1px solid var(--line);border-radius:var(--radius-control);background:var(--card);color:var(--fg);font:inherit;padding:5px 9px;outline:none}}.search input::placeholder{{color:var(--mut)}}.search input:focus{{border-color:var(--accent)}}
.board-list{{min-width:0}}.space-section{{margin:26px 0 0}}.space-heading{{margin:0;padding:0 0 7px;border-bottom:2px solid var(--fg);font-size:12px;line-height:1.4;letter-spacing:.15em;text-transform:uppercase;color:var(--mut)}}.space-projects{{min-width:0}}.project-group{{margin:17px 0 0;min-width:0}}.project-summary{{display:flex;align-items:center;gap:7px;min-height:34px;padding:0 0 7px;border-bottom:1px solid var(--line);list-style:none;cursor:pointer;color:var(--fg);font-size:16px;font-weight:700}}.project-summary::-webkit-details-marker{{display:none}}.project-summary::before{{content:"▸";width:11px;color:var(--accent);font-size:11px;line-height:1}}.project-group[open]>.project-summary::before{{content:"▾"}}.project-grip{{color:var(--mut);font:14px/1 ui-monospace,Menlo,monospace;cursor:grab;user-select:none;touch-action:none;opacity:.72}}.project-grip:active{{cursor:grabbing}}.project-name{{min-width:0;overflow-wrap:anywhere}}.project-list{{min-width:0;padding-top:2px}}.project-group.dragging{{opacity:.55}}.project-group.drag-over>.project-summary{{border-color:var(--accent)}}.ir{{position:relative;display:flex;gap:10px;align-items:baseline;padding:9px 13px;border:1px solid var(--line);border-radius:var(--radius-surface);margin:6px 0;text-decoration:none;color:var(--fg);background:var(--card);overflow:hidden}}.ir:hover{{border-color:var(--accent)}}.home-copy{{display:flex;flex:1;min-width:0;flex-direction:column;gap:1px}}.ir .t{{min-width:0;overflow-wrap:anywhere;font-weight:600}}.home-folder{{min-width:0;color:var(--mut);font:12px/1.55 ui-monospace,Menlo,monospace;overflow-wrap:anywhere;word-break:break-word}}.empty,.no-results{{color:var(--mut);padding:14px 0}}[hidden]{{display:none!important}}.sr-only{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}}
@media (max-width:680px){{main{{padding:28px 14px 62px}}.site-head{{margin-bottom:18px}}h1{{font-size:24px}}.search input{{min-height:40px}}.ir{{padding:9px 12px}}.project-summary{{gap:5px}}}}
</style></head><body><main><header class="site-head"><h1>{heading}</h1></header>
<div class="toolbar"><label class="search"><span class="sr-only">Search boards</span><input id="board-filter" type="search" placeholder="Search boards" aria-label="Search boards" autocomplete="off"></label></div>
<div id="board-list" class="board-list project-groups" role="list" aria-label="Projects">{body}</div><p id="no-results" class="no-results" hidden>No matching boards.</p></main><script>
const filter = document.getElementById('board-filter');
const noResults = document.getElementById('no-results');
const groups = Array.from(document.querySelectorAll('.project-group'));
const projectLists = Array.from(document.querySelectorAll('.space-projects'));
const storagePrefix = 'fusion-space:home:' + location.origin + location.pathname;
const orderStorageKey = storagePrefix + ':project-order';
// v2 makes the new default (all Projects closed) apply once to existing tabs;
// explicit choices made after that continue to persist locally.
const collapsedStorageKey = storagePrefix + ':project-collapsed:v2';

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
function saveCollapsed() {{
  writeStorage(collapsedStorageKey,
    groups.filter((group) => !group.open).map((group) => group.dataset.projectKey));
}}
function restoreCollapsed() {{
  const saved = readStorage(collapsedStorageKey, null);
  if (!Array.isArray(saved)) return;
  const collapsed = new Set(saved.map((key) => String(key)));
  groups.forEach((group) => {{ group.open = !collapsed.has(group.dataset.projectKey); }});
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
  group.addEventListener('toggle', saveCollapsed);
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
function applyFilter() {{
  const query = filter.value.trim().toLowerCase();
  let visible = 0;
  groups.forEach((group) => {{
    const groupMatch = !query || group.dataset.search.toLowerCase().includes(query);
    const groupRows = Array.from(group.querySelectorAll('.home-row'));
    let groupVisible = 0;
    groupRows.forEach((row) => {{
      const match = groupMatch || row.dataset.search.toLowerCase().includes(query);
      row.hidden = !match;
      if (match) groupVisible += 1;
    }});
    group.hidden = groupVisible === 0;
    if (query && groupVisible) group.open = true;
    visible += groupVisible;
  }});
  document.querySelectorAll('.space-section').forEach((section) => {{
    section.hidden = !Array.from(section.querySelectorAll('.project-group'))
      .some((group) => !group.hidden);
  }});
  noResults.hidden = visible !== 0 || !query;
}}
filter.addEventListener('input', applyFilter);
</script></body></html>'''


class HomeMixin:
    def serve_home(self):
        body = render_home(
            self.root,
            getattr(self, "space_name", ""),
            getattr(self, "public_url", ""),
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
        target, reason = resolve_workbench(self.root, slug, anchor, tab)
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
        """302 to the real generated file, keeping the query string.

        A redirect rather than serving the bytes here, so the address bar ends
        up on the canonical URL: every relative link, asset and write-back path
        inside the page is written against that location, and serving the file
        from `/b/...` would break all of them.
        """
        target = resolve_short(self.root, slug, anchor)
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
