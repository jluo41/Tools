# One selected asset, many consumers
state: ✅ SETTLED
owner: JL
method: keep evidence and rendering reusable while letting each consumer own its own surrounding semantics

## Question
Can the same Display unit serve Paper, slides, posters, and HTML?

Yes, after one asset is selected.
Each consumer projects that asset through its own adapter rather than recomputing or duplicating the underlying evidence.

## Diagram
```text
Task evidence ─► Intake ─► recipe ─► selected asset
                                       │
                       ┌───────────────┼────────────────┐
                       ▼               ▼                ▼
                    Paper float      slides            poster / HTML
                  caption + label   local layout       local layout
```

## Content
### Reuse the result, not the consumer wrapper
The asset and rebuild recipe can be reused.
Caption, numbering, placement, and nearby explanation belong to the consumer that presents the result.

### Do not create a second data pipeline
A slide or poster may crop, resize, or arrange an asset.
It must not silently create a different data subset or a new untracked numerical result.

## Items to Finish
- [x] 🔁 State the one-content-many-projections model
      The generic unit contract is source-agnostic and consumer adapters own placement.
- [x] 🧱 Keep consumer wrappers separate
      Paper wrapper semantics remain Paper-owned even when another consumer reuses the asset.

## Where we are
The content-plan specification gives non-paper consumers a shared bundle vocabulary.

## Files
- `display/ref/content-plan-spec.md`
  Consumer-plan contract.
- `display/ref/display-unit-output-contract.md`
  Reusable bundle contract.

## Law
Law: Reuse selected evidence and assets; never duplicate an untracked data transformation.

## Log
260727 · Connected the display-unit model to multi-format projection without giving Display ownership of every consumer.
