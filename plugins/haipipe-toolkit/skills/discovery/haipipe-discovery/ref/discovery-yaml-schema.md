# discovery.yaml — Discovery Folder Schema (v2, two-axis, 3 types: 搜 析 创)

## What this file is

`discovery.yaml` is the Plan + Report spec at the root of every discovery-folder. A discovery is one research topic = one folder, a sibling of a task-folder, running the uniform `Plan → Build(opt) → Execute → Report` lifecycle. `type:` names the folder type (`搜`/`析`/`创`); the lifecycle is identical for all three.

Location:

```
examples/<PROJECT>/discoveries/<GROUP_slug>/<NN_slug>/discovery.yaml
```

Sibling files:

```
discovery.yaml   Plan + Report spec (source of truth)
build/           (optional) instrument authored at Build
status.yaml      Axis-1 lifecycle progress snapshot
site.md          human-readable Report record
sources.md       Execute work product (搜: search)
notes.md         Execute work product (搜: read)
verdict.md | landscape.md | ideas.md   Execute TERMINAL (by type)
```

No local event log belongs here. Orchestration events go to `_haipipe/project.log.jsonl`.

## The two axes as fields

```
type:    Axis 2 — the folder type     搜 | 析 | 创      (decides the Execute terminal)
status:  Axis 1 — lifecycle progress  planned | building | executing | reported | ok | inconclusive | blocked
```

## Type values (Axis 2)

| 字 | type | IPO | Execute terminal | roles |
|---|---|---|---|---|
| 搜 | source | INPUT | `sources.md` (+ `notes.md`) | source_gather, source_read |
| 析 | analyze | PROCESS | `verdict.md` (判) / `landscape.md` (综) | prior_art_check, counterevidence, novelty_check → verdict; landscape_review, benchmark_landscape → landscape |
| 创 | create | OUTPUT | `ideas.md` | idea_generation |

`type` is authoritative for the terminal. For `析`, `role` picks the verdict-vs-landscape branch.

## Top-level fields

| Field | Type | Required | Notes |
|---|---|---|---|
| kind | string | yes | always `discovery` |
| id | string | yes | e.g. `L01.03` |
| **type** | enum | yes | **NEW** — folder type (Axis 2): `搜`/`析`/`创` |
| role | enum | yes | refinement within `type` (esp. 析); see Role Values |
| group | mapping | yes | discovery-group metadata |
| slug | string | yes | discovery-folder slug |
| title | string | yes | human-readable title |
| status | enum | yes | lifecycle progress (Axis 1) |
| parent | mapping | opt | delivery/probe/manual consumer |
| question | string | yes | external-world question (Plan) |
| sources | mapping | opt | search scope + selected refs (Plan); for `析`, may reference a `搜` folder |
| **build** | mapping | opt | **NEW** — optional instrument (`needed` + `artifact`) |
| expected_outputs | list | yes | files expected; terminal depends on `type` |
| **report** | mapping | yes | **RENAMED from `verdict`** — report-to-human outcome block, generalized across types |
| consumed_by | list | opt | project-relative parents that used the terminal |
| created_at | string | yes | quoted ISO8601 |
| updated_at | string | yes | quoted ISO8601 |

## Skeleton (析 type, synthesize flavor)

```yaml
kind: discovery
id: L01.03
type: 析                 # 搜 | 析 | 创
role: landscape_review   # picks landscape.md (综) vs verdict.md (判)
group:
  id: L01
  slug: personality-prescribing-landscape
  title: Personality x prescribing landscape
slug: empathy-agreeableness-outcomes
title: Empathy / agreeableness effects on prescribing outcomes
status: ok
created_at: "2026-06-22T10:00:00-04:00"
updated_at: "2026-06-22T11:30:00-04:00"

parent:
  type: paper
  path: paper/MISQ2026/0-lifecycle/2-claims
  role: required_evidence

# --- Plan (intent) ---
question: |
  What is known about physician agreeableness / empathy affecting prescribing outcomes?
sources:
  requested: [research-lit, semantic-scholar]
  from_source_folder: ""    # optional: a 搜 folder to reuse instead of searching inline
  local_first: true
  verification_required: true
build:
  needed: false             # true only for a systematic query string / extraction schema
  artifact: ""              # e.g. build/query-strategy.md
expected_outputs:
  - sources.md
  - notes.md
  - landscape.md            # terminal for 析-synthesize (verdict.md for 析-judge)

# --- Report (outcome, report-to-human) ---
report:
  outcome: mapped           # per-type values below (NOT the top-level lifecycle `status:`)
  summary: ""
  confidence: medium
  supports_claim: null      # 析-judge only
  contradicts_claim: null   # 析-judge only

consumed_by: []
```

