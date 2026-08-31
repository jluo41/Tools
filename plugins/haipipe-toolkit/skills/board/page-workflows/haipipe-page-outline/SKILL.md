---
name: haipipe-page-outline
description: >-
  The OUTLINE phase of a Board Page, phase ①: one pass that agrees the page's
  shape before a word of it is written. Reads the requirement, the routed
  feedback and the Page Type's outline mode; writes the versioned plan, the
  open threads and one log record; runs five checks; ends on a person's
  `approved:` tick. Trigger: page outline, OUTLINE phase, plan the page,
  outline pass, approve the outline, fold evidence into the plan,
  /haipipe-page-outline.
metadata:
  version: "0.12.0"
  last_updated: "2026-08-31"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-outline · one pass that agrees the shape before the prose

Load, in this order: `haipipe-page` (the base), the Page Type's `outline:`
block, this file, then `haipipe-plugin-outline/ref/plan-grammar.md` for the
file's grammar. Nothing else before the page itself. The plugin skill, the
sibling pages and board-wide checker output are not loaded.

## ⚡ Brief

```text
Q        what will this page say, division by division, bullet by bullet,
         and what does each bullet still owe?
READS    outline/<stem>-requirement.md (V1 to V4) · outline/<stem>-feedback.md
         (open rows) · outline/<stem>-evidence.md (owed, landed) · the Page
         Type's outline: mode · the page · the current plan
WRITES   outline/<stem>-outline-v<N>.md · outline/<stem>-discussion.md (D<nn>)
         · outline/<stem>-log.md (one record) · never the page
CHECKS   ⓪ ARC ① COVERAGE ② ADDRESS ③ VALUE ④ SHAPE, all pass before the
         person is asked
ENDS     a person ticks approved: (or a chat approval is transcribed with
         the quote)
WALLS    writes no prose · raises no card · dispatches no question · mints
         no Aim · names no division the type refuses · ticks nothing ·
         changes a ✅ plan only as v<N+1>
ROUTES   🧑 LOOK after every pass, then ② PROBE (a new question) · ③ EVIDENCE
         (an existing card or a landing gap) · ④ DRAFT (approved, nothing
         owed) · OUTLINE again · HOLD (the person is unavailable)
RECEIPT  §🧾, one block per pass; field law:
         ../haipipe-page-workflow/ref/page-run-contract.md §Receipt step
```

## ⓪ Boot · load little, trust the plan

- **Load**: this brief, the Page Type's `outline:` block (`fixed` lists the
  divisions · `grammar` fixes a first-word set and an order rule · `resolved`
  points at a source outside the type · no key means the base section order),
  `ref/plan-grammar.md`, the page, and the seven files under `outline/`. The
  `outline:` block sits in the type's SKILL.md frontmatter, which the Skill
  tool strips: read the file's first 20 lines with the Read tool. Read the
  page once, with the Read tool; a page piped through `cat` into a persisted
  output is read twice.
