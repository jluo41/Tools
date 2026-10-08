"""run_question, scaffold_block and check_block on a toy Insight Block.

ref/block-contract.md: an Insight Block is a task Block (board-kind: task-block, workbench: insight):
meta/ (partitions, thresholds), one Job per level (j01_data … j04_wisdom), one Task per question
(tNN_<name>/: question.md, scripts/, runs/<dataset>_<partition>.sh, results/, reports/, its page).
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
import check_block as ci  # noqa: E402
import run_question as rq  # noqa: E402
import scaffold_block as si  # noqa: E402

D, DF = "D01", "t01_row_shape"
I, IF = "I01", "t01_rate_by_group"
JOB = {DF: "j01_data", IF: "j02_information", "t02_rate_with_interval": "j02_information",
       "t01_which_group": "j04_wisdom"}
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


def qfile(qid, level, ask, needs, partitions, agreed="✅ 261002", question="the short question", name="Toy"):
    """A question file v2: the register's fields in YAML, why now and what would answer it as prose."""
    meta = {"id": qid, "level": level, "question": question, "name": name, "ask": ask, "partitions": partitions,
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
    proto = root / "tasks" / "b52_toy_dikw"
    for d in ("meta", "j01_data", "j02_information", "j03_knowledge", "j04_wisdom"):
        (proto / d).mkdir(parents=True)
    (proto / "board.md").write_text("---\nboard-kind: task-block\nworkbench: insight\ndatasets:\n  toy: data/x.parquet\n"
                                    "---\n\nToy\n")
    (proto / "meta" / "partitions.md").write_text(textwrap.dedent("""\
        ---
        partitions:
          - {name: full, where: [], plain: every row}
          - {name: alpha, where: [{column: g, eq: a}], plain: group a}
          - {name: cross, of: [alpha], plain: side by side}
        ---
        """))
    (proto / "meta" / "thresholds.yaml").write_text("power:\n  smallest_effect_pp: 5.0\n")
    dq = proto / "j01_data" / DF
    (dq / "scripts").mkdir(parents=True)
    (dq / "question.md").write_text(qfile(D, "data", "how many rows does the extract hold?", {
        "E1": {"kind": "compute", "what": "the row count", "pass": "a count", "cut": "the whole extract",
               "unit": "one row", "measure": "row count", "by": "partition", "uncertainty": "none, a count",
               "rivals": "none", "output": {"row_counts.csv": ["partition", "n_rows"]}}},
        {"asked": ["full"], "not_elsewhere": "it describes the extract"}))
    (dq / "scripts" / "row_shape.py").write_text(SCRIPT_D)
    iq = proto / "j02_information" / IF
    (iq / "scripts").mkdir(parents=True)
    (iq / "question.md").write_text(qfile(I, "information", "does the rate differ by group?", {
        "E1": {"kind": "compute", "what": "the rate per group", "pass": "a rate per group", "cut": "the cell's partition",
               "unit": "one row", "measure": "rate", "by": "g", "uncertainty": "Wilson", "rivals": "none",
               "output": {"rate_by_group.csv": ["group", "n", "rate"]}},
        "E2": {"kind": "cite", "what": "the row count", "from": f"{D}.E1"},
        "E3": {"kind": "compute", "what": "an older table", "pass": "-", "retired": "two units in one need",
               "output": {"old.csv": ["x"]}}},
        {"asked": "all", "power": {"test": "rate_precision", "outcome": "y", "alpha": 0.05, "target_power": 0.8}}))
    (iq / "scripts" / "rate_by_group.py").write_text(SCRIPT_I)
    inst = proto
    return root, proto, inst


def qpath(board_dir, folder):
    return board_dir / JOB[folder] / folder


def run_all(inst):
    si.scaffold(inst)
    out = {}
    for qf in rq.question_folders(inst):
        for t in sorted((qf / "runs").glob("*.sh")):
            out[f"{rq.question_id(qf)}-{t.stem}"] = rq.run(qf, t.stem)["status"]
    return out


def test_runs_land_with_reports_and_provenance(board):
    _, _, inst = board
    assert run_all(inst) == {"D01-toy_full": "ok", "I01-toy_alpha": "ok", "I01-toy_full": "ok"}
    problems, grid, _ = ci.run(inst)
    assert problems == []
    assert grid[I] == {"toy_full": "🟡", "toy_alpha": "🟡", "toy_cross": "—"}
    assert grid[D] == {"toy_full": "🟡", "toy_alpha": "—", "toy_cross": "—"}
    q = qpath(inst, IF)
    assert list(pd.read_csv(q / "results" / "toy_alpha" / "partition_power.csv").columns) == \
        ["partition", "test", "n", "base_rate", "mde", "effect", "answerable"]
    report = (q / "reports" / "toy_alpha" / "report.md").read_text()
    assert "I01.E1" in report and "| group | n | rate |" in report
    assert (q / "results" / "toy_alpha" / "provenance" / "rate_by_group.py").read_text() == SCRIPT_I


def test_a_column_the_spec_does_not_name_fails_the_run(board):
    _, _, inst = board
    si.scaffold(inst)
    (qpath(inst, IF) / "scripts" / "rate_by_group.py").write_text(SCRIPT_I.replace('"rate"]', '"click"]'))
    assert rq.run(qpath(inst, IF), "toy_full")["status"] == "failed"
    problems, _, _ = ci.run(inst)
    assert any("its run failed" in p and "columns" in p for p in problems)


def test_one_row_per_input_row_fails_the_run(board):
    _, _, inst = board
    si.scaffold(inst)
    bad = SCRIPT_I.replace('t = df.groupby("g")["y"].agg(["size", "mean"]).reset_index()', 't = df[["pid", "y", "g"]]')
    (qpath(inst, IF) / "scripts" / "rate_by_group.py").write_text(bad)
    assert rq.run(qpath(inst, IF), "toy_full")["status"] == "failed"


def test_a_script_change_makes_its_runs_stale(board):
    _, _, inst = board
    run_all(inst)
    (qpath(inst, IF) / "scripts" / "rate_by_group.py").write_text(SCRIPT_I + "\n# changed\n")
    problems, grid, _ = ci.run(inst)
    assert grid[I]["toy_full"] == "STALE" and grid[D]["toy_full"] == "🟡" and problems == []


def test_an_underpowered_partition_is_refused_before_any_contrast(board):
    _, proto, inst = board
    (proto / "meta" / "thresholds.yaml").write_text("power:\n  smallest_effect_pp: 0.5\n")
    assert run_all(inst)["I01-toy_alpha"] == "refused"
    _, grid, _ = ci.run(inst)
    assert grid[I]["toy_alpha"].startswith("🚫 underpowered")
    q = qpath(inst, IF)
    assert not (q / "results" / "toy_alpha" / "rate_by_group.csv").exists()
    assert "refused" in (q / "reports" / "toy_alpha" / "report.md").read_text()


def test_a_run_for_an_unasked_partition_is_a_problem(board):
    _, _, inst = board
    run_all(inst)
    (qpath(inst, DF) / "runs" / "toy_cross.sh").write_text(si.TICKET)
    assert any("does not ask D01 on toy_cross" in p for p in ci.run(inst)[0])


def test_question_rules(board):
    _, proto, inst = board
    f = qpath(proto, IF) / "question.md"
    text = f.read_text()
    f.write_text(text.replace("question: the short question\n", "").replace("**Why now**: a toy reason.", ""))
    problems, _, _ = ci.run(inst)
    assert any("no question" in p for p in problems)
    assert any("has no **Why now**" in p for p in problems)
    f.write_text(text)
    f = qpath(proto, DF) / "question.md"
    f.write_text(f.read_text().replace("kind: compute", "kind: judge"))
    assert any("judge need is not legal at level D" in p for p in ci.run(inst)[0])


def test_review_suspects_are_notes_not_problems(board):
    _, proto, inst = board
    f = qpath(proto, IF) / "question.md"
    f.write_text(f.read_text().replace("does the rate differ by group?",
                                       "does the group move the rate, and which group is largest?"))
    problems, _, notes = ci.run(inst)
    assert not any("cause" in p for p in problems)
    assert any("Q4 level" in n for n in notes) and any("Q1 one thing" in n for n in notes)


def test_a_retired_need_is_kept_but_never_run_or_cited(board):
    _, proto, inst = board
    assert run_all(inst)["I01-toy_full"] == "ok"
    assert "old.csv" not in rq.expected_outputs(rq.front(qpath(proto, IF) / "question.md")[0])
    f = qpath(proto, IF) / "question.md"
    f.write_text(f.read_text().replace(f"from: {D}.E1", "from: I01.E3"))
    assert any("not one level below" in p or "is retired" in p for p in ci.run(inst)[0])


def test_json_keys_are_dotted_and_two_needs_may_share_a_json(board):
    _, proto, inst = board
    f = qpath(proto, DF) / "question.md"
    meta, body = rq.front(f)
    meta["needs"]["E2"] = {"kind": "compute", "what": "the shape", "pass": "two counts", "cut": "the whole extract",
                           "unit": "the extract", "measure": "rows", "by": "none", "uncertainty": "none",
                           "rivals": "none", "output": {"metrics.json": ["shape.n_rows"]}}
    meta["needs"]["E3"] = dict(meta["needs"]["E2"], output={"metrics.json": ["min_cell_n"]})
    f.write_text("---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True) + "---\n" + body)
    assert rq.expected_outputs(meta)["metrics.json"] == ["shape.n_rows", "min_cell_n"]
    script = SCRIPT_D.replace("return {", 'return {"metrics.json": {"shape": {"n_rows": len(df)}, "min_cell_n": 100}, ')
    (qpath(proto, DF) / "scripts" / "row_shape.py").write_text(script)
    assert run_all(inst)["D01-toy_full"] == "ok"
    assert "shape.n_rows" in (qpath(inst, DF) / "reports" / "toy_full" / "report.md").read_text()
    (qpath(inst, DF) / "scripts" / "row_shape.py").write_text(script.replace('"min_cell_n": 100', '"floor": 100'))
    assert rq.run(qpath(inst, DF), "toy_full")["status"] == "failed"


def edit(path, change):
    meta, body = rq.front(path)
    change(meta)
    path.write_text("---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True) + "---\n" + body)


def test_a_question_may_override_the_board_wide_effect_only_with_a_reason(board):
    _, proto, inst = board
    f = qpath(proto, IF) / "question.md"
    edit(f, lambda m: m["partitions"]["power"].update(effect=0.5))
    assert any("effect_reason" in p for p in ci.run(inst)[0])
    edit(f, lambda m: m["partitions"]["power"].update(effect_reason="a toy reason"))
    assert not any("effect_reason" in p for p in ci.run(inst)[0])
    assert run_all(inst)["I01-toy_alpha"] == "refused"


def test_a_cite_must_point_one_level_below(board):
    _, proto, inst = board
    f = qpath(proto, IF) / "question.md"
    f.write_text(f.read_text().replace(f"{D}.E1", f"{I}.E1"))
    assert any("not one level below" in p for p in ci.run(inst)[0])


def test_a_run_before_agreement_is_a_problem(board):
    _, proto, inst = board
    f = qpath(proto, DF) / "question.md"
    f.write_text(f.read_text().replace("agreed: ✅ 261002", "agreed: ⬜"))
    run_all(inst)
    assert any("ran before" in p for p in ci.run(inst)[0])


def test_a_question_outside_its_levels_job_is_a_problem(board):
    _, proto, inst = board
    qpath(proto, IF).rename(proto / "j03_knowledge" / IF)
    assert any("is not the letter K" in p for p in ci.run(inst)[0])
    (proto / "j03_knowledge" / IF).rename(proto / "j02_information" / "rate-by-group")
    assert any("holds only tNN_<name>/" in p for p in ci.run(inst)[0])


def test_a_changed_partition_filter_makes_results_stale(board):
    _, proto, inst = board
    run_all(inst)
    t = (proto / "meta" / "partitions.md").read_text()
    (proto / "meta" / "partitions.md").write_text(t.replace("plain: group a", "plain: the a group"))
    assert ci.run(inst)[1][I]["toy_alpha"] == "STALE"


def test_one_checked_page_settles_its_cells_and_status_is_written(board):
    _, _, inst = board
    run_all(inst)
    q = qpath(inst, DF)
    ended = yaml.safe_load((q / "results" / "toy_full" / "runtime.yaml").read_text())["ended"]
    (q / f"{q.name}.md").write_text(
        f"# Rows\n\nfolder-kind: data\nresults-read: {ended}\n\n## Content\n\nThe extract holds 4,000 rows. "
        "<!-- realizes: C1.P1.B1 -->\n")
    (q / "draft").mkdir()
    (q / "draft" / f"{q.name}-evidence-items.md").write_text(
        f"### E01-VALUE-rows · C1.P1.B1 · the row count\n\n- **Need**: {D}.E1\n"
        f"- **Artifact**: `results/toy_full/row_counts.csv` · n_rows\n")
    (q / "runs" / "run-check-1002-page-check.md").write_text(
        "---\nrun: run-check-1002-page-check\nkind: check\nstatus: closed\nclosed_at: 2099-01-01T00:00:00+00:00\n---\n\n"
        "VERDICT: CLOSE\n")
    problems, grid, _ = ci.run(inst)
    assert problems == []
    assert grid[D]["toy_full"] == "✅ 990101"
    ci.main([str(inst), "--write"])
    assert "✅ 990101" in (inst / "meta" / "status.md").read_text()


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
                       "accept": "a rate"} for i, p in enumerate(["toy_full", "toy_alpha"], 1)],
            "divisions": [division("toy_alpha"), division("toy_full")]}
    with pytest.raises(SystemExit, match="one division per run"):
        wp.build(q, spec, "v0.1")
    spec["divisions"] = [division("toy_full"), division("toy_alpha")]
    wp.build(q, spec, "v0.1")
    head = (q / f"{IF}.md").read_text().split("## Opening")[0]
    assert "partitions: toy_full, toy_alpha" in head and "question: I01" in head and "state:" not in head


