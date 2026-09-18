from __future__ import annotations

import hashlib
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


harness = _load("sl_calibration_harness_for_embedding_test", "test_calibration.py")
emb = _load("sl_embedding_build_test", "embedding_build.py")
job = harness.job


def fake_encoder(texts: list[str]):
    """Deterministic stand-in for a sentence model: no download, no network."""
    rows = []
    for text in texts:
        seed = int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:8], 16)
        rows.append(np.random.default_rng(seed).normal(size=16))
    return np.asarray(rows, dtype="float32")


def test_build_embeds_only_development_items_before_g0(tmp_path: Path) -> None:
    root, _ = harness.build_job(tmp_path)
    sealed = harness.sealed_ids(root)
    result = emb.build(root, model="org/Tiny-Model_v1", encoder=fake_encoder, channel="test")

    assert result["built"] is True and result["version"] == "tiny-model-v1"
    folder = root / "cache" / "embeddings" / "tiny-model-v1"
    manifest = json.loads((folder / "manifest.json").read_text())
    assert manifest["population"] == {
        "eligible_embedded": 8, "sealed_excluded": 4,
        "corpus_items_sha256": job.sha256_file(root / "corpus" / "items.jsonl"),
    }
    mapped = [json.loads(l) for l in (folder / "map.jsonl").read_text().splitlines()]
    embedded = [json.loads(l) for l in (folder / "rows.jsonl").read_text().splitlines()]
    assert len(mapped) == len(embedded) == 8
    assert not ({r["item_id"] for r in mapped} | {r["item_id"] for r in embedded}) & sealed
    assert np.load(folder / "vectors.npy").shape == (8, 16)
    assert all(0.0 <= r["x"] <= 1.0 and 0.0 <= r["y"] <= 1.0 for r in mapped)
    for entry in manifest["files"]:
        assert job.sha256_file(folder / entry["path"]) == entry["sha256"]

    run = result["run"]
    assert run.startswith("rl02_embedding-build_tiny-model-v1")
    runtime = yaml.safe_load((root / "results" / run / "runtime.yaml").read_text())
    assert runtime["status"] == "complete"
    assert (root / "results" / run / "result.yaml").is_file()
    ticket = yaml.safe_load((root / "runs" / f"{run}.yaml").read_text())
    assert ticket["phase"] == "P0" and ticket["commission"]["embedder"]["model"] == "org/Tiny-Model_v1"

    state = job.status(root)  # a representation Run never moves the gate or breaks P0
    assert state["phase"] == "P0" and state["integrity_errors"] == []


def test_rebuild_is_a_no_op(tmp_path: Path) -> None:
    root, _ = harness.build_job(tmp_path)
    first = emb.build(root, model="org/tiny", encoder=fake_encoder)
    again = emb.build(root, model="org/tiny", encoder=fake_encoder)
    assert again["built"] is False and again["run"] == first["run"]
    assert len(list((root / "runs").glob("rl*_embedding-build_*.yaml"))) == 1


def test_changed_corpus_is_refused(tmp_path: Path) -> None:
    root, _ = harness.build_job(tmp_path)
    items = root / "corpus" / "items.jsonl"
    items.write_text(items.read_text() + "\n")
    with pytest.raises(emb.EmbeddingRefused):
        emb.build(root, model="org/tiny", encoder=fake_encoder)
    assert not (root / "cache" / "embeddings" / "tiny").exists()


def test_failed_encoder_marks_the_run_failed(tmp_path: Path) -> None:
    root, _ = harness.build_job(tmp_path)

    def broken(texts):
        raise OSError("model download failed")

    with pytest.raises(OSError):
        emb.build(root, model="org/tiny", encoder=broken)
    runtime = yaml.safe_load(next((root / "results").glob("rl*_embedding-build_tiny/runtime.yaml")).read_text())
    assert runtime["status"] == "failed" and "model download failed" in runtime["failure"]


