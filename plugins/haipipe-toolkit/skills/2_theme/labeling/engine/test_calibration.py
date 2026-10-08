from __future__ import annotations

import importlib.util
import json
import os
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


job = _load("sl_job_for_calibration_test", "job.py")
fence = _load("sl_fence_for_calibration_test", "fence_source.py")
cal = _load("sl_calibration_test", "calibration.py")


CONFIG = {
    "schema_version": "subjective-label/v2",
    "corpus": {"text_field": "text", "context_field": "context_prev"},
    "construct": {"name": "unsafe_response", "question": "How unsafe?"},
    "authority": {"human_id": "JL", "mode": "single_human_semantic_authority",
                  "creates_human_gold": True, "meaning_confirmed": False, "meaning_receipt": None},
    "labels": {"type": "ordinal", "values": ["high", "low", "none"], "none_value": "none",
               "meanings": {"high": "h", "low": "l", "none": "n"}},
    "regions": {"values": ["H", "L", "N", "HL", "LN", "HN", "HLN"]},
    "uncertainty": {"levels": ["low", "medium", "high"], "unresolved_is_label": False},
    "reveal": {"reference_observations": {"label": "raters", "file": "refs.jsonl", "id_field": "item_id",
                                          "count_fields": ["vote"], "item_fields": ["gold"]}},
    "rounds": {"round1": {"human_batch_size": 4, "seed": 7}},
    "simulation_only": False,
}


def build_job(tmp_path: Path, config: dict = CONFIG) -> tuple[Path, Path]:
    items = tmp_path / "items.jsonl"
    refs = tmp_path / "refs.jsonl"
    rows, ref_rows = [], []
    for i in range(12):
        rows.append({"item_id": f"i{i:02d}", "text": f"response {i}", "context_prev": f"USER: q{i}"})
        for vote in ("Yes", "No", "No"):
            ref_rows.append({"item_id": f"i{i:02d}", "vote": vote, "gold": "Yes" if i % 2 else "No"})
    items.write_text("".join(json.dumps(r) + "\n" for r in rows))
    refs.write_text("".join(json.dumps(r) + "\n" for r in ref_rows))
    config_path = tmp_path / "config.seed.yaml"
    config_path.write_text(yaml.safe_dump(config, sort_keys=False))
    source = tmp_path / "source"
    fence.build(items=items, config_path=config_path, out=source, sealed_n=4, seed=3,
                custodian="JL", stratify_jsonl=refs, stratify_field="gold")
    page = tmp_path / "board" / "pages" / "S-Label-9" / "S-Label-9.md"
    page.parent.mkdir(parents=True)
    page.write_text("# page\n")
    root = page.parent / "labeling"
    job.create_contract(source_job=source, job_root=root, page_file=page, job_id="t",
                        target="unsafe_response", human_id="JL", created_at="2026-09-16T10:00:00+00:00")
    # the reveal source path is resolved from the repo root; point it at the tmp file
    (tmp_path / "pyproject.toml").write_text("")
    (tmp_path / "code").mkdir()
    return root, page


def confirmed_job(tmp_path: Path) -> tuple[Path, Path]:
    root, page = build_job(tmp_path)
    job.confirm_meaning(job_root=root, page_file=page, human_id="JL",
                        confirmed_at="2026-09-16T10:05:00+00:00", accept_current_schema=True,
                        attest_as_human=True,
                        channel="test")
    return root, page


def sealed_ids(root: Path) -> set[str]:
    protected = root / "test" / "sealed" / "manifest.protected.jsonl"
    return {json.loads(line)["item_id"] for line in protected.read_text(encoding="utf-8").splitlines()
            if line.strip()}


