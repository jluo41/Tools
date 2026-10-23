"""import_fragments.py (haipipe-paper/scripts/carry_over/) on a version whose Sections keep their words only in an old
Page-local LaTeX fragment: a Section with no Draft gets one, a planned Abstract gets its § 3 filled, `page.py adopt`
then lays the words into Content, the LaTeX lane prints the fragment again line for line, and --retire moves the
old Page-local delivery/ out of the Section so the export can write the Block's Delivery."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path

CARRY = Path(__file__).parents[1] / "haipipe-paper" / "scripts" / "carry_over"
DRAFT_ENGINE = next(p for p in Path(__file__).resolve().parents if p.name == "skills") / "1_base" / "draft" / "haipipe-draft"
if str(DRAFT_ENGINE) not in sys.path:
    sys.path.insert(0, str(DRAFT_ENGINE))

spec = importlib.util.spec_from_file_location("import_fragments", CARRY / "import_fragments.py")
IMPORT = importlib.util.module_from_spec(spec)
spec.loader.exec_module(IMPORT)
from src import page_adopt  # noqa: E402

FACE = """# Introduction

page-type: section
section_kind: introduction
story-row: j01_v1_desk ## Narrative / {stem}
reader-question: Why is it hard?

## Opening

Why is it hard?

This page owns that unit's words. Its body is `delivery/latex/{stem}.tex`, 9 lines carved verbatim.

## Content

### 1 · Moves

1. The problem

## Aims
"""

FRAGMENT = r"""\section{Introduction}
\label{sec:intro}

\subsection{The Problem}

A prescription that is never collected does no good.
% src: tables/oec.tex
The firm sees only proxies.

\begin{equation}
  -2\log p(\mu)
   - 2\,\mu^\top z
\end{equation}
"""

ABSTRACT_FACE = FACE.replace("# Introduction", "# Abstract").replace("introduction", "abstract")

ABSTRACT_DRAFT = """# {stem} · draft v0.2
draft-version: v0.2
approved: ⬜

## 1 · Structure · Bullet Point Table

### Structure Overview

- C1 · Abstract · one paragraph
- C1.P1 · The whole claim

### C1.P1 · The whole claim · S1 to S2
- B1 · [Setting] A partner texts patients.
- B2 · [Finding] One price settles it.

## 2 · Scratch · What to write here

### C1.P1 · The whole claim · S1 to S2

## 3 · Draft · Reading and Revise

### C1.P1 · The whole claim · S1 to S2

## Open threads

1. none
"""

ABSTRACT_FRAGMENT = r"""\begin{abstract}
\noindent
We worked with a partner that texts patients.
% src: tables/oec.tex
One price settles the ranking.
\end{abstract}
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def quiet(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args)


class ImportFragmentsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        b = self.board = Path(self.tmp.name) / "Paper-Demo"
        write(b / "board.md", "# Paper-Demo\n")
        self.intro, self.abstract = "S-DESK-Main-1-Introduction", "S-DESK-Main-Abstract"
        v = b / "j01_v1_desk"
        write(v / self.intro / f"{self.intro}.md", FACE.format(stem=self.intro))
        write(v / self.intro / "delivery/latex" / f"{self.intro}.tex", FRAGMENT)
        write(v / self.abstract / f"{self.abstract}.md", ABSTRACT_FACE.format(stem=self.abstract))
        write(v / self.abstract / "delivery/latex" / f"{self.abstract}.tex", ABSTRACT_FRAGMENT)
        write(v / self.abstract / "draft" / f"{self.abstract}-draft-v0.2.md", ABSTRACT_DRAFT.format(stem=self.abstract))
        quiet(IMPORT.main, [str(b), "--apply"])
        for stem in (self.intro, self.abstract):
            report = page_adopt.run(v / stem)
            self.assertFalse(report["refused"], report["refused"])

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_a_section_with_no_draft_gets_one_bullet_per_line(self) -> None:
        draft = (self.board / "j01_v1_desk" / self.intro / "draft" / f"{self.intro}-draft-v0.1.md").read_text()
        self.assertIn("- C2 · The Problem", draft)                          # a \subsection opens a division
        self.assertIn("- B3 · S6 · The firm sees only proxies.", draft.split("## 3 · Draft")[1])
        self.assertIn("- B2 · S8 · -2\\log p(\\mu)", draft)                  # a line that starts with a dash is kept

    def test_the_face_names_the_draft_and_its_format(self) -> None:
        face = (self.board / "j01_v1_desk" / self.intro / f"{self.intro}.md").read_text()
        self.assertIn("task-type: draft\n", face)
        self.assertIn("content-format: latex\n", face)
        self.assertIn(f"`draft/{self.intro}-draft-v0.1.md`", face)
        self.assertNotIn("This page owns that unit's words", face)

    def test_a_planned_draft_gets_its_sentences_with_their_lines(self) -> None:
        draft = (self.board / "j01_v1_desk" / self.abstract / "draft" / f"{self.abstract}-draft-v0.2.md").read_text()
        s3 = draft.split("## 3 · Draft")[1]
        self.assertIn("- B1 · S1 · \\begin{abstract}\n  \\noindent\n  We worked with a partner that texts patients.", s3)
        self.assertIn("- B2 · S2 · % src: tables/oec.tex\n  One price settles the ranking.\n  \\end{abstract}", s3)
        self.assertIn("## Open threads", draft)                                # what follows § 3 stays

    def test_the_latex_lane_prints_each_fragment_again(self) -> None:
        good = quiet(IMPORT.verify, self.board)
        self.assertEqual(sorted(stem for _, stem in good), sorted([self.abstract, self.intro]))

    def test_retire_moves_the_old_lane_out_and_rollback_brings_it_back(self) -> None:
        quiet(IMPORT.main, [str(self.board), "--retire"])
        local = self.board / "j01_v1_desk" / self.intro / "delivery"
        self.assertFalse(local.exists())
        self.assertTrue((self.board / ".paper-fragments-1/retired/j01_v1_desk" / self.intro / "delivery").is_dir())
        quiet(IMPORT.main, [str(self.board), "--rollback"])
        self.assertTrue((local / "latex" / f"{self.intro}.tex").is_file())
        self.assertFalse((self.board / "j01_v1_desk" / self.intro / "draft" / f"{self.intro}-draft-v0.1.md").exists())
        face = (self.board / "j01_v1_desk" / self.intro / f"{self.intro}.md").read_text()
        self.assertIn("This page owns that unit's words", face)


if __name__ == "__main__":
    unittest.main()
