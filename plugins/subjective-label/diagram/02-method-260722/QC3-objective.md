# What standard picks a construct
state: 🔴 OPEN
owner: JL
method: pick one of two: downstream predictive power, or discriminance (separable from sibling traits)

## Question
When several large models each propose a construct candidate and the best one is then picked automatically, which standard (objective) does the picking use: downstream (can the label predict a downstream outcome, for example a physician's opioid prescribing volume) or discriminance (is the label separable from sibling traits)?

ZD's note-update-v3 Part 2 makes the point that this engine can run near-fully autonomously on exactly one condition, that a stated standard takes the place of a person's judgment.
Without an objective, "which construct and which label is right" is underdetermined and someone has to rule on it item by item; with one, it turns into a problem that can be optimized and automated.
The objective is the only human input that full autonomy keeps.
So while this stays open, QC2's auto-select has nothing to start from, and the scores QB2 produces cannot be judged good or bad.
The construct the objective picks is an operational construct, not the psychological trait a textbook describes, so the choice made here also decides what the resulting labels may honestly be called.
This face folded in from item ④ of the 01-license board.

## Boundary
- ✅ Covered here
  Which of the two objectives this project declares, downstream or discriminance, and the reason recorded next to the choice.
- ↪ Covered elsewhere
  When the human can let go of the loop is QC1, and this ruling is one of the gates it needs; running the auto-select over the remaining thousands is QC2; grading a resulting label set in three layers is QB2; the score awarded by an outside dataset is QB3.

## Diagram
```
  mode=auto: several large models each propose a construct definition and each labels a batch
        │
        ▼  score against the objective, keep the highest
     ┌─ downstream     the label predicts a downstream outcome (opioid-Rx regression)
     └─ discriminance  the label separates from sibling traits (conscientiousness, openness, ...)
        │
        ▼  then polish automatically against the disagreements between the models
     the picked construct = an operational construct, not the psychological trait in the textbook

  ⚠️ the objective is the one human input full autonomy keeps: without it, which construct
     and which label is right is underdetermined, and a person has to rule on it.
```

## Items to Finish
- [ ] 🧠 Pick one of the two and write down why
      JL names downstream or discriminance for this project and records the reason next to the choice, so this is a call waiting on him, not on more evidence.
      Both standards are already available in code, so nothing is blocked technically; what is missing is the declaration of what the labels are for in this project, which is what an objective states.
      Once it is named, construct auto-selection has a criterion to maximize and convergence has something to plateau against; until then every downstream judgment about a candidate is somebody's opinion.
- [ ] 📉 (a) If downstream is chosen: name the outcome and say how it is computed without moving PHI
      The choice is only usable once it says which downstream outcome the label is scored against and how that score is produced while the data stays where it must stay.
      CMS data is PHI: `_WorkSpace/1-CMS-Store` and `2-Data-Store` can only live on the secure server, so a real downstream score cannot be computed on a laptop.
      The way out, if there is one, is an aggregate measure that may legally be moved out of the secure environment and used as a proxy, which is exactly what this item has to pin down before downstream can be declared.
- [ ] 🧭 (b) If discriminance is chosen: use it for this round and push downstream to a later board
      This round runs on discriminance alone, and the downstream question moves to the next board rather than staying open here.
      Discriminance asks only whether the label separates from sibling traits, which needs no PHI and can therefore run now.
      Choosing it is the cheaper path and it closes this face for the current round, at the cost of leaving predictive validity unanswered until a later board picks it up.
- [x] 🛠 `lib/construct.py` implements both objectives and has been self-tested
      Both objectives are implemented and the self-test behaves: a good candidate wins, and redundant or degenerate candidates score 0.
      A redundant candidate copies a sibling trait, and a degenerate one is nearly constant, so a scoring rule that could not push both to the bottom would let the auto-selection pick a construct that carries no information.
      This is the part of the question that is already finished; what remains is not code but the declaration of which objective this project runs on.

## Where we are
The engine side is done and the project side is empty.
`lib/construct.py` supports both objectives and its self-test passes, but the standard for this physician project has not been named, so construct auto-selection has nothing to optimize.
⚠️ The blocker on the downstream branch is that CMS data is PHI: `_WorkSpace/1-CMS-Store` and `2-Data-Store` stay on the secure server, so a real downstream score cannot be run on a laptop unless some aggregate measure that may legally leave the secure environment stands in as a proxy.

## Files
- `lib/construct.py`
  It scores construct candidates against an objective and keeps the highest, so whichever standard is chosen takes effect here.
- `lib/converge.py`
  It reads `objective_score` when deciding whether a run has converged, which is the second place the same standard is used.
- `_source/note-update-v3-260721.md`
  ZD's 2026-07-21 note, whose Part 2, Part 3, and Part 10 are where the objective, the objective-driven construct selection, and the operational-construct boundary come from.

## Glossary
objective: the standard used when picking among construct candidates and when judging convergence (downstream / discriminance / dataset_match); it is the one piece of human input in this engine that cannot be automated away.
downstream: whether the label predicts a downstream outcome, for example a physician's opioid prescribing volume.
discriminance: whether the label separates from sibling traits.
operational vs theoretical construct: what an objective picks is the labeling that best serves the stated purpose, which is not necessarily the psychological trait in the textbook sense; unless it separately passes a construct-validity cross-check, it may not simply be called "openness".

## Comments
- [ ] ZD 「The objective is the only human input that full autonomy keeps.」 · 260721 1400
      ZD's note-update-v3 Part 2 and Part 3: in the whole flow only three places still need a person, stating the objective (once per construct family, and it is already part of the research design), signing the engine license (once in the engine's lifetime), and manual review of extreme cases (optional, and it can be switched off). Everything else runs automatically. This question is the first of those three.
- [ ] ZD 「The construct the objective picks is an operational construct, not the psychological trait a textbook describes, so the choice made here also decides what the resulting labels may honestly be called.」 · 260721 1400
      ZD's note-update-v3 Part 10, the honesty boundary: a construct selected by an objective has to be reported as an engineered feature and cannot simply be claimed to be "openness". It also warns about objective-gaming, since an auto-selected construct can exploit confounds, and the backstop is a downstream held-out: does it still predict on data it has never seen?

## Log
260725 · rewritten to the current face format in English
260723 1615 · created: folded in from item ④ of the 01-license board; absorbed ZD's note-update-v3 Part 2, 3, and 10 (the objective is the only human input autonomy keeps, plus the operational-construct honesty boundary)
