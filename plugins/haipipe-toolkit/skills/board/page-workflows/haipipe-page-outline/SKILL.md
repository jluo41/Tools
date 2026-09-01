---
name: haipipe-page-outline
description: >-
  The OUTLINE phase of a Board Page and the THINKING half of its OUTLINE part:
  two cycles, SHAPE (brief → propose → react → revise until a person ticks
  `approved:`) and SURVEY (one row per evidence mark in the item table: what is
  owed, which run in tasks/ answers it, how far up the tree the gap sits, and a
  person's Decide). Writes the versioned plan, the item table, the open threads
  and one log record; never raises a card, never lands material. Trigger: page
  outline, OUTLINE phase, shape the plan, survey the items, item table, approve
  the outline, fold evidence into the plan, /haipipe-page-outline.
metadata:
  version: "0.13.0"
  last_updated: "2026-09-01"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-outline · SHAPE the plan, then SURVEY what it owes

Load, in this order: `haipipe-page` (the base), the Page Type's `outline:`
block, this file, then `haipipe-plugin-outline/ref/plan-grammar.md` for the
plan's grammar and `ref/item-table.md` for the table's. Nothing else before
the page itself. The plugin skill, the sibling pages and board-wide checker
output are not loaded.

The page workflow has two PARTS (haipipe-page-workflow §🔁): the OUTLINE part
decides what is true and what the page will therefore say; the DRAFT part
writes it. This phase owns the OUTLINE part's two HUMAN-gated cycles; its
sibling `haipipe-page-evidence` owns the two machine-gated ones (LAND, EMBED).

```text
OUTLINE part
  SHAPE    this file    brief → propose → react → revise      👤 approved:
  SURVEY   this file    the item table: Need · Route · Run     👤 Decide, per row
  LAND     evidence     make the runs, fill the lanes          ⚙ every make-row landed
  EMBED    evidence     fold the numbers into plan v<N+1>      ⚙ back to SHAPE
```

## ⚡ Brief

```text
Q        what will this page say, division by division, bullet by bullet;
         what does each bullet owe; and where in tasks/ does each owed thing
         come from?
READS    outline/<stem>-requirement.md (V1 to V4) · outline/<stem>-feedback.md
         (open rows) · outline/<stem>-evidence.md (the table joined to the
         disk) · the Page Type's outline: mode · the page · the current plan ·
         the project's tasks/ tree (SURVEY only)
WRITES   outline/<stem>-outline-v<N>.md · outline/<stem>-items.md (SURVEY) ·
         outline/<stem>-discussion.md (D<nn>) · outline/<stem>-log.md (one
         record) · never the page
CHECKS   ⓪ ARC ① COVERAGE ② ADDRESS ③ VALUE ④ SHAPE, all pass before the
         person is asked (SHAPE); every mark has a row with an outcome and an
         address where one exists (SURVEY)
ENDS     SHAPE: a person ticks approved: (or a chat approval is transcribed
         with the quote) · SURVEY: every row carries a signed Decide
WALLS    writes no prose · raises no card · dispatches nothing · runs nothing ·
         mints no Aim · names no division the type refuses · ticks nothing ·
         changes a ✅ plan only as v<N+1> · never writes a Status word
ROUTES   SHAPE → SURVEY (approved, marks owed) · SHAPE → the DRAFT part
         (approved, every row folded) · SURVEY → LAND (every row decided) ·
         either → SHAPE again · HOLD (the person is unavailable)
RECEIPT  §🧾, one block per pass, `cycle: SHAPE | SURVEY`; field law:
         ../haipipe-page-workflow/ref/page-run-contract.md §Receipt step
```

## ⓪ Boot · load little, trust the plan

- **Load**: this brief, the Page Type's `outline:` block (`fixed` lists the
  divisions · `grammar` fixes a first-word set and an order rule · `resolved`
  points at a source outside the type · no key means the base section order),
  `ref/plan-grammar.md`, the page, and the eight files under `outline/`. The
  `outline:` block sits in the type's SKILL.md frontmatter, which the Skill
  tool strips: read the file's first 20 lines with the Read tool. Read the
  page once, with the Read tool; a page piped through `cat` into a persisted
  output is read twice.
