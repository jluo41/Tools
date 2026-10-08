"""make_inputs.py freezes a Block's inputs version and builds a Job's inputs/ fence (ref/inputs.md): only what the
method's step ① sees, relative links, a manifest with sha256, never an overwrite; and the design workbench's reader
(servers/workbench-design/design_reader.py) reads the fence."""
from __future__ import annotations

import importlib.util
import os
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
import make_inputs as M  # noqa: E402

READER = DESIGN.parents[2] / "servers" / "workbench-design" / "design_reader.py"
GOALS = {"goals": [{"id": "G01", "aim": "<the behaviour to change>", "who": "<audience>", "venue": "sms", "n": 3,
                    "rules": ["<a rule for this goal only>"], "leave-out": "<what>", "signed": "✅ 261007"},
                   {"id": "G02", "aim": "<another>", "who": "<audience>", "venue": "sms", "n": 3, "rules": [],
                    "leave-out": "", "signed": ""}]}


def reader():
    spec = importlib.util.spec_from_file_location("design_reader_goal_test", READER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class MakeInputsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.block = Path(self.tmp.name) / "Project" / "designs" / "b01_demo_app"
        D.main(["block", str(self.block), "--channel", "sms"])
        rules = self.block / "design-goal.md"
        rules.write_text(rules.read_text().replace("signed: ''", "signed: ✅ 261007"))
        board = self.block / "board.md"
        board.write_text(board.read_text().replace("```yaml\ngoals: []\n```",
                                                   "```yaml\n" + yaml.safe_dump(GOALS, allow_unicode=True) + "```"))
        v = self.block / "inputs" / "i2"
        (v / "theory").mkdir(parents=True)
        (v / "rules.md").write_text("# Shared rules\n\n- r2.1 <a rule>\n")
        (v / "handoff-W-03.md").write_text("# W-03 · the insight handoff (placeholder)\n")
        (v / "theory" / "papers.md").write_text("# Theory\n\n- <a paper>\n")
        (v / "manifest.yaml").write_text(yaml.safe_dump({"parts": [
            {"part": "Goal · how much is set", "file": "rules.md", "says": "the shared rules"},
            {"part": "Information · whose", "file": "handoff-W-03.md", "says": "ours: the insight handoff"},
            {"part": "Information · form", "file": "theory/papers.md", "says": "a theory"}]}, allow_unicode=True))
        self.job = self.block / "j01_g01_m04"
        D.main(["job", str(self.job), "--goal", "G01", "--method", "M04 m2", "--inputs", "i2", "--n", "3"])

    def tearDown(self):
        self.tmp.cleanup()

    def method(self, sees):
        (self.job / "inputs" / "method.md").write_text(
            "---\n" + yaml.safe_dump({"method": "M04", "version": "m2", "sees": sees}, allow_unicode=True) + "---\n")

    def test_freeze_lists_every_file_keeps_parts_and_never_edits(self):
        v = self.block / "inputs" / "i2"
        self.assertEqual(M.main(["freeze", str(v), "--new", "a new handoff", "--rules", "r2"]), [v / "manifest.yaml"])
        man = yaml.safe_load((v / "manifest.yaml").read_text())
        self.assertEqual({f["path"] for f in man["files"]}, {"rules.md", "handoff-W-03.md", "theory/papers.md"})
        self.assertEqual(len(man["parts"]), 3)
        self.assertTrue(man["frozen"])
        self.assertEqual(M.main(["freeze", str(v)]), [])                 # frozen: nothing made

    def test_the_fence_holds_only_what_step_one_sees(self):
        M.main(["freeze", str(self.block / "inputs" / "i2")])
        self.method(["Goal · how much is set", "Information · whose"])
        M.main(["job", str(self.job)])
        fence = self.job / "inputs"
        self.assertEqual(sorted(p.name for p in fence.iterdir()),
                         ["goal.md", "handoff-W-03.md", "manifest.yaml", "method.md", "rules.md"])
        self.assertEqual(os.readlink(fence / "rules.md"), "../../inputs/i2/rules.md")
        self.assertIn("<the behaviour to change>", (fence / "goal.md").read_text())
        man = yaml.safe_load((fence / "manifest.yaml").read_text())
        self.assertEqual(man["inputs"], "i2")
        self.assertEqual({f["path"] for f in man["files"]}, {"goal.md", "handoff-W-03.md", "method.md", "rules.md"})
        self.assertIn({"part": "Examples", "choice": "nothing", "file": ""}, man["parts"])
        self.assertEqual(M.main(["job", str(self.job)]), [])             # built once

    def test_a_kind_narrows_a_part(self):
        """sees: `<part> [<kind>]` links only that kind's files; a plain part links all its kinds (JL 261008)."""
        v = self.block / "inputs" / "i2"
        (v / "evidence.md").write_text("# evidence (placeholder)\n")
        (v / "advice.md").write_text("# advice (placeholder)\n")
        man = yaml.safe_load((v / "manifest.yaml").read_text())
        man["parts"] += [{"part": "Information · whose", "kind": "information", "file": "evidence.md", "says": "evidence"},
                         {"part": "Information · whose", "kind": "knowledge-wisdom", "file": "advice.md", "says": "advice"}]
        (v / "manifest.yaml").write_text(yaml.safe_dump(man, allow_unicode=True))
        M.main(["freeze", str(v)])
        self.method(["Goal · how much is set", "Information · whose [information]"])
        M.main(["job", str(self.job)])
        fence = self.job / "inputs"
        self.assertTrue((fence / "evidence.md").is_symlink())
        self.assertFalse((fence / "advice.md").exists())
        self.assertFalse((fence / "handoff-W-03.md").exists())          # no kind: not the narrowed kind
        rows = yaml.safe_load((fence / "manifest.yaml").read_text())["parts"]
        self.assertIn({"part": "Information · whose", "choice": "evidence", "file": "evidence.md", "kind": "information"}, rows)
        self.assertEqual(M._sees(["Information · whose [information]", "Information · whose [knowledge-wisdom]"]),
                         {"Information · whose": {"information", "knowledge-wisdom"}})
        self.assertEqual(M._sees(["Information · whose [information]", "Information · whose"]), {"Information · whose": None})

    def test_no_fence_before_the_method_is_pinned(self):
        M.main(["freeze", str(self.block / "inputs" / "i2")])
        with self.assertRaises(SystemExit):                              # run-setup-method first
            M.main(["job", str(self.job)])
        self.assertFalse((self.job / "inputs" / "manifest.yaml").exists())

    def test_a_method_without_sees_sees_only_the_goal(self):
        M.main(["freeze", str(self.block / "inputs" / "i2")])
        (self.job / "inputs" / "method.md").write_text("---\nmethod: M04\nversion: m2\n---\n")
        M.main(["job", str(self.job)])
        self.assertFalse((self.job / "inputs" / "handoff-W-03.md").exists())
        self.assertTrue((self.job / "inputs" / "rules.md").is_symlink())

    def test_refuses_an_unsigned_goal_or_an_unfrozen_version(self):
        with self.assertRaises(SystemExit):                              # i2 not frozen yet
            M.main(["job", str(self.job)])
        M.main(["freeze", str(self.block / "inputs" / "i2")])
        j2 = self.block / "j02_g02_m01"
        with self.assertRaises(SystemExit):                              # G02 is not signed: no Job launches
            D.main(["job", str(j2), "--goal", "G02", "--method", "M01 m1", "--inputs", "i2"])
        self.assertFalse((j2 / "j02_g02_m01.md").exists())

    def test_the_workbench_reads_the_fence(self):
        M.main(["freeze", str(self.block / "inputs" / "i2")])
        self.method(["Goal · how much is set", "Information · whose"])
        M.main(["job", str(self.job)])
        j = reader().job(self.job)
        self.assertEqual(j["manifest"]["inputs"], "i2")
        self.assertEqual({f["name"] for f in j["files"]}, {"goal.md", "handoff-W-03.md", "method.md", "rules.md"})
        self.assertFalse(any(f["broken"] for f in j["files"]))
        self.assertEqual(j["method_card"]["version"], "m2")


if __name__ == "__main__":
    unittest.main()
