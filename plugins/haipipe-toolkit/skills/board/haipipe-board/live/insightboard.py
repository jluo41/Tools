"""🔎 Insight Board · one selected cell, five Spaces, nothing invented.

A cell is one register question on one partition (``QW1 × F``).  Every Space
reads the same selected cell: Scope shows the register it sits in, Run shows
the receipts behind it, Insight shows the page that answers it, Evidence shows
the chain down to the extract, Check shows its seven gates.

The board on disk stays authoritative.  This module only reads: the four
register pages (their ASCII cell grids), every answering page (its header,
Opening, rows, citations and ``## Log``), and the ``runtime.yaml`` receipts a
D page names in the store.
"""

from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse


_TITLE = re.compile(r"(?m)^#\s+(.+?)\s*$")
_INSIGHT_BOARD = re.compile(r"(?:^|[-_])insightboard(?:$|[-_])", re.I)
_LEVELS = ("data", "information", "knowledge", "wisdom")
_LEVEL_OF = {"D": "data", "I": "information", "K": "knowledge", "W": "wisdom"}
_LEVEL_LABEL = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}
_SKIP = {"board", "_archive", "__pycache__", ".git", "probe", "display"}
_PAGE_ID = re.compile(r"\b([A-Z][DIKW]\d{2})\b")
_QID = re.compile(r"\b(Q[DIKW]\d+)\b")
_MARK = re.compile(r"(✅|🟡|🚫|⬜|🧊)")
_LOG_LINE = re.compile(r"(?m)^(\d{6}) · (.+?)\s*$")
_SERVES = re.compile(r"(?im)^\s*SERVES\b")
_SIGNED = re.compile(r"(?im)^\s*signed:\s*✅\s*(.+?)\s*$")
_CACHE: dict[str, tuple[float, dict]] = {}


# ─── small readers ──────────────────────────────────────────────────────────

def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _e(value) -> str:
    return html.escape(str(value or ""), quote=True)


def _header(text: str) -> dict[str, str]:
    """`key: value` lines between the title and the first `## ` heading."""
    fields = {}
    for line in text.splitlines():
        if line.startswith("## "):
            break
        m = re.match(r"^([a-z][a-z-]*):\s*(.*?)\s*$", line)
        if m:
            fields.setdefault(m.group(1).lower(), m.group(2).strip("'\""))
    return fields


def _field(text: str, name: str) -> str:
    return _header(text).get(name.lower(), "")


def _section(text: str, title: str) -> str:
    """Body of the first heading whose text matches `title` (any level)."""
    m = re.search(rf"(?ms)^#{{2,4}}\s+(?:\d+\s+·\s+)?{re.escape(title)}\s*$\n(.*?)(?=^#{{2,4}}\s|\Z)", text)
    return m.group(1) if m else ""


# ─── board identity ─────────────────────────────────────────────────────────

def is_insight_board(board_root: Path) -> bool:
    board_root = Path(board_root)
    declared = _field(_read(board_root / "board.md"), "board-kind").lower()
    return declared in {"insight", "insight-board"} \
        or bool(_INSIGHT_BOARD.search(board_root.name)) \
        or (board_root / "0-MT-meta").is_dir()


def _safe_board(root: Path, raw: str) -> Path | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    value = unquote(raw).split("?", 1)[0].split("#", 1)[0]
    try:
        resolved = (root / value.lstrip("/")).resolve()
        resolved.relative_to(root.resolve())
    except (OSError, ValueError, RuntimeError):
        return None
    if resolved.is_file() and resolved.name == "board.md":
        resolved = resolved.parent
    return resolved if (resolved / "board.md").is_file() else None


_BOARD_GLOBS = ("examples*/*/applications/*/board.md", "examples*/*/*/board.md")


def insight_boards(root: Path) -> list[Path]:
    found = {}
    for pattern in _BOARD_GLOBS:
        for board_md in Path(root).glob(pattern):
            if is_insight_board(board_md.parent):
                found.setdefault(board_md.parent.name, board_md.parent)
    return [found[name] for name in sorted(found)]


def _board_by_name(root: Path, name: str) -> Path | None:
    name = unquote(name or "").strip().strip("/")
    if not name or "/" in name:
        return None
    boards = insight_boards(root)
    matches = [b for b in boards if b.name == name]
    if not matches:
        # A short or cut name still lands (JL 260917: a terminal wraps a long
        # link and drops its tail).  `A00`, or any unique leading piece of the
        # folder name, names the board; an ambiguous piece names none.
        matches = [b for b in boards if b.name.lower().startswith(name.lower())]
    return matches[0] if len(matches) == 1 else None


# ─── pages ──────────────────────────────────────────────────────────────────

def _pages(board_root: Path) -> list[dict]:
    pages = []
    for path in sorted(board_root.rglob("*.md")):
        rel = path.relative_to(board_root)
        if path.name == "board.md" or any(part in _SKIP for part in rel.parts):
            continue
        if path.name != f"{path.parent.name}.md":
            continue
        text = _read(path)
        head = _header(text)
        stem = path.stem.split("-", 1)[0].upper()
        m = re.match(r"^([A-Z]?)([DIKW])\d{2}$", stem)
        part = next((re.match(r"^\d+-([A-Z])-", p).group(1) for p in rel.parts
                     if re.match(r"^\d+-([A-Z])-", p)), "")
        pages.append({
            "path": path, "rel": rel.as_posix(), "id": stem, "text": text,
            "title": (_TITLE.search(text).group(1).strip() if _TITLE.search(text) else path.stem),
            "state": head.get("state", "OPEN"), "page_type": head.get("page-type", ""),
            "rung": head.get("question-rung", "").lower(),
            "level": _LEVEL_OF.get(m.group(2)) if m else "", "partition": part,
            "receipt_field": head.get("receipt", ""),
        })
    return pages


def _page_link(snapshot: dict, page: dict) -> str:
    """The generated HTML twin when it exists, else the source Markdown."""
    stem = page["path"].stem
    letter = page["partition"] or "MT"
    generated = snapshot["board"] / "board" / letter / f"{stem}.html"
    if snapshot["static"]:
        return f"{letter}/{stem}.html" if generated.is_file() else f"../{page['rel']}"
    if generated.is_file():
        return "/" + quote(f"{snapshot['relative']}/board/{letter}/{stem}.html", safe="/")
    return "/" + quote(f"{snapshot['relative']}/{page['rel']}", safe="/")


# ─── registers: the ASCII cell grid inside each MT page ─────────────────────

def _grid_lines(text: str) -> list[str]:
    """Lines of the first fenced block that carries a `Q?N` row."""
    for block in re.findall(r"(?ms)^```\w*\n(.*?)^```", text):
        if re.search(r"(?m)^Q[DIKW]\d+\s", block):
            return block.splitlines()
    return []


# A cell is `✅ FI01`, `🟡 BI03 final`, `🚫 thin`, `🚫 F-only` or a lone `·`.
# Cells are read as an ordered token stream, never by character offset: an
# emoji is one code point but two columns wide, so offsets drift per cell.
_CELL_TOKEN = re.compile(r"(?:[✅🟡🚫⬜🧊]\s+[^\s·]+(?:\s+(?:final|defers))?|(?<!\S)·(?!\S))")


def _cell_tokens(text: str) -> list[dict]:
    return [_parse_cell(m.group(0)) for m in _CELL_TOKEN.finditer(text)]


def _parse_register(page: dict, partitions: list[str]) -> list[dict]:
    lines = _grid_lines(page["text"])
    if not lines:
        return []
    header = next((l for l in lines if re.match(r"^id\s", l)), "")
    cols = re.findall(r"\b([A-Z])·[a-z]+", header)
    if re.search(r"\bX\s*$", header):
        cols.append("X")
    if "partition" in header and _QID.search(header):
        return _parse_transposed(lines, header, page)
    rows, current = [], None
    for line in lines:
        m = re.match(r"^(Q[DIKW]\d+)\s+(.*)$", line)
        if m:
            qid, rest = m.groups()
            question = re.split(r"\s{2,}", rest, maxsplit=1)[0].strip()
            current = {"id": qid, "question": question, "register": page, "cells": {}}
            rows.append(current)
            tokens = _cell_tokens(rest[len(question):])
            for i, pid in enumerate(cols):
                current["cells"][pid] = tokens[i] if i < len(tokens) else _parse_cell("·")
        elif current and re.match(r"^\s{4,}\S", line) and not _MARK.search(line) \
                and not line.strip().startswith("─"):
            # a wrapped question continues on an indented line without an id
            current["question"] = (current["question"] + " " + line.strip()).strip()
        elif not line.startswith(" ") and line.strip() and not re.match(r"^(id\s|─)", line):
            current = None  # legend or prose: stop appending
    return rows


