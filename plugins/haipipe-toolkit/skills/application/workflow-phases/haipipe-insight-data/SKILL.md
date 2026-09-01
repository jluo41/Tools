---
name: haipipe-insight-data
description: >-
  InsightBoard workflow phase I2 and Folder contract for run-bound Data:
  observations with source/run provenance and no interpretation. Owns both
  Page and Task faces. Use when a Task, Discovery, or linked Folder has produced
  observations the board must cite once. Trigger: insight data, observations,
  I2, folder-kind data, legacy page-type data, /haipipe-insight-data.
metadata:
  version: "1.0.3"
  last_updated: "2026-09-01"
  workflow: haipipe-insight-workflow
  phase: I2
  folder_kind: data
  primary_face: task
  page_ruling: none
  legacy_page_type: data
  group-token: "D"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Origin → Source and Run → Observations → Coverage and Gaps"
---

# /haipipe-insight-data · record what was observed

Load `haipipe-folder`, `haipipe-page`, `haipipe-insight`, and the workflow.
Use `folder-kind: data`; `page-type: data` remains a read-only compatibility key.

## Position

I2 answers a `QD` question after GI1 and supplies named D rows to I3. It lives
in `1-D-data/D<NN>-<slug>/` on rung-major boards or the corresponding partition
group on partition-major boards.

## Folder Kind

One Data Folder holds one coherent observation set. It says **what was
observed and from which exact run**. It never computes a comparison, trend,
explanation, strength, or recommendation.

## Input

- one registered QD ask;
- one exact source Folder plus an accepted QA answer backed by a named run;
- source version, run identity, unit, window, and coverage.

## Page Face

Use `Origin → Source and Run → Observations → Coverage and Gaps`. Every D row
has a stable id and names the source/run path that produced it. Counts are
reported once here; higher rungs cite rows instead of restating them.

## Task Face

Resolve the source relationship and live status through PageX. For every value
coming from a Task or Discovery Folder, resolve an accepted QA answer through
Probe even when the producing Folder is already linked and reported. Verify the
named run and coverage; transcribe only reproducible observations; and reopen
this Folder on rerun. This phase does not launch another Folder's Run and
does not read raw `results/` when a QA/report surface is owed.

One local Run may normalize or validate an intermediate owned by this Data
Folder, but it cannot authorize a displayed value. Every displayed number
produced by a Run still crosses the one page-serving collection job and its QA
binding. A
reusable computation or source-data change belongs in its own linked executable
Folder.

## Plugins

- `pagex` required for the source Folder relationship and live task status;
- `probe` required for every Task/Discovery-derived value; accepted Page
  material may bind through PageX without a new Probe only when it already
  exposes the exact accepted evidence the phase needs;
- `outline` required;
- `runs` optional only when this Folder itself owns a declared Run/Result
  derivation; scripts remain optional. Otherwise it is absent.

## Gate and Closure

GI2 passes when every D value is bound by path to an accepted QA answer backed
by a named source/run, unit/window and coverage are explicit, gaps are visible,
and no interpretation has entered.
A rerun or changed source version reopens the affected rows and children.

## Handoff

Hand I3 the question id, D-row ids, exact provenance paths, unit/window, and
coverage/gaps. Do not hand it a precomputed claim.

## Files

- Page: `<DataFolder>/<DataFolder>.md`
- Cross-Folder binding: `evidence/pagex/`
- Required Task/Discovery QA bindings: `evidence/probe/`