def test_scaffold_writes_tickets_once_and_names_a_run_no_longer_asked(board):
    _, proto, _ = board
    made, extra = si.scaffold(proto)
    assert sorted(t.name for t in made) == ["toy_alpha.sh", "toy_full.sh", "toy_full.sh"]
    assert si.scaffold(proto) == ([], [])
    (qpath(proto, DF) / "runs" / "toy_alpha.sh").write_text(si.TICKET)
    assert [t.name for t in si.scaffold(proto)[1]] == ["toy_alpha.sh"]


def test_a_run_rests_only_on_the_shared_modules_its_scripts_import(board):
    _, proto, inst = board
    (proto / "src").mkdir()
    (proto / "src" / "helpers.py").write_text("def n(df):\n    return len(df)\n")
    for f in (qpath(proto, IF) / "scripts" / "rate_by_group.py",):
        f.write_text("import helpers  # noqa\n" + f.read_text())
    run_all(inst)
    (proto / "src" / "unrelated.py").write_text("X = 1\n")
    _, grid, _ = ci.run(inst)
    assert grid[D]["toy_full"] == "🟡" and grid[I]["toy_full"] == "🟡"
    (proto / "src" / "helpers.py").write_text("def n(df):\n    return int(len(df))\n")
    _, grid, _ = ci.run(inst)
    assert grid[I]["toy_full"] == "STALE" and grid[D]["toy_full"] == "🟡"


