"""The paper theme on the base frame (paper_theme.py): a paper Board opens as the Paper theme, every
Space and third-row choice renders, and a Section folder is left to the base. Placeholders only: the
Board is written into a temp folder, never a real paper."""
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

BOARD = """# Paper-Demo: does <a placeholder> change <an outcome>?

board-kind: paper-board

## Pages

### A1 · A1-Story
Story00-ideation.md
StoryA-desk-idea.md

### Ba · Ba-desk-Main
S-desk-Main-1-Introduction.md
"""
SECTION = """# S-desk-Main-1-Introduction · §1 Introduction

page-type: section
section_kind: introduction
reader-question: <the one question this Section answers>
must-establish: C1

## Content

#### P1. <the job of paragraph one>
<sentence one> \\citep{a2020,b2021}
<sentence two>

#### P2. <the job of paragraph two>
<sentence three> \\citep{c2022}
"""
ROUND = """# RD01-demo

## Review Items

| item | cites | lands on | work | reply | state |
|---|---|---|---|---|---|
| Review-demo-claim | R1.1 · E1.2 | S-desk-Main-1-Introduction ¶2 · C1 | run-revise-demo-claim | P3 | answered |
| Review-other-page | R2.1 | S-desk-Main-2-Methods ¶1 | — | — | open |
"""
SUBS = {"Description": ("Scope", "Venue", "Resources"), "Related": ("",), "Idea Studio": ("",),
        "Audience Report": ("Ideation", "Narrative", "High-level logic + Low-level work", "Related Questions",
                            "Related Papers"),
        "Work Details": ("Idea", "Story", "DataFlow", "PaperFlow", "Jobs"), "Runs": ("",),
        "Delivery": ("delivery/", "LaTeX", "Word", "Cover letter", "Rounds")}


class PaperThemeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.board = self.root / "examples-demo" / "Project-Demo" / "papers" / "Paper-Demo"
        (self.board / "A1-Story" / "Story00-ideation").mkdir(parents=True)
        (self.board / "Ba-desk-Main" / "S-desk-Main-1-Introduction").mkdir(parents=True)
        (self.board / "board.md").write_text(BOARD, encoding="utf-8")
        (self.board.parents[1] / "project.yaml").write_text("name: Demo\n", encoding="utf-8")
        self.theme = frame.themes()["paper"]

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_paper_board_opens_in_the_paper_theme(self):
        self.assertEqual(frame.theme_of(self.board, self.root), "paper")
        self.assertEqual(self.theme.level_name("Block"), "Paper Board")

    def test_every_space_and_choice_renders(self):
        for space, subs in SUBS.items():
            for sub in subs:
                with self.subTest(space=space, sub=sub):
                    page = frame.render(self.theme, self.root, self.board, space, sub)
                    self.assertIn("Paper theme", page)

    def test_the_block_spaces_carry_the_paper_views(self):
        spaces = {s["name"]: s for s in json.loads(frame.frame_json(self.theme, self.root, self.board))["spaces"]}
        for space, subs in SUBS.items():
            if subs != ("",):
                self.assertEqual(tuple(spaces[space]["subspaces"]), subs)
        self.assertTrue(spaces["Runs"]["run_types"])

    def test_the_board_work_is_its_steps_then_its_jobs(self):
        # JL 261020: "Like in the work, we might also have ... the Idea, and then the Story, and DataFlow, and PaperFlow
        # ... and later we can have many Jobs": each step reads its Studio group's topic, Operation over Result
        from live.paper_theme import spaces
        story = self.board / "studio" / "s02-story-demo"
        story.mkdir(parents=True)
        (story / "s02-story-demo.md").write_text(
            "s02 · the story\n\n**Tags:** `Story`\n\n**Stage:** explore\n\n**Topic:** one telling of the paper. More.\n\n"
            "Decided\n-------\n\n- s02-D01 · three questions (JL 261020)\n\nOpen\n----\n\n1. Which venue first?\n",
            encoding="utf-8")
        (story / "s02-story-demo.excalidraw").write_text("{}", encoding="utf-8")
        work = spaces("Block", self.board, self.root, "Story")["Work Details"]
        self.assertEqual((work.open, work.subspaces), ("Story", ("Idea", "Story", "DataFlow", "PaperFlow", "Jobs")))
        for needle in ("Operation", "Result", "📖 Story", "/haipipe-paper story", "studio/s02-story-demo",
                       "one telling of the paper.", "s02-story-demo.excalidraw", "🙋 Open · 1", "Which venue first?",
                       "✅ Decided · 1", "🔶 asked"):
            self.assertIn(needle, work.html)
        self.assertNotIn("More.", work.html)
        idea = spaces("Block", self.board, self.root, "Idea")["Work Details"]
        self.assertIn("none yet in the Ideation group", idea.html)
        self.assertIn("/haipipe-paper ideate", idea.html)
        # a bare link opens the first step with no topic yet; an old tab name opens Jobs
        self.assertEqual(spaces("Block", self.board, self.root, "")["Work Details"].open, "Idea")
        self.assertEqual(spaces("Block", self.board, self.root, "Evidence")["Work Details"].open, "Jobs")

    def test_a_story_reads_as_sections_and_an_idea_as_a_card(self):
        # JL 261020: "is there a way to show each idea as a card and we can review them? ... Make it very easy to read";
        # "we want to do the same to the story as well ... make the topics here into different section in the results"
        from live.paper_theme import _idea_card, _story_sections
        face = ("### 1 · Identity\n\n**One sentence**: we ask one thing.\n\n### 2 · Pitch\n\n"
                "1. **Tension**: patients ask agents.\n2. **Who cares**: patients.\n\n### 3 · Research Questions\n\n"
                "**The paper's question**: Which doctors do patients see?\n\n"
                "**The narrative, if the questions are answered** (what it can say):\n\n1. Agents name real doctors (RQ1).\n\n"
                "#### 3.1 · Question 1 · RQ1\n- **Name**: Real doctors?\n- **Research question**: Are they real? (RQ1a: how many?)\n"
                "- **Question**: We match names. Then more.\n- **Answer state**: 🔶 measured. Then more.\n\n**Hypotheses**\n"
                "- **1a** · Mostly real: most are real · tested by Ework02\n\n**Potential claims**\n"
                "- **1a** · C1 · from 1a · Real: the names are real.\n  - **Role**: boundary\n\n**Potential work**\n- **T1** · for 1a\n\n"
                "### 5 · Evidence Basis and Boundaries\n\n| E | evidence | source | state |\n|---|---|---|---|\n"
                "| Ework02 | names match | b03 | established |\n\n**We will not claim**:\n- that named is better;\n- a cause.\n")
        html = _story_sections(face)
        # laid out as the drawing (JL 261020: "让它的 layout 跟我们 draw 里面长得比较相似一些"), every card folded
        # ("可以把它们也都变成闭合的吗"): the question in the key box, a research question's row in three columns
        for needle in ("📖 The paper's question", "Which doctors do patients see?", "we ask one thing.", "Tension",
                       "RQ1 · Real doctors?", "🔶", "Are they real?", "We match names.",
                       "❓ The question →", "🔮 What we expect, and why →", "📣 What the paper can say",
                       "1 hypothesis: 1 with evidence in hand, 0 waiting for a Run", "✅ 1a · Mostly real", "most are real",
                       "tested by Ework02", "C1 · Real", "the names are real.", "Work: T1",
                       "📜 The narrative", "Agents name real doctors (RQ1).", "🚫 What we will not claim", "that named is better;",
                       "🧾 The evidence", "Ework02"):
            self.assertIn(needle, html)
        # quiet (JL 261020: "看起来太咋咋呼呼了，就没有重点"): no yellow key box, no box inside a card, no headings over rows
        for gone in ("RQ1a", "Then more.", "Role", "<details class=\"topic work-task\" open", "#ffd43b", "border:1px solid",
                     "❓ The research questions"):
            self.assertNotIn(gone, html)
        card = _idea_card({"id": "i13", "title": "Who gets named?", "verdict": "⬜ open",
                           "fields": [("novelty", "⬜ unverified (cross-model check only)"), ("verdict", "⬜ open")],
                           "substance": [("Hypothesis", ["the premium sits in reading answers. More words."]),
                                         ("Recommendation", ["test-ready; pick 1 of 3."])]})
        for needle in ('id="idea-i13"', "<b>i13 · Who gets named?</b>", "the premium sits in reading answers.",
                       "novelty ⬜ unverified", "test-ready", '<details class="topic work-task"'):
            self.assertIn(needle, card)
        drawn = _idea_card({"id": "i13", "title": "Who gets named?", "fields": [], "substance": []},
                           {"short": "Does it repeat the sites?", "why": "The sites would decide.", "data": ["answers"],
                            "method": ["tag each URL"], "results": [{"find": "the gap only where read", "means": "it re-presents"}],
                            "now": "pilot pending"})
        for needle in ("i13 · Does it repeat the sites?", "Why it matters", "The sites would decide.", ">Data<",
                       "1. tag each URL", "If we find", "the gap only where read", "it re-presents", "pilot pending"):
            self.assertIn(needle, drawn)
        self.assertNotIn("More words.", card)
        self.assertNotIn("cross-model check only", card)

    def test_related_folds_inside_the_studio(self):
        # b10 s04, JL 261011: Related is the Studio's second folding part; a Related link, or an old
        # Description › Related one, opens the Studio with it unfolded
        page = frame.render(self.theme, self.root, self.board, "Related")
        self.assertIn('aria-current="page">Studio</a>', page)
        self.assertNotIn(">Related</a>", page.split("<header")[0])
        self.assertIn("<details class=studio-related id=studio-related open>", page)
        self.assertIn("run-add-related-", page)
        old = frame.render(self.theme, self.root, self.board, "Description", "Related")
        self.assertIn("<details class=studio-related id=studio-related open>", old)

    def test_related_papers_by_each_question_and_no_email(self):
        # b10 s04-D07, D09: a group cell is comma-separated, and an email is no related work; the subfolder
        # (emails/, meetings/) is the Studio's group, never a research question
        (self.board / "related" / "emails").mkdir(parents=True)
        (self.board / "related" / "related.md").write_text(
            "| kind | date | item | link | feeds | group |\n|---|---|---|---|---|---|\n"
            "| paper | 2024 | <paper-a> | https://doi.org/x | q01 | RQ1, RQ2 |\n"
            "| email | 2026-10-09 | <email-b> | `emails/2026-10-09-0900 b.eml` | q01 | RQ1 |\n"
            "| meeting | 2026-10-10 | <meeting-c> | `meetings/2026-10-10-1800 c.md` | s01 | |\n", encoding="utf-8")
        page = frame.render(self.theme, self.root, self.board, "Audience Report", "Related Papers")
        body = page.split("<h3>RQ1</h3>")[1]
        self.assertIn("&lt;paper-a&gt;", body.split("<h3>RQ2</h3>")[0])
        self.assertIn("&lt;paper-a&gt;", body.split("<h3>RQ2</h3>")[1])
        self.assertNotIn("&lt;email-b&gt;", page)
        self.assertNotIn("<h3>emails</h3>", page)

    def test_related_papers_by_bears_on_when_the_table_has_it(self):
        # JL 261013: the Studio groups related items by kind, so what a paper bears on has its own column
        (self.board / "related").mkdir(parents=True, exist_ok=True)
        (self.board / "related" / "related.md").write_text(
            "| kind | date | item | link | feeds | group | bears on |\n|---|---|---|---|---|---|---|\n"
            "| paper | 2024 | <paper-a> | https://doi.org/x | s01 |  | Closest: LLMs, i02 Guardrail |\n", encoding="utf-8")
        page = frame.render(self.theme, self.root, self.board, "Audience Report", "Related Papers")
        self.assertIn("<h3>Closest: LLMs</h3>", page)
        self.assertIn("<h3>i02 Guardrail</h3>", page)
        self.assertNotIn("<h3>paper</h3>", page)

    def test_a_related_paper_links_its_deep_read_in_one_folder_per_run(self):
        # a Discovery Paper Run keeps its Result at runs/<run>/result/, its files named by the Run, not result
        run = "r01_demo2026_paper"
        result = (self.board.parents[1] / "discovery" / "b01_demo_board" / "j01_demo_job" / "t01_demo_task"
                  / "runs" / run / "result")
        result.mkdir(parents=True)
        (result / f"{run}.md").write_text("# demo card\n", encoding="utf-8")
        (self.board / "related").mkdir()
        (self.board / "related" / "related.md").write_text(
            "| kind | date | item | link | feeds | group | read |\n|---|---|---|---|---|---|---|\n"
            "| paper | 2026 | <paper-a> | https://doi.org/x | s01 | RQ1 | b01.j01.t01.r01 |\n", encoding="utf-8")
        page = frame.render(self.theme, self.root, self.board, "Audience Report", "Related Papers")
        self.assertIn("read r01 ↗", page)
        self.assertNotIn("no deep read yet", page)

    def test_a_section_folder_is_left_to_the_base(self):
        # a Section is a Page Task: its Spaces are the base's Page Task views (task_draft.draft_task_spaces,
        # b16 s13), which the paper's own lines will go over
        from live.task_draft import DRAFT_TASK_SUBS, draft_task_spaces
        from live.paper_theme import spaces
        section = self.board / "Ba-desk-Main" / "S-desk-Main-1-Introduction"
        got = spaces("Task", section, self.root, "")
        want = dict(DRAFT_TASK_SUBS, **{"Audience Report": DRAFT_TASK_SUBS["Audience Report"] + ("Comments",)})
        self.assertEqual({k: v.subspaces for k, v in got.items()}, want)
        reviews = spaces("Task", section, self.root, "Comments")["Audience Report"]
        self.assertEqual((reviews.open, reviews.run_types), ("Comments", ()))
        self.assertIn("No Review Items yet", reviews.html)
        rd = self.board / "Bc-desk-Round" / "RD01-demo"
        rd.mkdir(parents=True)
        (rd / "RD01-demo.md").write_text(ROUND, encoding="utf-8")
        reviews = spaces("Task", section, self.root, "Comments")["Audience Report"].html
        self.assertIn("Review-demo-claim", reviews)
        self.assertIn("run-revise-demo-claim", reviews)
        self.assertNotIn("Review-other-page", reviews)
        base = draft_task_spaces(section, self.root, "")
        for name in ("Work Details",):                                # the paper adds nothing here
            self.assertEqual(got[name], base[name])

    def test_a_section_carries_the_paper_lines(self):
        # ◆ (b16 s13): the reader contract in Scope, the SUB-* rows beside the Requirement in Work › 1 · Plan
        # (b32 s41 Ⓐ), the form over the Table, and "ready for the build" apart from "done" in Delivery
        from live.paper_theme import spaces
        section = self.board / "Ba-desk-Main" / "S-desk-Main-1-Introduction"
        (section / "S-desk-Main-1-Introduction.md").write_text(SECTION, encoding="utf-8")
        unit = section / "results" / "run-display-0101-demo" / "payload" / "Display1-demo"
        unit.mkdir(parents=True)
        scope = spaces("Task", section, self.root, "Scope")["Description"].html
        self.assertIn("The reader contract", scope)
        self.assertIn("&lt;the one question this Section answers&gt;", scope)
        self.assertIn("SUB-INTRO-01", spaces("Task", section, self.root, "1 · Plan")["Work Details"].html)
        evidence = spaces("Task", section, self.root, "3 · Evidence")["Work Details"].html
        self.assertIn("/haipipe-paper-evidence ", evidence)                  # the paper's rules on its Sections
        self.assertNotIn("/haipipe-evidence ", evidence)
        self.assertNotIn("◆ form", spaces("Task", section, self.root, "Table")["Audience Report"].html)
        delivery = spaces("Task", section, self.root, "LaTeX")["Delivery"].html
        self.assertIn("displays with preview.pdf: 0 of 1", delivery)
        self.assertIn("no Page CHECK yet", delivery)
        self.assertIn("◆ Ready", delivery)
        (unit / "preview.pdf").write_bytes(b"%PDF-")
        self.assertIn("1 of 1", spaces("Task", section, self.root, "Word")["Delivery"].html)
        latex = section / "delivery" / "latex"
        latex.mkdir(parents=True)
        (latex / "S-desk-Main-1-Introduction.tex").write_text("\\section{Introduction}", encoding="utf-8")
        html = spaces("Task", section, self.root, "")["Delivery"].html
        self.assertIn("Deliveries", html)
        self.assertIn("is not compiled yet", html)                 # no PDF: the piece itself
        (latex / "S-desk-Main-1-Introduction.pdf").write_bytes(b"%PDF-")
        self.assertIn("<iframe", spaces("Task", section, self.root, "")["Delivery"].html)


