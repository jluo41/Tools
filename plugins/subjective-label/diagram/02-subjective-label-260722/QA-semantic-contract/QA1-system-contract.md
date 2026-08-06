# Cold start: talk first, do not force-label
state: 🔴 OPEN
owner: RA
method: 60 items plus dialogue with a strong model (raised in the meeting)

## Question
When a new construct is just starting and nothing exists yet, where does the very first batch of labels come from?

This is the step JL rejected in his first sentence in the meeting: draw a random batch, put it in front of a person, and make them label it cold, because the person's judgment gets dragged along by whatever those items happen to be, and the guideline then gets patched together out of off-the-cuff reactions.
Nothing else in the method survives that: the gallery is the ruler every later exam is measured against, so if the first answers were produced by reacting to an arbitrary draw, every kappa reported downstream is measuring against a ruler that was bent at the start.
The replacement is to let a strong model go into the corpus and find relevant items first, then settle them in dialogue with JL, which grows a first guideline and 60 confirmed answers in the same pass instead of demanding one before the other exists.
Until this is settled there is no guideline for a model to follow and no gallery to grade it with, so QA2, QA3, and everything in QB is waiting on it.

## Boundary
- ✅ Covered here
  How the first labels come into existence when there is no guideline and no gallery yet: the strong model finds relevant items in the corpus, and the dialogue with JL produces a first guideline plus 60 confirmed answers at once.
- ↪ Covered elsewhere
  Who labels those 60 items and how only the disagreements are reported is QA2; putting a weak model through the exam on the resulting answers is QA3; growing the 60 up to 140 by hunting hard cases is QB1.

## Diagram
```
  ✗ old way:  draw a random batch  →  make a person label it cold
                                      the person's judgment gets dragged along by the items
                                      the guideline is patched together from off-the-cuff reactions

  ✓ settled in the meeting:  a strong model finds relevant items in the corpus  →  dialogue with JL
       └─► two things grow at the same time:
             ① a first-version guideline
             ② 60 answers JL confirmed himself  ← the standard answers for every later exam
```

## Items to Finish
- [ ] 📜 One run produces a first-version guideline
      A single cold-start run ends with a written guideline stating what counts as HIGH, LOW, or NONE, not with notes in somebody's head.
      Today the guideline is assembled after the fact out of JL's reactions to a dozen or so items, so it records whatever he happened to say rather than the rule he was applying, and no second person can check a label against it.
      Making the guideline an output of the same run that produces the first labels is what turns those labels into something another reader can reproduce.
      Until the document exists there is nothing for a model to follow and nothing for the later exams to grade against.
- [ ] 🎯 The same run produces 60 answers JL confirmed himself
      The run hands back 60 items whose labels JL personally signed off, and that set becomes the gallery every later exam is graded against.
      The two outputs have to come from one pass because they only make sense together: a guideline with no confirmed examples has no worked cases attached to it, and confirmed examples with no guideline give nothing to generalize from.
      60 is the starting size set in the meeting, and it is the number QB1 later grows to 140 by hunting hard cases.
      Nothing downstream can say whether a model labels correctly before this set exists, because the gallery is the ruler.
- [ ] 🚫 The 60 are not a random draw
      They come from a strong model going into the corpus to find relevant items first, and then get settled in dialogue with JL.
      The objection is not to randomness as such but to what a random batch does to the person: they end up reacting to whatever the draw contained, and the guideline that comes out of it is shaped by the sample rather than by the construct.
      Letting the model retrieve relevant items first puts arguable cases in front of JL, and the dialogue is where each call acquires a reason.
      Those reasons are what the guideline is made of, which is why this condition and the two above are one run and not three.

## Where we are
Nothing here has been built yet.
The present approach is to show JL a dozen or so items, take his off-the-cuff reactions, and patch a guideline together out of those reactions.
There is no step that produces 60 confirmed answers first, so nothing downstream has a ruler to be measured against.

## Files
- `lib/sample.py`
  The code that draws a batch out of the corpus, so this is where a decision about how the first items are chosen has to land.
- `lib/embed.py`
  Its `nearest` and `stratify` subcommands are the existing way to pull related items out of the corpus; how a sentence becomes a vector at all is QD1's ruling, not this one.

## Glossary
guideline: the document stating what counts as HIGH, LOW, or NONE, which a model follows when it labels.
gallery: the set of answers JL personally confirmed, used as the ruler for measuring whether a model labels correctly.
construct: the trait being labeled.

## Log
260725 · rewritten to the current face format in English
260723 1600 · migrated from the old `[Q1]` single-file format to the new format; the finish line was split into a checklist and a Diagram was added
