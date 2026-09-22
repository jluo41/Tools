#!/usr/bin/env python3
"""Insight item allocation, input freezing, audit, and exact citation packets.

Intent: validate materialized instance/item/version provenance and trace edges;
never infer scientific correctness, execute a recipe, or approve a handoff.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

import yaml

RUN = re.compile(r"(?:ri|r)\d{2,}_[a-z0-9][a-z0-9_-]*\Z")
INSIGHT_RUN = re.compile(r"ri\d{2,}_[a-z0-9][a-z0-9_-]*\Z")
BASE_RUN = re.compile(r"(?:r\d{2,}_[a-z0-9][a-z0-9_-]*|b\d+j\d+t\d+r\d+)\Z")
VERSION = re.compile(r"v\d{3,}\Z")
INSTANCE = re.compile(r"[a-z0-9][a-z0-9_/-]*\Z")
TARGETS = {"data": "D", "information": "I", "knowledge": "K", "wisdom": "W"}
STAGES = ("frozen", "evidence", "reasoned", "published")
STATUSES = {"planned", "running", "complete", "failed", "blocked"}
INSTANCE_SCHEMAS = {"haipipe.insight-instance/v1", "haipipe.insight-instance/v2"}
INPUT_SCHEMAS = {"haipipe.insight-input/v1", "haipipe.insight-input/v2"}
EVIDENCE_CONTRACT = "haipipe.insight-evidence/v1"
BINDING_FIELDS = ("instance", "run", "base_run", "question", "target", "expected",
                  "acceptance", "datasets")


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


def item_ticket(root, item):
    """Resolve the authored ticket for a legacy item or current RI binding."""
    run = item.get("run", "")
    suffix = ".yaml" if INSIGHT_RUN.fullmatch(str(run)) else ".sh"
    return Path(root) / "runs" / f"{run}{suffix}"


def validate_base_run(root, record, errors, label):
    """Validate the normal R ticket that an RI rebinds to new data."""
    if not isinstance(record, dict):
        errors.append(f"{label}: base_run must be a mapping")
        return
    required(record, ("id", "ticket", "sha256"), errors, f"{label}/base_run")
    ident = str(record.get("id", ""))
    if not BASE_RUN.fullmatch(ident):
        errors.append(f"{label}: invalid base Run id {ident}")
    try:
        ticket = resolve(root, record.get("ticket"))
        if ident.startswith("r") and ticket.stem != ident:
            errors.append(f"{label}: local base Run id does not match ticket stem")
    except (ValueError, TypeError):
        pass
    binding(root, record, errors, f"{label}/base_run", "ticket")


def validate_insight_ticket(root, item, ticket, errors):
    """Require RI to be an explicit immutable R + dataset binding."""
    run = item.get("run", "")
    if not INSIGHT_RUN.fullmatch(str(run)):
        return
    validate_base_run(root, item.get("base_run"), errors, run)
    try:
        record = read_yaml(ticket)
        if record.get("schema") != "haipipe.insight-run/v1":
            errors.append(f"{run}: invalid Insight Run ticket schema")
        if record.get("run") != run:
            errors.append(f"{run}: Insight Run ticket identity mismatch")
        for key in ("base_run", "datasets", "question", "target", "expected", "acceptance"):
            if record.get(key) != item.get(key):
                errors.append(f"{run}: Insight Run ticket differs from manifest field {key}")
    except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
        errors.append(f"{run}: invalid Insight Run ticket: {exc}")


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


def validate_evidence(root, frozen, errors, ident, *, new_input=False):
    """Check exact input bindings; native owners still own scientific acceptance."""
    for key in ("supporting_results", "local_sources", "recipe_calls"):
        if not isinstance(frozen.get(key, []), list):
            raise ValueError(f"{key} must be a list")
    supports = frozen.get("supporting_results", [])
    for source in supports:
        required(source, ("run", "path", "sha256"), errors, ident)
        source_id = str(source.get("run", ""))
        if not (re.fullmatch(r"b\d+j\d+t\d+r\d+", source_id)
                or re.fullmatch(r"pj\d+t\d+r\d+", source_id)
                or re.fullmatch(r"[a-z0-9][a-z0-9_/-]*#(?:ri|r)\d+_[a-z0-9_-]+@v\d{3,}", source_id)):
            errors.append(f"{ident}: unqualified Supporting Run id")
        if source_id == ident:
            errors.append(f"{ident}: an RI cannot be its own Supporting Run")
        binding(root, source, errors, ident)
        if new_input:
            required(source, ("ticket", "ticket_sha256", "receipt", "receipt_sha256"), errors, ident)
            for key in ("ticket", "receipt"):
                binding(root, {"path": source.get(key), "sha256": source.get(key + "_sha256")}, errors, ident)
            if source.get("receipt"):
                upstream_receipt = read_yaml(resolve(root, source["receipt"]))
                if source_id not in (upstream_receipt.get("execution"), upstream_receipt.get("run_id"), upstream_receipt.get("run")):
                    errors.append(f"{ident}: Supporting receipt execution identity mismatch")
                if upstream_receipt.get("status") not in {"complete", "accepted", "passed"}:
                    errors.append(f"{ident}: Supporting receipt is not complete")
        if "#" in source_id:
            upstream = read_yaml(resolve(root, source.get("path")))
            if upstream.get("execution") != source_id:
                errors.append(f"{ident}: Supporting Result execution identity mismatch")
            if upstream.get("schema") == "haipipe.insight-result/v1" and upstream.get("outcome") != "accepted":
                errors.append(f"{ident}: Supporting Insight Result is not accepted")
    for source in frozen.get("local_sources", []):
        binding(root, source, errors, ident)
    if new_input and not supports:
        required(frozen, ("local_evidence_reason",), errors, ident)
        # Dataset manifests can justify inventory observations; they do not
        # authorize numerical work that still needs an independent producer.
        if not frozen.get("local_sources") and not frozen.get("datasets"):
            errors.append(f"{ident}: no governed evidence for zero-support input")
    for call in frozen.get("recipe_calls", []):
        required(call, ("recipe_id", "owner", "entry", "entry_sha256", "code_version",
                        "parameters", "parameter_contract", "receipt"), errors, ident)
        binding(root, {"path": call.get("entry"), "sha256": call.get("entry_sha256")}, errors, ident)
        required(call.get("parameters", {}), ("input_manifest", "output_root"), errors, ident)
        if not new_input and "producer_execution" not in call:
            # Existing frozen packets retain their recorded dialect. New
            # freezes must resolve separate producer and consumer identities.
            required(call, ("execution",), errors, ident)
            continue
        required(call, ("producer_execution", "consumer_insight_execution",
                        "producer_ticket", "producer_ticket_sha256", "receipt_sha256"), errors, ident)
        producer = call.get("producer_execution")
        if producer == ident or call.get("consumer_insight_execution") != ident:
            errors.append(f"{ident}: recipe producer and consumer identities must be distinct and exact")
        if producer not in {source.get("run") for source in supports}:
            errors.append(f"{ident}: recipe producer has no accepted Supporting Result binding")
        binding(root, {"path": call.get("producer_ticket"),
                       "sha256": call.get("producer_ticket_sha256")}, errors, ident)
        binding(root, {"path": call.get("receipt"), "sha256": call.get("receipt_sha256")}, errors, ident)
        receipt = read_yaml(resolve(root, call.get("receipt")))
        if producer not in (receipt.get("execution"), receipt.get("run_id"), receipt.get("run")):
            errors.append(f"{ident}: producing receipt identity mismatch")
        if receipt.get("status") not in {"complete", "accepted", "passed"}:
            errors.append(f"{ident}: producing receipt is not complete")


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
        binding_path = directory / "binding.yaml"
        if binding_path.exists():
            allocated = read_yaml(binding_path)
            if allocated.get("schema") != "haipipe.insight-binding/v1":
                errors.append(f"{ident}: invalid allocation binding schema")
            if runtime.get("binding_sha256") != digest(binding_path):
                errors.append(f"{ident}: allocation binding hash mismatch")
            if allocated.get("instance") != manifest["instance"] or allocated.get("run") != run:
                errors.append(f"{ident}: allocation binding identity mismatch")
            for key in ("base_run", "question", "target", "expected", "acceptance"):
                if allocated.get(key) != item.get(key):
                    errors.append(f"{ident}: allocation binding differs from RI {key}")
            if [f"{d.get('id')}@{d.get('version')}" for d in allocated.get("datasets", [])] != item.get("datasets"):
                errors.append(f"{ident}: allocation dataset binding differs from RI")
        if "frozen" in checkpoints or status == "complete":
            frozen = read_yaml(directory / "input.yaml")
            if frozen.get("schema") not in INPUT_SCHEMAS:
                errors.append(f"{ident}: invalid input schema")
            for key, value in (("instance", manifest["instance"]), ("run", run), ("version", version)):
                if frozen.get(key) != value:
                    errors.append(f"{ident}: frozen {key} identity mismatch")
            required(frozen, ("question", "target", "acceptance", "datasets"), errors, ident)
            if INSIGHT_RUN.fullmatch(run):
                if frozen.get("schema") != "haipipe.insight-input/v2":
                    errors.append(f"{ident}: RI execution requires input schema v2")
                if frozen.get("base_run") != item.get("base_run"):
                    errors.append(f"{ident}: frozen base Run differs from RI binding")
                validate_base_run(root, frozen.get("base_run"), errors, ident)
            if runtime.get("input_sha256") != digest(directory / "input.yaml"):
                errors.append(f"{ident}: frozen input hash mismatch")
            if binding_path.exists() and any(frozen.get(key) != allocated.get(key) for key in BINDING_FIELDS):
                errors.append(f"{ident}: frozen input differs from allocation binding")
            known = {f"{d['id']}@{d['version']}": d for d in manifest.get("datasets", [])}
            for data in frozen.get("datasets", []):
                key = f"{data.get('id')}@{data.get('version')}"
                if key not in known or data != known[key]:
                    errors.append(f"{ident}: unknown or changed dataset binding {key}")
                binding(root, data, errors, f"{ident}/{key}", "manifest")
            evidence_contract = frozen.get("evidence_contract")
            if evidence_contract is not None and evidence_contract != EVIDENCE_CONTRACT:
                errors.append(f"{ident}: unsupported evidence contract")
            validate_evidence(root, frozen, errors, ident,
                              new_input=evidence_contract == EVIDENCE_CONTRACT)
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
    schema = manifest.get("schema")
    if schema not in INSTANCE_SCHEMAS:
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
        if schema == "haipipe.insight-instance/v1" and INSIGHT_RUN.fullmatch(str(run)):
            errors.append(f"{run}: RI requires instance schema v2")
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
        ticket = item_ticket(root, item)
        if INSIGHT_RUN.fullmatch(str(run)) and ticket.is_file():
            validate_insight_ticket(root, item, ticket, errors)
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


TABLE_HEADERS = ["Insight Run", "Base R", "Question", "Target", "Datasets", "Current execution", "Checkpoint", "Outcome", "Last accepted / RF"]


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
        base = item.get("base_run", {})
        values = [item["run"], base.get("id", "legacy self-ticket"),
                  item.get("question", ""), item.get("target", ""),
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


def _stored_path(root, path):
    path = Path(path).resolve()
    try:
        return str(path.relative_to(Path(root).resolve()))
    except ValueError:
        return str(path)


def _write_yaml(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False, allow_unicode=True), encoding="utf-8")


def bind_insight_run(root, *, base_run, base_ticket, datasets, stem, question,
                     target, expected, acceptance):
    """Allocate one RI that reuses an R ticket against declared new data."""
    root = Path(root).resolve()
    manifest_path = root / "workflow" / "insight.yaml"
    manifest = read_yaml(manifest_path)
    if manifest.get("schema") not in INSTANCE_SCHEMAS:
        raise ValueError("bind requires a valid Insight instance manifest")
    if not INSTANCE.fullmatch(str(manifest.get("instance", ""))):
        raise ValueError("bind requires a valid instance id")
    if not BASE_RUN.fullmatch(str(base_run)):
        raise ValueError("--base-run must be a normal local/global R identity")
    ticket_path = resolve(root, base_ticket).resolve()
    if not ticket_path.is_file():
        raise ValueError(f"base Run ticket not found: {ticket_path}")
    if str(base_run).startswith("r") and ticket_path.stem != base_run:
        raise ValueError("local --base-run must match the base ticket stem")
    stem = re.sub(r"[^a-z0-9_-]+", "-", stem.lower()).strip("-_")
    if not stem or not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", stem):
        raise ValueError("--stem must resolve to lowercase ASCII letters, digits, _ or -")
    if target not in TARGETS:
        raise ValueError(f"--target must be one of {', '.join(TARGETS)}")
    if not datasets:
        raise ValueError("bind requires at least one --dataset id@version")
    inventory = {f"{d.get('id')}@{d.get('version')}": d for d in manifest.get("datasets", [])}
    if any(dataset not in inventory for dataset in datasets):
        missing = sorted(set(datasets) - set(inventory))
        raise ValueError(f"undeclared dataset binding: {', '.join(missing)}")
    for dataset in datasets:
        faults = []
        binding(root, inventory[dataset], faults, dataset, "manifest")
        if faults:
            raise ValueError(faults[0])
    numbers = [int(match.group(1)) for item in manifest.get("items", [])
               if (match := re.match(r"ri(\d+)_", str(item.get("run", ""))))]
    run = f"ri{max(numbers, default=0) + 1:02d}_{stem}"
    base = {"id": base_run, "ticket": _stored_path(root, ticket_path),
            "sha256": digest(ticket_path)}
    item = {"run": run, "base_run": base, "question": question, "target": target,
            "datasets": list(datasets), "expected": expected, "acceptance": acceptance}
    ticket = {"schema": "haipipe.insight-run/v1", **item}
    version = "v001"
    allocated = {"schema": "haipipe.insight-binding/v1", "instance": manifest["instance"],
              "run": run, "base_run": base,
              "question": question, "target": target, "expected": expected,
              "acceptance": acceptance,
              "datasets": [inventory[key] for key in datasets]}
    run_ticket = root / "runs" / f"{run}.yaml"
    directory = root / "results" / run / version
    if run_ticket.exists() or directory.exists():
        raise ValueError(f"allocated Insight Run already exists: {run}")
    manifest["schema"] = "haipipe.insight-instance/v2"
    manifest.setdefault("items", []).append(item)
    _write_yaml(run_ticket, ticket)
    _write_yaml(directory / "binding.yaml", allocated)
    runtime = {"schema": "haipipe.insight-runtime/v1",
               "execution": full_id(manifest["instance"], run, version),
               "family": "insight", "operation": "item", "status": "planned",
               "binding_sha256": digest(directory / "binding.yaml"),
               "checkpoints": {},
               "attempts": [{"attempt": 1, "status": "planned"}]}
    _write_yaml(directory / "runtime.yaml", runtime)
    _write_yaml(manifest_path, manifest)
    return {"insight_run": run, "base_run": base_run, "datasets": list(datasets),
            "execution": runtime["execution"], "ticket": str(run_ticket),
            "binding": str(directory / "binding.yaml"), "input": None,
            "runtime": str(directory / "runtime.yaml")}


def freeze_insight_input(root, *, run, version, evidence):
    """Seal ready evidence once, or create a successor version of the same RI.

    Never rewrite a frozen input, including old empty envelopes created by
    earlier bind implementations. Those can use the next explicit version.
    """
    root = Path(root).resolve()
    if not INSIGHT_RUN.fullmatch(str(run)) or not VERSION.fullmatch(str(version)):
        raise ValueError("freeze requires an exact RI and vNNN version")
    if not isinstance(evidence, dict):
        raise ValueError("evidence must be a mapping")
    allowed = {"supporting_results", "local_sources", "recipe_calls", "local_evidence_reason"}
    if set(evidence) - allowed:
        raise ValueError(f"evidence contains binding overrides or unknown keys: {sorted(set(evidence) - allowed)}")
    manifest = read_yaml(root / "workflow/insight.yaml")
    matches = [item for item in manifest.get("items", []) if item.get("run") == run]
    if len(matches) != 1:
        raise ValueError("freeze requires one allocated RI")
    item = matches[0]
    faults = []
    validate_insight_ticket(root, item, item_ticket(root, item), faults)
    directory = root / "results" / run / version
    versions = sorted((p for p in directory.parent.iterdir()
                       if p.is_dir() and VERSION.fullmatch(p.name)),
                      key=lambda p: int(p.name[1:]))
    ident = full_id(manifest["instance"], run, version)
    if (directory / "input.yaml").exists():
        raise ValueError("input is already frozen; use the next explicit version without rewriting it")
    if directory.exists():
        runtime = read_yaml(directory / "runtime.yaml")
        if runtime.get("execution") != ident or runtime.get("checkpoints") or (directory / "result.yaml").exists():
            raise ValueError("freeze requires a matching planned execution with no checkpoints or Result")
        if runtime.get("status") not in {"planned", "blocked"}:
            raise ValueError("freeze requires planned or blocked state")
    else:
        if not versions or int(version[1:]) != int(versions[-1].name[1:]) + 1:
            raise ValueError("new publication must use the next monotonic version")
        if not (versions[-1] / "input.yaml").is_file():
            raise ValueError("freeze the existing planned version first")
        runtime = {"schema": "haipipe.insight-runtime/v1", "execution": ident,
                   "family": "insight", "operation": "item", "status": "planned",
                   "checkpoints": {}, "attempts": [{"attempt": 1, "status": "planned"}]}
    # Recover the immutable allocation from its binding file, or from a
    # hash-verified old frozen input. No missing input is silently synthesized.
    source_dir = directory if (directory / "binding.yaml").is_file() else versions[-1]
    source_runtime = read_yaml(source_dir / "runtime.yaml")
    source = source_dir / "binding.yaml"
    hash_key = "binding_sha256"
    if not source.is_file():
        source, hash_key = source_dir / "input.yaml", "input_sha256"
    if not source.is_file() or source_runtime.get(hash_key) != digest(source):
        raise ValueError("allocation source is missing or its hash changed")
    original = read_yaml(source)
    allocated = {"schema": "haipipe.insight-binding/v1",
                 **{key: original.get(key) for key in BINDING_FIELDS}}
    if allocated["instance"] != manifest["instance"] or allocated["run"] != run:
        faults.append("allocation identity differs from RI")
    for key in ("base_run", "question", "target", "expected", "acceptance"):
        if allocated.get(key) != item.get(key):
            faults.append(f"allocation {key} differs from RI; commission a new RI")
    inventory = {f"{d['id']}@{d['version']}": d for d in manifest.get("datasets", [])}
    if [f"{d['id']}@{d['version']}" for d in allocated["datasets"]] != item.get("datasets"):
        faults.append("allocation datasets differ from RI; commission a new RI")
    for data in allocated["datasets"]:
        if inventory.get(f"{data['id']}@{data['version']}") != data:
            faults.append("dataset inventory changed after allocation")
        binding(root, data, faults, ident, "manifest")
    frozen = {**allocated, "schema": "haipipe.insight-input/v2", "version": version,
              "evidence_contract": EVIDENCE_CONTRACT,
              "supporting_results": [], "recipe_calls": [], **evidence}
    validate_evidence(root, frozen, faults, ident, new_input=True)
    if faults:
        raise ValueError("; ".join(faults))
    directory.mkdir(parents=True, exist_ok=True)
    # Exclusive creation prevents a repeated freeze from replacing saved bytes.
    with (directory / "input.yaml").open("x", encoding="utf-8") as stream:
        stream.write(yaml.safe_dump(frozen, sort_keys=False, allow_unicode=True))
    if not (directory / "binding.yaml").exists():
        _write_yaml(directory / "binding.yaml", allocated)
    runtime["binding_sha256"] = digest(directory / "binding.yaml")
    runtime["input_sha256"] = digest(directory / "input.yaml")
    runtime["checkpoints"] = {"frozen": {
        "at": datetime.now().astimezone().isoformat(timespec="seconds"), "receipt": "input.yaml"}}
    _write_yaml(directory / "runtime.yaml", runtime)
    return {"execution": ident, "input": str(directory / "input.yaml"),
            "input_sha256": runtime["input_sha256"], "runtime": str(directory / "runtime.yaml")}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "table", "cite", "bind", "freeze"))
    parser.add_argument("folder", type=Path)
    parser.add_argument("--item")
    parser.add_argument("--version")
    parser.add_argument("--finding")
    parser.add_argument("--historical", action="store_true", help="Resolve an old pin without approving current applicability")
    parser.add_argument("--base-run")
    parser.add_argument("--base-ticket")
    parser.add_argument("--dataset", action="append", default=[])
    parser.add_argument("--stem")
    parser.add_argument("--question")
    parser.add_argument("--target", choices=tuple(TARGETS))
    parser.add_argument("--expected")
    parser.add_argument("--acceptance")
    parser.add_argument("--evidence", help="ready evidence mapping, relative to the instance or absolute")
    args = parser.parse_args(argv)
    try:
        if args.command == "freeze":
            if not (args.item and args.version and args.evidence):
                raise ValueError("freeze requires --item, --version, and --evidence")
            packet = freeze_insight_input(args.folder, run=args.item, version=args.version,
                                         evidence=read_yaml(resolve(args.folder, args.evidence)))
            print(json.dumps(packet, indent=2))
            return 0
        if args.command == "bind":
            missing = [name for name in ("base_run", "base_ticket", "stem", "question",
                                          "target", "expected", "acceptance")
                       if not getattr(args, name)]
            if missing:
                raise ValueError("bind requires --" + ", --".join(name.replace("_", "-") for name in missing))
            packet = bind_insight_run(args.folder, base_run=args.base_run,
                                      base_ticket=args.base_ticket, datasets=args.dataset,
                                      stem=args.stem, question=args.question,
                                      target=args.target, expected=args.expected,
                                      acceptance=args.acceptance)
            print(json.dumps(packet, indent=2))
            return 0
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
            selected_item = next(row["item"] for row in rows if row["item"]["run"] == args.item)
            print(json.dumps({"instance": manifest["instance"], "item": args.item,
                              "insight_run": args.item if INSIGHT_RUN.fullmatch(args.item) else None,
                              "base_run": selected_item.get("base_run"),
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
