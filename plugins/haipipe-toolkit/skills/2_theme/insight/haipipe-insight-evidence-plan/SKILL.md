---
name: haipipe-insight-evidence-plan
description: >-
  Plan the evidence for one InsightBoard question before any run: turn its
  "What would answer it" into evidence needs (E1, E2, … each compute, cite or
  judge, with a pass condition) and give every compute need its work spec
  (cut, unit, measure, grouping, uncertainty, rivals, output columns), written
  on its register row for an independent reviewer agent to agree. The Insight workbench's "Plan the evidence" run. Never names a task
  or a file and never answers. Trigger: plan the evidence, evidence needs,
  what would answer it, needs for this question, plan needs, backfill needs,
  /haipipe-insight-evidence-plan.
allowed-tools: Read, Edit, Grep, Glob
metadata:
  version: "0.4.0"
  last_updated: "2026-10-02"
  # version history: ./CHANGELOG.md
---

# /haipipe-insight-evidence-plan · say what would answer it, before any run

The contract is `../haipipe-insight/ref/evidence-needs.md`; read § 1 and § 5
first. This skill writes one question's need lines on its register row
(`haipipe-insight-question` owns the row; this is its planning step).

## Input

One question id on one board, read as the question layer: its short question,
name, **The ask**, **Why now** (what waits on it, what it replicates),
**What would answer it**, any **Expected**, and the needs it already has. In an
Insight Block this is the question's `question.md` (`ref/block-contract.md`); on
a register board, its register division. Also MT00 or `meta/meta.md` (which
fields the extract carries) and the needs already planned on lower questions
it may borrow from.

**Plan from the question, not from its ask alone.** Why now says what the
answer is for; What would answer it says, in the asker's words, what counts.
The needs follow those two. A question that already has needs keeps them
(carried, or agreed earlier): this skill adds a need only where What would
answer it names evidence no need gives, and proposes any other change for the
question review (`haipipe-insight-question` GI1) instead of making it. The
blind-drafter rule (step 7: no task, config or result read while planning)
applies to a question that has no needs yet.

## Steps

1. **Read What would answer it as the list of evidence.** Each piece of
   evidence it names (a number, a table, a comparison, a test) is one need, at
   most one thing each; usually one to four. A word of the ask that no need
   reaches is not covered by adding a need: it is a review note (is the ask one
   question?). A cause word in a Data or Information ask is a review note too
   (Q4); the review proposes the rewording and a person signs it.
2. **Mark the forcing words.** "with its uncertainty", "interval", "adjusted
   for", "rather than <rival>", "held-out", "smallest", "how much would X
   gain", "separate A from B", "survive in every stratum": each is a
   `compute` need at the question's level. Existing pages never turn one of
   these into reasoning.
3. **Name each rival as its own need.** At Knowledge, a rival the ask or the
   board names ("category rather than age") is a compute need for the
   adjusted contrast, not a sentence to argue.
4. **Borrow, don't redo.** A need a lower question already plans is a `cite`
   with `from: <QID>.E<n>`, within the level rule (same level or one below).
5. **Close with the reading.** At Knowledge and Wisdom, the claim, strength
   and boundary (or the counsel) is a `judge` need `from:` the needs above it.
6. **Write `pass:` so a null passes.** It names what the result must contain
   (an interval, an adjustment, a held-out split, a size), never the answer.
7. **Write the work spec of every compute need, from the ask alone.** On the
   indented lines under the need: `cut:` (a partition, `the cell's
   partition`, or `cross`), `unit:` (what one row is), `measure:`, `by:` (the
   grouping or the contrast), `uncertainty:` (the interval or test), `rivals:`
   (adjusted for, or `none`), `output:` (`<file>.csv [<column>, …]`, several
   joined by ` ; `; on a Prototype, the YAML map `output: {<file>: [<column>, …]}`).
   The spec computes what What would answer it names and nothing beside it.
   The output files are named for the measure, never for a
   task. This is the run proposal, written from the register and the
   extract's column list alone: the drafter has not read the tasks, configs or
   results, and binding decides afterwards whether code already computes it.
8. **Write the lines and leave agreement open.** Under the paragraph:
   `- E<n> · <kind> · <what> · pass: <…> | from: <…>` with its spec lines, then
   `**Needs agreed**: ⬜` (on a Prototype, the `needs:` map and `agreed: ⬜`). A different agent that did not draft them reviews and
   agrees them, recorded as `✅ <YYMMDD>` with no name or initials (a board is
   public); this skill never agrees its own plan.

## Rules

- One need, one thing; usually one to four. A need the extract cannot carry
  (no field measures it) is still planned, as a compute need against the
  column inventory: "no measure exists" is an answer.
- Never name a task, a config or a ticket, and never read one while planning:
  binding is `haipipe-insight-bind`. A spec shaped by an existing task is the
  failure this skill exists to prevent.
  The spec names only its own output file and columns. Never state or hint the
  answer.
- A refusal is planned as a compute need too: its spec is the probe that
  would show the absence (a column inventory, a classification of the text).
- A compute need on a Wisdom question is misrouted: propose a Knowledge
  successor (`haipipe-insight-question`) instead of planning it.
- Frozen once bound: after a bound result exists, change a need by appending
  `· retired: <reason>` and adding a new id, never by editing it.
- Backfill on an old board: plan from the existing prose, keep the prose, and
  flag each forcing word the current answering page did not compute.

## Output

The edited register division and one log line in
`<register>/draft/records/<register-stem>-log.md` naming the question, the
needs added and who asked. Return the need lines in chat for the person to
agree.
