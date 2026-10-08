"""The ladder checks of check_unit.py (--ladder-result): each step's Result shape, the fence, independence, N.

A Job is scaffolded by haipipe-design's design_ladder.py and its Results are written here as the design unit writes
them (references/unit-contract.md § Ladder). Placeholders only."""
import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("design_unit_gate_ladder", HERE.parent / "scripts" / "check_unit.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
sys.path.insert(0, str(HERE.parents[1] / "haipipe-design" / "scripts"))
import design_ladder as D  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "haipipe-design" / "tests"))
from ladder_kit import ready  # noqa: E402


def put(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def card(run, **fields):
    data = yaml.safe_load((run / "run.yaml").read_text())
    data.update(fields)
    (run / "run.yaml").write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))


class LadderResultTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="design-unit-ladder-")
        block = Path(self.tmp.name) / "designs" / "b01_demo_app"
        ready(block, n=2)
        put(block / "inputs" / "i2" / "rules.md", "# Shared rules\n\n- r2.1 <a rule>\n")
        put(block / "inputs" / "i2" / "handoff-W-03.md", "# W-03\n\n<the counsel>\n")
        self.job = block / "j01_g01_m04"
        D.main(["job", str(self.job), "--goal", "G01", "--method", "M04 m2", "--inputs", "i2", "--n", "2"])
        fence = self.job / "inputs"
        put(fence / "goal.md", "# G01\n\n<aim> · for <who> · N = 2\n")
        put(fence / "method.md", "---\nmethod: M04\nversion: m2\n---\n")
        for name in ("rules.md", "handoff-W-03.md"):
            os.symlink(f"../../inputs/i2/{name}", fence / name)
        put(fence / "manifest.yaml", yaml.safe_dump({"inputs": "i2", "files": [
            {"path": n, "source": "written", "sha256": "<sha>"} for n in ("goal.md", "method.md", "rules.md",
                                                                          "handoff-W-03.md")]}))
        self.t00 = D.task(self.job, "t00", "", [])
        self.d01 = D.task(self.job, "d01", "reason-first", [])
        self.d02 = D.task(self.job, "d02", "ask-only", [])
        self.t99 = D.task(self.job, "t99", "", [])

    def tearDown(self):
        self.tmp.cleanup()

    def reason(self, source="W-03 row 2"):
        run = D.run(self.t00, "reason", "", [])
        put(run / "result" / "chains.yaml", yaml.safe_dump({"topics": [
            {"id": "T1", "title": "why act", "from": source, "steps": [{"says": "<x>", "so": "<y>"}],
             "ideas": ["I01"]},
            {"id": "T2", "title": "what to ask", "from": "own knowledge", "steps": [{"says": "<x>", "so": "<y>"}],
             "ideas": ["I02"]}]}))
        put(run / "result" / "ideas.yaml", yaml.safe_dump({"ideas": [
            {"id": "I01", "idea": "<idea 1>", "topic": "T1", "design": "d01", "name": "reason-first"},
            {"id": "I02", "idea": "<idea 2>", "topic": "T2", "design": "d02", "name": "ask-only"}]}))
        put(run / "result" / "topics.md", "# Topics\n")
        return run

    def generate(self, task, source="rule r2.1", by="designer agent"):
        run = D.run(task, "generate", "", [])
        card(run, by=by, status="closed")
        put(run / "result" / "design.md", "<opening>. <the ask>: {LINK}\n")
        put(run / "result" / "elements.yaml", yaml.safe_dump([
            {"element": "ask", "words": "<the ask>", "from": source, "because": "<why>", "step": "③", "changed": ""}]))
        return run

    def test_a_reason_inside_the_fence_passes(self):
        self.assertEqual(gate.ladder_check(self.reason()), [])

    def test_a_source_outside_the_fence_is_named(self):
        problems = gate.ladder_check(self.reason(source="a blog post"))
        self.assertTrue(any("topic T1" in p and "fence" in p for p in problems), problems)

    def test_a_generate_needs_its_draft_and_elements_in_the_fence(self):
        self.assertEqual(gate.ladder_check(self.generate(self.d01)), [])
        bad = self.generate(self.d02, source="W-99 row 1")
        self.assertTrue(any("element ask" in p for p in gate.ladder_check(bad)))

    def test_a_verify_by_the_generator_is_refused(self):
        self.generate(self.d01)
        run = D.run(self.d01, "verify", "", [])
        self.assertEqual(run.name, "run-verify-d01-v1")
        put(run / "result" / "review.md", "# Review\n\nT0 ✓ · T1 ✓\n")
        card(run, status="passed", tests={"T0": "✓", "T1": "✓"}, by="another agent")
        self.assertEqual(gate.ladder_check(run), [])
        card(run, by="designer agent")
        self.assertTrue(any("not independent" in p for p in gate.ladder_check(run)))

    def test_a_ranking_keeps_the_jobs_n(self):
        run = D.run(self.t99, "rank", "", [])
        put(run / "result" / "ranking.csv", "rank,design,predicted,why,kept\n1,d02,+x [lo; hi],<why>,yes\n"
                                             "2,d01,+x [lo; hi],<why>,yes\n")
        self.assertEqual(gate.ladder_check(run), [])
        put(run / "result" / "ranking.csv", "rank,design,predicted,why,kept\n1,d02,+x [lo; hi],<why>,yes\n"
                                             "2,d01,+x [lo; hi],<why>,no\n3,d07,+x [lo; hi],<why>,no\n")
        problems = gate.ladder_check(run)
        self.assertTrue(any("keeps 1" in p for p in problems) and any("d07" in p for p in problems), problems)

    def test_a_hard_run_without_its_result_and_a_wrong_name_fail(self):
        run = D.run(self.t00, "reason", "", [])
        (run / "result").rmdir()
        self.assertTrue(any("result/" in p for p in gate.ladder_check(run)))
        other = put(self.t00 / "runs" / "run-draw-s01" / "run.yaml", "type: draw\n").parent
        self.assertTrue(gate.ladder_check(other)[0].endswith("(run-<reason|generate|verify|revise|rank>-<target>)"))

    def test_the_fence_rule(self):
        names = ["goal.md", "rules.md", "handoff-W-03.md"]
        for ok in ("own knowledge", "rules.md", "rule r2.1", "W-03 row 2", "handoff-W-03.md · row 4", "goal"):
            self.assertTrue(gate.in_fence(ok, names), ok)
        for bad in ("", "a paper", "W-04 row 1", "row 2"):
            self.assertFalse(gate.in_fence(bad, names), bad)


if __name__ == "__main__":
    unittest.main()
