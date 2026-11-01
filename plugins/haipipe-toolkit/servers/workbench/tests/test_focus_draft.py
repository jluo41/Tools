"""A draft Task on the focus page (b32 s42): Report and Work views drawn in place, no iframe step page, no fold."""
import re
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

from live import focus_page, frame  # noqa: E402

DRAFT = """# t00_summary draft v0.1
version: v0.1
approved: ⬜ waiting

## 1 · Structure

### C1.P1 · Background · S1 to S2
- B1 · The problem in one line
- B2 · What we set out to learn

## 2 · Scratch

## 3 · Draft

### C1.P1 · Background
The first sentence states the problem.
The second sentence names what we learn.
"""


class FocusDraftTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        block = self.root / "b01_paper"
        (block / "j01_v1").mkdir(parents=True)
        (block / "board.md").write_text("# Paper\nspine: Write the paper.\n")
        (block / "j01_v1" / "j01_v1.md").write_text("# j01 · v1\ngoal: The first send.\n")
        self.task = block / "j01_v1" / "t00_summary"
        (self.task / "draft").mkdir(parents=True)
        (self.task / "t00_summary.md").write_text(
            "# t00_summary · Summary\ntask-type: draft\nreader-question: What did the study find?\n\n## Content\n\n"
            "#### C1.P1 · Background · S1 to S2\nThe first sentence states the problem.\n")
        (self.task / "draft" / "t00_summary-draft-v0.1.md").write_text(DRAFT)
        self.theme = frame.Theme(name="paper")

    def page(self, section="", group=""):
        return focus_page.render(self.theme, self.root, self.task, section, group)

    def test_work_is_the_five_steps_in_place_with_their_state_words(self):
        page = self.page()
        bar = re.search(r'<nav class="section-views".*?</nav>', page, re.S).group(0)
        for step in ("1 · Plan", "2 · Write", "3 · Evidence", "5 · Revise", "Runs"):
            self.assertIn(step, bar)
        self.assertNotIn("4 · Display", bar)          # the text calls no Table or Figure: no empty view (JL 261031)
        self.assertNotIn("Ask the agent", self.page("work", "evidence"))   # prompts only on Plan, Write, Revise
        self.assertNotIn(">Studio<", bar)                            # a section, never a view (haipipe-ui Page parts)
        self.assertNotIn(">Delivery<", bar)
        self.assertNotIn("space=Work+Details", page)                # no old step page in an iframe
        self.assertNotIn('class="draft-frame"', page)
        self.assertIn('class="vw', bar)                              # each step's state, a word on its button

    def test_the_aim_is_the_reader_question(self):
        self.assertIn('<span class="goal-word">Aim</span><p>What did the study find?</p>', self.page())

    def test_studio_and_delivery_are_on_the_right_rail(self):
        rail = re.search(r'<nav class="focus-rail right".*?</nav>', self.page(), re.S).group(0)
        self.assertIn('aria-label="Studio"', rail)
        self.assertIn('aria-label="Delivery"', rail)

    def test_report_is_mindmap_text_status_and_opens_on_the_text(self):
        page = self.page("report")
        bar = re.search(r'<nav class="section-views".*?</nav>', page, re.S).group(0)
        for view in ("MindMap", "Text", "Status"):
            self.assertIn(view, bar)
        self.assertNotIn("Review", bar)                              # the review is Work › 5 · Revise's (JL 261031)
        self.assertIn("The first sentence states the problem.", page)
        status = self.page("report", "status")
        self.assertIn("1 · Plan", status)
        self.assertIn("Go</a>", status)

    def test_the_steps_have_sections_not_folds(self):
        plan = self.page("work", "plan")
        content = plan.split('<section class="focus-card">', 1)[1]
        self.assertNotIn('<details class="topic work-task', content)
        self.assertIn("class=fd-sec", content)
        self.assertIn("fd-copy", content)                            # the prompt as a verb


    def test_a_version_shows_its_whole_paper_and_a_section_previews_its_lanes(self):
        import json
        vdir = self.root / "b01_paper" / "delivery" / "j01_v1"
        for rel in ("latex/Paper-draft.pdf", "word/Paper-draft.pdf", "word/Paper-draft.docx", "t00_summary/latex/t00_summary.pdf"):
            (vdir / rel).parent.mkdir(parents=True, exist_ok=True)
            (vdir / rel).write_bytes(b"%PDF-1.4")
        (vdir / "build-manifest.json").write_text(json.dumps({"outputs": {"pdf": "latex/Paper-draft.pdf", "docx": "word/Paper-draft.docx",
                                                                          "docx_pdf": "word/Paper-draft.pdf"}}))
        job = self.task.parent
        page = focus_page.render(self.theme, self.root, job, "delivery")
        bar = re.search(r'<nav class="section-views".*?</nav>', page, re.S).group(0)
        for view in ("Paper", "Word", "Built files"):
            self.assertIn(view, bar)
        self.assertIn('class=fd-prev src="/b01_paper/delivery/j01_v1/latex/Paper-draft.pdf"', page)   # previewed in the page
        self.assertIn("Waiting for you: check the paper", focus_page.render(self.theme, self.root, job, "delivery", "files"))
        board = focus_page.render(self.theme, self.root, self.root / "b01_paper", "delivery")
        self.assertIn("Paper-draft.pdf", board)                                                   # the Board lists each version's paper
        section = focus_page.render(self.theme, self.root, self.task, "delivery", "pdf")
        self.assertIn("t00_summary.pdf", section)
        self.assertNotIn("Waiting for you: check", focus_page.render(self.theme, self.root, self.task, "delivery", "files"))



class PaperJobNamesTest(unittest.TestCase):
    """A paper Board's Jobs by layer (JL 261031): j01_evidence_display, j02_evidence_value, j03_evidence_cite, then the
    writing Jobs j11_writing_<version>; the page tells them apart by name."""

    def test_evidence_jobs_are_not_versions_and_fill_their_views(self):
        import re, tempfile
        from live import board_evidence, board_read, paper_version
        with tempfile.TemporaryDirectory() as tmp:
            b = Path(tmp) / "Paper-X"
            for j in ("j01_evidence_display/t01_figure1-x", "j01_evidence_display/t51_etable1-x",
                      "j02_evidence_value/t01_values-sample", "j03_evidence_cite", "j11_writing_v1130_venue/t00_summary"):
                (b / j).mkdir(parents=True)
            self.assertEqual([j.name for j in sorted(b.iterdir()) if board_read.is_version(j)], ["j11_writing_v1130_venue"])
            self.assertEqual(re.findall(r"<h3 class=fd-h>([^<]*)", board_evidence.evidence_html(b, Path(tmp))),
                             ["Displays · j01_evidence_display", "Values · j02_evidence_value", "Citations · j03_evidence_cite"])
            views = paper_version.version_work_views(b / "j11_writing_v1130_venue", Path(tmp))
            self.assertIn("t01_figure1-x", views["work-display-main"][1]())
            self.assertIn("t51_etable1-x", views["work-display-appendix"][1]())


if __name__ == "__main__":
    unittest.main()
