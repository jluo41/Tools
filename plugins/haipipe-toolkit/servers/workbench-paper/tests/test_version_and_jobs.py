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

    def test_a_version_is_structure_evidence_and_display(self):
        # JL 261113: "we want to put the structure at the first one ... I think we can just keep the evidence and display
        # views here": Structure first and opened by default; Values and Citations one Evidence view; no MindMap and no
        # Draft-Main or Draft-Appendix (each Section's text is a click away from its row in Structure)
        report = self.render(self.version, "report")
        views = views_of(report)
        self.assertEqual(views[0], "structure")
        self.assertTrue(set(views) <= {"structure", "evidence", "display"}, views)
        self.assertIn("evidence", views)
        self.assertEqual(views_of(self.render(self.version, "work")), views)   # Work retired (JL 261111)
        self.assertNotIn(">Work<", report.split("focus-rail right")[-1][:3000])
        old = self.render(self.version, "report", "draft-main")              # an old link opens Structure
        self.assertIn('group=structure" aria-current="page"', old)
        evidence = self.render(self.version, "report", "evidence")
        self.assertIn("Values</h3>", evidence)                              # a bar with no tally word (AGENTS § Page words)
        self.assertIn("Citations</h3>", evidence)

    def test_evidence_and_submission_jobs_have_their_own_views(self):
        # JL 261106: the evidence and submission Jobs fell back to the old Progress view
        want = {"j01_evidence_display": ["display-plan", "display-list", "display-examples"],
                "j02_evidence_value": ["value-list", "value-check"],
                "j03_evidence_cite": ["cite-list", "cite-check"],
                "j21_submission_v1130_desk": ["letter", "portal"]}
        for job, keys in want.items():
            report, work = self.render(self.b / job, "report"), self.render(self.b / job, "work")
            self.assertEqual(views_of(report), ["mindmap"] + keys, job)
            self.assertEqual(views_of(work), views_of(report), job)   # Work retired (JL 261111)
            self.assertNotIn(">Progress<", work, job)
            for key in keys:
                page = self.render(self.b / job, "report", key)
                self.assertNotIn("Process</h3>", page, (job, key))
                self.assertNotIn("Nothing asked yet", page, (job, key))     # no collection Run, no 🙋 section (261114)
        displays = self.render(self.b / "j01_evidence_display", "work", "work-display-list")
        self.assertNotIn("Where each display stands", displays)      # its state is its tab's (JL 261109)
        self.assertIn("Displays</h3>", displays)                           # no "1 of 1 drawn" tally on the bar
        self.assertNotIn("1 of 1 drawn", displays)
        cites = self.render(self.b / "j03_evidence_cite", "report", "cite-list")
        self.assertIn("Citations</h3>", cites)                             # no "1 of 3 verified" tally
        self.assertNotIn("1 of 3 verified", cites)
        check = self.render(self.b / "j02_evidence_value", "report", "value-check")
        self.assertIn("🔎 Check</h3>", check)                              # no "nothing yet" state word on its bar

    def test_display_tabs_draw_any_display_tasks_as_the_paper_does(self):
        # JL 261109: the work Block's Findings displays are drawn by the paper's own code, grouped by `group:`
        from live.board_results import display_tabs
        job = self.root / "work" / "b01_x" / "j21_display"
        for t, face in (("t01_figure_a", "label: Display 1\nname: Switches\ntype: figure\ngroup: result\nstatus: drawn\n"),
                        ("t21_method_a", "label: Method 1\nname: The rule\ntype: figure\ngroup: method\nstatus: drawn\n")):
            (job / t / "runs" / "r01_draw" / "result").mkdir(parents=True)
            (job / t / "runs" / "r01_draw" / "result" / "preview.pdf").write_bytes(b"%PDF-1.4\n")
            (job / t / f"{t}.md").write_text(f"# {t}\ntask-type: display\n{face}", encoding="utf-8")
        html, word = display_tabs(sorted(job.iterdir()), self.root, names={"main": "Results", "method": "Methods"})
        self.assertEqual(word, "")                                          # each tab shows its own state; no tally
        self.assertEqual(re.findall(r"pb-lgroup>([^<]+)", html), ["Results", "Methods"])
        self.assertIn("📈 Figure · Switches", html)
        self.assertIn("r01_draw/result/preview.pdf", html)
        self.assertEqual(display_tabs([], self.root), ("", ""))

    def test_the_tracked_word_file_has_its_own_tab(self):
        # JL 261110: "the Word-Change-Track ... based on the previous change tracks from professors and you add the changes"
        from live.board_results import _paper_files
        out = self.b / "delivery" / "j11_writing_v1130_desk"
        (out / "word-tracked").mkdir(parents=True)
        (out / "build-manifest.json").write_text('{"outputs": {}}', encoding="utf-8")
        for ext in ("pdf", "docx"):
            (out / "word-tracked" / f"Paper-X-v4-tracked.{ext}").write_bytes(b"x")
        res = self.b / "j31_review_coauthor_v1110" / "t03_tracked_word" / "runs" / "r01_v4_plus_ours" / "result"
        res.mkdir(parents=True)
        (res / "headline.txt").write_text("Paper-X-v4.docx + 2 tracked changes by <author> -> Paper-X-v4-tracked.docx\n", encoding="utf-8")
        html = _paper_files(out, self.root)
        self.assertIn("Paper-Word-Tracked", html)
        self.assertIn("v4 + 2 changes by &lt;author&gt;", html)
        self.assertIn("word-tracked/Paper-X-v4-tracked.pdf", html)
        self.assertIn("word-tracked/Paper-X-v4-tracked.docx", html)

    def test_the_structure_view_reads_the_story_and_the_version_side_by_side(self):
        # JL 261111: "it should be a view for the job workbench UI"; the Story's Narrative beside the version's, signed
        story = self.b / "s02-story-desk-x" / "s02-story-desk-x.md"
        story.write_text(STORY + "\n### 8 · Section Narrative\n\nC1 the first claim, then C2.\n", encoding="utf-8")
        face = self.version / "j11_writing_v1130_desk.md"
        face.write_text(face.read_text() + "\n## Narrative\n\n| Section | question |\n|---|---|\n| t00_summary | Q |\n",
                        encoding="utf-8")
        plan = self.version / "t00_summary" / "draft"
        plan.mkdir()
        (plan / "t00_summary-draft-v0.1.md").write_text(
            "# t00_summary\napproved: ⬜\n\n## 1 · Structure\n\n### C1.P1 · The problem · S1 to S2\n- B1 · S1 · x\n",
            encoding="utf-8")
        page = self.render(self.version, "report", "structure")
        self.assertIn("C1 the first claim, then C2.", page)                 # the Story, read, not copied
        self.assertNotIn("not signed", page)                               # the mark carries the state
        self.assertIn('<div class="st-sign st-no"><b>⬜</b>', page)
        self.assertNotIn("plans signed", page)
        self.assertIn("The problem", page)                                   # the paper map, one line per paragraph
        self.assertIn("pm-root", page)                                      # the Section's Plan mind map, the draft's own
        self.assertNotIn("contenteditable", page.split("pm-root", 1)[1][:4000])   # read-only here
        import sys as _s
        _s.path.insert(0, str(Path(__file__).resolve().parents[3] / "skills/1_base/draft/hai-draft"))
        from src.page_sign import sign_narrative
        self.assertTrue(sign_narrative(self.version, "this order")["ok"])
        page = self.render(self.version, "report", "structure")
        self.assertIn('in chat: &quot;this order&quot;', page)
        story.write_text(story.read_text().replace("then C2", "then C3"), encoding="utf-8")
        html = self.render(self.version, "report", "structure")   # drafting: a quiet note, never a re-sign (M-D09)
        self.assertIn("sync-narrative", html)
        self.assertNotIn("sign again", html)

    def test_the_structure_view_shows_the_examples_as_one_live_drawing(self):
        # JL 261111: "one draw should be okay": the Section's examples topic as its live drawing, a jump per frame
        # (Pattern, each paper), opening on the first; nothing listed under it
        import json
        task = self.version / "t00_summary"
        face = task / "t00_summary.md"
        face.write_text((face.read_text() if face.is_file() else "# t00_summary\n") + "examples: s23-t00-summary-desk-examples\n",
                        encoding="utf-8")
        topic = self.b / "s23-t00-summary-desk-examples"
        (topic / "reads" / "p02-frey2023").mkdir(parents=True)
        (topic / "reads" / "p02-frey2023" / "reading.yaml").write_text("paper:\n  title: <a paper>\n", encoding="utf-8")
        (topic / f"{topic.name}.excalidraw").write_text(json.dumps({"elements": [
            {"type": "frame", "name": "Pattern", "x": 0, "y": 0, "width": 100, "height": 50},
            {"type": "frame", "name": "Frey et al. 2023", "x": 0, "y": 60, "width": 100, "height": 50}]}), encoding="utf-8")
        page = self.render(self.version, "report", "structure")
        self.assertIn("The venue's papers", page)
        self.assertIn("fit=width&amp;bare=1&amp;focus=Pattern", page)       # opens on the first frame, its width
        self.assertIn(">Frey et al. 2023</button>", page)                    # a jump to that paper's area
        self.assertIn(">Whole drawing</button>", page)
        self.assertNotIn("st-paper", page)                                   # no rows under the drawing
        self.assertNotIn("open the page ↗", page)

    def test_a_paragraph_outside_4_to_7_sentences_is_marked_on_the_plan_map(self):
        # JL 261112: "unless having good reason, we might make sure they are between 4~7 sentences": red on the map,
        # muted with a reason, counted on the Section's tab
        task = self.version / "t00_summary"
        face = task / "t00_summary.md"
        face.write_text((face.read_text() if face.is_file() else "# t00_summary\n") + "section_kind: results\n", encoding="utf-8")
        (task / "draft").mkdir(exist_ok=True)
        (task / "draft" / "t00_summary-draft-v0.1.md").write_text(
            "# t00_summary\napproved: ⬜\n\n## 1 · Structure\n\n### C1.P1 · The long one · S1 to S10\n- B1 · S1 · x\n\n"
            "### C1.P2 · The short one · S11 to S12\nreason: one table, read once\n- B1 · S11 · y\n", encoding="utf-8")
        page = self.render(self.version, "report", "structure")
        self.assertIn("❗ 10 sentences (4 to 7)", page)
        self.assertIn("2 sentences · reason given", page)
        self.assertNotIn("2 paragraphs · 1 off", page)                    # no paragraph tally on the Section's tab
        self.assertNotIn("paragraphs ·", page)

    def test_each_view_shows_its_own_items(self):
        # JL 261106: "a view's bottom section shows that view's own items, and the rail shows everything"
        form(self.version, "r01_collect_story", "Story asks", "Paper-X-s02:paper @ story")
        form(self.b / "j02_evidence_value" / "t01_values", "r01_collect_values", "Value asks")
        form(self.version / "t00_summary", "r01_collect_words", "Section asks")
        story = re.sub(r'(?s)<template id="wait-items">.*?</template>', "", self.render(self.b, "report", "story"))   # the 🙋 tray lists every wait
        self.assertIn("Story asks", story)
        self.assertNotIn("Value asks", story)
        evidence = re.sub(r'(?s)<template id="wait-items">.*?</template>', "", self.render(self.b, "report", "evidence"))
        self.assertNotIn("Value asks", evidence)  # a folder's type does not assign a question to a View
        self.assertNotIn("Story asks", evidence)
        writing = re.sub(r'(?s)<template id="wait-items">.*?</template>', "", self.render(self.b, "report", "draft"))
        self.assertNotIn("Section asks", writing)  # unassigned questions remain in the rail
        version = re.sub(r'(?s)<template id="wait-items">.*?</template>', "", self.render(self.version, "report", "draft-main"))      # a version takes the draft Task's bands
        self.assertIn("📋 Review Content", version)                       # (JL 261113): its forms on its own rail;
        self.assertNotIn("Story asks", version)                           # an empty 🧭 band is hidden
        self.assertIn("Story asks", self.render(self.version, "interactions"))
        rail = self.render(self.b, "interactions")
        for title in ("Story asks", "Value asks", "Section asks"):          # the rail keeps everything
            self.assertIn(title, rail)


if __name__ == "__main__":
    unittest.main()
