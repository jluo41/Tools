# Label independently, report only the disagreements
state: 🟡 PARTIAL
owner: RA
method: several models label independently, one item at a time

## Question
Who labels these 60 items, and how should the labeling run so that it does not waste JL's time?

JL settled this step in two sentences at the meeting: have several models label independently so that the disagreements are surfaced, skipping whatever they all agree on, and go one item at a time rather than labeling a whole batch at once.
The scarce resource is JL's attention, so the labeling has to arrive already filtered: what everyone agrees on passes on its own, and only a disagreement is worth putting in front of a person.
What actually runs today is neither of those things: two models are compared head to head instead of several models labeling independently, and a whole batch is labeled in one pass, so the judgments made on the earlier items drag the later ones.
While that stands, a disagreement cannot be read cleanly, because the batch order is one possible reason for it, and every step downstream inherits labels produced under that drag.

## Boundary
- ✅ Covered here
  How the 60 items are labeled once they exist: how many labelers, whether they label independently of each other, and which disagreements reach JL.
- ↪ Covered elsewhere
  Where the first 60 items and the first guideline come from at all is QA1; having a strong model produce the answers while a weak model sits the exam is QA3; growing the 60 up to 140 by hunting hard cases is QB1.

## Diagram
```
  several models each label the same item independently
        │
        ├─ all agree ──► passes automatically, recorded (JL is not disturbed)
        └─ they differ ──► sorted into four kinds:
                             true boundary / guideline unclear / new situation ──► put in front of JL
                             the fourth kind (one model slipped) = noise       ──► handled automatically
```

## Items to Finish
- [x] 🔍 Disagreements are sorted before anyone is disturbed
      Every disagreement is sorted into four kinds, and only the first three are put in front of JL.
      The three that reach JL are a true boundary case, a guideline that does not say clearly enough what counts, and a situation that had not come up before.
      The fourth kind is one model slipping on an item it would normally get right, which says nothing about the guideline, so it is treated as noise and handled automatically.
      This is the part of the step that exists today, and it is the only ticked line on this face.
- [ ] 📄 One item at a time
      Labeling runs item by item instead of labeling a whole batch in one pass.
      Today a whole batch goes through at once, and the trouble with that is that the judgments made on the earlier items drag the later ones.
      JL said explicitly that this has to change.
- [ ] 🧑‍🤝‍🧑 Several models label independently
      Several models each label the same item on their own, rather than two models being compared head to head at the same level.
      Head to head comparison is not the same thing as independent labeling: independence is what makes a disagreement mean something, since it is then two judgments formed separately rather than one judgment weighed against another.
      JL said explicitly that this has to change too.
- [ ] ✅ Agreement passes automatically and is recorded
      When the labelers all agree, the item passes without JL seeing it, and the agreement is written down.
      This is the other half of the filter: JL's time goes to disagreements only, so an item that passes on its own still has to leave a trace of what it was labeled and that the labelers agreed.
      How that record is kept has not been pinned down on this face.

## Where we are
The mechanism for surfacing disagreements is in place: disagreements are sorted into four kinds, only the first three are put in front of JL, and the fourth is treated as noise and handled automatically.
What runs underneath it is not yet the labeling JL described: two models are compared head to head instead of several models labeling independently, and the labeling is done a batch at a time, whose fault is that the judgments on the earlier items drag the later ones.
JL said explicitly that this has to change.

- 260723 CC · 🔀 Migrated out of the old `[Q2]` single file
      The face was moved into the current format and its single finish line was split into a checklist.
      The one part already built, the sorting of disagreements, was ticked; the two parts JL asked to change were left open.

## Files
- `ref/ref-config.md`
  The `labeler:` block is where the panel is declared, so changing what labels these items and how many labelers there are starts in this config.

## Glossary
noise: one model slipping on an item now and then, which does not mean the guideline is wrong, so this kind of disagreement does not need to reach JL.
guideline: the document stating what counts as HIGH, LOW, or NONE, which a model follows when it labels.
panel: the set of model labelers.

## Log
260725 · rewritten to the current face format in English
260723 1600 · migrated out of the old `[Q2]`; the finish line was split into a checklist, the disagreement sorting already built was ticked, and the two parts still to change were left open
