"""🎨 Design · the writer behind the Design tab's buttons.

Every action here writes exactly the files the Design contract already names
(``haipipe-design`` register, ``haipipe-design-workflow`` Tickets and
decisions, ``haipipe-design-unit`` v2 config/receipt shapes) and nothing else.
A person's Commission decision is written with the person's name and words;
agent steps (Generate, Verify) are only *queued* as planned Tickets for
``haipipe-designer-agent`` to execute. A passed Verify becomes ready for
Delivery without a second human decision. Nothing here generates content,
judges a candidate, or marks a Run complete on the agent's behalf.
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from live.design import plan_folder

import yaml

TICKET_SCHEMA = "haipipe.design-ticket/v2"
STANCES = ("follow", "challenge", "explore", "generate")
BASES = ("brief-only", "evidence-informed")
MODES = ("compose", "revise", "brainstorm", "theory-driven", "challenge")
ROLES = ("evidence", "inspiration", "reference", "avoid", "base", "feedback", "handoff")
_RD = re.compile(r"^rd(\d+)_", re.I)
# Design Run names, the Page grammar with `design` as the family word:
#   run-design-<step>-<MMDD>-design-<N>[-2]   e.g. run-design-generate-0918-design-1
# Older `rdNN_<step>_itemNN` names are retired (rename_runs.py renames a folder once); a
# folder not yet renamed still orders by its rd number. Order is the ticket's `sequence:`.
RUN_NAME = re.compile(r"^run-design-(commission|generate|verify|adopt)-(\d{4})-([a-z0-9]+(?:-[a-z0-9]+)*)$")

# The parts live in sibling modules; every name stays readable here (design_actions.X).
from live.design_actions_files import ActionError, _dump, _load, _now, _ref, _relative, _slug  # noqa: F401,E402
from live.design_actions_criteria import (_CLAUSE, _CONNECTOR, _ENDS, _MAX_CHARS, _MAX_CHARS_2,  # noqa: F401,E402
                                          _NEGATIVE, _PLACEHOLDER, _QUOTED, _RENDER, _STARTS, _STRICT,
                                          _judged_criterion, _phrases, compile_criteria)
from live.design_actions_workers import (complete_run, name_worker, planned_runs, release_worker,  # noqa: F401,E402
                                         stale_inputs, supersede)
from live.design_actions_draft import (_COUNSEL, counsel_lines, counsel_rules, draft_request_path,  # noqa: F401,E402
                                       open_draft_request, request_draft)


def run_sequence(ticket: Path) -> int:
    """A Design Run's place in its folder: the ticket's `sequence:`, else its old rd number."""
    hit = _RD.match(ticket.name)
    if hit:
        return int(hit.group(1))
    try:
        return int((yaml.safe_load(ticket.read_text(encoding="utf-8")) or {}).get("sequence") or 0)
    except (OSError, ValueError, TypeError, yaml.YAMLError):
        return 0


def _next_run(folder: Path) -> int:
    runs = folder / "runs"
    tickets = [p for pat in ("rd*_*.yaml", "run-design-*.yaml") for p in runs.glob(pat)] if runs.is_dir() else []
    return max((run_sequence(p) for p in tickets), default=0) + 1


def design_slug(item_id: str) -> str:
    """`ITEM01` -> `design-1`: the design as the screen says it (Design 1)."""
    hit = re.match(r"^ITEM0*(\d+)$", str(item_id), re.I)
    return f"design-{hit.group(1)}" if hit else _slug(item_id).replace("_", "-")


def run_name(folder: Path, step: str, item_id: str, day: datetime | None = None) -> str:
    """A new Design Run name; a second one of the same step, day and design gets `-2`, `-3`."""
    base = f"run-design-{step}-{(day or datetime.now()).strftime('%m%d')}-{design_slug(item_id)}"
    name, n = base, 1
    while (folder / "runs" / f"{name}.yaml").exists() or (folder / "results" / name).exists():
        n += 1
        name = f"{base}-{n}"
    return name


def _register_path(folder: Path, stem: str) -> Path:
    return plan_folder(folder) / f"{stem}-design-items.md"


# --------------------------------------------------------------- register --

def next_item_id(register_text: str) -> str:
    numbers = [int(n) for n in re.findall(r"(?m)^##\s+ITEM(\d+)\b", register_text)]
    return f"ITEM{max(numbers, default=0) + 1:02d}"


# The design element is a first citizen. When the board's Design Goal names the
# starting text's elements (`Elements:` under Resources), every new Design Item asks its
# Generate for the element record under those names, as a rule its Verify checks.
ELEMENT_RULE = (
    "semantic: every element recorded | observe: read the Result's elements.yaml beside the text | "
    "pass: each element of the text has one entry naming its words, where it came from (requirements, "
    "internal insight, external insight or intuition), the rule, row or theory it rests on, and whether it "
    "was reasoned or intuitive; the Design Goal's elements keep their names ({names}), and any other element "
    "is named for its role | fail: an element of the text has no entry, an entry names no source or no kind "
    "of thinking, or a Design Goal element goes under another name | not-verifiable: elements.yaml is missing")


def goal_element_rule(folder: Path) -> str:
    """The element-record rule for a new item in this Design Folder, or "" when the board's
    Design Goal names no elements."""
    from live.design import design_input, element_slots
    inp = design_input(Path(folder).parent.parent, Path(folder))
    aim = {k.lower(): v for rows in inp["blocks"].values() for k, v, _ in rows}
    slots = element_slots(aim)
    return ELEMENT_RULE.format(names=", ".join(name for name, _ in slots)) if slots else ""


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
    expected = (fields.get("expected") or "").strip()
    falsified = (fields.get("falsified") or "").strip()
    # the same bindings the records check enforces (check_unit.design_intent), said up front
    if (stance == "challenge") != (mode == "challenge"):
        raise ActionError("a challenge stance goes with challenge mode, and only with it")
    if mode in ("challenge", "theory-driven") and not (expected and falsified):
        raise ActionError(f"{mode} needs both expected and falsified: the bet and what would prove it wrong")
    if mode == "brainstorm" and stance not in ("explore", "generate"):
        raise ActionError("brainstorm goes with stance explore or generate")
    if mode == "brainstorm" and (expected or falsified):
        raise ActionError("brainstorm makes rough options, so it carries no expected or falsified")
    acceptance = [line.strip("- ").strip() for line in str(fields.get("acceptance") or "").splitlines()
                  if line.strip("- ").strip()]
    if not acceptance:
        raise ActionError("a Design Item needs at least one acceptance rule")
    element_rule = goal_element_rule(folder)
    if element_rule and not any("elements.yaml" in rule for rule in acceptance):
        acceptance.append(element_rule)
    try:
        compile_criteria(acceptance)
    except ValueError as exc:
        raise ActionError(str(exc)) from exc
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
    if expected:
        lines.append(f"expected: {expected}")
    if falsified:
        lines.append(f"falsified: {falsified}")
    if (fields.get("because") or "").strip():
        lines.append(f"because: {fields['because'].strip()}")
    if evidence:
        lines.append("evidence:")
        lines += [f"- {line}" for line in evidence]
    lines.append("acceptance:")
    lines += [f"- {rule}" for rule in acceptance]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip("\n") + "\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    return {"item": item_id, "register": path.as_posix()}


def split_evidence(line: str) -> tuple[str, str]:
    """One register evidence line, `role · path` or `role  path`, as (role, path).

    The path is relative to the Design Folder (the folder holding `<stem>.md`).
    An unknown role word reads as `evidence`."""
    parts = [p.strip() for p in re.split(r"\s*·\s*|\s{2,}", line.strip(), maxsplit=1)]
    role, ref = (parts[0], parts[1]) if len(parts) == 2 else ("evidence", parts[0])
    return (role if role in ROLES else "evidence"), ref


def _evidence_inputs(folder: Path, evidence: list[str]) -> tuple[list[dict], list[str]]:
    """Resolve register evidence lines (`role · path`) into Ticket inputs."""
    inputs, missing = [], []
    for line in evidence:
        role, ref = split_evidence(line)
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
        "goal": item.get("goal") or item.get("title"), "kind": item.get("type") or "sms", "mode": mode,
        "basis": intent["basis"], "item": item["id"], "design_intent": intent,
        "unit": {"shape": "single", "count": 1}, "max_iterations": 2,
        "review_mode": review_mode, "criteria": compile_criteria(item.get("acceptance") or []),
        "acceptance": list(item.get("acceptance") or []),   # the rule text as released, for the card
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
        "inputs": inputs,
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
    runs = item.get("runs") or []
    released = _latest(runs, "commission", outcome="release")
    if released is not None:
        raise ActionError(f"{item['id']} was already released in {released['id']}; at most one released Commission per item")
    number = _next_run(folder)
    run = run_name(folder, "commission", item["id"])
    config_path = _config(folder, stem, item, run, "self")
    inputs, missing = _evidence_inputs(folder, item.get("evidence") or [])
    if (item.get("basis") == "evidence-informed") and not inputs:
        raise ActionError("evidence-informed item, but no evidence file resolves: " + ", ".join(missing))
    all_inputs = [_ref(folder, config_path)] + inputs
    ticket_path = _dump(folder / "runs" / f"{run}.yaml", {
        "schema": TICKET_SCHEMA, "run": run, "sequence": number, "run_type": "Design.commission",
        "operation": "commission", "item": item["id"], "target": item.get("title"),
        "actor": {"mode": "human", "owner": actor},
        "action": "release or hold the frozen commission", "inputs": all_inputs,
        "entry_gate": "the Design Item is registered",
        "exit_gate": {"mode": "human", "assertion": "decision names the exact config file"},
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


def _frozen(folder: Path, stem: str, item: dict, released: dict, run: str, review_mode: str,
            mode: str | None = None) -> tuple[Path, list[str]]:
    """The config and evidence lines a released Commission froze, copied for a new run.

    An edit to the register after release reaches only the next Commission
    (audit H2, 260918).  A Commission written before configs were pinned falls
    back to the register."""
    ticket = _load(folder / "runs" / f"{released['id']}.yaml")
    refs = [r for r in ticket.get("inputs") or [] if isinstance(r, dict) and r.get("path")]
    config_ref = next((r for r in refs if str(r["path"]).startswith("scripts/config/")), None)
    frozen = _load(folder / config_ref["path"]) if config_ref else {}
    evidence = [f"{r['role']} · {r['path']}" for r in refs if r.get("role") in ROLES]
    if not frozen:
        legacy_mode = "challenge" if mode and item.get("stance") == "challenge" else mode
        return _config(folder, stem, item, run, review_mode, legacy_mode), item.get("evidence") or []
    config = dict(frozen, review_mode=review_mode)
    if mode:
        config["mode"] = "challenge" if frozen.get("design_intent", {}).get("stance") == "challenge" else mode
    return _dump(folder / "scripts" / "config" / f"{run}.yaml", config), evidence


def open_runs(runs: list[dict]) -> list[dict]:
    """An item's Generate and Verify runs that are queued or running (not closed, not superseded)."""
    return [r for r in runs if r["kind"] in ("generate", "verify") and r["status"] in ("planned", "running")]