- **Trust the plan's `Answered:` and `Drawn:` lines as written.** Re-read only
  a card whose line ends `· recount` (it counts the run's own artifacts), plus
  one spot-check; a mismatch there means the plan is stale, and the route is
  this phase again, never a quiet correction.
- **In session or as an agent, the trace is the same**: the plan file, the
  log record, the receipt. `haipipe-page-outline-agent` runs the pass in a
  fresh context when the RUN loop dispatches it; a pass typed in a person's
  own session is equally a pass.

## ① Prepare · one command runs the mechanical half

```bash
python3 <haipipe-board>/cli/outline-pass.py <page>.md
```

It regenerates the three derived files, runs the plan checks for this page
(hard), runs `cli/check.py` scoped to the page, rebuilds the board (skip with
`--no-build`) and prints a receipt-lite. Run it TWICE: once before the plan is
written, to read; once after, to measure, because the evidence counts and the
checks describe the plan on disk. The log record is written after the second
run, so its folded receipt carries measured numbers:

```text
requirement  V1 Shape · V2 Size · V3 Refused · V4 Moves   read before a bullet is written
feedback     n routed · n open · n served · n declined     an open row is served or declined this pass
evidence     owed n · landed n · accepted n                what the fold appends
checks       plan-shape-off-type · bullet-missing-note · plan-no-arc ·
             feedback-unserved · head-too-long · head-too-short ·
             note-too-long · note-quotes-page · serves anchors   0 ❌ before the tick
tab          🧭 chips rebuilt                               open it and look
```

Run by hand, it is the three generators (`cli/requirement.py`,
`cli/feedback.py collect`, `cli/evidence-status.py`), the plan checks
(`src/plan_shape.py`, as `checks/outline.py --boards <board>` runs them),
`cli/check.py <board>`, and `cli/build.py <board>`.

## ② Plan · the type gives the words, this pass gives the argument

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
  the budget; a division V3 refuses fails ④ here and never reaches DRAFT.
  Terms are defined inline the first time; the plan never quotes the
  sentence it plans.
- **A hole is marked, never answered.** `📮` on the bullet that owes it;
  `🖼 owed · <kind>` on the one that owes a figure. A plan that already knows
  every answer was written after the fact.
- **The fold appends to the bullet that asked.** A landed value becomes
  `Answered:`, a built unit's README claim becomes `Drawn:`, a served Round
  row becomes `Routed:`; never a new bullet, never an edit to the head.
- **An older-grammar plan is rewritten into the current grammar on this
  pass**: in place while ⬜, as `v<N+1>` after a tick.

## ③ Threads and the log record

- **Every open ask becomes a `D<nn>` record** in `outline/<stem>-discussion.md`
  (Ask · Options · We lean · Decide), id allocated board-wide
  (`ref/record-shape.md`); a settled one is a log record. An ask with no Aim
  is a thread, never a minted Aim.
- **Every open feedback row is served or declined**: `Routed: <RD> <row id>`
  on the bullet that serves it, or `declined: <RD> <row id> · <reason>` in the
  plan head. `check.py` reports `feedback-unserved` on a row with neither.
- **One log record per pass**: `### YYMMDD HHMM · OUTLINE v<N>: <what changed
  in one line>`, the receipt folded under it when no run folder holds it.

## ④ Five checks, before the person is asked

```text
⓪ ARC       arc: present and an argument · adjacent pairs pass the swap test ·
            the heaviest finding has a division
① COVERAGE  every owing mark is served by a card or unit, or is bare and
            counted as owed in the receipt (② PROBE has not run yet) · every
            unit on disk is cited or retired · every open feedback row is
            served or declined
② ADDRESS   every card's serves: names an address this plan has
③ VALUE     every 🧮 number recomputes (checks/values.py)
④ SHAPE     divisions match the type's mode · heads 4 to 11 words · Notes
            ≤ 30 words · no Note quotes the page · nothing V3 refuses
```

Any ❌ is fixed in the plan here; the person is not asked yet. ⓪ is half a
judgment: `arc:` present is mechanical, whether it argues is this pass's call
and the person may overturn it at the tick.

## 🧑 The tick ends the phase

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

## 🔀 Routes

```text
any of the five ❌                     fix the plan here; no LOOK yet
five pass, a new Task/Discovery ask    🧑 LOOK, then ② PROBE (never skipped)
five pass, an existing card or a
  citation/display landing gap         🧑 LOOK, then ③ EVIDENCE
five pass, nothing owed, approved ✅   ④ DRAFT
approved ⬜, person unavailable        HOLD
the Page Type refuses the shape        fix the plan, never the type, unless the
                                       mismatch is a real finding against the type
```

OUTLINE never routes to REVISE.

## 🧾 Receipt

```text
phase: OUTLINE
file: <page>/outline/<stem>-outline-v<N>.md
supersedes: v<N-1> | none
requirement: V1 V2 V3 V4 read ✅
feedback: n routed · n served · n declined
evidence: owed n · landed n · accepted n
checks: ⓪ ✅ ① ✅ ② ✅ ③ ✅ ④ ✅
counts: divisions · paragraphs · bullets · marks by kind
threads: D<nn> opened … · D<nn> settled …
approved: ✅ <who> <date> | ⬜ waiting
next: OUTLINE | PROBE | EVIDENCE | DRAFT | HOLD
```

## 📂 Files

```text
haipipe-page-outline/
├── SKILL.md            this phase
└── CHANGELOG.md        version history, and the only home for what this phase used to say
```

Owns no scripts. The base is `haipipe-page`; the folder, the tab and the plan
grammar are `haipipe-plugin-outline`'s (`ref/plan-grammar.md`,
`ref/record-shape.md`, `ref/specimen-section-plan.md`); the loop and the
receipt law are `haipipe-page-workflow`'s; the six-field card of every phase
is `../haipipe-page-workflow/ref/phase-cards.md` §①; the next phase is
`haipipe-page-draft`. The design page is `QPw1-outline` on
`BoardSkillBoard-260722`.
