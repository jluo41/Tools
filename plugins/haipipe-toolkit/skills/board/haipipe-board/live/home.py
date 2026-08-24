"""The read-only SPACE-level Board Home.

This is deliberately not a Board: no board.md, no chat, no durable state.  It
discovers the Board folders already present below the server root and gives the
reader one stable place from which to enter them.
"""

from __future__ import annotations

import html
import os
import re
from pathlib import Path
from urllib.parse import quote, urlsplit

from src.common import page_files


# Folders that cannot contain a board and are expensive to walk. `board` is the
# GENERATED tree under every board; `_WorkSpace` is the gitignored data store.
SKIP_PARTS = {".git", ".venv", "node_modules", "__pycache__", "_archive", "board",
              "_WorkSpace", "site-packages", ".pytest_cache", "dist", "build"}
TITLE = re.compile(r"^#\s+(.+?)\s*$", re.M)
SPINE = re.compile(r"^spine:\s*(.+?)\s*$", re.M)
STATE = re.compile(r"^state:\s*(✅|🟡|🔴|⏸️)", re.M)
BOARD_KINDS = (
    ("Task Board", "📋"),
    ("Paper Board", "📄"),
    ("Skill Board", "🧩"),
)


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
    if "papers" in parts or "paper" in parts or "0-lifecycle" in parts:
        return "Paper Board", "📄"
    return "Task Board", "📋"


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
        cards.append({"title": title, "spine": spine, "path": rel,
                      "pages": len(pages), "settled": settled, "ready": ready,
                      "kind": kind, "icon": icon,
                      "slug": board_slug(board.name, board.parent.name),
                      "href": "/" + quote((board.relative_to(root) / "board" / "index.html").as_posix(), safe="/")})
    return sorted(cards, key=lambda c: str(c["path"]).lower())


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
    """One table, one row per board — the same shape as a board Index's page
    table (`bstat`), because that is the layout JL reads fastest (260819:
    "arrange the board like the page index"). Kind headers are the gray group
    rows; the spine is a hover tooltip, not a column, so 13 boards fit one
    screen without scrolling."""
    cards = discover_boards(root)
    rows = []
    for kind, icon in BOARD_KINDS:
        kind_cards = [card for card in cards if card["kind"] == kind]
        if not kind_cards:
            continue
        rows.append(f'<tr class="bsg"><td colspan="4">{icon} {kind}s · {len(kind_cards)}</td></tr>')
        for card in kind_cards:
            title = html.escape(str(card["title"]))
            spine = html.escape(str(card["spine"]), quote=True)
            path = html.escape(str(card["path"]))
            slug = html.escape(str(card["slug"]))
            href = html.escape(str(card["href"]), quote=True)
            pages, settled = card["pages"], card["settled"]
            if card["ready"]:
                state = "✅" if pages and settled == pages else "🟡"
                cls = "bs-ok" if pages and settled == pages else "bs-warn"
                id_cell = f'<a href="{href}">{state} {slug}</a>'
                title_cell = (f'<a class="bt" href="{href}" title="{spine}">{title}</a>'
                              f'<br><span class="path">{path}</span>')
                # Two doors, because they are two different jobs: reading the
                # board is one document, OPERATING it (QD5) is three panes with
                # a chat beside the page. Same board either way.
                # The split is what a board opens as now, so it is the plain
                # link; `?plain` is the opt-out back to the one-document board.
                action = (f'<a class="split" href="{href}?plain"'
                          f' title="The one-document board: sidebar, page and drawer in a single page">↗ plain</a>'
                          f'<a class="open" href="{href}">Open →</a>')
            else:
                state, cls = "🔴", "bs-no"
                id_cell = f'{state} {slug}'
                title_cell = (f'<span class="bt" title="{spine}">{title}</span>'
                              f'<br><span class="path">{path}</span>')
                action = '<span class="build">Build needed</span>'
            rows.append(f'<tr><th class="bsp">{id_cell}</th><td>{title_cell}</td>'
                        f'<td class="{cls}">{settled}/{pages}</td><td class="bact">{action}</td></tr>')
    table = "\n".join(rows)
    body = (f'''<div class="bwrap"><table class="bhome"><thead>
<tr><th>board</th><th>title</th><th>🎯 settled</th><th>open</th></tr></thead>
<tbody>{table}</tbody></table></div>''' if rows
            else '<p class="empty">No board.md files found below this SPACE root.</p>')
    label = html.escape(space_name.strip() or "SPACE")
    heading = html.escape(f"JJ-LUO / {space_name.strip()} Boards" if space_name.strip() else "SPACE Boards")
    url_note = (f' · <a href="{html.escape(public_url, quote=True)}">{html.escape(public_url)}</a>'
                if public_url.strip() else "")
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{heading}</title><style>
:root{{color-scheme:light;--ink:#202124;--mut:#6b7280;--line:#e5e7eb;--bg:#fafafa;--card:#fff;--accent:#2867b2}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
main{{max-width:1060px;margin:0 auto;padding:clamp(22px,5vw,56px) clamp(16px,4vw,36px)}}
h1{{font-size:clamp(28px,5vw,46px);letter-spacing:-.04em;margin:0 0 6px}}.lead{{margin:0 0 20px;color:var(--mut)}}
.bwrap{{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:var(--card);box-shadow:0 1px 2px #00000008}}
table.bhome{{width:100%;border-collapse:collapse}}
.bhome th,.bhome td{{padding:8px 14px;text-align:left;vertical-align:top;font-size:14px;border-top:1px solid var(--line)}}
.bhome thead th{{border-top:0;background:#f9fafb;color:var(--mut);font-size:12px;font-weight:700}}
tr.bsg td{{background:#f3f4f6;font-weight:700;font-size:13px;color:#374151}}
th.bsp{{white-space:nowrap;font-weight:700}}th.bsp a{{color:var(--ink);text-decoration:none}}th.bsp a:hover{{text-decoration:underline}}
a.bt{{color:var(--ink);text-decoration:none;font-weight:600}}a.bt:hover{{text-decoration:underline}}span.bt{{font-weight:600}}
.path{{color:var(--mut);font:11px ui-monospace,SFMono-Regular,Menlo,monospace;overflow-wrap:anywhere}}
td.bs-ok{{color:#116329;font-weight:700;white-space:nowrap}}td.bs-warn{{color:#9a6700;font-weight:700;white-space:nowrap}}td.bs-no{{color:#cf222e;font-weight:700;white-space:nowrap}}
td.bact{{white-space:nowrap;text-align:right}}
.open{{color:var(--accent);font-weight:700;text-decoration:none;white-space:nowrap}}.open:hover{{text-decoration:underline}}
.split{{color:var(--mut);font-weight:700;text-decoration:none;white-space:nowrap;border:1px solid var(--line);border-radius:999px;padding:2px 8px;margin-right:8px;font-size:12px}}.split:hover{{color:var(--accent);border-color:var(--accent)}}
.build{{color:#a05a00;font-weight:700;font-size:12px}}.empty{{padding:24px;border:1px dashed var(--line);border-radius:12px;color:var(--mut)}}
</style></head><body><main><h1>🏠 {heading}</h1><p class="lead">{label}: {len(cards)} boards discovered{url_note}. This home is a read-only map; each row opens that Board's own Index. Hover a title for the board's spine.</p>{body}</main></body></html>'''


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
