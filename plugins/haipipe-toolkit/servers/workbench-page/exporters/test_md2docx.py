#!/usr/bin/env python3
"""Regression checks for the shared Page-to-delivery reader."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import md2docx


class ParsePageTests(unittest.TestCase):
    def test_html_receipt_comment_is_not_delivery_prose(self):
        source = """# Example · §1 Introduction

## Content

### 1 · Introduction

#### P1. Opening

Visible sentence. <!-- realizes: C1.P1.B1 -->

## Aims
"""
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "Example.md"
            page.write_text(source)
            blocks, fenced = md2docx.parse_page(page)

        prose = [block[1] for block in blocks if block[0] == "p"]
        self.assertEqual(fenced, 0)
        self.assertEqual(prose, ["Visible sentence."])

    def test_displays_reads_v4_result_payload_units(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            unit = root / "results" / "re-display" / "payload" / "Display1-result"
            unit.mkdir(parents=True)
            (unit / "float.tex").write_text(
                r"\begin{table}[H]\caption{Result}\label{tab:v4}\end{table}"
            )
            (unit / "assets").mkdir()
            (unit / "assets" / "table-body.tex").write_text(
                "Outcome & Estimate \\\\\n"
            )

            displays = md2docx.Displays(root, extra_root=root / "results")

        self.assertIn("tab:v4", displays.by_label)
        self.assertIn("Display1-result", displays.by_unit)
        self.assertTrue(displays.by_unit["Display1-result"]["body"].endswith(
            "Display1-result/assets/table-body.tex"))

    def test_table_parser_keeps_shortstack_header_in_one_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            body = Path(tmp) / "table-body.tex"
            body.write_text(
                r"""\begin{tabular}{lcc}
 & \shortstack{(1)\\Basic} & \shortstack{(2)\\+Phys.} \\
\midrule
Outcome & 1 & 2 \\
\end{tabular}"""
            )

            parsed = md2docx.parse_table_body(body)

        self.assertIsNotNone(parsed)
        rows, _align = parsed
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][1][0], "(1) Basic")
        self.assertEqual(rows[0][2][0], "(2) +Phys.")

    def test_detex_drops_bibtex_penalty_number(self):
        ref = r"\emph{New England Journal of Medicine}, 376\penalty0 (7):\penalty0 663--673, 2017."
        self.assertEqual(md2docx.detex(ref),
                         "New England Journal of Medicine, 376 (7): 663–673, 2017.")

    def test_table_alignment_ignores_tex_modifier_commands(self):
        spec = (r"@{}>{\raggedright\arraybackslash}p{3.45cm}"
                r"*{6}{>{\centering\arraybackslash}X}@{}")
        self.assertEqual(md2docx._alignment_columns(spec), list("lcccccc"))


if __name__ == "__main__":
    unittest.main()


class DisplayPlacementTests(unittest.TestCase):
    def test_a_table_follows_the_whole_paragraph_that_first_cites_it(self):
        """S-MISQ-Main-5-Results 260928: a table placed after the citing SENTENCE cut the
        paragraph in two; the rest printed after the table as an orphaned paragraph."""
        import subprocess, sys, zipfile
        source = """# Example · §1 Results

## Content

### 1 · Results

#### P1. Estimates

Table \\ref{tab:x} reports the estimates. <!-- realizes: C1.P1.B1 -->
The second sentence reads them. <!-- realizes: C1.P1.B2 -->

#### P2. Next

A later paragraph. <!-- realizes: C1.P2.B1 -->

## Aims
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "Example.md"
            page.write_text(source)
            unit = root / "units" / "Display1-x"
            (unit / "assets").mkdir(parents=True)
            (unit / "float.tex").write_text(r"\begin{table}[H]\caption{Estimates}\label{tab:x}\end{table}")
            (unit / "assets" / "table-body.tex").write_text("Outcome & Estimate \\\\\nMME & 9.34 \\\\\n")
            out = root / "Example.docx"
            for join in (["--join-paragraphs"], []):
                run = subprocess.run([sys.executable, str(Path(md2docx.__file__)), str(page), "-o", str(out),
                                      "--paper-root", str(root), "--display-root", str(root / "units")] + join,
                                     capture_output=True, text=True)
                self.assertEqual(run.returncode, 0, run.stderr[-800:])
                xml = zipfile.ZipFile(out).read("word/document.xml").decode("utf-8")
                self.assertIn("<w:tbl>", xml, join)
                self.assertLess(xml.index("The second sentence reads them."), xml.index("<w:tbl>"), join)
                self.assertLess(xml.index("<w:tbl>"), xml.index("A later paragraph."), join)

    def test_a_ref_in_a_caption_never_places_or_numbers_a_table_early(self):
        """S-MISQ-Main-5-Results 260928: Table 1's caption named the pooled table, which
        Word then placed (and numbered 2) right after P1, and the pooled table's note pulled
        two more tables ahead of the prose that cites them. Only a sentence places a display;
        numbers follow the first citation in prose, as the LaTeX floats do."""
        import subprocess, sys, zipfile
        source = """# Example · §1 Results

## Content

### 1 · Results

#### P1. Sample

Table \\ref{tab:a} describes the sample. <!-- realizes: C1.P1.B1 -->

#### P2. Estimates

Table \\ref{tab:b} reports one model. <!-- realizes: C1.P2.B1 -->
Table \\ref{tab:c} pools them. <!-- realizes: C1.P2.B2 -->

## Aims
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "Example.md"
            page.write_text(source)
            captions = {"a": r"Sample, the pooled rows of Table~\ref{tab:c}",
                        "b": "One model", "c": r"Pooled, see also Table~\ref{tab:b}"}
            for key, caption in captions.items():
                unit = root / "units" / ("Display-" + key)
                (unit / "assets").mkdir(parents=True)
                (unit / "float.tex").write_text(r"\begin{table}[H]\caption{%s}\label{tab:%s}\end{table}" % (caption, key))
                (unit / "assets" / "table-body.tex").write_text("Row & %s \\\\\n" % key.upper())
            out = root / "Example.docx"
            run = subprocess.run([sys.executable, str(Path(md2docx.__file__)), str(page), "-o", str(out),
                                  "--paper-root", str(root), "--display-root", str(root / "units"),
                                  "--join-paragraphs"], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr[-800:])
            xml = zipfile.ZipFile(out).read("word/document.xml").decode("utf-8")
            at = {k: xml.index("Table %d. %s" % (n, captions[k].split(",")[0])) for k, n in (("a", 1), ("b", 2), ("c", 3))}
            self.assertLess(at["a"], xml.index("reports one model"))            # A after P1, before P2
            self.assertLess(xml.index("pools them"), at["b"])                    # B and C after all of P2
            self.assertLess(at["b"], at["c"])
            self.assertIn("pooled rows of Table 3", xml.replace("Table 3", "Table 3"))   # forward number
