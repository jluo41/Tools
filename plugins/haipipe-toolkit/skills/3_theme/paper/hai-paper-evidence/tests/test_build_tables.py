"""build_tables.py: raw rows arranged, never computed; the source file found in any Run of its Task. Placeholders only."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_tables.py"


class BuildTablesTest(unittest.TestCase):
    def build(self, config: str) -> dict:
        self.d = tempfile.TemporaryDirectory()
        self.addCleanup(self.d.cleanup)
        job = Path(self.d.name) / "j02_evidence_value"
        for run, value in (("r01_old", 9), ("r02_new", 1)):         # the newest Run holding the file wins
            src = job / "t01_v" / "runs" / run / "result" / "k" / "t.csv"
            src.parent.mkdir(parents=True)
            src.write_text(f"size,epochs,score\n1m,1,{value}\n1m,1,3\n10m,1,5\n")
        cfg = job / "t02_tables" / "scripts" / "tables.yaml"
        cfg.parent.mkdir(parents=True)
        cfg.write_text(config)
        self.res = job / "t02_tables" / "runs" / "r01" / "result"
        self.res.mkdir(parents=True)
        subprocess.run([sys.executable, str(SCRIPT), str(cfg)], check=True, capture_output=True, env={**os.environ, "RESULT_DIR": str(self.res)})
        return json.loads((self.res / "tables.json").read_text())

    def test_a_cell_shows_its_rows_never_their_mean(self):
        out = self.build("""
words: {size: Model size}
tabs:
- {slug: s, title: T, line: L, story: S, tables: [{from: t01_v/k/t.csv, pivot: {rows: size, cols: epochs, value: score}}]}
""")
        table = out["tabs"][0]["tables"][0]
        self.assertEqual(out["words"], {"size": "Model size"})
        self.assertEqual(table["rows"][0]["cells"][0]["v"], "1 / 3")      # both rows, not 2, and r02's value, not r01's
        self.assertEqual(table["rows"][0]["cells"][0]["n"], 2)
        self.assertEqual(table["rows"][1]["head"], "10m")                  # 1m before 10m
        self.assertEqual(out["tabs"][0]["method"], [])                     # no methods.yaml is fine
        self.assertTrue((self.res / "headline.txt").is_file())

    def test_a_list_table_keeps_each_number_as_written(self):
        # r02 (261106): a column holding 12480 and 2.3461 came back 12480.0 in the list table's .csv
        self.d = tempfile.TemporaryDirectory()
        self.addCleanup(self.d.cleanup)
        job = Path(self.d.name) / "j02_evidence_value"
        src = job / "t01_v" / "runs" / "r01" / "result" / "k" / "values.csv"
        src.parent.mkdir(parents=True)
        src.write_text("key,value,unit\nn,12480,units\nb,2.3461,points\n")
        cfg = job / "t02_tables" / "scripts" / "tables.yaml"
        cfg.parent.mkdir(parents=True)
        cfg.write_text("tabs:\n- {slug: s, title: T, line: L, story: S, tables: [{from: t01_v/k/values.csv, list: [key, value, unit]}]}\n")
        res = job / "t02_tables" / "runs" / "r01" / "result"
        res.mkdir(parents=True)
        subprocess.run([sys.executable, str(SCRIPT), str(cfg)], check=True, capture_output=True, env={**os.environ, "RESULT_DIR": str(res)})
        self.assertIn("n,12480,units", (res / "s.csv").read_text())
        cells = json.loads((res / "tables.json").read_text())["tabs"][0]["tables"][0]["rows"][0]["cells"]
        self.assertEqual(cells[1]["v"], "12480")

    def test_a_missing_source_stops_the_run(self):
        with self.assertRaises(subprocess.CalledProcessError):
            self.build("tabs:\n- {slug: s, title: T, line: L, story: S, tables: [{from: t01_v/k/none.csv, list: [a]}]}\n")


if __name__ == "__main__":
    unittest.main()
