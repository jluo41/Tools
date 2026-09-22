"""Read selected Insight work from frozen definitions; never allocate a Run."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


# Reader labels and surface placement for the Insight controller's own Spec
# templates. Canonical Run Types and workers always come from owner records.
_TEMPLATES = {
    "support": ("Produce the missing source result", "evidence"),
    "evidence": ("Prepare one evidence item", "evidence"),
    "structure": ("Plan the selected Page", "insight"),
    "write": ("Write the selected section or paragraphs", "insight"),
    "deliver": ("Build the selected deliverable", "delivery"),
}
_TERMINAL = {"complete", "completed", "accepted", "passed", "closed", "cancelled", "canceled"}
_OPEN = {"planned", "running", "held", "blocked"}


def describe(value) -> str:
    if value in (None, "", [], {}):
        return "not recorded"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    return str(value)


def people(record: dict) -> tuple[str, str]:
    worker = next((record[key] for key in ("worker_skills", "workers", "worker_skill", "worker")
                   if record.get(key)), None)
    return describe(worker), describe(record.get("actor"))


def reader_name(spec: dict) -> str:
    family = str(spec.get("id", spec.get("run_spec_id", ""))).split(".", 1)[0]
    return str(spec.get("name") or spec.get("label") or _TEMPLATES.get(family, ("Native Run", ""))[0])


def definition(board: Path, runtime: dict) -> dict:
    """Read only the frozen definition selected and hashed by this Runtime."""
    import yaml
    directory = (board / runtime["path"]).parent.resolve()
    ref = runtime.get("definition")
    if not isinstance(ref, str) or not ref or ref == "not recorded":
        raise ValueError("frozen definition path is not recorded")
    path = (directory / ref).resolve()
    if not path.is_relative_to(directory):
        raise ValueError("frozen definition must remain inside its Runtime directory")
    body = path.read_bytes()
    if hashlib.sha256(body).hexdigest() != runtime.get("definition_hash"):
        raise ValueError("frozen definition hash is missing or differs from its recorded hash")
    data = yaml.safe_load(body)
    if not isinstance(data, dict) or data.get("schema") != "haipipe.insight-definition/v1" \
            or data.get("workflow_id") != "haipipe-insight-workflow":
        raise ValueError("unsupported Insight definition")
    specs, targets = data.get("run_specs"), data.get("requested_answer_targets")
    if not isinstance(specs, list) or not isinstance(targets, list):
        raise ValueError("definition must list run_specs and requested_answer_targets")
    if any(not isinstance(target, dict) for target in targets):
        raise ValueError("definition answer targets must be records")
    ids = [s.get("id") for s in specs if isinstance(s, dict)]
    if len(ids) != len(specs) or any(not isinstance(i, str) or not i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("definition has missing or duplicate Spec identities")
    return data


def _cell(record, question: str, partition: str) -> bool:
    return isinstance(record, dict) and record.get("question") == question and record.get("partition") == partition


def _page_path(board: Path, value) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        return None
    return (board / value).resolve()


def selected_specs(snap: dict, question: str, partition: str, page: dict | None = None) -> dict:
    """Select owed Specs, including dependencies, using explicit cell bindings.

    A Folder/rung or an open Queue mark alone never commissions executable work.
    Missing bindings are reported for the controller to resolve through chain.
    """
    projection = {"items": [], "notes": [], "question": question, "partition": partition}
    row = next((q for q in snap["questions"] if q["id"] == question), None)
    if not row or partition not in row["cells"]:
        projection["notes"].append("Select a registered question and partition to see its owed Run Specs.")
        return projection
    cell = row["cells"][partition]
    if cell["mark"] in {"·", "🚫", "✅"} or (cell["mark"] == "🟡" and "final" in cell.get("note", "")):
        projection["notes"].append("This cell has no open answering target. Recorded Runs remain in the read-only inventory.")
        return projection
    board = Path(snap["board"])
    for runtime in snap.get("workflow_runtimes", []):
        if runtime.get("error"):
            projection["notes"].append(f'{runtime["id"]}: {runtime["error"]}')
            continue
        if runtime.get("status") not in _OPEN:
            continue
        try:
            data = definition(board, runtime)
        except Exception as exc:
            # Definition parsing cannot grant a fallback set of executable types.
            projection["notes"].append(f'{runtime["id"]}: cannot select work: {exc}')
            continue
        targets = data["requested_answer_targets"]
        selected_targets = [t for t in targets if _cell(t, question, partition)]
        if not selected_targets:
            continue
        specs = {s["id"]: s for s in data["run_specs"]}
        runs = runtime["runs"]
        page_paths = {_page_path(board, t.get("page")) for t in selected_targets}
        answer = snap["by_id"].get(cell.get("page", ""))
        if answer:
            page_paths.add(answer["path"].resolve())
        page_paths.discard(None)
        chosen = set()
        for sid, spec in specs.items():
            target = spec.get("target", {})
            bindings = spec.get("consumers", [])
            bindings = bindings if isinstance(bindings, list) else []
            bindings = bindings + [target] + [c for run in runs if run.get("run_spec_id") == sid
                                               for c in (run.get("consumers") if isinstance(run.get("consumers"), list) else [])
                                               if isinstance(c, dict)]
            explicit = [b for b in bindings if isinstance(b, dict) and (b.get("question") or b.get("partition"))]
            if any(_cell(b, question, partition) for b in explicit):
                chosen.add(sid)
            elif explicit:
                continue  # An explicit different/partial cell binding cannot fall back to a shared Page.
            elif isinstance(target, dict) and _page_path(board, target.get("page")) in page_paths:
                chosen.add(sid)
            elif len(targets) == 1:
                # A single-target definition scopes all its bounded Specs to
                # that one cell; multi-target definitions need an exact join.
                chosen.add(sid)
        run_to_spec = {r["run_id"]: r.get("run_spec_id") for r in runs}
        pending = list(chosen)
        while pending:
            deps = specs[pending.pop()].get("depends_on", [])
            for dep in deps if isinstance(deps, list) else []:
                if not isinstance(dep, str):
                    continue
                sid = dep if dep in specs else run_to_spec.get(dep)
                if sid in specs and sid not in chosen:
                    chosen.add(sid)
                    pending.append(sid)
        if not chosen and specs:
            projection["notes"].append(f'{runtime["id"]}: no exact Spec-to-cell binding; the workflow owner must resolve it.')
        for sid, spec in specs.items():
            if sid not in chosen:
                continue
            family = sid.split(".", 1)[0]
            if family not in _TEMPLATES:
                projection["notes"].append(f'{runtime["id"]}: {sid} has no Insight surface mapping; Not built.')
                continue
            target = spec.get("target")
            if page is not None and (not isinstance(target, dict) or
                                    _page_path(board, target.get("page")) != page["path"].resolve()):
                continue
            matches = [r for r in runs if r.get("run_spec_id") == sid]
            frontier = [f for f in runtime["frontier"] if f.get("run_spec_id") == sid]
            if matches and all(r["status"] in _TERMINAL for r in matches):
                continue
            if frontier and all(f.get("state") in _TERMINAL for f in frontier):
                continue
            if any(spec.get(key) and run.get(key) and spec[key] != run[key]
                   for run in matches for key in ("owner", "run_type")):
                projection["notes"].append(f'{runtime["id"]}: {sid} owner/Run Type conflicts with its native inventory; reconcile it before dispatch.')
                continue
            meta = dict(spec)
            for key in ("run_type", "owner", "worker_skills", "workers", "worker_skill", "worker", "actor"):
                if not meta.get(key):
                    values = [r[key] for r in matches if r.get(key)]
                    if values and all(v == values[0] for v in values):
                        meta[key] = values[0]
            prerequisites = [f'Inputs: {describe(spec.get("inputs"))}',
                             f'Dependencies: {describe(spec.get("depends_on", []))}',
                             f'Owner entry requirements: {describe(spec.get("entry"))}']
            prerequisites.extend(f'Waiting on: {describe(f.get("waiting_on"))}' for f in frontier if f.get("waiting_on"))
            for dep in spec.get("depends_on", []) if isinstance(spec.get("depends_on", []), list) else []:
                linked = [r for r in runs if r["run_id"] == dep or r.get("run_spec_id") == dep]
                prerequisites.append(f'{describe(dep)}: ' + (", ".join(f'{r["run_id"]} · {r["status"]}' for r in linked)
                                                           or "no native Run binding recorded"))
            missing = [key for key in ("run_type", "owner", "actor", "target") if not meta.get(key)]
            workers, actor = people(meta)
            if workers == "not recorded":
                missing.append("worker Skill(s)")
            if missing:
                prerequisites.append("Owner must resolve: " + ", ".join(missing))
            incomplete_reuse = any(r.get("participation") == "reused" and r["status"] not in _TERMINAL
                                   for r in matches)
            if incomplete_reuse:
                prerequisites.append("A reused Run is not recorded as complete; verify its accepted Result and native receipt.")
            next_action = ("Resolve the missing owner metadata and prerequisites; keep this target held."
                           if missing or incomplete_reuse else "Verify entry requirements and existing authorization, then "
                           + ("resume the matching native Run through its owner." if matches else
                              "let the owner allocate only this owed Spec if its entry requirements pass."))
            projection["items"].append({
                "spec": spec, "runtime": runtime, "name": reader_name(meta),
                "space": _TEMPLATES[family][1], "type": describe(meta.get("run_type")),
                "purpose": describe(spec.get("purpose") or (target.get("goal") if isinstance(target, dict) else target)
                                    or _TEMPLATES[family][0]),
                "owner": describe(meta.get("owner")), "workers": workers, "actor": actor,
                "target": describe(target), "prerequisites": prerequisites, "matches": matches,
                "state": ", ".join(str(f.get("state", "not recorded")) for f in frontier) or "entry needs owner check",
                "next_action": next_action,
            })
    if not projection["items"] and not projection["notes"]:
        projection["notes"].append("No owed Run Spec is recorded for this cell. Use chain to resolve the missing target and its prerequisites.")
    return projection


def request_text(snap: dict, projection: dict, item: dict | None = None) -> str:
    qid, pid = projection["question"], projection["partition"]
    row = next((q for q in snap["questions"] if q["id"] == qid), None)
    cell = row["cells"].get(pid, {}) if row else {}
    page = snap["by_id"].get(cell.get("page", ""))
    lines = [f'/haipipe-insight application {json.dumps(str(Path(snap["board"]).resolve()), ensure_ascii=False)} chain {qid} {pid}',
             "", f'Board: {Path(snap["board"]).resolve()}', f'Question: {qid} · {row["question"] if row else "not recorded"}',
             f'Partition: {pid}', f'Current cell: {cell.get("raw", "not recorded")}',
             f'Answer Page: {page["path"] if page else "not allocated or not recorded"}',
             "Workflow Skill: haipipe-insight-workflow; entry Skill: haipipe-insight."]
    if item:
        lines += [f'Workflow Runtime: {item["runtime"]["id"]}',
                  f'Frozen definition: {item["runtime"]["definition"]} · sha256 {item["runtime"].get("definition_hash", "not recorded")}',
                  f'Spec: {item["spec"]["id"]} · {item["name"]}', f'Canonical Run Type: {item["type"]}',
                  f'Bounded work: {item["purpose"]}', f'Target: {item["target"]}',
                  f'Owner Skill: {item["owner"]}', f'Worker Skill(s): {item["workers"]}', f'Actor: {item["actor"]}',
                  f'Workflow frontier state: {item["state"]}',
                  "Prerequisites:", *["- " + p for p in item["prerequisites"]], "Existing matching Runs:"]
        lines += [f'- {r["run_id"]} · {r["status"]} · Ticket {r.get("ticket", "not recorded")} · receipt {r["receipt"]}'
                  for r in item["matches"]] or ["- No matching native allocation recorded; inspect the owner store before creating one."]
        lines += [f'Next permitted action: {item["next_action"]}',
                  "Keep this request bounded to the selected Spec and its declared dependencies."]
    else:
        lines += ["Next permitted action: inspect the existing frozen definition and native receipts; "
                  "resolve which bounded target is missing and which Specs are owed before allocating anything.",
                  *projection["notes"]]
    lines += ["Reuse exact accepted Results and resume compatible existing Runs. Recheck native receipts and current input pins.",
              "Preserve native owner rules, mode: copilot, existing scoped authorization, and all person-reserved gates. "
              "Missing release, input, acceptance or signature stays a named hold; copying this request grants none of them.",
              "Registration, Page passes, checks, GI decisions and signatures remain control actions without Run identities.",
              "Report the actual native Run id, current status, exact Result and receipt paths, and any blocker. "
              "If no Run is allocated or resumed, say so and name the missing prerequisite; do not invent an id or receipt."]
    return "\n".join(lines)
