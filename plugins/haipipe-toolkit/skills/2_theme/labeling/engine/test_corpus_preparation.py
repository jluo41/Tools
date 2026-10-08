from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest
import yaml

HERE = Path(__file__).resolve().parent


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


prep = _load("subjective_label_preparation_test", "corpus_preparation.py")
job = _load("subjective_label_job_preparation_test", "job.py")


def _fixture(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    raw = tmp_path / "transcripts.jsonl"
    rows = [
        {"conversation_id": f"c{i}", "split_group_id": f"group-{i}", "turns": [
            {"role": "user", "content": f"question {i}a"},
            {"role": "assistant", "content": f"PRIVATE_REPLY_{i}a"},
            {"role": "user", "content": f"question {i}b"},
            {"role": "assistant", "content": f"PRIVATE_REPLY_{i}b"},
        ]} for i in range(1, 4)
    ]
    raw.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    config_path = tmp_path / "seed.yaml"
    config_path.write_text(yaml.safe_dump({
        "construct": {"name": "example", "question": "Does the reply show the target?"},
        "labels": {"values": ["high", "low", "none"],
                   "meanings": {"high": "high", "low": "low", "none": "absent"}},
        "regions": {"values": list(job.REGIONS)},
        "uncertainty": {"levels": ["low", "high"]},
        "corpus": {},
    }, sort_keys=False), encoding="utf-8")
    owner = tmp_path / "source" / "corpus-preparation"
    page = tmp_path / "board" / "pages" / "Label-1" / "Label-1.md"
    page.parent.mkdir(parents=True)
    page.write_text("# Label-1\n", encoding="utf-8")
    return raw, config_path, owner, page


def _prepare(tmp_path: Path, selector: str = "every-assistant-reply") -> dict:
    raw, config, owner, page = _fixture(tmp_path)
    snapshot = prep.normalize(owner, raw, "transcripts")["snapshot_id"]
    recipe_id = prep.recipe(owner, snapshot, selector, None, "preparation-owner")["recipe_id"]
    itemset = prep.materialize(owner, snapshot, recipe_id)["item_set_id"]
    prep.check(owner, snapshot, itemset)
    reserved = prep.reserve(owner, snapshot, itemset, config, 1, 42, "custodian")
    return {"owner": owner, "page": page, "snapshot": snapshot,
            "recipe": recipe_id, "itemset": itemset, **reserved}


def test_flat_board_source_cannot_own_a_shared_labeling_lane(tmp_path: Path) -> None:
    flat = tmp_path / "board" / "SL" / "S-Label-2.md"
    flat.parent.mkdir(parents=True)
    flat.write_text("# S-Label-2\n", encoding="utf-8")
    owner = tmp_path / "source" / "corpus-preparation"
    with pytest.raises(RuntimeError, match="canonical <Page>/<Page>.md folder"):
        prep.attach(owner, "transcripts", flat)
    with pytest.raises(RuntimeError, match="canonical <Page>/<Page>.md folder"):
        job.create_contract(source_job=tmp_path / "source-package",
                            job_root=flat.parent / "labeling", page_file=flat,
                            job_id="example", target="example", human_id="human",
                            created_at="2026-09-29")
    assert not (flat.parent / "labeling").exists()
    assert not owner.exists()


def test_multiturn_units_group_reservation_and_contract_binding(tmp_path: Path) -> None:
    state = _prepare(tmp_path)
    owner, page = state["owner"], state["page"]
    item_path = owner / "versions" / state["snapshot"] / "itemsets" / state["itemset"] / "items.private.jsonl"
    items = [json.loads(line) for line in item_path.read_text().splitlines()]
    assert len(items) == 6
    assert [row["text"] for row in items[:2]] == ["PRIVATE_REPLY_1a", "PRIVATE_REPLY_1b"]
    assert items[0]["context_prev"] == "user: question 1a"
    assert items[1]["context_prev"] == "user: question 1a\nassistant: PRIVATE_REPLY_1a\nuser: question 1b"
    assert items[0]["split_group_id"] == items[1]["split_group_id"]

    package = Path(state["package"])
    eligible = [json.loads(line) for line in (package / "corpus/items.jsonl").read_text().splitlines()]
    sealed = [json.loads(line) for line in (package / "test/sealed/manifest.protected.jsonl").read_text().splitlines()]
    assert len(eligible) == 4 and len(sealed) == 2
    sealed_ids = {row["item_id"] for row in sealed}
    assert not sealed_ids & {row["item_id"] for row in eligible}
    assert {row["conversation_id"] for row in eligible}.isdisjoint(
        {item["conversation_id"] for item in items if item["item_id"] in sealed_ids})
    assert not any(item["text"] in (package / "corpus/items.jsonl").read_text()
                   for item in items if item["item_id"] in sealed_ids)
    assert all(name.startswith("run-corpus-") for name in
               (path.stem for path in (owner / "runs").glob("*.yaml")))
    assert len(list((owner / "runs").glob("*.yaml"))) == 5

    prep.link(owner, package, page)
    assert not (page.parent / "labeling/config.yaml").exists()
    result = job.create_contract(source_job=package, job_root=page.parent / "labeling",
                                 page_file=page, job_id="example", target="example",
                                 human_id="human", created_at="2026-09-29")
    assert result["phase"] == "P0"
    assert (page.parent / "runs/run-labeling-corpus-contract-0929-job-v1.yaml").is_file()
    copied = (page.parent / "labeling/corpus/items.jsonl").read_text()
    assert all(item["text"] not in copied for item in items if item["item_id"] in sealed_ids)
    assert job.status(page.parent / "labeling")["p0_contract_integrity_valid"] is True


def test_same_source_partition_is_reused_across_unit_recipes(tmp_path: Path) -> None:
    state = _prepare(tmp_path)
    owner, snapshot = state["owner"], state["snapshot"]
    recipe_id = prep.recipe(owner, snapshot, "final-assistant-reply", None, "preparation-owner")["recipe_id"]
    itemset = prep.materialize(owner, snapshot, recipe_id)["item_set_id"]
    prep.check(owner, snapshot, itemset)
    config = tmp_path / "seed.yaml"
    second = prep.reserve(owner, snapshot, itemset, config, 1, 42, "custodian")
    assert second["partition_id"] == state["partition_id"]
    assert prep.verify_package(Path(second["package"]))["n_sealed"] == 1


def test_exact_repetition_reuses_accepted_run(tmp_path: Path) -> None:
    raw, _, owner, _ = _fixture(tmp_path)
    first = prep.normalize(owner, raw, "transcripts")
    second = prep.normalize(owner, raw, "transcripts")
    assert first["run"] == second["run"]
    assert len(list((owner / "runs").glob("*.yaml"))) == 1


def test_recipe_change_mints_a_distinct_run_and_artifact(tmp_path: Path) -> None:
    raw, _, owner, _ = _fixture(tmp_path)
    snapshot = prep.normalize(owner, raw, "transcripts")["snapshot_id"]
    first = prep.recipe(owner, snapshot, "every-assistant-reply", None, "owner")
    second = prep.recipe(owner, snapshot, "every-assistant-reply", 1, "owner")
    assert first["recipe_id"] != second["recipe_id"]
    assert first["run"] != second["run"]
    assert (owner / "versions" / snapshot / "recipes" / f"{second['recipe_id']}.yaml").is_file()
    assert prep.recipe(owner, snapshot, "every-assistant-reply", 1, "owner")["run"] == second["run"]


def test_normalize_preserves_raw_lineage_and_rejects_bad_grouping(tmp_path: Path) -> None:
    raw, _, owner, _ = _fixture(tmp_path)
    rows = raw.read_text(encoding="utf-8").splitlines()
    invalid = {"conversation_id": "bad", "split_group_id": "", "turns": [
        {"role": "assistant", "content": "should reject"}]}
    raw.write_text("\n" + json.dumps(invalid) + "\n" + "\n".join(rows) + "\n", encoding="utf-8")
    snapshot = prep.normalize(owner, raw, "transcripts")["snapshot_id"]
    folder = owner / "versions" / snapshot
    rejects = [json.loads(line) for line in (folder / "rejects.private.jsonl").read_text().splitlines()]
    accepted = [json.loads(line) for line in (folder / "normalized.private.jsonl").read_text().splitlines()]
    assert rejects == [{"reason": "split_group_id must be a nonempty string", "source_line": 2}]
    assert accepted[0]["source_line"] == 3


def test_contract_refuses_changed_page_owner_reference(tmp_path: Path) -> None:
    state = _prepare(tmp_path)
    package, page = Path(state["package"]), state["page"]
    prep.link(state["owner"], package, page)
    owner_ref = page.parent / "labeling/preparation-owner.yaml"
    changed = yaml.safe_load(owner_ref.read_text(encoding="utf-8"))
    changed["source_id"] = "another-source"
    owner_ref.write_text(yaml.safe_dump(changed), encoding="utf-8")
    with pytest.raises(RuntimeError, match="Page preparation owner disagrees"):
        job.create_contract(source_job=package, job_root=page.parent / "labeling",
                            page_file=page, job_id="example", target="example",
                            human_id="human", created_at="2026-09-29")
    assert not (page.parent / "labeling/config.yaml").exists()


def test_early_preparation_receipt_remains_linkable(tmp_path: Path) -> None:
    state = _prepare(tmp_path)
    owner, package, page = state["owner"], Path(state["package"]), state["page"]
    receipt_path = package / "preparation-receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    keep = {"schema", "status", "owner", "snapshot_id", "recipe_id", "item_set_id",
            "partition_id", "qa_digest", "frame_digest", "eligible_digest", "protected_digest",
            "n_eligible", "n_sealed", "group_disjointness"}
    legacy = {key: value for key, value in receipt.items() if key in keep}
    legacy["schema"] = "subjective-label/preparation-receipt-v1"
    receipt_path.write_text(json.dumps(legacy), encoding="utf-8")
    (owner / "source.yaml").unlink()
    assert prep.verify_package(package)["schema"].endswith("v1")
    prep.link(owner, package, page)
    assert (owner / "source.yaml").is_file()
    assert (page.parent / "labeling/preparation-owner.yaml").is_file()