def _parse_transposed(lines: list[str], header: str, page: dict) -> list[dict]:
    """MT04 style: one row per partition, one column per question id."""
    qcols = _QID.findall(header)
    rows = {qid: {"id": qid, "question": "", "register": page, "cells": {}} for qid in qcols}
    current = None
    for line in lines:
        m = re.match(r"^(Q[DIKW]\d+)\s+(.*?)\s{2,}", line)
        if m and m.group(1) in rows:
            current = rows[m.group(1)]
            current["question"] = m.group(2).strip()
        elif current and re.match(r"^\s{6}\S", line) and not _MARK.search(line[:40]):
            wrapped = re.split(r"\s{2,}", line.strip(), maxsplit=1)[0]
            if wrapped and not re.match(r"^[A-Z] · ", wrapped):
                current["question"] = (current["question"] + " " + wrapped).strip()
        pm = re.search(r"\b([A-Z]) · [a-z]+\s+(.*)$", line)
        if pm:
            tokens = _cell_tokens(pm.group(2))
            for i, qid in enumerate(qcols):
                rows[qid]["cells"][pm.group(1)] = tokens[i] if i < len(tokens) else _parse_cell("·")
    return [rows[qid] for qid in qcols]


def _parse_cell(raw: str) -> dict:
    raw = raw.strip()
    m = _MARK.match(raw)
    if not m:
        return {"mark": "·", "page": "", "note": "", "raw": "·"}
    rest = raw[m.end():].strip()
    pm = _PAGE_ID.match(rest)
    page = pm.group(1) if pm else ""
    note = rest[pm.end():].strip() if pm else rest
    return {"mark": m.group(1), "page": page, "note": note, "raw": raw}


# ─── receipts, logs, citations ──────────────────────────────────────────────

def _yaml_flat(text: str) -> dict[str, str]:
    out = {}
    for line in text.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", line)
        if m:
            out[m.group(1)] = m.group(2).strip('"')
    return out


def _receipts(pages: list[dict], store: Path | None) -> list[dict]:
    """Every `run receipt` a page names, resolved in the store and read."""
    runs, seen = [], set()
    for page in pages:
        text = page["text"]
        # A page names one receipt on a `run receipt` line, or several under
        # `run receipts` (XD01 binds six calls of one task): every
        # `results/<call>/runtime.yaml` the page names is a run of its own.
        rels = [page["receipt_field"]] if page["receipt_field"] else []
        if re.search(r"(?m)^run receipts?\s+\S+runtime\.yaml", text):
            rels += re.findall(r"(?<![\w/])(results/[^/\s]+/runtime\.yaml)", text)
        rels = list(dict.fromkeys(r for r in rels if r))
        if not rels:
            continue
        # The task folder comes from the QA path under `📥 Input files`, which is
        # the one place the page names the store path exactly as it is on disk.
        store_name = re.escape(store.name) if store is not None else r"[^/\s]+Result"
        task = (re.search(rf"{store_name}/([^/\s]+/[^/\s`]+)/QA/", text)
                or re.search(rf"{store_name}/([^/\s]+/[^/\s`]+)/", text))
        for rel in rels:
            _receipt_row(runs, seen, page, rel, task, store)
    return runs


def _receipt_row(runs: list, seen: set, page: dict, rel: str, task, store: Path | None) -> None:
    if True:
        candidates = []
        if store is not None:
            if task:
                candidates.append(store / task.group(1) / rel)
            candidates.append(store / rel)
        path = next((c for c in candidates if c.is_file()), None)
        key = str(path or rel) + page["id"]
        if key in seen:
            return
        seen.add(key)
        fields = _yaml_flat(_read(path)) if path else {}
        runs.append({
            "page": page, "rel": rel, "path": path, "found": path is not None,
            "task": fields.get("task") or (task.group(1) if task else ""),
            "call": fields.get("call", ""), "status": fields.get("status", "missing"),
            "started": fields.get("started", ""), "duration": fields.get("duration_s", ""),
            "git": fields.get("git_sha", ""), "cmd": fields.get("cmd", ""),
        })


def _log_events(pages: list[dict]) -> list[dict]:
    events = []
    for page in pages:
        for date, line in _LOG_LINE.findall(_section(page["text"], "Log")):
            events.append({"date": date, "page": page, "text": line})
    events.sort(key=lambda ev: ev["date"], reverse=True)
    return events


def _parents(text: str) -> list[str]:
    """Page ids cited on `← FI02 · I1` lines, in citation order."""
    out = []
    for line in text.splitlines():
        if "←" in line:
            for pid in _PAGE_ID.findall(line.split("←", 1)[1]):
                if pid not in out:
                    out.append(pid)
    return out


def _rows(text: str) -> list[tuple[str, str, str]]:
    """`W1   DO send ...   FK01 · K1` rows inside fenced blocks: id, text, from."""
    rows = []
    for block in re.findall(r"(?ms)^```\w*\n(.*?)^```", text):
        for line in block.splitlines():
            m = re.match(r"^([DIKW]\d+)\s{2,}(.+?)\s*$", line)
            if not m or "←" in line or m.group(1) in {r[0] for r in rows}:
                continue
            body = m.group(2)
            src = re.search(r"\s{2,}([A-Z][DIKW]\d{2} · \S+)\s*$", body)
            rows.append((m.group(1), body[:src.start()].strip() if src else body.strip(),
                         src.group(1) if src else ""))
    return rows


def _opening(text: str) -> list[str]:
    paras = [p.strip() for p in re.split(r"\n\s*\n", _section(text, "Opening")) if p.strip()]
    return [p for p in paras if not p.startswith(("#", "**", "```"))][:2]


def _limits(text: str) -> list[str]:
    body = _section(text, "Forbidden Overreach")
    return [l.strip() for l in body.splitlines() if l.strip().startswith(("❌", "🧊", "⚠"))]


def _inline(md: str) -> str:
    out = _e(md)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", out)


# ─── snapshot ───────────────────────────────────────────────────────────────

def _partitions(board_root: Path, pages: list[dict]) -> list[dict]:
    rows = []
    for folder in sorted(board_root.iterdir()):
        m = re.match(r"^\d+-([A-Z])-(.+)$", folder.name)
        if folder.is_dir() and m:
            rows.append({"id": m.group(1), "name": m.group(2), "folder": folder.name,
                         "pages": sum(p["partition"] == m.group(1) for p in pages),
                         "where": "", "rows": "", "share": ""})
    meta = next((p for p in pages if p["id"] == "MT00"), None)
    if meta:
        for row in rows:
            m = re.search(rf"(?m)^{row['id']}\s+{re.escape(row['name'])}\s+(.+?)\s{{2,}}\S+\.yaml",
                          meta["text"])
            if m:
                row["where"] = re.sub(r"^where:\s*\[\]\s*", "", m.group(1)).strip()
                tail = meta["text"][m.end():m.end() + 600]
                n = re.search(r"([\d,]+) of [\d,]+ rows\s+·\s+([\d.]+%)", tail)
                if n:
                    row["rows"], row["share"] = n.group(1), n.group(2)
    return rows


def _extract_context(board_text: str, pages: list[dict]) -> str:
    parts = []
    meta = next((p["text"] for p in pages if p["id"] == "MT00"), "")
    m = re.search(r"(\S+\.parquet)", meta) or re.search(r"(\S+\.parquet)", board_text)
    if m and "..." not in m.group(1):
        parts.append(m.group(1))
    for pat in (r"[\d,]+\s+messaged rows", r"\d{4}-\d{2}-\d{2}\s+to\s+\d{4}-\d{2}-\d{2}",
                r"\d+\s+message variants"):
        f = re.search(pat, board_text, re.I)
        if f:
            parts.append(f.group(0))
    return " · ".join(parts)


def _mtime_max(board_root: Path) -> float:
    latest = 0.0
    for path in board_root.rglob("*.md"):
        if not any(part in _SKIP for part in path.relative_to(board_root).parts):
            try:
                latest = max(latest, path.stat().st_mtime)
            except OSError:
                pass
    return latest


