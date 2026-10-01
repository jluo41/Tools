---
name: haipipe-insight-evidence-plan
description: >-
  Plan the evidence for one InsightBoard question before any run: turn its
  "What would answer it" into evidence needs (E1, E2, … each compute, cite or
  judge, with a pass condition), written on its register row for a person to
  agree. The Insight workbench's "Plan the evidence" run. Never names a task
  or a file and never answers. Trigger: plan the evidence, evidence needs,
  what would answer it, needs for this question, plan needs, backfill needs,
  /haipipe-insight-evidence-plan.
allowed-tools: Read, Edit, Grep, Glob
metadata:
  version: "0.1.0"
  last_updated: "2026-10-01"
  # version history: ./CHANGELOG.md
---

# /haipipe-insight-evidence-plan · say what would answer it, before any run

The contract is `../haipipe-insight/ref/evidence-needs.md`; read § 1 and § 5
first. This skill writes one question's need lines on its register row
(`haipipe-insight-question` owns the row; this is its planning step).

## Input

One question id on one board: its register division (**The ask**, **Why
now**, **What would answer it**, **Expected**), MT00's inventory (which fields
the extract carries), and the needs already planned on lower questions it may
borrow from.

## Steps

1. **Read the ask as a list of things to produce.** Each clause that names a
   number, a table, a comparison or a test is one need.
2. **Mark the forcing words.** "with its uncertainty", "interval", "adjusted
   for", "rather than <rival>", "held-out", "smallest", "how much would X
   gain", "separate A from B", "survive in every stratum": each is a
   `compute` need at the question's rung. Existing pages never turn one of
   these into reasoning.
3. **Name each rival as its own need.** At Knowledge, a rival the ask or the
   board names ("category rather than age") is a compute need for the
   adjusted contrast, not a sentence to argue.
4. **Borrow, don't redo.** A need a lower question already plans is a `cite`
   with `from: <QID>.E<n>`, within the rung rule (same rung or one below).
5. **Close with the reading.** At Knowledge and Wisdom, the claim, strength
   and boundary (or the counsel) is a `judge` need `from:` the needs above it.
6. **Write `pass:` so a null passes.** It names what the result must contain
   (an interval, an adjustment, a held-out split, a size), never the answer.
7. **Write the lines and leave agreement open.** Under the paragraph:
   `- E<n> · <kind> · <what> · pass: <…> | from: <…>`, then
   `**Needs agreed**: ⬜`. A person writes `✅ <initials> <YYMMDD>`; this skill
   never does.

## Rules

- One need, one thing; usually one to four. A need the extract cannot carry
  (no field measures it) is still planned, as a compute need against the
  column inventory: "no measure exists" is an answer.
- Never name a task, a config, a ticket or a file: binding is
  `haipipe-insight-bind`. Never state or hint the answer.
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