def test_latest_reads_map_and_groups(tmp_path: Path) -> None:
    root, _ = harness.build_job(tmp_path)
    assert emb.latest(root) is None
    emb.build(root, model="org/tiny", encoder=fake_encoder, groups=2)
    hit = emb.latest(root)
    assert hit is not None and len(hit["map"]) == 8
    assert hit["groups"]["k"] == 2 and sum(g["size"] for g in hit["groups"]["groups"]) == 8
    assert hit["groups"]["groups"][0]["size"] >= hit["groups"]["groups"][1]["size"]


def test_status_reports_each_catalog_model(tmp_path: Path) -> None:
    root, _ = harness.build_job(tmp_path)
    emb.build(root, model="sentence-transformers/all-MiniLM-L6-v2", encoder=fake_encoder)
    rows = {r["id"]: r for r in emb.build_status(root)}
    assert rows["sentence-transformers/all-MiniLM-L6-v2"]["state"] == "built"
    assert rows["Qwen/Qwen3-Embedding-0.6B"]["state"] == "none"
    assert not list((root / "cache" / "embeddings").glob(f"*/{emb.BUILD_MARKER}"))  # marker cleaned up


def test_failed_build_shows_as_failed_and_can_retry(tmp_path: Path) -> None:
    root, _ = harness.build_job(tmp_path)

    def broken(texts):
        raise OSError("model download failed")

    with pytest.raises(OSError):
        emb.build(root, model="BAAI/bge-m3", encoder=broken)
    row = next(r for r in emb.build_status(root) if r["id"] == "BAAI/bge-m3")
    assert row["state"] == "failed" and "model download failed" in row["failure"]
    again = emb.build(root, model="BAAI/bge-m3", encoder=fake_encoder)
    assert again["built"] is True and again["run"].startswith("rl03_")


def test_one_build_at_a_time_and_catalog_only(tmp_path: Path) -> None:
    root, _ = harness.build_job(tmp_path)
    busy = root / "cache" / "embeddings" / "bge-m3"
    busy.mkdir(parents=True)
    (busy / emb.BUILD_MARKER).write_text(json.dumps({"pid": 1, "model": "BAAI/bge-m3"}))  # pid 1 is alive
    with pytest.raises(emb.EmbeddingRefused, match="still building"):
        emb.build(root, model="org/tiny", encoder=fake_encoder)
    assert next(r for r in emb.build_status(root) if r["version"] == "bge-m3")["state"] == "building"
    (busy / emb.BUILD_MARKER).unlink()
    with pytest.raises(emb.EmbeddingRefused, match="not in the embedding catalog"):
        emb.start_background_build(root, "org/anything", channel="test", started_by="jl")
    with pytest.raises(emb.EmbeddingRefused, match="only when a person asks"):
        emb.start_background_build(root, "BAAI/bge-m3", channel="test", started_by="")


def test_neighbors_are_development_items_only(tmp_path: Path) -> None:
    root, _ = harness.build_job(tmp_path)
    sealed = harness.sealed_ids(root)
    emb.build(root, model="org/tiny", encoder=fake_encoder)
    hit = emb.neighbors(root, "tiny", "i00", k=3)
    assert hit["item_id"] == "i00" and len(hit["neighbors"]) == 3
    assert not {n["item_id"] for n in hit["neighbors"]} & sealed
    assert "i00" not in {n["item_id"] for n in hit["neighbors"]}
    assert hit["neighbors"] == sorted(hit["neighbors"], key=lambda n: -n["similarity"])
    with pytest.raises(emb.EmbeddingRefused):
        emb.neighbors(root, "tiny", next(iter(sealed)))
    with pytest.raises(emb.EmbeddingRefused):
        emb.neighbors(root, "not-built", "i00")


