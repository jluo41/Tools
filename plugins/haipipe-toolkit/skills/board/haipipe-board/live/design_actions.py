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

import hashlib
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
# A quote opens after a space or line start and closes before one, so the apostrophe
# in "it's" or "doesn't" is never read as a quote mark (audit H1, 260918).
_QUOTED = re.compile(r"(?<!\w)['\"‘“](.+?)['\"’”](?!\w)")
_NEGATIVE = re.compile(r"\b(?:no|not|never|without|excludes?|avoids?|don['’]t|doesn['’]t|isn['’]t)\b", re.I)
_ENDS = re.compile(r"\b(?:ends|ending|finishes)\s+with\b", re.I)
_STARTS = re.compile(r"\b(?:starts|starting|begins|opens)\s+with\b", re.I)
_RENDER = re.compile(r"\brender(?:s|ed|ing)?\b", re.I)
_PLACEHOLDER = re.compile(r"\{[A-Za-z_]+\}")
_MAX_CHARS = re.compile(r"(≤|<=|<|at most|max(?:imum)?|no more than|under|fewer than|less than)\s*(\d+)\s*(?:chars?|characters?|字)", re.I)
_STRICT = ("<", "under", "fewer than", "less than")
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
    if evidence:
        lines.append("evidence:")
        lines += [f"- {line}" for line in evidence]
    lines.append("acceptance:")
    lines += [f"- {rule}" for rule in acceptance]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip("\n") + "\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    return {"item": item_id, "register": path.as_posix()}


# --------------------------------------------------------------- criteria --

_CLAUSE = re.compile(r",|;|\band\b|\bbut\b|\bwhile\b|\bthen\b", re.I)
_CONNECTOR = re.compile(r"^(?:\s|,|\bor\b|\bnor\b|\band\b)*$", re.I)


def _phrases(rule: str) -> list[tuple[str, str]]:
    """(kind, phrase) for every quoted phrase and {PLACEHOLDER} of a rule, in order.

    Each phrase reads the words just before it, back to the last clause break:
    "keeps 'Hi' and does not say 'urgent'" contains Hi and excludes urgent.  A
    phrase with only "or"/"and"/commas before it shares the previous one's kind,
    so "no 'urgent', 'act now' or 'hurry'" excludes all three."""
    quoted = [(m.start(), m.end(), m.group(1)) for m in _QUOTED.finditer(rule)]
    spans = quoted + [(m.start(), m.end(), m.group(0)) for m in _PLACEHOLDER.finditer(rule)
                      if not any(a <= m.start() < b for a, b, _ in quoted)]
    out, prev_end, prev_kind = [], 0, None
    for start, end, phrase in sorted(spans):
        before = rule[prev_end:start]
        part = _CLAUSE.split(before)[-1]
        if prev_kind and _CONNECTOR.match(before):
            kind = prev_kind
        else:
            words = part if part.strip() else before
            kind = ("excludes" if _NEGATIVE.search(words) else "ends_with" if _ENDS.search(words)
                    else "starts_with" if _STARTS.search(words) else "contains")
        out.append((kind, phrase))
        prev_end, prev_kind = end, kind
    return out


def compile_criteria(acceptance: list[str]) -> list[dict]:
    """Turn acceptance prose into v2 criteria; anything not mechanical is semantic.

    Rule N compiles to criterion ``rNN``; a rule quoting several phrases adds
    ``rNNb``, ``rNNc`` for the rest, so "no 'urgent' or 'act now'" excludes both.
    A negative word (no, not, does not, never, without, avoid) before a quoted
    phrase or a {PLACEHOLDER} makes it ``excludes``; "ends with 'X'" is
    ``ends_with``; "under N characters" allows N - 1.
    """
    criteria = []
    for index, rule in enumerate(acceptance, start=1):
        cid = f"r{index:02d}"
        rubric_kind = None
        lowered = rule.casefold()
        for label in ("semantic", "visual"):
            if lowered.startswith(label + ":"):
                rubric_kind = label
                break
        if rubric_kind:
            fields = {}
            for part in rule.split("|"):
                key, sep, value = part.partition(":")
                if not sep or not value.strip():
                    raise ValueError(
                        f"{rubric_kind} criterion {cid} needs criterion, observe, pass, fail, "
                        "and not-verifiable fields separated by |"
                    )
                key = key.strip().casefold()
                if key in fields:
                    raise ValueError(f"{rubric_kind} criterion {cid} repeats {key}")
                fields[key] = value.strip()
            required = {rubric_kind, "observe", "pass", "fail", "not-verifiable"}
            if set(fields) != required:
                missing = ", ".join(sorted(required - set(fields))) or ""
                extra = ", ".join(sorted(set(fields) - required))
                detail = f"missing {missing}" if missing else f"unknown fields {extra}"
                raise ValueError(f"{rubric_kind} criterion {cid} has {detail}")
            criteria.append({
                "id": cid, "kind": rubric_kind, "description": fields[rubric_kind],
                "observation": fields["observe"], "pass_when": fields["pass"],
                "fail_when": fields["fail"],
                "not_verifiable_when": fields["not-verifiable"],
            })
            continue
        hit = _MAX_CHARS.search(rule)
        if hit:
            limit = int(hit.group(2))
            criteria.append({"id": cid, "kind": "max_chars",
                             "value": limit - 1 if hit.group(1).lower() in _STRICT else limit})
            continue
        hit = _MAX_CHARS_2.search(rule)
        if hit:
            criteria.append({"id": cid, "kind": "max_chars", "value": int(hit.group(1))})
            continue
        phrases = _phrases(rule)
        if phrases:
            for n, (kind, phrase) in enumerate(phrases):
                criteria.append({"id": cid + ("" if n == 0 else chr(ord("a") + n)), "kind": kind, "value": phrase})
        else:
            # A rule no built-in check can compute is judged by a reader. The
            # person writes it as a plain sentence; the method is derived from
            # it, so nothing has to be re-typed. Spelling the method out
            # (`semantic: … | observe: …`) stays available and wins.
            criteria.append(_judged_criterion(cid, rule))
    return criteria


