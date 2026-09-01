---
name: haipipe-insight-knowledge
description: >-
  InsightBoard workflow phase I4 and Folder contract for Knowledge: one
  supported proposition with strength, rival explanations, and boundary,
  derived from named Information rows and never advising. Trigger: insight
  knowledge, claim, rivals, I4, folder-kind knowledge, /haipipe-insight-knowledge.
metadata:
  version: "1.0.2"
  last_updated: "2026-09-01"
  workflow: haipipe-insight-workflow
  phase: I4
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

## Position

I4 answers a `QK` ask from named I rows and supplies K rows to I5. A
partition-major pooling verdict is a claim about exchangeability and may cite
the heterogeneity K row directly, one step and no further.

## Folder Kind

Knowledge says **what is true, how strongly, and where it stops being true**.
It never recommends an action. A row an implementer could act on without more
context has crossed into Wisdom.

## Input

One registered QK ask; named I-row parents; candidate proposition; strength
reason; rival explanations and their disposition; population/window/unit
boundary.

## Page Face

Use `Claim → Information Cited → Strength → Rivals → Boundary`. One proposition
per `K<n>`. Strength is `STRONG | MODERATE | WEAK` plus a reason. Rivals and
boundary are required; weak claims remain legal when honestly typed.

## Task Face

Test whether the proposition is narrower than its parents; enumerate and
evaluate rivals; set strength; inspect boundary conditions; and reopen every
child that cites a changed parent. This is claim adjudication, not message
design or local experimentation.

## Plugins

- `pagex` required for I/K parents;
- `outline` required;
- `probe` optional for a named rival test;
- `runs` optional only for a declared robustness Run; scripts remain
  optional.

## Gate and Closure

GI4 passes when every K row names its parents, strength/reason, unresolved
rivals, and boundary, and contains no recommendation. A pooling verdict also
states exactly `POOL` or `SPLIT` as an exchangeability claim.

## Handoff

Hand I5 the QK id, K-row id, proposition, strength/reason, rivals, boundary,
source versions, and any pooling condition.

## Files

- Page: `<KnowledgeFolder>/<KnowledgeFolder>.md`
- Parent bindings: `evidence/pagex/`
