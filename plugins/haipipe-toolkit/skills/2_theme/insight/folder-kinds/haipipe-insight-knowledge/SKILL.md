---
name: haipipe-insight-knowledge
description: >-
  InsightBoard level contract for Knowledge: one supported proposition with
  strength, rival explanations and boundary, written on its answering page
  from named results and Information pages, never advising. Trigger: insight
  knowledge, claim, rivals, folder-kind knowledge, /haipipe-insight-knowledge.
metadata:
  version: "2.4.0"
  last_updated: "2026-10-01"
  workflow: haipipe-insight-workflow
  folder_kind: knowledge
  primary_face: page
  page_ruling: none
  legacy_page_type: knowledge
  group-token: "K"
  report:
    shape: "Page Face: objective title; Opening answers (the claim); Content one division per need, the judge need last (strength → rivals → boundary); the pooling verdict cites the heterogeneity page"
---

# /haipipe-insight-knowledge · make the bounded claim

Load `haipipe-insight` (`ref/board-contract.md`, `ref/report.md`,
`ref/evidence-needs.md`) and the workflow. `folder-kind: knowledge` remains a read-only key for boards made
before page tickets.

## Position

Knowledge answers a `QK` question on its page and hands the claim to Wisdom.
It cites the runs and Information pages below it by name. A partition-major
pooling verdict is a claim about exchangeability and may cite the
heterogeneity Knowledge page directly, one step and no further.

## Folder Kind

Knowledge says **what is true, how strongly, and where it stops being true**.
It never recommends an action. A row an implementer could act on without more
context has crossed into Wisdom.

## Input

One registered QK question and its agreed evidence needs; the current results of the runs that bear on it
and the Information pages that read them; the candidate proposition; the
strength reason; rival explanations and their disposition; the
population/window/unit boundary.

## The page

The answering page (`<n>-<partition>/K<NN>-<partition>-<slug>/`) is a
`haipipe-page` Page Face written through that skill's flow
(`../../haipipe-insight/ref/report.md` § The flow): plan, Draft, `page.py
adopt`, `page.py health`, a page CHECK by another agent. A page may answer
several QK questions; the register cell names it. The Opening asks the question
in plain words and answers with the claim. Content has one division per need:
each compute need's evidence from its bound files, each cite need's Information
in plain words, and last the judge division, which holds the proposition, its
strength and the reason, the rivals with their disposition, and the boundary.
One proposition per judge division; `strength:` in the header is `STRONG |
MODERATE | WEAK`. Rivals and boundary are required; weak claims remain legal
when honestly typed. Each compute or cite need is one Evidence Item carrying
`**Need**:`; no id appears in the prose.

### Strength rubric

Strength rates support for this exact proposition inside its stated
population, unit, and window. It is not confidence in the analyst, a count of
citations, a measure of source prestige, or a probability. Apply the rubric to
the accepted, current results and Information pages the page cites:

| Label | Use when | Required explanation |
|---|---|---|
| `STRONG` | The parents directly test the proposition; their population, measure, and window match its boundary; the declared quality/precision checks pass; and no material named or unevaluated rival could change the bounded claim on the cited evidence. | Name the supporting results and checks, and say why the strongest plausible rival does not explain the result. |
| `MODERATE` | The parents directly bear on the proposition, but a material limitation, sensitivity, or plausible rival could change its scope or strength. The proposition is still better supported than its named alternatives. | Name the support and the unresolved limitation or rival; narrow the proposition to what remains supported. |
| `WEAK` | Relevant accepted evidence supports only a narrow reading, is fragile or indirect, or is materially challenged by a rival or contrary parent. | Name the limited support and the strongest contrary evidence; state the narrow boundary that keeps the proposition defensible. |

For every label, record (1) the exact runs and Information pages, (2) the evidence feature that
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

## Runs behind a claim

A claim computes whenever its question has a compute need
(`../../haipipe-insight/ref/evidence-needs.md`): a gain with its uncertainty, an adjusted contrast
for a named rival, a held-out score, a size calculation. Each such need is a
task in a `j3N_knowledge_<topic>` Job of the Project's DIKW Block,
commissioned through `haipipe-task`; the Knowledge page calls it through its
own ticket `runs/run_bNNjNNtNNrNN_<partition>_<task>.sh` (`RESULT_DIR` set to
the page's `results/<ticket>/`) and binds it in `answers.yaml`. The Information
it rests on is a cite need; the proposition, strength and boundary are judge
needs. A page whose question has only cite and judge needs has no `runs/`.

**A refusal is computed.** "No field measures this" or "the design never
varies this" is a compute need whose probe run shows the absence (a column
inventory, a classification of the sent text); a refusal read off another
page is not evidence.

**A compute need answered by reasoning is a GAP, never a WEAK claim.** When
the ask names a test and no run computes it, the page does not argue its way
around the missing number from other pages; the cell stays open until the run
exists. Rivals the ask names are compute needs too: a rival is ruled out by
its adjusted contrast, not by a sentence.

This is claim adjudication, not message design or local experimentation.

## Gate and Closure

GI4 passes after a fresh-context check of the page, when `haipipe-insight-check`
finds every need bound, fit, cited and current (no compute need reasoned
away), every number traces to a current result of a named ticket or a cited page, the page states strength/reason,
unresolved rivals and boundary, and contains no recommendation. A pooling verdict also
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

Hand Wisdom the QK id, its needs, the page path, proposition, strength/reason, rivals,
boundary, the runs it rests on, and any pooling condition.

## Files

- Page: `insights/<board>/<n>-<partition>/K<NN>-<partition>-<slug>/K<NN>-<partition>-<slug>.md`
- Tickets and results, when it computes: the page's `runs/<ticket>.sh` and
  `results/<ticket>/`, named in its `runs:` header
- Binding: the page's `answers.yaml` (each need → its result files, cited page or `judge`)
- Legacy: a board made before page tickets keeps its results in its old store
  (`ref/board-contract.md` § Boards made before page tickets).
