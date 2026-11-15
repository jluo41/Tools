"""The small pieces the insight Board page draws with: the selected cell, the gates, pills, links and tabs, a
question id spelled out, the Board list, and the dataset's facts in one line."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from urllib.parse import quote

from .insight_board_reader import (  # noqa: F401 · this module keeps answering these names
    _TITLE, _LEVEL_LABEL, _read, _e, insight_boards, _pages, _page_link, _parents, _rows, _inline)
from .insight_board_assets import (  # noqa: F401 · this module keeps answering these names
    _CSS)


# ─── the selected cell ──────────────────────────────────────────────────────

def _cell_view(snap: dict, qid: str, pid: str) -> dict:
    row = next((q for q in snap["questions"] if q["id"] == qid), None)
    cell = (row or {}).get("cells", {}).get(pid, {"mark": "·", "page": "", "note": "", "raw": "·"})
    page = snap["by_id"].get(cell.get("page", ""))
    ladder = []
    seen = set()
    frontier = [page] if page else []
    while frontier:
        cur = frontier.pop(0)
        if cur["id"] in seen:
            continue
        seen.add(cur["id"])
        parents = [snap["by_id"][p] for p in _parents(cur["text"]) if p in snap["by_id"] and p != cur["id"]]
        ladder.append({"page": cur, "parents": parents, "rows": _rows(cur["text"])})
        frontier.extend(parents)
    order = {"wisdom": 0, "knowledge": 1, "information": 2, "data": 3}
    ladder.sort(key=lambda item: (order.get(item["page"]["level"], 9), item["page"]["id"]))
    # The primary path: the answer page, its first-cited parent, and so on
    # down to a D page.  Rows are expanded only along this path.
    primary, cur = [], page
    while cur and cur["id"] not in {p["id"] for p in primary}:
        primary.append(cur)
        item = next((it for it in ladder if it["page"]["id"] == cur["id"]), None)
        cur = item["parents"][0] if item and item["parents"] else None
    receipt = next((r for r in snap["runs"] if any(r["page"]["id"] == p["id"] for p in primary)), None) \
        or next((r for r in snap["runs"] if any(r["page"]["id"] == it["page"]["id"] for it in ladder)), None)
    return {"row": row, "cell": cell, "page": page, "ladder": ladder, "primary": primary,
            "receipt": receipt, "gates": _gates(snap, row, pid, cell, page, primary, receipt)}


def _gates(snap, row, pid, cell, page, primary, receipt) -> list[dict]:
    lv = {}
    for p in primary:
        lv.setdefault(p["level"], p)
    meta = snap["by_id"].get("MT00")
    def st(p): return "passed" if p and p["state"].startswith("✅") else ("held" if p else "pending")
    target = (row or {}).get("id", "Q?")[1]
    needed = {"D": 2, "I": 3, "K": 4, "W": 5}.get(target, 5)
    handoff = next((h for h in snap["handoffs"] if page and h["page"] == page["path"]), {})
    signed = bool(handoff.get("signature_current"))
    gates = [
        ("GI0", "Meta ready", st(meta), "automatic", meta["state"] if meta else "no MT00"),
        ("GI1", "Question registered", "passed" if row else "pending", "person",
         f"{row['register']['id']} row" if row else ""),
        ("GI2", "Data observed", st(lv.get("data")), "automatic",
         (receipt and f"{receipt['rel']} · {receipt['status']}") or (lv.get("data") or {}).get("id", "")),
        ("GI3", "Information derived", st(lv.get("information")), "agent", (lv.get("information") or {}).get("id", "")),
        ("GI4", "Knowledge claimed", st(lv.get("knowledge")), "agent", (lv.get("knowledge") or {}).get("id", "")),
        ("GI5", "Wisdom signed", "passed" if signed else ("held" if lv.get("wisdom") else "pending"),
         "person", handoff.get("signature", "") if signed else handoff.get("eligibility_reason", "")),
        ("GI6", "Cell settled", "passed" if cell["mark"] == "✅" else ("held" if cell["mark"] == "🟡" else
                                                                   "refused" if cell["mark"] == "🚫" else "pending"),
         "automatic", cell["raw"]),
    ]
    out = []
    for i, (key, name, state, who, note) in enumerate(gates):
        if i > needed and i < 6:
            state, note = "skipped", f"not needed below {_LEVEL_LABEL[target]}"
        out.append({"key": key, "name": name, "state": state, "who": who, "note": note})
    return out


# ─── render ─────────────────────────────────────────────────────────────────

def _pill(mark: str, text: str = "") -> str:
    cls = {"✅": "ok", "🟡": "warn", "🚫": "bad", "🧊": "acc"}.get(mark, "")
    return f'<span class="pill {cls}">{_e(text or mark)}</span>'


def _clip(text: str, n: int) -> str:
    """Cut at a word boundary, never inside a word ("Gen 1 still car")."""
    if len(text) <= n:
        return text
    return text[:n].rsplit(" ", 1)[0].rstrip(" ·,;") + " …"


def _slug(page: dict) -> str:
    """`MT01-question-data` -> `question-data`: the folder's own name, so an
    id is never shown alone (an id alone tells a reader nothing)."""
    stem = page["path"].stem
    return stem[len(page["id"]) + 1:] if stem.startswith(page["id"] + "-") else ""


def _link(snap: dict, page: dict) -> str:
    slug = _slug(page)
    return (f'<a href="{_e(_page_link(snap, page))}" class="mono">{_e(page["id"])}'
            + (f' <span class=pn>{_e(slug)}</span>' if slug else '') + '</a>')


def _tabs(items: list[tuple[str, str]]) -> str:
    return '<div class="wtabs">' + "".join(
        f'<button class="wtab{" on" if i == 0 else ""}" type="button" data-view="{k}">{_e(v)}</button>'
        for i, (k, v) in enumerate(items)) + "</div>"


def _view(key: str, body: str, on: bool = False) -> str:
    return f'<div class="view{" on" if on else ""}" data-view="{key}">{body}</div>'


def display_id(pid: str, partitions: dict[str, str]) -> str:
    """A page id is already said in words, `I02-full` (no segment
    letters), so the screen shows it as written."""
    return pid


def _spell_ids(snap: dict, page_html: str) -> str:
    """Page ids are words already; nothing to spell (kept for callers)."""
    return page_html


def render_board_list(root: Path, raw: str = "") -> str:
    """The list of every InsightBoard under the server root, with page counts."""
    rows = []
    for board in insight_boards(root):
        pages = _pages(board)
        settled = sum(p["state"].startswith("✅") for p in pages)
        title = _TITLE.search(_read(board / "board.md"))
        rows.append(f'<tr><td><a href="/_board/insight-board?board={quote(board.name)}" class=mono>{_e(board.name)}</a></td>'
                    f'<td>{_e(title.group(1).strip() if title else "")}</td><td class=num>{len(pages)}</td><td class=num>{settled}</td>'
                    f'<td class=mono>{_e(board.relative_to(root).as_posix())}</td></tr>')
    note = (f'<p class=note>This link does not name a Board (got <code>{_e(raw)}</code>). Pick one below.</p>' if raw else "")
    body = "".join(rows) or '<tr><td colspan=5 class=mut>No InsightBoard found under this root.</td></tr>'
    return ('<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'
            f'<title>🔎 Insight Boards</title><style>{_CSS}</style></head><body><main>'
            f'<header><h1>🔎 Insight Boards</h1></header>{note}'
            f'<div class=shell><table><tr><th>Board</th><th>Title</th><th>Pages</th><th>Settled</th><th>Folder</th></tr>{body}</table></div>'
            '</main></body></html>')


_HEADS = ("midlife", "young", "older", "old", "senior", "adult", "child", "teen")


def _pretty(name: str) -> str:
    """`youngmale` -> `young male`, `midlifemale` -> `midlife male`: MT00
    keeps one token per segment, the screen keeps the words apart.  A known
    age word is split first (so `midlifemale` is not read as `midli female`);
    any other token is shown as written."""
    for head in _HEADS:
        tail = name[len(head):]
        if name.startswith(head) and tail in ("", "male", "female"):
            return f"{head} {tail}".strip()
    return re.sub(r"(?<=[a-z])(fe)?male$", lambda m: " " + m.group(0), name)


def _partition_name(snap: dict, pid: str) -> str:
    row = next((p for p in snap["partitions"] if p["id"] == pid), None)
    return _pretty(row["name"]) if row else ""


_GRAIN = re.compile(r"One row is one [^.]+\.")
_SHAPE = re.compile(r"([\d,]{5,})\s*[×x]\s*(\d{1,4})\b")
_WINDOW = re.compile(r"(\d{4}-\d{2}-\d{2})\s+to\s+(\d{4}-\d{2}-\d{2})")
_VARIANTS = re.compile(r"((?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen))\s+message variants", re.I)
_ROWS = re.compile(r"([\d,]{5,})\s+(?:messaged|patient|message)\s+rows", re.I)
_SIDECARS = ("data_dictionary.csv", "manifest.json", "Message-Content.md")


def _input_facts(snap: dict) -> list[tuple[str, str]]:
    """What the board reads, from MT00 and board.md: the one prepared extract,
    its grain, its window and the files beside it.  A fact with no sentence on
    either page is left out rather than guessed."""
    meta = next((p for p in snap["pages"] if p["id"] == "MT00"), None)
    meta_text = meta["text"] if meta else ""
    text = meta_text + "\n" + _read(snap["board"] / "board.md")
    facts: list[tuple[str, str]] = []
    lines = text.splitlines()
    file_line = next((i for i, line in enumerate(lines)
                      if ".parquet" in line and "..." not in line), None)
    if file_line is not None:
        name = re.search(r"(\S+\.parquet)", lines[file_line]).group(1)
        folder = next((lines[i].strip() for i in range(file_line - 1, -1, -1)
                       if re.fullmatch(r"\S+/", lines[i].strip())), "")
        shape = _SHAPE.search(lines[file_line])
        where = f'<code>{_e(folder)}</code><br><code>{_e(name.split("/")[-1])}</code>' if folder \
            else f'<code>{_e(name)}</code>'
        facts.append(("extract", where + (f' · {shape.group(1)} rows × {shape.group(2)} columns'
                                          if shape else "")))
    grain = _GRAIN.search(text)
    if grain:
        facts.append(("one row", _inline(grain.group(0).rstrip("."))))
    window = _WINDOW.search(text)
    rows = _ROWS.search(text)
    if window:
        facts.append(("window", f'{window.group(1)} to {window.group(2)}'
                      + (f' · {rows.group(1)} rows' if rows else "")))
    variants = _VARIANTS.search(text)
    if variants:
        facts.append(("what varies", f'{variants.group(1)} message variants'))
    beside = [name for name in _SIDECARS if name in text]
    if beside:
        facts.append(("beside it", " · ".join(f'<code>{_e(name)}</code>' for name in beside)))
    if meta:
        facts.append(("described by", _link(snap, meta) + ' <span class=mut>· sources, grain, population, freshness, limits</span>'))
    facts.append(("results store", f'<code>{_e(snap["store"] or "not declared on board.md")}</code>'))
    return facts


def _render_input_data(snap: dict) -> str:
    """Scope Space · Data: the one input every page on this board cites."""
    facts = _input_facts(snap)
    body = "".join(f'<tr><td>{_e(label)}</td><td>{value}</td></tr>' for label, value in facts)
    return ('<h2>Dataset</h2><p class=lead>The one prepared extract this workbench reads. '
            'The board reads it and never owns or changes it, and no page may cite a number that is not in it.</p>'
            f'<table class="rows inputs">{body}</table>')


_TICKET_TARGET = re.compile(r'tasks/([^"\s]+?)/runs/([^/"\s]+)\.sh')


_WORDS = {w: str(i) for i, w in enumerate(("zero one two three four five six seven eight nine ten eleven "
                                            "twelve thirteen fourteen fifteen").split())}


def _short_window(a: str, b: str) -> str:
    """`2025-06-16`, `2025-07-03` -> `Jun 16 – Jul 3, 2025`."""
    d1, d2 = date.fromisoformat(a), date.fromisoformat(b)
    left = f"{d1:%b} {d1.day}" + ("" if d1.year == d2.year else f", {d1.year}")
    return f"{left} – {d2:%b} {d2.day}, {d2.year}"


def _dataset_line(snap: dict) -> tuple[str, str]:
    """(short line, full extract name), e.g. `SMSR2v1 · 444,691 rows · 13 messages · Jun 16 – Jul 3, 2025`;
    only the full name is used now (the banner above the Spaces was removed)."""
    meta = snap["by_id"].get("MT00")
    text = (meta["text"] if meta else "") + "\n" + _read(snap["board"] / "board.md")
    name = re.search(r"(?m)^extract\s+(\S+)", text) or re.search(r"([\w.-]+)\.parquet", text)
    full = name.group(1) if name else snap["board"].name
    short = re.match(r"^\d{8}_([A-Za-z0-9]+)", full)          # 20250616_SMSR2v1_min_… -> SMSR2v1
    rows, window, variants = _ROWS.search(text), _WINDOW.search(text), _VARIANTS.search(text)
    bits = [short.group(1) if short else full]
    if rows:
        bits.append(f"{rows.group(1)} rows")
    if variants:
        bits.append(f"{_WORDS.get(variants.group(1).lower(), variants.group(1))} messages")
    if window:
        bits.append(_short_window(window.group(1), window.group(2)))
    return " · ".join(bits), full
