---
name: haipipe-insight-data
description: >-
  InsightBoard level contract for Data: what was observed in the board's one
  extract, from which exact run, with no interpretation. A Data question is
  answered by its page's ticket calling a task run; the results in the page's
  results/ are the evidence and the page says briefly what was observed. Use when a QD
  question needs its answering ticket or page. Trigger: insight
  data, observations, Data, folder-kind data, legacy page-type data,
  /haipipe-insight-data.
metadata:
  version: "2.3.0"
  last_updated: "2026-10-01"
  workflow: haipipe-insight-workflow
  folder_kind: data
  primary_face: task
  page_ruling: none
  legacy_page_type: data
  group-token: "D"
  report:
    shape: "headline → what was observed (counts, unit, window) → coverage and gaps"
---

# /haipipe-insight-data · record what was observed

Load `haipipe-insight` (`ref/board-contract.md`, `ref/report.md`,
`ref/evidence-needs.md`) and the workflow. `folder-kind: data` and `page-type: data` remain read-only keys for
boards made before page tickets.

## Position

Data answers a `QD` question after GI1 and supplies observations to
Information. It is answered by its page folder `<n>-<partition>/D<NN>-<partition>-<slug>/`:
the Work column is the page's `runs/` tickets and `results/`, and the Report
column is the page's `.md` (`ref/report.md`): for Data, a brief statement of what was observed.

## What a Data answer is

One coherent observation set: **what was observed and from which exact run**,
with its unit, window and coverage. It never computes a comparison, trend,
explanation, strength or recommendation; a ratio of two counts is
Information.

## The run · Work

- A task in the Project's DIKW Block, in a `j1N_data_<topic>` Job (extract
  shape, catalogs, balance checks). The task is dataset-neutral; one config
  per dataset × partition, stem `rNN_<dataset>_<cut>`.
- The config names the board's extract (`input.parquet_path`), the cut
  (`population.where`) and the questions its calling pages bind
  (`answers: [QD1]`, derived from their `answers.yaml`).
- The answering page calls it through its own ticket
  `runs/run_bNNjNNtNNrNN_<partition>_<task>.sh`, which sets `RESULT_DIR` to the
  page's `results/<ticket>/` and `RUN_TICKET` to itself; the result holds the
  tables, `metrics.json`, the Look step's `fig_*.png` and `runtime.yaml`
  (written before the work, finalized after its result gate passes).
- The join is the evidence need: the page's `answers.yaml` binds each
  compute need of the question (`QD<n>.E<k>`) to the narrowest files of this
  result, with the fields its `pass:` names (`../../haipipe-insight/ref/evidence-needs.md`). The config's
  `answers:` is a cross-check, never the join.
- Only aggregate, light output in the result; a file over 10 MB or a
  row-level table goes to
  `_WorkSpace/ProjectResult/<Project>/<page path>/results/<ticket>/` with a
  `heavy.yaml` pointer. A result is never edited by hand; rerun the ticket.
- A missing run is commissioned through `haipipe-task` (new config + ticket in
  an existing task, or a new task); the Insight workflow never executes a task
  invisibly.

## The page · Report (brief)

The page's `.md` says the observation in words, briefly: the denominators
every later answer divides by, a catalog correction. Shape:
headline (the observation, not the topic) → counts with unit and window →
coverage and gaps, with the figures embedded from its results. Each need is
cited where it is answered (`[QD1.E1]`). Its `runs:` header names every ticket
it read and `results-read:` when it read them; every number traces to a file in
one of those results.

## Gate and closure

GI2 passes when the answering page's ticket receipt is `ok` and current for
the board's extract, `haipipe-insight-check` finds every need of the question
bound, fit, cited and current, unit,
window and coverage are stated (in the QA note or the page), gaps are visible, and no
interpretation has entered. A rerun or a changed extract reopens the cell and
everything that cites it.

## Handoff

Hand Information the question id, its needs, the page, its tickets, the bound files, unit/window
and coverage/gaps. Do not hand it a precomputed claim.

## Files

- Task run: `tasks/b5N_<topic>_dikw/j1N_data_<topic>/tNN_<task>/scripts/config/rNN_<dataset>_<cut>.yaml` + `runs/rNN_….sh`
- Page ticket: `insights/<board>/<n>-<partition>/D<NN>-<partition>-<slug>/runs/run_bNNjNNtNNrNN_<partition>_<task>.sh`
- Result: `insights/<board>/<n>-<partition>/D<NN>-<partition>-<slug>/results/<ticket>/`
- Page: `insights/<board>/<n>-<partition>/D<NN>-<partition>-<slug>/D<NN>-<partition>-<slug>.md`
- Binding: `insights/<board>/<n>-<partition>/D<NN>-<partition>-<slug>/answers.yaml` (each need → its result files)
- Legacy: a board made before page tickets keeps its results in its old store
  (`ref/board-contract.md` § Boards made before page tickets).