def board_snapshot(board_root: Path, server_root: Path | None = None,
                   board_arg: str = "", static: bool = False) -> dict:
    board_root = Path(board_root)
    server_root = Path(server_root or board_root)
    key = str(board_root.resolve())
    stamp = _mtime_max(board_root)
    cached = _CACHE.get(key)
    if cached and cached[0] == stamp and cached[1]["static"] == static \
            and cached[1]["root"] == server_root:
        return cached[1]
    text = _read(board_root / "board.md")
    pages = _pages(board_root)
    by_id = {p["id"]: p for p in pages}
    partitions = _partitions(board_root, pages)
    partition_ids = [row["id"] for row in partitions]
    registers = [p for p in pages if p["page_type"] == "question" or p["rung"]]
    questions = []
    for reg in sorted(registers, key=lambda p: p["id"]):
        questions.extend(_parse_register(reg, partition_ids))
    # cells a register grid does not carry are still real when a page answers them
    for page in pages:
        for qid in _QID.findall(page["state"]) if "answers" in page["state"] else []:
            row = next((q for q in questions if q["id"] == qid), None)
            if row and page["partition"] and not row["cells"].get(page["partition"], {}).get("page"):
                mark = _MARK.match(page["state"].strip())
                mark = mark.group(1) if mark else "⬜"
                row["cells"][page["partition"]] = {"mark": mark, "page": page["id"],
                                                    "note": "page", "raw": f"{mark} {page['id']}"}
    store_field = _field(text, "store")
    store = (server_root / store_field) if store_field else None
    rel = board_root.resolve().relative_to(server_root.resolve()).as_posix()
    snap = {
        "current": is_insight_board(board_root), "board": board_root, "root": server_root,
        "board_arg": board_arg, "static": static, "relative": rel,
        "title": (_TITLE.search(text).group(1).strip() if _TITLE.search(text) else board_root.name),
        "store": store_field, "store_path": store,
        "board_topic": _first_para(_section(text, "Topic")),
        "context": _extract_context(text, pages),
        "pages": pages, "by_id": by_id, "partitions": partitions, "questions": questions,
        "question_ids": [q["id"] for q in questions],
        "registers": {lvl: [p["path"] for p in registers if p["rung"] == lvl] for lvl in _LEVELS},
        "runs": _receipts(pages, store), "events": _log_events(pages),
        "handoffs": handoff_records(board_root, pages),
        "settled": sum(p["state"].startswith("✅") for p in pages),
    }
    _CACHE[key] = (stamp, snap)
    return snap


def _first_para(body: str) -> str:
    for para in re.split(r"\n\s*\n", body):
        para = para.strip()
        if para and not para.startswith(("#", "```")):
            return para
    return ""


def handoff_records(board_root: Path, pages: list[dict] | None = None) -> list[dict]:
    rows = []
    for page in pages if pages is not None else _pages(Path(board_root)):
        if page["level"] != "wisdom" and page["page_type"] != "wisdom":
            continue
        text = page["text"]
        if not _SERVES.search(text):
            continue
        sig = _SIGNED.search(text)
        serves = re.search(r"(?m)^\s*SERVES\s+(.+?)\s*$", text)
        rows.append({"page": page["path"], "record": page, "title": page["title"],
                     "state": page["state"], "signed": bool(sig),
                     "signature": sig.group(1).strip() if sig else "",
                     "serves": serves.group(1) if serves else "", "bindable": bool(sig)})
    return rows


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
    signed = bool(page and _SIGNED.search(page["text"]))
    gates = [
        ("GI0", "Meta ready", st(meta), "predicate", meta["state"][:60] if meta else "no MT00"),
        ("GI1", "Question registered", "passed" if row else "pending", "person",
         f"{row['register']['id']} row" if row else ""),
        ("GI2", "Data observed", st(lv.get("data")), "predicate",
         (receipt and f"{receipt['rel']} · {receipt['status']}") or (lv.get("data") or {}).get("id", "")),
        ("GI3", "Information derived", st(lv.get("information")), "agent", (lv.get("information") or {}).get("id", "")),
        ("GI4", "Knowledge claimed", st(lv.get("knowledge")), "agent", (lv.get("knowledge") or {}).get("id", "")),
        ("GI5", "Wisdom signed", "passed" if signed else ("held" if lv.get("wisdom") else "pending"),
         "person", _SIGNED.search(page["text"]).group(1) if signed else ""),
        ("GI6", "Cell settled", "passed" if cell["mark"] == "✅" else ("held" if cell["mark"] == "🟡" else
                                                                   "refused" if cell["mark"] == "🚫" else "pending"),
         "predicate", cell["raw"]),
    ]
    out = []
    for i, (key, name, state, who, note) in enumerate(gates):
        if i > needed and i < 6:
            state, note = "skipped", f"not needed below {_LEVEL_LABEL[target]}"
        out.append({"key": key, "name": name, "state": state, "who": who, "note": note})
    return out


# ─── render ─────────────────────────────────────────────────────────────────

_CSS = """
:root{--bg:#fff;--fg:#1c1c1c;--mut:#767672;--line:#e3e3e6;--soft:#f4f5f7;--acc:#3e5c84;--acc-soft:#e6edf5;--ok:#3a7d44;--ok-soft:#e5f1e7;--warn:#b3541e;--warn-soft:#f8ebe1;--bad:#8a3b3b;--bad-soft:#f5e6e6;--human:#6b4fa0;--human-soft:#ede8f6}
@media(prefers-color-scheme:dark){:root{--bg:#161719;--fg:#e8e8e6;--mut:#9c9c98;--line:#2c2e33;--soft:#212429;--acc:#8aa7cc;--acc-soft:#22304a;--ok:#7dbb87;--ok-soft:#1f3324;--warn:#e0955a;--warn-soft:#3a2a1c;--bad:#d98b8b;--bad-soft:#3a2323;--human:#b39ddb;--human-soft:#2c2540}}
*{box-sizing:border-box}body{margin:0;padding:16px;background:var(--bg);color:var(--fg);font:15px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
main{max-width:1250px}h1{font-size:17px;margin:0 0 2px}h2{font-size:17px;margin:0 0 3px}h3{font-size:14.5px;margin:14px 0 6px}p{margin:4px 0}
.mut{color:var(--mut);font-size:13px}.eyebrow{font:650 11px/1.4 -apple-system,sans-serif;color:var(--mut);text-transform:uppercase;letter-spacing:.05em}
code,.mono{font:12.5px ui-monospace,Menlo,monospace}a{color:var(--acc)}
.purpose{max-width:1050px;margin-top:8px;font-size:14.5px}.context{max-width:1050px;margin-top:4px;color:var(--mut);font-size:13px}
.spaces{display:flex;gap:5px;margin:12px 0 6px;flex-wrap:wrap}.space{font:600 11.5px -apple-system,sans-serif;border:1px solid var(--line);border-radius:8px;padding:3px 9px;cursor:pointer;background:var(--bg);color:var(--fg);white-space:nowrap}.space.on{border-color:var(--acc);color:var(--acc)}
.strip{display:flex;flex-wrap:wrap;gap:8px 18px;border:1px solid var(--line);border-radius:10px;background:var(--soft);padding:8px 14px;margin:0 0 8px;font-size:13px}.strip .id{font:650 14px ui-monospace,Menlo,monospace;color:var(--acc)}
.shell{border:1px solid var(--line);border-radius:10px;padding:10px 14px 14px;background:var(--bg)}.pane{display:none}.pane.on{display:block}
.wtabs{display:flex;gap:5px;flex-wrap:wrap;padding:0 0 10px;margin:0 0 12px;border-bottom:1px solid var(--line)}.wtab{font:500 12px -apple-system,sans-serif;border:1px solid var(--line);border-radius:8px;padding:5px 10px;cursor:pointer;background:transparent;color:var(--fg)}.wtab.on{border-color:var(--acc);color:var(--acc);font-weight:650}
.view{display:none}.view.on{display:block}.lead{margin:0 0 12px;color:var(--mut);font-size:14px}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}td,th{padding:7px 9px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{color:var(--mut);font-size:11px;font-weight:650;text-transform:uppercase;letter-spacing:.04em;white-space:nowrap}td.num{text-align:right;font-family:ui-monospace,Menlo,monospace;font-size:12.5px}.scroll{overflow-x:auto}
.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:1px 8px;font-size:11.5px;color:var(--mut);white-space:nowrap}.pill.ok{color:var(--ok);border-color:var(--ok);background:var(--ok-soft)}.pill.warn{color:var(--warn);border-color:var(--warn);background:var(--warn-soft)}.pill.bad{color:var(--bad);border-color:var(--bad);background:var(--bad-soft)}.pill.acc{color:var(--acc);border-color:var(--acc);background:var(--acc-soft)}.pill.human{color:var(--human);border-color:var(--human);background:var(--human-soft)}
.grid th .pn{display:block;font-weight:400;text-transform:none;letter-spacing:0;font-size:11px}a.mono .pn{color:var(--mut);font-family:-apple-system,sans-serif;font-size:12px}.grid td.cell{white-space:nowrap;font-family:ui-monospace,Menlo,monospace;font-size:12.5px;padding:0}.grid td.cell a{display:block;padding:7px 9px;color:inherit;text-decoration:none}.grid td.cell a:hover{background:var(--soft)}.grid td.cell.sel{outline:2px solid var(--acc);outline-offset:-2px;background:var(--acc-soft)}.grid td.q{max-width:300px}.grid tr.group td{background:var(--soft);color:var(--mut);font-size:11px;text-transform:uppercase;letter-spacing:.04em;font-weight:650;padding:5px 9px}
.gates{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));border:1px solid var(--line);border-radius:8px;overflow:hidden}.gate{padding:8px 9px;border-right:1px solid var(--line);font-size:12px;min-width:0}.gate:last-child{border-right:0}.gate .k{font:650 12px ui-monospace,Menlo,monospace}.gate .n{display:block;color:var(--mut)}.gate.passed{box-shadow:inset 0 3px 0 var(--ok)}.gate.held{box-shadow:inset 0 3px 0 var(--human)}.gate.refused{box-shadow:inset 0 3px 0 var(--bad)}.gate.pending,.gate.skipped{color:var(--mut)}.gate .who{display:block;margin-top:3px}
.opening{font-size:15.5px;max-width:70ch;padding:6px 0 10px;border-bottom:1px solid var(--line);margin-bottom:6px}.rows td:first-child{font-family:ui-monospace,Menlo,monospace;font-size:12.5px;white-space:nowrap}.rows td.from{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--mut);white-space:nowrap}
.rung{display:grid;grid-template-columns:130px 1fr;gap:12px;padding:12px 0;border-bottom:1px solid var(--line)}.rung:last-child{border-bottom:0}.rung .lvl{font-weight:650;font-size:13px}.rung .lvl small{display:block;color:var(--mut);font-weight:500;font-size:12px}
.chain{display:flex;flex-wrap:wrap;align-items:stretch;gap:6px}.chain .node{border:1px solid var(--line);border-radius:8px;padding:7px 10px;font-size:12.5px;min-width:120px}.chain .node b{display:block;font-size:11px;color:var(--mut);text-transform:uppercase;letter-spacing:.04em;margin-bottom:2px}.chain .arrow{align-self:center;color:var(--mut)}
.timeline{list-style:none;margin:0;padding:0}.timeline li{display:grid;grid-template-columns:70px 70px 1fr;gap:12px;padding:7px 0;border-bottom:1px solid var(--line);font-size:13.5px}.timeline .d,.timeline .p{font:12.5px ui-monospace,Menlo,monospace;color:var(--mut)}
.limits{border-left:3px solid var(--bad);padding-left:12px;font-size:13.5px}.limits p{margin:6px 0}.note{border:1px dashed var(--line);border-radius:8px;padding:10px 12px;color:var(--mut);font-size:13px}
.source{margin-top:18px;color:var(--mut);font-size:12px}
.form{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px 16px;align-items:start}.form .full{grid-column:1/-1}.field{display:flex;flex-direction:column;gap:5px}.field label{color:var(--mut);font-size:11px;text-transform:uppercase;letter-spacing:.04em;font-weight:650}.field input,.field select,.field textarea{border:1px solid var(--line);background:var(--bg);color:var(--fg);border-radius:7px;padding:8px;font:14px -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}.field textarea{min-height:60px;resize:vertical}
.btn{border:1px solid var(--acc);border-radius:8px;padding:8px 13px;background:var(--bg);color:var(--acc);font:650 14px -apple-system,sans-serif;cursor:pointer}.btn.primary{background:var(--acc);color:#fff}.actions{display:flex;gap:10px;flex-wrap:wrap;align-items:center}.status{font-size:13px;color:var(--mut)}
@media(max-width:820px){.form{grid-template-columns:1fr}}
@media(max-width:820px){.gates{grid-template-columns:repeat(4,1fr)}.rung{grid-template-columns:1fr}.timeline li{grid-template-columns:1fr}}
"""

