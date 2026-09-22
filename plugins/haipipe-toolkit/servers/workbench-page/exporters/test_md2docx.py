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

    def test_table_alignment_ignores_tex_modifier_commands(self):
        spec = (r"@{}>{\raggedright\arraybackslash}p{3.45cm}"
                r"*{6}{>{\centering\arraybackslash}X}@{}")
        self.assertEqual(md2docx._alignment_columns(spec), list("lcccccc"))


if __name__ == "__main__":
    unittest.main()
