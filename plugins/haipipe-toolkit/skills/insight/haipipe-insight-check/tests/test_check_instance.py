"""run_question, scaffold_instance, sync_instance and check_instance on a toy Prototype and Instance.

ref/prototype-contract.md: the Instance mirrors the Prototype (0-Meta, 1-Data … 4-Wisdom); each
question folder holds a tracked copy of the Prototype's scripts/, one run per partition, its
results/ and generated reports/, and one page for the question.
"""
import sys
import textwrap
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "ref"))
sys.path.insert(0, str(HERE.parents[2] / "haipipe-insight" / "ref"))
import check_instance as ci  # noqa: E402
import run_question as rq  # noqa: E402
import scaffold_instance as si  # noqa: E402
import sync_instance as sy  # noqa: E402

D, DF = "D01", "D01-row-shape"
I, IF = "I01", "I01-rate-by-group"
SCRIPT_D = f'''
SPEC = "{D}"
COLUMNS = ["g"]

def run(df, ctx):
    import pandas as pd
    return {{"row_counts.csv": pd.DataFrame([{{"partition": ctx.partition, "n_rows": len(df)}}])}}
'''
SCRIPT_I = f'''
SPEC = "{I}"
COLUMNS = ["g", "y", "pid"]

def run(df, ctx):
    import pandas as pd
    t = df.groupby("g")["y"].agg(["size", "mean"]).reset_index()
    t.columns = ["group", "n", "rate"]
    return {{"rate_by_group.csv": t}}
'''


def qfile(qid, rung, ask, needs, partitions, agreed="✅ 261002", question="the short question", name="Toy"):
    """A question file v2: the register's fields in YAML, why now and what would answer it as prose."""
    meta = {"id": qid, "rung": rung, "question": question, "name": name, "ask": ask, "partitions": partitions,
            "needs": needs, "agreed": agreed}
    return ("---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True) + "---\n\n"
            f"{name}\n{'=' * len(name)}\n\n**Why now**: a toy reason.\n\n**What would answer it**: a toy answer.\n")


@pytest.fixture
def board(tmp_path):
    root = tmp_path
    (root / "env.sh").write_text("")
    rng = np.random.default_rng(0)
    n = 4000
    df = pd.DataFrame({"g": rng.choice(["a", "b"], n), "y": rng.integers(0, 2, n), "pid": np.arange(n)})
    (root / "data").mkdir()
    df.to_parquet(root / "data" / "x.parquet")
    proto = root / "insights" / "Prototype-Insight-Toy"
    for d in ("0-Meta", "1-Data", "2-Information", "3-Knowledge", "4-Wisdom"):
        (proto / d).mkdir(parents=True)
    (proto / "board.md").write_text("---\nboard-kind: insight-prototype\n---\n\nToy\n")
    (proto / "0-Meta" / "partitions.md").write_text(textwrap.dedent("""\
        ---
        partitions:
          - {name: full, where: [], plain: every row}
          - {name: alpha, where: [{column: g, eq: a}], plain: group a}
          - {name: cross, of: [alpha], plain: side by side}
        ---
        """))
    (proto / "0-Meta" / "thresholds.yaml").write_text("power:\n  smallest_effect_pp: 5.0\n")
    dq = proto / "1-Data" / DF
    (dq / "scripts").mkdir(parents=True)
    (dq / f"{DF}.md").write_text(qfile(D, "data", "how many rows does the extract hold?", {
        "E1": {"kind": "compute", "what": "the row count", "pass": "a count", "cut": "the whole extract",
               "unit": "one row", "measure": "row count", "by": "partition", "uncertainty": "none, a count",
               "rivals": "none", "output": {"row_counts.csv": ["partition", "n_rows"]}}},
        {"asked": ["full"], "not_elsewhere": "it describes the extract"}))
    (dq / "scripts" / "row_shape.py").write_text(SCRIPT_D)
    iq = proto / "2-Information" / IF
    (iq / "scripts").mkdir(parents=True)
    (iq / f"{IF}.md").write_text(qfile(I, "information", "does the rate differ by group?", {
        "E1": {"kind": "compute", "what": "the rate per group", "pass": "a rate per group", "cut": "the cell's partition",
               "unit": "one row", "measure": "rate", "by": "g", "uncertainty": "Wilson", "rivals": "none",
               "output": {"rate_by_group.csv": ["group", "n", "rate"]}},
        "E2": {"kind": "cite", "what": "the row count", "from": f"{D}.E1"},
        "E3": {"kind": "compute", "what": "an older table", "pass": "-", "retired": "two units in one need",
               "output": {"old.csv": ["x"]}}},
        {"asked": "all", "power": {"test": "rate_precision", "outcome": "y", "alpha": 0.05, "target_power": 0.8}}))
    (iq / "scripts" / "rate_by_group.py").write_text(SCRIPT_I)
    inst = root / "insights" / "Instance-Insight-Toy"
    inst.mkdir()
    (inst / "board.md").write_text("---\nboard-kind: insight-instance\nprototype: ../Prototype-Insight-Toy\n"
                                   "extract: data/x.parquet\n---\n\nToy instance\n")
    return root, proto, inst


