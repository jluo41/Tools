# discovery.yaml — Discovery BJTR Task Manifest (v6.0 + BJTR alignment addendum)

One research article/question = one `tNN_` Discovery Task Page. `discovery.yaml`
is its Task Face manifest; `tNN_<task>.md` and its lanes are the Page Face. Neither Face
replaces the other. Level-4 Run inventory is derived from `runs/` and
`results/`, never copied into YAML.

```text
discoveries/                                  bank
└── b01_<noun>_<qualifier>/                   Block
    ├── board.md                               Discovery Board head
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
            └── summary.md | verdict.md | landscape.md
```

Every new name uses `<level-letter><NN>_<noun>_<qualifier>`. `discoveries/` is
not a Block. The path is the identity: `b01j01t01r01` compact and
`b01.j01.t01.r01` readable. A bare `01_` at any addressed level is invalid.

Full Level-4 contract: `paper-run-contract.md`.

The old 0/1/2/3 and 1/2/3/4 labels are not manifest levels. See
`bjtr-alignment.md` for the retrofit: the path is always Block bNN, Job jNN,
Task tNN, and Run rNN; D1 and Page numbers remain workflow records.

The Block is a `haipipe-board` container from creation onward. Its
`board.md` declares `board-kind: discovery-block`; the Job folders are Board
Groups and the Task folders are Board Pages. The direct `jNN_/tNN_` tree is the
membership authority. Keep the Board head and generated `board/` projection in
sync with `scripts/board_sync.py`; do not copy Run inventories, Result prose,
or Page bodies into the manifest or Board source.

New manifests point `report.evidence_bib` to the Outline-owned
`outline/evidence/bibex/` lane. A legacy root `evidence/bibex/` path may be
read during migration, but new writes must not create or refresh that lane.
The checker rejects a root `<task>/evidence/` lane in a current v6 Task.

## Discovery Page Type → route and typed record

```text
discovery_type          route    question                              typed record
----------------------  -------  ------------------------------------  ----------------
source-map              Search      what relevant sources exist?          none
source-reading          Review      what does one selected source say?    none
topic-summary           Synthesize  what is known about this topic?       summary.md optional
prior-art-verdict       Synthesize  does the named claim already exist?   verdict.md
counterevidence-review  Synthesize  what argues against the claim?        verdict.md
landscape-review        Synthesize  map approaches / disagreements / gaps landscape.md
benchmark-landscape     Synthesize  compare standard evaluation setups    landscape.md
```

The root `tNN_<task>.md` is the Page and human-facing article for every type.
Typed records are Task-side synthesis receipts, not rival Pages or Level-4
Results. Paper/Source Cards are Level-4 Result readouts. Search candidate
discovery and cross-source synthesis are Page work; only selected canonical
Subjects become Runs. Semantic direction and idea generation is handled by
sibling `haipipe-ideation` after Discovery synthesis.
Full article grammar and permitted normalization:
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
| `sources` | conditional | required for broad retrieval; stores the frozen candidate-selection policy, candidate decisions, and retrieval-order context |
| `instrument` | optional | `{needed, path}` under `scripts/` |
| `typed_record` | optional | `summary.md`, `verdict.md`, or `landscape.md` when the type owns one |
| `report` | at D1 `CLOSE` | appended outcome block; absent before CLOSE |
| `created_at`, `updated_at` | yes | quoted ISO8601 strings |

`sources.requested` may name any active Discovery worker, including the
optional `openalex` and `gemini-search` adapters. These adapters only extend
candidate coverage or metadata; they never create a Run, alter the one-Subject
per-Run cardinality, or make a candidate evidentiary without independent
identity and content verification.

The factual retrieval-coverage declaration lives in the root Task Page's
`## Source map` body, as specified by `source-format.md`; it records channels,
queries, filters, limits, and stopping rule. `sources` frontmatter stores the
machine-readable candidate rule, per-candidate decisions, and retrieval-order
context. Keep these records consistent; there is no separate YAML `coverage`
key.

Keep retrieval ranking separate from admission. A `sources.candidate_rule`
records the question-specific rule frozen at SCOPE: the topical relationship
that qualifies a source, the evidence population or source type included, any
exclusions, and the candidate cap or stopping boundary. A search rank,
citation count, venue, publication date, or provider label may guide retrieval
order or be recorded as metadata; none is an admission decision or a quality
rating by itself. State how and when those values were observed if they affect
the shortlist. If a candidate's relevance or identity cannot be determined,
leave it outside the admitted Run set and record the unresolved screening item
or return to SCOPE; do not silently relabel uncertainty as irrelevance.

