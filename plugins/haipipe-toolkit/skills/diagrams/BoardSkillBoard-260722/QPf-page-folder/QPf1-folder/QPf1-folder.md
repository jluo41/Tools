# Folder · one page inside one folder it owns
state: ✅ SETTLED
owner: CC
method: recursive discovery in build.py + path vetting in serve.py; ruled by JL 260724, shipped same day
session: 62ed99a0-fe6c-4a9b-8ad7-a3a97425adb2

## Opening
Can a Board page live beside the files it describes without breaking discovery or safe write-back?
Boards were born flat: every page sat at the board root, so a real project tree needed a mirrored page folder kept in step by hand.
Discovery, ordering, and comment write-back all leaned on that flat layout.
The shipped rule replaces it: a `Q*.md` at any depth is a page, its folder is its home, and a flat board behaves exactly as before.

**Covered elsewhere**: `QB1` owns where the Board-Folder itself lives and what it is named. `QB2` owns how the Board-Webpage-Index orders and groups the pages it finds.

**No page wrapper for loose documents**: a folder's own files are shown by embedding them into a real page with `![[path]]` (`ref/board-form.md` §5). The retired ids behind these rules are traced in Log.

## Content
### 1 · The folder shows itself first
**The 📂 tab**: the rail's first surface renders what this page's own folder holds, live on every open.
```text
  🗂 QPf1-folder/                     📂 Folder tab (first on the rail)
  ├── draw/   1 file   ────▶   🖌 draw/    age shown · never flagged
  ├── skill/  2 files  ────▶   ⚙️ skill/   age shown · never flagged
  ├── slide/  1 file   ────▶   🎞 slide/   ⚠️ STALE only when older than the .md
  └── QPf1-folder.md   ← the clock every DERIVED plugin is read against
                                     ⬜ not present: latex · word · bibex · chat …
```

#### 1.1 · What the tab answers
The tab answers what the rail alone cannot: whether "no deck" means never built or built-and-unopened, and whether a compiled artifact still matches the prose it came from.

#### 1.2 · Staleness is claimed narrowly
Only a DERIVED plugin (latex, word, bibex, slide, display) can be ⚠️ STALE, exactly when its newest file predates the page's `.md`.
Source material gets an age, never a warning, because a drawing older than the prose is healthy.

#### 1.3 · Rendered live, never stored
The view is rendered live by `GET /_board/folderstat` and never stored: a status written to disk starts aging the moment it lands, and a stale page about staleness would defeat itself.
Fresh takes both layers: the server sends no-store, and the shell reloads the frame even when the URL has not changed, because a live view has one URL per page and "same src, skip it" is exactly how it would show yesterday's walk.

#### 1.4 · A stale row can cure itself
A ⚠️ STALE row is curable in place when its writer is mechanical: latex, word, bibex, and display rows carry ♻ rebuild, one click firing that plugin's own rebuild and re-rendering the status.
The tab's header carries the same affordance in bulk: 🔄 rebuild stale (n) walks every curable row in sequence and renders only while something mechanical is stale.
Slide points at the 🎞 tab's ✨ instead, because an authored deck must never rebuild as a browsing side effect.

### 2 · A row is a door
**Click to browse**: each plugin row unfolds its own STRUCTURE in place; each file opens as the served file itself.
```text
  ▸ 🔗 pagex/   6 files            click the row …
  ▾ 🔗 pagex/   6 files            … and it unfolds as a TREE:
      QPf11-pagex.md      1KB      the files this folder OWNS come first
      QPf11-pagex-view.html 10KB
      📁 QPs1-overall/   1 file    then one branch per folder under it
          QPs1-overall.md  🔗      a 🔗 marks a symlink, target on hover
```

#### 2.0 · A folder unfolds as a folder
The first build listed the walk's paths flat and alphabetically, so `pagex/` read as six unrelated rows with its own store and view wedged between four borrowed pages (JL 260816: "这个排版不是非常按照我们的思路来排的").
A folder's shape IS the information: files a level owns are listed before the folders under it, each branch carries its own file count so a glance is still worth something, and `display/`, whose units nest three deep, became readable by the same change.
A 🔗 marks a row whose file is a symlink, with the full target on hover, because the row reports the RESOLVED file and a borrowed page md would otherwise read as duplicated bytes (JL 260816: "are they copied or are they the symlink?").

