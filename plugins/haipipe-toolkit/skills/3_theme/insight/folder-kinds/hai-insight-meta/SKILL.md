---
name: hai-insight-meta
description: "InsightBoard Folder contract for Meta: inventory, grain, population, window, freshness, limits and optional segment rules, the scope prerequisite for answering work. Use when opening or refreshing an InsightBoard. Trigger: insight meta, data inventory, folder-kind meta, /hai-insight-meta."
metadata:
  version: "1.5.1"
  last_updated: "2026-10-09"
  workflow: hai-insight-workflow
  folder_kind: meta
  primary_face: page
  page_ruling: none
  legacy_page_type: meta
  group-token: "MT"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Purpose and Scope → Source Inventory → Unit and Grain → Population and Window → Freshness → Known Limits; partition-major inserts Segment Register → Shared Thresholds after Purpose and Scope"
---

# /hai-insight-meta · establish what the board can know

> **Older layout (261008) below.** The Meta Folder `0-MT-meta/MT00-meta/` and "a second extract is a second board"
> are the register board's (`insight/<Dataset>-InsightBoard/`). On the insight ladder
> (`../../hai-insight/ref/insight-ladder.md`) a Board `insight/Insight-<name>/` holds its dataset in `board.md`
> `versions:` and `meta/meta.md`, and a new extract is the next data version of the same Board
> (`run-add-version-data-v<M>`: `{version, folder, frozen, new}`). What Meta must establish still holds.

Load `hai-draft` (its `ref/folder.md`), `hai-insight`, and
`hai-insight-workflow`. Existing folders may retain `page-type: meta`;
new owner-authored folders use `folder-kind: meta`.
Read `../../hai-insight/ref/page-v2-adapter.md` for Page lifecycle and
evidence migration, and `../../hai-insight/ref/question-groups.md` before
changing the segment register.

## Position

Meta owns the inventory prerequisite. GI0 must pass before an answering
Run can consume that inventory. One Meta Folder exists at `0-MT-meta/MT00-meta/`
of a board in `insight/<Dataset>-InsightBoard/`.

**One dataset (JL 261001).** MT00 names the board's ONE prepared extract (its
path, manifest and data dictionary). It is the identity of the board: the
workbench shows it in one banner line on every Space, and every task config
the board dispatches reads exactly this extract (`input.parquet_path`). A
second extract is a second board.

## Folder Kind

Meta describes the evidence universe. It never asks a question, derives a
pattern, makes a claim, or advises. The four question registers are sibling
Folders owned by Question, not divisions of Meta.

## Input

- accepted Task/Discovery Run Results, bound through full Supporting Run ids,
  or governed page-local static sources frozen in Local Input;
- source versions, unit/grain, population, time window, and refresh clocks;
- the optional segment proposal and shared thresholds from `../../hai-insight/ref/segment.md`.

## Page Face

The reader promise is: **what data exists here, at what grain, for whom, for
when, and with which limits**. Use the fixed outline declared in metadata.
Segment-major boards insert `Segment Register` and `Shared Thresholds`
after division 1. Each segment row names the segment by its full name
(one lowercase word; there is no letter column), its segment (`where`), its row
count and share, and the config stem every task uses for that segment
(`rNN_<dataset>_<segment>`): that column is how a run is placed in its
partition's table. No question, result, or conclusion appears on this face.

## Task Face

Resolve every source path and Result; inspect source/run identity; reconcile grain,
population, coverage, and freshness; record staleness rules; and, when
partition-major, prove that the segment register is coherent. A refresh
reopens Meta and every downstream row that depended on a changed source.

### Run Profile

Use the parameterized Run Specs in
`../../hai-insight-workflow/ref/run-workflow.md`. This Folder kind does
not itself allocate a Run. Declare a bounded Spec per selected Page writing,
evidence, delivery, or supporting computation target; use the worker's native
Ticket, Result, receipt, and close rule. Record each actual Run once in the
Insight Runtime, with its full owner address and exact input versions.
Routine resource updates and GI evaluations remain control records. An accepted
Run Result satisfies only its declared target; Page CHECK/CLOSE and the
Folder's GI conditions still govern citation and register settlement.

## Workbenches

- `outline` required for Context, inventory, and source Evidence Items;
- full Supporting Run Results are required for cross-Folder evidence; a related
  Page link alone is navigation;
- no active PageX or Probe lane; missing source facts route through Page
  OUTLINE/EVIDENCE and an explicitly selected supporting worker;
- `code` forbidden by default: inventory does not execute analysis.

## Gate and Closure

GI0 accepts the inventory only after the Meta Page reaches CHECK/CLOSE, all named sources
resolve through the Page v2 evidence graph, unit/grain and population/window
are explicit, freshness and known limits are visible, and any segment
register passes its deterministic checks. A description with an unresolved
load-bearing source is open.

## Handoff

Hand Question the accepted inventory, refresh/staleness rule, and, when present,
segment register plus shared thresholds. Do not hand it a preferred question.

## Files

- Folder Page: `0-MT-meta/MT00-meta/MT00-meta.md`
- Shared segment law: `../../hai-insight/ref/segment.md`
- Page adapter: `../../hai-insight/ref/page-v2-adapter.md`
- This Folder owns no private scripts.
