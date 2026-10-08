#!/usr/bin/env python3
"""Read-only Design Ticket/Result gate. Requires PyYAML; never generates content.

--ladder-result <run folder> checks a Run on the design ladder (reason · generate · revise · verify ·
rank, ref/design-ladder.md); --ticket/--result and --folder check an older board's v2 Runs.

No content hashes (JL 260928): a reference is a path; staleness is file time,
a source modified after the record that names it. Any hash field left in an
older record is ignored.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys
import yaml

# Design Run names: `run-design-<op>-<MMDD>-<slug>` (JL 261001). Older short names are retired.
RUN = re.compile(r"run-design-(generate|verify)-[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*")
# Commission is the current human decision Run; Adopt is legacy audit only.
# The worker never produces them, so the folder audit checks only their
# Ticket/Result pairing and a recorded decision, never worker semantics.
DECISION_RUN = re.compile(r"run-design-(commission|adopt)-[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*")
RUN_GLOBS = ("run-design-*",)


def op_of(match):
    """The operation a Design Run name carries."""
    return match.group(1)
ROLES = {"evidence", "inspiration", "reference", "avoid", "base", "feedback", "handoff"}
LINK_SLOT = "{LINK}"
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


def reference(root, ref, bounded=False, record=None):
    """Resolve one referenced file. With ``record``, the file must not be newer
    than the record that names it (staleness by file time, never a hash)."""
    need(isinstance(ref, dict), "file reference must be a mapping")
    path = resolve(root, ref.get("path"), bounded)
    parts = Path(str(ref.get("path"))).parts
    if not bounded and not path.is_file() and parts[:1] == ("outline",):
        moved = root / "draft" / Path(*parts[1:])  # Page layout 0.118 renamed a Folder's outline/ to draft/
        if moved.is_file():
            path = moved.resolve()
    shown = _shown(path, root)
    need(path.is_file(), f"missing input/artifact: {shown}")
    if record is not None:
        need(path.stat().st_mtime <= Path(record).stat().st_mtime,
             f"stale: {shown} changed after {Path(record).name} was written")
    return path


def _shown(path, root):
    """A path as a reader finds it: relative to the folder being checked, never absolute."""
    import os
    try:
        return os.path.relpath(path, Path(root).resolve())
    except ValueError:
        return path.name


def artifact_records(folder, records, record=None):
    need(isinstance(records, list) and records, "a Generate Result requires content artifacts")
    seen = set()
    out = []
    for ref in records:
        path = reference(folder, ref, bounded=True, record=record)
        need(ref["path"].startswith("content/"), "a Generate Result artifact must live in content/")
        need(path not in seen, "duplicate content artifact")
        seen.add(path)
        out.append((ref["path"], path))
    return out


def render_records(output, manifest, subjects, item=None, record=None):
    """Validate optional render evidence without counting pictures as content.

    subjects maps resolved source artifact paths to their Generate Run ids.
    Returned picture paths are bounded by this Result's render directory.
    """
    if "render_manifest" not in manifest:
        return []
    root = output.resolve() / "render"
    path = reference(output, manifest["render_manifest"], bounded=True, record=record)
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
        source = reference(path.parent, {"path": row.get("source")})
        need(source in subjects and subjects[source] == row.get("candidate"),
             "render source/candidate is not a commissioned content artifact")
        picture = reference(path.parent, {"path": row.get("render")}, bounded=True, record=record)
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

    Staleness is file time, never a hash (JL 260928).  An open run is stale when
    one of its ``inputs`` or ``targets`` is newer than its Ticket; a closed Verify
    is stale when a target Result is newer than the Verify's own ``result.yaml``.
    The config and approval record are frozen copies the workbench writes with
    the Ticket; they are checked for existence only, so a fresh checkout (which
    writes ``scripts/`` after ``runs/`` and ``results/``) never reads as stale."""
    ticket = Path(ticket).resolve()
    since = None if historical else ticket
    need(ticket.parent.name == "runs" and ticket.suffix == ".yaml",
         "Ticket must be owner/runs/<run>.yaml")
    data = document(ticket)
    schema = data.get("schema")
    need(schema == TICKET_SCHEMA, "unsupported Ticket schema")
    match = RUN.fullmatch(ticket.stem)
    need(match is not None, "invalid Design Run stem")
    need(data.get("run") == ticket.stem, "Ticket identity mismatch")
    op = data.get("operation")
    need(op == op_of(match), "operation does not match Ticket stem")
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
            method = ("observation", "pass_when", "fail_when", "not_verifiable_when")
            # A closed run froze its config under the rule of its own day; the
            # observation method became required later.  A historical record
            # that names none of those keys is read as it was written, not
            # called invalid.  Naming some but not all is still a defect, and a
            # current Ticket always owes all four.
            if not historical or any(criterion.get(key) for key in method):
                for key in method:
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
        path = reference(owner, item, record=since)
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
    closed = output / "result.yaml"
    target_since = since if not historical else (closed if closed.is_file() else None)
    for target in targets:
        path = reference(owner, target, record=target_since)
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
        need(target_match is not None and op_of(target_match) == "generate"
             and path.parent.name == target_run, "target Run/Result identity mismatch")
        producer = string(manifest.get("producer"), "target.producer")
        producers.add(producer)
        runtime = document(path.parent / "runtime.yaml")
        need(runtime.get("status") == "complete" and runtime.get("run") == manifest.get("run"),
             "target generation is not complete")
        target_artifacts = artifact_records(path.parent, manifest.get("artifacts"), record=path)
        render_records(path.parent, manifest,
                       {artifact: target_run for _, artifact in target_artifacts}, data.get("item"),
                       record=path)
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
        need([t.get("path") for t in manifest.get("targets") or []] == [t.get("path") for t in data["targets"]],
             "Result target refs mismatch")
        if data["operation"] == "generate":
            subjects = artifact_records(output, manifest.get("artifacts"), record=result)
            need(len(subjects) == config["unit"]["count"], "Generate artifact count mismatch")
        else:
            need(manifest.get("artifacts") == [], "verify must not produce replacement artifacts")
        render_records(output, manifest, {
            path: (data["run"] if data["operation"] == "generate"
                   else Path(target.split("::", 1)[0]).parent.name)
            for target, path in subjects
        }, data.get("item"), record=result)
        checks_path = reference(output, manifest.get("checks"), bounded=True, record=result)
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
                # {LINK} is the slot the sending platform fills; it is not counted (JL 261001)
                passed = (len(content.replace(LINK_SLOT, "")) <= value if kind == "max_chars"
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
        op = op_of(DECISION_RUN.fullmatch(ticket.stem))
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
    tickets = sorted(p for pat in RUN_GLOBS for p in (folder / "runs").glob(pat + ".yaml"))
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
            # it was queued): it is stale by definition; only its reason is checked.
            if not runtime.get("failure") or (output / "result.yaml").is_file():
                issues.append(f"{ticket}: a superseded run needs a reason and no result")
            continue
        # an open run's inputs must not be newer than its Ticket; a closed one is read as history
        closed = runtime.get("status") in {"complete", "failed", "blocked"}
        for problem in validate(ticket, historical=closed):
            issues.append(f"{ticket}: {problem}")
        try:
            data = document(ticket)
            runtime = document(output / "runtime.yaml")
            for key, expected in {"run": ticket.stem, "family": "design",
                                  "operation": data.get("operation"),
                                  "target": data.get("target"),
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
            actual = {r.get("path") for r in bound if isinstance(r, dict)}
            need(all(r.get("path") in actual for r in expected_inputs),
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
    for output in sorted(p for pat in RUN_GLOBS for p in (folder / "results").glob(pat)):
        if output.is_dir() and not (folder / "runs" / (output.name + ".yaml")).is_file():
            issues.append(f"{output}: orphan Result without Ticket")
    for output in sorted((folder / "results").glob("r*_design_*")):
        if output.is_dir():
            issues.append(f"{output}: retired Design Result identity is unsupported")
    return issues


# ── the ladder (haipipe-design/ref/design-ladder.md, 261007): one Run folder run-<type>-<target>/ ─────────────
LADDER_RUN = re.compile(r"^(?:run-(reason|generate|verify|revise|rank)-([a-z0-9]+(?:-[a-z0-9]+)*)"
                        r"|r\d\d_(reason|generate|verify|revise|rank)_([a-z0-9<>-]+))$")
LADDER_HARD = {"reason", "generate", "verify", "rank"}
OWN = "own knowledge"


def _ydoc(path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return None


def fence_files(job):
    """The fence's file names, from the Job's inputs/manifest.yaml (else the files on disk)."""
    manifest = _ydoc(job / "inputs" / "manifest.yaml") if (job / "inputs" / "manifest.yaml").is_file() else None
    names = []
    if isinstance(manifest, dict):
        names = [str(f.get("path", "")) for f in manifest.get("files") or [] if isinstance(f, dict)]
    elif (job / "inputs").is_dir():
        names = [q.name for q in (job / "inputs").iterdir() if q.name != "manifest.yaml"]
    return [n for n in names if n]


def in_fence(source, names):
    """A `from` is exactly `own knowledge`; or it starts with a fence file's path, name or stem (`rules.md`, `rules`,
    or its singular `rule`), optionally followed by a locator (`rule r2.1`); or it carries an id, a token of 3+
    characters with a digit, found inside a fence file's name (`W-03 row 2` for handoff-W-03.md). Free prose that only
    mentions a file further on (`my hunch about the goal`) is not a source."""
    text = str(source or "").strip()
    if not text:
        return False
    if text.lower() == OWN:
        return True
    tokens = [t for t in re.split(r"[\s·,;:()]+", text) if t]
    first = tokens[0].lower()
    for name in names:
        base = name.rsplit("/", 1)[-1].lower()
        stem = base.rsplit(".", 1)[0]
        if first in (name.lower(), base, stem) or (stem.endswith("s") and first == stem[:-1]):
            return True
        for tok in tokens:
            low = tok.lower()
            if len(low) >= 3 and re.search(r"\d", low) and re.search(r"[a-z]", low) and low in base:
                return True
    return False


def _csv_rows(path):
    import csv
    try:
        with path.open(encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except OSError:
        return []


def _front(md):
    try:
        text = md.read_text(encoding="utf-8")
    except OSError:
        return {}
    m = re.match(r"(?s)^---\n(.*?)\n---\n", text)
    doc = yaml.safe_load(m.group(1)) if m else {}
    return doc if isinstance(doc, dict) else {}


def ladder_check(run_dir):
    """Problems with one ladder Run's Result: name and kind, the shape for its type, the fence, independence, N."""
    run_dir = Path(run_dir).resolve()
    issues = []
    m = LADDER_RUN.match(run_dir.name)
    if not m:
        return [f"{run_dir.name}: not a design unit Run (run-<reason|generate|verify|revise|rank>-<target>)"]
    rtype = m.group(1) or m.group(3)
    card = _ydoc(run_dir / "run.yaml") if (run_dir / "run.yaml").is_file() else None
    if not isinstance(card, dict):
        return [f"{run_dir.name}: run.yaml missing or not a mapping"]
    if card.get("type") not in (None, rtype):
        issues.append(f"{run_dir.name}: run.yaml type {card.get('type')!r} is not {rtype!r}")
    want = "hard" if rtype in LADDER_HARD else "soft"
    if card.get("kind") not in (None, want):
        issues.append(f"{run_dir.name}: a {rtype} Run is {want}, run.yaml says {card.get('kind')!r}")
    task = run_dir.parent.parent
    job = task.parent
    names = fence_files(job)
    if not names:
        issues.append(f"{job.name}: no fence (inputs/manifest.yaml lists no file)")
    result = run_dir / "result"
    if rtype in LADDER_HARD and not result.is_dir():
        return issues + [f"{run_dir.name}: a hard Run writes its result/; there is none"]

    def froms(entries, what):
        for e in entries:
            if isinstance(e, dict) and not in_fence(e.get("from"), names):
                issues.append(f"{run_dir.name}: {what} {e.get('id') or e.get('element') or '?'} cites "
                              f"{e.get('from')!r}, not a fence file nor 'own knowledge'")

    if rtype == "reason":
        chains, ideas = _ydoc(result / "chains.yaml"), _ydoc(result / "ideas.yaml")
        topics = chains.get("topics") if isinstance(chains, dict) else None
        rows = ideas.get("ideas") if isinstance(ideas, dict) else None
        if not isinstance(topics, list) or not topics:
            issues.append(f"{run_dir.name}: result/chains.yaml needs topics: [...]")
            topics = []
        if not isinstance(rows, list) or not rows:
            issues.append(f"{run_dir.name}: result/ideas.yaml needs ideas: [...]")
            rows = []
        if not (result / "topics.md").is_file():
            issues.append(f"{run_dir.name}: result/topics.md (the readable report) is missing")
        for t in topics:
            if not isinstance(t, dict) or not all(k in t for k in ("id", "title", "from", "steps", "ideas")):
                issues.append(f"{run_dir.name}: a topic needs id · title · from · steps · ideas")
            elif not all(isinstance(s, dict) and "says" in s and "so" in s for s in t["steps"] or [None]):
                issues.append(f"{run_dir.name}: topic {t['id']}: each step needs says · so")
            else:                                            # a step may cite its own source, over its topic's
                froms([st for st in t["steps"] if "from" in st], f"topic {t['id']} step")
        froms(topics, "topic")
        topic_ids = {t.get("id") for t in topics if isinstance(t, dict)}
        designs = []
        for i in rows:
            if not isinstance(i, dict) or not all(k in i for k in ("id", "name", "idea", "topic", "design")):
                issues.append(f"{run_dir.name}: an idea needs id · name · idea · topic · design (name: its Task's slug)")
                continue
            if i["topic"] not in topic_ids:
                issues.append(f"{run_dir.name}: idea {i['id']} names no topic of chains.yaml ({i['topic']})")
            if not re.match(r"^d\d\d$", str(i["design"])):
                issues.append(f"{run_dir.name}: idea {i['id']}: design is d<NN>, not {i['design']!r}")
            designs.append(i["design"])
        if len(designs) != len(set(designs)):
            issues.append(f"{run_dir.name}: two ideas name the same design")
    elif rtype in ("generate", "revise"):
        drafts = [result / "design.md"] + sorted((run_dir / "passes").glob("*/design.md"))
        if not any(d.is_file() and d.read_text(encoding="utf-8").strip() for d in drafts) and \
                not (result / "content" / "screen.html").is_file():
            issues.append(f"{run_dir.name}: no draft (result/design.md, a pass's design.md or content/screen.html)")
        elements = _ydoc(result / "elements.yaml") if (result / "elements.yaml").is_file() else \
            _ydoc(task / "elements.yaml") if (task / "elements.yaml").is_file() else None
        if rtype == "generate":
            if not isinstance(elements, list) or not elements:
                issues.append(f"{run_dir.name}: no element record (result/elements.yaml or the Task's elements.yaml)")
            else:
                for e in elements:
                    if not isinstance(e, dict) or not all(k in e for k in ("element", "words", "from", "because")):
                        issues.append(f"{run_dir.name}: an element needs element · words · from · because")
                froms(elements, "element")
    elif rtype == "verify":
        if not (result / "review.md").is_file():
            issues.append(f"{run_dir.name}: result/review.md (each test, verdict, evidence) is missing")
        if card.get("status") not in ("passed", "failed"):
            issues.append(f"{run_dir.name}: a finished verify's status is passed or failed, not {card.get('status')!r}")
        tests = card.get("tests")
        if not isinstance(tests, dict) or not {"T0", "T1"} <= set(tests):
            issues.append(f"{run_dir.name}: run.yaml tests needs at least T0 and T1")
        producers = set()
        for q in (task / "runs").iterdir() if (task / "runs").is_dir() else ():
            other = _ydoc(q / "run.yaml") if (q / "run.yaml").is_file() else None
            mm = LADDER_RUN.match(q.name)
            if isinstance(other, dict) and mm and (mm.group(1) or mm.group(3)) in ("generate", "revise") and other.get("by"):
                producers.add(str(other["by"]))
        if not str(card.get("by") or "").strip():
            issues.append(f"{run_dir.name}: run.yaml by is empty: who verified must be written to check independence")
        elif str(card["by"]) in producers:
            issues.append(f"{run_dir.name}: verify by {card['by']!r}, who also generated: not independent")
    elif rtype == "rank":
        rows = _csv_rows(result / "ranking.csv")
        if not rows:
            issues.append(f"{run_dir.name}: result/ranking.csv (rank,design,predicted,why,kept) is missing or empty")
        else:
            missing = {"rank", "design", "predicted", "why", "kept"} - set(rows[0])
            if missing:
                issues.append(f"{run_dir.name}: ranking.csv lacks {', '.join(sorted(missing))}")
            kept = [r for r in rows if str(r.get("kept", "")).strip().lower() == "yes"]
            bad = [r.get("design") for r in rows if str(r.get("kept", "")).strip().lower() not in ("yes", "no")]
            if bad:
                issues.append(f"{run_dir.name}: kept is yes or no ({', '.join(map(str, bad))})")
            jface = next((q for q in (job / f"{job.name}.md",) if q.is_file()), None)
            n = _front(jface).get("n") if jface else None
            if isinstance(n, int) and len(kept) != n:
                issues.append(f"{run_dir.name}: keeps {len(kept)} designs, the Job's n is {n}")
            known = {re.match(r"^t\d+_(d\d+)_", q.name).group(1) for q in job.iterdir()
                     if q.is_dir() and re.match(r"^t\d+_d\d+_", q.name)} if job.is_dir() else set()
            unknown = [r.get("design") for r in rows if known and r.get("design") not in known]
            if unknown:
                issues.append(f"{run_dir.name}: ranks designs with no Task: {', '.join(map(str, unknown))}")
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticket", type=Path)
    parser.add_argument("--result", type=Path)
    parser.add_argument("--folder", type=Path)
    parser.add_argument("--ladder-result", type=Path, help="a ladder Run folder: <Task>/runs/run-<type>-<target>")
    args = parser.parse_args()
    if args.ladder_result:
        if args.ticket or args.folder or args.result:
            parser.error("--ladder-result stands alone")
        problems = ladder_check(args.ladder_result)
        for problem in problems:
            print("FAIL:", problem)
        if not problems:
            print("PASS: ladder Result shape, fence and independence")
        return 1 if problems else 0
    if bool(args.ticket) == bool(args.folder) or (args.result and not args.ticket):
        parser.error("choose --ticket [--result], --folder, or --ladder-result")
    problems = audit_folder(args.folder) if args.folder else validate(args.ticket, args.result)
    for problem in problems:
        print("FAIL:", problem)
    if not problems:
        print("PASS: " + ("Run inventory" if args.folder else
                         "Result integrity and check coverage" if args.result else "Ticket inputs"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
