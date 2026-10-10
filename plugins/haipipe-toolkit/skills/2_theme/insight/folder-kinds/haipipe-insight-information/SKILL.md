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
  version: "2.4.1"
  last_updated: "2026-10-09"
  workflow: haipipe-insight-workflow
  folder_kind: information
  primary_face: task
  page_ruling: none
  legacy_page_type: information
  group-token: "I"
  report:
    shape: "Page Face: objective title; Opening answers (the pattern); Content one division per need: the numbers → nulls and contradictions → limit"
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

- A task in a `j2N_information_<topic>` Job of the Project's DIKW Block,
  chosen or built from each need's work spec, never the other way round. One
  run may serve several needs when each spec is met exactly by its own output
  file (a grouping per need); the config's `answers:` lists those need ids.
- One config per dataset × partition, stem `rNN_<dataset>_<cut>`; the
  partition is the config's `population.where`, read against MT00's
  partition register. Thresholds come from the Job's shared file, never
  restated in a config, so every partition runs at identical floors.
- The answering page calls it through its own ticket
  `runs/run_bNNjNNtNNrNN_<partition>_<task>.sh`, which sets `RESULT_DIR` to the
  page's `results/<ticket>/` and `RUN_TICKET` to itself. One task run may feed
  several pages, each through its own ticket and result.
- The join is the evidence need: the page's `answers.yaml` binds each compute
  need (`QI<n>.E<k>`) to the run that computes its work spec exactly: an
  interval column when the spec asks uncertainty, a trend term when it asks to
  separate two causes (`../../haipipe-insight/ref/evidence-needs.md`). A run that computes
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

The page is a `haipipe-page` Page Face written through that skill's flow
(`../../haipipe-insight/ref/report.md` § The flow): plan, Draft, `page.py
adopt`, `page.py health`, a page CHECK by another agent. The Opening asks the
question in plain words and answers with the pattern ("Weekday barely moves
clicks"); Content has one division per need: the numbers that show it, read
from the need's bound files and shown by the run's figures, then nulls and
contradictions, never silently empty, then the limit (unit, window, floor).
Each need is one Evidence Item carrying `**Need**:`; no id appears in the
prose. It asserts no strength, cause or recommendation. The header carries
`answers:` and `results-read:`.

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

- Task run: `work/b5N_<topic>_dikw/j2N_information_<topic>/tNN_<task>/scripts/config/rNN_<dataset>_<cut>.yaml` + `runs/rNN_….sh`
- Page ticket: `insight/<board>/<n>-<partition>/I<NN>-<partition>-<slug>/runs/run_bNNjNNtNNrNN_<partition>_<task>.sh`
- Result: `insight/<board>/<n>-<partition>/I<NN>-<partition>-<slug>/results/<ticket>/`
- Page: `insight/<board>/<n>-<partition>/I<NN>-<partition>-<slug>/I<NN>-<partition>-<slug>.md`
- Binding: `insight/<board>/<n>-<partition>/I<NN>-<partition>-<slug>/answers.yaml` (each need → its result files)
- Legacy: a board made before page tickets keeps its results in its old store
  (`ref/board-contract.md` § Boards made before page tickets).
