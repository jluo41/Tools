"""🔎 Insight Board · one dataset, four Spaces, logic left and work right.

One workbench reads one extract (MT00 names it; a new extract is a new board).
Scope shows the dataset, its partitions and the question registers.  Insight
shows one High/Low table per partition: on the left the questions asked at
Data, Information, Knowledge and Wisdom (MT01-MT04), on the right the runs
that answer them, joined by each task config's `answers:` line.  Check shows
the gates, the mechanical checks and the workflow runtime; Delivery the signed
handoffs.  Each Space has its Runs panel; a run line opens its results, and a
page opens as a document, in a pop-out.  Design: studio/insight-workbench-design.excalidraw.

The board on disk stays authoritative.  This module only reads: the register
pages (their ASCII cell grids), the answering pages, the task configs whose
`store:` is this board's store, and their `runtime.yaml` receipts.
"""

from __future__ import annotations

import html
import re
import uuid
from datetime import date, datetime
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse

from src.folder_contract import resolved_folder_kind
from .insight_handoff import eligibility as handoff_eligibility, watch_paths as handoff_watch_paths
from .insight_run_specs import (definition as read_insight_definition, describe as describe_run_field,
                                people as run_people, reader_name as run_reader_name)


_TITLE = re.compile(r"(?m)^#\s+(.+?)\s*$")
_INSIGHT_BOARD = re.compile(r"(?:^|[-_])insightboard(?:$|[-_])", re.I)
_LEVELS = ("data", "information", "knowledge", "wisdom")
_LEVEL_OF = {"D": "data", "I": "information", "K": "knowledge", "W": "wisdom"}
_LEVEL_LABEL = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}
_SKIP = {"board", "_archive", "__pycache__", ".git", "probe", "display", "_results", "reports", "results", "runs"}
# A page id is its level, its number and its partition's name: `I02-full`, `K02-cross`
# (JL 261001: no partition letters).  A folder is `<id>-<slug>`, so an id is never
# followed by `-<word>` when it stands alone.
_PAGE_ID = re.compile(r"(?<![\w-])([DIKW]\d{2}-[a-z]+)(?![a-z0-9]|-[a-z])")
_PAGE_STEM = re.compile(r"^([DIKW])(\d{2})-([a-z]+)(?:-|$)")
_PART_DIR = re.compile(r"^\d+-([a-z]+)$")
FULL, CROSS = "full", "cross"
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
# insights/ is the board world (JL 261001); insights/_old/ holds boards made before
# reports; applications/ is legacy and still read.
_BOARD_GLOBS = ("examples*/*/insights/*/board.md", "examples*/*/insights/_old/*/board.md",
                "examples*/*/applications/*/board.md", "examples*/*/*/board.md",
                "insights/*/board.md", "applications/*/board.md", "*/board.md")


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
        m = _PAGE_STEM.match(path.stem)
        stem = f"{m.group(1)}{m.group(2)}-{m.group(3)}" if m else path.stem.split("-", 1)[0].upper()
        part = next((_PART_DIR.match(p).group(1) for p in rel.parts if _PART_DIR.match(p)), "")
        pages.append({
            "path": path, "rel": rel.as_posix(), "id": stem, "text": text,
            "title": (_TITLE.search(text).group(1).strip() if _TITLE.search(text) else path.stem),
            "state": head.get("state", "OPEN"),
            "page_type": kind, "identity_error": identity_error,
            "rung": head.get("question-rung", "").lower(),
            "level": _LEVEL_OF.get(m.group(1)) if m else "", "partition": part,
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


# A cell is `✅ I01-full`, `🟡 I03-youngmale final`, `🚫 thin`, `🚫 full-only` or a lone `·`.
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
    cols = [tok for tok in header.split() if tok in partitions]
    if "partition" in header and _QID.search(header):
        return _parse_transposed(lines, header, page, partitions)
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


def _parse_transposed(lines: list[str], header: str, page: dict, partitions: list[str]) -> list[dict]:
    """MT04 style: one row per partition, one column per question id."""
    qcols = _QID.findall(header)
    rows = {qid: {"id": qid, "question": "", "register": page, "cells": {}} for qid in qcols}
    current = None
    for line in lines:
        m = re.match(r"^(Q[DIKW]\d+)\s+(.*?)\s{2,}", line)
        if m and m.group(1) in rows:
            current = rows[m.group(1)]
            current["question"] = m.group(2).strip()
        elif current and re.match(r"^\s{3,}\S", line) and not _MARK.search(line[:40]):
            wrapped = re.split(r"\s{2,}", line.strip(), maxsplit=1)[0]
            if wrapped and wrapped not in partitions:
                current["question"] = (current["question"] + " " + wrapped).strip()
        pm = re.search(r"(?<!\S)(" + "|".join(map(re.escape, partitions)) + r")\s{2,}(.*)$", line) if partitions else None
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
        # `run receipts` (D01-cross binds six calls of one task): every
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
        # a page folder is also a task folder: its own results/<ticket>/runtime.yaml first
        candidates = [page["path"].parent / rel]
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
    """Page ids cited on `← I02-full · I1` lines, in citation order."""
    out = []
    for line in text.splitlines():
        if "←" in line:
            for pid in _PAGE_ID.findall(line.split("←", 1)[1]):
                if pid not in out:
                    out.append(pid)
    return out


def _rows(text: str) -> list[tuple[str, str, str]]:
    """`W1   DO send ...   K01-full · K1` rows inside fenced blocks: id, text, from.
    An indented line right under a row continues its text, so a row that
    wraps in the page is shown whole (W3 on W01-full ended "on the")."""
    rows: list[list[str]] = []
    for block in re.findall(r"(?ms)^```\w*\n(.*?)^```", text):
        last, col = None, 0
        for line in block.splitlines():
            m = re.match(r"^([DIKW]\d+)\s{2,}(.+?)\s*$", line)
            if m and "←" not in line and m.group(1) not in {r[0] for r in rows}:
                body = m.group(2)
                src = re.search(r"\s{2,}([DIKW]\d{2}-[a-z]+\s?·\s?\S+)\s*$", body)
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
        m = _PART_DIR.match(folder.name)
        if folder.is_dir() and m:
            rows.append({"id": m.group(1), "name": m.group(1), "folder": folder.name,
                         "pages": sum(p["partition"] == m.group(1) for p in pages),
                         "where": "", "rows": "", "share": "", "config": ""})
    meta = next((p for p in pages if p["id"] == "MT00"), None)
    if meta:
        for row in rows:
            m = re.search(rf"(?m)^{re.escape(row['name'])}\s+(.+?)\s{{2,}}(?:(\S+)\.yaml|\(none\))",
                          meta["text"])
            if m:
                row["where"] = re.sub(r"^where:\s*\[\]\s*", "", m.group(1)).strip()
                row["config"] = m.group(2) or ""
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
    # `store: _results` is the board's own folder (JL 261001); a `_WorkSpace/...`
    # store (boards made before reports) is relative to the SPACE root.
    store = ((board_root / store_field) if store_field and not store_field.startswith(("_WorkSpace", "/"))
             else (server_root / store_field) if store_field else None)
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
                cell = matches[0]["cells"].get(page["partition"] or FULL, {}) if len(matches) == 1 else {}
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

def _pill(mark: str, text: str = "") -> str:
    cls = {"✅": "ok", "🟡": "warn", "🚫": "bad", "🧊": "acc"}.get(mark, "")
    return f'<span class="pill {cls}">{_e(text or mark)}</span>'


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


def display_id(pid: str, partitions: dict[str, str]) -> str:
    """A page id is already said in words, `I02-full` (JL 261001: no partition
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
            f'<header><h1>🔎 Insight Boards</h1><div class=mut><a href="/">all boards</a></div></header>{note}'
            f'<div class=shell><table><tr><th>Board</th><th>Title</th><th>Pages</th><th>Settled</th><th>Folder</th></tr>{body}</table></div>'
            '</main></body></html>')


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

    def add(task, name, ticket, receipt, source, page="", task_run=""):
        # one call per task and name (per page for a page ticket): tickets are often
        # symlinks to one shared `_run.sh`, so the resolved ticket path cannot tell calls apart
        key = (str(task.resolve()), name, page)
        if key in seen:
            return
        seen.add(key)
        rel = task.relative_to(tasks_root)
        calls.append({"family": rel.parts[0], "job": task.parent.name if len(rel.parts) > 2 else "",
                      "task": task.name, "call": name, "task_path": task, "source": source,
                      "ticket": ticket, "receipt": receipt, "script": ticket.is_file(),
                      "ran": receipt.is_file(), "page": page, "task_run": task_run or name})

    for runtime in snap.get("workflow_runtimes", []):
        for run in runtime.get("runs", []):
            ticket, receipt = absolute(run["ticket"]), absolute(run["receipt"])
            task = ticket.parent.parent
            if ticket.parent.name == "runs" and task.resolve().is_relative_to(tasks_root):
                add(task.resolve(), ticket.stem, ticket, receipt, "native-receipt")
    if not tasks_root.is_dir():
        return calls
    board_store = snap.get("store_path")
    # A page folder is also a task folder (JL 261001): its runs/run_bNNjNNtNNrNN_<partition>_<task>.sh
    # ticket calls a task run and writes the page's own results/<ticket>/.
    for ticket in sorted(snap["board"].glob("*/*/runs/run_*.sh")):
        hit = _TICKET_TARGET.search(_read(ticket))
        task = (tasks_root / hit.group(1)) if hit else None
        if task and task.is_dir():
            page = ticket.parent.parent
            add(task, ticket.stem, ticket, page / "results" / ticket.stem / "runtime.yaml",
                "page-ticket", page=page.name, task_run=hit.group(2))
    extract = _dataset_line(snap)[1] if snap.get("by_id") else ""
    for cfg in sorted(tasks_root.glob("*/*/*/scripts/config/*.yaml")):
        task = cfg.parents[2]
        job = task.parent
        if board_store is None:
            continue
        output_root = board_store / job.relative_to(tasks_root)
        # A config belongs to this board when the board dispatches it: its result is
        # in the board's store, or it reads the board's one extract (JL 261001). A
        # Job-level `store:` naming this board's store still counts (older Jobs).
        store = _field(_read(job / "src/config-defaults.yaml"), "store")
        owned = ((output_root / task.name / "results" / cfg.stem / "runtime.yaml").is_file()
                 or (extract and extract in (re.search(r"(?m)^\s*parquet_path:\s*(\S+)", _read(cfg)) or [None, ""])[1])
                 or (store and absolute(store).resolve() == board_store.resolve()))
        if not owned:
            continue
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


# ─── which cells a page answers ─────────────────────────────────────────────

def page_cells(snap: dict, page: dict) -> list[tuple[str, str]]:
    """The register cells this page answers, as (question id, partition)."""
    out = []
    for row in snap["questions"]:
        for pid, cell in row["cells"].items():
            if cell.get("page") == page["id"]:
                out.append((row["id"], pid))
    return out


# ─── the workbench: four Spaces, one dataset (studio/insight-workbench-design) ─

# A refused or deferred cell, said in words: the head goes where a run would
# be, the reason under it.  Tokens from MT02/MT03's legends.
_REASONS = {
    "full-only": ("Answered on Full", "a property of the whole extract, the same in every cut"),
    "thin": ("Too few rows", "fewer than 300 rows per message in this cut"),
    "defer": ("Defers to Full", "asking whether to segment from inside a segment is circular"),
    "nomeas": ("No answer", "no field in the extract records it"),
    "nocon": ("No answer", "the experiment never varies it"),
    "noiden": ("No answer", "13 messages cannot separate it"),
}
_SPACES = (("scope", "Scope"), ("insight", "Insight"), ("check", "Check"), ("delivery", "Delivery"))
_ANSWERS = re.compile(r"(?m)^answers:\s*(.*)$")
_STAGE = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}


def _part_label(snap: dict, pid: str) -> str:
    """`full` -> `Full`, `youngmale` -> `Young male`, `cross` -> `Cross` (JL 260916)."""
    if pid == FULL:
        return "Full"
    if pid == CROSS:
        return "Cross"
    name = _partition_name(snap, pid)
    return name[:1].upper() + name[1:] if name else pid


def _call_config(call: dict) -> Path | None:
    name = call.get("task_run") or call["call"]
    for path in (call["task_path"] / "configs" / f"{name}.yaml",
                 call["task_path"] / "scripts" / "config" / f"{name}.yaml"):
        if path.is_file():
            return path
    return None


def work_runs(snap: dict) -> list[dict]:
    """Every task call this board owns, with the questions it answers.

    A call belongs to this board because its config's `store:` is the board's
    store (one dataset, one workbench).  Its `answers:` line names the register
    questions its run answers; that line joins the Logic side to the Work side.
    Its partition is the MT00 row whose config it is.
    """
    if "work" in snap:
        return snap["work"]
    by_config = {row["config"]: row["id"] for row in snap["partitions"] if row.get("config")}
    # a run `rNN_<dataset>_<cut>` names its cut; the cut is the partition's MT00 name
    by_cut = {row["name"]: row["id"] for row in snap["partitions"]}
    out = []
    for call in _task_calls(snap):
        cfg = _call_config(call)
        hit = _ANSWERS.search(_read(cfg)) if cfg else None
        fields = _yaml_flat(_read(call["receipt"])) if call["ran"] else {}
        name = call.get("task_run") or call["call"]
        cut = "_".join(name.split("_")[2:]) if re.match(r"^r\d{2}_", name) else ""
        out.append({**call, "config": cfg, "partition": by_config.get(name) or by_cut.get(cut, ""),
                    "answers": _QID.findall(hit.group(1).split("#", 1)[0]) if hit else [],
                    "status": fields.get("status", "?") if call["ran"] else "not run"})
    snap["work"] = out
    return out


_TICKET_TARGET = re.compile(r'tasks/([^"\s]+?)/runs/([^/"\s]+)\.sh')


def page_tickets(snap: dict, page: dict | None) -> list[dict]:
    """The task runs one page rests on, read from its own runs/ tickets."""
    if not page:
        return []
    folder = page["path"].parent.name
    return [r for r in work_runs(snap) if r["source"] == "page-ticket" and r["page"] == folder]


def _run_url(snap: dict, run: dict) -> str:
    task = run["task_path"].resolve().relative_to(_tasks_root(snap).resolve()).as_posix()
    return (f"/_board/insight-run?board={quote(snap['board'].name)}"
            f"&task={quote(task, safe='/')}&call={quote(run['call'])}"
            + (f"&page={quote(run['page'])}" if run.get("page") else ""))


def _pop_url(snap: dict, page: dict) -> str:
    """A page opens as a document in the pop-out; there is no page-level workbench."""
    if snap["static"]:
        return _page_link(snap, page)
    return f"/_board/insight?board={quote(snap['board'].name)}&page={quote(page['id'])}"


def _answered_by(snap: dict) -> dict[str, list[str]]:
    """page id -> the register questions whose cell it settles."""
    out: dict[str, list[str]] = {}
    for q in snap["questions"]:
        for cell in q["cells"].values():
            if cell.get("page") and q["id"] not in out.setdefault(cell["page"], []):
                out[cell["page"]].append(q["id"])
    return out


def _builds_on(snap: dict, page: dict | None, qid: str, answered: dict) -> list[str]:
    """The lower questions this answer rests on: the questions its cited pages answer."""
    if not page:
        return []
    out = []
    for parent in _parents(page["text"]):
        for other in answered.get(parent, []):
            if other != qid and other not in out:
                out.append(other)
    return out


def _behind(snap: dict, page: dict | None, answered: dict) -> list[str]:
    """Every question below an answer, along all its citations (a K or W answer has
    no run of its own yet; the runs behind it are the runs of these questions)."""
    seen, out, frontier = set(), [], [page] if page else []
    while frontier:
        cur = frontier.pop(0)
        if cur["id"] in seen:
            continue
        seen.add(cur["id"])
        for parent in _parents(cur["text"]):
            out.extend(q for q in answered.get(parent, []) if q not in out)
            if parent in snap["by_id"]:
                frontier.append(snap["by_id"][parent])
    return out


def _numbers(qids: list[str]) -> str:
    """[QI7, QI8, QK2] -> `Information questions 7, 8 · Knowledge question 2`."""
    groups: dict[str, list[str]] = {}
    for qid in sorted(set(qids), key=lambda q: ("DIKW".index(q[1]), int(q[2:]))):
        groups.setdefault(qid[1], []).append(qid[2:])
    parts = []
    for lv in "DIKW":
        nums = groups.get(lv)
        if nums:
            parts.append(f'{_STAGE[lv]} question{"s" if len(nums) > 1 else ""} {", ".join(nums)}')
    return " · ".join(parts)


def _task_name(name: str) -> str:
    """`03_funnel_rates` -> `Funnel rates`."""
    words = re.sub(r"^[a-z]?\d+_", "", name).replace("_", " ")
    return words[:1].upper() + words[1:]


def _idname(name: str) -> str:
    """`j21_information_funnel` -> idtag `j21` + `information_funnel`."""
    head, _, tail = name.partition("_")
    return f'<span class=idtag>{_e(head)}</span> {_e(tail or head)}'


def _run_note(run: dict) -> str:
    """`ok`, or `ok · 11 pages` when one task run stands behind several pages."""
    pages = run.get("n_pages", 1)
    return f'{run["status"]} · {pages} pages' if pages > 1 else run["status"]


def _run_lines(snap: dict, runs: list[dict]) -> str:
    """Block → Job → Task → Run, one level per line, each one step in (the Paper's
    B → J → T → R, JL 261001). A two-level legacy task folder has no Job line."""
    out, last_block, last_job = [], None, None
    runs = sorted(runs, key=lambda r: str(r["task_path"]))     # one Block, then one Job, at a time
    for task_path in dict.fromkeys(r["task_path"] for r in runs):
        group = [r for r in runs if r["task_path"] == task_path]
        block, job = group[0]["family"], group[0]["job"]
        if block != last_block:
            out.append(f'<div class=bj-b>{_idname(block)}</div>')
            last_block, last_job = block, None
        if job and job != last_job:
            out.append(f'<div class=bj-j>{_idname(job)}</div>')
            last_job = job
        done = sum(r["status"] in {"ok", "complete", "completed", "done"} for r in group)
        lines = "".join(
            f'<a class="bj-run pop" href="{_e(_run_url(snap, r))}" data-pop="{_e(r["call"])}">'
            f'<span class=idtag>{_e(r["call"]).replace("_", "_<wbr>")}</span> <span class=mut>{_e(_run_note(r))}</span></a>'
            for r in group)
        out.append(f'<details class="bj-tr{" bj-flat" if not job else ""}"><summary class=bj-t>{_idname(task_path.name)} '
                   f'<span class=mut>▸ {len(group)} run{"" if len(group) == 1 else "s"} · done {done}</span></summary>'
                   f'<div class=bj-runs>{lines}</div></details>')
    return "".join(out)


def _work_cell(snap: dict, q: dict, pid: str, answered: dict) -> str:
    """The Work column of one question in one partition: the task and the runs that
    answer it.  A Knowledge or Wisdom answer has no run of its own yet: the runs
    behind it, along its citations.  What the answer says is the Report column."""
    cell = q["cells"].get(pid, _parse_cell("·"))
    page = snap["by_id"].get(cell.get("page", ""))
    if cell["mark"] == "·" or (cell["mark"] == "🚫" and not page):
        return '<p class=wk-none>—</p>'
    work = work_runs(snap)
    own = page_tickets(snap, page) or [
        r for r in work if q["id"] in r["answers"] and (pid == CROSS or r["partition"] == pid)]
    lv = q["id"][1]
    if own:
        names = list(dict.fromkeys(_task_name(r["task_path"].name) for r in own))
        return (f'<details class=wk open><summary><span class=kind>Task Work</span></summary>'
                f'<p class=wk-title><b>{_e(" · ".join(names))}</b></p>'
                f'<div class=bj>{_run_lines(snap, own)}</div></details>')
    if page and lv in "KW":
        lower = _behind(snap, page, answered)
        behind, seen = [], {}
        for r in work:
            if set(r["answers"]) & set(lower) and (pid == CROSS or r["partition"] == pid):
                key = (r["task_path"], r.get("task_run") or r["call"])
                if key in seen:
                    seen[key]["n_pages"] += 1
                else:
                    seen[key] = {**r, "n_pages": 1}
                    behind.append(seen[key])
        if behind:
            return (f'<details class=wk open><summary><span class=kind>Task Work</span></summary>'
                    f'<div class=bj>{_run_lines(snap, behind)}</div></details>')
    return '<p class=wk-none>No run names it under <code>answers:</code> yet</p>'


# ─── the Report column: what an answer says, in a few lines ─────────────────

_STRENGTH = re.compile(r"\b(STRONG|MODERATE|WEAK)\b")


def _report_path(snap: dict, qid: str, pid: str) -> Path:
    """`reports/<partition>/<question>.md` on the board, e.g. reports/full/QI4.md."""
    row = next((p for p in snap["partitions"] if p["id"] == pid), None)
    return snap["board"] / "reports" / (row["name"] if row else pid) / f"{qid}.md"


def _sentences(text: str, n: int = 2) -> str:
    """The first n sentences, never cut inside one."""
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z`(])", text.strip())
    return " ".join(parts[:n])


def report(snap: dict, qid: str, pid: str) -> dict | None:
    """What one question's answer says on one partition.

    The answering page IS the report (JL 261001: a page folder is also a task
    folder, its .md says what its own results/ show).  A `reports/` file, from
    the brief report-file layout, is still read first when one exists.
    """
    path = _report_path(snap, qid, pid)
    url = f"/_board/insight?board={quote(snap['board'].name)}&report={quote(pid + ':' + qid)}"
    if path.is_file():
        text = _read(path)
        head = _header(text)
        title = _TITLE.search(text)
        body = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()
                and not b.lstrip().startswith("#") and not re.match(r"^[a-z][a-z-]*:", b.strip())]
        return {"headline": title.group(1).strip() if title else qid, "text": _sentences(body[0]) if body else "",
                "strength": head.get("strength", ""), "limit": head.get("limit", ""), "url": url, "source": "report"}
    row = next((r for r in snap["questions"] if r["id"] == qid), None)
    page = snap["by_id"].get(((row or {}).get("cells", {}).get(pid) or {}).get("page", ""))
    if not page:
        return None
    # Only the headline: an old page's Opening says what the page does ("The prepared
    # SMSR2v1 cut, read once and described"), not what was found (JL 261001).
    strength = _STRENGTH.search(page["state"])
    return {"headline": page["title"], "text": "", "strength": strength.group(1) if strength else "",
            "limit": "", "url": _pop_url(snap, page), "source": "page", "page": page["id"]}


def _report_cell(snap: dict, q: dict, pid: str) -> str:
    cell = q["cells"].get(pid, _parse_cell("·"))
    if cell["mark"] == "·":
        return '<p class=wk-none>Not asked on this cut</p>'
    page = snap["by_id"].get(cell.get("page", ""))
    if cell["mark"] == "🚫" and not page:
        head, why = _REASONS.get(cell["note"], ("No answer", cell["note"]))
        return f'<p class=rp-text><b>{_e(head)}</b> · {_e(why)}</p>'
    rep = report(snap, q["id"], pid)
    if rep is None:
        return '<p class=wk-none>No report yet</p>'
    word = ("Defers to Full" if "defers" in cell["note"] else
            "Partly answered" if cell["mark"] == "🟡" else
            "No answer" if cell["mark"] == "🚫" else "")
    tags = " · ".join(x for x in (rep["strength"], rep["limit"]) if x)
    return (f'<p class=rp-label><span class=kind>Report</span>'
            + (f' <span class=mut>{_e(word)}</span>' if word else "") + '</p>'
            f'<p class=rp-title><a class=pop href="{_e(rep["url"])}" data-pop="{_e(rep["headline"])}">{_e(rep["headline"])}</a></p>'
            + (f'<p class=rp-text>{_inline(rep["text"])}</p>' if rep["text"] else "")
            + (f'<p class=rp-tags>{_e(tags)}</p>' if tags else "")
            + (f'<p class=rp-tags>page {_e(display_id(rep["page"], {p["id"]: p["name"] for p in snap["partitions"]}))}</p>'
               if rep["source"] == "page" else ""))


_DIVISION = re.compile(r"(?m)^#{3,4}\s+\d+\s+·\s+(Q[DIKW]\d+)\s+·\s+(.+?)\s*$")
_FIELD = re.compile(r"(?m)^\*\*([^*]{2,60})\*\*:\s*(.+?)\s*$")


def question_notes(snap: dict) -> dict[str, dict]:
    """question id -> its register division: short name, the ask, why it matters,
    what would answer it, and an expected answer when the register records one.
    Each MT01-MT04 register writes one `#### N · QI2 · Variant Performance`
    division per question; a question without one keeps only its Queue row."""
    if "notes" in snap:
        return snap["notes"]
    out = {}
    for q in snap["questions"]:
        reg = q["register"]
        if reg["id"] in {n.get("_reg") for n in out.values()}:
            continue
        heads = list(_DIVISION.finditer(reg["text"]))
        for i, m in enumerate(heads):
            body = reg["text"][m.end():heads[i + 1].start() if i + 1 < len(heads) else len(reg["text"])]
            body = re.split(r"(?m)^#{1,3}\s", body)[0]
            fields = {k.strip().lower(): v for k, v in _FIELD.findall(body)}
            out[m.group(1)] = {"_reg": reg["id"], "name": m.group(2),
                               "ask": fields.get("the ask", ""), "why": fields.get("why now", ""),
                               "answer": fields.get("what would answer it", ""),
                               "expect": next((v for k, v in fields.items() if "expect" in k), "")}
    snap["notes"] = out
    return out


def _logic_cell(snap: dict, q: dict, cell: dict, base: list[str]) -> str:
    """Question N · its short name, the ask, then (folded) why it matters, what
    would answer it and what was expected: rich enough to read, closed by default."""
    note = question_notes(snap).get(q["id"], {})
    short = q["question"][:1].upper() + q["question"][1:]      # the Queue row: short, plain (JL 261001)
    rows = [(label, note.get(key, "")) for label, key in
            (("The ask", "ask"), ("Why it matters", "why"), ("What would answer it", "answer"), ("Expected", "expect"))]
    rows = [(label, text) for label, text in rows if text]
    more = ('<details class=q-more><summary>More</summary><dl>'
            + "".join(f'<dt>{_e(label)}</dt><dd>{_inline(text[:1].upper() + text[1:])}</dd>' for label, text in rows)
            + '</dl></details>') if rows else ""
    # the mark sits right after its label (JL 261001): the status belongs to the question
    return (f'<div class=q-top><span class=kind>Question {_e(q["id"][2:])}</span>'
            f'<span class=mark>{_e(cell["mark"] if cell["mark"] != "·" else "")}</span></div>'
            f'{("<div class=q-title><b class=q-name>" + _e(note["name"]) + "</b></div>") if note.get("name") else ""}'
            f'<div class=q-text>{_inline(short)}</div>'
            f'{("<div class=q-sub>builds on " + _e(_numbers(base)) + "</div>") if base else ""}{more}')


def _questions_table(snap: dict, pid: str, sel: str, answered: dict) -> str:
    """One partition's table: Logic (the questions asked at each level), Work (the
    runs that answer them), Report (what each answer says).  Every audience table lists
    the same questions in the same order; only the work and the marks change.
    Cross owns no rows, so it lists only the questions that compare the cuts."""
    groups = []
    open_level = sel.split(":")[-1][1:2] if ":" in sel else ""
    for lv in "DIKW":
        rows = [q for q in snap["questions"] if q["id"][1] == lv
                and (pid != CROSS or q["cells"].get(CROSS, {}).get("mark", "·") != "·")]
        if not rows:
            continue
        body = []
        for q in rows:
            cell = q["cells"].get(pid, _parse_cell("·"))
            page = snap["by_id"].get(cell.get("page", ""))
            key = f"{pid}:{q['id']}"
            base = _builds_on(snap, page, q["id"], answered)
            muted = " dim" if cell["mark"] in {"·", "🚫"} and not page else ""
            body.append(
                f'<div class="hl-row{muted}{" on" if key == sel else ""}" data-key="{_e(key)}" '
                f'data-label="{_e(_STAGE[lv])} question {_e(q["id"][2:])} · {_e(_part_label(snap, pid))}" data-q="{_e(q["id"])}">'
                f'<div class=hl-l>{_logic_cell(snap, q, cell, base)}</div>'
                f'<div class=hl-r>{_work_cell(snap, q, pid, answered)}</div>'
                f'<div class=hl-p>{_report_cell(snap, q, pid)}</div></div>')
        reg = rows[0]["register"]
        source = (f'<a class="pop lvl-src" href="{_e(_pop_url(snap, reg))}" data-pop="{_e(reg["title"])}">'
                  f'{_e(reg["id"])} · {_e(_slug(reg))} ↗</a>')
        groups.append(f'<details class=lvl{" open" if lv == open_level else ""}><summary>{_e(_STAGE[lv])} questions '
                      f'<span class=mut>{len(rows)}</span>{source}</summary>{"".join(body)}</details>')
    row = next((p for p in snap["partitions"] if p["id"] == pid), {})
    size = f' · {row["rows"]} rows' if row.get("rows") else (" · compares the cuts" if pid == CROSS else "")
    return (f'<div class=hl data-part="{_e(pid)}"><h2>{_e(_part_label(snap, pid))}{_e(size)}</h2>'
            '<div class=hl-head><span>Logic · the question</span><span>Work · the runs</span><span>Report · what it says</span></div>'
            + "".join(groups) + '</div>')


def _render_questions(snap: dict, pid: str, sel: str) -> str:
    parts = [p["id"] for p in snap["partitions"]
             if any(p["id"] in q["cells"] for q in snap["questions"])]
    if not parts:
        return '<p class=note>No register question on this board yet. Ask one in Scope › Questions.</p>'
    pid = pid if pid in parts else parts[0]
    answered = _answered_by(snap)
    chips = "".join(f'<button type=button class="part{" on" if p == pid else ""}" data-part="{_e(p)}">{_e(_part_label(snap, p))}</button>'
                    for p in parts)
    tables = "".join(_questions_table(snap, p, sel if sel.startswith(p + ":") else "", answered) for p in parts)
    return f'<div class=parts>{chips}</div><div class=hls data-on="{_e(pid)}">{tables}</div>'


# ─── the Runs panel beside each Space ───────────────────────────────────────

def _runs_panel(space: str, kinds: list[dict]) -> str:
    """Run types on top, the runs of the chosen type below, each with its skill and a
    prompt to copy.  Picking a question narrows the runs to it.  Nothing here starts,
    sends or writes: Copy hands the prompt to a Claude or Codex session."""
    first = max(range(len(kinds)), key=lambda i: len(kinds[i]["rows"])) if kinds else 0
    buttons = "".join(f'<button type=button class="rp-type{" on" if i == first else ""}" data-k="{i}">'
                      f'{_e(k["label"])} <span class=rp-n>{len(k["rows"])}</span></button>' for i, k in enumerate(kinds))
    bodies = []
    for i, k in enumerate(kinds):
        rows = "".join(f'<li data-keys="{_e(" ".join(r.get("keys", [])))}"><a class=pop href="{_e(r["url"])}" data-pop="{_e(r["name"])}">'
                       f'{_e(r["name"])}</a> <span class=mut>{_e(r["status"])}</span></li>' if r.get("url") else
                       f'<li data-keys="{_e(" ".join(r.get("keys", [])))}">{_e(r["name"])} <span class=mut>{_e(r["status"])}</span></li>'
                       for r in k["rows"])
        bodies.append(f'<div class=rp-kind data-k="{i}"{"" if i == first else " hidden"}>'
                      f'<p class=rp-skill>Skill <code>{_e(k["skill"])}</code></p>'
                      f'<div class=rp-prompt><div class=rp-ph>Prompt <button type=button class=rp-copy>Copy</button></div>'
                      f'<pre data-base="{_e(k["prompt"])}">{_e(k["prompt"])}</pre></div>'
                      f'<ul class=rp-runs>{rows}</ul><p class=rp-empty{"" if not k["rows"] else " hidden"}>No runs yet.</p></div>')
    # Folded to a thin strip by default, like the Paper and Page workbenches; the
    # person's choice is remembered per Space (JL 261001: runs hidden until wanted).
    return (f'<aside class="rp folded" data-space="{_e(space)}"><div class=rp-head>'
            f'<button type=button class=rp-fold title="Open or fold the runs">◂</button><b>Runs</b> '
            f'<span class="rp-for mut"></span></div>'
            f'<div class=rp-body><div class=rp-types>{buttons}</div>{"".join(bodies)}</div></aside>')


def _resting(snap: dict) -> dict[tuple[str, str], set[str]]:
    """(partition, lower question) -> the Knowledge and Wisdom answers that rest on it,
    so picking a K or W question shows the runs behind its answer."""
    if "resting" in snap:
        return snap["resting"]
    answered, out = _answered_by(snap), {}
    for q in snap["questions"]:
        if q["id"][1] not in "KW":
            continue
        for pid, cell in q["cells"].items():
            for lower in _behind(snap, snap["by_id"].get(cell.get("page", "")), answered):
                out.setdefault((pid, lower), set()).add(q["id"])
    snap["resting"] = out
    return out


def _run_rows(snap: dict, level: str) -> list[dict]:
    resting = _resting(snap)
    called: dict[int, set[str]] = {}          # run -> the cells whose page tickets call it
    for page in snap["pages"]:
        cells = [(q, p) for q, p in page_cells(snap, page) if q[1] == level]
        for r in page_tickets(snap, page) if cells else []:
            called.setdefault(id(r), set()).update(f"{p}:{q}" for q, p in cells)
    out = []
    for r in work_runs(snap):
        mine = [a for a in r["answers"] if a[1] == level]
        if mine or id(r) in called:
            where = r["partition"] or CROSS
            keys = {f"{w}:{a}" for a in mine for w in (where, CROSS)} | called.get(id(r), set())
            keys |= {f"{w}:{up}" for a in mine for w in (where, CROSS) for up in resting.get((w, a), ())}
            out.append({"name": f'{r["task"]} · {r["call"]}', "status": r["status"], "url": _run_url(snap, r),
                        "keys": sorted(keys)})
    return out


def _report_rows(snap: dict) -> list[dict]:
    """Every report file on the board, keyed to its question and partition."""
    names = {p["name"]: p["id"] for p in snap["partitions"]}
    out = []
    for path in sorted((snap["board"] / "reports").glob("*/Q[DIKW]*.md")):
        pid = names.get(path.parent.name, path.parent.name)
        out.append({"name": f"{path.stem} · {_part_label(snap, pid)}", "status": _field(_read(path), "strength") or "written",
                    "url": f"/_board/insight?board={quote(snap['board'].name)}&report={quote(pid + ':' + path.stem)}",
                    "keys": [f"{pid}:{path.stem}"]})
    return out


def _space_kinds(snap: dict) -> dict[str, list[dict]]:
    rel = snap["relative"]
    return {
        "scope": [
            {"label": "Prepare extract", "skill": "haipipe-task", "rows": [],
             "prompt": f"/haipipe-task: prepare the extract this board reads; MT00 records it ({rel})."},
            {"label": "Ask", "skill": "haipipe-insight-question", "rows": [],
             "prompt": f'/haipipe-insight application {rel} question "<your question>"'},
        ],
        "insight": [
            {"label": "Data runs", "skill": "haipipe-task", "rows": _run_rows(snap, "D"),
             "prompt": "/haipipe-task: run the task call that answers {question} on {partition}; its config lists it under answers:."},
            {"label": "Information runs", "skill": "haipipe-task", "rows": _run_rows(snap, "I"),
             "prompt": "/haipipe-task: run the task call that answers {question} on {partition}; its config lists it under answers:."},
            {"label": "Report", "skill": "haipipe-insight-data · -information · -knowledge · -wisdom",
             "rows": _report_rows(snap),
             "prompt": f"/haipipe-insight application {rel} report {{question}} {{partition}}: read the runs that "
                       "answer it and write reports/<partition>/<question>.md (headline, answer, strength, limit, runs)."},
            {"label": "Pool or split", "skill": "haipipe-insight-workflow", "rows": [],
             "prompt": f"/haipipe-insight application {rel} verdict"},
        ],
        "check": [
            {"label": "Mechanical check", "skill": "cli/check.py", "rows": [],
             "prompt": f"/haipipe-insight application {rel} check"},
            {"label": "Answer review", "skill": "haipipe-page-check", "rows": [],
             "prompt": f"/haipipe-insight application {rel} review {{question}} {{partition}}"},
        ],
        "delivery": [
            {"label": "Handoff draft", "skill": "haipipe-insight-wisdom", "rows": [],
             "prompt": f"/haipipe-insight application {rel} handoff {{question}} {{partition}}"},
        ],
    }


# ─── the Spaces ─────────────────────────────────────────────────────────────

_WORDS = {w: str(i) for i, w in enumerate(("zero one two three four five six seven eight nine ten eleven "
                                            "twelve thirteen fourteen fifteen").split())}


def _short_window(a: str, b: str) -> str:
    """`2025-06-16`, `2025-07-03` -> `Jun 16 – Jul 3, 2025`."""
    d1, d2 = date.fromisoformat(a), date.fromisoformat(b)
    left = f"{d1:%b} {d1.day}" + ("" if d1.year == d2.year else f", {d1.year}")
    return f"{left} – {d2:%b} {d2.day}, {d2.year}"


def _dataset_line(snap: dict) -> tuple[str, str]:
    """(short line, full extract name) for the banner every Space shows:
    `SMSR2v1 · 444,691 rows · 13 messages · Jun 16 – Jul 3, 2025` (JL 261001: too wordy)."""
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


def _render_scope(snap: dict) -> str:
    prow = "".join(
        f'<tr><td><b>{_e(_part_label(snap, r["id"]))}</b></td><td class=mono>{_e(r["where"] or ("no rows of its own" if r["id"] == CROSS else "—"))}</td>'
        f'<td class=num>{_e(r["rows"] or "—")}</td><td class=num>{_e(r["share"] or "—")}</td>'
        f'<td class=mono>{_e((r.get("config") or "—") + (".yaml" if r.get("config") else ""))}</td></tr>'
        for r in snap["partitions"])
    partitions = ('<h2>Partitions</h2><p class=lead>Cuts of this one extract, from MT00. A cut is one config per task, never a second dataset.</p>'
                  f'<div class=scroll><table><tr><th>Partition</th><th>Where</th><th>Rows</th><th>Share</th><th>Config</th></tr>{prow}</table></div>')
    counts = "".join(f'<li>{_e(_STAGE[lv])} questions <span class=mut>{sum(q["id"][1] == lv for q in snap["questions"])}</span></li>'
                     for lv in "DIKW")
    ask = ('<h2>Questions</h2><ul class=counts>' + counts + '</ul>'
           '<p class=lead>Type the question. Claude Code decides its level, the cuts it runs on and what it grows out of, then registers it. It never answers it here.</p>'
           f'<form id=askform class=form data-root="{_e(snap["relative"])}">'
           '<div class="field full"><textarea id=ask-text required placeholder="e.g. does the send hour change which message works best?"></textarea></div>'
           '<div class="full actions"><button class="btn primary" type=submit>Ask</button><span class=status id=ask-status></span></div></form>'
           '<div id=ask-out hidden><p class=mut>Give this to Claude Code (copied to your clipboard):</p><p><code id=ask-cmd></code></p></div>')
    return (_tabs([("dataset", "Dataset"), ("partitions", "Partitions"), ("questions", "Questions")])
            + _view("dataset", _render_input_data(snap), True) + _view("partitions", partitions) + _view("questions", ask))


def _gate_blocks(snap: dict) -> str:
    """The seven gates of every answered cell; the picked question shows its own."""
    out = []
    for q in snap["questions"]:
        for pid, cell in q["cells"].items():
            if cell["mark"] == "·" or (cell["mark"] == "🚫" and not cell["page"]):
                continue
            view = _cell_view(snap, q["id"], pid)
            out.append(f'<div class=gateset data-key="{_e(pid)}:{_e(q["id"])}" hidden>'
                       f'<p class=mut>{_e(_STAGE[q["id"][1]])} question {_e(q["id"][2:])} · {_e(_part_label(snap, pid))}</p><div class=gates>'
                       + "".join(f'<div class="gate {g["state"]}"><span class=k>{_e(g["key"])}</span><span class=n>{_e(g["name"])}</span>'
                                 f'<span class=who><span class="pill {"human" if g["who"] == "person" else "acc" if g["who"] == "agent" else ""}">'
                                 f'{_e(g["who"])}</span> {_e(g["state"])}</span>'
                                 f'{("<span class=n>" + _e(_clip(g["note"], 90)) + "</span>") if g["note"] else ""}</div>'
                                 for g in view["gates"]) + '</div></div>')
    return ('<h2>Gates</h2><p class=lead>Pick a question in Insight; its gates show here. A gate is closed by its owner, never by this screen.</p>'
            + "".join(out) + '<p class="note gate-none">The picked question has no gates on this cut.</p>')


def _render_check(snap: dict) -> str:
    groom = groom_snapshot(snap["board"], snap)
    crow = "".join(
        f'<tr><td>{_pill("🚫" if c["level"] == "FAIL" else "🟡" if c["level"] == "WARN" else "✅", c["level"])}</td>'
        f'<td class=mono>{_e(c["where"])}</td><td>{_inline(c["message"])}</td></tr>' for c in groom["checks"])
    mech = f'<h2>Checks</h2><p class=lead>From <code>cli/check.py</code>, whole board.</p><table><tr><th>Level</th><th>Where</th><th>Finding</th></tr>{crow}</table>'
    return (_tabs([("gates", "Gates"), ("checks", "Checks"), ("runtime", "Runtime")])
            + _view("gates", _gate_blocks(snap), True) + _view("checks", mech)
            + _view("runtime", _render_runtime_inventory(snap)))


def _render_delivery(snap: dict) -> str:
    """What leaves this board: person-signed Wisdom answers a DesignBoard may use."""
    hrows = "".join(
        f'<tr><td><a class=pop href="{_e(_pop_url(snap, h["record"]))}" data-pop="{_e(h["title"])}">{_e(h["title"])}</a></td>'
        f'<td class=mono>{_e(h["serves"])}</td>'
        f'<td>{_pill("✅" if h["bindable"] else "🟡", h["eligibility"])} · {_e(h["eligibility_reason"])}</td></tr>'
        for h in snap["handoffs"]) or '<tr><td colspan=3 class=mut>No Wisdom answer is ready to leave this board yet.</td></tr>'
    ready = sum(h["bindable"] for h in snap["handoffs"])
    return (_tabs([("handoff", "Handoff")])
            + _view("handoff", f'<h2>Handoff</h2><p class=lead>{ready} signed Wisdom answer{"" if ready == 1 else "s"} ready for design. '
                    'Only a signed, current handoff leaves this board.</p>'
                    f'<table><tr><th>Wisdom answer</th><th>Serves</th><th>Current eligibility</th></tr>{hrows}</table>', True))


def render_insight_board(snapshot: dict, space: str = "insight",
                         selected_question: str = "", selected_partition: str = "") -> str:
    snap = snapshot
    aliases = {"overview": "scope", "registers": "scope", "partitions": "scope", "workspace": "scope",
               "evidence": "insight", "run": "check", "workflow": "check", "groom": "check"}
    space = aliases.get(space, space)
    if space not in {k for k, _ in _SPACES}:
        space = "insight"
    qids = snap["question_ids"]
    pids = [row["id"] for row in snap["partitions"]]
    qid = selected_question if selected_question in qids else ("QW1" if "QW1" in qids else (qids[0] if qids else ""))
    pid = selected_partition if selected_partition in pids else (FULL if FULL in pids else (pids[0] if pids else ""))
    sel = f"{pid}:{qid}" if qid and pid else ""
    kinds = _space_kinds(snap)
    bodies = {"scope": _render_scope(snap), "insight": _tabs([("questions", "Questions")])
              + _view("questions", _render_questions(snap, pid, sel), True),
              "check": _render_check(snap), "delivery": _render_delivery(snap)}
    nav = '<nav class=spaces>' + "".join(f'<button class=space type=button data-space="{k}">{label}</button>'
                                         for k, label in _SPACES) + '</nav>'
    panes = "".join(f'<section class=pane data-space="{k}"><div class=split><div class=shell>{bodies[k]}</div>'
                    f'{_runs_panel(k, kinds[k])}</div></section>' for k, _ in _SPACES)
    links = ('<a class=board-index href="index.html">board index</a>' if snap["static"] else
             f'<a href="/">all boards</a> · <a href="/{_e(snap["relative"])}/board/index.html">board index</a>')
    return _spell_ids(snap, "".join([
        '<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">',
        f'<title>🔎 {_e(snap["title"])}</title><style>{_CSS}</style></head>'
        f'<body data-space="{_e(space)}" data-sel="{_e(sel)}"><main>',
        f'<header><h1>🔎 {_e(snap["title"])}</h1><div class=mut>{links}</div></header>',
        '<div class=dataset title="{1}">{0}</div>'.format(*map(_e, _dataset_line(snap))),
        nav, panes, _POP, "</main>", _JS, "</body></html>",
    ]))


# ─── pop-outs: a run's results, a page as a document ────────────────────────

def _result_kit():
    from .paper import _RESULT_PAGE, _csv_view, _md_view
    return _RESULT_PAGE, _csv_view, _md_view


def render_insight_run(snap: dict, task_rel: str, call: str, page: str = "") -> str:
    """One task call's results: its receipt, then summaries, figures, tables and
    every other file.  The run's results are the answer; no page stands between."""
    page_tpl, csv_view, md_view = _result_kit()
    root = Path(snap["root"]).resolve()
    run = next((r for r in work_runs(snap) if r["call"] == call and r.get("page", "") == page and
                r["task_path"].resolve().relative_to(_tasks_root(snap).resolve()).as_posix() == task_rel.strip("/")), None)
    if run is None:
        raise FileNotFoundError(f"{task_rel} · {call}")
    raw = lambda f: "/" + quote(f.resolve().relative_to(root).as_posix(), safe="/")
    inside = lambda f: f.resolve().is_relative_to(root)
    res = run["receipt"].parent
    files = sorted(f for f in res.rglob("*") if f.is_file() and not f.name.startswith(".")) if res.is_dir() else []
    qa = sorted((res.parent.parent / "QA").glob("*.md")) if (res.parent.parent / "QA").is_dir() else []
    links = [f'<a href="{_e(raw(f))}" target=_blank rel=noopener>{label} ↗</a>'
             for f, label in ((run["ticket"], "Run script"), (run["config"], "Config")) if f and f.is_file() and inside(f)]
    body = [f'<h1>{_e(call)}</h1><p class="where mut"><code>{_e(res.resolve().relative_to(root).as_posix() if inside(res) else res.name)}</code>'
            f' · answers {_e(", ".join(run["answers"]) or "no question")}</p>', f'<div class=links>{"".join(links)}</div>']
    if run["receipt"].is_file():
        body.append(f'<h2>Receipt</h2><pre>{_e(_read(run["receipt"])[:4000])}</pre>')
    else:
        body.append('<p class=mut>Not run yet: no receipt.</p>')
    docs = qa + [f for f in files if f.suffix.lower() in {".md", ".txt"}]
    if docs:
        body.append(f'<h2>Summaries · {len(docs)}</h2>' + "".join(
            f'<div class=doc><h3>{_e(f.name)}</h3>{md_view(_read(f)) if f.stat().st_size < 200_000 else "<p class=mut>too long to show here</p>"}</div>'
            for f in docs))
    figs = [f for f in files if f.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg", ".webp"}]
    if figs:
        body.append(f'<h2>Figures · {len(figs)}</h2><div class=figs>' + "".join(
            f'<figure><img loading=lazy src="{_e(raw(f))}" alt="{_e(f.name)}"><figcaption>{_e(f.name)}</figcaption></figure>'
            for f in figs if inside(f)) + '</div>')
    tabs = [f for f in files if f.suffix.lower() in {".csv", ".tsv"}]
    for f in tabs:
        if f is tabs[0]:
            body.append(f'<h2>Tables · {len(tabs)}</h2>')
        body.append(f'<h3>{_e(f.name)}</h3>{csv_view(f)}')
    rest = [f for f in files if f not in docs and f not in figs and f not in tabs and f != run["receipt"]]
    if rest:
        body.append(f'<h2>Other files · {len(rest)}</h2><ul class=files>' + "".join(
            f'<li><a href="{_e(raw(f))}" target=_blank rel=noopener>{_e(f.name)}</a></li>' if inside(f) else f'<li>{_e(f.name)}</li>'
            for f in rest) + '</ul>')
    return page_tpl.format(title=_e(call), body="\n".join(body))


def render_insight_report(snap: dict, qid: str, pid: str) -> str:
    """One report file as a document, for the pop-out."""
    page_tpl, _, md_view = _result_kit()
    text = _read(_report_path(snap, qid, pid))
    title = _TITLE.search(text)
    body = re.sub(r"\A#[^\n]*\n", "", text)
    return page_tpl.format(title=_e(title.group(1) if title else qid), body=(
        f'<h1>{_e(title.group(1).strip() if title else qid)}</h1>'
        f'<p class="where mut">{_e(_STAGE.get(qid[1:2], ""))} question {_e(qid[2:])} on {_e(_part_label(snap, pid))}</p>'
        + md_view(body)))


def render_insight_page(snap: dict, page: dict) -> str:
    """One page as a document, for the pop-out: what it answers, then its text."""
    page_tpl, _, md_view = _result_kit()
    cells = page_cells(snap, page)
    where = " · ".join(f'{_STAGE[q[1]]} question {q[2:]} on {_part_label(snap, p)}' for q, p in cells) or "answers no register question"
    text = re.sub(r"\A#[^\n]*\n", "", page["text"])
    body = (f'<h1>{_e(page["title"])}</h1><p class="where mut">{_e(display_id(page["id"], {p["id"]: p["name"] for p in snap["partitions"]}))}'
            f' · {_e(_clip(page["state"], 90))} · {_e(where)}</p>'
            f'<div class=links><a href="{_e(_page_link(snap, page))}" target=_blank rel=noopener>Open the Markdown ↗</a></div>'
            f'{md_view(text)}')
    return page_tpl.format(title=_e(page["title"]), body=body)


_CSS = """
:root{--bg:#fff;--fg:#1c1c1c;--mut:#6f6f6b;--line:#e3e3e6;--soft:#f4f5f7;--acc:#3e5c84;--acc-soft:#e6edf5;--ok:#3a7d44;--ok-soft:#e5f1e7;--warn:#b3541e;--warn-soft:#f8ebe1;--bad:#8a3b3b;--bad-soft:#f5e6e6;--human:#6b4fa0;--human-soft:#ede8f6}
@media(prefers-color-scheme:dark){:root{--bg:#161719;--fg:#e8e8e6;--mut:#a0a09c;--line:#2c2e33;--soft:#212429;--acc:#8aa7cc;--acc-soft:#22304a;--ok:#7dbb87;--ok-soft:#1f3324;--warn:#e0955a;--warn-soft:#3a2a1c;--bad:#d98b8b;--bad-soft:#3a2323;--human:#b39ddb;--human-soft:#2c2540}}
*{box-sizing:border-box}body{margin:0;padding:16px;background:var(--bg);color:var(--fg);font:16px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
main{max-width:1600px}h1{font-size:18px;margin:0 0 2px}h2{font-size:17px;margin:0 0 6px}h3{font-size:15px;margin:14px 0 6px}p{margin:4px 0}
.mut{color:var(--mut);font-size:13px}code,.mono{font:13px ui-monospace,Menlo,monospace}a{color:var(--acc)}
.dataset{margin:10px 0 4px;padding:8px 14px;border:1px solid var(--acc);border-radius:10px;background:var(--acc-soft);color:var(--acc);font-size:14px}
.spaces{display:flex;gap:6px;margin:12px 0 8px;flex-wrap:wrap}.space{font:600 13px -apple-system,sans-serif;border:1px solid var(--line);border-radius:8px;padding:5px 12px;cursor:pointer;background:var(--bg);color:var(--fg)}.space.on{border-color:var(--acc);color:var(--acc);background:var(--acc-soft)}
.pane{display:none}.pane.on{display:block}.split{display:flex;align-items:flex-start;gap:14px}
.shell{flex:1 1 auto;border:1px solid var(--line);border-radius:10px;padding:12px 16px 16px;min-width:0;overflow-x:auto}
.wtabs{display:flex;gap:6px;flex-wrap:wrap;padding:0 0 10px;margin:0 0 12px;border-bottom:1px solid var(--line)}.wtab{font:500 13px -apple-system,sans-serif;border:1px solid var(--line);border-radius:8px;padding:5px 11px;cursor:pointer;background:transparent;color:var(--fg)}.wtab.on{border-color:var(--acc);color:var(--acc);font-weight:650}
.view{display:none}.view.on{display:block}.lead{margin:0 0 12px;color:var(--mut);font-size:14px}.note{border:1px dashed var(--line);border-radius:8px;padding:10px 12px;color:var(--mut);font-size:14px}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}td,th{padding:7px 9px;border:1px solid var(--line);text-align:left;vertical-align:top}th{background:var(--soft);color:var(--mut);font-size:12px;font-weight:650}td.num{text-align:right;font-family:ui-monospace,Menlo,monospace;font-size:13px}.scroll{overflow-x:auto}
.inputs td:first-child{background:var(--soft);color:var(--mut);width:160px}.inputs td{overflow-wrap:anywhere}
.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:1px 8px;font-size:12px;color:var(--mut);white-space:nowrap}.pill.ok{color:var(--ok);border-color:var(--ok);background:var(--ok-soft)}.pill.warn{color:var(--warn);border-color:var(--warn);background:var(--warn-soft)}.pill.bad{color:var(--bad);border-color:var(--bad);background:var(--bad-soft)}.pill.acc{color:var(--acc);border-color:var(--acc);background:var(--acc-soft)}.pill.human{color:var(--human);border-color:var(--human);background:var(--human-soft)}
.parts{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 12px}.part{font:500 13px -apple-system,sans-serif;border:1px solid var(--line);border-radius:8px;padding:5px 11px;cursor:pointer;background:transparent;color:var(--fg)}.part.on{border-color:var(--acc);color:var(--acc);background:var(--acc-soft);font-weight:650}
.hl{display:none;min-width:760px}.hl.on{display:block}.hl-head{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;padding:6px 10px;border-bottom:1px solid var(--line);color:var(--mut);font-size:13px}
details.lvl{border-bottom:1px solid var(--line)}details.lvl>summary{cursor:pointer;padding:9px 10px;font-weight:650;background:var(--soft)}details.lvl>summary .mut{font-weight:400;margin-left:6px}
.hl-row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;padding:10px 10px;border-top:1px solid var(--line);cursor:pointer}.hl-row:hover{background:var(--soft)}.hl-row.on{background:var(--acc-soft)}.hl-row.dim .hl-l{opacity:.6}
.hl-l,.hl-r,.hl-p{min-width:0}.hl-r,.hl-p{border-left:1px solid var(--line);padding-left:14px}
.rp-head{margin:0;font-weight:600}.rp-head a{color:inherit}.rp-text{margin:3px 0 0;font-size:14.5px}.rp-label{margin:0}.rp-title{margin:4px 0 0;font-weight:600}.rp-title a{color:inherit}.rp-tags{margin:3px 0 0;color:var(--mut);font-size:12.5px}
.q-top{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.q-title{margin:4px 0 0}.wk-title{margin:4px 0 0}.q-name{font-size:15px}
.lvl-src{float:right;font-weight:400;font-size:13px}
details.q-more{margin-top:4px;font-size:13.5px}details.q-more>summary{cursor:pointer;color:var(--acc);list-style:none}details.q-more>summary::before{content:'› '}details.q-more[open]>summary::before{content:'⌄ '}
.q-more dl{margin:4px 0 0}.q-more dt{color:var(--mut);font-size:12.5px;margin-top:6px}.q-more dd{margin:1px 0 0}.kind{display:inline-block;font:650 12px -apple-system,sans-serif;color:var(--acc);border:1px solid var(--acc);border-radius:999px;padding:0 8px;margin-right:4px}.q-text{margin-top:3px}.q-sub,.wk-sub{display:block;color:var(--mut);font-size:13px;margin-top:2px}
.wk-none{color:var(--mut);font-size:14px;margin:0}.wk-page{margin:4px 0}details.wk>summary{cursor:pointer;list-style:none}details.wk>summary::-webkit-details-marker{display:none}details.wk>summary::before{content:'› ';color:var(--mut)}details.wk[open]>summary::before{content:'⌄ '}
.bj{padding:4px 0 2px 14px;font-size:13.5px}.bj-b{margin-top:4px}.bj-j{margin-left:16px}.bj-tr{margin-left:32px}.bj-tr.bj-flat{margin-left:16px}.bj-tr>summary{cursor:pointer;list-style:none}.bj-tr>summary::-webkit-details-marker{display:none}.bj-runs{margin-left:18px}.bj-run{display:block;text-decoration:none;color:inherit;padding:1px 0;overflow-wrap:anywhere}.bj-run:hover{color:var(--acc)}.idtag{font:13px ui-monospace,Menlo,monospace;color:var(--mut)}
.rp{flex:0 0 clamp(260px,28vw,420px);border:1px solid var(--line);border-radius:10px;background:var(--soft);padding:12px;position:sticky;top:8px;min-width:0;max-height:calc(100vh - 16px);overflow:auto}
.rp-head{display:flex;align-items:center;gap:8px;margin-bottom:8px}.rp-fold{border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);cursor:pointer;padding:0 7px;font-size:13px}
.rp.folded{flex-basis:42px;padding:10px 6px;cursor:pointer;overflow:hidden}.rp.folded .rp-body,.rp.folded .rp-for{display:none}.rp.folded .rp-head{writing-mode:vertical-rl;margin:0}.rp-types{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
.rp-type{font:500 13px -apple-system,sans-serif;border:1px solid var(--line);border-radius:8px;padding:5px 10px;cursor:pointer;background:var(--bg);color:var(--fg)}.rp-type.on{border-color:var(--acc);color:var(--acc);background:var(--acc-soft)}.rp-n{color:var(--mut);margin-left:3px}
.rp-kind{background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:10px 12px}.rp-skill{font-size:13px;color:var(--ok)}.rp-ph{display:flex;justify-content:space-between;align-items:center;font-weight:600;font-size:14px;margin-top:6px}
.rp-copy{font:500 12px -apple-system,sans-serif;border:1px solid var(--line);border-radius:6px;padding:2px 8px;cursor:pointer;background:var(--bg);color:var(--fg)}.rp-prompt pre{white-space:pre-wrap;font:12.5px/1.5 ui-monospace,Menlo,monospace;background:var(--soft);padding:8px;border-radius:6px;margin:6px 0}
.rp-runs{list-style:none;margin:8px 0 0;padding:0;max-height:420px;overflow:auto;font-size:13.5px}.rp-runs li{padding:3px 0;border-top:1px solid var(--line)}.rp-empty{color:var(--mut);font-size:13px}
.gates{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));border:1px solid var(--line);border-radius:8px;overflow:hidden}.gate{padding:8px 9px;border-right:1px solid var(--line);font-size:13px;min-width:0;overflow-wrap:anywhere}.gate:last-child{border-right:0}.gate .k{font:650 13px ui-monospace,Menlo,monospace}.gate .n{display:block;color:var(--mut)}.gate.passed{box-shadow:inset 0 3px 0 var(--ok)}.gate.held{box-shadow:inset 0 3px 0 var(--human)}.gate.refused{box-shadow:inset 0 3px 0 var(--bad)}.gate.pending,.gate.skipped{color:var(--mut)}.gate .who{display:block;margin-top:3px}
.counts{margin:0 0 12px;padding-left:18px}.form{display:grid;gap:12px}.field textarea{width:100%;min-height:64px;border:1px solid var(--line);border-radius:7px;padding:8px;font:15px -apple-system,sans-serif;background:var(--bg);color:var(--fg)}
.btn{border:1px solid var(--acc);border-radius:8px;padding:8px 13px;background:var(--acc);color:#fff;font:650 14px -apple-system,sans-serif;cursor:pointer}.actions{display:flex;gap:10px;align-items:center}.status{font-size:13px;color:var(--mut)}
.pop-bg{position:fixed;inset:0;background:rgba(0,0,0,.35);display:flex;align-items:center;justify-content:center;z-index:50}.pop-bg[hidden]{display:none}.pop-box{width:min(1100px,94vw);height:88vh;background:var(--bg);border-radius:12px;display:flex;flex-direction:column;overflow:hidden}
.pop-bar{display:flex;align-items:center;gap:12px;padding:8px 14px;border-bottom:1px solid var(--line)}.pop-title{font-weight:650;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.pop-x{border:0;background:transparent;font-size:20px;cursor:pointer;color:var(--fg)}.pop-frame{flex:1;border:0;width:100%}
@media(max-width:820px){.gates{grid-template-columns:repeat(4,1fr)}}
@media(max-width:600px){body{padding:12px}.spaces{flex-wrap:nowrap;overflow-x:auto}.shell{padding:10px}}
"""

_POP = ('<div class=pop-bg hidden><div class=pop-box><div class=pop-bar><span class=pop-title></span>'
        '<a class=pop-new target=_blank rel=noopener>Open in its own tab ↗</a>'
        '<button type=button class=pop-x aria-label=Close>×</button></div><iframe class=pop-frame></iframe></div></div>')

_JS = """<script>(function(){
var body=document.body;
function setUrl(k,v){try{var u=new URL(location.href);u.searchParams.set(k,v);history.replaceState({},'',u)}catch(e){}}
var sp=[].slice.call(document.querySelectorAll('.space')),pn=[].slice.call(document.querySelectorAll('.pane'));
function space(s,w){if(!document.querySelector('.pane[data-space="'+s+'"]'))s='insight';body.dataset.space=s;sp.forEach(function(b){b.classList.toggle('on',b.dataset.space===s)});pn.forEach(function(p){p.classList.toggle('on',p.dataset.space===s)});if(w)setUrl('space',s)}
sp.forEach(function(b){b.onclick=function(){space(b.dataset.space,true)}});
document.querySelectorAll('.shell').forEach(function(sh){var tabs=[].slice.call(sh.querySelectorAll('.wtab'));function sync(){var on=sh.querySelector('.wtab.on');sh.querySelectorAll('.view').forEach(function(v){v.classList.toggle('on',!!on&&v.dataset.view===on.dataset.view)})}tabs.forEach(function(t){t.onclick=function(){tabs.forEach(function(x){x.classList.toggle('on',x===t)});sync();setUrl('view',t.dataset.view)}});sync()});
try{var vw=new URL(location.href).searchParams.get('view');if(vw)document.querySelectorAll('.pane[data-space="'+body.dataset.space+'"] .wtab[data-view="'+vw+'"]').forEach(function(t){t.click()})}catch(e){}
function part(p,w){document.querySelectorAll('.part').forEach(function(b){b.classList.toggle('on',b.dataset.part===p)});document.querySelectorAll('.hl').forEach(function(t){t.classList.toggle('on',t.dataset.part===p)});if(w)setUrl('p',p)}
document.querySelectorAll('.part').forEach(function(b){b.onclick=function(){part(b.dataset.part,true)}});
var hs=document.querySelector('.hls');if(hs)part(hs.dataset.on,false);
function label(){var r=document.querySelector('.hl-row[data-key="'+body.dataset.sel+'"]');return r?r.dataset.label:''}
function pick(key){body.dataset.sel=key;var lab=label(),k=key.split(':');
 document.querySelectorAll('.hl-row').forEach(function(r){r.classList.toggle('on',r.dataset.key===key)});
 document.querySelectorAll('.rp:not([data-space=scope]) .rp-for').forEach(function(s){s.textContent=lab?'· '+lab:''});
 document.querySelectorAll('.rp-runs li').forEach(function(li){var ks=(li.dataset.keys||'').split(' ');li.hidden=!!key&&ks.indexOf(key)<0});
 document.querySelectorAll('.rp').forEach(function(rp){var best=null;rp.querySelectorAll('.rp-kind').forEach(function(kd){var shown=[].slice.call(kd.querySelectorAll('.rp-runs li')).filter(function(li){return !li.hidden}).length;kd.querySelector('.rp-empty').hidden=shown>0;var t=rp.querySelector('.rp-type[data-k="'+kd.dataset.k+'"]');t.querySelector('.rp-n').textContent=shown;if(shown&&best===null)best=t});
  var on=rp.querySelector('.rp-type.on');if(best&&on&&on.querySelector('.rp-n').textContent==='0')showType(rp,best)});
 document.querySelectorAll('.rp-prompt pre').forEach(function(pre){pre.textContent=pre.dataset.base.replace(/\\{question\\}/g,k[1]||'<question>').replace(/\\{partition\\}/g,k[0]||'<partition>')});
 var any=false;document.querySelectorAll('.gateset').forEach(function(g){g.hidden=g.dataset.key!==key;any=any||!g.hidden});document.querySelectorAll('.gate-none').forEach(function(n){n.hidden=any});
 if(k.length===2){setUrl('q',k[1]);setUrl('p',k[0])}}
document.querySelectorAll('.hl-row').forEach(function(r){r.addEventListener('click',function(ev){if(ev.target.closest('a,summary'))return;pick(r.dataset.key===body.dataset.sel?'':r.dataset.key)})});
function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
document.querySelectorAll('.rp').forEach(function(rp){var key='insight-runs-open:'+rp.dataset.space,fb=rp.querySelector('.rp-fold');
 function setFold(on){rp.classList.toggle('folded',on);fb.textContent=on?'◂':'▸';store(key,on?'0':'1')}
 fb.addEventListener('click',function(ev){ev.stopPropagation();setFold(!rp.classList.contains('folded'))});
 rp.addEventListener('click',function(ev){if(rp.classList.contains('folded'))setFold(false)});
 if(store(key)==='1')setFold(false)});
function showType(rp,t){rp.querySelectorAll('.rp-type').forEach(function(x){x.classList.toggle('on',x===t)});rp.querySelectorAll('.rp-kind').forEach(function(k){k.hidden=k.dataset.k!==t.dataset.k})}
document.querySelectorAll('.rp').forEach(function(rp){rp.querySelectorAll('.rp-type').forEach(function(t){t.onclick=function(){showType(rp,t)}})});
document.querySelectorAll('.rp-copy').forEach(function(b){b.onclick=function(){var t=b.closest('.rp-prompt').querySelector('pre').textContent;try{navigator.clipboard.writeText(t).then(function(){b.textContent='Copied'},function(){b.textContent='Select it'})}catch(e){b.textContent='Select it'}}});
var bg=document.querySelector('.pop-bg');
document.addEventListener('click',function(ev){var a=ev.target.closest&&ev.target.closest('a.pop');if(a&&bg&&!(ev.metaKey||ev.ctrlKey)){ev.preventDefault();bg.querySelector('.pop-title').textContent=a.dataset.pop||a.textContent;bg.querySelector('.pop-new').href=a.href;bg.querySelector('.pop-frame').src=a.href;bg.hidden=false;return}
 if(bg&&!bg.hidden&&(ev.target===bg||(ev.target.closest&&ev.target.closest('.pop-x')))){bg.hidden=true;bg.querySelector('.pop-frame').src='about:blank'}},true);
document.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&bg&&!bg.hidden){bg.hidden=true;bg.querySelector('.pop-frame').src='about:blank'}});
var f=document.getElementById('askform');if(f){f.onsubmit=function(ev){ev.preventDefault();var q=document.getElementById('ask-text').value.replace(/\\s+/g,' ').trim();if(!q)return;
var cmd='/haipipe-insight application '+f.dataset.root+' question "'+q.replace(/"/g,"'")+'"';document.getElementById('ask-cmd').textContent=cmd;document.getElementById('ask-out').hidden=false;
var st=document.getElementById('ask-status');if(navigator.clipboard){navigator.clipboard.writeText(cmd).then(function(){st.textContent='copied'},function(){st.textContent='select and copy the line below'})}else{st.textContent='select and copy the line below'}}}
space(body.dataset.space,false);pick(body.dataset.sel||'');
})();</script>"""



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
            snapshot, (query.get("space") or ["insight"])[0],
            (query.get("q") or query.get("question") or [""])[0],
            (query.get("p") or query.get("partition") or [""])[0],
        ).encode("utf-8")
        return self._insight_board_send(body, 200 if snapshot["current"] else 404, head_only)

    def insight_page_view(self, head_only=False):
        """GET /_board/insight?path=<board>&file=<page.md>: one page as a document (the pop-out)."""
        query = parse_qs(urlparse(self.path).query)
        payload = {"path": (query.get("path") or [""])[0], "file": (query.get("file") or [""])[0]}
        short_board = (query.get("board") or [""])[0]
        short_page = (query.get("page") or [""])[0].strip()     # `W02-full`: ids keep their case
        wanted = (query.get("report") or [""])[0]
        if short_board and ":" in wanted:
            # ?board=<name>&report=<partition>:<question>: one report file as a document
            board = _board_by_name(Path(self.root), short_board)
            snap = board_snapshot(board, self.root) if board else None
            pid, qid = wanted.split(":", 1)
            path = _report_path(snap, qid, pid) if snap else None
            if path is None or not path.is_file():
                return self._insight_board_send(f"<p>No report {_e(wanted)} on this board.</p>".encode("utf-8"), 404, head_only)
            return self._insight_board_send(render_insight_report(snap, qid, pid).encode("utf-8"), 200, head_only)
        if short_board and short_page:
            # Short form for a terminal: ?board=<folder name>&page=<page id>.
            board = _board_by_name(Path(self.root), short_board)
            hit = next((p for p in (_pages(board) if board else []) if p["id"].lower() == short_page.lower()), None)
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
        body = render_insight_page(snapshot, page).encode("utf-8")
        return self._insight_board_send(body, 200 if snapshot["current"] else 404, head_only)

    def insight_run_view(self, head_only=False):
        """GET /_board/insight-run?board=<name>&task=<task folder>&call=<call>: one run's results."""
        query = parse_qs(urlparse(self.path).query)
        board = self._insight_target((query.get("board") or [""])[0])
        if board is None:
            return self._insight_board_send("<p>No such InsightBoard.</p>".encode("utf-8"), 404, head_only)
        snapshot = board_snapshot(board, self.root)
        try:
            body = render_insight_run(snapshot, (query.get("task") or [""])[0], (query.get("call") or [""])[0],
                                      (query.get("page") or [""])[0])
        except (FileNotFoundError, ValueError) as exc:
            return self._insight_board_send(f"<p>No such run on this board: {_e(exc)}</p>".encode("utf-8"), 404, head_only)
        return self._insight_board_send(body.encode("utf-8"), 200, head_only)

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
    ask.add_argument("partitions", help="comma-separated partition names, e.g. full or full,youngmale,youngfemale")
    ask.add_argument("question")
    ask.add_argument("--origin", default="", help="curiosity-driven or need-driven")
    ask.add_argument("--parent", default="", help="what it grew out of, e.g. 'I08-full · I3' or 'QI9'")
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
    partitions = list(dict.fromkeys(p.strip().lower() for p in partitions if p and p.strip()))
    if level not in _LEVEL_OF:
        raise ValueError("kind of answer must be D, I, K or W")
    if not question:
        raise ValueError("the question is empty")
    if not partitions:
        raise ValueError("choose at least one partition")
    if any(not re.fullmatch(r"[a-z]+", p) for p in partitions):
        raise ValueError("partitions are named by their full name, e.g. full, youngmale, cross")
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
                   "status": "planned", "requested_answer_targets": [], "requested_controls": [request],
                   "runs": [], "control": {"gates": [], "routes": []},
                   "resource_controls": [], "frontier": [], "output": {"acceptance": "pending"}}
    record_id = f"registration-{qid.lower()}-{uuid.uuid4().hex[:12]}"
    from src.outline_version import plan_dir, record_path
    log = record_path(plan_dir(path.parent), path.stem, "log")
    receipt = f"{log.relative_to(board_root).as_posix()}#{record_id}"
    control = {"key": "registration", "target": {"question": qid, "partitions": partitions},
               "status": "passed", "authority": "haipipe-insight-question", "actor": actor,
               "evidence": [{"path": path.relative_to(board_root).as_posix()}], "receipt": receipt}
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
    gen_at = header.find("Gen-1")
    cols = [(m.group(0), m.start()) for m in re.finditer(r"(?<!\S)[a-z]+(?!\S)", header)
            if m.start() > gen_at and m.group(0) != "cell"]
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
