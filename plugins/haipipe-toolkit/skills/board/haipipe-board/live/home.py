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
    """Render a compact, mobile-first directory for the boards in one SPACE."""
    cards = discover_boards(root)
    sections = []
    settled_total = sum(int(card["settled"]) for card in cards)
    page_total = sum(int(card["pages"]) for card in cards)
    ready_total = sum(bool(card["ready"]) for card in cards)
    for kind, icon in BOARD_KINDS:
        kind_cards = [card for card in cards if card["kind"] == kind]
        if not kind_cards:
            continue
        board_cards = []
        for card in kind_cards:
            title = html.escape(str(card["title"]))
            spine = html.escape(str(card["spine"]), quote=True)
            path = html.escape(str(card["path"]))
            slug = html.escape(str(card["slug"]))
            href = html.escape(str(card["href"]), quote=True)
            search = html.escape(
                " ".join((str(card["title"]), str(card["slug"]),
                          str(card["path"]), str(card["spine"]), kind)),
                quote=True,
            )
            pages, settled = int(card["pages"]), int(card["settled"])
            if card["ready"]:
                complete = bool(pages and settled == pages)
                status_class = "ready" if complete else "active"
                status_label = "Settled" if complete else "Active"
                # Two doors, because they are two different jobs: reading the
                # board is one document, OPERATING it (QD5) is three panes with
                # a chat beside the page. Same board either way.
                # The split is what a board opens as now, so it is the plain
                # link; `?plain` is the opt-out back to the one-document board.
                action = (f'<a class="primary" href="{href}">Open board <span aria-hidden="true">↗</span></a>'
                          f'<a class="secondary" href="{href}?plain"'
                          f' title="Open the one-document board">Plain</a>')
            else:
                status_class = "build"
                status_label = "Needs build"
                action = '<span class="build-note">Build needed</span>'
            page_label = f"{settled}/{pages} settled" if pages else "No pages yet"
            actions = f'<div class="actions">{action}</div>'
            board_cards.append(
                f'''<article class="board-row" data-search="{search}">
  <div class="row-main"><div class="row-kicker"><span class="kind">{icon} {kind}</span></div>
  <h3><a href="{href}" title="{spine}">{title}</a></h3>
  <p class="board-id">/{slug}</p>
  </div>
  <div class="row-status"><span class="status {status_class}"><span class="dot" aria-hidden="true"></span>{status_label}</span></div>
  <div class="row-pages"><span class="meta-label">Pages</span><strong>{page_label}</strong></div>
  <div class="row-path"><span class="meta-label">Path</span><span class="path" title="{path}">{path}</span></div>
  {actions}
</article>''')
        sections.append(
            f'''<section class="board-group" data-group>
  <div class="group-head"><h2>{icon} {html.escape(kind)}s</h2><span>{len(kind_cards)}</span></div>
  <div class="board-list">{"".join(board_cards)}</div>
</section>''')
    body = ("\n".join(sections) if sections else
            '<p class="empty">No board.md files found below this SPACE root.</p>')
    label = html.escape(space_name.strip() or "SPACE")
    heading = html.escape(f"JJ-LUO / {space_name.strip()} Boards" if space_name.strip() else "SPACE Boards")
    public = html.escape(public_url.strip(), quote=True)
    url_note = (f'<a href="{public}">{public}</a>' if public else "")
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{heading}</title><style>
:root{{color-scheme:light;--ink:#17212b;--mut:#667085;--line:#d9e0e7;--bg:#f4f6f8;--surface:#fff;--accent:#0f6b78;--accent-soft:#e5f3f2;--green:#176b42;--green-soft:#e8f5ed;--amber:#9a5b00;--amber-soft:#fff4dc;--red:#b42318}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
main{{max-width:1120px;margin:0 auto;padding:30px 22px 52px}}
.eyebrow{{color:var(--accent);font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase}}
h1{{font-size:36px;line-height:1.12;letter-spacing:0;margin:6px 0 8px}}.header-meta{{display:flex;gap:12px;align-items:center;color:var(--mut);font-size:13px;flex-wrap:wrap}}.header-meta a{{color:var(--accent);text-decoration:none}}.header-meta a:hover{{text-decoration:underline}}
.toolbar{{display:flex;align-items:center;justify-content:space-between;gap:14px;margin:28px 0 14px}}.search{{display:flex;align-items:center;gap:8px;flex:1;max-width:460px;color:var(--mut)}}.search input{{width:100%;min-height:42px;border:1px solid var(--line);border-radius:7px;background:var(--surface);color:var(--ink);font:inherit;padding:9px 12px;outline:none}}.search input:focus{{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}}.filter-count{{color:var(--mut);font-size:13px;white-space:nowrap}}
.summary{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-bottom:30px}}.metric{{border:1px solid var(--line);border-radius:8px;background:var(--surface);padding:13px 15px}}.metric strong{{display:block;font-size:24px;line-height:1.15}}.metric span{{display:block;color:var(--mut);font-size:12px;margin-top:3px}}
.board-group{{margin:0 0 28px}}.group-head{{display:flex;align-items:center;gap:9px;margin:0 0 10px}}.group-head h2{{font-size:15px;line-height:1.2;margin:0;font-weight:800}}.group-head span{{min-width:25px;border-radius:999px;background:#e7ebef;color:var(--mut);font-size:12px;font-weight:800;text-align:center;padding:2px 7px}}
.board-list{{display:grid;gap:8px}}.board-row{{display:grid;grid-template-columns:minmax(0,2.5fr) minmax(90px,auto) minmax(105px,auto) minmax(0,1.5fr) auto;align-items:center;column-gap:18px;min-width:0;border:1px solid var(--line);border-radius:8px;background:var(--surface);padding:13px 16px;box-shadow:0 1px 2px #1822300b}}.board-row:hover{{border-color:#b8c7d1;box-shadow:0 4px 14px #18223012}}.row-main,.row-path{{min-width:0}}.row-kicker{{display:flex;align-items:center;min-width:0}}.kind{{color:var(--mut);font-size:12px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}.status{{display:inline-flex;align-items:center;gap:5px;border-radius:999px;font-size:11px;font-weight:800;padding:3px 8px;white-space:nowrap}}.dot{{width:7px;height:7px;border-radius:50%;background:currentColor}}.status.ready{{color:var(--green);background:var(--green-soft)}}.status.active{{color:var(--amber);background:var(--amber-soft)}}.status.build{{color:var(--red);background:#fef0ef}}
.board-row h3{{font-size:16px;line-height:1.25;margin:5px 0 2px;overflow-wrap:anywhere}}.board-row h3 a{{color:var(--ink);text-decoration:none}}.board-row h3 a:hover{{color:var(--accent)}}.board-id{{margin:0;color:var(--accent);font:12px ui-monospace,SFMono-Regular,Menlo,monospace;overflow-wrap:anywhere}}.meta-label{{display:block;color:var(--mut);font-size:10px;font-weight:800;letter-spacing:.04em;text-transform:uppercase}}.row-pages{{min-width:0;color:var(--mut);font-size:12px}}.row-pages strong{{display:block;color:var(--ink);font-size:13px;line-height:1.25;margin-top:2px;white-space:nowrap}}.row-path{{color:var(--mut);font-size:12px}}.row-path .path{{display:block;min-width:0;margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font:11px ui-monospace,SFMono-Regular,Menlo,monospace}}.row-status{{justify-self:start}}.actions{{display:flex;align-items:center;justify-content:flex-end;gap:8px;min-width:0;margin-top:0;white-space:nowrap}}.primary,.secondary{{display:inline-flex;align-items:center;justify-content:center;min-height:34px;border-radius:6px;padding:6px 10px;font-size:13px;font-weight:800;text-decoration:none}}.primary{{background:var(--accent);color:#fff}}.primary:hover{{background:#0a5661}}.secondary{{border:1px solid var(--line);color:var(--mut);background:var(--surface)}}.secondary:hover{{border-color:var(--accent);color:var(--accent)}}.build-note{{color:var(--red);font-size:12px;font-weight:800}}.empty,.no-results{{border:1px dashed var(--line);border-radius:8px;background:var(--surface);color:var(--mut);padding:22px}}[hidden]{{display:none!important}}
@media (max-width:980px){{.board-row{{grid-template-columns:minmax(0,1fr) minmax(100px,auto) minmax(105px,auto);row-gap:10px}}.row-main{{grid-column:1 / 4}}.row-status{{grid-column:2;grid-row:2}}.row-pages{{grid-column:3;grid-row:2}}.row-path{{grid-column:1 / 4;grid-row:3}}.actions{{grid-column:1 / 4;grid-row:4;justify-content:flex-start}}}}
@media (max-width:680px){{main{{padding:22px 14px 38px}}h1{{font-size:28px}}.toolbar{{align-items:stretch;flex-direction:column;margin-top:22px}}.search{{max-width:none}}.filter-count{{font-size:12px}}.summary{{gap:7px;margin-bottom:26px}}.metric{{padding:11px 10px}}.metric strong{{font-size:20px}}.metric span{{font-size:11px}}.board-row{{grid-template-columns:minmax(0,1fr) auto;padding:13px 14px;row-gap:9px}}.row-main{{grid-column:1;grid-row:1}}.row-status{{grid-column:2;grid-row:1}}.row-pages{{grid-column:1;grid-row:2}}.row-path{{grid-column:1 / 3;grid-row:3}}.actions{{grid-column:1 / 3;grid-row:4}}.board-row h3{{font-size:17px}}}}
</style></head><body><main><header class="site-head"><div class="eyebrow">JJ-LUO · Private Space</div><h1>🏠 {heading}</h1><div class="header-meta"><span>{label} board directory</span>{f'<span aria-hidden="true">·</span>{url_note}' if url_note else ''}</div></header>
<div class="toolbar"><label class="search"><span aria-hidden="true">⌕</span><input id="board-filter" type="search" placeholder="Filter boards" aria-label="Filter boards" autocomplete="off"></label><span class="filter-count" id="filter-count">{len(cards)} boards</span></div>
<section class="summary" aria-label="Board summary"><div class="metric"><strong>{len(cards)}</strong><span>Total boards</span></div><div class="metric"><strong>{ready_total}</strong><span>Ready to open</span></div><div class="metric"><strong>{settled_total}/{page_total}</strong><span>Pages settled</span></div></section>
<div id="board-groups">{body}</div><p id="no-results" class="no-results" hidden>No matching boards.</p></main><script>
const filter = document.getElementById('board-filter');
const count = document.getElementById('filter-count');
const noResults = document.getElementById('no-results');
const cards = Array.from(document.querySelectorAll('.board-row'));
const groups = Array.from(document.querySelectorAll('[data-group]'));
function applyFilter() {{
  const query = filter.value.trim().toLowerCase();
  let visible = 0;
  cards.forEach((card) => {{
    const match = !query || card.dataset.search.toLowerCase().includes(query);
    card.hidden = !match;
    if (match) visible += 1;
  }});
  groups.forEach((group) => {{ group.hidden = !group.querySelector('.board-row:not([hidden])'); }});
  count.textContent = query ? visible + ' matching' : cards.length + ' boards';
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
