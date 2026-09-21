# Insight instance, item, and execution contract

## Runtime shape

```text
I01-<topic-instance>/
├── I01-<topic-instance>.md       topic Page and item findings
├── outline/                     existing plan and Evidence Space
├── workflow/insight.yaml        instance, dataset versions, RI intent
├── runs/r01_description.sh      normal reusable R ticket; never rewritten by RI
├── runs/ri01_description.yaml   RI ticket: points to R + freezes new dataset
└── results/ri01_description/
    ├── v001/
    │   ├── binding.yaml        immutable allocation: goal, base R, datasets
    │   ├── input.yaml          finalized evidence envelope; absent while waiting
    │   ├── runtime.yaml        status, checkpoints, hashes
    │   └── result.yaml         checked DIKW Result and RF records
    └── v002/                   later execution, preserves v001
```

Neither item nor version is a new Board/Group/Page level. Large upstream Task
output may live in a declared instance-owned store. Keep pointers and hashes
here, not a duplicate raw bank.

Local Page Evidence or Execution dependencies may coexist in `runs/` and
`results/` under their own distinct ticket stems and family receipts. They
retain their owning Run dialect and Result gate; do not add them to `items`
or recast them as Insight Results. The item audit checks their basic pairing
and delegates their domain acceptance to the producer. A ticket always has a
planned/blocked runtime receipt, even before inputs are available.

## Identity

`instance` is a stable, project-qualified research-instance id without direct
patient identifiers. `run` is the local `riNN` Insight Run stem. `base_run`
names the normal R ticket/recipe being reused. `version` is a monotonic `vNNN`
publication/execution version beneath the immutable RI binding. The full
execution id is:

```text
<instance>#<ri>@<version>
sms/patient-a-study#ri01_description@v001
```

Full id, Result path, Result hash, and base-R pointer travel together across
Folders. A new dataset binding allocates a new RI even when it points to the
same R. Changing the base R, question, target, or acceptance also allocates a
new RI. A retry of the same frozen contract appends an attempt under the same
execution. A corrected or newly reviewed publication over the unchanged RI
binding may allocate its next version. `supersedes` never relates independent
datasets. Published Results and existing R tickets are immutable. Historical
`#rNN@vNNN` item addresses remain readable as the items-v1 dialect.

## Instance manifest

`workflow/insight.yaml` is intent, not a second result/status database:

```yaml
schema: haipipe.insight-instance/v2
instance: sms/patient-a-study
topic: Message response in one longitudinal dataset
datasets:
  - id: patient-a
    version: snapshot-01
    manifest: outline/evidence/materials/dataset-manifest.yaml
    sha256: <manifest-sha256>
items:
  - run: ri01_description
    base_run:
      id: r01_description
      ticket: runs/r01_description.sh
      sha256: <base-ticket-sha256>
    question: What patterns and limits does the observed response funnel show?
    target: wisdom
    datasets: [patient-a@snapshot-01]
    expected: A sourced DIKW Result, including nulls and limitations
    acceptance: Every pattern is supported; rival explanations remain visible
```

Paths are relative to the instance unless absolute. Dataset manifests name
immutable snapshots or files, schema, window, filters, and content hashes or
immutable database snapshot ids. A manifest hash alone does not freeze a
mutable database. Freeze the queried data scope too. Keep credentials and raw
patient rows out of research manifests. A byte-identical relocated source may
use an explicit hash-preserving mapping; a changed snapshot cannot.

`datasets` is an append-only inventory of named versions. Each item declares
the versions it currently intends to use. A comparison item may declare
several datasets. Shared Task code needs no central patient roster.

## Frozen execution input

Allocation writes `binding.yaml` with schema `haipipe.insight-binding/v1`,
`instance`, `run`, `base_run`, `question`, `target`, `expected`, `acceptance`, and
full dataset bindings. Its hash goes on the planned runtime as `binding_sha256`.
It has no evidence checkpoint yet. Gather evidence in a separate working packet;
do not edit the allocation when producer or local Evidence Results arrive.

