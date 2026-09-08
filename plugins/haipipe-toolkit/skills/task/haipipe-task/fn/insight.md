# `insight` · enter the Task/Insights Board

Use this procedure for `/haipipe-task insight "<topic>" [<board>]`.

## Contract

One call creates or resumes a consumer-neutral topic/data instance Page and
its requested Insight Items. Each item is a local Run work unit with immutable
execution versions. It does not run an entire Task merely because a topic was
named. Load `haipipe-page-insight` and its item workflow table.

```text
task execution / discovery work
          │
          │ Supporting Run Results selected by SURVEY
          ▼
     Insight instance: item Runs, each with D → I → K → W
          │
          │ settled Reusable Finding as a reusable Result
          ▼
     Paper / Application
```

## Procedure

1. Resolve the board from the explicit path, the nearest `board.md`, or the project's Task Board. Ask only if more than one plausible board remains.
2. Search the board registry and aliases for an Insight instance whose topic
   and data context match. Then match the requested question to an item.
3. If one exists, open that Page through `haipipe-page`; never create a near-duplicate because its wording differs.
4. If none exists, create one `I<NN>-<slug>/` Folder through `haipipe-page`;
   its readable face is `I<NN>-<slug>.md` with `page-type: insight`,
   `scope: task`, `insight-layout: items-v1`, and `insight-instance:`. Declare
   snapshot inputs and item intent in `workflow/insight.yaml`. Each item has
   its own target and acceptance, not a new Page. Never write `application:`
   or `serves:` here; those fields would commission work, while this Board's
   Pages are consumer-neutral.
5. Seed topic/scope, proposed items, source candidates, and Aims. Do not
   pre-write K/W or claim a Run exists before its ticket and receipt exist.
6. In SURVEY, name Task/Discovery sources by full Supporting Run id and freeze
   any governed page-local source in the Local Input. LAND completes the
   Supporting Runs and one local Page Evidence Item Run per make-item; it never
   reads a producing Folder invisibly.
7. Follow the item workflow's bind/evidence/reason/publish checkpoints and the
   shared Page workflow. Content is Origin / Instance and Scope / Insight
   Items / Synthesis / Reusable Findings. Items close independently; update
   the Page synthesis from exact accepted Results. Return the generated item
   table and exact instance/item/version/RF references.

## Routing rules

- A requested calculation is dispatched to a named supporting Task execution
  under P-B-E-R. The Insight item supplies frozen input and output scope via
  the shared recipe protocol; it does not mutate the producer's default run.
- A narrow question about one Task Folder uses its ordinary Run/Result lifecycle; promote it to an Insight Page only when the evidence must be interpreted, combined, or reused.
- A Paper/Application-specific stake stays downstream. Rewrite the question in consumer-neutral language before it reaches this Board.
- This Board is where DATASET-FIRST exploration belongs. A dataset can land
  before any Brief exists; that work opens here, not on an Application
  InsightBoard, and an Application later reuses the settled Result through its
  own Supporting/local Run graph.
- A Reusable Finding is consumer-neutral and unsigned. It may become evidence
  for an Application-owned I1→I5 bridge, but it never binds directly to Design
  and never becomes a Design Handoff by being reused.
- A source rerun reopens dependent Insight rows; it never silently updates a settled conclusion.

Return the instance Page, item table, source status, exact completed item
Results, and the next item checkpoint/Page phase. Existing single-chain Pages
use the contract's migration procedure; do not fabricate historical Runs.
