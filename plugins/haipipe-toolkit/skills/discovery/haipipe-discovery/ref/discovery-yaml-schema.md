# discovery.yaml — Discovery BJTR Task Manifest (v6.0)

One research article/question = one `tNN_` Discovery Task Page. `discovery.yaml`
is its Task Face manifest; `tNN_<task>.md` and its lanes are the Page Face. Neither Face
replaces the other. Level-4 Run inventory is derived from `runs/` and
`results/`, never copied into YAML.

```text
discoveries/                                  bank
└── b01_<noun>_<qualifier>/                   Block
    └── j01_<noun>_<qualifier>/               Job
        └── t01_<noun>_<qualifier>/           Task Page
            ├── t01_<noun>_<qualifier>.md
            ├── discovery.yaml
            ├── outline/                      Page process + Evidence Workspace
            │   └── evidence/
            │       └── bibex/t01_<...>.bib   derived
            ├── scripts/                      optional instrument
            ├── runs/r01_<author><year>_<paper>.sh
            ├── results/r01_<author><year>_<paper>/
            ├── summary.md | verdict.md | landscape.md | ideas.md
            └── QA/
```

Every new name uses `<level-letter><NN>_<noun>_<qualifier>`. `discoveries/` is
not a Block. The path is the identity: `b01j01t01r01` compact and
`b01.j01.t01.r01` readable. A bare `01_` at any addressed level is invalid.

Full Level-4 contract: `paper-run-contract.md`.

New manifests point `report.evidence_bib` to the Outline-owned
`outline/evidence/bibex/` lane. A legacy root `evidence/bibex/` path may be
read during migration, but new writes must not create or refresh that lane.
The checker rejects a root `<task>/evidence/` lane in a current v6 Task.

## Discovery Page Type → route and typed record

```text
discovery_type          route    question                              typed record
----------------------  -------  ------------------------------------  ----------------
source-map              Search   what relevant sources exist?          none
source-reading          Search   what do the selected sources say?     none
topic-summary           Review   what is known about this topic?       summary.md optional
prior-art-verdict       Review   does the named claim already exist?   verdict.md
counterevidence-review  Review   what argues against the claim?        verdict.md
landscape-review        Review   map approaches / disagreements / gaps landscape.md
benchmark-landscape     Review   compare standard evaluation setups    landscape.md
ideation                Idea     generate + rank candidate claims      ideas.md
novelty-verdict         Idea     is this idea new enough?              verdict.md
```

The root `tNN_<task>.md` is the Page and human-facing article for every type.
Typed records are Task-side synthesis receipts, not rival Pages or Level-4
Results. Paper/Source Cards are Level-4 Result readouts. Search candidate
discovery, topic synthesis, and idea generation are Page work; only selected
canonical Subjects become Runs. Full article grammar and legacy mapping:
`page-types.md`.

## Fields

| Field | Required | Notes |
|---|---|---|
| `version` | yes | manifest schema version; `6` for this contract |
| `kind` | yes | always `discovery` |
| `address` | yes | readable `bNN.jNN.tNN`, derived from the path |
| `address_compact` | yes | compact `bNNjNNtNN`, derived from the same path |
| `discovery_type` | yes | one canonical article form from the table above |
| `block` | yes | `{id: bNN, slug, title}` matching the Block folder |
| `job` | yes | `{id: jNN, slug, title}` matching the Job folder |
| `task` | yes | `{id: tNN, slug, title}` matching the Task folder |
| `page` | yes | exactly `<task-folder-name>.md` |
| `status` | yes | Task Page lifecycle status |
| `question` | yes | external-world research question |
| `sources` | optional | coverage and candidate-selection policy |
| `instrument` | optional | `{needed, path}` under `scripts/` |
| `typed_record` | optional | `summary.md`, `verdict.md`, `landscape.md`, or `ideas.md` when the type owns one |
| `report` | at CLOSE | appended outcome block; absent before CLOSE |
| `created_at`, `updated_at` | yes | quoted ISO8601 strings |

No `runs:` list. No `expected_outputs:` list of per-paper files. The filesystem
is authoritative for both. No `parent` or `consumed_by` field: the Discovery
bank remains probe-unaware.

Legacy manifests using `type` + `role` remain readable through the exact map in
`page-types.md`. Legacy group/`01_` paths remain inspectable but must migrate to
explicit b/j/t addresses before the v6 checker accepts them. New manifests
write `discovery_type` only. If both type forms are present they must normalize
to the same value.

