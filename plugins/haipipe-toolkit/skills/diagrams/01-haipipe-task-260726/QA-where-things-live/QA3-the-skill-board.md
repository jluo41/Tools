# ② This board: what is argued, and what leaves
state: 🟡 PARTIAL
owner: JL
method: argue here, graduate the Law into the skill, and keep the runtime free of any dependency on an open page

## Question
What belongs on this board rather than in the skill, and what happens to a ruling once it is made? A design board and the package it argues about hold two different kinds of truth, and the failure when they blur is specific: a rule that lives only here binds nothing, because no runtime reads a design page.

The mechanism that keeps them separate is graduation. A question reaches ✅ and its `## Law` is copied into `SKILL.md` or the right `ref/`, so the manual is exactly the sum of settled rulings, no more and no less. What stays here is the argument: why the rule is that way, what was tried, and what is still open.

The direction that is easy to get wrong is the other one. An unsettled page must NOT be copied into the skill, because a convenient improvisation written into a manual becomes a rule nobody chose. So the board's job is as much to hold things back as to hand them over.

## Boundary
- ✅ Covered here
  What this board is for, what graduates and where to, and the dependency the runtime may never have on it.
- ↪ Covered elsewhere
  What ships is `QA2`; the map that places this folder is `QA1`; what a board IS belongs to `01-boardform-260722`. The paper family's version of this face is `QA3@paper` and the two are deliberately the same argument.

## Diagram
```
   THE GRADUATION MECHANISM

   ② this board                                    ① the skill
   ┌─────────────────────────┐   a Q hits ✅   ┌─────────────┐
   │ Question · why it is hard   │ ──────────▶ │ the Law only,  │
   │ Content  · the argument      │   its ## Law   │ in the place    │
   │ Items    · what is still owed │   is COPIED    │ that place is   │
   │ Law      · what was ruled     │                │ read from       │
   └─────────────────────────┘                └─────────────┘
       the WORKING RECORD                       SETTLED RULES ONLY
       keeps 🟡 and 🔴 too                     no more, no less

   ── where a Law lands, and it is not always SKILL.md ─────────
      an operating rule        → SKILL.md
      a folder or naming spec  → ref/hierarchy.md · ref/task-structure.md
      a code convention        → ref/authoring-conventions.md
      an engine specific       → that specialist's OWN ref/, never here
      a QA-file rule           → fn/qa.md — and see the caution below

   ── the one-way rule ──────────────────────────────────
      ✗ ① ──▶ ②   a runtime skill must never need an open Q page.
                 Delete this board and every skill still runs.

   ── ⚠️ the QA file is NOT ours to rule ────────────────────
      its state line is QC1@probe, its checker is QC2@probe.
      We write QA files; ⑥ rules what one IS. A Law here that
      restates that contract will drift from it.       → QD1
```

## Content
### What this board is for, in one line
To argue the questions the package cannot answer by running, and to hand the answers over in a
form a runtime can read. Everything else it holds is history, which is worth keeping and is not
the point.

### The two directions, and which one actually goes wrong
Graduation, the settled-to-manual direction, is easy to remember because the ruling is fresh.
What is easy to skip is the reverse discipline: NOT writing the unsettled thing down. An open
question with a plausible answer is exactly the thing that gets typed into a manual because it
reads well, and once there it is indistinguishable from a rule someone chose.

The board family has already recorded that failure: on the board tool's own board, a permission
rule was written as settled, shipped, and then overturned by JL. The page had been 🟡.

### The line this board must not cross
Half the questions here touch skills we do not own, and the rule that keeps that safe is narrow.
This board may rule what `/haipipe-task` DOES, including that it calls `/haipipe-board` (`QA4`).
It may not rule what a board IS, what a probe IS, or what a QA file IS. Those are `④`, `⑥` and
`⑥` again, and a Law here that restates one of them creates two authorities for one rule, which
is worse than having none.

## Items to Finish
- [ ] 🎓 State the graduation targets explicitly
      Five destinations are listed in the Diagram. Whether that list is closed, and who decides when a Law does not fit any of them, is not written.
- [ ] 🚫 Verify the one-way rule holds today
      "Delete this board and every skill still runs" is checkable: no `SKILL.md`, `ref/` or `fn/` file may reference a path under `diagrams/`. It has never been checked.
- [ ] 🔗 List what this board consults and may not write
      `④` boardform, `⑥` probe-qa. Both are linked from `board.md`; neither relationship is stated as a rule anywhere.
- [ ] 🧪 Graduate the first Law
      Nothing has graduated yet, because nothing is ✅. The first one will show whether the destination list above survives contact.

## Where we are
The board is one day old and nothing has graduated. Nineteen faces exist, all 🔴 or 🟡, and the
mechanism above is stated rather than exercised.

- 260726 CC · 🌱 Opened
      Modelled on `QA3@paper`, which states the same mechanism for the paper family. The one addition here is the caution about the QA file, because this family WRITES QA files while a different board RULES them, and that split has no counterpart on the paper side.

## Files
- `SKILL.md`
  The main graduation target: operating rules.
- `hierarchy.md`
  The graduation target for anything about folders, levels, naming or indexing.
- `authoring-conventions.md`
  The graduation target for code conventions: the four sisters, `_meta`, the heavy-artifact rule.

## Log
260726 · Created with the board.
