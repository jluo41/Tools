"""The carry-over scripts (haipipe-paper/scripts/carry_over/) on a Board shaped like ScalingGlucose's before
261009: no story-current in board.md, the build's order naming the Story, a "Question 0", and a "Question logic"
heading that is not a question. migrate_paper.py then topics_paper.py must keep every question's number, leave
"Question logic" in the Story, hand §8 to the version with each Section's story-row following it, and rename the
Story's draft/records/ files with its new name."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

CARRY = Path(__file__).parents[1] / "haipipe-paper" / "scripts" / "carry_over"


def load(name):
    spec = importlib.util.spec_from_file_location(name, CARRY / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MIGRATE, TOPICS = load("migrate_paper"), load("topics_paper")

BOARD = """# Paper-Demo · paper board
spine: one idea
dialect: paper
paper-root: .

## Pages

### STORY · A1-Story
Story00-ideation.md
StoryA-desk-idea.md

### MAIN · Ba-DESK-Main
S-DESK-Main-1-Introduction.md
"""

STORY = """# StoryA-desk-idea

## Opening

The paper in one line.

## Content

### 3 · Research questions

#### 3.0 · Question 0 · RQ0
- **Name**: The tasks
- **Question**: We say what every question is scored on.

#### 3.3 · Question 3 · RQ3
- **Name**: Different Prediction Horizon
- **Question**: We check how scale helps as we predict further ahead.

#### 3.7 · Question logic

Question 0 comes first; the rest lean on it.

### 8 · Section Narrative

| page | reader question |
|---|---|
| S-DESK-Main-1-Introduction | Why doubt it? |

<!-- haipipe:compile-order:start -->
- S-DESK-Main-1-Introduction
<!-- haipipe:compile-order:end -->
"""

SECTION = """# S-DESK-Main-1-Introduction

story-row: StoryA-desk-idea §8.3 / S-DESK-Main-1-Introduction · StoryA-desk-idea v0.2
"""

TOML = """desk = "desk"

[pages]
main = "../Ba-DESK-Main"
order = "../A1-Story/StoryA-desk-idea/StoryA-desk-idea.md"
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def quiet(fn, argv):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(argv)


class CarryOverTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        b = self.board = Path(self.tmp.name) / "Paper-Demo"
        write(b / "board.md", BOARD)
        write(b / "A1-Story/Story00-ideation/Story00-ideation.md", "# Story00-ideation\n\n## Content\n")
        write(b / "A1-Story/StoryA-desk-idea/StoryA-desk-idea.md", STORY)
        write(b / "A1-Story/StoryA-desk-idea/draft/records/StoryA-desk-idea-context.md", "# context\n")
        write(b / "Ba-DESK-Main/S-DESK-Main-1-Introduction/S-DESK-Main-1-Introduction.md", SECTION)
        write(b / "delivery/paper-build.toml", TOML)
        quiet(MIGRATE.main, [str(b), "--apply"])
        quiet(TOPICS.main, [str(b), "--apply"])

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_the_version_tells_the_story_its_build_reads(self) -> None:
        face = (self.board / "j01_v1_desk/j01_v1_desk.md").read_text()
        self.assertIn("tells: studio/s02-story-desk-idea", face)
        self.assertIn("## Narrative", face)
        self.assertIn("- S-DESK-Main-1-Introduction", face)              # the compile order came with it
        self.assertIn("story-current: s02-story-desk-idea", (self.board / "board.md").read_text())

    def test_questions_keep_their_numbers_and_question_logic_stays(self) -> None:
        reports = sorted(p.name for p in (self.board / "reports").iterdir())
        self.assertEqual(reports, ["q00_the_tasks", "q03_different_prediction_horizon"])
        story = (self.board / "studio/s02-story-desk-idea/s02-story-desk-idea.md").read_text()
        self.assertIn("#### 3.7 · Question logic", story)
        self.assertIn("the rest lean on it", story)
        self.assertNotIn("#### 3.3 · Question 3", story)
        self.assertNotIn("### 8 · Section Narrative", story)               # §8 left only because a version took it

    def test_the_storys_records_follow_its_new_name(self) -> None:
        records = self.board / "studio/s02-story-desk-idea/draft/records"
        self.assertEqual([p.name for p in records.iterdir()], ["s02-story-desk-idea-context.md"])

    def test_the_sections_story_row_follows_its_row(self) -> None:
        face = (self.board / "j01_v1_desk/S-DESK-Main-1-Introduction/S-DESK-Main-1-Introduction.md").read_text()
        self.assertIn("story-row: j01_v1_desk ## Narrative / S-DESK-Main-1-Introduction · s02-story-desk-idea v0.2",
                      face)


if __name__ == "__main__":
    unittest.main()
