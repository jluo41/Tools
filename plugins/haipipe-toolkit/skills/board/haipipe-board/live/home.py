"""The read-only SPACE-level Board Home.

This is deliberately not a Board: no board.md, no chat, no durable state.  It
discovers the Board folders already present below the server root and gives the
reader one stable place from which to enter them.
"""

from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import quote, urlsplit

from src.common import page_files


SKIP_PARTS = {".git", ".venv", "node_modules", "__pycache__", "_archive", "board"}
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


def discover_boards(root: Path) -> list[dict[str, object]]:
    """Read lightweight metadata from every real Board source folder."""
    root = root.resolve()
    cards = []
    for manifest in root.rglob("board.md"):
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
                      "href": "/" + quote((board.relative_to(root) / "board" / "index.html").as_posix(), safe="/")})
    return sorted(cards, key=lambda c: str(c["path"]).lower())


def render_home(root: Path) -> str:
    cards = discover_boards(root)
    sections = []
    for kind, icon in BOARD_KINDS:
        kind_cards = [card for card in cards if card["kind"] == kind]
        if not kind_cards:
            continue
        items = []
        for card in kind_cards:
            title = html.escape(str(card["title"]))
            spine = html.escape(str(card["spine"]))
            path = html.escape(str(card["path"]))
            progress = f'{card["settled"]}/{card["pages"]} pages settled'
            if card["ready"]:
                action = f'<a class="open" href="{html.escape(str(card["href"]), quote=True)}">Open board →</a>'
            else:
                action = '<span class="build">Build needed</span>'
            items.append(f'''<article class="card"><p class="path">{path}</p><h2>{title}</h2>
<p class="spine">{spine}</p><footer><span>{progress}</span><span class="kind">{icon} {kind}</span>{action}</footer></article>''')
        plural = f"{kind}s"
        cards_html = "\n".join(items)
        sections.append(f'''<section class="board-kind"><header><h2>{icon} {plural}</h2><span>{len(kind_cards)}</span></header>
<div class="grid">{cards_html}</div></section>''')
    body = "\n".join(sections) or '<p class="empty">No board.md files found below this SPACE root.</p>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>SPACE Boards</title><style>
:root{{color-scheme:light;--ink:#202124;--mut:#6b7280;--line:#e5e7eb;--bg:#fafafa;--card:#fff;--accent:#2867b2}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
main{{max-width:1060px;margin:0 auto;padding:clamp(22px,5vw,56px) clamp(16px,4vw,36px)}}
h1{{font-size:clamp(28px,5vw,46px);letter-spacing:-.04em;margin:0 0 6px}}.lead{{margin:0 0 28px;color:var(--mut)}}
.board-kind{{margin:32px 0 0}}.board-kind>header{{display:flex;align-items:center;justify-content:space-between;margin:0 0 12px}}.board-kind>header h2{{margin:0;font-size:20px;letter-spacing:-.02em}}.board-kind>header span{{border:1px solid var(--line);border-radius:999px;padding:2px 9px;color:var(--mut);font-size:12px;font-weight:700}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}}.card{{display:flex;min-height:210px;flex-direction:column;padding:18px;border:1px solid var(--line);border-radius:16px;background:var(--card);box-shadow:0 1px 2px #00000008}}
.path{{margin:0;color:var(--mut);font:12px ui-monospace,SFMono-Regular,Menlo,monospace;overflow-wrap:anywhere}}.card h2{{font-size:18px;line-height:1.25;margin:12px 0 8px}}.spine{{margin:0;color:#40444b;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}}footer{{display:flex;align-items:center;justify-content:flex-start;flex-wrap:wrap;gap:8px;margin-top:auto;padding-top:18px;color:var(--mut);font-size:12px}}.kind{{border-radius:999px;background:#f3f4f6;padding:3px 7px;white-space:nowrap}}.open{{color:var(--accent);font-weight:700;text-decoration:none;white-space:nowrap;margin-left:auto}}.open:hover{{text-decoration:underline}}.build{{color:#a05a00;font-weight:700}}.empty{{padding:24px;border:1px dashed var(--line);border-radius:12px;color:var(--mut)}}
</style></head><body><main><h1>🏠 SPACE Boards</h1><p class="lead">{len(cards)} boards discovered in this SPACE. This home is a read-only map; each card opens that Board's own Index.</p><section class="grid">{body}</section></main></body></html>'''


class HomeMixin:
    def serve_home(self):
        body = render_home(self.root).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def is_home_request(self):
        return urlsplit(self.path).path.rstrip("/") == "/boards"
