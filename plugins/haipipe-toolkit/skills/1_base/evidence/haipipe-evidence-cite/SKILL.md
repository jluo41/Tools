---
name: haipipe-evidence-cite
description: "CITE evidence cards: someone else's paper, and any value or figure it reports, found by a discovery Task and read from its Run's result/ (the .bib for title, authors, year and venue; facts.md for the quoted sentence). External, drawn blue. One card is one discovery Task or Job holding many items, each tied to its sentences and anchor words. Writes CITE cards in a Task's evidence/cards.yaml, checks them, and turns a missing source into a proposal for haipipe-discovery. The card format, ordering and proposals are the door's, haipipe-evidence. Trigger: cite, CITE card, citation evidence, which paper backs this, quote the paper, facts.md, discovery evidence, /haipipe-evidence-cite."
metadata:
  version: "0.1.0"
  last_updated: "2026-10-16"
---

# /haipipe-evidence-cite · a paper backs this sentence

Split out of haipipe-evidence on 2026-10-16 (JL: "for the haipipe-evidence, could we have the haipipe-evidence-work
and haipipe-evidence-cite ... I think we might want to separate them now"). The door, `../haipipe-evidence/`, keeps
the card format, the narrative order, the proposals and `scripts/cards.py`; this skill owns how a CITE card is found,
filled and checked. Its code is `cards.py`'s `paper()` and `facts()`.

A CITE card is someone else's work, found by a discovery Task (haipipe-discovery). It is external, drawn blue.

## Where it lives

```text
<project>/discovery/bNN_<block>/jNN_<job>/tNN_<task>/
├── tNN_<task>.md                 its title: the first '# ' line, shown on the card
└── runs/rNN_<paper>/result/
    ├── <rNN_paper>.bib           one entry: title, authors, year, journal or booktitle
    ├── facts.md                  "- `F09` · Abstract sentence: "…" Locator: abstract S8."
    └── paper.pdf, runtime.yaml   the source and how it was read
```

## What a card shows

1. **Header**: `CITE 3 · b01.j21.t05 · <the Task's title>`.
2. **Per item**: its sentences (S5), the anchor words, the paper's title, then authors, year, venue and Run.
3. **The quote**: each `fact` id's sentence, so a reader sees exactly what the paper says.

## Choosing the topic

One card is one discovery Task: the question it answers ("Glucose forecasters with meal, insulin and activity
inputs"). Several papers under it are items, each tagged with its own sentence. A value a paper reports, like
"21.0 to 18.6 mg/dL", is a CITE item quoting the fact that holds it.

## When nothing backs a sentence

Write a `need` item on a "Sources still needed" card (no `source`), with `propose`: usually `{level: run, in:
<the Task whose question it falls under>}`, or `{level: task, in: <the Job>, name: tNN_<new question>}` when no
Task asks it yet.

## Commands

```text
python ../haipipe-evidence/scripts/cards.py check   <task>/evidence/cards.yaml   every CITE address, .bib and fact id
python ../haipipe-evidence/scripts/cards.py propose <task>/evidence/cards.yaml --write   needs → evidence/proposals.md
```

A ticked CITE proposal is made by haipipe-discovery (a new paper Run in a Task, or a new Task in the Job); when its
Run lands, the `need` item becomes `run` + `fact`.

## Grows here next

Checking a quoted fact against the paper's PDF, citation styles for delivery, and a novelty search for a "none
does X" claim are CITE work and belong in this skill when they are built.
