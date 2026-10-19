# Asking: shape a question before any work

(Folded from the retired `haipipe-question-asking`, 2026-10-16. Invoke it as `/haipipe-report ask <folder>`.)

A question is shaped before any data is read or any work is done, so the answer cannot
shape the question. A question-asking method says what to fix first. Eight methods,
one card each in `ref/asking-methods/`; the cards' papers sit in the Insight workbench's
`servers/workbench-insight/related/papers.md` (its Guide › Related Paper).

How big a question is, and where it is recorded, is SKILL.md § Questions: a board's topic
holds several asks, and these methods shape one ask. Whether the shaped ask is a good
one is `ref/review.md`.


Which method when
-----------------

```text
What does the question need fixed first?
├─ its level                    By level              always first
├─ a goal it serves             By goal-question-metric
├─ its kind: describe, predict  By question type
│  or explain
├─ the number that answers it   By estimand
├─ a cause, from data already   By target trial      (future)
│  collected
├─ the analysis, before data    By analysis plan
├─ where it is asked, and       By partition and power
│  whether that is enough data
└─ the same plan on new data    By protocol reuse
```

A level is a kind of claim the answer may make. On an Insight board the levels are the
levels Data, Information, Knowledge and Wisdom; a Task Block or a paper names its own.
By partition and power and By protocol reuse come from the Insight workbench, where a
question is asked on partitions of one dataset and a Prototype is run on every dataset;
they apply wherever the same question is asked on several cuts or several datasets.


The cards
---------

| family | method | card |
|---|---|---|
| Question-asking | By level | asking-methods/01-by-level.md |
| Question-asking | By goal-question-metric | asking-methods/02-by-goal-question-metric.md |
| Question-asking | By question type | asking-methods/03-by-question-type.md |
| Question-asking | By estimand | asking-methods/04-by-estimand.md |
| Question-asking | By target trial | asking-methods/05-by-target-trial.md |
| Question-asking | By analysis plan | asking-methods/06-by-analysis-plan.md |
| Question-asking | By partition and power | asking-methods/07-by-partition-and-power.md |
| Question-asking | By protocol reuse | asking-methods/08-by-protocol-reuse.md |

Each card: the move, what it reads, what it returns, how it is tested (T0-T3 before any
work, T8 in use; the tests are listed in the Insight workbench's `servers/workbench-insight/guide/method.md`
§ 5), where it comes from; then what the literature says beside how it applies to AI. A
card marked `status: future` is a method to add later.


Return
------

```text
ask:      the shaped question, one thing, at its level
method:   the card used, and what it fixed
refused:  any word of the first wording the shaped ask drops, and why
```


Boundary
--------

Asking shapes; it never records or answers. Recording the question (its id, folder,
register) is SKILL.md § Questions; judging it is `ref/review.md`; on an Insight
board, its question file and its evidence plan are `haipipe-insight-question` and
`haipipe-insight-evidence-plan`. Turning a fuzzy research interest into a first
question is ideation's `framing-research-questions`.