For broad retrieval, freeze the exact rule and retain a disposition receipt for
each screened candidate. `candidate_rule_sha256` hashes the frozen rule text;
`candidate_rule_version` identifies its criteria revision. Each disposition
names the evaluator and timestamp, and links either to the admitted owning Run
or to a frozen candidate-record URI and SHA-256 (required for excluded or
unresolved candidates, which have no Run). This preserves what the evaluator
actually screened, not just the rule they meant to apply.

Compute `candidate_rule_sha256` over the UTF-8 bytes of the parsed YAML scalar
value, without further normalization. Compute `candidate_decisions_sha256`
over the list serialized as UTF-8 JSON with object keys sorted, no extra
whitespace, and list order preserved. Use the same JSON serialization for
`scope_snapshot_sha256`, with the frozen `question`, `discovery_type`, exact
declared source boundary from the Task Page's `## Source map`, and candidate
rule/version/hash as the object. Candidate snapshot hashes cover the exact saved provider record bytes;
`page_snapshot_sha256` covers the exact closed Page bytes encoded as UTF-8.

```yaml
sources:
  candidate_rule: >-
    Include studies that evaluate adaptive sampling for rare-phenotype
    detection; exclude generic sampling without that application.
  candidate_rule_version: "candidate-admission/1"
  candidate_rule_sha256: "sha256:<rule-text-digest>"
  candidate_rule_frozen_by: "person:<identifier>"
  candidate_rule_frozen_at: "2026-09-01T10:00:00-04:00"
  candidate_decisions:
    - subject: "doi:10.1234/example"
      disposition: admitted
      rationale: "The abstract reports an evaluated rare-phenotype method."
      decided_by: "person:<identifier>"
      decided_at: "2026-09-01T10:12:00-04:00"
      input_run:
        readable: "b02.j03.t01.r01"
        compact: "b02j03t01r01"
    - subject: "s2:record-123"
      disposition: unresolved
      rationale: "The abstract does not identify the target population."
      decided_by: "person:<identifier>"
      decided_at: "2026-09-01T10:14:00-04:00"
      candidate_snapshot:
        uri: "results/search/s2-record-123.json"
        sha256: "sha256:<record-digest>"
```

`sources.from_topic` is a read-only supporting reference to another Discovery
Task. Its Results and Bib entries are not copied into this Task's aggregate. If
one upstream paper becomes load-bearing, D1 ACQUIRE must admit a local
`paper-analysis` Run carrying the upstream Result path as provenance (or
`source-analysis` only for a genuinely non-paper Subject); only the local
completed Result Bib may enter this Task's
`outline/evidence/bibex/<task>.bib`.

No `runs:` list. No `expected_outputs:` list of per-paper files. The filesystem
is authoritative for both. No `parent` or `consumed_by` field: the Discovery
bank remains consumer-unaware.

Manifests using `type` + `role` may normalize only through the permitted map in
`page-types.md`. Idea-typed manifests are unsupported and fail validation;
there is no Idea compatibility route. Legacy group/`01_` paths must migrate to
explicit b/j/t addresses before the v6 checker accepts them. New manifests
write `discovery_type` only. If both type forms are present they must normalize
to the same value.

For an existing two-level bank, use `../scripts/migrate_bjtr.py`. Its default
mode is a no-write preview. The structural mapping is one legacy bank -> one
Board Block, each legacy Group -> a numbered `jNN_..._inquiry` Job, then each
numbered leaf -> its same-number `tNN_` Task Page. Existing source, note,
synthesis, and PDF artifacts move intact; legacy question artifacts are excluded from
the current contract;
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
    Before search, admit only studies of adaptive sampling for rare-phenotype
    detection that report an evaluated method or benchmark. Exclude generic
    sampling methods without a rare-phenotype application. Search S2 and arXiv
    for "adaptive sampling" and "rare phenotype" through 2026-09-01, screen
    the first 30 unique candidates per channel in retrieval order, and record
    citation counts with the search date for ordering only. Resolve canonical
    identity before opening a Paper Run.
  candidate_rule_version: "candidate-admission/1"
  candidate_rule_sha256: "sha256:<rule-text-digest>"
  candidate_rule_frozen_by: "person:<identifier>"
  candidate_rule_frozen_at: "2026-09-01T10:00:00-04:00"
  candidate_decisions: [] # append one disposition receipt per screened candidate
  candidate_decisions_sha256: "sha256:<decision-log-digest>"
instrument:
  needed: false
  path: ""
typed_record: verdict.md

