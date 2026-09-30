---
name: subjective-label-evaluation
description: >-
  The Quality › Evaluation view skill of the subjective-label family: it
  qualifies executors on the locked test: one prediction and one scorecard per candidate, then the preregistered selection. Every Run in this view names this skill, and no other view uses it.
  Use for executor evaluation, executor-predict, executor-score, executor-select, scorecards, baseline, choosing the model, or /subjective-label-evaluation.
metadata:
  version: "0.1.0"
  last_updated: "2026-09-29"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /subjective-label-evaluation · Quality Space › Evaluation

This skill owns the Runs of the labeling workbench's Quality › Evaluation
view: every Run card there names it, and no other view uses it (JL 260929:
one skill per view). Load `subjective-label` (the family door),
`subjective-label-workflow` (the Run graph) and `label-scanning` (who decides what) first. Which Run
comes before and after these is in `label-scanning-workflow`.

## Runs in this view

```text
step  Run Type                     state
15    executor-predict     not built · one per candidate and baseline
16    executor-score       not built · one per closed prediction
17    executor-select      not built
```

A new Run uses `run-labeling-<operation>-<MMDD>-<target>` on disk and
on the page. Older short-named Tickets remain readable. Its Ticket is
`<Page>/runs/<run>.yaml`
and its Result `<Page>/results/<run>/`, beside `labeling/`.

```text
SCORE
 7 predict    allocate one executor-predict per registered candidate and baseline, gold hidden;
              every Run closes before any score is computed       → evaluation/predictions/<executor>.jsonl
                                                                    evaluation/baselines/
 8 score      allocate one executor-score per closed prediction: absolute, per class,
              per region, uplift, held-out family, stability, cost, failures, intervals
                                                                  → evaluation/scorecards/<executor>.json
 9 select     allocate executor-select; apply the preregistered rule
                                                                  → evaluation/summary.md
```

Step 7 may not start before `lock.json` exists; step 8 may not start while any
candidate prediction Run is open.

## Return

Return the Run address or `none`, the files written, and exactly one next
runnable Run or named human gate.
