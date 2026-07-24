---
name: haipipe-application-descriptions
description: "Stage orchestrator for the intervention's 0-lifecycle/1a-descriptions/1a-descriptions.md: rung 1a of the venue-FREE evidence ladder (1a-descriptions -> 1b-themes -> 1c-claims -> 1d-advice). Describes what the data looks like: anchored summaries only (statistic + pointer + as-of date), populated by task-profile probes, never computed inline, never raw data. Consumes seed's [FORWARD -> CLAIMS] pointers; owns the staleness stamp when entries refresh. Markdown only. Trigger: descriptions, data profile, how does the data look, cohort size, describe the data, /haipipe-application descriptions."
argument-hint: "[intervention-path] [--refresh <Dnn>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.2.6"
  last_updated: "2026-07-19"
  summary: "Descriptions stage (rung 1a of the venue-FREE 1a–1d evidence ladder; the D rung) — the anchored data profile: each D entry is statistic + pointer + as-of date, one line, quoting what task-profile probes landed (rich landed detail redirects into _DESCRIPTIONS/DS<n> profile sheets). Rounds are a GROW saturation loop (lens-rotating question storms, blind self-test, dry-stop); the rung consumes seed's [FORWARD -> CLAIMS] pointers and owns the downstream staleness stamp. History: ./CHANGELOG.md."
---

Skill: haipipe-application-descriptions
========================================

Rung **1a** of the venue-FREE evidence ladder, and the floor every higher rung stands on.
It answers: what does the data look like, right now, with every number anchored and dated?

```text
1a-descriptions   what the data looks like          <- THIS RUNG
1b-themes         what patterns/topics emerge
1c-claims         what generalizes (the ledger)
1d-advice         what the evidence advises (the deliverable)
```

Read first: `../../../PHILOSOPHY.md`, `../../haipipe-application-lifecycle/SKILL.md` (Intervention Lifecycle Contract), `../../../haipipe-application/SKILL.md` (Stage Gate Protocol).
Interventions live on DYNAMIC data (iterate keeps refreshing it) and the artifact carries no Methods/Results body of its own — so the data description needs an explicit, dated, re-runnable home, and that home is this rung.


## What's special: three things make descriptions descriptions

**1. Anchored summaries ONLY — the doc quotes what landed, it never computes.**
One Description is a subsection — a topic title plus one anchored line, e.g. `## Description 3 · engagement timing` then `median engagement gap 41d -> tasks/A_message_design/results/summary.csv (as-of 2026-07-08)`.
Every number carries a pointer to a project-side artifact (task result, discovery source) and an as-of date; no raw data, no tables of rows, no inline computation or estimation.
There is no sidecar here: the Description subsections ARE the anchored entries, and the rich landed detail (arm-by-arm rates, distributions, the field inventory) stays in the task/discovery result the entry points to — the PROBE `values:` lane lands the anchored one-liner + pointer, not a sidecar copy.
Each Description carries a short id (Description 3 -> `D3`) that is ladder-local (1b cites `T1 (D3)`, 1c `C2 (T1; D3)`) and unrelated to PP numbers — spelled out where DEFINED, short where CITED.