# Appended at D1 CLOSE only:
report:
  outcome: supports
  summary: One line a human can act on.
  confidence: medium
  confidence_basis:
    supporting:
      - object: "b02.j03.t01.r01"
        locator: "Result Card § findings, Table 2"
        relation: "supports the bounded answer"
    contrary_or_qualifying: []
    limits: ["Population is limited to the reported cohort"]
  assessment:
    assessed_by: "person:<identifier> or agent:<name>/<model>/<session-id>"
    criteria_version: "discovery-confidence/v1"
    criteria_ref: "discovery-yaml-schema.md#confidence-and-evidence-axes and the frozen Task type promise"
    assessed_at: "2026-09-01T12:30:00-04:00"
    scope_snapshot_sha256: "sha256:<scope-digest>"
    page_snapshot_sha256: "sha256:<closed-page-digest>"
    candidate_decisions_sha256: "sha256:<decision-log-digest>"
    input_runs:
      - readable: "b02.j03.t01.r01"
        compact: "b02j03t01r01"
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
belong to CLOSE. Do not infer an exact current Cycle from `status`; the D1
Workflow Table and Page receipts are authoritative.

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
source-map                                          gathered
source-reading                                      reviewed
topic-summary · landscape-review · benchmark-landscape mapped
prior-art-verdict · counterevidence-review          supports | contradicts | inconclusive
```

`report.outcome` is the type-specific CLOSE result from the table above. For
topic-summary, landscape-review, and benchmark-landscape, `mapped` means the
synthesis or comparison was completed; it does not assert that a substantive
answer was established. The top-level Task `status` records the terminal
epistemic state: use `inconclusive` when all required evidence is complete and
verified but cannot establish the answer. Verdict types may instead record
`report.outcome: inconclusive` because that value is part of their outcome
set.

Common fields: `outcome`, `summary`, `confidence`, `completed_runs`,
`unresolved_runs`, and `evidence_bib`. Interpret `confidence` by `discovery_type`:
`not-applicable` for a factual `source-map`, source-extraction anchors for
`source-reading`, and synthesis anchors for topic-level types. Verdict types may add `supports_claim` and
`contradicts_claim`.

At CLOSE, `report.assessment` is required whenever an outcome, verdict, or
confidence label is assigned. It records who made the judgment, the exact
version/section that supplied its criteria, the time, a hash of the closed Page
snapshot, and the full identities of the Results considered. A typed record's
`assessment_ref` points to this same receipt; do not copy or silently revise the
judgment without a new timestamp and input snapshot. For an assessed confidence,
`assessment.criteria_version` is `discovery-confidence/v1` and
`assessment.criteria_ref` points to this section and the applicable type anchor.
For a factual `source-map`, use the frozen candidate-admission rule as the
assessment criteria; `not-applicable` is not an assessment under the confidence
rubric.
For `source-reading` and topic-level types, `report.confidence_basis` is
required and records the exact evidence objects and locators that support,
oppose, or qualify the answer, plus its stated limits. For `undetermined`, name
the conflicting or non-discriminating evidence; for `unavailable`, name the
missing input and route. Typed synthesis records point to both the basis and
receipt, and their confidence label must match `report.confidence` exactly. A
`source-map` uses `not-applicable` and has no confidence basis because it
reports coverage and candidate dispositions, not an answer-strength judgment.

The basis uses this shape; source-reading locators point into the inspected
source/Result, while synthesis locators point into admitted Results:

```yaml
confidence_basis:
  supporting:
    - object: "b02.j03.t01.r01"
      locator: "Result Card § findings, Table 2"
      relation: "supports the bounded answer"
  contrary_or_qualifying: []
  limits: ["Population is limited to the reported cohort"]
```

## Confidence and evidence axes

Use the following four records for different questions. Never substitute one
for another:

- **Retrieval coverage** is the factual channel/query/screening boundary in the
  root Task Page's frozen `## Source map` declaration: what was searched, what
  was not, filters, limits, and stopping rule. Candidate-selection rules and
  decisions are stored in `discovery.yaml#sources` and linked to that
  declaration. Do not summarize coverage as high/medium/low confidence. A
  complete sweep means complete only to that declared boundary.
- **Study appraisal** is recorded per source and criterion using the evidence
  states in `paper-analyzer`: `supported`, `partially-supported`,
  `not-supported`, `not-assessed`, or `not-applicable`, with locators or a
  reason a locator is unavailable. Do not collapse these states into a global
  study-quality score.
- **Source-extraction confidence** is the `2_review` packet's confidence that
  it faithfully represents the inspected source. It is not study quality or
  Task synthesis confidence; its separate anchors are below.
- **Synthesis confidence** (`report.confidence` and the typed summary/verdict/
  landscape header) concerns how strongly the admitted, inspected evidence
  supports the bounded answer to this Task's frozen question. It is an
  evidence-based ordinal judgment, not a probability, source-quality grade,
  search-coverage label, or assessor's general certainty.

For synthesis confidence, use these anchors:

- `high`: every load-bearing part of the bounded answer has direct support in
  verified Results; relevant contrary evidence and material limitations were
  checked; no unresolved material conflict changes the answer's scope. Use
  this only when the evidence objects directly establish the whole bounded
  answer and the remaining limits do not materially narrow it.
