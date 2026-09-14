# Page Run · post-run analysis

Post-run analysis is a derived, output-only review of a completed Page Run.
It is not another human-feedback Step and it never becomes a second prose or
planning authority.

## Trigger

Prepare exactly one analysis Task proposal after the person explicitly closes
a Page Run. Do not prepare it after every Step. If the analysis needs a
background worker, sub-agent, or substantial model/tool budget, ask for
explicit approval before dispatching it. The next Page Run may begin
immediately and must not wait for approval or this Task.

The host should launch it through the supported background-agent or Task
mechanism only after approval when the work is heavy. If no such mechanism is
available, or approval has not arrived, record `analysis: deferred` or
`analysis: awaiting-approval` and do not imply that work is running.

## Input

The Task reads the closed Page Run's immutable Version journal and records its
exact input hash. It may read the Page-local Context and the accepted planning
slice needed to interpret feedback. It must not read an open future Run as if
that Run were part of the closed decision.

```text
closed Page Run
  └── results/<page-run>/v001.md · SHA-256 <frozen>
          │
          ▼
post-run analysis Task · native rNN identity
```

## Output

The analysis Task owns its own ordinary Task Run records inside the Page
Folder:

```text
runs/rNN_page-run-analysis.md
results/rNN_page-run-analysis/
├── runtime.yaml
└── result.md
```

`result.md` may contain:

- a compact inventory of feedback by Step;
- provisional categories such as readability, concept, tone, terminology, or
  punctuation;
- repeated preference signals with exact supporting Step references;
- unresolved, conflicting, or low-confidence signals;
- recommendations for a future Page-local rule or a possible shared rule.

Every recommendation remains `candidate` until the person explicitly promotes
it. Analysis does not silently update Writing DNA, Requirements, shared policy,
the Shape, or Page Content.

## Write boundary

The analysis Task may write only its own Task Result and a small status pointer
from the closed Page Run's `working.md` or `runtime.yaml`. It must never edit:

- the closed Version journal or any earlier Step;
- the current candidate preview or accepted prose;
- the Outline Shape or Evidence contract;
- Page source, delivery, Web, LaTeX, or Word outputs;
- a shared preference or policy file.

If analysis discovers a possible prose or plan problem, it writes a
recommendation. A later human request opens the appropriate Page Run or Shape
route; analysis never applies that change on its own.

## Failure and continuation

Analysis failure is separate from Page Run closure. Mark the analysis Task
`failed` or `Held`, preserve its input hash, and keep the closed Page Run
closed. A later retry must create a new analysis Task or an explicitly recorded
retry Result; it must not rewrite the closed Page Run.
