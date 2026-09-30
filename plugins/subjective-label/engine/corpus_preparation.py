#!/usr/bin/env python3
"""Prepare a versioned transcript corpus before a Labeling Contract.

Each command closes one native Corpus Run. Candidate and sealed text stay in
the source owner's folder; only eligible rows enter the fenced package. The
package can be linked to a Page before its labeling job is created.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("subjective_label_job_for_preparation", HERE / "job.py")
job = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(job)

RUN_TYPES = ("source-normalize", "unit-recipe", "unit-materialize", "unit-check", "initial-group-reserve")
NORMALIZER = "transcript-turns-v1"


def _owner_record(owner: Path, source_id: str) -> dict:
    if owner.name != "corpus-preparation" or not isinstance(source_id, str) or not source_id.strip():
        raise ValueError("owner must end in corpus-preparation and source_id must be nonempty")
    return {"schema": "subjective-label/preparation-owner-v1", "source_id": source_id.strip()}


def attach(owner: Path, source_id: str, page_file: Path) -> dict:
    """Let a Page display source-owned Runs while preparation is in progress."""
    owner = owner.resolve()
    record = _owner_record(owner, source_id)
    page_file = job.require_page_folder(page_file)
    page_ref = page_file.parent / "labeling" / "preparation-owner.yaml"
    if (page_file.parent / "labeling" / "config.yaml").is_file() and not page_ref.is_file():
        raise RuntimeError("cannot attach a new preparation owner to an established Labeling job")
    reference = {**record, "owner": str(owner)}
    for path, data in ((owner / "source.yaml", job.yaml_bytes(record)),
                       (page_ref, job.yaml_bytes(reference))):
        if path.exists() and (not path.is_file() or path.read_bytes() != data):
            raise RuntimeError(f"refusing to overwrite changed preparation owner: {path}")
    job.write_once(owner / "source.yaml", job.yaml_bytes(record))
    job.write_once(page_ref, job.yaml_bytes(reference))
    return {"page": str(page_file), "owner": str(owner), "source_id": record["source_id"],
            "preparation_owner_ref": str(page_ref)}


def _bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _jsonl(rows: list[dict]) -> bytes:
    return b"".join(_bytes(row) for row in rows)


def _records(path: Path):
    if not path.is_file() or path.is_symlink():
        raise FileNotFoundError(path)
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"{path.name} line {number}: invalid JSON") from error
        if not isinstance(row, dict):
            raise ValueError(f"{path.name} line {number}: expected object")
        yield number, row


def _rows(path: Path) -> list[dict]:
    return [row for _, row in _records(path)]


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-") or "target"


def _run(owner: Path, operation: str, target: str, *, inputs: dict, artifacts: dict[Path, bytes],
         receipt: dict) -> dict:
    if operation not in RUN_TYPES:
        raise ValueError(f"unknown Corpus Run Type: {operation}")
    owner = owner.resolve()
    for path, data in artifacts.items():
        if not path.is_relative_to(owner) or path.is_symlink():
            raise ValueError(f"artifact outside preparation owner: {path}")
        if path.exists() and (not path.is_file() or path.read_bytes() != data):
            raise RuntimeError(f"refusing to overwrite changed artifact: {path}")
    for path in (owner / "runs").glob("*.yaml"):
        try:
            old = job.load_mapping(path)
            result = job.load_mapping(owner / "results" / path.stem / "result.yaml")
        except (OSError, ValueError, yaml.YAMLError):
            continue
        if (old.get("family") == "corpus" and old.get("operation") == operation
                and old.get("target") == target and old.get("inputs") == inputs
                and result.get("status") == "complete"
                and all(result.get(key) == value for key, value in receipt.items())
                and {entry.get("path") for entry in result.get("artifacts") or []
                     if isinstance(entry, dict)} == {p.relative_to(owner).as_posix() for p in artifacts}):
            if any(not p.is_file() or p.read_bytes() != data for p, data in artifacts.items()):
                raise RuntimeError(f"accepted Corpus Run {path.stem} has missing or changed artifacts")
            return {"run": path.stem, **receipt}
    now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    stem = job.run_stem("corpus", operation, target, now)
    taken = {p.stem for p in (owner / "runs").glob("*.yaml")}
    suffix = 2
    base = stem
    while stem in taken or (owner / "results" / stem).exists():
        stem = f"{base}-{suffix}"
        suffix += 1
    ticket = {"run": stem, "family": "corpus", "operation": operation, "target": target,
              "inputs": inputs, "worker": {"kind": "cli", "name": f"corpus_preparation:{operation}"},
              "acceptance": "accepted source-owned preparation receipt"}
    runtime = {"run": stem, "family": "corpus", "operation": operation, "target": target,
               "status": "complete", "started_at": now, "finished_at": now,
               "ticket": f"runs/{stem}.yaml", "result": f"results/{stem}/result.yaml"}
    result = {"run": stem, "family": "corpus", "operation": operation, "status": "complete",
              "artifacts": [{"path": p.relative_to(owner).as_posix()} for p in artifacts], **receipt}
    for path, data in artifacts.items():
        job.write_once(path, data)
    job.write_once(owner / "runs" / f"{stem}.yaml", job.yaml_bytes(ticket))
    job.write_once(owner / "results" / stem / "runtime.yaml", job.yaml_bytes(runtime))
    job.write_once(owner / "results" / stem / "result.yaml", job.yaml_bytes(result))
    return {"run": stem, **receipt}


def normalize(owner: Path, raw: Path, source_id: str) -> dict:
    owner = owner.resolve()
    owner_record = _owner_record(owner, source_id)
    source_id = owner_record["source_id"]
    raw_data = raw.read_bytes()
    snapshot = "source-" + _digest(_bytes({"source_id": source_id, "raw_digest": _digest(raw_data),
                                           "normalizer": NORMALIZER}))[:16]
    folder = owner / "versions" / snapshot
    good, rejected, seen = [], [], set()
    for line_number, row in _records(raw):
        cid = row.get("conversation_id")
        cid = cid.strip() if isinstance(cid, str) else ""
        turns = row.get("turns")
        reason = ""
        if not cid or cid in seen:
            reason = "missing or duplicate conversation_id"
        elif not isinstance(turns, list) or not turns:
            reason = "turns must be a nonempty list"
        else:
            turn_ids = set()
            for index, turn in enumerate(turns, start=1):
                if (not isinstance(turn, dict) or turn.get("role") not in {"system", "user", "assistant", "tool"}
                        or not isinstance(turn.get("content"), str) or not turn["content"].strip()):
                    reason = "turn needs a supported role and nonempty content"
                    break
                turn_id = turn.get("turn_id", f"t{index}")
                if not isinstance(turn_id, str) or not turn_id.strip() or turn_id in turn_ids:
                    reason = "turn_id must be a unique nonempty string within its conversation"
                    break
                turn_ids.add(turn_id)
        if reason:
            rejected.append({"source_line": line_number, "reason": reason})
            continue
        group = row.get("split_group_id", cid)
        if not isinstance(group, str) or not group.strip():
            rejected.append({"source_line": line_number, "reason": "split_group_id must be a nonempty string"})
            continue
        group = group.strip()
        seen.add(cid)
        good.append({"conversation_id": cid, "split_group_id": group, "source_line": line_number,
                     "turns": [{"turn_id": turn.get("turn_id", f"t{i}"),
                                "role": turn["role"], "content": turn["content"]}
                               for i, turn in enumerate(turns, start=1)]})
    if not good:
        raise ValueError("normalization accepted no conversations")
    good.sort(key=lambda row: row["conversation_id"])
    data = _jsonl(good)
    manifest = {"schema": "subjective-label/source-snapshot-v1", "snapshot_id": snapshot,
                "source_id": source_id, "normalizer": NORMALIZER, "raw_digest": _digest(raw_data),
                "normalized_digest": _digest(data), "n_conversations": len(good),
                "n_groups": len({r["split_group_id"] for r in good}), "n_rejected": len(rejected)}
    return {"snapshot_id": snapshot, **_run(owner, "source-normalize", source_id,
        inputs={"raw_path": str(raw.resolve()), "raw_digest": _digest(raw_data)},
        artifacts={owner / "source.yaml": job.yaml_bytes(owner_record),
                   folder / "normalized.private.jsonl": data,
                   folder / "rejects.private.jsonl": _jsonl(rejected),
                   folder / "manifest.public.json": job.json_bytes(manifest)},
        receipt={"snapshot_id": snapshot, "accepted": True, "counts": {"conversations": len(good), "rejected": len(rejected)}})}


def recipe(owner: Path, snapshot: str, selector: str, context_window: int | None,
           accepted_by: str) -> dict:
    owner = owner.resolve()
    job.load_mapping(owner / "versions" / snapshot / "manifest.public.json")
    if selector not in {"final-assistant-reply", "every-assistant-reply"}:
        raise ValueError("selector must be final-assistant-reply or every-assistant-reply")
    if context_window is not None and context_window < 0:
        raise ValueError("context_window must be non-negative; omit for all earlier turns")
    if not accepted_by.strip():
        raise ValueError("accepted_by names the preparation owner")
    body = {"schema": "subjective-label/unit-recipe-v1", "snapshot_id": snapshot,
            "selector": selector, "context_window": context_window,
            "context_rendering": "role: content, newline separated", "group_field": "split_group_id",
            "accepted_by": accepted_by}
    recipe_id = "recipe-" + _digest(_bytes(body))[:16]
    body["recipe_id"] = recipe_id
    path = owner / "versions" / snapshot / "recipes" / f"{recipe_id}.yaml"
    return {"recipe_id": recipe_id, **_run(owner, "unit-recipe", selector,
        inputs={"snapshot_id": snapshot}, artifacts={path: job.yaml_bytes(body)},
        receipt={"recipe_id": recipe_id, "accepted": True})}


def _candidate_rows(normalized: list[dict], recipe_data: dict) -> tuple[list[dict], list[dict]]:
    items, lineage = [], []
    selector = recipe_data["selector"]
    window = recipe_data.get("context_window")
    for conversation in normalized:
        turns = conversation["turns"]
        targets = [i for i, turn in enumerate(turns) if turn["role"] == "assistant"]
        if selector == "final-assistant-reply":
            targets = targets[-1:]
        for index in targets:
            target = turns[index]
            prior = turns[:index] if window is None else turns[max(0, index - window):index]
            item_id = f"{conversation['conversation_id']}:{target['turn_id']}"
            items.append({"item_id": item_id, "source_snapshot_id": recipe_data["snapshot_id"],
                          "conversation_id": conversation["conversation_id"],
                          "split_group_id": conversation["split_group_id"],
                          "target_turn_id": target["turn_id"], "text": target["content"],
                          "context_prev": "\n".join(f"{turn['role']}: {turn['content']}" for turn in prior),
                          "unit_recipe_id": recipe_data["recipe_id"],
                          "source_ref": f"line:{conversation['source_line']}"})
            lineage.append({"item_id": item_id, "conversation_id": conversation["conversation_id"],
                            "source_line": conversation["source_line"], "target_turn_id": target["turn_id"]})
    if len({row["item_id"] for row in items}) != len(items):
        raise ValueError("unit recipe creates duplicate item IDs; source turn IDs must be unique")
    return items, lineage


def materialize(owner: Path, snapshot: str, recipe_id: str) -> dict:
    owner = owner.resolve()
    folder = owner / "versions" / snapshot
    normalized = _rows(folder / "normalized.private.jsonl")
    recipe_data = job.load_mapping(folder / "recipes" / f"{recipe_id}.yaml")
    if recipe_data.get("snapshot_id") != snapshot or recipe_data.get("recipe_id") != recipe_id:
        raise ValueError("recipe does not bind the requested source snapshot")
    items, lineage = _candidate_rows(normalized, recipe_data)
    if not items:
        raise ValueError("recipe produced no assistant replies")
    data = _jsonl(items)
    itemset = "items-" + _digest(_bytes({"snapshot": snapshot, "recipe": recipe_id,
                                        "candidate_digest": _digest(data)}))[:16]
    for row in items:
        row["item_set_id"] = itemset
    data = _jsonl(items)
    target = folder / "itemsets" / itemset
    manifest = {"schema": "subjective-label/item-set-v1", "item_set_id": itemset,
                "snapshot_id": snapshot, "recipe_id": recipe_id, "n_items": len(items),
                "candidate_digest": _digest(data), "lineage_digest": _digest(_jsonl(lineage))}
    return {"item_set_id": itemset, **_run(owner, "unit-materialize", recipe_id,
        inputs={"snapshot_id": snapshot, "recipe_id": recipe_id},
        artifacts={target / "items.private.jsonl": data, target / "lineage.private.jsonl": _jsonl(lineage),
                   target / "manifest.public.json": job.json_bytes(manifest)},
        receipt={"item_set_id": itemset, "accepted": True, "n_items": len(items)})}


def check(owner: Path, snapshot: str, itemset: str) -> dict:
    owner = owner.resolve()
    folder = owner / "versions" / snapshot
    target = folder / "itemsets" / itemset
    manifest = job.load_mapping(target / "manifest.public.json")
    recipe_data = job.load_mapping(folder / "recipes" / f"{manifest['recipe_id']}.yaml")
    normalized = _rows(folder / "normalized.private.jsonl")
    actual = _rows(target / "items.private.jsonl")
    expected, lineage = _candidate_rows(normalized, recipe_data)
    for row in expected:
        row["item_set_id"] = itemset
    if _jsonl(actual) != _jsonl(expected) or len(actual) != manifest["n_items"]:
        raise RuntimeError("candidate item set differs from source and frozen recipe")
    if _digest(_jsonl(actual)) != manifest["candidate_digest"]:
        raise RuntimeError("candidate item-set digest differs from manifest")
    if _digest(_jsonl(lineage)) != manifest["lineage_digest"]:
        raise RuntimeError("candidate lineage differs from manifest")
    report = {"schema": "subjective-label/unit-check-v1", "status": "accepted",
              "snapshot_id": snapshot, "item_set_id": itemset, "recipe_id": manifest["recipe_id"],
              "candidate_digest": manifest["candidate_digest"], "n_items": len(actual),
              "n_groups": len({row["split_group_id"] for row in actual}),
              "checks": ["unique IDs", "target and earlier context", "source lineage", "stable leakage groups"]}
    return {"item_set_id": itemset, **_run(owner, "unit-check", itemset,
        inputs={"candidate_digest": manifest["candidate_digest"]},
        artifacts={target / "qa.public.json": job.json_bytes(report)},
        receipt={"item_set_id": itemset, "accepted": True, "n_items": len(actual)})}


def reserve(owner: Path, snapshot: str, itemset: str, config_path: Path,
            sealed_groups: int, seed: int, custodian: str) -> dict:
    owner = owner.resolve()
    folder = owner / "versions" / snapshot
    target = folder / "itemsets" / itemset
    source_manifest = job.load_mapping(folder / "manifest.public.json")
    manifest = job.load_mapping(target / "manifest.public.json")
    qa = job.load_mapping(target / "qa.public.json")
    if qa.get("status") != "accepted" or qa.get("candidate_digest") != manifest.get("candidate_digest"):
        raise RuntimeError("an accepted QA receipt bound to this item set is required")
    normalized = _rows(folder / "normalized.private.jsonl")
    items = _rows(target / "items.private.jsonl")
    if (_digest(_jsonl(normalized)) != source_manifest.get("normalized_digest")
            or manifest.get("snapshot_id") != snapshot or qa.get("item_set_id") != itemset):
        raise RuntimeError("source snapshot, item set, and QA do not bind the same inputs")
    if _digest(_jsonl(items)) != manifest["candidate_digest"]:
        raise RuntimeError("candidate items changed after QA")
    groups = sorted({row["split_group_id"] for row in normalized})
    if not 0 < sealed_groups < len(groups):
        raise ValueError("sealed_groups must leave at least one source group on each side")
    if not custodian.strip():
        raise ValueError("custodian must be named")
    config = job.load_mapping(config_path)
    if not isinstance(config.get("corpus"), dict):
        config["corpus"] = {}
    selected = set(random.Random(seed).sample(groups, sealed_groups))
    protected_rows = []
    eligible_rows = []
    for row in items:
        text_hash = _digest(row["text"].encode("utf-8"))
        if row["split_group_id"] in selected:
            protected_rows.append({"item_id": row["item_id"], "text_hash": text_hash})
        else:
            eligible_rows.append({**row, "population_status": "eligible", "text_hash": text_hash})
    if not protected_rows or not eligible_rows:
        raise RuntimeError("group reservation needs at least one sealed and one development item")
    partition = "partition-" + _digest(_bytes({"snapshot": snapshot, "groups": groups,
                                               "sealed_groups": sealed_groups, "seed": seed,
                                               "group_field": "split_group_id"}))[:16]
    partition_dir = owner / "partitions" / partition
    package = owner / "packages" / f"{itemset}-{partition}"
    eligible_data = _jsonl(eligible_rows)
    protected_data = _jsonl(sorted(protected_rows, key=lambda r: r["item_id"]))
    protected_groups = _jsonl([{"split_group_id": g, "partition": "sealed" if g in selected else "development"}
                               for g in groups])
    frame = {"schema": "subjective-label/group-frame-v1", "partition_id": partition,
             "snapshot_id": snapshot, "source_group_count": len(groups),
             "development_group_count": len(groups) - sealed_groups,
             "sealed_group_count": sealed_groups, "seed": seed,
             "group_field": "split_group_id", "protected_group_digest": _digest(protected_groups)}
    config["corpus"].update({"path": "corpus/items.jsonl", "id_field": "item_id",
                             "text_field": "text", "context_field": "context_prev"})
    corpus_manifest = {"schema_version": "subjective-label/fenced-corpus-v1",
                       "items_file": "corpus/items.jsonl", "n_items": len(eligible_rows),
                       "n_eligible": len(eligible_rows), "n_sealed": len(protected_rows),
                       "n_source_items": len(items), "id_field": "item_id", "text_field": "text",
                       "context_field": "context_prev", "population": "one frozen assistant reply",
                       "source": {"name": source_manifest["source_id"]},
                       "partition_id": partition, "item_set_id": itemset}
    status = {"schema_version": "subjective-label/sealed-v2", "status": "reserved",
              "custodian": custodian, "invalidation_state": "valid", "n_items": len(protected_rows),
              "frame": {"rule": "seeded draw of whole source groups", "sampling": "seeded_random_groups",
                        "seed": seed, "partition_id": partition, "n_source_groups": len(groups),
                        "n_sealed_groups": sealed_groups},
              "access_policy": ["no development read, embed, index, retrieve, dedup, or prelabel",
                                "release only after G* freezes, by the custodian"],
              "text_location": "source custody only; no sealed text in fenced package"}
    receipt = {"schema": "subjective-label/preparation-receipt-v2", "status": "accepted",
               "owner": str(owner), "snapshot_id": snapshot, "recipe_id": manifest["recipe_id"],
               "item_set_id": itemset, "partition_id": partition,
               "source_manifest_digest": _digest((folder / "manifest.public.json").read_bytes()),
               "normalized_digest": source_manifest["normalized_digest"],
               "recipe_digest": _digest((folder / "recipes" / f"{manifest['recipe_id']}.yaml").read_bytes()),
               "item_set_manifest_digest": _digest((target / "manifest.public.json").read_bytes()),
               "candidate_digest": manifest["candidate_digest"],
               "qa_digest": _digest((target / "qa.public.json").read_bytes()),
               "frame_digest": _digest(job.json_bytes(frame)),
               "eligible_digest": _digest(eligible_data), "protected_digest": _digest(protected_data),
               "config_digest": _digest(job.yaml_bytes(config)),
               "corpus_manifest_digest": _digest(job.json_bytes(corpus_manifest)),
               "sealed_status_digest": _digest(job.json_bytes(status)),
               "n_eligible": len(eligible_rows), "n_sealed": len(protected_rows),
               "group_disjointness": "passed"}
    artifacts = {
        partition_dir / "frame.public.json": job.json_bytes(frame),
        partition_dir / "frame.protected.jsonl": protected_groups,
        package / "config.yaml": job.yaml_bytes(config),
        package / "corpus" / "items.jsonl": eligible_data,
        package / "corpus" / "manifest.json": job.json_bytes(corpus_manifest),
        package / "test" / "sealed" / "status.json": job.json_bytes(status),
        package / "test" / "sealed" / "manifest.protected.jsonl": protected_data,
        package / "preparation-receipt.json": job.json_bytes(receipt),
    }
    result = _run(owner, "initial-group-reserve", itemset,
        inputs={"snapshot_id": snapshot, "item_set_id": itemset, "seed": seed,
                "sealed_groups": sealed_groups, "config_path": str(config_path.resolve()),
                "config_digest": _digest(config_path.read_bytes()), "custodian": custodian},
        artifacts=artifacts, receipt={"partition_id": partition, "package": str(package),
                                      "accepted": True, "n_eligible": len(eligible_rows),
                                      "n_sealed": len(protected_rows)})
    return {"package": str(package), "partition_id": partition, **result}


def _verify_legacy_package(package: Path, owner: Path, receipt: dict) -> dict:
    """Read early v1 packages without rewriting their accepted receipts."""
    snapshot, itemset, partition = (receipt[key] for key in
                                    ("snapshot_id", "item_set_id", "partition_id"))
    checks = (
        (owner / "versions" / snapshot / "itemsets" / itemset / "qa.public.json", "qa_digest"),
        (owner / "partitions" / partition / "frame.public.json", "frame_digest"),
        (package / "corpus" / "items.jsonl", "eligible_digest"),
        (package / "test" / "sealed" / "manifest.protected.jsonl", "protected_digest"),
    )
    for path, field in checks:
        if not path.is_file() or _digest(path.read_bytes()) != receipt.get(field):
            raise RuntimeError(f"preparation binding mismatch: {field}")
    qa, frame = job.load_mapping(checks[0][0]), job.load_mapping(checks[1][0])
    protected_groups = owner / "partitions" / partition / "frame.protected.jsonl"
    if (not protected_groups.is_file()
            or _digest(protected_groups.read_bytes()) != frame.get("protected_group_digest")):
        raise RuntimeError("protected group frame differs from its public receipt")
    status = job.load_mapping(package / "test" / "sealed" / "status.json")
    manifest = job.load_mapping(package / "corpus" / "manifest.json")
    if (qa.get("status") != "accepted" or qa.get("item_set_id") != itemset
            or frame.get("partition_id") != partition
            or status.get("frame", {}).get("partition_id") != partition
            or manifest.get("partition_id") != partition or manifest.get("item_set_id") != itemset
            or manifest.get("n_eligible") != receipt.get("n_eligible")
            or manifest.get("n_sealed") != receipt.get("n_sealed")
            or receipt.get("group_disjointness") != "passed"):
        raise RuntimeError("legacy preparation receipt, QA, frame, and package disagree")
    return receipt


def verify_package(package: Path) -> dict:
    package = package.resolve()
    receipt = job.load_mapping(package / "preparation-receipt.json")
    if (receipt.get("schema") not in {"subjective-label/preparation-receipt-v1",
                                       "subjective-label/preparation-receipt-v2"}
            or receipt.get("status") != "accepted"):
        raise RuntimeError("source package lacks an accepted preparation receipt")
    owner = Path(str(receipt.get("owner") or "")).resolve()
    snapshot = str(receipt["snapshot_id"])
    itemset = str(receipt["item_set_id"])
    partition = str(receipt["partition_id"])
    expected_package = owner / "packages" / f"{itemset}-{partition}"
    if package != expected_package:
        raise RuntimeError("preparation receipt does not identify this package")
    if receipt["schema"] == "subjective-label/preparation-receipt-v1":
        return _verify_legacy_package(package, owner, receipt)
    checks = (
        (owner / "versions" / snapshot / "manifest.public.json", "source_manifest_digest"),
        (owner / "versions" / snapshot / "normalized.private.jsonl", "normalized_digest"),
        (owner / "versions" / snapshot / "recipes" / f"{receipt['recipe_id']}.yaml", "recipe_digest"),
        (owner / "versions" / snapshot / "itemsets" / itemset / "manifest.public.json", "item_set_manifest_digest"),
        (owner / "versions" / snapshot / "itemsets" / itemset / "items.private.jsonl", "candidate_digest"),
        (owner / "versions" / snapshot / "itemsets" / itemset / "qa.public.json", "qa_digest"),
        (owner / "partitions" / partition / "frame.public.json", "frame_digest"),
        (package / "config.yaml", "config_digest"),
        (package / "corpus" / "items.jsonl", "eligible_digest"),
        (package / "corpus" / "manifest.json", "corpus_manifest_digest"),
        (package / "test" / "sealed" / "status.json", "sealed_status_digest"),
        (package / "test" / "sealed" / "manifest.protected.jsonl", "protected_digest"),
    )
    for path, field in checks:
        if not path.is_file() or _digest(path.read_bytes()) != receipt.get(field):
            raise RuntimeError(f"preparation binding mismatch: {field}")
    source_manifest = job.load_mapping(checks[0][0])
    if job.load_mapping(owner / "source.yaml") != _owner_record(owner, source_manifest["source_id"]):
        raise RuntimeError("preparation owner disagrees with its source snapshot")
    normalized = _rows(checks[1][0])
    recipe_data = job.load_mapping(checks[2][0])
    item_manifest = job.load_mapping(checks[3][0])
    items = _rows(checks[4][0])
    qa = job.load_mapping(checks[5][0])
    frame = job.load_mapping(checks[6][0])
    protected_groups = owner / "partitions" / partition / "frame.protected.jsonl"
    if (not protected_groups.is_file()
            or _digest(protected_groups.read_bytes()) != frame.get("protected_group_digest")):
        raise RuntimeError("protected group frame differs from its public receipt")
    status = job.load_mapping(package / "test" / "sealed" / "status.json")
    manifest = job.load_mapping(package / "corpus" / "manifest.json")
    if (qa.get("status") != "accepted" or qa.get("item_set_id") != itemset
            or source_manifest.get("snapshot_id") != snapshot
            or source_manifest.get("n_conversations") != len(normalized)
            or recipe_data.get("snapshot_id") != snapshot or recipe_data.get("recipe_id") != receipt["recipe_id"]
            or item_manifest.get("snapshot_id") != snapshot or item_manifest.get("item_set_id") != itemset
            or item_manifest.get("recipe_id") != receipt["recipe_id"]
            or item_manifest.get("candidate_digest") != receipt["candidate_digest"]
            or qa.get("candidate_digest") != receipt["candidate_digest"]
            or frame.get("partition_id") != partition
            or frame.get("snapshot_id") != snapshot
            or status.get("frame", {}).get("partition_id") != partition
            or status.get("n_items") != receipt.get("n_sealed")
            or manifest.get("partition_id") != partition or manifest.get("item_set_id") != itemset
            or manifest.get("n_eligible") != receipt.get("n_eligible")
            or manifest.get("n_sealed") != receipt.get("n_sealed")
            or manifest.get("n_source_items") != len(items)
            or receipt.get("group_disjointness") != "passed"):
        raise RuntimeError("preparation receipt, QA, frame, and fenced package disagree")
    expected, _ = _candidate_rows(normalized, recipe_data)
    for row in expected:
        row["item_set_id"] = itemset
    if expected != items or len(items) != item_manifest.get("n_items"):
        raise RuntimeError("prepared items disagree with the normalized source and unit recipe")
    groups = sorted({row["split_group_id"] for row in normalized})
    sealed_groups = frame.get("sealed_group_count")
    seed = frame.get("seed")
    if (not isinstance(sealed_groups, int) or not isinstance(seed, int)
            or not 0 < sealed_groups < len(groups)
            or source_manifest.get("n_groups") != len(groups)
            or frame.get("source_group_count") != len(groups)
            or frame.get("development_group_count") != len(groups) - sealed_groups):
        raise RuntimeError("invalid source-group reservation frame")
    selected = set(random.Random(seed).sample(groups, sealed_groups))
    expected_groups = [{"split_group_id": group,
                        "partition": "sealed" if group in selected else "development"}
                       for group in groups]
    if _rows(protected_groups) != expected_groups:
        raise RuntimeError("source-group reservation differs from the protected frame")
    expected_eligible, expected_protected = [], []
    for row in items:
        text_hash = _digest(row["text"].encode("utf-8"))
        if row["split_group_id"] in selected:
            expected_protected.append({"item_id": row["item_id"], "text_hash": text_hash})
        else:
            expected_eligible.append({**row, "population_status": "eligible", "text_hash": text_hash})
    expected_protected.sort(key=lambda row: row["item_id"])
    if (_rows(package / "corpus" / "items.jsonl") != expected_eligible
            or _rows(package / "test" / "sealed" / "manifest.protected.jsonl") != expected_protected
            or len(expected_eligible) != receipt["n_eligible"]
            or len(expected_protected) != receipt["n_sealed"]):
        raise RuntimeError("fenced package disagrees with the source-group reservation")
    return receipt


def preparation_reference(owner: Path, package: Path, receipt: dict) -> dict:
    wanted = (
        ("source-normalize", "snapshot_id", receipt["snapshot_id"]),
        ("unit-recipe", "recipe_id", receipt["recipe_id"]),
        ("unit-materialize", "item_set_id", receipt["item_set_id"]),
        ("unit-check", "item_set_id", receipt["item_set_id"]),
        ("initial-group-reserve", "partition_id", receipt["partition_id"]),
    )
    upstream_runs = []
    for operation, field, value in wanted:
        candidates = []
        for path in (owner / "runs").glob("*.yaml"):
            result_path = owner / "results" / path.stem / "result.yaml"
            if not result_path.is_file():
                continue
            try:
                result = job.load_mapping(result_path)
            except (OSError, ValueError, yaml.YAMLError):
                continue
            if (result.get("operation") == operation and result.get(field) == value
                    and result.get("status") == "complete"):
                candidates.append(path)
        if not candidates:
            raise RuntimeError(f"accepted preparation has no {operation} Result")
        upstream_runs.append(sorted(candidates, key=lambda p: (p.stat().st_mtime_ns, p.name))[-1].stem)
    return {"schema": "subjective-label/preparation-ref-v1", "owner": str(owner.resolve()),
            "package": str(package.resolve()),
            "receipt": str((package / "preparation-receipt.json").resolve()),
            "snapshot_id": receipt["snapshot_id"], "recipe_id": receipt["recipe_id"],
            "item_set_id": receipt["item_set_id"], "partition_id": receipt["partition_id"],
            "qa_digest": receipt["qa_digest"], "frame_digest": receipt["frame_digest"],
            "eligible_digest": receipt["eligible_digest"], "upstream_runs": upstream_runs}


def link(owner: Path, package: Path, page_file: Path) -> dict:
    owner = owner.resolve()
    receipt = verify_package(package)
    if Path(receipt["owner"]).resolve() != owner:
        raise RuntimeError("package is not owned by this Corpus Preparation folder")
    page_file = job.require_page_folder(page_file)
    source = job.load_mapping(owner / "versions" / receipt["snapshot_id"] / "manifest.public.json")
    owner_record = _owner_record(owner, source["source_id"])
    source_file = owner / "source.yaml"
    if source_file.exists() and job.load_mapping(source_file) != owner_record:
        raise RuntimeError("preparation owner no longer matches its source snapshot")
    page_owner_ref = page_file.parent / "labeling" / "preparation-owner.yaml"
    owner_reference = {**owner_record, "owner": str(owner)}
    if page_owner_ref.exists() and job.load_mapping(page_owner_ref) != owner_reference:
        raise RuntimeError("Page is already attached to another preparation owner")
    page_ref = page_file.parent / "labeling" / "preparation-ref.yaml"
    reference = preparation_reference(owner, package, receipt)
    if (page_file.parent / "labeling" / "config.yaml").is_file() and not page_ref.is_file():
        raise RuntimeError("cannot add preparation provenance after a Labeling Contract")
    if page_ref.exists() and job.load_mapping(page_ref) != reference:
        raise RuntimeError("Page is already linked to another preparation package")
    job.write_once(source_file, job.yaml_bytes(owner_record))
    job.write_once(page_owner_ref, job.yaml_bytes(owner_reference))
    job.write_once(page_ref, job.yaml_bytes(reference))
    return {"page": str(page_file), "preparation_ref": str(page_ref), "package": str(package)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    att = commands.add_parser("attach")
    att.add_argument("--owner", type=Path, required=True)
    att.add_argument("--source-id", required=True)
    att.add_argument("--page-file", type=Path, required=True)
    norm = commands.add_parser("normalize")
    norm.add_argument("--owner", type=Path, required=True)
    norm.add_argument("--raw", type=Path, required=True)
    norm.add_argument("--source-id", required=True)
    rec = commands.add_parser("recipe")
    rec.add_argument("--owner", type=Path, required=True)
    rec.add_argument("--snapshot", required=True)
    rec.add_argument("--selector", choices=("final-assistant-reply", "every-assistant-reply"), required=True)
    rec.add_argument("--context-window", type=int)
    rec.add_argument("--accepted-by", required=True)
    mat = commands.add_parser("materialize")
    mat.add_argument("--owner", type=Path, required=True)
    mat.add_argument("--snapshot", required=True)
    mat.add_argument("--recipe", required=True)
    qa = commands.add_parser("check")
    qa.add_argument("--owner", type=Path, required=True)
    qa.add_argument("--snapshot", required=True)
    qa.add_argument("--itemset", required=True)
    res = commands.add_parser("reserve")
    res.add_argument("--owner", type=Path, required=True)
    res.add_argument("--snapshot", required=True)
    res.add_argument("--itemset", required=True)
    res.add_argument("--config", type=Path, required=True)
    res.add_argument("--sealed-groups", type=int, required=True)
    res.add_argument("--seed", type=int, required=True)
    res.add_argument("--custodian", required=True)
    link_cmd = commands.add_parser("link")
    link_cmd.add_argument("--owner", type=Path, required=True)
    link_cmd.add_argument("--package", type=Path, required=True)
    link_cmd.add_argument("--page-file", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "attach":
        output = attach(args.owner, args.source_id, args.page_file)
    elif args.command == "normalize":
        output = normalize(args.owner, args.raw, args.source_id)
    elif args.command == "recipe":
        output = recipe(args.owner, args.snapshot, args.selector, args.context_window, args.accepted_by)
    elif args.command == "materialize":
        output = materialize(args.owner, args.snapshot, args.recipe)
    elif args.command == "check":
        output = check(args.owner, args.snapshot, args.itemset)
    elif args.command == "reserve":
        output = reserve(args.owner, args.snapshot, args.itemset, args.config,
                         args.sealed_groups, args.seed, args.custodian)
    else:
        output = link(args.owner, args.package, args.page_file)
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
