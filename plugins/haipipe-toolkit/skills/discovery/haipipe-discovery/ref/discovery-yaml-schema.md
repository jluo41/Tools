# discovery.yaml — Discovery Topic Task Manifest (v4.0)

One research Topic = one Discovery Task Page Folder. `discovery.yaml` is the
Task Face manifest; `<topic>.md` and its lanes are the Page Face. Neither Face
replaces the other. Level-4 Run inventory is derived from `runs/` and
`results/`, never copied into YAML.

```text
<topic>/
├── <topic>.md                       Page Face
├── discovery.yaml                   Task Face manifest
├── outline/                         optional
├── evidence/bibex/<topic>.bib       derived Page Evidence Bib
├── scripts/                         optional instrument
├── runs/<RUNNAME>.sh
├── results/<RUNNAME>/
├── verdict.md | landscape.md | ideas.md   optional type terminal
└── QA/                              optional readable digests
```

Full Level-4 contract: `paper-run-contract.md`.

## Types × roles → topic-level terminal

```text
type    role                 question                          terminal
------  -------------------  --------------------------------  ----------------
Search  source_gather        what sources exist?               <topic>.md source map
Search  source_read          what do the key sources say?      <topic>.md synthesis
Review  prior_art_check      does the claim already exist?     verdict.md
Review  counterevidence      what argues against the claim?    verdict.md
Review  landscape_review     map approaches / baselines        landscape.md
Review  benchmark_landscape  standard evaluation setups        landscape.md
Idea    idea_generation      generate + rank candidate claims  ideas.md
Idea    novelty_check        is this idea new enough?          verdict.md
```

Paper/Source Cards are Level-4 Result readouts, not topic terminals. Search
candidate discovery is topic-level work; only selected canonical Subjects
become Runs. Idea generation is also topic-level work; papers used to ground or
check novelty still become Runs.

## Fields

| Field | Required | Notes |
|---|---|---|
| `kind` | yes | always `discovery` |
| `id` | yes | `<GROUP-id>.<NN>`, mirrors the path |
| `type` | yes | `Search` / `Review` / `Idea` |
| `role` | yes | table above |
| `group` | yes | `{id, slug, title}` |
| `slug`, `title` | yes | folder slug and human title |
| `page` | yes | root Page markdown filename |
| `status` | yes | topic lifecycle status |
| `question` | yes | external-world Topic question |
| `sources` | optional | coverage and candidate-selection policy |
| `instrument` | optional | `{needed, path}` under `scripts/` |
| `terminal` | yes | topic-level terminal path |
| `report` | at Report | appended outcome block; absent before Report |
| `created_at`, `updated_at` | yes | quoted ISO8601 strings |

No `runs:` list. No `expected_outputs:` list of per-paper files. The filesystem
is authoritative for both. No `parent` or `consumed_by` field: the Discovery
bank remains probe-unaware.

## Skeleton

```yaml
kind: discovery
id: P01.02
type: Review
role: prior_art_check
group:
  id: P01
  slug: rare-phenotype-lift
  title: Rare phenotype lift
slug: prior-art-adaptive-sampling
title: Does adaptive sampling for rare phenotypes already exist?
page: prior-art-adaptive-sampling.md
status: planned
created_at: "2026-09-01T10:00:00-04:00"
updated_at: "2026-09-01T10:00:00-04:00"

question: |
  Has adaptive sampling for rare-phenotype detection been published?
sources:
  requested: [research-lit, semantic-scholar]
  from_topic: ""
  local_first: true
  verification_required: true
  candidate_rule: >-
    Admit a source as a Paper Run only after canonical identity is resolved and
    it is relevant enough to analyze.
instrument:
  needed: false
  path: ""
terminal: verdict.md

# Appended at Report only:
report:
  outcome: supports
  summary: One line a human can act on.
  confidence: medium
  completed_runs: 7
  unresolved_runs: 1
  evidence_bib: evidence/bibex/prior-art-adaptive-sampling.bib
```

## Lifecycle status

```text
planned -> building (optional) -> executing -> reported -> ok | inconclusive | blocked
```

Topic status and Paper Run status are different axes. A Topic may report an
`inconclusive` outcome while every admitted Paper Run is technically complete.
Conversely, unresolved Runs prevent `status: ok` when they are material to the
question.

## Report outcomes

```text
Search             gathered
Review-judge       supports | contradicts | inconclusive
Review-synthesize  mapped
Idea-generate      generated
Idea-novelty       novel | partial | preempted | inconclusive
```

Common fields: `outcome`, `summary`, `confidence`, `completed_runs`,
`unresolved_runs`, and `evidence_bib`. Judge roles may add `supports_claim` and
`contradicts_claim`.

## Topic terminal templates

### verdict.md

```md
# Verdict
- status: supports | contradicts | inconclusive
- confidence: high | medium | low

## Answer
One paragraph answering the Topic question.

## Evidence
- [r03_author2025_slug](results/r03_author2025_slug/r03_author2025_slug.md)
  — what this Result establishes — cite: @Key

## Caveats
- What this Topic did not establish.
```

### landscape.md

```md
# Landscape: <topic>
- confidence: high | medium | low

## Approaches
- <cluster> — explanation — Result links + cite keys

## Gaps
- <gap> — why it remains open
```

### ideas.md

```md
# Ideas: <prompt>

## Candidates
1. <claim> — rationale — novelty — testability — grounding Result links
```

Search writes its source map and synthesis into the Page Content rather than a
second monolithic `notes.md`. A generated `sources.md` may be kept as a legacy
index, but it is not authority.

## QA digests

`QA/` remains optional and is governed by `fn/qa.md`. A QA answer anchors to
stable Result Cards or topic terminal sections:

```md
# Q — <self-contained question>
- state: answered

## Answer
Plain answer. Anchors: [→ results/r03_x/r03_x.md#Facts] [→ verdict.md#Evidence]

## Caveats
- What this does not establish.

## Not-done
- What remains unresolved and why.
```

## Project log events

```text
discovery.opened      {"ts", "event", "discovery_group", "discovery_folder", "type", "role"}
discovery.run_opened  {"ts", "event", "discovery_folder", "run", "trigger_kind"}
discovery.run_done    {"ts", "event", "discovery_folder", "run", "status", "subject"}
discovery.completed   {"ts", "event", "discovery_folder", "status", "outcome"}
discovery.consumed    {"ts", "event", "discovery_folder", "consumed_by"}
```

`discovery.consumed` is written by the consumer, never by the Discovery Folder.
