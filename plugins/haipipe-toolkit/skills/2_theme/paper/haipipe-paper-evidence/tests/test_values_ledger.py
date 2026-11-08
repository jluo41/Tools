"""values_ledger.py on Tools' Paper-Example (copied into a temp folder with its placeholder work Block b90; the copy is
reset to no bindings first): the search proposes bindings, a person ticks them, and the ledger then says match,
differs, owed, found (a display hit not bound yet), never printed and printed-but-unbound. A typed stand-in in a value's
chain blocks it in evidence_ledger.py, and an older Section shape (draft S ids, a `key:` binding) still checks.
Placeholders only, no real paper."""
from __future__ import annotations

import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
import evidence_ledger as led  # noqa: E402
import values_ledger as vl  # noqa: E402

LADDER = next(p for p in HERE.parents if (p / "blueprints").is_dir()) / "blueprints" / "Project-Ladder"
DIFFERS = """evidence:
- kind: value
  source: j02.t01
  items:
  - {run: r01, for: [C2.P1.B2], value: RQ1-t01-006, anchor: ['4.10']}
"""


class ValuesLedgerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.proj = self.tmp / "Project-Ladder"
        (self.proj / "work").mkdir(parents=True)
        shutil.copy(LADDER / "project.yaml", self.proj / "project.yaml")
        shutil.copytree(LADDER / "paper" / "Paper-Example", self.proj / "paper" / "Paper-Example")
        shutil.copytree(LADDER / "work" / "b90_example_paper_results", self.proj / "work" / "b90_example_paper_results")
        self.board = self.proj / "paper" / "Paper-Example"
        self.j02 = self.board / "j02_evidence_value"
        self.task = self.j02 / "t01_values-sample"
        self.v = self.board / "j11_writing_v1130_desk"
        for f in list(self.board.rglob("evidence/cards.yaml")) + list(self.board.rglob("evidence/proposals.md")):
            f.unlink()
        (self.v / "t03_results/evidence").mkdir(parents=True, exist_ok=True)
        (self.v / "t03_results/evidence/cards.yaml").write_text(DIFFERS, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_task(self):
        out = self.tmp / "out"
        doc = vl.run(self.task, out)
        rows = list(__import__("csv").DictReader((out / "ledger.csv").open(encoding="utf-8")))
        return doc, rows, (out / "values.html").read_text(encoding="utf-8")

    def status(self, rows, key, where_part=""):
        return {r["status"] for r in rows if r["key"] == key and where_part in r["where"]}

    def test_catalog_ids_and_lineage(self):
        _, values = vl.catalog(self.task)
        self.assertEqual(values["main.b"]["id"], "RQ1-t01-002")
        self.assertEqual([c["address"] for c in values["main.b"]["checks"]], ["b90.j02.t01.r01", "b90.j01.t01.r01"])
        self.assertTrue(values["main.b"]["linked"])
        self.assertFalse(values["main.b"]["screen_read"])

    def test_search_then_tick_then_every_status(self):
        doc, rows, _ = self.run_task()
        self.assertEqual(self.status(rows, "main.b"), {"found"})              # found by the search, not bound
        self.assertEqual(self.status(rows, "sub.b"), {"differs"})             # bound when 4.10, the Run now says 4.12
        vl.bind(self.j02, propose=True)
        props = (self.v / "t03_results/evidence/proposals.md").read_text(encoding="utf-8")
        self.assertIn("bind VALUE RQ1-t01-002 (2.35) to t03_results C2.P1.B1", props)
        self.assertFalse((self.v / "t02_methods/evidence/cards.yaml").exists())     # nothing written before a tick
        for sec in ("t02_methods", "t03_results"):
            f = self.v / sec / "evidence/proposals.md"
            f.write_text(f.read_text(encoding="utf-8").replace("- [ ] bind VALUE", "- [x] bind VALUE"), encoding="utf-8")
        vl.bind(self.j02, adopt=True)
        items = yaml.safe_load((self.v / "t03_results/evidence/cards.yaml").read_text(encoding="utf-8"))["evidence"][0]["items"]
        self.assertIn({"run": "r01", "for": ["C2.P1.B1"], "value": "RQ1-t01-002", "anchor": ["2.35"]}, items)
        doc, rows, page = self.run_task()
        self.assertEqual(self.status(rows, "main.b"), {"match"})
        self.assertEqual(self.status(rows, "sample.n_units"), {"match"})      # in two Sections
        self.assertEqual(len([r for r in rows if r["key"] == "sample.n_units"]), 2)
        self.assertEqual(self.status(rows, "sub.b"), {"differs"})
        self.assertEqual(self.status(rows, "late.b"), {"owed"})
        self.assertEqual(self.status(rows, "mean.before", "Display B"), {"found"})   # a display hit, still proposed
        self.assertEqual(doc["never_printed"], ["extra.sd"])
        self.assertIn("2.35 (0.84 to 3.85)", page)                            # the estimate row prints its CI
        self.assertIn("1 never printed", doc["headline"])
        vl.bind(self.j02, confirm=[])                                          # an agent confirms the rest
        _, rows, _ = self.run_task()
        self.assertEqual(self.status(rows, "mean.before", "Display B"), {"match"})
        chk = vl.check(self.j02, self.tmp / "check")
        self.assertEqual([x["printed"] for x in chk["printed_unbound"]], ["37.5"])

    def test_a_display_not_drawn_from_the_values_run_is_no_hit(self):
        card = self.board / "j01_evidence_display/t02_table1-example/runs/r01_draw_table1/run.yaml"
        card.write_text(card.read_text(encoding="utf-8").replace("t01_example_main/runs/r01_example_main",
                                                                 "t09_other/runs/r01_other"), encoding="utf-8")
        _, rows, _ = self.run_task()
        self.assertFalse([r for r in rows if r["where"] == "Display B"])

    def test_a_pending_value_may_wait_for_a_run_with_no_result_yet(self):
        vmap = self.task / "scripts/value_map.yaml"
        m = yaml.safe_load(vmap.read_text(encoding="utf-8"))
        run = next(iter(m["runs"]))
        m["values"]["later.b"] = {"what": "from a server Run", "run": run, "file": "not_back_yet.csv", "column": "value",
                                  "pending": "the server Run has not returned"}
        vmap.write_text(yaml.safe_dump(m, sort_keys=False), encoding="utf-8")
        row = vl.catalog(self.task)[1]["later.b"]
        self.assertEqual((row["value"], row["shown"], row["linked"]), (None, "", False))
        self.assertEqual(row["pending"], "the server Run has not returned")
        self.run_task()                                               # the whole ledger still builds
        values = vl.catalog(self.task)[1]
        bind = {"item": {"key": "later.b", "anchor": ["2.5 points"], "for": ["S1"]}, "holder": self.v / "t03_results", "task": "t01"}
        rows = vl.check_binding(bind, values, lambda h: {"S1": "It rose 2.5 points."}, {})
        self.assertEqual([(r["status"], r["note"]) for r in rows], [("pending", "the server Run has not returned")])
        m["values"]["later.b"].pop("pending")                         # no `pending`: a missing file stays an error
        vmap.write_text(yaml.safe_dump(m, sort_keys=False), encoding="utf-8")
        with self.assertRaises(FileNotFoundError):
            vl.catalog(self.task)

    def test_a_screen_read_and_an_unlinked_value_block_the_ledger(self):
        b90 = self.proj / "work/b90_example_paper_results"
        csvf = b90 / "j02_example_estimates/t01_example_main/runs/r01_example_main/result/values.csv"
        csvf.write_text(csvf.read_text(encoding="utf-8").replace("main.b,2.3461,points,\"2.35 (95% CI, 0.84 to 3.85)\",r01_source:tables.csv",
                                                                 "main.b,2.3461,points,,typed:\"src/typed/main.csv\""), encoding="utf-8")
        vmap = self.task / "scripts/value_map.yaml"
        m = yaml.safe_load(vmap.read_text(encoding="utf-8"))
        m["values"]["sub.b"] = {"what": "typed into the map", "value": 4.10, "digits": 2}
        vmap.write_text(yaml.safe_dump(m, sort_keys=False), encoding="utf-8")
        vl.run(self.task, self.task / "runs" / vl.RUN / "result")
        bad = led.value_ledger(self.board)["bad"]
        self.assertTrue(any(b.startswith("value rests on a screen read: t01_values-sample RQ1-t01-002 main.b") for b in bad), bad)
        self.assertTrue(any(b.startswith("value not linked to a Run: t01_values-sample RQ1-t01-006 sub.b") for b in bad), bad)

    def test_an_older_section_draft_s_ids_and_a_key_binding(self):
        sec = self.v / "t03_results"
        (sec / "draft").mkdir(exist_ok=True)
        (sec / "draft/t03_results-draft-v0.2.md").write_text(
            "# draft\n\n## 3 · Draft\n\n- B1 · S5 · The subgroup difference was 4.12 points.\n", encoding="utf-8")
        (sec / "evidence/cards.yaml").write_text(
            "evidence:\n- kind: value\n  source: j02.t01\n  items:\n"
            "  - {run: r01, for: ['5'], file: values.yaml, key: values.sub.b.value, anchor: ['4.12']}\n", encoding="utf-8")
        _, rows, _ = self.run_task()
        self.assertEqual({r["status"] for r in rows if r["key"] == "sub.b" and r["where"] == "t03_results S5"}, {"match"})


if __name__ == "__main__":
    unittest.main()
