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
import hashlib
import re
import uuid
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse

from src.folder_contract import resolved_folder_kind
from .insight_handoff import eligibility as handoff_eligibility, watch_paths as handoff_watch_paths
from .insight_run_specs import (definition as read_insight_definition, describe as describe_run_field,
                                people as run_people, reader_name as run_reader_name,
                                request_text as insight_request_text, selected_specs)


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
_CACHE: dict[str, tuple[tuple, dict]] = {}


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


# a server rooted at the SPACE, at one project, or at one applications/ folder finds its boards
_BOARD_GLOBS = ("examples*/*/applications/*/board.md", "examples*/*/*/board.md",
                "applications/*/board.md", "*/board.md")


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
        identity_error = ""
        try:
            kind = resolved_folder_kind(path.parent, declared=head.get("folder-kind", ""),
                                        legacy=head.get("page-type", ""))
        except ValueError as exc:
            kind, identity_error = "", str(exc)
        stem = path.stem.split("-", 1)[0].upper()
        m = re.match(r"^([A-Z]?)([DIKW])\d{2}$", stem)
        part = next((re.match(r"^\d+-([A-Z])-", p).group(1) for p in rel.parts
                     if re.match(r"^\d+-([A-Z])-", p)), "")
        pages.append({
            "path": path, "rel": rel.as_posix(), "id": stem, "text": text,
            "title": (_TITLE.search(text).group(1).strip() if _TITLE.search(text) else path.stem),
            "state": head.get("state", "OPEN"),
            "page_type": kind, "identity_error": identity_error,
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
    """`W1   DO send ...   FK01 · K1` rows inside fenced blocks: id, text, from.
    An indented line right under a row continues its text, so a row that
    wraps in the page is shown whole (W3 on FW01 ended "on the")."""
    rows: list[list[str]] = []
    for block in re.findall(r"(?ms)^```\w*\n(.*?)^```", text):
        last, col = None, 0
        for line in block.splitlines():
            m = re.match(r"^([DIKW]\d+)\s{2,}(.+?)\s*$", line)
            if m and "←" not in line and m.group(1) not in {r[0] for r in rows}:
                body = m.group(2)
                src = re.search(r"\s{2,}([A-Z][DIKW]\d{2}\s?·\s?\S+)\s*$", body)
                last = [m.group(1), body[:src.start()].strip() if src else body.strip(),
                        src.group(1) if src else ""]
                rows.append(last)
                col = m.start(2)
            elif last and "←" not in line and not line[:col].strip() and line[col:col + 1].strip():
                # only the text column's wrap; a side column's wrap is its own
                last[1] += " " + re.split(r"\s{2,}", line[col:].strip())[0]
            else:
                last = None
    return [tuple(r) for r in rows]


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
            m = re.search(rf"(?m)^{row['id']}\s+{re.escape(row['name'])}\s+(.+?)\s{{2,}}(?:\S+\.yaml|\(none\))",
                          meta["text"])
            if m:
                row["where"] = re.sub(r"^where:\s*\[\]\s*", "", m.group(1)).strip()
                tail = meta["text"][m.end():m.end() + 600]
                # the rule continues on the next lines ("AND age lte 35.0"), and a
                # where read without them names the wrong population (JL 260921)
                for line in tail.splitlines()[1:7]:
                    clause = line.strip()
                    if re.match(r"^(AND|OR)\b", clause):
                        row["where"] += " " + clause
                    elif re.match(r"^[\d,]+ of ", clause):
                        break
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
    runtime_stamp = []
    for path in sorted((board_root / "_runs" / "insight").glob("*/runtime.yaml")):
        try:
            stat = path.stat()
            runtime_stamp.append((path.as_posix(), stat.st_mtime_ns, stat.st_size))
        except OSError:
            continue
    identity_stamp = []
    for path in sorted(board_root.rglob("workflow/*.yaml")):
        if path.name not in {"folder.yaml", "phase.yaml", "handoff.yaml"}:
            continue
        try:
            stat = path.stat()
            identity_stamp.append((path.as_posix(), stat.st_mtime_ns, stat.st_size))
        except OSError:
            continue
    source_stamp = []
    source_paths = set(board_root.rglob("*.md")) | set(handoff_watch_paths(board_root))
    for path in sorted(source_paths):
        try:
            stat = path.stat()
            source_stamp.append((path.as_posix(), stat.st_mtime_ns, stat.st_size))
        except OSError:
            source_stamp.append((path.as_posix(), None, None))
    stamp = (tuple(source_stamp), tuple(runtime_stamp), tuple(identity_stamp))
    cached = _CACHE.get(key)
    if cached and cached[0] == stamp and cached[1]["static"] == static \
            and cached[1]["root"] == server_root:
        return cached[1]
    text = _read(board_root / "board.md")
    pages = _pages(board_root)
    by_id = {p["id"]: p for p in pages}
    partitions = _partitions(board_root, pages)
    partition_ids = [row["id"] for row in partitions]
    registers = [p for p in pages if not p["identity_error"] and
                 (p["page_type"] == "question" or (not p["page_type"] and p["rung"]))]
    questions = []
    for reg in sorted(registers, key=lambda p: p["id"]):
        questions.extend(_parse_register(reg, partition_ids))
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
        "workflow_runtimes": _workflow_runtimes(board_root),
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
    pages = pages if pages is not None else _pages(Path(board_root))
    partitions = [row["id"] for row in _partitions(Path(board_root), pages)]
    questions = [row for register in pages
                 if register["page_type"] == "question" and not register["identity_error"]
                 for row in _parse_register(register, partitions)]
    for page in pages:
        if page["page_type"] and page["page_type"] != "wisdom":
            continue
        if page["level"] != "wisdom" and page["page_type"] != "wisdom":
            continue
        text = page["text"]
        if not _SERVES.search(text):
            continue
        sig = _SIGNED.search(text)
        serves = re.search(r"(?m)^\s*SERVES\s+(.+?)\s*$", text)
        signature = sig.group(1).strip() if sig else ""
        served = serves.group(1) if serves else ""
        eligibility = handoff_eligibility(page, signature, served)
        if eligibility["bindable"]:
            for qid in set(_QID.findall(served)):
                matches = [q for q in questions if q["id"] == qid]
                cell = matches[0]["cells"].get(page["partition"] or "F", {}) if len(matches) == 1 else {}
                terminal = cell.get("mark") == "✅" or (cell.get("mark") == "🟡" and "final" in cell.get("note", ""))
                if not terminal or cell.get("page") != page["id"]:
                    eligibility.update(bindable=False, eligibility="unverified",
                                       eligibility_reason=f"current register cell {qid} is not settled to this Page")
                    break
        rows.append({"page": page["path"], "record": page, "title": page["title"],
                     "state": page["state"], "signed": bool(sig),
                     "signature": signature, "serves": served,
                     **eligibility})
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

_CSS = """
:root{--bg:#fff;--fg:#1c1c1c;--mut:#767672;--line:#e3e3e6;--soft:#f4f5f7;--acc:#3e5c84;--acc-soft:#e6edf5;--ok:#3a7d44;--ok-soft:#e5f1e7;--warn:#b3541e;--warn-soft:#f8ebe1;--bad:#8a3b3b;--bad-soft:#f5e6e6;--human:#6b4fa0;--human-soft:#ede8f6}
@media(prefers-color-scheme:dark){:root{--bg:#161719;--fg:#e8e8e6;--mut:#9c9c98;--line:#2c2e33;--soft:#212429;--acc:#8aa7cc;--acc-soft:#22304a;--ok:#7dbb87;--ok-soft:#1f3324;--warn:#e0955a;--warn-soft:#3a2a1c;--bad:#d98b8b;--bad-soft:#3a2323;--human:#b39ddb;--human-soft:#2c2540}}
*{box-sizing:border-box}body{margin:0;padding:16px;background:var(--bg);color:var(--fg);font:15px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
main{max-width:1440px}h1{font-size:17px;margin:0 0 2px}h2{font-size:17px;margin:0 0 3px}h3{font-size:14.5px;margin:14px 0 6px}p{margin:4px 0}
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
.grid th .pn{display:block;font-weight:400;text-transform:none;letter-spacing:0;font-size:11px}a.mono .pn{color:var(--mut);font-family:-apple-system,sans-serif;font-size:12px}.grid td.cell{font-family:ui-monospace,Menlo,monospace;font-size:12.5px;padding:0;min-width:92px}.grid td.cell a{display:block;padding:7px 9px;color:inherit;text-decoration:none}.grid td.cell a:hover{background:var(--soft)}.grid td.cell.sel{outline:2px solid var(--acc);outline-offset:-2px;background:var(--acc-soft)}.grid td.q{max-width:300px;min-width:170px}.nw{white-space:nowrap}.grid tr.group td{background:var(--soft);color:var(--mut);font-size:11px;text-transform:uppercase;letter-spacing:.04em;font-weight:650;padding:5px 9px}
.gates{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));border:1px solid var(--line);border-radius:8px;overflow:hidden}.gate{padding:8px 9px;border-right:1px solid var(--line);font-size:12px;min-width:0;overflow-wrap:anywhere}.gate:last-child{border-right:0}.gate .k{font:650 12px ui-monospace,Menlo,monospace}.gate .n{display:block;color:var(--mut)}.gate.passed{box-shadow:inset 0 3px 0 var(--ok)}.gate.held{box-shadow:inset 0 3px 0 var(--human)}.gate.refused{box-shadow:inset 0 3px 0 var(--bad)}.gate.pending,.gate.skipped{color:var(--mut)}.gate .who{display:block;margin-top:3px}
.workline{margin:0 0 10px;padding:6px 0 8px;border-bottom:1px solid var(--line);color:var(--mut);font-size:12.5px;line-height:1.55}.workline .wl-count{color:var(--fg);opacity:.8}.workline .wl-more{margin-left:8px;white-space:nowrap}
.who td{font-size:12.5px;overflow-wrap:break-word}.who td:first-child{font-weight:650;white-space:nowrap}
.inputs td{overflow-wrap:anywhere}.inputs td:first-child{color:var(--mut)}.inputs code{overflow-wrap:anywhere}
.opening{font-size:15.5px;max-width:70ch;padding:6px 0 10px;border-bottom:1px solid var(--line);margin-bottom:6px}.rows td:first-child{font-family:ui-monospace,Menlo,monospace;font-size:12.5px;white-space:nowrap}.rows td.from{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--mut);white-space:nowrap}
.rung{display:grid;grid-template-columns:130px 1fr;gap:12px;padding:12px 0;border-bottom:1px solid var(--line)}.rung:last-child{border-bottom:0}.rung .lvl{font-weight:650;font-size:13px}.rung .lvl small{display:block;color:var(--mut);font-weight:500;font-size:12px}
.trace{list-style:none;margin:0;padding:0 0 0 14px;border-left:2px solid var(--line)}.trace li{display:grid;grid-template-columns:110px minmax(180px,260px) 1fr;gap:12px;align-items:baseline;padding:8px 0;border-bottom:1px solid var(--line);font-size:13.5px}.trace li:last-child{border-bottom:0}
.wmap{table-layout:fixed}.wmap th,.wmap td{font-size:12.5px;padding:7px;overflow-wrap:break-word}.wmap th{white-space:normal}.wmap th:first-child{width:13%}.wmap th:last-child{width:19%}.wmap .idtag{display:block;margin:0 0 3px}
.idtag{font:12px ui-monospace,Menlo,monospace;color:var(--mut)}.tree-title{margin-top:26px}
.treebox{--w:clamp(280px,40vw,560px);border:1px solid var(--line);border-radius:9px;overflow:hidden;margin:6px 0 12px}
.tree-head{display:flex;background:var(--soft);border-bottom:1px solid var(--line);font:700 11px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.03em;color:var(--mut)}
.tree-head>span:first-child{flex:1 1 auto;padding:7px 12px;min-width:0;overflow-wrap:anywhere}.tree-head>span:last-child{flex:0 0 var(--w);padding:7px 12px;border-left:1px solid var(--line);display:flex;align-items:center;gap:5px;flex-wrap:wrap}.tree-head .tn-note{text-transform:none;letter-spacing:0;font-weight:500;font-size:12px}
ul.tree,ul.tree ul{list-style:none;margin:0;padding:0 0 0 20px;position:relative}ul.tree{padding:4px 0 4px 6px}ul.tree ul::before{content:'';position:absolute;left:6px;top:0;bottom:12px;border-left:1.5px solid var(--line)}
ul.tree li{position:relative;margin:0;min-width:0}ul.tree ul>li::before{content:'';position:absolute;left:-14px;top:15px;width:12px;border-top:1.5px solid var(--line)}
details.tn{margin:0;min-width:0}details.tn>summary,.tn-file{display:flex;align-items:stretch;min-width:0;padding:0 0 0 6px}details.tn>summary{cursor:pointer;list-style:none}details.tn>summary::-webkit-details-marker{display:none}details.tn>summary:hover,.tn-file:hover{background:var(--soft)}
.tn-name{flex:1 1 auto;min-width:0;font:500 13px/1.6 ui-monospace,Menlo,monospace;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding:4px 10px 4px 0}details.tn>summary .tn-name{font-weight:650}
.tn-works{flex:0 0 var(--w);min-width:0;padding:5px 12px;border-bottom:1px solid var(--line);border-left:1px solid var(--line)}.tn-top{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;min-height:21px}
.tn-note{font-size:13px;line-height:1.5;opacity:.85;overflow-wrap:anywhere}.idtag.rt{color:var(--acc);border:1px solid var(--acc);border-radius:999px;padding:0 8px;font-size:11.5px;line-height:1.7;white-space:nowrap}.tn-more{color:var(--mut);font-size:12.5px;padding:2px 8px}
details.tn>summary .tn-name:before{content:'▸ ';color:var(--mut)}details.tn[open]>summary .tn-name:before{content:'▾ '}.tn-file .tn-name:before{content:'  ';white-space:pre}
@media(max-width:820px){.wmap{table-layout:auto;min-width:780px}.treebox{--w:46%}}
.taxis{display:flex;align-items:flex-end;gap:3px;height:72px;border-bottom:1px solid var(--line);margin:8px 0 3px}.tday{flex:1;min-width:4px;max-width:30px;height:100%;display:flex;flex-direction:column;justify-content:flex-end}.tday:not(.on)::after{content:'';height:3px;background:var(--line);border-radius:1px}.tday i{display:block;border-radius:2px 2px 0 0}.tday i.l{background:var(--acc)}.tday i.r{background:var(--ok)}.tday.on:hover i{opacity:.7}.taxis-lab{display:flex;justify-content:space-between;color:var(--mut);font-size:12px;margin-bottom:6px}.tsec h3{margin:20px 0 6px;font-size:14.5px}.tl{list-style:none;margin:0 0 0 5px;padding:0 0 0 16px;border-left:2px solid var(--line)}.tl li{padding:5px 0;font-size:13.5px;position:relative}.tl li::before{content:'';position:absolute;left:-21px;top:12px;width:8px;height:8px;border-radius:50%;background:var(--acc)}.tl li.trun::before{background:var(--ok)}.tl summary{cursor:pointer;list-style:none}.tl summary::-webkit-details-marker{display:none}.tl details[open]>summary{font-weight:600}.tl details p{margin:6px 0 6px 22px;max-width:95ch}.tl li.tgrp{padding:10px 0 2px;color:var(--mut);font:650 11px/1.4 -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.05em}.tl li.tgrp::before{display:none}.tk{display:inline-block;width:20px;color:var(--mut)}.trun .tk{width:auto;margin-right:6px;color:var(--ok);font-weight:600}
.strip-head{flex-basis:100%;font:650 12.5px -apple-system,sans-serif;color:var(--acc)}.strip-head .mut{font-weight:400}body[data-space=scope] main>.strip,body[data-space=run] main>.strip,body[data-space=delivery] main>.strip{display:none}
.legend{width:auto;margin-top:6px;font-size:12.5px}.legend td,.legend th{padding:3px 12px 3px 0;border:0}.legend td:first-child{white-space:nowrap;font-family:ui-monospace,Menlo,monospace}
.timeline{list-style:none;margin:0;padding:0}.timeline li{display:grid;grid-template-columns:70px 70px 1fr;gap:12px;padding:7px 0;border-bottom:1px solid var(--line);font-size:13.5px}.timeline .d,.timeline .p{font:12.5px ui-monospace,Menlo,monospace;color:var(--mut)}
.limits{border-left:3px solid var(--bad);padding-left:12px;font-size:13.5px}.limits p{margin:6px 0}.note{border:1px dashed var(--line);border-radius:8px;padding:10px 12px;color:var(--mut);font-size:13px}
.source{margin-top:18px;color:var(--mut);font-size:12px}
.source-short,.nav-short{display:none}
.form{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px 16px;align-items:start}.form .full{grid-column:1/-1}.field{display:flex;flex-direction:column;gap:5px}.field label{color:var(--mut);font-size:11px;text-transform:uppercase;letter-spacing:.04em;font-weight:650}.field input,.field select,.field textarea{border:1px solid var(--line);background:var(--bg);color:var(--fg);border-radius:7px;padding:8px;font:14px -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}.field textarea{min-height:60px;resize:vertical}
.btn{border:1px solid var(--acc);border-radius:8px;padding:8px 13px;background:var(--bg);color:var(--acc);font:650 14px -apple-system,sans-serif;cursor:pointer}.btn.primary{background:var(--acc);color:#fff}.actions{display:flex;gap:10px;flex-wrap:wrap;align-items:center}.status{font-size:13px;color:var(--mut)}
@media(max-width:820px){.form{grid-template-columns:1fr}}
@media(max-width:820px){.gates{grid-template-columns:repeat(4,1fr)}.rung{grid-template-columns:1fr}.timeline li,.trace li{grid-template-columns:1fr}}
@media(max-width:600px){
body{padding:12px}h1{font-size:16px;line-height:1.3}.board-links .all-boards,.source-full,.nav-full{display:none}.source-short,.nav-short{display:inline}
.spaces{flex-wrap:nowrap;overflow-x:auto;overscroll-behavior-x:contain;-webkit-overflow-scrolling:touch;scrollbar-width:none;margin:8px 0 4px;padding:0 0 3px}.spaces::-webkit-scrollbar{display:none}.space{flex:0 0 auto;padding:5px 8px;font-size:11px}
.strip{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:3px 10px;border:0;border-top:1px solid var(--line);border-radius:0;background:transparent;padding:7px 0;margin-bottom:5px;font-size:12px}.strip-head{display:none}.strip-field br{display:none}.strip-question{grid-column:1/-1;font-size:13px;line-height:1.4}.strip-question .eyebrow{display:none}.strip-data,.strip-answer{font-size:11.5px}.strip-data .eyebrow,.strip-answer .eyebrow{text-transform:none;letter-spacing:0;font-size:11px}.strip-data .eyebrow:after,.strip-answer .eyebrow:after{content:": "}.strip-next{grid-column:1/-1;margin-top:3px}
.shell{border:0;border-radius:0;padding:0;background:transparent}.wtabs{gap:14px;padding:0 0 6px;margin:0 0 8px}.wtab{border:0;border-radius:0;padding:5px 1px;border-bottom:2px solid transparent;font-size:12px}.wtab.on{border:0;border-bottom:2px solid var(--acc)}.lead{font-size:13px;margin-bottom:8px}.note{border:0;border-radius:0;padding:4px 0}.source{margin-top:10px;font-size:11px}
}
"""

_JS = """<script>(function(){
var sp=[].slice.call(document.querySelectorAll('.space')),pn=[].slice.call(document.querySelectorAll('.pane'));
function sel(s,w){if(!document.querySelector('.pane[data-space="'+s+'"]'))s='scope';document.body.dataset.space=s;sp.forEach(function(b){b.classList.toggle('on',b.dataset.space===s)});pn.forEach(function(p){p.classList.toggle('on',p.dataset.space===s)});if(w){try{var u=new URL(location.href);u.searchParams.set('space',s);history.replaceState({},'',u)}catch(e){}}}
sp.forEach(function(b){b.onclick=function(){sel(b.dataset.space,true)}});
document.querySelectorAll('.shell').forEach(function(sh){var tabs=[].slice.call(sh.querySelectorAll('.wtab'));function sync(){var on=sh.querySelector('.wtab.on');sh.querySelectorAll('.view').forEach(function(v){v.classList.toggle('on',on&&v.dataset.view===on.dataset.view)})}tabs.forEach(function(t){t.onclick=function(){tabs.forEach(function(x){x.classList.toggle('on',x===t)});sync();try{var u=new URL(location.href);u.searchParams.set('view',t.dataset.view);history.replaceState({},'',u)}catch(e){}}});sync()});
try{var vw=new URL(location.href).searchParams.get('view');if(vw==='folders')vw='wmap';if(vw){document.querySelectorAll('.pane[data-space="'+document.body.dataset.space+'"] .wtab[data-view="'+vw+'"]').forEach(function(t){t.click()})}}catch(e){}
sel(document.body.dataset.space,false);
document.querySelectorAll('[data-insight-copy]').forEach(function(b){b.onclick=function(){
var box=b.closest('[data-insight-request]'),ta=box.querySelector('textarea'),st=box.querySelector('[role=status]');
function fallback(){box.querySelector('details').open=true;ta.focus();ta.select();st.textContent='Select and copy the request, then paste and send it in your conversation.'}
try{if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(ta.value).then(function(){st.textContent='Copied. Paste and send in your conversation. Nothing has started.'},fallback)}else{fallback()}}catch(e){fallback()}
}});
var f=document.getElementById('askform');if(f){f.onsubmit=function(ev){ev.preventDefault();var q=document.getElementById('ask-text').value.replace(/\\s+/g,' ').trim();if(!q)return;
var cmd='/haipipe-insight application '+f.dataset.root+' question "'+q.replace(/"/g,"'")+'"';document.getElementById('ask-cmd').textContent=cmd;document.getElementById('ask-out').hidden=false;
var st=document.getElementById('ask-status');if(navigator.clipboard){navigator.clipboard.writeText(cmd).then(function(){st.textContent='copied'},function(){st.textContent='select and copy the line below'})}else{st.textContent='select and copy the line below'}}}
})();</script>"""


def _pill(mark: str, text: str = "") -> str:
    cls = {"✅": "ok", "🟡": "warn", "🚫": "bad", "🧊": "acc"}.get(mark, "")
    return f'<span class="pill {cls}">{_e(text or mark)}</span>'


# The registers keep a short reason token per refused cell; the screen says
# what it means.  Meanings from MT02/MT03's legends and FK05's rows.
_REASONS = {
    "F-only": ("full data only", "needs the whole extract, so it is answered once on F"),
    "thin": ("too few rows", "fewer than 300 rows per message in this cut"),
    "defer": ("board-wide", "asks whether to segment, so it is answered once for the board"),
    "nomeas": ("not measured", "no field in the extract records it"),
    "nocon": ("no contrast", "the experiment never varies it"),
    "noiden": ("not identifiable", "13 messages cannot separate it"),
}


def _cell_text(cell: dict) -> str:
    """A register cell in plain words: `🚫 thin` -> `🚫 too few rows`."""
    if cell["mark"] == "🚫" and not cell["page"] and cell["note"] in _REASONS:
        return f'🚫 {_REASONS[cell["note"]][0]}'
    return cell["raw"] or "·"


def _clip(text: str, n: int) -> str:
    """Cut at a word boundary, never inside a word ("Gen 1 still car")."""
    if len(text) <= n:
        return text
    return text[:n].rsplit(" ", 1)[0].rstrip(" ·,;") + " …"


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
    projection = selected_specs(snap, qid, pid)
    # Run Space and Delivery Space are always the last two (JL 260916).
    return _spell_ids(snap, "".join([
        '<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">',
        f'<title>🔎 {_e(snap["title"])}</title><style>{_CSS}</style></head><body data-space="{_e(space)}"><main>',
        _render_header(snap),
        _render_nav(),
        _render_strip(snap, view, qid, pid),
        f'<section class="pane" data-space="scope"><div class="shell">{_with_work_lines(_render_scope(snap, qid, pid), snap, "scope")}</div></section>',
        f'<section class="pane" data-space="insight"><div class="shell">{_with_work_lines(_render_insight(snap, view, qid, pid, projection), snap, "insight")}</div></section>',
        f'<section class="pane" data-space="evidence"><div class="shell">{_with_work_lines(_render_evidence(snap, view, projection), snap, "evidence")}</div></section>',
        f'<section class="pane" data-space="check"><div class="shell">{_with_work_lines(_render_check(snap, view, qid, pid), snap, "check")}</div></section>',
        f'<section class="pane" data-space="run"><div class="shell">{_with_work_lines(_render_run(snap, projection), snap, "run")}</div></section>',
        f'<section class="pane" data-space="delivery"><div class="shell">{_with_work_lines(_render_delivery(snap, projection), snap, "delivery")}</div></section>',
        "</main>", _JS, "</body></html>",
    ]))


_PAGE_CODE = re.compile(r"(?<![/\w])([A-Z])([DIKW])(\d{2})(?![\w/-])")


def display_id(pid: str, partitions: dict[str, str]) -> str:
    """`FD02` -> `full-D02`, `BI07` -> `young-male-I07` (JL 260918).  The
    first letter is spelled as its data cut; the level letter and number stay.
    Files keep `FD02`: only the screen changes."""
    hit = _PAGE_CODE.fullmatch(pid)
    if not hit or hit.group(1) not in partitions:
        return pid
    return f'{_pretty(partitions[hit.group(1)]).replace(" ", "-")}-{hit.group(2)}{hit.group(3)}'


def _spell_ids(snap: dict, page_html: str) -> str:
    """Spell every page code in the TEXT of a rendered page.  Tags and their
    attributes keep the code (a link's `page=FW01` is what the server reads),
    and so does a code inside a path or a folder name (`1-F-full/FW01-...`)."""
    parts = {p["id"]: p["name"] for p in snap["partitions"]}
    out, skip = [], False
    for chunk in re.split(r"(<[^>]+>)", page_html):
        if chunk.startswith("<"):
            skip = chunk[1:7].lower() in ("script", "style>") or (skip and not chunk.startswith("</"))
            out.append(chunk)
        else:
            out.append(chunk if skip else _PAGE_CODE.sub(lambda m: display_id(m.group(0), parts), chunk))
    return "".join(out)


def _render_header(snap: dict) -> str:
    if snap["static"]:
        links = '<a class=board-index href="index.html">board index</a>'
    else:
        links = (f'<a class=all-boards href="/">all boards</a> · '
                 f'<a class=board-index href="/{_e(snap["relative"])}/board/index.html">board index</a>')
    # JL 260921: the title and the two links, nothing else. The counts were a
    # line nobody read; every count still stands where it is used.
    return (f'<header><h1>🔎 {_e(snap["title"])}</h1>'
            f'<div class="mut board-links">{links}</div></header>')


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
                       f'<td>{_e(level)}</td><td>{_pill(page["state"][:1], _clip(page["state"], 70))}</td></tr>')
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


def _copy_insight_request(prompt: str) -> str:
    # Numeric entities keep the display-id formatter from rewriting identifiers
    # in the copyable request. The browser decodes them into the original text.
    encoded = "".join(f"&#{ord(char)};" for char in prompt)
    return ('<div data-insight-request><button class=btn type=button data-insight-copy>'
            'Copy request → paste and send</button> '
            '<span class=status role=status aria-live=polite>Copying does not send, start, allocate, or write a Run.</span>'
            '<details><summary>Request text</summary>'
            f'<textarea readonly rows=10 cols=90 aria-label="Insight Run request">{encoded}</textarea></details></div>')


def _render_selected_specs(snap: dict, projection: dict, space: str, *, read_only: bool = False) -> str:
    items = [item for item in projection["items"] if space == "all" or item["space"] == space]
    heading = f'Owed Run Specs · {projection["question"]} × {projection["partition"]}'
    parts = [f'<h3>{_e(heading)}</h3><p class=mut>Selected by the frozen workflow for this cell. '
             'A Spec describes work; the matching native Run, when allocated, is shown separately.</p>']
    if not items:
        parts.append('<p class=note>No owed Run Spec is recorded for this selection in this Space.</p>')
    for item in items:
        matches = '; '.join(f'{r["run_id"]} · {r["status"]} · {r.get("participation", "managed")}'
                            for r in item["matches"]) or 'No matching native Run recorded'
        allowed = 'Shown here · read-only' if read_only else 'Copy request → paste and send'
        parts.append(f'<h4>{_e(item["name"])}</h4><p>Run Type: <code>{_e(item["type"])}</code> '
                     f'· Spec: <code>{_e(item["spec"]["id"])}</code></p>'
                     f'<p>{_e(item["purpose"])}</p><p>Target: {_e(item["target"])}</p>'
                     f'<p>Owner Skill: <code>{_e(item["owner"])}</code> · '
                     f'Worker Skill(s): <code>{_e(item["workers"])}</code> · Actor: {_e(item["actor"])}</p>'
                     '<details><summary>Prerequisites and current work</summary><ul>'
                     + ''.join(f'<li>{_e(text)}</li>' for text in item['prerequisites'])
                     + f'</ul><p>Matching Run/status: {_e(matches)}</p><p>Workflow state: {_e(item["state"])}</p>'
                     f'<p>Runtime: {_e(item["runtime"]["id"])} · Definition: {_e(item["runtime"]["definition"])}</p></details>'
                     f'<p><b>{allowed}</b> · {_e(item["next_action"])}</p>')
        if not read_only:
            parts.append(_copy_insight_request(insight_request_text(snap, projection, item)))
    parts.extend(f'<p class=note>{_e(note)}</p>' for note in projection['notes'])
    return ''.join(parts)


def _next_step(snap: dict, view: dict, qid: str, pid: str) -> str:
    """What to do about the selected cell, as one line: a page to open or a
    command to hand to Claude Code.  The page reads; the skill writes."""
    cell, page = view["cell"], view["page"]
    cmd = f"/haipipe-insight application {snap['relative']} chain {qid} {pid}"
    stop = next((g for g in view["gates"][1:] if g["state"] in {"held", "pending"}), None)
    if cell["mark"] == "✅":
        return f'done · read {_link(snap, page)}' if page else 'answer recorded · resolve the missing Page reference'
    if cell["mark"] == "🟡" and "final" in cell.get("note", ""):
        return 'partial-final answer recorded · read its licensing reason and receipts'
    if cell["mark"] == "🚫":
        return f'refused: {_e(_REASONS.get(cell["note"], (cell["note"] or cell["raw"],))[0])} · nothing to run'
    if cell["mark"] == "·":
        return 'not asked on this data · use <b>Ask</b> in Scope Space'
    where = f' · stopped at {stop["key"]} {stop["name"]}' if stop else ""
    projection = selected_specs(snap, qid, pid)
    return (f'Execution entry: <code>{_e(cmd)}</code>{where}'
            + _copy_insight_request(insight_request_text(snap, projection)))


def _render_nav() -> str:
    tabs = (("scope", "Scope Space", "Scope"), ("insight", "Insight Space", "Insight"),
            ("evidence", "Evidence Space", "Evidence"), ("check", "Check Space", "Check"),
            ("run", "Run Space", "Runs"), ("delivery", "Delivery Space", "Delivery"))
    return '<nav class=spaces>' + "".join(
        f'<button class=space type=button data-space="{k}" aria-label="{label}" title="{label}">'
        f'<span class=nav-full>{label}</span><span class=nav-short>{short}</span></button>'
        for k, label, short in tabs) + '</nav>'


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
    answer = _cell_text(cell) if cell["mark"] != "·" else "not asked on this data"
    pick = ("" if snap["static"] else
            f' · <a href="{_e(_cell_url(snap, qid, pid, "scope"))}">pick another cell in Scope Space</a>')
    terminal = cell["mark"] in {"✅", "🚫"} or (cell["mark"] == "🟡" and "final" in cell.get("note", ""))
    next_step = ("" if terminal else
                 f'<div class=strip-next><span class=eyebrow>Next</span><br>{_next_step(snap, view, qid, pid)}</div>')
    return (f'<div class=strip><div class=strip-head>Selected cell <span class=mut>· the one question × data cut '
            f'this Space is about{pick}</span></div>'
            f'<span class="strip-field strip-question"><span class=eyebrow>Question</span><br><span class=id>{_e(qid)}</span> · {_e(_LEVEL_LABEL.get(qid[1], ""))} · {_e(row["question"])}</span>'
            f'<span class="strip-field strip-data"><span class=eyebrow>Data</span><br>{_e(_partition_label(snap, pid))}</span>'
            f'<span class="strip-field strip-answer"><span class=eyebrow>Answer</span><br>{_pill(cell["mark"], answer)}</span>'
            f'{next_step}</div>')


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
    return ('<h2>Input data</h2><p class=lead>The one prepared extract every page on this board reads. '
            'The board reads it and never owns or changes it, and no page may cite a number that is not in it.</p>'
            f'<table class="rows inputs">{body}</table>')


def _render_scope(snap: dict, qid: str, pid: str) -> str:
    cols = [p for p in ("F", "B", "C", "D", "E", "G", "X")
            if any(p in q["cells"] for q in snap["questions"])]
    parts = {p["id"]: p["name"] for p in snap["partitions"]}
    # "✅ midlife-female-I03" stays on one line; only a note such as "final" wraps
    def cell_html(c):
        if c["page"]:
            return (f'<span class=nw>{_e(c["mark"])} {_e(display_id(c["page"], parts))}</span>'
                    + (f' {_e(c["note"])}' if c["note"] else ""))
        return f'<span class=nw>{_e(_cell_text(c))}</span>'
    rows, last = [], ""
    for q in snap["questions"]:
        lv = q["id"][1]
        if lv != last:
            rows.append(f'<tr class=group><td colspan={len(cols) + 2}>{_e(_LEVEL_LABEL[lv])} · {_e(q["register"]["path"].stem)}</td></tr>')
            last = lv
        cells = ""
        for p in cols:
            c = q["cells"].get(p, {"mark": "·", "page": "", "note": "", "raw": "·"})
            on = " sel" if (q["id"] == qid and p == pid) else ""
            cells += f'<td class="cell{on}"><a href="{_e(_cell_url(snap, q["id"], p))}">{cell_html(c)}</a></td>'
        rows.append(f'<tr><td class=mono>{_e(q["id"])}</td><td class=q>{_e(q["question"])}</td>{cells}</tr>')
    # JL 260921: the grid alone. The marks are read in the cells, and a refused
    # cell already carries its reason beside it.
    register = ('<h2>Question register</h2><p class=lead>One row per question, one column per partition, as written in MT01 to MT04. Click a cell.</p>'
                f'<div class=scroll><table class=grid><tr><th>Id</th><th>Question</th>{"".join(f"<th>{p}<br><span class=pn>{_e(_partition_name(snap, p) or p)}</span></th>" for p in cols)}</tr>{"".join(rows)}</table></div>')
    prow = "".join(
        f'<tr><td><b>{_e(r["id"])}</b></td><td>{_e(_pretty(r["name"]))}</td><td class=mono>{_e(r["where"] or "—")}</td>'
        f'<td class=num>{_e(r["rows"] or "—")}</td><td class=num>{_e(r["share"] or "—")}</td><td class=num>{r["pages"]}</td></tr>'
        for r in snap["partitions"])
    partition = ('<h2>Partitions</h2><p class=lead>How the extract is cut, from MT00. A partition is one config, never a code change. '
                 'Every question is asked once per partition.</p>'
                 f'<div class=scroll><table><tr><th>Id</th><th>Partition</th><th>Where</th><th>Rows</th><th>Share</th><th>Pages</th></tr>{prow}</table></div>')
    # One box.  The person asks in plain words; Claude Code decides the answer
    # level, the partitions and the lineage, then writes the register row
    # through `python3 -m live.insightboard ask ...`.
    ask = (
        '<h2>Ask</h2><p class=lead>Type the question. Claude Code decides what kind of answer it needs, which data cuts it runs on, and what it grew out of, then registers it.</p>'
        f'<form id=askform class=form data-root="{_e(snap["relative"])}">'
        '<div class="field full"><textarea id=ask-text required placeholder="e.g. does the send hour change which message works best?"></textarea></div>'
        '<div class="full actions"><button class="btn primary" type=submit>Ask</button><span class=status id=ask-status></span></div></form>'
        '<div id=ask-out hidden><p class=mut>Give this to Claude Code (copied to your clipboard):</p><p><code id=ask-cmd></code></p></div>')
    # JL 260921: the input data first, then the cut, then the questions.
    return (_tabs([("data", "Data"), ("partition", "Partition"), ("register", "Register"),
                   ("ask", "Ask"), ("pages", "Pages")])
            + _view("data", _render_input_data(snap), True) + _view("partition", partition)
            + _view("register", register) + _view("ask", ask)
            + _view("pages", _render_pages(snap)))


def _workflow_runtimes(board: Path) -> list[dict]:
    """Read aggregate projections without writing or inventing native Runs."""
    records = []
    for path in sorted((board / "_runs" / "insight").glob("*/runtime.yaml")):
        record = {"path": path.relative_to(board).as_posix(),
                  "id": path.parent.name, "runs": [], "frontier": [],
                  "resource_controls": [], "error": ""}
        try:
            import yaml
        except ImportError:
            record["error"] = "PyYAML is required to read the workflow record"
            records.append(record)
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or data.get("schema") != "haipipe.workflow-runtime/v1":
                raise ValueError("unsupported workflow record schema")
            if data.get("workflow_id") != "haipipe-insight-workflow":
                raise ValueError("workflow owner is not haipipe-insight-workflow")
            if data.get("workflow_runtime_id") != path.parent.name:
                raise ValueError("workflow runtime id does not match its record directory")
            runs, frontier = data.get("runs"), data.get("frontier", [])
            resource_controls = data.get("resource_controls", [])
            if not isinstance(runs, list) or not isinstance(frontier, list):
                raise ValueError("runs and frontier must be lists")
            seen = set()
            for run in runs:
                required = ("run_id", "owner", "status", "result", "receipt")
                if isinstance(run, dict) and run.get("participation") != "reused":
                    required += ("run_spec_id", "ticket")
                if not isinstance(run, dict) or any(
                    not isinstance(run.get(key), str) or not run[key].strip() for key in required
                ):
                    raise ValueError("Run row lacks native identity, owner, state or record paths")
                if run["run_id"] in seen:
                    raise ValueError(f"duplicate native Run id: {run['run_id']}")
                seen.add(run["run_id"])
            if any(not isinstance(item, dict) for item in frontier):
                raise ValueError("frontier entries must be target records")
            if not isinstance(resource_controls, list) or any(
                not isinstance(item, dict) for item in resource_controls
            ):
                raise ValueError("resource_controls must be control records")
            record.update({"status": data.get("status", "not recorded"),
                           "definition": data.get("definition_ref", "not recorded"),
                           "definition_hash": data.get("definition_hash", ""),
                           "requested_answer_targets": data.get("requested_answer_targets", []),
                           "runs": runs, "frontier": frontier,
                           "resource_controls": resource_controls})
        except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
            record["error"] = str(exc)
        records.append(record)
    return records


def _render_runtime_inventory(snap: dict) -> str:
    records = snap.get("workflow_runtimes", [])
    if not records:
        return ('<h2>Workflow Runs</h2><p class=note>No aggregate workflow record yet. '
                'Resource kinds and Question Groups do not establish Run allocations.</p>')
    parts = ['<h2>Workflow Runs</h2><p>Recorded native identities and dependencies for each execution. '
             'Native Results and receipts own their outcomes.</p>']
    for record in records:
        parts.append(f'<h3>{_e(record["id"])}</h3><p class=mono>{_e(record["path"])}</p>')
        if record["error"]:
            parts.append(f'<p class=note>Cannot read workflow inventory: {_e(record["error"])}</p>')
            continue
        parts.append(f'<p>Status: {_e(record["status"])} · Definition: {_e(record["definition"])} '
                     f'· {len(record["runs"])} recorded Runs</p>')
        if record["runs"]:
            try:
                specs = {spec["id"]: spec for spec in read_insight_definition(Path(snap["board"]), record)["run_specs"]}
            except Exception as exc:
                specs = {}
                parts.append(f'<p class=note>Spec metadata unavailable: {_e(exc)}. Native inventory remains visible.</p>')
            rows = []
            for run in record["runs"]:
                spec = specs.get(run.get("run_spec_id"), {})
                metadata = {**spec, **run}
                workers, actor = run_people(metadata)
                purpose = run.get("purpose") or spec.get("purpose") or spec.get("action") or run.get("target")
                prerequisites = {"entry": spec.get("entry", "not recorded"),
                                 "inputs": run.get("inputs", spec.get("inputs", "not recorded")),
                                 "dependencies": run.get("depends_on", spec.get("depends_on", []))}
                identity = (f'<b>{_e(run_reader_name(metadata))}</b><br>Run Type: '
                            f'<code>{_e(run.get("run_type") or spec.get("run_type") or "not recorded")}</code>'
                            f'<br><code>{_e(run["run_id"])}</code><br>Spec: '
                            f'{_e(run.get("run_spec_id") or "reused external dependency")}')
                owner = f'Owner: {_e(run["owner"])}<br>Worker Skill(s): {_e(workers)}<br>Actor: {_e(actor)}'
                status = f'{_e(run["status"])} · {_e(run.get("participation", "not recorded"))}'
                paths = (f'Ticket: {_e(run.get("ticket", "not recorded"))}<br>'
                         f'Result: {_e(run["result"])}<br>Receipt: {_e(run["receipt"])}')
                rows.append('<tr><td>' + identity + '</td><td>' + _e(describe_run_field(purpose))
                            + '<br>Target: ' + _e(describe_run_field(run.get("target", spec.get("target"))))
                            + '</td><td>' + owner + '</td><td>' + _e(describe_run_field(prerequisites))
                            + '</td><td>Shown here · read-only</td><td>' + status + '</td><td>' + paths + '</td></tr>')
            headings = ("Run name, Type and identity", "Bounded work", "Skills and actor", "Prerequisites", "This Space", "Recorded status", "Native records")
            parts.append('<div class=scroll><table><tr>' + ''.join(f'<th>{h}</th>' for h in headings)
                         + '</tr>' + ''.join(rows) + '</table></div>')
        else:
            parts.append('<p>No allocated Runs in this execution; control-only work is recorded separately.</p>')
        if record["resource_controls"]:
            parts.append('<h4>Resource controls</h4><ul>')
            for item in record["resource_controls"]:
                parts.append(f'<li>{_e(item.get("key", "control action"))} · '
                             f'{_e(item.get("target", ""))} · {_e(item.get("status", "not recorded"))} · '
                             f'{_e(item.get("receipt", "receipt not recorded"))}</li>')
            parts.append('</ul>')
        if record["frontier"]:
            parts.append('<h4>Ready and waiting work</h4><ul>')
            for item in record["frontier"]:
                parts.append(f'<li>{_e(item.get("run_spec_id", "control action"))} · '
                             f'{_e(item.get("target", ""))} · {_e(item.get("state", "not recorded"))} · '
                             f'{_e(item.get("waiting_on", []))}</li>')
            parts.append('</ul>')
    return ''.join(parts)


def _render_run(snap: dict, projection: dict | None = None) -> str:
    runs = snap["runs"]
    if runs:
        body = "".join(
            f'<tr><td class=mono>{_e(r["task"] or "?")} · {_e(_pretty(r["call"]) if r["call"] else "?")}</td><td>{_link(snap, r["page"])}</td>'
            f'<td>{_pill("✅" if r["status"] == "ok" else "🚫", r["status"])}</td><td class=mono>{_e(r["started"].replace("T", " ")[:16])}</td>'
            f'<td class=num>{_e(r["duration"] + " s" if r["duration"] else "")}</td><td class=mono>{_e(r["git"])}</td>'
            f'<td class=mono>{_e(r["rel"]) if r["found"] else _e(r["rel"]) + " · not found in store"}</td></tr>'
            for r in runs)
        ledger = f'<div class=scroll><table><tr><th>Run</th><th>Named by</th><th>Status</th><th>Started</th><th>Took</th><th>Git</th><th>Receipt</th></tr>{body}</table></div>'
    else:
        ledger = '<p class=note>No page on this board names a run receipt yet. A D page names one with a <code>run receipt</code> line or a <code>receipt:</code> header.</p>'
    ledger = (_render_runtime_inventory(snap) + '<h2>Page-referenced Supporting receipts</h2>'
              '<p class=lead>Shown here · read-only. Historical source receipts named by Pages, read from the store. '
              'Their canonical Run Type, owner/worker Skills, actor and prerequisites are not recorded in this legacy projection; '
              'consult the native Ticket and receipt. These rows do not offer a new Run.</p>' + ledger)
    # The Folders table became the Workflow map's folder tree (the paper board's
    # shape); an old `view=folders` link opens the map.
    return (_tabs([("ledger", "Runs"), ("timeline", "Timeline"), ("who", "Who does it"), ("wmap", "Workflow map")])
            + _view("ledger", ledger, True) + _view("timeline", _render_timeline(snap))
            + _view("who", _render_who(snap)) + _view("wmap", _render_workflow_map(snap, projection)))


def _render_timeline(snap: dict) -> str:
    """A day axis, then one section per working day, newest first: each page
    changed that day on one line (its first log sentence, the rest on click),
    and the runs that ran that day.  JL 260918: a list of 219 log paragraphs
    is not a timeline."""
    days: dict[date, dict] = {}
    for ev in snap["events"]:
        try:
            day = datetime.strptime(ev["date"], "%y%m%d").date()
        except ValueError:
            continue
        days.setdefault(day, {"logs": [], "runs": []})["logs"].append(ev)
    for run in snap["runs"]:
        try:
            day = date.fromisoformat(run["started"][:10])
        except ValueError:
            continue
        days.setdefault(day, {"logs": [], "runs": []})["runs"].append(run)
    if not days:
        return '<h2>Timeline</h2><p class=note>No dated <code>## Log</code> line and no run on this board yet.</p>'

    first, last = min(days), max(days)
    peak = max(len(v["logs"]) + len(v["runs"]) for v in days.values())
    axis = []
    for i in range((last - first).days + 1):
        day = first + timedelta(days=i)
        v = days.get(day)
        if not v:
            axis.append('<span class=tday></span>')
            continue
        n_log, n_run = len(v["logs"]), len(v["runs"])
        tip = f'{day:%a %d %b} · {n_log} change{"" if n_log == 1 else "s"} · {n_run} run{"" if n_run == 1 else "s"}'
        axis.append(f'<a class="tday on" href="#day-{day:%y%m%d}" title="{tip}">'
                    f'<i class=r style="height:{max(6, round(64 * n_run / peak)) if n_run else 0}px"></i>'
                    f'<i class=l style="height:{max(6, round(64 * n_log / peak)) if n_log else 0}px"></i></a>')
    ticks = f'<div class=taxis-lab><span>{first:%d %b}</span><span>{last:%d %b %Y}</span></div>'

    folder_word = {p["folder"]: ("comparisons across the data cuts" if p["id"] == "X" else f'{_pretty(p["name"])} data')
                   for p in snap["partitions"]}
    folder_word["0-MT-meta"] = "meta and question registers"
    sections = []
    for day in sorted(days, reverse=True):
        v = days[day]
        by_page: dict[str, list] = {}
        for ev in v["logs"]:
            by_page.setdefault(ev["page"]["id"], []).append(ev)
        rows = []
        groups: dict[tuple, list] = {}      # one line per task and page: six calls of one task read as one
        for run in sorted(v["runs"], key=lambda r: r["started"]):
            groups.setdefault((run["task"], run["page"]["id"]), []).append(run)
        for (task, _pid), runs in groups.items():
            status = "all ok" if all(r["status"] == "ok" for r in runs) else " · ".join(r["status"] for r in runs)
            secs = sum(float(r["duration"] or 0) for r in runs)
            what = f'{len(runs)} runs of' if len(runs) > 1 else "run"
            rows.append(f'<li class=trun><span class=tk>▶ {what}</span><span class=mono>{_e(task.split("/")[-1])}</span> '
                        f'· {_e(", ".join(_pretty(r["call"]) for r in runs))} <span class=mut>· {_e(status)} · '
                        f'{_e(runs[0]["started"][11:16])} · {secs:g} s · for {_link(snap, runs[0]["page"])}</span></li>')
        last_folder = ""
        for pid in sorted(by_page, key=lambda p: by_page[p][0]["page"]["rel"]):
            evs = by_page[pid]
            folder = evs[0]["page"]["rel"].split("/")[0]
            if folder != last_folder:
                rows.append(f'<li class=tgrp>{_e(folder_word.get(folder, folder))}</li>')
                last_folder = folder
            first_line = re.split(r"(?<=[.;])\s", evs[0]["text"], 1)[0]
            more = f' <span class=mut>· {len(evs) - 1} more</span>' if len(evs) > 1 else ""
            body = "".join(f'<p>{_inline(ev["text"])}</p>' for ev in evs)
            rows.append(f'<li><details><summary><span class=tk>✎</span>{_link(snap, evs[0]["page"])} '
                        f'<span>{_inline(_clip(first_line, 130))}</span>{more}</summary>{body}</details></li>')
        n_pages = len(by_page)
        head = " · ".join(x for x in (
            f'{len(v["logs"])} change{"" if len(v["logs"]) == 1 else "s"} on {n_pages} page{"" if n_pages == 1 else "s"}' if v["logs"] else "",
            f'{len(v["runs"])} run{"" if len(v["runs"]) == 1 else "s"}' if v["runs"] else "") if x)
        sections.append(f'<section class=tsec id="day-{day:%y%m%d}"><h3>{day:%a %d %b %Y} <span class=mut>· {head}</span></h3>'
                        f'<ul class=tl>{"".join(rows)}</ul></section>')
    total, n_runs = sum(len(v["logs"]) for v in days.values()), sum(len(v["runs"]) for v in days.values())
    return ('<h2>Timeline</h2><p class=lead>Each bar is one working day: blue for page changes, green for runs. '
            f'Click a bar to jump to that day. {total} changes and {n_runs} runs over {len(days)} days, newest first below.</p>'
            f'<div class=taxis>{"".join(axis)}</div>{ticks}{"".join(sections)}')


def _tasks_root(snap: dict) -> Path:
    return next((parent / "tasks" for parent in snap["board"].parents
                 if (parent / "tasks").is_dir()), snap["board"].parent.parent / "tasks")


def _task_calls(snap: dict) -> list[dict]:
    """Project actual native addresses first, then declared Job store routes.

    A consumer override is known only from its recorded Ticket/Result/receipt;
    never infer it from this process's environment or a stale Task config.
    """
    tasks_root = _tasks_root(snap).resolve()
    calls, seen = [], set()

    def absolute(value):
        path = Path(value)
        return path if path.is_absolute() else snap["root"] / path

    def add(task, name, ticket, receipt, source):
        if str(ticket.resolve()) in seen:
            return
        seen.add(str(ticket.resolve()))
        rel = task.relative_to(tasks_root)
        calls.append({"family": rel.parts[0], "job": task.parent.name if len(rel.parts) > 2 else "",
                      "task": task.name, "call": name, "task_path": task, "source": source,
                      "ticket": ticket, "receipt": receipt, "script": ticket.is_file(),
                      "ran": receipt.is_file()})

    for runtime in snap.get("workflow_runtimes", []):
        for run in runtime.get("runs", []):
            ticket, receipt = absolute(run["ticket"]), absolute(run["receipt"])
            task = ticket.parent.parent
            if ticket.parent.name == "runs" and task.resolve().is_relative_to(tasks_root):
                add(task.resolve(), ticket.stem, ticket, receipt, "native-receipt")
    if not tasks_root.is_dir():
        return calls
    board_store = snap.get("store_path")
    for cfg in sorted(tasks_root.glob("*/*/*/scripts/config/*.yaml")):
        task = cfg.parents[2]
        job = task.parent
        store = _field(_read(job / "src/config-defaults.yaml"), "store")
        if not store or board_store is None or absolute(store).resolve() != board_store.resolve():
            continue
        output_root = absolute(store) / job.relative_to(tasks_root)
        add(task, cfg.stem, task / "runs" / f"{cfg.stem}.sh",
            output_root / task.name / "results" / cfg.stem / "runtime.yaml", "job-default")
    # Old two-level config banks remain readable as a labelled import only.
    store = (snap.get("store") or "").rstrip("/")
    for cfg in sorted(tasks_root.glob("*/*/configs/*.yaml")):
        hit = re.search(r"(?m)^store:\s*(\S+)", _read(cfg))
        if not hit or hit.group(1).rstrip("/") != store:
            continue
        task_dir = cfg.parent.parent
        result = (snap["store_path"] / task_dir.parent.name / task_dir.name / "results" / cfg.stem / "runtime.yaml"
                  if snap["store_path"] else None)
        if result:
            add(task_dir, cfg.stem, task_dir / "runs" / f"{cfg.stem}.sh", result, "legacy-config")
    return calls


# Resource ownership × Space columns. These rows do not allocate or count Runs.
_WORKFLOW_MAP = (
    ("Meta", "MT00", "meta", ("set · data cuts, extract, thresholds · Data tab", "—",
                                 "read · the extract, last line of the trace", "gate GI0 · meta ready",
                                 "log · MT00's dated lines", "—")),
    ("Question", "MT01 – MT04", "question", ("ask · one row per question, one cell per data cut · Register, Ask",
                                               "read · the chosen question on the top strip", "—",
                                               "gate GI1 · question registered · GI6 · cell settled",
                                               "log · the registers' dated lines", "—")),
    ("Supporting Task", "tasks/…/runs/<call>.sh", "task", ("—", "—", "read · the run line: status, git, seconds",
                                                    "GI2 for produced sources · exact accepted native Result/receipt",
                                                    "run · writes results/<call>/runtime.yaml · Runs tab", "—")),
    ("Data", "D pages", "data", ("cell · ✅ full-D02", "answer · the counts, D rows", "hop · data line, bound to exact source evidence",
                                    "gate GI2 · data observed", "named by · Runs table", "—")),
    ("Information", "I pages", "information", ("cell · ✅ full-I05", "answer · the results, I rows", "hop · information lines",
                                                  "gate GI3 · information derived", "log · Timeline", "—")),
    ("Knowledge", "K pages · X verdict", "knowledge", ("cell · ✅ full-K02", "answer · claims with their strength, K rows",
                                                          "hop · knowledge line", "gate GI4 · knowledge claimed", "log · Timeline", "—")),
    ("Wisdom", "W pages", "wisdom", ("cell · ✅ full-W01", "answer · DO and DO NOT rules · Limits tab",
                                        "hop · first line of the trace", "gate GI5 · signed by a person", "log · Timeline",
                                        "out · current signed payload + GI6 settlement")),
)
_FOLDER_KIND = {slot: name for name, _, slot, _ in _WORKFLOW_MAP}


def _page_slot(page: dict) -> str:
    if page["id"] == "MT00":
        return "meta"
    if page["id"].startswith("MT"):
        return "question"
    return page["level"]


def _slot_folders(snap: dict) -> dict[str, list[tuple[str, str]]]:
    """Each map slot → the real folders it lands in on this board, with a count."""
    out: dict[str, list[tuple[str, str]]] = {slot: [] for slot in _FOLDER_KIND}
    for page in snap["pages"]:
        if page["id"].startswith("MT"):
            out[_page_slot(page)].append((page["rel"].rsplit("/", 1)[0] + "/", ""))
    for level in _LEVELS:
        tops: dict[str, int] = {}
        for page in snap["pages"]:
            if page["level"] == level and page["partition"]:
                top = page["rel"].split("/", 1)[0]
                tops[top] = tops.get(top, 0) + 1
        out[level] = [(f"{top}/", str(n)) for top, n in sorted(tops.items())]
    calls = _task_calls(snap)
    for family in sorted({c["family"] for c in calls}):
        out["task"].append((f"tasks/{family}/", _plural(sum(c["family"] == family for c in calls), "call")))
    if snap["store"] and calls:
        out["task"].append((f'{snap["store"].rstrip("/")}/', _plural(sum(c["ran"] for c in calls), "result")))
    return out


_TREE_SKIP = {"__pycache__", ".git", "node_modules"}
_TREE_LEAF = {"board": "the built site, generated; never edited", "_archive": "parked records, not read"}
_TREE_FILES = 40          # a folder with more files than this lists a count, not the files


def _size(path: Path) -> str:
    try:
        n = float(path.stat().st_size)
    except OSError:
        return ""
    for unit in ("B", "KB", "MB"):
        if n < 1024 or unit == "MB":
            return f"{int(n)} B" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024.0
    return ""


def _plural(n: int, word: str) -> str:
    return f'{n} {word}{"" if n == 1 else "s"}'


def _tnode(name: str, path: Path, is_dir: bool, chips=(), note: str = "", kids=(), opened: bool = False,
           more: int = 0) -> dict:
    return {"name": name, "path": path, "dir": is_dir, "chips": list(chips), "note": note,
            "kids": list(kids), "open": opened, "more": more}


def _entries(path: Path) -> list[Path]:
    return sorted((x for x in path.iterdir() if not x.name.startswith(".") and x.name not in _TREE_SKIP),
                  key=lambda x: (x.is_file(), x.name.lower()))


def _walk(path: Path, depth: int) -> tuple[list[dict], int]:
    """Every child of a folder, folders first.  A folder opens while depth > 0
    (below that it is a closed count); files list up to _TREE_FILES."""
    kids, hidden, files = [], 0, 0
    if not path.is_dir():
        return kids, hidden
    for x in _entries(path):
        if x.is_dir():
            sub, more = _walk(x, depth - 1) if depth > 0 else ([], 0)
            kids.append(_tnode(x.name + "/", x, True, note=_plural(len(_entries(x)), "item"), kids=sub, more=more))
        elif files < _TREE_FILES:
            kids.append(_tnode(x.name, x, False, note=_size(x)))
            files += 1
        else:
            hidden += 1
    return kids, hidden


def _board_tree(snap: dict) -> list[dict]:
    """The board folder as it is on disk: every page folder carries its resource
    kind; a data-cut folder carries the resource kinds inside it."""
    board = snap["board"]
    by_dir = {p["path"].parent: p for p in snap["pages"]}
    cuts = {row["folder"] for row in snap["partitions"]}
    roots = []
    for x in sorted(_entries(board), key=lambda x: (x.is_dir(), x.name != "board.md", x.name.lower())):
        if x.is_file():
            roots.append(_tnode(x.name, x, False, note=_size(x)))
            continue
        if x.name in _TREE_LEAF:
            roots.append(_tnode(x.name + "/", x, True, note=_TREE_LEAF[x.name]))
            continue
        kids = []
        for y in _entries(x):
            page = by_dir.get(y)
            if not y.is_dir():
                kids.append(_tnode(y.name, y, False, note=_size(y)))
                continue
            sub, more = _walk(y, 2)
            if page:
                state = page["state"].split(" · ", 1)[0]
                extra = len(sub) + more - 1
                note = state + (f' · {_plural(extra, "more item")}' if extra > 0 else "")
                kids.append(_tnode(y.name + "/", y, True, [_FOLDER_KIND[_page_slot(page)]] if _page_slot(page) else [],
                                   note, sub, False, more))
            else:
                kids.append(_tnode(y.name + "/", y, True, note=_plural(len(sub) + more, "item"), kids=sub, more=more))
        mine = [p for p in snap["pages"] if p["rel"].split("/", 1)[0] == x.name]
        slots = [slot for slot in _FOLDER_KIND if any(_page_slot(p) == slot for p in mine)]
        if x.name in cuts:
            note = _plural(len(mine), "page") + "".join(
                f' · {sum(p["level"] == lv for p in mine)} {lv[0].upper()}' for lv in _LEVELS if any(p["level"] == lv for p in mine))
        elif mine:
            note = _plural(len(mine), "page") + (f' · {_plural(len(snap["questions"]), "question")}'
                                                 if "question" in slots else "")
        else:
            note = _plural(len(kids), "item")
        roots.append(_tnode(x.name + "/", x, True, [_FOLDER_KIND[s] for s in slots], note, kids, x.name not in cuts))
    return roots


def _homes_tree(snap: dict) -> list[dict]:
    """The project homes this board uses, outside its folder: the Task home
    (shared by every board of the project) and this board's Results store."""
    homes = []
    calls = _task_calls(snap)
    tasks_root = _tasks_root(snap)
    project = tasks_root.parent
    if tasks_root.is_dir():
        families = []
        for fam in _entries(tasks_root):
            if not fam.is_dir():
                families.append(_tnode(fam.name, fam, False, note=_size(fam)))
                continue
            mine = [c for c in calls if c["family"] == fam.name]
            kids = []
            for task in _entries(fam):
                if not task.is_dir():
                    kids.append(_tnode(task.name, task, False, note=_size(task)))
                    continue
                here = [c for c in mine if c.get("task_path", task) == task
                        or c.get("task_path", task).parent == task]
                sub, more = _walk(task, 3)
                note = (f'{_plural(len(here), "call")} for this board · {sum(c["ran"] for c in here)} ran'
                        if here else "no call for this board")
                kids.append(_tnode(task.name + "/", task, True, note=note, kids=sub, more=more))
            note = (f'{_plural(len(mine), "call")} for this board' if mine else 'not used by this board')
            families.append(_tnode(fam.name + "/", fam, True, note=note, kids=kids, opened=bool(mine)))
        homes.append(_tnode(f"{project.name}/tasks/", tasks_root, True, ["Task run"],
                            "the Task home · the code, one config per call · shared by every board", families, True))
    store = snap["store_path"]
    if store and store.is_dir():
        sub, more = _walk(store, 4)
        homes.append(_tnode(f'{snap["store"].rstrip("/")}/', store, True, ["Task run"],
                            f'the Results store · outside git · {_plural(sum(c["ran"] for c in calls), "result")} '
                            "· data pages cite these", sub, True, more))
    return homes


def _tree_href(snap: dict, path: Path) -> str:
    page = next((p for p in snap["pages"] if p["path"] == path), None)
    if page:
        return _page_link(snap, page)
    try:
        if snap["static"]:
            return "../" + quote(path.resolve().relative_to(snap["board"].resolve()).as_posix(), safe="/")
        return "/" + quote(path.resolve().relative_to(snap["root"].resolve()).as_posix(), safe="/")
    except ValueError:
        return ""


def _tree_html(snap: dict, nodes: list[dict]) -> str:
    """Two aligned columns per row: the bare tree on the left, the run types and
    counts on the right (the paper board's Folder tree × Run-Type)."""
    out = []
    for n in nodes:
        url = "" if n["dir"] else _tree_href(snap, n["path"])
        name = f'<a href="{_e(url)}">{_e(n["name"])}</a>' if url else _e(n["name"])
        top = "".join(f'<span class="idtag rt">{_e(c)}</span>' for c in n["chips"])
        top += f'<span class=tn-note>{_e(n["note"])}</span>' if n["note"] else ""
        line = (f'<span class=tn-name title="{_e(n["name"])}">{"📁" if n["dir"] else "📄"} {name}</span>'
                f'<span class=tn-works><span class=tn-top>{top}</span></span>')
        if n["dir"]:
            kids = _tree_html(snap, n["kids"])
            if n["more"]:
                kids += f'<li class=tn-more>… {_plural(n["more"], "more file")} not listed</li>'
            body = f"<ul>{kids}</ul>" if kids else ""
            out.append(f'<li><details class=tn{" open" if n["open"] else ""}><summary>{line}</summary>{body}</details></li>')
        else:
            out.append(f"<li><div class=tn-file>{line}</div></li>")
    return "".join(out)


def _wbr(text: str) -> str:
    """A path that may break only after a slash, never inside a name."""
    return "/<wbr>".join(_e(part) for part in text.split("/"))


# Space · subspace → the work that lands there, and who does it.  Owners are the
# Folder ownership table of haipipe-insight-workflow; the workers and agents are
# the skills that actually run the work (haipipe-task, haipipe-discovery and the
# Page workflow agents).  `count` names a live number read from this board.
_WHO = (
    ("Scope", "Data", "data", "none · the extract is prepared before this board reads it", "",
     "haipipe-insight-meta", "haipipe-task · the prep job under tasks/", "Claude Code, outside this board"),
    ("Scope", "Partition", "partition", "none · registering a partition is a control action", "",
     "haipipe-insight-meta", "—", "a person, in MT00"),
    ("Scope", "Register", "register", "none · registering a question is a control action", "",
     "haipipe-insight-question", "—", "a person, in MT01 – MT04"),
    ("Scope", "Ask", "ask", "none · the Ask box writes one register row", "",
     "haipipe-insight-question", "haipipe-insight · the /haipipe-insight door", "a person asks, Claude Code writes the row"),
    ("Scope", "Pages", "pages", "none · a list of every page", "", "—", "—", "—"),
    ("Insight", "Answer", "answer", "Page Writing Runs · rp-sec-NN · rp-para-NN", "page",
     "the level's folder skill: haipipe-insight-data · -information · -knowledge · -wisdom",
     "haipipe-page-workflow · agent haipipe-page-writing-agent", "the agent writes, a person accepts"),
    ("Insight", "Ladder", "ladder", "none · reads D → I → K → W already answered", "", "—", "—", "—"),
    ("Insight", "Limits", "limits", "none · reads the Wisdom page's limits", "", "—", "—", "—"),
    ("Evidence", "Trace", "", "Page Evidence Runs · RE lineage", "page",
     "the citing level's folder skill", "haipipe-page-evidence · agent haipipe-page-evidence-agent",
     "the agent runs it, a person decides the item"),
    ("Evidence", "Trace", "", "Supporting Runs · the numbers a data page cites", "support",
     "haipipe-insight-data", "haipipe-task · haipipe-discovery", "Claude Code runs the task"),
    ("Check", "Gates", "gates", "none · GI0 – GI6 are control actions, never Runs", "",
     "haipipe-insight-workflow", "—", "a person signs GI5"),
    ("Check", "Mechanical checks", "mech", "none · one script over the whole board", "",
     "haipipe-board", "cli/check.py", "anyone, any time"),
    ("Run", "Runs", "ledger", "every Supporting Run this board's pages name", "support",
     "haipipe-insight-workflow", "reads runtime.yaml in the store", "read-only"),
    ("Run", "Timeline", "timeline", "none · reads the same runs and the page logs", "", "—", "—", "—"),
    ("Run", "Who does it", "who", "none · this table", "", "—", "—", "—"),
    ("Run", "Workflow map", "wmap", "none · a definition view", "", "—", "—", "—"),
    ("Delivery", "Delivery", "", "none · signing the handoff is a control action", "",
     "haipipe-insight-wisdom", "—", "a person signs"),
)


def _live_counts(snap: dict) -> dict[str, str]:
    """The two numbers the work lines quote, read from disk on every request."""
    page_runs = sum(len(r["runs"]) for r in snap.get("workflow_runtimes", []) if not r.get("error"))
    store = snap["store_path"]
    receipts = sum(1 for _ in store.rglob("runtime.yaml")) if store and store.is_dir() else 0
    return {"support": (f'{len(snap["runs"])} named by pages · {receipts} receipts in the store'
                        if snap["runs"] or receipts else "none recorded yet"),
            "page": (f'{page_runs} recorded' if page_runs else "none recorded yet"),
            "": ""}


def _work_line(snap: dict, space: str, tab: str, live: dict[str, str]) -> str:
    """One quiet line under a tab: what runs land here, how many this board has,
    and the skill or agent that does the work.  The full table is Run Space ›
    Who does it; this line is the same row, where the person already is."""
    rows = [r for r in _WHO if r[0].lower() == space and (r[2] == tab if tab else True)]
    if not rows:
        return ""
    parts = []
    for _, _, _, work, key, owner, worker, actor in rows:
        count = live.get(key, "")
        who = " · ".join(x for x in (worker if worker != "—" else "", actor if actor != "—" else "") if x)
        if work.startswith("none"):
            line = f'<b>No run here</b> · {_wbr(work[7:])}'
        else:
            line = f'<b>Runs here</b> · {_wbr(work)}' + (f' · <span class=wl-count>{_e(count)}</span>' if count else "")
        parts.append(line + (f' · {_wbr(who)}' if who else ""))
    link = ("" if snap["static"] else
            f' <a class=wl-more href="{_e(_space_url(snap, "run", "who"))}">all runs and skills</a>')
    return f'<p class=workline>{" <br>".join(parts)}{link}</p>'


def _space_url(snap: dict, space: str, view: str) -> str:
    return f'?board={quote(snap["board_arg"] or snap["board"].name)}&space={space}&view={view}'


_VIEW_TAG = re.compile(r'(<div class="view(?: on)?" data-view="([a-z]+)">)')


def _with_work_lines(html: str, snap: dict, space: str) -> str:
    """Put each tab's work line right under its tab, without touching the
    renderers that own those Spaces (several sessions edit this file)."""
    live = _live_counts(snap)
    if not _VIEW_TAG.search(html):                      # a Space with a single view
        return _work_line(snap, space, "", live) + html
    return _VIEW_TAG.sub(lambda m: m.group(1) + _work_line(snap, space, m.group(2), live), html)


def _render_who(snap: dict) -> str:
    """Run Space · Who does it: for every Space and tab, the runs that land
    there and the skill or agent that does them.  Counts are read from disk."""
    live = _live_counts(snap)
    rows, last = [], ""
    for space, tab, _, work, key, owner, worker, actor in _WHO:
        if space != last:
            rows.append(f'<tr class=group><td colspan=6>{_e(space)} Space</td></tr>')
            last = space
        none = work.startswith("none")
        rows.append(f'<tr><td class=nw>{_e(tab)}</td>'
                    f'<td class={"mut" if none else ""}>{_wbr(work)}</td>'
                    f'<td class="mut nw">{_e(live.get(key, "—"))}</td>'
                    f'<td>{_wbr(owner)}</td><td>{_wbr(worker)}</td><td>{_e(actor)}</td></tr>')
    return ('<h2>Who does it</h2><p class=lead>Every Space and every tab: the runs that land there, how many this board '
            'has, and the skill or agent that does the work. A control action (registering, checking, signing) is '
            'a person\'s and never becomes a Run.</p>'
            '<div class=scroll><table class=who><tr><th>Tab</th><th>Runs that land here</th><th>On this board</th>'
            '<th>Owner skill</th><th>Worker skill or agent</th><th>Who acts</th></tr>'
            + "".join(rows) + '</table></div>')


def _render_workflow_map(snap: dict, projection: dict | None = None) -> str:
    where = _slot_folders(snap)
    head = "".join(f"<th>{s}</th>" for s in ("Folder resource", "Scope", "Insight", "Evidence", "Check", "Run", "Delivery",
                                               "Folder on this board"))
    body = "".join(
        f'<tr><td><b>{_e(name)}</b><div class="mut mono">{_wbr(hint)}</div></td>'
        + "".join(f'<td class={"mut" if c == "—" else ""}>{_wbr(c)}</td>' for c in cells)
        + '<td>' + ("".join(f'<span class=idtag>{_wbr(f)}' + (f' <span class=nw>· {_e(n)}</span>' if n else "") + '</span>'
                            for f, n in where.get(slot, []))
                    or '<span class=mut>—</span>') + '</td></tr>'
        for name, hint, slot, cells in _WORKFLOW_MAP)

    def count(nodes):
        return sum(1 + count(n["kids"]) for n in nodes)

    def box(caption, nodes, empty):
        tree = f'<ul class=tree>{_tree_html(snap, nodes)}</ul>' if nodes else f'<div class=tn-more>{empty}</div>'
        return (f'<div class=treebox><div class=tree-head><span>{caption}</span><span><span class="idtag rt">Folder kind</span>'
                f' · <span class=tn-note>counts</span></span></div>{tree}</div>')

    roots, homes = _board_tree(snap), _homes_tree(snap)
    selected = (_render_selected_specs(snap, projection, "all", read_only=True) if projection else
                '<p class=note>Select a question and partition to inspect its owed Specs.</p>')
    return ('<h2>Workflow map</h2><p class=lead>Shown here · read-only. This map describes selected work; '
            'the Runs view lists actual native executions.</p>' + selected +
            '<h3>Folder resources × Spaces</h3><p>The resources below hold questions and answers; their kinds do not count as Runs.</p>'
            f'<div class=scroll><table class=wmap><tr>{head}</tr>{body}</table></div>'
            f'<h2 class=tree-title>Folder tree × Folder kind <span class=mut>· {count(roots) + count(homes)} folders and files</span></h2>'
            '<p class=lead>Folders and their resource kinds, read from this board and the project stores it uses.</p>'
            + box(f'the board folder · {_e(snap["board"].name)}', roots, "the board folder is empty")
            + box("the project homes · Task home · Results store", homes,
                  "no Task home or Results store recorded"))



def _rows_table(rows: list[tuple[str, str, str]]) -> str:
    if not rows:
        return ""
    return '<table class=rows>' + "".join(
        f'<tr><td>{_e(i)}</td><td>{_inline(t)}</td><td class=from>{_e(f)}</td></tr>' for i, t, f in rows) + '</table>'


def _render_insight(snap: dict, view: dict | None, qid: str, pid: str,
                    projection: dict | None = None) -> str:
    if not view or not view["row"]:
        return '<p class=note>No question selected.</p>'
    row, cell, page = view["row"], view["cell"], view["page"]
    owed = _render_selected_specs(snap, projection, "insight") if projection else ""
    if not page:
        if cell["mark"] == "🚫":
            short, why = _REASONS.get(cell["note"], (cell["note"] or cell["raw"], ""))
            answer = (f'<h2>{_e(row["question"])}</h2><p class=opening>Refused on {_e(_partition_label(snap, pid))}: '
                      f'<b>{_e(short)}</b>{(", " + _e(why)) if why else ""}. A refusal is a recorded answer, not a gap.</p>')
        elif cell["mark"] != "·":
            answer = f'<h2>{_e(row["question"])}</h2><p class=opening>The answer Page is not allocated or recorded yet.</p>'
        else:
            answer = f'<h2>{_e(row["question"])}</h2><p class=opening>Not asked on partition {_e(pid)}. Pick another cell in the register.</p>'
        return _tabs([("answer", "Answer")]) + _view("answer", answer + owed, True)
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
            f'<small>{_pill(main["page"]["state"][:1], _clip(main["page"]["state"], 48))}</small></div>'
            f'<div>{_rows_table(main["rows"][:8])}'
            f'{("<p class=mut>… " + str(len(main["rows"]) - 8) + " more rows</p>") if len(main["rows"]) > 8 else ""}'
            f'{("<p class=mut>also cited: " + ", ".join(_link(snap, p) for p in others) + "</p>") if others else ""}</div></div>')
    ladder = ('<h2>How the answer was built</h2><p class=lead>Top down, along the first citation at each level. Other cited pages are linked.</p>'
              + ("".join(rungs) or '<p class=note>No citations found.</p>'))
    limits = "".join(f'<p>{_inline(l)}</p>' for l in _limits(page["text"]))
    limits = ('<h2>What this answer may not say</h2><div class=limits>' + limits + '</div>') if limits else '<p class=note>No answer limits have been recorded.</p>'
    return (_tabs([("answer", "Answer"), ("ladder", "Ladder"), ("limits", "Limits")])
            + _view("answer", answer + owed, True) + _view("ladder", ladder) + _view("limits", limits))


