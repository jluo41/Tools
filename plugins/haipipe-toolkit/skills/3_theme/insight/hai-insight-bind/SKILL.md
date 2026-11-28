---
name: hai-insight-bind
description: "Binds the work for one answering page of an InsightBoard: for each evidence need, finds or commissions the task output, runs the page's ticket and records the binding in answers.yaml. Use for the workbench's Bind the work run. Trigger: bind the work, bind needs, answers.yaml, /hai-insight bind."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
disable-model-invocation: true
metadata:
  version: "0.2.2"
  last_updated: "2026-10-26"
  # version history: ./CHANGELOG.md
---

# /hai-insight bind · each need to the narrowest file that answers it

The contract is `../hai-insight/ref/evidence-needs.md`; read § 2 and § 5
first. Tickets and results follow `../hai-insight/ref/report.md`.

## Input

One answering page (`<n>-<segment>/<L><NN>-<segment>-<slug>/`), the
register rows of the questions its cells name, their agreed needs, and the
Project's DIKW task Block (`work/b5N_<topic>_dikw/`).

## Steps

1. **List the needs and their specs.** Every live need of every question the
   page answers, with each compute need's work spec. A compute need without a
   spec goes back to `hai-insight-evidence-plan`: nothing is bound before
   the spec exists. Unagreed needs may be bound; say so in the reply.
2. **compute · match the spec exactly.** Read the Block's task pages, configs
   and the outputs their workers declare, against the spec, in this order:
   the segment (the config's `population`), the unit (what one row is), the
   measure, the grouping or contrast, the uncertainty, the rivals, then the
   spec's output file and columns. A run fits only when every item matches. A
   run on the same topic that misses one does not fit, however close.
3. **compute · nothing fits.** A run fits only if its config serves this
   question alone and it already writes the proposed files and columns, with
   nothing the ask does not name (`hai-insight` ref/evidence-needs.md, hard
   rules 1 and 5). Otherwise give the question its own run: a new config of an
   existing task when that task's code computes exactly the proposal, else a
   new task built from the proposal in the level's Job (`j3N_knowledge_<topic>`
   for a Knowledge test), through `hai-task`. Never extend another
   question's run with a column or a grouping to make it fit. New computation
   runs only once an independent reviewer agent has agreed the need's spec; the
   bind step never releases its own work.
4. **A refusal gets a probe run.** A need that will be refused ("no field",
   "never varied") is bound to the run that shows the absence; write its
   `refused:` reason beside that `ticket` and its `files`.
5. **Ticket and run.** Write the page ticket
   `runs/run_bNNjNNtNNrNN_<segment>_<task>.sh` (it sets `RESULT_DIR` and
   `RUN_TICKET` and execs the task's own ticket) and run it. The result is
   generated; never edit it.
6. **Write `answers.yaml`.** compute: `ticket` and `files` (every spec output
   file; an optional `fields:` adds columns beyond the spec's). cite: `pages`,
   or omit to use the register's page for the cited question on this
   segment. judge: `judge`. refused: `refused:` plus the probe's `ticket`
   and `files`, only for a cell that will settle 🟡 or 🚫.
7. **Sync the configs.** Run `ref/sync_config_answers.py <board>`: it rewrites
   each called config's `answers:` line to the need ids the board's
   `answers.yaml` files bind to it (`answers: [QK2.E1, QI4.E1]`). The page's
   `runs:` header lists its tickets.
8. **Check.** Run `hai-insight-check` for the page. Report each need's
   binding and any GAP left; a GAP for an uncited need is expected until the
   page is written through `hai-draft` (`hai-insight` `ref/report.md`).

## Rules

- Never answer a compute need by pointing at another page's prose: that is a
  GAP, not a cite. A cite binds a need the other page itself binds.
- Never fit the spec to an existing run: when they disagree, the run changes or
  a new one is built; the spec changes only through a retired need and a new id.
- One run, one question: a run serves the needs of one question, on every page
  that answers it; a second question gets its own run, even from the same code.
- Never write the page's text, its `results-read:` line or a register cell.
- Aggregate output only; heavy output goes to `HEAVY_DIR` with a `heavy.yaml`
  pointer (the SPACE's AGENTS.md § Working rules).

## Output

The page's `answers.yaml`, any new `runs/` tickets and their generated
`results/<ticket>/`, the synced `runs:` header, and a reply listing each need
with its file or its blocker.
