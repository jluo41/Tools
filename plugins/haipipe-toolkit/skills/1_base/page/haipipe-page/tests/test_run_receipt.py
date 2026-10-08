"""A VALUE or CITE item may bind a run's output file when the run's receipt vouches for it."""
from src.evidence_selection import run_receipt


def test_a_run_file_is_bound_by_its_runtime_receipt(tmp_path):
    run = tmp_path / "page" / "results" / "full"
    run.mkdir(parents=True)
    table = run / "column_inventory.csv"
    table.write_text("column,dtype\n")
    assert run_receipt(table) is None                      # no receipt, no binding
    (run / "runtime.yaml").write_text("status: ok\nquestion: D01\n")
    receipt, status = run_receipt(table)
    assert receipt == run / "runtime.yaml" and status == "ok"
    (run / "runtime.yaml").write_text("status: failed\n")
    assert run_receipt(table)[1] == "failed"
    stray = tmp_path / "page" / "notes.csv"
    stray.write_text("x\n")
    assert run_receipt(stray) is None                      # outside results/<run>/
