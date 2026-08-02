# Paper Display bridge
state: ✅ SETTLED
owner: JL
method: let Paper accept a display request, allocate a unit, bind its Intake, and gate the selected visual

## Opening
What does Paper Display do before it commissions a renderer?

It decides why the reader needs the display and whether a suitable approved input exists.
It allocates the S page and unit before renderer work begins.

## Content
### The request path
A Display Request names the claim, form, bank deliverable, Intake source, and consumer deliverable.
Paper Display advances it through `requested → accepted → intake-ready → done`.

### The existing-aggregate rule
When a verified aggregate already exists, start with Paper Display.
Call the display-input task only when the aggregate is missing or must change.

## Aims
- [x] 📝 Extend Display Requests with Intake source and consumer deliverable
      A request now names both sides of the handoff.
- [x] 🧭 Publish the explicit per-unit S-page creation route
      The Paper adapter uses `create-page.py display ... --family Display --unit <N>` while `QB2b@paper` remains open.

## States
The Paper adapter gives a fresh agent an executable route from a verified aggregate to an independently gated unit.

## Files
- `paper/1-lifecycle/4-display/ref/paper-adapter.md`
  Paper-to-Display bridge.
- `paper/2-phase/0-draft/haipipe-paper-draft-display/SKILL.md`
  Display Request lifecycle.

## Law
Law: Paper decides whether and why a visual exists before Display decides how to render it.

## Log
260727 · Fresh-context validation confirmed the existing-aggregate route starts at Paper Display.
