---
name: haipipe-insight-knowledge
description: >-
  InsightBoard Folder contract for Knowledge: one
  supported proposition with strength, rival explanations, and boundary,
  derived from named Information rows and never advising. Trigger: insight
  knowledge, claim, rivals, folder-kind knowledge, /haipipe-insight-knowledge.
metadata:
  version: "1.4.0"
  last_updated: "2026-09-20"
  workflow: haipipe-insight-workflow
  folder_kind: knowledge
  primary_face: page
  page_ruling: none
  legacy_page_type: knowledge
  group-token: "K"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Claim → Information Cited → Strength → Rivals → Boundary; the pooling-verdict Folder reads Knowledge Cited at division 2"
---

# /haipipe-insight-knowledge · make the bounded claim

Load `haipipe-folder`, `haipipe-page`, `haipipe-insight`, and the workflow.
Read `../../haipipe-insight/ref/page-v2-adapter.md` for Page closure and exact
semantic parent-row lineage.

## Position

Knowledge answers a `QK` ask from named I rows and supplies K rows to Wisdom. A
partition-major pooling verdict is a claim about exchangeability and may cite
the heterogeneity K row directly, one step and no further.

## Folder Kind

Knowledge says **what is true, how strongly, and where it stops being true**.
It never recommends an action. A row an implementer could act on without more
context has crossed into Wisdom.

## Input

One registered QK ask; exact path/version/hash-pinned I-row parents; candidate proposition; strength
reason; rival explanations and their disposition; population/window/unit
boundary.

## Page Face

Use `Claim → Information Cited → Strength → Rivals → Boundary`. One proposition
per `K<n>`, with the Page v2 adapter's `PARENTS` record beside it. Strength is
`STRONG | MODERATE | WEAK` plus a reason. Rivals and boundary are required;
weak claims remain legal when honestly typed.

### Strength rubric

Strength rates support for this exact proposition inside its stated
population, unit, and window. It is not confidence in the analyst, a count of
citations, a measure of source prestige, or a probability. Apply the rubric to
the accepted, current Information parents named in `PARENTS`:

| Label | Use when | Required explanation |
|---|---|---|
| `STRONG` | The parents directly test the proposition; their population, measure, and window match its boundary; the declared quality/precision checks pass; and no material named or unevaluated rival could change the bounded claim on the cited evidence. | Name the supporting I rows and checks, and say why the strongest plausible rival does not explain the result. |
| `MODERATE` | The parents directly bear on the proposition, but a material limitation, sensitivity, or plausible rival could change its scope or strength. The proposition is still better supported than its named alternatives. | Name the support and the unresolved limitation or rival; narrow the proposition to what remains supported. |
| `WEAK` | Relevant accepted evidence supports only a narrow reading, is fragile or indirect, or is materially challenged by a rival or contrary parent. | Name the limited support and the strongest contrary evidence; state the narrow boundary that keeps the proposition defensible. |

For every label, record (1) the exact I-row ids, (2) the evidence feature that
meets the selected definition, (3) the strongest limiting or contrary evidence,
and (4) why the adjacent stronger label does not fit. Do not count rows,
citations, or matching directions as a substitute for this explanation. A
missing, stale, or invalid parent is not `WEAK`: hold the claim until its
lineage is current. When the evidence is current but cannot distinguish the
claim from its rivals, record `WEAK` only for a still-supported narrow claim;
otherwise leave the claim unadjudicated and route the unresolved question.
If multiple reviewers read a consequential K claim, retain any differing
evidence interpretation and label rationale; do not average labels. If the
disagreement would change a pooling verdict and the frozen criteria do not
resolve it, use `UNDETERMINED` and name the disputed evidence or criterion.

This is a Knowledge-owner rubric. Do not translate these labels to confidence
scales owned by another Folder or workflow.

## Task Face

Test whether the proposition is narrower than its parents; enumerate and
evaluate rivals; set strength; inspect boundary conditions; and reopen every
child that cites a changed parent. This is claim adjudication, not message
design or local experimentation.

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
- any new rival test enters through a decided Supporting Run and local Evidence
  Result; no active PageX or Probe lane;
- `runs` holds selected Page Writing/Evidence/Delivery work or a declared
  robustness Run; scripts remain optional. Omit the lane with no allocation.

## Gate and Closure

GI4 passes only after Page CHECK/CLOSE, when every K row names exact
path/version/hash-pinned parents, strength/reason, unresolved rivals, and
boundary, and contains no recommendation. A pooling verdict also
states exactly `POOL`, `SPLIT`, or `UNDETERMINED` as an exchangeability claim.
The verdict names the predeclared shared-threshold source/version, compared
scope, evidence rows, decision-relevant limits, and consequence route. `POOL`
requires evidence that can rule out differences material to the stated counsel;
failure to find a statistically detectable difference is not enough. `SPLIT`
requires an evidenced, decision-relevant difference under the predeclared
criteria. Use `UNDETERMINED` when a completed, current comparison cannot
support either conclusion. Missing parents, absent threshold definitions, or
unfinished comparisons are not a verdict: GI4 remains held. Never force a
binary conclusion to make downstream work runnable.

## Handoff

Hand Wisdom the QK id, K-row id, proposition, strength/reason, rivals, boundary,
source versions, and any pooling condition.

## Files

- Page: `<KnowledgeFolder>/<KnowledgeFolder>.md`
- Parent lineage: Folder-owned `PARENTS` rows on the Page; no PageX path
