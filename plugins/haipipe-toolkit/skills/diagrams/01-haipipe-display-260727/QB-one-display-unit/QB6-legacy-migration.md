# Legacy units and migration
state: ✅ SETTLED
owner: JL
method: preserve working legacy units while requiring an explicit migration decision before adopting the new shape

## Opening
What happens to units that already use `source/` or independently authored wrappers?

They remain valid legacy units.
They are not automatically renamed or mixed with the new layout.

## Content
### Why migration is deliberate
An old folder may have a working compile path, embedded assumptions, or a hand-edited wrapper.
Renaming it just to make the tree look modern can break a manuscript without improving provenance.

### What a migration means
A deliberate migration verifies sources, materializes Intake, moves rebuild material to recipe, and reconciles the wrapper against the Paper page.
It is a unit-level review task, not a global search-and-replace.

## Aims
- [x] 🕰️ Declare compatibility rules
      Existing units remain readable through a legacy path.
- [x] 🚧 Reject accidental hybrid layouts
      New renderers choose either the legacy compatibility path or the new contract.

## States
The active MISQ paper retains legacy units and is not changed by the new Intake contract.

## Files
- `display/ref/display-unit-output-contract.md`
  Legacy-unit compatibility rules.
- `paper/1-lifecycle/4-display/ref/paper-adapter.md`
  Paper-side migration note.

## Law
Law: A migration is a reviewed conversion of one unit, never housekeeping.

## Log
260727 · Kept legacy paths intact while establishing the new-unit contract.
