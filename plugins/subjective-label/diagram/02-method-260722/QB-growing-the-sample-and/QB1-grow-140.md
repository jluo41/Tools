# Grow to 140 items by hunting hard cases
state: 🔴 OPEN
owner: RA
method: pick by geometric position, going after the hard cases on the border

## Question
The 60 seed items are already confirmed, so how do we choose the next batch of 80 to send for labeling, reaching 140?

JL's position is that picking at random is a waste.
In the meeting he drew a figure: think of each review as a point in space, with the three labels as three regions.
Most points sit near the middle of a region and can be told apart at a glance (about eight in ten), while a few sit on the border between regions and are ambiguous (about two in ten).
The labeling effort should go into that two in ten, not be spent on items whose answer is obvious.
The rule is therefore to pick by geometric position rather than draw at random from the pool.
What makes this hard is that the position only exists once every review has been turned into a point in space, so this face stands on QD1 (how a sentence becomes a vector); if that does not land, picking by position is empty talk.
While the question stays open the sample stays at 60, so QB2 (the three-layer examination) has no grown sample to examine and the labeling budget keeps going to items whose answer was never in doubt.

## Boundary
- ✅ Covered here
  Which items go into the next batch: growing the confirmed 60 to 140 by deliberately selecting hard or informative cases instead of random ones.
- ↪ Covered elsewhere
  How a sentence becomes a point in space at all is QD1, and training the label-trained classifier that ZD wants the hard cases mined from is QD3.
  Examining the grown sample in three layers is QB2, and finishing the remaining thousands after that is QC2.

## Diagram
```
  Each review becomes one point in space through its embedding (see QD1)
  Three labels = three regions:

        HIGH  ●●●●●              ●  near the center: typical, told apart at a glance (about 80%)
             ●●●● ◇◆ ●●●●        ◇◆ stuck on the border: ambiguous, the hard cases (about 20%)
        LOW ●●● ◆◇   ◇◆ ●●● NONE
                  ↑
      Spend the labeling effort on that 20%, not on items whose answer is obvious
```

## Items to Finish
- [ ] 🎯 One run picks the next 80 from the 60 seeds
      A single run takes the 60 confirmed seed items and returns the next batch of 80, reaching 140.
      Nothing has been run yet, so this is the plain existence check: there is a command that goes from the confirmed seeds to a concrete batch of 80 items ready to be sent for labeling.
      Until it runs once from end to end, the growth from 60 to 140 exists only as a plan written on this page.
- [ ] 📐 The batch is picked by position, not drawn at random
      Selection goes by geometric position in the space, not by a random draw from the pool.
      A random draw mostly returns points near the middle of a region, which is exactly where the answer was never in doubt, so the labeling effort buys almost nothing.
      Picking by geometric position aims the batch at the border between regions, where the answer is genuinely unclear and where a human label is worth paying for.
      ZD's 2026-07-21 note pushes the mining one step further: take the hard cases from a label-trained classifier (`classify.py`, which is QD3) rather than from raw embedding distance.
- [ ] 🔍 Easy and hard cases are told apart in the result
      The output shows which items are the typical cases you can tell apart at a glance and which are the hard cases stuck on the border.
      Without that split the batch is just 80 more items and nobody can check whether the selection did anything at all.
      ZD's second note is stricter than a label on each item: the two kinds must not be poured into one pool.
      A representative pool sampled at the base rate is where honest numbers come from, while an enriched pool of hard cases is only for refining the guideline.

## Where we are
Nothing has been done here at all.
The sampling code is on disk at `lib/sample.py`, but nothing anywhere calls it: items are currently taken straight from the big pool, with no selection by position.

## Files
- `lib/sample.py`
  The picking code this face needs: it holds the distance and novelty scoring for hard cases, it already implements the two pools ZD asked for, and nothing calls it yet.
- `lib/classify.py`
  Where ZD's note redirects hard-case mining: the label-trained classifier, which is QD3, rather than raw embedding distance.
- `_source/note-update-v3-260721.md`
  ZD's 2026-07-21 notes; F5 and F6 are the two comments pinned on this face.

## Glossary
hard case: an item stuck on the border between two labels, where even a person is unsure; these are the ones most worth giving to a human, and they expose where the guideline fails to say enough.
turning text into a point in space: an off-the-shelf model turns each sentence into a string of numbers (coordinates), and sentences with close meanings land at close coordinates, which is what makes picking from the middle or from the border mean anything; that step is QD1.

## Discussion
> CC0723: everything this face calls picking by position rests on QD1 (how a sentence becomes a vector), so if the embeddings do not land, this is empty talk. The distance and novelty scoring for hard cases lives in `lib/sample.py`.

## Comments
- [ ] ZD 「pick by geometric position」 · 260721 1400
      note-update-v3 F5: vector geometry is not label geometry, so sitting close in the embedding does not mean carrying the same label ("I feel alive" and "I feel nothing" have very close coordinates and opposite labels).
      Mine the hard cases from a label-trained classifier (`classify.py`, which is QD3) instead of raw embedding distance, and delete the claim in the docs that the guideline reshapes the embedding.
- [ ] ZD 「typical cases you can tell apart at a glance」 · 260721 1400
      note-update-v3 F6: do not mix deliberately selected hard cases and representative items into one pool.
      Keep two pools: a representative pool sampled at the base rate, which is where honest numbers come from, versus an enriched hard-case pool used only for refining the guideline.
      `lib/sample.py` is already implemented along those two pools.

## Log
260725 · rewritten to the current face format in English
260723 1600 · migrated from the old `[Q4]`; the finish line was split into a checklist, the Diagram gained the three-region figure, and the face was linked to QD1
