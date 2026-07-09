---
name: haipipe-application-descriptions
description: "Stage orchestrator for the intervention's 0-lifecycle/1a-descriptions/1a-descriptions.md: rung 1a of the venue-FREE evidence ladder (1a-descriptions -> 1b-themes -> 1c-claims -> 1d-principles). Describes what the data looks like: anchored summaries only (statistic + pointer + as-of date), populated by task-profile probes, never computed inline, never raw data. Consumes seed's [FORWARD -> CLAIMS] pointers; owns the staleness stamp when entries refresh. Markdown only. Trigger: descriptions, data profile, how does the data look, cohort size, describe the data, /haipipe-application descriptions."
argument-hint: "[intervention-path] [--refresh <Dnn>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-07-09"
  summary: "New rung skill from the ladder restage (SOP-ladder-restage.md): stage 1 split into a 1a-1d evidence ladder echoing D->I->K->W. 1a = the D rung: anchored data descriptions with as-of dates, FORWARD consumer, staleness stamp duty."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-descriptions
========================================

Stage orchestrator for **rung 1a** of the evidence ladder (venue-FREE). The user invokes this skill (or the `ladder` sweep); it drives the phases internally.

It answers one question:

```text
What does the data look like, right now, with every number anchored?
```

The evidence ladder (stage-1 family, all venue-FREE, echoing D->I->K->W without reusing the KB letters):

```text
1a-descriptions   what the data looks like        <- THIS RUNG
1b-themes         what patterns/topics emerge
1c-claims         what generalizes (the ledger)
1d-principles     what to do (the deliverable)
```

Interventions live on DYNAMIC data (iterate keeps refreshing it), and the artifact carries no methods/results body of its own -- so the data description needs an explicit, dated, re-runnable home. That home is this rung.

## Artifact Spec

**Files produced:**
- `0-lifecycle/1a-descriptions/1a-descriptions.md` -- anchored data descriptions
- `0-lifecycle/1a-descriptions/_LOG_1a-descriptions.md` -- phase progress journal
- `0-lifecycle/1a-descriptions/_PROBE/PPNN_*.md` -- probe cards (+ index row in `1-probe-plans/README.md`)

**Canonical template (source of truth for section order + placeholders):** `ref/descriptions-template.md`

**Content structure (1a-descriptions.md):**

```text
Datasets            one **DS<n>** per data source: name, scope, where it lives (pointer)
Descriptions        one **D<n>** per entry: statistic + anchor + as-of date, grouped by dataset
Refresh Log         which D ids were refreshed when, and which downstream ids were stamped
```

- **One entry, one line, three parts:** `**D3** - median engagement gap 41d -> tasks/A_message_design/results/summary.csv (as-of 2026-07-08)`.
- **Anchored summaries ONLY.** Every number carries a pointer to a project-side artifact (task result, discovery source) and an as-of date. No raw data, no tables of rows, no inline computation -- the doc quotes what landed, like `_VALUES_` satellites do. There is no separate `_VALUES_` here: this doc IS the anchored-numbers doc.
- Ids `D<n>` are ladder-local (cited by 1b themes as `T1 (D3)` and onward); they are unrelated to insight-KB card ids and PPNN card numbers.

**Formatting:** `=====` title, `-----` sections, `**bold**` sub-items, one sentence per line. No `#`/`##`/`###`.

## Phase Orchestration

```
descriptions invoked
  |
  v
DRAFT --> FIRST: consume seed's forward pointers -- grep seed's
          `_LOG_0-seed.md` for `[FORWARD -> CLAIMS]` lines (token unchanged
          from the paper-aligned seed contract; the CONSUMER is this rung,
          the ladder's first). Route each: data-profile need -> a PP entry in
          THIS rung's _PROBE/; verdict-shaped need -> a planned PP skeleton in
          1c-claims' Probes section. Either counts as consumed; record the
          routing in _LOG. An unconsumed pointer fails CHECK below.
          Then: list the datasets in play, draft the description slots the
          themes/claims work will need (cohort size, engagement rates, field
          coverage, outcome base rates), buffer a probe plan per missing slot
          (internally calls haipipe-application-draft with this artifact spec)
  |
  v
PROBE --> dispatch via haipipe-application-probe (mode light; task-profile
          probes: "profile the cohort", "pull engagement summary");
          TRANSLATE lands anchored numbers into D entries with as-of dates
  |
  v
REVISE -> tighten entry wording, group by dataset, dedupe
          (internally calls haipipe-application-revise)
  |
  v
CHECK --> exit gate (may be BATCHED into the ladder gate per the venue,
          wiki/08-stage-gate.md): every entry anchored + dated? pointers
          resolve? no unconsumed FORWARD pointer? no unresolved STALE tags?
          (internally calls haipipe-application-check)
```

Phase visibility: announce every phase boundary (reply line + `[PHASE]` entry in `_LOG`); skip a phase only by an explicit logged verdict; CHECK is never implicit (batching changes WHERE approval happens, not whether).

> CC: token ruling needed — `[FORWARD -> CLAIMS]` is kept VERBATIM for grep-stability (SOP R5) even though this rung (1a) now consumes it. Rename to `[FORWARD -> LADDER]` across seed + here + SOP, or keep the legacy token? Keeping means the token name lies slightly; renaming breaks greps on old interventions.

## Refresh + staleness stamp duty (the dynamic-data contract)

`--refresh <Dnn>` (or iterate's backfill) re-runs the entry's probe and updates the line + as-of date. AFTER any refresh, this skill stamps downstream dependents: grep `1b-themes.md`, `1c-claims.md`, `1d-principles.md` for the refreshed `D<n>` id and append `[STALE D<n> refreshed <date>]` to each citing entry. A rung's CHECK fails on unresolved STALE tags in its own doc -- the tag is removed only by that rung re-confirming or revising the entry. Record the stamp pass in this doc's Refresh Log.

## Done-criteria

- [ ] Every `**D<n>**` entry has statistic + resolving pointer + as-of date
- [ ] No raw data, no computation, no unanchored number anywhere in the doc
- [ ] No unconsumed `[FORWARD -> CLAIMS]` pointer in seed's `_LOG_0-seed.md`
- [ ] Refresh Log present (may be empty on first pass)
- [ ] Every probe card read/verdicted with resolving refs (checker-verified)

## Principles

1. The doc quotes what landed; probes acquire. Never compute or estimate inline.
2. Every number is dated -- an undated anchor is a latent staleness bug.
3. Venue-FREE: data truth does not change with the channel; retargeting never touches this rung.
4. Ids are ladder-local; downstream rungs cite them, this rung never cites downstream.
5. Insight KB is optional context, not a required source (ladder restage R7): anchor to task results and discovery sources directly.

## Handoff

On CHECK confirm (or ladder-gate batch): `promote -> /haipipe-application themes`. End the reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).