def test_attached_page_cannot_skip_preparation_with_legacy_source(tmp_path: Path) -> None:
    _, _, owner, page = _fixture(tmp_path)
    prep.attach(owner, "transcripts", page)
    with pytest.raises(RuntimeError, match="no accepted preparation receipt"):
        job.create_contract(source_job=tmp_path / "some-legacy-source",
                            job_root=page.parent / "labeling", page_file=page,
                            job_id="example", target="example", human_id="human",
                            created_at="2026-09-29")
    assert not (page.parent / "labeling/config.yaml").exists()


@pytest.mark.parametrize("relative", [
    "config.yaml", "corpus/manifest.json", "test/sealed/status.json",
])
def test_contract_rejects_changed_public_package_artifact(tmp_path: Path, relative: str) -> None:
    state = _prepare(tmp_path)
    package = Path(state["package"])
    artifact = package / relative
    artifact.write_bytes(artifact.read_bytes() + b"\n")
    with pytest.raises(RuntimeError, match="preparation binding mismatch"):
        job.create_contract(source_job=package, job_root=state["page"].parent / "labeling",
                            page_file=state["page"], job_id="example", target="example",
                            human_id="human", created_at="2026-09-29")
    assert not (state["page"].parent / "labeling/config.yaml").exists()


def test_contract_refuses_tampered_preparation_before_writing_page(tmp_path: Path) -> None:
    state = _prepare(tmp_path)
    package = Path(state["package"])
    items = package / "corpus/items.jsonl"
    items.write_bytes(items.read_bytes() + b' {"injected":true}\n')
    with pytest.raises(RuntimeError, match="preparation binding mismatch"):
        job.create_contract(source_job=package, job_root=state["page"].parent / "labeling",
                            page_file=state["page"], job_id="example", target="example",
                            human_id="human", created_at="2026-09-29")
    assert not (state["page"].parent / "labeling/config.yaml").exists()


