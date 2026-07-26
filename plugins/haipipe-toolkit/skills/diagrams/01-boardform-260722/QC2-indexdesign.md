# Index page design
state: 🟡 PARTIAL
owner: JL
method: settle which questions "the front-page list" must answer, then decide what it looks like
session: d2199106-8b6a-499d-8c24-9db3658486b5

## Question
You open a board and have not clicked into any question yet: what you see is the front-page list.
What should it look like so that a person knows **within three seconds which question to act on**?

It is hard because the single-question page (`QA4`) is settled, but nobody has owned the front page, and it must hold everything at once: all questions, all groups, every state and completion.
One notch more information and it becomes a wall nobody can enter.
It matters because a board is for the second person: if the front page does not show "which question is stuck, which one is mine to move", the board is only usable by whoever wrote it.
Downstream it drives group ordering, state display, completion coloring, and default sort, all in `build.py`'s index-rendering pass, coupled to `board.md`'s `## Pages`.

## Boundary
- ✅ Covered here
  **The front-page list**: group headers, what each row shows, the visuals of state and completion, sort rules, and how "see at a glance what to act on" is achieved.
- ↪ Covered elsewhere
  The **single-question page** after the click: that is `QA4`.
  Nor whether each question's **prose is well written**: that is `QA9`.
  Nor which folder the board lives in: that is `QC1`.

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
  ＋Group   appends "### QX · title" (+ intro line) to ## Pages, letter auto
  🗄        moves the file to _archive/ (question) or removes an EMPTY group;
            nothing is ever deleted, and the md stays the single source of truth
```

## Content
### 1 · Board orientation — say what this board is doing
The top strip gives the board name, spine, and close condition before showing any individual face.
It should let a newcomer understand the board's common question and the condition for finishing it without opening a row.

### 2 · Overall progress — show how far the board has moved
The global progress area reports settled Q rulings and passed S gates as separate workflow signals.
It answers "how far along is this board?" without implying that a paused face is complete or allowing lifecycle stages to inflate question settlement.

### 3 · Group — explain why these faces belong together
Each group header names one coherent part of the board and carries a short, always-visible introduction.
Opening the introduction reveals what the group is for and why it exists.
Group controls add a Q or archive an empty group, but the explanation remains the primary reading signal.

### 4 · Face row — identify the next action
Each row exposes only the evidence needed to choose whether to open it: workflow state, id, title, open-comment signal, owner, and finish ratio.
Its most important eventual job is to make "which face needs action, and whose action is it?" answerable within three seconds.

### 5 · Ordering — make priority legible
Group order and row order tell the reader what to scan first.
Today they follow the hand-written Pages; the open design decision is whether state, unfinished work, owner, or open comments should influence that order.
Any automatic sort must remain explainable and must not silently rewrite the source.

For a paper lifecycle board, ordering has one stronger rule: named S families are the groups.
The index follows `Seed → Work → Venue → Display → Main → Appendix → Submission`, but this is stable ownership order, not a claim that execution is linear.
Pipeline owns actual edges and may revisit the independent Display layer after Narrative.
Each S row is one concrete checkable page, and a blocking Q sits immediately after the S page it governs.
Seed includes S Seed and S Literature; Main and Appendix expose every reader-facing unit instead of hiding them inside one broad section-edit stage.
A paper-level ruling may sit before Seed only when it genuinely governs the full lifecycle.

### 6 · Structure controls — edit without hiding the source
`＋Q`, `＋Group`, and archive controls are page-side writers into `board.md` and the face files.
They make the index operational while preserving markdown as the single source of truth; archive moves material rather than deleting it.

### 7 · Board chat — discuss the board as a whole
Board chat is the place to ask how the work should proceed or which face to examine next before opening one.
It supports deliberation, but it cannot replace the index's visual three-second answer because a reader should not need a conversation to discover the next action.

### After a face opens
QC2 stops at the index.
QA4 owns the opened Q/S webpage and now defines its own numbered Content sections: Opening, Diagram, Content, Items to Finish, Where we are, Files, and Supporting folds.
The two specifications use the same principle without mixing their responsibilities.

## Items to Finish
- [x] 📖 Each group introduces itself on the index
      A short sentence always visible under the group header; clicking it expands the "what this group is for and why it is here" body.
      Grammar (260724): in `## Pages`, plain lines between a `### ` heading and its first `.md` line are the intro; line 1 is the sentence, the rest is the expandable body.
      Rendered as a native `<details>`, so the strip-scripts invariant holds; all five groups on this board carry one now.
