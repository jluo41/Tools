"""Work progress reads real sources without granting acceptance or changing records."""
import html
import re
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest
import yaml

from live import frame, work_progress
from live.frame_view import FrameMixin


@pytest.fixture
def board(tmp_path):
    block = tmp_path / "Project/work/b51_topic"
    job = block / "j01_tables"
    task = job / "t01_answers"
    task.mkdir(parents=True)
    (block / "board.md").write_text("# Tables\nboard-kind: task-block\nworkbench-layout: workflow\nspine: Reusable answers\nclose: Checked output\n")
    (job / "j01_tables.md").write_text("# Tables\ngoal: Build the table\nclose: Validate it\n")
    (task / "t01_answers.md").write_text("# Answers\nfolder-kind: task\ntask-type: data\ndevelops: Freeze answers\ninput: Requests\noutput: Table\n")
    return tmp_path, block, job, task


def run(task, name="r01_compare", **updates):
    folder = task / "runs" / name
    (folder / "result").mkdir(parents=True)
    (folder / (name + ".sh")).write_text("#!/bin/sh\ntrue\n")
    (folder / "run.yaml").write_text(yaml.safe_dump(dict(run=name, kind="hard", type=["asset-parity"], status="complete", passes=["p01", "p02"])))
    receipt = dict(run=name, status="complete", started_at="2026-09-29T23:57:50-04:00",
                   finished_at="2026-09-29T23:59:36-04:00", headline="12 requests agree", exit_code=0)
    receipt.update(updates)
    (folder / "result/runtime.yaml").write_text(yaml.safe_dump(receipt))
    (folder / "result/metrics.json").write_text('{"compared":12}')
    return folder


def test_opt_in_is_block_scoped_and_draft_keeps_its_layout(board):
    root, block, job, task = board
    run(task)
    theme = frame.themes()["work"]
    for level, folder in (("Block", block), ("Job", job), ("Task", task)):
        views = frame.spaces_for(theme, level, folder, root, "Execution")
        for mode in work_progress.MODES:
            assert views[mode].subspaces == work_progress.VIEWS
            assert views[mode].open == "Execution"
    face = task / "t01_answers.md"
    face.write_text(face.read_text().replace("task-type: data", "task-type: draft"))
    from live.task_draft import DRAFT_TASK_SUBS
    views = frame.spaces_for(theme, "Task", task, root)
    assert views["Work Details"].subspaces == DRAFT_TASK_SUBS["Work Details"]
    assert "Execution" not in views["Work Details"].subspaces
    (block / "board.md").write_text("# Tables\nboard-kind: task-block\n")
    assert not work_progress.enabled(task, root)


def test_goal_counts_runs_not_passes_or_soft_work_and_never_grants_acceptance(board):
    root, block, job, task = board
    run(task)
    soft = task / "runs/run-report-table"
    soft.mkdir()
    (soft / "run.yaml").write_text("run: run-report-table\nkind: soft\nstatus: complete\n")
    rows = work_progress.records(task)
    assert len(rows) == 1
    content = work_progress.goal_view("Task", task, root, {task: rows}, "Audience Report")
    assert "Freeze answers" in content
    assert "<b>📊 1 Run</b>" in content                                  # the hard Run only, never the soft one
    assert "Goal accepted by a person: not recorded" in content
    assert "100%" not in content


def test_plan_distinguishes_saved_work_from_run_history(board):
    root, block, job, task = board
    run(task)
    data = {task: work_progress.records(task)}
    content = work_progress.plan_view("Task", task, root, data, "Audience Report")
    assert "No workflow/plan.yaml saved" in content and "not an execution order" in content
    (task / "workflow").mkdir()
    (task / "workflow/plan.yaml").write_text(yaml.safe_dump({
        "run_specs": [{"id": "validate", "purpose": "Check the promised fields", "input": ["table.csv"],
                       "depends_on": ["build"], "exit_gate": {"assertion": "All fields valid"},
                       "result": {"receipt": "runs/r02/result/runtime.yaml"}}]}))
    content = work_progress.plan_view("Task", task, root, data, "Audience Report")
    assert "Check the promised fields" in content and "All fields valid" in content
    assert "No workflow/plan.yaml saved" not in content


def test_run_detail_uses_exact_receipt_and_rejects_other_runs(board):
    root, block, job, task = board
    run(task, headline="<script>bad()</script>")
    run(task, "r02_compare", headline="Different version", host="test-worker")
    content = work_progress.render_run(task, root, "r01_compare")
    assert "1 min 46 s" in content
    assert "Execution location</td><td>Not recorded" in content
    assert "b51_topic / j01_tables / t01_answers / r01_compare" in content
    assert "Different version" not in content
    assert "&lt;script&gt;bad()" in content
    assert "<script>bad()" not in content
    assert work_progress.render_run(task, root, "../r02_compare") is None


