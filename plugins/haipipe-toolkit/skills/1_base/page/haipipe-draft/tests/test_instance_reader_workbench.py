"""The Insight workbench draws an Insight Block (a task Block with `workbench: insight`) with its
OWN renderer (render_insight_board): instance_reader only reads the Block into the snapshot shape
the workbench already renders, one dataset at a time. Same Spaces, same tables, same columns."""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

from live.insightboard import is_insight_board, render_insight_board
from live.instance_reader import board_kind, legacy_snapshot, render_file, render_run

REF = next(p for p in Path(__file__).resolve().parents if p.name == "skills") / "2_theme" / "insight" / "haipipe-insight" / "ref"
sys.path.insert(0, str(REF))
import run_question as rq  # noqa: E402
import scaffold_block as si  # noqa: E402

SCRIPT = '''
SPEC = "I01"
COLUMNS = ["g"]

def run(df, ctx):
    import pandas as pd
    return {"row_counts.csv": pd.DataFrame([{"partition": ctx.partition, "n_rows": len(df)}])}
'''


@pytest.fixture
def boards(tmp_path):
    (tmp_path / "env.sh").write_text("")
    (tmp_path / "data").mkdir()
    pd.DataFrame({"g": np.random.default_rng(0).choice(["a", "b"], 500)}).to_parquet(tmp_path / "data" / "x.parquet")
    proto = tmp_path / "tasks" / "b52_toy_dikw"
    q = proto / "j02_information" / "t01_row_count"
    (q / "scripts").mkdir(parents=True)
    (proto / "meta").mkdir()
    (proto / "board.md").write_text("---\nboard-kind: task-block\nworkbench: insight\ndatasets:\n  toy: data/x.parquet\n"
                                    "---\n\nToy\n")
    (proto / "meta" / "partitions.md").write_text(textwrap.dedent("""\
        ---
        partitions:
          - {name: full, where: [], plain: every row}
          - {name: alpha, where: [{column: g, eq: a}], plain: group a}
        ---
        """))
    meta = {"id": "I01", "level": "information", "question": "rows per group?", "name": "Rows Per Group",
            "ask": "how many rows are in each group?", "partitions": {"asked": "all"},
            "source": {"cells": {"full": "🟡 I01-full", "alpha": "🚫 full-only"}},
            "needs": {"E1": {"kind": "compute", "what": "the row count", "pass": "a count", "cut": "the cell's partition",
                             "unit": "one row", "measure": "row count", "by": "group", "uncertainty": "none",
                             "rivals": "none", "output": {"row_counts.csv": ["partition", "n_rows"]}},
                      "E2": {"kind": "compute", "what": "an older count", "retired": "two units in one need"}},
            "agreed": "✅ 261002"}
    (q / "question.md").write_text("---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True)
                                   + "---\n\nRows Per Group\n==============\n\n**Why now**: a toy reason.\n\n"
                                   "**What would answer it**: a count per group.\n\n"
                                   "**What we expect to lose here**: nothing.\n")
    (proto / "meta" / "meta.md").write_text("# What the toy extract holds\n\n## Opening\n\nOne toy extract.\n")
    (proto / "j02_information" / "level.md").write_text("# What we ask of patterns\n\n## Opening\n\nA register.\n")
    (q / "scripts" / "row_count.py").write_text(SCRIPT)
    inst = proto
    si.scaffold(inst)
    for part in ("full", "alpha"):
        rq.run(q, f"toy_{part}")
    return tmp_path, proto, inst


def test_the_new_boards_are_insight_boards(boards):
    _, proto, inst = boards
    assert is_insight_board(inst)
    assert board_kind(inst) == "insight-block"


def test_the_same_renderer_draws_the_instance(boards):
    root, _, inst = boards
    snap = legacy_snapshot(inst, root)
    assert [q["id"] for q in snap["questions"]] == ["QI1"]
    assert set(snap["questions"][0]["cells"]) == {"full", "alpha"}
    page = render_insight_board(snap, "insight", "QI1", "alpha")
    for part in ('data-space="scope"', 'data-space="insight"', 'data-space="check"', 'data-space="delivery"',
                 "Logic · the question", "Work · the runs", "Report · what it says", "Task Work", "Alpha"):
        assert part in page, part
    assert "row_counts.csv" in page and "t01_row_count" in page
    for space in ("scope", "check", "delivery"):
        assert render_insight_board(snap, space)
    from live.insightboard import report
    rep = report(snap, "QI1", "alpha")                   # the Report cell reads reports/<dataset>_<partition>/
    assert rep and rep["source"] == "report" and rep["url"].endswith("call=toy_alpha")


def test_the_run_and_file_pop_outs(boards):
    root, _, inst = boards
    run = render_run(inst, root, "j02_information/t01_row_count", "toy_alpha")
    assert "<h2>Report</h2>" in run and "Receipt" in run and "row_counts.csv" in run
    assert run.index("<h2>Report</h2>") < run.index("Receipt")          # the report first (JL 261005)
    with pytest.raises(FileNotFoundError):
        render_run(inst, root, "j02_information/t01_row_count", "toy_beta")
    assert render_file(inst, root, "env.sh")[0] == 404
    spec = boards[1] / "j02_information" / "t01_row_count" / "question.md"
    assert render_file(inst, root, spec.relative_to(root).as_posix())[0] == 200


def test_the_logic_cell_shows_the_carried_question(boards):
    root, _, inst = boards
    snap = legacy_snapshot(inst, root)
    assert snap["questions"][0]["question"] == "rows per group?"
    note = snap["notes"]["QI1"]
    assert note["name"] == "Rows Per Group" and note["why"] == "a toy reason."
    assert note["answer"] == "a count per group." and note["expect"] == "nothing."
    assert [n[0] for n in note["needs"]] == ["E1"]
    page = render_insight_board(snap, "insight", "QI1", "alpha")
    assert "Rows per group?" in page and "Rows Per Group" in page and "A toy reason." in page
    meta = snap["by_id"]["MT00"]
    assert meta["rel"] == "meta/meta.md" and "One toy extract." in meta["text"]
    assert "A register." in snap["questions"][0]["register"]["text"]


def test_a_carried_refusal_shows_where_the_question_is_not_asked(boards):
    root, proto, inst = boards
    f = proto / "j02_information" / "t01_row_count" / "question.md"
    f.write_text(f.read_text().replace("asked: all", "asked: [full]\n  not_elsewhere: a property of the extract"))
    snap = legacy_snapshot(inst, root)
    assert snap["questions"][0]["cells"]["alpha"] == {"mark": "🚫", "page": "", "note": "full-only", "raw": "🚫 full-only"}
    from live.insightboard import _work_cell
    assert _work_cell(snap, snap["questions"][0], "alpha", {}) == "<p class=wk-none>—</p>"
    assert "Task Work" in _work_cell(snap, snap["questions"][0], "full", {})
