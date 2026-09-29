"""Every Page Run kind is known everywhere it must be (JL 260928).

A Run family's name lives in several lists: the kind tokens in
page-run-families.md, the Space folder (run_folders._KINDS), the ticket names
the workbench reads (runs._TICKET_NAME), a Runs panel button (run-cards.md),
and the full-word name (runs_panel.display_name). When one list forgets a kind,
its runs vanish or fall under "Other" (a Revise save did, 260928). This test
reads the kinds from the doc and asks every list about each one.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys
import unittest

SERVER_DIR = Path(__file__).resolve().parents[1]
PAGE_ROOT = SERVER_DIR.parents[1] / "skills" / "page" / "haipipe-page"
sys.path.insert(0, str(PAGE_ROOT))
sys.path.insert(0, str(SERVER_DIR.parent / "workbench-page"))

from src.run_folders import folder_for  # noqa: E402
from runs import _TICKET_NAME, _valid_page_run_id  # noqa: E402
from runs_panel import display_name, run_types  # noqa: E402

FAMILIES = PAGE_ROOT / "ref" / "page-run-families.md"


def kind_tokens(family: str) -> list[str]:
    """`- RP kind tokens are `struct`, `scratch`, … and `embed`;` → the tokens."""
    text = FAMILIES.read_text(encoding="utf-8")
    line = re.search(r"(?m)^- %s kind tokens are (.+?);" % family, text)
    assert line, "page-run-families.md has no '- %s kind tokens are …' line" % family
    return re.findall(r"`([a-z]+)`", line.group(1))


def sample_id(family: str, kind: str) -> str:
    if family == "RE":
        return "re-%s-01_example" % kind
    if kind == "struct":
        return "rp-struct-01"
    if kind == "sec":
        return "rp-sec-01"
    if kind == "para":
        return "rp-para-01_P01"
    return "rp-%s-01_C1.P1" % kind


class RunFamilyListsTest(unittest.TestCase):
    def setUp(self):
        self.buttons = [t for t in run_types() if t["space"] in {"Draft", "Evidence", "Delivery"}]

    def check(self, family: str, *, page_writing: bool):
        kinds = kind_tokens(family)
        self.assertTrue(kinds)
        for kind in kinds:
            run_id = sample_id(family, kind)
            ticket = run_id + ".md"
            with self.subTest(run=run_id):
                self.assertIsNotNone(folder_for(run_id),
                                     "run_folders._KINDS has no Space folder for %s" % run_id)
                self.assertTrue(_TICKET_NAME.match(ticket),
                                "runs._TICKET_NAME does not read %s" % ticket)
                self.assertTrue(any(re.search(t["pattern"], ticket) for t in self.buttons),
                                "no run-cards.md button in a Space matches %s" % ticket)
                self.assertTrue(display_name(run_id).startswith("run-"),
                                "runs_panel._DISPLAY has no full-word name for %s" % run_id)
                if page_writing:
                    self.assertTrue(_valid_page_run_id(run_id),
                                    "runs._valid_page_run_id would hold %s" % run_id)

    def test_every_page_writing_kind(self):
        self.check("RP", page_writing=True)

    def test_every_page_evidence_kind(self):
        self.check("RE", page_writing=False)

    def test_every_readable_kind(self):
        """The readable grammar (src/run_names.py, JL 260928): each kind is known everywhere."""
        from src import run_names
        writing = {"structure", "section", "paragraph", "scratch", "revise", "auto-write",
                   "evidence-embed", "context"}
        for kind in run_names.KINDS:
            run_id = run_names.mint(kind, "example", day="2026-09-29")
            ticket = run_id + ".md"
            with self.subTest(run=run_id):
                self.assertEqual(run_names.kind_of(run_id), kind)
                self.assertIsNotNone(folder_for(run_id), "no Space folder for %s" % run_id)
                self.assertTrue(_TICKET_NAME.match(ticket), "runs._TICKET_NAME does not read %s" % ticket)
                self.assertTrue(any(re.search(t["pattern"], ticket) for t in self.buttons),
                                "no run-cards.md button in a Space matches %s" % ticket)
                self.assertEqual(display_name(run_id), run_id)      # shown as it is
                if kind in writing:
                    self.assertTrue(_valid_page_run_id(run_id), "runs._valid_page_run_id would hold %s" % run_id)
        for lane in run_names.LANES:
            name = run_names.delivery_name(lane)
            with self.subTest(run=name):
                self.assertEqual(run_names.kind_of(name), "delivery")
                self.assertTrue(any(re.search(t["pattern"], name + ".sh") for t in self.buttons))


if __name__ == "__main__":
    unittest.main()
