---
name: hai-insight-data
description: "InsightBoard Data level: what was observed in the board's extract, from which exact run, without interpretation; a Data question's page calls a task run and reports its results. Trigger: insight data, observations, Data level, /hai-insight-data."
metadata:
  version: "2.4.2"
  last_updated: "2026-10-26"
  workflow: hai-insight-workflow
  folder_kind: data
  primary_face: task
  page_ruling: none
  legacy_page_type: data
  group-token: "D"
  report:
    shape: "Page Face: objective title; Opening answers (the observation); Content one division per need: counts, unit, window → coverage and gaps"
---

# /hai-insight-data · record what was observed

> **Older layout (261008) below.** The page folders `<n>-<segment>/D<NN>-<segment>-<slug>/`, `QD` ids and
> `answers.yaml` are the register board's. On the insight ladder (`../../hai-insight/ref/insight-ladder.md`) the
> answering page is the Task's `tNN_D<NN>_<slug>.md`, written by `run-write-t<NN>` from `runs/rNN_<segment>/result/`.
> What a Data page may say still holds.

Load `hai-insight` (`ref/board-contract.md`, `ref/report.md`,
`ref/evidence-needs.md`) and the workflow. `folder-kind: data` and `page-type: data` remain read-only keys for
boards made before page tickets.

## Position

Data answers a `QD` question after GI1 and supplies observations to
Information. It is answered by its page folder `<n>-<segment>/D<NN>-<segment>-<slug>/`:
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
  per dataset × segment, stem `rNN_<dataset>_<segment>`.
- The config names the board's extract (`input.parquet_path`), the segment
  (`population.where`) and the needs its calling pages bind
  (`answers: [QD1.E1]`, re-derived from their `answers.yaml`).
- The answering page calls it through its own ticket
  `runs/run_bNNjNNtNNrNN_<segment>_<task>.sh`, which sets `RESULT_DIR` to the
  page's `results/<ticket>/` and `RUN_TICKET` to itself; the result holds the
  tables, `metrics.json`, the Look step's `fig_*.png` and `runtime.yaml`
  (written before the work, finalized after its result gate passes).
- The join is the evidence need: the page's `answers.yaml` binds each
  compute need of the question (`QD<n>.E<k>`) to this result only when the
  run computes the need's work spec exactly (segment, unit, measure, grouping,
  uncertainty, rivals, output columns) (`../../hai-insight/ref/evidence-needs.md`). The config's
  `answers:` is a cross-check, never the join.
- Only aggregate, light output in the result; a file over 10 MB or a
  row-level table goes to
  `_WorkSpace/ProjectResult/<Project>/<page path>/results/<ticket>/` with a
  `heavy.yaml` pointer. A result is never edited by hand; rerun the ticket.
- A missing run is commissioned through `hai-task` (new config + ticket in
  an existing task, or a new task); the Insight workflow never executes a task
  invisibly.

## The page · Report (brief)

The page is a `hai-draft` Page Face written through that skill's flow
(`../../hai-insight/ref/report.md` § The flow): plan, Draft, `page.py
adopt`, `page.py health`, a page CHECK by another agent. For Data it is brief:
the Opening asks what was observed, in plain words, and answers with the
observation; Content has one division per need, each giving the counts with
unit and window, then coverage and gaps, with the run's figures. Each need is
one Evidence Item carrying `**Need**:`; no id appears in the prose. The header
carries `answers:` and `results-read:`.

## Gate and closure

GI2 passes when the answering page's ticket receipt is `ok` and current for
the board's extract, `hai-insight-check` finds every need of the question
bound, fit, cited and current, unit,
window and coverage are stated (in the QA note or the page), gaps are visible, and no
interpretation has entered. A rerun or a changed extract reopens the cell and
everything that cites it.

## Handoff

Hand Information the question id, its needs, the page, its tickets, the bound files, unit/window
and coverage/gaps. Do not hand it a precomputed claim.

## Files

- Task run: `work/b5N_<topic>_dikw/j1N_data_<topic>/tNN_<task>/scripts/config/rNN_<dataset>_<segment>.yaml` + `runs/rNN_….sh`
- Page ticket: `insight/<board>/<n>-<segment>/D<NN>-<segment>-<slug>/runs/run_bNNjNNtNNrNN_<segment>_<task>.sh`
- Result: `insight/<board>/<n>-<segment>/D<NN>-<segment>-<slug>/results/<ticket>/`
- Page: `insight/<board>/<n>-<segment>/D<NN>-<segment>-<slug>/D<NN>-<segment>-<slug>.md`
- Binding: `insight/<board>/<n>-<segment>/D<NN>-<segment>-<slug>/answers.yaml` (each need → its result files)
- Legacy: a board made before page tickets keeps its results in its old store
  (`ref/board-contract.md` § Boards made before page tickets).