def test_missing_or_invalid_times_are_not_fabricated():
    assert work_progress.elapsed({}) == "Not recorded"
    assert work_progress.elapsed({"started_at": "bad", "finished_at": "bad"}) == "Not recorded"
    assert work_progress.elapsed({"started_at": "2026-10-20", "finished_at": "2026-10-19"}) == "Conflicting timestamps"


def test_switching_report_work_keeps_subview(board):
    root, block, job, task = board
    run(task)
    theme = frame.themes()["work"]
    for mode, other in (("Audience Report", "Work Details"), ("Work Details", "Audience Report")):
        doc = frame.render(theme, root, task, mode, "Execution")
        navigation = re.search(r'<nav class="row spaces">(.*?)</nav>', doc).group(1)
        urls = [parse_qs(urlparse(html.unescape(url)).query) for url in re.findall(r'href="([^"]+)"', navigation)]
        assert any(q.get("space") == [other] and q.get("sub") == ["Execution"] for q in urls)
        assert any(q.get("space") == ["Runs"] and "sub" not in q for q in urls)


def test_reads_updated_receipt_without_writing_sources(board):
    root, block, job, task = board
    folder = run(task)
    before = {p: p.read_bytes() for p in block.rglob("*") if p.is_file()}
    data = work_progress.snapshot("Block", block)
    assert data[task][0]["status"] == "complete"
    work_progress.spaces("Task", task, root, "Goal", frame.themes()["work"])
    assert before == {p: p.read_bytes() for p in block.rglob("*") if p.is_file()}
    receipt = folder / "result/runtime.yaml"
    receipt.write_text(receipt.read_text().replace("status: complete", "status: failed"))
    assert work_progress.snapshot("Task", task)[task][0]["status"] == "failed"


def test_exact_run_http_route_is_confined_to_opted_in_tasks(board):
    root, block, job, task = board
    run(task)

    class Handler(FrameMixin):
        def guide_send(self, body, status, *args, **kwargs):
            return status, body

    handler = Handler()
    handler.root = root
    handler.path = frame.ROUTE + "?view=work-run&path=" + task.relative_to(root).as_posix() + "&run=r01_compare"
    status, body = handler.workbench_frame_view()
    assert status == 200 and "1 min 46 s" in body
    handler.path = handler.path.replace("r01_compare", "../../board.md")
    assert handler.workbench_frame_view()[0] == 404
    handler.path = frame.ROUTE + "?view=work-run&path=../outside&run=r01_compare"
    assert handler.workbench_frame_view()[0] == 404



def test_goal_is_a_checklist_ticked_from_disk(board):
    """JL 261020: "like the TODO list ... Large TODO items, and small TODO items, and the final check list": the
    Block's deliverables, then one large item per Job whose small items tick only when the files and the Run are there."""
    root, block, job, task = board
    run(task)
    (task / "runs/r01_compare/result/table.csv").write_text("a\n1\n")
    (block / "board.md").write_text((block / "board.md").read_text() + (
        "\n## Deliverables\n\n```yaml\ndeliverables:\n- what: \"The table, checked\"\n  kind: data\n"
        "  files: j01_tables/t01_answers/runs/r01_compare/result/table.csv\n- what: \"The report\"\n  files: report.md\n```\n"))
    (job / "j01_tables.md").write_text((job / "j01_tables.md").read_text() + (
        "\n## Deliverables\n\n```yaml\ndeliverables:\n- what: \"Answers table\"\n  kind: data\n"
        "  files: t01_answers/runs/r01_compare/result/*.csv\n  run: t01_answers/r01_compare\n"
        "- what: \"Second fold\"\n  files: t01_answers/runs/r01_compare/result/fold*.csv\n  count: 2\n```\n"))
    data = work_progress.snapshot("Block", block)
    content = work_progress.goal_cards("Block", block, root, data, "Audience Report")
    text = re.sub(r"<[^>]+>", "", content)
    assert content.count('<ul class=dtree>') == 1                           # one tree, never two lists
    assert text.index("j01_tables") < text.index("t01_answers") < text.index("Answers table") < text.index("Across all Jobs")
    assert "✅ Answers table" in text and "☐ The reporttodo" in text and "✅ The table, checked" in text
    assert "j01_tables🔶 1 of 2" in text                                    # the Run finished; no fold file yet
    assert "12 requests agree" in text                                      # the Run's key result beside its item
    assert "2 of 4 delivered" in text and "Goal accepted by a person: not recorded" in text
    job_view = re.sub(r"<[^>]+>", "", work_progress.goal_cards("Job", job, root, work_progress.snapshot("Job", job), "Audience Report"))
    assert "t01_answers✅ 1 of 1" in job_view and "☐ Second fold" in job_view


