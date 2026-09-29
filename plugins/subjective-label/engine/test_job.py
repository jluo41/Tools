from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import yaml


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("subjective_label_job", HERE / "job.py")
job = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(job)


def write(path: Path, data: str | bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))


def source_job(root: Path) -> Path:
    src = root / "source"
    items = b'{"item_id":"dev-1","text":"A public development item"}\n'
    write(
        src / "config.yaml",
        yaml.safe_dump(
            {
                "project": {"id": "source"},
                "construct": {"name": "old-target"},
                "authority": {"human_id": "PROXY", "mode": "simulation"},
                "labels": {"values": ["high", "low", "none"]},
                "regions": {"values": ["H", "L", "N", "HL", "LN", "HN", "HLN"]},
                "uncertainty": {"levels": ["low", "high"], "unresolved_is_label": False},
            },
            sort_keys=False,
        ),
    )
    write(src / "corpus" / "items.jsonl", items)
    write(
        src / "corpus" / "manifest.json",
        json.dumps({"n_items": 1, "n_eligible": 1, "n_sealed": 1}) + "\n",
    )
    protected = (json.dumps({"item_id": "sealed-1", "text_hash": job.sha256_bytes(b"reserved sealed item")}, sort_keys=True) + "\n").encode("utf-8")
    write(src / "test" / "sealed" / "manifest.protected.jsonl", protected)
    write(
        src / "test" / "sealed" / "status.json",
        json.dumps(
            {
                "status": "reserved",
                "custodian": "SOURCE-CUSTODIAN",
                "invalidation_state": "valid",
                "n_items": 1,
                "frame": {"rule": "split == test"},
                "access_policy": ["no development read, embed, index, or prelabel"],
                "simulation_only": True,
            }
        ) + "\n",
    )
    write(src / "policy" / "versions" / "G_00" / "guideline.md", "# Seed\n")
    write(src / "policy" / "versions" / "G_00" / "boundaries.yaml", "status: open\n")
    write(src / "policy" / "versions" / "G_00" / "procedure.yaml", "status: seed\n")
    write(src / "policy" / "versions" / "G_00" / "uncertainty.yaml", "required: true\n")
    write(src / "policy" / "versions" / "G_00" / "cheatsheet.md", "# Seed\n")
    write(src / "policy" / "versions" / "G_00" / "manifest.yaml", "policy_id: G_00\n")
    return src


def page_file(root: Path, name: str = "S-Label-1") -> Path:
    page = root / "page" / name / f"{name}.md"
    write(page, f"# {name}\n")
    return page