def _refuse_if_open(runs: list[dict]) -> None:
    busy = open_runs(runs)
    if busy:
        raise ActionError(f"{busy[-1]['id']} is already {busy[-1]['status']} for this item; wait for it to close")


def _latest(runs: list[dict], kind: str, **where) -> dict | None:
    rows = [r for r in runs if r["kind"] == kind and all(r.get(k) == v for k, v in where.items())]
    return rows[-1] if rows else None


def queue_generate(folder: Path, stem: str, item: dict, runs: list[dict],
                   feedback: str = "", base_run: str = "") -> dict:
    """Allocate a planned Generate (or revise) Ticket for the designer agent."""
    released = _latest(runs, "commission", outcome="release")
    if released is None:
        raise ActionError("no released Commission for this item; a person releases first")
    _refuse_if_open(runs)
    number = _next_run(folder)
    run = run_name(folder, "generate", item["id"])
    mode = None
    extra_inputs: list[dict] = []
    if feedback.strip():
        base = next((r for r in reversed(runs) if r["id"] == base_run), None) if base_run else \
            next((r for r in reversed(runs) if r["kind"] == "generate" and r["artifacts"]), None)
        if base is None or not base["artifacts"]:
            raise ActionError("revise needs an earlier candidate to revise")
        # A passed review is ready for Delivery.  If a later brief change needs
        # a new candidate, the normal revise path may queue it again; there is
        # no separate adoption decision in the Design workflow.
        note = plan_folder(folder) / "feedback" / f"{run}.md"
        note.parent.mkdir(parents=True, exist_ok=True)
        note.write_text(f"# feedback for {run}\n\nbase: {base['id']}\n\n{feedback.strip()}\n",
                        encoding="utf-8")
        extra_inputs = [{"role": "base", "run_id": base["id"], **_ref(folder, base["artifacts"][0]["path"])},
                        {"role": "feedback", **_ref(folder, note)}]
        # Derive challenge mode from the released config in _frozen, never from
        # a register that may have changed since release.
        mode = "revise"
    config_path, evidence = _frozen(folder, stem, item, released, run, "self", mode)
    inputs, missing = _evidence_inputs(folder, evidence)
    if missing:
        raise ActionError("evidence named at release is gone: " + ", ".join(missing))
    approval = folder / "results" / released["id"] / "decision.yaml"
    _dump(folder / "runs" / f"{run}.yaml", {
        "schema": TICKET_SCHEMA, "run": run, "sequence": number, "operation": "generate",
        "worker": "haipipe-design-unit", "actor": "designer-context-pending",
        "item": item["id"], "target": item.get("title"), "config": _ref(folder, config_path),
        "approval": {"actor": released["actor"], "record": _ref(folder, approval)},
        "inputs": inputs + extra_inputs, "targets": [],
    })
    _dump(folder / "results" / run / "runtime.yaml", {
        "run": run, "family": "design", "operation": "generate", "item": item["id"],
        "target": item.get("title"), "status": "planned",
        "ticket": f"runs/{run}.yaml", "result": f"results/{run}/",
        "inputs": [_ref(folder, config_path), _ref(folder, approval)] + inputs + extra_inputs,
        "worker": {"kind": "skill", "name": "haipipe-design-unit", "actor": "designer-context-pending"},
        "queued_at": _now(),
    })
    return {"run": run, "mode": _load(config_path)["mode"]}


