"""A Deliverable's ✅ waits on the Runs its maker read (Proj-PD2D 261118): a maker that said ok on a CaseSet whose
Run never finished leaves the item 🔶, not ✅."""
from pathlib import Path

import yaml

from live.work_progress_deliverables import item_state, unfinished_upstream


def runs(task, name, card, receipt=None):
    folder = task / "runs" / name
    (folder / "result").mkdir(parents=True)
    (folder / "run.yaml").write_text(yaml.safe_dump(dict(run=name, kind="hard", **card)))
    if receipt:
        (folder / "result" / "runtime.yaml").write_text(yaml.safe_dump(receipt))
    return folder


def test_a_maker_that_read_an_unfinished_run_does_not_tick(tmp_path):
    project = tmp_path / "Project-X"
    (project).mkdir()
    (project / "project.md").write_text("# X\n")
    up_task = project / "work/b03_cases/j51_case/t01_make"
    down_task = project / "work/b10_aidata/j51_aidata/t01_make"
    runs(up_task, "r06_casev2", {"status": "planned", "goal": "Build CaseSet v2"})
    runs(down_task, "r08_aidata_v2", {"goal": "Build v1 from CaseSet v2 (r06_casev2), one case per patient"},
         {"status": "ok"})
    (down_task / "runs/r08_aidata_v2/result/aidata.json").write_text("{}")
    item = {"what": "AIDataSet v2", "files": "runs/r08_aidata_v2/result/aidata.json", "run": "r08_aidata_v2",
            "owner": down_task}
    assert item_state(item, tmp_path, {})[0] == "partly"
    row = {"run": "r08_aidata_v2", "path": down_task / "runs/r08_aidata_v2",
           "card": yaml.safe_load((down_task / "runs/r08_aidata_v2/run.yaml").read_text())}
    assert unfinished_upstream(row, tmp_path) == ["r06_casev2"]

    (up_task / "runs/r06_casev2/result/runtime.yaml").write_text(yaml.safe_dump({"status": "ok"}))
    from live import work_progress_records as R
    R._TTL.clear()
    assert unfinished_upstream(row, tmp_path) == []
    assert item_state(item, tmp_path, {})[0] == "done"


def test_reads_on_the_card_counts_and_a_word_that_is_no_run_is_ignored(tmp_path):
    task = tmp_path / "b01/j01/t01"
    runs(task, "r01_base", {"status": "failed"})
    row = {"run": "r02_fit", "path": runs(task, "r02_fit", {"reads": ["t01/r01_base"], "goal": "see r99_nowhere"}),
           "card": {"reads": ["t01/r01_base"], "goal": "see r99_nowhere"}}
    assert unfinished_upstream(row, tmp_path) == ["r01_base"]


def test_an_unfinished_run_two_steps_up_still_blocks(tmp_path):
    (tmp_path / "project.md").write_text("# X\n")
    runs(tmp_path / "work/b03/j51/t01", "r06_case", {"status": "planned"})
    runs(tmp_path / "work/b10/j51/t01", "r08_aidata", {"goal": "from b03 r06_case"}, {"status": "ok"})
    fit = runs(tmp_path / "work/b11/j51/t01", "r06_fit", {"goal": "train on b10 r08_aidata"}, {"status": "ok"})
    row = {"run": "r06_fit", "path": fit, "card": yaml.safe_load((fit / "run.yaml").read_text())}
    assert unfinished_upstream(row, tmp_path) == ["r06_case"]
