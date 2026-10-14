"""The labeling theme on the base frame (labeling_theme.py): status and links only, read only.

A placeholder Project with one labeling Block (schema.yaml, one Job, one labeling Task Page with no
labeling/ lane yet): the Block's Description and Work Details, the Task's views, each linking to the
Labeling workbench at that view; without the labeling package the theme falls back to vanilla."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import frame  # noqa: E402
from live import labeling_theme as T  # noqa: E402


def project(tmp: str) -> tuple[Path, Path, Path]:
    root = Path(tmp)
    block = root / "Project-X" / "labeling" / "b61_demo_label"
    task = block / "j01_building_demo" / "t01_demo_labeling"
    task.mkdir(parents=True)
    (block / "board.md").write_text("# /demo-label: How <placeholder> is it?\n\nboard-kind: task-block\n"
                                    "spine: one placeholder schema\n")
    (block / "schema.yaml").write_text("schema: S_00\nlabels: [high, low, none]\n")
    (task / "t01_demo_labeling.md").write_text("# Demo labeling\nstate: 🔴 OPEN\ntask-type: labeling\n"
                                              "page-type: labeling\n\n## Opening\n\nA placeholder job.\n")
    return root, block, task


def task(job: Path, name: str, task_type: str, body: str = "") -> Path:
    folder = job / name
    folder.mkdir()
    (folder / f"{name}.md").write_text(f"# {name}\nstate: ✅ DONE · r01 read\ntask-type: {task_type}\n\n## Opening\n\n"
                                       f"A placeholder Task.\n{body}")
    return folder


def items_task(job: Path) -> Path:
    """A placeholder items Task: its face's Data and Method parts, one complete Run with its manifest."""
    folder = task(job, "t02_demo_items", "data", "\n## Content\n\n### 2 · Data · the raw file\n"
                  "**Division map — what was read**\n```text\nraw.csv ─▶ 10 rows\n```\n\nA placeholder raw file.\n\n"
                  "### 3 · Method · one row, one item\n\nEach row becomes one placeholder item.\n")
    run = folder / "runs" / "r01_demo"
    (run / "result").mkdir(parents=True)
    (run / "r01_demo.sh").write_text("echo placeholder\n")
    (run / "run.yaml").write_text("run: r01_demo\nkind: hard\nstatus: complete\n")
    (run / "result" / "manifest.yaml").write_text("source: Placeholder corpus\ntransform: items_transform.py\n"
                                                  "item: \"main: the placeholder text\"\nitems: 10\n"
                                                  "gold:\n  'Yes': 5\n  'No': 5\n")
    (run / "result" / "metrics.json").write_text('{"summary": {"headline": "10 placeholder items"}, '
                                                 '"store": "_WorkSpace/LabelingStore/demo/items-v1"}')
    store = job.parents[3] / "_WorkSpace" / "LabelingStore" / "demo" / "items-v1"
    store.mkdir(parents=True)
    (store / "items.jsonl").write_text("".join(
        f'{{"item_id": "demo-{i:02d}", "context_before": "Person: a\\nAI: b", "main": "placeholder words here", '
        f'"context_after": ""}}\n' for i in range(3)))
    (folder / "scripts").mkdir()
    (folder / "scripts" / "items_transform.py").write_text("# placeholder\n")
    return folder


def spaces(theme, root, folder, sub=""):
    data = json.loads(frame.frame_json(theme, root, folder, sub))
    return {s["name"]: s for s in data["spaces"]}


class LabelingThemeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root, self.block, self.task = project(self.tmp.name)
        self.theme = frame.themes()["labeling"]

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_labeling_block_reads_by_its_theme_folder(self):
        self.assertEqual(frame.theme_of(self.task, self.root), "labeling")

    def test_the_block_shows_its_schema_and_its_jobs_status(self):
        s = spaces(self.theme, self.root, self.block)
        self.assertEqual(s["Description"]["subspaces"], ["Scope", "Schema"])
        self.assertEqual(s["Work Details"]["subspaces"], ["Jobs", "Labeling"])
        self.assertIn("Prepare a corpus", s["Work Details"]["run_doing"])
        page = frame.render(self.theme, self.root, self.block, "Description", "Schema")
        self.assertIn("labels: [high, low, none]", page)
        page = frame.render(self.theme, self.root, self.block, "Work Details", "Labeling")
        # labeling/ is the Theme's name (s01-D29), so the row is the Job, b61j01, as under labelings/
        self.assertIn("b61j01", page)
        self.assertIn("/_board/labeling?path=", page)

    def test_a_job_page_opens_each_view_in_the_labeling_workbench(self):
        s = spaces(self.theme, self.root, self.task)
        work = [v[2] for v in T.WORK]
        self.assertEqual(s["Work Details"]["subspaces"][:len(work)], work)
        self.assertEqual(s["Description"]["subspaces"][:2], ["Scope", "Contract"])
        self.assertEqual(s["Delivery"]["subspaces"][:3], ["Files", "Handoff", "Final labels"])
        for sub, space, view in (("Rounds", "Work Details", "space=labeling&amp;view=rounds"),
                                 ("Audit", "Work Details", "space=quality&amp;view=audit"),
                                 ("Scan", "Work Details", "space=delivery&amp;view=scan"),
                                 ("Handoff", "Delivery", "space=delivery&amp;view=handoff"),
                                 ("Contract", "Description", "space=data&amp;view=contract")):
            with self.subTest(sub=sub):
                page = frame.render(self.theme, self.root, self.task, space, sub)
                self.assertIn(view, page)
                self.assertEqual(spaces(self.theme, self.root, self.task, sub)[space]["run_doing"], [sub])

    def test_it_writes_nothing_and_shows_no_items(self):
        before = sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob("*"))
        for sub in [v[2] for v in T.VIEWS] + ["Scope", "Files"]:
            frame.render(self.theme, self.root, self.task, "Work Details", sub)
        self.assertEqual(sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob("*")), before)

    def test_without_the_labeling_package_it_is_vanilla(self):
        saved, T.L = T.L, None
        try:
            self.assertEqual(T.spaces("Block", self.block, self.root, ""), {})
            self.assertEqual(T.spaces("Task", self.task, self.root, ""), {})
        finally:
            T.L = saved

    def test_a_task_that_is_no_labeling_job_is_vanilla(self):
        other = self.block / "j01_building_demo" / "t02_notes"
        other.mkdir()
        (other / "t02_notes.md").write_text("# Notes\n")
        self.assertEqual(T.spaces("Task", other, self.root, ""), {})


    # ── the Task types of a labeling Job (b15 s13-labeling-task) ─────────────────────────────────
    def test_a_task_type_comes_from_its_task_type_line(self):
        job = self.task.parent
        self.assertEqual(T.types_of(self.task), ("building", "scanning"))
        self.assertEqual(T.types_of(items_task(job)), ("items",))
        self.assertEqual(T.types_of(task(job, "t03_demo_keys", "raw")), ("keys",))
        self.assertEqual(T.types_of(task(job, "t04_demo_scanning", "labeling-scanning")), ("scanning",))
        self.assertEqual(T.types_of(job), ())

    def test_the_task_dropdown_groups_tasks_by_type(self):
        self.assertEqual(T.option(items_task(self.task.parent)), ("Task · t02 · items", "📦 Items"))
        self.assertEqual(T.option(self.task), ("Task · t01 · building + scanning", "🏗 Building + 🔍 Scanning"))
        self.assertIsNone(T.option(self.task.parent))

    def test_the_job_shows_each_tasks_type_and_the_types_still_to_make(self):
        job = self.task.parent
        items_task(job)
        page = frame.render(self.theme, self.root, job, "Work Details", "")
        self.assertIn("📦 items · ✅ DONE", page)
        self.assertIn("🏗 building + 🔍 scanning", page)
        self.assertIn("optional", page)                      # keys and score: optional while there are no keys
        self.assertNotIn("not made yet", page)
        task(job, "t03_demo_keys", "raw")                    # with keys, a score Task is needed
        page = frame.render(self.theme, self.root, job, "Work Details", "")
        self.assertIn("⬜ t04_building_demo_score", page)
        self.assertIn("not made yet", page)
        self.assertIn("run-add-&lt;tNN&gt;-score", page)
        self.assertEqual(T.work_meta(job, self.root), "to make: 📊 score")

    def test_the_items_task_reports_one_result_per_step(self):
        items = items_task(self.task.parent)
        s = spaces(self.theme, self.root, items)
        self.assertEqual(s["Audience Report"]["subspaces"], ["1 · Data", "2 · Items", "3 · Embedding"])
        page = frame.render(self.theme, self.root, items, "Audience Report", "2 · Items")
        for words in ("class=stat-row", "items", "One item = main: the placeholder text", "The items", "demo-00",
                      "placeholder words here", "One item, drawn"):                      # the real items (s41-D07)
            with self.subTest(words=words):
                self.assertIn(words, page)
        for words in ("Copy prompt", "The recipe, as signed"):                           # Work's only
            with self.subTest(absent=words):
                self.assertNotIn(words, page)
        page = frame.render(self.theme, self.root, items, "Audience Report", "3 · Embedding")
        self.assertIn("models built", page)
        self.assertIn("Not built yet", page)
        page = frame.render(self.theme, self.root, items, "Audience Report", "3 · Item list")    # an older link
        self.assertIn("One item = main: the placeholder text", page)

    def test_the_items_task_works_one_step_per_tab_with_its_prompt_and_details(self):
        items = items_task(self.task.parent)
        s = spaces(self.theme, self.root, items)
        self.assertEqual(s["Work Details"]["subspaces"], ["1 · Data", "2 · Items", "3 · Embedding"])
        tabs = {"1 · Data": ("📥 Step 1 · Read the raw data", "✓ done", "next: 🧱 Step 2 · Make the items"),
                "2 · Items": ("🧱 Step 2 · Make the items", "✓ done", "The recipe, as signed", "All 3 items",
                              "scripts/items_transform.py", "Each row becomes one placeholder item.",
                              "What the Run recorded", "Yes 5 · No 5", "r01_demo"),
                "3 · Embedding": ("🗺 Step 3 · Embed the items", "→ next", "Not built yet",
                                  "holds back the sealed set")}
        for sub, words in tabs.items():
            page = frame.render(self.theme, self.root, items, "Work Details", sub)
            for w in words:
                with self.subTest(sub=sub, words=w):
                    self.assertIn(w, page)
            with self.subTest(sub=sub, copy=True):
                self.assertEqual(page.count('class="run-copy work-act" data-copy="'), 1)
        page = frame.render(self.theme, self.root, items, "Work Details", "3 · Embedding")
        self.assertIn("<details class=run-prompt-box open>", page)                             # the step to do now
        page = frame.render(self.theme, self.root, items, "Work Details", "1 · Data")
        self.assertIn("Project-X/labeling/b61_demo_label/j01_building_demo/t02_demo_items: a new rNN_raw_read Run", page)

    def test_step_one_shows_the_raw_table_card_with_a_made_up_row(self):
        items = items_task(self.task.parent)
        read = items / "runs" / "r02_raw_read"
        (read / "result").mkdir(parents=True)
        (read / "r02_raw_read.sh").write_text("echo placeholder\n")
        (read / "result" / "runtime.yaml").write_text("run: r02_raw_read\nstatus: complete\n")
        (read / "result" / "description.json").write_text(json.dumps({
            "table": {"file": "_WorkSpace/demo/raw.csv", "bytes": 2000000, "rows": 10, "columns": 2,
                      "what_it_is": "a placeholder file"},
            "grain": {"one_row_is": "One placeholder rating of one chat.",
                      "proof": {"rows": 10, "distinct_id": 10, "distinct_item_id": 5}},
            "groups": [{"name": "the chat", "meaning": "the chat judged", "columns": [
                {"name": "item_id", "filled": 1.0, "distinct": 5, "typical": "1 to 5"},
                {"name": "response", "filled": 1.0, "distinct": 5, "typical": "4 words median"}]}],
            "synth_df": {"story": "A made-up chat.", "rows": [{"item_id": 9001, "response": "an invented reply"}]},
            "gotchas": ["a placeholder note"]}))
        page = frame.render(self.theme, self.root, items, "Work Details", "1 · Data")
        for words in ("class=stat-row", "<b>10</b><span>rows</span>", "<b>5</b><span>items</span>",
                      "One placeholder rating of one chat.", "One row, drawn", "class=card-row", "an invented reply",
                      "The 2 columns, by group", "4 words median", "Checks", "a placeholder note", "raw.csv · read by r02_raw_read"):
            with self.subTest(words=words):
                self.assertIn(words, page)
        page = frame.render(self.theme, self.root, items, "Audience Report", "1 · Data")
        self.assertIn("One row, drawn", page)
        self.assertNotIn("The 2 columns, by group", page)                   # the details stay in Work
        page = frame.render(self.theme, self.root, items, "Work Details", "2 · Items")
        self.assertIn("r01_demo", page)                                     # the items still come from the Run that made them

    def test_step_three_draws_the_items_tasks_own_embedding(self):
        items = items_task(self.task.parent)
        planned = items / "runs" / "r03_embedding_minilm"
        planned.mkdir(parents=True)
        (planned / "r03_embedding_minilm.sh").write_text("echo placeholder\n")
        (planned / "run.yaml").write_text("run: r03_embedding_minilm\nkind: hard\ntype:\n- embedding-build\nstatus: planned\n")
        page = frame.render(self.theme, self.root, items, "Work Details", "3 · Embedding")
        self.assertIn("its ticket is ready (r03_embedding_minilm)", page)
        self.assertIn("run Project-X/labeling/b61_demo_label/j01_building_demo/t02_demo_items/runs/r03_embedding_minilm/"
                      "r03_embedding_minilm.sh", page)                    # the prompt names the ready ticket
        (planned / "result").mkdir()
        (planned / "result" / "runtime.yaml").write_text("run: r03_embedding_minilm\nstatus: complete\n")
        (planned / "result" / "map.json").write_text(json.dumps(
            [{"item_id": f"demo-{i:02d}", "x": i * 1.0, "y": i % 2, "group": i % 2} for i in range(3)]))
        (planned / "result" / "groups.json").write_text(json.dumps(
            [{"group": 0, "size": 2, "keywords": ["picnic", "park"]}, {"group": 1, "size": 1, "keywords": ["tax"]}]))
        (planned / "result" / "manifest.yaml").write_text("model: sentence-transformers/all-MiniLM-L6-v2\ndim: 384\n"
                                                          "items: 3\ngroups: 2\ninput: the reply, then the context\n")
        for space in ("Work Details", "Audience Report"):
            page = frame.render(self.theme, self.root, items, space, "3 · Embedding")
            for words in ("<b>1</b><span>models built</span>", "<b>2</b><span>groups</span>", "The map", "<svg",
                          "<title>demo-01 · G2</title>", "picnic · park", "all-MiniLM-L6-v2"):
                with self.subTest(space=space, words=words):
                    self.assertIn(words, page)
        page = frame.render(self.theme, self.root, items, "Work Details", "3 · Embedding")
        self.assertIn("✓ done", page)

    def test_a_scanning_task_carries_out_the_jobs_labeling_job(self):
        scanning = task(self.task.parent, "t02_demo_scanning", "labeling-scanning")
        s = spaces(self.theme, self.root, scanning)
        self.assertEqual(s["Work Details"]["subspaces"][:4], ["Test", "Evaluation", "Scan", "Audit"])
        self.assertEqual(s["Description"]["subspaces"][:2], ["Scope", "Handoff"])
        self.assertEqual(s["Delivery"]["subspaces"][:2], ["Files", "Final labels"])
        page = frame.render(self.theme, self.root, scanning, "Work Details", "Audit")
        self.assertIn("space=quality&amp;view=audit", page)
        self.assertIn("t01_demo_labeling", page)                # the job's Page, not its own
        self.assertEqual(T.task_action(scanning, self.root)[0], "🔍 Audit")

    def test_the_items_task_writes_nothing(self):
        items = items_task(self.task.parent)
        before = sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob("*"))
        for sub in ("1 · Data", "2 · Items", "3 · Embedding", "3 · Item list", "Report", "Draft"):
            frame.render(self.theme, self.root, items, "Audience Report", sub)
        for sub in ("1 · Data", "2 · Items", "3 · Embedding"):
            frame.render(self.theme, self.root, items, "Work Details", sub)
        frame.render(self.theme, self.root, self.task.parent, "Work Details", "")
        self.assertEqual(sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob("*")), before)


if __name__ == "__main__":
    unittest.main()