def test_settings_make_their_own_build_and_are_recorded(tmp_path: Path) -> None:
    root, _ = harness.build_job(tmp_path)
    plain = emb.build(root, model="Qwen/Qwen3-Embedding-0.6B", encoder=fake_encoder)
    steered = emb.build(root, model="Qwen/Qwen3-Embedding-0.6B", encoder=fake_encoder, input_mode="reply",
                        instruction="Represent this AI reply by how unsafe it is", groups=3,
                        map_method="pca", seed=7)
    assert plain["version"] == "qwen3-embedding-0-6b"
    assert steered["version"].startswith("qwen3-embedding-0-6b-reply-only-instr-")
    assert steered["version"].endswith("-k3-pca-seed7")
    m = steered["manifest"]
    assert m["settings"]["instruction"] == "Represent this AI reply by how unsafe it is"
    assert m["preprocessing"]["prompt"] == "Instruct: Represent this AI reply by how unsafe it is\nQuery:"
    assert m["groups"]["k"] == 3 and m["map"]["method"] == "pca"
    folder = root / "cache" / "embeddings" / steered["version"]
    assert len((folder / "map3d.jsonl").read_text().splitlines()) == 8
    rows = {r["version"]: r for r in emb.build_status(root)}
    assert rows[steered["version"]]["state"] == "built" and rows[steered["version"]]["variant"]
    assert "the reply only" in rows[steered["version"]]["settings_summary"]


def test_bad_settings_are_refused_before_any_work(tmp_path: Path) -> None:
    root, _ = harness.build_job(tmp_path)
    for kwargs in ({"input_mode": "everything"}, {"groups": 1}, {"groups": 50}, {"map_method": "umap"},
                   {"seed": -1}, {"instruction": "x" * 301}):
        with pytest.raises(emb.EmbeddingRefused):
            emb.build(root, model="Qwen/Qwen3-Embedding-0.6B", encoder=fake_encoder, **kwargs)
    with pytest.raises(emb.EmbeddingRefused, match="does not take an instruction"):
        emb.build(root, model="BAAI/bge-m3", encoder=fake_encoder, instruction="anything")
    assert not list((root / "runs").glob("rl*_embedding-build_*.yaml"))


def test_old_builds_get_a_3d_view_without_touching_vectors(tmp_path: Path) -> None:
    root, _ = harness.build_job(tmp_path)
    emb.build(root, model="org/tiny", encoder=fake_encoder)
    folder = root / "cache" / "embeddings" / "tiny"
    before = job.sha256_file(folder / "vectors.npy")
    (folder / "map3d.jsonl").unlink()
    emb.ensure_map3d(root, "tiny")
    assert len((folder / "map3d.jsonl").read_text().splitlines()) == 8
    assert job.sha256_file(folder / "vectors.npy") == before


def test_group_examples_are_typical_items_and_record_who_saw_them(tmp_path: Path) -> None:
    root, _ = harness.build_job(tmp_path)
    sealed = harness.sealed_ids(root)
    v = emb.build(root, model="org/tiny", encoder=fake_encoder, groups=2)["version"]
    first = emb.group_examples(root, v, 0, k=2, human_id="jl", channel="test")
    size = first["size"]
    assert len(first["examples"]) == min(2, size) and first["hidden_waiting"] == 0
    assert all(e["text"] for e in first["examples"])
    assert not {e["item_id"] for e in first["examples"]} & sealed
    closeness = [e["closeness"] for e in first["examples"]]
    assert closeness == sorted(closeness, reverse=True)
    rest = emb.group_examples(root, v, 0, k=10, offset=2, human_id="jl")
    assert not {e["item_id"] for e in rest["examples"]} & {e["item_id"] for e in first["examples"]}
    assert rest["more"] is False and len(first["examples"]) + len(rest["examples"]) == size
    log = [json.loads(l) for l in (root / emb.EXPOSURE_LOG).read_text().splitlines()]
    assert log[0]["human_id"] == "jl" and log[0]["item_ids"] == [e["item_id"] for e in first["examples"]]
    assert set(emb.seen_items(root)) == {e["item_id"] for e in first["examples"] + rest["examples"]}
    for bad in ({"k": 0}, {"k": 11}, {"offset": -1}):
        with pytest.raises(emb.EmbeddingRefused):
            emb.group_examples(root, v, 0, **bad)
    with pytest.raises(emb.EmbeddingRefused, match="groups 1 to 2"):
        emb.group_examples(root, v, 2)


