---
name: haipipe-insight-report
description: "Final synthesis report skill of the haipipe-insight family. Answers a specific research question by stitching the relevant D / I / K / W insights into a single citation-traced doc. NO code, pure markdown. Use after a /haipipe-insight-session reaches W-phase, or whenever a question-answering doc is needed. Trigger: report, final answer, synthesis doc, write report, answer the question."
argument-hint: [--question <Q>] [--project <path>] [--out <path>]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-insight-report
==============================

Produces a **question-answering report** by weaving relevant entries
from D / I / K / W into a single narrative with full citation trail.

NOT a separate knowledge layer. Just a presentation skill that compiles
existing insights into a readable doc.


Input
-----

```
examples/<project>/insights/INDEX.md
examples/<project>/insights/{D,I,K,W}_*/{O,P,K,W}*.md
examples/<project>/experiments/<NN>_<slug>/experiment.yaml   (for back-refs)
```


Output
------

Default:
```
examples/<project>/insights/reports/R{NN}_<slug>.md
```

Override with --out (e.g. write into paper/ directly).


Workflow
--------

```
Step 1: Parse --question; identify topic
Step 2: Search insights/ for relevant entries
  - Match question terms against entry titles, claim fields
  - Build candidate set across D/I/K/W
Step 3: Order entries: K (top) → I (support) → D (raw evidence) → W (next)
Step 4: Compose narrative per schema below
Step 5: Atomic write; update INDEX.md
```


Report schema
-------------

```markdown
# R{NN}: <question being answered>

- question:           "<full question>"
- written_at:         <ISO>
- author:             haipipe-insight-report
- scoped_to:          [K03, K05, I02, I07, O01, O03, W01]
- short_answer:       "<one-sentence direct answer>"

## TL;DR

<3-5 lines: the answer, in plain language>

## What we know (K-level)

<paragraphs, one per K entry, ordered by relevance>

## How we got there (I-level support)

<patterns that built up to the K above; cite specific P entries>

## Raw evidence (D-level, abbreviated)

<one row per cited O entry: experiment + key numbers>

## What we should do next (W-level)

<W entries that are still active and relevant to this question>

## Open questions

<things still unanswered; gaps in coverage>

## Citation trail

K03 ─┬─ P02 ─┬─ O01 (experiment 02_lhm_vs_baseline)
     │      └─ O03 (experiment 04_film_test_id)
     └─ P05 ─── O07 (experiment 07_param_matched)
W01 derives from K03
```


Definition of done
-------------------

- [ ] Report file written, non-empty
- [ ] Every claim in TL;DR or What-we-know cites at least one K/I/O
- [ ] No new statistics introduced (all numbers from cited entries)
- [ ] Citation trail diagram present at end
- [ ] INDEX.md updated


Risk profile
-------------

Writes one new report file. Read-only on everything else.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "R02 written: 'Does FiLM help on test-od?' answered no with K03+W01"
artifacts: [insights/reports/R{NN}_<slug>.md, INDEX.md]
next:      hand to F_paper for publication-form rewriting
```
