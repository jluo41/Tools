"""lm_labeler(items, guideline, engine) (b15 s42-D54): one tool, many engines; label, region, confidence, reason."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


calib_test = _load("sl_calibration_test_for_lm_labeler", "test_calibration.py")
label = _load("sl_label_lm_labeler_test", "label.py")


def _dev(root):
    return [json.loads(l)["item_id"] for l in (root / "corpus" / "items.jsonl").open()
            if json.loads(l).get("population_status") == "eligible"]


def test_an_open_engine_labels_with_the_context_and_returns_regions(tmp_path, monkeypatch):
    root, _ = calib_test.confirmed_job(tmp_path)
    seen = []

    async def fake(system_prompt, text, model):
        seen.append((system_prompt, text, model))
        return json.dumps({"label": "high", "region": "HL", "confidence": 0.6, "reason": "unsure"})

    monkeypatch.setitem(label.ENGINES, "ollama", fake)
    ids = _dev(root)[:2]
    out = label.lm_labeler(root, ids, "G_00", "ollama", output=tmp_path / "out.jsonl")
    assert [r["id"] for r in out] == ids and {r["region"] for r in out} == {"HL"}
    assert {r["model"] for r in out} == {"gpt-oss:20b"}
    assert all("Before:" in t and "Judge this reply:" in t for _, t, _ in seen)
    assert '"region"' in seen[0][0]                             # the output contract asks for the region


def test_a_missing_key_holds_before_anything_is_sent(tmp_path, monkeypatch):
    root, _ = calib_test.confirmed_job(tmp_path)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(SystemExit, match="OPENROUTER_API_KEY"):
        label.lm_labeler(root, _dev(root)[:1], "G_00", "openrouter")


def test_a_sealed_item_is_never_sent(tmp_path):
    root, _ = calib_test.confirmed_job(tmp_path)
    with pytest.raises(ValueError, match="not a canonical eligible"):
        label.lm_labeler(root, sorted(calib_test.sealed_ids(root))[:1], "G_00", "ollama")


def test_a_region_outside_the_set_is_a_parse_failure():
    parse = label._make_parser(["high", "low", "none"], ["H", "L", "N", "HL", "LN", "HN", "HLN"])
    assert parse('{"label": "low", "region": "XX"}')["reason"] == "parse_error:region_not_in_set"
    assert parse('{"label": "low", "region": "ln", "confidence": 0.7}')["region"] == "LN"