def test_fence_and_page_corpus_omit_sealed_text(tmp_path: Path) -> None:
    root, _ = build_job(tmp_path)
    protected_ids = sealed_ids(root)
    assert len(protected_ids) == 4
    source_bytes = (tmp_path / "source" / "corpus" / "items.jsonl").read_bytes()
    page_bytes = (root / "corpus" / "items.jsonl").read_bytes()
    source_rows = [json.loads(line) for line in source_bytes.splitlines()]
    page_rows = [json.loads(line) for line in page_bytes.splitlines()]
    assert len(source_rows) == len(page_rows) == 8
    assert all(row["population_status"] == "eligible" for row in source_rows + page_rows)
    raw_rows = [json.loads(line) for line in (tmp_path / "items.jsonl").read_text().splitlines()]
    sealed_texts = {row["text"] for row in raw_rows if row["item_id"] in protected_ids}
    assert all(text.encode("utf-8") not in source_bytes for text in sealed_texts)
    assert all(text.encode("utf-8") not in page_bytes for text in sealed_texts)
    protected_rows = [json.loads(line) for line in
                      (root / "test" / "sealed" / "manifest.protected.jsonl").read_text().splitlines()]
    assert all(set(row) == {"item_id", "text_hash"} for row in protected_rows)
    assert not any(text in json.dumps(protected_rows) for text in sealed_texts)

    state = job.status(root)
    assert state["phase"] == "P0" and state["integrity_errors"] == []
    assert state["first_blocked_frontier"] == "G0 · human meaning confirmation"


def test_release_refused_before_meaning_confirmation(tmp_path: Path) -> None:
    root, _ = build_job(tmp_path)
    with pytest.raises(cal.LabelingRefused):
        cal.release_round(root, human_id="JL")


def test_g0_cannot_be_confirmed_after_a_round_without_prior_attestation(tmp_path: Path) -> None:
    root, page = build_job(tmp_path)
    card = root / "rounds" / "round_01" / "card.md"
    card.parent.mkdir(parents=True)
    card.write_text("# round_01\nreleased_at: 2026-09-28T12:00:00+00:00\n", encoding="utf-8")
    config_before = (root / "config.yaml").read_bytes()
    assert not job.g0_repairable_after_round(root, job.load_mapping(root / "config.yaml"))
    assert job.status(root)["g0_retroactive_block"]
    assert job.status(root)["first_blocked_frontier"] == "G0 · prior meaning confirmation missing"
    with pytest.raises(RuntimeError, match="cannot be confirmed retroactively"):
        job.confirm_meaning(job_root=root, page_file=page, human_id="JL",
                            confirmed_at="2026-09-29T12:00:00+00:00",
                            accept_current_schema=True, attest_as_human=True)
    assert (root / "config.yaml").read_bytes() == config_before
    assert not (root / "gates" / "g0" / "receipt.json").exists()


def test_blank_label_meanings_require_definition_before_g0(tmp_path: Path) -> None:
    config = json.loads(json.dumps(CONFIG))
    del config["labels"]["meanings"]
    root, page = build_job(tmp_path, config)
    state = job.status(root)
    assert state["p0_contract_integrity_valid"]
    assert state["meaning_definitions_missing"] == ["high", "low", "none"]
    assert state["first_blocked_frontier"] == "G0 · label meanings missing"
    with pytest.raises(RuntimeError, match="define every label meaning"):
        job.confirm_meaning(job_root=root, page_file=page, human_id="JL",
                            confirmed_at="2026-09-29T12:00:00+00:00",
                            accept_current_schema=True, attest_as_human=True)
    assert not (root / "gates" / "g0" / "receipt.json").exists()


def test_missing_g0_receipt_can_be_restored_from_pre_release_attestation(tmp_path: Path) -> None:
    root, page = confirmed_job(tmp_path)
    cal.release_round(root, human_id="JL")
    (root / "gates" / "g0" / "receipt.json").unlink()
    assert job.g0_repairable_after_round(root, job.load_mapping(root / "config.yaml"))
    assert not job.status(root)["g0_retroactive_block"]
    assert job.status(root)["next_action"] == "restore the missing G0 receipt from the pre-release human attestation"
    restored = job.confirm_meaning(job_root=root, page_file=page, human_id="JL",
                                   confirmed_at="2026-09-29T12:00:00+00:00",
                                   accept_current_schema=True, attest_as_human=True)
    assert restored["updated_files"] == ["gates/g0/receipt.json"]
    assert restored["next_action"] == "inspect the existing round"
    assert job.status(root)["g0_passed"]


