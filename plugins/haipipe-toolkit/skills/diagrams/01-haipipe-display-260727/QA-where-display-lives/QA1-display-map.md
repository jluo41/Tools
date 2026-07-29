# The Display map
state: ✅ SETTLED
owner: JL
method: separate evidence production, visual rendering, and reader-facing meaning before a renderer runs

## Question
Where does Display sit, and what does it own?

Display is the reusable visual-production layer.
It receives an approved input package and produces a reproducible visual bundle.
It is not a task executor and not a paper author.

## Boundary
- ✅ Display owns the transform from approved Intake to recipe, candidate, selected asset, preview, and renderer receipt.
- ↪ Task owns the canonical aggregate and its provenance.
- ↪ Paper owns the claim, visual argument, wrapper semantics, placement, and human approval.
- ↪ Section Edit owns the sentence that cites the selected display.

## Diagram
```text
TASK                              DISPLAY UNIT                         PAPER
canonical evidence                bounded visual production            reader-facing meaning

source_data.csv ──► intake/ ──► recipe/ ──► candidates/ ──► assets/ ──► float.tex ──► sentence
provenance.json       allowed       rebuild      reversible      selected       wrapper
                       inputs        path         alternatives    visual         + placement
```

## Content
### The Display boundary
Display never recomputes an estimate or searches an upstream task folder.
Display never decides whether an estimate supports a claim.
Display turns one already-approved input package into a visual that can be inspected and rebuilt.

### The atomic object
The unit is `displays/displayNN-<slug>/` for a paper consumer.
The same unit contract can serve another consumer through an adapter without moving the evidence into that consumer.

## Items to Finish
- [x] 🧭 Define Display as a reusable rendering layer
      The generic output contract describes its folder and renderer boundary.
- [x] 🔒 Keep evidence and argument ownership outside Display
      Task and Paper responsibilities are explicit in the Intake contract and Paper adapter.

## Where we are
The ownership split is implemented and used by all four paper renderers.

## Files
- `display/ref/display-unit-output-contract.md`
  The generic unit boundary.
- `paper/1-lifecycle/4-display/ref/paper-adapter.md`
  The Paper-specific ownership split.

## Law
Law: Display transforms approved inputs; it does not create evidence or meaning.

## Log
260727 · The Board was opened after Intake separated canonical task evidence from visual rendering.
