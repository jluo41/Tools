# src/: the Python split by page topic
state: ✅ SETTLED
owner: CC
method: mechanical move first under a byte-identical gate, features second; module names by what they render (JL 260724)

## Question
How does the board's Python stay manageable now that build.py and serve.py have both crossed
40KB and features keep landing?

QB4 already moved CSS/JS into `assets/`; the Python side was next. JL named the organizing
principle: modules named for what they render (`page_question.py`, `page_stage.py`), which
also gave the QF1 embed feature a clean seat before it was written.

## Items to Finish
- [x] 📦 Six modules under src/
      `common` (shared with serve.py) · `parse` · `body` (the §5 grammar) · `page_board` (cover + shell) · `page_question` (the card) · `page_stage` (embeds + generic renderer).
- [x] 🔬 Byte-identical regression
      board.html AND `--json` output identical before/after the move on the skill's own board.
- [x] 🔗 serve.py stops duplicating
      `QNAME` / `vet_qpath` / `q_files` now import from `src/common.py`.
- [x] 🐛 The pill-clobber bug fixed
      Found BY the byte-identical gate: old render() reused `lab`, so any question with comments wore the comments count in its state pill instead of SETTLED/PARTIAL. Reproduced first to prove the move pure, then fixed deliberately.

## Where we are
Shipped 260724. build.py is a thin CLI (arg parsing, BASE, assertions); serve.py keeps the
live layer and imports the shared helpers; the QD-group live layer was deliberately NOT
refactored while it is still forming.

## Files
- `build.py`
  Entry only.
- `src/`
  The six modules.
- `serve.py`
  Imports `src/common.py`; its own split waits for the QD group to settle.

## Law
- Refactors move code under a byte-identical gate (html AND json); features never ride along in the same step.
- Page modules are named for what they render: page_board · page_question · page_stage.
- `src/common.py` stays dependency-free; anything serve.py also needs lives there, never duplicated.

## Lesson
- The byte-identical gate caught a real user-visible bug on its first run (the state pill clobber). A refactor without that gate would have shipped the same bytes and nobody would have looked.

## Log
260724 · settled and shipped in the same body of work as QC3 and QF1
