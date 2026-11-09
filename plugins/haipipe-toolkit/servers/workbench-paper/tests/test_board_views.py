"""A paper Board's Report and Work views (board_views.py, b16 s32 and s33): every view is two bands, each numbered from
1; Report reads RESULTS first and Work PROCESS first; Work's RESULTS is Report's, section for section; the phone rules
come after the base rules they change. Placeholders only: the Board is written into a temp folder, never a real paper."""
from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import board_views, ui_parts  # noqa: E402

FLOW = """# s03 · Paper dataflow

**Topic:** <the data> go in; <the tables> come out.

**Stage:** shaping


Open
----

1. <an open point>
"""
STORY = """# s02 · Story

**Stage:** shaping

### 7 · Task Roadmap

| T | work | where | state | what it gives | feeds |
|---|---|---|---|---|---|
| T0 | <a Run> | b11.j25.t01 | ⬜ waiting for JL | <its tables> | E1 |
| T1 | <a Run> | b11.j25.t02 | ✅ done | <its tables> | E2 |


Open
----

1. <an open story point>
"""


IDEA = """# s01 · Ideation

**Stage:** chosen


Direction
---------

**Direction**: <a direction>.


Open
----

1. <an open idea>
"""
PAPERFLOW = """# s04 · Paper workflow

**Stage:** shaping


Timeline
--------

| when | step | who | state |
|---|---|---|---|
| 261201 | <a step> | <a person> | ⬜ |
"""


def board(tmp: Path) -> Path:
    b = tmp / "paper" / "Paper-X"
    for rel, text in (("s02-story-desk-idea/s02-story-desk-idea.md", STORY), ("s03-paper-dataflow/s03-paper-dataflow.md", FLOW)):
        (b / rel).parent.mkdir(parents=True, exist_ok=True)
        (b / rel).write_text(text, encoding="utf-8")
    (b / "j11_writing_v1130_desk" / "t00_summary").mkdir(parents=True)
    (b / "board.md").write_text("# Paper-X\n\nboard-kind: paper-board\n", encoding="utf-8")
    return b


def bars(html: str) -> list:
    """The band names and the numbered section bars, in page order."""
    return re.findall(r"<h3 class=pb-group>\S+ ([A-Za-z]+)<|<h3 class=fd-h>(\d+) · ", html)


def results(html: str) -> str:
    """The RESULTS band: from its heading to the next band, the dashed rule or the page's scripts."""
    part = html.split("Results</h3>", 1)[1]
    return re.split(r"<h3 class=pb-group>|<hr class=pb-rule>|<script>", part, maxsplit=1)[0]


class BoardViewsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.b = board(self.root)
        md = lambda text, base: text
        self.report = {k: f() for k, (_, f) in board_views.board_report_views(self.b, self.root, md).items()}
        self.work = {k: f() for k, (_, f) in board_views.board_work_views(self.b, self.root, md).items()}

    def tearDown(self):
        self.tmp.cleanup()

    def test_each_band_numbers_from_one(self):
        for key, html in {**self.report, **{f"work-{k}": v for k, v in self.work.items()}}.items():
            seq, band = [], None
            for name, num in bars(html):
                if name:
                    band = name
                    seq.append([])
                elif band:
                    seq[-1].append(int(num))
            for nums in seq:
                self.assertEqual(nums, list(range(1, len(nums) + 1)), key)

    def test_report_is_its_sections_and_work_process_first(self):
        # JL 261101: "for the Results and Process, they will just be in the Work"; the Report: 1, 2, 3 (s32-D27)
        self.assertEqual([n for n, _ in bars(self.report["plan"]) if n], [])
        self.assertNotIn("Process</h3>", self.report["plan"])
        self.assertEqual([n for n, _ in bars(self.work["work-plan"]) if n], ["Process", "Results"])

    def test_work_process_never_repeats_the_interaction(self):
        # JL 261105: the open forms show once, in the view's last section 🙋 Interaction; Process keeps only the
        # parts' own open points, and only when there are some
        for key, html in self.work.items():
            self.assertNotIn("Decisions waiting for you", html, key)
            self.assertNotIn("Nothing waits on you", html, key)

    def test_work_results_are_report_results(self):
        for key in self.report:
            page = re.split(r"<hr class=pb-rule>|<script>", self.report[key], maxsplit=1)[0]
            self.assertIn(results(self.work["work-" + key]).strip()[:400], page, key)

    def test_plan_process_is_its_plan_and_runs(self):
        work = self.work["work-plan"]
        self.assertIn("· 🧭 Plan<", work)
        self.assertIn("use /haipipe-paper-plan", work)
        self.assertIn('class="fd-btn pb-copy"', work)                 # the shared Prompt box (ui_parts.prompt_box)
        self.assertIn("⚙️ Runs to do<", work)               # a title names the step, never a count
        self.assertNotIn(" of 2 open", work)
        self.assertIn("pb-pill you", work)              # T0 waits for you: an orange pill

    def test_idea_and_story_are_one_view_data_and_paper_flow_are_plan(self):
        # JL 261104: "add Idea + Story to be in one view, and Data flow and Paper flow to be one view of Plan"
        names = {k: n for k, (n, _) in board_views.board_report_views(self.b, self.root, lambda t, b: t).items()}
        self.assertEqual(names["story"], "Story")
        self.assertEqual(names["plan"], "Data + Paper Plan")
        for gone in ("dataflow", "paperflow", "venue"):
            self.assertNotIn(gone, names)
        for rel, text in (("s01-ideation/s01-ideation.md", IDEA), ("s04-paper-workflow/s04-paper-workflow.md", PAPERFLOW),
                          ("s04-paper-workflow/s04-paper-workflow.mindmap.md", "# <a map>\n"),
                          ("s03-paper-dataflow/s03-paper-dataflow.mindmap.md", "# <a map>\n")):
            (self.b / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.b / rel).write_text(text, encoding="utf-8")
        (self.b / "s01-ideation" / "s01-ideation.png").write_bytes(b"x")
        (self.b / "s02-story-desk-idea" / "s02-story-desk-idea.png").write_bytes(b"x")
        md = lambda text, base: text
        views = board_views.board_report_views(self.b, self.root, md)
        self.assertEqual(views["idea"][0], "Idea")                      # each its own button (JL 261105: "I mean seperate this!!!")
        story = views["story"][1]()
        # JL 261104: "why the mind map is not at the top and should be embedded, and where are the studios here?"
        idea = views["idea"][1]()
        self.assertIn("🎨 Studio<", idea)                                # JL 261105: "idea for multiple direction, story for one direction"
        self.assertNotIn("🧭 Direction<span", idea)                     # a bar's title, then its state word (261106)
        self.assertLess(story.index("🎨 Studio<"), story.index("🧭 Direction<span"))
        self.assertIn("Open in Studio", story)
        self.assertNotIn("Open the mind map", story)
        self.assertEqual(story.count("<hr class=pb-rule>"), 0)          # nothing left to put under a rule
        self.assertNotIn("Roadmap", story)                              # the Plan's now (s32-D35)
        self.assertNotIn("Hand-off", story)
        plan = views["plan"][1]()
        self.assertEqual([x for x in re.findall(r"<h3 class=fd-h>(\d+) · ([^<]+)<", plan)][:2], [("1", "🗄️ Data flow"), ("2", "📝 Paper flow")])
        self.assertIn("Roadmaps<span", plan)
        work = board_views.board_work_views(self.b, self.root, md)
        page = work["work-plan"][1]()
        self.assertIn("🧭 Plan<", page)
        self.assertIn("🗓️ Next steps to the send<", page)
        self.assertIn("⚙️ Runs to do<", page)
        self.assertNotIn("🧰 Skills that do it<", page)                 # the rail's Skills section holds them (261105)
        self.assertIn("&lt;an open idea&gt;", work["work-idea"][1]())
        opens = work["work-story"][1]()
        self.assertIn("&lt;an open story point&gt;", opens)
        self.assertEqual(opens.count("📌 Open points<"), 1)               # one name for open items (261105)

    def test_related_is_the_last_numbered_section_of_idea_and_story(self):
        # JL 261104: "could you put the related section to be here?"; one card per `bears on`, a kept PDF opens that PDF
        self.assertNotIn("📚 Related<", self.report["story"])           # no related/ folder, no section
        rel = self.b / "related"
        (rel / "papers").mkdir(parents=True)
        (rel / "papers" / "kept.pdf").write_bytes(b"%PDF-1.4")
        (rel / "related.md").write_text(
            "| kind | date | item | link | bears on | key | venue | why here |\n|---|---|---|---|---|---|---|---|\n"
            "| paper | 2020 | Kept 2020 | `papers/kept.pdf` | Closest: type one | ★ | Journal A | because A |\n"
            "| paper | 2021 | Web 2021 | https://doi.org/10.1/x | Closest: type two |  |  |  |\n"
            "| paper | 2022 | Bare 2022 |  | Shared background: type three |  |  |  |\n"
            "| paper | 2023 | Arxiv 2023 | https://arxiv.org/abs/2304.08593 | Closest: type two |  |  |  |\n", encoding="utf-8")
        md = lambda text, base: text
        story = dict(board_views.board_report_views(self.b, self.root, md))["story"][1]()
        topic = self.b / 's01-ideation'
        topic.mkdir()
        (topic / 's01-ideation.md').write_text(IDEA)
        idea = dict(board_views.board_report_views(self.b, self.root, md))["idea"][1]()
        self.assertIn('📚 Related', idea)              # remains in Idea even after a Story exists
        self.assertIn('Kept 2020', idea)
        nums = [int(x) for x in re.findall(r"<h3 class=fd-h>(\d+) · ", story.split("<hr class=pb-rule>")[0])]
        self.assertIn(f"{max(nums)} · 📚 Related", story)
        for head in ("Closest: type one", "Closest: type two", "Shared background: type three"):
            self.assertIn(head, story)
        part = story.split("📚 Related")[1]
        self.assertIn("pb-side", part)                                 # left tabs, right content
        self.assertNotIn("<div class=pb-tiles", story)                 # no card tabs left anywhere in the view
        self.assertRegex(part, r'<iframe class=pb-relpdf title="Kept 2020" data-src="/[^"]*related/papers/kept.pdf">')
        self.assertRegex(part, r'data-pop="Kept 2020" href="/[^"]*related/papers/kept.pdf"[^>]*>Pop out')
        self.assertIn('data-src="https://arxiv.org/pdf/2304.08593"', part)  # an abstract page cannot be framed, its PDF can
        self.assertIn('data-pop="Arxiv 2023" href="https://arxiv.org/pdf/2304.08593"', part)
        self.assertIn('href="https://doi.org/10.1/x"', part)           # a publisher links out, no frame that would refuse
        self.assertNotIn('data-src="https://doi.org', part)
        self.assertNotIn(' src="', part.split("<script>")[1].split("</script>", 1)[1])   # nothing loads until its tab shows
        self.assertEqual(part.count("<iframe"), 2)
        self.assertIn("because A", story)
        self.assertIn("Journal A", story)

    def test_section_story_is_shared_with_displays_without_a_display_job(self):
        from live import board_results
        face = self.b / 's02-story-desk-idea/s02-story-desk-idea.md'
        face.write_text(face.read_text() + '\n## Section narrative\n\nA shared section argument.\n')
        for render in (board_results.story_view, board_results.displays_view):
            page = render(self.b, self.root, lambda text, base: text)
            self.assertIn('🧠 Story by Section', page)
            self.assertIn('A shared section argument.', page)
            self.assertEqual(page.count('🧠 Story by Section'), 1)
        displays = board_results.displays_view(self.b, self.root, lambda text, base: text)
        heads = re.findall(r'<h3 class=fd-h>\d+ · ([^<]+)', displays)
        self.assertEqual(heads[-1].strip(), '🧠 Story by Section')     # last in Displays (JL 261109)
        self.assertNotIn('Where each display stands', displays)
        from live import board_process
        for key in ('evidence', 'displays'):                           # no second list of the tabs' own states
            self.assertEqual(board_process._steps(self.b, key, None, '', self.root, lambda t, b: t), ('', []))
        self.assertEqual(board_results.sections_word([], self.root), ('nothing yet', ''))

    def test_story_by_section_opens_with_the_story_arc(self):
        """JL 261109: the first tab is the whole paper's story arc: `#### Story arc`, else the opening text block."""
        from live import board_results as br
        arc = br._story_arc(self.b, "#### Story arc\n\n1. **Puzzle**: p\n\n#### Claims\n\n| claim |\n")
        self.assertIn("Puzzle", arc)
        self.assertNotIn("claim", arc)
        spine = br._story_arc(self.b, "A note.\n\n```text\nHEADLINE  C4\n```\n\n#### 8.1 · Claims\n")
        self.assertIn("HEADLINE  C4", spine)
        self.assertIn("haipipe-paper-story", br._story_arc(self.b, "| claim | proposition |\n"))

    def test_each_section_tells_its_part_of_the_arc_before_its_claims(self):
        """JL 261109: "this is not just the claims, it is also about the narratives, the arc, how to make it smooth"."""
        from live import board_results as br
        v = self.b / 'j11_writing_v0101_x'
        (v / 't01_introduction').mkdir(parents=True, exist_ok=True)
        (v / 'j11_writing_v0101_x.md').write_text(
            '# v\n\n## Narrative\n\n| Section | reader question | entry | ordered moves | must refuse | displays | exit |\n'
            '|---|---|---|---|---|---|---|\n| t01_introduction | Why ask? | Has the abstract. | a → b → c | "first" | none |'
            ' accepts the gap |\n')
        (v / 't01_introduction' / 't01_introduction.md').write_text('# t01\n\ntransition-out: Results opens on the law\n')
        body = '| claim | proposition | lands in |\n|---|---|---|\n| C1 | The main claim | Introduction |\n'
        html = br._narrative(self.b / 's02-story-desk-idea', self.root, body)
        self.assertIn('accepts the gap', html.split('data-pbpanel')[0])          # the tab's line: what the reader leaves with
        panel = html[html.index('Why ask?'):]
        self.assertLess(panel.index('a → b → c'), panel.index('The main claim'))  # the arc first, the claims last
        self.assertIn('Results opens on the law', panel)                        # the Section face's hand-on

    def test_the_large_line_of_a_direction_is_never_its_glossary(self):
        from live.board_read import _lead_sentence
        lead, rest = _lead_sentence("**Direction**: what it asks.\n\nGLP-1 = a drug class.\n\nThe paper asks who lets it through.")
        self.assertEqual(lead, "The paper asks who lets it through.")
        self.assertIn("GLP-1 = a drug class.", rest)

    def test_interaction_is_a_section_with_a_tab_per_question(self):
        from live import focus_page as fp, interaction_section as IX
        view = lambda: IX.interaction_section(fp.interactions(self.b, self.root), self.root, 7)
        self.assertEqual(view(), "")                                    # no collection Run, no section
        run = self.b / "runs" / "r01_collect_story"
        (run / "result").mkdir(parents=True)
        (run / "run.yaml").write_text("status: waiting\n", encoding="utf-8")
        (run / "r01_collect_story.html").write_text("<html></html>", encoding="utf-8")
        (run / "question_collection.md").write_text(
            f"# Story asks\n\nfor: {self.b.name}-s02:paper @ story\n\n## Q1 · First\n\nWhy.\n\n**Which one?**\n\n- [ ] A · Aa\n- [ ] B · Bb\n\n"
            "## Q2 · Second\n\nWhy.\n\n**Which two?**\n\n- [ ] A · Cc\n- [ ] B · Dd\n", encoding="utf-8")
        page = view()
        # what waits is the bar's state word, and its first question shows under the closed bar (JL 261106)
        self.assertIn('7 · 🙋 Interaction<span class="word you">2 wait for you</span></h3><p class=fd-wait>🙋 Story asks: Q1 · First</p>', page)
        self.assertIn('data-ixq="Q1"><b>Q1 · First</b>', page)
        self.assertIn('data-ixq="Q2"><b>Q2 · Second</b>', page)
        self.assertEqual(page.count("class=pb-ixframe title"), 1)       # one form, one Copy
        self.assertIn(">waiting<", page)
        self.assertIn('<details class="pb-ixset waits" data-ixset="0" data-live=1 open>', page)   # a set folds in one list
        (run / "result" / "answer_collection.md").write_text(
            "# Story asks · answers\n\n## Q1 · First\n\n- [ ] A · Aa\n- [x] B · Bb\n\n## Q2 · Second\n\nAnswer: my own decision.\n", encoding="utf-8")
        page = view()
        self.assertNotIn("waiting for you", page)
        self.assertIn("7 · 🙋 Interaction<span class=word>answered</span></h3><style>", page)
        self.assertIn(">B · Bb<", page)
        self.assertIn(">my own decision<", page)

    def test_idea_and_story_each_have_a_theory(self):
        # JL 261105: "for both of them, we should have the section named theory as well"; "espeically for the IS"
        from live import board_results as BR
        self.assertEqual(BR._direction_theory({"reason": "Theory: trait activation. JL liked it."}), "trait activation")
        self.assertEqual(BR._direction_theory({"theory": "`accountability`", "reason": "Theory: other."}), "accountability")
        self.assertEqual(BR._direction_theory({"reason": "Lost on data."}), "")
        md = lambda text, base: text
        idea_dir = self.b / "s01-ideation"
        idea_dir.mkdir()
        (idea_dir / "s01-ideation.md").write_text(IDEA, encoding="utf-8")
        views = board_views.board_report_views(self.b, self.root, md)
        self.assertIn("🎓 Theory<span class=word>not written yet</span>", views["idea"][1]())
        story = views["story"][1]()
        self.assertIn("🎓 Theory<span class=word>not written yet</span>", story)
        self.assertIn("No theory written yet", story)
        self.assertNotIn("information systems journal", story)          # the fixture's journal is no IS journal
        (self.b / "board.md").write_text("# Paper-X\n\nboard-kind: paper-board\nvenue: MISQ\n", encoding="utf-8")
        self.assertIn("MISQ is an information systems journal", views["story"][1]())
        face = self.b / "s02-story-desk-idea" / "s02-story-desk-idea.md"
        face.write_text("# s02\n\n### 1 · Identity\n\n**Theory**: <a theory>.\n", encoding="utf-8")
        story = views["story"][1]()
        self.assertIn("<a theory>.", story)
        self.assertNotIn("No theory written yet", story)

    def test_next_number_counts_the_last_band_only(self):
        from live.interaction_section import next_number
        self.assertEqual(next_number("<h3 class=fd-h>1 · a</h3><h3 class=fd-h>2 · b</h3>"), 3)
        self.assertEqual(next_number("<h3 class=fd-h>5 · a</h3><h3 class=pb-group>R</h3><h3 class=fd-h>1 · b</h3>"), 2)
        self.assertEqual(next_number("<h3 class=fd-h>Plain</h3>"), 0)

    def test_a_board_with_only_one_part_still_shows_the_view(self):
        names = board_views.board_report_views(self.b, self.root, lambda t, b: t)
        self.assertIn("story", names)                                   # no Idea topic here, the Story alone
        self.assertIn("plan", names)                                    # no Paper flow topic here, the Data flow alone

    def test_phone_rules_come_after_the_base_rules(self):
        css = ui_parts.PB_CSS
        self.assertLess(css.index(".pb-side{display:grid"), css.index(".pb-side{grid-template-columns:minmax(0,1fr)}"))
        self.assertLess(css.index(".pb-flow{position:relative"), css.index(".pb-flow{grid-template-columns:1fr}"))

