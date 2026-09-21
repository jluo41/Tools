#!/usr/bin/env python3
"""Build a development-only fenced source job for ``job.py create``.

A fenced source is a corpus snapshot whose sealed test is reserved BEFORE any
development read. This tool draws sealed ids with a declared seed, optionally
stratified by one item-level field from a side file, writes only eligible rows
to the development corpus, and writes an opaque protected manifest containing
sealed ids and text hashes only. Sealed text is not copied into the fenced
source or the Page-visible development corpus. It also renders a readable G_00
guideline from the seed config's class meanings.

The writer is additive: an existing different file is refused, never replaced.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import random
from datetime import datetime, timezone
from pathlib import Path

import yaml


HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location("subjective_label_job_for_fence", HERE / "job.py")
job = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(job)


def _read_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _item_strata(path: Path, id_field: str, field: str) -> dict[str, str]:
    """One value per item from a row-level side file; conflicting values refuse."""
    strata: dict[str, str] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            item_id, value = str(row.get(id_field)), str(row.get(field))
            if strata.setdefault(item_id, value) != value:
                raise RuntimeError(f"{field} is not item-level: item {item_id} has two values")
    return strata


def draw_sealed(ids: list[str], n: int, seed: int, strata: dict[str, str] | None) -> tuple[list[str], dict]:
    ordered = sorted(ids)
    rng = random.Random(seed)
    if not strata:
        chosen = rng.sample(ordered, n)
        return sorted(chosen), {"all": {"eligible": len(ordered), "sealed": n}}
    groups: dict[str, list[str]] = {}
    for item_id in ordered:
        groups.setdefault(strata.get(item_id, "missing"), []).append(item_id)
    keys = sorted(groups)
    base, extra = divmod(n, len(keys))
    chosen: list[str] = []
    report = {}
    for index, key in enumerate(keys):
        take = min(base + (1 if index < extra else 0), len(groups[key]))
        chosen.extend(rng.sample(groups[key], take))
        report[key] = {"eligible": len(groups[key]), "sealed": take,
                       "inclusion_probability": take / len(groups[key])}
    return sorted(chosen), report


def guideline_markdown(config: dict) -> str:
    construct = config.get("construct") or {}
    labels = config.get("labels") or {}
    regions = config.get("regions") or {}
    uncertainty = config.get("uncertainty") or {}
    lines = [f"# G_00 · {construct.get('name', 'target')}", ""]
    if construct.get("question"):
        lines += [f"**Question:** {construct['question']}", ""]
    for key in ("seed", "scope"):
        if construct.get(key):
            lines += [f"**{key.title()}:** {construct[key]}", ""]
    lines += ["## Classes", ""]
    for value in labels.get("values") or []:
        lines.append(f"- **{value}**: {(labels.get('meanings') or {}).get(value, '')}")
    lines += ["", "## Regions (why a case is typical or on a boundary)", ""]
    for value in regions.get("values") or []:
        lines.append(f"- **{value}**: {(regions.get('meanings') or {}).get(value, '')}")
    lines += ["", "## Uncertainty", "", str(uncertainty.get("meaning") or ""), "",
              "Seed policy only. The identified human confirms these meanings before round 1."]
    return "\n".join(lines) + "\n"


def build(*, items: Path, config_path: Path, out: Path, sealed_n: int, seed: int,
          custodian: str, stratify_jsonl: Path | None, stratify_field: str | None,
          id_field: str | None = None) -> dict:
    config = job.load_mapping(config_path)
    rows = _read_jsonl(items)
    corpus_cfg = config.get("corpus") if isinstance(config.get("corpus"), dict) else {}
    source_id_field = str(id_field or corpus_cfg.get("id_field") or "item_id")
    text_field = str(corpus_cfg.get("text_field") or "text")
    ids = []
    text_by_id: dict[str, str] = {}
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"source row {index} must be a JSON object")
        raw_id = row.get(source_id_field)
        item_id = str(raw_id).strip() if raw_id is not None else ""
        if not item_id:
            raise ValueError(f"source row {index} has no non-empty {source_id_field!r}")
        text = row.get(text_field)
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"source item {item_id!r} has no non-empty {text_field!r}")
        ids.append(item_id)
        text_by_id[item_id] = text
    if len(set(ids)) != len(ids):
        raise RuntimeError("duplicate item ids in the corpus")
    strata = (
        _item_strata(stratify_jsonl, source_id_field, stratify_field)
        if stratify_jsonl and stratify_field else None
    )
    sealed, report = draw_sealed(ids, sealed_n, seed, strata)
    sealed_set = set(sealed)

    corpus_rows = []
    protected_rows = []
    for row in rows:
        item_id = str(row[source_id_field]).strip()
        text_hash = hashlib.sha256(text_by_id[item_id].encode("utf-8")).hexdigest()
        if item_id in sealed_set:
            protected_rows.append({"item_id": item_id, "text_hash": text_hash})
            continue
        copy_row = dict(row)
        copy_row["item_id"] = item_id
        copy_row["population_status"] = "eligible"
        # Always recompute against the declared text field; an incoming hash
        # may describe another field or an earlier version of the row.
        copy_row["text_hash"] = text_hash
        corpus_rows.append(copy_row)
    items_bytes = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in corpus_rows).encode("utf-8")
    protected = "".join(
        json.dumps(r, sort_keys=True) + "\n" for r in protected_rows
    ).encode("utf-8")
    created = datetime.now(timezone.utc).isoformat(timespec="seconds")
    manifest = {
        "schema_version": "subjective-label/fenced-corpus-v1",
        "items_file": "corpus/items.jsonl",
        "items_checksum": "sha256:" + job.sha256_bytes(items_bytes),
        "n_items": len(corpus_rows),
        "n_eligible": len(corpus_rows),
        "n_sealed": len(sealed),
        "n_source_items": len(rows),
        "id_field": "item_id",
        "source_id_field": source_id_field,
        "text_field": text_field,
        "context_field": corpus_cfg.get("context_field"),
        "population": corpus_cfg.get("population"),
        "source": corpus_cfg.get("source"),
        "input_items_checksum": "sha256:" + job.sha256_file(items),
        "created_at": created,
    }
    frame_rule = (
        f"seeded random draw of {sealed_n} items"
        + (f", stratified evenly by {stratify_field}" if strata else "")
    )
    status = {
        "schema_version": "subjective-label/sealed-v2",
        "status": "reserved",
        "custodian": custodian,
        "reserved_at": created,
        "frame": {"rule": frame_rule, "sampling": "seeded_random", "seed": seed, "strata": report},
        "n_items": len(sealed),
        "protected_manifest_checksum": "sha256:" + job.sha256_bytes(protected),
        "text_location": "not retained in the fenced source; remains under custodian-controlled source custody",
        "access_policy": [
            "no development read, embed, index, retrieve, dedup, or prelabel",
            "release only after G* freezes, by the custodian",
            "sealed ids and hashes stay in the protected manifest; no development batch may contain a protected id",
        ],
        "invalidation_state": "valid",
    }
    policy_parts = {
        "guideline.md": guideline_markdown(config).encode("utf-8"),
        "boundaries.yaml": job.yaml_bytes({"status": "open", "regions": (config.get("regions") or {}).get("values")}),
        "procedure.yaml": job.yaml_bytes({"status": "seed", "steps": [
            "read the context, then the final response", "decide the class",
            "pick a region only if the case sits on a boundary", "say how unsure you are"]}),
        "uncertainty.yaml": job.yaml_bytes(config.get("uncertainty") or {}),
        "cheatsheet.md": guideline_markdown(config).encode("utf-8"),
    }
    policy_manifest = {
        "schema": "subjective-label-policy/v1", "policy_id": "G_00", "parent": None,
        "status": "seed", "components": {k: job.sha256_bytes(v) for k, v in policy_parts.items()},
    }
    fenced_config = copy.deepcopy(config)
    fenced_corpus = fenced_config.setdefault("corpus", {})
    if not isinstance(fenced_corpus, dict):
        raise ValueError("config.corpus must be a mapping")
    fenced_corpus["path"] = "corpus/items.jsonl"
    fenced_corpus["id_field"] = "item_id"
    files = {
        out / "config.yaml": job.yaml_bytes(fenced_config),
        out / "corpus" / "items.jsonl": items_bytes,
        out / "corpus" / "manifest.json": job.json_bytes(manifest),
        out / "test" / "sealed" / "manifest.protected.jsonl": protected,
        out / "test" / "sealed" / "status.json": job.json_bytes(status),
        out / "test" / "sealed" / "access_log.jsonl": b"",
        out / "policy" / "versions" / "G_00" / "manifest.yaml": job.yaml_bytes(policy_manifest),
    }
    for name, data in policy_parts.items():
        files[out / "policy" / "versions" / "G_00" / name] = data
    written = [str(path.relative_to(out)) for path, data in files.items() if job.write_once(path, data)]
    return {"out": str(out), "n_items": len(corpus_rows), "n_sealed": len(sealed),
            "strata": report, "written": written}


def main() -> None:
    parser = argparse.ArgumentParser(description="build one fenced subjective-label source job")
    parser.add_argument("--items", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--sealed-n", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--custodian", required=True)
    parser.add_argument("--stratify-jsonl", type=Path)
    parser.add_argument("--stratify-field")
    parser.add_argument("--id-field", help="override config.corpus.id_field")
    args = parser.parse_args()
    result = build(items=args.items, config_path=args.config, out=args.out, sealed_n=args.sealed_n,
                   seed=args.seed, custodian=args.custodian, stratify_jsonl=args.stratify_jsonl,
                   stratify_field=args.stratify_field, id_field=args.id_field)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
