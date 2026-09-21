from __future__ import annotations

import importlib.util
import hashlib
import json
from pathlib import Path

import pytest
import yaml


HERE = Path(__file__).resolve().parent


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


fence = _load("sl_fence_source_test", "fence_source.py")
job = _load("sl_job_for_fence_source_test", "job.py")


def _config(path: Path) -> dict:
    return {
        "schema_version": "subjective-label/v2",
        "corpus": {"path": str(path), "id_field": "id", "text_field": "body",
                   "context_field": "context"},
        "construct": {"name": "fixture", "question": "What is shown?"},
        "labels": {"values": ["yes", "no"], "meanings": {"yes": "yes", "no": "no"}},
        "regions": {"values": ["Y", "N"]},
        "uncertainty": {"levels": ["low", "high"], "meaning": "How sure?"},
    }


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
                    encoding="utf-8")


def test_custom_id_and_body_are_canonicalized_and_sealed_text_stays_out(tmp_path: Path) -> None:
    raw = tmp_path / "raw.jsonl"
    rows = [
        {"id": f"custom-{i}", "body": f"PRIVATE_BODY_{i}",
         "text": f"unconfigured decoy {i}", "context": f"context {i}"}
        for i in range(8)
    ]
    _write_jsonl(raw, rows)
    config_path = tmp_path / "config.seed.yaml"
    config_path.write_text(yaml.safe_dump(_config(raw), sort_keys=False), encoding="utf-8")
    source = tmp_path / "source"

    result = fence.build(items=raw, config_path=config_path, out=source, sealed_n=3, seed=11,
                         custodian="JL", stratify_jsonl=None, stratify_field=None)

    source_corpus = source / "corpus" / "items.jsonl"
    source_bytes = source_corpus.read_bytes()
    source_rows = [json.loads(line) for line in source_bytes.splitlines()]
    protected_path = source / "test" / "sealed" / "manifest.protected.jsonl"
    protected_rows = [json.loads(line) for line in protected_path.read_text().splitlines()]
    sealed_ids = {row["item_id"] for row in protected_rows}
    sealed_texts = {row["body"] for row in rows if row["id"] in sealed_ids}

    assert result["n_items"] == len(source_rows) == 5
    assert len(protected_rows) == 3
    assert all(row["population_status"] == "eligible" for row in source_rows)
    assert all(row["item_id"] == row["id"] for row in source_rows)
    assert all(row["text_hash"] == hashlib.sha256(row["body"].encode()).hexdigest()
               for row in source_rows)
    assert all(text.encode() not in source_bytes for text in sealed_texts)
    assert all(set(row) == {"item_id", "text_hash"} for row in protected_rows)
    assert all(row["text_hash"] == hashlib.sha256(
        next(item["body"] for item in rows if item["id"] == row["item_id"]).encode()
    ).hexdigest() for row in protected_rows)
    assert not any(text in protected_path.read_text() for text in sealed_texts)

    fenced_cfg = yaml.safe_load((source / "config.yaml").read_text(encoding="utf-8"))
    assert fenced_cfg["corpus"]["id_field"] == "item_id"
    assert fenced_cfg["corpus"]["text_field"] == "body"
    assert fenced_cfg["corpus"]["path"] == "corpus/items.jsonl"
    assert str(raw) not in (source / "config.yaml").read_text(encoding="utf-8")

    page = tmp_path / "board" / "pages" / "S-Label-custom" / "S-Label-custom.md"
    page.parent.mkdir(parents=True)
    page.write_text("# page\n", encoding="utf-8")
    page_root = page.parent / "labeling"
    job.create_contract(source_job=source, job_root=page_root, page_file=page,
                        job_id="custom", target="fixture", human_id="JL",
                        created_at="2026-09-20T10:00:00+00:00")
    page_corpus = page_root / "corpus" / "items.jsonl"
    page_bytes = page_corpus.read_bytes()
    page_rows = [json.loads(line) for line in page_bytes.splitlines()]
    assert len(page_rows) == len(source_rows)
    assert all(row["population_status"] == "eligible" for row in page_rows)
    assert all(text.encode() not in page_bytes for text in sealed_texts)
    assert (page_root / "test" / "sealed" / "manifest.protected.jsonl").read_bytes() == protected_path.read_bytes()
    page_cfg = yaml.safe_load((page_root / "config.yaml").read_text(encoding="utf-8"))
    assert page_cfg["corpus"]["id_field"] == "item_id"
    assert page_cfg["corpus"]["text_field"] == "body"


@pytest.mark.parametrize("row", [{"id": "missing-body"}, {"id": "empty-body", "body": "  "}])
def test_required_configured_text_must_be_present_and_nonempty(tmp_path: Path, row: dict) -> None:
    raw = tmp_path / "bad.jsonl"
    _write_jsonl(raw, [row])
    config_path = tmp_path / "config.seed.yaml"
    config_path.write_text(yaml.safe_dump(_config(raw), sort_keys=False), encoding="utf-8")
    with pytest.raises(ValueError, match="body"):
        fence.build(items=raw, config_path=config_path, out=tmp_path / "source", sealed_n=0,
                    seed=1, custodian="JL", stratify_jsonl=None, stratify_field=None)
