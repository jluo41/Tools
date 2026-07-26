# Display meaning and rendering
state: 🟡 PARTIAL
owner: JL
method: keep meaning with the consumer, rendering in a reusable Display family, and primitives in Utils

## Question
Which parts of a Display belong to Paper, Display, Task, Deliver, and Utils?

Drawing and visualization should be reusable outside papers, but a publication Display carries a claim, takeaway, caption job, placement, and human gate that a generic drawing utility cannot own. The architecture needs a shared Display layer without stripping meaning from the consuming lifecycle.

## Boundary
- ✅ Covered here
  Ownership across Paper, Display, Task, Deliver, and low-level drawing utilities.
- ↪ Covered elsewhere
  The generic renderer contract is `QI2`; renderer kinds are `QI3`; output embedding is `QI4`.

## Content
### Ownership map
```
Paper or Application   why this Display exists, what it means, where it belongs
Task or Discovery      computed evidence and provenance
Display family         render a supplied brief into reproducible visual assets
Deliver adapters       embed the result into LaTeX, Word, HTML, slides, or poster
Utils                  ASCII, Draw.io, Excalidraw, SVG, image generation primitives
```

### The key distinction
Display is reusable, but it is not a small stateless utility.
It owns a render contract, renderer selection, reproducibility, preview, and visual quality checks.
Low-level drawing engines remain utilities that Display may call.

## Items to Finish
- [x] 🧭 Move rendering out of Paper ownership
      Paper commissions a renderer and keeps the semantic Display contract.
- [x] 🧰 Keep low-level drawing tools in Utils
      Utility tools do not decide claim, caption, placement, or gate.
- [ ] 📐 Graduate the ownership map
      Paper and Display skills must state the same boundary without copying full procedures.
- [ ] 🧪 Reuse one renderer outside a paper
      The renderer should succeed from a bounded brief without opening a paper folder.

## Where we are
The standalone `display/` family already exists and proves the intended direction.
Its table, plot, diagram, and illustration skills still contain paper-specific paths and responsibilities.

## Files
- `skills/display/`
  The reusable Display family.
- `paper/1-lifecycle/4-display/`
  The paper-specific meaning and commissioning layer.
- `0_utils/diagram-*`
  Low-level drawing primitives.
