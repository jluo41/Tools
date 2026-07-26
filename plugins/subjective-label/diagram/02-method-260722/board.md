# Subjective labeling: the method, the engine, and a score we did not award ourselves
spine: Settle this subjective-labeling system: the labeling method JL described in the meeting, the engine underneath it (how a sentence becomes a vector, the three-tier cascade, training a small classifier), and an externally awarded score. For every step, pin down what it should look like and whether the code already does it.
close: Every Q below reaches ✅ SETTLED or ⏸️ ON HOLD. When they all land, the system is written down.

## Topic
Patients write reviews of their doctors online, and we want to label each review for a personality trait: agreeableness, conscientiousness, openness, and so on.
Every label takes one of three values, HIGH, LOW, or NONE.
Asking real people to label is slow and expensive, so a set of large language models stands in for a team of human annotators.
This board settles the labeling method JL described out loud in the meeting, together with the engine beneath it and one external validation, and for each step it records both what it should look like and whether the code already does it.

Cast: JL is the project lead, who supplies the method and makes the calls, and shows as 🧠 on the page. RA is the research assistant doing the work. CC is Claude Code, responsible for migration and for writing things down. ZD is the colleague whose 2026-07-21 notes are pinned as comments.

Words this board leans on. A guideline is the document stating what counts as HIGH, LOW, or NONE, which a model follows when it labels. The gallery is the set of answers JL personally confirmed, used as the ruler for measuring whether a model labels correctly. A construct is the trait being labeled. The cascade is the three-tier funnel that decides which items a cheap method can settle and which need an expensive one. A license is a score awarded by an outside dataset rather than by this project. The human ceiling is the agreement level real annotators reach on a public dataset, which is what makes a kappa number interpretable.

## Pipeline
```
QA · method        the labeling loop settled in the meeting, starting from 60 items
  QA1 build the first 60  →  QA2 label them independently  →  QA3 weak-model exam

QB · grow + verify  roll the sample up, verify every version
  QB1 60 → 140, hard cases  →  QB2 three-layer exam  →  QB3 an external license

QC · calls JL owes  open judgment, not open evidence
  QC1 when can the human let go · QC2 how to finish the remaining thousands
  QC3 what standard picks a construct

QD · engine         answers the "does the code do it" half of the spine
  QD1 sentence → vector ✅ · QD2 cascade ✅ · QD3 train the classifier 🟡
  QD4 generate the lexicon instead of hard-coding it 🔴
```
The two layers interlock. QB1 picks hard cases by standing on QD1; the implementation of QC2's "let a small classifier take over" is QD3; the cascade's Tier 0 in QD2 is QD1 itself; and QC3's construct standard is one of the gates QC1 needs before a human can let go.
QC3, QD4, and the ZD comments distributed across the other faces (F1 to F8) all come from `note-update-v3`; the former 01-license board folded into this one and was deleted.

## Pages
### QA · Method: the labeling loop settled in the meeting
How the first labels come into existence at all, before any gallery or guideline exists.
QA1-coldstart.md
QA2-split-label.md
QA3-weak-exam.md
### QB · Growing the sample and verifying each version
Roll 60 items up to 140 by hunting hard cases, examine the result in three layers, then have an outside dataset award the score.
QB1-grow-140.md
QB2-layered-eval.md
QB3-external-license.md
### QC · Calls JL owes
These are not waiting on evidence; they are waiting on a decision.
QC1-when-stop.md
QC2-scale-out.md
QC3-objective.md
### QD · Engine: how the machine actually runs
The layer under the method: vectors, the cascade, the small classifier, and the lexicon.
QD1-embedding.md
QD2-cascade.md
QD3-train-classifier.md
QD4-auto-lexicon.md

## Links
lib/embed.py          ../../lib/embed.py
lib/classify.py       ../../lib/classify.py
lib/license.py        ../../lib/license.py
lib/construct.py      ../../lib/construct.py
lib/converge.py       ../../lib/converge.py
lib/sample.py         ../../lib/sample.py
ref/ref-embeddings.md ../../ref/ref-embeddings.md
ref/ref-cascade.md    ../../ref/ref-cascade.md
ref/ref-datasets.md   ../../ref/ref-datasets.md
ref/ref-config.md     ../../ref/ref-config.md
note-update-v3        _source/note-update-v3-260721.md
workflow-audit        _source/260721-workflow-audit.txt
