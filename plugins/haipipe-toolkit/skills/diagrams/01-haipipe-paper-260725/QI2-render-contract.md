# A source-agnostic render contract
state: 🟡 PARTIAL
owner: JL
method: pass a bounded render brief in and return an inspectable reproducible bundle

## Question
What is the smallest contract a generic Display renderer needs?

Current renderers discover a paper root, create `0-displays/` units, write `float.tex`, and sometimes call the paper stage. That makes them reusable in name but paper-coupled in execution.

## Boundary
- ✅ Covered here
  Generic renderer inputs, outputs, refusal behavior, and the boundary with paper adapters.
- ↪ Covered elsewhere
  Evidence computation belongs under `QD1`; paper queue handoff is `QG3`; format embedding is `QI4`.

## Content
### Input
```
kind
brief
data or source reference
style and accessibility constraints
output directory
required asset representations
```

### Output
```
winning asset
rebuild source or spec
preview
verification result
warnings or refusal
```

### Refusal
The renderer stops when the brief is incomplete, the named source is missing, or a requested numeric display has no verified aggregate.
It does not search a paper, invent data, create an S page, or guess manuscript placement.

### Paper adapter
The paper-side caller maps the generic bundle into `0-displays/displayNN-<slug>/`.
It owns the caption, label, placement, stable `display_id`, and the handoff on `S-Display-N`.

## Items to Finish
- [x] 📦 Separate render bundle from paper unit
      The generic result can be consumed by Paper, Application, slides, poster, or another caller.
- [ ] 📐 Write the request and result schema
      Keep it short enough for a queue task packet and complete enough for fresh-session recovery.
- [ ] 🔗 Repair shared contract ownership
      The four renderers currently point at a missing `../ref/display-unit-output-contract.md`.
- [ ] 🧪 Render one plot from a standalone brief
      No paper path, paper stage call, or manuscript file should be required.

## Where we are
Slides and poster already follow a source-agnostic content-plan contract.
The four unit renderers do not yet follow the same pattern.

## Files
- `display/ref/content-plan-spec.md`
  The existing source-agnostic handoff model.
- `paper/1-lifecycle/4-display/ref/display-unit-output-contract.md`
  The current paper-owned renderer contract.
- `display/skills/haipipe-display-*/SKILL.md`
  The renderers to decouple.
