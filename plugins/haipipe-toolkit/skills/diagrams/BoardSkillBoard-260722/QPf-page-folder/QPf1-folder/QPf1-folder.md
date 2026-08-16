# Folder · one page inside one folder it owns
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


## Content
### 1 · The folder shows itself first
**The 📂 tab**: the rail's first surface renders what the page-folder actually holds, live on every open.
```text
  🗂 <page>/                          📂 Folder tab (first on the rail)
  ├── draw/   1 file · 3KB   ────▶   🖌 draw/   8h ago   source material
  ├── skill/  2 files · 5KB  ────▶   ⚙️ skill/  7m ago   source material
  ├── latex/  compiled pdf   ────▶   📜 latex/  2d ago   ⚠️ STALE
  └── QPf1-folder.md  ← the clock every DERIVED plugin is read against
                                     ⬜ not present: slide · chat · word …
```
The tab answers what the rail alone cannot: whether "no deck" means never built or built-and-unopened, and whether a compiled artifact still matches the prose it came from.
Staleness is claimed narrowly: only a DERIVED plugin (latex, word, bibex, slide, display) can be ⚠️ STALE, exactly when its newest file predates the page's `.md`; source material gets an age, never a warning, because a drawing older than the prose is healthy.
The view is rendered live by `GET /_board/folderstat` and never stored: a status written to disk starts aging the moment it lands, and a stale page about staleness would defeat itself.
Fresh takes both layers: the server sends no-store, and the shell reloads the frame even when the URL has not changed, because a live view has one URL per page and "same src, skip it" is exactly how it would show yesterday's walk.
A ⚠️ STALE row is also curable in place when its writer is mechanical: latex, word, and bibex rows carry ♻ rebuild, one click firing that plugin's own POST and re-rendering the status; slide and display rows point to their own doors instead, because a compile may be a button reflex and an authored or human-gated artifact never is.

### 2 · A row is a door
**Click to browse**: each plugin row unfolds its files in place; each file opens as the served file itself.
```text
  ▸ 🖌 draw/   1 file · 3KB          click the row …
  ▾ 🖌 draw/   1 file · 3KB          … and it unfolds:
      QPf1.excalidraw   3KB · 8h ago   ← a link, opens in a new tab
```
The links are plain served URLs under the board tree, so the browser shows a pdf or an html directly and offers the rest for download; nothing is copied or wrapped.
This keeps the tab honest as both gauge and door: the same walk that measures the folder lists it, so what you click is exactly what was counted.

## Aims
- [x] 📂 The folder shows itself before any surface does
      The rail's first tab renders the page-folder's live contents with per-plugin freshness; a derived plugin older than the .md is flagged, and the first run caught QPf6's stale latex/ for real.
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
- [x] 🚪 The status rows open
      Clicking a plugin row in the 📂 tab unfolds that folder's files in place, each a link to the served file (JL 260816).

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
- 260816 0120 · [JL asked, CC shipped] STALE became curable where curing is mechanical ("why we have this stale, could we update them along the time?"): a stale latex/word/bibex row now carries ♻ rebuild, one click firing that plugin's own POST and re-rendering; slide points at the 🎞 tab's ✨ and display at its walk, because authored (claude, minutes, money) and human-gated artifacts must never rebuild as a browsing side effect. Verified live on QPf2: latex and bibex went ⚠️→✅ through the same POST the button sends. Auto-rebuild-on-edit was considered and refused: a person mid-edit would trigger a compile storm, and the flag would stop meaning anything.
- 260816 0100 · [JL asked, CC shipped] fresh became a guarantee, not a hope ("how to make sure the folder plugin can be refreshed every time?"): the server's no-store was only half, because the shell skipped landing an UNCHANGED src, and the folder view keeps one URL per page. `landFrame` in shell.py now reloads on same-src at both landing sites, so showing the tab, returning to a page, and the lit-click rebuild all refetch; the SKILL records fresh as a two-layer contract (0.1.2).
- 260816 0020 · [JL asked, CC shipped] the 📂 tab's rows became doors ("how could I click them and view the content of these folders?"): each row now unfolds its file list in place, every file a served link in a new tab (live/folderstat.py). Same session the plugin gained its own skill, `haipipe-plugin-folder`, the tenth of the family and the only one with no subfolder and no roster row, because its material is the folder itself. This page also gained the ## Content above (JL: "we should have the content as well"): the design had lived only in Aims ticks and this Log.
- 260815 1830 · [JL ruled] the plugin skill family's name is the SHORT form: the umbrella is `haipipe-plugin`, instances are `haipipe-plugin-draw`, `haipipe-plugin-latex`, `haipipe-plugin-word`; `haipipe-page-plugin*` renamed across 51 files, symlinks re-linked. CC's ambiguity concern (Claude Code plugins share the word) was heard and overruled: within this toolkit the word is ours.
- 260815 1700 · [JL via CC] the folder's own tab shipped: 📂 Folder registers FIRST on the rail (06-plugin-folder.js), GET /_board/folderstat renders the page-folder's live status (live/folderstat.py), and a DERIVED plugin older than the .md is flagged STALE. Rendered live and never stored, because a stale page about staleness would be absurd. First run caught a real one: QPf6's latex/ predated its .md.
- 260806 2056 · [REVISE-CC] swept to the 260806 architecture; serve.py's page ops relocated in Files (`target()` to `live/base.py`, `add_question`/`archive_question` to `live/structure.py`) and States now records the 260726 supersession of the flat-birth Law line plus the `page_files()` widening
260729 · Retitled to "Page folder management: a page inside its home folder" on JL's call. The id stays QB3, because the skill's SKILL.md and `ref/board-form.md` both cite it and so do two other faces; only the title changed. The index pointer in `## Boundary` moved from QC2 to QA10, which absorbed it the same day
260726 · opening lead widened to three lines (JL: the openings are too short; say the question, how it is answered, and what turns on it)
260724 · settled and shipped; first consumer is the MISQ paper's 0-lifecycle board
