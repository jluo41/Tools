"""Page Evidence in the Run Space: each Run's Evidence type, its Evidence Item
bindings and refs, and the count pills (moved verbatim from runs.py).
"""
from __future__ import annotations

import html
import re
from pathlib import Path

from live.runs_ids import _EVIDENCE_TYPE_ORDER, _EVIDENCE_TYPES
from src.item_table import (compact_global_run, compact_paper_run, read_items,
                            readable_global_run, readable_paper_route)


def _evidence_type(row: dict) -> str:
    """Return the reader-facing Page Evidence subspace for one Run."""
    candidates = [row.get("target", ""), *row.get("refs", [])]
    for value in candidates:
        match = re.search(
            r"E\d+-(VALUE|TABLE|DISPLAY|CITE)(?:-|$)",
            str(value or ""),
            re.I,
        )
        if match:
            return _EVIDENCE_TYPES[match.group(1).upper()]
    return ""


def _evidence_item_label(row: dict) -> str:
    """Turn an Evidence Item id into a short card label."""
    candidates = [row.get("target", ""), *row.get("refs", [])]
    for value in candidates:
        match = re.search(r"(E\d+)-(?:VALUE|TABLE|DISPLAY|CITE)(?:-|$)",
                          str(value or ""), re.I)
        if match:
            return match.group(1).upper()
    return "Evidence"


def _evidence_records(page_src: Path) -> dict[str, dict]:
    """Load the same Result-backed Evidence records used by Evidence Space."""
    try:
        from live.evidence import _result_records
        records = _result_records(page_src.parent)
    except (ImportError, OSError, ValueError, TypeError, AttributeError):
        return {}
    return {str(record.get("id", "")).strip(): record for record in records
            if str(record.get("id", "")).strip()}


def _attach_evidence_bindings(page_src: Path, rows: list[dict]) -> None:
    """Attach readable Evidence Item records to every bound Run."""
    records = _evidence_records(page_src)
    if not records:
        return
    for row in rows:
        bindings = [records[ref] for ref in row.get("refs", []) if ref in records]
        if not bindings:
            continue
        labels = []
        for binding in bindings:
            fields = binding.get("fields", {})
            for label in fields.get("labels", []):
                if isinstance(label, dict) and label not in labels:
                    labels.append(label)
        if labels:
            row["evidence_labels"] = labels
        row["evidence_bindings"] = bindings
        primary = bindings[0]
        item_id = str(primary.get("id", "")).strip()
        match = re.match(r"(E\d+)-", item_id, re.I)
        row["evidence_item_id"] = match.group(1).upper() if match else item_id
        row["evidence_title"] = str(primary.get("title", "")).strip()


def _run_pills(items: list[tuple[str, int]]) -> str:
    """Render the compact, non-interactive count pills used by each space."""
    return "".join(
        '<span class="run-pill%s">%d %s</span>' % (
            " total" if index == 0 else "", count, html.escape(label)
        )
        for index, (label, count) in enumerate(items)
    )


def _fallback_evidence_counts(rows: list[dict]) -> tuple[int, dict[str, int]]:
    """Count unique Evidence Item ids when no Result snapshot is available."""
    items: dict[str, str] = {}
    for row in rows:
        for value in [row.get("target", ""), *row.get("refs", [])]:
            for match in re.finditer(
                    r"\b(E\d+)-(VALUE|TABLE|DISPLAY|CITE)(?:-[a-z0-9-]+)?\b",
                    str(value or ""), re.I):
                items.setdefault(match.group(1).upper(),
                                 _EVIDENCE_TYPES[match.group(2).upper()])
    counts = {label: 0 for label in _EVIDENCE_TYPE_ORDER}
    for kind in items.values():
        if kind in counts:
            counts[kind] += 1
    return len(items), counts


def _evidence_summary_counts(page_src: Path, rows: list[dict]) -> tuple[int, dict[str, int]]:
    """Use the same current Result records as Evidence Space for its pills."""
    try:
        from live.evidence import _evidence_type as result_evidence_type
        from live.evidence import _result_records
        records = _result_records(page_src.parent)
    except (ImportError, OSError, ValueError, TypeError, AttributeError):
        records = []
        result_evidence_type = None
    if records and result_evidence_type is not None:
        counts = {label: 0 for label in _EVIDENCE_TYPE_ORDER}
        for record in records:
            kind = result_evidence_type(record)
            if kind == "DISPLAY":
                counts["Display"] += 1
            elif kind == "CITE":
                counts["Citation"] += 1
            elif kind == "VALUE":
                counts["Value"] += 1
        return len(records), counts
    return _fallback_evidence_counts(rows)


def _evidence_refs(page_src: Path, *, run_id: str, ticket: Path, ledger: dict | None = None) -> list[str]:
    """Return Evidence Items only when their ledger has named this local run.

    A caller that loops over a Page's runs passes `ledger` (the Page's `read_items`,
    read once): reading it per run cost 564 reads and 33 s on the MISQ paper's
    Sections Space (JL 260930)."""
    compact = compact_paper_run(run_id) or compact_global_run(run_id)
    needles = {run_id, ticket.name, str(ticket.relative_to(page_src.parent))}
    if compact:
        needles.update({compact, readable_paper_route(compact), readable_global_run(compact)})
    refs = []
    for item in (read_items(page_src) if ledger is None else ledger).values():
        declared = " ".join((item.get("local_run", ""), item.get("result", "")))
        if any(needle and needle in declared for needle in needles):
            refs.append(item["item"])
    return refs
