"""A draft Task's §1 Structure map is drawn by haipipe-mindmap's shared renderer (mapview.py), the one a Studio topic's
mind map is drawn by too; moving or breaking that skill breaks §1, so this fails first."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap
bootstrap()

from live import draft_steps  # noqa: E402
from live import frame  # noqa: E402

DRAFT = """# t01 · Introduction · draft v0.1

approved:
arc: why agents change who is found

## 1 · Structure · Bullet Point Table

### Structure Overview

- C1 · Introduction
- C1.P1 · Patients move to AI agents
  → C1.P2: Why should physicians care?
- C1.P2 · Who is seen

### C1.P1 · Patients move to AI agents

- B1 · S1 · [Stakes] How patients find a physician
  Note: the opening stakes
- B2 · S2 · [Search] Many look physicians up online

### C1.P2 · Who is seen

- B3 · S3 · [Reach] Agents may narrow coverage

## 3 · Draft · Reading and Revise

### C1.P1 · Patients move to AI agents

- S1 · How patients find a physician shapes whom they choose.
"""


def draft_task(root: Path) -> Path:
    task = root / "Project" / "paper" / "Paper-Demo" / "j01_v1_send" / "t01_introduction"
    (task / "draft").mkdir(parents=True)
    (task / "t01_introduction.md").write_text("# t01 · Introduction\n\ntask-type: draft\n", encoding="utf-8")
    (task / "draft" / "t01_introduction-draft-v0.1.md").write_text(DRAFT, encoding="utf-8")
    return task


class StructureMapTest(unittest.TestCase):
    def test_section_1_is_drawn_by_the_shared_renderer(self):
        mv = draft_steps._mapview()
        self.assertIn("haipipe-mindmap", str(Path(mv.__file__)))         # the shared skill, wherever it lives
        with tempfile.TemporaryDirectory() as tmp:
            task = draft_task(Path(tmp))
            d = draft_steps.read_draft(task)
            out = draft_steps._plan_map(d, {"cards": []}, "C1 · Introduction", "Project/paper/Paper-Demo/j01_v1_send/t01_introduction")
            self.assertTrue(out.startswith(mv.CSS))
            self.assertIn(mv.JS, out)
            self.assertNotIn("data-endpoint", out)                          # a draft posts to /_board/draft-plan
            self.assertIn('<div class=pm-para data-p="C1.P1">', out)
            self.assertIn('<li data-s="S1" title="the opening stakes">', out)
            self.assertIn('data-edit=ask data-p="C1.P1" data-raw="Why should physicians care?"', out)
            self.assertIn('<span class=pm-role data-edit=role data-raw="Stakes"', out)

    def test_an_edit_on_section_1_is_still_written_into_the_draft(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task = draft_task(root)
            code, res = draft_steps.plan_act(root, {"task": "Project/paper/Paper-Demo/j01_v1_send/t01_introduction",
                                                    "file": "t01_introduction-draft-v0.1.md", "what": "words",
                                                    "s": "S2", "was": "Many look physicians up online",
                                                    "value": "Many look physicians up on rating sites"})
            self.assertEqual((code, res.get("ok")), (200, True), res)
            self.assertIn("- B2 · S2 · [Search] Many look physicians up on rating sites",
                          (task / "draft" / "t01_introduction-draft-v0.1.md").read_text(encoding="utf-8"))

    def test_a_topic_mind_map_and_section_1_share_the_css_and_script(self):
        mv = draft_steps._mapview()
        with tempfile.TemporaryDirectory() as tmp:
            md = Path(tmp) / "s01-x.mindmap.md"
            md.write_text("# X <!-- root -->\n\n- [kind] A branch <!-- n01 -->\n  - a point <!-- n02 -->\n", encoding="utf-8")
            out = frame.mindmap_module().fragment(md, "s01-x.mindmap.md")
            self.assertIn(mv.CSS, out)
            self.assertIn(mv.JS, out)
            self.assertIn('data-endpoint="/_board/mindmap"', out)


if __name__ == "__main__":
    unittest.main()
