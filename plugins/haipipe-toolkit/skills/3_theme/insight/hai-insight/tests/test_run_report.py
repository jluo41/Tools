"""A Run's report: an agent's reading of one Run's result, beside result/, checked by another (ref/run-report.md; T31).

A placeholder Board is built in a temp folder: two Jobs, each with a question Task whose Runs hold a small table, and
a prep Task whose Run holds a card and a step's metrics. No real names and no data.
"""
import importlib.util
import sys
from pathlib import Path

import pytest
import yaml

HERE = Path(__file__).resolve().parent
REF = HERE.parent / "ref"
sys.path.insert(0, str(REF))
import run_report as RR  # noqa: E402

TABLE = "grouping,n_levels,n_suppressed,share\narm,13,0,0.0\nstate,73,20,0.27397\nhour,24,0,0.0\n"
WRITER, CHECKER = "hai-insight-agent", "hai-insight-reviewer-agent"


def _run(task: Path, stem: str, status="ok", sha="aaa111", table=TABLE, reason="", question="D05") -> Path:
    run = task / "runs" / stem
    (run / "result").mkdir(parents=True)
    (run / "run.yaml").write_text(yaml.safe_dump({"run": stem, "kind": "hard", "question": question,
                                                  "partition": stem.split("_", 1)[1], "status": status}))
    rec = {"status": status, **({"tables_sha256": sha} if status == "ok" else {}), **({"reason": reason} if reason else {})}
    (run / "result" / "runtime.yaml").write_text(yaml.safe_dump(rec))
    if status == "ok":
        (run / "result" / "grouping_audit.csv").write_text(table)
    (run / "result" / "partition_power.csv").write_text("partition,n,mde,effect\nfull,4000,0.12,0.05\n")
    return run


@pytest.fixture
def board(tmp_path):
    (tmp_path / "env.sh").write_text("# placeholder SPACE\n")
    b = tmp_path / "examples-x" / "Project-Demo" / "insight" / "Insight-Demo"
    b.mkdir(parents=True)
    (b / "board.md").write_text("---\nboard-kind: insight-board\n---\n")
    for job in ("j01_question-v1-basic_data-v1", "j02_data-v1_prep-v1_question-v1"):
        t = b / job / ("t05_D05_levels" if job.startswith("j01") else "t06_D05_levels")
        (b / job / "runs" / "run-launch-j01").mkdir(parents=True)      # a Job's own soft Runs sit beside its Tasks
        t.mkdir(parents=True)
        (t / f"{t.name}.md").write_text("---\nquestion: D05\n---\n\n# D05 · Levels\n\n**The ask**: which levels are thin?\n")
        _run(t, "r01_full")
        _run(t, "r02_older", status="refused", reason="underpowered: older MDE 0.12 > 0.05")
    return b


SPEC = {"headline": "Most groupings keep every level; state and hour differ.",
        "sentences": [{"text": "State has 73 levels and 20 fall below the floor, 27.4% of them.", "file": "grouping_audit.csv"}],
        "caveat": "Counts of levels, not of people."}


def test_a_report_is_written_beside_result_and_kept_by_a_rerun(board):
    run = next(board.glob("j01*/t05*/runs/r01_full"))
    assert RR.state(run) == "missing"
    md = RR.write(run, SPEC, WRITER)
    assert md == run / "report.md" and md.parent.name == "r01_full"
    fm = RR.front(md)
    assert fm["result-sha256"] == "aaa111" and fm["headline"].startswith("Most groupings") and fm["check"] == ""
    assert "(`grouping_audit.csv`)" in md.read_text() and "**Caveat**" in md.read_text()
    assert RR.state(run) == "unchecked"
    for f in (run / "result").iterdir():                  # a rerun: the ticket clears result/ only
        f.unlink()
    _rerun = yaml.safe_dump({"status": "ok", "tables_sha256": "aaa111"})
    (run / "result" / "runtime.yaml").write_text(_rerun)
    (run / "result" / "grouping_audit.csv").write_text(TABLE)
    assert md.is_file() and RR.state(run) == "unchecked"
    (run / "result" / "runtime.yaml").write_text(yaml.safe_dump({"status": "ok", "tables_sha256": "bbb222"}))
    assert RR.state(run) == "stale"
    with pytest.raises(RR.Refused, match="write it again"):
        RR.check(run, CHECKER)


