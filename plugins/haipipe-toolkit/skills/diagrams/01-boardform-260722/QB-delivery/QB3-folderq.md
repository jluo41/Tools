# Page · its home folder: one page inside one folder it owns
state: ✅ SETTLED
owner: CC
method: recursive discovery in build.py + path vetting in serve.py; ruled by JL 260724, shipped same day
session: 62ed99a0-fe6c-4a9b-8ad7-a3a97425adb2

## Opening
Can a Board page live beside the files it describes without breaking discovery or safe write-back?

This page lets an existing project tree serve directly as a Board instead of requiring a mirrored page folder.
The hard part is that discovery, ordering, and server writes originally assumed every page lived at the Board root.
That flat-only rule forces lifecycle trees to be copied and kept in step by hand.
The design succeeds when a nested page is discovered, ordered, and edited safely while flat Boards behave exactly as before.

**Covered elsewhere**: Where the Board-Folder itself belongs and what it is named is `QB1` (which absorbed QC1 on 260729); how the Board-Webpage-Index orders and groups the pages it finds is `QB2` (which absorbed QC2 as QB2 on 260729); showing a folder's own documents without a page wrapper was the former QF group's doc-line ruling (QF2 of that era, retired 260726; the id belongs to Execute's newcomer page today): embed them into a real page with `![[path]]` instead (`ref/board-form.md` §5).


## Diagram

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QB3

## Aims
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

## States
Shipped 260724.
Flat boards are untouched; nested pages work end to end including comment write-back (smoke-tested against `4-display/QD2-d01-iv-reporting.md`).
Discovery has since widened to `page_files()` in `src/common.py`: S, Agent, and Meeting pages join Q pages at any depth, same `_`/`.`/`fig/` exclusions.
The flat-birth rule below in Law was superseded 260726 (QA1): `add_question` in `live/structure.py` now creates the new page in its group's home folder, falls back to the board root only when the group's pages disagree, and an empty group opens its own `Q<letter>-<slug>` folder.

## Files
- `cli/build.py`
  Thin entry; discovery lives in `src/common.py` + `src/parse.py`.
- `cli/serve.py`
  Routes the write endpoints; `target()` now lives in `live/base.py` and `add_question` / `archive_question` in `live/structure.py`, all on board-relative paths (`vet_qpath()` in `src/common.py`).
- `cli/watch.py`
  Recursive stamp with the same exclusions.

## Law
- A question is a `Q*.md` file at ANY depth under the board folder; membership stays by path.
- Path segments starting with `_` or `.` (archives, previews) and `fig/` are not part of the board.
- The Pages keeps listing bare filenames; a duplicate basename anywhere in the tree warns and keeps the first.
- The page carries the board-relative posix path; serve.py vets it (no absolute, no `..`, basename must match `Q*.md`).
- Archiving a nested page flattens it into the board's top-level `_archive/`.
- New questions born from the page are still created flat at the board root.

## Log
- 260806 2056 · [REVISE-CC] swept to the 260806 architecture; serve.py's page ops relocated in Files (`target()` to `live/base.py`, `add_question`/`archive_question` to `live/structure.py`) and States now records the 260726 supersession of the flat-birth Law line plus the `page_files()` widening
260729 · Retitled to "Page folder management: a page inside its home folder" on JL's call. The id stays QB3, because the skill's SKILL.md and `ref/board-form.md` both cite it and so do two other faces; only the title changed. The index pointer in `## Boundary` moved from QC2 to QA10, which absorbed it the same day
260726 · opening lead widened to three lines (JL: the openings are too short; say the question, how it is answered, and what turns on it)
260724 · settled and shipped; first consumer is the MISQ paper's 0-lifecycle board
