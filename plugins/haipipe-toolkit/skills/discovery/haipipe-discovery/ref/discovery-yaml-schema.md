# discovery.yaml — Discovery Folder Schema (v2, two-axis, 3 types: Search Review Idea)

## What this file is

`discovery.yaml` is the Plan + Report spec at the root of every discovery-folder. A discovery is one research topic = one folder, a sibling of a task-folder, running the uniform `Plan → Build(opt) → Execute → Report` lifecycle. `type:` names the folder type (`Search`/`Review`/`Idea`); the lifecycle is identical for all three.

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
sources.md       Execute work product (Search: search)
notes.md         Execute work product (Search: read)
verdict.md | landscape.md | ideas.md   Execute TERMINAL (by type)
```

No local event log belongs here. Orchestration events go to `_haipipe/project.log.jsonl`.

## The two axes as fields

```
type:    Axis 2 — the folder type     Search | Review | Idea      (decides the Execute terminal)
status:  Axis 1 — lifecycle progress  planned | building | executing | reported | ok | inconclusive | blocked
```

## Type values (Axis 2)

| type | IPO | Execute terminal | roles |
|---|---|---|---|
| Search | INPUT | `sources.md` (+ `notes.md`) | source_gather, source_read |
| Review | PROCESS | `verdict.md` (judge) / `landscape.md` (synthesize) | prior_art_check, counterevidence, novelty_check → verdict; landscape_review, benchmark_landscape → landscape |
| Idea | OUTPUT | `ideas.md` | idea_generation |

`type` is authoritative for the terminal. For `Review`, `role` picks the verdict-vs-landscape branch.

## Top-level fields

| Field | Type | Required | Notes |
|---|---|---|---|
| kind | string | yes | always `discovery` |
| id | string | yes | e.g. `L01.03` |
| **type** | enum | yes | **NEW** — folder type (Axis 2): `Search`/`Review`/`Idea` |
| role | enum | yes | refinement within `type` (esp. Review); see Role Values |
| group | mapping | yes | discovery-group metadata |
| slug | string | yes | discovery-folder slug |
| title | string | yes | human-readable title |
| status | enum | yes | lifecycle progress (Axis 1) |
| parent | mapping | opt | delivery/probe/manual consumer |
| question | string | yes | external-world question (Plan) |
| sources | mapping | opt | search scope + selected refs (Plan); for `Review`, may reference a `Search` folder |
| **build** | mapping | opt | **NEW** — optional instrument (`needed` + `artifact`) |
| expected_outputs | list | yes | files expected; terminal depends on `type` |
| **report** | mapping | yes | **RENAMED from `verdict`** — report-to-human outcome block, generalized across types |
| consumed_by | list | opt | project-relative parents that used the terminal |
| created_at | string | yes | quoted ISO8601 |
| updated_at | string | yes | quoted ISO8601 |

## Skeleton (Review type, synthesize flavor)

```yaml
kind: discovery
id: L01.03
type: Review                 # Search | Review | Idea
role: landscape_review   # picks landscape.md (synthesize) vs verdict.md (judge)
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
  from_source_folder: ""    # optional: a Search folder to reuse instead of searching inline
  local_first: true
  verification_required: true
build:
  needed: false             # true only for a systematic query string / extraction schema
  artifact: ""              # e.g. build/query-strategy.md
expected_outputs:
  - sources.md
  - notes.md
  - landscape.md            # terminal for Review-synthesize (verdict.md for Review-judge)

# --- Report (outcome, report-to-human) ---
report:
  outcome: mapped           # per-type values below (NOT the top-level lifecycle `status:`)
  summary: ""
  confidence: medium
  supports_claim: null      # Review-judge only
  contradicts_claim: null   # Review-judge only

consumed_by: []
```

A `Search` folder omits the `report.supports_claim`/`contradicts_claim` fields and ends at `sources.md`/`notes.md`; an `Idea` folder ends at `ideas.md` and usually sets `sources.from_source_folder` to the `Search`/`Review` it builds on.

## Role values (refinements of type)

```
Search  source_gather        broad source scan, curated list          -> sources.md
Search  source_read          deep read of important source(s)         -> notes.md
Review  prior_art_check      does the claim already exist?  (judge)       -> verdict.md
Review  counterevidence      what argues against the claim? (judge)       -> verdict.md
Review  novelty_check        is the angle new enough?       (judge)       -> verdict.md
Review  landscape_review     map approaches/baselines       (synthesize)       -> landscape.md
Review  benchmark_landscape  standard eval setups           (synthesize)       -> landscape.md
Idea  idea_generation      generate + rank candidate claims         -> ideas.md
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
Search               gathered      (N sources curated / read)
Review-judge         supports | contradicts | inconclusive
Review-synthesize    mapped        (field organized)
Idea               generated     (N candidates ranked)
```

Common fields: `outcome`, `summary`, `confidence` (high/medium/low/unknown). `Review-judge` adds `supports_claim` / `contradicts_claim` (bool or null).

## Terminal contracts (by type)

### verdict.md — Review-judge (judge) → probe

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

### landscape.md — Review-synthesize (synthesize) → paper / idea-gen

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

### ideas.md — Idea → probe-open / paper-seed

A ranked candidate-claim set, not a verdict.

```md
# Ideas: <prompt>
status: generated

## Candidates (ranked)
1. <claim> — rationale — novelty: NOVEL | PARTIAL | SEEN (vs <ref>) — testability: <how a probe would test it>

## Grounding
- which Search / Review folder this builds on
```

### sources.md and notes.md — Search (also work products inside Review)

```md
# Sources
| id | citation / URL | role | verification |
|----|----------------|------|--------------|
| S001 | <full citation or URL> | adjacent method | VERIFIED |
```

`notes.md` holds per-source extracted findings, one block per source id. In a `Search` folder these are the terminal; in a `Review` folder they are work products feeding the verdict/landscape.

The full citation and verification discipline follows the Review Output Contract in `haipipe-discovery/SKILL.md` (rule 5: every id/DOI/venue VERIFIED or flagged NEEDS-VERIFICATION).

## Source records

Sources normally live as rows in `sources.md`, not as directories. Only create `sources/Sxxx_slug/` when the project must keep heavy artifacts (PDFs, HTML snapshots, per-source annotations).