def test_the_writer_cannot_check_and_every_number_traces(board):
    run = next(board.glob("j01*/t05*/runs/r01_full"))
    RR.write(run, SPEC, WRITER)
    with pytest.raises(RR.Refused, match="another agent"):
        RR.check(run, WRITER)
    assert RR.check(run, CHECKER).startswith("✅")       # 73, 20 in the table; 27.4% is 0.27397 as a share
    bad = dict(SPEC, sentences=[{"text": "Of 130 levels, 9 are suppressed in 2 groupings.", "file": "grouping_audit.csv"}])
    RR.write(run, bad, WRITER)
    assert RR.state(run) == "unchecked"
    with pytest.raises(RR.Refused, match="130.*9.*2|130"):
        RR.check(run, CHECKER)
    with pytest.raises(RR.Refused, match="9"):
        RR.check(run, CHECKER, accept=("130",))
    assert RR.check(run, CHECKER, accept=("130", "9", "2")).startswith("✅")
    assert RR.front(run / "report.md")["accepted"] == ["130", "9", "2"]
    RR.check(run, CHECKER, reject="the second sentence reads a count the table does not give")
    assert RR.state(run) == "returned"


def test_names_are_not_numbers():
    got = [w for w, *_ in RR.sentence_numbers("D05 on r01_full: prior_clicks_7d has 77 levels, ages 18-24, `t06` −0.5")]
    assert got == ["77", "18", "24", "−0.5"]


def test_a_headline_gives_only_numbers_its_sentences_give(board):
    run = next(board.glob("j01*/t05*/runs/r01_full"))
    RR.write(run, dict(SPEC, headline="State keeps 53 of its 73 levels."), WRITER)
    with pytest.raises(RR.Refused, match="headline: 53"):
        RR.check(run, CHECKER)
    RR.write(run, dict(SPEC, headline="State loses 20 of its 73 levels."), WRITER)
    assert RR.check(run, CHECKER).startswith("✅")


def test_a_count_of_rows_is_derived_by_its_rule(board):
    run = next(board.glob("j01*/t05*/runs/r01_full"))
    s = {"text": "1 of the 3 groupings has a thin level (33%), holding 20 of 110 levels", "file": "grouping_audit.csv",
         "derived": [{"value": 1, "how": "count rows where n_suppressed > 0"}, {"value": 3, "how": "count rows"},
                     {"value": "33%", "how": "1 / 3"}, {"value": 110, "how": "sum n_levels"}]}
    RR.write(run, dict(SPEC, headline="One grouping of 3 has thin levels.", sentences=[s]), WRITER)
    assert RR.problems(run / "result", RR.front(run / "report.md")) == ([], [], [])   # "One" is a word; 3 a sentence's
    assert RR.check(run, CHECKER).startswith("✅")      # every number traced or computed, no --accept
    wrong = dict(s, derived=[{"value": 3, "how": "count rows where n_levels > 20"}])
    with pytest.raises(RR.Refused, match="gives 2"):
        RR.write(run, dict(SPEC, sentences=[wrong]), WRITER)
    with pytest.raises(RR.Refused, match="not a number the sentence gives"):
        RR.write(run, dict(SPEC, sentences=[dict(s, derived=[{"value": 7, "how": "count rows"}])]), WRITER)
    hand = dict(s, derived=[{"value": 1, "how": "the groupings a reader would call thin"}])
    RR.write(run, dict(SPEC, sentences=[hand]), WRITER)
    with pytest.raises(RR.Refused, match="the groupings a reader"):
        RR.check(run, CHECKER)                            # a rule it cannot read: confirmed by hand
    with pytest.raises(RR.Refused, match="3"):
        RR.check(run, CHECKER, accept=("1",))             # 3 and 110 are no longer derived and in no cell
    assert RR.check(run, CHECKER, accept=("1", "3", "110", "33%")).startswith("✅")