def test_a_retired_question_is_asked_nowhere_and_names_its_successors(board):
    _, proto, inst = board
    run_all(inst)
    f = qpath(proto, IF) / "question.md"
    edit(f, lambda m: m.update(retired="split into two questions"))
    problems, grid, _ = ci.run(inst)
    assert any("names its successors" in p for p in problems)
    assert any("keeps no scripts" in p for p in problems)
    assert any("does not ask I01 on toy_full" in p for p in problems)      # its old tickets are flagged
    edit(f, lambda m: m.update(superseded_by=[]))
    for x in (qpath(proto, IF) / "scripts").glob("*.py"):
        x.unlink()
    import shutil
    for sub in ("runs", "results", "reports"):
        shutil.rmtree(qpath(inst, IF) / sub)
    problems, grid, _ = ci.run(inst)
    assert grid[I] == {"toy_full": "—", "toy_alpha": "—", "toy_cross": "—"}
    assert not any(p.startswith("I01") for p in problems)


def test_a_cross_run_also_reads_the_whole_extract(board):
    _, proto, inst = board
    f = qpath(proto, IF) / "question.md"
    edit(f, lambda m: m["partitions"].update(asked="cross", not_elsewhere="it compares partitions", power="none"))
    (qpath(proto, IF) / "scripts" / "rate_by_group.py").write_text(SCRIPT_I.replace(
        't = df.groupby("g")["y"].agg(["size", "mean"]).reset_index()',
        'assert df is None and set(ctx.partitions) == {"alpha"} and len(ctx.full) == 4000\n'
        '    t = ctx.full.groupby("g")["y"].agg(["size", "mean"]).reset_index()'))
    out = run_all(inst)
    assert out["I01-toy_cross"] == "ok"


