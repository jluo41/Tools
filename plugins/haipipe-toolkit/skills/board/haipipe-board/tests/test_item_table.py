#!/usr/bin/env python3
"""The item table · one row per mark, a derived ladder word per row.

`haipipe-plugin-outline/ref/item-table.md` (JL 260901): SURVEY writes Need ·
Route · Run · Decide, LAND appends ` → <result file>`, and the Status is never
typed: it is derived from the row, the result file and the plan's Answered:
line. These tests pin the derivation so the strip and the evidence file cannot
disagree with the law.
"""
import os
import tempfile
import time
import unittest
from pathlib import Path

from src import item_table as it

PLAN = """# QT2 · outline v1
approved: {tick}

## C1 · One
### C1.P1 · move
- B1 · the count of physicians
  Note: a number 📮
- B2 · the guideline anchor
  Note: a citation 📚
- B3 · the funnel figure
  Note: a picture 🖼 owed · figure
- B4 · no mark here
  Note: nothing owed
"""

ITEMS = """# QT2 · items
page: QT2
kind: items · authored
plan: v1

### C1.P1.B1 · 📮 the count of physicians
- **Need**: the count
- **Route**: task
- **Run**: found · tasks/b01/j01/t01 · the build run{arrow}
- **Decide**: {decide}

### C1.P1.B2 · 📚 the guideline anchor
- **Need**: the CDC guideline
- **Route**: bibex
- **Run**: person · you supply the entry
- **Decide**: ☑ make · JL 260901

### C1.P1.B3 · 🖼 the funnel figure
- **Need**: the funnel
- **Route**: display
- **Run**: none · a judgment, no run can draw it
- **Decide**: ☐ make
"""


def _page(root, *, tick="⬜", decide="☐ make", arrow="", result=True, answered=False):
    pd = Path(root) / "QT2"
    (pd / "outline").mkdir(parents=True)
    (pd / "QT2.md").write_text("# QT2\n\nstate: 🟡\n")
    plan = PLAN.format(tick=tick)
    if answered:
        plan = plan.replace("  Note: a number 📮\n", "  Note: a number 📮\n  Answered: 226,149 · tasks/b01/j01/t01/results/n.txt\n")
    (pd / "outline" / "QT2-outline-v1.md").write_text(plan)
    if result:
        (pd / "tasks" / "b01" / "j01" / "t01" / "results").mkdir(parents=True)
        (pd / "tasks" / "b01" / "j01" / "t01" / "results" / "n.txt").write_text("226149\n")
    (pd / "outline" / "QT2-items.md").write_text(ITEMS.format(decide=decide, arrow=arrow))
    return pd / "QT2.md"