def qpath(board_dir, folder):
    return board_dir / rq.RUNG_DIR[folder[0]] / folder


def run_all(inst):
    si.scaffold(inst)
    out = {}
    for qf in rq.question_folders(inst):
        for t in sorted((qf / "runs").glob("*.sh")):
            out[f"{qf.name[:3]}-{t.stem}"] = rq.run(qf, t.stem)["status"]
    return out


def test_runs_land_with_reports_and_provenance(board):
    _, _, inst = board
    assert run_all(inst) == {"D01-full": "ok", "I01-alpha": "ok", "I01-full": "ok"}
    problems, grid, _ = ci.run(inst)
    assert problems == []
    assert grid[I] == {"full": "🟡", "alpha": "🟡", "cross": "—"}
    assert grid[D] == {"full": "🟡", "alpha": "—", "cross": "—"}
    q = qpath(inst, IF)
    assert list(pd.read_csv(q / "results" / "alpha" / "partition_power.csv").columns) == \
        ["partition", "test", "n", "base_rate", "mde", "effect", "answerable"]
    report = (q / "reports" / "alpha" / "report.md").read_text()
    assert "I01.E1" in report and "| group | n | rate |" in report
    assert (q / "results" / "alpha" / "provenance" / "rate_by_group.py").read_text() == SCRIPT_I
    assert (q / "scripts" / "prototype.lock").is_file()


def test_a_column_the_spec_does_not_name_fails_the_run(board):
    _, _, inst = board
    si.scaffold(inst)
    (qpath(inst, IF) / "scripts" / "rate_by_group.py").write_text(SCRIPT_I.replace('"rate"]', '"click"]'))
    assert rq.run(qpath(inst, IF), "full")["status"] == "failed"
    problems, _, _ = ci.run(inst)
    assert any("its run failed" in p and "columns" in p for p in problems)


def test_one_row_per_input_row_fails_the_run(board):
    _, _, inst = board
    si.scaffold(inst)
    bad = SCRIPT_I.replace('t = df.groupby("g")["y"].agg(["size", "mean"]).reset_index()', 't = df[["pid", "y", "g"]]')
    (qpath(inst, IF) / "scripts" / "rate_by_group.py").write_text(bad)
    assert rq.run(qpath(inst, IF), "full")["status"] == "failed"


def test_a_local_change_is_stale_flagged_and_must_be_reviewed(board):
    _, _, inst = board
    run_all(inst)
    (qpath(inst, IF) / "scripts" / "rate_by_group.py").write_text(SCRIPT_I + "\n# adapted here\n")
    problems, grid, _ = ci.run(inst)
    assert grid[I]["full"] == "STALE ⚑"
    assert any("changed in the Instance and not reviewed" in p for p in problems)
    sy.main([str(inst), "--question", I, "--reviewed", "rate_by_group.py"])
    problems, _, _ = ci.run(inst)
    assert not any("not reviewed" in p for p in problems)
    assert [s for _, n, s, r in sy.status(inst) if n == "rate_by_group.py"] == ["instance changed"]


def test_a_prototype_update_waits_then_pull_makes_it_stale(board):
    _, proto, inst = board
    run_all(inst)
    (qpath(proto, IF) / "scripts" / "rate_by_group.py").write_text(SCRIPT_I + "\n# improved upstream\n")
    problems, grid, notes = ci.run(inst)
    assert grid[I]["full"] == "🟡 ⚑" and problems == []
    assert any("prototype changed" in n for n in notes)
    assert any("update waiting" in p for p in ci.run(inst, strict=True)[0])
    sy.main([str(inst), "--pull"])
    _, grid, notes = ci.run(inst)
    assert grid[I]["full"] == "STALE" and not notes


def test_a_change_in_both_boards_is_a_conflict(board):
    _, proto, inst = board
    run_all(inst)
    (qpath(proto, IF) / "scripts" / "rate_by_group.py").write_text(SCRIPT_I + "\n# upstream\n")
    (qpath(inst, IF) / "scripts" / "rate_by_group.py").write_text(SCRIPT_I + "\n# local\n")
    assert any("changed in both boards" in p for p in ci.run(inst)[0])


