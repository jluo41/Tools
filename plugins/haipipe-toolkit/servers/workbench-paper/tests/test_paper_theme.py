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
SUBS = {"Description": ("Scope", "Venue", "Resources", "Related"), "Idea Studio": ("",),
        "Audience Report": ("Ideation", "Narrative", "High-level logic + Low-level work", "Related Questions",
                            "Related Papers"),
        "Work Details": ("Jobs", "Main", "Appendix", "Evidence"), "Runs": ("",),
        "Delivery": ("LaTeX", "Word", "Cover letter", "Rounds")}


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

    def test_a_section_folder_is_left_to_the_base(self):
        # a Section is a Page Task: its Spaces are the base's Page Task views (frame.page_task_spaces,
        # b16 s13), which the paper's own lines will go over
        from live.frame import PAGE_TASK_SUBS, page_task_spaces
        from live.paper_theme import spaces
        section = self.board / "Ba-desk-Main" / "S-desk-Main-1-Introduction"
        got = spaces("Task", section, self.root, "")
        want = dict(PAGE_TASK_SUBS, **{"Audience Report": PAGE_TASK_SUBS["Audience Report"] + ("Comments",)})
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
        base = page_task_spaces(section, self.root, "")
        for name in ("Work Details",):                                # the paper adds nothing here
            self.assertEqual(got[name], base[name])

    def test_a_section_carries_the_paper_lines(self):
        # ◆ (b16 s13): the reader contract in Scope, the SUB-* rows in Requirement, the form over the
        # Table, and "ready for the build" apart from "done" in Delivery
        from live.paper_theme import spaces
        section = self.board / "Ba-desk-Main" / "S-desk-Main-1-Introduction"
        (section / "S-desk-Main-1-Introduction.md").write_text(SECTION, encoding="utf-8")
        unit = section / "results" / "run-display-0101-demo" / "payload" / "Display1-demo"
        unit.mkdir(parents=True)
        scope = spaces("Task", section, self.root, "Scope")["Description"].html
        self.assertIn("The reader contract", scope)
        self.assertIn("&lt;the one question this Section answers&gt;", scope)
        self.assertIn("SUB-INTRO-01", spaces("Task", section, self.root, "Requirement")["Description"].html)
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
            (folders["version"] / "delivery").mkdir()
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
        self.assertEqual(P.delivery_dir(board), f["version"] / "delivery")

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

    def test_related_names_its_other_group(self):
        # g03 D9: "Resources" is Description › Resources only; Related's other group is Datasets and repos
        from live import paper_theme as T
        self.assertEqual(T.OTHER, "Datasets and repos")


if __name__ == "__main__":
    unittest.main()
