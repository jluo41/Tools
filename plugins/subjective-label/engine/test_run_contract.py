import importlib.util
import json
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
    assert addresses[0].startswith("rl01_corpus-contract_")
    assert addresses[-1].startswith("rl43_dstar-materialize_")


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

    assert "P tag (compatibility only)" in completed.stdout
    assert "Compat tag (not authority)" in completed.stdout
    assert "P0-P5 are compatibility capability tags only" in completed.stdout
    tag_counts = {
        line.split()[0]: int(line.split()[1])
        for line in completed.stdout.splitlines()
        if line.split() and line.split()[0] in {"P0", "P1", "P2", "P3", "P4", "P5"}
    }
    assert tag_counts == {"P0": 6, "P1": 19, "P2": 1, "P3": 8, "P4": 5, "P5": 4}
    total_line = next(line for line in completed.stdout.splitlines() if line.startswith("TOTAL"))
    assert total_line.split() == ["TOTAL", "43"]
    assert "rl43_dstar-materialize_d-star-v1" in completed.stdout


def test_optional_p0_run_counts_can_be_zero_and_match_formula():
    catalog = _catalog_module()
    runs = catalog.plan_runs(
        discovery=2,
        round_weak=(0, 2, 2),
        executors=3,
        shards=1,
        guideline_seed_count=0,
        test_reserve_count=0,
        embedding_build_count=0,
    )

    assert len(runs) == 40
    assert not {
        "guideline-seed",
        "test-reserve",
        "embedding-build",
    }.intersection(run.operation for run in runs)
    assert len(runs) == 2 + 0 + 0 + 0 + 4 + 5 * 3 + 2 * 3 + 1 + 12


def test_planner_cli_accepts_zero_optional_p0_counts():
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
            "--guideline-seeds",
            "0",
            "--test-reservations",
            "0",
            "--embedding-builds",
            "0",
            "--json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    operations = [run["operation"] for run in payload["runs"]]
    assert payload["planned_count"] == 40
    assert payload["phase_semantics"] == (
        "compatibility capability tag only; not Workflow route authority"
    )
    assert "guideline-seed" not in operations
    assert "test-reserve" not in operations
    assert "embedding-build" not in operations


def test_labeling_run_ids_use_the_native_rl_namespace():
    catalog = _catalog_module()
    runs = catalog.plan_runs(discovery=0, round_weak=(0,), executors=1, shards=1)

    assert runs
    assert all(run.run.startswith("rl") for run in runs)
    assert all("_labeling-" not in run.run for run in runs)


def test_neutral_run_presenter_and_family_workflows_use_granular_dialect():
    paths = (
        TOOLKIT_ROOT / "skills" / "run" / "haipipe-run" / "SKILL.md",
        TOOLKIT_ROOT
        / "skills"
        / "page"
        / "haipipe-workbench-page"
        / "ref"
        / "run-space.md",
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
    assert "Bare approval, signature" in text


def test_planner_rejects_negative_cardinality():
    catalog = _catalog_module()
    for kwargs, expected in (
        ({"discovery": -1}, "discovery must be non-negative"),
        ({"guideline_seed_count": -1}, "guideline_seed_count must be non-negative"),
        ({"test_reserve_count": -1}, "test_reserve_count must be non-negative"),
        ({"embedding_build_count": -1}, "embedding_build_count must be non-negative"),
    ):
        values = {
            "discovery": 0,
            "round_weak": (0,),
            "executors": 1,
            "shards": 1,
            **kwargs,
        }
        try:
            catalog.plan_runs(**values)
        except ValueError as exc:
            assert expected in str(exc)
        else:
            raise AssertionError(f"negative cardinality must fail: {expected}")


def test_planner_rejects_missing_required_routes():
    catalog = _catalog_module()
    for kwargs, expected in (
        ({"round_weak": ()}, "round_weak must contain at least one calibration round"),
        ({"executors": 0}, "executors must be at least 1"),
        ({"shards": 0}, "shards must be at least 1"),
    ):
        values = {
            "discovery": 0,
            "round_weak": (0,),
            "executors": 1,
            "shards": 1,
            **kwargs,
        }
        try:
            catalog.plan_runs(**values)
        except ValueError as exc:
            assert expected in str(exc)
        else:
            raise AssertionError(f"missing required route must fail: {expected}")
