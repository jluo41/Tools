"""Receipt dialects the Task Workbench must read (REACH-SPACE, 261005).

A Databricks Run is a `.cmd` ticket whose receipt says `status: ok`; an extraction keeps
its row-level output on the server and lists it under `outputs:`; a laptop selftest may
seed a receipt before the server ever ran the Run.
"""
from pathlib import Path

from live.runs import _fields, _status, _ticket_files


def _receipt(tmp_path: Path, text: str, extra: str | None = None) -> Path:
    result = tmp_path / "results" / "r01_table"
    result.mkdir(parents=True)
    (result / "runtime.yaml").write_text(text, encoding="utf-8")
    if extra:
        (result / extra).write_text("x\n", encoding="utf-8")
    return result / "runtime.yaml"


def test_cmd_ticket_is_a_ticket(tmp_path):
    runs = tmp_path / "runs"
    runs.mkdir()
    (runs / "r01_table.cmd").write_text("@echo off\n", encoding="utf-8")
    assert [p.name for p in _ticket_files(runs)] == ["r01_table.cmd"]


def test_ok_with_a_local_file_is_done(tmp_path):
    runtime = _receipt(tmp_path, "run: r01_table\nstatus: ok\nhost: databricks\n", "census.csv")
    assert _status(runtime, _fields(runtime)) == "Done"


def test_ok_with_server_outputs_and_no_local_file_is_done(tmp_path):
    runtime = _receipt(tmp_path, 'run: r01_table\nstatus: "ok"\n'
                                 'outputs: [{"table": "signal", "rows": 12}]\nresults: []\n')
    assert _status(runtime, _fields(runtime)) == "Done"
    block = _receipt(tmp_path / "b", "status: ok\noutputs:\n  - table: signal\n    rows: 12\n")
    assert _status(block, _fields(block)) == "Done"


def test_ok_with_nothing_local_and_no_outputs_is_held(tmp_path):
    runtime = _receipt(tmp_path, "run: r01_table\nstatus: ok\noutputs: []\nresults: []\n")
    assert _status(runtime, _fields(runtime)) == "Held"


def test_a_selftest_seed_is_still_planned(tmp_path):
    runtime = _receipt(tmp_path, "run: r01_table\nstatus: ok\nhost: laptop-selftest\n", "profile.json")
    assert _status(runtime, _fields(runtime)) == "Ready"


def test_a_run_in_its_own_folder_pairs_with_its_result(tmp_path):
    """One folder per Run (haipipe-run 0.31.0): runs/<run>/<run>.cmd beside runs/<run>/result/."""
    from live.runs import _run_folder_receipt, _ticket_files
    run = tmp_path / "runs" / "r01_table"
    (run / "result").mkdir(parents=True)
    (run / "r01_table.cmd").write_text("@echo off\n", encoding="utf-8")
    (run / "run.yaml").write_text("run: r01_table\nkind: hard\n", encoding="utf-8")
    (run / "result" / "runtime.yaml").write_text("status: ok\n", encoding="utf-8")
    (run / "result" / "r01_card.md").write_text("a Result file named like a ticket\n", encoding="utf-8")
    (tmp_path / "runs" / "r02_old.cmd").write_text("@echo off\n", encoding="utf-8")
    tickets = _ticket_files(tmp_path / "runs")
    assert [p.name for p in tickets] == ["r01_table.cmd", "r02_old.cmd"]
    assert _run_folder_receipt(tickets[0]) == run / "result" / "runtime.yaml"
    assert _run_folder_receipt(tickets[1]) is None
