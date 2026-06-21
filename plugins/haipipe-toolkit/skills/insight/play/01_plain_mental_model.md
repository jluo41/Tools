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

Permanent memory is `insights/`.

It should be much smaller. It only keeps cards that future work can reuse.

```text
insights/
  D_data/          one useful observation
  I_information/   one useful pattern
  K_knowledge/     one judged belief
  W_wisdom/        one K-backed action
```

## Why Review Exists

Without review, every result could become a card. That makes the insight base
too noisy.

Review is the filter:

```text
source folder
  -> review: what is worth keeping?
  -> INSIGHT_REVIEW.yaml: proposed card actions
  -> apply: write accepted cards
```

Review does not invent new claims. It only inspects finished material and asks
whether that material deserves a permanent card.

## What A Card Should Be

One card should contain one reusable knowledge unit.

Good card:

```text
K03: "The model's validation gain does not transfer to OOD cases."
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
an existing card, merge or update that card instead of creating a duplicate.
