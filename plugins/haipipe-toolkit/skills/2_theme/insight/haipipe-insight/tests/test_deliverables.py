"""What a question delivers and how it is reviewed, read from its question file alone (ref/deliverables.py)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ref"))
import deliverables as DL  # noqa: E402

Q = {"id": "K01", "ask": "is the gap the same in both groups?", "needs": {
    "E1": {"kind": "cite", "what": "the gap in each group", "from": "I01.E2"},
    "E2": {"kind": "compute", "what": "the gaps and their difference", "pass": "three rows with intervals",
           "output": {"pooling.csv": ["part", "gap_pp", "gap_lo_pp", "gap_hi_pp"], "verdict.json": ["verdict"]}},
    "E3": {"kind": "compute", "what": "the rules", "pass": "per rule its error",
           "output": {"rules.csv": ["rule", "error"]}},
    "E4": {"kind": "judge", "what": "whether one counsel serves both", "from": ["E1", "E2"]},
    "E5": {"kind": "compute", "what": "an old table", "retired": "replaced by E2"}}}


def rows():
    return {r["id"]: r for r in DL.deliverables(Q)["needs"]}


def test_a_compute_need_delivers_its_tables_and_a_figure_per_known_shape():
    r = rows()
    assert r["E2"]["tables"] == ["pooling.csv", "verdict.json"]
    assert r["E2"]["figures"] == [{"table": "pooling.csv", "kind": "estimate", "declared": False}]
    assert r["E2"]["test"] == "three rows with intervals"


def test_a_table_of_no_known_shape_is_named_as_having_no_figure():
    assert rows()["E3"]["no_figure"] == ["rules.csv"]
    assert any("rules.csv has no known shape" in g for g in DL.gaps(Q))


def test_a_declared_figure_or_an_empty_list_closes_that_gap():
    q = {"id": "K01", "needs": {"E1": dict(Q["needs"]["E3"], figures=[{"table": "rules.csv", "kind": "bar"}]),
                                "E2": dict(Q["needs"]["E3"], figures=[])}}
    r = {x["id"]: x for x in DL.deliverables(q)["needs"]}
    assert r["E1"]["figures"] == [{"table": "rules.csv", "kind": "bar", "declared": True}]
    assert not r["E2"]["figures"] and not DL.gaps(q)


def test_kind_none_silences_one_table_and_keeps_the_needs_other_figures(tmp_path):
    need = {"kind": "compute", "what": "rates and their audit", "pass": "x",
            "output": {"gap.csv": ["part", "gap_pp", "gap_lo_pp", "gap_hi_pp"], "audit.csv": ["rule", "n"]},
            "figures": [{"table": "audit.csv", "kind": "none"}]}
    q = {"id": "I03", "needs": {"E1": need}}
    r = DL.deliverables(q)["needs"][0]
    assert [f["table"] for f in r["figures"]] == ["gap.csv"] and not r["no_figure"] and not DL.gaps(q)
    import pandas as pd
    pd.DataFrame({"part": ["a", "b"], "gap_pp": [1.0, 2.0], "gap_lo_pp": [0.0, 1.0], "gap_hi_pp": [2.0, 3.0]}).to_csv(
        tmp_path / "gap.csv", index=False)
    pd.DataFrame({"rule": ["r"], "n": [3]}).to_csv(tmp_path / "audit.csv", index=False)
    made = DL.figures.draw(tmp_path, q["needs"])
    assert [(m["table"], bool(m["file"])) for m in made] == [("gap.csv", True)]


def test_a_bar_with_long_names_tilts_them(tmp_path):
    import pandas as pd
    names = ["authenticated", "user_positive_feedback", "opted_out", "clicked", "delivered", "replied", "ignored"]
    pd.DataFrame({"outcome": names, "k": range(7)}).to_csv(tmp_path / "t.csv", index=False)
    seen = {}
    real = DL.figures._save
    DL.figures._save = lambda fig, path: seen.update(rot=[t.get_rotation() for t in fig.axes[0].get_xticklabels()]) or real(fig, path)
    try:
        DL.figures.draw(tmp_path, {"E1": {"kind": "compute", "output": {"t.csv": ["outcome", "k"]},
                                          "figures": [{"table": "t.csv", "kind": "bar", "x": "outcome", "y": "k"}]}})
    finally:
        DL.figures._save = real
    assert seen["rot"] and all(r == 45 for r in seen["rot"])


def test_a_judge_without_a_pass_line_has_no_test():
    assert any("K01.E4: review" in g for g in DL.gaps(Q))
    q = {"id": "K01", "needs": {"E1": dict(Q["needs"]["E4"], **{"pass": "one verdict word and where it stops"})}}
    assert not DL.gaps(q)


def test_a_retired_need_delivers_nothing():
    assert "E5" not in rows()


def test_the_brief_lists_one_review_line_per_live_need_then_the_level_and_the_trace():
    text = DL.brief(Q)
    review = text.split("## Review, one verdict per line")[1].strip().splitlines()
    assert [x.split(" · ")[0] for x in review] == ["- K01.E1", "- K01.E2", "- K01.E3", "- K01.E4", "- level", "- trace"]
    assert "NO TEST WRITTEN" in review[3] and "the cited need is answered" in review[0]


# ── insight_ladder.py review: where a Board's answers stand (scripts/insight_ladder_review.py) ──
def _board(tmp_path):
    import yaml
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    import insight_ladder  # noqa: F401 · puts ref/ on the path
    import insight_ladder_review as RV
    book = tmp_path / "insight" / "InsightQuestionBook-T" / "j01_question-v1_first"
    (book / "t01_K01_gap").mkdir(parents=True)
    (book / "t01_K01_gap" / "question.md").write_text("---\n" + yaml.safe_dump(
        {"id": "K01", "level": "knowledge", "needs": {"E1": {"kind": "judge", "what": "the reading", "from": ["E1"]}}})
        + "---\n")
    (book / "partitions.md").write_text("---\npartitions:\n- {name: full, where: []}\n- {name: young, where: []}\n---\n")
    board = tmp_path / "insight" / "Insight-T"
    job = board / "j01_question-v1-first_data-v1"
    task = job / "t01_K01_gap"
    for run, rec in (("r01_full", {"status": "ok", "content_since": "2026-11-10T00:00:00Z"}),
                     ("r02_young", {"status": "refused", "reason": "thin: too few rows"})):
        (task / "runs" / run / "result").mkdir(parents=True)
        (task / "runs" / run / "result" / "runtime.yaml").write_text(yaml.safe_dump(rec))
    (board / "board.md").write_text("---\nboard-kind: insight-board\nprototype: insight/InsightQuestionBook-T\n---\n")
    (job / f"{job.name}.md").write_text("---\nrelease: question-v1\n---\n")
    return RV, board, task


def _face(task, **fields):
    import yaml
    (task / f"{task.name}.md").write_text("---\n" + yaml.safe_dump(fields, allow_unicode=True) + "---\n")


def test_review_names_an_answer_older_than_its_tables_and_one_not_checked(tmp_path):
    RV, board, task = _board(tmp_path)
    _face(task, answer="it holds", **{"results-read": "2026-11-01T00:00:00Z", "check": ""})
    kinds = {k: w for _, k, w in RV.answers(board)}
    assert kinds["reread"] == "tables newer in r01_full" and kinds["check"] == "not checked"
    assert kinds["refused"] == "r02_young: thin: too few rows"


def test_review_is_quiet_on_a_current_checked_answer_and_on_one_not_written(tmp_path):
    RV, board, task = _board(tmp_path)
    _face(task, answer="it holds", **{"results-read": "2026-11-12T00:00:00Z", "check": "✅ 261112 · another agent"})
    assert [k for _, k, _ in RV.answers(board)] == ["refused"]
    _face(task, answer="")
    assert [k for _, k, _ in RV.answers(board)] == ["refused"]


def test_review_reads_the_question_book_a_board_pins(tmp_path, capsys):
    RV, board, _ = _board(tmp_path)
    _, notes = RV.review(board)
    assert any("K01.E1: review" in n for n in notes) and any("K01: links" in n for n in notes)
    assert any("segment young: no why" in n for n in notes) and not any("segment full" in n for n in notes)
