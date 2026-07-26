# Folder questions: a Q inside its home folder
state: ✅ SETTLED
owner: CC
method: recursive discovery in build.py + path vetting in serve.py; ruled by JL 260724, shipped same day

## Question
Can a question file live inside the folder it is about, so a board can sit on top of an existing tree instead of mirroring it?
The working answer is yes: discovery walks the whole tree, so a page sits beside what it discusses while `## Pages` keeps bare filenames for order alone.
That unlocks the case which forced the question: a paper's own `0-lifecycle/` becomes a board in place, rather than a second structure kept in step by hand.

The first consumer forced the question: JL wanted the MISQ paper's `0-lifecycle/` itself to be a board, with each stage folder acting as a question's home (the way `5-section-edit/` keeps one folder per unit).
Flat-only discovery made that impossible: `build.py` only globbed the board's top level, and `serve.py` resolved comment write-backs as `board / filename`.

## Boundary
- ✅ Covered here
  Where a page file may physically live: recursive discovery under the board folder, which path segments are excluded, and how comment write-back stays safe once a path rather than a bare filename is in play.
- ↪ Covered elsewhere
  Where the board folder itself belongs and what it is named is `QC1`; how the index orders and groups the pages it finds is `QC2`; showing a folder's own documents without a page wrapper was `QF2`, retired 260726: embed them into a real page with `![[path]]` instead (`ref/board-form.md` §5).

## Diagram

http://127.0.0.1:5599/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/fig/board.excalidraw&frame=QC3

## Items to Finish
- [x] 🔍 Recursive discovery shipped
      `q_files()` in `src/common.py`: `rglob("Q*.md")`, skipping path segments that start with `_` or `.` and `fig/`.
- [x] 💬 Comment plumbing carries the relative path
      The page's data-file attribute holds the board-relative posix path; `vet_qpath()` rejects absolute and `..`.
- [x] 👀 watch.py recursion
      The whole tree is watched with the same segment filter.
- [x] 🧪 Flat regression passed
      The skill's own board rebuilt with an unchanged question set; the script-free invariant held.
- [x] 🎴 First consumer live
      The MISQ `0-lifecycle/` board: 22 questions, pages inside stage folders down to depth 2.

## Where we are
Shipped 260724.
Flat boards are untouched; nested pages work end to end including comment write-back (smoke-tested against `4-display/QD2-d01-iv-reporting.md`).

## Files
- `build.py`
  Thin entry; discovery lives in `src/common.py` + `src/parse.py`.
- `serve.py`
  `target()` / `add_question` / `archive_question` accept board-relative paths.
- `watch.py`
  Recursive stamp with the same exclusions.

## Law
- A question is a `Q*.md` file at ANY depth under the board folder; membership stays by path.
- Path segments starting with `_` or `.` (archives, previews) and `fig/` are not part of the board.
- The Pages keeps listing bare filenames; a duplicate basename anywhere in the tree warns and keeps the first.
- The page carries the board-relative posix path; serve.py vets it (no absolute, no `..`, basename must match `Q*.md`).
- Archiving a nested page flattens it into the board's top-level `_archive/`.
- New questions born from the page are still created flat at the board root.

## Log
260726 · opening lead widened to three lines (JL: the openings are too short; say the question, how it is answered, and what turns on it)
260724 · settled and shipped; first consumer is the MISQ paper's 0-lifecycle board
