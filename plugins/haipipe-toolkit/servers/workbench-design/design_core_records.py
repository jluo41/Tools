"""A Design Folder's records: the item register, the Run records, and the state each item
folds to (its waiting line, its verified design, its hold).

Split out of design.py; design.py re-exports every name here."""
from __future__ import annotations

from pathlib import Path

from live.design_core_base import (
    _FIELD, _ITEM_FIELDS, _ITEM_HEAD, _ITEM_LISTS, _RUN_FILE, _RUN_FILE_NEW, _STEP, _read, _unit_gate, _yaml,
)


# ---------------------------------------------------------------- register --

def plan_folder(folder: Path) -> Path:
    """A Design Page's plan folder: ``draft/`` since Page layout 0.118, else the older ``outline/``."""
    draft = folder / "draft"
    return draft if draft.is_dir() or not (folder / "outline").is_dir() else folder / "outline"


def _register(folder: Path, stem: str) -> tuple[list[dict], Path]:
    """Parse ``draft/<stem>-design-items.md`` (``outline/`` before 0.118): one block per Design Item.

    The register is the bet and its rules (type, audience, job, goal,
    stance, basis, mode, expected, falsified, evidence, acceptance).  State is
    never read from it; it is derived from the Runs that name the item.
    """
    path = plan_folder(folder) / f"{stem}-design-items.md"
    items: list[dict] = []
    current = None
    for line in _read(path).splitlines():
        head = _ITEM_HEAD.match(line.strip())
        if head:
            current = {"id": head.group(1), "title": head.group(2), "_list": None,
                       **{key: "" for key in _ITEM_FIELDS}, **{key: [] for key in _ITEM_LISTS}}
            items.append(current)
            continue
        if current is None:
            continue
        if line.startswith("- ") and current["_list"]:
            current[current["_list"]].append(line[2:].strip())
            continue
        field = _FIELD.match(line.strip())
        if field:
            key, value = field.group(1), field.group(2)
            if key in _ITEM_LISTS and not value:
                current["_list"] = key
            elif key in _ITEM_FIELDS:
                current[key] = value
                current["_list"] = None
    for item in items:
        item.pop("_list", None)
    return items, path


# -------------------------------------------------------------------- runs --

def _actor(*records) -> tuple[str, str]:
    """Return (name, mode) from the first record that names an actor."""
    for record in records:
        if not isinstance(record, dict):
            continue
        actor = record.get("actor")
        if isinstance(actor, dict) and actor.get("owner"):
            return str(actor["owner"]), str(actor.get("mode") or "")
        if isinstance(actor, str) and actor:
            return actor, ""
        worker = record.get("worker")
        if isinstance(worker, dict) and worker.get("actor"):
            return str(worker["actor"]), "agent"
    return "", ""


def _when(value) -> str:
    text = str(value or "")
    text = text.replace("T", " ").rstrip("Z")
    return text[:16]


