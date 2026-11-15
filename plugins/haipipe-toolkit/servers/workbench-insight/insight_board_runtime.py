"""What ran on an insight Board: the workflow runtime inventory, each Task's calls, and the snapshot groomed for
the page."""

from __future__ import annotations

import re
from pathlib import Path

from src.themes import theme_dir, theme_dirs
from .insight_run_specs import (
    definition as read_insight_definition, describe as describe_run_field, people as run_people, reader_name as
    run_reader_name)
from .insight_board_reader import (  # noqa: F401 · this module keeps answering these names
    _read, _e, _field, board_snapshot)
from .insight_board_parts import _TICKET_TARGET, _dataset_line


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
    """The Project's work Theme (`work/`, or the old `tasks/`) nearest above the board."""
    return next((found[0] for parent in snap["board"].parents if (found := theme_dirs(parent, "task"))),
                theme_dir(snap["board"].parent.parent, "task"))


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
    # A page folder is also a task folder: its runs/run_bNNjNNtNNrNN_<segment>_<task>.sh
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
        # in the board's store, or it reads the board's one extract. A
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
    if snapshot and snapshot.get("layout") == "instance":
        # an Insight Block: haipipe-insight-check ref/check_block.py, problems FAIL, notes WARN
        checks = ([{"level": "FAIL", "code": "instance", "where": board_root.name, "message": m}
                   for m in snapshot["instance_problems"]]
                  + [{"level": "WARN", "code": "instance-note", "where": board_root.name, "message": m}
                     for m in snapshot["instance_notes"]])
        return {"checks": checks or [{"level": "PASS", "code": "instance-check-clean", "where": board_root.name,
                                      "message": "check_block.py returned no problem and no note"}],
                "queue": [], "handoffs": [], "bindable_handoffs": []}
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
    queue = [{"level": lvl, "page": path, "state": _field(_read(path), "state") or "OPEN",
              "next": "continue the register frontier"}
             for lvl, paths in snapshot["registers"].items() for path in paths
             if not (_field(_read(path), "state") or "").startswith("✅")]
    bindable = [h for h in snapshot["handoffs"] if h["bindable"]]
    if not bindable:
        checks.append({"level": "WARN", "code": "no-current-design-handoff", "where": board_root.name,
                       "message": "no current signed payload with verified dependency pins and GI6 receipt is available to Design"})
    return {"checks": checks, "queue": queue, "handoffs": snapshot["handoffs"], "bindable_handoffs": bindable}
