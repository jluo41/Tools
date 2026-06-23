# Plain Mental Model

Imagine your project has two kinds of memory.

## Working Memory

Working memory is where things happen:

```text
tasks/          runs, metrics, artifacts
probes/         hypotheses, verdicts, caveats
discover/       papers, external sources, notes
narratives/     story drafts, claim gaps, arguments
applications/   question-driven sessions and reports
```

These folders can be messy because they are where work is produced.

## Permanent Memory

Permanent memory is `insights/`. It should be much smaller. It only keeps cards
that future work can reuse.

```text
insights/
  D_data/          what one dataset looks like
  I_information/   the pattern inside that dataset
  K_knowledge/     does the pattern generalize (+ confidence)
  W_wisdom/        what to do, tuned to that confidence
```

## The One Cut To Remember

The whole model turns on one line: **in-sample description vs out-of-sample
generalization.**

```text
D and I  describe ONE dataset (in-sample). They never claim anything beyond it.
K        is the leap: does the pattern hold beyond the sample? K carries the
         confidence of that leap.
W        acts on K, more boldly or more cautiously depending on K's confidence.
```

Two rules fall out of this:

1. **D and I name their dataset.** A D card says what one dataset looks like
   (size, composition). An I card says what pattern is inside that same dataset.
   Both write down which dataset they mean.
2. **The p-value lives at K, not at I.** A regression gives you two things, and
   they go to two layers:

```text
coefficient / direction / magnitude   -> I   ("in this dataset, X and Y move together, +4.39")
p-value / CI / significance / confidence -> K ("...and that holds in the population, p<.001")
```

If you see a p-value or a confidence level, you are looking at a K.

## K Has No Gate

K is not a prize you earn with an experiment. It is just the layer where a
generalization claim is recorded, together with how sure you are.

```text
strong belief    "X generalizes, p<.001, holds across subgroups"   -> K (high)
weak belief      "X might generalize, only in aggregate"           -> K (low)
negative belief  "X does NOT generalize here (ns)"                 -> K (low/neg)
```

You record the weak and negative ones too. A low-confidence K is not withheld —
its confidence just tells W to be cautious. An archive that keeps only the wins
cannot support a careful decision later.

## Why Review Exists

Without review, every result could become a card, and the base gets noisy.
Review is the filter:

```text
source folder
  -> review: what is worth keeping?
  -> INSIGHT_REVIEW.yaml: proposed card actions
  -> apply: write accepted cards
```

Review does not invent claims. It inspects finished material and decides whether
it deserves a permanent card.

## What A Card Should Be

One card = one reusable unit.

Good K card:

```text
K03: "The model's validation gain does not generalize to OOD cases."
```

Too broad:

```text
K03: "Everything we learned about the model."
```

Too small:

```text
D17: "Run finished at 2:13pm."
```

If the card is too broad, split it. If it is too small, skip it. If it supports
an existing card, merge or update instead of duplicating.