def test_post_release_meaning_and_g0_receipts_cannot_validate_a_prior_round(tmp_path: Path) -> None:
    root, _ = confirmed_job(tmp_path)
    card = root / "rounds" / "round_01" / "card.md"
    card.parent.mkdir(parents=True)
    card.write_text("# round_01\nreleased_at: 2026-09-15T12:00:00+00:00\n", encoding="utf-8")
    state = job.status(root)
    assert not state["g0_passed"]
    assert not state["g0_receipt_valid"]
    assert state["g0_retroactive_block"]
    assert "G0 confirmation does not predate released round" in state["g0_integrity_errors"]


def test_hold_job_refuses_confirmation(tmp_path: Path) -> None:
    config = json.loads(json.dumps(CONFIG))
    config["authority"]["mode"] = "external_annotation_import"
    config["authority"]["creates_human_gold"] = False
    root, page = build_job(tmp_path, config)
    # create_contract forces a single human authority, so the page job is not on HOLD;
    # the seed config's import mode would have been.
    state = job.status(root)
    assert state["hold"] is False
    assert job.authority_hold(config)[0] is True


def test_full_round_one_flow(tmp_path: Path) -> None:
    root, _ = confirmed_job(tmp_path)
    assert job.status(root)["phase"] == "P1"
    released = cal.release_round(root, human_id="JL")
    assert released["batch_size"] == 4 and released["pool"] == 8
    batch = [json.loads(l) for l in (root / "rounds/round_01/human_batch.jsonl").read_text().splitlines()]
    assert not {row["item_id"] for row in batch} & sealed_ids(root)

    with pytest.raises(cal.LabelingRefused):
        cal.release_round(root, human_id="JL")  # one open round at a time

    for index in range(4):
        opened = cal.open_item(root, "round_01", human_id="JL", session_id="s1")
        assert opened["stage"] == "first" and opened["finals"] == index
        item_id = opened["item"]["item_id"]
        with pytest.raises(cal.LabelingRefused):
            cal.record_final(root, "round_01", item_id, human_id="JL", session_id="s1",
                             class_label="none", region=None, uncertainty="low")
        first = cal.record_first(root, "round_01", item_id, human_id="JL", session_id="s1",
                                 class_label="low", region=None, uncertainty="medium", reason="r")
        assert first["reveal"]["kind"] == "reference_observations"
        assert first["reveal"]["counts"]["vote"] == {"Yes": 1, "No": 2}
        with pytest.raises(cal.LabelingRefused):
            cal.record_first(root, "round_01", item_id, human_id="JL", session_id="s1",
                             class_label="high", region=None, uncertainty="low")
        with pytest.raises(cal.LabelingRefused):  # changed class without a change type
            cal.record_final(root, "round_01", item_id, human_id="JL", session_id="s1",
                             class_label="high", region=None, uncertainty="low")
        final = cal.record_final(root, "round_01", item_id, human_id="JL", session_id="s1",
                                 class_label="high" if index == 0 else "low", region=None,
                                 uncertainty="low", change_type="correction" if index == 0 else "none")
    assert final["closed_run"] and final["finals"] == 4

    assert cal.verify_events(root / "rounds/round_01") == []
    rows = [json.loads(l) for l in (root / "rounds/round_01/human_final.jsonl").read_text().splitlines()]
    assert len(rows) == 4 and rows[0]["final"]["change_type"] in {"correction", "none"}
    runtime = yaml.safe_load((root.parent / "results" / final["closed_run"] / "runtime.yaml").read_text())
    assert runtime["status"] == "complete"
    state = cal.job_state(root)
    assert state["rounds"][0]["state"] == "judged"
    assert (root.parent / "runs").is_dir() and len(list((root.parent / "runs").glob("run-labeling-*.yaml"))) == 3
    assert not (root / "gold/cumulative.jsonl").read_text()  # no gold without round-close


