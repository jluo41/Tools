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

from src.common import page_files


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
    for candidate in (board, *board.parents):
        if candidate == root.parent:
            break
        if not candidate.is_relative_to(root):
            continue
        manifest = _project_manifest(candidate)
        if manifest:
            rel = candidate.relative_to(root).as_posix()
            return {"project": manifest.get("id", candidate.name),
                    "project_path": rel, "project_key": f"project:{rel}",
                    "project_scope": "project",
                    "project_profile": manifest.get("profile", ""),
                    "project_state": manifest.get("state", "")}

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


def discover_boards(root: Path) -> list[dict[str, object]]:
    """Read lightweight metadata from every real Board source folder."""
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
        pages = list(page_files(board))
        states = [STATE.search(p.read_text(encoding="utf-8", errors="ignore")) for p in pages]
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
    if len(matches) != 1:
        return None
    board = matches[0]

    site = board / "board"
    rel = board.relative_to(root).as_posix()
    if not (site / "index.html").is_file():
        return None
    anchor = (anchor or "").strip().strip("/")
    if anchor:
        for page in sorted(site.glob("*/*.html")):
            if page.stem.split("-")[0].lower() == anchor.lower():
                return "/" + quote(f"{rel}/board/{page.parent.name}/{page.name}",
                                   safe="/")
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
    """
    cards = discover_boards(root)
    open_cards = [card for card in cards if card["ready"]]
    rows = []
    for card in open_cards:
        title = html.escape(str(card["title"]))
        href = html.escape(str(card["href"]), quote=True)
        search = html.escape(
            " ".join((str(card["project"]), str(card["title"]),
                      str(card["slug"]), str(card["path"]),
                      str(card["spine"]), str(card["kind"]))),
            quote=True,
        )
        rows.append(
            f'''<a class="ir home-row" href="{href}" data-search="{search}"
  role="listitem"><span class="t">{title}</span></a>''')
    if rows:
        body = "\n".join(rows)
    elif cards:
        body = '<p class="empty">No boards are ready to open.</p>'
    else:
        body = '<p class="empty">No boards found below this SPACE root.</p>'
    heading = html.escape(space_name.strip() or "Boards")
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
.board-list{{min-width:0}}.ir{{position:relative;display:flex;gap:10px;align-items:baseline;padding:9px 13px;border:1px solid var(--line);border-radius:var(--radius-surface);margin:6px 0;text-decoration:none;color:var(--fg);background:var(--card);overflow:hidden}}.ir:hover{{border-color:var(--accent)}}.ir .t{{flex:1;min-width:0;overflow-wrap:anywhere;font-weight:600}}.empty,.no-results{{color:var(--mut);padding:14px 0}}[hidden]{{display:none!important}}.sr-only{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}}
@media (max-width:680px){{main{{padding:28px 14px 62px}}.site-head{{margin-bottom:18px}}h1{{font-size:24px}}.search input{{min-height:40px}}.ir{{padding:9px 12px}}}}
</style></head><body><main><header class="site-head"><h1>{heading}</h1></header>
<div class="toolbar"><label class="search"><span class="sr-only">Search boards</span><input id="board-filter" type="search" placeholder="Search boards" aria-label="Search boards" autocomplete="off"></label></div>
<div id="board-list" class="board-list" role="list" aria-label="Boards">{body}</div><p id="no-results" class="no-results" hidden>No matching boards.</p></main><script>
const filter = document.getElementById('board-filter');
const noResults = document.getElementById('no-results');
const rows = Array.from(document.querySelectorAll('.home-row'));
function applyFilter() {{
  const query = filter.value.trim().toLowerCase();
  let visible = 0;
  rows.forEach((row) => {{
    const match = !query || row.dataset.search.toLowerCase().includes(query);
    row.hidden = !match;
    if (match) visible += 1;
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
