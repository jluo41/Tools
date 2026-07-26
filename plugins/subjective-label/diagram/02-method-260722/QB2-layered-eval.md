# A three-layer exam, not a single number
state: 🟡 PARTIAL
owner: RA
method: three layers of our own, plus one external layer

## Question
When a guideline is revised, how do we know it genuinely got better instead of having memorized the items it already saw?

One aggregate agreement number hides where the method actually fails, which is why JL ruled that validation cannot rest on a single number and has to be run in layers: on the gallery, on older items to see whether rules that used to work were broken, and on items nobody has seen, which is what generalization means.
Each layer can fail on its own, and only the layered form says which one did.
The cost of leaving this open is already measured rather than suspected: the same guideline reached 0.93 agreement on items it had seen and 0.67 on items it had not.
While only the first layer is reported, every comparison between two guideline versions rests on a number that can be inflated in exactly that way, and any downstream claim that the method works inherits the same weakness.

## Boundary
- ✅ Covered here
  The three layers this project runs on itself: the gallery, older items that were labeled but are not in the gallery, and items never seen before.
- ↪ Covered elsewhere
  The fourth layer, a score awarded by an outside dataset rather than by this project, is QB3.
  How the sample itself grows from 60 to 140 by hunting hard cases is QB1.

## Diagram
```
  Every revised guideline reports three numbers at once:
    ① on the gallery                              did the change do anything
    ② on older items (labeled, not in the gallery)  did it break rules that used to work
    ③ on items never seen before                  does it still hold on new data (= generalization)
  ── one more layer ──►  ④ against outside people / public data (see QB3)

  The measured trap: one and the same guideline
     items it had seen → agreement 0.93   ⬅ layer ① only, and drawn entirely from what JL labeled
     items never seen  → 0.67             ⬅ the high score was only memorization
```

## Items to Finish
- [x] 🔁 Guideline versions are iterated and scored on the gallery
      Layer ① exists: every revision of the guideline is scored against the gallery.
      This was already in place when the question was opened, and it is still the only layer running.
      It answers one narrow thing, whether the change did anything on the answers JL has confirmed.
      It cannot say whether the change broke something older or whether it survives new data, which is why the three lines below exist.
- [ ] 📊 Every revision reports three numbers at once
      A revision counts as judged only when layer ①, layer ②, and layer ③ are reported side by side.
      Layer ① is the gallery, layer ② is older items that were labeled but are not in the gallery, and layer ③ is items nobody has seen before.
      Today only ① is reported.
      The three stay separate instead of being averaged because each fails for a different reason: ① says the change did something, ② says the change did not break rules that used to work, and ③ says the guideline still holds on new data.
      A single aggregate number cannot tell those three apart.
- [ ] 🎲 Layer ①'s items stop coming entirely from what JL labeled
      Layer ① no longer overlaps completely with the sample JL personally labeled.
      Right now that overlap is 100%, and it is what manufactured the 0.93/0.67 trap: the score is measured on the same material the guideline was built from.
      Until the overlap is broken, layer ①'s number reports familiarity rather than quality.
- [ ] 🌍 One more layer: compared against outside people or public data
      A fourth layer measures the guideline against outside people or a public dataset, and that layer is QB3.
      This face owns the three layers we run on ourselves, and all three are scores we award ourselves.
      QB3 owns the outside layer, a score awarded by an outside dataset rather than by this project.
      The line stays on this checklist because the exam is not complete without it, while the work of choosing the datasets and running them belongs to QB3.

## Where we are
Version iteration is running, but only layer ① is reported.
The items in that layer are drawn entirely from what JL has labeled.
The consequence was measured, not suspected: the same guideline reached 0.93 agreement on items it had seen and 0.67 on items it had not.
The high score was only memorization.
This is the most convincing "why" on the whole board.

- 260723 CC · 🧪 The 0.93/0.67 trap reproduced offline
      The self-test in `lib/converge.py` already reproduces the trap on offline data.
      That matters because the trap stops being an anecdote from one run and becomes something the code can demonstrate on demand, which is what makes the remaining three finish lines arguable rather than a matter of taste.

## Files
- `lib/converge.py`
  The convergence gate that keeps the three sets apart; its self-test already reproduces the 0.93/0.67 trap on offline data.
- `_source/note-update-v3-260721.md`
  ZD's notes, the source of the two comments pinned to this face: F1 on circular validation and F7 on the three sets.

## Glossary
agreement 0.93 / 0.67: a statistic between 0 and 1 for how much two sides agree, where 0 is guessing and 1 is identical; 0.93 looks high, but if it is high only on items already seen, it is memorization and does not count.
generalization: still labeling accurately on a fresh batch of never-seen data, which is what knowing how to label means as opposed to memorizing answers.
gallery: the set of answers JL personally confirmed, used as the ruler.
guideline: the document stating what counts as HIGH, LOW, or NONE.
held-out: a set of items set aside fresh each round that the guideline has never seen, used to measure generalization.

## Discussion
> CC0723: the finish line "one more layer, compared against the outside" expands into QB3, a score we did not award ourselves. This face owns our own three layers; QB3 owns the outside layer. The implementation is `lib/converge.py`, whose self-test already reproduces the 0.93/0.67 trap on offline data.

## Comments
- [ ] ZD 「The high score was only memorization.」 · 260721 1400
      ZD note-update-v3 F1: circular validation, where the guideline is fitted to labels the models produced and the same models then validate themselves.
      Three fixes at once: each round uses a held-out the guideline has never seen, the validating model is not the labeling model, and correctness is measured once on outside public data (see QB3).
- [ ] ZD 「The items in that layer are drawn entirely from what JL has labeled.」 · 260721 1400
      ZD note-update-v3 F7: drawing 24 random items each round makes versions incomparable and the variance large.
      Replace it with three sets that are never merged: a fixed anchor (at least 100 items, representative, never changed, used to compare versions), a held-out (fresh each round, measures generalization), and a rolling batch (the random 24 demoted to this role, used only to dig out hard cases).
      `lib/converge.py` already reproduces the 0.93/0.67 trap.

## Log
260725 · rewritten to the current face format in English
260723 1600 · migrated in from the old `[Q5]`; the finish lines were split into a checklist, layer ① ticked and the external layer linked to QB3