def test_inside_a_space_records_keep_relative_paths_and_private_text_leaves_the_project(tmp_path: Path) -> None:
    """AGENTS.md rule 7: no absolute path in a record; corpus text never in a git-tracked folder."""
    space = tmp_path / "space"
    space.mkdir()
    (space / "env.sh").write_text("# the SPACE root\n", encoding="utf-8")
    state = _prepare(space)
    owner, page, package = state["owner"], state["page"], Path(state["package"])
    assert package.is_absolute()                          # the caller still gets a real path
    assert not list(owner.rglob("*.private.*"))            # no private text beside the records
    custody = space / "_WorkSpace" / "LabelingStore" / "_custody"
    kept = sorted(p.name for p in custody.rglob("*.private.*"))
    assert kept == ["items.private.jsonl", "lineage.private.jsonl",
                    "normalized.private.jsonl", "rejects.private.jsonl"]
    prep.link(owner, package, page)
    job.create_contract(source_job=package, job_root=page.parent / "labeling", page_file=page,
                        job_id="example", target="example", human_id="human", created_at="2026-09-29")
    records = [*owner.rglob("*.yaml"), *owner.rglob("*.json"), *package.rglob("*.json"),
               *(page.parent / "labeling").glob("preparation-*.yaml")]
    for record in records:
        assert str(tmp_path) not in record.read_text(encoding="utf-8"), record
    ref = yaml.safe_load((page.parent / "labeling" / "preparation-ref.yaml").read_text())
    assert ref["owner"] == "source/corpus-preparation"
    assert prep.resolve_stored(ref["package"], page) == package.resolve()
    assert job.status(page.parent / "labeling")["p0_contract_integrity_valid"] is True
