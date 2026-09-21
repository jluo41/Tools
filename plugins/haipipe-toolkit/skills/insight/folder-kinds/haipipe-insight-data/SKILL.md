---
name: haipipe-insight-data
description: >-
  InsightBoard Folder contract for Data observations:
  exact source provenance with no interpretation. Owns both
  Page and Task faces. Use when a Task, Discovery, or linked Folder has produced
  observations the board must cite once. Trigger: insight data, observations,
  Data, folder-kind data, legacy page-type data, /haipipe-insight-data.
metadata:
  version: "1.3.1"
  last_updated: "2026-09-20"
  workflow: haipipe-insight-workflow
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
Read `../../haipipe-insight/ref/page-v2-adapter.md` before planning evidence or
claiming GI2.

## Position

Data answers a `QD` question after GI1 and supplies named D rows to Information. It lives
in `1-D-data/D<NN>-<slug>/` on rung-major boards or the corresponding partition
group on partition-major boards.

## Folder Kind

One Data Folder holds one coherent observation set. It says **what was
observed and from which exact source, including its producing Run when applicable**. It never computes a comparison, trend,
explanation, strength, or recommendation.

## Input

- one registered QD ask;
- one exact accepted Supporting Run Result, or a governed page-local source
  frozen in Local Input under the shared Page contract;
- source version, producing Run identity when applicable, unit, window, and coverage.

## Page Face

Use `Origin → Source and Run → Observations → Coverage and Gaps`. Every D row
has a stable id and names the source/run path that produced it. Counts are
reported once here; higher rungs cite rows instead of restating them.

## Task Face

For a produced source, resolve its status through the source Folder's native
Run/Result receipt. Its accepted Supporting Result enters the shared Page graph:
Supporting Run Result → frozen Local Input → local Page Evidence Run → typed
VALUE/CITE/DISPLAY Result. For governed static local sources, start with their
exact path/version/hash in frozen Local Input and perform the required typed
local Evidence work; there is no external producer to allocate.
For every value coming from a Task or Discovery Folder, verify the named
Supporting Run, coverage, and runtime receipt; transcribe only reproducible
observations; and reopen this Folder on rerun. This Folder may commission a
missing Supporting Run only after the Page SURVEY `Decide` gate; it never
executes another Folder invisibly.

One local Run may normalize or validate an intermediate owned by this Data
Folder, but it cannot authorize a displayed value. Every displayed number
produced by a Run still crosses the one page-serving collection job and its
Evidence Item binding. A
reusable computation or source-data change belongs in its own linked executable
Folder.

### Run Profile

Use the parameterized Run Specs in
`../../haipipe-insight-workflow/ref/run-workflow.md`. This Folder kind does
not itself allocate a Run. Declare a bounded Spec per selected Page writing,
evidence, delivery, or supporting computation target; use the worker's native
Ticket, Result, receipt, and close rule. Record each actual Run once in the
Insight Runtime, with its full owner address and exact input versions.
Routine resource updates and GI evaluations remain control records. An accepted
Run Result satisfies only its declared target; Page CHECK/CLOSE and the
Folder's GI conditions still govern citation and register settlement.

## Plugins

- full Supporting Run id and accepted Result required for cross-Folder evidence;
- one frozen Local Input and one consumer-owned local Evidence Run/Result are
  required for each make-item, including displayed values;
- `outline` required;
- `runs` contains only actually commissioned Page Writing/Evidence/Delivery
  work or a declared native derivation Run; scripts remain optional. With no
  allocation, omit the lane.

## Gate and Closure

GI2 passes only after Page CHECK/CLOSE, when every D value is bound by path to
either (a) an accepted Supporting Result for cross-Folder computation, frozen
Local Input and ready typed local Result, or (b) a governed page-local static
source pinned by path/version/hash in Local Input and a ready typed local
Evidence Result with the owed VALUE/CITE/DISPLAY verification. Branch (b) has
zero Supporting Runs and states why external computation is unnecessary;
unit/window and coverage are explicit, gaps are visible, and no interpretation
has entered.
A rerun or changed source version reopens the affected rows and children.

## Handoff

Hand Information the question id, D-row ids, exact provenance paths, unit/window, and
coverage/gaps. Do not hand it a precomputed claim.

## Files

- Page: `<DataFolder>/<DataFolder>.md`
- Evidence graph: `outline/<stem>-evidence-items.md`, generated
  `outline/evidence/supporting-runs/`, frozen Local Input, and local Results
