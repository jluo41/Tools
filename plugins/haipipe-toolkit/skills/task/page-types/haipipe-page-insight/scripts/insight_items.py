#!/usr/bin/env python3
"""Read-only Insight item audit, table, and exact citation packet.

Intent: validate materialized instance/item/version provenance and trace edges;
never infer scientific correctness, execute a recipe, or approve a handoff.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

import yaml

RUN = re.compile(r"r\d{2,}_[a-z0-9][a-z0-9_-]*\Z")
VERSION = re.compile(r"v\d{3,}\Z")
INSTANCE = re.compile(r"[a-z0-9][a-z0-9_/-]*\Z")
TARGETS = {"data": "D", "information": "I", "knowledge": "K", "wisdom": "W"}
STAGES = ("frozen", "evidence", "reasoned", "published")
STATUSES = {"planned", "running", "complete", "failed", "blocked"}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def candidate_digest(result):
    """Bind review to the exact payload without a circular review-file hash."""
    candidate = {k: v for k, v in result.items() if k != "review"}
    return hashlib.sha256(json.dumps(candidate, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def read_yaml(path):
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a mapping")
    return data


def resolve(root, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("missing path")
    path = Path(value)
    return path if path.is_absolute() else Path(root) / path


def full_id(instance, run, version):
    return f"{instance}#{run}@{version}"


def required(record, keys, errors, label):
    for key in keys:
        if record.get(key) in (None, "", [], {}):
            errors.append(f"{label}: missing {key}")


def binding(root, record, errors, label, key="path"):
    try:
        path = resolve(root, record.get(key))
        if not path.is_file():
            raise ValueError(f"missing file {path}")
        sha = record.get("sha256", "")
        if not re.fullmatch(r"[0-9a-f]{64}", str(sha)) or digest(path) != sha:
            raise ValueError(f"hash mismatch {path}")
    except (ValueError, OSError, TypeError) as exc:
        errors.append(f"{label}: {exc}")


def local_receipt(directory, value, errors, label):
    try:
        path = resolve(directory, value).resolve()
        if not path.is_relative_to(directory.resolve()) or not path.is_file():
            raise ValueError("receipt must resolve inside execution directory")
    except (ValueError, OSError, TypeError) as exc:
        errors.append(f"{label}: {exc}")


def trace(result, frozen, errors, label):
    target = result.get("target")
    if target not in TARGETS:
        errors.append(f"{label}: invalid target")
        return
    if result.get("outcome") != "accepted":
        required(result, ("reason",), errors, label)
        if result.get("RF"):
            errors.append(f"{label}: non-answer cannot export accepted RF")
        return
    end = list(TARGETS).index(target)
    previous = {f"source:{i}" for i in range(len(frozen.get("supporting_results", [])))}
    previous |= {f"dataset:{i}" for i in range(len(frozen.get("datasets", [])))}
    previous |= {f"local:{i}" for i in range(len(frozen.get("local_sources", [])))}
    seen = set()
    for rung in list("DIKW")[:end + 1] + ["RF"]:
        rows = result.get(rung, [])
        if not isinstance(rows, list) or not rows:
            errors.append(f"{label}: accepted target requires {rung} rows")
            previous = set()
            continue
        current = set()
        for row in rows:
            if not isinstance(row, dict):
                errors.append(f"{label}: invalid {rung} row")
                continue
            ident = row.get("id", "")
            if not re.fullmatch(rf"{rung}[1-9]\d*", str(ident)) or ident in seen:
                errors.append(f"{label}: invalid or duplicate row id {ident}")
            seen.add(ident)
            current.add(ident)
            required(row, ("text", "parents"), errors, f"{label}/{ident}")
            parents = row.get("parents", [])
            if not isinstance(parents, list) or not all(p in previous for p in parents):
                errors.append(f"{label}/{ident}: parent skips rung or is unresolved")
            if rung in {"K", "RF"}:
                required(row, ("strength", "boundary"), errors, f"{label}/{ident}")
            if rung == "K":
                required(row, ("rivals",), errors, f"{label}/{ident}")
        previous = current


def execution(root, manifest, item, directory):
    errors = []
    run, version = item["run"], directory.name
    ident = full_id(manifest["instance"], run, version)
    info = {"execution": ident, "version": version, "checkpoint": "planned",
            "status": "invalid", "outcome": "", "findings": [], "stale": False}
    try:
        runtime = read_yaml(directory / "runtime.yaml")
        if runtime.get("schema") != "haipipe.insight-runtime/v1":
            errors.append(f"{ident}: invalid runtime schema")
        if runtime.get("execution") != ident:
            errors.append(f"{ident}: runtime execution identity mismatch")
        if runtime.get("family") != "insight" or runtime.get("operation") != "item":
            errors.append(f"{ident}: expected insight/item operation")
        status = runtime.get("status")
        info["status"] = status
        if status not in STATUSES:
            errors.append(f"{ident}: invalid runtime status")
        checkpoints = runtime.get("checkpoints", {})
        if not isinstance(checkpoints, dict):
            raise ValueError("checkpoints must be a mapping")
        unknown = set(checkpoints) - set(STAGES)
        if unknown:
            errors.append(f"{ident}: unknown checkpoints {sorted(unknown)}")
        for i, name in enumerate(STAGES):
            if name not in checkpoints:
                continue
            if any(prior not in checkpoints for prior in STAGES[:i]):
                errors.append(f"{ident}: checkpoint {name} skips a predecessor")
            mark = checkpoints[name]
            required(mark, ("at", "receipt"), errors, f"{ident}/{name}")
            local_receipt(directory, mark.get("receipt"), errors, f"{ident}/{name}")
            info["checkpoint"] = name
        attempts = runtime.get("attempts", [])
        if not isinstance(attempts, list) or not attempts:
            errors.append(f"{ident}: missing attempt trail")
        elif [a.get("attempt") for a in attempts] != list(range(1, len(attempts) + 1)):
            errors.append(f"{ident}: attempt trail must be contiguous and unique")
        frozen = {}
        if "frozen" in checkpoints or status == "complete":
            frozen = read_yaml(directory / "input.yaml")
            if frozen.get("schema") != "haipipe.insight-input/v1":
                errors.append(f"{ident}: invalid input schema")
            for key, value in (("instance", manifest["instance"]), ("run", run), ("version", version)):
                if frozen.get(key) != value:
                    errors.append(f"{ident}: frozen {key} identity mismatch")
            required(frozen, ("question", "target", "acceptance", "datasets"), errors, ident)
            if runtime.get("input_sha256") != digest(directory / "input.yaml"):
                errors.append(f"{ident}: frozen input hash mismatch")
            known = {f"{d['id']}@{d['version']}": d for d in manifest.get("datasets", [])}
            for data in frozen.get("datasets", []):
                key = f"{data.get('id')}@{data.get('version')}"
                if key not in known or data != known[key]:
                    errors.append(f"{ident}: unknown or changed dataset binding {key}")
                binding(root, data, errors, f"{ident}/{key}", "manifest")
            for source in frozen.get("supporting_results", []):
                required(source, ("run", "path", "sha256"), errors, ident)
                source_id = str(source.get("run", ""))
                if not (re.fullmatch(r"b\d+j\d+t\d+r\d+", source_id)
                        or re.fullmatch(r"pj\d+t\d+r\d+", source_id)
                        or re.fullmatch(r"[a-z0-9][a-z0-9_/-]*#r\d+_[a-z0-9_-]+@v\d{3,}", source_id)):
                    errors.append(f"{ident}: unqualified Supporting Run id")
                binding(root, source, errors, ident)
                if "#" in source_id:
                    upstream = read_yaml(resolve(root, source.get("path")))
                    if upstream.get("execution") != source_id:
                        errors.append(f"{ident}: Supporting Result execution identity mismatch")
                    if upstream.get("schema") == "haipipe.insight-result/v1" and upstream.get("outcome") != "accepted":
                        errors.append(f"{ident}: Supporting Insight Result is not accepted")
            for source in frozen.get("local_sources", []):
                binding(root, source, errors, ident)
            for call in frozen.get("recipe_calls", []):
                required(call, ("recipe_id", "owner", "entry", "entry_sha256", "code_version",
                                "parameters", "parameter_contract", "execution", "receipt"), errors, ident)
                binding(root, {"path": call.get("entry"), "sha256": call.get("entry_sha256")}, errors, ident)
                required(call.get("parameters", {}), ("input_manifest", "output_root"), errors, ident)
            intended = set(item.get("datasets", []))
            used = {f"{d.get('id')}@{d.get('version')}" for d in frozen.get("datasets", [])}
            info["stale"] = intended != used or any(frozen.get(k) != item.get(k)
                                                   for k in ("question", "target", "acceptance"))
        path = directory / "result.yaml"
        if path.exists():
            result = read_yaml(path)
            if result.get("schema") != "haipipe.insight-result/v1":
                errors.append(f"{ident}: invalid result schema")
            if result.get("execution") != ident:
                errors.append(f"{ident}: Result execution identity mismatch")
            if not frozen or result.get("target") != frozen.get("target"):
                errors.append(f"{ident}: Result target differs from frozen input")
            if runtime.get("result_sha256") != digest(path):
                errors.append(f"{ident}: Result hash mismatch")
            outcome = result.get("outcome")
            info["outcome"] = outcome
            if outcome not in {"accepted", "insufficient", "rejected"}:
                errors.append(f"{ident}: invalid outcome")
            trace(result, frozen, errors, ident)
            if outcome == "accepted":
                review = result.get("review", {})
                if review.get("verdict") != "pass":
                    errors.append(f"{ident}: accepted Result lacks passing review")
                local_receipt(directory, review.get("receipt"), errors, ident)
                receipt = read_yaml(resolve(directory, review.get("receipt")))
                if receipt.get("schema") != "haipipe.insight-review/v1" or receipt.get("verdict") != "pass":
                    errors.append(f"{ident}: invalid independent review receipt")
                required(receipt, ("author", "reviewer", "checked"), errors, ident)
                if receipt.get("author") == receipt.get("reviewer"):
                    errors.append(f"{ident}: reviewer must differ from author")
                if receipt.get("candidate_sha256") != candidate_digest(result) or receipt.get("input_sha256") != runtime.get("input_sha256"):
                    errors.append(f"{ident}: review does not bind exact candidate and input")
                if status != "complete" or set(STAGES) - set(checkpoints):
                    errors.append(f"{ident}: accepted Result lacks completed checkpoints")
                info["findings"] = [r["id"] for r in result.get("RF", [])]
            elif "published" in checkpoints:
                errors.append(f"{ident}: non-answer cannot be published as findings")
        elif status == "complete" or "published" in checkpoints:
            errors.append(f"{ident}: complete/published execution has no Result")
        if status == "complete" and set(STAGES[:3]) - set(checkpoints):
            errors.append(f"{ident}: completion skips reasoning/evidence checks")
    except (OSError, ValueError, TypeError, KeyError, AttributeError, yaml.YAMLError) as exc:
        errors.append(f"{ident}: invalid execution: {exc}")
    info["valid"] = not errors
    return info, errors


def inspect(root, selected=None, version=None):
    root = Path(root).resolve()
    errors, rows = [], []
    manifest = read_yaml(root / "workflow" / "insight.yaml")
    if manifest.get("schema") != "haipipe.insight-instance/v1":
        errors.append("invalid instance schema")
    required(manifest, ("instance", "topic", "datasets", "items"), errors, "instance")
    instance = str(manifest.get("instance", ""))
    if not INSTANCE.fullmatch(instance) or ".." in instance:
        errors.append("invalid instance id")
    seen_data = set()
    for data in manifest.get("datasets", []):
        required(data, ("id", "version", "manifest", "sha256"), errors, "dataset")
        key = f"{data.get('id')}@{data.get('version')}"
        if key in seen_data:
            errors.append(f"duplicate dataset version {key}")
        seen_data.add(key)
        if not selected:
            binding(root, data, errors, key, "manifest")
    seen_runs = set()
    for item in manifest.get("items", []):
        run = item.get("run", "")
        if not RUN.fullmatch(str(run)) or run in seen_runs:
            errors.append(f"invalid or duplicate item id {run}")
            continue
        seen_runs.add(run)
        if selected and run != selected:
            continue
        required(item, ("question", "target", "datasets", "expected", "acceptance"), errors, run)
        if item.get("target") not in TARGETS:
            errors.append(f"{run}: invalid target")
        if any(d not in seen_data for d in item.get("datasets", [])):
            errors.append(f"{run}: undeclared dataset version")
        versions = []
        result_root = root / "results" / run
        ticket = root / "runs" / f"{run}.sh"
        if result_root.exists():
            for directory in sorted(result_root.iterdir()):
                if version and directory.name != version:
                    continue
                if not directory.is_dir() or not VERSION.fullmatch(directory.name):
                    errors.append(f"{run}: unexpected result entry {directory.name}")
                    continue
                if not ticket.is_file():
                    errors.append(f"{run}: Result has no local ticket")
                info, faults = execution(root, manifest, item, directory)
                versions.append(info)
                errors.extend(faults)
        versions.sort(key=lambda v: int(v["version"][1:]))
        if ticket.is_file() and not versions and not version:
            errors.append(f"{run}: allocated ticket has no runtime receipt")
        rows.append({"item": item, "versions": versions, "ticket": ticket.is_file()})
    if selected and selected not in seen_runs:
        errors.append(f"unknown item {selected}")
    if not selected and (root / "results").is_dir():
        for path in (root / "results").iterdir():
            if path.name not in seen_runs:
                # Local Evidence/Execution dependencies retain their own Run
                # dialect, rather than becoming fictitious Insight Items.
                tickets = list((root / "runs").glob(f"{path.name}.*"))
                receipts = list(path.glob("**/runtime.yaml")) if path.is_dir() else []
                owned = False
                for receipt_path in receipts:
                    receipt = read_yaml(receipt_path)
                    if receipt.get("family") in {"page", "execution", "discovery", "design"} and receipt.get("status"):
                        owned = True
                    else:
                        errors.append(f"invalid dependency receipt {receipt_path}")
                if not tickets or not owned:
                    errors.append(f"orphan Result item {path.name}")
    return manifest, rows, errors


TABLE_HEADERS = ["Item", "Question", "Target", "Datasets", "Current execution", "Checkpoint", "Outcome", "Last accepted / RF"]


def table_rows(rows):
    cells = []
    for row in rows:
        item, versions = row["item"], row["versions"]
        current = versions[-1] if versions else {}
        accepted = [v for v in versions if v["valid"] and v["outcome"] == "accepted"]
        last = accepted[-1] if accepted else {}
        state = current.get("outcome") or current.get("status", "not run")
        if current.get("stale"):
            state += " (input binding stale)"
        if current and not current.get("valid"):
            state = "invalid"
        values = [item["run"], item.get("question", ""), item.get("target", ""),
                  ", ".join(item.get("datasets", [])), current.get("execution", "none"),
                  current.get("checkpoint", "ticket ready" if row["ticket"] else "planned"), state,
                  (last.get("execution", "none") + (" / " + ", ".join(last["findings"]) if last else ""))]
        cells.append(values)
    return cells


def table(rows):
    lines = ["| " + " | ".join(TABLE_HEADERS) + " |", "|" + "---|" * len(TABLE_HEADERS)]
    for values in table_rows(rows):
        lines.append("| " + " | ".join(str(v).replace("|", "\\|").replace("\n", " ") for v in values) + " |")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "table", "cite"))
    parser.add_argument("folder", type=Path)
    parser.add_argument("--item")
    parser.add_argument("--version")
    parser.add_argument("--finding")
    parser.add_argument("--historical", action="store_true", help="Resolve an old pin without approving current applicability")
    args = parser.parse_args(argv)
    try:
        manifest, rows, errors = inspect(args.folder, args.item if args.command == "cite" else None,
                                         args.version if args.command == "cite" else None)
        if args.command == "table":
            print(table(rows))
        if args.command == "cite" and not errors:
            if not (args.item and args.version and args.finding):
                raise ValueError("cite requires --item, --version, --finding; latest is not accepted")
            candidates = [v for row in rows for v in row["versions"] if v["version"] == args.version]
            if len(candidates) != 1 or args.finding not in candidates[0]["findings"]:
                raise ValueError("requested accepted item/version/finding does not resolve")
            if candidates[0]["stale"] and not args.historical:
                raise ValueError("historical Result exists but current input binding needs recheck")
            path = args.folder.resolve() / "results" / args.item / args.version / "result.yaml"
            print(json.dumps({"instance": manifest["instance"], "item": args.item,
                              "version": args.version, "finding": args.finding,
                              "applicability": "historical-needs-recheck" if args.historical else "current-binding-matches",
                              "result": str(path), "sha256": digest(path)}, indent=2))
        for error in errors:
            print(error, file=sys.stderr)
        if args.command == "check":
            print(f"{len(rows)} items; {sum(len(r['versions']) for r in rows)} executions; {len(errors)} findings")
        return int(bool(errors))
    except (OSError, ValueError, TypeError, KeyError, AttributeError, yaml.YAMLError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
