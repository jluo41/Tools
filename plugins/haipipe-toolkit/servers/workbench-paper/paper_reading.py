"""What the Story's § 6 Discovery Roadmap says the paper must read, one line per D row, shown in the Story view (JL
261111, Paper-CMS-AI-Usage r03_collect_plan_view_decisions: Reading belongs to the Story, which owns § 6; the Plan view
is s03 and s04 only). Also two small readers the Structure view shares: every Markdown table of a part, and the rule
that a template slot (`<…>`) is not content. Read-only, nothing copied.
"""
from __future__ import annotations

import re
from pathlib import Path

from live.frame import esc
from live.ui_parts import _plain
from live.board_read import _face, view_topics

READ_CSS = ("<style>.pp-read{list-style:none;margin:0;padding:0;font-size:14px}.pp-read li{margin:0 0 6px}"
            ".pp-read .mut{color:var(--muted)}</style>")


def _tables(body: str) -> list:
    """Every Markdown table in `body`, each a list of row dicts keyed by its lower-case header."""
    out, block = [], []
    for line in body.splitlines() + [""]:
        if line.strip().startswith("|"):
            block.append(line)
            continue
        if len(block) >= 3:
            cells = lambda r: [c.strip() for c in r.strip().strip("|").split("|")]
            head = [h.lower() for h in cells(block[0])]
            out.append([dict(zip(head, cells(r))) for r in block[2:]])
        block = []
    return out


def _rows(body: str, key: str) -> dict:
    """{id: row} from the first table whose first header is `key` (D in § 6)."""
    for t in _tables(body):
        if t and next(iter(t[0])) == key:
            return {_plain(r[key]): r for r in t if _plain(r.get(key, ""))}
    return {}


def drop_slots(html: str) -> str:
    """A list item or table cell that is only a template slot (`<a decision made while planning>`) is not content."""
    empty = lambda s: not re.sub(r"[\W_]+", "", re.sub(r"&lt;.*?&gt;|<[^>]+>", "", s))
    html = re.sub(r"<li>((?:(?!</?li\b).)*?)</li>", lambda m: "" if "&lt;" in m.group(1) and empty(m.group(1)) else m.group(0), html, flags=re.S)
    return re.sub(r"(<td[^>]*>)((?:(?!</td>).)*?)(</td>)",
                  lambda m: m.group(1) + m.group(3) if "&lt;" in m.group(2) and empty(m.group(2)) else m.group(0), html, flags=re.S)


def reading_list(board: Path) -> tuple:
    """(html, word) of the Story's § 6 D rows, one line each: name · its folder or none yet · what it feeds."""
    story = next((t for k, _, t in view_topics(board, "story") if k != "idea"), None)
    if story is None:
        return "", ""
    rows = _rows(_face(story)[1].get("discovery roadmap", ""), "d")
    if not rows:
        return "", ""
    items, done = "", 0
    for i, r in rows.items():
        folder = _plain(r.get("folder", ""))
        none = not folder or folder.lower().startswith(("none", "—", "-"))
        done += not none
        feeds = _plain(r.get("feeds rq/e/section", "") or r.get("feeds", ""))
        items += (f'<li>{esc(_plain(r.get("name", "")) or i)} · '
                  + ('<span class=mut>⬜ none yet</span>' if none else f'📁 {esc(folder)}')
                  + (f' · feeds {esc(feeds)}' if feeds else "") + '</li>')
    return READ_CSS + f'<ul class=pp-read>{items}</ul>', ("none started" if not done else "")
