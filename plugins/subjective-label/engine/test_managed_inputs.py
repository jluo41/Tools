from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest
import yaml


HERE = Path(__file__).resolve().parent


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


label = _load("sl_label_managed_inputs_test", "label.py")
embed = _load("sl_embed_managed_inputs_test", "embed.py")


def _v2_root(tmp_path: Path) -> Path:
    root = tmp_path / "labeling"
    root.mkdir()
    (root / "config.yaml").write_text(yaml.safe_dump({
        "schema_version": "subjective-label/v2",
        "corpus": {"id_field": "item_id", "text_field": "body"},
        "embedding": {"model": "test-model", "backend": "test"},
    }), encoding="utf-8")
    (root / "corpus").mkdir()
    (root / "corpus" / "items.jsonl").write_text(
        json.dumps({"item_id": "eligible-1", "body": "Canonical eligible text",
                    "population_status": "eligible"}) + "\n",
        encoding="utf-8",
    )
    (root / "test" / "sealed").mkdir(parents=True)
    (root / "test" / "sealed" / "manifest.protected.jsonl").write_text(
        json.dumps({"item_id": "sealed-1", "text_hash": "protected-hash"}) + "\n",
        encoding="utf-8",
    )
    return root


def test_label_and_embedding_inputs_are_bound_to_canonical_eligible_rows(tmp_path: Path) -> None:
    root = _v2_root(tmp_path)
    config = yaml.safe_load((root / "config.yaml").read_text(encoding="utf-8"))
    eligible_only = [{"id": "eligible-1"}]

    labeled = label._canonical_v2_items(root, config, eligible_only)
    embedded = embed._canonical_v2_items(root, eligible_only)
    assert labeled[0]["text"] == embedded[0]["text"] == "Canonical eligible text"
    assert labeled[0]["item_id"] == embedded[0]["item_id"] == "eligible-1"
    assert labeled[0]["population_status"] == embedded[0]["population_status"] == "eligible"

    bad_inputs = [
        {"id": "sealed-1", "text": "SEALED SECRET TEXT"},
        {"id": "caller-invented", "text": "arbitrary text"},
        {"id": "eligible-1", "text": "different text"},
    ]
    for bad in bad_inputs:
        with pytest.raises(ValueError):
            label._canonical_v2_items(root, config, [bad])
        with pytest.raises(ValueError):
            embed._canonical_v2_items(root, [bad])


def test_generic_embed_command_sends_only_canonical_v2_text_to_encoder(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _v2_root(tmp_path)
    input_path = tmp_path / "input.jsonl"
    output_path = tmp_path / "output.jsonl"
    seen: list[str] = []

    class Backend:
        def encode(self, texts: list[str]):
            seen.extend(texts)
            return np.ones((len(texts), 3), dtype="float32")

    monkeypatch.setattr(embed, "guard_job_root", lambda *_args: None)
    monkeypatch.setattr(embed, "_make_backend", lambda _cfg: Backend())
    input_path.write_text(json.dumps({"id": "eligible-1"}) + "\n", encoding="utf-8")
    embed.cmd_embed(root, input_path, output_path)
    assert seen == ["Canonical eligible text"]

    input_path.write_text(json.dumps({"id": "sealed-1", "text": "SEALED SECRET TEXT"}) + "\n",
                          encoding="utf-8")
    with pytest.raises(ValueError, match="canonical eligible"):
        embed.cmd_embed(root, input_path, output_path)
    assert seen == ["Canonical eligible text"]
