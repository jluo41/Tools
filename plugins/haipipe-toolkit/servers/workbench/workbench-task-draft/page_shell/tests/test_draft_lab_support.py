"""Draft Lab against haipipe-paper ref/must-check.md M-D18: every VALUE, CITE and DISPLAY in a Section renders with
its support state. A DISPLAY Result (results/re-display-<n>/) answers \\ref with its name and shows its picture and Run;
an Extended Data name is a reference to its Section; each evidence item that targets a sentence is resolved or not; a
printed number no VALUE item covers is marked; a citation the citation Job has not verified carries a quiet mark; an old
key in a card raises none. Every case runs on a temp Draft."""
from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap
bootstrap()

from live import task_draft  # noqa: E402
from live.draft_card_text import ref_names  # noqa: E402
from src import float_image  # noqa: E402
from src.result_displays import ref_map, web_figures  # noqa: E402

TESTS = Path(__file__).resolve().parents[5] / "skills" / "1_base" / "draft" / "haipipe-draft" / "tests"

BOARD = "Project-X/paper/Paper-Demo"
DRAFT = ("# Note · draft v1.0\n\n## 3 · Draft\n\n### C1.P1 · Data · s1 to s3\n"
         "- B1 · s1 · We used 2,660 patients (Fig. \\ref{fig:study}).\n"
         "- B2 · s2 · Tokens grow past one epoch (Extended Data Table 1), as \\ref{fig:study} shows, Figure~\\ref{fig:study}.\n"
         "- B3 · s3 · The error fell by 8.2% at 5 minutes.\n\n### C1.P2 · Work · s4 to s5\n"
         "- B1 · s4 · Scaling helps language models \\citep{kaplan2020,hoffmann2022}.\n"
         "- B2 · s5 · It also helps wearables \\citep{kaplan2020}.\n")
ITEMS = ("# t02_note · evidence items\n\n"
         "### E01-VALUE-study · C1.P1.B1 · Patients\n- **Target**: C1.P1.B1\n- **Label**: Patients\n"
         "- **Expected**: VALUE · j02_value/t01_q/runs/r16_values/result/values.md (V_patients 2,660)\n"
         "- **Verified**: ✅ checked\n\n"
         "### E02-DISPLAY-fig1 · C1.P1.B1 · Figure 1: study\n- **Target**: C1.P1.B1, C1.P1.B2\n"
         "- **Expected**: DISPLAY · j01_display/t05_study/runs/r07_study/result\n"
         "- **Local Run**: display unit → results/re-display-1\n\n"
         "### E03-VALUE-gone · C1.P1.B2 · Tokens\n- **Target**: C1.P1.B2\n"
         "- **Expected**: VALUE · j02_value/t09_gone/runs/r01_values/result/values.md (V_tokens)\n")
BIB = ("@article{kaplan2020,\n  author = {Kaplan, Jared and McCandlish, Sam and Henighan, Tom},\n  year = {2020},\n}\n"
       "@article{hoffmann2022,\n  author = {Hoffmann, Jordan and Borgeaud, Sebastian and Mensch, Arthur},\n  year = {2022},\n}\n")
CSV = ("key,group,status,cited_in,sentences,bib_entry,bib_in,in_reference_bib,doi,doi_conflict,title,year,doi_record,"
       "verified,cite_card,card_gaps,discovery_runs\n"
       "kaplan2020,t01,verified,,1,yes,,yes,,,T,2020,,JL · t02_note run-citation-1,,,\n"
       "hoffmann2022,t01,card-only,,1,yes,,yes,,,T,2022,,nobody yet,,,\n")