def test_an_underpowered_partition_is_refused_before_any_contrast(board):
    _, proto, inst = board
    (proto / "0-Meta" / "thresholds.yaml").write_text("power:\n  smallest_effect_pp: 0.5\n")
    assert run_all(inst)["I01-alpha"] == "refused"
    _, grid, _ = ci.run(inst)
    assert grid[I]["alpha"].startswith("🚫 underpowered")
    q = qpath(inst, IF)
    assert not (q / "results" / "alpha" / "rate_by_group.csv").exists()
    assert "refused" in (q / "reports" / "alpha" / "report.md").read_text()


def test_a_run_for_an_unasked_partition_is_a_problem(board):
    _, _, inst = board
    run_all(inst)
    (qpath(inst, DF) / "runs" / "cross.sh").write_text(si.TICKET)
    assert any("does not ask D01 on cross" in p for p in ci.run(inst)[0])


def test_question_rules(board):
    _, proto, inst = board
    f = qpath(proto, IF) / f"{IF}.md"
    text = f.read_text()
    f.write_text(text.replace("question: the short question\n", "").replace("**Why now**: a toy reason.", ""))
    problems, _, _ = ci.run(inst)
    assert any("no question" in p for p in problems)
    assert any("has no **Why now**" in p for p in problems)
    f.write_text(text)
    f = qpath(proto, DF) / f"{DF}.md"
    f.write_text(f.read_text().replace("kind: compute", "kind: judge"))
    assert any("judge need is not legal at rung D" in p for p in ci.run(inst)[0])


def test_review_suspects_are_notes_not_problems(board):
    _, proto, inst = board
    f = qpath(proto, IF) / f"{IF}.md"
    f.write_text(f.read_text().replace("does the rate differ by group?",
                                       "does the group move the rate, and which group is largest?"))
    problems, _, notes = ci.run(inst)
    assert not any("cause" in p for p in problems)
    assert any("Q4 rung" in n for n in notes) and any("Q1 one thing" in n for n in notes)


def test_a_retired_need_is_kept_but_never_run_or_cited(board):
    _, proto, inst = board
    assert run_all(inst)["I01-full"] == "ok"
    assert "old.csv" not in rq.expected_outputs(rq.front(qpath(proto, IF) / f"{IF}.md")[0])
    f = qpath(proto, IF) / f"{IF}.md"
    f.write_text(f.read_text().replace(f"from: {D}.E1", "from: I01.E3"))
    assert any("not one rung below" in p or "is retired" in p for p in ci.run(inst)[0])