- [x] 🧱 Groups and questions can be added and archived from the page
      JL 260724: "add and delete question groups, and add and delete question items."
      Shipped as one writer, `POST /_board/structure` (ops `add_group` / `add_question` / `archive_question` / `archive_group`) living in serve.py and imported by the console (QE3 Law). ＋Q seeds a stub Q file and lists it under its group; ＋Group appends a `### QX · title` heading with its intro; archive MOVES a question to `_archive/` and only removes a group once it lists nothing.
      Verified 260724: full add→archive round trip leaves board.md byte-identical, refusal paths clean over HTTP on 5599 and through the console on 8093.
- [x] 📚 Every index component explains its purpose
      Content now describes the eventual reader outcome for board orientation, overall progress, groups, face rows, ordering, structure controls, and board chat.
      The opened-face section meanings stay in QA4 so QC2 remains an index specification.
- [ ] Settle the questions the front page must answer
      At least three: what is this board doing · how far along is it · **which question do I act on now**.
      The third is the hardest and the one that matters.
- [ ] Settle what each row shows
      Today: state · id · title · open-comment badge · owner · completion coloring.
      Enough?
      Too much?
- [x] Settle lifecycle grouping; keep ordinary-board sorting open
      Paper lifecycle boards use seven full-name families: Seed, Work, Venue, Display, Main, Appendix, and Submission.
      Display owns the evidence-presentation layer consumed by Main and Appendix.
      Each S is one page; its blocking Q follows it.
      Ordinary boards still use hand-written Pages groups, and automatic priority sorting remains undecided.
- [ ] Settle how completion coloring reads
      Today white→green by tick ratio. ⏸️ ON HOLD also renders full, easily misread as "done".
- [ ] A zero-background person points at the right question within three seconds
      Same acceptance as `QA4`: a fresh agent sees only the front page, is asked "which question to act on", and must answer correctly.

## Where we are
**The index is now a place you can WORK and understand, not only view: its seven Content subsections explain what every component is eventually for; paper lifecycles use seven readable S-family groups; the structure itself is editable from the page; and the index carries its own chat. The reading design questions (sort, coloring, the three-second test) stay open.**

- 260725 JL · 🖼 Display became an independent family
  Display now owns the claim-to-display map, accepted assets, captions, statistical labels, and Main/Appendix placement.
  Pipeline still places it after Narrative; Pages order remains navigation.

- 260725 JL · 🌱 Full-name paper lifecycle families
  The paper lifecycle now reads Seed, Work, Venue, Display, Main, Appendix, Submission.
  Seed contains S Seed and S Literature; every Main section and Appendix unit is its own page; reconcile, compile, review, and submit are explicit terminal pages.
  Temporary SM/SA abbreviations retired.

- 260725 JL · 🔄 Submission is a repeatable round
  Submission keeps four stable pages.
  External review reopens affected Work, Display, Main, or Appendix pages, then the paper runs the same reconcile, compile, review, submit sequence again.

- 260725 JL · 🧭 Stage-first exposed the family model
  The MISQ paper first exposed the weakness of broad QA/QB/QC buckets and moved to one group per stage.
  That intermediate form made the stable families visible; the current rule above supersedes it with seven full-name groups and one concrete page per S row.

- 260725 JL · 📚 Index anatomy made explicit
  JL asked for Content to explain what each webpage section is for.
  QC2 now defines its own seven index components and points to QA4 for the opened Q/S face, keeping the ownership boundary visible.

