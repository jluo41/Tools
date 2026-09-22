---
name: haipipe-insight-information
description: >-
  InsightBoard Folder contract for Information: rates,
  contrasts, segments, distributions, and nulls derived reproducibly from
  named Data rows, without making a claim. Trigger: insight information,
  derive pattern, folder-kind information, /haipipe-insight-information.
metadata:
  version: "1.3.0"
  last_updated: "2026-09-20"
  workflow: haipipe-insight-workflow
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
Read `../../haipipe-insight/ref/page-v2-adapter.md` for evidence versus
semantic parent-row lineage.

## Position

Information answers a `QI` ask from named D rows and supplies named I rows to Knowledge.
Partition-major X contrasts are the only legal same-rung derivation: they cite
the two mirrored I rows they subtract.

## Folder Kind

Information organizes observations into a reproducible pattern. A row that can
be disputed on grounds other than arithmetic has become a Knowledge claim and
does not belong here. Covariates are cuts on Information, not partition groups.

## Input

One registered QI ask; exact version/hash-pinned D rows (or mirrored I rows for
an X contrast); unit/window; derivation formula; and relevant
null/contradictory observations. Actual values underneath those rows remain
bound through their Page evidence graphs.

## Page Face

Use `Question → Data Cited → Derivation → Patterns → Null and Contradiction`.
Every `I<n>` row carries the `PARENTS` record defined by the Page v2 adapter and
names its reproducible derivation. The lineage records interpretation; it does
not replace the evidence graph. Division 5 is never silently empty.

## Task Face

Select comparable rows; perform/check the derivation; preserve nulls and
contradictions; and reopen affected I rows when a parent changes. If a local
derivation Run is required, materialize Runs explicitly and bind its
Result before stating the pattern; execution alone does not close the Page Face.

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

## Workbenches

- `outline` required, including exact semantic parent-row lineage;
- Supporting/local Evidence Results required for any new value, citation, or
  display; no active PageX or Probe lane;
- `runs` holds selected Page Writing/Evidence/Delivery work or declared
  reproducible computation, with native Tickets as the execution door and
  `scripts/` optional. Omit the lane when no Run is allocated.

## Gate and Closure

GI3 passes only after Page CHECK/CLOSE, when every I row has exact
path/version/hash-pinned parents and repeatable derivation, the parents'
evidence remains current, nulls are visible, and no strength, cause, or
recommendation is asserted.

## Handoff

Hand Knowledge the QI id, I-row ids, parent-row paths, derivation, nulls, and
contradictions. Never turn arithmetic into a claim in the handoff.

## Files

- Page: `<InformationFolder>/<InformationFolder>.md`
- Parent lineage: Folder-owned `PARENTS` rows on the Page; no PageX path
- Optional Runs: tickets, paired Results, and optional `scripts/config/`