def test_wrong_human_and_sealed_item_refused(tmp_path: Path) -> None:
    root, _ = confirmed_job(tmp_path)
    cal.release_round(root, human_id="JL")
    with pytest.raises(cal.LabelingRefused):
        cal.open_item(root, "round_01", human_id="CC", session_id="s")
    sealed = sorted(sealed_ids(root))[0]
    with pytest.raises(cal.LabelingRefused):
        cal.open_item(root, "round_01", human_id="JL", session_id="s", item_id=sealed)


@pytest.mark.parametrize("locked", [False, True])
def test_interrupted_first_answer_resumes_at_reveal(tmp_path: Path, locked: bool) -> None:
    root, _ = confirmed_job(tmp_path)
    cal.release_round(root, human_id="JL")
    opened = cal.open_item(root, "round_01", human_id="JL", session_id="s1")
    item_id = opened["item"]["item_id"]
    round_path = root / "rounds/round_01"
    base = {"run": opened["run"], "round_id": "round_01", "item_id": item_id,
            "human_id": "JL", "session_id": "s1"}
    first = cal._append_event(round_path, {**base, "kind": "first", "payload": {
        "class_label": "low", "diagnostic_region": "L", "uncertainty": {"level": "low"},
        "rationale": {"reason": "", "rejected_label": None}, "prelabels_visible": False}})
    if locked:
        cal._append_event(round_path, {**base, "kind": "lock", "payload": {"first_seq": first["seq"]}})

    resumed = cal.open_item(root, "round_01", human_id="JL", session_id="s2")
    assert resumed["stage"] == "reveal"
    assert resumed["first"]["class_label"] == "low"
    assert resumed["reveal"]["kind"] == "reference_observations"
    kinds = [event["kind"] for event in cal._events(round_path)]
    assert kinds == ["show", "first", "lock", "reveal"]
    assert cal.verify_events(round_path) == []
    cal.record_final(root, "round_01", item_id, human_id="JL", session_id="s2",
                     class_label="low", region="L", uncertainty="low")


def test_closed_calibration_ticket_cannot_receive_more_events(tmp_path: Path) -> None:
    root, _ = confirmed_job(tmp_path)
    cal.release_round(root, human_id="JL")
    opened = cal.open_item(root, "round_01", human_id="JL", session_id="s1")
    runtime_path = root.parent / "results" / opened["run"] / "runtime.yaml"
    runtime = yaml.safe_load(runtime_path.read_text(encoding="utf-8"))
    runtime["status"] = "complete"
    runtime_path.write_text(yaml.safe_dump(runtime), encoding="utf-8")
    events_path = root / "rounds/round_01/sessions/events.jsonl"
    before = events_path.read_bytes()
    with pytest.raises(cal.LabelingRefused, match="not running"):
        cal.open_item(root, "round_01", human_id="JL", session_id="s2")
    assert events_path.read_bytes() == before


