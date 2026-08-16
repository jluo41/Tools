# Venue-free and venue-aligned
state: 🟡 PARTIAL
owner: JL
method: keep the split; state exactly what retargeting rewrites

## Question
Which stages survive a change of target journal, and which must be rewritten? The lifecycle splits at venue, and exactly where that line falls decides whether retargeting a paper is a bounded operation or an open-ended rewrite.

The lifecycle splits at venue: seed, resource and claims are venue-FREE, and pitch through section-edit are venue-ALIGNED. The split is what lets a rejected paper be retargeted without redoing its evidence, which is a real and frequent event, so the boundary has to be exact rather than approximately right.


The approach is a per-stage flag decided by one question: could a different journal change this stage's answer? What we want is a retarget that touches only what it must, so moving a paper to another outlet is a bounded operation rather than a rewrite with unclear edges.
## Boundary
- ✅ Covered here
  Which stages are rewritten on retarget, and what "rewritten" means for each.
- ↪ Covered elsewhere
  How a venue pack binds a section is `QE1`'s contract form question; the claims themselves belong to the claims stage.

## Diagram
```
 THE LINE FALLS BETWEEN WHAT IS TRUE AND HOW IT IS TOLD

   venue-FREE                    survives retargeting untouched
   ┌─────────────────────────────────────────────────┐
   │ 0-seed        why might this exist               │
   │ 1a-resource   does the evidence exist and carry  │  THE SCIENCE
   │ 1b-claims     supported / weak / GAP             │
   └─────────────────────────────────────────────────┘
                        │
                   2a-venue   ◄── THE PIN
                        │
   ┌─────────────────────────────────────────────────┐
   │ 2b-pitch      what is it selling, to whom        │
   │ 3-narrative   reveal order, section list         │  THE TELLING
   │ 4-display     display budget, conventions        │
   │ 5-section-edit house style, citation density     │
   └─────────────────────────────────────────────────┘
   venue-ALIGNED                 rewritten on retarget

 WHY EXACTLY THERE
   a claim's status does not change because a different editor reads it.
   a narrative's ORDER does. So does the display budget, and the house
   style. Everything downstream of the pin is an outlet property.

 THE CASE THAT TESTS IT, AND STILL LANDS ALIGNED
   MISQ ──rejected──► another outlet
     evidence   KEPT       every claim, every number, every probe entry
     figures    MOSTLY LOST  display limits and conventions differ
   That is expensive. It is still the right side of the line: a figure
   is an argument made FOR a venue, not a fact about the world.
```

## Content
### The split as it stands
```
 venue-FREE     0-seed · 1a-resource · 1b-claims
                the science: what is true and what can be defended
 the pin        2a-venue
 venue-ALIGNED  2b-pitch · 3-narrative · 4-display · 5-section-edit
                the telling: what is sold, in what order, with what displays,
                in whose house style
```

### Why the boundary sits exactly there
A claim's status does not change because a different editor will read it. A narrative's order does: the reveal order, the section list, the display budget and the citation density are all outlet properties. So the line falls between what is true and how it is told.

### The case that tests it
Display sits on the aligned side, and it is the one that hurts: a rejected paper retargeted to another outlet keeps its evidence but may keep almost none of its figures, because display limits and conventions differ. That is expensive, and it is the right answer anyway.

## Items to Finish
- [x] ✂️ The split is stated
      `PHILOSOPHY.md` and the per-stage `venue_aligned:` field.
- [ ] 📐 State what retargeting actually does to each aligned stage
      Rewrite from scratch, or re-derive against the new blueprint while keeping the argument? These are different operations and the contracts do not distinguish them.
- [ ] 🧠 Rule whether a retarget reopens the claims stage
      It should not, by this design. Say so explicitly, because the temptation at a new venue is to re-cut the claims to fit.

## Where we are
The split is implemented as a per-stage flag and honoured. What a retarget concretely does has never been run end to end, so it is design rather than practice.

## Files
- `PHILOSOPHY.md`
- `stages/*/stage.md`
  The `venue_aligned:` field.
