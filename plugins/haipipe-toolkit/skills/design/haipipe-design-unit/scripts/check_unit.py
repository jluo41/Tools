#!/usr/bin/env python3
"""Read-only Design Ticket/Result gate. Requires PyYAML; never generates content."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import yaml

RUN = re.compile(r"rd[0-9]{2,}_(generate|verify)_[a-z0-9][a-z0-9_-]*")
# Commission is the current human decision Run; Adopt is legacy audit only.
# The worker never produces them, so the folder audit checks only their
# Ticket/Result pairing and a recorded decision, never worker semantics.
DECISION_RUN = re.compile(r"rd[0-9]{2,}_(commission|adopt)_[a-z0-9][a-z0-9_-]*")
HASH = re.compile(r"[0-9a-f]{64}")
ROLES = {"evidence", "inspiration", "reference", "avoid", "base", "feedback", "handoff"}
KINDS = {"max_chars", "contains", "excludes", "starts_with", "ends_with", "semantic", "visual"}
UNRESOLVED_REASONS = {
    "missing_context", "criterion_ambiguous", "criterion_conflict", "inspection_limit"
}
TEXT_KINDS = {"contains", "excludes", "starts_with", "ends_with"}
TICKET_SCHEMA = "haipipe.design-ticket/v2"
RESULT_SCHEMA = "haipipe.design-result/v2"
STANCES = {"follow", "challenge", "explore", "generate"}


class ContractError(ValueError):
    pass


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    pairs = loader.construct_pairs(node, deep=deep)
    result = {}
    for key, value in pairs:
        if key in result:
            raise ContractError("duplicate YAML key")
        result[key] = value
    return result


UniqueLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def need(condition, message):
    if not condition:
        raise ContractError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def document(path):
    value = yaml.load(Path(path).read_text(encoding="utf-8"), Loader=UniqueLoader)
    need(isinstance(value, dict), f"{path}: expected a mapping")
    return value


def string(value, name):
    need(isinstance(value, str) and bool(value.strip()), f"{name}: nonempty string required")
    return value


def optional_string(value, name):
    need(value is None or (isinstance(value, str) and bool(value.strip())),
         f"{name}: null or nonempty string required")
    return value


def design_intent(config):
    """Validate the frozen design bet without treating it as evidence."""
    intent = config.get("design_intent")
    need(isinstance(intent, dict), "config.design_intent: mapping required")
    required = {"move", "basis", "stance", "expected_effect", "failure_condition"}
    need(required <= set(intent), "config.design_intent: all v2 fields required")
    string(intent.get("move"), "design_intent.move")
    need(intent.get("basis") == config.get("basis"),
         "design_intent.basis must match config.basis")
    stance = intent.get("stance")
    need(stance in STANCES, "unknown design_intent stance")
    expected = optional_string(intent.get("expected_effect"),
                               "design_intent.expected_effect")
    failure = optional_string(intent.get("failure_condition"),
                              "design_intent.failure_condition")
    mode = config.get("mode")
    if stance == "challenge":
        need(mode == "challenge", "challenge stance requires challenge mode")
    if mode == "challenge":
        need(stance == "challenge", "challenge mode requires challenge stance")
        need(expected is not None and failure is not None,
             "challenge requires an alternative effect and distinguishing condition")
    if mode == "brainstorm":
        need(stance in {"explore", "generate"},
             "brainstorm stance must explore or generate")
        need(expected is None and failure is None,
             "brainstorm cannot smuggle in a forecast")
    if mode == "theory-driven":
        need(expected is not None and failure is not None,
             "theory-driven intent requires expected effect and failure condition")


def inside(path, root):
    return path == root or root in path.parents


def resolve(root, value, bounded=False):
    value = string(value, "path")
    path = (root / value).resolve()
    if bounded:
        need(not Path(value).is_absolute() and ".." not in Path(value).parts
             and inside(path, root.resolve()), "output path escapes Result directory")
    return path


def reference(root, ref, bounded=False):
    need(isinstance(ref, dict), "file reference must be a mapping")
    path = resolve(root, ref.get("path"), bounded)
    sha = ref.get("sha256")
    need(isinstance(sha, str) and bool(HASH.fullmatch(sha)), "invalid SHA-256")
    shown = _shown(path, root)
    need(path.is_file(), f"missing input/artifact: {shown}")
    need(digest(path) == sha, f"hash mismatch: {shown} changed after it was pinned")
    return path


def _shown(path, root):
    """A path as a reader finds it: relative to the folder being checked, never absolute."""
    import os
    try:
        return os.path.relpath(path, Path(root).resolve())
    except ValueError:
        return path.name


def artifact_records(folder, records):
    need(isinstance(records, list) and records, "a Generate Result requires content artifacts")
    seen = set()
    out = []
    for ref in records:
        path = reference(folder, ref, bounded=True)
        need(ref["path"].startswith("content/"), "a Generate Result artifact must live in content/")
        need(path not in seen, "duplicate content artifact")
        seen.add(path)
        out.append((ref["path"], path))
    return out


def render_records(output, manifest, subjects, item=None):
    """Validate optional render evidence without counting pictures as content.

    subjects maps resolved source artifact paths to their Generate Run ids.
    Returned picture paths are bounded by this Result's render directory.
    """
    if "render_manifest" not in manifest:
        return []
    root = output.resolve() / "render"
    path = reference(output, manifest["render_manifest"], bounded=True)
    need(inside(path, root), "render manifest must live in Result render/")
    rows = json.loads(path.read_text(encoding="utf-8"))
    need(isinstance(rows, list) and rows, "render manifest requires a nonempty list")
    seen = set()
    checked = []
    for row in rows:
        need(isinstance(row, dict), "render entry must be a mapping")
        string(row.get("item"), "render.item")
        need(not item or row["item"] == item, "render item mismatch")
        need(type(row.get("version")) is int and row["version"] > 0,
             "render version must be a positive integer")
        source = reference(path.parent, {"path": row.get("source"), "sha256": row.get("sha256")})
        need(source in subjects and subjects[source] == row.get("candidate"),
             "render source/candidate is not a pinned content artifact")
        picture = reference(path.parent, {"path": row.get("render"), "sha256": row.get("render_sha256")}, bounded=True)
        need(inside(picture, root), "picture must live in Result render/")
        key = (row["candidate"], source, row["version"])
        need(key not in seen, "duplicate render version for source")
        seen.add(key)
        checked.append({**row, "path": picture})
    return checked


def context(ticket, historical=False):
    """Read and check one Ticket.  ``historical`` reads a closed run: an input that
    lives outside the Design Folder (an Insight page, still being edited) is
    history the run already consumed, so its later edits do not void the run.
    Everything inside the folder (config, approval, targets, artifacts) stays exact."""
    ticket = Path(ticket).resolve()
    need(ticket.parent.name == "runs" and ticket.suffix == ".yaml",
         "Ticket must be owner/runs/<run>.yaml")
    data = document(ticket)
    schema = data.get("schema")
    need(schema == TICKET_SCHEMA, "unsupported Ticket schema")
    match = RUN.fullmatch(ticket.stem)
    need(match is not None, "invalid Design Run stem")
    need(data.get("run") == ticket.stem, "Ticket identity mismatch")
    op = data.get("operation")
    need(op == match.group(1), "operation does not match Ticket stem")
    need(data.get("worker") == "haipipe-design-unit", "unexpected worker")
    string(data.get("actor"), "actor")
    string(data.get("target"), "target")
    owner = ticket.parent.parent
    output = owner / "results" / ticket.stem
    need(output.resolve() == output, "Result address cannot be redirected by a symlink")
    config_path = reference(owner, data.get("config"))
    need(not inside(config_path, output), "config cannot be inside the output")
    config = document(config_path)
    string(config.get("goal"), "config.goal")
    string(config.get("kind"), "config.kind")
    need(config.get("mode") in {"compose", "revise", "brainstorm", "theory-driven", "challenge"},
         "unknown design mode")
    need(config.get("basis") in {"brief-only", "evidence-informed"}, "unknown evidence basis")
    design_intent(config)
    need(config.get("review_mode") in {"self", "independent"}, "unknown review mode")
    if op == "generate":
        need(config["review_mode"] == "self", "generation cannot certify independent review")
    iterations = config.get("max_iterations")
    need(type(iterations) is int and iterations > 0, "positive max_iterations required")
    unit = config.get("unit", {})
    need(isinstance(unit, dict) and unit.get("shape") in {"single", "sequence", "set"},
         "invalid unit shape")
    need(type(unit.get("count")) is int and unit["count"] > 0, "positive unit count required")
    need(unit["shape"] != "single" or unit["count"] == 1, "single unit count must be 1")
    criteria = config.get("criteria")
    need(isinstance(criteria, list) and criteria, "nonempty criteria required")
    ids = set()
    for criterion in criteria:
        need(isinstance(criterion, dict), "criterion must be a mapping")
        cid = string(criterion.get("id"), "criterion.id")
        need(cid not in ids, "duplicate criterion id")
        ids.add(cid)
        kind = criterion.get("kind")
        need(kind in KINDS, "unsupported criterion kind")
        if kind == "max_chars":
            need(type(criterion.get("value")) is int and criterion["value"] >= 0,
                 "max_chars requires a nonnegative integer")
        elif kind in TEXT_KINDS:
            string(criterion.get("value"), "criterion.value")
        elif kind in {"semantic", "visual"}:
            string(criterion.get("description"), "criterion.description")
            for key in ("observation", "pass_when", "fail_when", "not_verifiable_when"):
                string(criterion.get(key), f"criterion.{key}")
    approval = data.get("approval", {})
    need(isinstance(approval, dict), "approval must be a mapping")
    string(approval.get("actor"), "approval.actor")
    approved_path = reference(owner, approval.get("record"))
    need(not inside(approved_path, output), "approval cannot be a generated output")
    inputs = data.get("inputs")
    need(isinstance(inputs, list), "inputs must be an explicit list")
    roles = set()
    for item in inputs:
        need(isinstance(item, dict) and item.get("role") in ROLES, "invalid input role")
        roles.add(item["role"])
        if historical and not inside(resolve(owner, item.get("path")), owner.resolve()):
            continue
        path = reference(owner, item)
        need(not inside(path, output), "input/output overlap")
        if "run_id" in item:
            run_id = string(item["run_id"], "upstream run_id")
            need(not run_id.startswith("rp") or item["role"] == "feedback",
                 "Page Run can enter a Design Ticket only as frozen feedback")
    if config["mode"] == "revise":
        need({"base", "feedback"} <= roles, "revise requires base and feedback")
    if config["basis"] == "evidence-informed":
        need(bool(roles & {"evidence", "handoff"}), "evidence-informed has no evidence")
    targets = data.get("targets")
    need(isinstance(targets, list), "targets must be an explicit list")
    need(bool(targets) == (op == "verify"), "only verify requires target Generate Results")
    subjects = []
    producers = set()
    seen_targets = set()
    for target in targets:
        path = reference(owner, target)
        need(path.name == "result.yaml", "target must name a Generate result.yaml")
        need(path not in seen_targets, "duplicate verification target")
        seen_targets.add(path)
        need(not inside(output, path.parent) and not inside(path.parent, output),
             "verification output overlaps target")
        manifest = document(path)
        need(manifest.get("schema") == RESULT_SCHEMA
             and manifest.get("operation") == "generate", "target is not a Generate Result")
        target_run = string(manifest.get("run"), "target.run")
        target_match = RUN.fullmatch(target_run)
        need(target_match is not None and target_match.group(1) == "generate"
             and path.parent.name == target_run, "target Run/Result identity mismatch")
        producer = string(manifest.get("producer"), "target.producer")
        producers.add(producer)
        runtime = document(path.parent / "runtime.yaml")
        need(runtime.get("status") == "complete" and runtime.get("run") == manifest.get("run"),
             "target generation is not complete")
        target_artifacts = artifact_records(path.parent, manifest.get("artifacts"))
        render_records(path.parent, manifest,
                       {artifact: target_run for _, artifact in target_artifacts}, data.get("item"))
        for rel, artifact in target_artifacts:
            subjects.append((target["path"] + "::" + rel, artifact))
    if config["review_mode"] == "independent":
        need(data["actor"] not in producers, "independent reviewer equals producer")
    return ticket, data, owner, output, config, subjects


def validate(ticket, result=None, historical=False):
    """Return diagnostic strings. No mutation, dispatch, or authority promotion."""
    try:
        ticket, data, owner, output, config, subjects = context(ticket, historical)
        if result is None:
            return []
        result = Path(result).resolve()
        need(result == output / "result.yaml", "Result address does not pair with Ticket")
        manifest = document(result)
        need(manifest.get("schema") == RESULT_SCHEMA,
             "Result schema does not match Ticket schema")
        for key in ("run", "operation", "target"):
            need(manifest.get(key) == data[key], f"Result {key} mismatch")
        need(manifest.get("producer") == data["actor"], "Result producer mismatch")
        need(manifest.get("ticket_sha256") == digest(ticket), "Result Ticket hash mismatch")
        need(manifest.get("config_sha256") == data["config"]["sha256"],
             "Result config hash mismatch")
        need(manifest.get("targets") == data["targets"], "Result target refs mismatch")
        if data["operation"] == "generate":
            subjects = artifact_records(output, manifest.get("artifacts"))
            need(len(subjects) == config["unit"]["count"], "Generate artifact count mismatch")
        else:
            need(manifest.get("artifacts") == [], "verify must not produce replacement artifacts")
        render_records(output, manifest, {
            path: (data["run"] if data["operation"] == "generate"
                   else Path(target.split("::", 1)[0]).parent.name)
            for target, path in subjects
        }, data.get("item"))
        checks_path = reference(output, manifest.get("checks"), bounded=True)
        checks = document(checks_path).get("checks")
        need(isinstance(checks, list), "checks must be a list")
        expected = {(target, c["id"]) for target, _ in subjects for c in config["criteria"]}
        indexed = {}
        for check in checks:
            need(isinstance(check, dict), "check must be a mapping")
            pair = (check.get("target"), check.get("criterion"))
            need(pair in expected and pair not in indexed, "extra or duplicate check pair")
            need(check.get("status") in {"pass", "fail", "unresolved"}, "invalid check status")
            string(check.get("evidence"), "check.evidence")
            if check.get("status") == "unresolved":
                need(check.get("unresolved_reason") in UNRESOLVED_REASONS,
                     "unresolved check needs a valid unresolved_reason")
                string(check.get("next_owner"), "unresolved check.next_owner")
                string(check.get("needed"), "unresolved check.needed")
            indexed[pair] = check
        need(set(indexed) == expected, "missing required check pairs")
        for target, path in subjects:
            for criterion in config["criteria"]:
                kind = criterion["kind"]
                if kind in {"semantic", "visual"}:
                    continue
                content = path.read_text(encoding="utf-8")
                value = criterion["value"]
                passed = (len(content) <= value if kind == "max_chars"
                          else value in content if kind == "contains"
                          else content.lstrip().startswith(value) if kind == "starts_with"
                          else content.rstrip().endswith(value) if kind == "ends_with"
                          else value not in content)
                need(indexed[(target, criterion["id"])]["status"] == ("pass" if passed else "fail"),
                     f"check disagrees with actual artifact: {target}/{criterion['id']}")
        statuses = {item["status"] for item in checks}
        verdict = ("unresolved" if "unresolved" in statuses else
                   "fail" if "fail" in statuses else "pass")
        need(manifest.get("verdict") == verdict, "verdict disagrees with checks")
        if data["operation"] == "generate":
            need(verdict == "pass", "Generate requires every criterion to pass; resolve an unknown criterion before commissioning")
        return []
    except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError) as exc:
        return [str(exc)]


def decision_run(folder, ticket):
    """Pair current Commission or historical Adopt records without authorizing writes."""
    try:
        data = document(ticket)
        need(data.get("schema") == TICKET_SCHEMA, "unsupported Ticket schema")
        need(data.get("run") == ticket.stem, "Ticket identity mismatch")
        op = DECISION_RUN.fullmatch(ticket.stem).group(1)
        need(data.get("operation") == op, "operation does not match Ticket stem")
        output = folder / "results" / ticket.stem
        runtime = document(output / "runtime.yaml")
        need(runtime.get("run") == ticket.stem, "runtime run mismatch")
        status = runtime.get("status")
        need(status in {"planned", "running", "complete", "failed", "blocked", "superseded"},
             "unknown runtime status")
        if status == "complete":
            decision = document(output / "decision.yaml")
            need(decision.get("run") == ticket.stem, "decision run mismatch")
            string(decision.get("decision"), "decision.decision")
            string(decision.get("actor"), "decision.actor")
            need(bool(runtime.get("finished_at")), "runtime missing finished_at")
        return []
    except (OSError, ValueError, TypeError, KeyError, AttributeError, yaml.YAMLError) as exc:
        return [str(exc)]


def audit_folder(folder):
    """Audit only allocated native Design YAML Tickets and their runtime pairs."""
    folder = Path(folder)
    issues = []
    retired_tickets = sorted((folder / "runs").glob("r*_design_*.yaml"))
    for ticket in retired_tickets:
        issues.append(f"{ticket}: retired Design Run identity is unsupported")
    tickets = sorted((folder / "runs").glob("rd*_*.yaml"))
    for ticket in tickets:
        if DECISION_RUN.fullmatch(ticket.stem):
            issues.extend(f"{ticket}: {p}" for p in decision_run(folder, ticket))
            continue
        output = folder / "results" / ticket.stem
        try:
            runtime = document(output / "runtime.yaml")
        except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError):
            runtime = {}
        if runtime.get("status") == "superseded":
            # A queued run replaced before any worker touched it (an input changed after
            # it was queued): its pins are stale by definition; only its reason is checked.
            if not runtime.get("failure") or (output / "result.yaml").is_file():
                issues.append(f"{ticket}: a superseded run needs a reason and no result")
            continue
        # an open run must still match its pins; a closed one is read as history
        closed = runtime.get("status") in {"complete", "failed", "blocked"}
        for problem in validate(ticket, historical=closed):
            issues.append(f"{ticket}: {problem}")
        try:
            data = document(ticket)
            runtime = document(output / "runtime.yaml")
            for key, expected in {"run": ticket.stem, "family": "design",
                                  "operation": data.get("operation"),
                                  "target": data.get("target"),
                                  "ticket_sha256": digest(ticket),
                                  "ticket": f"runs/{ticket.name}",
                                  "result": f"results/{ticket.stem}/"}.items():
                need(runtime.get(key) == expected, f"runtime {key} mismatch")
            worker = runtime.get("worker", {})
            need(isinstance(worker, dict) and worker.get("kind") == "skill"
                 and worker.get("name") == "haipipe-design-unit"
                 and worker.get("actor") == data.get("actor"),
                 "runtime worker identity mismatch")
            bound = runtime.get("inputs")
            need(isinstance(bound, list), "runtime missing input manifest")
            expected_inputs = [data["config"], data["approval"]["record"]]
            expected_inputs += data.get("inputs", []) + data.get("targets", [])
            actual = {(r["path"], r["sha256"]) for r in bound}
            need(all((r["path"], r["sha256"]) in actual for r in expected_inputs),
                 "runtime input manifest is incomplete")
            status = runtime.get("status")
            need(status in {"planned", "running", "complete", "failed", "blocked", "superseded"},
                 "unknown runtime status")
            if status in {"running", "complete", "failed", "blocked"}:
                need(bool(runtime.get("started_at")), "runtime missing started_at")
            if status in {"complete", "failed", "blocked"}:
                need(bool(runtime.get("finished_at")), "runtime missing finished_at")
            if status in {"failed", "blocked"}:
                need(bool(runtime.get("failure")), "non-success requires a reason")
            if status == "complete":
                issues.extend(f"{ticket}: {p}" for p in validate(ticket, output / "result.yaml", historical=True))
        except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError) as exc:
            issues.append(f"{ticket}: {exc}")
    for output in sorted((folder / "results").glob("rd*_*")):
        if output.is_dir() and not (folder / "runs" / (output.name + ".yaml")).is_file():
            issues.append(f"{output}: orphan Result without Ticket")
    for output in sorted((folder / "results").glob("r*_design_*")):
        if output.is_dir():
            issues.append(f"{output}: retired Design Result identity is unsupported")
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticket", type=Path)
    parser.add_argument("--result", type=Path)
    parser.add_argument("--folder", type=Path)
    args = parser.parse_args()
    if bool(args.ticket) == bool(args.folder) or (args.result and not args.ticket):
        parser.error("choose --ticket [--result] or --folder")
    problems = audit_folder(args.folder) if args.folder else validate(args.ticket, args.result)
    for problem in problems:
        print("FAIL:", problem)
    if not problems:
        print("PASS: " + ("Run inventory" if args.folder else
                         "Result integrity and check coverage" if args.result else "Ticket inputs"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
