"""The base frame (servers/workbench/frame.py): the levels, the six Spaces, the third row, the Runs
panel, the vanilla defaults read from disk, a theme laid over them, and the route."""
from __future__ import annotations

import json
import re
import tempfile
import unittest
from html import unescape
from urllib.parse import parse_qs, urlparse
from pathlib import Path

from host_paths import bootstrap
bootstrap()

from live import frame  # noqa: E402
from live.frame_view import FrameMixin  # noqa: E402


def project(tmp: str) -> Path:
    """A Project with one work Block: a Question, a drawing, one Job, one Task with a hard and a
    soft Run, code, a notebook and a delivery."""
    root = Path(tmp)
    block = root / "Project" / "tasks" / "b01_topic"
    task = block / "j01_job" / "t01_task"
    for d in (block / "studio" / "s01-flow", block / "reports" / "q01_ask", block / "delivery" / "d01-report",
              task / "scripts", task / "notebooks", task / "runs" / "r01_fit", task / "runs" / "run-build-t01"):
        d.mkdir(parents=True)
    (block / "b01_topic.md").write_text("# b01 · Topic\n\nboard-kind: task-block\nspine: a topic\n")
    (block / "studio" / "s01-flow" / "flow.excalidraw").write_text("{}")
    (block / "reports" / "q01_ask" / "q01_ask.md").write_text(
        "# What is asked?\n\nanswer-status: open\n\n## Opening\n\nOne line that answers it.\n")
    (block / "studio" / "s01-flow" / "s01-flow.md").write_text(
        "s01 · Flow\n=====\n\n**Topic:** how it flows.\n\n**Feeds:** `reports/q01_ask/`.\n\ns01-D01 · Proposed: one.\n")
    (block / "j01_job" / "j01_job.md").write_text("# j01 · Job\n\nanswers: Q01\n")
    (block / "delivery" / "d01-report" / "index.html").write_text("<p>x</p>")
    (task / "t01_task.md").write_text("# t01 · Task\n\ngoal: one thing\n\n## Plan\n\ninputs → worker → Runs\n")
    (task / "scripts" / "worker.py").write_text("print(1)\n")
    (task / "notebooks" / "r01_fit.ipynb").write_text("{}")
    (task / "runs" / "r01_fit" / "run.yaml").write_text("run: r01_fit\nkind: hard\ntype: [fit, evaluate]\nstatus: done\n")
    (task / "runs" / "run-build-t01" / "run.yaml").write_text("run: run-build-t01\nkind: soft\ntype: build\nstatus: open\n")
    return root