- `medium`: direct verified evidence supports the bounded answer, but a named
  material limitation, material partial scope match, or material gap left by
  the declared coverage boundary narrows what can be concluded. A bounded
  scope alone does not lower confidence. The limitation does not reverse the
  answer; use this when the answer remains supported but the boundary changes
  its applicable population, setting, or scope.
- `low`: the answer has only narrow or indirect support, or a material
  unresolved caveat substantially weakens it. State exactly which claim is
  tentative and what evidence would change the assessment; do not present it
  as established. Use this when evidence leans toward an answer but does not
  establish its load-bearing claim at the stated scope.
- `undetermined`: the required evidence was inspected, but conflicting or
  non-discriminating evidence does not support a defensible high/medium/low
  placement. Preserve the conflict and, once required evidence and citation
  verification are complete, use terminal Task `status: inconclusive` when the
  substantive answer cannot be established. Keep `report.outcome`
  type-specific: topic-summary remains `mapped`, while verdict types may use
  `report.outcome: inconclusive`.
- `unavailable`: the confidence assessment could not be made because required
  source access, frozen criteria, or input receipts are missing. Name the
  missing item and route; this is not a low-confidence finding or a terminal
  answer. Keep the Task blocked/open until the missing input is supplied; do
  not close it as `ok` or `inconclusive` on an unavailable assessment.

For source-extraction confidence, `high` requires direct locators for all
material extracted claims and no unresolved material reading ambiguity;
`medium` permits a bounded, named ambiguity while retaining direct locators
for the core extraction, where the ambiguity does not change the source's
meaning on a load-bearing claim; `low` means a material interpretation rests
on incomplete or indirect text and must not support a reported conclusion;
`undetermined` means inspected passages support conflicting readings, and
`unavailable` means insufficient source access and routes the Task back to
acquisition/access rather than a completed review. This field does not appraise
the study's methodological quality. Use the per-criterion evidence states for
that. Record the source locator(s), extracted claim(s), and unresolved reading
limits as the basis; do not use search coverage or downstream synthesis as its
evidence object.

The terminal `source-map` type writes a factual coverage record, not a
substantive synthesis or source-extraction judgment. Preserve the mandatory
legacy `report.confidence` key as `not-applicable` for that type; do not use
high/medium/low to rate search completeness. Its Task Page `## Source map`
body records channel/query/boundary facts; `discovery.yaml#sources` records
candidate decisions. `source-reading` uses the
source-extraction anchors above, and topic-level types use the synthesis
anchors. Each assessed judgment points `assessment.criteria_ref` at its exact
type-specific anchor; `not-applicable` is not an assessed confidence label.

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
- confidence: high | medium | low | undetermined | unavailable
- confidence_basis_ref: discovery.yaml#report.confidence_basis
- assessment_ref: discovery.yaml#report.assessment

## Synthesis
One bounded answer organized by findings, not one paragraph per paper.

## Evidence boundary
- Result links + cite keys, disagreements, and unresolved gaps.
```

### verdict.md

```md
# Verdict
- status: supports | contradicts | inconclusive
- confidence: high | medium | low | undetermined | unavailable
- confidence_basis_ref: discovery.yaml#report.confidence_basis
- assessment_ref: discovery.yaml#report.assessment

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
- confidence: high | medium | low | undetermined | unavailable
- confidence_basis_ref: discovery.yaml#report.confidence_basis
- assessment_ref: discovery.yaml#report.assessment

## Approaches
- <cluster> — explanation — Result links + cite keys

## Gaps
- <gap> — why it remains open
```

Search and every other type write their reader-facing synthesis into the root
Page Content rather than a second monolithic `notes.md`. A generated
`sources.md` may be kept as a legacy index, but it is not authority.

For all typed synthesis records, `confidence` exactly matches
`report.confidence`; `confidence_basis_ref` and `assessment_ref` point to the
corresponding report fields. The linked basis names supporting and
contrary/qualifying Result locators and material limits.

## Run/Result question receipts

Questions are answered by an existing immutable Run/Result or by a newly
admitted Paper/Source Run. The full BJTR Run id, runtime receipt, Result Card,
and any typed synthesis record are the durable receipt. A consumer records the
Supporting Run id and owns any Local Run/Result needed for a focal Page Evidence
Item. Discovery does not create a second answer bank.

## Project log events

```text
discovery.opened      {"ts", "event", "block", "job", "task", "address", "discovery_type"}
discovery.run_opened  {"ts", "event", "task", "address", "run", "trigger_kind"}
discovery.run_done    {"ts", "event", "task", "address", "run", "status", "subject"}
discovery.completed   {"ts", "event", "task", "address", "status", "outcome"}
discovery.consumed    {"ts", "event", "task", "address", "consumed_by"}
```

`discovery.consumed` is written by the consumer, never by the Discovery Folder.
