# Index page design
state: 🟡 PARTIAL
owner: JL
method: settle which questions "the front-page list" must answer, then decide what it looks like
session: d2199106-8b6a-499d-8c24-9db3658486b5

## Question
You open a board and have not clicked into any question yet: what you see is the front-page list. What should it look like so that a person knows **within three seconds which question to act on**?

It is hard because the single-question page (`QA4`) is settled, but nobody has owned the front page, and it must hold everything at once: all questions, all groups, every state and completion. One notch more information and it becomes a wall nobody can enter. It matters because a board is for the second person: if the front page does not show "which question is stuck, which one is mine to move", the board is only usable by whoever wrote it. Downstream it drives group ordering, state display, completion coloring, and default sort, all in `build.py`'s index-rendering pass, coupled to `board.md`'s `## Roster`.

## Boundary
- ✅ Covered here
  **The front-page list**: group headers, what each row shows, the visuals of state and completion, sort rules, and how "see at a glance what to act on" is achieved.
- ↪ Covered elsewhere
  The **single-question page** after the click: that is `QA4`. Nor whether each question's **prose is well written**: that is `QA5`. Nor which folder the board lives in: that is `QC1`.

## Diagram
```
top of board.html (no question opened yet)
┌──────────────────────────────────────────────┐
│ board name · 🦴 spine · 🏁 close condition    │
│ ▓▓▓▓▓░░░░░  N/M settled                      │  progress bar
├──────────────────────────────────────────────┤
│ QA · Defining a board            [＋Q] [🗄]  │  group header (hover controls)
│ ▸ Pin down the thing itself; nothing …       │  ← group intro: one sentence,
│   (click ▸ → expands: what / why this group) │    click to expand the why
│  ✅ QA1  Board folder shape        🔧 CC      │  ← what does each row show?
│  🟡 QA4  Single Question Webpage…  🔧 CC  7/9 │     how is completion colored?
│  🔴 QD4  LLM topic icons        🗄 🔧 CC  0/4 │     hover 🗄 = archive (2-click)
│  …                                            │
│  [＋ Group]                                   │
└──────────────────────────────────────────────┘
         ↑ within three seconds: "which question do I act on?"

  every button is only a writer into board.md:
  ＋Q       creates QXN-slug.md from the house stub + lists it under its group
  ＋Group   appends "### QX · title" (+ intro line) to ## Roster, letter auto
  🗄        moves the file to _archive/ (question) or removes an EMPTY group;
            nothing is ever deleted, and the md stays the single source of truth
```

## Items to Finish
- [x] 📖 Each group introduces itself on the index
      A short sentence always visible under the group header; clicking it expands the "what this group is for and why it is here" body. Grammar (260724): in `## Roster`, plain lines between a `### ` heading and its first `.md` line are the intro; line 1 is the sentence, the rest is the expandable body. Rendered as a native `<details>`, so the strip-scripts invariant holds; all five groups on this board carry one now.
- [x] 🧱 Groups and questions can be added and archived from the page
      JL 260724: "add and delete question groups, and add and delete question items." Shipped as one writer, `POST /_board/structure` (ops `add_group` / `add_question` / `archive_question` / `archive_group`) living in serve.py and imported by the console (QE3 Law). ＋Q seeds a stub Q file and lists it under its group; ＋Group appends a `### QX · title` heading with its intro; archive MOVES a question to `_archive/` and only removes a group once it lists nothing. Verified 260724: full add→archive round trip leaves board.md byte-identical, refusal paths clean over HTTP on 5599 and through the console on 8093.
- [ ] Settle the questions the front page must answer
      At least three: what is this board doing · how far along is it · **which question do I act on now**. The third is the hardest and the one that matters.
- [ ] Settle what each row shows
      Today: state · id · title · open-comment badge · owner · completion coloring. Enough? Too much?
- [ ] Settle sort and grouping rules
      Today it is purely the hand-written `## Roster` order. Should "by state", "by completion", "open comments first" exist?
- [ ] Settle how completion coloring reads
      Today white→green by tick ratio. ⏸️ ON HOLD also renders full, easily misread as "done".
