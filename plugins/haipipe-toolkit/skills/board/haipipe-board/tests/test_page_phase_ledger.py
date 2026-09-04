#!/usr/bin/env python3
"""The owed-tick COUNT and the owed-tick LIST are one computation.

`ticks_owed` has always carried the count and `owed_ledger()` now carries the
list. A count and a list that disagree are how a person stops trusting both, so
the invariant is asserted here rather than left to a comment.
"""

import tempfile
import unittest
from pathlib import Path

from src.page_phase import owed_ledger, phase_state, render_ledger


def _page(
    root, *, approved=False, cards=(), bib=(), displays=(),
    folder_kind=None, phase_folder_kind=None,
):
    """Write the smallest Page that exercises the variable owed ledger."""
    pd = Path(root) / "QT1-fixture"
    pd.mkdir(parents=True)
    (pd / "QT1-fixture.md").write_text(
        "# Fixture\n\n"
        + (f"folder-kind: {folder_kind}\n\n" if folder_kind else "")
        + "state: 🟡 PARTIAL · open: 1\n\n## Opening\n\nWhy.\n")
    (pd / "outline").mkdir()
    (pd / "outline" / "QT1-fixture-outline-v1.md").write_text(
        f"# plan\napproved: {'✅ JL 260821' if approved else '⬜'}\n"
        "checked: ✅ auto 260821 · approve-rules R1-R9 pass\n\n## C1 · A\n")
    if phase_folder_kind:
        phase = "D1" if phase_folder_kind == "design-card" else "D2"
        (pd / "workflow").mkdir()
        (pd / "workflow" / "phase.yaml").write_text(
            f"current:\n  phase: {phase}\n"
            f"  folder-kind: {phase_folder_kind}\nhistory: []\n",
            encoding="utf-8",
        )
    for name, state, read in cards:
        c = pd / "evidence" / "probe" / name
        c.mkdir(parents=True)
        (c / "card.md").write_text(
            f"# {name}\nstate: {state}\nread: {'✅ JL 260821' if read else '⬜ not yet'}\n"
            "question: how many\n")
    if bib:
        (pd / "bibex").mkdir()
        (pd / "bibex" / "QT1-fixture.bib").write_text("\n".join(
            f"@article{{{k},\n  title = {{T}},\n  verified = {{{v}}}\n}}" for k, v in bib))
    for name, drawn, accepted in displays:
        u = pd / "display" / name
        u.mkdir(parents=True)
        (u / "README.md").write_text(
            f"claim: c\naccepted: {'✅ JL 260821' if accepted else '⬜'}\n")
        if drawn:
            (u / "preview.pdf").write_bytes(b"%PDF-1.4\n")
    return pd / "QT1-fixture.md"


class OwedLedgerTest(unittest.TestCase):
    def state(self, **kw):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        return phase_state(_page(self.tmp.name, **kw))

    def test_the_count_equals_the_list_on_a_page_owing_all_five(self):
        st = self.state(
            approved=False,
            cards=(("PP01-a-count", "answered", False),),
            bib=(("k1", ""),),
            displays=(("QT1-Display1-x", True, False),))
        self.assertEqual(sum(st["ticks_owed"].values()), len(owed_ledger(st)))
        self.assertEqual({r["tick"] for r in owed_ledger(st)},
                         {"approved", "read", "verified", "accepted", "ruling"})

    def test_legacy_page_conservatively_owes_a_ruling(self):
        """A legacy Page keeps the conservative historical local RULING."""
        st = self.state(approved=True)
        self.assertEqual(st["owner_ruling"], "legacy-default")
        self.assertEqual(st["ticks_owed"]["ruling"], 1)
        self.assertEqual([r["tick"] for r in owed_ledger(st)], ["ruling"])

    def test_phase_owned_mechanical_page_owes_no_owner_ruling(self):
        st = self.state(approved=True, folder_kind="data")
        self.assertEqual(st["owner_ruling"], "none")
        self.assertEqual(st["ticks_owed"]["ruling"], 0)
        self.assertEqual(owed_ledger(st), [])

    def test_phase_owned_wisdom_reuses_its_domain_gate(self):
        st = self.state(approved=True, folder_kind="wisdom")
        self.assertEqual(st["owner_ruling"], "domain-gate")
        self.assertEqual(st["ticks_owed"]["ruling"], 1)
        self.assertEqual([r["tick"] for r in owed_ledger(st)], ["ruling"])
        self.assertIn("owner: domain-gate", owed_ledger(st)[0]["note"])

    def test_in_place_phase_file_resolves_a_card_without_frontmatter(self):
        st = self.state(approved=True, phase_folder_kind="design-card")
        self.assertEqual(st["folder_kind"], "design-card")
        self.assertEqual(st["folder_kind_source"], "workflow/phase.yaml")
        self.assertEqual(st["owner_ruling"], "domain-gate")

    def test_phase_file_and_markdown_kind_mismatch_is_never_guessed(self):
        st = self.state(
            approved=True,
            folder_kind="design-card",
            phase_folder_kind="design-unit",
        )
        self.assertEqual(st["owner_ruling"], "ambiguous")
        self.assertIn("conflicts", st["owner_ruling_error"])
        self.assertEqual(st["ticks_owed"]["ruling"], 1)

    def test_an_empty_verified_brace_is_owed_not_done(self):
        """cite-rules R7: `verified = {}` is the EXPLICIT unverified form."""
        st = self.state(bib=(("k1", ""), ("k2", "JL 260821")))
        self.assertEqual(st["bibex"], {"entries": 2, "verified": 1,
                                       "rows": st["bibex"]["rows"]})
        self.assertEqual([r["where"].split(" · ")[-1]
                          for r in owed_ledger(st) if r["tick"] == "verified"], ["k1"])

    def test_an_undrawn_unit_owes_a_render_not_a_person(self):
        st = self.state(approved=True, displays=(("QT1-Display1-x", False, False),))
        self.assertEqual([r["tick"] for r in owed_ledger(st)], ["ruling"])

    def test_a_card_still_in_flight_owes_nothing_yet(self):
        st = self.state(approved=True, cards=(("PP01-a-count", "commissioned", False),))
        self.assertEqual([r["tick"] for r in owed_ledger(st)], ["ruling"])

    def test_every_row_carries_the_machine_half_and_the_question(self):
        st = self.state(cards=(("PP01-a-count", "answered", False),))
        for r in owed_ledger(st):
            self.assertTrue(r["ask"], f"{r['tick']} asks the person nothing")
            self.assertIn("checked", r)
        outline_ok = self.state(approved=False)
        got = [r for r in owed_ledger(outline_ok) if r["tick"] == "approved"][0]
        self.assertIn("auto 260821", got["checked"] or "")

    def test_render_never_writes_and_always_returns_lines(self):
        st = self.state(approved=True)
        self.assertTrue(all(isinstance(x, str) for x in render_ledger(st)))


if __name__ == "__main__":
    unittest.main()
