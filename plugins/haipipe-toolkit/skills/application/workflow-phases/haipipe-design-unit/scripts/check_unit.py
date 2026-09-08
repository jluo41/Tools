#!/usr/bin/env python3
"""Read-only Design Ticket/Result gate. Requires PyYAML; never generates content."""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import re
import sys
import yaml

RUN = re.compile(r"r[0-9]{2,}_design_(generate|verify)_[a-z0-9][a-z0-9_-]*")
HASH = re.compile(r"[0-9a-f]{64}")
ROLES = {"evidence", "inspiration", "reference", "avoid", "base", "feedback", "handoff"}
KINDS = {"max_chars", "contains", "excludes", "semantic", "visual"}


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
    need(path.is_file(), f"missing input/artifact: {path}")
    need(digest(path) == sha, f"hash mismatch: {path}")
    return path


def artifact_records(folder, records):
    need(isinstance(records, list) and records, "DU requires content artifacts")
    seen = set()
    out = []
    for ref in records:
        path = reference(folder, ref, bounded=True)
        need(ref["path"].startswith("content/"), "DU artifact must live in content/")
        need(path not in seen, "duplicate content artifact")
        seen.add(path)
        out.append((ref["path"], path))
    return out


def context(ticket):
    ticket = Path(ticket).resolve()
    need(ticket.parent.name == "runs" and ticket.suffix == ".yaml",
         "Ticket must be owner/runs/<run>.yaml")
    data = document(ticket)
    need(data.get("schema") == "haipipe.design-ticket/v1", "unknown Ticket schema")
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
        elif kind in {"contains", "excludes"}:
            string(criterion.get("value"), "criterion.value")
        else:
            string(criterion.get("description"), "criterion.description")
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
        path = reference(owner, item)
        need(not inside(path, output), "input/output overlap")
        if "run_id" in item:
            string(item["run_id"], "upstream run_id")
    if config["mode"] == "revise":
        need({"base", "feedback"} <= roles, "revise requires base and feedback")
    if config["basis"] == "evidence-informed":
        need(bool(roles & {"evidence", "handoff"}), "evidence-informed has no evidence")
    targets = data.get("targets")
    need(isinstance(targets, list), "targets must be an explicit list")
    need(bool(targets) == (op == "verify"), "only verify requires target DU Results")
    subjects = []
    producers = set()
    seen_targets = set()
    for target in targets:
        path = reference(owner, target)
        need(path.name == "result.yaml", "target must name a DU result.yaml")
        need(path not in seen_targets, "duplicate verification target")
        seen_targets.add(path)
        need(not inside(output, path.parent) and not inside(path.parent, output),
             "verification output overlaps target")
        manifest = document(path)
        need(manifest.get("schema") == "haipipe.design-result/v1"
             and manifest.get("operation") == "generate", "target is not a DU Result")
        target_run = string(manifest.get("run"), "target.run")
        target_match = RUN.fullmatch(target_run)
        need(target_match is not None and target_match.group(1) == "generate"
             and path.parent.name == target_run, "target Run/Result identity mismatch")
        producer = string(manifest.get("producer"), "target.producer")
        producers.add(producer)
        runtime = document(path.parent / "runtime.yaml")
        need(runtime.get("status") == "complete" and runtime.get("run") == manifest.get("run"),
             "target generation is not complete")
        for rel, artifact in artifact_records(path.parent, manifest.get("artifacts")):
            subjects.append((target["path"] + "::" + rel, artifact))
    if config["review_mode"] == "independent":
        need(data["actor"] not in producers, "independent reviewer equals producer")
    return ticket, data, owner, output, config, subjects


def validate(ticket, result=None):
    """Return diagnostic strings. No mutation, dispatch, or authority promotion."""
    try:
        ticket, data, owner, output, config, subjects = context(ticket)
        if result is None:
            return []
        result = Path(result).resolve()
        need(result == output / "result.yaml", "Result address does not pair with Ticket")
        manifest = document(result)
        need(manifest.get("schema") == "haipipe.design-result/v1", "unknown Result schema")
        for key in ("run", "operation", "target"):
            need(manifest.get(key) == data[key], f"Result {key} mismatch")
        need(manifest.get("producer") == data["actor"], "Result producer mismatch")
        need(manifest.get("ticket_sha256") == digest(ticket), "Result Ticket hash mismatch")
        need(manifest.get("config_sha256") == data["config"]["sha256"],
             "Result config hash mismatch")
        need(manifest.get("targets") == data["targets"], "Result target refs mismatch")
        if data["operation"] == "generate":
            subjects = artifact_records(output, manifest.get("artifacts"))
            need(len(subjects) == config["unit"]["count"], "DU artifact count mismatch")
        else:
            need(manifest.get("artifacts") == [], "verify must not produce replacement artifacts")
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
                          else value not in content)
                need(indexed[(target, criterion["id"])]["status"] == ("pass" if passed else "fail"),
                     f"check disagrees with actual artifact: {target}/{criterion['id']}")
        statuses = {item["status"] for item in checks}
        verdict = ("unresolved" if "unresolved" in statuses else
                   "fail" if "fail" in statuses else "pass")
        need(manifest.get("verdict") == verdict, "verdict disagrees with checks")
        need(verdict != "unresolved", "required checks remain unresolved")
        if data["operation"] == "generate":
            need(verdict == "pass", "generated DU has failing criteria")
        return []
    except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError) as exc:
        return [str(exc)]


def audit_folder(folder):
    """Audit only allocated native Design YAML Tickets and their runtime pairs."""
    folder = Path(folder)
    issues = []
    tickets = sorted((folder / "runs").glob("r*_design_*.yaml"))
    for ticket in tickets:
        for problem in validate(ticket):
            issues.append(f"{ticket}: {problem}")
        output = folder / "results" / ticket.stem
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
                issues.extend(f"{ticket}: {p}" for p in validate(ticket, output / "result.yaml"))
        except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError) as exc:
            issues.append(f"{ticket}: {exc}")
    for output in sorted((folder / "results").glob("r*_design_*")):
        if output.is_dir() and not (folder / "runs" / (output.name + ".yaml")).is_file():
            issues.append(f"{output}: orphan Result without Ticket")
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