def queue_verify(folder: Path, stem: str, item: dict, runs: list[dict]) -> dict:
    released = _latest(runs, "commission", outcome="release")
    if released is None:
        raise ActionError("no released Commission for this item")
    generated = _latest(runs, "generate", status="complete")
    if generated is None:
        raise ActionError("no complete Generate Result to verify yet")
    _refuse_if_open(runs)
    judged = [r for r in runs if r["kind"] == "verify" and r["status"] == "complete"
              and any(str(t.get("path", "")).startswith(f"results/{generated['id']}/") for t in r.get("targets") or [])]
    if judged:
        raise ActionError(f"{generated['id']} already has an independent review ({judged[-1]['id']})")
    number = _next_run(folder)
    run = run_name(folder, "verify", item["id"])
    config_path, evidence = _frozen(folder, stem, item, released, run, "independent")
    approval = folder / "results" / released["id"] / "decision.yaml"
    target = _ref(folder, generated["result_dir"] / "result.yaml")
    # The reviewer reads the same evidence the bet rests on; an
    # evidence-informed Ticket with no evidence input fails the gate.
    inputs, missing = _evidence_inputs(folder, evidence)
    if missing:
        raise ActionError("evidence named at release is gone: " + ", ".join(missing))
    _dump(folder / "runs" / f"{run}.yaml", {
        "schema": TICKET_SCHEMA, "run": run, "sequence": number, "operation": "verify",
        "worker": "haipipe-design-unit", "actor": "reviewer-context-pending",
        "item": item["id"], "target": item.get("title"), "config": _ref(folder, config_path),
        "approval": {"actor": released["actor"], "record": _ref(folder, approval)},
        "inputs": inputs, "targets": [target],
    })
    _dump(folder / "results" / run / "runtime.yaml", {
        "run": run, "family": "design", "operation": "verify", "item": item["id"],
        "target": item.get("title"), "status": "planned",
        "ticket": f"runs/{run}.yaml", "result": f"results/{run}/",
        "inputs": [_ref(folder, config_path), _ref(folder, approval)] + inputs + [target],
        "worker": {"kind": "skill", "name": "haipipe-design-unit", "actor": "reviewer-context-pending"},
        "queued_at": _now(),
    })
    return {"run": run, "verifies": generated["id"]}


