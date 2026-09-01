# Folder · one page inside one folder it owns
state: ✅ SETTLED
owner: CC
method: recursive discovery in build.py + path vetting in serve.py; ruled by JL 260724, shipped same day
session: 62ed99a0-fe6c-4a9b-8ad7-a3a97425adb2

## Opening
Can a page sit in the same folder as the files it is about?
At first every page had to sit at the top of the board, so a folder tree needed a second flat copy, kept in step by hand.
The rule now is short: a page file counts as a page however deep it sits, unless a plugin folder holds it.
The folder around a page is its home, and saving from the browser is still safe.
Boards with no folders work just as before.

**Safe saving**: the page sends a path counted from the board, and the server turns it away if it starts at the disk root or steps up with `..`.

**Covered elsewhere**: `QB1` says where the board folder itself sits and what it is called.
`QB2` says how the board's index page sorts and groups the pages it finds.

**Loose files need no page of their own**: pull a folder's files into a real page with `![[path]]` (`ref/board-form.md` §5).
Log tracks the old ids these rules came from.

## Diagram
**The unit folder, two parts (final, JL 260831)**: one grammar for page and task; the root is the code home.
```text
<page or task folder>/
│  ── UPPER · the page part ──
├── <stem>.md         the PRODUCT · Opening · Diagram · Content · Aims
├── outline/          HUMAN process · plan (ticked) · D<nn> · log
├── workflow/         MACHINE process · receipts (task: plan/report.yaml)
├── evidence/         what the page CITES, each lane behind its gate:
│                     bibex verified: · probe read: · display accepted: ·
│                     pagex (links out, task units included) · materials
├── delivery/         what LEAVES the page: latex · word · slide · render
├── studio/           the HUMAN's room: chat/ (talk, sessions kept) ·
│                     draw/ (sketch; the chat may redraw on your ask)
│  ── LOWER · the code part (the root IS the code folder) ──
├── scripts/          any language (.py · .do · …) · config/ inside;
│                     a lane-local script is equally legal
├── runs/             REQUIRED where code exists · THE ONE DOOR
└── results/          REQUIRED where code exists · regenerable · never
                      PHI · never inside evidence/ · becomes evidence
                      only when a probe card binds it (PP<NN>.v<n>)
```
📌 Retired from the page: `meeting/` (→ project/SPACE, parsed into outline/) · `task/` (→ evidence/pagex/) · `logging/` (changes = outline log, executions = runs/) · flat lane names survive only as migration stubs.

## Content
### 1 · You see what your folder holds, and what has gone out of date
**The 📂 tab**: the first tab on the rail shows what this page's own folder holds, read fresh every time you open it.
```text
  🗂 QPf1-folder/                     📂 Folder tab (first on the rail)
  ├── bibex/  0 files  ────▶   📚 bibex/   rebuilt for you · empty · ✅ fresh
  ├── draw/   1 file   ────▶   🖌 draw/    age shown · never flagged
  ├── skill/  2 files  ────▶   ⚙️ skill/   age shown · never flagged
  ├── slide/  1 file   ────▶   🎬 slide/   ⚠️ STALE · ✨ regenerate in the 🎞 tab
  └── QPf1-folder.md   ← the clock every REBUILT folder is checked against
                               ⬜ not present: chat · latex · word · display · meeting
```
📌 The page's own folder is listed right on the page, with a warning on any part that has fallen behind the page.

#### 1.1 · Two things the rail alone cannot tell you
First, whether "no deck" means a deck was never built, or was built and never opened.
Second, whether a built file still matches the words it was made from.
The 📂 tab answers both.

#### 1.2 · Only a folder rebuilt for you can be called out of date
A row reads ⚠️ STALE only if a machine rebuilds that folder: latex, word, bibex, slide, and display.
It also has to hold files, with its newest file older than the page's `.md`.
An empty one is never flagged, so this page's own `bibex/` holds nothing and reads ✅ fresh.
A folder you write yourself shows an age and never a warning.
A drawing older than the words is normal, not a problem.

#### 1.3 · The list is read fresh, never saved
`GET /_board/folderstat` walks the folder each time you open the tab, and it saves nothing.
A saved status starts going out of date the moment it is written, and a stale report about staleness is worse than none.
Two layers keep it fresh.
The server sends `no-store`, and the page shell reloads the panel even when the address has not changed.
That second layer matters, because this view has one address per page, so "same address, skip it" would hand you yesterday's list.