def test_json_keys_are_dotted_and_two_needs_may_share_a_json(board):
    _, proto, inst = board
    f = qpath(proto, DF) / f"{DF}.md"
    meta, body = rq.front(f)
    meta["needs"]["E2"] = {"kind": "compute", "what": "the shape", "pass": "two counts", "cut": "the whole extract",
                           "unit": "the extract", "measure": "rows", "by": "none", "uncertainty": "none",
                           "rivals": "none", "output": {"metrics.json": ["shape.n_rows"]}}
    meta["needs"]["E3"] = dict(meta["needs"]["E2"], output={"metrics.json": ["min_cell_n"]})
    f.write_text("---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True) + "---\n" + body)
    assert rq.expected_outputs(meta)["metrics.json"] == ["shape.n_rows", "min_cell_n"]
    script = SCRIPT_D.replace("return {", 'return {"metrics.json": {"shape": {"n_rows": len(df)}, "min_cell_n": 100}, ')
    (qpath(proto, DF) / "scripts" / "row_shape.py").write_text(script)
    assert run_all(inst)["D01-full"] == "ok"
    assert "shape.n_rows" in (qpath(inst, DF) / "reports" / "full" / "report.md").read_text()
    (qpath(inst, DF) / "scripts" / "row_shape.py").write_text(script.replace('"min_cell_n": 100', '"floor": 100'))
    assert rq.run(qpath(inst, DF), "full")["status"] == "failed"


def edit(path, change):
    meta, body = rq.front(path)
    change(meta)
    path.write_text("---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True) + "---\n" + body)


def test_a_question_may_override_the_board_wide_effect_only_with_a_reason(board):
    _, proto, inst = board
    f = qpath(proto, IF) / f"{IF}.md"
    edit(f, lambda m: m["partitions"]["power"].update(effect=0.5))
    assert any("effect_reason" in p for p in ci.run(inst)[0])
    edit(f, lambda m: m["partitions"]["power"].update(effect_reason="a toy reason"))
    assert not any("effect_reason" in p for p in ci.run(inst)[0])
    assert run_all(inst)["I01-alpha"] == "refused"


def test_a_cite_must_point_one_rung_below(board):
    _, proto, inst = board
    f = qpath(proto, IF) / f"{IF}.md"
    f.write_text(f.read_text().replace(f"{D}.E1", f"{I}.E1"))
    assert any("not one rung below" in p for p in ci.run(inst)[0])


def test_a_run_before_agreement_is_a_problem(board):
    _, proto, inst = board
    f = qpath(proto, DF) / f"{DF}.md"
    f.write_text(f.read_text().replace("agreed: ✅ 261002", "agreed: ⬜"))
    run_all(inst)
    assert any("ran before" in p for p in ci.run(inst)[0])


def test_a_question_outside_its_rung_folder_is_a_problem(board):
    _, proto, inst = board
    qpath(proto, IF).rename(proto / "3-Knowledge" / IF)
    assert any("in the rung folder of its letter" in p for p in ci.run(inst)[0])


def test_a_changed_partition_filter_makes_results_stale(board):
    _, proto, inst = board
    run_all(inst)
    t = (proto / "0-Meta" / "partitions.md").read_text()
    (proto / "0-Meta" / "partitions.md").write_text(t.replace("plain: group a", "plain: the a group"))
    assert ci.run(inst)[1][I]["alpha"] == "STALE"


def test_one_checked_page_settles_its_cells_and_status_is_written(board):
    _, _, inst = board
    run_all(inst)
    q = qpath(inst, DF)
    ended = yaml.safe_load((q / "results" / "full" / "runtime.yaml").read_text())["ended"]
    (q / f"{q.name}.md").write_text(
        f"# Rows\n\nfolder-kind: data\nresults-read: {ended}\n\n## Content\n\nThe extract holds 4,000 rows. "
        "<!-- realizes: C1.P1.B1 -->\n")
    (q / "draft").mkdir()
    (q / "draft" / f"{q.name}-evidence-items.md").write_text(
        f"### E01-VALUE-rows · C1.P1.B1 · the row count\n\n- **Need**: {D}.E1\n"
        f"- **Artifact**: `results/full/row_counts.csv` · n_rows\n")
    (q / "runs" / "run-check-1002-page-check.md").write_text(
        "---\nrun: run-check-1002-page-check\nkind: check\nstatus: closed\nclosed_at: 2099-01-01T00:00:00+00:00\n---\n\n"
        "VERDICT: CLOSE\n")
    problems, grid, _ = ci.run(inst)
    assert problems == []
    assert grid[D]["full"] == "✅ 990101"
    ci.main([str(inst), "--write"])
    assert "✅ 990101" in (inst / "0-Meta" / "status.md").read_text()


def test_an_instance_page_has_one_division_per_partition(board):
    import write_answer_page as wp
    _, _, inst = board
    run_all(inst)
    q = qpath(inst, IF)

    def division(part):
        return {"title": f"In {part}", "map": "the rate", "diagram": "rate", "partition": part,
                "paragraphs": [{"label": "Rate", "job": "state it", "bullets": [
                    {"role": "Claim", "point": "the rate per group", "note": "n", "item": f"E01-VALUE-{part}",
                     "accept": "a rate", "draft": "The rate is read per group."}]}]}
    spec = {"title": "Rate by group", "folder-kind": "information", "arc": "one rate per partition",
            "opening": ["The rate per group."], "sits": "toy", "matters": "toy",
            "items": [{"id": f"E01-VALUE-{p}", "target": f"C{i}.P1.B1", "name": "rate", "need": f"{I}.E1",
                       "partition": p, "file": "rate_by_group.csv", "columns": "rate", "expected": "a rate",
                       "accept": "a rate"} for i, p in enumerate(["full", "alpha"], 1)],
            "divisions": [division("alpha"), division("full")]}
    with pytest.raises(SystemExit, match="one division per partition"):
        wp.build(q, spec, "v0.1")
    spec["divisions"] = [division("full"), division("alpha")]
    wp.build(q, spec, "v0.1")
    head = (q / f"{IF}.md").read_text().split("## Opening")[0]
    assert "partitions: full, alpha" in head and "state:" not in head


def test_scaffold_writes_a_new_instance_board(board):
    root, proto, _ = board
    new = root / "insights" / "Instance-Insight-New"
    si.scaffold(new, prototype=proto, extract="data/x.parquet")
    meta = rq.front(new / "board.md")[0]
    assert meta == {"board-kind": "insight-instance", "prototype": "../Prototype-Insight-Toy", "extract": "data/x.parquet"}
    assert (new / "2-Information" / IF / "runs" / "alpha.sh").is_file()
    assert rq.run(new / "2-Information" / IF, "full")["status"] == "ok"
