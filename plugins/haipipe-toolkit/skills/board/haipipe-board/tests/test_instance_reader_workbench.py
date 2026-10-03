"""The Insight workbench draws a Prototype and Instance board with its OWN renderer
(render_insight_board): instance_reader only reads the new layout into the snapshot
shape the workbench already renders. Same Spaces, same tables, same columns."""

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

REF = Path(__file__).resolve().parents[3] / "insight" / "haipipe-insight" / "ref"
sys.path.insert(0, str(REF))
import run_question as rq  # noqa: E402
import scaffold_instance as si  # noqa: E402

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
    proto = tmp_path / "insights" / "Prototype-Insight-Toy"
    q = proto / "2-Information" / "I01-row-count"
    (q / "scripts").mkdir(parents=True)
    (proto / "0-Meta").mkdir()
    (proto / "board.md").write_text("---\nboard-kind: insight-prototype\n---\n\nToy\n")
    (proto / "0-Meta" / "partitions.md").write_text(textwrap.dedent("""\
        ---
        partitions:
          - {name: full, where: [], plain: every row}
          - {name: alpha, where: [{column: g, eq: a}], plain: group a}
        ---
        """))
    meta = {"id": "I01", "rung": "information", "question": "rows per group?", "name": "Rows Per Group",
            "ask": "how many rows are in each group?", "partitions": {"asked": "all"},
            "source": {"cells": {"full": "🟡 I01-full", "alpha": "🚫 full-only"}},
            "needs": {"E1": {"kind": "compute", "what": "the row count", "pass": "a count", "cut": "the cell's partition",
                             "unit": "one row", "measure": "row count", "by": "group", "uncertainty": "none",
                             "rivals": "none", "output": {"row_counts.csv": ["partition", "n_rows"]}},
                      "E2": {"kind": "compute", "what": "an older count", "retired": "two units in one need"}},
            "agreed": "✅ 261002"}
    (q / "I01-row-count.md").write_text("---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True)
                                        + "---\n\nRows Per Group\n==============\n\n**Why now**: a toy reason.\n\n"
                                        "**What would answer it**: a count per group.\n\n"
                                        "**What we expect to lose here**: nothing.\n")
    (proto / "0-Meta" / "meta.md").write_text("# What the toy extract holds\n\n## Opening\n\nOne toy extract.\n")
    (proto / "2-Information" / "rung.md").write_text("# What we ask of patterns\n\n## Opening\n\nA register.\n")
    (q / "scripts" / "row_count.py").write_text(SCRIPT)
    inst = tmp_path / "insights" / "Instance-Insight-Toy"
    inst.mkdir()
    (inst / "board.md").write_text("---\nboard-kind: insight-instance\nprototype: ../Prototype-Insight-Toy\n"
                                   "extract: data/x.parquet\n---\n\nToy instance\n")
    si.scaffold(inst)
    for part in ("full", "alpha"):
        rq.run(inst / "2-Information" / "I01-row-count", part)
    return tmp_path, proto, inst


def test_the_new_boards_are_insight_boards(boards):
    _, proto, inst = boards
    assert is_insight_board(proto) and is_insight_board(inst)
    assert board_kind(inst) == "insight-instance"


def test_the_same_renderer_draws_the_instance(boards):
    root, _, inst = boards
    snap = legacy_snapshot(inst, root)
    assert [q["id"] for q in snap["questions"]] == ["QI1"]
    assert set(snap["questions"][0]["cells"]) == {"full", "alpha"}
    page = render_insight_board(snap, "insight", "QI1", "alpha")
    for part in ('data-space="scope"', 'data-space="insight"', 'data-space="check"', 'data-space="delivery"',
                 "Logic · the question", "Work · the runs", "Report · what it says", "Task Work", "Alpha"):
        assert part in page, part
    assert "row_counts.csv" in page and "I01-row-count" in page
    for space in ("scope", "check", "delivery"):
        assert render_insight_board(snap, space)


def test_the_run_and_file_pop_outs(boards):
    root, _, inst = boards
    run = render_run(inst, root, "2-Information/I01-row-count", "alpha")
    assert "Receipt" in run and "report.md" in run and "row_counts.csv" in run
    with pytest.raises(FileNotFoundError):
        render_run(inst, root, "2-Information/I01-row-count", "beta")
    assert render_file(inst, root, "env.sh")[0] == 404
    spec = boards[1] / "2-Information" / "I01-row-count" / "I01-row-count.md"
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
    assert meta["rel"] == "0-Meta/meta.md" and "One toy extract." in meta["text"]
    assert "A register." in snap["questions"][0]["register"]["text"]


def test_a_carried_refusal_shows_where_the_question_is_not_asked(boards):
    root, proto, inst = boards
    f = proto / "2-Information" / "I01-row-count" / "I01-row-count.md"
    f.write_text(f.read_text().replace("asked: all", "asked: [full]\n  not_elsewhere: a property of the extract"))
    snap = legacy_snapshot(inst, root)
    assert snap["questions"][0]["cells"]["alpha"] == {"mark": "🚫", "page": "", "note": "full-only", "raw": "🚫 full-only"}
    from live.insightboard import _work_cell
    assert _work_cell(snap, snap["questions"][0], "alpha", {}) == "<p class=wk-none>—</p>"
    assert "Task Work" in _work_cell(snap, snap["questions"][0], "full", {})