def _load_runs(folder: Path) -> list[dict]:
    runs_dir = folder / "runs"
    if not runs_dir.is_dir():
        return []
    rows = []
    for ticket_path in sorted(runs_dir.iterdir()):
        hit = _RUN_FILE.match(ticket_path.name)
        new = None if hit else _RUN_FILE_NEW.match(ticket_path.name)
        if not hit and not new:
            continue
        ticket = _yaml(ticket_path)
        if hit:
            run_id, number, kind = hit.group(1), int(hit.group(2)), hit.group(3).lower()
        else:
            run_id, kind = new.group(1), new.group(2)
            try:
                number = int(ticket.get("sequence") or 0)
            except (TypeError, ValueError):
                number = 0
        result_dir = folder / "results" / run_id
        runtime = _yaml(result_dir / "runtime.yaml")
        result = _yaml(result_dir / "result.yaml")
        decision = _yaml(result_dir / "decision.yaml")
        checks = _yaml(result_dir / "checks.yaml").get("checks") or []
        config_ref = ticket.get("config") if isinstance(ticket.get("config"), dict) else next(
            (r for r in ticket.get("inputs") or []           # a Commission pins its config among its inputs
             if isinstance(r, dict) and str(r.get("path", "")).startswith("scripts/config/")), {})
        config = _yaml(folder / str(config_ref.get("path", ""))) if config_ref.get("path") else {}
        name, mode = _actor(decision, runtime, ticket)
        mode = mode or ("human" if kind in ("commission", "adopt") else "agent")
        artifacts = []
        for ref in result.get("artifacts") or []:
            if isinstance(ref, dict) and ref.get("path"):
                path = result_dir / str(ref["path"])
                artifacts.append({"path": path, "text": _read(path).strip()})
        inputs = []
        for ref in ticket.get("inputs") or []:
            if isinstance(ref, dict) and ref.get("path") and ref.get("role"):
                inputs.append({"role": str(ref["role"]), "path": str(ref["path"]),
                               "run_id": str(ref.get("run_id") or ""),
                               "file": (folder / str(ref["path"])).resolve()})
        status = str(runtime.get("status") or ("complete" if decision else "planned"))
        stale = []
        if status == "planned" and kind in ("generate", "verify"):
            from live.design_actions import stale_inputs
            stale = stale_inputs(folder, run_id)
        verdict = str(result.get("verdict") or "")
        outcome = str(decision.get("decision") or runtime.get("terminal_outcome") or verdict)
        passed = sum(1 for c in checks if isinstance(c, dict) and c.get("status") == "pass")
        intent = config.get("design_intent") if isinstance(config.get("design_intent"), dict) else {}
        rows.append({
            "id": run_id, "number": number, "kind": kind, "step": _STEP[kind],
            "item": str(ticket.get("item") or config.get("item") or runtime.get("item") or ""),
            "target": str(ticket.get("target") or ""),
            "actor": name or "not recorded", "mode": mode,
            "status": status, "verdict": verdict, "outcome": outcome,
            "route": str(runtime.get("route") or ""),
            "started": _when(runtime.get("started_at")),
            "finished": _when(runtime.get("finished_at") or decision.get("at") or runtime.get("queued_at")),
            "failure": str(runtime.get("failure") or ""), "stale": stale,
            "words": str(decision.get("words") or ""),
            "checks": [c for c in checks if isinstance(c, dict)],
            "checks_passed": passed,
            "artifacts": artifacts, "inputs": inputs,
            "targets": [t for t in (ticket.get("targets") or []) if isinstance(t, dict)],
            "candidate": decision.get("candidate") if isinstance(decision.get("candidate"), dict) else {},
            "verification": decision.get("verification") if isinstance(decision.get("verification"), dict) else {},
            "preview": decision.get("preview") if isinstance(decision.get("preview"), dict) else {},
            "intent": {k: intent.get(k) for k in ("move", "basis", "stance", "expected_effect", "failure_condition")},
            "design_mode": str(config.get("mode") or ""),
            "criteria": config.get("criteria") or [],
            "acceptance": config.get("acceptance") if isinstance(config.get("acceptance"), list) else None,
            "ticket_path": ticket_path, "result_dir": result_dir,
        })
    rows.sort(key=lambda row: row["number"])
    return rows


def _fold_state(runs: list[dict], human: str = "person") -> tuple[str, str, str]:
    """Walk an item's Runs in order and return (state, glyph, waiting-on).

    "agent" is waited on only while a run is queued or running; a step that needs a
    click says "you" and never a name (a name here reads as the person who
    signed the last record, which is a different fact). `human` is kept for callers
    that still pass it and is no longer written to a surface."""
    state, glyph, waiting = "not commissioned", "⬜", "you · commission"
    for run in runs:
        if run["status"] == "superseded":
            continue
        if run["status"] == "blocked":
            state, glyph, waiting = "blocked", "⏸", f"you · resolve {run['id']}: {run['failure'] or 'blocked; inspect the Run record'}"
            continue
        if run["kind"] == "commission":
            if run["outcome"] == "release":
                state, glyph, waiting = "commissioned", "⬜", "you · queue the draft"
            elif run["outcome"] == "hold":
                state, glyph, waiting = "commission held", "⏸", "you · release or hold"
            else:
                state, glyph, waiting = "commission open", "⬜", "you · release or hold"
        elif run["kind"] == "generate":
            if run["status"] == "complete":
                state, glyph, waiting = "generated", "⬜", "you · queue the review"
            elif run["status"] == "failed":
                state, glyph, waiting = "generate failed", "✗", "you · queue a revise"
            elif run["status"] == "planned" and run.get("stale"):
                state, glyph, waiting = "queued run out of date", "⚠", "you · queue again"
            elif run["status"] == "planned":
                state, glyph, waiting = "generate queued", "⬜", "agent · generate"
            else:
                state, glyph, waiting = "generating", "⬜", "agent · running"
        elif run["kind"] == "verify":
            if run["status"] == "complete" and run["verdict"] == "pass":
                state, glyph, waiting = "ready", "✅", ""
            elif run["status"] == "complete" and run["verdict"] == "unresolved":
                owners = sorted({str(c.get("next_owner")) for c in run["checks"]
                                 if c.get("status") == "unresolved" and c.get("next_owner")})
                owner_text = ", ".join(owners) if owners else "you"
                state, glyph, waiting = "verify unresolved", "⏸", (
                    f"{owner_text} · resolve the recorded evidence/criterion gap; "
                    "preserve this Result and review only after inputs or criteria change")
            elif run["status"] == "complete":
                state, glyph, waiting = "verify failed", "✗", "you · queue a revise"
            elif run["status"] == "failed":
                # The review itself did not pass the gate: redo the review, not the candidate.
                state, glyph, waiting = "verify invalid", "✗", "you · queue the review again"
            elif run["status"] == "planned" and run.get("stale"):
                state, glyph, waiting = "queued run out of date", "⚠", "you · queue again"
            elif run["status"] == "planned":
                state, glyph, waiting = "verify queued", "⬜", "agent · verify"
            else:
                state, glyph, waiting = "verifying", "⬜", "agent · running"
        elif run["kind"] == "adopt":
            # Historical adoption records are read as an already-ready delivery.
            # New records never create this kind; the user-facing workflow ends at Verify.
            if run["outcome"] == "adopt":
                state, glyph, waiting = "ready", "✅", ""
            elif run["outcome"] == "decline":
                state, glyph, waiting = "declined", "🚫", ""
            elif run["outcome"] == "revise":
                state, glyph, waiting = "generated", "⬜", "you · queue the review"
            elif run["outcome"] == "hold":
                state, glyph, waiting = "legacy hold", "⏸", "you · historical decision; register a new item to continue"
            else:
                state, glyph, waiting = "generated", "⬜", "you · queue the review"
    return state, glyph, waiting


