"""The insight family's checks, each proven to FAIL on a board broken one way.

Same proof discipline as test_design_family: every case breaks a synthetic
InsightBoard in exactly ONE way and asserts the matching code fires, and the
intact board must be clean so a rule cannot pass by firing on everything.
"""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from cli.check import Report, check_insight_family, check_partition_register

W_PAGE = "1-F-full/FW01-send-salience/FW01-send-salience.md"
Q_PAGE = "0-MT-meta/MT02-question-information/MT02-question-information.md"
I_PAGE = "1-F-full/BI03-audience/BI03-audience.md"
M_PAGE = "0-MT-meta/MT00-meta/MT00-meta.md"

M_OK = """# MT00
page-type: meta

**Partitions**: the only place a partition is defined.

```text
letter name          population block                config        group
─────────────────────────────────────────────────────────────────────────
F      full          where: []  declared unfiltered  full.yaml     1-F-full/
                     400,000 of 400,000 rows · 100.0000%
B      youngmale     patient_gender eq M             ymale.yaml    2-B-youngmale/
                     AND age lte 35.0
                      50,000 of 400,000 rows ·  12.5000%
C      youngfemale   patient_gender eq F             yfem.yaml     3-C-youngfemale/
                     AND age lte 35.0
                     100,000 of 400,000 rows ·  25.0000%
X      cross         no rows of its own              (none)        9-X-cross/
```
"""

OVERLAP_ROW = """D      older         age gte 55.0                    older.yaml    4-D-older/
                     280,000 of 400,000 rows ·  70.0000%
X      cross"""

COVARIATE_ROW = """J      lowincome     income_level lte 3              lowinc.yaml   7-J-lowincome/
                      40,000 of 400,000 rows ·  10.0000%
X      cross"""


def pcheck(text):
    rep = Report()
    check_partition_register(text, "MT00-meta.md", rep)
    return [c for _, c, _, _ in rep.rows]

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


def build(tmp, w=W_OK, q=Q_OK, i=I_OK, m=M_OK):
    d = Path(tmp) / "A00_InsightBoard-Test"
    for rel, text in ((W_PAGE, w), (Q_PAGE, q), (I_PAGE, i), (M_PAGE, m)):
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


class TestPartitionRegister(unittest.TestCase):
    """Clause ① of the partition test, proven on the shape that broke A00."""

    def test_intact_register_is_clean(self):
        self.assertEqual(pcheck(M_OK), [])

    def test_overlapping_partitions_exceed_the_extract(self):
        # 12.5 + 25.0 + 70.0 = 107.5%: three disjoint cuts of one extract
        # cannot cover more than the extract, whatever the filters say.
        self.assertIn("partition-sum-over-100",
                      pcheck(M_OK.replace("X      cross", OVERLAP_ROW, 1)))

    def test_covariate_partition_is_cross_cutting(self):
        # 10% keeps the sum legal, so ONLY the axis rule may catch it —
        # income_level shares no column with patient_gender or age.
        codes_ = pcheck(M_OK.replace("X      cross", COVARIATE_ROW, 1))
        self.assertIn("partition-cross-cutting", codes_)
        self.assertNotIn("partition-sum-over-100", codes_)

    def test_template_and_cross_are_exempt(self):
        # F is 100% by construction and X holds no rows; counting either would
        # fire on every conformant partition-major board ever built.
        self.assertNotIn("partition-sum-over-100", pcheck(M_OK))
        self.assertNotIn("partition-cross-cutting", pcheck(M_OK))

    def test_one_partition_is_never_cross_cutting(self):
        solo = M_OK.replace("""C      youngfemale   patient_gender eq F             yfem.yaml     3-C-youngfemale/
                     AND age lte 35.0
                     100,000 of 400,000 rows ·  25.0000%
""", "")
        self.assertEqual(pcheck(solo), [])

    def test_unparseable_register_is_silent(self):
        self.assertEqual(pcheck("# MT00\npage-type: meta\n\nno register here\n"), [])

    def test_rounding_does_not_trip_the_sum(self):
        # Percentages are printed rounded; a rule firing at 100.01% is a rule
        # people learn to skip.
        near = M_OK.replace("·  12.5000%", "·  75.2000%").replace("·  25.0000%", "·  25.0000%")
        self.assertEqual(pcheck(near), [])


if __name__ == "__main__":
    unittest.main()