class AddressLinksTest(unittest.TestCase):
    """Every bNN.jNN.tNN in a paper Board view is a link to its folder's focus page (address_links, JL 261103)."""

    def test_roadmap_address_links_to_its_task(self):
        import html
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            b = board(root)
            (root / "project.yaml").write_text("name: <a Project>\n", encoding="utf-8")
            (root / "work" / "b11_x" / "j25_y" / "t01_z").mkdir(parents=True)
            md = lambda text, base: html.escape(text)
            for views in (board_views.board_report_views(b, root, md), board_views.board_work_views(b, root, md)):
                page = next(f() for k, (_, f) in views.items() if k.endswith("plan"))      # the Roadmaps are the Plan's (s32-D35)
                self.assertIn('<a class=addr-link href="/_board/workbench?path=work/b11_x/j25_y/t01_z&amp;layout=focus" '
                              'target="_top">b11.j25.t01</a>', page)
                self.assertIn('path=work/b11_x/j25_y&amp;layout=focus" target="_top">b11.j25.t02</a>', page)   # no such Task: its Job


class JobNameFormsTest(unittest.TestCase):
    """Support blocks reads a Job however the pages write it (JL 261102: it missed every b51 Job)."""

    def test_dot_space_and_range(self):
        from live import board_read as R
        self.assertEqual(R.DOT_REF.findall("b51.j04.t02 and b51 j07 t02 and b01 j11"),
                         [("51", "04", "02"), ("51", "07", "02"), ("01", "11", "")])
        self.assertEqual(R.RANGE_REF.findall("b01 j11 to j14; b01 j20-j23"), [("01", "11", "14"), ("01", "20", "23")])


