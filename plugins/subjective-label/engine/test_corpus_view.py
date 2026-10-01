from __future__ import annotations

import csv
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


calib_test = _load("sl_calibration_test_for_corpus_view", "test_calibration.py")
view = _load("sl_corpus_view_test", "corpus_view.py")


def test_item_page_shows_development_items_only_and_logs_what_was_shown(tmp_path) -> None:
    root, _page = calib_test.confirmed_job(tmp_path)
    sealed = {str(json.loads(line)["item_id"]) for line in (root / "corpus" / "items.jsonl").open()
              if json.loads(line).get("population_status") == "sealed"}
    first = view.item_page(root, offset=0, k=5, human_id="JL", channel="test")
    assert first["total"] == 8 and first["more"] is True
    assert [it["item_id"] for it in first["items"]] == sorted(it["item_id"] for it in first["items"])
    assert all(it["state"] == "to label" and it["text"].startswith("response") for it in first["items"])
    rest = view.item_page(root, offset=5, k=5, human_id="JL", channel="test")
    shown = [it["item_id"] for it in first["items"] + rest["items"]]
    assert len(shown) == 8 and not sealed & set(shown)
    log = [json.loads(line) for line in (root / "exposure" / "group_examples.jsonl").open()]
    assert [entry["where"] for entry in log] == ["preparation item table"] * 2
    assert sum(len(entry["item_ids"]) for entry in log) == 8


def test_item_page_keeps_a_waiting_round_item_for_the_rounds_screen(tmp_path) -> None:
    root, _page = calib_test.confirmed_job(tmp_path)
    calib_test.cal.release_round(root, human_id="JL", n=2, channel="test")
    page = view.item_page(root, offset=0, k=50, human_id="JL", channel="test")
    waiting = [it for it in page["items"] if it["state"].startswith("waiting in round_01")]
    assert len(waiting) == 2 and all("text" not in it for it in waiting)


def test_item_page_refuses_bad_paging(tmp_path) -> None:
    root, _page = calib_test.confirmed_job(tmp_path)
    with pytest.raises(view.CorpusViewRefused):
        view.item_page(root, offset=0, k=0)


def test_raw_source_describes_the_folder_without_row_values(tmp_path) -> None:
    root, _page = calib_test.confirmed_job(tmp_path)
    folder = tmp_path / "raw"
    folder.mkdir()
    with (folder / "dialogs.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["item_id", "context", "response", "rater_vote"])
        for i in range(3):
            for vote in ("SECRET-YES", "SECRET-NO"):
                writer.writerow([f"i{i}", f"USER: q{i}", f"response {i}", vote])
    (root / "corpus" / "source.yaml").write_text(
        "schema: subjective-label/corpus-source-v1\nfolder: raw\nfile: dialogs.csv\n"
        "one_row_is: one rater's answer\nitem_key: item_id\n"
        "fields: {item_id: item_id, context: context_prev, response: text}\n", encoding="utf-8")
    raw = view.raw_source(root)
    assert raw["found"] is True
    (entry,) = raw["files"]
    assert entry["rows"] == 6 and entry["keys"] == 3
    assert entry["columns"] == ["item_id", "context", "response", "rater_vote"]
    assert "SECRET" not in json.dumps(raw)