def _paper(root: Path) -> Path:
    board = root / BOARD
    task = board / "j11_writing_v1" / "t02_note"
    (task / "draft" / "records").mkdir(parents=True)
    (task / "draft" / "evidence" / "bibex").mkdir(parents=True)
    (board / "board.md").write_text("# Paper\n")
    (task / "t02_note.md").write_text("# t02_note · Note\n\nfolder-kind: task\ntask-type: draft\n")
    (task / "draft" / "t02_note-draft-v1.0.md").write_text(DRAFT)
    (task / "draft" / "t02_note-evidence-items.md").write_text(ITEMS)
    (task / "draft" / "evidence" / "bibex" / "page.bib").write_text(BIB)
    # an old pass's card cites a key the current Draft no longer has: plain text, no mark
    (task / "draft" / "records" / "t02_note-revise.md").write_text(
        "# t02_note · revise\n\n## Pass 1 · 261101 · on draft v0.5\n\n### Edit · s4 · old\nstate: rejected\n"
        "Original: \"As \\citep{Gone_2019} said.\"\nExpected: \"As said.\"\n")
    # the DISPLAY Result, as frame_section_displays.py writes it
    res = task / "results" / "re-display-1"
    unit = res / "payload" / "Display1-study"
    (unit / "assets").mkdir(parents=True)
    (res / "result.yaml").write_text("item: E02-DISPLAY-fig1\ntype: DISPLAY\nstatus: ready\n"
                                     "source: j01_display/t05_study/runs/r07_study/result\npayload:\n  unit: Display1-study\n")
    (unit / "float.tex").write_text("\\begin{figure}\n\\includegraphics{assets/figure.pdf}\n"
                                    "\\caption{\\textbf{Study design.} Patients by source.}\n\\label{fig:study}\n\\end{figure}\n")
    (unit / "README.md").write_text("# Display1-study\n\n## Placement\n\nFigure 1\n")
    (unit / "assets" / "figure.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    # the Runs the items name: E01's value file holds its id, E02's Run is there; E03's file is not
    vals = board / "j02_value/t01_q/runs/r16_values/result"
    vals.mkdir(parents=True)
    (vals / "values.md").write_text("V_patients = 2,660\n")
    (board / "j01_display/t05_study/runs/r07_study/result").mkdir(parents=True)
    # the extended-data Section of the same version, and the citation Job's check
    (board / "j11_writing_v1" / "t21_extended-data").mkdir()
    cite = board / "j03_evidence_cite/t99_paper_citation_check/runs/r01_check_citations/result"
    cite.mkdir(parents=True)
    (cite / "citations.csv").write_text(CSV)
    return task


def _html(root: Path, task: Path) -> str:
    return task_draft.draft_task_spaces(task, root, "5 · Revise")["Work Details"].html


def _row(html: str, addr: str) -> str:
    return re.search(r'(?s)<li data-s="[^"]*" data-a="' + re.escape(addr) + r'".*?</li>', html).group(0)


class DisplayResultTest(unittest.TestCase):
    def test_a_ref_reads_its_figure_and_the_box_shows_the_unit_and_its_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            task = _paper(Path(tmp))
            html = _html(Path(tmp), task)
            visible = re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style)\b.*?</\1>", "", html))
            self.assertNotIn("\\ref{", visible)
            self.assertIn('Fig. <span class=cite-ref title="fig:study">1</span>', html)       # after "Fig.": the number
            self.assertIn('as <span class=cite-ref title="fig:study">Figure 1</span> shows', html)   # alone: the name
            self.assertIn('Figure\u00a0<span class=cite-ref title="fig:study">1</span>', html)       # LaTeX's tie
            self.assertNotIn("no unit in display/", html)
            emb = re.findall(r'(?s)<li class="disp-embed[^"]*"><figure>.*?</figure>', html)
            self.assertEqual(len(emb), 1)
            self.assertIn("figure.png", emb[0])                     # no preview.pdf: the unit's own picture
            self.assertIn("<figcaption>Figure 1 · t05 r07</figcaption>", emb[0])
            self.assertNotIn("Patients by source.</figcaption>", emb[0])    # no caption rebuilt in HTML (M-D18)

    def test_extended_data_is_a_reference_not_a_missing_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            task = _paper(Path(tmp))
            html = _html(Path(tmp), task)
            self.assertIn('<span class=disp-xref title="in t21_extended-data">Extended Data Table 1</span>', html)
            self.assertNotIn("<b>Table 1</b>", html)
            self.assertNotIn("not made yet", html)

    def test_draft_lab_and_the_web_lane_read_the_same_units(self):
        with tempfile.TemporaryDirectory() as tmp:
            task = _paper(Path(tmp))
            self.assertEqual(ref_names(task), ref_map(task))
            self.assertEqual(ref_map(task), {"fig:study": "Figure 1"})
            web = web_figures("<p>Patients (Fig. \\ref{fig:study}).</p><p>Again \\ref{fig:study}.</p>", task)
            self.assertIn("(Fig. 1).</p><figure", web)
            self.assertIn("Again Figure 1.", web)
            self.assertEqual(web.count('class="page-display"'), 1)
            self.assertIn("data:image/png;base64,", web)