if __name__ == "__main__":
    unittest.main()


class StoryListsTest(unittest.TestCase):
    def test_a_story_that_starts_at_rq0_keeps_its_numbers(self):
        """A setup question RQ0 (haipipe-paper-story) is RQ0, and its narrative item is paired by number, not position."""
        from live import board_read
        body = ("**The story, question by question:**\n0. <a setup question>? set up\n1. <a question>? open\n\n"
                "**The narrative:**\n0. <what RQ0 says>\n1. <what RQ1 says>\n")
        qs, said = board_read._rq_lists(body)
        self.assertEqual([k for k, _ in qs], [0, 1])
        self.assertEqual(said[0], "<what RQ0 says>")


def test_a_discovery_block_named_alone_shows_every_paper(tmp_path):
    """JL 261108: the Discovery section showed the Block and nothing under it; it shows each Job, Task and paper."""
    import board_results
    proj = tmp_path / "Project-X"
    run = proj / "discovery" / "b01_evidence" / "j01_landscape" / "t01_trait" / "runs" / "r01_smith2020"
    (run / "result").mkdir(parents=True)
    (run / "result" / "r01_smith2020.bib").write_text("@article{s, title={Doctors and {Opioids}}, year={2020}}")
    (run / "result" / "runtime.yaml").write_text("status: complete\n")
    board = proj / "paper" / "Paper-X"
    board.mkdir(parents=True)
    (board / "board.md").write_text("# X\n\nReads discovery/b01_evidence.\n")
    html = board_results.explore_view(board, tmp_path, "")
    assert "r01_smith2020" in html and "Doctors and Opioids" in html