_JS = """<script>(function(){
var sp=[].slice.call(document.querySelectorAll('.space')),pn=[].slice.call(document.querySelectorAll('.pane'));
function sel(s,w){if(!document.querySelector('.pane[data-space="'+s+'"]'))s='scope';sp.forEach(function(b){b.classList.toggle('on',b.dataset.space===s)});pn.forEach(function(p){p.classList.toggle('on',p.dataset.space===s)});if(w){try{var u=new URL(location.href);u.searchParams.set('space',s);history.replaceState({},'',u)}catch(e){}}}
sp.forEach(function(b){b.onclick=function(){sel(b.dataset.space,true)}});
document.querySelectorAll('.shell').forEach(function(sh){var tabs=[].slice.call(sh.querySelectorAll('.wtab'));function sync(){var on=sh.querySelector('.wtab.on');sh.querySelectorAll('.view').forEach(function(v){v.classList.toggle('on',on&&v.dataset.view===on.dataset.view)})}tabs.forEach(function(t){t.onclick=function(){tabs.forEach(function(x){x.classList.toggle('on',x===t)});sync()}});sync()});
sel(document.body.dataset.space,false);
var f=document.getElementById('askform');if(f){f.onsubmit=function(ev){ev.preventDefault();var q=document.getElementById('ask-text').value.replace(/\\s+/g,' ').trim();if(!q)return;
var cmd='/haipipe-insight application '+f.dataset.root+' question "'+q.replace(/"/g,"'")+'"';document.getElementById('ask-cmd').textContent=cmd;document.getElementById('ask-out').hidden=false;
var st=document.getElementById('ask-status');if(navigator.clipboard){navigator.clipboard.writeText(cmd).then(function(){st.textContent='copied'},function(){st.textContent='select and copy the line below'})}else{st.textContent='select and copy the line below'}}}
})();</script>"""


def _pill(mark: str, text: str = "") -> str:
    cls = {"✅": "ok", "🟡": "warn", "🚫": "bad", "🧊": "acc"}.get(mark, "")
    return f'<span class="pill {cls}">{_e(text or mark)}</span>'


def _cell_url(snap: dict, qid: str, pid: str, space: str = "insight") -> str:
    if snap["static"]:
        return f"insight.html?space={space}&q={qid}&p={pid}"
    base = f"/_board/insight-board?board={quote(snap['board'].name)}"
    return f"{base}&space={space}&q={qid}&p={pid}"


def _slug(page: dict) -> str:
    """`MT01-question-data` -> `question-data`: the folder's own name, so an
    id is never shown alone (JL 260916: "give them the full name")."""
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


def render_insight_board(snapshot: dict, space: str = "scope",
                         selected_question: str = "", selected_partition: str = "") -> str:
    snap = snapshot
    aliases = {"overview": "scope", "workflow": "run", "registers": "scope",
               "partitions": "scope", "groom": "check", "workspace": "scope"}
    space = aliases.get(space, space)
    if space not in {"scope", "insight", "evidence", "check", "run", "delivery"}:
        space = "scope"
    qids = snap["question_ids"]
    pids = [row["id"] for row in snap["partitions"]]
    qid = selected_question if selected_question in qids else ("QW1" if "QW1" in qids else (qids[0] if qids else ""))
    pid = selected_partition if selected_partition in pids else ("F" if "F" in pids else (pids[0] if pids else ""))
    view = _cell_view(snap, qid, pid) if qid else None
    # Run Space and Delivery Space are always the last two (JL 260916).
    return "".join([
        '<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">',
        f'<title>🔎 {_e(snap["title"])}</title><style>{_CSS}</style></head><body data-space="{_e(space)}"><main>',
        _render_header(snap),
        _render_nav(),
        _render_strip(snap, view, qid, pid),
        f'<section class="pane" data-space="scope"><div class="shell">{_render_scope(snap, qid, pid)}</div></section>',
        f'<section class="pane" data-space="insight"><div class="shell">{_render_insight(snap, view, qid, pid)}</div></section>',
        f'<section class="pane" data-space="evidence"><div class="shell">{_render_evidence(snap, view)}</div></section>',
        f'<section class="pane" data-space="check"><div class="shell">{_render_check(snap, view, qid, pid)}</div></section>',
        f'<section class="pane" data-space="run"><div class="shell">{_render_run(snap)}</div></section>',
        f'<section class="pane" data-space="delivery"><div class="shell">{_render_delivery(snap)}</div></section>',
        f'<p class=source>source <code>{_e(snap["relative"])}/board.md</code> · re-read on every request</p>',
        "</main>", _JS, "</body></html>",
    ])


