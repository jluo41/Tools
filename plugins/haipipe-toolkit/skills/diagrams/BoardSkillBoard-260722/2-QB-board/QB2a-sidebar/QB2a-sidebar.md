# Board · the sidebar: jump anywhere from a fixed panel down the left
state: 🟡 PARTIAL · the page list and the per-page section outline ship; the outline's reach forks await JL
owner: JL
method: render the page list from the same listing as the index and the same Structure rows as the Opening drawer, so the page list can never disagree with the page
session: 552d0d85-7735-417b-b3a7-50bbc8f67677

## Opening
How can one left page list take a reader to any page, and to any section inside it, without ever drifting from what the page holds?
The page list is the strip down the left side of every board page.
Under the open page it also lists that page's own sections, such as `📚 Content` and each part under it.
Drift would be a row pointing at a part somebody deleted this morning.
So no row is typed by hand: the build works each one out from the page itself.

**What a page list row is**: A page row is three things: its state emoji, its id, and its title, like `🟡 QB4 the shared layout`.
Above the pages sit the groups, and above them the board's own Index.
Only the page you have open unfolds; every other page stays one row.

**Where this page sits**: `QB2` owns the Index, which is the page you land on when you open the board.
`QB4` owns what a single page is made of, section by section.
This page owns the strip that stays on screen for both of them, so it has to agree with each without being told about either.

**What the page list buys the rest of the board**: `QB4` ruled that every section of every page starts shut.
That is only readable because the page list already shows the page's parts, so a reader sees the whole shape without opening anything.
Take the page list away and a start-shut page shows almost nothing.

**What a hand-kept page list would cost**: A page list written by hand is a second copy of the board.
It is right the day it is written and wrong the first time somebody adds a part, and nothing tells you which of the two to believe.

## Diagram

**The page list on screen**: what the page list shows for the page you have open, and what it shows for every other page.

```
┌ ☰  the page list · fixed to the left of every page ──────────────┐
│ 🗂 Index                                          #top      │
│ 🏛 QA · Design                               #group-QA      │
│     🟡 QA0   three folders                        ▸ shut    │
│ 🏛 QB · Delivery                             #group-QB      │
│     🟡 QB2   webpage design                       ▸ shut    │
│     🟡 QB2a  the page list                          ▾ OPEN    │
│         🧭 Opening        the lead, and this drawer         │
│         🖼 Diagram        1 figure · no canvas              │
│         📚 Content        3 divisions                       │
│            1 · Three altitudes, one page list                    │
│            2 · The section outline, for the open page only  │
│            3 · Derived, never registered                    │
│         🎯 Aims           4 met · 2 waiting · 1 not started │
│         📍 States         the present state                 │
│         📎 Files          5 files                           │
│     🟡 QB4   the shared layout                    ▸ shut    │
└─────────────────────────────────────────────────────────────┘

🖱 row click      go to that page · click again ──▶ back to its top
🖱 ▸ click        unfold this page's sections · turns ▾ while open
🖱 outline row    open that section ──▶ scroll it to the top
🪗 accordion      at most ONE page's outline open, ever
↔️ drag the edge  150px ─── 60% of the window · remembered per machine
☰ toggle          open on a wide screen · hidden on a narrow one
```

## Content
### 1 · Three altitudes, one page list
**One list, three altitudes**: what the page list lists, and where each kind of row comes from.

```
🗂 BOARD              Index                    the board's own page
   │
   ├─ 🏛 GROUP        QA · QB · QC · QD …      one row per group
   │      │
   │      └─ 📄 PAGE  🟡 QB2a  the page list     state · id · title

📋 source        `## Pages` in board.md, in that exact order
⚙️ renderer      `page_board.py`, the loop that also draws the Index rows
🚫 JavaScript    not needed · the rows are in the HTML file
📍 placement     outside `.wrap`, where `:target` cannot hide it
🖱 ☰ toggle      one saved choice per board, in localStorage
```
🗂 One list at three altitudes, drawn from the same source as the Index, so the two can never list different pages.

#### 1.1 · The page list lists the board, its groups, and its pages
(three altitudes in one list, in the order `## Pages` gives them)
The page list shows the board as `🗂 Index`, then the groups, then the pages.
A page row is its state emoji, its id, and its title.
The order is `## Pages` order, so the page list and the Index read the same top to bottom.