#### 1.4 · One click brings an out-of-date row back
A ⚠️ STALE row can be fixed on the spot when a machine wrote its files.
The latex, word, bibex, and display rows carry ♻ rebuild.
One click runs that folder's own rebuild, then reads the status again.
The tab header does the same for all of them at once: 🔄 rebuild stale (n).
It works through every fixable row one after another, and it shows only while a machine-written row is out of date.
Slide sends you to the 🎞 tab's ✨ instead, because a deck someone wrote must never be rebuilt just from looking around.

### 2 · Click a row and the real files open
**Click to look inside**: a row opens its own folder shape in place, and every file link opens the real file.
```text
  ▸ 📁 pagex/   6 files            click the row …
  ▾ 📁 pagex/   6 files            … and it unfolds as a TREE:
      QPf11-pagex.md               the files this folder OWNS come first
      QPf11-pagex-view.html
      📁 QPs1-overall/   1 file    then one branch per folder under it
          QPs1-overall.md  🔗      a 🔗 marks a symlink, target on hover
```
📌 Every row opens into a tree of real files, and each link takes you to the file itself.

#### 2.1 · The rows show the folder's real shape
The first build listed every path flat and in alphabetical order.
So `pagex/` read as six rows with nothing joining them, its own list file and view file stuck between four borrowed pages (JL 260816: "这个排版不是非常按照我们的思路来排的").
The shape of a folder is the point.
A level's own files come first, then the folders under it.
Each branch shows its own file count, so one look is still worth something.
The same change made `display/` readable, and its parts sit three folders deep.
A 🔗 marks a row whose file is a symlink, and hovering shows the full target.
The row reports the file the link points at, so without the 🔗 a borrowed page would look like a copy (JL 260816: "are they copied or are they the symlink?").

#### 2.2 · What you click is the real file
The links are plain web addresses under the board tree.
The browser shows a pdf or an html page straight away and offers the rest as a download.
Nothing is copied, and nothing is wrapped.
So the tab is both a meter and a door.
The same walk that counts the folder also lists it, so what you click is exactly what was counted.

## Aims
- [x] 📂 §1 The folder shows its own contents before any other tab does
      The first tab on the rail reads this page's folder fresh and says how current each part is.
      A folder rebuilt for you holding files older than the .md is flagged, and the first run caught a real one, QPf6's stale latex/.
- [x] 🔍 A page is found however deep it sits
      `page_files()` in `src/common.py` finds Q, S, Agent, Meeting, and Design pages at any depth.
      It skips `_`, `.` and `fig/` folder names, and every path `_in_plugin()` puts inside a plugin folder.
      `q_files()` is the Q-only twin and skips the same things.
- [x] 💬 A comment saves back to the right file
      The page's data-file attribute holds the path counted from the board.
      Comment and discuss writes send it through `target()`, whose `vet_pagepath()` turns away an absolute path or a `..`.
- [x] 👀 The whole tree is watched
      `watch.py` watches every folder under the board and skips the same folder names.
- [x] 🧪 Old flat boards still work
      This skill's own board rebuilt with the same set of questions, and it still needed no scripts.
- [x] 🎴 The first real board is using it
      The MISQ paper's 0-lifecycle board holds 22 questions, with pages two folders deep inside stage folders.
      That board sits outside this checkout, so the count was read on the machine holding it, on 260724.
- [x] 🚪 §2 A status row opens into real files
      Clicking a row in the 📂 tab opens that folder's files right there, each one a link to the real file.

## Discussion

### From the retired States section (merged 260831)
§1 The 📂 Folder tab sits first on the rail and reads this page's folder on every open, one row per folder beside the `.md`: `bibex/`, `draw/`, `skill/`, `slide/`.
§1 A folder rebuilt for you reads ⚠️ STALE when its files are older than the `.md`, and it carries ♻ rebuild when a machine can redo it.
§1 latex, word, chat, display, and meeting have no folder here, so the tab lists them as not present.
§2 Every plugin row opens in place as a tree: a level's own files first, then one 📁 branch per folder under it with its file count.
§2 Each file is a link to the real file, and each symlink is marked 🔗.
Pages are found by `page_files()` in `src/common.py`: Q, S, Agent, Meeting, and Design pages at any depth.
It skips `_`, `.` and `fig/` folder names, and every path `_in_plugin()` puts inside a plugin folder.
So this page's own `skill/QPf1-folder.md` does not count as a second page.
Flat boards are untouched, and nested pages work all the way through, comment write-back included.
The write-back smoke test was run on 260724 on the MISQ paper's 0-lifecycle board, on the page at 4-display/QD2-d01-iv-reporting.md.
That board is not in this checkout, so neither that test nor the 22-question count can be re-run from here.
The old rule made every new page at the board root, and it was replaced on 260726 (QA1).
`add_question` in `live/structure.py` now writes a new page into its group's home folder.
It falls back to the board root only when the group's pages disagree, and an empty group opens its own `Q<letter>-<slug>` folder, numbered `<N>-Q<letter>-<slug>` when the board already numbers its groups (260816).