class ItemTableTest(unittest.TestCase):
    def test_read_items_parses_outcome_address_result_and_decision(self):
        with tempfile.TemporaryDirectory() as d:
            md = _page(d, decide="☑ make · JL 260901", arrow=" → tasks/b01/j01/t01/results/n.txt")
            rows = it.read_items(md)
            r = rows["C1.P1.B1"]
            self.assertEqual(("found", "tasks/b01/j01/t01", "tasks/b01/j01/t01/results/n.txt", "make"),
                             (r["outcome"], r["address"], r["result"], r["decision"]))
            self.assertEqual("none", rows["C1.P1.B3"]["outcome"])
            self.assertEqual("", rows["C1.P1.B3"]["decision"])

    def test_bullets_yield_every_mark_and_the_folded_flag(self):
        got = [(a, k, f) for a, _h, k, _r, f in it.bullets(PLAN.format(tick="⬜"))]
        self.assertEqual([("C1.P1.B1", "probe", False), ("C1.P1.B2", "cite", False),
                          ("C1.P1.B3", "display", False), ("C1.P1.B4", None, False)], got)
        folded = [f for a, _h, k, _r, f in it.bullets(PLAN.format(tick="⬜").replace(
            "  Note: a number 📮\n", "  Note: a number 📮\n  Answered: 1\n")) if a == "C1.P1.B1"]
        self.assertEqual([True], folded)

    def test_ladder_owed_bound_landed_folded(self):
        with tempfile.TemporaryDirectory() as d:
            # ☐ + no arrow → owed; a ☑ make person row waiting on the person → bound
            md = _page(d)
            s = it.summarize(md, md.parent / "outline" / "QT2-outline-v1.md")
            self.assertEqual(1, s["counts"]["owed"])        # B1: undecided, no pointer
            self.assertEqual(1, s["counts"]["bound"])       # B2: person, ☑ make, nothing supplied yet
            self.assertEqual(1, s["counts"]["blocked"])     # B3: outcome none
            self.assertEqual("SURVEY", s["cycle"])          # a ☐ row keeps the cycle at SURVEY
        with tempfile.TemporaryDirectory() as d:
            md = _page(d, decide="☑ make · JL 260901")
            s = it.summarize(md, md.parent / "outline" / "QT2-outline-v1.md")
            self.assertEqual(2, s["counts"]["bound"])       # B1 decided with an address, no result yet; B2 as above
            self.assertEqual("SURVEY", s["cycle"])          # B3 is still ☐, so the table is not survey-complete
            f = it.items_path(md)
            f.write_text(f.read_text().replace("- **Run**: none · a judgment, no run can draw it\n- **Decide**: ☐ make",
                                               "- **Run**: none · a judgment, no run can draw it\n- **Decide**: ☑ drop · SHAPE rewrites the bullet"))
            s = it.summarize(md, md.parent / "outline" / "QT2-outline-v1.md")
            self.assertEqual("LAND", s["cycle"])            # every row decided, two bound → LAND
        with tempfile.TemporaryDirectory() as d:
            md = _page(d, decide="☑ make · JL 260901", arrow=" → tasks/b01/j01/t01/results/n.txt")
            s = it.summarize(md, md.parent / "outline" / "QT2-outline-v1.md")
            self.assertEqual(1, s["counts"]["landed"])      # the pointer resolves (page-relative)
        with tempfile.TemporaryDirectory() as d:
            md = _page(d, tick="✅ JL", decide="☑ make · JL 260901",
                       arrow=" → tasks/b01/j01/t01/results/n.txt", answered=True)
            s = it.summarize(md, md.parent / "outline" / "QT2-outline-v1.md")
            self.assertEqual(1, s["counts"]["folded"])      # landed + Answered: line

    def test_stale_when_the_result_is_newer_than_the_plan(self):
        with tempfile.TemporaryDirectory() as d:
            md = _page(d, tick="✅ JL", decide="☑ make · JL 260901",
                       arrow=" → tasks/b01/j01/t01/results/n.txt", answered=True)
            plan = md.parent / "outline" / "QT2-outline-v1.md"
            old = time.time() - 600
            os.utime(plan, (old, old))
            s = it.summarize(md, plan)
            self.assertEqual(1, s["counts"]["stale"])

    def test_defer_drop_and_the_status_is_never_typed(self):
        with tempfile.TemporaryDirectory() as d:
            md = _page(d, decide="☑ defer · after the server run")
            s = it.summarize(md, md.parent / "outline" / "QT2-outline-v1.md")
            self.assertEqual(1, s["counts"]["deferred"])
            # a typed Status row in the table is ignored: the derivation wins
            f = it.items_path(md)
            f.write_text(f.read_text().replace("- **Decide**: ☑ defer · after the server run",
                                               "- **Status**: 📌 folded\n- **Decide**: ☑ drop · out of scope"))
            s = it.summarize(md, md.parent / "outline" / "QT2-outline-v1.md")
            self.assertEqual(1, s["counts"]["dropped"])
            self.assertEqual(0, s["counts"]["folded"])

    def test_no_table_reads_from_the_lane(self):
        with tempfile.TemporaryDirectory() as d:
            md = _page(d)
            it.items_path(md).unlink()
            plan = md.parent / "outline" / "QT2-outline-v1.md"
            s = it.summarize(md, plan, lane=lambda kind, ref: (kind == "cite", False))
            self.assertEqual({"owed": 2, "landed": 1}, {k: v for k, v in s["counts"].items() if v})
            self.assertEqual("SHAPE", s["cycle"])


if __name__ == "__main__":
    unittest.main()