#### 1.2 · It is drawn on the server, by the loop that draws the Index
(one loop, so a page can never be in one list and missing from the other)
`page_board.py` renders the page list from the same listing it renders the Index rows from.
Two things follow from that.
The page list works with JavaScript switched off, because the rows are already in the HTML file.
And it can never list a page the Index does not, because there is nothing to keep in step: there is one list.

#### 1.3 · It sits outside the part of the page that shows and hides
(so it stays up whether you are looking at the Index or at a page)
The board hides and shows pages with the `:target` rule, and everything it governs lives inside `.wrap`.
The page list sits outside `.wrap`, so those rules never touch it.
It is therefore on screen in the Index view and on an open page alike.
A group link re-targets `#group-…`, which brings the Index back on stage under the same page list.

#### 1.4 · The ☰ toggle remembers what you chose
(per board, so one board being open does not decide the next one)
The choice is kept in localStorage, one entry per board.
With no saved choice the page list opens on a wide screen and hides on a narrow one.
On a narrow screen it overlays the text instead of pushing it, and a jump closes it again.

#### 1.5 · The page list's width is one CSS variable, and the body reads it too
(drag the edge and the text moves with it, instead of being covered by it)
The width lives in `--sbw`, the same shape the chat drawer uses for `--chatw`.
The handle sets that variable, the body's `padding-left` reads it, and the browser remembers it per machine.
The range is 150px to 60% of the window, and a double click on the handle drops the override.
The handle is a fixed strip OUTSIDE the page list, because the page list is `overflow-y:auto` and clips anything sitting on its own edge.

### 2 · The section outline, for the open page only
**One page unfolded**: what the open page's row expands into, and what the two controls on it do.

```
📄 QB2a  the page list                           ◀ the page you have open
    │                                            ▸ ── the hidden chevron
    ├── 🧭 Opening        the lead, and this drawer
    ├── 🖼 Diagram        1 figure · no canvas
    ├── 📚 Content        3 divisions
    │      └── 1 · 2 · 3        one row per part
    ├── 🎯 Aims           4 met · 2 waiting · 1 not started
    │      └── A1 · A2 · A3     one row per group, with its own count
    ├── 📍 States         the present state
    │      └── Decision Now · 3 to tick
    └── 📎 Files          5 files

📄 QB4   the shared layout                     ◀ every other page: one row

🖱 the ROW        navigate · re-click ──▶ the top of the page
🖱 the ▸          unfold or fold this page's sections · ▾ while open
🪗 accordion      opening one outline shuts every other one
🔁 fresh arrival  the open page starts unfolded
🧩 source         `structure_rows()`, shared with the Opening drawer
```
🧭 The open page's own sections, one indented row each, with the two controls that reach them.

