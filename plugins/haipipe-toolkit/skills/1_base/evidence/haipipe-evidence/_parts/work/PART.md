---
name: work
part-of: haipipe-evidence
description: "VALUE evidence cards: our own result, made by a work Task and read from its Run's own output (a value at `file` + `key` in its result/, e.g. metrics.json rows_total), so the card never holds a copy that can go stale. Internal, drawn violet. One card is one work Task or Job holding many items, each tied to its sentences and anchor words. Writes VALUE cards in a Task's evidence/cards.yaml, checks the Run and the value, and turns a missing value into a proposal for haipipe-task. The card format, ordering and proposals are the door's, haipipe-evidence. Trigger: work evidence, VALUE card, our own result, value from a run, metrics, which run computed this number, /haipipe-evidence work."
metadata:
  version: "0.2.1"
  last_updated: "2026-10-26"
---

# /haipipe-evidence work · our own Run backs this sentence

Split out of haipipe-evidence on 2026-10-16 (JL: "for the haipipe-evidence, could we have the haipipe-evidence work
and haipipe-evidence cite ... I think we might want to separate them now"). The door, `../../`, keeps
the card format, the narrative order, the proposals and `scripts/cards.py`; this skill owns how a VALUE card is found,
filled and checked. Its code is `cards.py`'s `resolve()` for the two work-Run layouts and `work_value()`.

A VALUE card is our own result, made by a work Task (haipipe-task). It is internal, drawn violet.

## Where it lives

A work Run's result sits in one of two places; `cards.py` finds either:

```text
<project>/work/bNN_<block>/jNN_<job>/tNN_<task>/runs/rNN_<run>/result/      the Task keeps its Results
<project>/work/bNN_<block>/jNN_<job>/results/tNN_<task>/rNN_<run>/          the Job keeps its Tasks' Results
```

Tested on `Project-Samsung` `b51.j02.t01.r01` (the first) and `Proj32-CGM-Event-FixLenVec` `b04.j04.t02.r01`
(the second).

## What an item holds

1. **`run`**: the Run, so the number has a source a reader can open.
2. **`file` + `key`**: where the value is in the Run's own output, `metrics.json` and `rows_total` say; the
   script reads it, so the card never holds a copy that can go stale.
3. **`what`**: one line saying what the value measures.

## Choosing the topic

One card is one work Task: the analysis it ran. Values from the same Task are items on the same card. When a page
needs a value no Run computes yet, haipipe-task-for-evidence is the work Task type that computes values for a page.

## When nothing backs a sentence

A VALUE `need` item proposes `{level: run, in: <the work Task>}` to rerun or extend an analysis, or `{level: task,
in: <the work Job>, name: tNN_<analysis>}` for a new one, made by haipipe-task once a person ticks it.

## Commands

```text
python ../../scripts/cards.py check   <task>/evidence/cards.yaml   every VALUE Run and file + key value
python ../../scripts/cards.py propose <task>/evidence/cards.yaml --write   needs → evidence/proposals.md
```

A ticked VALUE proposal is made by haipipe-task (a rerun or new Run in a Task, or a new Task in the Job; a value made
for one page is haipipe-task-for-evidence's kind of Task).

## Grows here next

Refreshing every VALUE value when its Run reruns and flagging what changed, and checking a display's numbers against
the cards it is built on (b34_display), are VALUE checks and belong in this skill when they are built.
