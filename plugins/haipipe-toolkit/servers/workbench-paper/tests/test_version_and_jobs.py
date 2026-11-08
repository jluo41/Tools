"""A paper version's Report and the evidence and submission Jobs' pages (JL 261106): a version's Report is its Work's six
views, results only, MindMap first; the evidence and submission Jobs have Report and Work views of their own, never the
old Progress view; each view's 🙋 Interaction shows that view's own items; every bar carries a state word. Placeholders
only: the Board is written into a temp folder, never a real paper."""
from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import focus_page, frame  # noqa: E402

STORY = "# s02 · Story\n\n**Stage:** shaping\n\n### 2 · Pitch\n\n<the paper in short>.\n"
SECTION = ("# t00_summary · Summary\ntask-type: draft\nreader-question: What did the study find?\n\n## Content\n\n"
           "#### C1.P1 · Background · S1 to S2\nThe first sentence states the problem.\n")
FORM = ("# {title}\n\nfor: {about}\n\n## Q1 · First\n\nWhy.\n\n**Which one?**\n\n- [ ] A · Aa\n- [ ] B · Bb\n")


def form(page: Path, run: str, title: str, about: str = "") -> None:
    d = page / "runs" / run
    d.mkdir(parents=True)
    (d / "run.yaml").write_text("status: waiting\n", encoding="utf-8")
    (d / f"{run}.html").write_text("<html></html>", encoding="utf-8")
    (d / "question_collection.md").write_text(FORM.format(title=title, about=about), encoding="utf-8")


def views_of(page: str) -> list:
    nav = re.search(r'<nav class="section-views".*?</nav>', page, re.S)[0]
    return re.findall(r'group=([^"&]+)', nav)


class VersionAndJobsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        b = self.b = self.root / "paper" / "Paper-X"
        (b / "s02-story-desk-x").mkdir(parents=True)
        (b / "s02-story-desk-x" / "s02-story-desk-x.md").write_text(STORY, encoding="utf-8")
        (b / "board.md").write_text("# Paper-X\n\nboard-kind: paper-board\nstory-current: s02-story-desk-x\n", encoding="utf-8")
        self.version = b / "j11_writing_v1130_desk"
        for t in ("t00_summary", "t21_appendix"):
            (self.version / t).mkdir(parents=True)
            (self.version / t / f"{t}.md").write_text(SECTION.replace("t00_summary", t), encoding="utf-8")
        (self.version / "j11_writing_v1130_desk.md").write_text("# j11 · v1130\ngoal: The first send.\n", encoding="utf-8")
        for job, task, face in (("j01_evidence_display", "t01_figure1", "label: Figure 1\nstatus: drawn 2026-11-01\n"),
                                ("j02_evidence_value", "t01_values", "label: Values\nstatus: filled by r01\n"),
                                ("j03_evidence_cite", "t01_cite", "label: Prior work\nstatus: 3 keys: 1 verified\n")):
            (b / job / task).mkdir(parents=True)
            (b / job / task / f"{task}.md").write_text(f"# {task}\n{face}", encoding="utf-8")
        sub = b / "j21_submission_v1130_desk"
        (sub / "t01_cover-letter").mkdir(parents=True)
        (sub / "j21_submission_v1130_desk.md").write_text("# j21\nfor: j11_writing_v1130_desk\n", encoding="utf-8")
        (sub / "t01_cover-letter" / "t01_cover-letter.md").write_text(
            "# t01_cover-letter\nwords-in: ../../j11_writing_v1130_desk/t31_cover-letter\n", encoding="utf-8")
        self.theme = frame.Theme(name="paper")

    def render(self, folder, section="", group=""):
        return focus_page.render(self.theme, self.root, folder, section, group)

    def test_a_version_report_is_its_work_views_results_only(self):
        # JL 261106: "A paper version's Report gets the same six views as its Work ... showing results only"
        report = self.render(self.version, "report")
        work = self.render(self.version, "work")
        self.assertEqual(views_of(report)[0], "mindmap")                    # MindMap first
        self.assertEqual(views_of(report)[1:], [k.removeprefix("work-") for k in views_of(work)])
        self.assertEqual(views_of(report)[1:7], ["draft-main", "draft-appendix", "display-main", "display-appendix",
                                                 "values", "citations"])
        main = self.render(self.version, "report", "draft-main")
        self.assertNotIn("Process</h3>", main)                              # results only
        self.assertIn("1 · 📝 Text<span class=word>1 of 1 with text</span>", main)   # each Section's text, a side tab each
        self.assertIn("The first sentence states the problem.", main)
        self.assertIn("pb-side", main)
        done = self.render(self.version, "work", "work-draft-main")
        self.assertLess(done.index("⚙️ Process"), done.index("📊 Results"))
        self.assertIn("🪜 Sections", done)
        self.assertIn("The first sentence states the problem.", done.split("📊 Results")[1])
        self.assertIn("t21_appendix", self.render(self.version, "report", "draft-appendix"))
        # switching between Report and Work keeps the view (rail_view)
        self.assertIn("section=work&amp;group=work-draft-appendix", self.render(self.version, "report", "draft-appendix"))
        self.assertIn("section=report&amp;group=values", self.render(self.version, "work", "work-values"))

    def test_evidence_and_submission_jobs_have_their_own_views(self):
        # JL 261106: the evidence and submission Jobs fell back to the old Progress view
        want = {"j01_evidence_display": ["display-plan", "display-list", "display-examples"],
                "j02_evidence_value": ["value-list", "value-check"],
                "j03_evidence_cite": ["cite-list", "cite-check"],
                "j21_submission_v1130_desk": ["letter", "portal"]}
        for job, keys in want.items():
            report, work = self.render(self.b / job, "report"), self.render(self.b / job, "work")
            self.assertEqual(views_of(report), ["mindmap"] + keys, job)
            self.assertEqual(views_of(work), ["work-" + k for k in keys], job)
            self.assertNotIn(">Progress<", work, job)
            for key in keys:
                page = self.render(self.b / job, "report", key)
                self.assertNotIn("Process</h3>", page, (job, key))
                self.assertIn("🙋 Interaction<span", page, (job, key))
        displays = self.render(self.b / "j01_evidence_display", "work", "work-display-list")
        self.assertLess(displays.index("⚙️ Process"), displays.index("📊 Results"))
        self.assertIn("Displays<span class=word>1 of 1 drawn</span>", displays)
        cites = self.render(self.b / "j03_evidence_cite", "report", "cite-list")
        self.assertIn("Citations<span class=word>1 of 3 verified</span>", cites)
        check = self.render(self.b / "j02_evidence_value", "report", "value-check")
        self.assertIn("🔎 Check<span class=word>nothing yet</span>", check)

    def test_each_view_shows_its_own_items(self):
        # JL 261106: "a view's bottom section shows that view's own items, and the rail shows everything"
        form(self.version, "r01_collect_story", "Story asks", "Paper-X-s02:paper @ story")
        form(self.b / "j02_evidence_value" / "t01_values", "r01_collect_values", "Value asks")
        form(self.version / "t00_summary", "r01_collect_words", "Section asks")
        story = self.render(self.b, "report", "story")
        self.assertIn("Story asks", story.split("🙋 Interaction")[-1])
        self.assertNotIn("Value asks", story)
        evidence = self.render(self.b, "report", "evidence")
        self.assertIn("Value asks", evidence)
        self.assertNotIn("Story asks", evidence.split("🙋 Interaction")[-1])
        writing = self.render(self.b, "report", "draft")
        self.assertIn("Section asks", writing)                            # about no part: Writing's
        version = self.render(self.version, "report", "draft-main")
        self.assertIn("Story asks", version)                              # a version: its own forms
        self.assertNotIn("Section asks", version.split("🙋 Interaction")[-1])
        rail = self.render(self.b, "interactions")
        for title in ("Story asks", "Value asks", "Section asks"):          # the rail keeps everything
            self.assertIn(title, rail)


if __name__ == "__main__":
    unittest.main()