## Files
- `cli/build.py`
  A thin entry point. Page finding lives in `src/common.py` and `src/parse.py`.
- `cli/serve.py`
  Routes the write endpoints.
  `target()` now lives in `live/base.py` and checks the payload with `vet_pagepath()`.
  `add_question` and `archive_question` in `live/structure.py` stay on the Q-only `vet_qpath()`.
  Both checks live in `src/common.py`, and both work on paths counted from the board.
- `cli/watch.py`
  Stamps the whole tree, skipping the same folder names.
- `live/folderstat.py`
  Draws the 📂 tab.
  `folder_status()` walks the page folder and gives one row per folder, and the view turns each row into a tree of links.

## Law
- 🔍 A page is a page file at ANY depth, unless a plugin folder holds it
      A page belongs to the board by its path, and the walk is `page_files()` in `src/common.py`.
      It looks for `Q`, `S`, `Agent`, `Meeting`, and `Design` files under the board folder and keeps every name `PAGENAME` matches.
      So a page may sit inside the folder it is about, instead of at the root.
      `q_files()` is the Q-only twin, kept for the routes about questions alone, and it skips the same things.
- 🚫 `_` and `.` names, `fig/`, and every plugin folder sit outside the board
      Archives and previews (`_`, `.`) and `fig/` are skipped by folder name.
      A plugin folder is skipped by `_in_plugin()` in `src/common.py`.
      That function counts every subfolder of a page's home as a plugin, unless the subfolder is a folded page itself.
      It also drops a page file lying right beside the page's own `.md`.
      This page proves it.
      `skill/QPf1-folder.md` matches the page name pattern exactly, yet it shows up inside the ⚙️ skill tab and not as a second page.
- 📇 The Pages listing keeps bare filenames
      A repeated file name anywhere in the tree warns and keeps the first (`src/parse.py`).
      So the file name is a page's identity no matter how deep its folder sits.
      And `board.md` never has to be rewritten when a page moves.
- 🛂 The page sends a path counted from the board, and the server checks it
      `target()` in `live/base.py` runs the payload through `vet_pagepath()`.
      That check turns away an absolute path or any `..`, and it needs the file name to look like a page name.
      `add_question` and `archive_question` in `live/structure.py` still use the Q-only `vet_qpath()`, because those two routes create and retire questions.
- 🗄 Archiving a nested page flattens it
      The file moves to the board's top-level `_archive/` whatever depth it was written at, and a name collision there is resolved with a timestamped stem.
      Archive never deletes: the file stays recoverable by hand.
- 🏠 A new page is born in its group's home folder
      `add_question` reads where the group's pages already live and writes the new file there.
      The board root is only the fallback when the group's pages disagree, and an empty group opens its own `Q<letter>-<slug>` folder.

