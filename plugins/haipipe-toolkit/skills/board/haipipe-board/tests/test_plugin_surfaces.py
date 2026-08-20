"""Plugin surfaces expose material and report honest lifecycle counts."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

from live.export import ExportMixin
from live.plugview import _display_state, _probe_body_html


class PluginSurfaceTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_probe_body_is_visible_but_metadata_is_not_duplicated(self):
        html = _probe_body_html(
            "# PP01-example\nstate: bound\nquestion: What?\n"
            "binding: `task/QA/a.md`\n\n"
            "This **Probe** owns `OLS`.\n\n- first fact\n- second fact\n"
        )
        self.assertIn("This <strong>Probe</strong> owns <code>OLS</code>.", html)
        self.assertIn("<li>first fact</li>", html)
        self.assertNotIn("state: bound", html)
        self.assertNotIn("question: What?", html)

    def test_display_state_distinguishes_declared_rendered_and_accepted(self):
        unit = self.root / "Q-Display1-result"
        (unit / "intake" / "inputs").mkdir(parents=True)
        (unit / "intake" / "manifest.yaml").write_text("sources: []\n")
        state = _display_state(unit, [("accepted", "⬜ pending")])
        self.assertFalse(state["rendered"])
        self.assertIn("INTAKE missing", state["next"])

        (unit / "intake" / "inputs" / "values.csv").write_text("x\n1\n")
        (unit / "recipe").mkdir()
        (unit / "recipe" / "render.py").write_text("# recipe\n")
        (unit / "assets").mkdir()
        (unit / "assets" / "table-body.tex").write_text("value\\\\\n")
        (unit / "preview.pdf").write_bytes(b"%PDF")
        state = _display_state(unit, [("accepted", "⬜ pending")])
        self.assertTrue(state["rendered"])
        self.assertFalse(state["accepted"])
        self.assertIn("ACCEPT pending", state["next"])

        state = _display_state(unit, [("accepted", "✅ JL 2026-08-16")])
        self.assertTrue(state["accepted"])


class WordTitleTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.page = self.root / "QV2.md"
        self.page.write_text(
            "# Full Page Title: OLS, IV, and DID\n\n"
            "## Content\n\n### 1 Results\n\nOne paragraph.\n"
        )
        self.out = self.root / "word"
        self.out.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def test_board_word_caller_passes_canonical_h1_as_document_title(self):
        outer = self

        class Fake(ExportMixin):
            calls = []

            def _export_target(self, _p, _plugin):
                return outer.page, outer.out, None, None

            def _canon_ctx(self, _board, _p):
                return {}

            def _paper_root(self, _page):
                return None

            def _page_units(self, _page):
                return []

            def _run(self, cmd, **_kwargs):
                self.calls.append(cmd)
                if "-o" in cmd:
                    target = Path(cmd[cmd.index("-o") + 1])
                    target.write_bytes(b"artifact")
                return 0, "ok"

            def _rebuild_ui(self, _route, _p):
                return "", ""

            def _url_of(self, path):
                return str(path)

        fake = Fake()
        result, err = fake.export_word({})
        self.assertIsNone(err)
        self.assertTrue(result["docx"].endswith("QV2.docx"))
        cmd = fake.calls[0]
        self.assertEqual(
            cmd[cmd.index("--document-title") + 1],
            "Full Page Title: OLS, IV, and DID",
        )

    def test_writer_has_a_real_title_style(self):
        writer = (
            Path(__file__).resolve().parents[3]
            / "board" / "page-plugins" / "_shared-export" / "md2docx.py"
        )
        spec = importlib.util.spec_from_file_location("board_md2docx", writer)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        doc = module.Docx()
        doc.title("Full Page Title")
        self.assertIn('w:pStyle w:val="Title"', doc.body[0])
        self.assertIn("Full Page Title", doc.body[0])

    def test_writer_detexes_long_comparison_commands_without_residue(self):
        writer = (
            Path(__file__).resolve().parents[3]
            / "board" / "page-plugins" / "_shared-export" / "md2docx.py"
        )
        spec = importlib.util.spec_from_file_location("board_md2docx_detex", writer)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        rendered = module.detex(r"Total MME $\geq$ 500 and daily MME $\leq$ 90")
        self.assertEqual(rendered, "Total MME ≥ 500 and daily MME ≤ 90")
        self.assertNotIn("≥q", rendered)
        self.assertNotIn("≤q", rendered)

    def test_page_units_expose_local_and_full_display_aliases(self):
        display = self.root / "display" / "QV2-Display1-result"
        display.mkdir(parents=True)
        (display / "float.tex").write_text(
            "\\begin{table}[H]\\caption{Result}\\label{tab:qv2}\\end{table}"
        )

        class Fake(ExportMixin):
            pass

        units = Fake()._page_units(self.page)
        self.assertEqual(len(units), 1)
        self.assertEqual(units[0][0], "QV2-Display1")
        self.assertEqual(units[0][1]["aliases"], ["QV2-Display1", "Display1"])

    def test_display_mentions_are_ranked_by_source_order(self):
        body = (
            "% source QV2-Display9\n"
            "One paragraph cites Display2 and then Display4.\n\n"
            "\\begin{verbatim}\nDisplay1\n\\end{verbatim}\n"
        )
        fake = ExportMixin()
        display2 = {"aliases": ["QV2-Display2", "Display2"]}
        display4 = {"aliases": ["QV2-Display4", "Display4"]}
        hidden = {"aliases": ["QV2-Display9", "Display9"]}
        fenced = {"aliases": ["QV2-Display1", "Display1"]}
        self.assertLess(
            fake._first_unit_mention(body, display2).start(),
            fake._first_unit_mention(body, display4).start(),
        )
        self.assertIsNone(fake._first_unit_mention(body, hidden))
        self.assertIsNone(fake._first_unit_mention(body, fenced))

    def test_word_parser_reads_tabularx_without_leaking_tex_scaffolding(self):
        writer = (
            Path(__file__).resolve().parents[3]
            / "board" / "page-plugins" / "_shared-export" / "md2docx.py"
        )
        spec = importlib.util.spec_from_file_location("board_md2docx_table", writer)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        body = self.root / "table-body.tex"
        body.write_text(
            "\\begin{tabularx}{\\textwidth}{@{}X r@{}}\n"
            "\\toprule\nOutcome & Estimate \\\\\n"
            "\\midrule\n"
            "\\multicolumn{2}{@{}l}{\\textbf{Panel A}} \\\\\n"
            "\\addlinespace[-2pt]\nTotal MME & 9.3438 \\\\\n"
            "\\bottomrule\n\\end{tabularx}\n"
            "\\begin{minipage}{\\textwidth}Note outside table.\\end{minipage}\n"
        )
        rows, align = module.parse_table_body(body)
        rendered = " ".join(cell[0] for row in rows for cell in row)
        self.assertEqual(align, "@{}X r@{}")
        self.assertIn("Panel A", rendered)
        self.assertNotIn("tabularx", rendered)
        self.assertNotIn("multicolumn", rendered)
        self.assertNotIn("minipage", rendered)


if __name__ == "__main__":
    unittest.main()