def _judged_criterion(cid: str, rule: str) -> dict:
    """A plain acceptance sentence as a judged criterion with its method named."""
    visual = bool(_RENDER.search(rule))
    return {
        "id": cid, "kind": "visual" if visual else "semantic", "description": rule,
        "observation": ("Look at the rendered screen of this draft and judge the rule as written."
                        if visual else
                        "Read this draft as its recipient and judge the rule as written."),
        "pass_when": f"The draft does what the rule says: {rule}",
        "fail_when": f"The draft does not do what the rule says: {rule}",
        "not_verifiable_when": ("The render is missing or does not show what the rule names."
                                if visual else
                                "The draft does not show enough to judge the rule either way."),
    }


def split_evidence(line: str) -> tuple[str, str]:
    """One register evidence line, `role · path` or `role  path`, as (role, path).

    The path is relative to the Design Folder (the folder holding `<stem>.md`).
    An unknown role word reads as `evidence`."""
    parts = [p.strip() for p in re.split(r"\s*·\s*|\s{2,}", line.strip(), maxsplit=1)]
    role, ref = (parts[0], parts[1]) if len(parts) == 2 else ("evidence", parts[0])
    return (role if role in ROLES else "evidence"), ref


def _evidence_inputs(folder: Path, evidence: list[str]) -> tuple[list[dict], list[str]]:
    """Resolve register evidence lines (`role · path`) into hashed Ticket inputs."""
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
    runs = item.get("runs") or []
    released = _latest(runs, "commission", outcome="release")
    if released is not None:
        raise ActionError(f"{item['id']} was already released in {released['id']}; at most one released Commission per item")
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
    run = f"rd{number:02d}_generate_{_slug(item['id'])}"
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
        note = folder / "outline" / "feedback" / f"{run}.md"
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
    run = f"rd{number:02d}_verify_{_slug(item['id'])}"
    config_path, evidence = _frozen(folder, stem, item, released, run, "independent")
    approval = folder / "results" / released["id"] / "decision.yaml"
    target = _ref(folder, generated["result_dir"] / "result.yaml")
    # The reviewer reads the same evidence the bet rests on; an
    # evidence-informed Ticket with no evidence input fails the gate.
    inputs, missing = _evidence_inputs(folder, evidence)
    if missing:
        raise ActionError("evidence named at release is gone: " + ", ".join(missing))
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
    ``complete`` with the next route when the gate accepts a complete judgment
    (pass, fail, or unresolved), ``failed`` with the gate's own words when the
    record is malformed. It never edits the Result.
    """
    import importlib.util
    checker = Path(__file__).resolve().parents[3] / "design" / "haipipe-design-unit" / "scripts" / "check_unit.py"
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


def adopt(folder: Path, stem: str, item: dict, runs: list[dict], decision: str,
          actor: str, words: str) -> dict:
    """Retired write entry; historical records remain readable by the presenter."""
    raise ActionError("Adopt writes are retired; independent Verify pass is ready for Delivery")


# ------------------------------------------------------------ stale queue --

def stale_inputs(folder: Path, run: str) -> list[str]:
    """The files a queued run pinned that changed (or vanished) since it was queued."""
    ticket = _load(folder / "runs" / f"{run}.yaml")
    refs = [ticket.get("config"), (ticket.get("approval") or {}).get("record")]
    refs += list(ticket.get("inputs") or []) + list(ticket.get("targets") or [])
    changed = []
    for ref in refs:
        if isinstance(ref, dict) and ref.get("path"):
            path = (folder / str(ref["path"])).resolve()
            if not path.is_file() or _digest(path) != ref.get("sha256"):
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


def requeue(folder: Path, stem: str, item: dict, runs: list[dict]) -> dict:
    """Queue again: replace an item's out-of-date queued run with a fresh one that pins today's files.

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
        elif item["state"] in ("generated", "verify invalid"):
            runs.append(queue_verify(folder, stem, item, item["runs"])["run"])
        elif item["state"] == "queued run out of date":
            runs.append(requeue(folder, stem, item, item["runs"])["run"])
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
    """The DO / DO NOT counsel lines of an insight page, in order.  A rule that
    wraps goes on at the column its DO started in; only that column is read,
    so a side column's own wrap is not glued on (FW01's W3 used to end "on the")."""
    rows, col = [], None
    for line in text.splitlines():
        hit = _COUNSEL.match(line)
        if hit:
            rows.append({"id": hit.group(1), "do": hit.group(2) == "DO", "text": hit.group(3).strip()})
            col = hit.start(2)
        elif col and not line[:col].strip() and line[col:col + 1].strip():
            rows[-1]["text"] += " " + re.split(r"\s{2,}", line[col:].strip())[0]
        else:
            col = None
    for row in rows:
        row["text"] = row["text"].rstrip(".")
    return rows


def counsel_rules(text: str) -> list[str]:
    """Acceptance rules implied by the counsel: every DO NOT becomes a 'does not …' rule.

    Quote the phrase to ban ("does not say 'urgent'") and it compiles to an
    ``excludes`` check; left unquoted, the reviewer judges it (semantic)."""
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