def gates_module():
    path = HERE / "gates.py"
    spec = importlib.util.spec_from_file_location("subjective_label_gates", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_create_contract_is_p0_idempotent_and_keeps_seal_opaque(tmp_path: Path) -> None:
    src = source_job(tmp_path)
    page = page_file(tmp_path)
    dest = page.parent / "labeling"
    first = job.create_contract(
        source_job=src,
        job_root=dest,
        page_file=page,
        job_id="real-job",
        target="authority_appeal",
        human_id="JL",
        created_at="2026-09-01",
    )
    assert first["phase"] == "P0"
    assert first["protected_manifest_parsed"] is True
    assert first["protected_manifest_exposed"] is False
    assert (dest / "test/sealed/manifest.protected.jsonl").read_bytes() == (
        src / "test/sealed/manifest.protected.jsonl"
    ).read_bytes()
    assert (dest / "gold/cumulative.jsonl").read_bytes() == b""
    assert not any((dest / "rounds").iterdir())
    run = "rl01_corpus-contract_job-v1"
    assert (dest.parent / "runs" / f"{run}.yaml").is_file()
    assert (dest.parent / "results" / run / "runtime.yaml").is_file()
    assert (dest.parent / "results" / run / "result.yaml").is_file()
    runtime = yaml.safe_load((dest.parent / "results" / run / "runtime.yaml").read_text())
    assert runtime["run"] == run
    assert runtime["status"] == "complete"
    assert runtime["operation"] == "corpus-contract"
    assert runtime["ticket"] == f"runs/{run}.yaml"  # receipt paths are relative to the Page
    assert runtime["inputs"] == [{"path": "labeling/corpus/items.jsonl"}]
    assert runtime["started_at"] == "2026-09-01T00:00:00-04:00"
    assert runtime["finished_at"] == runtime["started_at"]

    cfg = yaml.safe_load((dest / "config.yaml").read_text())
    assert cfg["authority"] == {
        "human_id": "JL",
        "mode": "single_human_semantic_authority",
        "creates_human_gold": True,
        "meaning_confirmed": False,
        "meaning_receipt": None,
    }
    written = b"".join(path.read_bytes() for path in dest.parent.rglob("*") if path.is_file()
                       and path.name != "manifest.protected.jsonl" and path.name != "items.jsonl")
    assert b"checksum" not in written and b"sha256" not in written  # no record pins a hash
    assert yaml.safe_load((dest / "policy/versions/G_00/manifest.yaml").read_text())["components"] == list(
        job.POLICY_COMPONENTS)
    state = job.status(dest)
    assert state["phase"] == "P0"
    assert state["p0_contract_integrity_valid"] is True
    assert state["meaning_receipt_valid"] is False
    assert state["g0_passed"] is False
    assert state["hold"] is False
    assert state["first_blocked_frontier"] == "G0 · human meaning confirmation"
    assert state["sealed_custodian"] == "JL"
    assert state["source_custodian_provenance"] == "SOURCE-CUSTODIAN"

    second = job.create_contract(
        source_job=src,
        job_root=dest,
        page_file=page,
        job_id="real-job",
        target="authority_appeal",
        human_id="JL",
        created_at="2026-09-01",
    )
    assert second["created_count"] == 0


def test_create_contract_removes_inline_legacy_sealed_rows_before_page_copy(
    tmp_path: Path,
) -> None:
    src = source_job(tmp_path)
    rows = [
        {"item_id": "dev-1", "text": "eligible source text", "population_status": "eligible",
         "source": "kept"},
        {"item_id": "sealed-2", "text": "SEALED_PRIVATE_TEXT", "population_status": "sealed",
         "source": "must not enter Page"},
    ]
    source_items = "".join(json.dumps(row) + "\n" for row in rows).encode("utf-8")
    write(src / "corpus" / "items.jsonl", source_items)
    protected = (json.dumps({
        "item_id": "sealed-2",
        "text_hash": job.sha256_bytes(b"SEALED_PRIVATE_TEXT"),
    }, sort_keys=True) + "\n").encode("utf-8")
    write(src / "test" / "sealed" / "manifest.protected.jsonl", protected)
    source_manifest = json.loads((src / "corpus" / "manifest.json").read_text())
    source_manifest.update({
        "items_checksum": "sha256:legacy-source-value",  # a legacy field the import drops
        "n_items": 2,
        "n_eligible": 1,
        "n_sealed": 1,
        "id_field": "item_id",
        "text_field": "text",
    })
    write(src / "corpus" / "manifest.json", job.json_bytes(source_manifest))
    sealed_status = job.load_mapping(src / "test" / "sealed" / "status.json")
    sealed_status.update({
        "n_items": 1,
        "protected_manifest_checksum": "sha256:legacy-source-value",
    })
    write(src / "test" / "sealed" / "status.json", job.json_bytes(sealed_status))

    page = page_file(tmp_path)
    dest = page.parent / "labeling"
    result = job.create_contract(
        source_job=src,
        job_root=dest,
        page_file=page,
        job_id="legacy-import",
        target="authority_appeal",
        human_id="JL",
        created_at="2026-09-01",
    )

    page_items = (dest / "corpus" / "items.jsonl").read_bytes()
    page_rows = [json.loads(line) for line in page_items.splitlines()]
    assert len(page_rows) == 1
    assert page_rows[0]["item_id"] == "dev-1"
    assert page_rows[0]["population_status"] == "eligible"
    assert page_rows[0]["source"] == "kept"
    assert b"SEALED_PRIVATE_TEXT" not in page_items
    assert all(b"SEALED_PRIVATE_TEXT" not in path.read_bytes()
               for path in dest.rglob("*") if path.is_file())

    manifest = json.loads((dest / "corpus" / "manifest.json").read_text())
    assert manifest["n_items"] == manifest["n_eligible"] == 1
    assert manifest["n_sealed"] == 1
    assert "items_checksum" not in manifest
    assert "protected_manifest_checksum" not in job.load_mapping(dest / "test" / "sealed" / "status.json")
    protected_rows = [json.loads(line) for line in
                      (dest / "test" / "sealed" / "manifest.protected.jsonl").read_text().splitlines()]
    assert protected_rows == [{
        "item_id": "sealed-2",
        "text_hash": job.sha256_bytes(b"SEALED_PRIVATE_TEXT"),
    }]
    assert result["items"] == 1
    assert result["sealed_items"] == 1
    assert job.status(dest)["p0_contract_integrity_valid"] is True


def test_create_contract_refuses_opaque_seal_without_resolvable_legacy_rows(
    tmp_path: Path,
) -> None:
    src = source_job(tmp_path)
    opaque = b"opaque encrypted custody\n"
    write(src / "test" / "sealed" / "manifest.protected.jsonl", opaque)
    page = page_file(tmp_path)
    dest = page.parent / "labeling"
    try:
        job.create_contract(
            source_job=src,
            job_root=dest,
            page_file=page,
            job_id="opaque-import",
            target="authority_appeal",
            human_id="JL",
            created_at="2026-09-01",
        )
    except RuntimeError as error:
        assert "opaque source protected manifest" in str(error)
    else:
        raise AssertionError("unresolved opaque sealed custody must not be imported")
    assert not (dest / "corpus" / "items.jsonl").exists()


def test_import_manifest_counts_external_sealed_and_excluded_rows(tmp_path: Path) -> None:
    src = source_job(tmp_path)
    rows = [
        {"item_id": "dev-1", "text": "eligible", "population_status": "eligible"},
        {"item_id": "excluded-1", "text": "excluded", "population_status": "excluded"},
    ]
    source_items = "".join(json.dumps(row) + "\n" for row in rows).encode("utf-8")
    write(src / "corpus" / "items.jsonl", source_items)
    sealed_texts = {"sealed-1": "reserved one", "sealed-2": "reserved two"}
    protected = "".join(
        json.dumps({"item_id": item_id, "text_hash": job.sha256_bytes(text.encode())}, sort_keys=True) + "\n"
        for item_id, text in sorted(sealed_texts.items())
    ).encode("utf-8")
    write(src / "test" / "sealed" / "manifest.protected.jsonl", protected)
    source_manifest = json.loads((src / "corpus" / "manifest.json").read_text())
    source_manifest.update({
        "n_items": 1,
        "n_eligible": 1,
        "n_sealed": 2,
        "n_source_items": 4,
        "id_field": "item_id",
        "text_field": "text",
    })
    write(src / "corpus" / "manifest.json", job.json_bytes(source_manifest))
    sealed_status = job.load_mapping(src / "test" / "sealed" / "status.json")
    sealed_status.update({"n_items": 2})
    write(src / "test" / "sealed" / "status.json", job.json_bytes(sealed_status))

    page = page_file(tmp_path)
    dest = page.parent / "labeling"
    job.create_contract(
        source_job=src,
        job_root=dest,
        page_file=page,
        job_id="external-seal-counts",
        target="authority_appeal",
        human_id="JL",
        created_at="2026-09-01",
    )

    manifest = json.loads((dest / "corpus" / "manifest.json").read_text())
    assert manifest["n_items"] == manifest["n_eligible"] == 1
    assert manifest["n_sealed"] == 2
    assert manifest["n_source_items"] == 4
    assert job.status(dest)["p0_contract_integrity_valid"] is True


def test_opaque_legacy_seal_rows_are_rebound_to_id_hash_custody(tmp_path: Path) -> None:
    src = source_job(tmp_path)
    rows = [
        {"item_id": "dev-1", "text": "eligible", "population_status": "eligible"},
        {"item_id": "sealed-2", "text": "SEALED_PRIVATE_TEXT", "population_status": "sealed"},
    ]
    source_items = "".join(json.dumps(row) + "\n" for row in rows).encode("utf-8")
    write(src / "corpus" / "items.jsonl", source_items)
    source_manifest = json.loads((src / "corpus" / "manifest.json").read_text())
    source_manifest.update({
        "n_items": 2,
        "n_eligible": 1,
        "n_sealed": 1,
        "id_field": "item_id",
        "text_field": "text",
    })
    write(src / "corpus" / "manifest.json", job.json_bytes(source_manifest))
    opaque = b"encrypted legacy protected manifest\n"
    write(src / "test" / "sealed" / "manifest.enc-or-protected", opaque)
    (src / "test" / "sealed" / "manifest.protected.jsonl").unlink()
    sealed_status = job.load_mapping(src / "test" / "sealed" / "status.json")
    sealed_status.update({"n_items": 1})
    write(src / "test" / "sealed" / "status.json", job.json_bytes(sealed_status))

    page = page_file(tmp_path)
    dest = page.parent / "labeling"
    job.create_contract(
        source_job=src,
        job_root=dest,
        page_file=page,
        job_id="opaque-legacy-import",
        target="authority_appeal",
        human_id="JL",
        created_at="2026-09-01",
    )

    page_items = (dest / "corpus" / "items.jsonl").read_bytes()
    assert b"SEALED_PRIVATE_TEXT" not in page_items
    protected_rows = [json.loads(line) for line in
                      (dest / "test" / "sealed" / "manifest.protected.jsonl").read_text().splitlines()]
    assert protected_rows == [{
        "item_id": "sealed-2",
        "text_hash": job.sha256_bytes(b"SEALED_PRIVATE_TEXT"),
    }]
    assert job.status(dest)["p0_contract_integrity_valid"] is True


def test_shipped_mini_fixture_is_a_valid_p0_source_fence() -> None:
    fixture = HERE.parent / "fixtures" / "job-mini"
    status = job.load_mapping(fixture / "test" / "sealed" / "status.json")
    protected = job.find_protected_manifest(fixture / "test" / "sealed")

    assert protected.is_file()
    job.validate_source_fence(status)


def test_create_contract_refuses_changed_destination(tmp_path: Path) -> None:
    src = source_job(tmp_path)
    page = page_file(tmp_path)
    dest = page.parent / "labeling"
    write(dest / "config.yaml", "changed: true\n")
    try:
        job.create_contract(
            source_job=src,
            job_root=dest,
            page_file=page,
            job_id="real-job",
            target="authority_appeal",
            human_id="JL",
            created_at="2026-09-01",
        )
    except RuntimeError as error:
        assert "refusing to overwrite" in str(error)
    else:
        raise AssertionError("changed destination was overwritten")


def test_status_checks_content_and_requires_meaning_receipt(tmp_path: Path) -> None:
    src = source_job(tmp_path)
    page = page_file(tmp_path)
    dest = page.parent / "labeling"
    job.create_contract(
        source_job=src,
        job_root=dest,
        page_file=page,
        job_id="real-job",
        target="authority_appeal",
        human_id="JL",
        created_at="2026-09-01",
    )

    cfg = yaml.safe_load((dest / "config.yaml").read_text())
    cfg["authority"]["meaning_confirmed"] = True
    write(dest / "config.yaml", yaml.safe_dump(cfg, sort_keys=False))
    flipped = job.status(dest)  # a flag without a receipt confirms nothing
    assert flipped["phase"] == "P0"
    assert flipped["meaning_receipt_valid"] is False
    assert flipped["g0_passed"] is False
    assert flipped["first_blocked_frontier"] == "G0 · human meaning confirmation"

    items = dest / "corpus" / "items.jsonl"
    original = items.read_bytes()
    write(items, original + b'{"item_id":"tampered","population_status":"eligible"}\n')
    tampered = job.status(dest)
    assert tampered["phase"] == "P0"
    assert tampered["p0_contract_integrity_valid"] is False
    assert ("corpus/items.jsonl has 2 rows but corpus/manifest.json says n_items 1"
            in tampered["integrity_errors"])

    write(items, original + b'{"tampered":true}\n')
    assert "corpus/items.jsonl line 2 has no item_id" in job.status(dest)["integrity_errors"]


def test_meaning_confirmation_requires_explicit_caller_attestation(tmp_path: Path) -> None:
    src = source_job(tmp_path)
    page = page_file(tmp_path)
    dest = page.parent / "labeling"
    job.create_contract(
        source_job=src,
        job_root=dest,
        page_file=page,
        job_id="real-job",
        target="authority_appeal",
        human_id="JL",
        created_at="2026-09-01",
    )
    try:
        job.confirm_meaning(
            job_root=dest, page_file=page, human_id="JL",
            confirmed_at="2026-09-01T12:00:00Z", accept_current_schema=True,
        )
    except RuntimeError as error:
        assert "explicit human caller attestation" in str(error)
    else:
        raise AssertionError("confirmation must require an explicit caller attestation")


def test_old_semantic_receipt_can_be_upgraded_with_explicit_attestation(tmp_path: Path) -> None:
    src = source_job(tmp_path)
    page = page_file(tmp_path)
    dest = page.parent / "labeling"
    job.create_contract(
        source_job=src,
        job_root=dest,
        page_file=page,
        job_id="real-job",
        target="authority_appeal",
        human_id="JL",
        created_at="2026-09-01",
    )
    job.confirm_meaning(
        job_root=dest, page_file=page, human_id="JL",
        confirmed_at="2026-09-01T12:00:00Z", accept_current_schema=True,
        attest_as_human=True,
    )

    config_path = dest / "config.yaml"
    config = yaml.safe_load(config_path.read_text())
    config["authority"]["meaning_receipt"].pop("identity_assurance")
    old_config = job.yaml_bytes(config)
    write(config_path, old_config)
    g0_path = dest / "gates" / "g0" / "receipt.json"
    g0_before = g0_path.read_bytes()

    old_state = job.status(dest)
    assert old_state["p0_contract_integrity_valid"] is True
    assert old_state["g0_receipt_valid"] is True
    assert old_state["meaning_receipt_valid"] is False

    upgraded = job.confirm_meaning(
        job_root=dest, page_file=page, human_id="JL",
        confirmed_at="2026-09-02T12:00:00Z", accept_current_schema=True,
        attest_as_human=True,
    )
    assert upgraded["phase"] == "P1"
    archived = list((dest / "gates" / "g0" / "history").glob("*.json"))
    assert len(archived) == 1 and archived[0].read_bytes() == g0_before
    assert archived[0].stem[:8].isdigit()  # named by the time it was retired, never by a hash
    assert job.status(dest)["g0_passed"] is True


def test_create_contract_requires_direct_matching_labeling_lane(tmp_path: Path) -> None:
    src = source_job(tmp_path)
    page = page_file(tmp_path)
    for dest in (
        tmp_path / "page" / "S-Label-1" / "not-labeling",
        tmp_path / "detached" / "S-Label-1" / "labeling",
    ):
        try:
            job.create_contract(
                source_job=src,
                job_root=dest,
                page_file=page,
                job_id="real-job",
                target="authority_appeal",
                human_id="JL",
                created_at="2026-09-01",
            )
        except RuntimeError as error:
            assert "canonical destination" in str(error)
        else:
            raise AssertionError("noncanonical destination was accepted")


def test_status_requires_each_p0_file_to_parse_and_the_protected_manifest(tmp_path: Path) -> None:
    src = source_job(tmp_path)
    page = page_file(tmp_path)
    dest = page.parent / "labeling"
    job.create_contract(
        source_job=src,
        job_root=dest,
        page_file=page,
        job_id="real-job",
        target="authority_appeal",
        human_id="JL",
        created_at="2026-09-01",
    )
    register = dest / "register.md"
    write(register, register.read_bytes() + b"a note\n")
    assert job.status(dest)["p0_contract_integrity_valid"] is True  # an edit is not a hash break

    protected = dest / "test" / "sealed" / "manifest.protected.jsonl"
    kept = protected.read_bytes()
    protected.unlink()
    state = job.status(dest)
    assert state["p0_contract_integrity_valid"] is False
    assert any("exactly one opaque protected manifest" in e for e in state["integrity_errors"])
    write(protected, kept)

    manifest = dest / "corpus" / "manifest.json"
    kept = manifest.read_bytes()
    write(manifest, b"{not json")
    state = job.status(dest)
    assert state["p0_contract_integrity_valid"] is False
    assert "unreadable manifest.json: JSONDecodeError" in state["integrity_errors"]
    write(manifest, kept)

    (dest / "policy" / "versions" / "G_00" / "gallery.md").unlink()
    assert "G_00 component missing: gallery.md" in job.status(dest)["integrity_errors"]


def test_an_unrecorded_edit_to_the_meanings_after_confirmation_fails_g0(tmp_path: Path) -> None:
    src = source_job(tmp_path)
    page = page_file(tmp_path)
    dest = page.parent / "labeling"
    job.create_contract(source_job=src, job_root=dest, page_file=page, job_id="real-job",
                        target="authority_appeal", human_id="JL", created_at="2026-09-01")
    job.confirm_meaning(job_root=dest, page_file=page, human_id="JL", confirmed_at="2026-09-01T12:00:00Z",
                        accept_current_schema=True, attest_as_human=True)
    assert job.status(dest)["g0_passed"] is True
    receipt = job.load_mapping(dest / "config.yaml")["authority"]["meaning_receipt"]
    assert receipt["bindings"]["construct"]["name"] == "authority_appeal"  # a content snapshot, no hash
    assert receipt["bindings"]["policy_version"] == "G_00"

    config = job.load_mapping(dest / "config.yaml")
    config["labels"]["meanings"] = {"high": "edited by hand"}
    write(dest / "config.yaml", job.yaml_bytes(config))
    state = job.status(dest)
    assert state["g0_passed"] is False
    assert state["meaning_receipt_valid"] is False
    assert state["p0_contract_integrity_valid"] is True
    assert state["first_blocked_frontier"] == "G0 · human meaning confirmation"

    again = job.confirm_meaning(job_root=dest, page_file=page, human_id="JL",
                                confirmed_at="2026-09-02T12:00:00Z", accept_current_schema=True,
                                attest_as_human=True)
    assert "gates/g0/receipt.json" in again["updated_files"]
    assert len(list((dest / "gates" / "g0" / "history").glob("*.json"))) == 1
    assert job.status(dest)["g0_passed"] is True


def test_confirm_binds_current_semantics_and_is_idempotent_despite_stale_phase(
    tmp_path: Path, monkeypatch
) -> None:
    src = source_job(tmp_path)
    page = page_file(tmp_path)
    dest = page.parent / "labeling"
    job.create_contract(
        source_job=src,
        job_root=dest,
        page_file=page,
        job_id="real-job",
        target="authority_appeal",
        human_id="JL",
        created_at="2026-09-01",
    )
    real_status = job.status

    def stale_compatibility_phase(path: Path) -> dict:
        state = real_status(path)
        state["phase"] = "P0"
        return state

    monkeypatch.setattr(job, "status", stale_compatibility_phase)

    first = job.confirm_meaning(
        job_root=dest,
        page_file=page,
        human_id="JL",
        confirmed_at="2026-09-01T12:00:00Z",
        accept_current_schema=True,
        attest_as_human=True,
    )
    assert first["phase"] == "P1"
    assert first["updated_count"] == 2
    state = real_status(dest)
    assert state["phase"] == "P1"
    assert state["p0_contract_integrity_valid"] is True
    assert state["meaning_receipt_valid"] is True
    assert state["g0_passed"] is True

    second = job.confirm_meaning(
        job_root=dest,
        page_file=page,
        human_id="JL",
        confirmed_at="2026-09-01T12:00:00Z",
        accept_current_schema=True,
        attest_as_human=True,
    )
    assert second["updated_count"] == 0


def test_g0_gate_uses_semantic_predicates_and_distinguishes_pending_from_holds(
    tmp_path: Path, monkeypatch
) -> None:
    src = source_job(tmp_path)
    page = page_file(tmp_path)
    dest = page.parent / "labeling"
    job.create_contract(
        source_job=src,
        job_root=dest,
        page_file=page,
        job_id="real-job",
        target="authority_appeal",
        human_id="JL",
        created_at="2026-09-01",
    )

    gates = gates_module()
    monkeypatch.setitem(
        sys.modules,
        "job",
        SimpleNamespace(status=job.status),
    )

    pending = job.status(dest)
    assert pending["p0_contract_integrity_valid"] is True
    assert pending["hold"] is False
    assert pending["meaning_receipt_valid"] is False
    assert pending["g0_receipt_valid"] is False
    assert pending["g0_passed"] is False
    try:
        gates.require_gate(dest, "G0")
    except gates.GateHold as error:
        assert "G0 pending" in str(error)
        assert "HOLD" not in str(error)
    else:
        raise AssertionError("unconfirmed G0 must block with a pending reason")

    protected = dest / "test" / "sealed" / "manifest.protected.jsonl"
    original_protected = protected.read_bytes()
    protected.unlink()
    integrity_hold = job.status(dest)
    assert integrity_hold["p0_contract_integrity_valid"] is False
    try:
        gates.require_gate(dest, "G0")
    except gates.GateHold as error:
        assert "HOLD · G0 blocked by P0 contract integrity" in str(error)
    else:
        raise AssertionError("P0 integrity failure must hold dependent work")
    write(protected, original_protected)

    job.confirm_meaning(
        job_root=dest,
        page_file=page,
        human_id="JL",
        confirmed_at="2026-09-01T12:00:00Z",
        accept_current_schema=True,
        attest_as_human=True,
    )
    assert job.status(dest)["g0_passed"] is True
    gates.require_gate(dest, "G0")

    (dest / "gates" / "g0" / "receipt.json").unlink()
    g0_integrity_hold = job.status(dest)
    assert g0_integrity_hold["p0_contract_integrity_valid"] is True
    assert g0_integrity_hold["g0_receipt_valid"] is False
    assert g0_integrity_hold["next_action"] == "repair the G0 receipt before any Round 1 proposal"
    try:
        gates.require_gate(dest, "G0")
    except gates.GateHold as error:
        assert "HOLD · G0 receipt integrity" in str(error)
    else:
        raise AssertionError("missing post-confirmation G0 receipt must hold work")


def test_g0_gate_ignores_stale_phase_projection(monkeypatch, tmp_path: Path) -> None:
    gates = gates_module()
    ready = {
        "phase": "P0",
        "p0_contract_integrity_valid": True,
        "hold": False,
        "meaning_receipt_valid": True,
        "g0_receipt_valid": True,
    }
    monkeypatch.setitem(
        sys.modules,
        "job",
        SimpleNamespace(status=lambda _path: ready),
    )
    gates.require_gate(tmp_path, "G0")

    ready["phase"] = "P1"
    ready["g0_receipt_valid"] = False
    try:
        gates.require_gate(tmp_path, "G0")
    except gates.GateHold as error:
        assert "G0 receipt integrity" in str(error)
    else:
        raise AssertionError("a P1 compatibility tag must not bypass a missing G0 receipt")

    ready.update(
        phase="P1",
        g0_receipt_valid=True,
        hold=True,
        hold_reason="proxy authority is not allowed",
    )
    try:
        gates.require_gate(tmp_path, "G0")
    except gates.GateHold as error:
        assert "human-authority policy" in str(error)
    else:
        raise AssertionError("a compatibility tag must not bypass an authority HOLD")


def test_status_requires_valid_g0_receipt_after_confirmation(tmp_path: Path) -> None:
    src = source_job(tmp_path)
    page = page_file(tmp_path)
    dest = page.parent / "labeling"
    job.create_contract(
        source_job=src,
        job_root=dest,
        page_file=page,
        job_id="real-job",
        target="authority_appeal",
        human_id="JL",
        created_at="2026-09-01",
    )
    job.confirm_meaning(
        job_root=dest,
        page_file=page,
        human_id="JL",
        confirmed_at="2026-09-01T12:00:00Z",
        accept_current_schema=True,
        attest_as_human=True,
    )

    g0_path = dest / "gates" / "g0" / "receipt.json"
    good = g0_path.read_bytes()
    g0_path.unlink()
    missing = job.status(dest)
    assert missing["phase"] == "P0"
    assert missing["g0_receipt_valid"] is False
    assert "G0 receipt missing after semantic confirmation" in missing["integrity_errors"]

    write(g0_path, good)
    forged = json.loads(g0_path.read_text())
    forged["status"] = "failed"
    write(g0_path, json.dumps(forged, indent=2, sort_keys=True) + "\n")
    assert "G0 receipt is invalid or semantically unbound" in job.status(dest)["integrity_errors"]
    forged["status"] = "passed"
    forged["bindings"]["labels"] = {"values": ["other"]}  # a snapshot that is not the confirmed one
    write(g0_path, json.dumps(forged, indent=2, sort_keys=True) + "\n")
    invalid = job.status(dest)
    assert invalid["phase"] == "P0"
    assert invalid["g0_receipt_valid"] is False
    assert "G0 receipt is invalid or semantically unbound" in invalid["integrity_errors"]