def test_a_tasks_runs_group_by_role(board):
    """JL 261020: "一个 task 可能有很多 run ... 各司其职": a Task's Runs read as groups, each role named once."""
    root, block, job, task = board
    for name, role in (("r03_figures_counts", "figures"), ("r01_smoke", "trial"), ("r02_full", "make"), ("r04_full_retry", "fix")):
        folder = run(task, name)
        card = yaml.safe_load((folder / "run.yaml").read_text())
        (folder / "run.yaml").write_text(yaml.safe_dump(dict(card, role=role)))
    content = work_progress.run_rows(work_progress.records(task), root)
    order = [content.index(w) for w in ("🧪&nbsp;trial", "🔨&nbsp;make", "🔁&nbsp;retry&nbsp;or&nbsp;fix", "📊&nbsp;figures")]
    assert order == sorted(order)                                            # the order a Task lives, not the run numbers
    assert content.index("r01_smoke") < content.index("r02_full") < content.index("r04_full_retry") < content.index("r03_figures_counts")


def test_the_tree_folds_and_each_item_says_where_its_data_is(board):
    """JL 261020: "could I collapse them" and "show me where is the data to put"."""
    root, block, job, task = board
    run(task)
    (task / "runs/r01_compare/result/table.csv").write_text("a\n1\n")
    (job / "j01_tables.md").write_text((job / "j01_tables.md").read_text() + (
        "\n## Deliverables\n\n```yaml\ndeliverables:\n- what: \"Answers table\"\n"
        "  files: t01_answers/runs/r01_compare/result/*.csv\n  run: t01_answers/r01_compare\n  used_by:\n  - \"b02 j01\"\n```\n"))
    content = work_progress.goal_cards("Block", block, root, work_progress.snapshot("Block", block), "Audience Report")
    assert '<details class=branch data-work-key="tree-Project/work/b51_topic/j01_tables">' in content   # folded at first (JL 261021)
    assert " open " not in content.replace("Open all", "")
    assert "<details class=leaf data-work-key=" in content                  # an item opens on click, folded at first
    assert "📁 <code>runs/r01_compare/result/</code>" in content              # said from its Task (JL 261021)
    assert "table.csv" in content and "<h5>Read by</h5><div>b02 j01</div>" in content and "▸ Fold all" in content
    assert "<h5>Made by</h5>" in content and "r01_compare" in content and "✅ finished" in content   # the Run, with its mark


def test_what_an_item_is_reads_first_as_bullets(board):
    """JL 261021: "make this part a little big"; "这里可以用 bullet points 吗"."""
    root, block, job, task = board
    run(task)
    (task / "runs/r01_compare/result/table.csv").write_text("a\n1\n")
    (job / "j01_tables.md").write_text((job / "j01_tables.md").read_text() + (
        "\n## Deliverables\n\n```yaml\ndeliverables:\n- what: \"Answers table\"\n  means:\n  - \"Step two of two.\"\n"
        "  - \"One row per answer.\"\n  files: t01_answers/runs/r01_compare/result/*.csv\n  run: t01_answers/r01_compare\n"
        "- what: \"Old table\"\n  means: \"One sentence.\"\n  files: t01_answers/runs/r01_compare/result/*.csv\n```\n"))
    content = work_progress.goal_cards("Block", block, root, work_progress.snapshot("Block", block), "Audience Report")
    assert '<h5>What it is</h5><ul class="means lead"><li>Step two of two.</li><li>One row per answer.</li></ul>' in content
    assert '<h5>What it is</h5><div class="means lead">One sentence.</div>' in content   # a sentence stays one line