Before interpretation, use `freeze --item <ri> --version <vNNN> --evidence
<packet.yaml>` to finalize `results/<ri>/<version>/input.yaml`:

```yaml
schema: haipipe.insight-input/v2
evidence_contract: haipipe.insight-evidence/v1
instance: sms/patient-a-study
run: ri01_description
version: v001
base_run:
  id: r01_description
  ticket: runs/r01_description.sh
  sha256: <base-ticket-sha256>
question: What patterns and limits does the observed response funnel show?
target: wisdom
acceptance: Every pattern is supported; rival explanations remain visible
datasets:
  - id: patient-a
    version: snapshot-01
    manifest: outline/evidence/materials/dataset-manifest.yaml
    sha256: <manifest-sha256>
supporting_results:
  - run: <full-producing-execution-id>
    path: <accepted-result-envelope>
    sha256: <result-sha256>
    ticket: <exact-producing-Ticket>
    ticket_sha256: <ticket-sha256>
    receipt: <exact-complete-producing-receipt>
    receipt_sha256: <receipt-sha256>
recipe_calls: []
local_sources: []
# With no supporting_results: local_evidence_reason explains the local evidence.
```

The `evidence_contract` marker selects the new receipt-bound validation rules.
`freeze` always emits it; an unknown marker is invalid. Existing frozen packets
without the marker are read under their earlier evidence dialect, whether or
not they have allocation binding hashes. Do not add a marker by rewriting old
bytes; use the next explicit execution version for a revised contract.

Every new Supporting Result binding includes its native Ticket/hash and
receipt/hash, including reused support with `recipe_calls: []`. The receipt
must name that same full Run identity and an accepted terminal status. Frozen
historical packets retain their recorded dialect. `freeze` checks these
structural bindings and receipt status; the source owner and local Evidence
owner still judge scientific acceptance and typed verification.

Use `task-calls.md` for populated recipe calls. Upstream calls leave their own
receipts before their completed Results enter this final frozen interpretation
input. Earlier item dependency planning may be recorded separately. The
evidence checkpoint requires every supporting Result ready. If there are no
Supporting Results, name sufficient governed local evidence and explain why
no external numerical computation is owed.

## Runtime and Result

`runtime.yaml` records execution state:

```yaml
schema: haipipe.insight-runtime/v1
execution: sms/patient-a-study#ri01_description@v001
family: insight
operation: item
status: complete
binding_sha256: <binding-yaml-sha256>
input_sha256: <input-yaml-sha256>
result_sha256: <result-yaml-sha256>
checkpoints:
  frozen: {at: <timestamp>, receipt: input.yaml}
  evidence: {at: <timestamp>, receipt: evidence-check.md}
  reasoned: {at: <timestamp>, receipt: review.yaml}
  published: {at: <timestamp>, receipt: result.yaml}
attempts: [{attempt: 1, status: complete}]
```

Checkpoint and review receipt paths are relative to the execution directory.
`result.yaml` contains `schema: haipipe.insight-result/v1`, the same
`execution`, `target`, `outcome: accepted | insufficient | rejected`, and
`review: {verdict, receipt}`. An accepted Result requires a passing independent
review receipt; an exit code or schema check is insufficient. Use
`review: {verdict: pass, receipt: review.yaml}` and a typed local receipt:

```yaml
schema: haipipe.insight-review/v1
author: <actual-author-session-or-person>
reviewer: <different-independent-reviewer-session-or-person>
verdict: pass
input_sha256: <frozen-input-file-hash>
candidate_sha256: <candidate_digest-from-insight_items.py>
checked: [source fidelity, DIKW trace, rivals and boundaries]
```

