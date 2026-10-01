---
name: haipipe-insight-bind
description: >-
  Bind the work for one answering page of an InsightBoard: for each evidence
  need of the questions the page answers, find the task output that computes
  exactly that need (or commission one through haipipe-task), write the page's
  runs/ ticket, run it, and record the binding in the page's answers.yaml.
  The Insight workbench's "Bind the work" run. Never writes the page's prose
  and never settles a cell. Trigger: bind the work, bind needs, answers.yaml,
  which run answers this need, wire the page to its runs,
  /haipipe-insight-bind.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.0"
  last_updated: "2026-10-01"
  # version history: ./CHANGELOG.md
---

# /haipipe-insight-bind · each need to the narrowest file that answers it

The contract is `../haipipe-insight/ref/evidence-needs.md`; read § 2 and § 5
first. Tickets and results follow `../haipipe-insight/ref/report.md`.

## Input

One answering page (`<n>-<partition>/<L><NN>-<partition>-<slug>/`), the
register rows of the questions its cells name, their agreed needs, and the
Project's DIKW task Block (`tasks/b5N_<topic>_dikw/`).

## Steps

1. **List the needs.** Every live need of every question the page answers.
   Unagreed needs may be bound; say so in the reply.
2. **compute · search before building.** Read the Block's task pages and
   configs and the outputs their workers declare. A need is met by a file
   only when its columns or keys carry what `pass:` names: an interval when
   the need asks uncertainty, an adjusted rate when it asks adjustment, a
   held-out score when it asks prediction. A file about the same topic that
   lacks them does not fit.
3. **compute · nothing fits.** Propose the smallest change: a grouping added
   to an existing config, a new config of an existing task, or a new task in
   the rung's Job (`j3N_knowledge_<topic>` for a Knowledge test), through
   `haipipe-task`. New computation is released by a person; stop for that
   release, never infer it.
4. **Ticket and run.** Write the page ticket
   `runs/run_bNNjNNtNNrNN_<partition>_<task>.sh` (it sets `RESULT_DIR` and
   `RUN_TICKET` and execs the task's own ticket) and run it. The result is
   generated; never edit it.
5. **Write `answers.yaml`.** compute: `ticket`, `files` (the narrowest files,
   `<table>_by_<grouping>.csv` rather than the whole result) and `fields`
   (the columns or dotted JSON keys that carry `pass:`). cite: `pages`, or
   omit to use the register's page for the cited question on this partition.
   judge: `judge`. refused: a reason, only for a cell that will settle 🟡 or 🚫.
6. **Sync the header.** The page's `runs:` line lists its tickets; the called
   configs' `answers:` lists are re-derived from the board's `answers.yaml`
   files (a cross-check, never the join).
7. **Check.** Run `haipipe-insight-check` for the page. Report each need's
   binding and any GAP left; a GAP for an uncited need is expected until the
   page is written.

## Rules

- Never answer a compute need by pointing at another page's prose: that is a
  GAP, not a cite. A cite binds a need the other page itself binds.
- Bind where the answer is: one run may serve many needs and many pages.
- Never write the page's text, its `results-read:` line or a register cell.
- Aggregate output only; heavy output goes to `HEAVY_DIR` with a `heavy.yaml`
  pointer (AGENTS.md rule 10).

## Output

The page's `answers.yaml`, any new `runs/` tickets and their generated
`results/<ticket>/`, the synced `runs:` header, and a reply listing each need
with its file or its blocker.
