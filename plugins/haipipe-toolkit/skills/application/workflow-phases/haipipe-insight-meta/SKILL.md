---
name: haipipe-insight-meta
description: >-
  InsightBoard workflow phase I0 and Folder contract for Meta: inventory,
  grain, population, window, freshness, limits, and optional partition rules
  before any question is asked. Owns both Page and Task faces. Use when opening
  or refreshing an InsightBoard. Trigger: insight meta, data inventory, I0,
  folder-kind meta, legacy page-type meta, /haipipe-insight-meta.
metadata:
  version: "1.0.0"
  last_updated: "2026-08-31"
  workflow: haipipe-insight-workflow
  phase: I0
  folder_kind: meta
  primary_face: page
  page_ruling: none
  legacy_page_type: meta
  group-token: "MT"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Purpose and Scope → Source Inventory → Unit and Grain → Population and Window → Freshness → Known Limits; partition-major inserts Partition Register → Shared Thresholds after Purpose and Scope"
---

# /haipipe-insight-meta · establish what the board can know

Load `haipipe-folder`, `haipipe-page`, `haipipe-insight`, and
`haipipe-insight-workflow`. Existing folders may retain `page-type: meta`;
new phase-authored folders use `folder-kind: meta`.

## Position

I0 is the Insight workflow's entry phase. GI0 must pass before a question is
runnable. One Meta Folder exists at `0-MT-meta/MT00-meta/`.

## Folder Kind

Meta describes the evidence universe. It never asks a question, derives a
pattern, makes a claim, or advises. The four question registers are sibling
Folders owned by I1, not divisions of Meta.

## Input

- accepted Task/Discovery/other Folder sources, bound by exact PageX paths;
- source versions, unit/grain, population, time window, and refresh clocks;
- the optional partition proposal and shared thresholds from `ref/partition.md`.

## Page Face

The reader promise is: **what data exists here, at what grain, for whom, for
when, and with which limits**. Use the fixed outline declared in metadata.
Partition-major boards insert `Partition Register` and `Shared Thresholds`
after division 1. No question, result, or conclusion appears on this face.

## Task Face

Resolve every source path; inspect source/run identity; reconcile grain,
population, coverage, and freshness; record staleness rules; and, when
partition-major, prove that the partition register is coherent. A refresh
reopens Meta and every downstream row that depended on a changed source.

## Plugins

- `outline` required for the human-readable inventory plan;
- `pagex` required when the inventory binds another Folder;
- `probe` optional only to resolve a missing source fact;
- `code` forbidden by default: inventory does not execute analysis.

## Gate and Closure

GI0 closes I0 when all named sources resolve, unit/grain and population/window
are explicit, freshness and known limits are visible, and any partition
register passes its deterministic checks. A description with an unresolved
load-bearing source is open.

## Handoff

Hand I1 the accepted inventory, refresh/staleness rule, and, when present,
partition register plus shared thresholds. Do not hand it a preferred question.

## Files

- Folder Page: `0-MT-meta/MT00-meta/MT00-meta.md`
- Shared partition law: `../../haipipe-application/ref/partition.md`
- This phase owns no private scripts.
