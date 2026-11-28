"""aggregate_query.py, M05 m3's one door to a raw extract: the dictionary decides what may be asked, a group under 11
is hidden, the budget holds, and no answer or error carries a row. Synthetic data only."""
from __future__ import annotations

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import pandas as pd
import yaml

TOOL = Path(__file__).resolve().parents[1] / "methods" / "M05-raw-data-agent"
sys.path.insert(0, str(TOOL))
import aggregate_query as A  # noqa: E402

DICTIONARY = """# Synthetic extract

The extract: `data/extract.parquet`.

| name | group | dtype | null_pct | n_unique | notes |
|---|---|---|---|---|---|
| person_id | identity | object | 0.0 | 120 | |
| sent_at | derived | datetime64[ns] | 0.0 | 120 | |
| note | message | object | 0.0 | 5000 | |
| arm | experiment | object | 0.0 | 3 | |
| clicked | engagement | int32 | 0.0 | 2 | |
| visits | pre_period | int64 | 0.0 | 120 | |
| empty | message | object | 100.0 | 0 | |
| kind:joined | rx | object | 0.0 | 2 | |
"""


def space(tmp: Path) -> Path:
    (tmp / "env.sh").write_text("", encoding="utf-8")
    (tmp / "data").mkdir()
    n = 120
    pd.DataFrame({
        "person_id": [f"P{i:03d}" for i in range(n)],
        "sent_at": pd.date_range("2025-01-06 08:00", periods=n, freq="h"),
        "note": [f"secret-note-{i}" for i in range(n)],
        "arm": ["A"] * 60 + ["B"] * 55 + ["C"] * 5,          # C is under 11
        "clicked": [i % 2 for i in range(n)],
        "visits": list(range(n)),
        "empty": [None] * n,
        "kind:joined": ["x", "y"] * (n // 2),
    }).to_parquet(tmp / "data" / "extract.parquet")
    md = tmp / "dictionary.md"
    md.write_text(DICTIONARY, encoding="utf-8")
    return md


def run(argv) -> tuple[int, str]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = A.main(argv)
    return code, out.getvalue() + err.getvalue()


class AggregateQueryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.md = space(self.tmp)
        self.out = self.tmp / "result" / "queries"

    def ask(self, *extra):
        return run([str(self.md), "--out", str(self.out), "--why", "test", *extra])

    def test_a_small_group_is_hidden_and_only_counted(self):
        code, text = self.ask("--by", "arm", "--metrics", "clicked")
        self.assertEqual(code, 0, text)
        d = yaml.safe_load((self.out / "q01.yaml").read_text(encoding="utf-8"))
        self.assertEqual([r["arm"] for r in d["rows"]], ["A", "B"])
        self.assertEqual(d["hidden"], 1)
        self.assertEqual(d["receipt"]["extract"], "data/extract.parquet")
        self.assertIn("q01", (self.out / "queries.md").read_text(encoding="utf-8"))

    def test_identity_free_text_and_raw_times_are_refused(self):
        for key in ("person_id", "note", "sent_at", "visits", "empty"):
            code, text = self.ask("--by", key)
            self.assertEqual(code, 2, key)
            self.assertNotIn("P00", text)
            self.assertNotIn("secret-note", text)
        self.assertEqual(run([str(self.md), "--out", str(self.out), "--why", "x", "--where", "person_id=P001"])[0], 2)
        self.assertFalse(list(self.out.glob("q*.yaml")))

    def test_derived_keys_answer(self):
        for key in ("sent_at:weekday", "note:length", "visits:q5", "kind:joined"):
            code, text = self.ask("--by", key, "--metrics", "clicked")
            self.assertEqual(code, 0, f"{key}: {text}")
        self.assertEqual(len(list(self.out.glob("q*.yaml"))), 4)

    def test_no_row_values_reach_the_answer(self):
        self.ask("--by", "arm", "--metrics", "clicked,visits", "--where", "clicked=1")
        text = (self.out / "q01.yaml").read_text(encoding="utf-8")
        for value in ("P001", "secret-note", "2025-01-06 08:00"):
            self.assertNotIn(value, text)

    def test_the_budget_holds(self):
        for _ in range(2):
            self.assertEqual(self.ask("--by", "arm", "--budget", "2")[0], 0)
        code, text = self.ask("--by", "arm", "--budget", "2")
        self.assertEqual(code, 2)
        self.assertIn("budget", text)

    def test_columns_lists_uses_without_values(self):
        code, text = run([str(self.md), "--columns"])
        self.assertEqual(code, 0)
        self.assertIn("refused", text)
        self.assertIn(":q5", text)
        self.assertNotIn("P00", text)


if __name__ == "__main__":
    unittest.main()