def test_a_sentence_may_join_two_files(board):
    run = next(board.glob("j01*/t05*/runs/r01_full"))
    s = {"text": "State's 20 thin levels are 0.5% of the segment's 4,000 rows", "files": ["grouping_audit.csv", "partition_power.csv"],
         "derived": [{"value": "0.5%", "how": "20 / 4000"}]}
    RR.write(run, dict(SPEC, sentences=[s]), WRITER)
    assert "(`grouping_audit.csv`, `partition_power.csv`)" in (run / "report.md").read_text()
    assert RR.check(run, CHECKER).startswith("✅")
    two = dict(s, derived=[{"value": "0.5%", "how": "20 / 4000"}, {"value": 20, "how": "max n_suppressed"}])
    RR.write(run, dict(SPEC, sentences=[two]), WRITER)
    with pytest.raises(RR.Refused, match="in <file>"):
        RR.check(run, CHECKER)                            # two tables: the rule names one
    two["derived"][1]["how"] = "max n_suppressed in grouping_audit.csv"
    RR.write(run, dict(SPEC, sentences=[two]), WRITER)
    assert RR.check(run, CHECKER).startswith("✅")


def test_an_older_runs_generated_report_becomes_tables(board):
    run = next(board.glob("j01*/t05*/runs/r01_full"))
    RR.write(run, SPEC, WRITER)
    (run / "result" / "report.md").write_text("# D05\n\nGenerated by hai-insight ref/run_job.py from this run's results\n")
    before = RR.result_hash(run)
    assert [r.name for r in RR.tables(run.parent.parent.parent)] == ["r01_full"]
    assert (run / "result" / "tables.md").is_file() and not (run / "result" / "report.md").exists()
    assert RR.result_hash(run) == before and RR.state(run) == "unchecked"
    assert RR.tables(run) == []


def test_a_spec_cites_only_its_own_result_and_a_failed_run_has_no_report(board):
    run = next(board.glob("j01*/t05*/runs/r01_full"))
    with pytest.raises(RR.Refused, match="not a file of this Run"):
        RR.write(run, dict(SPEC, sentences=[{"text": "x", "file": "../run.yaml"}]), WRITER)
    with pytest.raises(RR.Refused, match="unknown key"):
        RR.write(run, dict(SPEC, takeaway="x"), WRITER)
    failed = _run(run.parent.parent, "r03_young", status="failed")
    with pytest.raises(RR.Refused, match="fix and rerun"):
        RR.write(failed, SPEC, WRITER)
    assert RR.state(failed) == ""


def test_a_refused_run_reports_its_reason(board):
    run = next(board.glob("j01*/t05*/runs/r02_older"))
    RR.write(run, {"headline": "Too few in this segment to read a difference of 5%.",
                   "sentences": [{"text": "Its smallest readable effect is 0.12, above the 0.05 asked.",
                                  "file": "partition_power.csv"}]}, WRITER)
    text = (run / "report.md").read_text()
    assert "**Refused**: underpowered" in text
    assert RR.check(run, CHECKER).startswith("✅")
    (run / "result" / "runtime.yaml").write_text(yaml.safe_dump({"status": "refused", "reason": "underpowered: other"}))
    assert RR.state(run) == "stale"                       # its reason is part of its result


def test_todo_and_carry_from_an_earlier_job_with_the_same_result(board):
    j01, j02 = sorted(p for p in board.iterdir() if p.is_dir())
    src = next(j01.glob("t05*/runs/r01_full"))
    RR.write(src, SPEC, WRITER)
    RR.check(src, CHECKER)
    assert dict((r.name, s) for s, r in RR.todo(j02)) == {"r01_full": "missing", "r02_older": "missing"}
    carried = RR.carry(j02)
    assert [r.name for r in carried] == ["r01_full"]      # r02's earlier report is not written: nothing to carry
    fm = RR.front(carried[0] / "report.md")
    assert fm["carried-from"].startswith("examples-x/") and fm["check"].startswith("✅") and fm["run"] == "r01_full"
    assert RR.state(carried[0]) == "checked"
    other = next(j02.glob("t06*/runs/r02_older"))
    assert [(s, r.name) for s, r in RR.todo(j02)] == [("missing", other.name)]
    (carried[0] / "report.md").unlink()                   # a different result is never carried
    (carried[0] / "result" / "runtime.yaml").write_text(yaml.safe_dump({"status": "ok", "tables_sha256": "ccc"}))
    assert RR.carry(j02) == []