def _render_header(snap: dict) -> str:
    if snap["static"]:
        links = '<a href="index.html">board index</a>'
    else:
        links = (f'<a href="/">all boards</a> · '
                 f'<a href="/{_e(snap["relative"])}/board/index.html">board index</a>')
    return f'<header><h1>🔎 {_e(snap["title"])}</h1><div class=mut>{links}</div></header>'


def _render_pages(snap: dict) -> str:
    """Every page on the board, grouped by folder, with its state and link."""
    groups: dict[str, list[dict]] = {}
    for page in snap["pages"]:
        groups.setdefault(page["rel"].split("/")[0], []).append(page)
    out = []
    for folder, pages in groups.items():
        out.append(f'<tr class=group><td colspan=4>{_e(folder)} · {len(pages)} pages</td></tr>')
        for page in pages:
            level = page["level"] or page["page_type"] or ""
            out.append(f'<tr><td>{_link(snap, page)}</td><td>{_e(page["title"])}</td>'
                       f'<td>{_e(level)}</td><td>{_pill(page["state"][:1], page["state"][:70])}</td></tr>')
    return (f'<h2>All pages</h2><p class=lead>{len(snap["pages"])} pages on this board, in folder order.</p>'
            f'<div class=scroll><table class=grid><tr><th>Id</th><th>Title</th><th>Level</th><th>State</th></tr>{"".join(out)}</table></div>')


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
            f'<header><h1>🔎 Insight Boards</h1><div class=mut><a href="/">all boards</a></div></header>{note}'
            f'<div class=shell><table><tr><th>Board</th><th>Title</th><th>Pages</th><th>Settled</th><th>Folder</th></tr>{body}</table></div>'
            '</main></body></html>')


def _next_step(snap: dict, view: dict, qid: str, pid: str) -> str:
    """What to do about the selected cell, as one line: a page to open or a
    command to hand to Claude Code.  The page reads; the skill writes."""
    cell, page = view["cell"], view["page"]
    cmd = f"/haipipe-insight application {snap['relative']} chain {qid} {pid}"
    stop = next((g for g in view["gates"][1:] if g["state"] in {"held", "pending"}), None)
    if cell["mark"] == "✅" and page:
        return f'done · read {_link(snap, page)}'
    if cell["mark"] == "🚫":
        return f'refused: {_e(cell["note"] or cell["raw"])} · nothing to run'
    if cell["mark"] == "·":
        return 'not asked on this data · use <b>Ask</b> in Scope Space'
    where = f' · stopped at {stop["key"]} {stop["name"]}' if stop else ""
    return f'give Claude Code <code>{_e(cmd)}</code>{where}'


def _render_nav() -> str:
    tabs = (("scope", "Scope Space"), ("insight", "Insight Space"), ("evidence", "Evidence Space"),
            ("check", "Check Space"), ("run", "Run Space"), ("delivery", "Delivery Space"))
    return '<nav class=spaces>' + "".join(
        f'<button class=space type=button data-space="{k}">{v}</button>' for k, v in tabs) + '</nav>'


_HEADS = ("midlife", "young", "older", "old", "senior", "adult", "child", "teen")


