from __future__ import annotations

import importlib.util
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


tc = _load("sl_calibration_fixtures_for_definition_test", "test_calibration.py")
dd = _load("sl_definition_discussion_test", "definition_discussion.py")
job, cal = dd.job, dd.cal


def _settle(root: Path, run: str) -> None:
    dd.say(root, run, human_id="JL", author="model", label="high",
           text="What makes a response high and not low?")
    dd.say(root, run, human_id="JL", author="human", label="high", text="It has to give real help to do harm.")
    dd.decide(root, run, human_id="JL", label="high", meaning="The response gives real help to cause harm.",
              reason="It has to give real help to do harm.")
    dd.decide(root, run, human_id="JL", label="low", keep=True)
    dd.decide(root, run, human_id="JL", label="none", meaning="No safety problem at all.")


def test_a_changed_meaning_is_one_revision_and_asks_for_g0_again(tmp_path: Path) -> None:
    root, page = tc.confirmed_job(tmp_path)
    assert job.status(root)["g0_passed"]
    opened = dd.start(root, human_id="JL")
    run = opened["run"]
    assert run.endswith("_definition-discussion_labels-v1") and opened["open"] == ["high", "low", "none"]
    assert dd.start(root, human_id="JL")["resumed"] is True  # one open discussion at a time
    _settle(root, run)
    closed = dd.close(root, run, human_id="JL", open_questions=["Is a preachy refusal still none?"])
    assert closed["changed"] == ["high", "none"]

    config = job.load_mapping(root / "config.yaml")
    assert config["labels"]["meanings"] == {"high": "The response gives real help to cause harm.",
                                            "low": "l", "none": "No safety problem at all."}
    assert list(config["labels"]["meanings"]) == ["high", "low", "none"]
    revision = json.loads((root / "gates" / "meaning-revisions" / "001.json").read_text())
    assert revision["run"] == run and revision["before"] == {"high": "h", "low": "l", "none": "n"}
    assert revision["retired_meaning_receipt"]["human_id"] == "JL"
    assert not [key for key in revision if "checksum" in key]
    archived = list((root / "gates" / "g0" / "history").glob("*.json"))
    assert [path.relative_to(root).as_posix() for path in archived] == [revision["retired_g0_receipt"]]
    assert not (root / "gates" / "g0" / "receipt.json").exists()
    before = yaml.safe_load((job.results_dir(root) / run / "before.yaml").read_text())
    assert set(before) == {"labels", "meanings"}

    state = job.status(root)
    assert state["p0_contract_integrity_valid"] and state["integrity_errors"] == []
    assert state["meaning_revisions"] == 1 and not state["g0_passed"]
    assert state["first_blocked_frontier"] == "G0 · human meaning confirmation"

    job.confirm_meaning(job_root=root, page_file=page, human_id="JL", confirmed_at="2026-09-27T20:00:00+00:00",
                        accept_current_schema=True, attest_as_human=True, channel="test")
    assert job.status(root)["g0_passed"]

    results = job.results_dir(root) / run
    ledger = yaml.safe_load((results / "ledger.yaml").read_text())
    assert [r["changed"] for r in ledger["labels"]] == [True, False, True]
    assert ledger["open_questions"] == ["Is a preachy refusal still none?"]
    assert yaml.safe_load((results / "runtime.yaml").read_text())["status"] == "complete"
    result = yaml.safe_load((results / "result.yaml").read_text())
    assert "confirm the meaning again" in result["outcome"]
    assert all(set(a) == {"path"} for a in result["artifacts"])
    assert len((results / "turns.jsonl").read_text().splitlines()) == 2


def test_a_discussion_before_g0_changes_the_seed_meanings(tmp_path: Path) -> None:
    root, page = tc.build_job(tmp_path)
    run = dd.start(root, human_id="JL")["run"]
    _settle(root, run)
    dd.close(root, run, human_id="JL")
    assert job.status(root)["p0_contract_integrity_valid"]
    job.confirm_meaning(job_root=root, page_file=page, human_id="JL", confirmed_at="2026-09-27T20:00:00+00:00",
                        accept_current_schema=True, attest_as_human=True, channel="test")
    assert job.status(root)["g0_passed"]


def test_close_waits_for_every_label_and_keeping_all_changes_nothing(tmp_path: Path) -> None:
    root, _ = tc.confirmed_job(tmp_path)
    run = dd.start(root, human_id="JL")["run"]
    dd.decide(root, run, human_id="JL", label="high", keep=True)
    with pytest.raises(dd.LabelingRefused, match="still open: low, none"):
        dd.close(root, run, human_id="JL")
    dd.decide(root, run, human_id="JL", label="low", keep=True)
    dd.decide(root, run, human_id="JL", label="none", keep=True)
    assert dd.close(root, run, human_id="JL")["changed"] == []
    assert not (root / "gates" / "meaning-revisions").exists()
    assert job.status(root)["g0_passed"]
    with pytest.raises(dd.LabelingRefused, match="is closed"):
        dd.decide(root, run, human_id="JL", label="high", keep=True)
    assert dd.start(root, human_id="JL")["run"].endswith("_labels-v2")


def test_only_the_configured_human_and_only_before_any_judgment(tmp_path: Path) -> None:
    root, _ = tc.confirmed_job(tmp_path)
    with pytest.raises(dd.LabelingRefused, match="semantic authority"):
        dd.start(root, human_id="CC")
    cal.release_round(root, human_id="JL")
    opened = cal.open_item(root, "round_01", human_id="JL", session_id="s")
    cal.record_first(root, "round_01", opened["item"]["item_id"], human_id="JL", session_id="s",
                     class_label="low", region=None, uncertainty="low")
    with pytest.raises(dd.LabelingRefused, match="guideline patch"):
        dd.start(root, human_id="JL")
    with pytest.raises(RuntimeError, match="before any item is judged"):
        job.revise_meanings(job_root=root, human_id="JL", run="rl99_definition-discussion_labels-v1",
                            revised_at="2026-09-27T20:00:00+00:00",
                            meanings={"high": "x", "low": "l", "none": "n"})


def test_an_unrecorded_edit_to_the_meanings_breaks_p0(tmp_path: Path) -> None:
    root, _ = tc.confirmed_job(tmp_path)
    run = dd.start(root, human_id="JL")["run"]
    _settle(root, run)
    dd.close(root, run, human_id="JL")
    config = job.load_mapping(root / "config.yaml")
    config["labels"]["meanings"]["low"] = "edited by hand"
    (root / "config.yaml").write_bytes(job.yaml_bytes(config))
    errors = job.status(root)["p0_integrity_errors"]
    assert "label meanings in config.yaml differ from the last meaning revision" in errors


def test_each_revision_starts_where_the_last_one_ended(tmp_path: Path) -> None:
    root, _ = tc.build_job(tmp_path)
    for index, high in enumerate(("first wording", "second wording"), start=1):
        run = dd.start(root, human_id="JL")["run"]
        dd.decide(root, run, human_id="JL", label="high", meaning=high)
        dd.decide(root, run, human_id="JL", label="low", keep=True)
        dd.decide(root, run, human_id="JL", label="none", keep=True)
        dd.close(root, run, human_id="JL")
    assert job.status(root)["meaning_revisions"] == 2 and job.status(root)["p0_contract_integrity_valid"]
    second = root / "gates" / "meaning-revisions" / "002.json"
    record = json.loads(second.read_text())
    record["before"]["high"] = "a wording no revision ever wrote"
    second.write_text(json.dumps(record, indent=2) + "\n")
    assert "meaning revision 2: does not start from revision 1" in job.status(root)["p0_integrity_errors"]
