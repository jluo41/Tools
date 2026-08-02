#!/usr/bin/env python3
"""What `apply` writes, `check` must accept. Run: python3 tests/test_roundtrip.py

This exists because the two halves disagreed for four releases and nothing
noticed. `apply` appends a record to the END of the sentence's lane run, which
`QB4`'s Law requires; `check` looked exactly one line up and demanded prose
there. So any sentence already carrying a `> Citation:` or `> Value:` lane got a
record written correctly by one half of the tool and rejected by the other.

It was invisible because the corpus that validated the tool, `QB4-overall.md`,
carries all 31 of its records on sentences with no other lane. A round trip is
not a grep, so it could never have been caught by `cli/agree.py`; it needs the
two halves actually run against each other, which is what this file does.
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "cli"))
import wdiff  # noqa: E402

OLD = "The map has three reusable skills, not two."
NEW = "The map has five reusable skills, not two."
FAILS = []


def case(name, body, host="board", expect_problems=0):
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write(body)
        p = f.name
    wdiff.apply(p, OLD, NEW, "CC", "260802 1500", host)
    bad = wdiff.check(p)
    ok = len(bad) == expect_problems
    print("%s %-46s %d problem(s), expected %d" % ("✅" if ok else "❌", name, len(bad), expect_problems))
    if not ok:
        FAILS.append((name, bad, Path(p).read_text()))
    return Path(p).read_text()


print("── what apply writes, check accepts ──")

case("bare sentence, board host",
     "# t\n\n%s\n\nAnother sentence.\n" % OLD)

case("sentence already carrying one lane",
     "# t\n\n%s\n> Citation: a source\n\nAnother sentence.\n" % OLD)

case("sentence carrying three lanes and a comment",
     "# t\n\n%s\n> Citation: a source\n> Value: 9.1 months\n> JL: is this right?\n\nAnother.\n" % OLD)

out = case("sentence already carrying a signed record",
           "# t\n\n%s\n> ✎ An ~older~ *earlier* record. · JL · 260801 1200\n\nAnother.\n" % OLD)
assert "260801 1200" in out, "the pre-existing signed record was destroyed"
print("✅ the pre-existing signed ✎ record survived")

out = case("paper host beside an existing board record",
           "# t\n\n%s\n> Citation: a source\n> ✎ An ~older~ *earlier* record. · JL · 260801 1200\n\nAnother.\n" % OLD,
           host="paper")
assert "> Note: " in out and "~~three~~" in out and "**five**" in out, "paper notation not emitted"
assert "260801 1200" in out, "a paper-host call destroyed a board record"
print("✅ paper host emits ~~old~~ **new** and destroys no ✎ record")

# A split is the rewrite this skill exists for: one long sentence becomes two or
# three short ones, one per source line. The record anchors on the FIRST of them
# (ref/change-record.md §3). Until 0.6.1 `apply` wrote it after the LAST, so the
# record described words that had moved to a line above it.
SPLIT = "It rains, and the road is wet.\nSo the road is wet."
with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
    f.write("# t\n\nIt rains, so the road is wet.\n> Citation: a source\n\nAnother.\n")
    _p = f.name
wdiff.apply(_p, "It rains, so the road is wet.", SPLIT, "CC", "260802 1500")
_lines = Path(_p).read_text().splitlines()
_i = next(k for k, x in enumerate(_lines) if x.startswith("> ✎"))
assert _lines[_i - 2] == "It rains, and the road is wet.", \
    "the record must sit under the FIRST line of a split, after its existing lanes"
assert _lines[_i - 1] == "> Citation: a source", "the existing lane run was reordered"
assert _lines[_i + 1] == "So the road is wet.", "the rest of the split must follow the record"
assert "~so~" in _lines[_i] and "*and*" in _lines[_i], \
    "the diff must cover the whole rewritten run, not just its first line"
assert not wdiff.check(_p), "check must accept what apply wrote for a split"
print("✅ %-46s %s" % ("a split anchors on its FIRST line", "record under line 1, tail below"))

print("\n── what check must still reject ──")


def rejects(name, body, why):
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write(body)
        p = f.name
    bad = wdiff.check(p)
    ok = len(bad) >= 1
    print("%s %-46s %s" % ("✅" if ok else "❌", name, why))
    if not ok:
        FAILS.append((name, bad, body))


rejects("record under no prose at all",
        "# a heading\n> ✎ some ~old~ *new* words. · CC · 260802 1500\n",
        "a record hanging off a heading is anchored to nothing")

rejects("record marking no change",
        "A sentence.\n> ✎ nothing marked here · CC · 260802 1500\n",
        "a record with no ~old~ or *new* says nothing")

rejects("malformed record",
        "A sentence.\n> ✎ missing its signature\n",
        "needs `> ✎ <diff> · WHO · YYMMDD HHMM`")

print()
if FAILS:
    for name, bad, body in FAILS:
        print("❌ %s\n%s\n%s" % (name, bad, body))
    sys.exit(1)
print("✅ all round trips hold")
