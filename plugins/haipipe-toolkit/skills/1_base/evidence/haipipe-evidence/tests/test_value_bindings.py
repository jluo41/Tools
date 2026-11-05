"""cards.py's VALUE bindings (0.9.0) on a made-up Project: an item bound by its value id, each status at the printed
precision, the lineage of a work Run's values.csv `source`, and a binding proposed, ticked once, then adopted.
Placeholders only."""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import cards  # noqa: E402

ROW = {"id": "RQ1-t01-002", "value": 2.3461, "shown": "2.35", "what": "<outcome>: difference"}


def write(p: Path, text: str) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


class BindingTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        write(self.tmp / "project.yaml", "id: demo\n")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_status_at_the_printed_precision(self):
        st = lambda it, text, row=ROW: [s for _, s, _ in cards.item_status(it, row, text)]  # noqa: E731
        self.assertEqual(st({"anchor": ["2.35"]}, "a 2.35 point gain"), ["match"])
        self.assertEqual(st({"anchor": ["2.3"]}, "a 2.3 point gain"), ["match"])
        self.assertEqual(st({"anchor": ["2.34"]}, "a 2.34 point gain"), ["differs"])
        self.assertEqual(st({"anchor": ["2.35"]}, "a gain"), ["missing"])
        self.assertEqual(st({}, "a gain"), ["no anchor"])
        self.assertEqual(st({"need": "a Run", "anchor": ["1.9"]}, "1.9"), ["owed"])
        self.assertEqual(st({"anchor": ["2.35"]}, "2.35", dict(ROW, pending="waits for b11.j21.t01.r04")), ["pending"])
        self.assertTrue(cards.agrees("P < .001", 0.0004))
        self.assertTrue(cards.agrees("0.125", 0.1245))            # half up, not banker's rounding
        self.assertTrue(cards.is_value_id("RQ1-t01-002"))
        self.assertFalse(cards.is_value_id("773,566 first visits"))   # a value stated in words stays one

    def test_lineage_from_the_source_column(self):
        block = self.tmp / "work/b90_demo"
        write(block / "src/inputs.yaml", "runs:\n  up:\n    label: the upstream tables\n    path: b90_demo/j01_a/t01_a/runs/r01_a\n"
                                          "    address: b90.j01.t01.r01\ntyped:\n  t1: {path: src/typed/x.csv, label: a screen read}\n")
        run = block / "j02_b/t01_b/runs/r01_b"
        write(run / "result/values.csv", "key,value,source\nmain.b,2.3461,up:tables.csv\nmain.p,0.01,typed:\"src/typed/x.csv\"\n")
        chain, has = cards.lineage(run, "values.csv", {"key": "main.b"})
        self.assertEqual([c["address"] for c in chain], ["b90.j01.t01.r01"])
        self.assertTrue(has)
        chain, _ = cards.lineage(run, "values.csv", {"key": "main.p"})
        self.assertEqual(chain[0]["name"], "a screen read")
        self.assertTrue(chain[0]["typed"])

    def test_propose_tick_adopt_and_check(self):
        res = self.tmp / "work/b51_x/j02_y/t01_z/runs/r01_v/result"
        write(res / "values.yaml", yaml.safe_dump({"values": {"main.b": ROW}}))
        sents = {"5": "The gain was 2.35 points (95% CI, 0.84 to 3.85).", "6": "Nothing here."}
        f = write(self.tmp / "task/evidence/cards.yaml", "evidence: []\n")
        props = cards.bind_proposals(cards.catalog(res / "values.yaml"), sents, "task", "b51.j02.t01", "r01", [])
        self.assertEqual([p[0] for p in props], ["bind-RQ1-t01-002-S5"])
        cards.write_proposals(f.parent / "proposals.md", [(p, line) for p, line, _ in props])
        self.assertEqual(cards.adopt_bindings(f, props), 0)       # nothing before the tick
        pm = f.parent / "proposals.md"
        pm.write_text(pm.read_text(encoding="utf-8").replace("- [ ]", "- [x]"), encoding="utf-8")
        self.assertEqual(cards.adopt_bindings(f, props), 1)
        loaded = cards.load(f)
        self.assertEqual(loaded[0]["items"][0], {"run": "r01", "for": ["5"], "value": "RQ1-t01-002", "anchor": ["2.35"]})
        self.assertEqual(cards.check(loaded, self.tmp, sents, near=f), [])
        self.assertEqual(cards.bind_proposals(cards.catalog(res / "values.yaml"), sents, "task", "b51.j02.t01", "r01", loaded), [])
        loaded[0]["items"][0]["anchor"] = ["2.53"]          # the text was changed to a wrong number
        probs = cards.check(loaded, self.tmp, {"5": "The gain was 2.53"}, near=f)
        self.assertTrue(any("differs from its value 2.35" in p for p in probs), probs)


if __name__ == "__main__":
    unittest.main()