def adopt(folder: Path, stem: str, item: dict, runs: list[dict], decision: str,
          actor: str, words: str) -> dict:
    """Retired write entry; historical records remain readable by the presenter."""
    raise ActionError("Adopt writes are retired; independent Verify pass is ready for Delivery")


def requeue(folder: Path, stem: str, item: dict, runs: list[dict]) -> dict:
    """Queue again: replace an item's out-of-date queued run with a fresh one that names today's files.

    A person asks for this on the page after an insight page changed under a queued
    run (audit H3); the old run is kept as superseded, with the files that changed."""
    stale = [r for r in open_runs(runs) if r["status"] == "planned" and stale_inputs(folder, r["id"])]
    if not stale:
        raise ActionError("no queued run of this item is out of date")
    old = stale[-1]
    changed = stale_inputs(folder, old["id"])
    supersede(folder, old["id"], "an input changed after it was queued: " + ", ".join(changed))
    rest = [dict(r, status="superseded") if r["id"] == old["id"] else r for r in runs]
    if old["kind"] == "verify":
        return {**queue_verify(folder, stem, item, rest), "replaces": old["id"], "changed": changed}
    ticket = _load(folder / "runs" / f"{old['id']}.yaml")
    base = next((i for i in ticket.get("inputs") or [] if isinstance(i, dict) and i.get("role") == "base"), None)
    note = next((i for i in ticket.get("inputs") or [] if isinstance(i, dict) and i.get("role") == "feedback"), None)
    feedback = ""
    if note and (folder / str(note["path"])).is_file():
        feedback = (folder / str(note["path"])).read_text(encoding="utf-8").split("\n\n", 2)[-1].strip()
    out = queue_generate(folder, stem, item, rest, feedback=feedback,
                         base_run=str(base.get("run_id") or "") if base else "")
    return {**out, "replaces": old["id"], "changed": changed}