def test_a_prep_run_reports_its_card_and_checks(board):
    t01 = next(board.glob("j02*")) / "t01_prep-v1_raw-chain"
    run = t01 / "runs" / "r01_demo"
    (run / "result" / "steps" / "t02_source").mkdir(parents=True)
    (run / "run.yaml").write_text(yaml.safe_dump({"run": "r01_demo", "kind": "hard", "type": "prep", "prep": "prep-v1"}))
    (run / "result" / "runtime.yaml").write_text(yaml.safe_dump({"status": "done", "steps": [{"step": "t01", "status": "done"}]}))
    (run / "result" / "experiment_card.json").write_text('{"arms": 13, "days": 18}')
    (run / "result" / "steps" / "t02_source" / "metrics.json").write_text('{"rows": 444691, "columns": 61}')
    assert RR.identity(run) == ("prep-v1", "demo")
    RR.write(run, {"headline": "The export matches its card: 13 arms over 18 days.",
                   "sentences": [{"text": "The card states 13 arms over 18 days.", "file": "experiment_card.json"},
                                 {"text": "The source step kept 444,691 rows and 61 columns.",
                                  "file": "steps/t02_source/metrics.json"}]}, WRITER)
    assert RR.check(run, CHECKER).startswith("✅")
    (run / "result" / "steps" / "t02_source" / "metrics.json").write_text('{"rows": 444690, "columns": 61}')
    assert RR.state(run) == "stale"


def test_the_task_page_takes_each_run_report_headline(board):
    _spec = importlib.util.spec_from_file_location("write_answer_page", REF / "write_answer_page.py")
    W = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(W)
    task = next(board.glob("j02*/t06*"))
    assert W._board_task(task)                            # a Job of three versions is a Board Job
    full, older = task / "runs" / "r01_full", task / "runs" / "r02_older"
    RR.write(full, SPEC, WRITER)
    spec = {"answer-status": "answered", "answer": "Most levels can be read.", "how-sure": "the counts are exact",
            "divisions": [{"partition": "full", "bullets": [{"draft": "State has 20 thin levels", "file": "grouping_audit.csv"}]},
                          {"partition": "older", "takeaway": "Too few to read."}]}
    W.build_task_page(task, spec)
    face = RR.front(task / f"{task.name}.md")
    assert face["takeaways"] == {"full": SPEC["headline"], "older": "Too few to read."}
    (full / "result" / "runtime.yaml").write_text(yaml.safe_dump({"status": "ok", "tables_sha256": "zzz"}))
    with pytest.raises(SystemExit, match="stale"):
        W.build_task_page(task, spec)
    assert older.is_dir()


def test_the_workbench_reads_the_same_hash():
    spec = importlib.util.spec_from_file_location(
        "insight_plan_c", HERE.parents[4] / "servers" / "workbench-insight" / "insight_plan_c.py")
    P = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(P)
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        task = Path(d) / "t06_D05_x"
        for stem, status in (("r01_full", "ok"), ("r02_older", "refused")):
            run = _run(task, stem, status=status, reason="thin" if status == "refused" else "")
            assert P.result_hash(run) == RR.result_hash(run)
            RR.write(run, SPEC if status == "ok" else dict(SPEC, sentences=[{"text": "x", "file": "partition_power.csv"}]), WRITER)
            card = P.run_card(run)
            assert card["run_report"]["headline"] == SPEC["headline"] and not card["run_report"]["stale"]
            assert P.report_headline(card) == SPEC["headline"]