**2. Rounds are the GROW saturation engine, not a formality.**
The roster GROWS because LANDED numbers feed the next round's questions — round 2's best questions cannot be asked until round 1's numbers exist.
Each round: GENERATE (a question storm per `ref/interrogation-battery.md`, the lens ROTATED per round) -> FILTER (answerable from existing D entries? discard : new D slot + a probe question) -> RELEASE MENU (user picks; PROBE dispatches picks) -> LAND (numbers land as D entries + DS sheets) -> REVISE -> SELF-TEST (answer the blind battery from D entries ONLY, one D id per answer; any stumble is next round's topic).
The lens rotates: round 1 SCHEMA, round 2 DISTRIBUTION ("click 1.9% — concentrated where? missing how?"), round 3 CROSSING / SURPRISE, until a DRY storm + a passed self-test says SATURATED.
Log every lap `[ROUND n]` in `_LOG`; the dry-stop bar is venue-scaled (Stage Gate Protocol: light = one clean round, medium = one dry round, full = two consecutive dry rounds).

**3. It owns the downstream staleness stamp (the dynamic-data contract).**
`--refresh <Dnn>` (or iterate's backfill) re-runs the entry's probe and updates the line + its as-of date.
AFTER any refresh this skill stamps dependents: grep `1b-themes.md`, `1c-claims.md`, `1d-advice.md` for the refreshed `D<n>` id and append `[STALE D<n> refreshed <date>]` to each citing entry, then record the pass in this doc's Refresh Log.
A rung's CHECK fails on unresolved STALE tags in its own doc; the tag is cleared only by that rung re-confirming or revising the entry.


## The four phases, in descriptions

```text
DRAFT   FIRST consume seed's forward pointers — grep seed's _LOG_0-seed.md for [FORWARD -> CLAIMS]
        lines (this rung is the CONSUMER, the ladder's first): route each data-profile need to a probe
        question here, each verdict-shaped need to a planned claim in 1c-claims' ledger; either counts
        as consumed, logged in _LOG (an unconsumed pointer fails CHECK). Then re-mine last round's waived
        facets, list the datasets, SCHEMA-SWEEP each (column names ONLY — PHI rail; from data/contract.yaml,
        a DDL, or a schema-only probe) into the DS sheet's Field Disposition (every field group profiled |
        waived | excluded-PHI), sweep the six coverage facets, run this round's lens-rotated question storm,
        turn each unanswerable question into a D slot + a probe question; end with the release menu
PROBE   dispatch via haipipe-application-probe (task-profile: "profile the cohort", "pull
        engagement summary"); the values: lane lands anchored numbers into Description entries (with as-of dates) — the rich
        detail stays in the task result the entry points to (no sidecar). Routing mechanics are the probe layer's:
        ../../../2-phase/1-probe/haipipe-application-probe/SKILL.md
REVISE  tighten entry wording, group by dataset, dedupe
CHECK   exit gate (may be BATCHED into the ladder gate per the venue, Stage Gate Protocol): every entry anchored +
        dated, pointers resolve, no unconsumed FORWARD pointer, no unresolved STALE tag, the last [ROUND n]
        DRY + self-test passed
```

Descriptions RECEIVES evidence, never PRODUCES it inline (LAW 1): it raises questions; `haipipe-application-probe` binds them.
Announce every phase boundary (reply line + `[PHASE]` in `_LOG`); skip a phase only by an explicit logged verdict; CHECK is never implicit — batching changes WHERE approval happens, not whether.
CHECK is part of the loop, not only its exit: the gate presents the saturation evidence AND asks "which data topics are still missing?" — the user is the strongest lens, a `grow` verdict converts the answers to new D slots and re-opens DRAFT as `[ROUND n+1]`, and approve means saturated AND the user added nothing.
Mid-phase back-routing stays legal (`[ROUTE -> seed]` for feasibility holes).


## The artifact

`0-lifecycle/1a-descriptions/1a-descriptions.md` — full skeleton in `ref/descriptions-template.md`:

```text
Dataset        the data this profile draws on — one source, several files, or a folder; list what's here (name, scope, pointer)
Coverage       the breadth floor: six facets (cohort, arms, outcomes, time window, data quality,
               benchmark), each filled (D ids) or waived with a why — waivers are the reservoir
Descriptions   one subsection per topic (`## Description <n> · <topic>`): statistic + resolving pointer + as-of date; cited downstream by the short id D<n>
Q-consumer     the questions this rung raises, one `## Q-Desc-<n>` block each (Ask / Why / Answer=__TO_BE_FILLED__ — the doc's only state); APPROVE adds each -> 1-probes/ pointer + state;
               a D-slot references its question via [AWAITING PP<nn>] until it lands
Refresh Log    which D ids refreshed when, and which downstream ids were STALE-stamped (may be empty)
```

Sidecar: `_LOG_1a-descriptions.md` (phase journal). No `_DESCRIPTIONS/` sheet — rich detail stays in the task/discovery result the entry points to; the schema sweep still reads COLUMN NAMES ONLY (PHI rail).
Evidence questions are RAISED as ENTRIES in the flat probe pool `1-probes/PPNN_<topic>/` (one file per TOPIC; each ENTRY is one `## QX<n>` q-executor carrying `### q-executor` / `### q-consumer` / `### bank binding` / `### a-executor`), states `planned | commissioned | answered | read | answered-local | failed`; the stake stays in this doc's Q-consumer.
Formatting: `=====` title, `-----` sections, `**bold**` sub-items, one sentence per line; content sections use no `#`; Descriptions use `## Description <n>`, Q-consumer questions use `## Q-Desc-<n>`.


## Done-criteria (read at CHECK)

```text
- every Description has a statistic + a resolving pointer + an as-of date; no raw data, no computation, no unanchored number
- Coverage: all six facets filled (D ids) or waived with a one-line why
- Schema sweep reads COLUMN NAMES ONLY, never data values (PHI rail)
- Saturation: the last [ROUND n] in _LOG is DRY and the blind self-test passed citing D ids
- no unconsumed [FORWARD -> CLAIMS] pointer in seed's _LOG_0-seed.md
- Refresh Log present (may be empty on first pass); no unresolved STALE tag
- Q-consumer questions are organized into 1-probes/ sections that serve this rung; every serving section resolved (answered | read | answered-local) with resolving refs (checker-verified)
```


## Principles

1. Every number is dated; an undated anchor is a latent staleness bug.
2. Venue-FREE: data truth does not change with the channel, so retargeting never touches this rung.
3. Insight KB is optional context, not a required source — anchor to task results and discovery sources directly.


## Questions this stage typically raises

DRAFT's RAISE+PLAN step raises what the draft cannot answer. These are the kinds this stage is prone to — read this list, then walk the draft against it.

```
🗄️ what we HAVE      Which store already holds this population, and what does it
                     actually contain? Path, producing pipeline, as-of date.
📏 magnitude         How many, over what window, with what completeness? An
                     anchored number, never an estimate written into prose.
🕳️ missingness       What fraction is missing, and is it missing at random?
                     A summary that hides this misleads every rung above it.
🌐 what to GET       Is there an external dataset that fills the gap, and can we get it?
```

Every entry here is COMPUTED by a task probe, never inline. This stage describes; it does not calculate.

## Exits

```text
promote -> /haipipe-application themes   (earned by a dry round + a passed self-test, never by impatience)
```

End every reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).