#### 2.1 · The link is the served file
The links are plain served URLs under the board tree, so the browser shows a pdf or an html directly and offers the rest for download; nothing is copied or wrapped.
This keeps the tab honest as both gauge and door: the same walk that measures the folder lists it, so what you click is exactly what was counted.

## Aims
- [x] 📂 §1 The folder shows itself before any surface does
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
- [x] 🚪 §2 The status rows open
      Clicking a plugin row in the 📂 tab unfolds that folder's files in place, each a link to the served file.

## States
§1 Shipped 260724.
Flat boards are untouched; nested pages work end to end including comment write-back (smoke-tested against the MISQ paper's 0-lifecycle board, `4-display/QD2-d01-iv-reporting.md`).
Discovery has since widened to `page_files()` in `src/common.py`: S, Agent, and Meeting pages join Q pages at any depth, same `_`/`.`/`fig/` exclusions.
The original flat-birth rule (a new page always created at the board root) was superseded 260726 (QA1): `add_question` in `live/structure.py` now creates the new page in its group's home folder, falls back to the board root only when the group's pages disagree, and an empty group opens its own `Q<letter>-<slug>` folder.

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
- New questions born from the page are created in the group's home folder; the board root is only the fallback when the group's pages disagree, and an empty group opens its own `Q<letter>-<slug>` folder.

## Log
- 260816 · [RULE-JL] the unfold became a TREE (JL: "我觉得这个 folder 是不是应该加一个 folder structure？… 这个排版不是非常按照我们的思路来排的"). It had listed the walk's relative paths flat and alphabetically, which is a fine way to enumerate files and a poor way to show a folder: `pagex/` read as six unrelated rows with its own store and view wedged between four borrowed pages, and `display/` spelled every unit's inner path on every line. Now a level's own files come first, then one 📁 branch per subfolder carrying its file count, indented by depth. Same round the rows got readable at all: 12px monospace went to 13px on a 1.6 line, sizes take tabular figures so they align, and a symlink wears a bare 🔗 with its target on hover. Proven on `pagex/` and on `display/`, which nests three deep.
- ✍️ 260816 · [REVISE-CC] reviewer pass: Opening, Law, figure, numbering, Log shape
      Worked the reviewer's nine findings; one was contradicted by disk and is noted below.
      The Opening's blank line moved below the rationale, so the question and a rewritten four-sentence rationale stand on stage as one block, without the house-skeleton stems.
      The Covered elsewhere drawer now names the live ids QB1 and QB2 in short labelled parts.
      The genealogy those ids carried moved here: QC1 was absorbed into QB1 and QC2 into QB2 on 260729, and the former QF group's doc-line ruling (QF2 of that era) was retired 260726, its id belonging to Execute's newcomer page today.
      The Law's flat-birth row was rewritten to the current home-folder rule; States and this Log keep the 260726 supersession story.
      The §1 figure was redrawn from the real folder: draw/, skill/, and slide/ exist beside the .md, and nothing else, so the reviewer's claim that bibex/ exists is contradicted by disk and the figure lists latex, word, bibex, and chat as not present.
      §1.4 was also brought up to the 0155 ruling below, which the old prose predated: display sits in the curable set now and slide is the only pointer row.
      The smoke-test line in States names the owning board before the path, the last Aim row lost its attribution parenthetical, Content paragraphs carry #### numbering, and every Log entry below was reshaped into a bulleted heading with its story indented beneath.
- 🖼 260816 0155 · [JL ruled] display's staleness stays and becomes curable
      JL overruled CC's recommendation to unflag display ("I want to add the rebuild button, so that we can have a new list").
      The 🖼 Display view's 🔄 now recompiles every unit's derived preview.tex ▶ preview.pdf before re-rendering (the unit README's own rebuild contract).
      Display joined the folder tab's MECHANICAL set, so its row and the header pill cure it; intake/, recipe/, and the accepted: tick stay untouched, and slide is now the only pointer row.
      Proven on QPf5: both tikz units recompiled and render correctly, row ⚠️→✅.
      Gotcha caught on the way: the view html lives INSIDE display/, so writing it alone had faked freshness; the first "cure" flipped the row while both previews had silently failed on a bare PATH (xelatex lives at /Library/TeX/texbin, export.py's env trick now shared).
- 🔄 260816 0140 · [JL asked, CC shipped] the header pill: rebuild stale (n)
      JL asked for the bulk affordance ("add the button like rebuild like this", pointing at the Word view's 🔄).
      The 📂 tab's header now carries 🔄 rebuild stale (n), the same affordance the Word and LaTeX views wear, walking every curable row in sequence and rendering only while something mechanical is stale.
      Never parallel: the writers share the folder and xelatex is not a thing to race.
      Proven on QPf2: word ⚠️→✅ through the pill's own POST, then the pill removed itself.
- ♻ 260816 0120 · [JL asked, CC shipped] STALE became curable where curing is mechanical
      JL asked "why we have this stale, could we update them along the time?".
      A stale latex/word/bibex row now carries ♻ rebuild, one click firing that plugin's own POST and re-rendering; slide points at the 🎞 tab's ✨ and display at its walk, because authored (claude, minutes, money) and human-gated artifacts must never rebuild as a browsing side effect.
      Verified live on QPf2: latex and bibex went ⚠️→✅ through the same POST the button sends.
      Auto-rebuild-on-edit was considered and refused: a person mid-edit would trigger a compile storm, and the flag would stop meaning anything.
- 🌊 260816 0100 · [JL asked, CC shipped] fresh became a guarantee, not a hope
      JL asked "how to make sure the folder plugin can be refreshed every time?".
      The server's no-store was only half, because the shell skipped landing an UNCHANGED src, and the folder view keeps one URL per page.
      `landFrame` in shell.py now reloads on same-src at both landing sites, so showing the tab, returning to a page, and the lit-click rebuild all refetch; the SKILL records fresh as a two-layer contract (0.1.2).
- 🚪 260816 0020 · [JL asked, CC shipped] the 📂 tab's rows became doors
      JL asked "how could I click them and view the content of these folders?".
      Each row now unfolds its file list in place, every file a served link in a new tab (live/folderstat.py).
      Same session the plugin gained its own skill, `haipipe-plugin-folder`, the tenth of the family and the only one with no subfolder and no roster row, because its material is the folder itself.
      This page also gained the ## Content above (JL: "we should have the content as well"): the design had lived only in Aims ticks and this Log.
- 🏷 260815 1830 · [JL ruled] the plugin skill family keeps the SHORT name
      The umbrella is `haipipe-plugin`, instances are `haipipe-plugin-draw`, `haipipe-plugin-latex`, `haipipe-plugin-word`; `haipipe-page-plugin*` renamed across 51 files, symlinks re-linked.
      CC's ambiguity concern (Claude Code plugins share the word) was heard and overruled: within this toolkit the word is ours.
- 📂 260815 1700 · [JL via CC] the folder's own tab shipped
      📂 Folder registers FIRST on the rail (06-plugin-folder.js), GET /_board/folderstat renders the page-folder's live status (live/folderstat.py), and a DERIVED plugin older than the .md is flagged STALE.
      Rendered live and never stored, because a stale page about staleness would be absurd.
      First run caught a real one: QPf6's latex/ predated its .md.
- ✍️ 260806 2056 · [REVISE-CC] swept to the 260806 architecture
      serve.py's page ops relocated in Files (`target()` to `live/base.py`, `add_question`/`archive_question` to `live/structure.py`) and States now records the 260726 supersession of the flat-birth Law line plus the `page_files()` widening.
- 🏷 260729 · retitled on JL's call; the id stayed
      Retitled to "Page folder management: a page inside its home folder"; the id stayed QB3, because the skill's SKILL.md and `ref/board-form.md` both cite it and so do two other faces; only the title changed.
      The index pointer in `## Boundary` moved from QC2 to QA10, which absorbed it the same day.
- 🧭 260726 · opening lead widened to three lines
      JL: the openings are too short; say the question, how it is answered, and what turns on it.
- 🚢 260724 · settled and shipped
      First consumer is the MISQ paper's 0-lifecycle board.