def _verified_design(item: dict) -> dict | None:
    """Return the candidate whose latest independent Verify passed.

    Delivery is deliberately derived from the Verify record, not from a
    separate human decision.  Historical ``run-design-adopt-*`` records may still
    be present, but they are not required for a design to be ready.
    """
    if item.get("state") != "ready":
        return None
    runs = item.get("runs") or []
    verify = next((r for r in reversed(runs)
                   if r["kind"] == "verify" and r["status"] == "complete"
                   and r.get("verdict") == "pass"), None)
    if verify is None:
        return None
    targets = verify.get("targets") or []
    target_path = str(targets[0].get("path") or "") if targets else ""
    target_file = (verify["ticket_path"].parent.parent / target_path).resolve() if target_path else None
    candidate = next((r for r in reversed(runs)
                      if r["kind"] == "generate" and r["status"] == "complete"
                      and r.get("artifacts")
                      and target_file == (r["result_dir"] / "result.yaml").resolve()), None)
    if candidate is None:
        return None
    # A completion receipt describes a past event; Delivery must still bind
    # the reviewed files. Recheck the two Results before exporting them.
    try:
        gate = _unit_gate()
        for run in (candidate, verify):
            problems = gate.validate(run["ticket_path"], run["result_dir"] / "result.yaml", historical=True)
            if problems:
                raise ValueError(f"{run['id']}: {'; '.join(problems)}")
        _, _, _, _, config, _ = gate.context(verify["ticket_path"], historical=True)
        if config["review_mode"] != "independent":
            raise ValueError(f"{verify['id']}: Delivery requires independent review")
    except (OSError, ImportError, AttributeError, TypeError, KeyError) as exc:
        raise ValueError(f"Delivery records check unavailable: {exc}") from exc
    art = candidate["artifacts"][0]
    return {"run": candidate["id"], "text": art["text"], "verification": verify["id"]}


def shown_design(item: dict) -> dict | None:
    """The design an item has: its ready candidate, else its latest draft."""
    return item.get("ready") or item.get("latest")


def _held_at(item: dict) -> str:
    """For an item on hold: the Commission that held it, else ``""``."""
    if item["state"] != "commission held":
        return ""
    last = next((r for r in reversed(item["runs"]) if r["kind"] == "commission"
                 and r["status"] != "superseded"), None)
    return last["kind"] if last and last["outcome"] == "hold" else ""


def _stale_names(item: dict) -> list[str]:
    return [name for r in item["runs"] for name in r.get("stale") or []]


_ALLOWED = {
    "commission-release": ("not commissioned", "commission open"),
    "commission-hold": ("not commissioned", "commission open"),
    "queue-generate": ("commissioned", "revise requested"),
    "queue-revise": ("generate failed", "verify failed"),
    "queue-verify": ("generated", "verify invalid"),
    "requeue": ("queued run out of date",),
}
