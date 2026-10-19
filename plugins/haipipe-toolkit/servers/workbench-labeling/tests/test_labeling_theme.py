"""The labeling theme on the base frame (labeling_theme.py): status and links; rendering writes nothing.

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
from live import task_labeling as TL  # noqa: E402


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
        scan = [T.VIEW[v][2] for v in T.SCAN_WORK]
        self.assertEqual(s["Work Details"]["subspaces"], list(TL.BUILD_TABS) + scan)
        self.assertEqual(s["Description"]["subspaces"][:2], ["Scope", "Contract"])
        self.assertEqual(s["Delivery"]["subspaces"][:3], ["Files", "Handoff", "Final labels"])
        for sub, space, view in (("Audit", "Work Details", "space=quality&amp;view=audit"),
                                 ("Scan", "Work Details", "space=delivery&amp;view=scan"),
                                 ("Handoff", "Delivery", "space=delivery&amp;view=handoff"),
                                 ("Contract", "Description", "space=data&amp;view=contract")):
            with self.subTest(sub=sub):
                page = frame.render(self.theme, self.root, self.task, space, sub)
                self.assertIn(view, page)
                self.assertEqual(spaces(self.theme, self.root, self.task, sub)[space]["run_doing"], [sub])

    def test_building_works_one_stage_per_tab(self):
        """b15 s42: the four Stages are tabs; each shows Operation (Input, 👁 budget, the prompt) then Result."""
        for i, (tab, title) in enumerate(zip(TL.BUILD_TABS, ("Stage 1 · Contract", "Stage 2 · Initial Labeling Definition",
                                                             "Stage 3 · Rounds", "Stage 4 · Handoff"))):
            with self.subTest(tab=tab):
                page = frame.render(self.theme, self.root, self.task, "Work Details", tab)
                self.assertIn(title, page)
                self.assertIn("/haipipe-labeling-building", page)
                self.assertIn("👁", page)
                self.assertIn(">Operation<", page)
                self.assertIn(">Result<", page)
        report = frame.render(self.theme, self.root, self.task, "Audience Report", "3 · Rounds")
        self.assertNotIn(">Operation<", report)
        self.assertIn("seed → retrieve over X∖S", frame.render(self.theme, self.root, self.task, "Work Details", "3 · Rounds"))

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
        self.assertEqual(T.types_of(task(job, "t03_demo_ground_truth", "raw")), ("ground_truth",))
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
        self.assertIn("optional", page)                      # ground truth and score: optional until there is ground truth
        self.assertNotIn("not made yet", page)
        task(job, "t03_demo_ground_truth", "raw")            # with ground truth, a score Task is needed
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
        for words in ("class=stat-row", "main: the placeholder text", "📊 Items", "demo-00",
                      "placeholder words here", "🧩 One item", "🎲 Random items", "📈 Statistics",
                      "📦 Version"):                                               # the cards, real items (s41-D07)
            with self.subTest(words=words):
                self.assertIn(words, page)
        for words in ("Copy prompt", "The recipe, as signed", "What we have", "Make the items, again"):  # Work's only
            with self.subTest(absent=words):
                self.assertNotIn(words, page)
        page = frame.render(self.theme, self.root, items, "Audience Report", "3 · Embedding")
        self.assertIn("Step 3 fills this", page)
        page = frame.render(self.theme, self.root, items, "Audience Report", "3 · Item list")    # an older link
        self.assertIn("main: the placeholder text", page)

    def test_the_items_task_works_one_step_per_tab_with_its_prompt_and_details(self):
        items = items_task(self.task.parent)
        s = spaces(self.theme, self.root, items)
        self.assertEqual(s["Work Details"]["subspaces"], ["1 · Data", "2 · Items", "3 · Embedding"])
        where = "Project-X/labeling/b61_demo_label/j01_building_demo/t02_demo_items"
        tabs = {"1 · Data": ("📥 Step 1 · Data", "→ next", "Input",
                             "next: 🧱 Step 2 · Items", f"/haipipe-labeling-preparation {where} describe:"),
                "2 · Items": ("🧱 Step 2 · Items", "✓ done", "Recipe, signed · r01_demo", "All 3 items",
                              "scripts/items_transform.py", "Each row becomes one placeholder item.", "📦 Version",
                              "Yes 5 · No 5", "🧱 Revise the items", f"{where} revise: read my notes"),
                "3 · Embedding": ("🗺 Step 3 · Embedding", "→ next", "Step 3 fills this",
                                  f"{where} embed: plan the embedding Run")}
        for sub, words in tabs.items():
            page = frame.render(self.theme, self.root, items, "Work Details", sub)
            for w in words:
                with self.subTest(sub=sub, words=w):
                    self.assertIn(w, page)
            with self.subTest(sub=sub, copy=True):         # Items has two prompts: the step's and its revise
                self.assertEqual(page.count('class="run-copy work-act" data-copy="'), 2 if sub == "2 · Items" else 1)
                self.assertIn("<textarea class=run-notes", page)   # every prompt takes the person's notes (s41-D14)
        page = frame.render(self.theme, self.root, items, "Work Details", "2 · Items")
        self.assertIn('<details class="topic work-task items-step"><summary>', page)     # a done step folds (D15)
        page = frame.render(self.theme, self.root, items, "Work Details", "3 · Embedding")
        self.assertIn('<details class="topic work-task items-step" open>', page)          # the step to do now
        self.assertIn("<details class=run-prompt-box open>", page)

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
            "background": {"what": "a placeholder corpus", "license": "CC BY 4.0"},
            "labels": [{"column": "gold", "who": "expert", "counted_per": "item_id", "values": {"Yes": 3, "No": 2}}],
            "text_to_label": {"columns": [{"column": "response", "words_median": 4, "words_min": 2, "words_max": 9,
                                           "values": 5, "lines_median": 1}]},
            "samples": {"seed": 7, "rows": [1, 2]},
            "gotchas": ["a placeholder note"]}))
        for space in ("Work Details", "Audience Report"):
            page = frame.render(self.theme, self.root, items, space, "1 · Data")
            for words in ("🎲 Random samples", "📖 Background", "a placeholder corpus", "📊 Basic description",
                          '<b style="font-size:20px">10</b><span>rows</span>', '<b style="font-size:20px">5</b><span>items</span>',
                          "One placeholder rating of one chat.", "🧩 One row (made up)", "rowspan=2", "an invented reply",
                          "🏷 Current labels", "<code>gold</code>", "💬 Text to label", "⚠️ Watch out",
                          "a placeholder note", "2 columns", "4 words median", "r02_raw_read"):
                with self.subTest(space=space, words=words):
                    self.assertIn(words, page)
        self.assertNotIn("<h4>Input</h4>", page)                              # Report: the cards only
        page = frame.render(self.theme, self.root, items, "Work Details", "2 · Items")
        self.assertIn("r01_demo", page)                                     # the items still come from the Run that made them

    def test_step_three_draws_the_items_tasks_own_embedding(self):
        items = items_task(self.task.parent)
        planned = items / "runs" / "r03_embedding_minilm"
        planned.mkdir(parents=True)
        (planned / "r03_embedding_minilm.sh").write_text("echo placeholder\n")
        (planned / "run.yaml").write_text("run: r03_embedding_minilm\nkind: hard\ntype:\n- embedding-build\nstatus: planned\n")
        (items / "scripts" / "config").mkdir()
        (items / "scripts" / "config" / "r03_embedding_minilm.yaml").write_text(
            "operation: embed\nmodel: sentence-transformers/all-MiniLM-L6-v2\ninput: main\nmap: tsne\n")
        page = frame.render(self.theme, self.root, items, "Work Details", "3 · Embedding")
        for words in ("Build · r03_embedding_minilm", "all-MiniLM-L6-v2", "data-post=\"/_board/labeling/items\"",
                      ">Agree</button>", "✍ sign",
                      "I Agree r03_embedding_minilm on the screen first; then run"):
            with self.subTest(words=words):
                self.assertIn(words, page)
        (planned / "run.yaml").write_text("run: r03_embedding_minilm\nkind: hard\ntype:\n- embedding-build\n"
                                          "status: planned\nsigns:\n  by: a person\n  at: today\n")
        page = frame.render(self.theme, self.root, items, "Work Details", "3 · Embedding")
        self.assertIn("✓ agreed</span> by a person", page)
        self.assertIn("run r03_embedding_minilm and settle it", page)
        (planned / "result").mkdir()
        (planned / "result" / "runtime.yaml").write_text("run: r03_embedding_minilm\nstatus: complete\n")
        (planned / "result" / "map.json").write_text(json.dumps(
            [{"item_id": f"demo-{i:02d}", "x": i * 1.0, "y": i % 2, "group": i % 2} for i in range(3)]))
        (planned / "result" / "groups.json").write_text(json.dumps(
            [{"group": 0, "size": 2, "keywords": ["picnic", "park"], "typical": ["demo-00"]},
             {"group": 1, "size": 1, "keywords": ["tax"]}]))
        (planned / "result" / "manifest.yaml").write_text("model: sentence-transformers/all-MiniLM-L6-v2\ndim: 384\n"
                                                          "items: 3\ngroups: 2\ninput: main\n")
        for space in ("Work Details", "Audience Report"):
            page = frame.render(self.theme, self.root, items, space, "3 · Embedding")
            for words in ("📍 Map", "<svg", "data-item=\"demo-01\" data-group=\"1\"", "🧩 Groups", "picnic · park",
                          "all-MiniLM-L6-v2", "📏 Near-duplicates", "🧭 Outliers", "⚙️ Builds"):
                with self.subTest(space=space, words=words):
                    self.assertIn(words, page)
        page = frame.render(self.theme, self.root, items, "Work Details", "3 · Embedding")
        self.assertIn("✓ done", page)
        self.assertIn("Build, agreed · r03_embedding_minilm", page)

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
