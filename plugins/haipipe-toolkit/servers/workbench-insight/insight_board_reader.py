"""What an insight Board holds on disk, read into one snapshot: its register pages (their cell grids), answering
pages, receipts, partitions, workflow runtimes and signed handoffs. Reads only; insightboard.py draws the snapshot."""

from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import unquote

from src.folder_contract import resolved_folder_kind
from .insight_handoff import eligibility as handoff_eligibility, watch_paths as handoff_watch_paths


_TITLE = re.compile(r"(?m)^#\s+(.+?)\s*$")
_INSIGHT_BOARD = re.compile(r"(?:^|[-_])insightboard(?:$|[-_])", re.I)
_LEVELS = ("data", "information", "knowledge", "wisdom")
_LEVEL_OF = {"D": "data", "I": "information", "K": "knowledge", "W": "wisdom"}
_LEVEL_LABEL = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}
_SKIP = {"board", "_archive", "__pycache__", ".git", "probe", "display", "_results", "reports", "results", "runs"}
# A page id is its level, its number and its partition's name: `I02-full`, `K02-cross`
# (no segment letters).  A folder is `<id>-<slug>`, so an id is never
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
    text = _read(board_root / "board.md")
    declared = _field(text, "board-kind").lower()
    if declared == "task-block":                 # an Insight Block (hai-insight ref/block-contract.md)
        return _field(text, "workbench").lower() == "insight"
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
# insights/ is the board world; insights/_old/ holds boards made before
# reports; applications/ is legacy and still read.
_BOARD_GLOBS = ("examples*/*/tasks/*/board.md", "examples*/*/insights/*/board.md", "examples*/*/insights/_old/*/board.md",
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
        # A short or segment name still lands (a terminal wraps a long
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
            "register_level": head.get("question-level", "").lower(),
            "level": _LEVEL_OF.get(m.group(1)) if m else "", "partition": part,
            "receipt_field": head.get("receipt", ""),
        })
    return pages


def _page_link(snapshot: dict, page: dict) -> str:
    """The Page in the shared live reader (`/_board/page`); the Board's static site is retired
. A static snapshot links the source Markdown."""
    if snapshot["static"]:
        return f"../{page['rel']}"
    from live.page_reader import page_url
    return page_url(page["path"], snapshot["root"])


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
    """MT04 style: one row per segment, one column per question id."""
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
        for day, line in _LOG_LINE.findall(_section(page["text"], "Log")):
            events.append({"date": day, "page": page, "text": line})
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
                # where read without them names the wrong population
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
                 (p["page_type"] == "question" or (not p["page_type"] and p["register_level"]))]
    questions = []
    for reg in sorted(registers, key=lambda p: p["id"]):
        questions.extend(_parse_register(reg, partition_ids))
    store_field = _field(text, "store")
    # `store: _results` is the board's own folder; a `_WorkSpace/...`
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
        "registers": {lvl: [p["path"] for p in registers if p["register_level"] == lvl] for lvl in _LEVELS},
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
            if data.get("workflow_id") != "hai-insight-workflow":
                raise ValueError("workflow owner is not hai-insight-workflow")
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
