"""A Supporting Run is named from the Page's own Project and world (REACH-SPACE 261005).

`b01j01t01r01` was a census Run in Project-0's tasks/ and a Paper Run in another
Project's discoveries/; the SPACE-wide registry named the Paper Run under the census.
"""
from pathlib import Path

from src.evidence_lines import _local_run_name


def _touch(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x\n", encoding="utf-8")
    return path


def test_execution_run_is_named_from_this_projects_tasks(tmp_path):
    here = tmp_path / "examples" / "Project-A"
    _touch(here / "project.yaml")
    _touch(here / "tasks/b01_x/j01_census/t01_catalog/runs/r01_deid_derived.cmd")
    _touch(here / "discoveries/b01_y/j01_papers/t01_review/runs/r01_slaby2022.sh")
    _touch(tmp_path / "examples/Project-B/project.yaml")
    _touch(tmp_path / "examples/Project-B/discoveries/b01_z/j01_p/t01_r/runs/r01_other.sh")
    page = _touch(here / "tasks/b01_x/reports/q01_t/q01_t.md")
    assert _local_run_name(page, "b01j01t01r01", "Execution") == "r01_deid_derived"
    assert _local_run_name(page, "b01j01t01r01", "Discovery") == "r01_slaby2022"
    assert _local_run_name(page, "b09j01t01r01", "Execution") == ""