def test_a_run_rests_only_on_the_threshold_sections_its_code_names(board):
    _, proto, inst = board
    run_all(inst)
    t = proto / "meta" / "thresholds.yaml"
    t.write_text(t.read_text() + "unrelated:\n  floor: 7\n")
    _, grid, _ = ci.run(inst)
    assert grid[D]["toy_full"] == "🟡" and grid[I]["toy_full"] == "🟡"
    (qpath(proto, IF) / "scripts" / "rate_by_group.py").write_text(SCRIPT_I + '\nKEY = "unrelated"\n')
    run_all(inst)
    t.write_text(t.read_text().replace("floor: 7", "floor: 8"))
    _, grid, _ = ci.run(inst)
    assert grid[I]["toy_full"] == "STALE" and grid[D]["toy_full"] == "🟡"


def test_a_later_level_may_import_an_earlier_levels_module_and_rests_on_it(board):
    _, proto, inst = board
    (proto / "j01_data" / "src").mkdir()
    (proto / "j01_data" / "src" / "data_helpers.py").write_text("def k():\n    return 1\n")
    f = qpath(proto, IF) / "scripts" / "rate_by_group.py"
    f.write_text("import data_helpers  # noqa\n" + f.read_text())
    assert run_all(inst)["I01-toy_full"] == "ok"
    (proto / "j01_data" / "src" / "data_helpers.py").write_text("def k():\n    return 2\n")
    _, grid, _ = ci.run(inst)
    assert grid[I]["toy_full"] == "STALE" and grid[D]["toy_full"] == "🟡"


