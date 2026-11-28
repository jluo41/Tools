# A01 · State shows by marks and layout, never by words or tallies

> "we don't want this, drop them"; "just like the layout and UI tell it" (JL 261113)

## 1. Need
JL reads a page by its marks and layout. A sentence that says what state a thing is in, or a count of how far
the work got, costs him a read and goes stale.

## 2. Now
AGENTS.md § Page words states the rule, and a memory holds it, but nothing checks a served page. A scan of every
running workbench (261118, `page_words.py --running --max 30`, 300 pages) still found "Status : Planning phase"
on a Project page and "status: ready" in a Paper delivery line.

## 3. Gap
- The rule lived in prose (AGENTS.md); page code is written by many sessions that never re-read it.
- No check read what a page SHOWS, so text coming from a face (a Project's own "Status:" line) passed.

## 4. Methods
1. Unit tests per module: fast, but each new module needs its own, and face text never passes through them.
2. A scanner over what every running server serves: catches any source (code, face, template); chosen.
3. A linter over Python strings: misses rendered face text and flags harmless code; rejected.

## 5. Update
- `hai-ui/scripts/page_words.py`: visible-text scan, every running server
- `hai-ui/CONSTITUTION.md`: this article, Run line is the scan
- `AGENTS.md` (root): read the owner's CONSTITUTION.md before changing a page
Cases: ✅ section bars · ⬜ Proj13 Project face · ⬜ Paper delivery line · ⬜ every other running page.

## 6. Never again
- The reader of record: `/hai-stack sweep` runs the scan over every running server; a new "Status:" anywhere
  turns this article ❗.
- The writer: AGENTS.md sends every session to this file before it changes a page.
- Still open: a face a person wrote may hold a "Status:" line on purpose; triage decides whether the page
  should render that line as a mark instead.