- 260725 CC · 🤖 A chatbot on the index (JL's ask)
  The bottom-right button now shows on the index too, labeled "🤖 Board chat".
  It opens the same `QD2` drawer (and the ⌨ inside it is the same `QD3` terminal), just attached to `board.md` instead of one question, so "how should we work / which question next" can be discussed right on the index.
  The three-second VISUAL answer this question owes is still owed: a chat answer takes longer than three seconds.

- 260724 CC · 🧱 Structure became editable from the front page
  Per JL's ask: ＋Q on every group header, ＋Group at the list's end, hover-🗄 archive on rows and headers, all two-click confirmed, no native dialogs.
  The buttons are writers only: board.md's `## Pages` plus the Q files stay the single source of truth, `_archive/` keeps everything recoverable, and the live watcher (QD6) swaps the updated index in under you after each op.
- 260724 CC · 📖 Group intros landed with a new Pages grammar
  Intro lines sit directly under each `### ` heading in `## Pages`; the per-group paragraphs that used to live in `## Pipeline` moved there (Pipeline keeps only the overall narrative), so nothing is said twice.
- What it looks like today
  Board name + spine + close condition + progress bar + two global fold-outs (what is this board / how are the Qs ordered) + the grouped list in `## Pages` order, each group led by its intro.
- What each row has today
  State badge · id · title · open-comment badge · owner · row tinted white→green by completion (`--fill`, percentage in `title`) · hover archive.
- Known defects
  ⏸️ ON HOLD renders as full green like ✅, reads as "done"; with many questions it is one long strip with no visible priority; group order is entirely hand-maintained in the Pages.

## Files
- `build.py`
  The index-rendering pass (`rows` / `frac_done` / the `.ir` CSS family), now also the Pages-intro parse (`gintro`) and the `details.gi` render.
  Changing this question starts here.
- `board.md`
  `## Pages` decides grouping, order, AND each group's intro (plain lines under the `### ` heading; line 1 = the visible sentence).
  If sorting ever becomes automatic, this section's role must be redefined too.
- `serve.py`
  `structure_op()`: the one writer for add_group / add_question / archive_question / archive_group; `POST /_board/structure`.
  The console imports it, never reimplements.
- `assets/board.js` + `assets/board.css`
  The page-side controls (＋Q, ＋Group, 🗄 with two-click confirm, inline mini form) and the intro styling; wired into `__boardRewire` so they survive live swaps.

## Discussion
> JL: QC2 Index page design 我们在这个地方需要能够添加和删除板块，也就是说，既能添加和删除 question group，也能添加和删除 question item。 另外，在 question group 之间，也需要有一个非常短的句子来介绍一下这个 group。我想的是这样的：比如你有一个 question group（像 QC、QA 这种），下面配一个简单的介绍（sentence）。当我们点击它的时候，它就会向下展开，弹出一个下拉的介绍。 这个介绍主要用来解释这个 group 是干嘛的，以及我们为什么要在这里使用它。大概就是这样的一个意思。
>> CC0724: both shipped. (1) Group intros: every group header now carries one always-visible sentence; click the ▸ and it drops open into the longer "what this group is for, why it is here" body. It lives in board.md's ## Pages as plain lines under the ### heading (first line = the sentence, the rest = the dropdown), rendered as a native details element, so it survives script-stripping and stays hand-editable. (2) Add/delete: ＋Q on each group header, ＋Group at the end of the list, and a hover 🗄 on every row and header. All of them only write the md through one endpoint (/_board/structure in serve.py, relayed by the console); "delete" is an archive that moves the file into _archive/, so nothing is ever lost. Try it on this page: hover a group header.
> JL: could we have the chatbot in the index page, so we can discuss how to work in the index page. (260725)
>> CC0725: built. The bottom-right 🤖 button now shows on the index as "🤖 Board chat"; it opens the same QD2 drawer (and QD3 terminal via ⌨), attached to board.md, primed with the index's own view: spine, close condition, every face's state and open comments. It has a canned 🧭 "Which question should I act on?" button, and its 🔧 button works comments board-wide. Implementation details are recorded on QD2; this page only owns the entry point.
> JL: Content should explain, section by section, what each part of the Q webpage is eventually for: Opening, Diagram, and so on. (260725)
>> CC0725: agreed on the principle and kept the ownership clean. QC2 now explains the index's own seven components; QA4 explains the seven parts of an opened Q/S face and is linked from QC2's final Content subsection.
> JL: how do we make this match the paper stages? (260725)
>> CC0725: this first became stage-first, then the paper exposed a clearer stable abstraction:
>> seven full-name S families. Seed, Work, Venue, Display, Main, Appendix, and Submission are now the groups;
>> each concrete S page is a row, and its blocking Q sits directly after it.
> JL: Display should be its own group because it is important. (260725)
>> CC0725: implemented as S Display 0. It is a separate progress family and remains between Narrative and the Main/Appendix consumers in Pipeline.

## Log
260725 · Display separated from Work into its own family; lifecycle index now has seven S groups
260725 · Family order clarified as navigation, Pipeline as execution; Submission pages now repeat across revision rounds
260725 · Full-name S families replaced temporary S/SM/SA grouping: Seed (including Literature), Work, Venue, Main, Appendix, Submission
260725 · Lifecycle board grouping settled: stage-order groups, canonical S first, owned Q rulings after; MISQ board reorganized to match
260725 · Content now defines seven index components and explicitly hands the opened Q/S face to QA4; QA4 received the parallel section-purpose map
260725 1040 · 🤖 Board chat entry landed on the index (JL's ask; it is the QD2 drawer / QD3 terminal opened on board.md, details on QD2): fab shows on the index, label switches, follow() returns to the board session
260724 1553 · JL's two asks shipped: Pages-intro grammar + details.gi render (build.py), structure_op writer + /_board/structure (serve.py, imported by boards_api), page controls ＋Q/＋Group/🗄 (board.js/css); board.md's five groups got intros, Pipeline slimmed to the narrative; round trip byte-identical, refusals verified on 5599 + 8093; 🔴 → 🟡
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Opened: the QC group refocused from "needs JL's ruling" to "index and structure"; the front page becomes its own question (`QA4` owns only the single-question page; the index page had no owner)
