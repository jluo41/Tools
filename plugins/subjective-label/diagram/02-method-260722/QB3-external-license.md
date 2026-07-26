# A score we did not award ourselves
state: 🟡 PARTIAL
owner: RA
method: run on public per-rater datasets (the battery) and see whether kappa reaches the human ceiling

## Question
Our own 0.93 came out of an exam whose items the guideline author had already seen and had personally labeled, so it does not count: how do we get a score that we did not award ourselves?

The engine is written but it has never run on real data, and until it has, we cannot tell anyone outside the project that this method works.
Correctness can only be borrowed from outside.
One kind of public dataset makes that possible: the kind that keeps every individual annotator's raw score (per-rater) instead of publishing only the merged answer, because those raw scores show how much real people disagree with each other, and that is the human ceiling.
Without a human ceiling there is nothing to read a kappa against.
Reaching that ceiling on the battery is what awards the engine an autonomy license, which is one-off and engine-level: a new construct inherits the same credibility, as long as it is adjacent to the battery and the distance is written down.
This face is also the expansion of QB2's fourth line, the one that adds a comparison against something external: QB2 owns the three internal layers, and this face owns the correctness borrowed from outside.

## Boundary
- ✅ Covered here
  The externally awarded score: which public per-rater datasets make up the battery, the human ceiling read off each of them, the engine's kappa against that ceiling, and the license that follows.
- ↪ Covered elsewhere
  The three internal layers of the exam belong to QB2's layered evaluation and this face is only its fourth, external layer; the standard that picks a construct (the objective) is QC3.

## Diagram
```
  exam setter = exam taker  ──►  0.93   but on unseen items → 0.667   ⬅ a hole in the method

  the way out: correctness can only be borrowed from outside
     one kind of public dataset is special: it keeps EVERY human annotator's raw score (per-rater)
        └─► so we can compute how much real people disagree with each other = the human ceiling
     run the engine on that set of datasets (the battery); kappa reaching the ceiling = an autonomy license
        └─► one-off, engine-level: a new construct inherits the same credibility (it must be adjacent to the battery, and how far must be written down)
```

## Items to Finish
- [x] 🧪 `lib/license.py` passes its self-test
      Well-formed data returns PASS and random numbers return BELOW.
      This only shows that the scoring code behaves the way it is meant to on inputs we built ourselves.
      It says nothing about whether the engine reaches the human ceiling, because the module has never seen a real dataset.
      It is the one box on this face that is closed.
- [ ] 📋 The battery list is settled · 🧠 waiting on JL
      Every dataset on the list carries two things: what its human ceiling kappa is, and why it was chosen.
      The candidates come from RA's survey P02: POPQuorn, DICES, GoEmotions, and LeWiDi.
      This is a JL call rather than an RA call because the list decides how wide the license ends up being: the more varied the battery, the wider the license.
      GoEmotions is the awkward candidate, since it labels emotions rather than personality traits, so putting it in means first working out what it would actually prove.
- [ ] 🏃 The whole engine runs on the battery for real
      One row lands per dataset: name, sample size, engine kappa, human ceiling, pass or not.
      Nothing has touched real data yet and not one dataset has been downloaded, so this is the line that separates a module that passes its own self-test from a method someone outside the project would believe.
      The shape of the row is the point: an engine kappa on its own says nothing, and it only becomes readable next to the human ceiling from the same dataset.
- [ ] 📝 One overall verdict, with the license's coverage stated honestly
      Write the verdict, say which kinds of construct this license covers and which it does not, then write it into `ref/ref-datasets.md`.
      The license only covers constructs adjacent to the battery, and how far that adjacency stretches has to be reported rather than assumed.
      Putting it in `ref/ref-datasets.md` is what keeps the claim somewhere it can be read back later, instead of living in whatever the run happened to print.

## Where we are
`lib/license.py` is written and has passed its self-test (well-formed data judged PASS, random numbers judged BELOW), but it has never touched real data, and not a single real dataset has been downloaded yet.
The candidates come from RA's survey P02: POPQuorn, DICES, GoEmotions, and LeWiDi.
⚠️ GoEmotions labels emotions, which is not the same thing as a personality trait, and it has already measured out at a kappa of only 0.25 to 0.30, so putting it in means first being clear about what it would prove.
Two JL decisions are holding this face down: the battery list, and the objective standard (the objective standard itself is QC3).

## Files
- `lib/license.py`
  Computes the engine's kappa against the human ceiling and returns PASS or BELOW; self-tested, never run on real data.
- `ref/ref-datasets.md`
  Where the battery, each dataset's human ceiling, the run results, and the license verdict get written down.
- `ref/ref-config.md`
  Holds the config field that names the battery, `license: {battery: [...]}`.
- `_source/note-update-v3-260721.md`
  ZD's design note; its F2 (construct transfer) and F3 (human ceiling) are the two comments pinned on this face.

## Glossary
battery: the set of public datasets used to examine the engine (the field name `license: {battery: [...]}` in `ref-config.md`).
autonomy license: a one-off certification; the engine reaches the human ceiling on the battery, and from then on a new construct inherits the same credibility.
human ceiling: the agreement real annotators reach with each other, which is our upper bound.
per-rater: the dataset keeps every single annotator's raw score, instead of publishing only the merged "gold answer".

## Discussion
> CC0723: This face was folded in from the old board `01-sublabel-license-260722`, and what was folded is its **validation core** (the old ①battery / ②license-run / ⑤rerun-3dims). The other three items on the old board each found a home too: ③auto-lexicon → QD4 · ④objective → QC3 · ⑥b02-naming → a comment on QC2.
>> CC0723: The old board was deleted once the fold was done; ZD's original design documents (note-update-v3 + workflow-audit) moved into this board's `_source/`, and board.md's ## Links points there.

## Comments
- [ ] ZD 「a new construct inherits the same credibility」 · 260721 1400
      ZD note-update-v3 F2: the construct transfer gap, where you validate on dataset A and then claim it holds on B. The license only covers constructs that are adjacent to the battery, and how far the adjacency stretches must be reported honestly rather than assumed. The more varied the battery, the wider the license.
- [ ] ZD 「Without a human ceiling there is nothing to read a kappa against」 · 260721 1400
      ZD note-update-v3 F3: with no human ceiling, a kappa being high or low has nothing to be measured against. The ceiling comes from public per-rater datasets (which keep every annotator's raw score) and is amortized once at engine level, not recomputed by each project separately.

## Log
260725 · rewritten to the current face format in English
260723 1615 · ③④⑥ each found a home (QD4 / QC3 / a QC2 comment); the old board deleted and ZD's originals moved into `_source/`; ZD's F2/F3 comments added
260723 1600 · Created: the validation core folded in from `01-sublabel-license-260722` (0.93 does not count → borrow from outside → license)
