"""The draft page's manual says what the page shows: skills/1_base/draft/workbench-task-draft/SKILL.md names the
views the code builds and nothing the page no longer has (its CONSTITUTION A02)."""
import re
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
TOOLKIT = next(p for p in HERE.parents if p.name == "haipipe-toolkit")
MANUAL = TOOLKIT / "skills/1_base/draft/workbench-task-draft/SKILL.md"
WORDS = HERE.parents[1] / "focus_draft_words.py"


def page_section() -> str:
    text = MANUAL.read_text(encoding="utf-8")
    return text.split("\nThe page\n", 1)[1].split("\nOther routes\n", 1)[0]


class ManualMatchesPageTest(unittest.TestCase):
    def test_every_view_the_code_builds_is_named(self):
        work = re.search(r"^WORK = (\(.*?\))$", WORDS.read_text(encoding="utf-8"), re.M | re.S).group(1)
        names = [n.split(" · ", 1)[-1] for _, n in eval(work)]          # the button names, numbered on the page
        section = page_section()
        for name in names:
            self.assertRegex(section, rf"\d · {name}\b", f"the manual does not name the {name} view")

    def test_no_view_or_band_the_page_no_longer_has(self):
        section = page_section()
        for gone in ("· Text", "· Write", "· Revise", "· Runs", "MindMap", "Plan + Results", "Around the Work"):
            self.assertNotIn(gone, section, f"the manual still describes {gone!r} on the page")


if __name__ == "__main__":
    unittest.main()