- [ ] A zero-background person points at the right question within three seconds
      Same acceptance as `QA4`: a fresh agent sees only the front page, is asked "which question to act on", and must answer correctly.

## Where we are
**The index is now a place you can WORK, not only view: groups introduce themselves, and the structure itself (groups + questions) is editable from the page. The reading design questions (sort, coloring, the three-second test) stay open.**

- 260724 CC · 🧱 Structure became editable from the front page
  Per JL's ask: ＋Q on every group header, ＋Group at the list's end, hover-🗄 archive on rows and headers, all two-click confirmed, no native dialogs. The buttons are writers only: board.md's `## Roster` plus the Q files stay the single source of truth, `_archive/` keeps everything recoverable, and the live watcher (QD6) swaps the updated index in under you after each op.
- 260724 CC · 📖 Group intros landed with a new Roster grammar
  Intro lines sit directly under each `### ` heading in `## Roster`; the per-group paragraphs that used to live in `## Pipeline` moved there (Pipeline keeps only the overall narrative), so nothing is said twice.
- What it looks like today
  Board name + spine + close condition + progress bar + two global fold-outs (what is this board / how are the Qs ordered) + the grouped list in `## Roster` order, each group led by its intro.
- What each row has today
  State badge · id · title · open-comment badge · owner · row tinted white→green by completion (`--fill`, percentage in `title`) · hover archive.
- Known defects
  ⏸️ ON HOLD renders as full green like ✅, reads as "done"; with many questions it is one long strip with no visible priority; group order is entirely hand-maintained in the Roster.

## Files
- `build.py`
  The index-rendering pass (`rows` / `frac_done` / the `.ir` CSS family), now also the Roster-intro parse (`gintro`) and the `details.gi` render. Changing this question starts here.
- `board.md`
  `## Roster` decides grouping, order, AND each group's intro (plain lines under the `### ` heading; line 1 = the visible sentence). If sorting ever becomes automatic, this section's role must be redefined too.
- `serve.py`
  `structure_op()`: the one writer for add_group / add_question / archive_question / archive_group; `POST /_board/structure`. The console imports it, never reimplements.
- `assets/board.js` + `assets/board.css`
  The page-side controls (＋Q, ＋Group, 🗄 with two-click confirm, inline mini form) and the intro styling; wired into `__boardRewire` so they survive live swaps.

## Discussion
> JL: QC2 Index page design 我们在这个地方需要能够添加和删除板块，也就是说，既能添加和删除 question group，也能添加和删除 question item。 另外，在 question group 之间，也需要有一个非常短的句子来介绍一下这个 group。我想的是这样的：比如你有一个 question group（像 QC、QA 这种），下面配一个简单的介绍（sentence）。当我们点击它的时候，它就会向下展开，弹出一个下拉的介绍。 这个介绍主要用来解释这个 group 是干嘛的，以及我们为什么要在这里使用它。大概就是这样的一个意思。
>> CC0724: both shipped. (1) Group intros: every group header now carries one always-visible sentence; click the ▸ and it drops open into the longer "what this group is for, why it is here" body. It lives in board.md's ## Roster as plain lines under the ### heading (first line = the sentence, the rest = the dropdown), rendered as a native details element, so it survives script-stripping and stays hand-editable. (2) Add/delete: ＋Q on each group header, ＋Group at the end of the list, and a hover 🗄 on every row and header. All of them only write the md through one endpoint (/_board/structure in serve.py, relayed by the console); "delete" is an archive that moves the file into _archive/, so nothing is ever lost. Try it on this page: hover a group header.

## Log
260724 1553 · JL's two asks shipped: Roster-intro grammar + details.gi render (build.py), structure_op writer + /_board/structure (serve.py, imported by boards_api), page controls ＋Q/＋Group/🗄 (board.js/css); board.md's five groups got intros, Pipeline slimmed to the narrative; round trip byte-identical, refusals verified on 5599 + 8093; 🔴 → 🟡
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Opened: the QC group refocused from "needs JL's ruling" to "index and structure"; the front page becomes its own question (`QA4` owns only the single-question page; the index page had no owner)
