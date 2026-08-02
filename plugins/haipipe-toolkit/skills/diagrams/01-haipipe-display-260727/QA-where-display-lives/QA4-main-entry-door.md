# The main Display entry door
state: 🟡 PARTIAL
owner: JL
method: retain the proven Paper entry path while deciding whether non-paper consumers justify a shared Display router

## Opening
Does the Display family need one public `haipipe-display` entry skill?

Today a paper starts through `haipipe-paper display`, which creates or resolves the unit and then commissions a named renderer.
The four renderers are independently callable when a caller already has a valid unit.

## Content
### Current route
`haipipe-paper display` is the safe public door for paper visuals.
It can decide whether a task aggregate is missing, allocate the S page, materialize Intake, and select a renderer.

### Open decision
A generic entry skill should exist only if it can resolve a non-paper consumer without stealing Paper's semantic role.
The Board keeps this visible rather than adding a superficial router now.

## Aims
- [x] 🚪 State the Paper-facing entry route
      Existing aggregate → Paper Display → Intake → renderer.
- [ ] 🧭 Test a real slide, poster, or HTML consumer that needs generic unit allocation
      Decide whether one shared Display front door reduces ambiguity without duplicating adapters.

## States
The current contracts work for paper consumers.
The generic entry-door decision is intentionally open.

## Files
- `paper/haipipe-paper/SKILL.md`
  Routes a paper-facing visual to the Display stage first.
- `display/ref/content-plan-spec.md`
  The existing non-paper consumer contract to evaluate.

## Log
260727 · Kept a generic entry skill as an open design question rather than creating a placeholder.
