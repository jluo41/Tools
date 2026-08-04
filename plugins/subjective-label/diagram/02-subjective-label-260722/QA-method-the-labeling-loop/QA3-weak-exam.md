# The strong model supplies the answers, the weak model sits the exam
state: 🔴 OPEN
owner: RA
method: a weak model labels the 60 items from the guideline alone, then is scored against the gallery

## Question
Once a version of the guideline is written, how do we know it is written clearly enough?

Clarity cannot be read off the guideline by whoever wrote it, and the strong model that produced the gallery cannot grade its own answers either.
The test JL set is to hand the guideline to a cheap weak model that had no part in writing it, let it label the same 60 items with nothing else to go on, and see whether it lands on the gallery's answers.
What this exam measures is whether the guideline is clear enough that a different, cheaper model can read it too.
It does not measure whether two models happen to think alike, which is all that agreement between two peers can show.
While this stays open the project has no clarity number at all, so a guideline that only reads clearly to whoever wrote it can pass unnoticed, and every later comparison of versions carries that ambiguity forward.

## Boundary
- ✅ Covered here
  Weak models label the same 60 items with the guideline as their only instruction, and each one reports a single agreement score against the gallery.
- ↪ Covered elsewhere
  Producing those 60 gallery answers in the first place is QA1, the panel labeling independently and reporting only its disagreements is QA2, and whether the labels are correct rather than merely reproducible from the guideline is measured on outside data in QB3.

## Diagram
```
  strong model (expensive) ──► produces the 60 gallery answers
  guideline
        │
        ▼  label those 60 items by following the guideline
  weak model A ─┐
  weak model B ─┼─► each scored against the [gallery] ──► each reports one number
  weak model C ─┘        (models are never scored against each other)

  even a cheap model labels them right = the guideline really is written clearly
```

## Items to Finish
- [ ] 🧪 Several cheap weak models label the 60 items from the guideline
      A handful of cheap weak models sit the exam, labeling the same 60 items with the guideline as their only instruction.
      Cheap is the point here: the expensive strong model is already spent on producing the gallery answers, and what the run has to find out is how much the guideline carries on its own, without the reader supplying the missing judgment.
      A weak model reading the guideline cold is the closest thing available to a stranger picking the document up.
- [ ] 📊 Each weak model reports one agreement score against the gallery
      Every weak model's labels are compared with the gallery and reduced to one number per model.
      One number per model keeps the result readable: you can see at a glance whether the guideline travels to a labeler that had nothing to do with writing it.
      This number is the clarity metric, which ZD's note asks to be reported separately from the panel's internal agreement and from correctness.
- [ ] 🚫 No model is compared with another model
      Every comparison runs against the gallery; the weak models are never scored against each other.
      The gallery is the only ruler here because it holds the answers JL confirmed personally, so a score against it means something outside the models.
      A score of one model against another only measures how similar two labelers are, and it can stay high for reasons that have nothing to do with the guideline.

## Where we are
Nothing of this exam has been run yet: no weak model has labeled the 60 items from the guideline alone.
What runs today is two peer models cross-checking each other.
When those two agree it tells us the two of them reason alike, which is not evidence that the guideline is written clearly.

## Files
- `_source/note-update-v3-260721.md`
  ZD's note of 2026-07-21, whose F4 row is why this face's number is reported as clarity, separately from reliability and correctness.

## Glossary
guideline: the document stating what counts as HIGH, LOW, or NONE, which a model follows when it labels.
gallery: the set of answers JL personally confirmed, used as the ruler for measuring whether a model labels correctly.
weak model / strong model: the expensive strong model produces the gallery answers and the cheap weak model sits the exam, so a cheap model labeling correctly from the guideline alone is what shows the guideline is genuinely clear.

## Comments
- [ ] ZD 「What this exam measures is whether the guideline is clear enough that a different, cheaper model can read it too.」 · 260721 1400
      From ZD's note-update-v3, row F4: clarity is not correctness.
      The three numbers have to be reported separately: reliability (the panel's internal kappa), clarity (executor-independence, which is exactly this face's weak-model exam), and correctness (measured only on public data, see QB3).
      Do not read "the weak models agree too" as "the labels are right".

## Log
260725 · rewritten to the current face format in English
260723 1600 · migrated from the old `[Q3]`; the finish line was split into a checklist and a Diagram was added