- **Trust the plan's `Answered:` and `Drawn:` lines as written.** Re-read only
  a card whose line ends `· recount` (it counts the run's own artifacts), plus
  one spot-check; a mismatch there means the plan is stale, and the route is
  this phase again, never a quiet correction.
- **In session or as an agent, the trace is the same**: the plan file (or the
  table), the log record, the receipt. `haipipe-page-outline-agent` runs the
  pass in a fresh context when the RUN loop dispatches it; a pass typed in a
  person's own session (the 🎨 Studio chat) is equally a pass.

## 🧩 SHAPE · brief → propose → react → revise, until the shape is agreed

The cycle where the human and the AI shape the plan together. Named for what
BOTH sides do; it ends when the shape is agreed, never earlier.

```text
1 BRIEF     the person says the narrative in a few lines: what this page must argue
2 PROPOSE   the AI writes plan v1 from the brief + the type's outline: block + the
            venue's requirement; every owed thing is a MARK, nothing else exists yet
3 REACT     the person reads the rendered plan on the 🧭 tab: ticks, comments, redirects
4 REVISE    the AI folds the rulings into v2
loop 3 ⇄ 4 until the person ticks approved:
```

Steps 2 and 4 are the chat's verbs (`propose`, `revise`); step 3 is the person
on the 🧭 tab. "Draft" and "Brief" are not cycle names: DRAFT is the second
part of the workflow, and Brief is the design family's D0.

### ① Prepare · one command runs the mechanical half

```bash
python3 <haipipe-board>/cli/outline-pass.py <page>.md
```

It regenerates the three derived files, runs the plan checks for this page
(hard), runs `cli/check.py` scoped to the page, rebuilds the board (skip with
`--no-build`) and prints a receipt-lite. Run it TWICE: once before the plan is
written, to read; once after, to measure, because the counts and the checks
describe the plan on disk. The log record is written after the second run, so
its folded receipt carries measured numbers:

```text
requirement  V1 Shape · V2 Size · V3 Refused · V4 Moves   read before a bullet is written
feedback     n routed · n open · n served · n declined     an open row is served or declined this pass
evidence     cycle: … · items n · decided n/n · <ladder tally>   what the table says
checks       plan-shape-off-type · bullet-missing-note · plan-no-arc ·
             feedback-unserved · head-too-long · head-too-short ·
             note-too-long · note-quotes-page · serves anchors   0 ❌ before the tick
tab          🧭 chips rebuilt                               open it and look
```

Run by hand, it is the three generators (`cli/requirement.py`,
`cli/feedback.py collect`, `cli/evidence-status.py`), the plan checks
(`src/plan_shape.py`, as `checks/outline.py --boards <board>` runs them),
`cli/check.py <board>`, and `cli/build.py <board>`.

### ② Plan · the type gives the words, this pass gives the argument

- **Read the mode first.** `fixed`: fill the listed divisions, add none, drop
  none. `grammar`: choose how many of each first word, write the free title
  after it. `resolved`: resolve the source the type names; a missing source
  is a hole, never a licence to invent a shape or copy a sibling's.
- **One `## C<n>` per Content division of the page.** A flat Section page
  (one `### §1`) is one `C1` with `P1` to `P<n>`; the SM00 specimen has three
  because its page has three parts.
- **`arc:` is one sentence that argues.** Every adjacent pair of divisions
  (or, on a one-division page, of paragraphs) passes the swap test: name why N
  must precede N+1 ("Method before Result, or the number cannot be believed");
  a date, a run order or a config order is not a reason. The heaviest finding
  has its own division, or its own paragraph on a one-division page; a finding
  a reader cannot reach from the list is mis-weighted.
- **The Narrative row's order binds.** A Round's proposed reader order is an
  input served through that row; where the two differ, follow the row and
  open a `D<nn>` naming the Round's row, because the Narrative ratifies order
  changes, not a Section.
- **A Section page plans sentence slots.** One bullet per slot in the
  Narrative row's order; the venue's moves (V4) are the slots' jobs; V2 sets
  the budget; a division V3 refuses fails ④ here and never reaches the DRAFT
  part. Terms are defined inline the first time; the plan never quotes the
  sentence it plans.
- **A hole is marked, never answered.** `📮` on the bullet that owes a number
  or a fact; `🧮` on one that owes a recomputed value; `📚` a citation; `🖼
  owed · <kind>` on the one that owes a figure. A plan that already knows
  every answer was written after the fact.
- **The fold appends to the bullet that asked** (EMBED's write, read here): a
  landed value becomes `Answered:`, a built unit's README claim becomes
  `Drawn:`, a served Round row becomes `Routed:`; never a new bullet, never an
  edit to the head.
- **An older-grammar plan is rewritten into the current grammar on this
  pass**: in place while ⬜, as `v<N+1>` after a tick.

### ③ Threads and the log record

- **Every open ask becomes a `D<nn>` record** in `outline/<stem>-discussion.md`
  (Ask · Options · We lean · Decide), id allocated board-wide
  (`ref/record-shape.md`); a settled one is a log record. An ask with no Aim
  is a thread, never a minted Aim.
- **Every open feedback row is served or declined**: `Routed: <RD> <row id>`
  on the bullet that serves it, or `declined: <RD> <row id> · <reason>` in the
  plan head. `check.py` reports `feedback-unserved` on a row with neither.
- **One log record per pass**: `### YYMMDD HHMM · SHAPE v<N>: <what changed
  in one line>` (or `SURVEY: <n> rows …`), the receipt folded under it when
  no run folder holds it.

### ④ Five checks, before the person is asked

```text
⓪ ARC       arc: present and an argument · adjacent pairs pass the swap test ·
            the heaviest finding has a division
① COVERAGE  every owing mark is served by a table row, a card or a unit, or is
            bare and counted as owed in the receipt (SURVEY has not run yet) ·
            every unit on disk is cited or retired · every open feedback row is
            served or declined
② ADDRESS   every card's and every table row's address names a bullet this plan has
③ VALUE     every 🧮 number recomputes (checks/values.py)
④ SHAPE     divisions match the type's mode · heads 4 to 11 words · Notes
            ≤ 30 words · no Note quotes the page · nothing V3 refuses
```

Any ❌ is fixed in the plan here; the person is not asked yet. ⓪ is half a
judgment: `arc:` present is mechanical, whether it argues is this pass's call
and the person may overturn it at the tick.

### 🧑 The tick ends the cycle, and it carries the fork

- **A person reads the 🧭 tab and ticks `approved:`.** The job there is to
  BREAK the plan: the division that argues nothing, the figure that shows the
  wrong thing, the answer that dodges its ask. The tick means "I tried to
  break it and failed", the one meaning left after a machine checked the
  arithmetic.
- **A chat approval is transcribed, never decided**:
  `approved: ✅ JL 260831 0146 · in chat: "ok, good, I approve this outline"`.
  A machine writes `checked:` for itself and nothing more.
- **A tick belongs to the version it ticked.** Evidence that changes an
  approved plan makes `v<N+1>`; `v<N>` is kept, because it was right at its
  date.
- **The tick is where the OUTLINE part exits.** EMBED always returns here with
  plan v<N+1>; `approved:` with every table row `folded` releases the DRAFT
  part, `approved:` with fresh marks sends the page to SURVEY again. The
  machine never decides that the part is over.

## 🔍 SURVEY · one row per mark: where does it come from, how big is the gap

The cycle that makes the probe's old MATCH step VISIBLE and puts a person's
decision behind it (JL 260901: "the run should be the basic element … for
each evidence item, what are their current status, how large they will be").
It runs only on an approved plan, and it creates nothing on disk but the table.

- **The law it serves**: every evidence number is answered by a RUN, a real
  address in the project's `tasks/` tree; the run computes, and only the page
  interprets (at EMBED). `ref/item-table.md` carries the grammar; this section
  carries the pass.
- **Write `outline/<stem>-items.md`**: one record per marked bullet, head
  byte-identical to the plan's words (`### <address> · <mark> <head>`), four
  labels: **Need** (one line, what exactly is owed) · **Route** (`task ·
  discovery · bibex · display · pagex`) · **Run** (`<outcome> · <address>
  [· note]`) · **Decide** (`☐ make`, left for the person).
- **Find the run by READING, cheapest first**: this page's own earlier rows →
  the `tasks/` tree by block, job, task, run (their `QA/` digests and
  `results/` listings are the index) → nothing. Never guess an outcome from
  the question's shape; open the folder.
- **The outcome word names the gap's LEVEL** in the b/j/t/r grammar, so the
  cost reads off the word: `found` (results answer it) · `rerun` (run exists,
  results missing or stale) · `new-run` (task exists, mint an `r<NN>_` config)
  · `new-task` · `new-job` · `new-block` (scaffold that level first) ·
  `person` (a citation, or a fact only a person holds) · `none` (no run could
  ever produce it: the bullet is wrong, and the row routes back to SHAPE, never
  to a Decide of make).
- **Citations are `person` for now.** The discoveries/ tree joins the same
  grammar later (a discovery folder is the task, a sweep its run, `sources.md`
  its results); until that mapping lands, the person supplies the entry and
  LAND transcribes it verbatim (`haipipe-plugin-bibex`).
- **A row is complete** when it has its outcome, its address where one exists,
  and a signed Decide (`☑ make · JL 260901`, `☑ defer · <reason>`, `☑ drop ·
  <reason>`). The cycle's gate is every row complete; LAND refuses a `☐`.
- **The table replaces the card for light rows.** A card folder
  (`evidence/probe/PP<NN>-<slug>/`) exists only when a question has to LEAVE
  the page at LAND (an outbound `new-*` computation someone else runs); a
  `found` row lives entirely in its table row. Card states, the consumer /
  executor wall and the `PP<NN>.v<n>` value grammar stay `haipipe-plugin-probe`'s.

### 🧑 The Decide ends the cycle

A person reads the table on the 🧭 tab (the 🧾 Evidence lens, which renders
the table joined to the disk with a derived Status chip per row) and writes
one Decide per row. A machine may transcribe a chat decision with the quote;
it never ticks `☑` on its own. `cli/evidence-status.py` prints `cycle: SURVEY
· decided n/n` until every row is signed, then `cycle: LAND`.

## 🔀 Routes

```text
SHAPE  any of the five ❌                     fix the plan here; no tick yet
SHAPE  five pass, marks owed, approved ✅     SURVEY
SHAPE  five pass, every row folded, ✅        the DRAFT part (haipipe-page-draft)
SHAPE  approved ⬜, person unavailable        HOLD
SURVEY rows incomplete                        SURVEY (waiting on Decide) · HOLD
SURVEY every row decided                      LAND (haipipe-page-evidence)
SURVEY a row's outcome is none                SHAPE, naming the bullet
the Page Type refuses the shape               fix the plan, never the type, unless the
                                              mismatch is a real finding against the type
```

OUTLINE never routes to the DRAFT part's REVISE or CHECK.

## 🧾 Receipt

```text
phase: OUTLINE
cycle: SHAPE | SURVEY
file: <page>/outline/<stem>-outline-v<N>.md | <page>/outline/<stem>-items.md
supersedes: v<N-1> | none
requirement: V1 V2 V3 V4 read ✅
feedback: n routed · n served · n declined
items: n marks · n rows · decided n · by outcome: found n · rerun n · new-run n · … · none n
checks: ⓪ ✅ ① ✅ ② ✅ ③ ✅ ④ ✅        (SHAPE)
counts: divisions · paragraphs · bullets · marks by kind
threads: D<nn> opened … · D<nn> settled …
approved: ✅ <who> <date> | ⬜ waiting
next: SHAPE | SURVEY | LAND | DRAFT | HOLD
```

## 📂 Files

```text
haipipe-page-outline/
├── SKILL.md            this phase: the SHAPE and SURVEY cycles
└── CHANGELOG.md        version history, and the only home for what this phase used to say
```

Owns no scripts. The base is `haipipe-page`; the folder, the tab, the plan
grammar and the item table's grammar are `haipipe-plugin-outline`'s
(`ref/plan-grammar.md`, `ref/item-table.md`, `ref/record-shape.md`,
`ref/specimen-section-plan.md`); the two-part loop and the receipt law are
`haipipe-page-workflow`'s; the six-field card of every phase is
`../haipipe-page-workflow/ref/phase-cards.md`; the next phase is
`haipipe-page-evidence` (LAND, EMBED), and after the part exits,
`haipipe-page-draft`. The design page is `QPw1-outline` on
`BoardSkillBoard-260722`.