def _render_evidence(snap: dict, view: dict | None, projection: dict | None = None) -> str:
    # One hop per line, read top to bottom; a wrapping row of arrows left an
    # arrow dangling at each line end.
    hops = []
    if view and view["page"]:
        for p in view["primary"]:
            rows = _rows(p["text"])
            first = rows[0] if rows else None
            hops.append((p["level"] or "page", _link(snap, p), _inline(first[1] if first else p["title"])))
        r = view["receipt"]
        if r:
            hops.append(("run", f'<span class=mono>{_e(r["rel"])}</span>',
                         _e(f'{r["status"]} · git {r["git"]} · {r["duration"]} s')))
        if snap["context"]:
            hops.append(("extract", f'<span class=mono>{_e(snap["context"].split(" · ")[0])}</span>', ""))
    chain = ('<h2>Trace</h2><p class=lead>From the answer down to the extract. Each line is a file that exists.</p><ol class=trace>'
             + "".join(f'<li><span class=eyebrow>{_e(k)}</span><span>{w}</span><span>{t}</span></li>' for k, w, t in hops)
             + '</ol>') if hops else '<p class=note>Select an answered cell to trace it.</p>'
    if view and view["page"] and not view["receipt"]:
        chain += '<p class=note style="margin-top:12px">No page in this chain names a run receipt, so the trace stops at the D page.</p>'
    return chain + (_render_selected_specs(snap, projection, "evidence") if projection else "")


