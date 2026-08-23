# `insight` · enter the Task/Insights Board

Use this procedure for `/haipipe-task insight "<question-or-topic>" [<board>]`.

## Contract

One call creates or resumes one consumer-neutral `page-type: insight` Page. It does not run a task merely because a question was named.

```text
task execution / discovery work
          │
          │ Probe, only after sources are selected
          ▼
     Insight Page: D → I → K → W
          │
          │ settled handoff through PageX
          ▼
     Paper / Application
```

## Procedure

1. Resolve the board from the explicit path, the nearest `board.md`, or the project's Task Board. Ask only if more than one plausible board remains.
2. Search the board registry and aliases for an Insight Page whose Question and Scope materially matches the request.
3. If one exists, open that Page through `haipipe-page`; never create a near-duplicate because its wording differs.
4. If none exists, create a folded Q or S Page through `haipipe-page` with `page-type: insight`, `scope: task`, and an explicit `insight-target`. Never write `application:` or `serves:` here; those two fields are what make a Page commissioned, and this Board's Pages are consumer-neutral.
5. Seed only Question and Scope, Source Map candidates, Aims, and current States. Do not pre-write K or W before evidence lands.
6. Use Probe from the Insight Page to reach Task/Discovery sources. Use PageX when another settled Page already answers part of the chain.
7. Run the Page workflow and close only under `haipipe-page-for-insight`, reading its `scope: task` column: division 1 is Origin, division 8 is Reusable Findings.

## Routing rules

- A request to execute, rerun, or calculate belongs to P-B-E-R, not this verb.
- A narrow question about one Task Folder may be answered by `qa`; promote it to an Insight Page only when the answer must be interpreted, combined, or reused.
- A Paper/Application-specific stake stays downstream. Rewrite the question in consumer-neutral language before it reaches this Board.
- This Board is where DATASET-FIRST exploration belongs. A dataset can land before any Brief exists; that work opens here, not on an Application InsightBoard, and an Application borrows it later through PageX.
- A source rerun reopens dependent Insight rows; it never silently updates a settled conclusion.

Return the Insight Page path, its target level, source status, and the next Page phase.
