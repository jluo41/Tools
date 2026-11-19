"""The Board's Data view shows a data version's shapes, counts and names, never a record value (workbench-insight T19).

A data version's folder holds a data file and a dictionary whose sample column carries a value. Neither the focus
page's Data view nor the version's fold may show that value, the sample column, a row of the data, or a link to the
raw dictionary; the columns table shows each column's name, type, null %, distinct and notes. Placeholders only.
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "_host"))
sys.path.insert(0, str(HERE))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import focus_page as FP  # noqa: E402
from live import insight_plan_c as P  # noqa: E402
from live import insight_views as V  # noqa: E402
from live.insight_theme import THEME  # noqa: E402
import plan_c_fixture as F  # noqa: E402

VALUE = "PLACEHOLDER-RECORD-VALUE-7"


class DataViewShapesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.board = F.make(self.root) / F.BOARD
        data = self.root / "_WorkSpace" / "store" / "demo_v1"
        data.mkdir(parents=True)
        (data / "demo_v1.parquet").write_bytes(b"PAR1 placeholder, never read for rows")
        (data / "data_dictionary.csv").write_text(
            "name,dtype,null_pct,n_unique,notes,sample_value\n"
            f"arm,str,0,2,the arm a row was given,{VALUE}\n", encoding="utf-8")
        (data / "manifest.json").write_text(json.dumps({"n_rows": 100, "n_cols": 1, "output_file": "demo_v1.parquet"}))
        md = self.board / "board.md"
        text = md.read_text(encoding="utf-8")
        md.write_text(re.sub(r'"extract": "\$EXTRACTS/demo-v1"', '"folder": "_WorkSpace/store/demo_v1/"', text, count=1)
                      .replace("extract: $EXTRACTS/demo-v1", "folder: _WorkSpace/store/demo_v1/", 1), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_the_dictionary_drops_its_sample_column_as_it_is_read(self):
        d = P.data_folder(self.root / "_WorkSpace" / "store" / "demo_v1")
        self.assertEqual(d["dictionary"], [{"name": "arm", "dtype": "str", "null_pct": "0", "n_unique": "2",
                                            "notes": "the arm a row was given"}])
        self.assertFalse(hasattr(P, "sample_rows"))                              # nothing left to draw rows with

    def test_the_data_view_shows_columns_and_no_record_value(self):
        b = P.board(self.board)
        v = next(x for x in b["versions"] if str(x.get("folder", "")).startswith("_WorkSpace/store/demo_v1"))
        pages = {"focus Data view": FP.render(THEME, self.root, self.board, "report", "data"),
                 "the version's fold": V._version(v, self.root)}
        for where, html in pages.items():
            with self.subTest(where=where):
                self.assertNotIn(VALUE, html)
                self.assertNotIn("sample_value", html)
                self.assertNotIn("A few rows", html)
                self.assertNotRegex(html, r'href="[^"]*data_dictionary\.csv"')    # the raw file is not one click away
        self.assertIn("<code>arm</code>", pages["the version's fold"])