#### 2.1 · The open page's row unfolds into that page's sections
(the same rows the Opening drawer's Structure map shows, plus the parts under them)
Under the open page the page list lists that page's sections: the section emoji, its name, and its computed meta.
`📚 Content · 3 divisions` and `📎 Files · 5 files` are two of those rows.
Below a section come its own parts: one row per Content part, and one row per `###` subsection of States.
A `Decision Now` row also says how many ticks it still owes.

#### 2.2 · The accordion is a rule, not an option
(fifty-three pages of open outlines is not a map, it is the whole board again)
Navigating collapses every other page's outline, so exactly one page's sections show at a time.
That was ruled the same day the outline shipped, and it is what keeps the page list a map rather than a second copy of the board.

#### 2.3 · The row and the chevron are two different controls
(one takes you to the page, the other opens the page's sections in place)
Clicking a page row goes to that page, and clicking it again returns to the TOP of that page.
The `▸` at the row's right end is hidden until you are near it; it folds and unfolds the section outline without leaving the page, and turns into `▾` while open.
This replaced an earlier version where the row itself was the toggle, which meant you could not go to a page and open its outline as two separate acts.

#### 2.4 · An outline row opens the section and scrolls to it
(a jump is a request that survives the page being replaced under it)
Clicking an outline row goes to the page if you are not on it, opens the target `<details>`, and brings it to the top of the viewport.
A Content part row opens Content first, then the part inside it.
The request is parked in `sessionStorage` and honoured by whichever document ends up holding the page, then cleared, so it can never fire twice.
It is honoured by the ARRIVAL and never by the click, because a click honoured too early acts on the document that is about to be thrown away.

#### 2.5 · The drawer and the page list read one function
(two views of one page's structure, so they cannot describe it differently)
The section rows come from `structure_rows()` in `page_question.py`.
It was pulled out of the Opening drawer's own renderer so the drawer and the page list read one source.
There is no second place where a section's name or its count is worked out, so there is no second place for one of them to be wrong.

### 3 · Derived, never registered
**Where every row comes from**: each kind of row, and the file it is computed from.

```
📝 board.md `## Pages`  ━━▶  📄 page rows        id · state · title
📄 the parsed page      ━━▶  🧭 🖼 📚 🎯 📍 📎   section rows
🧩 structure_rows()     ━━▶  🔢 the meta         3 divisions · 5 files
🗂 Content headings     ━━▶  ↳ part rows         1 · 2 · 3

✍️ authored page list rows    ZERO · there is no registry file to edit
🧮 build time            every row · recomputed on every build
🚫 the drift it removes  a row for a part that was deleted this morning

🔒 what leans on this ─── QB4: every section of every page starts SHUT
                          the reader still sees the page's parts, in here
```
🌱 The page list adds no authored surface at all, and that is what the rest of the board's start-shut default rests on.

#### 3.1 · Nothing in the page list is authored
(pages, sections, and counts are all read back out of files somebody already wrote)
Pages come from `## Pages` in `board.md`.
Sections come from parsing the page itself.
The counts come from the same regexes the Opening drawer uses.
There is no file anywhere that lists a page list row, which means there is nothing to forget to update.

#### 3.2 · A hand-kept outline would drift the day a part is added
(this is the Board Map's honesty argument, applied one level down)
A registry is right on the day it is written.
The first person to add a Content part makes it wrong, and nothing reports it, because a stale row looks exactly like a live one.
So the outline is computed or it is not there at all.

#### 3.3 · The start-shut default leans on this page list
(QB4 could only shut every section because the parts stayed visible somewhere)
`QB4` ruled that every section and every Content part starts shut.
The earlier rule was the opposite, and its reason was that a reader who never clicks must still be able to read straight down.
That held while a page had no page list beside it.
It stopped holding once the page list carried the page's parts, because the parts are still on screen even with every section shut.
The one case where this costs a click is a narrow screen, where the page list hides itself and has to be opened first.

## Aims
### Decision Now
- [ ] 🗣 Does the outline reach the `###` subsections of States?
      📍 `Part` `### 2 · The section outline, for the open page only`
      🔔 `Why now` JL 260731: "ok, also unfold the Decision Now in the page list, go ahead". It shipped in 0.67.0 the same round, and the row has been open since.
      ⭐ `A ·` keep it. Every `###` subsection of States is a jump row, found by its heading text, and a `Decision Now` row shows how many ticks it owes. It is what is live today.
      `B ·` cut it back to sections only. The page list gets shorter on a page with many subsections, and a reader loses the one row that says a decision is waiting.
      🛑 `Blocks` A2.2 in States, which stays 🧠 until this is answered.
      🤖 `If nobody answers` A stays, because it is what already ships; the row is a confirmation, not a build.

- [ ] 🗣 Does the `🗂 Index` row keep its own outline?
      📍 `Part` `### 1 · Three altitudes, one page list`
      🔔 `Why now` JL 260731: "what should be the index's section content? Please add them as well". Shipped in 0.78.0 as four present-only rows: 🗺 Board Map, 🩺 Section Matrix, 📄 All Pages, 📈 Activity.
      ⭐ `A ·` keep the four rows. Topic, Pipeline and Board-Structure are deliberately not rows, because JL removed them from the Index in the same round (`QB2`).
      `B ·` drop the Index outline. The Index is one screen and can be scrolled, so the rows save little.
      🛑 `Blocks` A1.2 in States, which stays 🧠 until this is answered.
      🤖 `If nobody answers` A stays, because it is what already ships.

- [ ] 🗣 Does this page own the page list, with `QB2` keeping the Index?
      📍 `Part` the whole page
      🔔 `Why now` This face was carved out of `QB2` on 260731, after the page list had already shipped under it. Both pages describe the same screen and the split has never been confirmed.
      ⭐ `A ·` `QB2` keeps the webpage and the Index design, and this face keeps the page list and its outline. It is how both pages are written today.
      `B ·` fold this page back into `QB2`. One page then carries the Index and the page list together, and `QB2a` is retired.
      🛑 `Blocks` nothing; both pages render either way.
      🤖 `If nobody answers` A stays, and this page goes on being the page list's home.


### A1 · 🗂 Three altitudes, one page list
- ✅ A1.1 · The page list lists exactly the pages the Index lists, and it is there with JavaScript switched off.
  **Done when:** `page_board.py` renders the page list from the same listing as the Index rows, and a page absent from `## Pages` is absent from both.
  **Now:** Shipped in haipipe-board 0.61.0: fixed left page list, ☰ toggle, per-board persistence, active row highlight, hidden in print. It became drag-resizable in 0.85.0.
- 🧠 A1.2 · The `🗂 Index` row unfolds into the components the Index really renders.
  **Done when:** the Index row carries the chevron and lists only components present on the Index, each scrolling to it.
  **Now:** Shipped in 0.78.0 with four present-only component rows. Waiting on the confirming tick in the Decision Now row above.


### A2 · 🧭 The section outline, for the open page only
- ✅ A2.1 · The open page shows its own sections in the page list, and no other page shows any.
  **Done when:** exactly one `.sb-out` is visible at a time, and clicking a row opens the target section and brings it to the top of the viewport.
  **Now:** Shipped in haipipe-board 0.66.0: Structure rows plus Content parts under the open page only, accordion enforced. The click path was repaired on 260801 and verified from four starting points.
- 🧠 A2.2 · The outline reaches every part of a page a reader would want to jump to.
  **Done when:** Content parts and every `###` subsection of States are rows, and a `Decision Now` row states how many ticks it owes.
  **Now:** Shipped in 0.67.0. Waiting on the confirming tick in the Decision Now row above.


### A3 · 🌱 Derived, never registered
- ✅ A3.1 · No row in the page list is authored anywhere.
  **Done when:** pages come from `## Pages`, sections from the parsed page, counts from `structure_rows()`, and no file on the board lists a page list row.
  **Now:** No board file lists a page list row. Pages are read from `## Pages`, sections from the parsed page, and every count from `structure_rows()`.
- ✅ A3.2 · Every page kind on this board gets its map in the page list, which is what lets a section start shut.
  **Done when:** a decision page, a meeting page and an agent page each render their Content parts as page list rows.
  **Now:** Checked on the built board: `Meeting-1` renders its 17 Content parts as page list rows and `Agent-1` renders its own, beside every decision page, all from the one function.


### P · 🏁 The page list on a small screen
- ⬜ P1 · The page list and its outline are usable with a finger.
  **Done when:** the outline can be opened and an outline row hit on an iPad, with no hover available.
  **Now:** Not started. The page list overlays and self-closes on a narrow screen, and nobody has opened the outline on a real touch device.


## Files
### ⚙️ Engines · what RUNS this subject
- `src/page_board.py`
  The page list and outline HTML, in the page list block of `render()`.
- `src/page_question.py`
  `structure_rows()`, the shared data half of the Structure map, read by the drawer and the page list alike.
- `assets/css/70-sidebar.css`
  The page list block, the `.sb-out` outline block, and the drag handle beside the two conditions that show it.
- `assets/js/60-sidebar.js`
  The ☰ toggle, the per-board persistence, `mark()` with its accordion, and the outline click handler.

### 📤 Output files · what a BUILD writes
- `board/QB/QB2a-sidebar.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit.

## Glossary
- 🧱 **page list**: the fixed strip down the left side of every board page, listing the Index, the groups and the pages. Also called the sidebar, the name the code identifiers keep; the two words mean the same thing on this page.
- 🧭 **section outline**: the rows the page list unfolds under the page you have open, one per section of that page and one per part inside a section.
- 🪗 **accordion**: the rule that at most one page's section outline is open at a time, so navigating to a page shuts the last one.
- 🧩 **Structure rows**: the section rows and their counts, computed once by `structure_rows()` and shown in two places, the Opening drawer and the page list.
- 👁 **on stage**: visible on the page without clicking anything.

## Lesson
- 🎯 **An outline row named a page id that never existed** · 260801
  JL: "when I click a page's content name it does not take me there."
  Two bugs stacked, and the first made the second invisible.
  The handler read the target page from the row's own href and sliced one character off it, which is exactly right in the one-file board, where the href IS `#QB8c`, and produces `B/QB8c-editing.html` in the tree, where the href is a file path.
  `getElementById` of that returns nothing, so the handler returned at its first line and the click did nothing at all.
  Behind it sat a timing bug: the work was scheduled on a fixed 80ms timer, which is a race against a fetch and a wrap swap, and losing it was equally silent.
  The id now comes from the `.sb-out` the row lives in, which carries it in BOTH packagings, and the click is treated as a REQUEST that outlives the click: it is parked in `sessionStorage` and honoured by whichever document ends up holding the page, this one after a swap or a fresh one after a real load, then cleared so it can never fire twice.
  A third bug hid behind those two and only appeared once they were fixed: honouring the request straight after the click opened the division on the DOM that was about to be REPLACED, and consumed it on the way, so the fresh wrap arrived with nothing left to apply.
  A row therefore worked from another page and did nothing from its own, which is the opposite of what anyone would guess.
  The request is now honoured only by the arrival, never by the click, except in the one-file board where no fetch happens.
  Scrolling is done TWICE on purpose: the swap path calls `window.scrollTo(0, 0)` on its way in and a real load gets the browser's own scroll restoration, so a single call can be undone a frame later.
  Verified from four starting points, each with a cleared open-state so a previous run could not flatter it: from the group page, from the target page itself, from the Index, and from an unrelated page; in every one the named division opened and came to rest at the top of the viewport.
- 🧭 **The page list never knew which page you were on in the tree** · 260801
  JL: "the left panel of indexing does not work anymore, and the page's subcontent indexing is not here anymore."
  Both symptoms were one line: `mark()` compared each row's `href` to `location.hash`, which is right in the one-file board and meaningless in the tree, where a page is its own file with no hash and the rows are file paths.
  So nothing matched, no row took `.on`, and because the section outline opens only for the marked row, the per-page outline never appeared either.
  That is the same assumption `QC4` took out of the chat drawer on 260731; the page list kept it, and it stayed hidden because the markup was perfect: 53 rows and 53 outlines were in every file, just never selected.
  The fix gives each row a `data-page` carrying the id, which is the ONE thing spelled identically in both packagings, and asks the DOCUMENT which page it is through the drawer's own `docPage()` rather than a second copy of it.
  `mark()` now answers in a fixed order, because a wrong order let the Index row win on a group page: a page, then a group file, then the Index.
  It also re-runs on `board:updated`, since a tree navigation swaps the wrap and fires no hashchange.
  Verified on all seven kinds of file: the Index marks itself, `QB.html` and `QD.html` mark their group, and QB8c, QC4, QB4 and Meeting-1 each mark their row and open their own outline (6, 14, 26 and 28 rows).
- 📏 **The drag handle stood in the page with no page list behind it** · 260801
  JL sent a screenshot of the QD group: a blue bar down the middle of the text, tooltip "Drag to resize", page list collapsed.
  The handle is `position:fixed` and placed off `--sbw` alone, which is right while the page list is open and meaningless once it is shut, so it stayed 238px into the page and tinted on hover because that is what a handle does.
  It now carries the page list's own two visibility conditions, written out beside them: `body.nav-open`, or a viewport over 1150px that is not `nav-closed`.
  A handle cannot be a child of the thing it resizes, since the page list is `overflow-y:auto` and clips it, so the condition has to be stated twice; keeping the two statements adjacent in `70-sidebar.css` is what stops them drifting again.
  It also moved out of `80-matrix.css`, where it had no business living.
  Verified over CDP at 1400px and 900px: the handle appears and disappears exactly with the page list, and a real drag still takes it from 238px to 400px and survives a close and reopen.
- 📐 **The page yields exactly as much as the page list takes** · 260731
  JL: "when I drag the left panel the body text does not follow; board.html does, can you unify them."
  The page list's own width had become `--sbw`, but the body's `padding-left` was still hard-coded at 238px, so widening the page list slid it OVER the text instead of pushing the text along.
  Both now read the same variable, which is what `--chatw` already does for the chat drawer and the body it displaces.
  Measured in a real browser, and the two packagings are now identical: dragging the page list 238 to 460 moves the content's left edge 369 to 480 and holds its width at 1000, in the tree page and in `board.html` alike, the same three numbers.
- ↔️ **The page list is draggable, and its width is remembered** · 260731
  JL: "can the left panel be dragged, left or right? right now it feels fixed."
  Width moved onto one CSS variable `--sbw`, exactly the shape the chat drawer already uses for `--chatw`, so a handle sets the variable and the browser remembers it per machine.
  Range is 150px to 60% of the window; double-clicking the handle drops the override and returns to the 238px default.
  One thing had to change to make it hittable at all, and it took a real drag to find: the page list is `overflow-y:auto`, which CLIPS anything sitting on its edge, so a handle absolutely positioned inside it was invisible to the pointer (`elementFromPoint` returned BODY).
  The handle is therefore a FIXED strip outside the nav, tracking `left: calc(var(--sbw) - 3px)`.
  Verified by dragging it in a real browser rather than by reading the code: 238 to 440 wider, 440 to 180 narrower, the 180 surviving a reload, a jump to another page in the tree, AND the single-file board, with the double-click reset returning it to 238.

## Log
- 260806 2056 · [REVISE-CC] swept to the 260806 architecture; repaired four leftovers of the 260802 sidebar-to-page-list rename sed: the Glossary's self-referential "also called the page list" restored to "also called the sidebar", the Decision Now 📍 pointer re-aimed at the real heading `### 1 · Three altitudes, one page list`, two Diagram rows de-stuttered from "the pages page list", and the nonexistent filename `70-page list.css` restored to `70-sidebar.css`
260802 · NAMED. JL ruled the panel down the left is the **page list** ("maybe we call it 'Panel list' or 'page list'? what is the better term for it?"). Chosen over `sidebar`, which names where it sits rather than what it holds and rots if it ever moves, and over `Index`, which is already the board's home page and would repeat the overloading that made `rail` unreadable. Applied to 252 prose uses across the board; code identifiers keep `sidebar` (`70-sidebar.css`, `.sidebar`, `--sbw`, `sidebar_rows()`) because renaming those buys a reader nothing. The ☰ button now reads `☰ Pages`
260802 · Page brought to the QB4 contract. Two `## Where we are` headings had collapsed onto one in the parser, so the FIRST one, five dated records of 260731 and 260801, had never rendered at all; those five moved verbatim into `## Lesson`, which is where a post-mortem belongs. `Items to Finish` became `## Aims` (7 Aims in A1/A2/A3/P groups, no checkboxes) and the surviving `Where we are` became `## States`, with each Decision Now row rewritten into the 📍🔔⭐🛑🤖 shape and none of them ticked. Every Content part gained a caption line, a face figure and numbered `####` paragraphs; the Opening's blank line had sat directly under the question, so its four rationale sentences were hidden in `More details` while the page showed a bare question, and the rationale itself was the banned "This page defines / The hard part is / succeeds when" skeleton. `### 3.3` now states the dependency `QB4` names: the start-shut default is readable only because the page list carries the page map. Files groups renamed from subjects to actions, and a `## Glossary` added for page list, section outline, accordion and Structure rows
260801 · Outline rows fixed: the target id comes from `.sb-out` instead of a sliced href, and the click is parked in sessionStorage so either arrival path honours it. Verified from four starting points: the named division opens and lands at the top; a third bug (honouring on the click, before the swap) was found and removed in the same pass
260801 · Page list fixed for the tree: rows carry `data-page`, `mark()` asks the document (page → group → Index) instead of the URL hash, and re-marks on `board:updated`. The active row and its section outline were both dead on every tree page
260801 · Page list drag handle hidden with the page list (it stood in the page as a bar when the page list was shut, JL screenshot) and moved from 80-matrix.css to 70-sidebar.css beside the page list it belongs to
260731 · The page list became drag-resizable (--sbw, handle outside the nav because overflow clips it, width remembered per machine, double-click resets) (haipipe-board 0.85.0)
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · The Index row unfolds (JL: "what should be the index's section content? Please add them as well"): chevron on 🗂 Index, four present-only component rows, open by default at load; Topic/Pipeline/Board-Structure are gone from the Index per QB2 (0.78.0)
260731 · The click model split in two on JL's follow-up ("maybe for the right end of the page, add a hiden > ... and the normal click will show us to the top"): row click always navigates with re-click returning to the top, the hidden ▸ chevron toggles the outline; supersedes the single-toggle from earlier the same day (0.72.0)
260731 · The active row became a toggle (JL: "click that again, I collapse that page level content"): clicking the open page's row folds or unfolds its outline without leaving the page; a fresh navigation always starts unfolded (0.70.0)
260731 · Items and Files subsections joined the outline: 🎯 rows show per-group done/total, 📎 rows list the file groups (0.70.0)
260731 · Decision Now joined the outline (JL: "also unfold the Decision Now in the page list, go ahead"): Where we are subsections are jump rows with owed-tick counts, and `###` now renders as a real `.sh` heading in every non-Content section (0.67.0)
260731 · Opened on JL's ask, absorbing the page list shipped under QB2 (0.61.0) and shipping the per-page section outline with the accordion rule (0.66.0)

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0