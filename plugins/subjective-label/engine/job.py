#!/usr/bin/env python3
"""Canonical P0 Contract API for one subjective-label job.

The API imports one already-fenced corpus snapshot and its sealed-test
reservation into a page-local ``labeling/`` lane. Legacy snapshots may still
contain sealed rows inline; those rows are removed before the Page corpus is
written, and custody is normalized to sealed IDs and text hashes. The API
deliberately creates no round, no human gold, and no claim that the seed policy
is mature.

The writer is additive and idempotent: an existing identical artifact is
accepted, while an existing different artifact is never overwritten.

No record carries a content hash (JL 260928).  Integrity is presence, parse,
and content: the P0 files exist and parse, their counts agree with the corpus
and the sealed custody, and a meaning confirmation stores a snapshot of what
the human confirmed, compared by value to the current configuration.  The one
hash kept is the item-level ``text_hash`` data column, which lets sealed
custody name its items without storing their text.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml


P0_FILES = (
    "config.yaml",
    "corpus/manifest.json",
    "test/sealed/status.json",
    "register.md",
    "policy/versions/G_00/manifest.yaml",
)
REGIONS = ("H", "L", "N", "HL", "LN", "HN", "HLN")
MEANING_REVISIONS = "gates/meaning-revisions"  # one JSON per human-decided change to the label meanings
MEANING_REVISION_SCHEMA = "subjective-label-meaning-revision/v1"
POLICY_COMPONENTS = (
    "guideline.md",
    "boundaries.yaml",
    "procedure.yaml",
    "uncertainty.yaml",
    "casebook.jsonl",
    "diff.yaml",
    "regression.jsonl",
    "cheatsheet.md",
    "gallery.md",
)


def sha256_bytes(data: bytes) -> str:
    """The item-level ``text_hash`` data column and internal cache keys only; never a record pin."""
    return hashlib.sha256(data).hexdigest()


def yaml_bytes(value: Any) -> bytes:
    return yaml.safe_dump(
        value, sort_keys=False, allow_unicode=True, default_flow_style=False
    ).encode("utf-8")


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode(
        "utf-8"
    )


def drop_checksum_fields(value: Any) -> Any:
    """Copy a record without any legacy ``*checksum*`` or ``*sha256*`` field, at any depth."""
    if isinstance(value, dict):
        return {
            key: drop_checksum_fields(item)
            for key, item in value.items()
            if "checksum" not in str(key).lower() and "sha256" not in str(key).lower()
        }
    if isinstance(value, list):
        return [drop_checksum_fields(item) for item in value]
    return copy.deepcopy(value)


def write_once(path: Path, data: bytes) -> bool:
    """Write one immutable artifact; refuse an in-place semantic change."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if not path.is_file() or path.read_bytes() != data:
            raise RuntimeError(f"refusing to overwrite changed artifact: {path}")
        return False
    path.write_bytes(data)
    return True


