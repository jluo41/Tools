"""health row `evidence-files` FAILs at the final gate where the page shows 📊❗ (a path that is not on disk)."""
from collections import namedtuple
from pathlib import Path

from src.support_health import check_files

F = namedtuple("F", "level row text")


def _task(tmp: Path, expected: str) -> Path:
    task = tmp / "j11_writing" / "t02_results"
    (task / "draft").mkdir(parents=True)
    (tmp / "runs" / "r01" / "result").mkdir(parents=True)
    (tmp / "runs" / "r01" / "result" / "values.csv").write_text("V_auc,0.81\n")
    (task / "draft" / "t02_results-evidence-items.md").write_text(
        f"### E01-VALUE-auc · AUC\n- **Target**: C1.P1.S1\n- **Expected**: {expected} V_auc\n")
    return task / "draft" / "t02_results-evidence-items.md"


def test_a_wrong_path_warns(tmp_path):
    out = []
    check_files(_task(tmp_path, "wrong-space/runs/r01/result/"), out, F, "WARN", "OK")
    assert out[-1].level == "WARN" and "E01" in out[-1].text and "not found" in out[-1].text


def test_a_real_path_passes(tmp_path):
    out = []
    check_files(_task(tmp_path, "runs/r01/result/"), out, F, "WARN", "OK")
    assert out[-1].level == "OK"