## Log
- 🚢 260831 · [HAIPIPE-PAGE-SKILL, JL evening round 4] the SWEEP reached its first board: 14 MISQ pages migrated to evidence/+delivery/+studio/ with flat-name stubs (pagex deferred: its borrow symlinks are depth-sensitive until pagex.py adopts the lane resolver); QPf1 finished its own pilot (draw→studio). The shell drawbar RETIRED into the composer's 🖌 menu (__studioDrawIt: composer text = the ask, empty = ## Diagram); evidence records carry the plan's WORDS in their heads (record-shape 0.18.1 — the bare-ref head was the ugly); 📂 rows carry real paths (evidence/bibex/ …) with stubs counted. board 0.156.0.
- 🚢 260831 · [HAIPIPE-PAGE-SKILL, JL evening round 2] the chat pane took the Claude Code COMPOSER shape (one rounded card: textarea + row ＋ new chat · 🗂 ✨ ⚙ as POPUP menus, closed by default, reversing the 260815 "list first" boot · 🖌 draw fold remote · ➤ send; plugin-chat 0.4.0); GUI text 14/15px → 12.5/13px (the narrow docked pane was living in the MOBILE media query — the real "too big"); the studio draw half FOLDS (⌄/⌃ + composer 🖌, per reader; plugin-studio 0.1.1); 🗂 Task and 🗣 Meeting menu rows REMOVED (JL; storage stays, task read owed to pagex); 📂 Folder speaks the two-part grammar (category chips + grammar gaps line + pre-migration flat-lane callout, plugin-folder 0.2.1). All Chrome-verified on SM05/SM00; board 0.155.0. The page-folder DISK migration itself is still the sweep.
- 🚢 260831 · [HAIPIPE-PAGE-SKILL, JL: "put both of them into the studio, as one page" + "one plugin for evidence, one for the delivery, only one for the studio"] the strip went FIVE-plus-mirror final: 🧭 🧾 📤 🎨 (⚙️ pending) 📂. NEW 🎨 Studio tab (haipipe-plugin-studio 0.1.0, shell tab id studio): the drawing above with its ✨ bar, the chat below with GUI/TUI, both live, so the scene the chat redraws changes in front of the person; the 💬 🖌 🎞 rows folded, stored tab sets migrate on load; the deck's ✨ pen moved into the 📤 Slides segment. The 260815 "no chat under the canvas" refusal stays true of the draw LANE. Chrome-verified on SM05-results (strip, split geometry, ✨ bar). haipipe-board 0.154.0 · haipipe-plugin 0.3.0.
- 🚢 260831 · [HAIPIPE-PAGE-SKILL, JL: "how do we design the plugin... to represent the above?"] the categories got their PRESENTERS: haipipe-plugin §🔌 splits plugins into LANE (owns one rostered folder's law) and PRESENTER (one surface over a category, no row) — 🧾 Evidence over evidence/, NEW 📤 Delivery over delivery/ (live/delivery.py: 🏠 stat · 📜📝 built on click · 🎞 read-only · 📱 ghost; the separate LaTeX/Word strip rows folded, native 🎞 stays as a tool), ⚙️ code contract-only until the first real runs/. Driven in real Chrome on SM05-results: menu → 📤 tab → LaTeX segment compiled the pdf on click; the drive also caught savedUrl breaking on the shell's board.md path (fixed in delivery+evidence). haipipe-board 0.153.0 · haipipe-plugin 0.2.0.
- 🗺 260831 · [HAIPIPE-PAGE-SKILL, JL: "this is great, please map it down"] the FINAL two-part unit grammar mapped into this page's Diagram: three upper categories (evidence · delivery · studio) + the root-as-code lower part (scripts · runs · results), the gate line, the stub rule, the retirements. Law home: haipipe-page 0.50.0 §📁 + the roster; pilot QPf1 itself.
- 🚢 260831 · [HAIPIPE-PAGE-SKILL, JL ruled] THIS page became the first CATEGORY folder pilot: bibex/probe/display moved under evidence/, latex/word/slide under delivery/, flat names kept as symlink stubs so every unpatched engine path still resolves (bibex saved view 200 via stub, 🧾 tab 200, roster scan silent). Roster gained evidence/ · delivery/ · runs/ rows; meeting leaves the page, task merges into pagex, logging retired. De-symlink debt: ~60 engine sites move to a lane resolver file by file, then the stubs go.
- 🚢 260831 · [HAIPIPE-PAGE-SKILL, JL ruled] a plugin IS a lane and a SKILL.md is EARNED BY LAW: the roster row is the record; retire/merge candidates tiered (value+folder now, latex+word+slide → one export later). A `code/` lane is agreed: the unit's own SIMPLE scripts with their run records INSIDE the code lane (runs folded into code, JL's call), `logging/` row retires into it; not yet minted.
- 🔎 260816 · [REVISE-CC] third reviewer pass: §2 numbering, the MISQ path, and the bibex proof
      Six findings arrived, three of them already cured by the tree rewrite that landed in between, and the three live ones were all about evidence a second person cannot check.
      Named so nobody reopens them: the §2 figure gives both folder rows 📁 and keeps 🔗 on the file line, it carries no size column at all so the wrong 10KB for `QPf11-pagex-view.html` is gone with it, and the §1 slide row already shows a state instead of the condition behind it.
      §2's paragraphs ran 2.0 then 2.1, and an ungrouped part numbers from .1, so they read 2.1 and 2.2 now.
      0-lifecycle/ is a Link declared in `board.md` that points six folders up into a SPACE this checkout does not hold, and a declared Link is turned into an href without any check that the file is there, so the Aim's backticked copy rendered as a link to nothing and earned this page its one outside-checkout warning.
      The Aim and its State now write that board and the smoke-test page as plain words the build cannot link, and both say the evidence was read on 260724 on the machine holding it and cannot be re-run here.
      The bibex entry below proved its point by quoting one reader's error strings, which nobody else can reproduce; it now states what anyone can look at, that `bibex/` sits beside the `.md` holding 0 files and that `folder_status()` emits one row per directory beside it.
