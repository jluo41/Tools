# Display meaning and rendering
state: ✅ SETTLED
owner: JL
method: keep meaning with the consumer, rendering in a reusable Display family, and primitives in Utils

## Question
Which parts of a Display belong to Paper, Display, Task, Deliver, and Utils? Drawing and visualization should be reusable outside papers, and that is only true if no public renderer quietly assumes a manuscript is there.

Drawing and visualization should be reusable outside papers, but a publication Display carries a claim, takeaway, caption job, placement, and human gate that a generic drawing utility cannot own. The architecture needs a shared Display layer without stripping meaning from the consuming lifecycle.


The approach is to split by what each layer owns rather than by what it produces: Paper keeps the visual argument, Display keeps reusable rendering, Task keeps the computed evidence. What we want is a rendering family that is genuinely usable outside a paper, without a public skill quietly assuming a manuscript is there.
## Boundary
- ✅ Covered here
  Ownership across Paper, Display, Task, Deliver, and low-level drawing utilities.
- ↪ Covered elsewhere
  The generic renderer contract is `QD2`; renderer kinds are `QD3`; output embedding is `QD4`.

## Diagram
```
 A DISPLAY IS REUSABLE. ITS MEANING IS NOT.

 ┌ PAPER / APPLICATION ────────────────────────────────────────┐
 │ WHY this display exists · what it MEANS · where it BELONGS  │
 │ the claim it carries · the caption job · the human gate     │
 └───────────────┬─────────────────────────────────────────────┘
                 │ hands down a brief
 ┌ TASK / DISCOVERY ──────────┐   ┌ DISPLAY family ────────────┐
 │ computed evidence          │──►│ render a brief into        │
 │ + provenance               │   │ reproducible visual assets │
 │ the numbers                │   │ owns: render contract ·    │
 └────────────────────────────┘   │ renderer selection ·       │
                                  │ reproducibility · preview ·│
                                  │ visual quality checks      │
                                  └───────────┬────────────────┘
                                              │ calls
 ┌ DELIVER adapters ──────────┐   ┌ UTILS ─────▼────────────────┐
 │ embed into LaTeX · Word ·  │◄──│ ASCII · Draw.io · Excalidraw│
 │ HTML · slides · poster     │   │ SVG · image generation      │
 └────────────────────────────┘   └─────────────────────────────┘

 THE DISTINCTION THAT DOES THE WORK
   Display is REUSABLE but it is NOT a small stateless utility.
   A drawing engine converts. Display decides which renderer, checks
   the result, and can refuse. Those are not the same job, and putting
   them in one box is what lets a low-level converter start owning
   high-level content decisions.
```

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

### The reader-facing review surface
Paper owns the `S-Display` page, so the page, not a renderer, tells a reader what the unit currently is.
Every allocated unit is reviewed in the same order: the compiled Current Float, the artifact the wrapper actually references, Display Versions, the real folder tree, and the authored display explanation.
The renderer never turns a legacy folder into a target-layout folder by presentation alone; the folder view must report the files that are actually on disk.

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
