# How to finish the remaining thousands
state: ⏸️ ON HOLD
owner: JL
method: (a) label everything, or (b) train a small classifier to take over

## Question
Once the guideline is final, how do the remaining thousands of items get labeled?

JL gave two routes in the meeting: (a) take the guideline and label all 5000 items, which is expensive, and (b) train a small model on the batch already labeled and let that model take over the rest, which saves money and time.
This is the last mile of the method.
The meeting ended without choosing (a) or (b), and while that stays open the corpus does not move: 48 items carry a label out of 5000.
The engine has already made the two routes coexist, because the three-tier cascade in QD2 runs Tier 0 embedding inheritance, Tier 1 small classifier, and Tier 2 model panel as one funnel, so inside the engine the choice turns into setting a threshold for how much work goes to the small classifier and how much wakes the model panel.
Whichever route JL picks, the small-classifier half of it lands on QD3, which owns how that classifier is trained.

## Boundary
- ✅ Covered here
  Which route finishes the corpus once the guideline is final: label everything with the guideline, or hand the rest to a trained small classifier, and which of the two JL picks.
- ↪ Covered elsewhere
  How that small classifier is trained is QD3; how the cascade divides the work between the cheap tiers and the model panel is QD2.

## Diagram
```
  Two routes came out of the meeting:
     (a) label all 5000 items with the guideline                 expensive
     (b) train a small model on the batch already labeled,
         and let it take over the rest                           cheaper and faster

  ⚠️ The meeting did not pick (a) or (b). Labeled so far: 48 of 5000.

  But the engine's three-tier cascade (QD2) already folds (a) and (b) into one machine:
     Tier 0 embedding inheritance + Tier 1 small classifier (= (b), see QD3)
                                  + Tier 2 model panel (= (a))
  so "pick a route" becomes "set a threshold": how much goes to the small classifier,
  and how much wakes the model panel.
```

## Items to Finish
- [ ] 🧠 Pick a route: (a) label everything, or (b) train a small classifier to take over
      JL decides between the two routes, and nothing else on this face can move until that call is made.
      The meeting produced both options and stopped there, which is why this face is parked rather than open: it is not waiting on evidence, on code, or on another face, it is waiting on a decision.
      The two routes cost very different amounts, (a) being the expensive one and (b) the one that saves money and time, and the engine can already express either of them, so the same call can also be made as a threshold inside the cascade rather than as a straight choice of one route over the other.
- [ ] 🏃 Run the chosen route through so all 5000 items carry a label
      The route JL picks has to be run once from end to end, until every one of the 5000 items has a label.
      Neither route has been run so far: nothing has gone through (a), and no small classifier has taken over under (b).
      Picking is not finishing, so this line stays open until the whole corpus comes out the other side labeled.
- [ ] 📊 Close the gap between 48 labeled items and the full 5000
      The count of labeled items is the progress signal on this face, and it currently reads 48 out of 5000.
      Nothing has moved that number since the meeting, because neither route has been run.
      It is kept as its own line so the size of the gap stays visible next to the two lines above it: a decision and a run are what change it, and until both happen the number stands still.

## Where we are
Neither route has been run.
Only 48 of the 5000 items are labeled so far.
The meeting did not pick (a) or (b), so this face sits on hold waiting for JL.

## Files
- `lib/classify.py`
  The small classifier that route (b) would hand the rest of the corpus to; how it is trained belongs to QD3.
- `ref/ref-cascade.md`
  The reference for the three-tier cascade: it describes the three tiers, their per-item cost, and roughly what share of items each one absorbs, which is where a route choice shows up as a threshold.
- `_source/note-update-v3-260721.md`
  ZD's note, the source of the comment pinned on this face.

## Glossary
train a small model to take over: use the few hundred items already labeled by people and by the models as teaching material, train a small fast dedicated model, then hand the remaining thousands to it, which saves money and time; this is QD3's Tier-1 classifier.

## Discussion
> CC0723: the technical implementation of (b) is QD3 (how the Tier-1 small classifier is trained), and how (a) and (b) coexist inside one cascade is QD2 (the three-tier funnel). This face is the method-level question of which route to take, QD3 is the engineering question of how to train it, and the two should not be mixed.

## Comments
- [ ] ZD 「Only 48 of the 5000 items are labeled so far.」 · 260721 1400
      ZD note-update-v3, closing hygiene (folded in from the old 01-license board, item ⑥): two B02 folders collide under `examples/Project-Subjective-Label/tasks/`.
      The disk has `B02_dim_conscientiousness` while the note writes `B02_dim_openness`, and openness already has its own `B03_dim_openness`; the branch `b03-openness` (commit f7e97f2) is unmerged.
      Numbering has to be unique, `INDEX.md` has to match what is on disk, and the branch has to be either merged or dropped, before rerun results can be cited.
      ⚠️ This one is housekeeping on the physical task folders, outside this board's method and engine scope, and it is pinned here only so it does not get lost.

## Log
260725 · rewritten to the current face format in English
260723 1600 · migrated from the old `[Q7]`; its relationship with QD2 and QD3 written into the Diagram and the Discussion
