"""The Page's own Runs (local_runs): tickets and receipts beside the Page, in its
Task store, and the fixed Delivery Run (moved verbatim from runs.py).
"""
from __future__ import annotations

import re
from pathlib import Path

from src import run_names as _names
from src.common import delivery_read_lane_dir, delivery_relative
from live.runs_ids import (_STATE_ORDER, _TICKET_NAME, _WRITING_KINDS, _audit_page_run_order, _is_page_run,
                          _new_kind, _valid_page_run_id)
from src.item_table import (compact_global_run, compact_paper_run, read_items,
                            readable_global_run, readable_paper_route)


try:
    # Board contributes the job-backed Task adapter through its ``src``
    # namespace. A standalone Page has no Board package and therefore keeps
    # the Folder-local Runs dialect only.
    from src.dialect_task_block import page_info as task_page_info
except ImportError:
    def task_page_info(_block, _page_src):
        return None


def _task_context(page_src: Path):
    """Return the Task adapter record and containing Job for a Task Page."""
    if len(page_src.parents) < 3:
        return None, None
    block = page_src.parents[2]
    info = task_page_info(block, page_src)
    return (info, page_src.parents[1]) if info else (None, None)


def _sort_key(row: dict) -> tuple:
    """Order active/recovery work first, then newer Run numbers."""
    numbers = re.findall(
        r"(?:r(?:p|l|i|d)?|rp-(?:struct|sec|para)-|re-(?:value|display|cite)-|rd)(\d+)",
        row.get("run_id", ""),
        re.I,
    )
    newest = -int(numbers[-1]) if numbers else 0
    return _STATE_ORDER.get(row["status"], 9), newest, row["run_id"]


def _task_result_locations(page_dir: Path, job_dir: Path,
                           findings: list[str] | None = None) -> list[tuple[Path, Path]]:
    """Declared Task store first, then current local and historical storage."""
    locations = []
    store = _fields(job_dir / "src" / "config-defaults.yaml").get("store", "")
    if store and store not in {"null", "~"}:
        store_path = Path(store).expanduser()
        if not store_path.is_absolute():
            ancestors = [job_dir, *job_dir.parents]
            checkout = next((a for a in ancestors if (a / "pyproject.toml").is_file()
                             and (a / "code").is_dir()), None)
            checkout = checkout or next((a for a in ancestors if (a / ".git").exists()), None)
            if checkout is None:
                if findings is not None:
                    findings.append("relative declared Task store has no resolvable checkout root")
                store_path = None
            else:
                store_path = checkout / store_path
        if store_path is not None:
            output_root = store_path / job_dir.parent.name / job_dir.name
            locations.extend(((output_root / page_dir.name / "results", output_root),
                              (output_root / "results" / page_dir.name, output_root)))
    locations.extend(((page_dir / "results", job_dir),
                      (job_dir / "results" / page_dir.name, job_dir)))
    return list(dict.fromkeys(locations))


def _fixed_delivery_run(page_src: Path, ticket: Path) -> dict | None:
    """`runs/run-delivery-<lane>.sh`: the lane's one Delivery Run (JL 260928). It keeps no
    runtime receipt; its result is the lane folder, and it is Done while the lane is current."""
    from live.delivery import LANE_OF_RUN
    lane = LANE_OF_RUN.get(ticket.stem)
    if lane is None:
        return None
    folder = delivery_read_lane_dir(page_src.parent, lane)
    return {"run_id": ticket.stem, "global_id": ticket.stem, "compact_id": "", "ticket": ticket,
            "runtime": None, "result_path": folder, "result": delivery_relative(page_src.parent) + "/%s/" % lane,
            "target": delivery_relative(page_src.parent) + "/%s" % lane, "outcome": "", "kind": "Delivery", "origin": "Local",
            "lane": "page", "family": "page", "operation": "delivery", "version": "", "step": "",
            "mode": "", "target_scope": "", "participants": "", "coordinator": "", "contributors": "",
            "goal": "", "audit": [], "refs": []}


