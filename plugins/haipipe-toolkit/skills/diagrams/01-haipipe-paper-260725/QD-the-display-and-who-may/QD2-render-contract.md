# A source-agnostic render contract
state: ✅ SETTLED
owner: JL
method: pass a bounded render brief in and return an inspectable reproducible bundle

## Question
What is the smallest contract a generic Display renderer needs? One input shape, one output shape, and an explicit refusal, with every paper-specific assumption pushed out into an adapter so the renderer never has to know that papers exist.

Current renderers discover a paper root, create `displays/` units, write `float.tex`, and sometimes call the paper stage. That makes them reusable in name but paper-coupled in execution.


The approach is the smallest possible contract, one input shape, one output shape, and an explicit refusal, with everything paper-specific pushed into an adapter. What we want is a renderer that can be handed a spec by anything at all and does not need to know that papers exist.
## Boundary
- ✅ Covered here
  Generic renderer inputs, outputs, refusal behavior, and the boundary with paper adapters.
- ↪ Covered elsewhere
  Evidence computation belongs under `QB3b`; paper queue handoff is `QA9`; format embedding is `QD4`.

## Diagram
```
 THE SMALLEST CONTRACT THAT DOES NOT KNOW WHAT A PAPER IS

  IN                              OUT
  ┌──────────────────────────┐    ┌──────────────────────────┐
  │ kind                     │    │ winning asset            │
  │ brief                    │───►│ rebuild source or spec   │
  │ data or source reference │    │ preview                  │
  │ style + accessibility    │    │ verification result      │
  │ output directory         │    │ warnings or REFUSAL      │
  │ required representations │    │                          │
  └──────────────────────────┘    └──────────────────────────┘

 IT REFUSES, rather than guessing, when
   the brief is incomplete · the named source is missing ·
   a numeric display has no VERIFIED aggregate

 WHAT IT MUST NEVER DO             ⛔
   search a paper · invent data · create an S page ·
   guess manuscript placement

 THE PROBLEM THIS FIXES
   today's renderers discover a paper root, create displays/ units,
   write float.tex, and sometimes call the paper stage.
   That is "reusable" in NAME and paper-coupled in EXECUTION.

 WHERE THE PAPER KNOWLEDGE GOES INSTEAD
   ┌ paper-side adapter ─────────────────────────────────────┐
   │ maps the generic bundle into                            │
   │   displays/displayNN-<slug>/                          │
   │ owns caption · label · placement · stable display_id ·  │
   │      the handoff on S-Display-N                         │
   └─────────────────────────────────────────────────────────┘
   same shape as the dialect boundary in QA8: the generic thing
   stays ignorant, and the caller supplies the meaning.
```

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
The paper-side caller maps the generic bundle into `displays/displayNN-<slug>/`.
It owns the caption, label, placement, stable `display_id`, and the handoff on `S-Display-N`.

## Items to Finish
- [x] 📦 Separate render bundle from paper unit
      The generic result can be consumed by Paper, Application, slides, poster, or another caller.
- [ ] 📐 Write the request and result schema
      Keep it short enough for a queue task packet and complete enough for fresh-session recovery.
- [x] 🔗 Repair shared contract ownership
      Done 2026-07-26. The contract was SPLIT rather than moved, because its content was half generic and half paper-coupled, and relocating it whole would have moved Paper's coupling into Display.
      The generic half is now `display/ref/display-unit-output-contract.md` (unit layout, candidate mode, per-renderer mapping, the numbers-from-a-task and grayscale invariants, refusal). The paper half is `paper/1-lifecycle/4-display/ref/paper-adapter.md` (unit resolution, paper-root-relative paths, caption, label, placement, the generated gallery, the lifecycle handoff).
      All 12 renderer references were repointed from `../ref/` to `../../ref/` and verified to resolve. The original 2026-07-20 relocation had rewritten them at the wrong depth, which is why they had been dangling since.
- [ ] 🧪 Render one plot from a standalone brief
      No paper path, paper stage call, or manuscript file should be required.

## Where we are
Slides and poster already follow a source-agnostic content-plan contract.
The four unit renderers do not yet follow the same pattern.

## Files
- `display/ref/content-plan-spec.md`
  The existing source-agnostic handoff model.
- `display/ref/display-unit-output-contract.md`
  The generic half, owned by Display since the 2026-07-26 split.
- `paper/1-lifecycle/4-display/ref/paper-adapter.md`
  The paper half. Paper reaches into Display, never the reverse.
- `display/skills/haipipe-display-*/SKILL.md`
  The renderers to decouple. Their contract references now resolve; their execution is still paper-coupled.