# ── every DIKW level is a run: figures, an unchanged rerun, a Wisdom test (JL 261005) ──────────────────
SCRIPT_I2 = '''
SPEC = "I02"
COLUMNS = ["g", "y"]

def run(df, ctx):
    import pandas as pd
    rows = []
    for g, s in df.groupby("g"):
        lo, hi = ctx.wilson(int(s["y"].sum()), len(s))
        rows.append({"level": g, "outcome": "y", "n": len(s), "k": int(s["y"].sum()),
                     "rate_pct": 100 * s["y"].mean(), "ci_lo_pct": 100 * lo, "ci_hi_pct": 100 * hi, "suppressed": False})
    return {"rates_by_g.csv": pd.DataFrame(rows)}
'''
SCRIPT_W = '''
SPEC = "W01"
COLUMNS = "none"

def run(df, ctx):
    import pandas as pd
    r = ctx.result("I02", "rates_by_g.csv")
    best = r.loc[r["rate_pct"].idxmax()]
    return {"slate_test.csv": pd.DataFrame([{"pick": best["level"], "lead_pp": r["rate_pct"].max() - r["rate_pct"].min(),
                                             "holds": bool(best["ci_lo_pct"] > r["rate_pct"].drop(best.name).max())}])}
'''
RATES = ["level", "outcome", "n", "k", "rate_pct", "ci_lo_pct", "ci_hi_pct", "suppressed"]


def add_rates_and_wisdom(proto):
    spec = {"pass": "-", "cut": "the cell's partition", "unit": "one row", "measure": "rate", "by": "g",
            "uncertainty": "Wilson", "rivals": "none"}
    iq = proto / "j02_information" / "t02_rate_with_interval"
    (iq / "scripts").mkdir(parents=True)
    (iq / "question.md").write_text(qfile("I02", "information", "how does the rate vary by group?", {
        "E1": {"kind": "compute", "what": "the rate per group with its interval", **spec,
               "output": {"rates_by_g.csv": RATES}}}, {"asked": ["full"], "not_elsewhere": "a toy"}))
    (iq / "scripts" / "rate_with_interval.py").write_text(SCRIPT_I2)
    wq = proto / "j04_wisdom" / "t01_which_group"
    (wq / "scripts").mkdir(parents=True)
    (wq / "question.md").write_text(qfile("W01", "wisdom", "which group should the next round favour, if any?", {
        "E1": {"kind": "compute", "what": "whether the pick holds against the runner-up", **spec, "by": "the pick",
               "output": {"slate_test.csv": ["pick", "lead_pp", "holds"]}}}, {"asked": ["full"], "not_elsewhere": "a toy"}))
    (wq / "scripts" / "which_group.py").write_text(SCRIPT_W)


