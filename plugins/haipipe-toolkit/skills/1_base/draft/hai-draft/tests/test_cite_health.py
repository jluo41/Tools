"""Folder health's citation look (hai-paper must-check M-D20): a CITE item with no Local Run is a WARN while
writing and a FAIL at the final gate; a bound item, or a retired one, raises nothing; a bound Result that is gone
is a WARN."""
from pathlib import Path

from src.folder_health import FAIL, WARN, folder_health

from test_folder_health import ITEMS, levels, make

CITE = """
### E02-CITE-kaplan · C1.P1.B2 · kaplan2020
- **Target**: C1.P1.B2
- **Label**: kaplan2020
- **Local Input**: @misc{kaplan2020,
"""
BOUND = "- **Local Run**: Page · Evidence Item · reuse · P.j03.t01.r01 → {path}\n"
RETIRED = "\n#### E03-CITE-old · retired · was C1.P1.B3\n- **Label**: old2019\n"


def test_an_unbound_cite_item_warns_then_fails_at_the_final_gate(tmp_path):
    folder = make(tmp_path, items=ITEMS + CITE)
    report = folder_health(folder)
    assert levels(report, "cite") == [WARN]
    msg = next(f["message"] for f in report["findings"] if f["check"] == "cite")
    assert "E02" in msg and "cite_tasks.py bind" in msg
    assert levels(folder_health(folder, final=True), "cite") == [FAIL]


def test_a_bound_or_retired_cite_item_is_quiet(tmp_path):
    result = tmp_path / "j03_evidence_cite/t01_scaling_laws/runs/r01_check_citations/result/citations.csv"
    result.parent.mkdir(parents=True)
    result.write_text("key\nkaplan2020\n", encoding="utf-8")
    rel = result.relative_to(tmp_path).as_posix()
    report = folder_health(make(tmp_path, items=ITEMS + CITE + BOUND.format(path=rel) + RETIRED))
    assert levels(report, "cite") == []


def test_a_bound_result_that_is_gone_warns(tmp_path):
    report = folder_health(make(tmp_path, items=ITEMS + CITE + BOUND.format(path="j03_gone/result/citations.csv")))
    msgs = [f["message"] for f in report["findings"] if f["check"] == "cite"]
    assert len(msgs) == 1 and "not on disk" in msgs[0] and "E02" in msgs[0]
