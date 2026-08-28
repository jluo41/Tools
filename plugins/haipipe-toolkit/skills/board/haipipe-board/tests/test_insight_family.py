"""The insight family's checks, each proven to FAIL on a board broken one way.

Same proof discipline as test_design_family: every case breaks a synthetic
InsightBoard in exactly ONE way and asserts the matching code fires, and the
intact board must be clean so a rule cannot pass by firing on everything.
"""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from cli.check import Report, check_insight_family

W_PAGE = "1-F-full/FW01-send-salience/FW01-send-salience.md"
Q_PAGE = "0-MT-meta/MT02-question-information/MT02-question-information.md"
I_PAGE = "1-F-full/BI03-audience/BI03-audience.md"

W_OK = """# FW01
page-type: wisdom

FINDING     the arm separates
SERVES      QW1 · BR00 A6.1

signed: ✅ JL 260828

## Log
"""

Q_OK = """# MT02
page-type: question

QI3   who is here?   🟡 BI03 final
QI5   drug class     🚫 F-only
"""

I_OK = """# BI03
page-type: information

## Log

260828 · QI3's register cell reads 🟡 final on this page's filter sentence.
"""


def build(tmp, w=W_OK, q=Q_OK, i=I_OK):
    d = Path(tmp) / "A00_InsightBoard-Test"
    for rel, text in ((W_PAGE, w), (Q_PAGE, q), (I_PAGE, i)):
        f = d / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8")
    (d / "board.md").write_text("# Test InsightBoard\n", encoding="utf-8")
    return d


def codes(d):
    rep = Report()
    check_insight_family(d, rep)
    return [c for _, c, _, _ in rep.rows]


class TestInsightFamily(unittest.TestCase):
    def test_intact_board_is_clean(self):
        with TemporaryDirectory() as tmp:
            self.assertEqual(codes(build(tmp)), [])

    def test_handoff_without_signed_row_fails(self):
        with TemporaryDirectory() as tmp:
            d = build(tmp, w=W_OK.replace("\nsigned: ✅ JL 260828\n", ""))
            self.assertIn("wisdom-handoff-no-signed-row", codes(d))

    def test_unsigned_handoff_warns(self):
        with TemporaryDirectory() as tmp:
            d = build(tmp, w=W_OK.replace("signed: ✅ JL 260828", "signed: ⬜"))
            self.assertIn("wisdom-handoff-unsigned", codes(d))

    def test_deferring_w_owes_nothing(self):
        with TemporaryDirectory() as tmp:
            d = build(tmp, w="# FW01\npage-type: wisdom\n\ndefer to FW09\n")
            self.assertEqual(codes(d), [])

    def test_legacy_refusal_token_warns(self):
        with TemporaryDirectory() as tmp:
            for bad in ("🚫Fonly", "🚫 F only", "🚫F-only"):
                d = build(tmp, q=Q_OK.replace("🚫 F-only", bad))
                self.assertIn("refusal-token-legacy", codes(d), bad)

    def test_canonical_token_is_clean(self):
        with TemporaryDirectory() as tmp:
            self.assertNotIn("refusal-token-legacy", codes(build(tmp)))

    def test_final_without_page_receipt_warns(self):
        with TemporaryDirectory() as tmp:
            d = build(tmp, i=I_OK.replace("260828 · QI3's register cell reads 🟡 final on this page's filter sentence.\n", ""))
            self.assertIn("partial-final-no-page-receipt", codes(d))

    def test_second_final_on_same_line_is_checked(self):
        with TemporaryDirectory() as tmp:
            d = build(tmp, q=Q_OK.replace("🟡 BI03 final", "🟡 BI03 final  🟡 ZI99 final"))
            self.assertIn("partial-final-ghost-page", codes(d))

    def test_unspaced_mark_warns(self):
        with TemporaryDirectory() as tmp:
            for bad in ("🟡BI03 final", "🚫thin", "⬜OPEN"):
                d = build(tmp, q=Q_OK.replace("🟡 BI03 final", bad))
                self.assertIn("mark-spacing-legacy", codes(d), bad)

    def test_mark_mention_in_log_is_not_flagged(self):
        with TemporaryDirectory() as tmp:
            q = Q_OK + "\n## Log\n\n260828 · sweep retired the legacy token 🚫Fonly from this Queue.\n"
            d = build(tmp, q=q)
            self.assertNotIn("mark-spacing-legacy", codes(d))

    def test_receipt_outside_log_section_still_warns(self):
        with TemporaryDirectory() as tmp:
            i = "# BI03\npage-type: information\n\n260828 · QI3 final receipt in prose, not Log.\n\n## Log\n"
            d = build(tmp, i=i)
            self.assertIn("partial-final-no-page-receipt", codes(d))

    def test_final_citing_ghost_page_fails(self):
        with TemporaryDirectory() as tmp:
            d = build(tmp, q=Q_OK.replace("🟡 BI03 final", "🟡 ZI99 final"))
            self.assertIn("partial-final-ghost-page", codes(d))


if __name__ == "__main__":
    unittest.main()