def test_a_run_draws_figures_and_its_report_leads_with_them(board):
    _, proto, inst = board
    add_rates_and_wisdom(proto)
    run_all(inst)
    q = qpath(inst, "t02_rate_with_interval")
    rec = yaml.safe_load((q / "results" / "toy_full" / "runtime.yaml").read_text())
    assert [f["file"] for f in rec["figures"]] == ["fig_E1_rates_by_g.png"]
    assert (q / "results" / "toy_full" / "fig_E1_rates_by_g.png").stat().st_size > 1000
    report = (q / "reports" / "toy_full" / "report.md").read_text()
    assert "![rates_by_g.csv](../../results/toy_full/fig_E1_rates_by_g.png)" in report
    assert report.index("- y: highest") < report.index("![rates_by_g.csv]") < report.index("**Pass**")


def test_an_unchanged_rerun_keeps_a_check_current(board):
    _, _, inst = board
    run_all(inst)
    q = qpath(inst, DF)
    first = yaml.safe_load((q / "results" / "toy_full" / "runtime.yaml").read_text())
    (q / f"{q.name}.md").write_text(f"# Rows\n\nfolder-kind: data\nresults-read: {first['ended']}\n\n## Content\n\nx\n")
    rq.run(q, "toy_full")
    again = yaml.safe_load((q / "results" / "toy_full" / "runtime.yaml").read_text())
    assert again["content_since"] == first["content_since"] and again["tables_sha256"] == first["tables_sha256"]


def test_a_wisdom_question_is_answered_by_a_run_and_goes_stale_with_what_it_read(board):
    _, proto, inst = board
    add_rates_and_wisdom(proto)
    status = run_all(inst)
    assert status["W01-toy_full"] == "ok", status
    problems, grid, _ = ci.run(inst)
    assert problems == [] and grid["W01"]["toy_full"] == "🟡"
    w = qpath(inst, "t01_which_group")
    rec = yaml.safe_load((w / "results" / "toy_full" / "runtime.yaml").read_text())
    assert list(rec["reads"]) == ["tasks/b52_toy_dikw/j02_information/t02_rate_with_interval/results/toy_full/rates_by_g.csv"]
    i2 = qpath(inst, "t02_rate_with_interval") / "results" / "toy_full" / "rates_by_g.csv"
    i2.write_text(i2.read_text().replace(",y,", ",y ,", 1))          # the lower result changed (a toy edit)
    assert ci.run(inst)[1]["W01"]["toy_full"] == "STALE"


def test_figures_know_the_knowledge_estimate_shape(tmp_path):
    import figures
    gain = pd.DataFrame([{"grouping": "partition", "naive_gain_pp": 0.0, "crossfit_gain_pp": -0.18,
                          "ci_lo_pp": -0.4, "ci_hi_pp": 0.05}])
    assert figures.shape(gain) == "estimate"
    assert figures.lead(gain) == ["crossfit_gain_pp -0.18 (-0.40 to 0.05)"]
    many = pd.DataFrame({"level": list("abcde"), "gap_pp": [1, 2, -3, 0.1, float("nan")],
                         "ci_lo_pp": [0.5, -1, -4, -1, float("nan")], "ci_hi_pp": [2, 3, -2, 1, float("nan")]})
    assert figures.lead(many) == ["gap_pp: 2 of 4 intervals exclude zero", "1 rows not readable or not estimable, left out"]
    figures.KINDS["estimate"][0](many, tmp_path / "f.png", "t")
    assert (tmp_path / "f.png").stat().st_size > 1000
    assert figures.shape(pd.DataFrame({"x": [1], "y": [2]})) == ""