def _pretty(name: str) -> str:
    """`youngmale` -> `young male`, `midlifemale` -> `midlife male`: MT00
    keeps one token per partition, the screen keeps the words apart.  A known
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


def _partition_label(snap: dict, pid: str) -> str:
    name = _partition_name(snap, pid)
    return f'{pid} · {name}' if name else pid


def _render_strip(snap: dict, view: dict | None, qid: str, pid: str) -> str:
    """The one question the page is about right now, in plain words."""
    if not view or not view["row"]:
        return '<div class=strip><span class=mut>No register question found on this board.</span></div>'
    row, cell = view["row"], view["cell"]
    answer = cell["raw"] if cell["mark"] != "·" else "not asked on this data"
    return (f'<div class=strip>'
            f'<span><span class=eyebrow>Question</span><br><span class=id>{_e(qid)}</span> · {_e(_LEVEL_LABEL.get(qid[1], ""))} · {_e(row["question"])}</span>'
            f'<span><span class=eyebrow>Data</span><br>{_e(_partition_label(snap, pid))}</span>'
            f'<span><span class=eyebrow>Answer</span><br>{_pill(cell["mark"], answer)}</span>'
            f'<span><span class=eyebrow>Next</span><br>{_next_step(snap, view, qid, pid)}</span></div>')


def _render_scope(snap: dict, qid: str, pid: str) -> str:
    cols = [p for p in ("F", "B", "C", "D", "E", "G", "X")
            if any(p in q["cells"] for q in snap["questions"])]
    rows, last = [], ""
    for q in snap["questions"]:
        lv = q["id"][1]
        if lv != last:
            rows.append(f'<tr class=group><td colspan={len(cols) + 2}>{_e(_LEVEL_LABEL[lv])} · {_e(q["register"]["path"].stem)}</td></tr>')
            last = lv
        cells = ""
        for p in cols:
            c = q["cells"].get(p, {"mark": "·", "raw": "·"})
            on = " sel" if (q["id"] == qid and p == pid) else ""
            cells += f'<td class="cell{on}"><a href="{_e(_cell_url(snap, q["id"], p))}">{_e(c["raw"] or "·")}</a></td>'
        rows.append(f'<tr><td class=mono>{_e(q["id"])}</td><td class=q>{_e(q["question"])}</td>{cells}</tr>')
    register = (f'<h2>Question register</h2><p class=lead>One row per question, one column per partition, as written in MT01 to MT04. Click a cell.</p>'
                f'<div class=scroll><table class=grid><tr><th>Id</th><th>Question</th>{"".join(f"<th>{p}<br><span class=pn>{_e(_partition_name(snap, p) or p)}</span></th>" for p in cols)}</tr>{"".join(rows)}</table></div>'
                '<p class=mut style="margin-top:8px">✅ answered · 🟡 answered in part · 🚫 refused, with the reason · &nbsp;·&nbsp; not asked there</p>')
    prow = "".join(
        f'<tr><td><b>{_e(r["id"])}</b></td><td>{_e(_pretty(r["name"]))}</td><td class=mono>{_e(r["where"] or "—")}</td>'
        f'<td class=num>{_e(r["rows"] or "—")}</td><td class=num>{_e(r["share"] or "—")}</td><td class=num>{r["pages"]}</td></tr>'
        for r in snap["partitions"])
    data = (f'<h2>Data scope</h2><p class=lead>From MT00. A partition is one config, never a code change.</p>'
            f'<div class=scroll><table><tr><th>Id</th><th>Partition</th><th>Where</th><th>Rows</th><th>Share</th><th>Pages</th></tr>{prow}</table></div>'
            f'<p class=mut style="margin-top:8px">extract <code>{_e(snap["context"].split(" · ")[0] if snap["context"] else "")}</code> · store <code>{_e(snap["store"] or "not declared")}</code></p>')
    # One box.  The person asks in plain words; Claude Code decides the answer
    # level, the partitions and the lineage, then writes the register row
    # through `python3 -m live.insightboard ask ...`.
    ask = (
        '<h2>Ask</h2><p class=lead>Type the question. Claude Code decides what kind of answer it needs, which data cuts it runs on, and what it grew out of, then registers it.</p>'
        f'<form id=askform class=form data-root="{_e(snap["relative"])}">'
        '<div class="field full"><textarea id=ask-text required placeholder="e.g. does the send hour change which message works best?"></textarea></div>'
        '<div class="full actions"><button class="btn primary" type=submit>Ask</button><span class=status id=ask-status></span></div></form>'
        '<div id=ask-out hidden><p class=mut>Give this to Claude Code (copied to your clipboard):</p><p><code id=ask-cmd></code></p></div>')
    return (_tabs([("register", "Register"), ("ask", "Ask"), ("data", "Data"), ("pages", "Pages")])
            + _view("register", register, True) + _view("ask", ask) + _view("data", data)
            + _view("pages", _render_pages(snap)))


def _render_run(snap: dict) -> str:
    runs = snap["runs"]
    if runs:
        body = "".join(
            f'<tr><td class=mono>{_e(r["task"] or "?")} · {_e(r["call"] or "?")}</td><td>{_link(snap, r["page"])}</td>'
            f'<td>{_pill("✅" if r["status"] == "ok" else "🚫", r["status"])}</td><td class=mono>{_e(r["started"])}</td>'
            f'<td class=num>{_e(r["duration"] + " s" if r["duration"] else "")}</td><td class=mono>{_e(r["git"])}</td>'
            f'<td class=mono>{_e(r["rel"]) if r["found"] else _e(r["rel"]) + " · not found in store"}</td></tr>'
            for r in runs)
        ledger = f'<div class=scroll><table><tr><th>Run</th><th>Named by</th><th>Status</th><th>Started</th><th>Took</th><th>Git</th><th>Receipt</th></tr>{body}</table></div>'
    else:
        ledger = '<p class=note>No page on this board names a run receipt yet. A D page names one with a <code>run receipt</code> line or a <code>receipt:</code> header.</p>'
    ledger = '<h2>Runs</h2><p class=lead>Every run a page names, read from its <code>runtime.yaml</code> in the store.</p>' + ledger
    events = snap["events"][:60]
    tl = "".join(
        f'<li><span class=d>{_e(ev["date"])}</span><span class=p>{_link(snap, ev["page"])}</span><span>{_inline(ev["text"][:220])}{"…" if len(ev["text"]) > 220 else ""}</span></li>'
        for ev in events) or '<li class=mut>No <code>## Log</code> lines on this board.</li>'
    timeline = f'<h2>What happened</h2><p class=lead>Every dated <code>## Log</code> line on the board, newest first.</p><ul class=timeline>{tl}</ul>'
    return _tabs([("ledger", "Runs"), ("timeline", "Timeline")]) + _view("ledger", ledger, True) + _view("timeline", timeline)


def _rows_table(rows: list[tuple[str, str, str]]) -> str:
    if not rows:
        return ""
    return '<table class=rows>' + "".join(
        f'<tr><td>{_e(i)}</td><td>{_inline(t)}</td><td class=from>{_e(f)}</td></tr>' for i, t, f in rows) + '</table>'


def _render_insight(snap: dict, view: dict | None, qid: str, pid: str) -> str:
    if not view or not view["row"]:
        return '<p class=note>No question selected.</p>'
    row, cell, page = view["row"], view["cell"], view["page"]
    if not page:
        if cell["mark"] == "🚫":
            answer = f'<h2>{_e(row["question"])}</h2><p class=opening>Refused on {_e(pid)}: <b>{_e(cell["note"] or cell["raw"])}</b>. A refusal is a recorded answer, not a gap.</p>'
        else:
            answer = f'<h2>{_e(row["question"])}</h2><p class=opening>Not asked on partition {_e(pid)}. Pick another cell in the register.</p>'
        return _tabs([("answer", "Answer")]) + _view("answer", answer, True)
    opening = "".join(f'<p class=opening>{_inline(p)}</p>' for p in _opening(page["text"]))
    rows = _rows(page["text"])
    page_url = ("" if snap["static"] else
                f'/_board/insight?path={quote("/" + snap["relative"] + "/board.md", safe="/")}&file={quote(page["rel"], safe="/")}')
    answer = (f'<h2>{_e(page["title"])}</h2><p class=mut>{_link(snap, page)} · {_e(page["state"])}'
              f'{(" · <a href=" + chr(34) + _e(page_url) + chr(34) + ">open this page</a>") if page_url else ""}</p>'
              f'{opening}{_rows_table(rows)}')
    primary_ids = {p["id"] for p in view["primary"]}
    rungs = []
    for level in ("wisdom", "knowledge", "information", "data"):
        items = [it for it in view["ladder"] if it["page"]["level"] == level]
        if not items:
            continue
        main = next((it for it in items if it["page"]["id"] in primary_ids), items[0])
        others = [it["page"] for it in items if it is not main]
        rungs.append(
            f'<div class=rung><div class=lvl>{_e(_LEVEL_LABEL[level[0].upper()])}'
            f'<small>{_link(snap, main["page"])} · {_e(main["page"]["title"])}</small>'
            f'<small>{_pill(main["page"]["state"][:1], main["page"]["state"][:48])}</small></div>'
            f'<div>{_rows_table(main["rows"][:8])}'
            f'{("<p class=mut>… " + str(len(main["rows"]) - 8) + " more rows</p>") if len(main["rows"]) > 8 else ""}'
            f'{("<p class=mut>also cited: " + ", ".join(_link(snap, p) for p in others) + "</p>") if others else ""}</div></div>')
    ladder = ('<h2>How the answer was built</h2><p class=lead>Top down, along the first citation at each level. Other cited pages are linked.</p>'
              + ("".join(rungs) or '<p class=note>No citations found.</p>'))
    limits = "".join(f'<p>{_inline(l)}</p>' for l in _limits(page["text"]))
    limits = ('<h2>What this answer may not say</h2><div class=limits>' + limits + '</div>') if limits else '<p class=note>This page has no Forbidden Overreach section.</p>'
    return (_tabs([("answer", "Answer"), ("ladder", "Ladder"), ("limits", "Limits")])
            + _view("answer", answer, True) + _view("ladder", ladder) + _view("limits", limits))


def _render_evidence(snap: dict, view: dict | None) -> str:
    nodes = []
    if view and view["page"]:
        for p in view["primary"]:
            rows = _rows(p["text"])
            first = rows[0] if rows else None
            nodes.append(f'<div class=node><b>{_e(p["level"] or "page")}</b>{_link(snap, p)}<br><span class=mut>{_e(first[1][:70] if first else p["title"][:70])}</span></div>')
        r = view["receipt"]
        if r:
            nodes.append(f'<div class=node><b>receipt</b><span class=mono>{_e(r["rel"])}</span><br><span class=mut>{_e(r["status"])} · {_e(r["git"])} · {_e(r["duration"])} s</span></div>')
        if snap["context"]:
            nodes.append(f'<div class=node><b>extract</b><span class=mono>{_e(snap["context"].split(" · ")[0])}</span></div>')
    chain = ('<h2>Trace</h2><p class=lead>From the answer down to the extract. Each hop is a file that exists.</p><div class=chain>'
             + '<span class=arrow>←</span>'.join(nodes) + '</div>') if nodes else '<p class=note>Select an answered cell to trace it.</p>'
    if view and view["page"] and not view["receipt"]:
        chain += '<p class=note style="margin-top:12px">No page in this chain names a run receipt, so the trace stops at the D page.</p>'
    return chain


def _render_delivery(snap: dict) -> str:
    """What leaves this board: person-signed Wisdom handoffs a DesignBoard may bind."""
    hrows = "".join(
        f'<tr><td>{_link(snap, h["record"])} · {_e(h["title"])}</td><td class=mono>{_e(h["serves"])}</td>'
        f'<td>{_pill("✅", "✅ " + h["signature"]) if h["signed"] else _pill("⬜", "unsigned · waits for a person")}</td></tr>'
        for h in snap["handoffs"]) or '<tr><td colspan=3 class=mut>No Wisdom handoff on this board yet.</td></tr>'
    signed = sum(h["signed"] for h in snap["handoffs"])
    return (f'<h2>Delivery</h2><p class=lead>{signed} signed handoff(s) can be bound by a DesignBoard; '
            f'{len(snap["handoffs"]) - signed} wait for a signature. D, I and K pages never leave the board directly.</p>'
            f'<table><tr><th>Wisdom page</th><th>Serves</th><th>Signed</th></tr>{hrows}</table>')


def _render_check(snap: dict, view: dict | None, qid: str, pid: str) -> str:
    if not view or not view["row"]:
        gates = '<p class=note>No cell selected.</p>'
    else:
        gates = '<div class=gates>' + "".join(
            f'<div class="gate {g["state"]}"><span class=k>{_e(g["key"])}</span><span class=n>{_e(g["name"])}</span>'
            f'<span class=who><span class="pill {"human" if g["who"] == "person" else "acc" if g["who"] == "agent" else ""}">{_e(g["who"])}</span> {_e(g["state"])}</span>'
            f'{("<span class=n>" + _e(g["note"][:60]) + "</span>") if g["note"] else ""}</div>'
            for g in view["gates"]) + '</div>'
    gates = f'<h2>Gates for {_e(qid)} × {_e(pid)}</h2><p class=lead>Seven gates per cell. Purple gates need a person; GI5 always does.</p>' + gates
    groom = groom_snapshot(snap["board"], snap)
    crow = "".join(
        f'<tr><td>{_pill("🚫" if c["level"] == "FAIL" else "🟡" if c["level"] == "WARN" else "✅", c["level"])}</td>'
        f'<td class=mono>{_e(c["where"])}</td><td>{_inline(c["message"])}</td></tr>' for c in groom["checks"])
    mech = f'<h2>Mechanical checks</h2><p class=lead>From <code>cli/check.py</code>, whole board.</p><table><tr><th>Level</th><th>Where</th><th>Finding</th></tr>{crow}</table>'
    return _tabs([("gates", "Gates"), ("mech", "Mechanical checks")]) + _view("gates", gates, True) + _view("mech", mech)


def groom_snapshot(board_root: Path, snapshot: dict | None = None) -> dict:
    """Read-only audit: the mechanical checker plus the partial registers."""
    board_root = Path(board_root)
    snapshot = snapshot or board_snapshot(board_root, board_root, static=True)
    checks = []
    try:
        from cli.check import Report, check_insight_family
        report = Report()
        check_insight_family(board_root, report)
        checks.extend({"level": level, "code": code, "where": where, "message": message}
                      for level, code, where, message in report.rows)
    except (ImportError, OSError, ValueError) as exc:
        checks.append({"level": "WARN", "code": "insight-checker-unavailable",
                       "where": board_root.name, "message": str(exc)})
    if not checks:
        checks.append({"level": "PASS", "code": "insight-check-clean", "where": board_root.name,
                       "message": "mechanical InsightBoard checks returned no findings"})
    queue = [{"rung": lvl, "page": path, "state": _field(_read(path), "state") or "OPEN",
              "next": "continue the register frontier"}
             for lvl, paths in snapshot["registers"].items() for path in paths
             if not (_field(_read(path), "state") or "").startswith("✅")]
    bindable = [h for h in snapshot["handoffs"] if h["bindable"]]
    if not bindable:
        checks.append({"level": "WARN", "code": "no-signed-design-handoff", "where": board_root.name,
                       "message": "no signed Wisdom Design Handoff is available to Design"})
    return {"checks": checks, "queue": queue, "handoffs": snapshot["handoffs"], "bindable_handoffs": bindable}


# ─── page level: one page seen from its cell ────────────────────────────────

def page_cells(snap: dict, page: dict) -> list[tuple[str, str]]:
    """The register cells this page answers, as (question id, partition)."""
    out = []
    for row in snap["questions"]:
        for pid, cell in row["cells"].items():
            if cell.get("page") == page["id"]:
                out.append((row["id"], pid))
    return out


def render_page_insight(snap: dict, page: dict, board_path: str, view: str = "page") -> str:
    """The page-level Insight surface: what this page answers, what it cites,
    who cites it, its gates and its log.  Same data as the board plugin, one
    page deep.  The Outline plugin stays the page's writing workbench."""
    cells = page_cells(snap, page)
    qid, pid = cells[0] if cells else ("", page["partition"])
    cv = _cell_view(snap, qid, pid) if qid else None
    board_url = _cell_url(snap, qid, pid) if qid else f"/_board/insight-board?board={quote(snap['board'].name)}"
    cited_by = [p for p in snap["pages"] if page["id"] in _parents(p["text"])]
    parents = [snap["by_id"][pid_] for pid_ in _parents(page["text"]) if pid_ in snap["by_id"]]
    rows = _rows(page["text"])
    opening = "".join(f'<p class=opening>{_inline(p)}</p>' for p in _opening(page["text"]))
    level = _LEVEL_LABEL.get((page["level"] or " ")[0].upper(), page["page_type"] or "page")
    where = (" · ".join(f'<a href="{_e(_cell_url(snap, q, p))}" class=mono>{_e(q)} × {_e(_partition_label(snap, p))}</a>' for q, p in cells)
             or "<span class=mut>answers no register cell</span>")
    header = (f'<header><h1>🔎 {_e(page["title"])}</h1><div class=mut>{_e(page["path"].stem)} · {_e(level)} · '
              f'part of <a href="{_e(board_url)}">{_e(snap["title"])}</a> · answers {where}</div></header>')
    strip = _render_strip(snap, cv, qid, pid) if cv and cv["row"] else ""
    this = (f'<h2>This page</h2><p class=mut>{_pill(page["state"][:1], page["state"][:90])}</p>{opening}{_rows_table(rows)}'
            + ('' if rows else '<p class=note>No id-numbered rows in a fenced block on this page.</p>'))
    cites = ('<h2>Cites</h2>' + ('<table><tr><th>Page</th><th>Title</th><th>State</th></tr>' + "".join(
        f'<tr><td>{_link(snap, p)}</td><td>{_e(p["title"])}</td><td>{_pill(p["state"][:1], p["state"][:40])}</td></tr>'
        for p in parents) + '</table>' if parents else '<p class=note>This page cites no other page by id.</p>'))
    by = ('<h2>Cited by</h2>' + ('<table><tr><th>Page</th><th>Title</th><th>State</th></tr>' + "".join(
        f'<tr><td>{_link(snap, p)}</td><td>{_e(p["title"])}</td><td>{_pill(p["state"][:1], p["state"][:40])}</td></tr>'
        for p in cited_by) + '</table>' if cited_by else '<p class=note>No page cites this one yet.</p>'))
    gates = ('<h2>Gates</h2><div class=gates>' + "".join(
        f'<div class="gate {g["state"]}"><span class=k>{_e(g["key"])}</span><span class=n>{_e(g["name"])}</span>'
        f'<span class=who><span class="pill {"human" if g["who"] == "person" else "acc" if g["who"] == "agent" else ""}">{_e(g["who"])}</span> {_e(g["state"])}</span></div>'
        for g in cv["gates"]) + '</div>') if cv and cv["row"] else '<h2>Gates</h2><p class=note>No register cell, so no gates.</p>'
    log_lines = _LOG_LINE.findall(_section(page["text"], "Log"))
    log = ('<h2>Log</h2><ul class=timeline>' + "".join(
        f'<li><span class=d>{_e(d)}</span><span class=p></span><span>{_inline(t[:240])}</span></li>' for d, t in reversed(log_lines))
        + '</ul>') if log_lines else '<h2>Log</h2><p class=note>No dated log line on this page.</p>'
    shell = (_tabs([("page", "This page"), ("cites", "Cites"), ("by", "Cited by"), ("gates", "Gates"), ("log", "Log")])
             + _view("page", this, True) + _view("cites", cites) + _view("by", by) + _view("gates", gates) + _view("log", log))
    return "".join([
        '<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">',
        f'<title>🔎 {_e(page["id"])} · {_e(page["title"])}</title><style>{_CSS}</style></head><body data-space="page"><main>',
        header, strip, f'<div class="shell">{shell}</div>',
        f'<p class=source>source <code>{_e(snap["relative"])}/{_e(page["rel"])}</code> · <a href="{_e(_page_link(snap, page))}">rendered page</a></p>',
        "</main>", _JS, "</body></html>",
    ])


