# Renderer taxonomy
state: ✅ SETTLED
owner: JL
method: route by visual form and editability rather than by a generic request to make a figure

## Question
Which renderer should make a requested display?

The form of the intended visual determines the renderer.
The same Intake contract applies before that choice.

## Diagram
```text
approved Intake + brief
        │
        ├── typeset rows and columns ─────► table
        ├── numeric marks and axes ───────► figure
        ├── deterministic topology ───────► diagram
        └── qualitative concept or hero ──► illustration
```

## Content
### Four current forms
`haipipe-display-table` renders booktabs table bodies.
`haipipe-display-figure` renders data plots.
`haipipe-display-diagram` renders editable deterministic vector diagrams.
`haipipe-display-illustration` renders AI concept illustrations with a review record.

### Form is not evidence strength
Choosing a diagram does not license unsupported numeric facts.
Choosing a figure does not permit recomputing a result.
The Intake and Paper brief remain the governing boundary.

## Items to Finish
- [x] 🧭 Publish a four-way routing table
      The generic output contract names the appropriate renderer for each visual form.
- [x] ✏️ Preserve editable form where it matters
      Architecture and workflow visuals route to FigureSpec rather than an opaque image by default.

## Where we are
All four paper-facing renderer skills use the same display-unit contract.

## Files
- `display/ref/display-unit-output-contract.md`
  Renderer routing and asset mapping.
- `display/skills/haipipe-display-table/SKILL.md`
  The table renderer.
- `display/skills/haipipe-display-figure/SKILL.md`
  The plot renderer.
- `display/skills/haipipe-display-diagram/SKILL.md`
  The vector-diagram renderer.
- `display/skills/haipipe-display-illustration/SKILL.md`
  The illustration renderer.

## Law
Law: Choose the renderer by visual form; use Intake to keep every form honest.

## Log
260727 · Consolidated the four renderers under one unit and Intake contract.
