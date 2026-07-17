---
name: haipipe-application-descriptions
description: "Stage orchestrator for the intervention's 0-lifecycle/1a-descriptions/1a-descriptions.md: rung 1a of the venue-FREE evidence ladder (1a-descriptions -> 1b-themes -> 1c-claims -> 1d-advice). Describes what the data looks like: anchored summaries only (statistic + pointer + as-of date), populated by task-profile probes, never computed inline, never raw data. Consumes seed's [FORWARD -> CLAIMS] pointers; owns the staleness stamp when entries refresh. Markdown only. Trigger: descriptions, data profile, how does the data look, cohort size, describe the data, /haipipe-application descriptions."
argument-hint: "[intervention-path] [--refresh <Dnn>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.2.0"
  last_updated: "2026-07-17"
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

Read first: `../../../PHILOSOPHY.md`, `../../../wiki/03-intervention-lifecycle.md`, `../../../wiki/08-stage-gate.md`.
Interventions live on DYNAMIC data (iterate keeps refreshing it) and the artifact carries no Methods/Results body of its own — so the data description needs an explicit, dated, re-runnable home, and that home is this rung.


## What's special: three things make descriptions descriptions

**1. Anchored summaries ONLY — the doc quotes what landed, it never computes.**
One D entry is one line, three parts: `**D3** - median engagement gap 41d -> tasks/A_message_design/results/summary.csv (as-of 2026-07-08)`.
Every number carries a pointer to a project-side artifact (task result, discovery source) and an as-of date; no raw data, no tables of rows, no inline computation or estimation.
There is no `_VALUES_` sidecar here: the D lines ARE the anchored one-liners, and the rich landed detail (arm-by-arm rates, distributions, the field inventory) lives in `_DESCRIPTIONS/DS<n>_<name>.md` — the PROBE `values:` lane REDIRECTS into those per-dataset sheets.
Ids `D<n>` are ladder-local (1b cites them as `T1 (D3)`, 1c as `C2 (T1; D3)`); they are unrelated to PP numbers.

**2. Rounds are the GROW saturation engine, not a formality.**
The roster GROWS because LANDED numbers feed the next round's questions — round 2's best questions cannot be asked until round 1's numbers exist.
Each round: GENERATE (a question storm per `ref/interrogation-battery.md`, the lens ROTATED per round) -> FILTER (answerable from existing D entries? discard : new D slot + a probe question) -> RELEASE MENU (user picks; PROBE dispatches picks) -> LAND (numbers land as D entries + DS sheets) -> REVISE -> SELF-TEST (answer the blind battery from D entries ONLY, one D id per answer; any stumble is next round's topic).
The lens rotates: round 1 SCHEMA, round 2 DISTRIBUTION ("click 1.9% — concentrated where? missing how?"), round 3 CROSSING / SURPRISE, until a DRY storm + a passed self-test says SATURATED.
Log every lap `[ROUND n]` in `_LOG`; the dry-stop bar is venue-scaled (`wiki/08`: light = one clean round, medium = one dry round, full = two consecutive dry rounds).

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
PROBE   dispatch via haipipe-application-probe (mode light, task-profile: "profile the cohort", "pull
        engagement summary"); the values: lane lands anchored numbers into D entries (with as-of dates) and
        the rich detail into _DESCRIPTIONS/DS<n> sheets. Routing mechanics are the probe layer's:
        ../../../2-phase/1-probe/haipipe-application-probe/SKILL.md
REVISE  tighten entry wording, group by dataset, dedupe
CHECK   exit gate (may be BATCHED into the ladder gate per the venue, wiki/08): every entry anchored +
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
Datasets       one DS<n> per data source: name, scope, where it lives (pointer)
Coverage       the breadth floor: six facets (cohort, arms, outcomes, time window, data quality,
               benchmark), each filled (D ids) or waived with a why — waivers are the reservoir
Descriptions   one D<n> per entry, grouped by dataset: statistic + resolving pointer + as-of date, one line
Probes         this rung's roster of the 1-probes/ sections that serve it: one line per PP + state;
               a D-slot references its question via [AWAITING PP<nn>] until it lands
Refresh Log    which D ids refreshed when, and which downstream ids were STALE-stamped (may be empty)
```

Sidecars: `_LOG_1a-descriptions.md` (phase journal) · `_DESCRIPTIONS/DS<n>_<name>.md` (per-dataset profile sheet: field inventory + Field Disposition — 100% of the schema profiled | waived | excluded — and the readable landed profile; written at PROBE, quoted-only, every line anchored + dated).
Evidence questions are RAISED as SECTIONS in the flat probe pool `1-probes/PPNN_<topic>.md` (one file per topic, one section per question, fields serves/target/state/q-executor/a-consumer + `## Why`), state `planned | commissioned | answered | read | answered-local | failed` — never a per-stage `_PROBE/` folder or a `1-probe-plans/` index (both retired; migrate a legacy card into `1-probes/` on first touch).
Formatting: `=====` title, `-----` sections, `**bold**` sub-items, one sentence per line; no `#`/`##`/`###`.


## Done-criteria (read at CHECK)

```text
- every D<n> has a statistic + a resolving pointer + an as-of date; no raw data, no computation, no unanchored number
- Coverage: all six facets filled (D ids) or waived with a one-line why
- Field Disposition: 100% of each dataset's schema dispositioned in its _DESCRIPTIONS/DS<n> sheet (quoted-only, anchored + dated)
- Saturation: the last [ROUND n] in _LOG is DRY and the blind self-test passed citing D ids
- no unconsumed [FORWARD -> CLAIMS] pointer in seed's _LOG_0-seed.md
- Refresh Log present (may be empty on first pass); no unresolved STALE tag
- Probes roster matches the 1-probes/ sections that serve this rung; every serving section resolved (answered | read | answered-local) with resolving refs (checker-verified)
```


## Principles

1. Every number is dated; an undated anchor is a latent staleness bug.
2. Venue-FREE: data truth does not change with the channel, so retargeting never touches this rung.
3. Insight KB is optional context, not a required source — anchor to task results and discovery sources directly.


## Exits

```text
promote -> /haipipe-application themes   (earned by a dry round + a passed self-test, never by impatience)
```

End every reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).