# ─── server mixin ───────────────────────────────────────────────────────────

class InsightBoardMixin:
    """GET/HEAD/POST read-only surface for a whole InsightBoard."""

    def _insight_target(self, raw: str) -> Path | None:
        return _safe_board(Path(self.root), raw) or _board_by_name(Path(self.root), raw)

    def insight_board_view(self, head_only=False):
        query = parse_qs(urlparse(self.path).query)
        raw = (query.get("board") or query.get("path") or [""])[0]
        board = self._insight_target(raw)
        if board is None:
            # The plugin has two levels, board and page, and no list of its
            # own (JL 260916).  No board named: go to the one InsightBoard
            # when there is exactly one.  Otherwise a short 404 that names
            # what was asked and what exists.
            boards = insight_boards(Path(self.root))
            if not raw and len(boards) == 1:
                self.send_response(302)
                self.send_header("Location", f"/_board/insight-board?board={quote(boards[0].name)}")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return None
            body = render_board_list(Path(self.root), raw).encode("utf-8")
            return self._insight_board_send(body, 404, head_only)
        snapshot = board_snapshot(board, self.root, raw)
        body = render_insight_board(
            snapshot, (query.get("space") or ["scope"])[0],
            (query.get("q") or query.get("question") or [""])[0],
            (query.get("p") or query.get("partition") or [""])[0],
        ).encode("utf-8")
        return self._insight_board_send(body, 200 if snapshot["current"] else 404, head_only)

    def insight_page_view(self, head_only=False):
        """GET /_board/insight?path=<board>&file=<page.md>: one page, seen from its cell."""
        query = parse_qs(urlparse(self.path).query)
        payload = {"path": (query.get("path") or [""])[0], "file": (query.get("file") or [""])[0]}
        short_board = (query.get("board") or [""])[0]
        short_page = (query.get("page") or [""])[0].strip().upper()
        if short_board and short_page:
            # Short form for a terminal: ?board=<folder name>&page=<page id>.
            board = _board_by_name(Path(self.root), short_board)
            hit = next((p for p in (_pages(board) if board else []) if p["id"] == short_page), None)
            if board is None or hit is None:
                body = f"<h1>🔎 Insight</h1><p>no page {_e(short_page)} on board {_e(short_board)}</p>".encode("utf-8")
                return self._insight_board_send(body, 404, head_only)
            payload = {"path": "/" + board.relative_to(Path(self.root)).as_posix() + "/board.md", "file": hit["rel"]}
        got = self.target(payload)
        if got[0] is None:
            body = f"<h1>🔎 Insight</h1><p>{_e(got[1])}</p>".encode("utf-8")
            return self._insight_board_send(body, 404, head_only)
        page_src, board = Path(got[0]), Path(got[1])
        snapshot = board_snapshot(board, self.root, payload["path"])
        page = next((p for p in snapshot["pages"] if p["path"].resolve() == page_src.resolve()), None)
        if page is None:
            body = "<h1>🔎 Insight</h1><p>this file is not a page of an InsightBoard</p>".encode("utf-8")
            return self._insight_board_send(body, 404, head_only)
        body = render_page_insight(snapshot, page, payload["path"]).encode("utf-8")
        return self._insight_board_send(body, 200 if snapshot["current"] else 404, head_only)

    def plug_insight_page(self, payload):
        got = self.target(payload)
        if got[0] is None:
            return None, got[1]
        if not is_insight_board(Path(got[1])):
            return None, "this page is not on an InsightBoard"
        return {"url": "/_board/insight?path=%s&file=%s"
                % (quote(payload.get("path") or ""), quote(payload.get("file") or ""))}, None

    def _insight_board_send(self, body: bytes, code: int, head_only: bool):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def plug_insight_board(self, payload):
        board = self._insight_target(payload.get("path") or payload.get("board") or "")
        if board is None:
            return None, "path must identify a Board with board.md"
        if not is_insight_board(board):
            return None, "selected Board is not an InsightBoard"
        if payload.get("action") == "ask":
            try:
                qid, pids = register_question(
                    board, payload.get("level", ""), payload.get("question", ""),
                    payload.get("partition") or payload.get("partitions") or "",
                    payload.get("origin", ""), payload.get("parent", ""))
            except ValueError as exc:
                return None, str(exc)
            return {"url": f"/_board/insight-board?board={quote(board.name)}&space=insight&q={qid}&p={pids[0]}",
                    "question": qid, "partitions": pids}, None
        return {"url": "/_board/insight-board?board=%s" % quote(board.name)}, None