class LadderTest(unittest.TestCase):
    def test_a_folder_knows_its_level_its_chain_and_its_theme(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            task = root / "Project/tasks/b01_topic/j01_job/t01_task"
            self.assertEqual(frame.level_of(task), "Task")
            self.assertEqual(sorted(frame.chain(task, root)), ["Block", "Job", "Task"])
            self.assertEqual(frame.theme_of(task, root), "work")          # tasks/ reads as the work theme
            self.assertEqual([r["type"] for r in frame.runs_of(task)], ["fit", "build"])
            tools = root / "Tools" / "blueprints" / "b02_workbench"           # not inside a Project
            tools.mkdir(parents=True)
            (tools / "board.md").write_text("# b02\n")
            self.assertEqual(frame.theme_of(tools, root), "vanilla")



class OptionTest(unittest.TestCase):
    # A theme labels and groups the Job ▾ / Task ▾ options (Theme.option, b12 s32 261008)
    def test_a_theme_labels_and_groups_the_dropdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            job = root / "Project/tasks/b01_topic/j01_job"
            (job / "t02_other").mkdir()
            task = job / "t01_task"
            theme = frame.Theme(option=lambda f: (f"Task · {f.name[:3]}", "steps") if f.name == "t01_task" else None)
            row = frame._level_row(theme, root, task, "Task", "Description")
            self.assertIn('<optgroup label="steps">', row)
            self.assertIn(">Task · t01</option>", row)
            self.assertIn(">t02 · other</option>", row)                # None: the folder's short name
            plain = frame._level_row(frame.VANILLA, root, task, "Task", "Description")
            self.assertNotIn("optgroup", plain)
            self.assertIn('title="t01_task" selected>t01 · task</option>', plain)   # full name on hover


class FillTagTest(unittest.TestCase):
    # a theme's Run name takes the folder's own tag, as the base's buttons do (b17 s32 261008)
    def test_a_placeholder_for_the_folders_level_is_filled(self):
        self.assertEqual(frame.fill_tag("run-plan-<tNN>", Path("x/t01_fit")), "run-plan-t01")
        self.assertEqual(frame.fill_tag("run-face-<jNN>", Path("x/t01_fit")), "run-face-<jNN>")
        self.assertEqual(frame.fill_tag("run-plan-<tNN>", Path("x/Design-A")), "run-plan-<tNN>")

    def test_a_themes_own_view_is_not_shadowed_by_a_page_view(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            task = root / "Project/tasks/b01_topic/j01_job/t01_task"
            out = frame.with_page_views({"Audience Report": frame.Space(subspaces=("Draft", "Report"), open="Draft")},
                                        "Task", task, root, "Draft", {"Description": "Face", "Audience Report": "Report",
                                        "Work Details": "Work", "Runs": "All", "Delivery": "Files"})
            self.assertEqual(out["Audience Report"].subspaces, ("Draft", "Report"))
            self.assertNotIn("page-view", out["Audience Report"].html)

    def test_the_work_themes_draft_shows_its_own_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            task = root / "Project/tasks/b01_topic/j01_job/t01_task"
            (task / "draft").mkdir()
            (task / "draft" / "t01-draft-v1.md").write_text("# plan\n")
            theme = frame.themes()["work"]
            out = frame.spaces_for(theme, "Task", task, root, "Draft")
            self.assertNotIn("page-view", out["Audience Report"].html)
            self.assertIn("t01-draft-v1.md", out["Audience Report"].html)

class LevelPatternTest(unittest.TestCase):
    # A theme names its own Job and Task folders (Theme.level_patterns, b03 261007): a paper's version
    # groups Ba-<desk>-Main and its Sections S-<desk>-<N>-<slug> climb the ladder unrenamed.
    def paper(self, tmp: str) -> Path:
        root = Path(tmp)
        board = root / "Project-X" / "paper" / "Paper-Demo"
        for d in (board / "Ba-Desk-Main" / "S-Desk-Main-1-Intro" / "draft", board / "A1-Story" / "StoryA-x",
                  board / "Ba-Desk-Main" / "notes"):
            d.mkdir(parents=True)
        (board / "board.md").write_text("# Paper\n\ndialect: paper\n")
        (board / "Ba-Desk-Main" / "S-Desk-Main-1-Intro" / "S-Desk-Main-1-Intro.md").write_text("# Intro\n")
        return root

    def test_a_theme_names_its_job_and_task_folders(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.paper(tmp)
            board = root / "Project-X/paper/Paper-Demo"
            group, section = board / "Ba-Desk-Main", board / "Ba-Desk-Main/S-Desk-Main-1-Intro"
            saved = dict(frame._PATTERNS)
            frame._PATTERNS.clear()
            frame._PATTERNS.update({"paper": {"Job": r"^B[a-z]-", "Task": r"^S-"}, "work": {}})
            try:
                self.assertEqual(frame.level_of(board), "Block")
                self.assertEqual(frame.level_of(group), "Job")
                self.assertEqual(frame.level_of(section), "Task")
                self.assertIsNone(frame.level_of(board / "A1-Story"))           # not declared
                self.assertIsNone(frame.level_of(group / "notes"))              # under a Job, not a Section
                self.assertIsNone(frame.level_of(section / "draft"))            # inside a Task
                self.assertEqual(frame.children(board, "Block"), [group])
                self.assertEqual(frame.children(group, "Job"), [section])
                self.assertEqual(frame.chain(section, root), {"Task": section, "Job": group, "Block": board})
                self.assertEqual(frame.theme_of(section, root), "paper")
                page = frame.render(frame.Theme(name="paper", label="Paper"), root, section)
                self.assertIn("S-Desk-Main-1-Intro", page)
                self.assertNotIn('<select disabled aria-label="Task"', page)  # the Task tab is live
            finally:
                frame._PATTERNS.clear()
                frame._PATTERNS.update(saved)

    def test_a_theme_with_no_patterns_reads_as_before(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            (block / "Bz-group").mkdir()
            self.assertIsNone(frame.level_of(block / "Bz-group"))               # the work theme declares none
            self.assertEqual([p.name for p in frame.children(block, "Block")], ["j01_job"])


class PageTaskTest(unittest.TestCase):
    # A Page Task on the frame (frame.page_task_spaces, b03 s13 / b16 s13): the Page's own views, embedded.
    def test_a_page_task_opens_the_pages_views_in_the_six_spaces(self):
        from urllib.parse import parse_qs, urlparse
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            board = root / "Project-X/paper/Paper-Demo"
            section = board / "Ba-Desk-Main/S-Desk-Main-1-Intro"
            (section / "draft" / "records").mkdir(parents=True)
            (board / "board.md").write_text("# Paper\n\ndialect: paper\n")
            (section / "S-Desk-Main-1-Intro.md").write_text("# Intro\n")
            (section / "draft" / "records" / "S-Desk-Main-1-Intro-requirement.md").write_text("V1 · at most 900 words\n")
            spaces = frame.page_task_spaces(section, root)
            self.assertEqual({k: v.subspaces for k, v in spaces.items()}, frame.PAGE_TASK_SUBS)
            src = re.search(r'src="([^"]+)"', spaces["Audience Report"].html).group(1)
            q = parse_qs(urlparse(src.replace("&amp;", "&")).query)
            self.assertEqual(urlparse(src).path, "/_board/draft")
            self.assertEqual((q["path"][0], q["file"][0], q["embed"][0], q["space"][0], q["view"][0]),
                             ("Project-X/paper/Paper-Demo/board.md", "Ba-Desk-Main/S-Desk-Main-1-Intro/S-Desk-Main-1-Intro.md",
                              "1", "bullet", "table"))
            (section / "delivery" / "latex" / "draft-bibliography").mkdir(parents=True)
            (section / "delivery" / "latex" / "S-Desk-Main-1-Intro.tex").write_text("x")
            (section / "delivery" / "latex" / "draft-bibliography" / "S-Desk-Main-1-Intro.bib").write_text("x")
            runs = frame.page_task_spaces(section, root)["Runs"]               # the Page Runs view, embedded (s13)
            self.assertEqual((runs.subspaces, runs.page), ((), True))
            self.assertIn("/_board/runs?", runs.html)
            self.assertIn("embed=1", runs.html)
            deliv = frame.page_task_spaces(section, root)["Delivery"]          # item cards, no third row (s13 1b)
            self.assertEqual((deliv.subspaces, deliv.page), ((), True))
            self.assertIn("<h2>Deliveries</h2>", deliv.html)                    # one card per kind, its result inside
            self.assertIn("📄 LaTeX", deliv.html)
            self.assertIn("S-Desk-Main-1-Intro.pdf is not compiled yet; the piece:", deliv.html)
            self.assertIn("draft-bibliography/S-Desk-Main-1-Intro.bib", deliv.html)
            self.assertIn("not built yet: run Build", deliv.html)                # Word, Web … not built
            self.assertEqual([k["label"] for k in deliv.run_types], ["run-delivery-<target>", "run-check-<page>"])
            self.assertTrue(all(isinstance(x, str) and not x.startswith("[") for k in deliv.run_types for x in k["skills"]))
            merged = frame.spaces_for(frame.Theme(name="paper", spaces=lambda *a: frame.page_task_spaces(section, root)),
                                      "Task", section, root)["Delivery"]
            self.assertEqual((merged.subspaces, [k["label"] for k in merged.run_types]),
                             ((), ["run-delivery-<target>", "run-check-<page>"]))
            self.assertIn("tab=supporting", frame.page_task_spaces(section, root, "Evidence-Supporting")["Work Details"].html)
            self.assertIn("at most 900 words", frame.page_task_spaces(section, root, "Requirement")["Description"].html)
            self.assertIn("-requirement.md", frame.page_task_spaces(section, root, "Records")["Description"].html)
            self.assertIn("No plan yet", frame.page_task_spaces(section, root, "Plan")["Description"].html)
            self.assertEqual(spaces["Description"].html, "")              # Scope: the vanilla face and fields

    def test_a_page_task_reads_in_the_audience_report_and_works_in_work_details(self):
        # b16 s13 Decided 4-5 (JL 261007): Table and Reading carry no run types; Questions asks and
        # answers; each Work Details view has its own run cards; Requirement carries the rubric
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            board = root / "Project-X/paper/Paper-Demo"
            section = board / "Ba-Desk-Main/S-Desk-Main-1-Intro"
            (section / "reports" / "q01_why").mkdir(parents=True)
            (board / "board.md").write_text("# Paper\n\ndialect: paper\n")
            (section / "S-Desk-Main-1-Intro.md").write_text("# Intro\n")
            (section / "reports/q01_why/q01_why.md").write_text("# Why this order?\n\nanswer-status: open\n")
            theme = frame.themes()["paper"]

            def runs(sub, space):
                spaces = json.loads(frame.frame_json(theme, root, section, sub))["spaces"]
                return next(s["run_types"] for s in spaces if s["name"] == space)
            self.assertEqual(runs("Table", "Audience Report"), [])
            self.assertEqual(runs("Reading", "Audience Report"), [])
            page = frame.render(theme, root, section, "Audience Report", "Table")
            self.assertNotIn("read only: its content is changed", page)   # no note in the Runs panel (JL 261008)
            self.assertEqual(runs("Questions", "Audience Report"), ["run-ask-<qNN>", "run-report-<qNN>"])   # named by its Run
            self.assertEqual(runs("Draft-Scratch", "Work Details"),
                             ["run-scratch-<target>", "run-structure-<slug>", "run-<value|display|citation>-<slug>"])
            self.assertEqual(runs("Draft-Revise", "Work Details"),
                             ["run-section-<slug>", "run-paragraph-<slug>", "run-revise-<target>", "run-section-<slug>"])
            self.assertEqual(runs("Evidence-Citation", "Work Details"), ["run-citation-<slug>"])
            self.assertEqual([r.split("-")[:2] for r in runs("Scope", "Description")], [["run", "face"]])
            spaces = frame.spaces_for(theme, "Task", section, root, "Questions")
            self.assertIn("Why this order?", spaces["Audience Report"].html)
            self.assertIn("Rubric", frame.page_task_spaces(section, root, "Requirement")["Description"].html)

    def test_a_theme_may_add_its_own_views_after_the_pages(self):
        # b16 s13 (JL 261007): paper adds Reviews after Table · Reading · Questions; the Space stays the
        # theme's, so the base's extra Page-view tabs do not come back and its run types are kept as set
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            section = root / "Project-X/paper/Paper-Demo/Ba-Desk-Main/S-Desk-Main-1-Intro"
            section.mkdir(parents=True)
            (section.parents[1] / "board.md").write_text("# Paper\n\ndialect: paper\n")
            (section / "S-Desk-Main-1-Intro.md").write_text("# Intro\n")

            def spaces(level, folder, root, sub):
                out = frame.page_task_spaces(folder, root, sub)
                ar = out["Audience Report"]
                out["Audience Report"] = frame.Space(html=ar.html, open=ar.open, run_types=ar.run_types,
                                                     subspaces=ar.subspaces + ("Reviews",))
                return out
            theme = frame.Theme(name="paper", label="Paper", spaces=spaces)
            ar = frame.spaces_for(theme, "Task", section, root)["Audience Report"]
            self.assertEqual(ar.subspaces, frame.PAGE_TASK_SUBS["Audience Report"] + ("Reviews",))
            self.assertEqual(ar.run_types, ())
            self.assertTrue(frame.lays_out_page("Audience Report", ar.subspaces))
            self.assertFalse(frame.lays_out_page("Audience Report", ("Reviews", "Table")))

    def test_the_page_view_embeds_without_its_own_chrome(self):
        from live.outline import EMBED_HTML
        self.assertIn("wb-embed", EMBED_HTML)
        for hidden in (".spaces", ".space-split>.runs-panel", ".draft-mode-switcher", "body>header"):
            self.assertIn(hidden, EMBED_HTML)


class ClaimTest(unittest.TestCase):
    # Theme.claims (261007): a theme reads a Block by what it holds, though its Theme folder names
    # another (a labeling Block with schema.yaml kept in tasks/); a failing check claims nothing.
    def test_a_theme_claims_a_block_by_what_it_holds(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            other = root / "Project/tasks/b02_schema"
            other.mkdir()
            (other / "board.md").write_text("# b02\n\nboard-kind: task-block\n")
            (other / "schema.yaml").write_text("question: placeholder\n")
            claiming = frame.Theme(name="labeling", claims=lambda b: (b / "schema.yaml").is_file())
            broken = frame.Theme(name="broken", claims=lambda b: 1 / 0)
            saved = frame.themes
            frame.themes = lambda: {"vanilla": frame.VANILLA, "broken": broken, "labeling": claiming}
            frame._CLAIMS.clear()
            try:
                self.assertEqual(frame.theme_of(other, root), "labeling")
                self.assertEqual(frame.theme_of(block, root), "work")          # no claim: its Theme folder
            finally:
                frame.themes = saved
                frame._CLAIMS.clear()


class FrameTest(unittest.TestCase):
    def test_every_level_keeps_one_studio_entry_above_the_five_space_buttons(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            for folder in (block, block / "j01_job", block / "j01_job/t01_task"):
                for space in ("Description", "Idea Studio", "Audience Report"):
                    with self.subTest(level=frame.level_of(folder), space=space):
                        page = frame.render(frame.VANILLA, root, folder, space)
                        levels = re.search(r'<nav class="row levels">(.*?)</nav>', page).group(1)
                        spaces = re.search(r'<nav class="row spaces">(.*?)</nav>', page)
                        self.assertEqual(re.findall(r'>([^<]+)</a>', levels)[:2], ["Studio", "Block"])
                        self.assertEqual(levels.count(">Studio</a>"), 1)
                        self.assertNotIn(">Index</a>", levels)
                        self.assertEqual(levels.count("<span class=bar></span>"), 1)
                        self.assertEqual('aria-current="page"' in levels, space == "Idea Studio")
                        work_space = "Description" if space == "Idea Studio" else space
                        self.assertIn(frame._e(frame.href(folder, root, frame.VANILLA, work_space, studio=True)), levels)
                        heading = re.search(r"<header class=page-title>(.*?)</header>", page).group(1)
                        if space == "Idea Studio":
                            self.assertIsNone(spaces)
                            self.assertNotIn('<nav class="row subs">', page)
                            self.assertEqual(levels.count('class="tab on"'), 1)
                            self.assertNotIn('select class="on"', levels)
                            self.assertIn("· Studio ·", heading)
                            self.assertIn("b01", heading)
                            self.assertIn("</span> · Topic", heading)
                            self.assertNotIn("· Job", heading)
                            self.assertNotIn("· Task", heading)
                        else:
                            self.assertIsNotNone(spaces)
                            self.assertNotIn(">Studio</a>", spaces.group(1))
                            self.assertEqual(re.findall(r'>([^<]+)</a>', spaces.group(1)),
                                             ["Report" if name == "Audience Report" else name
                                              for name in frame.SPACE_NAMES if name != "Idea Studio"])
                            self.assertEqual(spaces.group(1).count("<span class=bar></span>"), 3)
                            self.assertIn("Block b01", heading)
                        self.assertIn("j01_job", page)
                        self.assertIn("runs-panel", page)
            studio = self._space(root, block, "Idea Studio")
            self.assertIn('<details class=topic id="topic-s01-flow" data-studio-tags="[]"', studio)  # one closed row per topic
            self.assertIn("decided 1 · open 0 · 0 sessions · feeds", studio)
            self.assertIn('data-src="/_excalidraw/?board=Project%2Ftasks%2Fb01_topic%2Fstudio%2Fs01-flow%2Fflow.excalidraw"',
                          studio)                                            # its canvas loads when opened
            self.assertIn("s02-&lt;topic&gt;", studio)                       # where the next topic goes
            self.assertIn('data-pop="s01-flow · the topic, full size"', studio)  # a topic pops out
            self.assertIn("<dialog id=frame-pop", studio)                    # into the frame's pop-out
            report = self._space(root, block, "Audience Report")
            self.assertIn("What is asked?", report)                          # Logic │ Work │ Report
            self.assertIn("One line that answers it.", report)               # the report's answer line
            self.assertIn(">j01_job</a>", report)                            # the Job that answers it
            self.assertIn("s01-flow ↗", report)                              # the studio topic that feeds it

    def test_studio_tags_are_explicit_shared_and_keep_untyped_topics_visible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            note = block / "studio/s01-flow/s01-flow.md"
            note.write_text(note.read_text() + "\n**Type:** Structure\n**Tags:** UI · ui, Structure | Reading & writing\n")
            untyped = block / "studio/s02-legacy"
            untyped.mkdir()
            (untyped / "s02-legacy.md").write_text("s02 legacy\n====\n")
            self.assertEqual(frame._note_facts(note)["tags"], ["Structure", "UI", "Reading & writing"])
            for folder in (block, block / "j01_job", block / "j01_job/t01_task"):
                with self.subTest(level=frame.level_of(folder)):
                    page = frame.render(frame.VANILLA, root, folder, studio=True)
                    listing = re.search(r"<div class=studio-topics[^>]*>(.*?)</div>", page).group(1)
                    self.assertIn('data-studio-tag="" aria-pressed="false">All <span class=tag-count>2</span>', listing)
                    self.assertIn('data-studio-tag="ui" aria-pressed="false">UI <span class=tag-count>1</span>', listing)
                    self.assertIn('data-studio-tag="__untagged__" aria-pressed="false">Untagged <span class=tag-count>1</span>', listing)
                    self.assertIn('Reading &amp; writing', listing)
                    self.assertIn('id="topic-s02-legacy" data-studio-tags="[]"', listing)
                    self.assertNotRegex(listing, r'<details[^>]*\bhidden')
                    self.assertNotIn('<nav class="row spaces">', page)

    def test_vanilla_runs_are_grouped_by_type_in_the_third_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            task = root / "Project/tasks/b01_topic/j01_job/t01_task"
            data = json.loads(frame.frame_json(frame.VANILLA, root, task))
            runs = next(s for s in data["spaces"] if s["name"] == "Runs")
            self.assertEqual(runs["subspaces"], ["All", "build", "fit", "Page Runs"])
            page = frame.render(frame.VANILLA, root, task, "Runs", "build")
            shown = page.split("<section class=runs-panel", 1)[0]          # the Space, not the Disk list
            self.assertIn("run-build-t01", shown)
            self.assertNotIn("r01_fit/", shown)

    def test_a_theme_fills_only_what_differs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            task = root / "Project/tasks/b01_topic/j01_job/t01_task"
            work = frame.themes()["work"]
            data = json.loads(frame.frame_json(work, root, task))
            by = {s["name"]: s for s in data["spaces"]}
            self.assertEqual(by["Work Details"]["subspaces"], ["Code", "Review", "Notebooks", "Evidence", "Value"])
            self.assertEqual(by["Audience Report"]["subspaces"], ["Draft", "Report"])
            self.assertEqual(by["Runs"]["subspaces"], ["All", "build", "fit", "Page Runs"])   # the frame's own grouping
            self.assertIn("worker.py", frame.render(work, root, task, "Work Details", "Code"))
            self.assertIn("inputs → worker", frame.render(work, root, task, "Description", "Plan"))
            block = json.loads(frame.frame_json(work, root, root / "Project/tasks/b01_topic"))
            self.assertEqual([s["name"] for s in block["spaces"]], list(frame.SPACE_NAMES))

    def test_the_block_list_skips_a_link_that_leaves_the_root(self):
        from live.frame_view import _blocks
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as away:
            root = project(tmp)
            outside = Path(away) / "blueprints" / "b01_utils"     # a Tools checkout beside the SPACE
            outside.mkdir(parents=True)
            (outside / "board.md").write_text("# b01 · Utils\n\nboard-kind: task-block\n")
            (root / "Tools").symlink_to(Path(away), target_is_directory=True)
            found = [frame._rel(b, root) for b in _blocks(root)]    # _rel raised on the outside Block
            self.assertEqual(found, ["Project/tasks/b01_topic"])

    def test_studio_uses_the_block_topics_disk_sessions_and_new_run_target_at_every_level(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            job, task = block / "j01_job", block / "j01_job/t01_task"
            for folder in (job, task):
                topic = folder / "studio/s99-local"
                topic.mkdir(parents=True)
                (topic / "local.excalidraw").write_text("{}")
                (topic / "s99-local.md").write_text("s99 local\n====\n")
            run = block / "runs/run-draw-s01"
            (run / "passes/p01-1010").mkdir(parents=True)
            (run / "run.yaml").write_text("run: run-draw-s01\nkind: soft\ntype: draw\nstatus: done\ntarget: s01-flow\n")
            for folder in (block, job, task):
                with self.subTest(level=frame.level_of(folder)):
                    page = frame.render(frame.VANILLA, root, folder, "Idea Studio")
                    self.assertIn('data-owner="Project/tasks/b01_topic"', page)
                    self.assertIn('board=Project%2Ftasks%2Fb01_topic%2Fstudio%2Fs01-flow%2Fflow.excalidraw', page)
                    self.assertIn('id="topic-j01_job--s99-local"', page)
                    self.assertIn('id="topic-j01_job--t01_task--s99-local"', page)
                    disk_heading = re.search(r"<p class=disk-head>(.*?)</p>", page).group(1)
                    self.assertIn("b01_topic/", disk_heading)
                    self.assertNotIn("j01_job", disk_heading)
                    self.assertNotIn("t01_task", disk_heading)
                    self.assertIn("run-draw-s01", page)
                    self.assertIn("/haipipe-studio a topic of Project/tasks/b01_topic:", page)
                    self.assertNotIn("/haipipe-studio a topic of Project/tasks/b01_topic/j01_job:", page)

    def test_current_groups_keep_repeated_local_topics_distinct_and_skip_external_links(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as away:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            job, task = block / "j01_job", block / "j01_job/t01_task"
            for folder in (job, task):
                topic = folder / "studio/s01-flow"
                topic.mkdir(parents=True)
                (topic / "s01-flow.md").write_text("s01 local\n====\n\n**Feeds:** q01_ask\n")
                (topic / "flow.excalidraw").write_text("{}")
            report = job / "reports/q01_ask/q01_ask.md"
            report.parent.mkdir(parents=True)
            report.write_text("# Job's question\n")
            (job / "studio/s02-alias").symlink_to(block / "studio/s01-flow", target_is_directory=True)
            outside = Path(away) / "j99_private/studio/s99-secret"
            outside.mkdir(parents=True)
            (outside / "secret.excalidraw").write_text("{}")
            (block / "j99_private").symlink_to(outside.parent.parent, target_is_directory=True)
            (block / "studio/s99-external").symlink_to(outside, target_is_directory=True)
            old = block / "_archive/j98_old/studio/s98-old"
            old.mkdir(parents=True)
            inventory = frame.studio_inventory(block, root)
            self.assertEqual([source for source, _, _ in inventory], [p.resolve() for p in (block, job, task)])
            pages = [frame.render(frame.VANILLA, root, f, studio=True) for f in (block, job, task)]
            for page in pages:
                ids = re.findall(r'<details class=topic id="([^"]+)" data-studio-tags', page)
                self.assertEqual(ids, ["topic-s01-flow", "topic-j01_job--s01-flow", "topic-j01_job--t01_task--s01-flow"])
                listing = re.search(r'<div class=studio-topics[^>]*>(.*?)</div>', page).group(1)
                for name in ("s99-secret", "s99-external", "s02-alias", "s98-old"):
                    self.assertNotIn(name, listing)
                groups = re.findall(r'data-studio-tag="([^"]*)"', listing)
                self.assertEqual((groups[0], groups[-1]), ("__current__", ""))
                self.assertIn('data-studio-key="j01_job/studio/s01-flow"', page)
                local = re.search(r'<details class=topic id="topic-j01_job--s01-flow"(.*?)</details>', page).group(1)
                self.assertIn("j01_job%2Freports%2Fq01_ask", local)
                self.assertIn("s02-&lt;topic&gt;", page)  # old local numbers don't allocate new Block numbers

    def test_a_themes_studio_is_also_shared_from_its_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            task = root / "Project/tasks/b01_topic/j01_job/t01_task"
            theme = frame.Theme(spaces=lambda level, folder, root, sub: {
                "Idea Studio": frame.Space(f'<p>Studio source: {folder.name}</p>')})
            page = frame.render(theme, root, task, "Idea Studio")
            self.assertIn("Studio source: b01_topic", page)
            self.assertNotIn("Studio source: t01_task", page)
            self.assertIn("Studio source: b01_topic", frame.spaces_for(theme, "Task", task, root)["Idea Studio"].html)

    @staticmethod
    def _space(root, folder, space):
        return frame.render(frame.VANILLA, root, folder, space)


class BandTest(unittest.TestCase):
    def test_the_page_has_no_band_and_no_old_page_link(self):
        # JL 261007: "why I still have this? please remove that": the level tabs say where you are;
        # the path is the title's tooltip
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            page = frame.render(frame.themes()["work"], root, root / "Project/tasks/b01_topic")
            self.assertNotIn("class=band", page)
            self.assertNotIn("the old page", page)
            self.assertIn('<h1 title="Block · Project/tasks/b01_topic · Work theme · b01_topic" data-guide="📋 Work · Guide · Block b01">', page)
            # the level row is the page index, the page's title under it (b03 s32-D13, JL 261008)
            self.assertLess(page.index('<nav class="row levels">'), page.index("<header class=page-title>"))
            self.assertIn("<span class=lv>Block b01 ·</span> Topic</h1>", page)   # its tag said once


class StyleTest(unittest.TestCase):
    # JL 261007, "base styles only": the frame carries the base's shared view styles (a theme's Spaces
    # may use their classes) and no theme's own look; those styles never restyle the frame itself.
    def test_the_frame_carries_the_base_view_styles_and_they_leave_its_chrome_alone(self):
        import re
        from live.space_views import SPACE_VIEW_CSS
        from live.work_items import WORK_ITEM_CSS
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            page = frame.render(frame.themes()["work"], root, root / "Project/tasks/b01_topic")
            self.assertIn(SPACE_VIEW_CSS, page)
            self.assertIn(WORK_ITEM_CSS, page)
            for rule in (".st-ok{", ".st-warn{", ".topic.missing{"):      # base status and missing-card marks
                self.assertIn(rule, page)
        chrome = {"tab", "row", "band", "levels", "spaces", "bar", "subs", "split", "space-main", "runs-panel",
                  "topic", "q-row", "chip", "wf-table", "frame-body"}
        for css in (SPACE_VIEW_CSS, WORK_ITEM_CSS):
            css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
            for selector in re.findall(r"([^{}]+)\{", css):
                for part in selector.split(","):
                    first = part.strip().split()[0] if part.strip() else ""
                    with self.subTest(selector=part.strip()):
                        self.assertFalse(first.startswith(("body", "html", ":root")), part)
                        self.assertNotIn(first.split(":")[0].lstrip("."), chrome, part)


    def test_a_tasks_page_views_are_subspaces_drawn_in_place(self):
        # the old Page workbench's routes, one page per tab, are the Task's Spaces now (JL 261007)
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            task = root / "Project/tasks/b01_topic/j01_job/t01_task"
            data = json.loads(frame.frame_json(frame.VANILLA, root, task))
            by = {s["name"]: s["subspaces"] for s in data["spaces"]}
            self.assertEqual(by["Description"], ["Face", "Folder"])
            self.assertEqual(by["Work Details"], ["Folders", "Evidence", "Value"])
            self.assertEqual(by["Delivery"], ["Files", "Lanes"])
            page = frame.render(frame.VANILLA, root, task, "Work Details", "Evidence")
            self.assertIn('class=page-view src="/_board/workbench?view=evidence&amp;path=Project%2Ftasks', page)
            block = json.loads(frame.frame_json(frame.VANILLA, root, root / "Project/tasks/b01_topic"))
            self.assertNotIn("Evidence", {x for s in block["spaces"] for x in s["subspaces"]})   # a Block has none


    def test_the_disk_box_names_the_files_behind_the_open_space(self):
        # JL 261007: "add the disks as well ... so we have both disks and runs"
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            page = frame.render(frame.VANILLA, root, block, "Audience Report")
            self.assertIn("<div class=runs-body><div class=disk-in>", page)   # inside the Runs panel, first: one fold
            self.assertIn("<span>Report: the title and its answer line</span>", page)         # a group, one row per file
            self.assertIn("## Questions: one row per Question", page)
            work = frame.render(frame.VANILLA, root, block, "Work Details")
            self.assertIn('<span class=disk-p>j01_job/</span>', work)                          # the Block's one Job, a row
            missing = frame.disk_markup((("nothing-here/", "what it would feed"),), block, root)
            self.assertIn("<li class=miss", missing)                                           # greyed: not there yet
            self.assertIn("<span class=disk-n>not yet</span>", missing)
            task = root / "Project/tasks/b01_topic/j01_job/t01_task"
            runs = frame.render(frame.VANILLA, root, task, "Runs", "Page Runs")
            self.assertIn("the Page&#x27;s Runs: planned, registered, done", runs)               # the open Page view's own


class ButtonSkillTest(unittest.TestCase):
    """Every Run button the frame draws names its owning skill, and that skill exists (b03 s21-D02;
    haipipe-run ref/run-types-by-space.md)."""

    def buttons(self, root):
        block = root / "Project" / "tasks" / "b01_topic"
        task = block / "j01_job" / "t01_task"
        for level, folder in (("Block", block), ("Job", block / "j01_job"), ("Task", task)):
            for space, view in frame.spaces_for(frame.VANILLA, level, folder, root).items():
                for k in view.run_types:
                    yield level, space, k
        for space, subs in frame.PAGE_TASK_SUBS.items():
            for sub in subs or ("",):
                for k in frame.page_task_spaces(task, root, sub)[space].run_types:
                    yield "Page Task", space + " " + sub, k

    def test_every_button_names_a_skill_that_exists(self):
        skills = Path(frame.__file__).resolve().parents[2] / "skills"
        names = {p.parent.name for p in skills.glob("**/SKILL.md")}
        with tempfile.TemporaryDirectory() as tmp:
            seen = list(self.buttons(project(tmp)))
        self.assertGreater(len(seen), 30)
        for level, space, k in seen:
            self.assertTrue(k.get("skills"), f"{level} · {space} · {k['label']} names no skill")
            for s in k["skills"]:
                self.assertIn(s, names, f"{level} · {space} · {k['label']}: no skill {s}")

    def test_the_level_owns_its_own_buttons(self):
        with tempfile.TemporaryDirectory() as tmp:
            # a button is named by its soft Run, `run-<type>-<target>`, what it does under it (JL 261007)
            buttons = list(self.buttons(project(tmp)))
            seen = {(level, k.get("doing") or k["label"]): k["skills"] for level, _, k in buttons}
        self.assertTrue(all(k["label"].startswith(("run-", "rNN_")) for _, _, k in buttons),
                        [k["label"] for _, _, k in buttons if not k["label"].startswith(("run-", "rNN_"))])
        self.assertEqual(seen[("Block", "add a Job")], ["haipipe-board"])
        self.assertEqual(seen[("Job", "add a Task")], ["haipipe-job"])
        self.assertEqual(seen[("Task", "build the Task")], ["haipipe-task"])
        self.assertEqual(seen[("Job", "write the report")], ["haipipe-report"])
        self.assertEqual(seen[("Block", "add a topic · redraw it · save this session, each a pass")], ["haipipe-studio"])


class RouteTest(unittest.TestCase):
    def _get(self, root, path):
        sent = {}

        class Fake(FrameMixin):
            def guide_send(self, body, code=200, content_type="text/html", head_only=False):
                sent.update(body=body, code=code, type=content_type)

            def runs_view(self, head_only=False):
                sent.update(view="runs", path=self.path)
        handler = Fake()
        handler.root, handler.path = str(root), path
        handler.workbench_frame_view()
        return sent

    def test_the_route_lists_blocks_opens_a_folder_in_its_theme_and_refuses_outside_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            self.assertIn("Project/tasks/b01_topic", self._get(root, "/_board/workbench")["body"])
            sent = self._get(root, "/_board/workbench?path=Project/tasks/b01_topic/j01_job/t01_task&space=Work+Details")
            self.assertEqual(sent["code"], 200)
            self.assertIn("📋 Work", sent["body"])
            self.assertIn("Notebooks", sent["body"])
            self.assertEqual(self._get(root, "/_board/workbench?path=../../etc")["code"], 404)
            data = json.loads(self._get(root, "/_board/workbench?path=Project/tasks/b01_topic&format=json")["body"])
            self.assertEqual(data["theme"], "work")
            self.assertEqual(data["level"], "Block")

    def test_studio_preserves_the_task_and_work_view_for_return(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            original = "/_board/workbench?path=Project/tasks/b01_topic/j01_job/t01_task&space=Work+Details&sub=Code"
            page = self._get(root, original)["body"]
            studio_url = unescape(re.search(r'<a class="tab" href="([^"]+)"[^>]*>Studio</a>', page).group(1))
            query = parse_qs(urlparse(studio_url).query)
            self.assertEqual(query["studio"], ["1"])
            self.assertEqual(query["space"], ["Work Details"])
            self.assertEqual(query["sub"], ["Code"])
            studio = self._get(root, studio_url)["body"]
            self.assertNotIn('<nav class="row spaces">', studio)
            self.assertIn('data-owner="Project/tasks/b01_topic"', studio)
            back = unescape(re.search(r'<a class=tab href="([^"]+)" title="t01_task">', studio).group(1))
            self.assertNotIn("studio", parse_qs(urlparse(back).query))
            restored = self._get(root, back)["body"]
            self.assertIn('<nav class="row spaces">', restored)
            self.assertIn("worker.py", restored)
            self.assertIn('class="tab on"', restored)

    def test_view_draws_one_page_task_view_from_the_same_query(self):
        with tempfile.TemporaryDirectory() as tmp:
            sent = self._get(project(tmp), "/_board/workbench?view=runs&path=P/t01.md&run=r01")
            self.assertEqual(sent["view"], "runs")
            self.assertEqual(sent["path"], "/_board/workbench?path=P%2Ft01.md&run=r01")   # view= left out


if __name__ == "__main__":
    unittest.main()