- 📖 260816 · [REVISE-CC, JL ruled] the page was rewritten in plain words, for a reader with ADHD whose English is a second language (JL: "我真的读不下去"). The 🧭 Outline tab had been showing this page's own sentences back, and they were unreadable, so the tab was right and the prose was not. Every division title now names its consequence instead of a mechanism, each one gained a `📌` line saying in one sentence what the part settles, and every aim, `Done when:` and State row was replaced with a short plain-word version. House words went with them, `division` to part, `store` to list, `render` to read or draw, `seed` to suggest, `mint` to build. Measured with `haipipe-writing`'s `cli/score.py`: 36 sentences flagged before, 20 after, every one that remains inside this Log, which is history and was not touched. No fact, id, `§` mark or section changed; only the words.
- ✍️ 260816 · [REVISE-CC] second reviewer pass: the bibex row, discovery's real boundary, and the Law shape
      Ten findings worked, and the first of them was a dismissal this page had written down as fact.
      The previous pass claimed disk contradicted the reviewer's `bibex/` row and dropped it from the §1 figure.
      Disk says otherwise, and here is the fact anyone can check: `bibex/` sits beside this page's `.md` and holds 0 files, while `latex/` is not there at all.
      `folder_status()` in `live/folderstat.py` emits one row for every directory beside the `.md`, so the real tab shows four rows: bibex, draw, skill, slide.
      The row reads ✅ fresh rather than ⚠️ STALE because the stale test also requires `bool(files)`, so an empty derived folder is never flagged; §1.2 now says that, and the figure's slide row wears the tab's own 🎬 instead of the Slides rail's 🎞.
      The not-present line was rebuilt from the code's own gap list and now reads chat · latex · word · display · meeting.
      Discovery was restated everywhere it appeared: Opening, Law, Aims, and States now name `page_files()` and the `_in_plugin()` skip, and this page's own `skill/QPf1-folder.md` is the example of a page-named file that discovery refuses.
      States gained one §1 row for the Folder tab and one §2 row for the unfolding rows, and the old `§1 Shipped 260724` tag went with the mistake it carried: 260724 was nested discovery, and the tab shipped 260815.
      Law rows became icon headings with their sentences indented beneath, the shape Log already had, and the vetting row was corrected to `vet_pagepath()`, which is what `target()` in `live/base.py` actually calls.
      The Opening now says what makes a write safe, and both drawer parts sit one sentence per line.
      Three siblings of the named findings were swept with them: the comment-plumbing Aim still credited `vet_qpath()` for a path that `target()` vets, the §1 figure's slide row still said STALE means older than the .md, and the RULE-JL entry below was still one long line while the rest of Log had been reshaped.
- 🌲 260816 · [RULE-JL] the unfold became a TREE
      JL: "我觉得这个 folder 是不是应该加一个 folder structure？… 这个排版不是非常按照我们的思路来排的".
      It had listed the walk's relative paths flat and alphabetically, which is a fine way to enumerate files and a poor way to show a folder: `pagex/` read as six unrelated rows with its own store and view wedged between four borrowed pages, and `display/` spelled every unit's inner path on every line.
      Now a level's own files come first, then one 📁 branch per subfolder carrying its file count, indented by depth.
      Same round the rows got readable at all: 12px monospace went to 13px on a 1.6 line, sizes take tabular figures so they align, and a symlink wears a bare 🔗 with its target on hover.
      Proven on `pagex/` and on `display/`, which nests three deep.
- ✍️ 260816 · [REVISE-CC] reviewer pass: Opening, Law, figure, numbering, Log shape
      Worked the reviewer's nine findings; the one dismissed here was in fact correct, and the entry above records the correction.
      The Opening's blank line moved below the rationale, so the question and a rewritten four-sentence rationale stand on stage as one block, without the house-skeleton stems.
      The Covered elsewhere drawer now names the live ids QB1 and QB2 in short labelled parts.
      The genealogy those ids carried moved here: QC1 was absorbed into QB1 and QC2 into QB2 on 260729, and the former QF group's doc-line ruling (QF2 of that era) was retired 260726, its id belonging to Execute's newcomer page today.
      The Law's flat-birth row was rewritten to the current home-folder rule; States and this Log keep the 260726 supersession story.
      The §1 figure was redrawn from the real folder, but that redraw missed the empty `bibex/` and this entry dismissed the reviewer's row on the strength of it.
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

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0