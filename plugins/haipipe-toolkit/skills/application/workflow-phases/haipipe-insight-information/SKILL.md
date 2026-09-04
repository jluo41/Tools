---
name: haipipe-insight-information
description: >-
  InsightBoard workflow phase I3 and Folder contract for Information: rates,
  contrasts, segments, distributions, and nulls derived reproducibly from
  named Data rows, without making a claim. Trigger: insight information,
  derive pattern, I3, folder-kind information, /haipipe-insight-information.
metadata:
  version: "1.0.2"
  last_updated: "2026-09-01"
  workflow: haipipe-insight-workflow
  phase: I3
  folder_kind: information
  primary_face: page
  page_ruling: none
  legacy_page_type: information
  group-token: "I"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Question → Data Cited → Derivation → Patterns → Null and Contradiction; the X contrast Folder reads Information Cited at division 2"
---

# /haipipe-insight-information · derive the pattern

Load `haipipe-folder`, `haipipe-page`, `haipipe-insight`, and the workflow.

## Position

I3 answers a `QI` ask from named D rows and supplies named I rows to I4.
Partition-major X contrasts are the only legal same-rung derivation: they cite
the two mirrored I rows they subtract.

## Folder Kind

Information organizes observations into a reproducible pattern. A row that can
be disputed on grounds other than arithmetic has become a Knowledge claim and
does not belong here. Covariates are cuts on Information, not partition groups.

## Input

One registered QI ask; named D rows (or mirrored I rows for an X contrast);
unit/window; derivation formula; and relevant null/contradictory observations.

## Page Face

Use `Question → Data Cited → Derivation → Patterns → Null and Contradiction`.
Every `I<n>` row names its parent rows and reproducible derivation. Division 5
is never silently empty.

## Task Face

Select comparable rows; perform/check the derivation; preserve nulls and
contradictions; and reopen affected I rows when a parent changes. If a local
derivation Run is required, materialize Runs explicitly and bind its
Result before stating the pattern; execution alone does not close the Page Face.

## Plugins

- `pagex` required for D/I parent rows;
- `outline` required;
- `probe` optional for missing source facts;
- `runs` optional for reproducible computation, with `runs/` as the only
  door and `scripts/` optional.

## Gate and Closure

GI3 passes when every I row has named parents and repeatable derivation, nulls
are visible, and no strength, cause, or recommendation is asserted.

## Handoff

Hand I4 the QI id, I-row ids, parent-row paths, derivation, nulls, and
contradictions. Never turn arithmetic into a claim in the handoff.

## Files

- Page: `<InformationFolder>/<InformationFolder>.md`
- Optional Runs: tickets, paired Results, and optional `scripts/config/`
