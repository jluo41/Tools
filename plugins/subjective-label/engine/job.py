#!/usr/bin/env python3
"""Canonical P0 Contract API for one subjective-label job.

The API imports one already-fenced corpus snapshot and its opaque sealed-test
reservation into a page-local ``labeling/`` lane.  The protected manifest is
hashed and byte-copied, but never parsed or printed.  The API deliberately
creates no round, no human gold, and no claim that the seed policy is mature.

The writer is additive and idempotent: an existing identical artifact is
accepted, while an existing different artifact is never overwritten.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from datetime import date
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
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def yaml_bytes(value: Any) -> bytes:
    return yaml.safe_dump(
        value, sort_keys=False, allow_unicode=True, default_flow_style=False
    ).encode("utf-8")


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode(
        "utf-8"
    )


def canonical_hash(value: Any) -> str:
    data = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return sha256_bytes(data)


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


def count_jsonl(path: Path) -> int:
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


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


def validate_source_fence(status: dict, protected_checksum: str) -> None:
    declared = str(status.get("protected_manifest_checksum") or "").removeprefix(
        "sha256:"
    )
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
        and declared == protected_checksum
    )
    if not valid:
        raise RuntimeError(
            "source sealed reservation lacks a valid custodian, exclusion policy, "
            "frame, invalidation receipt, or matching protected-manifest checksum"
        )


def semantic_bindings(config: dict, policy_manifest: Path) -> dict:
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    labels = config.get("labels") if isinstance(config.get("labels"), dict) else {}
    regions = config.get("regions") if isinstance(config.get("regions"), dict) else {}
    uncertainty = (
        config.get("uncertainty") if isinstance(config.get("uncertainty"), dict) else {}
    )
    return {
        "construct_checksum": canonical_hash(construct),
        "classes_checksum": canonical_hash(labels),
        "regions_checksum": canonical_hash(regions),
        "uncertainty_checksum": canonical_hash(uncertainty),
        "unresolved_disposition": {
            "unresolved_is_label": uncertainty.get("unresolved_is_label"),
            "none_value": labels.get("none_value"),
        },
        "policy_manifest_checksum": sha256_file(policy_manifest),
    }


def _meaning_receipt_valid(config: dict, job_root: Path) -> bool:
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    receipt = authority.get("meaning_receipt")
    policy_manifest = job_root / "policy" / "versions" / "G_00" / "manifest.yaml"
    return bool(
        authority.get("meaning_confirmed") is True
        and isinstance(receipt, dict)
        and receipt.get("schema") == "subjective-label-meaning-confirmation/v1"
        and receipt.get("status") == "confirmed"
        and receipt.get("human_id") == authority.get("human_id")
        and receipt.get("confirmed_at")
        and policy_manifest.is_file()
        and receipt.get("bindings") == semantic_bindings(config, policy_manifest)
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

    items_checksum = sha256_file(source_items)
    manifest_items_checksum = str(
        source_corpus_manifest.get("items_checksum")
        or source_corpus_manifest.get("canonical_table", {}).get("checksum")
        or ""
    ).removeprefix("sha256:")
    if manifest_items_checksum and manifest_items_checksum != items_checksum:
        raise RuntimeError("source corpus manifest does not match corpus/items.jsonl")

    config = copy.deepcopy(source_config)
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
        "source_config_checksum": sha256_file(source_job / "config.yaml"),
        "source_corpus_manifest_checksum": sha256_file(source_job / "corpus" / "manifest.json"),
        "source_sealed_status_checksum": sha256_file(source_job / "test" / "sealed" / "status.json"),
        "created_at": created_at,
    }

    corpus_manifest = copy.deepcopy(source_corpus_manifest)
    corpus_manifest.update(
        {
            "job_id": job_id,
            "simulation_only": False,
            "items_file": "corpus/items.jsonl",
            "items_checksum": items_checksum,
            "n_items": count_jsonl(source_items),
            "imported_from_manifest_checksum": sha256_file(
                source_job / "corpus" / "manifest.json"
            ),
        }
    )

    protected_checksum = sha256_file(source_protected)
    validate_source_fence(source_sealed_status, protected_checksum)
    sealed_status = copy.deepcopy(source_sealed_status)
    sealed_status.update(
        {
            "status": "reserved-and-unexposed",
            "custodian": human_id,
            "simulation_only": False,
            "protected_manifest_checksum": protected_checksum,
            "imported_from_status_checksum": sha256_file(
                source_job / "test" / "sealed" / "status.json"
            ),
            "source_fence_attestation": {
                "validated": True,
                "source_status": source_sealed_status.get("status"),
                "source_custodian": source_sealed_status.get("custodian"),
                "source_invalidation_state": source_sealed_status.get(
                    "invalidation_state"
                ),
                "source_frame_checksum": canonical_hash(
                    source_sealed_status.get("frame")
                ),
                "source_access_policy_checksum": canonical_hash(
                    source_sealed_status.get("access_policy")
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
    component_hashes = {name: sha256_bytes(data) for name, data in component_bytes.items()}
    policy_manifest = {
        "schema": "subjective-label-policy/v1",
        "policy_id": "G_00",
        "parent": None,
        "status": "seed-awaiting-human-meaning",
        "simulation_only": False,
        "authority_confirmation": None,
        "components": component_hashes,
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
    p0_artifact_data = {
        "config.yaml": config_data,
        "corpus/manifest.json": corpus_manifest_data,
        "test/sealed/status.json": sealed_status_data,
        "register.md": register_bytes,
        "policy/versions/G_00/manifest.yaml": policy_manifest_data,
    }
    p0_artifact_checksums = {
        name: sha256_bytes(data) for name, data in p0_artifact_data.items()
    }

    receipt = {
        "schema": "subjective-label-contract-receipt/v2",
        "job_id": job_id,
        "created_at": created_at,
        "writer": "label-building-workflow:P0 Contract API",
        "human_id": human_id,
        "meaning_confirmed": False,
        "corpus_items_checksum": items_checksum,
        "sealed_manifest_checksum": protected_checksum,
        "p0_artifact_checksums": p0_artifact_checksums,
        "source_fence_attestation_checksum": canonical_hash(
            sealed_status["source_fence_attestation"]
        ),
        "source_policy_checksum": sha256_file(source_policy / "manifest.yaml")
        if (source_policy / "manifest.yaml").is_file()
        else None,
        "next_action": "identified human confirms target meaning and schema",
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
        "frontier": "P0 human meaning confirmation",
        "status": "human-meaning-confirmation-pending",
        "meaning_confirmed": False,
    }

    artifacts: dict[Path, bytes] = {
        job_root / "config.yaml": config_data,
        job_root / "corpus" / "items.jsonl": source_items.read_bytes(),
        job_root / "corpus" / "manifest.json": corpus_manifest_data,
        job_root / "test" / "sealed" / "status.json": sealed_status_data,
        job_root / "test" / "sealed" / source_protected.name: source_protected.read_bytes(),
        job_root / "test" / "sealed" / "access_log.jsonl": b"",
        job_root / "register.md": register_bytes,
        job_root / "gold" / "cumulative.jsonl": b"",
        job_root / "gold" / "cumulative.md": b"# cumulative human gold\n\nEmpty at P0.\n",
        job_root / "policy" / "current": b"G_00\n",
        job_root / "policy" / "versions" / "G_00" / "manifest.yaml": policy_manifest_data,
        job_root / "gates" / "p0-contract" / "receipt.json": json_bytes(receipt),
        job_root / "REPORT.md": report,
        job_root / ".state.json": json_bytes(state),
    }
    for name, data in component_bytes.items():
        artifacts[job_root / "policy" / "versions" / "G_00" / name] = data

    created: list[str] = []
    for path, data in artifacts.items():
        if write_once(path, data):
            created.append(path.relative_to(job_root).as_posix())
    for rel in ("cache/embeddings", "rounds", "handoff", "evaluation", "production", "audit"):
        (job_root / rel).mkdir(parents=True, exist_ok=True)

    return {
        "job_root": str(job_root),
        "job_id": job_id,
        "phase": "P0",
        "first_blocked_frontier": "P0 human meaning confirmation",
        "created_files": created,
        "created_count": len(created),
        "items": corpus_manifest["n_items"],
        "protected_manifest_copied_opaquely": True,
        "protected_manifest_parsed": False,
        "protected_manifest_exposed": False,
        "next_action": "human meaning confirmation",
    }


def _replace_exact(path: Path, expected_checksum: str, data: bytes) -> bool:
    """Replace one mutable P0 artifact only from the exact expected snapshot."""
    if not path.is_file() or sha256_file(path) != expected_checksum:
        raise RuntimeError(f"refusing semantic confirmation over changed artifact: {path}")
    if path.read_bytes() == data:
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
) -> dict:
    """Record the identified human's explicit confirmation of the current schema."""
    job_root = job_root.resolve()
    validate_page_lane(page_file, job_root)
    if not accept_current_schema:
        raise RuntimeError("confirmation requires --accept-current-schema")

    before = status(job_root)
    config_path = job_root / "config.yaml"
    config = load_mapping(config_path)
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    if authority.get("human_id") != human_id:
        raise RuntimeError("only the identified human semantic authority may confirm")
    if before["phase"] == "P1" and before["meaning_receipt_valid"]:
        return {
            "job_root": str(job_root),
            "phase": "P1",
            "updated_files": [],
            "updated_count": 0,
            "next_action": "propose round_01 card",
        }

    p0_receipt_path = job_root / "gates" / "p0-contract" / "receipt.json"
    p0_receipt = load_mapping(p0_receipt_path)
    initial_checksums = p0_receipt.get("p0_artifact_checksums")
    if not isinstance(initial_checksums, dict):
        raise RuntimeError("P0 contract receipt does not bind the five authority artifacts")

    already_semantic = _meaning_receipt_valid(config, job_root)
    if not already_semantic and not before["g0_integrity"]:
        raise RuntimeError("P0 integrity must pass before human meaning confirmation")

    if not already_semantic:
        final_config = copy.deepcopy(config)
        final_authority = final_config.setdefault("authority", {})
        bindings = semantic_bindings(
            final_config,
            job_root / "policy" / "versions" / "G_00" / "manifest.yaml",
        )
        final_authority["meaning_confirmed"] = True
        final_authority["meaning_receipt"] = {
            "schema": "subjective-label-meaning-confirmation/v1",
            "status": "confirmed",
            "human_id": human_id,
            "confirmed_at": confirmed_at,
            "bindings": bindings,
        }
        final_config_data = yaml_bytes(final_config)
    else:
        final_config = config
        final_config_data = config_path.read_bytes()

    final_p0_data = {
        "config.yaml": final_config_data,
        "corpus/manifest.json": (job_root / "corpus" / "manifest.json").read_bytes(),
        "test/sealed/status.json": (job_root / "test" / "sealed" / "status.json").read_bytes(),
        "register.md": (job_root / "register.md").read_bytes(),
        "policy/versions/G_00/manifest.yaml": (
            job_root / "policy" / "versions" / "G_00" / "manifest.yaml"
        ).read_bytes(),
    }
    final_checksums = {
        name: sha256_bytes(data) for name, data in final_p0_data.items()
    }
    sealed_status = load_mapping(job_root / "test" / "sealed" / "status.json")
    corpus_manifest = load_mapping(job_root / "corpus" / "manifest.json")
    meaning_receipt = final_config["authority"]["meaning_receipt"]
    g0_receipt = {
        "schema": "subjective-label-g0-receipt/v1",
        "status": "passed",
        "human_id": human_id,
        "confirmed_at": confirmed_at,
        "p0_artifact_checksums": final_checksums,
        "meaning_receipt_checksum": canonical_hash(meaning_receipt),
        "corpus_items_checksum": corpus_manifest.get("items_checksum"),
        "sealed_manifest_checksum": sealed_status.get("protected_manifest_checksum"),
        "source_fence_attestation_checksum": canonical_hash(
            sealed_status.get("source_fence_attestation")
        ),
    }

    updated: list[str] = []
    if not already_semantic:
        if _replace_exact(
            config_path, str(initial_checksums.get("config.yaml") or ""), final_config_data
        ):
            updated.append("config.yaml")
    g0_path = job_root / "gates" / "g0" / "receipt.json"
    if write_once(g0_path, json_bytes(g0_receipt)):
        updated.append("gates/g0/receipt.json")

    after = status(job_root)
    if after["phase"] != "P1":
        raise RuntimeError(f"confirmation did not close P0: {after['integrity_errors']}")
    return {
        "job_root": str(job_root),
        "phase": "P1",
        "updated_files": updated,
        "updated_count": len(updated),
        "next_action": "propose round_01 card",
    }