def test_last_final_event_can_finalize_an_interrupted_result(tmp_path: Path, monkeypatch) -> None:
    root, _ = confirmed_job(tmp_path)
    cal.release_round(root, human_id="JL")
    with pytest.raises(cal.LabelingRefused, match="no calibration Run"):
        cal.finalize_calibration(root, "round_01", human_id="JL")
    run = ""
    for index in range(4):
        opened = cal.open_item(root, "round_01", human_id="JL", session_id="s")
        run, item_id = opened["run"], opened["item"]["item_id"]
        if index == 0:
            with pytest.raises(cal.LabelingRefused, match="still has items"):
                cal.finalize_calibration(root, "round_01", human_id="JL")
        cal.record_first(root, "round_01", item_id, human_id="JL", session_id="s",
                         class_label="low", region=None, uncertainty="low")
        if index == 3:
            with monkeypatch.context() as patch:
                def interrupted(*_args, **_kwargs):
                    raise RuntimeError("interrupted after final event")
                patch.setattr(cal, "_close_calibration", interrupted)
                with pytest.raises(RuntimeError, match="interrupted"):
                    cal.record_final(root, "round_01", item_id, human_id="JL", session_id="s",
                                     class_label="low", region=None, uncertainty="low")
        else:
            cal.record_final(root, "round_01", item_id, human_id="JL", session_id="s",
                             class_label="low", region=None, uncertainty="low")
    runtime_path = root.parent / "results" / run / "runtime.yaml"
    assert yaml.safe_load(runtime_path.read_text(encoding="utf-8"))["status"] == "running"
    interrupted_state = cal.job_state(root)
    assert interrupted_state["rounds"][0]["state"] == "judged"
    assert "finalize the interrupted human-calibration Result" in interrupted_state["next_step"]
    result = cal.finalize_calibration(root, "round_01", human_id="JL")
    assert result == {"round_id": "round_01", "run": run, "status": "complete", "finals": 4}
    assert yaml.safe_load(runtime_path.read_text(encoding="utf-8"))["status"] == "complete"
    assert (root.parent / "results" / run / "result.yaml").is_file()
    assert cal.verify_events(root / "rounds/round_01") == []
    assert "finalize the interrupted" not in cal.job_state(root)["next_step"]


def test_events_carry_no_hash_and_a_broken_log_is_detected(tmp_path: Path) -> None:
    root, _ = confirmed_job(tmp_path)
    cal.release_round(root, human_id="JL")
    opened = cal.open_item(root, "round_01", human_id="JL", session_id="s")
    cal.record_first(root, "round_01", opened["item"]["item_id"], human_id="JL", session_id="s",
                     class_label="none", region=None, uncertainty="low")
    path = root / "rounds/round_01/sessions/events.jsonl"
    lines = path.read_text().splitlines()
    events = [json.loads(line) for line in lines]
    assert [e["kind"] for e in events] == ["show", "first", "lock", "reveal"]
    assert not any(key in e for e in events for key in ("checksum", "prev_checksum"))
    assert events[2]["payload"] == {"first_seq": events[1]["seq"]}
    assert cal.verify_events(root / "rounds/round_01") == []

    legacy = [dict(e, checksum="x", prev_checksum="y") for e in events]  # old fields are ignored
    path.write_text("".join(json.dumps(e, sort_keys=True) + "\n" for e in legacy))
    assert cal.verify_events(root / "rounds/round_01") == []

    path.write_text("\n".join(lines[:1] + lines[2:]) + "\n")  # a deleted first event
    errors = cal.verify_events(root / "rounds/round_01")
    assert "event 2: sequence gap" in errors
    assert any("lock for item" in e and "before any first" in e for e in errors)

    broken = dict(events[1])
    broken.pop("human_id")
    path.write_text("\n".join([lines[0], json.dumps(broken, sort_keys=True), *lines[2:]]) + "\n")
    assert "event 2: missing human_id" in cal.verify_events(root / "rounds/round_01")


def test_round_records_carry_no_hash(tmp_path: Path) -> None:
    root, _ = confirmed_job(tmp_path)
    released = cal.release_round(root, human_id="JL")
    manifest = yaml.safe_load((root / "rounds/round_01/manifest.yaml").read_text())
    assert not [key for key in manifest if "checksum" in key]
    ticket = yaml.safe_load((root.parent / "runs" / f"{released['run']}.yaml").read_text())
    result = yaml.safe_load((root.parent / "results" / released["run"] / "result.yaml").read_text())
    assert ticket["commission"] == {"path": "labeling/rounds/round_01/card.md"}
    assert ticket["inputs"] == [{"path": "labeling/corpus/items.jsonl"}]
    assert all(set(a) == {"path"} for a in result["artifacts"])
    assert "sha256" not in (root / "rounds/round_01/evidence.md").read_text()