def test_a_run_that_checked_an_item_is_not_its_maker(board):
    """JL 261021: "why this is still the r01? for the rebuilt": a Run that rebuilt and compared stored files checks
    them; it is listed under Checked by, never Made by, and still has to finish for the tick."""
    root, block, job, task = board
    run(task)
    (job / "store.csv").write_text("a\n1\n")
    (job / "j01_tables.md").write_text((job / "j01_tables.md").read_text() + (
        "\n## Deliverables\n\n```yaml\ndeliverables:\n- what: \"Stored table\"\n  files: store.csv\n"
        "  checked_by: t01_answers/r01_compare\n  note: \"Written by the old pipeline.\"\n```\n"))
    content = work_progress.goal_cards("Job", job, root, work_progress.snapshot("Job", job), "Audience Report")
    box = content[content.index("Stored table"):]
    assert "<h5>Checked by</h5>" in box and "r01_compare" in box.split("<h5>Checked by</h5>")[1]
    assert "Written by the old pipeline." in box and "✅ <b>Stored table</b>" in content
    assert content.index("t01_answers") < content.index("Stored table")      # under the Task of the Run that checked it


def test_a_runs_outputs_are_shown_not_only_linked(board):
    """JL 261021: "why I cannot do the preview of the csv or the figures here": a figure is a picture, a table shows
    its first rows, a record folds open in place."""
    root, block, job, task = board
    folder = run(task)
    (folder / "result/01_chart.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (folder / "result/table.csv").write_text("name,count\nalpha,3\nbeta,4\n")
    page = work_progress.render_run(task, root, "r01_compare")
    assert '<img src="/Project/work/b51_topic/j01_tables/t01_answers/runs/r01_compare/result/01_chart.png"' in page
    assert "<h3>Tables · 1</h3>" in page and "2 rows × 2 columns" in page and "<td title=\"alpha\">alpha</td>" in page
    assert "<b>metrics.json</b>" in page and "&quot;compared&quot;:12" in page


def test_one_deliverable_holds_its_batches_and_what_is_still_open(board):
    """JL 261021: "the google search results should have three batches, is that so?": the batches fold inside the one
    deliverable, each with its files and Runs; an open point keeps it partly done even when every file is there."""
    root, block, job, task = board
    run(task)
    for name in ("first.csv", "retry.csv", "merged.csv"):
        (task / "runs/r01_compare/result" / name).write_text("a\n1\n")
    (job / "j01_tables.md").write_text((job / "j01_tables.md").read_text() + (
        "\n## Deliverables\n\n```yaml\ndeliverables:\n- what: \"Results\"\n  files: t01_answers/runs/r01_compare/result/merged.csv\n"
        "  run: t01_answers/r01_compare\n  from:\n  - what: \"First pass\"\n    files: t01_answers/runs/r01_compare/result/first.csv\n"
        "  - what: \"Retry\"\n    files: t01_answers/runs/r01_compare/result/retry.csv\n  open:\n  - \"Two searches empty\"\n```\n"))
    content = work_progress.goal_cards("Job", job, root, work_progress.snapshot("Job", job), "Audience Report")
    assert "<h5>From 2 batches</h5>" in content and "<b>First pass</b>" in content and "<b>Retry</b>" in content
    assert "<h5>Still open</h5>" in content and "Two searches empty" in content
    assert "🔶 <b>Results</b>" in content                                    # every file there, one point still open


def test_an_item_with_several_makers_ticks_only_when_each_finished(board):
    """The b03 trial (261021): an item that lists its Runs under runs: ticked on its files alone."""
    root, block, job, task = board
    run(task)
    run(task, "r02_fold01", status="running")
    (task / "runs/r01_compare/result/a.csv").write_text("a\n1\n")
    (job / "j01_tables.md").write_text((job / "j01_tables.md").read_text() + (
        "\n## Deliverables\n\n```yaml\ndeliverables:\n- what: \"Both folds\"\n  files: t01_answers/runs/r01_compare/result/a.csv\n"
        "  runs:\n  - {run: t01_answers/r01_compare, part: fold00}\n  - {run: t01_answers/r02_fold01, part: fold01}\n```\n"))
    content = work_progress.goal_cards("Job", job, root, work_progress.snapshot("Job", job), "Audience Report")
    assert "✅ <b>Both folds</b>" not in content and "<b>Both folds</b>" in content


def test_the_runs_read_as_a_tree_like_the_goal(board):
    """JL 261021: "result 跟 go 一样的 structure": Job, Task, the job each Run does, each Run on one line with its mark
    and only what its receipt holds."""
    root, block, job, task = board
    folder = run(task)
    card = yaml.safe_load((folder / "run.yaml").read_text())
    (folder / "run.yaml").write_text(yaml.safe_dump(dict(card, role="make")))
    content = work_progress.status_tree("Block", block, root, work_progress.snapshot("Block", block), "Audience Report")
    text = re.sub(r"<[^>]+>", "", content)
    assert content.count("<ul class=dtree>") == 1 and "Not recorded" not in text
    assert text.index("j01_tables") < text.index("t01_answers") < text.index("make") < text.index("r01_compare")
    assert "✅ r01_compare" in text and "12 requests agree" in text and "1 min 46 s" in text


def test_a_run_page_shows_data_rows_and_an_old_run_its_outcome(board):
    """JL 261021: "could you show some data rows as well?"; "既然这个东西已经跑了，那你应该就能够 link 到之前的这个结果"."""
    import pandas as pd
    root, block, job, task = board
    folder = run(task)
    table = root / "_WorkSpace/t.parquet"
    table.parent.mkdir(parents=True)
    pd.DataFrame({"name": ["alpha", "beta"], "count": [3, 4]}).to_parquet(table)
    (folder / "result/heavy.yaml").write_text("heavy:\n- {file: t.parquet, path: _WorkSpace/t.parquet}\n")
    page = work_progress.render_run(task, root, "r01_compare")
    assert "<h3>Data rows · 1</h3>" in page and "2 rows × 2 columns" in page and 'title="alpha">alpha<' in page
    run(task, "r02_old", outcome={"searches_asked": 1983, "searches_answered": 1964}, receipt={"rebuilt_by": "rebuild_receipts.py"})
    run(task, "r03_old", outcome={"searches_asked": 21, "searches_answered": 21}, gate="missed: coverage")
    rows = {r["run"]: r for r in work_progress.records(task)}
    assert work_progress.run_mark(rows["r02_old"]) == "🔶 finished, 1,964 of 1,983 answered"     # a rebuilt receipt reads like any
    assert work_progress.run_mark(rows["r03_old"]).startswith("🔶 finished, gate missed: coverage")


def test_a_plain_table_inside_a_view_keeps_the_page_whole():
    """JL 261021: "这个地方怎么乱成了一坨呀": a Markdown table (no class) got the wrap's closing div without its opening one,
    which closed the item's box early and spilled the rest of the page beside it."""
    body = "<div><table><tr><td>a</td></tr></table><table class=wf-table><tr><td>b</td></tr></table></div>"
    import re as _re
    wrapped = _re.sub(r"<table(?=[\s>])", "<div class=work-table-scroll><table", body).replace("</table>", "</table></div>")
    assert wrapped.count("<div") == wrapped.count("</div>")


def test_a_finished_set_can_be_browsed_level_by_level(board):
    """JL 261021: "我在哪里可以看到我最终的 Virtual Set 的成品呢？": the index level by level, a page's records as cards,
    one record whole, its picture as bytes."""
    import pandas as pd
    root, block, job, task = board
    site = root / "_WorkSpace/site"
    (site / "state=TX").mkdir(parents=True)
    pd.DataFrame({"state": ["TX"], "city": ["Austin"], "specialty": ["Family Medicine"], "file_path": ["state=TX/p.parquet"],
                  "n_physicians": [2]}).to_parquet(site / "index.parquet")
    pd.DataFrame({"display_name": ["Ann A", "Bo B"], "stated_age_years": [58, 40], "page_markdown": ["# Ann A", "# Bo B"],
                  "portrait_image": [b"\xff\xd8jpg", None]}).to_parquet(site / "state=TX/p.parquet")
    (job / "j01_tables.md").write_text((job / "j01_tables.md").read_text() + (
        "\n## Deliverables\n\n```yaml\ndeliverables:\n- what: \"Site\"\n  files: ../../../_WorkSpace/site/index.parquet\n"
        "  browse:\n    root: _WorkSpace/site\n    index: index.parquet\n    count: n_physicians\n"
        "    card: [display_name, stated_age_years]\n    record: page_markdown\n    image: portrait_image\n```\n"))
    get = lambda q: (lambda k: q.get(k))
    top, kind = work_progress.render_browse(job, root, get({"item": "0"}))
    assert kind.startswith("text/html") and "<b>TX</b>" in top and "2 physicians · 1 pages" in top
    page, _ = work_progress.render_browse(job, root, get({"item": "0", "state": "TX", "city": "Austin", "specialty": "Family Medicine"}))
    assert "2 records on this page" in page and "<b>Ann A</b>" in page and "58 years" in page
    whole, _ = work_progress.render_browse(job, root, get({"item": "0", "state": "TX", "city": "Austin", "specialty": "Family Medicine", "row": "0"}))
    assert "One record, whole" in whole and "<h1>Ann A</h1>" in whole
    pic, ctype = work_progress.render_browse(job, root, get({"item": "0", "state": "TX", "city": "Austin", "specialty": "Family Medicine", "img": "0"}))
    assert pic == b"\xff\xd8jpg" and ctype == "image/jpeg"


def test_a_link_to_a_set_is_a_deliverable_ticked_only_when_it_opens(board):
    """JL 261021: "这个地方我觉得应该算是你的 Goal 中的一个呀 ... provide such a link": a view a reader opens is a
    deliverable, with its link on its line, and ticks only when the set it opens can be browsed."""
    import pandas as pd
    root, block, job, task = board
    site = root / "_WorkSpace/site"
    site.mkdir(parents=True)
    pd.DataFrame({"state": ["TX"], "city": ["Austin"], "specialty": ["FM"], "file_path": ["p.parquet"]}).to_parquet(site / "index.parquet")
    face = job / "j01_tables.md"
    base = face.read_text()
    lst = ("\n## Deliverables\n\n```yaml\ndeliverables:\n- what: \"Site\"\n  files: x\n{browse}- what: \"Link\"\n  kind: view\n"
           "  files: _WorkSpace/site/index.parquet\n  opens: \"Site\"\n```\n")
    face.write_text(base + lst.format(browse="  browse:\n    root: _WorkSpace/site\n    index: index.parquet\n"))
    text = re.sub(r"<[^>]+>", "", work_progress.goal_cards("Job", job, root, work_progress.snapshot("Job", job), "Audience Report"))
    assert "✅ Link" in text and "🔎 open it" in text
    face.write_text(base + lst.format(browse=""))                     # nothing to browse: the link is not delivered
    text = re.sub(r"<[^>]+>", "", work_progress.goal_cards("Job", job, root, work_progress.snapshot("Job", job), "Audience Report"))
    assert "☐ Link" in text and "🔎 open it" not in text


def test_a_ticket_receipt_saying_started_and_ended_reads_its_times_and_summary(board):
    root, block, job, task = board
    folder = run(task, started_at=None, finished_at=None, headline=None, started="2026-09-25T13:33:53+00:00",
                 ended="2026-09-25T13:34:02+00:00", summary={"tables": 28, "rows_total": 1562150228, "readiness": "blocked",
                                                          "unrouted": [], "blockers": ["fasting rule"]})
    row = next(r for r in work_progress.records(task) if r["run"] == folder.name)
    assert work_progress.elapsed(row["receipt"]) == "9 s"
    assert row["headline"] == "blockers: fasting rule · readiness blocked · 1,562,150,228 rows total · 28 tables"   # the fixture sorts keys
    assert work_progress.read_yaml(folder / "result/runtime.yaml")["started_at"] is None   # the record as read stays unchanged


def test_a_receipt_yaml_cannot_parse_still_gives_its_status(board):
    """An older receipt wrote an unquoted headline with a colon in it; its Run is complete, not "Not recorded"
    (b51 j01 t12-t15, 261021)."""
    root, block, job, task = board
    folder = run(task, "r01_b1_contract")
    (folder / "run.yaml").write_text("run: r01_b1_contract\nkind: hard\nstatus: null\n")
    (folder / "result/runtime.yaml").write_text(
        "run:        r01_b1_contract\nstatus:     complete\nstarted_at: 2026-09-12T16:33:54-04:00\n"
        "finished_at: 2026-09-12T16:33:57-04:00\ninputs:\n  - path: 'config.yaml'\n"
        "headline: B1 food: FAIL, 10/13 checks pass - FAIL C07 C12\n")
    row = next(r for r in work_progress.records(task) if r["run"] == "r01_b1_contract")
    assert row["status"] == "complete"
    assert row["headline"] == "B1 food: FAIL, 10/13 checks pass - FAIL C07 C12"
    assert work_progress.elapsed(row["receipt"]) == "3 s"


def test_a_deliverable_can_name_the_spaces_code(board):
    root, block, job, task = board
    (root / "code/haifn/fn_source").mkdir(parents=True)
    (root / "code/haifn/fn_source/SourceFn.py").write_text("x = 1\n")
    face = job / "j01_tables.md"
    face.write_text(face.read_text() + '\n## Deliverables\n\n```yaml\ndeliverables:\n- what: "SourceFn"\n  kind: code\n'
                    '  files: code/haifn/fn_source/SourceFn.py\n```\n')
    text = re.sub(r"<[^>]+>", "", work_progress.goal_cards("Job", job, root, work_progress.snapshot("Job", job), "Audience Report"))
    assert "✅ SourceFn" in text


def test_a_placeholder_goal_is_not_shown_as_the_goal(board):
    """A new Job face says `goal: open` until someone writes it; the Goal reads "Goal not yet specified" (261021)."""
    root, block, job, task = board
    (job / "j01_tables.md").write_text("# Tables\ngoal: open\nclose: open\n")
    assert work_progress.goal(job) == "Goal not yet specified"


def test_a_background_reads_under_the_goal_and_is_absent_without_one(board):
    """A face's `## Background` shows under its goal as bullets, bold and code kept; a face without one draws nothing
    (JL 261021: "可以再加一个 section，比如叫 background")."""
    root, block, job, task = board
    assert work_progress.background_html(job) == ""
    (job / "j01_tables.md").write_text("# Tables\ngoal: Build the table\nclose: Validate it\n\n## Background\n\n"
                                       "- **Why**: a model needs <one> number\n  for each row\n- **Where**: `t01` built it\n\n## Topic\nx\n")
    out = work_progress.background_html(job)
    assert "BACKGROUND" in out and out.count("<li>") == 2
    assert "<b>Why</b>: a model needs &lt;one&gt; number for each row" in out
    assert "<code>t01</code>" in out and "Topic" not in out


def test_a_background_timeline_block_is_drawn_and_another_block_kept_as_written(board):
    """A fenced yaml block holding `timeline:` draws the meal down its timeline: a lane per food item, a row per
    moment, a band per bite across the items it holds (JL 261021: the Item1 to Item3, t1 to tN sketch); any other
    fenced block shows as it is written."""
    root, block, job, task = board
    (job / "j01_tables.md").write_text(
        "# Tables\ngoal: Normalize food items\n\n## Background\n\n- **A bite**: one moment\n\n```yaml\ntimeline:\n"
        "  items: [Item 1, Item 2, Item 3]\n  times: [t1, t2, tN]\n  bites:\n"
        "  - {name: bite 1, at: t2, items: [Item 1, Item 2]}\n  - {name: lost, at: t9, items: [Item 1]}\n"
        "  caption: one meal\n```\n\n```text\na <plain> block\n```\n\n## Topic\nx\n")
    out = work_progress.background_html(job)
    assert out.count("<svg") == 1 and out.count("<li>") == 1
    assert out.count("<rect") == 1                                   # a bite at a moment not listed is not drawn
    assert all(f">{name}</text>" in out for name in ("Item 1", "Item 3", "t2", "tN", "bite 1"))
    assert "<figcaption" in out and "one meal" in out
    assert "<pre>a &lt;plain&gt; block</pre>" in out and "Topic" not in out


def test_a_timeline_span_holds_one_lane_over_a_stretch_of_time():
    """`spans` draw an activity in one lane from its start to its end; `aside` is dashed (s22 j02, 261021)."""
    svg = work_progress.timeline_svg({"items": ["Row 1", "Row 2"], "times": ["00:00", "t1", "t2", "24:00"],
                                      "spans": [{"name": "a walk", "item": "Row 1", "from": "t1", "to": "t2"},
                                                {"name": "day total", "item": "Row 2", "from": "00:00", "to": "24:00",
                                                 "aside": True},
                                                {"name": "lost", "item": "Row 9", "from": "t1", "to": "t2"}]})
    assert svg.count('rx="9"') == 2 and svg.count("stroke-dasharray") == 1
    assert ">a walk<" in svg and ">day total<" in svg and "lost" not in svg


def test_a_span_with_zoom_opens_into_its_own_lanes_in_the_same_picture(board):
    """A span marked `zoom: true` and the block's `zoom:` draw one picture: the day's events, and that span opened
    into its own items and bites beside it, joined by two dashed lines (JL 261021: "你可以把这两个图融成一个图吗")."""
    root, block, job, task = board
    (job / "j01_tables.md").write_text(
        "# Tables\ngoal: Normalize food items\n\n## Background\n\n```yaml\ntimeline:\n  items: [Meal 1, Meal 2]\n"
        "  times: [t1, t2, t3, t4]\n  spans:\n  - {name: lunch, item: Meal 1, from: t1, to: t2}\n"
        "  - {name: dinner, item: Meal 2, from: t3, to: t4, zoom: true}\n  zoom:\n    items: [Item 1, Item 2]\n"
        "    times: [T0, ta, T1]\n    bites:\n    - {name: bite 1, at: ta, items: [Item 1, Item 2]}\n```\n")
    out = work_progress.background_html(job)
    assert out.count("<svg") == 1 and out.count('stroke-dasharray="5 5"') == 2      # one picture, two zoom lines
    assert all(f">{name}</text>" in out for name in ("lunch", "dinner", "Item 2", "bite 1", "ta"))
    assert out.count('<g transform="translate(') == 1


def test_a_clock_timeline_gives_every_hour_the_same_height():
    """`clock` puts each HH:MM where its minutes put it and labels only the whole hours (s22 j02, 261021)."""
    parts, w, h, boxes = work_progress.timeline_parts({
        "items": ["a walk", "by the hour"], "clock": {"from": "07:00", "to": "09:00", "hour_px": 150},
        "spans": [{"name": "a walk", "item": "a walk", "from": "07:40", "to": "08:10"},
                  {"name": "walk 20 min", "item": "by the hour", "from": "07:00", "to": "08:00"},
                  {"name": "walk 10 · run 30", "item": "by the hour", "from": "08:00", "to": "09:00"}]})
    first, second = boxes["walk 20 min"], boxes["walk 10 · run 30"]
    assert abs((first[3] - first[1]) - (second[3] - second[1])) < 1        # two hours, two equal heights
    walk = boxes["a walk"]
    assert abs((walk[3] - walk[1]) - (150 / 2 - 6)) < 1                    # 30 minutes: half an hour's height
    assert ">07:00<" in parts and ">09:00<" in parts and ">07:40<" not in parts
    assert second[2] - second[0] > 116                                      # a longer name widens its box


def test_a_clock_runs_past_midnight_and_a_day_ends_at_24():
    """A night (23:00 to 07:00) keeps going past midnight; a whole day is labelled to 24:00, every `mark` minutes."""
    night, _, _, boxes = work_progress.timeline_parts({
        "items": ["asleep"], "clock": {"from": "23:00", "to": "07:00", "hour_px": 60},
        "spans": [{"name": "asleep", "item": "asleep", "from": "23:00", "to": "01:00"}]})
    top, bottom = boxes["asleep"][1], boxes["asleep"][3]
    assert abs((bottom - top) - (120 - 6)) < 1                              # two hours after 23:00, not backwards
    assert re.findall(r">(\d\d:\d\d)<", night)[:3] == ["23:00", "00:00", "01:00"]
    day, _, _, _ = work_progress.timeline_parts({
        "items": ["per day"], "clock": {"from": "00:00", "to": "24:00", "hour_px": 24, "mark": 180},
        "spans": [{"name": "day total", "item": "per day", "from": "00:00", "to": "24:00"}]})
    assert re.findall(r">(\d\d:\d\d)<", day) == ["00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00",
                                                     "21:00", "24:00"]


def test_a_rule_draws_its_question_and_a_box_per_answer_in_the_same_picture(board):
    """A timeline's `rule:` draws the handling rule beside it: the question, then a box per answer with its title,
    what is done and its example; the answer that holds today is filled (JL 261021: "只记了开始、没有记结束，这时候
    该怎么办？... 你在这个地方完全没有显示出来")."""
    root, block, job, task = board
    (job / "j01_tables.md").write_text(
        "# Tables\ngoal: Normalize food items\n\n## Background\n\n```yaml\ntimeline:\n  items: [event_meals]\n"
        "  clock: {from: '11:00', to: '13:00'}\n  spans:\n  - {name: lunch, item: event_meals, from: '11:30', to: '12:30'}\n"
        "  rule:\n    question: Is T1 logged?\n    branches:\n"
        "    - {answer: 'no', title: Only T0, then: all to its hour, example: snack 15:10, today: true}\n"
        "    - {answer: 'yes', title: T0 and T1, then: shared by minutes, example: lunch half and half}\n```\n")
    out = work_progress.background_html(job)
    assert out.count("<svg") == 1 and ">Is T1 logged?</text>" in out
    assert ">no</text>" in out and ">yes</text>" in out and ">Only T0</text>" in out and ">shared by minutes</text>" in out
    assert out.count('fill="#fff3bf" stroke="currentColor" stroke-width="1.5"/>') >= 2      # today's answer, and the span


def test_a_receipt_with_counts_or_outputs_or_metrics_says_its_numbers(board):
    root, block, job, task = board
    a = run(task, "r01_counts", headline=None, counts={"tables": 67, "min_cell": 11})
    b = run(task, "r02_outputs", headline=None, outputs=[{"table": "patient_universe", "rows": 466745, "columns": 7, "bytes": 9}])
    c = run(task, "r03_metrics", headline=None)
    (c / "result/metrics.json").write_text('{"procname": "SignalDiabAbsentA1c", "columns": 15, "pass": true}')
    said = {r["run"]: r["headline"] for r in work_progress.records(task)}
    assert said[a.name] == "11 min cell · 67 tables"                    # the fixture sorts keys
    assert said[b.name] == "patient_universe: 466,745 rows · 7 columns"
    assert said[c.name] == "procname SignalDiabAbsentA1c · 15 columns"
