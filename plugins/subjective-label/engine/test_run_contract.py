import importlib.util
import subprocess
import sys
from collections import Counter
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
PLUGINS_ROOT = PLUGIN_ROOT.parent
TOOLKIT_ROOT = PLUGINS_ROOT / "haipipe-toolkit"
CATALOG_PATH = PLUGIN_ROOT / "engine" / "run_catalog.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _catalog_module():
    spec = importlib.util.spec_from_file_location("subjective_label_run_catalog", CATALOG_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_labeling_run_dialect_declares_exact_operation_catalog_and_envelope():
    catalog = _catalog_module()
    contract = _read(PLUGIN_ROOT / "ref" / "ref-run.md")

    assert len(catalog.OPERATION_KINDS) == 25
    assert len(set(catalog.OPERATION_KINDS)) == 25
    for operation in catalog.OPERATION_KINDS:
        assert f"`{operation}`" in contract

    for path in (
        "runs/<RUNNAME>.yaml",
        "results/<RUNNAME>/runtime.yaml",
        "results/<RUNNAME>/result.yaml",
    ):
        assert path in contract

    assert "`Round`, `Test`," in contract
    assert "`Scan`, and `Audit` are episodes" in contract
    assert "gate event" in contract
    assert "actual count is the number of" in contract


def test_happy_path_formula_plans_43_runs_with_expected_phase_counts():
    catalog = _catalog_module()
    runs = catalog.plan_runs(discovery=2, round_weak=(0, 2, 2), executors=3, shards=1)

    assert len(runs) == 43
    assert Counter(run.phase for run in runs) == {
        "P0": 6,
        "P1": 19,
        "P2": 1,
        "P3": 8,
        "P4": 5,
        "P5": 4,
    }
    assert Counter(run.operation for run in runs)["weak-prelabel"] == 4
    assert Counter(run.operation for run in runs)["executor-predict"] == 3
    assert Counter(run.operation for run in runs)["executor-score"] == 3
    assert Counter(run.operation for run in runs)["scan-shard"] == 1

    addresses = [run.run for run in runs]
    assert len(addresses) == len(set(addresses))
    assert addresses[0].startswith("r01_labeling-corpus-contract_")
    assert addresses[-1].startswith("r43_labeling-dstar-materialize_")


def test_planner_cli_executes_the_documented_example():
    completed = subprocess.run(
        [
            sys.executable,
            str(CATALOG_PATH),
            "plan",
            "--discovery",
            "2",
            "--round-weak",
            "0,2,2",
            "--executors",
            "3",
            "--shards",
            "1",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "P0        6" in completed.stdout
    assert "P1       19" in completed.stdout
    assert "TOTAL    43" in completed.stdout
    assert "r43_labeling-dstar-materialize_d-star-v1" in completed.stdout


def test_neutral_run_presenter_and_family_workflows_use_granular_dialect():
    paths = (
        TOOLKIT_ROOT / "skills" / "run" / "haipipe-run" / "SKILL.md",
        TOOLKIT_ROOT
        / "skills"
        / "board"
        / "page-plugins"
        / "haipipe-plugin-runs"
        / "SKILL.md",
        PLUGIN_ROOT / "skills" / "subjective-label" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "subjective-label-workflow" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "label-building" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "label-building-workflow" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "label-scanning" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "label-scanning-workflow" / "SKILL.md",
    )
    text = "\n".join(_read(path) for path in paths)

    for operation in (
        "guideline-seed",
        "embedding-build",
        "weak-prelabel",
        "human-calibration",
        "executor-predict",
        "executor-score",
        "scan-shard",
        "audit-human-gold",
        "dstar-materialize",
    ):
        assert operation in text

    for stale in (
        "one `qualification-test` Run",
        "one `production-scan` Run",
        "one `final-audit` Run",
        "Candidate executor predictions are internal attempts",
    ):
        assert stale not in text

    assert "Never add a second row for the Round, Test, Scan, or Audit episode" in text
    assert "Bare human" in text


def test_planner_rejects_negative_cardinality():
    catalog = _catalog_module()
    try:
        catalog.plan_runs(discovery=-1, round_weak=(), executors=1, shards=1)
    except ValueError as exc:
        assert "discovery must be non-negative" in str(exc)
    else:
        raise AssertionError("negative cardinality must fail")
