---
name: haipipe-insight-information
description: >-
  InsightBoard level contract for Information: rates, contrasts, segments,
  distributions and nulls derived reproducibly by a task run from the board's
  one extract, without making a claim. The answering page's tickets call the
  task run; the results in the page's results/ are the evidence and the page
  says what they show. Trigger: insight information, derive pattern,
  folder-kind information, /haipipe-insight-information.
metadata:
  version: "2.3.0"
  last_updated: "2026-10-01"
  workflow: haipipe-insight-workflow
  folder_kind: information
  primary_face: task
  page_ruling: none
  legacy_page_type: information
  group-token: "I"
  report:
    shape: "headline (the pattern) → the numbers that show it → nulls and contradictions → limit"
---

# /haipipe-insight-information · derive the pattern

Load `haipipe-insight` (`ref/board-contract.md`, `ref/report.md`,
`ref/evidence-needs.md`) and the workflow. `folder-kind: information` and `page-type: information` remain
read-only keys for boards made before page tickets.

## Position

Information answers a `QI` question from the board's extract and hands a
reproducible pattern to Knowledge. Partition-major cross contrasts are the only
legal same-level derivation: they read the mirrored Information results of
each partition and say how they differ.

## What an Information answer is

A reproducible pattern: a rate, a contrast, a segment, a distribution, a null.
A statement that can be disputed on grounds other than arithmetic has become a
Knowledge claim and does not belong here. Covariates are cuts inside a run
(groupings), not partitions.

## The run · Work

- A task in a `j2N_information_<topic>` Job of the Project's DIKW Block. One
  computation answers several questions when they differ only in a `by`
  column (`t01_rates` answers "rate by group", "by age band", "by weekday"…):
  the config's `answers:` lists all of them, and each question binds only the
  files of its own grouping.
- One config per dataset × partition, stem `rNN_<dataset>_<cut>`; the
  partition is the config's `population.where`, read against MT00's
  partition register. Thresholds come from the Job's shared file, never
  restated in a config, so every partition runs at identical floors.
- The answering page calls it through its own ticket
  `runs/run_bNNjNNtNNrNN_<partition>_<task>.sh`, which sets `RESULT_DIR` to the
  page's `results/<ticket>/` and `RUN_TICKET` to itself. One task run may feed
  several pages, each through its own ticket and result.
- The join is the evidence need: the page's `answers.yaml` binds each compute
  need (`QI<n>.E<k>`) to the narrowest files that answer it, with the fields
  its `pass:` names: an interval column when it asks uncertainty, a trend term
  when it asks to separate two causes (`../../haipipe-insight/ref/evidence-needs.md`). A run that computes
  the topic but not what `pass:` names does not fit; commission the missing
  computation (`haipipe-insight-bind`). `answers:` is a cross-check, never the join.
- The result keeps the receipt, the aggregate tables (with counts and
  intervals), `metrics.json`, the task's QA note and the Look step's
  `fig_*.png` drawn from those tables; small cells are suppressed and counted,
  never rounded. A result is never edited by hand; rerun the ticket.
- Heavy output (a file over 10 MB, a row-level table) goes to
  `_WorkSpace/ProjectResult/<Project>/<page path>/results/<ticket>/` with a
  `heavy.yaml` pointer.

## The page · Report

The page's `.md` is the report, written by a Report run from its own results. Shape: headline (the pattern,
in plain words: "Weekday barely moves clicks") → the numbers that show it, each
cited as `results/<ticket>/<file>` and shown by an embedded `fig_*.png` → nulls and contradictions, never silently
empty → the limit (unit, window, floor). Each need is cited where it is
answered (`[QI4.E1]`). It asserts no strength, cause or recommendation. Its
`runs:` header names every ticket it read and `results-read:` when.

## Gate and closure

GI3 passes when `haipipe-insight-check` finds every need of the question
bound, fit, cited and current, every number on the page traces to a current
result of one of its own tickets, nulls are visible, the derivation is
repeatable from the task code and config, and no strength, cause or
recommendation is asserted. A rerun reopens the page and everything that
cites it.

## Handoff

Hand Knowledge the question id, its needs, the page, its tickets, the bound files, the pattern,
nulls and contradictions. Never turn arithmetic into a claim in the handoff.

## Files

- Task run: `tasks/b5N_<topic>_dikw/j2N_information_<topic>/tNN_<task>/scripts/config/rNN_<dataset>_<cut>.yaml` + `runs/rNN_….sh`
- Page ticket: `insights/<board>/<n>-<partition>/I<NN>-<partition>-<slug>/runs/run_bNNjNNtNNrNN_<partition>_<task>.sh`
- Result: `insights/<board>/<n>-<partition>/I<NN>-<partition>-<slug>/results/<ticket>/`
- Page: `insights/<board>/<n>-<partition>/I<NN>-<partition>-<slug>/I<NN>-<partition>-<slug>.md`
- Binding: `insights/<board>/<n>-<partition>/I<NN>-<partition>-<slug>/answers.yaml` (each need → its result files)
- Legacy: a board made before page tickets keeps its results in its old store
  (`ref/board-contract.md` § Boards made before page tickets).