A `搜` folder omits the `report.supports_claim`/`contradicts_claim` fields and ends at `sources.md`/`notes.md`; a `创` folder ends at `ideas.md` and usually sets `sources.from_source_folder` to the `搜`/`析` it builds on.

## Role values (refinements of type)

```
搜  source_gather        broad source scan, curated list          -> sources.md
搜  source_read          deep read of important source(s)         -> notes.md
析  prior_art_check      does the claim already exist?  (判)       -> verdict.md
析  counterevidence      what argues against the claim? (判)       -> verdict.md
析  novelty_check        is the angle new enough?       (判)       -> verdict.md
析  landscape_review     map approaches/baselines       (综)       -> landscape.md
析  benchmark_landscape  standard eval setups           (综)       -> landscape.md
创  idea_generation      generate + rank candidate claims         -> ideas.md
```

## Status values (Axis 1 lifecycle)

```
planned       Plan written (discovery.yaml exists), not executed
building      Build instrument in progress (optional stage)
executing     Execute in progress
reported      Report written, outcome being finalized
ok            terminal complete and usable by the parent
inconclusive  evidence exists but does not settle the question
blocked       missing access, missing sources, or unresolved ambiguity
```

A discovery can be reused by multiple parents. Keep `status: ok` (or `inconclusive`) and append consumers to `consumed_by`; never use `consumed` as the status.

## Report block (was `verdict`) — report to a human

The report block uses `outcome:`, NOT `status:`. The top-level `status:` is Axis-1 lifecycle progress (planned/executing/ok/...); `report.outcome` is the per-type result. Two distinct fields, deliberately different names so they never collide.

`report.outcome` per type:

```
搜               gathered      (N sources curated / read)
析-judge         supports | contradicts | inconclusive
析-synthesize    mapped        (field organized)
创               generated     (N candidates ranked)
```

Common fields: `outcome`, `summary`, `confidence` (high/medium/low/unknown). `析-judge` adds `supports_claim` / `contradicts_claim` (bool or null).

## Terminal contracts (by type)

### verdict.md — 析-judge (判) → probe

```md
# Verdict
status: supports | contradicts | inconclusive
confidence: high | medium | low

## Answer
One paragraph answering the discovery question.

## Evidence
- Full citation / URL / id — one-line finding — VERIFIED | NEEDS-VERIFICATION

## Caveats
- What this discovery did not check.
```

### landscape.md — 析-synthesize (综) → paper / idea-gen

A map, not a yes/no.

```md
# Landscape: <topic>
status: mapped
confidence: high | medium | low

## Approaches (taxonomy)
- <cluster> — what it does — exemplar refs

## Baselines / datasets / metrics      (for benchmark_landscape)
- <name> — what it measures — used by <refs>

## Gaps / open questions
- <gap> — why it is open

## References (full, verified)
1. <self-contained full citation>      (Review Output Contract rules 1-5)
```

### ideas.md — 创 → probe-open / paper-seed

A ranked candidate-claim set, not a verdict.

```md
# Ideas: <prompt>
status: generated

## Candidates (ranked)
1. <claim> — rationale — novelty: NOVEL | PARTIAL | SEEN (vs <ref>) — testability: <how a probe would test it>

## Grounding
- which 搜 / 析 folder this builds on
```

### sources.md and notes.md — 搜 (also work products inside 析)

```md
# Sources
| id | citation / URL | role | verification |
|----|----------------|------|--------------|
| S001 | <full citation or URL> | adjacent method | VERIFIED |
```

`notes.md` holds per-source extracted findings, one block per source id. In a `搜` folder these are the terminal; in an `析` folder they are work products feeding the verdict/landscape.

The full citation and verification discipline follows the Review Output Contract in `haipipe-discovery/SKILL.md` (rule 5: every id/DOI/venue VERIFIED or flagged NEEDS-VERIFICATION).

## Source records

Sources normally live as rows in `sources.md`, not as directories. Only create `sources/Sxxx_slug/` when the project must keep heavy artifacts (PDFs, HTML snapshots, per-source annotations).