For an existing two-level bank, use `../scripts/migrate_bjtr.py`. Its default
mode is a no-write preview. The structural mapping is one legacy bank -> one
Board Block, each legacy Group -> a numbered `jNN_..._inquiry` Job, then each
numbered leaf -> its same-number `tNN_` Task Page. Existing source, note,
synthesis, QA, and PDF artifacts move intact;
the migrator never manufactures historical Paper Runs from them.
A legacy `report:` preserves the old outcome but supports only `reported` after
structural migration; old `review`, `ok`, and `inconclusive` do not prove that
the v6 Result-backed evidence map is closed. Without that receipt, those states
truthfully reopen as `executing`. Migration never invents a Report or Paper Run
to defend an old status token. `--repair-pages` refreshes only deterministic
migration Pages and preserves their human-edited title line.

## Skeleton

```yaml
# path: discoveries/b01_rare_phenotype_lift/j02_adaptive_sampling_prior_art/t01_adaptive_sampling_verdict/
version: 6
kind: discovery
address: b01.j02.t01
address_compact: b01j02t01
discovery_type: prior-art-verdict
block:
  id: b01
  slug: rare_phenotype_lift
  title: Rare phenotype lift
job:
  id: j02
  slug: adaptive_sampling_prior_art
  title: Adaptive sampling prior-art inquiry
task:
  id: t01
  slug: adaptive_sampling_verdict
  title: Does adaptive sampling for rare phenotypes already exist?
page: t01_adaptive_sampling_verdict.md
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
typed_record: verdict.md

# Appended at CLOSE only:
report:
  outcome: supports
  summary: One line a human can act on.
  confidence: medium
  completed_runs: 7
  unresolved_runs: 1
  evidence_bib: outline/evidence/bibex/t01_adaptive_sampling_verdict.bib
```

## Lifecycle status

```text
planned -> building (optional) -> executing -> reported -> ok | inconclusive | blocked
```

This v6 field is a backward-compatible summary, not the D1 Cycle identity:
`planned` roughly covers SCOPE, `building` covers optional PREPARE,
`executing` may cover ACQUIRE or SYNTHESIZE, and reported/terminal values
belong to CLOSE. Do not infer an exact current Cycle from `status`. A later
schema migration will split workflow state/current Cycle from epistemic
`report.outcome`; until then the Workflow Table and receipts are authoritative.

Task Page status and Paper Run status are different axes. A Task Page may report an
`inconclusive` outcome while every admitted Paper Run is technically complete.
Conversely, unresolved Runs prevent `status: ok` when they are material to the
question.

Terminal classification is exact: `blocked` means an operational or gate
dependency remains (including citation-verification debt); `inconclusive`
means all admitted evidence completed but could not establish the substantive
answer; `ok` means every load-bearing Aim is met. Both epistemic outcomes
require every promoted citation to be verified; otherwise the outcome is
`blocked`. A non-load-bearing limitation may be recorded without becoming a
held load-bearing Aim.

## CLOSE outcomes

```text
source-map · source-reading                        gathered
topic-summary · landscape-review · benchmark-landscape mapped
prior-art-verdict · counterevidence-review        supports | contradicts | inconclusive
ideation                                             generated
novelty-verdict                                     novel | partial | preempted | inconclusive
```

Common fields: `outcome`, `summary`, `confidence`, `completed_runs`,
`unresolved_runs`, and `evidence_bib`. Verdict types may add `supports_claim` and
`contradicts_claim`.

For terminal `ok` or `inconclusive`, all common fields are mandatory,
`completed_runs` and `unresolved_runs` must equal the runtime inventory, and
`evidence_bib` must be exactly the canonical same-stem path under
`outline/evidence/bibex/`. The root Page must also carry a closed `✅` state,
with no active Aim. A preserved legacy `reported` receipt may omit new
reconciliation fields, but every field it does carry must still be truthful.

## Typed record templates

### summary.md

```md
# Topic summary: <topic>
- confidence: high | medium | low

## Synthesis
One bounded answer organized by findings, not one paragraph per paper.

## Evidence boundary
- Result links + cite keys, disagreements, and unresolved gaps.
```

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

Search and every other type write their reader-facing synthesis into the root
Page Content rather than a second monolithic `notes.md`. A generated
`sources.md` may be kept as a legacy index, but it is not authority.

## QA digests

`QA/` remains optional and is governed by `fn/qa.md`. A QA answer anchors to
stable Result Cards, root Page sections, or typed-record sections:

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
discovery.opened      {"ts", "event", "block", "job", "task", "address", "discovery_type"}
discovery.run_opened  {"ts", "event", "task", "address", "run", "trigger_kind"}
discovery.run_done    {"ts", "event", "task", "address", "run", "status", "subject"}
discovery.completed   {"ts", "event", "task", "address", "status", "outcome"}
discovery.consumed    {"ts", "event", "task", "address", "consumed_by"}
```

`discovery.consumed` is written by the consumer, never by the Discovery Folder.