def _render_delivery(snap: dict, projection: dict | None = None) -> str:
    """What leaves this board: person-signed Wisdom pages a DesignBoard may use."""
    hrows = "".join(
        f'<tr><td>{_link(snap, h["record"])} · {_e(h["title"])}</td><td class=mono>{_e(h["serves"])}</td>'
        f'<td>{_pill("✅" if h["bindable"] else "🟡", h["eligibility"])} · {_e(h["eligibility_reason"])}</td></tr>'
        for h in snap["handoffs"]) or '<tr><td colspan=3 class=mut>No Wisdom page is ready to leave this board yet.</td></tr>'
    ready = sum(h["bindable"] for h in snap["handoffs"])
    waiting = len(snap["handoffs"]) - ready
    return (f'<h2>Delivery</h2><p class=lead>{ready} Wisdom page{"" if ready == 1 else "s"} ready for design'
            f'{f"; {waiting} need current signature/settlement evidence" if waiting else ""}. '
            f'Data, Information and Knowledge pages never leave the board directly.</p>'
            f'<table><tr><th>Wisdom page</th><th>Serves</th><th>Current eligibility</th></tr>{hrows}</table>'
            + (_render_selected_specs(snap, projection, "delivery") if projection else ""))


def _render_check(snap: dict, view: dict | None, qid: str, pid: str) -> str:
    if not view or not view["row"]:
        gates = '<p class=note>No cell selected.</p>'
    else:
        gates = '<div class=gates>' + "".join(
            f'<div class="gate {g["state"]}"><span class=k>{_e(g["key"])}</span><span class=n>{_e(g["name"])}</span>'
            f'<span class=who><span class="pill {"human" if g["who"] == "person" else "acc" if g["who"] == "agent" else ""}">{_e(g["who"])}</span> {_e(g["state"])}</span>'
            f'{("<span class=n title=" + chr(34) + _e(g["note"]) + chr(34) + ">" + _e(_clip(g["note"], 90)) + "</span>") if g["note"] else ""}</div>'
            for g in view["gates"]) + '</div>'
    gates = f'<h2>Gates for {_e(qid)} × {_e(pid)}</h2><p class=lead>Shown here · read-only. These are resource controls, with no Run allocation. Applicable GI controls for this cell. Handoff signing needs a person; a permitted POOL deferral exports no handoff.</p>' + gates
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
        checks.append({"level": "WARN", "code": "no-current-design-handoff", "where": board_root.name,
                       "message": "no current signed payload with verified dependency pins and GI6 receipt is available to Design"})
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
    who cites it, its gates and its log.  Same data as the board workbench, one
    page deep.  The Outline workbench stays the page's writing workbench."""
    cells = page_cells(snap, page)
    qid, pid = cells[0] if cells else ("", page["partition"])
    cv = _cell_view(snap, qid, pid) if qid else None
    projection = selected_specs(snap, qid, pid, page=page)
    board_url = _cell_url(snap, qid, pid) if qid else f"/_board/insight-board?board={quote(snap['board'].name)}"
    cited_by = [p for p in snap["pages"] if page["id"] in _parents(p["text"])]
    parents = [snap["by_id"][pid_] for pid_ in _parents(page["text"]) if pid_ in snap["by_id"]]
    rows = _rows(page["text"])
    opening = "".join(f'<p class=opening>{_inline(p)}</p>' for p in _opening(page["text"]))
    level = _LEVEL_LABEL.get((page["level"] or " ")[0].upper(), page["page_type"] or "page")
    where = (" · ".join(f'<a href="{_e(_cell_url(snap, q, p))}" class=mono>{_e(q)} × {_e(_partition_label(snap, p))}</a>' for q, p in cells)
             or "<span class=mut>answers no register cell</span>")
    header = (f'<header><h1>🔎 {_e(page["title"])}</h1><div class=mut>{_e(page["id"])} {_e(_slug(page))} · {_e(level)} · '
              f'part of <a href="{_e(board_url)}">{_e(snap["title"])}</a> · answers {where}</div></header>')
    strip = _render_strip(snap, cv, qid, pid) if cv and cv["row"] else ""
    this = (f'<h2>This page</h2><p class=mut>{_pill(page["state"][:1], _clip(page["state"], 90))}</p>{opening}{_rows_table(rows)}'
            + ('' if rows else '<p class=note>No id-numbered rows in a fenced block on this page.</p>'))
    cites = ('<h2>Cites</h2>' + ('<table><tr><th>Page</th><th>Title</th><th>State</th></tr>' + "".join(
        f'<tr><td>{_link(snap, p)}</td><td>{_e(p["title"])}</td><td>{_pill(p["state"][:1], _clip(p["state"], 40))}</td></tr>'
        for p in parents) + '</table>' if parents else '<p class=note>This page cites no other page by id.</p>'))
    by = ('<h2>Cited by</h2>' + ('<table><tr><th>Page</th><th>Title</th><th>State</th></tr>' + "".join(
        f'<tr><td>{_link(snap, p)}</td><td>{_e(p["title"])}</td><td>{_pill(p["state"][:1], _clip(p["state"], 40))}</td></tr>'
        for p in cited_by) + '</table>' if cited_by else '<p class=note>No page cites this one yet.</p>'))
    gates = ('<h2>Gates</h2><div class=gates>' + "".join(
        f'<div class="gate {g["state"]}"><span class=k>{_e(g["key"])}</span><span class=n>{_e(g["name"])}</span>'
        f'<span class=who><span class="pill {"human" if g["who"] == "person" else "acc" if g["who"] == "agent" else ""}">{_e(g["who"])}</span> {_e(g["state"])}</span></div>'
        for g in cv["gates"]) + '</div>') if cv and cv["row"] else '<h2>Gates</h2><p class=note>No register cell, so no gates.</p>'
    log_lines = _LOG_LINE.findall(_section(page["text"], "Log"))
    log = ('<h2>Log</h2><ul class=timeline>' + "".join(
        f'<li><span class=d>{_e(d)}</span><span class=p></span><span>{_inline(t[:240])}</span></li>' for d, t in reversed(log_lines))
        + '</ul>') if log_lines else '<h2>Log</h2><p class=note>No dated log line on this page.</p>'
    this += _render_selected_specs(snap, projection, "all")
    shell = (_tabs([("page", "This page"), ("cites", "Cites"), ("by", "Cited by"), ("gates", "Gates"), ("log", "Log")])
             + _view("page", this, True) + _view("cites", cites) + _view("by", by) + _view("gates", gates) + _view("log", log))
    return _spell_ids(snap, "".join([
        '<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">',
        f'<title>🔎 {_e(page["id"])} · {_e(page["title"])}</title><style>{_CSS}</style></head><body data-space="page"><main>',
        header, strip, f'<div class="shell">{shell}</div>',
        f'<p class=source>source <code>{_e(snap["relative"])}/{_e(page["rel"])}</code> · <a href="{_e(_page_link(snap, page))}">rendered page</a></p>',
        "</main>", _JS, "</body></html>",
    ]))


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
            # The workbench has two levels, board and page, and no list of its
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
                    payload.get("origin", ""), payload.get("parent", ""),
                    workflow_runtime_id=payload.get("workflow_runtime_id", ""),
                    actor=payload.get("actor") or "board-ask")
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
    ask.add_argument("--workflow-runtime-id", default="", help="existing Runtime declaring this exact registration")
    ask.add_argument("--actor", default="board-ask", help="registration actor recorded in the control receipt")
    args = ap.parse_args(argv)
    board = Path(args.board).resolve()
    if not (board / "board.md").is_file():
        print(f"not a Board: {board}")
        return 2
    try:
        qid, pids = register_question(board, args.level, args.question, args.partitions,
                                      args.origin, args.parent,
                                      workflow_runtime_id=args.workflow_runtime_id, actor=args.actor)
    except ValueError as exc:
        print(f"refused: {exc}")
        return 1
    print(f"registered {qid} on {', '.join(pids)} · next: /haipipe-insight application {board.name} chain {qid} {pids[0]}")
    return 0



