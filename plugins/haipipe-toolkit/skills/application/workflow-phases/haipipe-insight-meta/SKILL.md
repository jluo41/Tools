---
name: haipipe-page-for-meta
description: >-
  The Page Type contract for the one META Page that heads an InsightBoard: what data this Application actually has before anyone asks a question of it. It fixes the source inventory, unit and grain, population, time window, freshness and staleness rule, and known limits. It performs no DIKW, reaches no finding, and holds no question: the group's four question registers (haipipe-page-for-question) own those. Use when opening an InsightBoard, when nobody can say what data is on hand, or when a source refreshes or a new extract lands. Trigger: data meta, source inventory, what data do we have, dataset description, grain, coverage, freshness, page-type meta, /haipipe-page-for-meta.
metadata:
  version: "0.3.0"
  last_updated: "2026-08-28"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
  group-token: "MT"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "purpose → source inventory → unit and grain → population and window → freshness → known limits; partition-major inserts Partition Register → Shared Thresholds after purpose"
---

# /haipipe-page-for-meta · say what data this Application has, before asking anything of it

Load `haipipe-page` first, and `haipipe-plugin-pagex` when binding accepted Task or Discovery Pages as sources.

Declare `page-type: meta`. One Meta Page exists per InsightBoard.

The word is `meta`, not `opening`, because `## Opening` is already a required section on every Board Page. A page called Opening gives a reader "the Opening of the Opening page." The paper family hit the same collision and named its head page Seed.

## Why this Page exists

Until 260820 the Application had one Brief carrying eight divisions, and they served two different readers: divisions 1-5 said what we are building and for whom, divisions 6-7 said what we must understand and from what sources. JL split the Application into an InsightBoard and a DesignBoard, and the Brief split on its own seam. This Page is the insight half.

```text
🔎 InsightBoard          MT00-meta   what data we have          ← this contract
🎨 DesignBoard           BR00-brief  what we are building       haipipe-page-for-brief
```

## Boundary

```text
Meta Page         what data exists, at what grain, how fresh, with what limits
Question register what is asked of one rung, and how far each ask has got
D/I/K/W page      one rung of an answer, citing the rung below
Brief Page        what the Application is building, and which needs it raises
Task/Discovery    the runs and sources themselves
```

**Meta describes; it never concludes.** It may say a table holds 41,000 invitations over eleven months. It may not say click rate is low, that a cohort underperforms, or that anything should change. The moment a sentence interprets, it belongs in an Information or Knowledge division and fails here.

Meta also holds no question. Since 260821 questions live beside it in the same group, on the four question registers `MT01` to `MT04` (`haipipe-page-for-question`), one facing each ladder rung. Meta says what exists; a register says what is asked of it; nothing in the MT group concludes.

**Meta may exist alone.** Data can land before anyone knows what it is for, so an InsightBoard with a full Source Inventory and four empty registers is a valid, complete state, not a half-finished one. The registers fill as a Brief raises needs or as a reader of this page becomes curious. Exploration that wants to start before then is `scope: task` work on the Task/Insights Board, not a row here.

## Fixed Content outline

```text
### 1 · Purpose and Scope
### 2 · Source Inventory
### 3 · Unit and Grain
### 4 · Population and Time Window
### 5 · Freshness and Staleness
### 6 · Known Limits
```

On a partition-major board (`haipipe-application` `ref/partition.md`) two more divisions are REQUIRED, in this order after Purpose and Scope: **Partition Register**, one row per partition with letter, name, filter and group folder, plus the X group listed beside them with no filter, so the register doubles as the complete group map; and **Shared Thresholds**, the one statement of where the threshold file lives and the rule that no config or page may restate a value from it. No other page may define a partition or a threshold.

- **Purpose and Scope** names the Application this board serves and what the data is on hand for. One paragraph.
- **Source Inventory** lists every source with its owner, path or table, run identity, and dated extract. A source with no resolvable run identity is a finding, not a row.
- **Unit and Grain** states what one row is, for each source, and how the sources join. Grain mismatches between sources are declared here rather than discovered mid-analysis.
- **Population and Time Window** states who is in, who is excluded, and the covered dates per source. Exclusions carry the reason.
- **Freshness and Staleness** gives each source its as-of date and the condition under which a refresh reopens dependent Insight Pages.
- **Known Limits** records missingness, instrumentation gaps, suspected bias, and anything a reader would otherwise rediscover. Empty is a claim and needs a sentence saying so.

**No Insight Roster.** Until 0.2.0 division 7 mapped each raised need to its answering page. JL moved that job out on 260821: each rung's queue lives on its own question register, and the board rollup lives on the wisdom register's Queue division, because W is where every chain terminates.

## Runtime shape

```text
<application-root>/<DataSubject>-InsightBoard/0-MT-meta/MT00-meta/
├── MT00-meta.md
├── pagex/     accepted Task/Discovery Pages bound as sources
└── display/   optional coverage or completeness views
```

Meta owns no `probe/`. Probing is a D/I/K/W page's authority; Meta only names what the sources are.

## Receipts

Two of the lane's transitions leave their dated `## Log` row on THIS page (`haipipe-insight-workflow` §Phase receipts), and a duty stated only in the machine file is a duty the page's author never reads:

```text
GI0 Meta → Question   this page past 🔴, its source resolving to a run, the four
                      registers existing · partition-major also needs the partition
                      register and the shared-threshold pointer
a PARTITION BIRTH     one row added to the Partition Register: letter, name, filter,
                      config, group folder — a partition is born HERE and nowhere else
```

The birth receipt is the load-bearing one. The register row is the only place a partition was ever declared, and retiring a partition edits that row away, so a board that minted and then withdrew one reads afterwards as though it never considered it. What the Log row preserves is the part that cannot be recovered: which candidate failed which clause of the partition test, and why — exactly what stops the next reader proposing the same cut again.

## Staleness

A source's as-of date changing does not rewrite this Page's prose. It updates that source's Freshness row and marks every D page whose Source and Run division names it. The question registers' Queue rows are the visible consequence.

## Closing checks

- Every source has an owner, a resolvable run identity, and a dated extract.
- Every source has a stated unit, grain, population, and covered window.
- Every source has an as-of date and a staleness condition.
- Known Limits is populated, or says explicitly that none are known.
- Partition-major only: every partition has a letter, name, filter and group folder; the threshold file is named with its PENDING/live status; no other page defines either.
- No division interprets, compares, ranks, or recommends.
- No question lives here, raised or recorded: the group's question registers own both.
- Every transition whose receipt this page owns — GI0, and each partition's birth — has a dated `## Log` row, and a retired partition's row survives its register row's removal.

This variant owns no scripts.
