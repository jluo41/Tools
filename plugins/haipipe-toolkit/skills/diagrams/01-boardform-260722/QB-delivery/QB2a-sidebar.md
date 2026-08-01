# The pages sidebar: jump anywhere from a fixed left rail
state: 🟡 PARTIAL · the rail and the per-page section outline ship; the outline's reach forks await JL
owner: JL
method: render the rail from the same listing as the index and the same Structure rows as the Opening drawer, so the sidebar can never disagree with the page

## Opening
What does the left rail show at each altitude, and how does it stay honest?
The rail lists Index, then every group, then every page, and, for the OPEN page only, that page's sections and subsections (JL 260731: "make sure that everytime, only one pages's section and subsection can be opened").
Both halves are derived at build time from sources that already exist, the `## Pages` listing and the Structure rows, so the rail keeps no registry of its own to rot.


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
260731 · The rail became drag-resizable (--sbw, handle outside the nav because overflow clips it, width remembered per machine, double-click resets) (haipipe-board 0.85.0)
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · The Index row unfolds (JL: "what should be the index's section content? Please add them as well"): chevron on 🗂 Index, four present-only component rows, open by default at load; Topic/Pipeline/Board-Structure are gone from the Index per QB2 (0.78.0)
260731 · The click model split in two on JL's follow-up ("maybe for the right end of the page, add a hiden > ... and the normal click will show us to the top"): row click always navigates with re-click returning to the top, the hidden ▸ chevron toggles the outline; supersedes the single-toggle from earlier the same day (0.72.0)
260731 · The active row became a toggle (JL: "click that again, I collapse that page level content"): clicking the open page's row folds or unfolds its outline without leaving the page; a fresh navigation always starts unfolded (0.70.0)
260731 · Items and Files subsections joined the outline: 🎯 rows show per-group done/total, 📎 rows list the file groups (0.70.0)
260731 · Decision Now joined the outline (JL: "also unfold the Decision Now in the sidebar, go ahead"): Where we are subsections are jump rows with owed-tick counts, and `###` now renders as a real `.sh` heading in every non-Content section (0.67.0)
260731 · Opened on JL's ask, absorbing the rail shipped under QB2 (0.61.0) and shipping the per-page section outline with the accordion rule (0.66.0)
