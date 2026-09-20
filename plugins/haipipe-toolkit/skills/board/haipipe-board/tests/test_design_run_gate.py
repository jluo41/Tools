"""Board admission delegates native Design integrity to the worker gate."""
import importlib.util
from pathlib import Path
import unittest
from cli.check import Report, check_design_family

HELPER = (Path(__file__).resolve().parents[3] / "design"
          / "haipipe-design-unit" / "tests" / "test_unit.py")
spec = importlib.util.spec_from_file_location("unit_fixtures", HELPER)
fixtures = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixtures)


class NativeDesignBoardGateTest(unittest.TestCase):
    def setUp(self):
        self.case = fixtures.DesignUnitGateTest()
        self.case.setUp()
        self.addCleanup(self.case.tearDown)

    def test_valid_native_result_is_admitted(self):
        self.case.result(self.case.ticket())
        report = Report()
        check_design_family(self.case.owner, report)
        self.assertEqual(report.rows, [])

    def test_known_broken_native_result_reaches_board_error(self):
        ticket = self.case.ticket()
        result = self.case.result(ticket, "Missing required placeholder")
        runtime_path = result.parent / "runtime.yaml"
        runtime = fixtures.gate.document(runtime_path)
        runtime.update(status="complete", started_at="now", finished_at="later")
        self.case.dump(runtime_path, runtime)
        report = Report()
        check_design_family(self.case.owner, report)
        self.assertTrue(any(row[1] == "design-run-contract" for row in report.rows))

    def test_orphan_native_result_is_not_hidden_by_absent_board_page(self):
        orphan = self.case.owner / "results" / "rd20_generate_orphan"
        orphan.mkdir(parents=True)
        report = Report()
        check_design_family(self.case.owner, report)
        self.assertTrue(any(row[1] == "design-run-contract" for row in report.rows))

    def test_page_delivery_result_is_not_sent_to_design_gate(self):
        delivery = self.case.owner / "results" / "rd01_latex"
        delivery.mkdir(parents=True)
        report = Report()
        check_design_family(self.case.owner, report)
        self.assertFalse(any(row[1] == "design-run-contract" for row in report.rows))


if __name__ == "__main__":
    unittest.main()