def status(job_root: Path) -> dict:
    job_root = job_root.resolve()
    present = {rel: (job_root / rel).is_file() for rel in P0_FILES}
    config = load_mapping(job_root / "config.yaml") if present["config.yaml"] else {}
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    meaning_confirmed = bool(authority.get("meaning_confirmed"))
    meaning_is_valid = _meaning_receipt_valid(config, job_root)
    missing = [rel for rel, exists in present.items() if not exists]

    integrity_errors: list[str] = []
    exclusion_asserted = False
    g0_receipt_valid = False
    if not missing:
        corpus_manifest = load_mapping(job_root / "corpus" / "manifest.json")
        items_path = job_root / "corpus" / "items.jsonl"
        expected_items = str(corpus_manifest.get("items_checksum") or "").removeprefix(
            "sha256:"
        )
        if not items_path.is_file() or not expected_items:
            integrity_errors.append("corpus items/checksum missing")
        elif sha256_file(items_path) != expected_items:
            integrity_errors.append("corpus items checksum mismatch")

        sealed_status = load_mapping(job_root / "test" / "sealed" / "status.json")
        try:
            protected_manifest = find_protected_manifest(job_root / "test" / "sealed")
        except RuntimeError as error:
            integrity_errors.append(str(error))
        else:
            expected_seal = str(
                sealed_status.get("protected_manifest_checksum") or ""
            ).removeprefix("sha256:")
            if not expected_seal or sha256_file(protected_manifest) != expected_seal:
                integrity_errors.append("protected manifest checksum mismatch")
        source_attestation = sealed_status.get("source_fence_attestation")
        exclusion_asserted = bool(
            sealed_status.get("status") == "reserved-and-unexposed"
            and sealed_status.get("custodian")
            and sealed_status.get("protected_manifest_checksum")
            and isinstance(source_attestation, dict)
            and source_attestation.get("validated") is True
            and source_attestation.get("source_invalidation_state") == "valid"
        )
        if not exclusion_asserted:
            integrity_errors.append("sealed/development exclusion custody is not asserted")

        policy_manifest = load_mapping(
            job_root / "policy" / "versions" / "G_00" / "manifest.yaml"
        )
        components = policy_manifest.get("components")
        if not isinstance(components, dict) or not components:
            integrity_errors.append("G_00 component checksums missing")
        else:
            for name, expected in components.items():
                component = job_root / "policy" / "versions" / "G_00" / str(name)
                if not component.is_file() or sha256_file(component) != str(expected):
                    integrity_errors.append(f"G_00 component checksum mismatch: {name}")

        g0_receipt_path = job_root / "gates" / "g0" / "receipt.json"
        receipt_path = (
            g0_receipt_path
            if g0_receipt_path.is_file()
            else job_root / "gates" / "p0-contract" / "receipt.json"
        )
        if not receipt_path.is_file():
            integrity_errors.append("P0 contract receipt missing")
        else:
            receipt = load_mapping(receipt_path)
            receipt_checksums = receipt.get("p0_artifact_checksums")
            if not isinstance(receipt_checksums, dict):
                integrity_errors.append("P0 receipt does not bind all five authority artifacts")
            else:
                for rel in P0_FILES:
                    expected = str(receipt_checksums.get(rel) or "")
                    if not expected or sha256_file(job_root / rel) != expected:
                        integrity_errors.append(f"P0 authority checksum mismatch: {rel}")
            if receipt.get("corpus_items_checksum") != expected_items:
                integrity_errors.append("P0 receipt corpus checksum mismatch")
            if receipt.get("sealed_manifest_checksum") != sealed_status.get(
                "protected_manifest_checksum"
            ):
                integrity_errors.append("P0 receipt sealed checksum mismatch")
            if receipt.get("source_fence_attestation_checksum") != canonical_hash(
                source_attestation
            ):
                integrity_errors.append("P0 receipt source-fence attestation mismatch")

        if meaning_confirmed or meaning_is_valid or g0_receipt_path.is_file():
            if not g0_receipt_path.is_file():
                integrity_errors.append("G0 receipt missing after semantic confirmation")
            else:
                g0_receipt = load_mapping(g0_receipt_path)
                meaning_receipt = authority.get("meaning_receipt")
                g0_receipt_valid = bool(
                    g0_receipt.get("schema") == "subjective-label-g0-receipt/v1"
                    and g0_receipt.get("status") == "passed"
                    and g0_receipt.get("human_id") == authority.get("human_id")
                    and isinstance(meaning_receipt, dict)
                    and g0_receipt.get("meaning_receipt_checksum")
                    == canonical_hash(meaning_receipt)
                )
                if not g0_receipt_valid:
                    integrity_errors.append("G0 receipt is invalid or semantically unbound")

    g0_integrity = not missing and not integrity_errors
    if missing:
        phase = "P0"
        next_action = "supply missing P0 files"
        first_blocked = "G0 Contract integrity"
    elif not g0_integrity:
        phase = "P0"
        next_action = "repair P0 integrity before any Round 1 proposal"
        first_blocked = "G0 Contract integrity"
    elif not meaning_is_valid:
        phase = "P0"
        next_action = "human meaning confirmation"
        first_blocked = "P0 human meaning confirmation"
    elif not g0_receipt_valid:
        phase = "P0"
        next_action = "repair the G0 receipt before any Round 1 proposal"
        first_blocked = "G0 Contract integrity"
    else:
        phase = "P1"
        next_action = "propose round_01 card"
        first_blocked = None
    return {
        "job_root": str(job_root),
        "p0_files": present,
        "missing": missing,
        "human_id": authority.get("human_id"),
        "meaning_confirmed": meaning_confirmed,
        "meaning_receipt_valid": meaning_is_valid,
        "g0_receipt_valid": g0_receipt_valid,
        "g0_integrity": g0_integrity,
        "integrity_errors": integrity_errors,
        "sealed_development_exclusion_asserted": exclusion_asserted,
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
    create.add_argument("--created-at", default=date.today().isoformat())

    confirm = sub.add_parser(
        "confirm", help="record the identified human's current-schema confirmation"
    )
    confirm.add_argument("--job-root", type=Path, required=True)
    confirm.add_argument("--page-file", type=Path, required=True)
    confirm.add_argument("--human-id", required=True)
    confirm.add_argument("--confirmed-at", default=date.today().isoformat())
    confirm.add_argument("--accept-current-schema", action="store_true", required=True)

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
        )
    else:
        result = status(args.job_root)
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