def local_runs(page_src: Path) -> list[dict]:
    """Read allocated Folder-local or Job-backed Task Run pairs."""
    # here, not at the top: runs_themes reads _sort_key back through live.runs
    from live.runs_themes import _insight_runs, _labeling_runs
    page_dir = page_src.parent
    instance_rows = (_insight_runs(page_src) if (page_dir / "workflow/insight.yaml").is_file() else [])
    item_tickets = {row["ticket"] for row in instance_rows}
    task_info, job_dir = _task_context(page_src)
    runs_dir = page_dir / "runs"
    location_findings = []
    locations = (_task_result_locations(page_dir, job_dir, location_findings) if task_info else
                 [(page_dir / "results", page_dir)])
    results_dir, result_base = locations[0]
    rows = list(instance_rows)
    paired_runtimes = {row["runtime"] for row in rows if row.get("runtime")}
    delivery_lanes = None
    ledger = read_items(page_src)
    for ticket in _ticket_files(runs_dir):
        if ticket in item_tickets:
            continue
        fixed = _fixed_delivery_run(page_src, ticket)
        if fixed is not None:
            if delivery_lanes is None:
                from live.delivery import check_delivery
                delivery_lanes = {lane["lane"]: lane["state"] for lane in check_delivery(page_src)["lanes"]}
            fixed["status"] = "Done" if delivery_lanes.get(fixed["target"].split("/")[-1]) == "pass" else "Ready"
            rows.append(fixed)
            continue
        own = _run_folder_receipt(ticket)
        matches = ([(own, page_dir)] if own is not None else
                   [(path, base_path) for result_root, base_path in locations
                    if (path := _runtime_for(ticket, runs_dir, result_root)) is not None])
        runtime, result_base = matches[0] if matches else (None, locations[0][1])
        paired_runtimes.update(path for path, _ in matches)
        fields = _fields(runtime)
        ticket_fields = _fields(ticket) if ticket.suffix.lower() in {".md", ".yaml", ".yml"} else {}
        for key in ("target", "family", "operation", "interaction", "mode", "version", "step",
                    "participants", "coordinator", "contributors"):
            fields[key] = fields.get(key) or ticket_fields.get(key, "")
        if not fields.get("operation") and re.fullmatch(r"r\d+_page-writing_c\d+-p\d+", ticket.stem):
            fields["operation"] = "paragraph-writing"
        if not fields.get("operation") and _valid_page_run_id(ticket.stem) and (
                _new_kind(ticket.stem) in (None, *_WRITING_KINDS)):
            fields.update({"family": fields.get("family") or "page",
                           "operation": "interactive-writing",
                           "interaction": fields.get("interaction") or "human-feedback"})
        is_page_run = _is_page_run(fields)
        audit = list(location_findings)
        # A readable-name run is open from its ticket until it closes (JL 260928:
        # records at the start and at close only), so no runtime yet is normal.
        open_run = (runtime is None and _names.is_run_name(ticket.stem)
                    and ticket_fields.get("status", "open").lower() in {"open", "running", ""})
        if runtime is None:
            fields["status"] = ticket_fields.get("status", "") or ("open" if open_run else "")
            if not open_run:
                audit.append("authored Run record has no runtime receipt")
        if len(matches) > 1:
            audit.append("multiple Result receipts resolve to the same Run; owner reconciliation required")
        retired_design = bool(re.fullmatch(
            r"r[0-9]{2,}_design_(?:commission|generate|verify|adopt)_[a-z0-9][a-z0-9_-]*",
            ticket.stem,
        ))
        if retired_design:
            audit.append("retired Design Run identity is unsupported")
        if is_page_run and fields.get("run") and fields["run"] != ticket.stem:
            audit.append("runtime Run identity does not match the authored Run record")
        kind = ("Interactive writing" if fields.get("operation") == "interactive-writing"
                else "Paragraph writing" if fields.get("operation") == "paragraph-writing"
                else fields.get("operation") or fields.get("family") or "Task")
        if task_info:
            compact = (compact_global_run(fields.get("global_id", ""))
                       or compact_global_run(ticket.stem))
            local_run = re.match(r"^(r\d{2})(?:_|$)", ticket.stem, re.I)
            if not compact and local_run:
                compact = f"{task_info['id']}{local_run.group(1).lower()}"
            global_id = readable_global_run(compact) if compact else ticket.stem
            run_id = global_id
        elif (fields.get("family") == "design" or
              re.fullmatch(r"rd[0-9]{2,}_(?:commission|generate|verify|adopt)_[a-z0-9][a-z0-9_-]*"
                           r"|run-design-(?:commission|generate|verify|adopt)-[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*",
                           ticket.stem)):
            # Design uses its stable Folder address, never a fabricated Paper
            # or b/j/t identity. Its YAML Ticket is already a supported suffix.
            compact = ""
            global_id = fields.get("global_id") or f"{page_dir.as_posix()}#{ticket.stem}"
            run_id = ticket.stem
            if fields.get("family") == "design" and not re.fullmatch(
                    r"rd[0-9]{2,}_(?:commission|generate|verify|adopt)_[a-z0-9][a-z0-9_-]*"
                    r"|run-design-(?:commission|generate|verify|adopt)-[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*",
                    ticket.stem):
                audit.append("invalid current Design Run identity")
        elif retired_design:
            compact = ""
            global_id = ticket.stem
            run_id = ticket.stem
        else:
            paper_id = (compact_paper_run(fields.get("global_id", ""))
                        or compact_paper_run(ticket.stem))
            compact = (paper_id or compact_global_run(fields.get("global_id", ""))
                       or compact_global_run(ticket.stem))
            # The Paper Board is the local block. This view omits an inherited
            # ``bNN`` prefix, while ledger and receipt retain it for global lookup.
            global_id = (paper_id or readable_global_run(compact)) if compact else ticket.stem
            relative_id = readable_paper_route(compact) if compact else ""
            if ((page_dir / "page.toml").is_file()
                    or (page_dir / "workflow/insight.yaml").is_file()) and not compact:
                run_id = ticket.stem
            else:
                run_id = "P " + (relative_id or ticket.stem)
        if is_page_run:
            run_id = ticket.stem
        rows.append({
            "run_id": run_id,
            "global_id": global_id,
            "compact_id": compact,
            "ticket": ticket,
            "runtime": runtime,
            "result_path": runtime.parent if runtime else None,
            "result": fields.get("result", "") or _fallback_result(runtime, result_base),
            "target": fields.get("target", "") or "page-local work",
            "outcome": _result_outcome(runtime, fields),
            "kind": kind,
            "origin": "Task Job" if task_info else "Local",
            "lane": "page" if is_page_run else "task",
            "family": fields.get("family", "") or "Task",
            "operation": fields.get("operation", ""),
            "version": fields.get("version", ""),
            "step": fields.get("step", ""),
            "mode": fields.get("mode", ""),
            "target_scope": fields.get("target_scope", ""),
            "participants": fields.get("participants", ""),
            "coordinator": fields.get("coordinator", ""),
            "contributors": fields.get("contributors", ""),
            "goal": _ticket_note(ticket, "Goal"),
            "status": "Held" if audit else _status(runtime, fields),
            "audit": audit,
            "refs": _evidence_refs(
                page_src,
                run_id=global_id,
                ticket=ticket,
                ledger=ledger,
            ),
        })
    orphan_candidates = {}
    ticket_stems = {p.stem for p in _ticket_files(runs_dir)}
    for result_root, base_path in locations:
        if not result_root.is_dir():
            continue
        for receipt in sorted(result_root.rglob("runtime.yaml")):
            if ("attempts" not in receipt.relative_to(result_root).parts
                    and receipt not in paired_runtimes and _confined_file(receipt, result_root)):
                orphan_candidates[receipt.parent] = (receipt, base_path)
        for directory in sorted(result_root.iterdir()):
            if (directory.is_dir() and not directory.is_symlink()
                    and _TICKET_NAME.match(directory.name)
                    and directory.name not in ticket_stems
                    and not (directory / "runtime.yaml").exists()
                    and not any(directory.rglob("runtime.yaml"))):
                orphan_candidates[directory] = (None, base_path)
    orphan_groups = {}
    for result_path, (runtime, result_base) in orphan_candidates.items():
        identity = result_path.name if task_info else result_path
        orphan_groups.setdefault(identity, []).append((result_path, runtime, result_base))
    for candidates in orphan_groups.values():
        result_path, runtime, result_base = candidates[0]
        orphan_audit = ["Result exists without its authored Run record" if runtime else
                        "Result directory has neither an authored Run record nor a runtime receipt"]
        if len(candidates) > 1:
            orphan_audit.append("multiple Result locations resolve to the same Run: " +
                                ", ".join(str(path) for path, _, _ in candidates))
        fields = _fields(runtime)
        is_page_run = _is_page_run(fields)
        stem = result_path.name
        rows.append({
            "run_id": stem if is_page_run else f"P {stem}",
            "global_id": fields.get("global_id") or stem,
            "compact_id": compact_global_run(fields.get("global_id", "")),
            "ticket": None,
            "runtime": runtime,
            "result_path": result_path,
            "result": fields.get("result", "") or str(result_path),
            "target": fields.get("target", "") or "orphan Result",
            "outcome": _result_outcome(runtime, fields),
            "kind": ("Interactive writing" if fields.get("operation") == "interactive-writing"
                     else fields.get("operation") or fields.get("family") or "Task"),
            "lane": "page" if is_page_run else "task",
            "origin": "Task Job" if task_info else "Local",
            "family": fields.get("family", "") or "Task",
            "operation": fields.get("operation", ""),
            "version": fields.get("version", ""),
            "step": fields.get("step", ""),
            "mode": fields.get("mode", ""),
            "target_scope": fields.get("target_scope", ""),
            "participants": fields.get("participants", ""),
            "coordinator": fields.get("coordinator", ""),
            "contributors": fields.get("contributors", ""),
            "goal": "",
            "status": "Held",
            "refs": [],
            "orphan": True,
            "audit": orphan_audit,
        })
    base_children = {}
    for relation in instance_rows:
        base = relation.get("base_run", "")
        if base:
            base_children.setdefault(base, []).append(relation["run_id"])
    for row in rows:
        children = base_children.get(row.get("global_id", ""), [])
        if children:
            row["kind"] = "Base Task Run"
            row["outcome"] = "Reusable method for " + ", ".join(children)
    _audit_page_run_order(rows)
    rows.extend(_labeling_runs(page_src))
    return sorted(rows, key=_sort_key)


# at the end, not the top: these parts import one another, so each can be imported first
from live.runs_evidence import _evidence_refs
from live.runs_receipts import (_confined_file, _fallback_result, _fields, _run_folder_receipt, _runtime_for,
                               _status, _ticket_files)
from live.runs_result_view import _result_outcome, _ticket_note
