# The pages sidebar: jump anywhere from a fixed left rail
state: 🟡 PARTIAL · the rail and the per-page section outline ship; the outline's reach forks await JL
owner: JL
method: render the rail from the same listing as the index and the same Structure rows as the Opening drawer, so the sidebar can never disagree with the page

## Opening
How should the sidebar let a reader move from Board to group to page section without becoming a second index that can drift?

This page defines one fixed left rail for the Index, every group, every page, and the open page's outline.
The hard part is exposing enough depth for precise jumps while keeping only one page outline open at a time.
A separate hand-kept registry would disagree with the source as soon as a page or section changed.
The rail succeeds when a reader can jump to any current section and always see the same structure the page renders.


## Diagram
```
┌ ☰ toggles the rail ────────────┐
│ 🗂 Index                #top    │
│ QA · Design           #group-QA│
│   🟡 QA0  three folders  #QA0  │
│ QB · Delivery                  │
│   🟡 QB2  webpage design       │
│   🟡 QB2a the pages sidebar ◀── the OPEN page, outline unfolded
│       🧭 Opening               │
│       📚 Content · 3 divisions │
│         1 · the rail …    ──▶  opens the division and scrolls to it
│       🎯 Items  2 done · 1 open│
│       📎 Files  3 files        │
│   🟡 QB4  the shared layout    │  every other page stays one row
└────────────────────────────────┘
```

## Content
### 1 · Three altitudes, one rail
The rail shows the board (`🗂 Index`), the groups, and the pages, exactly in `## Pages` order, each page as state emoji plus id plus title.
It is rendered server side by `page_board.py` from the same loop that renders the index rows, so it exists with JavaScript off and can never list a page the index does not.
It sits OUTSIDE `.wrap`, untouched by the `:target` show and hide rules, so it stays up in both the Index view and an open page; a group link re-targets `#group-…`, which also brings the Index back on stage.
The ☰ toggle persists per board in localStorage; with no saved choice the rail opens on wide screens and hides on narrow ones, where it overlays and a jump closes it.

### 2 · The section outline, for the open page only
Under the open page's row the rail unfolds that page's sections: the same rows the Opening drawer's Structure map shows, emoji, name, and the computed meta (`2 done · 1 open`, `3 files`), plus one indented row per Content division and per Where we are subsection (JL 260731; a Decision Now row also shows how many ticks it owes).
The accordion is the rule, not an option: navigation collapses every other page's outline, so the rail never becomes forty open trees (JL 260731).
The row and the fold are two controls (JL 260731, superseding the same-day single-toggle): clicking a page row goes to that page, re-click returning to its TOP, while the hidden `▸` at the row's right end toggles the section outline, rotating to `▾` while open.
The accordion still holds, at most one outline open, and a fresh navigation starts unfolded.
Clicking an outline row navigates to the page if needed, then opens the target `<details>` and scrolls to it; a division row opens Content first, then the division.
The section rows come from `structure_rows()` in `page_question.py`, extracted 260731 so the drawer and the rail read one source and can never disagree.

### 3 · Derived, never registered
The rail adds no authored surface: pages come from `## Pages`, sections from the parsed page, counts from the same regexes the drawer uses.
That is the honesty argument from the Board Map applied one level down: a hand-kept outline would drift the day someone adds a section, so the outline is computed or it is not there.

## Items to Finish
### The rail and its outline, shipped
- [x] 📑 The rail ships
      haipipe-board 0.61.0: fixed left rail, ☰ toggle, per-board persistence, active row highlight, print hidden.
- [x] 🧷 The per-page section outline ships, accordion enforced
      haipipe-board 0.66.0: Structure rows plus Content divisions under the open page only; click opens and scrolls the target section.
### The outline's reach forks, and the touch pass
- [ ] 🪗 Outline rows for Where we are subsections
      PROPOSED: shipped in 0.67.0 on JL's "also unfold the Decision Now in the sidebar, go ahead": every `###` subsection of Where we are is a jump row found by its heading text, and a Decision Now row shows how many ticks it owes.
      The same round made `###` render as a real subsection heading (`.sh`) inside any non-Content section, where it had rendered as literal "### …" prose.
- [ ] 🗂 An outline for the Index view itself
      PROPOSED: ruled by JL 260731 ("what should be the index's section content? Please add them as well") and shipped in 0.78.0: the `🗂 Index` row carries the chevron and unfolds 🗺 Board Map, 🩺 Section Matrix, 📄 All Pages, and 📈 Activity, present-only, each scrolling the Index to its component; Topic, Pipeline, and Board-Structure are not rows because JL removed them from the Index the same round (`QB2`).