LADDER_BOARD = """# Paper-Demo: does <a placeholder> change <an outcome>?

board-kind: paper-board
story-current: StoryA-desk-idea

## Pages

### J00 · j00_story
Story00-ideation.md
StoryA-desk-idea.md

### J01 · j01_v1_desk
S-desk-Main-1-Introduction.md
S-desk-Appendix-A-Data.md
RD01-demo.md
"""
FACE = """# j01_v1_desk · version 1 for <a venue>

send: j01_v1_desk
desk: desk
venue: <a venue>
state: drafting
tells: j00_story/StoryA-desk-idea

## Questions
"""


class LayoutsTest(unittest.TestCase):
    """g03: one placeholder Board in each layout (today's groups, and the ladder's j00_story · j01_v1_<desk>);
    every level and every third-row choice renders in both."""

    def _board(self, ladder):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        board = root / "examples-demo" / "Project-Demo" / "papers" / "Paper-Demo"
        story, main, appx, rnd = (("j00_story", "j01_v1_desk", "j01_v1_desk", "j01_v1_desk") if ladder else
                                  ("A1-Story", "Ba-desk-Main", "Bb-desk-Appendix", "Bc-desk-Round"))
        folders = {"story": board / story, "ideation": board / story / "Story00-ideation",
                   "storypage": board / story / "StoryA-desk-idea",
                   "section": board / main / "S-desk-Main-1-Introduction",
                   "appendix": board / appx / "S-desk-Appendix-A-Data", "round": board / rnd / "RD01-demo",
                   "version": board / main}
        for k in ("ideation", "storypage", "section", "appendix", "round"):
            folders[k].mkdir(parents=True)
        (folders["round"] / "RD01-demo.md").write_text(ROUND, encoding="utf-8")
        (folders["section"] / "S-desk-Main-1-Introduction.md").write_text(SECTION, encoding="utf-8")
        (folders["appendix"] / "S-desk-Appendix-A-Data.md").write_text("# S-desk-Appendix-A-Data\n", encoding="utf-8")
        (folders["storypage"] / "StoryA-desk-idea.md").write_text("# StoryA-desk-idea\n\nstate: 🟡 draft\n",
                                                                  encoding="utf-8")
        if ladder:
            (board / "board.md").write_text(LADDER_BOARD, encoding="utf-8")
            (folders["version"] / "j01_v1_desk.md").write_text(FACE, encoding="utf-8")
            (board / "delivery" / main).mkdir(parents=True)     # a version's build is the Board's (b10 s03-D01)
        else:
            (board / "board.md").write_text(BOARD.replace("### Ba", "### Bb · Bb-desk-Appendix\n- S-desk-Appendix-A-Data\n\n"
                                                          "### Bc · Bc-desk-Round\n- RD01-demo\n\n### Ba"),
                                            encoding="utf-8")
        (board.parents[1] / "project.yaml").write_text("name: Demo\n", encoding="utf-8")
        return root, board, folders

    def test_every_level_and_choice_renders_in_both_layouts(self):
        from live.paper_theme import spaces
        theme = frame.themes()["paper"]
        want = {"Block": "board", "story": "Job", "version": "Job", "section": "Task", "appendix": "Task",
                "round": "Task", "ideation": "Task", "storypage": "Task"}
        for ladder in (False, True):
            root, board, f = self._board(ladder)
            f["board"] = board
            for key, level in want.items():
                folder = f["board" if key == "Block" else key]
                level = "Block" if key == "Block" else level
                with self.subTest(ladder=ladder, folder=key):
                    self.assertEqual(frame.level_of(folder), level)
                    got = spaces(level, folder, root, "")
                    self.assertTrue(got, f"{key} has no Spaces")
                    for space, view in got.items():
                        for sub in view.subspaces or ("",):
                            page = frame.render(theme, root, folder, space, sub)
                            self.assertIn("Paper theme", page, f"{key} › {space} › {sub}")

    def test_the_version_tab_follows_s12(self):
        from live.paper_theme import VERSION_AR, VERSION_WD, spaces
        for ladder in (False, True):
            root, board, f = self._board(ladder)
            got = spaces("Job", f["version"], root, "")
            with self.subTest(ladder=ladder):
                self.assertEqual(got["Description"].subspaces, ("Version", "Venue rules"))
                self.assertEqual(got["Audience Report"].subspaces, VERSION_AR)
                self.assertEqual(got["Work Details"].subspaces, VERSION_WD)
                self.assertEqual(got["Delivery"].subspaces, ())          # item cards, no third row (s12)
                comments = spaces("Job", f["version"], root, "Comments")["Audience Report"].html
                self.assertIn("Review-demo-claim", comments)
        root, board, f = self._board(True)
        version = spaces("Job", f["version"], root, "Version")["Description"].html
        self.assertIn("j00_story/StoryA-desk-idea", version)       # read from the version's face (D6)
        self.assertIn("drafting", version)
        draft = spaces("Job", f["version"], root, "Draft-Main")["Audience Report"]
        self.assertIn("item-card", draft.html)                      # the old page's cards (JL 261007)
        self.assertIn("Introduction", draft.html)
        self.assertIn("Release a Section", [k.get("doing") or k["label"] for k in draft.run_types])
        delivery = got["Delivery"]
        self.assertIn("Build", [k.get("doing") or k["label"] for k in delivery.run_types])
        (f["round"] / "RD01-demo.md").write_text(ROUND + "\n## Cover letter\n\n### What we submit\n"
                                                 "We submit <a title>.\n\n### Why this venue\n<a fit>.\n",
                                                 encoding="utf-8")
        letter = spaces("Job", f["version"], root, "Cover letter")["Audience Report"].html
        self.assertIn("We submit &lt;a title&gt;.", letter)               # ¶1 from its sub-heading
        self.assertIn("&lt;a fit&gt;.", letter.split("J2 · why this venue")[1])
        self.assertIn("not written yet", letter)                        # ¶2, ¶4, ¶5
        work = spaces("Job", f["version"], root, "Appendix")["Work Details"].html
        self.assertIn('sec-name">Data<', work)
        self.assertNotIn("Introduction", work)

    def test_the_desk_and_delivery_are_found_on_the_ladder(self):
        from live import paper as P
        root, board, f = self._board(True)
        d = P.collect(board, "x")
        self.assertEqual(P.paper_desk(d), "desk")
        self.assertEqual(P.delivery_dir(board), (board / "delivery" / f["version"].name).resolve())

    def test_a_round_has_no_reader_contract(self):
        # the Task session's ask: the reader contract is a Section's, never a review batch's
        from live.paper_theme import spaces
        for ladder in (False, True):
            root, board, f = self._board(ladder)
            for sub in ("", "Scope"):
                html = spaces("Task", f["round"], root, sub)["Description"].html
                self.assertNotIn("reader contract", html)

    def test_a_version_of_numbered_tasks_reads_the_same(self):
        # tNN_ Tasks in a dated version (JL 261007): t0N Main, t2N Appendix, t3N a letter; the comments are a report
        # of type comments in the version's reports/ ("a special type of report"), never a Task
        from live.paper_theme import spaces
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        board = root / "examples-demo" / "Project-Demo" / "papers" / "Paper-Demo"
        version = board / "j01_v0101_desk"
        for stem in ("t01_introduction", "t21_data", "t31_cover-letter", "t32_response"):
            (version / stem).mkdir(parents=True)
            (version / stem / f"{stem}.md").write_text(f"# {stem}\n\nstate: drafting\n", encoding="utf-8")
        batch = version / "reports" / "q01_review-0101"
        batch.mkdir(parents=True)
        (batch / "q01_review-0101.md").write_text(ROUND.replace("# RD01-demo", "# q01_review-0101\n\npage-type: comments")
                                                  .replace("S-desk-Main-1-Introduction", "t01_introduction"),
                                                  encoding="utf-8")
        (version / "j01_v0101_desk.md").write_text("# j01_v0101_desk\n\nfrom: j00_v0001_desk\n", encoding="utf-8")
        (board / "board.md").write_text("# Paper-Demo\n\nboard-kind: paper-board\n\n## Pages\n\n### J01 · j01_v0101_desk\n"
                                        "t01_introduction.md\nt21_data.md\nt31_cover-letter.md\nt32_response.md\n",
                                        encoding="utf-8")
        (board.parents[1] / "project.yaml").write_text("name: Demo\n", encoding="utf-8")
        self.assertEqual(frame.level_of(version), "Job")
        for stem in ("t01_introduction", "t21_data", "t31_cover-letter"):
            self.assertEqual(frame.level_of(version / stem), "Task")
        main = spaces("Job", version, root, "Main")["Work Details"].html
        self.assertIn("introduction", main)
        self.assertNotIn("t21_data", main)
        self.assertIn("Review-demo-claim", spaces("Job", version, root, "Comments")["Audience Report"].html)
        letters = spaces("Job", version, root, "Letters")["Work Details"].html
        self.assertIn("t31_cover-letter", letters)
        self.assertIn("t32_response", letters)
        self.assertIn("q01_review-0101", letters.split("The comments they answer")[-1])
        self.assertNotIn("Review-demo-claim", letters)              # a letter is never read as a comments batch
        asked = spaces("Job", version, root, "Questions")["Audience Report"].html
        self.assertIn("J1", asked)
        self.assertIn("J5", asked)                                   # a revision (from: …) asks what changed
        self.assertIn("Comments", spaces("Task", version / "t01_introduction", root, "")["Audience Report"].subspaces)

    def test_a_story_as_studio_topics_and_questions_reads_as_a_story(self):
        # b16 Q04 (JL 261007): no Story Page; Ideation and a telling are studio topics, each research
        # question a Board Question with a report, the Section Narrative in the version's face
        from live import paper as P
        from live.paper_theme import spaces
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        board = root / "examples-demo" / "Project-Demo" / "papers" / "Paper-Demo"
        files = {
            "board.md": "# Paper-Demo\n\nboard-kind: paper-board\nstory-current: s02-story-demo\n\n## Pages\n\n"
                        "### J01 · j01_v0101_desk\nt01_introduction.md\n\n## Questions\n\n```yaml\nquestions:\n"
                        "- id: Q01\n  title: <does a placeholder change an outcome?>\n  group: demo\n"
                        "  report: reports/q01_placeholder/q01_placeholder.md\n```\n",
            "studio/s01-ideation/s01-ideation.md": "# s01-ideation\n\nfeeds: Q01\n\n## Content\n\n### 2 · Ideas (ranked)\n\n"
                        "| id | idea | why | test | verdict |\n|---|---|---|---|---|\n| i1 | <an idea> | <why> | <test> | ✅ admitted |\n",
            "studio/s02-story-demo/s02-story-demo.md": "# s02-story-demo\n\nfeeds: Q01\n\n## Content\n\n"
                        "### 1 · Identity\n\n<who it is for>\n\n### 2 · Pitch\n\n<one sentence>\n\n### 4 · Stakes\n\n<why>\n",
            "reports/q01_placeholder/q01_placeholder.md": "# <does a placeholder change an outcome?>\nanswers: Q01\n"
                        "answer-status: open\n\n## Content\n\n### 1 · The question\n\n#### 3.1 · Question 1 · RQ1\n\n"
                        "<does a placeholder change an outcome?>\n\n### 2 · Answer\n\nopen\n",
            "j01_v0101_desk/j01_v0101_desk.md": "# j01_v0101_desk\n\ntells: studio/s02-story-demo\n\n## Narrative\n\n"
                        "| Section | reader question | must establish |\n|---|---|---|\n"
                        "| t01_introduction | <what the introduction answers> | C1 |\n\n<!-- haipipe:compile-order:start -->\n"
                        "main:\n- t01_introduction\n<!-- haipipe:compile-order:end -->\n",
            "j01_v0101_desk/t01_introduction/t01_introduction.md": "# t01_introduction\n"}
        for rel_, text in files.items():
            (board / rel_).parent.mkdir(parents=True, exist_ok=True)
            (board / rel_).write_text(text, encoding="utf-8")
        (board.parents[1] / "project.yaml").write_text("name: Demo\n", encoding="utf-8")
        d = P.collect(board, "x")
        story = d["story"][0]
        self.assertEqual(story["stem"], "s02-story-demo")
        self.assertEqual([t for _, t, _ in story["spine"]], ["Identity", "Pitch", "Stakes"])
        self.assertEqual(len(story["qb"]), 1)                              # the report's question block
        self.assertEqual(story["order"], ["t01_introduction"])            # the version's compile order
        self.assertEqual(d["story00"]["stem"], "s01-ideation")
        self.assertEqual(P.section_rows(d)[0]["row"]["cells"][1], "<what the introduction answers>")
        draft = spaces("Job", board / "j01_v0101_desk", root, "Draft-Main")["Audience Report"].html
        self.assertIn("&lt;what the introduction answers&gt;", draft)
        for sub in ("Ideation", "Narrative", "High-level logic + Low-level work", "Related Questions", "Related Papers"):
            html = spaces("Block", board, root, sub)["Audience Report"].html
            self.assertNotIn("No Story yet", html, sub)

    def test_the_ideas_table_reads_verdict_and_went_to_by_name(self):
        # haipipe-paper-ideation 1.3.0 orders the Ideas (ranked) columns novelty · pilot · venue fit · verdict ·
        # target · went to, so the verdict is the sixth cell, not the fifth
        from live import paper as P
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        board = Path(tmp.name) / "examples-demo" / "Project-Demo" / "paper" / "Paper-Demo"
        (board / "studio" / "s01-ideation").mkdir(parents=True)
        (board / "board.md").write_text("# Paper-Demo\n\nboard-kind: paper-board\n", encoding="utf-8")
        (board / "studio" / "s01-ideation" / "s01-ideation.md").write_text(
            "# s01-ideation\n\n## Content\n\n### 4 · Ideas (ranked)\n\n"
            "| id | idea | novelty | pilot | venue fit | verdict | target | went to |\n|---|---|---|---|---|---|---|---|\n"
            "| i01 | <a question?> | partial | PENDING | 🔶 screen | ⬜ open | — | — |\n", encoding="utf-8")
        (board.parents[1] / "project.yaml").write_text("name: Demo\n", encoding="utf-8")
        idea = P.ideation(P.collect(board, "x"))["ideas"][0]
        self.assertEqual(idea["verdict"], "⬜ open")
        self.assertEqual(idea["went"], "—")

    def test_each_sections_build_state_links_back_to_it(self):
        # JL 261011: "how could the delivery from the section level link back to the block level delivery"
        import json, os, time
        from live import paper_theme as T
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        board = root / "examples-demo" / "Project-Demo" / "paper" / "Paper-Ladder"
        v = board / "j01_v0101_desk"
        for sec in ("t01_introduction", "t02_results"):
            (v / sec).mkdir(parents=True)
            frag = board / "delivery" / v.name / sec / "latex" / f"{sec}.tex"
            frag.parent.mkdir(parents=True)
            frag.write_text("x", encoding="utf-8")
        (board / "board.md").write_text("# Paper-Ladder\n\nboard-kind: paper-board\n", encoding="utf-8")
        built = time.time()
        (board / "delivery" / v.name / "build-manifest.json").write_text(json.dumps({
            "built": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(built)),
            "pages": [{"id": "t01_introduction", "ready": True, "reasons": [],
                       "fragment": f"delivery/{v.name}/t01_introduction/latex/t01_introduction.tex"},
                      {"id": "t02_results", "ready": False, "reasons": ["outline not approved"],
                       "fragment": f"delivery/{v.name}/t02_results/latex/t02_results.tex"},
                      {"id": "t03_discussion", "ready": False, "reasons": [], "fragment": None}]}), encoding="utf-8")
        newer = board / "delivery" / v.name / "t02_results" / "latex" / "t02_results.tex"
        os.utime(newer, (built + 60, built + 60))                  # written after the build
        os.utime(board / "delivery" / v.name / "t01_introduction" / "latex" / "t01_introduction.tex",
                 (built - 60, built - 60))
        states = {sec.name: (ready, why, state) for sec, ready, why, _, state, _ in T.section_states(board, v)}
        self.assertEqual(states["t01_introduction"], (True, "", "✅ in the build"))
        self.assertEqual(states["t02_results"], (False, "outline not approved", "❗ changed after the build: rebuild"))
        self.assertEqual(states["t03_discussion"][2], "⬜ not exported")
        html = T._section_rows(board, [v], root)
        self.assertIn("j01 › t02_results", html)
        self.assertIn("space=Delivery", html)                      # to the Section's part of the Delivery
        self.assertIn("folder ↗", html)                            # and back to its folder

    def test_related_names_its_other_group(self):
        # g03 D9: "Resources" is Description › Resources only; Related's other group is Datasets and repos
        from live import paper_theme as T
        self.assertEqual(T.OTHER, "Datasets and repos")



class DeliveryGroupsTest(unittest.TestCase):
    """JL 261014: "there should be groups for the section-task group": the whole paper, then Main, Appendix, Letters."""

    def test_each_result_goes_under_its_section_series_in_reading_order(self):
        from live import paper_theme as P
        items = [{"source": s} for s in ("j01_v1014_acl › t21_guideline-examples", "j01_v1014_acl",
                                         "j01_v1014_acl › t03_framework", "j01_v1014_acl › t00_abstract",
                                         "j01_v1014_acl › t31_cover-letter")]
        got = sorted((P.delivery_fixed(i) for i in items), key=lambda g: g[1])
        self.assertEqual([g[0][0] for g in got], ["📄 Paper", "Main", "Main", "Appendix", "Letters"])
        self.assertEqual(got[1][1], (1, 0))

if __name__ == "__main__":
    unittest.main()
