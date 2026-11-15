"""A worker Run's life after it is queued: name the worker, put it back if it died, close it through the records
check, find a stale queued run and supersede it, list the planned runs (split out of design_actions.py)."""
from __future__ import annotations

from pathlib import Path

from host_paths import skill_dir
from live.design_actions_files import ActionError, _dump, _load, _now


def complete_run(folder: Path, run: str, started_at: str = "") -> dict:
    """The caller closes a worker Run: gate the Result, then write the receipt.

    The worker wrote only ``results/<run>/`` (content, checks, result.yaml).
    This step runs ``check_unit`` on the pair and records the truthful status:
    ``complete`` with the next route when the gate accepts a complete judgment
    (pass, fail, or unresolved), ``failed`` with the gate's own words when the
    record is malformed. It never edits the Result.
    """
    import importlib.util
    checker = skill_dir("haipipe-design-unit") / "scripts" / "check_unit.py"
    spec = importlib.util.spec_from_file_location("design_unit_gate", checker)
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    ticket_path = folder / "runs" / f"{run}.yaml"
    result_path = folder / "results" / run / "result.yaml"
    runtime_path = folder / "results" / run / "runtime.yaml"
    if not ticket_path.is_file() or not runtime_path.is_file():
        raise ActionError(f"{run}: no planned Ticket/receipt to close")
    runtime = _load(runtime_path)
    if runtime.get("status") not in ("planned", "running"):
        raise ActionError(f"{run}: receipt is already {runtime.get('status')}")
    if not result_path.is_file():
        raise ActionError(f"{run}: the worker left no result.yaml; nothing to close")
    ticket = _load(ticket_path)
    problems = gate.validate(ticket_path, result_path)
    result = _load(result_path)
    verdict = str(result.get("verdict") or "")
    now = _now()
    runtime.update(started_at=started_at or runtime.get("queued_at") or now, finished_at=now)
    if problems:
        # A draft that fails the check is drafted again; a review that fails it is reviewed again.
        runtime.update(status="failed", failure="; ".join(problems),
                       route="verify" if ticket.get("operation") == "verify" else "generate")
    elif ticket.get("operation") == "verify" and verdict == "fail":
        runtime.update(status="complete", failure=None, route="generate", terminal_outcome="fail")
    elif ticket.get("operation") == "verify" and verdict == "unresolved":
        runtime.update(status="complete", failure=None, route="resolve-unresolved",
                       terminal_outcome="unresolved")
    else:
        runtime.update(status="complete", failure=None,
                       route="verify" if ticket.get("operation") == "generate" else "delivery",
                       terminal_outcome=verdict or "complete")
    _dump(runtime_path, runtime)
    return {"run": run, "status": runtime["status"], "verdict": verdict,
            "route": runtime.get("route"), "problems": problems}


# ------------------------------------------------------------ stale queue --

def stale_inputs(folder: Path, run: str) -> list[str]:
    """The files a queued run names that changed (or vanished) since it was queued.

    Staleness is file time: an input or target modified after the run's Ticket
    was written. Never a content hash. The config and approval are
    frozen copies written with the Ticket, so only their absence counts; the
    same rule as the records check (``check_unit.context``)."""
    ticket_path = folder / "runs" / f"{run}.yaml"
    ticket = _load(ticket_path)
    queued = ticket_path.stat().st_mtime if ticket_path.is_file() else 0.0
    frozen = [ticket.get("config"), (ticket.get("approval") or {}).get("record")]
    named = list(ticket.get("inputs") or []) + list(ticket.get("targets") or [])
    changed = []
    for ref, timed in [(r, False) for r in frozen] + [(r, True) for r in named]:
        if isinstance(ref, dict) and ref.get("path"):
            path = (folder / str(ref["path"])).resolve()
            if not path.is_file() or (timed and path.stat().st_mtime > queued):
                changed.append(Path(str(ref["path"])).name)
    return changed


def supersede(folder: Path, run: str, reason: str) -> dict:
    """Retire a queued run no worker has taken, with its reason; its record stays."""
    runtime_path = folder / "results" / run / "runtime.yaml"
    runtime = _load(runtime_path)
    if runtime.get("status") != "planned":
        raise ActionError(f"{run}: receipt is {runtime.get('status')}; only a queued run can be replaced")
    runtime.update(status="superseded", failure=reason, finished_at=_now())
    _dump(runtime_path, runtime)
    return {"run": run, "status": "superseded"}


# ------------------------------------------------------------ batch + queue --

def name_worker(folder: Path, run: str, actor: str) -> dict:
    """Name the real worker on a planned run record before dispatch, and mark the receipt running."""
    ticket_path = folder / "runs" / f"{run}.yaml"
    runtime_path = folder / "results" / run / "runtime.yaml"
    if not ticket_path.is_file() or not runtime_path.is_file():
        raise ActionError(f"{run}: no planned run record to name")
    runtime = _load(runtime_path)
    if runtime.get("status") != "planned":
        raise ActionError(f"{run}: receipt is {runtime.get('status')}, not planned")
    ticket = _load(ticket_path)
    ticket["actor"] = actor
    _dump(ticket_path, ticket)
    runtime.setdefault("worker", {})["actor"] = actor
    runtime.pop("ticket_sha256", None)  # a leftover hash field is dropped, never refreshed
    runtime["status"] = "running"
    runtime["started_at"] = _now()
    _dump(runtime_path, runtime)
    return {"run": run, "actor": actor, "ticket": ticket_path.as_posix()}


def release_worker(folder: Path, run: str) -> dict:
    """A dispatched worker died and left no result: put the run record back in the queue, truthfully."""
    ticket_path = folder / "runs" / f"{run}.yaml"
    runtime_path = folder / "results" / run / "runtime.yaml"
    if not ticket_path.is_file() or not runtime_path.is_file():
        raise ActionError(f"{run}: no run record to put back")
    runtime = _load(runtime_path)
    if runtime.get("status") != "running":
        raise ActionError(f"{run}: receipt is {runtime.get('status')}, not running")
    if (folder / "results" / run / "result.yaml").is_file():
        raise ActionError(f"{run}: a result exists; close it with the records check instead")
    ticket = _load(ticket_path)
    lost = str(ticket.get("actor") or "")
    pending = ("designer" if ticket.get("operation") == "generate" else "reviewer") + "-context-pending"
    ticket["actor"] = pending
    _dump(ticket_path, ticket)
    runtime.setdefault("worker", {})["actor"] = pending
    runtime.pop("ticket_sha256", None)  # a leftover hash field is dropped, never refreshed
    runtime["status"] = "planned"
    runtime.pop("started_at", None)
    runtime.setdefault("lost_workers", []).append({"actor": lost, "at": _now(), "why": "left no result"})
    _dump(runtime_path, runtime)
    return {"run": run, "lost": lost}


def planned_runs(folder: Path) -> list[dict]:
    """Every planned agent run in a folder: what the queue runner picks up."""
    out = []
    results = folder / "results"
    found = [p for pat in ("rd*/runtime.yaml", "run-design-*/runtime.yaml") for p in results.glob(pat)] if results.is_dir() else []
    for runtime_path in sorted(found):
        runtime = _load(runtime_path)
        if runtime.get("status") == "planned" and runtime.get("operation") in ("generate", "verify"):
            out.append({"run": runtime.get("run") or runtime_path.parent.name,
                        "operation": runtime.get("operation"), "item": runtime.get("item"),
                        "ticket": (folder / str(runtime.get("ticket") or "")).as_posix(),
                        "folder": folder.as_posix()})
    return out