class FloatBoxTest(unittest.TestCase):
    """The box shows the typeset float, page 1 of the unit's preview.pdf cut to its float, at full width, with one
    line under it (its name and Run); a LaTeX caption never leaks into the page."""

    def setUp(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("trd", TESTS / "test_result_displays.py")
        self.trd = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.trd)
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.old_cache = float_image.CACHE
        float_image.CACHE = self.root / "_float-cache"
        self.task = _paper(self.root)
        unit = self.task / "results" / "re-display-1" / "payload" / "Display1-study"
        (unit / "float.tex").write_text("\\begin{figure}\n\\caption{\\textbf{Study.} A 95\\% interval.}\n"
                                        "\\label{fig:study}\n\\end{figure}\n")
        self.pdf = self.trd.paper_page(unit / "preview.pdf")

    def tearDown(self):
        float_image.CACHE = self.old_cache
        self.tmp.cleanup()

    def _box(self):
        html = _html(self.root, self.task)
        emb = re.findall(r'(?s)<li class="disp-embed[^"]*"><figure>.*?</figure>', html)
        self.assertEqual(len(emb), 1)
        return html, emb[0]

    def test_the_box_is_the_float_image_and_its_run_line(self):
        if not float_image.can_rasterize():
            self.skipTest("no PyMuPDF and no pdftoppm")
        html, box = self._box()
        rel = self.pdf.relative_to(self.root).as_posix()
        self.assertIn('src="/_board/float?path=' + rel.replace(" ", "%20") + '" loading=lazy', box)
        self.assertIn('alt="Study. A 95% interval."', box)
        self.assertIn("<figcaption>Figure 1 · t05 r07</figcaption>", box)
        self.assertNotIn("\\%", html)
        png = float_image.float_png(self.pdf)                     # what the route serves: the cut float
        self.assertTrue(png and self.root / "_float-cache" in png.parents)

    def test_without_a_rasterizer_the_box_shows_the_unit_picture(self):
        old = float_image._fitz, float_image._pdftoppm
        float_image._fitz, float_image._pdftoppm = (lambda: None), (lambda: "")
        try:
            html, box = self._box()
        finally:
            float_image._fitz, float_image._pdftoppm = old
        self.assertNotIn("/_board/float", box)
        self.assertIn("assets/figure.png", box)
        self.assertIn("<figcaption>Figure 1 · t05 r07</figcaption>", box)
        self.assertNotIn("\\%", html)


class ValueChipTest(unittest.TestCase):
    def test_each_item_on_a_sentence_says_resolved_or_not_and_a_loose_number_says_no_item(self):
        with tempfile.TemporaryDirectory() as tmp:
            task = _paper(Path(tmp))
            html = _html(Path(tmp), task)
            s1, s2, s3 = (_row(html, a) for a in ("C1.P1.s1", "C1.P1.s2", "C1.P1.s3"))
            self.assertNotIn("ev-sup", s1)                         # all resolve: nothing beside the row's 📊 ❝ marks
            self.assertIn('class="ev-chip miss" tabindex=0 title="E03 VALUE"', s2)   # bound, its file is gone
            self.assertNotIn('title="E02 DISPLAY"', s2)                # a resolved item draws no chip (JL 261115)
            self.assertIn("not found: j02_value/t09_gone/runs/r01_values/result/values.md", s2)
            self.assertNotIn('class="ev-chip none"', s3)           # 8.2% and 5, no VALUE item: no ⚠ on the page
            self.assertNotIn("ev-sup", s3)
            self.assertNotIn("ev-sup", _row(html, "C1.P2.s4"))     # no number, no item: nothing


class CiteStateTest(unittest.TestCase):
    def test_an_unverified_key_gets_one_quiet_mark_and_an_old_card_key_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            task = _paper(Path(tmp))
            html = _html(Path(tmp), task)
            s4, s5 = _row(html, "C1.P2.s4"), _row(html, "C1.P2.s5")
            self.assertIn("(Kaplan et al. 2020; Hoffmann et al. 2022)", s4)
            self.assertEqual(s4.count("class=cite-unv"), 1)
            self.assertIn("hoffmann2022: card-only", s4)
            self.assertNotIn("kaplan2020:", s4)
            self.assertNotIn("cite-unv", s5)                       # verified by the citation Job
            self.assertNotIn(">not in Bib<", html)                 # Gone_2019 lives only in an old card


if __name__ == "__main__":
    unittest.main()
