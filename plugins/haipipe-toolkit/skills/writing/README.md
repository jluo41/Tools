# writing

The prose layer: draft from an approved plan and evidence, revise existing
writing within its authorized scope, or evaluate a candidate. Return readable
prose, located findings and genuine changes in the host's record format.

```
writing/
└── haipipe-writing/  draft/revise/evaluate → selected methods → review → host return
```

**Scope.** Writing provides prose work for Paper, Page, Insight, Design and
standalone files. The host owns its plan, Evidence, Run state and acceptance.
Writing owns the scoped candidate, genuine change trace and evaluation.

When a host already has an approved outline and evidence, read
`haipipe-writing/ref/realize-from-plan.md`. The host keeps ownership of the
outline, claims, and evidence; this worker turns one bounded plan slice into
reviewable prose and applies the shared change-record contract.

**Page integration.** Section and Paragraph Runs use the same
[Writing request](haipipe-writing/ref/writing-request.md), with their actual
scope and existing Run/Version/Step. Their host stores clean Before/After and
the review; method calls never allocate additional Runs.

**External capabilities.** Select writers, style inputs or evaluators through
[the method adapter contract](haipipe-writing/ref/method-adapter-contract.md)
and [catalog](haipipe-writing/ref/writing-methods.yaml). Add an adapter and
catalog entry for a new capability; no Page workflow change is needed.
The catalog does not install or launch a skill. Missing required methods block;
optional ones are visibly skipped. Base writing works with no external methods.

**Evaluation.** [The shared rubric](haipipe-writing/ref/evaluation-rubric.md)
covers Mechanics, Function, Evidence and Readability. Writing evaluates,
revises within its budget and evaluates the changed candidate again. Page
CHECK references the same base while retaining independent whole-Page review.

**Retirement (2026-09-20).** The standalone HAI humanizer is removed from skill
discovery. Shared Writing retains its meaning/venue protections and useful
rhythm diagnostics; the selected academic-humanizer adapter requires an actual
external entry. Historical material remains in Git. See
[provenance](haipipe-writing/ref/method-attribution.md).

Board hosts use the computed `✎` record. Legacy Paper generation remains
available, but its Note format is not validated by `wdiff.py check`. See
[change-record §4](haipipe-writing/ref/change-record.md#4--the-bridge-to-haipipe-paper).
