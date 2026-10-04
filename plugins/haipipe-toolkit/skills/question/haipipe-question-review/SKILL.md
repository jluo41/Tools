---
name: haipipe-question-review
description: >-
  Judge whether a question is a good question before any work is done on it, by seven
  tests (Q1 one thing, Q2 logic, Q3 consumer, Q4 level, Q5 answerable, Q6 new, Q7 open),
  and propose one verdict per question: keep, split, merge or move, each with its
  reason. Run by an agent that did not write the question; it proposes and a person
  signs; a signed change retires the old question, never edits it. Any board's asks:
  an Insight question, a Task Block's question, a paper's research question. Trigger:
  review the questions, question review, Q1-Q7, is this a good question, split or merge
  questions, /haipipe-question-review.
allowed-tools: Read, Grep, Glob
metadata:
  version: "0.1.0"
  last_updated: "2026-10-03"
  # version history: ./CHANGELOG.md
---

# /haipipe-question-review · is this a good question?

Whether a question is good is judged before any work is done on it, by a reviewer that
did not write it. The review judges an **ask**, one question that one piece of work
answers; a board's **topic** is judged by `haipipe-question`'s report test instead
(could it fill a report's Answer, Evidence, Limits and Next?).


The seven tests
---------------

```text
Q1 one thing     the ask asks one question; two joined by "and" are two questions
Q2 logic         what would answer it forms one argument from the observed to the
                 answer: each step is read by the next
Q3 consumer      it names who waits on the answer (a higher question, a design, a
                 decision, a replication) and what they do with it
Q4 level         the ask belongs at its level: it claims no more than its level allows
Q5 answerable    the data or the work can carry it, or the refusal is itself shown
Q6 new           no other question already asks it or computes the same thing
Q7 open          no preferred answer: a null and "do nothing" stay admissible
```

Q4 takes its levels from the board. On an Insight board they are the rungs: Data
observes, Information derives with no cause word, Knowledge claims with rivals, Wisdom
counsels (`haipipe-insight-question` adds that rule and the rung's legal evidence).


The verdict
-----------

One verdict per question, each with its reason:

```text
keep    the question passes, as worded
split   two or more asks: the small asks, and the one line of logic that joins them
merge   it asks what another question asks: the question it joins
move    it belongs at another level or on another board: where, and why
```

**It proposes; a person signs.** Nothing is split, merged, moved or reworded by a rule or
by the reviewer. A signed change retires the old question with its reason and a
successor id, and never edits it in place; a question carried over from an older board
keeps its words until a signed change replaces them.


Return
------

```text
question:  id and wording, as read
tests:     Q1-Q7, each pass or the problem in one line
verdict:   keep | split | merge | move, with its reason
proposal:  the new asks or the target, for a person to sign
```


Boundary
--------

This skill judges; it never rewords, records or answers. Shaping an ask is
`haipipe-question-asking`; recording a question is `haipipe-question`; on an Insight
board the question file, its register and its gate are `haipipe-insight-question`, and a
mechanical check that flags suspects for Q1, Q2, Q4 and Q6 is `haipipe-insight-check`.
