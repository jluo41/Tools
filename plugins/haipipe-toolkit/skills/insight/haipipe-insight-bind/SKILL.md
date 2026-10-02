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
  version: "0.2.0"
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

1. **List the needs and their specs.** Every live need of every question the
   page answers, with each compute need's work spec. A compute need without a
   spec goes back to `haipipe-insight-evidence-plan`: nothing is bound before
   the spec exists. Unagreed needs may be bound; say so in the reply.
2. **compute · match the spec exactly.** Read the Block's task pages, configs
   and the outputs their workers declare, against the spec, in this order:
   the cut (the config's `population`), the unit (what one row is), the
   measure, the grouping or contrast, the uncertainty, the rivals, then the
   spec's output file and columns. A run fits only when every item matches. A
   run on the same topic that misses one does not fit, however close.
3. **compute · nothing fits.** A run fits only if its config serves this
   question alone and it already writes the proposed files and columns, with
   nothing the ask does not name (`haipipe-insight` ref/evidence-needs.md, hard
   rules 1 and 5). Otherwise give the question its own run: a new config of an
   existing task when that task's code computes exactly the proposal, else a
   new task built from the proposal in the rung's Job (`j3N_knowledge_<topic>`
   for a Knowledge test), through `haipipe-task`. Never extend another
   question's run with a column or a grouping to make it fit. New computation
   runs only once an independent reviewer agent has agreed the need's spec; the
   bind step never releases its own work.
4. **A refusal gets a probe run.** A need that will be refused ("no field",
   "never varied") is bound to the run that shows the absence; write its
   `refused:` reason beside that `ticket` and its `files`.
5. **Ticket and run.** Write the page ticket
   `runs/run_bNNjNNtNNrNN_<partition>_<task>.sh` (it sets `RESULT_DIR` and
   `RUN_TICKET` and execs the task's own ticket) and run it. The result is
   generated; never edit it.
6. **Write `answers.yaml`.** compute: `ticket` and `files` (every spec output
   file; an optional `fields:` adds columns beyond the spec's). cite: `pages`,
   or omit to use the register's page for the cited question on this
   partition. judge: `judge`. refused: `refused:` plus the probe's `ticket`
   and `files`, only for a cell that will settle 🟡 or 🚫.
7. **Sync the configs.** Run `ref/sync_config_answers.py <board>`: it rewrites
   each called config's `answers:` line to the need ids the board's
   `answers.yaml` files bind to it (`answers: [QK2.E1, QI4.E1]`). The page's
   `runs:` header lists its tickets.
8. **Check.** Run `haipipe-insight-check` for the page. Report each need's
   binding and any GAP left; a GAP for an uncited need is expected until the
   page is written through `haipipe-page` (`haipipe-insight` `ref/report.md`).

## Rules

- Never answer a compute need by pointing at another page's prose: that is a
  GAP, not a cite. A cite binds a need the other page itself binds.
- Never fit the spec to an existing run: when they disagree, the run changes or
  a new one is built; the spec changes only through a retired need and a new id.
- One run, one question: a run serves the needs of one question, on every page
  that answers it; a second question gets its own run, even from the same code.
- Never write the page's text, its `results-read:` line or a register cell.
- Aggregate output only; heavy output goes to `HEAVY_DIR` with a `heavy.yaml`
  pointer (AGENTS.md rule 10).

## Output

The page's `answers.yaml`, any new `runs/` tickets and their generated
`results/<ticket>/`, the synced `runs:` header, and a reply listing each need
with its file or its blocker.