# ─── the one write: register a question ─────────────────────────────────────

def register_question(board_root: Path, level: str, question: str, partitions,
                      origin: str = "", parent: str = "", *,
                      workflow_runtime_id: str = "", actor: str = "board-ask") -> tuple[str, list[str]]:
    """Serialize shared register writes; a concurrent or interrupted writer holds."""
    lock = Path(board_root) / ".insight-registration.lock"
    try:
        lock.mkdir()
    except FileExistsError as exc:
        raise ValueError("registration is locked; finish or recover the existing writer first") from exc
    try:
        return _register_question(board_root, level, question, partitions, origin, parent,
                                  workflow_runtime_id=workflow_runtime_id, actor=actor)
    finally:
        lock.rmdir()


def _register_question(board_root: Path, level: str, question: str, partitions,
                       origin: str = "", parent: str = "", *,
                       workflow_runtime_id: str = "", actor: str = "board-ask") -> tuple[str, list[str]]:
    """Register a question and index its canonical control receipt; no Run.

    Called by the skill (`python3 -m live.insightboard ask ...`) after Claude
    Code has decided the level, the partitions and the lineage.  The register
    grid remains the question authority. Its Outline log owns the receipt;
    the aggregate Runtime indexes that control. Transposed grids need an
    explicit owner edit.
    """
    level = (level or "").strip().upper()
    question = " ".join((question or "").split())
    if isinstance(partitions, str):
        partitions = re.split(r"[,\s]+", partitions)
    partitions = list(dict.fromkeys(p.strip().upper() for p in partitions if p and p.strip()))
    if level not in _LEVEL_OF:
        raise ValueError("kind of answer must be D, I, K or W")
    if not question:
        raise ValueError("the question is empty")
    if not partitions:
        raise ValueError("choose at least one partition")
    if any(not re.fullmatch(r"[A-Z]", p) for p in partitions):
        raise ValueError("partition ids must be single letters")
    pages = _pages(Path(board_root))
    candidates = [p for p in pages if p["rung"] == _LEVEL_OF[level]
                  or p["id"] == f"MT0{'DIKW'.index(level) + 1}"]
    for page in candidates:
        if page["identity_error"]:
            raise ValueError(page["identity_error"])
        if page["page_type"] != "question":
            raise ValueError(f"{page['path']}: selected register is not a Question Folder")
    if len(candidates) > 1:
        raise ValueError("multiple Question registers face the requested rung")
    register = candidates[0] if candidates else None
    if register is None:
        raise ValueError(f"no register page faces the {_LEVEL_LABEL[level]} level")
    qid, updated = _prepare_question_row(register["path"], level, question, partitions)
    import yaml
    board_root = Path(board_root).resolve()
    path = register["path"].resolve()
    runtime_id = workflow_runtime_id or f"registration-{uuid.uuid4().hex}"
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]*", runtime_id):
        raise ValueError("invalid workflow_runtime_id")
    runtime_dir = board_root / "_runs/insight" / runtime_id
    runtime_path = runtime_dir / "runtime.yaml"
    request = {"action": "register-question", "level": level,
               "question": question, "partitions": partitions}
    if workflow_runtime_id:
        try:
            runtime = yaml.safe_load(runtime_path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            raise ValueError(f"registration Runtime cannot be read: {exc}") from exc
        if not isinstance(runtime, dict) or runtime.get("workflow_id") != "haipipe-insight-workflow" \
                or runtime.get("workflow_runtime_id") != runtime_id \
                or runtime.get("status") not in {"planned", "running", "held"} \
                or request not in runtime.get("requested_controls", []):
            raise ValueError("Runtime must declare this exact registration control and remain open")
        if not isinstance(runtime.get("resource_controls", []), list):
            raise ValueError("Runtime resource_controls must be a list")
    else:
        definition = {"schema": "haipipe.insight-definition/v1", "workflow_id": "haipipe-insight-workflow",
                      "revision": "v001", "run_specs": [], "requested_answer_targets": [],
                      "requested_controls": [request],
                      "completion": {"required_controls": "neutral-row-open-cells-and-registration-receipt",
                                     "required_runs": "none", "frontier": "empty"}}
        definition_text = yaml.safe_dump(definition, sort_keys=False, allow_unicode=True)
        runtime = {"schema": "haipipe.workflow-runtime/v1", "workflow_id": "haipipe-insight-workflow",
                   "workflow_version": "1.3.1", "workflow_runtime_id": runtime_id,
                   "definition_ref": "definition-v001.yaml",
                   "definition_hash": hashlib.sha256(definition_text.encode()).hexdigest(),
                   "status": "planned", "requested_answer_targets": [], "requested_controls": [request],
                   "runs": [], "control": {"gates": [], "routes": []},
                   "resource_controls": [], "frontier": [], "output": {"acceptance": "pending"}}
    record_id = f"registration-{qid.lower()}-{uuid.uuid4().hex[:12]}"
    log = path.parent / "outline" / f"{path.stem}-log.md"
    receipt = f"{log.relative_to(board_root).as_posix()}#{record_id}"
    control = {"key": "registration", "target": {"question": qid, "partitions": partitions},
               "status": "passed", "authority": "haipipe-insight-question", "actor": actor,
               "evidence": [{"path": path.relative_to(board_root).as_posix(),
                             "sha256": hashlib.sha256(updated.encode()).hexdigest()}], "receipt": receipt}
    stamp = datetime.now().astimezone().isoformat(timespec="seconds")
    record = {"workflow_runtime_id": runtime_id, "at": stamp, **control,
              "assertion": "neutral question row and requested open cells registered",
              "outcome": "registered", "origin": origin or "not stated", "parent": parent or "none",
              "next_action": "define any missing answerability facts before GI1; answering remains separate"}
    entry = (f"### {record_id}\n\n{date.today():%y%m%d} · Registered `{qid}` on {', '.join(partitions)} "
             f"from the Insight Board · origin: {origin or 'not stated'} · born from: {parent or 'new'}\n\n"
             f"```yaml\n{yaml.safe_dump(record, sort_keys=False, allow_unicode=True)}```\n")
    # Prepare and validate every input before the first write. A newly-created
    # planned Runtime makes an interrupted registration visible for recovery.
    if not workflow_runtime_id:
        runtime_dir.mkdir(parents=True, exist_ok=False)
        (runtime_dir / "definition-v001.yaml").write_text(definition_text, encoding="utf-8")
        runtime_path.write_text(yaml.safe_dump(runtime, sort_keys=False), encoding="utf-8")
    path.write_text(updated, encoding="utf-8")
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(_read(log).rstrip("\n") + "\n\n" + entry, encoding="utf-8")
    runtime.setdefault("resource_controls", []).append(control)
    if not workflow_runtime_id:
        runtime.update(status="complete", output={"path": path.relative_to(board_root).as_posix(),
                                                  "acceptance": "passed", "receipt": receipt})
    runtime_path.write_text(yaml.safe_dump(runtime, sort_keys=False, allow_unicode=True), encoding="utf-8")
    _CACHE.pop(str(board_root), None)
    return qid, partitions


def _prepare_question_row(path: Path, level: str, question: str, partitions) -> tuple[str, str]:
    if isinstance(partitions, str):
        partitions = [partitions]
    import textwrap

    text = _read(path)
    fence = re.compile(r"(?ms)^```\w*\n(.*?)^```")
    block = next((m for m in fence.finditer(text)
                  if re.search(r"(?m)^id\s+.*\bquestion\b", m.group(1))), None)
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
    last = max((i for i, l in enumerate(lines) if re.match(r"^Q[DIKW]\d+\s", l)),
               default=lines.index(header))
    while last + 1 < len(lines) and re.match(r"^\s{4,}\S", lines[last + 1]) and not _MARK.search(lines[last + 1]):
        last += 1  # keep a wrapped question with its row
    lines[last + 1:last + 1] = new_lines
    body = "\n".join(lines) + "\n"
    text = text[:block.start(1)] + body + text[block.end(1):]
    return qid, text
if __name__ == "__main__":
    import sys
    raise SystemExit(_main(sys.argv[1:]))
