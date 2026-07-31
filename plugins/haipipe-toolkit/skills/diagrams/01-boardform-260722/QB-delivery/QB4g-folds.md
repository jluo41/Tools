# Page folds: the drawer below the read
state: 🟡 PARTIAL · rules settled on QAa0, carved 260729; face awaits JL
owner: CC
method: Law, Lesson, Glossary, Discussion, Comments, Log sit folded below the reading path

## Question
What lives below the main reading path, and why does it start folded?
Law · Lesson · Glossary · Discussion · Comments · Log preserve rules, failures, vocabulary, deliberation, pinned remarks, and history for readers who need them, while Opening through Files stays a clean first pass.
The renderer assembles this drawer from a fixed list (`page_question.py`), so a section name it does not know renders nowhere, which is why a new section is a template decision (`QAa0`, which owns the template), never a page-local invention.

## Boundary
- ✅ Covered here
  Which sections fold below the read, their order, and the rule that they never fold a sentence's apparatus.
- ↪ Covered elsewhere
  What a Comment IS and its lifecycle: `QA6`. The Log line format: `SKILL.md`'s sync table.
  Retired section names (`Why here`) and aliases: `src/common.py`'s `ALIAS`.

## Diagram

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QAa6

## Content
### 1 · Supporting folds: preserve history without blocking the read
Law, Lesson, Glossary, Discussion, Comments, and Log sit below the main reading path and begin folded.
They preserve rules, failures, vocabulary, deliberation, pinned remarks, and change history for readers who need them, while Opening through Files remains a clean first pass.
Retired Why here content is still parsed here for compatibility, but new rationale belongs in Question.
Under the base/variant model on `QAa0`, the folds are frame: identical for every page kind.



The folds never swallow apparatus: a `>` run bound to a sentence folds under that sentence (`QAb1`), and the supporting folds render their own `>` threads as plain discussion, exactly as before the sentence apparatus existed.



## Items to Finish
- [ ] 🧠 JL confirms this face owns the folds
      Carved 260729 from QA4 §7 with the text verbatim; the history stays on `QAa0`.

## Where we are
Settled and shipped; the fixed fold list in `page_question.py` is the enforcement, and its lack of a catch-all is deliberate.

## Files
- `src/page_question.py`
  The fold assembly: Why here · Law · Lesson · Glossary · Log, plus the Comments drawer.
- `src/common.py`
  `ALIAS`, the section registry the folds resolve names through.

## Log
260729 · Marked frame under the base/variant model on QAa0: identical for every page kind
260729 · Opened by carving QA4 §7 out to its own face, text verbatim
