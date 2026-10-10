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
  version: "2.4.1"
  last_updated: "2026-10-09"
  workflow: haipipe-insight-workflow
  folder_kind: data
  primary_face: task
  page_ruling: none
  legacy_page_type: data
  group-token: "D"
  report:
    shape: "Page Face: objective title; Opening answers (the observation); Content one division per need: counts, unit, window → coverage and gaps"
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
  (`population.where`) and the needs its calling pages bind
  (`answers: [QD1.E1]`, re-derived from their `answers.yaml`).
- The answering page calls it through its own ticket
  `runs/run_bNNjNNtNNrNN_<partition>_<task>.sh`, which sets `RESULT_DIR` to the
  page's `results/<ticket>/` and `RUN_TICKET` to itself; the result holds the
  tables, `metrics.json`, the Look step's `fig_*.png` and `runtime.yaml`
  (written before the work, finalized after its result gate passes).
- The join is the evidence need: the page's `answers.yaml` binds each
  compute need of the question (`QD<n>.E<k>`) to this result only when the
  run computes the need's work spec exactly (cut, unit, measure, grouping,
  uncertainty, rivals, output columns) (`../../haipipe-insight/ref/evidence-needs.md`). The config's
  `answers:` is a cross-check, never the join.
- Only aggregate, light output in the result; a file over 10 MB or a
  row-level table goes to
  `_WorkSpace/ProjectResult/<Project>/<page path>/results/<ticket>/` with a
  `heavy.yaml` pointer. A result is never edited by hand; rerun the ticket.
- A missing run is commissioned through `haipipe-task` (new config + ticket in
  an existing task, or a new task); the Insight workflow never executes a task
  invisibly.

## The page · Report (brief)

The page is a `haipipe-page` Page Face written through that skill's flow
(`../../haipipe-insight/ref/report.md` § The flow): plan, Draft, `page.py
adopt`, `page.py health`, a page CHECK by another agent. For Data it is brief:
the Opening asks what was observed, in plain words, and answers with the
observation; Content has one division per need, each giving the counts with
unit and window, then coverage and gaps, with the run's figures. Each need is
one Evidence Item carrying `**Need**:`; no id appears in the prose. The header
carries `answers:` and `results-read:`.

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

- Task run: `work/b5N_<topic>_dikw/j1N_data_<topic>/tNN_<task>/scripts/config/rNN_<dataset>_<cut>.yaml` + `runs/rNN_….sh`
- Page ticket: `insight/<board>/<n>-<partition>/D<NN>-<partition>-<slug>/runs/run_bNNjNNtNNrNN_<partition>_<task>.sh`
- Result: `insight/<board>/<n>-<partition>/D<NN>-<partition>-<slug>/results/<ticket>/`
- Page: `insight/<board>/<n>-<partition>/D<NN>-<partition>-<slug>/D<NN>-<partition>-<slug>.md`
- Binding: `insight/<board>/<n>-<partition>/D<NN>-<partition>-<slug>/answers.yaml` (each need → its result files)
- Legacy: a board made before page tickets keeps its results in its old store
  (`ref/board-contract.md` § Boards made before page tickets).
