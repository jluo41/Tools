from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("subjective_label_gates", HERE / "gates.py")
assert SPEC and SPEC.loader
gates = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gates)


@pytest.mark.parametrize(
    ("config_text", "message"),
    [
        ("labels: [HIGH, LOW]\n", "unsupported schema_version missing"),
        ("schema_version: subjective-label/v999\n", "unsupported schema_version"),
        ("schema_version: [subjective-label/v2]\n", "unsupported schema_version"),
        ("- not-a-mapping\n", "must contain a YAML mapping"),
        ("schema_version: [\n", "cannot read"),
    ],
)
def test_guard_job_root_holds_missing_malformed_or_unknown_schema(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, config_text: str, message: str
) -> None:
    job_root = tmp_path / "job"
    job_root.mkdir()
    (job_root / "config.yaml").write_text(config_text, encoding="utf-8")
    calls = []
    monkeypatch.setitem(sys.modules, "job", SimpleNamespace(status=lambda _root: calls.append(True)))

    with pytest.raises(gates.GateHold, match=message):
        gates.guard_job_root(job_root, "G0")
    assert calls == []


def test_guard_job_root_holds_when_config_is_missing_or_root_is_none(
    tmp_path: Path,
) -> None:
    with pytest.raises(gates.GateHold, match="missing job config"):
        gates.guard_job_root(tmp_path / "missing", "G0")
    with pytest.raises(gates.GateHold, match="job root is required"):
        gates.guard_job_root(None, "G0")


def test_guard_job_root_keeps_v2_gate_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    job_root = tmp_path / "job"
    job_root.mkdir()
    (job_root / "config.yaml").write_text(
        yaml.safe_dump({"schema_version": "subjective-label/v2"}), encoding="utf-8"
    )
    ready = {
        "p0_contract_integrity_valid": True,
        "hold": False,
        "meaning_receipt_valid": True,
        "g0_receipt_valid": True,
    }
    calls = []
    monkeypatch.setitem(
        sys.modules,
        "job",
        SimpleNamespace(status=lambda root: calls.append(root) or ready),
    )

    assert gates.guard_job_root(job_root, "G0") is True
    assert calls == [job_root]
