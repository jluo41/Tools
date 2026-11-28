"""Read the corpus for Data → Preparation: the raw source folder and the items to label.

``raw_source`` describes the folder named in ``labeling/corpus/source.yaml``: its
files with size, rows and columns, and which raw column became which item field.
It never returns a row value, because raw rows carry other people's labels.

``item_page`` returns the development items to label, a page at a time, with their
context and text. Held-back items never appear. An item waiting in a round keeps
its text for the Rounds screen. Every page that returns text is appended to the
exposure log (``exposure/group_examples.jsonl``), like the Embedding view's
typical items, so a later round can tell a fresh item from one already seen.

``labeling/corpus/source.yaml``::

    schema: subjective-label/corpus-source-v1
    folder: _WorkSpace/InLabStore/runs/dices350-safety/source   # under the repository
    file: diverse_safety_adversarial_dialog_350.csv
    one_row_is: one rater's answers about one conversation
    item_key: item_id                                          # rows sharing it make one item
    fields: {item_id: item_id, context: context_prev, response: text}
    built_by: engine/fence_source.py
    built_on: 2026-09-16
"""
from __future__ import annotations

import re

import csv
import importlib.util
import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location("subjective_label_embedding_for_corpus_view",
                                               HERE / "embedding_build.py")
emb = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(emb)
cal, job = emb.cal, emb.job

SOURCE_FILE = "corpus/source.yaml"
PAGE_MAX = 50
csv.field_size_limit(1 << 26)


class CorpusViewRefused(RuntimeError):
    """A read that would show held-back text or could not be recorded."""


def source_record(job_root: Path) -> dict:
    path = Path(job_root) / SOURCE_FILE
    return job.load_mapping(path) if path.is_file() else {}


def _folder(job_root: Path, record: dict) -> Path | None:
    """The first ancestor of the Page that holds ``folder``; the repository root in practice."""
    rel = str(record.get("folder") or "").strip("/")
    if not rel or ".." in Path(rel).parts:
        return None
    for parent in Path(job_root).resolve().parents:
        candidate = parent / rel
        if candidate.is_dir() and not candidate.is_symlink():
            return candidate
    return None


@lru_cache(maxsize=32)
def _table_shape(path: str, mtime_ns: int, size: int, key: str) -> dict:
    """Rows, columns and distinct keys of one CSV or JSONL file; no values leave this function."""
    suffix = Path(path).suffix.lower()
    columns: list[str] = []
    rows = 0
    keys: set[str] = set()
    with open(path, encoding="utf-8", newline="") as handle:
        if suffix == ".csv":
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            for row in reader:
                rows += 1
                if key and key in row:
                    keys.add(str(row[key]))
        else:
            for line in handle:
                if not line.strip():
                    continue
                rows += 1
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if isinstance(row, dict):
                    for name in row:
                        if name not in columns:
                            columns.append(name)
                    if key and key in row:
                        keys.add(str(row[key]))
    return {"rows": rows, "columns": columns, "keys": len(keys)}


def raw_source(job_root: Path) -> dict:
    """The raw folder and how its rows became items; never a row value."""
    record = source_record(job_root)
    if not record:
        return {}
    folder = _folder(job_root, record)
    out = {"folder": str(record.get("folder") or ""), "found": folder is not None,
           "file": str(record.get("file") or ""), "one_row_is": str(record.get("one_row_is") or ""),
           "item_key": str(record.get("item_key") or ""),
           "fields": {str(k): str(v) for k, v in (record.get("fields") or {}).items()},
           "built_by": str(record.get("built_by") or ""), "built_on": str(record.get("built_on") or ""),
           "files": []}
    if folder is None:
        return out
    for path in sorted(p for p in folder.rglob("*") if p.is_file() and not p.name.startswith(".")):
        stat = path.stat()
        entry = {"path": path.relative_to(folder).as_posix(), "bytes": stat.st_size}
        if path.suffix.lower() in {".csv", ".jsonl"}:
            key = out["item_key"] if path.name == out["file"] else ""
            entry.update(_table_shape(str(path), stat.st_mtime_ns, stat.st_size, key))
        out["files"].append(entry)
    return out


def _order(item_id: str) -> tuple:
    """Numbers in their natural order: `dices-10:t02` before `dices-100:t06`."""
    if item_id.isdigit():
        return (0, int(item_id), ())
    return (1, 0, tuple((0, int(part), "") if part.isdigit() else (1, 0, part)
                        for part in re.split(r"(\d+)", item_id) if part))


def item_page(job_root: Path, *, offset: int = 0, k: int = 20, human_id: str | None = None,
              channel: str = "cli") -> dict:
    """One page of the items to label with their text; held-back items are never read."""
    job_root = Path(job_root).resolve()
    offset, k = int(offset), int(k)
    if offset < 0 or not 1 <= k <= PAGE_MAX:
        raise CorpusViewRefused(f"items come 1 to {PAGE_MAX} at a time, from offset 0 or more")
    if job.status(job_root).get("hold"):
        raise CorpusViewRefused("this job is read-only (HOLD), so showing item text cannot be recorded")
    config = job.load_mapping(job_root / "config.yaml")
    corpus = config.get("corpus") if isinstance(config.get("corpus"), dict) else {}
    text_field = str(corpus.get("text_field") or "text")
    context_field = str(corpus.get("context_field") or "context_prev")
    after_field = str(corpus.get("context_after_field") or "")   # optional: text after the main one
    rows = [row for row in cal._corpus_rows(job_root)
            if row.get("population_status") == "eligible" and row.get("item_id") is not None]
    rows.sort(key=lambda row: _order(str(row["item_id"])))
    waiting = emb.waiting_items(job_root)
    labeled: dict[str, str] = {}
    for round_path in cal._round_dirs(job_root):
        for item_id, state in cal._item_states(round_path).items():
            if state.get("final"):
                labeled[item_id] = f"labeled in {round_path.name}"
    page = []
    for row in rows[offset:offset + k]:
        item_id = str(row["item_id"])
        # the conversation an item belongs to, so a reader sees each conversation once
        conversation = str(row.get("conversation_id") or item_id.split(":", 1)[0])
        if item_id in waiting:
            page.append({"item_id": item_id, "conversation_id": conversation,
                         "state": f"waiting in {waiting[item_id]}"})
            continue
        page.append({"item_id": item_id, "conversation_id": conversation,
                     "state": labeled.get(item_id, "to label"),
                     "context": str(row.get(context_field) or ""), "text": str(row.get(text_field) or ""),
                     "after": str(row.get(after_field) or "") if after_field else ""})
    shown = [entry["item_id"] for entry in page if "text" in entry]
    if shown:
        emb._record_exposure(job_root, human_id=human_id, channel=channel,
                             where="preparation item table", version="items", item_ids=shown)
    return {"offset": offset, "k": k, "total": len(rows), "items": page,
            "more": offset + k < len(rows)}
