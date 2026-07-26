# Is the unit of work the stage, or the checkable page?
state: ✅ SETTLED
owner: JL
method: rule the grain once; the artifact and the naming questions both follow it

## Question
Does one stage produce one artifact, or one artifact per thing a human can gate? Seven of the eight stages assume one per stage and one does not. The answer decides how many pages a paper's board has, and whether that number is a design consequence or a matter of taste.

Seven of the eight stages assume one artifact per stage. One, section-edit, declares `runs: per-unit` and produces one artifact per manuscript section. That exception was not a compromise; it is the shape the work actually has, and the question is whether the other stages should follow it.


The way through is to let the grain follow the gate: a thing that a human accepts separately gets a page of its own, and a thing accepted as a whole gets one. What we want is for the number of pages to stop being a matter of taste and become a consequence of how the work is actually approved.
## Boundary
- ✅ Covered here
  What one run of a stage produces, and therefore how many gates it has.
- ↪ Covered elsewhere
  What that artifact IS is `QBa1`; what it is called is `QBa2`.

## Diagram
```
 THE TEST: COULD A HUMAN APPROVE ONE UNIT AND REJECT ANOTHER?

   yes ──► per-unit          no ──► one artifact for the stage

 THE WORKED EXAMPLE, BOTH WAYS

  BEFORE  one artifact for 4-display
  ┌────────────────────────────────────────────────────┐
  │ gate: "is the display stage done?"                 │
  │   display01 …  display02 …  display03 …  ×11       │
  │   different statuses · different source data ·     │
  │   different blockers                               │
  │   13-record checklist   ──►   NEVER CLOSED  ⚠️      │
  └────────────────────────────────────────────────────┘

  AFTER  one page per asset
  ┌──────────────┐┌──────────────┐┌──────────────┐
  │ display01    ││ display02    ││ display04    │  …
  │ gate: ✅      ││ gate: ⏳      ││ gate: ✅      │
  └──────────────┘└──────────────┘└──────────────┘
   each question answerable in a sentence

 HOW THE EIGHT FALL OUT
   per-unit        4-display          11 assets, independent gates
                   5-section-edit     runs: per-unit, already true
   single-output   0-seed · 1a-resource · 1b-claims ·
                   2a-venue · 2b-pitch · 3-narrative
                   one thing each; per-unit machinery buys nothing

 THE RULE IS NOT "EVERYTHING IS PER-UNIT"
   it is "per-unit where the WORK is per-unit", and the gate is the test.
```

## Content
### The argument from the gate
A gate is one human saying yes to one specific thing (`QB3`). So the grain of the artifact and the grain of the gate have to match, or the gate becomes unanswerable.

The display stage is the worked example. It had one artifact for the whole stage, and its gate asked "is the display stage done" across eleven separate figures and tables with different statuses, different source data and different blockers. It accumulated a thirteen-record checklist and never closed. Split into one page per asset, each question became answerable in a sentence.

### What speaks for the stage grain
Fewer contracts, and a stage that genuinely produces one thing (seed, venue, pitch) gains nothing from per-unit machinery. The rule cannot be "everything is per-unit"; it has to be "per-unit where the work is per-unit", which needs a test rather than a preference.

### The test worth ruling on
A stage is per-unit when its units have INDEPENDENT gates: when a human could reasonably approve one and reject another. Seed cannot; display obviously can; section-edit already does.

## Law
The unit follows the human gate, not the folder called a stage. A stage is `per-unit` exactly when one unit can be approved while another is rejected.

By this rule, Display and Section Edit are per-unit. Seed, Resource, Claims, Venue, Pitch, and Narrative remain single-output stages.

## Items to Finish
- [x] 🧠 Rule the grain, with the test
      Per-unit where units gate independently; one artifact otherwise. Or a different test, stated.
- [ ] 📐 Apply it to display
      If per-unit: `unit:`, `units_from:`, and an artifact pattern rather than a path.
- [x] 📐 Confirm which stages stay single
      Seed, resource, claims, venue, pitch, narrative: state that they are single-artifact by the same test, so it reads as a decision.

## Where we are
The grain is ruled. Section Edit already implements it; Display qualifies but still has a central `runs: once` contract, so that migration remains open and is intentionally not hidden inside this first creator test.

## Files
- `stages/5-section-edit/stage.md`
  The only stage that already answers per-unit.
- `stages/4-display/stage.md`
  The stage the argument is really about.