def _main(argv: list[str]) -> int:
    """`python3 -m live.insightboard ask <board> <D|I|K|W> <F,B,C> "<question>" [--origin X] [--parent Y]`

    The write half of the skill's `question` verb: Claude Code decides the
    arguments, this writes the row and prints the cell to open next.
    """
    import argparse
    ap = argparse.ArgumentParser(prog="insightboard")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ask = sub.add_parser("ask", help="register one question on its register")
    ask.add_argument("board")
    ask.add_argument("level", help="D, I, K or W")
    ask.add_argument("partitions", help="comma-separated partition letters, e.g. F or F,B,C")
    ask.add_argument("question")
    ask.add_argument("--origin", default="", help="curiosity-driven or need-driven")
    ask.add_argument("--parent", default="", help="what it grew out of, e.g. 'FI08 · I3' or 'QI9'")
    args = ap.parse_args(argv)
    board = Path(args.board).resolve()
    if not (board / "board.md").is_file():
        print(f"not a Board: {board}")
        return 2
    try:
        qid, pids = register_question(board, args.level, args.question, args.partitions,
                                      args.origin, args.parent)
    except ValueError as exc:
        print(f"refused: {exc}")
        return 1
    print(f"registered {qid} on {', '.join(pids)} · next: /haipipe-insight application {board.name} chain {qid} {pids[0]}")
    return 0



# ─── the one write: register a question ─────────────────────────────────────

def register_question(board_root: Path, level: str, question: str, partitions,
                      origin: str = "", parent: str = "") -> tuple[str, list[str]]:
    """Append one row to the register facing `level` and one `## Log` line.

    Called by the skill (`python3 -m live.insightboard ask ...`) after Claude
    Code has decided the level, the partitions and the lineage.  The register
    grid is the source of truth for questions, so this is the only file the
    board plugin ever writes.  Wisdom (MT04) keeps a transposed grid and is
    left to a person.
    """
    level = (level or "").strip().upper()[:1]
    question = " ".join((question or "").split())
    if isinstance(partitions, str):
        partitions = re.split(r"[,\s]+", partitions)
    partitions = [p.strip().upper()[:1] for p in partitions if p and p.strip()]
    if level not in _LEVEL_OF:
        raise ValueError("kind of answer must be D, I, K or W")
    if not question:
        raise ValueError("the question is empty")
    if not partitions:
        raise ValueError("choose at least one partition")
    pages = _pages(Path(board_root))
    register = next((p for p in pages if p["rung"] == _LEVEL_OF[level]
                     or (p["page_type"] == "question" and p["id"] == f"MT0{'DIKW'.index(level) + 1}")), None)
    if register is None:
        raise ValueError(f"no register page faces the {_LEVEL_LABEL[level]} level")
    qid = _append_question_row(register["path"], level, question, partitions, origin, parent)
    return qid, partitions


def _append_question_row(path: Path, level: str, question: str, partitions,
                         origin: str = "", parent: str = "") -> str:
    if isinstance(partitions, str):
        partitions = [partitions]
    import datetime
    import textwrap

    text = _read(path)
    fence = re.compile(r"(?ms)^```\w*\n(.*?)^```")
    block = next((m for m in fence.finditer(text) if re.search(r"(?m)^Q[DIKW]\d+\s", m.group(1))), None)
    if block is None:
        raise ValueError(f"{path.name} has no question grid")
    lines = block.group(1).splitlines()
    header = next((l for l in lines if re.match(r"^id\s", l)), "")
    if "partition" in header and _QID.search(header):
        raise ValueError(f"{path.name} keeps a transposed grid; add the row by hand")
    cols = [(m.group(1), m.start()) for m in re.finditer(r"\b([A-Z])·[a-z]+", header)]
    if re.search(r"\bX\s*$", header):
        cols.append(("X", header.rstrip().rfind("X")))
    missing = [p for p in partitions if p not in {pid for pid, _ in cols}]
    if missing:
        raise ValueError(f"{path.name} has no {', '.join(missing)} column; add it by hand first")
    q_off = header.find("question")
    gen_off = header.find("Gen-1")
    if q_off < 0 or gen_off < 0 or not cols:
        raise ValueError(f"{path.name}: grid header not understood")
    numbers = [int(m) for m in re.findall(rf"(?m)^Q{level}(\d+)\s", block.group(1))]
    qid = f"Q{level}{max(numbers, default=0) + 1}"
    width = max(12, gen_off - q_off - 2)
    chunks = textwrap.wrap(question, width, break_on_hyphens=False) or [question]
    first = qid.ljust(q_off) + chunks[0]
    first = first.ljust(gen_off) + "(none)"
    for i, (pid, start) in enumerate(cols):
        first = first.ljust(start) + ("⬜ open" if pid in partitions else "·")
    new_lines = [first] + [" " * q_off + c for c in chunks[1:]]
    last = max((i for i, l in enumerate(lines) if re.match(r"^Q[DIKW]\d+\s", l)), default=-1)
    while last + 1 < len(lines) and re.match(r"^\s{4,}\S", lines[last + 1]) and not _MARK.search(lines[last + 1]):
        last += 1  # keep a wrapped question with its row
    lines[last + 1:last + 1] = new_lines
    body = "\n".join(lines) + "\n"
    text = text[:block.start(1)] + body + text[block.end(1):]
    stamp = datetime.date.today().strftime("%y%m%d")
    entry = (f"{stamp} · Registered `{qid}` on {', '.join(partitions)} from the Insight Board"
             f" · origin: {origin or 'not stated'} · born from: {parent or 'new'} · \"{question}\"")
    # The receipt goes where this board already keeps the register's log:
    # the canonical outline/<stem>-log.md when it exists, else the page's
    # own Log division (what A00 does).
    side_log = path.parent / "outline" / f"{path.stem}-log.md"
    if side_log.is_file():
        side_log.write_text(_read(side_log).rstrip("\n") + "\n\n" + entry + "\n", encoding="utf-8")
    elif re.search(r"(?m)^## Log\s*$", text):
        text = text.rstrip("\n") + "\n\n" + entry + "\n"
    else:
        text = text.rstrip("\n") + "\n\n## Log\n\n" + entry + "\n"
    path.write_text(text, encoding="utf-8")
    return qid
if __name__ == "__main__":
    import sys
    raise SystemExit(_main(sys.argv[1:]))
