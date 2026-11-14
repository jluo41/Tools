"""Runs that a theme keeps in its own folders (Labeling and Insight), shown in
the Task Run lane like any other Run (moved verbatim from runs.py).
"""
from __future__ import annotations

from pathlib import Path

from src.item_table import read_items

# runs.py imports this module after it defines these helpers, so load it through live.runs.


def _labeling_runs(page_src: Path) -> list[dict]:
    """Project the page-local Labeling dialect into the Task Run lane.

    Labeling keeps its Ticket and Result beneath ``labeling/``.  The generic
    presenter reads only the safe envelope; domain artifacts remain owned by
    the Labeling workbench and never become previews here.
    """
    job = page_src.parent / "labeling"
    runs_dir = job / "runs"
    results_dir = job / "results"
    if not runs_dir.is_dir() and not results_dir.is_dir():
        return []
    rows = []
    paired = set()
    for ticket in _ticket_files(runs_dir):
        runtime = _run_folder_receipt(ticket) or _runtime_for(ticket, runs_dir, results_dir)
        if runtime:
            paired.add(runtime)
        fields = _fields(runtime)
        ticket_fields = _fields(ticket)
        for key in ("run", "status", "target", "result", "family", "operation",
                    "outcome", "summary"):
            fields[key] = fields.get(key) or ticket_fields.get(key, "")
        audit = []
        if runtime is None:
            audit.append("authored Run record has no runtime receipt")
        declared = fields.get("run")
        if declared and declared != ticket.stem:
            audit.append("runtime Run identity does not match the authored Run record")
        rows.append({
            "run_id": ticket.stem,
            "global_id": ticket.stem,
            "compact_id": ticket.stem,
            "ticket": ticket,
            "runtime": runtime,
            "result_path": runtime.parent if runtime else None,
            "result": fields.get("result", "") or _fallback_result(runtime, job),
            "target": fields.get("target", "") or "labeling operation",
            "outcome": fields.get("outcome", "") or fields.get("summary", ""),
            "kind": fields.get("operation", "") or "Labeling",
            "origin": "Local",
            "lane": "task",
            "family": "Labeling",
            "operation": fields.get("operation", ""),
            "version": "", "step": "", "goal": "", "refs": [],
            "status": "Held" if audit else _status(runtime, fields),
            "audit": audit,
        })
    for runtime in sorted(results_dir.glob("*/runtime.yaml")) if results_dir.is_dir() else []:
        if runtime in paired or not _confined_file(runtime, results_dir):
            continue
        fields = _fields(runtime)
        rows.append({
            "run_id": runtime.parent.name, "global_id": runtime.parent.name,
            "compact_id": runtime.parent.name, "ticket": None, "runtime": runtime,
            "result_path": runtime.parent,
            "result": fields.get("result", "") or _fallback_result(runtime, job),
            "target": fields.get("target", "") or "orphan Labeling Result",
            "outcome": fields.get("outcome", "") or fields.get("summary", ""),
            "kind": fields.get("operation", "") or "Labeling",
            "origin": "Local", "lane": "task", "family": "Labeling",
            "operation": fields.get("operation", ""), "version": "", "step": "",
            "goal": "", "refs": [], "status": "Held", "orphan": True,
            "audit": ["Result exists without its authored Run record"],
        })
    return rows


def _insight_runs(page_src: Path) -> list[dict]:
    """The instance dialect has one ticket and several explicit executions."""
    from src.insight_instances import contract
    api = contract()
    try:
        manifest, items, errors = api.inspect(page_src.parent)
    except (OSError, ValueError, TypeError, KeyError, AttributeError, api.yaml.YAMLError):
        return []  # the Outline item table displays the validation failure
    rows = []
    ledger = read_items(page_src)
    for item in items:
        if not item["ticket"]:
            continue  # proposed items are not allocated Runs
        run = item["item"]["run"]
        base_run = item["item"].get("base_run", {}).get("id", "")
        datasets = ", ".join(item["item"].get("datasets", []))
        target_level = item["item"].get("target", "")
        ticket = api.item_ticket(page_src.parent, item["item"])
        for info in item["versions"] or [None]:
            ident = info["execution"] if info else f"{manifest['instance']}#{run}"
            directory = page_src.parent / "results" / run / info["version"] if info else None
            status = "Ready"
            if info:
                status = {"planned": "Ready", "running": "Running", "complete": "Done",
                          "failed": "Failed", "blocked": "Held"}.get(info["status"], "Held")
                if not info["valid"] or info["stale"]:
                    status = "Held"
            result_file = directory / "result.yaml" if directory else None
            has_result = bool(result_file and result_file.is_file())
            binding_state = ((info.get("status", "").capitalize() + " binding · ")
                             if info else "Binding · ")
            rows.append({"run_id": ident, "global_id": ident, "compact_id": ident if info else "",
                         "ticket": ticket, "runtime": directory / "runtime.yaml" if directory else None,
                         "result_path": result_file if has_result else None,
                         "result": str(result_file) if has_result else "",
                         "target": item["item"].get("question", ""), "status": status,
                         "outcome": (f"{binding_state}binds {base_run} to {datasets}" if base_run else ""),
                         "origin": "Local", "lane": "task", "family": "Insight",
                         "kind": (f"Insight · RI · {target_level.title()}"
                                  if base_run else "Insight"),
                         "operation": "item", "version": info["version"] if info else "",
                         "step": "", "goal": "", "base_run": base_run,
                         "refs": _evidence_refs(page_src, run_id=ident, ticket=ticket, ledger=ledger)})
    return sorted(rows, key=_sort_key)


# looked up when called, never at import: the old module re-exports this file's names, so either can be imported first
def _confined_file(*args, **kwargs):
    from live.runs import _confined_file as real
    return real(*args, **kwargs)


def _evidence_refs(*args, **kwargs):
    from live.runs import _evidence_refs as real
    return real(*args, **kwargs)


def _fallback_result(*args, **kwargs):
    from live.runs import _fallback_result as real
    return real(*args, **kwargs)


def _fields(*args, **kwargs):
    from live.runs import _fields as real
    return real(*args, **kwargs)


def _run_folder_receipt(*args, **kwargs):
    from live.runs import _run_folder_receipt as real
    return real(*args, **kwargs)


def _runtime_for(*args, **kwargs):
    from live.runs import _runtime_for as real
    return real(*args, **kwargs)


def _sort_key(*args, **kwargs):
    from live.runs import _sort_key as real
    return real(*args, **kwargs)


def _status(*args, **kwargs):
    from live.runs import _status as real
    return real(*args, **kwargs)


def _ticket_files(*args, **kwargs):
    from live.runs import _ticket_files as real
    return real(*args, **kwargs)