def load_mapping(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    if path.suffix == ".json":
        value = json.loads(path.read_text(encoding="utf-8"))
    else:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected mapping: {path}")
    return value


def try_load_mapping(path: Path) -> tuple[dict, str | None]:
    """Load one mapping for status derivation; report a defect instead of raising."""
    try:
        if path.is_symlink():
            return {}, f"refusing symlinked authority file: {path.name}"
        return load_mapping(path), None
    except FileNotFoundError:
        return {}, f"missing: {path.name}"
    except (OSError, ValueError, UnicodeError, yaml.YAMLError) as error:
        return {}, f"unreadable {path.name}: {type(error).__name__}"


def authority_hold(config: dict) -> tuple[bool, str]:
    """Require one named human semantic authority; local callers are not authenticated."""
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    human_id = str(authority.get("human_id") or "").strip()
    mode = str(authority.get("mode") or "")
    if config.get("simulation_only") is True or "simulation" in mode.lower():
        return True, "a simulation or proxy cannot create human gold"
    if mode == "external_annotation_import":
        return True, "imported source labels only; no local human authority is appointed"
    if not human_id:
        return True, "config does not name one identified human semantic authority"
    if mode != "single_human_semantic_authority" or authority.get("creates_human_gold") is not True:
        return True, "authority mode does not allow this human to create gold"
    return False, ""


def g0_passed(state: dict) -> bool:
    """Return the semantic G0 predicate; compatibility phase tags are ignored."""
    return bool(
        state.get("p0_contract_integrity_valid")
        and not state.get("hold")
        and state.get("meaning_receipt_valid")
        and state.get("g0_receipt_valid")
    )


def meaning_revisions(job_root: Path) -> list[dict]:
    """Every recorded change to the label meanings, oldest first (see ``revise_meanings``)."""
    base = Path(job_root) / MEANING_REVISIONS
    if not base.is_dir() or base.is_symlink():
        return []
    rows = [load_mapping(path) for path in base.glob("*.json") if not path.is_symlink()]
    return sorted(rows, key=lambda row: int(row.get("seq") or 0))


def _revision_chain_errors(config: dict, revisions: list[dict]) -> list[str]:
    """Each revision starts where the last one ended, and config.yaml holds the last one's wording."""
    errors = []
    for index, revision in enumerate(revisions, start=1):
        if revision.get("schema") != MEANING_REVISION_SCHEMA or revision.get("seq") != index:
            errors.append(f"meaning revision {index}: malformed or out of sequence")
        elif index > 1 and revision.get("before") != revisions[index - 2].get("after"):
            errors.append(f"meaning revision {index}: does not start from revision {index - 1}")
    labels = config.get("labels") if isinstance(config.get("labels"), dict) else {}
    if revisions and labels.get("meanings") != revisions[-1].get("after"):
        errors.append("label meanings in config.yaml differ from the last meaning revision")
    return errors


def _judged_items(job_root: Path) -> list[str]:
    """Items that already have a first or final answer, in any round."""
    judged = []
    for events in sorted((Path(job_root) / "rounds").glob("round_*/sessions/events.jsonl")):
        for line in events.read_text(encoding="utf-8").splitlines():
            if line.strip():
                event = json.loads(line)
                if event.get("kind") in {"first", "final"}:
                    judged.append(f'{events.parents[1].name}:{event.get("item_id")}')
    return sorted(set(judged))


def find_protected_manifest(sealed_dir: Path) -> Path:
    matches = sorted(
        path
        for path in sealed_dir.glob("manifest*")
        if path.is_file() and path.name != "manifest.json"
    )
    if len(matches) != 1:
        raise RuntimeError(
            f"expected exactly one opaque protected manifest in {sealed_dir}; "
            f"found {[path.name for path in matches]}"
        )
    return matches[0]


def page_root(job_root: Path) -> Path:
    """The Page folder around labeling/; it holds the job's runs/ and results/."""
    return Path(job_root).parent


def runs_dir(job_root: Path) -> Path:
    return page_root(job_root) / "runs"


def results_dir(job_root: Path) -> Path:
    return page_root(job_root) / "results"


def page_path(job_root: Path, rel: str) -> str:
    """A labeling/ file as a Run receipt names it: relative to the Page."""
    return f"{Path(job_root).name}/{rel}"


def validate_page_lane(page_file: Path, job_root: Path) -> Path:
    page_file = page_file.resolve()
    job_root = job_root.resolve()
    if not page_file.is_file():
        raise FileNotFoundError(f"Page source file not found: {page_file}")
    expected = page_file.parent / "labeling"
    if job_root != expected:
        raise RuntimeError(
            "canonical destination must be the supplied Page file's direct "
            f"labeling/ lane: expected {expected}, got {job_root}"
        )
    return page_file


def validate_source_fence(status: dict) -> None:
    """The source reservation names a custodian, a frame, a no-development policy, and is valid."""
    policies = status.get("access_policy")
    frame = status.get("frame")
    valid = (
        status.get("status") in {"reserved", "reserved-and-unexposed"}
        and status.get("custodian")
        and status.get("invalidation_state") == "valid"
        and isinstance(frame, dict)
        and bool(frame.get("rule"))
        and isinstance(policies, list)
        and any("no development" in str(rule).lower() for rule in policies)
    )
    if not valid:
        raise RuntimeError(
            "source sealed reservation lacks a valid custodian, exclusion policy, "
            "frame, or invalidation state"
        )


def _source_count(value: object, field: str, source: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise RuntimeError(f"source {source} {field} must be a non-negative integer")
    return value


def _declared_count(mapping: dict, fields: tuple[str, ...], source: str) -> int | None:
    values = [
        (field, _source_count(mapping.get(field), field, source))
        for field in fields if mapping.get(field) is not None
    ]
    distinct = {value for _, value in values}
    if len(distinct) > 1:
        raise RuntimeError(f"source {source} has inconsistent counts: {values}")
    return values[0][1] if values else None


def _protected_records(data: bytes) -> dict[str, str] | None:
    """Parse the supported ID/hash JSONL form; return None for opaque custody."""
    try:
        lines = data.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        return None
    records: dict[str, str] = {}
    saw_opaque = False
    saw_structured = False
    for line in lines:
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            if saw_structured:
                raise RuntimeError("source protected manifest mixes structured and opaque rows") from None
            return None
        if not isinstance(row, dict) or set(row) != {"item_id", "text_hash"}:
            if isinstance(row, dict) and ("item_id" in row or "text_hash" in row):
                raise RuntimeError("source protected manifest has a malformed ID/hash record")
            if saw_structured:
                raise RuntimeError("source protected manifest mixes structured and opaque rows")
            saw_opaque = True
            continue
        if saw_opaque:
            raise RuntimeError("source protected manifest mixes structured and opaque rows")
        raw_id = row.get("item_id")
        item_id = str(raw_id).strip() if raw_id is not None else ""
        raw_hash = row.get("text_hash")
        text_hash = str(raw_hash).strip().removeprefix("sha256:").lower() if raw_hash is not None else ""
        if not item_id or len(text_hash) != 64 or any(c not in "0123456789abcdef" for c in text_hash):
            raise RuntimeError("source protected manifest requires non-empty IDs and SHA-256 text hashes")
        if item_id in records:
            raise RuntimeError(f"source protected manifest repeats item_id {item_id!r}")
        records[item_id] = text_hash
        saw_structured = True
    if saw_opaque:
        return None
    return records


def _canonical_source_corpus(
    source_items: Path,
    source_config: dict,
    source_manifest: dict,
    protected_data: bytes,
    sealed_status: dict,
) -> tuple[bytes, bytes, int, int, int]:
    """Return eligible-only Page rows and normalized protected ID/hash JSONL.

    Older snapshots stored sealed rows in corpus/items.jsonl, while current
    snapshots keep only eligible rows and a structured protected manifest.
    Unmarked legacy rows can be classified only when the protected manifest
    identifies their IDs; an opaque manifest with an unresolved sealed count
    is refused rather than copied into a Page lane.
    """
    try:
        source_rows = [
            json.loads(line)
            for line in source_items.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"source corpus is unreadable: {type(error).__name__}") from None
    if any(not isinstance(row, dict) for row in source_rows):
        raise RuntimeError("source corpus rows must be JSON objects")

    corpus_cfg = source_config.get("corpus")
    if corpus_cfg is not None and not isinstance(corpus_cfg, dict):
        raise RuntimeError("source config.corpus must be a mapping")
    corpus_cfg = corpus_cfg if isinstance(corpus_cfg, dict) else {}
    config_text_field = corpus_cfg.get("text_field")
    manifest_text_field = source_manifest.get("text_field")
    if config_text_field and manifest_text_field and str(config_text_field) != str(manifest_text_field):
        raise RuntimeError("source config and corpus manifest disagree on text_field")
    text_field = str(config_text_field or manifest_text_field or "text")
    id_fields = tuple(dict.fromkeys(str(value) for value in (
        source_manifest.get("id_field"), corpus_cfg.get("id_field"), "item_id", "id"
    ) if value))
    text_hashes = _protected_records(protected_data)
    opaque = text_hashes is None
    text_hashes = dict(text_hashes or {})
    protected_ids = set(text_hashes)

    sealed_count = _declared_count(
        sealed_status, ("n_items", "n", "n_sealed", "sealed_count"), "sealed status"
    )
    manifest_sealed_count = _declared_count(
        source_manifest, ("n_sealed", "sealed_reserved_n", "sealed_count"), "corpus manifest"
    )
    declared_sealed_counts = {value for value in (sealed_count, manifest_sealed_count) if value is not None}
    if len(declared_sealed_counts) > 1:
        raise RuntimeError("source sealed status and corpus manifest disagree on sealed count")
    declared_sealed = next(iter(declared_sealed_counts), None)

    eligible: list[dict] = []
    seen_ids: set[str] = set()
    seen_protected_rows: set[str] = set()
    n_excluded = 0
    inline_sealed: dict[str, str] = {}
    for index, source in enumerate(source_rows, start=1):
        aliases: set[str] = set()
        for field in id_fields:
            raw_value = source.get(field)
            value = str(raw_value).strip() if raw_value is not None else ""
            if value:
                aliases.add(value)
        if not aliases:
            raise RuntimeError(f"source corpus row {index} has no non-empty item ID")
        item_id = next((str(source[field]).strip() for field in id_fields
                        if source.get(field) is not None and str(source[field]).strip()), "")
        if item_id in seen_ids:
            raise RuntimeError(f"source corpus repeats item_id {item_id!r}")
        seen_ids.add(item_id)
        text = source.get(text_field)
        if not isinstance(text, str) or not text.strip():
            raise RuntimeError(f"source item {item_id!r} has no non-empty {text_field!r}")
        text_hash = sha256_bytes(text.encode("utf-8"))
        status = source.get("population_status")
        if status not in (None, "eligible", "sealed", "excluded", "invalid"):
            raise RuntimeError(f"source item {item_id!r} has unsupported population_status {status!r}")
        if opaque and protected_data.strip() and status is None:
            raise RuntimeError(
                "opaque source protected manifest requires explicit population_status on every corpus row"
            )
        protected_matches = aliases & protected_ids
        if len(protected_matches) > 1:
            raise RuntimeError(f"source item {item_id!r} resolves to multiple protected IDs")
        if status == "eligible" and protected_matches:
            raise RuntimeError(f"source item {item_id!r} is eligible but appears in protected custody")
        if status in ("excluded", "invalid") and protected_matches:
            raise RuntimeError(f"source item {item_id!r} is excluded but appears in protected custody")

        is_sealed = status == "sealed" or bool(protected_matches)
        if status == "sealed" and not opaque and not protected_matches:
            raise RuntimeError(f"sealed source item {item_id!r} is absent from protected custody")
        if is_sealed:
            custody_id = sorted(protected_matches)[0] if protected_matches else item_id
            if custody_id in seen_protected_rows:
                raise RuntimeError(f"source repeats sealed item {custody_id!r}")
            seen_protected_rows.add(custody_id)
            prior_hash = text_hashes.get(custody_id)
            if prior_hash is not None and prior_hash != text_hash:
                raise RuntimeError(f"sealed item {custody_id!r} text hash disagrees with protected custody")
            if custody_id in inline_sealed and inline_sealed[custody_id] != text_hash:
                raise RuntimeError(f"sealed item {custody_id!r} has conflicting source text")
            inline_sealed[custody_id] = text_hash
            if prior_hash is None:
                text_hashes[custody_id] = text_hash
            continue
        if status in ("excluded", "invalid"):
            n_excluded += 1
            continue
        row = dict(source)
        row["item_id"] = item_id
        row["population_status"] = "eligible"
        row["text_hash"] = text_hash
        eligible.append(row)

    if opaque and protected_data.strip() and not inline_sealed:
        raise RuntimeError(
            "opaque source protected manifest cannot be resolved to corpus rows; refusing to import"
        )
    if opaque and protected_data.strip() and declared_sealed is None:
        raise RuntimeError("opaque source protected manifest has no verifiable sealed count")
    if declared_sealed is not None and declared_sealed != len(text_hashes):
        raise RuntimeError(
            f"source declares {declared_sealed} sealed items but protected custody resolves {len(text_hashes)}"
        )
    if declared_sealed is not None and opaque and protected_data.strip() and declared_sealed != len(inline_sealed):
        raise RuntimeError(
            f"opaque source custody declares {declared_sealed} sealed items but only {len(inline_sealed)} inline sealed rows are resolvable"
        )

    declared_eligible = _declared_count(
        source_manifest, ("n_eligible", "development_pool_n"), "corpus manifest"
    )
    if declared_eligible is not None and declared_eligible != len(eligible):
        raise RuntimeError(
            f"source declares {declared_eligible} eligible items but resolves {len(eligible)}"
        )
    resolved_source_total = len(eligible) + len(text_hashes) + n_excluded
    declared_total = _declared_count(source_manifest, ("n_items",), "corpus manifest")
    if declared_total is not None and declared_total not in {
        len(source_rows), len(eligible), resolved_source_total
    }:
        raise RuntimeError(
            f"source declares {declared_total} corpus items but contains {len(source_rows)} rows and resolves {resolved_source_total} total ({len(eligible)} eligible)"
        )
    declared_source_total = _declared_count(source_manifest, ("n_source_items",), "corpus manifest")
    if declared_source_total is not None and declared_source_total != resolved_source_total:
        raise RuntimeError(
            "source corpus manifest n_source_items does not match eligible, sealed, and excluded records"
        )

    eligible_bytes = "".join(
        json.dumps(row, ensure_ascii=False) + "\n" for row in eligible
    ).encode("utf-8")
    protected_bytes = "".join(
        json.dumps({"item_id": item_id, "text_hash": digest}, sort_keys=True) + "\n"
        for item_id, digest in sorted(text_hashes.items())
    ).encode("utf-8")
    return eligible_bytes, protected_bytes, len(eligible), len(text_hashes), resolved_source_total


def policy_version(job_root: Path) -> str | None:
    """The seed policy's version name from its manifest; None when the manifest is absent."""
    manifest = Path(job_root) / "policy" / "versions" / "G_00" / "manifest.yaml"
    if not manifest.is_file() or manifest.is_symlink():
        return None
    value, error = try_load_mapping(manifest)
    if error:
        return None
    return str(value.get("policy_id") or "G_00")


def semantic_bindings(config: dict, policy: str | None) -> dict:
    """What the human confirms, as a content snapshot compared by value (no hash)."""
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    labels = config.get("labels") if isinstance(config.get("labels"), dict) else {}
    regions = config.get("regions") if isinstance(config.get("regions"), dict) else {}
    uncertainty = (
        config.get("uncertainty") if isinstance(config.get("uncertainty"), dict) else {}
    )
    return {
        "construct": copy.deepcopy(construct),
        "labels": copy.deepcopy(labels),
        "regions": copy.deepcopy(regions),
        "uncertainty": copy.deepcopy(uncertainty),
        "unresolved_disposition": {
            "unresolved_is_label": uncertainty.get("unresolved_is_label"),
            "none_value": labels.get("none_value"),
        },
        "policy_version": policy,
    }


def runtime_timestamp(value: str) -> str:
    """Normalize a date or datetime to an offset-bearing runtime timestamp."""
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.astimezone()
    return parsed.isoformat(timespec="seconds")


def _meaning_receipt_bound(config: dict, job_root: Path) -> bool:
    """The receipt still describes the current meanings: its snapshot equals the config by value."""
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    receipt = authority.get("meaning_receipt")
    policy = policy_version(job_root)
    return bool(
        authority.get("meaning_confirmed") is True
        and isinstance(receipt, dict)
        and receipt.get("schema") == "subjective-label-meaning-confirmation/v1"
        and receipt.get("status") == "confirmed"
        and receipt.get("human_id") == authority.get("human_id")
        and receipt.get("confirmed_at")
        and policy is not None
        and receipt.get("bindings") == semantic_bindings(config, policy)
    )


G0_RECEIPT_SCHEMA = "subjective-label-g0-receipt/v1"


def g0_receipt_for(meaning_receipt: dict) -> dict:
    """The G0 receipt that matches one meaning receipt: same human, time, and content snapshot."""
    return {
        "schema": G0_RECEIPT_SCHEMA,
        "status": "passed",
        "human_id": meaning_receipt.get("human_id"),
        "confirmed_at": meaning_receipt.get("confirmed_at"),
        "bindings": copy.deepcopy(meaning_receipt.get("bindings")),
    }


def _g0_receipt_matches(g0_receipt: dict, meaning_receipt: object, human_id: object) -> bool:
    return bool(
        isinstance(meaning_receipt, dict)
        and g0_receipt.get("schema") == G0_RECEIPT_SCHEMA
        and g0_receipt.get("status") == "passed"
        and g0_receipt.get("human_id") == human_id
        and g0_receipt.get("human_id") == meaning_receipt.get("human_id")
        and g0_receipt.get("confirmed_at")
        and g0_receipt.get("confirmed_at") == meaning_receipt.get("confirmed_at")
        and g0_receipt.get("bindings") == meaning_receipt.get("bindings")
    )


def _g0_history_path(job_root: Path, data: bytes) -> Path:
    """Where a retired G0 receipt is archived: gates/g0/history/<timestamp>.json, never a hash."""
    base = Path(job_root) / "gates" / "g0" / "history"
    stamp = datetime.now().astimezone().strftime("%Y%m%dT%H%M%S")
    candidate = base / f"{stamp}.json"
    counter = 2
    while candidate.exists() and candidate.read_bytes() != data:
        candidate = base / f"{stamp}-{counter}.json"
        counter += 1
    return candidate


def _meaning_receipt_valid(config: dict, job_root: Path) -> bool:
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    receipt = authority.get("meaning_receipt")
    return bool(
        _meaning_receipt_bound(config, job_root)
        and isinstance(receipt, dict)
        and receipt.get("identity_assurance") == "caller_attested_not_authenticated"
    )


def default_policy_component(name: str, target: str) -> bytes:
    if name == "guideline.md":
        return (
            f"# G_00 · {target}\n\n"
            "Seed policy only. One identified human must confirm the target, "
            "class meanings, and boundary questions before Round 1.\n"
        ).encode("utf-8")
    if name == "boundaries.yaml":
        return yaml_bytes({"status": "open", "regions": list(REGIONS)})
    if name == "procedure.yaml":
        return yaml_bytes({"status": "seed", "steps": ["inspect evidence", "decide class", "record uncertainty"]})
    if name == "uncertainty.yaml":
        return yaml_bytes({"required": True, "unresolved_is_not_none": True})
    if name == "diff.yaml":
        return yaml_bytes({"from": None, "to": "G_00", "kind": "contract-seed"})
    if name == "cheatsheet.md":
        return f"# G_00 cheatsheet · {target}\n\nHuman meaning confirmation pending.\n".encode("utf-8")
    if name == "gallery.md":
        return b"# G_00 gallery\n\nNo human-confirmed examples exist at P0.\n"
    return b""


def create_contract(
    *,
    source_job: Path,
    job_root: Path,
    page_file: Path,
    job_id: str,
    target: str,
    human_id: str,
    created_at: str,
) -> dict:
    source_job = source_job.resolve()
    job_root = job_root.resolve()
    page_file = validate_page_lane(page_file, job_root)
    if source_job == job_root:
        raise RuntimeError("source job and destination job root must differ")

    source_config = load_mapping(source_job / "config.yaml")
    source_corpus_manifest = load_mapping(source_job / "corpus" / "manifest.json")
    source_items = source_job / "corpus" / "items.jsonl"
    source_sealed_status = load_mapping(source_job / "test" / "sealed" / "status.json")
    source_protected = find_protected_manifest(source_job / "test" / "sealed")
    source_policy = source_job / "policy" / "versions" / "G_00"
    if not source_items.is_file():
        raise FileNotFoundError(source_items)

    validate_source_fence(source_sealed_status)
    # Counts, not hashes, bind the source: _canonical_source_corpus refuses any
    # declared eligible, sealed, or total count the rows do not resolve to.
    items_data, protected_data, n_eligible, n_sealed, n_source_items = _canonical_source_corpus(
        source_items, source_config, source_corpus_manifest,
        source_protected.read_bytes(), source_sealed_status,
    )

    config = drop_checksum_fields(source_config)
    config["schema_version"] = "subjective-label/v2"
    config["simulation_only"] = False
    project = config.setdefault("project", {})
    if not isinstance(project, dict):
        project = config["project"] = {}
    project["id"] = job_id
    project["board_page"] = page_file.stem
    project["page_file"] = os.path.relpath(page_file, job_root.resolve())
    construct = config.setdefault("construct", {})
    if not isinstance(construct, dict):
        construct = config["construct"] = {}
    construct["name"] = target
    authority = config.setdefault("authority", {})
    if not isinstance(authority, dict):
        authority = config["authority"] = {}
    authority.update(
        {
            "human_id": human_id,
            "mode": "single_human_semantic_authority",
            "creates_human_gold": True,
            "meaning_confirmed": False,
            "meaning_receipt": None,
        }
    )
    config["contract_import"] = {
        "source_job": source_job.name,
        "created_at": created_at,
    }

    corpus_cfg = config.get("corpus")
    if corpus_cfg is not None and not isinstance(corpus_cfg, dict):
        raise RuntimeError("source config.corpus must be a mapping")
    corpus_cfg = corpus_cfg if isinstance(corpus_cfg, dict) else {}
    corpus_cfg["path"] = "corpus/items.jsonl"
    corpus_cfg["id_field"] = "item_id"
    corpus_cfg["text_field"] = corpus_cfg.get("text_field") or source_corpus_manifest.get("text_field") or "text"
    if not corpus_cfg.get("context_field") and source_corpus_manifest.get("context_field"):
        corpus_cfg["context_field"] = source_corpus_manifest["context_field"]
    config["corpus"] = corpus_cfg

    corpus_manifest = drop_checksum_fields(source_corpus_manifest)
    corpus_manifest.update(
        {
            "job_id": job_id,
            "simulation_only": False,
            "items_file": "corpus/items.jsonl",
            "id_field": "item_id",
            "n_items": n_eligible,
            "n_eligible": n_eligible,
            "n_sealed": n_sealed,
            "n_source_items": n_source_items,
        }
    )
    corpus_manifest.setdefault("text_field", corpus_cfg.get("text_field") or "text")

    # The page status keeps the source frame and access policy by value; the
    # attestation records what the source reservation said when it was checked.
    sealed_status = drop_checksum_fields(source_sealed_status)
    sealed_status.update(
        {
            "status": "reserved-and-unexposed",
            "custodian": human_id,
            "simulation_only": False,
            "n_items": n_sealed,
            "source_fence_attestation": {
                "validated": True,
                "source_status": source_sealed_status.get("status"),
                "source_custodian": source_sealed_status.get("custodian"),
                "source_invalidation_state": source_sealed_status.get(
                    "invalidation_state"
                ),
            },
        }
    )

    component_bytes: dict[str, bytes] = {}
    for name in POLICY_COMPONENTS:
        candidate = source_policy / name
        if name in {"casebook.jsonl", "regression.jsonl", "gallery.md", "diff.yaml"}:
            component_bytes[name] = default_policy_component(name, target)
        elif candidate.is_file():
            component_bytes[name] = candidate.read_bytes()
        else:
            component_bytes[name] = default_policy_component(name, target)
    policy_manifest = {
        "schema": "subjective-label-policy/v1",
        "policy_id": "G_00",
        "parent": None,
        "status": "seed-awaiting-human-meaning",
        "simulation_only": False,
        "authority_confirmation": None,
        "components": list(component_bytes),
        "created_by": "P0 Contract API",
    }

    register = [
        f"# register · {target}\n",
        "P0 scaffold. Every region remains open until a Keeper-closed checkpoint.\n",
        "| cell | state | confirmed items | open card | last settled |",
        "|---|---|---:|---|---|",
    ]
    register.extend(f"| {cell} | open | 0 | — | — |" for cell in REGIONS)
    register_bytes = ("\n".join(register) + "\n").encode("utf-8")

    config_data = yaml_bytes(config)
    corpus_manifest_data = json_bytes(corpus_manifest)
    sealed_status_data = json_bytes(sealed_status)
    policy_manifest_data = yaml_bytes(policy_manifest)

    receipt = {
        "schema": "subjective-label-contract-receipt/v2",
        "job_id": job_id,
        "created_at": created_at,
        "writer": "label-building-workflow:P0 Contract API",
        "human_id": human_id,
        "meaning_confirmed": False,
        "p0_artifacts": list(P0_FILES),
        "next_action": "identified human confirms target meaning and schema",
    }
    run_name = "rl01_corpus-contract_job-v1"
    run_ticket = {
        "run": run_name,
        "family": "labeling",
        "domain": "subjective-label",
        "phase": "P0",
        "operation": "corpus-contract",
        "episode": "contract",
        "target": "job-v1",
        "commission": {"path": page_path(job_root, "gates/p0-contract/receipt.json")},
        "inputs": [{"path": page_path(job_root, "corpus/items.jsonl")}],
        "worker": {
            "kind": "cli",
            "name": "subjective-label.engine.job:create_contract",
        },
        "acceptance": "p0-contract-receipt-valid",
        "supersedes": None,
    }
    run_runtime = {
        "run": run_name,
        "family": "labeling",
        "operation": "corpus-contract",
        "target": "job-v1",
        "status": "complete",
        "ticket": f"runs/{run_name}.yaml",
        "result": f"results/{run_name}/result.yaml",
        "inputs": run_ticket["inputs"],
        "outcome": "P0 contract landed; human meaning confirmation remains open",
        "worker": run_ticket["worker"],
        "started_at": runtime_timestamp(created_at),
        "finished_at": runtime_timestamp(created_at),
        "supersedes": None,
        "failure": None,
    }
    run_result = {
        "run": run_name,
        "family": "labeling",
        "operation": "corpus-contract",
        "status": "complete",
        "outcome": "P0 contract landed; human meaning confirmation remains open",
        "artifacts": [{"path": page_path(job_root, "gates/p0-contract/receipt.json")}],
        "promotion": {
            "performed": False,
            "reason": "P0 human meaning confirmation is a separate gate",
        },
        "next_action": "human meaning confirmation",
    }

    report = (
        f"# {job_id} · P0 Contract\n\n"
        f"- Target: `{target}`\n"
        f"- Human semantic authority: `{human_id}`\n"
        f"- Corpus items: {corpus_manifest['n_items']} development items\n"
        "- Sealed test: reserved and unexposed\n"
        "- Human meaning gate: **pending**\n"
        "- Next: confirm the target, class meanings, regions, uncertainty, and unresolved disposition.\n"
    ).encode("utf-8")
    state = {
        "phase": "P0",
        "frontier": "G0 · human meaning confirmation",
        "status": "human-meaning-confirmation-pending",
        "meaning_confirmed": False,
    }

    artifacts: dict[Path, bytes] = {
        job_root / "config.yaml": config_data,
        job_root / "corpus" / "items.jsonl": items_data,
        job_root / "corpus" / "manifest.json": corpus_manifest_data,
        job_root / "test" / "sealed" / "status.json": sealed_status_data,
        job_root / "test" / "sealed" / "manifest.protected.jsonl": protected_data,
        job_root / "test" / "sealed" / "access_log.jsonl": b"",
        job_root / "register.md": register_bytes,
        job_root / "gold" / "cumulative.jsonl": b"",
        job_root / "gold" / "cumulative.md": b"# cumulative human gold\n\nEmpty at P0.\n",
        job_root / "policy" / "current": b"G_00\n",
        job_root / "policy" / "versions" / "G_00" / "manifest.yaml": policy_manifest_data,
        job_root / "gates" / "p0-contract" / "receipt.json": json_bytes(receipt),
        runs_dir(job_root) / f"{run_name}.yaml": yaml_bytes(run_ticket),
        results_dir(job_root) / run_name / "runtime.yaml": yaml_bytes(run_runtime),
        results_dir(job_root) / run_name / "result.yaml": yaml_bytes(run_result),
        job_root / "REPORT.md": report,
        job_root / ".state.json": json_bytes(state),
    }
    for name, data in component_bytes.items():
        artifacts[job_root / "policy" / "versions" / "G_00" / name] = data

    created: list[str] = []
    for path, data in artifacts.items():
        if write_once(path, data):
            created.append(path.relative_to(page_root(job_root)).as_posix())
    for rel in ("cache/embeddings", "rounds", "handoff", "evaluation", "production", "audit"):
        (job_root / rel).mkdir(parents=True, exist_ok=True)

    return {
        "job_root": str(job_root),
        "job_id": job_id,
        "phase": "P0",
        "first_blocked_frontier": "G0 · human meaning confirmation",
        "created_files": created,
        "created_count": len(created),
        "items": corpus_manifest["n_items"],
        "sealed_items": n_sealed,
        "protected_manifest_copied_opaquely": False,
        "protected_manifest_parsed": _protected_records(source_protected.read_bytes()) is not None,
        "protected_manifest_exposed": False,
        "next_action": "human meaning confirmation",
    }


def _replace_exact(path: Path, expected: bytes, data: bytes) -> bool:
    """Replace one mutable P0 artifact only if it still holds the bytes this call read."""
    if not path.is_file() or path.is_symlink() or path.read_bytes() != expected:
        raise RuntimeError(f"refusing semantic confirmation over changed artifact: {path}")
    if expected == data:
        return False
    temp = path.with_name(path.name + ".meaning-confirm.tmp")
    temp.write_bytes(data)
    temp.replace(path)
    return True


def confirm_meaning(
    *,
    job_root: Path,
    page_file: Path,
    human_id: str,
    confirmed_at: str,
    accept_current_schema: bool,
    attest_as_human: bool = False,
    channel: str = "cli",
) -> dict:
    """Record an explicit caller attestation for the current semantic schema.

    ``human_id`` is a configured project identifier, not an authenticated
    principal. Callers must opt into that attestation explicitly; the receipt
    records this limitation so it cannot be mistaken for identity proof.

    The meaning receipt stores a content snapshot of what was confirmed
    (``semantic_bindings``); the G0 receipt repeats that snapshot.  A G0
    receipt left over from an earlier confirmation is archived to
    ``gates/g0/history/<timestamp>.json`` before the new one is written.
    """
    job_root = job_root.resolve()
    validate_page_lane(page_file, job_root)
    if not accept_current_schema:
        raise RuntimeError("confirmation requires --accept-current-schema")
    if attest_as_human is not True:
        raise RuntimeError("confirmation requires an explicit human caller attestation")

    before = status(job_root)
    config_path = job_root / "config.yaml"
    config_bytes = config_path.read_bytes()
    config = load_mapping(config_path)
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    if authority.get("human_id") != human_id:
        raise RuntimeError(
            "caller-supplied human_id must match the configured semantic authority"
        )
    held, reason = authority_hold(config)
    if held:
        raise RuntimeError(f"HOLD · {reason}")
    # Any integrity defect other than the not-yet-written G0 receipt blocks the
    # confirmation BEFORE a single byte is written.
    blocking_p0 = before["p0_integrity_errors"]
    blocking_g0 = [
        error for error in before["g0_integrity_errors"]
        if error != "G0 receipt missing after semantic confirmation"
    ]
    if blocking_p0 or before["missing"]:
        raise RuntimeError(
            "P0 contract integrity must pass before confirmation: "
            f"{blocking_p0 or before['missing']}"
        )
    if blocking_g0:
        raise RuntimeError(
            "G0 receipt integrity must be repaired before confirmation: "
            f"{blocking_g0}"
        )
    if g0_passed(before):
        return {
            "job_root": str(job_root),
            "phase": "P1",
            "updated_files": [],
            "updated_count": 0,
            "next_action": "propose round_01 card",
        }

    already_semantic = _meaning_receipt_valid(config, job_root)
    if not already_semantic:
        final_config = copy.deepcopy(config)
        final_authority = final_config.setdefault("authority", {})
        final_authority["meaning_confirmed"] = True
        final_authority["meaning_receipt"] = {
            "schema": "subjective-label-meaning-confirmation/v1",
            "status": "confirmed",
            "human_id": human_id,
            "identity_assurance": "caller_attested_not_authenticated",
            "confirmed_at": confirmed_at,
            "channel": channel,
            "bindings": semantic_bindings(final_config, policy_version(job_root)),
        }
        final_config_data = yaml_bytes(final_config)
    else:
        final_config = config
        final_config_data = config_bytes
    g0_data = json_bytes(g0_receipt_for(final_config["authority"]["meaning_receipt"]))

    updated: list[str] = []
    if not already_semantic and _replace_exact(config_path, config_bytes, final_config_data):
        updated.append("config.yaml")
    g0_path = job_root / "gates" / "g0" / "receipt.json"
    if g0_path.is_file() and g0_path.read_bytes() != g0_data:
        # status() found no G0 integrity error, so this receipt is stale: it
        # belongs to an earlier confirmation whose snapshot no longer matches.
        prior_data = g0_path.read_bytes()
        archive = _g0_history_path(job_root, prior_data)
        write_once(archive, prior_data)
        _replace_exact(g0_path, prior_data, g0_data)
        updated.extend([archive.relative_to(job_root).as_posix(), "gates/g0/receipt.json"])
    elif write_once(g0_path, g0_data):
        updated.append("gates/g0/receipt.json")

    after = status(job_root)
    if not g0_passed(after):
        raise RuntimeError(f"confirmation did not pass G0: {after['integrity_errors']}")
    return {
        "job_root": str(job_root),
        "phase": "P1",
        "updated_files": updated,
        "updated_count": len(updated),
        "next_action": "propose round_01 card",
    }


def revise_meanings(
    *,
    job_root: Path,
    human_id: str,
    meanings: dict,
    run: str,
    revised_at: str,
) -> dict:
    """Record one human-decided change to the label meanings, before any item is judged.

    The P0 contract froze the meanings it was given (for S-Label-4, an AI draft).
    A closed ``definition-discussion`` Run is the one sanctioned way to change
    them: the revision keeps before, after and the deciding Run, retires the old
    meaning confirmation and G0 receipt (the receipt is archived), and so the
    human confirms the new meanings (G0) again.  ``human_id`` is checked against
    the configuration; it is not authenticated.
    """
    job_root = job_root.resolve()
    before_state = status(job_root)
    if before_state["missing"] or before_state["p0_integrity_errors"]:
        raise RuntimeError(f"P0 contract integrity must pass first: {before_state['p0_integrity_errors']}")
    if before_state["hold"]:
        raise RuntimeError(f"HOLD · {before_state['hold_reason']}")
    config_path = job_root / "config.yaml"
    config_bytes = config_path.read_bytes()
    config = load_mapping(config_path)
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    if not human_id or authority.get("human_id") != human_id:
        raise RuntimeError("caller-supplied human_id must match the configured semantic authority")
    judged = _judged_items(job_root)
    if judged:
        raise RuntimeError(
            "the meanings can change only before any item is judged; already judged: " + ", ".join(judged[:5])
        )
    labels = config.get("labels") if isinstance(config.get("labels"), dict) else {}
    values = [str(v) for v in labels.get("values") or []]
    current = labels.get("meanings") if isinstance(labels.get("meanings"), dict) else {}
    if set(meanings) != set(values) or any(not str(meanings[v] or "").strip() for v in values):
        raise RuntimeError(f"give one meaning for each label: {values}")
    after = {v: " ".join(str(meanings[v]).split()) for v in values}
    if after == current:
        return {"job_root": str(job_root), "changed": False, "updated_files": [],
                "next_action": before_state["next_action"]}

    revisions = meaning_revisions(job_root)
    new_config = copy.deepcopy(config)
    new_config["labels"]["meanings"] = after
    new_authority = new_config.setdefault("authority", {})
    retired = new_authority.get("meaning_receipt")
    new_authority["meaning_confirmed"] = False
    new_authority["meaning_receipt"] = None
    new_data = yaml_bytes(new_config)
    g0_path = job_root / "gates" / "g0" / "receipt.json"
    g0_prior = g0_path.read_bytes() if g0_path.is_file() else None
    archive = _g0_history_path(job_root, g0_prior) if g0_prior is not None else None
    record = {
        "schema": MEANING_REVISION_SCHEMA,
        "seq": len(revisions) + 1,
        "run": run,
        "human_id": human_id,
        "identity_assurance": "caller_attested_not_authenticated",
        "revised_at": revised_at,
        "before": copy.deepcopy(current),
        "after": after,
        "retired_meaning_receipt": retired,
        "retired_g0_receipt": archive.relative_to(job_root).as_posix() if archive else None,
    }

    updated: list[str] = []
    revision_path = job_root / MEANING_REVISIONS / f'{record["seq"]:03d}.json'
    write_once(revision_path, (json.dumps(record, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    updated.append(revision_path.relative_to(job_root).as_posix())
    if archive is not None and g0_prior is not None:
        write_once(archive, g0_prior)
        g0_path.unlink()
        updated.extend([archive.relative_to(job_root).as_posix(), "gates/g0/receipt.json (retired)"])
    _replace_exact(config_path, config_bytes, new_data)
    updated.append("config.yaml")
    after_state = status(job_root)
    if not after_state["p0_contract_integrity_valid"]:
        raise RuntimeError(f"meaning revision left P0 invalid: {after_state['p0_integrity_errors']}")
    return {"job_root": str(job_root), "changed": True, "revision": revision_path.relative_to(job_root).as_posix(),
            "updated_files": updated, "next_action": after_state["next_action"]}


CORPUS_STATUSES = ("eligible", "sealed")


def _declared_int(mapping: dict, field: str) -> int | None:
    value = mapping.get(field)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def _corpus_errors(items_path: Path, corpus_manifest: dict) -> list[str]:
    """Rows parse, name one unique item each, carry a known population status, and match the counts."""
    if items_path.is_symlink():
        return ["refusing symlinked corpus/items.jsonl"]
    if not items_path.is_file():
        return ["corpus/items.jsonl missing"]
    seen: set[str] = set()
    n_rows = n_eligible = 0
    try:
        lines = items_path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        return [f"unreadable corpus/items.jsonl: {type(error).__name__}"]
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            return [f"corpus/items.jsonl line {number} is not JSON"]
        if not isinstance(row, dict):
            return [f"corpus/items.jsonl line {number} is not a JSON object"]
        item_id = str(row.get("item_id") or "").strip()
        if not item_id:
            return [f"corpus/items.jsonl line {number} has no item_id"]
        if item_id in seen:
            return [f"corpus/items.jsonl repeats item_id {item_id!r}"]
        if row.get("population_status") not in CORPUS_STATUSES:
            return [f"corpus/items.jsonl line {number} has no eligible or sealed population_status"]
        seen.add(item_id)
        n_rows += 1
        n_eligible += row.get("population_status") == "eligible"
    errors = []
    declared_items = _declared_int(corpus_manifest, "n_items")
    if declared_items is not None and declared_items != n_rows:
        errors.append(
            f"corpus/items.jsonl has {n_rows} rows but corpus/manifest.json says n_items {declared_items}"
        )
    declared_eligible = _declared_int(corpus_manifest, "n_eligible")
    if declared_eligible is not None and declared_eligible != n_eligible:
        errors.append(
            f"corpus/items.jsonl has {n_eligible} eligible rows but corpus/manifest.json says "
            f"n_eligible {declared_eligible}"
        )
    return errors


def _protected_count(path: Path) -> int | None:
    """Items in a structured protected manifest (one JSON object with item_id per line); None if opaque."""
    try:
        lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except (OSError, UnicodeError):
        return None
    ids = []
    for line in lines:
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            return None
        if not isinstance(row, dict) or not str(row.get("item_id") or "").strip():
            return None
        ids.append(str(row["item_id"]).strip())
    return len(set(ids))


def _component_names(components: object) -> list | None:
    """G_00 component names: a list of names, or a legacy mapping whose values are ignored."""
    if isinstance(components, dict):
        return list(components)
    if isinstance(components, list):
        return list(components)
    return None


def _component_path(policy_dir: Path, name: object) -> Path | None:
    """Resolve one G_00 component only when its name is a known, contained file."""
    text = str(name)
    if text not in POLICY_COMPONENTS or "/" in text or "\\" in text or ".." in text:
        return None
    candidate = policy_dir / text
    if candidate.is_symlink():
        return None
    return candidate


def status(job_root: Path) -> dict:
    """Derive P0 integrity and G0 predicates without writing or raising on defects.

    P0 integrity is presence, parse and content: the five P0 files parse, the
    corpus rows match the corpus manifest's counts, exactly one protected
    manifest exists and matches the sealed count, sealed custody is asserted
    by status.json fields, every named G_00 component exists, and the P0
    receipt names this job and human.  G0 compares the meaning receipt's
    content snapshot with the current config by value; the G0 receipt must
    repeat that snapshot.  No content hash is written, read or compared.
    """
    job_root = job_root.resolve()
    present = {rel: (job_root / rel).is_file() for rel in P0_FILES}
    missing = [rel for rel, exists in present.items() if not exists]
    p0_integrity_errors: list[str] = []
    g0_integrity_errors: list[str] = []

    loaded: dict[str, dict] = {}
    for rel in P0_FILES:
        if not present[rel]:
            continue
        path = job_root / rel
        if rel == "register.md":
            try:
                if path.is_symlink():
                    p0_integrity_errors.append("refusing symlinked authority file: register.md")
                elif not path.read_text(encoding="utf-8").strip():
                    p0_integrity_errors.append("register.md is empty")
            except (OSError, UnicodeError) as error:
                p0_integrity_errors.append(f"unreadable register.md: {type(error).__name__}")
            continue
        value, error = try_load_mapping(path)
        if error:
            p0_integrity_errors.append(error)
        loaded[rel] = value

    config = loaded.get("config.yaml", {})
    corpus_manifest = loaded.get("corpus/manifest.json", {})
    sealed_status = loaded.get("test/sealed/status.json", {})
    policy_manifest = loaded.get("policy/versions/G_00/manifest.yaml", {})

    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    meaning_confirmed = bool(authority.get("meaning_confirmed"))
    try:
        meaning_is_bound = bool(config) and _meaning_receipt_bound(config, job_root)
        meaning_is_valid = meaning_is_bound and _meaning_receipt_valid(config, job_root)
    except (OSError, ValueError, TypeError):
        meaning_is_bound = meaning_is_valid = False
    hold, hold_reason = authority_hold(config) if config else (False, "")
    revisions: list[dict] = []
    if config:
        try:
            revisions = meaning_revisions(job_root)
        except (OSError, ValueError, TypeError) as error:
            p0_integrity_errors.append(f"meaning revisions unreadable: {error}")
        else:
            p0_integrity_errors.extend(_revision_chain_errors(config, revisions))

    source_attestation = sealed_status.get("source_fence_attestation")
    exclusion_asserted = False
    g0_receipt_valid = False
    g0_receipt_path = job_root / "gates" / "g0" / "receipt.json"
    p0_receipt_path = job_root / "gates" / "p0-contract" / "receipt.json"

    if not missing and not p0_integrity_errors:
        p0_integrity_errors.extend(_corpus_errors(job_root / "corpus" / "items.jsonl", corpus_manifest))

        sealed_dir = job_root / "test" / "sealed"
        if sealed_dir.is_symlink():
            p0_integrity_errors.append("refusing symlinked test/sealed/")
        else:
            try:
                protected_manifest = find_protected_manifest(sealed_dir)
            except RuntimeError as error:
                p0_integrity_errors.append(str(error))
            else:
                if protected_manifest.is_symlink():
                    p0_integrity_errors.append("refusing symlinked protected manifest")
                else:
                    n_protected = _protected_count(protected_manifest)
                    for mapping, field, where in (
                        (sealed_status, "n_items", "test/sealed/status.json"),
                        (corpus_manifest, "n_sealed", "corpus/manifest.json"),
                    ):
                        declared = _declared_int(mapping, field)
                        if n_protected is not None and declared is not None and declared != n_protected:
                            p0_integrity_errors.append(
                                f"protected manifest names {n_protected} items but {where} says {field} {declared}"
                            )
        exclusion_asserted = bool(
            sealed_status.get("status") == "reserved-and-unexposed"
            and sealed_status.get("custodian")
            and sealed_status.get("invalidation_state", "valid") == "valid"
            and isinstance(source_attestation, dict)
            and source_attestation.get("validated") is True
            and source_attestation.get("source_invalidation_state") == "valid"
        )
        if not exclusion_asserted:
            p0_integrity_errors.append("sealed/development exclusion custody is not asserted")

        policy_dir = job_root / "policy" / "versions" / "G_00"
        if str(policy_manifest.get("policy_id") or "G_00") != "G_00":
            p0_integrity_errors.append("policy/versions/G_00/manifest.yaml names another policy")
        names = _component_names(policy_manifest.get("components"))
        if not names:
            p0_integrity_errors.append("G_00 components missing")
        else:
            for name in names:
                component = _component_path(policy_dir, name)
                if component is None:
                    p0_integrity_errors.append(f"G_00 component name refused: {name}")
                elif not component.is_file():
                    p0_integrity_errors.append(f"G_00 component missing: {name}")

        if not p0_receipt_path.is_file():
            p0_integrity_errors.append("P0 contract receipt missing")
        else:
            p0_receipt, error = try_load_mapping(p0_receipt_path)
            project = config.get("project") if isinstance(config.get("project"), dict) else {}
            if error:
                p0_integrity_errors.append(error)
            elif project.get("id") and p0_receipt.get("job_id") != project.get("id"):
                p0_integrity_errors.append("P0 receipt names another job")
            elif p0_receipt.get("human_id") != authority.get("human_id"):
                p0_integrity_errors.append("P0 receipt names another human")

        # A G0 receipt matters only while the meaning receipt still describes the
        # current config; one left over from an earlier confirmation is stale and
        # the next confirmation archives it.
        if meaning_is_bound:
            if not g0_receipt_path.is_file():
                g0_integrity_errors.append("G0 receipt missing after semantic confirmation")
            else:
                g0_receipt, error = try_load_mapping(g0_receipt_path)
                g0_receipt_valid = not error and _g0_receipt_matches(
                    g0_receipt, authority.get("meaning_receipt"), authority.get("human_id")
                )
                if not g0_receipt_valid:
                    g0_integrity_errors.append("G0 receipt is invalid or semantically unbound")

    p0_contract_integrity_valid = not missing and not p0_integrity_errors
    integrity_errors = p0_integrity_errors + g0_integrity_errors
    g0_state = {
        "p0_contract_integrity_valid": p0_contract_integrity_valid,
        "hold": hold,
        "meaning_receipt_valid": meaning_is_valid,
        "g0_receipt_valid": g0_receipt_valid,
    }
    g0_ready = g0_passed(g0_state)
    # `phase` is a compatibility projection for older status readers. The
    # booleans above and below own every gate and confirmation decision.
    if missing:
        phase = "P0"
        next_action = "supply missing P0 files"
        first_blocked = "G0 · contract integrity"
    elif not p0_contract_integrity_valid:
        phase = "P0"
        next_action = "repair P0 integrity before any Round 1 proposal"
        first_blocked = "G0 · contract integrity"
    elif hold:
        phase = "P0"
        next_action = f"HOLD · {hold_reason}"
        first_blocked = "G0 · human authority"
    elif g0_integrity_errors:
        phase = "P0"
        next_action = "repair the G0 receipt before any Round 1 proposal"
        first_blocked = "G0 · receipt integrity"
    elif not meaning_is_valid:
        phase = "P0"
        next_action = "human meaning confirmation"
        first_blocked = "G0 · human meaning confirmation"
    else:
        phase = "P1"
        next_action = "propose round_01 card"
        first_blocked = None
    return {
        "job_root": str(job_root),
        "p0_files": present,
        "missing": missing,
        "human_id": authority.get("human_id"),
        "authority_mode": authority.get("mode"),
        "hold": hold,
        "hold_reason": hold_reason,
        "meaning_confirmed": meaning_confirmed,
        "meaning_receipt_valid": meaning_is_valid,
        "meaning_revisions": len(revisions),
        "g0_receipt_valid": g0_receipt_valid,
        "g0_passed": g0_ready,
        "p0_contract_integrity_valid": p0_contract_integrity_valid,
        "p0_integrity_errors": p0_integrity_errors,
        "g0_integrity_errors": g0_integrity_errors,
        "integrity_errors": integrity_errors,
        "sealed_development_exclusion_asserted": exclusion_asserted,
        "sealed_custodian": sealed_status.get("custodian"),
        "source_custodian_provenance": (
            source_attestation.get("source_custodian")
            if isinstance(source_attestation, dict)
            else None
        ),
        "phase": phase,
        "first_blocked_frontier": first_blocked,
        "next_action": next_action,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="subjective-label P0 Contract API")
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="create one page-local canonical P0 job")
    create.add_argument("--source-job", type=Path, required=True)
    create.add_argument("--job-root", type=Path, required=True)
    create.add_argument("--page-file", type=Path, required=True)
    create.add_argument("--job-id", required=True)
    create.add_argument("--target", required=True)
    create.add_argument("--human-id", required=True)
    create.add_argument(
        "--created-at", default=datetime.now().astimezone().isoformat(timespec="seconds")
    )

    confirm = sub.add_parser(
        "confirm", help="record explicit caller attestation to the current meaning"
    )
    confirm.add_argument("--job-root", type=Path, required=True)
    confirm.add_argument("--page-file", type=Path, required=True)
    confirm.add_argument("--human-id", required=True)
    confirm.add_argument("--confirmed-at", default=date.today().isoformat())
    confirm.add_argument("--accept-current-schema", action="store_true", required=True)
    confirm.add_argument(
        "--attest-as-human", action="store_true", required=True,
        help="explicitly attest that you are the configured human authority; identity is not authenticated",
    )

    inspect = sub.add_parser("status", help="derive the P0 frontier without writing")
    inspect.add_argument("--job-root", type=Path, required=True)

    args = parser.parse_args()
    if args.command == "create":
        result = create_contract(
            source_job=args.source_job,
            job_root=args.job_root,
            page_file=args.page_file,
            job_id=args.job_id,
            target=args.target,
            human_id=args.human_id,
            created_at=args.created_at,
        )
    elif args.command == "confirm":
        result = confirm_meaning(
            job_root=args.job_root,
            page_file=args.page_file,
            human_id=args.human_id,
            confirmed_at=args.confirmed_at,
            accept_current_schema=args.accept_current_schema,
            attest_as_human=args.attest_as_human,
        )
    else:
        result = status(args.job_root)
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