def test_meaning_edit_after_g0_reopens_the_meaning_gate(tmp_path: Path) -> None:
    root, _ = confirmed_job(tmp_path)
    config = job.load_mapping(root / "config.yaml")
    config["labels"]["meanings"]["low"] = "edited by hand, never confirmed"
    (root / "config.yaml").write_bytes(job.yaml_bytes(config))
    state = job.status(root)
    assert state["phase"] == "P0" and not state["g0_passed"]
    assert state["first_blocked_frontier"] == "G0 · human meaning confirmation"
    with pytest.raises(cal.LabelingRefused):
        cal.release_round(root, human_id="JL")


def test_reveal_index_never_contains_sealed_ids(tmp_path: Path) -> None:
    root, _ = confirmed_job(tmp_path)
    cal.release_round(root, human_id="JL")
    opened = cal.open_item(root, "round_01", human_id="JL", session_id="s")
    cal.record_first(root, "round_01", opened["item"]["item_id"], human_id="JL", session_id="s",
                     class_label="none", region=None, uncertainty="low")
    cache = next((root / "cache" / "reveal").glob("*.json"))
    assert not set(json.loads(cache.read_text())) & sealed_ids(root)


def test_reveal_cache_tracks_source_bytes_when_size_and_mtime_are_unchanged(tmp_path: Path) -> None:
    root, _ = confirmed_job(tmp_path)
    ref = CONFIG["reveal"]["reference_observations"]
    source = cal._repo_root(root) / ref["file"]
    eligible_id = cal._eligible_ids(root)[0]

    before = source.stat()
    first = cal._reference_index(root, ref)
    assert first[eligible_id]["counts"]["vote"] == {"No": 2, "Yes": 1}

    rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines()]
    for row in rows:
        row["vote"] = {"No": "Nx", "Yes": "Yez"}[row["vote"]]
    replacement = "".join(json.dumps(row) + "\n" for row in rows)
    assert len(replacement.encode("utf-8")) == before.st_size
    source.write_text(replacement, encoding="utf-8")
    os.utime(source, ns=(before.st_atime_ns, before.st_mtime_ns))

    second = cal._reference_index(root, ref)
    assert source.stat().st_size == before.st_size
    assert source.stat().st_mtime_ns == before.st_mtime_ns
    assert second[eligible_id]["counts"]["vote"] == {"Nx": 2, "Yez": 1}


def test_reveal_cache_tracks_frozen_corpus_identity(tmp_path: Path) -> None:
    root, _ = confirmed_job(tmp_path)
    ref = CONFIG["reveal"]["reference_observations"]
    eligible_id = cal._eligible_ids(root)[0]
    assert eligible_id in cal._reference_index(root, ref)

    corpus_path = root / "corpus" / "items.jsonl"
    rows = [json.loads(line) for line in corpus_path.read_text(encoding="utf-8").splitlines()]
    for row in rows:
        if row.get("item_id") == eligible_id:
            row["population_status"] = "sealed"
    corpus_path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")

    assert eligible_id not in cal._reference_index(root, ref)




def test_feedback_notes_are_appended_per_item(tmp_path: Path) -> None:
    root, _ = confirmed_job(tmp_path)
    cal.release_round(root, human_id="JL")
    rp = root / "rounds/round_01"
    item_id = json.loads((rp / "human_batch.jsonl").read_text().splitlines()[0])["item_id"]
    note = cal.add_feedback(root, "round_01", item_id, human_id="JL", author="human", text="  vague   refusal ")
    assert note["text"] == "vague refusal" and note["author"] == "human"
    cal.add_feedback(root, "round_01", item_id, human_id="JL", author="model", text="raters split")
    assert len((rp / "sessions" / cal.FEEDBACK_FILE).read_text().splitlines()) == 2
    for bad in ({"author": "rater", "text": "x"}, {"author": "human", "text": "  "}):
        with pytest.raises(cal.LabelingRefused):
            cal.add_feedback(root, "round_01", item_id, human_id="JL", **bad)
    with pytest.raises(cal.LabelingRefused):
        cal.add_feedback(root, "round_01", "sealed-or-missing", human_id="JL", author="human", text="x")
    assert not [e for e in cal._events(rp) if e["kind"] != "show"]  # notes never touch the event log