- [ ] 📱 Touch pass
      The rail overlays and self-closes on narrow screens; verify the outline is usable without hover on an iPad.

## Where we are

- 260801 JL · 🎯 An outline row named a page id that never existed
  JL: "when I click a page's content name it does not take me there."
  Two bugs stacked, and the first made the second invisible.
  The handler read the target page from the row's own href and sliced one character off it, which is exactly right in the one-file board, where the href IS `#QB5c`, and produces `B/QB5c-editing.html` in the tree, where the href is a file path.
  `getElementById` of that returns nothing, so the handler returned at its first line and the click did nothing at all.
  Behind it sat a timing bug: the work was scheduled on a fixed 80ms timer, which is a race against a fetch and a wrap swap, and losing it was equally silent.
  The id now comes from the `.sb-out` the row lives in, which carries it in BOTH packagings, and the click is treated as a REQUEST that outlives the click: it is parked in `sessionStorage` and honoured by whichever document ends up holding the page, this one after a swap or a fresh one after a real load, then cleared so it can never fire twice.
  A third bug hid behind those two and only appeared once they were fixed: honouring the request straight after the click opened the division on the DOM that was about to be REPLACED, and consumed it on the way, so the fresh wrap arrived with nothing left to apply.
  A row therefore worked from another page and did nothing from its own, which is the opposite of what anyone would guess.
  The request is now honoured only by the arrival, never by the click, except in the one-file board where no fetch happens.
  Scrolling is done TWICE on purpose: the swap path calls `window.scrollTo(0, 0)` on its way in and a real load gets the browser's own scroll restoration, so a single call can be undone a frame later.
  Verified from four starting points, each with a cleared open-state so a previous run could not flatter it: from the group page, from the target page itself, from the Index, and from an unrelated page; in every one the named division opened and came to rest at the top of the viewport.
- 260801 JL · 🧭 The rail never knew which page you were on in the tree
  JL: "the left panel of indexing does not work anymore, and the page's subcontent indexing is not here anymore."
  Both symptoms were one line: `mark()` compared each row's `href` to `location.hash`, which is right in the one-file board and meaningless in the tree, where a page is its own file with no hash and the rows are file paths.
  So nothing matched, no row took `.on`, and because the section outline opens only for the marked row, the per-page outline never appeared either.
  That is the same assumption `QC4` took out of the chat drawer on 260731; the rail kept it, and it stayed hidden because the markup was perfect: 53 rows and 53 outlines were in every file, just never selected.
  The fix gives each row a `data-page` carrying the id, which is the ONE thing spelled identically in both packagings, and asks the DOCUMENT which page it is through the drawer's own `docPage()` rather than a second copy of it.
  `mark()` now answers in a fixed order, because a wrong order let the Index row win on a group page: a page, then a group file, then the Index.
  It also re-runs on `board:updated`, since a tree navigation swaps the wrap and fires no hashchange.
  Verified on all seven kinds of file: the Index marks itself, `QB.html` and `QD.html` mark their group, and QB5c, QC4, QB4 and Meeting-1 each mark their row and open their own outline (6, 14, 26 and 28 rows).
- 260801 JL · 📏 The drag handle stood in the page with no rail behind it
  JL sent a screenshot of the QD group: a blue bar down the middle of the text, tooltip "Drag to resize", rail collapsed.
  The handle is `position:fixed` and placed off `--sbw` alone, which is right while the rail is open and meaningless once it is shut, so it stayed 238px into the page and tinted on hover because that is what a handle does.
  It now carries the rail's own two visibility conditions, written out beside them: `body.nav-open`, or a viewport over 1150px that is not `nav-closed`.
  A handle cannot be a child of the thing it resizes, since the rail is `overflow-y:auto` and clips it, so the condition has to be stated twice; keeping the two statements adjacent in `70-sidebar.css` is what stops them drifting again.
  It also moved out of `80-matrix.css`, where it had no business living.
  Verified over CDP at 1400px and 900px: the handle appears and disappears exactly with the rail, and a real drag still takes it from 238px to 400px and survives a close and reopen.

- 260731 JL · 📐 The page yields exactly as much as the rail takes
  JL: "when I drag the left panel the body text does not follow; board.html does, can you unify them."
  The rail's own width had become `--sbw`, but the body's `padding-left` was still hard-coded at 238px, so widening the rail slid it OVER the text instead of pushing the text along.
  Both now read the same variable, which is what `--chatw` already does for the chat drawer and the body it displaces.
  Measured in a real browser, and the two packagings are now identical: dragging the rail 238 to 460 moves the content's left edge 369 to 480 and holds its width at 1000, in the tree page and in `board.html` alike, the same three numbers.

