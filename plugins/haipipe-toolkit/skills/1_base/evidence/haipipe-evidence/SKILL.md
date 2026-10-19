---
name: haipipe-evidence
description: "Find the evidence a claim needs and show it as cards: CITE (someone else's paper, from a discovery Run, external, blue) and WORK (our own result, from a work Run, internal, violet). One card is one topic, a discovery or work Task or Job, holding many items; each item names the sentences it backs, the exact words it backs (anchor), and the Run it comes from. Reads the paper, quoted fact or value from the Run's result/, orders cards by the narrative, checks every address, and for each missing piece flags a proposal (a new Run, Task, Job or Studio topic, proposed by evidence, for a stated purpose) for a person to tick. Used by any page that needs support: a Section canvas, a Page's Evidence Space, a report, slides. Trigger: evidence, evidence card, CITE, WORK, find the evidence, what backs this sentence, missing evidence, propose a run for evidence, /haipipe-evidence. Also a Page's evidence Runs (the old haipipe-draft-evidence, now ref/page-evidence.md): page evidence, evidence Run, land evidence items, embed the result, fold evidence, /haipipe-draft-evidence."
metadata:
  version: "0.4.0"
  last_updated: "2026-10-16"
---

# /haipipe-evidence · what backs each sentence, and what to make when nothing does

It stands beside haipipe-draft (the words) and haipipe-display (the figures): evidence is needed wherever a claim
is made, not only in a Draft (JL 261016: "we can find the evidence we need, in many other scenarios"). It reads and
proposes; it never runs a discovery or a work Task itself, and it never writes the text.

## 🗂 Two kinds, by where the evidence comes from

```text
kind   comes from                         colour   example card
CITE   discovery/ world (external paper)  blue     CITE 3 · b01.j21.t05 · Glucose forecasters with meal ... inputs
WORK   work/ world (our own Run)          violet   WORK 1 · b51.j02.t01 · Lab against the Hopkins design
needed either, no source yet              red      CITE 2 · Sources still needed
```

A value or a figure a paper reports is CITE ("if the value is from the citation, then it should be the Ecite",
JL 261016). A figure or table built on evidence is a Display (haipipe-display), not a kind of evidence card. How to
find, fill and check each kind is its own skill (split 261016, JL: "I think we might want to separate them now"):

```text
haipipe-evidence        the door: card format, narrative order, proposals, scripts/cards.py, a Page's evidence Runs
├── haipipe-evidence-cite   CITE: a discovery Run's .bib and facts.md; proposals to haipipe-discovery
└── haipipe-evidence-work   WORK: a work Run's value at file + key; proposals to haipipe-task
```

## 📁 Where the cards live

In the Task, beside the words and the figures, one writer each (JL 261016):

```text
tNN_<task>/
├── draft/       haipipe-draft      the words; reads evidence/ and display/
├── evidence/    haipipe-evidence   cards.yaml · proposals.md
└── display/     haipipe-display    Display<n>-<slug>/, each built_on evidence cards
```

A canvas or a report only reads `evidence/cards.yaml`; it never keeps its own copy. A Studio face holding `evidence:`
in its yaml still works (`--key`) for a page made before the folder existed. First moved: b21's C2 cards, now in
`studio/s04-task21-updated-draft/evidence/`.

## 🧾 The card format

`evidence/cards.yaml` holds the list under `evidence:`:

```yaml
evidence:
  - kind: cite                      # cite | work
    source: b01.j21.t05             # the topic: a Task (bNN.jNN.tNN) or a Job (bNN.jNN)
    items:
      - {run: r02, for: [5], anchor: ["30-minute error from 21.0 to 18.6 mg/dL"], fact: [F09, F11]}
  - kind: work
    source: b51.j02.t01
    items:
      - {run: r01, for: [7], anchor: ["12 rows"], file: metrics.json, key: rows_total, what: "rows checked"}
  - kind: cite
    title: "Sources still needed"   # no source: a list of needs
    propose_in: b01.j21             # where its proposals go by default
    items:
      - {need: "a CDC source for the count", for: [1], anchor: ["More than 38 million"],
         propose: {level: run, in: b01.j21.t01}}
```

1. **`run`** completes the address: `rNN` under a Task, `tNN.rNN` under a Job.
2. **`for`** names the sentences; **`anchor`** the exact words, boxed in the text by the page's builder.
3. **`fact`** quotes lines of a discovery Run's `facts.md`; **`file` + `key`** read a work Run's own output.
4. **`need`** marks what is missing; **`propose`** says what to make for it.

## 🔧 The script

`scripts/cards.py`, imported by builders and run by hand:

```text
python cards.py check   <task>/evidence/cards.yaml [--sentences s.json]   every address, fact, value, anchor
python cards.py propose <task>/evidence/cards.yaml [--page <name>] [--write]   writes evidence/proposals.md
```

An address resolves in the Project's own world: `<project>/discovery/` for CITE, `<project>/work/` for WORK, the
Project being the folder that holds `project.yaml`. A Run is found as `tNN_*/runs/rNN_*/result/` or, for a Task whose
Results sit in its Job, `jNN_*/results/tNN_*/rNN_*/`. `order()` sorts cards by the first sentence each backs (the
narrative), CITE and WORK in one sequence, numbered within their kind. A builder calls `check()` first and stops on
any problem, so a canvas never shows a card that does not resolve.

## ⚑ Proposing what to make

When evidence is missing, the card says so and the skill flags what would fill it (JL 261016: "flag the ticket, and
flag what to run, flag the new job, and also propose the sNN ... propose the new task or run and flag it is proposed
by evidence and for xx purpose"):

```text
need ─▶ propose: {level, in, name} ─▶ evidence/proposals.md  - [ ] new discovery run in b01.j21.t01
                                                               · proposed by evidence (CITE 2, b21-s05 S1)
                                                               · for: a CDC source for the count
person ticks [x] ─▶ the level's own skill makes it ─▶ its Run fills the item ─▶ the need becomes a run
```

1. **Levels**: `run` (in an existing Task), `task` (a new Task in a Job), `job` (a new Job in a Block), `topic` (a Studio sNN).
2. **Makers**: discovery Runs and Tasks by haipipe-discovery, work ones by haipipe-task, Jobs by haipipe-job, topics by haipipe-studio.
3. **Ticks are kept**: `--write` rewrites the file and keeps every `[x]`; a proposal whose need is gone drops out.
4. **Nothing is made before the tick**, and this skill makes nothing itself.

## 🧱 A Page's evidence Runs

A Page's evidence is landed and embedded by the Runs `run-value-<slug>`, `run-display-<slug>` and `run-citation-<slug>`:
LAND executes each decided Evidence Item graph, EMBED folds the ready Result into the next outline version. This was
the skill haipipe-draft-evidence until 2026-10-16 (s41-D11); the text is `ref/page-evidence.md`, the Run names are
unchanged, and Pages made before then keep working. The producer is `haipipe-draft-evidence-agent`.

## 🔗 Who calls it

1. **A Page's evidence Runs** (`ref/page-evidence.md`): a Page's LAND and EMBED read and bind cards in this format.
2. **haipipe-task-for-evidence**: a work Task that computes values for a page; its Runs become WORK items.
3. **Section canvases** (b21 s05 first): CITE and WORK cards along the bottom, anchors boxed in the text.
4. **Reports and slides**: any claim that needs a backing card.
