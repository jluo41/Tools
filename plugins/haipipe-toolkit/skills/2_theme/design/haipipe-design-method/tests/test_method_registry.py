"""The method registry (methods/), pin_method.py (run-setup-method) and score_exp.py (run-score): the registry matches
what the design workbench's reader names, a pin copies the version word for word and records its sha, and an Exp's
arms are scored against the frozen predictions."""
from __future__ import annotations

import csv
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
DESIGN = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / "scripts"))
sys.path.insert(0, str(DESIGN / "haipipe-design" / "scripts"))
import design_ladder as D  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "haipipe-design" / "tests"))
from ladder_kit import ready  # noqa: E402
import pin_method as P  # noqa: E402
import score_exp as S  # noqa: E402

READER = DESIGN.parents[2] / "servers" / "workbench-design" / "design_reader.py"
STEPS = ("① See input", "② Reason ideas", "③ Conduct process", "④ Review item", "⑤ Review whole")


def reader():
    spec = importlib.util.spec_from_file_location("design_reader_method_test", READER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class RegistryTest(unittest.TestCase):
    def test_the_registry_names_what_the_workbench_reads(self):
        reg = P.registered()
        self.assertEqual({k: (v["name"], v["type"]) for k, v in reg.items()}, reader().METHODS)

    def test_every_version_has_the_five_steps_and_what_it_sees(self):
        toolkit = DESIGN.parents[2]
        for mid, m in P.registered().items():
            card = P.front((m["path"] / "method.md").read_text())
            self.assertTrue((toolkit / card["card"]).is_file(), card["card"])        # one of the Guide's 13
            self.assertTrue(m["versions"], mid)
            for v, path in m["versions"].items():
                f = P.front(path.read_text())
                self.assertEqual((f["method"], f["version"]), (mid, v))
                self.assertEqual(tuple(f["steps"]), STEPS)
                self.assertIn("Goal · how much is set", f["sees"])


class PinAndScoreTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.block = Path(self.tmp.name) / "Project" / "designs" / "b01_demo_app"
        ready(self.block, n=2)
        self.job = self.block / "j03_g01_m04"
        D.main(["job", str(self.job), "--goal", "G01", "--method", "M04 m2", "--inputs", "i2", "--n", "2"])

    def tearDown(self):
        self.tmp.cleanup()

    def test_pin_copies_the_version_and_records_its_sha(self):
        made = P.main([str(self.job)])
        dest = self.job / "inputs" / "method.md"
        self.assertIn(dest, made)
        self.assertEqual(dest.read_text(), P.version_file("M04 m2").read_text())
        face = P.front((self.job / "j03_g01_m04.md").read_text())
        self.assertRegex(str(face["method-sha"]), r"^[0-9a-f]{12}$")
        self.assertEqual(reader().job(self.job)["method_card"]["version"], "m2")
        self.assertEqual(P.main([str(self.job)]), [])                    # pinned already: nothing made

    def test_an_unknown_method_or_version_is_refused(self):
        for pin in ("M09 m1", "M04 m9", "by insight"):
            with self.assertRaises(SystemExit):
                P.version_file(pin)

    def test_a_different_method_text_is_refused(self):
        P.main([str(self.job)])
        (self.job / "inputs" / "method.md").write_text("---\nmethod: M04\nversion: m1\n---\n")
        with self.assertRaises(SystemExit):
            P.main([str(self.job)])

    def test_each_arm_is_scored_against_its_frozen_prediction(self):
        for k, (pred, slug) in enumerate((("+0.8 [0.2; 1.4]", "reason-first"), ("+x [lo; hi]", "ask-only")), 1):
            t = D.task(self.job, f"d0{k}", slug, [])
            (t / "prediction.yaml").write_text(yaml.safe_dump({"predicted": pred, "against": "the control",
                                                               "frozen": "261007"}))
        e = self.block / "observed" / "e01_demo-exp"
        e.mkdir(parents=True)
        (e / "arms.csv").write_text("arm,job,design,n,observed\nA,control,,<n>,<rate>\nB,j03,d01,<n>,+0.5\n"
                                    "C,j03,d02,<n>,-0.3\n")
        rows = S.main([str(self.block), "e01"])
        out = self.block / "runs" / "run-score-e01" / "scores.csv"
        with out.open() as f:
            got = list(csv.DictReader(f))
        self.assertEqual(list(got[0]), list(S.COLS))
        self.assertEqual([(r["design"], r["direction"], r["in_range"], r["error"]) for r in got],
                         [("d01", "✓", "✓", "-0.30"), ("d02", "✗", "?", "?")])
        self.assertEqual(S.scorecard(rows), [("M04 m2", 2, 1, 1)])
        self.assertIn("score", {r["type"] for r in reader().runs(self.block)})
        with self.assertRaises(SystemExit):                              # never overwrites
            S.main([str(self.block), "e01"])


if __name__ == "__main__":
    unittest.main()
