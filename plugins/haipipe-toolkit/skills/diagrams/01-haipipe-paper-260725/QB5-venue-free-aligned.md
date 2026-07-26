# Venue-free and venue-aligned
state: 🟡 PARTIAL
owner: JL
method: keep the split; state exactly what retargeting rewrites

## Question
Which stages survive a change of target journal, and which must be rewritten?

The lifecycle splits at venue: seed, resource and claims are venue-FREE, and pitch through section-edit are venue-ALIGNED. The split is what lets a rejected paper be retargeted without redoing its evidence, which is a real and frequent event, so the boundary has to be exact rather than approximately right.

## Boundary
- ✅ Covered here
  Which stages are rewritten on retarget, and what "rewritten" means for each.
- ↪ Covered elsewhere
  How a venue pack binds a section is `QE1`'s contract form question; the claims themselves belong to the claims stage.

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