def test_group_examples_hide_items_waiting_in_a_round(tmp_path: Path) -> None:
    root, _ = harness.build_job(tmp_path)
    v = emb.build(root, model="org/tiny", encoder=fake_encoder, groups=2)["version"]
    batch = root / "rounds" / "round_01" / "human_batch.jsonl"
    batch.parent.mkdir(parents=True)
    waiting = ["i00", "i01"]
    batch.write_text("".join(json.dumps({"item_id": i}) + "\n" for i in waiting))
    assert emb.waiting_items(root) == {"i00": "round_01", "i01": "round_01"}
    shown = []
    for g in (0, 1):
        hit = emb.group_examples(root, v, g, k=10, human_id="jl")
        shown += [e["item_id"] for e in hit["examples"]]
        assert hit["hidden_rounds"] == (["round_01"] if hit["hidden_waiting"] else [])
    assert not set(shown) & set(waiting) and len(shown) == 8 - len(waiting)


def test_item_text_refuses_waiting_items_and_is_recorded(tmp_path: Path) -> None:
    root, _ = harness.build_job(tmp_path)
    emb.build(root, model="org/tiny", encoder=fake_encoder)
    batch = root / "rounds" / "round_01" / "human_batch.jsonl"
    batch.parent.mkdir(parents=True)
    batch.write_text(json.dumps({"item_id": "i00"}) + "\n")
    with pytest.raises(emb.EmbeddingRefused, match="waits in round_01"):
        emb.item_text(root, "tiny", "i00", human_id="jl")
    hit = emb.item_text(root, "tiny", "i01", human_id="jl", channel="test")
    assert hit["item_id"] == "i01" and hit["text"]
    assert set(emb.seen_items(root)) == {"i01"}
    with pytest.raises(emb.EmbeddingRefused):
        emb.item_text(root, "tiny", next(iter(harness.sealed_ids(root))), human_id="jl")


def test_every_build_records_who_started_it(tmp_path: Path) -> None:
    root, _ = harness.build_job(tmp_path)
    hit = emb.build(root, model="sentence-transformers/all-MiniLM-L6-v2", encoder=fake_encoder,
                    channel=emb.BUTTON_CHANNEL, started_by="jl")
    assert hit["manifest"]["started_by"] == {"person": "jl", "via": emb.BUTTON_CHANNEL}
    ticket = yaml.safe_load((root / "runs" / f"{hit['run']}.yaml").read_text())
    assert ticket["commission"]["started_by"] == "jl"
    row = next(r for r in emb.build_status(root) if r["id"] == "sentence-transformers/all-MiniLM-L6-v2")
    assert row["started"] == {"person": "jl", "via": "run button", "note": None}
    assert next(r for r in emb.build_status(root) if r["id"] == "BAAI/bge-m3")["started"] is None


def test_who_started_reads_older_free_text_tickets() -> None:
    assert emb.who_started({"requested_by": "cli"}) == {"person": None, "via": "terminal", "note": None}
    assert emb.who_started({"requested_by": "cli, requested by JL in chat"}) == \
        {"person": "JL", "via": "terminal", "note": "asked in chat"}
    assert emb.who_started({"requested_by": "board labeling screen", "started_by": "JL"})["via"] == "run button"


def test_the_command_line_will_not_build_without_a_person(tmp_path: Path) -> None:
    root, _ = harness.build_job(tmp_path)
    with pytest.raises(SystemExit):
        emb.main(["build", "--job-root", str(root), "--model", "org/tiny"])
    assert not (root / "cache" / "embeddings" / "tiny").exists()
    assert not list((root / "runs").glob("rl*_embedding-build_*.yaml"))
