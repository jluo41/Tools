from __future__ import annotations

import importlib.util
import json
from pathlib import Path

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
    checksum = job.sha256_bytes(items)
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
        json.dumps({"n_items": 1, "items_checksum": checksum}) + "\n",
    )
    protected = b'{"opaque":"sealed-id"}\n'
    write(src / "test" / "sealed" / "manifest.protected.jsonl", protected)
    write(
        src / "test" / "sealed" / "status.json",
        json.dumps(
            {
                "status": "reserved",
                "custodian": "SOURCE-CUSTODIAN",
                "invalidation_state": "valid",
                "frame": {"rule": "split == test"},
                "access_policy": ["no development read, embed, index, or prelabel"],
                "protected_manifest_checksum": "sha256:" + job.sha256_bytes(protected),
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
    assert first["protected_manifest_parsed"] is False
    assert first["protected_manifest_exposed"] is False
    assert (dest / "test/sealed/manifest.protected.jsonl").read_bytes() == (
        src / "test/sealed/manifest.protected.jsonl"
    ).read_bytes()
    assert (dest / "gold/cumulative.jsonl").read_bytes() == b""
    assert not any((dest / "rounds").iterdir())

    cfg = yaml.safe_load((dest / "config.yaml").read_text())
    assert cfg["authority"] == {
        "human_id": "JL",
        "mode": "single_human_semantic_authority",
        "creates_human_gold": True,
        "meaning_confirmed": False,
        "meaning_receipt": None,
    }
    state = job.status(dest)
    assert state["phase"] == "P0"
    assert state["g0_integrity"] is True
    assert state["meaning_receipt_valid"] is False

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


def test_status_rehashes_g0_and_requires_meaning_receipt(tmp_path: Path) -> None:
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
    flipped = job.status(dest)
    assert flipped["phase"] == "P0"
    assert flipped["meaning_receipt_valid"] is False
    assert flipped["first_blocked_frontier"] == "G0 Contract integrity"
    assert "P0 authority checksum mismatch: config.yaml" in flipped["integrity_errors"]

    items = dest / "corpus" / "items.jsonl"
    write(items, items.read_bytes() + b'{"item_id":"tampered"}\n')
    tampered = job.status(dest)
    assert tampered["phase"] == "P0"
    assert tampered["g0_integrity"] is False
    assert "corpus items checksum mismatch" in tampered["integrity_errors"]


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


def test_status_rehashes_each_p0_authority_artifact(tmp_path: Path) -> None:
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
    write(register, register.read_bytes() + b"tampered\n")
    state = job.status(dest)
    assert state["g0_integrity"] is False
    assert "P0 authority checksum mismatch: register.md" in state["integrity_errors"]


def test_confirm_binds_current_semantics_and_is_idempotent(tmp_path: Path) -> None:
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
    first = job.confirm_meaning(
        job_root=dest,
        page_file=page,
        human_id="JL",
        confirmed_at="2026-09-01T12:00:00Z",
        accept_current_schema=True,
    )
    assert first["phase"] == "P1"
    assert first["updated_count"] == 2
    state = job.status(dest)
    assert state["phase"] == "P1"
    assert state["g0_integrity"] is True
    assert state["meaning_receipt_valid"] is True

    second = job.confirm_meaning(
        job_root=dest,
        page_file=page,
        human_id="JL",
        confirmed_at="2026-09-01T12:00:00Z",
        accept_current_schema=True,
    )
    assert second["updated_count"] == 0


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
    forged["meaning_receipt_checksum"] = "0" * 64
    write(g0_path, json.dumps(forged, indent=2, sort_keys=True) + "\n")
    invalid = job.status(dest)
    assert invalid["phase"] == "P0"
    assert invalid["g0_receipt_valid"] is False
    assert "G0 receipt is invalid or semantically unbound" in invalid["integrity_errors"]