- 260731 JL · ↔️ The rail is draggable, and its width is remembered
  JL: "can the left panel be dragged, left or right? right now it feels fixed."
  Width moved onto one CSS variable `--sbw`, exactly the shape the chat drawer already uses for `--chatw`, so a handle sets the variable and the browser remembers it per machine.
  Range is 150px to 60% of the window; double-clicking the handle drops the override and returns to the 238px default.
  One thing had to change to make it hittable at all, and it took a real drag to find: the rail is `overflow-y:auto`, which CLIPS anything sitting on its edge, so a handle absolutely positioned inside it was invisible to the pointer (`elementFromPoint` returned BODY).
  The handle is therefore a FIXED strip outside the nav, tracking `left: calc(var(--sbw) - 3px)`.
  Verified by dragging it in a real browser rather than by reading the code: 238 to 440 wider, 440 to 180 narrower, the 180 surviving a reload, a jump to another page in the tree, AND the single-file board, with the double-click reset returning it to 238.

## Where we are
The rail shipped in 0.61.0 and the section outline in 0.66.0, both derived at build time; nothing in the rail is authored.
Opened 260731 on JL's ask after the rail shipped under `QB2`: "For this left panel, do we have a Q for it? if not, make it and then go ahead to work on it."
The pasted Structure rows ("🎯 Items to Finish · 2 done · 1 open …") are the exact rows the outline now mirrors.

### Decision Now
- [ ] 🪗 Rule the outline's reach inside a page
      PROPOSED: ruled by JL 260731 ("ok, also unfold the Decision Now in the sidebar, go ahead") and shipped in 0.67.0; a tick closes this row and the matching Items row together.
- [ ] 🗂 Tick the shipped Index outline
      PROPOSED: ruled and shipped 260731 (four present-only rows: Board Map, Section Matrix, All Pages, Activity); a tick closes this row and the matching Items row.
- [ ] 🧠 Confirm QB2a owns the sidebar
      Carved 260731 from QB2's dated entry; QB2 keeps the webpage and Index design, this face keeps the rail.

## Files
### The server-rendered half
- `../../board/haipipe-board/src/page_board.py`
  The rail and outline HTML, in the sidebar block of `render()`.
- `../../board/haipipe-board/src/page_question.py`
  `structure_rows()`, the shared data half of the Structure map.
### The client assets
- `../../board/haipipe-board/assets/css/70-sidebar.css`
  The rail block and the `.sb-out` outline block at the end of the file.
- `../../board/haipipe-board/assets/js/60-sidebar.js`
  The toggle, persistence, accordion `mark()`, and the outline click handler.

## Log
260801 · Outline rows fixed: the target id comes from `.sb-out` instead of a sliced href, and the click is parked in sessionStorage so either arrival path honours it. Verified from four starting points: the named division opens and lands at the top; a third bug (honouring on the click, before the swap) was found and removed in the same pass
260801 · Rail fixed for the tree: rows carry `data-page`, `mark()` asks the document (page → group → Index) instead of the URL hash, and re-marks on `board:updated`. The active row and its section outline were both dead on every tree page
260801 · Rail drag handle hidden with the rail (it stood in the page as a bar when the rail was shut, JL screenshot) and moved from 80-matrix.css to 70-sidebar.css beside the rail it belongs to
260731 · The rail became drag-resizable (--sbw, handle outside the nav because overflow clips it, width remembered per machine, double-click resets) (haipipe-board 0.85.0)
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · The Index row unfolds (JL: "what should be the index's section content? Please add them as well"): chevron on 🗂 Index, four present-only component rows, open by default at load; Topic/Pipeline/Board-Structure are gone from the Index per QB2 (0.78.0)
260731 · The click model split in two on JL's follow-up ("maybe for the right end of the page, add a hiden > ... and the normal click will show us to the top"): row click always navigates with re-click returning to the top, the hidden ▸ chevron toggles the outline; supersedes the single-toggle from earlier the same day (0.72.0)
260731 · The active row became a toggle (JL: "click that again, I collapse that page level content"): clicking the open page's row folds or unfolds its outline without leaving the page; a fresh navigation always starts unfolded (0.70.0)
260731 · Items and Files subsections joined the outline: 🎯 rows show per-group done/total, 📎 rows list the file groups (0.70.0)
260731 · Decision Now joined the outline (JL: "also unfold the Decision Now in the sidebar, go ahead"): Where we are subsections are jump rows with owed-tick counts, and `###` now renders as a real `.sh` heading in every non-Content section (0.67.0)
260731 · Opened on JL's ask, absorbing the rail shipped under QB2 (0.61.0) and shipping the per-page section outline with the accordion rule (0.66.0)
