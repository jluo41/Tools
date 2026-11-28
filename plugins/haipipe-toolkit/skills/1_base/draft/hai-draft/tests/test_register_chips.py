"""Evidence-page divisions render their bindings as evidence cards (JL 260806).

Inside an evidence page's `### E<n> ·` division, and only there, a backticked
binding token becomes a chip: a bibliography key opens the cite card, a
tasks//discoveries/ path opens a val card whose links are the provenance
paths. Everything else in backticks, and every binding token outside an E
division, keeps its ordinary rendering. The page-level gate is body.EVIDENCE,
set from the head `route: outward|inward` line by page_question.
"""
import tempfile
import unittest
from pathlib import Path

from src import body as _bd
from src.body import body, note_body
from src.dialect_paper import Paper

BIB = """@article{luo2025mapping,
  title = {Mapping Patient-Perceived Physician Traits},
  author = {Luo, Jia},
  year = {2025},
  journal = {arXiv},
}
"""


class RegisterChipTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        (root / "paper.bib").write_text(BIB, encoding="utf-8")
        qa = root / "tasks" / "T1" / "QA"
        qa.mkdir(parents=True)
        (qa / "1-answer.md").write_text("state: answered\n\nthe digest\n",
                                        encoding="utf-8")
        self.paper = Paper(root)
        self._prev = (_bd.PAPER, _bd.BASE, _bd.EVIDENCE)
        _bd.PAPER, _bd.BASE = self.paper, root
        _bd.EVIDENCE = True     # the page under test declares route: outward

    def tearDown(self):
        _bd.PAPER, _bd.BASE, _bd.EVIDENCE = self._prev
        self._tmp.cleanup()

    # -- the dialect resolves ------------------------------------------------
    def test_bib_key_resolves_to_the_cite_binding(self):
        kind, state, label, _tip, meta = self.paper.register_binding("luo2025mapping")
        self.assertEqual(("cite", "ok", "luo2025mapping"), (kind, state, label))
        self.assertIsNotNone(meta.get("entry"))

    def test_key_shaped_token_that_misses_renders_broken(self):
        kind, state, *_ = self.paper.register_binding("nobody2020nothing")
        self.assertEqual(("cite", "broken"), (kind, state))

    def test_bank_path_resolves_with_answer_and_run_links(self):
        kind, state, label, _tip, meta = self.paper.register_binding(
            "tasks/T1/QA/1-answer.md")
        self.assertEqual(("val", "ok", "QA/1-answer.md"), (kind, state, label))
        self.assertEqual(["answer · 1-answer.md", "run · T1/"],
                         [name for name, _p in meta["files"]])

    def test_missing_bank_path_renders_owed_never_invented(self):
        kind, state, *_ = self.paper.register_binding("tasks/T1/QA/missing.md")
        self.assertEqual(("val", "owed"), (kind, state))

    def test_non_binding_shapes_stay_ordinary_code(self):
        self.assertIsNone(self.paper.register_binding("Q-Seed-1"))
        self.assertIsNone(self.paper.register_binding("probes/L01-x/entry.md"))
        self.assertIsNone(self.paper.register_binding("v0618"))

    # -- the board renders, register-scoped ----------------------------------
    def test_register_mode_chips_and_plain_mode_does_not(self):
        row = "- ⬜ stake · `luo2025mapping` and `tasks/T1/QA/1-answer.md`"
        chipped = body(row, register=True)
        self.assertIn("chip cite ok", chipped)
        self.assertIn("chip val ok", chipped)
        plain = body(row)
        self.assertNotIn("chip cite", plain)
        self.assertNotIn("chip val", plain)

    def test_own_heading_toggles_register_mode_on_and_off(self):
        txt = ("### E1 · is the measure novel?\n"
               "#### consumers\n"
               "- ⬜ stake · `luo2025mapping`\n"
               "### Something else\n- `luo2025mapping` again\n")
        html = body(txt)
        self.assertEqual(1, html.count("chip cite ok"))

    def test_e_division_stays_plain_off_an_evidence_page(self):
        _bd.EVIDENCE = False    # same division, page head carries no route:
        txt = ("### E1 · is the measure novel?\n"
               "- ⬜ stake · `luo2025mapping`\n")
        self.assertNotIn("chip cite", body(txt))

    def test_log_stays_chip_free(self):
        html = note_body("- 260806 · quoted `luo2025mapping` in a log line",
                         register=True)
        self.assertNotIn("chip cite", html)


if __name__ == "__main__":
    unittest.main()
