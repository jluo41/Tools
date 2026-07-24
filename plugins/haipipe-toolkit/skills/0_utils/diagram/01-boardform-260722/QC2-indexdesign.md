# Index page design
state: 🔴 OPEN
owner: JL
method: settle which questions "the front-page list" must answer, then decide what it looks like

## Question
You open a board and have not clicked into any question yet — what you see is the front-page list. What should it look like so that a person knows **within three seconds which question to act on**?

- Why it is hard
  The single-question page (`QA4`) is settled, but nobody has owned the front page. It must hold everything at once: all questions, all groups, every state and completion — one notch more information and it becomes a wall nobody can enter.
- What breaks if we leave it
  A board is for the second person. If the front page does not show "which question is stuck, which one is mine to move", the board is only usable by whoever wrote it.
- What it affects downstream
  Group ordering, state display, completion coloring, default sort — all in `build.py`'s index-rendering pass, coupled to `board.md`'s `## Roster`.

## Boundary
- ✅ This question owns
  **The front-page list**: group headers, what each row shows, the visuals of state and completion, sort rules, and how "see at a glance what to act on" is achieved.
- ❌ This question does not own
  The **single-question page** after the click — that is `QA4`. Nor whether each question's **prose is well written** — that is `QA5`. Nor which folder the board lives in — that is `QC1`.

## Diagram
```
top of board.html (no question opened yet)
┌──────────────────────────────────────────────┐
│ board name · 🦴 spine · 🏁 close condition    │
│ ▓▓▓▓▓░░░░░  N/M settled                      │  progress bar
├──────────────────────────────────────────────┤
│ QA · Defining a board                        │  group header
│  ✅ QA1  Board folder shape        🔧 CC      │  ← what does each row show?
│  🟡 QA4  Single Question Webpage…  🔧 CC  7/9 │     how is completion colored?
│  🔴 QD4  LLM topic icons           🔧 CC  0/4 │     what is the sort?
│  …                                            │
└──────────────────────────────────────────────┘
         ↑ within three seconds: "which question do I act on?"
```

## Items to Finish
- [ ] Settle the questions the front page must answer
      At least three: what is this board doing · how far along is it · **which question do I act on now**. The third is the hardest and the one that matters.
- [ ] Settle what each row shows
      Today: state · id · title · open-comment badge · owner · completion coloring. Enough? Too much?
- [ ] Settle sort and grouping rules
      Today it is purely the hand-written `## Roster` order. Should "by state", "by completion", "open comments first" exist?
- [ ] Settle how completion coloring reads
      Today white→green by tick ratio. ⏸️ ON HOLD also renders full — easily misread as "done".
- [ ] A zero-background person points at the right question within three seconds
      Same acceptance as `QA4`: a fresh agent sees only the front page, is asked "which question to act on", and must answer correctly.

## Where we are
**It "can be viewed" but is not "usable" — the front page has never been treated as a design problem.**

- What it looks like today
  Board name + spine + close condition + progress bar + two global fold-outs (what is this board / how are the Qs ordered) + the list in `## Roster` order.
- What each row has today
  State badge · id · title · open-comment badge · owner · row tinted white→green by completion (`--fill`, percentage in `title`).
- Known defects
  ⏸️ ON HOLD renders as full green like ✅ — reads as "done"; with many questions it is one long strip with no visible priority; group order is entirely hand-maintained in the Roster.

## Files
- `build.py`
  The index-rendering pass (`rows` / `frac_done` / the `.ir` CSS family). Changing this question starts here.
- `board.md`
  `## Roster` decides grouping and order — if sorting ever becomes automatic, this section's role must be redefined too.

## Log
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Opened: the QC group refocused from "needs JL's ruling" to "index and structure"; the front page becomes its own question (`QA4` owns only the single-question page; the index page had no owner)