`candidate_digest(result)` hashes canonical sorted compact UTF-8 JSON of the
Result mapping excluding `review`, avoiding a circular review link. The
reviewer checks this exact candidate and input. Changed content requires a
new review. Receipt identity is an auditable assertion, not cryptographic
proof of independence; a caller cannot self-certify a scientific review by
filling these fields. Use a genuinely independent reviewer and preserve its
review record. The checker only validates the receipt structure and binding.

The DIKW shape:

```yaml
D:
  - {id: D1, text: <dated observation>, parents: [source:0]}
I:
  - {id: I1, text: <pattern or null>, parents: [D1]}
K:
  - id: K1
    text: <bounded proposition>
    parents: [I1]
    strength: <evidence strength>
    rivals: [<alternative explanation>]
    boundary: <population and measurement limits>
W:
  - {id: W1, text: <applicability and unsafe inference>, parents: [K1]}
RF:
  - id: RF1
    text: <reusable finding without an added design consequence>
    parents: [W1]
    strength: <evidence strength>
    boundary: <scope limits>
```

`source:0` addresses `supporting_results[0]`; `dataset:0` may support dataset
inventory observations, not new statistics computed in the Page. Optional
`local_sources` use `local:0` and the same path/hash binding grammar. Rows cite
the immediately preceding rung. RF cites the declared target rung when the
item stops below Wisdom; only Wisdom-targeted RF can use the I1/I5 bridge.
Accepted Results contain every rung through the target. An insufficient or
rejected Result records `reason` and exports no accepted RF. A supported null
is an accepted finding; insufficient evidence is a different outcome.

## Exact consumer reference

```yaml
instance: sms/patient-a-study
item: ri01_description
insight_run: ri01_description
base_run:
  id: r01_description
  ticket: runs/r01_description.sh
  sha256: <base-ticket-sha256>
version: v001
finding: RF1
result: <consumer-resolved-result.yaml>
sha256: <result-sha256>
```

The consumer states how the bounded finding supports its decision. Resolve
the exact Result, hash, item-level acceptance, DIKW trace, and source versions.
Never resolve `latest`, accept all items because the Page is complete, or
substitute a sibling patient's Result. Existing citations remain pinned when
v002 appears; affected current-use bindings are stale until the consumer
rechecks applicability. Unchanged sibling items remain usable.

`cite --item <run> --version <vNNN> --finding <RF> --historical` resolves an
exact historical pin independently of later executions. It explicitly emits
`applicability: historical-needs-recheck`, not current-use approval. A failing
v002 cannot invalidate an intact v001 pin. Normal `cite` requires matching
current intent and emits `current-binding-matches`; neither flag grants
scientific or Design authority.

To reuse historical evidence for a new current decision, the consumer records
an applicability decision in its own Outline log: exact source packet, frozen
source data scope, current consumer/input version, applicable boundaries,
reviewer, decision (`applicable` or `reject`), and timestamp. This receipt
does not rewrite the old source Result or its current item intent. Application
I1/I5 signature rules still apply. No scheduler or automatic consumer-reopening
service is supplied by this read-only checker; the owner performs that review.

## Inspection

`scripts/insight_items.py bind ...` is the deterministic allocation door: it
chooses the next `riNN`, writes the RI YAML Ticket and `v001/binding.yaml`,
creates a planned runtime receipt, and upgrades the manifest to v2.
`freeze` later validates and seals complete evidence into `input.yaml`; it never
overwrites a frozen input. It never
executes or edits the base R. `scripts/insight_items.py check <folder>`
validates the materialized contract.
`table` projects item, question, target, input versions, current execution,
checkpoint, outcome, and last accepted findings. A proposed item does not
become a completed Run without a ticket and receipt. A higher incomplete
version shows current work without hiding the last accepted historical one.
The checker cannot judge scientific correctness or provide a human signature.
It also cannot detect a coordinated rewrite of all payloads and their hashes
without a trusted prior publication record. The execution owner must preserve
published versions in append-only/version-controlled storage and allocate new
versions under a lock when multiple callers commission the same item.
