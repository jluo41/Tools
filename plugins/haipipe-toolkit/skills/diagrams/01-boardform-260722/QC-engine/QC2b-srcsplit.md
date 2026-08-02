# src/: the Python split by page topic
state: ✅ SETTLED
owner: CC
method: mechanical move first under a byte-identical gate, features second; module names by what they render (JL 260724)

## Opening
How should the renderer's Python be divided so a new feature has an obvious home before it is written?

One large module hid page-specific behavior inside shared functions and made unrelated changes touch the same file.
The hard part was moving code without changing either the HTML or the parsed data.
Names based on what a module renders give future work a stable place and keep shared helpers singular.
It succeeds when the split is byte-identical and consumers stop carrying private copies of the same logic.

**Covered elsewhere**: Moving CSS and JS out to `assets/` is `QC2`; what those modules actually render is `QB4`'s page layout; the live server's own behavior belongs to the `QD` group.


## Diagram

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QC3

## Aims
- [x] 📦 Six modules under src/
      `common` (shared with serve.py) · `parse` · `body` (the §5 grammar) · `page_board` (cover + shell) · `page_question` (the card) · `page_stage` (embeds + generic renderer).
- [x] 🔬 Byte-identical regression
      board.html AND `--json` output identical before/after the move on the skill's own board.
- [x] 🔗 serve.py stops duplicating
      `QNAME` / `vet_qpath` / `q_files` now import from `src/common.py`.
- [x] 🐛 The pill-clobber bug fixed
      Found BY the byte-identical gate: old render() reused `lab`, so any question with comments wore the comments count in its state pill instead of SETTLED/PARTIAL.
      Reproduced first to prove the move pure, then fixed deliberately.

## States
Shipped 260724. build.py is a thin CLI (arg parsing, BASE, assertions); serve.py keeps the live layer and imports the shared helpers; the QD-group live layer was deliberately NOT refactored while it is still forming.

- 260731 JL · 🧩 The browser assets split by topic, then split again
  JL: "do we write everything into one board.js? can we split it like live, by topic, otherwise it is too long and touching one thing shakes everything."
  A first pass by a concurrent session took `board.js` from 3509 lines to 15 topic files and `board.css` from 1565 to 9, assembled by `src/assets.py` in sorted path order.
  Three files were still large enough to have the same problem inside them, so they were cut at their own topic banners: chat into open, sessions, focus, render, permissions, and prefs+paste; the comment dock into highlight, select, panel, write, paste, and excalidraw; the sentence layer into apparatus, address, and breadcrumb.
  27 JS files now, none over 365 lines, and 9 CSS files.
  The assembly rule is the dumbest one that can work, concatenate every part in sorted path order, so a new part is a new filename and there is no manifest to keep in sync.
  What makes that safe is not care but a gate: these parts are FRAGMENTS of shared closures, `40-sentence.js` began mid-function with `if (!b) return;`, so a rename out of order silently breaks the whole file. `assets.py verify()` parses the assembled text with node on every build and fails the BUILD rather than the browser; renaming one part in a scratch copy produced `SyntaxError: Single function literal required`, which is the proof it is not decorative.
  Parsing is not running, though, so the split was also driven in a real browser afterwards: chat drawer, chat fab, comment dock, comment fab, sidebar, sidebar handle, `boardPath()`, and a discussion write that reached the `.md`, all green.

## Files
- `cli/build.py`
  Entry only.
- `src/`
  The six modules.
- `cli/serve.py`
  Imports `src/common.py`; its own split waits for the QD group to settle.

## Law
- Refactors move code under a byte-identical gate (html AND json); features never ride along in the same step.
- Page modules are named for what they render: page_board · page_question · page_stage.
- `src/common.py` stays dependency-free; anything serve.py also needs lives there, never duplicated.

## Lesson
- The byte-identical gate caught a real user-visible bug on its first run (the state pill clobber). A refactor without that gate would have shipped the same bytes and nobody would have looked.

## Log
260802 · A second `## Where we are` heading was silently discarding everything under the first: `split_sections` builds a dict, so the later block won and 1643 bytes of dated records had never rendered. The two are merged and the duplicate heading is gone; `check.py` gained a `duplicate-section` ERROR the same day, because nothing reported this.
260801 0130 · Reindexed QC3 -> QC2b under the new QC2 code-shape parent (JL 260801)
260731 · Browser assets split by topic (27 js + 9 css, none over 365 lines), gated by assets.py verify() which parses the assembled file with node; verified functionally in a real browser (haipipe-board 0.87.0)
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260726 · opening lead widened to three lines (JL: the openings are too short; say the question, how it is answered, and what turns on it)
260725 1615 · dropped the retired "QF1" page id from the src/ rationale; the embed feature it named is unchanged
260724 · settled and shipped in the same body of work as QB3 and QF1
