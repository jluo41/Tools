"""A theme Block's UI view opens with one 🧩 Elements section per type of page (JL 261118): each type's views as
groups, one left tab per part, read from `delivery/page-spec/<level>-elements.md`, each with its marks and the part live."""
import tempfile
import unittest
from pathlib import Path

from live.focus_ui_elements import elements_section, parse, parse_types

SPEC = """# 🧩 Work Block
example: b90

## Page frame

### Path
show: .focus-crumb

## Plan + Results

### Section
show: details.band-sec
view: standing
topic: 1 · 🗃️ Data preparation · free
folder: a band of Jobs
- Starts closed.

# 🤝 Collaboration Block
example: b01

## Overview

### 🎯 Goal
show: details.band-sec
text: Goal
view: overview
"""


class UiElementsTest(unittest.TestCase):
    def test_parse_reads_types_views_and_parts(self):
        types = parse_types(SPEC)
        self.assertEqual([(k, e) for k, e, _ in types], [("🧩 Work Block", "b90"), ("🤝 Collaboration Block", "b01")])
        views = types[0][2]
        self.assertEqual([v for v, _ in views], ["Page frame", "Plan + Results"])
        self.assertEqual(views[1][1][0]["rules"], ["Starts closed."])
        self.assertEqual(views[1][1][0]["topics"], ["1 · 🗃️ Data preparation · free"])
        self.assertEqual([e["name"] for _, els in parse("## A\n## B\n") for e in els], ["A", "B"])   # no types, no views

    def test_one_section_per_type_with_marks_and_the_part_live(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            block = root / "b17_theme_work"
            (block / "delivery" / "page-spec").mkdir(parents=True)
            (block / "board.md").write_text("# b17\n")
            self.assertEqual(elements_section(block, root, "block", "/x?path=b90"), [])     # no file: none
            (block / "delivery" / "page-spec" / "block-elements.md").write_text(SPEC)
            secs = elements_section(block, root, "block", "/x?path=b90")
            self.assertEqual([t for t, _, _ in secs], ["🧩 Elements · 🧩 Work Block", "🧩 Elements · 🤝 Collaboration Block"])
            body = secs[0][2]
            self.assertIn("<h3 class=pb-group>Plan + Results</h3>", body)
            self.assertIn('data-addr="elements.block.Work-Block.Plan-Results.Section"', body)
            self.assertIn('group=standing', body)
            self.assertIn('data-show="details.band-sec"', body)
            self.assertNotIn("a band of Jobs", body)
            self.assertIn('<span class=el-tn>Topic 1</span> 🗃️ Data preparation <small class="el-tk el-free">free</small>', body)                             # notes stay in the file


if __name__ == "__main__":
    unittest.main()
