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

    def test_work_is_the_five_steps_in_place_by_name_only(self):
        page = self.page()
        bar = re.search(r'<nav class="section-views".*?</nav>', page, re.S).group(0)
        for step in ("1 · Draft", "2 · Plan", "3 · Evidence"):          # Draft first (JL 261113)
            self.assertIn(step, bar)
        for gone in ("2 · Write", "5 · Revise", ">Runs<", "MindMap", ">Text<", "Plan + Results"):   # JL 261113
            self.assertNotIn(gone, bar)
        self.assertNotIn("4 · Display", bar)          # the text calls no Table or Figure: no empty view (JL 261031)
        self.assertNotIn("Ask the agent", self.page("work", "evidence"))   # prompts only on Plan, Write, Revise
        self.assertNotIn(">Studio<", bar)                            # a section, never a view (haipipe-ui Page parts)
        self.assertNotIn(">Delivery<", bar)
        self.assertNotIn("space=Work+Details", page)                # no old step page in an iframe
        self.assertNotIn('class="draft-frame"', page)
        self.assertNotIn('class="vw', bar)                           # a view button carries only its name (Page words)

    def test_the_aim_is_the_reader_question(self):
        self.assertIn('<span class="goal-word">Aim</span><p>What did the study find?</p>', self.page())

    def test_studio_and_delivery_are_on_the_right_rail(self):
        rail = re.search(r'<nav class="focus-rail right".*?</nav>', self.page(), re.S).group(0)
        self.assertIn('aria-label="🎨 Studio"', rail)
        self.assertIn('aria-label="Delivery"', rail)

    def test_draft_is_the_sentence_board(self):
        page = self.page("report", "draft")                          # Write and Revise in one view (JL 261113)
        self.assertIn("The first sentence states the problem.", page)
        self.assertIn("sx-row", page)

    def test_the_steps_have_sections_not_folds(self):
        plan = self.page("work", "plan")
        content = plan.split('<section class="focus-card">', 1)[1]
        self.assertNotIn('<details class="topic work-task', content)
        self.assertIn("class=fd-sec", content)
        self.assertIn("fd-copy", content)                            # the prompt as a verb

    def test_old_work_links_open_report_with_shared_context_and_keep_actions(self):
        from live import work_frame
        for view, now in (('plan', 'plan'), ('write', 'draft'), ('evidence', 'evidence'), ('revise', 'draft')):
            page = self.page('work', view)
            self.assertIn('<h2>📋 Review Content</h2>', page)
            self.assertIn('🧭 Around the Work', page)
            rail = re.search(r'<nav class="focus-rail right".*?</nav>', page, re.S).group()
            self.assertNotIn('aria-label="Work"', rail)
            for key, title in work_frame.SHARED:
                self.assertIn(f'aria-label="{title}"', rail)
            bar = re.search(r'<nav class="section-views".*?</nav>', page, re.S).group()
            self.assertIn(f'section=report&amp;group={now}" aria-current="page"', bar)
            self.assertNotIn('⚙️ Process', page)
            self.assertNotIn('📊 Results', page)
        plan = self.page('work', 'work-plan')
        self.assertIn('§1 Structure', plan)          # Plan keeps Structure and Examples only (JL 261115: "others can drop")
        self.assertNotIn('Where this step stands', plan)
        self.assertNotIn('🗂 Records', plan)
        self.assertIn('fd-copy', self.page('studio'))

    def test_draft_context_respects_explicit_run_ownership_and_keeps_source_files(self):
        from live import draft_context, work_files
        def run(name, metadata=''):
            path = self.task / 'runs' / name
            path.mkdir(parents=True)
            (path / 'run.yaml').write_text('state: done\n' + metadata)
            return path
        native = run('run-structure-native')
        paragraph = run('run-paragraph-native', 'target: C1.P1\n')
        explicit = run('run-structure-explicit', 'view: revise\n')
        unknown = run('run-unknown')
        selected = draft_context.scope(self.task, self.root, 'plan', [], [], [])
        self.assertIn(native, selected['runs'])
        self.assertNotIn(explicit, selected['runs'])
        self.assertNotIn(unknown, selected['runs'])
        self.assertIn(explicit, draft_context.scope(self.task, self.root, 'revise', [], [], [])['runs'])
        self.assertIn(paragraph, draft_context.scope(self.task, self.root, 'write', [], [], [])['runs'])
        self.assertIn(unknown, draft_context.scope(self.task, self.root, None, [], [], [])['runs'])
        sources = dict(work_files.folder_groups(self.task, self.root, 'plan', scope=selected, skill_rows=[]))['🧩 Blocks']
        self.assertIn(self.task / 'draft' / 't00_summary-draft-v0.1.md', sources)
        outside = self.root.parent / 'outside'
        selected['source_paths'].append(outside)
        self.assertNotIn(outside, dict(work_files.folder_groups(self.task, self.root, 'plan', scope=selected, skill_rows=[]))['🧩 Blocks'])
        (self.task / 'display').mkdir()
        self.assertIn(self.task / 'display', draft_context.scope(self.task, self.root, 'display', [], [], [])['source_paths'])


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
            self.assertIn("t01_figure1-x", views["work-display"][1]())     # main and appendix, one Display view (261113)
            self.assertIn("t51_etable1-x", views["work-display"][1]())


if __name__ == "__main__":
    unittest.main()
