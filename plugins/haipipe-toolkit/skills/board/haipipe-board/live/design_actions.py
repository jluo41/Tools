"""🎨 Design · the writer behind the Design tab's buttons.

Every action here writes exactly the files the Design contract already names
(``haipipe-design`` register, ``haipipe-design-workflow`` Tickets and
decisions, ``haipipe-design-unit`` v2 config/receipt shapes) and nothing else.
A person's decisions (Commission, Adopt) are written with the person's name
and words; agent steps (Generate, Verify) are only *queued* as planned Tickets
for ``haipipe-designer-agent`` to execute.  Nothing here generates content,
judges a candidate, or marks a Run complete on the agent's behalf.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

TICKET_SCHEMA = "haipipe.design-ticket/v2"
STANCES = ("follow", "challenge", "explore", "generate")
BASES = ("brief-only", "evidence-informed")
MODES = ("compose", "revise", "brainstorm", "theory-driven", "challenge")
ROLES = ("evidence", "inspiration", "reference", "avoid", "base", "feedback", "handoff")
_RD = re.compile(r"^rd(\d+)_", re.I)
_QUOTED = re.compile(r"['\"‘’“”]([^'\"‘’“”]+)['\"‘’“”]")
_PLACEHOLDER = re.compile(r"\{[A-Za-z_]+\}")
_MAX_CHARS = re.compile(r"(?:≤|<=|at most|max(?:imum)?|no more than|under)\s*(\d+)\s*(?:chars?|characters?|字)", re.I)
_MAX_CHARS_2 = re.compile(r"(\d+)\s*(?:chars?|characters?)\s*(?:max|cap|or fewer|or less)", re.I)


class ActionError(ValueError):
    """A refused action; the message is shown to the person unchanged."""


# ------------------------------------------------------------------ files --

def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _dump(path: Path, obj) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(obj, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return path


def _load(path: Path) -> dict:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _ref(folder: Path, path: Path) -> dict:
    rel = path.resolve().relative_to(folder.resolve()) if folder.resolve() in path.resolve().parents \
        else Path(_relative(folder, path))
    return {"path": rel.as_posix(), "sha256": _digest(path)}


def _relative(folder: Path, path: Path) -> str:
    import os
    return os.path.relpath(path.resolve(), folder.resolve())


def _slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9_-]+", "-", text.lower()).strip("-_")
    return slug or "item"


def _next_run(folder: Path) -> int:
    runs = folder / "runs"
    numbers = [int(m.group(1)) for p in runs.glob("rd*_*.yaml")
               if (m := _RD.match(p.name))] if runs.is_dir() else []
    return max(numbers, default=0) + 1


def _register_path(folder: Path, stem: str) -> Path:
    return folder / "outline" / f"{stem}-design-items.md"


# --------------------------------------------------------------- register --

def next_item_id(register_text: str) -> str:
    numbers = [int(n) for n in re.findall(r"(?m)^##\s+ITEM(\d+)\b", register_text)]
    return f"ITEM{max(numbers, default=0) + 1:02d}"


def add_item(folder: Path, stem: str, fields: dict) -> dict:
    """Append one Design Item block to the register (goal and rules only, no state)."""
    title = (fields.get("title") or "").strip()
    goal = (fields.get("goal") or "").strip()
    if not title or not goal:
        raise ActionError("a Design Item needs a title and a goal")
    stance = (fields.get("stance") or "generate").strip()
    basis = (fields.get("basis") or "brief-only").strip()
    if stance not in STANCES:
        raise ActionError(f"stance must be one of {', '.join(STANCES)}")
    if basis not in BASES:
        raise ActionError(f"basis must be one of {', '.join(BASES)}")
    mode = (fields.get("mode") or ("challenge" if stance == "challenge" else "compose")).strip()
    if mode not in MODES:
        raise ActionError(f"mode must be one of {', '.join(MODES)}")
    acceptance = [line.strip("- ").strip() for line in str(fields.get("acceptance") or "").splitlines()
                  if line.strip("- ").strip()]
    if not acceptance:
        raise ActionError("a Design Item needs at least one acceptance rule")
    evidence = [line.strip("- ").strip() for line in str(fields.get("evidence") or "").splitlines()
                if line.strip("- ").strip()]
    if basis == "evidence-informed" and not evidence:
        raise ActionError("evidence-informed needs at least one evidence line (role · path)")
    path = _register_path(folder, stem)
    text = path.read_text(encoding="utf-8") if path.is_file() else (
        f"# {stem} · Design Items\n\nOne block per design target. Runs name an item through `item:`;\n"
        "state is derived from those Runs, never typed here.\n")
    item_id = (fields.get("id") or "").strip() or next_item_id(text)
    if re.search(rf"(?m)^##\s+{re.escape(item_id)}\b", text):
        raise ActionError(f"{item_id} already exists in the register")
    lines = [f"## {item_id} · {title}",
             f"type: {(fields.get('type') or 'sms').strip()}",
             f"audience: {(fields.get('audience') or '').strip()}",
             f"job: {(fields.get('job') or '').strip()}",
             f"goal: {goal}", f"stance: {stance}", f"basis: {basis}", f"mode: {mode}"]
    if (fields.get("expected") or "").strip():
        lines.append(f"expected: {fields['expected'].strip()}")
    if (fields.get("falsified") or "").strip():
        lines.append(f"falsified: {fields['falsified'].strip()}")
    if evidence:
        lines.append("evidence:")
        lines += [f"- {line}" for line in evidence]
    lines.append("acceptance:")
    lines += [f"- {rule}" for rule in acceptance]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip("\n") + "\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    return {"item": item_id, "register": path.as_posix()}


# --------------------------------------------------------------- criteria --

def compile_criteria(acceptance: list[str]) -> list[dict]:
    """Turn acceptance prose into v2 criteria; anything not mechanical is semantic."""
    criteria = []
    for index, rule in enumerate(acceptance, start=1):
        cid = f"r{index:02d}"
        lowered = rule.lower()
        hit = _MAX_CHARS.search(rule) or _MAX_CHARS_2.search(rule)
        if hit:
            criteria.append({"id": cid, "kind": "max_chars", "value": int(hit.group(1))})
            continue
        quoted = _QUOTED.search(rule)
        placeholder = _PLACEHOLDER.search(rule)
        negative = re.search(r"\b(no|never|without|excludes?|must not|avoid)\b", lowered)
        if quoted and negative:
            criteria.append({"id": cid, "kind": "excludes", "value": quoted.group(1)})
        elif quoted:
            criteria.append({"id": cid, "kind": "contains", "value": quoted.group(1)})
        elif placeholder and negative:
            criteria.append({"id": cid, "kind": "excludes", "value": placeholder.group(0)})
        elif placeholder:
            criteria.append({"id": cid, "kind": "contains", "value": placeholder.group(0)})
        else:
            criteria.append({"id": cid, "kind": "semantic", "description": rule})
    return criteria


def _evidence_inputs(folder: Path, evidence: list[str]) -> tuple[list[dict], list[str]]:
    """Resolve register evidence lines (`role · path`) into hashed Ticket inputs."""
    inputs, missing = [], []
    for line in evidence:
        parts = [p.strip() for p in re.split(r"\s*·\s*|\s{2,}", line, maxsplit=1)]
        role, ref = (parts[0], parts[1]) if len(parts) == 2 else ("evidence", parts[0])
        if role not in ROLES:
            role = "evidence"
        path = (folder / ref).resolve()
        if path.is_file():
            inputs.append({"role": role, **_ref(folder, path)})
        else:
            missing.append(ref)
    return inputs, missing


def _config(folder: Path, stem: str, item: dict, run: str, review_mode: str,
            mode: str | None = None) -> Path:
    intent = {
        "move": item.get("goal") or item.get("title"),
        "basis": item.get("basis") or "brief-only",
        "stance": item.get("stance") or "generate",
        "expected_effect": item.get("expected") or None,
        "failure_condition": item.get("falsified") or None,
    }
    mode = mode or item.get("mode") or ("challenge" if intent["stance"] == "challenge" else "compose")
    if mode == "brainstorm":
        intent["expected_effect"] = intent["failure_condition"] = None
    return _dump(folder / "scripts" / "config" / f"{run}.yaml", {
        "goal": item.get("title"), "kind": item.get("type") or "sms", "mode": mode,
        "basis": intent["basis"], "item": item["id"], "design_intent": intent,
        "unit": {"shape": "single", "count": 1}, "max_iterations": 2,
        "review_mode": review_mode, "criteria": compile_criteria(item.get("acceptance") or []),
    })


# ------------------------------------------------------------- decisions --

def _human_runtime(folder: Path, run: str, run_type: str, operation: str, item: dict,
                   target: str, actor: str, decision: str, inputs: list[dict],
                   route: str, ticket_path: Path):
    now = _now()
    _dump(folder / "results" / run / "runtime.yaml", {
        "run": run, "run_type": run_type, "operation": operation, "item": item["id"],
        "family": "design", "target": target,
        "actor": {"mode": "human", "owner": actor}, "action": decision,
        "status": "complete", "ticket": f"runs/{run}.yaml", "result": f"results/{run}/",
        "ticket_sha256": _digest(ticket_path), "inputs": inputs,
        "entry_gate": {"status": "passed", "assertion": "decision recorded by a named person"},
        "exit_gate": {"status": "passed", "assertion": "decision names its inputs"},
        "route": route, "terminal_outcome": decision,
        "started_at": now, "finished_at": now, "failure": None,
    })


def commission(folder: Path, stem: str, item: dict, actor: str, words: str,
               decision: str = "release") -> dict:
    if decision not in ("release", "hold"):
        raise ActionError("a Commission decision is release or hold")
    actor = actor.strip()
    if not actor:
        raise ActionError("the releasing person must be named")
    number = _next_run(folder)
    slug = _slug(item["id"])
    run = f"rd{number:02d}_commission_{slug}"
    config_path = _config(folder, stem, item, run, "self")
    inputs, missing = _evidence_inputs(folder, item.get("evidence") or [])
    if (item.get("basis") == "evidence-informed") and not inputs:
        raise ActionError("evidence-informed item, but no evidence file resolves: " + ", ".join(missing))
    all_inputs = [_ref(folder, config_path)] + inputs
    ticket_path = _dump(folder / "runs" / f"{run}.yaml", {
        "schema": TICKET_SCHEMA, "run": run, "run_type": "Design.commission",
        "operation": "commission", "item": item["id"], "target": item.get("title"),
        "actor": {"mode": "human", "owner": actor},
        "action": "release or hold the frozen commission", "inputs": all_inputs,
        "entry_gate": "the Design Item is registered",
        "exit_gate": {"mode": "human", "assertion": "decision names the exact config hash"},
        "routes": {"release": "generate", "hold": "HOLD"},
        "result": f"results/{run}/", "receipt": f"results/{run}/runtime.yaml",
    })
    _dump(folder / "results" / run / "decision.yaml", {
        "run": run, "item": item["id"], "decision": decision, "actor": actor,
        "words": words.strip() or f"{decision.title()} {item['id']}: {item.get('goal', '')}",
        "target": item.get("title"), "inputs": all_inputs, "at": _now(),
    })
    _human_runtime(folder, run, "Design.commission", "commission", item, item.get("title", ""),
                   actor, decision, all_inputs, "generate" if decision == "release" else "HOLD",
                   ticket_path)
    return {"run": run, "missing_evidence": missing}


def _latest(runs: list[dict], kind: str, **where) -> dict | None:
    rows = [r for r in runs if r["kind"] == kind and all(r.get(k) == v for k, v in where.items())]
    return rows[-1] if rows else None


def queue_generate(folder: Path, stem: str, item: dict, runs: list[dict],
                   feedback: str = "", base_run: str = "") -> dict:
    """Allocate a planned Generate (or revise) Ticket for the designer agent."""
    released = _latest(runs, "commission", outcome="release")
    if released is None:
        raise ActionError("no released Commission for this item; a person releases first")
    number = _next_run(folder)
    run = f"rd{number:02d}_generate_{_slug(item['id'])}"
    mode = None
    extra_inputs: list[dict] = []
    if feedback.strip():
        base = next((r for r in reversed(runs) if r["id"] == base_run), None) if base_run else \
            next((r for r in reversed(runs) if r["kind"] == "generate" and r["artifacts"]), None)
        if base is None or not base["artifacts"]:
            raise ActionError("revise needs an earlier candidate to revise")
        note = folder / "outline" / "feedback" / f"{run}.md"
        note.parent.mkdir(parents=True, exist_ok=True)
        note.write_text(f"# feedback for {run}\n\nbase: {base['id']}\n\n{feedback.strip()}\n",
                        encoding="utf-8")
        extra_inputs = [{"role": "base", "run_id": base["id"], **_ref(folder, base["artifacts"][0]["path"])},
                        {"role": "feedback", **_ref(folder, note)}]
        # A challenge bet stays in challenge mode (the checker binds stance to
        # mode); its revision is the same challenge over a frozen base + feedback.
        mode = "challenge" if (item.get("stance") == "challenge") else "revise"
    config_path = _config(folder, stem, item, run, "self", mode)
    inputs, _missing = _evidence_inputs(folder, item.get("evidence") or [])
    approval = folder / "results" / released["id"] / "decision.yaml"
    ticket_path = _dump(folder / "runs" / f"{run}.yaml", {
        "schema": TICKET_SCHEMA, "run": run, "operation": "generate",
        "worker": "haipipe-design-unit", "actor": "designer-context-pending",
        "item": item["id"], "target": item.get("title"), "config": _ref(folder, config_path),
        "approval": {"actor": released["actor"], "record": _ref(folder, approval)},
        "inputs": inputs + extra_inputs, "targets": [],
    })
    _dump(folder / "results" / run / "runtime.yaml", {
        "run": run, "family": "design", "operation": "generate", "item": item["id"],
        "target": item.get("title"), "status": "planned",
        "ticket": f"runs/{run}.yaml", "result": f"results/{run}/",
        "ticket_sha256": _digest(ticket_path),
        "inputs": [_ref(folder, config_path), _ref(folder, approval)] + inputs + extra_inputs,
        "worker": {"kind": "skill", "name": "haipipe-design-unit", "actor": "designer-context-pending"},
        "queued_at": _now(),
    })
    return {"run": run, "mode": mode or "compose"}


def queue_verify(folder: Path, stem: str, item: dict, runs: list[dict]) -> dict:
    released = _latest(runs, "commission", outcome="release")
    if released is None:
        raise ActionError("no released Commission for this item")
    generated = _latest(runs, "generate", status="complete")
    if generated is None:
        raise ActionError("no complete Generate Result to verify yet")
    number = _next_run(folder)
    run = f"rd{number:02d}_verify_{_slug(item['id'])}"
    config_path = _config(folder, stem, item, run, "independent")
    approval = folder / "results" / released["id"] / "decision.yaml"
    target = _ref(folder, generated["result_dir"] / "result.yaml")
    # The reviewer reads the same evidence the bet rests on; an
    # evidence-informed Ticket with no evidence input fails the gate.
    inputs, _missing = _evidence_inputs(folder, item.get("evidence") or [])
    ticket_path = _dump(folder / "runs" / f"{run}.yaml", {
        "schema": TICKET_SCHEMA, "run": run, "operation": "verify",
        "worker": "haipipe-design-unit", "actor": "reviewer-context-pending",
        "item": item["id"], "target": item.get("title"), "config": _ref(folder, config_path),
        "approval": {"actor": released["actor"], "record": _ref(folder, approval)},
        "inputs": inputs, "targets": [target],
    })
    _dump(folder / "results" / run / "runtime.yaml", {
        "run": run, "family": "design", "operation": "verify", "item": item["id"],
        "target": item.get("title"), "status": "planned",
        "ticket": f"runs/{run}.yaml", "result": f"results/{run}/",
        "ticket_sha256": _digest(ticket_path),
        "inputs": [_ref(folder, config_path), _ref(folder, approval)] + inputs + [target],
        "worker": {"kind": "skill", "name": "haipipe-design-unit", "actor": "reviewer-context-pending"},
        "queued_at": _now(),
    })
    return {"run": run, "verifies": generated["id"]}


def complete_run(folder: Path, run: str, started_at: str = "") -> dict:
    """The caller closes a worker Run: gate the Result, then write the receipt.

    The worker wrote only ``results/<run>/`` (content, checks, result.yaml).
    This step runs ``check_unit`` on the pair and records the truthful status:
    ``complete`` with the next route when the gate passes, ``failed`` with the
    gate's own words when it does not.  It never edits the Result.
    """
    import importlib.util
    checker = Path(__file__).resolve().parents[3] / "application" / "haipipe-design-unit" / "scripts" / "check_unit.py"
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
        runtime.update(status="failed", failure="; ".join(problems), route="generate")
    elif ticket.get("operation") == "verify" and verdict == "fail":
        runtime.update(status="complete", failure=None, route="generate", terminal_outcome="fail")
    else:
        runtime.update(status="complete", failure=None,
                       route="verify" if ticket.get("operation") == "generate" else "adopt",
                       terminal_outcome=verdict or "complete")
    _dump(runtime_path, runtime)
    return {"run": run, "status": runtime["status"], "verdict": verdict,
            "route": runtime.get("route"), "problems": problems}


def adopt(folder: Path, stem: str, item: dict, runs: list[dict], decision: str,
          actor: str, words: str) -> dict:
    if decision not in ("adopt", "decline", "revise", "hold"):
        raise ActionError("an Adopt decision is adopt, decline, revise, or hold")
    actor = actor.strip()
    if not actor:
        raise ActionError("the deciding person must be named")
    verified = _latest(runs, "verify", status="complete")
    if verified is None:
        raise ActionError("no complete Verify Result; adoption waits for the independent verifier")
    target_ref = (verified.get("targets") or [{}])[0]
    candidate = next((r for r in reversed(runs) if r["kind"] == "generate" and r["artifacts"]
                      and (not target_ref.get("path") or target_ref["path"].startswith(f"results/{r['id']}/"))), None)
    if candidate is None:
        raise ActionError("the verified candidate has no readable artifact")
    if decision == "adopt" and verified["verdict"] != "pass":
        raise ActionError(f"verify {verified['id']} did not pass; adopt is refused, revise or decline instead")
    artifact = candidate["artifacts"][0]["path"]
    number = _next_run(folder)
    run = f"rd{number:02d}_adopt_{_slug(item['id'])}"
    version = 1 + len(list((folder / "delivery" / "render").glob(f"{stem}-{item['id']}-v*.txt"))) \
        if (folder / "delivery" / "render").is_dir() else 1
    preview = folder / "delivery" / "render" / f"{stem}-{item['id']}-v{version}.txt"
    preview.parent.mkdir(parents=True, exist_ok=True)
    preview.write_bytes(Path(artifact).read_bytes())
    manifest_path = folder / "delivery" / "render" / "manifest.json"
    entries = json.loads(manifest_path.read_text()) if manifest_path.is_file() else []
    entries.append({"item": item["id"], "render": preview.name, "candidate": candidate["id"],
                    "sha256": _digest(preview), "version": version})
    manifest_path.write_text(json.dumps(entries, indent=2), encoding="utf-8")
    gen_result = _ref(folder, candidate["result_dir"] / "result.yaml")
    ver_result = _ref(folder, verified["result_dir"] / "result.yaml")
    inputs = [gen_result, ver_result, _ref(folder, preview)]
    ticket_path = _dump(folder / "runs" / f"{run}.yaml", {
        "schema": TICKET_SCHEMA, "run": run, "run_type": "Design.adopt", "operation": "adopt",
        "item": item["id"], "target": f"{item.get('title')} · exact verified candidate",
        "actor": {"mode": "human", "owner": actor},
        "action": "adopt, decline, revise, or hold the exact candidate", "inputs": inputs,
        "candidates": [{"run": candidate["id"], **_ref(folder, artifact)}],
        "verification": [{"run": verified["id"], **ver_result}], "preview": _ref(folder, preview),
        "entry_gate": "independent verify recorded",
        "exit_gate": {"mode": "human", "assertion": "decision names candidate hash"},
        "routes": {"adopt": "CLOSE", "decline": "CLOSE", "revise": "generate", "hold": "HOLD"},
        "result": f"results/{run}/", "receipt": f"results/{run}/runtime.yaml",
    })
    _dump(folder / "results" / run / "decision.yaml", {
        "run": run, "item": item["id"], "decision": decision, "actor": actor,
        "words": words.strip() or f"{decision.title()} {item['id']}",
        "candidate": {"run": candidate["id"], **_ref(folder, artifact)},
        "verification": {"run": verified["id"], **ver_result},
        "preview": _ref(folder, preview), "at": _now(),
    })
    route = {"adopt": "CLOSE", "decline": "CLOSE", "revise": "generate", "hold": "HOLD"}[decision]
    _human_runtime(folder, run, "Design.adopt", "adopt", item, f"{item.get('title')} · exact verified candidate",
                   actor, decision, inputs, route, ticket_path)
    out = {"run": run, "candidate": candidate["id"], "preview": preview.name}
    if decision == "revise":
        runs = runs + [{"id": run, "kind": "adopt", "outcome": "revise", "status": "complete",
                        "actor": actor, "artifacts": []}]
        out["revise"] = queue_generate(folder, stem, item, runs, feedback=words or "revise", base_run=candidate["id"])
    return out


# ------------------------------------------------------------ batch + queue --

def name_worker(folder: Path, run: str, actor: str) -> dict:
    """Name the real worker on a planned run record before dispatch, and re-pin the receipt."""
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
    runtime["ticket_sha256"] = _digest(ticket_path)
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
    runtime["ticket_sha256"] = _digest(ticket_path)
    runtime["status"] = "planned"
    runtime.pop("started_at", None)
    runtime.setdefault("lost_workers", []).append({"actor": lost, "at": _now(), "why": "left no result"})
    _dump(runtime_path, runtime)
    return {"run": run, "lost": lost}


def release_all(folder: Path, stem: str, items: list[dict], actor: str, words: str) -> dict:
    """Release every item that has no Commission yet; one decision Run per item."""
    todo = [i for i in items if i["state"] in ("not commissioned", "commission open")]
    if not todo:
        raise ActionError("nothing to release; every item already has a Commission")
    runs = [commission(folder, stem, item, actor, words, "release")["run"] for item in todo]
    return {"runs": runs, "items": [i["id"] for i in todo]}


def queue_all(folder: Path, stem: str, items: list[dict]) -> dict:
    """Queue the next agent step of every item that has one: Generate after release, Verify after generate."""
    runs, skipped = [], []
    for item in items:
        if item["state"] in ("commissioned", "revise requested"):
            runs.append(queue_generate(folder, stem, item, item["runs"])["run"])
        elif item["state"] == "generated":
            runs.append(queue_verify(folder, stem, item, item["runs"])["run"])
        else:
            skipped.append(item["id"])
    if not runs:
        raise ActionError("nothing to queue; no item is waiting for a Generate or a Verify")
    return {"runs": runs, "skipped": skipped}


def adopt_all(folder: Path, stem: str, items: list[dict], actor: str, words: str) -> dict:
    """Adopt every verified item with one name and one sentence; one decision Run per item."""
    todo = [i for i in items if i["state"] == "verified"]
    if not todo:
        raise ActionError("nothing to adopt; no item is verified")
    runs = [adopt(folder, stem, item, item["runs"], "adopt", actor, words)["run"] for item in todo]
    return {"runs": runs, "items": [i["id"] for i in todo]}


def planned_runs(folder: Path) -> list[dict]:
    """Every planned agent run in a folder: what the queue runner picks up."""
    out = []
    for runtime_path in sorted((folder / "results").glob("rd*/runtime.yaml")) if (folder / "results").is_dir() else []:
        runtime = _load(runtime_path)
        if runtime.get("status") == "planned" and runtime.get("operation") in ("generate", "verify"):
            out.append({"run": runtime.get("run") or runtime_path.parent.name,
                        "operation": runtime.get("operation"), "item": runtime.get("item"),
                        "ticket": (folder / str(runtime.get("ticket") or "")).as_posix(),
                        "folder": folder.as_posix()})
    return out


# ------------------------------------------------------------- rules + draft --

_COUNSEL = re.compile(r"^\s*(W\d+)\s+(DO NOT|DO)\s+(.+?)(?:\s{2,}\S.*)?$")


def counsel_lines(text: str) -> list[dict]:
    """The DO / DO NOT counsel lines of an insight page, in order."""
    rows = []
    for line in text.splitlines():
        hit = _COUNSEL.match(line)
        if hit:
            rows.append({"id": hit.group(1), "do": hit.group(2) == "DO", "text": hit.group(3).strip().rstrip(".")})
    return rows


def counsel_rules(text: str) -> list[str]:
    """Acceptance rules implied by the counsel: every DO NOT becomes a plain 'no …' rule."""
    return [f"does not {row['text'][0].lower() + row['text'][1:]}" for row in counsel_lines(text) if not row["do"]]


def draft_request_path(folder: Path, stem: str) -> Path:
    return folder / "outline" / f"{stem}-draft-request.md"


def request_draft(folder: Path, stem: str, goal: dict, insight_rows: list[dict], missing: int,
                  actor: str = "") -> dict:
    """Ask the agent to draft the missing Design Items: one request file the queue runner reads."""
    if missing < 1:
        raise ActionError("the register already has every design the Brief asks for")
    path = draft_request_path(folder, stem)
    if path.is_file():
        raise ActionError(f"a draft request is already open: {path.name}")
    lines = [f"# draft request · {stem}", "",
             f"asked-by: {actor or 'person'}", f"asked-at: {_now()}", f"items: {missing}",
             f"goal: {goal.get('sentence') or '(no Brief line)'}", ""]
    if goal.get("row"):
        row = goal["row"]
        lines += [f"venue: {row['venue']}", f"audience: {row['audience']}", f"job: {row['job']}", ""]
    lines.append("## insights to draw on")
    lines.append("")
    if insight_rows:
        for r in insight_rows:
            lines.append(f"- {r.get('word', r.get('role', 'insight'))} · {r.get('path', r.get('name', ''))}"
                         + (f" · {r['signed']}" if r.get("signed") else ""))
            if r.get("finding"):
                lines.append(f"  finding: {r['finding']}")
            if r.get("consequence"):
                lines.append(f"  then: {r['consequence']}")
            for c in r.get("counsel") or []:
                lines.append(f"  {'DO' if c['do'] else 'DO NOT'} {c['text']}")
    else:
        lines.append("- none · design from the Brief only")
    lines += ["", "## the agent writes",
              "", f"{missing} new Design Item blocks appended to the register through `design_actions.add_item`,",
              "each with its own goal, stance, basis, expected, falsified, evidence line, and acceptance rules",
              "(every DO NOT above becomes a rule). Then this file is removed.", ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return {"request": path.as_posix(), "items": missing}


def open_draft_request(folder: Path, stem: str) -> dict | None:
    path = draft_request_path(folder, stem)
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    field = lambda key: (re.search(rf"(?m)^{key}:\s*(.*)$", text) or [None, ""])[1]
    return {"path": path, "items": int(field("items") or 0), "asked_by": field("asked-by"), "asked_at": field("asked-at")}
